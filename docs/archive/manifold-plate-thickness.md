# Can the manifold faceplate also use 2 mm steel?

> **Historical reference — superseded.** This page describes an earlier design or assessment. Its recommendations and “current” labels apply only to that snapshot. Use the [current project guide](../../README.md) and [three-part recap](../three-part-recap.md) for P / R6.


**It is a possible redesign candidate, but the radiator calculation does not establish that the current manifold can simply change to 2 mm.** The manifold's six countersunk M4 retainers make this a different interface from the radiator's plain M3 holes. This check establishes mass and dimensional consequences, not a new structural qualification. Preserve O-M02's 3 mm supplier files.

## Countersink geometry

The released holes are Ø4.5 +0.10/0, countersunk Ø8 +0.10/0 at 90° ±1°. For a nominal 90° countersink, depth = (8 -4.5)/2 =1.75 mm.

| Sheet | Calculated plate mass | Weight saving | Nominal straight land below countersink | Minimum land before edge breaking, stated tolerance stack |
|---|---:|---:|---:|---:|
| 3.0 mm | 0.593 kg | - | 1.25 mm | 1.068 mm |
| 2.5 mm | 0.494 kg | 0.099 kg | 0.75 mm | 0.568 mm |
| 2.0 mm | 0.395 kg | 0.198 kg | 0.25 mm | 0.068 mm |

The stack uses sheet thickness at nominal minus 0.10 mm, countersink mouth 8.10 mm, through-hole 4.50 mm and included angle 89°. The deepest countersink is 1.8317 mm. On 1.90 mm actual sheet that leaves 0.0683 mm before the current general 0.10-0.20 mm edge-breaking operation. A 2 mm revision therefore needs an explicit back-edge treatment at these six holes instead of silently carrying across the general note.

Do not interpret the 0.25 mm nominal land as the full remaining bearing thickness, or as proof of failure. The conical seat still exists and its nominal bearing surface is not reduced merely by removing material behind it. Equally, a nominally fitting cone is not a pull-through or preload calculation.

The [specified Westfield M4 hex socket head](https://www.westfieldfasteners.co.uk/A4-ScrewBolt-SHCsk-M4.html) has maximum diameter 7.96 mm and maximum total head height 2.48 mm. Total head height is not the same as the countersink depth down to a Ø4.5 clearance bore: the lower neck can extend into that clearance/entry. Do not reject 2 mm solely because 2.48 exceeds 2. Check the actual head/neck against the POM entry as part of any revised interface. The [DIN 965 Z Pozi alternative](https://www.westfieldfasteners.co.uk/A4-ScrewBolt-PoziCsk-M4.html) remains part of that fit check.

## Assembly and structural consequences

- Existing 4 mm POM bosses would project 2 mm above a 2 mm plate. To preserve the operator's faceplate-plus-1-mm relationship, shorten bosses to 3 mm in a new body revision and update G1/4 entry/sealing-plane dimensions together. Extra boss projection alone does not prevent the fitting from seating on POM.
- M4 ×12 screws would reach nominally 10 mm from the POM face instead of 9 mm, before head recess/tolerance. The existing 14 mm pilot provides nominal tip space, so automatically shortening the screws is not necessary; actual engagement and alternative-head seating still need checking.
- The manifold face is 87 mm high, with twenty Ø32 windows, 7.5 mm top/bottom ligaments beside the windows and 8 mm webs between adjacent windows. Its screw/support pattern differs substantially from the radiator.
- Coupling insertion, release, tube pull and fitting torque act through the POM body. The 40 mm slab can stiffen the assembly, but its discrete screw attachment, contact with the faceplate and POM creep need appropriate treatment in a manifold model. Neither the radiator's load sharing nor its calculated 0.043 mm displacement transfers to this assembly.

## Recommendation

For an unchanged fastener family and a modest weight reduction, **2.5 mm is the less disruptive candidate**: it saves about 99 g and retains substantially more countersink manufacturing allowance. **2 mm remains feasible to investigate**, saving 198 g, but requires a deliberate countersink/back-edge specification and a separate manifold load assessment. The operator previously allowed slight head proudness outside port keep-outs; a shallower countersink is therefore an available design route if that trade-off is selected, subject to checking both head variants and their tolerances. No new countersink diameter or head proudness has been specified here.

This is not a finding that 2 mm stainless lacks static strength. It is a finding that the radiator result alone is insufficient and that the current countersink detail has little process allowance at 2 mm. O-M02 remains unchanged. Reproduce with `scripts/assess_manifold_plate_thickness.py`; results are in `output/manifold-plate-thickness/assessment.json`.
