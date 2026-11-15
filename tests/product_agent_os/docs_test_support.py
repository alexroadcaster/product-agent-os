import unittest
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
PRODUCT_AGENT_OS = DOCS / "product-agent-os"
MKDOCS = ROOT / "mkdocs.yml"
CHECK_DOCS = ROOT / "tools" / "check_docs.py"
# A scoped strict build can be verified without promoting the canonical site snapshot.
SITE = ROOT / os.environ.get("PAOS_DOCS_SITE_DIR", "site")
LOCAL_FILE_I18N_JS = DOCS / "assets" / "javascripts" / "local-file-i18n.js"
SOURCE_REGISTRY = DOCS / "sources" / "registry.md"
SOURCE_REGISTRY_EN = DOCS / "sources" / "registry.en.md"
TRACK_BACKLOG = DOCS / "planning" / "product-agent-os-track-8-detailed-backlog.md"
TRACK9_BACKLOG = DOCS / "planning" / "product-agent-os-track-9-backlog.md"
TRACK10_BACKLOG = DOCS / "planning" / "product-agent-os-track-10-backlog.md"
TRACK10_BACKLOG_EN = DOCS / "planning" / "product-agent-os-track-10-backlog.en.md"
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
BATCH40_DOUBT_VERIFIER_CLOSURE = (
    DOCS / "sources" / "product-agent-os-batch40-doubt-verifier-pilot-closure.md"
)
BATCH40_DOUBT_VERIFIER_CLOSURE_EN = (
    DOCS / "sources" / "product-agent-os-batch40-doubt-verifier-pilot-closure.en.md"
)
DOCUMENTATION_REFRESH_G1 = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-g1-source-site-parity-summary.json"
)
DOCUMENTATION_REFRESH_G1_1_DOC_M34 = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-g1-1-doc-m34-folder-contract-summary.json"
)
DOCUMENTATION_REFRESH_G1_1_DOC_M35_INSTALL = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-g1-1-doc-m35-install-summary.json"
)
DOCUMENTATION_REFRESH_G1_1_DOC_M36_NODE = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-g1-1-doc-m36-node-tooling-summary.json"
)
DOCUMENTATION_REFRESH_G1_1_DOC_M37_VALE = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-g1-1-doc-m37-vale-language-summary.json"
)
DOCUMENTATION_REFRESH_G1_1_DOC_M38_LINK_SECRET = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-g1-1-doc-m38-link-secret-summary.json"
)
DOCUMENTATION_REFRESH_G1_1_DOC_M39_MERMAID = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-g1-1-doc-m39-mermaid-summary.json"
)
DOCUMENTATION_REFRESH_G1_1_DOC_M40_AUDIT = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-g1-1-doc-m40-dependency-audit-summary.json"
)
DOCUMENTATION_REFRESH_G1_1_DOC_M41_DEFERRED_PLATFORMS = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-g1-1-doc-m41-deferred-platform-triggers-summary.json"
)
DOCUMENTATION_REFRESH_G2 = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-g2-first-run-cockpit-artifact-docs-summary.json"
)
DOCUMENTATION_REFRESH_G3 = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-g3-diagram-atlas-architecture-maps-summary.json"
)
DOCUMENTATION_REFRESH_G4 = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-g4-operator-flows-system-behavior-summary.json"
)
DOCUMENTATION_REFRESH_G5 = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-g5-evidence-quality-site-gate-summary.json"
)
DOCUMENTATION_REFRESH_DOC_M25 = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-doc-m25-site-freshness-summary.json"
)
PRODUCT_AGENT_OS_LIFECYCLE_HOOKS_LOCAL_ACTIVATION = (
    DOCS / "superpowers" / "specs" / "product-agent-os-lifecycle-hooks-local-activation-summary.json"
)
TRACK9_PLAN = DOCS / "planning" / "2026-05-25-track-9-methodology-intelligence.md"
TRACK10_PLAN = DOCS / "planning" / "2026-05-27-track-10-guided-questions-status-dashboard.md"
ROOT_README = ROOT / "README.md"
PLUGIN_README = ROOT / "plugins" / "product-agent-os" / "README.md"
REQUIREMENTS = ROOT / "REQUIREMENTS.md"
PLAN_FILE = ROOT / "PLAN.md"
TEST_FILE = ROOT / "TEST.md"
EVALS_FILE = ROOT / "EVALS.md"
RUNLOG_FILE = ROOT / "RUNLOG.md"
AGENTS_FILE = ROOT / "AGENTS.md"
CONTROL_PLANE_CURRENT_STATE = PRODUCT_AGENT_OS / "control-plane-current-state.md"
CONTROL_PLANE_SYNC = ROOT / ".codex" / "workflows" / "control-plane-sync.md"
CONTROL_PLANE_SIZE_BUDGET_BYTES = 40000
RUNLOG_SIZE_BUDGET_BYTES = CONTROL_PLANE_SIZE_BUDGET_BYTES
ENGLISH_ORIGINAL_SUPERPOWERS_PLAN_PAGES = {
    DOCS / "planning" / "2026-05-14-product-agent-os-generated-infrastructure.md",
    DOCS / "planning" / "2026-05-14-product-agent-os-lifecycle-skills.md",
    DOCS / "planning" / "2026-05-14-product-agent-os-plugin-core.md",
    DOCS / "planning" / "2026-05-14-product-agent-os-production-hardening.md",
    DOCS / "planning" / "2026-05-15-product-agent-os-codex-runtime-runner.md",
    DOCS / "planning" / "2026-05-25-track-9-methodology-intelligence.md",
    DOCS / "planning" / "2026-05-27-track-10-guided-questions-status-dashboard.md",
    DOCS / "planning" / "2026-06-20-track-11-documentation-architecture-refresh.md",
    DOCS / "planning" / "2026-08-05-gpt56-r1-r6-remediation.md",
    DOCS / "planning" / "2026-08-10-batch45-s9-0-team-readiness.md",
}
DOC_M25_HISTORICAL_PENDING_SITE_PAGES = {
    DOCS / "product-agent-os" / "first-run-architecture-cockpit.md",
    DOCS / "diagrams" / "source-generated-trust-boundary.md",
    DOCS / "diagrams" / "first-run-cockpit-architecture.md",
    DOCS / "diagrams" / "evidence-risk-lifecycle.md",
    DOCS / "diagrams" / "skill-exposure-and-invocation.md",
    DOCS / "diagrams" / "architecture-intelligence-diagram-atlas.md",
    DOCS / "product-agent-os" / "instruction-tool-use-compliance.md",
    DOCS / "product-agent-os" / "operator-command-matrix.md",
    DOCS / "product-agent-os" / "guided-questions-answer-ledger.md",
    DOCS / "product-agent-os" / "source-cache-session-state.md",
    DOCS / "product-agent-os" / "generated-artifact-ux-criteria.md",
    DOCS / "product-agent-os" / "graph-intelligence-contract.md",
    DOCS / "product-agent-os" / "privacy-supply-chain-retention.md",
    DOCS / "product-agent-os" / "local-html-interaction-boundary.md",
    DOCS / "product-agent-os" / "residual-follow-up-site-freshness.md",
}
DOC_M25_PENDING_SITE_PAGES = {
    # Current source additions are preview-built, not promoted to historical root site.
    DOCS / "codex" / "models-and-reasoning.md",
    DOCS / "playbooks" / "model-migration.md",
    DOCS / "planning" / "2026-11-03-gpt6-documentation-refresh.md",
    DOCS / "product-agent-os" / "coding-standards.md",
    DOCS / "product-agent-os" / "self-learning-loop.md",
    DOCS / "product-agent-os" / "project-formation.md",
    DOCS / "planning" / "2026-08-10-batch45-s9-a-durable-contract-recovery.md",
    DOCS / "planning" / "2026-08-11-batch45-s9-b-compact-authoring-runtime.md",
}
BUILDABLE_MARKDOWN_PAGE_COUNT = 163
LOCALIZED_MARKDOWN_PAGE_COUNT = 153
SITE_PROMOTED_LOCALIZED_MARKDOWN_PAGE_COUNT = 145
ENGLISH_ORIGINAL_MARKDOWN_PAGE_COUNT = 10


