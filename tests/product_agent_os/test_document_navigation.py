import hashlib
import sys
import tempfile
import unittest
import copy
import json
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'plugins/product-agent-os/scripts'))
from product_agent_os import document_navigation as navigation
from product_agent_os import control_plane_compaction as compaction


class DocumentNavigationTest(unittest.TestCase):
    def test_summary_requires_current_canonical_source_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = b'# Source\n' + b'Detailed supported facts.\n' * 30
            (root / 'source.md').write_bytes(raw)
            (root / 'summary.md').write_text('# Brief\n\n[Details](source.md)\n')
            record = {'kind': 'summary', 'path': 'summary.md', 'source': 'source.md', 'source_link': 'source.md',
                      'owner': 'docs owner', 'reason': 'navigation summary', 'source_digest': hashlib.sha256(raw).hexdigest()}
            self.assertEqual(navigation.check_reference(root, record)['status'], 'verified')
            (root / 'source.md').write_bytes(raw + b'Changed')
            self.assertEqual(navigation.check_reference(root, record)['status'], 'stale')

    def test_sync_public_cli_preview_apply_rollback(self):
        script = Path(__file__).resolve().parents[2] / 'plugins/product-agent-os/scripts/sync_task_documents.py'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sync, packet, patches, raw = self.sync_fixture(root)
            request = root / 'task-packet.json'
            request.write_text(json.dumps({'impact': packet, 'patches': patches}), encoding='utf-8')
            preview = subprocess.run([sys.executable, '-B', str(script), str(root), 'preview', str(request)], capture_output=True, text=True)
            self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
            plan = json.loads(preview.stdout)
            self.assertEqual((root / 'docs/api/README.md').read_bytes(), raw)
            proposal = root / 'proposal.json'
            proposal.write_text(json.dumps(plan), encoding='utf-8')
            command = [sys.executable, '-B', str(script), str(root), 'apply', str(proposal)]
            denied = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(denied.returncode, 1)
            applied = subprocess.run(command + ['--approved-digest', plan['digest']], capture_output=True, text=True)
            self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
            journal = json.loads(applied.stdout)['journal']
            recovered = subprocess.run([sys.executable, '-B', str(script), str(root), 'rollback', journal], capture_output=True, text=True)
            self.assertEqual(recovered.returncode, 0, recovered.stdout + recovered.stderr)
            self.assertEqual((root / 'docs/api/README.md').read_bytes(), raw)

    def test_each_changed_information_class_requires_owned_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sync, packet, patches, raw = self.sync_fixture(root)
            fact = packet['facts'][0]
            fact.pop('target')
            for event, owner in sync.TRIGGERS.items():
                if owner is None:
                    continue
                with self.subTest(event=event):
                    fact['event'] = event
                    self.assertEqual(sync.assess(root, packet)['status'], 'handoff_required')

    def test_sync_owner_aliases_and_required_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sync, packet, patches, raw = self.sync_fixture(root)
            for event, directory in [('decision', 'adr'), ('operations', 'runbooks'), ('evidence', 'testing'), ('retained_history', 'archive')]:
                (root / f'docs/{directory}').mkdir()
                (root / f'docs/{directory}/README.md').write_text('# Existing\n')
                self.assertEqual(sync.owner_candidates(root, event)['paths'], [f'docs/{directory}/README.md'])
            packet['facts'][0]['decision'] = 'no_change_needed'
            with self.assertRaisesRegex(ValueError, 'coverage'):
                sync.assess(root, packet)
            packet['facts'][0]['existing_coverage'] = 'Contract section already specifies this requirement'
            self.assertEqual(sync.assess(root, packet)['gaps'], [])

    def test_sync_budget_ambiguous_sections_and_link_preservation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sync, packet, patches, raw = self.sync_fixture(root)
            patches[0]['replacement'] = '## Contract\n' + 'я' * 21000 + '\n'
            with self.assertRaisesRegex(ValueError, '40000'):
                sync.propose(root, packet, patches)
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                sync.section_range(b'## Same\nA\n## Same\nB\n', 'same')
            self.assertEqual(sync.section_range(b'## Contract {#c}\nText\n## Other\n', 'c'), (0, len(b'## Contract {#c}\nText\n')))

    def test_duplicate_disposition_must_be_fresh_and_cannot_mask_conflicts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = b'# Contract\n\nA sufficiently long current contract paragraph.\n'
            for name in ('a.md', 'b.md'):
                (root / name).write_bytes(raw)
            finding = navigation.duplicate_blocks(root, ['a.md', 'b.md'])[0]
            disposition = {'path': 'b.md', 'source': 'a.md', 'kind': 'mirror', 'owner': 'docs owner',
                           'reason': 'intentional published mirror', 'source_digest': hashlib.sha256(raw).hexdigest(),
                           'block_digest': finding['block_digest']}
            self.assertEqual(navigation.duplicate_blocks(root, ['a.md', 'b.md'], dispositions=[disposition])[0]['disposition'], 'allowed_mirror')
            disposition['source_digest'] = '0' * 64
            self.assertEqual(navigation.duplicate_blocks(root, ['a.md', 'b.md'], dispositions=[disposition])[0]['disposition'], 'needs_review')
            (root / 'a.md').write_text('### Task `SYNC-T1`\n- Status: planned\n')
            (root / 'b.md').write_text('### Task `SYNC-T1`\n- Status: implemented\n')
            self.assertEqual(navigation.duplicate_blocks(root, ['a.md', 'b.md'])[0]['action'], 'conflicting_task_states')

    def sync_fixture(self, root):
        from product_agent_os import documentation_sync as sync
        from product_agent_os.stage_manifest import content_digest
        (root / 'docs/api').mkdir(parents=True)
        (root / 'source.py').write_bytes(b'contract version 2\n')
        raw = '# API\r\n\r\n## Contract\r\nOld behavior.\r\n\r\n## Other\r\nPreserve exactly.\r\n'.encode()
        (root / 'docs/api/README.md').write_bytes(raw)
        packet = {'schema_version': 1, 'task_id': 'SYNC-T1', 'facts': [
            {'id': 'api', 'event': 'api', 'changed_fact': 'Contract behavior changed',
             'reason': 'Reviewed source contract', 'decision': 'updated',
             'sources': [{'path': 'source.py', 'revision': content_digest((root / 'source.py').read_bytes())}],
             'target': {'path': 'docs/api/README.md', 'revision': content_digest(raw),
                        'section': 'contract', 'owner': 'API maintainer', 'role': 'api'}}]}
        patches = [{'fact_id': 'api', 'replacement': '## Contract\r\nNew behavior.\r\n\r\n'}]
        return sync, packet, patches, raw

    def test_section_update_preserves_bytes_repeats_and_recovers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sync, packet, patches, raw = self.sync_fixture(root)
            plan = sync.propose(root, packet, patches)
            result = sync.apply(root, plan, approved_digest=plan['digest'])
            target = root / 'docs/api/README.md'
            self.assertEqual(target.read_bytes(), raw.replace(b'Old behavior.', b'New behavior.'))
            stamp = target.stat().st_mtime_ns
            self.assertEqual(sync.apply(root, plan, approved_digest=plan['digest'])['status'], 'already_applied')
            self.assertEqual(target.stat().st_mtime_ns, stamp)
            compaction.rollback(root, result['journal'])
            self.assertEqual(target.read_bytes(), raw)

    def test_section_conflicts_freeze_and_tamper_fail_closed(self):
        from product_agent_os.stage_manifest import content_digest
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sync, packet, patches, raw = self.sync_fixture(root)
            plan = sync.propose(root, packet, patches)
            tampered = copy.deepcopy(plan)
            tampered['files'][0]['after'] = compaction._encode(b'destroyed')
            tampered['digest'] = compaction._digest(tampered)
            with self.assertRaises(ValueError):
                sync.apply(root, tampered, approved_digest=tampered['digest'])
            (root / 'source.py').write_bytes(b'later source')
            with self.assertRaisesRegex(ValueError, 'stale'):
                sync.apply(root, plan, approved_digest=plan['digest'])
            (root / 'source.py').write_bytes(b'contract version 2\n')
            config = root / '.codex/config.toml'
            config.parent.mkdir(exist_ok=True)
            config.write_text('[product_agent_os.documents]\nauthority="frozen"\n')
            with self.assertRaisesRegex(ValueError, 'authority'):
                sync.apply(root, plan, approved_digest=plan['digest'])
            config.write_text('[product_agent_os.documents]\nauthority="sql"\ntask_projections=["docs/api/README.md"]\n')
            with self.assertRaisesRegex(ValueError, 'authority'):
                sync.apply(root, plan, approved_digest=plan['digest'])
            self.assertEqual((root / 'docs/api/README.md').read_bytes(), raw)

    def test_section_failure_restores_and_later_edit_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sync, packet, patches, raw = self.sync_fixture(root)
            plan = sync.propose(root, packet, patches)
            def fail(_):
                raise RuntimeError('interrupted')
            with self.assertRaisesRegex(RuntimeError, 'interrupted'):
                sync.apply(root, plan, approved_digest=plan['digest'], after_write=fail)
            target = root / 'docs/api/README.md'
            self.assertEqual(target.read_bytes(), raw)
            result = sync.apply(root, plan, approved_digest=plan['digest'])
            target.write_bytes(b'later user edit')
            with self.assertRaisesRegex(ValueError, 'rollback conflict'):
                compaction.rollback(root, result['journal'])
            self.assertEqual(target.read_bytes(), b'later user edit')

    def test_no_change_and_unknown_owner_are_not_equivalent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sync, packet, patches, raw = self.sync_fixture(root)
            fact = packet['facts'][0]
            fact.update(event='test_rerun', decision='no_change_needed')
            fact.pop('target')
            plan = sync.propose(root, packet, [])
            self.assertEqual(sync.apply(root, plan, approved_digest=plan['digest'])['writes'], 0)
            self.assertFalse((root / '.codex').exists())
            fact.update(event='unknown', decision='handoff_required')
            self.assertEqual(sync.assess(root, packet)['status'], 'handoff_required')
            fact.update(event='test_rerun', decision='updated')
            with self.assertRaises(ValueError):
                sync.assess(root, packet)

    def test_explicit_markdown_anchor_is_resolved(self):
        self.assertIn((0, 'contract'), navigation._headings('## API {#contract}\n'))

    def test_cross_file_duplicates_require_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ('a.md', 'b.md'):
                (root / name).write_text('# Owner\n\nA sufficiently long duplicated contract paragraph.\n', encoding='utf-8')
            findings = navigation.duplicate_blocks(root, ['a.md', 'b.md'])
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0]['source_path'], 'a.md')
            self.assertEqual(findings[0]['path'], 'b.md')

    def test_split_rebinds_existing_selector_without_losing_task_states(self):
        import json
        from product_agent_os.status_snapshot import build_status_snapshot
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'research').mkdir()
            source = root / 'research/tasks.md'
            source.write_bytes(''.join(f'### Task `T{i}`\n- Status: planned\n#### Completion Report\n- status: planned\n' + 'detail ' * 90 + '\n' for i in range(9)).encode())
            reference = {'path': 'research/tasks.md', 'revision': 'sha256:' + hashlib.sha256(source.read_bytes()).hexdigest()}
            def select(refs):
                (root / 'PLAN.md').write_text('<!-- product-agent-os:current-state:start -->\n```json\n'
                    + json.dumps({'schema_version': 1, 'sources': refs})
                    + '\n```\n<!-- product-agent-os:current-state:end -->', encoding='utf-8')
            def state():
                return build_status_snapshot(workspace=root, generated_at='2026-11-10T00:00:00Z')['current_state']
            select([reference])
            before = {(r['task_id'], r['task_state']) for r in state()['tasks']}
            plan = compaction.propose(root, navigation.task_plan_moves(root, 'research/tasks.md', 'research/groups', limit=1000))
            references = navigation.split_source_references(plan, reference)
            self.assertEqual(len(references), 9)
            compaction.apply(root, plan, approved_digest=plan['digest'])
            self.assertEqual(state()['status'], 'unknown')  # Old pins cannot silently mask changed sources.
            select(references)
            self.assertEqual(state()['status'], 'projected')
            self.assertEqual({(r['task_id'], r['task_state']) for r in state()['tasks']}, before)

    def test_split_preserves_task_ids_links_and_original_card_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cards = [f'### Task `TEST-T{i}`\n\n- ID: TEST-T{i}\n- Depends on: TEST-T{i-1}\n\n#### Completion Report\n\n' + 'Я' * 5000 + '\n' for i in range(1, 4)]
            original = '# Plan\n\n' + ''.join(cards)
            (root / 'PLAN.md').write_bytes(original.encode('utf-8'))
            moves = navigation.task_plan_moves(root, 'PLAN.md', 'docs/tasks', limit=12000)
            plan = compaction.propose(root, moves, hard_limit=12000)
            compaction.apply(root, plan, approved_digest=plan['digest'])
            for i, card in enumerate(cards, 1):
                target = root / f'docs/tasks/part-{i:03}.md'
                self.assertEqual(target.read_bytes(), card.encode())
                self.assertIn(f'id="task-test-t{i}"', (root / 'PLAN.md').read_text())
            self.assertEqual(navigation.check_local_links(root, ['PLAN.md']), [])

    def test_mirror_and_required_evidence_are_not_inferred_from_presence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'source.md').write_text('current', encoding='utf-8')
            (root / 'mirror.md').write_text('old', encoding='utf-8')
            record = {'path': 'mirror.md', 'kind': 'mirror', 'source': 'source.md',
                      'source_digest': hashlib.sha256(b'old').hexdigest()}
            self.assertEqual(navigation.check_reference(root, record)['status'], 'stale')
            self.assertEqual(navigation.check_reference(root, {'path': 'absent.md', 'kind': 'required_evidence'})['status'], 'missing')
            self.assertEqual(navigation.check_reference(root, {'path': 'absent.md', 'kind': 'optional_evidence'})['status'], 'unavailable_optional')

    def test_cross_repository_reference_needs_bound_identity_revision_and_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = {'kind': 'cross_repository', 'path': 'README.md', 'repository': 'other'}
            self.assertEqual(navigation.check_reference(root, record)['status'], 'unknown')

    def test_existing_navigation_is_reused_and_optional_domains_need_triggers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'docs').mkdir()
            (root / 'docs/README.md').write_text('# Existing index', encoding='utf-8')
            (root / 'docs/runbooks').mkdir()
            result = navigation.documentation_inventory(root, signals={'api': False, 'operations': True})
            self.assertEqual(result['index'], 'docs/README.md')
            self.assertNotIn('api', result['needed_domains'])
            self.assertIn('operations', result['needed_domains'])
            self.assertEqual(result['needed_domains']['operations']['canonical_source'], 'docs/runbooks')

    def test_duplicate_blocks_and_portable_evidence_profile_are_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'README.md').write_text('# Read me\n\nRepeated current-state correction.\n\nRepeated current-state correction.\n', encoding='utf-8')
            self.assertEqual(len(navigation.duplicate_blocks(root, ['README.md'])), 1)
            evidence = root / 'evidence.json'
            evidence.write_bytes(b'{"outcome":"pass"}')
            record = {'kind': 'required_evidence', 'path': 'evidence.json', 'profile': 'offline_bundle',
                      'source_digest': hashlib.sha256(evidence.read_bytes()).hexdigest()}
            self.assertEqual(navigation.check_reference(root, record)['status'], 'verified')
            record['source_digest'] = ''
            self.assertEqual(navigation.check_reference(root, record)['status'], 'unknown')
