from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from product_agent_os.contracts import CONTROL_PLANE_FILES
from product_agent_os.methodology_audit import build_methodology_audit


FIRST_RESPONSE_CONTRACT = [
    "mode",
    "confidence",
    "next smallest action",
    "minimum artifacts",
    "evidence gaps",
    "approval boundary",
]

DOCS_AS_CODE_IMPACT_STATUSES = [
    "not_applicable",
    "present_unverified",
    "present_verified",
    "proposal_staged",
    "explicit_gap_accepted",
    "approval_required",
]

READINESS_STATUSES = [
    "not_applicable",
    "applicable_missing",
    "present_unverified",
    "present_verified",
    "proposal_staged",
    "explicit_gap_accepted",
    "approval_required",
]

MODE_MINIMUM_ARTIFACTS = {
    "bug_rescue": ["bug rescue report", "reproduction evidence"],
    "greenfield_idea": ["greenfield idea brief", "approval before scaffold", "approval boundary"],
    "complex_system_acceleration": ["integration catalog", "ownership split", "agent task packet", "release gates"],
    "pr_review": ["pr review readiness", "pr risk review", "changed files map"],
    "legacy_onboarding": ["onboarding map", "source map", "verification status map"],
    "api_migration": ["migration plan", "api contract review"],
    "ai_eval_regression": ["ai eval spec", "baseline result"],
    "native_mobile_feature": ["acceptance scenarios", "platform runtime check"],
    "desktop_local_first": ["local data risk note", "runtime log check"],
    "data_migration": ["migration plan", "database dictionary"],
    "security_sensitive_change": ["security risk review", "approval boundary"],
    "ci_stabilization": ["ci stabilization report", "failure evidence"],
    "release_packaging": ["release readiness", "finish options"],
    "standard_feature": ["workspace audit packet", "implementation plan"],
    "docs_only": ["docs tooling decision", "docs check"],
    "maintenance": ["workspace audit packet", "risk review note"],
}

MODE_BEHAVIORAL_CASES = {
    "bug_rescue": [
        "first-run-broken-bug-rescue",
        "bug-rescue-root-cause",
        "bug-rescue-no-broad-rewrite",
        "bug-rescue-no-repro-stop",
    ],
    "greenfield_idea": [
        "first-run-response",
        "first-run-empty-greenfield",
        "greenfield-no-scaffold-before-approval",
        "greenfield-lightweight-mode",
    ],
    "complex_system_acceleration": [
        "first-run-complex-system",
        "fresh-context-handoff",
        "cost-model-budget",
        "complex-ownership-split",
        "complex-no-overparallelization",
    ],
    "pr_review": ["pr-review-readiness", "two-stage-review"],
    "legacy_onboarding": ["legacy-onboarding-map"],
    "api_migration": ["api-migration-plan", "two-stage-review"],
    "ai_eval_regression": ["ai-eval-regression-plan"],
    "native_mobile_feature": ["native-mobile-runtime-plan"],
    "desktop_local_first": ["desktop-local-runtime-plan"],
    "data_migration": ["data-migration-plan"],
    "security_sensitive_change": ["security-sensitive-change-plan"],
    "ci_stabilization": ["ci-stabilization-plan"],
    "release_packaging": ["release-packaging-readiness", "finish-options"],
    "standard_feature": ["route-selection"],
    "docs_only": ["route-selection"],
    "maintenance": ["first-run-existing-control-plane", "route-selection"],
}

STACK_MARKERS = {
    "package.json": "node",
    "pyproject.toml": "python",
    "requirements.txt": "python",
    "mkdocs.yml": "docs",
    "Cargo.toml": "rust",
    "go.mod": "go",
}

IGNORED_DIR_NAMES = {
    ".git",
    ".angular",
    ".cache",
    ".codex-cache",
    ".docusaurus",
    ".eggs",
    ".gradle",
    ".hypothesis",
    ".mypy_cache",
    ".next",
    ".nox",
    ".nuxt",
    ".parcel-cache",
    ".pytest_cache",
    ".ruff_cache",
    ".svelte-kit",
    ".tox",
    ".turbo",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "htmlcov",
    "node_modules",
    "site",
    "target",
    "vendor",
    "venv",
}

BUG_EVIDENCE_FILE_NAMES = {
    "runlog.md",
    "test-results.log",
    "pytest.log",
    "npm-debug.log",
}

BUG_EVIDENCE_PATH_TERMS = (
    "failed-verification",
    "junit",
    "pytest",
    "test-result",
    "test_results",
)

BUG_FAILURE_TERMS = (
    "exit_code: 1",
    "exit code 1",
    "failed test",
    "tests failed",
    "verification failed",
    "assertionerror",
    "traceback",
)


def _relative_files(root: Path) -> set[str]:
    files: set[str] = set()
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in IGNORED_DIR_NAMES]
        current_path = Path(current_root)
        for filename in filenames:
            try:
                files.add((current_path / filename).relative_to(root).as_posix())
            except ValueError:
                continue
    release_artifact_root = root / "dist"
    if release_artifact_root.is_dir():
        for candidate in release_artifact_root.iterdir():
            relative_candidate = f"dist/{candidate.name}"
            if candidate.is_file() and _is_release_artifact_source(relative_candidate):
                try:
                    files.add(candidate.relative_to(root).as_posix())
                except ValueError:
                    continue
    return files


def _detect_stack(files: set[str]) -> list[str]:
    stack: list[str] = []
    for marker, name in STACK_MARKERS.items():
        if marker in files and name not in stack:
            stack.append(name)
    if any(path.startswith("packages/") for path in files):
        stack.append("monorepo")
    return stack


def _has_any(files: set[str], predicates: list[str]) -> bool:
    return any(any(predicate in path.lower() for predicate in predicates) for path in files)


def _detect_fsd_structure(files: set[str]) -> bool:
    lowered = {path.lower().replace("\\", "/") for path in files}
    native_markers = (
        "android/",
        "ios/",
        "app.json",
        "app.config.js",
        "app.config.ts",
    )
    if any(path.startswith(native_markers) for path in lowered):
        return False

    fsd_layers = {"app", "pages", "widgets", "features", "entities", "shared"}
    frontend_extensions = (".tsx", ".jsx", ".vue", ".svelte", ".ts", ".js")
    component_extensions = (".tsx", ".jsx", ".vue", ".svelte")
    detected_layers: set[str] = set()
    has_component_file = False

    for path in lowered:
        if not path.endswith(frontend_extensions):
            continue
        parts = path.split("/")
        layer = None
        if parts and parts[0] in fsd_layers and len(parts) >= 2:
            layer = parts[0]
        if "src" in parts:
            src_index = parts.index("src")
            if len(parts) > src_index + 1 and parts[src_index + 1] in fsd_layers:
                layer = parts[src_index + 1]
        if layer is None:
            continue
        detected_layers.add(layer)
        if path.endswith(component_extensions):
            has_component_file = True

    return has_component_file and len(detected_layers) >= 4


def _detect_frontend_signal(files: set[str]) -> bool:
    lowered = {path.lower().replace("\\", "/") for path in files}
    if any(path.startswith(("android/", "ios/")) for path in lowered):
        return False

    directory_prefixes = (
        "app/",
        "pages/",
        "routes/",
        "components/",
        "widgets/",
        "features/",
        "entities/",
        "shared/ui/",
        "stories/",
        ".storybook/",
        "e2e/",
        "tests/playwright/",
        "src/app/",
        "src/pages/",
        "src/routes/",
        "src/components/",
        "src/widgets/",
        "src/features/",
        "src/entities/",
        "src/shared/ui/",
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
    frontend_extensions = (".tsx", ".jsx", ".vue", ".svelte", ".css", ".scss")
    return any(
        path in exact_files
        or path.startswith(directory_prefixes)
        or any(fragment in path for fragment in fragments)
        or path.endswith(frontend_extensions)
        for path in lowered
    )


def _detect_backend_signal(files: set[str]) -> bool:
    lowered = {path.lower().replace("\\", "/") for path in files}
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
        "workers/",
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
    )
    exact_files = {
        "dockerfile",
        "docker-compose.yml",
        "procfile",
        "serverless.yml",
        "openapi.yaml",
        "openapi.yml",
        "openapi.json",
        "asyncapi.yaml",
        "asyncapi.yml",
        "asyncapi.json",
    }
    fragments = (
        "backend",
        "celery",
        "consumer",
        "controller",
        "django",
        "fastapi",
        "flask",
        "grpc",
        "health",
        "idempotency",
        "job",
        "liveness",
        "queue",
        "readiness",
        "repository",
        "retry",
        "runbook",
        "scheduler",
        "service",
        "slo",
        "spring",
        "worker",
    )
    return any(
        path in exact_files
        or path.startswith(directory_prefixes)
        or path.endswith((".proto", "/openapi.yaml", "/openapi.yml", "/openapi.json", "/asyncapi.yaml", "/asyncapi.yml"))
        or any(fragment in path for fragment in fragments)
        for path in lowered
    )


def _detect_methodology_signals(files: set[str], profile: dict[str, Any]) -> dict[str, bool]:
    lowered = {path.lower() for path in files}
    ci_present = bool(profile.get("drivers", {}).get("ci_present")) if isinstance(profile, dict) else False
    return {
        "architecture_docs": any(
            path.startswith("docs/architecture/")
            or path.startswith("architecture/")
            or path in {"architecture.md", "docs/architecture.md"}
            for path in lowered
        ),
        "adr": any(
            path.startswith("docs/adr/")
            or path.startswith("adr/")
            or "/adr/" in path
            or path.endswith("/adrs.md")
            for path in lowered
        ),
        "openapi": any(
            path.startswith("openapi/")
            or path.endswith("swagger.yaml")
            or path.endswith("swagger.yml")
            or path.endswith("swagger.json")
            or path.endswith("openapi.yaml")
            or path.endswith("openapi.yml")
            or path.endswith("openapi.json")
            for path in lowered
        ),
        "asyncapi": any(
            path.startswith("asyncapi/")
            or path.endswith("asyncapi.yaml")
            or path.endswith("asyncapi.yml")
            or path.endswith("asyncapi.json")
            for path in lowered
        ),
        "graphql_schema": any(path.endswith((".graphql", ".graphqls")) for path in lowered),
        "protobuf_schema": any(path.endswith(".proto") for path in lowered),
        "json_schema": any(_is_json_schema_source(path) for path in lowered),
        "pact_contract": any(_is_pact_source(path) for path in lowered),
        "api_external_provider": any(_is_external_provider_source(path) for path in lowered),
        "api_generated_client": any(_is_generated_client_source(path) for path in lowered),
        "api_webhook_event": any(_is_webhook_event_source(path) for path in lowered),
        "storybook": any(
            path.startswith(".storybook/")
            or ".stories." in path
            or ".story." in path
            for path in lowered
        ),
        "frontend": _detect_frontend_signal(files),
        "backend": _detect_backend_signal(files),
        "fsd_structure": _detect_fsd_structure(files),
        "database_docs": any(_is_database_data_source(path) for path in lowered),
        "database_data": any(_is_database_data_source(path) for path in lowered),
        "domain_model": _has_domain_model_signal(lowered),
        "docs_portal": any(
            path in {"mkdocs.yml", "docusaurus.config.js", "docusaurus.config.ts", "antora-playbook.yml"}
            or path in {".readthedocs.yaml", "readthedocs.yaml", "readthedocs.yml"}
            or path.endswith("conf.py") and "docs" in path
            for path in lowered
        ),
        "docs_tooling_decision": _has_docs_tooling_signal(lowered),
        "codeowners": any(path == "codeowners" or path.endswith("/codeowners") for path in lowered),
        "ci": ci_present,
        "evals": any(
            path == "evals.md"
            or path.startswith("evals/")
            or path.startswith(".codex/evals/")
            or "promptfoo" in path
            for path in lowered
        ),
        "llm_ai_rag": _has_llm_ai_rag_signal(lowered),
        "quality_testing_evals": _has_quality_testing_signal(lowered, profile),
        "codex_agentic_workflow": _has_codex_agentic_workflow_signal(lowered),
        "metrics": _has_any(files, ["metrics", "analytics", "telemetry", "observability"]),
    }


def _has_codex_agentic_workflow_signal(lowered_files: set[str]) -> bool:
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
    terms = (
        "codex",
        "subagent",
        "skill",
        "mcp",
        "hook",
        "plugin",
        "automation",
        "approval boundary",
        "external write",
        "worktree",
        "handoff",
        "task packet",
    )
    return any(
        path in exact_files
        or path.startswith(directory_prefixes)
        or path.endswith("/skill.md")
        or path.endswith("/automation.toml")
        or path.endswith("/hooks.json")
        or path.endswith("/config.toml")
        or path.endswith("/agent-task-packet.md")
        or path.endswith("/handoff-contract.md")
        or path.endswith("/worktree-ownership.md")
        or any(term in path for term in terms)
        for path in lowered_files
    )


def _has_quality_testing_signal(lowered_files: set[str], profile: dict[str, Any]) -> bool:
    drivers = profile.get("drivers", {}) if isinstance(profile, dict) else {}
    if drivers.get("test_maturity") != "none":
        return True
    directory_prefixes = (
        "tests/",
        "test/",
        "spec/",
        "e2e/",
        "playwright/",
        "cypress/",
        "evals/",
        ".github/workflows/",
        "fixtures/",
        "__tests__/",
        "snapshots/",
    )
    exact_files = {
        "test.md",
        "evals.md",
        "runlog.md",
        "pytest.ini",
        "tox.ini",
        "promptfoo.yaml",
        "promptfooconfig.yaml",
        "openapi.yaml",
        "openapi.yml",
        "openapi.json",
        "asyncapi.yaml",
        "asyncapi.yml",
        "asyncapi.json",
    }
    name_fragments = (
        "vitest.config.",
        "jest.config.",
        "playwright.config.",
        "coverage",
        "pact",
        "junit",
        "pytest",
        "unittest",
        "testing-library",
        "storybook",
        "stryker",
        "hypothesis",
        "ragas",
        "codecov",
        "github actions",
        "flaky",
        "retry",
    )
    return any(
        path in exact_files
        or path.startswith(directory_prefixes)
        or any(fragment in path for fragment in name_fragments)
        for path in lowered_files
    )


