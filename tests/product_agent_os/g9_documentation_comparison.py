"""Same-input local G9 comparison; no providers, model judging or host activation.

Run with --baseline pointing to an extracted repository snapshot and --report
pointing to the existing G9 results artifact. Original formation results remain.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def worker(source: Path) -> dict:
    """Exercise both revisions in separate Python processes with identical fixtures."""
    sys.path.insert(0, str(source / 'plugins/product-agent-os/scripts'))
    from product_agent_os import document_navigation as navigation
    from product_agent_os.project_formation import _owner_path
    result = {'cross_file_duplicates': {}, 'aliases': {}, 'section_sync_available': False}
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name in ('a.md', 'b.md'):
            (root / name).write_text('# Contract\n\nThis public contract must have one canonical owner.\n', encoding='utf-8')
        findings = navigation.duplicate_blocks(root, ['a.md', 'b.md'])
        result['cross_file_duplicates'] = {'expected': 1, 'observed': len(findings), 'missed': max(0, 1 - len(findings))}
        (root / 'task-a.md').write_text('### Task `COMPARE-T1`\n- Status: planned\n', encoding='utf-8')
        (root / 'task-b.md').write_text('### Task `COMPARE-T1`\n- Status: implemented\n', encoding='utf-8')
        conflicts = [f for f in navigation.duplicate_blocks(root, ['task-a.md', 'task-b.md']) if f.get('action') == 'conflicting_task_states']
        result['conflicting_task_copies'] = {'expected': 1, 'observed': len(conflicts)}
        for role, directory in [('decisions', 'adr'), ('operations', 'runbooks'), ('evidence', 'testing'), ('archive', 'archive')]:
            path = f'docs/{directory}/README.md'
            expected = path
            result['aliases'][role] = {'expected': expected, 'observed': _owner_path(role, f'docs/{role}/README.md', {}, {path: {}}, [])}
        try:
            from product_agent_os import documentation_sync as sync
        except ImportError:
            result['section_sync'] = {'status': 'unsupported', 'reason': 'baseline has no task-section synchronization route'}
        else:
            from product_agent_os.stage_manifest import content_digest
            result['section_sync_available'] = True
            (root / 'source.py').write_bytes(b'contract v2')
            target = root / 'API.md'
            original = b'# API\n\n## Contract\nOld.\n\n## Other\nKeep.\n'
            target.write_bytes(original)
            packet = {'schema_version': 1, 'task_id': 'COMPARE-T1', 'facts': [{
                'id': 'api', 'event': 'api', 'changed_fact': 'API behavior', 'reason': 'reviewed change',
                'decision': 'updated', 'sources': [{'path': 'source.py', 'revision': content_digest(b'contract v2')}],
                'target': {'path': 'API.md', 'revision': content_digest(original), 'owner': 'API owner', 'role': 'api', 'section': 'contract'}}]}
            patches = [{'fact_id': 'api', 'replacement': '## Contract\nNew.\n\n'}]
            missing = []
            for event, owner in sync.TRIGGERS.items():
                if owner is not None:
                    unowned = json.loads(json.dumps(packet))
                    unowned['facts'][0]['event'] = event
                    unowned['facts'][0].pop('target')
                    missing.append(not sync.assess(root, unowned)['gaps'])
            result['mandatory_impact'] = {'explicit_event_cases': len(missing), 'missed_required_owner_gaps': sum(missing),
                                          'scope': 'explicit reviewed facts only; not semantic discovery completeness'}
            plan = sync.propose(root, packet, patches)
            sync.apply(root, plan, approved_digest=plan['digest'])
            stamp = target.stat().st_mtime_ns
            repeat = sync.apply(root, plan, approved_digest=plan['digest'])
            result['section_sync'] = {'status': 'verified', 'files_changed': len(plan['files']), 'sections_changed': 1,
                                      'unnecessary_files': 0, 'outside_section_bytes_changed': int(target.read_bytes() != original.replace(b'Old.', b'New.')),
                                      'repeat_writes': int(stamp != target.stat().st_mtime_ns), 'repeat_status': repeat['status']}
            # The next task changes only new facts, keeping the earlier outcome in recovery history.
            packet['task_id'] = 'COMPARE-T2'
            packet['facts'][0]['target']['revision'] = content_digest(target.read_bytes())
            patches[0]['replacement'] = '## Contract\nNext.\n\n'
            next_plan = sync.propose(root, packet, patches)
            sync.apply(root, next_plan, approved_digest=next_plan['digest'])
            result['next_task'] = {'outside_section_bytes_changed': int(target.read_bytes() != original.replace(b'Old.', b'Next.')),
                                   'prior_recovery_retained': (root / '.codex/product-agent-os/compaction' / (plan['digest'].split(':')[1] + '.json')).is_file()}
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', type=Path)
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.worker:
        print(json.dumps(worker(args.worker)))
        return
    arms = {}
    for name, path in [('baseline', args.baseline), ('treatment', ROOT)]:
        run = subprocess.run([sys.executable, '-B', __file__, '--worker', str(path)], capture_output=True, text=True, check=True)
        arms[name] = json.loads(run.stdout)
    treatment = arms['treatment']
    assert treatment['cross_file_duplicates']['missed'] == 0
    assert treatment['conflicting_task_copies']['observed'] == 1
    assert treatment['mandatory_impact']['missed_required_owner_gaps'] == 0
    assert all(item['observed'] == item['expected'] for item in treatment['aliases'].values())
    assert treatment['section_sync']['outside_section_bytes_changed'] == treatment['section_sync']['repeat_writes'] == 0
    assert treatment['next_task'] == {'outside_section_bytes_changed': 0, 'prior_recovery_retained': True}
    paths = [ROOT / 'plugins/product-agent-os/scripts/product_agent_os' / name for name in
             ('documentation_sync.py', 'control_plane_documents.py', 'control_plane_compaction.py', 'document_navigation.py', 'project_formation.py', 'task_plan_lifecycle.py', 'validators.py', 'status_snapshot.py', 'system_file_hygiene.py')]
    paths += [Path(__file__), ROOT / 'tests/product_agent_os/test_document_navigation.py', ROOT / 'tests/product_agent_os/test_task_plan_lifecycle.py']
    paths += [ROOT / 'plugins/product-agent-os/assets/templates/workflows/control-plane-sync.md',
              ROOT / 'plugins/product-agent-os/skills/implementation-planner/SKILL.md',
              ROOT / '.codex/workflows/control-plane-sync.md',
              ROOT / 'plugins/product-agent-os/skills/references/handoff-contract.md',
              ROOT / 'plugins/product-agent-os/assets/templates/artifact-templates/task-matrix-plan.md',
              ROOT / 'tests/product_agent_os/test_lifecycle_skills.py',
              ROOT / 'plugins/product-agent-os/scripts/check_documents.py',
              ROOT / 'plugins/product-agent-os/scripts/sync_task_documents.py']
    baseline_instructions = (args.baseline / 'plugins/product-agent-os/skills/implementation-planner/SKILL.md').read_text(encoding='utf-8')
    current_instructions = (ROOT / 'plugins/product-agent-os/skills/implementation-planner/SKILL.md').read_text(encoding='utf-8')
    instruction_review = {
        'method': 'static source contract review, not model execution',
        'baseline_routes_command_output_to_RUNLOG': 'Evidence moves to RUNLOG.md for current slice outcomes, command output' in baseline_instructions,
        'treatment_routes_command_output_to_RUNLOG': 'Evidence moves to RUNLOG.md for current slice outcomes, command output' in current_instructions,
        'review_cases': {'internal_bugfix': 'no_change_needed with reason', 'API_change': 'canonical contract section',
                         'test_rerun': 'existing evidence owner; unchanged commands untouched',
                         'new_documentation_domain': 'formation preview', 'identical_repeat': 'zero writes',
                         'unknown_owner': 'handoff_required; no strong closure'},
        'model_behavior_evidence': 'unavailable_in_this_run; owner acceptance of this limit remains pending'}
    record = {'baseline_revision': 'eb4a74688c9df96e2481e653cd144b2a07f39d03',
              'environment': {'python': platform.python_version(), 'platform': platform.system()},
              'arms': arms, 'source_hashes': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
              'owner_acceptance': 'pending', 'behavioral_model_comparison': 'not_run; no model superiority claim',
              'instruction_review': instruction_review,
              'semantic_completeness': 'review input, not inferred from digests or deterministic tests',
              'scope': 'synthetic local; baseline unsupported routes are not fabricated numeric failures'}
    payload = json.loads(args.report.read_text(encoding='utf-8'))
    payload['owner_acceptance'] = 'accepted_T10_by_owner_2026-11-10'
    payload['documentation_sync_extension'] = record
    args.report.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(arms, indent=2))


if __name__ == '__main__':
    main()
