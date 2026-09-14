"""Unmarked, assembled Option B product views from revision G CAD meshes.

Run after build_cad.py. Bought-in QD3 shapes and fasteners are visual references.
No text, identification bands, engraving, dimensions or overlays are generated.
"""
import json
import math
from pathlib import Path
import bpy
import bmesh
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/product-views'
OUT.mkdir(parents=True, exist_ok=True)
P = json.loads((ROOT/'cad/parameters.json').read_text())
S = json.loads((ROOT/'tmp/scene.json').read_text())
assert S['parameters']['revision'] == P['revision']
assert S['parameters']['mounting'] == 'faceplate'
for key in P:
    assert S['parameters'][key] == P[key], key
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = .001


def material(name, colour, metallic, roughness):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*colour, 1)
    m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*colour, 1)
    bs.inputs['Metallic'].default_value = metallic
    bs.inputs['Roughness'].default_value = roughness
    return m


pom = material('Unmarked black Delrin', (.018, .021, .024), 0, .32)
steel = material('Unmarked satin stainless', (.52, .55, .58), .85, .30)
nickel = material('QD3 nickel visual reference', (.60, .62, .64), .9, .25)
product = []
fittings = []


def finish(obj, mat, bevel=.1):
    obj.data.materials.append(mat)
    if bevel:
        b = obj.modifiers.new('Visual edge break', 'BEVEL')
        b.width = bevel
        b.segments = 3
        b.limit_method = 'ANGLE'
        b.angle_limit = .5
        b.harden_normals = True
    obj.modifiers.new('Weighted normals', 'WEIGHTED_NORMAL')
    product.append(obj)
    return obj


for name in ('body', 'faceplate', 'lid'):
    bpy.ops.wm.stl_import(filepath=str(ROOT/'tmp/mesh'/f'{name}.stl'))
    o = bpy.context.object
    o.name = name
    # Remove coplanar tessellation edges before shading broad machined faces.
    mesh = bmesh.new()
    mesh.from_mesh(o.data)
    bmesh.ops.remove_doubles(mesh, verts=list(mesh.verts), dist=1e-5)
    bmesh.ops.dissolve_limit(mesh, angle_limit=1e-5, verts=list(mesh.verts),
                             edges=list(mesh.edges), use_dissolve_boundaries=False)
    mesh.to_mesh(o.data)
    mesh.free()
    o.data.update()
    finish(o, pom if name == 'body' else steel, 0)
    # Preserve flat CAD surfaces without modifier-created triangulation seams.
    o.modifiers.clear()


def cylinder(name, x, y, z, radius, depth, vertices=96):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth,
                                      location=(x,y,z), rotation=(math.pi/2,0,0))
    obj = bpy.context.object
    obj.name = name
    return obj


# Eighteen manifold-side male QDs. No female halves or hoses obscure the product.
for z in P['port_rows_z']:
    for x in S['ports_x']:
        for name, start, end, radius, sides in (
            ('Seating shoulder',0,2,9.9,96), ('Hex body',2,10,12.7,6),
            ('Barrel',10,18,10.7,96), ('Male nose',18,32.1,8,96)):
            o = cylinder('QD3 reference / '+name, x,-P['port_boss_height']-(start+end)/2,z,
                         radius,end-start,sides)
            finish(o,nickel,.15)
            fittings.append(o)


# Actual recesses in the reference screw heads, rather than black drive markings.
heads = []
for rear, positions in ((False,S['faceplate_mounts']),(True,S['cover_bolts'])):
    spec = P['cover_fastener'] if rear else P['faceplate_fastener']
    outer = P['body_depth']+P['lid_thickness'] if rear else -P['faceplate_thickness']
    inward = -1 if rear else 1
    recess = (spec['countersink_diameter']-spec['head_diameter'])/2
    top = outer+inward*recess
    cone_depth = (spec['head_diameter']-spec['nominal_diameter'])/2
    for x,z in positions:
        bpy.ops.mesh.primitive_cone_add(vertices=64,radius1=spec['head_diameter']/2,
                                       radius2=spec['nominal_diameter']/2,depth=cone_depth,
                                       location=(x,top+inward*cone_depth/2,z),
                                       rotation=(-inward*math.pi/2,0,0))
        head=bpy.context.object
        head.name=('Rear' if rear else 'Front')+' M4 DIN 7991 socket head'
        cutter=cylinder('Temporary hex socket cutter',x,top+inward*.55,z,2.5/math.sqrt(3),1.3,6)
        bpy.context.view_layer.objects.active=head
        mod=head.modifiers.new('Recessed hex socket','BOOLEAN')
        mod.operation='DIFFERENCE'
        mod.object=cutter
        bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.data.objects.remove(cutter,do_unlink=True)
        finish(head,steel,.025)
        heads.append(head)

