# Stored design iterations

| Iteration | Construction | Location | Status |
|---|---|---|---|
| G | Rear-milled galleries, separate stainless sealing plate, two large EPDM rings | Existing `cad/parameters.json`, `output/cad/`, `output/product-views/` | Preserved baseline; snapshot tag `revision-g-rear-cover` at `8ebd431` |
| H | Two long drilled bores, 440 mm body, four plugged G1/4 end ports | `cad/iterations/H-long-bore.json`, `output/long-bore-H/` | Preserved at `revision-h-long-bore` / `2ff8019` |
| I | Long bores, 390 mm body, 8 front pairs, 6 M4 mounts | `cad/iterations/I-long-bore.json`, `output/long-bore-I/` | Side-clearance variant |
| J | Long bores, 450 mm body, 9 front pairs, 8 M4 mounts | `cad/iterations/J-long-bore.json`, `output/long-bore-J/` | Maximum-body variant; insertion/installed fit conditional |
| K | Long bores, 410 mm body, 10 front pairs at 40 × 40 mm pitch, 6 M4 mounts | `cad/iterations/K-long-bore.json`, `output/long-bore-K/` | Visual review candidate; 25 mm centre-to-end allowance under review |

The annotated local Git tag preserves the complete G source, documentation, CAD and eight unmarked views as they existed before the long-bore iteration. H does not overwrite G's parameters or generated files. H reuses the unchanged front plate design; the builder checks solid equivalence before copying its cut DXF.

To retrieve a separate copy of G without changing the current working tree, use `git archive revision-g-rear-cover` into a new directory. The historical combined rack/rear plate Option C is also preserved in that history but remains unselected.

[Review revision G](product-views.md) · [Review revision H and its manufacturing trade-offs](long-bore-H.md)

[Compare I/J width variants and translucent views](width-variants.md).

[Review K: ten pairs and end spacing](revision-K-ten-pairs.md).