def _has_docs_tooling_signal(lowered_files: set[str]) -> bool:
    return any(
        path in {
            "mkdocs.yml",
            "docusaurus.config.js",
            "docusaurus.config.ts",
            "antora-playbook.yml",
            ".readthedocs.yaml",
            "readthedocs.yaml",
            "readthedocs.yml",
            "typedoc.json",
            "jsdoc.json",
            ".markdownlint.json",
            ".markdownlint.yaml",
            ".vale.ini",
            "schemaspy.properties",
        }
        or path.endswith("conf.py") and "docs" in path
        or path.startswith(".storybook/")
        or ".stories." in path
        or path.startswith("openapi/")
        or path.startswith("asyncapi/")
        or path.endswith((".dbml", ".csproj"))
        or path.endswith((".mmd", ".mermaid", ".puml", ".plantuml", ".dsl"))
        or "structurizr" in path
        or path in {"docs/architecture.md", "architecture.md", "docs/diagrams.md"}
        for path in lowered_files
    )


def _has_domain_model_signal(lowered_files: set[str]) -> bool:
    explicit_files = {
        ".codex/artifact-templates/domain-modeling.md",
        "domain-modeling.md",
        "docs/domain-modeling.md",
        "docs/domain/modeling.md",
        "docs/domain/model.md",
        "docs/ddd/domain-modeling.md",
        "docs/architecture/domain-modeling.md",
    }
    domain_terms = (
        "domain-model",
        "domain_model",
        "bounded-context",
        "bounded_context",
        "context-map",
        "context_map",
        "ubiquitous-language",
        "ubiquitous_language",
        "glossary",
        "invariant",
        "aggregate",
    )
    return any(
        path in explicit_files
        or (
            path.startswith(("docs/domain/", "docs/domains/", "docs/ddd/", "docs/architecture/", "domain/"))
            and any(term in path for term in domain_terms)
        )
        for path in lowered_files
    )


def _methodology_gaps(signals: dict[str, bool], profile: dict[str, Any], files: set[str]) -> list[str]:
    gaps: list[str] = []
    drivers = profile.get("drivers", {}) if isinstance(profile, dict) else {}
    test_maturity = drivers.get("test_maturity", "none")
    if not (signals["architecture_docs"] or signals["adr"]):
        gaps.append("missing architecture documentation signals")
    if test_maturity == "none" and not signals["evals"] and not signals["quality_testing_evals"]:
        gaps.append("missing test or eval signals")
    if not (signals["codeowners"] or signals["ci"]):
        gaps.append("missing docs-as-code ownership or CI signals")
    if not signals["metrics"]:
        gaps.append("missing product measurement signals")
    if _needs_domain_model(files, signals, profile) and not signals["domain_model"]:
        gaps.append("missing domain model for complex domain")
    return gaps


def _needs_domain_model(files: set[str], signals: dict[str, bool], profile: dict[str, Any]) -> bool:
    drivers = profile.get("drivers", {}) if isinstance(profile, dict) else {}
    service_count = int(drivers.get("service_count", 1) or 1)
    stack_count = int(drivers.get("stack_count", 0) or 0)
    lowered = {path.lower() for path in files}
    workflow_terms = ("workflow", "state-machine", "state_machine", "saga", "process-manager", "orchestration")
    data_heavy_terms = ("backfill", "ledger", "billing", "warehouse", "analytics", "retention", "payout")
    return (
        profile.get("name") == "production-team"
        or service_count > 1
        or any(any(term in path for term in workflow_terms) for path in lowered)
        or (signals["database_docs"] and (stack_count > 1 or any(any(term in path for term in data_heavy_terms) for path in lowered)))
    )


def _classify_usage_mode(
    workspace: Path,
    files: set[str],
    stack: list[str],
    profile: dict[str, Any],
    signals: dict[str, bool],
    existing_control_plane: list[str],
    intent_hint: str,
    bug_reproduction_signals: dict[str, Any],
) -> dict[str, Any]:
    lowered = {path.lower() for path in files}
    intent = intent_hint.lower()
    failed_verification = bool(bug_reproduction_signals.get("present"))
    active_surfaces = _active_route_surfaces(
        files,
        lowered,
        signals,
        profile,
        existing_control_plane,
        bug_reproduction_signals,
    )
    reasons: list[str] = []

    if _mentions_any(intent, ["pr", "pull request", "diff", "review before merge"]):
        primary = "pr_review"
        confidence = "high"
        reasons.append("prompt requests PR or diff review")
    elif _mentions_any(intent, ["ci", "flaky", "pipeline", "github actions"]):
        primary = "ci_stabilization"
        confidence = "high"
        reasons.append("prompt requests CI or flaky-test stabilization")
    elif _mentions_any(intent, ["release", "publish", "package", "changelog", "semver"]):
        primary = "release_packaging"
        confidence = "high"
        reasons.append("prompt requests release or packaging readiness")
    elif _mentions_any(intent, ["api migration", "contract migration", "breaking api"]):
        primary = "api_migration"
        confidence = "high"
        reasons.append("prompt requests API migration")
    elif _mentions_any(intent, ["rag", "eval regression", "hallucination", "retrieval"]):
        primary = "ai_eval_regression"
        confidence = "high"
        reasons.append("prompt requests AI or RAG eval regression")
    elif _mentions_any(intent, ["security", "auth", "permission", "payment", "billing", "pii"]):
        primary = "security_sensitive_change"
        confidence = "high"
        reasons.append("prompt requests security-sensitive change handling")
    elif _mentions_any(intent, ["ios", "android", "mobile", "simulator", "emulator"]):
        primary = "native_mobile_feature"
        confidence = "high"
        reasons.append("prompt requests native or mobile work")
    elif _mentions_any(intent, ["desktop", "electron", "tauri", "local-first", "local first"]):
        primary = "desktop_local_first"
        confidence = "high"
        reasons.append("prompt requests desktop or local-first work")
    elif _mentions_any(intent, ["legacy", "undocumented", "onboarding", "orient me"]):
        primary = "legacy_onboarding"
        confidence = "high"
        reasons.append("prompt requests legacy or undocumented repository onboarding")
    elif _mentions_any(intent, ["bug", "broken", "failed", "fix it", "stuck"]):
        primary = "bug_rescue"
        confidence = "high"
        reasons.append("prompt reports broken behavior")
    elif failed_verification:
        primary = "bug_rescue"
        confidence = "high"
        reasons.append("RUNLOG.md contains failed verification evidence")
    elif "pr_review_surface" in active_surfaces:
        primary = "pr_review"
        confidence = "medium"
        reasons.append("workspace has PR diff or changed-files review signals")
    elif _is_greenfield(files):
        primary = "greenfield_idea"
        confidence = "high"
        reasons.append("workspace has no implementation files")
    elif "docs" in stack and len(stack) == 1:
        primary = "docs_only"
        confidence = "medium"
        reasons.append("workspace is a docs-only project")
    elif "ci_failure_surface" in active_surfaces:
        primary = "ci_stabilization"
        confidence = "medium"
        reasons.append("workspace has CI failure evidence signals")
    elif "native_mobile_surface" in active_surfaces:
        primary = "native_mobile_feature"
        confidence = "medium"
        reasons.append("workspace has native or mobile runtime signals")
    elif "desktop_local_surface" in active_surfaces:
        primary = "desktop_local_first"
        confidence = "medium"
        reasons.append("workspace has desktop or local-first runtime signals")
    elif "data_migration_surface" in active_surfaces:
        primary = "data_migration"
        confidence = "medium"
        reasons.append("workspace has database or migration documentation signals")
    elif "security_sensitive_surface" in active_surfaces:
        primary = "security_sensitive_change"
        confidence = "medium"
        reasons.append("workspace has auth, permission, payment or sensitive-data signals")
    elif "ai_eval_surface" in active_surfaces:
        primary = "ai_eval_regression"
        confidence = "medium"
        reasons.append("workspace has AI or RAG eval regression signals")
    elif "api_contract_surface" in active_surfaces:
        primary = "api_migration"
        confidence = "medium"
        reasons.append("workspace has API contract migration signals")
    elif "distribution_surface" in active_surfaces:
        primary = "release_packaging"
        confidence = "medium"
        reasons.append("workspace has package or release distribution signals")
    elif "legacy_docs_debt_surface" in active_surfaces:
        primary = "legacy_onboarding"
        confidence = "medium"
        reasons.append("workspace has legacy or undocumented repository signals")
    elif "monorepo" in stack or _has_integration_surface(lowered) or _service_count(files) > 1:
        primary = "complex_system_acceleration"
        confidence = "medium"
        reasons.append("workspace has monorepo or integration-heavy signals")
    elif signals["database_docs"]:
        primary = "data_migration"
        confidence = "medium"
        reasons.append("workspace has database or migration documentation signals")
    elif existing_control_plane and not intent_hint:
        primary = "maintenance"
        confidence = "medium"
        reasons.append("workspace already has Product-Agent OS control-plane context")
    else:
        primary = "standard_feature"
        confidence = "medium"
        reasons.append("workspace has implementation files without a stronger usage-mode signal")

    secondary = _secondary_usage_modes(primary, lowered, signals, profile)
    return _usage_mode_packet(primary, secondary, confidence, reasons)


def _usage_mode_packet(
    primary: str,
    secondary: list[str],
    confidence: str,
    reasons: list[str],
) -> dict[str, Any]:
    behavioral_cases = list(MODE_BEHAVIORAL_CASES.get(primary, ["route-selection"]))
    for mode in secondary:
        for case in MODE_BEHAVIORAL_CASES.get(mode, []):
            if case not in behavioral_cases:
                behavioral_cases.append(case)
    return {
        "primary": primary,
        "secondary": secondary,
        "confidence": confidence,
        "reasons": reasons[:5],
        "fallback": "standard_feature" if primary != "standard_feature" else "maintenance",
        "first_response_contract": FIRST_RESPONSE_CONTRACT,
        "minimum_artifacts": MODE_MINIMUM_ARTIFACTS[primary],
        "behavioral_eval_cases": behavioral_cases,
    }


def _secondary_usage_modes(
    primary: str,
    lowered_files: set[str],
    signals: dict[str, bool],
    profile: dict[str, Any],
) -> list[str]:
    modes: list[str] = []
    if primary != "api_migration" and (signals["openapi"] or signals["asyncapi"]):
        modes.append("api_migration")
    if primary != "data_migration" and signals["database_docs"]:
        modes.append("data_migration")
    if primary != "security_sensitive_change" and _has_security_surface(lowered_files):
        modes.append("security_sensitive_change")
    if primary != "release_packaging" and _has_release_surface(lowered_files):
        modes.append("release_packaging")
    drivers = profile.get("drivers", {}) if isinstance(profile, dict) else {}
    if primary != "ci_stabilization" and drivers.get("ci_present"):
        modes.append("ci_stabilization")
    return modes


def _mentions_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def _is_greenfield(files: set[str]) -> bool:
    if not files:
        return True
    non_idea_files = {
        path
        for path in files
        if path.lower() not in {"readme.md", "license", ".gitignore"}
        and not path.lower().startswith("docs/")
    }
    return not non_idea_files


def _has_failed_verification(workspace: Path, files: set[str]) -> bool:
    return bool(_detect_bug_reproduction_signals(workspace, files)["present"])


def _detect_bug_reproduction_signals(workspace: Path, files: set[str]) -> dict[str, Any]:
    evidence_files: list[str] = []
    for relative in sorted(files, key=str.lower):
        if not _is_bug_evidence_candidate(relative):
            continue
        text = _read_lower_text(workspace / relative)
        if _contains_failure_signal(text):
            evidence_files.append(relative)

    present = bool(evidence_files)
    return {
        "present": present,
        "evidence_files": evidence_files,
        "verification_status": "possible_evidence" if present else "not_found",
        "note": (
            "candidate logs are possible evidence, not verified truth; rerun required before a fix claim"
            if present
            else "no candidate reproduction evidence found"
        ),
    }


def _is_bug_evidence_candidate(relative: str) -> bool:
    lowered = relative.lower()
    name = Path(lowered).name
    if name in BUG_EVIDENCE_FILE_NAMES:
        return True
    if not lowered.endswith((".log", ".txt", ".xml")):
        return False
    return any(term in lowered for term in BUG_EVIDENCE_PATH_TERMS)


def _contains_failure_signal(text: str) -> bool:
    return any(term in text for term in BUG_FAILURE_TERMS)


def _read_lower_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").lower()
    except (OSError, UnicodeDecodeError):
        return ""


def _service_count(files: set[str]) -> int:
    return len({path.split("/")[1] for path in files if path.startswith("packages/") and "/" in path})


def _has_integration_surface(lowered_files: set[str]) -> bool:
    terms = ["webhook", "integration", "client", "queue", "event", "openapi", "asyncapi"]
    return any(any(term in path for term in terms) for path in lowered_files)


def _has_api_contract_surface(lowered_files: set[str], signals: dict[str, bool]) -> bool:
    api_signal_names = (
        "openapi",
        "asyncapi",
        "graphql_schema",
        "protobuf_schema",
        "json_schema",
        "pact_contract",
        "api_generated_client",
        "api_webhook_event",
        "api_external_provider",
    )
    if not any(signals.get(name) for name in api_signal_names):
        return False
    migration_terms = [
        "migration",
        "breaking",
        "deprecation",
        "version",
        "v2",
        "consumer",
        "contract",
        "openapi",
        "asyncapi",
        "graphql",
        "proto",
        "schema",
        "pact",
        "webhook",
        "integration",
        "sdk",
    ]
    return any(any(term in path for term in migration_terms) for path in lowered_files)


