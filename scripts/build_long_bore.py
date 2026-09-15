"""Separate revision H: two through-drilled galleries, four G1/4 end plugs.

Preserves revision G files. Threads are pilot/envelope call-outs, not helices.
"""
from pathlib import Path
import json
import argparse
import ezdxf
import math
import shutil
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--iteration',choices=('H','I','J','K','L','M','N','O','P'),default='H')
args=parser.parse_args();REV=args.iteration
P=json.loads((ROOT/f'cad/iterations/{REV}-long-bore.json').read_text())
OUT=ROOT/f'output/long-bore-{REV}/cad';OUT.mkdir(parents=True,exist_ok=True)
MESH=ROOT/f'tmp/mesh-long-bore-{REV}';MESH.mkdir(parents=True,exist_ok=True)
W,D,H=P['body_width'],P['body_depth'],P['body_height']
T=P['faceplate_thickness'];BH=P['port_boss_height'];F=P['faceplate_fastener']
R=P['gallery_diameter']/2;Y=P['gallery_axis_y'];rows=P['port_rows_z']
pair_count=P.get('front_pair_count',P.get('branch_count',0)+1)
xs=[(i-(pair_count-1)/2)*P['port_pitch'] for i in range(pair_count)]

def box(w,d,h,x=0,y=0,z=0):
 return cq.Workplane('XY').box(w,d,h,centered=(True,False,False)).translate((x,y,z))
def cyl(r,l,pos,axis):
 return cq.Workplane(obj=cq.Solid.makeCylinder(r,l,cq.Vector(*pos),cq.Vector(*axis)))
def vol(s):return sum(v.Volume() for v in s.solids().vals())

body=box(W,D,H)
for z in rows:
 for x in xs:body=body.union(cyl(P['port_boss_diameter']/2,BH,(x,-BH,z),(0,1,0)))
roots=[e for e in body.val().Edges() if e.geomType()=='CIRCLE' and abs(e.Center().y)<1e-6]
assert len(roots)==2*len(xs)
body=body.newObject(roots).fillet(P['port_boss_root_radius'])
fluids=[];channels=[];side_ports=[]
point_length=P['tap_drill_diameter']/2/math.tan(math.radians(P['front_drill_point_angle']/2))
for z in rows:
 gallery=cyl(R,W,(-W/2,Y,z),(1,0,0));channels.append(gallery)
 fluid=gallery
 for x in xs:
  length=P['front_drill_cylinder_end_y']+BH
  bore=cyl(P['tap_drill_diameter']/2,length,(x,-BH,z),(0,1,0))
  tip=cq.Workplane(obj=cq.Solid.makeCone(P['tap_drill_diameter']/2,0,point_length,cq.Vector(x,P['front_drill_cylinder_end_y'],z),cq.Vector(0,1,0)))
  mouth=cq.Workplane(obj=cq.Solid.makeCone(6.9,P['tap_drill_diameter']/2,1,cq.Vector(x,-BH,z),cq.Vector(0,1,0)))
  fluid=fluid.union(bore).union(tip).union(mouth)
 for sign in (-1,1):
  start=(sign*W/2,Y,z);axis=(-sign,0,0)
  entry=cq.Workplane(obj=cq.Solid.makeCone(P['side_entry_mouth_diameter']/2,R,P['side_entry_chamfer_depth'],cq.Vector(*start),cq.Vector(*axis)))
  fluid=fluid.union(entry);side_ports.append((sign*W/2,Y,z))
 body=body.cut(fluid);fluids.append(fluid)

face=box(P['rack_width'],T,H,y=-T)
for z in rows:
 for x in xs:face=face.cut(cyl(P['faceplate_port_clearance']/2,T+.2,(x,-T-.1,z),(0,1,0)))
