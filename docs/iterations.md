# Stored design iterations

| Iteration | Construction | Location | Status |
|---|---|---|---|
| G | Rear-milled galleries, separate stainless sealing plate, two large EPDM rings | Existing `cad/parameters.json`, `output/cad/`, `output/product-views/` | Preserved baseline; snapshot tag `revision-g-rear-cover` at `8ebd431` |
| H | Two long drilled bores, solid POM rear, four plugged G1/4 end ports | `cad/iterations/H-long-bore.json`, `output/long-bore-H/` | Separate initial design for review |

The annotated local Git tag preserves the complete G source, documentation, CAD and eight unmarked views as they existed before the long-bore iteration. H does not overwrite G's parameters or generated files. H reuses the unchanged front plate design; the builder checks solid equivalence before copying its cut DXF.

To retrieve a separate copy of G without changing the current working tree, use `git archive revision-g-rear-cover` into a new directory. The historical combined rack/rear plate Option C is also preserved in that history but remains unselected.

[Review revision G](product-views.md) · [Review revision H and its manufacturing trade-offs](long-bore-H.md)
