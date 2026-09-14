"""Screen ten front pairs against the illustrative rack, without revising I.
This is an envelope study; it does not replace vendor drawings or a physical trial.
"""
import json,math
from pathlib import Path
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/ten-pair-feasibility';OUT.mkdir(parents=True,exist_ok=True)
assy=cq.importers.importStep(str(ROOT/'output/long-bore-I/cad/elbow-envelope-assembly.step'))
references=[s for s in assy.val().Solids() if s.BoundingBox().xmin>194 or s.BoundingBox().xmax<-194]
assert len(references)==4

def box(w,d,h,x,y,z):return cq.Workplane('XY').box(w,d,h).translate((x,y,z)).val()
rails=[box(35,3,87,s*242.5,1.5,43.5) for s in (-1,1)]
returns=[box(3,42,87,s*258.5,24,43.5) for s in (-1,1)]
nuts=[box(10,6,10,x,6,z) for x in (-232.55,232.55) for z in (5.4,81.6)]
results=[]
for width in (400,410,420):
    fits=[s.translate(((1 if s.Center().x>0 else -1)*(width-390)/2,0,0)) for s in references]
    distances={k:min(f.distance(p) for f in fits for p in parts) for k,parts in [('front_flange',rails),('upright_return',returns),('cage_nut',nuts)]}
    assert all(d>0 for d in distances.values())
    body=box(width,40,87,0,20,43.5)
    assert all(f.intersect(body).Volume()<1e-5 for f in fits)
    end_margin=width/2-180
    results.append({'body_width_mm':width,'front_pairs':10,'front_ports':20,'front_pitch_horizontal_vertical_mm':[40,40],'front_centres_x_mm':[-180+40*i for i in range(10)],'pull_ring_gap_nominal_mm':40-23.7,'end_port_centre_to_body_end_mm':end_margin,'boss_root_to_body_end_mm':end_margin-15,'end_full_thread_to_outer_front_drill_x_gap_mm':end_margin-8-5.9,'fitted_width_mm':width+57.6,'intrusion_beyond_assumed_opening_each_side_mm':(width+57.6-450)/2,'plugged_width_mm':width+8,'fitting_to_illustrative_rack_min_distances_mm':distances})
report={'status':'Geometric feasibility only; original I/J models unchanged','rack_basis':'The previously rendered illustrative rack: flange X225..260/Y0..3, return X257..260/Y3..45, cage nuts 10x6x10 at X±232.55/Y6/Z5.4,81.6','candidate':'410 mm body, ten pairs at 40 x 40 pitch; proposed six M4 mounts X-160/0/160, Z7/80','countersink_edge_to_port_window_mm':math.hypot(20,16.5)-4-16,'head_edge_to_36mm_keepout_mm':math.hypot(20,16.5)-7.96/2-18,'limitations':['Actual rail folds, cage clips, screw protrusion and other hardware are not represented fully','No fitted insertion sweep, installation-tool access or hose rotation sweep validated','Existing QD pull-ring reference dimensions; hand access requires physical check','No new machined-body CAD or pressure/structural qualification'], 'variants':results}
(OUT/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
