import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
WRAPPER = SCRIPTS / "render_status_dashboard.py"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.infrastructure import (  # noqa: E402
    InfrastructureError,
    render_infrastructure_plan,
    render_status_dashboard_plan,
    stage_status_dashboard,
)
from product_agent_os.merge_infrastructure import build_merge_plan  # noqa: E402
from product_agent_os.offline_artifact_safety import GENERATED_VIEW_ONLY_TEXT  # noqa: E402
from product_agent_os.stage_manifest import MANIFEST_NAME  # noqa: E402
from product_agent_os.status_dashboard import (  # noqa: E402
    STATUS_HTML_TARGET,
    STATUS_JSON_TARGET,
    render_status_dashboard,
    validate_status_dashboard_manifest,
)
from product_agent_os.templates import required_templates  # noqa: E402


class StatusDashboardTest(unittest.TestCase):
    def test_renderer_outputs_offline_html_sections_and_safe_snapshot_json(self):
        result = render_status_dashboard(_snapshot())
        html = result["html"]
        snapshot_json = result["json"]
        lower = html.lower()

        self.assertTrue(lower.startswith("<!doctype html>"))
        self.assertIn('<meta name="viewport"', lower)
        self.assertNotIn("http://", lower)
        self.assertNotIn("https://", lower)
        self.assertNotIn("<script src=", lower)
        self.assertIn('id="section-lifecycle"', html)
        self.assertIn('id="section-usage-mode"', html)
        self.assertIn('id="section-questions"', html)
        self.assertIn('id="section-readiness"', html)
        self.assertIn('id="section-completion-skeptic"', html)
        self.assertIn('id="section-professional-code-authoring"', html)
        self.assertIn('id="system-file-hygiene"', html)
        self.assertIn('id="section-evidence"', html)
        self.assertIn('id="section-approvals"', html)
        self.assertIn('id="section-next-action"', html)
        self.assertIn("Evidence requires review", html)
        self.assertIn("@media", html)
        self.assertIn('<script type="application/json" id="status-snapshot">', html)
        self.assertNotIn("</script><script", html)
        self.assertIn(GENERATED_VIEW_ONLY_TEXT, html)
        self.assertIn("generated view policy present", result["validation"]["checks"])
        self.assertIn("system hygiene dashboard present", result["validation"]["checks"])
        self.assertIn("completion skeptic dashboard present", result["validation"]["checks"])
        self.assertEqual(json.loads(snapshot_json)["schema_version"], 1)
        self.assertEqual(result["validation"]["errors"], [])

    def test_renderer_outputs_completion_skeptic_section_as_generated_guidance_only(self):
        snapshot = _snapshot()
        snapshot["completion_skeptic"] = {
            "status": "recommended",
            "trigger_level": "recommended",
            "recommended_skill": "completion-skeptic",
            "top_reason": "completion claim needs a second-pass evidence check",
            "trigger_sources": ["completion_claim"],
            "risk_classes": ["verification_gap"],
            "required_evidence": ["current command evidence"],
            "evidence_summary": {
                "required": 1,
                "available": 0,
                "missing": 1,
                "stale": 0,
                "approval_required": 0,
                "accepted_gap": 0,
            },
            "approval_boundary": {"status": "not_required", "hits": []},
            "packet_ref": {"kind": "not_available", "path": "", "digest": ""},
            "safe_next_action": "Run completion-skeptic before claiming completion.",
            "source_policy": "completion skeptic recommendation is generated routing guidance, not source of truth",
        }

        result = render_status_dashboard(snapshot)
        html = result["html"]

        self.assertIn('id="section-completion-skeptic"', html)
        self.assertIn("Completion Skeptic", html)
        self.assertIn("completion-skeptic", html)
        self.assertIn("generated routing guidance, not source of truth", html)
        self.assertIn("Run completion-skeptic before claiming completion.", html)
        self.assertNotIn("claim_ledger", html)
        self.assertEqual(result["validation"]["errors"], [])

    def test_renderer_outputs_system_file_hygiene_section_with_grouped_status_tables(self):
        snapshot = _snapshot()
        snapshot["system_file_hygiene"] = _system_file_hygiene_snapshot()

        result = render_status_dashboard(snapshot)
        html = result["html"]

        self.assertIn('id="system-file-hygiene"', html)
        self.assertIn("System Hygiene", html)
        self.assertIn("system file hygiene projection is generated status evidence, not source of truth", html)
        for expected in [
            "OK",
            "Review Required",
            "Blocked",
            "Missing",
            "Unreadable",
            "Stale",
            "Owner Unknown",
            "Root Control Plane",
            "Agents",
            "Skills",
            "Workflows",
            "Automation Candidates",
            "Hooks",
            "Evals",
            "Docs Source Control",
            "Plugin Control Files",
            "Top finding",
            "PLAN.md",
            ".codex/agents/reviewer.toml",
            ".codex/skills/review/SKILL.md",
            ".codex/workflows/release.md",
            ".codex/automation-candidates/system-file-hygiene-audit.md",
            ".codex/hooks/pre-tool-use.md",
            ".codex/evals/workflow.json",
            "docs/sources/registry.md",
            "plugins/product-agent-os/README.md",
            "2026-06-05",
            "2 days",
            "missing_control_plane_file",
            "unreadable_utf8",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, html)

        self.assertNotIn("C:\\Users\\person", html)
        self.assertEqual(result["validation"]["errors"], [])

    def test_renderer_displays_task_matrix_projection_deferred_decision_without_state_rows(self):
        snapshot = _snapshot()
        snapshot["projection_decisions"] = {
            "task_matrix_state": {
                "status": "deferred_in_b37",
                "state_projection": "not_projected",
                "source_policy": "task matrix state is not projected into status snapshot/dashboard in B37",
                "future_projection_policy": (
                    "future projection must be bounded read-only generated orientation evidence, "
                    "never source of truth or completion evidence"
                ),
            }
        }

        result = render_status_dashboard(snapshot)
        rendered = result["html"] + result["json"]

        self.assertIn("Task matrix state projection", result["html"])
        self.assertIn("deferred_in_b37", rendered)
        self.assertIn("not_projected", rendered)
        self.assertIn("bounded read-only generated orientation evidence", rendered)
        self.assertNotIn("task-matrix row", result["html"].lower())
        self.assertEqual(result["validation"]["errors"], [])

    def test_renderer_keeps_system_hygiene_html_when_embedded_json_is_trimmed(self):
        snapshot = _snapshot()
        snapshot["system_file_hygiene"] = _system_file_hygiene_snapshot()
        snapshot["large_generated_notes"] = ["x" * 1000 for _ in range(20)]

        result = render_status_dashboard(snapshot)
        embedded_json = json.loads(result["json"])

        self.assertEqual(embedded_json["status"], "trimmed")
        self.assertTrue(embedded_json["trimmed"])
        self.assertIn('id="system-file-hygiene"', result["html"])
        self.assertIn("System Hygiene", result["html"])
        self.assertIn(".codex/skills/review/SKILL.md", result["html"])
        self.assertEqual(result["validation"]["errors"], [])

    def test_system_hygiene_html_safety_and_severity_class_path_sorting(self):
        snapshot = _snapshot()
        snapshot["workspace"] = "C:\\Users\\person\\private-project"
        snapshot["system_file_hygiene"] = _system_file_hygiene_snapshot()
        snapshot["system_file_hygiene"]["file_statuses"] = [
            {
                "path": "Z-review.md",
                "class": "root_control_plane",
                "owner": "project root",
                "state": "review_required",
                "severity": "warning",
                "finding_count": 1,
                "mtime_utc": "2026-06-05T12:00:00+00:00",
                "age_days": 2,
                "content_digest": "sha256:" + "b" * 64,
                "last_audit_at": "2026-06-07T12:00:00+00:00",
                "top_finding": "duplicate_markdown_headings",
                "raw_body": "OPENAI_API_KEY = \"sk-test\"",
            },
            {
                "path": "A-owner.md",
                "class": "root_control_plane",
                "owner": "unknown",
                "state": "owner_unknown",
                "severity": "warning",
                "finding_count": 1,
                "mtime_utc": "2026-06-04T12:00:00+00:00",
                "age_days": 3,
                "content_digest": "sha256:" + "c" * 64,
                "last_audit_at": "2026-06-07T12:00:00+00:00",
                "top_finding": "owner_unknown",
            },
            {
                "path": "C:\\Users\\person\\private-project\\PLAN.md",
                "class": "root_control_plane",
                "owner": "TOKEN=fixture-secret",
                "state": "blocked",
                "severity": "error",
                "finding_count": 1,
                "mtime_utc": "2026-06-03T12:00:00+00:00",
                "age_days": 4,
                "content_digest": "sha256:" + "d" * 64,
                "last_audit_at": "2026-06-07T12:00:00+00:00",
                "top_finding": "secret_like_literal",
            },
        ]
        snapshot["large_generated_notes"] = ["x" * 1000 for _ in range(20)]

        result = render_status_dashboard(snapshot)
        rendered = result["html"] + result["json"]

        self.assertIn("Evidence requires review", result["html"])
        self.assertIn(GENERATED_VIEW_ONLY_TEXT, result["html"])
        self.assertLessEqual(len(result["json"].encode("utf-8")), 12000)
        self.assertLess(result["html"].index("A-owner.md"), result["html"].index("Z-review.md"))
        self.assertNotIn("C:\\Users\\person", rendered)
        self.assertNotIn("private-project", rendered)
        self.assertNotIn("fixture-secret", rendered)
        self.assertNotIn("OPENAI_API_KEY", rendered)
        self.assertNotIn("raw_body", rendered)
        self.assertNotIn("https://", rendered.lower())
        self.assertEqual(result["validation"]["errors"], [])

    def test_system_hygiene_stale_row_triggers_review_banner(self):
        snapshot = _snapshot()
        snapshot["usage_mode"]["primary"] = "standard_feature"
        snapshot["usage_mode"]["inspection_only"] = False
        snapshot["readiness_summary"]["warnings"] = []
        snapshot["evidence_summary"]["freshness"] = "current"
        snapshot["system_file_hygiene"] = _system_file_hygiene_snapshot()
        snapshot["system_file_hygiene"]["file_statuses"] = [
            {
                "path": "PLAN.md",
                "class": "root_control_plane",
                "owner": "project root",
                "state": "stale",
                "severity": "none",
                "finding_count": 0,
                "mtime_utc": "2026-05-01T12:00:00+00:00",
                "age_days": 37,
                "content_digest": "sha256:" + "e" * 64,
                "last_audit_at": "2026-06-07T12:00:00+00:00",
                "top_finding": "mtime_older_than_30_days",
            }
        ]

        result = render_status_dashboard(snapshot)

        self.assertIn("Evidence requires review", result["html"])
        self.assertEqual(result["validation"]["errors"], [])

    def test_renderer_redacts_secret_private_and_local_path_values(self):
        snapshot = _snapshot()
        snapshot["workspace"] = "C:\\Users\\person\\private-project"
        snapshot["next_safe_action"] = "\n".join(
            [
                "TOKEN=fixture-secret",
                "Inspect raw private chat log in C:\\Users\\person\\private-project",
                "Inspect D:\\work\\private-project\\PLAN.md",
                "Inspect \\\\server\\share\\private-project\\AGENTS.md",
                "Inspect /Users/person/private-project/RUNLOG.md",
                "Inspect /home/person/private-project/TEST.md",
                "Synthetic token sk-test-secret must not render.",
            ]
        )

        result = render_status_dashboard(snapshot)
        rendered = result["html"] + result["json"]

        self.assertNotIn("fixture-secret", rendered)
        self.assertNotIn("C:\\Users\\person", rendered)
        self.assertNotIn("D:\\work", rendered)
        self.assertNotIn("\\\\server\\share", rendered)
        self.assertNotIn("/Users/person", rendered)
        self.assertNotIn("/home/person", rendered)
        self.assertNotIn("sk-test-secret", rendered)
        self.assertNotIn("raw private chat log", rendered)
        self.assertIn("secret", result["redaction_summary"]["categories"])
        self.assertIn("absolute_path", result["redaction_summary"]["categories"])
        self.assertIn("private_data", result["redaction_summary"]["categories"])
        self.assertEqual(result["validation"]["errors"], [])

    def test_dashboard_staging_is_explicit_opt_in_and_uses_standard_stage_manifest(self):
        template_targets = {item.target_path for item in required_templates()}
        self.assertNotIn(STATUS_HTML_TARGET, template_targets)
        self.assertNotIn(STATUS_JSON_TARGET, template_targets)
        baseline = render_infrastructure_plan(FIXTURES / "empty-repo")
        baseline_targets = {item["target_path"] for item in baseline["rendered_artifacts"]["files"]}
        self.assertNotIn(STATUS_HTML_TARGET, baseline_targets)
        self.assertNotIn(STATUS_JSON_TARGET, baseline_targets)
        dashboard_plan = render_status_dashboard_plan(FIXTURES / "empty-repo", _snapshot())
        dashboard_targets = {item["target_path"] for item in dashboard_plan["rendered_artifacts"]["files"]}
        self.assertEqual(dashboard_plan["rendered_artifacts"]["mode"], "dry-run")
        self.assertEqual(dashboard_targets, {STATUS_HTML_TARGET, STATUS_JSON_TARGET})

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)

            result = stage_status_dashboard(workspace, stage_root, _snapshot())
            plan = build_merge_plan(workspace, stage_root)

            by_target = {item["target_path"]: item for item in result["rendered_artifacts"]["files"]}
            self.assertEqual(set(by_target), {STATUS_HTML_TARGET, STATUS_JSON_TARGET})
            self.assertEqual(by_target[STATUS_HTML_TARGET]["action"], "create")
            self.assertEqual(by_target[STATUS_JSON_TARGET]["action"], "create")
            self.assertTrue((stage_root / STATUS_HTML_TARGET).exists())
            self.assertTrue((stage_root / STATUS_JSON_TARGET).exists())
            self.assertTrue((stage_root / MANIFEST_NAME).exists())
            self.assertEqual(validate_status_dashboard_manifest(stage_root), [])
            self.assertFalse((workspace / STATUS_HTML_TARGET).exists())
            self.assertFalse((workspace / STATUS_JSON_TARGET).exists())
            self.assertEqual(plan["status"], "needs_approval")
            self.assertTrue(all(item["approval_required"] for item in plan["decisions"]))

    def test_existing_dashboard_targets_are_preserved_as_companion_proposals(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)
            existing_html = workspace / STATUS_HTML_TARGET
            existing_json = workspace / STATUS_JSON_TARGET
            existing_html.parent.mkdir(parents=True)
            existing_html.write_text("<!doctype html>\n<title>User status</title>\n", encoding="utf-8")
            existing_json.write_text('{"user": true}\n', encoding="utf-8")

            result = stage_status_dashboard(workspace, stage_root, _snapshot())
            plan = build_merge_plan(workspace, stage_root)

            by_target = {item["target_path"]: item for item in result["rendered_artifacts"]["files"]}
            self.assertEqual(by_target[STATUS_HTML_TARGET]["action"], "leave_unchanged")
            self.assertEqual(by_target[STATUS_JSON_TARGET]["action"], "leave_unchanged")
            self.assertIn("_proposals", by_target[STATUS_HTML_TARGET]["staged_path"])
            self.assertIn("_proposals", by_target[STATUS_JSON_TARGET]["staged_path"])
            self.assertEqual(existing_html.read_text(encoding="utf-8"), "<!doctype html>\n<title>User status</title>\n")
            self.assertEqual(existing_json.read_text(encoding="utf-8"), '{"user": true}\n')
            self.assertEqual(plan["status"], "ready")
            self.assertTrue(all(item["action"] == "companion_only" for item in plan["decisions"]))

    def test_dashboard_manifest_blocks_path_escape_and_stale_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)
            stage_status_dashboard(workspace, stage_root, _snapshot())

            html_path = stage_root / STATUS_HTML_TARGET
            html_path.write_text(html_path.read_text(encoding="utf-8") + "\n<!-- mutated -->\n", encoding="utf-8")

            errors = validate_status_dashboard_manifest(stage_root)
            plan = build_merge_plan(workspace, stage_root)

            self.assertIn("staged digest does not match manifest", " ".join(errors))
            self.assertEqual(plan["status"], "blocked")
            self.assertIn("staged digest does not match manifest", " ".join(plan["blocked"]))

            manifest_path = stage_root / MANIFEST_NAME
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["files"][0]["target_path"] = "../status.html"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            self.assertIn("target path escapes workspace", " ".join(validate_status_dashboard_manifest(stage_root)))

    def test_dashboard_stage_rejects_output_directory_inside_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            shutil.copytree(FIXTURES / "empty-repo", workspace)

            with self.assertRaises(InfrastructureError) as error:
                stage_status_dashboard(workspace, workspace / ".codex" / "product-agent-os", _snapshot())

        self.assertIn("outside workspace", str(error.exception))

    def test_cli_dry_run_and_stage_emit_json_without_workspace_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "status-stage"
            workspace.mkdir()
            _write_control_plane(workspace)

            dry_run = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--dry-run"],
                check=False,
                capture_output=True,
                text=True,
            )
            staged = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )

            dry_payload = json.loads(dry_run.stdout)
            staged_payload = json.loads(staged.stdout)
            self.assertEqual(dry_run.returncode, 0, dry_run.stdout + dry_run.stderr)
            self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
            self.assertEqual(dry_run.stderr, "")
            self.assertEqual(staged.stderr, "")
            self.assertEqual(dry_payload["rendered_artifacts"]["mode"], "dry-run")
            self.assertEqual(staged_payload["rendered_artifacts"]["mode"], "stage")
            status_json_entry = next(
                item
                for item in dry_payload["rendered_artifacts"]["files"]
                if item["target_path"] == STATUS_JSON_TARGET
            )
            status_snapshot = json.loads(status_json_entry["content"])
            self.assertNotEqual(status_snapshot["system_file_hygiene"]["status"], "not_available")
            self.assertGreaterEqual(len(status_snapshot["system_file_hygiene"]["file_statuses"]), 1)
            self.assertFalse((workspace / STATUS_HTML_TARGET).exists())
            self.assertFalse((workspace / STATUS_JSON_TARGET).exists())
            self.assertTrue((stage_root / STATUS_HTML_TARGET).exists())
            self.assertTrue((stage_root / STATUS_JSON_TARGET).exists())
            self.assertNotIn(str(workspace), dry_run.stdout)

    def test_cli_missing_workspace_returns_json_error_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing-workspace"

            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(missing), "--dry-run"],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "error")
        self.assertIn("workspace", payload["error"])


