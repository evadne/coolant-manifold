"""StarTech 25U open-frame use-case study. Current Q manifold and R7 plate; bought-in context envelopes noted."""
from pathlib import Path
import bpy, math, json, hashlib, argparse, sys
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from context_viewport import configure_context_viewports
from context_startech25 import build_rack, RACK_U_DATUM, RAIL_DEPTH
from context_tubing import Route, branch_route, make_tube, assess_routes
from check_context_fit import check_scene
from check_context_gpu import check_gpus
from context_gpu5090 import build_gpu, GPU, PORT_Z, P as GPU_PLACEMENT
import numpy as np
OUT=ROOT/'output/context-25U';OUT.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');parser.add_argument('--check-only',action='store_true');parser.add_argument('--device',choices=['CPU','METAL'],default='CPU')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'output/long-bore-Q/product-views/assembled-unmarked.blend'))
scene=bpy.context.scene
for o in list(scene.objects):
    if not (o.name in ('body','faceplate') or o.name.startswith(('Front M4','G1-4 side plug reference'))):
        bpy.data.objects.remove(o,do_unlink=True)
U=44.45; bottom=RACK_U_DATUM+U; manifold=bottom+14*U+.95; host=bottom+10*U+.9; gpu=bottom+16*U+24
rad_z=bottom+5*U
for o in scene.objects:
    o.location.z+=manifold
    if o.name.startswith('G1-4 side plug') and o.location.x<0:
        bpy.data.objects.remove(o,do_unlink=True)

def mat(name,c,metal=0,rough=.4):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    return m
rack=mat('Charcoal open-frame rack',(.035,.045,.055),.5)
steel=mat('Satin silver metal',(.50,.54,.57),.75)
pcb=mat('Dark green PCB',(.025,.09,.065))
block=mat('Chrome plated copper GPU block',(.57,.61,.65),.92,.22)
carbon=mat('Matt carbon composite GPU covers',(.022,.025,.028),.15,.4)
gold=mat('PCIe gold contacts',(.58,.36,.09),.8,.25)
gpu_pcb=mat('Black soldermask RTX 5090 PCB',(.014,.018,.017),0,.48)
black=mat('Black connectors and sleeving',(.01,.013,.018))
supply=mat('Coolant supply illustration',(.06,.27,.39),.1,.28)
ret=mat('Coolant return illustration',(.40,.16,.08),.1,.28)
data=mat('PCIe cable illustration',(.22,.15,.32),0,.5)

def box(name,loc,size,m):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.clear();o.data.materials.append(m)
    return o

def cyl(name,loc,r,depth,m,axis='Y'):
    rot=(math.pi/2,0,0) if axis=='Y' else ((0,math.pi/2,0) if axis=='X' else (0,0,0))
    bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=depth,location=loc,rotation=rot)
    o=bpy.context.object;o.name=name;o.data.materials.append(m);return o

def hose(name,pts,m,r=6.5):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=16;cu.bevel_depth=r;cu.bevel_resolution=3
    sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
    for b,p in zip(sp.bezier_points,pts):b.co=p;b.handle_left_type='AUTO';b.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,cu);scene.collection.objects.link(o);o.data.materials.append(m);return o
# Flat rear ports are unused in this accepted routing; close each with a plug envelope.
for x in (-180,180):
    for z in (23.5,63.5):
        cyl(f'G1-4 rear plug reference {x} {z}',(x,42,manifold+z),10,4,steel)
