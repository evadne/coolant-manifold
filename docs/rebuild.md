# Rebuilding current outputs

Use millimetres and explicit revision flags. Several shared/legacy scripts default to G, M, O-M02 or R1; calling them without the commands below can regenerate an older design.

## Environment

The supported authoring environment is **macOS and Python 3.12**, with Blender installed separately. Blender 5.2.1 LTS is the version used for the latest checks. The standard requirements cover CAD, DXF, PDF generation/packaging and the existing tube-equilibrium tools. The drawing programs use macOS Arial fonts; Blender examples use its normal application path. Where a renderer accepts `--device METAL`, omit that option to use its CPU default if needed. Other-platform failures will be investigated when reported; no Linux-specific adaptation has been added pre-emptively.

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/check_environment.py
.venv/bin/python scripts/check_publication.py
```

`check_environment.py` checks the declared package versions/imports, Arial, Blender startup and small STEP/DXF/PDF round trips. Use `--blender /path/to/Blender` if installed elsewhere. These are tested top-level dependency pins, not a promise of byte-identical exports across every future transitive dependency. The publication check verifies the retained fabrication pack and inputs without regenerating them.

For the optional historical structural-analysis tools:

```sh
.venv/bin/python -m pip install -r requirements-fea.txt
.venv/bin/python scripts/check_environment.py --fea
```

A separate CalculiX 2.23 executable is only needed to solve new structural cases; reading the retained results does not require it. The original solver ran on Linux; this does not change the macOS CAD/Blender baseline.

**To make a new revision, follow [the contributor workflow](new-revision.md).** The commands below reproduce existing revisions into their existing paths. Run them only in a disposable checkout for reproduction checks; do not overwrite released archives in your working branch. For a new revision, copy/adapt the relevant generators to new output paths and use the separate release helper. Ordering existing parts needs none of these installations.

Render meshes and scene descriptions are tracked beside the matching revision under `output/`. The Q inspection renderer reads its two gallery meshes from `output/long-bore-Q/meshes/` and its finished solids from `output/manufacturing/`; no preliminary cache preparation is needed.

For a read-only check of current download selection, hashes and navigation, run:

```sh
.venv/bin/python scripts/check_publication.py
```

## Current steel specification revisions: Q-M03 / R7-M01

Preserve the submitted Q-M01 body and original supplier archives. To rebuild the current R5-corner steel revisions, retaining accepted ±0.10 mm cut tolerances:

```sh
.venv/bin/python scripts/prepare_Q_faceplate_manufacturing_revision.py --manufacturing-revision Q-M03
.venv/bin/python scripts/build_radiator_plate.py --revision R7
.venv/bin/python scripts/prepare_radiator_production.py --manufacturing-revision R7-M01
# Inspect both PDFs (five sheets) before packaging.
.venv/bin/python scripts/draw_Q_production.py --faceplate-manufacturing-revision Q-M03 --faceplate-only
.venv/bin/python scripts/draw_radiator_production.py --manufacturing-revision R7-M01
.venv/bin/python scripts/package_Q_faceplate_manufacturing_revision.py --manufacturing-revision Q-M03
.venv/bin/python scripts/package_radiator_production.py --manufacturing-revision R7-M01
# Render and inspect current presentations below before finalising the index.
```

These commands do not upload. Regenerating an existing revision may change file bytes and invalidate the original source/review hashes even when the nominal design is unchanged. Inspect regenerated drawings and presentations in the disposable checkout; retain the delivered archives and their historical review records in the project. For new revisions, use the new-revision workflow rather than changing those historical hashes.

## Current POM body revision Q-M04

After preparing the Q-M03 faceplate, run:

```sh
.venv/bin/python scripts/prepare_Q_body_manufacturing_revision.py
.venv/bin/python scripts/draw_Q_production.py --body-manufacturing-revision Q-M04 --body-only
# Render and inspect the three new body sheets before packaging.
.venv/bin/python scripts/package_Q_body_manufacturing_revision.py
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
# Inspect all PDF sheets before packaging:
.venv/bin/python scripts/draw_Q_production.py
.venv/bin/python scripts/package_Q_production.py
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/render_revision_Q.py
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/render_photoreal_product.py -- --iteration Q --device METAL
```

Original supplier files are Q-M01; current faceplate specification is Q-M03. Do not run the original drawing/package commands to overwrite submitted archives during a steel-only revision. assembly references are separately in `output/assembly/Q/`. O-M02 manufacturing scripts are historical and must not be used for Q. Shared official fitting meshes remain under `output/long-bore-P/koolance-fit/`. The Q renderer shows unchanged button heads representing M4×10, with hidden shanks omitted. No upload occurs.

## Original radiator R6 / R6-M02 reproduction

```sh
.venv/bin/python scripts/build_radiator_plate.py --revision R6
.venv/bin/python scripts/prepare_radiator_production.py --manufacturing-revision R6-M02
# Inspect all three rendered PDF sheets:
.venv/bin/python scripts/draw_radiator_production.py --manufacturing-revision R6-M02
# Package after visual inspection:
.venv/bin/python scripts/package_radiator_production.py --manufacturing-revision R6-M02
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

