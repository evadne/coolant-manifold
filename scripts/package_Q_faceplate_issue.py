"""Verify and package Q-M02 faceplate only; preserve the submitted Q-M01 body/plate packs."""
from pathlib import Path
import json, hashlib, shutil, zipfile, re
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1]
src=R/'output/manufacturing/Q-M02';out=R/'output/submission/Q-M02';out.mkdir(parents=True,exist_ok=True)
stem='RM10-Q-M02-FACEPLATE'
report=json.loads((src/'geometry-verification.json').read_text())
assert report['checks']=='PASS' and report['nominal_geometry_unchanged']
for path,h in report['source_sha256'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==h,path
pdf=R/'output/pdf'/f'{stem}.pdf';pages=[p.extract_text() for p in PdfReader(pdf).pages]
assert len(pages)==2
text='\n'.join(pages)
features=json.loads((src/'feature-schedule.json').read_text())['features']
for f in features:
 assert f['id'] in pages[1]
 for i in [0,2]:assert f"{f['xyz_mm'][i]:.3f}" in pages[1],f['id']
for required in ['Ø32.00 ±0.10','Ø4.50 ±0.10','×7.00 ±0.10','coordinates ±0.10','Standard grinding and deburring','Complete burr removal is not guaranteed','NO COUNTERSINKS','NO TAPPED','0.30','2.00 ±0.10','Q-M02']:
 assert required in text,required
for obsolete in ['±0.05','+0.10/0','unilateral','0.10-0.20','ISO 2768','unused ports','loctite','tighten']:
 assert obsolete.lower() not in text.lower(),obsolete
files=[src/f'{stem}.step',src/f'{stem}.dxf',pdf]
for ext in ['step','dxf']:
 assert (src/f'{stem}.{ext}').read_bytes()==(R/f'output/manufacturing/Q-M01/RM10-Q-M01-FACEPLATE.{ext}').read_bytes()
for f in files:shutil.copyfile(f,out/f.name)
with zipfile.ZipFile(out/f'{stem}.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in files:z.write(f,f.name)
with zipfile.ZipFile(out/f'{stem}.zip') as z:
 assert z.testzip() is None and set(z.namelist())=={f.name for f in files}
 for f in files:assert z.read(f.name)==f.read_bytes()
for name in ['geometry-verification.json','feature-schedule.json']:shutil.copyfile(src/name,out/name)
guide=(R/'docs/jlc-submission-Q-M02.md').read_text()
(out/'README.md').write_text(re.sub(r'\]\(([^:/)]+\.md)\)',r'](../../../docs/\1)',guide))
shutil.copyfile(R/'docs/jlc-Q-faceplate-remarks-Q-M02.txt',out/'supplier-remarks.txt')
inputs=[R/'scripts/draw_Q_production.py',R/'scripts/package_Q_faceplate_issue.py',R/'scripts/prepare_Q_faceplate_issue.py',R/'cad/manufacturing/Q-M02.json']
verification={'issue':'Q-M02','checks':'PASS','pdf_pages':2,'scheduled_features':44,'zip_members':[f.name for f in files],'nominal_geometry_unchanged':True,'upload_performed_by_packaging_script':False,'source_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}}
(out/'package-verification.json').write_text(json.dumps(verification,indent=2)+'\n')
files=sorted(p for p in out.iterdir() if p.is_file() and p.name!='SHA256SUMS.txt')
(out/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in files))
print(json.dumps(verification,indent=2))
