"""R1 thickness comparison and explicitly simplified local strip screening.

Not FEA: it does not establish complete assembly strength or deflection.
Run with standard Python. Leaves the issued R1 geometry untouched.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'cad/radiator/R1.json').read_text())
v=json.loads((ROOT/'output/radiator-R1/verification.json').read_text())
payload=p['radiator_mass_kg']+p['additional_load_kg']
force=payload*9.80665
span=max(p['radiator_mount_y_from_centre'])-min(p['radiator_mount_y_from_centre'])
moment=force*p['assumed_load_cg_behind_plate_mm']
# Four radiator corner attachments idealised as carrying the full payload.
# Moment reacted by top/bottom couples; two attachment points per end.
normal_force=moment/span/2
# Intentionally put all gravity through the upper two paths, rather than
# distributing it evenly over all twelve radiator screws.
vertical_force=force/2
length=abs(max(p['rack_mount_x'])-max(p['radiator_mount_x']))
gross_width=20.
net_width=gross_width-p['rack_slot_width']
E=p['elastic_modulus_mpa']
results=[]
for t in (3.,2.5,2.,1.5):
    mass=v['plate_mass_kg']*(t/p['thickness'])
    I_normal=net_width*t**3/12
    I_inplane=t*net_width**3/12
    sigma_normal=normal_force*length*(t/2)/I_normal
    sigma_inplane=vertical_force*length*(net_width/2)/I_inplane
    result={
        'thickness_mm':t,'plate_mass_kg':mass,'rack_mass_kg':payload+mass,
        'saving_vs_3mm_kg':v['plate_mass_kg']-mass,
        'bending_stiffness_fraction':(t/p['thickness'])**3,
        'same_load_bending_deflection_multiplier':(p['thickness']/t)**3,
        'same_profile_elastic_bending_capacity_fraction':(t/p['thickness'])**2,
        'local_strip_normal_bending_stress_MPa':sigma_normal,
        'local_strip_inplane_bending_stress_MPa':sigma_inplane,
        'local_strip_sum_of_bending_stress_magnitudes_MPa':sigma_normal+sigma_inplane,
        'local_strip_out_of_plane_deflection_mm':normal_force*length**3/(3*E*I_normal)}
    results.append(result)
assert abs(results[0]['plate_mass_kg']-v['plate_mass_kg'])<1e-12
assert abs(results[2]['plate_mass_kg']-1.1313292866597686)<1e-9
assert abs(results[-1]['same_load_bending_deflection_multiplier']-8)<1e-9
report={
 'purpose':'Thickness screening only; R1 manufacturing geometry is unchanged.',
 'material_reference':'Outokumpu Core 304/4301 cold-rolled sheet: Rp0.2 230 MPa at 20 C; actual stock certificate required.',
 'source':'https://www.outokumpu.com/-/media/files/products/core/outokumpu-core-range-datasheet.pdf',
 'assumptions':{'payload_kg':payload,'load_CG_mm':p['assumed_load_cg_behind_plate_mm'],
  'radiator_vertical_attachment_span_mm':span,'normal_force_per_upper_path_N':normal_force,
  'vertical_force_per_upper_path_N':vertical_force,'strip_length_mm':length,
  'assumed_strip_gross_width_mm':gross_width,'equivalent_net_width_mm':net_width,
  'elastic_modulus_MPa':E},
 'limitations':['Ideal fixed-end rectangular strips between rack and radiator attachment columns, not a meshed plate.',
  'The 20 mm gross strip / 13 mm equivalent net width is an analyst assumption, not a proven effective width.',
  'No hole stress concentrations, washer contact, bolt preload/prying, radiator rail flexibility or uneven slip.',
  'No global plate bowing, plate self-weight distribution, shock, vibration or external hose loads.',
  'Local strip displacement must not be reported as whole-assembly displacement; nominal stresses are not a qualified safety factor.'],
 'comparison':results}
out=ROOT/'output/radiator-R1/thickness-assessment.json'
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
