"""Historical scene inspection; applies only to the revision named below."""
from pathlib import Path
import bpy,json
from mathutils import Vector
root=Path(__file__).resolve().parents[2];reports=[]
for stem,visible in [('01-bare-ports',False),('02-qd3-translucent-tubes',True)]:
 p=root/'output/long-bore-P/photorealistic'/f'{stem}.blend'
 bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene
 groups={name:[o for o in s.objects if o.name.startswith(prefix)] for name,prefix in [('male','Koolance QD3-MTG4 /'),('female','Koolance QD3-FT10X13 /'),('tubes','Translucent tube 10-13'),('screws','Front M4')]}
 assert {k:len(v) for k,v in groups.items()}==dict(male=40,female=60,tubes=20,screws=12)
 assert not any(o.type=='FONT' for o in s.objects)
 assert not any(o.name.startswith(('QD3 reference /','Female QD approximation')) for o in s.objects)
 for group in ('male','female','tubes'):assert all(o.hide_render != visible for o in groups[group])
 assert all(not o.hide_render for o in groups['screws'])
 assert all(abs(o.location.y+.003)<1e-7 for o in groups['male'])
 dims={}
 for name,expected in [('body',(410,43,87)),('faceplate',(482.6,2,87))]:
  ob=s.objects[name];coords=[ob.matrix_world@Vector(v) for v in ob.bound_box]
  actual=[1000*(max(v[i] for v in coords)-min(v[i] for v in coords)) for i in range(3)]
  assert all(abs(a-b)<.002 for a,b in zip(actual,expected)),(name,actual)
  dims[name]=actual
 assert (s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage)==(3000,1600,100)
 assert s.cycles.samples==256
 reports.append(dict(file=str(p.relative_to(root)),part_counts={k:len(v) for k,v in groups.items()},fittings_visible=visible,dimensions_xyz_mm=dims,surface_text_objects=0))
(root/'output/long-bore-P/photorealistic/scene-audit.json').write_text(json.dumps(reports,indent=2)+'\n')
print('STUDIO AUDIT PASS')
