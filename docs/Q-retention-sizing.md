# Q M4 retention sizing

**Engineering assessment, not a part manufacturing instruction.** Fabrication is defined only by the matching current STEP/PDF and supplier remarks.

15 September 2026. The operator requested a mathematical check of shorter retention threads. **Use 10 mm minimum full-form M4 thread after the entry, with M4 ×10 ISO 7380-1 button screws through the 2 mm steel.** Following the operator’s further instruction, reduce the pilot to 13 mm full diameter plus its 118° drill point, which leaves 2.45 mm for tap lead/run-out beyond the minimum full thread. This Q-M01 refinement changes the twelve pilot tails in the Q STEP; it does not move any hole or change the galleries. The operator selected ×10 rather than ×12 to leave additional allowance for screw/plate tolerances. Nominal screw insertion is 8 mm and clearance to the full-diameter pilot bottom is 5 mm. The twelve head positions and visible head dimensions remain unchanged.

G1/4 remains **8 mm minimum full-form thread after the 1 mm entry**. That female depth provides accommodation, not an assertion that a bought-in fitting engages all 8 mm; male thread lengths differ. Sealing is on the fitting's O-ring and POM land. No female depth can guarantee compatibility with every product carrying a G1/4 thread.

## Screening calculation

Use an approximate thread-strip shear cylinder, counting half the axial length as load-bearing tooth material:

`A_s = pi × D1 × L_e / 2`, with basic M4 ×0.7 minor diameter `D1 = 4 - 1.082532 ×0.7 = 3.242 mm`.

`L_e = screw length - 2 mm plate - 0.55 mm female entry - 0.70 mm male-tip allowance`.

| Screw | Effective overlap L_e | Screening shear area | Force at assumed 10 MPa shear |
|---|---:|---:|---:|
| M4 ×8 | 4.75 mm | 24.2 mm² | 242 N |
| **M4 ×10 (selected)** | **6.75 mm** | **34.4 mm²** | **344 N** |
| M4 ×12 | 8.75 mm | 44.6 mm² | 446 N |
| M4 ×16 | 12.75 mm | 64.9 mm² | 649 N |

A deliberately explicit planning case is 5 kg supported mass at 100 mm behind the plate, with only four screws effectively sharing load. The resulting 4.90 Nm gravity moment produces 33.6 N axial tension per top screw when two top screws oppose two bottom screws 73 mm apart. Add a local 100 N axial handling pull shared by two nearby screws: 83.6 N per screw, rounded up to **100 N external axial force per screw**. Direct gravitational shear is only 12.3 N per participating screw; no friction credit is needed for that comparison. These are assumed scenarios, not measured maximum user forces or a load rating.

Preload dominates. `F_preload = T/(K d)` with an illustrative 0.20 Nm tightening point, M4 diameter and assumed nut factor 0.15-0.30 gives **167-333 N**. Conservatively adding all 100 N external load gives 267-433 N. For the M4 ×12 effective engagement the upper case is **9.73 MPa average shear**; for ×10 it is 12.6 MPa and for ×8 17.9 MPa. At 0.5 Nm and K=0.15, preload alone rises to 833 N: shortening the thread cannot be separated from assembly control.

The 10 MPa screening allowance is an engineering assumption, **not a published creep allowable at 50°C**. Celanese cautions that punched-specimen shear strength includes other effects and recommends limiting a shear estimate to the smaller of published shear strength and half tensile strength. Ensinger lists 67 MPa tensile strength for its black TECAFORM AH stock, but that is one named material, not the yet-unselected JLC grade. Long-term relaxation, first-thread load concentration, temperature, fluid exposure and repeated assembly remain outside the simple calculation. [Celanese design guide, §3.3.7 and §3.4](https://www.celanese.com/-/media/Engineered%20Materials/Files/Product%20Technical%20Guides/POM-046_Celcon_DesignGuideTG_AM_0913.pdf), [Ensinger TECAFORM AH black](https://www.ensingerplastics.com/de-de/halbzeuge/pom-c-tecaform-ah-black).

The retained **10 mm full tapped length and selected M4 ×10 screw are a prototype specification**. Extra tapped length does not add strength beyond the male screw overlap. At the selected 6.75 mm effective engagement, the 100 N external-only case is 2.91 MPa; the upper 433 N preload-plus-load scenario is 12.6 MPa and **exceeds the assumed 10 MPa screening allowance**. At an illustrative 0.10 Nm and K=0.15 the total drops to 267 N /7.76 MPa. These comparisons support a low-load joint with controlled assembly, but do not justify a blanket strength or hand-tightening claim. It does not establish that every POM grade can sustain the assumed stress indefinitely. The 0.10/0.20 Nm values are comparison/test points only; no production torque is released. Test the actual stock and screw/plate joint for strip torque, clamp relaxation and retention at intended temperature before assigning one. No verified EK internal tapping-depth measurement is available, so its construction is not numerical proof.

JLC recommends effective thread length no more than three diameters and unthreaded bottom allowance of at least half a diameter. The revised 10 mm thread is 2.5× nominal M4 diameter, with 2.45 mm remaining full-diameter pilot. [JLC threaded-hole guideline](https://jlccnc.com/help/article/threaded-hole-guideline).

Rebuild: `.venv/bin/python scripts/assess_Q_retention.py`. Results: `output/analysis/Q-retention.json`. Q-M01 drawings and assembly references use the shorter hardware; historical P continues to specify ×16.

First assembly is explicitly dry, without Loctite; see [torque and creep review](Q-torque-and-creep.md).
