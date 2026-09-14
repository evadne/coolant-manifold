"""Flat cut profile, XY = model XZ, millimetres. Countersink separately per notes."""
from pathlib import Path
import json
import ezdxf
R=Path(__file__).resolve().parents[1];p=json.loads((R/'cad/parameters.json').read_text())
doc=ezdxf.new('R2010');doc.units=4;doc.layers.new('CUT');m=doc.modelspace()
w=p['rack_width']/2;h=p['body_height']
m.add_lwpolyline([(-w,0),(w,0),(w,h),(-w,h)],close=True,dxfattribs={'layer':'CUT'})
xs=[(i-p['branch_count']/2)*p['port_pitch'] for i in range(p['branch_count']+1)]
for z in p['port_rows_z']:
    for x in xs:m.add_circle((x,z),p['faceplate_port_clearance']/2,dxfattribs={'layer':'CUT'})
for x,z in p['faceplate_mounts_xz']:m.add_circle((x,z),2.75,dxfattribs={'layer':'CUT'})
for x in (-p['rack_hole_pitch']/2,p['rack_hole_pitch']/2):
    for z in (6.35-(88.9-h)/2,82.55-(88.9-h)/2):
        r=p['rack_slot_width']/2;a=(p['rack_slot_length']-p['rack_slot_width'])/2
        m.add_lwpolyline([(x-a,z-r,0),(x+a,z-r,1),(x+a,z+r,0),(x-a,z+r,1)],format='xyb',close=True,dxfattribs={'layer':'CUT'})
path=R/'output/cad/faceplate-flat.dxf';doc.saveas(path)
check=ezdxf.readfile(path);assert len(check.modelspace().query('CIRCLE'))==26;assert len(check.modelspace().query('LWPOLYLINE'))==5
print('Wrote and reopened faceplate-flat.dxf: 18 windows, 8 screw holes, 4 rack slots, 1 outline.')
