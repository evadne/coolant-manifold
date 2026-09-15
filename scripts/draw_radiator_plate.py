"""Draw R1 with ReportLab; use the bundled document Python runtime."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'cad/radiator/R1.json').read_text())
V=json.loads((ROOT/'output/radiator-R1/verification.json').read_text())
OUT=ROOT/'output/pdf/radiator-rack-plate-R1.pdf'
c=canvas.Canvas(str(OUT),pagesize=(420*mm,297*mm))
c.setTitle('R1 - SuperNova 1260 rack plate - prototype drawing')
ink=HexColor('#172c38'); pale=HexColor('#edf1f3')
def text(x,y,t,size=9,bold=False):
 c.setFillColor(ink); c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x*mm,y*mm,t)
def line(x1,y1,x2,y2): c.setStrokeColor(ink);c.setLineWidth(.5);c.line(x1*mm,y1*mm,x2*mm,y2*mm)
def title(n,sub):
 text(16,281,'SUPERNOVA 1260 / RACK PLATE R1',18,True)
 text(16,273,sub,10);line(16,269,404,269)
 text(16,10,'R1 | 15 September 2026 | Prototype review - interface verification required before fabrication',8)
 text(372,10,f'Sheet {n} of 2',8)
def dim(x1,y1,x2,y2,label):
 line(x1,y1,x2,y2)
 for x,y in ((x1,y1),(x2,y2)):line(x-1,y-1,x+1,y+1)
 if x1==x2:
  c.saveState();c.translate((x1-2)*mm,(y1+y2)/2*mm);c.rotate(90)
  c.setFont('Helvetica',8);c.drawCentredString(0,0,label);c.restoreState()
 else: text((x1+x2)/2+1,(y1+y2)/2+2,label,8)
title(1,'304 / EN 1.4301 stainless steel | 3.00 mm sheet | Flat part, no bends | All dimensions in mm')
s=.5; ox=139; oy=33; W=P['width'];H=P['height']
def point(x,y): return (ox+x*s)*mm,(oy+y*s)*mm
def rounded(x,y,w,h,r):
 a,b=point(x-w/2,y-h/2);c.roundRect(a,b,w*s*mm,h*s*mm,r*s*mm,stroke=1,fill=1)
c.setStrokeColor(ink);c.setLineWidth(.6);c.setFillColor(pale)
rounded(0,H/2,W,H,P['outer_radius'])
c.setFillColor(white)
for x in P['aperture_centres_x']:
 for dy in P['aperture_centres_y_from_centre']:rounded(x,H/2+dy,188,188,8)
for x in P['radiator_mount_x']:
 for dy in P['radiator_mount_y_from_centre']:
  a,b=point(x,H/2+dy);c.circle(a,b,1.8*s*mm,stroke=1,fill=1)
for x in P['rack_mount_x']:
 for y in P['rack_mount_y']:rounded(x,y,10,7,3.5)
# Datum and centre lines exist on drawing only.
c.setDash(3,2);a,b=point(0,0);aa,bb=point(0,H);c.line(a,b,aa,bb)
a,b=point(-W/2,H/2);aa,bb=point(W/2,H/2);c.line(a,b,aa,bb);c.setDash()
dim(ox-W/4,23,ox+W/4,23,'482.60')
dim(12,oy,12,oy+H*s,'442.60')
text(103,258,'FRONT VIEW - scale 1:2',10,True)
text(20,17,'Origin: X=0 on vertical centreline; Y=0 at bottom edge.',8)
text(43,oy+H/4+30,'4x 188 x 188, R8 corners',9,True)
text(43,oy+H/4+25,'Opening centres: X +/-100; Y 121.30 / 321.30',8)
text(166,oy+H/4+30,'12 mm central webs',9)
text(279,255,'A / RADIATOR ATTACHMENT',11,True)
text(279,248,'12x diameter 3.60 THROUGH; no countersinks.',9)
text(279,242,'Two columns: X = -203.50 and +203.50.',9)
text(279,236,'Each column uses these Y coordinates:',9)
for i,dy in enumerate(P['radiator_mount_y_from_centre']):text(285,228-6*i,f'A{i+1}    {H/2+dy:.3f}',9)
text(279,186,'B / RACK FIXINGS',11,True)
text(279,179,'12x horizontal slots, 10.00 x 7.00, R3.50 ends.',9)
text(279,173,'Two columns: X = -232.55 and +232.55.',9)
text(279,167,'Each column uses these Y coordinates:',9)
for i,y in enumerate(P['rack_mount_y']):text(285,159-6*i,f'B{i+1}    {y:.3f}',9)
text(279,116,'C / OUTLINE AND SECTION',11,True)
text(279,109,'4x outer corners R2.00. Thickness 3.00 +/-0.10.',9)
text(279,103,'No tapped holes. All cuts pass through the plate.',9)
text(279,97,'Sheet flatness: 0.5 mm overall target.',9)
text(279,91,'Profile / hole centre dimensions: +/-0.15 mm.',9)
text(279,85,'Hole / slot widths: +0.15 / 0 mm.',9)
text(279,79,'Deburr both faces and all cut edges, 0.2-0.3 mm.',9)
text(279,73,'Satin finish; no markings on the finished part.',9)
text(279,60,'RADIATOR DATUM',11,True)
text(279,53,'422 x 441 body centred at X=0, Y=221.30.',9)
text(279,47,'Stock mesh centre: X=0, Z=212.00.',9)
text(279,41,'Transform: plate Y = mesh Z + 9.30.',9)
text(279,35,'Ports face top or bottom. Fittings not in envelope.',9)
text(279,25,'Matching STEP and cut-only DXF: output/radiator-R1/',8)
c.showPage()
title(2,'Load estimate, assembly intent and interface verification | R1 prototype design')
text(18,252,'WEIGHT AND STATIC LOAD',13,True)
rows=[('Published radiator net weight','4.225 kg'),('Operator allowance','2.000 kg'),
      ('Load carried by radiator attachment screws',f'{V["radiator_plus_allowance_kg"]:.3f} kg / {V["payload_force_N"]:.1f} N'),
      ('New plate, CAD volume x 7900 kg/m3',f'{V["plate_mass_kg"]:.3f} kg'),
      ('Total estimated rack load',f'{V["total_rack_mass_kg"]:.3f} kg / {V["total_rack_force_N"]:.1f} N')]
for i,(a,b) in enumerate(rows):text(18,240-10*i,a,10);text(135,240-10*i,b,10,True)
text(18,184,'No credit is taken for removing the original front fan plate.',9)
text(18,178,'The 2 kg is a combined allowance, not a measured coolant/fan BOM.',9)
text(18,172,'Additional hardware or a pump/reservoir beyond that allowance adds load.',9)
text(18,158,'STATIC REACTION SCREEN - NOT A LOAD RATING',11,True)
for i,t in enumerate([
 f'Payload centre of gravity assumed 75 mm behind the rack plate.',
 f'Payload overturning moment: {V["eccentric_payload_moment_Nm"]:.2f} Nm.',
 f'Four outermost rack screws: average vertical shear {V["four_corner_rack_screws_average_shear_N"]:.1f} N each.',
 f'Top rack-screw pair total tension from moment: {V["four_corner_rack_screws_top_pair_total_tension_N"]:.1f} N.',
 f'Twelve radiator screws: average vertical shear {V["twelve_radiator_screws_average_shear_N"]:.1f} N each.',
 'These averages assume symmetric sharing; clearance holes may share unevenly.',
 'Doubling 1.5 to 3 mm gives 8x bending stiffness for an identical plate profile.',
 'This does not establish assembly deflection, pull-out strength or shock resistance.'
]):text(18,148-7*i,t,9)
text(18,78,'GEOMETRY CHECKS',11,True)
for i,t in enumerate([
 'One valid solid; STEP re-import volume and extents checked.',
 'DXF: 1 outline + 4 openings + 12 slots + 12 holes; closed cut contours.',
 f'Plate airflow opening area: {V["airflow_aperture_area_mm2"]:.0f} mm2; 88.2% of a 400 mm square.',
 'Minimum straight hole-to-air-opening ligament: 7.7 mm.',
 'Rack slot to outer plate edge: 3.75 mm; use flat washers.',
 '12 attachment centres cross-checked against the manufacturer STL pilots.'
]):text(18,68-7*i,t,9)
text(222,252,'ASSEMBLY',13,True)
for i,t in enumerate([
 'Replace the front fan plate with R1; retain the opposite fan plate.',
 'Four 200 mm rear fans shown in the review model; nine 140 mm',
 'fans remain an option with the matching opposite plate.',
 'Use all 12 radiator retention points. A4 M3 pan-head screws',
 'and suitable flat washers; maximum washer OD 7 mm.',
 'Starting candidate: M3 x 6, giving 3 mm reach before a washer.',
 'Confirm actual required engagement and safe depth before use.',
 'Do not use the supplied M3 x 30 fan screws on the bare plate.',
 'Rack: M6 screws / cage nuts where compatible with actual rails.',
 'Proposed installation: 4 per side, rows B1/B3/B4/B6.',
 'B2/B5 are additional optional rack fixing positions.',
 'The static screen conservatively uses only four corner screws.'
]):text(222,240-7*i,t,9)
text(222,145,'CHECK BEFORE FABRICATION / INSTALLATION',11,True)
for i,t in enumerate([
 'Confirm manufacturer revision, mounting pattern and seating faces.',
 'The catalogue mesh is corroboration, not a toleranced interface drawing.',
 'Apertures remove fan-only holes; actual structural side mounts remain.',
 'Check 3 mm plate flatness and contact against the radiator side rails.',
 'Verify the thin radiator rails/inserts can carry the intended rack load.',
 'Review top/bottom elbows against host/base and plate edge.',
 'No wet joint, radiator pressure boundary or manifold part is modified.'
]):text(222,135-7*i,t,9)
text(222,76,'SOURCE REFERENCES',11,True)
text(222,66,'Alphacool 14351 datasheet v1.007, 03.2026, pp2 and 4-6.',9)
text(222,60,'Alphacool 3D Centre: 14351_0.stl (checked 15 September 2026).',9)
text(222,54,'Outokumpu Core range: 304 density 7.9 kg/dm3, E = 200 GPa.',9)
text(222,44,'Full URLs, mesh hash and calculations accompany the CAD package.',9)
c.save()
print(OUT)
