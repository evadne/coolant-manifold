# Rack coolant manifold and SuperNova mount

The current accepted three-part set is **Q-M04 POM body, Q-M03 manifold faceplate and R7-M01 radiator plate**. The body has C0.5 slab-edge chamfers and eight modelled corner flats; both steel plates have R5 outer corners, ±0.10 mm cut dimensions/coordinates and matching raw sheet finish. A [separate new JLC order](docs/jlc-order-2026-09-16.md) was submitted for file review on 16 September after the operator confirmed UPS, the cheapest quoted shipping service. The operator reports clearing the original Q-M01/R6-M02 order; its fabrication archives are preserved. The operator’s 22 September screenshots show both steel parts awaiting carrier pickup and the POM body in production at 23.08%, with programming and blanking complete. The reviewed POM price is US$197.26. No payment has been made by the agent; payment transaction details are not shown.

![Q with official Koolance QD3 pairs](output/long-bore-Q/photorealistic/02-qd3-translucent-tubes.png)

| Part | Current definition | Supplier files |
|---|---|---|
| Q POM body | Black unfilled declared POM-C or POM-H;410×87×40 slab +3 mm bosses;28 G1/4 female ports; two isolated long galleries; C0.5 slab edges | [Q-M04 body ZIP](output/submission/Q-M04/RM10-Q-M04-BODY.zip), [drawing](output/pdf/RM10-Q-M04-BODY.pdf) |
| Q rack faceplate | 304 stainless,482.6×87×2;20 windows,12 plain M4 holes,12 optional rack slots; four R5 outer corners; raw stainless sheet finish | [Q-M03 plate ZIP](output/submission/Q-M03/RM10-Q-M03-FACEPLATE.zip), [drawing](output/pdf/RM10-Q-M03-FACEPLATE.pdf) |
| R7 radiator plate | 304 stainless,482.6×444.5×2; four NF-A20 positions,68 fixing openings,10×2 cable notch; four R5 outer corners; raw stainless sheet finish | [R7-M01 ZIP](output/submission/R7-M01/SN1260-R7-M01-PLATE.zip), [drawing](output/pdf/SN1260-R7-M01-PLATE.pdf) |

The manifold has20 front ports at40×40 mm pitch,4 side ports and4 rear ports aligned with the outermost front pairs. Side- or rear-fed infrastructure frees all ten front pairs for loads. Topology is parallel-only, without internal grouping or a rear cover. Fittings and plugs use their own face seals.

Q-M01 incorporates the operator's shorter retention detail: **10 mm full M4 thread after entry,13 mm pilot plus drill point**. Assembly uses **M4×10** button screws, initially dry without Loctite. [Assembly instructions](docs/assembly-Q.md) are separate from manufacturing drawings. This is a prototype mechanical definition, not a pressure/load/creep-rated release.

- [Three-part recap](docs/three-part-recap.md) · [JLC requirements and final-review items](docs/jlc-final-review.md) · [submission index](output/submission/current-three-parts/README.md).
- [Design/interfaces](docs/design.md) · [Q rear ports](docs/revision-Q-rear-ports.md) · [current product/studio views](docs/product-views.md) · [Koolance source geometry](docs/koolance-qd3-studio-integration.md).
- [StarTech25U scene](docs/context-25U.md) · [radiator assembly](docs/radiator-rack-plate.md) · [radiator load assessment](docs/radiator-load-assessment.md).
- [M4 sizing](docs/Q-retention-sizing.md) · [torque/creep and threadlocker research](docs/Q-torque-and-creep.md) · [POM/coolant](docs/pom-coolant-assessment.md).
- [Rebuild commands](docs/rebuild.md) · [revision register](docs/iterations.md) · [output guide](output/README.md) · [project instructions](AGENTS.md).

Sources: `cad/iterations/Q-rear-ports.json` derives from retained P CAD; `cad/manufacturing/Q-M04.json` adds the twelve C0.5 ×45° slab-edge chamfers to Q-M01 manufacture; `cad/assembly/Q.json` defines assembly choices. Faceplate corner detail is `cad/manufacturing/Q-M03.json`. Radiator sources are `cad/radiator/R7.json` and `cad/manufacturing/R7-M01.json`. Threads in STEP are tapping pilots; the matching drawings specify finished threads. Historical outputs remain identifiable by their own revision and are not current supplier files.
