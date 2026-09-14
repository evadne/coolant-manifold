# RM8-2U rack coolant manifold

Initial design, revision A: eight parallel circuits, all connections on one face, black Delrin body and stainless steel rack ears. The 2U format provides space to operate QD3 release rings without crowding adjacent fittings.

![Assembled manifold](output/images/assembled.png)

| Parameter | Initial model |
|---|---|
| Bare rack envelope | 482.6 × 45.5 × 87 mm (width × depth × height) |
| Ports |18 × G1/4 female BSPP, machined into Delrin |
| Circuits |8 paired branches plus main inlet/outlet |
| Port pitch |45 mm horizontal /40 mm vertical |
| Reference pull-ring gaps |21.3 mm horizontal /16.3 mm vertical |
| Internal paths |One uninterrupted supply gallery and one uninterrupted return gallery |
| Manufacture |Rear-pocket milling, drilled/tapped front ports, sealed stainless rear cover, bent stainless ears |

The dimensions of EK's reference manifold are 326 × 57 × 36 mm; its published 57 mm height is 12.55 mm above 1U. Our model uses 2U to prioritise servicing access. See [design reasoning](docs/design.md) and [manufacturer sources](docs/sources.md).

## Review files

- [Editable Blender scene](output/manifold-review.blend) — CAD-derived body/cover/ears plus simplified QD3 and tube references.
- [Assembly STEP](output/cad/manifold-assembly.step) — four manufactured components and two seal envelopes. Individual body, cover and ear STEP files are alongside it.
- [Dimensioned layout](output/layout.svg) — front and rear views.
- [Full-size clearance template](output/clearance-template-1to1.svg) — print 100%, calibrate against the 100 mm bar; large-format or tiled print required.
- [Rear pockets, cover removed](output/images/open-galleries.png).
- [Manufacturing notes and BOM](docs/manufacturing.md) — thread call-outs, sealing details, fasteners and DFM requirements.
- [Geometry verification](output/cad/verification.json).

This is an initial model for feedback and vendor DFM, not a pressure-rated production release. STEP thread holes are pilot bores: use the thread call-outs in the manufacturing notes. QD shapes are illustrative, and actual ring travel/hand access must be trialled. Working pressure, total flow, coolant and final seal selection remain open.

## Rebuild

Python 3.12 and Blender 5.2 were used. CadQuery 2.8 exports the STEP solids; Blender renders tessellations of those same solids. Millimetres throughout.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_cad.py
.venv/bin/python scripts/draw_layout.py
/Applications/Blender.app/Contents/MacOS/Blender --background --python scripts/render_blender.py
```

Parameters are in `cad/parameters.json`. The source defines the current bracket/bolt pattern explicitly; changing circuit count or major dimensions also requires reviewing those patterns and the manufacturing documentation. It is not an automatically qualified product configurator.
