"""Historical scene inspection; applies only to the revision named below."""
from pathlib import Path
import bpy,json
from mathutils import Vector
root=Path(__file__).resolve().parents[2]
bpy.ops.wm.open_mainfile(filepath=str(root/'output/long-bore-I/rack-installation/revision-I-in-42U-rack.blend'))
objects=list(bpy.context.scene.objects)
tubes=[o for o in objects if o.name.startswith('10-16 tube side')]
fittings=[o for o in objects if o.name.startswith('Side rotary elbow')]
assert len(tubes)==4 and len(fittings)==4
assert not any('side plug' in o.name.lower() or o.type=='FONT' for o in objects)
assert len([o for o in objects if o.name.startswith('42U perforated')])==4
assert len([o for o in objects if o.name.startswith('Front M4 DIN')])==6
assert len([o for o in objects if o.name.startswith('Rack mounting screw')])==4
assert abs(bpy.data.objects['body'].dimensions.x-390)<.001
for o in tubes+fittings:
 points=[o.matrix_world@Vector(v) for v in o.bound_box]
 assert max(abs(v.x) for v in points)<225
print('PASS: Revision I body, 4 fitted side ports, 4 annular tubes, 4 rack flanges, 6 M4 retainers, 4 rack screws; fittings/tubes inside assumed 450 mm opening; no plugs or text.')
