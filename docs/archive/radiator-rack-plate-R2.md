# R2 radiator bracket: 10U and forty fixing positions

> **Historical reference — superseded.** This page describes an earlier design or assessment. Its recommendations and “current” labels apply only to that snapshot. Use the [current project guide](../../README.md) and [three-part recap](../three-part-recap.md) for P / R6.


R2 changes the **radiator bracket only**. The completed manifold faceplate P remains unchanged. R1 and the earlier load studies are preserved.

The new plate is **482.6 × 444.5 × 2 mm** in 304 stainless steel: exactly ten nominal rack units high. It has **four rack fixing positions per U**, interpreted as two on each rail, giving forty 10 × 7 mm slots in total. Slot centres are X±232.55 and Y = 44.45n +6.35/+38.10 for n0–9. These are the first and third rail-hole positions within each unit; the middle position is unused.

The four airflow openings, 12 mm cross webs and twelve M3 radiator attachment holes retain their sizes and positions relative to the radiator centre. Moving the centre from Y221.30 to **Y222.25** recentres the radiator in the taller panel. CAD, DXF, drawing and FEA all use those revised coordinates. The radiator body's 441 mm height leaves 1.75 mm nominal at either end, excluding fittings and hoses.

## Edge and fit review

- Overall height **444.50 +0/−0.15 mm** in the drawing. A nominally exact 10U panel has no panel-to-panel gap if adjacent panels also consume their entire unit allocation; actual tolerance and installation fit still matter.
- Extreme slot centres are 6.35 mm from the top/bottom. With 7 mm slot height, the steel edge ligament is **2.85 mm**. Side edge ligament remains **3.75 mm**.
- Use suitable head/washer envelopes at the extreme rows: **Ø12 mm maximum** gives 0.35 mm nominal top/bottom reserve before tolerances; a Ø15 washer would overhang by 1.15 mm. This is a geometric envelope, not a fastener load rating. The closest pair of slot centres is 12.7 mm apart, leaving 0.7 mm between nominal Ø12 washers.
- All slots are plain through cuts. Rack screws and cage nuts must match the actual rack. The radiator attachment interface remains M3 and is independent of manifold M4 hardware.
- Moving from R1's 3 mm sheet to 2 mm increases the reach of an unchanged radiator screw by 1 mm. Select screw/washer thickness against actual OEM engagement and safe depth. No tightening torque or rail-thread rating has been established.

CAD-derived plate mass is **1.1195 kg**. The additional slot cut-outs more than offset the 1.9 mm increase in height; this is approximately 12 g lighter than the previous cut profile evaluated at 2 mm.

## Full-plate comparison

The [expanded equipment budget](radiator-expanded-load.md) includes the radiator, eight A20 fans, filled ULTITUBE, D5 NEXT and 2 kg additional equipment, with unverified masses labelled as allowances. Substituting the R2 plate mass makes that planning budget **14.298 kg**. The FEA again uses **15 kg payload plus plate self-weight =16.120 kg total**, retaining 1.8215 kg reserve over the planning budget.

Both installation comparisons use this same R2 plate geometry and the same 150 mm effective rearward CG. The eight-fixing case secures X±232.55 at Y6.35/184.15/260.35/438.15. The forty-fixing case secures every available position. Payload gravity and overturning couple enter through the radiator attachment holes. Forty positions are available by design; this does not require every builder to install forty screws, but the forty-support result requires all forty to be effective supports.

| Installation / load case | Normal movement | Recovered surface stress |
|---|---:|---:|
| 8 secured positions; 150 mm CG; distributed attachment load | 0.2560 mm | 79.5 MPa |
| 40 secured positions; 150 mm CG; distributed attachment load | **0.1423 mm** | **35.5 MPa** |
| 40 secured positions; 300 mm CG; gravity through upper two radiator mounts | 0.3488 mm | 88.5 MPa |

Securing all forty positions produces **44.4% less movement** and **55.3% less peak stress** than the eight-fixing installation on this same plate. The eight-point coordinates differ from the old R1 study, so the comparison above controls both geometry and loading rather than directly attributing a cross-revision change to thickness or height.

The refined models contain 58,840 S6 quadratic shell elements and 120,687 nodes. Refining the forty-fixing /150 mm case from a 6 mm to 3 mm target mesh changed displacement by **0.14%** and peak stress by **0.021%**. Force and moment balance checks pass to better than 0.1%. The previous beam benchmark and full profile checks remain applicable to the solver formulation. Steel E200 GPa and Poisson ratio0.3 are unchanged.

Relative to the [Outokumpu cold-rolled 304 proof strength of 230 MPa at 20°C](https://www.outokumpu.com/-/media/files/products/core/outokumpu-core-range-datasheet.pdf), the nominal forty-fixing case has a proof/peak-stress ratio around **6.47**; the 300 mm case about **2.60**. These are plate-model comparisons, not rated assembly safety factors.

**The results support retaining 2 mm for this prototype radiator bracket.** Additional installed fixings reduce plate bending substantially. Do not infer equivalent improvement from unpopulated holes or that forty screws are necessary for a satisfactory stationary installation. Further subsets can be compared if a lower assembly screw count is preferred.

The model fixes translations around secured slot edges; it does not model actual washer contact/preload, loose bolts, cage-nut/rail flexibility, radiator M3 pull-out, vibration, impact or transport. It takes no credit for radiator reinforcement. The 300 mm offset is a sensitivity case, not a measured CG or a handling rating. Eight A20 fan mounts and the optional pump bracket remain separate packaging/interface work; these new rack holes do not solve fan attachment geometry.

## Outputs and reproduction

- Source parameters: `cad/radiator/R2.json`.
- STEP, DXF, STL and geometry verification: `output/radiator-R2/`.
- One-sheet dimensional review: `output/pdf/radiator-rack-plate-R2.pdf`.
- Bare/front/rear Blender review views and editable scene: `output/radiator-R2/`. They illustrate the bracket and radiator, not the full eight-fan/pump inventory.
- Numeric FEA summary, inspected comparison plot, and compressed native inputs/results: `output/radiator-R2/analysis/`.

Build with `build_radiator_plate.py --revision R2`; draw with `draw_radiator_R2.py` using the PDF runtime; render with Blender `render_radiator_plate.py -- --revision R2`.

Generate FEA decks:

```sh
.venv/bin/python scripts/radiator_plate_fea.py --revision R2 --supports 40 --size 3 --payload-kg 15 --cg-mm 150 --label R2
.venv/bin/python scripts/radiator_plate_fea.py --revision R2 --supports 8 --size 3 --payload-kg 15 --cg-mm 150 --label R2
.venv/bin/python scripts/radiator_plate_fea.py --revision R2 --supports 40 --size 3 --payload-kg 15 --cg-mm 300 --load top --label R2
.venv/bin/python scripts/radiator_plate_fea.py --revision R2 --supports 40 --size 6 --payload-kg 15 --cg-mm 150 --label R2
```

Solve with CalculiX2.23, return DAT files to `output/radiator-R2/analysis/`, then run `review_radiator_R2.py`. The solver/runtime is unchanged from the earlier study. No supplier upload or order has been made.
