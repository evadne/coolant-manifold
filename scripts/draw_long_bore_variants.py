"""Dimensioned front-plate and side-fitting envelope drafts for I/J, in mm."""
from pathlib import Path
from xml.sax.saxutils import escape
import json
ROOT=Path(__file__).resolve().parents[1]

for rev in ('I','J'):
 p=json.loads((ROOT/f'cad/iterations/{rev}-long-bore.json').read_text())
 out=ROOT/f'output/long-bore-{rev}';out.mkdir(parents=True,exist_ok=True)
 pairs=p['front_pair_count'];xs=[(i-(pairs-1)/2)*p['port_pitch'] for i in range(pairs)]
 w=p['body_width'];h=p['body_height'];e=p['side_fitting_clearance'];f=p['faceplate_fastener']
 projection=max(e['elbow_base_height']+e['elbow_head_height'],e['elbow_outlet_axis_from_seat_inferred']+e['compression_diameter']/2)
 for kind in ('faceplate','side-clearance'):
  a=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1060" viewBox="0 0 1600 1060">','<rect width="1600" height="1060" fill="white"/>','<g font-family="Arial,sans-serif" fill="#193343">']
  def text(x,y,t,size=18,anchor='start',colour='#193343'):
   a.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{colour}">{escape(t)}</text>')
  def line(x1,y1,x2,y2,colour='#627480',dash=''):
   a.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" stroke-width="1.3" stroke-dasharray="{dash}"/>')
  def rect(x,y,ww,hh,fill,stroke='#193343'):
   a.append(f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" fill="{fill}" stroke="{stroke}"/>')
  def circle(x,y,r,fill='white',stroke='#193343'):
   a.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}"/>')
  def dimension(x1,x2,y,t):
   line(x1,y,x2,y);line(x1,y-7,x1,y+7);line(x2,y-7,x2,y+7);text((x1+x2)/2,y-12,t,18,'middle')
  text(60,58,f'REVISION {rev} / {int(w)} mm POM / {pairs} front pairs',30)
  text(60,96,'All dimensions in mm · Initial draft for DFM · No pressure or rack-fit qualification',18)
  if kind=='faceplate':
   text(60,138,'FRONT RACK FACEPLATE / OUTSIDE FACE / 3.00 ±0.10 FINISHED STAINLESS',20)
   s=2.7;ox=800;oy=230
   def pt(x,z):return ox+x*s,oy+(h-z)*s
   rect(*pt(-p['rack_width']/2,h),p['rack_width']*s,h*s,'#e7edf0')
   # Body outline is a reference behind the steel, not a cut or mark.
   for x in (-w/2,w/2):line(*pt(x,0),*pt(x,h),'#79909f','5 4')
   for z in p['port_rows_z']:
    for x in xs:circle(*pt(x,z),p['faceplate_port_clearance']/2*s)
   for x,z in p['faceplate_mounts_xz']:
    circle(*pt(x,z),f['clearance_diameter']/2*s)
    circle(*pt(x,z),f['countersink_diameter']/2*s,'none','#277d9b')
   for x in (-232.55,232.55):
    for z in (5.4,81.6):
     cx,cy=pt(x,z);a.append(f'<rect x="{cx-5*s}" y="{cy-3.5*s}" width="{10*s}" height="{7*s}" rx="{3.5*s}" fill="white" stroke="#193343"/>')
   dimension(ox-p['rack_width']/2*s,ox+p['rack_width']/2*s,oy-32,'482.6 overall / rack fixing centres 465.1')
   dimension(ox-w/2*s,ox+w/2*s,oy+h*s+55,f'{w:g} POM width behind faceplate')
   text(60,565,f'{2*pairs} × Ø32 +0.20/0 windows. Rows Z = 23.5 / 63.5. X = '+', '.join(f'{x:g}' for x in xs),17)
   text(60,600,f'{len(p["faceplate_mounts_xz"])} × Ø4.5 +0.10/0 through; Ø8.0 +0.10/0 × 90° countersink, outside face.',19)
   mounts=sorted(set(x for x,z in p['faceplate_mounts_xz']))
   text(60,636,'M4 centres: X = '+', '.join(f'{x:g}' for x in mounts)+'; each at Z = 7 and 80.',18)
   text(60,672,'Datum: X = 0 at width centre; Z = 0 at bottom. Plate height 87. Hole/window centres ±0.10.',18)
   text(60,708,'Four 10 × 7 rack slots, R3.5 ends: X = ±232.55; Z = 5.4 / 81.6. Other dimensions ±0.15.',18)
   text(60,759,'CUT DXF contains outline, port windows, screw through holes and rack slots only.',18)
   text(60,794,'Machine countersinks after cutting; do not laser-cut the blue countersink circles.',18)
   text(60,829,'304 or 316 stainless, dry structural plate. Deburr, flatten and inspect finished thickness.',18)
   text(60,864,'Use A4 M4 × 12 DIN 7991 socket countersunk screws; specified DIN 965 Z Pozi accepted.',18)
   text(60,899,'Dashed body edges are drawing references only. No surface text, lines or markings on the product.',17)
  else:
   text(60,138,'TOP VIEW / REARWARD 90° ELBOW + 10/16 COMPRESSION ENVELOPES',20)
   s=2.65;ox=800;oy=310
   def pt(x,y):return ox+x*s,oy+y*s
   for x in (-225,225):line(*pt(x,-12),*pt(x,95),'#b05139','7 5')
   rect(*pt(-w/2,0),w*s,40*s,'#c9d4db')
   rect(*pt(-241.3,-3),482.6*s,3*s,'#728997')
   for sign in (-1,1):
    x=sign*w/2
    def lr(u1,u2,y1,y2,fill):rect(*pt(min(x+sign*u1,x+sign*u2),y1),(u2-u1)*s,(y2-y1)*s,fill)
    lr(0,8.8,17,35,'#bac7cf');lr(8.8,26.8,17,35,'#dae2e7')
    lr(17.8-11,17.8+11,35,47.2,'#8db1c4')
    text(*pt(x+sign*17.8,59),'10/16',15,'middle')
   dimension(*[ox+v*s for v in (-225,225)],oy-100,'450 nominal equipment opening assumption')
   dimension(ox-w/2*s,ox+w/2*s,oy-42,f'{w:g} POM body')
   dimension(ox-(w/2+projection)*s,ox+(w/2+projection)*s,oy+83*s,f'{w+2*projection:g} across fitted body (nominal)')
   text(60,618,'Drawing-derived side projection: max(26.8, 17.8 + Ø22/2) = 28.8 mm.',21)
   text(60,656,'17.8 mm outlet-centre height is inferred as 8.8 + 18/2 from the supplied BP-90R drawing.',17)
   text(60,691,'Compression fitting adds 12.2 mm rearwards; its Ø22 body sets the lateral limit.',18)
   text(60,726,f'With 4 mm plug heads: {w+8:g} mm across body. With 30 mm allowances: {w+60:g} mm.',18)
   margin=(450-w)/2-projection
   text(60,769,(f'Nominal fitting margin: {margin:g} mm each side. Full 30 mm allowances leave zero margin.' if margin>0 else f'Fittings exceed the assumed opening by {-margin:g} mm per side; plugs exceed it by 4 mm.'),18,colour='#a44b32')
   text(60,811,'The 482.6 mm faceplate sits in front of the opening; it is not part of the insertion-width budget.',18)
   text(60,847,'These are fitting envelopes, not exact supplier solids. Tubes, bend radius, tolerances and rail geometry are excluded.',17)
   text(60,883,'Four side ports share these two top-view silhouettes. Shown outlets point rearwards; other angles need review.',17)
   text(60,919,'Angled insertion and final installed clearance require an actual rack check; no insertion path is validated here.',17)
  text(60,1018,f'REVISION {rev} / '+('faceplate-flat.dxf + faceplate.step' if kind=='faceplate' else 'User-supplied BP-90R and Barrow drawings / nominal envelope study'),16)
  a.append('</g></svg>');(out/f'{kind}-drawing.svg').write_text('\n'.join(a)+'\n')
print('Wrote four separate I/J drawings.')
