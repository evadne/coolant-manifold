# Revision M body-depth assessment

The current main POM slab is 40 mm deep. Its integral bosses add 6 mm, giving 46 mm overall POM depth. The 3 mm front plate occupies part of that boss projection; it does not add another 3 mm to the overall assembly depth. The following proposals refer to slab depth, excluding bosses.

There is no established structural requirement for a 40 mm slab. It is the retained layout dimension, with the longitudinal gallery axes at Y26. Reducing depth is geometrically plausible after moving those axes forwards and shortening the front branch drilling accordingly. Revision M CAD and presentation files remain unchanged; these are assessment candidates, not new manufacturing revisions.

| Dimension (mm) | Current | 35 mm candidate | 30 mm candidate |
|---|---:|---:|---:|
| Main slab depth | 40 | 35 | 30 |
| Overall POM depth including bosses | 46 | 41 | 36 |
| Gallery axis behind slab front, Y | 26 | 20 | 15 |
| Nominal front ligament to Ø11.8 gallery, away from branch holes | 20.1 | 14.1 | 9.1 |
| Nominal rear ligament to Ø11.8 gallery | 8.1 | 9.1 | 9.1 |
| Minimum front/rear edge reserve around Ø22 side sealing land | 3 | 4 | 4 |
| End of 8 mm full front thread to nearest gallery surface | 18.1 | 12.1 | 7.1 |
| Minimum distance from conservative Ø4 × 14 M4 envelope to gallery cylinders | 12.922 | 9.792 | 8.634 |

Distances to the gallery cylinders were checked with CadQuery/OpenCascade using Revision M fixing positions. These are nominal geometry checks, not a regenerated complete assembly or structural analysis. The side thread-major envelope is larger than the Ø11.8 gallery: its rear reserve is approximately 7.42 mm currently and 8.42 mm in both candidates. Drill wander and manufacturing tolerances still consume reserve.

Simply trimming the current back is unsuitable: retaining Y26 leaves only 3.1 mm behind the gallery in a 35 mm slab, and the Ø22 side land extends 2 mm beyond its rear edge. A 30 mm slab would intersect the existing gallery by 1.9 mm. Moving the axes is therefore part of either proposal.

Long bores leave a largely solid section surrounding two round passages, with no broad rear opening, sealing grooves or rear-cover fasteners. That makes a thinner body worth evaluating. Reducing slab depth does not change gallery diameter, long-bore drilling length or the parallel-only topology. It shortens the front branches. It does not solve the existing deep-drilling manufacturing question.

Thinner POM is less rigid. As a simple gross rectangular-beam comparison, front/back bending stiffness across the rack width scales with slab depth cubed: 35 mm retains about 67% of the 40 mm slab's stiffness, and 30 mm about 42%. Vertical bending stiffness for the same gross section scales linearly with depth. These are directional section comparisons, not assembled-manifold deflection predictions: bores, bosses, six discrete fixings, the faceplate, connection slip and actual loads affect the result. The unchanged steel faceplate mounts the assembly to the rack, but its contribution cannot be treated as a perfectly bonded composite without analysis.

The 35 mm / Y20 candidate is the preferred next design iteration: it reduces depth while retaining generous nominal sealing and thread clearances. The 30 mm / Y15 candidate also fits the nominal passage, thread and sealing-land geometry, but deserves a closer stiffness and fitting-load assessment. Neither is pressure- or load-qualified. Actual POM grade, temperature and sustained hose loads matter because polymer creep changes stiffness over time; see the manufacturer's [Delrin design guide](https://www.delrin.com/delrin-design-guide/).

Moving side ports 6 mm or 11 mm towards the front also moves the elbow envelopes. Recheck the rack flanges, selected cage nuts, screw tails and insertion path before carrying forward earlier installed-clearance conclusions. The 30 mm candidate also violates the generator's conservative requirement that all M4 pilots terminate in front of the gallery's Y range; that requirement is sufficient but not necessary when the holes are separated in Z. A future CAD revision must replace it with complete three-dimensional wet-network clearance checks rather than simply deleting the check.