def _snapshot():
    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "generated_at": "2026-05-28T10:00:00+00:00",
        "workspace": "[REDACTED_LOCAL_PATH]",
        "lifecycle_state": "quality_gate",
        "usage_mode": {
            "primary": "inspection_only",
            "confidence": "high",
            "inspection_only": True,
            "minimum_artifacts": ["RUNLOG.md", "TEST.md"],
        },
        "question_summary": {
            "total": 2,
            "blocking": 1,
            "recommended": 1,
            "optional": 0,
            "remaining": 1,
            "next_blocking_question": {
                "id": "q_owner_approval",
                "text": "Who owns approval for the next write?",
                "priority": "blocking",
            },
            "first_response_summary": ["1 blocking question", "1 recommended question", "0 optional questions"],
        },
        "readiness_summary": {
            "status": "inspection_only",
            "runtime_status": "completed",
            "success_claim": "not_claimed",
            "warnings": ["stale evidence", "inspection-only evidence cannot prove completion"],
        },
        "evidence_summary": {
            "freshness": "stale",
            "evidence_count": 1,
            "stale_count": 1,
            "max_age_days": 14,
        },
        "next_safe_action": "Ask the owner to refresh verification evidence before claiming completion.",
        "dashboard_policy": {
            "write_policy": "read_only",
            "source_of_truth": "underlying_artifacts",
            "success_claim_policy": "never from dashboard alone",
            "external_assets": "forbidden",
        },
        "renderer_file_count": 2,
        "staged_artifacts": {
            "mode": "stage",
            "targets": [{"target_path": "AGENTS.md", "action": "create"}],
            "validation_ok": True,
        },
        "manifest_digests": {
            "workspace_audit_digest": "sha256:" + "a" * 64,
            "infrastructure_plan_digest": "sha256:" + "b" * 64,
            "file_count": 1,
            "file_digests": [{"target_path": "AGENTS.md", "digest": "sha256:" + "c" * 64}],
        },
        "source_artifact_ledger": [{"artifact": "approval-record.md", "decision": "canonical_template"}],
        "semantic_evidence_sufficiency": {
            "status": "present_unverified",
            "required_evidence": ["owner-reviewed evidence"],
        },
        "question_ledger_summary": {"accepted": 1, "blocked": 0, "unanswered": 1, "total": 2},
        "question_ledger_artifact_updates": [
            {"artifact": "approval-record.md", "question_ids": ["q_owner_approval"]}
        ],
        "approval_summary": {
            "status": "required",
            "requirements": ["explicit approval required before workspace writes"],
        },
        "redaction_summary": {"count": 0, "categories": []},
    }


