"""Flat cut profile, XY = model XZ, millimetres. Countersink separately per notes."""
from pathlib import Path
import json,argparse
import ezdxf
R=Path(__file__).resolve().parents[1];p=json.loads((R/'cad/parameters.json').read_text())
parser=argparse.ArgumentParser();parser.add_argument('--mounting',choices=('faceplate','backplate'),default='faceplate');args=parser.parse_args();BACK=args.mounting=='backplate'
doc=ezdxf.new('R2010');doc.units=4;doc.layers.new('CUT');m=doc.modelspace()
w=p['rack_width']/2;h=p['body_height']
m.add_lwpolyline([(-w,0),(w,0),(w,h),(-w,h)],close=True,dxfattribs={'layer':'CUT'})
xs=[(i-p['branch_count']/2)*p['port_pitch'] for i in range(p['branch_count']+1)]
if BACK:
    bolts=[(x,z) for z in (p['cover_bolt_edge_offset'],h/2,h-p['cover_bolt_edge_offset']) for x in xs]+[(x,z) for x in (-213,213) for z in p['port_rows_z']]
    for x,z in bolts:m.add_circle((x,z),2.25,dxfattribs={'layer':'CUT'})
else:
    for z in p['port_rows_z']:
        for x in xs:m.add_circle((x,z),p['faceplate_port_clearance']/2,dxfattribs={'layer':'CUT'})
for x,z in p['faceplate_mounts_xz']:m.add_circle((x,z),2.75 if BACK else p['faceplate_fastener']['clearance_diameter']/2,dxfattribs={'layer':'CUT'})
for x in (-p['rack_hole_pitch']/2,p['rack_hole_pitch']/2):
    for z in (6.35-(88.9-h)/2,82.55-(88.9-h)/2):
        r=p['rack_slot_width']/2;a=(p['rack_slot_length']-p['rack_slot_width'])/2
        m.add_lwpolyline([(x-a,z-r,0),(x+a,z-r,1),(x+a,z+r,0),(x-a,z+r,1)],format='xyb',close=True,dxfattribs={'layer':'CUT'})
path=R/'output'/('backplate/cad/backplate-flat.dxf' if BACK else 'cad/faceplate-flat.dxf');doc.saveas(path)
check=ezdxf.readfile(path);assert len(check.modelspace().query('CIRCLE'))==(39 if BACK else 26);assert len(check.modelspace().query('LWPOLYLINE'))==5
print(f'Wrote and reopened {path.name}: '+('31 cover holes, 8 body mounts' if BACK else '18 windows, 8 body mounts')+', 4 rack slots, 1 outline.')
