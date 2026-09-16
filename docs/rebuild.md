# Rebuilding current outputs

Use millimetres and explicit revision flags. Several shared/legacy scripts default to G, M, O-M02 or R1; calling them without the commands below can regenerate an older design.

## Environment

CAD uses Python with the pinned dependencies in `requirements.txt` (CadQuery, Pillow and ezdxf). PDF generation additionally needs ReportLab; packaging needs pypdf. The drawing scripts use their configured fonts. Optional FEA dependencies are in `requirements-fea.txt`. Blender is available locally at `/Applications/Blender.app/Contents/MacOS/Blender`.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Use the available document runtime for ReportLab/pypdf if the CAD environment lacks them. Do not overwrite a working environment just to reproduce unchanged outputs.

## Current steel specification issues: Q-M03 / R7-M01

Preserve the submitted Q-M01 body and original supplier archives. To rebuild the current R5-corner steel issues, retaining accepted ±0.10 mm cut tolerances:

```sh
.venv/bin/python scripts/prepare_Q_faceplate_issue.py --issue Q-M03
.venv/bin/python scripts/build_radiator_plate.py --revision R7
.venv/bin/python scripts/prepare_radiator_production.py --issue R7-M01
# Use the ReportLab/pypdf runtime; inspect both PDFs (five sheets) before packaging.
python3 scripts/draw_Q_production.py --faceplate-issue Q-M03 --faceplate-only
python3 scripts/draw_radiator_production.py --issue R7-M01
python3 scripts/package_Q_faceplate_issue.py --issue Q-M03
python3 scripts/package_radiator_production.py --issue R7-M01
# Render and inspect current presentations below before finalising the index.
```

These commands do not upload. `finalise_three_part_pack.py` checks the current body against its verified chamfered geometry and original source, the new steel files against their geometry sources and drawings, and the new five-sheet visual review. Refresh Q product/studio, R7 radiator and Q/R7 context renders before finalising. Refresh the visual-review hashes only after inspecting all three new body PDF sheets and 25 refreshed presentation images; the five steel sheets and seven radiator images retain their prior review.

## Current POM body issue Q-M04

After preparing the Q-M03 faceplate, run:

```sh
.venv/bin/python scripts/prepare_Q_body_issue.py
python3 scripts/draw_Q_production.py --body-issue Q-M04 --body-only
# Render and inspect the three new body sheets before packaging.
python3 scripts/package_Q_body_issue.py
```

Q-M04 preserves the submitted Q-M01 source and adds only the twelve C0.5 ×45° slab-edge chamfers. It also refreshes the current assembly STEP; run this step after faceplate preparation. Current Q product/studio/context renderers load Q-M04. Do not overwrite submitted archives. The accepted new-order pack is Q-M04 body + Q-M03 faceplate + R7-M01 radiator. Current review comprises three new body sheets, five unchanged steel sheets, 25 refreshed manifold/studio/context images and seven inherited radiator images. The tube equilibrium remains unchanged.

## Original manifold Q / Q-M01 reproduction

Q derives from the retained P solids and source-fitting library. Do not rebuild P just to rebuild Q.

```sh
.venv/bin/python scripts/build_revision_Q.py
.venv/bin/python scripts/prepare_Q_production.py
.venv/bin/python scripts/assess_Q_retention.py
.venv/bin/python scripts/assess_Q_torque.py
.venv/bin/python scripts/draw_revision_Q.py
# Use ReportLab/pypdf Python for the following; inspect all PDF sheets before packaging:
python3 scripts/draw_Q_production.py
python3 scripts/package_Q_production.py
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/render_revision_Q.py
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/render_photoreal_product.py -- --iteration Q --device METAL
```

Original supplier files are Q-M01; current faceplate specification is Q-M03. Do not run the original drawing/package commands to overwrite submitted archives during a steel-only revision. assembly references are separately in `output/assembly/Q/`. O-M02 manufacturing scripts are historical and must not be used for Q. Shared official fitting meshes remain under `output/long-bore-P/koolance-fit/`. The Q renderer shows unchanged button heads representing M4×10, with hidden shanks omitted. No upload occurs.

