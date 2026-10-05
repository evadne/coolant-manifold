"""Historical scene inspection; applies only to the revision named below."""
import bpy,json
from pathlib import Path
p=Path(__file__).resolve().parents[2]/'output/long-bore-M/photorealistic'
for name in ['01-bare-ports','02-qd3-translucent-tubes']:
    f=p/(name+'.blend')
    if not f.exists():continue
    bpy.ops.wm.open_mainfile(filepath=str(f))
    scene=bpy.context.scene
    visible=[o for o in scene.objects if not o.hide_render]
    dims={n:[round(v*1000,3) for v in bpy.data.objects[n].dimensions] for n in ('body','faceplate')}
    assert abs(dims['body'][0]-410)<.01
    assert abs(dims['faceplate'][0]-482.6)<.01
    assert len([o for o in visible if o.name.startswith('Front M4')])==6
    assert not any(o.type=='FONT' for o in visible)
    groups={prefix:len([o for o in visible if o.name.startswith(prefix)]) for prefix in ('QD3 reference /','Female QD approximation','Translucent tube','G1-4 side plug reference')}
    assert list(groups.values())==([0,0,0,0] if 'bare' in name else [80,80,20,4])
    print('VERIFIED',name,json.dumps({'dimensions_mm':dims,'visible_hardware_parts':groups}))
