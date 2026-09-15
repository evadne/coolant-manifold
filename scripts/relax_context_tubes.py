"""Solve the front PVC branches as static elastic rods; run with .venv Python.

Coordinates/energy are mm and N mm. Lateral (X) routing lanes and short fitting
lead-outs are prescribed; Y/Z settle under gravity. The formulation uses axial
strain energy EA/(2h)*(length-h)^2, discrete bending EI/(2h^3)*|D2 r|^2,
and gravitational potential w*h*z. E is an explicit illustration assumption.
"""
from pathlib import Path
import hashlib,json,sys
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import CubicSpline
from context_tubing import branch_route, route_metrics, assess_routes
from context_startech25 import RACK_U_DATUM

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/context-25U'

def fingerprint(points):
    return hashlib.sha256(np.round(points,7).astype('<f8').tobytes()).hexdigest()

def nominal_branches():
    fit=json.loads((ROOT/'output/long-bore-P/koolance-fit/verification.json').read_text())
    tail=-3-fit['inferred_seat_to_female_tail_mm']
    bottom=RACK_U_DATUM+44.45;manifold=bottom+14*44.45+.95
    host=bottom+10*44.45+.9;gpu=bottom+16*44.45+24
    result={}
    for i in range(8):
        x=-180+40*i
        for row in range(2):
            result[f'GPU {i+1} parallel coolant {row}']=branch_route(x,tail+1,manifold+23.5+40*row,x,9,gpu+89+30*row,x+(-10 if row==0 else 10))
    for row in range(2):
        result[f'Host coolant branch {row}']=branch_route(140,tail+1,manifold+23.5+40*row,136,-33,host+42+40*row,128 if row==0 else 152,depth=-270)
    return result

