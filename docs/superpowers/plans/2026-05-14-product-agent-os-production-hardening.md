---
title: "Archive - Product-Agent OS Production Hardening Implementation Plan"
---

# Archive - Product-Agent OS Production Hardening Implementation Plan {#product-agent-os-production-hardening-implementation-plan}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

Source status: `official + experiment`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Track 4 production hardening for `product-agent-os`: staged manifest, explicit approval records, safe approved merge, rollback, hook activation gate, stronger fixture evals, source-policy validation, automation promotion validation, and optional Agents SDK runner design.

**Architecture:** Keep Track 3 rendering as the only template generation layer. Add a hardening layer that consumes staged artifacts, validates provenance and approval, plans safe writes, applies only approved changes inside the workspace, records rollback evidence, and extends fixture eval with merge/source/automation statuses. Source-policy, automation-policy, and optional Agents SDK runner design remain separate modules so default renderer behavior stays staged-first.

**Tech Stack:** Python 3 standard library, `unittest`, `pathlib`, `json`, `hashlib`, `tempfile`, `shutil`, `subprocess`, Markdown/TOML/JSON fixtures, MkDocs.

---

## Scope

This plan implements [Product-Agent OS Production Hardening Design](../specs/2026-05-14-product-agent-os-production-hardening-design.md).

In scope:

- staged manifest contract for Track 3 stage output;
- explicit approval record contract separate from merge plan id;
- read-only merge planner;
- approved apply mode;
- rollback manifest and rollback mode;
- hook activation gate;
- hardening fixtures and fixture eval expansion;
- deterministic source-policy validator;
- deterministic automation candidate validator;
- optional Agents SDK runner design document;
- docs navigation and full verification.

Out of scope:

- active Codex App automations, GitHub Actions, schedules, or recurring jobs;
- default Agents SDK runner implementation;
- dependency installation;
- network access in tests or fixture evals;
- global Codex config changes;
- plugin-root hook activation;
- replacing user-authored files without managed-section boundaries and explicit approval.

## File Structure

Create these implementation modules:

- `plugins/product-agent-os/scripts/product_agent_os/stage_manifest.py` - staged manifest, approval record, content digest, canonical JSON, and validation helpers.
- `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py` - merge plan, approval-gated apply, backup, rollback manifest, rollback mode, path safety.
- `plugins/product-agent-os/scripts/product_agent_os/source_policy.py` - deterministic source-policy scanner and report builder.
- `plugins/product-agent-os/scripts/product_agent_os/automation_policy.py` - automation candidate parser and readiness classifier.
- `plugins/product-agent-os/scripts/merge_infrastructure.py` - CLI wrapper for plan/apply/rollback.
- `plugins/product-agent-os/scripts/validate_source_policy.py` - CLI wrapper for source-policy validation.
- `plugins/product-agent-os/scripts/validate_automation_candidate.py` - CLI wrapper for automation candidate validation.

Modify these implementation files:

- `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py` - write `product-agent-os-stage-manifest.json` during stage mode and include manifest path in stage output.
- `plugins/product-agent-os/scripts/run_fixture_eval.py` - include merge, source-policy, automation, hook activation, rollback, and failure-log regression statuses.

Create these tests:

- `tests/product_agent_os/test_stage_manifest.py`
- `tests/product_agent_os/test_merge_infrastructure.py`
- `tests/product_agent_os/test_source_policy.py`
- `tests/product_agent_os/test_automation_policy.py`

Modify these tests:

- `tests/product_agent_os/test_infrastructure_renderer.py`
- `tests/product_agent_os/test_fixture_eval_runner.py`
- `tests/product_agent_os/test_plugin_structure.py`

Create these fixture folders:

- `plugins/product-agent-os/assets/fixtures/stale-merge-plan/`
- `plugins/product-agent-os/assets/fixtures/path-traversal-stage/`
- `plugins/product-agent-os/assets/fixtures/symlink-escape/`
- `plugins/product-agent-os/assets/fixtures/hook-activation-unapproved/`
- `plugins/product-agent-os/assets/fixtures/hook-activation-approved/`
- `plugins/product-agent-os/assets/fixtures/source-policy-conflict/`
- `plugins/product-agent-os/assets/fixtures/automation-candidate-valid/`
- `plugins/product-agent-os/assets/fixtures/automation-candidate-invalid/`
- `plugins/product-agent-os/assets/fixtures/rollback-required/`
- `plugins/product-agent-os/assets/fixtures/failure-log-regression/`

Create this docs artifact:

- `docs/superpowers/specs/2026-05-14-product-agent-os-agents-sdk-runner-design.md`

Modify navigation:

- `mkdocs.yml`

## Contract Decisions

Use JSON for implementation artifacts even when the design shows YAML-like shape. JSON keeps Track 4 dependency-free.

Artifact names:

- `product-agent-os-stage-manifest.json`
- `product-agent-os-approval-template.json`
- `product-agent-os-approval.json`
- `product-agent-os-rollback-manifest.json`

Allowed merge actions:

- `create_file`
- `append_managed_section`
- `replace_managed_section`
- `companion_only`
- `blocked`

Status values:

- merge plan: `needs_approval`, `blocked`, `applied`
- source policy: `ok`, `needs_review`, `blocked`
- automation promotion: `candidate_only`, `ready_for_manual_approval`, `blocked`

Safety invariants:

- Plan mode writes no files.
- Apply mode writes only inside the workspace.
- Rollback mode writes only inside the workspace.
- Stage root must not be inside the target workspace.
- Target paths and staged paths must be relative and must not contain `..`.
- Symlinked targets, target parents, stage files, and stage parents are blocked.
- Bare merge plan id is never treated as approval.
- Hook lifecycle config is not applied unless `enable_hooks` is true in the approval record.

## Task 1: Stage Manifest And Approval Record Contracts

**Files:**

- Create: `tests/product_agent_os/test_stage_manifest.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/stage_manifest.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`
- Modify: `tests/product_agent_os/test_infrastructure_renderer.py`

- [ ] **Step 1: Write failing stage manifest tests**

Create `tests/product_agent_os/test_stage_manifest.py`:

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

from product_agent_os.infrastructure import stage_infrastructure  # noqa: E402
from product_agent_os.stage_manifest import (  # noqa: E402
    APPROVAL_TEMPLATE_NAME,
    MANIFEST_NAME,
    build_approval_template,
    content_digest,
    load_stage_manifest,
    validate_approval_record,
    validate_stage_manifest,
)


class StageManifestTest(unittest.TestCase):
    def test_stage_mode_writes_manifest_with_file_digests(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)

            result = stage_infrastructure(workspace, stage_root)
            manifest_path = stage_root / MANIFEST_NAME
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertTrue(manifest_path.exists())
        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(manifest["renderer"], "product-agent-os")
        self.assertEqual(manifest["workspace"], str(workspace.resolve()))
        self.assertEqual(manifest["validation"]["ok"], True)
        self.assertEqual(result["rendered_artifacts"]["manifest_path"], str(manifest_path))
        self.assertTrue(any(item["target_path"] == "AGENTS.md" for item in manifest["files"]))
        for item in manifest["files"]:
            if item["action"] == "blocked":
                continue
            self.assertRegex(item["digest"], r"^sha256:[0-9a-f]{64}$")

    def test_load_stage_manifest_rejects_missing_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError) as error:
                load_stage_manifest(Path(tmp))

        self.assertIn("stage manifest does not exist", str(error.exception))

    def test_validate_stage_manifest_rejects_path_escape(self):
        manifest = {
            "schema_version": 1,
            "renderer": "product-agent-os",
            "renderer_version": "0.1.0",
            "workspace": "C:/workspace/project",
            "generated_at": "2026-05-14T00:00:00+00:00",
            "validation": {"ok": True, "checks": [], "errors": {}},
            "files": [
                {
                    "target_path": "../AGENTS.md",
                    "staged_path": "../AGENTS.md",
                    "action": "create",
                    "write_policy": "staged_only",
                    "digest": "sha256:" + "0" * 64,
                    "managed_section": "project-rules",
                }
            ],
        }

        errors = validate_stage_manifest(manifest)

        self.assertIn("target path escapes workspace: ../AGENTS.md", errors)

    def test_approval_template_is_not_an_approval_record(self):
        merge_plan = {
            "id": "merge-plan-abc",
            "decisions": [
                {"target_path": "AGENTS.md", "action": "create_file", "approval_required": True}
            ],
        }

        template = build_approval_template(merge_plan)
        errors = validate_approval_record(template, "merge-plan-abc", ["AGENTS.md"], ["create_file"])

        self.assertEqual(template["approval"]["merge_plan_id"], "merge-plan-abc")
        self.assertEqual(template["approval"]["approved_by"], "")
        self.assertIn("approved_by is required", errors)

    def test_completed_approval_record_must_match_plan_targets_and_actions(self):
        approval = {
            "approval": {
                "schema_version": 1,
                "merge_plan_id": "merge-plan-abc",
                "approved_by": "user",
                "approved_at": "2026-05-14T12:00:00+00:00",
                "approved_targets": ["AGENTS.md"],
                "approved_actions": ["create_file"],
                "accepted_risks": ["local workspace write"],
                "denied_targets": [],
                "notes": "Approved for fixture apply.",
                "enable_hooks": False,
                "approved_hook_events": [],
                "blocking_hooks": [],
                "hook_rollback": "",
            }
        }

        errors = validate_approval_record(approval, "merge-plan-abc", ["AGENTS.md"], ["create_file"])

        self.assertEqual(errors, [])

    def test_completed_approval_record_rejects_bare_plan_id(self):
        errors = validate_approval_record("merge-plan-abc", "merge-plan-abc", ["AGENTS.md"], ["create_file"])

        self.assertIn("approval record must be an object", errors)

    def test_content_digest_is_stable_sha256(self):
        self.assertEqual(
            content_digest("Product-Agent OS\n"),
            "sha256:6f316a8ae91c7998521da8286e88cae5ac6eac803ff45a8aa76a91b71a2e22be",
        )

    def test_approval_template_name_is_stable(self):
        self.assertEqual(APPROVAL_TEMPLATE_NAME, "product-agent-os-approval-template.json")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests and verify failure**

