"""Prepare and package separate, reviewed three-part releases; never submit orders.

CAD generation remains revision-specific. See docs/new-revision.md.
"""
from pathlib import Path
import argparse
import copy
from datetime import date
import hashlib
import revision_json as json
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ROLES = ('body', 'faceplate', 'radiator')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file(root, name):
    path = (root / name).resolve()
    require(not Path(name).is_absolute() and path.is_relative_to(root.resolve()),
            f'Path must stay inside the repository: {name}')
    return path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def canonical(root):
    parts = read(root / 'cad/current-release.json')['parts']
    suffixes = {'body':'-BODY', 'faceplate':'-FACEPLATE', 'radiator':'-PLATE'}
    result = {}
    for role, suffix in suffixes.items():
        matches = [part for part in parts if part['part'].endswith(suffix)]
        require(len(matches)==1, f'Canonical selection must identify one {role}')
        result[role] = matches[0]
    require(len(parts)==3, 'Expected the three custom parts')
    return result


def initialise(root, name, changes):
    require(re.fullmatch(r'[a-z][a-z0-9-]{0,47}', name), 'Use a short lowercase release name')
    require(changes and set(changes) <= set(ROLES), 'Choose body, faceplate and/or radiator')
    manifest = root / f'cad/releases/{name}.json'
    require(not manifest.exists(), f'Release already exists: {manifest}')
    selected = canonical(root)
    rows, configs = [], {}
    for role, original in selected.items():
        part = {k:copy.deepcopy(original[k]) for k in
                ('part', 'manufacturing_revision', 'source', 'step', 'drawing', 'dxf', 'pdf_sheets', 'jlc', 'quantity')}
        part.update(role=role, changed=role in changes, review_images=[], verification=None)
        if role in changes:
            manufacturing_revision = changes[role]
            require(re.fullmatch(r'[A-Z][A-Z0-9]*-M[0-9]{2}', manufacturing_revision), f'Invalid revision: {manufacturing_revision}')
            stem = original['part'].replace(original['manufacturing_revision'], manufacturing_revision)
            config_path = root / f'cad/manufacturing/{manufacturing_revision}.json'
            require(not config_path.exists() and config_path not in configs, f'Manufacturing revision already exists: {manufacturing_revision}')
            require(not (root / f'output/manufacturing/{manufacturing_revision}').exists(), f'Output revision already exists: {manufacturing_revision}')
            config = read(file(root, original['source']))
            config.update(manufacturing_revision=manufacturing_revision, part_number=stem, manufacturing_revision_date=date.today().isoformat(),
                          source_manufacturing_revision=original['manufacturing_revision'], status='Draft; not reviewed or submitted',
                          scope='Draft starting values; update geometry and fabrication requirements')
            for key in ('geometry_change', 'nominal_geometry_unchanged'):
                config.pop(key, None)
            for key in ('submission_performed', 'supplier_submission_performed'):
                if key in config:config[key] = False
            configs[config_path] = config
            part.update(part=stem, manufacturing_revision=manufacturing_revision, source=f'cad/manufacturing/{manufacturing_revision}.json',
                        step=f'output/manufacturing/{manufacturing_revision}/{stem}.step',
                        drawing=f'output/pdf/{stem}.pdf',
                        dxf=f'output/manufacturing/{manufacturing_revision}/{stem}.dxf' if original['dxf'] else None,
                        verification=f'output/manufacturing/{manufacturing_revision}/geometry-verification.json')
            part['jlc']['remarks'] = 'TODO: write manufacturing-only remarks for this revision'
        rows.append(part)
    value = dict(schema_version=2, name=name, status='draft', parts=rows,
                 note='Starting configurations only; adapt builders/checks/drawings before review. Current delivered selection is unchanged.')
    # Validate every destination before writing anything.
    for path, config in configs.items():write_new(path, config)
    write_new(manifest, value)
    return manifest


