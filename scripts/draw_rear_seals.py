"""Rear groove review and stock-ring sizing; geometry read from CAD parameters."""
from pathlib import Path
import json,math
from html import escape
R=Path(__file__).resolve().parents[1];p=json.loads((R/'cad/parameters.json').read_text())
out=R/'output';s=2.85;ox=800;oy=185
w=p['channel_width'];L=p['channel_length'];off=p['seal_offset'];gw=p['seal_groove_width'];gd=p['seal_groove_depth'];cs=p['seal_cross_section']
cl=L+2*off;cw=w+2*off;perimeter=2*(cl-cw)+math.pi*cw
zero_id=perimeter/math.pi-cs
r={'revision':p['revision'],'groove_centreline_length_mm':perimeter,'zero_stretch_equivalent_round_ring_ID_mm':zero_id,'groove_width_mm':gw,'groove_depth_mm':gd,'candidates':[],'section_comparison':[]}
for d in (260,262,265):
 free=math.pi*(d+cs);stretch=perimeter/free-1;stretched_cs=cs/math.sqrt(1+stretch)
 r['candidates'].append({'free_ring_ID_mm':d,'cross_section_mm':cs,'centreline_stretch_percent':stretch*100,'estimated_stretched_cross_section_mm':stretched_cs,'estimated_squeeze_percent':(1-gd/stretched_cs)*100,'status':'Dimension candidate only; EPDM compound, moulded construction and supply to be confirmed'})
for c in (1,1.5,2):
 r['section_comparison'].append({'cross_section_mm':c,'illustrative_groove_depth_for_20_percent_squeeze_mm':.8*c,'free_protrusion_mm':.2*c,'squeeze_change_from_0_05_mm_gap_percentage_points':.05/c*100})
r['rs_candidate']={'stock_number':'258-0460','url':'https://uk.rs-online.com/web/p/gaskets-o-rings/2580460','checked_date':'2026-09-14','checked_using':'Computer Use; RS product page and delivery dialog','ID_mm':253.59,'cross_section_mm':3.53,'material':'EPDM','standard':'AS568-274 / BS 1806-274','pack_quantity':2,'price_per_bag_GBP_ex_VAT':4.92,'availability_verbatim':'24 unit(s) ready to ship','free_centreline_length_mm':math.pi*(253.59+3.53),'stretch_on_existing_centreline_percent':100*(perimeter/(math.pi*(253.59+3.53))-1),'status':'Stocked alternative only; requires a new gland design, not compatible with revision E grooves'}
(out/'analysis'/'rear-seal-sizing.json').write_text(json.dumps(r,indent=2)+'\n')
a=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1130" viewBox="0 0 1600 1130">','<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto-start-reverse"><path d="M0 0 L8 4 L0 8" fill="none" stroke="#607080"/></marker></defs>','<rect width="1600" height="1130" fill="#f5f7f9"/>','<g font-family="Arial,sans-serif" fill="#182d3b">']
def text(x,y,t,size=20,colour='#182d3b',anchor='start'):
 a.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{colour}" text-anchor="{anchor}">{escape(t)}</text>')
def rect(x,y,w,h,fill,rx=0,stroke='none'):
 a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>')
def line(x1,y1,x2,y2,arrow=False,dash=False):
 a.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#607080" stroke-width="1.5"'+(' marker-start="url(#arr)" marker-end="url(#arr)"' if arrow else '')+(' stroke-dasharray="6 5"' if dash else '')+'/>')
def capsule(length,width,z,fill):
 rect(ox-length*s/2,oy+(p['body_height']-z-width/2)*s,length*s,width*s,fill,width*s/2)
