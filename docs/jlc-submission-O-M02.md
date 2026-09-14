# JLC submission handover: O-M02

Prepared 15 September 2026. This is the current package for quotation and manual manufacturing review. No upload, supplier message, order or payment has been made. Earlier revisions remain archived.

## Upload these two parts separately

| Setting | POM body | Rack faceplate |
|---|---|---|
| File | `RM10-O-M02-BODY.zip` | `RM10-O-M02-FACEPLATE.zip` |
| Contents | Matching STEP + three-sheet PDF | Matching STEP + two-sheet PDF + through-cut DXF |
| Material | Black unfilled POM; POM-C or POM-H accepted | SUS304 / 304 stainless / EN 1.4301 |
| Threads | **YES**: 24 G1/4 + six M4 | **NO**: six clearance holes with front countersinks |
| Finish | As machined; no coating, blasting or markings | As machined; no coating, blasting or markings |
| Quantity | Suggested first quotation: one body | Suggested first quotation: one plate |

Quantity one each is a preparation assumption for a prototype set, not an order instruction. Choose the actual quantity when submitting. Bought-in fittings, plugs, hoses, M4 screws and rack hardware are not included in these fabrication files.

Use the two ZIPs in `output/submission/O-M02/`. Each contains only JLC-supported drawing/model formats. **The enclosing `RM10-O-M02-HANDOVER.zip` is for local handover: extract it first; do not upload it as a single part.**

Copy the corresponding `BODY-REMARKS.txt` or `FACEPLATE-REMARKS.txt` into the part remarks. Review the supplied DFM PDF alongside the parts. If the portal asks for tolerances/roughness, keep its selections consistent with the drawing: general DIN ISO 2768-1 m with local specified tolerances; body seal lands Ra 1.6 µm and 0.05 mm local flatness; other body exterior Ra 3.2 µm; internal bores Ra 6.3 µm. Do not accidentally request the tightest local finish/tolerance over the entire part. The faceplate drawing controls its flatness, hole/countersink limits and functional finishes.

JLC requires matching model/drawing names, thread details in the drawing and the Threads-YES setting for tapped parts. Webpage options take precedence over conflicting drawing instructions. Tell JLC these two parts mate. [Official ordering guidance, rechecked 15 September 2026](https://jlccnc.com/help/article/cnc-machining-ordering-guidelines).

## Supplier decisions required

The body needs manual acceptance of the two Ø11.8 galleries through 410 mm, including the specified alignment and any opposed-drilling meeting step. Request the drilling and inspection method before manufacture. Confirm black POM stock grade and datasheet, G1/4 ISO 228-1 tooling/gauging and the local sealing finishes. JLC lists [POM](https://jlccnc.com/help/article/pom-cnc-machining); no restriction to branded Delrin or one POM family is imposed.

The faceplate is a flat 3 mm part with no bends. Its six Ø8 ×90° countersinks are secondary operations, not through-cuts. The Ø32 windows clear the Ø28 bosses and their R1 roots. External deburring and internal chip cleaning remain specified; internal cross-hole deburring is not requested.

The approved layout uses 4 mm bosses, projecting 1 mm above the faceplate, a 40 mm slab, ten front pairs at 40 ×40 mm pitch and four side ports. There is no rear cover. Supplier substitutions or geometry/tolerance changes should be returned for review.

## Review evidence

The existing seven PDF pages have been visually checked again. STEP/DXF verification checks the body and plate solids, 24 port entries, six M4 pilots, twenty windows, six countersinks and twelve rack slots. The per-part ZIPs are checked against the exact source files and have SHA-256 checksums.

Fresh images under `output/manufacturing/O-M02/product-views/` and `photorealistic/` use meshes from the issued O-M02 STEP files. Both bare and QD-populated studio views use the new sealing plane. QD3 pairs and translucent 10/13 tubes are visual approximations. The 50%-transparent image is an internal-channel inspection view; real black POM is opaque. Images are review aids, not machining drawings.

Both POM-C and POM-H are accepted for the current quotation. The operator reports long successful service of an EK Pro manifold after Blitz Part 2 cleaning; this supports the intended maintenance choice, without identifying EK's resin subtype. Further material-family research is not a condition of preparing this package. Physical prototype qualification remains separate from supplier machining acceptance.

## Rebuild the handover

Run `scripts/verify_manufacturing.py`, visually inspect the existing PDFs, then run `scripts/package_manufacturing.py`. The latter refreshes the two upload ZIPs, submission notes, checksums and the enclosing handover archive. Use the existing environment with CadQuery for geometry checks and the bundled Python with pypdf for packaging.

To refresh the images, run `scripts/prepare_manufacturing_views.py` with CadQuery, then Blender with `scripts/render_product.py -- --iteration O --manufacturing O-M02`, followed by `scripts/render_photoreal_product.py -- --manufacturing O-M02`. The preserved O reference meshes in `tmp/mesh-long-bore-O/` are required; rebuild those from O if the temporary directory has been cleared. Original O and O-M01 outputs are not replaced.