rack_z=P.get('rack_slot_centres_z',[6.35-(88.9-H)/2,82.55-(88.9-H)/2])
assert all(any(abs(((z+(88.9-H)/2)%44.45)-offset)<1e-6 for offset in (6.35,22.225,38.1)) for z in rack_z)
for sign in (-1,1):
 for z in rack_z:
  face=face.cut(cq.Workplane('XZ',origin=(sign*P['rack_hole_pitch']/2,.1,z)).slot2D(P['rack_slot_length'],P['rack_slot_width']).extrude(T+.2))
for x,z in P['faceplate_mounts_xz']:
 face=face.cut(cyl(F['clearance_diameter']/2,T+.1,(x,-T,z),(0,1,0)))
 if F.get('style')!='button':face=face.cut(cq.Solid.makeCone(F['countersink_diameter']/2,F['clearance_diameter']/2,(F['countersink_diameter']-F['clearance_diameter'])/2,cq.Vector(x,-T,z),cq.Vector(0,1,0)))
 body=body.cut(cyl(F['tap_drill_diameter']/2,F['pilot_depth'],(x,0,z),(0,1,0)))

if P.get('boss_outer_chamfer'):
 edges=[e for e in body.val().Edges() if e.geomType()=='CIRCLE' and abs(e.Center().y+BH)<1e-6 and abs(e.radius()-P['port_boss_diameter']/2)<1e-6]
 assert len(edges)==20
 body=body.newObject(edges).chamfer(P['boss_outer_chamfer'])
for x,z in P['faceplate_mounts_xz']:
 if F.get('entry_diameter'):
  pr=F['tap_drill_diameter']/2;er=F['entry_diameter']/2
  body=body.cut(cq.Solid.makeCone(er,pr,er-pr,cq.Vector(x,0,z),cq.Vector(0,1,0)))
  body=body.cut(cq.Solid.makeCone(pr,0,pr/math.tan(math.radians(F['drill_point_angle']/2)),cq.Vector(x,F['pilot_depth'],z),cq.Vector(0,1,0)))

plug_spec=P['side_plug_reference'];plugs=[]
for x,y,z in side_ports:
 sign=1 if x>0 else -1
 head=cyl(plug_spec['head_diameter']/2,plug_spec['head_projection'],(x,y,z),(sign,0,0))
 # Clearance-sized shank only: avoids false interference with pilot-model female threads.
 shank=cyl(R,plug_spec['thread_length'],(x,y,z),(-sign,0,0))
 plug=head.union(shank)
 socket=(cq.Workplane('YZ',origin=(x+sign*(plug_spec['head_projection']+.1),y,z))
         .polygon(6,2*plug_spec['socket_across_flats']/math.sqrt(3)).extrude(-sign*2.1))
 plug=plug.cut(socket)
 assert plug.val().isValid()
 plugs.append(plug)

# Manufacturing solids and connected fluid topology.
assert all(s.val().isValid() and len(s.solids().vals())==1 for s in [body,face]+fluids)
assert vol(fluids[0].intersect(fluids[1]))<1e-6
assert vol(body.intersect(face))<1e-6
assert P['gallery_diameter']<=P['tap_drill_diameter']
assert P['side_thread_full_depth']>plug_spec['thread_length']
assert Y+R<D and Y-R>0
# M4 holes may overlap the gallery's Y range while remaining well separated in Z.
# The complete 3D thread-envelope-to-wet-network distance is checked below.
if P.get('galleries_centred_in_depth'):assert abs(Y-D/2)<1e-6
assert min(rows[0]-R,H-rows[1]-R)>0
assert rows[1]-rows[0]>2*R
assert BH-T==P.get('boss_projection_above_plate',3) and len(side_ports)==4
# Every branch opens to its intended continuous gallery, without requiring a group jumper.
for z,gallery,fluid in zip(rows,channels,fluids):
 for x in xs:
  bore=cyl(P['tap_drill_diameter']/2,P['front_drill_cylinder_end_y']+BH,(x,-BH,z),(0,1,0))
  assert vol(bore.intersect(gallery))>1
  usable=cyl(P['thread_major_diameter']/2,P['thread_full_depth'],(x,-BH,z),(0,1,0))
  assert vol(usable.intersect(gallery))<1e-6
  keepout=cyl(P['port_hardware_keepout_diameter']/2,12,(x,-BH,z),(0,-1,0))
  assert vol(keepout.intersect(face))<1e-6
