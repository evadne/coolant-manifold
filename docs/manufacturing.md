# RM8-2U revision G — manufacturing notes for DFM

Units: mm. CAD source: `cad/parameters.json` and `scripts/build_cad.py`. STEP holes are pilot cylinders; no helical threads are modelled. Supply these notes with the STEP files. Automatic hole recognition is not enough to specify the threads.

Selected arrangement: **Option B**. The front plate mounts the POM to the rack; the rear plate only closes and seals the channels. All 39 plate-to-POM screws are M4 × 0.7; no M3 or M5 is used in these joints. The historical Option C files are outside this scope. See [front and rear plate drafts](steel-plates.md).

## Bill of materials

| Part | Qty | Material / specification | Process |
|---|---:|---|---|
| Body | 1 | Black unfilled Delrin / POM-H; stock grade and porosity to be agreed | CNC mill, drill, tap/thread mill |
| Rear cover | 1 | 316L / EN 1.4404 stainless, 3 finished thickness | Punch or laser-cut profile and through holes; finish holes, machine sealing face and countersinks |
| Rack faceplate | 1 | 304 or 316 stainless, 3 finished thickness | Punch or laser/waterjet cut, countersink, deburr; no bends |
| Gallery seals | 2 | Polymax 255 ID × 3 section, EPDM 70 ShA | Two complete rings; three at the displayed price meet the user-reported £10 minimum with one spare; confirm dispatch estimate, one-piece moulded supply and coolant compatibility, no cutting/gluing |
| Cover screws | 31 | A4 stainless M4 × 12 DIN 7991, 2.5 mm hex; specified DIN 965 Z Pozi accepted | Approximately 9.22 mm nominal penetration with maximum listed socket head |
| Faceplate/body screws | 8 | A4 stainless M4 × 12 DIN 7991, 2.5 mm hex; Pozi alternative below | Approximately 9.02 mm nominal penetration in body with maximum listed socket head |
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

Each capsule pocket is 388 overall length × 16 overall height, R8 ends, 24 deep from the rear. Centres (x 0,z 23.5) and(x 0,z 63.5). The front wall is 16. The intervening solid web is 24 mm high; upper and lower external walls are 15.5. End walls are 26. A Ø16 end mill can generate the pocket; smaller tools can rough and finish it.

Each gland centreline is the pocket perimeter offset outward 4.0: capsule **396 overall × 24**, R12 ends. Centreline overall length/height ±0.10. Gland **width 4.00 +0.10/0, depth 2.30 +0/−0.05** from the rear POM mating face. These limits are within the Polymax guide's face-seal ranges for 3 mm section: width3.90–4.10 and depth2.20–2.30. The guide's2.50 radial-seal depth is not used. The steel cover seats directly on POM lands and compresses the protruding ring; further tightening after seating is not a way to adjust compression.

The 255 ID × 3 section ring has a free centreline circumference of810.53. Groove path is819.40, giving1.09% nominal elongation. A volume-conserving uniform-stretch estimate gives2.984 installed section, **0.684 protrusion, 22.92% axial squeeze and 76.00% rectangular-gland fill**. Before stretch, nominal squeeze is23.33%. STEP seal solids are volume-equivalent rectangular compressed envelopes (3.040 wide ×2.30 deep), not predictions of deformed rubber profiles.

Pocket-to-groove land is2.00; groove inside end radius10.00. Groove outer extent is400×28. The minimum nominal dry land to a conservative Ø4.2 cover-thread envelope is **1.90**, and outer Ø8.4 cover countersinks remain **1.30** inside the body/cover edge. Control outer cover-hole positions to±0.10 and countersink diameter to+0.10/0; agree the finished profile datum with the vendor. Allowing0.10 hole-position error,0.05 half-height error and0.05 half-width increase reduces the simple thread-to-groove land to about1.70 before other process variation.

Using the Polymax published tolerances of ring ID±1.85 and section±0.09, with the groove tolerances above and a closed cover, the centreline model gives **20.22–27.07% squeeze**, **69.34–83.23% fill** and **0.30–1.90% stretch**. Fill extremes conservatively include both groove-root corners atR0.20. These checks exclude coolant swell, thermal effects, cover separation/creep and pressure-driven ring movement towards the groove's outer wall. See [rear-seal calculations and supplier guide](rear-seals.md).

