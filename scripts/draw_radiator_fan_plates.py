"""Issue matched R3 tapped / R4 clearance fan plate review drawings."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor,white
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf/radiator-fan-plates-R3-R4.pdf'
c=canvas.Canvas(str(OUT),pagesize=(420*mm,297*mm));c.setTitle('Supernova fan/rack plates R3 and R4')
ink=HexColor('#233748');fill=HexColor('#e9edf0');blue=HexColor('#126182')
def text(x,y,t,size=9,b=False):
 c.setFillColor(ink);c.setFont('Helvetica-Bold' if b else 'Helvetica',size);c.drawString(x*mm,y*mm,t)
def line(x1,y1,x2,y2):
 c.setStrokeColor(ink);c.setLineWidth(.5);c.line(x1*mm,y1*mm,x2*mm,y2*mm)
def lines(x,y,rows,size=9,leading=5.4):
 for i,t in enumerate(rows):text(x,y-i*leading,t,size)
for rev in ['R3','R4']:
 p=json.loads((ROOT/f'cad/radiator/{rev}.json').read_text());v=json.loads((ROOT/f'output/radiator-{rev}/verification.json').read_text())
 tapped=rev=='R3'
 text(17,282,f'SUPERNOVA 1260 / FAN-RACK PLATE {rev}',18,True)
 text(17,273,('M4 tapped alternative' if tapped else 'M4 clearance + nuts alternative')+' | 10U | 304 stainless | 2.00 +/-0.10 mm',11)
 line(17,269,403,269)
 s=.5;ox=140;oy=30
 def xy(x,y):return (ox+x*s)*mm,(oy+y*s)*mm
 def rounded(x,y,w,h,r):
  a,b=xy(x-w/2,y-h/2);c.roundRect(a,b,w*s*mm,h*s*mm,r*s*mm,fill=1)
 c.setFillColor(fill);c.setStrokeColor(ink);rounded(0,p['height']/2,p['width'],p['height'],2);c.setFillColor(white)
 for x in p['aperture_centres_x']:
  for dy in p['aperture_centres_y_from_centre']:rounded(x,p['height']/2+dy,188,188,50)
 for x in p['rack_mount_x']:
  for y in p['rack_mount_y']:rounded(x,y,10,7,3.5)
 for x in p['radiator_mount_x']:
  for dy in p['radiator_mount_y_from_centre']:
   a,b=xy(x,p['height']/2+dy);c.circle(a,b,1.8*s*mm,fill=1)
 for x,y in v['fan_holes']:
  a,b=xy(x,y);c.setStrokeColor(blue);c.circle(a,b,p['fan_mount_diameter']/2*s*mm,fill=1)
  if tapped:c.circle(a,b,2*s*mm,fill=0)
 c.setStrokeColor(ink)
 text(20,257,'FRONT / 1:2 - blue holes are fan mount positions',8)
 line(ox-p['width']/4,22,ox+p['width']/4,22);text(ox-10,24,'482.60',8)
 line(12,oy,12,oy+p['height']/2)
 c.saveState();c.translate(10*mm,(oy+p['height']/4)*mm);c.rotate(90);c.setFont('Helvetica',8);c.drawCentredString(0,0,'444.50 +0 / -0.15');c.restoreState()
 x=278
 text(x,256,'FAN FIXINGS / 16 HOLES',11,True)
 lines(x,248,[('M4 x 0.7 - 6H THROUGH; drill 3.3 nominal.' if tapped else 'Diameter 4.50 +0.15 / 0 THROUGH.'),
 ('STEP/DXF show tap pilots, not plain bores.' if tapped else 'Plain holes. Separate M4 nuts required.'),
 'X = -185, -15, +15, +185.',
 'Y = 37.25, 207.25, 237.25, 407.25.',
 'All 16 Cartesian combinations. No countersinks.',
 'Per-fan pitch 170 x 170; fan centres 200 x 200.'])
 text(x,207,'RADIATOR FIXINGS / 12 HOLES',11,True)
 lines(x,199,['Diameter 3.60 +0.15 / 0 THROUGH.',
 'X = -203.50, +203.50.',
 'Y = 18.75, 143.75, 159.75,',
 '      284.75, 300.75, 425.75.',
 'M3 threads remain in the radiator frame.'])
 text(x,167,'RACK FIXINGS / 40 SLOTS',11,True)
 lines(x,159,['10 x 7 THROUGH, R3.5 ends.',
 'X = -232.55, +232.55.',
 'Y = 44.45 n + 6.35 / 38.10; n = 0...9.',
 'Widths +0.15 / 0; ends remain semicircular.'])
 text(x,132,'PROFILE AND MANUFACTURING',11,True)
 lines(x,124,['4x 188 x 188 apertures with R50 corners.',
 'Centres X +/-100; Y122.25 / 322.25.',
 'Full diameter 188 air opening retained.',
 '12 mm central webs; outer corners R2.',
 'Hole centre coordinates +/-0.10.',
 'Other profile dimensions +/-0.15.',
 'Fan-hole edge break C0.1 maximum.',
 'Other cut edges: deburr 0.2-0.3.',
 'Flatness target 0.5 over the free plate.',
 'Satin finish; no surface markings.'])
 text(x,61,'ASSEMBLY / SEE SHEET 3',11,True)
 lines(x,53,['Origin: X midplane; Y bottom of plate.',
 'Depth is perpendicular to this elevation.',
 'Mass '+f'{v["plate_mass_kg"]:.3f}'+' kg; fan/cooler parts separate.',
 'Outer rack rows: head/washer OD <=12.',
 'Full nominal 10U height has no panel gap.'])
 text(18,12,f'{rev} | Sheet {1 if tapped else 2} of 3 | 15 September 2026 | Prototype review; not an assembly load rating | Units: mm',8)
 c.showPage()
text(17,282,'FAN FASTENER STACK / ALTERNATIVE COMPARISON',18,True)
text(17,272,'Four NF-A20 fans on the custom plate; opposite fan bank uses the retained Alphacool fan plate.',11)
line(17,265,403,265)
text(18,251,'R3 / TAPPED M4',13,True);text(215,251,'R4 / PLAIN BORES + NUTS',13,True)
lines(18,240,['16x M4 x 35 ISO 7380-1 button socket screws.',
 '16x M4 flat washers, OD9 x ID4.3 x 0.8.',
 'Nominal straight thread after edge breaks: 1.8 mm.',
 'Minimum at 1.9 mm sheet: 1.7 mm = 2.43 pitches.',
 'No proven tightening torque or strip-load rating.',
 'Check repeated assembly; avoid overtightening.'],10,7)
lines(215,240,['16x M4 x 40 ISO 7380-1 button socket screws.',
 '16x DIN 934 M4 nuts, AF7, height 3.2.',
 '32x M4 flat washers, OD9 x ID4.3 x 0.8.',
 'Rear button head + washer occupy 3.0 mm.',
 'Head nominally 3.5 mm short of the core.',
 'Recommended prototype: threads are replaceable.'],10,7)
# Side-section stack diagram, proportions shown in depth only.
text(18,185,'R4 DEPTH STACK / SCHEMATIC, NOMINAL VALUES',12,True)
x0=52;scale=6;yy=141
for start,end,label,col in [(-38,-34.8,'Outer nut','#8ca0ae'),(-34.8,-34,'Outer washer','#d4dce1'),(-34,-2,'Fan, pads included: 32','#dfceb9'),(-2,0,'Plate: 2','#aebbc3'),(0,.8,'Rear washer','#d4dce1'),(.8,3,'Button head','#8ca0ae')]:
 c.setFillColor(HexColor(col));c.rect((x0+(start+35)*scale)*mm,(yy-10)*mm,(end-start)*scale*mm,20*mm,fill=1)
for depth,label,ty in [(-39.2,'Tip -39.2',103),(-38,'Nut -38',113),(-34,'Fan -34',123),(-2,'-2',116),(0,'0',108),(3,'Head 3.0',120),(6.5,'Core 6.5',110)]:
 xx=x0+(depth+35)*scale;line(xx,yy-13,xx,ty+4);text(xx-3,ty,label,8)
xx=x0+(6.5+35)*scale;c.setFillColor(HexColor('#26343c'));c.rect(xx*mm,(yy-18)*mm,7*mm,36*mm,fill=1)
line(x0+(-39.2+35)*scale,yy,x0+(.8+35)*scale,yy)
text(55,163,'Outer nut',9);text(120,163,'32 mm fan',10);text(248,164,'Plate',9);text(272,177,'Head + washer: 3 mm',9)
text(18,87,'FIT AND ASSEMBLY REQUIREMENTS',12,True)
lines(18,78,[
 'Nominal core setback: 6.5 mm. R4 rear button head + washer: 3.0 mm. Nominal gap: 3.5 mm.',
 'R4 screws enter from the core side; nuts sit on the outer fan face. Screw tips point away from the core.',
 'Hold each rear hex socket while tightening its front nut. Assemble fans before fitting the plate to the radiator.',
 'Radiator M3 heads: OD <=5.6, height <=2.4, no washers. Confirm thread reach and allowable depth in the actual frame.',
 'Turn right-hand fans 180 degrees about their airflow axes, keeping cable exits inward. Front airflow into radiator for push.',
 'Fan frames nominally touch at 200 mm centres. Noctua specifies dimensional tolerances: verify all four fans on a first article.',
 'Reference CAD checks do not certify tolerance extremes, fastener loosening, core clearance under load or fan noise/airflow.'
],9,6)
text(18,22,'References: official Noctua NF-A20 CAD and specification; Alphacool 14351 catalogue mesh. See accompanying source and analysis notes.',8)
text(18,12,'R3 / R4 | Sheet 3 of 3 | Prototype integration review | No supplier submission | Units: mm',8)
c.save();print(OUT)
