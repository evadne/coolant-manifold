# Current source index

This index identifies the references already reviewed on 14–15 September 2026. Documentation grooming does not constitute a new supplier availability check. Manufacturer models/drawings are integration references; our current geometry is defined by P and R6 source parameters and matching deliverables.

| Topic | Source and local evidence |
|---|---|
| EK inspiration and height | [EK Pro portfolio, 2CPU 8GPU](https://www.ekwb.com/shop/mediaset/EK-PRO-Portfolio-2025-Q4.pdf): 326 ×57 ×36 mm, acetal/stainless. Exact resin C/H and port pitch were not established. The project adopts parallel-only topology, not EK's selectable grouping. |
| Current QD pair | Koolance [QD3-MTG4](https://koolance.com/quick-disconnect-no-spill-coupling-male-threaded-g-1-4-qd3-mtg4) and [QD3-FT10X13](https://koolance.com/quick-disconnect-no-spill-coupling-female-for-10mm-x-13mm-3-8in-x-1-2in-qd3-ft10x13). Original STEP/PDF files and hashes in `docs/references/koolance-qd3/`; see [integration notes](koolance-qd3-studio-integration.md). |
| Manifold button screws | [Westfield WF2237, M4 ×16 ISO 7380](https://www.westfieldfasteners.co.uk/Bolts-Screws-Metric/Hex-Button-Screw-M4x16-Stainless-Steel.html): A2 reference. Current P uses plain holes; DIN 7991/DIN 965 countersunk alternatives belong to older designs. |
| G1/4 tooling | [Völkel G1/4 ×19 tap](https://voelkel.com/en/machine-tap-din-5156-form-b-hsse-g-bsp-1-4-x-19/78514): 11.8 mm core-hole recommendation. Parallel G1/4 nominal major diameter 13.157 mm; drawings supply actual machining call-outs. |
| Rack geometry | [Penn Elcom panel drawing](https://www.farnell.com/datasheets/1843559.pdf), [Keysight rack guide](https://docs.rs-online.com/4a5b/0900766b80e686f6.pdf). Actual rails and hardware govern installed clearance. |
| POM, coolant and cleaning | [POM assessment](pom-coolant-assessment.md), [Blitz overrun plan](blitz-overrun-qualification.md) and their manufacturer/SDS references. Both unfilled POM-C and POM-H remain candidates. |
| Pump pressure | [D5 pressure basis](d5-pressure.md): dated Aqua Computer, EK and Xylem sources; no manifold pressure rating inferred. |
| Radiator | [Alphacool 14351 datasheet](https://download.alphacool.com/datasheet/ENG_14351_Alphacool_NexXxoS_XT45_Full_Copper_1260mm_SuperNova_Radiator_datasheet.pdf), [manufacturer mesh](https://3dcenter.alphacool.com/stl/14351_0.stl), retained in `docs/references/`. |
| Fans and nuts | [Noctua NF-A20 downloads](https://www.noctua.at/en/products/nf-a20-pwm/downloads), retained public CAD, drawing and README under `docs/references/noctua-nf-a20/`; [Westfield DIN 934 dimensions](https://www.westfieldfasteners.co.uk/Standards/Nut-Hex-M.pdf). Public fan CAD is not for performance simulation or manufacture. |
| Fan splitter | [Watercool MO-RA X-Splitter SKU60327](https://shop.watercool.de/MO-RA-X-SPLITTER-FOR-NOCTUA-NF-A20_1), operator fit report and [spacing assessment](radiator-x-splitter-fit.md). |
| Plate material/FEA | [Outokumpu Core datasheet](https://www.outokumpu.com/-/media/files/products/core/outokumpu-core-range-datasheet.pdf), [CalculiX](https://www.dhondt.de/), [Gmsh](https://gmsh.info/doc/texinfo/); [current load summary](radiator-load-assessment.md). |
| JLC fabrication | [R6-M01 guide](jlc-submission-R6-M01.md) links the reviewed sheet-metal format, material and design guidelines. [Manufacturing status](manufacturing.md) separates this current pack from the missing P issue. |
| Host/PCIe context | [Current StarTech25U plan](context-25U.md); [archived source review](archive/context-24U-O-M02.md) contains the SilverStone/c-payne references and unresolved switch-board selection. |

Older QD3-MSG4/FS10X16 drawings, rear-cover rings, wetted stainless-cover studies and alternative mounting research remain historical references. They do not override the current QD3-MTG4/FT10X13 choice, long-bore topology, dry faceplate or plain-hole fasteners. See [archive](archive/README.md).

## PVC bending and formulation

See [the rod-model material basis](pvc-routing-physics.md) for Koolance dimensions/Shore80A, the Gent hardness correlation, Blender soft-body documentation and the reviewed Mayhems Ultra Flex11/16 claims. The9.4MPa estimate is not an exact-formulation identification.

## RTX 5090 FE context refinement

The [GPU source record](references/alphacool-5090/sources.json) links the operator-selected Alphacool 5100182, manufacturer dimensioned datasheet/manual, NVIDIA stock-card dimensions and TechPowerUp front/back PCB photographs inspected through Computer Use. Published envelopes and visually estimated small details are distinguished in [the GPU context note](gpu-5090fe-context.md).

- Molex2191140001-SD revisionA cable receptacle housing and2191160001-SD revisionA1 board header: separate plug/socket reference dimensions, archived in `docs/references/alphacool-5090/`, with URLs and hashes in its `sources.json`. Header PDF acquired through Computer Use. Exact NVIDIA connector supplier unconfirmed.
