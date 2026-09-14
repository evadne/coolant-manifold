"""Dimensioned front elevation of the K POM body, for spacing review only."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'cad/iterations/K-long-bore.json').read_text())
out=ROOT/'output/long-bore-K';out.mkdir(parents=True,exist_ok=True)
s=3.;ox=760.;oy=270.;h=p['body_height'];w=p['body_width']
xs=[(i-4.5)*p['port_pitch'] for i in range(10)]
a=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="860" viewBox="0 0 1600 860"><rect width="1600" height="860" fill="#f7f9fa"/><g font-family="Arial,sans-serif" fill="#223341">']
def text(x,y,t,size=20,anchor='middle'):
 a.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}">{t}</text>')
def line(x1,y1,x2,y2):a.append(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#637985" stroke-width="1.5" fill="none"/>')
def dim(x1,x2,y,t):
 line(x1,y,x2,y);line(x1,y-6,x1,y+6);line(x2,y-6,x2,y+6);text((x1+x2)/2,y-13,t)
def pt(x,z):return ox+x*s,oy+(h-z)*s
text(70,60,'TEN PAIRS / 40 × 40 mm SPACING',32,'start')
text(70,100,'Revision K • 410 mm POM body • Front elevation with faceplate and fittings omitted',20,'start')
text(70,132,'Layout for review; dimensions are drawing annotations, not product markings.',18,'start')
left=ox-w/2*s;right=ox+w/2*s
# Body elevation and boss/port projections. No threaded helix is implied.
a.append(f'<rect x="{left}" y="{oy}" width="{w*s}" height="{h*s}" fill="#343c43"/>')
for z in p['port_rows_z']:
 for x in xs:
  cx,cy=pt(x,z)
  for radius,fill in [(14,'#737e87'),(5.9,'#10171d')]:a.append(f'<circle cx="{cx}" cy="{cy}" r="{radius*s}" fill="{fill}"/>')
for x,z in p['faceplate_mounts_xz']:
 cx,cy=pt(x,z);a.append(f'<circle cx="{cx}" cy="{cy}" r="{1.65*s}" fill="#111920"/>')
dim(left,right,190,'410 mm body')
dim(ox-180*s,ox+180*s,238,'360 mm — first to last port centre')
y=oy+h*s+60
dim(ox+xs[4]*s,ox+xs[5]*s,y,'40 mm')
for x in [xs[4],xs[5]]:line(*pt(x,0),ox+x*s,y+8)
dim(left,ox-180*s,y+52,'25 mm')
dim(ox+180*s,right,y+52,'25 mm')
for x in [-w/2,-180,180,w/2]:line(ox+x*s,oy+h*s+8,ox+x*s,y+59)
x=right+55;zlo=pt(0,23.5)[1];zhi=pt(0,63.5)[1]
line(x,zhi,x,zlo);line(x-6,zhi,x+6,zhi);line(x-6,zlo,x+6,zlo)
text(x+15,(zhi+zlo)/2+7,'40 mm',20,'start')
text(70,738,'Twenty front G1/4 ports. Ø28 mm bosses. QD3 Ø23.7 mm pull-ring reference: 16.3 mm nominal gap.',20,'start')
text(70,777,'25 mm is centre-to-end distance; the nominal margin beyond each Ø28 boss plus R1 root is 10 mm.',20,'start')
text(70,816,'Four reusable side G1/4 ports remain. End fitting space is shown separately in the assembled views.',19,'start')
a.append('</g></svg>');(out/'front-spacing.svg').write_text('\n'.join(a)+'\n')
