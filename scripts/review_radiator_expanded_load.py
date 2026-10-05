"""Assess the expanded radiator equipment budget with solved full-plate cases."""
from pathlib import Path
import json,gzip
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
from review_radiator_fea import read_case, case_bytes
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/radiator-expanded-load';OUT.mkdir(exist_ok=True)
plate_mass=json.loads((ROOT/'output/radiator-R1/verification.json').read_text())['plate_mass_kg']*2/3
items=[
 {'item':'SuperNova 1260 radiator, net dry','mass_kg':4.225,'basis':'Manufacturer net weight. No deduction for removed fan plate.'},
 {'item':'2 mm stainless rack plate','mass_kg':plate_mass,'basis':'Current R1 net CAD area x 2 mm x 7900 kg/m3; no new cut profile.'},
 {'item':'8 x Noctua NF-A20 PWM','mass_kg':8*.370,'basis':'Manufacturer 370 g per fan, excluding packaging.'},
 {'item':'ULTITUBE D5 200 dry reservoir','mass_kg':1.0,'basis':'Engineering allowance, not a verified manufacturer net mass.'},
 {'item':'D5 NEXT pump','mass_kg':.5,'basis':'Engineering allowance, not a verified manufacturer net mass.'},
 {'item':'ULTITUBE coolant, 470 ml','mass_kg':.470*1.05,'basis':'Manufacturer capacity; assumed formulated-coolant density 1.05 kg/l.'},
 {'item':'Radiator and local plumbing coolant','mass_kg':2.0,'basis':'Separate provisional allowance; measure actual fill mass. Does not consume equipment allowance.'},
 {'item':'Additional equipment requested by operator','mass_kg':2.0,'basis':'Additional to all listed fans, pump, reservoir, plate and coolant.'},
]
budget=sum(x['mass_kg'] for x in items)
names=['expanded-plate-t2-h3-s8-distributed','expanded-plate-t2-h6-s4-top','expanded-plate-t2-h3-s4-top']
reports=[];data={}
for name in names:
 report,raw=read_case(name);meta=raw[0]
 report.update(payload_mass_kg=meta['payload_mass_kg'],cg_offset_mm=meta['payload_cg_mm'],total_mass_kg=meta['payload_mass_kg']+plate_mass)
 reports.append(report);data[name]=raw
for report in reports:
 report['proof_strength_to_peak_stress_ratio']=230/report['max_recovered_surface_von_mises_MPa']
convergence={key:abs(reports[1][key]/reports[2][key]-1) for key in ['max_out_of_plane_mm','max_recovered_surface_von_mises_MPa']}
assert max(convergence.values())<.05,convergence
summary={'refinement_relative_changes_300mm_case':convergence,'basis':'Expanded equipment load screening, not a rack/radiator assembly rating.',
 'mass_budget':items,'budget_total_kg':budget,'analysis_payload_kg':15,'analysis_plate_mass_kg':plate_mass,
 'analysis_total_kg':15+plate_mass,'reserve_above_budget_kg':15+plate_mass-budget,
 'unverified_masses':'Dry reservoir, pump and radiator/local coolant entries are explicit allowances; not measured net weights.',
 'geometry':'Unchanged R1 cut profile modelled at 2 mm; no fan-tab or pump-bracket redesign.',
 'mounting':'Operator: optional pump/res on 140 mm fan-hole bracket using OEM radiator plate; alternatively separate rack pump/res. Loads here all attributed to radiator plate through radiator attachment holes.',
 'cases':reports,
 'limits':['Static linear elastic S6 shell model, E200 GPa, nu0.3, ideal fixed translations at rack holes.',
 'No radiator reinforcement, bolt preload, washer contact, thread pull-out, vibration or transport impact model.',
 '150 mm or 300 mm effective CG offsets are test scenarios, not a measured product centre of gravity.',
 'Direct pump loads applied to narrow aperture webs or a different carrier are not validated by these attachment-hole loads.',
 'Eight A20 fans need appropriate fan mounting plates/adapters. Existing R1 aperture windows alone do not supply A20 mounting holes.'],
 'sources':{
 'fan':'https://www.noctua.at/en/products/nf-a20-pwm/specifications',
 'reservoir':'https://shop.aquacomputer.de/Wasserkuehlung/Ausgleichsbehaelter-Zub/Fuer-Pumpenmontage/ULTITUBE-D5-200-Ausgleichsbehaelter-fuer-D5-Pumpen::3844.html',
 'radiator':'https://download.alphacool.com/legacy/ENG_1018089_Alphacool_NexXxoS_XT45_Full_Copper_1260mm_SuperNova_Radiator.pdf'}}
(OUT/'assessment.json').write_text(json.dumps(summary,indent=2)+'\n')
meta,xy,disp,tris,stress=data[names[2]]
tri=mtri.Triangulation(xy[:,0],xy[:,1],tris)
fig,axes=plt.subplots(1,2,figsize=(12,6.5),layout='constrained')
for ax in axes:
 ax.set_aspect('equal');ax.set_xlabel('Horizontal position / mm');ax.set_ylabel('Height / mm');ax.set_facecolor('#eef1f3')
im=axes[0].tripcolor(tri,np.abs(disp[:,2]),shading='gouraud',cmap='viridis');fig.colorbar(im,ax=axes[0],label='Out-of-plane movement / mm')
im=axes[1].tripcolor(tri,facecolors=stress,shading='flat',cmap='magma');fig.colorbar(im,ax=axes[1],label='Recovered surface von Mises stress / MPa')
axes[0].set_title('2 mm plate / more demanding load case');axes[1].set_title('Elastic surface stress')
fig.suptitle('15 kg payload + 1.131 kg plate; 300 mm effective CG offset\nFour rack fixings; gravity through two upper radiator mounts. Undeformed outline.',fontsize=12)
fig.savefig(OUT/'expanded-load-analysis.png',dpi=180);plt.close(fig)
for name in names:
 for ext in ['inp','dat']:
  evidence=case_bytes(name,ext)
  with gzip.GzipFile(filename=str(OUT/(name+'.'+ext+'.gz')),mode='wb',mtime=0) as f:f.write(evidence)
print(json.dumps({k:v for k,v in summary.items() if k not in ['mass_budget','limits','sources']},indent=2))
