"""A3 manufacturing sheets and A4 supplier review for approved O / detail revision O-M02.
Run using the bundled Python with reportlab and pypdf. Geometry comes from JSON.
"""
from pathlib import Path
import math, datetime
import revision_json as json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A3,A4,landscape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'cad/iterations/O-long-bore.json').read_text())
f=json.loads((ROOT/'cad/manufacturing/O-M02.json').read_text())
schedule=json.loads((ROOT/'output/manufacturing/O-M02/feature-schedule.json').read_text())
OUT=ROOT/'output/pdf';OUT.mkdir(exist_ok=True)
DATE=f['manufacturing_revision_date']
H=f['boss_height']
D=40+H
PILOT=20+H
pdfmetrics.registerFont(TTFont('Arial','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
BLACK=colors.HexColor('#16222a');GREY=colors.HexColor('#71808b');LIGHT=colors.HexColor('#edf1f3')
C=None

def text(x,y,t,size=2.8,bold=False,align='left'):
    C.setFillColor(BLACK);C.setFont('Arial-Bold' if bold else 'Arial',size*mm)
    fun=C.drawCentredString if align=='centre' else C.drawRightString if align=='right' else C.drawString
    fun(x*mm,y*mm,str(t))
def line(x1,y1,x2,y2,width=.22,dash=None):
    C.setStrokeColor(BLACK);C.setLineWidth(width*mm);C.setDash(dash or [])
    C.line(x1*mm,y1*mm,x2*mm,y2*mm);C.setDash([])
def rect(x,y,w,h,fill=False):
    C.setFillColor(LIGHT if fill else colors.white);C.setStrokeColor(BLACK);C.setLineWidth(.25*mm)
    C.rect(x*mm,y*mm,w*mm,h*mm,stroke=1,fill=int(fill))
def circle(x,y,r,width=.25):
    C.setStrokeColor(BLACK);C.setLineWidth(width*mm);C.circle(x*mm,y*mm,r*mm,stroke=1,fill=0)
def cross(x,y,r=2):
    line(x-r,y,x+r,y,.12);line(x,y-r,x,y+r,.12)
def arrow(x,y,dx,dy):
    # Filled 1.6 mm long arrow, tip at x,y.
    n=math.hypot(dx,dy);dx/=n;dy/=n
    path=C.beginPath();path.moveTo(x*mm,y*mm)
    path.lineTo((x+dx*1.6-dy*.5)*mm,(y+dy*1.6+dx*.5)*mm)
    path.lineTo((x+dx*1.6+dy*.5)*mm,(y+dy*1.6-dx*.5)*mm);path.close()
    C.setFillColor(BLACK);C.drawPath(path,fill=1,stroke=0)
def dimh(x1,x2,y,label,ext=None):
    if ext is not None:
        line(x1,ext,x1,y+1,.12);line(x2,ext,x2,y+1,.12)
    line(x1,y,x2,y,.15);arrow(x1,y,1,0);arrow(x2,y,-1,0);text((x1+x2)/2,y+2,label,2.7,align='centre')
def dimv(x,y1,y2,label,ext=None):
    if ext is not None:
        line(ext,y1,x+1,y1,.12);line(ext,y2,x+1,y2,.12)
    line(x,y1,x,y2,.15);arrow(x,y1,0,1);arrow(x,y2,0,-1)
    C.saveState();C.translate((x+2)*mm,((y1+y2)/2)*mm);C.rotate(90)
    text(0,0,label,2.7,align='centre');C.restoreState()
def leader(px,py,x,y,label):
    line(px,py,x,y,.15);arrow(px,py,x-px,y-py);text(x+1,y+1,label,2.7)
def datum(x,y,label):
    rect(x-2.5,y-2.5,5,5);text(x,y-1,label,3,bold=True,align='centre')
def centreline(x1,y1,x2,y2):line(x1,y1,x2,y2,.12,[6,2,1,2])
def notes(x,y,lines,size=2.8,step=5):
    for t in lines:text(x,y,t,size);y-=step
    return y

def table(x,top,width,headers,rows,weights=None,rowh=5.5):
    weights=weights or [1]*len(headers);total=sum(weights);ws=[width*v/total for v in weights]
    rect(x,top-rowh,width,rowh,True)
    xx=x
    for h,w in zip(headers,ws):text(xx+1.5,top-rowh+1.6,h,2.55,True);xx+=w
    for i,row in enumerate(rows):
        y=top-rowh*(i+2);line(x,y,x+width,y,.12);xx=x
        for val,w in zip(row,ws):text(xx+1.5,y+1.6,val,2.55);xx+=w
    bottom=top-rowh*(len(rows)+1);line(x,top,x,bottom,.18);line(x+width,top,x+width,bottom,.18)
    xx=x
    for w in ws[:-1]:xx+=w;line(xx,top,xx,bottom,.12)
    return bottom

def sheet(code,title,index,total,material,scale='AS SHOWN'):
    C.setPageSize(landscape(A3));C.setTitle(code);C.setAuthor('Coolant manifold rackmount project')
    rect(10,10,400,277)
    text(15,279,code,5,True);text(15,271,title,3.6)
    text(405,280,'LAYOUT O • DETAIL REVISION O-M02',3,True,align='right')
    text(405,273,'Single-part machining drawing',2.8,align='right')
    rect(10,10,400,27)
    for x in (135,265,345):line(x,10,x,37)
    text(14,31,material,3,True);text(14,24,'Units: mm • DIN ISO 2768-1 m unless stated',2.55)
    text(14,17,'Dimensions at 20 °C • Do not scale drawing',2.55)
    text(140,31,'Geometry: approved Revision O',3)
    text(140,24,'Detail revision: O-M02 • '+DATE,2.7)
    text(140,17,'No tapped holes; six countersinks only' if 'FACEPLATE' in code else 'Unmodelled helices: machine threads to this drawing',2.55)
    text(270,31,'Scale: '+scale,3);text(270,24,'Third-angle; views labelled',2.55)
    text(270,17,'No product markings',2.55)
    text(350,31,f'SHEET {index} / {total}',3.8,True)
    text(350,23,'PDF + matching STEP',2.7)
    text(350,16,'Quotation / supplier DFM',2.55)

def front_view(body=False,x0=42,y0=166,s=.68):
    width=p['body_width'] if body else p['rack_width'];height=87
    rect(x0,y0,width*s,height*s)
    def at(x,z):return x0+(x+width/2)*s,y0+z*s
    cx=x0+width*s/2;centreline(cx,y0-4,cx,y0+height*s+6)
    datum(cx,y0+height*s+10,'B')
    dimh(x0,x0+width*s,y0+height*s+20,f'{width:g} ±0.20',y0+height*s)
    dimv(x0+width*s+10,y0,y0+height*s,'87 ±0.10',x0+width*s)
    datum(x0-6,y0,'C');line(x0-3.5,y0,x0,y0)
    for item in schedule['front_ports']:
        x,z=item['x'],item['z'];cx,cy=at(x,z)
        circle(cx,cy,(14 if body else 16)*s)
        if body:
            circle(cx,cy,5.9*s);C.setDash([4,2]);circle(cx,cy,6.5785*s,.12);C.setDash([])
            text(cx,cy+7.2*s,item['id'],2.35,align='centre')
        else:text(cx,cy+3,item['id'],2.5,align='centre')
        cross(cx,cy,1.4)
    for item in schedule['body_fixings']:
        cx,cy=at(item['x'],item['z']);circle(cx,cy,(1.65 if body else 2.25)*s)
        circle(cx,cy,(2.2 if body else 4)*s,.15)
        yy=y0-8 if item['z']<40 else y0+height*s+4
        leader(cx,cy,cx+3,yy,item['id'])
    if not body:
        for item in schedule['rack_slots']:
            cx,cy=at(item['x'],item['z']);C.setLineWidth(.25*mm)
            C.roundRect((cx-5*s)*mm,(cy-3.5*s)*mm,10*s*mm,7*s*mm,3.5*s*mm,stroke=1,fill=0)
            cross(cx,cy,1.2)
            text(cx+(-5 if item['x']<0 else 5),cy-.8,item['id'],2.2,align='right' if item['x']<0 else 'left')
    text(x0,y0-16,'FRONT VIEW — looking +Y; countersinks / bosses face the viewer',2.8)
    return at

# ---------- FACEPLATE ----------
C=canvas.Canvas(str(OUT/'RM10-O-M02-FACEPLATE.pdf'),pagesize=landscape(A3))
sheet('RM10-O-M02-FACEPLATE','FLAT STAINLESS RACK FACEPLATE — HOLE LOCATION SCHEDULE',1,2,'304 STAINLESS / EN 1.4301','0.68:1')
text(15,260,'20 × Ø32 +0.20/0 THRU • 6 × Ø4.5 +0.10/0 THRU with Ø8 +0.10/0 × 90° ±1° CSK • 12 × 10 × 7 slots',3.0,True)
text(15,254,'All coordinates below: signed X from width midplane B; Z from bottom C. ±0.10 unless otherwise shown.',2.8)
front_view()
rows=[[f'P{i+1:02d} / P{i+11:02d}',f'{-180+40*i:g}','23.5 / 63.5'] for i in range(10)]
table(15,139,143,['WINDOW IDs','X ±0.10','Z ±0.10'],rows,[1.3,1,1.2])
table(166,139,105,['M4 CLEARANCE','X ±0.10','Z ±0.10'],[[i['id'],f"{i['x']:g}",f"{i['z']:g}"] for i in schedule['body_fixings']],[1.3,1,1])
table(279,139,126,['SLOT IDs L / R','X LEFT / RIGHT','Z ±0.10'],[[f'R{i+1:02d} / R{i+7:02d}','−232.55 / +232.55',f'{z:g}'] for i,z in enumerate(p['rack_slot_centres_z'])],[1.1,1.6,1])
notes(166,91,['All six fixing holes are CLEARANCE holes.','NO TAPPED HOLES IN THIS PLATE.','Countersink on FRONT / outside face only.'],2.75)
notes(279,91,['Slots: 10 ±0.10 long × 7 +0.10/0 wide.','End radii: R3.5 REF. Long axis along X.','Rack fasteners are selected by the builder.'],2.7)
notes(15,63,['A = flat POM-facing rear plane, Y0. B = derived width midplane, X0. C = bottom edge, Z0.',
              'Thickness and countersink section: sheet 2. DXF is the through-cut profile only; countersinks are in STEP/PDF.',
              'P01–P20, F1–F6 and R01–R12 are drawing IDs only. Do not engrave, print or laser-mark the part.'],2.75)
C.showPage()
sheet('RM10-O-M02-FACEPLATE','COUNTERSINK DETAIL, FINISH AND INSPECTION REQUIREMENTS',2,2,'304 STAINLESS / EN 1.4301','DETAIL 8:1')
text(20,259,'DETAIL A — F1–F6, section through each fixing hole',3.7,True)
x=50;y=210;s=8
# Two solid halves around the hole; front at x, rear at x+3s.
for sign in (-1,1):
    pts=[(x,y+sign*5*s),(x+3*s,y+sign*5*s),(x+3*s,y+sign*2.25*s),(x+1.75*s,y+sign*2.25*s),(x,y+sign*4*s)]
    path=C.beginPath();path.moveTo(pts[0][0]*mm,pts[0][1]*mm)
    for xx,yy in pts[1:]:path.lineTo(xx*mm,yy*mm)
    path.close();C.setFillColor(LIGHT);C.drawPath(path,fill=1,stroke=1)
centreline(x-10,y,x+3*s+10,y)
dimh(x,x+3*s,142,'3.00 ±0.10',154)
dimv(37,y-4*s,y+4*s,'Ø8 +0.10/0',x)
dimv(91,y-2.25*s,y+2.25*s,'Ø4.5 +0.10/0',x+3*s)
leader(x+.875*s,y+3.125*s,112,244,'90° ±1° INCLUDED ANGLE')
notes(112,228,['Countersink depth 1.75 REF at nominal sizes.','Remaining cylindrical land 1.25 REF.','Dimension the mouth diameter and included angle;','do not independently tolerance the derived depth.'],2.9)
text(50,131,'FRONT',2.8,align='centre');text(74,131,'POM SIDE / A',2.8,align='centre')
notes(220,256,['MANUFACTURING',
 '1. Finished thickness 3.00 ±0.10. No bends.',
 '2. Mill or profile-cut the blank and openings;',
 '   finish-machine the six countersinks from the front.',
 '3. All opening positions ±0.10 in X and Z.',
 '4. Free-state flatness of POM-facing plane A: 0.30.',
 '5. Ra ≤3.2 µm on face A and countersink seats.',
 '6. Remove cutting dross and all raised burrs.',
 '   Light edge break 0.10–0.20 max unless detailed.',
 '   Do not enlarge countersink mouths during deburring.',
 '7. No coating, bead blasting, engraving or markings.',
 '   Clean and dry after machining. No loose abrasive.',
 '8. Finish dimensions apply after all processing.'],2.9,6)
notes(20,111,['FASTENER INTERFACE',
 'Specified head: A4 M4 × 12 DIN 7991 hex socket; maximum head Ø7.96 (Westfield reference).',
 'DIN 965 Z M4 Pozi alternative: nominal head Ø7.5. It seats lower in the same 90° countersink.',
 'Nominal recess for Ø7.96 head: 0.02 mm; Ø7.5 head: 0.25 mm (ideal cone geometry only).',
 'Inspect with the specified screw. Target flush to slightly recessed; no more than 0.20 mm proud.',
 'Do not substitute a larger-head standard under an equivalent-name label without checking the fit.',
 'Inspect 20 windows, 6 clearance holes + countersinks, and 12 slots. No threads in this part.',
 'Outer slot-to-edge ligament is 1.90 REF before edge breaking; do not reduce the outer profile.'],2.8,6)
C.showPage();C.save()

# ---------- BODY ----------
material='BLACK UNFILLED POM / C OR H'
C=canvas.Canvas(str(OUT/'RM10-O-M02-BODY.pdf'),pagesize=landscape(A3))
sheet('RM10-O-M02-BODY','POM MANIFOLD — FRONT AND END PORT / FIXING LOCATIONS',1,3,material,'0.73:1')
text(15,260,'30 TAPPED FEATURES TOTAL: 20 front G 1/4 + 4 end G 1/4 + 6 M4 × 0.7. No thread inserts.',3.05,True)
text(15,254,'Two uninterrupted Ø11.8 galleries. Long-bore process requires supplier engineering confirmation before manufacture.',2.8)
front_view(True,27,165,.73)
# Right end view. Y grows rightwards; front at the left. Side mouths at Y20.
x=360;y=165;s=.73
rect(x,y,40*s,87*s)
for z in p['port_rows_z']:
    circle(x+20*s,y+z*s,6.9*s);C.setDash([3,2]);circle(x+20*s,y+z*s,11*s,.12);C.setDash([])
    cross(x+20*s,y+z*s);text(x+20*s,y+z*s+9*s,'E3' if z<40 else 'E4',2.4,align='centre')
    C.setDash([3,2]);rect(x-H*s,y+(z-14)*s,H*s,28*s);C.setDash([])
dimh(x,x+40*s,242,'40 ±0.10',y+87*s)
text(x+14.6,154,'RIGHT END',2.8,align='centre');text(x+14.6,148,'looking −X',2.5,align='centre')
table(15,138,145,['FRONT PORT IDs','X ±0.10','Z ±0.10'],rows,[1.3,1,1.2])
table(168,138,105,['M4 IDs','X ±0.10','Z ±0.10'],[[i['id'],f"{i['x']:g}",f"{i['z']:g}"] for i in schedule['body_fixings']])
table(281,138,124,['END ID','FACE','Y / Z ±0.10'],[[i['id'],i['side'],f"20 / {i['z']:g}"] for i in schedule['end_ports']],[.6,1,1.3])
notes(281,104,['Left face: X−205; right face: X+205.', 'Both ends have the same Y/Z coordinates.', 'Ø22 dashed rings show sealing lands;', 'they are NOT recesses or grooves.'],2.65,5)
notes(168,92,['A = body front mounting plane Y0.', 'B = width midplane X0; C = bottom Z0.', f'Boss faces: Y−{H:.1f} ±0.10 from A.', f'Overall depth: {D:g} REF including bosses.'],2.7,5)
notes(15,62,['20 bosses: Ø28 ±0.10, root R1.0 ±0.10, outer lip C0.5 ±0.10 × 45° ±1° (see sheet 2).',
 'Front drill/thread axes normal to A; end port axes parallel to X. All threads right-hand.',
 'Surface requirements, bore controls, inspection and manufacturing notes: sheet 3. No product markings.'],2.8)
C.showPage()
sheet('RM10-O-M02-BODY','PORT, BOSS AND BLIND M4 DETAILS',2,3,material,'AS SHOWN')
text(18,260,'DETAIL A — FRONT G 1/4 PORT / BOSS, 2:1 (20 places)',3.5,True)
# Cross-section through front boss and gallery, local horizontal distance measured from boss face.
x=30;y=204;s=2
path=C.beginPath();pts=[(0,13.5),(.5,14),(H-1,14)]
path.moveTo((x+pts[0][0]*s)*mm,(y+pts[0][1]*s)*mm)
for u,v in pts[1:]:path.lineTo((x+u*s)*mm,(y+v*s)*mm)
path.curveTo((x+(H-.4477)*s)*mm,(y+14*s)*mm,(x+H*s)*mm,(y+14.4477*s)*mm,(x+H*s)*mm,(y+15*s)*mm)
for u,v in [(H,18),(D,18),(D,-18),(H,-18),(H,-15)]:path.lineTo((x+u*s)*mm,(y+v*s)*mm)
path.curveTo((x+H*s)*mm,(y-14.4477*s)*mm,(x+(H-.4477)*s)*mm,(y-14*s)*mm,(x+(H-1)*s)*mm,(y-14*s)*mm)
for u,v in [(.5,-14),(0,-13.5)]:path.lineTo((x+u*s)*mm,(y+v*s)*mm)
path.close();C.setFillColor(LIGHT);C.drawPath(path,fill=1,stroke=1)
# Void union. Draw white shapes, then outline only the meaningful boundaries.
C.setFillColor(colors.white);C.rect(x*mm,(y-5.9*s)*mm,PILOT*s*mm,11.8*s*mm,fill=1,stroke=0)
C.circle((x+PILOT*s)*mm,y*mm,5.9*s*mm,fill=1,stroke=1)
C.rect(x*mm,(y-5.9*s)*mm,PILOT*s*mm,11.8*s*mm,fill=1,stroke=0)
for sign in [-1,1]:
    line(x,y+sign*6.9*s,x+1*s,y+sign*5.9*s)
    line(x+1*s,y+sign*5.9*s,x+PILOT*s,y+sign*5.9*s)
    line(x+1*s,y+sign*6.5785*s,x+9*s,y+sign*6.5785*s,.12)
    line(x+PILOT*s,y+sign*5.9*s,x+(PILOT+3.54507765)*s,y,.12,[3,2])
centreline(x-5,y,x+D*s+5,y)
dimh(x,x+H*s,156,f'{H:.1f} ±0.10',176)
dimh(x+H*s,x+D*s,143,'40.0 ±0.10',168)
leader(x+.25*s,y+13.75*s,65,245,'C0.5 ±0.10 × 45° ±1°')
leader(x+(H-.3)*s,y+14.3*s,117,235,'R1.0 ±0.10')
leader(x+PILOT*s,y-5.9*s,139,164,'Ø11.8 gallery, axis Y20')
notes(143,225,['G 1/4 — DIN EN ISO 228-1, parallel BSPP.', '19 TPI (P = 1.33684 REF); 55° thread form.', 'Entry Ø13.8 ±0.10 × 90° ±1° included.', 'Entry depth 1.0 REF to Ø11.8 pilot.', '8 MIN full-form thread length after lead-in.', 'Thread + tool run-out must end within', '16 mm of the sealing face.', f'Front pilot: Ø11.8, {PILOT:.1f} ±0.20 full diameter', 'from boss face to gallery axis; 118° tip REF.', 'Protect flat seal annulus: Ø13.8 to Ø27 REF.'],2.7,5)
# End section detail with the long bore represented by a cropped axial region.
text(267,260,'DETAIL B — END G 1/4, 2:1 (4 places)',3.4,True)
x=285;y=202;s=2
rect(x,y-35,70,70,True)
C.setFillColor(colors.white);C.rect(x*mm,(y-5.9*s)*mm,70*mm,11.8*s*mm,fill=1,stroke=0)
for sign in (-1,1):
    line(x,y+sign*6.9*s,x+s,y+sign*5.9*s)
    line(x+s,y+sign*5.9*s,x+70,y+sign*5.9*s)
    line(x+s,y+sign*6.5785*s,x+9*s,y+sign*6.5785*s,.12)
centreline(x-5,y,x+75,y)
notes(269,157,['Same G 1/4 thread and Ø13.8 × 90° entry.', '8 MIN full-form thread after lead-in.', 'Thread/run-out ≤16 from each end face.', 'Flat Ø22 MIN sealing land on end face.', 'Unthreaded bore continues to opposite end.', 'No end caps, inserts, glued plugs or splits.'],2.7,5)
# M4 detail lower-left.
text(18,124,'DETAIL C — M4 × 0.7 - 6H (6 places), 3:1',3.4,True)
x=32;y=88;s=3
rect(x,y-15,58,30,True)
C.setFillColor(colors.white);C.rect(x*mm,(y-1.65*s)*mm,14*s*mm,3.3*s*mm,fill=1,stroke=0)
for sign in (-1,1):
    line(x,y+sign*2.2*s,x+.55*s,y+sign*1.65*s)
    line(x+.55*s,y+sign*1.65*s,x+14*s,y+sign*1.65*s)
    line(x+14*s,y+sign*1.65*s,x+14.991*s,y)
    line(x+.55*s,y+sign*2*s,x+10.55*s,y+sign*2*s,.12)
centreline(x-4,y,x+61,y)
dimh(x,x+14*s,65,'14 +0.50/0 FULL Ø',73)
notes(112,115,['M4 × 0.7 - 6H, 10 MIN full-form thread after entry.', 'Ø3.3 tapping pilot, 14 +0.50/0 full-diameter depth.', '118° ±2° drill point; total tip depth ≤15.5 from A.', 'Entry Ø4.4 ±0.10 × 90° ±1° included (0.55 REF).', 'No inserts. Do not break into a coolant passage.', 'Drill depth ≠ full thread length; leave run-out space.', 'General unspecified external edges: break 0.10–0.20 max.'],2.8,6)
C.showPage()
sheet('RM10-O-M02-BODY','LONG-BORE SECTION, TOLERANCES AND MACHINING NOTES',3,3,material,'SECTION 0.80:1')
text(15,259,'SECTION THROUGH ONE GALLERY AT Z23.5 — second gallery identical at Z63.5',3.5,True)
x=40;y=207;s=.8
rect(x,y,410*s,40*s,True)
# Bosses in this section and the open cross-bores.
for xx in [-180+40*i for i in range(10)]:
    cx=x+(xx+205)*s;rect(cx-14*s,y-H*s,28*s,H*s,True)
C.setFillColor(colors.white);C.rect(x*mm,(y+14.1*s)*mm,410*s*mm,11.8*s*mm,fill=1,stroke=0)
line(x,y+14.1*s,x+410*s,y+14.1*s)
for xx in [-180+40*i for i in range(10)]:
    cx=x+(xx+205)*s
    C.setFillColor(colors.white);C.rect((cx-5.9*s)*mm,(y-H*s)*mm,11.8*s*mm,PILOT*s*mm,fill=1,stroke=0)
    line(cx-5.9*s,y-H*s,cx-5.9*s,y+14.1*s,.18);line(cx+5.9*s,y-H*s,cx+5.9*s,y+14.1*s,.18)
line(x,y+25.9*s,x+410*s,y+25.9*s)
centreline(x-5,y+20*s,x+410*s+5,y+20*s)
dimh(x,x+410*s,247,'410 ±0.20 THROUGH LENGTH',y+40*s)
dimv(x+410*s+12,y,y+40*s,'40 ±0.10',x+410*s)
text(40,192,'FRONT / BOSS SIDE',2.6);text(204,192,'Y20 gallery axis • equal 14.1 mm walls REF',2.7)
notes(15,180,['BORES / THREADS / CLEANLINESS',
 '1. Two galleries Ø11.8 +0.08/0 through 410 mm, axes Y20;',
 '   Z23.5 and Z63.5. Continuous parallel networks only.',
 '2. Opposed drilling is permissible. Nominal reach 207 mm',
 '   per end gives 4 mm overlap; select tooling/process.',
 '3. Gallery centreline deviation ≤0.30 from nominal axis;',
 '   meeting step ≤0.30. No blind webs or wall breakthrough.',
 '4. Unthreaded gallery / branch bores: Ra ≤6.3 µm.',
 '5. G 1/4: gauge to ISO 228-2. M4: gauge to ISO 1502.',
 '   Thread quality governs the final tapped pilot diameter.',
 '   G is PARALLEL; no NPT, R, Rp or tapered substitute.',
 '6. INTERNAL EDGE DEBURRING IS NOT REQUIRED.',
 '   Clean / flush out loose machining chips only.',
 '   Verify both galleries are continuous and open.',
 '7. Deliver dry and clean. No chemical treatment, impregnation',
 '   or adhesive repairs without agreement. No product marks.'],2.7,5.5)
notes(220,180,['DATUMS / FUNCTIONAL SURFACES',
 '8. A: front body mounting plane; flatness 0.15.',
 '   B: derived width midplane. C: bottom plane.',
 '   Front boss/thread and M4 positions: X/Z ±0.10.',
 '   Side mouth positions: Y/Z ±0.10 at each end face.',
 f'9. Boss OD Ø28 ±0.10; height {H:.1f} ±0.10; root R1 ±0.10.',
 '   Lip C0.5 ±0.10 ×45° ±1°. Do not round the sealing face.',
 '10. Each front sealing annulus and each Ø22 end land:',
 '    Ra ≤1.6 µm, local flatness 0.05; no radial scratches.',
 '    Seal plane perpendicular to its thread axis within',
 '    0.05 across Ø22. Do not recess the sealing lands.',
 '11. Other machined exterior surfaces: Ra ≤3.2 µm.',
 '12. Dimensions apply after material stabilisation at 20 °C.',
 '    Declare resin grade and stock form before manufacture.',
 '    POM-C or POM-H accepted; supply grade datasheet.',
 '13. 2 mm rack-envelope gap is not a tolerance allocation;',
 '    this drawing does not qualify the assembled rack fit.'],2.7,5.5)
text(15,79,'SUPPLIER DFM HOLD POINT: confirm long-bore process, alignment inspection and material grade before cutting.',2.9,True)
notes(15,67,['STEP contains nominal tapping pilots, not thread helices. General external edge deburring is not explicitly modelled.',
 'Boss lip chamfers, port-entry cones and M4 pilot drill points are modelled in the matching O-M02 STEP.',
 'Operator approval applies to layout O. This revision uses 4 mm bosses and edge / drill details; no pressure or structural rating is claimed.'],2.75)
C.showPage();C.save()

# ---------- SUPPLIER REVIEW (A4) ----------
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyA',fontName='Arial',fontSize=9.5,leading=13,spaceAfter=7))
styles.add(ParagraphStyle(name='HeadA',fontName='Arial-Bold',fontSize=16,leading=19,spaceAfter=10))
styles.add(ParagraphStyle(name='SubA',fontName='Arial-Bold',fontSize=11,leading=14,spaceBefore=8,spaceAfter=5))
story=[]
def para(t,style='BodyA'):story.append(Paragraph(t,styles[style]))
def link(title,url):return f'<link href="{url}" color="#175c83">{title}</link>'
para('Revision O / O-M02 — JLC manufacturability review','HeadA')
para('Checked '+DATE+'. Layout O is retained with the requested 4 mm bosses (1 mm above the plate). O-M01 remains archived. O-M02 is a detailed quotation package, not confirmation of supplier acceptance or a pressure-rated release.')
para('Conclusion','SubA')
para('The faceplate is a plausible conventional flat CNC part. The body is geometrically machinable in principle, but JLC acceptance remains conditional on deep-hole drilling, sealing finishes and the declared POM grade. Internal edge deburring is excluded at the operator’s request; only external deburring and internal chip cleaning are required. No supplier upload or order has been made.')
para('JLC requirements applied','SubA')
para('Upload each part separately as one STEP solid with its matching-name PDF. The plate ZIP also contains its cut-profile DXF. Select Threads YES for the body and NO for the faceplate. Threads are represented by tapping pilots in STEP. Order-page options must match the drawings. Tell JLC that these two separately quoted parts mate. '+link('JLC ordering guidance','https://jlccnc.com/help/article/cnc-machining-ordering-guidelines'))
para('Both parts fit the published 1100 × 600 × 500 mm envelope. The 3 mm faceplate is at the listed minimum thickness for a flat metal part; its long, perforated form still needs support and flatness control. '+link('JLC capabilities','https://jlccnc.com/'))
para('Thread depths are short: 8 mm full form for G 1/4 and 10 mm for M4. The M4 pilot provides run-out space and a conventional drill point. The R1 boss roots are shallow but require a suitable toolpath; confirm JLC can retain the specified radius. Wall reserves exceed its generic plastic guidance, which is a machining rule, not a pressure test. '+link('JLC CNC design guide','https://jlccnc.com/help/article/cnc-machining-design-guideline'))
para('Threads and long bores','SubA')
para('The body has 24 G 1/4 and 6 M4 threaded features. Confirm availability of ISO 228 G tooling and gauges; standard BSPP is not a permission to substitute ISO 7 Rp. The final thread gauge requirement controls the threaded region. '+link('JLC thread guide','https://jlccnc.com/help/article/threaded-hole-guideline'))
para('Our geometry gives 410/11.8 = 34.75D for a single bore, or 207/11.8 = 17.54D for opposed drilling. These are calculated ratios, not JLC published limits. Special drilling and chip control are likely; nominal straight STEP cylinders do not demonstrate achievable alignment. '+link('Deep-hole tooling context','https://www.mscdirect.com/knowledge-center/articles/canons-to-carbide-deep-hole-drilling-simplified'))
para('Material selection','SubA')
para('Body requirement: '+f['body_material'].rstrip('.')+'. JLC lists POM; confirm the supplied grade and black-stock availability. Branded Delrin is not required. '+link('JLC POM page','https://jlccnc.com/help/article/pom-cnc-machining'))
para('The faceplate is dry 304 stainless, a listed CNC material. It is not a wetted rear cover. '+link('JLC SUS304','https://jlccnc.com/help/article/sus304-cnc-machining'))
story.append(PageBreak())
para('Fit, edge treatment and supplier questions','HeadA')
para('Boss clearance','SubA')
para('Retain Ø32 +0.20/0 plate windows and Ø28 ±0.10 bosses. Nominal radial clearance is 2 mm. The R1 root grows to Ø30 nominal at the POM mounting plane. At worst specified sizes (Ø28.1 and R1.1), its envelope is Ø30.3: 0.85 mm radial reserve before positional error. Independent ±0.10 X/Z coordinates on both parts consume up to 0.283 mm, leaving about 0.567 mm with aligned assembly frames. Screw-clearance registration, thermal growth and deformation are additional; perform an assembly trial. A Ø29 window would interfere with the nominal root.')
para('Boss height is 4.0 ±0.10 mm above the POM mounting plane. With a 3.0 ±0.10 mm plate, nominal projection is 1 mm (0.8–1.2 mm size stack before flatness and assembly effects). This clears the plate for fittings whose sealing shoulder seats on the POM; verify unusually recessed shoulders and tool access. Boss lips receive C0.5 ×45°. Their flat sealing annulus remains about Ø13.8–Ø27. The existing mouth chamfer is retained; do not enlarge it casually into the O-ring footprint. POM can be burred, dented or gouged at thin edges; the edge break improves handling without treating the material as inherently brittle. Sealing lands require careful finishing, not general rounding.')
para('Faceplate countersinks','SubA')
para('Six Ø4.5 through holes receive Ø8 ×90° countersinks on the front only. Nominal depth is 1.75 mm in 3 mm stock, leaving 1.25 mm cylindrical land. The specified DIN 7991 reference has Ø7.96 maximum head; DIN 965 Z Pozi has Ø7.5 nominal head. Inspect using the specified screw family rather than relying only on a generic “M4 countersunk” label. '+link('Hex head reference','https://www.westfieldfasteners.co.uk/A4-ScrewBolt-SHCsk-M4.html')+'; '+link('Pozi reference','https://www.westfieldfasteners.co.uk/A4-ScrewBolt-PoziCsk-M4.html'))
para('Sheet-metal alternative','SubA')
para('Laser profiling plus secondary countersinking is possible if the drawing tolerances are met. JLC sheet-metal guidance lists minimum hole diameter max(1 mm, half stock thickness) and 1 mm between holes; this pattern exceeds those values. Its default tolerances and submission rules differ from CNC. Request the secondary countersinks and specified flatness explicitly. No bending is required. '+link('JLC sheet-metal guide','https://jlccnc.com/help/article/sheet-metal-fabrication-guidelines'))
para('Confirm with JLC before manufacture','SubA')
for t in [
 'Can you make two Ø11.8 +0.08/0 bores through 410 mm in the specified black POM, including the 0.30 mm alignment / meeting-step requirements?',
 'What drilling and inspection method will be used? Internal edge deburring is not required; passages must be cleaned/flushed free of loose machining chips.',
 'Can you supply the specified resin grade and machine/gauge G 1/4 ISO 228-1 and M4-6H directly in POM?',
 'Can you achieve the indicated seal-face finish, local flatness, perpendicularity and plate flatness without rounding the sealing lands?',
 'Please review the two-part fit and report any proposed geometry, tolerance or material changes before proceeding.'
]:para('• '+t)
para('Remaining design limits','SubA')
para('The approved rack pattern retains 1.9 mm nominal metal at the outermost slot edges; washer overhang there remains a builder-hardware concern. The previous 2 mm elbow/nut gap uses illustrative envelopes. Actual hardware, temperature, clamp preload, creep and assembled leak/pressure behaviour have not been qualified. These findings do not prevent requesting a manual manufacturing review.')
doc=SimpleDocTemplate(str(OUT/'RM10-O-M02-DFM.pdf'),pagesize=A4,leftMargin=17*mm,rightMargin=17*mm,topMargin=16*mm,bottomMargin=16*mm)
def footer(c,doc):
    c.setFont('Arial',8);c.drawString(17*mm,9*mm,'RM10-O-M02 • Supplier review • '+DATE);c.drawRightString(193*mm,9*mm,str(doc.page))
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('Created faceplate (2 sheets), body (3 sheets) and supplier review PDFs.')
