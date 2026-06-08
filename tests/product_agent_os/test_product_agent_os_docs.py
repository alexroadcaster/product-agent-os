import unittest
import json
from pathlib import Path
import re
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
PRODUCT_AGENT_OS = DOCS / "product-agent-os"
MKDOCS = ROOT / "mkdocs.yml"
CHECK_DOCS = ROOT / "tools" / "check_docs.py"
SITE = ROOT / "site"
LOCAL_FILE_I18N_JS = DOCS / "assets" / "javascripts" / "local-file-i18n.js"
SOURCE_REGISTRY = DOCS / "sources" / "registry.md"
SOURCE_REGISTRY_EN = DOCS / "sources" / "registry.en.md"
TRACK_BACKLOG = DOCS / "sources" / "product-agent-os-track-8-detailed-backlog.md"
TRACK9_BACKLOG = DOCS / "sources" / "product-agent-os-track-9-backlog.md"
TRACK10_BACKLOG = DOCS / "sources" / "product-agent-os-track-10-backlog.md"
TRACK10_BACKLOG_EN = DOCS / "sources" / "product-agent-os-track-10-backlog.en.md"
BATCH34_PACKAGING_SMOKE = DOCS / "sources" / "product-agent-os-batch34-packaging-install-smoke.md"
BATCH34A_PUBLIC_DOCS_BOUNDARY = (
    DOCS / "sources" / "product-agent-os-batch34a-public-docs-boundary.md"
)
BATCH34B_PUBLIC_COPY_REWRITE = (
    DOCS / "sources" / "product-agent-os-batch34b-public-copy-rewrite.md"
)
BATCH34C_I18N_LOCALIZATION = (
    DOCS / "sources" / "product-agent-os-batch34c-i18n-localization.md"
)
BATCH34D_QA_CLOSURE = (
    DOCS / "sources" / "product-agent-os-batch34d-product-docs-qa-closure.md"
)
BATCH34E_FULL_SITE_INVENTORY = (
    DOCS / "sources" / "product-agent-os-batch34e-full-site-i18n-inventory.md"
)
BATCH35_APPROVAL_DRAFT = DOCS / "sources" / "product-agent-os-batch35-approval-packet-draft.md"
BATCH35_APPROVAL_DRAFT_EN = DOCS / "sources" / "product-agent-os-batch35-approval-packet-draft.en.md"
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
ENGLISH_ORIGINAL_SUPERPOWERS_PLAN_PAGES = {
    DOCS / "superpowers" / "plans" / "2026-05-14-product-agent-os-generated-infrastructure.md",
    DOCS / "superpowers" / "plans" / "2026-05-14-product-agent-os-lifecycle-skills.md",
    DOCS / "superpowers" / "plans" / "2026-05-14-product-agent-os-plugin-core.md",
    DOCS / "superpowers" / "plans" / "2026-05-14-product-agent-os-production-hardening.md",
    DOCS / "superpowers" / "plans" / "2026-05-15-product-agent-os-codex-runtime-runner.md",
    DOCS / "superpowers" / "plans" / "2026-05-25-track-9-methodology-intelligence.md",
    DOCS / "superpowers" / "plans" / "2026-05-27-track-10-guided-questions-status-dashboard.md",
}
BUILDABLE_MARKDOWN_PAGE_COUNT = 128
LOCALIZED_MARKDOWN_PAGE_COUNT = 121
ENGLISH_ORIGINAL_MARKDOWN_PAGE_COUNT = 7


