> Current Q studio images reuse these retained official source meshes and accepted coupled pose. See [current views](product-views.md). The P paths below identify the original integration evidence.

# Koolance QD3 studio integration — Revision P

The two current studio outputs are `output/long-bore-P/photorealistic/01-bare-ports.png` and `02-qd3-translucent-tubes.png`, with matching editable Blender scenes. Both retain the current P manifold geometry. There are no added product surface markings.

## Manufacturer references

Downloaded on 15 September 2026 from the Files tabs on Koolance's [QD3-MTG4 page](https://koolance.com/quick-disconnect-no-spill-coupling-male-threaded-g-1-4-qd3-mtg4) and [QD3-FT10X13 page](https://koolance.com/quick-disconnect-no-spill-coupling-female-for-10mm-x-13mm-3-8in-x-1-2in-qd3-ft10x13). Original ZIPs, extracted STEP files and dimensioned PDFs are retained under `docs/references/koolance-qd3/`; `sources.json` records download URLs and SHA-256 hashes. These are supplier integration references, not instructions to manufacture the fittings.

| Published dimension | QD3-MTG4 male | QD3-FT10X13 female |
|---|---:|---:|
| Overall length, individual coupling body | 36.60 ±0.50 mm | 49.10 ±0.50 mm |
| Main hex across flats | 22 mm | 24 mm |
| Maximum body diameter | 23.90 mm | 26.10 mm |
| Pull-ring diameter | — | 23.70 mm |
| G1/4 thread projection | 4.50 mm | — |

The female drawing also gives a 15 mm compression nut, 21 mm across flats and Ø22.40 maximum, with an M18×1.5 compression thread. Tubing is 10 mm ID / 13 mm OD. The manufacturer's hex corners are clipped: do not calculate maximum diameters from an ideal sharp hexagon.

At the manifold's 40 mm horizontal and vertical pitch, the published Ø26.10 body envelopes leave **13.90 mm** between adjacent envelopes; Ø23.70 pull rings leave **16.30 mm**. These are nominal geometric gaps, not a measurement of finger access or a release-motion qualification.

## Geometry and assembly placement

`scripts/prepare_koolance_qd3.py` imports the original STEP geometry, verifies valid shapes and drawing length tolerances, checks relevant cylindrical radii, and exports separate meshes for all two male and three female solids. Only rigid positioning is applied; no dimensional scaling corrects or replaces supplier geometry. Blender converts millimetres to metres for physical lighting and material scale.

Measured planar-end lengths are 36.6154 mm and 49.1067 mm, within the drawings' ±0.50 mm tolerances. The male mounting-face-to-thread-tip distance is 4.4961 mm, consistent with the nominal 4.50 mm call-out. Small source-CAD/export differences are retained. Exact nominal dimensions and original supplier geometry must not be conflated.

Each male mounting face seats at the POM boss end, Y−3 mm. The female source includes the compression nut in position. The coupled axial pose registers the midpoint of the male annular latch groove with an internal female annular feature. This yields approximately 70.77 mm from the POM sealing face to the female barb tip, but **this is an inferred presentation dimension, not a published coupled length**. The operator has accepted this placement for the intended layout, as recorded below. Closed valves in the individual models are not articulated into their operating position; internal overlaps are not a coupled mechanism analysis.

Twenty linked instances of each complete fitting pair are present. Straight translucent tube tails use nominal free ID/OD; insertion is illustrative and rubber deformation over the barb or under the nut is not solved. Four side plugs and the button-head screw crowns remain visual references. POM thread bores retain the project's pilot-cylinder representation. The older general product-view set retains simpler QD references; the studio scenes are the current supplier-geometry fitting presentation.

## Reproduction and review

1. Generate the P manifold review scene using the existing P workflow.
2. Run `.venv/bin/python scripts/prepare_koolance_qd3.py`.
3. Run Blender with `--python scripts/render_photoreal_product.py -- --iteration P --device METAL`, or omit the device option for CPU rendering.
4. Inspect both fresh PNGs; retain the source hashes, fitting checks, scene counts and image dimensions in `output/long-bore-P/rendition-refresh.json`.

`output/long-bore-P/koolance-fit/verification.json` contains source hashes, drawing dimensions, measured lengths, mesh bounds and the explicit axial-pose assumption. Neither the P manufacturing geometry nor historical supplier packages are modified by this rendition refresh.

## Operator acceptance — 15 September 2026

The operator accepts the studio rendition and considers the depicted coupled length within the intended parameters, based on familiarity with many of these fitting pairs in their laboratory. Retain the current fitting placement and images. Rack installations are expected to provide sufficient space in front of the panels for fittings, tubing and servicing; the panel plane is not the installation's front clearance limit. No fixed numerical front clearance was specified. This acceptance resolves the visual layout review; the inferred dimension retains its documented provenance.