def _has_ai_eval_surface(lowered_files: set[str]) -> bool:
    terms = ["rag", "retrieval", "prompt", "eval", "evaluation", "hallucination", "judge"]
    regression_terms = ["regression", "baseline", "quality", "eval"]
    return any(any(term in path for term in terms) for path in lowered_files) and any(
        any(term in path for term in regression_terms) for path in lowered_files
    )


def _has_native_mobile_surface(lowered_files: set[str]) -> bool:
    return any(
        path.startswith("android/")
        or path.startswith("ios/")
        or path.endswith(".xcodeproj/project.pbxproj")
        or path.endswith(".xcworkspace/contents.xcworkspacedata")
        or path.endswith("androidmanifest.xml")
        or path in {"podfile", "pubspec.yaml"}
        or "react-native" in path
        for path in lowered_files
    )


def _has_desktop_local_surface(lowered_files: set[str]) -> bool:
    terms = ["src-tauri/", "tauri.conf", "electron", "main-process", "desktop", ".sln", ".csproj"]
    return any(any(term in path for term in terms) for path in lowered_files)


def _has_security_surface(lowered_files: set[str]) -> bool:
    terms = [
        "auth",
        "permission",
        "payment",
        "billing",
        "secret",
        "pii",
        "oauth",
        "mfa",
        "rbac",
        "acl",
        "checkout",
        "stripe",
        "abuse",
        "rate-limit",
        "rate_limit",
    ]
    return any(any(term in path for term in terms) for path in lowered_files)


def _has_release_surface(lowered_files: set[str]) -> bool:
    return any(
        path in {"changelog.md", "release.md"}
        or "release.md" in path
        or path.startswith(".github/workflows/release")
        or _is_release_artifact_source(path)
        for path in lowered_files
    )


def _has_pr_review_surface(lowered_files: set[str]) -> bool:
    return any(
        path.endswith(".patch")
        or path.endswith(".diff")
        or path in {".codex/pr/changed-files.md", ".codex/pr/pr-body.md"}
        or path.endswith("/changed-files.md")
        or path.endswith("/diff-summary.md")
        or path.endswith("/review-request.md")
        for path in lowered_files
    )


def _has_ci_failure_surface(lowered_files: set[str], profile: dict[str, Any]) -> bool:
    drivers = profile.get("drivers", {}) if isinstance(profile, dict) else {}
    if not drivers.get("ci_present"):
        return False
    terms = [
        "ci/failure",
        "ci/flaky",
        "ci/test-result",
        "ci/rerun",
        "ci/job",
        "ci/log",
        "github-actions",
        "workflow-failure",
        "junit",
    ]
    return any(any(term in path for term in terms) for path in lowered_files)


def _has_legacy_docs_debt_surface(
    files: set[str],
    lowered_files: set[str],
    existing_control_plane: list[str],
) -> bool:
    if existing_control_plane:
        return False
    explicit_terms = ["legacy", "undocumented", "onboarding"]
    if any(any(term in path for term in explicit_terms) for path in lowered_files):
        return True
    if _has_readme_or_docs(lowered_files):
        return False
    return _has_run_command_file(lowered_files) and _has_code_entry_surface(lowered_files)


def _has_readme_or_docs(lowered_files: set[str]) -> bool:
    return any(path in {"readme.md", "docs/readme.md"} or path.startswith("docs/") for path in lowered_files)


def _has_run_command_file(lowered_files: set[str]) -> bool:
    return any(
        path.startswith("scripts/run.")
        or path.startswith("scripts/start.")
        or path in {"run.sh", "start.sh"}
        for path in lowered_files
    )


def _has_code_entry_surface(lowered_files: set[str]) -> bool:
    suffixes = (".py", ".js", ".ts", ".tsx", ".go", ".rs", ".java", ".cs")
    entry_terms = ("app", "main", "index", "server", "service", "worker", "cli")
    return any(path.endswith(suffixes) and any(term in Path(path).stem for term in entry_terms) for path in lowered_files)


def _legacy_onboarding_signals(
    files: set[str],
    signals: dict[str, bool],
    existing_control_plane: list[str],
) -> dict[str, Any]:
    lowered = {path.lower() for path in files}
    entry_points = sorted(path for path in files if _is_entry_point_candidate(path))
    run_commands = sorted(path for path in files if _is_run_command_candidate(path))
    docs = sorted(path for path in files if path.lower() in {"readme.md", "docs/readme.md"} or path.lower().startswith("docs/"))
    architecture_sources = sorted(
        path
        for path in files
        if path.lower().startswith(("architecture/", "docs/architecture/", "docs/adr/", "adr/"))
        or path.lower() in {"architecture.md", "docs/architecture.md"}
    )
    return {
        "entry_points": entry_points[:20],
        "entry_points_status": "present_unverified" if entry_points else "applicable_missing",
        "run_commands": run_commands[:20],
        "run_commands_status": "present_unverified" if run_commands else "applicable_missing",
        "documentation_files": docs[:20],
        "documentation_status": "present_unverified" if docs else "applicable_missing",
        "architecture_files": architecture_sources[:20],
        "architecture_status": (
            "present_unverified"
            if architecture_sources or signals.get("architecture_docs") or signals.get("adr")
            else "applicable_missing"
        ),
        "control_plane_status": "present_unverified" if existing_control_plane else "applicable_missing",
        "note": "present_unverified until commands run or owner evidence confirms the claim",
    }


def _api_migration_signals(files: set[str], signals: dict[str, bool]) -> dict[str, Any]:
    contract_sources = sorted(path for path in files if _is_contract_source(path))
    consumer_sources = sorted(path for path in files if _is_consumer_source(path))
    generated_clients = sorted(path for path in files if _is_generated_client_source(path))
    deprecation_sources = sorted(path for path in files if _is_deprecation_source(path))
    release_sources = sorted(path for path in files if _is_release_source(path))
    compatibility_sources = sorted(path for path in files if _is_compatibility_source(path))

    if signals.get("openapi") and not any("openapi" in path.lower() for path in contract_sources):
        contract_sources.append("openapi:present")
    if signals.get("asyncapi") and not any("asyncapi" in path.lower() for path in contract_sources):
        contract_sources.append("asyncapi:present")

    return {
        "contract_sources": contract_sources[:20],
        "contract_sources_status": "present_unverified" if contract_sources else "applicable_missing",
        "consumer_sources": consumer_sources[:20],
        "consumer_impact_status": "present_unverified" if consumer_sources else "applicable_missing",
        "generated_clients": generated_clients[:20],
        "generated_clients_status": "present_unverified" if generated_clients else "applicable_missing",
        "deprecation_sources": deprecation_sources[:20],
        "deprecation_status": "present_unverified" if deprecation_sources else "applicable_missing",
        "release_sources": release_sources[:20],
        "release_impact_status": "present_unverified" if release_sources else "applicable_missing",
        "compatibility_sources": compatibility_sources[:20],
        "compatibility_status": "present_unverified" if compatibility_sources else "applicable_missing",
        "verification_status": "applicable_missing",
        "note": "present_unverified until contract lint, generated client checks, or owner evidence confirms compatibility",
    }


def _api_integration_signals(files: set[str]) -> dict[str, Any]:
    normalized = {path.replace("\\", "/") for path in files}

    def packet(sources: list[str]) -> dict[str, Any]:
        return {
            "sources": sources[:20],
            "status": "present_unverified" if sources else "applicable_missing",
        }

    contract_sources = sorted(path for path in normalized if _is_http_contract_source(path))
    event_contract_sources = sorted(path for path in normalized if _is_asyncapi_contract_source(path))
    graphql_sources = sorted(path for path in normalized if path.lower().endswith((".graphql", ".graphqls")))
    protobuf_sources = sorted(path for path in normalized if path.lower().endswith(".proto"))
    json_schema_sources = sorted(path for path in normalized if _is_json_schema_source(path))
    pact_sources = sorted(path for path in normalized if _is_pact_source(path))
    generated_client_sources = sorted(path for path in normalized if _is_generated_client_source(path))
    webhook_event_sources = sorted(path for path in normalized if _is_webhook_event_source(path))
    external_provider_sources = sorted(path for path in normalized if _is_external_provider_source(path))
    security_auth_sources = sorted(path for path in normalized if _is_api_security_auth_source(path))
    compatibility_sources = sorted(path for path in normalized if _is_compatibility_source(path))

    return {
        "contract_sources": packet(contract_sources),
        "event_contract_sources": packet(event_contract_sources),
        "graphql_sources": packet(graphql_sources),
        "protobuf_sources": packet(protobuf_sources),
        "json_schema_sources": packet(json_schema_sources),
        "pact_sources": packet(pact_sources),
        "generated_client_sources": packet(generated_client_sources),
        "webhook_event_sources": packet(webhook_event_sources),
        "external_provider_sources": packet(external_provider_sources),
        "security_auth_sources": packet(security_auth_sources),
        "compatibility_sources": packet(compatibility_sources),
        "note": (
            "API discovery records contracts, consumers, generated clients, webhooks, providers, auth "
            "and compatibility signals as present_unverified without executing API tools, publishing SDKs "
            "or performing external writes; approval_required applies before side effects."
        ),
    }


def _ai_eval_signals(files: set[str]) -> dict[str, Any]:
    baseline_sources = sorted(path for path in files if _is_ai_baseline_source(path))
    dataset_sources = sorted(path for path in files if _is_ai_dataset_source(path))
    prompt_context_sources = sorted(path for path in files if _is_ai_prompt_context_source(path))
    retrieval_sources = sorted(path for path in files if _is_ai_retrieval_source(path))
    judge_rubric_sources = sorted(path for path in files if _is_ai_judge_rubric_source(path))
    threshold_sources = sorted(path for path in files if _is_ai_threshold_source(path))
    latency_cost_sources = sorted(path for path in files if _is_ai_latency_cost_source(path))
    failure_examples = sorted(path for path in files if _is_ai_failure_example_source(path))

    return {
        "baseline_sources": baseline_sources[:20],
        "baseline_status": "present_unverified" if baseline_sources else "applicable_missing",
        "dataset_sources": dataset_sources[:20],
        "dataset_status": "present_unverified" if dataset_sources else "applicable_missing",
        "prompt_context_sources": prompt_context_sources[:20],
        "prompt_context_status": "present_unverified" if prompt_context_sources else "applicable_missing",
        "retrieval_sources": retrieval_sources[:20],
        "retrieval_status": "present_unverified" if retrieval_sources else "applicable_missing",
        "judge_rubric_sources": judge_rubric_sources[:20],
        "judge_rubric_status": "present_unverified" if judge_rubric_sources else "applicable_missing",
        "threshold_sources": threshold_sources[:20],
        "threshold_status": "present_unverified" if threshold_sources else "applicable_missing",
        "latency_cost_sources": latency_cost_sources[:20],
        "latency_cost_status": "present_unverified" if latency_cost_sources else "applicable_missing",
        "failure_examples": failure_examples[:20],
        "failure_examples_status": "present_unverified" if failure_examples else "applicable_missing",
        "verification_status": "applicable_missing",
        "note": "present_unverified until eval rerun, baseline comparison, or owner evidence confirms quality",
    }


def _source_packet(sources: list[str]) -> dict[str, Any]:
    return {
        "sources": sources[:20],
        "status": "present_unverified" if sources else "applicable_missing",
    }


def _llm_ai_rag_signals(files: set[str]) -> dict[str, Any]:
    prompt_sources = sorted(path for path in files if _is_ai_prompt_context_source(path))
    model_config_sources = sorted(path for path in files if _is_ai_model_config_source(path))
    structured_output_sources = sorted(path for path in files if _is_ai_structured_output_source(path))
    tool_sources = sorted(path for path in files if _is_ai_tool_source(path))
    retrieval_sources = sorted(path for path in files if _is_ai_retrieval_source(path))
    dataset_sources = sorted(path for path in files if _is_ai_dataset_source(path))
    eval_sources = sorted(path for path in files if _is_ai_eval_source(path))
    agent_trace_sources = sorted(path for path in files if _is_ai_agent_trace_source(path))
    safety_sources = sorted(path for path in files if _is_ai_safety_source(path))
    latency_cost_sources = sorted(path for path in files if _is_ai_latency_cost_source(path))
    core_signal_present = any(
        [
            prompt_sources,
            model_config_sources,
            structured_output_sources,
            tool_sources,
            retrieval_sources,
            dataset_sources,
            eval_sources,
            agent_trace_sources,
            safety_sources,
        ]
    )

    return {
        "prompt_sources": _source_packet(prompt_sources),
        "model_config_sources": _source_packet(model_config_sources),
        "structured_output_sources": _source_packet(structured_output_sources),
        "tool_sources": _source_packet(tool_sources),
        "retrieval_sources": _source_packet(retrieval_sources),
        "dataset_sources": _source_packet(dataset_sources),
        "eval_sources": _source_packet(eval_sources),
        "agent_trace_sources": _source_packet(agent_trace_sources),
        "safety_sources": _source_packet(safety_sources),
        "latency_cost_sources": _source_packet(latency_cost_sources),
        "diff_signal_policy": {
            "status": "limited_to_workspace_and_intent_signals",
            "external_git_or_network_used": False,
            "limitations": [
                "no external branches",
                "no network",
                "filename changes alone are not certainty",
            ],
        },
        "verification_status": "applicable_missing" if core_signal_present else "not_applicable",
        "note": (
            "AI/RAG discovery is read-only: no model calls, eval runs, vector DB access, "
            "external writes or owner approvals are performed; signals remain present_unverified."
            if core_signal_present
            else "no AI/RAG behavior signal detected"
        ),
    }


