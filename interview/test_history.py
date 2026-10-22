import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import history
from sample import SAMPLE

class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.patch = patch.object(history, 'PATH', Path(self.dir.name) / 'data' / 'history.json')
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.dir.cleanup()

    def test_empty_progress(self):
        result = history.progress()
        self.assertEqual(result['sessions'], 0)
        self.assertIsNone(result['suggested_focus'])

    def test_record_stores_signals_not_text(self):
        saved = history.record(SAMPLE['question'], SAMPLE['first'], SAMPLE['retry'])
        self.assertEqual(saved['total_sessions'], 1)
        raw = history.PATH.read_text(encoding='utf-8')
        for phrase in ('We worked on the database', 'I inspected the database queries', 'made it better'):
            self.assertNotIn(phrase, raw)
        entry = json.loads(raw)[0]
        self.assertEqual(entry['first']['priority'], 'ownership')
        self.assertIn('ownership', entry['retry']['moved_toward'])

    def test_progress_suggests_recurring_priority(self):
        history.record(SAMPLE['question'], SAMPLE['first'])
        history.record(SAMPLE['question'], 'We made it better and it worked well.')
        history.record(SAMPLE['question'], SAMPLE['retry'])
        result = history.progress()
        self.assertEqual(result['sessions'], 3)
        self.assertEqual(result['suggested_focus']['id'], 'ownership')
        self.assertEqual(result['recurring_priorities'][0]['times_priority'], 2)
        self.assertEqual(len(result['recent']), 3)

    def test_identical_retry_rejected_without_saving(self):
        with self.assertRaises(ValueError):
            history.record(SAMPLE['question'], SAMPLE['first'], SAMPLE['first'])
        self.assertFalse(history.PATH.exists())

    def test_clear(self):
        history.record(SAMPLE['question'], SAMPLE['first'])
        self.assertTrue(history.clear()['cleared'])
        self.assertEqual(history.progress()['sessions'], 0)
        self.assertFalse(history.clear()['cleared'])

    def test_corrupt_file_is_treated_as_empty(self):
        history.PATH.parent.mkdir(parents=True)
        history.PATH.write_text('not json', encoding='utf-8')
        self.assertEqual(history.progress()['sessions'], 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
