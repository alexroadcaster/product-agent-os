"""Synthetic acceptance flows through public render/merge and compaction boundaries."""
import hashlib
import json
import sys
import tempfile
import unittest
import platform
import time
import io
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'plugins/product-agent-os/scripts'))
from product_agent_os.infrastructure import render_infrastructure_plan, stage_infrastructure
from product_agent_os.merge_infrastructure import build_merge_plan, apply_merge_plan
from product_agent_os.control_plane_documents import document_readiness
from product_agent_os import control_plane_compaction as compaction
from product_agent_os.document_navigation import documentation_inventory, check_reference, check_local_links

CASES = ROOT / 'tests/fixtures/product_agent_os/g8-control-plane/cases.json'


def run_pilot(profile, baseline_scripts=None):
    """Raise on any lost invariant; return metadata only, never recovery bodies."""
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='g8-pilot-') as tmp:
        root, stage = Path(tmp) / profile['id'], Path(tmp) / 'stage'
        root.mkdir()
        (root / 'TEST.md').write_bytes(b'# Verification\n`python check_docs.py`\n')
        task = {'schema_version': 1, 'task_id': 'SYN-01', 'intent': 'Update documentation',
                'changed_paths': ['README.md'], 'change_mode': 'docs_only', 'risk_level': 'low',
                'acceptance': ['R-01 preserve decisions'], 'risks': [], 'explicit_full_packet': True,
                'evals_required': profile['evals_required'], 'documents': {
                    'REQUIREMENTS.md': {'source': 'task:SYN-01', 'goal': 'R-01 preserve decisions',
                                        'scope': ['README.md'], 'acceptance': ['R-01 checked'],
                                        'constraints': ['Never remove open owner gate']}}}
        baseline = render_infrastructure_plan(root, legacy_catalog=True)
        controlled_comparison = None
        if baseline_scripts:
            common = {key: value for key, value in task.items() if key not in {'documents', 'evals_required'}}
            before = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            packet_path = Path(tmp) / 'common-task.json'
            packet_path.write_text(json.dumps(common), encoding='utf-8')
            code = ("import json,sys; from pathlib import Path; sys.path.insert(0,sys.argv[1]); "
                    "from product_agent_os.infrastructure import stage_infrastructure; "
                    "r=stage_infrastructure(sys.argv[2],sys.argv[3],task_context=json.loads(Path(sys.argv[4]).read_text())); "
                    "files=r['rendered_artifacts']['files']; "
                    "print(json.dumps({'count':len(files),'bytes':sum(Path(f['staged_path']).stat().st_size for f in files),"
                    "'validation_ok':r['rendered_artifacts']['validation']['ok']}))")
            old = subprocess.run([sys.executable, '-B', '-c', code, str(baseline_scripts), str(root),
                                  str(Path(tmp) / 'baseline-stage'), str(packet_path)], capture_output=True, text=True, timeout=60)
            assert old.returncode == 0, old.stderr
            old_metrics = json.loads(old.stdout)
            new = stage_infrastructure(root, Path(tmp) / 'controlled-treatment-stage', task_context=common)
            assert old_metrics['validation_ok'] and new['rendered_artifacts']['validation']['ok']
            assert before == {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            controlled_comparison = {'input_sha256': hashlib.sha256(json.dumps(common, sort_keys=True).encode()).hexdigest(),
                'baseline': old_metrics, 'treatment': {'count': len(new['rendered_artifacts']['files']),
                'bytes': sum(f['bytes'] or 0 for f in new['rendered_artifacts']['files']), 'validation_ok': True},
                'scope': 'identical common task packet; supplied document facts and AI applicability tested separately'}
        initial = stage_infrastructure(root, stage, task_context=task)
        if not initial['rendered_artifacts']['validation']['ok']:
            raise AssertionError('staging validation failed')
        merge = build_merge_plan(root, stage)
        decisions = [d for d in merge['decisions'] if d['approval_required']]
        approval = stage / 'synthetic-approval.json'
        approval.write_text(json.dumps({'approval': {
            'schema_version': 1, 'merge_plan_id': merge['id'], 'approved_by': 'synthetic-fixture-owner',
            'approved_at': datetime.now(timezone.utc).isoformat(),
            'approved_targets': [d['target_path'] for d in decisions],
            'approved_actions': sorted({d['action'] for d in decisions}),
            'accepted_risks': ['synthetic local fixture only'], 'denied_targets': [],
            'notes': 'Not a real project approval', 'enable_hooks': False,
            'approved_hook_events': [], 'blocking_hooks': [], 'hook_rollback': ''}}), encoding='utf-8')
        apply_merge_plan(root, stage, approval)
        requirements = root / 'REQUIREMENTS.md'
        populated = requirements.read_bytes()
        assert document_readiness('REQUIREMENTS.md', populated.decode())['state'] == 'draft'
        requirements.write_bytes(populated + b'\nR-02: New user requirement; owner gate remains open.\n')
        before_regeneration = requirements.read_bytes()
        stage_infrastructure(root, Path(tmp) / 'second-stage', task_context=task)
        second_merge = build_merge_plan(root, Path(tmp) / 'second-stage')
        assert next(d for d in second_merge['decisions'] if d['target_path'] == 'REQUIREMENTS.md')['action'] == 'companion_only'
        assert requirements.read_bytes() == before_regeneration
        current = b'# Current\nR-01/R-02; owner acceptance PENDING; failure receipt retained.\n'
        history = ('## Closed receipt\nSynthetic failed attempt; exit 1; Я🙂\n' * profile['history_rows']).encode()
        original = current + history
        (root / 'RUNLOG.md').write_bytes(original)
        moves = [{'source': 'RUNLOG.md', 'start': len(current), 'end': len(original),
                  'destination': 'docs/history/runlog-cycle.md', 'classification': 'history',
                  'owner': 'synthetic-project', 'reason': 'closed receipts; active gate retained'}]
        plan = compaction.propose(root, moves, hard_limit=profile['budget'])
        assert (root / 'RUNLOG.md').read_bytes() == original
        (root / 'RUNLOG.md').write_bytes(original + b'concurrent edit')
        try:
            compaction.apply(root, plan, approved_digest=plan['digest'])
        except ValueError:
            pass
        else:
            raise AssertionError('stale plan accepted')
        assert (root / 'RUNLOG.md').read_bytes().endswith(b'concurrent edit')
        (root / 'RUNLOG.md').write_bytes(original)  # Reset only this synthetic case's input.
        receipt = compaction.apply(root, plan, approved_digest=plan['digest'])
        after = (root / 'RUNLOG.md').read_bytes()
        assert current in after and len(after) <= profile['budget']
        assert (root / 'docs/history/runlog-cycle.md').read_bytes() == history
        assert check_local_links(root, ['RUNLOG.md']) == []
        compaction.rollback(root, receipt['journal'])
        assert (root / 'RUNLOG.md').read_bytes() == original
        compaction.apply(root, plan, approved_digest=plan['digest'])
        (root / 'RUNLOG.md').write_bytes(after + b'\nNext task SYN-02: continue with R-02.\n')
        assert b'R-02' in requirements.read_bytes()
        navigation = documentation_inventory(root, signals={'history': True, 'operations': profile['id'] == 'trade-like'})
        assert 'history' in navigation['needed_domains']
        if profile['id'] == 'mypartners-like':
            mirror = root / 'docs/requirements-mirror.md'
            mirror.write_bytes(requirements.read_bytes())
            assert check_reference(root, {'kind': 'mirror', 'path': 'docs/requirements-mirror.md',
                                         'source': 'REQUIREMENTS.md',
                                         'source_digest': hashlib.sha256(requirements.read_bytes()).hexdigest()})['status'] == 'verified'
        if profile['id'] == 'site-like':
            from product_agent_os.document_navigation import duplicate_blocks
            (root / 'README.md').write_text('Repeated correction block for current project.\n\nRepeated correction block for current project.\n', encoding='utf-8')
            assert len(duplicate_blocks(root, ['README.md'])) == 1
            assert check_reference(root, {'kind': 'cross_repository', 'repository': 'missing',
                                          'path': 'README.md'})['status'] == 'unknown'
        return {'profile': profile['id'], 'status': 'passed', 'budget': profile['budget'],
                'before_bytes': len(original), 'after_bytes': len(after), 'recovery_exact': True,
                'current_gate_preserved': True, 'regeneration_preserved': True,
                'original_sha256': hashlib.sha256(original).hexdigest(),
                'history_sha256': hashlib.sha256(history).hexdigest(),
                'next_change': {'files_changed': 1, 'added_bytes': len(b'\nNext task SYN-02: continue with R-02.\n'),
                                'history_rewrite_required': False},
                'elapsed_seconds': round(time.monotonic() - started, 3),
                'controlled_comparison': controlled_comparison,
                'legacy_template_count': len(baseline['rendered_artifacts']['files']),
                'scoped_template_count': len(initial['rendered_artifacts']['files']),
                'legacy_template_bytes': sum(f['bytes'] or 0 for f in baseline['rendered_artifacts']['files']),
                'scoped_template_bytes': sum(f['bytes'] or 0 for f in initial['rendered_artifacts']['files']),
                'scenarios': json.loads(CASES.read_text())['required_scenarios']}


class G8ControlPlaneTest(unittest.TestCase):
    def test_three_frozen_synthetic_profiles(self):
        for profile in json.loads(CASES.read_text())['profiles']:
            with self.subTest(profile=profile['id']):
                self.assertEqual(run_pilot(profile)['status'], 'passed')


def write_report(path, baseline_root):
    """Reproducible local pilot runner; retain outcomes without source-private bodies."""
    from tests.product_agent_os.test_control_plane_compaction import CompactionTest
    from tests.product_agent_os.test_control_plane_documents import ControlPlaneDocumentsTest
    from tests.product_agent_os.test_document_navigation import DocumentNavigationTest
    profiles = []
    for profile in json.loads(CASES.read_text())['profiles']:
        try:
            profiles.append(run_pilot(profile, baseline_root / 'plugins/product-agent-os/scripts'))
        except Exception as exc:
            profiles.append({'profile': profile['id'], 'status': 'failed', 'error_type': type(exc).__name__})
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(cls)
                               for cls in (CompactionTest, ControlPlaneDocumentsTest, DocumentNavigationTest))
    checks = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
    sources = [*sorted((ROOT / 'plugins/product-agent-os/scripts/product_agent_os').glob('*.py')),
               ROOT / 'plugins/product-agent-os/scripts/codex_runtime_runner/state.py',
               ROOT / 'plugins/product-agent-os/scripts/codex_runtime_runner/cli.py',
               *sorted((ROOT / 'tests/product_agent_os').glob('test_*plane*.py')),
               ROOT / 'tests/product_agent_os/test_document_navigation.py', CASES]
    sources.append(ROOT / 'tests/product_agent_os/test_status_snapshot.py')
    sources.append(ROOT / 'tests/product_agent_os/test_system_file_hygiene.py')
    result = {'schema_version': 1, 'group': 'PAOS-AUD-G8',
              'generated_at': datetime.now(timezone.utc).isoformat(),
              'environment': {'python': platform.python_version(), 'system': platform.system(), 'providers': False},
              'baseline_revision': (baseline_root / 'BASELINE_REVISION.txt').read_text().strip(),
              'comparison': 'checked-in pre-G8 versus G8 on identical task packet/workspace; additional legacy-route inventory and exact-byte compaction metrics',
              'profiles': profiles, 'profile_denominator': len(profiles),
              'supporting_suite': {'run': checks.testsRun, 'failures': len(checks.failures), 'errors': len(checks.errors),
                                   'skipped': len(checks.skipped), 'passed': checks.wasSuccessful(),
                                   'failed_cases': [str(case) for case, _ in checks.failures + checks.errors]},
              'source_sha256': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
              'owner_acceptance': 'pending', 'fresh_session_activation': 'not_run_separate',
              'scope_decisions': {'docs_planning_detailed_matrices': 'default_size_exception_preserve_intact',
                                  'research_audit_matrix': 'retain_unsplit_owner_directed; preview_not_authorized'},
              'limits': ['synthetic local only', 'no model superiority, token or monetary saving claim',
                         'junction/hardlink guards simulated; real symlink refusal checked separately in execution report',
                         'M1 SQL adapter tested as declared file-authority boundary only'],
              'earlier_failed_attempts': 'research/product-agent-os-g8-execution-report.md'}
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    return checks.wasSuccessful() and all(item['status'] == 'passed' for item in profiles)


if __name__ == '__main__':
    if len(sys.argv) == 5 and sys.argv[1] == '--report' and sys.argv[3] == '--baseline':
        raise SystemExit(0 if write_report(Path(sys.argv[2]), Path(sys.argv[4])) else 1)
    unittest.main()
