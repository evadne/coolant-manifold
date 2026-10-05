# Working rules

## Read and resolve the current design

- Use millimetres and British English.
- Before design changes, read [README](README.md), [the canonical release manifest](cad/current-release.json), [the design recap](docs/three-part-recap.md) and [manufacturing status](docs/manufacturing.md).
- Resolve current files from the manifest and [current fabrication index](output/submission/current-three-parts/README.md). Do not infer authority from directory names, modification times or a historical document saying “current”.
- Treat `docs/archive/` as historical evidence, never active instructions. Use [the revision register](docs/iterations.md) and [design evidence index](docs/README.md) for rationale.
- Preserve recorded operator acceptance unless a relevant design change or new finding requires reassessment. Distinguish operator observations, measured evidence, simulation and supplier approval.

## Change and verify

- For a new issue, follow [the contributor workflow](docs/new-revision.md). Keep draft configurations, geometry, drawings and outputs separate; use `scripts/release.py` for new quotation packs. The historical finaliser selects the delivered set only.
- Support macOS/Python 3.12/Blender as the authoring baseline; address other-platform failures when reported rather than adding speculative adaptations.
- Follow [rebuild instructions](docs/rebuild.md), using explicit revisions; older script defaults are not current build commands.
- Preserve submitted fabrication bundles and source references. Make fabrication changes as new issues with matching STEP, PDF and steel DXF; do not silently amend a received part's issue.
- Keep fabrication documents limited to manufacture and inspection. Put bought-in hardware, plugs, tightening, threadlocker and installation in assembly guides.
- Keep material and finish selections consistent across CAD, drawings, remarks and supplier options. Treat render shaders as illustrative, not fabrication specifications.
- Maintain two isolated continuous galleries; do not add internal grouping or cross-links without a requested design change.
- Preserve the approved rack-scene tube routes, GPU/power geometry, fitting registration and original unscaled reference meshes. Use the specialised context/physics documents linked in [docs/README.md](docs/README.md) before editing them.
- Keep unresolved physical-fit concerns explicit; do not promote simplified clearance envelopes, FEA or visual acceptance to qualified ratings.
- Use headless Blender for scripted changes. Close a stale desktop session without saving over regenerated scenes. Preserve 5 mm viewport near clipping in the rack scene.
- Track required build inputs and retained evidence beside their owning revision or study. Temporary files must be disposable, with their directories created by the operation that uses them.
- For changed geometry, run relevant checks and inspect the affected drawings/renders before packaging. Do not refresh review hashes without actually reviewing the corresponding images or sheets.
- After changing canonical selection or packaging, run `python3 scripts/check_publication.py`; run `python3 scripts/finalise_three_part_pack.py` when regenerating the verified index. Neither command submits an order.
- Check local documentation links and preserve provenance when editing navigation. Update generator templates as well as generated indexes.

## Records and repository hygiene

- Put design decisions, rationale and project narrative in `docs/`; keep this file procedural.
- Keep vendor-specific feedback in the named supplier's report. Do not generalise one delivered sample to all manufacturers.
- Keep current status concise; retain dated events in the order/history record rather than repeating superseded statuses in entry points.
- Retain historical outputs and retrieved reference assets in place. Do not redact, remove, rescale or rewrite history as a publication-cleanup shortcut.
- Distinguish original design/code from third-party reference assets and record licensing decisions in [LICENSING.md](LICENSING.md). Do not apply a blanket licence to third-party content.
- Do not add credentials or new private checkout data to public documentation. Existing retained records have an explicit publication-review disposition.
- Commit completed work on the current feature branch at logical boundaries, using imperative British-English messages. Keep unrelated changes separate; finish with a clean worktree and report commit hashes.
- In the operator's local environment, append progress to `~/Projects/workspace/memory/YYYY-MM-DD.md` and commit that append promptly. Do not create that personal workspace for other contributors.

## External actions

- Require a user request for supplier orders, submissions or publication. Preparation of a package is not a payment instruction.
- For an explicitly requested repeat JLC quotation, follow [the repeat-order guide](docs/order-from-jlc.md) and use the canonical ZIPs.
- Preserve browser sign-in sessions; sign out only when account switching is expected. Use the established authentication method.
- Follow the user's existing authority for cart management; do not add redundant approval prompts for reversible cart changes.
