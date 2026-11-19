"""Synthetic verification of the scoped methodology runner."""

import json
import subprocess
import sys
import unittest

from tests.product_agent_os import test_pmeth_b1


class MethodologyB4Test(unittest.TestCase):
    setUp = test_pmeth_b1.MethodologyB1Test.setUp
    task = test_pmeth_b1.MethodologyB1Test.task
    snapshot = test_pmeth_b1.MethodologyB1Test.snapshot

    def scoped_route(self, task, previous=None):
        from codex_runtime_runner.cli import run_contract

        kwargs = {} if previous is None else {"previous_methodology_context": previous}
        return run_contract(self.workspace, task_context=task, **kwargs)["route_packet"]

    def test_unchanged_context_can_be_compared_without_writing(self):
        task = self.task()
        before = self.snapshot()
        first = self.scoped_route(task)["methodology_context"]
        second = self.scoped_route(task, first["snapshot"])["methodology_context"]
        self.assertEqual(second["impact"]["status"], "unchanged")
        self.assertEqual(second["snapshot"], first["snapshot"])
        self.assertEqual(self.snapshot(), before)

    def test_changed_acceptance_and_overlapping_owner_edit_require_review(self):
        task = self.task()
        first = self.scoped_route(task)["methodology_context"]["snapshot"]
        task["acceptance"][0] = "increment(3) returns 5"
        owner_file = self.workspace / "TEST.md"
        owner_file.write_text(owner_file.read_text(encoding="utf-8") + "\n# Other owner's edits\n", encoding="utf-8")
        before = self.snapshot()
        route = self.scoped_route(task, first)
        impact = route["methodology_context"]["impact"]
        self.assertEqual(impact["status"], "review_required")
        self.assertIn("AC-1", impact["changed_criteria"])
        self.assertIn("TEST.md", impact["owner_review_paths"])
        self.assertEqual(impact["previous_evidence"], "stale")
        self.assertEqual(route["methodology_decision"]["acceptance"], "not_evaluated")
        self.assertEqual(self.snapshot(), before)

    def test_identical_bytes_at_a_new_path_are_a_rename_candidate_only(self):
        task = self.task()
        first = self.scoped_route(task)["methodology_context"]["snapshot"]
        (self.workspace / "counter.py").rename(self.workspace / "moved.py")
        task["changed_paths"] = ["moved.py"]
        before = self.snapshot()
        impact = self.scoped_route(task, first)["methodology_context"]["impact"]
        self.assertEqual(impact["rename_candidates"], [{"from": "counter.py", "to": "moved.py"}])
        self.assertEqual(impact["semantic_coverage"], "not_established")
        self.assertEqual(self.snapshot(), before)

    def test_foreign_context_fails_closed(self):
        from product_agent_os.task_routing import TaskContextError

        task = self.task()
        snapshot = self.scoped_route(task)["methodology_context"]["snapshot"]
        with self.assertRaisesRegex(TaskContextError, "methodology_context:scope_mismatch"):
            self.scoped_route({**task, "task_id": "different"}, snapshot)

    def test_cli_compares_a_missing_requirements_owner_and_keeps_legacy_route(self):
        task = self.task()
        (self.workspace / "task.json").write_text(json.dumps(task), encoding="utf-8")
        owner = self.workspace / "REQUIREMENTS.md"
        owner.write_text("# Requirements\n", encoding="utf-8")
        snapshot = self.scoped_route(task)["methodology_context"]["snapshot"]
        owner.rename(self.workspace / "requirements-proposal.md")
        before = self.snapshot()
        result = subprocess.run(
            [sys.executable, "-B", str(test_pmeth_b1.SCRIPTS / "run_codex_runtime_runner.py"),
             str(self.workspace), "--contract", "--task-context", "task.json", "--compare-methodology-context"],
            input=json.dumps(snapshot), capture_output=True, text=True, encoding="utf-8", timeout=30, check=False,
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "needs_context")
        self.assertEqual(payload["route_packet"]["methodology_context"]["impact"]["missing_owner_paths"],
                         ["REQUIREMENTS.md"])
        self.assertEqual(self.snapshot(), before)

    def test_scoped_runner_keeps_ordinary_assignment_read_only_and_serial(self):
        route = self.scoped_route(self.task())
        assignment = route["methodology_execution"]
        self.assertEqual(assignment["format"], "concise")
        self.assertEqual(assignment["scope"], route["methodology_decision"]["scope"])
        self.assertEqual(assignment["planned_paths"], ["counter.py"])
        self.assertEqual(assignment["allowed_writes"], [])
        self.assertEqual(assignment["parallelism"], "serial")
        self.assertEqual(assignment["runtime_policy"], "inherited")

    def test_missing_host_skill_exposure_keeps_routes_as_manual_proposals(self):
        route = self.scoped_route(self.task())
        capabilities = route["methodology_execution"]["capabilities"]
        self.assertEqual({row["method"] for row in capabilities}, {"spec_driven", "tdd", "add"})
        tdd = next(row for row in capabilities if row["method"] == "tdd")
        self.assertEqual(tdd["skill"], "test-eval-designer")
        self.assertEqual(tdd["availability"], "packaged")
        self.assertIsNone(tdd["exposed"])
        self.assertFalse(tdd["invoked"])
        self.assertEqual(tdd["next_action"], "Review the source-backed check with the task owner")

    def test_timeout_and_stale_handoff_have_distinct_dispositions(self):
        from codex_runtime_runner.cli import run_contract

        task = self.task()
        assignment = self.scoped_route(task)["methodology_execution"]
        handoff = {"scope": assignment["scope"], "input_digest": assignment["input_digest"],
                   "status": "timeout", "evidence_refs": []}
        for digest, expected in ((assignment["input_digest"], "timeout"), ("0" * 64, "stale_handoff")):
            with self.subTest(status=expected):
                result = run_contract(self.workspace, allow_subagents=True, task_context=task,
                                      methodology_handoff={**handoff, "input_digest": digest})
                current = result["route_packet"]["methodology_execution"]
                self.assertEqual(current["handoff_review"]["status"], expected)
                self.assertEqual(current["delegation_gap"], "HOST_PARALLEL_CAPABILITY_UNOBSERVED")
                self.assertEqual(current["retry_limit"], 0)
                self.assertEqual(result["status"], "needs_context")

    def test_explicit_delivery_plan_reuses_owner_and_has_only_relevant_prerequisites(self):
        from codex_runtime_runner.cli import run_contract

        (self.workspace / "requirements.md").write_text("# Requirements owner\n", encoding="utf-8")
        task = self.task()
        before = self.snapshot()
        route = run_contract(self.workspace, task_context=task, include_delivery_plan=True)["route_packet"]
        plan = route["methodology_delivery_plan"]
        self.assertEqual(plan["authority"], "read_only")
        self.assertEqual(plan["artifacts"]["REQUIREMENTS.md"]["path"], "requirements.md")
        self.assertEqual({row["id"] for row in plan["slices"]}, {"specification", "red", "implementation", "verification"})
        self.assertEqual(plan["slices"][2]["depends_on"], ["red"])
        self.assertNotIn("methodology_delivery_plan", self.scoped_route(task))
        self.assertEqual(self.snapshot(), before)

    def test_formation_apply_rejects_changed_behavior_file_even_with_reviewed_approval(self):
        from product_agent_os.merge_infrastructure import MergeInfrastructureError, apply_merge_plan
        from tests.product_agent_os.test_project_formation import approve, stage_request

        stage = self.workspace.parent / "stage"
        task = {**self.task(), "explicit_full_packet": True}
        stage_request(self.workspace, stage, {"schema_version": 1, "task": task, "domains": []})
        approval = approve(self.workspace, stage)
        source = self.workspace / "counter.py"
        source.write_text(source.read_text(encoding="utf-8").replace("+ 2", "+ 3"), encoding="utf-8")
        before = self.snapshot()
        with self.assertRaisesRegex(MergeInfrastructureError, "task inputs changed"):
            apply_merge_plan(self.workspace, stage, approval)
        self.assertEqual(self.snapshot(), before)

    def test_formation_preserves_file_created_by_another_writer_during_publish(self):
        import os
        from pathlib import Path
        from unittest.mock import patch

        from product_agent_os.merge_infrastructure import MergeInfrastructureError, apply_merge_plan
        from tests.product_agent_os.test_project_formation import approve, stage_request

        stage = self.workspace.parent / "stage"
        task = {**self.task(), "explicit_full_packet": True}
        stage_request(self.workspace, stage, {"schema_version": 1, "task": task, "domains": []})
        approval = approve(self.workspace, stage)
        raced = []
        action = "rename" if os.name == "nt" else "link"
        publish = getattr(os, action)

        def concurrent_create(temp, target):
            path = Path(target)
            path.write_bytes(b"user edited this document\r\n")
            raced.append(path)
            return publish(temp, path)

        with patch(f"product_agent_os.merge_infrastructure.os.{action}", side_effect=concurrent_create):
            with self.assertRaisesRegex(MergeInfrastructureError, "target appeared"):
                apply_merge_plan(self.workspace, stage, approval)
        self.assertEqual(len(raced), 1)
        self.assertEqual(raced[0].read_bytes(), b"user edited this document\r\n")
        self.assertTrue((stage / "product-agent-os-rollback-manifest.json").is_file())

    def test_cli_criterion_projection_never_promotes_a_caller_pass(self):
        task = self.task()
        route = self.scoped_route(task)
        task["check_results"] = [{"command": route["methodology_decision"]["plan"]["next_step"]["target"],
                                  "input_digest": route["task_routing"]["input_digest"], "status": "passed", "exit_code": 0}]
        row = self.scoped_route(task)["methodology_criterion_evidence"]["criteria"][0]
        self.assertEqual(row["technical"], "not_evaluated")
        self.assertEqual(row["caller_observations"][0]["freshness"], "current")
        self.assertEqual(row["caller_observations"][0]["provenance"], "caller_reported_not_independently_verified")
