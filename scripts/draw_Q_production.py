"""Self-contained A3 supplier drawings for Q-M01, mm, tap-pilot STEP convention."""
from pathlib import Path
import json,math,argparse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib import colors
R=Path(__file__).resolve().parents[1];OUT=R/'output/pdf';OUT.mkdir(exist_ok=True)
S=json.loads((R/'output/manufacturing/Q-M01/feature-schedule.json').read_text())['features']
M=json.loads((R/'cad/manufacturing/Q-M01.json').read_text())
parser=argparse.ArgumentParser();parser.add_argument('--faceplate-issue',choices=['Q-M01','Q-M02'],default='Q-M01');parser.add_argument('--faceplate-only',action='store_true')
ARGS=parser.parse_args();FI=ARGS.faceplate_issue
FM=json.loads((R/f'cad/manufacturing/{FI}.json').read_text())
SIZE_TOL='±0.10' if FI=='Q-M02' else '+0.10/0'
CENTRE_TOL='±0.10' if FI=='Q-M02' else '±0.05'
pdfmetrics.registerFont(TTFont('Arial','/System/Library/Fonts/Supplemental/Arial.ttf'));pdfmetrics.registerFont(TTFont('Arial-Bold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
ink=colors.HexColor('#183342');grey=colors.HexColor('#e8eef1')
def t(x,y,v,size=2.7,b=False):
 c.setFillColor(ink);c.setFont('Arial-Bold' if b else 'Arial',size*mm);c.drawString(x*mm,y*mm,str(v))
def ln(x,y,xx,yy,w=.18):
 c.setStrokeColor(ink);c.setLineWidth(w*mm);c.line(x*mm,y*mm,xx*mm,yy*mm)
def rect(x,y,w,h,fill=False):
 c.setStrokeColor(ink);c.setFillColor(grey);c.setLineWidth(.18*mm);c.rect(x*mm,y*mm,w*mm,h*mm,fill=int(fill))
def circle(x,y,r,fill=False):
 c.setStrokeColor(ink);c.setFillColor(colors.white);c.circle(x*mm,y*mm,r*mm,fill=int(fill))
def lines(x,y,items,step=5.3,size=2.7):
 for i,v in enumerate(items):t(x,y-i*step,v,size)
def arrow(x,y,d):
 ln(x,y,x+d*1.6,y+.5);ln(x,y,x+d*1.6,y-.5)
def dh(x1,x2,y,label):
 ln(x1,y,x2,y);arrow(x1,y,1);arrow(x2,y,-1);t((x1+x2)/2-len(label)*.62,y+2,label,2.5)
def dv(x,y1,y2,label):
 ln(x,y1,x,y2);ln(x-1,y1,x+1,y1);ln(x-1,y2,x+1,y2)
 c.saveState();c.translate((x-2)*mm,(y1+y2)/2*mm);c.rotate(90);t(0,0,label,2.5);c.restoreState()
def page(n,total,title,material):
 rect(10,10,400,277);t(15,279,stem,5,True);t(15,270,title,3.2);ln(10,265,410,265)
 ln(10,30,410,30);t(15,23,material,2.8,True);t(15,16,(FI+' | 16 September 2026' if stem=='RM10-Q-M02-FACEPLATE' else 'Q-M01 | 15 September 2026')+' | Units mm | Dimensions at 20°C | Do not scale',2.5)
 t(308,23,'SUPPLIER MANUFACTURING REVIEW',2.7,True);t(350,16,f'SHEET {n} / {total}',2.8)
def table(x,y,headers,rows,widths):
 total=sum(widths);rh=5.8;rect(x,y-rh,total,rh,True)
 for i,row in enumerate([headers]+rows):
  yy=y-(i+1)*rh;xx=x
  for v,w in zip(row,widths):t(xx+1.3,yy+1.8,v,2.45,i==0);xx+=w
  ln(x,yy,x+total,yy,.1)
 for xx in [x]+[x+sum(widths[:i]) for i in range(1,len(widths)+1)]:ln(xx,y,xx,y-(len(rows)+1)*rh,.1)
def group(g):return [v for v in S if v['group']==g]
def elevation(kind,ox,oy,scale,labels=True):
 width=482.6 if kind=='plate' else 410;rev=kind=='rear'
 def p(x,z):return ox+(-x if rev else x)*scale,oy+z*scale
 rect(ox-width*scale/2,oy,width*scale,87*scale,True)
 gs=['W','H','R'] if kind=='plate' else ['B'] if rev else ['P','F']
 for g in gs:
  for row in group(g):
   x,y,z=row['xyz_mm'];xx,yy=p(x,z)
   if g=='R':
    c.setFillColor(colors.white);c.roundRect((xx-5*scale)*mm,(yy-3.5*scale)*mm,10*scale*mm,7*scale*mm,3.5*scale*mm,fill=1)
   else:
    radius={'W':16,'H':2.25,'P':14,'B':6.9,'F':2.2}[g];circle(xx,yy,radius*scale,True)
    if g=='P':circle(xx,yy,6.9*scale);circle(xx,yy,5.9*scale)
    if g=='B':
     c.setDash([2,1]);circle(xx,yy,14*scale);c.setDash()
   if labels:
    if g=='R':t(xx+10*scale,yy-.8,row['id'],2)
    else:t(xx+1.4,yy+(4 if g in ['F','H'] else 18 if g=='W' else 16)*scale,row['id'],2)
 dh(ox-width*scale/2,ox+width*scale/2,oy-8,f'{width:.2f} ±0.10')
 dv(ox-width*scale/2-7,oy,oy+87*scale,'87.00 ±0.10')
 return p
# FACEPLATE
stem=f'RM10-{FI}-FACEPLATE';c=canvas.Canvas(str(OUT/f'{stem}.pdf'),pagesize=(420*mm,297*mm));c.setTitle(stem)
page(1,2,'Flat rack faceplate - through features and finish','304 / EN 1.4301 stainless steel | 2.00 ±0.10 thick')
elevation('plate',211,166,.75)
t(25,251,'FRONT VIEW 3:4 - SAME COORDINATES AS BODY FRONT',2.7,True)
t(25,149,'RAW STAINLESS SHEET FINISH - BOTH broad faces; no brushing or polishing.',2.9,True)
lines(22,132,[f'W01-W20: 20x Ø32.00 {SIZE_TOL} THROUGH port windows.',
f'H01-H12: 12x Ø4.50 {SIZE_TOL} THROUGH M4 retention holes.',
f'R01-R12: 12x horizontal 10.00 ±0.10 ×7.00 {SIZE_TOL} THROUGH slots; R3.50 REF ends.',
'NO TAPPED HOLES. NO COUNTERSINKS. Flat plate; all openings through.',
'Coordinate origin: X0 derived width midplane, Z0 bottom edge; POM mating plane A at Y0.',
'Sheet occupies Y-2 to Y0. All feature axes normal to the broad faces; coordinate schedule on sheet 2.',
'Free-state flatness of mating plane A: 0.30 maximum. Dimensions apply after finishing.',
('Standard grinding and deburring on both faces; no specified chamfer or edge-round size.' if FI=='Q-M02' else 'External deburr / edge break 0.10-0.20 max, both faces; maintain flat screw bearing seats.'),
('Complete burr removal is not guaranteed. Nominal STEP/DXF profile has no face-edge breaks.' if FI=='Q-M02' else 'Edge breaks are finishing operations; nominal STEP/DXF cut profile has no face-edge breaks.'),
'Laser-cut profile/windows/slots; drill or finish holes where required to achieve call-outs.',
'No brushing, polishing, coating, paint, engraving, printing or other product markings.',
('All non-reference cut dimensions and X/Z coordinates: ±0.10 mm; flatness specified separately.' if FI=='Q-M02' else 'General DIN ISO 2768-1 class m; H centres ±0.05; other centres ±0.10; specific limits override.'),
'H01-H12: finished plain bores; preserve the specified full through diameter.',
('Inspect sizes, coordinates, thickness and free-state flatness against this drawing.' if FI=='Q-M02' else 'Supplier must confirm unilateral hole sizes, flatness and specified edge finish before fabrication.')],step=6,size=2.8)
c.showPage();page(2,2,'Coordinate schedules - all 44 through openings','304 / EN 1.4301 stainless steel | 2.00 ±0.10 thick')
for x,g,title in [(18,'W','PORT WINDOWS'),(152,'H','BODY RETENTION'),(280,'R','OPTIONAL RACK SLOTS')]:
 t(x,254,title,3.2,True);table(x,247,['ID','X','Z'],[[v['id'],f"{v['xyz_mm'][0]:.3f}",f"{v['xyz_mm'][2]:.3f}"] for v in group(g)],[29,43,43])
lines(18,109,[f'W diameter Ø32.00 {SIZE_TOL}; H diameter Ø4.50 {SIZE_TOL}; R dimensions 10.00 ±0.10 ×7.00 {SIZE_TOL}.',
f'H01-H12 X/Z coordinates {CENTRE_TOL}; W/R coordinates ±0.10 from the stated origin. Do not accumulate chained pitch errors.',
'Port pitch 40.00 REF horizontally and vertically. Rack column pitch 465.10 REF.',
'Raw stainless sheet finish on both broad faces. No brushing, polishing or surface markings.'],step=7,size=2.8)
c.save()
if ARGS.faceplate_only:
 print(FI+': 2 faceplate sheets written; body files untouched');raise SystemExit(0)
# BODY
stem='RM10-Q-M01-BODY';c=canvas.Canvas(str(OUT/f'{stem}.pdf'),pagesize=(420*mm,297*mm));c.setTitle(stem)
material='Black unfilled POM-C or POM-H | Declare grade and machining-stock datasheet'
page(1,3,'Front elevation and front-hole coordinates',material)
elevation('front',210,181,.8);t(46,256,'FRONT VIEW 4:5 - VIEW ALONG +Y',2.7,True)
t(20,163,'P01-P20: G 1/4 FEMALE; integral bosses Ø28 ±0.10 ×3.00 ±0.05 high.',3,True)
t(20,155,'F01-F12: M4 ×0.7 - 6H; 10 MIN full thread after entry; Ø3.30 pilot ×13.00 full depth.',2.9,True)
for x,g,cols in [(18,'P',group('P')[:10]),(145,'P',group('P')[10:]),(272,'F',group('F'))]:
 table(x,145,['ID','X','Z'],[[v['id'],f"{v['xyz_mm'][0]:.3f}",f"{v['xyz_mm'][2]:.3f}"] for v in cols],[27,44,44])
lines(18,61,['Datum A: front mounting plane Y0; flatness 0.15. Datum B: width midplane X0. Datum C: bottom Z0.',
'Front boss sealing faces Y-3.00; rear face Y40.00. Slab 40.00 ±0.10; overall depth 43.00 REF.',
'F01-F12 X/Z ±0.05; port coordinates ±0.10. Root R1.00 ±0.10; outer boss lip C0.50 ±0.10 ×45° ±1°.',
'20 front +4 side +4 rear =28 G1/4 ports. Threads are pilot representations in STEP; tap per sheet 3.'],step=6,size=2.8)
c.showPage();page(2,3,'Rear and end ports - alignment to the same two galleries',material)
elevation('rear',205,184,.8);t(45,256,'REAR VIEW 4:5 - VIEW ALONG -Y (X REVERSED ON PAGE)',2.7,True)
t(18,165,'B01-B04: four rear G1/4 ports. Dashed Ø28 lands are flat reference areas, not grooves.',2.9,True)
t(18,156,'Gallery axes Y20.00 ±0.10, Z23.50 /63.50 ±0.10 at each end face; Ø11.80 +0.08/0 THROUGH.',2.8)
# Right end viewed along -X, Y increases to the right on this separate view.
x0=24;y0=55;ss=1.0;rect(x0,y0,40*ss,87*ss,True)
for z in (23.5,63.5):
 rect(x0-3,y0+z-14,3,28,True);circle(x0+20,y0+z,6.9,True);c.setDash([2,1]);circle(x0+20,y0+z,11);c.setDash()
dh(x0,x0+40,y0-7,'40.00 ±0.10');t(20,148,'RIGHT END 1:1',2.8,True)
lines(76,139,['Both end faces:',
'X = -205.00 /+205.00.',
'Y = 20.00; Z =23.50 /63.50.',
'Ø22 MIN flat seal lands.',
'Left end is mirrored.'],step=6,size=2.7)
table(191,145,['ID','X','Y','Z'],[[v['id']]+[f'{q:.3f}' for q in v['xyz_mm']] for v in group('E')+group('B')],[23,53,53,53])
lines(191,81,['E01-E04: 4x G1/4 at longitudinal gallery ends.',
'B01-B04: 4x G1/4 at Y40 rear face, opposed to outer front pairs.',
'Rear pilot: Ø11.80 ×20.00 ±0.20 full diameter from rear face,',
'plus 118° drill point; axis intersects the matching gallery.',
'Each row is one continuous network. No internal row link.'],step=6,size=2.7)
c.showPage();page(3,3,'Port/retention sections and manufacturing requirements',material)
# Longitudinal port drilling section at either outer front/rear aligned column: X fixed.
t(19,255,'A-A / THROUGH ALIGNED FRONT AND REAR PORT (2:1)',2.8,True)
ox=35;oy=217;sc=2
# Sideways section: horizontal coordinate is Y; vertical is port radial offset.
rect(ox,oy-15*sc,40*sc,30*sc,True);rect(ox-3*sc,oy-14*sc,3*sc,28*sc,True)
c.setFillColor(colors.white);c.rect((ox-3*sc)*mm,(oy-5.9*sc)*mm,43*sc*mm,11.8*sc*mm,fill=1,stroke=0)
circle(ox+20*sc,oy,5.9*sc)
ln(ox-3*sc,oy-6.9*sc,ox-2*sc,oy-5.9*sc);ln(ox-3*sc,oy+6.9*sc,ox-2*sc,oy+5.9*sc)
ln(ox+40*sc,oy-6.9*sc,ox+39*sc,oy-5.9*sc);ln(ox+40*sc,oy+6.9*sc,ox+39*sc,oy+5.9*sc)
c.setDash([3,1]);ln(ox-6*sc,oy,ox+43*sc,oy);c.setDash()
dh(ox,ox+40*sc,oy-37,'40.00 slab');t(21,174,'Boss Y-3',2.5);t(114,174,'Rear Y40',2.5);t(47,234,'Gallery axis Y20',2.4)
lines(143,251,['ALL 28 PORTS: G 1/4, DIN EN ISO 228-1, parallel BSPP.',
'19 TPI / pitch 1.33684 REF; 55° thread form; right hand.',
'8 MIN full-form thread AFTER entry. Gauge to ISO 228-2.',
'Entry Ø13.80 ±0.10 ×90° ±1° included (45° per side);',
'1.00 depth REF to Ø11.80 pilot. No NPT/R/Rp substitute.',
'Front pilot: 23.00 ±0.20 full diameter from boss sealing face.',
'Rear pilot: 20.00 ±0.20 full diameter from rear sealing face.',
'Front/rear drill point 118° ±2° (tip inside gallery).',
'Thread + run-out maximum from seal face: front/end 16.00;',
'rear 12.00. Supplier to select tap/thread-milling process.',
'Section shows open passage; aligned front/rear points overlap.',
'Other front ports terminate in their gallery with the drill point.'],step=5.7,size=2.75)
t(18,159,'M4 RETENTION / F01-F12',3.2,True)
lines(18,151,['12x M4 ×0.7 - 6H; 10 MIN full thread after entry.',
'Ø3.30 ±0.05 pilot ×13.00 ±0.10 full diameter from A.',
'118° ±2° point; 13.99 total drilled depth REF.',
'Entry Ø4.40 ±0.10 ×90° ±1° included; depth 0.55 REF.',
'10.55 total minimum thread reach from A REF.',
'2.45 unthreaded full-diameter tap allowance REF.',
'Gauge to ISO 1502; no inserts.',
'Blind pilot depth excludes its conical drill point.',
'All twelve F holes are blind and isolated from fluid bores.',
'Supplier must confirm tapping/run-out before machining.'],step=5.7,size=2.75)
t(210,159,'FUNCTIONAL SURFACES / FINISH',3.2,True)
lines(210,151,['All seal lands: Ra ≤1.6 µm; local flatness ≤0.05.',
'Front annulus Ø13.8 to Ø27 REF; rear Ø28 flat land;',
'each side port Ø22 MIN flat land. No radial scratches.',
'Seal-face perpendicularity to thread axis ≤0.05 across Ø22.',
'Exterior POM Ra ≤3.2 µm; unthreaded bores Ra ≤6.3 µm.',
'External edges: break 0.20 max unless otherwise specified.',
'Protect sealing lands; no general rounding of seal faces.',
'NO INTERNAL BORE / CROSS-HOLE DEBURR OPERATION.',
'Clean/flush loose chips; deliver dry, clean and unmarked.',
'No polishing, coating, impregnation or adhesive repairs.'],step=5.7,size=2.75)
lines(18,86,['Two Ø11.80 +0.08/0 galleries THROUGH 410 mm. Opposed drilling permitted: 207 mm reach per end /4 mm overlap REF.',
'Gallery centreline deviation ≤0.30 from nominal; meeting step ≤0.30; no blind web or wall breakthrough.',
'General DIN ISO 2768-1 class m; coordinate tolerances ±0.10 unless stated. Dimensions after stock stabilisation at 20°C.',
'Use sound black unfilled POM-C or POM-H stock; declare grade and supply datasheet before manufacture.',
'Confirm long-bore tooling, thread process and functional finishes. Report proposed deviations before manufacture.',
'Inspect finished threads, bore continuity, all datum dimensions, surface finishes and specified flatness.'],step=7.5,size=2.7)
c.save();print('Q-M01: 2 faceplate sheets and 3 body sheets written')
