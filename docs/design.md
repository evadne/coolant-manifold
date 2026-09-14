# RM8-2U coolant manifold — initial design, revision B

Eight parallel circuits in two rack units, with vertically paired supply and return connections on one service face. The black Delrin body, repeated G1/4 ports and satin stainless steel hardware follow the requested industrial character of EK's Pro manifold. The design prioritises access to the female QD3 release rings.

## EK and rack-height comparison

EK lists the Pro 2CPU 8GPU manifold at 326 × 57 × 36 mm (L × H × W), without its mounting system. One rack unit is 44.45 mm; two are 88.9 mm. Its stated 57 mm height exceeds 1U by 12.55 mm, and leaves 31.9 mm within 2U before mounting and access allowances. Rotating the 36 mm dimension vertically fits the bare body height, but changes port orientation and does not prove coupling or hand clearance.

This initial design uses a finished 87 mm high panel, leaving 1.9 mm total clearance within 2U. It is deliberately wider and taller than EK to provide access around the ports. EK's exact port pitch has not been verified from an accessible dimensional drawing; no spacing here is claimed to be copied from it.

## Layout

| Feature | Revision B |
|---|---|
| Delrin body | 440 wide × 40 deep × 87 high |
| Front rack faceplate | 3 thick, eighteen Ø28 windows |
| Rear stainless cover | 3 thick |
| Bare rack assembly | 482.6 wide × 46 deep × 87 high |
| Branches | 8 parallel circuits |
| Ports | 18 G1/4 female: 8 supply + 8 return + IN + OUT |
| Horizontal pitch | 45 |
| Vertical pitch | 40 |
| Port rows | z=23.5 supply; z=63.5 return |
| Rack slots | 10 × 7; 465.1 horizontal and 76.2 vertical centres |

Looking at the service face, the lower row is IN, S1…S8 and the upper row is OUT, R1…R8. Each vertical S/R pair belongs to one load. IN and OUT occupy the leftmost column. All ports share the same face and thread type. Plug any unused connections or use the intended self-closing QDs.

The two galleries are the common supply and common return required for parallel flow. Neither gallery has partitions, internal plugs, selectable groups or a bypass. The solid web between them keeps supply and return separate. Connect S1 → load 1 → R1, and similarly for all eight circuits. IN receives flow from the pump; OUT returns flow to the external loop.

Parallel flow is not inherently equal. Different blocks, hoses and QDs have different resistance. The design provides no internal balancing and makes no thermal-capacity claim. As drawn, both main ports are at the same end (direct return); this is a practical routing choice, not a claim of equal header pressure at every branch.

## QD3 service clearance

Reference male: Koolance QD3-MTG4. The drawing shows 36.6 ±0.5 overall, 4.5 male thread and approximately 32.1 projection from the face; 22 across flats and 23.9 outside diameter. The earlier QD3-MSG4 has a 4 mm thread and about 31.1 mm face projection.

Reference female: QD3-FS10X16 for 10/16 mm hose. Its drawing shows a 23.7 mm pull ring, 23 mm across flats at the compression end and 46.2 ±0.5 mm overall. A regular 23 mm hex can reach 26.56 mm across corners. Consequently:

| Clearance between adjacent reference fittings | Horizontal | Vertical |
|---|---:|---:|
| 23.7 mm release rings | 21.3 | 16.3 |
| 26.56 mm compression-hex envelope | 18.44 | 13.44 |
| Conservative 28 mm circular envelope | 17 | 12 |

The ring-to-body-top/bottom edge clearance is 11.65 mm; actual 2U boundaries give another 0.95 mm each. Rings project in front of the mounting plane, allowing access from the front, sides and between rows. These dimensions improve access substantially compared with the explored dense 1U arrangement, but do not constitute an ergonomic validation. Verify the actual female variant, hand/glove size and release stroke with adjacent real fittings. The included full-size SVG is intended for that trial.