After the current Q/R7 source scenes and official fitting meshes exist (run `.venv/bin/python scripts/assess_manifold_side_clearance.py` for the separate40/45/50mm envelope assessment):

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

Run `.venv/bin/python scripts/finalise_three_part_pack.py` to verify/recreate the delivered Q/R7 index from its retained files and review records. It is specific to that set and does not promote a new revision. The separate `release.py` workflow packages new reviewed revisions without modifying this index. Assembly instructions remain outside fabrication ZIPs.

## Reading retained structural studies

The original solver decks, results and node/load metadata are tracked together, compressed, in each study's output directory. With the FEA Python dependencies installed, `review_radiator_fea.py`, `review_radiator_expanded_load.py`, `review_radiator_R2.py` and `review_radiator_R4.py` can recalculate reports/plots directly from those files without running CalculiX again.

For a new solver run, `radiator_plate_fea.py` writes the plain `.inp` deck and compressed metadata into the corresponding study directory (R1: `output/radiator-FEA/`; expanded label: `output/radiator-expanded-load/`; R2/R4: their `analysis/` directories). Run CalculiX with that directory as the working directory and retain the resulting `.dat` there. The review script prefers these plain fresh results, then archives the decks/results as gzip. Once archived, remove the redundant plain decks/results. Midsurface geometry is an automatically disposed intermediate. Do not rerun a historical study merely to select files for manufacture.

The preserved scene-specific checks in `scripts/archive/` apply only to their named historical scenes. They are not current-design acceptance checks.

Run `.venv/bin/python scripts/check_publication.py` for read-only bundle, navigation and retained-input checks. `.venv/bin/python scripts/check_retained_inputs.py` can also check the renderer meshes, scene descriptions, all sixteen complete solver cases and the explicit source-maintenance records independently. Neither command needs Blender or CalculiX.

## Manufacturing revision terminology

The command options are `--manufacturing-revision`, `--body-manufacturing-revision` and `--faceplate-manufacturing-revision`. The four Q preparation/packaging scripts use `_manufacturing_revision.py` filenames. The canonical selection and new release manifests use schema version 2. Configuration and new verification metadata use `manufacturing_revision` (and explicit body/faceplate variants), distinct from `geometry_revision`.

Retained supplier archives, drawings, render manifests and quoted correspondence preserve the wording used when released. Their legacy `issue` fields mean manufacturing revision. `scripts/revision_json.py` translates those fields when reading them; it rejects conflicting old/new values. Exact source-maintenance records account for terminology and filename changes without changing submitted artefacts or claiming a fresh review of their geometry.
