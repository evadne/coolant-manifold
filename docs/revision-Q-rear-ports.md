# Revision Q: four optional rear connections

Q is a separate review candidate derived from the selected P body. It adds **four G1/4 female ports** on the flat rear face, directly opposite the leftmost and rightmost front pairs. P and the current rack composite remain intact for comparison.

| Feature | Q candidate |
|---|---|
| Rear centres | X −180 / +180, Z 23.5 / 63.5 mm |
| Rear sealing plane | Y40, flat POM; no bosses |
| Rear pair separation | 360 mm horizontally; 40 mm vertically |
| Body | 410 × 87 × 40 mm slab; 43 mm overall with front bosses |
| Port count | 20 front + 4 side + 4 rear = 28 G1/4 female |
| Internal topology | Two separate continuous galleries; no grouping or cross-link |
| Front plate and fixings | Identical to P, twelve M4 retainers |

The rear ports are additional access points to the same supply and return galleries, not independent circuits. All ten front pairs can remain connected to systems while the cooling plant connects from behind. A typical external path is **return gallery → radiator(s) → reservoir/pump → supply gallery**. Radiators can be placed in series, or in an externally split and rejoined radiator stage. Four rear ports do not introduce a separate internal radiator circuit.

Rear connections allow the infrastructure to enter behind the rack panel and avoid needing lateral elbow projection. With the original 4 mm-head side plugs, the equipment envelope remains 418 mm wide before tolerances. Exact rear hose bends, reach and rack hardware still depend on the installation. This candidate does not assert a rerouted full-rack fit or settle the separate side-elbow concern when side elbows are used.

## Geometry and manufacturing

Each new Ø11.8 pilot reaches 20 mm to its gallery axis, with the same 118° drill-point convention as P. The entry is Ø13.8 × 1 deep; specify G1/4 BSPP to ISO 228-1, at least 8 mm full-form thread after the entry. That thread envelope ends at Y31, leaving 5.1 mm before the near gallery surface at Y25.9. The drilling meets the aligned front drilling and the longitudinal gallery.

The uninterrupted rear POM surface supplies the fitting's face seal. Preserve a nominal Ø28 flat sealing land; its closest body-edge margin is 9.5 mm. No raised rear boss, perimeter groove, rear plate or extra retention fastener is needed. Fittings/plugs provide their own O-rings. Every unused rear port must be plugged or fitted with a suitable self-closing coupling.

The addition needs four short rear drilling/tapping operations and a rear-facing setup. The reach is approximately 1.7 drill diameters; it does not change the original deep-gallery drilling requirement. Retain external deburring and internal cleaning/flushing, with no internal cross-hole deburring operation, as specified for P. Four extra ports also mean four extra threaded sealing interfaces to inspect. No pressure, creep, torque or fitting-load rating is inferred from these geometry checks.

## Checks and review files

The generated solid is valid and the two fluid networks remain separate. All four rear branches intersect only their intended gallery. The minimum M4 envelope-to-wet-network distance is **8.635 mm**. Four Ø36 × 80 mm rear hardware keep-outs clear the retained side-elbow reference solids by at least **13.038 mm**, with 4 mm between the two keep-outs in each rear pair. These are conservative nominal layout envelopes, not exact fitting or hand-access qualification. The faceplate STEP is copied byte-for-byte from P.

- [Rear layout and port call-outs](../output/long-bore-Q/rear-port-layout.svg)
- [POM body STEP](../output/long-bore-Q/cad/body.step)
- [Assembly STEP](../output/long-bore-Q/cad/manifold-assembly.step)
- [CAD verification](../output/long-bore-Q/cad/verification.json)
- [Unmarked assembly Blender file](../output/long-bore-Q/product-views/assembled-unmarked.blend)
- [50% transparency inspection Blender file](../output/long-bore-Q/product-views/body-50-percent-transparent.blend)

The STEP uses pilot representations for threads. The layout sheet and this candidate are **review outputs, not a manufacturing submission package**. Transparency and coloured voids show internal connectivity; real POM remains opaque.

```sh
.venv/bin/python scripts/build_revision_Q.py
.venv/bin/python scripts/draw_revision_Q.py
/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/render_revision_Q.py
```
