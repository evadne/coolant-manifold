# Revision P: plain-bore manifold faceplate

**Historical predecessor:** Q / Q-M01 is current. Retain P as a geometry and fitting-reference source; do not use its screw lengths or pilot depths for Q.

P is the current manifold body/faceplate pair, with a 2 mm plain-hole faceplate. It supersedes O-M02, whose 3 mm countersunk plate and JLC handover files are historical. This is a geometry and presentation iteration, not a qualified structural release.

## Changes

- 304 stainless faceplate: 482.6 × 87 × **2 mm**, approximately **395 g** from CAD. Twelve Ø4.5 through clearance holes; **no countersinks and no tapped steel holes**.
- Twelve body-retention screws, in two rows at Z7/80. Columns X−198/−120/−40/+40/+120/+198: four near the body corners and top/bottom fixings between pairs 2–3, 4–5, 6–7 and 8–9. X is measured from the width centre. Rack holes are a separate interface; six optional positions per side remain.
- Reference screws: [Westfield WF2237, M4 × 16 ISO 7380 button-head screws](https://www.westfieldfasteners.co.uk/Bolts-Screws-Metric/Hex-Button-Screw-M4x16-Stainless-Steel.html), A2 stainless; Ø7.6 head, 2.2 high, 2.5 mm hex socket, 1.3 socket depth. Length is measured **under the head**, unlike the former countersunk screws. The supplied product is A2, superseding the old A4 reference for this variation.
- Plain-bearing M4 × 0.7 heads are the alternative family, subject to head/washer clearance, length and thread engagement. **Countersunk screws are incompatible and using them is an assembly error.** No countersunk-head adaptor is part of this design.
- 16 mm screws through the 2 mm plate reach 14 mm into the POM. New M4 pilots extend 18 mm full diameter plus a 118° drill point (18.99 total); require 16 mm full-form thread after the 0.55 mm entry chamfer. The old 14 mm pilot/10 mm thread call-out is not sufficient for this screw choice. No washers in the rendition.
- Bosses shortened to **3 mm**, retaining 1 mm projection above the steel, Ø28 outer diameter, R1 root and C0.5 outer lip. Main slab remains 40 mm; overall POM depth 43 mm. Front pilot length becomes 23 mm to gallery axis Y20.

Ten front pairs retain 40 × 40 mm pitch. All 24 direct G1/4 female ports and two independent continuous long-bore galleries remain. No grouping, rear plate or large perimeter seals. Side plugs/fittings retain their own face seals.

## Geometry checks

The CAD builder checks valid connected solids, isolated fluid networks, port/gallery connectivity and body/plate interference. Additional checks verify twelve plain cylindrical retention holes and no conical steel faces; screw-reference/part interference; and head clearance.

The M4 major-diameter envelope including the drill-tip depth remains approximately **8.64 mm** from the pilot-represented wet network. The smallest head-edge gap to a Ø36 front-port keep-out is **2.62 mm**, at the corner fixings; the top/bottom head-edge reserve is **3.2 mm**. These are nominal geometry checks, not proof of POM pull-out strength, creep life, coupling service clearance under every fitting, or torque allowance. Thread helices are not modelled. The domed screw crown is a visual approximation within the linked supplier's main dimensions.

## Review outputs

- `cad/iterations/P-long-bore.json`: source parameters.
- `output/long-bore-P/cad/`: STEP body/plate, flat DXF, reference assembly and geometry reports.
- `output/pdf/manifold-revision-P.pdf`: two-sheet plate/body review drawing, including hole schedules and new thread depths.
- `output/long-bore-P/product-views/`: eleven unmarked review angles/configurations and editable scene.
- `output/long-bore-P/photorealistic/`: bare-port and QD/tube studio views. No product surface markings. QDs and tube tails remain visual references, not a routed loop.

Reproduce with `build_long_bore.py --iteration P`, then `prepare_revision_P.py`, then `draw_revision_P.py` using the PDF runtime. Blender: `render_product.py -- --iteration P`. Prepare official fitting meshes with `prepare_koolance_qd3.py`, then run Blender `render_photoreal_product.py -- --iteration P` (optional `--device METAL` on a supported Mac). Preserve older issues. P needs its own supplier manufacturing issue; do not combine its 2 mm plate with the old screw-depth call-outs.

## Rendition refresh - 15 September 2026

The current P body and faceplate STEP files were reimported as valid single solids and checked against their 410×43×87 and 482.6×2×87 mm XYZ extents. Render meshes were refreshed at 0.025 mm linear / 0.06 rad angular tessellation settings, without modifying the source STEP or design parameters. The eleven unmarked product/inspection views and both 3000×1600 studio variants were regenerated with Blender. The accompanying `output/long-bore-P/rendition-refresh.json` records source hashes and output sizes. P retains its twelve button-head screws, 2 mm faceplate and 3 mm bosses.

The connected **studio** image now uses unscaled official Koolance **QD3-MTG4 + QD3-FT10X13** STEP geometry, cross-checked against the supplier drawings. The individual parts are manufacturer geometry; their coupled axial placement is inferred because the individual drawings do not dimension coupled length or release stroke. The translucent tube tails have nominal 10 mm ID / 13 mm OD; their deformation over barbs and under compression nuts is not simulated. See [fitting integration notes](koolance-qd3-studio-integration.md). The eleven general product/inspection views retain their simpler fitting references and should not be used to measure these Koolance parts.