Run:

```powershell
python -m unittest tests.product_agent_os.test_stage_manifest -v
```

Expected: FAIL because `product_agent_os.stage_manifest` does not exist.

- [ ] **Step 3: Implement `stage_manifest.py`**

Create `plugins/product-agent-os/scripts/product_agent_os/stage_manifest.py`:

```python
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


MANIFEST_NAME = "product-agent-os-stage-manifest.json"
APPROVAL_TEMPLATE_NAME = "product-agent-os-approval-template.json"
APPROVAL_RECORD_NAME = "product-agent-os-approval.json"


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_digest(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def plan_digest(plan: dict[str, Any]) -> str:
    public_plan = json.loads(canonical_json(plan))
    return content_digest(canonical_json(public_plan))


def build_stage_manifest(
    *,
    workspace: Path,
    stage_root: Path,
    renderer_result: dict[str, Any],
    renderer_version: str,
) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    managed = {
        item["target_path"]: item.get("section_id", "")
        for item in renderer_result["rendered_artifacts"].get("managed_sections", [])
        if isinstance(item, dict)
    }
    for item in renderer_result["rendered_artifacts"]["files"]:
        if item["action"] == "blocked" or not item.get("staged_path"):
            digest = ""
        else:
            staged_path = Path(item["staged_path"])
            digest = file_digest(staged_path)
        files.append(
            {
                "target_path": item["target_path"],
                "staged_path": str(Path(item["staged_path"]).relative_to(stage_root))
                if item.get("staged_path")
                else "",
                "action": item["action"],
                "write_policy": item["write_policy"],
                "digest": digest,
                "managed_section": managed.get(item["target_path"], ""),
            }
        )

    manifest = {
        "schema_version": 1,
        "renderer": "product-agent-os",
        "renderer_version": renderer_version,
        "workspace": str(workspace.resolve()),
        "workspace_audit_digest": content_digest(str(workspace.resolve())),
        "infrastructure_plan_digest": plan_digest(renderer_result["infrastructure_plan"]),
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "validation": renderer_result["rendered_artifacts"]["validation"],
        "files": files,
    }
    return manifest


def write_stage_manifest(stage_root: Path, manifest: dict[str, Any]) -> Path:
    errors = validate_stage_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    path = stage_root / MANIFEST_NAME
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return path


def load_stage_manifest(stage_root: Path) -> dict[str, Any]:
    path = stage_root / MANIFEST_NAME
    if not path.exists():
        raise ValueError(f"stage manifest does not exist: {path}")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid stage manifest json: {exc}") from exc
    errors = validate_stage_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    return manifest


def validate_stage_manifest(manifest: Any) -> list[str]:
    if not isinstance(manifest, dict):
        return ["stage manifest must be an object"]
    errors: list[str] = []
    if manifest.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if manifest.get("renderer") != "product-agent-os":
        errors.append("renderer must be product-agent-os")
    if not isinstance(manifest.get("files"), list):
        errors.append("files must be a list")
        return errors
    for item in manifest["files"]:
        if not isinstance(item, dict):
            errors.append("file entry must be an object")
            continue
        target = str(item.get("target_path", ""))
        staged = str(item.get("staged_path", ""))
        if _unsafe_relative_path(target):
            errors.append(f"target path escapes workspace: {target}")
        if staged and _unsafe_relative_path(staged):
            errors.append(f"staged path escapes stage root: {staged}")
        digest = str(item.get("digest", ""))
        if item.get("action") != "blocked" and not digest.startswith("sha256:"):
            errors.append(f"missing digest for staged file: {target}")
    return errors


def build_approval_template(merge_plan: dict[str, Any]) -> dict[str, Any]:
    decisions = [
        item
        for item in merge_plan.get("decisions", [])
        if isinstance(item, dict) and item.get("approval_required")
    ]
    return {
        "approval": {
            "schema_version": 1,
            "merge_plan_id": merge_plan["id"],
            "approved_by": "",
            "approved_at": "",
            "approved_targets": [item["target_path"] for item in decisions],
            "approved_actions": sorted({item["action"] for item in decisions}),
            "accepted_risks": [],
            "denied_targets": [],
            "notes": "",
            "enable_hooks": False,
            "approved_hook_events": [],
            "blocking_hooks": [],
            "hook_rollback": "",
        }
    }


def validate_approval_record(
    approval_payload: Any,
    merge_plan_id: str,
    required_targets: list[str],
    required_actions: list[str],
) -> list[str]:
    if not isinstance(approval_payload, dict):
        return ["approval record must be an object"]
    approval = approval_payload.get("approval")
    if not isinstance(approval, dict):
        return ["approval field must be an object"]
    errors: list[str] = []
    if approval.get("schema_version") != 1:
        errors.append("approval schema_version must be 1")
    if approval.get("merge_plan_id") != merge_plan_id:
        errors.append("approval merge_plan_id does not match current merge plan")
    if not str(approval.get("approved_by", "")).strip():
        errors.append("approved_by is required")
    if not str(approval.get("approved_at", "")).strip():
        errors.append("approved_at is required")
    approved_targets = approval.get("approved_targets")
    approved_actions = approval.get("approved_actions")
    if not isinstance(approved_targets, list):
        errors.append("approved_targets must be a list")
    elif sorted(approved_targets) != sorted(required_targets):
        errors.append("approved_targets do not match merge plan write targets")
    if not isinstance(approved_actions, list):
        errors.append("approved_actions must be a list")
    elif sorted(approved_actions) != sorted(required_actions):
        errors.append("approved_actions do not match merge plan write actions")
    if not isinstance(approval.get("accepted_risks"), list):
        errors.append("accepted_risks must be a list")
    return errors


def _unsafe_relative_path(value: str) -> bool:
    path = Path(value)
    return not value or path.is_absolute() or path.drive != "" or ".." in path.parts
```

- [ ] **Step 4: Wire manifest writing into `stage_infrastructure`**

Modify `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`:

```python
from product_agent_os.stage_manifest import build_stage_manifest, write_stage_manifest
```

Inside `stage_infrastructure`, after the `_build_result` call returns successfully:

```python
        result = _build_result(workspace_path, audit, stage_root, write_files=True)
        manifest = build_stage_manifest(
            workspace=workspace_path,
            stage_root=stage_root,
            renderer_result=result,
            renderer_version="0.1.0",
        )
        manifest_path = write_stage_manifest(stage_root, manifest)
        result["rendered_artifacts"]["manifest_path"] = str(manifest_path)
        return result
```

Keep dry-run output unchanged except that `rendered_artifacts` may include `"manifest_path": ""` if tests need a stable key.

- [ ] **Step 5: Add renderer integration test**

Modify `tests/product_agent_os/test_infrastructure_renderer.py`:

```python
def test_stage_mode_writes_stage_manifest(self):
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / "workspace"
        stage_root = Path(tmp) / "stage"
        shutil.copytree(FIXTURES / "empty-repo", workspace)

        result = stage_infrastructure(workspace, stage_root)
        manifest = stage_root / "product-agent-os-stage-manifest.json"

    self.assertTrue(manifest.exists())
    self.assertEqual(result["rendered_artifacts"]["manifest_path"], str(manifest))
```

- [ ] **Step 6: Run focused tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_stage_manifest tests.product_agent_os.test_infrastructure_renderer -v
```

Expected: PASS.

## Task 2: Read-Only Merge Planner

**Files:**

- Create: `tests/product_agent_os/test_merge_infrastructure.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`
- Create: `plugins/product-agent-os/scripts/merge_infrastructure.py`

- [ ] **Step 1: Write failing merge planner tests**

Create `tests/product_agent_os/test_merge_infrastructure.py` with the first planner tests:

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

from product_agent_os.infrastructure import stage_infrastructure  # noqa: E402
from product_agent_os.merge_infrastructure import (  # noqa: E402
    MergeInfrastructureError,
    build_merge_plan,
)


class MergeInfrastructureTest(unittest.TestCase):
    def test_merge_plan_is_read_only_and_needs_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)
            stage_infrastructure(workspace, stage_root)
            before = self._files(workspace)

            plan = build_merge_plan(workspace, stage_root)
            after = self._files(workspace)

        self.assertEqual(before, after)
        self.assertEqual(plan["status"], "needs_approval")
        self.assertRegex(plan["id"], r"^merge-[0-9a-f]{64}$")
        self.assertTrue(any(item["action"] == "create_file" for item in plan["decisions"]))
        self.assertTrue(plan["approval_template_path"].endswith("product-agent-os-approval-template.json"))

    def test_merge_plan_rejects_missing_stage_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            workspace.mkdir()
            stage_root.mkdir()

            with self.assertRaises(MergeInfrastructureError) as error:
                build_merge_plan(workspace, stage_root)

        self.assertIn("stage manifest does not exist", str(error.exception))

    def test_merge_plan_blocks_parent_target_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            workspace.mkdir()
            stage_root.mkdir()
            (stage_root / "escape.md").write_text("bad\n", encoding="utf-8")
            manifest = {
                "schema_version": 1,
                "renderer": "product-agent-os",
                "renderer_version": "0.1.0",
                "workspace": str(workspace),
                "generated_at": "2026-05-14T00:00:00+00:00",
                "validation": {"ok": True, "checks": [], "errors": {}},
                "files": [
                    {
                        "target_path": "../escape.md",
                        "staged_path": "escape.md",
                        "action": "create",
                        "write_policy": "staged_only",
                        "digest": "sha256:" + "0" * 64,
                        "managed_section": "",
                    }
                ],
            }
            (stage_root / "product-agent-os-stage-manifest.json").write_text(
                json.dumps(manifest),
                encoding="utf-8",
            )

            with self.assertRaises(MergeInfrastructureError) as error:
                build_merge_plan(workspace, stage_root)

        self.assertIn("target path escapes workspace", str(error.exception))

    def test_existing_unmarked_config_is_companion_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "existing-codex-config", workspace)
            stage_infrastructure(workspace, stage_root)

            plan = build_merge_plan(workspace, stage_root)

        by_target = {item["target_path"]: item for item in plan["decisions"]}
        self.assertEqual(by_target[".codex/config.toml"]["action"], "companion_only")

    def _files(self, root: Path) -> list[str]:
        return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests and verify failure**

Run:

```powershell
python -m unittest tests.product_agent_os.test_merge_infrastructure -v
```

Expected: FAIL because `product_agent_os.merge_infrastructure` does not exist.

- [ ] **Step 3: Implement read-only planner**

Create `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`:

```python
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from product_agent_os.stage_manifest import (
    APPROVAL_TEMPLATE_NAME,
    build_approval_template,
    canonical_json,
    content_digest,
    file_digest,
    load_stage_manifest,
)


OWNER = "product-agent-os"


class MergeInfrastructureError(RuntimeError):
    pass


def build_merge_plan(workspace: str | Path, stage_root: str | Path) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_directory(workspace_path, "workspace")
    _validate_directory(stage_path, "stage root")
    manifest = _load_manifest(stage_path)
    decisions = [_decision_for_entry(workspace_path, stage_path, entry) for entry in manifest["files"]]
    blocked = [item for item in decisions if item["action"] == "blocked"]
    plan = {
        "id": _merge_plan_id(workspace_path, stage_path, manifest, decisions),
        "status": "blocked" if blocked else "needs_approval",
        "workspace": str(workspace_path),
        "stage_root": str(stage_path),
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "decisions": decisions,
        "blocked": [{"target_path": item["target_path"], "reason": item["reason"]} for item in blocked],
        "warnings": [],
        "verification": {
            "ok": not blocked,
            "checks": [
                "stage manifest loaded",
                "target paths stay inside workspace",
                "staged paths stay inside stage root",
                "symlink paths blocked",
            ],
            "errors": {},
        },
    }
    approval_template = build_approval_template(plan)
    approval_template_path = stage_path / APPROVAL_TEMPLATE_NAME
    approval_template_path.write_text(json.dumps(approval_template, indent=2, sort_keys=True), encoding="utf-8")
    plan["approval_template_path"] = str(approval_template_path)
    return plan
```

Add helper functions in the same file:

```python
def _load_manifest(stage_root: Path) -> dict[str, Any]:
    try:
        return load_stage_manifest(stage_root)
    except ValueError as exc:
        raise MergeInfrastructureError(str(exc)) from exc


def _validate_directory(path: Path, label: str) -> None:
    if not path.exists():
        raise MergeInfrastructureError(f"{label} does not exist: {path}")
    if not path.is_dir():
        raise MergeInfrastructureError(f"{label} is not a directory: {path}")


def _decision_for_entry(workspace: Path, stage_root: Path, entry: dict[str, Any]) -> dict[str, Any]:
    target_rel = str(entry["target_path"])
    staged_rel = str(entry.get("staged_path", ""))
    try:
        target = _safe_child(workspace, target_rel, "target path")
        staged = _safe_child(stage_root, staged_rel, "staged path") if staged_rel else None
    except MergeInfrastructureError as exc:
        return _blocked(target_rel, str(exc))
    if _has_symlink_in_path(target) or (staged is not None and _has_symlink_in_path(staged)):
        return _blocked(target_rel, "symlink path is not allowed")
    if entry.get("action") == "blocked":
        return _blocked(target_rel, "renderer marked artifact as blocked")
    if staged is None or not staged.exists():
        return _blocked(target_rel, "staged file does not exist")
    if file_digest(staged) != entry.get("digest"):
        return _blocked(target_rel, "staged digest does not match manifest")
    action = _merge_action(target, target_rel, entry)
    digest_before = file_digest(target) if target.exists() and target.is_file() else ""
    return {
        "target_path": target_rel,
        "staged_path": str(staged),
        "action": action,
        "reason": _reason_for_action(action, entry),
        "target_digest_before": digest_before,
        "staged_digest": entry["digest"],
        "approval_required": action in {"create_file", "append_managed_section", "replace_managed_section"},
        "rollback_entry": target_rel if action in {"create_file", "append_managed_section", "replace_managed_section"} else "",
        "managed_section": entry.get("managed_section", ""),
    }


def _merge_action(target: Path, target_rel: str, entry: dict[str, Any]) -> str:
    if target_rel == ".codex/hooks/hooks.json":
        return "companion_only"
    if not target.exists():
        return "create_file"
    if target.suffix.lower() == ".md" and entry.get("managed_section"):
        text = target.read_text(encoding="utf-8")
        start = f"<!-- {OWNER}:start {entry['managed_section']} -->"
        end = f"<!-- {OWNER}:end {entry['managed_section']} -->"
        if text.count(start) == 1 and text.count(end) == 1:
            return "replace_managed_section"
        if text.count(start) == 0 and text.count(end) == 0:
            return "append_managed_section"
        return "blocked"
    return "companion_only"


def _safe_child(root: Path, relative: str, label: str) -> Path:
    path = Path(relative)
    if not relative or path.is_absolute() or path.drive or ".." in path.parts:
        raise MergeInfrastructureError(f"{label} escapes workspace: {relative}")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise MergeInfrastructureError(f"{label} escapes workspace: {relative}")
    return resolved