def _native_mobile_signals(files: set[str]) -> dict[str, Any]:
    platform_sources = sorted(path for path in files if _is_native_platform_source(path))
    permission_sources = sorted(path for path in files if _is_native_permission_source(path))
    offline_sources = sorted(path for path in files if _is_native_offline_source(path))
    simulator_emulator_sources = sorted(path for path in files if _is_native_simulator_emulator_source(path))
    build_command_sources = sorted(path for path in files if _is_native_build_command_source(path))
    log_sources = sorted(path for path in files if _is_native_log_source(path))
    screenshot_sources = sorted(path for path in files if _is_native_screenshot_source(path))

    return {
        "platform_sources": platform_sources[:20],
        "platform_status": "present_unverified" if platform_sources else "applicable_missing",
        "permission_sources": permission_sources[:20],
        "permission_status": "present_unverified" if permission_sources else "applicable_missing",
        "offline_sources": offline_sources[:20],
        "offline_status": "present_unverified" if offline_sources else "applicable_missing",
        "simulator_emulator_sources": simulator_emulator_sources[:20],
        "simulator_emulator_status": "present_unverified" if simulator_emulator_sources else "applicable_missing",
        "build_command_sources": build_command_sources[:20],
        "build_command_status": "present_unverified" if build_command_sources else "applicable_missing",
        "log_sources": log_sources[:20],
        "logs_status": "present_unverified" if log_sources else "applicable_missing",
        "screenshot_sources": screenshot_sources[:20],
        "screenshot_status": "present_unverified" if screenshot_sources else "applicable_missing",
        "verification_status": "applicable_missing",
        "note": (
            "present_unverified until platform build/run, simulator/emulator, "
            "device, log, or screenshot evidence confirms behavior"
        ),
    }


def _desktop_local_signals(files: set[str]) -> dict[str, Any]:
    platform_sources = sorted(path for path in files if _is_desktop_platform_source(path))
    filesystem_sources = sorted(path for path in files if _is_desktop_filesystem_source(path))
    local_data_sources = sorted(path for path in files if _is_desktop_local_data_source(path))
    background_job_sources = sorted(path for path in files if _is_desktop_background_job_source(path))
    privacy_sources = sorted(path for path in files if _is_desktop_privacy_source(path))
    build_command_sources = sorted(path for path in files if _is_desktop_build_command_source(path))
    runtime_log_sources = sorted(path for path in files if _is_desktop_runtime_log_source(path))
    screenshot_sources = sorted(path for path in files if _is_desktop_screenshot_source(path))
    recovery_sources = sorted(path for path in files if _is_desktop_recovery_source(path))

    return {
        "platform_sources": platform_sources[:20],
        "platform_status": "present_unverified" if platform_sources else "applicable_missing",
        "filesystem_sources": filesystem_sources[:20],
        "filesystem_status": "present_unverified" if filesystem_sources else "applicable_missing",
        "local_data_sources": local_data_sources[:20],
        "local_data_status": "present_unverified" if local_data_sources else "applicable_missing",
        "background_job_sources": background_job_sources[:20],
        "background_job_status": "present_unverified" if background_job_sources else "applicable_missing",
        "privacy_sources": privacy_sources[:20],
        "privacy_status": "present_unverified" if privacy_sources else "applicable_missing",
        "build_command_sources": build_command_sources[:20],
        "build_command_status": "present_unverified" if build_command_sources else "applicable_missing",
        "runtime_log_sources": runtime_log_sources[:20],
        "runtime_log_status": "present_unverified" if runtime_log_sources else "applicable_missing",
        "screenshot_sources": screenshot_sources[:20],
        "screenshot_status": "present_unverified" if screenshot_sources else "applicable_missing",
        "recovery_sources": recovery_sources[:20],
        "recovery_status": "present_unverified" if recovery_sources else "applicable_missing",
        "verification_status": "applicable_missing",
        "note": (
            "present_unverified until desktop build/run, app log, screenshot, "
            "local data, recovery, or owner evidence confirms behavior"
        ),
    }


def _data_migration_signals(files: set[str]) -> dict[str, Any]:
    schema_sources = sorted(path for path in files if _is_data_schema_source(path))
    backfill_sources = sorted(path for path in files if _is_data_backfill_source(path))
    sensitive_sources = sorted(path for path in files if _is_data_sensitive_source(path))
    retention_sources = sorted(path for path in files if _is_data_retention_source(path))
    rollback_sources = sorted(path for path in files if _is_data_rollback_source(path))
    validation_sources = sorted(path for path in files if _is_data_validation_source(path))
    dry_run_sources = sorted(path for path in files if _is_data_dry_run_source(path))
    database_dictionary_sources = sorted(path for path in files if _is_database_dictionary_source(path))

    return {
        "schema_sources": schema_sources[:20],
        "schema_status": "present_unverified" if schema_sources else "applicable_missing",
        "backfill_sources": backfill_sources[:20],
        "backfill_status": "present_unverified" if backfill_sources else "applicable_missing",
        "sensitive_data_sources": sensitive_sources[:20],
        "sensitive_data_status": "present_unverified" if sensitive_sources else "applicable_missing",
        "retention_sources": retention_sources[:20],
        "retention_status": "present_unverified" if retention_sources else "applicable_missing",
        "rollback_sources": rollback_sources[:20],
        "rollback_status": "present_unverified" if rollback_sources else "applicable_missing",
        "validation_sources": validation_sources[:20],
        "validation_status": "present_unverified" if validation_sources else "applicable_missing",
        "dry_run_sources": dry_run_sources[:20],
        "dry_run_status": "present_unverified" if dry_run_sources else "applicable_missing",
        "database_dictionary_sources": database_dictionary_sources[:20],
        "database_dictionary_status": (
            "present_unverified" if database_dictionary_sources else "applicable_missing"
        ),
        "verification_status": "applicable_missing",
        "note": (
            "present_unverified until migration dry run, validation, rollback, "
            "backup, owner review, or approved environment evidence confirms behavior"
        ),
    }


def _database_data_signals(files: set[str]) -> dict[str, Any]:
    normalized = {path.replace("\\", "/") for path in files}

    def packet(sources: list[str]) -> dict[str, Any]:
        return {
            "sources": sources[:20],
            "status": "present_unverified" if sources else "applicable_missing",
        }

    schema_sources = sorted(path for path in normalized if _is_data_schema_source(path))
    migration_sources = sorted(path for path in normalized if _is_database_migration_source(path))
    migration_tools = sorted(path for path in normalized if _is_database_migration_tool_source(path))
    orm_models = sorted(path for path in normalized if _is_database_orm_source(path))
    dictionary_sources = sorted(path for path in normalized if _is_database_dictionary_source(path))
    data_quality_sources = sorted(path for path in normalized if _is_database_quality_source(path))
    lineage_sources = sorted(path for path in normalized if _is_database_lineage_source(path))
    query_performance_sources = sorted(path for path in normalized if _is_database_query_performance_source(path))
    production_access_sources = sorted(path for path in normalized if _is_database_production_access_source(path))
    destructive_change_sources = sorted(path for path in normalized if _is_database_destructive_source(path))
    pipeline_sources = sorted(path for path in normalized if _is_database_pipeline_source(path))
    rag_ingestion_sources = sorted(path for path in normalized if _is_database_rag_ingestion_source(path))
    backup_restore_sources = sorted(path for path in normalized if _is_database_backup_restore_source(path))
    privacy_retention_sources = sorted(path for path in normalized if _is_database_privacy_retention_source(path))

    return {
        "schema_sources": packet(schema_sources),
        "migration_sources": packet(migration_sources),
        "migration_tools": packet(migration_tools),
        "orm_models": packet(orm_models),
        "dictionary_sources": packet(dictionary_sources),
        "data_quality_sources": packet(data_quality_sources),
        "lineage_sources": packet(lineage_sources),
        "query_performance_sources": packet(query_performance_sources),
        "production_access_sources": packet(production_access_sources),
        "destructive_change_sources": packet(destructive_change_sources),
        "pipeline_sources": packet(pipeline_sources),
        "rag_ingestion_sources": packet(rag_ingestion_sources),
        "backup_restore_sources": packet(backup_restore_sources),
        "privacy_retention_sources": packet(privacy_retention_sources),
        "verification_status": "applicable_missing",
        "note": (
            "database_data_signals are present_unverified until owner review, dry run, validation, "
            "backup/restore, query-plan, lineage, data-quality or runtime evidence exists; discovery is "
            "read-only without database connections; approval_required applies before DB introspection, "
            "production access, production data access, destructive migration, backup restore, retention "
            "mutation or migration execution; do not claim database safety from detection."
        ),
    }


def _security_sensitive_signals(files: set[str]) -> dict[str, Any]:
    authn_sources = sorted(path for path in files if _is_security_authn_source(path))
    authz_sources = sorted(path for path in files if _is_security_authz_source(path))
    permission_sources = sorted(path for path in files if _is_security_permission_source(path))
    payment_sources = sorted(path for path in files if _is_security_payment_source(path))
    secret_sources = sorted(path for path in files if _is_security_secret_source(path))
    sensitive_data_sources = sorted(path for path in files if _is_security_sensitive_data_source(path))
    abuse_control_sources = sorted(path for path in files if _is_security_abuse_control_source(path))
    audit_logging_sources = sorted(path for path in files if _is_security_audit_logging_source(path))
    test_sources = sorted(path for path in files if _is_security_test_source(path))
    rollback_sources = sorted(path for path in files if _is_security_rollback_source(path))
    approval_sources = sorted(path for path in files if _is_security_approval_source(path))

    return {
        "authn_sources": authn_sources[:20],
        "authn_status": "present_unverified" if authn_sources else "applicable_missing",
        "authz_sources": authz_sources[:20],
        "authz_status": "present_unverified" if authz_sources else "applicable_missing",
        "permission_sources": permission_sources[:20],
        "permission_status": "present_unverified" if permission_sources else "applicable_missing",
        "payment_sources": payment_sources[:20],
        "payment_status": "present_unverified" if payment_sources else "applicable_missing",
        "secret_sources": secret_sources[:20],
        "secret_status": "present_unverified" if secret_sources else "applicable_missing",
        "sensitive_data_sources": sensitive_data_sources[:20],
        "sensitive_data_status": "present_unverified" if sensitive_data_sources else "applicable_missing",
        "abuse_control_sources": abuse_control_sources[:20],
        "abuse_control_status": "present_unverified" if abuse_control_sources else "applicable_missing",
        "audit_logging_sources": audit_logging_sources[:20],
        "audit_logging_status": "present_unverified" if audit_logging_sources else "applicable_missing",
        "test_sources": test_sources[:20],
        "test_status": "present_unverified" if test_sources else "applicable_missing",
        "rollback_sources": rollback_sources[:20],
        "rollback_status": "present_unverified" if rollback_sources else "applicable_missing",
        "approval_sources": approval_sources[:20],
        "approval_status": "present_unverified" if approval_sources else "applicable_missing",
        "verification_status": "applicable_missing",
        "note": (
            "present_unverified until security tests, owner review, approval, "
            "rollback evidence, and abuse-control evidence confirm behavior"
        ),
    }


def _backend_dependency_signals(files: set[str]) -> dict[str, Any]:
    normalized = {path.replace("\\", "/") for path in files}

    def packet(sources: list[str]) -> dict[str, Any]:
        return {
            "sources": sources[:20],
            "status": "present_unverified" if sources else "applicable_missing",
        }

    categories = {
        "database": sorted(path for path in normalized if _is_backend_database_dependency_source(path)),
        "message_broker": sorted(path for path in normalized if _is_backend_message_broker_dependency_source(path)),
        "cache": sorted(path for path in normalized if _is_backend_cache_dependency_source(path)),
        "payment": sorted(path for path in normalized if _is_backend_payment_dependency_source(path)),
        "email": sorted(path for path in normalized if _is_backend_email_dependency_source(path)),
        "storage": sorted(path for path in normalized if _is_backend_storage_dependency_source(path)),
        "search": sorted(path for path in normalized if _is_backend_search_dependency_source(path)),
        "third_party_http_provider": sorted(
            path for path in normalized if _is_backend_third_party_http_provider_source(path)
        ),
    }
    result = {name: packet(sources) for name, sources in categories.items()}
    result["note"] = (
        "backend dependency categories include database, message broker, cache, payment, email, "
        "storage, search and third-party HTTP/provider clients; present_unverified until owner review, "
        "contract evidence and runtime verification confirm dependency behavior"
    )
    return result


def _backend_delivery_signals(files: set[str], stack: list[str]) -> dict[str, Any]:
    normalized = {path.replace("\\", "/") for path in files}

    def packet(sources: list[str]) -> dict[str, Any]:
        return {
            "sources": sources[:20],
            "status": "present_unverified" if sources else "applicable_missing",
        }

    stack_sources = sorted(path for path in normalized if _is_backend_stack_source(path, stack))
    command_sources = sorted(path for path in normalized if _is_run_command_candidate(path))
    ci_sources = sorted(path for path in normalized if _is_ci_workflow_source(path))
    api_sources = sorted(path for path in normalized if _is_contract_source(path))
    database_sources = sorted(path for path in normalized if _is_backend_database_dependency_source(path))
    queue_sources = sorted(path for path in normalized if _is_backend_message_broker_dependency_source(path))
    worker_sources = sorted(path for path in normalized if _is_backend_worker_source(path))
    deployment_sources = sorted(path for path in normalized if _is_backend_deployment_manifest_source(path))
    security_sources = sorted(path for path in normalized if _is_backend_security_signal_source(path))

    return {
        "backend_stack": packet(stack_sources),
        "commands": packet(command_sources),
        "ci": packet(ci_sources),
        "api_contracts": packet(api_sources),
        "database": packet(database_sources),
        "queues": packet(queue_sources),
        "workers": packet(worker_sources),
        "deployment_manifests": packet(deployment_sources),
        "security": packet(security_sources),
        "note": (
            "Workspace discovery records backend stack, backend commands, CI, APIs, DB, queues, "
            "workers, deployment manifests and security signals as present_unverified without "
            "executing deployments, commands or external writes; approval_required applies before "
            "deployment, production data, secrets or other external mutations."
        ),
    }


