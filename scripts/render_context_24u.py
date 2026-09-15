"""24U open-frame use-case study. Exact O-M02 manifold; contextual envelopes only."""
from pathlib import Path
import bpy, math, json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/context-24U';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'output/manufacturing/O-M02/product-views/assembled-unmarked.blend'))
scene=bpy.context.scene
for o in list(scene.objects):
    if not (o.name in ('body','faceplate') or o.name.startswith(('QD3 reference /','Front M4 DIN 7991','G1-4 side plug reference'))):
        bpy.data.objects.remove(o,do_unlink=True)
U=44.45; bottom=100.; manifold=bottom+12*U+.95; host=bottom+8*U+.9; gpu=bottom+14*U+24
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
block=mat('Nickel GPU waterblock',(.43,.48,.51),.7)
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
# Four posts, 600 mm overall depth. Rail planes at 0 and 500 mm.
for x in (-253,253):
    for y in (0,500):
        box('24U structural post',(x,y,bottom+12*U),(28,28,24*U+30),rack)
    for z in (75,bottom+24*U+20):
        box('Rack depth beam',(x,250,z),(35,600,35),rack)
    for y in (-20,520):cyl('Levelling foot',(x,y,35),23,22,black,'Z')
for y in (-20,520):
    for z in (75,bottom+24*U+20):box('Rack width beam',(0,y,z),(540,35,35),rack)
# Rails have actual repeated square apertures, built from rectangular strips.
for sign in (-1,1):
    xc=sign*232.55
    for y in (0,500):
        box('Rail outer strip',(xc+sign*10,y+2,bottom+12*U),(11,3,24*U),rack)
        box('Rail inner strip',(xc-sign*9,y+2,bottom+12*U),(9,3,24*U),rack)
        zs=[bottom+u*U+d for u in range(24) for d in (6.35,22.225,38.1)]
        last=bottom
        for z in zs+[bottom+24*U+4.5]:
            length=z-4.5-last
            if length>0:box('Rail aperture web',(xc,y+2,last+length/2),(10,3,length),rack)
            last=z+4.5
# Connected female QD3 envelopes on nine branch pairs; pair ten stays available.
for x in [-180+40*i for i in range(9)]:
    for z in (manifold+23.5,manifold+63.5):
        cyl('Female QD pull ring',(x,-25,z),11.85,8,steel)
        cyl('Female QD receiver',(x,-38,z),10.7,18,steel)
        cyl('10-13 tube collar',(x,-57,z),10.6,16,steel)
# 4U host envelope: 440 W x456 D x176 H. I/O and PCI brackets face the viewer.
box('RM46-502-I host envelope',(0,228,host+88),(440,456,176),rack)
box('Front-facing motherboard IO',( -110,-2,host+47),(150,5,43),steel)
for i in range(6):box('IO socket',(-165+i*23,-6,host+47),(14,5,16),black)
for i in range(8):box('Front PCI slot bracket',(36+i*20,-3,host+72),(18,5,118),steel)
for x in (-232.55,232.55):
    box('Host rack ear',(x,-3,host+88),(25,5,176),rack)
    box('Host handle',(x,-27,host+88),(9,16,100),steel)
for x in (-222,222):box('Host four-post support rail',(x,250,host+10),(10,500,16),steel)
# Host branch pair nine terminates at a two-port PCI bracket on the rack-facing end.
for z in (host+42,host+82):cyl('PCI bracket G1-4 feedthrough',(136,-11,z),10,18,steel)
box('Host MCIO pair bracket',(176,-7,host+70),(16,8,80),black)
# 6U open GPU shelf. Cards are single-slot THICK, but separated at 40 mm for service.
box('GPU tray',(0,211,gpu-18),(440,420,3),steel)
for x in (-215,215):box('GPU tray side support',(x,211,gpu-4),(10,420,28),rack)
for y in (55,345):box('GPU mechanical retention crossbar',(0,y,gpu-1),(420,15,15),rack)
for i,x in enumerate([-180+40*i for i in range(8)]):
    box(f'GPU {i+1} single-slot waterblock',(x,190,gpu+77),(17,270,132),block)
    box(f'GPU {i+1} PCB',(x-9.5,190,gpu+77),(2,274,133),pcb)
    box(f'GPU {i+1} PCIe riser',(x,190,gpu+6),(20,112,12),black)
    box(f'GPU {i+1} water terminal',(x,42,gpu+104),(20,26,53),black)
    for j,z in enumerate((gpu+89,gpu+119)):
        cyl(f'GPU {i+1} coolant fitting',(x,20,z),8,22,steel)
        source_z=manifold+(23.5 if j==0 else 63.5)
        hose(f'GPU {i+1} parallel coolant '+str(j),[(x,-65,source_z),(x,-100-j*34,source_z+25),(x,-100-j*34,z-20),(x,-15,z),(x,9,z)],supply if j==0 else ret)
    # Explicit powered riser and auxiliary feed, with restrained rear routing.
    hose(f'GPU {i+1} riser data',[(x,240,gpu+4),(x,370,gpu-2),(117+i*13,360,gpu+10),(117+i*13,337,gpu+20)],data,3)
    hose(f'GPU {i+1} auxiliary power',[(x,310,gpu+123),(x,385,gpu+130),(195,395,gpu+100)],black,4)
