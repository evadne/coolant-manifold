"""Photographic studio presentation of M, O-M02 or Revision P.
No CAD changes; millimetre model converted to metres for lighting/material scale.
"""
from pathlib import Path
import argparse,json,math,sys
import bpy
import bmesh
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');parser.add_argument('--variant',choices=['all','bare','connected'],default='all')
parser.add_argument('--manufacturing', choices=['O-M02'])
parser.add_argument('--iteration',choices=['P'])
parser.add_argument('--device',choices=['CPU','METAL'],default='CPU')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
assert not (args.iteration and args.manufacturing), 'Select either a layout iteration or a manufacturing issue'
REV=args.iteration or args.manufacturing or 'M'
BASE=ROOT/('output/long-bore-P' if args.iteration else 'output/manufacturing/O-M02' if args.manufacturing else 'output/long-bore-M')
OUT=BASE/'photorealistic';OUT.mkdir(parents=True,exist_ok=True)
BOSS=(json.loads((ROOT/'cad/manufacturing/O-M02.json').read_text())['boss_height'] if args.manufacturing else 3 if args.iteration else 6)*.001
bpy.ops.wm.open_mainfile(filepath=str(BASE/'product-views/assembled-unmarked.blend'))
scene=bpy.context.scene
for o in list(scene.objects):
    keep=(o.name in ('body','faceplate') or o.name.startswith(('QD3 reference /','Front M4','G1-4 side plug reference')))
    if args.iteration and o.name.startswith('QD3 reference /'):keep=False
    if not keep:bpy.data.objects.remove(o,do_unlink=True)
product=list(scene.objects)
for o in product:
    o.hide_render=False;o.hide_set(False)
    o.location*=.001;o.data.transform(Matrix.Scale(.001,4))
    for mod in o.modifiers:
        if mod.type=='BEVEL':mod.width*=.001
    if o.name.startswith('QD3 reference /') and 'Hex body' not in o.name:
        for poly in o.data.polygons:poly.use_smooth=len(poly.vertices)==4
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1

def base(name,c,metal,rough):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*c,1)
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    return m,p

def bevel(m,p,radius):
    b=m.node_tree.nodes.new('ShaderNodeBevel');b.inputs['Radius'].default_value=radius;b.samples=8
    m.node_tree.links.new(b.outputs['Normal'],p.inputs['Normal'])

pom,p=base('Black machined POM — fine satin polymer',(.004,.005,.006),0,.31)
p.inputs['IOR'].default_value=1.48
bevel(pom,p,.00012)
# Extremely subtle isotropic finish variation, not scratches or decorative markings.
n=pom.node_tree.nodes;links=pom.node_tree.links
g=n.new('ShaderNodeNewGeometry');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=14000;noise.inputs['Detail'].default_value=2
links.new(g.outputs['Position'],noise.inputs['Vector'])
r=n.new('ShaderNodeMapRange');r.inputs['To Min'].default_value=.29;r.inputs['To Max'].default_value=.34;links.new(noise.outputs['Fac'],r.inputs['Value']);links.new(r.outputs['Result'],p.inputs['Roughness'])
steel,p=base('Satin brushed stainless — directional reflection',(.56,.58,.60),1,.28)
p.inputs['Anisotropic'].default_value=.55;p.inputs['Tangent'].default_value=(1,0,0)
bevel(steel,p,.000075)
n=steel.node_tree.nodes;links=steel.node_tree.links
g=n.new('ShaderNodeNewGeometry');stretch=n.new('ShaderNodeVectorMath');stretch.operation='MULTIPLY';stretch.inputs[1].default_value=(30,18000,18000);links.new(g.outputs['Position'],stretch.inputs[0])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1;noise.inputs['Detail'].default_value=2;noise.inputs['Roughness'].default_value=.65;links.new(stretch.outputs['Vector'],noise.inputs['Vector'])
r=n.new('ShaderNodeMapRange');r.inputs['To Min'].default_value=.25;r.inputs['To Max'].default_value=.32;links.new(noise.outputs['Fac'],r.inputs['Value']);links.new(r.outputs['Result'],p.inputs['Roughness'])
nickel,p=base('Nickel-plated brass fittings — polished metal',(.66,.64,.59),1,.19)
bevel(nickel,p,.000065)
fastener,p=base('Stainless screw heads',(.53,.55,.57),1,.23);bevel(fastener,p,.000035)
for o in product:
    o.data.materials.clear();o.data.materials.append(pom if o.name=='body' else steel if o.name=='faceplate' else fastener if o.name.startswith('Front M4') else nickel)
