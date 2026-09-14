# Revision F — rear grooves for stock EPDM rings

The CAD now uses **two RS PRO 258-0460 O-rings**, each **253.59 mm ID × 3.53 mm section**, in **4.5 mm-wide × 2.8 mm-deep grooves**. The stainless cover seats against the surrounding POM lands and compresses the rings. Both mounting options share this revision.

![Rear seal detail](../output/images/rear-seal-review.png)

## Dimensions and compression

| Feature | Revision F |
|---|---|
| Gallery opening | 384 × 16 mm, R8 ends, 24 mm deep |
| Groove centreline | 395 × 27 mm overall, R13.5 ends |
| Groove width × depth | **4.50 ±0.05 × 2.80 ±0.05 mm** |
| Groove centreline length/height tolerance | ±0.10 mm |
| Centreline path per ring | 820.82 mm |
| Free ring centreline circumference | 807.77 mm |
| Nominal centreline elongation | 1.62% |
| Estimated installed section after elongation | 3.502 mm |
| Estimated protrusion above POM before closure | **0.702 mm** |
| Estimated squeeze with cover seated | **20.04%** |
| Estimated gland fill | **76.44%** |
| Solid POM land between gallery and groove | 3.25 mm |
| Inside radius of groove ends | 11.25 mm |

Ring circumference is `π × (ID + section)`. A complete circular ring is laid into the capsule-shaped groove without cutting or gluing. Uniform elongation is estimated by `λ = groove path / free circumference`; conservation of elastomer volume gives `installed section ≈ free section / sqrt(λ)`.

For installed section `d`, groove depth `h` and width `b`, initial squeeze is `1 − h/d`, and rectangular-gland fill is approximately `πd²/(4bh)`. Rubber is nearly incompressible, so axial compression needs lateral room. Groove void also accommodates dimensional variation and coolant/thermal expansion. Parker gives 60–85% fill for most applications; this is general guidance, not a pressure qualification. [Parker O-Ring Handbook](https://www.parker.com/content/dam/Parker-com/Literature/O-Ring-Division-Literature/ORD-5700.pdf).

The selected 4.5 mm width is a simple machining dimension. At 2.8 mm depth, a 4 mm width would give about 86% fill after nominal stretch and leave insufficient tolerance margin. A 5 mm width would leave less material beside the outer screw rows in this 2U envelope. No unusual custom-width cutter is needed: a smaller end mill can interpolate and finish the 4.5 mm groove.

The 2.8 mm depth deliberately remains below the ring section. A 3.5 or 4 mm-deep groove would remove almost all, or all, intended squeeze. The ring is compressed when the cover lands seat; the cover must not be held away from the POM by a spacer or screw bottoming.

## Fit and dimensional tolerance checks

The galleries shorten from 400 to 384 mm, reducing elongation of the stock ring. All eighteen G1/4 port-major-diameter circles remain fully within their intended gallery openings; the 16 × 24 mm flow section and parallel-only topology are retained. The outer cover screw rows move from z5.5/81.5 to **z4.5/82.5**. The middle row remains z43.5; four end screws remain at x±213 on the gallery rows. There are still 31 M4 cover screws.

A conservative Ø4.2 cover-thread envelope leaves **1.15 mm minimum nominal dry land** to the groove. The outer Ø8.4 countersinks lie **0.30 mm inside the cover/body edge**. These are relatively narrow margins, explicitly identified for vendor review in the manufacturing notes. The assembly has no modelled hole/groove collisions; that does not establish thread strength or resistance to cracking/creep.

Using ring ID ±1.40 mm and section ±0.10 mm as review allowances, plus the groove tolerances above, the centreline model gives:

| Check | Calculated dimensional range |
|---|---:|
| Squeeze | **15.98–23.87%** |
| Fill | **69.69–83.74%** |
| Elongation | **0.99–2.25%** |

The ring allowances come from the [Techno Ad AS568 table, size274](https://www.technoad.com/engineering/dimensions/as-568-parker/); confirm that the supplied EPDM batch meets them. The calculation assumes the cover contacts the POM face and uses a uniform volume-conserving stretch approximation. It excludes coolant swell, thermal effects, cover lift, creep and local nonuniform deformation. Internal pressure pushes the ring towards the groove's outer wall; the final seal review must account for that position. Remaining dimensional squeeze is necessary for sealing, but does not by itself establish pressure capability.

STEP includes two volume-equivalent rectangular compressed seal envelopes, approximately 3.440 mm wide × 2.80 mm deep. They are review representations, not predictions of the actual deformed rubber profile. The drawing shows the circular section **before closure**.

## RS UK purchase reference

Checked 14 September 2026 through Computer Use, including the product page and delivery dialog. No order was placed.

| Item | Product-page information |
|---|---|
| Product | [RS PRO 258-0460](https://uk.rs-online.com/web/p/gaskets-o-rings/2580460) |
| Standard | AS568-274 / BS 1806-274 |
| Material | EPDM; range labelled 70 ShA, specifications list 71 IRHD |
| Free size | 253.59 mm ID × 3.53 mm section; 260.65 mm OD |
| Pack | Two rings, sufficient for one manifold |
| Indicative price | £4.92 per bag excluding VAT |
| Availability displayed | 24 unit(s) ready to ship |
| Default-quantity delivery check | 16 September 2026 |

RS uses “Bag(s)” for ordering and “unit(s)” in stock wording; do not interpret that as 24 bags. Availability is a point-in-time observation. The product is a complete O-ring; confirm one-piece moulded construction if mandatory, because the page did not explicitly establish its manufacturing/joining method. No user-cut or glued rings are specified.

Revision E's 2 mm section and 2.8 × 1.60 mm grooves are superseded. The earlier 260/262/265 × 2 mm dimensional candidates were not confirmed stocked products and are not the current selection.

## Reproduction

Run `scripts/build_cad.py` for Option B and with `--mounting backplate` for Option C. Run `scripts/draw_rear_seals.py` for the dimensioned review and `output/analysis/rear-seal-sizing.json`, then rasterise `output/rear-seal-review.svg` with `rsvg-convert`. Rebuild the Blender scenes from the resulting CAD tessellations using `scripts/render_blender.py` with the corresponding mounting option.
