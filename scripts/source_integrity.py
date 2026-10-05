"""Verify retained source hashes across exact, reversible maintenance edits.

Historical artefacts are not claimed to have been regenerated or re-reviewed.
Renamed generators are resolved through their explicitly recorded current path.
"""
from pathlib import Path
import hashlib
import json


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_matches(root, path, expected):
    root = Path(root)
    record = json.loads((root / 'cad/source-maintenance.json').read_text())
    change = record['files'].get(str(path))
    if change is None:
        change = next((item for item in record['files'].values()
                       if item.get('current_path') == str(path)), None)
    current = root / (change.get('current_path', str(path)) if change else path)
    if not current.is_file():
        return False
    data = current.read_bytes()
    if digest(data) == expected:
        return True
    if not change or change['after_sha256'] != digest(data):
        return False
    original = data.decode()
    for edit in reversed(change['replacements']):
        if edit['after'] not in original:
            return False
        original = original.replace(edit['after'], edit['before'])
        if digest(original.encode()) == expected:
            return True
    return False
