import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'plugins/product-agent-os/scripts'))
from codex_runtime_runner import reviewer_contract as reviewer


def pair_inputs():
    primary = json.loads((ROOT / 'tests/fixtures/product_agent_os/batch45/promotion-contract/valid-primary-result.json').read_text())
    other = copy.deepcopy(primary)
    primary['arm'], other['arm'] = 'baseline', 'treatment'
    patches = {'baseline': '--- a/main.py\n+++ b/main.py\n@@ -1 +1 @@\n-old\n+new\n',
               'treatment': '--- a/main.py\n+++ b/main.py\n@@ -1 +1 @@\n-old\n+better\n'}
    evidence = {arm: {'task_id': primary['task_id'], 'patch_sha256': reviewer.digest(patch),
                     'acceptance': 'passed', 'regression': 'passed', 'seeded_faults': 'passed',
                     'dependency': 'passed'} for arm, patch in patches.items()}
    return primary, other, patches, evidence


class BlindedReviewerTest(unittest.TestCase):
    def test_rubric_matches_executable_dimensions_and_threshold(self):
        rubric = json.loads((ROOT/'plugins/product-agent-os/assets/templates/evals/code-quality-reviewer-rubric.json').read_text())
        self.assertEqual(tuple(rubric['dimensions']), reviewer.DIMENSIONS)
        self.assertEqual(rubric['minimum_each_dimension'], 6)

    def test_blinded_packet_omits_primary_metadata_and_randomizes_ids(self):
        a, b, patches, evidence = pair_inputs()
        packet, mapping = reviewer.prepare_review(a, b, patches=patches, evidence=evidence)
        serialized = json.dumps(packet)
        for forbidden in ('baseline', 'treatment', 'behavior_score', 'dimension_scores', 'model_id'):
            self.assertNotIn(forbidden, serialized)
        self.assertEqual(set(mapping.values()), {'baseline', 'treatment'})
        self.assertEqual(set(mapping), {c['candidate_id'] for c in packet['candidates']})
        packet2, _ = reviewer.prepare_review(a, b, patches=patches, evidence=evidence)
        self.assertNotEqual(packet['review_id'], packet2['review_id'])

    def test_invalid_or_stale_pair_blocks_before_reviewer(self):
        for kind in ('schema', 'mismatch', 'failed', 'missing', 'stale', 'label_leak'):
            with self.subTest(kind=kind):
                a, b, patches, evidence = pair_inputs()
                if kind == 'schema': b['behavior_score'] = 'perfect'
                if kind == 'mismatch': b['model_id'] = 'different-model'
                if kind == 'failed': evidence['treatment']['regression'] = 'failed'
                if kind == 'missing': del evidence['baseline']['seeded_faults']
                if kind == 'stale': patches['treatment'] += '+extra\n'
                if kind == 'label_leak': patches['baseline'] += '+ baseline treatment\n'
                with self.assertRaises(reviewer.ReviewerContractError):
                    reviewer.prepare_review(a, b, patches=patches, evidence=evidence)

    def test_critical_findings_override_perfect_scores_and_bind_receipt(self):
        a, b, patches, evidence = pair_inputs()
        packet, _ = reviewer.prepare_review(a, b, patches=patches, evidence=evidence)
        verdict = {'review_id': packet['review_id'], 'packet_sha256': reviewer.packet_digest(packet),
                   'candidates': [{'candidate_id': item['candidate_id'],
                                   'scores': {k: 10 for k in reviewer.DIMENSIONS}, 'findings': []}
                                  for item in packet['candidates']]}
        self.assertEqual(reviewer.validate_review(packet, verdict)['verdict'], 'approve')
        for category in ('correctness', 'security', 'data_loss', 'regression'):
            changed = copy.deepcopy(verdict)
            changed['candidates'][0]['findings'] = [{'severity': 'critical', 'category': category, 'evidence': 'synthetic counterexample'}]
            self.assertEqual(reviewer.validate_review(packet, changed)['verdict'], 'changes_requested')
        verdict['packet_sha256'] = '0' * 64
        with self.assertRaises(reviewer.ReviewerContractError):
            reviewer.validate_review(packet, verdict)

    def test_invalid_reviewer_scores_or_candidate_sets_fail_closed(self):
        a, b, patches, evidence = pair_inputs()
        packet, _ = reviewer.prepare_review(a, b, patches=patches, evidence=evidence)
        for candidates in ([], [packet['candidates'][0]]):
            with self.assertRaises(reviewer.ReviewerContractError):
                reviewer.validate_review(packet, {'review_id': packet['review_id'], 'packet_sha256': reviewer.packet_digest(packet), 'candidates': candidates})
        valid_rows = [{'candidate_id': c['candidate_id'], 'scores': {k: 10 for k in reviewer.DIMENSIONS}, 'findings': []} for c in packet['candidates']]
        for score in (True, -1, 11, float('nan'), '10'):
            rows = copy.deepcopy(valid_rows)
            rows[0]['scores']['correctness'] = score
            with self.subTest(score=score), self.assertRaises(reviewer.ReviewerContractError):
                reviewer.validate_review(packet, {'review_id': packet['review_id'], 'packet_sha256': reviewer.packet_digest(packet), 'candidates': rows})
        rows = copy.deepcopy(valid_rows)
        rows[0]['scores']['correctness'] = 5
        result = reviewer.validate_review(packet, {'review_id': packet['review_id'], 'packet_sha256': reviewer.packet_digest(packet), 'candidates': rows})
        self.assertEqual(result['verdict'], 'changes_requested')
