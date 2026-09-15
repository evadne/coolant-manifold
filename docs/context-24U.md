# O-M02 in a 24U open GPU workstation

This use-case study places the issued manifold in a short-depth open frame, above a separate host computer and below an exposed eight-GPU tray. It is an illustration of a modular riser-based workstation, not a proprietary eight-GPU server. O-M02 manufacturing files remain unchanged.

## Racking order

Rack units count upwards from the bottom. The proposed allocation is:

| Position, top to bottom | Allocation | Contents |
|---|---|---|
| U23–U24 | 2U | Open service / spare space |
| U17–U22 | 6U | Eight single-slot waterblocked GPUs on individual powered risers, mechanical retention and a PCIe switch-board envelope |
| U15–U16 | 2U | O-M02 parallel coolant manifold |
| U11–U14 | 4U | SilverStone RM46-502-I-style host, with motherboard I/O and PCIe brackets facing the manifold service side |
| U1–U10 | 10U | Custom front-mounted MO-RA cooling assembly: radiator, reservoir and D5 pumping, below the server |

The illustrative frame is 600 mm deep overall, with 500 mm between rail planes. The host envelope is 440 ×456 ×176 mm (width ×depth ×height); the GPU blade envelope is approximately 19 mm thick including PCB, 270 mm long and 132 mm high. GPU centres are 40 mm apart. **Single-slot thickness does not require single-slot spacing:** the extra gap aligns each card with a manifold pair and leaves room for servicing. These GPU dimensions are study assumptions, not a selected waterblock drawing. The six-unit GPU allocation includes cable/hose access above the cards; it does not imply the cards themselves are six units tall.

The lower radiator allocation is **10U = 444.5 mm**. The model shows a custom 440 mm-wide ×440 mm-high radiator body with an approximately 110 mm front-to-back envelope and nine illustrative 120 mm fans. Rack ears extend to the 19-inch mounting positions. These are space-study dimensions, not the specification of a selected stock MO-RA product; core size, fan arrangement and structural mounting remain open. The radiator face is at the rack front, with its depth extending mostly into the rack and open space behind it. The tank is now on the radiator's narrow connection side, with its window and D5 facing outwards, following the MO-RA IV mounting reference. It attaches through the upper direct port adapter and a compact lower retainer; the previous rear-offset carrier and long radiator-to-reservoir hose were incorrect and have been removed. Two fill plugs are on top. The Tank 200 body reference is 275 mm high ×84 mm across the side ×49 mm projection; the D5 envelope is approximate.

**Packaging consequence:** with the existing 440 mm-wide custom radiator body, the side-facing pump reaches X+336 mm, about 69 mm beyond the illustrative rack post's outer side. The radiator is recessed a further 60 mm on short rack stand-offs so the tank clears the front post. The 10U vertical allocation is retained, but this is an outboard pump/tank arrangement, not a width-contained rack package. A narrower/custom cooling core or a different mounting orientation would need a separate packaging decision. Do not relocate the tank behind the fins simply to conceal this issue. See the [mounting reference review](references/mo-ra-tank-mounting.md).

The server, manifold and GPU shelf move upwards by 2U together; their relative spacing and coolant branches remain the same. This reduces the top reserve from 4U to 2U.

The shelf and host have illustrative four-post supports. Selection of commercial rack rails, rear cable clearance, shelf loading and exact waterblock/terminal envelopes remains an installation detail. A 456 mm chassis envelope inside a 600 mm frame does not establish compatibility with a particular telescopic rail kit.

The GPU I/O brackets face the rack rear. Coolant terminals and 12VHPWR sockets share the opposite, non-bracket region, facing the manifold service side. The power sockets are on the top edge near that end, with straight cable leads above the plugs before routing overhead to the side power-distribution envelope. Earlier views incorrectly placed auxiliary power at the opposite end from the coolant terminals. These corrected positions represent the operator's intended GPU arrangement; exact connector positions and cable bend clearances depend on the selected card and cable.

## Coolant and data connections

