"""Two A3 production sheets for the selected R4 flat plate, all features scheduled."""
from pathlib import Path
import json,math
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib import colors
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'cad/radiator/R4.json').read_text());M=json.loads((ROOT/'cad/manufacturing/R4-M01.json').read_text())
S=json.loads((ROOT/'output/manufacturing/R4-M01/feature-schedule.json').read_text())['features']
STEM=M['part_number'];OUT=ROOT/'output/pdf'/f'{STEM}.pdf'
pdfmetrics.registerFont(TTFont('Arial','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
C=canvas.Canvas(str(OUT),pagesize=(420*mm,297*mm));C.setTitle(STEM);C.setAuthor('Coolant manifold rackmount project')
ink=colors.HexColor('#142833');grey=colors.HexColor('#e9eef1');accent=colors.HexColor('#315e74')
def text(x,y,t,size=2.7,bold=False,align='left'):
 C.setFillColor(ink);C.setFont('Arial-Bold' if bold else 'Arial',size*mm)
 f=C.drawCentredString if align=='centre' else C.drawRightString if align=='right' else C.drawString
 f(x*mm,y*mm,str(t))
def line(x1,y1,x2,y2,w=.18):
 C.setStrokeColor(ink);C.setLineWidth(w*mm);C.line(x1*mm,y1*mm,x2*mm,y2*mm)
def rect(x,y,w,h,fill=False):
 C.setStrokeColor(ink);C.setLineWidth(.18*mm);C.setFillColor(grey if fill else colors.white);C.rect(x*mm,y*mm,w*mm,h*mm,stroke=1,fill=int(fill))
def arrow(x,y,dx,dy):
 length=math.hypot(dx,dy);dx/=length;dy/=length;p=C.beginPath();p.moveTo(x*mm,y*mm)
 for a,b in [(x+1.7*dx-.45*dy,y+1.7*dy+.45*dx),(x+1.7*dx+.45*dy,y+1.7*dy-.45*dx)]:p.lineTo(a*mm,b*mm)
 p.close();C.setFillColor(ink);C.drawPath(p,fill=1,stroke=0)
def dimh(x1,x2,y,t,extension=None):
 if extension is not None:
  line(x1,extension,x1,y+1,.12);line(x2,extension,x2,y+1,.12)
 line(x1,y,x2,y,.12);arrow(x1,y,1,0);arrow(x2,y,-1,0);text((x1+x2)/2,y+2,t,2.5,align='centre')
def dimv(x,y1,y2,t,extension=None):
 if extension is not None:
  line(extension,y1,x+1,y1,.12);line(extension,y2,x+1,y2,.12)
 line(x,y1,x,y2,.12);arrow(x,y1,0,1);arrow(x,y2,0,-1)
 C.saveState();C.translate((x-2)*mm,((y1+y2)/2)*mm);C.rotate(90);text(0,0,t,2.5,align='centre');C.restoreState()
def lines(x,y,items,size=2.6,step=5):
 for i,t in enumerate(items):text(x,y-i*step,t,size)
def table(x,y,width,headers,rows,weights=None,rh=5.6):
 weights=weights or [1]*len(headers);ws=[width*w/sum(weights) for w in weights]
 rect(x,y-rh,width,rh,True)
 for i,row in enumerate([headers]+rows):
  yy=y-(i+1)*rh;xx=x
  for v,w in zip(row,ws):text(xx+1.5,yy+1.7,v,2.5,i==0);xx+=w
  line(x,yy,x+width,yy,.12)
 bottom=y-(len(rows)+1)*rh;xx=x
 for w in [0]+ws:xx+=w;line(xx,y,xx,bottom,.12)
 return bottom
def sheet(n,title):
 rect(10,10,400,277);text(15,279,STEM,4.9,True);text(15,271,title,3.3)
 text(405,280,'R4 APPROVED / ISSUE M01',3.1,True,'right');text(405,273,'Single flat plate - all features through',2.6,False,'right')
 line(10,267,410,267);rect(10,10,400,20)
 for x in (145,283,352):line(x,10,x,30)
 lines(14,24,['304 / EN 1.4301 stainless steel; thickness 2.00 ±0.10','Units: mm; dimensions at 20°C; do not scale'],2.55,7)
 lines(149,24,['Geometry R4 unchanged; '+M['issue_date'],'Production drawing / quotation and supplier review'],2.55,7)
 lines(287,24,['No threads or countersinks','Scale as stated'],2.55,7)
 text(357,23,f'SHEET {n} / 2',3.8,True);text(357,16,'No product markings',2.5)
sheet(1,'Supernova 1260 radiator / NF-A20 rack plate - profile and feature identification')
s=.5;ox=145;oy=39
xy=lambda x,y:(ox+x*s,oy+y*s)
def rounded(x,y,w,h,r,fill=False):
 xx,yy=xy(x-w/2,y-h/2);C.setFillColor(colors.white if fill else grey);C.setStrokeColor(ink);C.setLineWidth(.18*mm)
 C.roundRect(xx*mm,yy*mm,w*s*mm,h*s*mm,r*s*mm,fill=1,stroke=1)
rounded(0,P['height']/2,P['width'],P['height'],2)
# Cut-out fills must precede identifiers: labels may extend over the air openings.
for r in S:
 if r['kind']=='aperture':rounded(r['x'],r['y'],188,188,50,True)
for r in S:
 x,y=xy(r['x'],r['y'])
 if r['kind']=='aperture':text(x,y,r['id'],3,True,'centre')
 elif r['kind']=='slot':
  rounded(r['x'],r['y'],10,7,3.5,True)
  text(x+5.1,y-.7,r['id'],1.9)
 else:
  C.setFillColor(colors.white);C.setStrokeColor(ink);C.circle(x*mm,y*mm,r['diameter']/2*s*mm,stroke=1,fill=1)
  # Place labels away from the nearest aperture, clear of its outline.
  left = (r['x'] < 0) if r['group']=='B' else r['x'] in (-185,15)
  text(x-2.4 if left else x+2.4,y+.8,r['id'],1.9,align='right' if left else 'left')
# Centreline and coordinate origin; identifiers belong to the drawing only.
C.setDash([4,2,1,2]);line(ox,oy-2,ox,oy+P['height']*s+1,.12);C.setDash()
text(ox+3,oy+3,'O (0,0)',2.3)
dimh(ox-P['width']*s/2,ox+P['width']*s/2,34,'482.60 ±0.15',oy)
dimv(16,oy,oy+P['height']*s,'444.50 +0 / -0.15',ox-P['width']*s/2)
text(ox,264,'FRONT VIEW 1:2  /  IDENTIFIERS REFER TO SHEET 2',2.3,False,'centre')
x=294
text(x,254,'FEATURES',3.2,True)
lines(x,246,['A01-A16: 16x Ø4.50 +0.15/0 THROUGH.',
 'Plain fan mounting holes for M4 screws + nuts.',
 'B01-B12: 12x Ø3.60 +0.15/0 THROUGH.',
 'Plain radiator mounting holes for M3 screws.',
 'M3 threads are in the bought-in radiator.',
 'C01-C40: 40x 10.00 ±0.15 x 7.00 +0.15/0',
 'horizontal slots THROUGH; semicircular ends.',
 'D01-D04: 4x 188.00 ±0.15 square cut-outs,',
 'corner R50.00 ±0.15, THROUGH.',
 'Outer corners: 4x R2.00 ±0.15.'],2.6,5.2)
text(x,184,'MANUFACTURING NOTES',3.2,True)
lines(x,176,['1. One flat 2 mm sheet; no bends or welds.',
 '2. NO TAPPED HOLES IN THIS PLATE.',
 '3. NO COUNTERSINKS OR COUNTERBORES.',
 '4. Laser-cut profile and slots. Drill/finish round',
 '   holes where necessary to meet this drawing.',
 '5. Fan holes A: edge break 0.10 max both faces.',
 '   All other cut edges: deburr / break 0.20-0.30.',
 '   Edge breaks are not modelled in STEP.',
 '6. Flatness: 0.50 max, free state, whole plate.',
 '7. Uniform satin brushed finish; no coating,',
 '   engraving, printing or identification marks.',
 '8. Do not add fasteners, rivet nuts or standoffs.',
 '9. Confirm specified tolerances and flatness',
 '   before fabrication; report discrepancies.'],2.6,5.2)
text(x,97,'COORDINATES AND TOLERANCES',3.2,True)
lines(x,89,['Origin O: width centreline at bottom edge.',
 'X right; Y up; all feature axes normal to sheet.',
 'Hole / slot centre X,Y coordinates: ±0.10.',
 'Other profile dimensions: ±0.15 unless stated.',
 'Dimensions apply after finishing; full through',
 'diameters exclude the permitted edge breaks.'],2.6,5.2)
text(x,50,'Matching STEP defines the nominal geometry.',2.5)
text(x,44,'All dimensions / feature IDs are drawing-only.',2.5)
C.showPage()
sheet(2,'Hole and slot coordinate schedules - all 68 fixing positions and four air apertures')
text(16,257,'A: FAN HOLES / 16x Ø4.50 +0.15/0',3.0,True)
fmt=lambda v:f'{v:.3f}'
table(16,251,111,['ID','X','Y'],[[r['id'],fmt(r['x']),fmt(r['y'])] for r in S if r['group']=='A'],[1,1.4,1.4],5.7)
text(16,143,'B: RADIATOR HOLES / 12x Ø3.60 +0.15/0',2.9,True)
table(16,137,111,['ID','X','Y'],[[r['id'],fmt(r['x']),fmt(r['y'])] for r in S if r['group']=='B'],[1,1.4,1.4],5.7)
text(141,257,'C: RACK SLOTS / 40x 10.00 x 7.00',3.0,True)
cs=[r for r in S if r['group']=='C']
table(141,251,149,['ID','X','Y','ID','X','Y'],[[cs[i]['id'],fmt(cs[i]['x']),fmt(cs[i]['y']),cs[i+20]['id'],fmt(cs[i+20]['x']),fmt(cs[i+20]['y'])] for i in range(20)],[1,1.4,1.4,1,1.4,1.4],5.7)
text(141,123,'D: APERTURE CENTRES / 4x 188 SQUARE, R50',2.8,True)
table(141,117,149,['ID','X','Y'],[[r['id'],fmt(r['x']),fmt(r['y'])] for r in S if r['group']=='D'],[1,1.4,1.4],5.7)
lines(141,80,['All scheduled X,Y coordinates: ±0.10 for A/B/C.',
 'D centre coordinates: ±0.15. Values are not chain dimensions.',
 'A/B holes and C/D cut-outs pass through the full 2 mm sheet.',
 'No pilot bores awaiting tapping: A/B are finished clearance holes.',
 'Inspect all 68 fixing positions for size and position.',
 'Check overall width, height, thickness and free-state flatness.'],2.6,6)
# Slot detail at 5:1.
x=302;text(x,257,'SLOT C / 5:1',3.0,True)
C.setFillColor(colors.white);C.setStrokeColor(ink);C.roundRect(319*mm,203*mm,50*mm,35*mm,17.5*mm,fill=0,stroke=1)
dimh(319,369,246,'10.00 ±0.15',238);dimv(382,203,238,'7.00 +0.15/0',369)
line(321.5,211.5,302,192,.12);arrow(321.5,211.5,-19.5,-19.5)
text(302,187,'Ends R3.50 REF = half finished width.',2.5)
text(302,181,'Horizontal centre segment: 3.00 REF.',2.5)
# Shortened edge view: actual material thickness, schematic height.
text(302,163,'EDGE VIEW / 5:1, HEIGHT SHORTENED',2.65,True)
rect(329,121,10,24,True)
for yy in (123,129,135,141):line(329,yy,339,yy+4,.12)
dimh(329,339,154,'2.00 ±0.10',145)
lines(302,111,['All feature axes perpendicular to broad faces.',
 'No countersink angle applies to this part.',
 'Permitted small edge breaks: see sheet 1.',
 'Free-state flatness 0.50 max over whole plate.'],2.5,5.8)
text(302,78,'ISSUE CONTROL',3,True)
lines(302,70,['Approved geometry: R4; manufacturing issue M01.',
 'Quote / manufacture this single plate only.',
 'Radiator, fans, screws and nuts are bought-in.',
 'No supplier assembly or fitting trial is requested.',
 'Drawing tolerances require supplier acceptance.'],2.5,5.8)
C.save();print(OUT)
