# Output directory guide

Current custom parts: accepted Q manifold, supplier issue Q-M01; accepted R6 radiator plate, finish issue R6-M02.

| Location | Purpose |
|---|---|
| `submission/current-three-parts/` | Current three-part ZIP index and final consistency manifest |
| `submission/Q-M01/` | Body/faceplate supplier STEP/PDF ZIPs; DXF for steel; checks and remarks |
| `submission/R6-M02/` | Radiator STEP/PDF/DXF ZIP; checks and remarks |
| `manufacturing/Q-M01/`, `manufacturing/R6-M02/` | Derived single-part solids and verified feature schedules |
| `pdf/RM10-Q-M01-*.pdf`, `pdf/SN1260-R6-M02-PLATE.pdf` | Current technical fabrication drawings |
| `assembly/Q/` | Separate reference assembly and selected M4×10 screw; not supplier part uploads |
| `long-bore-Q/cad/` | Current Q geometry, two wet networks and checks |
| `long-bore-Q/product-views/` | Current ten review angles and unmarked/transparent Blender scenes |
| `long-bore-Q/photorealistic/` | Four refreshed studio images, bare/connected Blender scenes |
| `long-bore-P/koolance-fit/` | Shared retained official fitting meshes and provenance |
| `radiator-R6/` | Current radiator CAD, checks and refreshed brushed plate/notch views |
| `context-25U/` | Current Q/R6 StarTech composite, nine views and fit/tubing checks |
| `analysis/Q-retention.json`, `analysis/Q-torque.json` | Explicit preliminary assumptions and numerical sensitivity; not qualified ratings |

Earlier P/O and R6-M01 manufacturer/review files are historical; do not submit them as Q-M01/R6-M02. Older `long-bore-*`, `radiator-R1` throughR5, generic24U scenes and unversioned G outputs retain their original history. The R4 FEA remains baseline evidence, not a new R6/Q solver result. [Project guide](../README.md) · [manufacturing](../docs/manufacturing.md) · [assembly](../docs/assembly-Q.md).
