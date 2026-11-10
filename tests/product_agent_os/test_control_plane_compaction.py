import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'plugins/product-agent-os/scripts'))
from product_agent_os import control_plane_compaction as compaction


class CompactionTest(unittest.TestCase):
    def test_explicit_move_can_retain_large_detailed_planning_matrix(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'docs/planning').mkdir(parents=True)
            current = ('### Task `P-01`\n- ID: P-01\n- Status: planned\n- Acceptance criteria: retained\n' + 'Detail.\n' * 6000).encode()
            name = 'docs/planning/tasks.md'
            (root / name).write_bytes(current + b'closed receipt\n')
            moves = [dict(source=name, start=len(current), end=len(current) + 15,
                          destination='docs/history.md', classification='history', owner='fixture', reason='explicit closed receipt move')]
            plan = compaction.propose(root, moves)
            self.assertGreater(next(f['after_bytes'] for f in plan['files'] if f['path'] == name), 40000)
            self.assertEqual((root / name).read_bytes(), current + b'closed receipt\n')

    def fixture(self, root):
        current = '# Current\r\nR-01 open; gate owner acceptance pending\r\n'.encode()
        history = ('## Receipt\r\nFailed attempt preserved Я🙂\r\n' * 1000).encode()
        (root / 'RUNLOG.md').write_bytes(current + history)
        return current, history, [{'source': 'RUNLOG.md', 'start': len(current),
                                  'end': len(current + history), 'destination': 'docs/history.md',
                                  'classification': 'history', 'owner': 'project', 'reason': 'closed cycle'}]

    def test_proposal_is_read_only_and_apply_preserves_original_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            current, history, moves = self.fixture(root)
            plan = compaction.propose(root, moves)
            self.assertEqual((root / 'RUNLOG.md').read_bytes(), current + history)
            self.assertFalse((root / 'docs').exists())
            receipt = compaction.apply(root, plan, approved_digest=plan['digest'])
            self.assertIn(current, (root / 'RUNLOG.md').read_bytes())
            self.assertEqual((root / 'docs/history.md').read_bytes(), history)
            self.assertLessEqual((root / 'RUNLOG.md').stat().st_size, 40000)
            self.assertEqual(compaction.apply(root, plan, approved_digest=plan['digest'])['status'], 'already_applied')
            compaction.rollback(root, receipt['journal'])
            self.assertEqual((root / 'RUNLOG.md').read_bytes(), current + history)
            self.assertFalse((root / 'docs/history.md').exists())

    def test_stale_input_and_wrong_approval_do_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, _, moves = self.fixture(root)
            plan = compaction.propose(root, moves)
            with self.assertRaises(ValueError):
                compaction.apply(root, plan, approved_digest='wrong')
            (root / 'RUNLOG.md').write_bytes(b'Concurrent work')
            with self.assertRaisesRegex(ValueError, 'conflict'):
                compaction.apply(root, plan, approved_digest=plan['digest'])
            self.assertEqual((root / 'RUNLOG.md').read_bytes(), b'Concurrent work')

    def test_interrupted_write_rolls_back_without_losing_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            current, history, moves = self.fixture(root)
            plan = compaction.propose(root, moves)
            def fail(index):
                if index == 1:
                    raise OSError('injected disk failure')
            with self.assertRaisesRegex(OSError, 'injected'):
                compaction.apply(root, plan, approved_digest=plan['digest'], after_write=fail)
            self.assertEqual((root / 'RUNLOG.md').read_bytes(), current + history)
            self.assertFalse((root / 'docs/history.md').exists())

    def test_invalid_paths_overlaps_and_unknown_classification_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, _, moves = self.fixture(root)
            for field, value in [('destination', '../escape.md'), ('classification', 'unknown'),
                                 ('destination', 'runlog.md'), ('destination', 'docs//history.md'),
                                 ('destination', '.GIT/history.md')]:
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    compaction.propose(root, [moves[0] | {field: value}])
            with self.assertRaises(ValueError):
                compaction.propose(root, moves * 2)

    def test_rollback_preserves_post_apply_user_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, _, moves = self.fixture(root)
            plan = compaction.propose(root, moves)
            receipt = compaction.apply(root, plan, approved_digest=plan['digest'])
            (root / 'docs/history.md').write_bytes(b'new user work')
            with self.assertRaisesRegex(ValueError, 'conflict'):
                compaction.rollback(root, receipt['journal'])
            self.assertEqual((root / 'docs/history.md').read_bytes(), b'new user work')

    def test_rehashed_lossy_plan_is_rejected_before_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            current, history, moves = self.fixture(root)
            plan = compaction.propose(root, moves)
            item = next(f for f in plan['files'] if f['path'] == 'RUNLOG.md')
            item['after'] = compaction._encode(b'gate lost')
            item['after_digest'] = compaction.content_digest(b'gate lost')
            item['after_bytes'] = len(b'gate lost')
            item['diff'] = ''.join(compaction.difflib.unified_diff(
                compaction._decode(item['before']).decode().splitlines(True), ['gate lost'],
                item['path'], item['path']))
            plan['digest'] = compaction._digest(plan)
            with self.assertRaisesRegex(ValueError, 'preservation'):
                compaction.apply(root, plan, approved_digest=plan['digest'])
            self.assertEqual((root / 'RUNLOG.md').read_bytes(), current + history)

    def test_sql_projection_and_frozen_source_cannot_be_compacted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, _, moves = self.fixture(root)
            (root / '.codex').mkdir()
            for mode in ('sql', 'frozen', 'unknown'):
                (root / '.codex/config.toml').write_text(
                    '[product_agent_os.documents]\nauthority = "' + mode + '"\n'
                    'task_projections = ["RUNLOG.md"]\n', encoding='utf-8')
                with self.subTest(mode=mode), self.assertRaisesRegex(ValueError, 'authority'):
                    compaction.propose(root, moves)

    def test_crash_journal_can_recover_only_after_explicit_lock_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            current, history, moves = self.fixture(root)
            plan = compaction.propose(root, moves)
            import json
            import subprocess
            proposal = root / 'proposal.json'
            proposal.write_text(json.dumps(plan), encoding='utf-8')
            code = ("import json,os,sys; from pathlib import Path; "
                    "sys.path.insert(0,sys.argv[1]); "
                    "from product_agent_os.control_plane_compaction import apply; "
                    "root=Path(sys.argv[2]); plan=json.loads((root/'proposal.json').read_text()); "
                    "apply(root,plan,approved_digest=plan['digest'],after_write=lambda index:os._exit(23))")
            process = subprocess.run([sys.executable, '-B', '-c', code, str(Path(compaction.__file__).parents[1]), str(root)],
                                     capture_output=True, timeout=30)
            self.assertEqual(process.returncode, 23, process.stderr)
            receipt = {'journal': compaction.JOURNAL_ROOT + '/' + plan['digest'].split(':')[1] + '.json'}
            lock = root / compaction.LOCK
            self.assertEqual(lock.read_text(), plan['digest'])
            with self.assertRaises(FileExistsError):
                compaction.rollback(root, receipt['journal'])
            compaction.rollback(root, receipt['journal'], abandoned_lock_digest=plan['digest'])
            self.assertEqual((root / 'RUNLOG.md').read_bytes(), current + history)

    def test_stricter_budget_and_broken_links_block_before_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            current, history, moves = self.fixture(root)
            (root / '.codex').mkdir()
            (root / '.codex/config.toml').write_text('[product_agent_os.documents.limits]\n"RUNLOG.md" = 10\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'budget'):
                compaction.propose(root, moves)
            (root / '.codex/config.toml').write_bytes(b'')
            (root / 'RUNLOG.md').write_bytes(current + history + b'\n[broken](missing.md)\n')
            plan = compaction.propose(root, moves)
            with self.assertRaisesRegex(ValueError, 'link'):
                compaction.apply(root, plan, approved_digest=plan['digest'])
            self.assertTrue((root / 'RUNLOG.md').read_bytes().startswith(current + history))
            self.assertFalse((root / 'docs/history.md').exists())

    def test_redirected_file_and_existing_destination_bytes_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, _, moves = self.fixture(root)
            (root / 'docs').mkdir(exist_ok=True)
            destination = root / 'docs/history.md'
            destination.write_bytes(b'prior history\r\n')
            plan = compaction.propose(root, moves)
            receipt = compaction.apply(root, plan, approved_digest=plan['digest'])
            self.assertTrue(destination.read_bytes().startswith(b'prior history\r\n'))
            compaction.rollback(root, receipt['journal'])
            self.assertEqual(destination.read_bytes(), b'prior history\r\n')
            from unittest.mock import patch
            for method in ('is_junction', 'is_symlink'):
                with patch.object(Path, method, return_value=True), self.assertRaisesRegex(ValueError, 'redirected'):
                    compaction.propose(root, moves)

    def test_multiple_sources_have_deterministic_preservation_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'A.md').write_bytes(b'A body')
            (root / 'B.md').write_bytes(b'B body')
            moves = [{'source': name, 'start': 0, 'end': 6, 'destination': 'history.md',
                      'classification': 'history', 'owner': 'owner', 'reason': 'closed'}
                     for name in ('B.md', 'A.md')]
            plan = compaction.propose(root, moves)
            compaction.apply(root, plan, approved_digest=plan['digest'])
            self.assertEqual((root / 'history.md').read_bytes(), b'A bodyB body')


if __name__ == '__main__':
    unittest.main()
