# Watercool MO-RA X-Splitter fit assessment

**Conclusion: compatible with the selected fan-centre spacing, based on the operator's physical fit evidence and the Alphacool reference geometry.** On 15 September 2026 the operator confirmed that the Watercool MO-RA X-Splitter for Noctua NF-A20 sits snugly in Alphacool's existing four-NF-A20 fan plate for this radiator. R3/R4 use the same 200 × 200 mm fan-centre grid. No increase in fan spacing or change to the steel cut profile is indicated by this assessment.

## Independent spacing check

The Alphacool 14351 manufacturer mesh includes the four-fan plate on its Y = +24 mm outer face. Its four approximately Ø195 openings have nominal centres X = ±100, Z = 112/312, relative to the radiator centre at Z = 212. The surrounding small mounting holes independently give the same centres: X −178/−22 and +22/+178, with Z34/190 and Z234/390. Midpoints are exactly X±100, Z112/312: **200 mm horizontally and vertically**.

In our plate coordinates the radiator centre is at height222.25, so these become X±100, height122.25/322.25: exactly the R3/R4 fan centres. Changing the local fan fixing pattern to 170 × 170 mm does not move the fan bodies. The 12 mm steel webs describe the apertures; they must not be confused with a uniform 12 mm free gap between fan frames. The usable space follows the shaped NF-A20 frames and is cross-shaped.

## Splitter and installation

[Watercool SKU60327](https://shop.watercool.de/MO-RA-X-SPLITTER-FOR-NOCTUA-NF-A20_1) lists dimensions 105 × 9 × 105 mm, one 4-pin PWM input and four 4-pin fan outputs. Product photos show a cross-shaped board seated between four NF-A20s. The 9 mm dimension is assembly depth, not an independently specified arm width. No dimensioned board outline or mounting drawing was found on the product page; no exact splitter CAD or numerical part-to-part clearance is claimed here.

The operator's stock-plate fit observation is stronger evidence for the fan-frame gap than an approximate silhouette reconstructed from these photographs. Treat this as a supported accessory choice for the equivalent fan layout, while checking the local assembly details when a sample is installed:

- Centre the splitter at X0 / plate height222.25. Keep it in the central pocket on the fan side of the steel.
- R4's button heads sit on the core side of the plate; its nuts sit outside the fan faces. These are not located within the plate-adjacent 9 mm-deep pocket. The screw shafts occupy the fan mounting holes. This arrangement avoids adding a projecting screw head beneath the splitter on the fan side.
- The four innermost fan fixings are at X±15 / relative height±15. Their Ø9 washers leave a 21 mm-wide cross corridor in projection, before considering fan-frame shape. This is a hardware-envelope observation, not a certified PCB width limit.
- Fix and electrically isolate the splitter using nonconductive double-sided tape, as selected by the operator. Follow the installation requirements below. The catalogue does not specify a dedicated mounting-hole pattern; do not invent tapped holes in the plate for it.
- Orient the fan cable exits towards the splitter and check reach of the actual leads. Any fan rotations should retain clearance from the compact radiator M3 heads. The photographed tidy installation uses the Chromax arrangement; standard brown fans may require managing their longer leads.
- One splitter serves four fans. An eight-fan push/pull arrangement uses one per bank and an appropriate upstream connection. The separately required PWM supply extension is stated on Watercool's product page. Electrical current-capacity assessment is separate from this mechanical fit check.

## Selected isolation and retention method

Use **electrically insulating double-sided tape** between the splitter PCB and the stainless plate. The tape provides both retention and the dielectric barrier. Do not rely on paint, a passive oxide film or another surface treatment as the electrical isolation: protruding through-hole connector pins or solder joints could damage a coating and contact conductive steel.

Installer guidance:

- Use tape with an electrically insulating carrier and adhesive, with suitable adhesion and service-temperature specifications. Conductive adhesive or metal-foil tape is unsuitable. No particular tape product or thickness has yet been qualified.
- Inspect the PCB underside before fitting. Arrange the tape to support the board and isolate every exposed conductor that could approach the plate. After compression, protruding pin ends and solder joints must neither touch the steel nor puncture the tape. Determine the required tape thickness from the actual underside geometry; do not assume a nominal tape thickness is sufficient.
- Bond to clean, dry surfaces prepared according to the tape supplier's instructions. Allow for the tape thickness when checking splitter height, connector access and fan clearance.
- Support the splitter when connecting or disconnecting fan leads. Do not press sharp pin ends into the tape or drag the PCB across the plate. Route and retain cables so their pull does not peel the tape or move the board towards an impeller.
- Inspect the attachment and insulation during servicing. Replace tape that has lifted, shifted, torn or been punctured; do not rely on a damaged layer merely because the splitter still operates.

These are installation requirements, not a claim that a particular adhesive system has passed ageing, puncture or dielectric testing. No change to the steel surface finish is required for this isolation method.

R3/R4 STEP, DXF, drawings and renders remain unchanged. This assessment does not claim an exact splitter-body collision check or change the previous structural qualification limits.

References: [Alphacool catalogue mesh](https://3dcenter.alphacool.com/stl/14351_0.stl), retained as `docs/references/alphacool-14351-manufacturer.stl`; [Watercool product specifications and installation photograph](https://shop.watercool.de/MO-RA-X-SPLITTER-FOR-NOCTUA-NF-A20_1), viewed 15 September 2026; operator report in this task on the same date.
