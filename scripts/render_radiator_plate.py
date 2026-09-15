"""Blender review of CAD-derived R1 plate, with illustrative radiator and fans."""
from pathlib import Path
import json, math
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'output/radiator-R1'
P=json.loads((ROOT/'cad/radiator/R1.json').read_text()); H=P['height']
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
bpy.ops.wm.stl_import(filepath=str(OUT/'rack-plate-R1.stl'));plate=bpy.context.object
plate.name='R1 rack plate - exact CAD mesh';plate.rotation_euler.x=math.pi/2;plate.data.materials.append(steel);bevel(plate,.15)
# The source CAD is XY, extruded +Z. Rotation maps it to X,-thickness,height.
assembly=[]
def keep(o):assembly.append(o);return o
keep(box('Illustrative 400 mm radiator core',(0,22.5,H/2),(400,42,400),black))
for x in (-206,206):keep(box('Radiator structural side rail',(x,22.5,H/2),(10,45,424),black,.5))
for z in (H/2-212,H/2+212):keep(box('Radiator end chamber',(0,22.5,z),(422,45,17),black,1.5))
# Visible fin texture on the front and rear; radiator is an envelope, not new production CAD.
for y in (.6,44.1):
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
  keep(cyl('M3 washer',(x,-3.3,z),3.5,.6,steel))
  screw=keep(cyl('M3 pan head reference',(x,-4.8,z),2.8,2.4,steel));bevel(screw,.3)
  cut(screw,box('Drive recess',(x,-5.9,z),(2.3,.8,.55),black))
for x in (-140.5,140.5):
 keep(cyl('Top G1-4 plug reference',(x,22.5,H/2+221.8),9,2.6,steel,'Z'))
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
scene.render.resolution_x=1500;scene.render.resolution_y=1300;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG'
def render(name,loc,bare=False):
 for o in assembly:o.hide_render=bare
 camera.location=loc;camera.rotation_euler=(Vector((0,20,H/2))-camera.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(OUT/name);bpy.ops.render.render(write_still=True)
render('01-plate-perspective.png',(630,-1100,700),True)
render('02-radiator-front.png',(630,-1100,700))
render('03-radiator-rear.png',(-700,1100,650))
camera.location=(630,-1100,700);camera.rotation_euler=(Vector((0,20,H/2))-camera.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'radiator-rack-plate-R1.blend'))
