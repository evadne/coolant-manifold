"""Rear groove review and stock-ring sizing; geometry read from CAD parameters."""
from pathlib import Path
import json,math
from html import escape
R=Path(__file__).resolve().parents[1];p=json.loads((R/'cad/parameters.json').read_text())
out=R/'output';s=2.85;ox=800;oy=185
w=p['channel_width'];L=p['channel_length'];off=p['seal_offset'];gw=p['seal_groove_width'];gd=p['seal_groove_depth'];cs=p['seal_cross_section']
cl=L+2*off;cw=w+2*off;perimeter=2*(cl-cw)+math.pi*cw
zero_id=perimeter/math.pi-cs
ring=p['seal_ring'];ring_id=ring['ID'];free=math.pi*(ring_id+cs);ratio=perimeter/free;installed_cs=cs/math.sqrt(ratio)
# Review AS568 allowances, pending confirmation for the purchased EPDM batch.
# Centreline length/height +/-0.10 mm, groove width/depth +/-0.05 mm.
path_tol=.10*(2+math.pi-2)
cases=[]
for dd in (-ring['cross_section_tolerance_review'],ring['cross_section_tolerance_review']):
 for di in (-ring['ID_tolerance_review'],ring['ID_tolerance_review']):
  for dl in (-path_tol,path_tol):
   d=cs+dd; elongation=(perimeter+dl)/(math.pi*(ring_id+di+d));effective=d/math.sqrt(elongation)
   for dh in (-.05,.05):
    for db in (-.05,.05):
     cases.append({'squeeze_percent':100*(1-(gd+dh)/effective),'fill_percent':100*math.pi*effective**2/(4*(gw+db)*(gd+dh)),'stretch_percent':100*(elongation-1)})
r={'revision':p['revision'],'groove_centreline_length_mm':perimeter,'groove_centreline_overall_length_mm':cl,'groove_centreline_overall_height_mm':cw,'groove_width_mm':gw,'groove_depth_mm':gd,'free_ring_ID_mm':ring_id,'ring_cross_section_mm':cs,'ring_free_centreline_length_mm':free,'centreline_stretch_percent':100*(ratio-1),'estimated_installed_cross_section_mm':installed_cs,'nominal_squeeze_before_stretch_percent':100*(1-gd/cs),'estimated_squeeze_after_stretch_percent':100*(1-gd/installed_cs),'estimated_protrusion_after_stretch_mm':installed_cs-gd,'estimated_gland_fill_after_stretch_percent':100*math.pi*installed_cs**2/(4*gw*gd),'tolerance_review':{'status':ring['tolerance_status'],'ID_plus_minus_mm':ring['ID_tolerance_review'],'cross_section_plus_minus_mm':ring['cross_section_tolerance_review'],'centreline_overall_length_and_height_plus_minus_mm':.10,'groove_width_and_depth_plus_minus_mm':.05,'squeeze_percent_range':[min(c['squeeze_percent'] for c in cases),max(c['squeeze_percent'] for c in cases)],'fill_percent_range':[min(c['fill_percent'] for c in cases),max(c['fill_percent'] for c in cases)],'stretch_percent_range':[min(c['stretch_percent'] for c in cases),max(c['stretch_percent'] for c in cases)],'excludes':'Coolant swell, thermal expansion, cover separation/creep and nonuniform deformation; neutral path taken on groove centreline'},'selected_ring':{'stock_number':ring['stock_number'],'url':'https://uk.rs-online.com/web/p/gaskets-o-rings/2580460','material':ring['material'],'standard':ring['standard'],'pack_quantity':2,'stock_checked_date':'2026-09-14','availability_verbatim':'24 unit(s) ready to ship','price_per_bag_GBP_ex_VAT':4.92}}
assert min(c['squeeze_percent'] for c in cases)>15
assert max(c['fill_percent'] for c in cases)<85
assert max(c['stretch_percent'] for c in cases)<3
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
bolts=[(x,z) for z in (p['cover_bolt_edge_offset'],p['body_height']/2,p['body_height']-p['cover_bolt_edge_offset']) for x in xs]+[(x,z) for x in (-213,213) for z in p['port_rows_z']]
for x,z in bolts:
 a.append(f'<circle cx="{ox-x*s}" cy="{oy+(p["body_height"]-z)*s}" r="{1.65*s}" fill="#c9d2d9"/>')
text(800,475,'Yellow highlights the two empty grooves; each takes one complete O-ring.',21,anchor='middle')
text(800,507,f'Each gallery: {L:g} × {w:g} opening · Groove centreline: {cl:g} × {cw:g} · Path length: {perimeter:.2f}',19,'#526777','middle')
text(65,573,'Gland section before the cover closes',25)
# A local section, 60 pixels/mm. The round ring rests on the groove floor.
k=40;x=245;top=690;bottom=top+gd*k;right=x+gw*k
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
text(860,701,f'Selected: {ring_id:g} mm ID × {cs:g} mm section',20)
text(860,747,'RS 258-0460 · EPDM · AS568-274 / BS 1806-274',19)
text(860,787,f'Nominal ring elongation: {100*(ratio-1):.2f}%',20)
text(860,824,f'Estimated squeeze after stretch: {100*(1-gd/installed_cs):.1f}%',20)
text(860,861,f'Estimated gland fill after stretch: {r["estimated_gland_fill_after_stretch_percent"]:.1f}%',20)
text(860,904,'Two complete rings; one around each gallery.',18)
text(860,935,'Cover seats on the POM lands to set compression.',18)
text(65,1011,f'Grooves {gw:g} wide × {gd:g} deep · Centreline end radius {cw/2:g} · Seal land {off-gw/2:g}',22)
text(65,1045,'Nominal design checked; confirm ring tolerances, coolant and cover preload before manufacture.',19,'#526777')
text(65,1096,'REVIEW DRAWING · Cross-section enlarged · Highlights are explanatory · No pressure rating',17,'#926223')
a.append('</g></svg>');(out/'rear-seal-review.svg').write_text('\n'.join(a))
print(json.dumps(r,indent=2))