build_rack(box,cyl,rack,steel,black)
pvc=mat('Transparent PVC wall',(.94,.975,1),0,.1)
pvc.node_tree.nodes.get('Principled BSDF').inputs['Transmission Weight'].default_value=1
pvc.node_tree.nodes.get('Principled BSDF').inputs['IOR'].default_value=1.54
fluid=mat('Clear inhibited coolant',(.87,.95,.98),0,.08)
fluid.node_tree.nodes.get('Principled BSDF').inputs['Transmission Weight'].default_value=1
fluid.node_tree.nodes.get('Principled BSDF').inputs['IOR'].default_value=1.333
relaxed=json.loads((OUT/'relaxed-branches.json').read_text())
relaxation_report=json.loads((OUT/'pvc-equilibrium.json').read_text())
for path,expected in relaxation_report['source_sha256'].items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected, 'Re-run scripts/relax_context_tubes.py: '+path
routes={}
def pvc_tube(name,points,od=13,floor=50):
    points=np.asarray(points)
    if name in relaxed:
        digest=hashlib.sha256(np.round(points,7).astype('<f8').tobytes()).hexdigest()
        assert digest==relaxed[name]['nominal_sha256'], 'Stale equilibrium route: '+name
        points=np.asarray(relaxed[name]['points'])
        if name.startswith('Host '):floor=relaxation_report['parameters']['minimum_host_bend_radius_mm']
    routes[name]=dict(points=points,od=od,floor=floor)
    return make_tube(scene,name,points,pvc,fluid,od=od)
# Official supplier fitting meshes; retain the operator-accepted studio registration.
fit_dir=ROOT/'output/long-bore-P/koolance-fit'
fit=json.loads((fit_dir/'verification.json').read_text());templates={}
for rec in fit['mesh_records']:
    bpy.ops.wm.stl_import(filepath=str(fit_dir/rec['mesh']));o=bpy.context.object
    o.data.materials.append(steel)
    for face in o.data.polygons:face.use_smooth=True
    o.data.set_sharp_from_angle(angle=math.radians(35))
    templates[(rec['part'],rec['solid_index'])]=o.data
    bpy.data.objects.remove(o,do_unlink=True)
for i in range(10):
    for row,z in enumerate((23.5,63.5)):
        for (part,solid),mesh in templates.items():
            male=part=='qd3-mtg4'
            if i==9 and not male:continue
            o=bpy.data.objects.new(f'Koolance {part} / pair {i+1} row {row+1} solid {solid}',mesh)
            scene.collection.objects.link(o)
            o.location=(-180+40*i,-3+(0 if male else fit['female_mouth_Y_relative_to_male_sealing_face_mm']),manifold+z)
qd_tail_y=-3-fit['inferred_seat_to_female_tail_mm']
for x in (-232.55,232.55):
    for dz in (5.4,81.6):
        cyl('Manifold rack screw reference',(x,-5,manifold+dz),5,6,steel)
        box('Manifold M6 cage-nut envelope',(math.copysign(232.5,x),8.5,manifold+dz),(13,12,13),steel)
# 4U host envelope: 440 W x456 D x176 H. I/O and PCI brackets face the viewer.
box('RM46-502-I host envelope',(0,228,host+88),(440,456,176),rack)
box('Front-facing motherboard IO',( -110,-2,host+47),(150,5,43),steel)
for i in range(6):box('IO socket',(-165+i*23,-6,host+47),(14,5,16),black)
for i in range(8):box('Front PCI slot bracket',(36+i*20,-3,host+72),(18,5,118),steel)
for x in (-232.55,232.55):
    box('Host rack ear',(x,-3,host+88),(25,5,176),rack)
    box('Host handle',(x,-27,host+88),(9,16,100),steel)
for x in (-222,222):box('Host four-post support rail',(x,RAIL_DEPTH/2,host+10),(10,RAIL_DEPTH,16),steel)
# Host branch pair nine terminates at a two-port PCI bracket on the rack-facing end.
for z in (host+42,host+82):
    cyl('PCI bracket G1-4 feedthrough',(136,-11,z),10,18,steel)
    cyl('Host 10-13 compression envelope',(136,-27,z),10,14,steel)
