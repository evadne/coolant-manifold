# Option C — one flat backing plate, exposed POM face

This alternative implements the user's proposal to eliminate the faceplate and let the POM sit proud of the rack. Here “bottom plate” means a backing plate parallel to the vertical rack face, not a horizontal shelf. A horizontal plate alone would not present a mounting face to the vertical rack rails.

## Configuration

- One Delrin body, 440 × 40 × 87 mm. Port locations, galleries and seals follow Option B; eight M5 retention holes are on the rear, and the front has only its eighteen G1/4 ports.
- One flat 316L stainless backing plate, 482.6 × 87 × 3 mm, with a machined sealing face. This replaces both the separate rear cover and the front rack faceplate.
- Four 10 × 7 rack slots at X = ±232.55, Z = 5.4 / 81.6.
- Thirty-one M4 pressure-cover screws, with the same positions and countersinks as Option B.
- Eight independent M5 body-retention screws, accessible from the rear. Their X/Z pattern is the same as Option B, but Option C retains M5 while Option B revision E uses M4 DIN 7991. They enter POM from y = 40, towards the front.
- Two unchanged EPDM gallery seals. No port windows and no bent metal.

Mounting load passes from the body to the backing plate through the rear screw joint, then through the plate's outboard mounting regions to the rack fixings. The dedicated M5 screws provide body retention; the M4 screws distribute seal clamping. Both sets and the same plate remain mechanically coupled, so assigning them names does not isolate structural forces from the seal joint.

## Rack projection and access

The POM front stays at y = 0, body rear at y = 40, backing plate at y = 40…43. The rack's rail mating surface is y = 43. Consequently the POM face projects 43 mm ahead of the rail surface, or 40 mm ahead of the mounting plate's front face. Reference QD3-MTG4 male tips project approximately 75.1 mm ahead of the rail surface (43 + 32.1).

For current Option B (revision E), the rail mating surface is y = 0, raised boss ends are 6 mm ahead of it and male tips project about 38.1 mm. Thus Option C moves the fitting/service arrangement 37 mm further into the space in front of the rails. The 100 mm provisional service zone in front of the POM face becomes 143 mm in front of the rails. Connected female QDs, hose bends and a closed rack door still need an actual fit check.

Both alternatives retain eight parallel circuits, a main inlet/outlet pair, 45 mm horizontal and 40 mm vertical port pitch, and an 87 mm / 2U height. There is no loss of lateral QD spacing.

## Manufacturing differences from Option B

The shared G1/4 thread specification, gallery, rear seal and general tolerance notes in `manufacturing.md` apply. Option C does not use the raised-port features added to Option B revision D: its G1/4 seal datum stays at y = 0, with 16 mm wall to the gallery and Ø24 flat sealing lands. Ignore the boss dimensions and boss-related front machining notes for this option. For this option, replace the faceplate and rear-cover BOM rows with one backing plate; there are two manufactured solids, plus two seal envelopes in STEP.

The backing plate is cut or punched flat. Its body-facing area must then meet the existing seal-face flatness and finish requirements; it is not an untouched punched blank. Deburr the rack slots and screw holes and protect the seal face. No bend allowance is needed. The same 3 mm finished thickness is retained for comparison, not selected from a completed structural analysis.

M4 cover screws: 31 × M4 × 12, countersunk from y = 43, with nominal 9 mm body engagement. Plate holes Ø4.5 / Ø8.4 × 90° countersink. Body pilot Ø3.3 × 14 from y = 40, minimum 10 mm full M4 thread, as before.

M5 mounting screws: 8 × M5 × 12, countersunk from y = 43, with nominal 9 mm body engagement. Plate holes Ø5.5 / Ø10.4 × 90° countersink. Body pilot Ø4.2 × 14 from y = 40, minimum 10 mm full M5 thread. Positions (X,Z): (±208,9), (±208,43.5), (±208,78), (±67.5,43.5). No front or side mounting holes are present.

The DXF `output/backplate/cad/backplate-flat.dxf` contains one outline, four rack slots, 31 Ø4.5 cover holes and eight Ø5.5 body-mount holes. Units are mm, DXF XY = assembly XZ, origin at bottom centre. All entities are CUT geometry; countersinks are omitted from the cut layer and must be machined separately using the STEP/notes. This is the only steel plate in Option C.

## Assessment

This is the simpler arrangement by part count and front-face machining and removes the need to fit QD bases through faceplate openings. It also leaves the POM face fully exposed for access and marking. Its disadvantages are the additional front projection, rear access to all body-retention screws, and use of the pressure cover as the structural rack mount. Removing the backing plate opens the galleries; this is not a detachable dry rack bracket.

Plate bending near the rack fixings, seal-face distortion under hose/handling loads, screw preload, POM creep and rack-door clearance must be checked before preferring this option for manufacture. The body and fittings project in front of the rails, so pulling, side loads and impacts must be included in that review. The CAD checks establish connectivity and geometric separation, not a pressure or load rating.

The two alternatives are preserved for user review. No variant has been ordered or designated a production release.
