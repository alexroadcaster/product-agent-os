import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
PRODUCT_AGENT_OS = DOCS / "product-agent-os"
MKDOCS = ROOT / "mkdocs.yml"
CHECK_DOCS = ROOT / "tools" / "check_docs.py"
SOURCE_REGISTRY = DOCS / "sources" / "registry.md"
TRACK_BACKLOG = DOCS / "sources" / "product-agent-os-track-8-detailed-backlog.md"
TRACK9_BACKLOG = DOCS / "sources" / "product-agent-os-track-9-backlog.md"
TRACK10_BACKLOG = DOCS / "sources" / "product-agent-os-track-10-backlog.md"
TRACK9_PLAN = DOCS / "superpowers" / "plans" / "2026-05-25-track-9-methodology-intelligence.md"
TRACK10_PLAN = DOCS / "superpowers" / "plans" / "2026-05-27-track-10-guided-questions-status-dashboard.md"
ROOT_README = ROOT / "README.md"
PLUGIN_README = ROOT / "plugins" / "product-agent-os" / "README.md"
REQUIREMENTS = ROOT / "REQUIREMENTS.md"
PLAN = ROOT / "PLAN.md"
TEST = ROOT / "TEST.md"
EVALS = ROOT / "EVALS.md"
RUNLOG = ROOT / "RUNLOG.md"
AGENTS = ROOT / "AGENTS.md"


