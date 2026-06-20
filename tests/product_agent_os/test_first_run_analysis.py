from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _load_contract():
    if importlib.util.find_spec("product_agent_os.first_run_analysis") is None:
        raise AssertionError("product_agent_os.first_run_analysis module is required")
    from product_agent_os.first_run_analysis import (  # noqa: PLC0415
        FIRST_RUN_ANALYSIS_PACKET_SCHEMA,
        build_first_run_analysis_packet,
        validate_first_run_analysis_packet,
    )

    return (
        FIRST_RUN_ANALYSIS_PACKET_SCHEMA,
        build_first_run_analysis_packet,
        validate_first_run_analysis_packet,
    )


class FirstRunAnalysisPacketTests(unittest.TestCase):
    def test_m20_1_builds_packet_with_required_source_and_policy_fields(self) -> None:
        _schema, build_packet, validate_packet = _load_contract()

        packet = build_packet(
            target_label="SOL 0.6",
            generated_at="2026-06-18T12:00:00+03:00",
            source_artifacts=[
                {
                    "artifact_id": "discovery",
                    "path": "docs/superpowers/specs/batch39-m11-target-fixture-pack.json",
                    "digest": "sha256:" + "a" * 64,
                    "evidence_status": "current",
                    "provenance": "workspace_discovery_auditor",
                },
                {
                    "artifact_id": "status_snapshot",
                    "path": ".codex/product-agent-os/status.json",
                    "digest": "sha256:" + "b" * 64,
                    "evidence_status": "inspection_only",
                    "provenance": "status_snapshot",
                },
            ],
            generated_pages=[
                {
                    "page_id": "overview",
                    "path": ".codex/product-agent-os/analysis/index.html",
                    "digest": "sha256:" + "c" * 64,
                    "source_policy": "generated_view_only",
                }
            ],
            section_summaries={
                "discovery": {"status": "current", "unsupported_claims": []},
                "runtime_route": {"status": "approval_required", "unsupported_claims": ["live runtime not run"]},
                "methodology_audit": {"status": "present_unverified", "unsupported_claims": []},
                "control_plane": {"status": "present_unverified", "unsupported_claims": []},
                "source_policy": {"status": "present_unverified", "unsupported_claims": []},
                "graph": {"status": "inspection_only", "unsupported_claims": ["graph is not source truth"]},
                "status_snapshot": {"status": "inspection_only", "unsupported_claims": []},
            },
            safe_next_action="Review packet and continue with dry-run orchestration only.",
        )

        encoded = json.dumps(packet, ensure_ascii=False, sort_keys=True)
        self.assertEqual(packet["schema_version"], "first_run_analysis_packet_v1")
        self.assertEqual(packet["artifact_version"], 1)
        self.assertEqual(packet["target"]["label"], "SOL 0.6")
        self.assertEqual(packet["write_policy"], "read_only_generated_analysis_only")
        self.assertEqual(packet["generated_view_policy"], "orientation_only_not_proof")
        self.assertEqual(packet["redaction_status"]["status"], "passed_redacted")
        self.assertEqual(packet["evidence_status"]["freshness"], "mixed")
        self.assertEqual(packet["evidence_status"]["completion_claim"], "not_claimed")
        self.assertTrue(packet["packet_digest"].startswith("sha256:"))
        self.assertNotIn("C:\\Users\\user", encoded)
        self.assertNotIn("raw_source", encoded)
        self.assertEqual(validate_packet(packet), [])

    def test_m20_1_schema_declares_required_packet_fields(self) -> None:
        schema, _build_packet, _validate_packet = _load_contract()
        required = set(schema["required"])

        for field in [
            "schema_version",
            "artifact_version",
            "generated_at",
            "target",
            "write_policy",
            "source_artifacts",
            "generated_pages",
            "section_summaries",
            "redaction_status",
            "evidence_status",
            "generated_view_policy",
            "safe_next_action",
            "packet_digest",
        ]:
            self.assertIn(field, required)

    def test_m20_1_packet_round_trips_as_json_and_rejects_unsafe_values(self) -> None:
        _schema, build_packet, validate_packet = _load_contract()
        packet = build_packet(
            target_label="SOL 0.6",
            generated_at="2026-06-18T12:00:00+03:00",
            source_artifacts=[
                {
                    "artifact_id": "discovery",
                    "path": "docs/superpowers/specs/batch39-m11-target-fixture-pack.json",
                    "digest": "sha256:" + "d" * 64,
                    "evidence_status": "current",
                    "provenance": "workspace_discovery_auditor",
                }
            ],
            generated_pages=[],
            section_summaries={
                "discovery": {"status": "current", "unsupported_claims": []},
                "runtime_route": {"status": "not_available", "unsupported_claims": []},
                "methodology_audit": {"status": "not_available", "unsupported_claims": []},
                "control_plane": {"status": "not_available", "unsupported_claims": []},
                "source_policy": {"status": "not_available", "unsupported_claims": []},
                "graph": {"status": "not_available", "unsupported_claims": []},
                "status_snapshot": {"status": "not_available", "unsupported_claims": []},
            },
            safe_next_action="Run dry-run orchestration contract next.",
        )

        round_tripped = json.loads(json.dumps(packet, ensure_ascii=False, sort_keys=True))
        self.assertEqual(round_tripped, packet)

        unsafe = json.loads(json.dumps(packet, ensure_ascii=False))
        unsafe["source_artifacts"][0]["path"] = r"C:\Users\user\Desktop\private\artifact.json"
        unsafe["section_summaries"]["discovery"]["raw_source"] = "private body"
        unsafe["redaction_status"]["secrets_allowed"] = True

        errors = validate_packet(unsafe)
        self.assertIn("local absolute path leaked", errors)
        self.assertIn("raw source field retained", errors)
        self.assertIn("redaction_status.secrets_allowed must be false", errors)

    def test_m20_2_cli_dry_run_prints_packet_without_writing_analysis_directory(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "sample-target"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--dry-run",
                    "--generated-at",
                    "2026-06-18T13:00:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["mode"], "dry_run")
            self.assertEqual(payload["packet"]["schema_version"], "first_run_analysis_packet_v1")
            self.assertEqual(payload["write_boundary"]["analysis_dir"], ".codex/product-agent-os/analysis")
            self.assertFalse((workspace / ".codex" / "product-agent-os" / "analysis").exists())
            self.assertNotIn(str(workspace), result.stdout)

    def test_m20_2_cli_write_mode_writes_only_generated_analysis_packet_inside_workspace(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "sample-target"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")
            before_files = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--write",
                    "--generated-at",
                    "2026-06-18T13:00:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            output_ref = ".codex/product-agent-os/analysis/first-run-analysis-packet.json"
            output_path = workspace / output_ref
            after_files = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())
            added_files = sorted(set(after_files) - set(before_files))

            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["mode"], "write")
            self.assertEqual(payload["written_files"], [output_ref])
            self.assertTrue(output_path.exists())
            self.assertEqual(added_files, [output_ref])
            written_packet = json.loads(output_path.read_text(encoding="utf-8"))
            _schema, _build_packet, validate_packet = _load_contract()
            self.assertEqual(validate_packet(written_packet), [])
            self.assertNotIn(str(workspace), result.stdout)

    def test_m20_2_cli_rejects_ambiguous_mode(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "sample-target"
            workspace.mkdir()

            ambiguous = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--dry-run",
                    "--write",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(ambiguous.returncode, 0)
            self.assertIn("choose exactly one mode", ambiguous.stdout)

    def test_m20_3_adapter_normalizes_analyzer_outputs_with_provenance_and_gaps(self) -> None:
        _schema, build_packet, validate_packet = _load_contract()
        from product_agent_os.first_run_analysis import adapt_first_run_analysis_sections  # noqa: PLC0415

        sections = adapt_first_run_analysis_sections(
            {
                "discovery": {
                    "source_module": "product_agent_os.discovery",
                    "source_artifact": "docs/superpowers/specs/discovery.json",
                    "evidence_freshness": "current",
                    "confidence": "high",
                    "unsupported_claims": [],
                    "accepted_gaps": [],
                },
                "runtime_route": {
                    "source_module": "codex_runtime_runner.cli",
                    "source_artifact": ".codex/product-agent-os/runtime-result.json",
                    "evidence_freshness": "approval_required",
                    "confidence": "medium",
                    "unsupported_claims": ["live runtime not run"],
                    "accepted_gaps": ["runtime launch requires exact approval"],
                },
            }
        )

        self.assertEqual(sections["discovery"]["source_module"], "product_agent_os.discovery")
        self.assertEqual(sections["discovery"]["evidence_freshness"], "current")
        self.assertEqual(sections["runtime_route"]["confidence"], "medium")
        self.assertIn("live runtime not run", sections["runtime_route"]["unsupported_claims"])
        self.assertIn("runtime launch requires exact approval", sections["runtime_route"]["accepted_gaps"])
        self.assertEqual(sections["graph"]["source_module"], "not_available")
        self.assertEqual(sections["graph"]["evidence_freshness"], "not_available")

        packet = build_packet(
            target_label="SOL 0.6",
            generated_at="2026-06-18T14:00:00+03:00",
            source_artifacts=[
                {
                    "artifact_id": "discovery",
                    "path": "docs/superpowers/specs/discovery.json",
                    "digest": "sha256:" + "e" * 64,
                    "evidence_status": "current",
                    "provenance": "product_agent_os.discovery",
                }
            ],
            generated_pages=[],
            section_summaries=sections,
            safe_next_action="Continue with renderer safety tests.",
        )

        self.assertEqual(packet["section_summaries"]["runtime_route"]["source_module"], "codex_runtime_runner.cli")
        self.assertEqual(packet["section_summaries"]["runtime_route"]["source_artifact"], ".codex/product-agent-os/runtime-result.json")
        self.assertEqual(validate_packet(packet), [])

    def test_m20_3_adapter_redacts_unsafe_artifacts_and_rejects_raw_source_fields(self) -> None:
        _schema, _build_packet, _validate_packet = _load_contract()
        from product_agent_os.first_run_analysis import adapt_first_run_analysis_sections  # noqa: PLC0415

        sections = adapt_first_run_analysis_sections(
            {
                "discovery": {
                    "source_module": "product_agent_os.discovery",
                    "source_artifact": r"C:\Users\user\private\discovery.json",
                    "evidence_freshness": "current",
                    "confidence": "high",
                    "raw_source": "private body",
                }
            }
        )

        self.assertEqual(sections["discovery"]["source_artifact"], "[REDACTED_LOCAL_PATH]")
        self.assertNotIn("raw_source", sections["discovery"])

    def test_m20_4_renderer_writes_offline_pages_and_manifest_under_analysis_dir(self) -> None:
        _schema, build_packet, _validate_packet = _load_contract()
        from product_agent_os.analysis_artifact_renderer import (  # noqa: PLC0415
            FIRST_RUN_ANALYSIS_PAGE_IDS,
            render_first_run_analysis_artifact,
        )

        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "sample-target"
            workspace.mkdir()
            packet = build_packet(
                target_label="SOL 0.6",
                generated_at="2026-06-18T15:00:00+03:00",
                source_artifacts=[
                    {
                        "artifact_id": "discovery",
                        "path": "docs/superpowers/specs/discovery.json",
                        "digest": "sha256:" + "f" * 64,
                        "evidence_status": "current",
                        "provenance": "product_agent_os.discovery",
                    }
                ],
                generated_pages=[],
                section_summaries={
                    "discovery": {"status": "current", "unsupported_claims": []},
                    "runtime_route": {"status": "approval_required", "unsupported_claims": ["live runtime not run"]},
                    "methodology_audit": {"status": "present_unverified", "unsupported_claims": []},
                    "control_plane": {"status": "present_unverified", "unsupported_claims": []},
                    "source_policy": {"status": "present_unverified", "unsupported_claims": []},
                    "graph": {"status": "not_available", "unsupported_claims": ["graph not generated"]},
                    "status_snapshot": {"status": "not_available", "unsupported_claims": []},
                },
                safe_next_action="Continue with manifest digest support.",
            )

            result = render_first_run_analysis_artifact(packet, workspace)
            analysis_dir = workspace / ".codex" / "product-agent-os" / "analysis"
            manifest_path = analysis_dir / "analysis-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            html = "\n".join((analysis_dir / page["path"]).read_text(encoding="utf-8") for page in manifest["pages"])

            self.assertEqual(result["status"], "ready")
            self.assertEqual(FIRST_RUN_ANALYSIS_PAGE_IDS, [page["page_id"] for page in manifest["pages"]])
            self.assertTrue((analysis_dir / "index.html").exists())
            self.assertTrue(manifest_path.exists())
            self.assertEqual(manifest["generated_view_policy"], "orientation_only_not_proof")
            self.assertEqual(manifest["source_packet_digest"], packet["packet_digest"])
            self.assertIn("generated-view-only", html)
            self.assertIn("docs/superpowers/specs/discovery.json", html)
            self.assertNotIn("http://", html)
            self.assertNotIn("https://", html)
            self.assertNotIn("<script src", html.lower())
            self.assertNotIn("fetch(", html.lower())
            self.assertNotIn(str(workspace), html)

    def test_m20_4_renderer_rejects_invalid_packet_before_writing_pages(self) -> None:
        _schema, build_packet, _validate_packet = _load_contract()
        from product_agent_os.analysis_artifact_renderer import render_first_run_analysis_artifact  # noqa: PLC0415

        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "sample-target"
            workspace.mkdir()
            packet = build_packet(
                target_label="SOL 0.6",
                generated_at="2026-06-18T15:00:00+03:00",
                source_artifacts=[],
                generated_pages=[],
                section_summaries={
                    "discovery": {"status": "current", "unsupported_claims": []},
                    "runtime_route": {"status": "not_available", "unsupported_claims": []},
                    "methodology_audit": {"status": "not_available", "unsupported_claims": []},
                    "control_plane": {"status": "not_available", "unsupported_claims": []},
                    "source_policy": {"status": "not_available", "unsupported_claims": []},
                    "graph": {"status": "not_available", "unsupported_claims": []},
                    "status_snapshot": {"status": "not_available", "unsupported_claims": []},
                },
                safe_next_action="Continue.",
            )
            packet["target"]["target_ref"] = r"C:\Users\user\private"

            with self.assertRaises(ValueError):
                render_first_run_analysis_artifact(packet, workspace)
            self.assertFalse((workspace / ".codex" / "product-agent-os" / "analysis").exists())

    def test_m20_5_manifest_records_digest_maps_and_previous_baseline_diff(self) -> None:
        _schema, build_packet, _validate_packet = _load_contract()
        from product_agent_os.analysis_artifact_renderer import (  # noqa: PLC0415
            FIRST_RUN_ANALYSIS_PAGE_IDS,
            render_first_run_analysis_artifact,
        )

        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "sample-target"
            workspace.mkdir()
            first_packet = build_packet(
                target_label="SOL 0.6",
                generated_at="2026-06-18T16:00:00+03:00",
                source_artifacts=[
                    {
                        "artifact_id": "discovery",
                        "path": "docs/superpowers/specs/discovery.json",
                        "digest": "sha256:" + "1" * 64,
                        "evidence_status": "current",
                        "provenance": "product_agent_os.discovery",
                    }
                ],
                generated_pages=[],
                section_summaries={
                    "discovery": {"status": "current", "unsupported_claims": []},
                    "runtime_route": {"status": "approval_required", "unsupported_claims": ["live runtime not run"]},
                    "methodology_audit": {"status": "present_unverified", "unsupported_claims": []},
                    "control_plane": {"status": "present_unverified", "unsupported_claims": []},
                    "source_policy": {"status": "present_unverified", "unsupported_claims": []},
                    "graph": {"status": "not_available", "unsupported_claims": ["graph not generated"]},
                    "status_snapshot": {"status": "not_available", "unsupported_claims": []},
                },
                safe_next_action="Continue with baseline digest support.",
            )
            render_first_run_analysis_artifact(first_packet, workspace)
            analysis_dir = workspace / ".codex" / "product-agent-os" / "analysis"
            first_manifest = json.loads((analysis_dir / "analysis-manifest.json").read_text(encoding="utf-8"))

            second_packet = build_packet(
                target_label="SOL 0.6",
                generated_at="2026-06-18T16:05:00+03:00",
                source_artifacts=[
                    {
                        "artifact_id": "discovery",
                        "path": "docs/superpowers/specs/discovery.json",
                        "digest": "sha256:" + "2" * 64,
                        "evidence_status": "current",
                        "provenance": "product_agent_os.discovery",
                    },
                    {
                        "artifact_id": "runtime_route",
                        "path": "docs/superpowers/specs/runtime-route.json",
                        "digest": "sha256:" + "3" * 64,
                        "evidence_status": "approval_required",
                        "provenance": "codex_runtime_runner.cli",
                    },
                ],
                generated_pages=[],
                section_summaries=first_packet["section_summaries"],
                safe_next_action="Review changed baseline before continuing.",
            )
            render_first_run_analysis_artifact(second_packet, workspace)
            second_manifest = json.loads((analysis_dir / "analysis-manifest.json").read_text(encoding="utf-8"))

            self.assertEqual(second_manifest["renderer_version"], 1)
            self.assertEqual(second_manifest["previous_baseline"]["status"], "compared")
            self.assertEqual(second_manifest["previous_baseline"]["manifest_digest"], first_manifest["manifest_digest"])
            self.assertTrue(second_manifest["target_fingerprint"].startswith("sha256:"))
            self.assertEqual(sorted(second_manifest["page_digests"]), sorted(FIRST_RUN_ANALYSIS_PAGE_IDS))
            self.assertEqual(second_manifest["source_digests"]["discovery"], "sha256:" + "2" * 64)
            self.assertEqual(second_manifest["source_digests"]["runtime_route"], "sha256:" + "3" * 64)
            self.assertEqual(second_manifest["change_summary"]["added_sources"], ["runtime_route"])
            self.assertEqual(second_manifest["change_summary"]["changed_sources"], ["discovery"])
            self.assertEqual(second_manifest["change_summary"]["removed_sources"], [])
            self.assertTrue(second_manifest["change_summary"]["changed_pages"])
            self.assertNotIn(str(workspace), json.dumps(second_manifest, ensure_ascii=False, sort_keys=True))

    def test_m20_6_manifest_records_redaction_report_and_source_policy_gate(self) -> None:
        _schema, build_packet, _validate_packet = _load_contract()
        from product_agent_os.analysis_artifact_renderer import render_first_run_analysis_artifact  # noqa: PLC0415

        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "sample-target"
            workspace.mkdir()
            packet = build_packet(
                target_label="SOL 0.6",
                generated_at="2026-06-18T17:00:00+03:00",
                source_artifacts=[
                    {
                        "artifact_id": "source_policy",
                        "path": "docs/superpowers/specs/source-policy.json",
                        "digest": "sha256:" + "4" * 64,
                        "evidence_status": "approval_required",
                        "provenance": "source_policy_validator",
                    }
                ],
                generated_pages=[],
                section_summaries={
                    "discovery": {"status": "current", "unsupported_claims": []},
                    "runtime_route": {"status": "approval_required", "unsupported_claims": ["live runtime not run"]},
                    "methodology_audit": {"status": "present_unverified", "unsupported_claims": []},
                    "control_plane": {"status": "present_unverified", "unsupported_claims": []},
                    "source_policy": {
                        "status": "approval_required",
                        "unsupported_claims": ["apply blocked until source policy is approved"],
                        "accepted_gaps": ["diagnostic artifact remains allowed"],
                    },
                    "graph": {"status": "not_available", "unsupported_claims": ["graph not generated"]},
                    "status_snapshot": {"status": "not_available", "unsupported_claims": []},
                },
                safe_next_action="Review diagnostic artifact; do not apply or promote.",
            )

            render_first_run_analysis_artifact(packet, workspace)
            manifest = json.loads(
                (workspace / ".codex" / "product-agent-os" / "analysis" / "analysis-manifest.json").read_text(
                    encoding="utf-8"
                )
            )

            self.assertEqual(manifest["redaction_report"]["status"], "passed_redacted")
            self.assertEqual(manifest["redaction_report"]["blocked_categories"]["local_absolute_path"], 0)
            self.assertEqual(manifest["redaction_report"]["blocked_categories"]["raw_source_field"], 0)
            self.assertEqual(manifest["redaction_report"]["blocked_categories"]["secret_like_value"], 0)
            self.assertEqual(manifest["source_policy_gate"]["status"], "approval_required")
            self.assertFalse(manifest["source_policy_gate"]["apply_allowed"])
            self.assertFalse(manifest["source_policy_gate"]["promotion_allowed"])
            self.assertTrue(manifest["source_policy_gate"]["diagnostic_artifact_allowed"])

    def test_m20_6_renderer_blocks_secret_like_values_before_writing_pages(self) -> None:
        _schema, build_packet, validate_packet = _load_contract()
        from product_agent_os.analysis_artifact_renderer import render_first_run_analysis_artifact  # noqa: PLC0415

        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "sample-target"
            workspace.mkdir()
            packet = build_packet(
                target_label="SOL 0.6",
                generated_at="2026-06-18T17:05:00+03:00",
                source_artifacts=[],
                generated_pages=[],
                section_summaries={
                    "discovery": {"status": "current", "unsupported_claims": []},
                    "runtime_route": {"status": "not_available", "unsupported_claims": []},
                    "methodology_audit": {"status": "not_available", "unsupported_claims": []},
                    "control_plane": {"status": "not_available", "unsupported_claims": []},
                    "source_policy": {"status": "not_available", "unsupported_claims": []},
                    "graph": {"status": "not_available", "unsupported_claims": []},
                    "status_snapshot": {"status": "not_available", "unsupported_claims": []},
                },
                safe_next_action="Continue.",
            )
            packet["safe_next_action"] = "Use sk-proj-abcdefghijklmnopqrstuvwxyz1234567890 for setup."

            self.assertIn("secret-like value retained", validate_packet(packet))
            with self.assertRaises(ValueError):
                render_first_run_analysis_artifact(packet, workspace)
            self.assertFalse((workspace / ".codex" / "product-agent-os" / "analysis").exists())

    def test_graph_depth_artifact_pack_projects_graph_packets_into_first_run_html_without_proof_claims(self) -> None:
        _schema, build_packet, validate_packet = _load_contract()
        from product_agent_os.analysis_artifact_renderer import render_first_run_analysis_artifact  # noqa: PLC0415

        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "sample-target"
            workspace.mkdir()
            packet = build_packet(
                target_label="SOL 0.6",
                generated_at="2026-06-18T21:00:00+03:00",
                source_artifacts=[
                    {
                        "artifact_id": "project_graph",
                        "path": ".codex/product-agent-os/project-code-graph.json",
                        "digest": "sha256:" + "7" * 64,
                        "evidence_status": "inspection_only",
                        "provenance": "scan_project_code_graph",
                    }
                ],
                generated_pages=[],
                section_summaries={
                    "discovery": {"status": "current", "unsupported_claims": []},
                    "runtime_route": {"status": "approval_required", "unsupported_claims": ["live runtime not run"]},
                    "methodology_audit": {"status": "present_unverified", "unsupported_claims": []},
                    "control_plane": {"status": "present_unverified", "unsupported_claims": []},
                    "source_policy": {"status": "present_unverified", "unsupported_claims": []},
                    "graph": {"status": "inspection_only", "unsupported_claims": ["graph is orientation evidence only"]},
                    "status_snapshot": {"status": "inspection_only", "unsupported_claims": []},
                },
                safe_next_action="Use graph packet as orientation only; read source files before edits.",
                graph_artifact_summary={
                    "status": "inspection_only",
                    "graph_packet_digest": "sha256:" + "8" * 64,
                    "agent_packet_refs": [
                        {
                            "kind": "agent_reading_packet",
                            "path": ".codex/product-agent-os/agent-reading-packet.json",
                            "digest": "sha256:" + "9" * 64,
                        }
                    ],
                    "coverage": {
                        "status": "partial_static",
                        "covered_files": 4,
                        "partial_files": 1,
                        "unsupported_languages": {"ruby": "unsupported"},
                    },
                    "freshness": {
                        "status": "stale",
                        "blocks_action_claims": True,
                        "safe_next_action": "Refresh graph or read source first.",
                    },
                    "rejected_link_summary": {"total": 2, "by_reason": {"weak_name_similarity": 2}},
                    "framework_semantic_summary": {"total": 3, "frameworks": {"react": 2, "next": 1}},
                    "guided_tour": [
                        {"page": "code-intelligence", "safe_next_action": "Read listed spans before editing."}
                    ],
                    "unsupported_claims": ["release_readiness", "runtime_routing", "source_read_completion"],
                },
            )

            self.assertEqual(validate_packet(packet), [])
            self.assertEqual(packet["graph_artifact_summary"]["generated_view_policy"], "orientation_only_not_proof")
            self.assertTrue(packet["graph_artifact_summary"]["freshness"]["blocks_action_claims"])

            render_first_run_analysis_artifact(packet, workspace)
            analysis_dir = workspace / ".codex" / "product-agent-os" / "analysis"
            graph_html = (analysis_dir / "graph.html").read_text(encoding="utf-8")
            index_html = (analysis_dir / "index.html").read_text(encoding="utf-8")
            manifest = json.loads((analysis_dir / "analysis-manifest.json").read_text(encoding="utf-8"))
            rendered = graph_html + index_html + json.dumps(manifest, sort_keys=True)

            self.assertEqual(manifest["graph_artifact_summary"]["status"], "inspection_only")
            self.assertEqual(manifest["graph_artifact_summary"]["freshness"]["status"], "stale")
            self.assertIn("Graph Packet Summary", graph_html)
            self.assertIn("Coverage", graph_html)
            self.assertIn("Freshness", graph_html)
            self.assertIn("Rejected Links", graph_html)
            self.assertIn("Framework Hints", graph_html)
            self.assertIn("Guided Tour", graph_html)
            self.assertIn("orientation evidence only", rendered)
            self.assertNotIn("release-ready", rendered.lower())
            self.assertNotIn("production-ready", rendered.lower())
            self.assertNotIn("runtime route verified", rendered.lower())
            self.assertNotIn(str(workspace), rendered)


if __name__ == "__main__":
    unittest.main()
