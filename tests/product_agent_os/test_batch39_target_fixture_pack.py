from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


from product_agent_os.batch39_target_fixture_pack import (  # noqa: E402
    build_target_fixture_pack,
    validate_target_fixture_pack,
)


class Batch39TargetFixturePackTests(unittest.TestCase):
    def test_builds_redacted_target_fixture_pack_for_idea_stage_architecture_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Neural_Flow"
            _write_target_fixture(target)

            pack = build_target_fixture_pack(
                target_root=target,
                target_label="Neural_Flow",
                generated_at="2026-06-11T00:00:00+00:00",
            )

            self.assertEqual(pack["schema_version"], "target_fixture_pack_v1")
            self.assertEqual(pack["test_id"], "B39-TEST-M11")
            self.assertEqual(pack["slice"], "B39-S2")
            self.assertEqual(pack["target"]["target_ref"], "approved_target:Neural_Flow")
            self.assertEqual(pack["target"]["mutation_allowed"], False)
            self.assertEqual(pack["control_plane"]["status"], "present")
            self.assertEqual(pack["inventory"]["git_repository_status"], "not_git_repository")
            self.assertEqual(pack["inventory"]["excluded_count"], 4)
            self.assertEqual(len(pack["inventory"]["excluded_entries"]), 4)
            self.assertEqual(pack["design_signals"]["architecture_phase_count"], 2)
            self.assertEqual(pack["design_signals"]["citation_density_signal"], 2)
            self.assertIn("docs_research", {item["archetype"] for item in pack["archetype_candidates"]})
            self.assertIn("ai_rag", {item["archetype"] for item in pack["archetype_candidates"]})
            self.assertEqual(pack["safety_profile"]["manual_verification_required"], True)
            self.assertEqual(pack["fixture_usage"]["raw_source_bodies_stored"], False)
            self.assertEqual(pack["approval_boundary"]["target_workspace_mutation"], "not_performed")
            self.assertEqual(pack["status"]["overall"], "prepared_for_s2_pilots")
            self.assertIn("sensitive_paths_excluded_from_inventory", pack["status"]["warnings"])
            self.assertTrue(pack["fixture_pack_digest"].startswith("sha256:"))

            encoded = json.dumps(pack, ensure_ascii=False, sort_keys=True)
            self.assertNotIn(str(target), encoded)
            self.assertNotIn("raw private body", encoded)
            self.assertNotIn(".env", encoded)
            self.assertNotIn("private.key", encoded)
            self.assertNotIn("debug.log", encoded)
            self.assertNotIn("config_secret.md", encoded)
            self.assertEqual(validate_target_fixture_pack(pack), [])

    def test_validation_rejects_absolute_paths_and_unapproved_actions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Neural_Flow"
            _write_target_fixture(target)
            pack = build_target_fixture_pack(target_root=target, target_label="Neural_Flow")
            pack["inventory"]["entries"][0]["path"] = r"C:\Users\person\secret.md"
            pack["approval_boundary"]["target_workspace_mutation"] = "performed"

            errors = validate_target_fixture_pack(pack)

            self.assertIn("local absolute path leaked", errors)
            self.assertIn("approval_boundary.target_workspace_mutation must be not_performed", errors)

    def test_cli_writes_target_fixture_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Neural_Flow"
            output = Path(tmp) / "target-fixture-pack.example.json"
            _write_target_fixture(target)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "create_target_fixture_pack.py"),
                    "--output",
                    str(output),
                    "--target-root",
                    str(target),
                    "--target-label",
                    "Neural_Flow",
                    "--generated-at",
                    "2026-06-11T00:00:00+00:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            pack = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(validate_target_fixture_pack(pack), [])
            self.assertIn('"status": "ok"', result.stdout)
            self.assertNotIn(str(output), result.stdout)


def _write_target_fixture(target: Path) -> None:
    for path in [
        target / "docs" / "superpowers" / "plans",
        target / "research",
        target / "legacy",
    ]:
        path.mkdir(parents=True, exist_ok=True)

    for name in ["REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]:
        (target / name).write_text(f"# {name}\n\nSource Of Truth\n", encoding="utf-8")
    (target / "README.md").write_text("# Neural Flow\n\nProduct Intent\n", encoding="utf-8")
    (target / "architecture-v2.md").write_text(
        "# Architecture\n\n## One [C101]\n\n## Two [C102]\n",
        encoding="utf-8",
    )
    (target / "architecture.md").write_text("# Legacy\n\n## One\n", encoding="utf-8")
    (target / "issues.md").write_text("- [ ] one\n- [x] two\n", encoding="utf-8")
    (target / "docs" / "superpowers" / "plans" / "plan.md").write_text("# Plan\n", encoding="utf-8")
    (target / "research" / "p2a-findings.md").write_text("# Research\nraw private body\n", encoding="utf-8")
    (target / "legacy" / "old.md").write_text("# Old\n", encoding="utf-8")
    (target / ".env").write_text("SECRET=fixture\n", encoding="utf-8")
    (target / "private.key").write_text("fixture-key\n", encoding="utf-8")
    (target / "debug.log").write_text("debug\n", encoding="utf-8")
    (target / "config_secret.md").write_text("secret notes\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