def _backend_resilience_signals(files: set[str]) -> dict[str, Any]:
    normalized = {path.replace("\\", "/") for path in files}

    def packet(sources: list[str]) -> dict[str, Any]:
        return {
            "sources": sources[:20],
            "status": "present_unverified" if sources else "applicable_missing",
        }

    retry_idempotency_sources = sorted(path for path in normalized if _is_backend_retry_idempotency_source(path))
    job_context_sources = sorted(path for path in normalized if _is_backend_job_context_source(path))
    dependency_context_sources = sorted(path for path in normalized if _is_backend_dependency_context_source(path))

    return {
        "retry_idempotency_terms": packet(retry_idempotency_sources),
        "job_context": packet(job_context_sources),
        "dependency_context": packet(dependency_context_sources),
        "note": (
            "T9-D7 uses lightweight read-only signals for retry/idempotency terms and "
            "dependency/job context only; deeper static analysis deferred to avoid false positives "
            "until a later stack-specific slice has owner, examples and verification."
        ),
    }


def _ci_stabilization_signals(files: set[str]) -> dict[str, Any]:
    workflow_sources = sorted(path for path in files if _is_ci_workflow_source(path))
    failure_log_sources = sorted(path for path in files if _is_ci_failure_log_source(path))
    job_sources = sorted(path for path in files if _is_ci_job_source(path))
    command_sources = sorted(path for path in files if _is_ci_command_source(path))
    environment_sources = sorted(path for path in files if _is_ci_environment_source(path))
    test_result_sources = sorted(path for path in files if _is_ci_test_result_source(path))
    flaky_sources = sorted(path for path in files if _is_ci_flaky_source(path))
    local_reproduction_sources = sorted(path for path in files if _is_ci_local_reproduction_source(path))
    rerun_sources = sorted(path for path in files if _is_ci_rerun_source(path))
    approval_sources = sorted(path for path in files if _is_ci_approval_source(path))

    return {
        "workflow_sources": workflow_sources[:20],
        "workflow_status": "present_unverified" if workflow_sources else "applicable_missing",
        "failure_log_sources": failure_log_sources[:20],
        "failure_log_status": "present_unverified" if failure_log_sources else "applicable_missing",
        "job_sources": job_sources[:20],
        "job_status": "present_unverified" if job_sources else "applicable_missing",
        "command_sources": command_sources[:20],
        "command_status": "present_unverified" if command_sources else "applicable_missing",
        "environment_sources": environment_sources[:20],
        "environment_status": "present_unverified" if environment_sources else "applicable_missing",
        "test_result_sources": test_result_sources[:20],
        "test_result_status": "present_unverified" if test_result_sources else "applicable_missing",
        "flaky_sources": flaky_sources[:20],
        "flaky_status": "present_unverified" if flaky_sources else "applicable_missing",
        "local_reproduction_sources": local_reproduction_sources[:20],
        "local_reproduction_status": (
            "present_unverified" if local_reproduction_sources else "applicable_missing"
        ),
        "rerun_sources": rerun_sources[:20],
        "rerun_status": "present_unverified" if rerun_sources else "applicable_missing",
        "approval_sources": approval_sources[:20],
        "approval_status": "present_unverified" if approval_sources else "applicable_missing",
        "verification_status": "applicable_missing",
        "note": (
            "present_unverified until local reproduction, deterministic/flaky "
            "classification, rerun evidence, and owner approval confirm CI behavior"
        ),
    }


def _release_packaging_signals(files: set[str]) -> dict[str, Any]:
    package_metadata_sources = sorted(path for path in files if _is_package_metadata_source(path))
    version_sources = sorted(path for path in files if _is_release_version_source(path))
    changelog_sources = sorted(path for path in files if _is_release_changelog_source(path))
    build_sources = sorted(path for path in files if _is_release_build_source(path))
    test_sources = sorted(path for path in files if _is_release_test_source(path))
    docs_sources = sorted(path for path in files if _is_release_docs_source(path))
    security_sources = sorted(path for path in files if _is_release_security_source(path))
    license_sources = sorted(path for path in files if _is_release_license_source(path))
    artifact_sources = sorted(path for path in files if _is_release_artifact_source(path))
    rollback_sources = sorted(path for path in files if _is_release_rollback_source(path))
    approval_sources = sorted(path for path in files if _is_release_approval_source(path))

    return {
        "package_metadata_sources": package_metadata_sources[:20],
        "package_metadata_status": "present_unverified" if package_metadata_sources else "applicable_missing",
        "version_sources": version_sources[:20],
        "version_status": "present_unverified" if version_sources else "applicable_missing",
        "changelog_sources": changelog_sources[:20],
        "changelog_status": "present_unverified" if changelog_sources else "applicable_missing",
        "build_sources": build_sources[:20],
        "build_status": "present_unverified" if build_sources else "applicable_missing",
        "test_sources": test_sources[:20],
        "test_status": "present_unverified" if test_sources else "applicable_missing",
        "docs_sources": docs_sources[:20],
        "docs_status": "present_unverified" if docs_sources else "applicable_missing",
        "security_sources": security_sources[:20],
        "security_status": "present_unverified" if security_sources else "applicable_missing",
        "license_sources": license_sources[:20],
        "license_status": "present_unverified" if license_sources else "applicable_missing",
        "artifact_sources": artifact_sources[:20],
        "artifact_status": "present_unverified" if artifact_sources else "applicable_missing",
        "rollback_sources": rollback_sources[:20],
        "rollback_status": "present_unverified" if rollback_sources else "applicable_missing",
        "approval_sources": approval_sources[:20],
        "approval_status": "present_unverified" if approval_sources else "applicable_missing",
        "verification_status": "applicable_missing",
        "note": (
            "present_unverified until release evidence, SemVer review, build and test evidence, "
            "docs evidence, security/license review, owner review, publish approval, and rollback evidence confirm readiness"
        ),
    }


def _is_package_metadata_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered
        in {
            "package.json",
            "pyproject.toml",
            "setup.cfg",
            "setup.py",
            "cargo.toml",
            "go.mod",
            "package.swift",
            "pubspec.yaml",
            "plugin.json",
            ".codex-plugin/plugin.json",
        }
        or lowered.endswith((".gemspec", ".nuspec", ".csproj"))
    )


def _is_release_version_source(relative: str) -> bool:
    lowered = relative.lower()
    return _is_package_metadata_source(relative) or any(
        term in lowered for term in ("version", "semver", "release", "changelog")
    )


def _is_release_changelog_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered == "changelog.md" or "changelog" in lowered or "changeset" in lowered


def _is_release_build_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered == "package.json"
        or _is_release_workflow_source(relative)
        or any(term in lowered for term in ("build", "bundle", "dist/", "artifact", "package"))
    )


def _is_release_test_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered == "package.json"
        or lowered.startswith(("test/", "tests/", "__tests__/"))
        or ".test." in lowered
        or ".spec." in lowered
        or "test-result" in lowered
    )


def _is_release_docs_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered.startswith("docs/") and any(
        term in lowered for term in ("release", "publish", "package", "docs", "readme")
    )


def _is_release_security_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("security", "vulnerability", "sbom", "slsa", "provenance"))


def _is_release_license_source(relative: str) -> bool:
    lowered = relative.lower()
    name = Path(lowered).name
    return name in {"license", "license.md", "license.txt", "notice", "notice.md"} or "license" in lowered


def _is_release_artifact_source(relative: str) -> bool:
    lowered = relative.lower()
    suffixes = (
        ".tgz",
        ".tar.gz",
        ".zip",
        ".whl",
        ".jar",
        ".gem",
        ".nupkg",
        ".vsix",
        ".pkg",
        ".msi",
        ".dmg",
        ".apk",
        ".aab",
        ".ipa",
    )
    return lowered.startswith(("dist/", "artifacts/", "release-artifacts/")) and lowered.endswith(suffixes)


def _is_release_rollback_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("rollback", "revert", "restore", "unpublish", "yank"))


def _is_release_approval_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("approval", "owner-review", "publish-approval", "release-approval"))


def _is_release_workflow_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered.startswith(".github/workflows/release") or any(
        term in lowered for term in ("release.yml", "release.yaml", "publish.yml", "publish.yaml")
    )


def _is_database_data_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered in {"alembic.ini", "dbt_project.yml", "flyway.conf", "schemaspy.properties"}
        or lowered.endswith((".dbml", ".sql", "schema.prisma"))
        or lowered.startswith(("db/", "database/", "migrations/", "prisma/", "liquibase/", "warehouse/"))
        or any(
            term in lowered
            for term in (
                "backfill",
                "retention",
                "lineage",
                "openlineage",
                "great_expectations",
                "query-plan",
                "production-data",
            )
        )
    )


def _is_data_schema_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith(("migrations/", "db/", "database/", "schema/"))
        or lowered.endswith((".sql", ".dbml", "schema.prisma"))
        or any(term in lowered for term in ("schema", "migration", "ddl"))
    )


def _is_data_backfill_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("backfill", "seed", "data-fix", "data_migration"))


def _is_data_sensitive_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("pii", "sensitive", "personal-data", "customer-data", "privacy"))


def _is_data_retention_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("retention", "ttl", "expiry", "archive", "purge"))


def _is_data_rollback_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("rollback", "restore", "backup", "down.sql", "revert"))


def _is_data_validation_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("validation", "data-quality", "quality", "row-count", "checksum", "constraint"))


def _is_data_dry_run_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("dry-run", "plan", "preview", "migration-report"))


def _is_database_dictionary_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("database-dictionary", "data-dictionary", "schema.dbml", ".dbml"))


def _is_database_migration_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered.startswith("migrations/") or "migration" in lowered or lowered.endswith(".sql")


def _is_database_migration_tool_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered in {"alembic.ini", "flyway.conf", "dbt_project.yml"}
        or lowered.startswith("liquibase/")
        or lowered.startswith("prisma/")
        or "liquibase" in lowered
        or "flyway" in lowered
        or "alembic" in lowered
        or "prisma" in lowered
    )


def _is_database_orm_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.endswith("schema.prisma")
        or "models.py" in lowered
        or lowered.endswith(("entity.ts", "model.ts", "model.py"))
        or "typeorm" in lowered
        or "sequelize" in lowered
        or "active_record" in lowered
    )


def _is_database_quality_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(
        term in lowered
        for term in ("great_expectations", "data-quality", "data_quality", "dbt_project.yml", "dbt", "row-count", "checksum", "constraint")
    )


def _is_database_lineage_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("lineage", "openlineage", "dbt_project.yml", "dbt"))


def _is_database_query_performance_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("query-plan", "explain", "performance", "index-review", "slow-query"))


def _is_database_production_access_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("production-data", "production-db", "prod-db", "prod-data", "production-access"))


def _is_database_destructive_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("drop", "truncate", "rename", "cleanup", "purge", "destructive"))


def _is_database_pipeline_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered.startswith(("warehouse/", "pipelines/", "etl/", "elt/")) or any(
        term in lowered for term in ("pipeline", "warehouse", "dbt_project.yml", "model.sql")
    )


def _is_database_rag_ingestion_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("rag_ingest", "rag-ingest", "rag_ingestion", "rag-ingestion", "retrieval"))


def _is_database_backup_restore_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("backup", "restore", "snapshot", "dump", "production-data"))


def _is_database_privacy_retention_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("pii", "privacy", "retention", "deletion", "sensitive", "production-data"))


def _is_security_authn_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("authn", "authentication", "login", "oauth", "oidc", "sso", "mfa"))


def _is_security_authz_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("authz", "authorization", "rbac", "acl", "role", "policy", "permission"))


def _is_security_permission_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("permission", "entitlement", "scope", "role", "access-control", "access_control"))


def _is_security_payment_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("payment", "billing", "checkout", "stripe", "invoice", "subscription"))


def _is_security_secret_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("secret", "credential", "token-policy", "key-management", "vault"))


def _is_security_sensitive_data_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("pii", "sensitive", "personal-data", "privacy", "customer-data"))


def _is_security_abuse_control_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("abuse", "rate-limit", "rate_limit", "fraud", "throttle", "quota"))


def _is_security_audit_logging_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("audit", "security-log", "security_log", "logging", "access-log"))


def _is_security_test_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith(("test/", "tests/", "__tests__/"))
        or ".test." in lowered
        or ".spec." in lowered
    ) and any(term in lowered for term in ("auth", "permission", "payment", "billing", "security", "pii"))


def _is_security_rollback_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("rollback", "revert", "disable", "kill-switch", "feature-flag"))


def _is_security_approval_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("approval", "owner-review", "security-review", "risk-review"))


def _is_backend_database_dependency_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith(("repositories/", "src/repositories/", "db/", "database/", "migrations/"))
        or lowered.endswith((".sql", ".dbml", "schema.prisma"))
        or any(term in lowered for term in ("postgres", "psycopg", "mysql", "sqlite", "database", "repository"))
    )


def _is_backend_message_broker_dependency_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith(("queues/", "src/queues/", "consumers/", "src/consumers/"))
        or any(
            term in lowered
            for term in (
                "message-broker",
                "message_broker",
                "broker",
                "queue",
                "consumer",
                "kafka",
                "rabbitmq",
                "sqs",
                "pubsub",
                "nats",
            )
        )
    )


def _is_backend_cache_dependency_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered.startswith(("cache/", "src/cache/")) or any(
        term in lowered for term in ("redis", "memcache", "memcached", "cache")
    )


def _is_backend_payment_dependency_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("payment", "billing", "checkout", "stripe", "invoice", "subscription"))


def _is_backend_email_dependency_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("email", "mail", "smtp", "sendgrid", "ses", "postmark"))


def _is_backend_storage_dependency_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered.startswith(("storage/", "src/storage/")) or any(
        term in lowered for term in ("blob", "object-store", "object_store", "s3", "gcs", "r2", "storage")
    )


def _is_backend_search_dependency_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered.startswith(("search/", "src/search/")) or any(
        term in lowered for term in ("search", "elasticsearch", "opensearch", "algolia", "meilisearch")
    )