def _write_control_plane(workspace: Path) -> None:
    (workspace / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
    (workspace / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n## Acceptance Criteria\n\n- Synthetic.\n",
        encoding="utf-8",
    )
    (workspace / "PLAN.md").write_text("# Plan\n\n## Verification\n\n- Run tests.\n", encoding="utf-8")
    (workspace / "TEST.md").write_text("# Test\n\nQuality gates: unit tests.\n", encoding="utf-8")
    (workspace / "EVALS.md").write_text("# Evals\n\nQuality gates: fixture eval.\n", encoding="utf-8")
    (workspace / "RUNLOG.md").write_text("# Runlog\n\nlifecycle_state: quality_gate\n", encoding="utf-8")


def _system_file_hygiene_snapshot():
    digest = "sha256:" + "a" * 64
    records = [
        ("PLAN.md", "root_control_plane", "project root", "blocked", "error", "hard_size_limit_exceeded"),
        (".codex/agents/reviewer.toml", "codex_agents", "agent-team designer", "ok", "none", "none"),
        (".codex/skills/review/SKILL.md", "codex_skills", "skill owner", "unreadable", "error", "unreadable_utf8"),
        (".codex/workflows/release.md", "codex_workflows", "workflow owner", "review_required", "warning", "duplicate_markdown_headings"),
        (
            ".codex/automation-candidates/system-file-hygiene-audit.md",
            "automation_candidates",
            "automation owner",
            "missing",
            "warning",
            "missing_control_plane_file",
        ),
        (".codex/hooks/pre-tool-use.md", "hooks", "project operator", "stale", "none", "none"),
        (".codex/evals/workflow.json", "evals", "test/eval owner", "owner_unknown", "warning", "owner_unknown"),
        ("docs/sources/registry.md", "docs_source_control", "docs maintainer", "ok", "none", "none"),
        ("plugins/product-agent-os/README.md", "plugin_package_control", "plugin maintainer", "ok", "none", "none"),
    ]
    return {
        "status": "blocked",
        "audit_trigger": "status_dashboard_projection",
        "last_audit_at": "2026-06-07T12:00:00+00:00",
        "write_policy": "read_only",
        "schedule_status": "not_created",
        "summary": {
            "files_scanned": len(records),
            "warnings": 3,
            "errors": 2,
            "active_schedule_markers": 0,
        },
        "file_statuses": [
            {
                "path": path,
                "class": class_key,
                "owner": owner,
                "state": state,
                "severity": severity,
                "finding_count": 0 if top_finding == "none" else 1,
                "size": 128,
                "line_count": 8,
                "mtime_utc": "2026-06-05T12:00:00+00:00",
                "age_days": 2,
                "content_digest": digest,
                "last_audit_at": "2026-06-07T12:00:00+00:00",
                "top_finding": top_finding,
            }
            for path, class_key, owner, state, severity, top_finding in records
        ],
        "source_policy": "system file hygiene projection is generated status evidence, not source of truth",
        "approval_boundary": "owner_approval_required_for_writes",
    }


if __name__ == "__main__":
    unittest.main()
