"""Assess O-M02 faceplate mass and countersink geometry; not structural FEA."""
from pathlib import Path
import json,math
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'cad/iterations/O-long-bore.json').read_text())
f=json.loads((ROOT/'cad/manufacturing/O-M02.json').read_text())
fast=p['faceplate_fastener']
plate=cq.importers.importStep(str(ROOT/'output/manufacturing/O-M02/RM10-O-M02-FACEPLATE.step')).val()
area=p['rack_width']*p['body_height']-20*math.pi*(p['faceplate_port_clearance']/2)**2
area-=6*math.pi*(fast['clearance_diameter']/2)**2
area-=12*((p['rack_slot_length']-p['rack_slot_width'])*p['rack_slot_width']+math.pi*(p['rack_slot_width']/2)**2)
depth=(fast['countersink_diameter']-fast['clearance_diameter'])/(2*math.tan(math.radians(fast['countersink_angle']/2)))
max_depth=(fast['countersink_diameter']+f['countersink_diameter_upper_deviation']-fast['clearance_diameter'])/(2*math.tan(math.radians((fast['countersink_angle']-f['countersink_angle_tolerance_degrees'])/2)))
rows=[]
for t in (3.,2.5,2.):
    volume=plate.Volume()-(p['faceplate_thickness']-t)*area
    rows.append({'thickness_mm':t,'mass_kg':volume*7.9e-6,
      'saving_kg':(p['faceplate_thickness']-t)*area*7.9e-6,
      'nominal_countersink_depth_mm':depth,'nominal_cylindrical_land_mm':t-depth,
      'minimum_land_before_edge_break_mm':t-.1-max_depth,
      'existing_boss_projection_mm':f['boss_height']-t,
      'boss_height_for_1mm_projection_mm':t+1,
      'nominal_M4x12_reach_from_POM_face_mm':12-t})
assert abs(depth-1.75)<1e-10
assert abs(rows[-1]['mass_kg']-.3951615713202164)<1e-9
report={'scope':'Dimensional and mass assessment only; no separate manifold structural simulation.',
 'reference':'released O-M02 geometry unchanged; 7900 kg/m3 stainless density.',
 'worst_case_stack':'Thickness -0.10; countersink diameter +0.10; included angle -1 degree; through-hole at minimum 4.50.',
 'important':'A thin cylindrical land is not itself proof of inadequate strength. Nominal conical seating geometry remains present.',
 'comparison':rows}
out=ROOT/'output/manifold-plate-thickness';out.mkdir(exist_ok=True)
(out/'assessment.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
