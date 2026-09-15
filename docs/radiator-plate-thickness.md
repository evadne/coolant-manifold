# R1 thickness assessment

The operator is willing to reduce sheet thickness if strength is retained. **2 mm 304 stainless is the proposed next prototype candidate**, keeping R1's outline, twelve radiator attachment points, cross web and rack fixings. This assessment does not replace the issued 3 mm R1 CAD/drawing or establish a qualified minimum thickness.

| Thickness | Plate mass | Saving against 3 mm | Total rack mass, including 6.225 kg payload | Relative bending stiffness |
|---|---:|---:|---:|---:|
| 3.0 mm | 1.697 kg | - | 7.922 kg | 100% |
| 2.5 mm | 1.414 kg | 0.283 kg | 7.639 kg | 57.9% |
| 2.0 mm | 1.131 kg | 0.566 kg | 7.356 kg | 29.6% |
| 1.5 mm | 0.848 kg | 0.848 kg | 7.073 kg | 12.5% |

Mass scales linearly with thickness. For the same plate profile and material in elastic bending, stiffness scales with thickness cubed and nominal bending capacity at a given stress scales with thickness squared. Thus 2 mm has 44.4% of the 3 mm nominal bending capacity, while deflection under the same transverse load would scale by 3.375. These ratios do not say how far the assembled radiator moves: the radiator, joints and rack also contribute stiffness.

## Local static screening

The load remains 6.225 kg, or 61.05 N, with the R1 screening assumption of its centre of gravity 75 mm behind the plate. That gives a 4.58 Nm moment. The outer radiator mount span is 407 mm vertically; ideal top/bottom couples put 5.625 N normal force at each upper corner load path. For the gravity component, this screening case puts all payload weight through the upper two paths, 30.523 N each, rather than assuming twelve-way sharing.

Idealise each short connection between a radiator mount column and the adjacent rack column as a fixed-ended-at-the-rack cantilever strip of length 29.05 mm. Assume 20 mm gross effective strip width and subtract the 7 mm rack slot width to use a 13 mm equivalent net rectangular section. This is a transparent hand-calculation idealisation, **not a finite-element model or a proven bound**. The small vertical offset between the upper radiator hole and rack slot, detailed hole geometry and contact are omitted.

Use E = 200,000 N/mm². For out-of-plane bending, I = b t³ /12, stress = 6 F L /(b t²), and tip displacement = 4 F L³ /(E b t³). For in-plane bending, interchange b and t. The sums below add the two nominal bending-stress magnitudes for a conservative combination within this simplified strip; they do not include hole stress concentration or establish an assembly safety factor.

| Thickness | Nominal sum of local bending stress magnitudes | Local strip out-of-plane displacement |
|---|---:|---:|
| 3.0 mm | 18.9 MPa | 0.0079 mm |
| 2.5 mm | 24.7 MPa | 0.0136 mm |
| 2.0 mm | 34.6 MPa | 0.0265 mm |
| 1.5 mm | 54.5 MPa | 0.0629 mm |

For context, [Outokumpu's Core range datasheet](https://www.outokumpu.com/-/media/files/products/core/outokumpu-core-range-datasheet.pdf) lists 230 MPa minimum 0.2% proof strength for cold-rolled 304/1.4301 sheet at 20°C, with E = 200 GPa. Actual purchased material must match its declared specification. Comparing that value with these nominal stresses suggests that static yielding of the short sheet connections is unlikely to be the controlling requirement for a 2 mm prototype. It does **not** assess bolt-hole peaks, pull-through, prying, uneven slip, thin radiator rails or handling damage.

The displacement column is only the displacement of the assumed 29.05 mm local strip. Do not present it as the deflection of the full 442.6 mm-high plate. Global bowing, radiator stiffness, washer contact, screw preload, plate self-weight distribution, shock, vibration and hose loads are not modelled.

## Design decision

Proceed towards a 2 mm prototype while retaining R1 as the 3 mm baseline. A 2.5 mm option saves only 283 g but retains more stiffness; it remains a fallback if the 2 mm assembly feels too flexible. A 1.5 mm option is not ruled out by this simple static calculation, but its eightfold transverse deflection scaling relative to 3 mm makes it a less attractive first prototype.

Before approving a thinner production drawing, assemble with the intended radiator, all twelve M3 retention fixings and proposed four rack screws per side. Apply the 6.225 kg payload at the intended centre of gravity, measure movement and check for residual deformation or joint slip after unloading. Review practical handling/hose loads separately. If changing from 3 to 2 mm, shorten or space the radiator screws to preserve the verified engagement: unchanged screws would reach 1 mm deeper. The support assessment must include the radiator's own rails and threaded features.

Calculations are reproducible using `scripts/assess_radiator_plate_thickness.py`; results are in `output/radiator-R1/thickness-assessment.json`. No STEP, DXF, drawing or render geometry changed in this assessment.

The subsequent [full-plate finite-element assessment](radiator-plate-FEA.md) supersedes the local-strip estimate as the basis for the thickness decision. It supports 2 mm for the specified static duty, with about 0.043 mm maximum plate deflection and 14 MPa recovered surface stress in the refined normal case. These are full-plate model results, distinct from the local strip values above. The 3 mm R1 manufacturing files remain preserved.
