"""Preliminary M4 retention sizing. Assumed loads/allowable, not a qualified torque rating."""
from pathlib import Path
import math,json
R=Path(__file__).resolve().parents[1]
pitch=.7;minor=4-1.082532*pitch
# Conservative screening shear cylinder: only half of axial pitch counted as material.
def area(L):return math.pi*minor*L/2
# Effective overlap excludes .55 female lead and one pitch at male screw tip.
rows=[]
for length in (8,10,12,16):
 engagement=length-2-.55-pitch
 rows.append(dict(screw_length_mm=length,effective_engagement_mm=engagement,shear_area_mm2=area(engagement),capacity_at_assumed_10MPa_N=10*area(engagement),stress_at_433N_MPa=433.333333/area(engagement)))
r=dict(status='Screening calculation; actual-grade joint testing required',method='A_s = pi * (4 - 1.082532 * 0.7) * L_e / 2; F_p = T / (K*d)',
 assumptions=dict(supported_mass_kg=5,rearward_CG_mm=100,minimum_effective_load_sharing_screws=4,top_row_screws=2,row_spacing_mm=73,local_axial_service_load_N=100,local_load_sharing_screws=2,allowable_shear_MPa=10,allowable_status='Engineering screening assumption, NOT a measured 50 C long-term material property',torque_screening_Nm=.2,nut_factor_range=[.15,.30],tip_allowance_mm=.7),
 gravity_N=5*9.80665,gravity_moment_Nmm=5*9.80665*100,
 top_screw_axial_from_gravity_N=5*9.80665*100/73/2,
 local_external_axial_per_screw_N=5*9.80665*100/73/2+100/2,
 rounded_external_axial_design_case_N=100,preload_N_range=[.2/(.30*.004),.2/(.15*.004)],
 rows=rows,selected_screw='12 x M4 x 10 ISO 7380-1 A2 stainless; no washers in reference assembly',
 full_thread_min_after_entry_mm=10,pilot_full_diameter_depth_mm=13,
 unthreaded_full_diameter_allowance_mm=13-.55-10,
 G1_4_thread_unchanged='8 mm minimum full form after 1 mm entry; actual engagement depends on the fitting male thread length',
 limits=['Uniform-load shear-cylinder approximation does not resolve first-thread loading or thread-root bending.','No long-term creep, stripping, torque or temperature rating is established.','0.2 Nm is a proposed test point, not a released assembly torque.','5 kg and 100 N service loads are screening scenarios, not rated limits.','Pressure does not load a rear cover or these dry faceplate retainers; Q has no rear cover.'])
r['selected_screw_effective_engagement_mm']=rows[1]['effective_engagement_mm']
r['selected_screw_assumed_allowable_exceeded_at_upper_preload_case']=rows[1]['stress_at_433N_MPa']>10
r['selected_screw_stress_100N_external_only_MPa']=100/rows[1]['shear_area_mm2']
out=R/'output/analysis/Q-retention.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
