# Current manufacturing status

The operator accepted the complete Q-M04/Q-M03/R7-M01 set on 16 September 2026 and authorised a **separate new JLC order**, superseding the earlier hold. Submitted for file review on 16 September after explicit confirmation of UPS shipping at US$71.99. Prior material, finish and goods metadata were reused. No payment was made. Preserve the original orders and archives. [New-order submission record](jlc-order-2026-09-16.md).

The original **Q-M01 body +Q-M01 faceplate +R6-M02 radiator plate** were [submitted to JLCCNC for review before payment](jlc-quotation-2026-09-15.md) on 15 September 2026. On 16 September, the operator reported emailing JLC to **accept the stated faceplate manufacturing limitations and proceed**: ±0.1 mm laser tolerance and standard grinding/deburring, without guaranteed chamfering, sharp-corner removal or complete burr removal. This order-specific concession is recorded in the [feedback and acceptance record](jlc-feedback-2026-09-16.md#operator-acceptance). The submitted drawings, geometry and ZIPs remain unchanged; the concession accompanies their tighter original call-outs.

The last portal check, before that acceptance, showed faceplate Pending, radiator Awaiting Payment and POM body Approved; batch File Review, unpaid. JLC's acknowledgement and subsequent portal status have not been checked. Each part has its own matching-name STEP/PDF package; steel parts also include a DXF cut profile.

- [Q-M03 faceplate submission guide](jlc-submission-Q-M03.md): two-sheet drawing with bilateral ±0.10 mm tolerances and standard deburring.
- [Q-M04 body guide](jlc-submission-Q-M04.md): three-sheet body drawing with twelve explicit perimeter chamfers, all28 G1/4 and12 M4 call-outs, shorter13 mm M4 pilots, finished hole tolerances and seal lands.
- [R7-M01 submission guide](jlc-submission-R7-M01.md): R7 geometry with four R5 outer corners, three-sheet drawing, raw sheet finish on both broad faces.
- [JLC requirements and final checks](jlc-final-review.md): current official process/material rules, long-drilling acceptance, exact POM stock, functional finishes, mating coordinates, plate flatness and first-article checks.
- [Three-part file index](../output/submission/current-three-parts/README.md): verified ZIPs and cross-part manifest.

**Assembly is separate:** [Q assembly guide](assembly-Q.md) and [radiator assembly guide](radiator-rack-plate.md). The fabrication PDFs do not set screw torque, apply threadlocker or order bought-in hardware.

The long galleries were the principal CNC capability review item; the submitted Q-M01 body had Approved status at the last check; Q-M04 is now separately submitted for review, although no separate detailed gallery/stock declaration was visible in its product details. Black unfilled declared POM-C or POM-H is accepted in principle; JLC must identify its offered stock. Both2 mm stainless plates use sheet-metal fabrication and matching raw sheet finish. The current body retains M4 hole coordinates ±0.05; the Q-M03 faceplate specifies ±0.10 for every cut size and X/Z position, including Ø4.50 ±0.10 holes. This replaces the original faceplate’s tighter call-outs with the accepted capability. POM requirements are retained except for the new explicit perimeter chamfers. All20 boss roots retain positive nominal/tolerance clearance to the windows.

Earlier P review files and O-M02 supplier ZIPs are historical. Do not mix their16 mm M4 threads/18 mm pilots or old countersunk plate details into Q-M01. R6-M01 is superseded by the explicit finish issue, with no radiator geometry change.

Assembly, installation and performance studies are maintained separately; they are not fabrication instructions. See [Q assembly](assembly-Q.md), [radiator assembly](radiator-rack-plate.md) and [engineering retention study](Q-torque-and-creep.md).

## Q-M04 POM perimeter chamfers — 16 September 2026

The operator requested C0.5 ×45° on all twelve outside edges of the main block. Q-M04 models and dimensions C0.50 ±0.10 ×45° ±1°, with eight triangular corner flats per STEP. Only 267.833 mm³ is removed; every curved face, boss, bore and entry is unchanged. Seal lands and M4 bearing areas are outside the removed volume. The new three-sheet body drawing includes an enlarged detail; current reference assembly and affected renders use Q-M04. The two steel fabrication files are unchanged. Original JLC order files are preserved; this body is accepted for the separately authorised new order. See [Q-M04 guide](jlc-submission-Q-M04.md) and [JLC chamfer manufacturability assessment](Q-M04-chamfer-manufacturability.md). JLC has not yet accepted the new chamfer/corner call-outs.

## R5 outside-corner revision — 16 September 2026

At the operator’s request, the held issues are now Q-M03 and R7-M01. Both STEP/DXF profiles and PDFs specify four R5.00 ±0.10 mm outside corners. This is a cut-profile feature, distinct from face-edge deburring. Q-M01 POM and all steel holes/slots/notch/air apertures remain unchanged. Product, studio, radiator and StarTech25U renders use the new geometry. Original supplier-order archives remain intact.

## Historical outer-corner inspection — 16 September 2026

Direct inspection of the held-issue STEP and DXF confirms that **Q-M02 faceplate has four square outer corners**: its DXF perimeter is a four-vertex rectangle with zero bulges, and STEP has no outer corner cylindrical faces. **R6-M03 radiator has four R2 mm outer corners**, present in both STEP and DXF; the four STEP cylinders lie at X±239.3, Y2/442.5. The unchanged predecessor geometries have the same corners. These cut-profile radii are distinct from rounding the sheet's face edges or standard deburring. No geometry change was made during this inspection.

## Historical POM edge inspection — 16 September 2026

Direct inspection of the submitted Q-M01 body STEP and its three-sheet PDF confirms:

- All twelve outside edges of the 410 ×87 ×40 mm slab are sharp right-angle intersections in the nominal STEP: four 410 mm edges, four 87 mm edges and four 40 mm edges. No perimeter chamfer or outside-corner fillet is modelled.
- The twenty front bosses have modelled R1 root fillets and C0.5 ×45° outer-lip chamfers. The drawing specifies R1.00 ±0.10 and C0.50 ±0.10 ×45° ±1°.
- All 28 G1/4 mouths have modelled 45° entry chamfers: Ø13.80 mouth to Ø11.80 pilot, 1.00 mm nominal axial depth. The twelve M4 mouths have modelled Ø4.40 /90° included entries, 0.55 mm nominal depth.
- Drawing sheet 3 specifies “External edges: break 0.20 max unless otherwise specified.” This is a finishing allowance without a specified minimum, chamfer angle or radius; it is not modelled in STEP. It does not define a consistent visible perimeter chamfer. Seal lands remain protected from general rounding.

The user's EK comparison is an observation of their manifold; no exact EK perimeter-chamfer size has been established. No design, drawing or supplier-file change was made by this inspection. The steel R5 outside corners do not extend to the POM body.
