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
    DOCS / "product-agent-os" / "project-code-graph.md",
    DOCS / "product-agent-os" / "live-runtime-governance.md",
    DOCS / "product-agent-os" / "approval-bound-real-testing.md",
    DOCS / "product-agent-os" / "agent-skill-modernization-loop.md",
    DOCS / "product-agent-os" / "cli-reference.md",
    DOCS / "product-agent-os" / "artifact-contracts.md",
    DOCS / "product-agent-os" / "packaging-and-closure.md",
    DOCS / "product-agent-os" / "technical.md",
    DOCS / "product-agent-os" / "development-standards.md",
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
    "product-agent-os/project-code-graph.md",
    "product-agent-os/live-runtime-governance.md",
    "product-agent-os/approval-bound-real-testing.md",
    "product-agent-os/agent-skill-modernization-loop.md",
    "product-agent-os/cli-reference.md",
    "product-agent-os/artifact-contracts.md",
    "product-agent-os/packaging-and-closure.md",
]

MERMAID_EXTERNAL_ASSET = "https://unpkg.com/mermaid@10/dist/mermaid.min.js"
MERMAID_ACCEPTED_GAP = "Batch 34 accepted gap: Mermaid loads from CDN"


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

    if MERMAID_EXTERNAL_ASSET in config and MERMAID_ACCEPTED_GAP not in config:
        fail("mkdocs Mermaid external asset needs accepted gap or vendor/offline follow-up")


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
