from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

REQUIRED_PATHS = [
    ROOT / "AGENTS.md",
    ROOT / "README.md",
    ROOT / "mkdocs.yml",
    ROOT / "requirements.txt",
    DOCS / "index.md",
    DOCS / "sources" / "registry.md",
    DOCS / "sources" / "context7-research.md",
    DOCS / "sources" / "source-card-template.md",
    DOCS / "sources" / "product-agent-os-batch34a-public-docs-boundary.md",
    DOCS / "sources" / "product-agent-os-batch34b-public-copy-rewrite.md",
    DOCS / "sources" / "product-agent-os-batch34c-i18n-localization.md",
    DOCS / "sources" / "product-agent-os-batch34d-product-docs-qa-closure.md",
    DOCS / "sources" / "product-agent-os-batch34e-full-site-i18n-inventory.md",
    DOCS / "sources" / "product-agent-os-batch40-doubt-verifier-source-transfer.md",
    DOCS / "codex" / "overview.md",
    DOCS / "codex" / "surfaces.md",
    DOCS / "codex" / "configuration.md",
    DOCS / "codex" / "security.md",
    DOCS / "codex" / "workflows.md",
    DOCS / "codex" / "use-cases-deep-analysis.md",
    DOCS / "prompting" / "overview.md",
    DOCS / "prompting" / "question-design.md",
    DOCS / "prompting" / "context-engineering.md",
    DOCS / "prompting" / "anti-hallucination.md",
    DOCS / "product-agent" / "overview.md",
    DOCS / "product-agent" / "lifecycle.md",
    DOCS / "product-agent" / "roles.md",
    DOCS / "product-agent" / "control-plane.md",
    DOCS / "product-agent" / "product-agent-os-plugin-spec.md",
    DOCS / "product-agent-os" / "index.md",
    DOCS / "product-agent-os" / "artifact-gallery.md",
    DOCS / "product-agent-os" / "first-run-architecture-cockpit.md",
    DOCS / "product-agent-os" / "project-code-graph.md",
    DOCS / "product-agent-os" / "live-runtime-governance.md",
    DOCS / "product-agent-os" / "approval-bound-real-testing.md",
    DOCS / "product-agent-os" / "real-project-pilot.md",
    DOCS / "product-agent-os" / "agent-skill-modernization-loop.md",
    DOCS / "product-agent-os" / "instruction-tool-use-compliance.md",
    DOCS / "product-agent-os" / "operator-command-matrix.md",
    DOCS / "product-agent-os" / "guided-questions-answer-ledger.md",
    DOCS / "product-agent-os" / "source-cache-session-state.md",
    DOCS / "product-agent-os" / "generated-artifact-ux-criteria.md",
    DOCS / "product-agent-os" / "graph-intelligence-contract.md",
    DOCS / "product-agent-os" / "privacy-supply-chain-retention.md",
    DOCS / "product-agent-os" / "local-html-interaction-boundary.md",
    DOCS / "product-agent-os" / "residual-follow-up-site-freshness.md",
    DOCS / "product-agent-os" / "cli-reference.md",
    DOCS / "product-agent-os" / "artifact-contracts.md",
    DOCS / "product-agent-os" / "packaging-and-closure.md",
    DOCS / "product-agent-os" / "technical.md",
    DOCS / "product-agent-os" / "development-standards.md",
    DOCS / "product-agent-os" / "coding-standards.md",
    DOCS / "product-agent-os" / "methodology-intelligence.md",
    DOCS / "product-agent-os" / "scenarios.md",
    DOCS / "product-agent-os" / "behavioral-evals.md",
    DOCS / "product-agent-os" / "codex-compatibility.md",
    DOCS / "product-agent-os" / "architecture.md",
    DOCS / "runtime" / "overview.md",
    DOCS / "runtime" / "non-interactive-and-mcp.md",
    DOCS / "runtime" / "automations-github.md",
    DOCS / "runtime" / "worktrees-hooks-rules.md",
    DOCS / "agent-systems" / "overview.md",
    DOCS / "agent-systems" / "memory.md",
    DOCS / "agent-systems" / "session-control.md",
    DOCS / "agent-systems" / "subagents-skills.md",
    DOCS / "agent-systems" / "sdk-patterns.md",
    DOCS / "agent-systems" / "evals-observability.md",
    DOCS / "agent-systems" / "templates.md",
    DOCS / "playbooks" / "research-loop.md",
    DOCS / "playbooks" / "context7-deep-research.md",
    DOCS / "playbooks" / "grounded-answering.md",
    DOCS / "playbooks" / "doubt-verification-loop.md",
    DOCS / "playbooks" / "build-full-feature.md",
    DOCS / "playbooks" / "workflow-to-skill.md",
    DOCS / "playbooks" / "use-case-to-plugin.md",
    DOCS / "playbooks" / "eval-driven-improvement.md",
    DOCS / "playbooks" / "product-ready-pr.md",
    DOCS / "playbooks" / "maintain-agent-operating-docs.md",
    DOCS / "playbooks" / "workspace-readiness-audit.md",
    DOCS / "playbooks" / "docs-update.md",
    DOCS / "playbooks" / "code-review.md",
    DOCS / "playbooks" / "ai-team-design.md",
    DOCS / "artifact-templates" / "prompt-packet.md",
    DOCS / "artifact-templates" / "control-plane-files.md",
    DOCS / "artifact-templates" / "runlog.md",
    DOCS / "artifact-templates" / "product-skill.md",
    DOCS / "artifact-templates" / "plugin-blueprint.md",
    DOCS / "insights" / "index.md",
    DOCS / "insights" / "insight-card-template.md",
    DOCS / "insights" / "seed-insights.md",
    DOCS / "diagrams" / "index.md",
    DOCS / "diagrams" / "architecture.md",
    DOCS / "diagrams" / "source-generated-trust-boundary.md",
    DOCS / "diagrams" / "first-run-cockpit-architecture.md",
    DOCS / "diagrams" / "evidence-risk-lifecycle.md",
    DOCS / "diagrams" / "skill-exposure-and-invocation.md",
    DOCS / "diagrams" / "architecture-intelligence-diagram-atlas.md",
    DOCS / "diagrams" / "product-delivery-lifecycle.md",
    DOCS / "diagrams" / "agent-team-and-skills.md",
    DOCS / "diagrams" / "runtime-decision-map.md",
    DOCS / "diagrams" / "skill-lifecycle.md",
    DOCS / "diagrams" / "context-memory-verification.md",
]

