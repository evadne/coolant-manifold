"""Historical scene inspection; applies only to the revision named below."""
from pathlib import Path
import bpy,json,hashlib
from collections import defaultdict
bpy.ops.wm.open_mainfile(filepath=str(Path(__file__).resolve().parents[2]/'output/context-24U/24U-context.blend'))
s=bpy.context.scene;groups=defaultdict(list)
for o in s.objects:
 if o.type!='MESH':continue
 key=(tuple(round(v,5) for row in o.matrix_world for v in row),len(o.data.vertices),len(o.data.polygons),tuple(round(v,5) for v in o.dimensions))
 groups[key].append(o)
dup=[]
for obs in groups.values():
 if len(obs)<2:continue
 coords=defaultdict(list)
 for o in obs:
  h=hashlib.sha256(str([(tuple(v.co)) for v in o.data.vertices]).encode()).hexdigest();coords[h].append(o.name)
 dup.extend(v for v in coords.values() if len(v)>1)
p=next(o for o in s.objects if o.name.startswith('R6 rack plate'))
print(json.dumps({'duplicate_mesh_placements':dup,'plate_objects':[o.name for o in s.objects if 'rack plate' in o.name],'plate_faces':len(p.data.polygons),'plate_triangles':sum(len(f.vertices)==3 for f in p.data.polygons),'plate_modifiers':[(m.name,m.type) for m in p.modifiers],'viewports':[dict(screen=sc.name,near=a.spaces.active.clip_start,far=a.spaces.active.clip_end,wire=a.spaces.active.overlay.show_wireframes,xray=a.spaces.active.shading.show_xray) for sc in bpy.data.screens for a in sc.areas if a.type=='VIEW_3D']},indent=2))
