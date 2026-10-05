"""Prepare the Q-M02 specification-only faceplate revision from submitted Q-M01 geometry."""
from pathlib import Path
import hashlib
import revision_json as json
import shutil
import math, argparse

R = Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--manufacturing-revision',choices=['Q-M02','Q-M03'],default='Q-M02')
MANUFACTURING_REVISION=parser.parse_args().manufacturing_revision
M = json.loads((R/f'cad/manufacturing/{MANUFACTURING_REVISION}.json').read_text())
source = R/'output/manufacturing/Q-M01'
out = R/f'output/manufacturing/{MANUFACTURING_REVISION}'
out.mkdir(parents=True, exist_ok=True)
prior = json.loads((source/'geometry-verification.json').read_text())
assert prior['checks'] == 'PASS' and prior['plate_solid_count'] == 1
submission = json.loads((R/'output/submission/jlc-quotation-2026-09-15.json').read_text())
sent = next(p for p in submission['parts'] if p['part'] == 'RM10-Q-M01-FACEPLATE')
assert hashlib.sha256((R/sent['archive']).read_bytes()).hexdigest() == sent['sha256']
import zipfile
with zipfile.ZipFile(R/sent['archive']) as archive:
    for ext in ['step', 'dxf']:
        old = source/f'RM10-Q-M01-FACEPLATE.{ext}'
        assert old.read_bytes() == archive.read(old.name)
        shutil.copyfile(old, out/f"{M['part_number']}.{ext}")
corner_report={}
if MANUFACTURING_REVISION=='Q-M03':
    import cadquery as cq
    import ezdxf
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    old=cq.importers.importStep(str(source/'RM10-Q-M01-FACEPLATE.step')).val()
    edges=[e for e in old.Edges() if e.geomType()=='LINE' and abs(e.Length()-2)<1e-6 and abs(abs(e.Center().x)-241.3)<1e-6 and min(abs(e.Center().z),abs(e.Center().z-87))<1e-6]
    assert len(edges)==4
    shape=cq.Workplane(obj=old).newObject(edges).fillet(5).val()
    assert shape.isValid() and len(shape.Solids())==1
    assert shape.cut(old).Volume()<1e-6
    expected=(4-math.pi)*25*2
    assert abs(old.cut(shape).Volume()-expected)<1e-5
    cq.exporters.export(shape,str(out/f"{M['part_number']}.step"))
    cq.exporters.export(shape,str(out/f"{M['part_number']}.stl"),tolerance=.025,angularTolerance=.06)
    dxf=ezdxf.readfile(source/'RM10-Q-M01-FACEPLATE.dxf');ms=dxf.modelspace()
    outer=max(ms.query('LWPOLYLINE'),key=lambda e:max(p[0] for p in e.get_points())-min(p[0] for p in e.get_points()))
    l,r,h,cr=-241.3,241.3,87,5;q=math.tan(math.pi/8)
    outer.set_points([(l+cr,0,0),(r-cr,0,q),(r,cr,0),(r,h-cr,q),(r-cr,h,0),(l+cr,h,q),(l,h-cr,0),(l,cr,q)],format='xyb')
    dxf.saveas(out/f"{M['part_number']}.dxf")
    assert not dxf.audit().has_errors
    cylinders=[]
    for face in shape.Faces():
        if face.geomType()=='CYLINDER':
            c=BRepAdaptor_Surface(face.wrapped).Cylinder();p=c.Location()
            if abs(c.Radius()-5)<1e-6:cylinders.append([p.X(),p.Y(),p.Z()])
    assert len(cylinders)==4
    front=max([f for f in shape.Faces() if f.geomType()=='PLANE' and abs(f.Center().y)<1e-6],key=lambda f:f.Area())
    outer_wire=front.outerWire();inner=[w for w in front.Wires() if not w.isSame(outer_wire)]
    assert len(inner)==44
    min_gap=min(outer_wire.distance(w) for w in inner)
    assert min_gap>1.89
    # Current assembly reference; original submitted single-part body stays unchanged.
    body=cq.importers.importStep(str(source/'RM10-Q-M01-BODY.step')).val()
    screw=cq.importers.importStep(str(R/'output/assembly/Q/REFERENCE-M4x10-ISO7380.step')).val()
    assy=cq.Assembly(name='Q_with_Q_M03_R5_faceplate');assy.add(body,name='POM_Q');assy.add(shape,name='faceplate_Q_M03')
    parent=json.loads((R/'cad/iterations/P-long-bore.json').read_text())
    for i,(x,z) in enumerate(parent['faceplate_mounts_xz']):assy.add(screw.translate((x,-2,z)),name=f'M4_reference_{i+1}')
    assy.export(str(R/'output/assembly/Q/REFERENCE-assembled-with-screws.step'))
    corner_report=dict(outer_corner_radius_mm=5,outer_corner_centres_xyz=cylinders,removed_volume_mm3=expected,
                       minimum_opening_to_outer_profile_mm=min_gap,volume_mm3=shape.Volume(),mass_kg=shape.Volume()*7.9e-6,
                       geometry_change='Only four outer corners rounded R5; all holes/windows/slots unchanged')
features = [f for f in json.loads((source/'feature-schedule.json').read_text())['features'] if f['group'] in 'WHR']
assert len(features) == 44
(out/'feature-schedule.json').write_text(json.dumps({'part_number':M['part_number'], 'features':features}, indent=2)+'\n')
inputs = [R/f'cad/manufacturing/{MANUFACTURING_REVISION}.json', source/'geometry-verification.json', source/'feature-schedule.json']
inputs += [source/f'RM10-Q-M01-FACEPLATE.{ext}' for ext in ['step','dxf']]
report = {'manufacturing_revision':MANUFACTURING_REVISION,'checks':'PASS','nominal_geometry_unchanged':MANUFACTURING_REVISION=='Q-M02',
          'plate_solid_count':1,'extent_mm':prior['plate_extent_mm'],
          'volume_mm3':prior['plate_volume_mm3'],'windows':20,'retention_holes':12,'rack_slots':12,
          'linear_and_coordinate_tolerance_mm':0.1,'POM_M4_coordinate_tolerance_mm':0.05,
          'worst_case_M4_radial_margin_mm':(4.4-4)/2-math.hypot(.15,.15),
          'fit_status':'Operator accepted JLC capability; worst-case interchangeability is not guaranteed',
          'source_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}}
report.update(corner_report)
(out/'geometry-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
