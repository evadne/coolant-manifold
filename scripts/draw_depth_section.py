"""Dimensioned section between front port columns; bosses shown in projection."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--iteration',default='O');args=parser.parse_args()
p=json.loads((ROOT/f'cad/iterations/{args.iteration}-long-bore.json').read_text())
out=ROOT/f'output/long-bore-{args.iteration}'
s=5.;ox=280.;oy=190.;D=p['body_depth'];H=p['body_height'];Y=p['gallery_axis_y'];R=p['gallery_diameter']/2;BH=p['port_boss_height']
a=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="840" viewBox="0 0 1200 840"><rect width="1200" height="840" fill="#f7f9fa"/><g font-family="Arial,sans-serif" fill="#223341">']
def text(x,y,t,size=20,anchor='start'):a.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}">{t}</text>')
def line(x1,y1,x2,y2,dash=''):a.append(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#637985" stroke-width="1.5" fill="none" stroke-dasharray="{dash}"/>')
def dim(x1,x2,y,label,size=18):
    line(x1,y,x2,y);line(x1,y-6,x1,y+6);line(x2,y-6,x2,y+6);text((x1+x2)/2,y-12,label,size,'middle')
def zpos(z):return oy+(H-z)*s
text(65,65,f'REVISION {args.iteration} / CENTRED LONGITUDINAL GALLERIES',30)
text(65,103,'Schematic section between front port columns; dimensions in mm.',18)
a.append(f'<rect x="{ox}" y="{oy}" width="{D*s}" height="{H*s}" fill="#b7bfc4" stroke="#283944" stroke-width="2"/>')
a.append(f'<rect x="{ox-3*s}" y="{oy}" width="{3*s}" height="{H*s}" fill="#718b9b"/>')
for z in p['port_rows_z']:
    cy=zpos(z)
    a.append(f'<circle cx="{ox+Y*s}" cy="{cy}" r="{R*s}" fill="#c8e9f3" stroke="#186980" stroke-width="2"/>')
    a.append(f'<rect x="{ox-BH*s}" y="{cy-14*s}" width="{BH*s}" height="{28*s}" fill="none" stroke="#72848e" stroke-width="1.5" stroke-dasharray="6 4"/>')
    line(ox+Y*s-40,cy,ox+Y*s+40,cy,'5 4')
# At X0 the two M4 pilot holes appear in this section.
for z in [7,80]:
    a.append(f'<rect x="{ox}" y="{zpos(z)-1.65*s}" width="{14*s}" height="{3.3*s}" fill="#f7f9fa"/>')
line(ox+Y*s,oy-15,ox+Y*s,oy+H*s+15,'7 5')
dim(ox,ox+D*s,155,f'{D:g} slab')
dim(ox,ox+(Y-R)*s,410,f'{Y-R:g}',16)
dim(ox+(Y+R)*s,ox+D*s,410,f'{D-Y-R:g}',16)
dim(ox-BH*s,ox+D*s,690,f'{D+BH:g} overall POM, including bosses')
text(ox-35,oy+H*s+30,'FRONT',16,'end');text(ox+D*s+15,oy+H*s+30,'REAR',16)
text(565,215,f'Body: {p["body_width"]:g} × {D:g} × {H:g} mm',24)
text(565,262,f'Two Ø{2*R:g} galleries at Y{Y:g}',22)
text(565,307,f'{Y-R:g} mm ahead and {D-Y-R:g} mm behind',22)
text(565,352,'Front branch holes interrupt the front wall',18)
text(565,379,'at the port columns; they are outside this section.',18)
text(565,431,'Dashed outlines: 6 mm boss projections.',18)
text(565,458,'Blue strip: 3 mm stainless faceplate.',18)
text(565,485,'White recesses: blind M4 pilot holes at X0.',18)
text(565,539,'Side ports are centred in the body depth.',20)
text(565,570,f'Ø22 sealing lands have {min(Y,D-Y)-11:g} mm edge reserve',18)
text(565,597,'to both the front and rear of the side face.',18)
text(65,755,'Nominal geometry review; not a pressure or stiffness qualification.',18)
text(65,789,'Side-elbow / optional cage-nut clearance is recorded separately in rack-clearance-review.json.',18)
a.append('</g></svg>');(out/'depth-section.svg').write_text('\n'.join(a)+'\n')
