"""Check PDF feature coverage and package each Q-M01 part separately; never upload."""
from pathlib import Path
import json,hashlib,zipfile,shutil,re
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];src=R/'output/manufacturing/Q-M01';out=R/'output/submission/Q-M01';out.mkdir(parents=True,exist_ok=True)
r=json.loads((src/'geometry-verification.json').read_text());assert r['checks']=='PASS'
for p,h in r['source_sha256'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
S=json.loads((src/'feature-schedule.json').read_text())['features'];results=[]
for part,n,groups in [('BODY',3,'PEBF'),('FACEPLATE',2,'WHR')]:
 stem='RM10-Q-M01-'+part;pdf=R/'output/pdf'/f'{stem}.pdf';pages=[p.extract_text() for p in PdfReader(pdf).pages];text='\n'.join(pages);assert len(pages)==n
 for f in [f for f in S if f['group'] in groups]:
  page=pages[1] if part=='FACEPLATE' or f['group'] in 'EB' else pages[0]
  assert f['id'] in page,f['id']
  for j in ([0,1,2] if f['group'] in 'EB' else [0,2]):assert f"{f['xyz_mm'][j]:.3f}" in page,(f['id'],j)
 required=['13.00','10 MIN','G 1/4','ISO 228-1','118°','90°','NO INTERNAL','0.05','28 G1/4'] if part=='BODY' else ['NO TAPPED','NO COUNTERSINKS','RAW STAINLESS SHEET FINISH','BOTH broad faces','482.60','2.00','0.30','±0.05']
 for s in required:assert s in text,s
 for s in ['unused ports', 'no rear cover', 'loctite', 'tighten', 'M4 ×10', 'installed rack screws']:
  assert s.lower() not in text.lower(),f'Assembly/design commentary in fabrication PDF: {s}'
 files=[src/f'{stem}.step',pdf]+([src/f'{stem}.dxf'] if part=='FACEPLATE' else [])
 for f in files:assert f.stat().st_size<100_000_000;shutil.copyfile(f,out/f.name)
 z=out/f'{stem}.zip'
 with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
  for f in files:a.write(f,f.name)
 with zipfile.ZipFile(z) as a:
  assert a.testzip() is None and set(a.namelist())=={f.name for f in files}
  for f in files:assert a.read(f.name)==f.read_bytes()
 results.append(dict(part=stem,pages=n,scheduled_features=sum(f['group'] in groups for f in S),zip_members=[f.name for f in files],checks='PASS'))
for name in ['geometry-verification.json','feature-schedule.json']:shutil.copyfile(src/name,out/name)
guide=(R/'docs/jlc-submission-Q-M01.md').read_text()
(out/'README.md').write_text(re.sub(r'\]\(([^:/)]+\.md)\)', r'](../../../docs/\1)', guide))
for name in ['body','faceplate']:shutil.copyfile(R/f'docs/jlc-Q-{name}-remarks.txt',out/f'{name}-supplier-remarks.txt')
(out/'package-verification.json').write_text(json.dumps(dict(issue='Q-M01',checks='PASS',parts=results,source_sha256={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'scripts/draw_Q_production.py',R/'scripts/package_Q_production.py']},supplier_submission_performed=False),indent=2)+'\n')
files=sorted(p for p in out.iterdir() if p.is_file() and p.name!='SHA256SUMS.txt');(out/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in files));print(json.dumps(results,indent=2))
