"""Prepare the Q-M02 specification-only faceplate issue from submitted Q-M01 geometry."""
from pathlib import Path
import hashlib
import json
import shutil
import math

R = Path(__file__).resolve().parents[1]
M = json.loads((R/'cad/manufacturing/Q-M02.json').read_text())
source = R/'output/manufacturing/Q-M01'
out = R/'output/manufacturing/Q-M02'
out.mkdir(parents=True, exist_ok=True)
prior = json.loads((source/'geometry-verification.json').read_text())
assert prior['checks'] == 'PASS' and prior['plate_solid_count'] == 1
submission = json.loads((R/'output/submission/jlc-quotation-2026-09-15.json').read_text())
sent = next(p for p in submission['parts'] if p['part'] == 'RM10-Q-M01-FACEPLATE')
assert hashlib.sha256((R/sent['archive']).read_bytes()).hexdigest() == sent['sha256']
import zipfile
with zipfile.ZipFile(R/sent['archive']) as archive:
    for ext in ['step', 'dxf']:
        old = source/f'RM10-Q-M01-FACEPLATE.{ext}'
        assert old.read_bytes() == archive.read(old.name)
        shutil.copyfile(old, out/f"{M['part_number']}.{ext}")
features = [f for f in json.loads((source/'feature-schedule.json').read_text())['features'] if f['group'] in 'WHR']
assert len(features) == 44
(out/'feature-schedule.json').write_text(json.dumps({'part_number':M['part_number'], 'features':features}, indent=2)+'\n')
inputs = [R/'cad/manufacturing/Q-M02.json', source/'geometry-verification.json', source/'feature-schedule.json']
inputs += [source/f'RM10-Q-M01-FACEPLATE.{ext}' for ext in ['step','dxf']]
report = {'issue':'Q-M02','checks':'PASS','nominal_geometry_unchanged':True,
          'plate_solid_count':1,'extent_mm':prior['plate_extent_mm'],
          'volume_mm3':prior['plate_volume_mm3'],'windows':20,'retention_holes':12,'rack_slots':12,
          'linear_and_coordinate_tolerance_mm':0.1,'POM_M4_coordinate_tolerance_mm':0.05,
          'worst_case_M4_radial_margin_mm':(4.4-4)/2-math.hypot(.15,.15),
          'fit_status':'Operator accepted JLC capability; worst-case interchangeability is not guaranteed',
          'source_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}}
(out/'geometry-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