def _has_symlink_in_path(path: Path) -> bool:
    current = path.anchor
    probe = Path(current) if current else Path()
    parts = path.parts[1:] if current else path.parts
    for part in parts:
        probe = probe / part
        if probe.exists() and probe.is_symlink():
            return True
    return False


def _merge_plan_id(workspace: Path, stage_root: Path, manifest: dict[str, Any], decisions: list[dict[str, Any]]) -> str:
    payload = {
        "workspace": str(workspace),
        "stage_root": str(stage_root),
        "manifest": manifest,
        "decisions": decisions,
    }
    return "merge-" + content_digest(canonical_json(payload)).split(":", 1)[1]


def _blocked(target_path: str, reason: str) -> dict[str, Any]:
    return {
        "target_path": target_path,
        "staged_path": "",
        "action": "blocked",
        "reason": reason,
        "target_digest_before": "",
        "staged_digest": "",
        "approval_required": False,
        "rollback_entry": "",
        "managed_section": "",
    }


def _reason_for_action(action: str, entry: dict[str, Any]) -> str:
    if action == "create_file":
        return "target does not exist and can be created after approval"
    if action == "append_managed_section":
        return "markdown target has no managed section and requires explicit append approval"
    if action == "replace_managed_section":
        return "markdown target has exactly one managed section"
    if action == "companion_only":
        return "target remains a staged companion proposal"
    return "merge action is blocked"
```

- [ ] **Step 4: Add CLI wrapper for plan mode**

Create `plugins/product-agent-os/scripts/merge_infrastructure.py`:

```python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.merge_infrastructure import (  # noqa: E402
    MergeInfrastructureError,
    build_merge_plan,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plan or apply Product-Agent OS staged infrastructure.")
    parser.add_argument("workspace")
    parser.add_argument("stage_dir")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--plan", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--rollback", metavar="ROLLBACK_MANIFEST")
    parser.add_argument("--approval-file", default="")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.plan:
            result = build_merge_plan(args.workspace, args.stage_dir)
        elif args.apply:
            raise MergeInfrastructureError("apply mode is added in the approved apply task")
        else:
            raise MergeInfrastructureError("rollback mode is added in the rollback task")
    except MergeInfrastructureError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("verification", {}).get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run focused tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_merge_infrastructure -v
```

Expected: PASS for read-only planner tests.

## Task 3: Approved Apply Mode

**Files:**

- Modify: `tests/product_agent_os/test_merge_infrastructure.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`
- Modify: `plugins/product-agent-os/scripts/merge_infrastructure.py`

- [ ] **Step 1: Add failing apply tests**

Append tests to `tests/product_agent_os/test_merge_infrastructure.py`:

```python
    def test_apply_rejects_missing_approval_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)
            stage_infrastructure(workspace, stage_root)

            with self.assertRaises(MergeInfrastructureError) as error:
                apply_merge_plan(workspace, stage_root, stage_root / "missing-approval.json")

        self.assertIn("approval file does not exist", str(error.exception))

    def test_apply_creates_approved_files_and_rollback_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)
            stage_infrastructure(workspace, stage_root)
            plan = build_merge_plan(workspace, stage_root)
            approval_file = self._write_approval(stage_root, plan)

            result = apply_merge_plan(workspace, stage_root, approval_file)

            self.assertEqual(result["status"], "applied")
            self.assertTrue((workspace / "AGENTS.md").exists())
            self.assertTrue(Path(result["rollback_manifest"]).exists())
            self.assertTrue(result["verification"]["ok"])

    def test_apply_rejects_stale_target_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)
            stage_infrastructure(workspace, stage_root)
            plan = build_merge_plan(workspace, stage_root)
            approval_file = self._write_approval(stage_root, plan)
            (workspace / "AGENTS.md").write_text("# User changed file\n", encoding="utf-8")

            with self.assertRaises(MergeInfrastructureError) as error:
                apply_merge_plan(workspace, stage_root, approval_file)

        self.assertIn("merge plan is stale", str(error.exception))

    def test_apply_does_not_enable_hooks_without_enable_hooks_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)
            stage_infrastructure(workspace, stage_root)
            plan = build_merge_plan(workspace, stage_root)
            approval_file = self._write_approval(stage_root, plan)

            result = apply_merge_plan(workspace, stage_root, approval_file)

            by_target = {item["target_path"]: item for item in result["decisions"]}
            self.assertEqual(by_target[".codex/hooks/hooks.json"]["action"], "companion_only")
            self.assertFalse((workspace / ".codex" / "hooks" / "hooks.json").exists())

    def _write_approval(self, stage_root: Path, plan: dict) -> Path:
        approval = {
            "approval": {
                "schema_version": 1,
                "merge_plan_id": plan["id"],
                "approved_by": "user",
                "approved_at": "2026-05-14T12:00:00+00:00",
                "approved_targets": [
                    item["target_path"]
                    for item in plan["decisions"]
                    if item["approval_required"] and item["target_path"] != ".codex/hooks/hooks.json"
                ],
                "approved_actions": sorted(
                    {
                        item["action"]
                        for item in plan["decisions"]
                        if item["approval_required"] and item["target_path"] != ".codex/hooks/hooks.json"
                    }
                ),
                "accepted_risks": ["local workspace write"],
                "denied_targets": [".codex/hooks/hooks.json"],
                "notes": "Approved synthetic fixture apply.",
                "enable_hooks": False,
                "approved_hook_events": [],
                "blocking_hooks": [],
                "hook_rollback": "",
            }
        }
        path = stage_root / "product-agent-os-approval.json"
        path.write_text(json.dumps(approval, indent=2, sort_keys=True), encoding="utf-8")
        return path
```

Add the import:

```python
from product_agent_os.merge_infrastructure import apply_merge_plan
```

- [ ] **Step 2: Run tests and verify failure**

Run:

```powershell
python -m unittest tests.product_agent_os.test_merge_infrastructure -v
```

Expected: FAIL because `apply_merge_plan` is not implemented.

- [ ] **Step 3: Implement approved apply**

Add to `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`:

```python
import shutil
from product_agent_os.stage_manifest import validate_approval_record


ROLLBACK_MANIFEST_NAME = "product-agent-os-rollback-manifest.json"


def apply_merge_plan(workspace: str | Path, stage_root: str | Path, approval_file: str | Path) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    approval_path = Path(approval_file).resolve()
    if not approval_path.exists():
        raise MergeInfrastructureError(f"approval file does not exist: {approval_path}")
    plan = build_merge_plan(workspace_path, stage_path)
    approval_payload = json.loads(approval_path.read_text(encoding="utf-8"))
    write_decisions = [
        item
        for item in plan["decisions"]
        if item["approval_required"] and item["target_path"] != ".codex/hooks/hooks.json"
    ]
    errors = validate_approval_record(
        approval_payload,
        plan["id"],
        [item["target_path"] for item in write_decisions],
        sorted({item["action"] for item in write_decisions}),
    )
    if errors:
        raise MergeInfrastructureError("; ".join(errors))

    applied: list[dict[str, Any]] = []
    backups_root = stage_path / "_rollback" / plan["id"] / "backups"
    backups_root.mkdir(parents=True, exist_ok=True)
    for decision in plan["decisions"]:
        if decision["action"] in {"blocked", "companion_only"}:
            applied.append(decision)
            continue
        _assert_target_is_not_stale(workspace_path, decision)
        target = _safe_child(workspace_path, decision["target_path"], "target path")
        staged = Path(decision["staged_path"]).resolve()
        backup = _backup_target(workspace_path, backups_root, target, decision["target_path"])
        if decision["action"] == "create_file":
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(staged, target)
        elif decision["action"] in {"append_managed_section", "replace_managed_section"}:
            _apply_markdown_managed_section(target, staged, decision["managed_section"])
        else:
            raise MergeInfrastructureError(f"unsupported apply action: {decision['action']}")
        applied.append({**decision, "backup_path": str(backup), "digest_after": file_digest(target)})

    rollback_manifest = _write_rollback_manifest(stage_path, plan, applied)
    return {
        "status": "applied",
        "merge_plan_id": plan["id"],
        "decisions": applied,
        "rollback_manifest": str(rollback_manifest),
        "verification": {"ok": True, "checks": ["approval validated", "writes applied", "rollback manifest written"]},
    }
