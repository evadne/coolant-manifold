# O-M02 in a 24U open GPU workstation

This use-case study places the issued manifold in a short-depth open frame, above a separate host computer and below an exposed eight-GPU tray. It is an illustration of a modular riser-based workstation, not a proprietary eight-GPU server. O-M02 manufacturing files remain unchanged.

## Racking order

Rack units count upwards from the bottom. The proposed allocation is:

| Position, top to bottom | Allocation | Contents |
|---|---|---|
| U21–U24 | 4U | Open service / spare space |
| U15–U20 | 6U | Eight single-slot waterblocked GPUs on individual powered risers, mechanical retention and a PCIe switch-board envelope |
| U13–U14 | 2U | O-M02 parallel coolant manifold |
| U9–U12 | 4U | SilverStone RM46-502-I-style host, with motherboard I/O and PCIe brackets facing the manifold service side |
| U1–U8 | 8U | Reserved cooling / power equipment space, left empty in this first study |

The illustrative frame is 600 mm deep overall, with 500 mm between rail planes. The host envelope is 440 ×456 ×176 mm (width ×depth ×height); the GPU blade envelope is approximately 19 mm thick including PCB, 270 mm long and 132 mm high. GPU centres are 40 mm apart. **Single-slot thickness does not require single-slot spacing:** the extra gap aligns each card with a manifold pair and leaves room for servicing. These GPU dimensions are study assumptions, not a selected waterblock drawing. The six-unit GPU allocation includes cable/hose access above the cards; it does not imply the cards themselves are six units tall.

The shelf and host have illustrative four-post supports. Selection of commercial rack rails, rear cable clearance, shelf loading and exact waterblock/terminal envelopes remains an installation detail. A 456 mm chassis envelope inside a 600 mm frame does not establish compatibility with a particular telescopic rail kit.

## Coolant and data connections

- Front manifold pairs 1–8 each feed one GPU and receive its return. All eight GPU branches are parallel; there is no daisy chain, GPU bridge or internal grouping.
- Pair 9 feeds the host's CPU/chassis loop through **two bulkhead fittings in a PCIe slot bracket** on the front-accessible expansion side. The bracket is an added liquid-cooling accessory, not a built-in SilverStone coolant feature.
- Pair 10 is spare, shown with shut male quick-disconnect references.
- The left side supply/return ports connect to external cooling infrastructure; the right side ports remain plugged. Pump/reservoir/radiator hardware is not selected or thermally sized here. The lower eight units remain available for it and dedicated GPU power equipment.
- Blue and amber identify supply/return routes in the illustration. Purple identifies PCIe cabling; black represents auxiliary GPU power. Colours are drawing aids, not specified coolant colours or product markings.
- The host has one **logical PCIe x16 uplink** to the switch arrangement; GPUs attach through individual risers. The sketch does not imply eight independent x16 links back to the CPU or full simultaneous x16 host bandwidth per GPU. The host connection is explicitly a **PCIe x16 to two MCIO 8i host adapter**, with **two separate eight-lane cables** to the switch. Together they carry one x16 link; they do not represent two independent x8 hosts. The adapter is used in x16 mode with matching lane ordering at the switch. Both [passive](https://c-payne.com/products/mcio-pcie-gen5-host-adapter-x16-passive) and [retimed](https://c-payne.com/products/mcio-pcie-gen5-host-adapter-x16-retimer) c-payne adapters provide this connector arrangement; exact generation, SKU and cable length remain to be selected.

## Product references and limits

The operator recalled RM46-502. The RM46-502-I matches the front-accessible expansion-slot and interchangeable-component description. SilverStone's manufacturer-authored [manual, available through this mirror](https://manualsfile.com/product/k65g9ofmcnk.html) describes the front/rear component interchange and chassis layout. Its specification lists the 440 ×176 ×456 mm envelope. The rendered exterior is a simplified envelope with recognisable I/O and slot brackets, not a detailed manufacturer CAD model.

The requested **one x16 uplink / eight x16 downlinks on one c-payne board** has not been verified. The current documented [c-payne PM50100 board](https://c-payne.com/products/pcie-gen5-mcio-switch-100-lane-microchip-switchtec-pm50100) is 110 ×150 mm and defaults to an x16 uplink plus five x16 and one x4 downstream connection. Its 100-lane count cannot provide 16 +8×16 =144 electrical lanes on that single switch. The [Gen4 catalogue](https://c-payne.com/collections/pcie-packet-switch-adapters-gen4) lists four- and five-x16 downstream products. These references inform the visual style of the exposed board; the eight-endpoint switch-board envelope in this study is explicitly conceptual. Confirm the intended board or switch topology before designing its mounting holes or ordering risers/cables.

The [c-payne vertical device adapter](https://c-payne.com/products/mcio-pcie-gen5-device-adapter-x8-x16) supports single-width placement and uses two MCIO 8i inputs for an electrical x16 output. Powered risers, auxiliary GPU power, switch cooling, firmware and host enumeration need to be selected together; this sketch is not an electrical BOM.

## Files and method

- [Context sketch](../output/context-24U/03-context-sketch-v3.png): generated with the built-in image-generation tool using the Blender context views as references. [Initial prompt](../output/context-24U/sketch-prompt.txt), [dimension correction](../output/context-24U/sketch-edit-prompt.txt), and [dual-MCIO update](../output/context-24U/sketch-mcio-prompt.txt).
- [CAD-based context view](../output/context-24U/01-rack-context.png) and [front elevation](../output/context-24U/02-front-layout.png).
- [Editable Blender scene](../output/context-24U/24U-context.blend), [layout data](../output/context-24U/layout.json), and `scripts/render_context_24u.py`.

The manifold uses the issued O-M02 CAD meshes: 410 mm body, 40 mm slab, 4 mm bosses, 3 mm faceplate, twenty front ports at 40 ×40 mm pitch and four end ports. No surface text, lines or other markings are added to the manifold. Context equipment, hoses and fittings are illustrative. The generated sketch may simplify small features; the CAD-based views and O-M02 manufacturing package control the actual manifold geometry.

Sources checked 15 September 2026. No purchases, enquiries or changes to the finalised JLC package were made.
