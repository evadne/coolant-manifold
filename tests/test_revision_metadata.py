"""Exercise migration of immutable metadata and rejection of conflicting data."""
from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import revision_json
from source_integrity import source_matches


class RevisionMetadataTest(unittest.TestCase):
    def test_legacy_keys_normalise_without_rewriting_evidence(self):
        original = '{"issue":"Q-M04","nested":[{"body_issue":"Q-M04"}],"source_sha256":{"scripts/prepare_Q_body_issue.py":"hash"},"note":"original issue wording"}'
        value = revision_json.loads(original)
        self.assertEqual(value['manufacturing_revision'], 'Q-M04')
        self.assertEqual(value['nested'][0]['body_manufacturing_revision'], 'Q-M04')
        self.assertEqual(value['source_sha256'], {'scripts/prepare_Q_body_issue.py':'hash'})
        self.assertEqual(value['note'], 'original issue wording')
        self.assertEqual(revision_json.loads(revision_json.dumps(value)), value)
        self.assertIn('issue', json.loads(original))

    def test_conflicting_old_and_new_revision_rejected(self):
        for fields in ('"issue":"Q-M01","manufacturing_revision":"Q-M04"',
                       '"manufacturing_revision":"Q-M04","issue":"Q-M01"'):
            with self.assertRaisesRegex(ValueError, 'Conflicting'):
                revision_json.loads('{'+fields+'}')
        self.assertEqual(revision_json.loads('{"issue":"Q-M04","manufacturing_revision":"Q-M04"}'),
                         {'manufacturing_revision':'Q-M04'})

    def test_renamed_source_checks_all_retained_stages_and_rejects_tampering(self):
        digest=lambda s:hashlib.sha256(s.encode()).hexdigest()
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'cad').mkdir();(root/'scripts').mkdir()
            target=root/'scripts/new.py';target.write_text('third\n')
            record={'files':{'scripts/old.py':dict(current_path='scripts/new.py',
                before_sha256=digest('first\n'),after_sha256=digest('third\n'),
                replacements=[dict(before='first\n',after='second\n'),dict(before='second\n',after='third\n')])}}
            (root/'cad/source-maintenance.json').write_text(json.dumps(record))
            for path in ('scripts/old.py','scripts/new.py'):
                for text in ('first\n','second\n','third\n'):
                    self.assertTrue(source_matches(root,path,digest(text)))
                self.assertFalse(source_matches(root,path,'0'*64))
            target.write_text('unreviewed\n')
            self.assertFalse(source_matches(root,'scripts/old.py',digest('first\n')))
