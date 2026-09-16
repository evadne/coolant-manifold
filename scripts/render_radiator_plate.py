"""Blender review of CAD-derived R1 plate, with illustrative radiator and fans."""
from pathlib import Path
import json, math, argparse, sys
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--revision',choices=['R1','R2','R3','R4','R5','R6','R7'],default='R1')
parser.add_argument('--plate-only',action='store_true')
parser.add_argument('--device',choices=['CPU','METAL'],default='CPU')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
REV=args.revision
OUT=ROOT/f'output/radiator-{REV}'
P=json.loads((ROOT/f'cad/radiator/{REV}.json').read_text()); H=P['height'];T=P['thickness']
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001
def mat(name,c,metal=0,rough=.4):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes.get('Principled BSDF')
 n.inputs['Base Color'].default_value=(*c,1);n.inputs['Metallic'].default_value=metal;n.inputs['Roughness'].default_value=rough
 return m
steel=mat('Satin 304 stainless',(.49,.53,.57),.85,.31)
black=mat('Radiator black coating',(.018,.024,.030),.4,.37)
fins=mat('Dark metallic fins',(.065,.074,.081),.65,.35)
plastic=mat('Fan polymer',(.018,.021,.025),.05,.42)
floor=mat('Studio floor',(.22,.25,.28),.1,.5)
def bevel(o,r=.3):
 m=o.modifiers.new('Edge highlights','BEVEL');m.width=r;m.segments=3
 o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
def box(name,loc,size,material,r=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material)
 if r:bevel(o,r)
 return o
def cyl(name,loc,r,d,material,axis='Y'):
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=d,location=loc,rotation=(math.pi/2,0,0) if axis=='Y' else (0,0,0))
 o=bpy.context.object;o.name=name;o.data.materials.append(material);return o
def cut(a,b):
 m=a.modifiers.new('Cut','BOOLEAN');m.operation='DIFFERENCE';m.object=b
 bpy.context.view_layer.objects.active=a;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(b,do_unlink=True)
bpy.ops.wm.stl_import(filepath=str(OUT/f'rack-plate-{REV}.stl'));plate=bpy.context.object
plate.name=f'{REV} rack plate - exact CAD mesh';plate.rotation_euler.x=math.pi/2;plate.data.materials.append(steel);bevel(plate,.15)
if REV=='R6':
 brushed=steel.copy();brushed.name='R6-M02 satin brushed along rack width X'
 n=brushed.node_tree.nodes;p=n.get('Principled BSDF');p.inputs['Anisotropic'].default_value=.55;p.inputs['Tangent'].default_value=(1,0,0)
 g=n.new('ShaderNodeNewGeometry');stretch=n.new('ShaderNodeVectorMath');stretch.operation='MULTIPLY';stretch.inputs[1].default_value=(.03,18,18)
 noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1
 remap=n.new('ShaderNodeMapRange');remap.inputs['To Min'].default_value=.28;remap.inputs['To Max'].default_value=.34
 links=brushed.node_tree.links;links.new(g.outputs['Position'],stretch.inputs[0]);links.new(stretch.outputs['Vector'],noise.inputs['Vector']);links.new(noise.outputs['Fac'],remap.inputs['Value']);links.new(remap.outputs['Result'],p.inputs['Roughness'])
 plate.data.materials.clear();plate.data.materials.append(brushed)
# The source CAD is XY, extruded +Z. Rotation maps it to X,-thickness,height.
assembly=[];front_hardware=[];front_fans=[];rear_fans=[]
NEW=REV in ['R3','R4','R5','R6','R7']
def keep(o):assembly.append(o);return o
keep(box('Illustrative 400 mm radiator core',(0,22.5,H/2),(400,32 if NEW else 42,400),black))
for x in (-206,206):keep(box('Radiator structural side rail',(x,22.5,H/2),(10,45,424),black,.5))
for z in (H/2-212,H/2+212):keep(box('Radiator end chamber',(0,22.5,z),(422,45,17),black,1.5))
# Visible fin texture on the front and rear; radiator is an envelope, not new production CAD.
for y in ((6.5,38.5) if NEW else (.6,44.1)):
 for i in range(201):keep(box('Cooling fin',(i*1.98-198,y,H/2),(.22,.6,396),fins))
 for z in range(-190,200,20):keep(box('Core cross tube',(0,y-.2,H/2+z),(396,.8,2),black))
