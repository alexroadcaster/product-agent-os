import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'plugins/product-agent-os/scripts'))
from product_agent_os import document_navigation as navigation
from product_agent_os import control_plane_compaction as compaction


class DocumentNavigationTest(unittest.TestCase):
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
