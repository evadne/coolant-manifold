# Q retention torque and creep

**Engineering assessment, not a part manufacturing instruction.** Fabrication is defined only by the matching current STEP/PDF and supplier remarks.

Applies to the selected **M4 ×10 ISO 7380-1 button screws**, 2 mm steel plate, 10 mm full-form POM threads after entry and 13 mm full-diameter pilots. G1/4 fitting torque is a separate interface and is not specified here. **Operator decision: first assembly dry, without Loctite or other threadlocker.**

## What the calculation can establish

Around **0.10 Nm is a plausible initial prototype test point**. Test 0.08, 0.10 and 0.12 Nm first; extend to 0.15/0.20 Nm on sacrificial coupons to establish margin. **This is a test band, not an established acceptable production range.** A defensible maximum needs actual stock, fastener friction and joint testing. Simply assigning a material shear strength and dividing it by three does not establish lifetime at 50°C.

The [retention calculation](Q-retention-sizing.md) uses a screening thread shear area of 34.4 mm² at 6.75 mm effective engagement. With `T = K F d`, torque implies the following preload. K is an assumed overall friction factor, not a measured property of this joint.

| Torque | Preload, K=0.30 to 0.15 | Mean thread shear including 100 N external load |
|---|---:|---:|
| 0.05 Nm | 42-83 N | 4.1-5.3 MPa |
| 0.08 Nm | 67-133 N | 4.8-6.8 MPa |
| 0.10 Nm | 83-167 N | 5.3-7.8 MPa |
| 0.12 Nm | 100-200 N | 5.8-8.7 MPa |
| 0.15 Nm | 125-250 N | 6.5-10.2 MPa |
| 0.20 Nm | 167-333 N | 7.8-12.6 MPa |
| 0.30 Nm | 250-500 N | 10.2-17.5 MPa |
| 0.50 Nm | 417-833 N | 15.0-27.1 MPa |

Lower friction creates **more** preload at the same torque. At K=0.10, 0.10 Nm gives 250 N before external load, or 10.2 MPa average including the 100 N scenario. A dimensional sensitivity case (screw 0.30 mm shorter, plate 2.10, entry 0.60 and male tip allowance 0.70) leaves 6.30 mm effective overlap and 32.1 mm². That raises this case to 10.9 MPa. The 0.30 mm screw variation is a sensitivity assumption, not a claimed standard tolerance; confirm the purchased screw's specification.

Using the provisional 10 MPa screening allowance, the reduced-engagement case permits 321 N total. Subtracting the 100 N external case leaves 221 N preload. This corresponds to 0.088 Nm at K=0.10, 0.133 Nm at K=0.15 and 0.265 Nm at K=0.30. This wide variation is why an exact allowable torque cannot presently be claimed. At 10 kg rather than the 5 kg planning load, the conservative four-screw sharing calculation also raises the external demand; neither mass nor operator handling force is rated by these calculations.

There is no pressurised rear cover to clamp and no gasket squeeze to generate at these twelve screws. They need to seat and retain the dry rack plate. That makes a low-preload assembly plausible, but no-slip behaviour, plate seating and resistance to loosening must be demonstrated. Do not assume all twelve screws share every handling load equally.

## Is finger tight sufficient?

It may be sufficient to seat this joint; it is **not a reproducible torque specification**. A 5 N finger force at 20 mm gives 0.10 Nm; 10 N at 50 mm gives 0.50 Nm; 20 N at 75 mm gives 1.50 Nm. All could be described casually as hand or finger tightening. Gripping the long arm of an L-key can easily exceed the provisional band.

For prototype work, seat the plate progressively in a crossing pattern using a small controlled driver; no powered driver and no extra final heave. If using an L-key, holding the short lever with fingertips is a useful technique to evaluate, not proof of a torque. Once tested, an instruction such as “gently seat with the short end; do not lean on the long arm” may be practical for builders. Do not publish “finger tight is safe” before representative users and joints have been tested.

The retained plain-head plate does not require an arbitrary high bolt preload, and the screws do not need to approach their steel strength. If uncontrolled conventional metal-joint tightening is an actual product requirement, metal inserts or another load-limiting joint should be evaluated separately; extra unused female thread cannot protect a short screw from stripping its engaged POM threads.

## What long-term creep means here

POM is viscoelastic. Under constant force it deforms progressively (**creep**); when deformation is held approximately fixed, its reaction force reduces (**stress relaxation**). A screwed joint combines both effects. Local thread-flank and bearing deformation can reduce clamp force while the screws remain in the same rotational position. Some deformation can recover after unloading; it is not synonymous with immediate damage or inevitable failure.