# Retained stock rear plate represented by its outline and four circular fan apertures.
rear=keep(box('Retained opposite 200 mm fan plate',(0,45.75,H/2),(420,1.5,420),black))
for x in (-100,100):
 for dz in (-100,100):cut(rear,cyl('Aperture cutter',(x,45.75,H/2+dz),97.5,5,black))
bevel(rear,.15)
for x in P['radiator_mount_x']:
 for dy in P['radiator_mount_y_from_centre']:
  z=H/2+dy
  if not NEW:keep(cyl('M3 washer',(x,-T-.3,z),3.5,.6,steel))
  screw=keep(cyl('M3 pan head reference',(x,-T-(1.2 if NEW else 1.8),z),2.8,2.4,steel));bevel(screw,.3)
  cut(screw,box('Drive recess',(x,-T-(2.3 if NEW else 2.9),z),(2.3,.8,.55),black))
for x in (-140.5,140.5):
 keep(cyl('Top G1-4 plug reference',(x,22.5,H/2+221.8),9,2.6,steel,'Z'))
# Noctua official reference meshes: pad-to-pad 32 mm, airflow +Y.
if NEW:
 beige=mat('Noctua frame polymer',(.55,.43,.29),0,.5)
 brown=mat('Noctua impeller and pads',(.15,.07,.035),0,.48)
 meshpaths=sorted((ROOT/'output/radiator-fan-integration/reference-meshes').glob('fan-*.stl'))
 assert len(meshpaths)==10, 'Run prepare_radiator_fan_mounts.py first'
 def add_fan(x,dy,centre_y,group):
  for path in meshpaths:
   bpy.ops.wm.stl_import(filepath=str(path));o=bpy.context.object
   o.name='NF-A20 reference '+path.stem;o.location=(x,centre_y,H/2+dy)

   if x>0:o.rotation_euler.y=math.pi
   o.data.materials.append(beige if path.stem=='fan-00' else brown);keep(o);group.append(o)
 for x in P['aperture_centres_x']:
  for dy in P['aperture_centres_y_from_centre']:add_fan(x,dy,-T-16,front_fans)
 # Opposite original fan plate retains its 200 mm grid.
 for x in (-100,100):
  for dy in (-100,100):add_fan(x,dy,62.5,rear_fans)
 def washer(name,x,y,z):
  o=keep(cyl(name,(x,y,z),4.5,.8,steel));cut(o,cyl('Washer bore',(x,y,z),2.15,2,steel));return o
 def hardware(o):front_hardware.append(o);return o
 for x in P['aperture_centres_x']:
  for dy in P['aperture_centres_y_from_centre']:
   for dx in (-85,85):
    for dz in (-85,85):
     xx=x+dx;zz=H/2+dy+dz;seat=-T-32-.8 if REV=='R3' else .8;length=P['fan_bolt_length'];direction=1 if REV=='R3' else -1
     hardware(washer('M4 front washer',xx,-T-32-.4,zz))
     hardware(keep(cyl('M4 screw shank reference',(xx,seat+direction*length/2,zz),2,length,steel)))
     head=hardware(keep(cyl('M4 button hex socket head',(xx,seat-direction*1.1,zz),3.8,2.2,steel)))
     bevel(head,.65)
     bpy.ops.mesh.primitive_cylinder_add(vertices=6,radius=1.443,depth=1.5,location=(xx,seat-direction*2.1,zz),rotation=(math.pi/2,0,0));cut(head,bpy.context.object)
     if REV in ['R4','R5','R6','R7']:
      hardware(washer('M4 rear washer',xx,.4,zz))
      bpy.ops.mesh.primitive_cylinder_add(vertices=6,radius=7/math.sqrt(3),depth=3.2,location=(xx,-T-32-.8-1.6,zz),rotation=(math.pi/2,0,0))
      nut=hardware(keep(bpy.context.object));nut.name='DIN 934 M4 nut';nut.data.materials.append(steel)
      cut(nut,cyl('Nut pilot reference',(xx,-T-32-.8-1.6,zz),1.7,5,steel));bevel(nut,.15)
