"""Reproducible RM8-2U review CAD in mm. Thread call-outs in manufacturing.md."""
import json, math, argparse
from pathlib import Path
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--mounting',choices=('faceplate','backplate'),default='faceplate')
args=parser.parse_args();BACK=args.mounting=='backplate'
P=json.loads((ROOT/'cad/parameters.json').read_text())
# Both mounting options carry the shared geometry revision.
P['mounting']=args.mounting
BASE=ROOT/'output'/('backplate' if BACK else '')
OUT=BASE/'cad'; OUT.mkdir(parents=True,exist_ok=True)
MESH=ROOT/'tmp'/('mesh-backplate' if BACK else 'mesh'); MESH.mkdir(parents=True,exist_ok=True)
W,D,H=P['body_width'],P['body_depth'],P['body_height']
xs=[(i-P['branch_count']/2)*P['port_pitch'] for i in range(P['branch_count']+1)]
rows=P['port_rows_z']
BH=0 if BACK else P['port_boss_height']
FACE_Y=-BH
def box(w,d,h,x=0,y=0,z=0):
    return cq.Workplane('XY').box(w,d,h,centered=(True,False,False)).translate((x,y,z))
def cylinder(r,l,pos,axis):
    return cq.Workplane(obj=cq.Solid.makeCylinder(r,l,cq.Vector(*pos),cq.Vector(*axis)))
def capsule(length,width,depth,z,y=D):
    return (cq.Workplane('XY').slot2D(length,width).extrude(depth)
            .rotate((0,0,0),(1,0,0),90).translate((0,y,z)))
def volume(shape):
    return sum(s.Volume() for s in shape.solids().vals())

body=box(W,D,H)
if not BACK:
    for z in rows:
        for x in xs:
            body=body.union(cylinder(P['port_boss_diameter']/2,BH,(x,-BH,z),(0,1,0)))
    roots=[e for e in body.val().Edges() if e.geomType()=='CIRCLE' and abs(e.Center().y)<1e-6]
    assert len(roots)==2*len(xs)
    body=body.newObject(roots).fillet(P['port_boss_root_radius'])
voids=[]; seals=[]; grooves=[]
for z in rows:
    channel=capsule(P['channel_length'],P['channel_width'],P['channel_depth'],z)
    fluid=channel
    for x in xs:
        pos=(x,FACE_Y,z); axis=(0,1,0)
        bore=cylinder(P['tap_drill_diameter']/2,P['front_wall']+BH+.1,pos,axis)
        body=body.cut(bore)
        cone=cq.Solid.makeCone(6.9,P['tap_drill_diameter']/2,1.0,cq.Vector(*pos),cq.Vector(*axis))
        body=body.cut(cone);fluid=fluid.union(bore)
    body=body.cut(channel)
    off=P['seal_offset'];gw=P['seal_groove_width'];gd=P['seal_groove_depth']
    outer=capsule(P['channel_length']+2*off+gw,P['channel_width']+2*off+gw,gd,z)
    inner=capsule(P['channel_length']+2*off-gw,P['channel_width']+2*off-gw,gd+.2,z,D+.1)
    groove=outer.cut(inner);body=body.cut(groove);grooves.append(groove)
    # Volume-equivalent rectangular compressed envelope, not deformed elastomer FEA.
    path=2*(P['channel_length']-P['channel_width'])+math.pi*(P['channel_width']+2*off)
    free_path=math.pi*(P['seal_ring']['ID']+P['seal_cross_section'])
    stretch_ratio=path/free_path
    installed_cs=P['seal_cross_section']/math.sqrt(stretch_ratio)
    seal_width=math.pi*installed_cs**2/(4*gd)
    sealouter=capsule(P['channel_length']+2*off+seal_width,P['channel_width']+2*off+seal_width,gd,z)
    sealinner=capsule(P['channel_length']+2*off-seal_width,P['channel_width']+2*off-seal_width,gd+.2,z,D+.1)
    seals.append(sealouter.cut(sealinner));voids.append(fluid)
