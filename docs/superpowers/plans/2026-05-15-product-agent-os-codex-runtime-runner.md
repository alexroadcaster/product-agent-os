---
title: "Archive - Product-Agent OS Codex Runtime Runner Implementation Plan"
---

# Archive - Product-Agent OS Codex Runtime Runner Implementation Plan {#product-agent-os-codex-runtime-runner-implementation-plan}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

Source status: `official + experiment`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** реализовать Track 5: dependency-free Codex runtime runner для `product-agent-os`, который внутри Codex App, CLI, IDE extension, skills и subagents читает control-plane artifacts, определяет lifecycle state, строит route packet, проверяет guardrails и возвращает machine-readable `codex_runner_result`.

**Architecture:** runner остается локальным contract-first helper под `plugins/product-agent-os/scripts/codex_runtime_runner/`. Он не вызывает внешние модели, не требует credentials, не устанавливает зависимости и не запускает MCP/service runtime; Codex остается execution plane, а runner только читает workspace, валидирует boundary и выдает следующий безопасный маршрут.

**Tech Stack:** Python 3 standard library, `unittest`, `argparse`, `dataclasses`, `json`, `pathlib`, existing `product_agent_os` validators, synthetic fixtures, MkDocs.

---

## Scope

План реализует [Product-Agent OS Codex Runtime Runner Design](../specs/2026-05-15-product-agent-os-codex-runtime-runner-design.md).

Входит в scope:

- contract schemas for `codex_runner_request`, `codex_route_packet`, `codex_runner_handoff`, `codex_runner_result`;
- read-only context loader for `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- deterministic lifecycle state detector;
- lifecycle-to-skill/subagent route planner;
- validators for request, route packet, handoff, approval boundary, source policy, automation boundary, result evidence, redaction;
- deterministic redaction for secret-like literals, private markers, raw chat markers, and local absolute paths;
- contract-mode CLI wrapper;
- fixture eval extension with `codex_runtime_runner_status` and runner checks;
- synthetic runner fixtures only;
- plugin structure assertion that runner is present but not default-active.

Не входит в scope:

- standalone OpenAI Agents SDK app;
- direct OpenAI API calls;
- external credentials, environment-provided model access, or external credential setup;
- external Agents SDK runtime dependency;
- external Codex MCP bridge;
- HTTP server, deployment target, background service, schedule, recurring automation, GitHub Action, or external workflow;
- global Codex config mutation;
- automatic subagent spawning from deterministic tests;
- workspace writes from runner default mode.

## Execution Model

Recommended execution: Inline Execution using `superpowers:executing-plans`, because current workspace is not a git repository and the first implementation slice is tightly coupled across tests, runner package, and fixture eval.

If subagents are explicitly requested later, split ownership as:

- Worker A: contracts/state/routes tests and implementation.
- Worker B: guards/redaction tests and implementation.
- Worker C: CLI, fixture eval, synthetic fixtures, plugin structure tests.
- Main agent: integration review, docs checks, full verification.

Workers are not alone in the codebase. They must not revert edits made by others and must preserve Track 1-4 behavior.

## File Structure

Create implementation package:

- `plugins/product-agent-os/scripts/codex_runtime_runner/__init__.py` - package marker and version.
- `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py` - allowed enums, result/request/route/handoff shape validators, result builder helpers.
- `plugins/product-agent-os/scripts/codex_runtime_runner/context_loader.py` - safe UTF-8 read of control-plane files with missing/unreadable metadata.
- `plugins/product-agent-os/scripts/codex_runtime_runner/state.py` - lifecycle state inference from request override and workspace artifacts.
- `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py` - deterministic mapping from lifecycle state to skill/subagent role and write policy.
- `plugins/product-agent-os/scripts/codex_runtime_runner/guards.py` - source, approval, handoff, automation, route, request, and result validators.
- `plugins/product-agent-os/scripts/codex_runtime_runner/redaction.py` - deterministic redaction and redaction report.
- `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py` - contract-mode runner orchestration and argument parsing.
- `plugins/product-agent-os/scripts/run_codex_runtime_runner.py` - CLI wrapper.
- `plugins/product-agent-os/scripts/validate_codex_runtime_runner.py` - result/request validator wrapper.

Create tests:

- `tests/product_agent_os/test_codex_runtime_runner_contracts.py`
- `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`
- `tests/product_agent_os/test_codex_runtime_runner_guards.py`
- `tests/product_agent_os/test_codex_runtime_runner_cli.py`
- `tests/product_agent_os/test_codex_runtime_runner_fixture_eval.py`

Modify tests:

- `tests/product_agent_os/test_plugin_structure.py`
- `tests/product_agent_os/test_fixture_eval_runner.py`
- `tests/product_agent_os/test_fixtures.py`

Modify implementation:

- `plugins/product-agent-os/scripts/run_fixture_eval.py`

Create synthetic fixture folders:

- `plugins/product-agent-os/assets/fixtures/codex-runner-ready/`
- `plugins/product-agent-os/assets/fixtures/codex-runner-missing-context/`
- `plugins/product-agent-os/assets/fixtures/codex-runner-handoff-incomplete/`
- `plugins/product-agent-os/assets/fixtures/codex-runner-approval-required/`
- `plugins/product-agent-os/assets/fixtures/codex-runner-automation-blocked/`
- `plugins/product-agent-os/assets/fixtures/codex-runner-secret-redaction/`

Modify docs/navigation:

- `mkdocs.yml`
- `docs/superpowers/plans/2026-05-15-product-agent-os-codex-runtime-runner.md`

## Contract Decisions

Use dictionaries and pure functions rather than dataclass instances as public return values. Existing plugin tests assert JSON-like dictionaries, and this keeps CLI output simple.

Status values:

- runner result: `route_ready`, `needs_context`, `needs_approval`, `blocked`, `completed`, `failed`;
- fixture eval runner status: `route_ready`, `needs_context`, `needs_approval`, `blocked`, `not_applicable`;
- source policy: reuse `ok`, `needs_review`, `blocked`;
- approval status: `not_required`, `required`, `approved`, `rejected`, `stale`.

Write policies:

- `read_only` - no approval required;
- `staged_only` - may propose staged artifacts but runner itself writes nothing by default;
- `approved_write` - requires explicit approval record before route readiness;
- `blocked` - unsafe or incomplete route.

Route mapping:

| State | Skill | Subagent role | Write policy |
| --- | --- | --- | --- |
| `uninitialized` | `workspace-discovery-auditor` | empty | `read_only` |
| `infrastructure_planned` | `requirements-author` | empty | `staged_only` |
| `requirements_ready` | `implementation-planner` | empty | `staged_only` |
| `plan_ready` | `agent-team-designer` | empty | `staged_only` |
| `team_ready` | `test-eval-designer` | empty | `staged_only` |
| `build_active` | empty | `builder` | `approved_write` |
| `quality_gate` | `risk-reviewer` | empty | `read_only` |
| `review_ready` | `pr-release-operator` | empty | `staged_only` |
| `release_ready` | `learning-loop-maintainer` | empty | `staged_only` |
| `learning_ready` | `automation-promoter` | empty | `staged_only` |
| `maintenance` | `project-lifecycle-orchestrator` | empty | `read_only` |

Lifecycle inference order:

1. If request explicitly provides a valid `task.lifecycle_state`, use it.
2. If `AGENTS.md` is missing, use `uninitialized`.
3. If `REQUIREMENTS.md` is missing or lacks acceptance criteria, use `infrastructure_planned`.
4. If `PLAN.md` is missing or lacks verification strategy, use `requirements_ready`.
5. If project agent configs are missing, use `plan_ready`.
6. If `TEST.md` or `EVALS.md` is missing required quality gates, use `team_ready`.
7. If `RUNLOG.md` contains build-active marker, use `build_active`.
8. If `RUNLOG.md` contains quality-gate marker, use `quality_gate`.
9. If `RUNLOG.md` contains review-ready marker, use `review_ready`.
10. If `RUNLOG.md` contains release-ready marker, use `release_ready`.
11. If `RUNLOG.md` contains learning-ready marker, use `learning_ready`.
12. Otherwise use `maintenance`.

Required marker strings are intentionally simple and synthetic-friendly:

- acceptance criteria: `Критерии приемки`;
- verification strategy: `Verification`;
- build active: `lifecycle_state: build_active`;
- quality gate: `lifecycle_state: quality_gate`;
- review ready: `lifecycle_state: review_ready`;
- release ready: `lifecycle_state: release_ready`;
- learning ready: `lifecycle_state: learning_ready`.

## Task 1: Runner Contract Tests

**Files:**

- Create: `tests/product_agent_os/test_codex_runtime_runner_contracts.py`
- Create: `plugins/product-agent-os/scripts/codex_runtime_runner/__init__.py`
- Create: `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`

- [ ] **Step 1: Write failing contract tests**

Create `tests/product_agent_os/test_codex_runtime_runner_contracts.py`:

```python
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.contracts import (  # noqa: E402
    ALLOWED_RUNNER_STATUSES,
    ALLOWED_RUNTIME_SURFACES,
    ALLOWED_WRITE_POLICIES,
    REQUIRED_RESULT_FIELDS,
    build_result,
    validate_runner_request,
    validate_runner_result,
)


