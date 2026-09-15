# Radiator fan plates R3 and R4

Two separate prototype alternatives add four Noctua NF-A20 fans to the custom rack plate. R3 has tapped M4 holes; R4 has plain holes with separate nuts. **R4 is the recommended prototype**, with button screw heads on the radiator side and nuts on the outer fan faces. This recommendation is not an operator selection or a load rating. Manifold revision P and radiator revisions R1/R2 are preserved.

## Shared geometry

- 304 / EN 1.4301 stainless steel, 482.60 × 444.50 × 2.00 mm; nominal 10U.
- Forty optional rack slots, unchanged from R2: 10 × 7, X ±232.55, Y = 44.45n + 6.35/38.10 for n = 0…9. Four positions per U, two on each side. Available positions do not imply forty installed screws.
- Twelve Ø3.6 radiator holes remain at X ±203.5 and Y 18.75/143.75/159.75/284.75/300.75/425.75. These are clearance holes; their mating M3 threads remain in the radiator frame.
- Four 188 × 188 apertures now have **R50 corners**. This retains steel under the fan mounting pads and Ø9 washers. Every aperture still contains an unobstructed Ø188 circle. The change removes about 5.9% of the old R8 aperture area, but does not establish an airflow or acoustic performance change.
- Fan centres X ±100, Y 122.25/322.25: the original 200 × 200 grid, with 12 mm central webs.
- Sixteen fan mount centres are the Cartesian product of X −185/−15/+15/+185 and Y 37.25/207.25/237.25/407.25. Each fan uses its **170 × 170 mm pattern**.
- R3 holes: M4 × 0.7–6H through. Ø3.3 nominal tap-pilot cylinders are used in STEP/DXF; the drawing supplies the thread specification.
- R4 holes: Ø4.50 +0.15/0 through. No tapped holes and no countersinks in this plate.
- Fan-hole edge breaks C0.1 maximum. Other external cut edges deburred 0.2–0.3. Hole centres ±0.10, other profile dimensions ±0.15; 0.5 mm free-state flatness target requires vendor agreement.

The plate weighs approximately **1.249 kg for R3** and **1.248 kg for R4**, versus 1.120 kg for R2. The extra steel at the aperture corners accounts for this increase. These are net CAD masses at 7,900 kg/m³, not shipping weights.

## Fan and radiator fasteners

| Feature | R3, tapped plate | R4, plain bores + nuts |
|---|---|---|
| Fan screws | 16 × M4 × 35 ISO 7380-1 | 16 × M4 × 40 ISO 7380-1 |
| Material | A2 stainless reference | A2 stainless reference |
| Flat washers | 16 × M4, Ø9 / Ø4.3 / 0.8 | 32 × M4, Ø9 / Ø4.3 / 0.8 |
| Nuts | None | 16 × DIN 934 M4, AF7, height 3.2 |
| Orientation | Heads outside fans | Heads behind plate; nuts outside fans |
| Maintenance | Short plate threads can be damaged | Replaceable nuts; hold both ends when assembling |

Nominal thread length in the R3 sheet after two C0.1 edge breaks is 1.8 mm, or 2.57 pitches. At the specified minimum sheet thickness, this becomes 1.7 mm, or 2.43 pitches. The actual usable engagement also depends on tapping and screw lead geometry. The four fan screws carry only one 370 g fan, but that does not qualify a tightening torque or resistance to repeated assembly. The global plate analysis does not assess thread stripping.

For R4, assemble each fan to the plate before attaching the plate to the radiator. Hold the rear hex socket while tightening its outer nut. Select a tested anti-loosening approach before release; the DIN 934 reference is a plain nut, not a self-locking nut. Do not silently substitute a taller locknut without checking screw length.

Radiator attachment screws require **compact M3 heads, maximum Ø5.6 × 2.4 high, without washers**. Their length must be selected from the actual tapped-frame engagement and blind-depth allowance; this revision does not guess a safe M3 screw length. Fit the custom plate with its fans attached, then install these accessible edge screws. The CAD reference shows a minimum 0.772 mm nominal gap between these M3 head envelopes and the fans. Larger washers from earlier illustrative scenes are unsuitable here.

The right-hand front fans are rotated 180° about their airflow axes relative to the left-hand fans, keeping the asymmetric cable exits inward. This is an in-plane rotation, not a reversal of airflow. Fan frames meet nominally at 200 mm centres. The Noctua drawing gives tolerances on outer dimensions and hole patterns; nominal CAD fit alone is not a worst-case tolerance guarantee. Verify the four actual fans on a first article before manufacture in quantity.

## Nuts fit, but screw orientation improves core protection

The Alphacool catalogue mesh places the front plate seating plane at Y −22.5 and the core face at Y −16, giving a nominal **6.5 mm cavity**. Ray sampling checks the centres and Ø9 washer envelopes at all sixteen fan fixings (272 samples). This is reference-model evidence, not a toleranced drawing of the production radiator.

A DIN 934 M4 nut plus a 0.8 mm washer would occupy **4.0 mm**, leaving **2.5 mm** nominally. The user's suggested rear-nut arrangement therefore fits the reference geometry. With a 32 mm padded fan and M4 × 40 screw, however, the tip would project 5.2 mm behind the plate, leaving only 1.3 mm to the core. Fan-pad compression could consume that gap; it is not a universally safe screw length in that orientation.