def solve(points,params,modulus=None):
    arclength=np.r_[0,np.cumsum(np.linalg.norm(np.diff(points,axis=0),axis=1))]
    n=params['nodes'];reduction=params.get('shorten_each_front_branch_mm',0.)
    target_length=arclength[-1]-reduction
    assert target_length>np.linalg.norm(points[-1]-points[0])
    s=np.linspace(0,target_length,n);h=s[1]
    # Compress only the initial guess towards the fitting plane, then resample
    # it by its own arc length. Uneven seed segments can create false buckles.
    t=arclength/arclength[-1];chord_y=points[0,1]*(1-t)+points[-1,1]*t
    lo,hi=0.,1.
    for _ in range(50):
        scale=(lo+hi)/2;seed=points.copy()
        seed[:,1]=chord_y+(points[:,1]-chord_y)*scale
        if np.linalg.norm(np.diff(seed,axis=0),axis=1).sum()>target_length:hi=scale
        else:lo=scale
    seed_arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(seed,axis=0),axis=1))]
    base=np.array([np.interp(s,seed_arc,seed[:,i]) for i in range(3)]).T
    for i in range(params['fixed_nodes_each_end']):
        base[i]=points[0]+np.array((0,-i*h,0))
        base[-1-i]=points[-1]+np.array((0,-i*h,0))
    E=params['young_modulus_MPa'] if modulus is None else modulus
    od=params['tube_OD_mm'];id_=params['tube_ID_mm']
    area=np.pi/4*(od**2-id_**2);inertia=np.pi/64*(od**4-id_**4)
    EA=E*area;EI=E*inertia
    wet_mass=params['dry_mass_kg_per_m']+params['coolant_density_kg_per_m3']*np.pi/4*(id_/1000)**2
    w=wet_mass*params['gravity_m_per_s2']/1000
    fixed=params['fixed_nodes_each_end']
    ix=np.array([3*i+j for i in range(fixed,n-fixed) for j in (1,2)])
    D=np.diff(np.eye(n),n=2,axis=0);bending_hessian=np.kron(EI/h**3*(D.T@D),np.eye(3))
    def unpack(v):
        q=base.copy();q[fixed:-fixed,1:]=v.reshape(-1,2);return q
    def energy_gradient(v):
        q=unpack(v);d=np.diff(q,axis=0);length=np.linalg.norm(d,axis=1);dd=np.diff(q,n=2,axis=0)
        energy=EI/(2*h**3)*(dd**2).sum()+EA/(2*h)*((length-h)**2).sum()+w*h*(q[:,2]-base[:,2]).sum()
        g=np.zeros_like(q);bd=EI/h**3*dd;g[:-2]+=bd;g[1:-1]-=2*bd;g[2:]+=bd
        sd=(EA/h*(length-h)/length)[:,None]*d;g[:-1]-=sd;g[1:]+=sd;g[:,2]+=w*h
        return energy,g[fixed:-fixed,1:].ravel()
    def hessian(v):
        q=unpack(v);d=np.diff(q,axis=0);length=np.linalg.norm(d,axis=1);H=bending_hessian.copy()
        for i,(di,li) in enumerate(zip(d,length)):
            b=EA/h*((1-h/li)*np.eye(3)+h/li**3*np.outer(di,di));u=slice(3*i,3*i+3);v=slice(3*i+3,3*i+6)
            H[u,u]+=b;H[v,v]+=b;H[u,v]-=b;H[v,u]-=b
        return H[np.ix_(ix,ix)]
    initial=base[fixed:-fixed,1:].ravel()
    # Finite differences independently check representative analytic derivatives.
    delta=1e-4;_,g0=energy_gradient(initial);H0=hessian(initial);errors=[]
    for k in (0,len(initial)//3,len(initial)-1):
        e=np.zeros_like(initial);e[k]=delta
        fp,gp=energy_gradient(initial+e);fm,gm=energy_gradient(initial-e)
        assert abs((fp-fm)/(2*delta)-g0[k])<1e-5
        errors.append(float(np.max(abs((gp-gm)/(2*delta)-H0[:,k]))))
    assert max(errors)<1e-5
    res=minimize(energy_gradient,initial,jac=True,hess=hessian,method='trust-exact',
                 options={'maxiter':300,'gtol':1e-7,'initial_trust_radius':20,'max_trust_radius':100})
    residual=float(np.max(abs(res.jac)));assert residual<1e-6,(res.message,residual)
    q=unpack(res.x)
    spline=CubicSpline(s,q,bc_type=((1,(base[1]-base[0])/h),(1,(base[-1]-base[-2])/h)))
    sampled=spline(np.linspace(0,s[-1],int(np.ceil(s[-1]*2))+1))
    metrics=route_metrics(sampled)
    report=dict(modulus_MPa=E,EI_N_mm2=EI,EA_N=EA,wet_mass_kg_per_m=wet_mass,
                gravity_N_per_mm=w,solver_iterations=res.nit,maximum_free_force_residual_N=residual,
                maximum_strain=float(np.max(abs(np.linalg.norm(np.diff(q,axis=0),axis=1)/h-1))),
                maximum_downward_shift_mm=float(max(base[:,2]-q[:,2])),
                previous_nominal_length_mm=float(arclength[-1]),shortening_mm=reduction,nominal_length_mm=float(target_length),relaxed_length_mm=metrics['length_mm'],
                minimum_radius_mm=metrics['minimum_sampled_radius_mm'],
                fixed_lead_length_mm=float((fixed-1)*h),derivative_check_max_error=max(errors))
    return sampled,report

if __name__=='__main__':
    params=json.loads((ROOT/'cad/context/pvc-routing.json').read_text());result={};records={};cache={}
    for name,p in nominal_branches().items():
        # Translation-equivalent GPU branches share a solution, avoiding numerical
        # differences between identical manufactured fitting positions.
        origin=p[0].copy();rel=p-origin;key=fingerprint(rel)
        if key not in cache:cache[key]=solve(rel,params)
        q,record=cache[key];q=q+origin
        result[name]=dict(nominal_sha256=fingerprint(p),points=q.tolist())
        records[name]=record
    routes={name:dict(points=np.array(r['points']),od=13,floor=params['minimum_host_bend_radius_mm'] if name.startswith('Host ') else params['minimum_branch_bend_radius_mm']) for name,r in result.items()}
    checks=assess_routes(routes)
    print('Branch pair gap',checks['minimum_conservative_tube_gap_mm'])
    assert checks['minimum_conservative_tube_gap_mm']>0
    sensitivity={}
    first=next(iter(nominal_branches().values()))
    for E in (3,10,30):
        _,sensitivity[str(E)]=solve(first-first[0],params,E)
    report=dict(parameters=params,branches=records,stiffness_sensitivity_MPa=sensitivity,
                branch_checks=checks,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
                for p in ('cad/context/pvc-routing.json','scripts/relax_context_tubes.py','scripts/context_tubing.py')})
    OUT.mkdir(exist_ok=True,parents=True)
    (OUT/'relaxed-branches.json').write_text(json.dumps(result)+'\n')
    (OUT/'pvc-equilibrium.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:{x:v[x] for x in ('maximum_downward_shift_mm','minimum_radius_mm')} for k,v in records.items()},indent=2))
