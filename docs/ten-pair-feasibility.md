# Ten front pairs in a 400–420 mm body

Ten total front-facing pairs are geometrically plausible within this width range, using 40 mm horizontal pitch and the existing 40 mm vertical pitch. The outer front port centres are X = ±180 mm. This is a feasibility study, not a new manufactured-body revision; I and J remain unchanged.

The corner rack nuts do not create a continuous obstruction along either side of the manifold. A side fitting can share a nut's lateral position while occupying different height and depth ranges. It does not need to be aligned directly behind a nut. The rack's continuous flange and folded return must be checked independently of the four local nuts.

## Envelope comparison

| POM width | Front pairs | Centre-to-end margin | Width across fitted elbows/compression | Beyond nominal 450 mm opening, each side |
|---|---:|---:|---:|---:|
| 400 mm | 10 | 20 mm | 457.6 mm | 3.8 mm |
| 410 mm | 10 | 25 mm | 467.6 mm | 8.8 mm |
| 420 mm | 10 | 30 mm | 477.6 mm | 13.8 mm |

At 40 mm pitch, the existing Ø23.7 pull-ring reference leaves 16.3 mm nominal edge-to-edge clearance horizontally and vertically. This matches the existing vertical spacing; physical release-ring and finger access still need assessment. Keeping the old 45 mm horizontal pitch would require 405 mm between the outer port centres alone, plus the boss radii and edge margins, and therefore cannot support ten pairs within 400–420 mm.

410 mm is a useful next candidate: ten pairs, 25 mm from each outer front port centre to the body end, and 10 mm beyond its Ø28 boss plus R1 root envelope. Proposed M4 mounts at X = −160, 0, +160 and Z = 7, 80 provide six attachment locations. Their countersink edges clear the Ø32 plate windows by 5.93 mm, and their head edges clear the Ø36 fitting keep-outs by 3.95 mm. These are layout clearances, not a fastener-load calculation.

## Check against the rendered rack

The study reuses the exact four elbow/compression solids from Revision I's envelope STEP, translates them to each proposed body width, and checks minimum 3D distances against the illustrative rack's flange, folded return and four nut bodies. Coordinates here use X across the rack, Y rearwards and Z upwards; the physical height/depth distinction is what matters.

| POM width | Minimum fitting-to-front-flange distance | Minimum fitting-to-folded-return distance | Minimum fitting-to-corner-nut distance |
|---|---:|---:|---:|
| 400 mm | 14.0 mm | 28.2 mm | 9.02 mm |
| 410 mm | 14.0 mm | 23.2 mm | 8.99 mm |
| 420 mm | 14.0 mm | 18.2 mm | 8.99 mm |

All three avoid collision with those simplified rack parts. The rail flange is represented conservatively as solid here, without relying on its square holes. Its thickness occupies Y = 0–3 mm; the elbows begin at Y = 17 mm. The nut bodies occupy Y = 3–9 mm. Their centres are at Z = 5.4 and 81.6 mm, whereas side port centres are at Z = 23.5 and 63.5 mm: the nearest centre-height difference is 18.1 mm. The calculations account for the complete 3D solids rather than treating the 450 mm opening as a continuous keep-out volume at every depth.

This supports using space beyond that opening in the installed state. It does not establish an insertion path with the elbows attached. Installing the body with side plugs and adding elbows afterwards is a possible assembly sequence to evaluate; access for fitting, rotation and tightening remains necessary.

An actual rack's folds, inward returns, cage clips, screw protrusions and adjacent equipment can differ from the illustrative frame. The current fitting shapes also remain drawing-derived envelopes. Exact hardware and rack measurements are required before turning this study into a fit claim. Hydraulic and structural performance have not been evaluated here.

[Computed comparison](../output/ten-pair-feasibility/comparison.json) · [Evaluation script](../scripts/evaluate_ten_pair_layout.py)

Run with `.venv/bin/python scripts/evaluate_ten_pair_layout.py`.
