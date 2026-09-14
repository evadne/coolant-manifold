# D5 pressure basis for the manifold

14 September 2026. The user expects one or two D5 pumps ordinarily, with up to four in series for the rack. This supplies a pump-count scenario, not a final working-pressure specification. No CAD change or pressure rating is made here. Calculations are recorded in `output/analysis/d5-pressure.json`.

## Published pump head and series pressure

Aqua Computer lists 3.7 m maximum head for the D5 NEXT; EK lists 3.9 m for its 12 V D5 G3 PWM. These are maximum-head values, not simultaneous maximum-flow operating points. Xylem's D5 curves explicitly depend on pump housing, speed and voltage. The estimates below apply to conventional 12 V examples with these head ratings, not every D5-branded or higher-voltage variant. [Aqua Computer D5 NEXT](https://shop.aquacomputer.de/Water-Cooling/Pumps-Accessories/Pumps/D5-NEXT-pump::3785.html?language=en), [EK D5 G3 PWM](https://www.ekwb.com/shop/ek-loop-d5-g3-pwm-motor?___from_store=default&___store=de), [Xylem D5 curves](https://www.xylem.com/siteassets/brand/lowara/resources/brochure/cat_ecocirc_d5vario_uk_web.pdf).

For pumps in series, add their heads at the same flow rate. The resulting flow through the loop is then set by the intersection with its resistance curve; adding pumps can raise operating flow as well as head. [KSB: series operation](https://www.ksb.com/en-global/centrifugal-pump-lexicon/article/series-operation-1115590).

Using water density 1,000 kg/m³ and `Δp = ρgH`, one metre of water head is 9.807 kPa = 0.09807 bar. Published head values are approximate; additional decimal places in the JSON represent arithmetic, not measurement precision.

| Full-speed pumps in series | Combined nominal shut-off head | Pump differential pressure | Approximate psi |
|---|---:|---:|---:|
| 1 | 3.7–3.9 m | 36–38 kPa / 0.36–0.38 bar | 5.3–5.5 |
| 2 | 7.4–7.8 m | 73–76 kPa / 0.73–0.76 bar | 10.5–11.1 |
| 4 | 14.8–15.6 m | 145–153 kPa / 1.45–1.53 bar | 21.1–22.2 |

These are nominal zero-flow pump differentials, not hard limits on local gauge pressure. A low-flow restriction or closing all available load branches can move the pumps towards shut-off while they remain powered. Running pressure follows the actual pump curve and can remain relatively close to shut-off in a restrictive loop; it should not simply be assumed negligible because coolant is flowing. Reduced speed generally reduces developed head, but a PWM percentage alone is not enough to calculate it. Exact operating pressure needs the selected pump/top curves, actual speed and the hydraulic operating point or measurements.

## What pressure acts on the cover and seals?

Use each gallery's local internal pressure relative to ambient air. The pressure difference between supply and return is a different quantity and does not by itself determine outward cover load.

With a near-atmospheric reservoir on the pump suction side and approximately equal elevations, pressure immediately after the pump group is approximately reservoir gauge pressure plus the group's pressure rise, less any intervening losses. Elsewhere, component losses and height changes alter it. A sealed reservoir's headspace pressure can change with temperature and fluid expansion; any intentional fill pressure is an additional baseline. This pressure-distribution distinction is also used in circulator-system design. [Grundfos circulator handbook](https://ma.grundfos.com/rs/233-GTS-982/images/LUPSL033_Circulator%20Handbook_0423-DigitalV2.pdf?dtid=EM%3AMARKETO%3A38jpwt).

Hydrostatic pressure changes by approximately 0.098 bar per metre downward. For example, a manifold 2 m below an atmospheric reservoir has approximately 0.196 bar static gauge pressure before pump effects. In a filled closed loop the ascent and descent cancel in the net circulation-head balance; local hydrostatic pressure still exists. Thus a four-pump discharge located 2 m below that reservoir could approach approximately 1.7 bar gauge at shut-off, under those specific assumptions. Reservoir pressure, pump position and the connected flow path must be stated before adding terms. Fast transients or heating trapped coolant can exceed a steady pump-head estimate and require separate consideration when setting a working rating.

## Relevance to the gallery comparison

One or two ordinary D5s therefore support a sub-bar pump-differential scenario. Four in series move the nominal pump-only shut-off estimate to about 1.5 bar. The earlier 1 bar example was a scaling illustration: it is above a single standard D5's nominal head but below the four-pump scenario.

At the revision G nominal seal-centreline projected area of 9,380.39 mm² per gallery, approximate separating force per gallery is:

| Local gallery gauge pressure | Force on rear cover from that gallery |
|---|---:|
| 0.4 bar | 375 N |
| 0.8 bar | 750 N |
| 1.6 bar | 1,501 N |

These values use the seal-centreline area from the gallery assessment. Do not assume both galleries simultaneously have the full pump discharge pressure: calculate each local pressure separately. They are total area loads, not screw-load distributions or proof that a particular cover thickness fails or succeeds. The long cover can be designed for these pressures; the end-cap alternative's reduced closure area remains an engineering advantage rather than a necessity established solely by pump count.

Use approximately 0.4 / 0.8 / 1.6 bar as rounded nominal pump-only scenarios for one / two / four pumps when comparing concepts. They are not certified upper bounds or design safety margins. Establish the exact pump/top, speed limits, reservoir/fill arrangement, elevations, maximum temperature and relevant transient conditions before selecting the working and proof pressures. Neither a 1 bar nor a 2 bar manifold rating is assigned by this assessment.