R4 instead puts the **2.2 mm button head and 0.8 mm washer behind the plate**, occupying 3.0 mm and leaving **3.5 mm nominally**. The screw points outwards. Its nominal 1.2 mm projection beyond the outer nut can grow with pad compression without moving towards the core. Actual head height, washers, radiator position and loaded deflection still need a physical clearance check. Rear clearance is why button heads are specified here; arbitrary taller heads are not interchangeable without checking them.

## Rack-front and rack-rear use

The custom plate is the structural rack interface and the fan mount. The radiator retains its original opposite fan plate. The supplied assembly views show front fans pushing into the radiator and rear fans pulling in the same airflow direction. Four-fan-only operation uses the relevant bank; eight fans give push/pull. The same assembly can attach to front or rear rack rails. Orient the fan airflow for the desired rack ventilation direction; moving the plate between rail faces does not by itself reverse airflow.

The rear stock fan plate and radiator are illustrated envelopes, informed by the manufacturer's dimensions. The custom plate comes directly from its STEP mesh. Noctua fan parts come from the official public reference CAD; the manufacturer deliberately alters some impeller/internal details, so these parts must not be used for airflow simulation or fan manufacture. No product surface text or markings have been added.

## Verification and structural analysis

The build checks valid single solids, STEP round-trip volume/extents, exact analytical cut area, DXF entities/layers, all twelve M3 reference locations, forty rack slot locations, full Ø188 airflow circles and complete Ø9 washer bearing lands. `output/radiator-fan-integration/verification.json` records reference hashes and hardware/cavity checks.

The R4 shell analysis uses the larger Ø4.5 fan holes and revised R50 geometry, with 15 kg total payload plus plate self-weight. Four front fans (1.48 kg) act directly at their sixteen M4 holes with a centre of gravity 18 mm in front of the plate. The remaining 13.52 kg enters through the twelve M3 radiator attachments. Its eccentric moment is adjusted so the complete payload retains the same conservative 150 mm effective rearward centre of gravity as the earlier study. The radiator/pump/reservoir/filled-system weight budget remains covered by that envelope; the new front fans are not counted twice.

See `output/radiator-R4/analysis/assessment.json` for the regenerated 6 mm / 3 mm mesh comparison and eight/forty secured rack-fixing cases. The analysis is linear elastic plate screening: it does not qualify the screws, M3 frame pull-out, fan pads, vibration, transport shocks, cage nuts, rails, contact stiffness or a complete assembly load rating. R3 is not independently thread-strength qualified by the R4 plate study.

| Secured rack fixings | Peak out-of-plane movement | Peak recovered surface stress |
|---|---:|---:|
| 40 | 0.1020 mm | 34.77 MPa |
| 8 | 0.2165 mm | 76.73 MPa |

The 6 to 3 mm refinement changed peak movement by 0.16% and peak recovered stress by 0.98%. The 3 mm mesh has 82,196 S6 elements. Force and moment balance checks pass. Under these stated loads and supports, 2 mm remains a reasonable prototype thickness. These results do not prescribe how many screws an operator must install.

## Files and reproduction

- `cad/radiator/R3.json`, `R4.json`: separate parameters.
- `output/radiator-R3/`, `output/radiator-R4/`: STEP, DXF, STL, checks, Blender scenes and five review angles per alternative.
- `output/pdf/radiator-fan-plates-R3-R4.pdf`: three sheets covering both cut profiles, holes, threads and the recommended screw stack.
- `output/radiator-fan-integration/`: common integration evidence and Noctua reference meshes. These meshes are assembly references, not supplier fabrication parts.

Run `build_radiator_plate.py --revision R3|R4`, then `prepare_radiator_fan_mounts.py`, `draw_radiator_fan_plates.py`, and Blender `render_radiator_plate.py -- --revision R3|R4`. Shell cases are generated with `radiator_plate_fea.py --revision R4 --payload-kg 15 --cg-mm 150`, solved using CalculiX 2.23, and reduced using `review_radiator_R4.py`. Native input/output files are preserved compressed with the analysis.

## Primary references

- [Noctua NF-A20 PWM specifications](https://www.noctua.at/en/products/nf-a20-pwm/specifications): padded 200 × 200 × 32 mm envelope, fan mass and mounting pattern.
- [Noctua downloads](https://www.noctua.at/en/products/nf-a20-pwm/downloads): public CAD and dimensioned PDF, retained with its README under `docs/references/noctua-nf-a20/`.
- [Noctua CAD terms](https://www.noctua.at/en/3d-cad-models): integration/rendering use; altered internal geometry; no performance simulation or reproduction of fans.
- [Westfield DIN 934 nut specification](https://www.westfieldfasteners.co.uk/Standards/Nut-Hex-M.pdf): standard M4 nut dimensions.
- [Alphacool 14351 datasheet](https://download.alphacool.com/datasheet/ENG_14351_Alphacool_NexXxoS_XT45_Full_Copper_1260mm_SuperNova_Radiator_datasheet.pdf) and [reference mesh](https://3dcenter.alphacool.com/stl/14351_0.stl): radiator envelope, weight and frame geometry.

No order or supplier submission has been made.