Reserve 100 mm unobstructed service space forward of the port face. This is a layout allowance for hand access and axial disconnection, not a measured release stroke or a hose bend-radius specification. The sum of the uncoupled reference projections is approximately 78.3 mm; coupling overlap reduces the connected length. Blender shows simplified reference fittings and four example female/tube connections; their connected geometry is illustrative. Hose bends may extend outside 2U. The rack door and adjacent equipment must remain clear of the service region.

## Construction and manufacture

Two continuous capsule pockets are milled from the rear of one Delrin block. Each is 400 × 16 in the XZ plane and 24 deep, leaving a 16 mm front wall. Their centres are z=23.5 and 63.5; ends are R8. All front ports drill into the appropriate pocket. There are no buried junctions or deep longitudinal drilled galleries.

Each gallery has its own continuous EPDM seal beneath a 3 mm stainless steel rear cover. The rigid cover avoids a large thin plastic pressure lid. Its underside is a machined sealing face, not unfinished sheet. A single 3 mm flat stainless steel faceplate carries the body on the rack. Its eighteen Ø28 mm windows expose the original POM port faces. Eight dedicated front-facing M5 screws fasten the body to it; the QDs are not mounting fasteners. The previous bent ears and side mounting holes are removed. The POM outer shape, port arrangement, galleries and rear seal design are unchanged.

The operations are conventional 3-axis milling with rear/front setups, standard threaded holes, profile punching or cutting and countersinking. No metal bending is required. This is a design for vendor DFM and budget quotation, not a promise of instant-quote acceptance. Confirm branded Delrin homopolymer, stock size/porosity, sealing flatness and BSPP tooling. Generic POM offered by a vendor is not automatically Delrin.

## Faceplate and fitting seating

The faceplate occupies y = −3…0, with the POM sealing face at y = 0. Its windows must clear the fitting base and the portion of the hex lying within the plate thickness, not merely the nominal Ø13.157 G1/4 thread. A conservative 22 mm AF male hex has a Ø25.404 circumscribed envelope; the Ø28 opening leaves about 1.30 mm radial clearance before positional tolerances. The entire Ø24 POM sealing land is exposed.

The fitting screws through the clearance window and stops against POM. Its O-ring seals there, not on stainless steel. The plate therefore consumes none of the reference 4.5 mm male thread engagement. Do not shrink the opening to a thread-clearance hole: the fitting could then bottom on steel before sealing on POM. Deburr and lightly edge-break each window to protect fitting surfaces and fingers.

The plate is a dry structural rack mount, not a wet sealing component. The eight body-retention screws remain installed when fittings are changed. Hole size and fastener alignment are checked geometrically; final tolerance stack, fitting fit, screw preload, plate deflection and load capacity still require review. Keep the 45 × 40 mm port pitch.

The user also permits a bottom plate fixed to the body. Such a flat support plate can be added independently if installation loads require it; it is not included in this revision. The existing rear gallery closure is retained as its own body-mounted plate. No folds or bent ears are needed for the current mounting arrangement.

## Status and open engineering work

This is an initial dimensional model, not a pressure-rated production release. Working pressure, coolant, temperature, pump shut-off head and desired flow have not yet been specified. No structural FEA, seal validation, creep test or hydraulic test has been performed. QD component pressure ratings do not rate the manifold assembly.

The G1/4/QD3 main pair carries the sum of all branch flows and may dominate pressure loss. Establish the required total flow before treating eight circuits as a cooling-capacity promise. There is no dedicated drain or bleed connection in revision B; draining/bleeding is via the external loop and appropriate orientation. Closed unused QDs cannot vent air.

Before manufacture release: choose actual QDs and coolant; trial release-ring access; confirm continuous seals and gland dimensions; review plastic threads, cover flatness, preload/torque and creep; check rack and hose loads; then agree separate-gallery leak/cross-leak, thermal-cycle and pressure qualification for the intended working pressure.
