"""Generate reproducible CalculiX S6 shell studies from the R1 CAD face.

Optional dependencies: gmsh==4.15.2 and existing CadQuery/numpy.
Solver: CalculiX 2.23. Units N, mm, s, tonne. No changes to issued CAD.
"""
from pathlib import Path
import argparse,json,math
import numpy as np
import cadquery as cq
import gmsh
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'cad/radiator/R1.json').read_text())
OUT=ROOT/'tmp/radiator-fea';OUT.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--size',type=float,default=6)
parser.add_argument('--thickness',type=float,default=2)
parser.add_argument('--supports',type=int,choices=[4,8],default=8)
parser.add_argument('--load',choices=['distributed','corners','top'],default='distributed')
parser.add_argument('--benchmark',action='store_true')
a=parser.parse_args();H=P['height'];t=a.thickness
name=f'plate-t{t:g}-h{a.size:g}-s{a.supports}-{a.load}' if not a.benchmark else f'benchmark-h{a.size:g}'
gmsh.initialize();gmsh.option.setNumber('General.Terminal',0)
if a.benchmark:
 gmsh.model.occ.addRectangle(0,0,0,100,20)
else:
 body=cq.importers.importStep(str(ROOT/'output/radiator-R1/rack-plate-R1.step')).val()
 face=max([f for f in body.Faces() if abs(f.Center().z)<1e-6],key=lambda f:f.Area())
 assert abs(face.Area()-body.Volume()/P['thickness'])<1e-4
 cq.exporters.export(face,str(OUT/'plate-midsurface.step'))
 gmsh.model.occ.importShapes(str(OUT/'plate-midsurface.step'))
gmsh.model.occ.synchronize()
gmsh.option.setNumber('Mesh.MeshSizeMax',a.size)
gmsh.option.setNumber('Mesh.MeshSizeMin',min(.8,a.size/4))
gmsh.option.setNumber('Mesh.MeshSizeFromCurvature',24)
gmsh.option.setNumber('Mesh.Algorithm',6)
gmsh.model.mesh.generate(2);gmsh.model.mesh.setOrder(2)
ids,coords,_=gmsh.model.mesh.getNodes();coords=coords.reshape(-1,3)
types,els,conns=gmsh.model.mesh.getElements(2)
assert list(types)==[9],types
elements=np.array(els[0]);connectivity=np.array(conns[0]).reshape(-1,6)
gmsh.write(str(OUT/(name+'.msh')))
gmsh.finalize()
xyz={int(n):v for n,v in zip(ids,coords)}
loads={};supports=set();mounts=[]
def add(n,d,f):loads[(int(n),d)]=loads.get((int(n),d),0)+float(f)
if a.benchmark:
 supports=set(map(int,ids[abs(coords[:,0])<1e-7]))
 tip=ids[abs(coords[:,0]-100)<1e-7]
 for n in tip:add(n,3,10/len(tip))
 t=2.
else:
 indices=[0,5] if a.supports==4 else [0,2,3,5]
 for x in P['rack_mount_x']:
  for j in indices:
   y=P['rack_mount_y'][j]
   # Distance to central straight segment of each horizontal slot.
   rr=np.sqrt(np.maximum(abs(coords[:,0]-x)-1.5,0)**2+(coords[:,1]-y)**2)
   ns=ids[abs(rr-3.5)<1e-5];assert len(ns)>10
   supports.update(map(int,ns))
 for x in P['radiator_mount_x']:
  for dy in P['radiator_mount_y_from_centre']:
   rr=np.sqrt((coords[:,0]-x)**2+(coords[:,1]-H/2-dy)**2)
   ns=ids[abs(rr-1.8)<1e-5];assert len(ns)>10
   mounts.append((x,dy,ns))
 force=(P['radiator_mass_kg']+P['additional_load_kg'])*9.80665
 moment=force*75
 active=mounts if a.load=='distributed' else [m for m in mounts if abs(m[1])==203.5]
 denominator=sum(m[1]**2 for m in active)
 for x,dy,ns in active:
  fy=-force/len(active) if a.load!='top' else (-force/2 if dy>0 else 0)
  fz=moment*dy/denominator
  for n in ns:add(n,2,fy/len(ns));add(n,3,fz/len(ns))
resultant=np.zeros(3);mom=np.zeros(3)
for (n,d),f in loads.items():
 vec=np.zeros(3);vec[d-1]=f;resultant+=vec;mom+=np.cross(xyz[n]-[0,H/2,0],vec)
if not a.benchmark:
 assert abs(resultant[1]+force)<1e-8 and abs(mom[0]-moment)<1e-5
def node_set(name,values):
 values=sorted(map(int,values));r=[f'*NSET,NSET={name}']
 r+= [','.join(map(str,values[i:i+16])) for i in range(0,len(values),16)]
 return r
lines=['*HEADING',name+'; elastic shell study, not an assembly load rating','*NODE']
lines +=[f'{n},{x:.10g},{y:.10g},{z:.10g}' for n,(x,y,z) in zip(ids,coords)]
lines+=['*ELEMENT,TYPE=S6,ELSET=PLATE']
lines +=[','.join(map(str,[n,*conn])) for n,conn in zip(elements,connectivity)]
lines+=node_set('ALL',ids)+node_set('SUPPORT',supports)
lines+=['*MATERIAL,NAME=STEEL','*ELASTIC','200000.,0.' if a.benchmark else '200000.,0.3','*DENSITY','7.9E-9',
 '*SHELL SECTION,ELSET=PLATE,MATERIAL=STEEL',str(t),'*BOUNDARY',
 'SUPPORT,1,6' if a.benchmark else 'SUPPORT,1,3',
 '*STEP','*STATIC','*CLOAD']
lines +=[f'{n},{d},{f:.12g}' for (n,d),f in sorted(loads.items()) if abs(f)>1e-12]
if not a.benchmark:lines+=['*DLOAD','PLATE,GRAV,9810.,0.,-1.,0.']
lines+=['*NODE PRINT,NSET=ALL','U','*NODE PRINT,NSET=SUPPORT,TOTALS=YES','RF',
 '*EL PRINT,ELSET=PLATE','S','*NODE FILE,OUTPUT=2D','U','*END STEP']
(OUT/(name+'.inp')).write_text('\n'.join(lines)+'\n')
metadata={'name':name,'thickness_mm':t,'mesh_size_mm':a.size,'nodes':len(ids),'elements':len(elements),
 'solver':'CalculiX 2.23','element':'S6','gmsh':'4.15.2','poisson_ratio':0. if a.benchmark else .3,'payload_resultant_N':resultant.tolist(),
 'payload_moment_about_plate_centre_Nmm':mom.tolist(),'supports':a.supports if not a.benchmark else 'fixed edge',
 'load':a.load,'self_weight':not a.benchmark,
 'node_ids':list(map(int,ids)),'coordinates':coords.tolist(),'elements_connectivity':connectivity.astype(int).tolist(),
 'support_nodes':sorted(supports),
 'benchmark_expected_tip_mm':10*100**3/(3*200000*(20*2**3/12)) if a.benchmark else None}
(OUT/(name+'.json')).write_text(json.dumps(metadata)+'\n')
print(name,len(ids),'nodes;',len(elements),'S6 elements')
