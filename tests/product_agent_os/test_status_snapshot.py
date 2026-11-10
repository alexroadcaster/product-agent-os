import json
import sys
import hashlib
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.status_snapshot import build_status_snapshot  # noqa: E402


class StatusSnapshotTest(unittest.TestCase):
    def test_split_plan_preserves_nine_sources_with_bounded_reader(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'research').mkdir()
            sources = []
            for index in range(9):
                path = root / f'research/part-{index}.md'
                path.write_bytes(f'### Task `T{index}`\n- Status: planned\n#### Completion Report\n- status: planned\n'.encode())
                sources.append({'path': path.relative_to(root).as_posix(),
                                'revision': 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()})
            def write_pointer(refs):
                (root / 'PLAN.md').write_text('<!-- product-agent-os:current-state:start -->\n```json\n'
                    + json.dumps({'schema_version': 1, 'sources': refs})
                    + '\n```\n<!-- product-agent-os:current-state:end -->', encoding='utf-8')
            write_pointer(sources)
            result = build_status_snapshot(workspace=root, generated_at='2026-11-10T00:00:00Z')['current_state']
            self.assertEqual(result['status'], 'projected')
            self.assertEqual({row['task_id'] for row in result['tasks']}, {f'T{i}' for i in range(9)})
            write_pointer((sources * 4)[:33])
            self.assertIn('invalid_current_sources', build_status_snapshot(workspace=root, generated_at='2026-11-10T00:00:00Z')['current_state']['issues'])

    def _current_workspace(self, root, document):
        source = root / 'docs/superpowers/specs/tasks.json'
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(json.dumps(document), encoding='utf-8')
        pointer = {'schema_version': 1, 'sources': [{'path': source.relative_to(root).as_posix(), 'revision': 'sha256:'+hashlib.sha256(source.read_bytes()).hexdigest()}]}
        (root / 'PLAN.md').write_text('<!-- product-agent-os:current-state:start -->\n```json\n'+json.dumps(pointer)+'\n```\n<!-- product-agent-os:current-state:end -->\n\n## Current historical\nOld planned record.\n', encoding='utf-8')
        return source

    def test_current_execution_overrides_historical_planned_with_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self._current_workspace(root, {'generated_at':'2026-06-19T00:00:00Z', 'tasks':[{'id':'B42-S2-M04','status':'planned','execution_evidence':{'checked_at':'2026-11-05','status':'implemented_locally_verified_explicit_only'}}]})
            result=build_status_snapshot(workspace=root, generated_at='2026-11-09T00:00:00Z')['current_state']
            self.assertEqual(result['status'],'projected')
            task=result['tasks'][0]
            self.assertEqual(task['task_state'],'implemented')
            self.assertEqual(task['verification_state'],'locally_verified')
            self.assertEqual(task['acceptance_state'],'unknown')
            self.assertEqual(task['historical_status'],'planned')
            self.assertEqual(task['selected_evidence'],'execution_evidence')
            self.assertTrue(task['source_revision'].startswith('sha256:'))

    def test_current_projection_rejects_stale_revision_without_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); source=self._current_workspace(root, {'tasks':[{'id':'T1','status':'planned'}]})
            source.write_text('{"tasks":[]}', encoding='utf-8')
            result=build_status_snapshot(workspace=root, generated_at='2026-11-09T00:00:00Z')['current_state']
            self.assertEqual(result['status'],'unknown')
            self.assertEqual(result['tasks'],[])
            self.assertIn('source_revision_mismatch',result['issues'])

    def test_equal_new_receipts_conflict_and_unknown_timestamps_fail_closed(self):
        receipts=[{'checked_at':'2026-11-05','status':'implemented'},{'checked_at':'2026-11-05','status':'planned'}]
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for evidence,expected in [(receipts,'conflict'), ({'status':'implemented'},'unknown'), ({'checked_at':'2030-01-01','status':'implemented'},'unknown')]:
                self._current_workspace(root, {'generated_at':'2026-06-19', 'tasks':[{'id':'T1','status':'planned','execution_evidence':evidence}]})
                result=build_status_snapshot(workspace=root, generated_at='2026-11-09T00:00:00Z')['current_state']
                self.assertEqual(result['status'],expected)
                self.assertEqual(result['tasks'][0]['task_state'],expected)

    def test_current_pointer_unknown_unsafe_and_duplicate_ownership(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.assertEqual(build_status_snapshot(workspace=root,generated_at='2026-11-09T00:00:00Z')['current_state']['status'],'unknown')
            self._current_workspace(root,{'tasks':[{'id':'T1','status':'implemented'},{'id':'T1','status':'planned'}]})
            result=build_status_snapshot(workspace=root, generated_at='2026-11-09T00:00:00Z')['current_state']
            self.assertEqual(result['status'],'conflict')
            plan=root/'PLAN.md'
            plan.write_text(plan.read_text(encoding='utf-8').replace('docs/superpowers/specs/tasks.json','../outside.json'),encoding='utf-8')
            result=build_status_snapshot(workspace=root, generated_at='2026-11-09T00:00:00Z')['current_state']
            self.assertEqual(result['status'],'unknown')
            self.assertEqual(result['tasks'],[])

    def test_snapshot_undated_and_future_evidence_are_not_current(self):
        for item,status in [({'status':'ok'},'unknown'),({'recorded_at':'2030-01-01T00:00:00Z'},'future'),({'recorded_at':'2026-11-08T00:00:00'},'unknown')]:
            snapshot=build_status_snapshot(runtime_result={'status':'completed','verification_evidence':[item]},generated_at='2026-11-09T00:00:00Z')
            self.assertEqual(snapshot['evidence_summary']['freshness'],status)
            self.assertIn('completion status lacks current verification evidence',snapshot['readiness_summary']['warnings'])

    def test_current_markdown_projection_and_dashboard_wiring_are_read_only(self):
        import importlib.util
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); source=self._current_workspace(root, {'tasks':[]})
            source.unlink()
            source=root/'research/tasks.md'; source.parent.mkdir()
            source.write_text('### Task `T1`\n- Status: implemented\n#### Completion Report\n- status: implemented\n',encoding='utf-8')
            pointer={'schema_version':1,'sources':[{'path':'research/tasks.md','revision':'sha256:'+hashlib.sha256(source.read_bytes()).hexdigest()}]}
            (root/'PLAN.md').write_text('<!-- product-agent-os:current-state:start -->\n```json\n'+json.dumps(pointer)+'\n```\n<!-- product-agent-os:current-state:end -->',encoding='utf-8')
            before={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
            spec=importlib.util.spec_from_file_location('g3_status_cli',SCRIPTS/'render_status_dashboard.py')
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            snapshot=module._snapshot_for_workspace(root)
            row=snapshot['current_state']['tasks'][0]
            self.assertEqual(row['task_state'],'implemented')
            self.assertEqual(row['verification_state'],'not_verified')
            self.assertEqual(row['acceptance_state'],'unknown')
            self.assertEqual(before,{p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()})

    def test_stale_receipt_does_not_override_newer_source_and_dimensions_are_separate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self._current_workspace(root,{'checked_at':'2026-11-06','tasks':[{'id':'T1','status':'implemented','execution_evidence':{'checked_at':'2026-11-05','status':'planned'},'run_status':'failed','acceptance_status':'needs_user_acceptance'}]})
            row=build_status_snapshot(workspace=root,generated_at='2026-11-09T00:00:00Z')['current_state']['tasks'][0]
            self.assertEqual(row['task_state'],'implemented')
            self.assertEqual(row['run_state'],'failed')
            self.assertEqual(row['verification_state'],'not_verified')
            self.assertEqual(row['acceptance_state'],'needs_user_acceptance')

    def test_pointer_scope_preserves_canonical_owner_over_planning_cross_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            source=self._current_workspace(root,{'tasks':[{'id':'AUD-1','status':'planned'},{'id':'B45-T30','status':'planned'}]})
            canonical=source.with_name('canonical.json')
            canonical.write_text(json.dumps({'tasks':[{'id':'B45-T30','status':'implemented'}]}),encoding='utf-8')
            pointer={'schema_version':1,'sources':[
                {'path':source.relative_to(root).as_posix(),'revision':'sha256:'+hashlib.sha256(source.read_bytes()).hexdigest(),'task_prefixes':['AUD-']},
                {'path':canonical.relative_to(root).as_posix(),'revision':'sha256:'+hashlib.sha256(canonical.read_bytes()).hexdigest()}]}
            (root/'PLAN.md').write_text('<!-- product-agent-os:current-state:start -->\n```json\n'+json.dumps(pointer)+'\n```\n<!-- product-agent-os:current-state:end -->',encoding='utf-8')
            result=build_status_snapshot(workspace=root,generated_at='2026-11-09T00:00:00Z')['current_state']
            self.assertEqual(result['status'],'projected')
            self.assertEqual(len(result['tasks']),2)
            self.assertEqual(result['tasks'][1]['task_state'],'implemented')
            self.assertEqual(result['tasks'][1]['source_path'],canonical.relative_to(root).as_posix())

    def test_status_snapshot_summarizes_runtime_renderer_manifest_and_ledgers_without_raw_paths(self):
        runtime_result = {
            "status": "needs_approval",
            "workspace": "C:\\Users\\person\\private-project",
            "lifecycle_state": "quality_gate",
            "route_packet": {
                "write_policy": "read_only",
                "usage_mode": {"primary": "security_sensitive_change", "confidence": "high"},
                "question_queue": {
                    "summary": {"total": 3, "blocking": 1, "recommended": 2, "optional": 0, "remaining": 2},
                    "next_blocking_question": {
                        "id": "q_approval_synthetic",
                        "text": "Who approves the external write?",
                        "priority": "blocking",
                    },
                },
                "first_response_contract": {
                    "safe_next_action": "Stage approval-record.md before external mutation.",
                    "next_blocking_question": {"id": "q_approval_synthetic"},
                    "question_counts": {"total": 3, "blocking": 1, "recommended": 2, "optional": 0, "remaining": 2},
                    "question_summary": ["1 blocking question", "2 recommended questions", "0 optional questions"],
                },
                "methodology_packet": self._methodology_packet(),
            },
            "approval_status": "required",
            "verification_evidence": [],
            "redactions": {"count": 0, "categories": []},
        }
        renderer_result = {
            "infrastructure_plan": {"status": "needs_approval"},
            "rendered_artifacts": {
                "mode": "stage",
                "files": [
                    {
                        "target_path": "AGENTS.md",
                        "staged_path": "C:\\Users\\person\\stage\\AGENTS.md",
                        "action": "create",
                    },
                    {
                        "target_path": ".codex/artifact-templates/question-ledger.md",
                        "staged_path": "C:\\Users\\person\\stage\\.codex\\artifact-templates\\question-ledger.md",
                        "action": "create",
                    },
                ],
                "validation": {"ok": True, "errors": {}},
            },
        }
        stage_manifest = {
            "workspace": "C:\\Users\\person\\private-project",
            "workspace_audit_digest": "sha256:" + "a" * 64,
            "infrastructure_plan_digest": "sha256:" + "b" * 64,
            "files": [
                {
                    "target_path": "AGENTS.md",
                    "staged_path": "C:\\Users\\person\\stage\\AGENTS.md",
                    "digest": "sha256:" + "c" * 64,
                }
            ],
        }
        question_ledger = {
            "summary": {"accepted": 1, "blocked": 0, "unanswered": 2, "total": 3},
            "artifact_updates": [{"artifact": "approval-record.md", "question_ids": ["q_approval_synthetic"]}],
        }

        snapshot = build_status_snapshot(
            runtime_result=runtime_result,
            renderer_result=renderer_result,
            stage_manifest=stage_manifest,
            question_ledger=question_ledger,
            generated_at="2026-05-28T10:00:00+00:00",
        )
        serialized = json.dumps(snapshot, sort_keys=True)

        self.assertEqual(snapshot["schema_version"], 1)
        self.assertEqual(snapshot["write_policy"], "read_only")
        self.assertEqual(snapshot["generated_at"], "2026-05-28T10:00:00+00:00")
        self.assertEqual(snapshot["workspace"], "[REDACTED_LOCAL_PATH]")
        self.assertEqual(snapshot["lifecycle_state"], "quality_gate")
        self.assertEqual(snapshot["usage_mode"]["primary"], "security_sensitive_change")
        self.assertEqual(snapshot["question_summary"]["blocking"], 1)
        self.assertEqual(snapshot["readiness_summary"]["status"], "needs_approval")
        self.assertEqual(snapshot["evidence_summary"]["freshness"], "missing")
        self.assertEqual(snapshot["next_safe_action"], "Stage approval-record.md before external mutation.")
        self.assertEqual(snapshot["dashboard_policy"]["source_of_truth"], "underlying_artifacts")
        self.assertEqual(snapshot["dashboard_policy"]["write_policy"], "read_only")
        self.assertEqual(snapshot["renderer_file_count"], 2)
        self.assertEqual(
            snapshot["manifest_digests"]["workspace_audit_digest"],
            "sha256:" + "a" * 64,
        )
        self.assertEqual(snapshot["manifest_digests"]["file_count"], 1)
        self.assertEqual(
            snapshot["source_artifact_ledger"],
            [{"artifact": "approval-record.md", "decision": "canonical_template"}],
        )
        self.assertEqual(
            snapshot["semantic_evidence_sufficiency"]["status"],
            "present_unverified",
        )
        self.assertEqual(snapshot["question_ledger_summary"]["accepted"], 1)
        self.assertIn("absolute_path", snapshot["redaction_summary"]["categories"])
        self.assertNotIn("C:\\Users\\person", serialized)
        self.assertNotIn("private-project", serialized)
        self.assertNotIn("staged_path", serialized)

    def test_snapshot_marks_inspection_only_and_stale_evidence_without_success_claims(self):
        runtime_result = {
            "status": "completed",
            "workspace": "C:\\Users\\person\\inspection-only",
            "lifecycle_state": "maintenance",
            "route_packet": {
                "usage_mode": {"primary": "inspection_only", "confidence": "high"},
                "question_queue": {
                    "summary": {"total": 0, "blocking": 0, "recommended": 0, "optional": 0, "remaining": 0},
                    "next_blocking_question": None,
                },
                "first_response_contract": {
                    "safe_next_action": "Record read-only audit findings.",
                    "question_counts": {"total": 0, "blocking": 0, "recommended": 0, "optional": 0, "remaining": 0},
                    "question_summary": ["0 blocking questions", "0 recommended questions", "0 optional questions"],
                },
                "methodology_packet": self._methodology_packet(status="present_unverified"),
            },
            "verification_evidence": [
                {"command": "python -m unittest", "status": "ok", "recorded_at": "2026-04-01T00:00:00+00:00"}
            ],
            "approval_status": "not_required",
        }

        snapshot = build_status_snapshot(
            runtime_result=runtime_result,
            generated_at="2026-05-28T10:00:00+00:00",
            evidence_max_age_days=14,
        )
        serialized = json.dumps(snapshot, sort_keys=True).lower()

        self.assertEqual(snapshot["usage_mode"]["primary"], "inspection_only")
        self.assertTrue(snapshot["usage_mode"]["inspection_only"])
        self.assertEqual(snapshot["evidence_summary"]["freshness"], "stale")
        self.assertEqual(snapshot["readiness_summary"]["success_claim"], "not_claimed")
        self.assertEqual(snapshot["readiness_summary"]["status"], "inspection_only")
        self.assertIn("stale evidence", snapshot["readiness_summary"]["warnings"])
        self.assertIn("inspection-only evidence cannot prove completion", snapshot["readiness_summary"]["warnings"])
        self.assertNotIn("tests pass", serialized)
        self.assertNotIn("checks passed", serialized)
        self.assertNotIn("success", snapshot["readiness_summary"]["status"])

    def test_snapshot_redacts_secret_and_private_data_from_nested_packets(self):
        runtime_result = {
            "status": "route_ready",
            "workspace": "C:\\Users\\person\\project",
            "lifecycle_state": "quality_gate",
            "route_packet": {
                "usage_mode": {"primary": "standard_feature", "confidence": "medium"},
                "question_queue": {
                    "summary": {"total": 1, "blocking": 1, "recommended": 0, "optional": 0, "remaining": 0},
                    "next_blocking_question": {"id": "q_secret", "text": "TOKEN=fixture-secret"},
                },
                "first_response_contract": {
                    "safe_next_action": "Inspect C:\\Users\\person\\project and raw private chat log.",
                    "question_counts": {"total": 1, "blocking": 1, "recommended": 0, "optional": 0, "remaining": 0},
                    "question_summary": ["1 blocking question"],
                },
            },
            "verification_evidence": ["TOKEN=fixture-secret"],
        }

        snapshot = build_status_snapshot(
            runtime_result=runtime_result,
            generated_at="2026-05-28T10:00:00+00:00",
        )
        serialized = json.dumps(snapshot, sort_keys=True)

        self.assertNotIn("fixture-secret", serialized)
        self.assertNotIn("raw private chat log", serialized)
        self.assertNotIn("C:\\Users\\person", serialized)
        self.assertIn("secret", snapshot["redaction_summary"]["categories"])
        self.assertIn("private_data", snapshot["redaction_summary"]["categories"])
        self.assertIn("absolute_path", snapshot["redaction_summary"]["categories"])

    def test_snapshot_includes_bounded_metrics_loop_summary_and_report_refs(self):
        runtime_result = {
            "status": "route_ready",
            "workspace": "C:\\Users\\person\\metrics-loop",
            "lifecycle_state": "quality_gate",
            "route_packet": {
                "usage_mode": {"primary": "maintenance", "confidence": "medium"},
                "agent_skill_metrics_loop": {
                    "status": "present_unverified",
                    "summary": {
                        "target_count": 12,
                        "overall_status": "blocked_by_guardrail",
                        "cadence_level": "L2",
                    },
                    "report_refs": [
                        {
                            "kind": "staged_artifact",
                            "path": ".codex/eval-reports/agent-skill-evaluation-report.html",
                            "digest": "sha256:" + "a" * 64,
                        },
                        {
                            "kind": "external_ref",
                            "path": "https://example.invalid/report.html",
                        },
                    ],
                    "update_candidate_summary": {
                        "candidate_count": 9,
                        "top_candidates": [
                            {"candidate_id": f"candidate-{index}", "requires_rollback": True}
                            for index in range(8)
                        ],
                    },
                    "unsafe_extra": "TOKEN=fixture-secret C:\\Users\\person\\metrics-loop",
                },
            },
            "verification_evidence": [],
        }

        snapshot = build_status_snapshot(
            runtime_result=runtime_result,
            generated_at="2026-05-28T10:00:00+00:00",
        )
        serialized = json.dumps(snapshot, sort_keys=True)

        summary = snapshot["agent_skill_metrics_loop"]
        self.assertEqual(summary["status"], "present_unverified")
        self.assertEqual(summary["summary"]["target_count"], 12)
        self.assertEqual(summary["summary"]["cadence_level"], "L2")
        self.assertEqual(summary["report_refs"][0]["path"], ".codex/eval-reports/agent-skill-evaluation-report.html")
        self.assertEqual(len(summary["report_refs"]), 1)
        self.assertEqual(len(summary["update_candidate_summary"]["top_candidates"]), 5)
        self.assertEqual(summary["source_policy"], "generated summaries are not source of truth")
        self.assertNotIn("fixture-secret", serialized)
        self.assertNotIn("C:\\Users\\person", serialized)
        self.assertNotIn("https://example.invalid", serialized)

    def test_snapshot_includes_completion_skeptic_projection_without_raw_ledgers(self):
        runtime_result = {
            "status": "route_ready",
            "workspace": "C:\\Users\\person\\doubt-project",
            "lifecycle_state": "quality_gate",
            "route_packet": {
                "usage_mode": {"primary": "maintenance", "confidence": "medium"},
                "completion_skeptic_recommendation": {
                    "schema_version": 1,
                    "write_policy": "read_only",
                    "status": "recommended",
                    "recommended_skill": "completion-skeptic",
                    "trigger_level": "recommended",
                    "trigger_sources": ["completion_claim"],
                    "risk_classes": ["verification_gap"],
                    "reasons": ["completion claim needs a second-pass evidence check"],
                    "skip_reasons": [],
                    "artifact_under_review": {
                        "kind": "runtime_result",
                        "path": ".codex/product-agent-os/status.json",
                        "label": "status snapshot",
                    },
                    "artifact_type": "plugin_skill",
                    "required_evidence": ["current command evidence", "source artifact ledger", "accepted gaps"],
                    "evidence_summary": {
                        "required": 3,
                        "available": 1,
                        "missing": 1,
                        "stale": 0,
                        "approval_required": 0,
                        "accepted_gap": 1,
                    },
                    "approval_boundary": {"status": "not_required", "hits": []},
                    "packet_ref": {
                        "kind": "staged_artifact",
                        "path": ".codex/product-agent-os/doubt-verification-packet.json",
                        "digest": "sha256:" + "a" * 64,
                    },
                    "safe_next_action": "Run completion-skeptic before claiming completion.",
                    "source_policy": "completion skeptic recommendation is generated routing guidance, not source of truth",
                    "redaction_status": {"status": "clean", "categories": []},
                    "claim_ledger": [{"raw": "must not project"}],
                    "unsafe_extra": "TOKEN=fixture-secret C:\\Users\\person\\doubt-project",
                },
            },
            "verification_evidence": [],
        }

        snapshot = build_status_snapshot(
            runtime_result=runtime_result,
            generated_at="2026-06-09T12:00:00+03:00",
        )
        serialized = json.dumps(snapshot, sort_keys=True)
        summary = snapshot["completion_skeptic"]

        self.assertEqual(summary["status"], "recommended")
        self.assertEqual(summary["trigger_level"], "recommended")
        self.assertEqual(summary["recommended_skill"], "completion-skeptic")
        self.assertEqual(summary["evidence_summary"]["missing"], 1)
        self.assertEqual(summary["evidence_summary"]["accepted_gap"], 1)
        self.assertEqual(summary["packet_ref"]["path"], ".codex/product-agent-os/doubt-verification-packet.json")
        self.assertEqual(
            summary["source_policy"],
            "completion skeptic recommendation is generated routing guidance, not source of truth",
        )
        self.assertNotIn("claim_ledger", summary)
        self.assertNotIn("fixture-secret", serialized)
        self.assertNotIn("C:\\Users\\person", serialized)

    def test_snapshot_includes_bounded_project_graph_summary_and_never_claims_graph_as_truth(self):
        runtime_result = {
            "status": "route_ready",
            "workspace": "C:\\Users\\person\\graph-project",
            "lifecycle_state": "quality_gate",
            "route_packet": {
                "usage_mode": {"primary": "maintenance", "confidence": "medium"},
                "project_graph_status": {
                    "schema_version": 1,
                    "write_policy": "read_only",
                    "status": "stale",
                    "freshness": {"status": "stale", "scan_id": "scan-old", "as_of": "2026-05-01T00:00:00+00:00"},
                    "counts": {"nodes": 1000, "edges": 2000, "observations": 3000, "omitted_nodes": 750},
                    "unsupported_languages": [
                        {
                            "language": "typescript",
                            "file_count": 20,
                            "status": "file_only",
                            "raw_source": "def charge_card(): pass",
                        }
                    ],
                    "artifact_refs": [
                        {
                            "kind": "staged_artifact",
                            "path": ".codex/product-agent-os/project-code-graph.json",
                            "digest": "sha256:" + "a" * 64,
                        },
                        {"kind": "external_ref", "path": "https://example.invalid/graph.json"},
                        {"kind": "staged_artifact", "path": "D:/private/project/graph.json"},
                    ],
                    "top_gaps": [
                        {
                            "id": f"gap-{index}",
                            "severity": "medium",
                            "safe_next_action": "Read source files before acting.",
                        }
                        for index in range(10)
                    ],
                    "safe_next_action": "Use graph as orientation only; read source files before edits.",
                    "source_policy": "generated graph is not source of truth",
                    "nodes": [{"id": "file:C:\\Users\\person\\graph-project\\app.py"}],
                    "edges": [{"source": "a", "target": "b"}],
                },
            },
            "verification_evidence": [],
        }

        snapshot = build_status_snapshot(
            runtime_result=runtime_result,
            generated_at="2026-06-01T00:00:00+00:00",
        )
        serialized = json.dumps(snapshot, sort_keys=True)
        graph_summary = snapshot["project_graph_summary"]

        self.assertEqual(graph_summary["status"], "stale")
        self.assertEqual(graph_summary["counts"]["nodes"], 1000)
        self.assertEqual(graph_summary["unsupported_languages"][0]["language"], "typescript")
        self.assertNotIn("raw_source", graph_summary["unsupported_languages"][0])
        self.assertEqual(len(graph_summary["artifact_refs"]), 1)
        self.assertEqual(len(graph_summary["top_gaps"]), 5)
        self.assertEqual(graph_summary["source_policy"], "generated graph is not source of truth")
        self.assertIn("stale project graph", snapshot["readiness_summary"]["warnings"])
        self.assertNotIn("nodes", graph_summary)
        self.assertNotIn("edges", graph_summary)
        self.assertNotIn("https://example.invalid", serialized)
        self.assertNotIn("D:/private", serialized)
        self.assertNotIn("charge_card", serialized)
        self.assertNotIn("C:\\Users\\person", serialized)
        self.assertNotIn("graph-project", serialized)

    def test_snapshot_projects_graph_depth_packet_summary_without_generated_view_as_proof(self):
        runtime_result = {
            "status": "route_ready",
            "workspace": "C:\\Users\\person\\graph-depth-project",
            "route_packet": {
                "usage_mode": {"primary": "maintenance", "confidence": "medium"},
                "project_graph_status": {
                    "schema_version": 1,
                    "write_policy": "read_only",
                    "status": "current",
                    "freshness": {
                        "status": "partial",
                        "blocks_action_claims": True,
                        "safe_next_action": "Refresh graph or read source files before edits.",
                    },
                    "counts": {"nodes": 10, "edges": 11, "observations": 12, "omitted_nodes": 0},
                    "coverage_map": {
                        "status": "partial_static",
                        "covered_files": 7,
                        "partial_files": 2,
                        "unsupported_languages": {"ruby": "unsupported"},
                        "raw_source": "must not project",
                    },
                    "rejected_link_summary": {"total": 2, "by_reason": {"weak_name_similarity": 2}},
                    "framework_semantic_summary": {"total": 3, "frameworks": {"react": 2, "next": 1}},
                    "agent_packet_refs": [
                        {
                            "kind": "agent_reading_packet",
                            "path": ".codex/product-agent-os/agent-reading-packet.json",
                            "digest": "sha256:" + "b" * 64,
                        },
                        {"kind": "external_ref", "path": "https://example.invalid/packet.json"},
                    ],
                    "safe_next_action": "Use graph as orientation only; read source files before edits.",
                    "source_policy": "generated graph is not source of truth",
                    "nodes": [{"id": "file:C:\\Users\\person\\graph-depth-project\\app.py"}],
                },
            },
            "verification_evidence": [],
        }

        snapshot = build_status_snapshot(
            runtime_result=runtime_result,
            generated_at="2026-06-18T21:15:00+03:00",
        )
        serialized = json.dumps(snapshot, sort_keys=True)
        graph_summary = snapshot["project_graph_summary"]

        self.assertEqual(graph_summary["coverage"]["status"], "partial_static")
        self.assertEqual(graph_summary["coverage"]["unsupported_languages"]["ruby"], "unsupported")
        self.assertTrue(graph_summary["freshness"]["blocks_action_claims"])
        self.assertEqual(graph_summary["rejected_link_summary"]["total"], 2)
        self.assertEqual(graph_summary["framework_semantic_summary"]["frameworks"]["react"], 2)
        self.assertEqual(len(graph_summary["agent_packet_refs"]), 1)
        self.assertEqual(graph_summary["generated_view_policy"], "orientation_only_not_proof")
        self.assertEqual(graph_summary["source_policy"], "generated graph is not source of truth")
        self.assertNotIn("raw_source", serialized)
        self.assertNotIn("https://example.invalid", serialized)
        self.assertNotIn("C:\\Users\\person", serialized)
        self.assertNotIn("release-ready", serialized.lower())

    def test_snapshot_includes_bounded_system_file_hygiene_projection_without_raw_content(self):
        audit_packet = {
            "artifact_kind": "system_file_hygiene_audit",
            "schema_version": 1,
            "write_policy": "read_only",
            "schedule_status": "not_created",
            "status": "blocked",
            "audit_trigger": "soft_size_review",
            "last_audit_at": "2026-06-07T12:00:00+00:00",
            "summary": {
                "files_scanned": 2,
                "warnings": 1,
                "errors": 1,
                "active_schedule_markers": 0,
                "approval_boundary": "owner_approval_required_for_writes",
            },
            "file_statuses": [
                {
                    "path": "PLAN.md",
                    "class": "root_control_plane",
                    "owner": "project root",
                    "state": "blocked",
                    "severity": "error",
                    "finding_count": 1,
                    "size": 128,
                    "line_count": 8,
                    "mtime_utc": "2026-06-05T12:00:00+00:00",
                    "age_days": 2,
                    "content_digest": "sha256:" + "a" * 64,
                    "last_audit_at": "2026-06-07T12:00:00+00:00",
                    "top_finding": "secret_like_literal",
                    "raw_body": "OPENAI_API_KEY = \"sk-test\"",
                },
                {
                    "path": "C:\\Users\\person\\private\\AGENTS.md",
                    "class": "root_control_plane",
                    "owner": "project root",
                    "state": "ok",
                    "severity": "none",
                    "finding_count": 0,
                    "size": 10,
                    "line_count": 1,
                    "mtime_utc": "2026-06-07T12:00:00+00:00",
                    "age_days": 0,
                    "content_digest": "sha256:" + "b" * 64,
                    "last_audit_at": "2026-06-07T12:00:00+00:00",
                },
            ],
        }

        snapshot = build_status_snapshot(
            runtime_result={"status": "route_ready", "workspace": "C:\\Users\\person\\project"},
            system_file_hygiene_audit=audit_packet,
            generated_at="2026-06-07T12:00:00+00:00",
        )
        serialized = json.dumps(snapshot, sort_keys=True)
        hygiene = snapshot["system_file_hygiene"]

        self.assertEqual(hygiene["status"], "blocked")
        self.assertEqual(hygiene["audit_trigger"], "soft_size_review")
        self.assertEqual(hygiene["last_audit_at"], "2026-06-07T12:00:00+00:00")
        self.assertEqual(hygiene["summary"]["files_scanned"], 2)
        self.assertEqual(len(hygiene["file_statuses"]), 1)
        self.assertEqual(hygiene["file_statuses"][0]["path"], "PLAN.md")
        self.assertEqual(hygiene["file_statuses"][0]["content_digest"], "sha256:" + "a" * 64)
        self.assertEqual(hygiene["file_statuses"][0]["top_finding"], "secret_like_literal")
        self.assertNotIn("raw_body", hygiene["file_statuses"][0])
        self.assertEqual(
            hygiene["source_policy"],
            "system file hygiene projection is generated status evidence, not source of truth",
        )
        self.assertEqual(hygiene["approval_boundary"], "owner_approval_required_for_writes")
        self.assertNotIn("sk-test", serialized)
        self.assertNotIn("OPENAI_API_KEY", serialized)
        self.assertNotIn("C:\\Users\\person", serialized)
        self.assertNotIn("private", serialized)

    def test_snapshot_records_task_matrix_projection_deferred_decision_without_projecting_state(self):
        runtime_result = {
            "status": "route_ready",
            "workspace": "C:\\Users\\person\\task-matrix-project",
            "route_packet": {
                "task_matrix_state": {
                    "tasks": [
                        {
                            "id": "T10-PLAN-M15",
                            "status": "matrix-projected-status",
                            "completion_evidence": "matrix-completion-evidence",
                        }
                    ]
                }
            },
        }

        snapshot = build_status_snapshot(
            runtime_result=runtime_result,
            discovery_result={"task_matrix_state": {"raw": "matrix-discovery-state"}},
            generated_at="2026-06-08T00:00:00+00:00",
        )
        serialized = json.dumps(snapshot, sort_keys=True)
        decision = snapshot["projection_decisions"]["task_matrix_state"]

        self.assertEqual(decision["status"], "deferred_in_b37")
        self.assertEqual(decision["state_projection"], "not_projected")
        self.assertEqual(
            decision["source_policy"],
            "task matrix state is not projected into status snapshot/dashboard in B37",
        )
        self.assertEqual(
            decision["future_projection_policy"],
            "future projection must be bounded read-only generated orientation evidence, never source of truth or completion evidence",
        )
        self.assertNotIn("T10-PLAN-M15", serialized)
        self.assertNotIn("matrix-projected-status", serialized)
        self.assertNotIn("matrix-completion-evidence", serialized)
        self.assertNotIn("matrix-discovery-state", serialized)

    def _methodology_packet(self, *, status="present_unverified"):
        return {
            "safe_next_action": "Stage approval-record.md before external mutation.",
            "status": status,
            "semantic_evidence_sufficiency": {
                "status": "present_unverified",
                "required_evidence": ["owner-reviewed evidence"],
            },
            "source_artifact_ledger": [
                {"artifact": "approval-record.md", "decision": "canonical_template"}
            ],
        }


if __name__ == "__main__":
    unittest.main()
