# Rack coolant manifold and SuperNova mount

The current three-part set is the **accepted Revision Q manifold body and faceplate**, plus the **R7 radiator plate with R5 external corners**. The held repeat-order issues are **Q-M01 body, Q-M03 faceplate and R7-M01 radiator**; both new steel issues use ±0.10 mm cut dimensions and coordinates. The original Q-M01/R6-M02 files were [submitted to JLCCNC for review before payment](docs/jlc-quotation-2026-09-15.md); the revised steel bundles are held for a future repeat order, not for replacement on the current order. The current order proceeds with its original files and the operator’s emailed acceptance. Both steel plates specify matching raw sheet finish. No payment or automatic payment was authorised.

![Q with official Koolance QD3 pairs](output/long-bore-Q/photorealistic/02-qd3-translucent-tubes.png)

| Part | Current definition | Supplier files |
|---|---|---|
| Q POM body | Black unfilled declared POM-C or POM-H;410×87×40 slab +3 mm bosses;28 G1/4 female ports; two isolated long galleries | [Q-M01 body ZIP](output/submission/Q-M01/RM10-Q-M01-BODY.zip), [drawing](output/pdf/RM10-Q-M01-BODY.pdf) |
| Q rack faceplate | 304 stainless,482.6×87×2;20 windows,12 plain M4 holes,12 optional rack slots; four R5 outer corners; raw stainless sheet finish | [Q-M03 plate ZIP](output/submission/Q-M03/RM10-Q-M03-FACEPLATE.zip), [drawing](output/pdf/RM10-Q-M03-FACEPLATE.pdf) |
| R7 radiator plate | 304 stainless,482.6×444.5×2; four NF-A20 positions,68 fixing openings,10×2 cable notch; four R5 outer corners; raw stainless sheet finish | [R7-M01 ZIP](output/submission/R7-M01/SN1260-R7-M01-PLATE.zip), [drawing](output/pdf/SN1260-R7-M01-PLATE.pdf) |

The manifold has20 front ports at40×40 mm pitch,4 side ports and4 rear ports aligned with the outermost front pairs. Side- or rear-fed infrastructure frees all ten front pairs for loads. Topology is parallel-only, without internal grouping or a rear cover. Fittings and plugs use their own face seals.

Q-M01 incorporates the operator's shorter retention detail: **10 mm full M4 thread after entry,13 mm pilot plus drill point**. Assembly uses **M4×10** button screws, initially dry without Loctite. [Assembly instructions](docs/assembly-Q.md) are separate from manufacturing drawings. This is a prototype mechanical definition, not a pressure/load/creep-rated release.

- [Three-part recap](docs/three-part-recap.md) · [JLC requirements and final-review items](docs/jlc-final-review.md) · [submission index](output/submission/current-three-parts/README.md).
- [Design/interfaces](docs/design.md) · [Q rear ports](docs/revision-Q-rear-ports.md) · [current product/studio views](docs/product-views.md) · [Koolance source geometry](docs/koolance-qd3-studio-integration.md).
- [StarTech25U scene](docs/context-25U.md) · [radiator assembly](docs/radiator-rack-plate.md) · [radiator load assessment](docs/radiator-load-assessment.md).
- [M4 sizing](docs/Q-retention-sizing.md) · [torque/creep and threadlocker research](docs/Q-torque-and-creep.md) · [POM/coolant](docs/pom-coolant-assessment.md).
- [Rebuild commands](docs/rebuild.md) · [revision register](docs/iterations.md) · [output guide](output/README.md) · [project instructions](AGENTS.md).

Sources: `cad/iterations/Q-rear-ports.json` derives from retained P CAD; `cad/manufacturing/Q-M01.json` defines manufacture; `cad/assembly/Q.json` defines assembly choices. Faceplate corner detail is `cad/manufacturing/Q-M03.json`. Radiator sources are `cad/radiator/R7.json` and `cad/manufacturing/R7-M01.json`. Threads in STEP are tapping pilots; the matching drawings specify finished threads. Historical outputs remain identifiable by their own revision and are not current supplier files.
