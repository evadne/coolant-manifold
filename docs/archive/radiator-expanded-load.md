# Expanded radiator equipment load

> **Historical reference — superseded.** This page describes an earlier design or assessment. Its recommendations and “current” labels apply only to that snapshot. Use the [current project guide](../../README.md) and [three-part recap](../three-part-recap.md) for P / R6.


**2 mm remains a viable prototype choice for stationary use with eight secured rack fixings and the load kept reasonably close to the rack plane.** The expanded study uses 15 kg of equipment/coolant payload plus the 1.131 kg plate itself. It predicts approximately 0.207 mm out-of-plane movement and 67.4 MPa peak surface stress at a 150 mm effective rearward centre of gravity. This is a full-plate elastic simulation, not a certified complete-assembly rating.

## Mass budget

| Component | Mass / kg | Basis |
|---|---:|---|
| SuperNova 1260 radiator, dry | 4.225 | Manufacturer net weight; no removed-plate deduction |
| Rack plate, 2 mm 304 | 1.131 | CAD net area and density 7900 kg/m³ |
| Eight NF-A20 PWM fans | 2.960 | 8 × manufacturer 370 g net |
| ULTITUBE D5 200, dry, without pump | 1.000 | Explicit engineering allowance; net mass unverified |
| D5 NEXT pump | 0.500 | Explicit engineering allowance; net mass unverified |
| ULTITUBE contents | 0.494 | 470 ml capacity × assumed coolant density 1.05 kg/l |
| Radiator/local plumbing coolant | 2.000 | Separate provisional allowance; actual fill quantity unverified |
| Additional equipment | 2.000 | Operator's extra allowance, retained in full |
| **Budget total** | **14.310** | Mixture of sourced values and declared allowances |
| **FEA total** | **16.131** | 15 kg payload + plate; 1.821 kg above the budget |

