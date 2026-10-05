# Mathematical assessment of the 2 mm radiator rack plate

> **Historical reference — superseded.** This page describes an earlier design or assessment. Its recommendations and “current” labels apply only to that snapshot. Use the [current project guide](../../README.md) and [three-part recap](../three-part-recap.md) for P / R6.


**The full-plate static calculation supports using 2 mm stainless steel for the specified load and fixing arrangement.** The earlier strip calculation was only a local estimate. This study uses the complete R1 cut profile, including the four openings, twelve radiator holes and twelve rack slots, and varies the sheet thickness without changing the released 3 mm CAD.

## What is being calculated

Steel does not have a threshold below which it never bends. It deforms elastically under load and springs back when unloaded. Two useful design questions are how much it moves and whether stress approaches the material's proof strength, beyond which permanent deformation becomes significant.

For an elastic isotropic plate, flexural rigidity is

`D = E t³ / [12 (1 - ν²)]`.

With E = 200 GPa, ν = 0.3 and t = 2 mm, D = 146,520 N mm. The load, cut-outs and boundary conditions then determine deflection and stress. This perforated plate with multiple discrete supports is better represented by finite elements than by a single beam formula.

## Model and loading

- Solver: CalculiX 2.23, Debian package 2.23-1, using quadratic S6 shell elements; Gmsh 4.15.2 generates the mesh from the exact CAD face. E = 200,000 N/mm², ν = 0.3, density 7900 kg/m³. Small-displacement, linear elastic calculation.
- Payload: 4.225 kg radiator net +2 kg allowance =6.225 kg. Apply 61.0464 N downward and a 4,578.48 N mm overturning moment from a 75 mm centre-of-gravity offset behind the plate. Include the plate's own weight separately (gravity 9.81 m/s² for this body load).
- Normal case: share gravity across all twelve radiator holes. Normal forces proportional to each hole's height relative to the centre provide the required moment with zero net normal force. Nodal loads are spread around each hole's circumference.
- Secure eight rack positions, four per side, at R1 rows B1/B3/B4/B6. Constrain translation on those slot boundaries. Shell rotations are not explicitly fixed. The other four slots remain unrestrained.
- Sensitivity case: only four outermost rack positions secured; all downward payload force enters through the two uppermost radiator holes. Only the four outer radiator holes carry the moment couple. This is a separate less favourable load/support assumption, not a claimed worst case of every possible installation.
- Radiator structural reinforcement, bolt preload, washer contact and friction are not modelled. The radiator's actual attachment rails and threaded features are outside the plate mesh. Support constraints assume secured fixings without slip; neither this nor the alternative is a loose-bolt analysis.

## Results

| Sheet thickness / case | Plate mass | Maximum out-of-plane displacement | Peak recovered surface von Mises stress |
|---|---:|---:|---:|
| 3 mm, eight rack fixings | 1.697 kg | 0.0135 mm | 6.2 MPa |
| **2 mm, eight rack fixings, refined mesh** | **1.131 kg** | **0.0429 mm** | **14.0 MPa** |
| 1.5 mm, eight rack fixings | 0.848 kg | 0.0989 mm | 25.2 MPa |
| 2 mm, four rack fixings / upper gravity loading | 1.131 kg | 0.0493 mm | 14.9 MPa |

The largest plate movement is near the centre of the upper/lower border, rather than at a radiator fixing. The peak calculated stress is local to the supported regions. The 2 mm refined model's maximum downward displacement is about 0.00094 mm. This is movement of the idealised steel plate, not movement of a real rack including fastener clearance and flexible rails.

