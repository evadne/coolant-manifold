"""Read CalculiX DAT results, check equilibrium/convergence and plot fields."""
from pathlib import Path
import json,gzip,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'tmp/radiator-fea'; OUT=ROOT/'output/radiator-FEA';OUT.mkdir(exist_ok=True)
def vm(s):
 xx,yy,zz,xy,xz,yz=s
 return math.sqrt(((xx-yy)**2+(yy-zz)**2+(zz-xx)**2)/2+3*(xy*xy+xz*xz+yz*yz))
def read_case(name):
 meta=json.loads((WORK/(name+'.json')).read_text());u={};stress={};reaction=None;reactions={};mode=''
 for line in (WORK/(name+'.dat')).read_text().splitlines():
  if 'displacements (' in line:mode='u';continue
  if 'forces (' in line:mode='r';continue
  if 'total force (' in line:mode='total';continue
  if 'stresses (' in line:mode='s';continue
  v=line.split()
  try:
   if mode=='u' and len(v)==4:u[int(v[0])]=np.array(list(map(float,v[1:])))
   if mode=='r' and len(v)==4:reactions[int(v[0])]=np.array(list(map(float,v[1:])))
   if mode=='s' and len(v)>=8:stress.setdefault(int(v[0]),{})[int(v[1])]=np.array(list(map(float,v[2:8])))
   if mode=='total' and len(v)==3:reaction=np.array(list(map(float,v)))
  except ValueError:pass
 ids=meta['node_ids'];xy=np.array(meta['coordinates']);disp=np.array([u[n] for n in ids])
 coord_map=dict(zip(ids,xy));reaction_moment=sum((np.cross(coord_map[n]-[0,221.3,0],r) for n,r in reactions.items()),start=np.zeros(3))
 assert len(u)==len(ids)
 # S6 uses nine integration points: three in-plane points at each of three
 # thickness positions. Recover top/bottom surface stresses linearly from
 # matching outer layers at +/-sqrt(3/5) of half-thickness.
 surface={}
 for eid,points in stress.items():
  assert set(points)==set(range(1,10))
  stresses=[]
  for i in (1,2,3):
   membrane=(points[i]+points[i+6])/2;bending=(points[i]-points[i+6])/(2*math.sqrt(.6))
   stresses.extend([membrane+bending,membrane-bending])
  surface[eid]=max(map(vm,stresses))
 peak_index=np.abs(disp[:,2]).argmax()
 report={k:meta[k] for k in ('name','thickness_mm','mesh_size_mm','nodes','elements','supports','load')}
 report.update({'max_out_of_plane_mm':float(np.abs(disp[:,2]).max()),'max_downwards_mm':float(-disp[:,1].min()),
  'peak_displacement_location_mm':xy[peak_index].tolist(),
  'max_integration_point_von_mises_MPa':max(vm(p) for points in stress.values() for p in points.values()),
  'max_recovered_surface_von_mises_MPa':max(surface.values()),'total_support_reaction_N':reaction.tolist()})
 if name.startswith('benchmark'):
  mean=np.mean(disp[abs(xy[:,0]-100)<1e-5,2]);expected=meta['benchmark_expected_tip_mm']
  report.update({'mean_tip_mm':float(mean),'Euler_Bernoulli_tip_mm':expected,'relative_error':float(abs(mean/expected-1))})
  assert report['relative_error']<.015,report
  report['expected_root_bending_stress_MPa']=75.
  assert abs(report['max_recovered_surface_von_mises_MPa']/75.-1)<.03
 else:
  mass=json.loads((ROOT/'output/radiator-R1/verification.json').read_text())['plate_mass_kg']*meta['thickness_mm']/3
  expected=meta.get('payload_mass_kg',6.225)*9.80665+mass*9.81
  report['vertical_force_balance_relative_error']=abs(reaction[1]/expected-1)
  assert report['vertical_force_balance_relative_error']<.001
  report['support_reaction_moment_Nmm']=reaction_moment.tolist()
  report['overturning_moment_balance_relative_error']=abs(reaction_moment[0]/meta['payload_moment_about_plate_centre_Nmm'][0]+1)
  assert report['overturning_moment_balance_relative_error']<.001
 # Get the original element ordering from the solver deck.
 einput=[];reading=False
 for line in (WORK/(name+'.inp')).read_text().splitlines():
  if line.startswith('*ELEMENT'):reading=True;continue
  if line.startswith('*'):reading=False
  if reading:einput.append(list(map(int,line.split(','))))
 lookup={n:i for i,n in enumerate(ids)}
 triangles=np.array([[lookup[n] for n in e[1:4]] for e in einput])
 face_stress=np.array([surface[e[0]] for e in einput])
 return report,(meta,xy,disp,triangles,face_stress)
