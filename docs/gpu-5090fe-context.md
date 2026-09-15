# RTX 5090 FE and Alphacool 5100182 in the rack scene

The eight generic, mirrored single-slot GPU envelopes are replaced by NVIDIA GeForce RTX 5090 Founders Edition assemblies with the **Alphacool ES RTX 6000 Pro Workstation/RTX 5090 Founders Edition**, article **5100182**. Looking into the coolant ports, the main cooling block is on the left, the processor PCB is to its right and the active backplate is further right. The block covers the processor board; it is not a plate attached to the wrong face of a full-length PCB.

## Source dimensions

The [Alphacool datasheet](references/alphacool-5090/datasheet.pdf), its Figure 1 assembly drawing, and [installation manual](references/alphacool-5090/manual.pdf) govern the cooling assembly. The [source record](references/alphacool-5090/sources.json) records URLs and file hashes.

| Published feature | Dimensions, mm |
|---|---|
| Main cooler, length × height × thickness | 231.10 × 119.40 × 13.40 |
| Active backplate, length × height × thickness | 208.97 × 120.90 × 10.93 |
| Assembled cooling-body thickness | 29.68 |
| Overall length including bracket extension | 245.83 |
| Length to bracket datum | 231.97 |
| Overall height including bracket | 150.60 |
| Aggregate thickness including offset bracket | 42.07 |
| Two G1/4 port centres | 34.00 apart |
| Upper port below assembly top | 61.18 |
| Port axis to outer backplate face | 21.18 |

Alphacool calls this a **1.5-slot** assembly. The thicknesses of the loose block and backplate cannot simply be added to obtain the assembled thickness: they also enclose the boards, components and mounting clearances.

NVIDIA's [304 × 137 mm, two-slot specification](https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/) describes the original air-cooled FE card. Its cooler is removed, so that envelope is retained in the source parameters as a stock-card reference only. It is not used as a bare-PCB rectangle.

## PCB and key elements

The manual shows separate processor, PCIe-edge and display boards; this agrees with NVIDIA's [three-piece PCB description](https://www.nvidia.com/en-gb/geforce/news/rtx-50-series-graphics-cards-gpu-laptop-announcements/). The scene includes all three boards, their interconnects, three DisplayPort openings and one HDMI opening, plus the angled top-front power connection.

The operator suggested [TechPowerUp's circuit-board analysis](https://www.techpowerup.com/review/nvidia-geforce-rtx-5090-founders-edition/6.html). Its front and back photographs were inspected in the browser: they show black soldermask, a nearly square processor board, stepped lower edges, rear interconnect sockets and the angled corner power connector. These guide the visible outline and placement. The processor-board envelope is approximately **108 × 110 mm**, estimated visually within the cooler envelope, not a published board measurement. PCB thickness/stack position, 45° connector placement, small fasteners and notch details remain visual approximations. No supplier STEP was available from the reviewed configurator download list.

The model has chrome-plated copper sides and dark carbon covers. Covers and metal have separate, non-overlapping thickness intervals to avoid coincident outer faces. Product surfaces remain unmarked.

## Power plug and board socket

The former square-ish cuboids are replaced by separate compatible **Molex 219114 cable receptacle** and **219116 board header** reference geometry. These are commonly described as the cable plug and GPU socket respectively; Molex names them by contact gender. The exact connector supplier fitted to NVIDIA's board and the eventual PSU harness are not established.

The [cable housing drawing](references/alphacool-5090/power-housing.pdf), revision A, supplies the 20.85 mm flange width, 7.55 mm main housing height, 14.00 mm axial length, 3 mm power-contact pitch and 2 mm signal pitch. The separate [board-header drawing](references/alphacool-5090/power-header.pdf), revision A1, supplies its 18.85 mm width, 6.86 mm main shroud height and 9.91 mm depth. Its mated view gives 17.66 mm axial housing length, implying 6.25 mm insertion. The cable contact towers enter the header; the broad flange is at the wire end.

The scene models the stepped signal section, header shroud, latch ramp and cable latch, twelve individual power-wire exits and four smaller signal wires. The width lies in the PCB plane; the two-row thickness lies across it. Moulding details, wire insulation sizes, sleeving, connector placement and cable curves are illustrative. Hidden contacts and solder tails are omitted. This reference is for visual fit, not connector manufacture or electrical qualification.

## Registration and fit

Card spacing stays **40 mm**, giving 10.32 mm between nominal cooling-body envelopes. The 42.07 mm aggregate width includes an offset bracket; it is not a 42.07 mm-wide solid slab along the whole card. The reference bracket uses an inferred 38 mm sheet width at a rear plane beyond the neighbouring cooler body, with a 0.37 mm nominal axial gap to that body. Inter-card meshes clear in this illustration, but the undimensioned bracket profile is not a qualified physical fit.

The port midpoint and fitting face remain at their former positions. Correcting 30 mm to 34 mm GPU port spacing moves the lower port down 2 mm and the upper port up 2 mm. The new shorter card body sits on raised support crossbars to retain this interface height. These supports are illustrative; they are not a new manufactured part.

All eighteen accepted nominal hose lengths are retained explicitly in `cad/context/pvc-routing.json`. The sixteen GPU hoses are re-solved with the two adjusted terminal heights; host routing is unchanged. Free XYZ coordinates and paired-tube contact remain enabled. Manifold, radiator, rack allocation and the separate manifold side-elbow/cage-nut concern are unchanged.

## Rebuild and verification

Parameters: `cad/context/gpu-5090fe.json`. The pure coordinate definitions in `scripts/context_gpu5090.py` are shared with the rod solver and Blender generator. Rebuild using the [normal composite instructions](rebuild.md).

The generator verifies orientation, three PCB parts per card, four display sockets, 34 mm coolant pitch and cooling-body thickness, then checks inter-card mesh intersections and all existing tube/equipment clearances. Reports: `output/context-25U/gpu-verification.json`, `gpu-interface-change.json`, `pvc-equilibrium.json` and `scene-verification.json`. Small inferred details remain distinct from published dimensions in the parameters and layout record.

The current native scene and all nine rendered views are refreshed, including `09-GPU-block-detail.png` and `10-GPU-power-detail.png`. Blender remains closed after headless generation.