class ProductAgentOsDocsTest(unittest.TestCase):
    def test_t8h_dedicated_docs_pages_exist_with_operating_contracts(self):
        expected_pages = {
            "scenarios.md": [
                "usage_mode",
                "first response",
                "minimum artifacts",
                "approval boundary",
                "verification gates",
                "bug_rescue",
                "greenfield_idea",
                "complex_system_acceleration",
                "release_packaging",
            ],
            "behavioral-evals.md": [
                "behavioral-workflows.json",
                "expected behavior",
                "forbidden behavior",
                "fixture eval",
                "transcript/session eval runner",
                "evidence-before-completion",
                "residual risk",
            ],
            "codex-compatibility.md": [
                "Codex App",
                "CLI",
                "IDE extension",
                ".codex-plugin/plugin.json",
                "skills",
                "MCP",
                "staged hooks",
                "validate_codex_compatibility.py",
                "no standalone Agents SDK",
                "no separate OpenAI API key",
            ],
        }

        for filename, terms in expected_pages.items():
            with self.subTest(filename=filename):
                path = PRODUCT_AGENT_OS / filename
                self.assertTrue(path.exists(), path)
                text = path.read_text(encoding="utf-8")
                self.assertIn("Source status:", text)
                self.assertIn("Inputs", text)
                self.assertIn("Outputs", text)
                self.assertIn("Verification", text)
                self.assertIn("Risks", text)
                for term in terms:
                    self.assertIn(term, text)

    def test_t8h_docs_are_in_nav_and_required_docs_check(self):
        nav = MKDOCS.read_text(encoding="utf-8")
        check_docs = CHECK_DOCS.read_text(encoding="utf-8")

        for path in [
            "product-agent-os/scenarios.md",
            "product-agent-os/behavioral-evals.md",
            "product-agent-os/codex-compatibility.md",
        ]:
            with self.subTest(path=path):
                self.assertIn(path, nav)
                self.assertIn(path.replace("/", '" / "'), check_docs)

    def test_track9_methodology_intelligence_docs_exist(self):
        path = PRODUCT_AGENT_OS / "methodology-intelligence.md"
        self.assertTrue(path.exists(), path)

        text = path.read_text(encoding="utf-8")
        self.assertIn("Source status:", text)
        self.assertIn("Inputs", text)
        self.assertIn("Outputs", text)
        self.assertIn("Verification", text)
        self.assertIn("Risks", text)

        nav = MKDOCS.read_text(encoding="utf-8")
        check_docs = CHECK_DOCS.read_text(encoding="utf-8")
        self.assertIn("methodology-intelligence.md", nav)
        self.assertIn('product-agent-os" / "methodology-intelligence.md', check_docs)

    def test_track10_guided_question_status_dashboard_docs_are_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        behavioral_evals = (PRODUCT_AGENT_OS / "behavioral-evals.md").read_text(encoding="utf-8")
        scenarios = (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8")
        root_readme = ROOT_README.read_text(encoding="utf-8")
        plugin_readme = PLUGIN_README.read_text(encoding="utf-8")
        control_plane = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [REQUIREMENTS, PLAN, TEST, EVALS, RUNLOG]
        )

        for expected in [
            "Product-Agent OS Track 10 guided question and status dashboard coverage",
            "T10-Q-M15..M22",
            "T10-Q-M23..M25",
            "question_queue_contract_present",
            "status_snapshot_present",
            "status_dashboard_present",
            "dashboard_no_external_assets",
            "dashboard_not_source_of_truth",
            "stale_evidence_no_success_claim",
            "verification_status:",
        ]:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        for expected in [
            "guided-question-smallest-blocking-question",
            "guided-question-no-broad-methodology-interview",
            "status-dashboard-generated-view-only",
            "status-dashboard-stale-evidence-no-success-claim",
            "runtime-first-response-no-question-dump",
            "one blocking question maximum",
            "dashboard is a generated view",
            "no success claim from stale evidence",
        ]:
            with self.subTest(behavioral_evals=expected):
                self.assertIn(expected, behavioral_evals)

        for expected in [
            "Guided question protocol",
            "status snapshot",
            ".codex/product-agent-os/status.html",
            ".codex/product-agent-os/status.json",
            "generated view only",
            "underlying artifacts",
        ]:
            with self.subTest(scenarios=expected):
                self.assertIn(expected, scenarios)
                self.assertIn(expected, plugin_readme)

        for expected in [
            "Task 23 guided question protocol and status dashboard",
            "question_queue_contract_present",
            "status_snapshot_present",
            "status_dashboard_present",
            "dashboard_not_source_of_truth",
            "stale_evidence_no_success_claim",
        ]:
            with self.subTest(control_plane=expected):
                self.assertIn(expected, control_plane)
                self.assertIn(expected, root_readme)

    def test_track10_task24_self_verification_docs_and_control_plane_are_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
            "behavioral_evals": (PRODUCT_AGENT_OS / "behavioral-evals.md").read_text(
                encoding="utf-8"
            ),
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
        }

        for expected in [
            "Product-Agent OS Track 10 self-verification metrics-loop final closure",
            "T10-SV-M58..M62",
            "agent_skill_metrics_loop_contract_present",
            "metrics_report_redacted",
            "trace_normalization_contract_present",
            "judge_calibration_gate_present",
            "scorecard_ledger_contract_present",
            "source_priority_contract_present",
            "metrics_packet_bounds_present",
            "trace_data_classification_gate_present",
            "offline_artifact_safety_shared",
            "no_baseline_renderer_pollution",
            "active_metrics_automation_blocked",
            "update_candidate_rollback_required",
            "metrics_loop_runtime_route_contract_present",
            "metrics_loop_lifecycle_contract_present",
            "metrics_loop_false_positive_guards_present",
            "verification_status:",
        ]:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        docs_contract_terms = [
            "agent_skill_metrics_loop",
            "target registry",
            "trace intake",
            "dataset quality",
            "grader/judge calibration",
            "cadence recommendation",
            "scorecard ledger",
            "agent-skill-evaluation-report.html",
            "modernization candidates",
            "approval boundary",
            "source-of-truth policy",
            "staged evidence only",
            "report is not source of truth",
            "no live eval/model/API calls",
            "no active schedules",
            "no self-applied updates",
            "L0",
            "L1",
            "L2",
            "L3",
        ]
        for document in ["technical", "scenarios", "behavioral_evals"]:
            for expected in docs_contract_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, documents[document])

        overview_terms = [
            "Task 24 Self-Verification And Modernization Loop",
            "self-verification metrics loop",
            "agent_skill_metrics_loop",
            "staged evidence only",
            "no live eval/model/API calls",
            "no active schedules",
            "no self-applied updates",
        ]
        for document in ["index", "root_readme", "plugin_readme"]:
            for expected in overview_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, documents[document])

        for expected in [
            "| `done` | `T10-SV-M58..M62` final docs/control-plane verification closure |",
            "Task 24 Batch 12",
            "full unittest must use `timeout_ms: 1200000`",
            "explicit-only git boundary",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        for filename, text in control_plane.items():
            for expected in [
                "Task 24 Batch 12",
                "T10-SV-M58..M62",
                "agent_skill_metrics_loop",
                "timeout_ms: 1200000",
                "explicit-only",
            ]:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task25_project_graph_batch16_docs_and_control_plane_are_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
        }

        registry_terms = [
            "Product-Agent OS Track 10 project code graph Batch 16 cockpit visualization",
            "T10-CG-V2-M19..M26",
            "project_cockpit_model.py",
            "project_graph_visual_model.py",
            "project_graph_renderer.py",
            "project-cockpit.html",
            "Graphology-compatible static visual projection",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "| `done` | `T10-CG-V2-M19..M26` cockpit visualization |",
            "Code Flow inside `Code Intelligence`",
            "local Graphology/Sigma vendor boundary",
            "full unittest must continue to use `timeout_ms: 1200000`",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 25 Batch 13, Batch 14, Batch 15 and Batch 16",
            ".codex/product-agent-os/project-cockpit.html",
            ".codex/product-agent-os/project-cockpit.json",
            "exactly eight top-level pages",
            "Code Flow",
            "Code Intelligence",
            "Graphology-compatible static projection",
            "local Graphology/Sigma",
            "selected-node evidence",
            "fallback",
            "no external assets",
            "not source of truth",
        ]
        for document, text in documents.items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 25 Batch 16",
            "T10-CG-V2-M19..M26",
            "Code Flow inside `Code Intelligence`",
            "Graphology-compatible static",
            "local Graphology/Sigma",
            "selected-node evidence",
            "fallback static",
            "timeout_ms: 1200000",
            "explicit-only",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task25_project_graph_batch17_docs_and_control_plane_are_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "product_index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
        }

        registry_terms = [
            "Product-Agent OS Track 10 project code graph Batch 17 evals and future gates",
            "T10-CG-V2-M27..M30",
            "project_graph_search_quality.py",
            "project_graph_search_quality_present",
            "project_graph_future_backend_semantic_gates_present",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "| `done` | `T10-CG-V2-M27..M30` evals/docs/future gates |",
            "search-quality eval loop",
            "fixture structural fields",
            "future backend and semantic gates",
            "static search index",
            "live database/server",
            "semantic extraction and rationale/comment extraction",
            "LLM semantic extraction",
            "redaction, cache, token budget, eval threshold and rollback path",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 25 Batch 17",
            "fixture structural fields",
            "search-quality eval loop",
            "symbol recall",
            "top-k/MRR",
            "affected-test precision",
            "future backend and semantic gates",
            "static search index",
            "live database/server",
            "LLM semantic extraction",
            "explicit approval",
            "redaction, cache, token budget, eval threshold and rollback path",
        ]
        for document, text in documents.items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 25 Batch 17",
            "T10-CG-V2-M27..M30",
            "fixture structural fields",
            "search-quality eval loop",
            "project_graph_future_backend_semantic_gates_present",
            "static search index",
            "live database/server",
            "semantic extraction and rationale/comment extraction",
            "LLM semantic extraction",
            "redaction, cache, token budget, eval threshold and rollback path",
            "explicit-only",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task25_future_gated_extension_matrix_is_staged(self):
        plan = TRACK10_PLAN.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        control_plane = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [REQUIREMENTS, PLAN, EVALS, RUNLOG]
        )

        plan_terms = [
            "Task 25 future-gated extension analysis",
            "Task 25 future-gated extension matrix",
            "T10-CG-V2-M39",
            "T10-CG-V2-M62",
            "Batch 20: Local Query Backend And Live Database/Server Gate",
            "Batch 21: Semantic Retrieval, Embeddings And Cross-Encoder Eval",
            "Batch 22: LLM Semantic Extraction And Rationale/Comment Proposals",
            "Batch 23: Future Extension Verification, Rollback And Closure",
            "approval_required",
            "redaction boundary, cache policy, token budget, eval threshold, rollback/disable path",
            "Planning matrix presence is not implementation evidence",
        ]
        for expected in plan_terms:
            with self.subTest(plan=expected):
                self.assertIn(expected, plan)

        backlog_terms = [
            "Task 25 Future-Gated Extension Matrix",
            "| `done` | `T10-CG-V2-M33..M38` offline static search index |",
            "| `done` | `T10-CG-V2-M39..M44` local query backend and live database/server gate |",
            "| `done` | `T10-CG-V2-M45..M51` semantic retrieval, embeddings and cross-encoder eval |",
            "| `done` | `T10-CG-V2-M52..M57` LLM semantic extraction and rationale/comment proposals |",
            "| `done` | `T10-CG-V2-M58..M62` future extension verification, rollback and closure |",
            "Generated semantic nodes, rationale and comments are staged proposals, not canonical graph facts.",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        control_terms = [
            "extension matrix `T10-CG-V2-M39..M62`",
            "Batch 19 offline static search index",
            "approved offline static search index",
            "Batch 20 local query backend/live database-server gate",
            "Batch 21 semantic retrieval with embeddings/cross-encoder",
            "Batch 22 LLM semantic extraction/rationale-comment proposals",
            "Batch 23 extension",
            "project_graph_extension_closure.py",
            "Planning matrix presence is not implementation evidence",
            "explicit approval with redaction, cache, token budget, eval threshold and rollback path",
        ]
        for expected in control_terms:
            with self.subTest(control_plane=expected):
                self.assertIn(expected, control_plane)

    def test_track10_task25_batch22_llm_extraction_proposals_are_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "product_index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
        }

        registry_terms = [
            "Product-Agent OS Track 10 project code graph Batch 22 LLM semantic extraction",
            "T10-CG-V2-M52..M57",
            "project_graph_llm_extraction.py",
            "project_graph_llm_extraction_gate_present",
            "rationale/comment proposals",
            "staged proposals, not canonical graph facts",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "| `done` | `T10-CG-V2-M52..M57` LLM semantic extraction and rationale/comment proposals |",
            "Batch 22 explicit approval",
            "project_graph_llm_extraction.py",
            "prompt/model policy",
            "structured JSON with provenance, uncertainty and unsupported-claim labels",
            "semantic node and edge proposals",
            "rationale/comment proposals",
            "human review can accept, reject or mark accepted_gap",
            "AI incident workflow",
            "rollback/disable path is deleting `.codex/product-agent-os/project-code-graph-llm-proposals.json`",
            "Batch 23 is closed separately as generated extension verification/rollback evidence",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 25 Batch 22",
            "T10-CG-V2-M52..M57",
            "project_graph_llm_extraction.py",
            "project_graph_llm_extraction_gate_present",
            "prompt/model policy",
            "structured JSON",
            "semantic node and edge proposals",
            "rationale/comment proposals",
            "staged proposals, not canonical graph facts",
            "no canonical graph mutation",
            "AI incident workflow",
            "rollback/disable path",
            "Batch 23",
        ]
        for document, text in documents.items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 25 Batch 22",
            "T10-CG-V2-M52..M57",
            "project_graph_llm_extraction.py",
            "project_graph_llm_extraction_gate_present",
            "project_graph_llm_proposal_schema_present",
            "project_graph_rationale_comment_proposals_present",
            "project_graph_llm_extraction_eval_present",
            "prompt/model policy",
            "staged proposals, not canonical graph facts",
            "no canonical graph mutation",
            "AI incident workflow",
            "Batch 23",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task25_batch23_future_extension_closure_is_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "product_index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
        }

        registry_terms = [
            "Product-Agent OS Track 10 project code graph Batch 23 future extension verification",
            "T10-CG-V2-M58..M62",
            "project_graph_extension_closure.py",
            "project_graph_future_extension_closure_present",
            "project_graph_extension_rollback_deletion_present",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "| `done` | `T10-CG-V2-M58..M62` future extension verification, rollback and closure |",
            "Batch 23 explicit approval",
            "project_graph_extension_closure.py",
            "verify-extensions",
            "disable-extensions",
            "deletion proof",
            "graph-only fallback",
            "blocked_without_new_explicit_approval",
            "full verification with `timeout_ms: 1200000`",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 25 Batch 23",
            "T10-CG-V2-M58..M62",
            "project_graph_extension_closure.py",
            "verify-extensions",
            "disable-extensions",
            "rollback/data deletion proof",
            "graph-only fallback",
            "blocked_without_new_explicit_approval",
            "no live external model/API calls",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for document, text in documents.items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 25 Batch 23",
            "T10-CG-V2-M58..M62",
            "project_graph_extension_closure.py",
            "project_graph_future_extension_closure_present",
            "project_graph_extension_rollback_deletion_present",
            "project_graph_unapproved_surface_blocking_present",
            "project_graph_extension_full_verification_contract_present",
            "rollback/data deletion proof",
            "graph-only fallback",
            "blocked_without_new_explicit_approval",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task26_batch24_live_governance_is_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "product_index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
            "agents": AGENTS.read_text(encoding="utf-8"),
        }

        registry_terms = [
            "Product-Agent OS Track 10 Task 26 Batch 24 live governance",
            "T10-LIVE-M01..M06",
            "project_graph_live_governance.py",
            "project_graph_live_approval_packet_present",
            "project_graph_live_redaction_guard_present",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "Task 26 Batch 24 Closure",
            "| `done` | `T10-LIVE-M01..M06` approval, data classification, redaction, credentials, cache and budget governance |",
            "Batch 24 explicit approval",
            "project_graph_live_governance.py",
            "No complete approval packet means no live action",
            "Secrets, raw source bodies and absolute paths are blocked",
            "Provider call is impossible without sanitizer pass",
            "Cache can be deleted without graph loss",
            "Budget exceed routes to blocked or degraded mode",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 26 Batch 24",
            "T10-LIVE-M01..M06",
            "Approval, Data Classification, Redaction, Credentials, Cache And Budget Governance",
            "project_graph_live_governance.py",
            "project_graph_live_approval_packet_present",
            "project_graph_live_data_classification_policy_present",
            "project_graph_live_redaction_guard_present",
            "project_graph_provider_credentials_boundary_present",
            "project_graph_live_cache_deletion_policy_present",
            "project_graph_live_budget_guard_present",
            "project_graph_live_governance_no_live_calls_present",
            "no live server",
            "no provider calls",
            "no canonical graph mutation",
            "staged evidence only",
            "not source of truth",
        ]
        for document, text in documents.items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 26 Batch 24",
            "T10-LIVE-M01..M06",
            "project_graph_live_governance.py",
            "project_graph_live_approval_packet_present",
            "project_graph_live_data_classification_policy_present",
            "project_graph_live_redaction_guard_present",
            "project_graph_provider_credentials_boundary_present",
            "project_graph_live_cache_deletion_policy_present",
            "project_graph_live_budget_guard_present",
            "project_graph_live_governance_no_live_calls_present",
            "no live server",
            "no provider calls",
            "no live external model/API calls",
            "no canonical graph mutation",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task26_batch25_live_runtime_is_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "product_index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
            "agents": AGENTS.read_text(encoding="utf-8"),
        }

        registry_terms = [
            "Product-Agent OS Track 10 Task 26 Batch 25 live runtime",
            "T10-LIVE-M07..M10",
            "project_graph_live_runtime.py",
            "project_graph_live_runtime_contract_present",
            "project_graph_live_runtime_auth_policy_present",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "Task 26 Batch 25 Closure",
            "| `done` | `T10-LIVE-M07..M10` live local read-only runtime, auth and fallback |",
            "Batch 25 explicit approval",
            "project_graph_live_runtime.py",
            "No write endpoints and no canonical mutation",
            "Starts only after approval; cleanup is verified",
            "Runtime is not public by default and rejects unauthorized access",
            "Fallback works after disabling live layer",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 26 Batch 25",
            "T10-LIVE-M07..M10",
            "Live Local Read-Only Runtime, Auth And Fallback",
            "project_graph_live_runtime.py",
            "project_graph_live_runtime_contract_present",
            "project_graph_live_runtime_governance_prerequisite_present",
            "project_graph_live_runtime_read_only_routes_present",
            "project_graph_live_runtime_lifecycle_controls_present",
            "project_graph_live_runtime_auth_policy_present",
            "project_graph_live_runtime_graph_only_fallback_present",
            "project_graph_live_runtime_no_public_or_mutation_surface_present",
            "disabled_by_default_not_started",
            "local-only access",
            "rejects unauthorized access",
            "no write endpoints",
            "graph_only_query_mode",
            "no canonical graph mutation",
            "staged evidence only",
            "not source of truth",
        ]
        for document, text in documents.items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 26 Batch 25",
            "T10-LIVE-M07..M10",
            "project_graph_live_runtime.py",
            "project_graph_live_runtime_contract_present",
            "project_graph_live_runtime_governance_prerequisite_present",
            "project_graph_live_runtime_read_only_routes_present",
            "project_graph_live_runtime_lifecycle_controls_present",
            "project_graph_live_runtime_auth_policy_present",
            "project_graph_live_runtime_graph_only_fallback_present",
            "project_graph_live_runtime_no_public_or_mutation_surface_present",
            "disabled_by_default_not_started",
            "no write endpoints",
            "local-only access",
            "rejects unauthorized access",
            "no provider calls",
            "no live external model/API calls",
            "no canonical graph mutation",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task26_batch26_external_embedding_provider_gate_is_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "product_index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
            "agents": AGENTS.read_text(encoding="utf-8"),
        }

        registry_terms = [
            "Product-Agent OS Track 10 Task 26 Batch 26 external embedding provider gate and eval",
            "T10-LIVE-M11..M12",
            "project_graph_embedding_provider.py",
            "project_graph_external_embedding_provider_gate_present",
            "project_graph_external_embedding_eval_baseline_present",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "Task 26 Batch 26 Closure",
            "| `done` | `T10-LIVE-M11..M12` external embedding provider gate and eval |",
            "Batch 26 explicit approval",
            "project_graph_embedding_provider.py",
            "No external call without approval/redaction/cache/budget",
            "Must beat approved threshold or stay disabled",
            "semantic_retrieval_or_graph_only",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 26 Batch 26",
            "T10-LIVE-M11..M12",
            "External Embedding Provider Gate And Eval",
            "project_graph_embedding_provider.py",
            "project_graph_external_embedding_provider_gate_present",
            "project_graph_external_embedding_governance_prerequisite_present",
            "project_graph_external_embedding_redaction_cache_budget_present",
            "project_graph_external_embedding_eval_baseline_present",
            "project_graph_external_embedding_threshold_fallback_present",
            "project_graph_external_embedding_no_live_calls_present",
            "No external call without approval/redaction/cache/budget",
            "Must beat approved threshold or stay disabled",
            "semantic_retrieval_or_graph_only",
            "provider_call_allowed",
            "external_call_performed",
            "staged evidence only",
            "not source of truth",
            "no provider calls",
            "no live external model/API calls",
            "no canonical graph mutation",
        ]
        for document, text in documents.items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 26 Batch 26",
            "T10-LIVE-M11..M12",
            "project_graph_embedding_provider.py",
            "project_graph_external_embedding_provider_gate_present",
            "project_graph_external_embedding_governance_prerequisite_present",
            "project_graph_external_embedding_redaction_cache_budget_present",
            "project_graph_external_embedding_eval_baseline_present",
            "project_graph_external_embedding_threshold_fallback_present",
            "project_graph_external_embedding_no_live_calls_present",
            "No external call without approval/redaction/cache/budget",
            "Must beat approved threshold or stay disabled",
            "semantic_retrieval_or_graph_only",
            "provider_call_allowed",
            "external_call_performed",
            "no provider calls",
            "no live external model/API calls",
            "no canonical graph mutation",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task26_batch27_reranker_and_hybrid_retrieval_is_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "product_index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
            "agents": AGENTS.read_text(encoding="utf-8"),
        }

        registry_terms = [
            "Product-Agent OS Track 10 Task 26 Batch 27 cross-encoder reranker and hybrid retrieval",
            "T10-LIVE-M13..M14",
            "project_graph_reranker_provider.py",
            "project_graph_hybrid_retrieval.py",
            "reranker_provider.py",
            "hybrid_retrieval.py",
            "project_graph_external_reranker_provider_gate_present",
            "project_graph_hybrid_retrieval_pipeline_present",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "Task 26 Batch 27 Closure",
            "| `done` | `T10-LIVE-M13..M14` cross-encoder reranker and hybrid retrieval |",
            "Batch 27 explicit approval",
            "project_graph_reranker_provider.py",
            "project_graph_hybrid_retrieval.py",
            "Precision/MRR improves or fallback remains active",
            "source-backed, bounded and explainable",
            "semantic_retrieval_or_graph_only",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 26 Batch 27",
            "T10-LIVE-M13..M14",
            "Cross-Encoder Reranker And Hybrid Retrieval",
            "project_graph_reranker_provider.py",
            "project_graph_hybrid_retrieval.py",
            "reranker_provider.py",
            "hybrid_retrieval.py",
            "project_graph_external_reranker_provider_gate_present",
            "project_graph_external_reranker_governance_prerequisite_present",
            "project_graph_external_reranker_redaction_cache_budget_present",
            "project_graph_external_reranker_eval_baseline_present",
            "project_graph_external_reranker_threshold_fallback_present",
            "project_graph_external_reranker_no_live_calls_present",
            "project_graph_hybrid_retrieval_pipeline_present",
            "project_graph_hybrid_retrieval_explainable_fusion_present",
            "project_graph_hybrid_retrieval_fallback_present",
            "project_graph_hybrid_retrieval_no_canonical_mutation_present",
            "approval_required",
            "Precision/MRR improves or fallback remains active",
            "source-backed, bounded and explainable",
            "semantic_retrieval_or_graph_only",
            "provider_call_allowed",
            "external_call_performed",
            "staged evidence only",
            "not source of truth",
            "No live provider calls",
            "no provider calls",
            "no live external model/API calls",
            "no canonical graph mutation",
        ]
        for document, text in documents.items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 26 Batch 27",
            "T10-LIVE-M13..M14",
            "project_graph_reranker_provider.py",
            "project_graph_hybrid_retrieval.py",
            "reranker_provider.py",
            "hybrid_retrieval.py",
            "project_graph_external_reranker_provider_gate_present",
            "project_graph_external_reranker_governance_prerequisite_present",
            "project_graph_external_reranker_redaction_cache_budget_present",
            "project_graph_external_reranker_eval_baseline_present",
            "project_graph_external_reranker_threshold_fallback_present",
            "project_graph_external_reranker_no_live_calls_present",
            "project_graph_hybrid_retrieval_pipeline_present",
            "project_graph_hybrid_retrieval_explainable_fusion_present",
            "project_graph_hybrid_retrieval_fallback_present",
            "project_graph_hybrid_retrieval_no_canonical_mutation_present",
            "Precision/MRR improves or fallback remains active",
            "source-backed, bounded and explainable",
            "semantic_retrieval_or_graph_only",
            "provider_call_allowed",
            "external_call_performed",
            "No live provider calls",
            "no provider calls",
            "no live external model/API calls",
            "no canonical graph mutation",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task26_batch28_llm_proposal_adapter_and_safety_eval_is_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "product_index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
            "agents": AGENTS.read_text(encoding="utf-8"),
        }

        registry_terms = [
            "Product-Agent OS Track 10 Task 26 Batch 28 live LLM proposal adapter and safety eval",
            "T10-LIVE-M15..M16",
            "project_graph_llm_proposal_provider.py",
            "llm_proposal_provider.py",
            "llm-proposal-eval.json",
            "project_graph_live_llm_proposal_provider_gate_present",
            "project_graph_live_llm_proposal_safety_eval_present",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "Task 26 Batch 28 Closure",
            "| `done` | `T10-LIVE-M15..M16` live LLM proposal adapter and safety eval |",
            "Batch 28 explicit approval",
            "project_graph_llm_proposal_provider.py",
            "llm_proposal_provider.py",
            "llm-proposal-eval.json",
            "proposal-only, never canonical fact",
            "hallucination, privacy, grounding and stale-context tests",
            "incident_blocked",
            "local_llm_proposals_or_semantic_retrieval_or_graph_only",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 26 Batch 28",
            "T10-LIVE-M15..M16",
            "Live LLM Proposal Adapter And Safety Eval",
            "project_graph_llm_proposal_provider.py",
            "llm_proposal_provider.py",
            "llm-proposal-eval.json",
            "project_graph_live_llm_proposal_provider_gate",
            "batch28_live_llm_proposal_adapter_and_safety_eval",
            "external_llm",
            "external_llm_proposal_adapter",
            "llm_proposal_safety_eval",
            "structured_json",
            "unsupported_claim",
            "proposal-only, never canonical fact",
            "hallucination, privacy, grounding and stale-context tests",
            "incident_blocked",
            "AI incident workflow",
            "local_llm_proposals_or_semantic_retrieval_or_graph_only",
            "provider_call_allowed",
            "external_call_performed",
            "staged evidence only",
            "not source of truth",
            "No live provider calls",
            "no provider calls",
            "no live external model/API calls",
            "no canonical graph mutation",
        ]
        for document, text in documents.items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 26 Batch 28",
            "T10-LIVE-M15..M16",
            "project_graph_llm_proposal_provider.py",
            "llm_proposal_provider.py",
            "llm-proposal-eval.json",
            "project_graph_live_llm_proposal_provider_gate_present",
            "project_graph_live_llm_proposal_governance_prerequisite_present",
            "project_graph_live_llm_proposal_prompt_schema_present",
            "project_graph_live_llm_proposal_redaction_cache_budget_present",
            "project_graph_live_llm_proposal_safety_eval_present",
            "project_graph_live_llm_proposal_threshold_fallback_present",
            "project_graph_live_llm_proposal_incident_path_present",
            "project_graph_live_llm_proposal_no_live_calls_present",
            "project_graph_live_llm_proposal_no_canonical_mutation_present",
            "proposal-only, never canonical fact",
            "hallucination, privacy, grounding and stale-context tests",
            "incident_blocked",
            "local_llm_proposals_or_semantic_retrieval_or_graph_only",
            "provider_call_allowed",
            "external_call_performed",
            "No live provider calls",
            "no provider calls",
            "no live external model/API calls",
            "no canonical graph mutation",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task25_batch20_local_backend_gate_is_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "product_index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
        }

        registry_terms = [
            "Product-Agent OS Track 10 project code graph Batch 20 local query backend gate",
            "T10-CG-V2-M39..M44",
            "project_graph_backend.py",
            "project_graph_local_backend_gate_present",
            "disabled by default",
            "graph-only fallback",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "| `done` | `T10-CG-V2-M39..M44` local query backend and live database/server gate |",
            "Batch 20 explicit approval",
            "generated local file-store",
            "not source of truth",
            "server mode is disabled by default",
            "no production server",
            "graph-only fallback",
            "rollback/disable path is deleting `.codex/product-agent-os/project-code-graph-backend.json`",
            "Batch 21, Batch 22 and Batch 23 are now implemented separately as generated, approval-bound extension slices",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 25 Batch 20",
            "T10-CG-V2-M39..M44",
            "project_graph_backend.py",
            "project_graph_local_backend_gate_present",
            "approval decision packet",
            "storage path, port policy, process lifecycle, auth boundary, cleanup, logging, performance threshold and rollback path",
            "disabled by default",
            "generated local file-store",
            "not source of truth",
            "graph-only fallback",
            "no production server",
        ]
        for document, text in documents.items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 25 Batch 20",
            "T10-CG-V2-M39..M44",
            "project_graph_backend.py",
            "project_graph_local_backend_gate_present",
            "approval decision packet",
            "storage path, port policy, process lifecycle, auth boundary, cleanup, logging, performance threshold and rollback path",
            "disabled by default",
            "generated local file-store",
            "not source of truth",
            "graph-only fallback",
            "no production server",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task25_batch21_semantic_retrieval_is_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "product_index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
        }

        registry_terms = [
            "Product-Agent OS Track 10 project code graph Batch 21 semantic retrieval",
            "T10-CG-V2-M45..M51",
            "project_graph_semantic.py",
            "project_graph_semantic_retrieval_gate_present",
            "cross-encoder eval",
            "present_unverified",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "| `done` | `T10-CG-V2-M45..M51` semantic retrieval, embeddings and cross-encoder eval |",
            "Batch 21 explicit approval",
            "semantic corpus and chunk policy",
            "embeddings cache metadata",
            "semantic query packets",
            "cross-encoder reranking gate",
            "semantic retrieval eval suite",
            "present_unverified orientation evidence",
            "no canonical graph edge rewrites",
            "rollback/disable path is deleting `.codex/product-agent-os/project-code-graph-semantic-index.json`",
            "Batch 22 and Batch 23 are now implemented separately as generated, approval-bound extension slices",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 25 Batch 21",
            "T10-CG-V2-M45..M51",
            "project_graph_semantic.py",
            "project_graph_semantic_retrieval_gate_present",
            "semantic corpus and chunk policy",
            "embeddings cache metadata",
            "semantic query packets",
            "cross-encoder eval",
            "present_unverified",
            "no canonical graph edge rewrites",
            "rollback/disable path",
            "Batch 23",
        ]
        for document, text in documents.items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 25 Batch 21",
            "T10-CG-V2-M45..M51",
            "project_graph_semantic.py",
            "project_graph_semantic_retrieval_gate_present",
            "semantic corpus and chunk policy",
            "embeddings cache metadata",
            "semantic query packets",
            "cross-encoder eval",
            "present_unverified orientation evidence",
            "no canonical graph edge rewrites",
            "Batch 23",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task25_batch18_final_closure_is_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "product_index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
        }

        registry_terms = [
            "Product-Agent OS Track 10 project code graph Batch 18 final verification closure",
            "T10-CG-V2-M31..M32",
            "focused/full verification",
            "explicit-only git boundary",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "| `done` | `T10-CG-V2-M31..M32` final verification and closure |",
            "Task 25 Batch 18",
            "full unittest ran 664 tests with `OK`",
            "fixture eval exited `0` for 91 fixture directories",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 25 Batch 18",
            "T10-CG-V2-M31..M32",
            "focused/full verification",
            "full unittest ran 664 tests with `OK`",
            "fixture eval exited `0` for 91 fixture directories",
            "explicit-only git boundary",
            "Batch 23",
        ]
        for document, text in documents.items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 25 Batch 18",
            "T10-CG-V2-M31..M32",
            "focused/full verification",
            "full unittest ran 664 tests with `OK`",
            "fixture eval exited `0` for 91 fixture directories",
            "transcript eval exited `0` with 17 sessions and 0 failures",
            "Codex compatibility returned `status: compatible`",
            "strict MkDocs",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task25_batch19_static_search_index_is_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "product_index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
        }

        registry_terms = [
            "Product-Agent OS Track 10 project code graph Batch 19 offline static search index",
            "T10-CG-V2-M33..M38",
            "project_graph_index.py",
            "project_graph_static_search_index_present",
            "offline static search index",
            "explicit user approval",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "| `done` | `T10-CG-V2-M33..M38` offline static search index |",
            "Batch 19 explicit approval",
            "generated, cache-bound and not source of truth",
            "no live database/server, LLM, embedding or cross-encoder",
            "rollback/disable path is deleting `.codex/product-agent-os/project-code-graph-search-index.json`",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 25 Batch 19",
            "T10-CG-V2-M33..M38",
            "offline static search index",
            ".codex/product-agent-os/project-code-graph-search-index.json",
            "generated, cache-bound and not source of truth",
            "graph artifact only",
            "no live database/server, LLM, embedding or cross-encoder",
            "rollback/disable path",
        ]
        for document, text in documents.items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 25 Batch 19",
            "T10-CG-V2-M33..M38",
            "explicit user approval",
            "project_graph_index.py",
            "project_graph_static_search_index_present",
            "offline static search index",
            "generated, cache-bound and not source of truth",
            "graph artifact only",
            "rollback/disable path",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_t8h_and_t8gy_source_and_backlog_closure_are_documented(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK_BACKLOG.read_text(encoding="utf-8")

        self.assertIn("Product-Agent OS Track 8 scenario, eval and transcript docs", registry)
        self.assertIn("docs/product-agent-os/scenarios.md", registry)
        self.assertIn("docs/product-agent-os/behavioral-evals.md", registry)
        self.assertIn("docs/product-agent-os/codex-compatibility.md", registry)
        self.assertIn("plugins/product-agent-os/scripts/product_agent_os/discovery.py", registry)
        self.assertIn("plugins/product-agent-os/scripts/run_transcript_eval.py", registry)
        self.assertIn("T8-D", registry)
        self.assertIn("verification_status:", registry)

        self.assertIn("| `done` | `T8-H` system docs and control-plane sync |", backlog)
        self.assertIn("dedicated scenario, behavioral eval and Codex compatibility docs", backlog)
        self.assertIn("| `T8-GY` behavioral workflow evals | `done` |", backlog)
        self.assertIn("deterministic transcript/session runner", backlog)
        self.assertIn("| `T8-D` discovery model | `done` |", backlog)
        self.assertIn("methodology_applicability", backlog)

    def test_track9_backend_docs_and_source_registry_are_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK9_BACKLOG.read_text(encoding="utf-8")
        behavioral_evals = (PRODUCT_AGENT_OS / "behavioral-evals.md").read_text(encoding="utf-8")
        scenarios = (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8")
        readme = (ROOT / "plugins" / "product-agent-os" / "README.md").read_text(encoding="utf-8")

        for expected in [
            "Product-Agent OS Track 9 backend methodology coverage",
            "T9-D7",
            "backend_contract_present",
            "docs/product-agent-os/behavioral-evals.md",
            "plugins/product-agent-os/scripts/product_agent_os/discovery.py",
            "verification_status:",
        ]:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        for expected in [
            "backend_contract_present",
            "Backend eval",
            "runtime/failure/observability/security/rollback evidence",
            "owner reviewed test/eval/runtime evidence sufficiency",
        ]:
            with self.subTest(behavioral_evals=expected):
                self.assertIn(expected, behavioral_evals)

        for expected in [
            "Backend methodology routing",
            "backend-service-overview.md",
            "backend-runtime-behavior.md",
            "runtime/failure evidence",
        ]:
            with self.subTest(scenarios=expected):
                self.assertIn(expected, scenarios)

        for expected in [
            "Backend methodology",
            "backend_contract_present",
            "backend_service_boundary_present",
            "owner reviewed test/eval/runtime evidence sufficiency",
        ]:
            with self.subTest(readme=expected):
                self.assertIn(expected, readme)

        self.assertIn("T9-D7-M40..M45", backlog)
        self.assertIn("stack-specific backend snippets deferred", backlog)
        self.assertIn("cross-domain semantic sufficiency backlog", backlog)

    def test_track9_api_integrations_docs_and_source_registry_are_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK9_BACKLOG.read_text(encoding="utf-8")
        behavioral_evals = (PRODUCT_AGENT_OS / "behavioral-evals.md").read_text(encoding="utf-8")
        scenarios = (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8")
        readme = (ROOT / "plugins" / "product-agent-os" / "README.md").read_text(encoding="utf-8")

        for expected in [
            "Product-Agent OS Track 9 API & Integrations methodology coverage",
            "T9-D8",
            "api_integrations_contract_present",
            "docs/product-agent-os/behavioral-evals.md",
            "plugins/product-agent-os/scripts/product_agent_os/discovery.py",
            "verification_status:",
        ]:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        for expected in [
            "api_integrations_contract_present",
            "API & Integrations eval",
            "Swagger UI is not source of truth",
            "external writes are approval_required",
        ]:
            with self.subTest(behavioral_evals=expected):
                self.assertIn(expected, behavioral_evals)

        for expected in [
            "API & Integrations methodology routing",
            "api-inventory.md",
            "api-contract-test-matrix.md",
            "external-integration-approval.md",
        ]:
            with self.subTest(scenarios=expected):
                self.assertIn(expected, scenarios)

        for expected in [
            "API & Integrations methodology",
            "api_integrations_contract_present",
            "api_contract_source_present",
            "external_write_approval_present",
        ]:
            with self.subTest(readme=expected):
                self.assertIn(expected, readme)

        self.assertIn("T9-D8", backlog)
        self.assertIn("API lint tooling", backlog)
        self.assertIn("multi-repository generated clients deferred", backlog)

    def test_track9_database_data_docs_and_source_registry_are_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK9_BACKLOG.read_text(encoding="utf-8")
        behavioral_evals = (PRODUCT_AGENT_OS / "behavioral-evals.md").read_text(encoding="utf-8")
        scenarios = (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8")
        readme = (ROOT / "plugins" / "product-agent-os" / "README.md").read_text(encoding="utf-8")

        for expected in [
            "Product-Agent OS Track 9 Database & Data methodology coverage",
            "T9-D9",
            "database_data_contract_present",
            "docs/product-agent-os/behavioral-evals.md",
            "plugins/product-agent-os/scripts/product_agent_os/discovery.py",
            "verification_status:",
        ]:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        for expected in [
            "database_data_contract_present",
            "Database & Data eval",
            "schema-only artifact is not safety proof",
            "production access approval_required",
        ]:
            with self.subTest(behavioral_evals=expected):
                self.assertIn(expected, behavioral_evals)

        for expected in [
            "Database & Data methodology routing",
            "database-inventory.md",
            "database-migration-plan.md",
            "database-production-access-approval.md",
        ]:
            with self.subTest(scenarios=expected):
                self.assertIn(expected, scenarios)

        for expected in [
            "Database & Data methodology",
            "database_data_contract_present",
            "database_migration_plan_present",
            "database_production_access_approval_present",
        ]:
            with self.subTest(readme=expected):
                self.assertIn(expected, readme)

        self.assertIn("T9-D9", backlog)
        self.assertIn("schema-diff tooling deferred", backlog)
        self.assertIn("runtime/pipeline/RAG signals stay `present_unverified`", backlog)

    def test_track9_llm_ai_rag_docs_and_backlog_are_synced_through_m36(self):
        backlog = TRACK9_BACKLOG.read_text(encoding="utf-8")
        behavioral_evals = (PRODUCT_AGENT_OS / "behavioral-evals.md").read_text(encoding="utf-8")
        scenarios = (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8")
        development_standards = (PRODUCT_AGENT_OS / "development-standards.md").read_text(
            encoding="utf-8"
        )
        readme = (ROOT / "plugins" / "product-agent-os" / "README.md").read_text(encoding="utf-8")

        for expected in [
            "Batch `M20..M29` completed scope",
            "Batch `M30..M36` completed scope",
            "llm_ai_rag_contract_present",
            "renderer file count increased from 142 to 157",
            "diff_signal_policy",
            "AI incident workflow",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        for expected in [
            "LLM / AI / RAG eval",
            "llm_ai_rag_contract_present",
            "Prompt inspection is not enough",
            "citations alone do not prove grounding",
            "eval tooling selector",
            "AI incident workflow",
        ]:
            with self.subTest(behavioral_evals=expected):
                self.assertIn(expected, behavioral_evals)

        for expected in [
            "LLM / AI / RAG methodology routing",
            "ai-behavior-spec.md",
            "rag-retrieval-config.md",
            "live model calls",
            "agent-handoff-contract.md",
            "filename-only diffs",
        ]:
            with self.subTest(scenarios=expected):
                self.assertIn(expected, scenarios)

        for expected in [
            "LLM / AI / RAG methodology",
            "llm_ai_rag_contract_present",
            "ai-cost-latency-budget.md",
            "live model calls",
            "agent-task-packet.md",
            "eval tooling selector",
        ]:
            with self.subTest(readme=expected):
                self.assertIn(expected, readme)

        self.assertIn("llm_ai_rag_readiness_when_ai_behavior_changes", development_standards)
        self.assertIn("AI/RAG behavior changes record `llm_ai_rag` evidence", development_standards)

    def test_track9_security_privacy_compliance_docs_and_backlog_are_synced(self):
        backlog = TRACK9_BACKLOG.read_text(encoding="utf-8")
        behavioral_evals = (PRODUCT_AGENT_OS / "behavioral-evals.md").read_text(encoding="utf-8")
        scenarios = (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8")
        methodology_intelligence = (PRODUCT_AGENT_OS / "methodology-intelligence.md").read_text(
            encoding="utf-8"
        )
        development_standards = (PRODUCT_AGENT_OS / "development-standards.md").read_text(
            encoding="utf-8"
        )
        readme = (ROOT / "plugins" / "product-agent-os" / "README.md").read_text(encoding="utf-8")

        for expected in [
            "T9-D11",
            "Security, Privacy & Compliance",
            "security_privacy_compliance_contract_present",
            "renderer file count increased from 157 to 173",
            "Codex Security scan status",
            "docs-only security article",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        for expected in [
            "Security, Privacy & Compliance eval",
            "security_privacy_compliance_contract_present",
            "security_sensitive_classification_present",
            "Codex Security scan is implied",
            "privacy compliance is universal",
        ]:
            with self.subTest(behavioral_evals=expected):
                self.assertIn(expected, behavioral_evals)

        for expected in [
            "Security, Privacy & Compliance methodology routing",
            "threat-surface.md",
            "asvs-ssdf-mapping.md",
            "approval-record.md",
            "Codex Security scans",
        ]:
            with self.subTest(scenarios=expected):
                self.assertIn(expected, scenarios)

        for expected in [
            "Security/Privacy/Compliance",
            "security_privacy_compliance_contract_present",
            "data-classification-register.md",
            "vulnerability-response-record.md",
        ]:
            with self.subTest(methodology_intelligence=expected):
                self.assertIn(expected, methodology_intelligence)

        for expected in [
            "security_privacy_compliance_when_sensitive_surface",
            "Security/Privacy/Compliance-sensitive slices record `security_privacy_compliance` evidence",
        ]:
            with self.subTest(development_standards=expected):
                self.assertIn(expected, development_standards)

        for expected in [
            "Security, Privacy & Compliance methodology",
            "security_privacy_compliance_contract_present",
            "threat-surface.md",
            "Codex Security scan status",
            "approval_required",
        ]:
            with self.subTest(readme=expected):
                self.assertIn(expected, readme)

    def test_track9_delivery_release_operations_docs_and_backlog_are_synced(self):
        backlog = TRACK9_BACKLOG.read_text(encoding="utf-8")
        behavioral_evals = (PRODUCT_AGENT_OS / "behavioral-evals.md").read_text(encoding="utf-8")
        scenarios = (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8")
        methodology_intelligence = (PRODUCT_AGENT_OS / "methodology-intelligence.md").read_text(
            encoding="utf-8"
        )
        development_standards = (PRODUCT_AGENT_OS / "development-standards.md").read_text(
            encoding="utf-8"
        )
        readme = (ROOT / "plugins" / "product-agent-os" / "README.md").read_text(encoding="utf-8")

        for expected in [
            "T9-D12",
            "Implemented scope in batch `M20..M29`",
            "Implemented scope in batch `M30..M40`",
            "delivery_release_operations_contract_present",
            "renderer file count increased from 173 to 186",
            "package-release-approval",
            "release-mobile-signing-only",
            "release-tooling-only",
            "owner-reviewed release evidence sufficiency",
            "active schedules remain out of scope",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        for expected in [
            "Delivery, Release & Operations eval",
            "delivery_release_operations_contract_present",
            "automation_manual_stability_present",
            "release mode policy",
            "build-release-run boundary",
            "DORA metrics prove individual performance",
            "single observability tool is mandatory",
            "owner-reviewed release evidence sufficiency",
            "GitOps is automatically safe",
            "repeatable automation is automatically safe",
        ]:
            with self.subTest(behavioral_evals=expected):
                self.assertIn(expected, behavioral_evals)

        for expected in [
            "Delivery, Release & Operations methodology routing",
            "release-artifact-manifest.md",
            "rollback-recovery-plan.md",
            "automation-candidate.md",
            "release mode policy",
            "platform distribution evidence",
            "observability/on-call tooling",
            "active automation remain approval_required",
        ]:
            with self.subTest(scenarios=expected):
                self.assertIn(expected, scenarios)

        for expected in [
            "Delivery/Release/Operations",
            "delivery_release_operations_contract_present",
            "release-artifact-manifest.md",
            "operations-runbook.md",
            "post-release-review.md",
            "release mode policy",
            "owner-reviewed release evidence sufficiency",
        ]:
            with self.subTest(methodology_intelligence=expected):
                self.assertIn(expected, methodology_intelligence)

        for expected in [
            "delivery_release_operations_readiness_when_release_or_operations_changes",
            "Delivery/Release/Operations slices record `delivery_release_operations` evidence",
            "automation_manual_stability_present",
            "release_evidence_sufficiency_owner_reviewed",
            "DORA metrics prove individual performance",
        ]:
            with self.subTest(development_standards=expected):
                self.assertIn(expected, development_standards)

        for expected in [
            "Delivery, Release & Operations methodology",
            "delivery_release_operations_contract_present",
            "release-artifact-manifest.md",
            "automation_manual_stability_present",
            "release_mode_policy_present",
            "release_evidence_sufficiency_owner_reviewed",
            "approval_required",
        ]:
            with self.subTest(readme=expected):
                self.assertIn(expected, readme)

    def test_track9_cross_domain_synthesis_docs_and_backlog_are_synced(self):
        backlog = TRACK9_BACKLOG.read_text(encoding="utf-8")
        behavioral_evals = (PRODUCT_AGENT_OS / "behavioral-evals.md").read_text(encoding="utf-8")
        methodology_intelligence = (PRODUCT_AGENT_OS / "methodology-intelligence.md").read_text(
            encoding="utf-8"
        )
        development_standards = (PRODUCT_AGENT_OS / "development-standards.md").read_text(
            encoding="utf-8"
        )

        for expected in [
            "T9-S-M10..M14",
            "cross_domain_synthesis_contract_present",
            "safe_next_action_risk_ordered",
            "source_artifact_mapping_contract_present",
            "cross_domain_false_positive_guards_present",
            "semantic evidence sufficiency review ownership",
            "source artifact alias/deferred decisions",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        for expected in [
            "Cross-domain synthesis eval",
            "cross_domain_synthesis_contract_present",
            "safe_next_action_risk_ordered",
            "source_artifact_mapping_contract_present",
            "cross_domain_false_positive_guards_present",
            "generic quality strategy hides security approval",
        ]:
            with self.subTest(behavioral_evals=expected):
                self.assertIn(expected, behavioral_evals)

        for expected in [
            "Cross-Domain Synthesis",
            "recommendation_groups",
            "methodology_synthesis",
            "source_artifact_ledger",
            "risk-aware safe next action",
            "owner domains",
            "consumer domains",
            "semantic evidence sufficiency",
            "approval-bound behavior",
        ]:
            with self.subTest(methodology_intelligence=expected):
                self.assertIn(expected, methodology_intelligence)

        for expected in [
            "semantic evidence sufficiency",
            "owner_reviewed_evidence_sufficient_for_real_project_risk",
            "explicit_gap_accepted",
            "detection alone remains `present_unverified`",
            "grouped methodology recommendations",
            "approval-bound behavior",
        ]:
            with self.subTest(development_standards=expected):
                self.assertIn(expected, development_standards)

    def test_task22_final_docs_sync_user_facing_stack_is_closed(self):
        documents = {
            "index": (PRODUCT_AGENT_OS / "index.md").read_text(encoding="utf-8"),
            "architecture": (PRODUCT_AGENT_OS / "architecture.md").read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "methodology": (PRODUCT_AGENT_OS / "methodology-intelligence.md").read_text(
                encoding="utf-8"
            ),
            "scenarios": (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8"),
            "behavioral_evals": (PRODUCT_AGENT_OS / "behavioral-evals.md").read_text(
                encoding="utf-8"
            ),
            "codex_compatibility": (PRODUCT_AGENT_OS / "codex-compatibility.md").read_text(
                encoding="utf-8"
            ),
            "development_standards": (PRODUCT_AGENT_OS / "development-standards.md").read_text(
                encoding="utf-8"
            ),
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
        }

        expected_terms = {
            "index": [
                "Task 22 final documentation sync closure",
                "Tracks 1-9 are implementation provenance",
                "inspect workspace",
                "stage infrastructure",
                "approved merge",
                "Codex-only runtime",
                "conditional methodology gates",
                "evidence before completion",
            ],
            "architecture": [
                "Task 22 layer map",
                "Track 1 foundation",
                "Track 2 lifecycle skills",
                "Track 3 staged generation",
                "Track 4 approved merge",
                "Track 5 Codex runtime",
                "Track 6 engineering standards",
                "Track 7 hardening",
                "Track 8 scenario workflows",
                "Track 9 methodology intelligence",
            ],
            "technical": [
                "Task 22 operator contract",
                "base workspace audit profile",
                "Track 9 methodology audit complexity",
                "schema v1 additive compatibility",
                "codex_runner_result",
                "renderer_file_count",
                "run_methodology_audit.py",
                "run_transcript_eval.py",
            ],
            "methodology": [
                "Task 22 final methodology contract",
                "methodology_packet",
                "finish_options",
                "owner_questions",
                "safe_next_action",
                "source_artifact_ledger",
                "staged artifact boundary",
            ],
            "scenarios": [
                "Task 22 scenario closure",
                "finish_options",
                "safe_next_action",
                "bug_rescue",
                "greenfield_idea",
                "api_migration",
                "ai_eval_regression",
                "security_sensitive_change",
                "release_packaging",
            ],
            "behavioral_evals": [
                "Task 22 eval closure",
                "fixture eval limits",
                "runtime packet safety",
                "transcript/session replay",
                "synthetic regression evidence does not prove real project readiness",
            ],
            "codex_compatibility": [
                "Task 22 canonical safety boundary",
                "no live model call",
                "no global config mutation",
                "no readiness claims from detection",
                "hosted docs or DB introspection require approval",
            ],
            "development_standards": [
                "Task 22 standards closure",
                "Track 7 artifact catalog",
                "Red-Green-Refactor evidence",
                "no-forced-ceremony",
                "mechanical edits can be not_applicable",
                "owner_reviewed_evidence_sufficient_for_real_project_risk",
            ],
            "root_readme": [
                "Task 22 final documentation sync closure",
                "Product-Agent OS full stack",
                "Track 1-9",
                "Codex-only runtime",
                "methodology intelligence",
            ],
            "plugin_readme": [
                "Task 22 final documentation sync closure",
                "Product-Agent OS full stack",
                "Track 1-9",
                "schema v1 additive compatibility",
                "staged artifact boundary",
            ],
        }

        for document, terms in expected_terms.items():
            for term in terms:
                with self.subTest(document=document, term=term):
                    self.assertIn(term, documents[document])

    def test_task22_source_registry_and_control_plane_closure_are_documented(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
            "plan": PLAN.read_text(encoding="utf-8"),
            "test": TEST.read_text(encoding="utf-8"),
            "evals": EVALS.read_text(encoding="utf-8"),
            "runlog": RUNLOG.read_text(encoding="utf-8"),
            "track9_plan": TRACK9_PLAN.read_text(encoding="utf-8"),
            "track10_plan": TRACK10_PLAN.read_text(encoding="utf-8"),
        }

        for expected in [
            "Product-Agent OS Track 1-9 final documentation closure",
            "Task 22 final documentation sync closure",
            "Product-Agent OS pre-Track 8 implemented plans and specs inventory",
            "Product-Agent OS Track 9 methodology intelligence design and backlog",
            "docs/product-agent-os/methodology-intelligence.md",
            "plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py",
            "plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py",
            "OpenAPI v3.2.0 freshness claim",
            "verification_status:",
        ]:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        expected_by_file = {
            "requirements": [
                "Task 22 final documentation sync closure",
                "Track 1-9 acceptance",
                "legacy Track 9 `Task 23: Final Verification Baseline` is absorbed into Task 22",
            ],
            "plan": [
                "| 17 | `Task 22` final Track 9 documentation sync | `done` |",
                "Track 10 `Task 23` starts only after Task 22 closure",
            ],
            "test": [
                "Task 22 final documentation sync closure",
                "python -m unittest tests.product_agent_os.test_product_agent_os_docs -v",
                "python plugins\\product-agent-os\\scripts\\run_transcript_eval.py",
                "git diff --check",
            ],
            "evals": [
                "Task 22 final documentation sync closure",
                "readiness/evidence quality",
                "stale Track 1-9 claims",
                "synthetic eval evidence limits",
            ],
            "runlog": [
                "Task 22 final documentation sync closure",
                "source inventory links",
                "legacy Track 9 Task 23 baseline absorbed into Task 22",
            ],
            "track9_plan": [
                "### Legacy Track 9 Final Verification Baseline (absorbed into Task 22)",
                "`T22-U-M23`",
            ],
            "track10_plan": [
                "Task 22 absorbs that verification baseline into `T22-U-M23`",
                "Track 10 uses `Task 23` for the next product capability",
            ],
        }

        for filename, terms in expected_by_file.items():
            for term in terms:
                with self.subTest(control_plane=filename, term=term):
                    self.assertIn(term, control_plane[filename])

        self.assertNotIn(
            "The current Track 9 plan still contains a legacy `Task 23: Final Verification Baseline`",
            control_plane["track10_plan"],
        )


if __name__ == "__main__":
    unittest.main()