```

Add helpers:

```python
def _assert_target_is_not_stale(workspace: Path, decision: dict[str, Any]) -> None:
    target = _safe_child(workspace, decision["target_path"], "target path")
    expected = decision.get("target_digest_before", "")
    actual = file_digest(target) if target.exists() and target.is_file() else ""
    if actual != expected:
        raise MergeInfrastructureError(f"merge plan is stale for {decision['target_path']}")


def _backup_target(workspace: Path, backup_root: Path, target: Path, target_rel: str) -> Path:
    safe_name = target_rel.replace("/", "__").replace("\\", "__")
    backup = backup_root / f"{safe_name}.backup"
    backup.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        shutil.copyfile(target, backup)
    else:
        backup.write_text("__PRODUCT_AGENT_OS_ABSENT__\n", encoding="utf-8")
    return backup


def _apply_markdown_managed_section(target: Path, staged: Path, section_id: str) -> None:
    from product_agent_os.merge_markdown import merge_section

    staged_text = staged.read_text(encoding="utf-8")
    body = _extract_managed_body(staged_text, section_id)
    current = target.read_text(encoding="utf-8") if target.exists() else ""
    updated = merge_section(current, OWNER, section_id, body)
    target.write_text(updated, encoding="utf-8")


def _extract_managed_body(text: str, section_id: str) -> str:
    start = f"<!-- {OWNER}:start {section_id} -->"
    end = f"<!-- {OWNER}:end {section_id} -->"
    start_index = text.find(start)
    end_index = text.find(end)
    if start_index == -1 or end_index == -1 or end_index < start_index:
        raise MergeInfrastructureError(f"staged markdown missing managed section: {section_id}")
    return text[start_index + len(start) : end_index].strip()


def _write_rollback_manifest(stage_root: Path, plan: dict[str, Any], decisions: list[dict[str, Any]]) -> Path:
    entries = []
    for item in decisions:
        if item["action"] not in {"create_file", "append_managed_section", "replace_managed_section"}:
            continue
        entries.append(
            {
                "target_path": item["target_path"],
                "action": "created" if item["action"] == "create_file" else "updated",
                "existed_before": bool(item.get("target_digest_before")),
                "digest_before": item.get("target_digest_before", ""),
                "digest_after": item["digest_after"],
                "backup_path": item["backup_path"],
            }
        )
    manifest = {
        "schema_version": 1,
        "merge_plan_id": plan["id"],
        "applied_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "workspace": plan["workspace"],
        "entries": entries,
        "verification": {"ok": True, "checks": ["rollback entries recorded"]},
    }
    path = stage_root / ROLLBACK_MANIFEST_NAME
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return path
```

- [ ] **Step 4: Update CLI apply mode**

Modify `plugins/product-agent-os/scripts/merge_infrastructure.py`:

```python
from product_agent_os.merge_infrastructure import apply_merge_plan
```

Replace the apply branch:

```python
        elif args.apply:
            if not args.approval_file:
                raise MergeInfrastructureError("--approval-file is required for apply mode")
            result = apply_merge_plan(args.workspace, args.stage_dir, args.approval_file)
```

- [ ] **Step 5: Run focused tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_merge_infrastructure -v
```

Expected: PASS.

## Task 4: Rollback Mode

**Files:**

- Modify: `tests/product_agent_os/test_merge_infrastructure.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`
- Modify: `plugins/product-agent-os/scripts/merge_infrastructure.py`

- [ ] **Step 1: Add failing rollback tests**

Append tests:

```python
    def test_rollback_restores_updated_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)
            (workspace / "AGENTS.md").write_text("# Existing\n", encoding="utf-8")
            stage_infrastructure(workspace, stage_root)
            plan = build_merge_plan(workspace, stage_root)
            approval_file = self._write_approval(stage_root, plan)
            applied = apply_merge_plan(workspace, stage_root, approval_file)

            result = rollback_merge(workspace, applied["rollback_manifest"])

            self.assertEqual(result["status"], "rolled_back")
            self.assertEqual((workspace / "AGENTS.md").read_text(encoding="utf-8"), "# Existing\n")

    def test_rollback_refuses_changed_post_apply_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)
            stage_infrastructure(workspace, stage_root)
            plan = build_merge_plan(workspace, stage_root)
            approval_file = self._write_approval(stage_root, plan)
            applied = apply_merge_plan(workspace, stage_root, approval_file)
            (workspace / "AGENTS.md").write_text("# Changed after apply\n", encoding="utf-8")

            with self.assertRaises(MergeInfrastructureError) as error:
                rollback_merge(workspace, applied["rollback_manifest"])

        self.assertIn("current digest differs from rollback manifest", str(error.exception))
```

Add import:

```python
from product_agent_os.merge_infrastructure import rollback_merge
```

- [ ] **Step 2: Implement rollback**

Add:

```python
def rollback_merge(workspace: str | Path, rollback_manifest: str | Path) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    manifest_path = Path(rollback_manifest).resolve()
    if not manifest_path.exists():
        raise MergeInfrastructureError(f"rollback manifest does not exist: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rolled_back: list[dict[str, Any]] = []
    for entry in manifest.get("entries", []):
        target = _safe_child(workspace_path, entry["target_path"], "target path")
        current = file_digest(target) if target.exists() and target.is_file() else ""
        if current != entry["digest_after"]:
            raise MergeInfrastructureError(
                f"current digest differs from rollback manifest for {entry['target_path']}"
            )
        backup = Path(entry["backup_path"]).resolve()
        if not backup.exists():
            raise MergeInfrastructureError(f"rollback backup does not exist: {backup}")
        if entry["existed_before"]:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(backup, target)
        else:
            target.unlink()
        rolled_back.append(entry)
    return {
        "status": "rolled_back",
        "merge_plan_id": manifest.get("merge_plan_id", ""),
        "entries": rolled_back,
        "verification": {"ok": True, "checks": ["rollback digests verified", "rollback applied"]},
    }
```

- [ ] **Step 3: Update CLI rollback mode**

Modify rollback branch:

```python
from product_agent_os.merge_infrastructure import rollback_merge
```

```python
        else:
            result = rollback_merge(args.workspace, args.rollback)
```

- [ ] **Step 4: Run focused tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_merge_infrastructure -v
```

Expected: PASS.

## Task 5: Hook Activation Gate

**Files:**

- Modify: `tests/product_agent_os/test_merge_infrastructure.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`

- [ ] **Step 1: Add failing hook activation tests**

Append tests:

```python
    def test_hook_lifecycle_config_requires_enable_hooks(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)
            stage_infrastructure(workspace, stage_root)
            plan = build_merge_plan(workspace, stage_root)
            approval_file = self._write_approval(stage_root, plan)

            result = apply_merge_plan(workspace, stage_root, approval_file)

        by_target = {item["target_path"]: item for item in result["decisions"]}
        self.assertEqual(by_target[".codex/hooks/hooks.json"]["action"], "companion_only")

    def test_hook_lifecycle_config_can_be_enabled_by_explicit_hook_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)
            stage_infrastructure(workspace, stage_root)
            plan = build_merge_plan(workspace, stage_root)
            approval_file = self._write_approval(stage_root, plan, enable_hooks=True)

            result = apply_merge_plan(workspace, stage_root, approval_file)

            self.assertTrue((workspace / ".codex" / "hooks" / "hooks.json").exists())
            by_target = {item["target_path"]: item for item in result["decisions"]}
            self.assertEqual(by_target[".codex/hooks/hooks.json"]["action"], "create_file")
```

Update `_write_approval` signature and behavior:

```python
    def _write_approval(self, stage_root: Path, plan: dict, enable_hooks: bool = False) -> Path:
        approved = [
            item
            for item in plan["decisions"]
            if item["approval_required"]
            and (enable_hooks or item["target_path"] != ".codex/hooks/hooks.json")
        ]
```

Set:

```python
"enable_hooks": enable_hooks,
"approved_hook_events": ["SessionStart", "PreToolUse", "PermissionRequest", "PostToolUse", "Stop"] if enable_hooks else [],
"blocking_hooks": ["PreToolUse"] if enable_hooks else [],
"hook_rollback": "restore hooks.json from rollback manifest" if enable_hooks else "",
```

- [ ] **Step 2: Modify planner/apply hook decisions**

In `_decision_for_entry`, after `action = _merge_action(target, target_rel, entry)`, leave `.codex/hooks/hooks.json` as `companion_only` in plan by default.

In `apply_merge_plan`, read:

```python
approval = approval_payload["approval"]
enable_hooks = bool(approval.get("enable_hooks"))
```

When applying decisions:

```python
        decision_to_apply = dict(decision)
        if decision["target_path"] == ".codex/hooks/hooks.json" and enable_hooks:
            decision_to_apply["action"] = "create_file" if not target.exists() else "replace_managed_section"
            decision_to_apply["approval_required"] = True