class CodexRuntimeRunnerContractsTest(unittest.TestCase):
    def test_contract_enums_are_codex_only(self):
        self.assertIn("Codex App", ALLOWED_RUNTIME_SURFACES)
        self.assertIn("CLI", ALLOWED_RUNTIME_SURFACES)
        self.assertIn("IDE extension", ALLOWED_RUNTIME_SURFACES)
        self.assertIn("subagent", ALLOWED_RUNTIME_SURFACES)
        self.assertIn("skill", ALLOWED_RUNTIME_SURFACES)
        self.assertNotIn("Agents SDK", ALLOWED_RUNTIME_SURFACES)
        self.assertNotIn("api", {item.lower() for item in ALLOWED_RUNTIME_SURFACES})
        self.assertEqual(ALLOWED_WRITE_POLICIES, ["read_only", "staged_only", "approved_write", "blocked"])
        self.assertIn("route_ready", ALLOWED_RUNNER_STATUSES)

    def test_valid_runner_request_passes(self):
        request = self._valid_request()

        self.assertEqual(validate_runner_request(request), [])

    def test_runner_request_rejects_unknown_surface_and_writes_without_approval(self):
        request = self._valid_request()
        request["routing"]["preferred_surface"] = "external service"
        request["routing"]["allow_workspace_writes"] = True
        request["approval"]["approval_status"] = "required"

        errors = validate_runner_request(request)

        self.assertIn("routing.preferred_surface:unknown", errors)
        self.assertIn("routing.allow_workspace_writes:approval_required", errors)

    def test_build_result_returns_complete_shape(self):
        result = build_result(
            status="route_ready",
            workspace="C:/workspace/synthetic",
            lifecycle_state="quality_gate",
            route_packet={"write_policy": "read_only"},
            source_policy_status="ok",
            approval_status="not_required",
            next_action="Run risk-reviewer.",
        )

        self.assertEqual(list(result.keys()), REQUIRED_RESULT_FIELDS)
        self.assertEqual(validate_runner_result(result), [])
        self.assertEqual(result["redactions"], {"count": 0, "categories": []})

    def test_result_rejects_completion_claim_without_evidence(self):
        result = build_result(
            status="completed",
            workspace="C:/workspace/synthetic",
            lifecycle_state="review_ready",
            route_packet={"write_policy": "staged_only"},
            source_policy_status="ok",
            approval_status="not_required",
            next_action="No action.",
        )

        errors = validate_runner_result(result)

        self.assertIn("verification_evidence:required_for_completed", errors)

    def _valid_request(self):
        return {
            "schema_version": 1,
            "workspace": "C:/workspace/synthetic",
            "task": {
                "goal": "Prepare next Product-Agent OS action.",
                "lifecycle_state": "quality_gate",
                "constraints": ["Do not write files."],
                "allowed_sources": ["official docs", "repo artifacts"],
                "expected_artifacts": ["codex_runner_result"],
            },
            "routing": {
                "preferred_surface": "CLI",
                "allow_subagents": False,
                "allow_workspace_writes": False,
            },
            "approval": {
                "required": False,
                "approval_file": "",
                "approval_status": "not_required",
            },
        }


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run contract tests and verify failure**

Run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_contracts -v
```

Expected: FAIL because `codex_runtime_runner` does not exist.

- [ ] **Step 3: Implement package marker**

Create `plugins/product-agent-os/scripts/codex_runtime_runner/__init__.py`:

```python
"""Codex-only runtime runner helpers for the Product-Agent OS plugin."""

__version__ = "0.1.0"
```

- [ ] **Step 4: Implement contract validators**

Create `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`:

```python
from __future__ import annotations

from typing import Any


ALLOWED_RUNNER_STATUSES = ["route_ready", "needs_context", "needs_approval", "blocked", "completed", "failed"]
ALLOWED_RUNTIME_SURFACES = ["Codex App", "CLI", "IDE extension", "codex exec", "subagent", "skill"]
ALLOWED_WRITE_POLICIES = ["read_only", "staged_only", "approved_write", "blocked"]
ALLOWED_APPROVAL_STATUSES = ["not_required", "required", "approved", "rejected", "stale"]
ALLOWED_LIFECYCLE_STATES = [
    "uninitialized",
    "infrastructure_planned",
    "requirements_ready",
    "plan_ready",
    "team_ready",
    "build_active",
    "quality_gate",
    "review_ready",
    "release_ready",
    "learning_ready",
    "maintenance",
]
REQUIRED_RESULT_FIELDS = [
    "schema_version",
    "status",
    "workspace",
    "lifecycle_state",
    "route_packet",
    "handoffs",
    "files_touched",
    "files_proposed",
    "verification_evidence",
    "source_policy_status",
    "approval_status",
    "redactions",
    "errors",
    "warnings",
    "next_action",
]


