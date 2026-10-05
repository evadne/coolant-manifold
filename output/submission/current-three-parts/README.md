# Current three-part fabrication pack

**Canonical delivered revisions: Q-M04 body, Q-M03 faceplate and R7-M01 radiator.** To reproduce the order, download the three ZIPs below and follow [the JLC order guide](../../../docs/order-from-jlc.md). These are byte-identical copies of the revision-specific bundles. [The canonical manifest](../../../cad/current-release.json) selects their paths and hashes. Older outputs remain historical unless explicitly identified as shared dependencies. This index verifies files; it does not submit or pay for an order.

| Part | Fabrication bundle | Process |
|---|---|---|
| Q POM body | [RM10-Q-M04-BODY.zip](RM10-Q-M04-BODY.zip) | CNC milling, drilling and tapping; black unfilled declared POM-C or POM-H |
| Q faceplate | [RM10-Q-M03-FACEPLATE.zip](RM10-Q-M03-FACEPLATE.zip) | 2 mm 304 flat sheet; plain holes and raw sheet finish on both faces |
| R7 radiator plate | [SN1260-R7-M01-PLATE.zip](SN1260-R7-M01-PLATE.zip) | 2 mm 304 flat sheet; plain holes and raw sheet finish on both faces |

Each ZIP contains a same-name single-part STEP and PDF; the steel parts also have a DXF cut profile. The drawings define finished geometry, threads, tolerances, surface finish and inspection. STEP thread cylinders represent tapping pilots. There are eight drawing sheets across the three parts. Both steel drawings specify four R5 outside corners and ±0.10 mm cut dimensions and coordinates. Other cut profiles and fixing positions are retained. Separate flatness limits remain 0.30/0.50 mm; faceplate uses standard deburring, radiator retains its specified cable-contact edge finish.

[Verification](verification.json) records bundle integrity and consistency with the reviewed Q/R7 outputs. [Checksums](SHA256SUMS.txt) cover the index files. Operator manifold fit checks passed; the delivered radiator is operator-unverified. The [JLCCNC first-article report](../../../docs/jlc-first-article.md) records that supplier’s steel-edge sharpness finding. Repeating these ZIPs does not add an improved finishing specification.

[Manifold assembly instructions](../../../docs/assembly-Q.md), [radiator assembly instructions](../../../docs/radiator-rack-plate.md) and engineering assessments are separate project documents, outside these fabrication ZIPs. The current [product views](../../../docs/product-views.md) and [rack scene](../../../docs/context-25U.md) are review references.