```

For existing `hooks.json`, block replacement unless the file is absent or already generated with a safe managed marker in a later design. For Track 4 implementation, tests should create it only when absent.

- [ ] **Step 3: Run focused tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_merge_infrastructure -v
```

Expected: PASS.

## Task 6: Hardening Fixtures And Failure-Log Regression

**Files:**

- Modify: `tests/product_agent_os/test_fixtures.py`
- Create fixture folders listed in File Structure
- Create fixture files under each folder

- [ ] **Step 1: Add fixture completeness tests**

Modify `tests/product_agent_os/test_fixtures.py`:

```python
TRACK_FOUR_FIXTURES = [
    "stale-merge-plan",
    "path-traversal-stage",
    "symlink-escape",
    "hook-activation-unapproved",
    "hook-activation-approved",
    "source-policy-conflict",
    "automation-candidate-valid",
    "automation-candidate-invalid",
    "rollback-required",
    "failure-log-regression",
]


def test_track_four_fixture_projects_exist(self):
    for name in TRACK_FOUR_FIXTURES:
        with self.subTest(name=name):
            self.assertTrue((FIXTURES / name).exists())
            self.assertTrue((FIXTURES / name).is_dir())
```

If `test_fixtures.py` uses a class-based style, add the method to the existing class.

- [ ] **Step 2: Create synthetic fixture content**

Create each fixture with synthetic files only:

```text
stale-merge-plan/
  README.md
  AGENTS.md
path-traversal-stage/
  README.md
symlink-escape/
  README.md
hook-activation-unapproved/
  README.md
hook-activation-approved/
  README.md
source-policy-conflict/
  docs/index.md
  docs/sources/registry.md
automation-candidate-valid/
  .codex/automation-candidates/automation-candidate.md
automation-candidate-invalid/
  .codex/automation-candidates/automation-candidate.md
rollback-required/
  AGENTS.md
failure-log-regression/
  RUNLOG.md
```

Use this content for `failure-log-regression/RUNLOG.md`:

```markdown
# RUNLOG

Source status: `experiment`

## 2026-05-14 stale merge failure

- command: `python plugins\product-agent-os\scripts\merge_infrastructure.py workspace stage --apply --approval-file stage\product-agent-os-approval.json`
- exit_code: 2
- failure: merge plan is stale for AGENTS.md
- expected_regression_fixture: stale-merge-plan
- expected_check: stale_digest_blocked
- privacy: synthetic fixture only
```

Use this valid automation candidate content:

```markdown
# Automation Candidate

Readiness: candidate_only
Project: Synthetic Fixture
name: Weekly docs drift scan
purpose: Detect source-policy drift in docs.
trigger_or_cadence: Weekly manual review candidate
required_inputs: docs directory, source registry
candidate_only: true

## manual stability evidence

- Manual workflow runs: 2
- Successful manual workflow runs: 2
- Failures observed: none in synthetic fixture
- Required approvals: owner approval before scheduling

## Stable Inputs And Outputs

- Inputs: docs directory, source registry
- Outputs: source-policy report
- Invariants: no external writes

## Owner

- Accountable owner: Docs maintainer

## Cadence

- Trigger: weekly

## Verification

- Deterministic checks: python tools\check_docs.py

## Failure Modes

- Known failure: missing source status

## Rollback Or Disable Path

- Disable path: do not create schedule

## Explicit Write Policy

- Allowed write targets: staged report only
- Forbidden write targets: external systems

## Explicit Approval

- Status: not approved for active scheduling
```

Use a shorter invalid automation candidate missing owner, verification, rollback, and write policy.

- [ ] **Step 3: Run fixture tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_fixtures -v
```

Expected: PASS.

## Task 7: Source-Policy Validator

**Files:**

- Create: `tests/product_agent_os/test_source_policy.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/source_policy.py`
- Create: `plugins/product-agent-os/scripts/validate_source_policy.py`

- [ ] **Step 1: Write failing source-policy tests**

Create `tests/product_agent_os/test_source_policy.py`:

```python
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.source_policy import validate_source_policy  # noqa: E402


class SourcePolicyTest(unittest.TestCase):
    def test_docs_repo_source_policy_is_ok_or_needs_review_without_blocking(self):
        report = validate_source_policy(ROOT)

        self.assertIn(report["status"], {"ok", "needs_review"})
        self.assertIsInstance(report["files"], list)
        self.assertEqual(report["secret_findings"], [])

    def test_missing_source_status_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "page.md").write_text("# Page\n\nCodex hooks are active by default.\n", encoding="utf-8")

            report = validate_source_policy(root)

        self.assertEqual(report["status"], "blocked")
        self.assertIn("missing Source status", str(report["errors"]))

    def test_openai_behavior_without_source_is_needs_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "page.md").write_text(
                "# Page\n\nSource status: `experiment`\n\nCodex hooks can block commands.\n",
                encoding="utf-8",
            )

            report = validate_source_policy(root)

        self.assertEqual(report["status"], "needs_review")
        self.assertIn("semantic source review required", str(report["files"]))

    def test_secret_like_literal_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "page.md").write_text(
                "# Page\n\nSource status: `experiment`\n\nAPI_KEY=plain-text-value\n",
                encoding="utf-8",
            )

            report = validate_source_policy(root)

        self.assertEqual(report["status"], "blocked")
        self.assertIn("secret-like literal", str(report["secret_findings"]))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Implement deterministic validator**

Create `plugins/product-agent-os/scripts/product_agent_os/source_policy.py`:

```python
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from product_agent_os.validators import is_forbidden_secret_assignment


OPENAI_TERMS = re.compile(r"\b(Codex|Agents SDK|OpenAI|MCP|hooks?|approvals?|models?|automation)\b", re.IGNORECASE)
OFFICIAL_SOURCE_HINTS = [
    "developers.openai.com",
    "openai.github.io",
    "github.com/openai",
    "Source status: `official",
    "source registry",
]


def validate_source_policy(workspace: str | Path) -> dict[str, Any]:
    root = Path(workspace)
    files = []
    errors = []
    secret_findings = []
    registry_updates_required = []
    docs_root = root / "docs"
    markdown_files = sorted(docs_root.rglob("*.md")) if docs_root.exists() else []
    for path in markdown_files:
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        file_report = _scan_file(relative, text)
        files.append(file_report)
        errors.extend(file_report["errors"])
        secret_findings.extend(file_report["secret_findings"])
        if file_report["registry_update_required"]:
            registry_updates_required.append(relative)
    status = _status(files, errors, secret_findings)
    return {
        "source_policy_report": {
            "status": status,
            "files": files,
            "registry_updates_required": registry_updates_required,
            "secret_findings": secret_findings,
            "errors": errors,
        },
        "status": status,
        "files": files,
        "registry_updates_required": registry_updates_required,
        "secret_findings": secret_findings,
        "errors": errors,
    }
```

Add helpers:

```python
def _scan_file(relative: str, text: str) -> dict[str, Any]:
    source_status = _source_status(text)
    errors: list[str] = []
    assumptions: list[str] = []
    unsupported_claims: list[str] = []
    missing_context: list[str] = []
    freshness_risks: list[str] = []
    secret_findings: list[str] = []
    if relative not in {"docs/index.md", "docs/sources/registry.md"} and source_status == "missing":
        errors.append(f"{relative}: missing Source status")
    for line_no, line in enumerate(text.splitlines(), start=1):
        if is_forbidden_secret_assignment(line):
            secret_findings.append(f"{relative}:{line_no}: secret-like literal")
    if OPENAI_TERMS.search(text) and not any(hint in text for hint in OFFICIAL_SOURCE_HINTS):
        missing_context.append("semantic source review required for OpenAI behavior claim")
    if "community" in text.lower() and "trust_level" not in text:
        unsupported_claims.append("community claim lacks trust_level")
    if any(term in text for term in ["models", "pricing", "security", "approval", "automation"]):
        freshness_risks.append("current behavior may require freshness review")
    return {
        "path": relative,
        "source_status": source_status,
        "supported_facts": [],
        "assumptions": assumptions,
        "unsupported_claims": unsupported_claims,
        "missing_context": missing_context,
        "freshness_risks": freshness_risks,
        "registry_update_required": bool(freshness_risks),
        "secret_findings": secret_findings,
        "errors": errors,
    }


