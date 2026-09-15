# Output directory guide

Current parts are manifold P and radiator R6. This directory also retains older generated evidence; folder presence and old embedded “current” wording do not imply current selection.

| Location | Use |
|---|---|
| `long-bore-P/cad/` | Current P body/faceplate STEP and DXF, geometry and retention checks |
| `long-bore-P/photorealistic/` | Current bare/connected studio images and Blender scenes; official Koolance fitting geometry |
| `long-bore-P/koolance-fit/` | Supplier fitting meshes and dimensional/provenance verification |
| `long-bore-P/product-views/` | Current P geometry inspection views; fittings remain simpler references |
| `pdf/manifold-revision-P.pdf` | Current P review drawing, not a dedicated supplier manufacturing issue |
| `radiator-R6/` | Current radiator plate CAD, checks, bare renders and notch detail |
| `manufacturing/R6-M01/`, `pdf/SN1260-R6-M01-PLATE.pdf` | Current radiator production geometry, feature schedule and drawing |
| `submission/R6-M01/` | Current radiator part ZIP, remarks, guide and checksums |
| `context-25U/` | Current StarTech25U P/R6 composite, six views, orbitable scene and tubing/fit checks |
| `context-24U/` | Historical generic24U composite; superseded by the StarTech25U installation |
| `radiator-fan-integration/`, `radiator-R4/analysis/` | Retained fan/hardware fit evidence and pre-notch structural baseline supporting R6 |

**Historical, not current supplier files:** `submission/O-M02/`, `submission/R4-M01/`, `submission/R5-M01/`, `manufacturing/O-M01/`, `manufacturing/O-M02/` and older radiator issues. Do not mix their dimensions or hardware with P/R6. Their snapshot readmes remain historical records.

Other `long-bore-*` and `radiator-R1` through `radiator-R5` folders are previous revisions. Unversioned manifold `cad/`, `product-views/`, `images/`, SVGs and `manifold-review.blend` belong to the old rear-cover G design. `backplate/` is the unselected combined rear/rack alternative. The former O-M02/MO-RA composite and generated sketches are recoverable from Git at `0ec11be`; the active context folder contains the refreshed P/R6 scene.

Older analysis directories and revision-labelled PDFs retain their actual model/load assumptions. Do not relabel their numerical results as new P/R6 tests. [Current project guide](../README.md) · [manufacturing status](../docs/manufacturing.md) · [archive](../docs/archive/README.md).