SOURCE_FIELDS = [
    "title:",
    "url:",
    "type:",
    "status:",
    "checked_at:",
    "summary:",
    "relevance:",
    "trust_level:",
]

INSIGHT_FIELDS = [
    "claim:",
    "source:",
    "evidence:",
    "works_for:",
    "risks:",
    "verification_status:",
]

BAD_PLACEHOLDERS = ["TBD", "TODO", "fill in", "implement later"]
LINK_RE = re.compile(r"\]\((?!https?://|mailto:|#)([^)]+)\)")

REQUIRED_NAV_PATHS = [
    "product-agent/product-agent-os-plugin-spec.md",
    "product-agent-os/artifact-gallery.md",
    "product-agent-os/first-run-architecture-cockpit.md",
    "diagrams/source-generated-trust-boundary.md",
    "diagrams/first-run-cockpit-architecture.md",
    "diagrams/evidence-risk-lifecycle.md",
    "diagrams/skill-exposure-and-invocation.md",
    "diagrams/architecture-intelligence-diagram-atlas.md",
    "product-agent-os/project-code-graph.md",
    "product-agent-os/live-runtime-governance.md",
    "product-agent-os/approval-bound-real-testing.md",
    "product-agent-os/real-project-pilot.md",
    "product-agent-os/agent-skill-modernization-loop.md",
    "product-agent-os/instruction-tool-use-compliance.md",
    "product-agent-os/operator-command-matrix.md",
    "product-agent-os/guided-questions-answer-ledger.md",
    "product-agent-os/source-cache-session-state.md",
    "product-agent-os/generated-artifact-ux-criteria.md",
    "product-agent-os/graph-intelligence-contract.md",
    "product-agent-os/privacy-supply-chain-retention.md",
    "product-agent-os/local-html-interaction-boundary.md",
    "product-agent-os/residual-follow-up-site-freshness.md",
    "playbooks/doubt-verification-loop.md",
    "sources/product-agent-os-batch40-doubt-verifier-source-transfer.md",
    "product-agent-os/cli-reference.md",
    "product-agent-os/artifact-contracts.md",
    "product-agent-os/packaging-and-closure.md",
    "product-agent-os/coding-standards.md",
]

