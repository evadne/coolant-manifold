"""Package the selected plate with its checked production drawing, not an assembly."""
from pathlib import Path
import hashlib,json,shutil,zipfile,argparse,re
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--issue',default='R6-M02',choices=['R4-M01','R5-M01','R6-M01','R6-M02'])
ISSUE=parser.parse_args().issue
M=json.loads((ROOT/f'cad/manufacturing/{ISSUE}.json').read_text());REV=M['geometry_revision']
stem=M['part_number'];src=ROOT/f'output/manufacturing/{ISSUE}'
out=ROOT/f'output/submission/{ISSUE}';out.mkdir(parents=True,exist_ok=True)
report=json.loads((src/'geometry-verification.json').read_text())
assert report['checks']=='PASS' and report['nominal_geometry_unchanged']
schedule=json.loads((src/'feature-schedule.json').read_text())['features']
pdf=ROOT/'output/pdf'/f'{stem}.pdf';reader=PdfReader(pdf)
assert len(reader.pages)==(3 if REV in ['R5','R6'] else 2)
pages=[p.extract_text() for p in reader.pages];txt='\n'.join(pages)
for phrase in ('NO TAPPED HOLES IN THIS PLATE','NO COUNTERSINKS OR COUNTERBORES','482.60','444.50','2.00','0.50','304',f'{REV} CABLE NOTCH' if REV in ['R5','R6'] else 'R4 APPROVED'):
 assert phrase in txt,phrase
for r in schedule:
 page=pages[2] if r['kind']=='edge_notch' else pages[1]
 assert r['id'] in pages[0] and r['id'] in page,r['id']
 for key in ('x','y'):assert f"{r[key]:.3f}" in page,(r['id'],key)
if REV in ['R5','R6']:
 n=next(r for r in schedule if r['kind']=='edge_notch')
 throat=n['mouth_width']-2*n['mouth_radius'];floor=throat-2*n['bottom_radius']
 for phrase in (f"{n['mouth_width']:.2f}",f"{n['depth']:.2f}",f"R{n['mouth_radius']:.2f}",f"R{n['bottom_radius']:.2f}",'R0.30-0.50',f'{throat:.2f} REF',f'{floor:.2f} REF'):
  assert phrase in pages[2],phrase
if ISSUE=='R6-M02':
 for phrase in ('RAW SHEET FINISH: BOTH FACES', 'M02'):assert phrase in txt,phrase
 for phrase in ('M4 ×40', 'screws + nuts', 'assembly order', 'loctite'):
  assert phrase.lower() not in txt.lower(),f'Assembly instruction in fabrication PDF: {phrase}'
files=[src/f'{stem}.step',src/f'{stem}.dxf',pdf]
for f in files:assert f.stat().st_size<100_000_000
for f in files:shutil.copyfile(f,out/f.name)
zpath=out/f'{stem}.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for f in files:z.write(f,f.name)
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None and set(z.namelist())=={f.name for f in files}
 for f in files:assert z.read(f.name)==f.read_bytes()
guide_dir=ROOT/('docs' if ISSUE == 'R6-M02' else 'docs/archive')
guide=(guide_dir/f'jlc-submission-{ISSUE}.md').read_text()
(out/'README.md').write_text(re.sub(r'\]\(([^:/)]+\.md)\)', r'](../../../docs/\1)', guide))
shutil.copyfile(guide_dir/f'jlc-radiator-remarks-{ISSUE}.txt',out/'supplier-remarks.txt')
shutil.copyfile(src/'geometry-verification.json',out/'geometry-verification.json')
report={'issue':M['issue'],'checks':'PASS','pdf_pages':len(pages),'scheduled_features':len(schedule),
 'round_holes':28,'rack_slots':40,'air_apertures':4,'edge_notches':int(REV in ['R5','R6']),'zip_members':[f.name for f in files],
 'pdf_identifier_and_coordinate_coverage':'PASS','zip_integrity':'PASS',
 'supplier_submission_performed':False}
(out/'package-verification.json').write_text(json.dumps(report,indent=2)+'\n')
paths=sorted(p for p in out.iterdir() if p.is_file() and p.name!='SHA256SUMS.txt')
(out/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in paths))
print(json.dumps(report,indent=2));print(zpath)
