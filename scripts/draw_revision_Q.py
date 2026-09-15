"""Dimensioned rear elevation for Q design review, not a production drawing."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];p=json.loads((ROOT/'cad/iterations/Q-rear-ports.json').read_text())
out=ROOT/'output/long-bore-Q';out.mkdir(exist_ok=True)
a=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="930" viewBox="0 0 1500 930"><rect width="1500" height="930" fill="white"/><g font-family="Arial,sans-serif" fill="#203342">']
def text(x,y,t,size=20,anchor='start'):a.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">{t}</text>')
def line(x1,y1,x2,y2,dash=False):a.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="#607583" stroke-width="1.5"'+(' stroke-dasharray="7 5"' if dash else '')+'/>')
def dim(x1,x2,y,t):
 line(x1,y,x2,y);line(x1,y-7,x1,y+7);line(x2,y-7,x2,y+7);text((x1+x2)/2,y-12,t,18,'middle')
s=2.7;ox=750;oy=240
def pt(x,z):return ox-x*s,oy+(87-z)*s
text(65,58,'REVISION Q — FOUR REAR G1/4 PORTS',30)
text(65,94,'Rear elevation • millimetres • design review only • P faceplate and front interfaces retained',20)
x0,y0=pt(205,87);x1,y1=pt(-205,0)
a.append(f'<rect x="{x0}" y="{y0}" width="{410*s}" height="{87*s}" fill="#eef2f4" stroke="#203342" stroke-width="2"/>')
for z in (23.5,63.5):
 line(x0,pt(0,z)[1],x1,pt(0,z)[1],True)
 for x in p['rear_port_columns_x_mm']:
  xx,yy=pt(x,z)
  a.append(f'<circle cx="{xx}" cy="{yy}" r="{13.8*s/2}" fill="white" stroke="#203342" stroke-width="2"/>')
  a.append(f'<circle cx="{xx}" cy="{yy}" r="{28*s/2}" fill="none" stroke="#81949f" stroke-dasharray="5 5"/>')
  line(xx-24,yy,xx+24,yy);line(xx,yy-24,xx,yy+24)
for xx in (x0,x1,pt(180,0)[0],pt(-180,0)[0]):line(xx,oy-75,xx,oy-5)
dim(x0,x1,oy-65,'410 body width')
dim(x0,pt(180,0)[0],oy-22,'25');dim(pt(180,0)[0],pt(-180,0)[0],oy-22,'360 between outer pairs');dim(pt(-180,0)[0],x1,oy-22,'25')
for z in (0,23.5,63.5,87):
 yy=pt(0,z)[1];line(x1+10,yy,x1+70,yy);text(x1+78,yy+6,f'Z {z:g}',17)
line(x1+35,pt(0,23.5)[1],x1+35,pt(0,63.5)[1]);text(x1+42,pt(0,43.5)[1]+6,'40',18)
text(65,550,'4 × G1/4 BSPP FEMALE — ISO 228-1, FITTING O-RING FACE SEAL',23)
for i,t in enumerate([
 'Centres: X −180 / +180; Z 23.5 / 63.5. Flat rear sealing face at Y40.',
 'Pilot Ø11.80 × 20 full diameter from rear face, to gallery axis Y20; 118° drill point.',
 'Entry Ø13.80 × 1 deep; full thread 8 minimum AFTER entry (9 minimum from face).',
 'Preserve a flat Ø28 sealing land around each port. Dashed circles are reference lands, not grooves.',
 'No rear bosses. No rear cover. Existing 40 mm slab and 3 mm front bosses retained.',
 'Each rear port joins the gallery of the front port directly opposite it; two wet networks total.',
 'Unused ports require G1/4 face-sealing plugs. External deburr only; clean and flush internal bores.',
 'Threads in STEP are pilot cylinders, not finished plain bores. This sheet is not a supplier release.'
]):text(65,595+i*34,t,20)
text(65,904,'Rear view reverses left/right relative to the front. Coordinate signs use the existing P datum.',17)
a.append('</g></svg>');(out/'rear-port-layout.svg').write_text('\n'.join(a))
