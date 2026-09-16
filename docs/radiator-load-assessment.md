# Current radiator load budget and analysis basis

**Engineering assessment, not a part manufacturing instruction.** Fabrication is defined only by the matching current STEP/PDF and supplier remarks.

The current R7 plate is 2 mm 304 stainless. The existing full-plate analysis supports this prototype choice under its stated static loads and supports. Its final pre-notch calculation uses the R4 profile and direct fan loads; it is not a newly solved R7 or complete-assembly load rating.

## Updated planning mass

| Component | Mass, kg | Basis |
|---|---:|---|
| SuperNova 1260 dry radiator | 4.225 | Manufacturer net mass; no deduction for the replaced stock plate |
| R7 custom plate | 1.247 | [Current CAD verification](../output/manufacturing/R7-M01/geometry-verification.json), density 7,900 kg/m³ |
| Eight NF-A20 fans | 2.960 | Eight ×370 g manufacturer net mass |
| ULTITUBE D5 200, dry, without pump | 1.000 | Engineering allowance; dry net mass unverified |
| D5 NEXT | 0.500 | Engineering allowance; dry net mass unverified |
| Reservoir coolant | 0.494 | 470 ml × assumed 1.05 kg/l |
| Radiator/local plumbing coolant | 2.000 | Provisional allowance; actual fill unverified |
| Additional equipment | 2.000 | Operator allowance, retained in full |
| **Planning total** | **14.426** | Includes current plate; mixed sourced masses and allowances |

Payload excluding the custom plate is approximately 13.179 kg. The retained analysis uses **15 kg payload plus plate self-weight**, providing approximately 1.821 kg mass reserve over this planning budget. Actual pump/reservoir inventory and centre of gravity remain to be confirmed. The earlier 14.310 kg total used an older, lighter cut profile and is superseded for present planning.

The operator's suggested pump/reservoir bracket can use 140 mm fan holes on Alphacool's opposite plate behind the radiator, or the pump/reservoir can have separate rack support. The mass assessment conservatively attributes it all to the radiator mount; it does not select or qualify that bracket.

## Retained R4 structural evidence

The [R4 assessment](../output/radiator-R4/analysis/assessment.json) models the same 2 mm R50-aperture/fan-hole layout before the small R6 edge notch. Four front fans (1.48 kg) load the sixteen fan fixings at 18 mm forwards; the remaining 13.52 kg enters through the twelve M3 attachments. The complete payload retains a 150 mm effective rearward centre of gravity. R4 plate self-weight is approximately 1.24764 kg. R6 removes 36 mm³, about 0.284 g, at the top notch and retains the fixing/air-aperture geometry.

| Secured rack fixings | Maximum out-of-plane movement | Peak recovered surface stress |
|---|---:|---:|
| 40 | 0.1020 mm | 34.77 MPa |
| 8 | 0.2165 mm | 76.73 MPa |

Empty optional slots provide no support. These cases do not require all forty screws or guarantee arbitrary two-/four-screw installations. Refinement from 6 to 3 mm changed displacement by 0.16% and peak recovered stress by 0.98%; force/moment balance checks passed. The refined model has 82,196 S6 elements.

The calculation uses small-displacement linear elastic steel at room temperature, E200 GPa and Poisson ratio0.3. It excludes joint slip/contact, bolt preload, cage nuts, actual radiator M3 frame pull-out, fan pads, pump vibration, transport shocks, rack flexibility and a complete assembly rating. The manifold needs its own load/creep assessment; radiator results do not transfer to it.

## Evidence and reproduction

- [R4 model, hardware and original analysis narrative](archive/radiator-fan-plates-R3-R4.md); native compressed solver decks/results and plots under `output/radiator-R4/analysis/`.
- [Earlier full-plate method and beam benchmark](archive/radiator-plate-FEA.md), superseding the initial local-strip estimate.
- [Earlier expanded-load scenarios and sourced mass basis](archive/radiator-expanded-load.md), including the deliberately less favourable 300 mm offset case on the historical R1 profile.
- Reproduce R4 cases with `scripts/radiator_plate_fea.py --revision R4 --payload-kg 15 --cg-mm 150`, CalculiX and `scripts/review_radiator_R4.py`, following the archived numerical procedure. Do not relabel these as R6 results.

No new solver run is implied by this documentation update. The original source reviews are dated 15 September 2026; allowances remain allowances.

## R7 outside corners

R7 increases only the four outer outline corners from R2 to R5. It removes 36.053 mm³ (0.285 g) from R6; the current plate mass is 1.247067 kg. All fixing positions, airflow apertures and central webs are unchanged. The approximately 14.426 kg planning load remains unchanged at its quoted precision. The R4 FEA remains historical baseline evidence; no new R7 solver run, joint qualification or load rating is claimed.
