"""Read retained manufacturing metadata using the current revision vocabulary.

Old supplier/review records are immutable. Translate their explicitly listed
schema keys in memory; never rewrite their text, filenames or hash dictionaries.
New metadata is written with the descriptive keys used by the current tools.
"""
import json as _json

LEGACY_KEYS = {
    'issue': 'manufacturing_revision',
    'issue_date': 'manufacturing_revision_date',
    'issue_bundle': 'manufacturing_revision_bundle',
    'source_issue': 'source_manufacturing_revision',
    'body_issue': 'body_manufacturing_revision',
    'faceplate_issue': 'faceplate_manufacturing_revision',
    'manifold_body_issue': 'manifold_body_manufacturing_revision',
    'manifold_faceplate_issue': 'manifold_faceplate_manufacturing_revision',
}


def normalise(value):
    if isinstance(value, list):
        return [normalise(item) for item in value]
    if not isinstance(value, dict):
        return value
    result = {}
    for key, item in value.items():
        target = LEGACY_KEYS.get(key, key)
        item = normalise(item)
        if target in result and result[target] != item:
            raise ValueError(f'Conflicting manufacturing revision metadata: {target}')
        result[target] = item
    return result


def loads(data, **kwargs):
    return normalise(_json.loads(data, **kwargs))


def load(stream, **kwargs):
    return loads(stream.read(), **kwargs)


def dumps(value, **kwargs):
    return _json.dumps(value, **kwargs)


def dump(value, stream, **kwargs):
    return _json.dump(value, stream, **kwargs)


JSONDecodeError = _json.JSONDecodeError