def inputs(root, manifest):
    data = read(manifest)
    require(data['status'] == 'draft', 'Expected a draft manifest')
    name = data['name']
    require(re.fullmatch(r'[a-z][a-z0-9-]{0,47}', name), 'Invalid release name')
    require(manifest.resolve() == (root / f'cad/releases/{name}.json').resolve(), 'Unexpected manifest path')
    parts = data['parts'];base = canonical(root)
    require(len(parts) == 3 and {p['role'] for p in parts} == set(ROLES), 'Select exactly one of each part')
    require(any(p['changed'] for p in parts), 'Use the existing order guide for an unchanged repeat order')
    require(len({p['part'] for p in parts}) == 3, 'Duplicate part number')
    protected = {p[k] for p in base.values() for k in ('source', 'step', 'drawing', 'dxf') if p[k]}
    paths = {str(manifest.relative_to(root))}
    for part in parts:
        role=part['role'];old=base[role]
        require(isinstance(part['quantity'], int) and part['quantity'] > 0, 'Quantity must be a positive integer')
        expected = part['jlc']
        require(all(expected.get(k) for k in ('category','material','finish','remarks')), 'Complete supplier metadata')
        require(isinstance(expected.get('threads'), bool), 'Specify whether threads are required')
        require('TODO' not in expected['remarks'], f"Complete remarks for {part['part']}")
        for field, ext in [('step','step'),('drawing','pdf'),('dxf','dxf')]:
            if field=='dxf' and role=='body':
                require(part[field] is None, 'Body uses STEP/PDF only');continue
            require(Path(part[field]).name == f"{part['part']}.{ext}", f'Mismatched {field} filename')
        if not part['changed']:
            for key in ('part','manufacturing_revision','source','step','drawing','dxf','pdf_sheets','jlc'):
                require(part[key] == old[key], f'Unchanged {role} differs in {key}; allocate a new revision')
            require(sha(file(root, old['manufacturing_revision_bundle'])) == old['sha256'], 'Changed original archive')
            with zipfile.ZipFile(file(root, old['manufacturing_revision_bundle'])) as archive:
                for field in ('step','drawing','dxf'):
                    if old[field]:require(archive.read(Path(old[field]).name) == file(root, old[field]).read_bytes(),
                                          f'Unchanged {role} no longer matches its released ZIP')
            paths.add(old['manufacturing_revision_bundle'])
        else:
            require(re.fullmatch(r'[A-Z][A-Z0-9]*-M[0-9]{2}', part['manufacturing_revision']), 'Invalid revision')
            require(part['part'] == old['part'].replace(old['manufacturing_revision'],part['manufacturing_revision']) and part['manufacturing_revision'] != old['manufacturing_revision'],
                    'Changed parts need a new revision and matching part number')
            for field in ('source','step','drawing','dxf','verification'):
                if part[field]:require(part[field] not in protected, f'Cannot reuse delivered {field}')
            require(part['source'] == f"cad/manufacturing/{part['manufacturing_revision']}.json", 'Unexpected source configuration')
            for field in ('step','dxf','verification'):
                if part[field]:require(Path(part[field]).parent == Path(f"output/manufacturing/{part['manufacturing_revision']}"),
                                       f'Keep {field} inside the new revision directory')
            config = read(file(root,part['source']))
            require(config['manufacturing_revision']==part['manufacturing_revision'] and config['part_number']==part['part'], 'Source revision mismatch')
            verification = read(file(root, part['verification']))
            require(verification['checks']=='PASS' and verification['manufacturing_revision']==part['manufacturing_revision'], 'Geometry checks must pass for this revision')
            hashes = verification.get('source_sha256',{})
            require(part['source'] in hashes, 'Geometry verification must cover the source configuration')
            for path, expected_hash in hashes.items():
                require(sha(file(root,path))==expected_hash, f'Stale geometry verification: {path}')
                paths.add(path)
            require(part['review_images'], f"Add affected drawing previews/product renders for {part['part']}")
            for image in part['review_images']:
                require(Path(image).suffix.lower() in ('.png','.jpg','.jpeg'), 'Review images must be raster previews')
                paths.add(image)
            paths.add(part['verification'])
        for field in ('source','step','drawing','dxf'):
            if part[field]:paths.add(part[field])
        from pypdf import PdfReader
        pdf=PdfReader(file(root,part['drawing']))
        require(len(pdf.pages)==part['pdf_sheets'], f"PDF sheet count differs: {part['part']}")
        text='\n'.join(page.extract_text() or '' for page in pdf.pages)
        require(part['part'] in text, f"Drawing must identify {part['part']}")
        require(b'ISO-10303-21' in file(root,part['step']).read_bytes()[:256], 'Invalid STEP header')
    return data, {path:sha(file(root,path)) for path in sorted(paths)}


