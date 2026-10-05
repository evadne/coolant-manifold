# Current manifold design — Revision Q

Canonical delivered manifold issues are [Q-M04 body](jlc-submission-Q-M04.md) and [Q-M03 faceplate](jlc-submission-Q-M03.md). Q-M04 retains the shorter M4 detail introduced in historical Q-M01 and adds twelve C0.5 ×45° main-slab edge chamfers. Q-M03 adds four R5 outside outline corners and retains all original openings/positions. Use the [repeat-order guide](order-from-jlc.md) for the exact files.

The RM10-2U manifold provides a common supply gallery and a separate common return gallery for parallel loads. It has no internal grouping, partitions, bypass or supply-to-return connection. The current manufactured parts are one POM body and one dry stainless front rack plate. There is no rear plate.

| Interface | Revision Q, nominal mm |
|---|---|
| POM body | 410 wide × 87 high × 40 main depth; 43 overall with bosses |
| Integral bosses | Twenty Ø28 × 3 high; R1 roots; C0.5 ×45° outer lips |
| Rack faceplate | 482.6 wide × 87 high × 2 thick, 304 / EN 1.4301; four R5 outside corners (Q-M03) |
| Front ports | Twenty G1/4 female, ten pairs at 40 × 40 centres |
| Side ports | Four G1/4 female, two at each end |
| Rear ports | Four G1/4 female at X±180, Y40, Z23.5/63.5; flat Ø28 seal lands |
| Galleries | Two continuous Ø11.8 bores along X, axes Y20 and Z23.5/63.5 |
| Body retention | Twelve M4 ×0.7 holes; M4 ×10 ISO 7380-1 A2 button-head screws |
| Rack mounting | Six optional 10 ×7 slots per side, at X±232.55 |

X runs across the rack, Y rearwards and Z upwards. The slab front is Y0, the plate occupies Y−2…0 and the POM sealing faces are Y−3. The bosses therefore project 1 mm above the steel. Fittings seal on the uninterrupted POM annuli using their own O-rings. Ø32 plate windows provide 2 mm nominal radial clearance around the bosses and 1 mm around the Ø30 root envelope, before tolerances.

Front port centres run from X−180 to +180 in 40 mm increments. The outer centres are 25 mm from the body ends. Either row can be assigned supply or return by the external plumbing; each vertical pair serves one load. Side- or rear-fed infrastructure frees all ten front pairs. Front-fed infrastructure consumes one pair. Unused connections require suitable plugged or self-closing fittings; plugged side ports remain reusable.

## Rack and fitting access

The 87 mm panel uses a nominal 2U allocation, leaving 1.9 mm within 88.9 mm. EK's reference manifold is listed at 326 ×57 ×36 mm; its 57 mm height exceeds 1U by 12.55 mm. The project chose service access over a dense 1U arrangement. See the dated [source index](sources.md).

The current studio references are **Koolance QD3-MTG4 + QD3-FT10X13**, with nominal 10/13 tubing. Official STEP models are retained at supplier scale. At 40 mm pitch, the published female Ø26.1 body and Ø23.7 pull ring leave 13.9 and 16.3 mm between nominal envelopes. The operator accepts the depicted coupled placement based on experience with physical pairs. Front space is required for fittings, hose routing and servicing; no numerical minimum was approved. The inherited `service_projection_front: 100` parameter is an illustrative allowance, not a newly specified installation limit. See [fitting integration](koolance-qd3-studio-integration.md).

The twelve rack slots offer installation choices, not twelve mandatory screws. Slot heights are Z5.4/21.275/37.15/49.85/65.725/81.6. The outer slots retain a 1.9 mm nominal panel-edge ligament; washers can overhang the panel. Selected hardware, rail geometry and nearby equipment determine installed fit.

The 410 mm body leaves 20 mm per side inside an assumed 450 mm equipment opening. Four 4 mm plug heads give a nominal 418 mm fitted width. The earlier BP-90R/Barrow side-elbow envelope reaches approximately 467.6 mm overall, so it must not be described as contained inside 450 mm. Elbow depth and height may use space between rack features. Installation clearance depends on actual rails, nuts, fittings and insertion path; it is distinct from the accepted front-QD visual layout.

## Materials and manufacture

Use black unfilled POM-C or POM-H of an identified machining-stock grade; Delrin branding is optional. Intended duty is formulated inhibited computer coolant at approximately 50°C maximum liquid temperature, with Blitz Part 2 maintenance as described in the [material assessment](pom-coolant-assessment.md). These are design assumptions, not tested ratings.

The body uses long-bore drilling, external milling and direct tapped ports. Drilling from one end or from opposed ends is a process choice; JLC’s actual route has not been established. See the [machining-route assessment](Q-M04-machining-route.md). External deburring only; clean/flush loose internal chips without specifying internal cross-hole deburring. Long-hole alignment and vendor capability remain DFM items. The dry 2 mm faceplate has plain through holes, no countersinks and no threads. Fitting retention and body-to-rack retention are separate functions.

Parallel topology does not enforce equal flow. Required flow, gallery losses, plastic thread retention, thermal cycling and assembled leak performance remain engineering work. The current geometry and screw checks are detailed in [Revision Q](revision-Q-rear-ports.md); [manufacturing status](manufacturing.md) distinguishes review files from supplier issues.

Q-M01 retention:10 mm full M4 thread after entry,13 mm pilot plus118° point. First assembly dry, no Loctite. Both stainless plates: raw stainless sheet finish on both broad faces, with no brushing or polishing. See [torque/creep assessment](Q-torque-and-creep.md).
