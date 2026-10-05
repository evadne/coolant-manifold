# Revision O: manufacturing revision O-M02

> **Historical reference — superseded.** This page describes an earlier design or assessment. Its recommendations and “current” labels apply only to that snapshot. Use the [current project guide](../../README.md) and [three-part recap](../three-part-recap.md) for P / R6.


The operator-approved O layout is preserved at `980b4d4`. O-M02 implements the subsequent operator request: bosses are 4 mm high, equal to the 3 mm faceplate plus 1 mm. The 40 mm main slab, port pitch, gallery positions, faceplate and fixing locations remain as approved. The earlier 6 mm boss revision is preserved in [O-M01](manufacturing-O-M01.md). It is prepared for supplier quotation and engineering review; it is not an accepted supplier order or a pressure-rated release.

## Files for quotation

The final [JLC submission handover](jlc-submission-O-M02.md) includes separate upload ZIPs, ready-to-paste part remarks and checksums. Updated [bare](../../output/manufacturing/O-M02/photorealistic/01-bare-ports.png) and [connected](../../output/manufacturing/O-M02/photorealistic/02-qd3-translucent-tubes.png) studio renders use the released O-M02 STEP geometry and new sealing plane.

| Part | Drawing | Upload bundle |
|---|---|---|
| POM body | [Three-sheet A3 PDF](../../output/pdf/RM10-O-M02-BODY.pdf) | [STEP + PDF ZIP](../../output/manufacturing/O-M02/RM10-O-M02-BODY.zip) |
| Front rack faceplate | [Two-sheet A3 PDF](../../output/pdf/RM10-O-M02-FACEPLATE.pdf) | [STEP + PDF + cut DXF ZIP](../../output/manufacturing/O-M02/RM10-O-M02-FACEPLATE.zip) |

Read the [two-page JLC manufacturability review](../../output/pdf/RM10-O-M02-DFM.pdf) alongside the drawings. Individual solids, a feature schedule, verification reports and checksums are in `output/manufacturing/O-M02/`. The DXF describes through-cuts only; the countersinks are specified in the STEP and PDF. Do not cut their Ø8 mouths through the plate.

