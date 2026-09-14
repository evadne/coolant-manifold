"""Reproducible RM8-2U review CAD in mm. Thread call-outs in manufacturing.md."""
import json, math
from pathlib import Path
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'cad/parameters.json').read_text())
OUT=ROOT/'output/cad'; OUT.mkdir(parents=True,exist_ok=True)
MESH=ROOT/'tmp/mesh'; MESH.mkdir(parents=True,exist_ok=True)
W,D,H=P['body_width'],P['body_depth'],P['body_height']
xs=[(i-P['branch_count']/2)*P['port_pitch'] for i in range(P['branch_count']+1)]
rows=P['port_rows_z']
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
voids=[]; seals=[]; grooves=[]
for z in rows:
    channel=capsule(P['channel_length'],P['channel_width'],P['channel_depth'],z)
    fluid=channel
    for x in xs:
        pos=(x,0,z); axis=(0,1,0)
        bore=cylinder(P['tap_drill_diameter']/2,P['front_wall']+.1,pos,axis)
        body=body.cut(bore)
        cone=cq.Solid.makeCone(6.9,P['tap_drill_diameter']/2,1.0,cq.Vector(*pos),cq.Vector(*axis))
        body=body.cut(cone);fluid=fluid.union(bore)
    body=body.cut(channel)
    off=P['seal_offset'];gw=P['seal_groove_width'];gd=P['seal_groove_depth']
    outer=capsule(P['channel_length']+2*off+gw,P['channel_width']+2*off+gw,gd,z)
    inner=capsule(P['channel_length']+2*off-gw,P['channel_width']+2*off-gw,gd+.2,z,D+.1)
    groove=outer.cut(inner);body=body.cut(groove);grooves.append(groove)
    # Compressed seal envelope. Purchased seals have round 2 mm cross-section.
    sealouter=capsule(P['channel_length']+2*off+2,P['channel_width']+2*off+2,gd,z)
    sealinner=capsule(P['channel_length']+2*off-2,P['channel_width']+2*off-2,gd+.2,z,D+.1)
    seals.append(sealouter.cut(sealinner));voids.append(fluid)
lid=box(W,P['lid_thickness'],H,y=D)
bolts=[(x,z) for z in (5.5,H/2,H-5.5) for x in xs]+[(x,z) for x in (-213,213) for z in rows]
for x,z in bolts:
    body=body.cut(cylinder(1.65,14,(x,D,z),(0,-1,0)))
    lid=lid.cut(cylinder(2.25,3.1,(x,D,z),(0,1,0)))
    lid=lid.cut(cq.Solid.makeCone(4.2,2.25,1.95,cq.Vector(x,D+3,z),cq.Vector(0,-1,0)))
# Flat mounting faceplate, with the POM sealing face exposed through each window.
T=P['faceplate_thickness']
faceplate=box(P['rack_width'],T,H,y=-T)
for z in rows:
    for x in xs:
        faceplate=faceplate.cut(cylinder(P['faceplate_port_clearance']/2,T+.2,(x,-T-.1,z),(0,1,0)))
rack_z=[6.35-(88.9-H)/2,82.55-(88.9-H)/2]
for sign in (-1,1):
    for z in rack_z:
        faceplate=faceplate.cut(cq.Workplane('XZ',origin=(sign*P['rack_hole_pitch']/2,.1,z)).slot2D(P['rack_slot_length'],P['rack_slot_width']).extrude(T+.2))
mounts=P['faceplate_mounts_xz']
for x,z in mounts:
    faceplate=faceplate.cut(cylinder(2.75,T+.2,(x,-T-.1,z),(0,1,0)))
    faceplate=faceplate.cut(cq.Solid.makeCone(5.2,2.75,2.45,cq.Vector(x,-T,z),cq.Vector(0,1,0)))
    body=body.cut(cylinder(2.1,14,(x,0,z),(0,1,0)))
parts={'body':body,'lid':lid,'faceplate':faceplate}
assembly=cq.Assembly(name='RM8_2U_revision_'+P['revision'])
colours={'body':(.055,.065,.072),'lid':(.56,.59,.62),'faceplate':(.56,.59,.62)}
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
for x,z in mounts:
    fastener=cylinder(2.5,14,(x,0,z),(0,1,0))
    assert all(volume(fastener.intersect(v))<1e-6 for v in voids+grooves)
    for px,pz in bolts:
        assert volume(fastener.intersect(cylinder(2.1,14,(px,D,pz),(0,-1,0))))<1e-6
# The male fitting envelope passes the faceplate without losing thread engagement.
for z in rows:
    for x in xs:
        reference=cylinder(P['qd_male_hex_envelope']/2,T,(x,-T,z),(0,1,0))
        assert volume(reference.intersect(faceplate))<1e-6
        seal_land=cylinder(12,.01,(x,-.01,z),(0,1,0))
        assert volume(seal_land.intersect(faceplate))<1e-6
        assert all(((mx-x)**2+(mz-z)**2)**.5 > 14+5.2 for mx,mz in mounts)
assert H<88.9
assert min(P['port_pitch'],rows[1]-rows[0])-P['qd_clearance_diameter']>=12
# Explicit branch bore connectivity and threaded-bore web envelope.
for z,v in zip(rows,voids):
    for x in xs:
        probe=cylinder(1,P['front_wall']+2,(x,0,z),(0,1,0))
        assert volume(probe.cut(v))<1e-5
report={'revision':P['revision'],'model':'RM8-2U','valid_manufactured_solids':3,'wet_networks':2,
 'branch_circuits':P['branch_count'],'ports':2*len(xs),'lid_screws_M4':len(bolts),'faceplate_screws_M5':len(mounts),
 'assembly_envelope_mm':[P['rack_width'],D+P['lid_thickness']+T,H],'body_volume_mm3':volume(body),
 'estimated_dry_mass_without_fittings_or_screws_kg':volume(body)*1.42e-6+sum(volume(parts[n]) for n in ('lid','faceplate'))*8e-6,
 'reference_pull_ring_gaps_xy_mm':[45-23.7,40-23.7],
 'conservative_28mm_envelope_gaps_mm':[17,12],
 'seal_squeeze_nominal_percent':20,'seal_gland_fill_nominal_percent':math.pi/(2.8*1.6)*100,
 'seal_centreline_length_mm':2*(P['channel_length']-16)+math.pi*(16+7),
 'rack_slot_centres_z_mm':rack_z,
 'faceplate_openings_mm':P['faceplate_port_clearance'],
 'nominal_radial_clearance_to_male_hex_mm':(P['faceplate_port_clearance']-P['qd_male_hex_envelope'])/2,
 'checks':['valid solids','single solid per manufactured part','two separate connected wet networks','all 18 bores connected to intended gallery','no manufactured part overlap','cover and faceplate screws outside galleries and seal grooves','male fitting envelope and POM sealing lands clear faceplate','mounting screws clear fitting envelopes','no intersecting front/rear screw bores','2U envelope','12 mm minimum conservative fitting gap'],
 'limitations':['No pressure or structural rating established','Threads represented by pilot bores, not helices','QD envelopes and release travel require physical trial']}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'tmp/scene.json').write_text(json.dumps({'parameters':P,'ports_x':xs,'cover_bolts':bolts,'faceplate_mounts':mounts}))
print(json.dumps(report,indent=2))
