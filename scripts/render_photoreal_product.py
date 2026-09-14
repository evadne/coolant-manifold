"""Photographic studio presentation of the existing Revision M assembly.
No CAD changes; millimetre model converted to metres for lighting/material scale.
"""
from pathlib import Path
import argparse,json,math,sys
import bpy
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');parser.add_argument('--variant',choices=['all','bare','connected'],default='all')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=ROOT/'output/long-bore-M/photorealistic';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'output/long-bore-M/product-views/assembled-unmarked.blend'))
scene=bpy.context.scene
for o in list(scene.objects):
    keep=(o.name in ('body','faceplate') or o.name.startswith(('QD3 reference /','Front M4 DIN 7991','G1-4 side plug reference')))
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
fastener,p=base('A4 stainless screw heads',(.53,.55,.57),1,.23);bevel(fastener,p,.000035)
for o in product:
    o.data.materials.clear();o.data.materials.append(pom if o.name=='body' else steel if o.name=='faceplate' else fastener if o.name.startswith('Front M4') else nickel)
# Simplified connected female halves. Dimensions are visual envelopes, not supplier CAD.
connected=[]
def sleeve(name,x,z,start,end,outer,inner=0,vertices=96):
    verts=[]
    for y,r in ((start,outer),(end,outer),(start,inner),(end,inner)):
        verts.extend([(x+r*math.cos(2*math.pi*i/vertices),-.006-y,z+r*math.sin(2*math.pi*i/vertices)) for i in range(vertices)])
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
bpy.ops.object.camera_add(location=(.45,-1.15,.48));camera=bpy.context.object;camera.name='Revision M photographic front three-quarter'
camera.rotation_euler=(Vector((0,-.032,.044))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='PERSP';camera.data.lens=72;camera.data.sensor_width=36;camera.data.clip_start=.01;camera.data.clip_end=250
# Deep focus preserves all twenty QDs and both rack ears; no artificial focus blur.
camera.data.dof.use_dof=False;scene.camera=camera
scene.render.engine='CYCLES';scene.cycles.samples=48 if args.preview else 256
scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.015 if args.preview else .006
scene.cycles.max_bounces=12;scene.cycles.glossy_bounces=8;scene.cycles.transparent_max_bounces=8
scene.render.resolution_x=3000;scene.render.resolution_y=1600;scene.render.resolution_percentage=50 if args.preview else 100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.color_depth='8'
scene.render.film_transparent=False;scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.25
assert len([o for o in product if o.name.startswith('QD3 reference /')])==80
assert len([o for o in product if o.name.startswith('Front M4')])==6
assert not any(o.type=='FONT' for o in scene.objects)
assert len(connected)==100
for variant in (['bare','connected'] if args.variant=='all' else [args.variant]):
    for o in product:
        if o.name.startswith(('QD3 reference /','G1-4 side plug reference')):
            o.hide_render=variant=='bare';o.hide_set(variant=='bare')
    for o in connected:o.hide_render=variant=='bare';o.hide_set(variant=='bare')
    stem='01-bare-ports' if variant=='bare' else '02-qd3-translucent-tubes'
    scene.render.filepath=str(ROOT/f'tmp/M-{variant}-preview.png' if args.preview else OUT/f'{stem}.png')
    bpy.ops.render.render(write_still=True)
    if not args.preview:
        for screen in bpy.data.screens:
            for a in screen.areas:
                if a.type=='VIEW_3D':
                    a.spaces.active.overlay.show_overlays=False;a.spaces.active.clip_end=250;a.spaces.active.region_3d.view_perspective='CAMERA'
        bpy.ops.wm.save_as_mainfile(filepath=str(OUT/f'{stem}.blend'))
if not args.preview:
    (OUT/'render-notes.json').write_text(json.dumps({
        'revision':'M','source_scene':'../product-views/assembled-unmarked.blend',
        'geometry_changes':'No manifold changes; converted millimetres to metres. Small shader-only edge rounding.',
        'bare':'20 front and 4 side ports unpopulated; six M4 body screws retained.',
        'connected':'20 male/female QD approximations, 20 annular 10 mm ID / 13 mm OD tube tails; four side plugs fitted.',
        'materials':['Fine satin black POM','Directionally brushed stainless faceplate','Polished nickel-plated brass fitting references','A4 stainless fastener references','Translucent polymer tubing, IOR 1.46'],
        'lighting':'Four rectangular softboxes, low world illumination, tabletop contact shadows',
        'camera':'72 mm perspective, front three-quarter, deep focus',
        'render':'Cycles 256 samples, adaptive threshold 0.006, denoising, AgX Medium High Contrast',
        'resolution':[3000,1600],'surface_markings':False,
        'scope':'Physically based visual finish choices, not measured materials. QD3 female halves and compression ends are approximate envelopes; exact 10/13 female SKU has not been selected. Tubing is an open-ended visual sample, not a complete routed loop. Threads remain CAD pilot representations.'
    },indent=2)+'\n')