box('Host MCIO pair bracket',(176,-7,host+70),(16,8,80),steel)
box('PCIe x16 to dual MCIO host adapter PCB',(176,48,host+70),(2,95,65),pcb)
for j in range(2):box('Host MCIO 8i socket '+str(j+1),(176,-13,host+62+j*27),(13,12,16),black)
# 6U open GPU shelf; dimensioned 1.5-slot 5090 FE assemblies at 40 mm pitch.
box('GPU tray',(0,211,gpu-18),(440,420,3),steel)
for x in (-215,215):box('GPU tray side support',(x,211,gpu-4),(10,420,28),rack)
# Raised crossbars locate the shorter water-cooled cards at the accepted port mid-height.
for y in (155,230):
    box('GPU mechanical retention crossbar',(0,y,gpu+42),(410,8,8),rack)
    for x in (-201,201):box('GPU crossbar standoff',(x,y,gpu+10.75),(8,8,54.5),steel)
gpu_records=[]
for i,x in enumerate([-180+40*i for i in range(8)]):
    gpu_records.append(build_gpu(i,x,gpu,box,cyl,hose,(block,carbon,gpu_pcb,black,steel,gold)))
    for j,dz in enumerate(PORT_Z):
        source_z=manifold+(23.5 if j==0 else 63.5)
        pvc_tube(f'GPU {i+1} parallel coolant '+str(j),branch_route(x,qd_tail_y+1,source_z,x,9,gpu+dz,x+(-10 if j==0 else 10)))
box('GPU auxiliary power distribution enclosure',(195,112,gpu+20),(32,48,45),black)
for x in (-220,220):box('GPU tray four-post support',(x,RAIL_DEPTH/2,gpu-25),(10,RAIL_DEPTH,16),steel)
# A switch-board envelope beside the eight cards: requested topology, SKU provisional.
box('Conceptual eight-endpoint PCIe switch PCB',(164,260,gpu+14),(110,150,2),pcb)
box('Switch heatsink',(164,260,gpu+26),(42,48,22),black)
for i in range(8):box('Switch downstream connector',(117+i*13,329,gpu+20),(10,15,10),steel)
for i in range(2):box('Switch host MCIO connector',(155+i*20,187,gpu+20),(16,15,10),steel)
for j in range(2):
    hose('Host uplink MCIO 8i cable '+str(j+1),[(176,-20,host+62+j*27),(207+j*16,-65-j*12,host+145),(210+j*16,-75-j*12,gpu+35),(191+j*16,145,gpu+40),(155+j*20,180,gpu+20)],data,3.5)
assert len([o for o in scene.objects if o.name.startswith('Host uplink MCIO 8i cable')])==2
# Pair nine cools host; pair ten remains spare with disconnected male QDs.
for j,z in enumerate((host+42,host+82)):
    pvc_tube('Host coolant branch '+str(j),branch_route(140,qd_tail_y+1,manifold+(23.5 if j==0 else 63.5),136,-33,z,128 if j==0 else 152,depth=-270))
# Append the existing R7 CAD/fan assembly from its native mm Blender scene.
# Even the plate-only file retains the other components, hidden for its own view.
rad_source=ROOT/'output/radiator-R7/radiator-rack-plate-R7.blend'
with bpy.data.libraries.load(str(rad_source),link=False) as (src,dst):
    dst.objects=[name for name in src.objects if name!='Studio ground']
rad_objects=[]
for o in dst.objects:
    if o is None:continue
    if o.type!='MESH':bpy.data.objects.remove(o,do_unlink=True);continue
    # Ports point down to use pedestal space below U1 instead of the host above.
    if o.name.startswith('Top G1-4 plug reference'):
        bpy.data.objects.remove(o,do_unlink=True);continue
    scene.collection.objects.link(o);o.location.z+=bottom
    o.hide_render=False;o.hide_set(False);rad_objects.append(o)
