# Make and order a new revision

The supported authoring baseline is **macOS, Python 3.12 and Blender**. Start with [environment setup](rebuild.md#environment). Linux support is handled when somebody reports a concrete problem; it is not a prerequisite for contributing.

The CAD and drawing programs contain revision-specific geometry and checks. Making a new design requires editing those programs as well as configuration values. The release helper handles file selection and packaging; it does not generate a different manifold from a name alone.

## 1. Start a separate draft

Read the [current recap](three-part-recap.md), [manufacturing status](manufacturing.md) and [working rules](../AGENTS.md). Decide which custom parts change and which interfaces must remain compatible. A manufacturing revision identifies a specific drawing/part specification; a geometry revision identifies the underlying design. Give changed parts unused manufacturing revision numbers, and update their geometry revision if the design changes.

For example, start a body-only study from the current Q-M04/Q-M03/R7-M01 set:

```sh
git switch -c feature/corner-study
.venv/bin/python scripts/release.py init corner-study --change body=Q-M05
```

This creates `cad/releases/corner-study.json` and a draft `cad/manufacturing/Q-M05.json`. It reserves a new body name and output paths; faceplate and radiator remain references to the unchanged delivered revisions. Starting values are inherited, **not approved specifications**. Existing configurations and output directories are never overwritten by `init`.

For multiple changed parts, repeat `--change`, using `body`, `faceplate` or `radiator` and distinct unused revision numbers. The example number is illustrative, not a new canonical selection. The same name cannot be initialised twice; continue editing the existing draft instead.

Commit the draft with its design rationale. Keep the current release manifest and delivered archives unchanged while developing it.

## 2. Adapt the relevant builders and checks

Copy the relevant programs to new names directly under `scripts/` so their existing repository-root calculation remains correct. Give all generated outputs new paths **before running the copies**. Keep shared inputs as references to the original files; do not copy or rescale vendor models.

| Changed area | Starting point | What must be updated together |
|---|---|---|
| Body finishing / minor machining detail | `prepare_Q_body_manufacturing_revision.py`, `cad/manufacturing/Q-M04.json` | New revision and part number, output folder, source solid, dimensional checks, feature schedule, own script name in source hashes; put any new assembly in a separate folder |
| Galleries, port layout or body dimensions | `build_revision_Q.py`, and where necessary `build_long_bore.py`; `cad/iterations/Q-rear-ports.json` and its P basis | Actual solids and port positions, two-gallery connectivity, wall/clearance checks, tapping pilots, mating faceplate positions and manufacturing schedule |
| Manifold faceplate | `prepare_Q_faceplate_manufacturing_revision.py` and, for layout changes, the manifold geometry builders | Cut geometry, holes/windows/slots, mating-body clearance, feature schedule and revision-specific checks |
| Radiator plate | `build_radiator_plate.py`, `prepare_radiator_production.py`, `cad/radiator/R7.json` | New geometry and manufacturing revisions, accepted argument choices, output names, apertures/notch/mounting positions and independent geometry checks |
| Body or faceplate drawings | A new copy of `draw_Q_production.py` | Manufacturing revision choices, feature-schedule inputs, title/date/material/finish, dimensions, coordinate tables and matching STEP pilot/thread definitions |
| Radiator drawing | A new copy of `draw_radiator_production.py` | Geometry/manufacturing revision inputs, title/date, all profile/hole tables, tolerances and finishing notes |
| Manifold presentation | Copies of `render_revision_Q.py` and `render_photoreal_product.py` | New body/plate input paths, separate image/Blender output folder, source hashes and revision labels |
| Radiator presentation / rack fit | Copies of `render_radiator_plate.py` / `render_context_25u.py` as affected | New geometry references and separate outputs; rerun affected fit/tube checks when interfaces change |

In particular, the existing body builder checks a literal C0.5 chamfer against a 410 × 40 × 87 slab, and drawings contain literal dimensions and revision-specific branches. Changing a JSON value alone is insufficient. Update the CAD operation, independent expected geometry and drawing together. Preserve unrelated checks; adjust a check because its requirement changed, not merely to make a failure disappear.

The new geometry-verification JSON must identify the new `manufacturing_revision`, have `checks: "PASS"`, and include `source_sha256` covering its new configuration and the geometry generator/inputs used. Use the existing verification reports as examples. The release helper checks these hashes strictly. Do not extend the historical `cad/source-maintenance.json` exceptions to bless a design change.

Protect released files by checking every output assignment in the copied programs, including `output/assembly/Q/`, `output/pdf/`, renderer manifests and source-hash paths. Use `git diff --name-only` after a build; changes to released files indicate a wrong destination. For exploratory runs of an original program, use a separate disposable checkout and copy back only deliberately selected new outputs.

## 3. Build and inspect the changed parts

Run your new geometry and drawing programs with `.venv/bin/python`; run your new scene programs with Blender. The [rebuild guide](rebuild.md) supplies the existing dependency order and Blender commands. Supply explicit geometry/manufacturing revision arguments where supported.

For each changed part, produce the paths listed in the draft manifest:

- A source manufacturing configuration and passing geometry-verification report.
- A single-part STEP, matching fabrication PDF, and a DXF for either steel plate. Threads remain pilot cylinders in STEP with finished thread specifications in the PDF.
- Drawing previews and affected product/fit renders, saved under a new revision directory.

Check all affected dimensions, thread/pilot depths, hole coordinates, mating clearances and required finishing operations. Inspect every changed PDF sheet for legibility and correct call-outs. Check STEP/DXF geometry against those call-outs. Reassess relevant loads or coolant/clearance assumptions only when the change affects them; a new filename does not require repeating unrelated studies.

In `cad/releases/corner-study.json`, update `pdf_sheets`, supplier material/finish/thread options and manufacturing-only `jlc.remarks`. Replace the TODO remarks. Populate each changed part's `review_images` with repository-relative paths to **all changed PDF-sheet previews and the affected product/fit renders**. Those images are review evidence, not contents of the supplier ZIPs. The tool checks their existence and hashes; it cannot decide whether the chosen views adequately show the design.

```sh
.venv/bin/python scripts/release.py check cad/releases/corner-study.json
.venv/bin/python scripts/release.py snapshot cad/releases/corner-study.json
```

`snapshot` records the selected files and verification inputs in `cad/releases/corner-study-review.json`, initially with `status: "pending"`. Inspect the outputs, then set `status` to `reviewed` and fill in `reviewer` and the ISO date `reviewed_on`. This is a record of completed review, not an extra supplier approval. Do not mark files reviewed simply because the command succeeded.

If inputs change, inspect the changed outputs again, remove the obsolete **draft** review snapshot and run `snapshot` again. released packages and their embedded review records remain unchanged. The tool refuses to overwrite an existing snapshot accidentally.

## 4. Package and order

```sh
.venv/bin/python scripts/release.py package cad/releases/corner-study.json
```

Check the packaged files with `shasum -a 256 -c SHA256SUMS.txt` from inside the resulting directory.

The result is `output/submission/releases/corner-study/`, containing three part ZIPs, per-part quotation metadata/remarks, the review record, source hashes and checksums. Each ZIP contains only its part's STEP/PDF and, for steel, DXF. Unchanged parts reuse the original ZIP bytes. The tool refuses pending/stale review, mismatched drawing identities and an existing destination. It never uploads, pays, edits the canonical selection or overwrites released packages.

Use that directory's README and ZIPs with the process in [the JLC order guide](order-from-jlc.md). The original guide's download links select the delivered design; **use your new package's files and metadata instead**. Get a fresh supplier review and quotation. Any supplier-requested change must be reconciled with the affected drawing and revision before manufacture.

Commit the new configuration, generators, outputs, checks and review records together when they pass. Document the change and its limits in `docs/`, and add it to [the revision register](iterations.md). Record quotation, supplier acceptance and later physical checks separately; a successful package command is none of those things.

## Canonical selection and publication

A new quotation package is independently usable without becoming the repository's default. Keep `cad/current-release.json`, the root README's delivered-part links and the historical finaliser unchanged during a study. `finalise_three_part_pack.py` verifies the existing Q/R7 delivered set; it is not the new-release packager.

If the project deliberately adopts a new canonical design, update those entry points, assembly guidance and status records together in a separate reviewed change, and adapt the canonical index verifier to that selection. Do not label an unmade revision as delivered or carry forward physical acceptance that does not apply to it.

Run `.venv/bin/python scripts/check_publication.py` to confirm that the delivered files/navigation remain intact. Run `.venv/bin/python -m unittest discover -s tests` when changing the release tooling.

## Problems encountered by contributors

File a GitHub issue with macOS version/architecture, Python and Blender versions, the exact command, geometry/manufacturing revision, error output and relevant geometry or screenshot. Include `check_environment.py` output when setup is involved. Remove credentials and private account details from new reports. We will address observed failures rather than promise untested platform support.
