# SuperNova rack plate R1

> **Historical reference — superseded.** This page describes an earlier design or assessment. Its recommendations and “current” labels apply only to that snapshot. Use the [current project guide](../../README.md) and [three-part recap](../three-part-recap.md) for P / R6.


R1 implements the operator's replacement front fan plate in **3 mm 304 / EN 1.4301 stainless steel**. It is a separate radiator accessory, not a change to manifold O-M02. It replaces the front removable plate; the original opposite plate still carries the fans. No bending, welding, tapped plate holes or countersinks are required.

## Geometry

- Outside: 482.6 ×442.6 ×3 mm, R2 outer corners. This is a nominal 10U panel with 0.95 mm clearance at each rack-unit boundary.
- Four 188 ×188 mm airflow openings, R8 corners, on 200 mm centres. The central vertical and horizontal webs are 12 mm wide. The cut area is 141,156 mm², 88.2% of the nominal 400 ×400 mm core face; this is geometric open area, not a thermal-performance claim.
- Twelve Ø3.6 through-holes accept M3 radiator retention screws. Their two columns are 407 mm apart. All twelve centres were checked against the manufacturer's M3 pilot-cylinder geometry, distinct from the fan-only holes.
- Twelve horizontal 10 ×7 mm rack slots: six available positions per side, 465.1 mm between column centres. Proposed installation uses four screws per side at the outermost and central pair of rows; the other four slots are optional.
- Use A4 M3 pan-head screws with flat washers up to 7 mm OD for radiator retention. M3 ×6 is an initial length candidate only: a 3 mm plate and 0.5 mm washer would leave 2.5 mm reach. Verify engagement and safe insertion depth against the actual radiator. Do not use 30 mm fan screws without fans.
- Rack screws remain the size required by the rack, typically M6 with suitable cage nuts and washers. The manifold's M4-only retention requirement does not change Alphacool's M3 interface.

CAD/drawing coordinates are X horizontal, Y upwards from the plate bottom, Z through the 3 mm sheet. The radiator centre is X0 / Y221.3. Its manufacturer mesh uses X0 / Z212, so plate Y = mesh Z +9.3. The radiator is 422 mm wide and 441 mm high with ports at the top or bottom. The studio model shows four illustrative 200 ×30 mm fans on the opposite face. These fan envelopes, radiator fins and hardware appearances are simplified; the new plate itself uses its exported CAD mesh.

## Weight and load estimate

| Item | Mass |
|---|---:|
| Published radiator net weight | 4.225 kg |
| Operator's additional allowance | 2.000 kg |
| Payload carried at the radiator attachments | **6.225 kg** |
| New plate from CAD volume, density 7900 kg/m³ | **1.697 kg** |
| Total estimated rack load | **7.922 kg** |

The corresponding static forces are 61.05 N at the radiator attachment and 77.69 N total at the rack. No mass credit is taken for removing the original front plate. The 2 kg is an allowance for additional supported items, not a verified fan/coolant/hardware BOM. Items beyond that allowance, including a separately added pump/reservoir, must be added if supported by this plate.

For an explicit static screening case, put the payload centre of gravity 75 mm behind the rack plate. This produces a 4.58 Nm overturning moment. With only the four outermost rack fixings counted, symmetric sharing gives 19.42 N vertical shear per screw and 11.44 N total tension across the top screw pair. The twelve radiator screws average 5.09 N vertical shear each. Clearances, friction and stiffness affect real sharing; these are equilibrium estimates, not maximum individual loads or a structural qualification.

For identical material and cut profile, bending stiffness scales with thickness cubed: 3 mm gives eight times the stiffness of 1.5 mm. R1 also provides a continuous outer border and central cross web. The specified 3 mm is retained as the prototype choice. The radiator's own thin rails, inserts, attachment engagement and contact surfaces still form part of the load path; thicker rack sheet does not strengthen those parts. No validated deflection, shock, vibration or pull-out rating is claimed.

## Drawing and verification

The PDF defines all holes, slots, opening centres, corner radii, sheet thickness, edge deburring and proposed fabrication tolerances. Exact-cut DXF and STEP are consistent with the same parameters. The generator checks one valid solid, exported/re-imported STEP volume and dimensions, closed DXF contours/counts, hole placement and the 7.7 mm minimum straight ligament between radiator retention holes and airflow apertures.

Before fabrication, check the catalogue interface against the actual radiator revision, particularly hole locations and screw engagement. The mesh corroborates nominal positions but does not replace a toleranced supplier interface drawing. The radiator drawing's general/end-tank tolerance notes should not be silently assumed to be M3 hole-position tolerances. Top/bottom fitting clearance against the host or rack base remains a separate three-dimensional installation check. The nominal radiator body has only 0.8 mm panel-edge margin top/bottom; the panel face need not contain all fittings, but those fittings need actual free space.

Files:

- `cad/radiator/R1.json`: source parameters.
- `scripts/build_radiator_plate.py`: CadQuery, DXF, verification and mass calculation.
- `scripts/draw_radiator_plate.py`: two-sheet A3 PDF drawing using the bundled document Python.
- `scripts/render_radiator_plate.py`: Blender review, preserving previous rack context views.
- `output/radiator-R1/`: STEP, DXF, STL, verification JSON, three renders and editable Blender scene.
- `output/pdf/radiator-rack-plate-R1.pdf`: dimensioned drawing and load/assembly sheet.

## Sources

- [Alphacool 14351 datasheet, v1.007, March 2026](https://download.alphacool.com/datasheet/ENG_14351_Alphacool_NexXxoS_XT45_Full_Copper_1260mm_SuperNova_Radiator_datasheet.pdf): net weight, dimensions and plate/interface drawings. Net 4.225 kg is used, not the roughly 4.9 kg packaged weight.
- [Alphacool 14351 3D viewer](https://3dcenter.alphacool.com/view.php?product=14351) and its [manufacturer STL](https://3dcenter.alphacool.com/stl/14351_0.stl): reference copy under `docs/references/alphacool-14351-manufacturer.stl`; SHA-256 recorded in verification JSON. Its fine details are reference geometry, not a request to manufacture the radiator.
- [Alphacool installation manual](https://download.alphacool.com/manual/14351_Alphacool_NexXxoS_XT45_Full_Copper_1260mm_SuperNova_Radiator_Manual.pdf): removable plate and fan assembly.
- [Outokumpu Core range datasheet](https://www.outokumpu.com/-/media/files/products/core/outokumpu-core-range-datasheet.pdf): 304 density 7.9 kg/dm³, elastic modulus 200 GPa at 20°C.

Checked 15 September 2026. Prototype design only; no supplier submission or order made.

The subsequent [thickness assessment](radiator-plate-thickness.md) proposes 2 mm as the next prototype candidate, saving 566 g. R1 remains the preserved 3 mm drawing; the simplified local stress check does not qualify whole-assembly stiffness or the radiator attachment.
