# Q-M04 POM body fabrication issue

Issued 16 September 2026. Part **RM10-Q-M04-BODY** supersedes Q-M01 for the accepted new-order pack. Its twelve main-block outside edges have **C0.50 ±0.10 mm ×45° ±1° chamfers**, modelled in STEP. The eight triangular corner flats follow the model. All other geometry and manufacturing requirements are retained.

Use `output/submission/Q-M04/RM10-Q-M04-BODY.zip`: one single-part STEP and matching three-sheet A3 PDF. Thread cylinders represent tapping pilots; the PDF specifies finished threads. This is a CNC part, not sheet metal.

- Black unfilled declared POM-C or POM-H machining stock; 410 ×87 ×40 mm main slab and twenty Ø28 ×3 mm front bosses, 43 mm overall depth.
- Twenty front, four end and four rear G1/4 female ports; 8 mm minimum full thread after entry; ISO 228-1, gauged to ISO 228-2. Two Ø11.8 continuous galleries. Follow the drawing for all pilot depths and drill points.
- Twelve M4 ×0.7-6H blind retention holes; 10 mm minimum full thread after entry, Ø3.3 ×13 mm full-diameter pilots plus 118° points. Entry Ø4.4 ×90° included, 0.55 mm nominal depth. Gauge to ISO 1502.
- Retain R1 boss roots, C0.5 ×45° boss lips and all G1/4 entry chamfers. The new perimeter chamfer applies only to the twelve outer slab edges.
- Preserve the specified front, rear and end sealing lands and front mounting plane. Ra ≤1.6 µm and local flatness ≤0.05 mm on seal lands; other finishes, datum flatness and coordinates per PDF.
- Other unspecified external edges: break 0.20 mm maximum. No internal bore/cross-hole deburring operation; clean and flush loose chips. Deliver clean, dry and unmarked.

STEP comparison confirms only the slab-perimeter chamfers remove material: 267.833 mm³ total. Every curved face, hole and boss feature is unchanged, and the specified sealing lands and M4 bearing areas are outside the removed volume. Finished solid is valid; no material is added. The drawing includes an enlarged edge detail and explicit perimeter call-out.

Rebuild using `.venv/bin/python scripts/prepare_Q_body_issue.py`, then `python3 scripts/draw_Q_production.py --body-issue Q-M04 --body-only` with ReportLab. Render and inspect all three PDF sheets, then run `python3 scripts/package_Q_body_issue.py` with pypdf. The body preparation also refreshes the separate reference assembly with the current Q-M03 faceplate; run it after faceplate preparation.

The operator accepted the complete Q-M04/Q-M03/R7-M01 set on 16 September 2026 and authorised a **separate new JLC order**, superseding the earlier hold. Submitted for file review on 16 September after explicit confirmation of UPS shipping at US$71.99. Prior material, finish and goods metadata were reused. No payment was made. The operator subsequently reported clearing the original order; preserve its fabrication archives. [New-order submission record](jlc-order-2026-09-16.md). On 17 September 2026, the operator supplied a JLC timeline screenshot showing all three current parts Approved and the batch awaiting payment. No review comments are shown. The screenshot does not establish the final reviewed prices or machining route. See [approval record](jlc-order-2026-09-16.md#supplier-approval--17-september-2026). Assembly instructions remain outside the fabrication ZIP.
