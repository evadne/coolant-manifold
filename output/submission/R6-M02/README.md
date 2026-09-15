# R6-M02 radiator plate production pack

Issued 15 September 2026. R6 operator-approved on 15 September 2026. Part **SN1260-R6-M02-PLATE** adds the requested shallow 10 × 2 mm rounded cable notch to the operator-approved, non-tapped R4 radiator plate. R6-M02 supersedes R6-M01 for finish specification only; the approved R6 geometry is unchanged. The manifold package remains separate.

## Upload files

Use `output/submission/R6-M02/SN1260-R6-M02-PLATE.zip` as one part. It contains identically named STEP, DXF and three-sheet A3 PDF files. The STEP is a single finished nominal solid; the DXF is the 1:1 millimetre cut profile. The drawing defines tolerances, edge breaks and finish. Report conflicts before cutting; do not silently substitute nominal model sizes for drawing limits.

Suggested route: JLC's sheet-metal service, stainless steel 304, 2 mm, raw sheet finish, no brushing or polishing. Flat plate with plain through holes; no tapping or countersinks. Round holes may be laser-cut where the specified finished dimensions are met, otherwise drilled/finished. This avoids prescribing an unnecessary separate drilling operation.

JLC's [sheet-metal fabrication guidelines](https://jlccnc.com/help/article/sheet-metal-fabrication-guidelines) require STEP/STP, accept PDF/DXF supplementary drawings and permit ZIP uploads containing STEP; matching file names are recommended. Their listed minima are 1 mm hole spacing and cut diameter at least 1 mm and half the sheet thickness. Published general/cutting/hole tolerances do not automatically establish compliance with this drawing's unilateral hole limits, cable-notch edge finish or free-state flatness. Checked 15 September 2026.

JLC lists 2 mm 304 sheet and an 800 mm maximum length in its [supported sheet-metal materials](https://jlccnc.com/help/article/materials-supported-in-sheet-metal-fabrication). This part's maximum extent is 482.6 mm. These catalogue checks support requesting a quotation, not a confirmed supplier acceptance.

## Drawing coverage

| Group | Quantity | Finished feature |
|---|---:|---|
| A01–A16 | 16 | Ø4.50 +0.15/0 through; plain clearance holes |
| B01–B12 | 12 | Ø3.60 +0.15/0 through; plain clearance holes |
| C01–C40 | 40 | Horizontal 10.00 ±0.15 × 7.00 +0.15/0 through slots |
| D01–D04 | 4 | 188.00 ±0.15 square, R50.00 ±0.15 through apertures |
| E01 | 1 | Top-centre open cable notch: 10.00 ±0.15 mouth × 2.00 ±0.15 depth, R0.5 mouth and bottom transitions |

Sheet 1 identifies every feature and specifies the profile, material, finish and edge treatment. Sheet 2 schedules the fixing and aperture coordinates and details the slot and sheet thickness. Sheet 3 details E01, centred at X0 ±0.10 on the top edge. Its 10 mm mouth includes the two R0.5 entry transitions; the parallel throat is 9 mm and the bottom flat is 8 mm. All four corners are tangent arcs. No sloped ramp is needed. All holes are normal to the broad faces; there is no countersink angle or tapped thread in this plate.

Overall dimensions are 482.60 ±0.15 × 444.50 +0/−0.15 × 2.00 ±0.10 mm. The height retains the accepted nominal 10U geometry. Hole/slot centres are ±0.10 mm from the defined width-centre/bottom-edge origin. Whole-plate free-state flatness is 0.50 mm maximum. Supplier acceptance of these requirements is required before fabrication; do not assume portal defaults override them.

## Manufacturing and inspection review

The smallest round hole is 3.6 mm. Nominal rack-slot end margins are 2.85 mm vertically and 3.75 mm laterally; the nearest adjacent slot gap is 5.70 mm. Central aperture webs are 12 mm. None of these dimensions require a sub-millimetre cut ligament. The thin, broad plate should be inspected without fixture forces masking distortion.

Deburr both faces: fan holes have only a 0.10 mm maximum edge break; other cut edges have a 0.20–0.30 mm break, except E01. At E01, continuously round the cable-contact edges R0.30–0.50 on both faces and blend into the adjacent top edge. Remove burrs, sharp lips and rough cut striations. These small face rounds are specified separately from the R0.5 cut-profile radii. These finishing details are drawing requirements, not extra machined STEP chamfers. Specify raw stainless sheet finish on BOTH broad faces, with no brushing, polishing, product markings or applied coating.

CAD verification confirms one valid solid, 72 openings, all 68 fixing positions and matching circular DXF coordinates. The production STEP is byte-identical to the R6 source. A solid comparison against R4 verifies that the only removed material is the 10 × 2 mm notch envelope (36.000 mm³); there is no added material. Nominal net mass is 1.247 kg using 7,900 kg/m³; finishing is not deducted. The notch removes about 0.284 g at the top centre and leaves the mount patterns and central web intact.

First article: inspect thickness, overall dimensions, all fixing positions, finished hole/slot sizes, aperture profiles, edge treatment and free-state flatness.

Assembly instructions are maintained separately in [the radiator assembly guide](../../../docs/radiator-rack-plate.md).

## Reproduction and records

The shallow notch supersedes the previous 5 mm depth; its floor is Y442.500.

Build geometry first with `scripts/build_radiator_plate.py --revision R6`. Run `scripts/prepare_radiator_production.py` with the CAD environment, with `--issue R6-M02`, then `scripts/draw_radiator_production.py --issue R6-M02` with ReportLab. Render and visually inspect all three PDF pages before running `scripts/package_radiator_production.py --issue R6-M02` with pypdf. The package script checks drawing coverage and ZIP integrity and records SHA-256 hashes. Geometry/source data stay in `output/manufacturing/R6-M02/`; the upload bundle and supplier remarks are in `output/submission/R6-M02/`.

The generation scripts prepare local files only; the separate quotation status below records the authorised supplier submission. Supplier acceptance and payment remain pending.

R6-M02 supersedes R6-M01. Before quotation, the operator amended both steel parts to raw sheet finish with no brushing or polishing. STEP/DXF geometry remains byte-identical to approved R6. See [current three-part JLC review](../../../docs/jlc-final-review.md).

## Quotation status

[Submitted to JLCCNC for review before payment](../../../docs/jlc-quotation-2026-09-15.md), with raw sheet finish. No payment made.
