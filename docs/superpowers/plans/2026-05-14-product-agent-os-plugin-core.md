---
title: "Archive - Product-Agent OS Plugin Core Implementation Plan"
---

# Archive - Product-Agent OS Plugin Core Implementation Plan {#product-agent-os-plugin-core-implementation-plan}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

Source status: `official + experiment`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the core package, contracts, validators, fixture harness and safe merge utilities for the `product-agent-os` Codex plugin.

**Architecture:** This plan implements Track 1 from the [Product-Agent OS plugin spec](../../product-agent/product-agent-os-plugin-spec.md). It creates a repo-local plugin under `plugins/product-agent-os/`, keeps runtime logic in small Python stdlib modules under `plugins/product-agent-os/scripts/product_agent_os/`, and proves behavior with `unittest` fixture tests before lifecycle skills are written.

**Tech Stack:** Codex plugin manifest, Python 3 standard library, `unittest`, `json`, `pathlib`, `tomllib`, Markdown fixture files.

---

## Scope

This plan covers only **Plugin core and contracts**:

- plugin package skeleton;
- `plugin.json` manifest;
- core schemas and lifecycle constants;
- fixture projects;
- workspace discovery;
- control-plane, agent and hook validators;
- managed Markdown section merge utility;
- fixture eval runner;
- docs navigation for the plan.

It intentionally does not create lifecycle skill bodies, project infrastructure templates, active hooks, automations or Agents SDK runner code. Those belong to the next implementation plans.

## File Structure

Create these files:

- `plugins/product-agent-os/.codex-plugin/plugin.json` - plugin manifest and interface metadata.
- `plugins/product-agent-os/.mcp.json` - empty MCP server bundle for later extension.
- `plugins/product-agent-os/skills/.gitkeep` - keeps packaged skills directory present.
- `plugins/product-agent-os/hooks/.gitkeep` - keeps hook templates directory present.
- `plugins/product-agent-os/scripts/product_agent_os/__init__.py` - Python package marker.
- `plugins/product-agent-os/scripts/product_agent_os/contracts.py` - lifecycle states, profile names and handoff validation.
- `plugins/product-agent-os/scripts/product_agent_os/discovery.py` - workspace audit and complexity profile inference.
- `plugins/product-agent-os/scripts/product_agent_os/merge_markdown.py` - managed section insert/update logic.
- `plugins/product-agent-os/scripts/product_agent_os/validators.py` - control-plane, agent TOML and hook validation.
- `plugins/product-agent-os/scripts/detect_project.py` - CLI wrapper for discovery.
- `plugins/product-agent-os/scripts/merge_markdown.py` - CLI wrapper for Markdown merge.
- `plugins/product-agent-os/scripts/validate_control_plane.py` - CLI wrapper for control-plane validation.
- `plugins/product-agent-os/scripts/validate_agents.py` - CLI wrapper for custom agent TOML validation.
- `plugins/product-agent-os/scripts/validate_hooks.py` - CLI wrapper for hook script validation.
- `plugins/product-agent-os/scripts/run_fixture_eval.py` - CLI runner for plugin fixture checks.
- `plugins/product-agent-os/assets/fixtures/*` - fixture workspaces.
- `tests/__init__.py` - test package marker.
- `tests/product_agent_os/__init__.py` - test package marker.
- `tests/product_agent_os/test_plugin_structure.py` - manifest and package layout tests.
- `tests/product_agent_os/test_contracts.py` - lifecycle and handoff contract tests.
- `tests/product_agent_os/test_fixtures.py` - fixture completeness tests.
- `tests/product_agent_os/test_discovery.py` - workspace audit tests.
- `tests/product_agent_os/test_validators.py` - validator behavior tests.
- `tests/product_agent_os/test_merge_markdown.py` - managed Markdown merge tests.
- `tests/product_agent_os/test_fixture_eval_runner.py` - eval runner tests.

Modify these files:

- `mkdocs.yml` - add this implementation plan to navigation.

## Task 1: Plugin Skeleton and Manifest

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/product_agent_os/__init__.py`
- Create: `tests/product_agent_os/test_plugin_structure.py`
- Create: `plugins/product-agent-os/.codex-plugin/plugin.json`
- Create: `plugins/product-agent-os/.mcp.json`
- Create: `plugins/product-agent-os/skills/.gitkeep`
- Create: `plugins/product-agent-os/hooks/.gitkeep`
- Create: `plugins/product-agent-os/scripts/.gitkeep`
- Create: `plugins/product-agent-os/assets/.gitkeep`

- [ ] **Step 1: Write the failing manifest structure test**

Create `tests/__init__.py` as an empty file.

Create `tests/product_agent_os/__init__.py` as an empty file.

Create `tests/product_agent_os/test_plugin_structure.py`:

```python
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = ROOT / "plugins" / "product-agent-os"


