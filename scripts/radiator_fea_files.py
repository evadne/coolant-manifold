"""Locate retained solver evidence by study; compressed files work directly."""
from pathlib import Path
import gzip

ROOT = Path(__file__).resolve().parents[1]


def case_directory(name):
    if name.startswith('R2-'):
        return ROOT / 'output/radiator-R2/analysis'
    if name.startswith('R4-'):
        return ROOT / 'output/radiator-R4/analysis'
    if name.startswith('expanded-'):
        return ROOT / 'output/radiator-expanded-load'
    return ROOT / 'output/radiator-FEA'


def case_bytes(name, extension):
    path = case_directory(name) / f'{name}.{extension}'
    if path.exists():
        return path.read_bytes()
    return gzip.decompress(path.with_suffix(path.suffix + '.gz').read_bytes())
