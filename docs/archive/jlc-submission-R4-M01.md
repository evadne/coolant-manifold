# R4-M01 radiator plate production pack

> **Historical reference — superseded.** This page describes an earlier design or assessment. Its recommendations and “current” labels apply only to that snapshot. Use the [current project guide](../../README.md) and [three-part recap](../three-part-recap.md) for P / R6.


released 15 September 2026. Part **SN1260-R4-M01-PLATE** derives unchanged geometry from the operator-approved, non-tapped R4 radiator plate. It supersedes the R3/R4 comparison drawing for fabrication of this part. The manifold package remains separate.

## Upload files

Use `output/submission/R4-M01/SN1260-R4-M01-PLATE.zip` as one part. It contains identically named STEP, DXF and two-sheet A3 PDF files. The STEP is a single finished nominal solid; the DXF is the 1:1 millimetre cut profile. The drawing defines tolerances, edge breaks and finish. Report conflicts before cutting; do not silently substitute nominal model sizes for drawing limits.

Suggested route: JLC's sheet-metal service, stainless steel 304, 2 mm, brushed finish. No bends, tapping, countersinking, welding, inserted hardware or supplier assembly. Round holes may be laser-cut where the specified finished dimensions are met, otherwise drilled/finished. This avoids prescribing an unnecessary separate drilling operation.

JLC's [sheet-metal fabrication guidelines](https://jlccnc.com/help/article/sheet-metal-fabrication-guidelines) require STEP/STP, accept PDF/DXF supplementary drawings and permit ZIP uploads containing STEP; matching file names are recommended. Their listed minima are 1 mm hole spacing and cut diameter at least 1 mm and half the sheet thickness. Published general/cutting/hole tolerances do not automatically establish compliance with this drawing's unilateral hole limits or free-state flatness. Checked 15 September 2026.

JLC lists 2 mm 304 sheet and an 800 mm maximum length in its [supported sheet-metal materials](https://jlccnc.com/help/article/materials-supported-in-sheet-metal-fabrication). This part's maximum extent is 482.6 mm. These catalogue checks support requesting a quotation, not a confirmed supplier acceptance.

## Drawing coverage

| Group | Quantity | Finished feature |
|---|---:|---|
| A01–A16 | 16 | Ø4.50 +0.15/0 through; M4 fan screws with separate nuts |
| B01–B12 | 12 | Ø3.60 +0.15/0 through; M3 screws into the radiator frame |
| C01–C40 | 40 | Horizontal 10.00 ±0.15 × 7.00 +0.15/0 through slots |
| D01–D04 | 4 | 188.00 ±0.15 square, R50.00 ±0.15 through apertures |

Sheet 1 identifies every feature and specifies the profile, material, finish and edge treatment. Sheet 2 schedules every centre coordinate and details the slot and sheet thickness. All holes are normal to the broad faces; there is no countersink angle or tapped thread in this plate. M3 threads belong to the bought-in radiator only.

Overall dimensions are 482.60 ±0.15 × 444.50 +0/−0.15 × 2.00 ±0.10 mm. The height retains the accepted nominal 10U geometry. Hole/slot centres are ±0.10 mm from the defined width-centre/bottom-edge origin. Whole-plate free-state flatness is 0.50 mm maximum. Supplier acceptance of these requirements is required before fabrication; do not assume portal defaults override them.

## Manufacturing and inspection review

The smallest round hole is 3.6 mm. Nominal rack-slot end margins are 2.85 mm vertically and 3.75 mm laterally; the nearest adjacent slot gap is 5.70 mm. Central aperture webs are 12 mm. None of these dimensions require a sub-millimetre cut ligament. The thin, broad plate should be inspected without fixture forces masking distortion.

Deburr both faces: fan holes have only a 0.10 mm maximum edge break; other cut edges have a 0.20–0.30 mm break. These finishing details are drawing requirements, not extra machined STEP chamfers. Specify uniform satin brushing with no product markings or applied coating. Do not infer electrical isolation from the finish.

CAD verification confirms one valid solid, 72 openings, all 68 fixing positions and matching circular DXF coordinates. The production STEP is byte-identical to accepted R4. Nominal net mass is 1.248 kg using 7,900 kg/m³; finishing is not deducted. Existing R4 structural estimates remain applicable to unchanged geometry but are not a tested assembly load rating.

First article: inspect thickness, overall dimensions, all fixing positions, finished hole/slot sizes, aperture profiles, edge treatment and free-state flatness. Trial-fit the actual radiator and fans before further production; M3 engagement and real hardware clearances remain assembly checks outside this plate-only supplier order.

## Assembly retained from R4

1. Fit fans to the plate. M4 ×40 button heads and washers are on the radiator/core side; nuts and washers are outside the fan faces.
2. Fix the populated plate to the radiator through the twelve M3 clearance holes.
3. Mount the assembly to the rack using the chosen optional rack positions.

Use the existing R4 assembly notes for hardware details. If using the X-Splitter, retain/insulate it with suitable nonconductive double-sided tape. No additional holes are required.

## Reproduction and records

Run `scripts/prepare_radiator_production.py` with the CAD environment, then `scripts/draw_radiator_production.py` with ReportLab. Render and visually inspect both PDF pages before running `scripts/package_radiator_production.py` with pypdf. The package script checks drawing coverage and ZIP integrity and records SHA-256 hashes. Geometry/source data stay in `output/manufacturing/R4-M01/`; the upload bundle and supplier remarks are in `output/submission/R4-M01/`.

This revision prepares the files only. No supplier upload, quotation acceptance or order has been made.