class PluginStructureTest(unittest.TestCase):
    def test_manifest_exists_and_points_to_packaged_assets(self):
        manifest_path = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
        self.assertTrue(manifest_path.exists(), "plugin.json must exist")
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "product-agent-os")
        self.assertEqual(data["skills"], "./skills/")
        self.assertEqual(data["mcpServers"], "./.mcp.json")
        self.assertEqual(data["interface"]["displayName"], "Product-Agent OS")
        self.assertIn("Write", data["interface"]["capabilities"])

    def test_required_package_directories_exist(self):
        required = [
            ".codex-plugin",
            "skills",
            "hooks",
            "scripts",
            "assets",
        ]
        for relative in required:
            with self.subTest(relative=relative):
                self.assertTrue((PLUGIN_ROOT / relative).exists())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m unittest tests.product_agent_os.test_plugin_structure -v
```

Expected: FAIL because `plugins/product-agent-os/.codex-plugin/plugin.json` does not exist.

- [ ] **Step 3: Create plugin skeleton and manifest**

Create `plugins/product-agent-os/.codex-plugin/plugin.json`:

```json
{
  "name": "product-agent-os",
  "version": "0.1.0",
  "description": "Production-ready Codex plugin for end-to-end product-agent project delivery.",
  "author": {
    "name": "OpenAI Codex Knowledge Base",
    "email": "codex-docs@example.invalid",
    "url": "https://developers.openai.com/codex"
  },
  "homepage": "https://developers.openai.com/codex",
  "repository": "https://example.invalid/product-agent-os",
  "license": "MIT",
  "keywords": [
    "codex",
    "product-agent",
    "skills",
    "workflow",
    "automation"
  ],
  "skills": "./skills/",
  "mcpServers": "./.mcp.json",
  "interface": {
    "displayName": "Product-Agent OS",
    "shortDescription": "Guide projects from idea to PR or release with Codex.",
    "longDescription": "Creates and maintains product-agent control-plane files, lifecycle skills, project-scoped agents, evidence logs, eval gates and automation candidates.",
    "developerName": "OpenAI Codex Knowledge Base",
    "category": "Productivity",
    "capabilities": [
      "Read",
      "Write"
    ],
    "websiteURL": "https://developers.openai.com/codex",
    "privacyPolicyURL": "https://example.invalid/privacy",
    "termsOfServiceURL": "https://example.invalid/terms",
    "defaultPrompt": [
      "Use Product-Agent OS to audit this workspace and propose a safe infrastructure plan.",
      "Use Product-Agent OS to guide this feature from requirements to PR packet."
    ],
    "brandColor": "#10A37F"
  }
}
```

Create `plugins/product-agent-os/.mcp.json`:

```json
{
  "mcpServers": {}
}
```

Create `.gitkeep` files with one line:

```text
keep
```

- [ ] **Step 4: Run test to verify it passes**

Run:

```powershell
python -m unittest tests.product_agent_os.test_plugin_structure -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

If the workspace is a git repository, run:

```powershell
git add tests plugins/product-agent-os
git commit -m "feat: add product-agent-os plugin skeleton"
```

If the workspace is not a git repository, record the changed file list in the implementation run log for this task.

## Task 2: Core Contracts

**Files:**
- Create: `tests/product_agent_os/test_contracts.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/__init__.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/contracts.py`

- [ ] **Step 1: Write the failing contract tests**

Create `tests/product_agent_os/test_contracts.py`:

```python
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.contracts import (  # noqa: E402
    COMPLEXITY_PROFILES,
    LIFECYCLE_STATES,
    REQUIRED_HANDOFF_FIELDS,
    validate_handoff,
)


class ContractsTest(unittest.TestCase):
    def test_lifecycle_states_are_ordered(self):
        self.assertEqual(LIFECYCLE_STATES[0], "uninitialized")
        self.assertEqual(LIFECYCLE_STATES[-1], "maintenance")
        self.assertIn("quality_gate", LIFECYCLE_STATES)

    def test_complexity_profiles_cover_production_modes(self):
        self.assertIn("guided-small", COMPLEXITY_PROFILES)
        self.assertIn("production-team", COMPLEXITY_PROFILES)
        self.assertIn("enterprise-governed", COMPLEXITY_PROFILES)

    def test_handoff_requires_evidence_and_constraints(self):
        missing = validate_handoff({"goal": "ship feature"})
        self.assertIn("constraints", missing)
        self.assertIn("verification_evidence", missing)

    def test_handoff_rejects_empty_constraints_and_verification_evidence(self):
        payload = self._valid_handoff()
        payload["constraints"] = []
        payload["verification_evidence"] = []

        errors = validate_handoff(payload)

        self.assertIn("constraints:empty", errors)
        self.assertIn("verification_evidence:empty", errors)

    def test_handoff_requires_files_touched_or_files_proposed(self):
        payload = self._valid_handoff()
        payload["files_touched"] = []
        payload["files_proposed"] = []

        self.assertIn("files:empty", validate_handoff(payload))

    def test_valid_handoff_has_no_missing_fields(self):
        payload = self._valid_handoff()
        self.assertEqual(validate_handoff(payload), [])

    def _valid_handoff(self):
        return {
            "lifecycle_state": "plan_ready",
            "goal": "ship feature",
            "constraints": ["Do not store secrets."],
            "allowed_sources": [],
            "inputs_used": [],
            "verified_claims": [],
            "unsupported_claims": [],
            "files_touched": ["PLAN.md"],
            "files_proposed": [],
            "commands_run": [],
            "verification_evidence": ["python -m unittest tests.product_agent_os.test_contracts -v"],
            "risks": [],
            "next_agent_task": "",
            "stop_reason": "",
        }


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m unittest tests.product_agent_os.test_contracts -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'product_agent_os'`.

- [ ] **Step 3: Implement contracts**

Create `plugins/product-agent-os/scripts/product_agent_os/__init__.py`:

```python
"""Core helpers for the product-agent-os Codex plugin."""

__all__ = ["contracts"]
```

Create `plugins/product-agent-os/scripts/product_agent_os/contracts.py`:

```python
from __future__ import annotations

from typing import Any


LIFECYCLE_STATES = [
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

COMPLEXITY_PROFILES = [
    "guided-small",
    "standard-product",
    "production-team",
    "ai-product",
    "enterprise-governed",
    "autonomous-maintenance",
]

CONTROL_PLANE_FILES = [
    "AGENTS.md",
    "REQUIREMENTS.md",
    "PLAN.md",
    "TEST.md",
    "EVALS.md",
    "RUNLOG.md",
]

REQUIRED_HANDOFF_FIELDS = [
    "lifecycle_state",
    "goal",
    "constraints",
    "allowed_sources",
    "inputs_used",
    "verified_claims",
    "unsupported_claims",
    "files_touched",
    "files_proposed",
    "commands_run",
    "verification_evidence",
    "risks",
    "next_agent_task",
    "stop_reason",
]


def validate_handoff(payload: dict[str, Any]) -> list[str]:
    """Return missing or invalid handoff fields."""
    missing: list[str] = []
    for field in REQUIRED_HANDOFF_FIELDS:
        if field not in payload:
            missing.append(field)

    state = payload.get("lifecycle_state")
    if state is not None and (not isinstance(state, str) or not state.strip()):
        missing.append("lifecycle_state:empty")
    elif state is not None and state not in LIFECYCLE_STATES:
        missing.append("lifecycle_state:unknown")

    goal = payload.get("goal")
    if goal is not None and (not isinstance(goal, str) or not goal.strip()):
        missing.append("goal:empty")

    for field in [
        "allowed_sources",
        "inputs_used",
        "verified_claims",
        "unsupported_claims",
        "commands_run",
        "risks",
    ]:
        value = payload.get(field)
        if value is not None and not isinstance(value, list):
            missing.append(f"{field}:invalid")

    for field in ["constraints", "verification_evidence"]:
        value = payload.get(field)
        if value is not None and not isinstance(value, list):
            missing.append(f"{field}:invalid")
        elif value is not None and not value:
            missing.append(f"{field}:empty")

    files_touched = payload.get("files_touched")
    files_proposed = payload.get("files_proposed")
    for field, value in [
        ("files_touched", files_touched),
        ("files_proposed", files_proposed),
    ]:
        if value is not None and not isinstance(value, list):
            missing.append(f"{field}:invalid")

    if (
        isinstance(files_touched, list)
        and isinstance(files_proposed, list)
        and not files_touched
        and not files_proposed
    ):
        missing.append("files:empty")

    for field in ["next_agent_task", "stop_reason"]:
        value = payload.get(field)
        if value is not None and not isinstance(value, str):
            missing.append(f"{field}:invalid")

    return missing
```