mount_clearance=min(cyl(F['nominal_diameter']/2,F['pilot_depth']+(1 if F.get('entry_diameter') else 0),(x,0,z),(0,1,0)).val().distance(fluid.val()) for x,z in P['faceplate_mounts_xz'] for fluid in fluids)
assert mount_clearance>2
for i,plug in enumerate(plugs):
 assert vol(plug.intersect(body))<1e-5
 assert vol(plug.intersect(face))<1e-5
 for other in plugs[i+1:]:assert vol(plug.intersect(other))<1e-6
# Entire flat side seal land fits the POM side, clear of front/rear edges.
assert P['side_seal_land_diameter']/2<min(Y,D-Y,rows[0],H-rows[-1])
# Conservative plug-thread envelope stays clear of the first front branch on each end.
plug_to_branch=(W/2-max(abs(x) for x in xs))-plug_spec['thread_length']-P['thread_major_diameter']/2
assert plug_to_branch>P.get('minimum_side_plug_branch_clearance',20)
# This clearance threshold is a layout constraint, not a strength qualification.
assert W/2-max(abs(x) for x in xs)-P['side_entry_chamfer_depth']-P['side_thread_full_depth']-P['tap_drill_diameter']/2>2

assy=cq.Assembly(name=P['name'].replace('-','_')+f'_revision_{REV}_long_bore')
for name,part,col in [('body',body,(.025,.03,.035)),('faceplate',face,(.5,.53,.56))]:
 cq.exporters.export(part,str(OUT/f'{name}.step'))
 cq.exporters.export(part,str(MESH/f'{name}.stl'),tolerance=.06,angularTolerance=.12)
 assy.add(part,name=name,color=cq.Color(*col))
for i,plug in enumerate(plugs):
 cq.exporters.export(plug,str(MESH/f'side_plug_{i}.stl'),tolerance=.04,angularTolerance=.12)
 assy.add(plug,name=f'REFERENCE_side_plug_{i+1}',color=cq.Color(.6,.62,.64))
assy.export(str(OUT/'manifold-assembly.step'))
# Separate technical cutaway, explicitly a section rather than a milled pocket design.
cutaway=body.cut(box(W+2,D-Y+1,H+2,y=Y,z=-1))
assert cutaway.val().isValid()
cq.exporters.export(cutaway,str(MESH/'body-section.stl'),tolerance=.06,angularTolerance=.12)
for i,v in enumerate(fluids):
 cq.exporters.export(v,str(OUT/f'fluid-network-{i+1}.step'))
 cq.exporters.export(v,str(MESH/f'fluid-network-{i+1}.stl'),tolerance=.04,angularTolerance=.12)
# Each iteration has its own cut profile. H also checks equivalence to frozen G.
if REV=='H':
 gface=cq.importers.importStep(str(ROOT/'output/cad/faceplate.step'))
 assert vol(face.cut(gface))+vol(gface.cut(face))<1e-5
 shutil.copyfile(ROOT/'output/cad/faceplate-flat.dxf',OUT/'faceplate-flat.dxf')
