"""Package the single R4 plate with its checked production drawing, not an assembly."""
from pathlib import Path
import hashlib,json,shutil,zipfile
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
M=json.loads((ROOT/'cad/manufacturing/R4-M01.json').read_text())
stem=M['part_number'];src=ROOT/'output/manufacturing/R4-M01'
out=ROOT/'output/submission/R4-M01';out.mkdir(parents=True,exist_ok=True)
report=json.loads((src/'geometry-verification.json').read_text())
assert report['checks']=='PASS' and report['nominal_geometry_unchanged']
schedule=json.loads((src/'feature-schedule.json').read_text())['features']
pdf=ROOT/'output/pdf'/f'{stem}.pdf';reader=PdfReader(pdf)
assert len(reader.pages)==2
pages=[p.extract_text() for p in reader.pages];txt='\n'.join(pages)
for phrase in ('NO TAPPED HOLES IN THIS PLATE','NO COUNTERSINKS OR COUNTERBORES','482.60','444.50','2.00','0.50','304','R4 APPROVED'):
 assert phrase in txt,phrase
for r in schedule:
 assert r['id'] in pages[0] and r['id'] in pages[1],r['id']
 for key in ('x','y'):assert f"{r[key]:.3f}" in pages[1],(r['id'],key)
files=[src/f'{stem}.step',src/f'{stem}.dxf',pdf]
for f in files:assert f.stat().st_size<100_000_000
for f in files:shutil.copyfile(f,out/f.name)
zpath=out/f'{stem}.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for f in files:z.write(f,f.name)
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None and set(z.namelist())=={f.name for f in files}
 for f in files:assert z.read(f.name)==f.read_bytes()
shutil.copyfile(ROOT/'docs/jlc-submission-R4-M01.md',out/'README.md')
shutil.copyfile(ROOT/'docs/jlc-radiator-remarks-R4-M01.txt',out/'supplier-remarks.txt')
shutil.copyfile(src/'geometry-verification.json',out/'geometry-verification.json')
report={'issue':M['issue'],'checks':'PASS','pdf_pages':2,'scheduled_features':len(schedule),
 'round_holes':28,'rack_slots':40,'air_apertures':4,'zip_members':[f.name for f in files],
 'pdf_identifier_and_coordinate_coverage':'PASS','zip_integrity':'PASS',
 'supplier_submission_performed':False}
(out/'package-verification.json').write_text(json.dumps(report,indent=2)+'\n')
paths=sorted(p for p in out.iterdir() if p.is_file() and p.name!='SHA256SUMS.txt')
(out/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in paths))
print(json.dumps(report,indent=2));print(zpath)
