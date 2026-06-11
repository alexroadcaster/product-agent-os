from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


from product_agent_os.batch39_target_mutation import (  # noqa: E402
    build_target_mutation_proof,
    validate_target_mutation_proof,
)


class Batch39TargetMutationTests(unittest.TestCase):
    def test_builds_no_mutation_proof_without_raw_paths_or_file_bodies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            before = Path(tmp) / "before"
            after = Path(tmp) / "after"
            before.mkdir()
            (before / "README.md").write_text("hello\n", encoding="utf-8")
            shutil.copytree(before, after)

            proof = build_target_mutation_proof(
                test_id="B39-TEST-M04",
                attempt_id="B39-TEST-M04-A01",
                before_root=before,
                after_root=after,
                target_ref="synthetic-target",
                generated_at="2026-06-11T00:00:00+00:00",
            )

        self.assertEqual(proof["schema_version"], "target_mutation_proof_v1")
        self.assertEqual(proof["test_id"], "B39-TEST-M04")
        self.assertEqual(proof["diff"]["status"], "unchanged")
        self.assertEqual(proof["verdict"], "no_mutation_detected")
        self.assertEqual(proof["approval_boundary"]["target_workspace_mutation"], "not_performed")
        self.assertEqual(proof["approval_boundary"]["mcp_server_activation"], "not_performed")
        self.assertEqual(proof["approval_boundary"]["agents_sdk_runner_activation"], "not_performed")
        self.assertEqual(proof["approval_boundary"]["canonical_graph_mutation"], "not_performed")
        self.assertFalse(proof["redaction"]["absolute_paths_stored"])
        self.assertFalse(proof["redaction"]["raw_file_bodies_stored"])
        self.assertEqual(validate_target_mutation_proof(proof), [])

        encoded = json.dumps(proof, ensure_ascii=False)
        self.assertIn("README.md", encoded)
        self.assertNotIn("hello", encoded)
        self.assertNotIn("C:\\", encoded)
        self.assertNotIn(str(Path.home()), encoded)

    def test_validation_blocks_unapproved_target_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            before = Path(tmp) / "before"
            after = Path(tmp) / "after"
            before.mkdir()
            (before / "README.md").write_text("before\n", encoding="utf-8")
            shutil.copytree(before, after)
            (after / "README.md").write_text("after\n", encoding="utf-8")
            (after / "new.txt").write_text("new\n", encoding="utf-8")

            proof = build_target_mutation_proof(
                test_id="B39-TEST-M04",
                attempt_id="B39-TEST-M04-A01",
                before_root=before,
                after_root=after,
                target_ref="synthetic-target",
                generated_at="2026-06-11T00:00:00+00:00",
            )

        self.assertEqual(proof["diff"]["status"], "changed")
        self.assertEqual(proof["diff"]["modified"], ["README.md"])
        self.assertEqual(proof["diff"]["added"], ["new.txt"])
        self.assertEqual(proof["verdict"], "unapproved_mutation_detected")
        self.assertIn("unapproved target mutation detected", validate_target_mutation_proof(proof))

    def test_approved_mutation_requires_approval_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            before = Path(tmp) / "before"
            after = Path(tmp) / "after"
            before.mkdir()
            (before / "a.txt").write_text("a\n", encoding="utf-8")
            shutil.copytree(before, after)
            (after / "a.txt").write_text("b\n", encoding="utf-8")

            missing_approval = build_target_mutation_proof(
                test_id="B39-TEST-M04",
                attempt_id="B39-TEST-M04-A01",
                before_root=before,
                after_root=after,
                target_ref="synthetic-target",
                mutation_allowed=True,
            )
            approved = build_target_mutation_proof(
                test_id="B39-TEST-M04",
                attempt_id="B39-TEST-M04-A01",
                before_root=before,
                after_root=after,
                target_ref="synthetic-target",
                mutation_allowed=True,
                approval_ref="owner-approved-target-mutation-001",
            )

        self.assertIn("mutation_allowed requires approval_ref", validate_target_mutation_proof(missing_approval))
        self.assertEqual(approved["verdict"], "approved_mutation_detected")
        self.assertEqual(validate_target_mutation_proof(approved), [])

    def test_cli_writes_target_mutation_proof(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            before = root / "before"
            after = root / "after"
            before.mkdir()
            (before / "docs").mkdir()
            (before / "docs" / "note.md").write_text("note\n", encoding="utf-8")
            shutil.copytree(before, after)
            output = root / "target-mutation-proof.example.json"

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "create_target_mutation_proof.py"),
                    "--output",
                    str(output),
                    "--test-id",
                    "B39-TEST-M04",
                    "--attempt-id",
                    "B39-TEST-M04-A01",
                    "--before-root",
                    str(before),
                    "--after-root",
                    str(after),
                    "--target-ref",
                    "synthetic-target",
                    "--generated-at",
                    "2026-06-11T00:00:00+00:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(validate_target_mutation_proof(payload), [])
            self.assertEqual(payload["verdict"], "no_mutation_detected")
            self.assertIn('"status": "ok"', result.stdout)


if __name__ == "__main__":
    unittest.main()
