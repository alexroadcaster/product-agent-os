"""Read-only methodology audit for Product-Agent OS Track 9."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from product_agent_os.contracts import CONTROL_PLANE_FILES
from product_agent_os.methodology_catalog import load_methodology_catalog


PRIORITY_ORDER = {
    "P0_blocker": 0,
    "P1_high_risk": 1,
    "P2_recommended": 2,
    "P3_optional_maturity": 3,
    "not_applicable": 4,
}

STACK_MARKERS = {
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
}

OPENAPI_MARKERS = {"openapi.yaml", "openapi.yml", "openapi.json"}
ASYNCAPI_MARKERS = {"asyncapi.yaml", "asyncapi.yml", "asyncapi.json"}
DOC_CONTROL_FILES = {"readme.md", "agents.md", "requirements.md", "plan.md", "test.md", "evals.md", "runlog.md"}
DEPLOY_MARKERS = {"dockerfile", "docker-compose.yml", "serverless.yml"}
RELEASE_FILE_MARKERS = {"changelog.md", "changes.md", "release.md", "release-notes.md"}

BUSINESS_INTENT_TERMS = {
    "analytics",
    "behavior",
    "dashboard",
    "experiment",
    "metric",
    "mvp",
    "product",
    "release",
    "success",
    "telemetry",
    "usage",
    "user",
    "value",
}
BEHAVIOR_INTENT_TERMS = {"behavior", "feature", "change", "ship", "release", "user"}
UI_INTENT_TERMS = {"frontend", "ui", "ux", "component", "screen", "page"}
FRONTEND_INTENT_TERMS = UI_INTENT_TERMS | {
    "a11y",
    "accessibility",
    "browser",
    "console",
    "design-system",
    "design system",
    "fsd",
    "frontend",
    "interaction",
    "keyboard",
    "layout",
    "playwright",
    "responsive",
    "route",
    "storybook",
    "visual",
    "wcag",
}
BACKEND_INTENT_TERMS = {
    "api",
    "backend",
    "circuit breaker",
    "consumer",
    "health check",
    "idempotency",
    "liveness",
    "microservice",
    "microservices",
    "queue",
    "readiness",
    "retry",
    "runbook",
    "scheduler",
    "server",
    "service",
    "slo",
    "worker",
}
BACKEND_NOT_APPLICABLE_PHRASES = {
    "cli-only",
    "dependency metadata without backend runtime behavior",
    "docs-only",
    "frontend-only",
    "native-only",
    "package-name-only service folder without runtime evidence",
}
BACKEND_RUNTIME_TERMS = {
    "background job",
    "backpressure",
    "consumer",
    "deduplication",
    "distributed workflow",
    "failure mode",
    "idempotency",
    "job",
    "ordering",
    "queue",
    "replay",
    "retry",
    "scheduler",
    "timeout",
    "worker",
}
BACKEND_DEPENDENCY_TERMS = {
    "cache",
    "dependency",
    "external adapter",
    "external provider",
    "message broker",
    "payment",
    "remote dependency",
    "search",
    "storage",
    "third-party",
}
BACKEND_OBSERVABILITY_TERMS = {
    "alert",
    "correlation",
    "dashboard",
    "log",
    "logs",
    "metric",
    "metrics",
    "observability",
    "redaction",
    "trace",
    "traces",
}
BACKEND_HEALTH_TERMS = {"health", "health check", "liveness", "readiness", "startup"}
BACKEND_DATA_CONSISTENCY_TERMS = {
    "compensation",
    "consistency",
    "data recovery",
    "distributed transaction",
    "migration",
    "outbox",
    "saga",
    "transaction",
}
BACKEND_CONFIG_SECRET_TERMS = {"config", "env", "environment", "secret", "secrets", "token"}
BACKEND_SECURITY_TERMS = {"auth", "authorization", "external write", "money", "payment", "pii", "privileged", "secret"}
BACKEND_ROLLBACK_TERMS = {"feature flag", "irreversible", "migration", "recovery", "replay", "rollback"}
BACKEND_CONTRACT_TERMS = {"api", "asyncapi", "contract", "event", "openapi", "pact", "protobuf", "provider"}
UNSUPPORTED_BACKEND_CLAIMS = {
    "backend means only business logic files",
    "health endpoint exists, so readiness is solved",
    "logs are observability",
    "microservices are the professional default",
    "retries make systems reliable",
    "slos are only for large companies",
}
API_INTENT_TERMS = {"api", "webhook", "integration", "external", "graphql", "grpc", "protobuf"}
AI_INTENT_TERMS = {"prompt", "model", "eval", "rag", "vector", "embedding", "ai", "llm"}
DELIVERY_INTENT_TERMS = {"production", "release", "deploy", "package", "docker", "kubernetes", "operations"}
ARCHITECTURE_INTENT_TERMS = {
    "adr",
    "architecture",
    "boundary",
    "c4",
    "container",
    "deployment",
    "diagram",
    "multi-service",
    "observability",
    "runtime",
    "service split",
    "topology",
}
BUSINESS_NOT_APPLICABLE_PHRASES = {
    "typo-only",
    "formatting-only",
    "dependency pin without behavior impact",
    "without behavior impact",
}
REQUIREMENTS_NOT_APPLICABLE_PHRASES = {
    "typo-only",
    "formatting-only",
    "dependency metadata without behavior impact",
    "dependency pin without behavior impact",
    "without behavior impact",
}
SOLUTION_ARCHITECTURE_NOT_APPLICABLE_PHRASES = {
    "typo-only",
    "formatting-only",
    "docs-light prototype without reviewed/diffable diagrams",
    "non-cloud work without well-architected review",
    "dependency metadata without behavior impact",
    "dependency pin without behavior impact",
}
IMPLEMENTATION_OR_RELEASE_TERMS = {"implement", "implementation", "ship", "release", "build", "deliver"}
PRODUCT_ANALYTICS_TERMS = {"analytics", "usage", "event", "events", "dashboard", "telemetry", "tracking"}
PRODUCT_SUCCESS_TERMS = {"success", "north star", "value metric", "product value"}
WORKFLOW_PROMOTION_TERMS = {"workflow promotion", "promote workflow", "automation", "skill promotion", "playbook"}
REQUIREMENTS_INTENT_TERMS = {
    "acceptance",
    "behavior",
    "business rule",
    "change",
    "constraint",
    "domain",
    "feature",
    "requirement",
    "scenario",
    "story",
    "user",
    "workflow",
}
REQUIREMENT_ID_TERMS = {
    "multi-slice",
    "regulatory",
    "regulated",
    "risky",
    "long-lived",
    "public contract",
    "public api",
}
CONSTRAINT_TERMS = {
    "accessibility",
    "compliance",
    "cost",
    "localization",
    "operational",
    "performance",
    "platform",
    "privacy",
    "retention",
    "rollback",
    "rollout",
    "security",
}
UNCLEAR_STORY_TERMS = {"unclear", "large", "disputed", "ambiguous"}
STORY_SLICE_TERMS = {"story", "mvp", "deferred", "slice", "slices", "non-goal", "non-goals"}
STAKEHOLDER_OWNER_TERMS = {"stakeholder", "owner", "domain expert", "process", "value ambiguity"}
DOMAIN_DISCOVERY_TERMS = {"cross-silo", "eventstorming", "domain storytelling", "overloaded language"}
DOMAIN_EVENT_TERMS = {"domain event", "event across boundary", "event-driven", "producer", "consumer"}
STATE_TRANSITION_TERMS = {"state transition", "invariant", "invalid transition", "failure mode"}
API_UI_DATA_TRACE_TERMS = {"api", "ui", "data", "schema", "database", "contract", "event"}
CHANGE_IMPACT_TERMS = {"changed after planning", "change impact", "requirement changed", "domain rule changes"}
DECLARATIVE_SCENARIO_LEAK_TERMS = {
    "css selector",
    "database table",
    "db table",
    "function name",
    "test harness",
    "ui selector",
}
DOMAIN_REVIEW_TERMS = {
    "ai generated",
    "ai-generated",
    "business-critical",
    "compliance",
    "finance",
    "legal",
}
UNSUPPORTED_REQUIREMENTS_CLAIMS = {
    "bdd replaces testing",
    "gherkin is mandatory",
    "user story template is complete requirement",
    "a user story template is a complete requirement",
    "glossary is ubiquitous language",
    "a glossary is ubiquitous language",
    "openapi is requirements source of truth",
    "openapi is the requirements source of truth",
}
UNSUPPORTED_ARCHITECTURE_CLAIMS = {
    "architecture means diagrams",
    "rendered diagram proves correctness",
    "c4 code diagrams are always required",
    "adr is bureaucracy",
    "well-architected review proves architecture quality",
    "architecture-as-code is always required",
    "ai can design architecture from chat alone",
}
QUALITY_NOT_APPLICABLE_PHRASES = {
    "typo-only docs edit",
    "formatting-only markdown cleanup",
    "formatting-only edit",
    "docs-only source cleanup",
    "dependency metadata without behavior impact",
    "pure dependency metadata without behavior impact",
}
QUALITY_INTENT_TERMS = {
    "test",
    "tests",
    "eval",
    "evals",
    "quality",
    "verification",
    "runtime",
    "manual qa",
    "visual",
    "accessibility",
    "ci",
    "coverage",
    "flaky",
    "retry",
    "regression",
    "bugfix",
    "bug fix",
    "completion",
    "ready",
}
QUALITY_RISK_TERMS = {"risky", "broad", "constrained", "high-risk", "high risk"}
DETERMINISTIC_CHANGE_TERMS = {"deterministic", "business rule", "bugfix", "bug fix"}
RUNTIME_EVIDENCE_TERMS = {"runtime", "run behavior", "runtime behavior", "works claim"}
MANUAL_QA_TERMS = {"manual qa", "manual test", "exploratory testing"}
VISUAL_A11Y_TERMS = {"ui", "visual", "accessibility", "a11y", "keyboard", "focus", "responsive"}
QUALITY_EVAL_TERMS = {"ai", "rag", "docs", "ux", "search", "subjective", "eval", "evals", "baseline", "rerun"}
CI_QUALITY_TERMS = {"ci", "github actions", "shared branch", "release", "pull request", "pr"}
FLAKY_TEST_TERMS = {"flaky", "retry", "retries", "quarantine", "intermittent"}
COVERAGE_POLICY_TERMS = {"coverage", "line coverage", "branch coverage", "codecov"}
TEST_DATA_PRIVACY_TERMS = {
    "test data privacy",
    "fixture privacy",
    "fixtures privacy",
    "eval dataset",
    "logs privacy",
    "trace privacy",
    "screenshot privacy",
    "private data",
    "secrets in tests",
}
REGRESSION_IMPACT_TERMS = {"regression impact", "refactor", "migration", "dependency update", "shared-code"}
COMPLETION_CLAIM_TERMS = {"completion", "ready", "readiness", "release", "quality claim", "works claim", "done"}
UNSUPPORTED_QUALITY_CLAIMS = {
    "more tests always means better quality",
    "coverage proves correctness",
    "line coverage proves correctness",
    "100 percent line coverage proves correctness",
    "100% line coverage proves correctness",
    "e2e tests should dominate because they are most realistic",
    "manual qa is not evidence",
    "ai evals are optional for ai behavior changes",
}
CODEX_AGENTIC_NOT_APPLICABLE_PHRASES = {
    "typo-only docs edit without codex workflow change",
    "single local deterministic command without agent delegation",
    "read-only research without staged artifacts or external writes",
}
FRONTEND_NOT_APPLICABLE_PHRASES = {
    "backend-only",
    "cli-only",
    "data-only",
    "dependency metadata without ui behavior impact",
    "docs-only",
    "native-only",
    "simple crud without non-trivial frontend state",
}
FRONTEND_REUSABLE_TERMS = {"component", "reusable", "design-system", "design system", "primitive", "storybook"}
FRONTEND_DESIGN_SYSTEM_TERMS = {"design-system", "design system", "token", "variant", "icon", "typography", "theme"}
FRONTEND_DATA_TERMS = {"api", "contract", "data", "cache", "permission", "auth", "pagination", "stale"}
FRONTEND_ACCESSIBILITY_TERMS = {"accessibility", "a11y", "keyboard", "focus", "wcag", "form", "public"}
FRONTEND_VISUAL_TERMS = {"visual", "layout", "screenshot", "responsive", "viewport", "theme", "dark"}
FRONTEND_PERFORMANCE_TERMS = {"performance", "web vitals", "lcp", "inp", "cls"}
FRONTEND_BROWSER_TERMS = {"browser", "device", "webview", "chrome", "firefox", "safari"}
FRONTEND_I18N_TERMS = {"i18n", "localization", "long text", "rtl", "pluralization", "user-generated"}
FRONTEND_STATE_TERMS = {"state", "loading", "empty", "error", "disabled", "success", "skeleton", "offline"}
UNSUPPORTED_FRONTEND_CLAIMS = {
    "fsd should be mandatory for every frontend project",
    "storybook proves ui quality",
    "storybook proves ui quality by itself",
    "automated a11y addon output is enough",
    "automated accessibility addon output is enough",
    "a desktop screenshot proves responsive ui",
    "desktop screenshot proves responsive ui",
    "lab web vitals always represent production ux",
    "code inspection proves ui completion",
}
CODEX_AGENTIC_INTENT_TERMS = {
    "agent",
    "agentic",
    "agents sdk",
    "automation",
    "codex",
    "codex app",
    "codex exec",
    "cli",
    "external write",
    "handoff",
    "hook",
    "ide extension",
    "mcp",
    "memory",
    "plugin",
    "skill",
    "subagent",
    "task packet",
    "tool call",
    "worktree",
}
CODEX_AGENTIC_HIGH_RISK_TERMS = {
    "automation schedule",
    "blocking hook",
    "external write",
    "production data",
    "remote mcp",
    "side-effecting tool",
    "secrets",
    "overlap",
}
UNSUPPORTED_AGENTIC_CLAIMS = {
    "memory is source of truth",
    "memory is project source of truth",
    "subagents are automatically faster",
    "mcp tools are safe because they are tools",
    "hooks are harmless convenience scripts",
    "repeated workflow should become automation immediately",
    "agents sdk and codex runtime are the same layer",
    "inspection proves completion",
}
PUBLIC_CONTRACT_TERMS = {"public api", "public contract", "event contract", "generated client", "sdk"}
DATA_BOUNDARY_TERMS = {"persistent data", "pii", "retention", "migration", "database", "data ownership"}
TRUST_BOUNDARY_TERMS = {"trust boundary", "auth", "authorization", "security boundary", "pii", "payment"}
HIGH_IMPACT_ARCHITECTURE_TERMS = {
    "adr",
    "decision",
    "hard to reverse",
    "irreversible",
    "service split",
    "multi-service",
    "tradeoff",
}
RUNTIME_ARCHITECTURE_TERMS = {"runtime", "topology", "deployment", "service", "worker", "queue"}
OBSERVABILITY_TERMS = {"observability", "trace", "tracing", "metrics", "logs", "dashboard", "alert"}
MIGRATION_ROLLBACK_TERMS = {"migration", "rollback", "service split", "split"}
FITNESS_FUNCTION_TERMS = {"boundary drift", "dependency rule", "fitness function", "parallel agent", "parallel"}
ARCHITECTURE_DIAGRAM_SUFFIXES = (".mmd", ".puml", ".plantuml", ".dsl")
HIGH_RISK_INTENT_TERMS = {
    "security",
    "privacy",
    "payment",
    "pii",
    "compliance",
    "healthcare",
    "finance",
    "production data",
    "auth",
    "authorization",
    "secret",
}
REGULATED_INTENT_TERMS = {"regulated", "compliance", "audit", "hipaa", "pci", "soc2", "finance", "healthcare", "minors"}


def build_methodology_audit(workspace: Path, intent_hint: str = "") -> dict[str, Any]:
    """Build a read-only methodology audit packet for a workspace."""

    root = Path(workspace)
    files, directories = _relative_inventory(root)
    lowered_files = {path.lower() for path in files}
    lowered_dirs = {path.lower() for path in directories}
    intent = intent_hint.lower()
    observed = _observed_signals(root, lowered_files, lowered_dirs)
    intent_signals = _intent_signals(intent)
    maturity_level = _classify_maturity(lowered_files, lowered_dirs, observed, intent)
    complexity_profile = _classify_complexity(lowered_files, lowered_dirs, observed, intent)
    methodology_domains = _methodology_domains(
        observed,
        intent,
        maturity_level["selected"],
        complexity_profile["selected"],
        bool(files),
    )
    recommendations = _prioritize_recommendations(
        _recommendations(root, lowered_files, lowered_dirs, observed, intent, complexity_profile["selected"])
    )

    return {
        "status": "ok",
        "write_policy": "read_only",
        "maturity_level": maturity_level,
        "complexity_profile": complexity_profile,
        "observed_signals": observed,
        "intent_signals": intent_signals,
        "unknowns": _unknowns(lowered_files, lowered_dirs, observed),
        "questions_for_owner": _questions_for_owner(lowered_files, lowered_dirs, observed, recommendations),
        "provisional_assumptions": _provisional_assumptions(files, intent),
        "delivery_map": _delivery_map(lowered_files, lowered_dirs, observed, methodology_domains, recommendations),
        "methodology_domains": methodology_domains,
        "recommendations": recommendations,
        "safe_next_action": _safe_next_action(recommendations),
    }


def _relative_inventory(root: Path) -> tuple[set[str], set[str]]:
    files: set[str] = set()
    directories: set[str] = set()
    if not root.exists() or not root.is_dir():
        return files, directories
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in {".git", "node_modules", "__pycache__"}]
        current_path = Path(current_root)
        for dirname in dirnames:
            try:
                directories.add((current_path / dirname).relative_to(root).as_posix())
            except ValueError:
                continue
        for filename in filenames:
            try:
                files.add((current_path / filename).relative_to(root).as_posix())
            except ValueError:
                continue
    return files, directories


def _observed_signals(root: Path, files: set[str], directories: set[str]) -> list[dict[str, Any]]:
    signals: list[dict[str, Any]] = []

    def add(signal_id: str, evidence: list[str]) -> None:
        if evidence:
            signals.append({"id": signal_id, "source": "workspace", "evidence": sorted(evidence)})

    add("stack_manifest", [path for path in files if path in STACK_MARKERS])
    add("openapi_contract", [path for path in files if _is_openapi(path)])
    add("asyncapi_contract", [path for path in files if _is_asyncapi(path)])
    add("graphql_schema", [path for path in files if path.endswith("schema.graphql")])
    add("protobuf_schema", [path for path in files if path.endswith(".proto")])
    add(
        "database_migration_or_schema",
        [path for path in files if path in {"alembic.ini", "dbt_project.yml"}]
        + [directory for directory in directories if directory in {"migrations", "prisma"}],
    )
    add(
        "ci_configuration",
        [path for path in files if path.startswith(".github/workflows/") or path in {".gitlab-ci.yml", "azure-pipelines.yml"}],
    )
    add(
        "deployment_configuration",
        [path for path in files if path in DEPLOY_MARKERS] + [directory for directory in directories if directory == "k8s"],
    )
    add("release_file", [path for path in files if path in RELEASE_FILE_MARKERS or path.startswith(".changeset/")])
    add("docs_or_control_plane", [path for path in files if path in DOC_CONTROL_FILES] + ["docs" for item in directories if item == "docs"])
    add("codex_agentic_workflow", _codex_agentic_signal_evidence(files, directories))
    add("frontend", _frontend_signal_evidence(files, directories))
    add("backend", _backend_signal_evidence(files, directories))
    add(
        "ai_eval_or_rag",
        [
            path
            for path in files
            if path.startswith(("evals/", "prompts/", "rag/"))
            or "vector" in path
            or "embeddings" in path
        ]
        + [directory for directory in directories if directory in {"evals", "prompts", "rag", "vector", "embeddings"}],
    )
    add("test_evidence", [path for path in files if "test" in path or path.startswith("evals/")])
    add("quality_testing_signal", _quality_signal_evidence(files, directories))
    add(
        "architecture_docs",
        [
            path
            for path in files
            if _artifact_present({path}, "architecture-overview.md")
            or _artifact_present({path}, "adr.md")
            or path.startswith(("docs/architecture/", "architecture/", "docs/adr/", "adr/", "docs/diagrams/"))
            or path.endswith(ARCHITECTURE_DIAGRAM_SUFFIXES)
        ],
    )
    if _has_package_test_script(root):
        add("test_command", ["package.json"])
    return signals


def _frontend_signal_evidence(files: set[str], directories: set[str]) -> list[str]:
    native_markers = ("android/", "ios/", "app.json", "app.config.js", "app.config.ts")
    if any(path.startswith(native_markers) for path in files):
        return []
    directory_prefixes = (
        ".storybook/",
        "app/",
        "components/",
        "e2e/",
        "entities/",
        "features/",
        "pages/",
        "routes/",
        "shared/ui/",
        "stories/",
        "tests/playwright/",
        "widgets/",
        "src/app/",
        "src/components/",
        "src/entities/",
        "src/features/",
        "src/pages/",
        "src/routes/",
        "src/shared/ui/",
        "src/widgets/",
    )
    exact_files = {
        "components.json",
        "vite.config.js",
        "vite.config.ts",
        "next.config.js",
        "next.config.ts",
        "nuxt.config.js",
        "nuxt.config.ts",
        "svelte.config.js",
        "svelte.config.ts",
        "astro.config.mjs",
        "astro.config.ts",
        "playwright.config.js",
        "playwright.config.ts",
        "tailwind.config.js",
        "tailwind.config.ts",
    }
    fragments = (
        ".stories.",
        ".story.",
        "storybook",
        "playwright",
        "testing-library",
        "axe",
        "chromatic",
        "tokens",
        "theme",
        "viewport",
        "accessibility",
        "wcag",
        "keyboard",
        "focus",
        "responsive",
        "web-vitals",
        "lcp",
        "inp",
        "cls",
    )
    extensions = (".tsx", ".jsx", ".vue", ".svelte", ".css", ".scss")
    evidence = [
        path
        for path in files
        if path in exact_files
        or path.startswith(directory_prefixes)
        or any(fragment in path for fragment in fragments)
        or path.endswith(extensions)
    ]
    evidence.extend(directory for directory in directories if directory.startswith(("components", "pages", "routes", "src/components", "src/pages")))
    return evidence


def _backend_signal_evidence(files: set[str], directories: set[str]) -> list[str]:
    directory_prefixes = (
        "adapters/",
        "backend/",
        "consumers/",
        "cron/",
        "jobs/",
        "queues/",
        "repositories/",
        "schedulers/",
        "server/",
        "services/",
        "src/adapters/",
        "src/backend/",
        "src/consumers/",
        "src/jobs/",
        "src/queues/",
        "src/repositories/",
        "src/schedulers/",
        "src/server/",
        "src/services/",
        "src/workers/",
        "workers/",
    )
    exact_files = {
        "docker-compose.yml",
        "dockerfile",
        "procfile",
        "serverless.yml",
    }
    file_fragments = (
        "celery",
        "consumer",
        "controller",
        "django",
        "fastapi",
        "flask",
        "grpc",
        "health",
        "job",
        "queue",
        "repository",
        "retry",
        "scheduler",
        "service",
        "sidekiq",
        "spring",
        "worker",
    )
    evidence = [
        path
        for path in files
        if path in exact_files
        or path.startswith(directory_prefixes)
        or path in OPENAPI_MARKERS
        or path in ASYNCAPI_MARKERS
        or path.endswith((".proto", "/openapi.yaml", "/openapi.yml", "/openapi.json", "/asyncapi.yaml", "/asyncapi.yml"))
        or any(fragment in path for fragment in file_fragments)
    ]
    evidence.extend(
        directory
        for directory in directories
        if directory in {
            "adapters",
            "backend",
            "consumers",
            "cron",
            "jobs",
            "queues",
            "repositories",
            "schedulers",
            "server",
            "services",
            "workers",
        }
        or directory.startswith(directory_prefixes)
    )
    return evidence


def _codex_agentic_signal_evidence(files: set[str], directories: set[str]) -> list[str]:
    exact_files = {
        ".mcp.json",
        "agents.md",
        "agents.override.md",
        "automation.toml",
        "config.toml",
        "hooks.json",
        "skill.md",
        "agent-task-packet.md",
        "handoff-contract.md",
        "worktree-ownership.md",
        "plugin-blueprint.md",
        "automation-candidate.md",
        "model-reasoning-policy.md",
        "mcp-permission-review.md",
        "hook-governance.md",
        "skill-promotion-record.md",
        "agent-eval-workflow.md",
    }
    directory_prefixes = (
        ".agents/",
        ".codex/",
        ".codex-plugin/",
        "docs/artifact-templates/",
        "docs/insights/",
        "docs/playbooks/",
        "docs/product-agent/",
        "docs/runtime/",
        "plugins/",
        "skills/",
        "subagents/",
    )
    directory_names = {
        ".agents",
        ".codex",
        ".codex-plugin",
        "plugins",
        "skills",
        "subagents",
    }
    evidence = [
        path
        for path in files
        if path in exact_files
        or path.startswith(directory_prefixes)
        or path.endswith("/skill.md")
        or path.endswith("/automation.toml")
        or path.endswith("/hooks.json")
        or path.endswith("/config.toml")
        or path.endswith("/agent-task-packet.md")
        or path.endswith("/handoff-contract.md")
        or path.endswith("/worktree-ownership.md")
    ]
    evidence.extend(directory for directory in directories if directory in directory_names)
    return evidence


def _quality_signal_evidence(files: set[str], directories: set[str]) -> list[str]:
    directory_names = {
        "tests",
        "test",
        "spec",
        "e2e",
        "playwright",
        "cypress",
        "coverage",
        "evals",
        ".github/workflows",
        "fixtures",
        "__tests__",
        "snapshots",
    }
    exact_files = {
        "test.md",
        "evals.md",
        "runlog.md",
        "pytest.ini",
        "tox.ini",
        "promptfoo.yaml",
        "promptfooconfig.yaml",
    }
    file_fragments = (
        "vitest.config.",
        "jest.config.",
        "playwright.config.",
        "coverage",
        "pact",
        "openapi",
        "asyncapi",
        "junit",
        "pytest",
        "unittest",
        "testing-library",
        "storybook",
        "stryker",
        "hypothesis",
        "ragas",
        "codecov",
        "flaky",
        "retry",
    )
    evidence = [
        path
        for path in files
        if path in exact_files
        or path.startswith(tuple(f"{directory}/" for directory in directory_names))
        or any(fragment in path for fragment in file_fragments)
    ]
    evidence.extend(directory for directory in directories if directory in directory_names)
    return evidence


def _intent_signals(intent: str) -> list[dict[str, str]]:
    signals: list[dict[str, str]] = []
    for category, terms in [
        ("business_product", BUSINESS_INTENT_TERMS),
        ("requirements_domain", REQUIREMENTS_INTENT_TERMS),
        ("behavior_change", BEHAVIOR_INTENT_TERMS),
        ("frontend", UI_INTENT_TERMS),
        ("backend", BACKEND_INTENT_TERMS),
        ("api_integrations", API_INTENT_TERMS),
        ("solution_architecture", ARCHITECTURE_INTENT_TERMS),
        ("quality_testing_evals", QUALITY_INTENT_TERMS),
        ("llm_ai_rag", AI_INTENT_TERMS),
        ("delivery_release_operations", DELIVERY_INTENT_TERMS),
        ("high_risk", HIGH_RISK_INTENT_TERMS),
        ("regulated", REGULATED_INTENT_TERMS),
    ]:
        for term in sorted(terms):
            if term in intent:
                signals.append({"category": category, "term": term})
    return signals


def _classify_maturity(
    files: set[str],
    directories: set[str],
    observed: list[dict[str, Any]],
    intent: str,
) -> dict[str, Any]:
    if _mentions_any(intent, REGULATED_INTENT_TERMS):
        return {
            "selected": "regulated",
            "confidence": "medium",
            "reasons": ["regulated intent term detected"],
        }
    has_ci = _has_signal(observed, "ci_configuration")
    has_release = _mentions_any(intent, {"production", "release"}) or _has_any_signal(
        observed,
        {"deployment_configuration", "release_file"},
    )
    if has_release and _has_any_signal(observed, {"ci_configuration", "deployment_configuration", "release_file"}):
        return {
            "selected": "production",
            "confidence": "medium",
            "reasons": ["production or release intent with CI or deployment evidence"],
        }
    if has_ci or len(files) > 1 or bool(directories - {"docs"}):
        return {
            "selected": "team",
            "confidence": "medium",
            "reasons": ["workspace has project or collaboration signals"],
        }
    return {
        "selected": "baseline",
        "confidence": "high" if not files or files <= {"readme.md"} else "medium",
        "reasons": ["empty or README-only workspace" if not files or files <= {"readme.md"} else "minimal workspace signals"],
    }


def _classify_complexity(
    files: set[str],
    directories: set[str],
    observed: list[dict[str, Any]],
    intent: str,
) -> dict[str, Any]:
    if _mentions_any(intent, HIGH_RISK_INTENT_TERMS | REGULATED_INTENT_TERMS):
        return {
            "selected": "high_risk",
            "confidence": "medium",
            "reasons": ["high-risk or regulated intent term detected"],
        }
    has_api = _has_any_signal(observed, {"openapi_contract", "asyncapi_contract", "graphql_schema", "protobuf_schema"})
    has_database = _has_signal(observed, "database_migration_or_schema")
    has_ci = _has_signal(observed, "ci_configuration")
    if has_api and (has_database or has_ci):
        return {
            "selected": "complex",
            "confidence": "high",
            "reasons": ["API contract plus database or CI signal detected"],
        }
    if has_api or has_database or _has_signal(observed, "deployment_configuration") or len(directories) > 3:
        return {
            "selected": "standard",
            "confidence": "medium",
            "reasons": ["multiple implementation surfaces detected"],
        }
    return {
        "selected": "simple",
        "confidence": "high" if not files or files <= {"readme.md"} else "medium",
        "reasons": ["empty or README-only workspace" if not files or files <= {"readme.md"} else "limited workspace signals"],
    }


def _methodology_domains(
    observed: list[dict[str, Any]],
    intent: str,
    maturity_level: str,
    complexity_profile: str,
    has_files: bool,
) -> list[dict[str, Any]]:
    catalog = load_methodology_catalog()
    applicable = {
        "business_product": _business_product_applies(intent),
        "requirements_domain": _requirements_domain_applies(has_files, intent),
        "solution_architecture": _solution_architecture_applies(
            observed,
            intent,
            maturity_level,
            complexity_profile,
        ),
        "quality_testing_evals": _quality_testing_evals_applies(observed, has_files, intent),
        "codex_agentic_workflow": _codex_agentic_workflow_applies(observed, intent),
        "frontend": _frontend_applies(observed, intent),
        "backend": _backend_applies(observed, intent),
        "api_integrations": _mentions_any(intent, API_INTENT_TERMS)
        or _has_any_signal(observed, {"openapi_contract", "asyncapi_contract", "graphql_schema", "protobuf_schema"}),
        "database_data": _has_signal(observed, "database_migration_or_schema") or "production data" in intent,
        "llm_ai_rag": _mentions_any(intent, AI_INTENT_TERMS) or _has_signal(observed, "ai_eval_or_rag"),
        "security_privacy_compliance": complexity_profile == "high_risk"
        or maturity_level == "regulated"
        or _mentions_any(intent, HIGH_RISK_INTENT_TERMS),
        "delivery_release_operations": maturity_level in {"production", "regulated"}
        or _mentions_any(intent, DELIVERY_INTENT_TERMS)
        or _has_any_signal(observed, {"ci_configuration", "deployment_configuration"}),
    }

    domain_packets: list[dict[str, Any]] = []
    observed_domain_ids = _observed_domain_ids(observed)
    for domain in catalog["domains"]:
        domain_id = domain["id"]
        is_applicable = bool(applicable.get(domain_id, False))
        status = "present_unverified" if domain_id in observed_domain_ids else "applicable_missing"
        domain_packets.append(
            {
                "id": domain_id,
                "title": domain["title"],
                "source_file": domain["source_file"],
                "status": status if is_applicable else "not_applicable",
                "applicability_reason": "catalog domain applies to observed workspace or intent signals"
                if is_applicable
                else "no deterministic signal detected",
            }
        )
    return domain_packets


def _business_product_applies(intent: str) -> bool:
    if _business_product_not_applicable(intent):
        return False
    return _mentions_any(intent, BUSINESS_INTENT_TERMS | IMPLEMENTATION_OR_RELEASE_TERMS)


def _business_product_not_applicable(intent: str) -> bool:
    return any(phrase in intent for phrase in BUSINESS_NOT_APPLICABLE_PHRASES)


def _requirements_domain_applies(has_files: bool, intent: str) -> bool:
    if _requirements_domain_not_applicable(intent):
        return False
    return has_files or _mentions_any(intent, REQUIREMENTS_INTENT_TERMS | BEHAVIOR_INTENT_TERMS)


def _requirements_domain_not_applicable(intent: str) -> bool:
    return any(phrase in intent for phrase in REQUIREMENTS_NOT_APPLICABLE_PHRASES)


def _solution_architecture_applies(
    observed: list[dict[str, Any]],
    intent: str,
    maturity_level: str,
    complexity_profile: str,
) -> bool:
    if _solution_architecture_not_applicable(intent):
        return False
    return (
        complexity_profile in {"complex", "high_risk"}
        or maturity_level in {"team", "production", "regulated"}
        or _mentions_any(intent, ARCHITECTURE_INTENT_TERMS | PUBLIC_CONTRACT_TERMS | DATA_BOUNDARY_TERMS)
        or _has_any_signal(
            observed,
            {
                "openapi_contract",
                "asyncapi_contract",
                "graphql_schema",
                "protobuf_schema",
                "database_migration_or_schema",
                "ai_eval_or_rag",
                "deployment_configuration",
                "architecture_docs",
            },
        )
    )


def _solution_architecture_not_applicable(intent: str) -> bool:
    return any(phrase in intent for phrase in SOLUTION_ARCHITECTURE_NOT_APPLICABLE_PHRASES)


def _quality_testing_evals_applies(observed: list[dict[str, Any]], has_files: bool, intent: str) -> bool:
    if _quality_testing_evals_not_applicable(intent):
        return False
    return (
        has_files
        or _mentions_any(intent, QUALITY_INTENT_TERMS | BEHAVIOR_INTENT_TERMS | DELIVERY_INTENT_TERMS)
        or _has_any_signal(observed, {"test_evidence", "test_command", "quality_testing_signal"})
    )


def _quality_testing_evals_not_applicable(intent: str) -> bool:
    return any(phrase in intent for phrase in QUALITY_NOT_APPLICABLE_PHRASES)


def _codex_agentic_workflow_applies(observed: list[dict[str, Any]], intent: str) -> bool:
    if _codex_agentic_workflow_not_applicable(intent):
        return False
    return _has_signal(observed, "codex_agentic_workflow") or _mentions_any(intent, CODEX_AGENTIC_INTENT_TERMS)


def _codex_agentic_workflow_not_applicable(intent: str) -> bool:
    return any(phrase in intent for phrase in CODEX_AGENTIC_NOT_APPLICABLE_PHRASES)


def _frontend_applies(observed: list[dict[str, Any]], intent: str) -> bool:
    if _frontend_not_applicable(intent):
        return False
    return _has_signal(observed, "frontend") or _mentions_any(intent, FRONTEND_INTENT_TERMS)


def _frontend_not_applicable(intent: str) -> bool:
    return any(phrase in intent for phrase in FRONTEND_NOT_APPLICABLE_PHRASES)


def _backend_applies(observed: list[dict[str, Any]], intent: str) -> bool:
    if _backend_not_applicable(intent):
        return False
    return (
        _has_signal(observed, "backend")
        or _has_any_signal(observed, {"openapi_contract", "asyncapi_contract", "database_migration_or_schema"})
        or _mentions_any(intent, BACKEND_INTENT_TERMS | BACKEND_RUNTIME_TERMS | BACKEND_CONTRACT_TERMS)
        or _mentions_any(intent, UNSUPPORTED_BACKEND_CLAIMS)
    )


def _backend_not_applicable(intent: str) -> bool:
    return any(phrase in intent for phrase in BACKEND_NOT_APPLICABLE_PHRASES)


def _backend_severity_mode(intent: str) -> str:
    lightweight_terms = (
        "backend-light",
        "local/backend-light",
        "simple local",
        "local-only",
        "prototype",
        "without production users",
        "non-production",
    )
    if any(term in intent for term in lightweight_terms):
        return "lightweight"
    production_terms = (
        "production",
        "deploy",
        "release",
        "ship",
        "external write",
        "irreversible",
        "payment",
        "pii",
        "sensitive",
        "security",
        "migration",
        "public api",
        "public contract",
    )
    if any(term in intent for term in production_terms):
        return "production"
    return "standard"


def _backend_has_complete_accepted_gap(intent: str) -> bool:
    gap_marker = "explicit_gap_accepted" in intent or "accepted gap" in intent
    required_terms = ("owner", "reason", "review date")
    risk_terms = ("downstream risk", "residual risk")
    follow_up_terms = ("follow-up", "follow up", "followup")
    return (
        gap_marker
        and all(term in intent for term in required_terms)
        and any(term in intent for term in risk_terms)
        and any(term in intent for term in follow_up_terms)
    )


def _business_product_recommendations(files: set[str], intent: str) -> list[dict[str, Any]]:
    if not _business_product_applies(intent):
        return []

    recommendations: list[dict[str, Any]] = []
    implementation_or_release = bool(files) and _mentions_any(intent, IMPLEMENTATION_OR_RELEASE_TERMS)
    product_hypothesis_priority = "P1_high_risk" if implementation_or_release else "P2_recommended"
    recommendations.append(
        _recommendation(
            priority=product_hypothesis_priority,
            reason="Product or behavior-changing intent needs a product hypothesis before implementation.",
            domain="business_product",
            gate="product_hypothesis_present",
            artifact="product-brief.md",
            evidence_required=[
                "target user segment",
                "problem or opportunity",
                "expected outcome",
                "non-goals",
                "owner",
            ],
            evidence_owner="product owner",
            approval_boundary="not required for read-only audit; approval_required before broad implementation",
            accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
            residual_risk="Implementation can optimize the wrong behavior when product intent is implicit.",
            safe_next_action="Stage a product brief before requirements slicing or implementation.",
        )
    )
    recommendations.append(
        _recommendation(
            priority="P2_recommended",
            reason="Decision horizon is missing for product methodology depth.",
            domain="business_product",
            gate="decision_horizon_present",
            artifact="product-brief.md",
            evidence_required=["discovery, MVP, beta, production or scale", "owner", "review window"],
            evidence_owner="product owner",
            approval_boundary="not required for drafting methodology recommendations",
            accepted_gap_option="explicit_gap_accepted with owner and reason for unknown decision horizon",
            residual_risk="The same process depth can be over-applied to discovery work or under-applied to production work.",
            safe_next_action="Classify the decision horizon before choosing required artifacts.",
        )
    )
    recommendations.append(
        _recommendation(
            priority="P1_high_risk" if implementation_or_release else "P2_recommended",
            reason="Metric scope is not classified for product behavior work.",
            domain="business_product",
            gate="metric_scope_classified",
            artifact="REQUIREMENTS.md",
            evidence_required=["metric_scope required, not_applicable or accepted_gap", "owner", "residual risk"],
            evidence_owner="product owner",
            approval_boundary="not required for read-only classification",
            accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
            residual_risk="Unclassified metric scope can turn planned measurement into unsupported success claims.",
            safe_next_action="Classify metric scope before planning implementation or release text.",
        )
    )
    if _mentions_any(intent, PRODUCT_SUCCESS_TERMS):
        recommendations.append(
            _recommendation(
                priority="P2_recommended",
                reason="Product success or North Star wording needs metric-level separation.",
                domain="business_product",
                gate="outcome_metric_level_separated",
                artifact="metric-spec.md",
                evidence_required=["business outcome", "product outcome", "feature traction metric"],
                evidence_owner="product owner",
                approval_boundary="not required for metric classification",
                accepted_gap_option="explicit_gap_accepted with owner and reason for metric-level ambiguity",
                residual_risk="A local feature traction metric can be mistaken for a product value metric.",
                safe_next_action="Separate business outcome, product outcome and feature traction metric.",
            )
        )
    if _mentions_any(intent, {"metric", "success", "measurement", "analytics", "dashboard"}):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Metric claim needs counter-metric, guardrail, qualitative review and privacy classification.",
                domain="business_product",
                gate="metric_hardening_when_product_behavior_changes",
                artifact="metric-spec.md",
                evidence_required=[
                    "primary metric",
                    "input metric",
                    "counter-metric",
                    "guardrail",
                    "proxy metric risk",
                    "qualitative review",
                    "privacy classification",
                ],
                evidence_owner="product owner",
                approval_boundary="approval_required before external analytics writes or product success claims",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="A single metric can improve while product quality, trust, support load or privacy degrades.",
                safe_next_action="Stage metric hardening before implementation or success claims.",
            )
        )
        recommendations.append(
            _recommendation(
                priority="P2_recommended",
                reason="Metric claim needs qualitative feedback or an accepted qualitative evidence gap.",
                domain="business_product",
                gate="qualitative_feedback_loop_present",
                artifact="metric-spec.md",
                evidence_required=["user research, support, sales, customer-success or owner review evidence"],
                evidence_owner="product owner",
                approval_boundary="not required for read-only audit",
                accepted_gap_option="explicit_gap_accepted with owner and reason for missing qualitative loop",
                residual_risk="Quantitative movement can hide user trust, support or satisfaction regressions.",
                safe_next_action="Record a qualitative feedback loop or accepted gap.",
            )
        )
    if _mentions_any(intent, PRODUCT_ANALYTICS_TERMS):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Product analytics claim needs event taxonomy, property definitions, owner and validation evidence.",
                domain="business_product",
                gate="analytics_tracking_plan_present",
                artifact="tracking-plan.md",
                evidence_required=[
                    "event names",
                    "properties",
                    "property types",
                    "taxonomy",
                    "owner",
                    "validation command or report",
                    "privacy classification",
                ],
                evidence_owner="data or product analytics owner",
                approval_boundary="approval_required before external analytics writes or production telemetry changes",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="Analytics events without taxonomy or validation can make product decisions unreliable.",
                safe_next_action="Stage a tracking plan before instrumentation or analytics claims.",
            )
        )
    if _mentions_any(intent, AI_INTENT_TERMS):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="AI product behavior needs both eval evidence and product value evidence.",
                domain="business_product",
                gate="ai_product_eval_when_ai_behavior_changes",
                artifact="ai-eval-spec.md",
                evidence_required=["user-visible promise", "baseline eval", "threshold", "failure review owner"],
                evidence_owner="AI product owner",
                approval_boundary="not required for baseline planning; approval_required before external AI behavior release",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="AI eval score can be mistaken for product value without user outcome evidence.",
                safe_next_action="Stage AI product eval and value evidence before prompt, model, retrieval or agent changes.",
            )
        )
    if "release" in intent or "after release" in intent or "telemetry" in intent:
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Product success claim after release needs actual evidence or an accepted evidence gap.",
                domain="business_product",
                gate="release_measurement_evidence_present",
                artifact="RUNLOG.md",
                evidence_required=[
                    "actual metric",
                    "eval result",
                    "user feedback",
                    "support signal",
                    "owner review",
                    "accepted evidence gap",
                ],
                evidence_owner="learning-loop maintainer",
                approval_boundary="approval_required before release success claims or external release actions",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="Planned measurement alone is not product success evidence.",
                safe_next_action="Record post-release evidence or accepted gap before success claims.",
            )
        )
    if _mentions_any(intent, WORKFLOW_PROMOTION_TERMS):
        recommendations.append(
            _recommendation(
                priority="P2_recommended",
                reason="Workflow promotion needs value evidence, verification, owner and safety boundary.",
                domain="business_product",
                gate="workflow_promotion_value_evidence_present",
                artifact="skill-promotion-record.md",
                evidence_required=["engineering time saved", "verification", "owner", "safety boundary"],
                evidence_owner="workflow owner",
                approval_boundary="approval_required before active automation or durable promotion",
                accepted_gap_option="explicit_gap_accepted with owner and reason for no external product metric",
                residual_risk="A repeated workflow can be automated before it has stable value or safety evidence.",
                safe_next_action="Record workflow value evidence before promotion to skill, plugin or automation.",
            )
        )
    return recommendations


def _requirements_domain_recommendations(files: set[str], intent: str) -> list[dict[str, Any]]:
    if not _requirements_domain_applies(bool(files), intent):
        return []

    recommendations: list[dict[str, Any]] = []
    behavior_change = _mentions_any(intent, BEHAVIOR_INTENT_TERMS | {"behavior change", "feature"})
    requirements_intent = _mentions_any(intent, REQUIREMENTS_INTENT_TERMS)
    non_trivial = bool(files) and (behavior_change or requirements_intent)

    if _mentions_any(intent, UNSUPPORTED_REQUIREMENTS_CLAIMS):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Unsupported requirements or domain methodology claim appeared as evidence.",
                domain="requirements_domain",
                gate="unsupported_claims_rejected",
                artifact="domain-review-record.md",
                evidence_required=[
                    "claim",
                    "source or owner verification",
                    "replacement evidence",
                    "unsupported claim disposition",
                ],
                evidence_owner="requirements owner",
                approval_boundary="not required for read-only audit; approval_required before using claim as delivery evidence",
                accepted_gap_option="explicit_gap_accepted with owner, reason, downstream risk and follow-up condition",
                residual_risk="A method slogan can be mistaken for requirements, test or domain evidence.",
                safe_next_action="Record the unsupported claim in domain-review-record.md before planning implementation.",
            )
        )

    if behavior_change and not _artifact_present(files, "acceptance-scenarios.md"):
        recommendations.append(
            _recommendation(
                priority="P0_blocker",
                reason="Behavior-changing work needs acceptance scenarios before implementation.",
                domain="requirements_domain",
                gate="acceptance_scenarios_when_behavior_changes",
                artifact="acceptance-scenarios.md",
                evidence_required=[
                    "requirement",
                    "scenario",
                    "observable outcome",
                    "check",
                    "evidence owner",
                ],
                evidence_owner="requirements owner",
                approval_boundary="not required for staging scenarios; approval_required before broad implementation",
                accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                residual_risk="Implementation can change behavior without a shared acceptance contract.",
                safe_next_action="Stage acceptance-scenarios.md before implementation.",
            )
        )
    if non_trivial:
        recommendations.extend(
            [
                _recommendation(
                    priority="P1_high_risk",
                    reason="Non-trivial product or system work needs requirement quality evidence.",
                    domain="requirements_domain",
                    gate="requirement_quality_present",
                    artifact="requirement-registry.md",
                    evidence_required=[
                        "atomicity",
                        "clarity",
                        "testability",
                        "feasibility",
                        "traceability",
                        "source",
                        "owner",
                    ],
                    evidence_owner="requirements owner",
                    approval_boundary="not required for read-only audit",
                    accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                    residual_risk="A story title or vague requirement can be planned as complete scope.",
                    safe_next_action="Stage requirement-registry.md and record quality fields.",
                ),
                _recommendation(
                    priority="P1_high_risk",
                    reason="Requirements evidence must exist before implementation starts.",
                    domain="requirements_domain",
                    gate="requirements_evidence_before_implementation",
                    artifact="PLAN.md",
                    evidence_required=[
                        "requirements packet",
                        "acceptance scenarios",
                        "traceability",
                        "owner",
                        "accepted gap if incomplete",
                    ],
                    evidence_owner="implementation planner",
                    approval_boundary="approval_required before implementation proceeds with missing requirements evidence",
                    accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                    residual_risk="Build work can proceed from assumptions instead of source-backed requirements.",
                    safe_next_action="Block implementation until requirements evidence or accepted gaps are recorded.",
                ),
            ]
        )
    if _mentions_any(intent, REQUIREMENT_ID_TERMS):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Multi-slice, regulatory, risky, long-lived or public-contract work needs stable requirement IDs.",
                domain="requirements_domain",
                gate="requirement_ids_present",
                artifact="requirement-registry.md",
                evidence_required=["stable requirement ID", "status", "source", "owner", "linked artifacts"],
                evidence_owner="requirements owner",
                approval_boundary="not required for registry staging",
                accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                residual_risk="Tests, contracts, docs and release evidence cannot reliably reference changing requirements.",
                safe_next_action="Create requirement IDs in requirement-registry.md.",
            )
        )
    if _mentions_any(intent, CONSTRAINT_TERMS):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Constraint evidence needs traceability to requirements, tests, contracts and release decisions.",
                domain="requirements_domain",
                gate="constraints_traceability_present",
                artifact="requirements-traceability-matrix.md",
                evidence_required=[
                    "compliance/privacy/security/operational/performance/platform/accessibility/retention/localization/cost constraint",
                    "affected requirement",
                    "check or eval",
                    "owner",
                ],
                evidence_owner="requirements owner",
                approval_boundary="approval_required before sensitive, external or irreversible constraint changes",
                accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                residual_risk="Constraints can be lost between requirements, implementation and release evidence.",
                safe_next_action="Add constraint rows to requirements-traceability-matrix.md.",
            )
        )
    if _mentions_any(intent, API_UI_DATA_TRACE_TERMS):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Requirement or domain terms touching API, UI or data need downstream traceability.",
                domain="requirements_domain",
                gate="api_ui_data_traceability_present",
                artifact="requirements-traceability-matrix.md",
                evidence_required=[
                    "requirement or domain term",
                    "API/event/schema",
                    "UI label or state",
                    "data field",
                    "code/test/eval evidence",
                ],
                evidence_owner="requirements owner",
                approval_boundary="approval_required before public contract, schema or user-visible behavior changes",
                accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                residual_risk="API, UI and data semantics can diverge from business requirements.",
                safe_next_action="Stage requirements-traceability-matrix.md with API/UI/data mappings.",
            )
        )
    if _mentions_any(intent, STAKEHOLDER_OWNER_TERMS) or "business rule" in intent or _mentions_any(intent, DOMAIN_REVIEW_TERMS):
        recommendations.append(
            _recommendation(
                priority="P2_recommended",
                reason="Stakeholder, process or value ambiguity needs an owner map.",
                domain="requirements_domain",
                gate="stakeholder_owner_map_present",
                artifact="stakeholder-owner-map.md",
                evidence_required=["stakeholder", "domain expert", "technical owner", "decision authority", "escalation path"],
                evidence_owner="requirements owner",
                approval_boundary="not required for owner-map staging",
                accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                residual_risk="Domain meaning and business rules can be reviewed by the wrong owner.",
                safe_next_action="Stage stakeholder-owner-map.md before finalizing the requirements packet.",
            )
        )
    if _mentions_any(intent, STORY_SLICE_TERMS):
        recommendations.append(
            _recommendation(
                priority="P2_recommended",
                reason="User stories, MVP boundaries or deferred slices need story-slice evidence.",
                domain="requirements_domain",
                gate="story_slice_map_present",
                artifact="story-slice-map.md",
                evidence_required=["user story", "value slice", "risk slice", "MVP boundary", "deferred slices", "non-goals"],
                evidence_owner="requirements owner",
                approval_boundary="not required for story-slice staging",
                accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                residual_risk="A story title can be mistaken for complete requirements and release scope.",
                safe_next_action="Stage story-slice-map.md and link it to acceptance scenarios.",
            )
        )
    if _mentions_any(intent, UNCLEAR_STORY_TERMS):
        recommendations.append(
            _recommendation(
                priority="P2_recommended",
                reason="Unclear, large or disputed stories need Example Mapping before implementation.",
                domain="requirements_domain",
                gate="example_mapping_when_unclear_story",
                artifact="example-map.md",
                evidence_required=["story", "rules", "examples", "questions", "owner", "next action"],
                evidence_owner="requirements owner",
                approval_boundary="not required for clarification artifact staging",
                accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                residual_risk="Ambiguous stories can hide rules, examples and unresolved questions.",
                safe_next_action="Run Example Mapping or stage example-map.md before slicing implementation.",
            )
        )
    if "business rule" in intent or "business rules" in intent:
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Business rules need source, owner, enforcement layer, exceptions and failure behavior.",
                domain="requirements_domain",
                gate="business_rules_present",
                artifact="business-rules.md",
                evidence_required=["rule", "source", "owner", "enforcement layer", "exceptions", "failure mode"],
                evidence_owner="domain owner",
                approval_boundary="approval_required before business-critical or compliance rule changes",
                accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                residual_risk="Implicit business rules can be enforced inconsistently across code, API, UI and tests.",
                safe_next_action="Stage business-rules.md before implementation planning.",
            )
        )
    if _mentions_any(intent, DOMAIN_DISCOVERY_TERMS):
        recommendations.append(
            _recommendation(
                priority="P2_recommended",
                reason="Complex process or overloaded domain language needs discovery workshop evidence.",
                domain="requirements_domain",
                gate="domain_discovery_workshop_when_complex_process",
                artifact="domain-modeling.md",
                evidence_required=["EventStorming, Domain Storytelling, interview or accepted gap", "owner", "hotspots"],
                evidence_owner="domain owner",
                approval_boundary="not required for discovery notes",
                accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                residual_risk="Cross-silo process behavior can be planned from a partial mental model.",
                safe_next_action="Record domain discovery evidence or accepted gap in domain-modeling.md.",
            )
        )
    if _mentions_any(intent, STATE_TRANSITION_TERMS):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Domain state transitions need invariants and failure modes.",
                domain="requirements_domain",
                gate="invariants_and_failure_modes_present",
                artifact="domain-modeling.md",
                evidence_required=["invariant", "invalid transition", "enforcement layer", "failure behavior", "test/eval evidence"],
                evidence_owner="domain owner",
                approval_boundary="approval_required before risky state transition changes",
                accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                residual_risk="Invalid domain transitions can ship without explicit failure behavior.",
                safe_next_action="Add invariants and failure modes to domain-modeling.md.",
            )
        )
    if _mentions_any(intent, DOMAIN_EVENT_TERMS):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Domain events crossing a boundary need contract semantics.",
                domain="requirements_domain",
                gate="domain_event_contracts_present",
                artifact="requirements-traceability-matrix.md",
                evidence_required=["meaning", "producer", "consumers", "schema link", "ordering/idempotency", "privacy classification"],
                evidence_owner="domain or API owner",
                approval_boundary="approval_required before event contract or public integration changes",
                accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                residual_risk="Technical events can lose business meaning, compatibility and privacy assumptions.",
                safe_next_action="Trace the domain event in requirements-traceability-matrix.md.",
            )
        )
    if _mentions_any(intent, DOMAIN_REVIEW_TERMS):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Business-critical, compliance, finance/legal or AI-generated domain claims need owner review.",
                domain="requirements_domain",
                gate="domain_expert_review_present",
                artifact="domain-review-record.md",
                evidence_required=["domain expert", "claim", "source", "review outcome", "conflicts or accepted gap"],
                evidence_owner="domain expert",
                approval_boundary="approval_required before using reviewed claim for release or external behavior",
                accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                residual_risk="AI or unreviewed domain claims can become unverified system behavior.",
                safe_next_action="Stage domain-review-record.md before implementation or release claims.",
            )
        )
    if _mentions_any(intent, CHANGE_IMPACT_TERMS):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Requirement or domain rule changes after planning need impact review.",
                domain="requirements_domain",
                gate="requirement_change_impact_review_present",
                artifact="requirement-change-impact.md",
                evidence_required=["tests/evals", "API", "DB", "UI", "docs", "rollout", "rollback", "approval boundary"],
                evidence_owner="implementation planner",
                approval_boundary="approval_required before applying changed scope to public, data or release surfaces",
                accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                residual_risk="Downstream tests, contracts, data, UI, docs or release plans can remain stale after scope changes.",
                safe_next_action="Stage requirement-change-impact.md before continuing implementation.",
            )
        )
    if "accepted gap" in intent and not all(
        term in intent for term in ["owner", "reason", "scope", "review date", "downstream risk", "follow-up"]
    ):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Accepted gaps require owner, reason, scope, review date, downstream risk and follow-up condition.",
                domain="requirements_domain",
                gate="accepted_gap_recorded",
                artifact="domain-review-record.md",
                evidence_required=["owner", "reason", "scope", "review date", "downstream risk", "follow-up condition"],
                evidence_owner="requirements owner",
                approval_boundary="approval_required before treating an incomplete methodology gate as accepted",
                accepted_gap_option="explicit_gap_accepted only when all accepted-gap fields are present",
                residual_risk="Accepted gaps can become invisible scope debt without owner and review conditions.",
                safe_next_action="Complete the accepted-gap record before proceeding.",
            )
        )
    if _mentions_any(intent, DECLARATIVE_SCENARIO_LEAK_TERMS):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Business-facing acceptance scenarios must stay declarative and avoid implementation details.",
                domain="requirements_domain",
                gate="declarative_acceptance_scenarios_present",
                artifact="acceptance-scenarios.md",
                evidence_required=[
                    "actor",
                    "context",
                    "trigger",
                    "observable outcome",
                    "no UI selectors, DB internals, function names or test harness details",
                ],
                evidence_owner="requirements owner",
                approval_boundary="not required for scenario rewrite",
                accepted_gap_option="explicit_gap_accepted with owner, reason, scope, review date and residual risk",
                residual_risk="Implementation-specific scenarios can stop being readable or reviewable by domain owners.",
                safe_next_action="Rewrite acceptance scenarios in declarative business language.",
            )
        )
    return recommendations


def _solution_architecture_recommendations(
    files: set[str],
    observed: list[dict[str, Any]],
    intent: str,
    complexity_profile: str,
) -> list[dict[str, Any]]:
    maturity_assumption = "team" if files and files != {"readme.md"} else "baseline"
    if not _solution_architecture_applies(observed, intent, maturity_assumption, complexity_profile):
        return []

    recommendations: list[dict[str, Any]] = []
    has_architecture_overview = _artifact_present(files, "architecture-overview.md")
    high_impact = _mentions_any(intent, HIGH_IMPACT_ARCHITECTURE_TERMS | HIGH_RISK_INTENT_TERMS)
    has_public_contract = _has_any_signal(
        observed,
        {"openapi_contract", "asyncapi_contract", "graphql_schema", "protobuf_schema"},
    ) or _mentions_any(intent, PUBLIC_CONTRACT_TERMS)
    has_data_boundary = _has_signal(observed, "database_migration_or_schema") or _mentions_any(intent, DATA_BOUNDARY_TERMS)
    has_runtime_change = _has_signal(observed, "deployment_configuration") or _mentions_any(
        intent,
        RUNTIME_ARCHITECTURE_TERMS,
    )
    has_observability_need = has_runtime_change or _mentions_any(intent, OBSERVABILITY_TERMS)
    has_diagram = _has_architecture_diagram(files)

    def add(
        *,
        priority: str,
        reason: str,
        gate: str,
        artifact: str,
        evidence_required: list[str],
        residual_risk: str,
        safe_next_action: str,
        evidence_owner: str = "architecture owner",
        approval_boundary: str = "not required for read-only audit",
        accepted_gap_option: str = "explicit_gap_accepted with owner, reason, scope, review date and residual risk",
    ) -> None:
        recommendations.append(
            _recommendation(
                priority=priority,
                reason=reason,
                domain="solution_architecture",
                gate=gate,
                artifact=artifact,
                evidence_required=evidence_required,
                evidence_owner=evidence_owner,
                approval_boundary=approval_boundary,
                accepted_gap_option=accepted_gap_option,
                residual_risk=residual_risk,
                safe_next_action=safe_next_action,
            )
        )

    if _mentions_any(intent, UNSUPPORTED_ARCHITECTURE_CLAIMS):
        add(
            priority="P1_high_risk",
            reason="Unsupported solution architecture claim appeared as evidence.",
            gate="unsupported_architecture_claims_rejected",
            artifact="architecture-review-record.md",
            evidence_required=["claim", "source or owner verification", "replacement evidence", "claim disposition"],
            residual_risk="Architecture slogans can replace boundary, decision, verification or owner evidence.",
            safe_next_action="Record the unsupported architecture claim in architecture-review-record.md before planning.",
        )

    if not has_architecture_overview:
        for gate, reason, evidence in [
            (
                "solution_architecture_scope_present",
                "Complex or multi-surface work needs architecture scope, stakeholders and non-goals.",
                ["scope", "stakeholders", "architecture question", "non-goals", "owner"],
            ),
            (
                "architecture_context_view_present",
                "External users, systems or trust boundaries need a context view or equivalent boundary map.",
                ["external actors", "systems", "trust boundary", "owner"],
            ),
            (
                "architecture_container_boundary_present",
                "Multiple runtime units need container, service, storage, queue or worker boundaries.",
                ["runtime unit", "boundary", "responsibility", "owner"],
            ),
        ]:
            add(
                priority="P1_high_risk",
                reason=reason,
                gate=gate,
                artifact="architecture-overview.md",
                evidence_required=evidence,
                residual_risk="Implementation can cross implicit system boundaries without review.",
                safe_next_action="Stage architecture-overview.md with scope, context and container boundaries.",
            )

    if high_impact or has_public_contract or has_data_boundary or "parallel" in intent:
        add(
            priority="P1_high_risk",
            reason="Architecture boundary changes need responsibility, owner and review evidence.",
            gate="boundary_responsibility_owner_present",
            artifact="architecture-review-record.md",
            evidence_required=["boundary", "responsibility", "owner", "public contract or data ownership", "review outcome"],
            residual_risk="A changed boundary can be owned by no one or reviewed by the wrong owner.",
            safe_next_action="Stage architecture-review-record.md with boundary owner evidence.",
        )

    if has_public_contract:
        add(
            priority="P1_high_risk",
            reason="Public API, event or generated client changes need architecture boundary traceability.",
            gate="public_contract_boundary_trace_present",
            artifact="api-contract-review.md",
            evidence_required=["contract source", "boundary", "consumers", "versioning", "compatibility check"],
            evidence_owner="API owner",
            approval_boundary="approval_required before public contract or generated client changes",
            residual_risk="Consumers can break when contract ownership and boundary semantics are implicit.",
            safe_next_action="Stage api-contract-review.md and link it to the architecture boundary.",
        )

    if has_data_boundary:
        add(
            priority="P1_high_risk",
            reason="Persistent data, PII, retention or migration changes need data ownership evidence.",
            gate="data_ownership_boundary_present",
            artifact="database-dictionary.md",
            evidence_required=["data owner", "source of truth", "retention", "deletion", "migration ownership"],
            evidence_owner="data owner",
            approval_boundary="approval_required before production data or migration changes",
            residual_risk="Data responsibility can diverge from system boundaries and privacy obligations.",
            safe_next_action="Stage database-dictionary.md ownership rows for affected architecture boundaries.",
        )

    if _mentions_any(intent, TRUST_BOUNDARY_TERMS):
        add(
            priority="P1_high_risk",
            reason="Trust boundary or security-sensitive boundary changes need security review evidence.",
            gate="trust_boundary_security_review_present",
            artifact="trust-boundary-map.md",
            evidence_required=["trust boundary", "data flow", "auth", "PII", "security review", "approval boundary"],
            evidence_owner="security or architecture owner",
            approval_boundary="approval_required before auth, payment, PII or security boundary changes",
            residual_risk="Security assumptions can cross runtime and data boundaries without explicit review.",
            safe_next_action="Stage trust-boundary-map.md and link security-risk-review.md where needed.",
        )

    if high_impact:
        add(
            priority="P1_high_risk",
            reason="High-impact or hard-to-reverse architecture decisions need ADR evidence.",
            gate="adr_for_architecture_decision",
            artifact="adr.md",
            evidence_required=["decision", "options", "tradeoff", "verification", "rollback or no-rollback rationale"],
            residual_risk="Architecture choices can become irreversible without recorded alternatives and rollback logic.",
            safe_next_action="Stage adr.md for the architecture decision before implementation.",
        )

    if has_runtime_change:
        add(
            priority="P1_high_risk",
            reason="Runtime or deployment changes need topology evidence.",
            gate="runtime_deployment_topology_present",
            artifact="architecture-overview.md",
            evidence_required=["runtime unit", "deployment target", "dependency", "health check", "rollback path"],
            residual_risk="Runtime behavior can diverge from documented service boundaries.",
            safe_next_action="Add runtime topology to architecture-overview.md.",
        )

    if has_observability_need:
        add(
            priority="P1_high_risk",
            reason="Service or runtime behavior needs observability architecture evidence.",
            gate="observability_architecture_present",
            artifact="architecture-fitness-functions.md",
            evidence_required=["signals", "logs", "metrics", "traces", "dashboards or alerts", "owner"],
            evidence_owner="architecture or operations owner",
            residual_risk="Runtime failures can ship without measurable health or diagnostics.",
            safe_next_action="Stage architecture-fitness-functions.md with observability checks.",
        )

    if _mentions_any(intent, MIGRATION_ROLLBACK_TERMS) or _has_signal(observed, "database_migration_or_schema"):
        add(
            priority="P1_high_risk",
            reason="Architecture migration or service split needs rollback or compensation evidence.",
            gate="migration_rollback_path_present",
            artifact="migration-plan.md",
            evidence_required=["migration step", "rollback", "compensation", "owner", "verification command"],
            evidence_owner="implementation planner",
            approval_boundary="approval_required before irreversible migration or service split",
            residual_risk="A boundary migration can strand data, consumers or runtime traffic without recovery.",
            safe_next_action="Stage migration-plan.md with rollback or accepted no-rollback rationale.",
        )

    if has_diagram and not _artifact_present(files, "architecture-docs-tooling-decision.md"):
        add(
            priority="P2_recommended",
            reason="Architecture diagram files need render or validate evidence when used for review.",
            gate="diagram_render_check_present",
            artifact="architecture-docs-tooling-decision.md",
            evidence_required=["diagram source", "render command", "validation result", "maintenance owner"],
            evidence_owner="docs or architecture owner",
            residual_risk="A diagram can exist but fail to render or drift from reviewed architecture.",
            safe_next_action="Record render check policy in architecture-docs-tooling-decision.md.",
        )

    if _mentions_any(intent, FITNESS_FUNCTION_TERMS) or high_impact:
        add(
            priority="P2_recommended",
            reason="Boundary drift, dependency rules or parallel ownership need architecture fitness functions.",
            gate="architecture_fitness_function_present",
            artifact="architecture-fitness-functions.md",
            evidence_required=["fitness function", "dependency rule", "contract drift check", "owner", "command"],
            residual_risk="Architecture rules can remain advisory and regress silently.",
            safe_next_action="Stage architecture-fitness-functions.md with dependency and drift checks.",
        )

    return recommendations


def _quality_testing_evals_recommendations(
    root: Path,
    files: set[str],
    observed: list[dict[str, Any]],
    intent: str,
    complexity_profile: str,
) -> list[dict[str, Any]]:
    if not _quality_testing_evals_applies(observed, bool(files), intent):
        return []

    recommendations: list[dict[str, Any]] = []

    def add(
        gate: str,
        priority: str,
        artifact: str,
        reason: str,
        evidence_required: list[str],
        evidence_owner: str = "tester",
        approval_boundary: str = "not required for drafting quality evidence; approval_required before external writes",
        accepted_gap_option: str = "explicit_gap_accepted with owner, reason, residual risk and review date",
        residual_risk: str = "Quality claims can be made without current evidence.",
        safe_next_action: str = "Stage the smallest quality evidence artifact before implementation or completion claims.",
    ) -> None:
        recommendations.append(
            _recommendation(
                priority=priority,
                reason=reason,
                domain="quality_testing_evals",
                gate=gate,
                artifact=artifact,
                evidence_required=evidence_required,
                evidence_owner=evidence_owner,
                approval_boundary=approval_boundary,
                accepted_gap_option=accepted_gap_option,
                residual_risk=residual_risk,
                safe_next_action=safe_next_action,
            )
        )

    if any(claim in intent for claim in UNSUPPORTED_QUALITY_CLAIMS):
        add(
            "unsupported_quality_claims_rejected",
            "P1_high_risk",
            "quality-strategy.md",
            "Unsupported quality methodology claim appeared as evidence.",
            ["claim", "source or owner verification", "replacement evidence", "claim disposition"],
            residual_risk="Quality slogans can replace current evidence, risk scope or eval results.",
        )

    if not _has_test_command_or_evidence(root, files, observed):
        add(
            "quality_strategy_present",
            "P0_blocker",
            "quality-strategy.md",
            "No current local test command or quality evidence was detected.",
            ["test command", "eval command", "current output", "evidence owner or accepted gap"],
            residual_risk="Completion claims remain unsupported without a current verification path.",
            safe_next_action="Stage quality-strategy.md with the smallest local verification command or accepted gap.",
        )

    if complexity_profile == "high_risk" or _mentions_any(intent, QUALITY_RISK_TERMS):
        add(
            "risk_based_scope_present",
            "P1_high_risk",
            "quality-strategy.md",
            "Risky, broad or constrained scope needs risk-based quality scope.",
            ["risk areas", "impact", "likelihood", "selected checks", "accepted gaps"],
            evidence_owner="implementation planner",
            residual_risk="Verification can over-focus on easy checks while missing user, data or operational risk.",
        )

    behavior_or_rule = _mentions_any(intent, BEHAVIOR_INTENT_TERMS | DETERMINISTIC_CHANGE_TERMS)
    if behavior_or_rule and not _artifact_present(files, "test-eval-matrix.md"):
        add(
            "acceptance_traceability_present",
            "P1_high_risk",
            "test-eval-matrix.md",
            "Behavior or business-rule work needs acceptance criteria mapped to checks, evals or gaps.",
            ["acceptance criterion", "check or eval", "manual charter", "owner", "explicit gap"],
            evidence_owner="requirements owner",
            residual_risk="Tests can exist without proving the accepted behavior.",
        )
    if _mentions_any(intent, DETERMINISTIC_CHANGE_TERMS) and "red-green" not in intent and "test-first" not in intent:
        add(
            "test_first_or_gap_present",
            "P1_high_risk",
            "test-eval-matrix.md",
            "Deterministic bugfix or business rule needs Red-Green-Refactor evidence or a recorded gap.",
            ["failing command", "passing command", "refactor evidence", "exception reason"],
            evidence_owner="builder",
            residual_risk="A deterministic change can be implemented without proving the test catches the issue.",
        )

    if (
        _mentions_any(intent, API_INTENT_TERMS | PUBLIC_CONTRACT_TERMS | {"schema", "event"})
        or _has_any_signal(observed, {"openapi_contract", "asyncapi_contract", "graphql_schema", "protobuf_schema"})
    ) and not _has_contract_tests(files):
        add(
            "contract_check_present",
            "P1_high_risk",
            "api-contract-review.md",
            "API, event, schema or public package change needs contract compatibility evidence.",
            ["contract source", "consumer/provider impact", "contract check command", "compatibility result"],
            evidence_owner="API owner",
            approval_boundary="approval_required before external API writes or breaking contract changes",
            residual_risk="Contract files do not prove consumers remain compatible.",
        )

    if _mentions_any(intent, RUNTIME_EVIDENCE_TERMS):
        add(
            "runtime_evidence_present",
            "P1_high_risk",
            "manual-qa-evidence.md",
            "Runtime behavior claim needs current runtime evidence.",
            ["command", "environment", "logs", "screenshot, trace or API output", "actual result"],
            evidence_owner="tester",
            residual_risk="Runtime behavior can differ from code inspection or stale logs.",
        )
    if _mentions_any(intent, MANUAL_QA_TERMS):
        add(
            "manual_qa_evidence_present",
            "P2_recommended",
            "manual-qa-evidence.md",
            "Manual QA needs a charter, environment, criteria, reviewer, notes and result.",
            ["charter", "environment", "criteria", "reviewer", "notes", "result"],
            evidence_owner="tester",
            residual_risk="Manual QA without structure cannot be repeated or reviewed.",
        )
    if _mentions_any(intent, VISUAL_A11Y_TERMS):
        public_ui = "public ui" in intent or ("public" in intent and "ui" in intent and "internal" not in intent)
        add(
            "visual_a11y_evidence_present",
            "P1_high_risk" if public_ui else "P2_recommended",
            "manual-qa-evidence.md",
            "UI visual or accessibility change needs viewport, keyboard/focus and screenshot evidence.",
            ["viewport", "component state", "keyboard/focus check", "a11y result", "screenshot or accepted diff"],
            evidence_owner="tester",
            residual_risk="User-facing UI regressions can remain invisible to unit tests.",
        )

    if _mentions_any(intent, QUALITY_EVAL_TERMS):
        add(
            "eval_spec_present",
            "P1_high_risk",
            "ai-eval-spec.md",
            "AI, docs, UX, search or subjective quality change needs an eval spec.",
            ["dataset", "rubric", "grader or assertion", "threshold", "owner"],
            evidence_owner="test-eval designer",
            residual_risk="Subjective quality can drift without a baseline and rubric.",
        )
        add(
            "eval_rerun_evidence_present",
            "P1_high_risk",
            "EVALS.md",
            "Eval-governed change needs baseline/current result, failed cases and rerun command.",
            ["baseline result", "current result", "failed cases", "rerun command", "threshold"],
            evidence_owner="test-eval designer",
            residual_risk="Eval claims can be stale or hide regressions without rerun evidence.",
        )

    if _mentions_any(intent, CI_QUALITY_TERMS) or _has_signal(observed, "ci_configuration"):
        release_or_shared = _mentions_any(intent, {"release", "shared branch", "production"})
        add(
            "ci_quality_gate_present",
            "P1_high_risk" if release_or_shared else "P2_recommended",
            "ci-evidence-record.md",
            "CI quality gate needs command/job, trigger, permissions, artifacts and current result.",
            ["job or command", "trigger", "permissions", "artifact", "exit code", "rerun path"],
            evidence_owner="release operator",
            approval_boundary="approval_required before changing remote CI, rerunning remote jobs or external writes",
            residual_risk="CI configuration does not prove the latest run supports the claim.",
        )
    if _mentions_any(intent, FLAKY_TEST_TERMS):
        add(
            "flaky_test_policy_present",
            "P2_recommended",
            "flaky-test-policy.md",
            "Flaky tests or retries need owner, classification, expiry and follow-up.",
            ["test", "symptom", "owner", "root-cause class", "expiry", "follow-up"],
            evidence_owner="tester",
            residual_risk="Retries can hide intermittent failures without accountability.",
        )
    if _mentions_any(intent, COVERAGE_POLICY_TERMS):
        add(
            "coverage_policy_present",
            "P2_recommended",
            "quality-strategy.md",
            "Coverage claim needs critical-path mapping and non-goals.",
            ["coverage type", "threshold", "critical path", "exclusions", "non-goals"],
            evidence_owner="tester",
            residual_risk="Coverage is a signal, not proof of correctness.",
        )
    if _mentions_any(intent, TEST_DATA_PRIVACY_TERMS):
        add(
            "test_data_privacy_present",
            "P1_high_risk",
            "quality-strategy.md",
            "Tests, fixtures, logs, traces, screenshots or eval datasets need privacy status.",
            ["synthetic or sanitized status", "no secrets", "retention", "owner", "redaction policy"],
            evidence_owner="security or data owner",
            approval_boundary="approval_required before using production data, private customer data or secrets",
            residual_risk="Quality evidence can leak secrets or private customer data.",
        )
    if _mentions_any(intent, {"bugfix", "bug fix"}) and not _artifact_present(files, "bug-rescue-report.md"):
        add(
            "bug_reproduction_evidence_present",
            "P0_blocker",
            "bug-rescue-report.md",
            "Bugfix needs reproduction evidence or an accepted reproduction gap.",
            ["original failure", "reproduction command or steps", "environment", "fixed evidence"],
            evidence_owner="builder",
            residual_risk="A bugfix can miss the original failure without reproduction evidence.",
        )
    if _mentions_any(intent, REGRESSION_IMPACT_TERMS):
        add(
            "regression_impact_present",
            "P1_high_risk",
            "test-eval-matrix.md",
            "Refactor, migration, dependency or shared-code work needs regression impact mapping.",
            ["changed files/contracts/data", "impacted behavior", "checks to rerun", "owner"],
            evidence_owner="implementation planner",
            residual_risk="Unchanged behavior can regress outside the edited files.",
        )
    if _mentions_any(intent, COMPLETION_CLAIM_TERMS):
        add(
            "current_evidence_before_completion",
            "P0_blocker",
            "RUNLOG.md",
            "Completion, readiness, release or quality claim needs current evidence.",
            ["current command evidence", "current eval evidence", "current runtime/manual evidence", "accepted gap"],
            evidence_owner="release operator",
            residual_risk="Old evidence or inspection-only review can be mistaken for current verification.",
        )

    return recommendations


def _codex_agentic_workflow_recommendations(
    files: set[str],
    observed: list[dict[str, Any]],
    intent: str,
) -> list[dict[str, Any]]:
    if not _codex_agentic_workflow_applies(observed, intent):
        return []

    recommendations: list[dict[str, Any]] = []
    high_risk = _mentions_any(intent, CODEX_AGENTIC_HIGH_RISK_TERMS | COMPLETION_CLAIM_TERMS)

    def add(
        gate: str,
        priority: str,
        artifact: str,
        reason: str,
        evidence_required: list[str],
        *,
        owner: str = "product-agent operator",
        approval: str = "approval_required before workspace writes, external writes or activation",
        accepted_gap: str = "explicit_gap_accepted with owner, reason, residual risk and review date",
        residual: str = "Agentic workflow evidence is missing or unverified.",
        next_action: str = "Stage the missing Codex workflow artifact before activating capabilities.",
    ) -> None:
        recommendations.append(
            _recommendation(
                priority=priority,
                reason=reason,
                domain="codex_agentic_workflow",
                gate=gate,
                artifact=artifact,
                evidence_required=evidence_required,
                evidence_owner=owner,
                approval_boundary=approval,
                accepted_gap_option=accepted_gap,
                residual_risk=residual,
                safe_next_action=next_action,
            )
        )

    missing_control_plane = [name for name in CONTROL_PLANE_FILES if name.lower() not in files]
    if missing_control_plane:
        add(
            "control_plane_present",
            "P0_blocker" if high_risk or _has_signal(observed, "codex_agentic_workflow") else "P2_recommended",
            "AGENTS.md",
            "Product-Agent OS control-plane files are missing.",
            ["AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"],
            residual="Missing control-plane files can leave requirements, verification and ownership implicit.",
            next_action="Stage control-plane artifact proposals without mutating existing workspace files.",
        )
    if not {"agents.md", "requirements.md", "plan.md"} <= files:
        add(
            "source_of_truth_present",
            "P0_blocker" if high_risk else "P1_high_risk",
            "AGENTS.md",
            "Codex workflow source-of-truth boundaries are missing.",
            ["AGENTS.md rules", "REQUIREMENTS.md scope", "PLAN.md implementation contract"],
            residual="Memory, chat or generated artifacts can be mistaken for project source of truth.",
        )
    if not _artifact_present(files, "PLAN.md"):
        add(
            "agentic_scope_classified",
            "P1_high_risk",
            "PLAN.md",
            "Agentic scope and runtime path are not classified.",
            ["use-case archetype", "runtime route", "owner", "non-goals", "approval boundary"],
            residual="Agent orchestration can be selected before the smallest useful workflow is known.",
        )
    if not _artifact_present(files, "RUNLOG.md"):
        add(
            "read_only_discovery_complete",
            "P1_high_risk",
            "RUNLOG.md",
            "Read-only discovery evidence is missing before Codex workflow decisions.",
            ["files inspected", "signals observed", "assumptions", "unknowns", "safe next action"],
            residual="Implementation can start from stale or incomplete repository context.",
        )
    if _mentions_any(intent, {"model", "reasoning", "agents sdk", "codex app", "cli", "ide extension"}):
        add(
            "model_reasoning_policy_present",
            "P1_high_risk",
            "model-reasoning-policy.md",
            "Model and reasoning policy is missing for agentic work.",
            ["default model", "reasoning effort", "escalation", "downgrade", "cost/latency budget"],
            residual="Roles can silently overuse or underuse reasoning for risky decisions.",
        )
    if _mentions_any(intent, {"subagent", "subagents", "parallel", "handoff"}) and not _artifact_present(
        files, "agent-task-packet.md"
    ):
        add(
            "fresh_context_handoff_present",
            "P1_high_risk",
            "agent-task-packet.md",
            "Subagent or parallel work lacks a fresh-context task packet.",
            ["sources/context used", "assumptions", "owned files", "expected evidence", "stop conditions"],
            residual="Subagents can act on stale context or unclear ownership.",
        )
    if _mentions_any(intent, {"subagent", "subagents", "parallel", "overlap"}) and not _artifact_present(
        files, "worktree-ownership.md"
    ):
        add(
            "ownership_split_present",
            "P1_high_risk",
            "worktree-ownership.md",
            "Parallel or subagent work lacks explicit ownership split.",
            ["owned files", "forbidden files", "merge order", "rollback owner"],
            residual="Parallel edits can collide without ownership boundaries.",
        )
        add(
            "subagent_parallelism_safe",
            "P1_high_risk",
            "worktree-ownership.md",
            "Parallel subagent work lacks worktree or sequential fallback policy.",
            ["worktree requirement", "shared generated files", "contract/migration ownership", "sequential fallback"],
            residual="Parallel work can overwrite shared artifacts or hide merge risk.",
        )
    if high_risk and not _artifact_present(files, "approval-record.md"):
        add(
            "approval_boundary_present",
            "P0_blocker",
            "approval-record.md",
            "External write, production, MCP, hook or automation boundary lacks approval evidence.",
            ["requested action", "permission boundary", "owner", "approval result", "rollback"],
            residual="A side-effecting workflow can execute without an auditable owner approval.",
        )
    if (
        _has_signal(observed, "codex_agentic_workflow") and any(path.endswith(".mcp.json") for path in files)
    ) or _mentions_any(intent, {"mcp", "remote mcp", "side-effecting tool"}):
        add(
            "mcp_permission_review_present",
            "P1_high_risk",
            "mcp-permission-review.md",
            "MCP capability or trust-boundary review is missing.",
            ["tools/resources/prompts", "auth/secrets", "data boundary", "side effects", "approval"],
            residual="MCP tools can cross data or side-effect boundaries without explicit review.",
        )
    if any(path.endswith("hooks.json") for path in files) or _mentions_any(intent, {"hook", "blocking hook"}):
        add(
            "hook_activation_approval_present",
            "P1_high_risk",
            "hook-governance.md",
            "Hook activation lacks governance and approval evidence.",
            ["event", "matcher", "command", "trust review", "failure behavior", "disable path"],
            residual="Hooks can run commands automatically without sufficient review.",
        )
    if any(path.startswith(".codex-plugin/") or path.startswith("plugins/") for path in files) or "plugin" in intent:
        add(
            "plugin_boundary_present",
            "P2_recommended",
            "plugin-blueprint.md",
            "Plugin packaging boundary is missing or unreviewed.",
            ["inputs", "outputs", "permissions", "owner", "eval cases", "update loop"],
            residual="Reusable plugin behavior can ship without clear boundary or maintenance owner.",
        )
    if _mentions_any(intent, {"repeated workflow", "skill promotion", "playbook", "skill"}):
        add(
            "skill_promotion_evidence_present",
            "P2_recommended",
            "skill-promotion-record.md",
            "Repeated workflow lacks skill promotion evidence.",
            ["manual success evidence", "trigger tests", "negative trigger tests", "failure log"],
            residual="A workflow can be promoted before repeatability and failure modes are known.",
        )
    if any(path.endswith("automation.toml") for path in files) or _mentions_any(intent, {"automation", "schedule"}):
        add(
            "automation_manual_stability_present",
            "P1_high_risk" if high_risk else "P2_recommended",
            "automation-candidate.md",
            "Automation promotion lacks manual stability evidence.",
            ["two successful manual runs or accepted gap", "owner", "cadence", "verification", "disable path"],
            residual="A recurring workflow can run before the manual process is stable.",
        )
    if _mentions_any(intent, {"agents sdk", "tool call", "handoff correctness", "eval", "evals"}):
        add(
            "agent_eval_workflow_present",
            "P1_high_risk",
            "agent-eval-workflow.md",
            "Agent behavior lacks an eval workflow.",
            ["baseline", "trace-derived dataset", "tool-call correctness", "handoff correctness", "threshold"],
            residual="Agent behavior can regress without replayable eval evidence.",
        )
    if "memory" in intent:
        add(
            "memory_policy_present",
            "P1_high_risk",
            "AGENTS.md",
            "Memory policy is missing or confused with source of truth.",
            ["memory as recall only", "durable source files", "secrets policy", "promotion path"],
            residual="Memory can be treated as authoritative project state.",
        )
    if _mentions_any(intent, COMPLETION_CLAIM_TERMS):
        add(
            "agentic_evidence_before_completion",
            "P0_blocker",
            "RUNLOG.md",
            "Completion or readiness claim lacks current agentic workflow evidence.",
            ["current commands", "current evals", "runtime/manual evidence", "accepted gaps"],
            residual="Inspection-only review can be mistaken for completed work.",
        )
    if any(claim in intent for claim in UNSUPPORTED_AGENTIC_CLAIMS):
        add(
            "unsupported_agentic_claims_rejected",
            "P1_high_risk",
            "model-reasoning-policy.md",
            "Unsupported Codex workflow claim was used as evidence.",
            ["claim", "source status", "verification status", "replacement evidence"],
            residual="Agentic workflow myths can bypass evidence and approval gates.",
        )

    return recommendations


def _frontend_recommendations(
    files: set[str],
    observed: list[dict[str, Any]],
    intent: str,
) -> list[dict[str, Any]]:
    if not _frontend_applies(observed, intent):
        return []

    recommendations: list[dict[str, Any]] = []

    def add(
        gate: str,
        priority: str,
        artifact: str,
        reason: str,
        evidence: list[str],
        *,
        owner: str = "UI owner",
        approval: str = "not required for read-only audit; approval_required before external browser, visual service or production-data actions",
        gap: str = "explicit_gap_accepted with owner, reason, residual risk and review date",
        residual: str = "UI behavior can be claimed complete without user-observable browser evidence.",
        action: str = "Stage the frontend artifact or accepted gap before claiming UI completion.",
    ) -> None:
        recommendations.append(
            _recommendation(
                priority=priority,
                reason=reason,
                domain="frontend",
                gate=gate,
                artifact=artifact,
                evidence_required=evidence,
                evidence_owner=owner,
                approval_boundary=approval,
                accepted_gap_option=gap,
                residual_risk=residual,
                safe_next_action=action,
            )
        )

    add(
        "frontend_user_flow_acceptance_present",
        "P0_blocker",
        "frontend-flow-spec.md",
        "Frontend work needs user flow, route/screen and acceptance scenario before implementation.",
        ["user goal", "route/screen", "acceptance scenario", "visible state path", "owner"],
        residual="UI can optimize component structure while the actual user flow remains vague.",
    )
    add(
        "frontend_component_state_matrix_present",
        "P1_high_risk",
        "frontend-state-matrix.md",
        "Frontend component or page work needs visible state coverage.",
        [
            "default/loading/skeleton",
            "empty/error/validation error",
            "disabled/success/focus",
            "long-content/responsive states",
            "state ownership",
        ],
        residual="Missing state coverage hides loading, empty, error, focus or long-content regressions.",
    )
    add(
        "frontend_component_docs_present",
        "P1_high_risk",
        "component-card.md",
        "Reusable UI or design-system work needs component documentation or an explicit docs gap.",
        ["component card", "Storybook story", "Autodocs/MDX note", "state coverage", "owner"],
        residual="Reusable UI can be shipped without stable usage, state or ownership documentation.",
    )
    add(
        "frontend_design_system_boundary_present",
        "P1_high_risk",
        "component-card.md",
        "Design-system changes need reuse or extension decision and owner review.",
        [
            "existing primitive reuse",
            "token owner",
            "variant policy",
            "icon/typography/spacing/theme rule",
            "breaking component API migration notes",
        ],
        owner="design-system owner",
        residual="Unowned tokens, variants or primitives can drift from product and brand constraints.",
    )
    add(
        "frontend_fsd_boundary_reviewed",
        "P2_recommended",
        "component-card.md",
        "FSD or growing UI structure needs boundary review when it applies.",
        ["layer", "slice", "segment", "public API", "import direction", "not applicable reason"],
        residual="Folders can imitate Feature-Sliced Design while imports and public APIs remain tangled.",
    )
    add(
        "frontend_api_contract_alignment_present",
        "P1_high_risk",
        "frontend-flow-spec.md",
        "UI data dependencies need contract examples, auth, permission, cache and error mapping.",
        ["endpoint/query/mutation", "contract examples", "auth/permission", "error shape", "cache/stale/pagination"],
        owner="API and UI owners",
        residual="UI can assume ideal data and miss permission, stale, loading or error states.",
    )
    add(
        "frontend_accessibility_review_present",
        "P1_high_risk",
        "frontend-accessibility-review.md",
        "Interactive or public UI needs accessibility review beyond scanner output.",
        ["WCAG 2.2 AA target or accepted exception", "semantic controls", "labels/names", "errors", "contrast"],
        owner="accessibility owner",
        residual="Automated checks can miss keyboard, semantic and error-announcement behavior.",
    )
    add(
        "frontend_keyboard_focus_contract_present",
        "P1_high_risk",
        "frontend-accessibility-review.md",
        "Interactive UI needs keyboard and focus behavior specified or marked as gap.",
        ["tab order", "visible focus", "focus trap/release", "escape behavior", "modal/menu/listbox/dialog behavior"],
        owner="accessibility owner",
        residual="Keyboard users can be blocked even when visual UI looks complete.",
    )
    add(
        "frontend_responsive_viewport_matrix_present",
        "P1_high_risk",
        "frontend-visual-qa.md",
        "Layout or visual work needs responsive viewport evidence.",
        ["mobile viewport", "desktop viewport", "orientation", "input modality", "reduced motion/preferences", "theme"],
        residual="Desktop-only screenshots can hide mobile, input and preference regressions.",
    )
    add(
        "frontend_visual_evidence_present",
        "P1_high_risk",
        "frontend-visual-qa.md",
        "Visual UI work needs privacy-safe screenshot, baseline or explicit gap.",
        [
            "screenshot/story baseline",
            "browser/OS/viewport",
            "baseline owner",
            "known noisy diffs",
            "privacy-safe mock data",
        ],
        approval="approval_required before external visual service, hosted screenshot upload or production-data screenshot",
        residual="Visual regressions can ship without deterministic or reviewable evidence.",
    )
    add(
        "frontend_runtime_console_evidence_present",
        "P0_blocker",
        "frontend-visual-qa.md",
        "UI completion requires current browser/runtime evidence or explicit verification gap.",
        ["dev-server or preview URL/context", "browser/OS", "console status", "network/runtime errors", "Playwright trace"],
        residual="Code inspection cannot prove the UI renders, runs or has no relevant console/runtime errors.",
    )
    add(
        "frontend_interaction_test_evidence_present",
        "P1_high_risk",
        "test-eval-matrix.md",
        "Interaction changes need user-observable test or manual interaction evidence.",
        ["role/name query", "keyboard input", "click/tap", "form submit", "async state assertion"],
        owner="tester",
        residual="Implementation-oriented checks can miss observable user behavior.",
    )
    add(
        "frontend_performance_budget_present",
        "P1_high_risk",
        "frontend-performance-budget.md",
        "User-facing or interaction-heavy routes need Web Vitals budget or non-applicability.",
        ["LCP target", "INP target", "CLS target", "measurement path", "lab vs field/RUM status"],
        owner="performance owner",
        residual="Lab metrics can be mistaken for production UX and performance can regress late.",
    )
    add(
        "frontend_browser_support_present",
        "P2_recommended",
        "frontend-visual-qa.md",
        "Public UI needs supported browsers/devices or known gaps named.",
        ["supported browsers", "devices/webviews", "Playwright projects", "known gaps", "fallback"],
        residual="Browser-specific behavior can fail outside the developer's default browser.",
    )
    add(
        "frontend_content_i18n_boundary_present",
        "P2_recommended",
        "frontend-flow-spec.md",
        "Long text, localization or user-generated content needs layout and i18n assumptions recorded.",
        ["long text", "wrapping/truncation", "localization", "pluralization", "RTL/locales", "non-overlap assumptions"],
        owner="product copy or i18n owner",
        residual="Content variants can break layout or meaning after implementation appears complete.",
    )

    if _mentions_any(intent, UNSUPPORTED_FRONTEND_CLAIMS):
        add(
            "unsupported_frontend_claims_rejected",
            "P1_high_risk",
            "frontend-visual-qa.md",
            "Unsupported frontend methodology claim was used as evidence.",
            ["claim", "source status", "verification status", "replacement frontend evidence"],
            residual="Frontend myths can bypass browser, accessibility, responsive or owner-review evidence.",
            action="Record the unsupported claim and replace it with frontend evidence or an accepted gap.",
        )

    return recommendations


def _backend_recommendations(
    files: set[str],
    observed: list[dict[str, Any]],
    intent: str,
) -> list[dict[str, Any]]:
    if not _backend_applies(observed, intent):
        return []

    recommendations: list[dict[str, Any]] = []
    severity_mode = _backend_severity_mode(intent)
    accepted_gap_recorded = _backend_has_complete_accepted_gap(intent)
    blocker_priority = "P2_recommended" if severity_mode == "lightweight" else "P0_blocker"
    high_risk_priority = "P3_optional_maturity" if severity_mode == "lightweight" else "P1_high_risk"
    accepted_gap_priority = "P2_recommended" if accepted_gap_recorded else high_risk_priority
    accepted_gap_reason = (
        " Accepted gap downgrade applies because owner, reason, review date, downstream risk and follow-up are recorded."
        if accepted_gap_recorded
        else ""
    )

    def add(
        gate: str,
        priority: str,
        artifact: str,
        reason: str,
        evidence: list[str],
        *,
        owner: str = "backend owner",
        approval: str = "not required for read-only audit; approval_required before production data, external writes, secrets or deploy actions",
        gap: str = "explicit_gap_accepted with owner, reason, residual risk and review date",
        residual: str = "Backend behavior can be claimed complete without runtime, failure or owner-reviewed evidence.",
        action: str = "Stage the backend artifact or accepted gap before claiming backend completion.",
    ) -> None:
        recommendations.append(
            _recommendation(
                priority=priority,
                reason=reason,
                domain="backend",
                gate=gate,
                artifact=artifact,
                evidence_required=evidence,
                evidence_owner=owner,
                approval_boundary=approval,
                accepted_gap_option=gap,
                residual_risk=residual,
                safe_next_action=action,
            )
        )

    add(
        "backend_service_boundary_present",
        blocker_priority,
        "backend-service-overview.md",
        "Backend work needs service/module boundary, owner, contracts, dependencies, data ownership and runtime shape.",
        [
            "changed backend responsibility",
            "service/user behavior",
            "affected backend unit",
            "purpose",
            "owner",
            "inbound contracts",
            "outbound dependencies",
            "data stores",
            "data ownership",
            "deployment/runtime shape",
            "operational assumptions",
            "modular monolith default",
            "microservice rationale",
            "independent deploy/scale/team/ownership evidence",
            "owner review",
            "ADR",
            "decision authority",
            "boundary rationale",
            "ADR link or accepted gap",
            "ports/adapters boundary",
            "domain logic independent from HTTP/DB/queue/vendor SDK",
            "Twelve-Factor vocabulary",
            "explicit dependencies",
            "APIs/events/external providers",
            "OpenAPI/AsyncAPI/Pact/protobuf/provider contracts where applicable",
            "contract changes synced with code and tests",
        ],
        residual="Package or service names can hide unclear ownership and runtime boundaries.",
    )
    add(
        "backend_runtime_behavior_present",
        blocker_priority,
        "backend-runtime-behavior.md",
        "Backend runtime behavior needs retries, timeouts, idempotency, ordering, replay and failure modes documented.",
        [
            "jobs/queues/remote calls",
            "timeout",
            "backoff/max attempts",
            "idempotency",
            "deduplication",
            "ordering",
            "backpressure",
            "poison message",
            "replay/recovery",
            "process model",
            "admin tasks",
            "logs-as-event-stream",
            "stateless process or accepted gap",
            "lightweight read-only retry/idempotency signals",
            "dependency/job context",
            "deeper static analysis deferred",
            "avoid false positives",
        ],
        residual="Retries, workers or distributed behavior can amplify failures without idempotency and replay evidence.",
    )
    add(
        "backend_dependency_failure_matrix_present",
        high_risk_priority,
        "backend-dependency-failure-matrix.md",
        "Remote dependencies need timeout, retry, circuit breaker or non-applicability, fallback, alert and owner policy.",
        [
            "per dependency",
            "timeout",
            "retry/backoff/max attempts",
            "circuit breaker non-applicability",
            "fallback",
            "alert owner",
            "verification evidence",
        ],
        residual="A backend dependency can fail in production with no bounded failure policy.",
    )
    add(
        "backend_observability_contract_present",
        accepted_gap_priority,
        "backend-observability-map.md",
        "Backend runtime changes need traces, metrics, logs, dashboards, alerts, correlation IDs and redaction notes."
        + accepted_gap_reason,
        [
            "traces",
            "metrics",
            "logs",
            "dashboards",
            "alerts",
            "correlation IDs",
            "redaction/no-secrets",
            "context propagation",
            "semantic conventions or accepted gaps",
            "collector/instrumentation notes",
            "redaction policy",
            "alert ownership",
            "no-private-payload logging",
            "logs alone are not accepted as observability",
        ],
        residual="Logs alone cannot prove observability or safe production debugging.",
    )
    add(
        "backend_slo_or_gap_present",
        accepted_gap_priority,
        "backend-slo-sheet.md",
        "Production or user-facing backend needs SLI/SLO or explicit no-telemetry/not-yet-production gap."
        + accepted_gap_reason,
        [
            "SLI/SLO or explicit gap",
            "user journey",
            "user-relevant SLI",
            "SLO target",
            "measurement window",
            "alert policy",
            "owner",
            "no-telemetry or not-yet-production gap",
        ],
        residual="Reliability expectations can remain implicit until incidents expose them.",
    )
    add(
        "backend_health_probe_contract_present",
        accepted_gap_priority,
        "backend-health-check-contract.md",
        "Deployable backend needs health semantics and verification or a platform-unavailable gap."
        + accepted_gap_reason,
        [
            "health endpoint semantics",
            "liveness",
            "readiness",
            "startup",
            "platform equivalent",
            "test evidence or accepted gap",
            "platform-unavailable gap",
            "tested where platform/runtime is available",
            "platform-unavailable gap owner",
            "platform-unavailable gap reason",
            "platform-unavailable follow-up",
            "documentation alone is not sufficient",
        ],
        residual="A vague health endpoint can route traffic to an alive but not ready service.",
    )
    add(
        "backend_job_queue_contract_present",
        high_risk_priority,
        "backend-job-queue-contract.md",
        "Jobs, queues, consumers or schedulers need payload, retry, DLQ, idempotency and replay contract.",
        [
            "queue/job",
            "producer",
            "consumer",
            "payload contract",
            "retry policy",
            "dead-letter behavior",
            "dead-letter queue",
            "idempotency key",
            "replay procedure",
            "poison-message handling",
        ],
        residual="Duplicate or poison messages can corrupt state without dedupe and recovery procedures.",
    )
    add(
        "backend_data_consistency_strategy_present",
        high_risk_priority,
        "backend-data-consistency-record.md",
        "Distributed data behavior needs transaction boundary, consistency model, outbox/saga/compensation and recovery path.",
        [
            "local transaction",
            "transaction boundary",
            "consistency model",
            "outbox",
            "saga",
            "compensation",
            "monitoring",
            "reconciliation",
            "migration impact",
            "recovery path",
        ],
        owner="backend and data owners",
        residual="Distributed workflow can partially commit without compensation or reconciliation evidence.",
    )
    add(
        "backend_config_secrets_boundary_present",
        high_risk_priority,
        "backend-config-secrets-manifest.md",
        "Backend config and secrets need manifest without values, secret source, rotation and local/prod parity.",
        [
            "config/env keys without values",
            "secret source",
            "rotation notes",
            "local/prod parity",
            "required/optional",
            "required/optional status",
            "authn/authz config",
            "tokens",
            "PII",
            "explicit dependencies",
            "build-release-run boundary",
            "dev/prod parity",
            "no-secrets/no-private-data constraints",
            "docs, prompts, fixtures, logs and examples",
        ],
        residual=(
            "Secrets or environment assumptions can leak into docs, prompts, fixtures and logs, "
            "or expose production payloads and private customer data."
        ),
    )
    add(
        "backend_security_reviewed",
        high_risk_priority,
        "security-risk-review.md",
        "Security-sensitive backend behavior needs authn/authz, secrets, rate limits, audit logging and abuse-case review.",
        [
            "authn/authz",
            "tokens",
            "PII",
            "money movement",
            "privileged operations",
            "external writes",
            "irreversible side effects",
            "secrets",
            "rate limits",
            "audit logging",
            "sensitive data",
            "abuse cases",
            "no-secrets evidence",
        ],
        owner="security or backend owner",
        approval="approval_required before touching auth, secrets, PII, money movement, privileged operations or external writes",
        residual="Security-sensitive backend behavior can ship without explicit risk ownership.",
    )
    add(
        "backend_rollback_plan_present",
        high_risk_priority,
        "backend-release-rollback-notes.md",
        "Risky backend changes need rollback trigger, migration/feature flag plan, replay and data recovery path.",
        [
            "rollback trigger",
            "feature flag",
            "migration",
            "rollback command or manual procedure",
            "rollback/no-rollback rationale",
            "verification command",
            "data recovery/replay",
            "irreversible side effects",
            "owner approval",
            "residual risk",
            "contract changes synced with code/tests where applicable",
        ],
        owner="backend and release owners",
        residual="Production backend changes can become irreversible without rollback, recovery or replay evidence.",
    )
    add(
        "backend_evidence_sufficiency_owner_reviewed",
        high_risk_priority,
        "EVALS.md",
        "Backend completion evidence needs human owner review of test/eval/runtime sufficiency for real project risk.",
        [
            "owner reviewed test/eval/runtime evidence sufficiency",
            "real project risk",
            "accepted gap owner",
            "accepted gap reason",
            "review date",
            "downstream risk",
            "follow-up",
            "T9-S",
            "cross-domain semantic sufficiency backlog",
        ],
        owner="human owner and backend owner",
        residual=(
            "A backend route can prove evidence shape without proving the human owner accepted that the "
            "specific checks are sufficient for this project's production risk."
        ),
        action="Record owner-reviewed evidence sufficiency in EVALS/RUNLOG or route the gap to T9-S.",
    )

    if _mentions_any(intent, UNSUPPORTED_BACKEND_CLAIMS):
        add(
            "unsupported_backend_claims_rejected",
            "P1_high_risk",
            "backend-service-overview.md",
            "Unsupported backend methodology claim was used as evidence.",
            ["claim", "source status", "verification status", "replacement backend evidence"],
            residual="Backend myths can bypass runtime, failure-mode, observability, SLO or owner-review evidence.",
            action="Record the unsupported claim and replace it with backend evidence or an accepted gap.",
        )

    return recommendations


def _recommendations(
    root: Path,
    files: set[str],
    directories: set[str],
    observed: list[dict[str, Any]],
    intent: str,
    complexity_profile: str,
) -> list[dict[str, Any]]:
    recommendations: list[dict[str, Any]] = []
    recommendations.extend(_business_product_recommendations(files, intent))
    recommendations.extend(_requirements_domain_recommendations(files, intent))
    recommendations.extend(_solution_architecture_recommendations(files, observed, intent, complexity_profile))
    recommendations.extend(_quality_testing_evals_recommendations(root, files, observed, intent, complexity_profile))
    recommendations.extend(_codex_agentic_workflow_recommendations(files, observed, intent))
    recommendations.extend(_frontend_recommendations(files, observed, intent))
    recommendations.extend(_backend_recommendations(files, observed, intent))
    if _has_any_signal(observed, {"openapi_contract", "asyncapi_contract", "graphql_schema", "protobuf_schema"}) and not _has_contract_tests(files):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="API contract signals exist without contract test evidence.",
                domain="api_integrations",
                gate="api_contract_source_present",
                artifact="api-contract-review.md",
                evidence_required=["contract source", "consumer impact", "contract test command", "compatibility notes"],
                evidence_owner="API owner",
                approval_boundary="approval_required before external API writes or breaking contract changes",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="A contract file does not prove consumers remain compatible.",
                safe_next_action="Stage an API contract review before changing implementation or release behavior.",
            )
        )
    if _has_signal(observed, "database_migration_or_schema"):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Database migration or schema signals were detected.",
                domain="database_data",
                gate="database_migration_plan_present",
                artifact="database-migration-plan.md",
                evidence_required=["ordered migration steps", "dry run command", "rollback or compensation", "owner approval"],
                evidence_owner="data owner",
                approval_boundary="approval_required before production database access or migration execution",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="Artifact presence does not prove the migration is safe.",
                safe_next_action="Stage a migration plan proposal without connecting to production data.",
            )
        )
    if complexity_profile == "high_risk":
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="High-risk security, privacy, payment, compliance or sensitive-data intent was detected.",
                domain="security_privacy_compliance",
                gate="security_risk_review_present",
                artifact="security-risk-review.md",
                evidence_required=["threat surface", "auth or data impact", "tests", "rollback", "owner review"],
                evidence_owner="security or product owner",
                approval_boundary="approval_required before touching secrets, payment, auth, PII or production data",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="Intent classification does not prove all security requirements are known.",
                safe_next_action="Stage a security risk review and list unknowns before implementation.",
            )
        )
    if _mentions_any(intent, DELIVERY_INTENT_TERMS) or _has_any_signal(
        observed,
        {"ci_configuration", "deployment_configuration", "release_file"},
    ):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Production, release, CI or deployment signals were detected.",
                domain="delivery_release_operations",
                gate="release_evidence_present",
                artifact="release-readiness.md",
                evidence_required=["build command", "test evidence", "artifact manifest", "rollback", "owner approval"],
                evidence_owner="release operator",
                approval_boundary="approval_required before publish, tag, deploy or release creation",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="CI or deployment files do not prove the release is ready.",
                safe_next_action="Stage release readiness evidence before external release actions.",
            )
        )
    return recommendations


def _recommendation(
    *,
    priority: str,
    reason: str,
    domain: str,
    gate: str,
    artifact: str,
    evidence_required: list[str],
    evidence_owner: str,
    approval_boundary: str,
    accepted_gap_option: str,
    residual_risk: str,
    safe_next_action: str,
) -> dict[str, Any]:
    return {
        "priority": priority,
        "reason": reason,
        "domain": domain,
        "gate": gate,
        "artifact": artifact,
        "evidence_required": evidence_required,
        "evidence_owner": evidence_owner,
        "approval_boundary": approval_boundary,
        "accepted_gap_option": accepted_gap_option,
        "residual_risk": residual_risk,
        "safe_next_action": safe_next_action,
    }


def _prioritize_recommendations(recommendations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        recommendations,
        key=lambda recommendation: (
            PRIORITY_ORDER.get(str(recommendation.get("priority", "not_applicable")), 99),
            str(recommendation.get("domain", "")),
            str(recommendation.get("gate", "")),
        ),
    )


def _delivery_map(
    files: set[str],
    directories: set[str],
    observed: list[dict[str, Any]],
    methodology_domains: list[dict[str, Any]],
    recommendations: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "surface_map": {
            "ui": _has_any_signal(observed, {"stack_manifest"}) and bool(files & {"package.json"}),
            "api": _has_any_signal(observed, {"openapi_contract", "asyncapi_contract", "graphql_schema", "protobuf_schema"}),
            "data": _has_signal(observed, "database_migration_or_schema"),
            "ai": _has_signal(observed, "ai_eval_or_rag"),
            "delivery": _has_any_signal(observed, {"ci_configuration", "deployment_configuration"}),
        },
        "system_map": {
            "files_observed": len(files),
            "directories_observed": len(directories),
            "control_plane_present": [name for name in CONTROL_PLANE_FILES if name.lower() in files],
        },
        "lifecycle_map": {
            "write_policy": "read_only",
            "artifact_strategy": "stage proposals before workspace writes",
        },
        "methodology_map": {
            packet["id"]: packet["status"]
            for packet in methodology_domains
            if packet["status"] != "not_applicable"
        },
        "next_action_map": [recommendation["safe_next_action"] for recommendation in recommendations[:5]],
    }


def _unknowns(files: set[str], directories: set[str], observed: list[dict[str, Any]]) -> list[str]:
    unknowns: list[str] = []
    if not _has_test_signal(files, observed):
        unknowns.append("current verification command")
    if not any(name in files for name in {"requirements.md", "plan.md"}):
        unknowns.append("accepted scope and implementation plan")
    if directories or files:
        unknowns.append("artifact owners and approval boundaries")
    return unknowns


def _questions_for_owner(
    files: set[str],
    directories: set[str],
    observed: list[dict[str, Any]],
    recommendations: list[dict[str, Any]],
) -> list[str]:
    questions = ["What is the smallest safe next artifact to stage?"]
    if not _has_test_signal(files, observed):
        questions.append("Which local command is the source of truth for verification?")
    if recommendations:
        questions.append("Who owns the highest-priority missing methodology gate?")
    if directories or files:
        questions.append("Which detected surfaces are in scope for this slice?")
    return questions


def _provisional_assumptions(files: set[str], intent: str) -> list[str]:
    assumptions = ["Audit is read-only and does not approve workspace writes."]
    if not files:
        assumptions.append("Empty workspace means methodology recommendations are provisional.")
    if intent:
        assumptions.append("Intent hint is routing context, not observed repository evidence.")
    return assumptions


def _safe_next_action(recommendations: list[dict[str, Any]]) -> str:
    if recommendations:
        return recommendations[0]["safe_next_action"]
    return "Record methodology audit output and proceed only with evidence-backed planning."


def _observed_domain_ids(observed: list[dict[str, Any]]) -> set[str]:
    mapping = {
        "test_evidence": "quality_testing_evals",
        "test_command": "quality_testing_evals",
        "quality_testing_signal": "quality_testing_evals",
        "openapi_contract": "api_integrations",
        "asyncapi_contract": "api_integrations",
        "graphql_schema": "api_integrations",
        "protobuf_schema": "api_integrations",
        "database_migration_or_schema": "database_data",
        "ai_eval_or_rag": "llm_ai_rag",
        "ci_configuration": "delivery_release_operations",
        "deployment_configuration": "delivery_release_operations",
        "release_file": "delivery_release_operations",
        "codex_agentic_workflow": "codex_agentic_workflow",
        "backend": "backend",
        "frontend": "frontend",
    }
    return {mapping[signal["id"]] for signal in observed if signal["id"] in mapping}


def _has_package_test_script(root: Path) -> bool:
    package_file = root / "package.json"
    if not package_file.is_file():
        return False
    try:
        data = json.loads(package_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    scripts = data.get("scripts") if isinstance(data, dict) else None
    return isinstance(scripts, dict) and isinstance(scripts.get("test"), str) and bool(scripts["test"].strip())


def _has_test_command_or_evidence(root: Path, files: set[str], observed: list[dict[str, Any]]) -> bool:
    return _has_test_signal(files, observed) or _has_package_test_script(root)


def _has_test_signal(files: set[str], observed: list[dict[str, Any]]) -> bool:
    return _has_any_signal(observed, {"test_evidence", "test_command"}) or any(
        "test" in path or path.startswith("evals/") for path in files
    )


def _has_contract_tests(files: set[str]) -> bool:
    return any("contract" in path and "test" in path for path in files)


def _has_architecture_diagram(files: set[str]) -> bool:
    return any(path.endswith(ARCHITECTURE_DIAGRAM_SUFFIXES) for path in files)


def _artifact_present(files: set[str], name: str) -> bool:
    return any(path == name or path.endswith(f"/{name}") for path in files)


def _has_signal(observed: list[dict[str, Any]], signal_id: str) -> bool:
    return any(signal["id"] == signal_id for signal in observed)


def _has_any_signal(observed: list[dict[str, Any]], signal_ids: set[str]) -> bool:
    return any(signal["id"] in signal_ids for signal in observed)


def _mentions_any(text: str, terms: set[str]) -> bool:
    return any(term in text for term in terms)


def _is_openapi(path: str) -> bool:
    return path in OPENAPI_MARKERS or path.startswith("openapi/") or path.endswith(("/openapi.yaml", "/openapi.yml", "/openapi.json"))


def _is_asyncapi(path: str) -> bool:
    return path in ASYNCAPI_MARKERS or path.startswith("asyncapi/") or path.endswith(("/asyncapi.yaml", "/asyncapi.yml", "/asyncapi.json"))
