"""Dimensioned concept sheet and physical-size QD3 trial template (SVG)."""
import json
from pathlib import Path
from xml.sax.saxutils import escape
R=Path(__file__).resolve().parents[1];p=json.loads((R/'cad/parameters.json').read_text())
out=R/'output';xs=[-180+45*i for i in range(9)]
# One SVG unit equals one millimetre on the print template.
a=['<svg xmlns="http://www.w3.org/2000/svg" width="520mm" height="145mm" viewBox="0 0 520 145">',
'<rect width="520" height="145" fill="white"/>',
'<g font-family="Arial,sans-serif" font-size="3.2" fill="#142c3c">',
'<text x="19" y="9" font-size="5">RM8-2U / REV A — QD3 clearance trial, full size</text>',
'<text x="19" y="16">Print at 100%, no fit-to-page. Verify the 100 mm scale before use. Large-format or tiled printing required.</text>']
x0=260;y0=25
# Face shown top to bottom in screen coordinates.
a.append(f'<rect x="{x0-220}" y="{y0}" width="440" height="87" fill="#f2f5f7" stroke="#152d40" stroke-width=".5"/>')
for z in p['port_rows_z']:
    y=y0+87-z
    for i,x in enumerate(xs):
        c='#1673a4' if z<40 else '#b64e2b';cx=x0+x
        lab=('IN' if z<40 else 'OUT') if i==0 else ('S' if z<40 else 'R')+str(i)
        a.append(f'<circle cx="{cx}" cy="{y}" r="14" fill="none" stroke="#9da8ae" stroke-width=".3" stroke-dasharray="1.5 1"/>')
        a.append(f'<circle cx="{cx}" cy="{y}" r="11.85" fill="none" stroke="{c}" stroke-width=".5"/>')
        a.append(f'<circle cx="{cx}" cy="{y}" r="6.5785" fill="white" stroke="#52616b" stroke-width=".3"/>')
        a.append(f'<path d="M {cx-3} {y} h6 M {cx} {y-3} v6" stroke="#52616b" stroke-width=".2"/>')
        a.append(f'<text x="{cx}" y="{y-16}" text-anchor="middle" fill="{c}">{lab}</text>')
a.extend(['<path d="M40 130 h100 M40 127 v6 M140 127 v6" stroke="#152d40" stroke-width=".4"/>',
'<text x="90" y="126" text-anchor="middle">100 mm calibration</text>',
'<text x="180" y="128">Solid circles: Ø23.7 pull rings. Dashed: conservative Ø28 bodies.</text>',
'<text x="180" y="135">45 mm column pitch / 40 mm row pitch. Test actual mating fittings and hand access.</text>',
'</g></svg>'])
(out/'clearance-template-1to1.svg').write_text('\n'.join(a))
# Presentation drawing; not a production drawing. Explicit view directions.
b=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1100" viewBox="0 0 1600 1100">',
'<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto-start-reverse"><path d="M0 0 L7 3.5 L0 7" fill="none" stroke="#6b7d8b"/></marker></defs>',
'<rect width="1600" height="1100" fill="#f4f6f8"/>',
'<g font-family="Arial,sans-serif" fill="#192e3f">',
'<text x="65" y="70" font-size="35" font-weight="bold">RM8 / 2U coolant manifold</text>',
'<text x="65" y="108" font-size="19" fill="#526777">Revision A · Eight parallel circuits · All ports G1/4 female · Millimetres</text>']
def text(x,y,t,size=16,colour='#192e3f',anchor='start'):
    b.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{colour}" text-anchor="{anchor}">{escape(t)}</text>')
def rect(x,y,w,h,fill,stroke='#192e3f',radius=0):
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
def line(x1,y1,x2,y2,colour='#6b7d8b',dash='',arrows=False):
    extra=' marker-start="url(#arrow)" marker-end="url(#arrow)"' if arrows else ''
    b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" stroke-width="1" stroke-dasharray="{dash}"{extra}/>')
s=2.65;ox=800;oy=220
text(65,164,'FRONT / SERVICE FACE',18)
rect(ox-241.3*s,oy,482.6*s,87*s,'#d1d9de')
rect(ox-220*s,oy,440*s,87*s,'#263540')
for z in p['port_rows_z']:
    cy=oy+(87-z)*s
    for i,x in enumerate(xs):
        cx=ox+x*s;colour='#52b8ed' if z<40 else '#ffa378'
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{14*s}" fill="none" stroke="#6c808c" stroke-dasharray="5 4"/>')
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{11.85*s}" fill="#c5cfd5" stroke="{colour}" stroke-width="2.5"/>')
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{6.5785*s}" fill="#263540"/>')
        lab=('IN' if z<40 else 'OUT') if i==0 else ('S' if z<40 else 'R')+str(i)
        text(cx,cy-14*s-5,lab,13,colour,'middle')
for sign in(-1,1):
    for z in (5.4,81.6):
        rect(ox+sign*232.55*s-5*s,oy+(87-z)*s-3.5*s,10*s,7*s,'#f4f6f8','#71808b',3.5*s)
line(ox-241.3*s,oy+87*s+35,ox+241.3*s,oy+87*s+35,arrows=True)
text(800,oy+87*s+60,'482.6 overall / rack centres 465.1',17,anchor='middle')
line(ox+241.3*s+30,oy,ox+241.3*s+30,oy+87*s,arrows=True)
text(ox+241.3*s+40,oy+45*s,'87',17)
line(ox-135*s,oy-23,ox-90*s,oy-23,arrows=True)
text(ox-112.5*s,oy-34,'45 pitch',15,anchor='middle')
text(65,550,'REAR / COVER REMOVED',18)
text(65,578,'Two uninterrupted pockets, each with its own perimeter seal. No groups or internal plugs.',16,'#526777')
ry=615
rect(ox-220*s,ry,440*s,87*s,'#e1e6e9')
for z,col in zip(p['port_rows_z'],('#258fc6','#d66c3c')):
    cy=ry+(87-z)*s
    rect(ox-204.9*s,cy-12.9*s,409.8*s,25.8*s,'none','#333f48',12.9*s)
    rect(ox-200*s,cy-8*s,400*s,16*s,col,col,8*s)
    text(800,cy+5,'SUPPLY — one common gallery' if z<40 else 'RETURN — one common gallery',16,'white','middle')
for z in(5.5,43.5,81.5):
    for x in xs:
        b.append(f'<circle cx="{ox+x*s}" cy="{ry+(87-z)*s}" r="4.3" fill="white" stroke="#758592"/>')
for x in(-213,213):
    for z in p['port_rows_z']:
        b.append(f'<circle cx="{ox+x*s}" cy="{ry+(87-z)*s}" r="4.3" fill="white" stroke="#758592"/>')
text(65,890,'Clearance around the couplings',22)
text(65,925,'Ø23.7 release rings: 21.3 horizontal gap / 16.3 vertical gap.',18)
text(65,954,'Ø28 conservative body envelopes: 17 horizontal gap / 12 vertical gap.',18)
text(65,985,'Allow 100 mm service space forward of the face; verify release travel and hose bends with actual fittings.',17,'#526777')
text(65,1047,'INITIAL MODEL / FOR FEEDBACK AND VENDOR DFM — NOT PRESSURE RATED',17,'#a55432')
text(1535,1047,'2026-09-14',16,'#526777','end')
b.append('</g></svg>');(out/'layout.svg').write_text('\n'.join(b))
print('Wrote layout.svg and clearance-template-1to1.svg')
