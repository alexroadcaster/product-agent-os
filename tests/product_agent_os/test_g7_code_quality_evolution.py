"""Independent expected outcomes for G7's offline evidence contracts."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'plugins/product-agent-os/scripts'))


class G7EvolutionTest(unittest.TestCase):
    def test_pressure_oracle_and_structural_advice_controls(self):
        import importlib.util
        import hashlib
        import json
        folder = ROOT / 'tests/fixtures/product_agent_os/g7-pressure'
        manifest = json.loads((folder / 'manifest.json').read_text())
        def load(name):
            path = folder / (name + '.py')
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), manifest['exact_files'][path.name])
            spec = importlib.util.spec_from_file_location('g7_pressure_' + name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        oracle = load('oracle')
        for name in ('justified', 'overbuilt'):
            candidate = load(name)
            self.assertEqual(oracle.check(candidate), [])
            self.assertEqual(oracle.check_batch(candidate), [])
        import types
        unsafe = types.SimpleNamespace(apply=lambda state, request, amount, notify: state.update(balance=70))
        self.assertIn('callback_must_observe_uncommitted_state', oracle.check(unsafe))
        self.assertEqual([case['id'] for case in manifest['cases']], ['deadline', 'sunk_cost', 'incorrect_review'])

    def test_incomplete_or_malformed_codex_stream_cannot_pass(self):
        from run_g7_codex_pilot import collect_events
        self.assertTrue(collect_events('{"type":"item.completed","item":{"type":"agent_message","text":"source"}}')['tool_activity'])
        self.assertTrue(collect_events('not json\n{"type":"turn.completed","usage":{}}')['tool_activity'])

    def test_known_cli_config_warning_is_not_a_tool_call_but_unknown_error_blocks(self):
        import json
        from run_g7_codex_pilot import collect_events
        warning = {'type':'item.completed','item':{'type':'error','message':'Codex is ignoring 6 unrecognized configuration settings. Check for typos or deprecated settings.'}}
        ending = '\n' + json.dumps({'type':'turn.completed','usage':{'input_tokens':1,'output_tokens':1}})
        self.assertFalse(collect_events(json.dumps(warning)+ending)['tool_activity'])
        warning['item']['message'] = 'Unclassified runtime failure'
        self.assertTrue(collect_events(json.dumps(warning))['tool_activity'])

    def test_codex_tool_start_without_completion_is_ineligible(self):
        import json
        from run_g7_codex_pilot import collect_events
        output = '\n'.join(json.dumps(event) for event in [
            {'type':'item.started', 'item':{'type':'command_execution'}},
            {'type':'item.completed', 'item':{'type':'agent_message','text':'def f(): pass'}},
        ])
        self.assertTrue(collect_events(output)['tool_activity'])

    def test_fixture_drift_and_traversal_are_rejected(self):
        import hashlib
        import tempfile
        from codex_runtime_runner.g7_quality_eval import verify_fixture_files
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            (folder / 'oracle.py').write_bytes(b'original')
            manifest = {'exact_fixture_files': {'oracle.py': hashlib.sha256(b'original').hexdigest()}}
            verify_fixture_files(folder, manifest)
            (folder / 'oracle.py').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'fixture drift'):
                verify_fixture_files(folder, manifest)
            with self.assertRaisesRegex(ValueError, 'invalid fixture path'):
                verify_fixture_files(folder, {'exact_fixture_files': {'../oracle.py': 'a' * 64}})

    def test_generation_projection_excludes_oracle_and_binds_prior_candidate(self):
        from codex_runtime_runner.g7_quality_eval import render_generation_context
        packet = render_generation_context(ROOT, 'baseline', 'state-boundary', 0)
        self.assertNotIn('oracle', packet['context_keys'])
        self.assertNotIn('100,30,id1', packet['prompt'])
        self.assertFalse(packet['provider_call_performed'])
        with self.assertRaises(ValueError):
            render_generation_context(ROOT, 'baseline', 'state-boundary', 1)
        second = render_generation_context(ROOT, 'treatment', 'state-boundary', 1, 'synthetic previous candidate')
        self.assertIn('synthetic previous candidate', second['prompt'])
        self.assertNotEqual(packet['previous_candidate_digest'], second['previous_candidate_digest'])

    def test_executable_reference_oracle_rejects_stub_and_unsafe_controls(self):
        import importlib.util
        folder = ROOT / 'tests/fixtures/product_agent_os/g7-code-quality-evolution'
        def load(name):
            spec = importlib.util.spec_from_file_location('g7_' + name, folder / (name + '.py'))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        oracle = load('oracle')
        self.assertEqual(oracle.check(load('reference')), [])
        self.assertIn('complete', oracle.check(load('stub')))
        self.assertIn('rollback', oracle.check(load('unsafe')))
        self.assertIn('idempotent', oracle.check(load('unsafe')))

    def test_unknown_and_structural_checks_never_become_executable_pass(self):
        from codex_runtime_runner.g7_quality_eval import summarize_outcomes
        rows = [dict(case_id=str(i), status=s) for i, s in enumerate(
            ['passed', 'failed', 'skipped', 'unknown', 'structural_only', 'timeout', 'setup_error'])]
        result = summarize_outcomes(rows, expected_cases=[str(i) for i in range(8)])
        self.assertEqual(result['counts']['passed'], 1)
        self.assertEqual(result['counts']['missing'], 1)
        self.assertEqual(result['executable_pass_rate'], 0.5)
        self.assertFalse(result['complete'])
        self.assertEqual(result['eligible'], 8)

    def test_missing_duplicate_and_extra_cases_cannot_hide_failures(self):
        from codex_runtime_runner.g7_quality_eval import summarize_outcomes
        self.assertIsNone(summarize_outcomes([], ['a'])['executable_pass_rate'])
        for rows in ([{'case_id': 'a', 'status': 'passed'}] * 2,
                     [{'case_id': 'unexpected', 'status': 'passed'}]):
            with self.assertRaises(ValueError):
                summarize_outcomes(rows, ['a'])

    def test_review_requires_revision_and_scenario_not_low_self_score(self):
        from codex_runtime_runner.g7_quality_eval import review_findings
        revision = 'a' * 64
        finding = dict(id='f', revision=revision, source='src/ledger.py:8',
                       scenario='Second identical request', consequence='Charged twice',
                       action='Check idempotency before charging', confidence='high',
                       kind='correctness', disposition='confirmed', evidence='case-idempotent')
        self.assertEqual(review_findings([], revision)['verdict'], 'approve')
        self.assertEqual(review_findings([finding], revision)['verdict'], 'changes_requested')
        preference = dict(finding, kind='preference')
        self.assertEqual(review_findings([preference], revision)['verdict'], 'approve')
        stale = dict(finding, revision='b' * 64)
        self.assertEqual(review_findings([stale], revision)['verdict'], 'blocked')
        unsupported = dict(finding, evidence='')
        self.assertEqual(review_findings([unsupported], revision)['verdict'], 'blocked')
        deferred = dict(finding, disposition='deferred', owner='maintainer', revisit_trigger='new caller')
        self.assertEqual(review_findings([deferred], revision)['verdict'], 'blocked')
        with self.assertRaises(ValueError):
            review_findings([dict(finding, disposition='deferred')], revision)

    def test_evidence_fingerprint_changes_with_environment_and_keeps_input_immutable(self):
        from codex_runtime_runner.g7_quality_eval import evidence_fingerprint
        context = {'source': 'a', 'config': 'b', 'tool': '1', 'environment': 'local'}
        original = copy.deepcopy(context)
        self.assertNotEqual(evidence_fingerprint(context), evidence_fingerprint(dict(context, tool='2')))
        self.assertEqual(context, original)


if __name__ == '__main__':
    unittest.main()