For context, [Outokumpu's Core range datasheet](https://www.outokumpu.com/-/media/files/products/core/outokumpu-core-range-datasheet.pdf) gives a 230 MPa minimum 0.2% proof strength for cold-rolled 304 / EN 1.4301 sheet at 20°C. The 2 mm model's 14-15 MPa peak is well below that. This supports a conclusion of small elastic bending under the stated stationary load; it is not a certified assembly load rating or a rating for transport/drop/shock forces. Even 1.5 mm is not predicted to approach yielding in the modelled static case. Choosing 2 mm retains more stiffness for handling and installation while saving 566 g against R1.

## Numerical checks

1. **Analytical beam benchmark:** a 100 ×20 ×2 mm cantilever with a 10 N tip load, E =200 GPa and ν =0, calculated with the same S6 elements. Euler-Bernoulli theory gives 1.250 mm tip deflection and 75 MPa root bending stress. The solver gives 1.25025 mm mean tip deflection (0.020% difference) and 74.73 MPa recovered peak surface stress. Setting ν =0 removes the plate's lateral Poisson restraint from this beam comparison; the actual rack plate uses ν =0.3.
2. **Mesh refinement:** the 2 mm normal case grows from 18,662 S6 elements /38,763 nodes to 40,374 elements /82,941 nodes. Maximum deflection changes by 0.157%; recovered peak stress changes by 0.595%. These results are sufficiently stable for this model comparison; they do not remove uncertainty in the real joint assumptions.
3. **Equilibrium:** input nodal forces reproduce the payload force and moment. Support reaction forces and their overturning moment balance the applied loads to better than 0.1%, including plate self-weight.
4. **Stress recovery:** the solver reports stresses at nine integration points per S6 element. Matching outer through-thickness layers are extrapolated linearly to the two sheet surfaces; the plotted value is the maximum von Mises value per element across those surface samples. There is no in-plane extrapolation to the hole edge and no additional stress concentration factor. Peak values remain dependent on how the fastener support/contact is idealised.

## Why rack posts are not a direct thickness comparison

A thin folded channel or angle can be very stiff because the cross-section places material farther from the bending axis: bending stiffness depends on E I, not thickness alone. Rack posts also carry much of their service load as axial compression. A flat radiator panel has a different load path and an eccentric attached load. Rack material is not necessarily stainless: for example, [Eaton's open-frame SmartRack specification](https://assets.tripplite.com/product-pdfs/en/sr4post50hd.pdf) describes coated cold-rolled steel. Do not infer the material or gauge of the operator's particular rack from appearance.

## Design conclusion and reproducibility

Use **2 mm as the next radiator plate design thickness**, retaining the present border, cross web and fixing arrangement. The mathematical result supports that choice for the stated static duty. A fit check still needs to verify the radiator's own attachment capacity and screw engagement; reducing plate thickness without changing screw length adds 1 mm of insertion. This analysis is not a reason to require a thicker sheet solely because the full assembly has not been physically tested. Preserve the 3 mm R1 files as the baseline; a 2 mm revision should carry its own revision and updated screw-length note.

Files:

- `scripts/radiator_plate_fea.py`: generate shell solver decks and node metadata in `output/radiator-FEA/`.
- `scripts/review_radiator_fea.py`: parse DAT files, check the benchmark/equilibrium/convergence and produce the plot and summary.
- `requirements-fea.txt`: optional local dependencies in addition to the project's CAD requirements.
- `output/radiator-FEA/results.json`: results and numerical checks.
- `output/radiator-FEA/2mm-plate-analysis.png`: visually inspected displacement and stress fields, on the undeformed outline.
- `output/radiator-FEA/*.inp.gz` and `*.dat.gz`: compressed solver input and result evidence for all six cases.

Reproduce the six decks with the generator options: `--benchmark --size 3`; `--size 6 --thickness 3`; `--size 6 --thickness 2`; `--size 3 --thickness 2`; `--size 6 --thickness 1.5`; and `--size 6 --thickness 2 --supports 4 --load top`. Run each with `ccx -i <case-name>` and place its DAT alongside its working JSON before running the review script. The calculations were run on the operator-provided Linux host using two OpenMP threads and one OpenBLAS thread.

Primary method references: [CalculiX author and downloads](https://www.dhondt.de/), [CalculiX 2.23 manual, shell elements and result output](https://www.dhondt.de/ccx_2.23.pdf), and [Gmsh 4.15.2 manual](https://gmsh.info/doc/texinfo/). Checked 15 September 2026. No supplier submission, order or manifold modification.
