"""Dimensioned one-sheet R2 review drawing, matching its STEP and DXF."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor,white
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'cad/radiator/R2.json').read_text());v=json.loads((ROOT/'output/radiator-R2/verification.json').read_text())
c=canvas.Canvas(str(ROOT/'output/pdf/radiator-rack-plate-R2.pdf'),pagesize=(420*mm,297*mm))
c.setTitle('Radiator bracket R2 - 10U, 40 rack positions, 2 mm stainless')
ink=HexColor('#233748');fill=HexColor('#e9edf0')
def text(x,y,t,size=9,b=False):
 c.setFillColor(ink);c.setFont('Helvetica-Bold' if b else 'Helvetica',size);c.drawString(x*mm,y*mm,t)
def line(x1,y1,x2,y2):
 c.setStrokeColor(ink);c.setLineWidth(.5);c.line(x1*mm,y1*mm,x2*mm,y2*mm)
text(17,282,'SUPERNOVA 1260 / RACK BRACKET R2',18,True)
text(17,273,'10U = 444.50 mm | 304 stainless | 2.00 +/-0.10 mm | Four rack fixing positions per U',11)
line(17,269,403,269)
s=.5;ox=140;oy=30
def xy(x,y):return (ox+x*s)*mm,(oy+y*s)*mm
def rounded(x,y,w,h,r):
 a,b=xy(x-w/2,y-h/2);c.roundRect(a,b,w*s*mm,h*s*mm,r*s*mm,fill=1)
c.setFillColor(fill);c.setStrokeColor(ink);rounded(0,p['height']/2,p['width'],p['height'],2)
c.setFillColor(white)
for x in [-100,100]:
 for dy in [-100,100]:rounded(x,p['height']/2+dy,188,188,8)
for x in p['rack_mount_x']:
 for y in p['rack_mount_y']:rounded(x,y,10,7,3.5)
for x in p['radiator_mount_x']:
 for dy in p['radiator_mount_y_from_centre']:
  a,b=xy(x,p['height']/2+dy);c.circle(a,b,1.8*s*mm,fill=1)
# Drawing-only unit boundaries and origin dimensions.
c.setDash(2,2);c.setStrokeColor(HexColor('#95a0a8'))
for u in range(1,10):
 a,b=xy(-p['width']/2,u*44.45);aa,bb=xy(p['width']/2,u*44.45);c.line(a,b,aa,bb)
c.setDash();line(ox-p['width']/4,22,ox+p['width']/4,22)
text(ox-10,24,'482.60',8)
line(12,oy,12,oy+p['height']/2)
c.saveState();c.translate(10*mm,(oy+p['height']/4)*mm);c.rotate(90);c.setFont('Helvetica',8);c.drawCentredString(0,0,'444.50 +0 / -0.15');c.restoreState()
text(20,257,'FRONT / 1:2 - dashed U boundaries are drawing references only',8)
x=278
text(x,256,'RACK FIXINGS / 40 POSITIONS',11,True)
text(x,248,'10 x 7 slots, R3.5 ends, THROUGH.',9)
text(x,242,'X = -232.55 and +232.55.',9)
text(x,236,'Y = 44.45 n + 6.35 / 38.10; n = 0...9.',9)
text(x,228,'U       Lower Y         Upper Y',9,True)
for i in range(10):text(x,220-5.4*i,f'{i+1:2d}       {44.45*i+6.35:7.3f}          {44.45*i+38.1:7.3f}',9)
text(x,159,'RADIATOR FIXINGS / 12 HOLES',11,True)
text(x,152,'Diameter 3.60 THROUGH; X = +/-203.50.',9)
text(x,146,'Y = 18.75, 143.75, 159.75,',9)
text(x,140,'      284.75, 300.75, 425.75.',9)
text(x,130,'CUT PROFILE AND FINISH',11,True)
for i,t in enumerate([
 '4x 188-square apertures, corner R8.',
 'Centres X +/-100; Y122.25 / 322.25.',
 '12 mm central webs; outer corners R2.',
 'No countersinks, no tapped holes.',
 'Coordinates/profile +/-0.15 unless stated.',
 'Hole and slot widths +0.15 / 0.',
 'Deburr 0.2-0.3; flatness target 0.5 overall.',
 'Satin finish; no surface markings.'
]):text(x,123-i*5.5,t,9)
text(x,71,'ASSEMBLY NOTES',11,True)
for i,t in enumerate([
 'Origin: X midplane, Y bottom, Z rear face.',
 'Use suitable rack hardware; outer rows need',
 'head/washer OD <=12 to stay within height.',
 'Full 10U outline has no nominal panel gap.',
 'Radiator retention remains M3: recheck reach',
 'with the thinner plate and actual washers.',
 'Mass '+f'{v["plate_mass_kg"]:.3f}'+' kg; fittings/hoses outside envelope.',
 '40 available holes do not require 40 screws.'
]):text(x,64-i*5.5,t,9)
text(18,12,'R2 | 15 September 2026 | Prototype review - independent of manifold P | STEP/DXF and analysis accompany this drawing',8)
c.save()
