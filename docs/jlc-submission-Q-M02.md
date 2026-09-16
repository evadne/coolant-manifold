# Q-M02 manifold faceplate submission guide

Issued 16 September 2026. **RM10-Q-M02-FACEPLATE** replaces the Q-M01 faceplate specification only. The accepted Q geometry is unchanged; the POM body remains **RM10-Q-M01-BODY**, with its existing threads, positions and finishes.

Use `output/submission/Q-M02/RM10-Q-M02-FACEPLATE.zip` as one sheet-metal part. It contains matching-name STEP, DXF and two-sheet A3 PDF. The STEP/DXF are byte-identical to the submitted Q-M01 geometry, renamed for this manufacturing issue.

- Material: 304 / EN 1.4301 stainless, 482.6 ×87 ×2 mm, raw sheet finish on both broad faces; no brushing, polishing, coating or markings.
- All non-reference cut dimensions, including hole diameters, slot sizes, profiles and all X/Z coordinates: **±0.10 mm**. Thickness: 2.00 ±0.10 mm.
- W01–W20: Ø32.00 ±0.10 mm windows. H01–H12: Ø4.50 ±0.10 mm plain through holes. R01–R12: 10.00 ±0.10 ×7.00 ±0.10 mm slots; end radius half finished width.
- Free-state flatness: **0.30 mm maximum**, unchanged and separate from dimensional tolerances.
- Standard grinding and deburring on both faces; no specified chamfer or face-edge round size. Complete burr removal is not guaranteed, consistent with the operator-accepted JLC faceplate limitation.
- No tapped holes, countersinks, bends or welds. Manufacturing instructions only; assembly remains in the separate Q assembly guide.

The twelve hole positions and all nominal diameters remain unchanged. The earlier proposed Ø4.5 minimum-hole condition is not retained: the new specification allows Ø4.40–4.60 mm. The [fit assessment](Q-faceplate-as-drawn-capability.md) and [operator acceptance](jlc-feedback-2026-09-16.md#operator-acceptance) are engineering records outside the fabrication ZIP.

Prepared locally for revised submission. Existing supplier reference: **SMS2609163000694-6347288A**. No replacement upload or supplier acknowledgement is recorded by packaging. Original Q-M01 submitted archives remain intact; see [quotation history](jlc-quotation-2026-09-15.md).

Rebuild: `python3 scripts/prepare_Q_faceplate_issue.py`, then `python3 scripts/draw_Q_production.py --faceplate-issue Q-M02 --faceplate-only`. Render and inspect both sheets, then run `python3 scripts/package_Q_faceplate_issue.py`. Use a Python runtime with ReportLab/pypdf for the final two commands.
