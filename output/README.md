# Output directory guide

Current custom parts: Q-M04 manifold body, Q-M03 faceplate and R7/R7-M01 radiator; both steel plates have four R5 outside corners and ±0.10 cut tolerances. Held for repeat orders.

| Location | Purpose |
|---|---|
| `submission/current-three-parts/` | Current three-part ZIP index and final consistency manifest |
| `submission/Q-M04/`, `submission/Q-M03/` | Body/faceplate supplier STEP/PDF ZIPs; DXF for steel; checks and remarks |
| `submission/R7-M01/` | Radiator STEP/PDF/DXF ZIP; checks and remarks |
| `manufacturing/Q-M04/`, `manufacturing/Q-M03/`, `manufacturing/R7-M01/` | Derived single-part solids and verified feature schedules |
| `pdf/RM10-Q-M04-BODY.pdf`, `pdf/RM10-Q-M03-FACEPLATE.pdf`, `pdf/SN1260-R7-M01-PLATE.pdf` | Current technical fabrication drawings |
| `assembly/Q/` | Separate reference assembly and selected M4×10 screw; not supplier part uploads |
| `long-bore-Q/cad/` | Original Q-M01 body and baseline geometry/checks; original faceplate/assembly retained as source history. Current plate is manufacturing/Q-M03; current assembly is assembly/Q |
| `long-bore-Q/product-views/` | Current twelve review angles and unmarked/transparent Blender scenes |
| `long-bore-Q/photorealistic/` | Four refreshed studio images, bare/connected Blender scenes |
| `long-bore-P/koolance-fit/` | Shared retained official fitting meshes and provenance |
| `radiator-R7/` | Current radiator CAD, checks and seven refreshed plate/populated assembly/notch/R5 views |
| `context-25U/` | Current Q/R7 StarTech composite, nine views and fit/tubing checks |
| `analysis/Q-retention.json`, `analysis/Q-torque.json` | Explicit preliminary assumptions and numerical sensitivity; not qualified ratings |

Earlier P/O and R6-M01 manufacturer/review files are historical; do not submit them as Q-M01/R7-M01. Older `long-bore-*`, `radiator-R1` throughR6, generic24U scenes and unversioned G outputs retain their original history. The R4 FEA remains baseline evidence, not a new R7/Q solver result. [Project guide](../README.md) · [manufacturing](../docs/manufacturing.md) · [assembly](../docs/assembly-Q.md).