- [ ] **Step 4: Run test to verify it passes**

Run:

```powershell
python -m unittest tests.product_agent_os.test_contracts -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

If git is available:

```powershell
git add tests/product_agent_os/test_contracts.py plugins/product-agent-os/scripts/product_agent_os
git commit -m "feat: add product agent core contracts"
```

If not, update the implementation run log with changed files.

## Task 3: Fixture Projects

**Files:**
- Create: `tests/product_agent_os/test_fixtures.py`
- Create: `plugins/product-agent-os/assets/fixtures/empty-repo/README.md`
- Create: `plugins/product-agent-os/assets/fixtures/node-app/package.json`
- Create: `plugins/product-agent-os/assets/fixtures/node-app/src/index.js`
- Create: `plugins/product-agent-os/assets/fixtures/python-app/pyproject.toml`
- Create: `plugins/product-agent-os/assets/fixtures/python-app/app/main.py`
- Create: `plugins/product-agent-os/assets/fixtures/monorepo/package.json`
- Create: `plugins/product-agent-os/assets/fixtures/monorepo/packages/api/package.json`
- Create: `plugins/product-agent-os/assets/fixtures/docs-repo/mkdocs.yml`
- Create: `plugins/product-agent-os/assets/fixtures/docs-repo/docs/index.md`
- Create: `plugins/product-agent-os/assets/fixtures/existing-codex-config/AGENTS.md`
- Create: `plugins/product-agent-os/assets/fixtures/existing-codex-config/.codex/config.toml`

- [ ] **Step 1: Write failing fixture completeness tests**

Create `tests/product_agent_os/test_fixtures.py`:

```python
import json
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"


