"""Historical scene inspection; applies only to the revision named below."""
from pathlib import Path
import json
import bpy
from mathutils import Vector
root=Path(__file__).resolve().parents[2]
base=root/'output/manufacturing/O-M02'
results=[]
for variant in ['01-bare-ports','02-qd3-translucent-tubes']:
    bpy.ops.wm.open_mainfile(filepath=str(base/'photorealistic'/f'{variant}.blend'))
    scene=bpy.context.scene
    body=bpy.data.objects['body']
    verts=[body.matrix_world@v.co for v in body.data.vertices]
    lo=min(v.y for v in verts); hi=max(v.y for v in verts)
    assert abs(lo+.004)<1e-7 and abs(hi-.040)<1e-7
    heads=[o for o in scene.objects if o.name.startswith('Front M4')]
    assert len(heads)==6 and all(not o.hide_render for o in heads)
    shoulders=[o for o in scene.objects if o.name.startswith('QD3 reference / Seating shoulder')]
    assert len(shoulders)==20 and all(abs(o.location.y+.005)<1e-7 for o in shoulders)
    tubes=[o for o in scene.objects if o.name.startswith('Translucent tube 10-13')]
    assert len(tubes)==20
    bare=variant=='01-bare-ports'
    assert all(o.hide_render==bare for o in shoulders+tubes)
    assert not any(o.type=='FONT' for o in scene.objects)
    results.append(dict(variant=variant,body_depth_mm=(hi-lo)*1000,boss_seal_plane_y_mm=lo*1000,retention_heads=6,visible_QD_pairs=0 if bare else 20,visible_tubes=0 if bare else 20,surface_markings=False))
report=dict(issue='O-M02',status='PASS',method='Reopen saved Blender scenes; inspect actual mesh bounds, QD placement and visibility',scenes=results)
(base/'render-scene-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
