"""Nominal scene checks: tube sweeps against all other visible equipment/cables.
Meshes are integration envelopes where manufacturer geometry is unavailable.
"""
import math
import numpy as np

def check_scene(scene,routes):
    import bpy
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    deps=bpy.context.evaluated_depsgraph_get();bpy.context.view_layer.update()
    equipment=[]
    for o in scene.objects:
        if o.type not in ('MESH','CURVE') or o.hide_render or o.name in routes or o.name.startswith('Fluid inside '):continue
        vv=np.array([tuple(o.matrix_world@Vector(v)) for v in o.bound_box])
        equipment.append((o,vv.min(axis=0),vv.max(axis=0)))
    trees={};hits=[];nearest=[]
    def intended(name,obj):
        if name.startswith('GPU '):
            parts=name.split();gpu=int(parts[1]);row=int(parts[-1])+1
            return (obj.startswith('Koolance ') and f'/ pair {gpu} row {row} ' in obj) or obj.startswith(f'GPU {gpu} coolant fitting')
        if name.startswith('Host coolant'):
            row=int(name[-1])+1
            return (obj.startswith('Koolance ') and f'/ pair 9 row {row} ' in obj) or obj.startswith(('Host 10-13 compression','PCI bracket G1-4 feedthrough'))
        if name.startswith('Cooling infrastructure'):
            return obj.startswith('Left infrastructure') or (name.endswith('supply') and obj.startswith('Pump outlet')) or (name.endswith('return') and obj.startswith('SuperNova bottom'))
        return obj.startswith(('SuperNova bottom','Reservoir inlet'))
    for name,r in routes.items():
        p=r['points'];radius=r['od']/2;closest=(1e9,None,None)
        for o,lo,hi in equipment:
            if intended(name,o.name):continue
            delta=np.maximum(np.maximum(lo-p,p-hi),0);indices=np.where(np.linalg.norm(delta,axis=1)<radius+15)[0]
            if not len(indices):continue
            if o.name not in trees:
                eo=o.evaluated_get(deps);me=eo.to_mesh()
                trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in me.vertices],[list(f.vertices) for f in me.polygons])
                eo.to_mesh_clear()
            tree=trees[o.name];worst=1e9;at=None
            for i in indices:
                v,n,_,dist=tree.find_nearest(Vector(p[i]))
                if dist is None:continue
                signed=-dist if (Vector(p[i])-v).dot(n)<-1e-4 else dist
                gap=signed-radius
                if gap<worst:worst=gap;at=p[i].tolist()
            if worst<closest[0]:closest=(worst,o.name,at)
            if worst<-.05:hits.append(dict(tube=name,equipment=o.name,signed_surface_gap_mm=worst,at=at))
        step=float(np.max(np.linalg.norm(np.diff(p,axis=0),axis=1)))
        nearest.append(dict(tube=name,equipment=closest[1],sampled_surface_gap_mm=closest[0],conservative_surface_gap_mm=closest[0]-step/2,at=closest[2]))
    # Original CAD source extents and part counts independently read from scene.
    def dims(o):
        v=np.array([tuple(o.matrix_world@Vector(p)) for p in o.bound_box])
        return [round(float(x),4) for x in v.max(axis=0)-v.min(axis=0)]
    counts={
        'male_fitting_solids':sum(o.name.startswith('Koolance qd3-mtg4 /') for o in scene.objects),
        'female_fitting_solids':sum(o.name.startswith('Koolance qd3-ft10x13 /') for o in scene.objects),
        'manifold_retention_screws':sum(o.name.startswith('Front M4') for o in scene.objects),
        'fan_frames':sum(o.name.startswith('NF-A20 reference fan-00') for o in scene.objects),
        'host_MCIO_cables':sum(o.name.startswith('Host uplink MCIO') for o in scene.objects),
        'radiator_rack_screws':sum(o.name.startswith('R6 populated rack screw') for o in scene.objects),
        'tubes':len(routes),'rack_square_holes':25*3*4}
    assert np.allclose(dims(bpy.data.objects['body']),[410,43,87],atol=.01)
    assert np.allclose(dims(bpy.data.objects['faceplate']),[482.6,2,87],atol=.01)
    assert np.allclose(dims(next(o for o in scene.objects if o.name.startswith('R6 rack plate'))),[482.6,2,444.5],atol=.01)
    assert list(counts.values())==[40,54,12,8,2,8,21,300],counts
    return dict(body_dimensions_xyz_mm=dims(bpy.data.objects['body']),faceplate_dimensions_xyz_mm=dims(bpy.data.objects['faceplate']),
                radiator_plate_dimensions_xyz_mm=dims(next(o for o in scene.objects if o.name.startswith('R6 rack plate'))),counts=counts,
                tube_equipment_intersections=hits,nearest_equipment=nearest,
                method='Evaluate actual equipment mesh surfaces including cable sweeps; sample identical tube centreline used in meshes and subtract tube OD/2. Signed nearest surface test on closed meshes. Intended fitting/barb insertion interfaces excluded by owner. Clearance envelope approximations do not establish first-article fit.',
                rack_front_opening_mm=450,host_lateral_clearance_mm=5,host_depth_to_rear_rail_mm=558.8-456,
                old_radiator_elbow_to_base_top_mm=142.255+1.75-18-9-140,
                new_radiator_elbow_to_base_top_mm=142.255+44.45+1.75-18-9-140,
                manifold_selected_rack_slots_z_mm=[5.4,81.6],
                viewport=dict(clip_start_mm=5,clip_end_mm=10000,orbit_centre_mm=[0,220,660],orbit_distance_mm=1800),
                scope='Nominal reference geometry, not tolerance-stack, strength, transport, thermal or ergonomic qualification.')
