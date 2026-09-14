# Revision G — selected front and rear plate drafts

Option B is selected. The front faceplate carries the POM on the rack; the rear cover closes the galleries and clamps the two seals. All plate-to-POM joints use **M4 × 0.7**, with **A4 M4 × 12 DIN 7991 socket countersunk screws** as standard. The specified Westfield DIN 965 Z Pozi alternative remains acceptable. Rack fixings must match the actual rails/cage nuts; they are not reduced to M4 by this choice.

| Part | Finished size | Cut features | Secondary machining |
|---|---|---|---|
| Front rack faceplate | 482.6 × 87 × 3 mm | 18 Ø32 windows, 8 Ø4.5 screw holes, 4 slots 10 × 7 | 8 Ø8.0 × 90° countersinks on outside/front face |
| Rear sealing plate | 440 × 87 × 3 mm | 31 Ø4.5 screw holes | 31 Ø8.4 × 90° countersinks on outside/rear face; finish opposite sealing surface |

Both use the same M4 screw size. The different countersink diameters are retained from revision G: the rear socket heads sit approximately 0.22 mm lower than the outside surface with a Ø7.96 head, versus 0.02 mm on the front. Pozi heads sit lower in both. There are no M3 or M5 plate-to-POM screws in the selected design. The larger M5 features in the historical Option C assets are not part of this package.

- Front: [dimensioned draft](../output/faceplate-drawing.svg), [cut-only DXF](../output/cad/faceplate-flat.dxf), [finished STEP](../output/cad/faceplate.step).
- Rear: [dimensioned draft](../output/rear-cover-drawing.svg), [cut-only DXF](../output/cad/rear-cover-flat.dxf), [finished STEP](../output/cad/lid.step).
- [Geometry cross-check report](../output/cad/steel-plate-verification.json).

DXFs contain only a CUT layer, at 1:1 in millimetres. DXF XY corresponds to assembly XZ, with origin at the bottom centre. Both patterns are left/right symmetric; the drawings show the outside face. Do not cut the blue countersink circles shown on the drawings: the through holes are Ø4.5, not Ø8.0 or Ø8.4. Neither steel plate is tapped. The POM receives the M4 threads; its Ø3.3 CAD bores represent tapping pilots.

Punching or laser cutting the through holes is acceptable if the final dimensions, position and flatness are achieved. The supplier may finish the holes after cutting. Machine countersinks separately on the outside face. Retain a flat POM-facing surface, remove burrs and inspect after all finishing. The rear plate's 3 mm is **finished thickness**, so stock/process allowance must accommodate sealing-face machining. An unqualified 3 mm sheet blank is not a guarantee of the final thickness and flatness.

See [manufacturing notes](manufacturing.md) for tolerances, sealing finish and screw engagement, and [wetted-material assessment](wetted-materials.md) for the rear plate's 316L requirement. These are initial drafts for quotation and DFM; geometry revision G has not changed.

Regenerate both drawings and cut profiles with `.venv/bin/python scripts/export_steel_plates.py`. The exporter checks cut hole locations/diameters, countersinks, plate bounds and finished volume against the individual STEP plates. The older `export_faceplate_dxf.py` remains available for historical Option C export.
