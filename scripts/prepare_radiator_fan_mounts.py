"""Check reference fan integration and nut cavity; prepare review meshes.
Noctua reference CAD is for integration/rendering only, not fan manufacture.
"""
from pathlib import Path
import json, math, hashlib
import cadquery as cq
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'cad/radiator/R4.json').read_text())
source=ROOT/'docs/references/noctua-nf-a20/NF-A20_Public-CAD.stp'
fan=cq.importers.importStep(str(source)).val().translate((0,-8.47,0)).rotate((0,0,0),(0,0,1),180)
solids=fan.Solids()
OUT=ROOT/'output/radiator-fan-integration';OUT.mkdir(exist_ok=True)
meshdir=OUT/'reference-meshes';meshdir.mkdir(exist_ok=True)
for i,s in enumerate(solids):
 if i!=9:cq.exporters.export(s,str(meshdir/f'fan-{i:02}.stl'),tolerance=.12,angularTolerance=.15)
print('Reference meshes exported',flush=True)
# Check relevant fan/frame hardware only. A bounding box removes distant pairs.
min_gap=1e6; tested=[]
for x in P['aperture_centres_x']:
 for dy in P['aperture_centres_y_from_centre']:
  for mx in P['radiator_mount_x']:
   for my in P['radiator_mount_y_from_centre']:
    if abs(mx-x)>104 or abs(my-dy)>104:continue
    head=cq.Solid.makeCylinder(2.8,2.4,cq.Vector(mx-x,13.6,my-dy),cq.Vector(0,1,0))
    oriented=[s.rotate((0,0,0),(0,1,0),180) for s in solids] if x>0 else solids
    # Source frame placed at Y=-18. M3 head at Y=-4.4..-2, with no washer.
    # Compare frame plus nearby pads; impeller envelope is too far inward.
    d=min(s.distance(head) for i,s in enumerate(oriented) if i!=1)
    tested.append({'fan_centre':[x,dy],'M3_centre':[mx,my],'gap_mm':d});min_gap=min(min_gap,d)
    print('M3 clearance',tested[-1],flush=True)
assert min_gap>0.05,min_gap
# Ray-cast catalogue radiator mesh at centre and around the nut/washer envelope.
raw=(ROOT/'docs/references/alphacool-14351-manufacturer.stl').read_bytes()
t=np.frombuffer(raw,dtype=np.dtype([('n','<f4',3),('v','<f4',(3,3)),('a','<u2')]),offset=84)['v'].astype(float)
a=t[:,0][:,[0,2]];u=t[:,1][:,[0,2]]-a;v=t[:,2][:,[0,2]]-a
den=u[:,0]*v[:,1]-u[:,1]*v[:,0]
gaps=[]
for x in (-185,-15,15,185):
 for dz in (-185,-15,15,185):
  for radius,angle in [(0,0)]+[(4.5,k*math.pi/8) for k in range(16)]:
   q=np.array([x+radius*math.cos(angle),212+dz+radius*math.sin(angle)])-a
   with np.errstate(divide='ignore',invalid='ignore'):
    s=(q[:,0]*v[:,1]-q[:,1]*v[:,0])/den;r=(u[:,0]*q[:,1]-u[:,1]*q[:,0])/den
   hit=(abs(den)>1e-10)&(s>=-1e-7)&(r>=-1e-7)&(s+r<=1+1e-7)
   yy=t[hit,0,1]+s[hit]*(t[hit,1,1]-t[hit,0,1])+r[hit]*(t[hit,2,1]-t[hit,0,1])
   beyond=yy[yy>-22.5+1e-5];assert len(beyond)
   gaps.append(float(min(beyond)+22.5))
assert min(gaps)>=6.49,min(gaps)
# Stack from the outside fan pad, using 32 mm nominal fan thickness.
bearing=-P['thickness']-32-.8
r={'reference_fan_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'fan_centre_pitch_mm':200,'nominal_adjacent_fan_gap_mm':0,
 'M3_hardware':'Pan head OD5.6, height2.4, no washer; reverse right-hand fans 180 degrees about airflow axis',
 'reference_M3_hardware_minimum_gap_mm':min_gap,'M3_hardware_checks':tested,
 'sampled_core_setback_mm':min(gaps),'core_samples':len(gaps),
 'rear_nut_and_washer_height_mm':4.0,'nut_to_core_nominal_gap_mm':min(gaps)-4,
 'rear_nut_alternative_M4x40_tip_behind_plate_mm':bearing+40,
 'rear_nut_alternative_tip_to_core_nominal_gap_mm':min(gaps)-bearing-40,
 'R4_selected_screw_orientation':'Button heads behind plate; nuts on outside of fans',
 'R4_head_and_washer_behind_plate_mm':3.0,'R4_head_to_core_nominal_gap_mm':min(gaps)-3.0,
 'R4_M4x40_tip_ahead_of_front_nut_mm':1.2,
 'R3_M4x35_tip_behind_plate_mm':bearing+35,
 'R3_nominal_effective_thread_mm':1.8,'R3_minimum_effective_thread_mm':1.7,
 'R3_minimum_full_pitch_count':1.7/.7,
 'limits':'Nominal integration only. Fan/pad compression, part tolerances, fastener length tolerances and actual core position require first-article check. No tightening torque or vibration qualification. Public Noctua CAD must not be used for fan performance simulation or manufacture.'}
(OUT/'verification.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