assert len(heads)==39 and len(fittings)==72
assert not any(o.type=='FONT' for o in scene.objects)
assert len([o for o in scene.objects if o.type=='MESH'])==114

world=bpy.data.worlds.new('Neutral studio')
scene.world=world
world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.5,.5,.5,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.65


def area(name, pos, power, size):
    bpy.ops.object.light_add(type='AREA',location=pos)
    obj=bpy.context.object
    obj.name=name
    obj.data.energy=power
    obj.data.shape='DISK'
    obj.data.size=size
    obj.rotation_euler=(Vector((0,0,43.5))-obj.location).to_track_quat('-Z','Y').to_euler()


area('Front softbox',(40,-320,440),4500000,430)
area('Rear softbox',(-80,280,370),4500000,380)
area('Left softbox',(-380,-40,80),2200000,280)
area('Underside fill',(120,40,-300),1800000,300)
scene.render.engine='CYCLES'
scene.cycles.samples=40
scene.cycles.use_denoising=True
scene.render.resolution_x=1800
scene.render.resolution_y=1100
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.image_settings.color_mode='RGB'
scene.view_settings.view_transform='AgX'
# Neutral, unlabelled background; camera rays see a separate studio backdrop.
scene.render.film_transparent=False
wn=world.node_tree.nodes
camera_background=wn.new('ShaderNodeBackground')
camera_background.inputs['Color'].default_value=(.84,.86,.88,1)
camera_background.inputs['Strength'].default_value=1
light_path=wn.new('ShaderNodeLightPath')
mix=wn.new('ShaderNodeMixShader')
world.node_tree.links.new(light_path.outputs['Is Camera Ray'],mix.inputs[0])
world.node_tree.links.new(wn['Background'].outputs[0],mix.inputs[1])
world.node_tree.links.new(camera_background.outputs[0],mix.inputs[2])
world.node_tree.links.new(mix.outputs[0],wn['World Output'].inputs['Surface'])

views=[
    ('01-front-three-quarter',(280,-540,300),(0,0,43.5)),
    ('02-rear-three-quarter',(-270,510,285),(0,5,43.5)),
    ('03-front',(0,-600,43.5),(0,0,43.5)),
    ('04-rear',(0,600,43.5),(0,0,43.5)),
    ('05-left',(-600,0,43.5),(0,0,43.5)),
    ('06-right',(600,0,43.5),(0,0,43.5)),
    ('07-top',(0,0,650),(0,0,43.5)),
    ('08-bottom',(0,0,-600),(0,0,43.5)),
]
# Orthographic cameras fit the exact product bounds with consistent margins.
bpy.context.view_layer.update()
points=[o.matrix_world@Vector(v) for o in product for v in o.bound_box]
report=[]
for name,location,target in views:
    bpy.ops.object.camera_add(location=location)
    camera=bpy.context.object
    camera.name=name
    camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.type='ORTHO'
    camera.data.clip_end=5000
    bpy.context.view_layer.update()
    inv=camera.matrix_world.inverted()
    local=[inv@v for v in points]
    xmin,xmax=min(v.x for v in local),max(v.x for v in local)
    ymin,ymax=min(v.y for v in local),max(v.y for v in local)
    camera.location+=camera.rotation_euler.to_matrix()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0))
    aspect=scene.render.resolution_x/scene.render.resolution_y
    camera.data.ortho_scale=max(xmax-xmin,(ymax-ymin)*aspect)*1.16
    scene.camera=camera
    scene.render.filepath=str(OUT/f'{name}.png')
    report.append({'view':name,'orthographic_scale_mm':camera.data.ortho_scale,'path':f'{name}.png'})

# Save a complete, editable unmarked assembly with all eight named cameras.
scene.camera=bpy.data.objects[views[0][0]]
for screen in bpy.data.screens:
    for a in screen.areas:
        if a.type=='VIEW_3D':
            a.spaces.active.overlay.show_overlays=False
            a.spaces.active.clip_end=10000
            a.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'assembled-unmarked.blend'))
for item in report:
    scene.camera=bpy.data.objects[item['view']]
    scene.render.filepath=str(OUT/item['path'])
    bpy.ops.render.render(write_still=True)
(OUT/'render-manifest.json').write_text(json.dumps({
    'revision':P['revision'],'mounting':'selected Option B',
    'surface_markings':False,'plate_to_POM_screw_heads_M4':len(heads),
    'QD3_male_references':18,'notes':'QD3 shapes and screws are visual references; CAD-derived POM and steel. No tubing, labels or markings.',
    'views':report},indent=2)+'\n')
print('Completed eight unmarked product views and editable Blender assembly.')