Warm service and repeated thermal cycles change the rate. POM and steel also expand differently, so preload and hole registration vary with temperature. In this assembly, relaxation would first allow movement between the plate and body, fretting or loosening. The M4s are dry and do not compress a coolant-cover seal; reduced M4 clamp alone is therefore not equivalent to a leak. Severe movement or damaged retention can still load the fittings and tubing.

A “creep rating” would need an explicit time, temperature, material grade, stress/preload, chemical duty and acceptable residual performance. We have no basis for claiming a ten-year joint life from a room-temperature tensile value or the fact that POM generally supports warm service. Celanese treats creep and stress relaxation separately from short-term strength in its design guide; actual-grade data are needed for lifetime prediction. [Celanese design guide, §3.4](https://www.celanese.com/-/media/Engineered%20Materials/Files/Product%20Technical%20Guides/POM-046_Celcon_DesignGuideTG_AM_0913.pdf).

A proportionate first qualification is representative M4 coupons and an assembled manifold in the supplied stock: establish seating and strip-torque distributions at room temperature and 50°C, then measure clamp/retention loss after 24 h, 168 h and 1,000 h at 50°C plus thermal cycling and repeated assembly. Test the intended mechanical handling loads afterwards. These are proposed test points, not validated durations or a service-life extrapolation. Use instrumented clamping/retention checks where possible; breakaway torque alone is affected by friction and cannot be equated to retained preload. Do not repeatedly retighten test samples and thereby hide their relaxation.

The existing formulated-coolant and Blitz-overrun qualification scope remains separate and applicable. Production torque stays unassigned pending actual-grade evidence. Rebuild numerical sensitivity with `scripts/assess_Q_torque.py`; output `output/analysis/Q-torque.json`.

## Published torque search and threadlocker review

The subsequent search found **KNAUER's AZURA P6.1L service instructions, printed pages 68-69**, listing POM among its plastic component materials and **1.0 Nm for M4**. This is a real manufacturer value for its equipment, but the table does not specify the engaged length, particular resin grade, bearing geometry or our service loads. It cannot establish 1.0 Nm for this manifold. At 1.0 Nm, the simple K=0.15 model implies 1,667 N preload, already beyond the conservative screening capacity used here. [KNAUER manual hosted by Antec](https://antecscientific.com/wp-content/mu-plugins/antec-downloads/files/manuals/serv_manuals/194_0020_04%20-%20P6.1L%20pump%20service%20manual_v4.2%20V6895.pdf).

The Delrin-hosted DuPont guide also publishes screw-stripping calculations and data, but its relevant tables concern **self-tapping screws**, not the ISO7380 machine screws in our pre-tapped M4 holes. Those data are useful evidence that joint geometry and thread type matter, not a transferable installation torque. [DuPont design principles, §10](https://www.delrin.com/wp-content/uploads/2023/10/General-Design-Principles-for-Engineering-Polymers.pdf).

**Result: no directly applicable, published final torque was found for our exact joint.** Retain 0.10 Nm as an initial dry-joint test setting, not a claimed manufacturer recommendation or production maximum. Establish the right production value using matching-stock coupons: select a setting that seats the plate, meets the required handling retention after warm dwell, and remains comfortably below the measured stripping distribution. A proposed short-term stripping margin of at least three against the lower observed result is a starting criterion, not statistical confidence from one coupon. Do not transfer generic stainless M4 torque tables or substitute unmeasured “finger tight”.

**Loctite is product-specific.** Henkel identifies **425** as a low-strength adhesive for metal and plastic fasteners, so it is a candidate to trial on these dry M4 joints. Its published breakaway data are on zinc-plated fasteners, not stainless/POM M4, and do not give an installation torque for this assembly. Test actual-grade adhesion, removal without POM damage, warm exposure and any influence of pre-application on tightening friction. It is not yet specified as a supplied treatment. [LOCTITE425 TDS](https://datasheets.tdx.henkel.com/LOCTITE-425-en_GL.pdf).

Do not substitute ordinary **243** without compatibility confirmation: Henkel's TDS says it is not normally recommended for plastics, particularly thermoplastics that may stress-crack. Threadlocker can resist rotation; it cannot restore clamp preload that has relaxed. No adhesive is specified for G1/4 sealing or allowed to migrate into coolant galleries. [LOCTITE243 TDS](https://datasheets.tdx.henkel.com/LOCTITE-243-en_GL.pdf).

The operator's EK manifold has reportedly remained secure after two years of 24/7 operation. That supports a proportionate test programme and distinguishes observable retention from small, unmeasured preload changes. Normal coolant oscillation is not automatically thermal shock. Twelve fixings provide distributed retention, but shared material and assembly conditions mean their behaviour should not be modelled as twelve statistically independent failure events. Sudden simultaneous screw loss is not asserted or expected by this assessment.
