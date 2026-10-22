import unittest
import checks
from sample import SAMPLE

class CheckTests(unittest.TestCase):
    def signal(self, result, sid):
        return next(s for s in result['signals'] if s['id'] == sid)

    def test_quotes_are_exact_substrings(self):
        for text in (SAMPLE['first'], SAMPLE['retry'], 'Um, we, like, shipped it. It was 40% faster, you know? I tested it.'):
            for s in checks.check_answer(text)['signals']:
                for q in s['quotes']:
                    self.assertIn(q, text)

    def test_sample_first_take_flags_ownership(self):
        result = checks.check_answer(SAMPLE['first'])
        self.assertEqual(result['priority']['id'], 'ownership')
        self.assertEqual(self.signal(result, 'ownership')['status'], 'missing')
        self.assertIn('made it better', self.signal(result, 'vague')['quotes'])
        self.assertEqual(self.signal(result, 'fillers')['count'], 2)

    def test_sample_retry_moves_toward_suggestions(self):
        result = checks.compare_answers(SAMPLE['first'], SAMPLE['retry'])
        directions = {c['id']: c['direction'] for c in result['changes']}
        self.assertEqual(directions['ownership'], 'toward')
        self.assertEqual(directions['vague'], 'toward')
        self.assertTrue(result['summary'].startswith('Moved in the suggested direction'))

    def test_no_verification_is_reported_missing_without_quotes(self):
        result = checks.check_answer('I built a scheduling page for our club and I designed the layout with my friend.')
        verification = self.signal(result, 'verification')
        self.assertEqual(verification['status'], 'missing')
        self.assertEqual(verification['quotes'], [])

    def test_numbers_prompt_support_not_judgment(self):
        result = checks.check_answer('I cached the results and latency dropped 40% in our load test.')
        claims = self.signal(result, 'claims')
        self.assertEqual(claims['status'], 'watch')
        self.assertIn('40%', claims['quotes'][0])

    def test_no_scores_in_output(self):
        result = checks.check_answer(SAMPLE['first'])
        keys = set(result) | {k for s in result['signals'] for k in s}
        self.assertFalse([k for k in keys if 'score' in k or 'grade' in k or 'rating' in k])

    def test_empty_and_identical_inputs_rejected(self):
        with self.assertRaises(ValueError):
            checks.check_answer('   ')
        with self.assertRaises(ValueError):
            checks.compare_answers(SAMPLE['first'], SAMPLE['first'])

    def test_unchanged_retry_is_honest(self):
        result = checks.compare_answers('We made it better.', 'We made it much better.')
        self.assertFalse(result['summary'].startswith('Moved'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
