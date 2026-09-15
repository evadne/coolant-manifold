"""Unmarked Q review views, with a separate diagnostic transparency file."""
import bpy,bmesh,json,sys,math,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from context_viewport import configure_context_viewports
OUT=ROOT/'output/long-bore-Q/product-views';OUT.mkdir(parents=True,exist_ok=True)
MESH=ROOT/'tmp/mesh-long-bore-Q'
report=json.loads((ROOT/'output/long-bore-Q/cad/verification.json').read_text())
for p,h in report['source_sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
source=ROOT/'output/long-bore-P/product-views/assembled-unmarked.blend'
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene
for o in list(scene.objects):
 if o.type not in ('LIGHT','CAMERA') and o.name not in ('faceplate',) and not o.name.startswith(('Front M4','G1-4 side plug reference')):
  bpy.data.objects.remove(o,do_unlink=True)
for o in scene.objects:o.hide_render=False;o.hide_set(False)
pom=bpy.data.materials['Unmarked black POM'];pom.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.32

def load(name,path,material):
 bpy.ops.wm.stl_import(filepath=str(path));o=bpy.context.object;o.name=name
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5)
 bmesh.ops.dissolve_limit(bm,angle_limit=1e-5,verts=list(bm.verts),edges=list(bm.edges),use_dissolve_boundaries=False)
 bm.to_mesh(o.data);bm.free();o.data.materials.clear();o.data.materials.append(material);return o
body=load('body',MESH/'body.stl',pom)
assert not any(o.type=='FONT' for o in scene.objects)
scene.render.resolution_x=1800;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
scene.cycles.samples=64;scene.cycles.use_denoising=True;scene.cycles.transparent_max_bounces=40
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
 prefs.compute_device_type='METAL';prefs.get_devices()
 for d in prefs.devices:d.use=d.type=='METAL'
 scene.cycles.device='GPU'
except TypeError:pass

def camera(name,loc,target,scale):
 bpy.ops.object.camera_add(location=loc);o=bpy.context.object;o.name=name;o.data.type='ORTHO';o.data.ortho_scale=scale;o.data.clip_end=5000;o.data.clip_start=1
 o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
rear=camera('Q rear three-quarter',(-265,580,290),(0,18,43.5),515)
straight=camera('Q rear elevation',(0,600,43.5),(0,40,43.5),490)
front=camera('Q front three-quarter',(270,-550,275),(0,15,43.5),545)

def render(name,cam):
 scene.camera=cam;scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
render('01-rear-assembled',rear)
render('02-rear-elevation',straight)
render('03-front-unchanged',front)
scene.camera=rear
configure_context_viewports(scene,target=(0,20,43.5),distance=650,clean=True)
for o in scene.objects:o.select_set(False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'assembled-unmarked.blend'),compress=True)
for o in scene.objects:
 if o.type=='MESH' and o!=body:o.hide_render=True;o.hide_set(True)
render('04-POM-rear',rear)
# 50/50 surface transparency is an inspection aid, not real POM optics.
trans=pom.copy();trans.name='Q POM inspection - 50 percent transparency';nt=trans.node_tree
transparent=nt.nodes.new('ShaderNodeBsdfTransparent');mix=nt.nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=.5
nt.links.new(nt.nodes['Principled BSDF'].outputs[0],mix.inputs[1]);nt.links.new(transparent.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],nt.nodes['Material Output'].inputs['Surface']);body.data.materials[0]=trans
for i,colour in enumerate(((.025,.35,.6,1),(.8,.19,.06,1)),1):
 mat=bpy.data.materials.new('Diagnostic gallery '+str(i));mat.diffuse_color=colour;mat.use_nodes=True
 mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=colour
 load('Diagnostic fluid volume '+str(i),MESH/f'fluid-network-{i}.stl',mat)
render('05-POM-transparent-channels',rear)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'body-50-percent-transparent.blend'),compress=True)
(OUT/'render-manifest.json').write_text(json.dumps({'revision':'Q','surface_markings':False,'views':['01-rear-assembled.png','02-rear-elevation.png','03-front-unchanged.png','04-POM-rear.png','05-POM-transparent-channels.png'],'rear_G1_4_ports':4,'diagnostic_transparency':.5,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,ROOT/'output/long-bore-Q/cad/body.step',ROOT/'scripts/render_revision_Q.py',ROOT/'output/long-bore-Q/cad/verification.json']},'scope':'Pilot-cylinder threads; transparent POM and coloured channel voids for inspection only; P remains selected baseline.'},indent=2)+'\n')
