"""Add P fastener references and verify the new plain-bore retention details.
Run build_long_bore.py --iteration P first. Threads are pilot representations.
"""
from pathlib import Path
import json, math
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'cad/iterations/P-long-bore.json').read_text());f=p['faceplate_fastener']
out=ROOT/'output/long-bore-P/cad';mesh=ROOT/'output/long-bore-P/meshes'
body=cq.importers.importStep(str(out/'body.step')).val();plate=cq.importers.importStep(str(out/'faceplate.step')).val()
# ISO 7380 supplier external dimensions. Dome is a visual approximation;
# head underside at Y0, shank towards +Y. No decorative markings.
r=f['head_diameter']/2;h=f['head_height'];rim=.3;cap=h-rim
dome_height=cap+.3
sr=(r*r+dome_height*dome_height)/(2*dome_height)
sphere=cq.Solid.makeSphere(sr,cq.Vector(0,sr-h-.3,0),angleDegrees1=-90)
capbox=cq.Solid.makeBox(20,cap,20,cq.Vector(-10,-h,-10))
head=sphere.intersect(capbox).fuse(cq.Solid.makeCylinder(r,rim,cq.Vector(0,-rim,0),cq.Vector(0,1,0)))
hexcut=cq.Workplane('XZ',origin=(0,-h-.1,0)).polygon(6,2*2.5/math.sqrt(3)).extrude(-(1.3+.1)).val()
head=head.cut(hexcut)
assert head.isValid() and abs(head.BoundingBox().ylen-h)<1e-6
cq.exporters.export(head,str(mesh/'button-head.stl'),tolerance=.015,angularTolerance=.06)
shank=cq.Solid.makeCylinder(1.6,16,cq.Vector(0,0,0),cq.Vector(0,1,0))
screw=head.fuse(shank);cq.exporters.export(screw,str(out/'REFERENCE-M4x16-ISO7380.step'))
assy=cq.Assembly(name='RM10_revision_P_plain_bores')
assy.add(body,name='POM');assy.add(plate,name='faceplate')
for i,(x,z) in enumerate(p['faceplate_mounts_xz']):
 placed=screw.translate(cq.Vector(x,-2,z))
 assert placed.intersect(body).Volume()<1e-6 and placed.intersect(plate).Volume()<1e-6
 assy.add(placed,name=f'REFERENCE_button_screw_{i+1}')
assy.export(str(out/'assembled-with-button-screws.step'))
point=1.65/math.tan(math.radians(59))
wet=[cq.importers.importStep(str(out/f'fluid-network-{i}.step')).val() for i in (1,2)]
clearance=min(cq.Solid.makeCylinder(2,18+point,cq.Vector(x,0,z),cq.Vector(0,1,0)).distance(v) for x,z in p['faceplate_mounts_xz'] for v in wet)
assert clearance>2
xs=[-180+40*i for i in range(10)]
head_to_keepout=min(math.hypot(mx-x,mz-z)-3.8-18 for mx,mz in p['faceplate_mounts_xz'] for x in xs for z in p['port_rows_z'])
assert head_to_keepout>2
# Check every retention hole has cylindrical radius 2.25; plate has no conical faces.
assert not any(face.geomType()=='CONE' for face in plate.Faces())
assert sum(face.geomType()=='CYLINDER' and abs(face._geomAdaptor().Cylinder().Radius()-2.25)<1e-6 for face in plate.Faces())==12
report={'revision':'P','status':'Separate design variation; O-M02 retained',
 'plate_thickness_mm':2,'plate_mass_kg':plate.Volume()*7.9e-6,'plate_clearance_holes':12,'countersinks':0,
 'body_mounts_xz_mm':p['faceplate_mounts_xz'],'boss_height_mm':3,'boss_projection_mm':1,
 'body_depth_including_bosses_mm':43,'head_diameter_mm':7.6,'head_height_mm':2.2,
 'fastener':'12 x M4 x 16 ISO 7380-1 A2 stainless, Westfield WF2237',
 'screw_nominal_reach_in_POM_mm':14,'minimum_full_form_thread_from_end_of_entry_mm':16,
 'M4_entry_depth_mm':.55,'M4_full_diameter_pilot_depth_mm':18,'M4_drill_tip_depth_mm':18+point,
 'minimum_M4_envelope_to_pilot_represented_wet_network_mm':clearance,
 'minimum_head_edge_to_diameter_36_port_keepout_mm':head_to_keepout,
 'minimum_head_edge_to_body_top_bottom_mm':7-3.8,
 'alternative_screws':'Plain-bearing M4 x 0.7 heads only; check head/washer envelope, screw length and engagement. Countersunk screws incompatible.',
 'scope':'Geometry checks only; POM thread stripping, creep, torque, coupling loads and rack stiffness not qualified. Thread helices omitted.'}
(out/'retention-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
