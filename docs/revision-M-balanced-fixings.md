# Revision M — POM fixings moved inward

The six faceplate-to-POM M4 fixings now form three columns at **X = −120, 0 and +120 mm**, each at **Z = 7 and 80 mm**. From the front, these sit between pairs **2–3**, **5–6**, and **8–9**. The outer four screws have moved inward by one 40 mm port pitch; the centre two remain in place.

![Front view](../output/long-bore-M/product-views/03-front.png)

![Angled assembled view](../output/long-bore-M/product-views/01-front-three-quarter.png)

Both the countersunk steel holes and matching blind POM holes have moved. The design retains six optional rack slots per side, ten front pairs at 40 × 40 mm pitch, the 410 mm POM body, and the existing galleries, bosses and side ports. Screws remain A4 M4 × 12 DIN 7991 with the specified DIN 965 Z alternative. Product surfaces remain unmarked.

- [Editable Blender assembly](../output/long-bore-M/product-views/assembled-unmarked.blend).
- [Assembly STEP](../output/long-bore-M/cad/manifold-assembly.step), [body STEP](../output/long-bore-M/cad/body.step), [faceplate STEP](../output/long-bore-M/cad/faceplate.step), [faceplate cut DXF](../output/long-bore-M/cad/faceplate-flat.dxf).
- [Parameters](../cad/iterations/M-long-bore.json), [geometry checks](../output/long-bore-M/cad/verification.json).

The previous L outputs remain preserved, with its original design snapshot tagged `revision-l-six-rack-positions` at `d229d19`. Rebuild using `scripts/build_long_bore.py --iteration M`, then `scripts/render_product.py --iteration M` through Blender's script arguments.
