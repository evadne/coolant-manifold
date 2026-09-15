# Current manufacturing status

The current set is the matching **P manifold body and P faceplate**, plus the **approved R6 radiator plate**. Do not use an older supplier package to manufacture a current part. No supplier upload or order has been made.

| Part | Available files | Release work remaining |
|---|---|---|
| P body | [STEP](../output/long-bore-P/cad/body.step), [two-sheet P review PDF](../output/pdf/manifold-revision-P.pdf), geometry/retention checks | Prepare a dedicated P manufacturing issue, full feature schedule, tolerances, final machining call-outs, DFM review and part ZIP. |
| P faceplate | [STEP](../output/long-bore-P/cad/faceplate.step), [DXF](../output/long-bore-P/cad/faceplate-flat.dxf), same review PDF | Issue alongside the matching P body; no countersinks or tapped steel holes. |
| R6 radiator plate | [R6-M01 part ZIP](../output/submission/R6-M01/SN1260-R6-M01-PLATE.zip), matching STEP/DXF/three-sheet PDF, remarks and checksums | Supplier confirmation of process, tolerances and flatness; first-article fit. See [submission guide](jlc-submission-R6-M01.md). |

O-M02 remains a historical manufactured-part definition: 3 mm countersunk plate, six M4 retainers, 4 mm bosses and shorter M4 thread/pilot depths. Its ZIPs are **not the current P pair**. The common POM/coolant research remains useful, but old dimensions must not be copied into P drawings.

## P interface requirements to carry into its supplier issue

- Body: black unfilled POM-C or POM-H, identified stock grade and datasheet; 410 ×87 ×40 main slab, 3 mm integral bosses and 43 mm overall depth.
- Twenty front and four side **G1/4 female BSPP, ISO 228-1** ports. Pilot cylinders in STEP are not finished plain holes or thread helices. Nominal full-form thread depth is 8 mm; the production drawing must explicitly define its datum, entry, run-out and inspection requirements.
- Two Ø11.8 long galleries through the 410 mm width, centred at Y20. Opposed drilling with 4 mm nominal overlap requires about 207 mm reach per side, approximately 17.54 diameters. Supplier deep-hole acceptance and alignment/meeting-step requirements must be reviewed rather than assumed from ordinary CNC capacity.
- Boss ends are fitting seal lands. Retain Ø28 bosses, R1 roots, C0.5 ×45° outer lips and the current port entries. Preserve complete annular seating surfaces.
- External deburring only; internal cleaning/flushing removes loose chips. No internal cross-hole edge-finishing operation is required.
- Twelve M4 ×0.7 POM mounting holes: Ø3.3 pilots, 18 mm full-diameter depth plus 118° drill points; at least 16 mm full-form thread after entry. Nominal M4 ×16 screw reach through the 2 mm plate is 14 mm. Final supplier call-outs must preserve tip clearance and entry/run-out allowances.
- Faceplate: dry 304 / EN 1.4301, 482.6 ×87 ×2; twenty Ø32 windows, twelve Ø4.5 plain retention holes and twelve optional rack slots. No bending, tapping or countersinking. Use the actual matching P window/boss tolerances; old O-M02 tolerance calculations are historical evidence, not an issued P specification.
- Body hardware: twelve M4 ×16 ISO 7380-1 A2 stainless button heads, Westfield WF2237. Plain-bearing alternatives need correct length and head clearance. Countersunk screws are incompatible. Rack screws/cage nuts are a separate interface.

The [P detail](revision-P-plain-bore-faceplate.md) records nominal interference and head-clearance checks. These do not establish torque, creep life or an assembly pressure/load rating. [Coolant/material selection](pom-coolant-assessment.md) and [Blitz overrun targets](blitz-overrun-qualification.md) remain applicable.

## Remaining work, in order

1. Prepare the two P supplier issues from the current CAD, including complete hole schedules and drawing tolerances; cross-check them as a mating pair.
2. Verify the P PDF/STEP/DXF consistency, inspect rendered sheets and package each part separately. Keep R6-M01 separate.
3. Obtain supplier DFM confirmation when submission is authorised: POM grade, long bores, BSPP threading, functional finishes and plate tolerances.
4. Trial-fit bought-in fittings, rack hardware, radiator and fans on first articles. Resolve mechanical, flow and exposure qualification using the actual assembly and duty.

The accepted Koolance studio placement does not need another visual approval. Current deliverables and rebuild commands are indexed in the [project guide](../README.md) and [rebuild guide](rebuild.md).

## Open manifold integration concern

The current approved P slab is40mm, excluding3mm bosses. The StarTech25U scene uses outer manifold rack slots provisionally, but90° side-elbow compatibility with actual rail/cage-clip/screw-tail hardware remains open. A separate centred-gallery sensitivity check finds45mm still overlaps the present conservative nut envelope;50mm gives only1.5mm nominal depth clearance. No P geometry or supplier definition has been changed. See [the fit concern and comparison](context-25U.md#open-concern-manifold-side-elbows-and-cage-nuts) before treating any slot choice or thicker slab as a qualified solution. This concern does not concern radiator width or require changing R6.
