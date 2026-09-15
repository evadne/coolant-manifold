# Alphacool alternatives for the 10U cooling bay

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
