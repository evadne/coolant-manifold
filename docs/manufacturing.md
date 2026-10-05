# Current manufacturing status

As of 5 October 2026, the canonical fabricated set is **Q-M04 body, Q-M03 faceplate and R7-M01 radiator plate**. All three parts are delivered. The operator has verified the manifold body's and faceplate's dimensions, the POM M4 holes and the G1/4 ports. The radiator plate is **operator-unverified**, pending access to a spare Supernova.

## Current files

Use [the repeat-order guide](order-from-jlc.md) for another quotation, [the fabrication index](../output/submission/current-three-parts/README.md) for downloads, and [the canonical manifest](../cad/current-release.json) for machine-readable paths and hashes. Do not choose files by a historical directory's “current” label.

| Part | Issue guide | Fabrication definition |
|---|---|---|
| Manifold POM body | [Q-M04](jlc-submission-Q-M04.md) | Chamfered slab; 28 G1/4 ports; 12 M4 threads; two long galleries |
| Manifold faceplate | [Q-M03](jlc-submission-Q-M03.md) | Raw 2 mm 304; R5 outside corners; plain holes; ±0.10 mm cut dimensions/coordinates |
| Radiator plate | [R7-M01](jlc-submission-R7-M01.md) | Raw 2 mm 304; R5 corners; plain fan/radiator holes; rounded cable notch |

The matching fabrication PDFs define finished features and inspection. STEP thread cylinders are pilots. Assembly instructions, bought-in hardware and tightening are separate: [manifold assembly](assembly-Q.md), [radiator assembly](radiator-rack-plate.md).

## Physical verification and supplier findings

The first article was made by **JLCCNC**. Smooth QD3 engagement, accepted POM corner detail and a faceplate mounting without perceptible flex are operator observations. Covered POM holding marks were accepted. Slight sharpness on the steel remains an open finish-quality finding specific to that batch. See [the JLCCNC first-article report](jlc-first-article.md).

Dimensional/fit acceptance does not imply recorded leak testing or qualification of pressure, transport loading or long-term creep. Those results have not been reported. The radiator's fit against the actual radiator and fans is still unverified. Separate side-elbow/rack-hardware clearance remains an actual-hardware concern in [the context study](context-25U.md).

## Evidence and history

- [Current design recap](three-part-recap.md): dimensions, material and interfaces.
- [Supplier requirement review](jlc-final-review.md): the reviewed process requirements and first-article checks.
- [Q-M04 machining route](Q-M04-machining-route.md): three-axis feasibility with deep-drilling capability; not JLC's actual CAM.
- [Latest order and delivery chronology](jlc-order-2026-09-16.md): approval, prices, manufacture, delivery and operator reports.
- [Original order](jlc-quotation-2026-09-15.md) and [faceplate concession](jlc-feedback-2026-09-16.md#operator-acceptance): superseded order, retained unchanged files and order-specific feedback.
- [Earlier status narrative](archive/manufacturing-status-through-2026-10-05.md): historical inspections and manufacturing issue changes.

The original order was cleared by the operator. The current parts came from the subsequent order. Neither this status record nor the repeat-order guide authorises payment or submission by an automated agent.
