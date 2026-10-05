# Output directory guide

Current custom parts: Q-M04 manifold body, Q-M03 faceplate and R7/R7-M01 radiator; both steel plates have four R5 outside corners and ±0.10 cut tolerances. These are the delivered first-article issues. Start with [the repeat-order guide](../docs/order-from-jlc.md) or [machine-readable selection](../cad/current-release.json).

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

Earlier P/O, Q-M01 and R6 manufacturer/review files are historical; do not submit them as the current Q-M04/Q-M03/R7-M01 set. Older `long-bore-*`, `radiator-R1` throughR6, generic24U scenes and unversioned G outputs retain their original history. The R4 FEA remains baseline evidence, not a new R7/Q solver result. [Project guide](../README.md) · [manufacturing](../docs/manufacturing.md) · [assembly](../docs/assembly-Q.md).

## Authority and dependencies

Only the three ZIPs selected by `cad/current-release.json` are canonical fabrication uploads. The current index contains byte-identical copies of the issue-specific archives. PDFs plus STEP/DXF define fabrication; STL and Blender files are display/assembly aids. The original files are retained in place rather than renamed, because historical scripts and current reference scenes still depend on some of them.

A directory labelled `long-bore-Q` is not enough to choose a supplier file: its `cad/` subdirectory retains baseline Q-M01 solids, while current presentation scripts load the finished Q-M04/Q-M03 parts explicitly. `long-bore-P/koolance-fit/` is a shared current reference dependency despite its older revision name. The [revision register](../docs/iterations.md) describes the progression.

No Git LFS migration or historical asset removal has been performed. Large scenes and solver outputs are intentionally retained. Use [the publication review](../docs/publication-review.md) for size/provenance decisions, not a renderer's defaults.

Some frozen source JSONs and historical verification records contain status text from the day of issue (for example “held” or “submitted”). Do not edit them merely to update live status: their hashes are part of fabrication provenance. The canonical manifest selects the parts; [manufacturing status](../docs/manufacturing.md) describes their current physical disposition.

Renderer inputs are retained beside the owning revision: `meshes/` contains tessellations and `render-scene.json` contains placement parameters. The unversioned G inputs live directly under `output/`; its alternative mounting uses `backplate/`. O-M02 presentation meshes live under `manufacturing/O-M02/meshes/`. Q's gallery meshes are diagnostic void volumes; current part surfaces still come from Q-M04/Q-M03.

Structural studies retain compressed `.inp.gz` solver decks, `.dat.gz` results and `.json.gz` node/load metadata together under `radiator-FEA/`, `radiator-expanded-load/`, `radiator-R2/analysis/` and `radiator-R4/analysis/`. Review scripts read these directly. `context-24U/history/`, `context-25U/history/` and `analysis/historical-body-depth-assessment.json` hold earlier exploratory evidence, not current acceptance results.
