"""Editable Blender review scene built from the CAD's exact tessellation."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
S=json.loads((ROOT/'tmp/scene.json').read_text());P=S['parameters']
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001

def mat(name,colour,metal=0,rough=.4):
    m=bpy.data.materials.new(name);m.diffuse_color=(*colour,1);m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*colour,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
    return m
black=mat('Black Delrin',(.028,.037,.044),0,.31)
steel=mat('Satin stainless steel',(.46,.53,.59),.8,.3)
nickel=mat('QD nickel reference',(.55,.59,.62),.85,.24)
blue=mat('Supply blue',(.025,.43,.75),.3,.3)
red=mat('Return orange',(.95,.23,.075),.3,.3)
white=mat('Legend',(.78,.85,.88),.1,.5)
floor=mat('Backdrop',(.065,.085,.115),0,.7)

def stl(name,material):
    bpy.ops.wm.stl_import(filepath=str(ROOT/'tmp/mesh'/f'{name}.stl'));o=bpy.context.object;o.name=name;o.data.materials.append(material)
    mod=o.modifiers.new('Small visual edge break','BEVEL');mod.width=.18;mod.segments=2
    o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o
parts={n:stl(n,black if n=='body' else steel) for n in ('body','lid','bracket_left','bracket_right')}

def cyl(name,x,y,z,r,depth,material,vertices=64,axis='Y'):
    rot=(math.pi/2,0,0) if axis=='Y' else ((0,math.pi/2,0) if axis=='X' else (0,0,0))
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=(x,y,z),rotation=rot)
    o=bpy.context.object;o.name=name;o.data.materials.append(material)
    bevel=o.modifiers.new('Machined edges','BEVEL');bevel.width=.18;bevel.segments=2
    o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o

def label(txt,x,y,z,size,material,front=False):
    bpy.ops.object.text_add(location=(x,y,z),rotation=(math.pi/2,0,0) if front else (0,0,0))
    o=bpy.context.object;o.name='Legend '+txt;o.data.body=txt;o.data.size=size;o.data.align_x='CENTER';o.data.extrude=.015;o.data.materials.append(material);return o

qd=[];females=[]
for j,z in enumerate(P['port_rows_z']):
    colour=blue if j==0 else red
    for i,x in enumerate(S['ports_x']):
        for name,start,end,r,v in [('Seat',0,2,9.9,64),('Hex',2,10,12.7,6),('Barrel',10,18,10.7,64),('Nose',18,32.1,8,64)]:
            qd.append(cyl('REFERENCE QD3 male '+name,x,-(start+end)/2,z,r,end-start,nickel,v))
        qd.append(cyl('Port colour band',x,-11,z,10.85,1.8,colour))
        txt=('IN' if j==0 else 'OUT') if i==0 else (f'S{i}' if j==0 else f'R{i}')
        label(txt,x,-.12,z+14,3.4,white,True)
        if i in (2,6):
            females.append(cyl('REFERENCE female pull ring',x,-32,z,11.85,20,nickel))
            females.append(cyl('REFERENCE female tail',x,-49,z,10,14,black))
            females.append(cyl('REFERENCE compression hex',x,-60,z,13.28,8,nickel,6))
            females.append(cyl('REFERENCE tube',x,-89,z,8,50,black))
for x,z in S['cover_bolts']:
    cyl('M4 countersunk head reference',x,42.75,z,3.7,.5,steel)
    cyl('M4 socket reference',x,43.02,z,1.3,.06,black,6)
for sign in (-1,1):
    for y,z in S['ear_mounts']:
        cyl('M5 countersunk head reference',sign*222.25,y,z,4.8,.5,steel,axis='X')
label('RM8  /  PARALLEL',-110,17,87.12,5.8,white)
label('2U   -   REV A',110,17,87.12,5.8,white)
label('S',-211,-.15,22,5,blue,True);label('R',-211,-.15,62,5,red,True)
# Blue/orange thin identification bars in the dry middle land; visual engraving only.
for z,material in ((7,blue),(47,red)):
    bpy.ops.mesh.primitive_cube_add(size=1,location=(0,-.1,z));o=bpy.context.object;o.name='Colour identification strip';o.dimensions=(398,.12,.8);o.data.materials.append(material)

bpy.ops.mesh.primitive_plane_add(size=2500,location=(0,0,-3));ground=bpy.context.object;ground.name='Studio floor';ground.data.materials.append(floor)
world=bpy.data.worlds.new('Studio world');scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.23,.28,.35,1);world.node_tree.nodes['Background'].inputs[1].default_value=.5

def light(name,loc,energy,size):
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=energy;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,25))-o.location).to_track_quat('-Z','Y').to_euler()
light('Key softbox',(0,-200,450),4500000,450)
light('Rim softbox',(100,200,350),6000000,350)
light('Fill softbox',(-350,-50,170),2000000,250)
bpy.ops.object.camera_add(location=(300,-540,340));cam=bpy.context.object;cam.rotation_euler=(Vector((0,-12,40))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=600;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=40;scene.cycles.use_denoising=True
scene.render.resolution_x=1800;scene.render.resolution_y=1050;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG'
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_distance=650;area.spaces.active.region_3d.view_location=(0,0,40);area.spaces.active.clip_end=10000
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'output'/'manifold-review.blend'))
scene.render.filepath=str(ROOT/'output/images'/'assembled.png');bpy.ops.render.render(write_still=True)
# Rear cover removed. Actual pockets are shown, not a fictitious internal route.
parts['lid'].hide_render=True
for o in bpy.data.objects:
    if o.name.startswith('M4'):o.hide_render=True
for o in females:o.hide_render=True
cam.location=(220,440,330);cam.rotation_euler=(Vector((0,20,43))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=550
scene.render.filepath=str(ROOT/'output/images'/'open-galleries.png');bpy.ops.render.render(write_still=True)
print('Saved editable Blender model and two review renders.')
