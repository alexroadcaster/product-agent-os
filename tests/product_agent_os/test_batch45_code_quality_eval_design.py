import copy
import hashlib
import json
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'plugins/product-agent-os/scripts'))
from codex_runtime_runner.promotion_contract import parse_primary_result, ValidatedPrimaryResult, QuarantinedPrimaryResult
from codex_runtime_runner.eval_design import render_eval_prompt, EvalDesignError


class FrozenEvalDesignTest(unittest.TestCase):
    def test_compiler_emits_only_frozen_generation_context_and_rejects_drift(self):
        corpus = json.loads((ROOT/'docs/superpowers/specs/batch45-code-quality-heldout-corpus.json').read_text())
        for task in corpus['tasks']:
            for arm in ('baseline', 'treatment'):
                result = render_eval_prompt(ROOT, arm, task['task_id'])
                self.assertFalse(result['provider_call_performed'])
                self.assertTrue(result['approval_required'])
                self.assertIn(task['intent'], result['prompt'])
                self.assertNotIn('reference_file', result['prompt'])
                self.assertNotIn('seeded_file', result['prompt'])
        with self.assertRaises(EvalDesignError):
            render_eval_prompt(ROOT, 'other', 'CQ01')
        with self.assertRaises(EvalDesignError):
            render_eval_prompt(ROOT, 'baseline', 'CQ99')
        original = Path.read_bytes
        def corrupted(path):
            content = original(path)
            return content + b'drift' if path.name == 'input.py' else content
        with patch.object(Path, 'read_bytes', corrupted):
            with self.assertRaisesRegex(EvalDesignError, 'fixture_drift'):
                render_eval_prompt(ROOT, 'baseline', 'CQ01')

    def test_versioned_corpus_and_explicit_no_change_result(self):
        payload = json.loads((ROOT/'tests/fixtures/product_agent_os/batch45/promotion-contract/valid-primary-result.json').read_text())
        payload.update(schema_version='batch45_cqrr_primary_result_v1', corpus_id='B45-CQRR-HELDOUT-V1', task_id='CQ03')
        payload['result_class'] = 'no_op'
        payload['changed_files'] = []
        self.assertIsInstance(parse_primary_result(payload, material_change_required=False), ValidatedPrimaryResult)
        self.assertIsInstance(parse_primary_result(payload), QuarantinedPrimaryResult)
        for bad in ('CQ13', 'UNKNOWN'):
            payload['task_id'] = bad
            self.assertIsInstance(parse_primary_result(payload, False), QuarantinedPrimaryResult)

    def test_single_intervention_and_hashes_are_frozen(self):
        design = json.loads((ROOT/'docs/superpowers/specs/batch45-code-quality-eval-design.json').read_text())
        baseline, treatment = design['arms']['baseline'], design['arms']['treatment']
        for key in ('model', 'reasoning_effort', 'runner', 'timeout_seconds', 'tools', 'corpus_sha256', 'context_policy'):
            self.assertEqual(baseline[key], treatment[key], key)
        prompts = {arm: (ROOT/row['prompt_path']).read_text(encoding='utf-8') for arm, row in design['arms'].items()}
        self.assertEqual(prompts['treatment'], prompts['baseline'].replace('<!-- intervention -->', design['intervention']))
        self.assertLess(len(design['intervention'].split()), 100)
        for arm, row in design['arms'].items():
            self.assertEqual(hashlib.sha256((ROOT/row['prompt_path']).read_bytes()).hexdigest(), row['prompt_sha256'])
        for name, digest in design['context_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), digest)
        corpus = json.loads((ROOT/design['corpus_path']).read_text())
        self.assertEqual(corpus['content_sha256'], baseline['corpus_sha256'])
        self.assertEqual(design['generation_context_keys'], ['intent', 'acceptance', 'input_source'])
        self.assertFalse(design['reviewer_assistance'])
        self.assertFalse(design['comment_advisory'])
