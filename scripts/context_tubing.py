"""Deterministic PVC centre-lines and annular meshes in mm.
Tangent circular bends and smooth lateral transitions replace AUTO-handle splines.
This is a geometric routing study, not a flexible-body or kink simulation.
"""
import math
import numpy as np

class Route:
    def __init__(self, start):
        self.points=[np.array(start,dtype=float)]
    def line(self,end):
        a=self.points[-1];b=np.array(end,dtype=float)
        n=max(1,math.ceil(np.linalg.norm(b-a)))
        self.points.extend(a+(b-a)*t/n for t in range(1,n+1));return self
    def shift(self,end):
        """Quintic lateral transition, linear principal travel; straight end tangents."""
        a=self.points[-1];b=np.array(end,dtype=float);d=b-a;k=np.argmax(abs(d))
        n=max(2,math.ceil(np.linalg.norm(d)*1.2))
        for t in np.linspace(0,1,n+1)[1:]:
            s=6*t**5-15*t**4+10*t**3;p=a+d*s;p[k]=a[k]+d[k]*t;self.points.append(p)
        return self
    def bend(self,incoming,outgoing,r):
        """90 degree centre-line arc. incoming/outgoing are orthogonal unit vectors."""
        a=self.points[-1];u=np.array(incoming,float);v=np.array(outgoing,float)
        assert abs(np.dot(u,v))<1e-8 and abs(np.linalg.norm(u)-1)<1e-8
        for t in np.linspace(0,math.pi/2,math.ceil(math.pi*r/2)+1)[1:]:
            self.points.append(a+r*math.sin(t)*u+r*(1-math.cos(t))*v)
        return self
    def array(self):return np.array(self.points)

def branch_route(x,source_y,source_z,end_x,end_y,end_z,lane,depth=-250,radius=55):
    """Separate lateral lanes allow two rows to pass without crossing."""
    direction=1 if end_z>source_z else -1
    p=Route((x,source_y,source_z))
    p.line((x,source_y-30,source_z)).shift((lane,source_y-110,source_z))
    p.line((lane,depth+radius,source_z)).bend((0,-1,0),(0,0,direction),radius)
    p.line((lane,depth,end_z-direction*radius)).bend((0,0,direction),(0,1,0),radius)
    p.line((lane,-130,end_z)).shift((end_x,-50,end_z)).line((end_x,end_y,end_z))
    return p.array()

def route_metrics(points):
    p=np.asarray(points);d=np.diff(p,axis=0);lengths=np.linalg.norm(d,axis=1)
    assert min(lengths)>1e-6,'Duplicate route points'
    dots=np.sum(d[:-1]*d[1:],axis=1)/(lengths[:-1]*lengths[1:])
    assert min(dots)>.99,('Tangent discontinuity or backtracking',float(min(dots)))
    a=d[:-1];b=d[1:];cross=np.linalg.norm(np.cross(a,b),axis=1)
    denom=2*cross;valid=denom>1e-7
    radii=(lengths[:-1]*lengths[1:]*np.linalg.norm(a+b,axis=1))[valid]/denom[valid]
    return dict(length_mm=float(sum(lengths)),minimum_sampled_radius_mm=float(min(radii)) if len(radii) else None,
                max_sample_step_mm=float(max(lengths)),start=list(p[0]),end=list(p[-1]))