assert sum(o.name.startswith('NF-A20 reference fan-00') for o in rad_objects)==8
rad_plate=next(o for o in rad_objects if o.name.startswith('R7 rack plate'))
rad_params=json.loads((ROOT/'cad/radiator/R7.json').read_text())
for x in rad_params['rack_mount_x']:
    for i in (0,6,13,19):
        cyl('R7 populated rack screw',(x,-5,bottom+rad_params['rack_mount_y'][i]),5,6,steel)
        box('R7 M6 cage-nut envelope',(math.copysign(232.5,x),8.5,bottom+rad_params['rack_mount_y'][i]),(13,12,13),steel)
# The stock radiator/frame/fan geometry is an integration envelope; the R7 plate
# is CAD-derived. Rotate the symmetrical radiator port arrangement to the bottom.
port_z=bottom+(rad_params['height']-rad_params['radiator_height'])/2
for x in (-140.5,140.5):
    cyl('SuperNova bottom port elbow stem',(x,22.5,port_z-7),9,14,steel,'Z')
    box('SuperNova bottom port elbow',(x,22.5,port_z-18),(18,18,18),steel)
    cyl('SuperNova bottom hose compression',(x,39,port_z-18),11,16,steel)
# ULTITUBE/D5 NEXT context envelope, independently supported behind the fans.
# Glass dimensions follow the retained 200 mm / OD65 / wall5 reference. Pump,
# caps, clamps and support are provisional envelopes, not manufacture-ready CAD.
pump_x=0.;pump_y=285.;glass_bottom=bottom+150;glass_top=glass_bottom+200
for x in (-220,220):box('Provisional pump shelf depth support',(x,RAIL_DEPTH/2,bottom+55),(10,RAIL_DEPTH,12),steel)
box('Provisional pump shelf crossmember',(0,pump_y+55,bottom+54.5),(440,30,10),steel)
box('Provisional separate pump shelf',(0,pump_y+25,bottom+61),(110,120,3),steel)
box('Provisional pump mount',(pump_x,pump_y,bottom+81),(90,90,35),black)
cyl('D5 NEXT pump envelope',(pump_x,pump_y,bottom+110),32,50,rack,'Z')
box('D5 NEXT display envelope',(pump_x,pump_y+32,bottom+106),(45,10,30),black)
cyl('ULTITUBE bottom cap envelope',(pump_x,pump_y,glass_bottom-10),36,20,black,'Z')
cyl('ULTITUBE top cap envelope',(pump_x,pump_y,glass_top+8),36,16,black,'Z')
glass=mat('Borosilicate glass context',(.90,.97,1),0,.1)
glass.node_tree.nodes.get('Principled BSDF').inputs['Transmission Weight'].default_value=1
glass.node_tree.nodes.get('Principled BSDF').inputs['IOR'].default_value=1.47
# Annular glass mesh avoids an opaque solid-cylinder shortcut.
verts=[];N=64
for zz,rr in ((glass_bottom,32.5),(glass_top,32.5),(glass_bottom,27.5),(glass_top,27.5)):
    verts.extend([(pump_x+rr*math.cos(2*math.pi*i/N),pump_y+rr*math.sin(2*math.pi*i/N),zz) for i in range(N)])
faces=[]
for i in range(N):
    j=(i+1)%N;faces.extend([(i,j,N+j,N+i),(2*N+j,2*N+i,3*N+i,3*N+j),(j,i,2*N+i,2*N+j),(N+i,N+j,3*N+j,3*N+i)])
mesh=bpy.data.meshes.new('ULTITUBE nominal glass');mesh.from_pydata(verts,[],faces);mesh.update()
o=bpy.data.objects.new('ULTITUBE 200 glass envelope',mesh);scene.collection.objects.link(o);o.data.materials.append(glass)
for face in mesh.polygons:face.use_smooth=face.index%4<2
cyl('Reservoir coolant illustration',(pump_x,pump_y,glass_bottom+80),27.2,160,supply,'Z')
cyl('Reservoir fill plug',(pump_x,pump_y,glass_top+19),9,6,steel,'Z')
for x in (-40,40):box('Provisional reservoir rear support',(x,pump_y+46,bottom+209),(8,4,278),steel)
for zz in (glass_bottom+18,glass_top-18):
    box('Provisional reservoir clamp link',(0,pump_y+33,zz),(24,27,8),black)
    box('Provisional reservoir support bridge',(0,pump_y+46,zz),(88,4,8),steel)
    bpy.ops.mesh.primitive_torus_add(major_radius=34,minor_radius=3,major_segments=64,minor_segments=8,location=(pump_x,pump_y,zz))
    bpy.context.object.name='Provisional reservoir clamp';bpy.context.object.data.materials.append(black)