Indicative DFM requirements: gland/port seal finish Ra≤1.6 µm, cover seal face Ra≤0.8 µm, mating-face flatness 0.05 across each seal perimeter. General dimensions±0.15; port positions±0.10; gland dimensions as above. These are quote requirements to confirm, not supplier guarantees. Break exposed sharp edges 0.3–0.5, except sealing edges which need a controlled small edge break. Groove root radius≤0.2 to be agreed with the seal vendor. CAD omits microscopic edge treatments.

The wetted cover remains 316L: see [material compatibility assessment](wetted-materials.md). Remove oxide/heat tint and iron contamination as applicable, clean/passivate by an agreed vendor process, rinse and dry. Inspect sealing finish and flatness after treatment. Confirm an inhibited coolant compatible with stainless, copper/brass/nickel, POM and EPDM.

## Cover fastening

The rear plate has clearance holes only, with no threads and no rack slots. Punch or laser-cut the 31 Ø4.5 through holes, finishing them to Ø4.5 +0.10/0 as required, then machine the countersinks from the rear/outside face. Keep the POM-facing sealing surface free of countersinks and burrs. Use the same specified M4 × 12 DIN 7991 / DIN 965 Z screws as the front. Revision G retains Ø8.4 +0.10/0 rear countersinks: nominal ideal-cone recess is 0.22 mm for the Ø7.96 socket head and 0.45 mm for the Ø7.5 Pozi head. These are both M4 holes despite differing from the front Ø8.0 countersinks. Check sample head seating and blind-hole bottom clearance.

31 screw positions: the nine port-column X positions at z 5.5,43.5,81.5, plus x±213 at each gallery-centre Z. Cover clearanceØ4.5, Ø8.4 × 90° countersink from rear. Body pilotØ3.3 × 14 deep from y 40, M4 × 0.7, minimum 10 full thread. Confirm blind tapping run-out and screw bottom clearance. Heads flush or recessed; inspect actual seating.

## Flat rack faceplate

One 482.6 × 87 × 3 mm stainless plate; no bends or formed features. Eighteen Ø32 (+0.2/0) through windows centred on the ports. Window centre positions ±0.10 relative to the mounting pattern. Request a deburred, flattened sheet and agree flatness with the supplier. Punching can distort ligaments, so laser/waterjet cutting is also acceptable.

Each POM boss is Ø28 ±0.05, 6.00 ±0.05 high from the faceplate-supporting POM plane, with an R1 root fillet. Plate finished thickness 3.00 ±0.10 gives a nominal 3 mm axial stand-off, a dimensional minimum of 2.85 mm before plate flatness, assembly gap and other effects. The maximum root-fillet envelope is nominal Ø30, leaving 1 mm radial clearance in the Ø32 window. Check registration and the actual plate against the bosses before assembly.

The threaded boss end, not the stainless plate, is the seal datum. Bore/tap G1/4 from y = −6; the base front wall and gallery position are unchanged. The nominal wall around the thread at the boss is (28 − 13.157)/2 = 7.42 mm before thread/chamfer tolerances. Bosses are integral, milled from thicker POM stock by pocketing the surrounding face; they are not glued, pressed-in or separately threaded parts.

The fitting's O-ring must contact a complete flat POM annulus around the thread. A 3 mm stand-off prevents the faceplate from obstructing an ordinary flat fitting shoulder; it does not guarantee sealing independently of O-ring size/compression, thread length, contact finish or fitting geometry. Fitting bodies may overhang the boss, but an oversized O-ring cannot overhang its sealing face. No gasket is needed between the dry faceplate and the body. Finish seal lands to the specified roughness and inspect for burrs/damage.

