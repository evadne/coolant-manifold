# Q manifold assembly - first article

Current reference assembly uses the unchanged Q-M01 POM body and Q-M03 faceplate with R5 outside corners. Fixings, port positions and assembly procedure are retained.

**Assembly document, not a supplier manufacturing drawing.** Applies to RM10-Q-M01-BODY and RM10-Q-M01-FACEPLATE. Fabrication and JLC requirements are in [the manufacturing guide](jlc-submission-Q-M01.md). Do not place this guide in the supplier fabrication ZIPs.

## Hardware and starting condition

- Twelve **M4 ×10 ISO7380-1 A2 stainless hex-socket button screws**, 2.5 mm key, nominal Ø7.6 ×2.2 head envelope. Plain bearing heads; no countersunk screws. No washers in the reference assembly.
- Body: M4×0.7-6H,10 mm full thread after0.55 entry,13 mm full-diameter pilot plus point. Plate2 mm. Nominal screw insertion8 mm;5 mm spare to the cylindrical pilot bottom. Confirm actual screw length and tip form.
- First assembly **dry, without Loctite, other threadlocker or added lubricant**. Adhesive options remain unselected; do not use generic Loctite243 on POM by default.
- Bought-in G1/4 fittings/plugs seal with their own compatible face O-rings. No threadlocker or thread seal tape is specified on the BSPP fitting threads. The separate fitting manufacturer's assembly instructions govern those interfaces.

The reference assembly STEP and individual M4×10 screw are under `output/assembly/Q/`. Product/studio images show the same head envelope; hidden screw shanks are omitted in Blender. The former Westfield WF2237 ×16 reference establishes head appearance only; **it is not the screw length to order for this assembly**. Select an actual compliant ×10 product.

## Sequence

1. Inspect the body for loose swarf, clean passages, intact lands and sound threads. Inspect the flat plate, burr removal and window alignment. Obtain the actual-grade record.
2. Rest the plate on the body with bosses freely entering all twenty windows. Do not pull a misaligned or distorted plate into place using screws.
3. Start all twelve screws by hand before seating any. Tighten progressively in a crossing pattern from the middle towards the ends, with the body supported.
4. For the first controlled dry trial, use **0.10 Nm as an initial test setting only** with a suitable low-range calibrated driver. Record seating and retention; this is not a validated production torque. Do not apply a generic steel M4 setting or treat “finger tight” as a measurement. Do not force a screw if it binds before the head seats.
5. Confirm plate seating and absence of free movement. Check the defined handling loads with support before installing the manifold above equipment. Establish the tested torque/retention window on matching-stock coupons and the first article; see [the calculation and test plan](Q-torque-and-creep.md).
6. Install the selected G1/4 fittings/face-sealing plugs according to their own instructions. Every unused port must be sealed or fitted with a suitable self-closing coupling. There are20 front,4 side and4 rear ports. Verify both gallery assignments; no internal grouping exists.
7. Install with rack-specific screws/cage nuts at suitable available slots and check actual side-elbow/hose clearance. The six optional positions per side are choices, not a requirement to fill all of them. Complete leak/flow and warm-retention checks before operational use.

Expected duty is inhibited computer coolant, approximately50°C maximum liquid temperature assumption. There is no tested pressure/temperature/load/creep rating. The operator's two-year EK experience supports proportionate warm-retention checks; small preload relaxation and failure to retain the manifold are different outcomes. Do not retighten during a relaxation test and hide the measured change.

The manufacturing supplier is not asked to assemble these parts, apply adhesive or set a torque. The current R6 radiator assembly order remains fans onto plate → plate onto radiator → assembly onto rack, documented separately in [the radiator assembly guide](radiator-rack-plate.md).
