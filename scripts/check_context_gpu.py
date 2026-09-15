"""Verify GPU handedness and inter-card geometry without treating AABBs as collisions."""
import json
import numpy as np


def check_gpus(scene, records):
    import bpy
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    from context_gpu5090 import D, P
    scene.view_layers[0].update()
    deps=bpy.context.evaluated_depsgraph_get()
    groups=[];trees={};hits=[];candidates=0
    for index in range(8):
        group=[];prefix=f'GPU {index+1} '
        for obj in scene.objects:
            if not obj.name.startswith(prefix) or obj.type!='MESH':continue
            if 'parallel coolant' in obj.name:continue
            verts=np.array([tuple(obj.matrix_world @ Vector(v)) for v in obj.bound_box])
            group.append((obj,verts.min(axis=0),verts.max(axis=0)))
        groups.append(group)
        record=records[index]
        assert record['main_block_X_bounds'][1] < record['pcb_X'] < record['backplate_X_bounds'][0]
        assert abs(record['port_centres'][1][2]-record['port_centres'][0][2]-34)<1e-6
        assert abs(record['backplate_X_bounds'][1]-record['main_block_X_bounds'][0]-29.68)<1e-6
        assert sum('processor PCB' in o.name for o,_,_ in group)==1
        assert sum('PCIe daughter PCB' in o.name for o,_,_ in group)==1
        assert sum('display daughter PCB' in o.name for o,_,_ in group)==1
        assert sum('DisplayPort socket' in o.name for o,_,_ in group)==3
        assert sum('HDMI socket' in o.name for o,_,_ in group)==1
        flange=scene.objects[prefix+'power housing flange']
        extent=np.ptp(np.array([tuple(v.co) for v in flange.data.vertices]),axis=0)
        assert np.allclose(extent,[7.55,20.85,1],atol=1e-5),extent
        assert sum(o.name.startswith(prefix+'power conductor ') for o in scene.objects)==12
        assert sum(o.name.startswith(prefix+'sense conductor ') for o in scene.objects)==4
        assert scene.objects.get(prefix+'power latch arm') is not None
    def tree(obj):
        if obj.name not in trees:
            eo=obj.evaluated_get(deps);me=eo.to_mesh()
            trees[obj.name]=BVHTree.FromPolygons([obj.matrix_world @ v.co for v in me.vertices],
                                                [list(f.vertices) for f in me.polygons])
            eo.to_mesh_clear()
        return trees[obj.name]
    for i,group in enumerate(groups):
        for other in groups[i+1:]:
            for a,alo,ahi in group:
                for b,blo,bhi in other:
                    if np.any(np.minimum(ahi,bhi)-np.maximum(alo,blo)<1e-5):continue
                    candidates+=1
                    if tree(a).overlap(tree(b)):hits.append([a.name,b.name])
    assert not hits,hits
    return dict(handedness='From ports: main block left, processor PCB right, active backplate further right',
                power_housing_flange_width_height_mm=[20.85,7.55],power_wires_per_card=12,sense_wires_per_card=4,
                cards=8,main_PCBs=8,PCIe_daughter_PCBs=8,display_daughter_PCBs=8,
                ports_per_card=2,port_pitch_mm=D['port_pitch_mm'],card_pitch_mm=P['card_pitch_mm'],
                cooling_body_width_mm=D['assembled_body_thickness_mm'],
                cooling_body_nominal_gap_mm=P['card_pitch_mm']-D['assembled_body_thickness_mm'],
                aggregate_width_including_offset_bracket_mm=D['assembled_overall_width_including_bracket_mm'],
                inferred_bracket_sheet_width_mm=P['bracket_width_mm'],
                bracket_plane_ahead_of_adjacent_body_end_mm=D['assembled_length_to_bracket_datum_mm']-P['bracket_sheet_mm']/2-D['main_cooler_length_height_thickness_mm'][0],
                inter_card_broad_phase_candidates=candidates,inter_card_mesh_intersections=hits,
                scope='Published cooling envelopes and port datums; detailed brackets, PCBs and connector placements are inferred reference geometry. Inter-card mesh tests exclude cables and coolant; tube/equipment is checked separately. Exact bought-in hardware fit is not qualified.')