# P uses supplier CAD below; older iterations retain their historical fitting envelopes.
connected=[]
def sleeve(name,x,z,start,end,outer,inner=0,vertices=96):
    verts=[]
    for y,r in ((start,outer),(end,outer),(start,inner),(end,inner)):
        verts.extend([(x+r*math.cos(2*math.pi*i/vertices),-BOSS-y,z+r*math.sin(2*math.pi*i/vertices)) for i in range(vertices)])
    faces=[]
    for i in range(vertices):
        j=(i+1)%vertices
        faces.extend([(i,j,vertices+j,vertices+i),(2*vertices+j,2*vertices+i,3*vertices+i,3*vertices+j),(j,i,2*vertices+i,2*vertices+j),(vertices+i,vertices+j,3*vertices+j,3*vertices+i)])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    ob=bpy.data.objects.new(name,mesh);scene.collection.objects.link(ob)
    for poly in mesh.polygons:poly.use_smooth=poly.index%4<2
    connected.append(ob);return ob

tube_mat,p=base('Translucent 10-13 polymer tube',(.89,.96,.985),0,.12)
p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.46
scene.cycles.transmission_bounces=12
if args.iteration:
    fit_dir=BASE/'koolance-fit';fit=json.loads((fit_dir/'verification.json').read_text())
    assert fit['checks']=='PASS' and not fit['scaling_applied']
    templates={}
    for rec in fit['mesh_records']:
        bpy.ops.wm.stl_import(filepath=str(fit_dir/rec['mesh']));ob=bpy.context.object
        bm=bmesh.new();bm.from_mesh(ob.data)
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
        bmesh.ops.dissolve_limit(bm,angle_limit=1e-5,verts=list(bm.verts),edges=list(bm.edges),use_dissolve_boundaries=False)
        bm.to_mesh(ob.data);bm.free();ob.data.transform(Matrix.Scale(.001,4));ob.data.update()
        for poly in ob.data.polygons:poly.use_smooth=True
        ob.data.set_sharp_from_angle(angle=math.radians(35))
        ob.data.materials.append(nickel)
        templates[(rec['part'],rec['solid_index'])]=ob.data
        bpy.data.objects.remove(ob,do_unlink=True)
    for ix in range(10):
        x=(-180+40*ix)*.001
        for iz,z in enumerate((.0235,.0635)):
            label=f'{ix+1:02d}-{iz+1}'
            for (part,index),mesh in templates.items():
                male=part=='qd3-mtg4'
                ob=bpy.data.objects.new(f'Koolance {part.upper()} / {label} / solid {index}',mesh)
                scene.collection.objects.link(ob)
                ob.location=(x,-BOSS+(0 if male else fit['female_mouth_Y_relative_to_male_sealing_face_mm']*.001),z)
                (product if male else connected).append(ob)
            # Tube tails show nominal free ID/OD; insertion under the nut is illustrative.
            tail=fit['inferred_seat_to_female_tail_mm']*.001
            ob=sleeve(f'Translucent tube 10-13 {label}',x,z,tail-.014,tail+.060,.0065,.005)
            ob.data.materials.append(tube_mat)
else:
    for ix in range(10):
        x=(-180+40*ix)*.001
        for iz,z in enumerate((.0235,.0635)):
            label=f'{ix+1:02d}-{iz+1}'
            # Female sleeve covers the male nose; its pull ring remains visibly accessible.
            for part,a,b,r,ri in [('Pull ring',.017,.025,.01185,.0081),('Receiver',.025,.043,.0107,.0075),('Tail shoulder',.043,.046,.0092,.006),('Compression collar',.046,.061,.0106,.0065)]:
                ob=sleeve(f'Female QD approximation {label} / {part}',x,z,a,b,r,ri);ob.data.materials.append(nickel)
                mod=ob.modifiers.new('Soft manufactured edges','BEVEL');mod.width=.00018;mod.segments=3
            ob=sleeve(f'Translucent tube 10-13 {label}',x,z,.059,.121,.0065,.005);ob.data.materials.append(tube_mat)


# A continuous tabletop gives a real contact shadow beneath the upright product.
floor,p=base('Warm neutral photographic surface',(.09,.10,.115),0,.55)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.00005));o=bpy.context.object;o.name='Studio tabletop';o.data.materials.append(floor)
world=bpy.data.worlds.new('Low neutral studio ambience');world.use_nodes=True;scene.world=world
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.8,.9,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.12

