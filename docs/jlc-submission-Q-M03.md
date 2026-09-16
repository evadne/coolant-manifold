# Q-M03 manifold faceplate submission guide

Issued 16 September 2026. **RM10-Q-M03-FACEPLATE** supersedes Q-M02 with four R5 external outline corners; every opening and fixing position is retained; the current companion POM body is **RM10-Q-M04-BODY**, which adds C0.5 slab-edge chamfers while retaining all threads and mating positions.

Use `output/submission/Q-M03/RM10-Q-M03-FACEPLATE.zip` as one sheet-metal part. It contains matching-name STEP, DXF and two-sheet A3 PDF. The STEP/DXF model four R5.00 ±0.10 mm external outline corners. Compared with the submitted square-corner faceplate, only 42.920 mm³ is removed; no material is added. Nominal mass is 0.394607 kg. The minimum opening-to-outer-profile clearance remains 1.90 mm.

- Material: 304 / EN 1.4301 stainless, 482.6 ×87 ×2 mm, raw sheet finish on both broad faces; no brushing, polishing, coating or markings.
- All non-reference cut dimensions, including hole diameters, slot sizes, profiles and all X/Z coordinates: **±0.10 mm**. Thickness: 2.00 ±0.10 mm.
- W01–W20: Ø32.00 ±0.10 mm windows. H01–H12: Ø4.50 ±0.10 mm plain through holes. R01–R12: 10.00 ±0.10 ×7.00 ±0.10 mm slots; end radius half finished width.
- Free-state flatness: **0.30 mm maximum**, unchanged and separate from dimensional tolerances.
- Standard grinding and deburring on both faces; no specified chamfer or face-edge round size. Complete burr removal is not guaranteed, consistent with the operator-accepted JLC faceplate limitation.
- No tapped holes, countersinks, bends or welds. Manufacturing instructions only; assembly remains in the separate Q assembly guide.

The twelve hole positions and all nominal diameters remain unchanged. The earlier proposed Ø4.5 minimum-hole condition is not retained: the new specification allows Ø4.40–4.60 mm. The [fit assessment](Q-faceplate-as-drawn-capability.md) and [operator acceptance](jlc-feedback-2026-09-16.md#operator-acceptance) are engineering records outside the fabrication ZIP.

The operator accepted the complete Q-M04/Q-M03/R7-M01 set on 16 September 2026 and authorised a **separate new JLC order**, superseding the earlier hold. Submitted for file review on 16 September after explicit confirmation of UPS shipping at US$71.99. Prior material, finish and goods metadata were reused. No payment was made. The operator subsequently reported clearing the original order; preserve its fabrication archives. [New-order submission record](jlc-order-2026-09-16.md). Assembly instructions remain outside the fabrication ZIP.

Rebuild: `.venv/bin/python scripts/prepare_Q_faceplate_issue.py --issue Q-M03`, then `python3 scripts/draw_Q_production.py --faceplate-issue Q-M03 --faceplate-only`. Render and inspect both sheets, then run `python3 scripts/package_Q_faceplate_issue.py --issue Q-M03`. Use a Python runtime with ReportLab/pypdf for the final two commands.
