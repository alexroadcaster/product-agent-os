import hashlib
import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'docs/superpowers/specs/batch45-code-quality-heldout-corpus.json'


class HeldoutCorpusTest(unittest.TestCase):
    def test_freeze_inventory_and_synthetic_privacy(self):
        corpus = json.loads(MANIFEST.read_text())
        tasks = corpus['tasks']
        self.assertTrue(12 <= len(tasks) <= 16)
        self.assertEqual(len({t['task_id'] for t in tasks}), len(tasks))
        self.assertGreaterEqual(len({t['stack_family'] for t in tasks}), 4)
        self.assertGreaterEqual(len({t['risk_class'] for t in tasks}), 5)
        self.assertTrue({'reuse', 'deletion', 'configuration', 'no_new_code'} <= {t['expected_action'] for t in tasks})
        self.assertFalse(corpus['treatment_outputs_inspected'])
        self.assertEqual(corpus['content_sha256'], hashlib.sha256(json.dumps(tasks, sort_keys=True, separators=(',', ':')).encode()).hexdigest())
        for task in tasks:
            folder = ROOT / task['path']
            self.assertEqual(set(task['sha256']), {p.name for p in folder.iterdir() if p.is_file()})
            for name, digest in task['sha256'].items():
                data = (folder / name).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), digest)
                text = data.decode('utf-8')
                self.assertNotRegex(text, r'(?i)(?:[A-Z]:[\\/]Users[\\/]|/home/|sk-[a-z0-9]{20}|BEGIN .*PRIVATE KEY)')

    def test_reference_passes_and_seeded_fault_is_detected_for_every_task(self):
        for task in json.loads(MANIFEST.read_text())['tasks']:
            for variant, expected in [('input_file', task['initial_expected_pass']), ('reference_file', True), ('seeded_file', False)]:
                with self.subTest(task=task['task_id'], variant=variant):
                    folder = ROOT / task['path']
                    args = [str((folder / task[variant]).resolve()) if x == '{candidate}' else x for x in task['check_command']]
                    if args[0] == 'python': args[0:1] = [sys.executable, '-B']
                    else:
                        executable = shutil.which(args[0])
                        self.assertIsNotNone(executable, f'required corpus runtime missing: {args[0]}')
                        args[0] = executable
                    result = subprocess.run(args, cwd=folder, capture_output=True, text=True, timeout=15)
                    self.assertEqual(result.returncode == 0, expected, result.stderr)
                    if not expected:
                        self.assertRegex(result.stderr, r'AssertionError|regression|assertion', 'Fault must fail its oracle, not setup')
