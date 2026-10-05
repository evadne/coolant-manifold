# Repository publication review

Review date: 5 October 2026. The repository has been prepared for readers to identify the current design, order its three parts and understand the evidence. The operator has authorised public release at `evadne/coolant-manifold` and selected CERN-OHL-W-2.0 for original project material. Publication verification is recorded below. Repository size and retrieved assets are retained deliberately; no history rewriting, censorship, redaction or LFS conversion is part of this cleanup.

## Changes made for readers

- README introduces the product with an angled assembled render, a connected render, a first-article photograph and a radiator render. It links directly to the current fabrication files.
- [Repeat-order instructions](order-from-jlc.md) give the exact three ZIPs, quantities, CNC/sheet-metal categories, material/finish choices and original manufacturing remarks. They separate historical prices from a fresh quotation.
- [Canonical selection](../cad/current-release.json) gives machine-readable revisions, paths and hashes. Historical geometry and supplier revisions remain in their original locations, with their roles explained in [the output guide](../output/README.md).
- AGENTS contains working procedures. Former mixed notes and manufacturing chronology are preserved as explicitly historical documents. Current status, design specifications, vendor experience and project reflection have separate homes.
- [JLCCNC first-article findings](jlc-first-article.md) name the supplier and batch. Slight steel-edge sharpness is not presented as a universal property of the design or raw stainless steel.
- Required renderer meshes and scene descriptions are tracked beside their owning revisions. Structural-analysis node metadata sits beside the retained compressed solver decks/results; review scripts read those directly. Original reference downloads and useful historical assessments have permanent homes. Redundant working copies, previews, logs and superseded one-off patch scripts have been removed.
- The generated fabrication index and its generator now use the same public ordering path. A read-only [publication checker](../scripts/check_publication.py) checks bundle identity, archive contents, index hashes and maintained local navigation links.

## Size and retention

At the start of this review, Git tracked 916 files containing 1,502,294,509 bytes (about 1.50 GB). The subsequent input classification adds the retained renderer assets, analysis metadata and reference sources; this initial count is not the final publication size.

