# Q-M04 POM: likely machining route and axis requirements

Engineering assessment, 16 September 2026. This is a process-feasibility review of the submitted part, not JLC's actual CAM programme or confirmation of its equipment. It does not modify the fabrication package.

**Simultaneous five-axis machining is not required by the geometry.** A suitably equipped three-axis machining centre, with the part re-fixtured for different faces, can produce it. The principal capability question is deep drilling, together with workholding and machine clearance. An ordinary three-axis mill with only standard short drills is insufficient; adding rotary axes alone does not solve that limitation.

## Basis checked

- STEP: `output/manufacturing/Q-M04/RM10-Q-M04-BODY.step`.
- SHA-256: `4a74cb2bdcdad374159c58848f8b74530f83332fb091012a047a6942e433e881`.
- Matching Q-M04 feature schedule, manufacturing configuration, drawing generator and existing geometric verification.
- Slab 410 × 87 × 40 mm; twenty Ø28 bosses project 3 mm from the front. Overall depth 43 mm.
- Two Ø11.8 × 410 mm galleries run along X, at Y20 and Z23.5/63.5. Front/rear port axes run along Y. No angled fluid passages or inaccessible milled pockets.
- Twenty front, four rear and four end G1/4 ports; twelve front M4 retention holes. All forty threaded holes have ordinary orthogonal access. The STEP represents tapping pilots; the PDF defines finished threads.

## Plausible operation sequence

| Stage | Likely toolpath and workholding | Axis implication |
|---|---|---|
| Prepare stock and datums | Saw oversize stock, face and square it, rough the envelope while retaining boss stock. Use distributed support and controlled clamping. Allow temperature and distortion to settle before critical finishing. | Conventional facing/profile milling; stock preparation can require additional clampings. |
| Drill galleries from an end | Locate both axes from common datums. Prepare guided entries and drill the longitudinal galleries with suitable long-hole tooling; an independent horizontal deep-drilling machine is also a viable production route. | Fixed-axis drilling. Tool reach, guidance, chip removal and machine envelope matter more than rotary axes. |
| Finish both end faces | Machine sealing surfaces and entries; tap the two G1/4 mouths on each end. Re-fixture to access the opposite end. | Two opposed fixed orientations. |
| Machine front | Clear the shallow area around twenty circular boss islands; finish the mounting face, boss sealing faces, R1 roots and C0.5 lips. Drill twenty branch pilots and twelve M4 pilots; cut entries and threads to drawing depths. | Mostly 2.5D pocket/profile paths and axial drilling/tapping. A corner-radius cutter or ball-end finishing can produce the roots. |
| Machine rear | Support the body in a fixture relieved around the finished bosses. Finish four rear seal lands, branch pilots, entries and G1/4 threads. | Another fixed orientation; protect finished front sealing surfaces. |
| Complete edge finishing and inspect | Cut accessible slab chamfers during the relevant setups, finish the eight corner flats, externally deburr, flush loose chips and inspect finished features. | Ordinary chamfer paths plus local three-axis surface finishing; no internal cross-hole deburring operation is added. |

This suggests **four principal feature orientations: front, rear, left end and right end**. It is not a promise of four total clampings: stock squaring, support access and finishing may add operations. Machining the front boss pattern and M4 pattern together reduces registration error. Indexed 3+2 machining can automate reorientation and reduce handling, but is an efficiency choice rather than a shape requirement. Haas distinguishes indexed five-sided work from simultaneous five-axis contouring in its [machine guidance](https://www.haascnc.com/machines/multi-axis/5-axis-mills.html).

Engineering preference: make the long galleries before opening the intersecting front/rear branches. That gives the long drill a more continuous cut instead of repeated cross-hole interruptions. The supplier may select another validated sequence. Final threads must still meet the specified full-form depths and run-out limits; a suitable tap or thread-milling process must leave the required bottom clearance.

## Deep-hole constraint

| Candidate route | Nominal reach per direction | Depth/diameter | Main consideration |
|---|---:|---:|---|
| Drill through from one end | 410 mm | 34.75D | Long guided tool and chip evacuation; avoids a meeting point between independently drilled halves. |
| Drill from both ends | Approximately 205 mm each, plus overlap/point allowance | More than 17.37D | Shorter tools, but datum transfer and drill wander can produce a step or mismatch near the centre. |

The second route does not inherently require a design change, but its result must comply with the current drawing. This assessment does not authorise extra bore mismatch, an internal ridge or relaxed tolerances.

[Botek's machining-centre deep-drilling guide](https://www.botek.de/downloads/en/Brochuere_BAZ_EN.pdf) describes guided drilling at 40D and beyond, using appropriate equipment, pilot guidance and coolant/chip-removal systems. This establishes that our approximately 35D ratio is within the general deep-drilling process class; it is not a POM-specific tool selection or evidence of JLC's capability. Tool geometry and machining fluid must suit the selected POM stock. Ordinary twist-drill peck cycles and guided gundrilling are different processes; do not prescribe one generic cycle for both.

For a vertical mill, standing a 410 mm body on end beneath a long drill can be an awkward clearance and support problem. Horizontal drilling, a suitable attachment or a dedicated deep-hole station may be more practical. A five-axis trunnion can itself consume available space. The supplier needs enough travel and clearance for the body, fixture, exposed tool and holder, not merely a table long enough for a 410 mm part.

POM cutting forces are relatively modest, but heat, long-drill wander, chip packing and clamping distortion still affect the result. Preserve the drawing's functional surfaces and locations: seal-land Ra1.6 and flatness 0.05 mm, mounting-face flatness 0.15 mm and M4 coordinates ±0.05 mm. These are process-control considerations, not reasons to require five axes.

## Eight corner flats

Direct STEP inspection finds eight triangular planes, each approximately 0.216506 mm² with 0.707107 mm sides. Their normal vectors have components ±1/√3; each normal is 54.7356° to a primary axis. Consequently, they are compound-angle facets, distinct from the twelve 45° edge chamfers.

They are exposed convex features. A fixed-axis ball-end cutter can surface them with three-axis XYZ moves and an appropriately small stepover; front/rear access can cover the corresponding corners if the fixture permits. An angled fixture or suitable form tool is another option. They do not require continuous tool-axis rotation or eight independent special setups. Exact cutter/holder clearance and finish still need CAM verification. [Autodesk's parallel-finishing guidance](https://help.autodesk.com/cloudhelp/ENU/Fusion-CAM/files/3D-PARALLEL-STEPS.htm) describes ball/bull-nose surface finishing; its application to these particular facets is our geometric assessment, not an executed toolpath simulation.

## Cost interpretation

Likely cost contributors are deep-drill tooling/setup, several orientations, forty threaded holes, boss/seal finishing and inspection. The small corner facets add programming/finishing detail but do not turn the whole part into a simultaneous five-axis job. It is plausible that the earlier manual quotation accounted for deep drilling; JLC has not supplied an itemised explanation, so that remains an inference.

The useful supplier capability question is: **Can the chosen process hold the specified Ø11.8 galleries and functional features over this 410 mm body?** Whether its chosen machine happens to have three or five axes is secondary. No design or order changes follow from this assessment.