## Original radiator R6 / R6-M02 reproduction

```sh
.venv/bin/python scripts/build_radiator_plate.py --revision R6
.venv/bin/python scripts/prepare_radiator_production.py --issue R6-M02
# Use ReportLab, then inspect all three rendered PDF sheets:
python3 scripts/draw_radiator_production.py --issue R6-M02
# Use pypdf after visual inspection:
python3 scripts/package_radiator_production.py --issue R6-M02
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/render_radiator_plate.py -- --revision R6 --plate-only --device METAL
```

For a populated radiator assembly, first run `prepare_radiator_fan_mounts.py` with the CAD environment, then render R6 without `--plate-only`. The checked-in R6 images are the bare plate and notch views; populated R4 scenes remain historical assembly references. Do not imply a new render exists until it has been generated and inspected.

The package script reads the current submission writeup and supplier remarks, verifies PDF feature coverage and ZIP contents, then refreshes checksums. No command above uploads to a supplier.

## Current presentation regeneration

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/render_revision_Q.py
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/render_photoreal_product.py -- --iteration Q --device METAL
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/render_radiator_plate.py -- --revision R7 --device METAL
```

The Q renderer loads the Q-M03 faceplate explicitly. R7 produces seven views including the populated assembly, fasteners, notch and outside-corner detail. The Q inspection set has twelve views including R5 steel and C0.5 POM details; studio has four. Retain the existing tube equilibrium solution for this corner-only change.

## Composite StarTech25U scene

After the current Q/R7 source scenes and official fitting meshes exist (run `python3 scripts/assess_manifold_side_clearance.py` for the separate40/45/50mm envelope assessment):

```sh
# Only rerun these preparation checks when tubing inputs change:
# .venv/bin/python scripts/relax_context_tubes.py
# .venv/bin/python scripts/check_pvc_equilibrium.py
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/render_context_25u.py -- --device METAL
```

Use `--preview` for a half-resolution front overview in `tmp/`. A full run refreshes nine views (including a straight-on front tubing detail, a GPU block detail and a power-connector close-up) and `output/context-25U/25U-StarTech-context.blend`, recording source hashes in `layout.json`. `--check-only` rebuilds the native scene and verification without rendering. The preparation step requires NumPy/SciPy and writes rod solutions plus their force/stiffness checks. The Blender generator rejects stale solver inputs or changed nominal fitting routes. See [PVC physics](pvc-routing-physics.md). The generator calls `context_startech25.py`, `context_gpu5090.py`, `context_tubing.py`, `check_context_gpu.py` and `check_context_fit.py`; any failed curvature, tube-separation or mesh-intersection assertion stops the run before rendering/saving. Inspect the rear/pump detail as well as the front. Exact custom parts are retained; provisional pump/support, GPU and host envelopes remain labelled in the layout data.

## Historical reproduction

Sources and generated data for older revisions remain in their original locations. Superseded writeups and older packaging remarks are in [archive](archive/README.md); historical package scripts resolve those archived templates. See [iterations](iterations.md) for revisions and tags. Never combine an older manufacturing drawing with a newer mating part.

The composite saves a rack-centred perspective viewport with 5 mm near /10,000 mm far clipping. The previous 0.01 mm near clip provides very poor depth precision at rack viewing distances and can cause apparent z-fighting. `scripts/context_viewport.py` sets these defaults; it changes neither geometry nor render cameras. For close inspection below 5 mm, adjust the near plane temporarily rather than reverting to that extreme range for whole-rack viewing.

Operator confirmation, 15 September 2026: increasing Clip Start made the live viewport smoother. Retain the 5 mm default for the composite rack scene.

## Final three-part consistency record

After the current files and fresh visual checks exist, run `python3 scripts/finalise_three_part_pack.py`. This checks part ZIPs, source hashes and current Q/R7 context; it creates the submission index without uploading. Assembly instructions remain in `docs/assembly-Q.md`, outside the fabrication ZIPs.
