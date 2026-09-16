# R7-M01 radiator plate production pack

Issued 16 September 2026. **SN1260-R7-M01-PLATE** supersedes R6-M03 with four external outline corners increased from R2 to **R5.00 ±0.10 mm**. All fixing holes, slots, R50 airflow apertures and the rounded 10 × 2 mm cable notch remain in their accepted positions. Cut sizes and coordinates retain ±0.10 mm. The manifold package remains separate.

## Upload files

Use `output/submission/R7-M01/SN1260-R7-M01-PLATE.zip` as one part. It contains identically named STEP, DXF and three-sheet A3 PDF files. The STEP is a single finished nominal solid; the DXF is the 1:1 millimetre cut profile. The drawing defines tolerances, edge breaks and finish. Report conflicts before cutting; do not silently substitute nominal model sizes for drawing limits.

Suggested route: JLC's sheet-metal service, stainless steel 304, 2 mm, raw sheet finish, no brushing or polishing. Flat plate with plain through holes; no tapping or countersinks. Round holes may be laser-cut where the specified finished dimensions are met, otherwise drilled/finished. This avoids prescribing an unnecessary separate drilling operation.

JLC's [sheet-metal fabrication guidelines](https://jlccnc.com/help/article/sheet-metal-fabrication-guidelines) require STEP/STP, accept PDF/DXF supplementary drawings and permit ZIP uploads containing STEP; matching file names are recommended. Their listed minima are 1 mm hole spacing and cut diameter at least 1 mm and half the sheet thickness. Published general/cutting/hole tolerances do not automatically establish compliance with this drawing's hole limits, cable-notch edge finish or free-state flatness. Checked 15 September 2026.

JLC lists 2 mm 304 sheet and an 800 mm maximum length in its [supported sheet-metal materials](https://jlccnc.com/help/article/materials-supported-in-sheet-metal-fabrication). This part's maximum extent is 482.6 mm. These catalogue checks support requesting a quotation, not a confirmed supplier acceptance.

## Drawing coverage

| Group | Quantity | Finished feature |
|---|---:|---|
| Outside corners | 4 | R5.00 ±0.10 in the cut profile |
| A01–A16 | 16 | Ø4.50 ±0.10 through; plain clearance holes |
| B01–B12 | 12 | Ø3.60 ±0.10 through; plain clearance holes |
| C01–C40 | 40 | Horizontal 10.00 ±0.10 × 7.00 ±0.10 through slots |
| D01–D04 | 4 | 188.00 ±0.10 square, R50.00 ±0.10 through apertures |
| E01 | 1 | Top-centre open cable notch: 10.00 ±0.10 mouth × 2.00 ±0.10 depth, R0.5 mouth and bottom transitions |

Sheet 1 identifies every feature and specifies the profile, material, finish and edge treatment. Sheet 2 schedules the fixing and aperture coordinates and details the slot and sheet thickness. Sheet 3 details E01, centred at X0 ±0.10 on the top edge. Its 10 mm mouth includes the two R0.5 entry transitions; the parallel throat is 9 mm and the bottom flat is 8 mm. All four corners are tangent arcs. No sloped ramp is needed. All holes are normal to the broad faces; there is no countersink angle or tapped thread in this plate.

Overall dimensions are 482.60 ±0.10 × 444.50 ±0.10 × 2.00 ±0.10 mm. The height retains the accepted nominal 10U geometry. Hole/slot centres are ±0.10 mm from the defined width-centre/bottom-edge origin. Whole-plate free-state flatness is 0.50 mm maximum. Supplier acceptance of these requirements is required before fabrication; do not assume portal defaults override them.

## Manufacturing and inspection review

The smallest round hole is 3.6 mm. Nominal rack-slot end margins are 2.85 mm vertically and 3.75 mm laterally; the nearest adjacent slot gap is 5.70 mm. Central aperture webs are 12 mm. None of these dimensions require a sub-millimetre cut ligament. The thin, broad plate should be inspected without fixture forces masking distortion.

Deburr both faces: fan holes have only a 0.10 mm maximum edge break; other cut edges have a 0.20–0.30 mm break, except E01. At E01, continuously round the cable-contact edges R0.30–0.50 on both faces and blend into the adjacent top edge. Remove burrs, sharp lips and rough cut striations. These small face rounds are specified separately from the R0.5 cut-profile radii. These finishing details are drawing requirements, not extra machined STEP chamfers. Specify raw stainless sheet finish on BOTH broad faces, with no brushing, polishing, product markings or applied coating.

CAD verification confirms one valid solid, 72 openings, all 68 fixing positions and matching circular DXF coordinates. The production STEP and DXF match the R7 source. Compared with R6, only 36.053 mm³ is removed at the four external corners; no material is added. Nominal net mass is **1.247067 kg** using 7,900 kg/m³. The 0.285 g reduction leaves all fixing patterns, central webs and the cable notch intact.

First article: inspect thickness, overall dimensions, all fixing positions, finished hole/slot sizes, aperture profiles, edge treatment and free-state flatness.

Assembly instructions are maintained separately in [the radiator assembly guide](radiator-rack-plate.md).

## Reproduction and records

The shallow notch supersedes the previous 5 mm depth; its floor is Y442.500.

Build geometry first with `scripts/build_radiator_plate.py --revision R7`. Run `scripts/prepare_radiator_production.py` with the CAD environment, with `--issue R7-M01`, then `scripts/draw_radiator_production.py --issue R7-M01` with ReportLab. Render and visually inspect all three PDF pages before running `scripts/package_radiator_production.py --issue R7-M01` with pypdf. The package script checks drawing coverage and ZIP integrity and records SHA-256 hashes. Geometry/source data stay in `output/manufacturing/R7-M01/`; the upload bundle and supplier remarks are in `output/submission/R7-M01/`.

The generation scripts prepare local files only; the separate quotation status below records the authorised supplier submission. This revised package is selected for a separate new order; it does not replace files on the original order.

R7-M01 supersedes the held R6-M03 issue. Both steel parts retain raw sheet finish with no brushing or polishing. STEP/DXF contain the new R5 outside corners; all other geometry is retained. See [current three-part JLC review](jlc-final-review.md).

## Quotation status

The operator accepted the complete Q-M04/Q-M03/R7-M01 set on 16 September 2026 and authorised a **separate new JLC order**, superseding the earlier hold. Submitted for file review on 16 September after explicit confirmation of UPS shipping at US$71.99. Prior material, finish and goods metadata were reused. No payment was made. Preserve the original orders and archives. [New-order submission record](jlc-order-2026-09-16.md). Assembly instructions remain outside the fabrication ZIP.
