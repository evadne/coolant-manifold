# Current three-part fabrication pack

Accepted new-order pack: Q-M04 body with C0.5 slab-edge chamfers and eight corner flats, Q-M03 faceplate and R7-M01 radiator. A separate new order was submitted for file review after the operator confirmed UPS, the cheapest quoted shipping option. The operator reports clearing the original supplier order; preserve its fabrication files as history. [New-order status](../../../docs/jlc-order-2026-09-16.md) records UI progress separately from these local packaging checks. No payment is performed by these scripts.

| Part | Fabrication bundle | Process |
|---|---|---|
| Q POM body | [RM10-Q-M04-BODY.zip](RM10-Q-M04-BODY.zip) | CNC milling, drilling and tapping; black unfilled declared POM-C or POM-H |
| Q faceplate | [RM10-Q-M03-FACEPLATE.zip](RM10-Q-M03-FACEPLATE.zip) | 2 mm 304 flat sheet; plain holes and raw sheet finish on both faces |
| R7 radiator plate | [SN1260-R7-M01-PLATE.zip](SN1260-R7-M01-PLATE.zip) | 2 mm 304 flat sheet; plain holes and raw sheet finish on both faces |

Each ZIP contains a same-name single-part STEP and PDF; the steel parts also have a DXF cut profile. The drawings define finished geometry, threads, tolerances, surface finish and inspection. STEP thread cylinders represent tapping pilots. There are eight drawing sheets across the three parts. Both steel drawings specify four R5 outside corners and ±0.10 mm cut dimensions and coordinates. Other cut profiles and fixing positions are retained. Separate flatness limits remain 0.30/0.50 mm; faceplate uses standard deburring, radiator retains its specified cable-contact edge finish.

[Supplier requirements and open fabrication questions](../../../docs/jlc-final-review.md) cover the POM stock, long-gallery drilling and specified tolerances/finishes. [Verification](verification.json) records bundle integrity and consistency with the reviewed Q/R7 outputs.

[Manifold assembly instructions](../../../docs/assembly-Q.md), [radiator assembly instructions](../../../docs/radiator-rack-plate.md) and engineering assessments are separate project documents, outside these fabrication ZIPs. The current [product views](../../../docs/product-views.md) and [rack scene](../../../docs/context-25U.md) are review references.