MERMAID_EXTERNAL_ASSET = "https://unpkg.com/mermaid@10/dist/mermaid.min.js"
MERMAID_LOCAL_ASSET = "assets/javascripts/vendor/mermaid-10.9.6.min.js"
MERMAID_VENDOR_EVIDENCE = "documentation_refresh_G1_1-DOC-M39-MERMAID-A01"
DOC_M40_AUDIT_EVIDENCE = "documentation_refresh_G1_1-DOC-M40-AUDIT-SBOM-A01"
DOC_M40_AUDIT_HELPER = ROOT / "tools" / "docs_dependency_audit.ps1"
DOC_M25_I18N_REPAIR_HELPER = ROOT / "tools" / "fix_site_i18n_links.ps1"
DOC_M40_AUDIT_PACKET = (
    DOCS / "superpowers" / "specs" / "documentation-refresh-g1-1-doc-m40-dependency-audit-summary.json"
)
DOC_M41_DEFERRED_PLATFORM_EVIDENCE = "documentation_refresh_G1_1-DOC-M41-DEFERRED-PLATFORMS-A01"
DOC_M41_DEFERRED_PLATFORM_PACKET = (
    DOCS
    / "superpowers"
    / "specs"
    / "documentation-refresh-g1-1-doc-m41-deferred-platform-triggers-summary.json"
)
DOCUMENTATION_REFRESH_G3_EVIDENCE = "documentation_refresh_G3-A01"
DOCUMENTATION_REFRESH_G3_PACKET = (
    DOCS
    / "superpowers"
    / "specs"
    / "documentation-refresh-g3-diagram-atlas-architecture-maps-summary.json"
)
DOCUMENTATION_REFRESH_G4_EVIDENCE = "documentation_refresh_G4-A01"
DOCUMENTATION_REFRESH_G4_PACKET = (
    DOCS
    / "superpowers"
    / "specs"
    / "documentation-refresh-g4-operator-flows-system-behavior-summary.json"
)
DOCUMENTATION_REFRESH_G5_EVIDENCE = "documentation_refresh_G5-A01"
DOCUMENTATION_REFRESH_G5_PACKET = (
    DOCS
    / "superpowers"
    / "specs"
    / "documentation-refresh-g5-evidence-quality-site-gate-summary.json"
)
DOCUMENTATION_REFRESH_DOC_M25_EVIDENCE = "documentation_refresh_DOC-M25-A01"
DOCUMENTATION_REFRESH_DOC_M25_PACKET = (
    DOCS
    / "superpowers"
    / "specs"
    / "documentation-refresh-doc-m25-site-freshness-summary.json"
)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required_paths() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_PATHS if not path.exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))


def check_templates() -> None:
    registry = read(DOCS / "sources" / "registry.md")
    for field in SOURCE_FIELDS:
        if field not in registry:
            fail(f"source registry missing field {field}")

    insight_template = read(DOCS / "insights" / "insight-card-template.md")
    for field in INSIGHT_FIELDS:
        if field not in insight_template:
            fail(f"insight template missing field {field}")


def check_mermaid() -> None:
    count = sum(read(path).count("```mermaid") for path in DOCS.rglob("*.md"))
    if count < 2:
        fail("expected at least two Mermaid diagrams")


