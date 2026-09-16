# Three-part JLC review: Q-M04 body, Q-M03 faceplate and R7-M01 radiator

Checked against live JLCCNC official pages on **15 September 2026**. Q is operator-approved; the subsequent M4 refinement uses 10 mm full thread, 13 mm pilot. Original R6-M02 specifies raw sheet finish, matching the manifold faceplate. The held Q-M03/R7-M01 issues add four R5 outside corners to each plate; other cut profiles remain unchanged. The three parts were [submitted for review before payment](jlc-quotation-2026-09-15.md). Subsequent review/acceptance is recorded in [manufacturing status](manufacturing.md). The new Q-M03/R7-M01 steel files are prepared locally; no replacement upload or payment is claimed.

| Part | Process / material selection | Finish and options | Supplier pack |
|---|---|---|---|
| RM10-Q-M04-BODY | CNC milling/drilling/tapping; black unfilled POM, declared POM-C or POM-H stock | As-machined; no polish/coating. Threads YES. 28 G1/4 +12 M4. External deburr only; flush loose chips. | Matching STEP +3-sheet PDF |
| RM10-Q-M03-FACEPLATE | Sheet-metal / flat laser-cut 2 mm SUS304, with hole finishing if needed | Raw stainless sheet finish on BOTH broad faces; no brushing or polishing. Plain through holes; flat profile. | Matching STEP +DXF +2-sheet PDF |
| SN1260-R7-M01-PLATE | Sheet-metal / flat laser-cut 2 mm SUS304, with hole finishing if needed | Same raw sheet finish on BOTH broad faces; no brushing or polishing. 68 plain fixing positions, four air apertures, 10×2 rounded cable notch. Plain through holes; flat profile. | Matching STEP +DXF +3-sheet PDF |

## Official requirements and their application