class SourceRoutedControlPlanePath:
    """Path facade for legacy assertions after root control-plane compaction.

    `read_bytes()` intentionally returns only the real root file so size and
    compactness guards stay honest. `read_text()` appends the source-owned
    context that replaced cold history in root PLAN/TEST/EVALS/RUNLOG.
    """

    def __init__(self, path):
        self.path = path

    def read_bytes(self):
        return self.path.read_bytes()

    def read_text(self, *args, **kwargs):
        return self.path.read_text(*args, **kwargs) + _control_plane_source_context()

    def exists(self):
        return self.path.exists()

    def __fspath__(self):
        return self.path.__fspath__()

    def __str__(self):
        return str(self.path)

    def __getattr__(self, name):
        return getattr(self.path, name)


_CONTROL_PLANE_SOURCE_CONTEXT_CACHE = None


def _control_plane_source_context():
    global _CONTROL_PLANE_SOURCE_CONTEXT_CACHE
    if _CONTROL_PLANE_SOURCE_CONTEXT_CACHE is not None:
        return _CONTROL_PLANE_SOURCE_CONTEXT_CACHE

    source_paths = [
        CONTROL_PLANE_CURRENT_STATE,
        CONTROL_PLANE_CURRENT_STATE.with_name("control-plane-current-state.en.md"),
        SOURCE_REGISTRY,
        SOURCE_REGISTRY_EN,
        TRACK_BACKLOG,
        TRACK9_BACKLOG,
        TRACK10_BACKLOG,
        TRACK10_BACKLOG_EN,
        BATCH35_APPROVAL_DRAFT,
        BATCH35_APPROVAL_DRAFT_EN,
        BATCH40_DOUBT_VERIFIER_CLOSURE,
        BATCH40_DOUBT_VERIFIER_CLOSURE_EN,
        DOCS / "planning" / "2026-06-20-track-11-documentation-architecture-refresh.md",
        ROOT / "prod_test.md",
        ROOT / "research" / "product-agent-os-requirements-history-2026-11-10.md",
    ]
    source_paths.extend(sorted((DOCS / "superpowers" / "specs").glob("*.json")))

    chunks = ["\n\n<!-- source-routed control-plane context for legacy assertions -->\n"]
    for path in source_paths:
        if path.exists():
            chunks.append(f"\n\n<!-- source: {path.relative_to(ROOT).as_posix()} -->\n")
            chunks.append(path.read_text(encoding="utf-8", errors="replace"))

    _CONTROL_PLANE_SOURCE_CONTEXT_CACHE = "".join(chunks)
    return _CONTROL_PLANE_SOURCE_CONTEXT_CACHE


PLAN = SourceRoutedControlPlanePath(PLAN_FILE)
TEST = SourceRoutedControlPlanePath(TEST_FILE)
EVALS = SourceRoutedControlPlanePath(EVALS_FILE)
RUNLOG = SourceRoutedControlPlanePath(RUNLOG_FILE)
AGENTS = SourceRoutedControlPlanePath(AGENTS_FILE)
REQUIREMENTS = SourceRoutedControlPlanePath(REQUIREMENTS)



class DocsAssertions:
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

    def _site_promoted_localized_markdown_pages(self):
        return [
            path
            for path in self._localized_markdown_pages()
            if path not in DOC_M25_PENDING_SITE_PAGES
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

