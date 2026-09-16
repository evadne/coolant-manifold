# JLCCNC feedback identification — 16 September 2026

Read Nelson's email in Safari/Gmail through Computer Use: subject `Order issue confirm 6347288A-SMS2609163000694 from JLCCNC`, dated 16 September 2026 at 14:10 as displayed. [Source email](https://mail.google.com/mail/u/0/#inbox/FMfcgzQhWTnmLqKstRdQwbfGTGFqVFTm). This record identifies requirements for discussion; no proposed deviation has been accepted and no fabrication file has been changed.

## Confirmed affected part

**SMS2609163000694 = RM10-Q-M01-FACEPLATE**, the 482.6 ×87 ×2 mm stainless manifold rack faceplate. It is not the POM body or radiator plate.

The email reproduces our submitted faceplate remarks, including M4 hole centres ±0.05 mm and flatness 0.30 mm. JLC says the noted tolerance cannot be processed with its factory's ±0.1 mm laser tolerance. It also declines controlled chamfering/sharp-corner removal and complete burr removal, offering standard grinding/deburring without a perfect-deburr guarantee.

| Drawing feature | Submitted requirement | Relationship to feedback |
|---|---|---|
| H01–H12: twelve M4 retention clearance holes | Ø4.50 +0.10/0; X/Z centres ±0.05 mm, sheets 1–2 | The ±0.05 coordinate call-out is explicitly reproduced in the email and conflicts with the stated ±0.1 laser capability. |
| W01–W20 port windows; H01–H12 holes; R01–R12 rack slot widths | Ø32.00 +0.10/0; Ø4.50 +0.10/0; slot width 7.00 +0.10/0 | Additional drawing conflict if ±0.1 applies to finished feature sizes: each permitted size band is only 0.10 mm wide, versus 0.20 mm for ±0.1. JLC did not individually identify these groups in the email. |
| External edges on both faces, including opening edges | Deburr / specified 0.10–0.20 mm edge break; keep screw bearing seats flat | Controlled edge treatment exceeds the standard grinding/deburring service described in the reply. |
| Mating face | Free-state flatness ≤0.30 mm | Mentioned in the reproduced remarks, but not separately accepted or explicitly rejected. Do not substitute a ±0.1 cutting-size tolerance for a flatness specification. |

These are plain clearance holes; there are **no countersinks** on the submitted faceplate. The concern about chamfering therefore relates to edge finishing, not screw-head countersinks. A radius in the two-dimensional laser outline is also distinct from a chamfer or round over the sheet thickness.

## Other parts and verified order statuses

- **SMS2609163000690 — SN1260-R6-M02-PLATE (radiator mount):** this email does not name it. Its drawing nevertheless contains similar potentially affected requirements: +0.15/0 hole/slot-width limits, 0.20–0.30 mm general edge breaks, and especially the E01 cable-notch R0.30–0.50 face-edge rounds. Those rounds are secondary edge finishing; they are distinct from the R0.50 notch outline already modelled for laser cutting. Whole-plate free-state flatness is ≤0.50 mm. These are engineering implications of the stated process limitation, not a separately observed rejection.
- **CNC2609165002398 — RM10-Q-M01-BODY (POM):** not named in this sheet-metal feedback. Its CNC threads, seals, bosses and galleries use a different process. The order-history page now marks this part **Approved**. Its product details retain black POM, threads enabled, ±0.05 mm tightest tolerance and the submitted remark requesting grade/deep-gallery confirmation. No specific grade declaration or feature-by-feature engineering response was visible in the inspected details; the email provides no basis to relax the POM requirements.

After restarting the Computer Use service and Safari under the operator's instruction, signed in to JLCCNC using the existing account and inspected all three product-detail panels in [order history](https://jlccnc.com/user-center/orders/) on 16 September 2026. Batch **W2026091606463892** remained at **File Review**:

| Part / order reference (all suffix `-6347288A`) | Displayed status | Current part price, USD | Build time |
|---|---|---:|---|
| Q faceplate — SMS2609163000694 | **Pending**; confirmation email sent, response requested | 9.86 | 2 days |
| R6 radiator plate — SMS2609163000690 | **Awaiting Payment** | 29.84 | 2 days |
| Q POM body — CNC2609165002398 | **Approved** | 197.26 | 8 days |

The radiator details retain the full submitted remark, explicitly asking confirmation of specified tolerances, ≤0.50 mm flatness and external edge finishing including the rounded cable-contact notch. No separate objection was displayed for that part. Its payment status does not resolve the apparent inconsistency between that finishing requirement and the sheet-metal limitation in the faceplate email; clarify it before accepting a manufacturing solution.

Displayed merchandise total is **$236.96**, shipping **$119.99**, combined **$356.95**. The body has increased from the original automatic estimate of $128.74 to $197.26; both steel prices are unchanged. These are the current displayed figures, not payment authorisation, a landed-cost guarantee or a finalised batch while the faceplate remains pending. The historical submission record and original prices remain intact.

## Follow-up fit assessment

The operator requested a check of the unchanged nominal faceplate at JLC capability. The [calculated assessment](Q-faceplate-as-drawn-capability.md) finds ample boss-root clearance and marginal worst-case M4 clearance if nominal Ø4.5 is permitted to fall to Ø4.4. Retaining Ø4.5 minimum passes with plate positions ±0.1 and existing POM positions ±0.05. No supplier concession or geometry change has been made.

## Scope retained

Keep the submitted Q-M01/R6-M02 ZIPs intact while discussing alternatives. The existing [tolerance-relaxation assessment](tolerance-relaxation-review.md) can inform a later change, but accepting ±0.1 everywhere on the existing geometry is not yet approved. No supplier reply, acceptance, replacement upload or payment was sent by the assistant during this investigation.