lid=box(P['rack_width'] if BACK else W,P['lid_thickness'],H,y=D)
bolts=[(x,z) for z in (P['cover_bolt_edge_offset'],H/2,H-P['cover_bolt_edge_offset']) for x in xs]+[(x,z) for x in (-213,213) for z in rows]
C=P['cover_fastener'];CT=P['lid_thickness']
for x,z in bolts:
    body=body.cut(cylinder(C['tap_drill_diameter']/2,C['pilot_depth'],(x,D,z),(0,-1,0)))
    lid=lid.cut(cylinder(C['clearance_diameter']/2,CT+.1,(x,D,z),(0,1,0)))
    lid=lid.cut(cq.Solid.makeCone(C['countersink_diameter']/2,C['clearance_diameter']/2,(C['countersink_diameter']-C['clearance_diameter'])/2,cq.Vector(x,D+CT,z),cq.Vector(0,-1,0)))
# Both options use flat steel: a front mounting faceplate or a rear combined cover/mount.
T=P['faceplate_thickness']
# Option C retains its independent M5 mounting specification.
F=({'nominal_diameter':5.0,'clearance_diameter':5.5,'countersink_diameter':10.4,
    'tap_drill_diameter':4.2,'pilot_depth':14.0} if BACK else P['faceplate_fastener'])
CS_DEPTH=(F['countersink_diameter']-F['clearance_diameter'])/2
assert CS_DEPTH<T
if BACK:
    mounting_plate=lid
else:
    mounting_plate=box(P['rack_width'],T,H,y=-T)
    for z in rows:
        for x in xs:
            mounting_plate=mounting_plate.cut(cylinder(P['faceplate_port_clearance']/2,T+.2,(x,-T-.1,z),(0,1,0)))
rack_z=[6.35-(88.9-H)/2,82.55-(88.9-H)/2]
for sign in (-1,1):
    for z in rack_z:
        origin_y=D+T+.1 if BACK else .1
        mounting_plate=mounting_plate.cut(cq.Workplane('XZ',origin=(sign*P['rack_hole_pitch']/2,origin_y,z)).slot2D(P['rack_slot_length'],P['rack_slot_width']).extrude(T+.2))
mounts=P['faceplate_mounts_xz']
for x,z in mounts:
    outer_y=D+T if BACK else -T
    body_y=D if BACK else 0
    axis=(0,-1,0) if BACK else (0,1,0)
    mounting_plate=mounting_plate.cut(cylinder(F['clearance_diameter']/2,T+.1,(x,outer_y,z),axis))
    mounting_plate=mounting_plate.cut(cq.Solid.makeCone(F['countersink_diameter']/2,F['clearance_diameter']/2,CS_DEPTH,cq.Vector(x,outer_y,z),cq.Vector(*axis)))
    body=body.cut(cylinder(F['tap_drill_diameter']/2,F['pilot_depth'],(x,body_y,z),axis))
parts={'body':body,'backplate':mounting_plate} if BACK else {'body':body,'lid':lid,'faceplate':mounting_plate}
assembly=cq.Assembly(name='RM8_2U_revision_'+P['revision'])
colours={'body':(.055,.065,.072),'lid':(.56,.59,.62),'faceplate':(.56,.59,.62),'backplate':(.56,.59,.62)}
for name,part in parts.items():
    assert part.val().isValid(),name
    assert len(part.solids().vals())==1,name
    cq.exporters.export(part,str(OUT/f'{name}.step'))
    cq.exporters.export(part,str(MESH/f'{name}.stl'),tolerance=.06,angularTolerance=.12)
    assembly.add(part,name=name,color=cq.Color(*colours[name]))
for i,s in enumerate(seals):
    assembly.add(s,name=f'seal_{i+1}',color=cq.Color(.1,.1,.1))
    cq.exporters.export(voids[i],str(MESH/f'gallery_{i}.stl'))
assembly.export(str(OUT/'manifold-assembly.step'))
# Check topology and the main manufacturing/clearance failure modes.
assert all(len(v.solids().vals())==1 for v in voids)
assert volume(voids[0].intersect(voids[1]))<1e-6
for a,pa in parts.items():
    for b,pb in parts.items():
        if a<b: assert volume(pa.intersect(pb))<1e-5,(a,b)
for x,z in bolts:
    fastener=cylinder(2.1,14,(x,D,z),(0,-1,0))
    assert all(volume(fastener.intersect(v))<1e-6 for v in voids+grooves)