class ProductAgentOsDocsTest(unittest.TestCase):
    def _internal_history_documents(self, documents):
        internal = {
            name: text
            for name, text in documents.items()
            if name in {"plugin_readme"}
        }
        return internal or documents

    def _localized_contract_text(self, path):
        text = path.read_text(encoding="utf-8-sig")
        en_path = path.with_name(path.stem + ".en" + path.suffix)
        if en_path.exists():
            text += "\n" + en_path.read_text(encoding="utf-8-sig")
        return text

    def _batch34_public_ready_pages(self):
        return [
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

    def _base_markdown_pages(self):
        return sorted(
            path
            for path in DOCS.rglob("*.md")
            if not path.name.endswith(".en.md")
        )

    def _localized_markdown_pages(self):
        english_original = set(ENGLISH_ORIGINAL_SUPERPOWERS_PLAN_PAGES)
        return [
            path
            for path in self._base_markdown_pages()
            if path not in english_original
        ]

    def _english_original_markdown_pages(self):
        return sorted(ENGLISH_ORIGINAL_SUPERPOWERS_PLAN_PAGES)

    def _en_sibling_for(self, path):
        return path.with_name(path.stem + ".en" + path.suffix)

    def _missing_localized_en_siblings(self):
        return [
            path
            for path in self._localized_markdown_pages()
            if not self._en_sibling_for(path).exists()
        ]

    def _rendered_site_path_for_source(self, source_path, locale=None):
        rendered = source_path.relative_to(DOCS).with_suffix(".html")
        if locale == "en":
            return SITE / "en" / rendered
        return SITE / rendered

    def _language_switcher_hrefs(self, html):
        links = {}
        for match in re.finditer(r"<a\b[^>]*>", html):
            tag = match.group(0)
            if "md-select__link" not in tag:
                continue
            hreflang = re.search(r'\bhreflang="([^"]+)"', tag)
            href = re.search(r'\bhref="([^"]+)"', tag)
            if hreflang and href:
                links.setdefault(hreflang.group(1), []).append(href.group(1))
        return links

    def _resolve_site_href(self, html_path, href):
        target = href.split("#", 1)[0].split("?", 1)[0]
        if not target:
            return html_path.resolve()
        if target.startswith("/") or target.startswith("//"):
            return None
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            return None
        return (html_path.parent / unquote(target)).resolve()

    def test_root_runlog_is_compact_current_handoff_and_distribution_map(self):
        runlog = RUNLOG.read_text(encoding="utf-8")

        self.assertLess(len(runlog), 50000)
        self.assertIn("track10_task26_batch35_closed_through_m41_owner_closed_no_op_git_release_pr_b38_s2_m05_blocked_stale_cache", runlog)
        self.assertIn("Task 26 Batch 35 `T10-LIVE-M41`", runlog)
        self.assertIn("owner_closed_no_op_git_release_pr", runlog)
        self.assertIn("blocked_pending_explicit_cache_mutation_approval", runlog)
        self.assertIn("done_through_m40", runlog)
        self.assertIn("RUNLOG.md` is now the compact handoff layer", runlog)

        for expected in [
            "REQUIREMENTS.md",
            "PLAN.md",
            "TEST.md",
            "EVALS.md",
            "AGENTS.md",
            "docs/sources/registry.md",
            "docs/sources/product-agent-os-track-8-detailed-backlog.md",
            "docs/sources/product-agent-os-track-9-backlog.md",
            "docs/sources/product-agent-os-track-10-backlog.md",
            "docs/sources/product-agent-os-batch35-approval-packet-draft.md",
            "Control-Plane Marker Bank",
        ]:
            with self.subTest(runlog_distribution=expected):
                self.assertIn(expected, runlog)

        self.assertIn("Product-Agent OS Track 10 Task 26 Batch 35 approval-bound real testing execution matrix", runlog)
        self.assertIn("no git stage/commit/push/PR", runlog)

    def test_root_plan_is_compact_current_sequencing_contract(self):
        plan = PLAN.read_text(encoding="utf-8")

        self.assertLess(len(plan), 50000)
        self.assertIn("PLAN.md` is the compact sequencing and rollback layer", plan)
        self.assertIn("Current Planning Contract", plan)
        self.assertIn("Next Implementation Queue", plan)
        self.assertIn("Source Planning Artifacts", plan)
        self.assertIn("Evidence ownership", plan)
        self.assertIn("T10-LIVE-M41", plan)
        self.assertIn("owner_closed_no_op_git_release_pr", plan)
        self.assertIn("blocked_pending_explicit_cache_mutation_approval", plan)
        self.assertIn("B38-S2", plan)

        for expected in [
            "REQUIREMENTS.md",
            "TEST.md",
            "EVALS.md",
            "RUNLOG.md",
            "AGENTS.md",
            "docs/sources/product-agent-os-track-8-detailed-backlog.md",
            "docs/sources/product-agent-os-track-9-backlog.md",
            "docs/sources/product-agent-os-track-10-backlog.md",
            "docs/sources/registry.md",
            "docs/sources/product-agent-os-batch35-approval-packet-draft.md",
            "git diff --check",
        ]:
            with self.subTest(plan_distribution=expected):
                self.assertIn(expected, plan)

        self.assertNotIn("## T9-D12 Delivery, Release & Operations Completed Slice", plan)

    def test_root_test_is_compact_current_verification_contract(self):
        test_plan = TEST.read_text(encoding="utf-8")

        self.assertLess(len(test_plan), 50000)
        self.assertIn("TEST.md` is the compact verification routing layer", test_plan)
        self.assertIn("Current Verification State", test_plan)
        self.assertIn("Required Checks After Docs Or Control-Plane Changes", test_plan)
        self.assertIn("Required Checks After Plugin Or Runtime Changes", test_plan)
        self.assertIn("Runtime And External-Action Verification Boundaries", test_plan)
        self.assertIn("Historical Evidence Owners", test_plan)
        self.assertIn("T10-LIVE-M41", test_plan)
        self.assertIn("owner_closed_no_op_git_release_pr", test_plan)
        self.assertIn("blocked_pending_explicit_cache_mutation_approval", test_plan)
        self.assertIn("B38-S2", test_plan)

        for expected in [
            "python -m unittest tests.product_agent_os.test_product_agent_os_docs -v",
            "python tools\\check_docs.py",
            "git diff --check",
            "python -m unittest discover -s tests -p \"test_*.py\" -v",
            "python plugins\\product-agent-os\\scripts\\run_fixture_eval.py",
            "python plugins\\product-agent-os\\scripts\\run_transcript_eval.py",
            "python plugins\\product-agent-os\\scripts\\validate_codex_compatibility.py",
            "timeout_ms: 1200000",
            "docs/sources/product-agent-os-track-8-detailed-backlog.md",
            "docs/sources/product-agent-os-track-9-backlog.md",
            "docs/sources/product-agent-os-track-10-backlog.md",
            "docs/sources/registry.md",
            "docs/sources/product-agent-os-batch35-approval-packet-draft.md",
        ]:
            with self.subTest(test_distribution=expected):
                self.assertIn(expected, test_plan)

        self.assertNotIn("## Completed Focused Checks For T9-D12", test_plan)

    def test_track10_batch37_s1_task_matrix_contract_is_recorded(self):
        track10_plan = TRACK10_PLAN.read_text(encoding="utf-8")
        plan = PLAN.read_text(encoding="utf-8")
        test_plan = TEST.read_text(encoding="utf-8")
        runlog = RUNLOG.read_text(encoding="utf-8")

        track10_terms = [
            "Batch 37 S1 implementation contract",
            "B37-S1 implemented scope: `T10-PLAN-M01..M03`, `T10-PLAN-M18`",
            "Allowed task statuses: `planned`, `in_progress`, `implemented`, `blocked`, `accepted_gap`",
            "Plan-file placement policy:",
            "docs/superpowers/plans/YYYY-MM-DD-<scope>-task-matrix.md",
            "Lightweight exception fields: `reason`, `reduced_evidence_path`, `residual_risk`",
            "Validator target: detailed task blocks with one explicit field per line",
            "Summary tables are planning indexes only",
            "| `T10-PLAN-M01` | 37 |",
            "| `T10-PLAN-M02` | 37 |",
            "| `T10-PLAN-M03` | 37 |",
            "| `T10-PLAN-M18` | 37 |",
            "what was done:",
            "actual implementation date and time:",
            "B37-S1 completion evidence",
        ]
        for expected in track10_terms:
            with self.subTest(track10_plan=expected):
                self.assertIn(expected, track10_plan)

        for expected in [
            "B37-S1",
            "T10-PLAN-M01..M03",
            "T10-PLAN-M18",
            "task-matrix contract",
            "task-matrix-plan.md",
        ]:
            with self.subTest(control_plane=expected):
                self.assertIn(expected, plan)
                self.assertIn(expected, test_plan)
                self.assertIn(expected, runlog)

    def test_track10_batch37_s2_task_matrix_template_and_renderer_are_recorded(self):
        track10_plan = TRACK10_PLAN.read_text(encoding="utf-8")
        plan = PLAN.read_text(encoding="utf-8")
        test_plan = TEST.read_text(encoding="utf-8")
        runlog = RUNLOG.read_text(encoding="utf-8")
        readme = (ROOT / "plugins" / "product-agent-os" / "README.md").read_text(encoding="utf-8")
        backlog = (ROOT / "docs" / "sources" / "product-agent-os-track-10-backlog.md").read_text(
            encoding="utf-8"
        )
        registry = (ROOT / "docs" / "sources" / "registry.md").read_text(encoding="utf-8")

        track10_terms = [
            "B37-S2 implementation evidence",
            "B37-S2 implemented scope: `T10-PLAN-M04..M05`, `T10-PLAN-M17`",
            "plugins/product-agent-os/assets/templates/artifact-templates/task-matrix-plan.md",
            ".codex/artifact-templates/task-matrix-plan.md",
            "artifact-task-matrix-plan",
            "renderer_file_count: 195",
            "Template source is packaged in the checked-in plugin source tree",
            "does not publish the plugin cache",
            "does not mutate `.codex-plugin/plugin.json`",
            "does not perform live automation",
            "does not call providers/live external model/API endpoints",
            "does not perform git stage/commit/push/PR",
            "| `T10-PLAN-M04` | 37 |",
            "| `T10-PLAN-M05` | 37 |",
            "| `T10-PLAN-M17` | 37 |",
        ]
        for expected in track10_terms:
            with self.subTest(track10_plan=expected):
                self.assertIn(expected, track10_plan)

        for expected in [
            "B37-S2",
            "T10-PLAN-M04..M05",
            "T10-PLAN-M17",
            "task-matrix-plan.md",
            "renderer_file_count: 195",
            "plugin cache remains stale until an explicit publication/cache refresh action is approved",
        ]:
            with self.subTest(control_plane=expected):
                self.assertIn(expected, plan)
                self.assertIn(expected, test_plan)
                self.assertIn(expected, runlog)

        for expected in [
            "Task Matrix Plan template",
            "artifact-task-matrix-plan",
            ".codex/artifact-templates/task-matrix-plan.md",
            "current session skills are loaded separately from the packaged plugin source",
        ]:
            with self.subTest(readme=expected):
                self.assertIn(expected, readme)

        self.assertIn("done_through_s2", backlog)
        self.assertIn("Product-Agent OS Batch 37 S2 task-matrix template and renderer registration", registry)

    def test_track10_batch37_s3_task_matrix_validator_eval_and_completion_report_are_recorded(self):
        track10_plan = TRACK10_PLAN.read_text(encoding="utf-8")
        plan = PLAN.read_text(encoding="utf-8")
        test_plan = TEST.read_text(encoding="utf-8")
        runlog = RUNLOG.read_text(encoding="utf-8")
        backlog = (ROOT / "docs" / "sources" / "product-agent-os-track-10-backlog.md").read_text(
            encoding="utf-8"
        )
        registry = (ROOT / "docs" / "sources" / "registry.md").read_text(encoding="utf-8")

        track10_terms = [
            "B37-S3 implementation evidence",
            "B37-S3 implemented scope: `T10-PLAN-M06`, `T10-PLAN-M10`, `T10-PLAN-M13`",
            "validate_task_matrix.py",
            "validate_task_matrix_text",
            "task-matrix-validator-and-completion-report",
            "task_matrix_validator_contract_present",
            "task_matrix_completion_report_guard_present",
            "implemented with `pending_execution_timestamp` is invalid",
            "planned rows are not implementation evidence",
            "summary tables are planning indexes only",
            "| `T10-PLAN-M06` | 37 |",
            "| `T10-PLAN-M10` | 37 |",
            "| `T10-PLAN-M13` | 37 |",
        ]
        for expected in track10_terms:
            with self.subTest(track10_plan=expected):
                self.assertIn(expected, track10_plan)

        for expected in [
            "B37-S3",
            "T10-PLAN-M06",
            "T10-PLAN-M10",
            "T10-PLAN-M13",
            "validate_task_matrix.py",
            "task_matrix_validator_contract_present",
        ]:
            with self.subTest(control_plane=expected):
                self.assertIn(expected, plan)
                self.assertIn(expected, test_plan)
                self.assertIn(expected, runlog)

        self.assertIn("done_through_s3", backlog)
        self.assertIn("Product-Agent OS Batch 37 S3 task-matrix validator, eval and completion-report guard", registry)

    def test_track10_batch37_s4_skill_routing_discovery_and_control_are_recorded(self):
        track10_plan = TRACK10_PLAN.read_text(encoding="utf-8")
        plan = PLAN.read_text(encoding="utf-8")
        test_plan = TEST.read_text(encoding="utf-8")
        runlog = RUNLOG.read_text(encoding="utf-8")
        backlog = (ROOT / "docs" / "sources" / "product-agent-os-track-10-backlog.md").read_text(
            encoding="utf-8"
        )
        registry = (ROOT / "docs" / "sources" / "registry.md").read_text(encoding="utf-8")

        track10_terms = [
            "B37-S4 implementation evidence",
            "B37-S4 implemented scope: `T10-PLAN-M07..M09`, `T10-PLAN-M20`",
            "task_matrix_planner_routing_contract_present",
            "task_matrix_agent_handoff_contract_present",
            "task_matrix_discovery_signal_contract_present",
            "task_matrix_planning_control_governance_present",
            "task-matrix-plan.md",
            "present_unverified",
            "reminder-only hooks",
            "hard gates live in validator/tests/skills",
            "| `T10-PLAN-M07` | 37 |",
            "| `T10-PLAN-M08` | 37 |",
            "| `T10-PLAN-M09` | 37 |",
            "| `T10-PLAN-M20` | 37 |",
        ]
        for expected in track10_terms:
            with self.subTest(track10_plan=expected):
                self.assertIn(expected, track10_plan)

        for expected in [
            "B37-S4",
            "T10-PLAN-M07..M09",
            "T10-PLAN-M20",
            "task_matrix_planner_routing_contract_present",
            "task_matrix_agent_handoff_contract_present",
            "task_matrix_discovery_signal_contract_present",
            "task_matrix_planning_control_governance_present",
        ]:
            with self.subTest(control_plane=expected):
                self.assertIn(expected, plan)
                self.assertIn(expected, test_plan)
                self.assertIn(expected, runlog)

        self.assertIn("done_through_s4", backlog)
        self.assertIn("Product-Agent OS Batch 37 S4 skill routing, discovery and planning control", registry)

    def test_track10_batch37_s5_docs_projection_lifecycle_and_closure_are_recorded(self):
        track10_plan = TRACK10_PLAN.read_text(encoding="utf-8")
        plan = PLAN.read_text(encoding="utf-8")
        test_plan = TEST.read_text(encoding="utf-8")
        runlog = RUNLOG.read_text(encoding="utf-8")
        backlog = (ROOT / "docs" / "sources" / "product-agent-os-track-10-backlog.md").read_text(
            encoding="utf-8"
        )
        registry = (ROOT / "docs" / "sources" / "registry.md").read_text(encoding="utf-8")

        track10_terms = [
            "B37-S5 implementation evidence",
            "B37-S5 implemented scope: `T10-PLAN-M11..M12`, `T10-PLAN-M14..M16`, `T10-PLAN-M19`",
            "task_matrix_docs_source_sync_present",
            "task_matrix_backward_compatibility_policy_present",
            "task_matrix_status_projection_deferred_present",
            "task_matrix_system_file_hygiene_owner_present",
            "task_matrix_lifecycle_archive_policy_present",
            "Batch 37 closure evidence",
            "staged artifact, not source truth or execution evidence",
            "existing matrices stay valid as historical plans",
            "dashboard projection is deferred",
            "artifact_templates ownership",
            "docs/source ownership",
            "RUNLOG.md",
            "docs/sources/*backlog*.md",
            "docs/sources/registry*.md",
            "| `T10-PLAN-M11` | 37 |",
            "| `T10-PLAN-M12` | 37 |",
            "| `T10-PLAN-M14` | 37 |",
            "| `T10-PLAN-M15` | 37 |",
            "| `T10-PLAN-M16` | 37 |",
            "| `T10-PLAN-M19` | 37 |",
        ]
        for expected in track10_terms:
            with self.subTest(track10_plan=expected):
                self.assertIn(expected, track10_plan)

        for expected in [
            "B37-S5",
            "T10-PLAN-M11..M12",
            "T10-PLAN-M14..M16",
            "T10-PLAN-M19",
            "task_matrix_docs_source_sync_present",
            "task_matrix_backward_compatibility_policy_present",
            "task_matrix_status_projection_deferred_present",
            "task_matrix_system_file_hygiene_owner_present",
            "task_matrix_lifecycle_archive_policy_present",
        ]:
            with self.subTest(control_plane=expected):
                self.assertIn(expected, plan)
                self.assertIn(expected, test_plan)
                self.assertIn(expected, runlog)

        self.assertIn("done_through_s5", backlog)
        self.assertIn("Product-Agent OS Batch 37 S5 docs, projection, hygiene, lifecycle and closure", registry)

    def test_root_agents_is_compact_durable_rule_contract(self):
        agents = AGENTS.read_text(encoding="utf-8")

        self.assertLess(len(agents), 50000)
        self.assertIn("AGENTS.md` is the durable project instruction layer", agents)
        self.assertIn("Control-Plane Role", agents)
        self.assertIn("Documentation Rules", agents)
        self.assertIn("Diagram Atlas Rules", agents)
        self.assertIn("Product-Agent Operating Model", agents)
        self.assertIn("Windows Codex Shell Guard", agents)
        self.assertIn("Product-Agent OS Plugin Rules", agents)
        self.assertIn("Source And Insight Policy", agents)
        self.assertIn("Verification", agents)
        self.assertIn("T10-LIVE-M41", agents)
        self.assertIn("owner_closed_no_op_git_release_pr", agents)
        self.assertIn("blocked_pending_explicit_cache_mutation_approval", agents)
        self.assertIn("B38-S2", agents)

        for expected in [
            "REQUIREMENTS.md",
            "PLAN.md",
            "TEST.md",
            "EVALS.md",
            "RUNLOG.md",
            "docs/sources/registry.md",
            "docs/sources/product-agent-os-track-8-detailed-backlog.md",
            "docs/sources/product-agent-os-track-9-backlog.md",
            "docs/sources/product-agent-os-track-10-backlog.md",
            "docs/sources/product-agent-os-batch35-approval-packet-draft.md",
            "python -m unittest tests.product_agent_os.test_product_agent_os_docs -v",
            "python tools\\check_docs.py",
            "git diff --check",
        ]:
            with self.subTest(agents_distribution=expected):
                self.assertIn(expected, agents)

        self.assertNotIn("Product-Agent OS implementation status", agents)
        self.assertNotIn("Track 8 T8-A16 baseline was refreshed", agents)
        self.assertNotIn("Task 26 Batch 34E corrective control-plane sync terms", agents)

    def test_root_evals_is_compact_current_eval_contract(self):
        evals = EVALS.read_text(encoding="utf-8")

        self.assertLess(len(evals), 50000)
        self.assertIn("EVALS.md` is the compact evaluation routing layer", evals)
        self.assertIn("Rubrics", evals)
        self.assertIn("Thresholds", evals)
        self.assertIn("Current Evaluation State", evals)
        self.assertIn("Active Eval Routes", evals)
        self.assertIn("Methodology Eval Map", evals)
        self.assertIn("Unsupported Claims", evals)
        self.assertIn("Historical Eval Evidence Owners", evals)
        self.assertIn("T10-LIVE-M41", evals)
        self.assertIn("owner_closed_no_op_git_release_pr", evals)
        self.assertIn("blocked_pending_explicit_cache_mutation_approval", evals)
        self.assertIn("B38-S2", evals)

        for expected in [
            "evidence_before_completion",
            "quality_testing_evals_contract_present",
            "llm_ai_rag_contract_present",
            "security_privacy_compliance_contract_present",
            "delivery_release_operations_contract_present",
            "cross_domain_synthesis_contract_present",
            "T10-Q-M15..M25",
            "T10-SV-M58..M62",
            "T10-CG-V2-M01..M62",
            "T10-LIVE-M01..M41",
            "B34E-I18N-M34..M49",
            "docs/sources/product-agent-os-track-8-detailed-backlog.md",
            "docs/sources/product-agent-os-track-9-backlog.md",
            "docs/sources/product-agent-os-track-10-backlog.md",
            "docs/sources/registry.md",
            "docs/sources/product-agent-os-batch35-approval-packet-draft.md",
            "python -m unittest tests.product_agent_os.test_product_agent_os_docs -v",
            "python tools\\check_docs.py",
            "git diff --check",
        ]:
            with self.subTest(evals_distribution=expected):
                self.assertIn(expected, evals)

        self.assertNotIn("Current Task 22 eval evidence", evals)
        self.assertNotIn("Batch 21 focused and broad evidence", evals)
        self.assertNotIn("Batch 34E M44 sync", evals)

    def test_root_readme_is_compact_product_entrypoint_without_history_ledger(self):
        readme = ROOT_README.read_text(encoding="utf-8")

        self.assertLess(len(readme), 50000)
        for expected in [
            "Product-Agent OS - local Codex plugin",
            "Product-Agent OS full stack",
            "Why Product-Agent OS",
            "What You Get After The First Run",
            "Output Preview",
            "Codex Vs Product-Agent OS",
            "Implementation Depth",
            "Before And After",
            "Current Implementation Status",
            "Operating Loop",
            "Capability Map",
            "Core Capabilities",
            "Implemented Technical Surface",
            "Packaged Skills",
            "Use-Case Routing",
            "Methodology Intelligence And Auto-Selection",
            "Project Scanning Principle",
            "Methodology Map",
            "Methodology And Readiness Gates",
            "No Forced Ceremony",
            "Who It Fits Best",
            "Documentation And Evidence",
            "Guided Questions And Status",
            "Project Code Graph",
            "Live Runtime And Retrieval Boundaries",
            "Self-Verification And Modernization Loop",
            "System File Hygiene",
            "Repository Layout",
            "Quick Commands",
            "Where History Lives",
            "docs/product-agent-os/index.md",
            "artifact-gallery.md",
            "methodology-intelligence.md",
            "approval-bound-real-testing.md",
            "docs/sources/registry.md",
            "plugins/product-agent-os/README.md",
            "TDD / Red-Green-Refactor",
            "DDD",
            "ADD / architecture-driven design",
            "FSD and frontend boundary discipline",
            "Eval-driven AI / RAG development",
        ]:
            with self.subTest(readme_product_contract=expected):
                self.assertIn(expected, readme)

        forbidden_history = re.compile(
            r"\b(Task|Track|Batch)\b|T[0-9]+-|B[0-9]+-|done_through|Implementation Evidence Archive"
        )
        self.assertIsNone(forbidden_history.search(readme))

    def test_batch38_p0_product_docs_are_current(self):
        approval_page = self._localized_contract_text(
            PRODUCT_AGENT_OS / "approval-bound-real-testing.md"
        )
        methodology_page = self._localized_contract_text(
            PRODUCT_AGENT_OS / "methodology-intelligence.md"
        )
        source_draft = "\n".join(
            [
                (DOCS / "sources" / "add-ddd-tdd-fsd-llm-development.md").read_text(
                    encoding="utf-8"
                ),
                (DOCS / "sources" / "add-ddd-tdd-fsd-llm-development.en.md").read_text(
                    encoding="utf-8"
                ),
            ]
        )

        for expected in [
            "M37-M41",
            "M37",
            "M38",
            "M39",
            "M40",
            "M41",
            "owner_closed_no_op_git_release_pr",
            "server_shutdown_complete: true",
            "Playwright Chromium",
            "codex_user_session",
            "canonical_graph_source_mutated: false",
            "no git stage/commit/push/PR",
        ]:
            with self.subTest(approval_page=expected):
                self.assertIn(expected, approval_page)

        for expected in [
            "Project Scanning Principle",
            "Business & Product",
            "Requirements & Domain",
            "Solution architecture",
            "Quality, Testing & Evals",
            "Codex / Agentic Workflow",
            "Frontend",
            "Backend",
            "API & Integrations",
            "Database & Data",
            "LLM / AI / RAG",
            "Security, Privacy & Compliance",
            "Delivery, Release & Operations",
            "These 12 methodology domains",
            "Readiness statuses",
            "not_applicable",
            "applicable_missing",
            "present_unverified",
            "present_verified",
            "proposal_staged",
            "explicit_gap_accepted",
            "approval_required",
            "Methodology Examples",
            "Product discovery and metric design",
            "ATDD / BDD acceptance scenarios",
            "DDD",
            "Architecture-driven design and ADRs",
            "C4 / arc42-style architecture views",
            "TDD / Red-Green-Refactor",
            "FSD and frontend boundary discipline",
            "API contract-first delivery",
            "Eval-driven AI / RAG development",
        ]:
            with self.subTest(methodology_page=expected):
                self.assertIn(expected, methodology_page)

        for expected in [
            "Terminology boundary",
            "Product-Agent OS core methodology reserves `DDD` for Domain-Driven Design",
            "Product-Agent OS core `DDD` means Domain-Driven Design",
            "Data-Driven Development as product/metric discipline",
            "DDD (draft term here)",
        ]:
            with self.subTest(source_draft=expected):
                self.assertIn(expected, source_draft)

    def test_batch38_p1_product_docs_route_outputs_and_boundary_are_current(self):
        first_run = self._localized_contract_text(PRODUCT_AGENT_OS / "index.md")
        gallery = self._localized_contract_text(PRODUCT_AGENT_OS / "artifact-gallery.md")
        root_index = "\n".join(
            [
                (DOCS / "index.md").read_text(encoding="utf-8"),
                (DOCS / "index.en.md").read_text(encoding="utf-8"),
            ]
        )
        nav = MKDOCS.read_text(encoding="utf-8")
        check_docs = CHECK_DOCS.read_text(encoding="utf-8")
        plan = PLAN.read_text(encoding="utf-8")

        for expected in [
            "Первый запуск: маршрут пользователя",
            "First-Run Walkthrough",
            "read-only workspace audit",
            "lifecycle state",
            "usage_mode",
            "methodology gaps",
            "Methodology selection",
            "staged artifacts",
            "verification route",
            "approval boundary",
            "evidence gaps",
            "safe_next_action",
            "Generated views are not source of truth",
            "no live server launch",
            "no browser automation",
            "no provider/API calls",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]:
            with self.subTest(first_run=expected):
                self.assertIn(expected, first_run)

        for expected in [
            "Витрина результатов Product-Agent OS",
            "Product-Agent OS Artifact Gallery",
            "Control plane",
            "First-run route",
            "Methodology packet",
            "Status dashboard",
            "Graph and cockpit",
            "Real-testing evidence",
            "Scorecards",
            "Release and closure",
            "Source of truth remains in project source files",
            "Generated views help navigation, but canonical files remain authoritative",
            "One approval never authorizes another action",
            "Historical evidence and public product copy must stay separate",
        ]:
            with self.subTest(gallery=expected):
                self.assertIn(expected, gallery)

        for expected in [
            "Граница public/internal документации",
            "Public/Internal Documentation Boundary",
            "Public product pages explain capabilities, user route, outputs, boundaries and next action",
            "Internal evidence pages under `docs/sources/` store source/history material",
            "Generated `site/` output is a rendered copy of source docs and review output, not source of truth",
            "source registry, packets, backlogs and verification records",
            "Source of truth remains in Markdown source files",
        ]:
            with self.subTest(boundary=expected):
                self.assertTrue(expected in first_run or expected in root_index)

        for expected in [
            "product-agent-os/artifact-gallery.md",
            'DOCS / "product-agent-os" / "artifact-gallery.md"',
        ]:
            with self.subTest(nav_or_check_docs=expected):
                self.assertTrue(expected in nav or expected in check_docs)

        public_forbidden_pattern = re.compile(
            r"\b(Task|Track|Batch)\b|T[0-9]+-[A-Z0-9-]+|B[0-9]+-[A-Z]+-M[0-9]+"
        )
        for path in [
            PRODUCT_AGENT_OS / "artifact-gallery.md",
            PRODUCT_AGENT_OS / "artifact-gallery.en.md",
        ]:
            text = path.read_text(encoding="utf-8")
            with self.subTest(public_forbidden_terms=path.name):
                self.assertIsNone(public_forbidden_pattern.search(text), path)

        for expected in [
            "`B38-DOC-M04` | P1 | Add end-user first-run walkthrough.",
            "`B38-DOC-M05` | P1 | Add artifact/output gallery for user-facing value.",
            "`B38-DOC-M06` | P1 | Define public vs internal documentation IA boundary for `site/`.",
            "| `B38-DOC-M04` | P1 |",
            "| `B38-DOC-M05` | P1 |",
            "| `B38-DOC-M06` | P1 |",
        ]:
            with self.subTest(plan=expected):
                self.assertIn(expected, plan)

    def test_batch38_p2_readme_registry_and_control_plane_sync_are_current(self):
        readme = ROOT_README.read_text(encoding="utf-8")
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        registry_en = SOURCE_REGISTRY_EN.read_text(encoding="utf-8")
        plan = PLAN.read_text(encoding="utf-8")

        for expected in [
            "docs/product-agent-os/index.md",
            "artifact-gallery.md",
            "methodology-intelligence.md",
            "approval-bound-real-testing.md",
            "not a ledger",
            "route first run, outputs, methods, approvals",
        ]:
            with self.subTest(readme_route=expected):
                self.assertIn(expected, readme)

        self.assertLess(len(readme), 50000)
        public_forbidden_pattern = re.compile(
            r"\b(Task|Track|Batch)\b|T[0-9]+-|B[0-9]+-|done_through|Implementation Evidence Archive"
        )
        self.assertIsNone(public_forbidden_pattern.search(readme))

        for expected in [
            "Product-Agent OS Batch 38 public docs, README and registry sync",
            "B38-DOC-M04..M10",
            "artifact/output gallery",
            "public/internal documentation boundary",
            "compact README routing",
            "RU/EN parity confirmation",
            "final docs verification",
            "generated `site/` refresh decision",
            "read-only agent audits for README/i18n/registry/site scope",
            "site/` was refreshed intentionally",
            "root RUNLOG/TEST/EVALS remain compact",
            'trust_level: "high"',
            'verification_status: "Backed by the Batch 38 docs contract',
        ]:
            with self.subTest(registry=expected):
                self.assertIn(expected, registry)
                self.assertIn(expected, registry_en)

        for expected in [
            "`B38-DOC-M07` | P1 | Compact README sync after source docs are corrected.",
            "`B38-DOC-M08` | P2 | Keep RU/EN parity for every changed user-facing page.",
            "`B38-DOC-M09` | P2 | Update source registry and control-plane pointers only where source-backed claims change.",
            "`B38-DOC-M10` | P2 | Final docs verification and generated `site/` refresh decision.",
            "| `B38-DOC-M07` | P1 |",
            "| `B38-DOC-M08` | P2 |",
            "| `B38-DOC-M09` | P2 |",
            "| `B38-DOC-M10` | P2 |",
            "`B38-DOC-M01..M10` implemented",
        ]:
            with self.subTest(plan=expected):
                self.assertIn(expected, plan)

        m10_rows = [
            line for line in plan.splitlines() if line.startswith("| `B38-DOC-M10` |")
        ]
        self.assertEqual(1, len(m10_rows))
        self.assertIn("`implemented`", m10_rows[0])
        self.assertNotIn("`planned`; `pending_execution_timestamp`", m10_rows[0])
        self.assertNotIn("`B38-DOC-M10` remains planned", plan)

        rendered_registry = "\n".join(
            [
                (SITE / "sources" / "registry.html").read_text(encoding="utf-8"),
                (SITE / "en" / "sources" / "registry.html").read_text(encoding="utf-8"),
                (SITE / "search" / "search_index.json").read_text(encoding="utf-8"),
            ]
        )
        for expected in [
            "B38-DOC-M04..M10",
            "final docs verification",
            "generated",
            "refresh decision",
        ]:
            with self.subTest(rendered_site=expected):
                self.assertIn(expected, rendered_registry)

    def test_batch38_s1_release_gate_package_metadata_packet_is_source_owned(self):
        packet = TRACK10_BACKLOG.read_text(encoding="utf-8")
        plan = PLAN.read_text(encoding="utf-8")
        track10 = TRACK10_BACKLOG.read_text(encoding="utf-8")
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        registry_en = SOURCE_REGISTRY_EN.read_text(encoding="utf-8")
        test_plan = TEST.read_text(encoding="utf-8")
        runlog = RUNLOG.read_text(encoding="utf-8")

        for expected in [
            "B38-S1 Release gate and package metadata",
            "B38-PROD-M01..M03",
            "T10-LIVE-M41 status: `blocked_pending_explicit_git_release_fields`",
            "release_fields_deferral_status: `not_deferred_without_owner_fields`",
            "git_stage_commit_push_pr_performed: false",
            "tracked_plugin_file_count: 586",
            "skill_count: 11",
            "template_file_count: 202",
            "script_file_count: 84",
            "fixture_file_count: 266",
            "package_source_digest_sha256: `7d5a7634d1223f72ccdd1edcd24fddeb8bbdcc38d36d73ab1d002f352b06dcbb`",
            "ignored_cache_exclusions: `__pycache__ only`",
            "metadata_release_candidate_status: `local_only_exception_recorded`",
            "example.invalid trust fields remain blocked for public or team release",
            "Codex compatibility status: `compatible`",
            "No plugin install, plugin-cache mutation, live runtime, browser automation, provider call, canonical graph mutation or git write was performed.",
        ]:
            with self.subTest(packet=expected):
                self.assertIn(expected, packet)

        for expected in [
            "`B38-PROD-M01` | P0 | Resolve or explicitly defer `T10-LIVE-M41` git release/PR gate.",
            "`B38-PROD-M02` | P0 | Freeze install source and package surface.",
            "`B38-PROD-M03` | P0 | Finalize public and organization-facing plugin metadata.",
            "| `B38-PROD-M01` | P0 |",
            "| `B38-PROD-M02` | P0 |",
            "| `B38-PROD-M03` | P0 |",
            "B38-S1 `B38-PROD-M01..M03`",
            "M01 `owner_closed_no_op_git_release_pr`",
            "M02 `implemented`",
            "M03 `accepted_gap`",
        ]:
            with self.subTest(plan=expected):
                self.assertIn(expected, plan)

        m01_rows = [
            line for line in plan.splitlines() if line.startswith("| `B38-PROD-M01` |")
        ]
        m02_rows = [
            line for line in plan.splitlines() if line.startswith("| `B38-PROD-M02` |")
        ]
        m03_rows = [
            line for line in plan.splitlines() if line.startswith("| `B38-PROD-M03` |")
        ]
        self.assertEqual(1, len(m01_rows))
        self.assertEqual(1, len(m02_rows))
        self.assertEqual(1, len(m03_rows))
        self.assertIn("`owner_closed_no_op`", m01_rows[0])
        self.assertIn("`implemented`", m02_rows[0])
        self.assertIn("`accepted_gap`", m03_rows[0])
        self.assertNotIn("`planned`; `pending_execution_timestamp`", m01_rows[0])
        self.assertNotIn("`planned`; `pending_execution_timestamp`", m02_rows[0])
        self.assertNotIn("`planned`; `pending_execution_timestamp`", m03_rows[0])

        for expected in [
            "Product-Agent OS Batch 38 S1 release gate and package metadata",
            "B38-S1 `B38-PROD-M01..M03`",
            "package_source_digest_sha256",
            "local-only exception",
            'trust_level: "high"',
            'verification_status: "Backed by the B38-S1 source packet',
        ]:
            with self.subTest(registry=expected):
                self.assertIn(expected, registry)
                self.assertIn(expected, registry_en)

        for expected in [
            "`b38_s1_release_gate_package_metadata`",
            "M01 stays blocked without release fields",
            "M02 freezes the checked-in package source",
            "M03 records a local-only metadata exception",
        ]:
            with self.subTest(track10=expected):
                self.assertIn(expected, track10)

        for expected in [
            "B38-S1 release gate/package metadata run",
            "focused docs contract",
            "Codex compatibility returned `status: compatible`",
            "strict MkDocs was not run",
        ]:
            with self.subTest(test_plan=expected):
                self.assertIn(expected, test_plan)

        for expected in [
            "Batch 38 S1 release gate/package metadata",
            "M01 remains blocked pending explicit git release fields",
            "package source digest `7d5a7634d1223f72ccdd1edcd24fddeb8bbdcc38d36d73ab1d002f352b06dcbb`",
            "local-only metadata exception",
        ]:
            with self.subTest(runlog=expected):
                self.assertIn(expected, runlog)

    def test_t10_live_m41_post_b38_audit_boundary_is_source_owned(self):
        plan = PLAN.read_text(encoding="utf-8")
        runlog = RUNLOG.read_text(encoding="utf-8")
        test_plan = TEST.read_text(encoding="utf-8")
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        registry_en = SOURCE_REGISTRY_EN.read_text(encoding="utf-8")
        track10 = TRACK10_BACKLOG.read_text(encoding="utf-8")
        track10_en = TRACK10_BACKLOG_EN.read_text(encoding="utf-8")
        batch35 = BATCH35_APPROVAL_DRAFT.read_text(encoding="utf-8")
        batch35_en = BATCH35_APPROVAL_DRAFT_EN.read_text(encoding="utf-8")

        for expected in [
            "T10-LIVE-M41 post-B38 audit",
            "historical_preflight_snapshot",
            "dirty_file_count: 15 is historical Batch 35 evidence, not current release readiness",
            "B37/B38/B38-S1 do not close M41",
            "fresh preflight is required before any git write",
        ]:
            with self.subTest(source_packet=expected):
                self.assertIn(expected, batch35)
                self.assertIn(expected, batch35_en)
                self.assertIn(expected, track10)
                self.assertIn(expected, track10_en)

        for expected in [
            "Next release/install/cache action",
            "future git write",
            "owner_closed_no_op_git_release_pr",
        ]:
            with self.subTest(plan=expected):
                self.assertIn(expected, plan)
        self.assertNotIn("Next executable product action: none", plan)

        for expected in [
            "M41 post-B38 audit",
            "historical_preflight_snapshot",
            "fresh git status/unrelated-change preflight",
            "B37/B38/B38-S1 do not close M41",
        ]:
            with self.subTest(control_plane=expected):
                self.assertIn(expected, runlog)
                self.assertIn(expected, test_plan)

        for expected in [
            "Product-Agent OS T10-LIVE-M41 post-B38 audit",
            "historical_preflight_snapshot",
            "fresh preflight is required before any git write",
        ]:
            with self.subTest(registry=expected):
                self.assertIn(expected, registry)
                self.assertIn(expected, registry_en)

    def test_batch38_s2_verification_install_cache_smoke_is_source_owned(self):
        plan = PLAN.read_text(encoding="utf-8")
        runlog = RUNLOG.read_text(encoding="utf-8")
        test_plan = TEST.read_text(encoding="utf-8")
        evals = EVALS.read_text(encoding="utf-8")
        requirements = REQUIREMENTS.read_text(encoding="utf-8")
        agents = AGENTS.read_text(encoding="utf-8")
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        registry_en = SOURCE_REGISTRY_EN.read_text(encoding="utf-8")
        track10 = TRACK10_BACKLOG.read_text(encoding="utf-8")
        track10_en = TRACK10_BACKLOG_EN.read_text(encoding="utf-8")
        track10_plan = TRACK10_PLAN.read_text(encoding="utf-8")

        for expected in [
            "owner_closed_no_op_git_release_pr",
            "git_stage_commit_push_pr_performed: false",
            "future_git_write_requires_fresh_preflight: true",
            "B38-S2 Verification and install smoke",
            "B38-PROD-M04",
            "B38-PROD-M05",
            "b38_s2_verification_install_cache_smoke",
            "full_unittest_count: 846",
            "fixture_eval_exit_code: 0",
            "transcript_eval_session_count: 19",
            "transcript_eval_failure_count: 0",
            "codex_compatibility_status: compatible",
            "docs_check_status: ok",
            "diff_hygiene_exit_code: 0",
            "plugin_install_smoke_status: read_only_inspection_completed_stale_cache_detected",
            "plugin_cache_refresh_status: blocked_pending_explicit_cache_mutation_approval",
            "visible_cache_skill_count: 10",
            "checked_in_skill_count: 11",
            "missing_cache_skill: docs-maintainer",
            "visible_cache_script_file_count: 32",
            "checked_in_script_file_count: 84",
            "visible_cache_template_file_count: 34",
            "checked_in_template_file_count: 202",
            "no_plugin_cache_mutation_performed",
            "no_git_stage_commit_push_pr",
            "agent_team_design_packet_present",
            "roles_have_disjoint_ownership",
            "handoff_packet_fields_present",
            "agent_skill_stop_conditions_present",
        ]:
            with self.subTest(track10=expected):
                self.assertIn(expected, track10)
                self.assertIn(expected, track10_en)

        for expected in [
            "`B38-PROD-M04` | P0 | Run full pre-install verification.",
            "`B38-PROD-M05` | P0 | Refresh or install the new plugin version and prove no stale plugin cache is used.",
            "M04 `implemented`",
            "M05 `blocked_stale_plugin_cache_pending_refresh_approval`",
            "B38-S2 `B38-PROD-M04..M05`",
            "Next release/install/cache action: none until plugin-cache refresh target, rollback path and mutation approval are explicit.",
        ]:
            with self.subTest(plan=expected):
                self.assertIn(expected, plan)

        m04_rows = [
            line for line in plan.splitlines() if line.startswith("| `B38-PROD-M04` |")
        ]
        m05_rows = [
            line for line in plan.splitlines() if line.startswith("| `B38-PROD-M05` |")
        ]
        self.assertEqual(1, len(m04_rows))
        self.assertEqual(1, len(m05_rows))
        self.assertIn("`implemented`", m04_rows[0])
        self.assertIn("`blocked`", m05_rows[0])
        self.assertNotIn("`planned`; `pending_execution_timestamp`", m04_rows[0])
        self.assertNotIn("`planned`; `pending_execution_timestamp`", m05_rows[0])

        for expected in [
            "Product-Agent OS T10-LIVE-M41 owner no-op closure and B38-S2 verification/install smoke",
            "B38-S2 `B38-PROD-M04..M05`",
            "blocked_pending_explicit_cache_mutation_approval",
            "trust_level: \"high\"",
        ]:
            with self.subTest(registry=expected):
                self.assertIn(expected, registry)
                self.assertIn(expected, registry_en)

        for expected in [
            "B38-S2 verification/install smoke run",
            "full unittest ran 846 tests with `OK`",
            "fixture eval exited `0`",
            "transcript eval exited `0` with 19 sessions and 0 failures",
            "plugin cache inspection found stale installed cache",
        ]:
            with self.subTest(test_plan=expected):
                self.assertIn(expected, test_plan)

        for document_name, document in [
            ("runlog", runlog),
            ("evals", evals),
            ("requirements", requirements),
            ("agents", agents),
            ("track10_plan", track10_plan),
        ]:
            with self.subTest(document=document_name):
                self.assertIn("owner_closed_no_op_git_release_pr", document)
                self.assertIn("B38-S2", document)
                self.assertIn("blocked_pending_explicit_cache_mutation_approval", document)

    def test_system_file_hygiene_audit_contract_is_documented_and_source_owned(self):
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "technical": (PRODUCT_AGENT_OS / "technical.md").read_text(encoding="utf-8"),
            "technical_en": (PRODUCT_AGENT_OS / "technical.en.md").read_text(encoding="utf-8"),
            "artifact_contracts": (PRODUCT_AGENT_OS / "artifact-contracts.md").read_text(encoding="utf-8"),
            "artifact_contracts_en": (PRODUCT_AGENT_OS / "artifact-contracts.en.md").read_text(encoding="utf-8"),
            "runtime_automations": (DOCS / "runtime" / "automations-github.md").read_text(encoding="utf-8"),
            "runtime_automations_en": (DOCS / "runtime" / "automations-github.en.md").read_text(encoding="utf-8"),
            "track10_plan": TRACK10_PLAN.read_text(encoding="utf-8"),
            "track10_backlog": TRACK10_BACKLOG.read_text(encoding="utf-8"),
            "registry": SOURCE_REGISTRY.read_text(encoding="utf-8"),
        }
        combined = "\n".join(documents.values())

        for expected in [
            "system_file_hygiene_audit",
            "validate_system_file_hygiene.py",
            "system-file-hygiene-audit.md",
            "system-file-hygiene-report.md",
            ".codex/automation-candidates/system-file-hygiene-audit.md",
            "weekly full",
            "monthly deep ownership review",
            "on-change",
            "size",
            "release/automation",
            "schedule_status: not_created",
            "read_only",
            "active schedules remain out of scope",
            "root control-plane files",
            "nested `AGENTS.md`",
            ".codex/agents",
            ".codex/skills",
            ".codex/workflows",
            ".codex/hooks",
            ".codex/evals",
            "docs source-control files",
            ".github/workflows",
            "plugin package control files",
            "done_through_m06",
            "T10-HYG-M04..M06",
            "done_through_m07",
            "T10-HYG-M07",
            "workflow-system-file-hygiene-audit",
            "artifact-system-file-hygiene-report",
            "automation-system-file-hygiene-audit",
            "Renderer stages `.codex/workflows/system-file-hygiene-audit.md`",
            "done_through_m09",
            "T10-HYG-M08..M09",
            "Product-Agent OS technical docs",
            "runtime automation docs",
            "root README",
            "source registry/backlog",
            "activation approval requirements",
            "renderer_file_count: 194",
            "maintained file classes",
            "read-only boundary",
            "candidate-only automation",
            "docs contract",
            "done_through_m12",
            "T10-HYG-M10..M12",
            "activation_gate",
            "accepted_residual_risks_present",
            "future_activation_handoff_required",
            "schedule text for non-metrics candidates",
            "done_through_m13",
            "T10-HYG-M13",
            "file_statuses",
            "mtime_utc",
            "age_days",
            "content_digest",
            "last_audit_at",
            "status_dashboard_projection",
            "system file hygiene projection is generated status evidence, not source of truth",
            "done_through_m15",
            "T10-HYG-M14..M15",
            "System Hygiene",
            "system-file-hygiene",
            "status_dashboard.py",
            "status-dashboard/status.html",
            "status-dashboard/status.css",
            "top_finding",
            "missing",
            "unreadable",
            "stale",
            "owner_unknown",
            "done_through_m17",
            "T10-HYG-M16..M17",
            "system_file_hygiene_dashboard_present",
            "system_file_status_dates_present",
            "agent_skill_file_status_present",
            "system_hygiene_dashboard_not_source_of_truth",
            "filesystem metadata",
            "freshness hints",
            "not semantic proof",
            "batch36_final_closure",
            "strict_mkdocs_environment_gap",
            "No module named mkdocs",
            "audit_trigger",
            "no_secrets_status",
            "active_schedule_markers",
            "finding_type",
            "compaction_decision",
            "approval_boundary",
            "--trigger",
            "owner-approved slice",
        ]:
            with self.subTest(system_file_hygiene_contract=expected):
                self.assertIn(expected, combined)

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
                text = self._localized_contract_text(path)
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

        text = self._localized_contract_text(path)
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
        behavioral_evals = self._localized_contract_text(PRODUCT_AGENT_OS / "behavioral-evals.md")
        scenarios = self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md")
        root_readme = ROOT_README.read_text(encoding="utf-8")
        plugin_readme = PLUGIN_README.read_text(encoding="utf-8")
        control_plane = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [REQUIREMENTS]
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

        for expected in [
            "Guided question protocol",
            "one blocking question maximum",
            ".codex/product-agent-os/status.html",
            ".codex/product-agent-os/status.json",
            "dashboard is a generated view",
            "no success claim from stale evidence",
        ]:
            with self.subTest(root_readme=expected):
                self.assertIn(expected, root_readme)

    def test_track10_task24_self_verification_docs_and_control_plane_are_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
            "behavioral_evals": self._localized_contract_text(PRODUCT_AGENT_OS / "behavioral-evals.md"),
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "control-plane artifacts",
            "staged evidence",
            "report",
            "live eval/model/API calls",
            "active schedules",
            "self-applied updates",
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
            "index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            for path in [REQUIREMENTS]
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
            "Batch 20 local backend gate",
            "Batch 21 semantic retrieval gate",
            "Batch 22 local deterministic LLM proposal gate",
            "Batch 23 extension",
            "project_graph_extension_closure.py",
            "planning matrix presence remains not implementation evidence",
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            for path in [ROOT_README, PLUGIN_README, REQUIREMENTS]
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
                "M37-M41",
                "owner_closed_no_op_git_release_pr",
                "separately scoped",
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
            text = self._localized_contract_text(path)
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
            for path in [ROOT_README, PLUGIN_README, REQUIREMENTS]
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

        public_ready_pages = self._batch34_public_ready_pages()

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

    def test_track10_task26_batch34c_ru_en_i18n_localization_is_enabled(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        plan = TRACK10_PLAN.read_text(encoding="utf-8")
        config = MKDOCS.read_text(encoding="utf-8")
        check_docs = CHECK_DOCS.read_text(encoding="utf-8")
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        packet = BATCH34C_I18N_LOCALIZATION.read_text(encoding="utf-8")
        control_plane = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [REQUIREMENTS]
        )

        for expected in [
            "mkdocs-static-i18n",
            "B34-I18N-M24",
            "B34-I18N-M25",
            "B34-I18N-M26",
            "B34-I18N-M27",
            "B34-I18N-M28",
            "B34-I18N-M29",
            "B34-I18N-M30",
            "RU default at site root",
            "EN under /en/",
            "fallback_to_default: false",
            "reconfigure_material: true",
            "reconfigure_search: false",
            "terminology_allowlist",
            "localized_page_parity",
            "no live server",
            "no browser automation",
            "no provider/live external model/API calls",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]:
            with self.subTest(packet=expected):
                self.assertIn(expected, packet)

        for expected in [
            "mkdocs-static-i18n",
            "- i18n:",
            "docs_structure: suffix",
            "fallback_to_default: false",
            "reconfigure_material: true",
            "reconfigure_search: false",
            "locale: ru",
            "default: true",
            "locale: en",
            "link: /en/",
            "theme:",
            "language: en",
            "site_name: Product-Agent OS Documentation",
            "site_description: Product documentation for Product-Agent OS.",
        ]:
            with self.subTest(mkdocs=expected):
                self.assertIn(expected, config)

        self.assertIn("mkdocs-static-i18n", requirements)
        self.assertIn('sources" / "product-agent-os-batch34c-i18n-localization.md', check_docs)

        public_forbidden_pattern = re.compile(
            r"\b(Task|Track|Batch)\b|T[0-9]+-[A-Z0-9-]+|B[0-9]+-[A-Z]+-M[0-9]+"
        )
        for path in self._batch34_public_ready_pages():
            rel_path = path.relative_to(ROOT).as_posix()
            text = path.read_text(encoding="utf-8")
            en_path = path.with_name(path.stem + ".en" + path.suffix)
            en_rel_path = en_path.relative_to(ROOT).as_posix()

            with self.subTest(ru_source_status=rel_path):
                self.assertIn("Source status:", text)
            with self.subTest(en_exists=en_rel_path):
                self.assertTrue(en_path.exists(), en_path)

            en_text = en_path.read_text(encoding="utf-8")
            with self.subTest(en_source_status=en_rel_path):
                self.assertIn("Source status:", en_text)
            with self.subTest(packet_lists_page=rel_path):
                self.assertIn(rel_path, packet)
                self.assertIn(en_rel_path, packet)
            with self.subTest(en_is_english=en_rel_path):
                self.assertIn("Source status:", en_text)
                self.assertIn("Inputs", en_text)
                self.assertIn("Outputs", en_text)
                self.assertIn("Verification", en_text)
                self.assertIn("Risks", en_text)
                self.assertNotRegex(en_text, r"[А-Яа-яЁё]{4,}")
            with self.subTest(public_forbidden_terms=rel_path):
                self.assertIsNone(public_forbidden_pattern.search(text), rel_path)
                self.assertIsNone(public_forbidden_pattern.search(en_text), en_rel_path)

        for expected in [
            "Approved terms that may remain English in RU pages:",
            "Product-Agent OS",
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
            "Forbidden non-term English prose examples in RU pages:",
        ]:
            with self.subTest(terminology_policy=expected):
                self.assertIn(expected, packet)

        for expected in [
            "Product-Agent OS Batch 34C RU/EN I18N localization packet",
            "B34-I18N-M24..M30",
            "mkdocs-static-i18n",
            "localized_page_parity",
            "verification_status:",
        ]:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        for expected in [
            "`done_through_m30` | Batch 34C RU/EN localization |",
            "B34-I18N-M24..M30",
            "RU default at site root",
            "EN under `/en/`",
            "localized_page_parity",
            "Batch 34D product docs QA and closure",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        for expected in [
            "Batch 34C: RU/EN I18N And L10N Enablement",
            "B34-I18N-M24",
            "B34-I18N-M30",
            "Execution status through Batch 34C",
        ]:
            with self.subTest(plan=expected):
                self.assertIn(expected, plan)

        for expected in [
            "Batch 34C RU/EN localization",
            "B34-I18N-M24..M30",
            "mkdocs-static-i18n",
            "localized_page_parity",
            "no live server",
            "no browser automation",
            "no provider/live external model/API calls",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]:
            with self.subTest(control_plane=expected):
                self.assertIn(expected, control_plane)

    def test_track10_task26_batch34d_product_docs_qa_and_closure_is_recorded(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        plan = TRACK10_PLAN.read_text(encoding="utf-8")
        config = MKDOCS.read_text(encoding="utf-8")
        check_docs = CHECK_DOCS.read_text(encoding="utf-8")
        packet = BATCH34D_QA_CLOSURE.read_text(encoding="utf-8")
        control_plane = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [REQUIREMENTS]
        )

        for expected in [
            "B34-QA-M31",
            "B34-QA-M32",
            "B34-QA-M33",
            "public_forbidden_terms",
            "localized_page_parity",
            "Source status",
            "localized_nav_coverage",
            "static_html_language_switcher_evidence",
            "regular site/ rebuild evidence",
            "no live server",
            "no browser automation",
            "no provider/live external model/API calls",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]:
            with self.subTest(packet=expected):
                self.assertIn(expected, packet)

        public_forbidden_pattern = re.compile(
            r"\b(Task|Track|Batch)\b|T[0-9]+-[A-Z0-9-]+|B[0-9]+-[A-Z]+-M[0-9]+"
        )
        for path in self._batch34_public_ready_pages():
            rel_path = path.relative_to(ROOT).as_posix()
            en_path = path.with_name(path.stem + ".en" + path.suffix)
            en_rel_path = en_path.relative_to(ROOT).as_posix()
            text = path.read_text(encoding="utf-8")
            en_text = en_path.read_text(encoding="utf-8")

            with self.subTest(source_status=rel_path):
                self.assertIn("Source status:", text)
                self.assertIn("Source status:", en_text)
            with self.subTest(public_forbidden_terms=rel_path):
                self.assertIsNone(public_forbidden_pattern.search(text), rel_path)
                self.assertIsNone(public_forbidden_pattern.search(en_text), en_rel_path)
            with self.subTest(localized_page_parity=rel_path):
                self.assertTrue(en_path.exists(), en_path)
                self.assertIn(rel_path, packet)
                self.assertIn(en_rel_path, packet)
            with self.subTest(en_has_no_cyrillic=en_rel_path):
                self.assertIsNone(re.search(r"[\u0400-\u04FF]", en_text), en_rel_path)

        for expected in [
            "plugins:",
            "- i18n:",
            "docs_structure: suffix",
            "fallback_to_default: false",
            "reconfigure_material: true",
            "reconfigure_search: false",
            "locale: ru",
            "locale: en",
            "link: /en/",
            "name: RU",
            "name: EN",
        ]:
            with self.subTest(localized_nav_coverage=expected):
                self.assertIn(expected, config)

        for expected in [
            SITE / "index.html",
            SITE / "en" / "index.html",
            SITE / "product-agent-os" / "index.html",
            SITE / "en" / "product-agent-os" / "index.html",
        ]:
            with self.subTest(rendered_site=expected):
                self.assertTrue(expected.exists(), expected)

        rendered_html = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [
                SITE / "index.html",
                SITE / "en" / "index.html",
                SITE / "product-agent-os" / "index.html",
                SITE / "en" / "product-agent-os" / "index.html",
            ]
        )
        for expected in [
            "md-select",
            'hreflang="ru"',
            'hreflang="en"',
            "/en/",
        ]:
            with self.subTest(static_html_language_switcher_evidence=expected):
                self.assertIn(expected, rendered_html)

        self.assertIn('sources" / "product-agent-os-batch34d-product-docs-qa-closure.md', check_docs)

        for expected in [
            "Product-Agent OS Batch 34D product docs QA and closure packet",
            "B34-QA-M31..M33",
            "static_html_language_switcher_evidence",
            "regular site/ rebuild evidence",
            "verification_status:",
        ]:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        for expected in [
            "`done_through_m33` | Batch 34D product docs QA and closure |",
            "B34-QA-M31..M33",
            "public_forbidden_terms",
            "localized_page_parity",
            "static_html_language_switcher_evidence",
            "regular site/ rebuild evidence",
            "Batch 35 execution remains separate and approval-required",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        for expected in [
            "Batch 34D: Product Docs QA And Closure",
            "B34-QA-M31",
            "B34-QA-M33",
            "done_through_m33",
            "Execution status through Batch 34D",
        ]:
            with self.subTest(plan=expected):
                self.assertIn(expected, plan)

        for expected in [
            "Batch 34D product docs QA and closure",
            "B34-QA-M31..M33",
            "public_forbidden_terms",
            "localized_page_parity",
            "static_html_language_switcher_evidence",
            "regular site/ rebuild evidence",
            "no live server",
            "no browser automation",
            "no provider/live external model/API calls",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]:
            with self.subTest(control_plane=expected):
                self.assertIn(expected, control_plane)

    def test_track10_task26_local_file_language_switcher_is_file_safe(self):
        config = MKDOCS.read_text(encoding="utf-8")
        script = LOCAL_FILE_I18N_JS.read_text(encoding="utf-8")

        self.assertIn("assets/javascripts/local-file-i18n.js", config)
        for expected in [
            'window.location.protocol !== "file:"',
            'a[href="/en/"], link[href="/en/"]',
            'a[href="/"], link[href="/"]',
            "assets/javascripts/local-file-i18n.js",
            "en/index.html",
        ]:
            with self.subTest(local_file_i18n_guard=expected):
                self.assertIn(expected, script)

        pages_with_absolute_en = []
        for path in SITE.rglob("*.html"):
            html = path.read_text(encoding="utf-8")
            if 'href="/en/"' in html:
                pages_with_absolute_en.append(path)
                with self.subTest(local_file_guard_loaded=path.relative_to(ROOT).as_posix()):
                    self.assertIn("assets/javascripts/local-file-i18n.js", html)

        self.assertEqual(
            [],
            [path.relative_to(SITE).as_posix() for path in pages_with_absolute_en],
            "full-site i18n parity should not leave RU pages with absolute /en/ fallback links",
        )
        self.assertTrue((SITE / "en" / "index.html").exists())

    def test_track10_task26_ru_localized_pages_do_not_use_english_explanatory_copy(self):
        localized_ru_pages = sorted(
            path
            for path in self._batch34_public_ready_pages()
            if path.exists()
            and path.with_name(path.stem + ".en" + path.suffix).exists()
        )
        self.assertGreaterEqual(len(localized_ru_pages), 35)

        english_markers = {
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "before",
            "by",
            "can",
            "default",
            "do",
            "does",
            "each",
            "for",
            "from",
            "has",
            "have",
            "in",
            "into",
            "is",
            "it",
            "its",
            "no",
            "not",
            "of",
            "on",
            "only",
            "or",
            "over",
            "path",
            "remain",
            "remains",
            "run",
            "runs",
            "start",
            "starts",
            "support",
            "supports",
            "that",
            "the",
            "this",
            "through",
            "to",
            "under",
            "use",
            "used",
            "uses",
            "validate",
            "validates",
            "when",
            "where",
            "with",
            "without",
            "write",
            "writes",
        }
        forbidden_phrases = [
            "Target users",
            "Supported surfaces",
            "Plugin package",
            "Lifecycle state machine",
            "Generated project files",
            "System file update policy",
            "Failure modes",
            "Acceptance criteria",
            "Definition of ready",
            "Current operating boundary",
            "Inputs",
            "Outputs",
            "Verification",
            "Risks",
            "Expected behavior",
            "Forbidden behavior",
            "Source of truth",
            "Not source of truth",
            "Generated artifacts are",
            "This page",
            "This order",
            "The loop",
            "Expected artifacts",
            "Navigation and docs tooling",
        ]
        allowed_line_prefixes = ("Source status:", "Источники:")
        word_pattern = re.compile(r"[A-Za-z][A-Za-z0-9_./-]*")

        unexpected = {}
        for path in localized_ru_pages:
            in_code = False
            page_hits = []
            for line_no, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
                stripped = line.strip().lstrip("\ufeff")
                if stripped.startswith("```"):
                    in_code = not in_code
                    continue
                if in_code or not stripped or stripped.startswith("| ---"):
                    continue
                if stripped.startswith(allowed_line_prefixes):
                    continue

                cleaned = re.sub(r"https?://\S+", " ", stripped)
                cleaned = re.sub(r"`[^`]*`", " ", cleaned)
                cleaned = re.sub(r"\buse cases?\b", " ", cleaned, flags=re.I)
                words = word_pattern.findall(cleaned)
                marker_count = sum(
                    1 for word in words if word.lower().strip("./-") in english_markers
                )
                phrase_hit = next(
                    (phrase for phrase in forbidden_phrases if phrase in cleaned), None
                )
                if marker_count >= 2 or phrase_hit:
                    page_hits.append(f"{line_no}: {stripped}")

            if page_hits:
                unexpected[path.relative_to(ROOT).as_posix()] = page_hits[:10]

        self.assertEqual({}, unexpected)

    def test_track10_task26_batch34e_m45_full_site_ru_quality_red_gate(self):
        packet = BATCH34E_FULL_SITE_INVENTORY.read_text(encoding="utf-8")
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        plan = TRACK10_PLAN.read_text(encoding="utf-8")
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
        }

        for expected in [
            "B34E-I18N-M45",
            "done_through_m45",
            "full_site_ru_quality_sweep",
            "ru_source_forbidden_english_phrase_hits: 0",
        ]:
            with self.subTest(packet=expected):
                self.assertIn(expected, packet)

        for expected in [
            "| `done_through_m45` | Batch 34E M45 RU quality sweep |",
            "full_site_ru_quality_sweep",
            "B34E-I18N-M46..M49",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        for expected in [
            "Product-Agent OS Batch 34E M45 RU quality sweep",
            "full_site_ru_quality_sweep",
            "verification_status:",
        ]:
            with self.subTest(registry=expected):
                self.assertIn(expected, registry)

        self.assertIn("Execution status through Batch 34E M45", plan)

        for filename, text in control_plane.items():
            for expected in [
                "B34E-I18N-M45",
                "done_through_m45",
                "full_site_ru_quality_sweep",
                "B34E-I18N-M46..M49",
                "no live server",
                "no browser automation",
                "no provider/live external model/API calls",
                "no canonical graph mutation",
                "no git stage/commit/push/PR",
            ]:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

        localized_ru_pages = self._localized_markdown_pages()
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(localized_ru_pages))
        self.assertEqual([], self._missing_localized_en_siblings())

        forbidden_phrases = [
            "Target users",
            "Supported surfaces",
            "Plugin package",
            "Lifecycle state machine",
            "Generated project files",
            "System file update policy",
            "Failure modes",
            "Acceptance criteria",
            "Definition of ready",
            "Current operating boundary",
            "Expected behavior",
            "Forbidden behavior",
            "Source of truth",
            "Not source of truth",
            "Generated artifacts are",
            "This page",
            "This order",
            "The loop",
            "Expected artifacts",
            "Navigation and docs tooling",
        ]
        unexpected = {}
        for path in localized_ru_pages:
            hits = []
            in_code = False
            for line_no, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
                stripped = line.strip().lstrip("\ufeff")
                if stripped.startswith("```"):
                    in_code = not in_code
                    continue
                if in_code or not stripped:
                    continue
                cleaned = re.sub(r"https?://\S+", " ", stripped)
                cleaned = re.sub(r"`[^`]*`", " ", cleaned)
                phrase_hit = next(
                    (phrase for phrase in forbidden_phrases if phrase in cleaned), None
                )
                if phrase_hit:
                    hits.append(f"{line_no}: {stripped}")
            if hits:
                unexpected[path.relative_to(ROOT).as_posix()] = hits[:10]

        self.assertEqual({}, unexpected)

    def test_track10_task26_batch34e_m46_language_switcher_parity_is_recorded(self):
        packet = BATCH34E_FULL_SITE_INVENTORY.read_text(encoding="utf-8")
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        plan = TRACK10_PLAN.read_text(encoding="utf-8")
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
        }

        for expected in [
            "B34E-I18N-M46",
            "done_through_m46",
            "full_site_language_switcher_parity",
            "static_language_switcher_pairs_checked: 120",
            "english_original_pages_total: 7",
            "language_switcher_pair_failures: 0",
            "file_url_escape_failures: 0",
        ]:
            with self.subTest(packet=expected):
                self.assertIn(expected, packet)

        for expected in [
            "| `done_through_m46` | Batch 34E M46 full-site language switcher parity |",
            "full_site_language_switcher_parity",
            "B34E-I18N-M47..M49",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        for expected in [
            "Product-Agent OS Batch 34E M46 language switcher parity",
            "full_site_language_switcher_parity",
            "verification_status:",
        ]:
            with self.subTest(registry=expected):
                self.assertIn(expected, registry)

        self.assertIn("Execution status through Batch 34E M46", plan)

        for filename, text in control_plane.items():
            for expected in [
                "B34E-I18N-M46",
                "done_through_m46",
                "full_site_language_switcher_parity",
                "B34E-I18N-M47..M49",
                "no live server",
                "no browser automation",
                "no provider/live external model/API calls",
                "no canonical graph mutation",
                "no git stage/commit/push/PR",
            ]:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

        source_pages = self._localized_markdown_pages()
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(source_pages))
        self.assertEqual([], self._missing_localized_en_siblings())

        missing_rendered = []
        pair_failures = []
        file_escape_failures = []
        site_root = SITE.resolve()
        for source_path in source_pages:
            ru_html = self._rendered_site_path_for_source(source_path)
            en_html = self._rendered_site_path_for_source(source_path, locale="en")
            expected = {
                "ru": ru_html.resolve(),
                "en": en_html.resolve(),
            }

            for rendered in [ru_html, en_html]:
                if not rendered.exists():
                    missing_rendered.append(rendered.relative_to(SITE).as_posix())

            if missing_rendered:
                continue

            pages = {
                "ru": (ru_html, self._language_switcher_hrefs(ru_html.read_text(encoding="utf-8"))),
                "en": (en_html, self._language_switcher_hrefs(en_html.read_text(encoding="utf-8"))),
            }
            for page_locale, (html_path, links) in pages.items():
                for target_locale, expected_path in expected.items():
                    hrefs = links.get(target_locale, [])
                    if not hrefs:
                        pair_failures.append(
                            f"{html_path.relative_to(SITE).as_posix()}: missing {target_locale}"
                        )
                        continue

                    resolved_hrefs = []
                    for href in hrefs:
                        resolved = self._resolve_site_href(html_path, href)
                        if resolved is None:
                            file_escape_failures.append(
                                f"{html_path.relative_to(SITE).as_posix()}: {target_locale} -> {href}"
                            )
                            continue
                        try:
                            resolved.relative_to(site_root)
                        except ValueError:
                            file_escape_failures.append(
                                f"{html_path.relative_to(SITE).as_posix()}: {target_locale} -> {href}"
                            )
                            continue
                        resolved_hrefs.append(resolved)

                    if expected_path not in resolved_hrefs:
                        pair_failures.append(
                            f"{html_path.relative_to(SITE).as_posix()}: "
                            f"{page_locale}->{target_locale} expected "
                            f"{expected_path.relative_to(SITE).as_posix()}"
                        )

        self.assertEqual([], missing_rendered[:20])
        self.assertEqual([], pair_failures[:20])
        self.assertEqual([], file_escape_failures[:20])

    def test_track10_task26_batch34e_m47_search_sitemap_parity_is_recorded(self):
        packet = BATCH34E_FULL_SITE_INVENTORY.read_text(encoding="utf-8")
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        plan = TRACK10_PLAN.read_text(encoding="utf-8")
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
        }

        for expected in [
            "B34E-I18N-M47",
            "done_through_m47",
            "full_site_search_sitemap_parity",
            "strict_mkdocs_build_exit_code: 0",
            "search_index_ru_pages_present: 120",
            "search_index_en_pages_present: 120",
            "sitemap_ru_pages_present: 120",
            "sitemap_en_pages_present: 120",
            "english_original_pages_total: 7",
            "search_index_ru_fallback_pollution: 0",
            "sitemap_ru_fallback_pollution: 0",
        ]:
            with self.subTest(packet=expected):
                self.assertIn(expected, packet)

        for expected in [
            "| `done_through_m47` | Batch 34E M47 search, sitemap and strict build parity |",
            "full_site_search_sitemap_parity",
            "B34E-I18N-M48..M49",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        for expected in [
            "Product-Agent OS Batch 34E M47 search sitemap and strict build parity",
            "full_site_search_sitemap_parity",
            "verification_status:",
        ]:
            with self.subTest(registry=expected):
                self.assertIn(expected, registry)

        self.assertIn("Execution status through Batch 34E M47", plan)

        for filename, text in control_plane.items():
            for expected in [
                "B34E-I18N-M47",
                "done_through_m47",
                "full_site_search_sitemap_parity",
                "B34E-I18N-M48..M49",
                "no live server",
                "no browser automation",
                "no provider/live external model/API calls",
                "no canonical graph mutation",
                "no git stage/commit/push/PR",
            ]:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

        source_pages = self._localized_markdown_pages()
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(source_pages))
        self.assertEqual([], self._missing_localized_en_siblings())

        expected_ru = {
            source_path.relative_to(DOCS).with_suffix(".html").as_posix()
            for source_path in source_pages
        }
        expected_en = {
            "en/" + source_path.relative_to(DOCS).with_suffix(".html").as_posix()
            for source_path in source_pages
        }

        search_index = SITE / "search" / "search_index.json"
        sitemap = SITE / "sitemap.xml"
        self.assertTrue(search_index.exists())
        self.assertTrue(sitemap.exists())

        search_locations = {
            doc.get("location", "").split("#", 1)[0]
            for doc in json.loads(search_index.read_text(encoding="utf-8")).get("docs", [])
        }
        sitemap_locations = set(
            match.split("#", 1)[0]
            for match in re.findall(
                r"<loc>(.*?)</loc>",
                sitemap.read_text(encoding="utf-8"),
            )
        )

        missing_search_ru = sorted(expected_ru - search_locations)
        missing_search_en = sorted(expected_en - search_locations)
        missing_sitemap_ru = sorted(expected_ru - sitemap_locations)
        missing_sitemap_en = sorted(expected_en - sitemap_locations)

        self.assertEqual([], missing_search_ru[:20])
        self.assertEqual([], missing_search_en[:20])
        self.assertEqual([], missing_sitemap_ru[:20])
        self.assertEqual([], missing_sitemap_en[:20])
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(expected_ru & search_locations))
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(expected_en & search_locations))
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(expected_ru & sitemap_locations))
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(expected_en & sitemap_locations))

    def test_track10_task26_batch34e_m48_m49_final_closure_is_recorded(self):
        packet = BATCH34E_FULL_SITE_INVENTORY.read_text(encoding="utf-8")
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        plan = TRACK10_PLAN.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
        }

        for expected in [
            "B34E-I18N-M48",
            "B34E-I18N-M49",
            "done_through_m48",
            "done_through_m49",
            "full_site_i18n_closure",
            "full_site_i18n_final_evidence",
            "strict_mkdocs_final_closure_exit_code: 0",
            "docs_ru_pages_total: 127",
            "english_original_pages_total: 7",
            "localized_ru_pages_total: 120",
            "existing_en_siblings: 120",
            "missing_localized_en_siblings: 0",
            "rendered_ru_pages_checked: 120",
            "rendered_en_pages_checked: 120",
            "static_language_switcher_pairs_checked: 120",
            "language_switcher_pair_failures: 0",
            "file_url_escape_failures: 0",
            "search_index_ru_pages_present: 120",
            "search_index_en_pages_present: 120",
            "sitemap_ru_pages_present: 120",
            "sitemap_en_pages_present: 120",
            "en_source_cyrillic_hits: 0",
            "ru_source_forbidden_english_phrase_hits: 0",
        ]:
            with self.subTest(packet=expected):
                self.assertIn(expected, packet)

        for expected in [
            "| `done_through_m49` | Batch 34E M48-M49 final full-site i18n closure |",
            "full_site_i18n_closure",
            "full_site_i18n_final_evidence",
            "B34E-I18N-M48..M49",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)
        self.assertNotIn("| `planned` | Batch 34E remaining build and closure gates |", backlog)

        for expected in [
            "Product-Agent OS Batch 34E M48-M49 final full-site i18n closure",
            "full_site_i18n_closure",
            "full_site_i18n_final_evidence",
            "verification_status:",
        ]:
            with self.subTest(registry=expected):
                self.assertIn(expected, registry)

        self.assertIn("Execution status through Batch 34E M49", plan)

        for document, text in self._internal_history_documents(documents).items():
            for expected in [
                "Batch 34E full-site i18n parity",
                "B34E-I18N-M48..M49",
                "done_through_m49",
                "full_site_i18n_closure",
                "full_site_i18n_final_evidence",
                "no remaining Batch 34E gates",
                "Batch 35",
            ]:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        for filename, text in control_plane.items():
            for expected in [
                "B34E-I18N-M48..M49",
                "done_through_m49",
                "full_site_i18n_closure",
                "full_site_i18n_final_evidence",
                "strict_mkdocs_final_closure_exit_code: 0",
                "no remaining Batch 34E gates",
                "Batch 35",
                "no live server",
                "no browser automation",
                "no provider/live external model/API calls",
                "no canonical graph mutation",
                "no git stage/commit/push/PR",
            ]:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

        base_pages = self._base_markdown_pages()
        source_pages = self._localized_markdown_pages()
        english_original_pages = self._english_original_markdown_pages()
        paired_pages = [
            path
            for path in source_pages
            if self._en_sibling_for(path).exists()
        ]
        missing_pages = self._missing_localized_en_siblings()
        self.assertEqual(BUILDABLE_MARKDOWN_PAGE_COUNT, len(base_pages))
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(source_pages))
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(paired_pages))
        self.assertEqual(ENGLISH_ORIGINAL_MARKDOWN_PAGE_COUNT, len(english_original_pages))
        self.assertEqual([], [path.relative_to(DOCS).as_posix() for path in missing_pages])
        self.assertEqual(
            [],
            [
                self._en_sibling_for(path).relative_to(DOCS).as_posix()
                for path in english_original_pages
                if self._en_sibling_for(path).exists()
            ],
        )

        expected_ru = {
            source_path.relative_to(DOCS).with_suffix(".html").as_posix()
            for source_path in source_pages
        }
        expected_en = {
            "en/" + source_path.relative_to(DOCS).with_suffix(".html").as_posix()
            for source_path in source_pages
        }
        rendered_missing = []
        for source_path in source_pages:
            for locale in (None, "en"):
                rendered = self._rendered_site_path_for_source(source_path, locale)
                if not rendered.exists():
                    rendered_missing.append(rendered.relative_to(SITE).as_posix())
        self.assertEqual([], rendered_missing[:20])

        pair_failures = []
        file_escape_failures = []
        site_root = SITE.resolve()
        for source_path in source_pages:
            ru_html = self._rendered_site_path_for_source(source_path)
            en_html = self._rendered_site_path_for_source(source_path, "en")
            pages = {
                "ru": (ru_html, self._language_switcher_hrefs(ru_html.read_text(encoding="utf-8"))),
                "en": (en_html, self._language_switcher_hrefs(en_html.read_text(encoding="utf-8"))),
            }
            expected_paths = {"ru": ru_html.resolve(), "en": en_html.resolve()}
            for page_locale, (html_path, hrefs_by_locale) in pages.items():
                target_locale = "en" if page_locale == "ru" else "ru"
                hrefs = hrefs_by_locale.get(target_locale, [])
                if not hrefs:
                    pair_failures.append(
                        f"{html_path.relative_to(SITE).as_posix()}: missing {target_locale}"
                    )
                    continue
                resolved_hrefs = []
                for href in hrefs:
                    resolved = self._resolve_site_href(html_path, href)
                    if resolved is None:
                        file_escape_failures.append(
                            f"{html_path.relative_to(SITE).as_posix()}: {target_locale} -> {href}"
                        )
                        continue
                    try:
                        resolved.relative_to(site_root)
                    except ValueError:
                        file_escape_failures.append(
                            f"{html_path.relative_to(SITE).as_posix()}: {target_locale} -> {href}"
                        )
                        continue
                    resolved_hrefs.append(resolved)
                if expected_paths[target_locale] not in resolved_hrefs:
                    pair_failures.append(
                        f"{html_path.relative_to(SITE).as_posix()}: "
                        f"{page_locale}->{target_locale} expected "
                        f"{expected_paths[target_locale].relative_to(SITE).as_posix()}"
                    )
        self.assertEqual([], pair_failures[:20])
        self.assertEqual([], file_escape_failures[:20])

        search_index = SITE / "search" / "search_index.json"
        sitemap = SITE / "sitemap.xml"
        self.assertTrue(search_index.exists())
        self.assertTrue(sitemap.exists())
        search_locations = {
            doc.get("location", "").split("#", 1)[0]
            for doc in json.loads(search_index.read_text(encoding="utf-8")).get("docs", [])
        }
        sitemap_locations = set(
            match.split("#", 1)[0]
            for match in re.findall(
                r"<loc>(.*?)</loc>",
                sitemap.read_text(encoding="utf-8"),
            )
        )
        self.assertEqual([], sorted(expected_ru - search_locations)[:20])
        self.assertEqual([], sorted(expected_en - search_locations)[:20])
        self.assertEqual([], sorted(expected_ru - sitemap_locations)[:20])
        self.assertEqual([], sorted(expected_en - sitemap_locations)[:20])
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(expected_ru & search_locations))
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(expected_en & search_locations))
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(expected_ru & sitemap_locations))
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(expected_en & sitemap_locations))

        en_cyrillic = [
            path.relative_to(DOCS).as_posix()
            for path in DOCS.rglob("*.en.md")
            if re.search(r"[\u0400-\u04FF]", path.read_text(encoding="utf-8-sig"))
        ]
        self.assertEqual([], en_cyrillic[:20])

    def test_track10_task26_batch34e_full_site_i18n_parity_is_planned(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        plan = TRACK10_PLAN.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
        }

        ru_pages = self._base_markdown_pages()
        localized_pages = self._localized_markdown_pages()
        english_original_pages = self._english_original_markdown_pages()
        paired_pages = [
            path
            for path in localized_pages
            if self._en_sibling_for(path).exists()
        ]
        missing_pages = self._missing_localized_en_siblings()

        self.assertEqual(BUILDABLE_MARKDOWN_PAGE_COUNT, len(ru_pages))
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(localized_pages))
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(paired_pages))
        self.assertEqual(ENGLISH_ORIGINAL_MARKDOWN_PAGE_COUNT, len(english_original_pages))
        self.assertEqual(0, len(missing_pages))

        for expected in [
            "Batch 34E: Full-Site I18N Parity Corrective Plan",
            "B34E-I18N-M34..M49",
            "docs_ru_pages_total: 127",
            "english_original_pages_total: 7",
            "localized_ru_pages_total: 120",
            "existing_en_siblings: 120",
            "missing_localized_en_siblings: 0",
            "every localized RU Markdown page has a `.en.md` sibling",
            "full EN navigation/search/sitemap coverage",
            "no missing-page language-switcher fallback",
            "Batch 34C remains valid only for the promoted public-ready page set",
        ]:
            with self.subTest(plan=expected):
                self.assertIn(expected, plan)

        for marker in [f"B34E-I18N-M{number:02d}" for number in range(34, 50)]:
            with self.subTest(matrix_id=marker):
                self.assertIn(marker, plan)

        for expected in [
            "| `done_through_m37` | Batch 34E M34-M37 full-site i18n inventory and nav gate |",
            "| `done_through_m43` | Batch 34E M38-M43 EN sibling translation pass |",
            "| `done_through_m44` | Batch 34E M44 EN editorial quality sweep |",
            "| `done_through_m45` | Batch 34E M45 RU quality sweep |",
            "| `done_through_m46` | Batch 34E M46 full-site language switcher parity |",
            "| `done_through_m47` | Batch 34E M47 search, sitemap and strict build parity |",
            "| `done_through_m49` | Batch 34E M48-M49 final full-site i18n closure |",
            "B34E-I18N-M34..M37",
            "B34E-I18N-M38..M43",
            "B34E-I18N-M44",
            "B34E-I18N-M45",
            "B34E-I18N-M46",
            "B34E-I18N-M47",
            "B34E-I18N-M48..M49",
            "done_through_m49",
            "B34E-I18N-M45..M49",
            "B34E-I18N-M46..M49",
            "B34E-I18N-M47..M49",
            "docs_ru_pages_total: 127",
            "english_original_pages_total: 7",
            "localized_ru_pages_total: 120",
            "existing_en_siblings: 120",
            "missing_localized_en_siblings: 0",
            "full_site_en_nav_configured",
            "full_site_en_siblings_created",
            "full_site_en_editorial_quality_sweep",
            "full_site_ru_quality_sweep",
            "full_site_language_switcher_parity",
            "full_site_search_sitemap_parity",
            "full_site_i18n_closure",
            "full_site_i18n_final_evidence",
            "no remaining Batch 34E gates",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        self.assertNotIn("| `planned` | Batch 34E remaining build and closure gates |", backlog)

        for expected in [
            "Product-Agent OS Batch 34E full-site i18n parity corrective matrix",
            "Product-Agent OS Batch 34E M48-M49 final full-site i18n closure",
            "B34E-I18N-M34..M49",
            "full-site bilingual documentation",
            "docs_ru_pages_total: 127",
            "english_original_pages_total: 7",
            "localized_ru_pages_total: 120",
            "existing_en_siblings: 120",
            "missing_localized_en_siblings: 0",
            "full_site_en_siblings_created",
            "full_site_search_sitemap_parity",
            "full_site_i18n_closure",
            "full_site_i18n_final_evidence",
            "verification_status:",
        ]:
            with self.subTest(registry=expected):
                self.assertIn(expected, registry)

        for document, text in self._internal_history_documents(documents).items():
            for expected in [
                "Batch 34E full-site i18n parity",
                "B34E-I18N-M34..M37",
                "B34E-I18N-M38..M43",
                "B34E-I18N-M44",
                "B34E-I18N-M45",
                "B34E-I18N-M47",
                "B34E-I18N-M48..M49",
                "done_through_m49",
                "B34E-I18N-M47..M49",
                "Batch 34C localized the public-ready set only",
                "docs_ru_pages_total: 127",
                "english_original_pages_total: 7",
                "localized_ru_pages_total: 120",
                "existing_en_siblings: 120",
                "missing_localized_en_siblings: 0",
                "full_site_i18n_closure",
                "full_site_i18n_final_evidence",
                "no remaining Batch 34E gates",
                "complete through",
            ]:
                with self.subTest(document=document, term=expected):
                    self.assertIn(expected, text)

        for filename, text in control_plane.items():
            for expected in [
                "B34E-I18N-M34..M37",
                "B34E-I18N-M38..M43",
                "B34E-I18N-M44",
                "B34E-I18N-M45",
                "B34E-I18N-M45..M49",
                "B34E-I18N-M46..M49",
                "B34E-I18N-M47",
                "B34E-I18N-M47..M49",
                "B34E-I18N-M48..M49",
                "done_through_m49",
                "full_site_search_sitemap_parity",
                "full_site_i18n_closure",
                "full_site_i18n_final_evidence",
                "full-site i18n parity",
                "docs_ru_pages_total: 127",
                "english_original_pages_total: 7",
                "localized_ru_pages_total: 120",
                "existing_en_siblings: 120",
                "missing_localized_en_siblings: 0",
                "full_site_en_siblings_created",
                "full_site_en_editorial_quality_sweep",
                "full_site_ru_quality_sweep",
                "no remaining Batch 34E gates",
                "no live server",
                "no browser automation",
                "no provider/live external model/API calls",
                "no canonical graph mutation",
                "no git stage/commit/push/PR",
            ]:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task26_batch34e_m34_m37_inventory_and_nav_are_recorded(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        plan = TRACK10_PLAN.read_text(encoding="utf-8")
        check_docs = CHECK_DOCS.read_text(encoding="utf-8")
        config = MKDOCS.read_text(encoding="utf-8")
        self.assertTrue(BATCH34E_FULL_SITE_INVENTORY.exists(), BATCH34E_FULL_SITE_INVENTORY)
        packet = BATCH34E_FULL_SITE_INVENTORY.read_text(encoding="utf-8")
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
        }

        ru_pages = self._base_markdown_pages()
        localized_pages = self._localized_markdown_pages()
        english_original_pages = self._english_original_markdown_pages()
        paired_pages = [
            path
            for path in localized_pages
            if self._en_sibling_for(path).exists()
        ]
        missing_pages = self._missing_localized_en_siblings()

        self.assertEqual(BUILDABLE_MARKDOWN_PAGE_COUNT, len(ru_pages))
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(localized_pages))
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(paired_pages))
        self.assertEqual(ENGLISH_ORIGINAL_MARKDOWN_PAGE_COUNT, len(english_original_pages))
        self.assertEqual(0, len(missing_pages))

        for expected in [
            "Source status:",
            "B34E-I18N-M34..M37",
            "full_site_i18n_inventory",
            "full_site_i18n_red_gate",
            "full_site_en_nav_configured",
            "full_site_en_siblings_created",
            "docs_ru_pages_total: 127",
            "english_original_pages_total: 7",
            "localized_ru_pages_total: 120",
            "existing_en_siblings: 120",
            "missing_localized_en_siblings: 0",
            "initial_m35_existing_en_siblings: 37",
            "initial_m35_missing_en_siblings: 90",
            "expected_red_full_site_i18n_parity",
            "fallback_to_default: false",
            "no missing-page language-switcher fallback",
        ]:
            with self.subTest(packet=expected):
                self.assertIn(expected, packet)

        for path in missing_pages:
            rel_path = path.relative_to(DOCS).as_posix()
            with self.subTest(missing_page_inventory=rel_path):
                self.assertIn(rel_path, packet)

        for expected in [
            'sources" / "product-agent-os-batch34e-full-site-i18n-inventory.md',
            "Product-Agent OS Batch 34E M34-M37 full-site i18n inventory and nav gate",
            "`done_through_m37` | Batch 34E M34-M37 full-site i18n inventory and nav gate |",
            "`done_through_m43` | Batch 34E M38-M43 EN sibling translation pass |",
            "Execution status through Batch 34E M34-M37",
            "Execution status through Batch 34E M38-M43",
        ]:
            with self.subTest(sync_term=expected):
                self.assertTrue(
                    expected in check_docs
                    or expected in registry
                    or expected in backlog
                    or expected in plan,
                    expected,
                )

        for expected in [
            "- Sources:",
            "- Codex:",
            "- Prompt And Context Engineering:",
            "- Product-Agent Workflows:",
            "- Product-Agent OS Plugin:",
            "- Methodologies For Large Projects:",
            "- Agent Systems:",
            "- Playbooks:",
            "- Templates:",
            "- Insights:",
            "sources/registry.md",
            "codex/overview.md",
            "prompting/overview.md",
            "product-agent-os/index.md",
            "methodologies/index.md",
            "agent-systems/overview.md",
            "playbooks/research-loop.md",
            "artifact-templates/prompt-packet.md",
            "insights/index.md",
        ]:
            with self.subTest(full_en_nav=expected):
                self.assertIn(expected, config)

        for filename, text in control_plane.items():
            for expected in [
                "B34E-I18N-M34..M37",
                "full_site_i18n_inventory",
                "full_site_i18n_red_gate",
                "full_site_en_nav_configured",
                "full_site_en_siblings_created",
                "expected_red_full_site_i18n_parity",
                "done_through_m44",
                "no live server",
                "no browser automation",
                "no provider/live external model/API calls",
                "no canonical graph mutation",
                "no git stage/commit/push/PR",
            ]:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

    def test_track10_task26_batch34e_english_original_plan_files_are_not_translation_gaps(self):
        packet = BATCH34E_FULL_SITE_INVENTORY.read_text(encoding="utf-8")
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        plan = TRACK10_PLAN.read_text(encoding="utf-8")
        english_original_pages = [
            DOCS / "superpowers" / "plans" / "2026-05-14-product-agent-os-generated-infrastructure.md",
            DOCS / "superpowers" / "plans" / "2026-05-14-product-agent-os-lifecycle-skills.md",
            DOCS / "superpowers" / "plans" / "2026-05-14-product-agent-os-plugin-core.md",
            DOCS / "superpowers" / "plans" / "2026-05-14-product-agent-os-production-hardening.md",
            DOCS / "superpowers" / "plans" / "2026-05-15-product-agent-os-codex-runtime-runner.md",
            DOCS / "superpowers" / "plans" / "2026-05-25-track-9-methodology-intelligence.md",
            DOCS / "superpowers" / "plans" / "2026-05-27-track-10-guided-questions-status-dashboard.md",
        ]
        base_pages = sorted(
            path
            for path in DOCS.rglob("*.md")
            if not path.name.endswith(".en.md")
        )
        localized_pages = [
            path for path in base_pages if path not in set(english_original_pages)
        ]
        missing_localized_siblings = [
            path.relative_to(DOCS).as_posix()
            for path in localized_pages
            if not path.with_name(path.stem + ".en" + path.suffix).exists()
        ]

        self.assertEqual(BUILDABLE_MARKDOWN_PAGE_COUNT, len(base_pages))
        self.assertEqual(7, len(english_original_pages))
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(localized_pages))
        self.assertEqual([], missing_localized_siblings)
        self.assertTrue(
            all(
                page.exists()
                and not page.with_name(page.stem + ".en" + page.suffix).exists()
                for page in english_original_pages
            )
        )

        for text in [packet, registry, backlog, plan]:
            for expected in [
                "english_original_pages_total: 7",
                "localized_ru_pages_total: 120",
                "existing_en_siblings: 120",
                "missing_localized_en_siblings: 0",
            ]:
                with self.subTest(expected=expected):
                    self.assertIn(expected, text)

    def test_track10_task26_batch34e_m38_m43_en_translations_exist(self):
        expected_pages = [
            "agent-systems/evals-observability.md",
            "agent-systems/memory.md",
            "agent-systems/overview.md",
            "agent-systems/sdk-patterns.md",
            "agent-systems/session-control.md",
            "agent-systems/templates.md",
            "artifact-templates/control-plane-files.md",
            "artifact-templates/plugin-blueprint.md",
            "artifact-templates/product-skill.md",
            "artifact-templates/prompt-packet.md",
            "artifact-templates/runlog.md",
            "codex/configuration.md",
            "codex/overview.md",
            "codex/security.md",
            "codex/surfaces.md",
            "codex/use-cases-deep-analysis.md",
            "codex/workflows.md",
            "insights/index.md",
            "insights/insight-card-template.md",
            "insights/seed-insights.md",
            "methodologies/api-integrations.md",
            "methodologies/backend.md",
            "methodologies/business-product.md",
            "methodologies/codex-agentic-workflow.md",
            "methodologies/database-data.md",
            "methodologies/delivery-release-operations.md",
            "methodologies/frontend.md",
            "methodologies/index.md",
            "methodologies/llm-ai-rag.md",
            "methodologies/quality-testing-evals.md",
            "methodologies/requirements-domain.md",
            "methodologies/security-privacy-compliance.md",
            "methodologies/solution-architecture.md",
            "playbooks/ai-team-design.md",
            "playbooks/build-full-feature.md",
            "playbooks/code-review.md",
            "playbooks/context7-deep-research.md",
            "playbooks/eval-driven-improvement.md",
            "playbooks/grounded-answering.md",
            "playbooks/maintain-agent-operating-docs.md",
            "playbooks/product-ready-pr.md",
            "playbooks/research-loop.md",
            "playbooks/workflow-to-skill.md",
            "prompting/anti-hallucination.md",
            "prompting/context-engineering.md",
            "prompting/overview.md",
            "prompting/question-design.md",
            "sources/add-ddd-tdd-fsd-llm-development.md",
            "sources/context7-research.md",
            "sources/deep-research-report.md",
            "sources/development-methodology-gap-matrix.md",
            "sources/development-methodology-research-log.md",
            "sources/methodology-research/api-integrations.md",
            "sources/methodology-research/backend.md",
            "sources/methodology-research/business-product.md",
            "sources/methodology-research/codex-agentic-workflow.md",
            "sources/methodology-research/database-data.md",
            "sources/methodology-research/delivery-release-operations.md",
            "sources/methodology-research/frontend.md",
            "sources/methodology-research/llm-ai-rag.md",
            "sources/methodology-research/quality-testing-evals.md",
            "sources/methodology-research/requirements-domain.md",
            "sources/methodology-research/security-privacy-compliance.md",
            "sources/methodology-research/solution-architecture.md",
            "sources/product-agent-os-batch34-packaging-install-smoke.md",
            "sources/product-agent-os-batch34a-public-docs-boundary.md",
            "sources/product-agent-os-batch34b-public-copy-rewrite.md",
            "sources/product-agent-os-batch34c-i18n-localization.md",
            "sources/product-agent-os-batch34d-product-docs-qa-closure.md",
            "sources/product-agent-os-batch35-approval-packet-draft.md",
            "sources/product-agent-os-final-predevelopment-review.md",
            "sources/product-agent-os-pre-track-8-implementation-inventory.md",
            "sources/product-agent-os-track-10-backlog.md",
            "sources/product-agent-os-track-8-detailed-backlog.md",
            "sources/product-agent-os-track-9-backlog.md",
            "sources/registry.md",
            "sources/source-card-template.md",
            "superpowers/specs/2026-05-14-product-agent-os-agents-sdk-runner-design.md",
            "superpowers/specs/2026-05-14-product-agent-os-generated-infrastructure-design.md",
            "superpowers/specs/2026-05-14-product-agent-os-lifecycle-skills-design.md",
            "superpowers/specs/2026-05-14-product-agent-os-production-hardening-design.md",
            "superpowers/specs/2026-05-15-product-agent-os-codex-runtime-runner-design.md",
            "superpowers/specs/2026-05-25-track-9-methodology-intelligence-design.md",
        ]

        missing = []
        cyrillic_hits = []
        for rel_path in expected_pages:
            source = DOCS / rel_path
            en_path = source.with_name(source.stem + ".en" + source.suffix)
            if not en_path.exists():
                missing.append(en_path.relative_to(DOCS).as_posix())
                continue

            text = en_path.read_text(encoding="utf-8-sig")
            if "Source status:" not in text:
                cyrillic_hits.append(f"{en_path.relative_to(DOCS).as_posix()}: missing Source status")
            if re.search(r"[\u0400-\u04FF]", text):
                cyrillic_hits.append(en_path.relative_to(DOCS).as_posix())

        self.assertEqual([], missing)
        self.assertEqual([], cyrillic_hits)

        packet = BATCH34E_FULL_SITE_INVENTORY.read_text(encoding="utf-8")
        for path in self._english_original_markdown_pages():
            rel_path = path.relative_to(DOCS).as_posix()
            with self.subTest(english_original_plan=rel_path):
                self.assertIn(rel_path, packet)
                self.assertFalse(self._en_sibling_for(path).exists())

    def test_track10_task26_batch34e_m44_en_editorial_quality_sweep_is_recorded(self):
        packet = BATCH34E_FULL_SITE_INVENTORY.read_text(encoding="utf-8")
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        plan = TRACK10_PLAN.read_text(encoding="utf-8")
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
        }

        for expected in [
            "B34E-I18N-M44",
            "done_through_m44",
            "full_site_en_editorial_quality_sweep",
            "en_source_cyrillic_hits: 0",
            "en_source_mojibake_hits: 0",
            "en_source_transliteration_hits: 0",
            "en_internal_link_failures: 0",
        ]:
            with self.subTest(packet=expected):
                self.assertIn(expected, packet)

        for expected in [
            "| `done_through_m44` | Batch 34E M44 EN editorial quality sweep |",
            "full_site_en_editorial_quality_sweep",
            "B34E-I18N-M45..M49",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        for expected in [
            "Product-Agent OS Batch 34E M44 EN editorial quality sweep",
            "full_site_en_editorial_quality_sweep",
            "verification_status:",
        ]:
            with self.subTest(registry=expected):
                self.assertIn(expected, registry)

        self.assertIn("Execution status through Batch 34E M44", plan)

        for filename, text in control_plane.items():
            for expected in [
                "B34E-I18N-M44",
                "done_through_m44",
                "full_site_en_editorial_quality_sweep",
                "B34E-I18N-M45..M49",
                "no live server",
                "no browser automation",
                "no provider/live external model/API calls",
                "no canonical graph mutation",
                "no git stage/commit/push/PR",
            ]:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

        transliteration_terms = [
            "sdelat",
            "dolzhen",
            "dolzhna",
            "dolzhny",
            "dokumentats",
            "istochnik",
            "istochniki",
            "istochnikov",
            "razrabot",
            "metodologiya",
            "metodologiy",
            "ispolz",
            "vyvod",
            "gotov",
            "tolko",
            "posle",
            "rasshireniya",
            "stsenar",
            "matrits",
            "proekta",
            "proveryat",
            "proverki",
            "proverku",
            "proveryaetsya",
            "proveryaemuyu",
            "proveryaet",
            "artefakt",
            "trebuet",
            "chelovechesk",
            "ponyat",
            "vazhny",
            "sobstvennyy",
            "kazhdaya",
            "statusov",
            "sokhranen",
            "zafiksirovat",
            "primenyaetsya",
            "izbytochna",
            "poka",
            "sredniy",
            "nizhe",
            "issledovaniya",
            "sostavit",
            "opisanie",
            "pervichnye",
            "ozhidaemyy",
            "kogda",
            "primenyat",
            "nuzh",
            "mozhno",
            "nelzya",
            "esli",
            "dlya",
            "kakie",
            "kakikh",
            "chto",
            "zhivut",
            "stranits",
            "bazovyy",
            "luchshe",
            "vybrat",
            "universalnyy",
        ]
        transliteration_re = re.compile(
            r"\b(?:"
            + "|".join(re.escape(term) for term in transliteration_terms)
            + r")\w*\b",
            re.IGNORECASE,
        )
        link_re = re.compile(
            r"!\[[^\]]*\]\(([^)]+)\)|(?<!!)\[[^\]]+\]\(([^)]+)\)"
        )

        content_issues = []
        link_issues = []
        for path in sorted(DOCS.rglob("*.en.md")):
            text = path.read_text(encoding="utf-8-sig")
            rel_path = path.relative_to(DOCS).as_posix()
            if re.search(r"[\u0400-\u04FF]", text):
                content_issues.append(f"{rel_path}: cyrillic")
            if any(marker in text for marker in ["\ufffd", "\u00d0", "\u00d1"]):
                content_issues.append(f"{rel_path}: mojibake")
            if transliteration_re.search(text):
                content_issues.append(f"{rel_path}: transliteration")
            lowered = text.lower()
            if "???" in text or "translation pending" in lowered:
                content_issues.append(f"{rel_path}: placeholder")

            link_scan_text = re.sub(r"(?ms)^```.*?^```", "", text)
            for match in link_re.finditer(link_scan_text):
                raw_link = (match.group(1) or match.group(2) or "").strip()
                if not raw_link or raw_link.startswith("#"):
                    continue
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw_link):
                    continue

                target = raw_link.split("#", 1)[0].split("?", 1)[0].strip()
                target = target.strip("<>")
                if not target:
                    continue

                resolved = (path.parent / unquote(target)).resolve()
                if target.endswith("/"):
                    candidates = [resolved / "index.md", resolved / "index.en.md"]
                elif resolved.suffix:
                    candidates = [resolved]
                    if resolved.suffix == ".md" and not resolved.name.endswith(".en.md"):
                        candidates.append(
                            resolved.with_name(resolved.stem + ".en" + resolved.suffix)
                        )
                else:
                    candidates = [
                        resolved,
                        resolved.with_suffix(".md"),
                        resolved.with_name(resolved.name + ".en.md"),
                    ]

                if not any(candidate.exists() for candidate in candidates):
                    link_issues.append(f"{rel_path}: {raw_link}")

        self.assertEqual([], content_issues)
        self.assertEqual([], link_issues)

    def test_track10_task26_batch34e_full_site_parity_red_gate(self):
        ru_pages = self._localized_markdown_pages()
        missing_siblings = [
            path.relative_to(DOCS).as_posix()
            for path in ru_pages
            if not self._en_sibling_for(path).exists()
        ]
        self.assertEqual([], missing_siblings)
        self.assertEqual(LOCALIZED_MARKDOWN_PAGE_COUNT, len(ru_pages))
        self.assertEqual(
            [],
            [
                self._en_sibling_for(path).relative_to(DOCS).as_posix()
                for path in self._english_original_markdown_pages()
                if self._en_sibling_for(path).exists()
            ],
        )

        cyrillic_en_pages = []
        for path in DOCS.rglob("*.en.md"):
            text = path.read_text(encoding="utf-8-sig")
            if re.search(r"[\u0400-\u04FF]", text):
                cyrillic_en_pages.append(path.relative_to(DOCS).as_posix())
        self.assertEqual([], cyrillic_en_pages)

        missing_rendered_en = []
        for path in ru_pages:
            rel = path.relative_to(DOCS).with_suffix(".html")
            rendered = SITE / "en" / rel
            if rel.name == "index.html":
                rendered = SITE / "en" / rel.parent / "index.html"
            if not rendered.exists():
                missing_rendered_en.append(rendered.relative_to(SITE).as_posix())
        self.assertEqual([], missing_rendered_en)

    def test_track10_task26_batch35_real_testing_execution_matrix_is_planned(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        batch35_packet = BATCH35_APPROVAL_DRAFT.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
        }

        registry_terms = [
            "Product-Agent OS Track 10 Task 26 Batch 35 approval-bound real testing execution matrix",
            "Product-Agent OS Batch 35 M37 approved local runtime launch evidence",
            "Product-Agent OS Batch 35 M38 actual browser automation smoke evidence",
            "Product-Agent OS Batch 35 M39 Codex session provider pilot evidence",
            "Product-Agent OS Batch 35 M40 canonical mutation pilot evidence",
            "Product-Agent OS Batch 35 M41 git release/PR preflight evidence",
            "T10-LIVE-M37..M41",
            "T10-LIVE-M37",
            "T10-LIVE-M38",
            "T10-LIVE-M39",
            "T10-LIVE-M40",
            "T10-LIVE-M41",
            "batch35_approval_bound_real_testing_execution",
            "approved_local_runtime_launch",
            "actual_browser_automation_smoke",
            "approved_provider_api_pilot",
            "approved_canonical_mutation_pilot",
            "explicit_git_release_pr_action",
            "live-server-run-evidence.json",
            "browser-automation-smoke.json",
            "provider-call-evidence.json",
            "provider-eval-report.json",
            "canonical-mutation-run.json",
            "graph-mutation-journal.jsonl",
            "rollback-proof.json",
            "git-release-pr-evidence.md",
            "owner_closed_no_op_git_release_pr",
            "Playwright Chromium",
            "codex_user_session",
            "desktop.png",
            "mobile.png",
            "verification_status:",
        ]
        for expected in registry_terms:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        backlog_terms = [
            "Task 26 Batch 35 Execution Matrix",
            "| `done_through_m37` | `T10-LIVE-M37` approved local runtime launch |",
            "| `done_through_m38` | `T10-LIVE-M38` actual browser automation smoke |",
            "| `done_through_m39` | `T10-LIVE-M39` Codex session provider pilot |",
            "| `done_through_m40` | `T10-LIVE-M40` canonical mutation pilot |",
            "| `owner_closed_no_op_git_release_pr` | `T10-LIVE-M41` git release/PR action |",
            "approved_local_runtime_launch",
            "actual_browser_automation_smoke",
            "approved_provider_api_pilot",
            "approved_canonical_mutation_pilot",
            "explicit_git_release_pr_action",
            "short-lived local server bound to `127.0.0.1`",
            "Playwright Chromium",
            "browser-automation-smoke.json",
            "desktop/mobile screenshots",
            "console_errors: 0",
            "network_failures: 0",
            "mobile_overflow: false",
            "generated-view labels",
            "source-boundary labels",
            "provider-call-evidence.json",
            "provider-eval-report.json",
            "codex_user_session",
            "OPENAI_API_KEY used: false",
            "direct API call from workspace shell: false",
            "canonical-mutation-run.json",
            "graph-mutation-journal.jsonl",
            "rollback-proof.json",
            "stage_root_only",
            "canonical_graph_source_mutated: false",
            "rollback_restores_previous_graph_digest: true",
            "git-release-pr-evidence.md",
            "missing_required_fields",
            "performs no canonical graph mutation",
            "performs no git stage/commit/push/PR",
        ]
        for expected in backlog_terms:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        docs_terms = [
            "Task 26 Batch 35",
            "T10-LIVE-M37..M41",
            "T10-LIVE-M37",
            "T10-LIVE-M38",
            "T10-LIVE-M39",
            "T10-LIVE-M40",
            "T10-LIVE-M41",
            "Approval-Bound Real Testing Execution Matrix",
            "done_through_m40",
            "approved_local_runtime_launch",
            "actual_browser_automation_smoke",
            "browser-automation-smoke.json",
            "Playwright Chromium",
            "server_shutdown_complete: true",
            "approved_provider_api_pilot",
            "provider-call-evidence.json",
            "provider-eval-report.json",
            "codex_user_session",
            "OPENAI_API_KEY used: false",
            "approved_canonical_mutation_pilot",
            "canonical-mutation-run.json",
            "graph-mutation-journal.jsonl",
            "rollback-proof.json",
            "stage_root_only",
            "owner_closed_no_op_git_release_pr",
            "explicit_git_release_pr_action",
            "batch35_approval_bound_real_testing_execution",
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
            "T10-LIVE-M37",
            "T10-LIVE-M38",
            "T10-LIVE-M39",
            "T10-LIVE-M40",
            "T10-LIVE-M41",
            "Approval-Bound Real Testing Execution Matrix",
            "batch35_approval_bound_real_testing_execution",
            "approved_local_runtime_launch",
            "done_through_m40",
            "actual_browser_automation_smoke",
            "browser-automation-smoke.json",
            "Playwright Chromium",
            "server_shutdown_complete: true",
            "approved_provider_api_pilot",
            "provider-call-evidence.json",
            "provider-eval-report.json",
            "codex_user_session",
            "OPENAI_API_KEY used: false",
            "approved_canonical_mutation_pilot",
            "canonical-mutation-run.json",
            "graph-mutation-journal.jsonl",
            "rollback-proof.json",
            "stage_root_only",
            "owner_closed_no_op_git_release_pr",
            "explicit_git_release_pr_action",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]
        for filename, text in control_plane.items():
            for expected in control_terms:
                with self.subTest(control_plane=filename, term=expected):
                    self.assertIn(expected, text)

        batch35_packet_terms = [
            "Source status: `internal`",
            "T10-LIVE-M37",
            "approved_local_runtime_launch",
            "T10-LIVE-M38",
            "actual_browser_automation_smoke",
            "T10-LIVE-M39",
            "approved_provider_api_pilot",
            "T10-LIVE-M40",
            "approved_canonical_mutation_pilot",
            "T10-LIVE-M41",
            "explicit_git_release_pr_action",
            "batch35_approval_bound_real_testing_execution",
            "live-server-run-evidence.json",
            "browser-automation-smoke.json",
            "provider-call-evidence.json",
            "provider-eval-report.json",
            "canonical-mutation-run.json",
            "graph-mutation-journal.jsonl",
            "rollback-proof.json",
            "git-release-pr-evidence.md",
            "status: `passed`",
            "blocked_pending_explicit_git_release_fields",
            "127.0.0.1",
            "health_check",
            "auth_rejection",
            "public_bind_rejection",
            "query_check",
            "write_endpoint_rejection",
            "server_shutdown_complete: true",
            "redaction.ok: true",
            "Playwright Chromium",
            "desktop.png",
            "mobile.png",
            "console_errors: 0",
            "network_failures: 0",
            "mobile_overflow: false",
            "generated-view labels",
            "source-boundary labels",
            "codex_user_session",
            "OPENAI_API_KEY used: false",
            "direct API call from workspace shell: false",
            "provider_secret_stored: false",
            "canonical_graph_source_mutated: false",
            "operation_count: 1",
            "journal_entry_count: 1",
            "rollback_restores_previous_graph_digest: true",
            "git_stage_commit_push_pr_performed: false",
            "missing_required_fields",
            "no canonical graph mutation",
            "no git stage/commit/push/PR",
        ]
        for expected in batch35_packet_terms:
            with self.subTest(batch35_packet=expected):
                self.assertIn(expected, batch35_packet)

    def test_track10_task25_batch20_local_backend_gate_is_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK10_BACKLOG.read_text(encoding="utf-8")
        documents = {
            "root_readme": ROOT_README.read_text(encoding="utf-8"),
            "plugin_readme": PLUGIN_README.read_text(encoding="utf-8"),
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
            "product_index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
        }
        control_plane = {
            "requirements": REQUIREMENTS.read_text(encoding="utf-8"),
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
        behavioral_evals = self._localized_contract_text(PRODUCT_AGENT_OS / "behavioral-evals.md")
        scenarios = self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md")
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
        behavioral_evals = self._localized_contract_text(PRODUCT_AGENT_OS / "behavioral-evals.md")
        scenarios = self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md")
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
        behavioral_evals = self._localized_contract_text(PRODUCT_AGENT_OS / "behavioral-evals.md")
        scenarios = self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md")
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
        behavioral_evals = self._localized_contract_text(PRODUCT_AGENT_OS / "behavioral-evals.md")
        scenarios = self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md")
        development_standards = self._localized_contract_text(PRODUCT_AGENT_OS / "development-standards.md")
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
        behavioral_evals = self._localized_contract_text(PRODUCT_AGENT_OS / "behavioral-evals.md")
        scenarios = self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md")
        methodology_intelligence = self._localized_contract_text(PRODUCT_AGENT_OS / "methodology-intelligence.md")
        development_standards = self._localized_contract_text(PRODUCT_AGENT_OS / "development-standards.md")
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
        behavioral_evals = self._localized_contract_text(PRODUCT_AGENT_OS / "behavioral-evals.md")
        scenarios = self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md")
        methodology_intelligence = self._localized_contract_text(PRODUCT_AGENT_OS / "methodology-intelligence.md")
        development_standards = self._localized_contract_text(PRODUCT_AGENT_OS / "development-standards.md")
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
            "active automation are not automatic actions",
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
        behavioral_evals = self._localized_contract_text(PRODUCT_AGENT_OS / "behavioral-evals.md")
        methodology_intelligence = self._localized_contract_text(PRODUCT_AGENT_OS / "methodology-intelligence.md")
        development_standards = self._localized_contract_text(PRODUCT_AGENT_OS / "development-standards.md")

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
            "Detection alone остается `present_unverified`",
            "grouped methodology recommendations",
            "approval-bound behavior",
        ]:
            with self.subTest(development_standards=expected):
                self.assertIn(expected, development_standards)

    def test_task22_final_docs_sync_user_facing_stack_is_closed(self):
        documents = {
            "index": self._localized_contract_text(PRODUCT_AGENT_OS / "index.md"),
            "architecture": self._localized_contract_text(PRODUCT_AGENT_OS / "architecture.md"),
            "technical": self._localized_contract_text(PRODUCT_AGENT_OS / "technical.md"),
            "methodology": self._localized_contract_text(PRODUCT_AGENT_OS / "methodology-intelligence.md"),
            "scenarios": self._localized_contract_text(PRODUCT_AGENT_OS / "scenarios.md"),
            "behavioral_evals": self._localized_contract_text(PRODUCT_AGENT_OS / "behavioral-evals.md"),
            "codex_compatibility": self._localized_contract_text(PRODUCT_AGENT_OS / "codex-compatibility.md"),
            "development_standards": self._localized_contract_text(PRODUCT_AGENT_OS / "development-standards.md"),
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
                "Fixture eval proves expected structure",
                "route safety",
                "transcript/session replay",
                "not deep semantic quality of a real product decision",
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