Quote the parts separately. Set **Threads YES for the body** (24 G1/4 plus six M4) and **Threads NO for the faceplate**. Select materials and manufacturing options consistent with the PDFs, and tell JLC that the two parts mate. The bundles contain matching-basename STEP/PDF files and only supported upload types. JLC requires STEP geometry and drawing call-outs for threads; the model intentionally contains tapping pilots, not helical threads. [JLC ordering guidance](https://jlccnc.com/help/article/cnc-machining-ordering-guidelines)

For the intended computer coolant duty at an expected maximum liquid temperature of 50°C, **both POM-C and POM-H remain acceptable candidates**; see the [coolant-specific material assessment](../pom-coolant-assessment.md).

## Material and edge requirements

- Body: **black unfilled POM**, accepting POM-C or POM-H. Branded Delrin is not required. The supplier must identify its grade and stock form, provide the material datasheet, and supply material conforming to that declared grade. JLC lists POM, but its public listing does not establish the exact black stock or branded resin that will be supplied. [JLC POM listing](https://jlccnc.com/help/article/pom-cnc-machining)
- Faceplate: dry **304 stainless / EN 1.4301**, SUS304 equivalent. JLC lists SUS304. There is no wetted rear cover in this iteration. [JLC stainless listing](https://jlccnc.com/help/article/sus304-cnc-machining)
- **External deburring only. Internal bore and cross-hole edges do not require deburring.** Clean/flush the internal passages to remove loose machining chips. This is a cleaning requirement, not an internal edge-finishing operation.
- Modelled boss lips receive **C0.5 ×45°**; retain the R1 roots and existing Ø13.8 ×90° port entries. Unspecified external edges receive a light 0.10–0.20 mm break, with explicit feature dimensions taking precedence. Preserve the flat O-ring sealing lands.

## Detail changes from approved O

The derived body STEP shortens all twenty bosses from 6 mm to 4 mm and repositions their G1/4 entry chamfers onto the new Y−4 sealing plane. It includes twenty outer boss chamfers, six Ø4.4 M4 entry cones and six conventional 118° M4 pilot drill points. Overall POM depth becomes 44 mm; the front drilling full-diameter depth becomes 24 mm from the boss face to the unchanged gallery axis. Original O files remain unchanged. The longitudinal galleries and front-to-gallery intersections are unchanged. The faceplate STEP and DXF are copied unchanged from O.

The drawing clarifies full-form thread length separately from entry lead-in and drill depth: G1/4 has 8 mm minimum full form after the entry, with thread/run-out ending within 16 mm of the seal face; M4 ×0.7-6H has 10 mm minimum full form after entry and a 14 +0.50/0 full-diameter pilot. The additional total-tip limit also applies. G1/4 is parallel ISO 228-1; no NPT or ISO 7 substitute.

The **1 mm nominal projection** becomes 0.8–1.2 mm under the boss-height and plate-thickness size tolerances alone, before flatness and assembly effects. The fitting must seat on the raised POM sealing land. A smaller projection does not itself establish clearance for every possible fitting shoulder or installation tool.

Use **Ø32 +0.20/0 faceplate windows** around Ø28 ±0.10 bosses. The R1 root reaches Ø30 nominal at the plate mating plane, so a Ø29 window would interfere. The maximum specified root envelope is Ø30.3. At the stated independent ±0.10 X/Z position tolerances on both parts, 0.567 mm radial reserve remains when the datum frames are aligned. This calculation excludes thermal growth, screw-hole registration and deformation; trial assembly is still required.

Retain the **3 mm faceplate**. Six Ø4.5 through holes have Ø8 ×90° front countersinks: 1.75 mm nominal depth and 1.25 mm remaining cylindrical land. The standard screw remains A4 M4 ×12 DIN 7991; the specified DIN 965 Z Pozi alternative seats lower. Head fit is controlled against the specified screw family because similarly named countersunk standards can have different head dimensions. [Socket reference](https://www.westfieldfasteners.co.uk/A4-ScrewBolt-SHCsk-M4.html), [Pozi reference](https://www.westfieldfasteners.co.uk/A4-ScrewBolt-PoziCsk-M4.html)

## Manufacturability finding

The flat faceplate is a conventional machining candidate. Laser profiling followed by countersinking is another route if the final tolerances and flatness are met. No bending is required. [JLC sheet-metal guidance](https://jlccnc.com/help/article/sheet-metal-fabrication-guidelines)

The body needs **manual deep-hole drilling acceptance**. Each Ø11.8 gallery is 410 mm long: 34.75D from one end, or approximately 17.54D for 207 mm opposed drilling with 4 mm nominal overlap. These ratios are calculations, not published JLC capability limits. The proposed ≤0.30 mm axis deviation and ≤0.30 mm meeting step require an agreed drilling and inspection method. Removing internal deburring does not remove the deep-drilling and chip-removal work.

Both parts are inside JLC's published overall size envelope. Generic wall and thread design guidance supports the local geometry, but does not prove long-bore alignment, sealing finish or structural performance. Ask JLC to confirm the resin grade, bore process, G thread tooling/gauges, R1 boss-root machining and specified functional finishes before cutting. [JLC CNC design guidance](https://jlccnc.com/help/article/cnc-machining-design-guideline), [thread guidance](https://jlccnc.com/help/article/threaded-hole-guideline)

The approved twelve optional rack slots remain. The outermost slots retain a 1.9 mm nominal edge ligament and possible washer overhang. The previous 2 mm elbow/nut clearance uses illustrative hardware envelopes. These are retained design limits, not new dimensional changes in O-M02. Actual fittings, rack hardware, coolant compatibility, clamp preload, creep and assembled leakage require physical qualification.

## Verification and rebuild

CAD-derived checks establish valid single solids, no nominal plate/body overlap, separated wet networks and 9.441 mm minimum clearance from a conservative nominal M4 drill-depth envelope to the wet network. Re-import checks independently verify boss/port chamfers, M4 entry/drill features, all plate circles/countersinks, and all twelve DXF slot sizes/locations. These checks do not simulate manufacturing or certify pressure performance.

The seven PDF pages were rendered and visually inspected. Packaging checks verify page counts, material/deburring notes, ZIP contents and checksums. Thread helices and general light external deburring are intentionally not modelled.

Rebuild in order:

1. `.venv/bin/python scripts/prepare_manufacturing.py`
2. Run `scripts/draw_manufacturing.py` with Python containing ReportLab and the documented Arial fonts.
3. `.venv/bin/python scripts/verify_manufacturing.py`
4. Render and visually inspect all changed PDF sheets.
5. Run `scripts/package_manufacturing.py` with Python containing pypdf.

Parameters are in `cad/manufacturing/O-M02.json`; dimensional layout remains in `cad/iterations/O-long-bore.json`. The revision date is fixed in the manufacturing parameters so rebuilds retain the same drawing revision.