# Measure the material beside the conservative Ø4.2 threaded-hole envelopes.
cover_land=min(cylinder(2.1,14,(x,D,z),(0,-1,0)).val().distance(g.val()) for x,z in bolts for g in grooves)
assert cover_land >= 1.0
for x,z in mounts:
    fastener=cylinder(F['nominal_diameter']/2,F['pilot_depth'],(x,D if BACK else 0,z),(0,-1 if BACK else 1,0))
    assert all(volume(fastener.intersect(v))<1e-6 for v in voids+grooves)
    for px,pz in bolts:
        assert volume(fastener.intersect(cylinder(2.1,14,(px,D,pz),(0,-1,0))))<1e-6
# Raised sealing lands clear the plate even when a fitting body overhangs the boss.
if not BACK:
    assert BH-T>=3
    for z in rows:
        for x in xs:
            # A 36 mm body is deliberately larger than the 32 mm plate window.
            overhang=cylinder(P['port_hardware_keepout_diameter']/2,12,(x,FACE_Y,z),(0,-1,0))
            assert volume(overhang.intersect(mounting_plate))<1e-6
            seal_land=cylinder(P['port_boss_diameter']/2-.2,.01,(x,FACE_Y-.01,z),(0,1,0))
            assert volume(seal_land.intersect(mounting_plate))<1e-6
            assert all(((mx-x)**2+(mz-z)**2)**.5 > P['faceplate_port_clearance']/2+F['countersink_diameter']/2 for mx,mz in mounts)
assert H<88.9
assert min(P['port_pitch'],rows[1]-rows[0])-P['qd_clearance_diameter']>=12
# Explicit branch bore connectivity and threaded-bore web envelope.
for z,v in zip(rows,voids):
    for x in xs:
        probe=cylinder(1,P['front_wall']+BH+2,(x,FACE_Y,z),(0,1,0))
        assert volume(probe.cut(v))<1e-5
# Check both specified bought-in head envelopes and blind-hole length budget.
fastener_fit={}
proud_head_clearance=None
if not BACK:
    for name,diameter,height in [(F['standard'],F['head_diameter'],F['head_height']),
            (F['alternative']['standard'],F['alternative']['head_diameter'],F['alternative']['head_height'])]:
        recess=(F['countersink_diameter']-diameter)/2
        penetration=F['length_including_head']-T+recess
        assert recess>=0 and height+recess<T
        assert penetration<F['full_thread_depth_min']<F['pilot_depth']
        # The countersunk bearing cone must lie entirely inside the steel cutout.
        x,z=mounts[0]
        head=cq.Solid.makeCone(diameter/2,F['nominal_diameter']/2,
            (diameter-F['nominal_diameter'])/2,cq.Vector(x,-T+recess,z),cq.Vector(0,1,0))
        assert volume(mounting_plate.intersect(cq.Workplane(obj=head)))<1e-6
        fastener_fit[name]={'nominal_head_recess_mm':recess,'nominal_tip_depth_in_POM_mm':penetration,
            'full_thread_depth_margin_mm':F['full_thread_depth_min']-penetration}
    # Conservative independent head extrema with specified plate/countersink tolerances.
    worst_head_depth=F['head_height']+(F['countersink_diameter']+.1-F['head_diameter_min'])/2
    assert worst_head_depth<T-.1
    # Slightly proud heads are acceptable only outside the port hardware keep-out.
    # Check 0.2 mm as a review case; this is not an ergonomic or load qualification.
    head_r=max(F['head_diameter'],F['alternative']['head_diameter'])/2
    proud_head_clearance=min(math.hypot(mx-x,mz-z)-head_r-P['port_hardware_keepout_diameter']/2
        for mx,mz in mounts for x in xs for z in rows)
    assert proud_head_clearance>0
    for mx,mz in mounts:
        proud_head=cylinder(head_r,F['proud_head_review_height'],(mx,-T,mz),(0,-1,0))
        for x in xs:
            for z in rows:
                keepout=cylinder(P['port_hardware_keepout_diameter']/2,100,(x,0,z),(0,-1,0))
                assert volume(proud_head.intersect(keepout))<1e-6
# Check nominal and dimensional-tolerance seal compression. No thermal/swell or preload model.
assert .15 < 1-gd/installed_cs < .30
assert .60 < math.pi*installed_cs**2/(4*gw*gd) < .85
assert 0 < stretch_ratio-1 < .03
assert P['seal_offset']-gw/2 >= 2
assert P['channel_width']/2+P['seal_offset']-gw/2 >= 3*(P['seal_cross_section']+P['seal_ring']['cross_section_tolerance_review'])
# Full projected thread-major circle must fit the gallery opening at each port.
for z in rows:
    channel=capsule(P['channel_length'],P['channel_width'],1,z)
    for x in xs:
        major=cylinder(P['thread_major_diameter']/2,1,(x,D,z),(0,-1,0))
        assert volume(major.cut(channel))<1e-6