The [Noctua specification](https://www.noctua.at/en/products/nf-a20-pwm/specifications) states 370 g per fan, rather than the 705 g packaged mass. [Aqua Computer's ULTITUBE description](https://shop.aquacomputer.de/Wasserkuehlung/Ausgleichsbehaelter-Zub/Fuer-Pumpenmontage/ULTITUBE-D5-200-Ausgleichsbehaelter-fuer-D5-Pumpen::3844.html) identifies a 200 mm long borosilicate tube, Ø65 outside with 5 mm walls, and 470 ml fill capacity. Its product/manual information inspected for this study did not establish a usable dry net mass for the selected reservoir and D5 NEXT combination; the table deliberately uses allowances rather than retailer packaging weights. These are planning values, not certified upper bounds. Confirm the final assembly is within the analysed payload before relying on the result.

The [Alphacool 14351 datasheet](https://download.alphacool.com/legacy/ENG_1018089_Alphacool_NexXxoS_XT45_Full_Copper_1260mm_SuperNova_Radiator.pdf) gives 4225 g net dry radiator mass. Keeping that full value is conservative with respect to replacing one original fan plate. The extra 2 kg of equipment does **not** pay for the eight fans, pump, reservoir or the separately budgeted coolant. Adapter brackets, fittings and electrical accessories can consume the extra equipment allowance; a larger inventory must be added explicitly.

## Mounting and load application

The operator clarified that the pump/reservoir might attach via its 140 mm fan-hole mounting bracket to Alphacool's existing plate behind the radiator, or be replaced by a different rack-mounted pump/reservoir. This exercise estimates necessary carrying capacity, without selecting or designing that bracket. All payload is conservatively attributed to this radiator plate; a separately rack-supported pump/reservoir would unload it.

The current R1 cut profile is evaluated at 2 mm. Eight secured rack positions are X±232.55, heights 21.275/199.075/243.525/421.325. Payload gravity enters the twelve radiator attachment holes, and its overturning moment is represented by a corresponding force couple. Effective CG distances of 150 and 300 mm are deliberately imposed cases, **not measured CG locations**. The 300 mm case also retains only four outer rack supports and transfers all payload gravity through the upper two radiator attachment holes; its moment couple uses the four outer attachment holes.

The present four-aperture R1 faceplate does not itself contain the NF-A20 fixing pattern. Eight A20 fans require suitable fan plates/adapters on both sides; the mass study does not establish this fit. Any future change to the load-bearing cut profile needs an updated analysis. Do not mount the pump directly to an unanalysed narrow central web and apply these results to that local bracket load.

## CalculiX results

All cases include 15 kg payload and 1.131 kg plate self-weight. Steel is modelled with E200 GPa, Poisson ratio0.3, at room temperature.

| Case | Secured rack fixings | Effective CG behind plate | Maximum normal movement | Recovered peak surface stress |
|---|---:|---:|---:|---:|
| Distributed attachment loading, refined mesh | 8 | 150 mm | 0.2068 mm | 67.4 MPa |
| Upper attachment loading, coarse mesh | 4 | 300 mm | 0.4753 mm | 136.8 MPa |
| Upper attachment loading, refined mesh | 4 | 300 mm | 0.4761 mm | 137.6 MPa |

The refined mesh has 40,374 quadratic S6 shell elements and 82,941 nodes. Refining the second load case changed normal movement by **0.18%** and peak stress by **0.60%**. Force/moment equilibrium checks pass to better than 0.1%. The underlying shell formulation, baseline profile refinement and beam benchmark were established in [the original FEA review](radiator-plate-FEA.md). Complete compressed input decks and DAT outputs are retained in `output/radiator-expanded-load/`, with numeric assessment and an inspected stress/displacement plot.

[Outokumpu's Core datasheet](https://www.outokumpu.com/-/media/files/products/core/outokumpu-core-range-datasheet.pdf) gives 230 MPa minimum 0.2% proof strength for cold-rolled 304 sheet at 20°C. The ratios of that value to the simulated peaks are about **3.41** and **1.67**. These ratios concern the modelled plate stress only; they are not assembly safety factors or lifting/transport ratings.

## Decision

Retain **2 mm** as the radiator plate candidate for the stationary rack, using eight secured rack fixings and a target effective load CG no farther than 150 mm behind the plate. The 16.1 kg analysed total provides useful mass reserve above this 14.3 kg planning budget. Movement around two tenths of a millimetre is small for this mounting function, subject to actual fit requirements.

The deliberately unfavourable four-fixing / 300 mm case still predicts stresses below proof strength, but its reserve is much smaller. Do not turn that case into a general 16 kg handling rating. For such a long cantilever or transport duty, revise the support arrangement, add rear support, or reassess thickness and dynamic loads.

The simulation excludes bolt preload/contact, slot/washer slip, radiator M3 thread/rail pull-out, pump vibration and rack flexibility. It does not credit radiator reinforcement. It checks the plate rather than certifying the bought-in radiator mounting interfaces. R1's released 3 mm CAD remains unchanged pending a distinct 2 mm manufacturing revision.

## Reproduction

Generate with `scripts/radiator_plate_fea.py`:

```sh
.venv/bin/python scripts/radiator_plate_fea.py --size 3 --payload-kg 15 --cg-mm 150 --label expanded
.venv/bin/python scripts/radiator_plate_fea.py --size 6 --payload-kg 15 --cg-mm 300 --supports 4 --load top --label expanded
.venv/bin/python scripts/radiator_plate_fea.py --size 3 --payload-kg 15 --cg-mm 300 --supports 4 --load top --label expanded
```

Run the three `expanded-*.inp` decks with CalculiX2.23 (same Debian runtime as the original study); return corresponding `.dat` files to `output/radiator-expanded-load/`. Run `.venv/bin/python scripts/review_radiator_expanded_load.py`. The old 6.225 kg cases and results are preserved; default generator loads are unchanged.
