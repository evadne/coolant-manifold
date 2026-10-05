"""Revision I in an illustrative 42U four-post rack; dimensions in mm.
Reuses the preserved assembly. No exact commercial rack or hose qualification.
"""
from pathlib import Path
import math, json
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/long-bore-I/rack-installation';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'output/long-bore-I/product-views/assembled-unmarked.blend'))
scene=bpy.context.scene
# Retain only the manufactured assembly, front QDs and body-retention screws.
for o in list(scene.objects):
    if not (o.name in ('body','faceplate') or o.name.startswith('QD3 reference /') or o.name.startswith('Front M4 DIN 7991')):
        bpy.data.objects.remove(o,do_unlink=True)
assembly=list(scene.objects)
U=44.45; rack_bottom=100.; rail_height=42*U
mount_z=rack_bottom+30*U+(2*U-87)/2 # U31–U32, centred in two rack units.
for o in assembly:o.location.z+=mount_z

def mat(name,c,metal=0,rough=.4):
    m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    return m
rackmat=mat('Plain charcoal powder-coated steel',(.055,.065,.075),.55,.36)
rubber=mat('Unmarked black 10 ID 16 OD tubing',(.014,.018,.021),0,.46)
metal=mat('Unmarked nickel fitting reference',(.58,.62,.66),.9,.23)
floor=mat('Neutral studio floor',(.57,.60,.63),0,.75)

def finish(o,name,m,bevel=0):
    o.name=name;o.data.materials.clear();o.data.materials.append(m)
    if bevel:
        mod=o.modifiers.new('Small visual edge breaks','BEVEL');mod.width=bevel;mod.segments=3
        o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o

def box(name,loc,size,m,bevel=.3):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return finish(o,name,m,bevel)

def cylinder(name,loc,r,d,m):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=d,location=loc)
    return finish(bpy.context.object,name,m,.3)

# Perforated rack rail flanges: 9 mm square openings, in a repeating 3-hole pattern.
# Mesh boxes on either side of each aperture avoid hundreds of Boolean operations.
def flange(sign,y):
    xmin,xmax=(225.,260.) if sign>0 else (-260.,-225.)
    xc=sign*232.55; intervals=[];last=rack_bottom
    for u in range(42):
        for offset in (6.35,22.225,38.1):
            z=rack_bottom+u*U+offset
            intervals.append((xmin,xmax,last,z-4.5))
            intervals.extend(((xmin,xc-4.5,z-4.5,z+4.5),(xc+4.5,xmax,z-4.5,z+4.5)))
            last=z+4.5
    intervals.append((xmin,xmax,last,rack_bottom+rail_height))
    verts=[];faces=[]
    for a,b,c,d in intervals:
        k=len(verts);verts.extend([(a,y,c),(b,y,c),(b,y+3,c),(a,y+3,c),(a,y,d),(b,y,d),(b,y+3,d),(a,y+3,d)])
        faces.extend(tuple(k+i for i in f) for f in ((0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)))
    mesh=bpy.data.meshes.new('126 actual square openings');mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new('42U perforated mounting flange',mesh);scene.collection.objects.link(o);finish(o,o.name,rackmat)
    # Folded return of the illustrative rack rail, outboard of the clear opening.
    box('Rack upright return',(sign*258.5,y+24,rack_bottom+rail_height/2),(3,42,rail_height),rackmat)

for sign in (-1,1):
    for y in (0,800):flange(sign,y)
    for z in (75,rack_bottom+rail_height+25):
        box('Longitudinal frame beam',(sign*280,420,z),(40,900,40),rackmat,1)
    for y in (10,830):
        box('Outboard structural post',(sign*280,y,1020),(40,40,1930),rackmat,1)
    box('Floor outrigger',(sign*280,420,35),(60,1020,35),rackmat,1)
    for y in (-60,900):
        cylinder('Levelling foot',(sign*280,y,10),25,15,rubber)
        cylinder('Foot stud',(sign*280,y,25),6,18,metal)
for y in (-10,850):
    for z in (75,rack_bottom+rail_height+25):
        box('Transverse frame beam',(0,y,z),(520,40,40),rackmat,1)
# Four rack screws match the faceplate slot centres. Front hardware is unmarked.
for x in (-232.55,232.55):
    for z in (5.4,81.6):
        o=cylinder('Rack mounting screw',(x,-5,mount_z+z),5.5,4,metal);o.rotation_euler.x=math.pi/2
        box('Rack cage nut',(x,6,mount_z+z),(10,6,10),metal,.4)

# Four elbows/compression assemblies reuse the supplied-drawing reference envelopes.
for i in range(4):
    bpy.ops.wm.stl_import(filepath=str(ROOT/f'output/long-bore-I/meshes/elbow-reference-{i}.stl'))
    o=bpy.context.object;o.location.z+=mount_z;finish(o,f'Side rotary elbow and 10-16 compression reference {i+1}',metal)

