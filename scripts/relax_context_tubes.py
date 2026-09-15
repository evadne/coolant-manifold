"""Solve the front PVC branches as static elastic rods; run with .venv Python.

Coordinates/energy are mm and N mm. Only short fitting lead-outs are
prescribed; all three free-span coordinates settle under gravity. The formulation uses axial
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
from context_gpu5090 import PORT_Z, P as GPU_PLACEMENT

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
            result[f'GPU {i+1} parallel coolant {row}']=branch_route(x,tail+1,manifold+23.5+40*row,x,9,gpu+PORT_Z[row],x+(-10 if row==0 else 10))
    for row in range(2):
        result[f'Host coolant branch {row}']=branch_route(140,tail+1,manifold+23.5+40*row,136,-33,host+42+40*row,128 if row==0 else 152,depth=-270)
    return result

def rod_problem(points,params,modulus=None,nominal_length=None):
    arclength=np.r_[0,np.cumsum(np.linalg.norm(np.diff(points,axis=0),axis=1))]
    n=params['nodes'];reduction=params.get('shorten_each_front_branch_mm',0.)
    target_length=arclength[-1]-reduction if nominal_length is None else nominal_length
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
    ix=np.array([3*i+j for i in range(fixed,n-fixed) for j in (0,1,2)])
    D=np.diff(np.eye(n),n=2,axis=0);bending_hessian=np.kron(EI/h**3*(D.T@D),np.eye(3))
    def unpack(v):
        q=base.copy();q[fixed:-fixed,:]=v.reshape(-1,3);return q
    def energy_gradient(v):
        q=unpack(v);d=np.diff(q,axis=0);length=np.linalg.norm(d,axis=1);dd=np.diff(q,n=2,axis=0)
        energy=EI/(2*h**3)*(dd**2).sum()+EA/(2*h)*((length-h)**2).sum()+w*h*(q[:,2]-base[:,2]).sum()
        g=np.zeros_like(q);bd=EI/h**3*dd;g[:-2]+=bd;g[1:-1]-=2*bd;g[2:]+=bd
        sd=(EA/h*(length-h)/length)[:,None]*d;g[:-1]-=sd;g[1:]+=sd;g[:,2]+=w*h
        return energy,g[fixed:-fixed,:].ravel()
    def hessian(v):
        q=unpack(v);d=np.diff(q,axis=0);length=np.linalg.norm(d,axis=1);H=bending_hessian.copy()
        for i,(di,li) in enumerate(zip(d,length)):
            b=EA/h*((1-h/li)*np.eye(3)+h/li**3*np.outer(di,di));u=slice(3*i,3*i+3);v=slice(3*i+3,3*i+6)
            H[u,u]+=b;H[v,v]+=b;H[u,v]-=b;H[v,u]-=b
        return H[np.ix_(ix,ix)]
    initial=base[fixed:-fixed,:].ravel()
    # Finite differences independently check representative analytic derivatives.
    delta=1e-4;_,g0=energy_gradient(initial);H0=hessian(initial);errors=[]
    for k in (0,len(initial)//3,len(initial)-1):
        e=np.zeros_like(initial);e[k]=delta
        fp,gp=energy_gradient(initial+e);fm,gm=energy_gradient(initial-e)
        assert abs((fp-fm)/(2*delta)-g0[k])<1e-5
        errors.append(float(np.max(abs((gp-gm)/(2*delta)-H0[:,k]))))
    assert max(errors)<1e-5
    def report(v,iterations,residual):
        q=unpack(v)
        spline=CubicSpline(s,q,bc_type=((1,(base[1]-base[0])/h),(1,(base[-1]-base[-2])/h)))
        sampled=spline(np.linspace(0,s[-1],int(np.ceil(s[-1]*2))+1))
        metrics=route_metrics(sampled)
        record=dict(modulus_MPa=E,EI_N_mm2=EI,EA_N=EA,wet_mass_kg_per_m=wet_mass,
                    gravity_N_per_mm=w,solver_iterations=iterations,maximum_free_force_residual_N=residual,
                    maximum_strain=float(np.max(abs(np.linalg.norm(np.diff(q,axis=0),axis=1)/h-1))),
                    maximum_downward_shift_mm=float(max(base[:,2]-q[:,2])),
                    maximum_lateral_shift_from_seed_mm=float(max(abs(base[:,0]-q[:,0]))),
                    lateral_extent_relative_to_pair_origin_mm=[float(min(q[:,0])),float(max(q[:,0]))],
                    seed_route_length_mm=float(arclength[-1]),accepted_shortening_mm=reduction,nominal_length_mm=float(target_length),relaxed_length_mm=metrics['length_mm'],
                    minimum_radius_mm=metrics['minimum_sampled_radius_mm'],
                    fixed_lead_length_mm=float((fixed-1)*h),derivative_check_max_error=max(errors))
        return sampled,record
    return dict(initial=initial,energy_gradient=energy_gradient,hessian=hessian,
                unpack=unpack,report=report,indices=ix,nodes=n,fixed=fixed)


def solve(points,params,modulus=None):
    rod=rod_problem(points,params,modulus)
    res=minimize(rod['energy_gradient'],rod['initial'],jac=True,hess=rod['hessian'],method='trust-exact',
                 options={'maxiter':300,'gtol':1e-7,'initial_trust_radius':20,'max_trust_radius':100})
    residual=float(np.max(abs(res.jac)));assert residual<1e-6,(res.message,residual)
    return rod['report'](res.x,res.nit,residual)


def solve_pair(points,params,modulus=None):
    """Two fully free 3D rods with frictionless, regularised inter-tube contact.

    Former routing lanes seed the assembly's left/right passing order only;
    they exert no force and impose no coordinate constraints on free spans.
    A 1 mm numerical contact allowance covers node sampling and interpolation.
    """
    lengths=params.get('pair_nominal_lengths_mm',[None,None])
    rods=[rod_problem(p,params,modulus,length) for p,length in zip(points,lengths)]
    size=len(rods[0]['initial']);n=rods[0]['nodes'];fixed=rods[0]['fixed']
    distance=params['tube_OD_mm']+params['contact_numerical_allowance_mm']
    stiffness=params['contact_penalty_N_per_mm']
    indices=np.r_[rods[0]['indices'],3*n+rods[1]['indices']]
    def contact(v,with_hessian=False):
        a,b=[r['unpack'](x) for r,x in zip(rods,(v[:size],v[size:]))]
        d=a[:,None,:]-b[None,:,:];length=np.linalg.norm(d,axis=2)
        active=length<distance;i,j=np.nonzero(active);di=d[i,j];li=length[i,j]
        assert np.all(li>1e-9), 'Degenerate contact seed'
        gap=li-distance;energy=stiffness/2*np.sum(gap**2)
        f=(stiffness*gap/li)[:,None]*di;g=np.zeros((2,n,3))
        np.add.at(g[0],i,f);np.add.at(g[1],j,-f)
        gradient=np.r_[g[0,fixed:-fixed].ravel(),g[1,fixed:-fixed].ravel()]
        if not with_hessian:return energy,gradient
        H=np.zeros((6*n,6*n))
        for ii,jj,dd,ll in zip(i,j,di,li):
            block=stiffness*((1-distance/ll)*np.eye(3)+distance/ll**3*np.outer(dd,dd))
            u=slice(3*ii,3*ii+3);v_=slice(3*(n+jj),3*(n+jj)+3)
            H[u,u]+=block;H[v_,v_]+=block;H[u,v_]-=block;H[v_,u]-=block
        return H[np.ix_(indices,indices)]
    def fun(v):
        e0,g0=rods[0]['energy_gradient'](v[:size]);e1,g1=rods[1]['energy_gradient'](v[size:])
        ec,gc=contact(v);return e0+e1+ec,np.r_[g0,g1]+gc
    def hess(v):
        H=contact(v,True);H[:size,:size]+=rods[0]['hessian'](v[:size]);H[size:,size:]+=rods[1]['hessian'](v[size:]);return H
    initial=np.concatenate([r['initial'] for r in rods])
    # Verify contact derivatives with active contact, in X, Y and Z.
    probe=initial.copy();q0=rods[0]['unpack'](probe[:size]);q1=rods[1]['unpack'](probe[size:])
    dd=np.linalg.norm(q0[:,None]-q1[None,:],axis=2);ii,jj=np.unravel_index(np.argmin(dd),dd.shape)
    assert fixed<=ii<n-fixed and fixed<=jj<n-fixed
    delta=q1[jj]-q0[ii];probe[3*(ii-fixed):3*(ii-fixed)+3]+=delta*(1-(distance-.25)/np.linalg.norm(delta))
    _,g=contact(probe);H=contact(probe,True);errors=[]
    for k in range(3*(ii-fixed),3*(ii-fixed)+3):
        dv=np.zeros_like(probe);dv[k]=1e-5;ep,gp=contact(probe+dv);em,gm=contact(probe-dv)
        assert abs((ep-em)/2e-5-g[k])<1e-5
        errors.append(float(max(abs((gp-gm)/2e-5-H[:,k]))))
    assert max(errors)<1e-5
    res=minimize(fun,initial,jac=True,hess=hess,method='trust-exact',
                 options={'maxiter':500,'gtol':1e-7,'initial_trust_radius':10,'max_trust_radius':100})
    residual=float(np.max(abs(res.jac)));assert residual<1e-6,(res.message,residual)
    outputs=[r['report'](v,res.nit,residual) for r,v in zip(rods,(res.x[:size],res.x[size:]))]
    for _,record in outputs:
        record['contact_derivative_check_max_error']=max(errors)
        record['contact_energy_N_mm']=float(contact(res.x)[0])
    return outputs

if __name__=='__main__':
    params=json.loads((ROOT/'cad/context/pvc-routing.json').read_text());result={};records={};cache={}
    nominal=nominal_branches();names=list(nominal)
    for start in range(0,len(names),2):
        pair=names[start:start+2];points=[nominal[name] for name in pair]
        # Whole GPU pairs are translation-equivalent, including contact.
        origin=points[0][0].copy();relative=[p-origin for p in points]
        key=tuple(fingerprint(p) for p in relative)
        pair_params=dict(params,pair_nominal_lengths_mm=[params['accepted_front_branch_lengths_mm'][name] for name in pair])
        if key not in cache:cache[key]=solve_pair(relative,pair_params)
        for name,p,(q,record) in zip(pair,points,cache[key]):
            result[name]=dict(nominal_sha256=fingerprint(p),points=(q+origin).tolist())
            records[name]=record
    routes={name:dict(points=np.array(r['points']),od=13,floor=params['minimum_host_bend_radius_mm'] if name.startswith('Host ') else params['minimum_branch_bend_radius_mm']) for name,r in result.items()}
    checks=assess_routes(routes)
    print('Branch pair gap',checks['minimum_conservative_tube_gap_mm'])
    assert checks['minimum_conservative_tube_gap_mm']>0
    sensitivity={}
    first=next(iter(nominal_branches().values()))
    for E in (3,10,30):
        sensitivity_params=dict(params,pair_nominal_lengths_mm=[params['accepted_front_branch_lengths_mm'][name] for name in names[:2]])
        sensitivity[str(E)]=[r for _,r in solve_pair([nominal[name]-first[0] for name in names[:2]],sensitivity_params,E)]
    report=dict(parameters=params,branches=records,stiffness_sensitivity_MPa=sensitivity,
                branch_checks=checks,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
                for p in ('cad/context/pvc-routing.json','scripts/relax_context_tubes.py','scripts/context_tubing.py','scripts/context_gpu5090.py','cad/context/gpu-5090fe.json')})
    OUT.mkdir(exist_ok=True,parents=True)
    (OUT/'relaxed-branches.json').write_text(json.dumps(result)+'\n')
    (OUT/'pvc-equilibrium.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:{x:v[x] for x in ('maximum_downward_shift_mm','minimum_radius_mm')} for k,v in records.items()},indent=2))
