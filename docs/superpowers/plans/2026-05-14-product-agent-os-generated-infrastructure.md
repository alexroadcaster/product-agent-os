# Product-Agent OS Generated Infrastructure Implementation Plan

Source status: `official + experiment`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** реализовать Track 3: staged-first генератор проектной инфраструктуры для `product-agent-os`, который создаёт reviewable artifacts без скрытых записей в пользовательский проект.

**Architecture:** генератор состоит из template registry, deterministic renderer, CLI wrapper и расширенного fixture eval. Renderer читает workspace audit из Track 1, выбирает profile, строит JSON infrastructure plan, валидирует generated artifacts и пишет файлы только в staging directory.

**Tech Stack:** Python 3 standard library, `unittest`, `pathlib`, `json`, `tomllib`, Codex plugin assets, Markdown templates, TOML agent configs, hook scripts, fixture projects, MkDocs.

---

## Scope

Этот план реализует только Track 3 из [generated infrastructure design](../specs/2026-05-14-product-agent-os-generated-infrastructure-design.md).

Входит в scope:

- template registry и template safety tests;
- control-plane templates: `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- project-scoped `.codex/config.toml` proposal;
- `.codex/agents/*.toml` templates для восьми ролей;
- packaged hook scripts и staged `.codex/hooks/hooks.json`;
- workflow packets, eval JSON, automation candidate packet, PR/release packets;
- staged renderer с dry-run и stage modes;
- CLI wrapper `render_infrastructure.py`;
- fixture eval расширение для renderer scenarios;
- MkDocs navigation для этого плана.

Не входит в scope:

- direct writes в пользовательский проект;
- active automations, schedules, GitHub Actions, recurring Codex App automations;
- global `~/.codex/config.toml`;
- Agents SDK runner, MCP runtime orchestration, external integrations;
- dependency installation, network calls, external writes;
- claims that generated tests or hooks pass без текущей verification evidence.

## Execution Model

Рекомендуемый способ исполнения: `Subagent-Driven`.

Разделение ownership:

- Worker A: tests and fixtures. Owns `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_infrastructure_renderer.py`, `tests/product_agent_os/test_render_infrastructure_cli.py`, fixture folders, and fixture eval tests.
- Worker B: template registry and templates. Owns `plugins/product-agent-os/scripts/product_agent_os/templates.py` and `plugins/product-agent-os/assets/templates/**`.
- Worker C: renderer and CLI. Owns `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`, `plugins/product-agent-os/scripts/render_infrastructure.py`, and `plugins/product-agent-os/scripts/run_fixture_eval.py`.
- Worker D: docs and verification. Owns this plan navigation, docs checks, full test run, strict build, and final evidence.

Workers are not alone in the codebase. They must not revert edits made by others and must adapt to already merged Track 1 and Track 2 files.

## File Structure

Create these implementation files:

- `plugins/product-agent-os/scripts/product_agent_os/templates.py` - registry of template specs, target paths, validation kinds, and deterministic render substitutions.
- `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py` - dry-run and stage renderer, action planner, safety checks, validation, and JSON result model.
- `plugins/product-agent-os/scripts/render_infrastructure.py` - CLI wrapper.

Create these template files:

- `plugins/product-agent-os/assets/templates/control-plane/AGENTS.md`
- `plugins/product-agent-os/assets/templates/control-plane/REQUIREMENTS.md`
- `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`
- `plugins/product-agent-os/assets/templates/control-plane/TEST.md`
- `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`
- `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`
- `plugins/product-agent-os/assets/templates/config/config.toml`
- `plugins/product-agent-os/assets/templates/agents/product-manager.toml`
- `plugins/product-agent-os/assets/templates/agents/architect.toml`
- `plugins/product-agent-os/assets/templates/agents/explorer.toml`
- `plugins/product-agent-os/assets/templates/agents/builder.toml`
- `plugins/product-agent-os/assets/templates/agents/tester.toml`
- `plugins/product-agent-os/assets/templates/agents/reviewer.toml`
- `plugins/product-agent-os/assets/templates/agents/docs-maintainer.toml`
- `plugins/product-agent-os/assets/templates/agents/release-operator.toml`
- `plugins/product-agent-os/assets/templates/hooks/hooks.json`
- `plugins/product-agent-os/assets/templates/hooks/session_start_context.py`
- `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`
- `plugins/product-agent-os/assets/templates/hooks/permission_request_summary.py`
- `plugins/product-agent-os/assets/templates/hooks/post_tool_use_evidence.py`
- `plugins/product-agent-os/assets/templates/hooks/stop_runlog_reminder.py`
- `plugins/product-agent-os/assets/templates/workflows/source-context-pack.md`
- `plugins/product-agent-os/assets/templates/workflows/worktree-ownership.md`
- `plugins/product-agent-os/assets/templates/workflows/build-slice.md`
- `plugins/product-agent-os/assets/templates/workflows/review-slice.md`
- `plugins/product-agent-os/assets/templates/workflows/release-packet.md`
- `plugins/product-agent-os/assets/templates/workflows/runlog-compaction.md`
- `plugins/product-agent-os/assets/templates/runlogs/archive/README.md`
- `plugins/product-agent-os/assets/templates/evals/project-readiness.json`
- `plugins/product-agent-os/assets/templates/evals/handoff-completeness.json`
- `plugins/product-agent-os/assets/templates/evals/renderer-fixtures.json`
- `plugins/product-agent-os/assets/templates/automations/automation-candidate.md`
- `plugins/product-agent-os/assets/templates/pr/pr-body.md`
- `plugins/product-agent-os/assets/templates/pr/release-notes.md`

Create these tests:

- `tests/product_agent_os/test_infrastructure_templates.py`
- `tests/product_agent_os/test_infrastructure_renderer.py`
- `tests/product_agent_os/test_render_infrastructure_cli.py`

Modify these files:

- `tests/product_agent_os/test_fixtures.py` - add Track 3 fixture coverage.
- `tests/product_agent_os/test_fixture_eval_runner.py` - expect renderer evidence in fixture eval output.
- `plugins/product-agent-os/scripts/run_fixture_eval.py` - include renderer dry-run checks in fixture evaluation.
- `mkdocs.yml` - add this plan to implementation plans navigation.

Create these fixture folders:

- `plugins/product-agent-os/assets/fixtures/duplicate-managed-section/`
- `plugins/product-agent-os/assets/fixtures/docs-source-conflict/`
- `plugins/product-agent-os/assets/fixtures/failed-verification/`
- `plugins/product-agent-os/assets/fixtures/unsafe-write-request/`

## Contract Decisions

Renderer actions:

- `create`: target file does not exist; generated file can be staged as a create proposal.
- `update`: target file has exactly one managed section for the same section id; generated file stages a managed-section replacement.
- `leave_unchanged`: target file exists and has no managed marker; generated file stages a companion proposal and preserves user content.
- `blocked`: target file has duplicate or broken managed markers, unsafe path request, invalid workspace, or validation failure.

Staging rules:

- Default mode is dry-run and writes no files.
- Stage mode writes only inside the requested output directory.
- Staged file paths mirror target paths under the staging root.
- Companion proposals for user-authored files live under `_proposals/` inside the staging root.
- The renderer never writes into plugin root `hooks/hooks.json`.

Managed section markers:

```markdown
<!-- product-agent-os:start <section-id> -->
Generated body
<!-- product-agent-os:end <section-id> -->
```

Template substitution keys:

- `project_name`
- `workspace_path`
- `profile_name`
- `detected_stack`
- `detected_stack_text`
- `existing_control_plane`
- `missing_control_plane`
- `existing_codex_assets`
- `risk_text`
- `generated_at`

The renderer must replace every substitution before staged output is accepted.

## Task 1: Infrastructure Template Tests

**Files:**
- Create: `tests/product_agent_os/test_infrastructure_templates.py`

- [ ] **Step 1: Write failing template registry and safety tests**

Create `tests/product_agent_os/test_infrastructure_templates.py`:

```python
import json
import re
import sys
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
TEMPLATE_ROOT = ROOT / "plugins" / "product-agent-os" / "assets" / "templates"
PLUGIN_ROOT = ROOT / "plugins" / "product-agent-os"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.templates import required_templates, render_template  # noqa: E402
from product_agent_os.validators import validate_agent_file, validate_hook_file  # noqa: E402


REQUIRED_TARGETS = {
    "AGENTS.md",
    "REQUIREMENTS.md",
    "PLAN.md",
    "TEST.md",
    "EVALS.md",
    "RUNLOG.md",
    ".codex/config.toml",
    ".codex/agents/product-manager.toml",
    ".codex/agents/architect.toml",
    ".codex/agents/explorer.toml",
    ".codex/agents/builder.toml",
    ".codex/agents/tester.toml",
    ".codex/agents/reviewer.toml",
    ".codex/agents/docs-maintainer.toml",
    ".codex/agents/release-operator.toml",
    ".codex/hooks/hooks.json",
    ".codex/hooks/session_start_context.py",
    ".codex/hooks/pre_tool_use_policy.py",
    ".codex/hooks/permission_request_summary.py",
    ".codex/hooks/post_tool_use_evidence.py",
    ".codex/hooks/stop_runlog_reminder.py",
    ".codex/workflows/source-context-pack.md",
    ".codex/workflows/worktree-ownership.md",
    ".codex/workflows/build-slice.md",
    ".codex/workflows/review-slice.md",
    ".codex/workflows/release-packet.md",
    ".codex/workflows/runlog-compaction.md",
    ".codex/evals/project-readiness.json",
    ".codex/evals/handoff-completeness.json",
    ".codex/evals/renderer-fixtures.json",
    ".codex/automation-candidates/automation-candidate.md",
    ".codex/pr/pr-body.md",
    ".codex/pr/release-notes.md",
}

FORBIDDEN_TEXT = [
    "sk-",
    "BEGIN PRIVATE KEY",
    "PASSWORD=",
    "API_KEY=",
    "TOKEN=",
    "recurring schedule is active",
    "checks passed",
    "tests pass",
    "global ~/.codex/config.toml",
]


class InfrastructureTemplateTest(unittest.TestCase):
    def test_required_template_targets_are_registered_once(self):
        templates = required_templates()
        targets = [item.target_path for item in templates]

        self.assertEqual(set(targets), REQUIRED_TARGETS)
        self.assertEqual(len(targets), len(set(targets)))

    def test_template_source_files_exist(self):
        for item in required_templates():
            with self.subTest(key=item.key):
                self.assertTrue(item.source_path.exists(), item.source_path)
                self.assertTrue(item.source_path.is_file(), item.source_path)
                self.assertTrue(item.source_path.resolve().is_relative_to(TEMPLATE_ROOT.resolve()))

    def test_template_text_has_no_unsafe_literals(self):
        for item in required_templates():
            text = item.source_path.read_text(encoding="utf-8")
            with self.subTest(key=item.key):
                for forbidden in FORBIDDEN_TEXT:
                    self.assertNotIn(forbidden, text)
                self.assertNotRegex(text, re.compile(r"(?i)secret-value|private-customer|raw chat log"))

    def test_rendered_templates_have_no_unresolved_substitutions(self):
        context = {
            "project_name": "Synthetic Project",
            "workspace_path": "C:/workspace/synthetic-project",
            "profile_name": "standard-product",
            "detected_stack": ["python", "docs"],
            "detected_stack_text": "python, docs",
            "existing_control_plane": ["AGENTS.md"],
            "missing_control_plane": ["PLAN.md"],
            "existing_codex_assets": [".codex/config.toml"],
            "risk_text": "no detected test files or test configuration",
            "generated_at": "2026-05-14",
        }

        for item in required_templates():
            rendered = render_template(item, context)
            with self.subTest(key=item.key):
                self.assertNotRegex(rendered, re.compile(r"\{[a-zA-Z0-9_]+\}"))
                self.assertNotIn("None", rendered)

    def test_agent_templates_validate_after_render(self):
        context = self._context()
        for item in required_templates():
            if item.validation_kind != "agent":
                continue
            with self.subTest(key=item.key):
                path = self._render_temp_file(item, context)
                self.assertEqual(validate_agent_file(path), [])

    def test_hook_templates_validate_after_render(self):
        context = self._context()
        for item in required_templates():
            if item.validation_kind != "hook":
                continue
            with self.subTest(key=item.key):
                path = self._render_temp_file(item, context)
                self.assertEqual(validate_hook_file(path), [])

    def test_hook_lifecycle_config_is_template_only(self):
        self.assertFalse((PLUGIN_ROOT / "hooks" / "hooks.json").exists())
        hooks_template = TEMPLATE_ROOT / "hooks" / "hooks.json"
        data = json.loads(hooks_template.read_text(encoding="utf-8"))

        self.assertIn("SessionStart", data)
        self.assertIn("PreToolUse", data)
        self.assertIn("PermissionRequest", data)
        self.assertIn("PostToolUse", data)
        self.assertIn("Stop", data)

    def test_eval_templates_are_valid_json(self):
        for item in required_templates():
            if item.validation_kind != "eval_json":
                continue
            with self.subTest(key=item.key):
                data = json.loads(item.source_path.read_text(encoding="utf-8"))
                self.assertIn("name", data)
                self.assertIn("cases", data)
                self.assertIsInstance(data["cases"], list)

    def test_config_template_is_valid_toml(self):
        config = TEMPLATE_ROOT / "config" / "config.toml"
        data = tomllib.loads(config.read_text(encoding="utf-8"))

        self.assertIn("agents", data)
        self.assertNotIn("network_access", data)
        self.assertNotIn("secrets", data)

    def test_automation_template_is_candidate_only(self):
        text = (TEMPLATE_ROOT / "automations" / "automation-candidate.md").read_text(encoding="utf-8")

        self.assertIn("candidate_only", text)
        self.assertIn("manual stability evidence", text)
        self.assertIn("explicit approval", text)
        self.assertNotIn("RRULE", text)
        self.assertNotIn("schedule:", text)

    def test_workflow_inventory_covers_context_and_ownership(self):
        names = {item.source_path.name for item in required_templates() if item.category == "workflows"}

        self.assertEqual(
            names,
            {
                "source-context-pack.md",
                "worktree-ownership.md",
                "build-slice.md",
                "review-slice.md",
                "release-packet.md",
                "runlog-compaction.md",
            },
        )

    def _context(self):
        return {
            "project_name": "Synthetic Project",
            "workspace_path": "C:/workspace/synthetic-project",
            "profile_name": "standard-product",
            "detected_stack": ["python"],
            "detected_stack_text": "python",
            "existing_control_plane": [],
            "missing_control_plane": ["AGENTS.md"],
            "existing_codex_assets": [],
            "risk_text": "no detected test files or test configuration",
            "generated_at": "2026-05-14",
        }

    def _render_temp_file(self, item, context):
        import tempfile

        root = Path(tempfile.mkdtemp())
        path = root / item.target_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_template(item, context), encoding="utf-8")
        return path


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the template test to verify it fails**

Run:

```powershell
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
```

Expected: FAIL because `product_agent_os.templates` and template files do not exist yet.

## Task 2: Infrastructure Renderer Tests

**Files:**
- Create: `tests/product_agent_os/test_infrastructure_renderer.py`

- [ ] **Step 1: Write failing renderer behavior tests**

Create `tests/product_agent_os/test_infrastructure_renderer.py`:

```python
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.infrastructure import (  # noqa: E402
    InfrastructureError,
    render_infrastructure_plan,
    stage_infrastructure,
)


class InfrastructureRendererTest(unittest.TestCase):
    def test_dry_run_returns_json_shape_without_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            shutil.copytree(FIXTURES / "node-app", workspace)
            before = self._relative_files(workspace)

            result = render_infrastructure_plan(workspace)
            after = self._relative_files(workspace)

        self.assertEqual(before, after)
        self.assertEqual(result["infrastructure_plan"]["status"], "ready")
        self.assertEqual(result["infrastructure_plan"]["profile"], "guided-small")
        self.assertIn("rendered_artifacts", result)
        self.assertTrue(result["rendered_artifacts"]["validation"]["ok"])

    def test_greenfield_plan_creates_control_plane_and_codex_assets(self):
        result = render_infrastructure_plan(FIXTURES / "empty-repo")
        files = result["rendered_artifacts"]["files"]
        by_target = {item["target_path"]: item for item in files}

        self.assertEqual(by_target["AGENTS.md"]["action"], "create")
        self.assertEqual(by_target["REQUIREMENTS.md"]["action"], "create")
        self.assertEqual(by_target[".codex/config.toml"]["action"], "create")
        self.assertEqual(by_target[".codex/hooks/hooks.json"]["write_policy"], "staged_only")
        self.assertIn("explicit approval", " ".join(result["infrastructure_plan"]["approval_required"]))

    def test_stage_mode_writes_only_inside_output_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "python-app", workspace)

            result = stage_infrastructure(workspace, stage_root)

            staged_paths = [Path(item["staged_path"]).resolve() for item in result["rendered_artifacts"]["files"]]
            self.assertTrue(staged_paths)
            for path in staged_paths:
                self.assertTrue(path.is_relative_to(stage_root.resolve()), path)
                self.assertTrue(path.exists(), path)
            self.assertFalse((workspace / "AGENTS.md").exists())
            self.assertFalse((workspace / ".codex").exists())

    def test_existing_agents_file_without_marker_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "existing-codex-config", workspace)

            result = stage_infrastructure(workspace, stage_root)

            by_target = {item["target_path"]: item for item in result["rendered_artifacts"]["files"]}
            agents = by_target["AGENTS.md"]
            self.assertEqual(agents["action"], "leave_unchanged")
            self.assertIn("_proposals", agents["staged_path"])
            self.assertIn("preserved user-authored file", " ".join(result["infrastructure_plan"]["warnings"]))
            self.assertEqual((workspace / "AGENTS.md").read_text(encoding="utf-8"), "Existing project instructions.\n")

    def test_existing_project_config_without_marker_is_preserved(self):
        result = render_infrastructure_plan(FIXTURES / "existing-codex-config")
        by_target = {item["target_path"]: item for item in result["rendered_artifacts"]["files"]}

        self.assertEqual(by_target[".codex/config.toml"]["action"], "leave_unchanged")
        self.assertEqual(by_target[".codex/config.toml"]["write_policy"], "approved_write_required")
        self.assertIn(".codex/config.toml", " ".join(result["infrastructure_plan"]["warnings"]))

    def test_duplicate_managed_section_blocks_target(self):
        result = render_infrastructure_plan(FIXTURES / "duplicate-managed-section")
        by_target = {item["target_path"]: item for item in result["rendered_artifacts"]["files"]}

        self.assertEqual(result["infrastructure_plan"]["status"], "blocked")
        self.assertEqual(by_target["AGENTS.md"]["action"], "blocked")
        self.assertIn("duplicate managed section", " ".join(result["infrastructure_plan"]["blocked"]))

    def test_invalid_workspace_error_has_no_traceback_contract(self):
        with self.assertRaises(InfrastructureError) as error:
            render_infrastructure_plan(FIXTURES / "missing-workspace")

        self.assertIn("workspace does not exist", str(error.exception))

    def test_renderer_blocks_stage_directory_inside_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            shutil.copytree(FIXTURES / "node-app", workspace)

            with self.assertRaises(InfrastructureError) as error:
                stage_infrastructure(workspace, workspace / ".product-agent-os" / "staged")

        self.assertIn("outside workspace", str(error.exception))

    def test_rendered_control_plane_files_include_managed_markers(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)

            result = stage_infrastructure(workspace, stage_root)

            for item in result["rendered_artifacts"]["files"]:
                if item["target_path"] not in {"AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"}:
                    continue
                text = Path(item["staged_path"]).read_text(encoding="utf-8")
                self.assertIn("<!-- product-agent-os:start", text)
                self.assertIn("<!-- product-agent-os:end", text)

    def _relative_files(self, root):
        return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run renderer tests to verify they fail**

Run:

```powershell
python -m unittest tests.product_agent_os.test_infrastructure_renderer -v
```

Expected: FAIL because `product_agent_os.infrastructure` and new fixtures do not exist yet.

## Task 3: CLI And Fixture Eval Tests

**Files:**
- Create: `tests/product_agent_os/test_render_infrastructure_cli.py`
- Modify: `tests/product_agent_os/test_fixture_eval_runner.py`

- [ ] **Step 1: Write failing CLI wrapper tests**

Create `tests/product_agent_os/test_render_infrastructure_cli.py`:

```python
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins" / "product-agent-os" / "scripts" / "render_infrastructure.py"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"


class RenderInfrastructureCliTest(unittest.TestCase):
    def test_dry_run_cli_prints_plan_json(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURES / "node-app"), "--dry-run"],
            check=False,
            capture_output=True,
            text=True,
        )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertEqual(payload["infrastructure_plan"]["status"], "ready")
        self.assertIn("rendered_artifacts", payload)

    def test_stage_cli_writes_output_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "stage"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(FIXTURES / "python-app"), "--stage", str(out)],
                check=False,
                capture_output=True,
                text=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stderr, "")
            self.assertTrue((out / "AGENTS.md").exists())
            self.assertTrue(payload["rendered_artifacts"]["validation"]["ok"])

    def test_invalid_workspace_cli_returns_clear_error(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURES / "missing-workspace"), "--dry-run"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("workspace does not exist", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_cli_rejects_missing_mode(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURES / "node-app")],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("choose --dry-run or --stage", result.stderr)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Update fixture eval runner tests for renderer evidence**

Modify `tests/product_agent_os/test_fixture_eval_runner.py` so successful fixture results use this key order:

```python
["fixture", "ok", "profile", "risks", "renderer_status", "renderer_file_count"]
```

Update every hard-coded failed result with:

```python
"renderer_status": "",
"renderer_file_count": 0,
```

- [ ] **Step 3: Run CLI and fixture eval tests to verify they fail**

Run:

```powershell
python -m unittest tests.product_agent_os.test_render_infrastructure_cli tests.product_agent_os.test_fixture_eval_runner -v
```

Expected: FAIL because the CLI and fixture eval implementation do not exist yet.

## Task 4: Track 3 Fixture Projects

**Files:**
- Modify: `tests/product_agent_os/test_fixtures.py`
- Create: `plugins/product-agent-os/assets/fixtures/duplicate-managed-section/AGENTS.md`
- Create: `plugins/product-agent-os/assets/fixtures/docs-source-conflict/mkdocs.yml`
- Create: `plugins/product-agent-os/assets/fixtures/docs-source-conflict/docs/index.md`
- Create: `plugins/product-agent-os/assets/fixtures/docs-source-conflict/docs/sources/registry.md`
- Create: `plugins/product-agent-os/assets/fixtures/failed-verification/RUNLOG.md`
- Create: `plugins/product-agent-os/assets/fixtures/unsafe-write-request/.codex/config.toml`
- Create: `plugins/product-agent-os/assets/fixtures/unsafe-write-request/AGENTS.md`

- [ ] **Step 1: Add fixture tests**

Extend `test_required_fixture_projects_exist` in `tests/product_agent_os/test_fixtures.py` with:

```python
"duplicate-managed-section",
"docs-source-conflict",
"failed-verification",
"unsafe-write-request",
```

Add these tests:

```python
def test_duplicate_managed_section_fixture_has_two_markers(self):
    text = (FIXTURES / "duplicate-managed-section" / "AGENTS.md").read_text(encoding="utf-8")
    self.assertEqual(text.count("<!-- product-agent-os:start project-rules -->"), 2)

def test_docs_source_conflict_fixture_has_source_registry(self):
    self.assertTrue((FIXTURES / "docs-source-conflict" / "docs" / "sources" / "registry.md").exists())
    self.assertIn("docs_dir: docs", (FIXTURES / "docs-source-conflict" / "mkdocs.yml").read_text(encoding="utf-8"))

def test_failed_verification_fixture_records_failure_without_success_claim(self):
    text = (FIXTURES / "failed-verification" / "RUNLOG.md").read_text(encoding="utf-8")
    self.assertIn("exit_code: 1", text)
    self.assertIn("verification failed", text)

def test_unsafe_write_request_fixture_has_existing_codex_config(self):
    self.assertTrue((FIXTURES / "unsafe-write-request" / ".codex" / "config.toml").exists())
    text = (FIXTURES / "unsafe-write-request" / "AGENTS.md").read_text(encoding="utf-8")
    self.assertIn("Do not write outside this workspace", text)
```

- [ ] **Step 2: Add fixture files**

Create `duplicate-managed-section/AGENTS.md`:

```markdown
# Existing Rules

<!-- product-agent-os:start project-rules -->
First generated block.
<!-- product-agent-os:end project-rules -->

User-authored content between blocks.

<!-- product-agent-os:start project-rules -->
Second generated block.
<!-- product-agent-os:end project-rules -->
```

Create `docs-source-conflict/mkdocs.yml`:

```yaml
site_name: Source Conflict Fixture
docs_dir: docs
```

Create `docs-source-conflict/docs/index.md`:

```markdown
# Source Conflict Fixture

This fixture simulates a docs project with its own source registry.
```

Create `docs-source-conflict/docs/sources/registry.md`:

```markdown
# Local Source Registry

This registry is user-authored and must be preserved by generated infrastructure.
```

Create `failed-verification/RUNLOG.md`:

```markdown
# RUNLOG

## Verification Evidence

- command: `python -m unittest`
- exit_code: 1
- result: verification failed
```

Create `unsafe-write-request/AGENTS.md`:

```markdown
# Project Instructions

Do not write outside this workspace.
```

Create `unsafe-write-request/.codex/config.toml`:

```toml
[sandbox]
mode = "workspace-write"

[approvals]
policy = "on-request"
```

- [ ] **Step 3: Run fixture tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_fixtures -v
```

Expected: PASS after fixture files are added.

## Task 5: Template Registry Module

**Files:**
- Create: `plugins/product-agent-os/scripts/product_agent_os/templates.py`

- [ ] **Step 1: Implement template registry**

Create `plugins/product-agent-os/scripts/product_agent_os/templates.py` with:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from string import Formatter
from typing import Any


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = PLUGIN_ROOT / "assets" / "templates"


@dataclass(frozen=True)
class TemplateSpec:
    key: str
    category: str
    source_path: Path
    target_path: str
    validation_kind: str = "text"
    managed_section: str = ""


def _template(category: str, name: str, target: str, validation_kind: str = "text", managed_section: str = "") -> TemplateSpec:
    key = f"{category}/{name}"
    return TemplateSpec(
        key=key,
        category=category,
        source_path=TEMPLATE_ROOT / category / name,
        target_path=target,
        validation_kind=validation_kind,
        managed_section=managed_section,
    )


TEMPLATES = [
    _template("control-plane", "AGENTS.md", "AGENTS.md", managed_section="project-rules"),
    _template("control-plane", "REQUIREMENTS.md", "REQUIREMENTS.md", managed_section="requirements"),
    _template("control-plane", "PLAN.md", "PLAN.md", managed_section="plan"),
    _template("control-plane", "TEST.md", "TEST.md", managed_section="test-plan"),
    _template("control-plane", "EVALS.md", "EVALS.md", managed_section="evals"),
    _template("control-plane", "RUNLOG.md", "RUNLOG.md", managed_section="runlog"),
    _template("config", "config.toml", ".codex/config.toml", validation_kind="toml"),
    _template("agents", "product-manager.toml", ".codex/agents/product-manager.toml", validation_kind="agent"),
    _template("agents", "architect.toml", ".codex/agents/architect.toml", validation_kind="agent"),
    _template("agents", "explorer.toml", ".codex/agents/explorer.toml", validation_kind="agent"),
    _template("agents", "builder.toml", ".codex/agents/builder.toml", validation_kind="agent"),
    _template("agents", "tester.toml", ".codex/agents/tester.toml", validation_kind="agent"),
    _template("agents", "reviewer.toml", ".codex/agents/reviewer.toml", validation_kind="agent"),
    _template("agents", "docs-maintainer.toml", ".codex/agents/docs-maintainer.toml", validation_kind="agent"),
    _template("agents", "release-operator.toml", ".codex/agents/release-operator.toml", validation_kind="agent"),
    _template("hooks", "hooks.json", ".codex/hooks/hooks.json", validation_kind="hook_json"),
    _template("hooks", "session_start_context.py", ".codex/hooks/session_start_context.py", validation_kind="hook"),
    _template("hooks", "pre_tool_use_policy.py", ".codex/hooks/pre_tool_use_policy.py", validation_kind="hook"),
    _template("hooks", "permission_request_summary.py", ".codex/hooks/permission_request_summary.py", validation_kind="hook"),
    _template("hooks", "post_tool_use_evidence.py", ".codex/hooks/post_tool_use_evidence.py", validation_kind="hook"),
    _template("hooks", "stop_runlog_reminder.py", ".codex/hooks/stop_runlog_reminder.py", validation_kind="hook"),
    _template("workflows", "source-context-pack.md", ".codex/workflows/source-context-pack.md"),
    _template("workflows", "worktree-ownership.md", ".codex/workflows/worktree-ownership.md"),
    _template("workflows", "build-slice.md", ".codex/workflows/build-slice.md"),
    _template("workflows", "review-slice.md", ".codex/workflows/review-slice.md"),
    _template("workflows", "release-packet.md", ".codex/workflows/release-packet.md"),
    _template("workflows", "runlog-compaction.md", ".codex/workflows/runlog-compaction.md"),
    _template("evals", "project-readiness.json", ".codex/evals/project-readiness.json", validation_kind="eval_json"),
    _template("evals", "handoff-completeness.json", ".codex/evals/handoff-completeness.json", validation_kind="eval_json"),
    _template("evals", "renderer-fixtures.json", ".codex/evals/renderer-fixtures.json", validation_kind="eval_json"),
    _template("automations", "automation-candidate.md", ".codex/automation-candidates/automation-candidate.md"),
    _template("pr", "pr-body.md", ".codex/pr/pr-body.md"),
    _template("pr", "release-notes.md", ".codex/pr/release-notes.md"),
]


class StrictFormatDict(dict[str, Any]):
    def __missing__(self, key: str) -> str:
        raise KeyError(f"missing template context key: {key}")


def required_templates() -> list[TemplateSpec]:
    return list(TEMPLATES)


def template_by_target(target_path: str) -> TemplateSpec:
    for item in TEMPLATES:
        if item.target_path == target_path:
            return item
    raise KeyError(f"unknown template target: {target_path}")


def template_fields(text: str) -> set[str]:
    return {field_name for _, field_name, _, _ in Formatter().parse(text) if field_name}


def render_template(item: TemplateSpec, context: dict[str, Any]) -> str:
    text = item.source_path.read_text(encoding="utf-8")
    fields = template_fields(text)
    missing = sorted(field for field in fields if field not in context)
    if missing:
        raise KeyError("missing template context keys: " + ", ".join(missing))
    return text.format_map(StrictFormatDict(context))
```

- [ ] **Step 2: Run template tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
```

Expected: FAIL because template files are not present yet.

## Task 6: Control-Plane And Workflow Templates

**Files:**
- Create: all files under `plugins/product-agent-os/assets/templates/control-plane/`
- Create: all files under `plugins/product-agent-os/assets/templates/workflows/`

- [ ] **Step 1: Add control-plane template bodies**

Each control-plane template must start with a title, include the managed section markers, and use only deterministic substitution keys from the contract.

Use these section ids:

- `AGENTS.md`: `project-rules`
- `REQUIREMENTS.md`: `requirements`
- `PLAN.md`: `plan`
- `TEST.md`: `test-plan`
- `EVALS.md`: `evals`
- `RUNLOG.md`: `runlog`

Create `plugins/product-agent-os/assets/templates/control-plane/AGENTS.md`:

```markdown
# AGENTS.md

<!-- product-agent-os:start project-rules -->
Project: {project_name}
Profile: {profile_name}
Detected stack: {detected_stack_text}

## Durable Rules

- Treat official project docs and checked-in files as source of truth.
- Preserve user-authored content outside managed sections.
- Do not store secrets, credentials, private keys, customer data, or raw private chat logs.
- Do not write outside the current workspace.
- Use staged drafts before direct project writes.
- Record commands and observed results in `RUNLOG.md` before claiming readiness.

## Verification Policy

- Run deterministic tests, builds, linters, docs checks, or evals that match the current slice.
- If verification cannot run, record the gap and stop before readiness claims.
- External systems, network access, permission changes, and publishing require explicit approval.

## Agent Handoff

Every handoff must include sources, assumptions, files touched or proposed, commands run, evidence, risks, stop reason, and recommended next role.
<!-- product-agent-os:end project-rules -->
```

Create the other control-plane templates with the same marker pattern and these required headings:

- `REQUIREMENTS.md`: `Goal`, `Users`, `Scope`, `Non-Goals`, `Constraints`, `Acceptance Criteria`, `Assumptions`, `Open Questions`.
- `PLAN.md`: `Lifecycle State`, `Implementation Slices`, `Ownership`, `Dependencies`, `Risks`, `Rollback`, `Verification Gates`, `Approval Needs`.
- `TEST.md`: `Deterministic Checks`, `Manual Checks`, `Runtime Or Visual Checks`, `Known Gaps`, `Evidence Format`.
- `EVALS.md`: `Rubrics`, `Thresholds`, `Artifacts`, `Regression Notes`, `Unsupported Claims`.
- `RUNLOG.md`: `Current State`, `Decisions`, `Commands`, `Verification Evidence`, `Failures`, `Risks`, `Handoff Summary`.

For each file include these generated context lines inside the managed section:

```markdown
Project: {project_name}
Workspace: {workspace_path}
Profile: {profile_name}
Detected stack: {detected_stack_text}
Generated at: {generated_at}
```

- [ ] **Step 2: Add workflow packet templates**

Create workflow templates under `plugins/product-agent-os/assets/templates/workflows/`.

Each workflow file must include:

- `# <Workflow Name>`
- `Project: {project_name}`
- `Profile: {profile_name}`
- `## Inputs`
- `## Process`
- `## Outputs`
- `## Verification`
- `## Stop Conditions`

Add workflow-specific required content:

- `source-context-pack.md`: source status, freshness, Context7, official-source registry update notes, unsupported claims.
- `worktree-ownership.md`: workspace root, branch or worktree assumption, file ownership map, parallel write conflict rules.
- `build-slice.md`: one approved slice, inputs, owner, files, commands, evidence, rollback.
- `review-slice.md`: findings-first review format, missing tests, regressions, security risk, verdict.
- `release-packet.md`: PR summary, checks, user impact, rollback, residual risks, approval requirements.
- `runlog-compaction.md`: hot context, warm context, cold archive proposal, evidence preservation, privacy boundaries.

Example baseline for `build-slice.md`:

```markdown
# Build Slice Workflow

Project: {project_name}
Profile: {profile_name}

## Inputs

- Approved requirement or issue.
- Current `PLAN.md` slice.
- Ownership boundary.
- Verification command or documented gap.

## Process

1. Confirm scope and files.
2. Run or inspect the baseline before changing code when feasible.
3. Make one focused change.
4. Run relevant checks.
5. Record evidence and risks.

## Outputs

- Changed files summary.
- Commands run with observed results.
- Remaining risks.
- Next role recommendation.

## Verification

Do not mark the slice ready without current evidence.

## Stop Conditions

- Scope is unclear.
- Required approval is missing.
- Verification fails and no safe fix is available in the slice.
```

- [ ] **Step 3: Run template tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
```

Expected: FAIL because config, agents, hooks, evals, automation, and PR templates are not present yet.

## Task 7: Config, Agent, Hook, Eval, Automation, And PR Templates

**Files:**
- Create: all remaining files under `plugins/product-agent-os/assets/templates/`

- [ ] **Step 1: Add project config template**

Create `plugins/product-agent-os/assets/templates/config/config.toml`:

```toml
# Product-Agent OS project-scoped Codex proposal.
# Stage this file for review before enabling it in a project.

[agents]
default_profile = "{profile_name}"
max_parallel = 2

[agents.reasoning]
planning = "high"
building = "medium"
review = "high"
mechanical = "low"

[sandbox]
default_mode = "workspace-write"

[approvals]
external_writes = "explicit"
network_access = "explicit"
permission_changes = "explicit"
automation_activation = "explicit"

[product_agent_os]
control_plane = ["AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
workflow_dir = ".codex/workflows"
runlog_archive_dir = ".codex/runlogs/archive"
```

- [ ] **Step 2: Add agent templates**

Each agent TOML must include:

- `name`
- `description`
- `developer_instructions`
- `ownership`
- `inputs`
- `outputs`
- `stop_conditions`
- `model_policy`
- `handoff_requirements`

Create `plugins/product-agent-os/assets/templates/agents/explorer.toml` as the reference shape:

```toml
name = "explorer"
description = "Read-only codebase and source mapper for Product-Agent OS projects."
developer_instructions = """
Operate as a read-only explorer. Inspect files, docs, tests, and project conventions. Do not edit files. Return sources used, assumptions, relevant paths, verification commands discovered, risks, and recommended next role.
"""
ownership = "Read-only project discovery and source mapping."
inputs = ["workspace audit", "user goal", "current lifecycle packet"]
outputs = ["source map", "project conventions", "test command candidates", "risk notes"]
stop_conditions = ["requested edit", "missing workspace", "source conflict requiring approval"]
model_policy = "Use medium reasoning for bounded discovery and high reasoning for architecture or security-sensitive mapping."
handoff_requirements = ["sources", "assumptions", "files inspected", "commands discovered", "risks", "next role"]
```

Create the other seven agent templates with the same TOML shape and these ownership boundaries:

- `product-manager`: requirements, scope, non-goals, acceptance criteria.
- `architect`: decomposition, dependencies, ownership, rollback, risk routing.
- `builder`: one approved implementation slice and local verification.
- `tester`: deterministic checks, manual checks, eval gaps, evidence capture.
- `reviewer`: findings-first review, regressions, missing tests, security and approval risk.
- `docs-maintainer`: docs updates, source status, runlog updates, navigation impacts.
- `release-operator`: PR packet, release notes, rollout, rollback, residual risk.

- [ ] **Step 3: Add hook lifecycle config and hook scripts**

Create `plugins/product-agent-os/assets/templates/hooks/hooks.json`:

```json
{
  "SessionStart": [
    {
      "command": "python .codex/hooks/session_start_context.py"
    }
  ],
  "PreToolUse": [
    {
      "command": "python .codex/hooks/pre_tool_use_policy.py"
    }
  ],
  "PermissionRequest": [
    {
      "command": "python .codex/hooks/permission_request_summary.py"
    }
  ],
  "PostToolUse": [
    {
      "command": "python .codex/hooks/post_tool_use_evidence.py"
    }
  ],
  "Stop": [
    {
      "command": "python .codex/hooks/stop_runlog_reminder.py"
    }
  ]
}
```

Hook scripts must be deterministic Python, accept JSON on stdin when available, avoid network calls, avoid secret storage, and print concise JSON or text. Use this safety baseline in `pre_tool_use_policy.py`:

```python
from __future__ import annotations

import json
import re
import sys


DESTRUCTIVE_PATTERNS = [
    r"\brm\s+-rf\b",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+checkout\s+--\b",
    r"\bRemove-Item\b.*\b-Recurse\b",
]

FORBIDDEN_PATHS = [
    r"\.\.[/\\]",
    r"~[/\\]\.codex[/\\]config\.toml",
]


def main() -> int:
    payload = sys.stdin.read()
    command = payload
    try:
        data = json.loads(payload) if payload.strip() else {}
        command = str(data.get("command", payload))
    except json.JSONDecodeError:
        command = payload

    findings = []
    for pattern in DESTRUCTIVE_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            findings.append("destructive command requires explicit approval")
    for pattern in FORBIDDEN_PATHS:
        if re.search(pattern, command):
            findings.append("path outside approved project boundary requires explicit approval")

    print(json.dumps({"ok": not findings, "findings": findings}, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Other hook scripts:

- `session_start_context.py`: read safe project file presence only and summarize which control-plane files exist.
- `permission_request_summary.py`: summarize requested permission reason and remind that approval must be explicit.
- `post_tool_use_evidence.py`: format command, exit code, and short result for runlog buffer.
- `stop_runlog_reminder.py`: print a reminder when evidence exists and `RUNLOG.md` may need an update.

- [ ] **Step 4: Add eval JSON templates**

Create `project-readiness.json`, `handoff-completeness.json`, and `renderer-fixtures.json` with this shape:

```json
{
  "name": "project-readiness",
  "version": 1,
  "purpose": "Check Product-Agent OS generated infrastructure for safety, required artifacts, and verification gaps.",
  "cases": [
    {
      "id": "control-plane-present",
      "input": {
        "artifact_summary": ["AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
      },
      "expected": {
        "required_artifacts_named": true,
        "claims_checks_passed": false
      }
    }
  ]
}
```

Use distinct `name`, `purpose`, and `cases` for each eval:

- `handoff-completeness`: sources, assumptions, files, evidence, risks, stop reason.
- `renderer-fixtures`: greenfield, existing config, missing tests, unsafe write, monorepo ownership, docs source conflict, failed verification.

- [ ] **Step 5: Add automation and PR templates**

Create `plugins/product-agent-os/assets/templates/automations/automation-candidate.md` with these required lines:

```markdown
# Automation Candidate

Readiness: candidate_only
Project: {project_name}

## Required Evidence

- manual stability evidence
- stable inputs
- stable outputs
- owner
- cadence
- verification
- failure modes
- rollback or disable path
- explicit approval for writes

This packet does not create a schedule, recurring run, external workflow, or active automation.
```

Create PR templates:

- `pr-body.md`: summary, user impact, checks run, evidence, rollback, residual risks, approvals.
- `release-notes.md`: release scope, behavior change, verification, migration notes, rollback, known gaps.

- [ ] **Step 6: Run template tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
```

Expected: PASS.

## Task 8: Infrastructure Renderer Implementation

**Files:**
- Create: `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`

- [ ] **Step 1: Implement renderer module**

Create `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py` with these public functions:

```python
from __future__ import annotations

import json
import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from product_agent_os.discovery import analyze_workspace
from product_agent_os.merge_markdown import merge_section
from product_agent_os.templates import TemplateSpec, required_templates, render_template
from product_agent_os.validators import validate_agent_file, validate_hook_file


OWNER = "product-agent-os"


class InfrastructureError(RuntimeError):
    pass


@dataclass(frozen=True)
class PlannedFile:
    target_path: str
    staged_path: str
    action: str
    write_policy: str
    template_key: str


def render_infrastructure_plan(workspace: str | Path) -> dict[str, Any]:
    workspace_path = _workspace(workspace)
    audit = analyze_workspace(workspace_path)
    return _plan(workspace_path, audit, stage_root=None)


def stage_infrastructure(workspace: str | Path, output_dir: str | Path) -> dict[str, Any]:
    workspace_path = _workspace(workspace)
    stage_root = Path(output_dir).resolve()
    if _is_relative_to(stage_root, workspace_path):
        raise InfrastructureError("stage output directory must be outside workspace for Track 3 staged review")
    audit = analyze_workspace(workspace_path)
    result = _plan(workspace_path, audit, stage_root=stage_root)
    if result["infrastructure_plan"]["status"] == "blocked":
        return result
    _write_staged_files(result, stage_root)
    return result
```

Implement private helpers:

- `_workspace(workspace)`: resolve path, raise `InfrastructureError` for missing or non-directory workspace.
- `_context(workspace, audit)`: build deterministic template substitution context.
- `_plan(workspace, audit, stage_root)`: iterate `required_templates()`, compute action, staged path, warnings, blocked entries, approval requirements, and validation result.
- `_action_for_target(workspace, item)`: inspect existing target file and return `create`, `update`, `leave_unchanged`, or `blocked`.
- `_managed_count(text, section_id)`: count matching start and end markers.
- `_staged_path(stage_root, item, action)`: mirror target path or use `_proposals/<target>.product-agent-os-proposal`.
- `_render_body(item, context, existing_text, action)`: render template; for control-plane files use `merge_section` when action is `update`; for unmarked existing files stage the full generated proposal without touching original.
- `_validate_rendered_files(files)`: validate agent TOML, hook scripts, hook JSON, eval JSON, staged config TOML, and unresolved substitutions.
- `_write_staged_files(result, stage_root)`: create parent dirs and write internal file content only inside `stage_root`.

Public JSON must not include internal file contents. Keep `content` in an internal structure and strip it before printing.

Validation details:

```python
def _validate_content(item: TemplateSpec, path: Path, content: str) -> list[str]:
    errors: list[str] = []
    if "{" in content and "}" in content:
        errors.append("rendered output contains unresolved substitution marker")
    if item.validation_kind == "agent":
        errors.extend(validate_agent_file(path))
    elif item.validation_kind == "hook":
        errors.extend(validate_hook_file(path))
    elif item.validation_kind == "hook_json":
        data = json.loads(content)
        for event in ["SessionStart", "PreToolUse", "PermissionRequest", "PostToolUse", "Stop"]:
            if event not in data:
                errors.append(f"hook config missing event: {event}")
    elif item.validation_kind == "eval_json":
        data = json.loads(content)
        if not isinstance(data.get("cases"), list):
            errors.append("eval JSON must include cases list")
    elif item.validation_kind == "toml":
        tomllib.loads(content)
    return errors
```

Write validation temp files under the stage root when staging and under a temporary directory for dry-run. Do not write into the workspace.

- [ ] **Step 2: Run renderer tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_infrastructure_renderer -v
```

Expected: PASS.

- [ ] **Step 3: Run template and renderer tests together**

Run:

```powershell
python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_infrastructure_renderer -v
```

Expected: PASS.

## Task 9: CLI Wrapper

**Files:**
- Create: `plugins/product-agent-os/scripts/render_infrastructure.py`

- [ ] **Step 1: Implement CLI**

Create `plugins/product-agent-os/scripts/render_infrastructure.py`:

```python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.infrastructure import (  # noqa: E402
    InfrastructureError,
    render_infrastructure_plan,
    stage_infrastructure,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render Product-Agent OS project infrastructure.")
    parser.add_argument("workspace", help="Workspace directory to inspect.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Print infrastructure plan JSON without writing files.")
    mode.add_argument("--stage", metavar="OUTPUT_DIR", help="Write staged artifacts under OUTPUT_DIR.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.dry_run and not args.stage:
        print("error: choose --dry-run or --stage", file=sys.stderr)
        return 2

    try:
        if args.dry_run:
            result = render_infrastructure_plan(args.workspace)
        else:
            result = stage_infrastructure(args.workspace, args.stage)
    except InfrastructureError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["rendered_artifacts"]["validation"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run CLI tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_render_infrastructure_cli -v
```

Expected: PASS.

## Task 10: Fixture Eval Renderer Coverage

**Files:**
- Modify: `plugins/product-agent-os/scripts/run_fixture_eval.py`
- Modify: `tests/product_agent_os/test_fixture_eval_runner.py`

- [ ] **Step 1: Integrate renderer dry-run into fixture eval**

Modify `plugins/product-agent-os/scripts/run_fixture_eval.py`:

```python
from product_agent_os.infrastructure import InfrastructureError, render_infrastructure_plan  # noqa: E402
```

Inside `evaluate_fixture`, after discovery succeeds:

```python
try:
    rendered = render_infrastructure_plan(path)
    renderer_status = rendered["infrastructure_plan"]["status"]
    renderer_file_count = len(rendered["rendered_artifacts"]["files"])
    renderer_ok = rendered["rendered_artifacts"]["validation"]["ok"]
except InfrastructureError as exc:
    renderer_status = "error"
    renderer_file_count = 0
    renderer_ok = False
    risks = list(risks) if isinstance(risks, list) else ["invalid discovery risks"]
    risks.append(f"renderer failed: {exc}")
```

Return shape:

```python
return {
    "fixture": path.name,
    "ok": ok and renderer_ok and renderer_status in {"ready", "blocked"},
    "profile": profile_name,
    "risks": risks if isinstance(risks, list) else ["invalid discovery risks"],
    "renderer_status": renderer_status,
    "renderer_file_count": renderer_file_count,
}
```

For `_failed_result`, include:

```python
"renderer_status": "",
"renderer_file_count": 0,
```

Rationale: `duplicate-managed-section` is an expected blocked fixture, so fixture eval accepts `blocked` when validation remains structurally clean.

- [ ] **Step 2: Run fixture eval tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_fixture_eval_runner -v
```

Expected: PASS.

- [ ] **Step 3: Run fixture eval CLI**

Run:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: exit 0. JSON contains all fixture names and each item includes `renderer_status` and `renderer_file_count`.

## Task 11: Profile Routing And Safety Refinement

**Files:**
- Modify: `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`
- Modify: `tests/product_agent_os/test_infrastructure_renderer.py`

- [ ] **Step 1: Add profile artifact routing tests**

Add tests:

```python
def test_monorepo_includes_worktree_ownership_workflow(self):
    result = render_infrastructure_plan(FIXTURES / "monorepo")
    targets = {item["target_path"] for item in result["rendered_artifacts"]["files"]}

    self.assertEqual(result["infrastructure_plan"]["profile"], "production-team")
    self.assertIn(".codex/workflows/worktree-ownership.md", targets)

def test_docs_project_includes_source_context_workflow(self):
    result = render_infrastructure_plan(FIXTURES / "docs-source-conflict")
    targets = {item["target_path"] for item in result["rendered_artifacts"]["files"]}

    self.assertIn(".codex/workflows/source-context-pack.md", targets)
    self.assertIn("source registry", " ".join(result["infrastructure_plan"]["warnings"]).lower())

def test_failed_verification_fixture_keeps_evidence_gap_visible(self):
    result = render_infrastructure_plan(FIXTURES / "failed-verification")

    self.assertIn("failed verification evidence", " ".join(result["infrastructure_plan"]["warnings"]))
    self.assertNotIn("checks passed", json.dumps(result).lower())
```

- [ ] **Step 2: Implement warnings and artifact depth**

In `infrastructure.py`, keep all required templates registered for Track 3, but add profile warnings:

- monorepo or `production-team`: add warning to use `worktree-ownership.md`.
- docs stack or `docs/sources/registry.md`: add warning to preserve existing source registry and use `source-context-pack.md`.
- existing `RUNLOG.md` with `exit_code: 1` or `verification failed`: add warning that failed verification evidence must stay visible.
- `autonomous-maintenance`: automation candidate stays candidate-only and no active schedule appears.

Do not remove required templates by profile in this Track. The profile changes depth and warnings, while lifecycle order and safety remain stable.

- [ ] **Step 3: Run renderer tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_infrastructure_renderer -v
```

Expected: PASS.

## Task 12: Navigation And Full Verification

**Files:**
- Modify: `mkdocs.yml`

- [ ] **Step 1: Add plan to MkDocs navigation**

Add this entry under implementation plans:

```yaml
      - Product-Agent OS generated infrastructure: superpowers/plans/2026-05-14-product-agent-os-generated-infrastructure.md
```

- [ ] **Step 2: Run full unit test suite**

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

Expected: exit 0 with renderer-aware fixture results.

- [ ] **Step 4: Run documentation checks**

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

Expected: exit 0. The known upstream Material for MkDocs warning is acceptable only if the command exits 0.

- [ ] **Step 6: Record implementation evidence**

If the workspace is not a git repository, record in the final implementation response:

- changed files and directories;
- exact commands run;
- observed results;
- unresolved risks;
- next action.

If a git repository exists in a future execution environment, make a focused commit after tests pass:

```powershell
git add plugins/product-agent-os/assets/templates plugins/product-agent-os/scripts tests/product_agent_os docs/superpowers/plans/2026-05-14-product-agent-os-generated-infrastructure.md mkdocs.yml
git commit -m "feat: add product agent infrastructure renderer"
```

## Self-Review

Spec coverage:

- staged-first renderer is covered by Tasks 2, 8, and 9.
- template registry and completeness tests are covered by Tasks 1, 5, 6, and 7.
- control-plane, config, agents, hooks, workflows, evals, automation candidate, and PR templates are covered by Tasks 6 and 7.
- hook lifecycle config is staged as `.codex/hooks/hooks.json` and plugin-root hook activation is explicitly absent in Task 1.
- existing `.codex/config.toml`, existing unmarked `AGENTS.md`, and duplicate managed sections are covered by Task 2.
- context overflow and runlog compaction are covered by `runlog-compaction.md` and archive config in Tasks 6 and 7.
- source/context research and Context7 packet are covered by `source-context-pack.md`.
- worktree and parallel ownership are covered by `worktree-ownership.md`.
- expanded fixture eval coverage is covered by Tasks 3, 4, 10, and 11.
- automation remains candidate-only in Task 7.
- final verification is covered by Task 12.

Residual risks:

- Static template validation cannot prove that every generated workflow works well in every real user project.
- Track 3 still avoids direct merge into user files; a safe approved merge command belongs in Track 4.
- Hook scripts are packaged examples and need real-project approval before activation.
- Fixture eval checks renderer structure and safety, not application-specific product quality.

Execution handoff:

Plan complete and saved to `docs/superpowers/plans/2026-05-14-product-agent-os-generated-infrastructure.md`.

Two execution options:

1. **Subagent-Driven (recommended)** - dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** - execute tasks in this session using executing-plans with checkpoints.
