# Q faceplate at JLC standard capability — unchanged geometry

16 September 2026. Investigation completed before the operator subsequently [accepted JLC’s stated limitations](jlc-feedback-2026-09-16.md#operator-acceptance) by email. Preserve the calculations below as the pre-acceptance assessment, not an outstanding approval gate. No drawing, STEP, DXF or supplier ZIP has been changed. Scope: the Q manifold faceplate under JLC's proposed sheet-metal capability, mated to the existing Q POM body.

**Practical assessment: the unchanged nominal geometry is likely to assemble, but the published capability alone does not guarantee every tolerance-extreme combination.** The boss windows have ample clearance; the twelve M4 retention holes are marginal only when minimum hole diameter and opposing positional extremes coincide. The supplier cannot comply with the unchanged drawing literally: its tighter coordinate/size/edge-finish call-outs would still need a recorded concession or revised specification.

## What JLC's capability means here

[JLC's sheet-metal guidelines](https://jlccnc.com/help/article/sheet-metal-fabrication-guidelines), checked 16 September 2026, state cutting and hole-diameter tolerances ±0.1 mm, and general tolerances ±0.2 mm. Nelson's order-specific email states ±0.1 mm laser tolerance and standard grinding/deburring only. See the [verified feedback record](jlc-feedback-2026-09-16.md).

For this calculation, interpret ±0.1 as independent X/Z centre-coordinate limits measured from the drawing's common origin, and ±0.1 on the finished diameter. The guide/email do not fully define a positional tolerance zone, datum control, accumulated pitch error, hole taper or inspection method. This interpretation needs confirmation if used as the acceptance basis. In particular, do not silently substitute the guide's ±0.2 general tolerance for these hole coordinates.

Keep the **POM M4 coordinates at their submitted ±0.05 mm**. Only the plate is being assessed at looser capability; the earlier example relaxing both mating parts is not the present scenario.

## M4 retention: quantified fit

Source dimensions: `cad/manufacturing/Q-M01.json`, retained P geometry in `cad/iterations/P-long-bore.json`, and the Q drawing generator `scripts/draw_Q_production.py`. Current hardware is M4×10 ISO 7380-1, as selected in `cad/assembly/Q.json`.

For parallel axes and rigid parts at a common datum registration:

- Maximum mismatch per axis = 0.10 plate + 0.05 POM = **0.15 mm**.
- Maximum radial mismatch `e = sqrt(0.15² + 0.15²)` = **0.212132 mm**.
- Radial clearance `c = (finished hole diameter − screw envelope diameter)/2`.
- A sufficient clearance condition is `c ≥ e` at every hole.

| Case, with plate centres ±0.1 and POM centres ±0.05 | Minimum hole | Screw envelope | Radial clearance | Residual after centre mismatch |
|---|---:|---:|---:|---:|
| Retain drawing's minimum hole size | 4.500 | 4.000 | 0.2500 | **+0.0379 mm** |
| Apply JLC ±0.1 to nominal Ø4.5 | 4.400 | 4.000 | 0.2000 | **−0.0121 mm** |
| Same minimum hole, thread-major-diameter sensitivity | 4.400 | 3.978 | 0.2110 | **−0.0011 mm** |
| Optional future Ø4.6 ±0.1 hole, unchanged coordinates | 4.500 | 4.000 | 0.2500 | **+0.0379 mm** |

The 4.00 mm envelope avoids relying on a particular screw batch or on thread clearance. [ITP's socket-thread table](https://itpbolt.com/wp-content/uploads/2015/08/Thread-Dimensions.pdf) gives an M4 external major diameter maximum of 3.978 mm (6g major-diameter tolerance), illustrating why actual threaded screws are less demanding than a perfect Ø4 cylinder. This sensitivity does not certify the complete under-head transition, coating or actual supplied screw envelope. Do not use the approximately one-micron residual as a meaningful manufacturing guarantee.

A hole at its nominal Ø4.5 therefore clears the full assumed positional stack. With the conservative Ø4 screw envelope, the minimum effective clear diameter required by this calculation is **4.424264 mm**. JLC's nominal Ø4.5 ±0.1 band straddles that threshold. It is reasonable to expect a practical first article to fit, but no process distribution or fit yield can be inferred from a tolerance limit alone.

Common offset can be removed by positioning the plate during assembly; opposite individual hole errors cannot necessarily all be removed by one translation/rotation. The bound intentionally does not take credit for POM flexure, screw tilt, thread play or forcing screws into alignment. Negative residual means the stated capability does not prove clearance, not that an actual delivered plate will fail. Positive residual is a size/position check assuming clear, normal bores, not a full joint qualification.

For sensitivity, if JLC instead used ±0.2 per-axis hole coordinates, the relative offset would rise to `sqrt(2)×(0.2+0.05) = 0.3536 mm`, exceeding even a nominal Ø4.5 hole's 0.25 mm radial clearance. The meaning of the quoted ±0.1 matters.

## Boss windows, sealing clearance and rack slots

**Boss windows pass comfortably.** Applying ±0.1 to nominal Ø32 gives a 31.9 mm minimum window. The POM drawing retains Ø28 ±0.1 bosses, R1 ±0.1 roots and port coordinates ±0.1. At the mounting plane, conservatively enclose the entire root by a radius of `28.1/2 + 1.1 = 15.15 mm`. With opposing ±0.1 plate/window and POM/boss coordinate limits:

`minimum root clearance = 31.9/2 − 15.15 − sqrt(0.2²+0.2²) = 0.5172 mm`.

This leaves over **0.5 mm radial clearance including the root fillet and positional stack**, without relying on edge breaking the window. The plate is not the G1/4 sealing surface. Keeping existing 3.00 ±0.05 mm boss height and 2.00 ±0.10 mm sheet gives **0.85–1.15 mm size-only projection**. The plate must still seat properly; cutting accuracy says nothing about raised burrs or uncontrolled sheet flatness.

Rack slots at 10×7 ±0.1 would be at least 9.9×6.9 mm. A conservative Ø6 rack-screw envelope has 0.45 mm minimum vertical radial clearance before rack-side positional errors; the 0.1 mm slot-location change alone is small. Actual rack alignment and cage-nut float remain separate. The accepted outer slot's approximately 1.9 mm nominal edge ligament is not improved by looser tolerances; allowing 0.1 mm each on slot location and adjacent profile and 0.05 mm on slot radius leaves approximately 1.65 mm in a conservative cut-profile stack. This is a geometric observation, not a new load rating or closure of the separate side-elbow/cage-nut concern.

## Edge finish and flatness

A precisely dimensioned 0.10–0.20 mm edge break is not intrinsically required for the faceplate's coolant seal: it is a dry structural part with clearance around POM seal bosses. **Ordinary deburring is a plausible functional substitute**, provided it leaves usable screw clearances, no raised burrs preventing seating and no hazardous snagging edges. Perfect cosmetic burr removal is a different requirement from usable mating surfaces. JLC's unquantified residual-burr statement cannot itself establish those conditions.

The **0.30 mm faceplate flatness** and **2.00 ±0.10 mm thickness** remain separate requirements. Neither is guaranteed merely by ±0.1 laser-cut dimensions. No broader flatness or thickness acceptance has been calculated or granted here.

## Decision supported by this investigation

There is no evidence that the overall faceplate layout or Ø32 boss windows need redesign. **Relaxing plate position to ±0.1 while retaining Ø4.5 minimum effective clearance passes this positional calculation.** Applying JLC's full default ±0.1 hole-size band to the existing nominal Ø4.5 gives a very small worst-case shortfall. The current geometry is a reasonable prototype candidate if actual fit and ordinary deburring are accepted as first-article checks, but that is a different acceptance basis from guaranteed interchangeability across the full tolerance envelope.

A later decision could keep all CAD geometry and explicitly retain a minimum finished M4 clearance diameter, or use Ø4.6 ±0.1 for modest additional allowance with JLC's default size tolerance. The earlier Ø5.0 example is not necessary merely to accommodate this plate-only ±0.1 scenario. The investigation itself did not authorise those alternatives. Subsequently the operator accepted JLC’s stated limitations with the existing files; neither a minimum-hole condition nor manual rework obligation was added by that acceptance record. Manufacturing files remain intact.