def _is_backend_third_party_http_provider_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith(("adapters/", "src/adapters/", "integrations/", "src/integrations/"))
        or any(
            term in lowered
            for term in (
                "provider_client",
                "provider-client",
                "http_client",
                "http-client",
                "api_client",
                "api-client",
                "external_client",
                "external-client",
                "third_party",
                "third-party",
                "webhook",
            )
        )
    )


def _is_backend_stack_source(relative: str, stack: list[str]) -> bool:
    lowered = relative.lower()
    stack_markers = {
        "package.json",
        "pyproject.toml",
        "requirements.txt",
        "go.mod",
        "pom.xml",
        "build.gradle",
        "cargo.toml",
    }
    return (
        lowered in stack_markers
        or _detect_backend_signal({relative})
        or bool(stack)
        and lowered in stack_markers
    )


def _is_backend_worker_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered.startswith(
        (
            "workers/",
            "src/workers/",
            "jobs/",
            "src/jobs/",
            "schedulers/",
            "src/schedulers/",
            "consumers/",
            "src/consumers/",
        )
    ) or any(term in lowered for term in ("worker", "scheduler", "consumer", "job"))


def _is_backend_deployment_manifest_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered in {"dockerfile", "docker-compose.yml", "docker-compose.yaml", "procfile", "serverless.yml"}
        or lowered.startswith(("k8s/", "kubernetes/", "helm/", "charts/", ".github/workflows/deploy"))
        or lowered.endswith((".tf", ".tf.json"))
        and any(term in lowered for term in ("deploy", "service", "worker", "backend"))
    )


def _is_backend_security_signal_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith(("security/", "src/security/", "auth/", "src/auth/"))
        or _is_security_authn_source(relative)
        or _is_security_authz_source(relative)
        or _is_security_permission_source(relative)
        or _is_security_payment_source(relative)
        or _is_security_secret_source(relative)
        or _is_security_sensitive_data_source(relative)
        or _is_security_abuse_control_source(relative)
        or _is_security_audit_logging_source(relative)
    )


def _is_backend_retry_idempotency_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(
        term in lowered
        for term in (
            "retry",
            "retries",
            "backoff",
            "timeout",
            "idempotency",
            "idempotent",
            "dedupe",
            "deduplication",
            "circuit-breaker",
            "circuit_breaker",
        )
    )


def _is_backend_job_context_source(relative: str) -> bool:
    lowered = relative.lower()
    return _is_backend_worker_source(relative) or _is_backend_message_broker_dependency_source(relative)


def _is_backend_dependency_context_source(relative: str) -> bool:
    return (
        _is_backend_database_dependency_source(relative)
        or _is_backend_message_broker_dependency_source(relative)
        or _is_backend_cache_dependency_source(relative)
        or _is_backend_payment_dependency_source(relative)
        or _is_backend_email_dependency_source(relative)
        or _is_backend_storage_dependency_source(relative)
        or _is_backend_search_dependency_source(relative)
        or _is_backend_third_party_http_provider_source(relative)
    )


def _is_ci_workflow_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith(".github/workflows/")
        or lowered in {".gitlab-ci.yml", "azure-pipelines.yml", "jenkinsfile"}
        or lowered.startswith((".circleci/", ".buildkite/"))
    )


def _is_ci_failure_log_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(
        term in lowered
        for term in (
            "ci/failure",
            "ci/log",
            "failure.log",
            "workflow-failure",
            "github-actions",
            "junit",
        )
    )


def _is_ci_job_source(relative: str) -> bool:
    lowered = relative.lower()
    return _is_ci_workflow_source(relative) or any(term in lowered for term in ("ci/job", "jobs", "workflow"))


def _is_ci_command_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered in {"package.json", "makefile", "justfile", "taskfile.yml"}
        or lowered.startswith("scripts/")
        and any(term in Path(lowered).name for term in ("test", "ci", "build", "lint"))
        or _is_ci_workflow_source(relative)
    )


def _is_ci_environment_source(relative: str) -> bool:
    lowered = relative.lower()
    return _is_ci_workflow_source(relative) or any(
        term in lowered for term in ("environment", "runner", "ubuntu", "windows", "macos", "node-version")
    )


def _is_ci_test_result_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("test-result", "test_results", "junit", "coverage", "testsuite"))


def _is_ci_flaky_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("flaky", "flake", "intermittent", "nondeterministic"))


def _is_ci_local_reproduction_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("local-reproduction", "reproduction", "scripts/test", "test-ci"))


def _is_ci_rerun_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("rerun", "retry", "re-run"))


def _is_ci_approval_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("approval", "owner", "remote", "settings", "branch-protection"))


def _is_desktop_platform_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith("src-tauri/")
        or "tauri.conf" in lowered
        or "electron" in lowered
        or "main-process" in lowered
        or lowered.endswith((".sln", ".csproj", ".xcodeproj/project.pbxproj"))
        or lowered in {"package.json", "cargo.toml"}
    )


def _is_desktop_filesystem_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(
        term in lowered
        for term in (
            "filesystem",
            "file-system",
            "file-access",
            "documents",
            "downloads",
            "appdata",
            "local-data",
            "storage",
        )
    )


def _is_desktop_local_data_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith(("db/", "database/", "data/"))
        or lowered.endswith((".sqlite", ".sqlite3", ".db"))
        or any(term in lowered for term in ("indexeddb", "localdb", "local-db", "local-store", "local-data", "cache"))
    )


def _is_desktop_background_job_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("background", "indexer", "worker", "daemon", "scheduler", "tray"))


def _is_desktop_privacy_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("privacy", "pii", "telemetry", "retention", "local-data"))


def _is_desktop_build_command_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered in {"package.json", "cargo.toml"}
        or lowered.startswith("src-tauri/")
        or lowered.endswith((".sln", ".csproj"))
        or lowered.startswith("scripts/")
        and any(term in lowered for term in ("build", "desktop", "electron", "tauri", "run"))
    )


def _is_desktop_runtime_log_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered.endswith(".log") or any(term in lowered for term in ("app-log", "runtime-log", "desktop-log"))


def _is_desktop_screenshot_source(relative: str) -> bool:
    lowered = relative.lower()
    return "screenshot" in lowered or "screen-shot" in lowered


def _is_desktop_recovery_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("recovery", "rollback", "restore", "backup", "crash"))


def _is_native_platform_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith(("android/", "ios/"))
        or lowered.endswith(".xcodeproj/project.pbxproj")
        or lowered.endswith(".xcworkspace/contents.xcworkspacedata")
        or lowered in {"podfile", "pubspec.yaml"}
        or "react-native" in lowered
    )


def _is_native_permission_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("androidmanifest.xml", ".entitlements", "permission", "camera", "location"))


def _is_native_offline_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("offline", "sync", "cache", "local-store", "localdb"))


def _is_native_simulator_emulator_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("simulator", "emulator", "androidtest", "xctest", "xcuitest", "device"))


def _is_native_build_command_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered in {"pubspec.yaml", "podfile", "package.json"}
        or lowered.endswith(("build.gradle", "settings.gradle", "gradlew", "gradlew.bat"))
        or lowered.endswith(".xcodeproj/project.pbxproj")
        or lowered.endswith(".xcworkspace/contents.xcworkspacedata")
        or lowered.startswith("scripts/")
        and any(term in lowered for term in ("build", "android", "ios", "simulator", "emulator"))
    )


def _is_native_log_source(relative: str) -> bool:
    lowered = relative.lower()
    return "log" in lowered and lowered.endswith((".txt", ".log", ".md"))


def _is_native_screenshot_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("screenshot", "screenshots", "screen-recording")) or lowered.endswith(
        (".png", ".jpg", ".jpeg", ".webp")
    )


def _is_ai_baseline_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("baseline", "golden", "expected-output"))


def _is_ai_dataset_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith(("datasets/", "evals/", "fixtures/"))
        and lowered.endswith((".json", ".jsonl", ".csv", ".yaml", ".yml", ".md"))
        and _has_ai_rag_context_term(lowered)
        or any(term in lowered for term in ("ai-dataset", "rag-dataset"))
        or (any(term in lowered for term in ("eval-cases", "testset")) and _has_ai_rag_context_term(lowered))
    )


def _is_ai_prompt_context_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered.startswith("prompts/") or any(term in lowered for term in ("prompt", "retrieval"))


def _is_ai_retrieval_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("rag", "retrieval", "vector", "embedding", "rerank", "grounding"))


def _is_ai_model_config_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith(("model-config/", "config/ai/", "config/openai/"))
        or (
            any(term in lowered for term in ("model-config", "model_config", "openai", "llm"))
            and lowered.endswith((".json", ".yaml", ".yml", ".toml", ".md"))
        )
    )


def _is_ai_structured_output_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith("structured-output/")
        or any(term in lowered for term in ("structured-output", "structured_output", "json-schema", "json_schema"))
        and _has_ai_rag_context_term(lowered)
    )


def _is_ai_tool_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered.startswith("mcp/") or any(
        term in lowered for term in ("ai-tool", "tool-call", "function_call", "function-call", "mcp")
    ) or (
        lowered.startswith(("tools/", "functions/"))
        and "tool" in lowered
    )


def _is_ai_eval_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("promptfoo", "ragas")) or (
        (lowered.startswith("evals/") or "eval" in lowered)
        and _has_ai_rag_context_term(lowered)
    )


def _is_ai_agent_trace_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith("agents/")
        and any(term in lowered for term in ("trace", "span", "handoff", "workflow"))
    ) or any(
        term in lowered for term in ("agents-sdk", "openai-agents", "agent-trace", "open telemetry", "opentelemetry")
    )


def _is_ai_safety_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered.startswith(("guardrails/", "safety/", "red-team/")) or any(
        term in lowered for term in ("guardrail", "safety", "red-team", "red_team", "prompt-injection", "prompt_injection")
    )


def _has_ai_rag_context_term(lowered: str) -> bool:
    normalized = lowered.replace("_", "-")
    return any(
        term in normalized
        for term in (
            "ai-",
            "/ai/",
            "llm",
            "rag",
            "retrieval",
            "prompt",
            "embedding",
            "vector-store",
            "vector-db",
            "grounding",
            "hallucination",
            "judge",
            "openai",
            "ragas",
            "promptfoo",
            "guardrail",
            "model-config",
            "function-call",
            "tool-call",
            "structured-output",
        )
    )


def _has_llm_ai_rag_signal(lowered_files: set[str]) -> bool:
    return any(
        _is_ai_prompt_context_source(path)
        or _is_ai_model_config_source(path)
        or _is_ai_structured_output_source(path)
        or _is_ai_tool_source(path)
        or _is_ai_retrieval_source(path)
        or _is_ai_dataset_source(path)
        or _is_ai_eval_source(path)
        or _is_ai_agent_trace_source(path)
        or _is_ai_safety_source(path)
        for path in lowered_files
    )


def _is_ai_judge_rubric_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("rubric", "judge", "criteria", "eval"))


def _is_ai_threshold_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("threshold", "score", "metric", "quality"))


def _is_ai_latency_cost_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("latency", "cost", "token", "performance"))


def _is_ai_failure_example_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("failure", "regression", "bad-example", "failure-examples"))


def _is_contract_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        _is_http_contract_source(lowered)
        or _is_asyncapi_contract_source(lowered)
        or lowered.endswith((".graphql", ".graphqls", ".proto"))
        or _is_json_schema_source(lowered)
        or _is_pact_source(lowered)
    )


def _is_http_contract_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith("openapi/")
        or lowered.endswith(("openapi.yaml", "openapi.yml", "openapi.json"))
        or lowered.endswith(("swagger.yaml", "swagger.yml", "swagger.json"))
    )


def _is_asyncapi_contract_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith("asyncapi/")
        or lowered.endswith(("asyncapi.yaml", "asyncapi.yml", "asyncapi.json"))
    )


def _is_json_schema_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.endswith(".schema.json")
        or lowered.startswith(("schemas/", "schema/")) and lowered.endswith(".json")
        or "json-schema" in lowered
    )


def _is_pact_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered.startswith(("pact/", "pacts/", "contract-tests/", "consumer-contracts/"))
        or "pact" in lowered and lowered.endswith(".json")
    )


def _is_consumer_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(
        term in lowered
        for term in (
            "consumer",
            "client",
            "sdk",
            "docs/api",
            "docs/deprecation",
            "deprecation",
        )
    )


def _is_generated_client_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("generated", "clients/", "sdk/"))


def _is_webhook_event_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered.startswith(("webhooks/", "events/")) or any(
        term in lowered for term in ("webhook", "event-contract", "cloudevents")
    )


def _is_external_provider_source(relative: str) -> bool:
    lowered = relative.lower()
    return lowered.startswith(("integrations/", "providers/")) or any(
        term in lowered for term in ("external-provider", "provider-client", "payment-provider")
    )


def _is_api_security_auth_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("auth", "oauth", "scope", "token", "rate-limit", "rate_limit", "security"))


def _is_deprecation_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("deprecation", "deprecated", "sunset"))


def _is_release_source(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered in {"changelog.md", "release.md", "package.json", "pyproject.toml", "cargo.toml", "go.mod"}
        or lowered.startswith(".github/workflows/release")
        or "release" in lowered
    )


def _is_compatibility_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(term in lowered for term in ("compat", "migration", "contract", "openapi", "asyncapi"))


def _is_entry_point_candidate(relative: str) -> bool:
    lowered = relative.lower()
    if not lowered.endswith((".py", ".js", ".ts", ".tsx", ".go", ".rs", ".java", ".cs")):
        return False
    return any(term in Path(lowered).stem for term in ("app", "main", "index", "server", "service", "worker", "cli"))


def _is_run_command_candidate(relative: str) -> bool:
    lowered = relative.lower()
    return (
        lowered in {"package.json", "pyproject.toml", "requirements.txt", "cargo.toml", "go.mod"}
        or lowered.startswith("scripts/")
        and Path(lowered).name.startswith(("run", "start", "dev", "test", "build"))
    )


