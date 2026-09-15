# Tolerance relaxation assessment — 16 September 2026

Assessment only; submitted Q-M01/R6-M02 drawings and supplier instructions remain unchanged. Yes, the design can be adapted to looser fabrication tolerances. The submitted requirements include conservative choices; a lower-cost specification should retain functional controls and provide clearance at mechanical interfaces, rather than loosen every value uniformly. Actual price benefit requires the supplier's review.

## Manifold retention example

Assume a conservative 4.00 mm screw envelope, parallel axes and rigid parts. With independent X and Z coordinate limits ±t on each mating part, worst relative radial offset is sqrt((2t)^2 + (2t)^2). Multiple holes mean arbitrary errors cannot all be removed by translating the plate. This is a size/position check, not a complete joint or thermal qualification.

| Scenario | Worst radial offset | Minimum radial screw clearance | Remaining radial margin |
|---|---:|---:|---:|
| Submitted ±0.05 per axis on both parts; Ø4.50 minimum plate bore | 0.1414 mm | 0.2500 mm | +0.1086 mm |
| Merely relax both patterns to ±0.10; retain Ø4.50 minimum | 0.2828 mm | 0.2500 mm | −0.0328 mm |
| Candidate ±0.10 patterns; enlarge plate holes to Ø5.00 ±0.10 | 0.2828 mm | 0.4500 mm | +0.1672 mm |

The third case is a plausible way to remove the special ±0.05 coordinate requirement. It changes only the plate clearance-hole size in this example; tapped M4 thread sizes remain standard. Before adopting it, check head bearing/contact at maximum hole diameter and offsets, edge distances, axis orientation and other assembled tolerance effects. It is not permission to enlarge or loosen tapped threads.

## Other features

- External profiles, airflow apertures and non-mating dimensions are candidates for general fabrication tolerances instead of uniformly tight individual call-outs. Check rack envelope/edge margins at the proposed limits.
- Boss/window fit has deliberate clearance. It need not function as a precision locating fit, but the boss root fillet, minimum window size and relative position must all be included.
- Boss height could potentially move from 3.00 ±0.05 to ±0.10. With 2.00 ±0.10 sheet, the size-only boss projection changes from 0.85–1.15 to 0.80–1.20 mm. Flatness, seating and fitting geometry still need consideration.
- Radiator fan/frame mounting patterns interface with bought-in parts whose positional errors must be included. Enlarging appropriate clearance holes may be preferable to tight laser-cut locations; do not assume every existing hole tolerates ±0.2 mm coordinates.
- Preserve standard G1/4 and M4 thread acceptance, adequate full thread/pilot depth, clean uninterrupted O-ring lands and the required external edge finishes. A seal-land flatness value might also be revisited with the selected fitting seal geometry; this assessment does not establish a looser sealing limit.
- Long-gallery diameter and straightness are separate process questions. Relaxation needs checks of wall reserve, intersections, flow restriction and the end-port thread pilot dimensions, not a general claim that internal bores can be arbitrarily inaccurate.
- Whole-plate free-state flatness might be negotiable, but drawing a plate down with screws introduces loads into POM or the radiator frame. No relaxed numerical flatness limit is justified here.

JLC's current sheet-metal guide lists general tolerances ±0.2 mm and cutting, punching and hole-diameter tolerances ±0.1 mm. These labels alone do not define a complete inter-part positional tolerance stack. Source checked 16 September 2026: https://jlccnc.com/help/article/sheet-metal-fabrication-guidelines

Next supplier discussion can ask which special limits affect price and feasibility. Keep the quoted design intact until a concrete alternative has been checked and selected.
