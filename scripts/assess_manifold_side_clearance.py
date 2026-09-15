"""Compare centred-gallery slab depths against illustrative cage-nut envelopes.
Only a geometric sensitivity study; does not regenerate or modify approved P CAD.
"""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
SLOTS=[5.4,21.275,37.15,49.85,65.725,81.6]
PORTS=[23.5,63.5]

def box_gap(a,b):
    separation=[max(a[0][i]-b[1][i],b[0][i]-a[1][i]) for i in range(3)]
    return math.sqrt(sum(max(x,0)**2 for x in separation)) if max(separation)>0 else max(separation)

def nut(x,y,z,w,d,h):return ((x-w/2,y-d/2,z-h/2),(x+w/2,y+d/2,z+h/2))

cases=[]
for slab in (40,45,50):
    axis=slab/2;elbows=[((-231.8,axis-9,z-9),(-213.8,axis+9,z+9)) for z in PORTS]
    row=[]
    for z in SLOTS:
        box=nut(-232.5,8.5,z,13,12,13)
        gap=min(box_gap(e,box) for e in elbows)
        row.append(dict(slot_z_mm=z,signed_envelope_gap_mm=round(gap,4),overlap=gap<0))
    cases.append(dict(slab_mm=slab,boss_mm=3,overall_POM_mm=slab+3,gallery_axis_Y_mm=axis,
        side_port_rear_shift_from_P_mm=axis-20,front_rear_gallery_ligament_mm=axis-5.9,
        elbow_to_nut_depth_gap_mm=axis-9-14.5,optional_slots=row))
assert cases[0]['optional_slots'][0]['signed_envelope_gap_mm']==2.6
assert cases[0]['optional_slots'][1]['signed_envelope_gap_mm']==-3.5
assert cases[1]['optional_slots'][1]['signed_envelope_gap_mm']==-1.0
assert cases[2]['optional_slots'][1]['signed_envelope_gap_mm']==1.5
old=nut(-232.55,6,21.275,10,6,10)
elbow=((-231.8,11,14.5),(-213.8,29,32.5))
assert abs(box_gap(elbow,old)-2)<1e-6
report=dict(status='OPEN: actual rack cage clips, screw tails and selected90-degree rotary fitting need measured/CAD fit confirmation',
    approved_design='P:40mm slab plus3mm bosses.35mm N was superseded. All manufactured P CAD remains unchanged.',
    basis='Same conservative18mm elbow-head boxes as the composite, two port rows,13x12x13 cage-nut envelopes centred atX+/-232.5,Y8.5. Negative gap is AABB minimum translation overlap, not proven physical contact.',
    previous_O_basis='10x6x10 nut boxes centred atY6 extended toY9, yielding2mm depth clearance atY20. Current larger illustrative hardware extends toY14.5, consuming5.5mm more space. The earlier conclusion was conditional on those generic envelopes.',
    cases=cases,installed_width_mm=467.6,opening_mm=450,
    depth_changes_do_not_fix_width='Slab depth affectsY placement only.410mm body plus2x28.8mm nominal side fitting projection still exceeds450mm opening.',
    recommendation='Keep approved40mm P and lodge the concern.45mm still overlaps these envelopes at inner slots;50mm gives only1.5mm nominal depth gap, not a tolerance-qualified solution. Outer-slot rendering is one provisional arrangement, not universal90-degree fitting feasibility.',
    unresolved=['Actual cage-clip geometry and projection from rail back','Actual bolt length and screw tails','Selected rotary elbow and compression dimensions/rotation sweep','Rack datum/tolerances and flange section','Insertion sequence and assembly/service access'])
out=ROOT/'output/context-25U/manifold-side-clearance.json';out.write_text(json.dumps(report,indent=2)+'\n')
print('PASS:40/45/50mm sensitivity comparison; inner-slot depth gaps -3.5/-1.0/+1.5mm; approved P unchanged.')