def _active_route_surfaces(
    files: set[str],
    lowered_files: set[str],
    signals: dict[str, bool],
    profile: dict[str, Any],
    existing_control_plane: list[str],
    bug_reproduction_signals: dict[str, Any],
) -> list[str]:
    surfaces: list[str] = []
    checks = [
        ("bug_reproduction_surface", bool(bug_reproduction_signals.get("present"))),
        ("pr_review_surface", _has_pr_review_surface(lowered_files)),
        ("api_contract_surface", _has_api_contract_surface(lowered_files, signals)),
        ("ai_eval_surface", _has_ai_eval_surface(lowered_files)),
        ("native_mobile_surface", _has_native_mobile_surface(lowered_files)),
        ("desktop_local_surface", _has_desktop_local_surface(lowered_files)),
        ("database_data_surface", signals["database_data"]),
        ("data_migration_surface", signals["database_docs"]),
        ("security_sensitive_surface", _has_security_surface(lowered_files)),
        ("ci_failure_surface", _has_ci_failure_surface(lowered_files, profile)),
        ("distribution_surface", _has_release_surface(lowered_files)),
        ("integration_surface", _has_integration_surface(lowered_files)),
        ("legacy_docs_debt_surface", _has_legacy_docs_debt_surface(files, lowered_files, existing_control_plane)),
    ]
    for name, present in checks:
        if present:
            surfaces.append(name)
    return surfaces


def _docs_tooling_decision(
    files: set[str],
    stack: list[str],
    profile: dict[str, Any],
    signals: dict[str, bool],
) -> dict[str, Any]:
    lowered = {path.lower() for path in files}
    selected_tools: list[str] = []
    rejected_tools: list[str] = []
    commands: list[str] = []
    approval_required: list[str] = []

    def select(tool: str, command: str = "") -> None:
        if tool not in selected_tools:
            selected_tools.append(tool)
        if command and command not in commands:
            commands.append(command)

    def require_approval(item: str) -> None:
        if item not in approval_required:
            approval_required.append(item)

    def status_packet(status: str, tool: str = "none", command: str = "", reason: str = "") -> dict[str, str]:
        return {
            "status": status,
            "tool": tool,
            "command": command,
            "reason": reason,
        }

    has_docs_file = any(
        path == "readme.md" or path == "docs/readme.md" or path.startswith("docs/") for path in lowered
    )
    has_mkdocs = "mkdocs.yml" in lowered
    has_docusaurus = bool({"docusaurus.config.js", "docusaurus.config.ts"} & lowered)
    has_sphinx = any(path.endswith("conf.py") and "docs" in path for path in lowered)
    has_antora = "antora-playbook.yml" in lowered
    has_readthedocs = bool({".readthedocs.yaml", "readthedocs.yaml", "readthedocs.yml"} & lowered)
    has_schemaspy = "schemaspy.properties" in lowered
    has_typedoc = "typedoc.json" in lowered
    has_jsdoc = "jsdoc.json" in lowered
    has_markdownlint = bool({".markdownlint.json", ".markdownlint.yaml"} & lowered)
    has_vale = ".vale.ini" in lowered
    has_xml_docs = any(path.endswith(".csproj") for path in lowered)
    has_javadoc = any(path.endswith((".java", "pom.xml", "build.gradle", "build.gradle.kts")) for path in lowered)
    has_mermaid = any(
        path.endswith((".mmd", ".mermaid"))
        or path in {"docs/architecture.md", "architecture.md", "docs/diagrams.md"}
        for path in lowered
    )
    has_structurizr = any("structurizr" in path or path.endswith(".dsl") for path in lowered)
    has_plantuml = any(path.endswith((".puml", ".plantuml")) for path in lowered)

    tool_statuses: dict[str, dict[str, str]] = {}

    if has_mkdocs:
        select("MkDocs", "mkdocs build --strict")
        tool_statuses["docs_portal"] = status_packet("present_unverified", "MkDocs", "mkdocs build --strict")
    elif has_docusaurus:
        select("Docusaurus", "npm run build")
        tool_statuses["docs_portal"] = status_packet("present_unverified", "Docusaurus", "npm run build")
    elif has_sphinx:
        select("Sphinx", "sphinx-build docs docs/_build")
        tool_statuses["docs_portal"] = status_packet(
            "present_unverified",
            "Sphinx",
            "sphinx-build docs docs/_build",
            "import-safety review required for autodoc",
        )
    elif has_antora:
        select("Antora", "antora antora-playbook.yml")
        tool_statuses["docs_portal"] = status_packet(
            "present_unverified", "Antora", "antora antora-playbook.yml"
        )
    elif has_docs_file or "docs" in stack:
        tool_statuses["docs_portal"] = status_packet(
            "proposal_staged", "none", "", "docs exist but no docs portal tooling was detected"
        )
    else:
        tool_statuses["docs_portal"] = status_packet(
            "not_applicable", "none", "", "docs-light or internal-only workspace"
        )
        rejected_tools.extend(["MkDocs", "Docusaurus", "Sphinx", "Antora", "Read the Docs"])

    if signals.get("openapi"):
        select("OpenAPI tooling", "openapi lint/build")
        api_status = status_packet("present_unverified", "OpenAPI tooling", "openapi lint/build")
    elif signals.get("asyncapi"):
        select("AsyncAPI tooling", "asyncapi lint/build")
        api_status = status_packet("present_unverified", "AsyncAPI tooling", "asyncapi lint/build")
    else:
        api_status = status_packet("not_applicable", "none", "", "no API contract signal")
    tool_statuses["api_docs"] = api_status

    if signals.get("storybook"):
        select("Storybook", "npm run build-storybook")
        tool_statuses["ui_component_docs"] = status_packet(
            "present_unverified", "Storybook", "npm run build-storybook"
        )
    else:
        tool_statuses["ui_component_docs"] = status_packet("not_applicable", "none", "", "no UI component docs signal")

    if signals.get("database_docs"):
        select("DBML/dbdocs", "dbml validation/docs build")
        tool_statuses["database_docs"] = status_packet("present_unverified", "DBML/dbdocs", "dbml validation/docs build")
    else:
        tool_statuses["database_docs"] = status_packet("not_applicable", "none", "", "no database docs signal")

    if has_schemaspy:
        require_approval("db introspection")
        tool_statuses["db_introspection"] = status_packet(
            "approval_required", "SchemaSpy", "", "DB introspection approval required"
        )
    else:
        tool_statuses["db_introspection"] = status_packet("not_applicable", "none", "", "no SchemaSpy signal")

    if has_readthedocs:
        select("Read the Docs")
        require_approval("hosted docs")
        tool_statuses["hosted_docs"] = status_packet(
            "approval_required", "Read the Docs", "", "hosted docs approval required"
        )
    else:
        tool_statuses["hosted_docs"] = status_packet("not_applicable", "none", "", "no hosted docs signal")

    if has_typedoc:
        select("TypeDoc", "typedoc")
        code_reference = status_packet("present_unverified", "TypeDoc", "typedoc")
    elif has_jsdoc:
        select("JSDoc", "jsdoc")
        code_reference = status_packet("present_unverified", "JSDoc", "jsdoc")
    elif has_sphinx:
        code_reference = status_packet("present_unverified", "Sphinx", "sphinx-build docs docs/_build")
    elif has_javadoc:
        select("Javadoc", "javadoc")
        code_reference = status_packet("proposal_staged", "Javadoc", "javadoc")
    elif has_xml_docs:
        select("XML docs", "dotnet build")
        code_reference = status_packet("proposal_staged", "XML docs", "dotnet build")
    else:
        code_reference = status_packet("not_applicable", "none", "", "no public code reference signal")
    tool_statuses["code_reference"] = code_reference

    if has_vale:
        select("Vale", "vale .")
        docs_lint = status_packet("present_unverified", "Vale", "vale .")
    elif has_markdownlint:
        select("markdownlint", "markdownlint .")
        docs_lint = status_packet("present_unverified", "markdownlint", "markdownlint .")
    else:
        docs_lint = status_packet("not_applicable", "none", "", "no docs lint signal")
    tool_statuses["docs_lint"] = docs_lint

    architecture_diagram_commands: list[str] = []
    if has_mermaid:
        select("Mermaid", "docs build/render check")
        architecture_diagram_commands.append("docs build/render check")
    if has_structurizr:
        select("Structurizr DSL", "structurizr validate")
        architecture_diagram_commands.append("structurizr validate")
    if has_plantuml:
        select("PlantUML", "plantuml")
        architecture_diagram_commands.append("plantuml")
    if architecture_diagram_commands:
        selected_diagram_tools = [
            tool for tool in ("Mermaid", "Structurizr DSL", "PlantUML") if tool in selected_tools
        ]
        tool_statuses["architecture_diagrams"] = status_packet(
            "present_unverified",
            ", ".join(selected_diagram_tools),
            "; ".join(architecture_diagram_commands),
        )
    else:
        tool_statuses["architecture_diagrams"] = status_packet(
            "not_applicable", "none", "", "no architecture diagram tooling signal"
        )

    if approval_required:
        impact_status = "approval_required"
    elif selected_tools:
        impact_status = "present_unverified"
    elif has_docs_file or signals.get("docs_portal") or profile.get("name") == "production-team":
        impact_status = "proposal_staged"
    else:
        impact_status = "not_applicable"

    if "Docusaurus" not in selected_tools and "Docusaurus" not in rejected_tools:
        rejected_tools.append("Docusaurus")
    if "Antora" not in selected_tools and "Antora" not in rejected_tools:
        rejected_tools.append("Antora")

    return {
        "docs_as_code_impact": {
            "status": impact_status,
            "allowed_statuses": DOCS_AS_CODE_IMPACT_STATUSES,
            "evidence_owner": "docs maintainer",
            "maintenance_owner": "docs maintainer",
        },
        "selected_tools": selected_tools,
        "rejected_tools": rejected_tools,
        "commands": commands,
        "approval_required": approval_required,
        "tool_statuses": tool_statuses,
        "safety": {
            "no_forced_install": True,
            "no_ci_activation_without_approval": True,
            "hosted_docs_approval": "required",
            "db_introspection_approval": "required",
        },
    }


