"""Formation contracts: selection, preservation and explicit authority."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
import subprocess
import hashlib
import platform
import re
from urllib.parse import unquote
from unittest.mock import patch
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / 'plugins/product-agent-os/scripts'
sys.path.insert(0, str(SCRIPTS))
from product_agent_os.infrastructure import render_infrastructure_plan
from product_agent_os.project_formation import form_project
from product_agent_os.merge_infrastructure import build_merge_plan, apply_merge_plan, rollback_merge
from product_agent_os.stage_manifest import build_approval_template
from product_agent_os.document_navigation import check_local_links


def request(domains=None):
    return {'schema_version': 1, 'task': {
        'schema_version': 1, 'task_id': 'FORM-01', 'intent': 'Establish project documentation',
        'change_mode': 'docs_only', 'changed_paths': ['README.md'], 'risk_level': 'low',
        'acceptance': ['R-01 preserve user decisions'], 'risks': [], 'explicit_full_packet': True,
        'evals_required': 'ai' in (domains or []),
        'documents': {'REQUIREMENTS.md': {'source': 'task:FORM-01', 'goal': 'R-01 preserve user decisions',
                       'scope': ['README.md'], 'acceptance': ['R-01 retained'], 'constraints': ['No activation']}}},
        'domains': domains or ['architecture', 'planning', 'evidence']}


def approve(root, stage):
    plan = build_merge_plan(root, stage)
    if plan['blocked']:
        raise AssertionError(plan['blocked'])
    payload = build_approval_template(plan)
    payload['approval'].update(approved_by='synthetic-owner', approved_at=datetime.now(timezone.utc).isoformat(),
                               accepted_risks=['synthetic workspace only'], notes='fixture approval only')
    path = stage / 'synthetic-approval.json'
    path.write_text(json.dumps(payload), encoding='utf-8')
    return path


def stage_request(root, stage, packet):
    preview = form_project(root, packet)
    return form_project(root, packet, stage=stage, approved_preview_digest=preview['formation']['digest'])


def run_pilot(case, baseline_scripts=None):
    """Exercise preview/stage/approved merge/regenerate/rollback on synthetic data."""
    with tempfile.TemporaryDirectory() as tmp:
        root, stage = Path(tmp) / 'project', Path(tmp) / 'stage'; root.mkdir()
        for name, text in case['files'].items():
            path = root / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(text.encode())
        packet = request(case['domains'])
        before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        baseline = None
        if baseline_scripts:
            packet_path = Path(tmp) / 'input.json'; packet_path.write_text(json.dumps(packet))
            code = ('import sys,json; from pathlib import Path; sys.path.insert(0,sys.argv[1]); '
                    'from product_agent_os.infrastructure import render_infrastructure_plan as render; '
                    'r=render(sys.argv[2],task_context=json.loads(Path(sys.argv[3]).read_text())["task"]); '
                    'legacy=render(sys.argv[2]); fs=r["rendered_artifacts"]["files"]; '
                    'print(json.dumps({"files":len(fs),"bytes":sum(f["bytes"] or 0 for f in fs),'
                    '"default_without_context_files":len(legacy["rendered_artifacts"]["files"]),'
                    '"project_docs":sum(f["target_path"].startswith("docs/") for f in fs),'
                    '"validation_ok":r["rendered_artifacts"]["validation"]["ok"],'
                    '"desired_domains_supported":False}))')
            proc = subprocess.run([sys.executable, '-B', '-c', code, str(baseline_scripts), str(root), str(packet_path)],
                                  capture_output=True, text=True, timeout=90)
            if proc.returncode: raise AssertionError(proc.stderr)
            baseline = json.loads(proc.stdout)
        preview = form_project(root, packet)
        assert preview['formation']['gaps'] == []
        staged = form_project(root, packet, stage=stage, approved_preview_digest=preview['formation']['digest'])
        assert before == {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        receipt = apply_merge_plan(root, stage, approve(root, stage))
        assert all((root / p).read_bytes() == raw for p, raw in before.items())
        index = staged['formation']['owners']['index']
        assert not check_local_links(root, [index])
        # Existing indexes remain untouched: validate their companion navigation
        # against the resulting workspace, not merely the old index's links.
        index_file = next(f for f in staged['rendered_artifacts']['files'] if f['target_path'] == index)
        proposal = Path(index_file['staged_path']).read_text(encoding='utf-8')
        links = re.findall(r'\]\(([^)]+)\)', proposal)
        assert links
        for link in links:
            destination = ((root / index).parent / unquote(link)).resolve()
            assert destination.is_relative_to(root.resolve()) and destination.is_file()
        after = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        again = stage_request(root, Path(tmp) / 'again', packet)
        assert not any(d['approval_required'] for d in build_merge_plan(root, Path(tmp) / 'again')['decisions'])
        assert after == {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        (root / 'RUNLOG.md').write_bytes((root / 'RUNLOG.md').read_bytes() + b'\nSYN-02 next change; pending acceptance.\n')
        followup = form_project(root, packet, previous=again)
        assert followup['formation']['changes']['source_changed']
        # Restore only this synthetic probe edit so rollback can validate its CAS.
        (root / 'RUNLOG.md').write_bytes(after[Path('RUNLOG.md')])
        rollback_merge(root, receipt['rollback_manifest'])
        assert before == {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        files = staged['rendered_artifacts']['files']
        return {'profile': case['id'], 'status': 'passed', 'baseline': baseline,
                'input_digest': hashlib.sha256(json.dumps(packet, sort_keys=True).encode()).hexdigest(),
                'template_revisions': staged['formation']['template_revisions'],
                'treatment': {'files': len(files), 'bytes': sum(f['bytes'] or 0 for f in files),
                              'project_docs': sum(f['target_path'].startswith('docs/') for f in files),
                              'formation_gaps': [], 'implementation_gaps': staged['formation']['implementation_gaps'],
                              'manual_updates': staged['formation']['manual_updates']},
                'preservation_exact': True, 'rollback_exact': True, 'navigation_valid': True,
                'proposed_navigation_valid': True,
                'repeat_no_writes': True, 'next_change_detected': True, 'activation': 'not_tested',
                'ceiling': 'synthetic local; existing index update remains companion proposal'}


class ProjectFormationTest(unittest.TestCase):
    def test_receipt_lock_retry_is_bounded_and_retains_last_journal(self):
        from product_agent_os.merge_infrastructure import _write_rollback_manifest, MergeInfrastructureError
        from product_agent_os.control_plane_compaction import _write
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / 'receipt.json'
            path.write_text('previous journal', encoding='utf-8')
            attempts = []
            def transient_lock(*args):
                attempts.append(True)
                if len(attempts) == 1:
                    raise PermissionError('transient lock')
                return _write(*args)
            with patch('product_agent_os.control_plane_compaction._write',
                       side_effect=transient_lock) as writer:
                _write_rollback_manifest(path, root, [])
                self.assertEqual(writer.call_count, 2)
            previous = path.read_bytes()
            self.assertEqual(json.loads(previous)['entries'], [])
            with patch('product_agent_os.control_plane_compaction._write',
                       side_effect=PermissionError('persistent denial')) as writer:
                with self.assertRaises(MergeInfrastructureError):
                    _write_rollback_manifest(path, root, [])
                self.assertEqual(writer.call_count, 3)
            self.assertEqual(path.read_bytes(), previous)

    def test_missing_context_never_selects_full_catalog(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = render_infrastructure_plan(tmp)
            self.assertEqual(result['rendered_artifacts']['files'], [])
            self.assertIn('formation_context_required', result['infrastructure_plan']['blocked'])

    def test_new_project_preview_is_deterministic_and_stage_requires_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'project'
            root.mkdir()
            first = form_project(root, request())
            self.assertEqual(first['formation']['gaps'], [])
            self.assertNotIn('EVALS.md', first['formation']['selected'])
            self.assertTrue(first['rendered_artifacts']['validation']['ok'], first['rendered_artifacts']['validation'])
            self.assertEqual(first['formation'], form_project(root, request())['formation'])
            self.assertEqual(list(root.iterdir()), [])
            with self.assertRaisesRegex(Exception, 'preview'):
                form_project(root, request(), stage=Path(tmp) / 'bad', approved_preview_digest='wrong')
            self.assertFalse((Path(tmp) / 'bad').exists())
            staged = form_project(root, request(), stage=Path(tmp) / 'stage',
                                  approved_preview_digest=first['formation']['digest'])
            self.assertTrue(staged['rendered_artifacts']['validation']['ok'])

    def test_existing_aliases_are_reused_and_all_bytes_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, stage = Path(tmp) / 'project', Path(tmp) / 'stage'
            (root / 'docs').mkdir(parents=True)
            (root / 'docs/architecture.md').write_bytes(b'# Custom architecture\nDecision R-01\n')
            (root / 'docs/index.md').write_bytes(b'# Existing index\n')
            (root / 'AGENTS.md').write_bytes(b'User rules\r\n')
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            result = stage_request(root, stage, request())
            self.assertEqual(result['formation']['owners']['architecture'], 'docs/architecture.md')
            self.assertEqual(result['formation']['owners']['index'], 'docs/index.md')
            approval = approve(root, stage)
            applied = apply_merge_plan(root, stage, approval)
            for path, raw in before.items(): self.assertEqual((root / path).read_bytes(), raw)
            self.assertFalse((root / 'docs/architecture/overview.md').exists())
            regenerated = stage_request(root, Path(tmp) / 'again', request())
            plan = build_merge_plan(root, Path(tmp) / 'again')
            self.assertFalse(any(d['approval_required'] for d in plan['decisions']))
            self.assertTrue(all(f['action'] == 'leave_unchanged' for f in regenerated['rendered_artifacts']['files']))
            rollback_merge(root, applied['rollback_manifest'])
            self.assertEqual(before, {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()})

    def test_new_project_merge_has_resolvable_navigation_and_ai_conditional(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, stage = Path(tmp) / 'project', Path(tmp) / 'stage'; root.mkdir()
            packet = request(['architecture', 'api', 'data', 'operations', 'decisions', 'archive', 'ai'])
            packet['document_facts'] = {'architecture': {'source': 'owner:FORM-01', 'sections': {'Boundary': 'R-01 single process'}}}
            result = stage_request(root, stage, packet)
            self.assertIn('EVALS.md', result['formation']['selected'])
            self.assertEqual(result['formation']['document_readiness']['docs/architecture/overview.md'], 'draft')
            apply_merge_plan(root, stage, approve(root, stage))
            self.assertEqual(check_local_links(root, ['docs/README.md']), [])
            self.assertIn('R-01', (root / 'REQUIREMENTS.md').read_text())

    def test_source_change_and_new_source_invalidate_stage_and_merge(self):
        for change in ('edit', 'new'):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                root, stage = Path(tmp) / 'project', Path(tmp) / 'stage'; root.mkdir()
                (root / 'README.md').write_text('before')
                preview = form_project(root, request())
                stage_request(root, stage, request())
                approval = approve(root, stage)
                (root / ('README.md' if change == 'edit' else 'ARCHITECTURE.md')).write_text('changed')
                with self.assertRaisesRegex(Exception, 'preview'):
                    form_project(root, request(), stage=Path(tmp) / 'stale', approved_preview_digest=preview['formation']['digest'])
                with self.assertRaisesRegex(Exception, 'blocked'):
                    apply_merge_plan(root, stage, approval)
                self.assertFalse((root / 'PLAN.md').exists())

    def test_frozen_and_sql_projection_authority_cannot_be_bypassed(self):
        for mode in ('frozen', 'sql'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                root, stage = Path(tmp) / 'project', Path(tmp) / 'stage'; root.mkdir()
                stage_request(root, stage, request()); approval = approve(root, stage)
                (root / '.codex').mkdir()
                (root / '.codex/config.toml').write_text('[product_agent_os.documents]\nauthority="'+mode+'"\ntask_projections=["PLAN.md"]\n')
                preview = form_project(root, request())
                self.assertIn('document authority forbids file mutation', preview['formation']['gaps'])
                with self.assertRaises(Exception): apply_merge_plan(root, stage, approval)
                self.assertFalse((root / 'PLAN.md').exists())

    def test_ambiguous_owners_require_explicit_resolution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / 'docs').mkdir()
            (root / 'ARCHITECTURE.md').write_text('first'); (root / 'docs/architecture.md').write_text('second')
            preview = form_project(root, request())
            self.assertTrue(any('ambiguous_owner' in x for x in preview['formation']['gaps']))
            packet = request(); packet['canonical_paths'] = {'architecture': 'ARCHITECTURE.md'}
            self.assertEqual(form_project(root, packet)['formation']['gaps'], [])

    def test_traversal_collisions_and_secret_input_fail_before_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            for invalid in ('../escape.md', '.codex/config.md', 'C:/outside.md', 'docs/../outside.md'):
                packet = request(); packet['canonical_paths'] = {'architecture': invalid}
                with self.subTest(path=invalid), self.assertRaises(ValueError): form_project(tmp, packet)
            packet = request(); packet['canonical_paths'] = {'architecture': 'docs/same.md', 'planning': 'docs/same.md'}
            self.assertTrue(form_project(tmp, packet)['formation']['gaps'])
            packet = request(); packet['task']['intent'] = 'api_key=' + 'X' * 25
            with self.assertRaisesRegex(ValueError, 'secret'): form_project(tmp, packet)

    def test_profile_change_is_review_only_and_history_is_retained(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, stage = Path(tmp) / 'project', Path(tmp) / 'stage'; root.mkdir()
            original = stage_request(root, stage, request(['architecture', 'api', 'ai']))
            apply_merge_plan(root, stage, approve(root, stage))
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            changed = form_project(root, request(['architecture']), previous=original)
            self.assertIn('docs/api/README.md', changed['formation']['changes']['review_only_removed'])
            self.assertEqual(before, {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()})
            self.assertEqual(changed['formation']['acceptance'], 'not_accepted')

    def test_interrupted_apply_has_recoverable_completed_entries(self):
        from product_agent_os import merge_infrastructure as merger
        with tempfile.TemporaryDirectory() as tmp:
            root, stage = Path(tmp) / 'project', Path(tmp) / 'stage'; root.mkdir()
            stage_request(root, stage, request()); approval = approve(root, stage)
            original = merger._apply_decision
            counter = []
            def interrupt(*args):
                if counter: raise OSError('synthetic interruption before next write')
                counter.append(1); return original(*args)
            with patch.object(merger, '_apply_decision', side_effect=interrupt):
                with self.assertRaises(OSError): apply_merge_plan(root, stage, approval)
            rollback_merge(root, stage / 'product-agent-os-rollback-manifest.json')
            self.assertFalse(any(p.is_file() for p in root.rglob('*')))

    def test_explicit_control_surfaces_are_proposals_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            packet = request(); packet['control_surfaces'] = ['hooks', 'config']
            result = form_project(tmp, packet)
            self.assertEqual(result['formation']['gaps'], [])
            self.assertTrue(result['rendered_artifacts']['validation']['ok'], result['rendered_artifacts']['validation'])
            self.assertIn('.codex/hooks.json', result['formation']['selected'])
            self.assertIn('.codex/agents/builder.toml', result['formation']['selected'])
            self.assertEqual(result['formation']['activation'], 'not_activated')
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_interruption_after_write_before_receipt_can_recover(self):
        from product_agent_os import merge_infrastructure as merger
        with tempfile.TemporaryDirectory() as tmp:
            root, stage = Path(tmp) / 'project', Path(tmp) / 'stage'; root.mkdir()
            stage_request(root, stage, request()); approval = approve(root, stage)
            original = merger._apply_decision
            def interrupt(*args):
                original(*args)
                raise OSError('synthetic interruption after write before receipt')
            with patch.object(merger, '_apply_decision', side_effect=interrupt):
                with self.assertRaises(OSError): apply_merge_plan(root, stage, approval)
            rollback_merge(root, stage / 'product-agent-os-rollback-manifest.json')
            self.assertFalse(any(p.is_file() for p in root.rglob('*')))

    def test_cli_preview_and_stage_use_the_same_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, stage = Path(tmp) / 'project', Path(tmp) / 'stage'; root.mkdir()
            context = Path(tmp) / 'request.json'; context.write_text(json.dumps(request()))
            command = [sys.executable, '-B', str(SCRIPTS / 'render_infrastructure.py'), str(root), '--formation-context', str(context)]
            preview = subprocess.run(command + ['--dry-run'], capture_output=True, text=True)
            self.assertEqual(preview.returncode, 0, preview.stderr)
            payload = json.loads(preview.stdout)
            self.assertEqual(payload['formation']['digest'], form_project(root, request())['formation']['digest'])
            staged = subprocess.run(command + ['--stage', str(stage), '--preview-digest', payload['formation']['digest']], capture_output=True, text=True)
            self.assertEqual(staged.returncode, 0, staged.stderr)
            self.assertTrue((stage / 'product-agent-os-stage-manifest.json').exists())

    def test_inferred_domains_have_source_reasons_and_unknown_stack_stays_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); packet = request(); del packet['domains']
            (root / 'openapi.json').write_text('{"openapi":"3.1.0"}')
            (root / 'schema.sql').write_text('-- synthetic schema')
            result = form_project(root, packet)
            self.assertEqual(result['formation']['domain_decisions']['api'], 'contract_source:openapi.json')
            self.assertIn('docs/data/README.md', result['formation']['selected'])
            self.assertEqual(result['formation']['acceptance'], 'not_accepted')

    def test_budget_and_invalid_previous_plan_leave_no_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, stage = Path(tmp) / 'project', Path(tmp) / 'stage'; root.mkdir()
            packet = request(); packet['document_facts'] = {'architecture': {'source': 'fixture', 'sections': {'facts': 'x'*41000}}}
            with self.assertRaisesRegex(Exception, 'budget'): form_project(root, packet)
            self.assertFalse(stage.exists())
            packet = request(); preview = form_project(root, packet)
            with self.assertRaises(ValueError):
                form_project(root, packet, stage=stage, approved_preview_digest=preview['formation']['digest'], previous=[])
            self.assertFalse(stage.exists())

    def test_root_document_alias_and_encoded_navigation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, stage = Path(tmp) / 'project', Path(tmp) / 'stage'; (root / 'docs').mkdir(parents=True)
            (root / 'docs/requirements.md').write_text('# Existing requirements\nKeep R-01')
            packet = request(); packet['canonical_paths'] = {'architecture': 'docs/design (local).md'}
            result = stage_request(root, stage, packet)
            self.assertEqual(result['formation']['owners']['REQUIREMENTS.md'], 'docs/requirements.md')
            self.assertNotIn('REQUIREMENTS.md', result['formation']['selected'])
            apply_merge_plan(root, stage, approve(root, stage))
            self.assertEqual(check_local_links(root, ['docs/README.md']), [])
            self.assertEqual((root / 'docs/requirements.md').read_text(), '# Existing requirements\nKeep R-01')

    def test_real_process_exit_after_atomic_write_recovers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, stage = Path(tmp) / 'project', Path(tmp) / 'stage'; root.mkdir()
            stage_request(root, stage, request()); approval = approve(root, stage)
            code = ('import sys,os; sys.path.insert(0,sys.argv[1]); '
                    'from product_agent_os import merge_infrastructure as m; old=m._apply_decision; '
                    'm._apply_decision=lambda *a: (old(*a),os._exit(17)); '
                    'm.apply_merge_plan(sys.argv[2],sys.argv[3],sys.argv[4])')
            proc = subprocess.run([sys.executable, '-B', '-c', code, str(SCRIPTS), str(root), str(stage), str(approval)],
                                  capture_output=True, text=True, timeout=30)
            self.assertEqual(proc.returncode, 17, proc.stderr)
            self.assertTrue(any(p.is_file() for p in root.rglob('*')))
            rollback_merge(root, stage / 'product-agent-os-rollback-manifest.json')
            self.assertFalse(any(p.is_file() for p in root.rglob('*')))

    def test_three_integrated_profiles(self):
        cases = json.loads((SCRIPTS.parents[2] / 'tests/fixtures/product_agent_os/g9-project-formation/cases.json').read_text())
        for case in cases:
            with self.subTest(profile=case['id']):
                self.assertEqual(run_pilot(case)['status'], 'passed')

    def test_tampered_binding_cannot_hide_actual_manifest_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, stage = Path(tmp) / 'project', Path(tmp) / 'stage'; root.mkdir()
            stage_request(root, stage, request())
            path = stage / 'product-agent-os-stage-manifest.json'
            payload = json.loads(path.read_text()); payload['formation']['selected'] = []
            path.write_text(json.dumps(payload))
            self.assertTrue(any('target set' in x for x in build_merge_plan(root, stage)['blocked']))

    def test_blocked_source_does_not_create_partial_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, stage = Path(tmp) / 'project', Path(tmp) / 'stage'; root.mkdir()
            (root / 'AGENTS.md').write_text('<!-- product-agent-os:start project-rules -->\n' * 2)
            preview = form_project(root, request())
            self.assertTrue(preview['infrastructure_plan']['blocked'])
            with self.assertRaisesRegex(Exception, 'validation failed'):
                form_project(root, request(), stage=stage, approved_preview_digest=preview['formation']['digest'])
            self.assertFalse(stage.exists())


if __name__ == '__main__':
    if '--report' in sys.argv:
        import argparse
        parser = argparse.ArgumentParser(); parser.add_argument('--report', required=True); parser.add_argument('--baseline', required=True)
        args = parser.parse_args(); root = SCRIPTS.parents[2]
        fixture = root / 'tests/fixtures/product_agent_os/g9-project-formation/cases.json'
        cases = json.loads(fixture.read_text())
        source_paths = [SCRIPTS / 'product_agent_os' / name for name in
                        ['project_formation.py', 'infrastructure.py', 'merge_infrastructure.py', 'stage_manifest.py', 'templates.py']]
        source_paths += [SCRIPTS / 'render_infrastructure.py', Path(__file__), fixture,
                         SCRIPTS.parent / 'assets/templates/workflows/project-formation.md',
                         SCRIPTS.parent / 'skills/implementation-planner/SKILL.md']
        payload = {'schema_version': 1, 'group': 'PAOS-AUD-G9', 'owner_acceptance': 'pending',
                   'environment': {'python': platform.python_version(), 'system': platform.system(), 'providers': False},
                   'baseline_revision': (Path(args.baseline).parent / 'baseline-revision.txt').read_text().strip(),
                   'source_hashes': {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},
                   'comparison': 'same workspace and request; baseline receives identical task facts; desired domains unsupported in baseline',
                   'profiles': [run_pilot(c, Path(args.baseline) / 'scripts') for c in cases]}
        Path(args.report).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
        print('G9 comparison: 3/3 profiles passed; source hashes recorded; owner acceptance pending')
    else:
        unittest.main()
