"""Screen side elbows against the illustrative rack and optional cage-nut positions.
Unpopulated slots are not obstacles. This is not a specific rack qualification.
"""
import argparse,json
from pathlib import Path
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--iteration',default='N');args=parser.parse_args()
p=json.loads((ROOT/f'cad/iterations/{args.iteration}-long-bore.json').read_text())
out=ROOT/f'output/long-bore-{args.iteration}'
solids=cq.importers.importStep(str(out/'cad/elbow-envelope-assembly.step')).val().Solids()
half=p['body_width']/2
fittings=[s for s in solids if s.BoundingBox().xmin>half-.1 or s.BoundingBox().xmax<-half+.1]
assert len(fittings)==4

def box(w,d,h,x,y,z):return cq.Workplane('XY').box(w,d,h).translate((x,y,z)).val()
def assess(parts):
    return {'minimum_distance_mm':min(f.distance(s) for f in fittings for s in parts),
            'total_overlap_mm3':sum(f.intersect(s).Volume() for f in fittings for s in parts)}
rails=[box(35,3,87,s*242.5,1.5,43.5) for s in (-1,1)]
returns=[box(3,42,87,s*258.5,24,43.5) for s in (-1,1)]
rows=[]
for z in p['rack_slot_centres_z']:
    nuts=[box(10,6,10,x,6,z) for x in (-232.55,232.55)]
    rows.append(dict(slot_centre_z_mm=z,**assess(nuts)))
report={'revision':args.iteration,'gallery_axis_y_mm':p['gallery_axis_y'],
        'front_flange':assess(rails),'upright_return':assess(returns),
        'optional_nut_positions':rows,
        'basis':'Same illustrative rack as ten-pair feasibility: front flanges Y0..3, folded returns Y3..45, cage-nut boxes 10x6x10 centred at X±232.55/Y6. Conservative rectangular elbow heads.',
        'interpretation':'Each row tests nuts fitted at that pair of optional slots, not twelve installed nuts. A conservative envelope overlap requires exact hardware review; it is not proof of physical collision.',
        'limitations':['No actual cage clips or screw tails','No insertion or elbow-rotation sweep','No hose routing clearance','No load assessment']}
(out/'rack-clearance-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
