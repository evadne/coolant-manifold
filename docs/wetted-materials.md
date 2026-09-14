# Wetted rear plate — material selection

**Retain 316L stainless steel (EN 1.4404) for the rear sealing plate**, for the user-confirmed use of a formulated, inhibited coolant, with the exact product and operating conditions still to be chosen. Copper/brass components elsewhere in the loop do not by themselves require replacing this plate. The front rack faceplate remains dry and does not need a material change for coolant compatibility.

This is a design selection, not a corrosion-life qualification. Koolance explicitly lists stainless steel, copper, brass, nickel, POM and EPDM among the materials tested with [LIQ-705 coolant](https://koolance.com/liq-705-liquid-coolant-bottle-electrically-insulative-700ml-clear). That supports a feasible material/coolant combination for this design; it is not a blanket approval of all PC coolants, operating temperatures or assembly details. The user named Mayhems X1 and Koolance 705 as examples; neither has been purchased or made mandatory.

The checked [Mayhems X1 Eco premix listing](https://mayhems.store/mayhems-x1-v2-eco-series-blood-red-premixed-coolant-1-litre.html) specifies corrosion inhibitors and protection for copper, brass, steel, nickel and aluminium. It does not explicitly identify 316L, POM or EPDM on that page, so this is less specific evidence than Koolance’s material list. Retain X1 as a candidate, with those details to be confirmed for the exact formulation; absence from this page is not evidence of incompatibility.

## Galvanic coupling and this assembly

Passive stainless steel can accelerate corrosion of copper or brass when the metals are electrically connected and exposed to an electrolyte. The anodic/cathodic area ratio and environment matter. Electrical insulation between dissimilar metals is one recognised mitigation. [Outokumpu corrosion guidance](https://www.outokumpu.com/en/expertise/stainless-basics/corrosion-resistance)

In this CAD, the rear cover contacts POM and EPDM, and its screws terminate in blind POM holes on dry lands. The G1/4 fittings also thread into POM. Front and rear screws do not intersect. Thus the model provides no direct metallic connection from the wetted cover to the fittings or dry rack faceplate. The liquid provides an ionic path; sustained galvanic coupling also needs an electronic return path. This is an inference from the assembly, not a measured insulation test. Avoid creating an unintended bridge through added brackets, foil, inserts or touching hardware; do not alter protective earthing elsewhere in the system to address corrosion.

Electrical separation does not prevent every corrosion mechanism. Local pitting/crevice corrosion, contamination and unsuitable coolant chemistry still require consideration, especially near the rear seal crevice. The design assumes formulated inhibited coolant, not plain-water operation.

## Manufacturing and operating requirements

- Specify **316L / EN 1.4404**, not unspecified stainless. Its molybdenum alloying supports increased corrosion resistance; the low-carbon designation principally benefits resistance after welding, rather than eliminating galvanic coupling. [Outokumpu 316L grade data](https://www.outokumpu.com/en/products/product-ranges/supra)
- Remove fabrication debris, free-iron contamination, oxide and heat tint as applicable; agree appropriate cleaning/pickling/passivation with the vendor. Passivation alone is not a substitute for removing substantial oxide or a chromium-depleted layer. Final rinse, dry and protect the sealing face. Inspect finish/flatness after treatment. [Outokumpu post-fabrication treatment](https://www.outokumpu.com/en/expertise/stainless-basics/post-fabrication-treatment)
- Use an inhibited coolant whose supplier supports the full wetted material set: copper/brass/nickel, 316L, POM and EPDM. Confirm temperature range, concentration and maintenance interval for the actual fluid. Avoid unqualified additives and cleaning residues.
- Qualify the assembled loop under its intended coolant, temperature and maintenance regime before claiming service life. Keep the rear cover isolated from added conductive mounts as designed.

Changing to brass or copper could simplify the metal mix, but would require selecting an exact alloy and reassessing plate stiffness, flatness and countersunk bearing. Nickel plating introduces coating-quality and porosity questions; it is not automatically safer. A POM pressure cover would need its own thickness, creep and clamping design. None offers a demonstrated reason to replace the current 316L cover at this stage.

Sources checked 14 September 2026. Manufacturer compatibility statements do not establish the manifold's pressure, structural or corrosion rating.