def area(name,loc,target,power,size_x,size_y,colour):
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='RECTANGLE';o.data.size=size_x;o.data.size_y=size_y;o.data.color=colour
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
area('Large diffused key',(-.35,-.48,.7),(0,0,.04),40,.65,.45,(1,.96,.9))
area('Long top strip highlight',(.04,.12,.65),(0,0,.035),45,.70,.13,(.94,.97,1))
area('Right soft fill',(.65,-.1,.22),(0,0,.04),35,.25,.4,(.92,.96,1))
area('Broad frontal reflection card',(-.08,-.6,.16),(0,0,.04),4,.75,.35,(1,1,1))
bpy.ops.object.camera_add(location=(.45,-1.15,.48));camera=bpy.context.object;camera.name=f'Revision {REV} photographic front three-quarter'
camera.rotation_euler=(Vector((0,-.032,.044))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='PERSP';camera.data.lens=72;camera.data.sensor_width=36;camera.data.clip_start=.01;camera.data.clip_end=250
# Deep focus preserves all twenty QDs and both rack ears; no artificial focus blur.
camera.data.dof.use_dof=False;scene.camera=camera
scene.render.engine='CYCLES';scene.cycles.samples=48 if args.preview else 256
if args.device=='METAL':
    prefs=bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type='METAL';prefs.get_devices()
    devices=[d for d in prefs.devices if d.type=='METAL']
    assert devices, 'Metal GPU requested but unavailable'
    for d in prefs.devices:d.use=d.type=='METAL'
    scene.cycles.device='GPU'
    print('Studio render device: '+', '.join(d.name for d in devices),flush=True)
scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.015 if args.preview else .006
scene.cycles.max_bounces=12;scene.cycles.glossy_bounces=8;scene.cycles.transparent_max_bounces=8
scene.render.resolution_x=3000;scene.render.resolution_y=1600;scene.render.resolution_percentage=50 if args.preview else 100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.color_depth='8'
scene.render.film_transparent=False;scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.25
assert len([o for o in product if o.name.startswith('Koolance QD3-MTG4 /' if args.iteration else 'QD3 reference /')])==(40 if args.iteration else 80)
assert len([o for o in product if o.name.startswith('Front M4')])==(12 if args.iteration else 6)
assert not any(o.type=='FONT' for o in scene.objects)
assert len(connected)==(80 if args.iteration else 100)
for variant in (['bare','connected'] if args.variant=='all' else [args.variant]):
    for o in product:
        if o.name.startswith(('QD3 reference /','Koolance QD3-MTG4 /','G1-4 side plug reference')):
            o.hide_render=variant=='bare';o.hide_set(variant=='bare')
    for o in connected:o.hide_render=variant=='bare';o.hide_set(variant=='bare')
    stem='01-bare-ports' if variant=='bare' else '02-qd3-translucent-tubes'
    scene.render.filepath=str(ROOT/f'tmp/{REV}-{variant}-preview.png' if args.preview else OUT/f'{stem}.png')
    bpy.ops.render.render(write_still=True)
    if not args.preview:
        for screen in bpy.data.screens:
            for a in screen.areas:
                if a.type=='VIEW_3D':
                    a.spaces.active.overlay.show_overlays=False;a.spaces.active.clip_end=250;a.spaces.active.region_3d.view_perspective='CAMERA'
        bpy.ops.wm.save_as_mainfile(filepath=str(OUT/f'{stem}.blend'))
if not args.preview:
    (OUT/'render-notes.json').write_text(json.dumps({
        'revision':REV,'source_scene':'../product-views/assembled-unmarked.blend',
        'boss_height_mm':BOSS*1000,
        'geometry_changes':'No manifold changes; converted millimetres to metres. Small shader-only edge rounding.',
        'bare':'20 front and 4 side ports unpopulated; M4 body screws retained (12 in P; six in O-M02).',
        'connected':('20 official QD3-MTG4 / QD3-FT10X13 STEP pairs; 20 annular 10 mm ID / 13 mm OD tube tails; four reference side plugs.' if args.iteration else '20 male/female QD approximations and 20 tube tails.'),
        'materials':['Fine satin black POM','Directionally brushed stainless faceplate','Polished nickel-plated brass fitting references','A2 stainless button screws' if args.iteration else 'A4 stainless fastener references','Translucent polymer tubing, IOR 1.46'],
        'lighting':'Four rectangular softboxes, low world illumination, tabletop contact shadows',
        'camera':'72 mm perspective, front three-quarter, deep focus',
        'render':'Cycles 256 samples, adaptive threshold 0.006, denoising, AgX Medium High Contrast',
        'resolution':[3000,1600],'surface_markings':False,
        'device':args.device,
        'scope':('Koolance supplier STEP geometry, unscaled. Coupled axial pose inferred from annular interface registration; individual supplier drawings do not state coupled length or release stroke. See ../koolance-fit/verification.json. Closed valves are not articulated. Tube tails use nominal free ID/OD; deformation over the barb and compression under the nut are not simulated. Side plugs are visual references. Manifold threads remain pilot representations.' if args.iteration else 'Approximate QD envelopes and tube tails, not a complete routed loop.'),
        'fitting_sources':fit['source_sha256'] if args.iteration else None
    },indent=2)+'\n')