**Steel finish:** The operator selected raw stainless sheet finish for BOTH plates during quotation preparation, with no brushing or polishing. Q-M03 uses the accepted standard grinding/deburring; R7-M01 retains its specified edge breaks and cable-contact edge rounding. The live [sheet-metal quote form](https://jlccnc.com/sheet-metal-quote) lists a 1000×360 mm brushing limit, smaller than the radiator plate in its short dimension; brushing is therefore no longer requested. No grain direction is specified for raw sheet.

**POM:** JLC lists POM machining, but its generic article mixes POM-C terminology with homopolymer and injection-moulding discussion. It does not identify an offered black stock grade. Thus availability of POM is confirmed; **black unfilled stock, exact family/grade, 410×87×43 envelope stock and datasheet still need confirmation**. No Delrin brand requirement. As-machined exterior and the specified seal-land finishing are requested, not plastic polishing or chemical treatment. [JLC POM material page](https://jlccnc.com/help/article/pom-cnc-machining).

**CNC files and precedence:** STEP/STP is mandatory; JLC recommends matching-name 2D drawings. Geometry normally follows 3D, while threads, tolerances and roughness follow 2D; conflicting website selections override drawings. Accordingly each ZIP has one single-solid STEP with its same-name PDF, and upload options must match the table. The POM STEP deliberately represents tap pilots, as JLC recommends; finished thread type, pitch, depth and gauges are on the PDF. Specific limits require explicit selection and confirmation. [JLC ordering guidelines](https://jlccnc.com/help/article/cnc-machining-ordering-guidelines).

**CNC geometry and threads:** The POM body fits the published CNC envelope. Two Ø11.8 galleries through 410 mm require special deep-drilling review: one-sided ratio 34.75D; opposed nominal 207 mm reach is 17.54D. We have not found an official blanket acceptance for that drilling ratio and do not apply an end-milling cavity rule as a drill acceptance rule. The revised M4 full thread is 2.5× nominal diameter with 2.45 mm full-diameter run-out allowance after the entry/thread; it meets JLC's suggested ≤3D effective thread and ≥0.5D bottom allowance. G1/4 thread + run-out limits are separately specified for front/end and rear ports. [JLC design guideline](https://jlccnc.com/help/article/cnc-machining-design-guideline), [JLC threaded-hole guideline](https://jlccnc.com/help/article/threaded-hole-guideline).

**Steel stock and route:** JLC lists SUS304 sheet at 2 mm and an 800 mm maximum length. Both plates fit this route. Use sheet-metal ordering, rather than assuming their CNC flat-metal minimum of 3 mm admits a 2 mm plate. [JLC sheet materials](https://jlccnc.com/help/article/materials-supported-in-sheet-metal-fabrication), [JLC CNC size limits](https://jlccnc.com/).

**Sheet geometry/files:** JLC requires STEP; same-name PDF/DXF can accompany it in a ZIP. The guide lists 100 MB per file and up to 20 drawings per upload. Its hole minimum is max(1 mm, half thickness), and minimum hole-to-hole distance is 1 mm. Our smallest round holes are 4.5 mm in the manifold plate and 3.6 mm in R7. Both retain webs above that spacing. The manifold's optional outer rack slots retain a 1.90 mm edge ligament; the radiator's is 2.85 mm. Current steel issues use bilateral ±0.10 mm cut sizes and coordinates. Free-state flatness (0.30 manifold /0.50 radiator) is separate from JLC’s published cutting tolerance. Both parts are flat profiles. [JLC sheet-metal guide](https://jlccnc.com/help/article/sheet-metal-fabrication-guidelines).

## Final checks and open supplier questions

1. **POM drilling:** accept continuous 410 mm galleries, ≤0.30 mm axis deviation/meeting step, no blind webs and no wall breakthrough? Identify the method and any proposed changes.
2. **Material/finish:** confirm black unfilled stock grade, functional seal Ra≤1.6 µm/flatness0.05, other finishes and cleaning. No internal cross-hole deburring operation; external deburr only.
3. **Threads:** confirm G1/4 ISO228-1 tooling/gauging (not tapered threads), full8 after1 entry, and M4×0.7-6H full10 after0.55 entry in13 mm full-diameter pilots. No inserts or arbitrary substitute tapping.
4. **Mating dimensions:** Q-M04 body M4 centres remain ±0.05; Q-M03 plate centres and hole sizes use ±0.10. The accepted capability gives a conservative worst-case M4 radial margin of −0.0121 mm; it is not a guaranteed-interchangeability claim or an outstanding approval gate. See [fit assessment](Q-faceplate-as-drawn-capability.md). Ø32 ±0.10 windows retain approximately 0.517 mm worst-case boss-root clearance. Boss projection remains 0.85–1.15 mm size-only.
5. **Steel:** confirm sheet grade/thickness, hole sizes/positions, free-state flatness, raw sheet finish on both faces and external edge finishing. The cable-notch outline R0.5 is in STEP/DXF; R0.3-0.5 face-edge finishing is additional and must be performed after cutting.
6. **Part inspection:** inspect all finished thread types and depths, pilot depths, bore continuity and separation, seal lands, datum dimensions, hole sizes/coordinates, flatness, edge finish against each part's drawing.

Assembly and operational qualification are separate from this fabrication review: see [Q assembly](assembly-Q.md), [radiator assembly](radiator-rack-plate.md) and [retention engineering](Q-torque-and-creep.md).

## File selection

Use the three ZIPs indexed in `output/submission/current-three-parts/README.md`, each as a separate part. Use only matching current-issue files for each part. Uploaded files, exact submitted remarks, supplier references and review status are recorded in the [submission log](jlc-quotation-2026-09-15.md).

## New-order authority — 16 September 2026

The operator accepted the complete Q-M04/Q-M03/R7-M01 set on 16 September 2026 and authorised a **separate new JLC order**, superseding the earlier hold. Reuse prior material, finish and goods metadata; compare shipping services and obtain operator confirmation of the cheapest option before final submission. Preserve the original orders and archives. [New-order preparation record](jlc-order-2026-09-16.md). Q-M04 chamfer manufacturability is assessed in [the dedicated note](Q-M04-chamfer-manufacturability.md); supplier approval of the new issue remains outstanding.