class FixtureCompletenessTest(unittest.TestCase):
    def test_required_fixture_projects_exist(self):
        for name in [
            "empty-repo",
            "node-app",
            "python-app",
            "monorepo",
            "docs-repo",
            "existing-codex-config",
        ]:
            with self.subTest(name=name):
                self.assertTrue((FIXTURES / name).is_dir())

    def test_node_fixture_has_package_json(self):
        self.assertTrue((FIXTURES / "node-app" / "package.json").exists())

    def test_existing_codex_fixture_has_project_config(self):
        self.assertTrue((FIXTURES / "existing-codex-config" / ".codex" / "config.toml").exists())

    def test_json_fixtures_are_valid(self):
        for path in [
            FIXTURES / "node-app" / "package.json",
            FIXTURES / "monorepo" / "package.json",
            FIXTURES / "monorepo" / "packages" / "api" / "package.json",
        ]:
            with self.subTest(path=path):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertIn("name", data)

    def test_node_fixture_is_explicit_esm(self):
        data = json.loads((FIXTURES / "node-app" / "package.json").read_text(encoding="utf-8"))
        self.assertEqual(data["type"], "module")

    def test_toml_fixtures_are_valid(self):
        for path in [
            FIXTURES / "python-app" / "pyproject.toml",
            FIXTURES / "existing-codex-config" / ".codex" / "config.toml",
        ]:
            with self.subTest(path=path):
                tomllib.loads(path.read_text(encoding="utf-8"))

    def test_docs_fixture_has_docs_dir(self):
        mkdocs_config = (FIXTURES / "docs-repo" / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertIn("docs_dir: docs", mkdocs_config)
        self.assertTrue((FIXTURES / "docs-repo" / "docs").is_dir())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m unittest tests.product_agent_os.test_fixtures -v
```

Expected: FAIL because fixture directories do not exist. When updating an existing fixture set,
the ESM test should fail until `node-app/package.json` declares `"type": "module"`.

- [ ] **Step 3: Add fixture project files**

Create `plugins/product-agent-os/assets/fixtures/empty-repo/README.md`:

```markdown
# Empty Fixture

Minimal workspace with no detected stack.
```

Create `plugins/product-agent-os/assets/fixtures/node-app/package.json`:

```json
{
  "name": "node-app-fixture",
  "private": true,
  "type": "module",
  "scripts": {
    "test": "node --test",
    "build": "node src/index.js"
  },
  "devDependencies": {}
}
```

Create `plugins/product-agent-os/assets/fixtures/node-app/src/index.js`:

```javascript
export function health() {
  return "ok";
}
```

Create `plugins/product-agent-os/assets/fixtures/python-app/pyproject.toml`:

```toml
[project]
name = "python-app-fixture"
version = "0.1.0"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Create `plugins/product-agent-os/assets/fixtures/python-app/app/main.py`:

```python
def health() -> str:
    return "ok"
```

Create `plugins/product-agent-os/assets/fixtures/monorepo/package.json`:

```json
{
  "name": "monorepo-fixture",
  "private": true,
  "workspaces": [
    "packages/*"
  ]
}
```

Create `plugins/product-agent-os/assets/fixtures/monorepo/packages/api/package.json`:

```json
{
  "name": "@fixture/api",
  "private": true,
  "scripts": {
    "test": "node --test"
  }
}
```

Create `plugins/product-agent-os/assets/fixtures/docs-repo/mkdocs.yml`:

```yaml
site_name: Docs Fixture
docs_dir: docs
```

Create `plugins/product-agent-os/assets/fixtures/docs-repo/docs/index.md`:

```markdown
# Docs Fixture

Source status: `experiment`
```

Create `plugins/product-agent-os/assets/fixtures/existing-codex-config/AGENTS.md`:

```markdown
# AGENTS.md

## Existing user rules

- Preserve user-authored rules.
```

Create `plugins/product-agent-os/assets/fixtures/existing-codex-config/.codex/config.toml`:

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

- [ ] **Step 4: Run test to verify it passes**

Run:

```powershell
python -m unittest tests.product_agent_os.test_fixtures -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

If git is available:

```powershell
git add tests/product_agent_os/test_fixtures.py plugins/product-agent-os/assets/fixtures
git commit -m "test: add product agent plugin fixtures"
```

If not, update the implementation run log with changed files.

## Task 4: Workspace Discovery

**Files:**
- Create: `tests/product_agent_os/test_discovery.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/discovery.py`
- Create: `plugins/product-agent-os/scripts/detect_project.py`

- [ ] **Step 1: Write failing discovery tests**

Create `tests/product_agent_os/test_discovery.py`:

```python
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.discovery import analyze_workspace  # noqa: E402


class DiscoveryTest(unittest.TestCase):
    def test_node_app_detection(self):
        audit = analyze_workspace(FIXTURES / "node-app")
        self.assertIn("node", audit["detected_stack"])
        self.assertIn("package.json", audit["detected_files"])
        self.assertEqual(audit["complexity_profile"]["name"], "guided-small")

    def test_docs_repo_detection(self):
        audit = analyze_workspace(FIXTURES / "docs-repo")
        self.assertIn("docs", audit["detected_stack"])
        self.assertIn("mkdocs.yml", audit["detected_files"])

    def test_existing_control_plane_detection(self):
        audit = analyze_workspace(FIXTURES / "existing-codex-config")
        self.assertIn("AGENTS.md", audit["existing_control_plane"])
        self.assertIn(".codex/config.toml", audit["existing_codex_assets"])

    def test_missing_workspace_raises_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            analyze_workspace(FIXTURES / "does-not-exist")

    def test_file_workspace_raises_not_a_directory(self):
        with tempfile.NamedTemporaryFile() as handle:
            with self.assertRaises(NotADirectoryError):
                analyze_workspace(handle.name)

    def test_generated_directories_are_ignored(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            (workspace / "package.json").write_text("{}", encoding="utf-8")
            (workspace / "node_modules" / "pkg").mkdir(parents=True)
            (workspace / "node_modules" / "pkg" / "index.js").write_text("", encoding="utf-8")
            (workspace / ".git").mkdir()
            (workspace / ".git" / "config").write_text("", encoding="utf-8")
            (workspace / "site").mkdir()
            (workspace / "site" / "index.html").write_text("", encoding="utf-8")
            (workspace / "src").mkdir()
            (workspace / "src" / "app.js").write_text("", encoding="utf-8")

            audit = analyze_workspace(workspace)

        self.assertIn("package.json", audit["detected_files"])
        self.assertIn("src/app.js", audit["detected_files"])
        self.assertNotIn("node_modules/pkg/index.js", audit["detected_files"])
        self.assertNotIn(".git/config", audit["detected_files"])
        self.assertNotIn("site/index.html", audit["detected_files"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m unittest tests.product_agent_os.test_discovery -v
```

Expected: FAIL before implementation if missing/non-directory workspaces are silently accepted or generated/cache directories appear in `detected_files`.

- [ ] **Step 3: Implement workspace discovery**

Create `plugins/product-agent-os/scripts/product_agent_os/discovery.py`:

```python
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from product_agent_os.contracts import CONTROL_PLANE_FILES


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
    "node_modules",
    "site",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".codex-cache",
}


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
    return files


def _detect_stack(files: set[str]) -> list[str]:
    stack: list[str] = []
    for marker, name in STACK_MARKERS.items():
        if marker in files and name not in stack:
            stack.append(name)
    if any(path.startswith("packages/") for path in files):
        stack.append("monorepo")
    return stack


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


def analyze_workspace(root: str | Path) -> dict[str, Any]:
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
    risks: list[str] = []
    if "AGENTS.md" not in files:
        risks.append("missing durable project instructions")
    if not any("test" in path.lower() for path in files):
        risks.append("no detected test files or test configuration")
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
        "risks": risks,
        "complexity_profile": _profile_for(files, stack),
    }


def main(argv: list[str]) -> int:
    root = Path(argv[0]) if argv else Path.cwd()
    try:
        audit = analyze_workspace(root)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(audit, indent=2, sort_keys=True))
    return 0
```

Create `plugins/product-agent-os/scripts/detect_project.py`:

```python
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.discovery import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 4: Run tests and CLI check**

Run:

```powershell
python -m unittest tests.product_agent_os.test_discovery -v
python plugins\\product-agent-os\\scripts\\detect_project.py plugins\\product-agent-os\\assets\\fixtures\\node-app
python plugins\\product-agent-os\\scripts\\detect_project.py plugins\\product-agent-os\\assets\\fixtures\\does-not-exist
```

Expected: unit tests PASS; fixture CLI prints JSON containing `"node"` in `detected_stack`; missing fixture CLI exits non-zero and prints `error: workspace does not exist: ...` to stderr.

- [ ] **Step 5: Commit**

If git is available:

```powershell
git add tests/product_agent_os/test_discovery.py plugins/product-agent-os/scripts
git commit -m "feat: add workspace discovery"
```

If not, update the implementation run log with changed files.

## Task 5: Validators

**Files:**
- Create: `tests/product_agent_os/test_validators.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/validators.py`
- Create: `plugins/product-agent-os/scripts/validate_control_plane.py`
- Create: `plugins/product-agent-os/scripts/validate_agents.py`
- Create: `plugins/product-agent-os/scripts/validate_hooks.py`

- [ ] **Step 1: Write failing validator tests**

Create `tests/product_agent_os/test_validators.py`:

```python
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.validators import (  # noqa: E402
    validate_agent_file,
    validate_control_plane,
    validate_hook_file,
)


class ValidatorsTest(unittest.TestCase):
    def test_control_plane_reports_missing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = validate_control_plane(Path(tmp))
        self.assertIn("AGENTS.md", result["missing"])
        self.assertFalse(result["ok"])

    def test_agent_file_accepts_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "reviewer.toml"
            path.write_text(
                'name = "reviewer"\n'
                'description = "Reviews correctness and missing tests."\n'
                'developer_instructions = "Return findings by severity."\n',
                encoding="utf-8",
            )
            self.assertEqual(validate_agent_file(path), [])

    def test_hook_file_rejects_secret_literal(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hook.py"
            path.write_text('TOKEN = "secret-value"\n', encoding="utf-8")
            errors = validate_hook_file(path)
        self.assertIn("contains forbidden secret-like literal", errors)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m unittest tests.product_agent_os.test_validators -v
```

Expected: FAIL because `product_agent_os.validators` does not exist.

- [ ] **Step 3: Implement validators and wrappers**

Create `plugins/product-agent-os/scripts/product_agent_os/validators.py`:

```python
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None

from product_agent_os.contracts import CONTROL_PLANE_FILES


AGENT_REQUIRED_FIELDS = ["name", "description", "developer_instructions"]
SECRET_MARKERS = ["secret", "token", "private_key", "password"]


def validate_control_plane(root: Path) -> dict[str, Any]:
    missing = [name for name in CONTROL_PLANE_FILES if not (root / name).exists()]
    return {
        "ok": not missing,
        "missing": missing,
    }


def validate_agent_file(path: Path) -> list[str]:
    if tomllib is None:
        return ["tomllib unavailable"]
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"invalid toml: {exc}"]
    return [field for field in AGENT_REQUIRED_FIELDS if field not in data]


def validate_hook_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8").lower()
    errors: list[str] = []
    if any(marker in text for marker in SECRET_MARKERS):
        errors.append("contains forbidden secret-like literal")
    if "exit(2)" not in text and "sys.exit(2)" not in text:
        errors.append("no blocking exit path")
    return errors


def print_json(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("ok") else 1


def main_control_plane(argv: list[str]) -> int:
    root = Path(argv[0]) if argv else Path.cwd()
    return print_json(validate_control_plane(root))


def main_agents(argv: list[str]) -> int:
    root = Path(argv[0]) if argv else Path(".codex/agents")
    files = sorted(root.glob("*.toml")) if root.exists() else []
    errors = {str(path): validate_agent_file(path) for path in files}
    ok = bool(files) and all(not item for item in errors.values())
    return print_json({"ok": ok, "files": [str(path) for path in files], "errors": errors})


def main_hooks(argv: list[str]) -> int:
    root = Path(argv[0]) if argv else Path(".codex/hooks")
    files = sorted(root.glob("*.py")) if root.exists() else []
    errors = {str(path): validate_hook_file(path) for path in files}
    ok = bool(files) and all(not item for item in errors.values())
    return print_json({"ok": ok, "files": [str(path) for path in files], "errors": errors})
```

Create `plugins/product-agent-os/scripts/validate_control_plane.py`:

```python
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.validators import main_control_plane


if __name__ == "__main__":
    raise SystemExit(main_control_plane(sys.argv[1:]))
```

Create `plugins/product-agent-os/scripts/validate_agents.py`:

```python
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.validators import main_agents


if __name__ == "__main__":
    raise SystemExit(main_agents(sys.argv[1:]))
```

Create `plugins/product-agent-os/scripts/validate_hooks.py`:

```python
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.validators import main_hooks


if __name__ == "__main__":
    raise SystemExit(main_hooks(sys.argv[1:]))
```

- [ ] **Step 4: Run tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_validators -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

If git is available:

```powershell
git add tests/product_agent_os/test_validators.py plugins/product-agent-os/scripts
git commit -m "feat: add product agent validators"
```

If not, update the implementation run log with changed files.

## Task 6: Managed Markdown Merge

**Files:**
- Create: `tests/product_agent_os/test_merge_markdown.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/merge_markdown.py`
- Create: `plugins/product-agent-os/scripts/merge_markdown.py`

- [ ] **Step 1: Write failing merge tests**

Create `tests/product_agent_os/test_merge_markdown.py`:

```python
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.merge_markdown import merge_section  # noqa: E402


class MergeMarkdownTest(unittest.TestCase):
    def test_insert_managed_section_preserves_user_content(self):
        original = "# AGENTS.md\n\nUser rule.\n"
        updated = merge_section(original, "product-agent-os", "checks", "- Run tests.")
        self.assertIn("User rule.", updated)
        self.assertIn("product-agent-os:start checks", updated)
        self.assertIn("- Run tests.", updated)

    def test_update_existing_managed_section(self):
        original = (
            "# AGENTS.md\n\n"
            "<!-- product-agent-os:start checks -->\n"
            "- Old check.\n"
            "<!-- product-agent-os:end checks -->\n"
        )
        updated = merge_section(original, "product-agent-os", "checks", "- New check.")
        self.assertIn("- New check.", updated)
        self.assertNotIn("- Old check.", updated)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m unittest tests.product_agent_os.test_merge_markdown -v
```

Expected: FAIL because `product_agent_os.merge_markdown` does not exist.

- [ ] **Step 3: Implement merge utility and wrapper**

Create `plugins/product-agent-os/scripts/product_agent_os/merge_markdown.py`:

```python
from __future__ import annotations

import re
import sys
from pathlib import Path


def merge_section(text: str, owner: str, section_id: str, body: str) -> str:
    start = f"<!-- {owner}:start {section_id} -->"
    end = f"<!-- {owner}:end {section_id} -->"
    block = f"{start}\n{body.rstrip()}\n{end}\n"
    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end) + r"\n?",
        flags=re.DOTALL,
    )
    if pattern.search(text):
        return pattern.sub(block, text)
    separator = "" if text.endswith("\n") else "\n"
    return f"{text}{separator}\n{block}"


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("usage: merge_markdown.py <file> <owner> <section-id> <body-file>", file=sys.stderr)
        return 2
    target = Path(argv[0])
    owner = argv[1]
    section_id = argv[2]
    body = Path(argv[3]).read_text(encoding="utf-8")
    original = target.read_text(encoding="utf-8") if target.exists() else ""
    target.write_text(merge_section(original, owner, section_id, body), encoding="utf-8")
    return 0
```

Create `plugins/product-agent-os/scripts/merge_markdown.py`:

```python
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.merge_markdown import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 4: Run tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_merge_markdown -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

If git is available:

```powershell
git add tests/product_agent_os/test_merge_markdown.py plugins/product-agent-os/scripts
git commit -m "feat: add managed markdown merge"
```

If not, update the implementation run log with changed files.

## Task 7: Fixture Eval Runner

**Files:**
- Create: `tests/product_agent_os/test_fixture_eval_runner.py`
- Create: `plugins/product-agent-os/scripts/run_fixture_eval.py`

- [ ] **Step 1: Write failing eval runner tests**

Create `tests/product_agent_os/test_fixture_eval_runner.py`:

```python
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = ROOT / "plugins" / "product-agent-os" / "scripts" / "run_fixture_eval.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("run_fixture_eval", RUNNER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FixtureEvalRunnerTest(unittest.TestCase):
    def test_fixture_eval_returns_named_results(self):
        runner = load_runner()
        results = runner.evaluate_all()
        names = {item["fixture"] for item in results}
        self.assertIn("node-app", names)
        self.assertTrue(all("ok" in item for item in results))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m unittest tests.product_agent_os.test_fixture_eval_runner -v
```

Expected: FAIL because `run_fixture_eval.py` does not exist.

- [ ] **Step 3: Implement eval runner**

Create `plugins/product-agent-os/scripts/run_fixture_eval.py`:

```python
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.discovery import analyze_workspace


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = PLUGIN_ROOT / "assets" / "fixtures"


def evaluate_fixture(path: Path) -> dict[str, object]:
    audit = analyze_workspace(path)
    ok = bool(audit["workspace"]) and "complexity_profile" in audit
    return {
        "fixture": path.name,
        "ok": ok,
        "profile": audit["complexity_profile"]["name"],
        "risks": audit["risks"],
    }


def evaluate_all() -> list[dict[str, object]]:
    return [evaluate_fixture(path) for path in sorted(FIXTURES.iterdir()) if path.is_dir()]


def main() -> int:
    results = evaluate_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if results and all(item["ok"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run tests and fixture eval**

Run:

```powershell
python -m unittest tests.product_agent_os.test_fixture_eval_runner -v
python plugins\\product-agent-os\\scripts\\run_fixture_eval.py
```

Expected: unit tests PASS and fixture eval exits with code 0.

- [ ] **Step 5: Commit**

If git is available:

```powershell
git add tests/product_agent_os/test_fixture_eval_runner.py plugins/product-agent-os/scripts/run_fixture_eval.py
git commit -m "feat: add product agent fixture eval runner"
```

If not, update the implementation run log with changed files.

## Task 8: Navigation and Verification

**Files:**
- Modify: `mkdocs.yml`

- [ ] **Step 1: Add plan to MkDocs navigation**

Modify `mkdocs.yml` by adding this section near the end of `nav`:

```yaml
  - Планы реализации:
      - Product-Agent OS plugin core: superpowers/plans/2026-05-14-product-agent-os-plugin-core.md
```

- [ ] **Step 2: Run all plugin core tests**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: all `tests.product_agent_os` tests PASS.

- [ ] **Step 3: Run docs checks**

Run:

```powershell
python tools\check_docs.py
```

Expected: `OK: documentation structure checks passed`.

- [ ] **Step 4: Run strict MkDocs build**

Run:

```powershell
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; python -m mkdocs build --strict
```

Expected: documentation builds successfully.

- [ ] **Step 5: Commit**

If git is available:

```powershell
git add mkdocs.yml docs/superpowers/plans/2026-05-14-product-agent-os-plugin-core.md
git commit -m "docs: add product agent plugin core implementation plan"
```

If not, record verification results and changed files in the implementation run log.

## Self-Review

Spec coverage:

- Пакет plugin and manifest are covered by Task 1.
- Core lifecycle state, complexity profile names and handoff validation are covered by Task 2.
- Fixture projects required by production hardening are started in Task 3.
- Workspace audit and profile inference are covered by Task 4.
- Validation scripts for control-plane files, custom agents and hooks are covered by Task 5.
- Safe managed-section updates are covered by Task 6.
- Fixture eval foundation is covered by Task 7.
- Documentation validation is covered by Task 8.

Known follow-up plans:

- Lifecycle skills implementation plan.
- Generated project infrastructure implementation plan.
- Production hardening and optional Agents SDK runner implementation plan.

The plan avoids active automations, external writes and global Codex config changes. It builds only local plugin package assets and validation tooling.
