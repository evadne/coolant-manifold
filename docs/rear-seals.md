# Revision G — Polymax 3 mm EPDM face seals

The selected Option B design uses **two Polymax 255 mm ID × 3 mm section EPDM 70 ShA rings**, in **4.0 mm-wide × 2.3 mm-deep grooves**. The cover closes onto the surrounding POM lands, compressing each ring by approximately **23%**. This is partial compression, not flattening the rubber.

![Rear seal detail](../output/images/rear-seal-review.png)

## Supplier guide and dimensions

The supplied [Polymax O-ring groove guide](https://www.polymax.co.uk/media/documents/Polymax_O-ringen_Guide.pdf) has separate radial and face-seal columns. On page 2, the row for a 3 mm ring gives:

| Column | Groove depth | Groove width |
|---|---|---|
| Dynamic/static radial | 2.50 +0.06/0 mm | 3.90 +0.20/0 mm |
| **Face type — applicable here** | **2.20 +0.10/0 mm** | **3.90 +0.20/0 mm** |

Revision G uses **width 4.00 +0.10/0 mm** and **depth 2.30 +0/−0.05 mm**. The resulting width range 4.00–4.10 and depth range 2.25–2.30 sit within the guide's face-seal ranges. Selecting the deeper end gives less squeeze than a nominal 2.20 mm groove while retaining compression throughout the checked dimensional range.

The guide also lists radius r = 0.8 mm without backup rings. The current machining specification retains a smaller groove-root radius of **0.20 mm maximum**, preserving gland volume; this detail needs supplier agreement and is not claimed to reproduce the guide's entire recommended profile. The tolerance calculation includes the volume displaced by two R0.20 root corners. STEP omits these microscopic edge treatments, as called out in the manufacturing notes. The guide's surface-finish values are labelled Rt; do not directly substitute them for the existing Ra requirements.

| Feature | Revision G |
|---|---|
| Gallery opening | 388 × 16 mm, R8 ends, 24 mm deep |
| Groove centreline | 396 × 24 mm overall, R12 ends; overall dimensions ±0.10 |
| Groove width × depth | **4.0 × 2.3 mm**, tolerances above |
| Centreline path per ring | 819.40 mm |
| Free ring centreline circumference | 810.53 mm |
| Nominal elongation | 1.09% |
| Estimated installed section | 2.984 mm |
| Estimated protrusion before cover closure | **0.684 mm** |
| Estimated squeeze after cover closure | **22.92%** |
| Approximate rectangular-gland fill | **76.00%** |
| Gallery-to-groove POM land | 2.00 mm |
| Inside radius of groove ends | 10.00 mm |

The 255 mm ring was compared with the user's 260 × 3 mm example. At the selected groove path, a 260 mm ring would be nominally too long; the 255 mm ring provides modest positive elongation. The path is adjusted with the ring selection rather than forcing a ring into the previous 3.53 mm-ring geometry. All eighteen G1/4 port-major circles remain inside their intended gallery openings, and the 16 × 24 mm flow section is retained. Supply and return remain uninterrupted and separate.

## Compression and closing force

The screws supply the force to compress the ring until the cover reaches the POM lands. Once the faces seat, groove depth sets the intended compression. Additional torque should not be used to bend the cover or deform the POM to obtain more squeeze; nor can it compensate for a groove deeper than the ring section. The cover needs enough retained clamping force to resist fluid pressure and service loads, but that requirement is separate from selecting the initial squeeze percentage.

Free ring circumference is `π × (ID + section)`. For stretch ratio `λ = groove path / free circumference`, a uniform volume-conserving approximation gives `installed section ≈ free section / sqrt(λ)`. Initial squeeze is `1 − groove depth / installed section`. Rectangular-gland fill is approximately `π × installed section² / (4 × width × depth)`.

Using Polymax's published ISO 3601-1 tolerances of **±1.85 mm ID** and **±0.09 mm section**, together with the specified groove ranges, gives:

| Dimensional check | Calculated range |
|---|---:|
| Squeeze | **20.22–27.07%** |
| Fill, including maximum specified root radii | **69.34–83.23%** |
| Elongation | **0.30–1.90%** |

Sources: the catalogue's Tolerance tab and [Polymax large-ID tolerance table](https://www.polymax.co.uk/o-ring-tolerance-54-600id). These are dimensional checks with the cover seated, excluding coolant swell, thermal effects, cover lift/creep and nonuniform rubber deformation. Internal pressure pushes the ring towards the groove's outer wall, which the final seal review must account for. Partial compression is necessary for sealing but does not alone establish a pressure rating.

Cover outer screw rows return to z5.5/81.5; the middle row remains z43.5. Four end screws remain at x±213 on the gallery rows. There are still 31 M4 cover screws. Nominal dry land to a conservative Ø4.2 thread envelope is **1.90 mm**, and the outer countersinks have **1.30 mm edge margin**. These margins improve on the preceding 3.53 mm-ring layout.

STEP contains two volume-equivalent rectangular compressed seal envelopes, approximately 3.040 mm wide × 2.30 mm deep. They are review representations, not predictions of the deformed rubber profile. The drawing shows the circular section before closure.

## Polymax procurement

The [EPDM catalogue](https://www.polymax.co.uk/o-rings/rubber-epdm-oring/) was checked through Computer Use on 14 September 2026: search ID255, CS3, material EPDM. It lists **255 × 3 mm EPDM 70 ShA at £3.37 each**. The 260 × 3 mm alternatives were also observed: 70 ShA at £3.44 and peroxide-cured 80 ShA at £3.76. The 70 ShA material is selected; do not substitute the harder compound solely because it shares the dimensions.

The user reports that adding rings to the cart gives **dispatch in 5–7 days**, with a **£10 minimum rubber order value** and no apparent per-size minimum quantity. These are user-observed checkout terms, not an independently checked stock quantity or evidence of manufacture to order. At the displayed unit price, **three selected rings total £10.11**, providing the two required seals and one spare. Confirm the applicable VAT/shipping/minimum-order basis and selected size's dispatch estimate at checkout. No order has been placed.

The product is listed as a complete ring. Confirm one-piece moulded construction if mandatory; the observed listing did not establish its manufacturing/joining method. No user-cut or glued seals are specified.

Revision F's RS 3.53 mm rings and revision E's 2 mm concept are superseded, with their completed models retained in Git history.

## Reproduction

Run `scripts/build_cad.py` for Option B and with `--mounting backplate` for Option C. `scripts/draw_rear_seals.py` generates the review SVG and `output/analysis/rear-seal-sizing.json`; rasterise the SVG with `rsvg-convert`. Rebuild Blender scenes from the resulting CAD tessellations with `scripts/render_blender.py`, using the corresponding mounting option. The numerical checks and supplier listings are documented design inputs, not manufacturing release approval.
