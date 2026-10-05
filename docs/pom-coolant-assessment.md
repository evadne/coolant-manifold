# POM selection for computer coolant at up to 50°C

Assessment date: 15 September 2026.

The operator expects formulated computer coolant, such as Koolance LIQ-705 or correctly prepared Mayhems X1, with liquid temperature probably no higher than 50°C. Strong acid, strong alkali and aggressive cleaning service are outside the intended duty. The 50°C value is a design assumption, not a tested assembly rating.

## Conclusion

Both black unfilled POM-C and POM-H remain acceptable material candidates for this duty. There is no demonstrated coolant-compatibility reason to reject POM-H solely because it is a homopolymer. The earlier general preference for POM-C gave excessive weight to resistance in aggressive chemical environments that do not apply here. Retain both materials for Revision P, with an identified grade and stock form in its forthcoming supplier revision.

POM-C offers established low-porosity machining-stock options. POM-H offers generally higher stiffness, strength and creep resistance. Choose between actual available grades and sound stock rather than treating either polymer family as automatically superior for this application. No geometry or supplier PDF change is needed for this conclusion.

## Coolant evidence

- **Koolance LIQ-705:** Koolance explicitly lists POM among tested plastics. The public listing does not distinguish C/H or publish the complete test temperature, duration and loading, so it is useful compatibility evidence rather than a specific lifetime qualification of our manifold. [Koolance product page](https://koolance.com/liq-705-liquid-coolant-electrically-insulative-5000ml-clear)
- Its April 2024 US SDS reports 50–55% propylene glycol, 45–50% water and small quantities of inhibitors; pH is 5.5–6.5 at 20°C. This is consistent with the operator's non-aggressive coolant service. [Koolance SDS](https://koolance.com/files/products/manuals/Koolance_LIQ-705_SDS_%28English-US%29.pdf)
- **Mayhems X1:** the June 2025 Ice Crystal Clear concentrate SDS identifies glycerol and water as the principal ingredients. It reports pH 7–8 at **10 g/L and 25°C**. This specific SDS measurement must not be represented as the guaranteed pH of every X1 premix or colour. The concentrate must be used at the supplier's prescribed dilution. The chemistry supports retaining both POM families as candidates; the SDS is not a material compatibility test. [Mayhems SDS](https://mayhems.store/pub/media/pdf/mayhems_msds_x1_concentrate_icecrystalclear.pdf)
- Delrin's design guide describes resistance to water, alcohols and many weak acids/bases, and considers temperature, stress and exposure time in service assessment. Its general pH guidance is 4–9. That supports considering POM-H for this duty rather than excluding it on generic hydrolysis comparisons; pH alone is not a compatibility certificate. [Delrin design guide, environmental effects](https://www.delrin.com/wp-content/uploads/2023/01/Delrin-Design-Guide-NA-FNL.pdf)

## What remains relevant at 50°C

Neither material has a general temperature-based exclusion at the proposed 50°C coolant temperature. Both soften progressively with temperature and can creep under sustained fastener/fitting loads. Room-temperature tensile values and dry-air service-temperature ratings must not be used as an assembled pressure or thread-torque rating.

Stock integrity, sealing-land finish, thread quality, fitting loads, differential expansion against the steel plate and leak performance are more useful selection and verification considerations for this design than resistance to strong chemicals. Centreline porosity is stock/process dependent; do not label all POM-C void-free or all POM-H porous. MCAM offers a specifically porosity-free copolymer stock grade and documents the mechanical benefits of its homopolymer grade. [Acetron GP / Ertacetal C](https://www.mcam.com/en/products/shapes/engineering/acetron-ertacetal/acetron-gp-pom-c), [Ertacetal H datasheet](https://www.mcam.com/mam/datasheets/GEP-Ertacetal%C2%AE%20H%20POM-H_en_US.pdf)

Practical selection: accept the supplier's identified, sound unfilled POM-C or POM-H machining stock if it meets the drawing and the selected coolant's compatibility requirements. Prototype leak/thermal testing remains part of assembly qualification, not grounds to reject either polymer family at this stage.

Operator decision, 15 September 2026: retain both POM families and finalise the quotation package. The operator reports cleaning an EK Pro manifold with Blitz Part 2, followed by long satisfactory service. This is relevant field experience supporting the maintenance choice; the exact EK resin grade and exposure conditions remain unspecified. Further C/H comparison does not hold up preparation of the P supplier revision; the earlier O-M02 package remains historical.

## Mayhems Blitz Part 2 / Blitz System cleaning

The operator includes Blitz Part 2 in the intended maintenance regime. Treat correctly diluted, temporary Blitz System cleaning followed by thorough flushing as an intended use for either POM-C or POM-H; this does not by itself justify restricting the body to copolymer. This is an engineering expectation, not a published C/H-specific compatibility certification or an assembly test result.

The current Mayhems instructions describe Blitz System as a whole-loop cleaner. For the documented 125 ml bottle, they specify adding the entire bottle to 1500 ml distilled/purified water, circulating with the pump alone for 6–12 hours, then completing four fresh-water flushes of 5–10 minutes each. Follow the instructions matching the actual bottle/version; older Part 2 dilution instructions differ. Normal cleaning remains pump-only. The subsequent [overrun qualification requirement](blitz-overrun-qualification.md) separately includes foreseeable accidental cleaner exposure at 50°C. [Mayhems instructions, pages 6–7](https://mayhems.store/pub/media/pdf/mayhems_instructions_blitzkit.pdf)

This maintenance allowance is specifically for Part 2 / Blitz System. It does not extend the whole-loop allowance to Blitz Radiator / Part 1. No geometry or drawing material change is needed.

## Foreseeable overdue cleaning

Exact adherence to Blitz drain timing is not an acceptable basis for manifold robustness. The operator requires resilience to delayed draining. See the [overrun qualification targets](blitz-overrun-qualification.md): proposed seven-day minimum and thirty-day extended assessment, with installed fittings and exposures up to 50°C. Both POM families remain candidates, but extended-exposure survival is untested.
