"""Compare eight and forty secured rack positions on the new 10U R2 plate."""
from pathlib import Path
import json,gzip
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from review_radiator_fea import read_case,WORK
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/radiator-R2/analysis';OUT.mkdir(exist_ok=True)
names=['R2-plate-t2-h6-s40-distributed','R2-plate-t2-h3-s40-distributed','R2-plate-t2-h3-s8-distributed','R2-plate-t2-h3-s40-top']
reports=[];raws=[]
for name in names:
 r,raw=read_case(name);meta=raw[0]
 r.update(cg_offset_mm=meta['payload_cg_mm'],payload_mass_kg=meta['payload_mass_kg'])
 reports.append(r);raws.append(raw)
convergence={key:abs(reports[0][key]/reports[1][key]-1) for key in ['max_out_of_plane_mm','max_recovered_surface_von_mises_MPa']}
assert max(convergence.values())<.05,convergence
improvement={key:1-reports[1][key]/reports[2][key] for key in convergence}
report={'revision':'R2','plate_height_mm':444.5,'rack_units':10,'plate_thickness_mm':2,
 'plate_mass_kg':json.loads((ROOT/'output/radiator-R2/verification.json').read_text())['plate_mass_kg'],
 'payload_kg':15,'cases':reports,'coarse_to_fine_relative_change':convergence,
 'relative_reduction_8_to_40_secured_fixings':improvement,
 'limits':'Linear elastic plate only. Added empty holes are not supports. Actual screws, washers, cage nuts, rail compliance and radiator M3 interface are not qualified.'}
(OUT/'assessment.json').write_text(json.dumps(report,indent=2)+'\n')
fig,axs=plt.subplots(1,2,figsize=(12,6.5),layout='constrained')
for ax,idx,label in zip(axs,[2,1],['Eight secured rack fixings','Forty secured rack fixings']):
 meta,xy,u,tris,stress=raws[idx];tri=mtri.Triangulation(xy[:,0],xy[:,1],tris)
 im=ax.tripcolor(tri,np.abs(u[:,2]),shading='gouraud',vmin=0,vmax=max(reports[1]['max_out_of_plane_mm'],reports[2]['max_out_of_plane_mm']),cmap='viridis')
 ax.set_aspect('equal');ax.set_xlabel('Horizontal position / mm');ax.set_ylabel('Height / mm')
 ax.set_title(label+f'\nPeak movement {reports[idx]["max_out_of_plane_mm"]:.4f} mm')
 fig.colorbar(im,ax=ax,label='Out-of-plane movement / mm')
fig.suptitle('R2: same 444.5 mm / 10U / 2 mm plate in both cases\n15 kg payload + plate; 150 mm effective rearward CG. Undeformed outline.',fontsize=12)
fig.savefig(OUT/'fixing-comparison.png',dpi=180);plt.close(fig)
for name in names:
 for ext in ['inp','dat']:
  with gzip.GzipFile(filename=str(OUT/(name+'.'+ext+'.gz')),mode='wb',mtime=0) as f:f.write((WORK/(name+'.'+ext)).read_bytes())
print(json.dumps(report,indent=2))
