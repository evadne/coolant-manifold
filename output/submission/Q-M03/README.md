# Q-M03 manifold faceplate submission guide

Issued 16 September 2026. **RM10-Q-M03-FACEPLATE** supersedes Q-M02 with four R5 external outline corners; every opening and fixing position is retained; the current companion POM body is **RM10-Q-M04-BODY**, which adds C0.5 slab-edge chamfers while retaining all threads and mating positions.

Use `output/submission/Q-M03/RM10-Q-M03-FACEPLATE.zip` as one sheet-metal part. It contains matching-name STEP, DXF and two-sheet A3 PDF. The STEP/DXF model four R5.00 ±0.10 mm external outline corners. Compared with the submitted square-corner faceplate, only 42.920 mm³ is removed; no material is added. Nominal mass is 0.394607 kg. The minimum opening-to-outer-profile clearance remains 1.90 mm.

- Material: 304 / EN 1.4301 stainless, 482.6 ×87 ×2 mm, raw sheet finish on both broad faces; no brushing, polishing, coating or markings.
- All non-reference cut dimensions, including hole diameters, slot sizes, profiles and all X/Z coordinates: **±0.10 mm**. Thickness: 2.00 ±0.10 mm.
- W01–W20: Ø32.00 ±0.10 mm windows. H01–H12: Ø4.50 ±0.10 mm plain through holes. R01–R12: 10.00 ±0.10 ×7.00 ±0.10 mm slots; end radius half finished width.
- Free-state flatness: **0.30 mm maximum**, unchanged and separate from dimensional tolerances.
- Standard grinding and deburring on both faces; no specified chamfer or face-edge round size. Complete burr removal is not guaranteed, consistent with the operator-accepted JLC faceplate limitation.
- No tapped holes, countersinks, bends or welds. Manufacturing instructions only; assembly remains in the separate Q assembly guide.

The twelve hole positions and all nominal diameters remain unchanged. The earlier proposed Ø4.5 minimum-hole condition is not retained: the new specification allows Ø4.40–4.60 mm. The [fit assessment](../../../docs/Q-faceplate-as-drawn-capability.md) and [operator acceptance](../../../docs/jlc-feedback-2026-09-16.md#operator-acceptance) are engineering records outside the fabrication ZIP.

**Held for later submission if a repeat order is needed**, by operator decision on 16 September 2026. This package records the accepted dimensional tolerances. Do not replace the current order’s files. The existing order **SMS2609163000694-6347288A** proceeds under the operator’s emailed acceptance; it is a historical reference, not an order for this new issue. No upload of this issue has occurred. Original Q-M01 submitted archives remain intact; see [quotation history](../../../docs/jlc-quotation-2026-09-15.md).

Rebuild: `.venv/bin/python scripts/prepare_Q_faceplate_manufacturing_revision.py --manufacturing-revision Q-M03`, then `python3 scripts/draw_Q_production.py --faceplate-manufacturing-revision Q-M03 --faceplate-only`. Render and inspect both sheets, then run `python3 scripts/package_Q_faceplate_manufacturing_revision.py --manufacturing-revision Q-M03`. Use a Python runtime with ReportLab/pypdf for the final two commands.