# Complete cooling plumbing: return -> radiator -> reservoir -> pump -> supply.
# Side elbows direct the infrastructure rearwards; hoses use the free side aisle.
for j,z in enumerate((manifold+23.5,manifold+63.5)):
    cyl('Left infrastructure G1-4 fitting',(-213.8,20,z),9,17.6,steel,'X')
    box('Left infrastructure rotary elbow',(-222.8,20,z),(18,18,18),steel)
    cyl('Left infrastructure compression',(-222.8,38,z),11,18,steel)
    if j==0:
        p=Route((-222.8,47,z)).line((-222.8,77,z)).shift((-265,217,z))
        p.line((-265,220,z)).bend((0,1,0),(0,0,-1),65)
        p.line((-265,pump_y,bottom+110+65)).bend((0,0,-1),(1,0,0),65)
        p.line((-51,pump_y,bottom+110))
    else:
        p=Route((-222.8,47,z)).line((-222.8,77,z)).shift((-280,257,z))
        p.line((-280,370,z)).bend((0,1,0),(0,0,-1),65)
        p.line((-280,435,port_z-18+65)).bend((0,0,-1),(1,0,0),65)
        p.line((-205.5,435,port_z-18)).bend((1,0,0),(0,-1,0),65)
        p.line((-140.5,47,port_z-18))
    pvc_tube('Cooling infrastructure '+('supply' if j==0 else 'return'),p.array(),16,60)
p=Route((140.5,47,port_z-18)).line((140.5,pump_y-65,port_z-18)).bend((0,1,0),(0,0,1),65)
p.line((140.5,pump_y,glass_bottom-10-65)).bend((0,0,1),(-1,0,0),65).line((55,pump_y,glass_bottom-10))
pvc_tube('Radiator to reservoir',p.array(),16,60)
cyl('Pump outlet reference',(-42,pump_y,bottom+110),11,20,steel,'X')
cyl('Reservoir inlet reference',(46,pump_y,glass_bottom-10),11,20,steel,'X')
assert len([o for o in scene.objects if o.name.startswith('Koolance qd3-mtg4 /')])==40
assert len([o for o in scene.objects if o.name.startswith('Koolance qd3-ft10x13 /')])==54
assert len([o for o in scene.objects if o.name.startswith('Front M4')])==12
assert not any('MO-RA' in o.name for o in scene.objects)
assert len([o for o in scene.objects if 'main chrome cooling block' in o.name])==8
assert len([o for o in scene.objects if o.name.startswith('GPU ') and 'parallel coolant' in o.name])==16
assert len([o for o in scene.objects if o.name.startswith('GPU ') and '12V-2x6 socket' in o.name])==8
assert len([o for o in scene.objects if o.name.startswith('GPU ') and 'IO bracket top flange' in o.name])==8
assert not any(o.type=='FONT' for o in scene.objects)
# Validate the same sampled centrelines used to build the rendered annular meshes.
gpu_report=check_gpus(scene,gpu_records)
(OUT/'gpu-verification.json').write_text(json.dumps(gpu_report,indent=2)+'\n')
tube_report=assess_routes(routes)
(OUT/'tube-verification.json').write_text(json.dumps(tube_report,indent=2)+'\n')
(OUT/'tube-centrelines.json').write_text(json.dumps({name:{'points':r['points'].tolist(),'od':r['od']} for name,r in routes.items()})+'\n')
print('Minimum conservative tube surface gap:',tube_report['minimum_conservative_tube_gap_mm'])
assert tube_report['minimum_conservative_tube_gap_mm']>0,tube_report['closest_pairs'][:3]

