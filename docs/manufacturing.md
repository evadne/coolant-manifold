# RM8-2U revision D — manufacturing notes for DFM

Units: mm. CAD source: `cad/parameters.json` and `scripts/build_cad.py`. STEP holes are pilot cylinders; no helical threads are modelled. Supply these notes with the STEP files. Automatic hole recognition is not enough to specify the threads.

## Bill of materials

| Part | Qty | Material / specification | Process |
|---|---:|---|---|
| Body | 1 | Black unfilled Delrin / POM-H; stock grade and porosity to be agreed | CNC mill, drill, tap/thread mill |
| Rear cover | 1 | 316L stainless, 3 finished thickness | Cut profile; machine sealing face, drill and countersink |
| Rack faceplate | 1 | 304 or 316 stainless, 3 finished thickness | Punch or laser/waterjet cut, countersink, deburr; no bends |
| Gallery seals | 2 | EPDM 70 Shore A, 2 mm cross-section, coolant-compatible | Continuous moulded or factory-vulcanised loops |
| Cover screws | 31 | Stainless M4 × 12, 90° countersunk | 9 mm nominal engagement in body |
| Faceplate/body screws | 8 | Stainless M5 × 12, 90° countersunk | 9 mm nominal engagement in body |
| Rack fixings | 4 sets | Match rails/cage nuts, normally M6 | Purchased |
| Manifold QDs | 18 | QD3-MTG4 or verified equivalent male QD / male G1/4 | Purchased; includes IN/OUT |
| Hose QDs | 18 | Compatible QD3 female, hose connection to be selected | Purchased; 16 branch +2 trunk ends |

STEP assembly contains three manufactured solids plus two compressed seal envelopes. Blender depicts simplified bought-in fittings and screws. Rack screws, exact QD internals and hose bends are not modelled. Colour labels in Blender are intended marking locations, not machined recesses in STEP.

## Coordinates and datum convention

X: rack width, zero at centre. Y: depth, front plate-supporting plane at 0 and rear body face at 40. Z: height, bottom at 0 and top at 87. The rear cover occupies y 40…43. The faceplate occupies y = −3…0. The boss ends are at y = −6, making the complete bare depth 49.

All ports face forward: axis +Y, sealing faces at y = −6. Both rows use x=−180, −135, −90, −45, 0, +45, +90, +135, +180. Supply z=23.5, return z=63.5. Leftmost column is IN/OUT; subsequent columns are paired branches 1…8.

## G1/4 ports — 18 places

ISO 228-1 G1/4 female parallel pipe thread, 19 TPI, 55° form; nominal major diameter 13.157. Agree finished thread gauging/acceptance with supplier. The 11.8 pilot in CAD is a starting tap-drill diameter, not a final thread-minor-diameter tolerance. Supplier selects tooling for the chosen POM grade and gauges the finished threads.

8 mm minimum full usable thread from each raised boss end. There is 22 mm nominal distance from that end to the gallery: 6 mm boss plus the 16 mm base front wall. Provide tool run-out into the open gallery and remove breakthrough burrs. A 1.0 mm lead chamfer is modelled; review it against the actual fitting's O-ring contact band. The reference 4.5 mm male thread will not bottom out. Preserve the continuous flat annulus on each Ø28 boss end around the thread mouth. The seal face must accommodate the actual fitting O-ring contact band. Break its outside rim at most 0.2 mm; do not encroach on that contact band. The fitting's face O-ring provides sealing; BSPP threads alone do not. No NPT or tapered BSPT substitution.

## Pocket and seal geometry

Each capsule pocket is 400 overall length × 16 overall height, R8 ends, 24 deep from the rear. Centres (x 0,z 23.5) and(x 0,z 63.5). The front wall is 16. The intervening solid web is 24 mm high; upper and lower external walls are 15.5. End walls are 20. A Ø16 end mill can generate the pocket; smaller tools can rough and finish it.

Each gland centreline is the pocket perimeter offset outward 3.5: capsule 407 overall × 23, R11.5 ends. Gland width 2.8 ±0.05, depth 1.60 ±0.05. Nominal 2 mm cord gives 20% axial squeeze and 70.1% gland fill. These are starting values at room temperature, pending seal tolerance, coolant swell, corner behaviour and cover/plastic creep review.

Centreline perimeter is approximately 840.26 mm per loop. This is a path length, not an approved cord cut length or standard O-ring ID. The seal vendor must choose the continuous-loop size and any stretch. Do not assume an adhesive butt joint is a production pressure seal. STEP shows rectangular compressed envelopes; the supplied elastomer has a round section.

