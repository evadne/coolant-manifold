"""Selected Option B: cut-only DXFs and dimensioned SVG plate drafts in mm.

Checks exported cut features against the finished STEP plates, including the
cylindrical through-hole and conical countersink surfaces. No threads in steel.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import json
import math
import ezdxf
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
P = json.loads((ROOT / 'cad/parameters.json').read_text())
OUT = ROOT / 'output'
H = P['body_height']
XS = [(i-P['branch_count']/2)*P['port_pitch'] for i in range(P['branch_count']+1)]
COVER = [(x,z) for z in (P['cover_bolt_edge_offset'], H/2, H-P['cover_bolt_edge_offset']) for x in XS]
COVER += [(x,z) for x in (-213,213) for z in P['port_rows_z']]
SLOTS = [(x,z) for x in (-P['rack_hole_pitch']/2,P['rack_hole_pitch']/2)
         for z in (6.35-(88.9-H)/2,82.55-(88.9-H)/2)]


def export_plate(rear):
    name = 'rear-cover' if rear else 'faceplate'
    title = 'REAR / GALLERY SEALING PLATE' if rear else 'FRONT / RACK FACEPLATE'
    width = P['body_width'] if rear else P['rack_width']
    thick = P['lid_thickness'] if rear else P['faceplate_thickness']
    fast = P['cover_fastener'] if rear else P['faceplate_fastener']
    assert fast['thread'] == 'M4 x 0.7' and fast['standard'] == 'DIN 7991'
    mounts = COVER if rear else P['faceplate_mounts_xz']
    windows = [] if rear else [(x,z) for z in P['port_rows_z'] for x in XS]
    slots = [] if rear else SLOTS
    dia, csk = fast['clearance_diameter'], fast['countersink_diameter']
    depth = (csk-dia)/2
    circles = [(x,z,dia/2) for x,z in mounts] + [(x,z,P['faceplate_port_clearance']/2) for x,z in windows]
    doc = ezdxf.new('R2010'); doc.units = 4; doc.layers.new('CUT'); m = doc.modelspace()
    attr = {'layer':'CUT'}
    m.add_lwpolyline([(-width/2,0),(width/2,0),(width/2,H),(-width/2,H)], close=True, dxfattribs=attr)
    for x,z,r in circles:
        m.add_circle((x,z),r,dxfattribs=attr)
    for x,z in slots:
        r=P['rack_slot_width']/2; a=(P['rack_slot_length']-P['rack_slot_width'])/2
        m.add_lwpolyline([(x-a,z-r,0),(x+a,z-r,1),(x+a,z+r,0),(x-a,z+r,1)],format='xyb',close=True,dxfattribs=attr)
    dxf = OUT / 'cad' / f'{name}-flat.dxf'; doc.saveas(dxf)
    check = ezdxf.readfile(dxf)
    assert not check.audit().has_errors
    assert len(check.modelspace().query('CIRCLE')) == len(circles)
    assert len(check.modelspace().query('LWPOLYLINE')) == 1+len(slots)
    assert all(e.dxf.layer=='CUT' for e in check.modelspace())
    for entity, expected in zip(check.modelspace().query('CIRCLE'),circles):
        assert all(abs(a-b)<1e-8 for a,b in zip((entity.dxf.center.x,entity.dxf.center.y,entity.dxf.radius),expected))

    # Check the cut circles against actual cylinder faces in the existing CAD.
    step = OUT / 'cad' / ('lid.step' if rear else 'faceplate.step')
    solid = cq.importers.importStep(str(step)).val()
    assert solid.isValid() and len(solid.Solids()) == 1
    bb=solid.BoundingBox()
    assert abs(bb.xlen-width)<1e-6 and abs(bb.ylen-thick)<1e-6 and abs(bb.zlen-H)<1e-6
    cylinder_faces=[f for f in solid.Faces() if f.geomType()=='CYLINDER']
    cone_faces=[f for f in solid.Faces() if f.geomType()=='CONE']
    assert len(cone_faces)==len(mounts)
    for x,z,r in circles:
        matches=[f for f in cylinder_faces if abs(f.BoundingBox().xmin-(x-r))<1e-5 and abs(f.BoundingBox().xmax-(x+r))<1e-5 and abs(f.BoundingBox().zmin-(z-r))<1e-5 and abs(f.BoundingBox().zmax-(z+r))<1e-5]
        assert len(matches)==1, (name,x,z,r)
        expected_depth=thick-depth if (x,z) in [tuple(v) for v in mounts] else thick
        assert abs(matches[0].BoundingBox().ylen-expected_depth)<1e-5
    for x,z in mounts:
        matches=[f for f in cone_faces if abs(f.BoundingBox().xmin-(x-csk/2))<1e-5 and abs(f.BoundingBox().zmin-(z-csk/2))<1e-5]
        assert len(matches)==1 and abs(matches[0].BoundingBox().ylen-depth)<1e-5
    # Volume also checks the rack slots and verifies that DXF represents the blank before countersinking.
    removed=sum(math.pi*r*r for x,z,r in circles)
    removed+=len(slots)*((P['rack_slot_length']-P['rack_slot_width'])*P['rack_slot_width']+math.pi*(P['rack_slot_width']/2)**2)
    cone_extra=math.pi*depth/3*((csk/2)**2+csk*dia/4+(dia/2)**2)-math.pi*(dia/2)**2*depth
    expected_volume=(width*H-removed)*thick-len(mounts)*cone_extra
    assert abs(solid.Volume()-expected_volume)<1e-3

    a=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1130" viewBox="0 0 1600 1130">',
       '<rect width="1600" height="1130" fill="white"/>',
       '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto-start-reverse"><path d="M8 0 L0 4 L8 8" fill="none" stroke="#596a75"/></marker></defs>',
       '<g font-family="Arial,sans-serif" fill="#193343">']
    def text(x,y,t,size=18,anchor='start',colour='#193343'):
        a.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{colour}">{escape(t)}</text>')
    def line(x1,y1,x2,y2,dash='',arrow=False):
        markers=' marker-start="url(#arr)" marker-end="url(#arr)"' if arrow else ''
        a.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#596a75" stroke-width="1" stroke-dasharray="{dash}"{markers}/>')
    text(60,58,f'RM8-2U / {title}',30)
    text(60,94,f'Geometry revision {P["revision"]} · Selected Option B · 1 required · All dimensions in mm · Do not scale',18)
    text(60,128,'316L / EN 1.4404 stainless · 3.00 ±0.10 FINISHED thickness' if rear else '304 or 316 stainless · 3.00 ±0.10 FINISHED thickness',18)
    text(60,162,'Outside face shown; countersink this face. Opposite face mates to POM.',17)
    scale=2.7; ox=800; oy=218
    def pt(x,z): return ox+scale*x,oy+scale*(H-z)
    left,top=pt(-width/2,H); right,bottom=pt(width/2,0)
    a.append(f'<rect x="{left}" y="{top}" width="{width*scale}" height="{H*scale}" fill="#f3f5f6" stroke="#193343" stroke-width="1.5"/>')
    for x,z,r in circles:
        cx,cy=pt(x,z)
        a.append(f'<circle cx="{cx}" cy="{cy}" r="{r*scale}" fill="white" stroke="#193343" stroke-width="1.2"/>')
    for x,z in mounts:
        cx,cy=pt(x,z)
        a.append(f'<circle cx="{cx}" cy="{cy}" r="{csk/2*scale}" fill="none" stroke="#207c9a" stroke-width="1.2"/>')
        line(cx-5,cy,cx+5,cy);line(cx,cy-5,cx,cy+5)
    for x,z in slots:
        cx,cy=pt(x,z);sw=P['rack_slot_length']*scale;sh=P['rack_slot_width']*scale
        a.append(f'<rect x="{cx-sw/2}" y="{cy-sh/2}" width="{sw}" height="{sh}" rx="{sh/2}" fill="white" stroke="#193343"/>')
    line(ox,top-12,ox,bottom+18,'8 4')
    text(ox,bottom+39,'X = 0 / Z = 0 at bottom centre',15,'middle')
    line(left,top-42,right,top-42,arrow=True)
    line(left,top-50,left,top-8);line(right,top-50,right,top-8)
    text(ox,top-51,f'{width:g} overall',17,'middle')
    line(right+28,top,right+28,bottom,arrow=True)
    text(right+43,(top+bottom)/2+6,f'{H:g}',17)
    text(60,525,f'{len(mounts)} × Ø{dia:g} +0.10/0 THRU · Ø{csk:g} +0.10/0 × 90° countersink on outside face',22)
    text(60,555,'Black outlines = CUT DXF geometry. Blue circles = machined countersinks; not laser-cut circles.',17)
    line(60,578,1540,578)
    text(60,614,'HOLE CENTRES / X, Z',21)
    if rear:
        rows=[
          '27 holes: every combination of the following X and Z coordinates:',
          'X = −180, −135, −90, −45, 0, 45, 90, 135, 180',
          f'Z = {P["cover_bolt_edge_offset"]:g}, {H/2:g}, {H-P["cover_bolt_edge_offset"]:g} (9 holes per row)',
          '4 end holes: X = −213 and 213; Z = 23.5 and 63.5',
          'No rack slots, port windows, threads or grooves in this plate.'
        ]
    else:
        rows=[
          '8 M4 holes: X = −208 and 208; Z = 9, 43.5 and 78 (6 holes)',
          'Plus X = −67.5 and 67.5; Z = 43.5 (2 holes)',
          '18 × Ø32 +0.20/0 windows: X = −180 to 180 at 45 pitch;',
          'Z = 23.5 and 63.5 (9 windows per row)',
          '4 slots: 10 × 7 overall, R3.5 ends; X = ±232.55;',
          'Z = 5.4 and 81.6. Rack fixing centres 465.1 horizontally.'
        ]
    for i,t in enumerate(rows):text(60,647+29*i,t,17)
    text(1040,614,'TYPICAL M4 SECTION',21)
    # Through-hole section, enlarged; outside at top, POM side at bottom.
    sx,sy,ss=1270,647,19
    for sign in (-1,1):
        points=[(sx+sign*7*ss,sy),(sx+sign*csk/2*ss,sy),(sx+sign*dia/2*ss,sy+depth*ss),(sx+sign*dia/2*ss,sy+thick*ss),(sx+sign*7*ss,sy+thick*ss)]
        a.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in points)+'" fill="#d7e0e4" stroke="#193343"/>')
    text(sx,sy-10,f'Ø{csk:g} / 90°',16,'middle')
    text(sx,sy+thick*ss+25,f'Ø{dia:g} through',16,'middle')
    text(1040,761,f'Cone depth {depth:.2f} nominal',17)
    text(1040,788,f'Straight bore {thick-depth:.2f} nominal',17)
    text(1040,817,'No countersink on POM-facing side',17)
    line(60,842,1540,842)
    notes=[
      'Punch or laser-cut outline and through holes. Finish holes as needed; machine countersinks afterwards. No bending.',
      'Hole/window centres ±0.10 relative to bottom-centre datum; other dimensions ±0.15 unless specified.',
      'Deburr and flatten after cutting. External edges: break 0.3–0.5; do not enlarge specified bores or countersinks.',
      'A4 M4 × 12 DIN 7991 socket countersunk screws; specified DIN 965 Z Pozi accepted. Threads are in POM only.',
    ]
    if rear:
        notes += ['POM-facing seal surface: Ra ≤0.8 µm; flatness 0.05 across each seal perimeter. No burrs or radial scratches.',
                  'Remove cutting oxide/heat tint and iron contamination; clean/passivate as appropriate, rinse and dry. See material notes.']
    else:
        notes += ['Dry structural plate. Eighteen windows clear the integral POM bosses; fittings seal directly on their raised ends.',
                  'Rack slots take fixings matching the actual rails/cage nuts; the M4 specification applies to plate-to-POM joints.']
    for i,t in enumerate(notes):text(60,878+28*i,t,17)
    text(60,1090,'DRAFT FOR VENDOR DFM / NOT A PRESSURE OR STRUCTURAL RELEASE',17,colour='#a4502c')
    text(1540,1090,f'{name}-flat.dxf + '+step.name,16,'end')
    a.append('</g></svg>');(OUT/f'{name}-drawing.svg').write_text('\n'.join(a)+'\n')
    return {'plate':name,'screw_holes_M4':len(mounts),'through_diameter_mm':dia,'countersink_diameter_mm':csk,'windows':len(windows),'rack_slots':len(slots),'finished_STEP_volume_mm3':solid.Volume(),'checks':['DXF reopened and audited','cut circle centres and diameters match STEP','countersink surfaces match STEP','plate envelope and analytic volume match STEP']}

if __name__=='__main__':
    report={'revision':P['revision'],'mounting':'selected Option B','plates':[export_plate(False),export_plate(True)]}
    (OUT/'cad/steel-plate-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