def make_tube(scene,name,points,wall_material,fluid_material,od=13,id=10):
    import bpy
    p=np.array(points);t=np.gradient(p,axis=0);t/=np.linalg.norm(t,axis=1)[:,None]
    # Parallel-transport frame avoids arbitrary roll flips along 3D routes.
    normal=np.cross(t[0],(1,0,0))
    if np.linalg.norm(normal)<.1:normal=np.cross(t[0],(0,0,1))
    normal/=np.linalg.norm(normal);frames=[]
    for tangent in t:
        normal=normal-tangent*np.dot(normal,tangent);normal/=np.linalg.norm(normal)
        frames.append((normal.copy(),np.cross(tangent,normal)))
    frames=np.array(frames);sides=20;ang=np.linspace(0,2*math.pi,sides,endpoint=False)
    direction=frames[:,0,None,:]*np.cos(ang)[None,:,None]+frames[:,1,None,:]*np.sin(ang)[None,:,None]
    def mesh(name,radii,material):
        vv=np.concatenate([(p[:,None,:]+r*direction).reshape(-1,3) for r in radii]);ff=[];rings=len(p);offset=rings*sides
        for layer in range(len(radii)):
            off=layer*offset
            for i in range(rings-1):
                for j in range(sides):
                    q=(off+i*sides+j,off+i*sides+(j+1)%sides,off+(i+1)*sides+(j+1)%sides,off+(i+1)*sides+j)
                    ff.append(q if layer==0 else q[::-1])
        if len(radii)==2:
            for j in range(sides):
                k=(j+1)%sides;ff.extend([(j,offset+j,offset+k,k),((rings-1)*sides+k,offset+(rings-1)*sides+k,offset+(rings-1)*sides+j,(rings-1)*sides+j)])
        else:
            ff.extend([tuple(reversed(range(sides))),tuple((rings-1)*sides+j for j in range(sides))])
        m=bpy.data.meshes.new(name);m.from_pydata(vv.tolist(),[],ff);m.update()
        o=bpy.data.objects.new(name,m);scene.collection.objects.link(o);m.materials.append(material)
        for f in m.polygons:f.use_smooth=True
        return o
    o=mesh(name,[od/2,id/2],wall_material);o['tube_ID_mm']=id;o['tube_OD_mm']=od
    mesh('Fluid inside '+name,[id/2-.03],fluid_material)
    return o

def assess_routes(routes):
    """1mm-point sampling with a conservative step allowance on pair separation."""
    result={};mins=[]
    for name,r in routes.items():
        m=route_metrics(r['points']);m.update(od_mm=r['od'],id_mm=10,design_radius_floor_mm=r['floor'])
        assert m['minimum_sampled_radius_mm']>=r['floor']-.05,(name,m)
        # Explicit fitting-axis alignment, independent of adjacent-point smoothness.
        desired_start=(0,1,0) if name.startswith(('Cooling infrastructure','Radiator')) else (0,-1,0)
        desired_end=(1,0,0) if name=='Cooling infrastructure supply' else ((0,-1,0) if name=='Cooling infrastructure return' else ((-1,0,0) if name=='Radiator to reservoir' else (0,1,0)))
        points=r['points'];t0=points[1]-points[0];t1=points[-1]-points[-2]
        assert np.dot(t0/np.linalg.norm(t0),desired_start)>.9999,name
        assert np.dot(t1/np.linalg.norm(t1),desired_end)>.9999,name
        arclength=np.r_[0,np.cumsum(np.linalg.norm(np.diff(points,axis=0),axis=1))]
        closest=float('inf')
        for k in range(0,len(points),100):
            ds=np.sum((points[k:k+100,None,:]-points[None,:,:])**2,axis=2)
            ds[abs(arclength[k:k+100,None]-arclength[None,:])<3*r['od']]=np.inf
            closest=min(closest,float(np.sqrt(np.min(ds))))
        m['nonlocal_self_surface_gap_mm']=closest-r['od']-m['max_sample_step_mm']
        assert m['nonlocal_self_surface_gap_mm']>0,(name,'Self overlap')
        m['fitting_axes_aligned']=True
        result[name]=m
    names=list(routes)
    for i,name in enumerate(names):
        a=routes[name];p=a['points'];ra=a['od']/2
        for other in names[i+1:]:
            b=routes[other];q=b['points'];best=float('inf')
            for k in range(0,len(p),100):
                best=min(best,float(np.sqrt(np.min(np.sum((p[k:k+100,None,:]-q[None,:,:])**2,axis=2)))))
            uncertainty=(result[name]['max_sample_step_mm']+result[other]['max_sample_step_mm'])/2
            mins.append(dict(a=name,b=other,sampled_surface_gap_mm=best-ra-b['od']/2,
                             conservative_surface_gap_mm=best-ra-b['od']/2-uncertainty))
    mins.sort(key=lambda x:x['conservative_surface_gap_mm'])
    return dict(routes=result,closest_pairs=mins[:20],minimum_conservative_tube_gap_mm=mins[0]['conservative_surface_gap_mm'],
                method='Centrelines sampled at <=1mm (quintic transition <=~1mm); subtract both outer radii and half the sum of maximum steps. Curvature from three-point circumcircles. No load, ovalisation or temperature simulation.')
