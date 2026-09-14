# Working on this manifold

Use millimetres and British English. The current deliverable is an initial mechanical design, not a pressure-rated release. Preserve direct G1/4 female ports, parallel-only topology and no internal grouping. Service clearance has priority over 1U: revision F is 2U with 8 circuits. The rack mount is one flat stainless faceplate with clearance windows; integral cylindrical POM bosses house the G1/4 female threads and project 3 mm beyond the steel. Fittings seat on the boss ends. Faceplate/body retention uses eight A4 M4 × 12 DIN 7991 hex socket countersunk screws, accepting the specified DIN 965 Z Pozi alternative. Target flush socket heads and lower Pozi heads; slight proudness is acceptable outside the port/fitting keep-outs and other hardware. Keep body retention separate from QD retention. A separate bottom plate is permissible.

Generate solids with `scripts/build_cad.py`; use Blender for review scenes and renders. Keep drawings, source parameters, manufacturing notes and generated STEP consistent. Threads are call-outs with pilot-cylinder representations in STEP; do not mistake them for finished plain bores. Run the built-in geometric checks after geometry changes and visually inspect fresh renders. Do not imply validated pressure, temperature, flow, torque or ergonomic performance without evidence.

Commit completed work on the current feature branch. Do not submit supplier orders or publish without the user's request.

Option C is a separate alternative generated with `--mounting backplate`, retained alongside Option B under `output/backplate/`. It combines the rack mount and gallery cover in one flat rear plate, with POM proud of the rails. Do not silently replace either option. Shared thread, seal and port spacing requirements apply to both.

Revision F uses two purchased RS 258-0460 EPDM rings (253.59 ID × 3.53 section). Rear grooves are 4.5 wide × 2.8 deep, capsule centreline 395 × 27 (R13.5), around 384 × 16 × 24 galleries. Outer cover screw rows are z4.5/82.5; read their edge offset from parameters. Both mounting options share revision F seal geometry. Keep analysis examples labelled with their geometry revision.
