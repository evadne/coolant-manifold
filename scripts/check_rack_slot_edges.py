"""Assess K rack slots and a middle-hole alternative; do not modify CAD."""
import json
from pathlib import Path
import cadquery as cq
import ezdxf
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/rack-slot-review'
p=json.loads((ROOT/'cad/iterations/K-long-bore.json').read_text());H=p['body_height'];offset=(88.9-H)/2
old=[6.35-offset,82.55-offset];new=[22.225-offset,66.675-offset]
d=ezdxf.readfile(ROOT/'output/long-bore-K/cad/faceplate-flat.dxf')
slots=[]
for e in d.modelspace().query('LWPOLYLINE'):
 xy=list(e.get_points('xy'));zmin=min(v[1] for v in xy);zmax=max(v[1] for v in xy)
 if abs(zmax-zmin-7)<1e-6:
  slots.append({'centre_x':sum(v[0] for v in xy)/4,'centre_z':(zmin+zmax)/2,'top_bottom_edge_ligament_mm':min(zmin,H-zmax)})
assert len(slots)==4 and all(abs(x['top_bottom_edge_ligament_mm']-1.9)<1e-6 for x in slots)
assy=cq.importers.importStep(str(ROOT/'output/long-bore-K/cad/elbow-envelope-assembly.step')).val()
fits=[s for s in assy.Solids() if s.BoundingBox().xmin>204 or s.BoundingBox().xmax<-204];assert len(fits)==4
nuts=[cq.Workplane('XY').box(10,6,10).translate((x,6,z)).val() for x in [-232.55,232.55] for z in new]
gap=min(f.distance(n) for f in fits for n in nuts);assert gap>0
report={'revision_checked':'K','plate_height_mm':H,'plate_thickness_mm':3,'rack_slots':slots,'slot_size_mm':[10,7],'current_centres_z_mm':old,'current_minimum_vertical_edge_ligament_mm':1.9,'current_side_edge_ligament_mm':p['rack_width']/2-p['rack_hole_pitch']/2-5,'washer_reference':{'manufacturer':'Penn Elcom','part':'S1940','outer_diameter_mm':15,'url':'https://www.penn-elcom.com/slim-m6-black-plastic-cup-washer-s1940','current_panel_overhang_mm':7.5-old[0],'nominal_overlap_of_two_identical_washers_across_adjacent_U_boundary_mm':15-12.7},'alternative_middle_holes':{'centres_z_mm':new,'vertical_bolt_spacing_mm':new[1]-new[0],'vertical_slot_edge_ligament_mm':new[0]-3.5,'washer_to_vertical_panel_edge_mm':new[0]-7.5,'minimum_new_corner_nut_to_K_elbow_reference_mm':gap},'status':'Assessment only; existing K CAD unchanged. Edge/washer issue confirmed; no structural failure load inferred. Alternative nuts use illustrative 10x6x10 envelopes at Y6; actual clips and screw tails require checking.'}
(OUT/'assessment.json').write_text(json.dumps(report,indent=2)+'\n')
# Comparison of the right-hand panel end, with washer envelopes on the front face.
a=['<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="720" viewBox="0 0 1320 720"><rect width="1320" height="720" fill="white"/><g font-family="Arial,sans-serif" fill="#233746">']
def text(x,y,t,size=20):a.append(f'<text x="{x}" y="{y}" font-size="{size}">{t}</text>')
text(50,48,'RACK SLOT EDGE REVIEW — 87 mm faceplate',29)
text(50,82,'Right-hand end, front elevation. Orange circles: Ø15 mm washer envelopes.',19)
for x0,zs,title in [(180,old,'Current outer holes'),(770,new,'Middle-hole alternative')]:
 s=5.;y0=175.;xx=x0+26.25*s
 text(x0-60,135,title,24)
 a.append(f'<rect x="{x0}" y="{y0}" width="{35*s}" height="{87*s}" fill="#dbe3e8" stroke="#36505f"/>')
 for z in zs:
  yy=y0+(87-z)*s
  a.append(f'<circle cx="{xx}" cy="{yy}" r="{7.5*s}" fill="none" stroke="#bb642c" stroke-width="2"/>')
  a.append(f'<rect x="{xx-5*s}" y="{yy-3.5*s}" width="{10*s}" height="{7*s}" rx="{3.5*s}" fill="white" stroke="#233746"/>')
  a.append(f'<path d="M{xx-8},{yy}h16 M{xx},{yy-8}v16" stroke="#637983" fill="none"/>')
 if zs==old:
  text(x0+200,215,'1.9 mm edge ligament',19);text(x0+200,250,'2.1 mm washer overhang',18)
 else:
  text(x0+200,280,'17.775 mm edge ligament',19);text(x0+200,315,'Washer within panel',18)
text(50,661,'Both use existing holes on a universal three-hole-per-U rail. Alternative not applied to CAD.',19)
text(50,695,'Source: K DXF; rack-hole pattern and washer dimensions checked against manufacturer documentation.',17)
a.append('</g></svg>');(OUT/'comparison.svg').write_text('\n'.join(a)+'\n')
print(json.dumps(report,indent=2))
