"""Prepare unscaled official Koolance STEP meshes for Revision P visual integration.
Separate source parts are retained. Coupled axial pose is an explicitly inferred
registration of annular interface features, not a supplier coupled-length drawing.
"""
from pathlib import Path
import cadquery as cq
import json,math,hashlib
from OCP.BRepAdaptor import BRepAdaptor_Surface
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'docs/references/koolance-qd3';OUT=ROOT/'output/long-bore-P/koolance-fit';OUT.mkdir(parents=True,exist_ok=True)
models={n:cq.importers.importStep(str(SRC/f'{n}.step')).val() for n in ('qd3-mtg4','qd3-ft10x13')}
for s in models.values():assert s.isValid()
# Use the common cylinder axis in each independent supplier export.
def axis_centre(s):
 f=max((f for f in s.Faces() if f.geomType()=='CYLINDER'),key=lambda f:f.Area())
 c=BRepAdaptor_Surface(f.wrapped).Cylinder();v=c.Axis().Direction();p=c.Location()
 assert abs(v.X())>.999999
 return p.Y(),p.Z()
def planes(s):
 return sorted({f.Center().x for f in s.Faces() if f.geomType()=='PLANE' and abs(f.normalAt().x)>.999999})
m=models['qd3-mtg4'];f=models['qd3-ft10x13'];mx=planes(m);fx=planes(f)
# Drawing: 4.50 mm thread projection measured from the fitting mounting face.
thread_tip=max(mx);male_seat=min(mx,key=lambda x:abs(x-(thread_tip-4.5)))
assert abs(thread_tip-male_seat-4.5)<.01
female_mouth=max(fx)
# Inferred engagement: male annular latch-groove centre and female annular feature.
mt=[];ft=[]
for source,target in ((m,mt),(f,ft)):
 for face in source.Faces():
  if face.geomType()=='TORUS':
   t=BRepAdaptor_Surface(face.wrapped).Torus()
   target.append((t.MajorRadius(),t.MinorRadius(),t.Location().X()))
groove=sorted({x for r,rr,x in mt if abs(r-8.45)<1e-5 and abs(rr-1)<1e-5})
assert len(groove)==2
male_registration=sum(groove)/2
female_registration=next(x for r,rr,x in ft if abs(r-9.7)<1e-5 and abs(rr-.5)<1e-5)
female_offset=male_registration-male_seat-(female_registration-female_mouth)
records=[]
for name,source in models.items():
 cy,cz=axis_centre(source);origin=male_seat if name=='qd3-mtg4' else female_mouth
 for i,s in enumerate(source.Solids()):
  # X axis becomes assembly Y; fitting projects into negative Y from seat at Y0.
  normal=s.translate(cq.Vector(-origin,-cy,-cz)).rotate((0,0,0),(0,0,1),90)
  path=OUT/f'{name}-{i}.stl';cq.exporters.export(normal,str(path),tolerance=.025,angularTolerance=.06)
  verts,_=normal.tessellate(.005,.04)
  bounds=[[min(getattr(v,k) for v in verts),max(getattr(v,k) for v in verts)] for k in ('x','y','z')]
  records.append({'part':name,'solid_index':i,'mesh':path.name,'bounds_xyz_mm':bounds})
assert len(records)==5
published={'male_overall_length_mm':36.6,'male_length_tolerance_mm':.5,'male_hex_across_flats_mm':22,'male_max_diameter_mm':23.9,'male_thread_projection_mm':4.5,'male_shoulder_diameter_mm':19.8,'female_body_overall_length_mm':49.1,'female_length_tolerance_mm':.5,'female_hex_across_flats_mm':24,'female_max_diameter_mm':26.1,'female_pull_ring_diameter_mm':23.7,'compression_nut_length_mm':15,'compression_nut_hex_across_flats_mm':21,'compression_nut_max_diameter_mm':22.4,'tube_id_mm':10,'tube_od_mm':13}
# Compare drawing lengths with actual planar end datums, avoiding loose curved BREP bounds.
assert abs(max(mx)-min(mx)-published['male_overall_length_mm'])<=.5
assert abs(max(fx)-min(fx)-published['female_body_overall_length_mm'])<=.5
# Verify published radial surfaces in supplied BREP, without rescaling them.
def has_radius(shape,r,tol=.001):
 return any(face.geomType()=='CYLINDER' and abs(BRepAdaptor_Surface(face.wrapped).Cylinder().Radius()-r)<tol for face in shape.Faces())
for shape,r in [(m,11.95),(m,9.9),(f,13.05),(f,11.85),(f,11.2)]:assert has_radius(shape,r)
female_tail=min(fx)-female_mouth+female_offset
report={'revision':'P','source':'Unscaled Koolance supplier STEP files; rigid transforms only','published_dimensions':published,
 'male_mounting_face_source_x':male_seat,'female_mouth_source_x':female_mouth,
 'male_planar_end_length_mm':max(mx)-min(mx),'male_thread_projection_from_model_mm':thread_tip-male_seat,
 'female_planar_end_length_mm':max(fx)-min(fx),
 'female_mouth_Y_relative_to_male_sealing_face_mm':female_offset,
 'inferred_seat_to_female_tail_mm':-female_tail,
 'inferred_axial_pose':'Register midpoint of male R8.45/r1 annular groove with female R9.7/r0.5 annular feature. This is an inferred presentation pose; Koolance individual drawings do not dimension the coupled length or release stroke. Closed-valve interior geometry is not articulated.',
 'nominal_gap_at_40mm_pitch_mm':{'maximum_body_envelopes':40-26.1,'pull_ring_envelopes':40-23.7},
 'scaling_applied':False,'surface_text_added':False,'manifold_geometry_changed':False,
 'mesh_records':records,'source_sha256':{n:hashlib.sha256((SRC/f'{n}.step').read_bytes()).hexdigest() for n in models},'checks':'PASS'}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='mesh_records'},indent=2))