text(65,64,'Rear galleries and O-ring grooves',36)
text(65,101,f"RM8 / 2U · Revision {p['revision']} geometry · Rear cover removed · Dimensions in mm",20,'#526777')
line(ox-p['body_width']*s/2,151,ox+p['body_width']*s/2,151,True)
text(800,139,'440 POM body',18,anchor='middle')
rect(ox-p['body_width']*s/2,oy,p['body_width']*s,p['body_height']*s,'#25343e',2)
xs=[(i-p['branch_count']/2)*p['port_pitch'] for i in range(p['branch_count']+1)]
for j,z in enumerate(p['port_rows_z']):
 capsule(cl+gw,cw+gw,z,'#efb542');capsule(cl-gw,cw-gw,z,'#25343e')
 capsule(L,w,z,'#28617d' if j==0 else '#935849')
 for x in xs:
  a.append(f'<circle cx="{ox-x*s}" cy="{oy+(p["body_height"]-z)*s}" r="{p["tap_drill_diameter"]*s/2}" fill="#14242e"/>')
 text(800,oy+(p['body_height']-z)*s+6,'SUPPLY' if j==0 else 'RETURN',16,'#ffffff','middle')
bolts=[(x,z) for z in (5.5,p['body_height']/2,p['body_height']-5.5) for x in xs]+[(x,z) for x in (-213,213) for z in p['port_rows_z']]
for x,z in bolts:
 a.append(f'<circle cx="{ox-x*s}" cy="{oy+(p["body_height"]-z)*s}" r="{1.65*s}" fill="#c9d2d9"/>')
text(800,475,'Yellow highlights the two empty grooves; each takes one complete O-ring.',21,anchor='middle')
text(800,507,f'Each gallery: {L:g} × {w:g} opening · Groove centreline: {cl:g} × {cw:g} · Path length: {perimeter:.2f}',19,'#526777','middle')
text(65,573,'Gland section before the cover closes',25)
# A local section, 60 pixels/mm. The round ring rests on the groove floor.
k=60;x=245;top=690;bottom=top+gd*k;right=x+gw*k
path=f'M100 {top} H{x} V{bottom} H{right} V{top} H615 V870 H100 Z'
a.append(f'<path d="{path}" fill="#25343e"/>')
a.append(f'<circle cx="{(x+right)/2}" cy="{bottom-cs*k/2}" r="{cs*k/2}" fill="#efb542" stroke="#9a7122" stroke-width="2"/>')
line(110,top,610,top,dash=True)
line(x,616,right,616,True);text((x+right)/2,604,f'{gw:g} groove width',18,anchor='middle')
line(655,top,655,bottom,True);text(675,(top+bottom)/2+6,f'{gd:g} deep',18)
text(105,907,f'Ø{cs:g} ring · {cs-gd:.2f} nominal protrusion · {(1-gd/cs)*100:.0f}% nominal squeeze',20)
text(105,937,'Dashed line: POM mating face / closed cover underside.',17,'#526777')
text(860,573,'Use a complete circular ring',25)
text(860,619,'The ring bends into the capsule-shaped groove.',20)
text(860,652,'No cut, splice or adhesive joint is required.',20)
text(860,701,f'Zero-stretch equivalent size: {zero_id:.1f} ID × {cs:g} section',20)
text(860,747,'Candidate size',18,'#526777');text(1110,747,'Centreline stretch',18,'#526777')
for i,c in enumerate(r['candidates']):
 text(860,782+34*i,f"{c['free_ring_ID_mm']:g} × {cs:g} mm",20);text(1110,782+34*i,f"{c['centreline_stretch_percent']:.2f}%",20)
text(860,904,'Size candidates are not confirmed stock selections.',17,'#926223')
text(860,935,'Specify EPDM, 70 Shore A, one-piece moulded.',18)
text(65,1011,'2 mm remains the baseline: more compression allowance than a 1–1.5 mm section.',22)
text(65,1045,'Select the purchased ring and its tolerances before releasing the gland dimensions.',19,'#526777')
text(65,1096,'REVIEW DRAWING · Cross-section enlarged · Highlights are explanatory · No pressure rating',17,'#926223')
a.append('</g></svg>');(out/'rear-seal-review.svg').write_text('\n'.join(a))
print(json.dumps(r,indent=2))