def check_mkdocs_nav() -> None:
    config = read(ROOT / "mkdocs.yml")
    missing = [path for path in REQUIRED_NAV_PATHS if path not in config]
    if missing:
        fail("mkdocs nav missing required paths: " + ", ".join(missing))

    if MERMAID_EXTERNAL_ASSET in config:
        fail("mkdocs Mermaid external CDN asset is no longer allowed after DOC-M39")

    if MERMAID_LOCAL_ASSET not in config:
        fail("mkdocs Mermaid local vendor asset missing from extra_javascript")

    registry = read(DOCS / "sources" / "registry.md")
    if MERMAID_VENDOR_EVIDENCE not in registry:
        fail("source registry missing DOC-M39 Mermaid vendor evidence")

    if DOC_M40_AUDIT_EVIDENCE not in registry:
        fail("source registry missing DOC-M40 dependency audit evidence")

    if not DOC_M40_AUDIT_HELPER.exists():
        fail("DOC-M40 dependency audit helper is missing")

    if not DOC_M25_I18N_REPAIR_HELPER.exists():
        fail("DOC-M25 local file i18n repair helper is missing")

    if not DOC_M40_AUDIT_PACKET.exists():
        fail("DOC-M40 dependency audit evidence packet is missing")

    if DOC_M41_DEFERRED_PLATFORM_EVIDENCE not in registry:
        fail("source registry missing DOC-M41 deferred platform trigger evidence")

    if not DOC_M41_DEFERRED_PLATFORM_PACKET.exists():
        fail("DOC-M41 deferred platform trigger evidence packet is missing")

    if DOCUMENTATION_REFRESH_G3_EVIDENCE not in registry:
        fail("source registry missing Track 11 G3 diagram atlas evidence")

    if not DOCUMENTATION_REFRESH_G3_PACKET.exists():
        fail("Track 11 G3 diagram atlas evidence packet is missing")

    if DOCUMENTATION_REFRESH_G4_EVIDENCE not in registry:
        fail("source registry missing Track 11 G4 operator-flow evidence")

    if not DOCUMENTATION_REFRESH_G4_PACKET.exists():
        fail("Track 11 G4 operator-flow evidence packet is missing")

    if DOCUMENTATION_REFRESH_G5_EVIDENCE not in registry:
        fail("source registry missing Track 11 G5 evidence quality evidence")

    if not DOCUMENTATION_REFRESH_G5_PACKET.exists():
        fail("Track 11 G5 evidence quality evidence packet is missing")

    if DOCUMENTATION_REFRESH_DOC_M25_EVIDENCE not in registry:
        fail("source registry missing Track 11 DOC-M25 site freshness evidence")

    if not DOCUMENTATION_REFRESH_DOC_M25_PACKET.exists():
        fail("Track 11 DOC-M25 site freshness evidence packet is missing")


def check_placeholders() -> None:
    for path in DOCS.rglob("*.md"):
        text = read(path)
        for placeholder in BAD_PLACEHOLDERS:
            if placeholder in text:
                fail(f"{path.relative_to(ROOT)} contains placeholder {placeholder}")


def check_internal_links() -> None:
    for path in DOCS.rglob("*.md"):
        text = read(path)
        for match in LINK_RE.finditer(text):
            target = match.group(1).split("#", 1)[0]
            if not target or target.startswith("<"):
                continue
            if target.startswith("../") or target.endswith(".md") or "/" in target:
                candidate = (path.parent / target).resolve()
                try:
                    candidate.relative_to(ROOT)
                except ValueError:
                    fail(f"{path.relative_to(ROOT)} links outside project: {target}")
                if not candidate.exists():
                    fail(f"{path.relative_to(ROOT)} has broken internal link: {target}")


def check_source_status() -> None:
    for path in DOCS.rglob("*.md"):
        if path.relative_to(DOCS).as_posix().startswith("artifact-templates/"):
            continue
        text = read(path)
        if "Source status:" not in text and path.relative_to(DOCS).as_posix() not in {
            "index.md",
            "sources/registry.md",
        }:
            fail(f"{path.relative_to(ROOT)} missing Source status marker")


def main() -> None:
    check_required_paths()
    check_templates()
    check_mermaid()
    check_mkdocs_nav()
    check_placeholders()
    check_internal_links()
    check_source_status()
    print("OK: documentation structure checks passed")


if __name__ == "__main__":
    main()