def validate_runner_request(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("schema_version") != 1:
        errors.append("schema_version:must_be_1")
    if not _non_empty_string(payload.get("workspace")):
        errors.append("workspace:required")
    task = payload.get("task")
    routing = payload.get("routing")
    approval = payload.get("approval")
    if not isinstance(task, dict):
        errors.append("task:required")
        task = {}
    if not isinstance(routing, dict):
        errors.append("routing:required")
        routing = {}
    if not isinstance(approval, dict):
        errors.append("approval:required")
        approval = {}
    state = task.get("lifecycle_state")
    if state not in ("", None) and state not in ALLOWED_LIFECYCLE_STATES:
        errors.append("task.lifecycle_state:unknown")
    for field in ["constraints", "allowed_sources", "expected_artifacts"]:
        if field in task and not isinstance(task[field], list):
            errors.append(f"task.{field}:invalid")
    surface = routing.get("preferred_surface")
    if surface not in ALLOWED_RUNTIME_SURFACES:
        errors.append("routing.preferred_surface:unknown")
    if not isinstance(routing.get("allow_subagents"), bool):
        errors.append("routing.allow_subagents:invalid")
    if not isinstance(routing.get("allow_workspace_writes"), bool):
        errors.append("routing.allow_workspace_writes:invalid")
    approval_status = approval.get("approval_status")
    if approval_status not in ALLOWED_APPROVAL_STATUSES:
        errors.append("approval.approval_status:unknown")
    if routing.get("allow_workspace_writes") and approval_status != "approved":
        errors.append("routing.allow_workspace_writes:approval_required")
    return errors


def build_result(
    *,
    status: str,
    workspace: str,
    lifecycle_state: str,
    route_packet: dict[str, Any],
    source_policy_status: str,
    approval_status: str,
    next_action: str,
    handoffs: list[dict[str, Any]] | None = None,
    files_touched: list[str] | None = None,
    files_proposed: list[str] | None = None,
    verification_evidence: list[str] | None = None,
    redactions: dict[str, Any] | None = None,
    errors: list[str] | None = None,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "status": status,
        "workspace": workspace,
        "lifecycle_state": lifecycle_state,
        "route_packet": route_packet,
        "handoffs": handoffs or [],
        "files_touched": files_touched or [],
        "files_proposed": files_proposed or [],
        "verification_evidence": verification_evidence or [],
        "source_policy_status": source_policy_status,
        "approval_status": approval_status,
        "redactions": redactions or {"count": 0, "categories": []},
        "errors": errors or [],
        "warnings": warnings or [],
        "next_action": next_action,
    }


def validate_runner_result(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if list(payload.keys()) != REQUIRED_RESULT_FIELDS:
        errors.append("result:field_order_or_shape")
    if payload.get("schema_version") != 1:
        errors.append("schema_version:must_be_1")
    if payload.get("status") not in ALLOWED_RUNNER_STATUSES:
        errors.append("status:unknown")
    if payload.get("lifecycle_state") not in ALLOWED_LIFECYCLE_STATES:
        errors.append("lifecycle_state:unknown")
    if not isinstance(payload.get("route_packet"), dict):
        errors.append("route_packet:invalid")
    for field in ["handoffs", "files_touched", "files_proposed", "verification_evidence", "errors", "warnings"]:
        if not isinstance(payload.get(field), list):
            errors.append(f"{field}:invalid")
    redactions = payload.get("redactions")
    if not isinstance(redactions, dict) or not isinstance(redactions.get("count"), int):
        errors.append("redactions:invalid")
    if payload.get("status") == "completed" and not payload.get("verification_evidence"):
        errors.append("verification_evidence:required_for_completed")
    return errors


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())
```

- [ ] **Step 5: Run contract tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_contracts -v
```

Expected: PASS.

## Task 2: Context Loader And Lifecycle State

**Files:**

- Create: `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`
- Create: `plugins/product-agent-os/scripts/codex_runtime_runner/context_loader.py`
- Create: `plugins/product-agent-os/scripts/codex_runtime_runner/state.py`

- [ ] **Step 1: Write failing state tests**

Create `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`:

```python
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.context_loader import load_control_plane_context  # noqa: E402
from codex_runtime_runner.routes import plan_route  # noqa: E402
from codex_runtime_runner.state import infer_lifecycle_state  # noqa: E402


class CodexRuntimeRunnerStateRoutesTest(unittest.TestCase):
    def test_missing_agents_is_uninitialized(self):
        with tempfile.TemporaryDirectory() as tmp:
            context = load_control_plane_context(Path(tmp))

        self.assertEqual(infer_lifecycle_state(context, {}), "uninitialized")

    def test_missing_plan_after_requirements_is_requirements_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, omit={"PLAN.md"})
            context = load_control_plane_context(workspace)

        self.assertEqual(infer_lifecycle_state(context, {}), "requirements_ready")

    def test_request_lifecycle_override_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace)
            context = load_control_plane_context(workspace)

        self.assertEqual(
            infer_lifecycle_state(context, {"task": {"lifecycle_state": "quality_gate"}}),
            "quality_gate",
        )

    def test_route_maps_quality_gate_to_risk_reviewer(self):
        route = plan_route("quality_gate", allow_subagents=False)

        self.assertEqual(route["recommended_skill"], "risk-reviewer")
        self.assertEqual(route["recommended_subagent_role"], "")
        self.assertEqual(route["write_policy"], "read_only")
        self.assertIn("python", " ".join(route["verification"]))

    def test_build_active_uses_builder_subagent_and_requires_approval(self):
        route = plan_route("build_active", allow_subagents=True)

        self.assertEqual(route["recommended_skill"], "")
        self.assertEqual(route["recommended_subagent_role"], "builder")
        self.assertEqual(route["write_policy"], "approved_write")
        self.assertTrue(route["approval_requirements"])

    def _write_control_plane(self, workspace: Path, omit: set[str] | None = None) -> None:
        omit = omit or set()
        content = {
            "AGENTS.md": "# Rules\n",
            "REQUIREMENTS.md": "# Requirements\n\n## Критерии приемки\n\n- Synthetic acceptance.\n",
            "PLAN.md": "# Plan\n\n## Verification\n\n- Run unit tests.\n",
            "TEST.md": "# Test\n\nQuality gates: unit tests.\n",
            "EVALS.md": "# Evals\n\nQuality gates: fixture eval.\n",
            "RUNLOG.md": "# Runlog\n\nNo active lifecycle marker.\n",
        }
        for name, text in content.items():
            if name not in omit:
                (workspace / name).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run state tests and verify failure**

Run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_state_routes -v
```

Expected: FAIL because `context_loader`, `state`, and `routes` do not exist.

- [ ] **Step 3: Implement context loader**

Create `plugins/product-agent-os/scripts/codex_runtime_runner/context_loader.py`:

```python
from __future__ import annotations

from pathlib import Path
from typing import Any


CONTROL_PLANE_FILES = ["AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]


def load_control_plane_context(workspace: str | Path) -> dict[str, Any]:
    root = Path(workspace)
    files: dict[str, dict[str, Any]] = {}
    for name in CONTROL_PLANE_FILES:
        path = root / name
        files[name] = _read_file(path)
    return {
        "workspace": str(root),
        "exists": root.exists(),
        "is_dir": root.is_dir(),
        "files": files,
        "missing": [name for name, item in files.items() if not item["exists"]],
        "unreadable": [name for name, item in files.items() if item["exists"] and item["error"]],
    }


def _read_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "text": "", "error": ""}
    if not path.is_file():
        return {"exists": True, "text": "", "error": "not a file"}
    try:
        return {"exists": True, "text": path.read_text(encoding="utf-8"), "error": ""}
    except (OSError, UnicodeDecodeError):
        return {"exists": True, "text": "", "error": "unable to read file as utf-8 text"}
```

- [ ] **Step 4: Implement lifecycle state detector**

Create `plugins/product-agent-os/scripts/codex_runtime_runner/state.py`:

```python
from __future__ import annotations

from typing import Any

from codex_runtime_runner.contracts import ALLOWED_LIFECYCLE_STATES


def infer_lifecycle_state(context: dict[str, Any], request: dict[str, Any]) -> str:
    requested = request.get("task", {}).get("lifecycle_state") if isinstance(request.get("task"), dict) else ""
    if requested in ALLOWED_LIFECYCLE_STATES:
        return str(requested)
    files = context.get("files", {})
    if not files.get("AGENTS.md", {}).get("exists"):
        return "uninitialized"
    requirements = files.get("REQUIREMENTS.md", {}).get("text", "")
    if not requirements or "Критерии приемки" not in requirements:
        return "infrastructure_planned"
    plan = files.get("PLAN.md", {}).get("text", "")
    if not plan or "Verification" not in plan:
        return "requirements_ready"
    if not _has_agent_config(context):
        return "plan_ready"
    test_text = files.get("TEST.md", {}).get("text", "")
    evals_text = files.get("EVALS.md", {}).get("text", "")
    if "Quality gates" not in test_text or "Quality gates" not in evals_text:
        return "team_ready"
    runlog = files.get("RUNLOG.md", {}).get("text", "")
    for state in ["build_active", "quality_gate", "review_ready", "release_ready", "learning_ready"]:
        if f"lifecycle_state: {state}" in runlog:
            return state
    return "maintenance"


def _has_agent_config(context: dict[str, Any]) -> bool:
    workspace = str(context.get("workspace", ""))
    if not workspace:
        return False
    from pathlib import Path

    return (Path(workspace) / ".codex" / "agents" / "builder.toml").exists()
```

- [ ] **Step 5: Run state tests until only route import fails**

Run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_state_routes -v
```

Expected: FAIL because `codex_runtime_runner.routes` does not exist.

## Task 3: Route Planner

**Files:**

- Create: `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`
- Modify: `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`

- [ ] **Step 1: Implement route planner**

Create `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`:

```python
from __future__ import annotations

from typing import Any


ROUTES = {
    "uninitialized": ("workspace-discovery-auditor", "", "read_only", "Audit workspace readiness."),
    "infrastructure_planned": ("requirements-author", "", "staged_only", "Draft requirements packet."),
    "requirements_ready": ("implementation-planner", "", "staged_only", "Draft implementation plan."),
    "plan_ready": ("agent-team-designer", "", "staged_only", "Design ownership and handoffs."),
    "team_ready": ("test-eval-designer", "", "staged_only", "Define quality gates."),
    "build_active": ("", "builder", "approved_write", "Execute one approved build slice."),
    "quality_gate": ("risk-reviewer", "", "read_only", "Review risks and verification evidence."),
    "review_ready": ("pr-release-operator", "", "staged_only", "Prepare PR or release packet."),
    "release_ready": ("learning-loop-maintainer", "", "staged_only", "Capture learnings and failures."),
    "learning_ready": ("automation-promoter", "", "staged_only", "Evaluate candidate-only automation."),
    "maintenance": ("project-lifecycle-orchestrator", "", "read_only", "Route maintenance work."),
}


def plan_route(lifecycle_state: str, *, allow_subagents: bool) -> dict[str, Any]:
    skill, subagent, write_policy, action = ROUTES[lifecycle_state]
    if subagent and not allow_subagents:
        skill = "project-lifecycle-orchestrator"
        subagent = ""
    approval_requirements = ["explicit approval record required before workspace writes"] if write_policy == "approved_write" else []
    return {
        "lifecycle_state": lifecycle_state,
        "next_action": action,
        "recommended_skill": skill,
        "recommended_subagent_role": subagent,
        "runtime_surface": "subagent" if subagent else "skill",
        "write_policy": write_policy,
        "required_inputs": ["AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"],
        "expected_outputs": ["codex_runner_result", "handoff packet"],
        "verification": [
            "python -m unittest discover -s tests -p \"test_*.py\" -v",
            "python plugins\\product-agent-os\\scripts\\run_fixture_eval.py",
        ],
        "approval_requirements": approval_requirements,
        "stop_conditions": [
            "missing required control-plane context",
            "blocked source policy",
            "missing approval for approved_write route",
            "active automation request",
        ],
    }
```

- [ ] **Step 2: Run state and route tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_state_routes -v
```

Expected: PASS.

## Task 4: Redaction And Guard Validators

**Files:**

- Create: `tests/product_agent_os/test_codex_runtime_runner_guards.py`
- Create: `plugins/product-agent-os/scripts/codex_runtime_runner/redaction.py`
- Create: `plugins/product-agent-os/scripts/codex_runtime_runner/guards.py`

- [ ] **Step 1: Write failing guard tests**

Create `tests/product_agent_os/test_codex_runtime_runner_guards.py`:

```python
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.guards import (  # noqa: E402
    validate_approval_boundary,
    validate_automation_boundary,
    validate_codex_handoff,
    validate_route_packet,
)
from codex_runtime_runner.redaction import redact_text, validate_redaction  # noqa: E402


class CodexRuntimeRunnerGuardsTest(unittest.TestCase):
    def test_approved_write_route_requires_approval(self):
        route = {"write_policy": "approved_write", "approval_requirements": ["approval required"]}

        errors = validate_approval_boundary(route, {"approval_status": "required"})

        self.assertIn("approval:required_for_write", errors)

    def test_read_only_route_does_not_require_approval(self):
        route = {"write_policy": "read_only", "approval_requirements": []}

        self.assertEqual(validate_approval_boundary(route, {"approval_status": "not_required"}), [])

    def test_route_packet_rejects_unknown_skill_for_state(self):
        route = {
            "lifecycle_state": "quality_gate",
            "recommended_skill": "requirements-author",
            "recommended_subagent_role": "",
            "write_policy": "read_only",
        }

        errors = validate_route_packet(route)

        self.assertIn("route:unexpected_skill_for_state", errors)

    def test_handoff_requires_constraints_and_evidence(self):
        handoff = {
            "lifecycle_state": "quality_gate",
            "role": "risk-reviewer",
            "goal": "Review release risk.",
            "constraints": [],
            "sources_used": [],
            "assumptions": [],
            "verified_claims": [],
            "unsupported_claims": [],
            "files_touched": [],
            "files_proposed": ["RUNLOG.md"],
            "commands_run": [],
            "verification_evidence": [],
            "approval_requirements": [],
            "open_risks": [],
            "recommended_next_role": "",
            "stop_reason": "",
        }

        errors = validate_codex_handoff(handoff)

        self.assertIn("constraints:empty", errors)
        self.assertIn("verification_evidence:empty", errors)

    def test_active_automation_request_is_blocked(self):
        text = "Create active recurring automation after this run."

        self.assertIn("automation:active_request_blocked", validate_automation_boundary(text))

    def test_redaction_removes_secret_like_and_absolute_path_values(self):
        text = "TOKEN=fixture-secret\nPath C:\\Users\\person\\project\\file.txt\nraw private chat log"

        redacted, report = redact_text(text)

        self.assertNotIn("fixture-secret", redacted)
        self.assertNotIn("C:\\Users\\person", redacted)
        self.assertIn("secret", report["categories"])
        self.assertIn("absolute_path", report["categories"])
        self.assertEqual(validate_redaction(redacted), [])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run guard tests and verify failure**

Run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_guards -v
```

Expected: FAIL because `guards` and `redaction` do not exist.

- [ ] **Step 3: Implement redaction**

Create `plugins/product-agent-os/scripts/codex_runtime_runner/redaction.py`:

```python
from __future__ import annotations

import re


SECRET_ASSIGNMENT = re.compile(r"(?im)^\\s*[A-Z_]*(?:SECRET|TOKEN|PASSWORD|KEY)[A-Z_]*\\s*[=:]\\s*[^\\r\\n]+")
WINDOWS_USER_PATH = re.compile(r"C:\\\\Users\\\\[^\\s\\\\]+(?:\\\\[^\\s]+)*", re.IGNORECASE)
PRIVATE_MARKERS = re.compile(r"(?i)(private customer data|raw private chat log|raw chat log)")


def redact_text(text: str) -> tuple[str, dict[str, object]]:
    categories: list[str] = []
    redacted = text
    redacted, secret_count = SECRET_ASSIGNMENT.subn("[REDACTED_SECRET_ASSIGNMENT]", redacted)
    if secret_count:
        categories.append("secret")
    redacted, path_count = WINDOWS_USER_PATH.subn("[REDACTED_LOCAL_PATH]", redacted)
    if path_count:
        categories.append("absolute_path")
    redacted, private_count = PRIVATE_MARKERS.subn("[REDACTED_PRIVATE_DATA]", redacted)
    if private_count:
        categories.append("private_data")
    return redacted, {"count": secret_count + path_count + private_count, "categories": sorted(set(categories))}


def validate_redaction(text: str) -> list[str]:
    errors: list[str] = []
    if SECRET_ASSIGNMENT.search(text):
        errors.append("redaction:secret_retained")
    if WINDOWS_USER_PATH.search(text):
        errors.append("redaction:absolute_path_retained")
    if PRIVATE_MARKERS.search(text):
        errors.append("redaction:private_data_retained")
    return errors
```

- [ ] **Step 4: Implement guard validators**

Create `plugins/product-agent-os/scripts/codex_runtime_runner/guards.py`:

```python
from __future__ import annotations

import re
from typing import Any

from codex_runtime_runner.routes import ROUTES


ACTIVE_AUTOMATION_PATTERN = re.compile(r"(?i)\\b(active|recurring|scheduled)\\s+automation\\b|\\bcreate\\s+.*automation\\b")


def validate_route_packet(route: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    state = route.get("lifecycle_state")
    expected = ROUTES.get(str(state))
    if not expected:
        return ["route:lifecycle_state_unknown"]
    expected_skill, expected_subagent, expected_write_policy, _ = expected
    if route.get("write_policy") != expected_write_policy:
        errors.append("route:unexpected_write_policy_for_state")
    if expected_skill and route.get("recommended_skill") != expected_skill:
        errors.append("route:unexpected_skill_for_state")
    if expected_subagent and route.get("recommended_subagent_role") not in {expected_subagent, ""}:
        errors.append("route:unexpected_subagent_for_state")
    return errors


def validate_approval_boundary(route: dict[str, Any], approval: dict[str, Any]) -> list[str]:
    write_policy = route.get("write_policy")
    approval_status = approval.get("approval_status")
    if write_policy == "approved_write" and approval_status != "approved":
        return ["approval:required_for_write"]
    return []


def validate_codex_handoff(handoff: dict[str, Any]) -> list[str]:
    required = [
        "lifecycle_state",
        "role",
        "goal",
        "constraints",
        "sources_used",
        "assumptions",
        "verified_claims",
        "unsupported_claims",
        "files_touched",
        "files_proposed",
        "commands_run",
        "verification_evidence",
        "approval_requirements",
        "open_risks",
        "recommended_next_role",
        "stop_reason",
    ]
    errors = [field for field in required if field not in handoff]
    for field in ["constraints", "verification_evidence"]:
        value = handoff.get(field)
        if value is not None and not isinstance(value, list):
            errors.append(f"{field}:invalid")
        elif value == []:
            errors.append(f"{field}:empty")
    for field in ["files_touched", "files_proposed"]:
        if field in handoff and not isinstance(handoff[field], list):
            errors.append(f"{field}:invalid")
    if handoff.get("files_touched") == [] and handoff.get("files_proposed") == []:
        errors.append("files:empty")
    return errors


def validate_automation_boundary(text: str) -> list[str]:
    if ACTIVE_AUTOMATION_PATTERN.search(text):
        return ["automation:active_request_blocked"]
    return []
```

- [ ] **Step 5: Run guard tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_guards -v
```

Expected: PASS.

## Task 5: Contract-Mode CLI Runner

**Files:**

- Create: `tests/product_agent_os/test_codex_runtime_runner_cli.py`
- Create: `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`
- Create: `plugins/product-agent-os/scripts/run_codex_runtime_runner.py`
- Create: `plugins/product-agent-os/scripts/validate_codex_runtime_runner.py`

- [ ] **Step 1: Write failing CLI tests**

Create `tests/product_agent_os/test_codex_runtime_runner_cli.py`:

```python
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
WRAPPER = SCRIPTS / "run_codex_runtime_runner.py"
VALIDATOR = SCRIPTS / "validate_codex_runtime_runner.py"


class CodexRuntimeRunnerCliTest(unittest.TestCase):
    def test_contract_cli_returns_route_ready_for_quality_gate_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: quality_gate")
            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--contract"],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(payload["status"], "route_ready")
        self.assertEqual(payload["lifecycle_state"], "quality_gate")
        self.assertEqual(payload["route_packet"]["recommended_skill"], "risk-reviewer")

    def test_contract_cli_requires_contract_flag(self):
        result = subprocess.run(
            [sys.executable, str(WRAPPER), "."],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("choose --contract", result.stderr)

    def test_contract_cli_returns_needs_approval_for_build_active_without_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: build_active")
            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--contract", "--allow-subagents"],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload["status"], "needs_approval")
        self.assertEqual(payload["route_packet"]["write_policy"], "approved_write")

    def test_validator_accepts_valid_result_json_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: quality_gate")
            output = Path(tmp) / "result.json"
            run_result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--contract", "--output", str(output)],
                check=False,
                capture_output=True,
                text=True,
            )
            validate_result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(output)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(run_result.returncode, 0)
        self.assertEqual(validate_result.returncode, 0, validate_result.stdout + validate_result.stderr)
        self.assertIn('"ok": true', validate_result.stdout)

    def _write_control_plane(self, workspace: Path, runlog_marker: str) -> None:
        (workspace / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
        (workspace / "REQUIREMENTS.md").write_text("# Requirements\n\n## Критерии приемки\n\n- Synthetic.\n", encoding="utf-8")
        (workspace / "PLAN.md").write_text("# Plan\n\n## Verification\n\n- Run tests.\n", encoding="utf-8")
        (workspace / "TEST.md").write_text("# Test\n\nQuality gates: unit tests.\n", encoding="utf-8")
        (workspace / "EVALS.md").write_text("# Evals\n\nQuality gates: fixture eval.\n", encoding="utf-8")
        (workspace / "RUNLOG.md").write_text(f"# Runlog\n\n{runlog_marker}\n", encoding="utf-8")
        agents = workspace / ".codex" / "agents"
        agents.mkdir(parents=True)
        (agents / "builder.toml").write_text('name = "builder"\n', encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run CLI tests and verify failure**

Run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_cli -v
```

Expected: FAIL because CLI files do not exist.

- [ ] **Step 3: Implement CLI orchestration**

Create `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`:

```python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from codex_runtime_runner.context_loader import load_control_plane_context
from codex_runtime_runner.contracts import build_result, validate_runner_result
from codex_runtime_runner.guards import validate_approval_boundary, validate_route_packet
from codex_runtime_runner.redaction import redact_text, validate_redaction
from codex_runtime_runner.routes import plan_route
from codex_runtime_runner.state import infer_lifecycle_state


def run_contract(workspace: str | Path, *, allow_subagents: bool = False, approval_status: str = "not_required") -> dict[str, Any]:
    context = load_control_plane_context(workspace)
    request = {
        "task": {"lifecycle_state": ""},
        "routing": {"allow_subagents": allow_subagents, "allow_workspace_writes": False},
        "approval": {"approval_status": approval_status},
    }
    state = infer_lifecycle_state(context, request)
    route = plan_route(state, allow_subagents=allow_subagents)
    errors = []
    warnings = []
    if context["unreadable"]:
        errors.extend(f"context:unreadable:{name}" for name in context["unreadable"])
    route_errors = validate_route_packet(route)
    approval_errors = validate_approval_boundary(route, {"approval_status": approval_status})
    errors.extend(route_errors)
    if approval_errors:
        warnings.extend(approval_errors)
    status = _status_for(context, route, errors, approval_errors)
    result = build_result(
        status=status,
        workspace=str(workspace),
        lifecycle_state=state,
        route_packet=route,
        source_policy_status="not_evaluated",
        approval_status=approval_status,
        next_action=route["next_action"],
        files_proposed=[] if route["write_policy"] == "read_only" else ["staged handoff packet"],
        verification_evidence=["codex_runtime_runner contract mode completed"] if status == "route_ready" else [],
        errors=errors,
        warnings=warnings,
    )
    redacted_text, redactions = redact_text(json.dumps(result, sort_keys=True))
    result = json.loads(redacted_text)
    result["redactions"] = redactions
    result["errors"].extend(validate_redaction(json.dumps(result, sort_keys=True)))
    result["errors"].extend(validate_runner_result(result))
    if result["errors"] and result["status"] == "route_ready":
        result["status"] = "blocked"
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Product-Agent OS Codex runtime runner in contract mode.")
    parser.add_argument("workspace")
    parser.add_argument("--contract", action="store_true", help="Run deterministic offline contract mode.")
    parser.add_argument("--allow-subagents", action="store_true", help="Allow subagent route recommendations.")
    parser.add_argument("--approval-status", default="not_required")
    parser.add_argument("--output", help="Optional JSON output file.")
    args = parser.parse_args(argv)
    if not args.contract:
        print("error: choose --contract", file=sys.stderr)
        return 2
    result = run_contract(args.workspace, allow_subagents=args.allow_subagents, approval_status=args.approval_status)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if result["status"] == "route_ready" else 1


def _status_for(
    context: dict[str, Any],
    route: dict[str, Any],
    errors: list[str],
    approval_errors: list[str],
) -> str:
    if errors:
        return "blocked"
    if context["missing"] and route["lifecycle_state"] != "uninitialized":
        return "needs_context"
    if approval_errors:
        return "needs_approval"
    return "route_ready"
```

- [ ] **Step 4: Add CLI wrapper**

Create `plugins/product-agent-os/scripts/run_codex_runtime_runner.py`:

```python
from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from codex_runtime_runner.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 5: Add validator wrapper**

Create `plugins/product-agent-os/scripts/validate_codex_runtime_runner.py`:

```python
from __future__ import annotations

import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from codex_runtime_runner.contracts import validate_runner_result  # noqa: E402


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: validate_codex_runtime_runner.py <result-json>", file=sys.stderr)
        return 2
    path = Path(argv[0])
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1
    errors = validate_runner_result(payload)
    print(json.dumps({"ok": not errors, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 6: Run CLI tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_cli -v
```

Expected: PASS.

## Task 6: Synthetic Runner Fixtures

**Files:**

- Modify: `tests/product_agent_os/test_fixtures.py`
- Create fixture folders under `plugins/product-agent-os/assets/fixtures/`

- [ ] **Step 1: Add failing fixture inventory test**

Modify `tests/product_agent_os/test_fixtures.py` by adding these names to `test_required_fixture_projects_exist`:

```python
"codex-runner-ready",
"codex-runner-missing-context",
"codex-runner-handoff-incomplete",
"codex-runner-approval-required",
"codex-runner-automation-blocked",
"codex-runner-secret-redaction",
```

Add:

```python
def test_codex_runner_fixtures_are_synthetic(self):
    for name in [
        "codex-runner-ready",
        "codex-runner-missing-context",
        "codex-runner-handoff-incomplete",
        "codex-runner-approval-required",
        "codex-runner-automation-blocked",
        "codex-runner-secret-redaction",
    ]:
        with self.subTest(name=name):
            text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in (FIXTURES / name).rglob("*")
                if path.is_file()
            )
            self.assertIn("Synthetic", text)
            self.assertNotIn("private customer", text.lower())
```

- [ ] **Step 2: Run fixture test and verify failure**

Run:

```powershell
python -m unittest tests.product_agent_os.test_fixtures -v
```

Expected: FAIL because runner fixtures do not exist.

- [ ] **Step 3: Create ready fixture**

Create `plugins/product-agent-os/assets/fixtures/codex-runner-ready/` with:

`AGENTS.md`:

```markdown
# Synthetic Product-Agent OS Rules

Synthetic fixture only.
```

`REQUIREMENTS.md`:

```markdown
# Synthetic Requirements

## Критерии приемки

- Synthetic route can reach quality gate.
```

`PLAN.md`:

```markdown
# Synthetic Plan

## Verification

- Run unit tests.
```

`TEST.md`:

```markdown
# Synthetic Test

Quality gates: unit tests and fixture eval.
```

`EVALS.md`:

```markdown
# Synthetic Evals

Quality gates: runner contract eval.
```

`RUNLOG.md`:

```markdown
# Synthetic Runlog

lifecycle_state: quality_gate
```

Also create `.codex/agents/builder.toml`:

```toml
name = "builder"
```

- [ ] **Step 4: Create missing context fixture**

Create `plugins/product-agent-os/assets/fixtures/codex-runner-missing-context/` with `AGENTS.md`, `REQUIREMENTS.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, but intentionally omit `PLAN.md`. Use synthetic text and include `## Критерии приемки` in `REQUIREMENTS.md`.

- [ ] **Step 5: Create approval-required fixture**

Create `plugins/product-agent-os/assets/fixtures/codex-runner-approval-required/` with the same complete files as ready fixture, but `RUNLOG.md` contains:

```markdown
# Synthetic Runlog

lifecycle_state: build_active
```

Create `.codex/agents/builder.toml` with `name = "builder"`.

- [ ] **Step 6: Create guard fixture markers**

Create `plugins/product-agent-os/assets/fixtures/codex-runner-handoff-incomplete/RUNLOG.md`:

```markdown
# Synthetic Runlog

expected_codex_runner_check: handoff_incomplete_blocked
```

Create `plugins/product-agent-os/assets/fixtures/codex-runner-automation-blocked/RUNLOG.md`:

```markdown
# Synthetic Runlog

expected_codex_runner_check: active_automation_blocked
Synthetic request asks for active recurring automation.
```

Create `plugins/product-agent-os/assets/fixtures/codex-runner-secret-redaction/RUNLOG.md`:

```markdown
# Synthetic Runlog

expected_codex_runner_check: secret_redaction_enforced
Synthetic redaction input contains token-like text and a local user path.
```

- [ ] **Step 7: Run fixture tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_fixtures -v
```

Expected: PASS.

## Task 7: Fixture Eval Extension

**Files:**

- Create: `tests/product_agent_os/test_codex_runtime_runner_fixture_eval.py`
- Modify: `tests/product_agent_os/test_fixture_eval_runner.py`
- Modify: `plugins/product-agent-os/scripts/run_fixture_eval.py`

- [ ] **Step 1: Write failing runner fixture eval tests**

Create `tests/product_agent_os/test_codex_runtime_runner_fixture_eval.py`:

```python
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = ROOT / "plugins" / "product-agent-os" / "scripts" / "run_fixture_eval.py"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"


def load_runner():
    spec = importlib.util.spec_from_file_location("run_fixture_eval", RUNNER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CodexRuntimeRunnerFixtureEvalTest(unittest.TestCase):
    def test_ready_fixture_reports_route_ready(self):
        runner = load_runner()

        result = runner.evaluate_fixture(FIXTURES / "codex-runner-ready")

        self.assertEqual(result["codex_runtime_runner_status"], "route_ready")
        self.assertTrue(result["codex_runtime_runner_checks"]["contract_mode_offline"])
        self.assertTrue(result["codex_runtime_runner_checks"]["route_matches_lifecycle_state"])
        self.assertTrue(result["ok"])

    def test_missing_context_fixture_reports_needs_context(self):
        runner = load_runner()

        result = runner.evaluate_fixture(FIXTURES / "codex-runner-missing-context")

        self.assertEqual(result["codex_runtime_runner_status"], "needs_context")
        self.assertTrue(result["codex_runtime_runner_checks"]["missing_context_detected"])

    def test_approval_fixture_reports_needs_approval(self):
        runner = load_runner()

        result = runner.evaluate_fixture(FIXTURES / "codex-runner-approval-required")

        self.assertEqual(result["codex_runtime_runner_status"], "needs_approval")
        self.assertTrue(result["codex_runtime_runner_checks"]["approval_required_for_writes"])

    def test_guard_fixtures_are_checked(self):
        runner = load_runner()
        results = {item["fixture"]: item for item in runner.evaluate_all()}

        self.assertTrue(results["codex-runner-handoff-incomplete"]["codex_runtime_runner_checks"]["handoff_incomplete_blocked"])
        self.assertTrue(results["codex-runner-automation-blocked"]["codex_runtime_runner_checks"]["active_automation_blocked"])
        self.assertTrue(results["codex-runner-secret-redaction"]["codex_runtime_runner_checks"]["secret_redaction_enforced"])


if __name__ == "__main__":
    unittest.main()
```

Modify `tests/product_agent_os/test_fixture_eval_runner.py` expected result keys by adding:

```python
"codex_runtime_runner_status",
"codex_runtime_runner_checks",
```

Add matching type assertions:

```python
self.assertIsInstance(item["codex_runtime_runner_status"], str)
self.assertIsInstance(item["codex_runtime_runner_checks"], dict)
```

- [ ] **Step 2: Run fixture eval tests and verify failure**

Run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_fixture_eval tests.product_agent_os.test_fixture_eval_runner -v
```

Expected: FAIL because fixture eval does not include runner fields.

- [ ] **Step 3: Extend fixture eval defaults**

Modify `_failed_result` in `plugins/product-agent-os/scripts/run_fixture_eval.py` to include:

```python
"codex_runtime_runner_status": "",
"codex_runtime_runner_checks": {},
```

Modify all test stub result dictionaries in `tests/product_agent_os/test_fixture_eval_runner.py` to include the same keys.

- [ ] **Step 4: Import runner helpers**

Add imports in `plugins/product-agent-os/scripts/run_fixture_eval.py`:

```python
from codex_runtime_runner.cli import run_contract  # noqa: E402
from codex_runtime_runner.guards import validate_automation_boundary, validate_codex_handoff  # noqa: E402
from codex_runtime_runner.redaction import redact_text, validate_redaction  # noqa: E402
```

- [ ] **Step 5: Add runner eval helper**

Add to `plugins/product-agent-os/scripts/run_fixture_eval.py`:

```python
def _codex_runtime_runner_eval(path: Path) -> tuple[str, dict[str, bool]]:
    if not path.name.startswith("codex-runner-"):
        return "not_applicable", {}
    checks: dict[str, bool] = {"contract_mode_offline": True}
    if path.name == "codex-runner-ready":
        result = run_contract(path)
        checks["route_matches_lifecycle_state"] = (
            result["lifecycle_state"] == "quality_gate"
            and result["route_packet"]["recommended_skill"] == "risk-reviewer"
        )
        return str(result["status"]), checks
    if path.name == "codex-runner-missing-context":
        result = run_contract(path)
        checks["missing_context_detected"] = result["status"] == "needs_context"
        return str(result["status"]), checks
    if path.name == "codex-runner-approval-required":
        result = run_contract(path, allow_subagents=True)
        checks["approval_required_for_writes"] = result["status"] == "needs_approval"
        return str(result["status"]), checks
    if path.name == "codex-runner-handoff-incomplete":
        errors = validate_codex_handoff({"lifecycle_state": "quality_gate", "constraints": [], "verification_evidence": []})
        checks["handoff_incomplete_blocked"] = "constraints:empty" in errors and "verification_evidence:empty" in errors
        return "blocked", checks
    if path.name == "codex-runner-automation-blocked":
        errors = validate_automation_boundary((path / "RUNLOG.md").read_text(encoding="utf-8"))
        checks["active_automation_blocked"] = "automation:active_request_blocked" in errors
        return "blocked", checks
    if path.name == "codex-runner-secret-redaction":
        redacted, _report = redact_text("TOKEN=fixture-secret\nC:\\Users\\person\\workspace")
        checks["secret_redaction_enforced"] = validate_redaction(redacted) == []
        return "blocked", checks
    return "not_applicable", {}
```

- [ ] **Step 6: Wire runner eval into `evaluate_fixture`**

Inside `evaluate_fixture`, after existing Track 4 status helpers:

```python
codex_runtime_runner_status, codex_runtime_runner_checks = _codex_runtime_runner_eval(path)
expected_checks.update(codex_runtime_runner_checks)
```

Add returned keys:

```python
"codex_runtime_runner_status": codex_runtime_runner_status,
"codex_runtime_runner_checks": codex_runtime_runner_checks,
```

Ensure `renderer_ok` remains:

```python
renderer_ok = (
    bool(renderer_validation.get("ok"))
    and renderer_status in {"needs_approval", "blocked"}
    and all(expected_checks.values())
)
```

This keeps runner fixtures green only when runner-specific checks are true.

- [ ] **Step 7: Run fixture eval tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_fixture_eval tests.product_agent_os.test_fixture_eval_runner -v
```

Expected: PASS.

## Task 8: Plugin Inactive Boundary

**Files:**

- Modify: `tests/product_agent_os/test_plugin_structure.py`

- [ ] **Step 1: Add failing inactive-boundary test**

Modify `tests/product_agent_os/test_plugin_structure.py` by adding:

```python
def test_codex_runtime_runner_exists_but_is_not_default_activated(self):
    runner_package = PLUGIN_ROOT / "scripts" / "codex_runtime_runner"
    runner_wrapper = PLUGIN_ROOT / "scripts" / "run_codex_runtime_runner.py"
    manifest_path = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
    manifest_text = manifest_path.read_text(encoding="utf-8")
    mcp_text = (PLUGIN_ROOT / ".mcp.json").read_text(encoding="utf-8")

    self.assertTrue(runner_package.is_dir())
    self.assertTrue(runner_wrapper.exists())
    self.assertNotIn("run_codex_runtime_runner.py", manifest_text)
    self.assertNotIn("codex_runtime_runner", manifest_text)
    self.assertNotIn("codex_runtime_runner", mcp_text)
```

- [ ] **Step 2: Run plugin structure test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_plugin_structure -v
```

Expected: PASS after Tasks 1-5 created runner files.

## Task 9: Full Verification And Docs

**Files:**

- Modify: `AGENTS.md`
- Modify: `docs/superpowers/plans/2026-05-15-product-agent-os-codex-runtime-runner.md`

- [ ] **Step 1: Run focused runner test pack**

Run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_codex_runtime_runner_guards tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_codex_runtime_runner_fixture_eval -v
```

Expected: all Track 5 focused tests PASS.

- [ ] **Step 2: Run full unit tests**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: all tests PASS.

- [ ] **Step 3: Run fixture eval**

Run:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: exit `0`; every result includes `codex_runtime_runner_status` and `codex_runtime_runner_checks`; runner fixtures report expected route/blocked/approval statuses.

- [ ] **Step 4: Run documentation structure check**

Run:

```powershell
python tools\check_docs.py
```

Expected: `OK: documentation structure checks passed`.

- [ ] **Step 5: Run strict MkDocs build**

Run:

```powershell
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; python -m mkdocs build --strict
```

Expected: exit `0`. The known upstream Material for MkDocs warning is acceptable only if the command exits `0`.

- [ ] **Step 6: Search for removed standalone/live runner path**

Run:

```powershell
rg -n "Agents SDK runner implementation|run_agents_sdk_runner|agents_sdk_runner_status|--live" plugins\product-agent-os tests\product_agent_os
```

Expected: no Track 5 implementation or test references to removed standalone/live runner path.

- [ ] **Step 7: Update project implementation status after verification**

Only after Steps 1-6 pass, update `AGENTS.md` under `Product-Agent OS implementation status`:

```markdown
- Track 5 Codex runtime runner is implemented with dependency-free contract mode, lifecycle routing, handoff/source/approval/automation/redaction guards, CLI wrappers, inactive-by-default plugin boundary, and fixture eval coverage.
```

Add baseline evidence line with the observed command results from the current run.

- [ ] **Step 8: Commit or report non-git workspace**

If `.git` exists in the execution environment:

```powershell
git add AGENTS.md mkdocs.yml docs/superpowers/plans/2026-05-15-product-agent-os-codex-runtime-runner.md plugins/product-agent-os tests/product_agent_os
git commit -m "feat: add codex runtime runner"
```

If `.git` does not exist, report that no commit was created because the workspace is not a git repository.

## Rollback

If implementation creates regressions that cannot be resolved in the current execution:

- remove `plugins/product-agent-os/scripts/codex_runtime_runner/`;
- remove `plugins/product-agent-os/scripts/run_codex_runtime_runner.py`;
- remove `plugins/product-agent-os/scripts/validate_codex_runtime_runner.py`;
- remove new `tests/product_agent_os/test_codex_runtime_runner_*.py`;
- remove new `plugins/product-agent-os/assets/fixtures/codex-runner-*` fixture folders;
- revert `run_fixture_eval.py`, `test_fixture_eval_runner.py`, `test_fixtures.py`, and `test_plugin_structure.py` to pre-Track-5 behavior without touching unrelated user changes;
- keep this plan and the Track 5 spec as design artifacts unless the user asks to remove them.

## Self-Review

Spec coverage:

- Contract schemas are covered by Task 1.
- Context loader and lifecycle state detection are covered by Task 2.
- Skill/subagent route planner is covered by Task 3.
- Approval, route, handoff, automation, and redaction validators are covered by Task 4.
- Contract-mode CLI and validator wrappers are covered by Task 5.
- Synthetic fixtures are covered by Task 6.
- Fixture eval extension is covered by Task 7.
- Inactive plugin boundary is covered by Task 8.
- Full verification and status update are covered by Task 9.

Source and safety coverage:

- The plan keeps Track 5 Codex-only and excludes standalone API-backed execution.
- No task installs dependencies, uses network access, starts an external service, creates active automation, or changes global Codex config.
- Redaction tests use synthetic values only and fixture content is synthetic.
- Workspace writes from runner default mode are out of scope; only `--output` writes a result JSON to an explicit file path during CLI tests.

Placeholder scan:

- No step uses unresolved placeholder terms.
- Each code-changing task includes explicit files, test command, implementation command, and expected result.
- All function names used in tests are introduced in implementation tasks.

Execution handoff:

Plan complete and saved to `docs/superpowers/plans/2026-05-15-product-agent-os-codex-runtime-runner.md`.

Two execution options:

1. **Subagent-Driven (recommended only if explicitly requested)** - dispatch separate workers by ownership area, then review and integrate.
2. **Inline Execution** - execute tasks in this session using `superpowers:executing-plans` with checkpoints after focused test packs.
