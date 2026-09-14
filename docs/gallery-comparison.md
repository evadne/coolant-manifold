# Gallery and seal architecture assessment

Historical 14 September 2026 assessment of revision E. Numerical geometry and quantities below describe that revision, not the revised seal glands. Revision G now uses388 mm pockets and selected3 mm Polymax rings; see [current rear seals](rear-seals.md). Numerical results are in `output/analysis/gallery-comparison.json`.

**Retain the rear-milled pockets as the current design baseline; investigate longitudinal bores as a manufacturing and assembly alternative.** Small end closures offer shorter seal paths and potentially fewer screws, but those advantages do not establish lower total cost or better reliability. The deciding procurement question is the price and capability for deep drilling this particular 440 mm POM body, alongside the cost of the complete closure and rack mounting assembly.

EK describes an acetal body with stainless steel end caps and brass plugs, and publishes a 326 mm body length. Its accessible documentation does not establish the exact bore diameter, machining sequence or number of passes. The comparison below treats the user's EK-style construction as enclosed longitudinal bores with end closures; it does not claim knowledge of EK's production tooling. [EK product portfolio, page 31](https://www.ekwb.com/shop/mediaset/EK-PRO-Portfolio-2025-Q4.pdf).

## Manufacturing and assembly

Compare complete rack-mounted assemblies with the same front faceplate, rather than comparing our rack assembly with an unmounted manifold. The user's two-end-cap arrangement gives the following count; the end-cap screw quantity has not been designed here.

| Component | Current rear-pocket assembly | Through-bore assembly retaining our rack faceplate |
|---|---:|---:|
| POM body | 1 | 1 |
| Stainless pressure-closure plates | 1 large rear cover | 2 small end caps |
| Stainless rack faceplate | 1 | 1 |
| Total stainless plates | 2 | 3 |
| Gallery O-rings | 2 large loops | 4 small rings |
| Pressure-closure screws | 31 | Expected fewer; quantity pending cap design |
| Faceplate/body screws | 8 | Retain 8 as the comparison assumption; recheck against bores |
| Rack fixings | 4 sets | 4 sets |

Fittings and their seals are common to both and excluded from this table. End drilling does not reduce the plate or O-ring count in this comparison. Its potential efficiency comes from smaller closures, shorter seal paths and fewer closure screws. A combined end-cap/rack bracket might change that count, but would be a separate mounting design and is not credited here. The complete manufacturing and assembly cost, including the custom rack mount, must be compared.

| Criterion | Longitudinal bores and end caps | Current rear pockets and cover |
|---|---|---|
| Gallery access for machining | Long drills entering from the body ends | Shorter end mills entering the broad rear face |
| Main machining difficulty | Drill wander, chip removal, heat, end setup and available machine travel | Pocket finishing, long seal grooves and seal-face flatness |
| Additional pressure closure | Small end caps, local seals and retaining screws | 440 × 87 × 3 cover, two long seal paths and 31 screws |
| Assembly effort | Likely lower after the end joint is developed | More screws, longer seals and a larger surface to inspect |
| Internal inspection and deburring | Access through the ends and intersecting ports; harder to see every junction | Direct access before fitting the cover |
| Cleaning after use | Through bores can be brushed/flushed with caps removed | Cover removal exposes the full gallery |
| Likely production advantage | Fewer closure features and simpler seal handling | Broadly accessible milling operations |

The current pockets are also two continuous channels, not a set of separate cells. Their 24 mm machining depth is only 1.5 times their 16 mm width. Each can follow a straight longitudinal toolpath at successive depths. A long drilled hole may likewise require a pilot, pecking or a dedicated deep-hole process. One continuous gallery does not imply one uninterrupted cutting pass for either design.

At Ø22, drilling through our 440 mm body from one end is 20D; drilling from both ends is nominally 220 mm/22 mm = 10D per side, plus allowance for overlap and the drill point. Meeting bores introduce alignment/step and inspection considerations, but no intentional restriction or grouping. Our body is approximately 35% longer than EK's published body, so its manufacturing difficulty cannot be transferred directly from the reference product.

Xometry recommends ordinary hole depths around 4D and identifies higher costs around 10D. Its advanced design guidance discusses special tooling or equipment for greater depths. Deep drilling is feasible, but neither JLC nor Xometry has quoted this geometry. Request manual DFM with the actual POM grade, machine access and cross-hole deburring requirements. Do not impose precision shaft-fit tolerances on the whole gallery when only flow clearance and wall thickness require control. [Xometry machining guidance](https://xometry.pro/en/articles/cnc-machining-design-tips/), [Xometry advanced DFM discussion](https://www.xometry.com/resources/blog/advanced-tips-for-cnc-designs-and-drawings-webinar/).

## Seal efficiency and pressure load

The user points to GPU waterblocks with large perimeter O-rings as a relevant comparison. The engineering principle is applicable here: a long static face seal is not inherently unreliable. Seal length alone cannot predict leakage, and four small seals are not automatically more reliable than two large ones. Uniform compression, surface condition, gland geometry, cover support, fastener spacing and retained preload govern the joint. The analogy supports the viability of this construction, rather than transferring a particular waterblock's pressure rating to our manifold. [Parker O-Ring Handbook, static sealing section](https://www.parker.com/content/dam/Parker-com/Literature/O-Ring-Division-Literature/ORD-5700.pdf).

The rear cover is supported by the surrounding POM lands; it is not an unsupported plate spanning the entire 400 mm gallery length. Its local unsupported width, support contact, screw pitch and deformation between screws need to be assessed. The current 31-screw pattern is a prototype layout, not a demonstrated minimum. Review whether that count can be reduced while preserving seal compression before accepting the additional deep-drilling operation solely to simplify the seal. Long-term POM creep and thermal cycling remain joint-design considerations, not evidence that the large-ring approach is unsuitable.

The current seal centreline is approximately 840 mm around each gallery: 1.68 m in total. The revision E BOM requested continuous moulded or factory-vulcanised loops. A suitable stock circular O-ring might instead be laid into this elongated path, subject to available size, stretch and corner-radius checks; the pocket architecture does not inherently require a custom mould. Small end seals make standard O-ring sourcing and installation much simpler. Face-seal design must still address squeeze, fill, finish, extrusion clearance and joint distortion. [Parker O-Ring Handbook, static sealing section](https://www.parker.com/content/dam/Parker-com/Literature/O-Ring-Division-Literature/ORD-5700.pdf).

For comparison, four independent end seals on a hypothetical Ø26 seal centreline total approximately 327 mm: about one fifth of the current seal length. This diameter is an illustrative comparison around a Ø22 bore, not a selected O-ring or finished gland. Through drilling requires four sealed openings for two galleries, whether drilling from one end or both. Two blind galleries can use only two end seals, but remain harder to clean and require deep blind drilling.

Pressure separation force is pressure multiplied by effective projected seal area. Using the seal centreline as an approximate pressure boundary:

| Closure | Effective projected area | Separating force at illustrative 1 bar gauge |
|---|---:|---:|
| Current cover, per gallery | 9,247 mm² | 925 N |
| Illustrative Ø26 end seal, per bore end | 531 mm² | 53 N |

The forces act in different directions and on different closure geometries; this is not a direct plate-stress comparison. Both gallery loads act on the common rear cover. One end cap covering two independently sealed bores carries both local end loads. The smaller pressure-loaded closure is a substantial advantage for stiffness and seal control. It does not remove pressure stress from the POM walls or establish a pressure rating. Loads scale linearly with pressure; 1 bar is an arithmetic example, not the proposed operating or test pressure.

The subsequent [D5 pressure assessment](d5-pressure.md) estimates nominal full-speed pump-only shut-off differentials around 0.36–0.38 bar for one standard 12 V D5, 0.73–0.76 bar for two in series and 1.45–1.53 bar for four. Actual local seal pressure also depends on reservoir/fill pressure and elevation. This sets a relevant scale for the comparison without establishing a working-pressure rating.

The current rear cover weighs approximately 0.90 kg at the model's assumed stainless density. The bored design replaces it with small end caps, so assembly mass should fall, but a net saving requires the revised body, caps and fasteners to be modelled. The eight dry front mounting screws and the rack faceplate remain necessary.

## Hydraulic efficiency

The current mid-gallery section is 16 × 24 = 384 mm², with hydraulic diameter `4A / wetted perimeter = 19.2 mm`. A circular bore with equal area is Ø22.11 mm.

| Gallery section | Flow area | Relative to current area |
|---|---:|---:|
| Current 16 × 24 pocket | 384 mm² | 100% |
| Ø16 bore | 201 mm² | 52% |
| Ø20 bore | 314 mm² | 82% |
| Ø22 bore | 380 mm² | 99% |

Thus Ø22 is the appropriate initial comparison; choosing Ø16 simply because the present pocket is 16 mm wide would nearly halve its area. At similar area and finish, the circular section has a larger hydraulic diameter and can reduce straight-channel friction. As a geometric sensitivity check only, the Darcy-Weisbach ratio at equal flow, length and Darcy friction factor is `(Dh_current / D_bore) × (A_current / A_bore)^2`: approximately 4.38 for Ø16, 1.43 for Ø20 and 0.89 for Ø22. Equal friction factor is an assumption, not a prediction across different Reynolds numbers or shapes. The JSON records these ratios for reproducibility. [ASHRAE Fundamentals, fluid flow](https://handbook.ashrae.org/Handbooks/F25/IP/f25_ch03/f25_ch03_ip.aspx) describes the Darcy-Weisbach method and hydraulic-diameter substitution for turbulent noncircular conduit flow.

Real header flow changes at every branch, and losses also depend on junctions, ports, coolant, fittings and the branch circuits. Neither straight geometry guarantees equal branch flow. The same-end IN/OUT arrangement remains direct return, and the main G1/4/QD3 pair still carries total system flow. There is no evidence yet that gallery friction dominates system loss. Both architectures can implement the required two uninterrupted, separate networks without grouping or a supply-to-return bypass.

## Implications for the next design

Investigate two approximately Ø22 through galleries, with a flat removable cap at each end and an independent face O-ring around each bore. A shared metal cap can cover both bores, but must not contain a common recess that connects them. Bolted caps avoid introducing larger threaded coolant ports; all user connections remain G1/4 female. End-face sealing localises the accurately finished seal features instead of requiring a precision radial sealing finish along the deep bore.

This is a body redesign, not merely replacing the rear pockets with circles at the same location. Keeping the present 16 mm front wall and adding a Ø22 bore within a 40 mm body would leave only 2 mm behind the bore. Moving its centre to mid-depth would instead give nominal 9 mm front and rear walls, with 15 mm from the raised boss end to the bore entrance. Neither arrangement is structurally qualified. Recheck front thread depth, wall thickness, dry M4 mounts, end-cap fasteners, end access and the rack envelope together. The 3 mm front plate and raised port bosses can remain conceptually unchanged.

For a one-off using ordinary short-tool milling, the current pockets are a sound architecture to develop. First assess the rear cover and screw spacing for the D5 pressure scenarios. For repeated assemblies, the bored construction may offer lower assembly effort if a capable supplier offers an acceptable deep-drilling quote. Supplier machining and assembly quotes, followed by separate-gallery leak and service-load validation, decide the final choice; there is no substantiated percentage cost saving or reliability ranking yet.
