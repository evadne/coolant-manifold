# RM8-2U revision A — manufacturing notes for DFM

Units: mm. CAD source: `cad/parameters.json` and `scripts/build_cad.py`. STEP holes are pilot cylinders; no helical threads are modelled. Supply these notes with the STEP files. Automatic hole recognition is not enough to specify the threads.

## Bill of materials

| Part | Qty | Material / specification | Process |
|---|---:|---|---|
| Body | 1 | Black unfilled Delrin / POM-H; stock grade and porosity to be agreed | CNC mill, drill, tap/thread mill |
| Rear cover | 1 | 316L stainless, 3 finished thickness | Cut profile; machine sealing face, drill and countersink |
| Rack ears | 1 each hand | 304 or 316 stainless, 2.5 | Profile cut, countersink and one 90° bend |
| Gallery seals | 2 | EPDM 70 Shore A, 2 mm cross-section, coolant-compatible | Continuous moulded or factory-vulcanised loops |
| Cover screws | 31 | Stainless M4 × 12, 90° countersunk | 9 mm nominal engagement in body |
| Ear screws | 8 | Stainless M5 × 12, 90° countersunk | 9.5 mm nominal engagement in body |
| Rack fixings | 4 sets | Match rails/cage nuts, normally M6 | Purchased |
| Manifold QDs | 18 | QD3-MTG4 or verified equivalent male QD / male G1/4 | Purchased; includes IN/OUT |
| Hose QDs | 18 | Compatible QD3 female, hose connection to be selected | Purchased; 16 branch +2 trunk ends |

STEP assembly contains four manufactured solids plus two compressed seal envelopes. Blender depicts simplified bought-in fittings and screws. Rack screws, exact QD internals and hose bends are not modelled. Colour labels in Blender are intended marking locations, not machined recesses in STEP.

## Coordinates and datum convention

X: rack width, zero at centre. Y: depth, front sealing face at 0 and rear body face at 40. Z: height, bottom at 0 and top at 87. The rear cover occupies y 40…43. Ears project to y−2.5, making total bare depth 45.5.

All ports face forward: axis +Y, y=0. Both rows use x=−180, −135, −90, −45, 0, +45, +90, +135, +180. Supply z=23.5, return z=63.5. Leftmost column is IN/OUT; subsequent columns are paired branches 1…8.

## G1/4 ports — 18 places

ISO 228-1 G1/4 female parallel pipe thread, 19 TPI, 55° form; nominal major diameter 13.157. Agree finished thread gauging/acceptance with supplier. The 11.8 pilot in CAD is a starting tap-drill diameter, not a final thread-minor-diameter tolerance. Supplier selects tooling for the chosen POM grade and gauges the finished threads.

8 mm minimum full usable thread from the face. There is 16 mm nominal wall to the gallery. Provide tool run-out into the open gallery and remove breakthrough burrs. A 1.0 mm lead chamfer is modelled; review it against the actual fitting's O-ring contact band. The reference 4.5 mm male thread will not bottom out. Preserve a continuous flat Ø24 sealing land at every port. The fitting's face O-ring provides sealing; BSPP threads alone do not. No NPT or tapered BSPT substitution.

## Pocket and seal geometry

Each capsule pocket is 400 overall length × 16 overall height, R8 ends, 24 deep from the rear. Centres (x 0,z 23.5) and(x 0,z 63.5). The front wall is 16. The intervening solid web is 24 mm high; upper and lower external walls are 15.5. End walls are 20. A Ø16 end mill can generate the pocket; smaller tools can rough and finish it.

Each gland centreline is the pocket perimeter offset outward 3.5: capsule 407 overall × 23, R11.5 ends. Gland width 2.8 ±0.05, depth 1.60 ±0.05. Nominal 2 mm cord gives 20% axial squeeze and 70.1% gland fill. These are starting values at room temperature, pending seal tolerance, coolant swell, corner behaviour and cover/plastic creep review.

Centreline perimeter is approximately 840.26 mm per loop. This is a path length, not an approved cord cut length or standard O-ring ID. The seal vendor must choose the continuous-loop size and any stretch. Do not assume an adhesive butt joint is a production pressure seal. STEP shows rectangular compressed envelopes; the supplied elastomer has a round section.

Indicative DFM requirements: gland/port seal finish Ra≤1.6 µm, cover seal face Ra≤0.8 µm, mating-face flatness 0.05 across each seal perimeter. General dimensions±0.15; port positions±0.10; gland dimensions as above. These are quote requirements to confirm, not supplier guarantees. Break exposed sharp edges 0.3–0.5, except sealing edges which need a controlled small edge break. Groove root radius≤0.2 to be agreed with the seal vendor. CAD omits microscopic edge treatments.

## Cover fastening

31 screw positions: the nine port-column X positions at z 5.5,43.5,81.5, plus x±213 at each gallery-centre Z. Cover clearanceØ4.5, Ø8.4 × 90° countersink from rear. Body pilotØ3.3 × 14 deep from y 40, M4 × 0.7, minimum 10 full thread. Confirm blind tapping run-out and screw bottom clearance. All heads flush.

## Brackets

2.5 mm sheet, R2.5 internal bend, finished height 87. STEP contains formed geometry. The fabricator must derive the flat pattern using its own bend allowance/K-factor and tooling; a projection of formed STEP is not a flat pattern.

Rack width 482.6, hole spacing 465.1 across. Slots 10 wide × 7 high, centres at z 5.4 and 81.6. These align to the lowest and highest holes of the allocated 2U when the panel is centred within 88.9 mm. Slot vertical separation 76.2.

Each end has four attachment holes at y 12 and 30, z 9 and 78, axis X. Body pilotØ4.2 × 12 deep, M5 × 0.8, minimum 10 full thread. Ears haveØ5.5 clearance withØ10.4 × 90° outer countersinks. Flush side heads keep the rear assembly width 445 within a nominal 450.8 rack opening; validate the real rack geometry. Every attachment hole is outside the galleries and seals.

Direct POM threads are simple for the first prototype, but torque/preload and long-term retention must be validated. No tightening torque is established here. Review the rack ear bending strength, QD insertion forces and hose loads; support hoses independently instead of relying on the plastic ports. No operating pressure or mechanical load rating is assigned to revision A.