def _methodology_applicability(
    files: set[str],
    stack: list[str],
    profile: dict[str, Any],
    signals: dict[str, bool],
    methodology_gaps: list[str],
    docs_tooling_decision: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    docs_impact = docs_tooling_decision.get("docs_as_code_impact", {})
    docs_status = docs_impact.get("status", "not_applicable") if isinstance(docs_impact, dict) else "not_applicable"
    domain_model_needed = _needs_domain_model(files, signals, profile)
    fsd_needed = signals.get("fsd_structure", False) or _needs_fsd_structure(files)
    frontend_needed = signals.get("frontend", False)
    backend_needed = signals.get("backend", False)
    database_needed = signals.get("database_data", False) or signals.get("database_docs", False)
    ai_rag_needed = signals.get("llm_ai_rag", False)
    standards_evidence = [
        name
        for name in ("architecture_docs", "adr", "openapi", "asyncapi", "codeowners", "ci")
        if signals.get(name)
    ]

    return {
        "architecture_boundary": _applicability_packet(
            "present_unverified" if signals.get("architecture_docs") or signals.get("adr") else "applicable_missing",
            "architecture docs or ADR exist" if signals.get("architecture_docs") or signals.get("adr") else "missing architecture documentation signals",
            _signal_evidence(signals, "architecture_docs", "adr"),
            ["architecture boundary", "ADR or architecture overview when architecture changes"],
            "architect",
            "artifact presence does not prove boundary quality",
        ),
        "test_eval_first_evidence": _applicability_packet(
            "present_unverified" if _has_test_or_eval_evidence(signals, profile) else "applicable_missing",
            "test or eval evidence exists" if _has_test_or_eval_evidence(signals, profile) else "missing test or eval signals",
            _test_eval_evidence(signals, profile),
            ["test command, eval command or accepted explicit gap"],
            "tester",
            "detection alone does not prove quality evidence; current run evidence is still required",
        ),
        "docs_as_code_ownership": _applicability_packet(
            "present_unverified" if signals.get("codeowners") or signals.get("ci") else "applicable_missing",
            "docs-as-code ownership or CI signal exists"
            if signals.get("codeowners") or signals.get("ci")
            else "missing docs-as-code ownership or CI signals",
            _signal_evidence(signals, "codeowners", "ci"),
            ["CODEOWNERS, CI owner or accepted ownership gap"],
            "docs maintainer",
            "ownership signal does not prove owner review happened",
        ),
        "product_measurement": _applicability_packet(
            "present_unverified" if signals.get("metrics") else "applicable_missing",
            "product measurement signal exists" if signals.get("metrics") else "missing product measurement signals",
            _signal_evidence(signals, "metrics"),
            ["metric spec, analytics evidence or accepted measurement gap"],
            "product manager",
            "metric artifact does not prove the selected metric is correct",
        ),
        "domain_model_when_complex_domain": _applicability_packet(
            _domain_model_status(signals, domain_model_needed),
            _domain_model_reason(signals, domain_model_needed, methodology_gaps),
            _signal_evidence(signals, "domain_model"),
            ["domain-modeling.md or accepted gap when complex domain applies"],
            "architect",
            "domain expert review is still required",
        ),
        "fsd_structure_when_ui_architecture_applies": _applicability_packet(
            _fsd_status(signals, fsd_needed),
            _fsd_reason(signals, fsd_needed),
            _signal_evidence(signals, "fsd_structure"),
            ["component-card.md boundary fields or accepted UI architecture gap"],
            "builder",
            "directory detection does not prove Feature-Sliced Design quality",
        ),
        "frontend_methodology": _applicability_packet(
            "present_unverified" if frontend_needed else "not_applicable",
            "frontend signal exists" if frontend_needed else "no frontend signal",
            _signal_evidence(signals, "frontend", "storybook", "fsd_structure"),
            [
                "frontend-flow-spec.md",
                "frontend-state-matrix.md",
                "browser/runtime evidence",
                "console status",
                "privacy-safe screenshot or accepted explicit gap",
            ],
            "builder",
            "detection alone does not prove UI completion, browser/runtime evidence or owner acceptance",
        ),
        "backend_methodology": _applicability_packet(
            "present_unverified" if backend_needed else "not_applicable",
            "backend signal exists" if backend_needed else "no backend signal",
            _signal_evidence(signals, "backend", "openapi", "asyncapi", "database_docs", "ci"),
            [
                "backend-service-overview.md",
                "backend-runtime-behavior.md",
                "runtime/failure evidence",
                "observability/SLO/health evidence or accepted explicit gap",
            ],
            "backend owner",
            "detection alone does not prove backend runtime safety, failure-mode coverage or owner acceptance",
        ),
        "database_data_readiness": _applicability_packet(
            "present_unverified" if database_needed else "not_applicable",
            "database/data signal exists" if database_needed else "no database/data signal",
            _signal_evidence(signals, "database_data", "database_docs"),
            [
                "database-inventory.md",
                "database-dictionary.md",
                "database-migration-plan.md",
                "database-data-contract.md",
                "backup/restore, data quality, lineage and production access evidence or accepted explicit gap",
            ],
            "data owner",
            "detection alone does not prove database safety, migration readiness, production access approval or data quality",
        ),
        "llm_ai_rag_readiness": _applicability_packet(
            "present_unverified" if ai_rag_needed else "not_applicable",
            "AI/RAG behavior signal exists" if ai_rag_needed else "no AI/RAG behavior signal",
            _signal_evidence(signals, "llm_ai_rag"),
            [
                "ai-behavior-spec.md",
                "ai-eval-spec.md",
                "eval-run-report.md",
                "prompt-contract.md",
                "model-decision-record.md",
                "rag-source-inventory.md",
                "rag-retrieval-config.md",
                "grounding rubric",
                "tool contract",
                "approval boundary",
                "cost and latency evidence or accepted explicit gap",
            ],
            "test-eval-designer",
            "detection alone does not prove AI/RAG quality, grounding, tool safety, owner approval or cost/latency readiness",
        ),
        "docs_tooling_decision": _applicability_packet(
            docs_status if docs_status in READINESS_STATUSES else "present_unverified",
            str(docs_impact.get("reason", "docs tooling selector evaluated"))
            if isinstance(docs_impact, dict)
            else "docs tooling selector evaluated",
            _docs_tooling_evidence(docs_tooling_decision),
            ["docs-tooling-decision.md, selected/rejected tools and approval boundary"],
            "docs maintainer",
            "tool selection still needs owner review and current command evidence",
        ),
        "standards_trigger_policy": _applicability_packet(
            "present_unverified" if standards_evidence else "not_applicable",
            "standards trigger context detected" if standards_evidence else "no architecture/API/governance standard signal",
            standards_evidence,
            ["ADR/C4/arc42/OpenAPI/AsyncAPI/SemVer/CODEOWNERS/GitHub Actions applicability"],
            "architect",
            "standards context does not prove every standard is proportionate",
        ),
        "codex_agentic_workflow": _applicability_packet(
            "present_unverified" if signals.get("codex_agentic_workflow") else "not_applicable",
            "Codex workflow signal exists" if signals.get("codex_agentic_workflow") else "no Codex workflow signal",
            _signal_evidence(signals, "codex_agentic_workflow"),
            ["AGENTS.md, runtime routing, approval boundary, handoff, MCP/hook/automation review"],
            "product-agent operator",
            "detection alone does not prove safe activation, owner approval or current verification",
        ),
    }


def _applicability_packet(
    status: str,
    reason: str,
    evidence: list[str],
    required_evidence: list[str],
    owner: str,
    residual_risk: str,
) -> dict[str, Any]:
    return {
        "status": status if status in READINESS_STATUSES else "present_unverified",
        "applies_when": reason,
        "reason": reason,
        "evidence": evidence,
        "required_evidence": required_evidence,
        "owner": owner,
        "residual_risk": residual_risk,
    }


def _has_test_or_eval_evidence(signals: dict[str, bool], profile: dict[str, Any]) -> bool:
    drivers = profile.get("drivers", {}) if isinstance(profile, dict) else {}
    return (
        signals.get("evals", False)
        or signals.get("quality_testing_evals", False)
        or drivers.get("test_maturity") != "none"
    )


def _test_eval_evidence(signals: dict[str, bool], profile: dict[str, Any]) -> list[str]:
    evidence: list[str] = []
    drivers = profile.get("drivers", {}) if isinstance(profile, dict) else {}
    if drivers.get("test_maturity") != "none":
        evidence.append("test_maturity")
    if signals.get("evals"):
        evidence.append("evals")
    if signals.get("quality_testing_evals"):
        evidence.append("quality_testing_evals")
    return evidence


def _signal_evidence(signals: dict[str, bool], *names: str) -> list[str]:
    return [name for name in names if signals.get(name)]


def _domain_model_status(signals: dict[str, bool], domain_model_needed: bool) -> str:
    if not domain_model_needed:
        return "not_applicable"
    return "present_unverified" if signals.get("domain_model") else "applicable_missing"


def _domain_model_reason(
    signals: dict[str, bool],
    domain_model_needed: bool,
    methodology_gaps: list[str],
) -> str:
    if not domain_model_needed:
        return "domain model gate is not applicable for this workspace shape"
    if signals.get("domain_model"):
        return "domain model signal exists for complex domain"
    if "missing domain model for complex domain" in methodology_gaps:
        return "missing domain model for complex domain"
    return "complex domain requires domain model evidence"


def _needs_fsd_structure(files: set[str]) -> bool:
    lowered = {path.lower().replace("\\", "/") for path in files}
    if any(path.startswith(("android/", "ios/")) for path in lowered):
        return False
    component_files = [
        path
        for path in lowered
        if path.endswith((".tsx", ".jsx", ".vue", ".svelte"))
        and path.startswith(("src/pages/", "src/widgets/", "src/features/", "src/entities/", "src/components/"))
    ]
    return len(component_files) >= 4


def _fsd_status(signals: dict[str, bool], fsd_needed: bool) -> str:
    if signals.get("fsd_structure"):
        return "present_unverified"
    return "applicable_missing" if fsd_needed else "not_applicable"


def _fsd_reason(signals: dict[str, bool], fsd_needed: bool) -> str:
    if signals.get("fsd_structure"):
        return "fsd_structure signal exists"
    if fsd_needed:
        return "growing UI surface needs explicit UI architecture boundary"
    return "FSD structure gate is not applicable for this workspace shape"


def _docs_tooling_evidence(docs_tooling_decision: dict[str, Any]) -> list[str]:
    evidence: list[str] = []
    selected_tools = docs_tooling_decision.get("selected_tools", [])
    approval_required = docs_tooling_decision.get("approval_required", [])
    if isinstance(selected_tools, list):
        evidence.extend(str(tool) for tool in selected_tools)
    if isinstance(approval_required, list):
        evidence.extend(f"approval_required:{item}" for item in approval_required)
    return evidence


def _behavioral_route_inputs(
    files: set[str],
    stack: list[str],
    profile: dict[str, Any],
    signals: dict[str, bool],
    existing_control_plane: list[str],
    existing_codex_assets: list[str],
    intent_hint: str,
    bug_reproduction_signals: dict[str, Any],
) -> dict[str, Any]:
    lowered = {path.lower() for path in files}
    active_surfaces = _active_route_surfaces(
        files,
        lowered,
        signals,
        profile,
        existing_control_plane,
        bug_reproduction_signals,
    )
    return {
        "intent_hint_present": bool(intent_hint.strip()),
        "workspace_signals": {
            "stack": stack,
            "active_surfaces": active_surfaces,
            "methodology_signals": sorted(name for name, present in signals.items() if present),
            "docs_tooling_decision": _docs_tooling_decision(files, stack, profile, signals),
            "legacy_onboarding_signals": _legacy_onboarding_signals(files, signals, existing_control_plane),
            "api_migration_signals": _api_migration_signals(files, signals),
            "api_integration_signals": _api_integration_signals(files),
            "ai_eval_signals": _ai_eval_signals(files),
            "llm_ai_rag_signals": _llm_ai_rag_signals(files),
            "native_mobile_signals": _native_mobile_signals(files),
            "desktop_local_signals": _desktop_local_signals(files),
            "data_migration_signals": _data_migration_signals(files),
            "database_data_signals": _database_data_signals(files),
            "security_sensitive_signals": _security_sensitive_signals(files),
            "backend_dependency_signals": _backend_dependency_signals(files),
            "backend_delivery_signals": _backend_delivery_signals(files, stack),
            "backend_resilience_signals": _backend_resilience_signals(files),
            "ci_stabilization_signals": _ci_stabilization_signals(files),
            "release_packaging_signals": _release_packaging_signals(files),
        },
        "control_plane_state": {
            "existing_control_plane_files": existing_control_plane,
            "has_codex_assets": bool(existing_codex_assets),
        },
    }


def _profile_for(files: set[str], stack: list[str]) -> dict[str, Any]:
    service_count = len({path.split("/")[1] for path in files if path.startswith("packages/") and "/" in path})
    ci_present = any(path.startswith(".github/workflows/") for path in files)
    test_maturity = "partial" if any("test" in path.lower() for path in files) else "none"
    if "monorepo" in stack or service_count > 1:
        name = "production-team"
    elif "docs" in stack and len(stack) == 1:
        name = "guided-small"
    elif ci_present:
        name = "standard-product"
    else:
        name = "guided-small"
    return {
        "name": name,
        "confidence": "medium",
        "drivers": {
            "repo_size": "small" if len(files) < 200 else "medium",
            "stack_count": len([item for item in stack if item != "monorepo"]),
            "service_count": max(service_count, 1),
            "test_maturity": test_maturity,
            "ci_present": ci_present,
        },
    }


def analyze_workspace(root: str | Path, *, intent_hint: str = "") -> dict[str, Any]:
    workspace = Path(root).resolve()
    if not workspace.exists():
        raise FileNotFoundError(f"workspace does not exist: {workspace}")
    if not workspace.is_dir():
        raise NotADirectoryError(f"workspace is not a directory: {workspace}")
    files = _relative_files(workspace)
    stack = _detect_stack(files)
    existing_control_plane = [name for name in CONTROL_PLANE_FILES if name in files]
    missing_control_plane = [name for name in CONTROL_PLANE_FILES if name not in files]
    existing_codex_assets = sorted(path for path in files if path.startswith(".codex/"))
    profile = _profile_for(files, stack)
    methodology_signals = _detect_methodology_signals(files, profile)
    docs_tooling_decision = _docs_tooling_decision(files, stack, profile, methodology_signals)
    methodology_intelligence = build_methodology_audit(workspace, intent_hint=intent_hint)
    methodology_gaps = _methodology_gaps(methodology_signals, profile, files)
    methodology_applicability = _methodology_applicability(
        files,
        stack,
        profile,
        methodology_signals,
        methodology_gaps,
        docs_tooling_decision,
    )
    bug_reproduction_signals = _detect_bug_reproduction_signals(workspace, files)
    route_inputs = _behavioral_route_inputs(
        files,
        stack,
        profile,
        methodology_signals,
        existing_control_plane,
        existing_codex_assets,
        intent_hint,
        bug_reproduction_signals,
    )
    usage_mode = _classify_usage_mode(
        workspace,
        files,
        stack,
        profile,
        methodology_signals,
        existing_control_plane,
        intent_hint,
        bug_reproduction_signals,
    )
    risks: list[str] = []
    if "AGENTS.md" not in files:
        risks.append("missing durable project instructions")
    if not any("test" in path.lower() for path in files):
        risks.append("no detected test files or test configuration")
    risks.extend(methodology_gaps)
    return {
        "workspace": str(workspace),
        "detected_files": sorted(files),
        "detected_stack": stack,
        "existing_control_plane": existing_control_plane,
        "missing_control_plane": missing_control_plane,
        "existing_codex_assets": existing_codex_assets,
        "git": {
            "present": (workspace / ".git").exists(),
        },
        "methodology_signals": methodology_signals,
        "methodology_gaps": methodology_gaps,
        "methodology_applicability": methodology_applicability,
        "methodology_intelligence": methodology_intelligence,
        "docs_tooling_decision": docs_tooling_decision,
        "bug_reproduction_signals": bug_reproduction_signals,
        "legacy_onboarding_signals": _legacy_onboarding_signals(files, methodology_signals, existing_control_plane),
        "api_migration_signals": _api_migration_signals(files, methodology_signals),
        "ai_eval_signals": _ai_eval_signals(files),
        "llm_ai_rag_signals": _llm_ai_rag_signals(files),
        "native_mobile_signals": _native_mobile_signals(files),
        "desktop_local_signals": _desktop_local_signals(files),
        "data_migration_signals": _data_migration_signals(files),
        "database_data_signals": _database_data_signals(files),
        "security_sensitive_signals": _security_sensitive_signals(files),
        "backend_dependency_signals": _backend_dependency_signals(files),
        "backend_delivery_signals": _backend_delivery_signals(files, stack),
        "backend_resilience_signals": _backend_resilience_signals(files),
        "ci_stabilization_signals": _ci_stabilization_signals(files),
        "release_packaging_signals": _release_packaging_signals(files),
        "route_inputs": route_inputs,
        "usage_mode": usage_mode,
        "risks": risks,
        "complexity_profile": profile,
    }


def discover_workspace(root: str | Path, *, intent_hint: str = "") -> dict[str, Any]:
    return analyze_workspace(root, intent_hint=intent_hint)


def main(argv: list[str]) -> int:
    root = Path(argv[0]) if argv else Path.cwd()
    try:
        audit = analyze_workspace(root)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(audit, indent=2, sort_keys=True))
    return 0