Indicative DFM requirements: gland/port seal finish Ra≤1.6 µm, cover seal face Ra≤0.8 µm, mating-face flatness 0.05 across each seal perimeter. General dimensions±0.15; port positions±0.10; gland dimensions as above. These are quote requirements to confirm, not supplier guarantees. Break exposed sharp edges 0.3–0.5, except sealing edges which need a controlled small edge break. Groove root radius≤0.2 to be agreed with the seal vendor. CAD omits microscopic edge treatments.

## Cover fastening

31 screw positions: the nine port-column X positions at z 5.5,43.5,81.5, plus x±213 at each gallery-centre Z. Cover clearanceØ4.5, Ø8.4 × 90° countersink from rear. Body pilotØ3.3 × 14 deep from y 40, M4 × 0.7, minimum 10 full thread. Confirm blind tapping run-out and screw bottom clearance. All heads flush.

## Flat rack faceplate

One 482.6 × 87 × 3 mm stainless plate; no bends or formed features. Eighteen Ø32 (+0.2/0) through windows centred on the ports. Window centre positions ±0.10 relative to the mounting pattern. Request a deburred, flattened sheet and agree flatness with the supplier. Punching can distort ligaments, so laser/waterjet cutting is also acceptable.

Each POM boss is Ø28 ±0.05, 6.00 ±0.05 high from the faceplate-supporting POM plane, with an R1 root fillet. Plate finished thickness 3.00 ±0.10 gives a nominal 3 mm axial stand-off, a dimensional minimum of 2.85 mm before plate flatness, assembly gap and other effects. The maximum root-fillet envelope is nominal Ø30, leaving 1 mm radial clearance in the Ø32 window. Check registration and the actual plate against the bosses before assembly.

The threaded boss end, not the stainless plate, is the seal datum. Bore/tap G1/4 from y = −6; the base front wall and gallery position are unchanged. The nominal wall around the thread at the boss is (28 − 13.157)/2 = 7.42 mm before thread/chamfer tolerances. Bosses are integral, milled from thicker POM stock by pocketing the surrounding face; they are not glued, pressed-in or separately threaded parts.

The fitting's O-ring must contact a complete flat POM annulus around the thread. A 3 mm stand-off prevents the faceplate from obstructing an ordinary flat fitting shoulder; it does not guarantee sealing independently of O-ring size/compression, thread length, contact finish or fitting geometry. Fitting bodies may overhang the boss, but an oversized O-ring cannot overhang its sealing face. No gasket is needed between the dry faceplate and the body. Finish seal lands to the specified roughness and inspect for burrs/damage.

Eight body mounting positions (X,Z): (−208,9), (−208,43.5), (−208,78), (+208,9), (+208,43.5), (+208,78), (−67.5,43.5), (+67.5,43.5). Faceplate holes Ø5.5 with Ø10.4 × 90° countersink from the front (y = −3). Body pilot Ø4.2 × 14 deep from the front, M5 × 0.8, minimum 10 mm full thread. With M5 × 12 countersunk screws, nominal POM engagement is 9 mm. Finish heads flush and confirm blind-hole bottom clearance. These mounts are separate from the pressure-cover screws and do not intersect galleries, seal grooves or rear screw bores.

Rack slots are 10 × 7, centres X = ±232.55, Z = 5.4 and 81.6: 465.1 horizontal and 76.2 vertical separation. Body width behind the rail plane is 440 mm. Verify fit and cage-nut access on the actual rack.

`output/cad/faceplate-flat.dxf` is a genuine flat profile in millimetres: DXF X/Y correspond to assembly X/Z, with origin at the faceplate's bottom centre. CUT contains the outline, eighteen Ø32 windows, eight Ø5.5 mounting holes and four rack slots. It deliberately omits countersink outlines to prevent them being cut through. Countersink the eight body mounts as a separate operation. Do not countersink the rack slots or port windows. The STEP includes the countersinks.

The front plate is the rack mount; the raised POM bosses provide the independent port sealing surfaces. The retained rear cover closes the wet galleries. A separate flat bottom support plate fixed to the body is allowed by the user but is not included in revision D; its fasteners would need their own clearance and load checks.

Direct POM threads are simple for the first prototype, but torque/preload and long-term retention must be validated. No tightening torque is established here. Review faceplate bending/deflection, QD insertion forces and hose loads; support hoses independently instead of relying on the plastic ports. No operating pressure or mechanical load rating is assigned to revision D.
