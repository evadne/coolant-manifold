# Current SuperNova radiator/fan plate — R6

R6 is the operator-approved flat rack/fan plate for Alphacool's NexXxoS XT45 Full Copper 1260 SuperNova, product 14351. It retains R4's selected plain fan holes and adds the final 10 ×2 mm cable notch. R3's tapped-hole alternative and R5's deeper notch are superseded.

The radiator is rotated to a nominal 422 mm width ×441 mm height, with its ports at the top or bottom. The custom plate replaces one stock fan plate and carries the radiator into the rack; the opposite stock plate can remain. Four front fans provide push or pull, with a second bank permitting push/pull. Front- or rear-rail mounting does not itself determine fan airflow direction.

## Plate and interfaces

| Feature | Current nominal geometry, mm |
|---|---|
| Plate | 482.6 ×444.5 ×2, 304 / EN 1.4301; 10U; approximately 1.247 kg |
| Air openings | Four 188 ×188 squares with **R50** corners; each contains a Ø188 circle |
| Fan centres | X±100, plate heights 122.25/322.25; 200 ×200 grid |
| Fan fixing holes | Sixteen Ø4.5 plain through; 170 ×170 pattern per NF-A20 |
| Radiator holes | Twelve Ø3.6 plain through; mating M3 threads are in the radiator frame |
| Rack slots | Forty optional 10 ×7 slots; two per side per U |
| Cable notch | Top centre, 10 mouth ×2 deep; four tangent R0.5 profile corners, 9 throat, 8 bottom flat |

The final [production drawing and guide](jlc-submission-R6-M01.md) control tolerances, feature coordinates, finish and R0.3–0.5 cable-contact rounding on both faces. The actual notch outline is modelled in STEP/DXF; light face-edge finishing is a separate drawing requirement. No bending, tapping, countersinking, applied coating or product markings.

## Hardware and assembly

| Interface | Hardware |
|---|---|
| Four NF-A20 fans | Sixteen M4 ×40 ISO 7380-1 A2 button-head screws, thirty-two M4 washers Ø9/Ø4.3/0.8, sixteen DIN 934 M4 nuts (AF7, 3.2 high) |
| Radiator frame | Twelve M3 screws with compact heads, maximum Ø5.6 ×2.4, without washers; choose length from actual frame engagement and blind depth |
| Rack | Suitable screws, washers and cage nuts for the actual rails; choose which optional slots to secure |

Accepted sequence:

1. Fit fans to the plate. Button heads and one washer per screw sit on the core side; the second washer and nut sit outside the fan face. Hold the rear hex socket while tightening.
2. Fix the populated plate to the radiator through the twelve M3 clearance holes.
3. Mount the assembly onto the rack.

The reference radiator has a nominal 6.5 mm gap from plate seating face to core. A 2.2 mm button head and 0.8 mm washer occupy 3 mm, leaving 3.5 mm nominal clearance. Outward screw tips avoid consuming that core clearance as fan pads compress. Actual hardware and frame dimensions still govern the first-article fit. The plain nuts are not self-locking; select an appropriate retention method without silently changing the nut height or screw stack.

Rotate the right-hand fans 180° in their plane to bring cable exits towards the centre. This is not airflow reversal. Nominal fan frames meet at 200 mm centres; the supplier CAD is an integration reference, not a worst-case tolerance guarantee. Fan CAD and cavity/fastener evidence are retained in [the integration verification](../output/radiator-fan-integration/verification.json).

The Watercool MO-RA X-Splitter is supported by the operator's physical fit experience with Alphacool's same fan spacing. Mount and insulate it using nonconductive double-sided tape; see the brief [splitter notes](radiator-x-splitter-fit.md). No added mounting holes are required.

## Load basis and files

The [current load summary](radiator-load-assessment.md) updates the equipment budget to R6's plate mass and identifies R4's 15 kg payload shell calculations as baseline evidence. No new R6 FEA or complete-assembly load rating is claimed. The pump/reservoir may be attached behind the radiator via an existing 140 mm fan-hole adapter, or supported separately; that assembly choice remains open.

Use [R6-M01](../output/submission/R6-M01/SN1260-R6-M01-PLATE.zip) for the radiator part, [current plate views](product-views.md) for the notch, and [rebuild commands](rebuild.md) for regeneration. R4's populated views still illustrate the retained fan/hardware stack, but omit the notch. [Archived R3/R4 notes](archive/radiator-fan-plates-R3-R4.md) retain the original comparison, references and calculation details.
