# Current three-part design recap

**5 October 2026 — received manifold verified by the operator:** Q-M04 POM body and Q-M03 faceplate are dimensionally correct; all POM M4 screw holes and the G1/4 ports are correct. QD3 thread engagement is smooth, corner detail is accepted, covered holding marks are acceptable, and the 2 mm faceplate mounts without perceptible flex. See the [first-article observations](jlc-order-2026-09-16.md#first-article-observations--5-october-2026).

The R7-M01 radiator plate is **delivered but operator-unverified**, pending access to a spare Supernova. The operator reports slight sharpness on the steel; edge-finish adequacy remains an open first-article finding. The faceplate conceals POM holding marks and is the principal visible surface, so its perceived finish quality needs control. This does not reopen the accepted dimensions or establish a supplier nonconformance.

**22 September 2026:** operator-supplied screenshots show both steel parts awaiting carrier pickup and the Q-M04 POM body at 23.08% production progress (data processing, programming and blanking complete). POM price is US$197.26 with an eight-day build; steel prices remain US$9.86/29.82. See the [production update](jlc-order-2026-09-16.md#production-update--22-september-2026).

Updated 5 October 2026. The operator approved radiator revision R6 after reducing its cable notch to 10 × 2 mm. This approval does not constitute supplier manufacturing acceptance or a tested assembly rating.

The current design set is the Revision Q manifold body (Q-M04) and matching faceplate (Q-M03), plus the R7 radiator plate (R7-M01). Both steel issues use ±0.10 mm cut dimensions and coordinates; both plates now have four R5 external outline corners; all holes and other profiles are retained. These are three custom parts; fittings, plugs, screws, nuts, fans and the radiator are bought-in hardware. There is no manifold rear cover in this long-bore design.

## 1. Manifold POM body - Revision Q

- Black, unfilled POM-C or POM-H with a declared machining-stock grade; Delrin branding is optional.
- 410 mm wide × 87 mm high × 40 mm main depth; 3 mm integral front bosses give 43 mm overall depth.
- Twenty front G1/4 female ports: ten pairs at 40 mm horizontal and vertical centre spacing. Four G1/4 female side ports and four rear G1/4 ports aligned with the outermost front pairs:28 ports total.
- Two separate, continuous Ø11.8 mm longitudinal galleries centred in the 40 mm depth. One supply gallery and one return gallery, parallel-only with no grouping or internal supply-to-return link.
- Side- or rear-fed infrastructure makes all ten front pairs available to loads. A front-fed inlet/outlet pair leaves nine load pairs. Unused side/rear ports take G1/4 plugs with their own face seals.
- Ø28 bosses, R1 roots and C0.5 outer lips. Each boss stands 1 mm above the matching 2 mm faceplate; fittings seal directly against POM.
- Twelve M4 × 0.7 blind retention holes for the matching faceplate. Ø3.3 pilot cylinders are 13 mm deep plus a 118° drill point; minimum full-form thread depth is 10 mm after entry.
- Twelve main-slab outside edges: C0.50 ±0.10 ×45° ±1°, modelled in STEP.
- External deburring and internal chip cleaning/flushing; no internal cross-hole deburring operation specified.

Duty remains formulated inhibited computer coolant, with approximately 50°C intended maximum liquid temperature. This is a duty assumption, not a tested product rating. The [coolant assessment](pom-coolant-assessment.md) and [Blitz overrun plan](blitz-overrun-qualification.md) continue to apply. Deep-drilling acceptance, exact stock grade and prototype checks remain supplier/engineering items.

## 2. Manifold rack faceplate - Revision Q

- One flat 304 / EN 1.4301 stainless plate, 482.6 × 87 × 2 mm, approximately 0.394607 kg; four R5 external outline corners. Nominal 2U allocation.
- Twenty Ø32 windows for the Ø28 POM bosses: nominal 2 mm radial clearance before the root radius and tolerances.
- Twelve Ø4.5 ±0.10 plain through retention holes: four near the body corners and top/bottom fixings between each two front-port pairs.
- Reference retention hardware: twelve M4 × 10 ISO 7380-1 A2 stainless hex-socket button-head screws. No countersinks; countersunk screws are incompatible.
- Twelve optional 10 × 7 mm rack slots, six per side. The builder chooses which rack positions to populate; rack screws/cage nuts remain a separate interface.
- Q-M03 uses standard grinding/deburring; no specified face-edge chamfer/round size. Free-state flatness remains 0.30 mm maximum.
- This plate carries the manifold into the rack. Body retention is independent of coolant fittings and quick-disconnect retention.

## 3. Supernova radiator/fan rack plate - Revision R7

- One flat 304 / EN 1.4301 stainless plate, 482.6 × 444.5 × 2 mm: nominal 10U and approximately 1.247067 kg, with four R5 external outline corners.
- Four 188 × 188 mm airflow apertures with R50 corners, on the retained 200 × 200 mm fan-centre grid.
- Sixteen Ø4.5 plain fan holes for four NF-A20 fans using M4 screws and separate nuts; twelve Ø3.6 plain radiator holes for M3 screws into the radiator frame.
- Forty optional 10 × 7 mm rack slots: four available fixing positions per U, two per side. Empty holes are not structural supports.
- Top-centre cable notch: 10 mm mouth × 2 mm depth, four tangent R0.5 profile corners, 9 mm throat and 8 mm bottom flat.
- Cable-contact edges receive R0.3–0.5 rounding on both faces after cutting. STEP/DXF contain the actual notch outline; these additional face-edge finishing rounds are specified in the drawing.
- Raw stainless sheet finish on both broad faces; no brushing or polishing, no surface markings; no tapping, countersinking or bending.
- Assembly order: fans onto plate, populated plate onto radiator, complete assembly onto rack. Fan screw heads and washers sit on the core side; nuts sit outside the fan faces.

The [current load summary](radiator-load-assessment.md) uses R4 structural calculations as baseline evidence for the radiator mount, not an R7 tested assembly rating. R6 added the small top-edge notch and R7 rounds the four outer corners to R5; fixing positions and air apertures remain the same.

## Production-file status

The operator accepted the complete Q-M04/Q-M03/R7-M01 set on 16 September 2026 and authorised a **separate new JLC order**, superseding the earlier hold. Submitted for file review on 16 September after explicit confirmation of UPS shipping at US$71.99. Prior material, finish and goods metadata were reused. No payment was made. The operator subsequently reported clearing the original order; preserve its fabrication archives. [New-order submission record](jlc-order-2026-09-16.md). On 17 September 2026, the operator supplied a JLC timeline screenshot showing all three current parts Approved and the batch awaiting payment. No review comments are shown. The screenshot does not establish the final reviewed prices or machining route. See [approval record](jlc-order-2026-09-16.md#supplier-approval--17-september-2026). Each fabrication ZIP contains a matching single-part STEP and PDF; both steel packs also include DXF.

Use `output/submission/current-three-parts/` as the submission index. Older O-M02, P and R6-M01 files are historical. Q studio and StarTech25U scenes show the current parts; supplier Koolance geometry and accepted tubing routes remain. First assembly: M4×10, dry, without Loctite. The [torque/creep assessment](Q-torque-and-creep.md) records the unqualified trial setting and remaining actual-grade tests.
