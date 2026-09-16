# Revision register

**Current:** Q-M04 manifold body, Q-M03 faceplate and radiator R7 / R7-M01. Both steel plates have four R5 outside corners and retain ±0.10 mm cut dimensions/coordinates. All other geometry is retained. New steel bundles remain held for future repeat orders; original supplier-order files stay unchanged.

## Manifold history

| Revision | Main change | Status / location |
|---|---|---|
| G | Rear-milled galleries, separate rear cover and two large rings | Historical baseline; `cad/parameters.json`, unversioned `output/cad/` and `output/product-views/`; tag `revision-g-rear-cover` |
| H | Two long bores and four side ports; removed rear cover | Historical; `cad/iterations/H-long-bore.json`, `output/long-bore-H/`; tag `revision-h-long-bore` |
| I / J | 390 mm /8-pair and 450 mm /9-pair width variants | Historical; matching iteration/output directories |
| K | 410 mm body, ten pairs at 40 ×40 | Historical; tag `revision-k-ten-pair` |
| L | Six optional rack positions per side | Historical; tag `revision-l-six-rack-positions` |
| M | Six POM retainers at balanced X−120/0/+120 columns | Historical; tag `revision-m-before-centred-depth` |
| N | 35 mm slab and centred galleries | Historical rejected depth candidate; tag `revision-n-35mm-centred` |
| O | Restored 40 mm slab, galleries at Y20 | Historical operator-approved predecessor; tag `revision-o-operator-approved` |
| O-M01 / O-M02 | Manufacturing details, then 4 mm bosses above a 3 mm countersunk plate | Superseded supplier issues; `cad/manufacturing/` and `output/manufacturing/`; do not submit as Q |
| **P** | 2 mm plain-hole plate, twelve M4 ×16 button screws, 3 mm bosses, revised M4 depths | Historical predecessor, `cad/iterations/P-long-bore.json`, `output/long-bore-P/`; [detail](revision-P-plain-bore-faceplate.md) |
| **Q** | Four rear G1/4 ports aligned with outer front pairs; P front geometry retained | **Current operator-approved geometry / Q-M04 body, Q-M03 faceplate**, `cad/iterations/Q-rear-ports.json`, `output/long-bore-Q/`; [detail](revision-Q-rear-ports.md). M4: 10 mm full thread, 13 mm pilot. |

P's official Koolance studio fitting update and operator acceptance are presentation/installation decisions, not new manufactured-part revisions. Source geometry remains unchanged.

## Radiator history

| Revision / issue | Main change | Status |
|---|---|---|
| R1 | 3 mm flat rack plate | Historical; early thickness/FEA studies also evaluated thinner versions of this profile |
| R2 | 2 mm, integral 10U, forty optional rack slots | Historical |
| R3 | Added tapped M4 fan holes and R50 aperture corners | Historical unselected alternative |
| R4 / R4-M01 | Plain fan holes and nuts; accepted assembly sequence | Superseded geometry/pack; its final load analysis remains baseline evidence |
| R5 / R5-M01 | 10 ×5 mm cable notch | Historical deeper-notch version |
| **R6 / R6-M02** | **10 ×2 mm rounded cable notch**, same fan/fixing pattern | Historical submitted geometry; M02 specifies raw sheet finish |

## Archive policy

Superseded writeups are in [archive](archive/README.md), labelled historical. Their original revision-specific CAD, render and analysis paths remain available for traceability and script dependencies. Unversioned legacy manifold outputs are G, not the current design. See [output guide](../output/README.md).

Git preserves all earlier revisions, recaps and README/AGENTS history. Retrieve a snapshot into a separate directory with `git archive <tag-or-commit>` when needed; do not replace the current files to inspect history. Older descriptions saying “current”, “selected” or “next” apply only to their labelled snapshot.

## StarTech25U context update —15 September2026

The composite now uses the manufacturer-informed4POSTRACK25U at minimum22in mounting depth, reserves lowerU1 for radiator plumbing and uses Q/R7. Front PVC routes use the accepted shortened free-XYZ rod/contact solution; infrastructure retains geometric65 mm bends. See [current context](context-25U.md). This is an installation iteration, not a new custom-part revision.

## 16 September steel tolerance issues

- **Q-M02 faceplate:** all cut sizes and X/Z coordinates ±0.10; standard grinding/deburring, no dimensioned face-edge break. Q-M04 body unchanged.
- **R6-M03 radiator:** all cut sizes, profile radii and X/Y coordinates ±0.10; separate flatness and edge finishes unchanged.
- STEP/DXF geometry byte-identical to previous issues. Original submitted archives preserved; current local index selects the two new issues.

## R5 outside-corner issues — 16 September 2026

- **Q-M03 faceplate:** four square outside corners become R5; Q-M04 POM and every cut opening/position are unchanged. Nominal mass 0.394607 kg.
- **R7 / R7-M01 radiator:** four outside corners increase R2 → R5; all fan/radiator holes, rack slots, R50 apertures and 10 ×2 notch are unchanged. Nominal mass 1.247067 kg.
- Both preserve the held ±0.10 mm cut-size/coordinate specifications, raw finish and separate edge treatments. Fresh STEP/DXF/PDF, eleven Q inspection views, four studio views, seven radiator views and nine rack views replace current presentation outputs. No supplier upload.

## Q-M04 body — 16 September 2026

Twelve main-slab outside edges gain C0.50 ±0.10 ×45° ±1° chamfers with modelled corner junctions. All functional geometry is retained. Held body issue replaces Q-M01 locally; submitted originals are untouched. Steel remains Q-M03 / R7-M01. Three new body drawing sheets and 25 affected renders refreshed; total current presentation set 32 images.