if __name__=='__main__':
 names=['benchmark-h3','plate-t3-h6-s8-distributed','plate-t2-h6-s8-distributed',
  'plate-t2-h3-s8-distributed','plate-t1.5-h6-s8-distributed','plate-t2-h6-s4-top']
 reports=[];data={}
 for name in names:
  report,raw=read_case(name);reports.append(report);data[name]=raw
 coarse=reports[2];fine=reports[3]
 convergence={key:abs(coarse[key]/fine[key]-1) for key in ('max_out_of_plane_mm','max_recovered_surface_von_mises_MPa')}
 assert convergence['max_out_of_plane_mm']<.05,convergence
 assert convergence['max_recovered_surface_von_mises_MPa']<.05,convergence
 summary={'method':'Linear elastic S6 shell analysis, E 200 GPa, nu 0.3, except benchmark nu=0.',
  'solver':'CalculiX 2.23 Debian build 2.23-1; SPOOLES solver; Gmsh 4.15.2',
  'scope':'Full R1 cut profile at varied thickness; no radiator stiffening or joint/contact model.',
  'surface_stress_recovery':'Linear through-thickness extrapolation from outer Gauss layers to surfaces; no in-plane nodal extrapolation.',
  'convergence_relative_changes_h6_to_h3':convergence,'cases':reports}
 (OUT/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
 meta,xy,disp,tris,stress=data['plate-t2-h3-s8-distributed']
 tri=mtri.Triangulation(xy[:,0],xy[:,1],tris)
 fig,axes=plt.subplots(1,2,figsize=(12,6.5),layout='constrained')
 for ax in axes:
  ax.set_aspect('equal');ax.set_xlabel('Horizontal position / mm');ax.set_ylabel('Height / mm')
  ax.set_facecolor('#eef1f3')
 im=axes[0].tripcolor(tri,np.abs(disp[:,2])*1000,shading='gouraud',cmap='viridis')
 fig.colorbar(im,ax=axes[0],label='Out-of-plane displacement magnitude / micrometres')
 im=axes[1].tripcolor(tri,facecolors=stress,shading='flat',cmap='magma')
 fig.colorbar(im,ax=axes[1],label='Recovered surface von Mises stress / MPa')
 axes[0].set_title('2 mm plate / elastic deflection')
 axes[1].set_title('2 mm plate / surface stress')
 fig.suptitle('6.225 kg payload + plate weight; 75 mm eccentricity; eight secured rack fixings\n'
  'Undeformed outline shown. Idealised supports and distributed radiator loads.',fontsize=12)
 fig.savefig(OUT/'2mm-plate-analysis.png',dpi=180);plt.close(fig)
 # Retain compressed input and result evidence; meshes and full coordinate JSON
 # remain regenerable working files rather than duplicating them in git.
 for name in names:
  for ext in ('inp','dat'):
   with gzip.GzipFile(filename=str(OUT/(name+'.'+ext+'.gz')),mode='wb',mtime=0) as f:f.write((WORK/(name+'.'+ext)).read_bytes())
 print(json.dumps(summary,indent=2))