- Front manifold pairs 1–8 each feed one GPU and receive its return. All eight GPU branches are parallel; there is no daisy chain, GPU bridge or internal grouping.
- Pair 9 feeds the host's CPU/chassis loop through **two bulkhead fittings in a PCIe slot bracket** on the front-accessible expansion side. The bracket is an added liquid-cooling accessory, not a built-in SilverStone coolant feature.
- Pair 10 is spare, shown with shut male quick-disconnect references.
- The left side service hoses connect to the complete MO-RA cooling assembly; the right side ports remain plugged. The schematic circuit is manifold return → radiator → reservoir → D5 pump → manifold supply. Reservoir and pumping are included functions of this assembly, not a separate unresolved subsystem. One D5 stage is illustrated; the exact modules and pump count remain selectable. No heat-rejection or hydraulic rating is inferred from the context views.
- Blue and amber identify supply/return routes in the illustration. Purple identifies PCIe cabling; black represents auxiliary GPU power. Colours are drawing aids, not specified coolant colours or product markings.
- The host has one **logical PCIe x16 uplink** to the switch arrangement; GPUs attach through individual risers. The layout does not imply eight independent x16 links back to the CPU or full simultaneous x16 host bandwidth per GPU. The host connection is explicitly a **PCIe x16 to two MCIO 8i host adapter**, with **two separate eight-lane cables** to the switch. Together they carry one x16 link; they do not represent two independent x8 hosts. The adapter is used in x16 mode with matching lane ordering at the switch. Both [passive](https://c-payne.com/products/mcio-pcie-gen5-host-adapter-x16-passive) and [retimed](https://c-payne.com/products/mcio-pcie-gen5-host-adapter-x16-retimer) c-payne adapters provide this connector arrangement; exact generation, SKU and cable length remain to be selected.

## Product references and limits

The MO-RA is treated here as a complete configured cooling assembly. Watercool documents radiator-mounted [HEATKILLER Tube reservoir adapters for MO-RA3](https://shop.watercool.de/HEATKILLER-Tube-MO-RA3-Adapter-White_1), D5 modules in its [MO-RA3 manual](https://shop.watercool.de/mediafiles/Manuals/MA_MO-RA3_A5.pdf), and a dedicated [MO-RA IV Tank with integrated D5 mount](https://shop.watercool.de/MO-RA-IV-Tank-200-D5_1). These are components of the MO-RA ecosystem; a bare radiator purchase does not by itself establish which pump/reservoir parts are supplied. The previous “pump/reservoir TBD” annotation omitted the intended integrated function and is superseded. Exact generation and accessory selection remain implementation details within the allocated assembly.

The operator recalled RM46-502. The RM46-502-I matches the front-accessible expansion-slot and interchangeable-component description. SilverStone's manufacturer-authored [manual, available through this mirror](https://manualsfile.com/product/k65g9ofmcnk.html) describes the front/rear component interchange and chassis layout. Its specification lists the 440 ×176 ×456 mm envelope. The rendered exterior is a simplified envelope with recognisable I/O and slot brackets, not a detailed manufacturer CAD model.

The requested **one x16 uplink / eight x16 downlinks on one c-payne board** has not been verified. The current documented [c-payne PM50100 board](https://c-payne.com/products/pcie-gen5-mcio-switch-100-lane-microchip-switchtec-pm50100) is 110 ×150 mm and defaults to an x16 uplink plus five x16 and one x4 downstream connection. Its 100-lane count cannot provide 16 +8×16 =144 electrical lanes on that single switch. The [Gen4 catalogue](https://c-payne.com/collections/pcie-packet-switch-adapters-gen4) lists four- and five-x16 downstream products. These references inform the visual style of the exposed board; the eight-endpoint switch-board envelope in this study is explicitly conceptual. Confirm the intended board or switch topology before designing its mounting holes or ordering risers/cables.

The [c-payne vertical device adapter](https://c-payne.com/products/mcio-pcie-gen5-device-adapter-x8-x16) supports single-width placement and uses two MCIO 8i inputs for an electrical x16 output. Powered risers, auxiliary GPU power, switch cooling, firmware and host enumeration need to be selected together; this layout is not an electrical BOM.

## Files and method

The Blender renders are the primary presentation from this point onwards. Update the scene and render it directly for design changes; separate generated sketches are no longer required.

- [Perspective context view](../output/context-24U/01-rack-context.png), [front elevation](../output/context-24U/02-front-layout.png), [rear view showing the MO-RA pump/reservoir assembly](../output/context-24U/04-rear-cooling-assembly.png), and [side-mount detail](../output/context-24U/05-tank-side-detail.png).
- [Editable Blender scene](../output/context-24U/24U-context.blend), [layout data](../output/context-24U/layout.json), and `scripts/render_context_24u.py`.
- Earlier generated sketches remain historical references only. The last is [sketch v5](../output/context-24U/03-context-sketch-v5.png); its prompts and provenance remain alongside it. They are not maintained with subsequent design changes. In particular, v5’s “pump/reservoir TBD” annotation is obsolete; use the current Blender views and this guide.

The manifold uses the issued O-M02 CAD meshes: 410 mm body, 40 mm slab, 4 mm bosses, 3 mm faceplate, twenty front ports at 40 ×40 mm pitch and four end ports. No surface text, lines or other markings are added to the manifold. Context equipment, hoses and fittings are illustrative. The context views use CAD-derived manifold meshes; the O-M02 manufacturing package controls the actual manifold geometry.

Sources checked 15 September 2026. No purchases, enquiries or changes to the finalised JLC package were made.

The operator subsequently suggested Alphacool's large NexXxoS radiators. See the [Nova/SuperNova packaging assessment](alphacool-radiator-options.md): the 1080 offers useful installation reserve, while the 1260's nominal body fit leaves fittings and tolerances unresolved. This is an alternative under assessment, not a change to the current Blender scene.