report={'revision':P['revision'],'model':'RM8-2U','mounting':args.mounting,'valid_manufactured_solids':len(parts),'wet_networks':2,
 'branch_circuits':P['branch_count'],'ports':2*len(xs),'lid_screws_M4':len(bolts),('body_mount_screws_M5' if BACK else 'body_mount_screws_M4'):len(mounts),
 'assembly_envelope_mm':[P['rack_width'],D+P['lid_thickness']+BH,H],'body_volume_mm3':volume(body),
 'estimated_dry_mass_without_fittings_or_screws_kg':volume(body)*1.42e-6+sum(volume(v) for k,v in parts.items() if k!='body')*8e-6,
 'reference_pull_ring_gaps_xy_mm':[45-23.7,40-23.7],
 'conservative_28mm_envelope_gaps_mm':[17,12],
 'seal_squeeze_nominal_percent':100*(1-gd/P['seal_cross_section']),
 'seal_squeeze_after_centreline_stretch_percent':100*(1-gd/installed_cs),
 'seal_gland_fill_nominal_percent':math.pi*P['seal_cross_section']**2/(4*gw*gd)*100,
 'seal_gland_fill_after_centreline_stretch_percent':seal_width/gw*100,
 'seal_centreline_length_mm':path,'seal_ring_free_ID_mm':P['seal_ring']['ID'],
 'seal_centreline_stretch_percent':100*(stretch_ratio-1),
 'seal_compressed_envelope_width_mm':seal_width,
 'gallery_to_groove_land_mm':off-gw/2,
 'groove_inside_end_radius_mm':P['channel_width']/2+off-gw/2,
 'cover_thread_envelope_to_groove_min_mm':cover_land,
 'cover_countersink_to_outer_edge_min_mm':P['cover_bolt_edge_offset']-4.2,
 'rack_slot_centres_z_mm':rack_z,
 'mounting_countersink_depth_mm':CS_DEPTH,
 'mounting_plate_straight_bore_length_mm':T-CS_DEPTH,
 'faceplate_fastener_fit':fastener_fit,
 'proud_head_review_height_mm':None if BACK else F['proud_head_review_height'],
 'port_hardware_keepout_diameter_mm':None if BACK else P['port_hardware_keepout_diameter'],
 'head_edge_to_port_hardware_keepout_min_mm':proud_head_clearance,
 'faceplate_openings_mm':None if BACK else P['faceplate_port_clearance'],
 'boss_to_window_radial_clearance_mm':None if BACK else (P['faceplate_port_clearance']-P['port_boss_diameter'])/2,
 'boss_height_from_mounting_face_mm':BH,
 'seal_face_proud_of_steel_mm':None if BACK else BH-T,
 'pom_projection_ahead_of_rack_rail_mm':D+T if BACK else BH,
 'reference_male_tip_ahead_of_rack_rail_mm':D+T+32.1 if BACK else BH+32.1,
 'checks':['valid solids','single solid per manufactured part','two separate connected wet networks','all 18 bores connected to intended gallery','thread-major port circles fully inside gallery openings','seal compression and fill after nominal stretch','at least 1 mm nominal cover thread-envelope to groove land','groove inside end radius at least three maximum review cord diameters','no manufactured part overlap','cover and body-mount screws outside galleries and seal grooves','unobstructed POM sealing faces' if BACK else '36 mm fitting overhang and raised POM seals clear faceplate','no intersecting cover/mount screw bores','2U envelope','12 mm minimum conservative fitting gap']+([] if BACK else ['both specified M4 bearing cones clear steel','head envelope contained within plate','blind M4 nominal thread and pilot depth budget','0.2 mm proud heads remain outside 36 mm port hardware keep-outs']),
 'limitations':['No pressure or structural rating established','Threads represented by pilot bores, not helices','QD envelopes and release travel require physical trial']}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'tmp'/('scene-backplate.json' if BACK else 'scene.json')).write_text(json.dumps({'parameters':P,'ports_x':xs,'cover_bolts':bolts,'faceplate_mounts':mounts}))
print(json.dumps(report,indent=2))
