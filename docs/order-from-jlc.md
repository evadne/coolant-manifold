# Order the current three parts from JLC

This guide reproduces the **Q-M04 body, Q-M03 faceplate and R7-M01 radiator plate** fabricated for this project. Use one of each unless you deliberately want another quantity. You do not need to run the generators or obtain the historical project revisions.

For changed designs, first follow [the new-revision workflow](new-revision.md). Its generated release README supplies the new ZIPs and per-part metadata; the upload/account/shipping process below still applies.

## Download exactly these bundles

| Part | Download | JLC category | Material | Finish | Threads |
|---|---|---|---|---|---|
| Manifold body | [RM10-Q-M04-BODY.zip](../output/submission/current-three-parts/RM10-Q-M04-BODY.zip) | CNC machining | POM (Black); unfilled POM-C or POM-H declared per drawing | No surface finish | Yes: 28 G1/4 + 12 M4 |
| Manifold faceplate | [RM10-Q-M03-FACEPLATE.zip](../output/submission/current-three-parts/RM10-Q-M03-FACEPLATE.zip) | Sheet Metal | Stainless Steel 304 | No surface finish; raw both faces | No |
| Radiator plate | [SN1260-R7-M01-PLATE.zip](../output/submission/current-three-parts/SN1260-R7-M01-PLATE.zip) | Sheet Metal | Stainless Steel 304 | No surface finish; raw both faces | No |

These direct links select the delivered fabrication revisions, not the original order that was superseded. [Machine-readable selection and hashes](../cad/current-release.json) and [pack checksums](../output/submission/current-three-parts/SHA256SUMS.txt) identify the same files. On GitHub, open each file and use Download raw file; do not save its HTML preview as a ZIP.

## Submit for quotation

1. Start a new JLC quotation. Upload the body under CNC machining and the two plates under Sheet Metal. The original process accepted a separate ZIP per part; if the interface instead requests separate files, extract and attach all members of that part's ZIP.
2. Select the table's materials, finish and quantity. The body was quoted with threads enabled, Standard appearance and ±0.05 mm as the tightest tolerance selector; the attached PDF carries the actual feature-specific requirements. Both steel drawings specify ±0.10 mm cut dimensions/coordinates and separate flatness requirements. Do not mark either steel plate as tapped.
3. Verify that the **matching PDF accompanies every STEP**. Attach the body PDF in the additional tolerance-drawing field when offered. Steel ZIPs also contain matching DXFs. STEP threads are represented by pilot cylinders: manufacturing the STEP as plain bores would not reproduce this part.
4. Use the part remarks below. For goods metadata, the original body description was “Plastic coolant manifold”; steel was “Stainless steel Rectangular Plate”, HS 732690. Confirm the classifications offered for your own order and destination.
5. Choose review before payment where offered. Have JLC assess the actual submitted PDFs, including the two Ø11.8 × 410 mm galleries and external finish requirements. Review any proposed deviation against the specific part drawing.
6. Compare current shipping charges. The historical UPS choice was destination- and date-specific; it is not a reusable shipping quotation. Inspect the reviewed price before paying.

Portal labels and available options may change. This procedure records the successful September 2026 route, not a claim of live UI verification.

## Part remarks

The following are the submitted manufacturing remarks, retained so another user can reproduce the same request. The PDFs remain the detailed fabrication definition.

**Body**

```text
Q-M04 PDF governs.12 edges C0.50+/-0.10 x45deg+/-1deg;8 corner flats per STEP.Declare black unfilled POM-C/H.28 G1/4+12 M4 threads;STEP pilots.External deburr only;flush chips.Confirm D11.8x410 galleries/deviations.
```

**Manifold faceplate**

```text
Q-M03 PDF/DXF govern. Raw 304 both faces; no brushing/polishing. Cut sizes/coordinates +/-0.10mm; four R5 corners; plain holes. Standard grinding/deburring accepted; no complete burr-removal guarantee. Flatness 0.30mm max.
```

**Radiator plate**

```text
R7-M01 PDF/DXF govern. Raw 304 both faces; no brushing/polishing. Cut sizes/coordinates +/-0.10mm; four R5 corners; plain holes. Flatness 0.50mm max. External edge finishing incl cable-contact rounds per PDF.
```

## What this order reproduces

The JLCCNC first article passed the operator's manifold dimensional/thread fit checks. The delivered steel has slight sharpness; its edge-finish adequacy remains an open finding. **Ordering the same pack repeats the existing finish requirement, not a newly improved deburring specification.** The faceplate concession does not waive the radiator's separate cable-contact rounding. If you want a different edge finish, agree and document the changed requirement rather than silently treating it as part of these released files. See [the JLCCNC report](jlc-first-article.md).

The radiator plate is delivered but not yet checked against a spare Supernova. Bought-in fittings, plugs, screws, fans and radiator are excluded from these three custom-part ZIPs. Use the separate [manifold](assembly-Q.md) and [radiator](radiator-rack-plate.md) assembly guides.

September 2026 displayed reviewed part prices were US$197.26 + US$9.86 + US$29.82 = **US$236.94 for one of each**, excluding shipping and destination charges. They are historical comparison data, not a current quote. [The order record](jlc-order-2026-09-16.md) retains the complete chronology.