# Swept annular tubes: OD16 / ID10, straight into the socket then R80 bends downward.
# Upper and lower rows use separate depth lanes; routes remain at X±212.8.
def tube(sign,zlocal,lane):
    R=80.;x=sign*212.8;z0=mount_z+zlocal
    points=[(x,42.2,z0,0),(x,lane,z0,0)]
    for i in range(1,49):
        theta=math.pi/2*i/48
        points.append((x,lane+R*math.sin(theta),z0-R*(1-math.cos(theta)),theta))
    points.append((x,lane+R,210.,math.pi/2))
    verts=[];faces=[];N=48
    for x,y,z,t in points:
        for radius in (8.,5.):
            for j in range(N):
                a=2*math.pi*j/N
                verts.append((x+radius*math.cos(a),y-radius*math.sin(a)*math.sin(t),z-radius*math.sin(a)*math.cos(t)))
    for k in range(len(points)-1):
        for ring in (0,1):
            for j in range(N):
                a=k*2*N+ring*N+j;b=k*2*N+ring*N+(j+1)%N
                f=(a,b,b+2*N,a+2*N);faces.append(f if ring==0 else f[::-1])
    for k in (0,len(points)-1):
        for j in range(N):
            a=k*2*N+j;b=k*2*N+(j+1)%N;faces.append((a,a+N,b+N,b) if k==0 else (a,b,b+N,a+N))
    mesh=bpy.data.meshes.new('Annular 10-16 tube');mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new(f'10-16 tube side {sign} row {zlocal}',mesh);scene.collection.objects.link(o);finish(o,o.name,rubber)
    for p in mesh.polygons:p.use_smooth=True
    return o
hoses=[tube(sign,z,lane) for sign in (-1,1) for z,lane in ((23.5,140.),(63.5,220.))]
assert len(hoses)==4
assert not any(o.type=='FONT' for o in scene.objects)
box('Studio floor',(0,300,-10),(24000,24000,10),floor,0)
# Soft side and rear lighting exposes the fittings against the black POM.
world=bpy.data.worlds.new('Rack studio');world.use_nodes=True;scene.world=world
world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.70,.76,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.55

def area(name,loc,target,power,size):
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
area('Large rear key',(-1100,1700,2400),(0,250,1250),85000000,1500)
area('Right reflection',(1100,900,2100),(0,200,1400),65000000,1200)
area('Front fill',(0,-900,1700),(0,300,1300),45000000,1100)
scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.view_settings.view_transform='AgX'
scene.render.resolution_percentage=100
cameras=[]
for name,loc,target,scale,res in [
 ('01-42U-rear-three-quarter',(-3300,3300,2300),(0,410,1010),2780,(1800,2200)),
 ('02-installed-manifold-rear-detail',(-180,560,mount_z+240),(0,60,mount_z+20),680,(2200,1500))]:
    bpy.ops.object.camera_add(location=loc);o=bpy.context.object;o.name=name;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.type='ORTHO';o.data.ortho_scale=scale;o.data.clip_end=15000
    o.data.clip_start=200 if name.startswith('02') else .1
    cameras.append((o,res));scene.camera=o;scene.render.resolution_x,scene.render.resolution_y=res;scene.render.filepath=str(OUT/f'{name}.png')
    bpy.ops.render.render(write_still=True)
scene.camera=cameras[1][0];scene.render.resolution_x,scene.render.resolution_y=cameras[1][1]
for screen in bpy.data.screens:
    for a in screen.areas:
        if a.type=='VIEW_3D':
            a.spaces.active.overlay.show_overlays=False;a.spaces.active.clip_end=15000;a.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'revision-I-in-42U-rack.blend'))
(OUT/'scene-notes.json').write_text(json.dumps({'revision':'I','rack':'Illustrative 42U four-post open frame','rack_units':42,'rack_pitch_mm':U,'mounting_height':'U31–U32','manifold_bottom_world_z_mm':mount_z,'front_to_rear_mounting_planes_mm':800,'assumed_equipment_opening_mm':450,'side_elbows_and_compression_fittings':4,'tube_count':4,'tube_ID_OD_mm':[10,16],'tube_centreline_bend_radius_mm':80,'tube_vertical_depth_lanes_mm':[220,300],'model_scope':'Spatial illustration; rack and fittings are reference geometry, not exact commercial models. Tube tails intentionally stop without downstream equipment; not a complete hydraulic circuit. No rack-fit, hose bend-radius or structural qualification.','source_assembly':'../product-views/assembled-unmarked.blend','renders':[o.name+'.png' for o,r in cameras]},indent=2)+'\n')
