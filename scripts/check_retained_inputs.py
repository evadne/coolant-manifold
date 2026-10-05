"""Check that display inputs and structural evidence exist without local caches.

Standard-library only; read-only. Does not render, solve or qualify the design.
"""
from pathlib import Path
import gzip
import json
import struct
from radiator_fea_files import case_directory, case_bytes

ROOT = Path(__file__).resolve().parents[1]


def check():
    scenes = [ROOT / 'output/render-scene.json', ROOT / 'output/backplate/render-scene.json']
    scenes += [ROOT / f'output/long-bore-{r}/render-scene.json' for r in 'HIJKLMNOP']
    for path in scenes:
        scene = json.loads(path.read_text())
        assert scene['parameters']['revision'], path
        assert scene['ports_x'], path
        assert (path.parent / 'meshes/body.stl').is_file(), path
    directories = [p.parent / 'meshes' for p in scenes]
    directories += [ROOT / 'output/long-bore-Q/meshes', ROOT / 'output/manufacturing/O-M02/meshes']
    meshes = []
    for directory in directories:
        files = sorted(directory.glob('*.stl'))
        assert files, directory
        for path in files:
            data = path.read_bytes()
            assert len(data) >= 84, path
            triangles = struct.unpack_from('<I', data, 80)[0]
            assert triangles > 0 and len(data) == 84 + 50 * triangles, path
            meshes.append(path)
    for i in (1, 2):
        assert ROOT / f'output/long-bore-Q/meshes/fluid-network-{i}.stl' in meshes
    cases = []
    for directory in ['output/radiator-FEA', 'output/radiator-expanded-load',
                      'output/radiator-R2/analysis', 'output/radiator-R4/analysis']:
        for path in sorted((ROOT / directory).glob('*.dat.gz')):
            name = path.name.removesuffix('.dat.gz')
            assert case_directory(name) == path.parent
            meta = json.loads(case_bytes(name, 'json'))
            assert len(meta['node_ids']) == len(meta['coordinates']) == meta['nodes'], name
            assert len(meta['elements_connectivity']) == meta['elements'], name
            assert b'*NODE' in case_bytes(name, 'inp'), name
            assert b'displacements (' in gzip.decompress(path.read_bytes()), name
            cases.append(name)
    assert len(cases) == 16, cases
    return {'checks': 'PASS', 'scene_descriptions': len(scenes), 'display_meshes': len(meshes),
            'complete_solver_cases': len(cases)}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