else:
 # Four 200 mm fans, 30 mm thickness used as an explicit visual envelope.
 for x in (-100,100):
  for dz in (-100,100):
   z=H/2+dz
   fan=keep(box('200 mm fan frame',(x,61.5,z),(200,30,200),plastic,2))
   cut(fan,cyl('Fan bore cutter',(x,61.5,z),95,34,black))
   keep(cyl('Fan hub',(x,67,z),26,19,plastic))
   for j in range(9):
    a=j*2*math.pi/9;verts=[]
    for r,theta,y in [(24,a,64),(88,a+.32,64),(92,a+.68,60),(35,a+.68,60)]:
     verts.append((x+r*math.cos(theta),y,z+r*math.sin(theta)))
    mesh=bpy.data.meshes.new('Fan blade mesh');mesh.from_pydata(verts,[],[(0,1,2,3)]);mesh.update()
    o=bpy.data.objects.new('Fan blade',mesh);scene.collection.objects.link(o);o.data.materials.append(plastic)
    m=o.modifiers.new('Blade thickness','SOLIDIFY');m.thickness=1.3;keep(o)
   for sx in (-78,78):
    for sz in (-78,78):keep(cyl('Rear fan screw reference',(x+sx,77,z+sz),3,2,steel))
# Studio lighting in millimetre scene units.
box('Studio ground',(0,0,-4),(4000,4000,2),floor)
world=bpy.data.worlds.new('Studio world');scene.world=world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.25,.28,.32,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.45
def light(loc,power,size):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size
 o.rotation_euler=(Vector((0,15,H/2))-o.location).to_track_quat('-Z','Y').to_euler()
light((200,-450,900),18000000,650);light((-600,-200,450),13000000,550);light((300,650,650),20000000,450)
bpy.ops.object.camera_add();camera=bpy.context.object;scene.camera=camera;camera.data.type='ORTHO';camera.data.ortho_scale=650;camera.data.clip_end=10000
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
if args.device=='METAL':
 prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
 assert any(d.type=='METAL' for d in prefs.devices)
 for d in prefs.devices:d.use=d.type=='METAL'
 scene.cycles.device='GPU'
scene.render.resolution_x=1500;scene.render.resolution_y=1300;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG'
def render(name,loc,bare=False):
 for o in assembly:o.hide_render=bare
 camera.location=loc;camera.rotation_euler=(Vector((0,20,H/2))-camera.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(OUT/name);bpy.ops.render.render(write_still=True)
if REV in ['R2','R3','R4','R5','R6','R7']:render('00-plate-front.png',(0,-1000,H/2),True)
render('01-plate-perspective.png',(630,-1100,700),True)
if not args.plate_only:render('02-radiator-front.png',(630,-1100,700))
if not args.plate_only:render('03-radiator-rear.png',(-700,1100,650))
if NEW and not args.plate_only:
 # Expose rear fasteners without the radiator hiding the nut stack.
 for o in assembly:o.hide_render=o not in front_hardware and o not in front_fans
 camera.location=(-620,1000,650);camera.rotation_euler=(Vector((0,-10,H/2))-camera.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(OUT/'04-fan-fasteners-rear.png');bpy.ops.render.render(write_still=True)
 for o in assembly:o.hide_render=False

if P.get('cable_notch'):
 for o in assembly:o.hide_render=True
 camera.data.ortho_scale=34
 camera.location=(14,-60,H+14);camera.rotation_euler=(Vector((0,-1,H-4))-camera.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(OUT/'05-cable-notch-detail.png');bpy.ops.render.render(write_still=True)
 camera.data.ortho_scale=650
# Dedicated outline-corner detail at true CAD radius.
if REV=='R7':
 for o in assembly:o.hide_render=True
 camera.data.ortho_scale=30
 camera.location=(P['width']/2+10,-60,H+12);camera.rotation_euler=(Vector((P['width']/2-7,-1,H-7))-camera.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(OUT/'06-R5-corner-detail.png');bpy.ops.render.render(write_still=True)
 camera.data.ortho_scale=650
for o in assembly:o.hide_render=args.plate_only
camera.location=(630,-1100,700);camera.rotation_euler=(Vector((0,20,H/2))-camera.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/f'radiator-rack-plate-{REV}.blend'),compress=True)
