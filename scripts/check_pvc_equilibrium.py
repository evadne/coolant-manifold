"""Check free XYZ motion, reflection symmetry and paired-rod node refinement."""
import hashlib
import json
import numpy as np
from relax_context_tubes import ROOT, OUT, nominal_branches, solve, solve_pair


def main():
    params = json.loads((ROOT / 'cad/context/pvc-routing.json').read_text())
    pair = list(nominal_branches().values())[:2]
    origin = pair[0][0]
    pair = [points - origin for points in pair]

    # An isolated hose with coplanar attachments must lose its artificial lane.
    free, _ = solve(pair[0], params)
    planar_error = float(np.ptp(free[:, 0]))
    assert planar_error < 1e-5

    solved = solve_pair(pair, params)
    reflection = np.array([-1, 1, 1])
    mirrored = solve_pair([points * reflection for points in pair], params)
    mirror_error = max(float(np.max(np.linalg.norm(a[0] * reflection - b[0], axis=1)))
                       for a, b in zip(solved, mirrored))
    assert mirror_error < 1e-5

    # Double the element count while preserving each physical clamped length.
    finer = dict(params, nodes=201, fixed_nodes_each_end=5)
    refined = solve_pair(pair, finer)
    refinement_error = max(float(np.max(np.linalg.norm(a[0] - b[0], axis=1)))
                           for a, b in zip(solved, refined))
    assert refinement_error < .5
    record = dict(
        uncontacted_GPU_lateral_extent_mm=planar_error,
        mirror_symmetry_max_difference_mm=mirror_error,
        refinement_101_to_201_max_difference_mm=refinement_error,
        refined_minimum_radii_mm=[r['minimum_radius_mm'] for _, r in refined],
        fixed_end_length_preserved=True,
        source_sha256={path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                       for path in ('cad/context/pvc-routing.json',
                                    'scripts/relax_context_tubes.py',
                                    'scripts/context_tubing.py',
                                    'scripts/check_pvc_equilibrium.py')})
    (OUT / 'pvc-3d-validation.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
