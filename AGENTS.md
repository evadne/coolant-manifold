# Working on this manifold

Use millimetres and British English. The current deliverable is an initial mechanical design, not a pressure-rated release. Preserve direct G1/4 female ports, parallel-only topology and no internal grouping. Service clearance has priority over 1U: revision A is 2U with 8 circuits.

Generate solids with `scripts/build_cad.py`; use Blender for review scenes and renders. Keep drawings, source parameters, manufacturing notes and generated STEP consistent. Threads are call-outs with pilot-cylinder representations in STEP; do not mistake them for finished plain bores. Run the built-in geometric checks after geometry changes and visually inspect fresh renders. Do not imply validated pressure, temperature, flow, torque or ergonomic performance without evidence.

Commit completed work on the current feature branch. Do not submit supplier orders or publish without the user's request.