else:
 dxf=ezdxf.new('R2010');dxf.units=4;dxf.layers.new('CUT');m=dxf.modelspace();attr={'layer':'CUT'}
 fw=P['rack_width']/2
 m.add_lwpolyline([(-fw,0),(fw,0),(fw,H),(-fw,H)],close=True,dxfattribs=attr)
 for z in rows:
  for x in xs:m.add_circle((x,z),P['faceplate_port_clearance']/2,dxfattribs=attr)
 for x,z in P['faceplate_mounts_xz']:m.add_circle((x,z),F['clearance_diameter']/2,dxfattribs=attr)
 for x in [-P['rack_hole_pitch']/2,P['rack_hole_pitch']/2]:
  for z in rack_z:
   r=P['rack_slot_width']/2;a=(P['rack_slot_length']-P['rack_slot_width'])/2
   m.add_lwpolyline([(x-a,z-r,0),(x+a,z-r,1),(x+a,z+r,0),(x-a,z+r,1)],format='xyb',close=True,dxfattribs=attr)
 dxf.saveas(OUT/'faceplate-flat.dxf')
 check=ezdxf.readfile(OUT/'faceplate-flat.dxf')
 assert not check.audit().has_errors and len(check.modelspace().query('CIRCLE'))==2*len(xs)+len(P['faceplate_mounts_xz'])
 assert len(check.modelspace().query('LWPOLYLINE'))==1+2*len(rack_z)
 # Check every screw keeps a dry, continuous head-bearing land outside port windows.
 assert min(math.hypot(mx-x,mz-z)-F.get('countersink_diameter',F['clearance_diameter'])/2-P['faceplate_port_clearance']/2 for mx,mz in P['faceplate_mounts_xz'] for x in xs for z in rows)>2
 assert min(math.hypot(mx-x,mz-z)-F['head_diameter']/2-P['port_hardware_keepout_diameter']/2 for mx,mz in P['faceplate_mounts_xz'] for x in xs for z in rows)>2
 assert min(P['port_pitch'],rows[1]-rows[0])-P['qd_female_diameter_reference']>=16
 assert W/2-max(abs(x) for x in xs)-P['port_boss_diameter']/2-P['port_boss_root_radius']>=P.get('minimum_end_boss_root_margin',20)
 # Reference elbow+compression envelopes from supplied dimensions; no branding or knurling.
 E=P['side_fitting_clearance'];elbows=[]
 for i,(x,y,z) in enumerate(side_ports):
  sign=1 if x>0 else -1
  base=cyl(E['elbow_diameter']/2,E['elbow_base_height'],(x,y,z),(sign,0,0))
  # Conservative rectangular head envelope; physical elbow's rounded corner is inside it.
  head=box(E['elbow_head_height'],E['elbow_diameter'],E['elbow_diameter'],x=x+sign*(E['elbow_base_height']+E['elbow_head_height']/2),y=y-E['elbow_diameter']/2,z=z-E['elbow_diameter']/2)
  compression=cyl(E['compression_diameter']/2,E['compression_projection'],(x+sign*E['elbow_outlet_axis_from_seat_inferred'],y+E['elbow_diameter']/2,z),(0,1,0))
  fitting=base.union(head).union(compression)
  # Visible tube entrance only; internal fitting geometry is not supplied.
  fitting=fitting.cut(cyl(8,5,(x+sign*E['elbow_outlet_axis_from_seat_inferred'],y+E['elbow_diameter']/2+E['compression_projection']+.1,z),(0,-1,0)))
  assert fitting.val().isValid() and vol(fitting.intersect(body))<1e-5 and vol(fitting.intersect(face))<1e-5
  if REV=='I':assert max(abs(fitting.val().BoundingBox().xmin),abs(fitting.val().BoundingBox().xmax))<E['equipment_width_assumption']/2
  cq.exporters.export(fitting,str(MESH/f'elbow-reference-{i}.stl'),tolerance=.04,angularTolerance=.12)
  elbows.append(fitting)
 for i,a in enumerate(elbows):
  for b in elbows[i+1:]:assert vol(a.intersect(b))<1e-5
 alternative=cq.Assembly(name=f'REFERENCE_{REV}_rearward_elbows_and_compression_fittings')
 alternative.add(body,name='body');alternative.add(face,name='faceplate')
 for i,e in enumerate(elbows):alternative.add(e,name=f'REFERENCE_fitting_{i+1}')
 alternative.export(str(OUT/'elbow-envelope-assembly.step'))