box('GPU auxiliary power distribution enclosure',(195,395,gpu+90),(32,30,45),black)
for x in (-220,220):box('GPU tray four-post support',(x,250,gpu-25),(10,500,16),steel)
# A switch-board envelope beside the eight cards: requested topology, SKU provisional.
box('Conceptual eight-endpoint PCIe switch PCB',(164,260,gpu+14),(110,150,2),pcb)
box('Switch heatsink',(164,260,gpu+26),(42,48,22),black)
for i in range(8):box('Switch downstream connector',(117+i*13,329,gpu+20),(10,15,10),steel)
for i in range(2):box('Switch host MCIO connector',(155+i*20,187,gpu+20),(16,15,10),steel)
hose('Logical PCIe x16 host uplink',[(176,-16,host+115),(210,-65,host+145),(218,-75,gpu+35),(200,160,gpu+40),(164,180,gpu+20)],data,5)
# Pair nine cools host; pair ten remains spare with disconnected male QDs.
for j,z in enumerate((host+42,host+82)):
    hose('Host coolant branch '+str(j),[(140,-65,manifold+(23.5 if j==0 else 63.5)),(150+j*22,-110-j*25,manifold-30),(136,-90-j*25,z),(136,-22,z)],supply if j==0 else ret)
# Left side supplies infrastructure; right ports remain plugged. External plant not sized here.
for j,z in enumerate((manifold+23.5,manifold+63.5)):
    cyl('Left infrastructure G1-4 fitting',(-215,20,z),9,20,steel,'X')
    hose('External cooling connection '+str(j),[(-224,20,z),(-275,50+j*35,z-20),(-280,90+j*35,bottom+70),(-390,90+j*35,bottom+70)],supply if j==0 else ret,8)
assert len([o for o in scene.objects if 'single-slot waterblock' in o.name])==8
assert len([o for o in scene.objects if o.name.startswith('GPU ') and 'parallel coolant' in o.name])==16
assert not any(o.type=='FONT' for o in scene.objects)
# Broad studio lighting and two deterministic cameras, for both image reference and review.
world=bpy.data.worlds.new('White studio');world.use_nodes=True;scene.world=world
world.node_tree.nodes['Background'].inputs[0].default_value=(.85,.88,.92,1);world.node_tree.nodes['Background'].inputs[1].default_value=.8
for loc,power,size in [((0,-1100,2200),50000000,1400),((1000,600,1900),40000000,1200),((-1200,100,1400),25000000,1000)]:
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,200,650))-o.location).to_track_quat('-Z','Y').to_euler()
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.view_settings.view_transform='AgX'
scene.render.resolution_x=1700;scene.render.resolution_y=2000;scene.render.resolution_percentage=100
for name,loc,target,scale in [('01-rack-context',(1500,-2450,1630),(0,180,625),1570),('02-front-layout',(0,-2600,625),(0,0,625),1400)]:
    bpy.ops.object.camera_add(location=loc);o=bpy.context.object;o.name=name;o.data.type='ORTHO';o.data.ortho_scale=scale;o.data.clip_end=10000;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();scene.camera=o
    scene.render.filepath=str(OUT/f'{name}.png');bpy.ops.render.render(write_still=True)
scene.camera=bpy.data.objects['01-rack-context']
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'24U-context.blend'))
(OUT/'layout.json').write_text(json.dumps(dict(rack_U=24,rack_depth_overall_mm=600,rail_spacing_depth_mm=500,rack_units_bottom_to_top=[dict(U='1-8',use='Reserved cooling/power space; external cooling connections shown'),dict(U='9-12',use='4U host, front-accessible PCIe coolant bracket'),dict(U='13-14',use='O-M02 manifold'),dict(U='15-20',use='Open eight-GPU shelf and conceptual PCIe switch'),dict(U='21-24',use='Service space / spare')],front_pair_allocation={'1-8':'Individual GPUs in parallel','9':'Host CPU/chassis branch','10':'Spare'},gpu_envelope_mm=[17,270,132],gpu_pitch_mm=40,host_envelope_mm=[440,456,176],switch_status='Requested x16 uplink / eight x16 endpoints is conceptual; exact board unverified',scope='Concept layout, not an assembly fit, power, thermal or signal-integrity qualification. Coolant colours identify routes only; no markings applied to manifold.'),indent=2)+'\n')
