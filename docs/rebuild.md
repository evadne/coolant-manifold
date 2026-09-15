# Rebuilding current outputs

Use millimetres and explicit revision flags. Several shared/legacy scripts default to G, M, O-M02 or R1; calling them without the commands below can regenerate an older design.

## Environment

CAD uses Python with the pinned dependencies in `requirements.txt` (CadQuery, Pillow and ezdxf). PDF generation additionally needs ReportLab; packaging needs pypdf. The drawing scripts use their configured fonts. Optional FEA dependencies are in `requirements-fea.txt`. Blender is available locally at `/Applications/Blender.app/Contents/MacOS/Blender`.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Use the available document runtime for ReportLab/pypdf if the CAD environment lacks them. Do not overwrite a working environment just to reproduce unchanged outputs.

## Manifold P

```sh
.venv/bin/python scripts/build_long_bore.py --iteration P
.venv/bin/python scripts/prepare_revision_P.py
# Run with a Python environment containing ReportLab:
python3 scripts/draw_revision_P.py
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/render_product.py -- --iteration P
.venv/bin/python scripts/prepare_koolance_qd3.py
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/render_photoreal_product.py -- --iteration P --device METAL
```

Omit `--device METAL` for CPU rendering. Import the retained original Koolance STEP sources at supplier scale. The last rendition refresh used finer body/plate tessellation (0.025 mm /0.06 rad); ordinary regeneration may differ slightly at rendered edges without changing STEP geometry. Inspect fresh images after regeneration. The P scripts check geometry and retention clearance, and the fitting preparation checks supplier model dimensions.

These commands generate design/review outputs under `output/long-bore-P/` and `output/pdf/manifold-revision-P.pdf`. **They do not create a P manufacturing issue.** `prepare_manufacturing.py`, `draw_manufacturing.py`, `verify_manufacturing.py` and `package_manufacturing.py` currently belong to historical O-M02 and must not be mistaken for a P packaging workflow.

## Radiator R6 / R6-M01

```sh
.venv/bin/python scripts/build_radiator_plate.py --revision R6
.venv/bin/python scripts/prepare_radiator_production.py --issue R6-M01
# Use ReportLab, then inspect all three rendered PDF sheets:
python3 scripts/draw_radiator_production.py --issue R6-M01
# Use pypdf after visual inspection:
python3 scripts/package_radiator_production.py --issue R6-M01
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/render_radiator_plate.py -- --revision R6 --plate-only
```

For a populated radiator assembly, first run `prepare_radiator_fan_mounts.py` with the CAD environment, then render R6 without `--plate-only`. The checked-in R6 images are the bare plate and notch views; populated R4 scenes remain historical assembly references. Do not imply a new render exists until it has been generated and inspected.

The package script reads the current submission writeup and supplier remarks, verifies PDF feature coverage and ZIP contents, then refreshes checksums. No command above uploads to a supplier.

## Composite 24U scene

After the current P/R6 source scenes and official fitting meshes exist:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/render_context_24u.py -- --device METAL
```

Use `--preview` for a half-resolution front overview in `tmp/`. A full run refreshes four views and `output/context-24U/24U-context.blend`, recording source hashes in `layout.json`. Inspect the rear/pump detail as well as the front. Exact custom parts are retained; provisional pump/support, GPU and host envelopes remain labelled in the layout data.

## Historical reproduction

Sources and generated data for older revisions remain in their original locations. Superseded writeups and older packaging remarks are in [archive](archive/README.md); historical package scripts resolve those archived templates. See [iterations](iterations.md) for revisions and tags. Never combine an older manufacturing drawing with a newer mating part.