def snapshot(root, manifest):
    data, hashes=inputs(root,manifest)
    path=manifest.with_name(manifest.stem+'-review.json')
    write_new(path,dict(status='pending',reviewer='',reviewed_on='',source_sha256=hashes,
                        instructions='Inspect geometry checks, all changed PDF sheets and affected renders; then set status to reviewed and record reviewer/date. This snapshot is not approval.'))
    return path


def package(root, manifest):
    data, hashes=inputs(root,manifest)
    review_path=manifest.with_name(manifest.stem+'-review.json');review=read(review_path)
    require(review['status']=='reviewed' and review['reviewer'].strip(), 'Record the completed visual review first')
    date.fromisoformat(review['reviewed_on'])
    require(review['source_sha256']==hashes, 'Files changed since the review snapshot; inspect again and create a new snapshot')
    out=file(root,f"output/submission/releases/{data['name']}")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.mkdir()  # Never overwrite even an empty existing release.
    try:
        rows=[];base=canonical(root)
        for part in data['parts']:
            bundle=out/(part['part']+'.zip')
            if part['changed']:
                with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as archive:
                    for field in ('step','drawing','dxf'):
                        if part[field]:archive.write(file(root,part[field]),Path(part[field]).name)
            else:shutil.copyfile(file(root,base[part['role']]['manufacturing_revision_bundle']),bundle)
            with zipfile.ZipFile(bundle) as archive:
                expected={Path(part[k]).name:file(root,part[k]).read_bytes() for k in ('step','drawing','dxf') if part[k]}
                require(archive.testzip() is None and set(archive.namelist())==set(expected),'Invalid ZIP contents')
                for name,content in expected.items():require(archive.read(name)==content,'ZIP member mismatch')
            rows.append(dict(part=part['part'],quantity=part['quantity'],bundle=bundle.name,sha256=sha(bundle),jlc=part['jlc']))
        write_new(out/'release.json',dict(name=data['name'],status='reviewed quotation package',
                  supplier_submission_performed=False,parts=rows,source_sha256=hashes,
                  review_sha256=sha(review_path)))
        shutil.copyfile(review_path,out/'review.json')
        lines=['# '+data['name']+' quotation package','',
               'Reviewed files; no supplier submission or payment has been performed. This package does not replace the delivered canonical set.','',
               'Use the JLC workflow in docs/order-from-jlc.md with THESE ZIPs and the metadata below, not that guide’s original download links.','']
        for row in rows:
            j=row['jlc'];lines += [f"## {row['part']}",'',f"File: {row['bundle']}; quantity: {row['quantity']}",
                f"Category: {j['category']}; material: {j['material']}; finish: {j['finish']}; threads: {j['threads']}",'',j['remarks'],'']
        (out/'README.md').write_text('\n'.join(lines))
        (out/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in sorted(out.iterdir()) if p.is_file()))
    except Exception:
        shutil.rmtree(out)
        raise
    return out


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    init=sub.add_parser('init');init.add_argument('name');init.add_argument('--change',action='append',required=True,metavar='ROLE=REVISION')
    for name in ('check','snapshot','package'):
        sub.add_parser(name).add_argument('manifest',type=Path)
    args=parser.parse_args()
    try:
        if args.command=='init':
            pairs=[v.split('=',1) for v in args.change]
            require(all(len(p)==2 for p in pairs),'Use ROLE=REVISION')
            require(len({p[0] for p in pairs})==len(pairs),'Duplicate changed role')
            result=initialise(ROOT,args.name,dict(pairs))
        else:
            manifest=file(ROOT,str(args.manifest))
            result=inputs(ROOT,manifest)[0]['name']+' inputs PASS' if args.command=='check' else globals()[args.command](ROOT,manifest)
        print(result)
    except (ValueError,KeyError,FileNotFoundError,FileExistsError,zipfile.BadZipFile) as exc:
        parser.exit(1,f'{exc}\nSee docs/new-revision.md.\n')


if __name__=='__main__':main()