scene_report=check_scene(scene,routes)
(OUT/'scene-verification.json').write_text(json.dumps(scene_report,indent=2)+'\n')
print('Tube/equipment intersections:',scene_report['tube_equipment_intersections'])
assert not scene_report['tube_equipment_intersections']
# Broad studio lighting and deterministic review cameras.
world=bpy.data.worlds.new('White studio');world.use_nodes=True;scene.world=world
world.node_tree.nodes['Background'].inputs[0].default_value=(.85,.88,.92,1);world.node_tree.nodes['Background'].inputs[1].default_value=.8
for loc,power,size in [((0,-1100,2200),50000000,1400),((1000,600,1900),40000000,1200),((-1200,100,1400),25000000,1000)]:
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,200,650))-o.location).to_track_quat('-Z','Y').to_euler()
scene.render.engine='CYCLES';scene.cycles.samples=16 if args.preview else 64;scene.cycles.use_denoising=True
if args.device=='METAL':
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
    assert any(d.type=='METAL' for d in prefs.devices)
    for d in prefs.devices:d.use=d.type=='METAL'
    scene.cycles.device='GPU'
scene.cycles.transmission_bounces=12;scene.cycles.max_bounces=16
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.view_settings.view_transform='AgX'
scene.render.resolution_x=1700;scene.render.resolution_y=2000;scene.render.resolution_percentage=50 if args.preview else 100
for name,loc,target,scale in [('01-rack-context',(1500,-2450,1630),(0,220,660),1700),('02-front-layout',(0,-2600,660),(0,0,660),1480),('04-rear-cooling-assembly',(1800,2100,1250),(0,220,660),1700),('05-pump-reservoir-detail',(-350,1350,700),(0,285,rad_z),750),('06-front-tube-routing',(1050,-1700,1100),(0,-65,manifold+40),790),('07-side-tube-routing',(1350,-350,1000),(0,-110,manifold+35),740),('08-front-tube-detail',(0,-2000,manifold+35),(0,0,manifold+35),620),('09-GPU-block-detail',(-150,-800,gpu+350),(-40,130,gpu+130),550),('10-GPU-power-detail',(-225,-100,gpu+295),(-172,67,gpu+183),100)]:
    bpy.ops.object.camera_add(location=loc);o=bpy.context.object;o.name=name;o.data.type='ORTHO';o.data.ortho_scale=scale;o.data.clip_end=10000;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();scene.camera=o
    scene.render.filepath=str(ROOT/f'tmp/context25-{name}.png' if args.preview else OUT/f'{name}.png')
    if not args.check_only:bpy.ops.render.render(write_still=True)
    if args.preview:break