Eight body mounting positions (X,Z): (−208,9), (−208,43.5), (−208,78), (+208,9), (+208,43.5), (+208,78), (−67.5,43.5), (+67.5,43.5). Faceplate holes Ø4.5 (+0.1/0), with Ø8.0 (+0.1/0) × 90° countersink from the front (y = −3). The nominal cone depth is 1.75, leaving 1.25 straight bore through a 3 mm plate. Body pilot Ø3.3 × 14 deep from the front; tap M4 × 0.7, minimum 10 mm full thread. These mounts remain separate from the pressure-cover screws and do not intersect galleries, seal grooves or rear screw bores.

Default purchase: 8 × M4 × 12 A4 stainless DIN 7991 socket countersunk, 2.5 mm hex, Westfield WF14434. Listed head Ø7.53–7.96, maximum height 2.48. Accepted alternative: M4 × 12 A4 stainless DIN 965 Z Pozi, PZ2, Westfield WF33490; listed head Ø7.5, height 2.20. Require these head envelopes and a 90° bearing cone when ordering. Westfield also cross-references the socket item to ISO 10642; this is not blanket permission to substitute a different ISO head geometry. Confirm DIN 7991 dimensions and fully threaded stock at this length.

The common countersink is deliberately dimensioned to accept both specified heads; it is not claimed to be a DIN 74 standard hole. Nominal seating targets the socket head flush or slightly recessed, with the smaller Pozi head lower in the same countersink. Optimise seating for the DIN 7991 socket head: nominal ideal-cone recess is 0.02 for the Ø7.96 head, and 0.25 for the Ø7.5 Pozi alternative. With the listed minimum socket head Ø7.53, nominal recess is 0.235. Target socket heads flush to 0.30 below the face and Pozi heads slightly below it; inspect with the actual screws. Slight proudness is permissible when the head remains outside the port/fitting keep-out and clears any other overlapping hardware; it is not automatically a functional rejection. This accounts for head-size variation instead of promising every screw will be exactly coplanar. Countersunk screw length includes the head: a 12 mm screw therefore penetrates approximately 9.02 (maximum-diameter socket head) or 9.25 (Pozi) into POM. These are geometric penetration values, not certified effective thread engagement; allow for entry chamfer, screw tip, length tolerance and tapping run-out. Verify actual sample seating and bottom clearance before releasing the batch. Do not deepen countersinks indiscriminately. The head bears on steel and the thread engages POM directly. The current clearance review checks heads projecting 0.20 above the plate against Ø36 cylindrical port hardware keep-outs. The minimum plan-view clearance from a maximum listed head edge to a keep-out is approximately 8.12 mm. This is a checked example, not a universal protrusion tolerance or a hand-access envelope. Larger fittings or added hardware require their own envelope check.

Keep the faceplate at 3.00 ±0.10. Both stated head envelopes, including recess, fit within this thickness; 2 mm does not contain their full height. A 2.5 mm plate leaves little or no allowance for the socket head and its seating recess. No increase to 4 mm is required just to house these M4 heads. This dimensional fit does not establish joint preload, pull-out capacity or plate stiffness under service loads.

Rack slots are 10 × 7, centres X = ±232.55, Z = 5.4 and 81.6: 465.1 horizontal and 76.2 vertical separation. Body width behind the rail plane is 440 mm. Verify fit and cage-nut access on the actual rack.

`output/cad/faceplate-flat.dxf` is a genuine flat profile in millimetres: DXF X/Y correspond to assembly X/Z, with origin at the faceplate's bottom centre. CUT contains the outline, eighteen Ø32 windows, eight Ø4.5 mounting holes and four rack slots. It deliberately omits countersink outlines to prevent them being cut through. Countersink the eight body mounts as a separate operation. Do not countersink the rack slots or port windows. The STEP includes the countersinks.

The front plate is the rack mount; the raised POM bosses provide the independent port sealing surfaces. The retained rear cover closes the wet galleries. A separate flat bottom support plate fixed to the body is allowed by the user but is not included in revision G; its fasteners would need their own clearance and load checks.

Direct POM threads are simple for the first prototype, but torque/preload and long-term retention must be validated. No tightening torque is established here. Review faceplate bending/deflection, QD insertion forces and hose loads; support hoses independently instead of relying on the plastic ports. No operating pressure or mechanical load rating is assigned to revision G.