def _source_status(text: str) -> str:
    match = re.search(r"Source status:\s*`([^`]+)`", text)
    return match.group(1).strip() if match else "missing"


def _status(files: list[dict[str, Any]], errors: list[str], secret_findings: list[str]) -> str:
    if errors or secret_findings:
        return "blocked"
    if any(item["missing_context"] or item["unsupported_claims"] for item in files):
        return "needs_review"
    return "ok"
```

- [ ] **Step 3: Add CLI wrapper**

Create `plugins/product-agent-os/scripts/validate_source_policy.py`:

```python
from __future__ import annotations

import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.source_policy import validate_source_policy  # noqa: E402


def main(argv: list[str]) -> int:
    workspace = Path(argv[0]) if argv else Path.cwd()
    result = validate_source_policy(workspace)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"ok", "needs_review"} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 4: Run focused tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_source_policy -v
```

Expected: PASS.

## Task 8: Automation Promotion Validator

**Files:**

- Create: `tests/product_agent_os/test_automation_policy.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/automation_policy.py`
- Create: `plugins/product-agent-os/scripts/validate_automation_candidate.py`

- [ ] **Step 1: Write failing automation policy tests**

Create `tests/product_agent_os/test_automation_policy.py`:

```python
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.automation_policy import validate_automation_candidate  # noqa: E402


