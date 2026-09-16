# JLCCNC quotation submission — 15 September 2026

**Submitted for file review**, approximately 22:46 UTC, through the existing signed-in Safari session. JLC confirmed **“Your order has been submitted.”** The selected mode was **Review Before Payment**: no payment was made, PayPal automatic payment was not selected, and the site states production waits for payment. This is a quotation/manufacturability request, not supplier acceptance or a paid production release.

| Part | Supplier part reference | Qty | Route/material | Preliminary part estimate |
|---|---|---:|---|---:|
| Q-M01 body | CNC2609165002398-6347288A | 1 | CNC / POM(Black), no finish, threads YES, ±0.05 mm selection | $128.74 |
| Q-M01 faceplate | SMS2609163000694-6347288A | 1 | Sheet Metal / 304, no surface finish, threads NO | $9.86 |
| R6-M02 radiator plate | SMS2609163000690-6347288A | 1 | Sheet Metal / 304, no surface finish, threads NO | $29.84 |

References were recorded from the three-item cart immediately before combined submission. The success page was verified; a later individual order-history review state was not read successfully. [Order history](https://jlccnc.com/user-center/orders) is the supplier follow-up location. JLC says it will email the review results during business hours. No background monitoring has been arranged.

The preliminary subtotal was **$168.44**, with **$122.79** estimated DHL Express shipping to the existing saved address (**$291.23** combined). These are automatic estimates, not reviewed quotations, final landed costs or payment approval.

## Files and finish amendment

The cart was empty before uploading. After the operator elected matching **raw stainless sheet finish for both plates**, both steel PDFs and ZIPs were regenerated and checked. The two earlier steel cart entries were removed; only the current body and replacement steel bundles were submitted. Both plates retain the specified external deburring, tolerance and edge-rounding operations. No brushing, polishing or coating is requested. Geometry is unchanged.

Each upload was a single-part ZIP containing matching-name STEP and PDF; both steel ZIPs also contain DXF. The body PDF was additionally attached through the CNC tolerance drawing control. The sheet-metal UI displays the extracted STEP name and does not separately expose PDF/DXF receipt in its specification dialogue. ZIP contents and uploaded archive hashes are recorded in the [submission record](../output/submission/jlc-quotation-2026-09-15.json).

All remark fields were checked in full before saving. POM remarks request declared unfilled stock and deep-gallery feasibility; steel remarks call out drawing tolerances, raw finish and external edge finishing. The exact remarks and selected options are in the submission record. The POM product declaration was “Plastic coolant manifold”; both steel parts used the offered rectangular stainless plate category (HS 732690).

## Awaiting supplier review

Supplier review must address stock grade, deep drilling, threads, specific tolerances, flatness, sealing surfaces and edge finishing. Proposed deviations require review before manufacture. No design or process acceptance is inferred from upload success or the automatic prices. Keep assembly instructions outside supplier fabrication drawings.

## Subsequent feedback

[16 September 2026: verified order statuses and manifold faceplate tolerance/edge-finishing limitations](jlc-feedback-2026-09-16.md). Faceplate Pending, radiator Awaiting Payment, POM body Approved; displayed combined total now $356.95 including shipping. Original submission details and hashes above remain unchanged.
