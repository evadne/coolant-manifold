"""Two-sheet revision P review drawing; no change to O-M02 supplier revision."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor,white
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'cad/iterations/P-long-bore.json').read_text())
out=ROOT/'output/pdf/manifold-revision-P.pdf';out.parent.mkdir(exist_ok=True)
c=canvas.Canvas(str(out),pagesize=(420*mm,297*mm));c.setTitle('Manifold revision P - plain-bore faceplate and revised body')
ink=HexColor('#233748');fill=HexColor('#e9edf0')
def txt(x,y,t,size=10,b=False):
 c.setFillColor(ink);c.setFont('Helvetica-Bold' if b else 'Helvetica',size);c.drawString(x*mm,y*mm,t)
def line(x1,y1,x2,y2):
 c.setStrokeColor(ink);c.setLineWidth(.5);c.line(x1*mm,y1*mm,x2*mm,y2*mm)
def dim(x1,y1,x2,y2,label):
 line(x1,y1,x2,y2)
 for x,y in [(x1,y1),(x2,y2)]:line(x-1,y-1,x+1,y+1)
 if x1==x2:
  c.saveState();c.translate((x1-2)*mm,(y1+y2)/2*mm);c.rotate(90);c.setFont('Helvetica',8);c.drawCentredString(0,0,label);c.restoreState()
 else:txt((x1+x2)/2-7,(y1+y2)/2+2,label,8)
def header(n,label):
 txt(18,280,'RM10 / REVISION P',19,True);txt(18,271,label,11);line(18,266,402,266)
 txt(18,12,'15 September 2026 | All dimensions mm | Review variation - not a released pressure-rated design',8)
 txt(367,12,f'Sheet {n} / 2',8)
def front(body=False):
 s=.75;ox=210;oy=183;W=410 if body else 482.6
 def q(x,z):return ((ox+x*s)*mm,(oy+z*s)*mm)
 c.setStrokeColor(ink);c.setFillColor(fill);a,b=q(-W/2,0);c.rect(a,b,W*s*mm,87*s*mm,fill=1)
 for z in p['port_rows_z']:
  for x in [-180+40*i for i in range(10)]:
   a,b=q(x,z);c.setFillColor(white);c.circle(a,b,(14 if body else 16)*s*mm,fill=1)
   if body:c.circle(a,b,5.9*s*mm);c.circle(a,b,6.9*s*mm)
 for x,z in p['faceplate_mounts_xz']:
  a,b=q(x,z);c.setFillColor(white);c.circle(a,b,(1.65 if body else 2.25)*s*mm,fill=1)
 if not body:
  for x in [-232.55,232.55]:
   for z in p['rack_slot_centres_z']:
    a,b=q(x-5,z-3.5);c.roundRect(a,b,10*s*mm,7*s*mm,3.5*s*mm,fill=1)
 dim(ox-W*s/2,176,ox+W*s/2,176,f'{W:.2f}')
 dim(ox-W*s/2-8,oy,ox-W*s/2-8,oy+87*s,'87.00')
 txt(ox-W*s/2,255,'FRONT ELEVATION / scale 3:4',9,True)
 return q
header(1,'FACEPLATE / 304 stainless steel / 2.00 +/-0.10 thick / no countersinks, no tapped holes')
front()
txt(18,157,'HOLE AND WINDOW SCHEDULE',12,True)
rows=[('20 port windows','Diameter 32.00 +0.10/0 THROUGH','X = -180 to +180 in 40 increments; Z = 23.50, 63.50'),
('12 body fixings','Diameter 4.50 +0.10/0 THROUGH','X = -198, -120, -40, +40, +120, +198; Z = 7.00, 80.00'),
('12 rack positions','10.00 x 7.00 horizontal slots, R3.50 ends','X = -232.55, +232.55; Z = 5.40, 21.275, 37.15, 49.85, 65.725, 81.60')]
for i,(name,spec,pos) in enumerate(rows):
 y=143-i*22;txt(18,y,name,10,True);txt(63,y,spec,10);txt(63,y-7,pos,9)
txt(18,65,'MANUFACTURING AND ASSEMBLY',12,True)
notes=['Coordinates: signed X from width midplane; Z from bottom edge; rear mating plane Y = 0.',
'Unless specified: linear dimensions +/-0.10; hole-centre coordinates +/-0.10. No surface markings.',
'External deburr only: light edge break 0.10-0.20 maximum; keep the screw bearing faces flat.',
'Fit 12 x M4 x 16 ISO 7380-1 button-head screws, A2 stainless, Westfield WF2237; no washers in reference assembly.',
'Other plain-bearing M4 heads require a clearance/length check. Countersunk screws are incompatible.',
'Rack slots accept separately selected rack screws/cage nuts. Optional positions do not imply 12 installed rack screws.']
for i,n in enumerate(notes):txt(18,55-i*6,n,9)
c.showPage()
header(2,'POM BODY / black unfilled declared POM-C or POM-H / 410 x 87 x 40 slab + 3 mm bosses')
front(True)
txt(18,158,'FRONT / SIDE MACHINING',12,True)
notes=[
'20 FRONT: G 1/4 female, ISO 228-1; full thread 8 minimum after the 1 mm entry chamfer.',
'Port centres X = -180 to +180 in 40 increments; Z = 23.50 / 63.50. Entry diameter 13.80 to 11.80, depth 1, 45 degrees.',
'Front pilot: diameter 11.80, 23.00 full diameter from boss face to Y20, plus 118-degree drill point.',
'20 bosses: diameter 28.00 +/-0.10; height 3.00 +/-0.05 from Y0; root R1.00; outer lip C0.50 x 45 degrees.',
'Two longitudinal galleries: diameter 11.80 THROUGH across 410 width; axes Y20, Z23.50 / 63.50.',
'4 SIDE: G 1/4 female at X+/-205, Y20, Z23.50 / 63.50; full thread 8 minimum after entry; entry as front ports.',
'12 FIXINGS: M4 x 0.7 - 6H; 16 minimum full-form thread after entry. Diameter 3.30 pilot x 18 full diameter from Y0.',
'M4 entry: diameter 4.40 to 3.30, 0.55 deep x 45 degrees. Drill point 118 degrees; total pilot depth 18.99 nominal.',
'Fixing centres match plate: X = -198, -120, -40, +40, +120, +198; Z = 7.00 / 80.00.',
'16 mm under-head screws through 2 mm plate reach 14 mm into the POM. Do not reuse the old 14 mm pilot depth.'
]
for i,n in enumerate(notes):txt(18,147-i*7,n,9)
txt(18,65,'SEALING, FINISH AND REVIEW SCOPE',12,True)
notes=[
'Flat fitting seal lands on boss ends and side faces; retain O-M02 surface requirements: refer to that revision for finish details.',
'External deburr only; no internal/cross-hole deburring operation. Clean and flush out all loose swarf.',
'No rear plate or perimeter seals. End plugs/fittings require their own face seals. Two independent continuous galleries.',
'G1/4 and M4 threads are pilot representations in STEP, not plain finished holes. Tap to the drawing call-outs.',
'General linear and coordinate tolerance +/-0.10 unless stated. Gallery drilling, material grade and thread process require vendor review.',
'Separate variation: O-M02 is preserved. Drawing is for design review; refresh the supplier package if P is selected.'
]
for i,n in enumerate(notes):txt(18,55-i*6,n,9)
c.save();print(out)
