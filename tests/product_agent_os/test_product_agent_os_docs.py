import unittest
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
PRODUCT_AGENT_OS = DOCS / "product-agent-os"
MKDOCS = ROOT / "mkdocs.yml"
CHECK_DOCS = ROOT / "tools" / "check_docs.py"
SOURCE_REGISTRY = DOCS / "sources" / "registry.md"
TRACK_BACKLOG = DOCS / "sources" / "product-agent-os-track-8-detailed-backlog.md"
TRACK9_BACKLOG = DOCS / "sources" / "product-agent-os-track-9-backlog.md"
TRACK10_BACKLOG = DOCS / "sources" / "product-agent-os-track-10-backlog.md"
BATCH34_PACKAGING_SMOKE = DOCS / "sources" / "product-agent-os-batch34-packaging-install-smoke.md"
BATCH34A_PUBLIC_DOCS_BOUNDARY = (
    DOCS / "sources" / "product-agent-os-batch34a-public-docs-boundary.md"
)
BATCH34B_PUBLIC_COPY_REWRITE = (
    DOCS / "sources" / "product-agent-os-batch34b-public-copy-rewrite.md"
)
BATCH35_APPROVAL_DRAFT = DOCS / "sources" / "product-agent-os-batch35-approval-packet-draft.md"
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
    def _internal_history_documents(self, documents):
        internal = {
            name: text
            for name, text in documents.items()
            if name in {"root_readme", "plugin_readme"}
        }
        return internal or documents

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
            "Self-Verification And Modernization Loop",
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
        for document, text in self._internal_history_documents(documents).items():
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
        for document, text in self._internal_history_documents(documents).items():
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
        for document, text in self._internal_history_documents(documents).items():
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
        for document, text in self._internal_history_documents(documents).items():
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
        for document, text in self._internal_history_documents(documents).items():
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
        for document, text in self._internal_history_documents(documents).items():
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
        for document, text in self._internal_history_documents(documents).items():
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
        for document, text in self._internal_history_documents(documents).items():
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
        for document, text in self._internal_history_documents(documents).items():
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

    def test_track10_task26_batch29_human_review_ledger_and_diff_preview_is_synced(self):
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
            "Product-Agent OS Track 10 Task 26 Batch 29 human review ledger and proposal diff preview",
            "T10-LIVE-M17..M18",
            "project_graph_review_ledger.py",
            "graph-review-ledger.json",
            "proposal-diff.json",
            "project_graph_human_review_ledger_present",
            "project_graph_proposal_diff_preview_present",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "Task 26 Batch 29 Closure",
            "| `done` | `T10-LIVE-M17..M18` human review ledger and proposal diff preview |",
            "Batch 29 explicit approval",
            "project_graph_review_ledger.py",
            "graph-review-ledger.json",
            "proposal-diff.json",
            "No accepted proposal without owner decision",
            "Accept, reject or accepted_gap decisions with evidence refs",
            "Human can inspect before mutation",
            "proposal-only until Batch 30 dry-run mutation",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 26 Batch 29",
            "T10-LIVE-M17..M18",
            "Human Review Ledger And Proposal Diff Preview",
            "project_graph_review_ledger.py",
            "graph-review-ledger.json",
            "proposal-diff.json",
            "project_graph_human_review_ledger",
            "project_graph_proposal_diff_preview",
            "batch29_human_review_ledger_and_proposal_diff_preview",
            "human_review_ledger",
            "proposal_diff_preview",
            "accepted",
            "rejected",
            "accepted_gap",
            "No accepted proposal without owner decision",
            "Accept, reject or accepted_gap decisions with evidence refs",
            "Human can inspect before mutation",
            "proposal-only until Batch 30 dry-run mutation",
            "provider_call_allowed",
            "external_call_performed",
            "staged evidence only",
            "not source of truth",
            "no provider calls",
            "no live external model/API calls",
            "no canonical graph mutation",
        ]
        for document, text in self._internal_history_documents(documents).items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 26 Batch 29",
            "T10-LIVE-M17..M18",
            "project_graph_review_ledger.py",
            "graph-review-ledger.json",
            "proposal-diff.json",
            "project_graph_human_review_ledger_present",
            "project_graph_human_review_ledger_governance_prerequisite_present",
            "project_graph_human_review_ledger_owner_decision_required_present",
            "project_graph_human_review_ledger_evidence_refs_present",
            "project_graph_human_review_accepted_gap_present",
            "project_graph_proposal_diff_preview_present",
            "project_graph_proposal_diff_inspectable_changes_present",
            "project_graph_proposal_diff_no_canonical_mutation_present",
            "project_graph_human_review_ledger_no_live_calls_present",
            "No accepted proposal without owner decision",
            "Accept, reject or accepted_gap decisions with evidence refs",
            "Human can inspect before mutation",
            "proposal-only until Batch 30 dry-run mutation",
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

    def test_track10_task26_batch30_canonical_mutation_journal_and_rollback_is_synced(self):
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
            "Product-Agent OS Track 10 Task 26 Batch 30 canonical graph mutation journal and rollback",
            "T10-LIVE-M19..M22",
            "project_graph_canonical_mutation.py",
            "canonical_graph_mutation.py",
            "graph_rollback.py",
            "mutation_plan.json",
            "graph-mutation-journal.jsonl",
            "project_graph_canonical_mutation_dry_run_plan_present",
            "project_graph_rollback_previous_digest_restore_present",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "Task 26 Batch 30 Closure",
            "| `done` | `T10-LIVE-M19..M22` canonical graph mutation journal and rollback |",
            "Batch 30 explicit approval",
            "project_graph_canonical_mutation.py",
            "mutation_plan.json",
            "graph-mutation-journal.jsonl",
            "No mutation without dry-run plan",
            "Every mutation has rollback patch",
            "Only accepted proposals mutate graph",
            "Rollback restores previous graph digest",
            "accepted_gap remains non-mutating",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 26 Batch 30",
            "T10-LIVE-M19..M22",
            "Canonical Graph Mutation, Journal And Rollback Engine",
            "project_graph_canonical_mutation.py",
            "canonical_graph_mutation.py",
            "graph_rollback.py",
            "mutation_plan.json",
            "graph-mutation-journal.jsonl",
            "project_graph_canonical_mutation_plan",
            "project_graph_mutation_journal",
            "project_graph_rollback_proof",
            "batch30_canonical_graph_mutation_journal_and_rollback",
            "canonical_mutation_dry_run",
            "mutation_journal",
            "accepted_mutation_apply",
            "rollback_engine",
            "No mutation without dry-run plan",
            "Every mutation has rollback patch",
            "Only accepted proposals mutate graph",
            "Rollback restores previous graph digest",
            "accepted_gap remains non-mutating",
            "stage-root generated graph copy only",
            "provider_call_allowed",
            "external_call_performed",
            "staged evidence only",
            "not source of truth",
            "no provider calls",
            "no live external model/API calls",
        ]
        for document, text in self._internal_history_documents(documents).items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 26 Batch 30",
            "T10-LIVE-M19..M22",
            "project_graph_canonical_mutation.py",
            "mutation_plan.json",
            "graph-mutation-journal.jsonl",
            "project_graph_canonical_mutation_dry_run_plan_present",
            "project_graph_canonical_mutation_governance_prerequisite_present",
            "project_graph_canonical_mutation_conflict_checks_present",
            "project_graph_mutation_journal_append_only_present",
            "project_graph_mutation_journal_rollback_patch_present",
            "project_graph_canonical_mutation_only_accepted_proposals_present",
            "project_graph_canonical_mutation_apply_digest_present",
            "project_graph_rollback_previous_digest_restore_present",
            "project_graph_canonical_mutation_no_live_calls_present",
            "No mutation without dry-run plan",
            "Every mutation has rollback patch",
            "Only accepted proposals mutate graph",
            "Rollback restores previous graph digest",
            "accepted_gap remains non-mutating",
            "provider_call_allowed",
            "external_call_performed",
            "no provider calls",
            "no live external model/API calls",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task26_batch31_audit_security_observability_and_handoff_is_synced(self):
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
            "Product-Agent OS Track 10 Task 26 Batch 31 audit logging security privacy observability and agent skill routing",
            "T10-LIVE-M23..M26",
            "project_graph_live_audit.py",
            "audit-log.jsonl",
            "runtime-observability.json",
            "agent-skill-handoff.json",
            "project_graph_live_audit_log_present",
            "project_graph_live_audit_no_live_calls_present",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "Task 26 Batch 31 Closure",
            "| `done` | `T10-LIVE-M23..M26` audit logging security/privacy observability and agent/skill routing |",
            "Batch 31 explicit approval",
            "project_graph_live_audit.py",
            "audit-log.jsonl",
            "security-privacy.json",
            "runtime-observability.json",
            "agent-skill-handoff.json",
            "redacted append-only audit evidence",
            "Unsafe secret/path/raw-source/prompt-injection cases are blocked",
            "Runtime health, latency, provider errors, budget usage and degraded graph-only mode",
            "ownership, verification evidence, fresh context and stop conditions",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 26 Batch 31",
            "T10-LIVE-M23..M26",
            "Audit Logging, Security/Privacy Tests, Observability And Agent/Skill Routing",
            "project_graph_live_audit.py",
            "audit-log.jsonl",
            "security-privacy.json",
            "runtime-observability.json",
            "agent-skill-handoff.json",
            "project_graph_live_audit_log",
            "project_graph_live_security_privacy_tests",
            "project_graph_runtime_observability",
            "project_graph_agent_skill_handoff_routing",
            "batch31_audit_security_observability_agent_skill_routing",
            "audit_logging",
            "security_privacy_tests",
            "runtime_observability",
            "agent_skill_handoff_routing",
            "redacted append-only audit event",
            "unsafe secret/path/raw-source/prompt-injection cases are blocked",
            "runtime health, latency, provider errors, budget usage and degraded graph-only mode",
            "ownership, verification evidence, fresh context and stop conditions",
            "provider_call_allowed",
            "external_call_performed",
            "staged evidence only",
            "not source of truth",
            "no live server",
            "no provider calls",
            "no live external model/API calls",
            "no canonical graph mutation",
        ]
        for document, text in self._internal_history_documents(documents).items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 26 Batch 31",
            "T10-LIVE-M23..M26",
            "project_graph_live_audit.py",
            "audit-log.jsonl",
            "security-privacy.json",
            "runtime-observability.json",
            "agent-skill-handoff.json",
            "project_graph_live_audit_log_present",
            "project_graph_live_audit_governance_prerequisite_present",
            "project_graph_live_audit_event_coverage_present",
            "project_graph_live_audit_redaction_append_only_present",
            "project_graph_live_security_privacy_tests_present",
            "project_graph_live_security_privacy_negative_cases_blocked_present",
            "project_graph_live_runtime_observability_present",
            "project_graph_live_runtime_observability_degraded_mode_visible_present",
            "project_graph_live_agent_skill_handoff_routing_present",
            "project_graph_live_agent_skill_handoff_stop_conditions_present",
            "project_graph_live_audit_operability_stage_disable_present",
            "project_graph_live_audit_no_live_calls_present",
            "redacted append-only audit event",
            "unsafe secret/path/raw-source/prompt-injection cases are blocked",
            "runtime health, latency, provider errors, budget usage",
            "degraded graph-only mode",
            "ownership",
            "verification evidence",
            "fresh context",
            "stop conditions",
            "provider_call_allowed",
            "external_call_performed",
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

    def test_track10_task26_batch32_real_testing_readiness_and_pilot_is_synced(self):
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
            "Product-Agent OS Track 10 Task 26 Batch 32 real testing readiness target consent pilot harness and Codex surface smoke",
            "T10-LIVE-M27..M31",
            "project_graph_real_testing.py",
            "real-testing-readiness.json",
            "pilot-harness.json",
            "codex-surface-smoke.json",
            "real-testing-pilot-matrix.json",
            "project_graph_real_testing_readiness_present",
            "project_graph_real_testing_stage_disable_present",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "Task 26 Batch 32 Closure",
            "| `done` | `T10-LIVE-M27..M31` real testing readiness target consent pilot harness and Codex surface smoke |",
            "Batch 32 explicit approval",
            "project_graph_real_testing.py",
            "real-testing-readiness.json",
            "real-testing-targets.json",
            "pilot-harness.json",
            "codex-surface-smoke.json",
            "real-testing-pilot-matrix.json",
            "No real project test without owner-approved target and data policy",
            "Pilot harness remains dry-run and stage-only",
            "Codex App, CLI and IDE extension smoke",
            "Track 8 archetypes",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 26 Batch 32",
            "T10-LIVE-M27..M31",
            "Real Testing Readiness, Target Consent, Pilot Harness And Codex Surface Smoke",
            "project_graph_real_testing.py",
            "real-testing-readiness.json",
            "real-testing-targets.json",
            "pilot-harness.json",
            "codex-surface-smoke.json",
            "real-testing-pilot-matrix.json",
            "project_graph_real_testing_readiness",
            "project_graph_real_testing_targets",
            "project_graph_pilot_harness",
            "project_graph_codex_surface_smoke",
            "project_graph_real_testing_pilot_matrix",
            "batch32_real_testing_readiness_target_consent_pilot_harness_codex_surface_smoke",
            "real_testing_readiness",
            "real_project_target_selection",
            "pilot_harness",
            "codex_surface_smoke",
            "use_case_pilot_matrix",
            "no hidden unresolved Track 10 gates",
            "owner-approved target and data policy",
            "dry-run pilot harness",
            "Codex App, CLI and IDE extension",
            "Track 8 archetypes",
            "staged evidence only",
            "not source of truth",
            "no live server",
            "no provider calls",
            "no live external model/API calls",
            "no canonical graph mutation",
        ]
        for document, text in self._internal_history_documents(documents).items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 26 Batch 32",
            "T10-LIVE-M27..M31",
            "project_graph_real_testing.py",
            "real-testing-readiness.json",
            "real-testing-targets.json",
            "pilot-harness.json",
            "codex-surface-smoke.json",
            "real-testing-pilot-matrix.json",
            "project_graph_real_testing_readiness_present",
            "project_graph_real_testing_target_consent_present",
            "project_graph_real_testing_pilot_harness_present",
            "project_graph_real_testing_codex_surface_smoke_present",
            "project_graph_real_testing_use_case_pilot_matrix_present",
            "project_graph_real_testing_no_hidden_track10_gates_present",
            "project_graph_real_testing_no_unapproved_actions_present",
            "project_graph_real_testing_stage_disable_present",
            "no hidden unresolved Track 10 gates",
            "owner-approved target and data policy",
            "dry-run pilot harness",
            "Codex App, CLI and IDE extension",
            "Track 8 archetypes",
            "provider_call_allowed",
            "external_call_performed",
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

    def test_track10_task26_batch33_runtime_qa_performance_stabilization_is_synced(self):
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
            "Product-Agent OS Track 10 Task 26 Batch 33 runtime browser QA performance and stabilization",
            "T10-LIVE-M32..M34",
            "project_graph_runtime_qa.py",
            "runtime-browser-qa.json",
            "performance-budget.json",
            "stabilization-ledger.json",
            "project_graph_runtime_browser_qa_present",
            "project_graph_performance_budget_threshold_fallback_present",
            "project_graph_stabilization_no_open_p0_p1_present",
            "project_graph_runtime_qa_stage_disable_present",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "Task 26 Batch 33 Closure",
            "| `done` | `T10-LIVE-M32..M34` runtime browser QA performance and stabilization |",
            "Batch 33 explicit approval",
            "browser smoke",
            "console/network checks",
            "mobile overflow",
            "generated-view labels",
            "source-boundary labels",
            "budget breach disables live layer or records accepted gap",
            "No open P0/P1",
            "git staging/commit/push/PR remains explicit-only",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 26 Batch 33",
            "T10-LIVE-M32..M34",
            "Runtime Browser QA, Performance And Stabilization",
            "project_graph_runtime_qa.py",
            "project-code-graph-runtime-browser-qa.json",
            "project-code-graph-performance-budget.json",
            "project-code-graph-stabilization-ledger.json",
            "project_graph_runtime_browser_qa",
            "project_graph_performance_budget",
            "project_graph_stabilization_ledger",
            "batch33_runtime_browser_qa_performance_stabilization",
            "runtime_browser_qa",
            "runtime_performance_budget",
            "runtime_stabilization_loop",
            "browser smoke",
            "console/network checks",
            "mobile overflow",
            "generated-view labels",
            "source-boundary labels",
            "budget breach disables live layer or records accepted gap",
            "No open P0/P1",
            "staged evidence only",
            "not source of truth",
            "no live server",
            "no provider calls",
            "no live external model/API calls",
            "no canonical graph mutation",
        ]
        for document, text in self._internal_history_documents(documents).items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 26 Batch 33",
            "T10-LIVE-M32..M34",
            "project_graph_runtime_qa.py",
            "runtime-browser-qa.json",
            "performance-budget.json",
            "stabilization-ledger.json",
            "project_graph_runtime_browser_qa_present",
            "project_graph_runtime_browser_qa_console_network_checks_present",
            "project_graph_runtime_browser_qa_mobile_overflow_labels_present",
            "project_graph_performance_budget_present",
            "project_graph_performance_budget_threshold_fallback_present",
            "project_graph_stabilization_ledger_present",
            "project_graph_stabilization_no_open_p0_p1_present",
            "project_graph_runtime_qa_no_unapproved_actions_present",
            "project_graph_runtime_qa_stage_disable_present",
            "browser smoke",
            "console/network checks",
            "mobile overflow",
            "generated-view labels",
            "source-boundary labels",
            "budget breach disables live layer or records accepted gap",
            "No open P0/P1",
            "provider_call_allowed",
            "external_call_performed",
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

    def test_track10_task26_batch34_docs_packaging_closure_matrix_is_planned(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        plan = TRACK10_PLAN.read_text(encoding="utf-8")
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

        matrix_terms = [
            "Task 26 Batch 34",
            "T10-LIVE-M35..M36",
            "Batch 34 Detailed Task Matrix",
            "B34-DOC-M01",
            "B34-DOC-M15",
            "docs/product-agent-os/project-code-graph.md",
            "docs/product-agent-os/live-runtime-governance.md",
            "docs/product-agent-os/approval-bound-real-testing.md",
            "docs/product-agent-os/agent-skill-modernization-loop.md",
            "docs/product-agent-os/cli-reference.md",
            "docs/product-agent-os/artifact-contracts.md",
            "docs/product-agent-os/packaging-and-closure.md",
            "project_graph_sanitization.py",
            "docs/product-agent/product-agent-os-plugin-spec.md",
            "python -m mkdocs build --strict",
            "site/",
            "docs-maintainer plugin-cache gap",
            "Mermaid external asset gap",
            "staged evidence only",
            "not source of truth",
            "no live server",
            "no browser automation",
            "no provider/live external model/API calls",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]
        for expected in matrix_terms:
            with self.subTest(plan=expected):
                self.assertIn(expected, plan)

        backlog_terms = [
            "Task 26 Batch 34 Planned Matrix",
            "| `approval_required` | `T10-LIVE-M35..M36` docs packaging source registry site closure and Batch 35 handoff |",
            "Batch 34 implements the documentation and packaging closure plan",
            "B34-DOC-M01..M15",
            "source docs -> registry -> docs tests -> check_docs.py -> strict MkDocs -> optional full closure",
            "site/ must be rebuilt with the regular MkDocs site_dir",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        registry_terms = [
            "Product-Agent OS Track 10 Task 26 Batch 34 docs packaging closure matrix",
            "T10-LIVE-M35..M36",
            "B34-DOC-M01..M15",
            "project-authored docs pages",
            "`site/` rebuild",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        docs_terms = [
            "Task 26 Batch 34",
            "T10-LIVE-M35..M36",
            "Packaging, Docs, Source Registry, Closure And Batch 35 Handoff",
            "B34-DOC-M01..M15",
            "project-code-graph.md",
            "live-runtime-governance.md",
            "approval-bound-real-testing.md",
            "agent-skill-modernization-loop.md",
            "cli-reference.md",
            "artifact-contracts.md",
            "packaging-and-closure.md",
            "site/",
            "planned, not implemented",
        ]
        for document, text in self._internal_history_documents(documents).items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 26 Batch 34",
            "T10-LIVE-M35..M36",
            "Batch 34 Detailed Task Matrix",
            "B34-DOC-M01..M15",
            "source docs -> registry -> docs tests -> check_docs.py -> strict MkDocs -> optional full closure",
            "docs-maintainer plugin-cache gap",
            "Mermaid external asset gap",
            "packaging/install smoke",
            "Batch 35 approval packet draft",
            "staged evidence only",
            "not source of truth",
            "no live server",
            "no browser automation",
            "no provider/live external model/API calls",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task26_batch34_docs_packet_is_implemented(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        nav = MKDOCS.read_text(encoding="utf-8")
        check_docs = CHECK_DOCS.read_text(encoding="utf-8")
        control_plane = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [ROOT_README, PLUGIN_README, REQUIREMENTS, PLAN, TEST, EVALS, RUNLOG, AGENTS]
        )

        pages = {
            "project-code-graph.md": [
                "Generated graph artifacts are not source of truth",
                "orientation evidence",
                "provider/API calls",
                "canonical graph mutation",
                "git stage/commit/push/PR",
            ],
            "live-runtime-governance.md": [
                "approval packet",
                "data classification",
                "redaction",
                "generated artifacts are labeled as staged evidence and not source of truth",
                "no live server launch during docs/governance preparation",
                "no browser automation during docs/governance preparation",
                "no canonical graph mutation",
                "no git stage/commit/push/PR",
            ],
            "approval-bound-real-testing.md": [
                "planned, not implemented",
                "отдельного explicit owner approval",
                "approved_local_runtime_launch",
                "actual_browser_automation_smoke",
                "approved_provider_api_pilot",
                "approved_canonical_mutation_pilot",
                "explicit_git_release_pr_action",
                "approval_required",
            ],
            "agent-skill-modernization-loop.md": [
                "agent_skill_metrics_loop",
                "staged candidate-only pipeline",
                "self-applied updates",
                "active schedules",
                "live eval/model/API calls",
                "target registry",
                "scorecards",
                "modernization candidates",
            ],
            "cli-reference.md": [
                "Generated outputs are not source of truth",
                "render_infrastructure.py",
                "scan_project_code_graph.py",
                "--build-index",
                "--build-backend",
                "--build-semantic-index",
                "--build-llm-proposals",
                "--validate-live-governance",
                "--build-live-audit",
                "--build-real-testing-readiness",
                "--build-runtime-qa",
            ],
            "artifact-contracts.md": [
                "Generated artifacts are staged evidence only",
                ".codex/product-agent-os/project-code-graph.json",
                ".codex/product-agent-os/project-cockpit.html",
                "project-code-graph-runtime-browser-qa.json",
                "live-server-run-evidence.json",
                "browser-automation-smoke.json",
                "provider-call-evidence.json",
                "canonical-mutation-run.json",
                "git-release-pr-evidence.md",
            ],
            "packaging-and-closure.md": [
                "python -m mkdocs build --strict",
                "approved_local_runtime_launch",
                "actual_browser_automation_smoke",
                "approved_provider_api_pilot",
                "approved_canonical_mutation_pilot",
                "explicit_git_release_pr_action",
                "Packaging and closure work does not perform these actions without a separate explicit owner approval",
                "no live server launch",
                "no browser automation",
                "no provider calls",
                "no live external model/API calls",
                "no canonical graph mutation",
                "no `git add`, commit, push or PR",
            ],
        }

        for filename, terms in pages.items():
            path = PRODUCT_AGENT_OS / filename
            with self.subTest(page=filename, exists=True):
                self.assertTrue(path.exists(), path)
            text = path.read_text(encoding="utf-8")
            with self.subTest(page=filename, source_status=True):
                self.assertIn("Source status: `official + experiment`", text)
            for required_heading in ["Verification", "Risks"]:
                with self.subTest(page=filename, heading=required_heading):
                    self.assertIn(required_heading, text)
            for term in terms:
                with self.subTest(page=filename, term=term):
                    self.assertIn(term, text)

            nav_path = f"product-agent-os/{filename}"
            with self.subTest(nav=nav_path):
                self.assertIn(nav_path, nav)
            with self.subTest(check_docs=nav_path):
                self.assertIn(nav_path.replace("/", '" / "'), check_docs)

        for path in [
            "product-agent/product-agent-os-plugin-spec.md",
            "product-agent-os/project-code-graph.md",
            "product-agent-os/live-runtime-governance.md",
            "product-agent-os/approval-bound-real-testing.md",
            "product-agent-os/agent-skill-modernization-loop.md",
            "product-agent-os/cli-reference.md",
            "product-agent-os/artifact-contracts.md",
            "product-agent-os/packaging-and-closure.md",
        ]:
            with self.subTest(required_nav_path=path):
                self.assertIn(path, nav)
                self.assertIn(path, check_docs)

        for expected in [
            "Product-Agent OS Track 10 Task 26 Batch 34 docs packaging closure matrix",
            "Product-Agent OS Batch 34 project-authored docs packet",
            "docs/product-agent-os/project-code-graph.md",
            "docs/product-agent-os/live-runtime-governance.md",
            "docs/product-agent-os/approval-bound-real-testing.md",
            "docs/product-agent-os/agent-skill-modernization-loop.md",
            "docs/product-agent-os/cli-reference.md",
            "docs/product-agent-os/artifact-contracts.md",
            "docs/product-agent-os/packaging-and-closure.md",
            "Product-Agent OS Batch 34 packaging/install smoke packet",
            "Product-Agent OS Batch 35 approval packet draft",
            "B34-DOC-M15",
            "Generated `site/` pages are review output and not source of truth",
            "no live server",
            "no browser automation",
            "no provider/live external model/API calls",
            "no canonical graph mutation",
            "no git staging/commit/push/PR",
            "verification_status:",
        ]:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        for expected in [
            "Task 26 Batch 34 Planned Matrix And Closure Status",
            "`done_through_m15`",
            "`blocked_without_approval` | Batch 35 execution from Batch 34 handoff",
            "B34-DOC-M15",
            "Batch 35 approval packet draft",
            "site/ must be rebuilt with the regular MkDocs site_dir",
            "staged evidence only",
            "not source of truth",
            "no live server",
            "no browser automation",
            "no provider/live external model/API calls",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        for expected in [
            "B34-DOC-M15",
            "packaging/install smoke",
            "Batch 35 approval packet draft",
            "docs-maintainer plugin-cache gap",
            "accepted Mermaid external asset gap",
            "staged evidence only",
            "not source of truth",
            "no live server",
            "no browser automation",
            "no provider/live external model/API calls",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]:
            with self.subTest(control_plane=expected):
                self.assertIn(expected, control_plane)

    def test_track10_task26_batch34_packaging_handoff_is_recorded(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        smoke = BATCH34_PACKAGING_SMOKE.read_text(encoding="utf-8")
        approval = BATCH35_APPROVAL_DRAFT.read_text(encoding="utf-8")
        control_plane = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [ROOT_README, PLUGIN_README, REQUIREMENTS, PLAN, TEST, EVALS, RUNLOG, AGENTS]
        )

        smoke_terms = [
            "Source status: `internal`",
            "B34-DOC-M15",
            "validate_codex_compatibility.py",
            "status: compatible",
            "checked_docs_maintainer_present: true",
            "cache_docs_maintainer_present: false",
            "checked_skill_count: 12",
            "cache_skill_count: 11",
            "docs-maintainer plugin-cache gap",
            "plugin publication",
            "external writes",
            "hook activation",
            "active schedules or automations",
            "live server launch",
            "browser automation",
            "provider/live external model/API calls",
            "canonical graph mutation",
            "git stage/commit/push/PR",
        ]
        for expected in smoke_terms:
            with self.subTest(packaging_smoke=expected):
                self.assertIn(expected, smoke)

        approval_terms = [
            "Source status: `internal`",
            "T10-LIVE-M37..M41",
            "approval_status: approval_required",
            "approved_local_runtime_launch",
            "actual_browser_automation_smoke",
            "approved_provider_api_pilot",
            "approved_canonical_mutation_pilot",
            "explicit_git_release_pr_action",
            "No local live server launch",
            "No browser automation",
            "No provider/live external model/API calls",
            "No canonical graph mutation",
            "No git stage/commit/push/PR",
        ]
        for expected in approval_terms:
            with self.subTest(batch35_approval=expected):
                self.assertIn(expected, approval)

        registry_terms = [
            "Product-Agent OS Batch 34 packaging/install smoke packet",
            "Product-Agent OS Batch 35 approval packet draft",
            "checked-in `docs-maintainer` presence",
            "installed-cache `docs-maintainer` absence",
            "Batch 35 approval packet draft for `T10-LIVE-M37..M41`",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        for expected in [
            "done_through_m15",
            "B34-DOC-M15",
            "packaging/install smoke",
            "Batch 35 approval packet draft",
            "blocked_without_approval",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        for expected in [
            "B34-DOC-M15",
            "packaging/install smoke",
            "docs-maintainer plugin-cache gap",
            "Batch 35 approval packet draft",
            "no live server",
            "no browser automation",
            "no provider/live external model/API calls",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]:
            with self.subTest(control_plane=expected):
                self.assertIn(expected, control_plane)

    def test_track10_task26_batch34a_product_docs_boundary_is_recorded(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        plan = TRACK10_PLAN.read_text(encoding="utf-8")
        check_docs = CHECK_DOCS.read_text(encoding="utf-8")
        boundary = BATCH34A_PUBLIC_DOCS_BOUNDARY.read_text(encoding="utf-8")

        boundary_terms = [
            "Source status: `internal`",
            "B34-PROD-M16",
            "B34-PROD-M17",
            "B34-PROD-M18",
            "public_product_candidates",
            "internal_evidence",
            "docs/sources/",
            "docs/superpowers/",
            "root control-plane",
            "Product-Agent OS",
            "Proposed public navigation shape",
            "Reader journey map",
            "Page ownership map",
            "Product Docs Lead",
            "Architect",
            "Builder",
            "Tester / Reviewer",
            "public_forbidden_terms",
            "public_ready_pages: []",
            "cleanup_pending_public_candidates",
            "test_policy",
            "activation_condition",
            "staged evidence only",
            "not source of truth",
            "no live server",
            "no browser automation",
            "no provider/API call",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]
        for expected in boundary_terms:
            with self.subTest(boundary=expected):
                self.assertIn(expected, boundary)

        public_candidate_paths = [
            "docs/product-agent-os/index.md",
            "docs/product-agent-os/project-code-graph.md",
            "docs/product-agent-os/live-runtime-governance.md",
            "docs/product-agent-os/approval-bound-real-testing.md",
            "docs/product-agent-os/agent-skill-modernization-loop.md",
            "docs/product-agent-os/cli-reference.md",
            "docs/product-agent-os/artifact-contracts.md",
            "docs/product-agent-os/packaging-and-closure.md",
            "docs/product-agent/product-agent-os-plugin-spec.md",
            "docs/diagrams/index.md",
            "docs/runtime/overview.md",
            "docs/agent-systems/subagents-skills.md",
            "docs/playbooks/docs-update.md",
        ]
        for doc_path in public_candidate_paths:
            with self.subTest(public_candidate=doc_path):
                self.assertIn(doc_path, boundary)

        registry_terms = [
            "Product-Agent OS Batch 34A public docs boundary and IA packet",
            "B34-PROD-M16..M18",
            "public documentation boundary",
            "internal evidence inventory",
            "proposed presentation IA",
            "public-docs forbidden-term policy",
            "cleanup_pending",
            "public_ready",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "`done_through_m18` | Batch 34A product documentation boundary and IA |",
            "B34-PROD-M16..M18",
            "public_product_candidates",
            "internal_evidence",
            "public_forbidden_terms",
            "cleanup_pending",
            "public_ready_pages",
            "Batch 34B public copy rewrite",
            "Batch 34C RU/EN localization",
            "Batch 34D product docs QA and closure",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        plan_terms = [
            "Batch 34A: Product Documentation Boundary And IA",
            "B34-PROD-M16",
            "B34-PROD-M17",
            "B34-PROD-M18",
            "Product-facing pages are listed separately from evidence/control-plane pages",
            "Public pages fail tests if they contain `Task`, `Track`, `Batch`, `T10-*`, `B34-*`",
        ]
        for expected in plan_terms:
            with self.subTest(plan=expected):
                self.assertIn(expected, plan)

        self.assertIn(
            'sources" / "product-agent-os-batch34a-public-docs-boundary.md',
            check_docs,
        )

    def test_track10_task26_batch34a_forbidden_term_policy_is_staged(self):
        boundary = BATCH34A_PUBLIC_DOCS_BOUNDARY.read_text(encoding="utf-8")

        forbidden_pattern = re.compile(
            r"\b(Task|Track|Batch)\b|T[0-9]+-[A-Z0-9-]+|B[0-9]+-[A-Z]+-M[0-9]+"
        )

        self.assertRegex("Task 26 Batch 34 T10-LIVE-M35 B34-PROD-M18", forbidden_pattern)
        self.assertIsNone(forbidden_pattern.search("Product-Agent OS delivery lifecycle"))

        for expected in [
            'exact_words:',
            '- "Task"',
            '- "Track"',
            '- "Batch"',
            'ledger_patterns:',
            '- "T[0-9]+-[A-Z0-9-]+"',
            '- "B[0-9]+-[A-Z]+-M[0-9]+"',
            "Allowed contexts:",
            "internal evidence paths listed in `internal_evidence`",
            "code identifiers, commands, filenames, JSON field names and literal artifact ids",
            "official OpenAI terms",
            "Codex App",
            "CLI",
            "IDE extension",
            "subagents",
            "skills",
            "`AGENTS.md`",
            "memory",
            "sandbox",
            "approvals",
            "MCP",
            "Agents SDK",
        ]:
            with self.subTest(policy=expected):
                self.assertIn(expected, boundary)

        cleanup_pending_pages = [
            PRODUCT_AGENT_OS / "index.md",
            PRODUCT_AGENT_OS / "project-code-graph.md",
            PRODUCT_AGENT_OS / "live-runtime-governance.md",
            PRODUCT_AGENT_OS / "approval-bound-real-testing.md",
            PRODUCT_AGENT_OS / "agent-skill-modernization-loop.md",
            PRODUCT_AGENT_OS / "cli-reference.md",
            PRODUCT_AGENT_OS / "artifact-contracts.md",
            PRODUCT_AGENT_OS / "packaging-and-closure.md",
        ]
        for path in cleanup_pending_pages:
            with self.subTest(cleanup_pending_page=path.name):
                self.assertTrue(path.exists(), path)
                self.assertIn(f"docs/product-agent-os/{path.name}", boundary)
                self.assertIn("cleanup_pending", boundary)

        public_ready_pages = []
        self.assertEqual(public_ready_pages, [])
        for path in public_ready_pages:
            text = path.read_text(encoding="utf-8")
            with self.subTest(public_ready_page=path.name):
                self.assertIsNone(forbidden_pattern.search(text), path)

    def test_track10_task26_batch34b_public_copy_is_product_ready(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        boundary = BATCH34A_PUBLIC_DOCS_BOUNDARY.read_text(encoding="utf-8")
        rewrite = BATCH34B_PUBLIC_COPY_REWRITE.read_text(encoding="utf-8")

        public_ready_pages = [
            PRODUCT_AGENT_OS / "index.md",
            PRODUCT_AGENT_OS / "project-code-graph.md",
            PRODUCT_AGENT_OS / "live-runtime-governance.md",
            PRODUCT_AGENT_OS / "approval-bound-real-testing.md",
            PRODUCT_AGENT_OS / "agent-skill-modernization-loop.md",
            PRODUCT_AGENT_OS / "cli-reference.md",
            PRODUCT_AGENT_OS / "artifact-contracts.md",
            PRODUCT_AGENT_OS / "packaging-and-closure.md",
            PRODUCT_AGENT_OS / "technical.md",
            PRODUCT_AGENT_OS / "development-standards.md",
            PRODUCT_AGENT_OS / "methodology-intelligence.md",
            PRODUCT_AGENT_OS / "scenarios.md",
            PRODUCT_AGENT_OS / "behavioral-evals.md",
            PRODUCT_AGENT_OS / "codex-compatibility.md",
            PRODUCT_AGENT_OS / "architecture.md",
            DOCS / "product-agent" / "overview.md",
            DOCS / "product-agent" / "lifecycle.md",
            DOCS / "product-agent" / "roles.md",
            DOCS / "product-agent" / "control-plane.md",
            DOCS / "product-agent" / "product-agent-os-plugin-spec.md",
            DOCS / "diagrams" / "index.md",
            DOCS / "diagrams" / "architecture.md",
            DOCS / "diagrams" / "product-delivery-lifecycle.md",
            DOCS / "diagrams" / "agent-team-and-skills.md",
            DOCS / "diagrams" / "runtime-decision-map.md",
            DOCS / "diagrams" / "skill-lifecycle.md",
            DOCS / "diagrams" / "context-memory-verification.md",
            DOCS / "runtime" / "overview.md",
            DOCS / "runtime" / "non-interactive-and-mcp.md",
            DOCS / "runtime" / "automations-github.md",
            DOCS / "runtime" / "worktrees-hooks-rules.md",
            DOCS / "agent-systems" / "subagents-skills.md",
            DOCS / "playbooks" / "docs-update.md",
            DOCS / "playbooks" / "use-case-to-plugin.md",
            DOCS / "playbooks" / "workspace-readiness-audit.md",
        ]

        forbidden_pattern = re.compile(
            r"\b(Task|Track|Batch)\b|T[0-9]+-[A-Z0-9-]+|B[0-9]+-[A-Z]+-M[0-9]+"
        )
        allowed_public_matches = {}

        for path in public_ready_pages:
            with self.subTest(public_ready_exists=path):
                self.assertTrue(path.exists(), path)

            rel_path = path.relative_to(ROOT).as_posix()
            text = path.read_text(encoding="utf-8")
            with self.subTest(source_status=rel_path):
                self.assertIn("Source status:", text)

            unexpected = []
            allowed = allowed_public_matches.get(path, [])
            for line in text.splitlines():
                if forbidden_pattern.search(line) and line not in allowed:
                    unexpected.append(line)
            with self.subTest(forbidden_terms=rel_path):
                self.assertEqual([], unexpected)

            with self.subTest(packet_lists_ready_page=rel_path):
                self.assertIn(rel_path, rewrite)

        for expected in [
            "Source status: `internal`",
            "B34-PROD-M19..M23",
            "public_ready_pages",
            "Product-Agent OS overview",
            "core concept pages",
            "reference pages",
            "scenario and quality pages",
            "diagram and bridge pages",
            "internal ledger language removed",
            "Source status preserved",
            "no live server",
            "no browser automation",
            "no provider/live external model/API calls",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]:
            with self.subTest(rewrite_packet=expected):
                self.assertIn(expected, rewrite)

        for expected in [
            "Product-Agent OS Batch 34B public copy rewrite packet",
            "B34-PROD-M19..M23",
            "internal ledger language removed from public-ready pages",
            "verification_status:",
        ]:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        for expected in [
            "`done_through_m23` | Batch 34B public copy rewrite |",
            "B34-PROD-M19..M23",
            "public_ready_pages",
            "internal ledger language removed",
            "Batch 34C RU/EN localization",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        self.assertIn("public_ready_pages:", boundary)
        self.assertIn("cleanup_pending_public_candidates: []", boundary)

    def test_track10_task26_batch35_real_testing_execution_matrix_is_planned(self):
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
            "Product-Agent OS Track 10 Task 26 Batch 35 approval-bound real testing execution matrix",
            "T10-LIVE-M37..M41",
            "batch35_approval_bound_real_testing_execution",
            "approved_local_runtime_launch",
            "actual_browser_automation_smoke",
            "approved_provider_api_pilot",
            "approved_canonical_mutation_pilot",
            "explicit_git_release_pr_action",
            "live-server-run-evidence.json",
            "browser-automation-smoke.json",
            "provider-call-evidence.json",
            "canonical-mutation-run.json",
            "git-release-pr-evidence.md",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "Task 26 Batch 35 Planned Matrix",
            "| `approval_required` | `T10-LIVE-M37..M41` approval-bound real testing execution matrix |",
            "approved_local_runtime_launch",
            "actual_browser_automation_smoke",
            "approved_provider_api_pilot",
            "approved_canonical_mutation_pilot",
            "explicit_git_release_pr_action",
            "starts no live server",
            "runs no browser automation",
            "performs no provider/live external model/API calls",
            "performs no canonical graph mutation",
            "performs no git stage/commit/push/PR",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 26 Batch 35",
            "T10-LIVE-M37..M41",
            "Approval-Bound Real Testing Execution Matrix",
            "planned, not implemented",
            "approved_local_runtime_launch",
            "actual_browser_automation_smoke",
            "approved_provider_api_pilot",
            "approved_canonical_mutation_pilot",
            "explicit_git_release_pr_action",
            "batch35_approval_bound_real_testing_execution",
            "no live server",
            "no browser automation",
            "no provider/live external model/API calls",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]
        for document, text in self._internal_history_documents(documents).items():
            for expected in docs_terms:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        control_terms = [
            "Task 26 Batch 35",
            "T10-LIVE-M37..M41",
            "Approval-Bound Real Testing Execution Matrix",
            "batch35_approval_bound_real_testing_execution",
            "approved_local_runtime_launch",
            "actual_browser_automation_smoke",
            "approved_provider_api_pilot",
            "approved_canonical_mutation_pilot",
            "explicit_git_release_pr_action",
            "no live server",
            "no browser automation",
            "no provider/live external model/API calls",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
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
        for document, text in self._internal_history_documents(documents).items():
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
        for document, text in self._internal_history_documents(documents).items():
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
        for document, text in self._internal_history_documents(documents).items():
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
        for document, text in self._internal_history_documents(documents).items():
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
                "Executive overview",
                "Current operating boundary",
                "read-only workspace audit",
                "staged infrastructure",
                "generated evidence",
                "source of truth",
                "approval",
                "evidence-before-completion",
            ],
            "architecture": [
                "Layered Model",
                "Plugin package",
                "Lifecycle skills",
                "Staged infrastructure",
                "Approved merge",
                "Codex runtime runner",
                "Engineering standards",
                "Scenario routes",
                "Methodology intelligence",
            ],
            "technical": [
                "base workspace audit profile",
                "methodology audit complexity",
                "schema v1 additive compatibility",
                "codex_runner_result",
                "renderer_file_count",
                "run_methodology_audit.py",
                "run_transcript_eval.py",
            ],
            "methodology": [
                "Methodology intelligence is the read-only layer",
                "methodology_packet",
                "finish_options",
                "owner_questions",
                "safe_next_action",
                "source_artifact_ledger",
                "staged proposal",
            ],
            "scenarios": [
                "Operator Route Map",
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
                "Runtime Packet Safety",
                "Fixture eval and docs tests prove",
                "route safety",
                "transcript/session replay",
                "They do not prove real project readiness",
            ],
            "codex_compatibility": [
                "Canonical Safety Boundary",
                "no live model call",
                "no global config mutation",
                "no readiness claims from detection",
                "no hosted docs or DB introspection bypass",
            ],
            "development_standards": [
                "Development standards turn methodology into concrete reviewable artifacts",
                "Artifact Templates",
                "Red-Green-Refactor evidence",
                "no-forced-ceremony",
                "mechanical edits can be not_applicable",
                "owner_reviewed_evidence_sufficient_for_real_project_risk",
            ],
            "root_readme": [
                "Product-Agent OS full stack",
                "Codex-only runtime",
                "methodology intelligence",
                "staged evidence only",
            ],
            "plugin_readme": [
                "Product-Agent OS full stack",
                "schema v1 additive compatibility",
                "staged artifact boundary",
                "Codex App, CLI, and IDE extension",
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
