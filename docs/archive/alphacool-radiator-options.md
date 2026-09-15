# Alphacool alternatives for the 10U cooling bay

> **Historical reference — superseded.** This page describes an earlier design or assessment. Its recommendations and “current” labels apply only to that snapshot. Use the [current project guide](../../README.md) and [three-part recap](../three-part-recap.md) for P / R6.


Assessment, 15 September 2026. The operator suggested a large NexXxoS radiator supplied without an external frame. These are candidate alternatives; the existing MO-RA Blender scene and O-M02 manifold remain unchanged.

The bay provides 444.5 mm nominal height (10U) and an assumed 450 mm equipment opening. The following are radiator dimensions, excluding fans, fittings, hoses, pump/reservoir and custom rack supports.

| Candidate | Published dimensions, mm | Fans | Nominal width/height remainder in the stated orientation |
|---|---|---|---|
| XT45 Nova 1080, 14349 | 378 W ×360 H ×46.5 D | 9 ×120 mm | 72 /84.5 mm total |
| XT45 SuperNova 1260, 14351, end ports sideways | 441 W ×422 H ×48 D | 9 ×140 or 4 ×200 mm | 9 /22.5 mm total |
| Same SuperNova, rotated 90°, end ports upwards or downwards | 422 W ×441 H ×48 D | Same | 28 /3.5 mm total |

Sources: Alphacool [Nova 1080](https://shop.alphacool.com/en/shop/radiators/special-sizes/rad-alphacool-nexxxos-xt45-full-copper-1080mm-nova-radiator) and [SuperNova 1260](https://shop.alphacool.com/en/shop/radiators/special-sizes/14351-alphacool-nexxxos-xt45-full-copper-1260mm-supernova-radiator). Both have three G1/4 connections and removable fan mounting plates. The [Nova fan housing](https://shop.alphacool.com/en/shop/radiators/accessories/rab-alphacool-nexxxos-nova-1080-mm-fan-box-black) is a separate accessory. A distinct frameless heat-exchanger-core SKU has not been confirmed: removable fan plates and an optional outer enclosure establish useful modularity, but do not establish that the structural casing can be discarded.

The [SuperNova manufacturer drawing](https://download.alphacool.com/datasheet/ENG_14351_Alphacool_NexXxoS_XT45_Full_Copper_1260mm_SuperNova_Radiator_datasheet.pdf), figure 3, places connection faces at the end of the 441 mm direction. As the operator clarified, rotating the radiator 90° puts these ports at the top or bottom. This is a valid arrangement to investigate: at 422 mm wide, the body leaves 14 mm nominal clearance per side when centred, and fittings no longer need to project sideways into that allowance.

The radiator body then occupies 441 mm vertically, leaving 3.5 mm total within the nominal 10U height. Top/bottom fittings therefore require a separately allocated volume beyond the body's 10U face envelope; they need not share the radiator's front plane. A proposed carrier can recess the radiator and use elbows to turn hoses into rack depth, but must include the elbows' initial projection above/below the port faces. Check that volume against the host chassis above or the rack base below; rotation alone does not establish that it is free. Do not reject this orientation merely because fittings exceed the radiator's nominal face rectangle. The drawing footer also shows end-tank allowances of ±3 mm and general tolerance ±0.75 mm; clarify their application before fixing a close-fitting carrier.

The 1080 has more generous body clearances, while the rotated 1260 remains a candidate for the next three-dimensional packaging review. A custom front carrier could support the radiator through suitable structural mounting points, with a separately mounted pump/reservoir further into the rack depth. This is a new modular assembly, not the MO-RA side-tank mounting arrangement. Preserve fan airflow and service access; do not support the radiator through its fins or infer compatibility with MO-RA accessory brackets.

Next geometry review should include the selected radiator's port positions, fittings and hose bends, fans, carrier, pump/reservoir, fill/drain access and actual rail/post geometry. Thermal adequacy for eight GPUs plus the host remains unverified and requires the intended power, fan/noise target and coolant-to-air temperature difference. No replacement is selected or ordered by this assessment.

## Replace the front fan plate with the rack plate

The operator proposes one custom front rack plate replacing the radiator's removable front fan plate, with fans on the opposite face. Adopt this as the mounting concept for the rotated SuperNova candidate. Alphacool explicitly describes interchangeable/removable plates on both faces; the stock plate drawings show 420 ×420 ×1.5 mm plates. The custom part extends to the 19-inch rack mounting positions and combines radiator attachment, airflow openings and rack ears in one plate. Retain the appropriate stock opposite plate for nine 140 mm or four 200 mm fans.

Front-to-back arrangement: rack plate with airflow apertures → radiator → retained opposite fan plate → fans within the rack. A pull arrangement can draw room air through the front apertures and radiator into the rack; preserve a clear discharge path. Port orientation stays upwards or downwards. The rack plate's width is the rack-panel width, while the radiator remains 422 mm wide behind it; the 450 mm equipment-opening assumption does not constrain the ears to 450 mm.

Reuse the radiator's actual plate attachment pattern, distinguishing it from fan-only holes. Figure 3 calls out M3 ×0.5 threads: these remain M3, independent of the manifold's M4-only plate retention. Establish the attachment coordinates and allowable screw engagement from manufacturer CAD or the actual part before releasing the custom plate. A thicker replacement needs a corresponding screw-length review, not simply longer screws without an engagement limit. Use broad airflow openings with enough connecting material to transmit the load from radiator fixings to rack ears.

The stock 1.5 mm fan plate thickness is a reference, not a rack-support specification. Size the replacement for the filled radiator, opposite fans and handling loads; verify the radiator attachment points as well as plate stiffness. This defines the proposed load path without claiming a qualified load rating. Existing Blender outputs still depict the preceding MO-RA study; no radiator manufacturing drawing has yet been issued.

The operator has now requested this part in 3 mm stainless steel, using radiator net weight plus 2 kg. [Prototype R1](radiator-rack-plate-R1.md) implements it with a dimensioned drawing, STEP/DXF and separate Blender views. The existing full 24U MO-RA scene is retained; the new radiator views are under `output/radiator-R1/`.
