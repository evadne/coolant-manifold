"""Check retained source hashes across explicitly recorded maintenance edits.

This never accepts an arbitrary changed generator. Each exception pins both
versions and reverses the exact recorded edits to recover the original hash.
It does not claim that historical artefacts were regenerated or re-reviewed.
"""
from pathlib import Path
import hashlib
import json


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_matches(root, path, expected):
    root = Path(root)
    data = (root / path).read_bytes()
    if digest(data) == expected:
        return True
    record = json.loads((root / 'cad/source-maintenance.json').read_text())
    change = record['files'].get(str(path))
    if not change or change['before_sha256'] != expected or change['after_sha256'] != digest(data):
        return False
    original = data.decode()
    for edit in reversed(change['replacements']):
        if edit['after'] not in original:
            return False
        original = original.replace(edit['after'], edit['before'])
    return digest(original.encode()) == expected