scene.camera=bpy.data.objects['01-rack-context']
if not args.preview:
    for o in scene.objects:o.select_set(False)
    configure_context_viewports(scene, target=(0,220,660), distance=1800, clean=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'25U-StarTech-context.blend'),compress=True)
    def digest(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
    report=dict(rack_U=25,rack_model='StarTech 4POSTRACK25U',rack_depth_overall_mm=661.8,rail_spacing_depth_mm=RAIL_DEPTH,rack_width_mm=600,rack_height_casters_mm=1288.34,rack_U_datum_mm=RACK_U_DATUM,depth_setting='22in / 0 and 0',
      manifold_revision='Q',manifold_body_issue='Q-M04',manifold_faceplate_issue='Q-M03',radiator_plate_revision='R7',outer_corner_radius_mm=5,
      rack_units_bottom_to_top=[dict(U='1',use='Radiator bottom fitting and plumbing clearance'),dict(U='2-11',use='SuperNova 1260 / R7 plate, eight NF-A20 fans; provisional pump/reservoir behind'),dict(U='12-15',use='4U host with front PCIe coolant bracket'),dict(U='16-17',use='Q parallel manifold'),dict(U='18-23',use='Eight RTX 5090 FE / Alphacool 5100182 assemblies and conceptual PCIe switch'),dict(U='24-25',use='Service space')],
      radiator=dict(plate_dimensions_mm=[482.6,444.5,2],body_envelope_mm=[422,48,441],fans=8,fan_model='Official Noctua NF-A20 integration meshes',port_orientation='Downwards into reserved U1; radiator begins at U2',rack_screws_populated=8,cable_notch_mm=[10,2],plate_aperture_radius_mm=50),
      pump_reservoir=dict(selection='Provisional ULTITUBE 200 / D5 NEXT envelopes',glass_length_mm=200,glass_od_mm=65,glass_wall_mm=5,position_xy_mm=[pump_x,pump_y],mounting='Illustrative independent rack shelf/support behind rear fans; not an engineered bracket or final product selection',reason='Eight A20s occupy both fan banks. Do not invent a 140 mm adapter interface on the retained 200 mm fan plate.'),
      front_pair_allocation={'1-8':'Individual GPUs','9':'Host CPU/chassis','10':'Spare male QDs'},
      fittings=dict(male='QD3-MTG4',female='QD3-FT10X13',connected_pairs=9,spare_pairs=1,rear_ports=4,rear_ports_state='Four reference face-sealing plugs; existing side-fed routing retained',source_scale='Unscaled supplier meshes in mm',axial_placement='Operator-accepted inferred studio pose'),
      pvc_equilibrium=dict(report='pvc-equilibrium.json',modulus_MPa=relaxation_report['parameters']['young_modulus_MPa'],method=relaxation_report['parameters']['model']),
      gpu_pitch_mm=40,gpu_reference=GPU,gpu_registration=gpu_records,gpu_orientation='Viewed from ports, main block left, processor PCB right, active backplate further right. Bracket rear; angled 12V-2x6 at top-front cutout',host_envelope_mm=[440,456,176],host_link=dict(adapter='x16 to 2x MCIO 8i',physical_cables=2,logical_link='one x16'),switch_status='Eight-endpoint concept; exact board not selected',
      source_sha256={path:digest(path) for path in ['output/manufacturing/Q-M04/RM10-Q-M04-BODY.step','output/manufacturing/Q-M03/RM10-Q-M03-FACEPLATE.step','output/radiator-R7/rack-plate-R7.step','output/long-bore-P/koolance-fit/verification.json','output/long-bore-Q/product-views/assembled-unmarked.blend','output/radiator-R7/radiator-rack-plate-R7.blend','docs/references/startech-25u/dimensions.pdf','docs/references/startech-25u/sources.json','scripts/context_startech25.py','scripts/context_tubing.py','scripts/check_context_fit.py','scripts/check_context_gpu.py','scripts/render_context_25u.py','scripts/relax_context_tubes.py','cad/context/pvc-routing.json','scripts/context_gpu5090.py','cad/context/gpu-5090fe.json','docs/references/alphacool-5090/datasheet.pdf','docs/references/alphacool-5090/manual.pdf','docs/references/alphacool-5090/power-housing.pdf','docs/references/alphacool-5090/power-header.pdf','output/context-25U/relaxed-branches.json']},
      view_files=['01-rack-context.png','02-front-layout.png','04-rear-cooling-assembly.png','05-pump-reservoir-detail.png','06-front-tube-routing.png','07-side-tube-routing.png','08-front-tube-detail.png','09-GPU-block-detail.png','10-GPU-power-detail.png'],
      scope='Current custom parts with manufacturer-dimensioned StarTech rack envelope and inferred section registration; chassis, GPU, pump and support remain illustrative. Not a complete fit, load, heat-rejection or electrical qualification. Routing colours are aids, not product surface markings.')
    (OUT/'layout.json').write_text(json.dumps(report,indent=2)+'\n')

