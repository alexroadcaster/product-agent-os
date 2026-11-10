import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
WRAPPER = SCRIPTS / "run_codex_runtime_runner.py"
VALIDATOR = SCRIPTS / "validate_codex_runtime_runner.py"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner import cli as runtime_cli  # noqa: E402
from codex_runtime_runner.contracts import build_result  # noqa: E402
from codex_runtime_runner.contracts import validate_runner_result  # noqa: E402
from codex_runtime_runner.guards import validate_route_packet  # noqa: E402


class CodexRuntimeRunnerCliTest(unittest.TestCase):
    def test_inline_intake_routes_both_languages_without_builder_or_task_file(self):
        import contextlib
        import io
        from render_infrastructure import main as render_main
        for intent in ("Correct a typo", "Исправить опечатку"):
            with self.subTest(intent=intent), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / "project"
                root.mkdir()
                (root / "AGENTS.md").write_text("Follow local instructions.", encoding="utf-8")
                (root / "README.md").write_text("Text", encoding="utf-8")
                (root / "TEST.md").write_text("`python check_docs.py`", encoding="utf-8")
                before = {p.name: p.read_bytes() for p in root.iterdir()}
                intake = ["--task", intent, "--change-mode", "docs_only", "--changed-path", "README.md",
                          "--acceptance", "Correct wording", "--risk-level", "low"]
                stream = io.StringIO()
                with contextlib.redirect_stdout(stream):
                    code = runtime_cli.main([str(root), "--contract", *intake])
                result = json.loads(stream.getvalue())
                self.assertEqual(code, 0, result)
                self.assertEqual(result["route_packet"]["task_routing"]["mode"], "ordinary")
                self.assertEqual(result["route_packet"]["intake"]["mode"], "explicit_task_context")
                stream = io.StringIO()
                with contextlib.redirect_stdout(stream):
                    code = render_main([str(root), "--stage", str(Path(tmp) / "stage"), *intake])
                staged = json.loads(stream.getvalue())
                self.assertEqual(code, 0)
                self.assertEqual(staged["rendered_artifacts"]["files"], [])
                self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})

    def test_inline_intake_rejects_partial_mixed_and_escaping_inputs(self):
        from product_agent_os.task_routing import add_task_intake_arguments, task_context_from_args, TaskContextError
        import argparse
        parser = argparse.ArgumentParser()
        add_task_intake_arguments(parser)
        with tempfile.TemporaryDirectory() as tmp:
            for args in (["--task", "Fix"], ["--changed-path", "README.md"], ["--task-context", ""],
                         ["--task-context", "task.json", "--task", "Fix"],
                         ["--task", "Fix", "--change-mode", "docs_only", "--changed-path", "../outside.md", "--acceptance", "Fixed"]):
                with self.subTest(args=args), self.assertRaises(TaskContextError):
                    task_context_from_args(tmp, parser.parse_args(args))
            args = parser.parse_args(["--task", "Fix", "--change-mode", "docs_only", "--changed-path", "README.md", "--acceptance", "Fixed"])
            self.assertEqual(task_context_from_args(tmp, args)["risk_level"], "unknown")

    def test_legacy_callers_expose_fallback_without_changing_default(self):
        from product_agent_os.infrastructure import render_infrastructure_plan
        from product_agent_os.templates import required_templates
        with tempfile.TemporaryDirectory() as tmp:
            result = runtime_cli.run_contract(tmp)
            self.assertEqual(result["route_packet"]["intake"]["mode"], "legacy_fallback")
            rendered = render_infrastructure_plan(tmp)
            self.assertEqual(rendered["infrastructure_plan"]["intake"]["mode"], "legacy_fallback")
            self.assertEqual(len(rendered["rendered_artifacts"]["files"]), len(required_templates()))

    def test_contract_cli_does_not_infer_quality_gate_from_runlog_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: quality_gate")
            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--contract"],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(payload["status"], "route_ready")
        self.assertEqual(payload["lifecycle_state"], "maintenance")
        self.assertNotEqual(payload["route_packet"]["recommended_skill"], "risk-reviewer")
        self.assertEqual(payload["workspace"], "[REDACTED_LOCAL_PATH]")
        self.assertNotIn(str(workspace), result.stdout)

    def test_contract_cli_requires_contract_flag(self):
        result = subprocess.run(
            [sys.executable, str(WRAPPER), "."],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("choose --contract", result.stderr)

    def test_contract_cli_includes_first_run_usage_mode_for_empty_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            (workspace / "README.md").write_text("# Idea\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--contract"],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "route_ready")
        self.assertEqual(payload["lifecycle_state"], "uninitialized")
        self.assertEqual(payload["route_packet"]["usage_mode"]["primary"], "greenfield_idea")
        self.assertEqual(payload["route_packet"]["first_response_contract"]["mode"], "greenfield_idea")
        self.assertIn("greenfield idea brief", payload["route_packet"]["first_response_contract"]["minimum_artifacts"])
        self.assertIn("minimum artifacts", payload["route_packet"]["first_response_contract"]["required_fields"])
        self.assertIn("evidence gaps", payload["route_packet"]["first_response_contract"]["required_fields"])
        self.assertIn(
            "first-run-empty-greenfield",
            payload["route_packet"]["usage_mode"]["behavioral_eval_cases"],
        )

    def test_contract_cli_returns_needs_approval_for_build_active_without_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: build_active")
            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--contract", "--allow-subagents",
                 "--requested-state", "build_active"],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload["status"], "needs_approval")
        self.assertEqual(payload["route_packet"]["write_policy"], "approved_write")

    def test_contract_cli_blocks_source_policy_blocked_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: quality_gate")
            docs = workspace / "docs"
            docs.mkdir()
            (docs / "guide.md").write_text("# Guide\n\nOpenAI Codex behavior claim.\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--contract"],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["source_policy_status"], "blocked")
        self.assertIn("source_policy:blocked", payload["errors"])

    def test_contract_cli_intent_hint_does_not_bypass_source_policy_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: quality_gate")
            docs = workspace / "docs"
            docs.mkdir()
            (docs / "guide.md").write_text("# Guide\n\nOpenAI Codex behavior claim.\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(WRAPPER),
                    str(workspace),
                    "--contract",
                    "--intent-hint",
                    "release this package now",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["source_policy_status"], "blocked")
        self.assertEqual(payload["route_packet"]["usage_mode"]["primary"], "release_packaging")
        self.assertTrue(payload["route_packet"]["behavioral_route_inputs"]["intent_hint_present"])
        self.assertIn("source_policy:blocked", payload["errors"])

    def test_validator_accepts_valid_result_json_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: quality_gate")
            output = Path(tmp) / "result.json"
            run_result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--contract", "--output", str(output)],
                check=False,
                capture_output=True,
                text=True,
            )
            validate_result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(output)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(run_result.returncode, 0)
        self.assertEqual(validate_result.returncode, 0, validate_result.stdout + validate_result.stderr)
        self.assertIn('"ok": true', validate_result.stdout)

    def test_cli_stdout_and_output_include_redacted_methodology_packet_and_finish_options(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            self._write_control_plane(workspace, "lifecycle_state: quality_gate")
            src = workspace / "src"
            src.mkdir()
            (src / "payment_api.py").write_text("def charge(): pass\n", encoding="utf-8")
            output = Path(tmp) / "result.json"
            run_result = subprocess.run(
                [
                    sys.executable,
                    str(WRAPPER),
                    str(workspace),
                    "--contract",
                    "--intent-hint",
                    "security-sensitive payment release",
                    "--output",
                    str(output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            validate_result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(output)],
                check=False,
                capture_output=True,
                text=True,
            )
            file_payload = json.loads(output.read_text(encoding="utf-8"))

        stdout_payload = json.loads(run_result.stdout)
        route = stdout_payload["route_packet"]

        self.assertEqual(run_result.returncode, 1, run_result.stdout + run_result.stderr)
        self.assertEqual(validate_result.returncode, 0, validate_result.stdout + validate_result.stderr)
        self.assertEqual(stdout_payload, file_payload)
        self.assertEqual(stdout_payload["schema_version"], 1)
        self.assertEqual(stdout_payload["status"], "needs_approval")
        self.assertIn("methodology_packet", route)
        self.assertIn("finish_options", route)
        self.assertIn("request_approval", route["finish_options"])
        self.assertIn("first_response_contract", route)
        self.assertIn("question_queue", route)
        self.assertIn("next_blocking_question", route["first_response_contract"])
        self.assertIn("question_counts", route["first_response_contract"])
        self.assertIn("question_summary", route["first_response_contract"])
        self.assertNotIn("owner_questions", route["first_response_contract"])
        self.assertNotIn("questions", route["first_response_contract"])
        self.assertIn("safe_next_action", route["first_response_contract"])
        self.assertNotIn(str(workspace), run_result.stdout)

    def test_contract_run_redacts_methodology_route_payload_before_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: quality_gate")
            audit = self._audit(
                methodology_intelligence=self._methodology_intelligence(
                    safe_next_action="TOKEN=fixture-secret\nInspect C:\\Users\\person\\project\nraw private chat log",
                    question="Can C:\\Users\\person\\project be inspected?",
                )
            )
            with patch.object(runtime_cli, "analyze_workspace", return_value=audit):
                payload = runtime_cli.run_contract(workspace)

        text = json.dumps(payload, sort_keys=True)
        self.assertNotIn("fixture-secret", text)
        self.assertNotIn("C:\\Users\\person", text)
        self.assertNotIn("raw private chat log", text)
        self.assertIn("secret", payload["redactions"]["categories"])
        self.assertNotIn("redaction:secret_retained", payload["errors"])

    def test_validator_rejects_malformed_methodology_packet_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "result.json"
            payload = build_result(
                status="route_ready",
                workspace="C:/workspace/synthetic",
                lifecycle_state="quality_gate",
                route_packet={
                    "write_policy": "read_only",
                    "methodology_packet": {"write_policy": "staged_only"},
                },
                source_policy_status="ok",
                approval_status="not_required",
                next_action="Run risk-reviewer.",
            )
            output.write_text(json.dumps(payload), encoding="utf-8")
            validate_result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(output)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(validate_result.returncode, 1)
        self.assertIn("methodology_packet.safe_next_action:required", validate_result.stdout)
        self.assertNotIn("Traceback", validate_result.stdout + validate_result.stderr)

    def _write_control_plane(self, workspace: Path, runlog_marker: str) -> None:
        (workspace / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
        (workspace / "REQUIREMENTS.md").write_text(
            "# Requirements\n\n## Acceptance Criteria\n\n- Synthetic.\n",
            encoding="utf-8",
        )
        (workspace / "PLAN.md").write_text("# Plan\n\n## Verification\n\n- Run tests.\n", encoding="utf-8")
        (workspace / "TEST.md").write_text("# Test\n\nQuality gates: unit tests.\n", encoding="utf-8")
        (workspace / "EVALS.md").write_text("# Evals\n\nQuality gates: fixture eval.\n", encoding="utf-8")
        (workspace / "RUNLOG.md").write_text(f"# Runlog\n\n{runlog_marker}\n", encoding="utf-8")
        agents = workspace / ".codex" / "agents"
        agents.mkdir(parents=True)
        (agents / "builder.toml").write_text('name = "builder"\n', encoding="utf-8")

    def _audit(self, *, methodology_intelligence: dict):
        return {
            "usage_mode": {
                "primary": "maintenance",
                "secondary": [],
                "confidence": "medium",
                "reasons": ["synthetic patched audit"],
                "fallback": "standard_feature",
                "first_response_contract": [
                    "mode",
                    "confidence",
                    "next smallest action",
                    "minimum artifacts",
                    "evidence gaps",
                    "approval boundary",
                ],
                "minimum_artifacts": ["workspace audit packet"],
                "behavioral_eval_cases": ["route-selection"],
            },
            "route_inputs": {
                "intent_hint_present": False,
                "workspace_signals": {
                    "stack": [],
                    "active_surfaces": [],
                    "methodology_signals": [],
                },
                "control_plane_state": {
                    "existing_control_plane_files": [],
                    "has_codex_assets": False,
                },
            },
            "methodology_intelligence": methodology_intelligence,
        }

    def _methodology_intelligence(self, *, safe_next_action: str, question: str = "Who owns the decision?"):
        return {
            "status": "present_unverified",
            "write_policy": "read_only",
            "methodology_domains": [{"id": "security", "status": "applicable_missing"}],
            "recommendations": [
                {
                    "domain": "security",
                    "artifact": "security-risk-review.md",
                    "priority": "P1_high_risk",
                    "safe_next_action": safe_next_action,
                }
            ],
            "recommendation_groups": [
                {
                    "artifact": "security-risk-review.md",
                    "owner_domain": "security",
                    "consumer_domains": ["quality_testing_evals"],
                    "priority": "P1_high_risk",
                    "safe_next_action": safe_next_action,
                }
            ],
            "questions_for_owner": [question],
            "methodology_synthesis": {
                "safe_next_action": safe_next_action,
                "semantic_evidence_sufficiency": {"status": "present_unverified"},
                "source_artifact_ledger": [
                    {"artifact": "security-risk-review.md", "decision": "canonical_template"}
                ],
            },
        }


class OrdinaryRouteCliTest(unittest.TestCase):
    """Exercise the public opt-in path, without granting target write authority."""

    def test_g7_route_reuses_inventory_and_invalidates_lockfile_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            context = self._workspace(root)
            context['change_mode'] = 'refactor'
            (root / 'uv.lock').write_text('version = 1\n', encoding='utf-8')
            first = json.loads(self._cli(root, context).stdout)['route_packet']
            self.assertEqual(first['quality_strategy']['test_first_decision']['status'], 'not_applicable')
            summary = first['code_change_contract']['existing_capability']
            self.assertIsInstance(summary, dict)
            self.assertEqual(summary['reference_coverage'], 'unknown')
            self.assertTrue(summary['candidates'])
            self.assertEqual(len(first['code_change_contract']), 8)
            digest = first['task_routing']['input_digest']
            (root / 'uv.lock').write_text('version = 2\n', encoding='utf-8')
            second = json.loads(self._cli(root, context).stdout)['route_packet']
            self.assertNotEqual(digest, second['task_routing']['input_digest'])
            self.assertEqual(first['verification'], second['verification'])


    def _workspace(self, root, *, language="en"):
        (root / "AGENTS.md").write_text("# Rules\nPreserve existing behavior.\n", encoding="utf-8")
        (root / "pyproject.toml").write_text('[project]\nname = "sample"\nversion = "0.1.0"\n', encoding="utf-8")
        (root / "calc.py").write_text("def total(a, b):\n    return a - b\n", encoding="utf-8")
        (root / "TEST.md").write_text(
            ("# Проверки" if language == "ru" else "# Checks")
            + "\n```sh\npython -m unittest test_calc -v\n```\n", encoding="utf-8",
        )
        return {
            "schema_version": 1, "task_id": "ordinary-fix", "intent": "Fix addition",
            "change_mode": "defect_fix", "changed_paths": ["calc.py"], "risk_level": "low",
            "acceptance": ["total(2, 3) equals 5"],
            "risks": [{"risk_id": "sum", "kind": "pure_logic", "description": "Addition regression",
                       "protected_invariants": ["addition"], "languages": ["python"]}],
            "executable_test_seam": True, "test_seam_reason": "test_calc regression",
            "checks": [{"command": "python -m unittest test_calc -v", "source": "TEST.md",
                        "test_kinds": ["unit"]}],
        }

    def _cli(self, root, context):
        (root / "task.json").write_text(json.dumps(context), encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-B", str(WRAPPER), str(root), "--contract", "--task-context", "task.json"],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )

    def test_ordinary_cli_selects_existing_helpers_without_full_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            context = self._workspace(root)
            result = self._cli(root, context)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        route = payload["route_packet"]
        self.assertEqual(payload["status"], "route_ready")
        self.assertEqual(route["routing_trace"]["mode"], "ordinary")
        self.assertFalse(route["routing_trace"]["legacy_fallback_used"])
        self.assertEqual(route["routing_trace"]["selectors"],
                         ["select_code_quality_profile", "select_test_strategy"])
        self.assertNotIn("EVALS.md", route["required_inputs"])
        self.assertEqual(route["verification"], ["python -m unittest test_calc -v"])
        self.assertEqual(len(route["code_change_contract"]), 8)
        self.assertEqual(payload["files_touched"], [])

    def test_ru_and_en_single_agent_have_identical_route_decisions(self):
        decisions = []
        for language in ("ru", "en"):
            with self.subTest(language=language), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                result = self._cli(root, self._workspace(root, language=language))
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                route = json.loads(result.stdout)["route_packet"]
                decisions.append((route["routing_trace"]["mode"], route["verification"], route["required_inputs"]))
        self.assertEqual(len(decisions), 2)
        self.assertEqual(decisions[0], decisions[1])

    def test_docs_only_and_no_op_do_not_force_behavior_tests(self):
        for mode in ("docs_only", "no_op"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                context = self._workspace(root)
                (root / "README.md").write_text("# Wording\n", encoding="utf-8")
                context.update(change_mode=mode, changed_paths=["README.md"] if mode == "docs_only" else [],
                               risks=[], checks=[], intent="Review wording" if mode == "docs_only" else "Reuse existing result")
                result = self._cli(root, context)
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                route = json.loads(result.stdout)["route_packet"]
                # Explicit project instructions still win, even for docs/no-op.
                self.assertEqual(route["verification"], ["python -m unittest test_calc -v"])
                if mode == "docs_only":
                    self.assertEqual(route["code_change_contract"], {})
                    self.assertEqual(route["quality_strategy"]["status"], "not_applicable")
                else:
                    self.assertTrue(all(d["status"] == "not_applicable" for d in route["quality_strategy"]["test_decisions"]))

    def test_high_risk_and_explicit_full_context_retain_full_gates(self):
        for extra in ({"risk_level": "high"}, {"financially_material": True},
                      {"explicit_full_packet": True}, {"changed_paths": ["auth.py"]}):
            with self.subTest(extra=extra), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                context = self._workspace(root)
                context.update(extra)
                context["risks"][0]["kind"] = "high_risk_rule"
                context["checks"][0]["test_kinds"] = ["mutation"]
                result = self._cli(root, context)
                payload = json.loads(result.stdout)
                route = payload["route_packet"]
                self.assertEqual(payload["status"], "needs_context")  # full control plane is missing
                self.assertEqual(route["routing_trace"]["mode"], "full")
                self.assertEqual(route["reporting_scope"], "full")
                self.assertIn("EVALS.md", route["required_inputs"])
                self.assertTrue(any(d["test_kind"] == "mutation" and d["status"] == "required"
                                    for d in route["quality_strategy"]["test_decisions"]))

    def test_sensitive_windows_paths_cannot_select_ordinary(self):
        for name in (r".codex\config.toml", r"src\auth.py", "./.github/workflows/check.yml"):
            with self.subTest(path=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                context = self._workspace(root)
                context["changed_paths"] = [name]
                payload = json.loads(self._cli(root, context).stdout)
                self.assertEqual(payload["route_packet"]["routing_trace"]["mode"], "full")
                self.assertIn("sensitive_changed_path", payload["route_packet"]["task_routing"]["full_reasons"])
                self.assertEqual(payload["status"], "needs_context")

    def test_reuse_configuration_and_deletion_keep_invariant_checks(self):
        for mode in ("reuse", "configuration", "deletion"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                context = self._workspace(root)
                context["change_mode"] = mode
                payload = json.loads(self._cli(root, context).stdout)
                self.assertEqual(payload["status"], "route_ready")
                self.assertEqual(payload["route_packet"]["task_routing"]["change_mode"], mode)
                self.assertEqual(payload["route_packet"]["code_change_contract"]["invariants"], ["addition"])
                self.assertEqual(payload["files_touched"], [])

    def test_unknown_risk_and_missing_check_are_explicit_gaps(self):
        for missing in ("risk", "check"):
            with self.subTest(missing=missing), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                context = self._workspace(root)
                if missing == "risk":
                    context["risk_level"] = "unknown"
                else:
                    context["checks"] = []
                    (root / "TEST.md").write_text("# Checks not yet selected\n", encoding="utf-8")
                result = self._cli(root, context)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["status"], "needs_context")
                self.assertTrue(payload["route_packet"]["task_routing"]["gaps"])

    def test_malformed_context_never_falls_back_or_grants_authority(self):
        variants = [
            {"schema_version": 2}, {"schema_version": True}, {"approval_status": "approved"},
            {"changed_paths": ["../outside.py"]}, {"changed_paths": ["C:outside.py"]},
            {"change_mode": []}, {"risk_level": {}}, {"risks": [{"kind": "pure_logic"}]},
            {"financially_material": "false"}, {"change_mode": "docs_only"},
        ]
        for extra in variants:
            with self.subTest(extra=extra), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                context = self._workspace(root)
                context.update(extra)
                result = self._cli(root, context)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("task_context:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_bound_task_state_requires_matching_id_hash_and_lifecycle_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            context = self._workspace(root)
            raw = json.dumps({"task_id": context["task_id"], "lifecycle_state": "build_active"}).encode()
            (root / "state.json").write_bytes(raw)
            context["state"] = {"value": "build_active", "source": "state.json", "sha256": hashlib.sha256(raw).hexdigest()}
            payload = json.loads(self._cli(root, context).stdout)
            self.assertEqual(payload["status"], "needs_approval")
            self.assertEqual(payload["route_packet"]["write_policy"], "approved_write")
            (root / "state.json").write_text('{"task_id":"other","lifecycle_state":"release_ready"}', encoding="utf-8")
            stale = json.loads(self._cli(root, context).stdout)
            self.assertEqual(stale["status"], "needs_context")
            self.assertIsNone(stale["route_packet"]["routing_trace"]["state_resolution"]["task_state"])

    def test_unsafe_command_and_source_policy_do_not_allow_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            context = self._workspace(root)
            unsafe = "python -m unittest test_calc; echo unsafe"
            (root / "TEST.md").write_text(unsafe, encoding="utf-8")
            context["checks"][0]["command"] = unsafe
            payload = json.loads(self._cli(root, context).stdout)
            self.assertIn(payload["status"], {"blocked", "needs_context"})
            self.assertEqual(payload["route_packet"]["verification"], [])
            self.assertEqual(payload["route_packet"]["verification_plan"][0]["status"], "blocked")
            context = self._workspace(root)
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("# Guide\nOpenAI Codex behavior claim.\n", encoding="utf-8")
            payload = json.loads(self._cli(root, context).stdout)
            self.assertEqual(payload["status"], "blocked")
            self.assertIn("source_policy:blocked", payload["errors"])

    def test_actual_regression_journey_and_stale_receipt_never_claim_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            context = self._workspace(root)
            (root / "test_calc.py").write_text(
                "import unittest\nfrom calc import total\nclass SumTest(unittest.TestCase):\n"
                "    def test_addition(self):\n        self.assertEqual(total(2, 3), 5)\n", encoding="utf-8",
            )
            before = json.loads(self._cli(root, context).stdout)
            command = before["route_packet"]["verification"][0]
            self.assertEqual(command, "python -m unittest test_calc -v")
            # Execute only this test-owned known command, not arbitrary route text.
            argv = [sys.executable, "-B", "-m", "unittest", "test_calc", "-v"]
            red = subprocess.run(argv, cwd=root, capture_output=True, text=True)
            self.assertNotEqual(red.returncode, 0)
            self.assertIn("AssertionError", red.stderr)
            (root / "calc.py").write_text("def total(a, b):\n    return a + b\n", encoding="utf-8")
            green = subprocess.run(argv, cwd=root, capture_output=True, text=True)
            self.assertEqual(green.returncode, 0, green.stderr)
            current = json.loads(self._cli(root, context).stdout)
            digest = current["route_packet"]["task_routing"]["input_digest"]
            self.assertNotEqual(digest, before["route_packet"]["task_routing"]["input_digest"])
            context["check_results"] = [{"command": command, "input_digest": digest,
                                          "status": "passed", "exit_code": green.returncode}]
            verified = json.loads(self._cli(root, context).stdout)
            self.assertEqual(verified["status"], "route_ready")
            receipt = verified["route_packet"]["task_routing"]["check_observations"][0]
            self.assertEqual(receipt["freshness"], "current")
            self.assertEqual(receipt["provenance"], "caller_reported_not_independently_verified")
            (root / "calc.py").write_text("def total(a, b):\n    return 0\n", encoding="utf-8")
            stale = json.loads(self._cli(root, context).stdout)
            self.assertEqual(stale["status"], "needs_context")
            self.assertEqual(stale["route_packet"]["task_routing"]["check_observations"][0]["freshness"], "stale")

    def test_route_contract_rejects_forged_fallback_and_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = json.loads(self._cli(root, self._workspace(root)).stdout)
        self.assertEqual(validate_route_packet(payload["route_packet"]), [])
        payload["route_packet"]["routing_trace"]["legacy_fallback_used"] = True
        self.assertIn("task_routing:legacy_fallback_conflict", validate_route_packet(payload["route_packet"]))
        payload["route_packet"]["routing_trace"]["legacy_fallback_used"] = False
        payload["status"] = "completed"
        payload["verification_evidence"] = ["caller says success"]
        self.assertIn("task_routing:contract_mode_not_completion", validate_runner_result(payload))

    def test_adapter_uses_actual_multi_stack_manifests_and_project_commands(self):
        cases = [
            ("package.json", '{"devDependencies":{"vitest":"1.0.0"}}', "javascript", "javascript_typescript", "npm test"),
            ("go.mod", "module example.test/sample\n", "go", "compiled_systems", "go test ./..."),
            ("Cargo.toml", '[package]\nname="sample"\nversion="0.1.0"\n', "rust", "compiled_systems", "cargo test"),
            ("pom.xml", "<project/>\n", "java", "enterprise_oop", "mvn test"),
        ]
        for manifest, content, language, family, command in cases:
            with self.subTest(manifest=manifest), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                context = self._workspace(root)
                (root / "pyproject.toml").unlink()
                (root / manifest).write_text(content, encoding="utf-8")
                (root / "TEST.md").write_text(command + "\n", encoding="utf-8")
                context["risks"][0]["languages"] = [language]
                context["checks"][0]["command"] = command
                result = self._cli(root, context)
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                route = json.loads(result.stdout)["route_packet"]
                profile = next(p for p in route["code_quality_profile"]["stack_profiles"] if p["family"] == family)
                self.assertEqual(profile["status"], "present_unverified")
                self.assertEqual(route["verification"], [command])

    def test_nested_project_instructions_and_verification_file_changes_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            context = self._workspace(root)
            (root / "src").mkdir()
            (root / "src" / "AGENTS.md").write_text("Always run `python -m unittest test_extra`.\n", encoding="utf-8")
            (root / "src" / "calc.py").write_text("value = 1\n", encoding="utf-8")
            (root / "test_calc.py").write_text("# test definition\n", encoding="utf-8")
            context.update(changed_paths=["src/calc.py"], verification_paths=["test_calc.py"])
            payload = json.loads(self._cli(root, context).stdout)
            self.assertEqual(payload["status"], "route_ready")
            route = payload["route_packet"]
            self.assertIn("src/AGENTS.md", route["required_inputs"])
            self.assertIn("python -m unittest test_extra", route["verification"])
            (root / "test_calc.py").write_text("# changed test definition\n", encoding="utf-8")
            current = json.loads(self._cli(root, context).stdout)
            self.assertNotEqual(route["task_routing"]["input_digest"], current["route_packet"]["task_routing"]["input_digest"])


if __name__ == "__main__":
    unittest.main()
