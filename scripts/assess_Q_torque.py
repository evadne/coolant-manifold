"""Torque/preload sensitivity, deliberately not a certified torque or creep rating."""
from pathlib import Path
import json,math
R=Path(__file__).resolve().parents[1];d1=4-1.082532*.7
nominal_Le=10-2-.55-.7
# Dimensional sensitivity only: actual screw length tolerance must be confirmed from supplier.
low_Le=10-.3-2.1-.6-.7
A=lambda L:math.pi*d1*L/2
rows=[]
for t in (.05,.08,.10,.12,.15,.20,.30,.50):
 loads=[t/(k*.004) for k in (.30,.15,.10)]
 rows.append(dict(torque_Nm=t,preload_at_K_030_015_010_N=loads,stress_with_100N_external_at_nominal_engagement_MPa=[(f+100)/A(nominal_Le) for f in loads],stress_with_100N_at_reduced_engagement_K010_MPa=(loads[-1]+100)/A(low_Le)))
out=dict(status='Screening sensitivity only; friction, material allowable and loads are unvalidated',effective_engagement_nominal_mm=nominal_Le,reduced_engagement_sensitivity_mm=low_Le,reduced_engagement_assumptions='0.30 mm shorter screw, 2.10 mm plate, 0.60 mm entry, 0.70 mm incomplete male tip; these are sensitivity inputs, not a claimed ISO screw length tolerance',shear_area_nominal_mm2=A(nominal_Le),shear_area_reduced_mm2=A(low_Le),external_axial_screw_load_assumed_N=100,assumed_long_term_shear_allowable_MPa=10,rows=rows,torque_limit_at_10MPa_and_reduced_engagement_Nm={str(k):(10*A(low_Le)-100)*k*.004 for k in (.1,.15,.3)},prototype_test_points_Nm=[.08,.10,.12,.15,.20],production_torque=None,conclusion='Around 0.10 Nm is a plausible initial coupon-test point, not an established safe torque. 0.08-0.12 Nm is a test band, not a qualified allowable interval. No generic finger-tight claim.')
(R/'output/analysis/Q-torque.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
