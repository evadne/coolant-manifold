"""Historical scene inspection; applies only to the revision named below."""
from pathlib import Path
import bpy,json,hashlib
from mathutils import Vector
root=Path(__file__).resolve().parents[2];out=root/'output/context-24U'
bpy.ops.wm.open_mainfile(filepath=str(out/'24U-context.blend'));scene=bpy.context.scene
checks={}
for name,want in [('body',(410,43,87)),('faceplate',(482.6,2,87))]:
 o=scene.objects[name];verts=[o.matrix_world@Vector(v) for v in o.bound_box]
 sizes=[max(v[i] for v in verts)-min(v[i] for v in verts) for i in range(3)]
 assert all(abs(a-b)<.002 for a,b in zip(sizes,want)),(name,sizes)
 checks[name+'_dimensions_xyz_mm']=sizes
plate=next(o for o in scene.objects if o.name.startswith('R6 rack plate'))
verts=[plate.matrix_world@Vector(v) for v in plate.bound_box]
sizes=[max(v[i] for v in verts)-min(v[i] for v in verts) for i in range(3)]
assert all(abs(a-b)<.002 for a,b in zip(sizes,(482.6,2,444.5)))
assert abs(min(v.z for v in verts)-100)<.002
checks['radiator_plate_dimensions_xyz_mm']=sizes
checks['counts']={k:sum(o.name.startswith(prefix) for o in scene.objects) for k,prefix in [('male_fitting_solids','Koolance qd3-mtg4 /'),('female_fitting_solids','Koolance qd3-ft10x13 /'),('manifold_retention_screws','Front M4'),('fan_frames','NF-A20 reference fan-00'),('host_MCIO_cables','Host uplink MCIO 8i cable'),('radiator_rack_screws','R6 populated rack screw')]}
assert checks['counts']==dict(male_fitting_solids=40,female_fitting_solids=54,manifold_retention_screws=12,fan_frames=8,host_MCIO_cables=2,radiator_rack_screws=8)
assert not any(o.type=='FONT' or 'MO-RA' in o.name for o in scene.objects)
layout=json.loads((out/'layout.json').read_text())
for path,sha in layout['source_sha256'].items():assert hashlib.sha256((root/path).read_bytes()).hexdigest()==sha
assert layout['manifold_revision']=='P' and layout['radiator_plate_revision']=='R6'
assert len(layout['view_files'])==4
checks['source_hashes']='PASS';checks['added_text_objects']=0;checks['obsolete_MO_RA_objects']=0
checks['scope']='Scene inventory and nominal source extents; not a complete collision or mechanical qualification.'
checks['checks']='PASS'
(out/'scene-verification.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