The largest tracked file is the approximately 92.7 MiB StarTech25U Blender scene. The current tree contains no file above 100 MiB; a scan of all reachable Git blobs also found none above 100 MiB. Several files exceed 50 MiB. GitHub documents warnings above 50 MiB, a normal-Git block above 100 MiB and a preference for smaller repositories. [GitHub file and repository guidance](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

The operator explicitly accepts a large repository. Publication uses ordinary Git with retained history and revision tags. Required assets have been placed in their owning directories; historical tracked outputs remain in place. LFS or release attachments remain possible future choices, not changes silently applied now. The current `.gitattributes` marks CAD/media binary; that does not itself enable LFS.

## Provenance and information exposure

The operator explicitly requests retaining Koolance and other retrieved models, supplier records and full history without redaction. [LICENSING.md](../LICENSING.md) identifies original work, reference assets, manufacturer notices and composite scenes. No blanket reuse grant or comprehensive third-party rights clearance is claimed. Original project material is now licensed under [CERN-OHL-W-2.0](../LICENSE); third-party material retains its own terms.

Publishing the retained history also exposes supplier order references, a recorded checkout reference, portal screenshots, local workspace paths and Git author metadata. These are retained knowingly under that direction; the public order guide does not require another user's account data. A targeted scan of 364 then-tracked text files found no matches for the selected high-confidence private-key/GitHub-token/AWS-key-ID/OpenAI-key patterns. This was not an exhaustive secret audit, OCR scan or scan of every historical text blob. The five first-article JPEGs have no GPS EXIF field; their original files were retained unchanged.

No credentials, supplier accounts or payment actions were accessed during this publication review. No files were removed or redacted to produce a misleadingly clean history.

## Reproduction limits

The delivered fabrication ZIPs are usable without rebuilding the project. Their hashes and extracted members are checked against the revision-specific originals and current STEP/PDF/DXF files. They have not changed during this cleanup.

A full source rebuild still has host assumptions: the drawing scripts register macOS Arial paths, Blender examples use a macOS application path and Metal, some scripts require historical retained solids/scenes, and optional FEA needs a separate solver. The supported baseline is now explicitly macOS/Python 3.12/Blender. The requirements include the direct CAD, DXF, PDF and tube-physics dependencies; optional FEA requirements add Gmsh/Matplotlib. An unavailable `ezdxf==2.9.0` pin was corrected to the project’s installed and tested 1.4.4. [Rebuild instructions](rebuild.md) describe these limits and the tracked input locations. This review does not claim a clean Linux or Windows rebuild or re-run physical simulations. A fresh export containing only staged Git files passed the bundle/navigation/input checks without a project scratch directory. All sixteen retained structural cases were read from compressed evidence and reproduced the saved displacement/stress summaries. Blender constructed the historical G backplate and P scenes and the current Q scene from that export; the construction check suppressed rendering and saving. This is input/reproduction validation, not renewed visual approval.

The final pack verifier checks the retained geometry, eight drawing sheets and recorded 32-image review evidence. Exact source edits for input relocation and preview-directory creation are recorded in `cad/source-maintenance.json`; the verifier checks both source hashes and reverses those recorded edits before accepting the older provenance hash. This checks existing review provenance; no fresh visual approval of all those artefacts is claimed. The README's angled assembled render was visually inspected during this review. Local Markdown target checks do not establish identical rendering in GitHub's UI.

## Contributor workflow verification

[The new-revision workflow](new-revision.md) covers draft revision allocation, geometry/drawing changes, checks, visual review, separate quotation packages and ordering. `release.py` leaves released archives and the delivered selection untouched; it carries unchanged part ZIPs forward byte-for-byte and rejects stale review records or a reused output directory. It deliberately leaves revision-specific CAD and engineering checks explicit.

A new Python 3.12 virtual environment installed successfully from the declared requirements. Package consistency, macOS fonts, Blender startup and STEP/DXF/PDF round trips passed. In an isolated Git-only checkout, the current body/faceplate and radiator generators, all eight drawing sheets and all three existing packaging commands ran successfully using that environment. Seven release-tool tests cover output preservation, stale geometry/review, incorrect drawing revisions, unchanged-part integrity and invalid paths. The ordinary publication check still validates the original delivered ZIPs. These checks are not new supplier approval or a fresh visual/physical qualification of the design.

No speculative Linux work or general-purpose CAD framework was added. Contributors should report concrete failures with commands, versions and affected revisions.

## Public release

On 5 October 2026 the operator authorised public publication at `evadne/coolant-manifold` under CERN-OHL-W-2.0. The GitHub CLI initially used `evadne-feg`; it was switched to the already authenticated `evadne` account and the active identity was verified before repository creation.

Published at **[evadne/coolant-manifold](https://github.com/evadne/coolant-manifold)** on 5 October 2026. Default branch: `main`. The initial public push contains licence commit `9c57e66` and the full existing history, with all eight revision tags. GitHub accepted the ordinary Git push, issuing advisory warnings for files over 50 MiB; no file removal, LFS conversion or history rewriting was needed.

Verification completed:

- GitHub reports public visibility, owner `evadne`, default branch `main` and recognised licence `CERN-OHL-W-2.0`.
- Remote `main` matched the local licence commit; the downloaded root `LICENSE` matched the local file byte-for-byte.
- The public README was inspected in GitHub's browser renderer. All four embedded product/first-article images loaded; the canonical fabrication table and licence navigation rendered correctly.
- All three canonical ZIPs were downloaded without authentication and matched the manifest's SHA-256 hashes.
- Local publication checks passed for three fabrication bundles, 207 navigation links, 140 retained meshes, eleven scene descriptions and sixteen solver cases.

The local `design/initial-manifold` branch is retained and tracks `origin/main`. The publication record is committed and pushed after these checks. GitHub authentication remains on `evadne`; no account was signed out.

These are publication decisions. They do not reopen the operator's manifold fit acceptance or change the delivered design. The radiator remains delivered but operator-unverified; no leak-test result has been reported. [Astra's commentary](astra-commentary.md) records the significance of moving from models and supplier drawings to physical objects without promoting those observations into unperformed tests.

## Terminology clarification — 5 October 2026

Manufacturing uses of “issue” have been replaced by “revision” in maintained prose, archived project narratives and generator labels. Geometry revisions and manufacturing revisions are named separately. Bug-report instructions explicitly say “GitHub issue”; physical difficulties are concerns, problems or limitations. Commands, four Q script filenames and current JSON keys now use explicit manufacturing-revision names; schema version 2 identifies the updated selection/release manifests.

Previously submitted PDF/STEP/DXF/ZIP files, supplier records, render manifests and third-party references remain unchanged. Their original terminology is retained as evidence, with legacy keys translated in memory by `revision_json.py`. Exact reversible source-maintenance records resolve renamed generators and verify earlier source hashes; conflicting old/new revision values are rejected.

Validation: eleven release/metadata tests passed; all nine current preparation, drawing and packaging commands passed in a temporary Git-only checkout. All eight regenerated drawing sheets were rendered and visually checked, including the radiator’s revised title/control labels. Headless Blender also constructed the Q product, studio and 25U context scenes successfully; studio/context rendering and scene saving were suppressed for this construction check, and the context reported no tube/equipment intersections. These temporary files were not substituted into the delivered manufacturing pack. The final-pack/publication checks continue to verify the unchanged three canonical fabrication ZIPs.