area=math.pi*R*R;old_area=16*24
report={'revision':REV,'system_pairs_with_side_feed':len(xs),'system_pairs_with_front_feed':len(xs)-1,'parent_tag':P['parent_tag'],'wet_networks':2,'front_G1_4_ports':2*len(xs),'front_pairs':len(xs),'side_G1_4_ports':4,'initial_side_plugs':4,
 'rack_mounting_slots':2*len(rack_z),'rack_slot_centres_z_mm':rack_z,
 'manufactured_parts':2,'rear_plate':False,'large_gallery_O_rings':0,'plug_face_seals_required':4,'front_mount_screws_M4':len(P['faceplate_mounts_xz']),'rear_screws':0,
 'body_envelope_mm':[W,D,H],'rack_assembly_envelope_without_front_QDs_mm':[P['rack_width'],D+BH,H],
 'gallery_diameter_mm':2*R,'gallery_axis_y_mm':Y,'gallery_length_mm':W,'gallery_area_mm2':area,'previous_gallery_area_mm2':old_area,
 'same_local_flow_velocity_ratio_H_to_G':old_area/area,'nominal_full_bore_L_over_D':W/(2*R),
 'opposed_drill_nominal_reach_with_overlap_mm':(W+P['opposed_drill_overlap'])/2,
 'opposed_drill_L_over_D':(W+P['opposed_drill_overlap'])/(4*R),
 'front_wall_to_gallery_mm':Y-R,'rear_wall_mm':D-Y-R,'inter_gallery_web_mm':rows[1]-rows[0]-2*R,
 'front_drill_tip_y_mm':P['front_drill_cylinder_end_y']+point_length,'M4_thread_envelope_to_wet_network_min_mm':mount_clearance,
 'side_plug_to_nearest_front_thread_envelope_mm':plug_to_branch,'body_volume_mm3':vol(body),
 'checks':['valid connected solids','two separated uninterrupted fluid networks','all front ports intersect intended gallery','four side mouths and plug positions','front usable threads precede gallery breakthrough','M4 mounts clear wet networks','no overlap of plugs with pilot-represented body or faceplate','side seal lands within POM face','front plate geometrically identical to G' if REV=='H' else 'M4 clearance holes and heads clear port windows and hardware','raised port fitting keep-outs clear steel'],
 'limitations':['Deep drilling exceeds ordinary 10D guidance even from both ends; manual vendor DFM required','Nominal straight cylinder does not simulate drill wander or opposed-bore mismatch','Plugs are provisional envelopes; seal footprint and thread length need confirmation','No pressure, thermal, creep or hydraulic qualification','BSPP thread helices and plug face seals not modelled']}
if REV in ('I','J','K','L','M','N','O','P'):
 E=P['side_fitting_clearance'];projection=max(E['elbow_base_height']+E['elbow_head_height'],E['elbow_outlet_axis_from_seat_inferred']+E['compression_diameter']/2)
 report['side_fitting_review']={'equipment_width_assumption_mm':E['equipment_width_assumption'],'body_width_mm':W,'reserved_per_side_mm':(E['equipment_width_assumption']-W)/2,'drawing_inferred_projection_mm':projection,'fitted_body_width_nominal_mm':W+2*projection,'nominal_margin_each_side_mm':(E['equipment_width_assumption']-W)/2-projection,'plugged_body_width_mm':W+2*plug_spec['head_projection'],'rearward_fitting_extent_y_mm':Y+E['elbow_diameter']/2+E['compression_projection'],'front_pull_ring_gap_mm':P['port_pitch']-P['qd_female_diameter_reference'],'body_with_30mm_side_allowances_mm':W+60,'straight_insertion_exceeds_assumed_opening_with_plugs':W+2*plug_spec['head_projection']>E['equipment_width_assumption'],'mount_positions_xz_mm':P['faceplate_mounts_xz'],'status':'Nominal envelope only; rack rails, hose bends and fitting tolerances unverified'}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/f'tmp/scene-long-bore-{REV}.json').write_text(json.dumps({'parameters':dict(P,mounting='faceplate'),'ports_x':xs,'cover_bolts':[],'faceplate_mounts':P['faceplate_mounts_xz'],'side_plugs':side_ports},indent=2)+'\n')
print(json.dumps(report,indent=2))
