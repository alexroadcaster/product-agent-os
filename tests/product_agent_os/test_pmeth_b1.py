"""Synthetic cases for the existing CLI and the task methodology decision."""

from __future__ import annotations

import copy
import hashlib
import json
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins/product-agent-os/scripts"
FIXTURE = ROOT / "tests/fixtures/product_agent_os/pmeth-b1-synthetic.json"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.cli import run_contract  # noqa: E402
from product_agent_os.methodology_contract import read_methodology_decision  # noqa: E402
from product_agent_os.task_routing import TaskContextError  # noqa: E402


class MethodologyB1Test(unittest.TestCase):
    def setUp(self):
        attempt = tempfile.TemporaryDirectory()
        self.addCleanup(attempt.cleanup)
        self.workspace = Path(attempt.name) / "project"
        self.workspace.mkdir()
        self.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        for name, content in self.fixture["files"].items():
            (self.workspace / name).write_text(content, encoding="utf-8", newline="\n")

    def task(self, case="backend_bug"):
        return copy.deepcopy(self.fixture["cases"][case]["task"])

    def cli(self, *args, script="run_codex_runtime_runner.py"):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPTS / script), str(self.workspace), *args],
            capture_output=True, text=True, encoding="utf-8", timeout=30, check=False,
        )

    def advice(self, task):
        return run_contract(self.workspace, task_context=task)["route_packet"]["methodology_decision"]

    def snapshot(self):
        return {path.relative_to(self.workspace).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in self.workspace.rglob("*") if path.is_file()}

    def test_conflicting_hint_fails_instead_of_merging_two_intents(self):
        with self.assertRaisesRegex(TaskContextError, "task_context:intent_hint_conflict"):
            run_contract(self.workspace, task_context=self.task(), intent_hint="Redesign the dashboard")

    def test_equivalent_hint_and_whitespace_have_one_task_revision(self):
        task = self.task()
        expected = run_contract(self.workspace, task_context=task)["route_packet"]["task_routing"]
        task["intent"] = "  Fix  the counter increment "
        task["acceptance"] = [" increment(3) returns 4 ", "increment(3) returns 4"]
        actual = run_contract(self.workspace, task_context=task, intent_hint="Fix the counter increment")
        self.assertEqual(actual["route_packet"]["task_routing"]["input_digest"], expected["input_digest"])
        self.assertEqual(actual["route_packet"]["task_routing"]["acceptance"], expected["acceptance"])

    def test_profile_keeps_repository_scale_separate_from_task_risk(self):
        from product_agent_os.discovery import analyze_workspace
        from product_agent_os.methodology_profile import describe_project

        bug = self.task()
        audit = analyze_workspace(self.workspace)
        route = run_contract(self.workspace, task_context=bug)["route_packet"]["task_routing"]
        profile = describe_project(audit, bug, route)
        self.assertEqual(profile["lifecycle"], "existing_code_observed")
        self.assertEqual(profile["surface"], "backend")
        self.assertEqual(profile["scale"], "small")
        self.assertEqual(profile["risk"], "low")
        self.assertEqual(profile["check_count"], 1)
        self.assertEqual(profile["environment"], "not_observed")
        bug["risk_level"] = "high"
        high_risk = describe_project(audit, bug, route)
        self.assertEqual(high_risk["scale"], "small")
        self.assertEqual(high_risk["risk"], "high")

    def test_policy_applies_to_changed_surface_and_existing_test_strategy(self):
        from product_agent_os.discovery import analyze_workspace
        from product_agent_os.methodology_policy import select_methodologies
        from product_agent_os.methodology_profile import describe_project

        audit = analyze_workspace(self.workspace)
        for case in ("backend_bug", "docs_only"):
            with self.subTest(case=case):
                task = self.task(case)
                route = run_contract(self.workspace, task_context=task)["route_packet"]["task_routing"]
                profile = describe_project(audit, task, route)
                next_check = self.fixture["cases"][case]["expected"]["step_kind"]
                rows = {row["method"]: row for row in select_methodologies(profile, route, next_check)}
                self.assertEqual(set(rows), {"spec_driven", "design_driven", "tdd", "add", "fsd"})
                self.assertEqual(rows["spec_driven"]["depth"], "compact")
                self.assertEqual(rows["design_driven"]["applicability"], "not_applicable")
                self.assertEqual(rows["fsd"]["applicability"], "not_applicable")
                self.assertEqual(rows["tdd"]["applicability"], "applicable" if case == "backend_bug" else "not_applicable")

    def test_candidate_cli_matches_python_adapter_preserves_audit_and_target(self):
        baseline = json.loads(FIXTURE.with_name("pmeth-b1-baseline.json").read_text(encoding="utf-8"))
        for case, data in self.fixture["cases"].items():
            with self.subTest(case=case):
                name = f"{case}.json"
                (self.workspace / name).write_text(json.dumps(data["task"]), encoding="utf-8")
        before = self.snapshot()
        self.assertEqual(before, baseline["project_file_hashes"])
        for case, data in self.fixture["cases"].items():
            with self.subTest(case=case):
                result = self.cli("--contract", "--task-context", f"{case}.json")
                self.assertEqual(result.returncode, 0, result.stderr)
                route = json.loads(result.stdout)["route_packet"]
                self.assertEqual(route["reporting_scope"], baseline["task_routes"][case]["scope"])
                decision = route["methodology_decision"]
                self.assertEqual(decision, self.advice(data["task"]))
                self.assertEqual(decision["plan"]["next_step"]["kind"], data["expected"]["step_kind"])
                self.assertEqual(decision["plan"]["next_step"]["target"], data["expected"]["target"])
                self.assertIn(f'file:{data["expected"]["source"]}', decision["plan"]["next_step"]["evidence_refs"])
                self.assertEqual(decision["plan"]["gaps"], data["expected"]["gaps"])
                self.assertIsNone(decision["plan"]["blocking_question"])
                self.assertEqual(decision["requirements"]["criteria"][0]["trace"], "proposed")
                self.assertEqual(decision["execution"], "not_started")
                self.assertEqual(decision["acceptance"], "not_evaluated")
        legacy = self.cli("--contract")
        self.assertEqual(legacy.stderr, "")
        legacy_payload = json.loads(legacy.stdout)
        self.assertEqual(legacy_payload["route_packet"]["intake"]["mode"], "legacy_fallback")
        self.assertNotIn("methodology_decision", legacy_payload["route_packet"])
        audit = self.cli("--json", script="run_methodology_audit.py")
        self.assertEqual(audit.returncode, 0, audit.stderr)
        self.assertEqual(len(json.loads(audit.stdout)["methodology_domains"]), baseline["repository_audit"]["domain_count"])
        self.assertEqual(self.snapshot(), before)

    def test_cli_rejects_conflicting_mixed_incomplete_and_writing_requests(self):
        (self.workspace / "task.json").write_text(json.dumps(self.task()), encoding="utf-8")
        before = self.snapshot()
        cases = [
            (["--task-context", "task.json", "--intent-hint", "Redesign UI"], "intent_hint_conflict"),
            (["--task-context", "task.json", "--task", "Fix"], "mixed_inline_and_file"),
            (["--task", "Fix"], "change_mode_invalid"),
            (["--task-context", "task.json", "--output", str(self.workspace / "guide.md")], "read_only_stdout"),
        ]
        for args, error in cases:
            with self.subTest(error=error):
                result = self.cli("--contract", *args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn(error, result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_missing_tests_and_partial_criteria_remain_gaps(self):
        task = self.task()
        (self.workspace / "test_counter.py").unlink()
        packet = self.advice(task)
        self.assertEqual(packet["facts"]["lifecycle"], "legacy_candidate")
        self.assertEqual(packet["plan"]["next_step"]["kind"], "clarify")
        self.assertEqual(packet["decisions"][2]["applicability"], "needs_context")
        self.assertIsInstance(packet["plan"]["blocking_question"], str)
        self.assertEqual(packet["requirements"]["criteria"][0]["trace"], "gap")
        docs = self.task("docs_only")
        docs["acceptance"].append("Another claim needs its own source")
        partial = self.advice(docs)
        self.assertEqual([row["trace"] for row in partial["requirements"]["criteria"]], ["gap", "gap"])
        self.assertIsInstance(partial["plan"]["blocking_question"], str)

    def test_existing_inventory_filters_differ_without_a_second_task_scan(self):
        from product_agent_os.discovery import analyze_workspace
        from product_agent_os.methodology_audit import _relative_inventory

        alternate = self.workspace / ".venv"
        alternate.mkdir()
        (alternate / "pyproject.toml").write_text("[project]\nname='excluded'\n", encoding="utf-8")
        self.assertNotIn(".venv/pyproject.toml", analyze_workspace(self.workspace)["detected_files"])
        files, _directories = _relative_inventory(self.workspace)
        self.assertIn(".venv/pyproject.toml", files)

    def test_full_proposals_keep_invariants_and_greenfield_does_not_scaffold(self):
        task = self.task()
        task["explicit_full_packet"] = True
        full = self.advice(task)
        self.assertEqual(full["requirements"]["depth"], "full")
        self.assertEqual(full["requirements"]["invariants"], ["Increment by exactly one"])
        self.assertEqual(full["requirements"]["criteria"][0]["check"], "plan.next_step")
        (self.workspace / "counter.py").unlink()
        (self.workspace / "test_counter.py").unlink()
        before = self.snapshot()
        task["change_mode"] = "new_behavior"
        proposed = self.advice(task)
        self.assertEqual(proposed["facts"]["lifecycle"], "greenfield_candidate")
        self.assertEqual(proposed["plan"]["next_step"]["kind"], "clarify")
        self.assertEqual(proposed["authority"], "read_only")
        self.assertEqual(self.snapshot(), before)

    def test_verification_refactor_configuration_and_eval_do_not_require_red(self):
        refactor = self.task()
        refactor["change_mode"] = "refactor"
        configuration = {**self.task(), "change_mode": "configuration", "changed_paths": ["pyproject.toml"]}
        (self.workspace / "EVALS.md").write_text("Review deterministic rubric examples discussion.\n", encoding="utf-8")
        subjective = {**self.task(), "evals_required": True, "verification_paths": ["EVALS.md"]}
        for task, expected in (
            (refactor, "run_characterization"),
            (configuration, "check_configuration"),
            (subjective, "review_evaluation"),
        ):
            with self.subTest(expected=expected):
                packet = self.advice(task)
                self.assertEqual(packet["plan"]["next_step"]["kind"], expected)
                self.assertEqual(packet["decisions"][2]["applicability"], "not_applicable")

    def test_decision_is_revision_bound_and_rejects_forged_or_malformed_claims(self):
        task = self.task()
        packet = self.advice(task)
        scope = packet["scope"]
        self.assertEqual(read_methodology_decision(json.loads(json.dumps(packet)), scope), packet)
        for key in scope:
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "scope_mismatch"):
                read_methodology_decision(packet, {**scope, key: "mismatched"})
        variants = [
            ({"schema_version": "paos_methodology_decision_v2"}, "unsupported_version"),
            ({"execution": "passed"}, "invalid_projection"),
            ({"acceptance": "verified"}, "invalid_projection"),
            ({"evidence": []}, "invalid_evidence"),
            ({"decisions": [{}]}, "invalid_projection"),
        ]
        for patch, error in variants:
            with self.subTest(patch=patch), self.assertRaisesRegex(ValueError, error):
                read_methodology_decision({**packet, **patch}, scope)
        broken = copy.deepcopy(packet)
        broken["plan"]["next_step"]["evidence_refs"] = ["file:unrelated.py"]
        with self.assertRaisesRegex(ValueError, "invalid_projection"):
            read_methodology_decision(broken, scope)
        (self.workspace / "counter.py").write_text("def increment(value):\n    return value + 1\n", encoding="utf-8")
        current = self.advice(task)
        self.assertNotEqual(current["scope"]["source_revision"], scope["source_revision"])
        self.assertEqual(current["scope"]["task_revision"], scope["task_revision"])
        with self.assertRaisesRegex(ValueError, "scope_mismatch"):
            read_methodology_decision(packet, current["scope"])
        route = run_contract(self.workspace, task_context=task)["route_packet"]["task_routing"]
        task["check_results"] = [{"command": route["checks"][0]["command"], "input_digest": "0"*64,
                                  "status": "passed", "exit_code": 0}]
        stale = self.advice(task)
        self.assertTrue(any("Stale verification receipt" in gap for gap in stale["plan"]["gaps"]))
        self.assertEqual(stale["acceptance"], "not_evaluated")

    def test_runtime_regression_has_intended_red_minimal_green_and_distinct_setup_failure(self):
        target = self.fixture["cases"]["backend_bug"]["expected"]
        selected = self.advice(self.task())["plan"]["next_step"]["target"]
        self.assertEqual(selected, target["target"])
        args = [sys.executable, *shlex.split(selected)[1:]]

        def run_check():
            return subprocess.run(args, cwd=self.workspace, capture_output=True, text=True,
                                  encoding="utf-8", timeout=15, check=False)

        before = self.snapshot()
        red = run_check()
        self.assertEqual(red.returncode, 1)
        self.assertIn(target["red"], red.stderr)
        self.assertIn("FAIL: test_increment_by_one", red.stderr)
        self.assertNotIn("ImportError", red.stderr)
        self.assertEqual(self.snapshot(), before)
        counter = self.workspace / "counter.py"
        counter.write_text(self.fixture["files"]["counter.py"].replace("+ 2", "+ 1"),
                           encoding="utf-8", newline="\n")
        fixed = self.snapshot()
        self.assertEqual([name for name in fixed if fixed[name] != before[name]], ["counter.py"])
        green = run_check()
        self.assertEqual(green.returncode, 0, green.stderr)
        self.assertIn("Ran 1 test", green.stderr)
        self.assertEqual(self.snapshot(), fixed)
        counter.rename(self.workspace / "counter-moved.py")
        setup = run_check()
        self.assertNotEqual(setup.returncode, 0)
        self.assertIn("ModuleNotFoundError", setup.stderr)
        self.assertNotIn(target["red"], setup.stderr)