class AutomationPolicyTest(unittest.TestCase):
    def test_valid_candidate_is_ready_for_manual_approval(self):
        candidate = (
            FIXTURES
            / "automation-candidate-valid"
            / ".codex"
            / "automation-candidates"
            / "automation-candidate.md"
        )

        report = validate_automation_candidate(candidate)

        self.assertEqual(report["status"], "ready_for_manual_approval")
        self.assertEqual(report["manual_success_count"], 2)
        self.assertTrue(report["owner_present"])
        self.assertEqual(report["errors"], [])

    def test_invalid_candidate_is_blocked(self):
        candidate = (
            FIXTURES
            / "automation-candidate-invalid"
            / ".codex"
            / "automation-candidates"
            / "automation-candidate.md"
        )

        report = validate_automation_candidate(candidate)

        self.assertEqual(report["status"], "blocked")
        self.assertIn("owner is required", report["errors"])
        self.assertIn("verification is required", report["errors"])

    def test_candidate_only_without_two_runs_is_not_ready(self):
        text = "# Automation Candidate\n\nReadiness: candidate_only\n\n## Owner\n\n- Accountable owner: Ops\n"

        report = validate_automation_candidate.from_text(text, "inline.md")

        self.assertEqual(report["status"], "candidate_only")
        self.assertIn("manual success count is below 2", report["warnings"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Implement automation policy module**

Create `plugins/product-agent-os/scripts/product_agent_os/automation_policy.py`:

```python
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from product_agent_os.validators import is_forbidden_secret_assignment


def validate_automation_candidate(candidate_file: str | Path) -> dict[str, Any]:
    path = Path(candidate_file)
    text = path.read_text(encoding="utf-8")
    return from_text(text, str(path))


def from_text(text: str, candidate_file: str) -> dict[str, Any]:
    manual_success_count = _manual_success_count(text)
    owner_present = "Accountable owner:" in text
    cadence_present = "## Cadence" in text and ("Trigger:" in text or "Frequency:" in text)
    verification_present = "## Verification" in text and "Deterministic checks:" in text
    failure_modes_present = "## Failure Modes" in text and "Known failure:" in text
    rollback_or_disable_present = "## Rollback Or Disable Path" in text and "Disable path:" in text
    write_policy_present = "## Explicit Write Policy" in text and "Allowed write targets:" in text
    explicit_approval_present = "## Explicit Approval" in text
    errors: list[str] = []
    warnings: list[str] = []
    if not owner_present:
        errors.append("owner is required")
    if not verification_present:
        errors.append("verification is required")
    if not rollback_or_disable_present:
        errors.append("rollback or disable path is required")
    if not write_policy_present:
        errors.append("write policy is required")
    if any(is_forbidden_secret_assignment(line) for line in text.splitlines()):
        errors.append("secret-like literal is forbidden")
    if manual_success_count < 2:
        warnings.append("manual success count is below 2")
    status = "blocked" if errors else "ready_for_manual_approval" if manual_success_count >= 2 else "candidate_only"
    return {
        "automation_promotion_report": {
            "status": status,
            "candidate_file": candidate_file,
            "required_fields_present": not errors,
            "manual_success_count": manual_success_count,
            "owner_present": owner_present,
            "cadence_present": cadence_present,
            "verification_present": verification_present,
            "failure_modes_present": failure_modes_present,
            "rollback_or_disable_present": rollback_or_disable_present,
            "write_policy_present": write_policy_present,
            "explicit_approval_present": explicit_approval_present,
            "errors": errors,
            "warnings": warnings,
        },
        "status": status,
        "candidate_file": candidate_file,
        "required_fields_present": not errors,
        "manual_success_count": manual_success_count,
        "owner_present": owner_present,
        "cadence_present": cadence_present,
        "verification_present": verification_present,
        "failure_modes_present": failure_modes_present,
        "rollback_or_disable_present": rollback_or_disable_present,
        "write_policy_present": write_policy_present,
        "explicit_approval_present": explicit_approval_present,
        "errors": errors,
        "warnings": warnings,
    }
```

Add:

```python
def _manual_success_count(text: str) -> int:
    match = re.search(r"Successful manual workflow runs:\s*(\d+)", text)
    if match:
        return int(match.group(1))
    match = re.search(r"Manual workflow runs:\s*(\d+)", text)
    if match and "Failures observed: none" in text:
        return int(match.group(1))
    return 0


validate_automation_candidate.from_text = from_text
```

- [ ] **Step 3: Add CLI wrapper**

Create `plugins/product-agent-os/scripts/validate_automation_candidate.py`:

```python
from __future__ import annotations

import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.automation_policy import validate_automation_candidate  # noqa: E402


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: validate_automation_candidate.py <candidate-file>", file=sys.stderr)
        return 2
    result = validate_automation_candidate(Path(argv[0]))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"candidate_only", "ready_for_manual_approval"} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 4: Run focused tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_automation_policy -v
```

Expected: PASS.

## Task 9: Fixture Eval Expansion

**Files:**

- Modify: `plugins/product-agent-os/scripts/run_fixture_eval.py`
- Modify: `tests/product_agent_os/test_fixture_eval_runner.py`

- [ ] **Step 1: Add failing fixture eval tests**

Modify `tests/product_agent_os/test_fixture_eval_runner.py`:

```python
def test_fixture_eval_includes_track_four_statuses(self):
    runner = load_runner()

    result = runner.evaluate_fixture(FIXTURES / "automation-candidate-valid")

    self.assertIn("merge_status", result)
    self.assertIn("source_policy_status", result)
    self.assertIn("automation_status", result)
    self.assertIn("rollback_status", result)
    self.assertIn("failure_log_regression_status", result)
    self.assertIn("evidence", result)


def test_fixture_eval_checks_automation_candidate_behavior(self):
    runner = load_runner()

    results = {item["fixture"]: item for item in runner.evaluate_all()}

    self.assertEqual(results["automation-candidate-valid"]["automation_status"], "ready_for_manual_approval")
    self.assertEqual(results["automation-candidate-invalid"]["automation_status"], "blocked")
    self.assertTrue(results["failure-log-regression"]["expected_checks"]["failure_log_regression_visible"])
```

Define `FIXTURES` near `RUNNER_PATH` if not already present:

```python
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
```

- [ ] **Step 2: Update fixture eval runner**

Modify imports in `plugins/product-agent-os/scripts/run_fixture_eval.py`:

```python
from product_agent_os.automation_policy import validate_automation_candidate
from product_agent_os.merge_infrastructure import MergeInfrastructureError, build_merge_plan
from product_agent_os.source_policy import validate_source_policy
```

Add helper functions:

```python
def _merge_status(path: Path) -> str:
    try:
        rendered = render_infrastructure_plan(path)
        return str(rendered["infrastructure_plan"]["status"])
    except Exception:
        return "error"


def _source_policy_status(path: Path) -> str:
    report = validate_source_policy(path)
    return str(report["status"])


def _automation_status(path: Path) -> str:
    candidates = sorted(path.rglob("automation-candidate.md"))
    if not candidates:
        return "not_applicable"
    report = validate_automation_candidate(candidates[0])
    return str(report["status"])


def _failure_log_status(path: Path) -> tuple[str, dict[str, bool]]:
    runlog = path / "RUNLOG.md"
    if not runlog.exists():
        return "not_applicable", {}
    text = runlog.read_text(encoding="utf-8")
    checks = {
        "failure_log_regression_visible": (
            "expected_regression_fixture:" in text and "expected_check:" in text
        )
    }
    return "ready" if all(checks.values()) else "needs_review", checks
```

Extend result shape in `evaluate_fixture`:

```python
    source_policy_status = _source_policy_status(path)
    automation_status = _automation_status(path)
    failure_log_status, failure_log_checks = _failure_log_status(path)
    expected_checks.update(failure_log_checks)
```

Return additional keys:

```python
"merge_status": renderer_status,
"source_policy_status": source_policy_status,
"automation_status": automation_status,
"rollback_status": "not_exercised",
"failure_log_regression_status": failure_log_status,
"evidence": {
    "files_inspected": sorted(str(item.relative_to(path)) for item in path.rglob("*") if item.is_file()),
    "commands": ["render_infrastructure_plan", "validate_source_policy", "validate_automation_candidate"],
    "reports": [],
},
```

Update `_failed_result` with the same keys and stable defaults.

- [ ] **Step 3: Run fixture eval tests and CLI**

Run:

```powershell
python -m unittest tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: tests PASS; CLI exits `0`.

## Task 10: Optional Agents SDK Runner Design Artifact

**Files:**

- Create: `docs/superpowers/specs/2026-05-14-product-agent-os-agents-sdk-runner-design.md`
- Modify: `mkdocs.yml`
- Modify: `tests/product_agent_os/test_plugin_structure.py`

- [ ] **Step 1: Add doc presence test**

Modify `tests/product_agent_os/test_plugin_structure.py`:

```python
def test_optional_agents_sdk_runner_design_is_documented_but_not_activated(self):
    runner_design = (
        ROOT
        / "docs"
        / "superpowers"
        / "specs"
        / "2026-05-14-product-agent-os-agents-sdk-runner-design.md"
    )
    self.assertTrue(runner_design.exists())
    text = runner_design.read_text(encoding="utf-8")
    self.assertIn("Source status:", text)
    self.assertIn("Codex MCP", text)
    self.assertIn("model and reasoning", text)
    self.assertIn("redaction", text)
    self.assertFalse((PLUGIN_ROOT / "scripts" / "agents_sdk_runner").exists())
```

- [ ] **Step 2: Create runner design doc**

Create `docs/superpowers/specs/2026-05-14-product-agent-os-agents-sdk-runner-design.md`:

```markdown
# Product-Agent OS Agents SDK Runner Design

Source status: `official + experiment`

Sources: Product-Agent OS production hardening design (`docs/superpowers/specs/2026-05-14-product-agent-os-production-hardening-design.md`), source registry entries for Codex with Agents SDK and OpenAI Agents SDK Python.

This document defines the optional Agents SDK runner boundary for Product-Agent OS. It is not part of default plugin activation.

## Goal

Design a future programmable runner that can orchestrate Product-Agent OS roles while preserving Codex sandbox, approvals, source policy, and evidence trail.

## Runtime Boundary

- Codex App, CLI, skills, and project `.codex/agents` remain the default workflow.
- Agents SDK runner is an advanced optional layer.
- Codex MCP performs workspace work only with explicit sandbox and approval policy.
- Runner must fail closed when credentials, source status, approval state, or ownership are unclear.

## Manager Agent

- Owns lifecycle state and final output.
- Reads `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, and `RUNLOG.md`.
- Routes to specialist agents or tools.
- Rejects handoffs missing constraints, sources, files, evidence, risks, or stop reason.

## Specialist Roles

| Role | Model and reasoning | Boundary |
| --- | --- | --- |
| Product Manager | project default, medium/high | requirements and acceptance criteria |
| Architect | project default, high/xhigh | decomposition, ownership, rollback |
| Builder | project default, medium/high | one approved implementation slice |
| Tester | project default, medium/high | deterministic checks and eval evidence |
| Reviewer | project default, high/xhigh | findings-first review |
| Release Operator | project default, medium/high | staged PR and release packets |

## Credentials

- Credentials are read from environment variables or platform configuration.
- Plaintext credential values are never written to prompts, docs, fixtures, runlogs, traces, sessions, or memory.
- Missing credentials stop runner execution before workspace mutation.

## Sessions And Tracing

- Sessions preserve application conversation continuity only.
- Sessions do not replace checked-in project memory or `RUNLOG.md`.
- Traces record tool names, handoffs, latency, failures, and approval events.
- Traces redact secrets, private customer data, raw private chat logs, and absolute user-specific paths before persistence.

## Eval Gates

- Handoff completeness.
- Source fidelity.
- Tool boundary.
- Approval handling.
- Secret retention.
- Rollback or shutdown behavior.

## Non-Goals

- No default dependency installation.
- No default network access in plugin verification.
- No active automation scheduling.
- No replacement for Codex App, CLI, project skills, or `.codex/agents`.
```

- [ ] **Step 3: Add doc to MkDocs navigation**

Under implementation specs in `mkdocs.yml`, add:

```yaml
      - Product-Agent OS Agents SDK runner design: superpowers/specs/2026-05-14-product-agent-os-agents-sdk-runner-design.md
```

- [ ] **Step 4: Run focused tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_plugin_structure -v
```

Expected: PASS.

## Task 11: Full Verification And Baseline Update

**Files:**

- Modify: `AGENTS.md`
- Modify: `docs/superpowers/plans/2026-05-14-product-agent-os-production-hardening.md`

- [ ] **Step 1: Run full unit tests**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: all tests PASS.

- [ ] **Step 2: Run fixture eval**

Run:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: exit `0`; each result includes renderer, merge, source-policy, automation, rollback, and failure-log fields.

- [ ] **Step 3: Run docs check**

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

Expected: exit `0`. The known upstream Material for MkDocs warning is acceptable only if the command exits `0`.

- [ ] **Step 5: Update `AGENTS.md` status**

Modify `AGENTS.md` under `Product-Agent OS implementation status` after verification:

```markdown
- Track 4 production hardening is implemented with staged manifest, explicit approval record, safe merge planner/apply, rollback, hook activation gate, source-policy validation, automation promotion validation, and expanded fixture eval coverage.
```

Do not add this line until the verification commands above have passed in the current run.

- [ ] **Step 6: Record final evidence**

Final implementation response must include:

- files changed;
- commands run;
- observed results;
- unresolved risks;
- next action.

If `.git` exists in the execution environment, make a focused commit after verification:

```powershell
git add AGENTS.md mkdocs.yml docs/superpowers/specs docs/superpowers/plans plugins/product-agent-os tests/product_agent_os
git commit -m "feat: harden product agent os production workflow"
```

If `.git` does not exist, report that no commit was created because the workspace is not a git repository.

## Self-Review

Spec coverage:

- Stage manifest and approval record are implemented by Task 1.
- Read-only merge plan is implemented by Task 2.
- Approved apply is implemented by Task 3.
- Rollback is implemented by Task 4.
- Hook activation gate is implemented by Task 5.
- Hardening fixtures and failure-log regression are implemented by Task 6 and wired into Task 9.
- Source-policy validator is implemented by Task 7.
- Automation promotion validator is implemented by Task 8.
- Optional Agents SDK runner remains design-only in Task 10.
- Full verification and durable status update are covered by Task 11.

Placeholder scan:

- This plan avoids unresolved placeholders and avoids relying on hidden follow-up decisions.
- Example content uses synthetic data only.
- No task requires network access or secrets.

Type and signature consistency:

- `build_merge_plan(workspace, stage_root)` returns a merge plan dictionary.
- `apply_merge_plan(workspace, stage_root, approval_file)` returns an applied result dictionary.
- `rollback_merge(workspace, rollback_manifest)` returns a rollback result dictionary.
- `validate_source_policy(workspace)` returns a source-policy report dictionary.
- `validate_automation_candidate(candidate_file)` returns an automation promotion report dictionary.

Execution handoff:

Plan complete and saved to `docs/superpowers/plans/2026-05-14-product-agent-os-production-hardening.md`.

Two execution options:

1. **Subagent-Driven (recommended)** - dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** - execute tasks in this session using executing-plans with checkpoints.
