"""Package the checked Q-M04 POM body only; never submit or replace original Q-M01."""
from pathlib import Path
import json,hashlib,zipfile,shutil
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];issue='Q-M04';stem=f'RM10-{issue}-BODY';src=R/f'output/manufacturing/{issue}';out=R/f'output/submission/{issue}';out.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((src/'geometry-verification.json').read_text());assert r['checks']=='PASS' and r['perimeter_edges']==12
for p,h in r['source_sha256'].items():assert sha(R/p)==h,p
pdf=R/f'output/pdf/{stem}.pdf';pages=[p.extract_text() for p in PdfReader(pdf).pages];assert len(pages)==3;text='\n'.join(pages)
S=json.loads((src/'feature-schedule.json').read_text())['features']
for f in [f for f in S if f['group'] in 'PEBF']:
 page=pages[1] if f['group'] in 'EB' else pages[0]
 assert f['id'] in page
 for j in ([0,1,2] if f['group'] in 'EB' else [0,2]):assert f"{f['xyz_mm'][j]:.3f}" in page
for phrase in ['Q-M04','C0.50 ±0.10 ×45° ±1°','All 12 slab perimeter edges','13.00','10 MIN','G 1/4','ISO 228-1','NO INTERNAL','Root R1.00','outer boss lip C0.50','Ø4.40']:
 assert phrase in text,phrase
for phrase in ['unused ports','loctite','tighten','M4 ×10','no rear cover']:
 assert phrase.lower() not in text.lower(),phrase
files=[src/f'{stem}.step',pdf]
for p in files:shutil.copyfile(p,out/p.name)
with zipfile.ZipFile(out/f'{stem}.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,p.name)
with zipfile.ZipFile(out/f'{stem}.zip') as z:
 assert z.testzip() is None and set(z.namelist())=={p.name for p in files}
 for p in files:assert z.read(p.name)==p.read_bytes()
for name in ['geometry-verification.json','feature-schedule.json']:shutil.copyfile(src/name,out/name)
shutil.copyfile(R/'docs/jlc-submission-Q-M04.md',out/'README.md');shutil.copyfile(R/'docs/jlc-Q-body-remarks-Q-M04.txt',out/'supplier-remarks.txt')
inputs=[R/'scripts/draw_Q_production.py',R/'scripts/prepare_Q_body_issue.py',R/'scripts/package_Q_body_issue.py',R/'cad/manufacturing/Q-M04.json']
r=dict(issue=issue,checks='PASS',pdf_pages=3,scheduled_features=40,zip_members=[p.name for p in files],supplier_submission_performed=False,source_sha256={str(p.relative_to(R)):sha(p) for p in inputs})
(out/'package-verification.json').write_text(json.dumps(r,indent=2)+'\n')
(out/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in sorted(out.iterdir()) if p.is_file() and p.name!='SHA256SUMS.txt'))
print(json.dumps(r,indent=2))
