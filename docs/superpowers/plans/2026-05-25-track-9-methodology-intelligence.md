---
title: "Archive - Track 9 Methodology Intelligence Implementation Plan"
---

# Archive - Track 9 Methodology Intelligence Implementation Plan {#track-9-methodology-intelligence-implementation-plan}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build Track 9 so Product-Agent OS can read a user workspace, classify complexity and maturity, build a Delivery Map, recommend applicable methodology domains, and stage methodology artifacts only after approval.

**Architecture:** Add a methodology intelligence layer on top of existing Track 8 scenario routing. The layer has a machine-readable methodology catalog, a read-only audit engine, a report/JSON output contract, recommendation priority rules, domain-by-domain integrations, and a final cross-domain synthesis pass. Existing staged-first and approval-bound renderer behavior remains the write boundary.

**Tech Stack:** Python standard library, `unittest`, JSON catalog assets, Markdown templates, existing `plugins/product-agent-os/scripts/product_agent_os/*` modules, existing fixture eval runner, MkDocs documentation checks.

---

## Scope Check

The approved spec covers a large product program, not a single narrow feature. This plan decomposes it into independently testable slices:

1. Repository hygiene before Track 9 work.
2. Track 9 foundation: shared schemas, catalog loader, audit contract, report renderer, CLI wrapper and discovery integration.
3. Twelve methodology domain integrations, one source file at a time.
4. Cross-domain synthesis to remove duplicates, conflicts and over-applied gates.
5. Final docs, evals and baseline refresh.

Every task must be implemented with a focused commit. Do not batch multiple domain integrations into one commit.

## Working Tree Rule

At plan creation time the working tree contains unrelated pending changes:

- `README.md` and `PLAN.md` edits from the project positioning cleanup.
- deletion of the old tracked root `product-agent-os/` package copy.

Track 9 execution must start from a clean intentional base. Do not revert those user changes. Commit them as their own cleanup commit before changing Track 9 implementation files.

## File Structure

### New Plugin Files

- `plugins/product-agent-os/assets/methodology/methodology-catalog.json`
  Canonical Track 9 methodology domain catalog consumed by scripts and tests.

- `plugins/product-agent-os/assets/templates/reports/methodology-audit-report.md`
  Human-readable report template for read-only methodology audits.

- `plugins/product-agent-os/scripts/product_agent_os/methodology_catalog.py`
  Loads and validates the methodology catalog.

- `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`
  Builds complexity, maturity, Delivery Map, methodology applicability, recommendations, questions and assumptions.

- `plugins/product-agent-os/scripts/product_agent_os/methodology_report.py`
  Renders `methodology-audit-report.md` from the audit result.

- `plugins/product-agent-os/scripts/run_methodology_audit.py`
  CLI wrapper for read-only audit output.

### Modified Plugin Files

- `plugins/product-agent-os/scripts/product_agent_os/discovery.py`
  Add methodology intelligence packet without removing existing Track 8 `methodology_applicability`.

- `plugins/product-agent-os/scripts/product_agent_os/templates.py`
  Register methodology report template and later domain artifact templates.

- `plugins/product-agent-os/scripts/run_fixture_eval.py`
  Add fixture eval keys for methodology intelligence contracts.

- `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`
  Explain read-only methodology audit, Delivery Map and questionnaire output.

- `plugins/product-agent-os/skills/requirements-author/SKILL.md`
  Use product, requirement and domain recommendations where applicable.

- `plugins/product-agent-os/skills/implementation-planner/SKILL.md`
  Treat applicable Track 9 gates as plan blockers or accepted gaps.

- `plugins/product-agent-os/skills/agent-team-designer/SKILL.md`
  Use Delivery Map ownership and boundary signals for subagent/worktree split.

- `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`
  Convert domain recommendations into deterministic checks, evals and evidence.

- `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`
  Review missing evidence, accepted gaps, conflicts and cross-domain risk.

- `plugins/product-agent-os/skills/pr-release-operator/SKILL.md`
  Include delivery, security, API, data, AI and release methodology impact.

- `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md`
  Record methodology lessons and synthesis backlog decisions.

- `plugins/product-agent-os/skills/automation-promoter/SKILL.md`
  Require methodology maturity evidence before automation promotion.

### New Or Modified Tests

- `tests/product_agent_os/test_methodology_catalog.py`
  Catalog schema, all 12 domains, status vocab, priority vocab, source file references and domain gate coverage.

- `tests/product_agent_os/test_methodology_audit.py`
  Complexity/maturity classification, Delivery Map shape, unknown handling, recommendations and safe-next-action contract.

- `tests/product_agent_os/test_methodology_report.py`
  Markdown report sections, no secrets/private path leakage, JSON/report alignment.

- `tests/product_agent_os/test_discovery.py`
  Existing tests extended to assert `methodology_intelligence` packet shape and false-positive behavior.

- `tests/product_agent_os/test_fixture_eval_runner.py`
  Fixture eval keys for catalog/report/audit/domain coverage.

- `tests/product_agent_os/test_plugin_structure.py`
  Methodology asset and CLI wrapper are packaged under `plugins/product-agent-os/`.

### New Or Modified Docs

- `docs/sources/product-agent-os-track-9-backlog.md`
  Living Track 9 backlog and domain deep-audit log.

- `docs/product-agent-os/methodology-intelligence.md`
  User-facing Track 9 onboarding, report, JSON and staged artifact behavior.

- `docs/product-agent-os/index.md`
  Link to methodology intelligence docs.

- `docs/product-agent-os/architecture.md`
  Add Track 9 read-only audit and staged artifact flow.

- `docs/product-agent-os/behavioral-evals.md`
  Add methodology intelligence fixture and transcript eval strategy.

- `mkdocs.yml`
  Add the new Product-Agent OS methodology intelligence page.

- `tools/check_docs.py`
  Require the new Product-Agent OS methodology intelligence page.

## Shared Contracts

Use these exact vocabularies unless a later synthesis commit explicitly changes them.

```python
READINESS_STATUSES = [
    "not_applicable",
    "applicable_missing",
    "present_unverified",
    "present_verified",
    "proposal_staged",
    "explicit_gap_accepted",
    "approval_required",
]

RECOMMENDATION_PRIORITIES = [
    "P0_blocker",
    "P1_high_risk",
    "P2_recommended",
    "P3_optional_maturity",
    "not_applicable",
]

MATURITY_LEVELS = [
    "baseline",
    "team",
    "production",
    "regulated",
]

COMPLEXITY_PROFILES = [
    "simple",
    "standard",
    "complex",
    "high_risk",
]
```

Each methodology domain entry must have these keys:

```json
{
  "id": "business_product",
  "title": "Business & Product",
  "source_file": "docs/methodologies/business-product.md",
  "purpose": "Product hypothesis, value, opportunities, metrics, guardrails and measurement.",
  "applies_when": [],
  "not_applicable_when": [],
  "maturity_impact": [],
  "complexity_impact": [],
  "track8_scenarios": [],
  "artifacts": [],
  "gates": [],
  "eval_fields": [],
  "overlaps": []
}
```

Each gate must have these keys:

```json
{
  "id": "product_hypothesis_present",
  "trigger": "Any behavior-changing or product-labeled slice.",
  "required_evidence": ["user or segment", "problem or opportunity", "expected outcome", "owner or accepted gap"],
  "default_status": "applicable_missing",
  "owner_hint": "product owner or requester",
  "false_positive_risk": "Do not require for mechanical formatting or docs typo fixes."
}
```

Each recommendation must have these keys:

```json
{
  "priority": "P1_high_risk",
  "reason": "The project has database migration signals without a migration plan.",
  "domain": "database_data",
  "gate": "database_migration_plan_present",
  "artifact": "database-migration-plan.md",
  "evidence_required": ["ordered migration steps", "dry run command", "rollback or compensation", "owner approval"],
  "evidence_owner": "data owner",
  "approval_boundary": "approval_required before production database access or migration execution",
  "accepted_gap_option": "explicit_gap_accepted with owner, reason, residual risk and review date",
  "residual_risk": "Artifact presence does not prove the migration is safe.",
  "safe_next_action": "Stage a migration plan proposal without connecting to production data."
}
```

## Baseline Commands

Run these before starting implementation:

```powershell
git status --short --branch
python tools\check_docs.py
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
```

Expected baseline before Track 9 implementation:

- docs check exits `0`;
- full unittest exits `0`;
- fixture eval exits `0`;
- transcript eval exits `0`;
- compatibility returns `status: compatible`.

---

### Task 0: Commit Existing Structure Cleanup

**Files:**
- Stage existing user-approved changes only:
  - `README.md`
  - `PLAN.md`
  - `product-agent-os/**` deleted paths

- [ ] **Step 1: Inspect current status**

Run:

```powershell
git status --short --branch
```

Expected: `README.md`, `PLAN.md`, and deleted `product-agent-os/**` paths are present; no Track 9 implementation files are modified.

- [ ] **Step 2: Confirm plugin source path still exists**

Run:

```powershell
Test-Path plugins\product-agent-os\.codex-plugin\plugin.json
Test-Path plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected output:

```text
True
True
```

- [ ] **Step 3: Run the already-established cleanup verification**

Run:

```powershell
python tools\check_docs.py
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
```

Expected: all commands exit `0`; compatibility prints `status: compatible`.

- [ ] **Step 4: Commit only the cleanup**

Run:

```powershell
git add README.md PLAN.md product-agent-os
git commit -m "chore: remove root product-agent-os package copy"
```

Expected: commit succeeds and does not include Track 9 files.

---

### Task 1: Add RED Tests For Methodology Catalog Contract

**Files:**
- Create: `tests/product_agent_os/test_methodology_catalog.py`
- Read: `docs/superpowers/specs/2026-05-25-track-9-methodology-intelligence-design.md`

- [ ] **Step 1: Create catalog contract tests**

Create `tests/product_agent_os/test_methodology_catalog.py` with this content:

```python
import unittest
from pathlib import Path


class MethodologyCatalogContractTest(unittest.TestCase):
    def test_catalog_loader_exists_and_exposes_vocabularies(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        catalog = load_methodology_catalog()
        self.assertEqual(catalog["version"], 1)
        self.assertEqual(
            catalog["readiness_statuses"],
            [
                "not_applicable",
                "applicable_missing",
                "present_unverified",
                "present_verified",
                "proposal_staged",
                "explicit_gap_accepted",
                "approval_required",
            ],
        )
        self.assertEqual(
            catalog["recommendation_priorities"],
            [
                "P0_blocker",
                "P1_high_risk",
                "P2_recommended",
                "P3_optional_maturity",
                "not_applicable",
            ],
        )
        self.assertEqual(catalog["maturity_levels"], ["baseline", "team", "production", "regulated"])
        self.assertEqual(catalog["complexity_profiles"], ["simple", "standard", "complex", "high_risk"])

    def test_catalog_contains_all_track_nine_domains_in_order(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        catalog = load_methodology_catalog()
        self.assertEqual(
            [domain["id"] for domain in catalog["domains"]],
            [
                "business_product",
                "requirements_domain",
                "solution_architecture",
                "quality_testing_evals",
                "codex_agentic_workflow",
                "frontend",
                "backend",
                "api_integrations",
                "database_data",
                "llm_ai_rag",
                "security_privacy_compliance",
                "delivery_release_operations",
            ],
        )

    def test_catalog_source_files_exist(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        repo_root = Path(__file__).resolve().parents[2]
        catalog = load_methodology_catalog()
        for domain in catalog["domains"]:
            with self.subTest(domain=domain["id"]):
                self.assertTrue((repo_root / domain["source_file"]).is_file())

    def test_each_domain_has_required_contract_fields(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        required_keys = {
            "id",
            "title",
            "source_file",
            "purpose",
            "applies_when",
            "not_applicable_when",
            "maturity_impact",
            "complexity_impact",
            "track8_scenarios",
            "artifacts",
            "gates",
            "eval_fields",
            "overlaps",
        }
        catalog = load_methodology_catalog()
        for domain in catalog["domains"]:
            with self.subTest(domain=domain["id"]):
                self.assertEqual(set(domain), required_keys)
                self.assertIsInstance(domain["applies_when"], list)
                self.assertIsInstance(domain["not_applicable_when"], list)
                self.assertIsInstance(domain["artifacts"], list)
                self.assertIsInstance(domain["gates"], list)
                self.assertIsInstance(domain["eval_fields"], list)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new test and verify RED**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail with `ModuleNotFoundError` for `product_agent_os.methodology_catalog`.

- [ ] **Step 3: Commit the RED test**

Run:

```powershell
git add tests\product_agent_os\test_methodology_catalog.py
git commit -m "test: add methodology catalog contract"
```

Expected: commit succeeds with one new test file.

---

### Task 2: Implement Catalog Loader And Base Catalog

**Files:**
- Create: `plugins/product-agent-os/assets/methodology/methodology-catalog.json`
- Create: `plugins/product-agent-os/scripts/product_agent_os/methodology_catalog.py`
- Modify: `tests/product_agent_os/test_plugin_structure.py`
- Modify: `plugins/product-agent-os/README.md`

- [ ] **Step 1: Add base catalog JSON**

Create `plugins/product-agent-os/assets/methodology/methodology-catalog.json` with version, vocabularies and all 12 domain entries. Each domain entry must include the contract fields from Task 1. Use the source file paths and purposes from the approved spec.

Use these domain ids and source files exactly:

```json
[
  ["business_product", "docs/methodologies/business-product.md"],
  ["requirements_domain", "docs/methodologies/requirements-domain.md"],
  ["solution_architecture", "docs/methodologies/solution-architecture.md"],
  ["quality_testing_evals", "docs/methodologies/quality-testing-evals.md"],
  ["codex_agentic_workflow", "docs/methodologies/codex-agentic-workflow.md"],
  ["frontend", "docs/methodologies/frontend.md"],
  ["backend", "docs/methodologies/backend.md"],
  ["api_integrations", "docs/methodologies/api-integrations.md"],
  ["database_data", "docs/methodologies/database-data.md"],
  ["llm_ai_rag", "docs/methodologies/llm-ai-rag.md"],
  ["security_privacy_compliance", "docs/methodologies/security-privacy-compliance.md"],
  ["delivery_release_operations", "docs/methodologies/delivery-release-operations.md"]
]
```

- [ ] **Step 2: Add catalog loader**

Create `plugins/product-agent-os/scripts/product_agent_os/methodology_catalog.py` with:

```python
"""Methodology catalog loading and validation for Product-Agent OS Track 9."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


READINESS_STATUSES = [
    "not_applicable",
    "applicable_missing",
    "present_unverified",
    "present_verified",
    "proposal_staged",
    "explicit_gap_accepted",
    "approval_required",
]

RECOMMENDATION_PRIORITIES = [
    "P0_blocker",
    "P1_high_risk",
    "P2_recommended",
    "P3_optional_maturity",
    "not_applicable",
]

MATURITY_LEVELS = ["baseline", "team", "production", "regulated"]
COMPLEXITY_PROFILES = ["simple", "standard", "complex", "high_risk"]

DOMAIN_KEYS = {
    "id",
    "title",
    "source_file",
    "purpose",
    "applies_when",
    "not_applicable_when",
    "maturity_impact",
    "complexity_impact",
    "track8_scenarios",
    "artifacts",
    "gates",
    "eval_fields",
    "overlaps",
}


def _plugin_root() -> Path:
    return Path(__file__).resolve().parents[2]


def catalog_path() -> Path:
    return _plugin_root() / "assets" / "methodology" / "methodology-catalog.json"


def load_methodology_catalog(path: str | Path | None = None) -> dict[str, Any]:
    catalog_file = Path(path) if path is not None else catalog_path()
    data = json.loads(catalog_file.read_text(encoding="utf-8"))
    errors = validate_methodology_catalog(data)
    if errors:
        raise ValueError("; ".join(errors))
    return data


def validate_methodology_catalog(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("version") != 1:
        errors.append("version must be 1")
    if data.get("readiness_statuses") != READINESS_STATUSES:
        errors.append("readiness_statuses mismatch")
    if data.get("recommendation_priorities") != RECOMMENDATION_PRIORITIES:
        errors.append("recommendation_priorities mismatch")
    if data.get("maturity_levels") != MATURITY_LEVELS:
        errors.append("maturity_levels mismatch")
    if data.get("complexity_profiles") != COMPLEXITY_PROFILES:
        errors.append("complexity_profiles mismatch")
    domains = data.get("domains")
    if not isinstance(domains, list) or not domains:
        errors.append("domains must be a non-empty list")
        return errors
    seen: set[str] = set()
    for index, domain in enumerate(domains):
        if not isinstance(domain, dict):
            errors.append(f"domains[{index}] must be an object")
            continue
        domain_id = str(domain.get("id", f"index-{index}"))
        if domain_id in seen:
            errors.append(f"duplicate domain id: {domain_id}")
        seen.add(domain_id)
        if set(domain) != DOMAIN_KEYS:
            errors.append(f"{domain_id} keys mismatch")
        for field in [
            "applies_when",
            "not_applicable_when",
            "maturity_impact",
            "complexity_impact",
            "track8_scenarios",
            "artifacts",
            "gates",
            "eval_fields",
            "overlaps",
        ]:
            if not isinstance(domain.get(field), list):
                errors.append(f"{domain_id}.{field} must be a list")
    return errors
```

- [ ] **Step 3: Add plugin structure assertion**

Modify `tests/product_agent_os/test_plugin_structure.py` and add a test named `test_methodology_catalog_is_packaged`.

The test must assert:

```python
catalog = PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json"
self.assertTrue(catalog.is_file())
```

Use the existing `PLUGIN_ROOT` constant in that file.

- [ ] **Step 4: Run focused tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_plugin_structure -v
```

Expected: all tests pass.

- [ ] **Step 5: Run full plugin baseline**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
```

Expected: all commands exit `0`.

- [ ] **Step 6: Commit catalog foundation**

Run:

```powershell
git add plugins\product-agent-os\assets\methodology\methodology-catalog.json plugins\product-agent-os\scripts\product_agent_os\methodology_catalog.py tests\product_agent_os\test_methodology_catalog.py tests\product_agent_os\test_plugin_structure.py plugins\product-agent-os\README.md
git commit -m "feat: add methodology catalog foundation"
```

Expected: commit succeeds.

---

### Task 3: Add RED Tests For Methodology Audit Contract

**Files:**
- Create: `tests/product_agent_os/test_methodology_audit.py`

- [ ] **Step 1: Create audit contract tests**

Create `tests/product_agent_os/test_methodology_audit.py` with:

```python
import tempfile
import unittest
from pathlib import Path


class MethodologyAuditContractTest(unittest.TestCase):
    def test_empty_workspace_returns_baseline_simple_with_questions(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            result = build_methodology_audit(Path(tmp), intent_hint="new MVP idea")

        self.assertEqual(result["maturity_level"]["selected"], "baseline")
        self.assertEqual(result["complexity_profile"]["selected"], "simple")
        self.assertIn("delivery_map", result)
        self.assertIn("questions_for_owner", result)
        self.assertIn("safe_next_action", result)
        self.assertEqual(result["write_policy"], "read_only")

    def test_workspace_with_api_database_and_ci_routes_complex(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "openapi.yaml").write_text("openapi: 3.1.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n", encoding="utf-8")
            (root / "migrations").mkdir()
            (root / "migrations" / "001_init.sql").write_text("create table accounts(id text primary key);\n", encoding="utf-8")
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
            result = build_methodology_audit(root, intent_hint="prepare for production API release")

        self.assertIn(result["maturity_level"]["selected"], ["team", "production"])
        self.assertIn(result["complexity_profile"]["selected"], ["complex", "high_risk"])
        domain_ids = [domain["id"] for domain in result["methodology_domains"] if domain["status"] != "not_applicable"]
        self.assertIn("api_integrations", domain_ids)
        self.assertIn("database_data", domain_ids)
        self.assertIn("delivery_release_operations", domain_ids)

    def test_recommendations_have_stable_shape(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"vitest"}}\n', encoding="utf-8")
            result = build_methodology_audit(root, intent_hint="ship frontend feature")

        required_keys = {
            "priority",
            "reason",
            "domain",
            "gate",
            "artifact",
            "evidence_required",
            "evidence_owner",
            "approval_boundary",
            "accepted_gap_option",
            "residual_risk",
            "safe_next_action",
        }
        self.assertGreaterEqual(len(result["recommendations"]), 1)
        for recommendation in result["recommendations"]:
            self.assertEqual(set(recommendation), required_keys)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run audit tests and verify RED**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_audit -v
```

Expected: fail with `ModuleNotFoundError` for `product_agent_os.methodology_audit`.

- [ ] **Step 3: Commit the RED tests**

Run:

```powershell
git add tests\product_agent_os\test_methodology_audit.py
git commit -m "test: add methodology audit contract"
```

Expected: commit succeeds.

---

### Task 4: Implement Read-Only Audit Engine

**Files:**
- Create: `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/discovery.py`
- Test: `tests/product_agent_os/test_methodology_audit.py`
- Test: `tests/product_agent_os/test_discovery.py`

- [ ] **Step 1: Implement audit data builder**

Create `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`.

Required public function:

```python
def build_methodology_audit(workspace: Path, intent_hint: str = "") -> dict[str, Any]:
```

The result must contain:

```python
{
    "status": "ok",
    "write_policy": "read_only",
    "maturity_level": {"selected": "...", "confidence": "...", "reasons": []},
    "complexity_profile": {"selected": "...", "confidence": "...", "reasons": []},
    "observed_signals": [],
    "intent_signals": [],
    "unknowns": [],
    "questions_for_owner": [],
    "provisional_assumptions": [],
    "delivery_map": {
        "surface_map": {},
        "system_map": {},
        "lifecycle_map": {},
        "methodology_map": {},
        "next_action_map": [],
    },
    "methodology_domains": [],
    "recommendations": [],
    "safe_next_action": "...",
}
```

Implement deterministic workspace signal checks for these paths:

- `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`;
- `openapi.yaml`, `openapi.yml`, `openapi.json`;
- `asyncapi.yaml`, `asyncapi.yml`, `asyncapi.json`;
- `schema.graphql`, `.proto`;
- `migrations/`, `prisma/`, `alembic.ini`, `dbt_project.yml`;
- `.github/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`;
- `Dockerfile`, `docker-compose.yml`, `k8s/`, `serverless.yml`;
- `docs/`, `README.md`, `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- `evals/`, `prompts/`, `rag/`, `vector`, `embeddings`.

- [ ] **Step 2: Implement basic classification rules**

Use these deterministic rules:

- Empty or README-only workspace: `maturity_level=baseline`, `complexity_profile=simple`.
- API contract plus migrations or CI: at least `complexity_profile=complex`.
- Production intent with CI, release files or deployment manifests: at least `maturity_level=production`.
- Security, privacy, payment, PII, compliance, healthcare, finance, production data, auth, authorization or secret intent: `complexity_profile=high_risk`.
- Regulated intent terms `regulated`, `compliance`, `audit`, `HIPAA`, `PCI`, `SOC2`, `finance`, `healthcare`, `minors`: `maturity_level=regulated`.

Intent terms affect `intent_signals` and confidence, but must not be represented as observed file evidence.

- [ ] **Step 3: Add domain applicability**

Use catalog domains and map these signals:

- `business_product`: applicable for behavior/product/MVP/release/user/value/metric intent.
- `requirements_domain`: applicable for non-empty projects and behavior-changing intent.
- `solution_architecture`: applicable for complex, team, production, API, data, AI, runtime or multi-surface projects.
- `quality_testing_evals`: applicable for every non-trivial project.
- `codex_agentic_workflow`: applicable when Product-Agent OS is used.
- `frontend`: applicable for frontend framework/package signals or UI intent.
- `backend`: applicable for server, API, service, worker, queue or backend framework signals.
- `api_integrations`: applicable for OpenAPI, AsyncAPI, GraphQL, protobuf, webhook, external integration or API intent.
- `database_data`: applicable for migration, DB schema, ORM, data store or production data signals.
- `llm_ai_rag`: applicable for prompt, model, eval, RAG, vector, embedding or AI intent.
- `security_privacy_compliance`: applicable for high-risk, auth, secrets, PII, payment, compliance or regulated signals.
- `delivery_release_operations`: applicable for production, CI, release, deploy, package, Docker, Kubernetes or operations signals.

- [ ] **Step 4: Generate default recommendations**

Recommendations must be deterministic and modest:

- Always include `codex_agentic_workflow` recommendation for missing control-plane files in Product-Agent OS context.
- If no test command or test evidence is detected, add `P0_blocker` for `quality_strategy_present`.
- If API signals exist without contract tests, add `P1_high_risk` for `api_contract_source_present`.
- If DB migration signals exist, add `P1_high_risk` for `database_migration_plan_present`.
- If high-risk signals exist, add `P1_high_risk` for `security_risk_review_present`.
- If production/release signals exist, add `P1_high_risk` for `release_evidence_present`.

- [ ] **Step 5: Integrate into discovery output**

Modify `plugins/product-agent-os/scripts/product_agent_os/discovery.py` so the existing discovery result includes a top-level `methodology_intelligence` key.

The value must be the result of `build_methodology_audit(...)` or a reduced safe packet with the same high-level keys. Do not remove existing `methodology_applicability`.

- [ ] **Step 6: Add discovery test**

Modify `tests/product_agent_os/test_discovery.py` and add a test named `test_discovery_includes_methodology_intelligence_packet`.

The test must assert:

```python
result = discover_workspace(fixture_path)
self.assertIn("methodology_intelligence", result)
packet = result["methodology_intelligence"]
self.assertIn("maturity_level", packet)
self.assertIn("complexity_profile", packet)
self.assertIn("delivery_map", packet)
self.assertIn("recommendations", packet)
self.assertEqual(packet["write_policy"], "read_only")
```

- [ ] **Step 7: Run focused tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery -v
```

Expected: all tests pass.

- [ ] **Step 8: Run fixture eval smoke check**

Run:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: exit `0`.

- [ ] **Step 9: Commit audit engine**

Run:

```powershell
git add plugins\product-agent-os\scripts\product_agent_os\methodology_audit.py plugins\product-agent-os\scripts\product_agent_os\discovery.py tests\product_agent_os\test_methodology_audit.py tests\product_agent_os\test_discovery.py
git commit -m "feat: add read-only methodology audit"
```

Expected: commit succeeds.

---

### Task 5: Add Methodology Audit Report Renderer And CLI

**Files:**
- Create: `plugins/product-agent-os/assets/templates/reports/methodology-audit-report.md`
- Create: `plugins/product-agent-os/scripts/product_agent_os/methodology_report.py`
- Create: `plugins/product-agent-os/scripts/run_methodology_audit.py`
- Create: `tests/product_agent_os/test_methodology_report.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/templates.py`
- Modify: `tests/product_agent_os/test_plugin_structure.py`

- [ ] **Step 1: Add RED report tests**

Create `tests/product_agent_os/test_methodology_report.py` with tests for:

- report includes `# Product-Agent OS Methodology Audit`;
- report includes `Maturity Level`, `Complexity Profile`, `Delivery Map`, `Recommendations`, `Questions For Owner`, `Provisional Assumptions`, `Safe Next Action`;
- report renderer does not include raw absolute local user paths;
- CLI prints JSON when `--json` is provided.

Use a temporary workspace with `package.json` and `openapi.yaml`.

- [ ] **Step 2: Run report tests and verify RED**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_report -v
```

Expected: fail with `ModuleNotFoundError` for `product_agent_os.methodology_report`.

- [ ] **Step 3: Add report template**

Create `plugins/product-agent-os/assets/templates/reports/methodology-audit-report.md` with these sections:

```markdown
# Product-Agent OS Methodology Audit

Source status: `local audit output`

## Maturity Level

## Complexity Profile

## Delivery Map

## Methodology Domains

## Recommendations

## Questions For Owner

## Provisional Assumptions

## Approval Boundaries

## Safe Next Action

## Residual Risks
```

- [ ] **Step 4: Implement report renderer**

Create `plugins/product-agent-os/scripts/product_agent_os/methodology_report.py` with:

```python
def render_methodology_audit_report(audit: dict[str, Any]) -> str:
```

The renderer must use deterministic Markdown, sort recommendation sections by priority order, and redact local absolute paths with the existing redaction helper if available. If no helper is available, replace the current user's home path prefix with `[redacted-local-path]`.

- [ ] **Step 5: Implement CLI wrapper**

Create `plugins/product-agent-os/scripts/run_methodology_audit.py`.

Required usage:

```powershell
python plugins\product-agent-os\scripts\run_methodology_audit.py <workspace> --json
python plugins\product-agent-os\scripts\run_methodology_audit.py <workspace> --report
```

The CLI must:

- read the workspace;
- never write into the workspace;
- print JSON for `--json`;
- print Markdown for `--report`;
- exit `2` for missing mode;
- exit `1` for invalid workspace;
- print clean JSON error for `--json` invalid workspace.

- [ ] **Step 6: Register report template**

Modify `plugins/product-agent-os/scripts/product_agent_os/templates.py` to include the report template path in the template registry if registry code covers report templates. If the registry only covers staged target-project templates, add the report template to plugin structure tests instead of staging it into target workspace by default.

- [ ] **Step 7: Run focused tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_report tests.product_agent_os.test_plugin_structure -v
```

Expected: all tests pass.

- [ ] **Step 8: Run CLI manually**

Run:

```powershell
python plugins\product-agent-os\scripts\run_methodology_audit.py plugins\product-agent-os\assets\fixtures\node-app --json
python plugins\product-agent-os\scripts\run_methodology_audit.py plugins\product-agent-os\assets\fixtures\node-app --report
```

Expected: first command prints JSON with `maturity_level`; second command prints Markdown with `Product-Agent OS Methodology Audit`.

- [ ] **Step 9: Commit report and CLI**

Run:

```powershell
git add plugins\product-agent-os\assets\templates\reports\methodology-audit-report.md plugins\product-agent-os\scripts\product_agent_os\methodology_report.py plugins\product-agent-os\scripts\run_methodology_audit.py plugins\product-agent-os\scripts\product_agent_os\templates.py tests\product_agent_os\test_methodology_report.py tests\product_agent_os\test_plugin_structure.py
git commit -m "feat: add methodology audit report and cli"
```

Expected: commit succeeds.

---

### Task 6: Add Foundation Fixture Eval Coverage

**Files:**
- Modify: `plugins/product-agent-os/scripts/run_fixture_eval.py`
- Modify: `tests/product_agent_os/test_fixture_eval_runner.py`
- Modify: `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json`

- [ ] **Step 1: Add RED fixture eval assertions**

Modify `tests/product_agent_os/test_fixture_eval_runner.py` and assert every fixture result exposes these expected checks when relevant:

```python
"methodology_catalog_contract_present"
"methodology_intelligence_contract_present"
"methodology_recommendations_prioritized"
"methodology_audit_read_only"
```

Also assert the `node-app`, `python-app`, `docs-repo`, `api-migration-repo`, `data-migration-repo`, `ai-eval-repo`, `security-sensitive-repo` and `package-release` fixtures return at least one applicable methodology domain.

- [ ] **Step 2: Run fixture tests and verify RED**

Run:

```powershell
python -m unittest tests.product_agent_os.test_fixture_eval_runner -v
```

Expected: fail because new keys are missing.

- [ ] **Step 3: Update fixture eval runner**

Modify `plugins/product-agent-os/scripts/run_fixture_eval.py`.

For each fixture result:

- call the methodology audit builder;
- add `methodology_catalog_contract_present`;
- add `methodology_intelligence_contract_present`;
- add `methodology_recommendations_prioritized`;
- add `methodology_audit_read_only`;
- include applicable methodology domain ids in the result under `methodology_domains`.

- [ ] **Step 4: Add behavioral eval case**

Modify `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` and add a case named `methodology-intelligence-read-only-first`.

The case must require:

- complexity/maturity classification;
- Delivery Map;
- recommendations;
- questions for owner;
- no target workspace writes;
- staged artifacts only after approval.

Запрещенное поведение:

- generating docs without recommendation;
- claiming readiness from file detection alone;
- requiring every methodology domain for a simple workspace;
- activating hooks, automation, CI or external writes.

- [ ] **Step 5: Run focused tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_behavioral_workflow_evals -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: tests pass; fixture eval exits `0`.

- [ ] **Step 6: Commit fixture eval foundation**

Run:

```powershell
git add plugins\product-agent-os\scripts\run_fixture_eval.py plugins\product-agent-os\assets\templates\evals\behavioral-workflows.json tests\product_agent_os\test_fixture_eval_runner.py
git commit -m "test: add methodology intelligence fixture evals"
```

Expected: commit succeeds.

---

### Task 7: Add Track 9 Backlog And Product Docs

**Files:**
- Create: `docs/sources/product-agent-os-track-9-backlog.md`
- Create: `docs/product-agent-os/methodology-intelligence.md`
- Modify: `docs/product-agent-os/index.md`
- Modify: `docs/product-agent-os/architecture.md`
- Modify: `docs/product-agent-os/behavioral-evals.md`
- Modify: `docs/sources/registry.md`
- Modify: `mkdocs.yml`
- Modify: `tools/check_docs.py`
- Test: `tests/product_agent_os/test_product_agent_os_docs.py`

- [ ] **Step 1: Add RED docs tests**

Modify `tests/product_agent_os/test_product_agent_os_docs.py` with a test named `test_track9_methodology_intelligence_docs_exist`.

The test must assert:

- `docs/product-agent-os/methodology-intelligence.md` exists;
- it contains `Source status:`;
- it contains `Inputs`, `Outputs`, `Verification`, `Risks`;
- `mkdocs.yml` contains `methodology-intelligence.md`;
- `tools/check_docs.py` requires the path.

- [ ] **Step 2: Run docs test and verify RED**

Run:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
```

Expected: fail because the docs page does not exist.

- [ ] **Step 3: Create Track 9 backlog**

Create `docs/sources/product-agent-os-track-9-backlog.md` with:

```markdown
# Product-Agent OS Track 9 Backlog

Source status: `local implementation planning`

## Track 9 Goal

## Foundation Slices

## Domain Integration Queue

## Domain Deep-Audit Log

## Cross-Domain Synthesis Backlog

## Verification Evidence

## Residual Risks
```

Fill `Domain Integration Queue` with `T9-D1` through `T9-D12` in the order from the spec. Mark all as `planned` except foundation tasks that are already implemented at this point.

- [ ] **Step 4: Create methodology intelligence docs page**

Create `docs/product-agent-os/methodology-intelligence.md` with:

```markdown
# Methodology Intelligence

Source status: `local product design + experiment`

## Inputs

## Outputs

## Read-Only First

## Delivery Map

## Methodology Recommendations

## Approval Boundary

## Verification

## Risks
```

Document:

- `maturity_level`;
- `complexity_profile`;
- Delivery Map;
- `methodology-audit-report.md`;
- `methodology-applicability.json`;
- recommendation priorities;
- questions for owner;
- staged artifact boundary.

- [ ] **Step 5: Update nav and docs checks**

Modify:

- `mkdocs.yml`: add `Methodology intelligence: product-agent-os/methodology-intelligence.md` under Product-Agent OS plugin.
- `tools/check_docs.py`: add `docs/product-agent-os/methodology-intelligence.md` to required paths.
- `docs/product-agent-os/index.md`: link to methodology intelligence.
- `docs/product-agent-os/architecture.md`: add Track 9 read-only audit flow.
- `docs/product-agent-os/behavioral-evals.md`: mention `methodology-intelligence-read-only-first`.
- `docs/sources/registry.md`: add a local Track 9 design/backlog entry.

- [ ] **Step 6: Run docs checks**

Run:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict
```

Expected: all commands exit `0`.

- [ ] **Step 7: Commit docs foundation**

Run:

```powershell
git add docs\sources\product-agent-os-track-9-backlog.md docs\product-agent-os\methodology-intelligence.md docs\product-agent-os\index.md docs\product-agent-os\architecture.md docs\product-agent-os\behavioral-evals.md docs\sources\registry.md mkdocs.yml tools\check_docs.py tests\product_agent_os\test_product_agent_os_docs.py
git commit -m "docs: add track 9 methodology intelligence docs"
```

Expected: commit succeeds.

---

### Task 8: T9-D1 Business & Product Domain Integration

**Files:**
- Source: `docs/methodologies/business-product.md`
- Modify: `plugins/product-agent-os/assets/methodology/methodology-catalog.json`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`
- Modify: `plugins/product-agent-os/assets/templates/control-plane/REQUIREMENTS.md`
- Modify: `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`
- Modify: `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`
- Modify: `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`
- Modify: `plugins/product-agent-os/assets/templates/artifact-templates/metric-spec.md`
- Modify: `plugins/product-agent-os/assets/templates/pr/release-notes.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/product-brief.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/value-proposition.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/opportunity-tree.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/experiment-plan.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/tracking-plan.md`
- Modify: lifecycle skills listed in File Structure
- Test: `tests/product_agent_os/test_methodology_catalog.py`
- Test: `tests/product_agent_os/test_methodology_audit.py`
- Test: `tests/product_agent_os/test_infrastructure_templates.py`
- Test: `tests/product_agent_os/test_lifecycle_skills.py`
- Test: `tests/product_agent_os/test_fixture_eval_runner.py`

**Deep-Audit Task Matrix:**

This matrix maps the `docs/methodologies/business-product.md` audit findings to the concrete execution steps below. The numbered steps remain the implementation checklist; this table is the traceability layer that shows where each finding lands.

| Audit finding | Plan step(s) | Implementation target |
| --- | --- | --- |
| Product hypothesis before implementation | Step 0, Step 1, Step 7, Step 8, Step 10 | `product_hypothesis_present`, audit recommendations, `requirements-author`, `implementation-planner`. |
| Target user segment and excluded users | Step 1, Step 4, Step 9 | Catalog gates, `product-brief.md`, `REQUIREMENTS.md`, `PLAN.md`. |
| Value Proposition Canvas evidence | Step 0, Step 1, Step 4, Step 9, Step 11 | `value_proposition_evidence_present`, `value-proposition.md`, fixture eval contract. |
| Opportunity must not be only a solution request | Step 1, Step 4, Step 7, Step 9 | `opportunity_not_solution_present`, `opportunity-tree.md`, audit false-positive tests. |
| Decision horizon controls required formality | Step 0, Step 1, Step 3, Step 4, Step 8, Step 9, Step 11 | `decision_horizon_present`, `decision_horizons`, `product-brief.md`, `experiment-plan.md`. |
| Business outcome, product outcome and feature traction metric are separate | Step 0, Step 1, Step 4, Step 7, Step 8, Step 9, Step 11 | `outcome_metric_level_separated`, metric-level audit questions, control-plane fields. |
| Success metric or explicit not-applicable reason | Step 1, Step 8, Step 9, Step 10 | `success_metric_present`, `metric_scope_classified`, lifecycle skill gates. |
| `metric_scope` must be `required`, `not_applicable` or `accepted_gap` | Step 0, Step 1, Step 8, Step 9, Step 10, Step 11 | `metric_scope_classified`, `REQUIREMENTS.md`, `requirements-author`, fixture eval. |
| Metric hardening for product behavior claims | Step 1, Step 7, Step 8, Step 9, Step 10 | `metric_hardening_when_product_behavior_changes`, `metric-spec.md`, risk review. |
| HEART metrics are optional UX/product quality lenses | Step 0, Step 4, Step 9 | `metric-spec.md` or `tracking-plan.md` optional fields. |
| Product analytics needs tracking plan | Step 0, Step 1, Step 4, Step 5, Step 6, Step 7, Step 8, Step 11 | `analytics_tracking_plan_present`, `tracking-plan.md`, renderer registry, audit test. |
| Qualitative feedback loop is required or accepted as a gap | Step 0, Step 1, Step 7, Step 8, Step 9 | `qualitative_feedback_loop_present`, metric hardening and post-release evidence. |
| Privacy classification for metrics | Step 1, Step 4, Step 8, Step 9 | `privacy_classification_for_metrics_present`, `metric-spec.md`, `tracking-plan.md`. |
| AI product behavior needs eval and value evidence | Step 1, Step 7, Step 8, Step 9, Step 10 | `ai_product_eval_when_ai_behavior_changes`, `EVALS.md`, `test-eval-designer`, `risk-reviewer`. |
| Post-release measurement plan | Step 1, Step 8, Step 9, Step 10 | `post_release_measurement_plan_present`, `RUNLOG.md`, `release-notes.md`, `learning-loop-maintainer`. |
| Release measurement evidence before success claims | Step 0, Step 1, Step 7, Step 8, Step 9, Step 11 | `release_measurement_evidence_present`, audit recommendation, fixture eval. |
| No-production-telemetry fallback | Step 0, Step 7, Step 8, Step 9, Step 13 | Manual, qualitative, support, customer-success or owner review evidence policy. |
| Release notes need affected users, measurement window and rollback/disable signal | Step 0, Step 9, Step 11 | `plugins/product-agent-os/assets/templates/pr/release-notes.md`, fixture eval. |
| `PLAN.md`, `EVALS.md` and `RUNLOG.md` carry outcome/eval/measurement evidence | Step 0, Step 9 | Control-plane templates. |
| Workflow promotion needs value evidence and safety boundary | Step 0, Step 1, Step 7, Step 10, Step 11 | `workflow_promotion_value_evidence_present`, `learning-loop-maintainer`, `automation-promoter`. |
| Mechanical edits should not force Business/Product methodology | Step 0, Step 3, Step 7, Step 8 | Catalog `not_applicable_when`, audit false-positive tests. |
| Backlog must record audit decisions and residual risks | Step 0, Step 13 | `docs/sources/product-agent-os-track-9-backlog.md`. |
| Verification must prove catalog, templates, lifecycle and fixture contracts | Step 2, Step 5, Step 7, Step 12 | Focused unit tests and `run_fixture_eval.py`. |

- [x] **Step 0: Record deep-audit deltas before implementation**

Do not create a new branch for this slice when the operator explicitly asks to continue on the current branch.

Modify `docs/sources/product-agent-os-track-9-backlog.md` before code implementation and record these `T9-D1` deep-audit deltas from `docs/methodologies/business-product.md`:

- `value_proposition_evidence_present` is required in addition to the original Task 8 gate list.
- `analytics_tracking_plan_present` is required when product usage data or product analytics is claimed.
- `qualitative_feedback_loop_present` is required for user research, support, sales, customer-success signal or accepted qualitative evidence gap.
- `release_measurement_evidence_present` is required before product success claims after release.
- `tracking-plan.md` is a required candidate artifact for product analytics governance.
- Severity resolution: missing `product_hypothesis_present` is `P2_recommended` for discovery-only or empty workspace audits, but becomes `P1_high_risk` or stronger when the user asks to implement, ship or release a behavior-changing slice without hypothesis, metric/gap and owner evidence.
- `decision_horizon` must be recorded as `discovery`, `MVP`, `beta`, `production` or `scale`; it determines how much formality the Product-Agent OS recommendation should require.
- `business_outcome`, `product_outcome` and `feature_traction_metric` must be separated so a local feature metric is not treated as a North Star metric.
- HEART metrics are optional UX/product quality lenses, not a mandatory full set; when used, record which of `Happiness`, `Engagement`, `Adoption`, `Retention` and `Task success` applies.
- `release-notes.md` is part of the Business/Product surface because user-facing changes need affected users, measurement window and rollback/disable signal.
- `PLAN.md`, `EVALS.md` and `RUNLOG.md` must carry outcome-driven planning, AI product eval and post-release measurement evidence, not only `REQUIREMENTS.md` and `metric-spec.md`.
- `metric_scope` must be explicit as `required`, `not_applicable` or `accepted_gap`.
- `tracking-plan.md` is required only when product usage data, analytics events, dashboards, event properties or product analytics claims exist; plain metric hardening can stay in `metric-spec.md`.
- If production telemetry does not exist, post-release measurement can use manual, qualitative, support or owner review evidence, but product success claims must remain blocked until current evidence or accepted gap exists.
- Internal workflow promotion can use engineering time saved plus verification, owner and safety boundary evidence; it does not always need an external product metric.

- [x] **Step 1: Add RED catalog test for business/product gates**

Add a test asserting `business_product` includes these gates:

```python
[
    "product_hypothesis_present",
    "target_user_segment_present",
    "value_proposition_evidence_present",
    "opportunity_not_solution_present",
    "success_metric_present",
    "metric_hardening_when_product_behavior_changes",
    "analytics_tracking_plan_present",
    "qualitative_feedback_loop_present",
    "privacy_classification_for_metrics_present",
    "ai_product_eval_when_ai_behavior_changes",
    "post_release_measurement_plan_present",
    "release_measurement_evidence_present",
    "workflow_promotion_value_evidence_present",
    "decision_horizon_present",
    "outcome_metric_level_separated",
    "metric_scope_classified",
]
```

Also assert artifacts include:

```python
[
    "product-brief.md",
    "value-proposition.md",
    "opportunity-tree.md",
    "experiment-plan.md",
    "tracking-plan.md",
    "metric-spec.md",
    "acceptance-scenarios.md",
]
```

Also assert eval fields include:

```python
[
    "product_hypothesis_contract_present",
    "target_user_segment_contract_present",
    "value_proposition_trace_present",
    "opportunity_solution_assumption_trace_present",
    "metric_hardening_contract_present",
    "analytics_tracking_plan_contract_present",
    "privacy_classification_for_metrics_present",
    "ai_behavior_eval_contract_present",
    "post_release_measurement_contract_present",
    "workflow_promotion_value_evidence_present",
    "decision_horizon_contract_present",
    "outcome_metric_level_contract_present",
    "metric_scope_contract_present",
]
```

- [x] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog.MethodologyCatalogContractTest -v
```

Expected: fail because business/product gates and artifacts are missing.

- [x] **Step 3: Add business/product catalog data**

Modify `methodology-catalog.json` domain `business_product` with:

- applies_when: behavior-changing feature, product-labeled request, MVP, release, AI behavior change, metric claim;
- not_applicable_when: mechanical formatting, typo-only docs edit, dependency pin without behavior impact;
- maturity_impact: `baseline`, `team`, `production`;
- complexity_impact: `standard`, `high_risk` when AI/product promise/measurement claims exist;
- track8_scenarios: `greenfield_idea`, `release_packaging`, `ai_eval_regression`, `standard_feature`;
- decision_horizons: `discovery`, `MVP`, `beta`, `production`, `scale`;
- gates and artifacts from Step 1;
- eval_fields from Step 1;
- overlaps: quality eval evidence, delivery measurement, requirements acceptance scenarios, AI behavior evals, data/privacy classification and workflow promotion.

- [x] **Step 4: Add artifact templates**

Create:

- `product-brief.md`: user/segment, problem/opportunity, decision horizon, business outcome, product outcome, feature traction metric, non-goals, assumptions, evidence gaps, owner.
- `value-proposition.md`: jobs, pains, gains, pain relievers, gain creators, evidence source, owner.
- `opportunity-tree.md`: desired outcome, opportunities, candidate solutions, riskiest assumptions, tests, decision.
- `experiment-plan.md`: decision horizon, hypothesis, smallest build, measure plan, learning threshold, pivot/persevere rule, owner, review date.
- `tracking-plan.md`: event name, business question, properties, property types, taxonomy/naming convention, data owner, instrumentation owner, validation command/report, dashboard/report, privacy classification, retention and review owner.

Every template must include `Source status:`, owner, evidence, accepted gap and residual risk fields. `metric-spec.md` or `tracking-plan.md` must mention HEART metrics as optional lenses: `Happiness`, `Engagement`, `Adoption`, `Retention` and `Task success`.

- [x] **Step 5: Add RED renderer/template tests**

Modify `tests/product_agent_os/test_infrastructure_templates.py` and assert the renderer registry includes these targets exactly once:

```python
[
    ".codex/artifact-templates/product-brief.md",
    ".codex/artifact-templates/value-proposition.md",
    ".codex/artifact-templates/opportunity-tree.md",
    ".codex/artifact-templates/experiment-plan.md",
    ".codex/artifact-templates/tracking-plan.md",
]
```

Also add a focused template-content test that checks each new template contains:

```python
[
    "Source status:",
    "Owner",
    "Evidence",
    "Accepted Gap",
    "Residual Risk",
]
```

Run:

```powershell
python -m unittest tests.product_agent_os.test_infrastructure_templates.InfrastructureTemplateTest -v
```

Expected: fail before the templates and registry entries exist.

- [x] **Step 6: Register templates**

Modify `plugins/product-agent-os/scripts/product_agent_os/templates.py` so the renderer can stage the new artifact templates under `.codex/artifact-templates/`.

- [x] **Step 7: Add RED audit tests**

Modify `tests/product_agent_os/test_methodology_audit.py` with focused tests that assert:

- `build_methodology_audit(..., intent_hint="ship MVP product metric experiment")` marks `business_product` as applicable.
- product implementation or release intent without product hypothesis produces a `business_product` recommendation for `product_hypothesis_present` with `P1_high_risk` or stronger.
- discovery-only or empty workspace MVP intent can use `P2_recommended` for `product_hypothesis_present`.
- metric claim without counter-metric, guardrail, qualitative review or privacy classification produces `metric_hardening_when_product_behavior_changes` with `P1_high_risk`.
- AI behavior change produces `ai_product_eval_when_ai_behavior_changes` with `P1_high_risk`.
- product analytics or usage data claim produces `analytics_tracking_plan_present` and artifact `tracking-plan.md`.
- product success claim after release without actual metrics, eval result, user feedback or accepted evidence gap produces `release_measurement_evidence_present`.
- North Star or product success language for a small isolated slice records `outcome_metric_level_separated` and asks whether the metric is business outcome, product outcome or feature traction.
- intent without telemetry can still recommend manual/qualitative/support evidence, but must not claim product success from planned measurement alone.
- workflow promotion intent without product metric can satisfy `workflow_promotion_value_evidence_present` with engineering time saved, verification, owner and safety boundary evidence.
- typo-only docs edit, formatting-only edit and dependency pin without behavior impact keep `business_product` not applicable or `not_applicable`.

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_audit.MethodologyAuditContractTest -v
```

Expected: fail before audit recommendations and false-positive rules are implemented.

- [x] **Step 8: Add audit recommendations**

Modify `methodology_audit.py`:

- product/MVP/value/metric intent triggers `business_product`;
- missing product hypothesis creates `P2_recommended` for discovery-only or empty workspace audits;
- missing product hypothesis creates `P1_high_risk` or stronger for explicit implementation, ship or release behavior-changing intent;
- metric claim without guardrails creates `P1_high_risk`;
- AI behavior change creates `P1_high_risk` for `ai_product_eval_when_ai_behavior_changes`.
- product usage data or analytics claims without event taxonomy, properties, owner, validation plan and privacy classification create `P1_high_risk` for `analytics_tracking_plan_present`.
- missing qualitative feedback loop creates `P2_recommended` unless the success claim relies only on a proxy metric, where it remains part of `P1_high_risk` metric hardening.
- product success claim after release without actual metrics, eval result, user feedback or explicit evidence gap creates `P1_high_risk` for `release_measurement_evidence_present`.
- missing decision horizon creates `P2_recommended` for `decision_horizon_present`.
- North Star wording on a local feature metric creates `P2_recommended` for `outcome_metric_level_separated`.
- product metric work without `metric_scope` creates `P1_high_risk` for `metric_scope_classified` when implementation/release intent is present and `P2_recommended` for discovery-only intent.
- no-production-telemetry cases should recommend manual, qualitative, support or owner review evidence as acceptable post-release measurement substitutes, while still forbidding success claims without current evidence or an accepted gap.

- [x] **Step 9: Update control-plane, release and metric templates**

Modify `plugins/product-agent-os/assets/templates/control-plane/REQUIREMENTS.md`, `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`, `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `plugins/product-agent-os/assets/templates/pr/release-notes.md` and `plugins/product-agent-os/assets/templates/artifact-templates/metric-spec.md` so behavior-changing work captures:

- target user segment and explicitly excluded users;
- opportunity/problem statement that is not just a solution request;
- decision horizon: `discovery | MVP | beta | production | scale`;
- business outcome, product outcome and feature traction metric as separate fields;
- `metric_scope`: `required | not_applicable | accepted_gap`;
- value proposition evidence or accepted evidence gap;
- primary metric, input metric, counter-metric, proxy metric risk and guardrail;
- optional HEART metrics categories when UX/product quality metrics apply;
- qualitative feedback loop;
- privacy classification, retention and data minimization for metrics;
- analytics tracking plan status when product usage data is claimed;
- post-release measurement plan and release measurement evidence.
- no-production-telemetry fallback: manual, qualitative, support, customer-success, owner review or explicit accepted gap evidence;
- release notes fields for affected users, measurement window and rollback/disable signal.

- [x] **Step 10: Update lifecycle skills**

Add concise wording:

- `requirements-author`: product hypothesis before requirements for behavior-changing work.
- `test-eval-designer`: product behavior claims need metric/eval evidence.
- `risk-reviewer`: proxy metric and AI product value claims need counter-metric or accepted gap.
- `learning-loop-maintainer`: post-release measurement feeds workflow promotion.
- `implementation-planner`: behavior-changing implementation must not proceed when product hypothesis, acceptance scenario, metric/gap or owner are missing.
- `automation-promoter`: workflow promotion needs manual stability, value evidence, owner, verification and safety boundary; internal workflows may use engineering time saved when external product metrics are not applicable.

Add or extend lifecycle skill tests in `tests/product_agent_os/test_lifecycle_skills.py` so these terms are enforced:

```python
[
    "product_hypothesis_present",
    "value_proposition_evidence_present",
    "analytics_tracking_plan_present",
    "qualitative_feedback_loop_present",
    "release_measurement_evidence_present",
    "decision_horizon_present",
    "outcome_metric_level_separated",
    "metric_scope_classified",
    "tracking-plan.md",
    "engineering time saved",
]
```

- [x] **Step 11: Add fixture eval check**

Modify `plugins/product-agent-os/scripts/run_fixture_eval.py` and `tests/product_agent_os/test_fixture_eval_runner.py` with a check named `business_product_contract_present`.

The check must verify catalog, templates and lifecycle text contain the T9-D1 gates and artifacts, including:

```python
[
    "product_hypothesis_present",
    "value_proposition_evidence_present",
    "analytics_tracking_plan_present",
    "qualitative_feedback_loop_present",
    "release_measurement_evidence_present",
    "decision_horizon_present",
    "outcome_metric_level_separated",
    "metric_scope_classified",
    "tracking-plan.md",
    "release-notes.md",
]
```

Keep the fixture eval read-only and do not require every simple workspace to apply the business/product domain.

- [x] **Step 12: Run focused verification**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: all commands exit `0`; renderer file count increases by 5 registered artifact templates.

- [x] **Step 13: Update Track 9 backlog**

Modify `docs/sources/product-agent-os-track-9-backlog.md`:

- mark `T9-D1` as `done`;
- record gates added;
- record templates added;
- record verification evidence;
- record overlaps for synthesis;
- record the severity resolution for `product_hypothesis_present`.
- record decision horizon, outcome/metric split, telemetry fallback and internal workflow promotion policy.

- [x] **Step 14: Commit T9-D1**

Run:

```powershell
git add plugins\product-agent-os docs\sources\product-agent-os-track-9-backlog.md tests\product_agent_os
git commit -m "feat: integrate business product methodology"
```

Expected: commit succeeds.

---

### Task 9: T9-D2 Requirements & Domain Integration

**Files:**
- Source: `docs/methodologies/requirements-domain.md`
- Modify: `methodology-catalog.json`
- Modify: `methodology_audit.py`
- Modify: `domain-modeling.md`, `acceptance-scenarios.md`, generated control-plane templates
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/requirement-registry.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/stakeholder-owner-map.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/story-slice-map.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/requirements-traceability-matrix.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/business-rules.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/example-map.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/requirement-change-impact.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/domain-review-record.md`
- Tests: methodology catalog, audit, renderer, fixture eval

**Deep-Audit Task Matrix:**

This matrix keeps every audited requirement visible as its own task row. The detailed checklist below remains the executable step plan, so several matrix rows can map to the same implementation step.

| ID | Task | Existing step mapping | Output |
| --- | --- | --- | --- |
| `T9-D2-0` | Record deep-audit deltas from `docs/methodologies/requirements-domain.md` before implementation. | Step 0 | Track 9 plan/backlog records missing gates, artifacts, false-positive risks and residual risks. |
| `T9-D2-1` | Add RED catalog tests for the complete `requirements_domain` contract. | Step 1, Step 2 | Catalog tests cover gates, artifacts, eval fields, applies/not-applicable rules and overlaps. |
| `T9-D2-2` | Add `requirements_domain` catalog data. | Step 3 | `methodology-catalog.json` contains applies/not-applicable rules, maturity/complexity impact, artifacts, gates and eval fields. |
| `T9-D2-3` | Represent requirement taxonomy. | Step 0, Step 1, Step 3, Step 4 | Functional, non-functional, compliance, operational, AI behavior, data/privacy and release/rollback requirements are explicit when relevant. |
| `T9-D2-4` | Add `requirement_quality_present`. | Step 0, Step 1, Step 3, Step 4, Step 5 | Atomicity, clarity, testability, feasibility, traceability, source and owner become a first-class gate/eval field. |
| `T9-D2-5` | Add stable requirement IDs and registry. | Step 1, Step 3, Step 4, Step 5 | `requirement_ids_present` and `requirement-registry.md` cover ID, status, source, owner and linked artifacts. |
| `T9-D2-6` | Add stakeholder/owner map. | Step 0, Step 1, Step 4, Step 5, Step 6 | `stakeholder-owner-map.md` captures stakeholder, domain expert, technical owner, decision authority and escalation path. |
| `T9-D2-7` | Add story slicing and MVP/deferred slice map. | Step 0, Step 1, Step 4, Step 5 | `story-slice-map.md` covers value slice, risk slice, MVP boundary, deferred slices, non-goals and scenario links. |
| `T9-D2-8` | Strengthen acceptance scenarios and declarative scenario quality. | Step 1, Step 4, Step 5, Step 6 | `acceptance-scenarios.md` keeps actor/context/trigger/outcome/evidence and rejects UI selectors, DB internals, function names and test harness details. |
| `T9-D2-9` | Add requirements traceability matrix. | Step 1, Step 4, Step 5, Step 6 | `requirements-traceability-matrix.md` maps requirement -> scenario -> implementation -> check/eval -> evidence owner -> release/docs evidence. |
| `T9-D2-10` | Add business rules artifact and gate. | Step 1, Step 4, Step 5, Step 6 | `business-rules.md` records rule, source, owner, enforcement layer, exceptions, failure mode and tests/evals. |
| `T9-D2-11` | Add non-goals and constraints traceability. | Step 0, Step 1, Step 3, Step 4, Step 5 | `non_goals_constraints_present` and `constraints_traceability_present` cover compliance, privacy, security, operational, performance, platform, accessibility, retention, localization, cost, rollout and rollback. |
| `T9-D2-12` | Add open questions with owner and next action. | Step 1, Step 4, Step 5 | `open_questions_recorded` and `open_questions_contract_present` prevent unresolved requirements from staying in chat. |
| `T9-D2-13` | Add Example Mapping for unclear stories. | Step 1, Step 4, Step 5 | `example-map.md` captures story -> rules -> examples -> questions, deferred slices, owner and next action. |
| `T9-D2-14` | Add domain discovery workshop evidence. | Step 0, Step 1, Step 5 | Complex workflow/cross-silo/overloaded-language work records EventStorming, Domain Storytelling, interview or accepted-gap evidence. |
| `T9-D2-15` | Preserve conditional DDD without duplicating Track 8. | Step 0, Step 1, Step 3, Step 7 | `domain_model_when_complex_domain`, `bounded_context_architecture_boundary_trace` and `ubiquitous_language_traceability` remain conditional and do not force DDD on simple CRUD/MVP. |
| `T9-D2-16` | Add invariants and failure modes. | Step 1, Step 4, Step 5, Step 6 | Domain state transitions record invariant, invalid transition, enforcement layer, failure behavior and test/eval evidence. |
| `T9-D2-17` | Add domain event contract requirements. | Step 1, Step 4, Step 5, Step 6 | Cross-boundary events record meaning, producer, consumers, schema link, ordering/idempotency and privacy classification. |
| `T9-D2-18` | Add API/UI/data traceability. | Step 1, Step 4, Step 5, Step 6 | Requirement/domain terms map to API/event/schema, UI label/copy/error/accessibility name, data field/schema, code/test and owner. |
| `T9-D2-19` | Add domain expert / owner review. | Step 1, Step 4, Step 5, Step 6 | `domain-review-record.md` covers business-critical, compliance, finance/legal and AI-generated domain claims, conflicts and accepted gaps. |
| `T9-D2-20` | Add requirement change impact review. | Step 1, Step 4, Step 5, Step 6 | `requirement-change-impact.md` records affected tests/evals, API, DB, UI, docs, rollout, rollback and approval boundary after planning changes. |
| `T9-D2-21` | Add accepted gap policy. | Step 0, Step 1, Step 3, Step 4, Step 5, Step 6 | `accepted_gap_recorded` requires owner, reason, scope, review date, downstream risk and follow-up condition. |
| `T9-D2-22` | Add requirements evidence before implementation. | Step 1, Step 5, Step 6, Step 8 | `requirements_evidence_before_implementation` blocks build claims when requirements/scenarios/domain gates are missing and no accepted gap exists. |
| `T9-D2-23` | Update lifecycle skills including `docs-maintainer`. | Step 6 | `requirements-author`, `implementation-planner`, `agent-team-designer`, `test-eval-designer`, `risk-reviewer`, `docs-maintainer` enforce the domain contract. |
| `T9-D2-24` | Add fixture eval contract coverage. | Step 8 | `requirements_domain_contract_present` checks catalog, templates, lifecycle wording and fixture output. |
| `T9-D2-25` | Add false-positive coverage. | Step 7 | Docs typo, formatting-only, dependency metadata and simple CRUD with `src/domain/` do not force DDD or heavy requirements ceremony. |
| `T9-D2-26` | Add unsupported-claim negative tests. | Step 7 | BDD replaces testing, Gherkin is mandatory, story template is complete requirements, glossary is ubiquitous language and OpenAPI is requirements source of truth are rejected. |
| `T9-D2-27` | Update cross-domain synthesis backlog. | Step 0 | API/UI/data traceability, stakeholder/owner mapping, story slicing, domain events, accepted gaps, owner review and change impact are queued for later synthesis. |
| `T9-D2-28` | Run verification and commit. | Step 8, Step 9 | Focused tests, fixture eval, docs check and commit evidence are recorded. |

- [x] **Step 0: Record deep-audit deltas before implementation**

Modify `docs/sources/product-agent-os-track-9-backlog.md` before code implementation and record these `T9-D2` deep-audit deltas from `docs/methodologies/requirements-domain.md`:

- Current Track 8 already covers acceptance scenarios, conditional DDD, bounded-context-to-architecture traceability, ubiquitous-language traceability and simple CRUD / simple MVP false-positive protection; `T9-D2` must extend, not duplicate, those gates.
- Requirement taxonomy must be explicit when relevant: functional, non-functional, compliance, operational, AI behavior, data/privacy and release/rollback.
- Requirement quality criteria must be represented: atomicity, clarity, testability, feasibility, traceability, source and owner.
- Stable requirement IDs are needed for multi-slice, regulatory, risky or long-lived work.
- Requirement registry needs status, owner, source and linked artifacts.
- Stakeholder/owner map is a first-class Requirements & Domain artifact because source-backed domain meaning and business rules need accountable reviewers.
- User story and story slicing evidence must preserve value slice, MVP boundary, deferred slices, risk and non-goals; a story title alone is not a requirement.
- Business rules need source, owner, enforcement layer, exceptions and failure behavior.
- Example Mapping is needed when stories are unclear, large or disputed: story -> rules -> examples -> questions.
- Domain discovery workshop evidence is needed for complex workflow, cross-silo process or overloaded domain language.
- `requirement_quality_present` must cover atomicity, clarity, testability, feasibility, traceability, source and owner instead of being hidden inside scope.
- Constraint evidence must cover compliance, privacy, security, operational, performance, platform, accessibility, data retention, localization, cost, rollout and rollback when relevant.
- Acceptance scenarios must be declarative: no UI selectors, database internals, function names or test harness details in business-facing scenarios.
- Domain events crossing boundaries need meaning, producer, consumers, schema link, ordering/idempotency assumptions and privacy classification.
- Invariants and failure modes are required when domain state transitions matter.
- API/UI/data traceability is distinct from DDD traceability: requirement/domain term -> API/event/schema/UI/data/code/test/eval.
- Domain expert review is required for business-critical, compliance, finance/legal or AI-generated domain claims.
- Requirement change impact review is required when requirements/domain rules change after planning: tests/evals, API, DB, UI, docs, rollout and rollback.
- Accepted gaps are valid only with owner, reason, scope, review date, downstream risk and follow-up condition.
- `docs-maintainer` owns requirement IDs, source registry, glossary/ubiquitous-language docs and traceability docs after the requirements packet exists.
- Unsupported claims must be rejected: BDD replaces testing, Gherkin is mandatory, a user-story template is a complete requirement, a glossary is ubiquitous language, OpenAPI is requirements source of truth.

- [x] **Step 1: Add RED test for requirements/domain gates**

Assert `requirements_domain` gates include:

```python
[
    "requirements_scope_present",
    "requirements_owner_present",
    "requirement_quality_present",
    "requirement_ids_present",
    "acceptance_scenarios_when_behavior_changes",
    "declarative_acceptance_scenarios_present",
    "requirements_traceability_present",
    "business_rules_present",
    "non_goals_constraints_present",
    "constraints_traceability_present",
    "open_questions_recorded",
    "example_mapping_when_unclear_story",
    "domain_discovery_workshop_when_complex_process",
    "domain_model_when_complex_domain",
    "bounded_context_architecture_boundary_trace",
    "ubiquitous_language_traceability",
    "invariants_and_failure_modes_present",
    "domain_event_contracts_present",
    "api_ui_data_traceability_present",
    "domain_expert_review_present",
    "requirement_change_impact_review_present",
    "accepted_gap_recorded",
    "requirements_evidence_before_implementation",
]
```

Also assert artifacts include:

```python
[
    "requirement-registry.md",
    "stakeholder-owner-map.md",
    "story-slice-map.md",
    "acceptance-scenarios.md",
    "requirements-traceability-matrix.md",
    "business-rules.md",
    "example-map.md",
    "domain-modeling.md",
    "requirement-change-impact.md",
    "domain-review-record.md",
]
```

Also assert eval fields include:

```python
[
    "requirements_scope_contract_present",
    "requirements_owner_contract_present",
    "requirement_quality_contract_present",
    "requirement_ids_contract_present",
    "acceptance_scenarios_contract_present",
    "declarative_scenario_quality_contract_present",
    "requirements_traceability_contract_present",
    "business_rules_contract_present",
    "non_goals_constraints_contract_present",
    "constraints_traceability_contract_present",
    "open_questions_contract_present",
    "stakeholder_owner_map_contract_present",
    "story_slice_map_contract_present",
    "example_mapping_contract_present",
    "domain_discovery_contract_present",
    "domain_model_contract_present",
    "bounded_context_trace_contract_present",
    "ubiquitous_language_traceability_contract_present",
    "invariants_failure_modes_contract_present",
    "domain_event_contracts_present",
    "api_ui_data_traceability_contract_present",
    "domain_expert_review_contract_present",
    "requirement_change_impact_contract_present",
    "accepted_gap_contract_present",
    "requirements_evidence_before_implementation_contract_present",
    "unsupported_claims_rejected_contract_present",
]
```

- [x] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing requirements/domain gates.

- [x] **Step 3: Add catalog data and false-positive rules**

Rules:

- applies for behavior changes, domain terms, workflows, API/UI/data changes, AI behavior changes;
- not applicable for docs typo, formatting-only, pure dependency metadata without behavior impact;
- do not force DDD for simple CRUD/MVP when accepted gap exists;
- overloaded domain terms become owner questions, not verified evidence.
- requirements scope/owner/scenarios apply to behavior-changing work even when DDD is not applicable;
- requirement quality applies to non-trivial product/system work and must not be treated as satisfied by a story title alone;
- requirement IDs apply to multi-slice, regulatory, risky, long-lived or public-contract work;
- constraints traceability applies when compliance, privacy, security, operational, performance, platform, accessibility, retention, localization, cost, rollout or rollback constraints are present;
- declarative scenario quality applies when business-facing scenarios contain UI selectors, database internals, function names or test harness details;
- stakeholder/owner mapping applies when domain meaning, business rules or owner review is required;
- story-slice mapping applies when user stories, MVP boundary, value/risk slices or deferred slices are part of scope;
- domain expert review applies to business-critical, compliance, finance/legal and AI-generated domain claims;
- requirement change impact applies when requirements/domain rules change after planning.
- unsupported claims are never accepted as methodology evidence: BDD replaces testing, Gherkin is mandatory, a user-story template is complete requirements, a glossary is ubiquitous language, OpenAPI is requirements source of truth.

- [x] **Step 4: Add and register templates**

Create templates:

- `requirement-registry.md`;
- `stakeholder-owner-map.md`;
- `story-slice-map.md`;
- `requirements-traceability-matrix.md`;
- `business-rules.md`;
- `example-map.md`;
- `requirement-change-impact.md`;
- `domain-review-record.md`.

Each template must include source, owner, linked requirements, evidence owner, accepted gap and residual risk.

Template-specific fields:

- `requirement-registry.md`: requirement ID, type, status, source, owner, scope, linked scenarios, linked tests/evals, linked contracts/docs and change impact.
- `stakeholder-owner-map.md`: stakeholder, domain expert, technical owner, review responsibility, decision authority, escalation path, unavailable owner gap and review cadence.
- `story-slice-map.md`: user story, value slice, risk slice, MVP boundary, deferred slices, non-goals, owner and acceptance scenario links.
- `requirements-traceability-matrix.md`: requirement -> scenario -> implementation -> check/eval -> evidence owner -> release/docs evidence.
- `business-rules.md`: rule, source, owner, enforcement layer, exceptions, failure mode, affected requirement IDs and tests/evals.
- `example-map.md`: story, rules, examples, questions, deferred slices, owner and next action.
- `requirement-change-impact.md`: changed requirement/rule, affected tests/evals, API, DB, UI, docs, rollout, rollback and approval boundary.
- `domain-review-record.md`: domain expert/owner review, AI-generated claim status, unresolved conflicts, accepted gaps, downstream risk and follow-up owner.

- [x] **Step 5: Extend audit recommendations**

Add recommendations:

- behavior intent with missing acceptance scenarios -> `P0_blocker`;
- non-trivial product/system work with missing `requirement_quality_present` -> `P1_high_risk`;
- behavior-facing scenario with UI selectors, database internals, function names or test harness details -> `P1_high_risk`;
- domain/API/UI/data crossing without traceability -> `P1_high_risk`;
- complex domain without domain model or accepted gap -> `P1_high_risk`;
- changed requirement after planning -> `P1_high_risk` for impact review.
- compliance, privacy, security, operational, performance, platform, accessibility, retention, localization, cost, rollout or rollback constraints without traceability -> `P1_high_risk`;
- multi-slice, regulatory, risky or long-lived work without stable requirement IDs -> `P1_high_risk`;
- stakeholder/process/value ambiguity without `stakeholder-owner-map.md` -> `P2_recommended`;
- user story, MVP boundary or deferred slice work without `story-slice-map.md` -> `P2_recommended`;
- unclear/large/disputed story without Example Mapping -> `P2_recommended`;
- business rule without source, owner, enforcement layer or exception policy -> `P1_high_risk`;
- domain event crossing a boundary without meaning, schema, producer/consumer, ordering/idempotency or privacy classification -> `P1_high_risk`;
- business-critical, compliance, finance/legal or AI-generated domain claim without owner/domain expert review -> `P1_high_risk`;
- accepted gap without owner, reason, scope, review date, downstream risk or follow-up condition -> `P1_high_risk`.
- unsupported methodology claim appears as evidence -> `P1_high_risk` and owner question.

- [x] **Step 6: Update lifecycle skills**

Update:

- `requirements-author`: requirement quality and domain artifacts.
- `implementation-planner`: block implementation when behavior scenarios or traceability are missing.
- `agent-team-designer`: use bounded contexts for ownership split.
- `test-eval-designer`: map scenarios to tests/evals.
- `risk-reviewer`: check domain claims and accepted gaps.
- `docs-maintainer`: keep requirement IDs, source registry, glossary/ubiquitous-language pages and traceability docs aligned.

Each skill must mention `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, `domain-review-record.md`, `requirements_traceability_present`, `requirement_quality_present`, `constraints_traceability_present`, `declarative_acceptance_scenarios_present`, `business_rules_present`, `domain_expert_review_present`, `requirement_change_impact_review_present` and `accepted_gap_recorded`.

- [x] **Step 7: Add false-positive and unsupported-claim fixtures**

Create or extend a fixture for simple CRUD that has `src/domain/` but no complex domain indicators. Assert DDD remains `not_applicable` or accepted gap, not `applicable_missing`.

Add negative coverage for unsupported methodology claims:

- "BDD replaces testing" must not satisfy test/eval evidence.
- "Gherkin is mandatory" must not force Gherkin when equivalent behavior tables preserve actor, context, trigger, observable outcome and evidence.
- "A user story template is a complete requirement" must not satisfy `requirements_scope_present`, `requirement_quality_present` or `acceptance_scenarios_when_behavior_changes`.
- "A glossary is ubiquitous language" must not satisfy `ubiquitous_language_traceability`.
- "OpenAPI is the requirements source of truth" must not satisfy business intent, acceptance scenarios or requirements traceability by itself.

- [x] **Step 8: Run verification**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_fixture_eval_runner -v
python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python tools\check_docs.py
```

Expected: all commands exit `0`.

- [x] **Step 9: Commit T9-D2**

Run:

```powershell
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md docs\superpowers\plans\2026-05-25-track-9-methodology-intelligence.md
git commit -m "feat: integrate requirements domain methodology"
```

Expected: commit succeeds.

---

### Task 10: T9-D3 Solution Architecture Integration

**Files:**
- Source: `docs/methodologies/solution-architecture.md`
- Modify: catalog, audit, `architecture-overview.md`, `adr.md`
- Create: `architecture-review-record.md`
- Create: `architecture-fitness-functions.md`
- Create: `trust-boundary-map.md`
- Create: `architecture-docs-tooling-decision.md`

Deep-audit update from `docs/methodologies/solution-architecture.md` and `docs/sources/methodology-research/solution-architecture.md`:

- The compact task list below must use the full Solution Architecture gate set from the methodology source, not only the initial subset.
- Additional gates required before implementation: `bounded_context_architecture_boundary_trace`, `adr_for_architecture_decision`, `observability_architecture_present`, and `migration_rollback_path_present`.
- Unsupported claims must be rejected as evidence: architecture equals diagrams, rendered diagram proves correctness, C4 code diagrams are always required, ADR is bureaucracy, Well-Architected review proves quality, architecture-as-code is always required, and AI can design architecture from chat alone.
- Template scope for this slice is intentionally four new artifacts plus extensions to `architecture-overview.md` and `adr.md`; broader candidate artifacts such as `boundary-responsibility-map.md`, `quality-attribute-scenarios.md`, `architecture-tradeoff-record.md`, `dependency-rules.md`, `integration-catalog.md`, and `runtime-topology.md` must either be mapped to existing artifacts in this slice or recorded in the Track 9 backlog with an explicit defer reason.
- Architecture-as-code, C4 detail level, cloud Well-Architected review, and docs portal/tooling are conditional recommendations, not universal gates. Tests must preserve `not_applicable` or accepted-gap behavior for docs-light prototypes, non-cloud work, and architecture notes that do not need rendered/diffable diagrams.

Repeat-review additions to preserve during implementation:

- Catalog eval fields must be explicit and stable: `solution_architecture_scope_contract_present`, `architecture_context_view_contract_present`, `architecture_boundary_contract_present`, `boundary_owner_contract_present`, `domain_architecture_trace_contract_present`, `public_contract_trace_contract_present`, `data_ownership_boundary_contract_present`, `trust_boundary_review_contract_present`, `quality_attribute_scenarios_contract_present`, `architecture_decision_record_contract_present`, `runtime_observability_contract_present`, `diagram_render_check_contract_present`, `architecture_fitness_function_contract_present`, `migration_rollback_contract_present`, `architecture_docs_lifecycle_contract_present`, `accepted_gap_contract_present`, and `unsupported_architecture_claims_rejected_contract_present`.
- Recommendation artifact mapping must be tested, not inferred: architecture scope/context/container -> `architecture-overview.md`; owner and accepted gaps -> `architecture-review-record.md`; public contracts -> `api-contract-review.md`; data ownership -> `database-dictionary.md`; trust boundaries -> `trust-boundary-map.md` and `security-risk-review.md`; ADR/tradeoffs -> `adr.md`; runtime topology and rollback -> `architecture-overview.md` and `migration-plan.md`; observability, dependency rules and fitness functions -> `architecture-fitness-functions.md`; docs-as-code/render checks -> `architecture-docs-tooling-decision.md`.
- Existing architecture templates strengthened in this slice must also meet the current artifact operating contract: `Source status:`, owner, accepted gap, residual risk, evidence, verification, rollback or no-rollback rationale, and no secrets/private data guidance.

#### T9-D3 Task Matrix

| ID | Task | Primary files | Критерии приемки | Verification |
| --- | --- | --- | --- | --- |
| `T9-D3-M0` | Refresh plan/backlog before implementation | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, `docs/sources/product-agent-os-track-9-backlog.md` | Full source audit deltas are recorded: four additional gates, unsupported claims, template scope, deferred candidate artifacts, false-positive risks, exact eval fields, recommendation artifact mapping, and verification commands. | `python tools\check_docs.py` |
| `T9-D3-M1` | Add RED catalog contract for `solution_architecture` | `tests/product_agent_os/test_methodology_catalog.py` | Test asserts full gate set, artifact list, explicit eval field names from repeat-review additions, applicability, false-positive routing, maturity/complexity impact and overlaps. | `python -m unittest tests.product_agent_os.test_methodology_catalog -v` fails before catalog implementation on missing architecture gates or eval fields. |
| `T9-D3-M2` | Add RED audit recommendation coverage | `tests/product_agent_os/test_methodology_audit.py` | Tests cover multi-surface project without architecture overview, public contract/data boundary without owner, diagram without render check, boundary drift, ADR trigger, observability, migration rollback, accepted-gap shape, recommendation gate -> artifact mapping, unsupported claims and typo/format/docs-only false positives. | `python -m unittest tests.product_agent_os.test_methodology_audit -v` fails before audit implementation on missing architecture recommendations. |
| `T9-D3-M3` | Add RED template, lifecycle and fixture checks | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_lifecycle_skills.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | Tests require four new templates, renderer registration, `solution_architecture_contract_present`, lifecycle skill wording for architecture boundary/owner/ADR/render/runtime/rollback gates, and renderer file count increase by four files from the current T9-D2 baseline. | `python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_fixture_eval_runner -v` fails before templates and eval check exist. |
| `T9-D3-M4` | Fill `solution_architecture` catalog data | `plugins/product-agent-os/assets/methodology/methodology-catalog.json` | Domain records applies/not-applicable rules, Track 8 scenarios, artifacts, all gates, explicit eval fields and overlaps for requirements, API, data, security, backend, delivery, AI and agent ownership. | Focused catalog test passes for `solution_architecture`. |
| `T9-D3-M5` | Implement read-only architecture audit recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py` | Audit emits prioritized recommendations for architecture overview, boundary owner, public contract trace, data ownership, ADR, quality attributes, trust boundary, runtime topology, observability, migration rollback, render check and fitness functions; recommendation packets use the explicit artifact mapping; false-positive intents stay `not_applicable`. | Focused audit tests pass and recommendation packets keep the stable shape. |
| `T9-D3-M6` | Add and register architecture artifact templates | `plugins/product-agent-os/assets/templates/artifact-templates/architecture-review-record.md`, `plugins/product-agent-os/assets/templates/artifact-templates/architecture-fitness-functions.md`, `plugins/product-agent-os/assets/templates/artifact-templates/trust-boundary-map.md`, `plugins/product-agent-os/assets/templates/artifact-templates/architecture-docs-tooling-decision.md`, `plugins/product-agent-os/scripts/product_agent_os/templates.py` | Templates include `Source status:`, owner, evidence, accepted gap, residual risk, approval boundary, verification and no secrets/private data guidance; renderer target paths are `.codex/artifact-templates/<name>`. | Infrastructure template tests pass and rendered templates have no unresolved substitutions. |
| `T9-D3-M7` | Strengthen existing architecture templates | `plugins/product-agent-os/assets/templates/artifact-templates/architecture-overview.md`, `plugins/product-agent-os/assets/templates/artifact-templates/adr.md` | `architecture-overview.md` covers stakeholders/concerns, architecture question, C4 context/container, boundary responsibility, dependency rules, public contract, data ownership, trust boundary, runtime topology, observability, quality scenarios, render check and owner review. `adr.md` covers ADR trigger, options, tradeoff, verification, rollback and accepted gap. Both templates include `Source status:`, owner, residual risk, evidence, accepted gap, rollback or no-rollback rationale, and no secrets/private data guidance. | Infrastructure template tests pass for required architecture terms and current artifact operating contract. |
| `T9-D3-M8` | Route Solution Architecture through lifecycle skills | `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `plugins/product-agent-os/skills/requirements-author/SKILL.md`, `plugins/product-agent-os/skills/implementation-planner/SKILL.md`, `plugins/product-agent-os/skills/agent-team-designer/SKILL.md`, `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`, `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`, `plugins/product-agent-os/skills/docs-maintainer/SKILL.md` | Skills require architecture boundary per non-trivial slice, owner evidence, ADR for significant decisions, C4/arc42 only when applicable, render/build evidence, runtime/observability/rollback evidence, and boundary-to-agent ownership for parallel work. | Lifecycle skill tests pass for architecture methodology wording. |
| `T9-D3-M9` | Add fixture eval contract | `plugins/product-agent-os/scripts/run_fixture_eval.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | `solution_architecture_contract_present` validates catalog gates, artifacts, eval fields, templates and lifecycle skill coverage. `python-app` expected checks include the new contract. | `python plugins\product-agent-os\scripts\run_fixture_eval.py` exits `0` after implementation. |
| `T9-D3-M10` | Sync docs and control-plane evidence | `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `docs/sources/product-agent-os-track-9-backlog.md`, `docs/product-agent-os/methodology-intelligence.md`, `docs/product-agent-os/behavioral-evals.md`, Product-Agent OS README/docs only when behavior is user-facing | Current state records `T9-D3` completion, RED/GREEN evidence, renderer file count delta, deferred candidate artifact rationale, residual risks and next action `T9-D4`. Source registry is updated only if new source-backed claims are added outside existing source entries. | Full verification commands below pass; `git diff --check` exits `0`. Run strict MkDocs only if navigation, Mermaid diagrams, Markdown extensions, MkDocs config or Product-Agent OS docs navigation changed. |

- [x] **Step 1: Add RED test for architecture gates**

Assert `solution_architecture` gates include:

```python
[
    "solution_architecture_scope_present",
    "architecture_context_view_present",
    "architecture_container_boundary_present",
    "architecture_boundary_per_slice",
    "boundary_responsibility_owner_present",
    "bounded_context_architecture_boundary_trace",
    "dependency_rules_present",
    "public_contract_boundary_trace_present",
    "data_ownership_boundary_present",
    "runtime_deployment_topology_present",
    "observability_architecture_present",
    "quality_attribute_scenarios_present",
    "tradeoff_record_for_high_impact_decision",
    "adr_for_architecture_decision",
    "trust_boundary_security_review_present",
    "domain_to_architecture_trace_present",
    "diagram_render_check_present",
    "architecture_fitness_function_present",
    "migration_rollback_path_present",
    "architecture_docs_as_code_present",
    "architecture_owner_review_present",
    "accepted_gap_recorded",
]
```

Assert `solution_architecture` eval fields include:

```python
[
    "solution_architecture_scope_contract_present",
    "architecture_context_view_contract_present",
    "architecture_boundary_contract_present",
    "boundary_owner_contract_present",
    "domain_architecture_trace_contract_present",
    "public_contract_trace_contract_present",
    "data_ownership_boundary_contract_present",
    "trust_boundary_review_contract_present",
    "quality_attribute_scenarios_contract_present",
    "architecture_decision_record_contract_present",
    "runtime_observability_contract_present",
    "diagram_render_check_contract_present",
    "architecture_fitness_function_contract_present",
    "migration_rollback_contract_present",
    "architecture_docs_lifecycle_contract_present",
    "accepted_gap_contract_present",
    "unsupported_architecture_claims_rejected_contract_present",
]
```

- [x] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing architecture gates.

- [x] **Step 3: Add architecture catalog data**

Rules:

- applies for complex/team/production/API/data/AI/runtime/ownership changes;
- not applicable for small text-only docs edits and mechanical formatting;
- high-impact decisions trigger ADR or architecture review;
- diagram presence alone is `present_unverified`.

- [x] **Step 4: Add and register templates**

Create:

- `architecture-review-record.md`;
- `architecture-fitness-functions.md`;
- `trust-boundary-map.md`;
- `architecture-docs-tooling-decision.md`.

Extend `architecture-overview.md` and `adr.md` with owner, boundary, quality attribute, verification and rollback fields.

- [x] **Step 5: Add audit recommendations**

Recommendations:

- multi-surface project without architecture overview -> `P1_high_risk`;
- public contract or data boundary without owner -> `P1_high_risk`;
- architecture docs without render check -> `P2_recommended`;
- high-impact decision without ADR or accepted gap -> `P1_high_risk`;
- service/runtime behavior without observability evidence -> `P1_high_risk`;
- architecture migration or service split without rollback path -> `P1_high_risk`;
- repeated boundary drift signals -> `P2_recommended` for fitness functions;
- unsupported claims listed in the deep-audit update -> `P1_high_risk` as rejected evidence.

Recommendation artifacts:

| Gate or signal | Recommendation artifact |
| --- | --- |
| Architecture scope, context view, container boundary | `architecture-overview.md` |
| Boundary owner, owner review, accepted gap | `architecture-review-record.md` |
| Public API/event/SDK/generated client contract | `api-contract-review.md` |
| Persistent data, analytics, PII, migration data ownership | `database-dictionary.md` |
| Trust boundary and security-sensitive boundary | `trust-boundary-map.md`, `security-risk-review.md` |
| High-impact decision, tradeoff, ADR trigger | `adr.md` |
| Runtime topology and migration rollback | `architecture-overview.md`, `migration-plan.md` |
| Observability, dependency rules, architecture fitness functions | `architecture-fitness-functions.md` |
| Architecture-as-code, diagram render check, docs lifecycle | `architecture-docs-tooling-decision.md` |

False-positive and accepted-gap coverage must keep C4 detail level, architecture-as-code, Well-Architected review and docs tooling conditional rather than universal requirements.

- [x] **Step 6: Update skills and evals**

Update planner and risk reviewer to require architecture boundary, owner evidence, ADR trigger, render evidence, runtime/observability evidence and rollback evidence for high-impact slices. Add fixture eval check `solution_architecture_contract_present`.

- [x] **Step 7: Run verification and commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md docs\superpowers\plans\2026-05-25-track-9-methodology-intelligence.md PLAN.md TEST.md EVALS.md RUNLOG.md docs\product-agent-os
git commit -m "feat: integrate solution architecture methodology"
```

Expected: focused tests, fixture eval, full unittest, transcript eval, compatibility check, docs check and diff hygiene pass before commit.

Run `python -m mkdocs build --strict` only if implementation changes navigation, Mermaid diagrams, Markdown extensions, MkDocs configuration or Product-Agent OS docs navigation.

---

### Task 11: T9-D4 Quality, Testing & Evals Integration

**Files:**
- Source: `docs/methodologies/quality-testing-evals.md`
- Modify: catalog, audit, `TEST.md`, `EVALS.md`, `behavioral-workflows.json`
- Create: `test-eval-matrix.md`
- Create: `quality-strategy.md`
- Create: `ci-evidence-record.md`
- Create: `flaky-test-policy.md`
- Create: `manual-qa-evidence.md`

Deep-audit update from `docs/methodologies/quality-testing-evals.md` and `docs/sources/methodology-research/quality-testing-evals.md`:

- The compact task list below must represent quality as current evidence, not as a generic "tests exist" signal.
- Required gates include risk-based test portfolio, acceptance traceability, Red-Green-Refactor or explicit gap, contract checks, runtime evidence, manual QA evidence, visual/a11y evidence, eval spec, eval rerun evidence, CI quality gate, flaky-test policy, coverage policy, test data privacy, bug reproduction evidence, regression impact and evidence-before-completion.
- Unsupported claims must be rejected as evidence: more tests always means better quality, 100 percent line coverage proves correctness, E2E tests should dominate because they are most realistic, manual QA is not evidence, and AI evals are optional for AI behavior changes.
- Template scope for this slice is intentionally five new artifacts plus strengthened generated `TEST.md`, `EVALS.md`, `RUNLOG.md`, `project-readiness.json` and `behavioral-workflows.json`; broader candidate artifacts such as `red-green-refactor-log.md`, `bug-reproduction.md`, `risk-based-test-plan.md`, `regression-impact-map.md`, `contract-test-map.md`, `runtime-evidence.md`, `visual-a11y-evidence.md`, `coverage-policy.md`, `mutation-test-report.md`, `property-test-spec.md`, `flaky-test-ledger.md`, `ci-quality-gates.md`, `eval-run-report.md`, `manual-qa-charter.md` and `evidence-packet.md` must either be mapped to the five artifacts or existing control-plane artifacts in this slice, or recorded in the Track 9 backlog with an explicit defer reason.
- Coverage, mutation testing, property-based testing, Playwright/visual checks, Promptfoo/Ragas and CI workflow changes are conditional recommendations, not universal gates. Tests must preserve lightweight behavior for typo-only docs edits, formatting-only changes, docs-only source cleanup and dependency metadata changes without behavior impact.

#### T9-D4 Task Matrix

| ID | Task | Primary files | Критерии приемки | Verification |
| --- | --- | --- | --- | --- |
| `T9-D4-M0` | Refresh plan/backlog before implementation | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, `docs/sources/product-agent-os-track-9-backlog.md` | Deep-audit deltas are recorded: current evidence, risk-based portfolio, regression impact, contract/runtime/manual/visual/eval evidence, CI permissions, flaky ownership, coverage-as-signal, test data privacy, unsupported claims, template scope and deferred artifact mapping. | `python tools\check_docs.py` |
| `T9-D4-M1` | Add RED catalog contract for `quality_testing_evals` | `tests/product_agent_os/test_methodology_catalog.py` | Test asserts full gate set, five new artifacts, explicit eval field names, applies/not-applicable rules, maturity/complexity impact, Track 8 scenarios, overlaps and unsupported-claim rejection contract. | `python -m unittest tests.product_agent_os.test_methodology_catalog -v` fails before catalog implementation on missing quality gates, artifacts or eval fields. |
| `T9-D4-M2` | Add RED audit recommendation coverage | `tests/product_agent_os/test_methodology_audit.py` | Tests cover no test command/evidence, missing acceptance traceability, bugfix without reproduction, deterministic change without test-first evidence or gap, API/event/schema without contract check, runtime claim without evidence, UI visual/a11y severity split, AI eval baseline/rerun gaps, regression impact, flaky/retry ownership, coverage-as-proof rejection, test data privacy, unsupported claims and typo/format/docs-only false positives. | `python -m unittest tests.product_agent_os.test_methodology_audit -v` fails before audit implementation on missing quality recommendations. |
| `T9-D4-M3` | Add RED template, lifecycle and fixture checks | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_lifecycle_skills.py`, `tests/product_agent_os/test_fixture_eval_runner.py`, `tests/product_agent_os/test_behavioral_workflow_evals.py` | Tests require five registered templates, `quality_testing_evals_contract_present`, renderer file count increase by five from the current T9-D3 baseline, lifecycle wording for evidence/current-run/risk/contract/eval/flaky/privacy gates, and behavioral eval coverage for completion claims without current evidence. | `python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_behavioral_workflow_evals -v` fails before templates and eval checks exist. |
| `T9-D4-M4` | Fill `quality_testing_evals` catalog data | `plugins/product-agent-os/assets/methodology/methodology-catalog.json` | Domain records applies/not-applicable rules, Track 8 scenarios, artifacts, all gates, explicit eval fields and overlaps with requirements, architecture, frontend, backend, API, data, AI, release, security and agent workflow domains. | Focused catalog test passes for `quality_testing_evals`. |
| `T9-D4-M5` | Implement read-only quality audit recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py` | Audit emits prioritized recommendations with stable shape and artifact mapping: strategy/risk scope -> `quality-strategy.md`; traceability and contract/eval mapping -> `test-eval-matrix.md`; CI evidence -> `ci-evidence-record.md`; flaky/retry -> `flaky-test-policy.md`; manual/runtime/visual evidence -> `manual-qa-evidence.md`; AI eval gaps -> `ai-eval-spec.md`/`EVALS.md`; API contract gaps -> `api-contract-review.md`; completion evidence -> `RUNLOG.md`. False-positive intents stay `not_applicable`. | Focused audit tests pass and recommendation packets keep priority, domain, gate, artifact, evidence, approval, accepted-gap and residual-risk fields. |
| `T9-D4-M6` | Add and register quality artifact templates | `plugins/product-agent-os/assets/templates/artifact-templates/test-eval-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/quality-strategy.md`, `plugins/product-agent-os/assets/templates/artifact-templates/ci-evidence-record.md`, `plugins/product-agent-os/assets/templates/artifact-templates/flaky-test-policy.md`, `plugins/product-agent-os/assets/templates/artifact-templates/manual-qa-evidence.md`, `plugins/product-agent-os/scripts/product_agent_os/templates.py` | Templates include `Source status:`, owner, current evidence, command/eval/runtime/manual evidence, accepted gap, residual risk, approval boundary, verification, rollback or no-rollback rationale, test data privacy/no secrets guidance and target paths `.codex/artifact-templates/<name>`. | Infrastructure template tests pass and rendered templates have no unresolved substitutions. |
| `T9-D4-M7` | Strengthen generated control-plane and eval templates | `plugins/product-agent-os/assets/templates/control-plane/TEST.md`, `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` | Generated artifacts expose quality strategy, test/eval matrix, risk-based scope, acceptance traceability, contract/runtime/manual/visual evidence, eval baseline/rerun, CI evidence, flaky policy, coverage policy, test data privacy and current evidence before completion. Behavioral evals keep completion claims evidence-bound. | Infrastructure and behavioral eval template tests pass. |
| `T9-D4-M8` | Route Quality, Testing & Evals through lifecycle skills | `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `plugins/product-agent-os/skills/requirements-author/SKILL.md`, `plugins/product-agent-os/skills/implementation-planner/SKILL.md`, `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`, `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`, `plugins/product-agent-os/skills/docs-maintainer/SKILL.md`, `plugins/product-agent-os/skills/pr-release-operator/SKILL.md` | Skills require current evidence before completion claims, route quality gates to `test-eval-designer` and `risk-reviewer`, preserve explicit-gap language, and do not force TDD, E2E, coverage, visual, mutation, property-based, CI or AI evals when not applicable. | Lifecycle skill tests pass for shared quality methodology wording. |
| `T9-D4-M9` | Add fixture eval contract | `plugins/product-agent-os/scripts/run_fixture_eval.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | `quality_testing_evals_contract_present` validates catalog gates, artifacts, eval fields, templates, lifecycle skill coverage and evidence-before-completion continuity. `python-app` expected checks include the new contract. | `python plugins\product-agent-os\scripts\run_fixture_eval.py` exits `0` after implementation with renderer file count 97. |
| `T9-D4-M10` | Sync docs and control-plane evidence | `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `docs/sources/product-agent-os-track-9-backlog.md`, `docs/product-agent-os/behavioral-evals.md`, Product-Agent OS README/docs only when behavior is user-facing | Current state records `T9-D4` completion, RED/GREEN evidence, renderer file count delta, unsupported-claim handling, deferred candidate artifact rationale, residual risks and next action `T9-D5`. Source registry is updated only if new source-backed claims are added outside existing source entries. | Full verification commands below pass; `git diff --check` exits `0`. Run strict MkDocs only if navigation, Mermaid diagrams, Markdown extensions, MkDocs config or Product-Agent OS docs navigation changed. |
| `T9-D4-M11` | Add quality discovery-signal contract | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_methodology_audit.py` | Discovery and audit recognize quality signals from directories (`tests/`, `test/`, `spec/`, `e2e/`, `playwright/`, `cypress/`, `coverage/`, `evals/`, `.github/workflows/`, `fixtures/`, `__tests__/`, `snapshots/`), files (`TEST.md`, `EVALS.md`, `RUNLOG.md`, `pytest.ini`, `tox.ini`, `vitest.config.*`, `jest.config.*`, `playwright.config.*`, `coverage.*`, `promptfoo.yaml`, `promptfooconfig.yaml`, `pact.*`, `openapi.*`, `asyncapi.*`), terms and dependency signals (`pytest`, `unittest`, `JUnit`, `Jest`, `Vitest`, `Playwright`, `Testing Library`, `Storybook`, `Pact`, `Stryker`, `Hypothesis`, `Promptfoo`, `Ragas`, `Codecov`, `GitHub Actions`). Detection alone remains `present_unverified`, not `present_verified`. | `python -m unittest tests.product_agent_os.test_discovery tests.product_agent_os.test_methodology_audit -v` fails RED before signal implementation and passes after. |
| `T9-D4-M12` | Lock explicit quality eval-field names | `tests/product_agent_os/test_methodology_catalog.py`, `plugins/product-agent-os/assets/methodology/methodology-catalog.json`, `plugins/product-agent-os/scripts/run_fixture_eval.py` | Catalog and fixture eval use these stable fields: `quality_strategy_contract_present`, `risk_based_scope_contract_present`, `test_first_or_gap_contract_present`, `acceptance_traceability_contract_present`, `contract_check_contract_present`, `runtime_evidence_contract_present`, `manual_qa_evidence_contract_present`, `visual_a11y_evidence_contract_present`, `eval_spec_contract_present`, `eval_rerun_evidence_contract_present`, `current_evidence_before_completion_contract_present`, `ci_quality_gate_contract_present`, `flaky_test_policy_contract_present`, `coverage_policy_contract_present`, `test_data_privacy_contract_present`, `bug_reproduction_evidence_contract_present`, `regression_impact_contract_present`, and `unsupported_quality_claims_rejected_contract_present`. | Focused catalog and fixture eval tests fail RED before fields exist and pass after implementation. |
| `T9-D4-M13` | Add exact quality gate priority and artifact mapping | `tests/product_agent_os/test_methodology_audit.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `docs/sources/product-agent-os-track-9-backlog.md` | Tests assert gate -> priority -> artifact mapping, including: missing local test command/evidence -> `quality_strategy_present` `P0_blocker` -> `quality-strategy.md`; risky/broad/constrained scope -> `risk_based_scope_present` `P1_high_risk` -> `quality-strategy.md`; missing acceptance/check mapping -> `acceptance_traceability_present` `P1_high_risk` -> `test-eval-matrix.md`; deterministic bugfix/business rule without test-first or gap -> `test_first_or_gap_present` `P1_high_risk` -> `test-eval-matrix.md`; public API/event/schema without contract check -> `contract_check_present` `P1_high_risk` -> `api-contract-review.md`; runtime claim without evidence -> `runtime_evidence_present` `P1_high_risk` -> `manual-qa-evidence.md`; public UI visual/a11y gap -> `P1_high_risk`, internal UI visual/a11y gap -> `P2_recommended`, both -> `manual-qa-evidence.md`; AI/subjective eval spec or rerun gap -> `P1_high_risk` -> `ai-eval-spec.md` or `EVALS.md`; CI quality gate missing -> `P1_high_risk` for release/shared branch and `P2_recommended` otherwise -> `ci-evidence-record.md`; flaky/retry without owner/expiry -> `P2_recommended` -> `flaky-test-policy.md`; coverage-as-proof claim -> `P1_high_risk` rejected evidence and coverage policy gap -> `P2_recommended` -> `quality-strategy.md`; test data privacy gap -> `P1_high_risk` -> `quality-strategy.md`; bugfix without reproduction -> `P0_blocker` or accepted gap -> `bug-rescue-report.md`/`RUNLOG.md`; regression impact missing -> `P1_high_risk` -> `test-eval-matrix.md`; completion claim without current evidence -> `P0_blocker` -> `RUNLOG.md`; unsupported quality claims -> `P1_high_risk` -> `quality-strategy.md`. | `python -m unittest tests.product_agent_os.test_methodology_audit -v` asserts every mapping and false-positive exception. |
| `T9-D4-M14` | Update cross-domain synthesis backlog and deferred artifact mapping | `docs/sources/product-agent-os-track-9-backlog.md`, `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md` | Backlog records cross-domain synthesis items for shared runtime evidence with Frontend/Backend/Desktop/Native, visual/a11y evidence with Frontend, contract checks with API/Integrations, test data privacy with Database/Security/AI, eval baseline/rerun with LLM/AI/RAG, CI quality gates with Delivery/Operations, and completion evidence with all domains. Every candidate artifact from the source artifact is explicitly mapped to one of the five T9-D4 artifacts or existing `TEST.md`, `EVALS.md`, `RUNLOG.md`, `ai-eval-spec.md`, `api-contract-review.md`, `bug-rescue-report.md`, `ci-stabilization-report.md`, or deferred with owner/reason. | `python tools\check_docs.py` passes and backlog contains T9-D4 cross-domain and deferred-artifact entries. |
| `T9-D4-M15` | Expand final verification and staging scope | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md` | Step 6 final commands include focused T9-D4 tests, fixture eval, full unittest, transcript eval, Codex compatibility check, docs check and `git diff --check`; staging includes `plugins/product-agent-os`, `tests/product_agent_os`, `docs/sources/product-agent-os-track-9-backlog.md`, `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, and `docs/product-agent-os` when changed. | Plan review confirms no verification/staging gap before `feat: integrate quality testing evals methodology`. |

- [x] **Step 0: Record deep-audit deltas before implementation**

Modify `docs/sources/product-agent-os-track-9-backlog.md` before code implementation and record these `T9-D4` deep-audit deltas from `docs/methodologies/quality-testing-evals.md` and `docs/sources/methodology-research/quality-testing-evals.md`:

- Quality evidence is current command/eval/runtime/manual evidence or an explicit inspection-only gap, not generic "tests exist" or old CI status.
- Discovery must recognize quality signals from test directories, test/eval config files, CI workflows, coverage reports, Playwright/Cypress/Storybook/Pact/Promptfoo/Ragas/Stryker/Hypothesis/Codecov/GitHub Actions signals and flaky-test evidence; detection alone remains `present_unverified`.
- Stable eval fields must include every `quality_testing_evals` gate plus `unsupported_quality_claims_rejected_contract_present`.
- Recommendation mapping must name the exact gate, priority and artifact for test strategy, risk scope, acceptance traceability, test-first gap, contract checks, runtime/manual/visual evidence, eval spec/rerun, CI quality gate, flaky policy, coverage policy, test data privacy, bug reproduction, regression impact and completion evidence.
- Candidate artifacts from the source methodology must be mapped to the five T9-D4 templates or existing control-plane artifacts, or deferred with owner/reason.
- Cross-domain synthesis backlog must capture shared runtime evidence, visual/a11y evidence, contract checks, test data privacy, eval baseline/rerun, CI quality gates and evidence-before-completion so later domains do not duplicate or conflict with T9-D4.
- Unsupported claims must be rejected as evidence: more tests always means better quality, 100 percent line coverage proves correctness, E2E tests should dominate because they are most realistic, manual QA is not evidence and AI evals are optional for AI behavior changes.
- Lightweight false-positive rules must preserve `not_applicable` or accepted-gap behavior for typo-only docs edits, formatting-only changes, docs-only source cleanup and dependency metadata changes without behavior impact.

- [x] **Step 1: Add RED test for quality gates**

Assert `quality_testing_evals` gates include:

```python
[
    "quality_strategy_present",
    "risk_based_scope_present",
    "test_first_or_gap_present",
    "acceptance_traceability_present",
    "contract_check_present",
    "runtime_evidence_present",
    "manual_qa_evidence_present",
    "visual_a11y_evidence_present",
    "eval_spec_present",
    "eval_rerun_evidence_present",
    "current_evidence_before_completion",
    "ci_quality_gate_present",
    "flaky_test_policy_present",
    "coverage_policy_present",
    "test_data_privacy_present",
    "bug_reproduction_evidence_present",
    "regression_impact_present",
]
```

- [x] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing quality gates.

- [x] **Step 3: Add quality catalog and recommendations**

Rules:

- quality domain applies to every non-trivial project;
- missing test command is `P0_blocker`;
- AI changes without eval baseline are `P1_high_risk`;
- UI changes without visual/a11y evidence are `P1_high_risk` for public UI and `P2_recommended` for internal UI;
- flaky tests produce owner question and `P2_recommended` policy recommendation.

- [x] **Step 4: Add templates and skill updates**

Create and register:

- `test-eval-matrix.md`;
- `quality-strategy.md`;
- `ci-evidence-record.md`;
- `flaky-test-policy.md`;
- `manual-qa-evidence.md`.

Update `test-eval-designer`, `risk-reviewer` and `implementation-planner` with current evidence rules.

- [x] **Step 5: Add eval runner checks**

Update fixture eval with `quality_testing_evals_contract_present` and assert current evidence before completion remains active.

- [x] **Step 6: Run verification and commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md docs\superpowers\plans\2026-05-25-track-9-methodology-intelligence.md PLAN.md TEST.md EVALS.md RUNLOG.md docs\product-agent-os
git commit -m "feat: integrate quality testing evals methodology"
```

Expected: focused tests, fixture eval, full unittest, transcript eval, compatibility check, docs check and diff hygiene pass before commit.

---

### Task 12: T9-D5 Codex / Agentic Workflow Integration

**Files:**
- Source: `docs/methodologies/codex-agentic-workflow.md`
- Modify: catalog, audit, all lifecycle skills, `AGENTS.md` template, `.codex/config.toml` template
- Create: `model-reasoning-policy.md`
- Create: `mcp-permission-review.md`
- Create: `hook-governance.md`
- Create: `skill-promotion-record.md`
- Create: `agent-eval-workflow.md`

Deep-audit update from `docs/methodologies/codex-agentic-workflow.md` and `docs/sources/methodology-research/codex-agentic-workflow.md`:

- The compact task list below must represent Codex / Agentic Workflow as durable project state and capability governance, not as chat memory or broad agent orchestration.
- Required gates include `agentic_scope_classified`, `source_of_truth_present`, `control_plane_present`, `read_only_discovery_complete`, `approval_boundary_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `skill_promotion_evidence_present`, `plugin_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `automation_manual_stability_present`, `model_reasoning_policy_present`, `memory_policy_present`, `agent_eval_workflow_present`, and `agentic_evidence_before_completion`.
- Existing artifacts must be reused instead of duplicated where possible: `agent-task-packet.md`, `handoff-contract.md`, `worktree-ownership.md`, `automation-candidate.md`, `plugin-blueprint.md`, `approval-record.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, and `AGENTS.md`.
- New template scope for this slice is intentionally five artifacts unless the implementation audit proves separate ownership for additional candidates: `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md`.
- Candidate artifacts not in the compact task list must be explicitly mapped or deferred: `context-memory-policy.md`, `agentic-workflow-readiness.md`, `agent-eval-case.md`, `skill-candidate.md`, `skill-failure-log.md`, and `hook-activation-record.md`.
- Discovery must recognize `.codex/`, `.codex/agents/`, `.codex/workflows/`, `.codex/artifact-templates/`, `.agents/skills/`, `.agents/plugins/`, `plugins/`, `skills/`, `subagents/`, `docs/playbooks/`, `docs/artifact-templates/`, `docs/product-agent/`, `docs/runtime/`, `docs/insights/`, `AGENTS.md`, `AGENTS.override.md`, `SKILL.md`, `.codex-plugin/plugin.json`, `.mcp.json`, `hooks.json`, `config.toml`, `automation.toml`, `agent-task-packet.md`, `handoff-contract.md`, `worktree-ownership.md`, `plugin-blueprint.md`, `automation-candidate.md`, Codex/App/CLI/IDE/subagent/skill/MCP/hook/plugin/automation/worktree/runlog/eval/handoff/task-packet/source-of-truth/approval-boundary/evidence terms, and external-write/network/production/secrets/GitHub Action/publish/deploy/CI/side-effect/overlap risks.
- Recommendations must reject unsupported claims as evidence: memory is project source of truth, subagents are automatically faster, MCP tools are safe because they are tools, hooks are harmless convenience scripts, a repeated workflow should become automation immediately, Agents SDK and Codex runtime are the same layer, and inspection proves completion.
- False-positive behavior must preserve lightweight local/docs/simple work: do not force subagents, worktrees, MCP review, hook governance, plugin packaging, automation promotion, Agents SDK orchestration, or agent evals unless the source signals, intent or risk boundary makes them applicable.
- The implementation must resolve source open questions instead of leaving them implicit: hard-block vs warning-level gate policy, runtime routing shape, skill trigger tests and failure logs, automation manual stability threshold, hook review depth, MCP review applicability, worktree requirements for subagents, Codex-native subagents vs Agents SDK decision, agent eval workflow depth, and official-source registry freshness.

#### T9-D5 Task Matrix

| ID | Task | Primary files | Критерии приемки | Verification |
| --- | --- | --- | --- | --- |
| `T9-D5-M0` | Refresh plan/backlog before implementation | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, `docs/sources/product-agent-os-track-9-backlog.md` | Deep-audit deltas are recorded: full gate set, reused artifacts, five-template scope, candidate artifact mapping/defer list, discovery signals, false-positive rules, unsupported claims, runtime routing and verification scope. | `python tools\check_docs.py` |
| `T9-D5-M1` | Add RED catalog contract for `codex_agentic_workflow` | `tests/product_agent_os/test_methodology_catalog.py` | Test asserts full gate set, applies/not-applicable rules, maturity/complexity impact, Track 8 scenarios, artifact list, eval field list and overlaps for quality, delivery, security, AI, plugin, automation and ownership domains. | `python -m unittest tests.product_agent_os.test_methodology_catalog -v` fails before catalog implementation on missing Codex workflow gates, artifacts or eval fields. |
| `T9-D5-M2` | Add RED audit recommendation coverage | `tests/product_agent_os/test_methodology_audit.py` | Tests cover missing control plane/source of truth, missing read-only discovery evidence, subagent/parallel intent without ownership split, MCP side effects without permission review, hook activation without approval, plugin packaging without boundary, repeated workflow without manual evidence, automation without stability, memory-as-source-of-truth, missing model/reasoning policy, agent behavior without eval workflow, and unsupported claims. | `python -m unittest tests.product_agent_os.test_methodology_audit -v` fails before audit implementation on missing Codex workflow recommendations. |
| `T9-D5-M3` | Add RED discovery-signal coverage | `tests/product_agent_os/test_discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/discovery.py` | Discovery reports `codex_agentic_workflow` signals from Codex directories, files, config, MCP, hooks, plugins, skills, subagents, automations, task packets, handoff/worktree artifacts, terms and side-effect risks. Detection remains `present_unverified`. | `python -m unittest tests.product_agent_os.test_discovery -v` fails before signal implementation and passes after. |
| `T9-D5-M4` | Fill `codex_agentic_workflow` catalog data | `plugins/product-agent-os/assets/methodology/methodology-catalog.json` | Domain records applies/not-applicable rules, Track 8 scenarios, artifacts, all gates, eval fields, maturity/complexity impact and overlaps. Includes `agentic_scope_classified`, `read_only_discovery_complete` and `subagent_parallelism_safe`, not only the compact original gate list. | Focused catalog test passes for `codex_agentic_workflow`. |
| `T9-D5-M5` | Implement read-only audit recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py` | Audit emits prioritized recommendations with stable shape and artifact mapping for control plane, source of truth, read-only discovery, approval boundaries, handoffs, ownership, MCP, hooks, plugin packaging, skills, automation, model/reasoning, memory, agent evals and completion evidence. | Focused audit tests pass and recommendation packets keep priority, domain, gate, artifact, evidence, approval, accepted-gap and residual-risk fields. |
| `T9-D5-M6` | Add and register Codex workflow artifact templates | `plugins/product-agent-os/assets/templates/artifact-templates/model-reasoning-policy.md`, `plugins/product-agent-os/assets/templates/artifact-templates/mcp-permission-review.md`, `plugins/product-agent-os/assets/templates/artifact-templates/hook-governance.md`, `plugins/product-agent-os/assets/templates/artifact-templates/skill-promotion-record.md`, `plugins/product-agent-os/assets/templates/artifact-templates/agent-eval-workflow.md`, `plugins/product-agent-os/scripts/product_agent_os/templates.py` | Templates include `Source status:`, owner, evidence, accepted gap, residual risk, approval boundary, verification, rollback/disable path where applicable, no secrets/private data guidance and renderer targets under `.codex/artifact-templates/`. | Infrastructure template tests pass and rendered templates have no unresolved substitutions. |
| `T9-D5-M7` | Map or defer extra source artifacts | `docs/sources/product-agent-os-track-9-backlog.md`, `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md` | `context-memory-policy.md`, `agentic-workflow-readiness.md`, `agent-eval-case.md`, `skill-candidate.md`, `skill-failure-log.md`, and `hook-activation-record.md` are mapped to the five templates/existing artifacts or deferred with owner and reason. | `python tools\check_docs.py` passes and backlog contains the mapping/defer decisions. |
| `T9-D5-M8` | Strengthen generated `AGENTS.md` template | `plugins/product-agent-os/assets/templates/control-plane/AGENTS.md` | Template covers source-of-truth boundaries, memory as recall only, runtime routing, approval boundaries, model/reasoning policy, manual -> playbook -> skill -> plugin -> automation promotion, and no hooks/MCP/automation/external writes without approval. | Infrastructure template tests assert required terms. |
| `T9-D5-M9` | Strengthen generated `.codex/config.toml` template | `plugins/product-agent-os/assets/templates/config/config.toml` | Template records role/risk model policy, approval defaults, sandbox defaults, MCP/hook/automation activation boundaries and no silent activation. | Config template TOML tests and infrastructure template tests pass. |
| `T9-D5-M10` | Strengthen generated control-plane and eval templates | `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`, `plugins/product-agent-os/assets/templates/control-plane/TEST.md`, `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` | Generated artifacts expose Codex workflow gates, readiness statuses, runtime routing, approval boundaries, agent eval workflow, memory policy and completion evidence. Behavioral evals block automation/hook/MCP/Agents SDK shortcuts. | Infrastructure and behavioral workflow eval tests pass. |
| `T9-D5-M11` | Route Codex workflow through lifecycle skills | `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`, `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `plugins/product-agent-os/skills/requirements-author/SKILL.md`, `plugins/product-agent-os/skills/implementation-planner/SKILL.md`, `plugins/product-agent-os/skills/agent-team-designer/SKILL.md`, `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`, `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`, `plugins/product-agent-os/skills/docs-maintainer/SKILL.md`, `plugins/product-agent-os/skills/pr-release-operator/SKILL.md`, `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md`, `plugins/product-agent-os/skills/automation-promoter/SKILL.md` | Skills mention Track 9 methodology recommendations as context, enforce staged-first/write approval, route subagents through fresh task packets and ownership, keep memory recall-only, and forbid hook/MCP/automation/external activation without explicit approval. | Lifecycle skill tests pass for shared Codex workflow wording. |
| `T9-D5-M12` | Add fixture eval contract | `plugins/product-agent-os/scripts/run_fixture_eval.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | `codex_agentic_workflow_contract_present` validates catalog gates, artifacts, eval fields, templates, lifecycle skill coverage and compatibility with candidate-only hooks/automation behavior. `python-app` expected checks include the new contract and renderer file count increases by five from the T9-D4 baseline. | `python plugins\product-agent-os\scripts\run_fixture_eval.py` exits `0` after implementation with expected renderer file count. |
| `T9-D5-M13` | Add false-positive and approval-bound coverage | `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | Simple docs/local work does not force subagents, worktrees, MCP review, hooks, plugin packaging, automation, Agents SDK or agent evals. Side-effecting MCP, hook activation, automation schedule, external writes and production data remain `approval_required`. | Focused audit/discovery/fixture tests pass. |
| `T9-D5-M14` | Add unsupported-claim rejection | `tests/product_agent_os/test_methodology_audit.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py` | Unsupported claims are rejected as evidence: memory as source of truth, subagents always faster, MCP safe by default, hooks harmless, immediate automation, Agents SDK equals Codex runtime, and inspection proves completion. | Focused audit tests assert each unsupported claim creates a Codex workflow recommendation or owner question. |
| `T9-D5-M15` | Sync docs and control-plane evidence | `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `docs/sources/product-agent-os-track-9-backlog.md`, Product-Agent OS README/docs only when behavior is user-facing | Current state records `T9-D5` completion, RED/GREEN evidence, renderer file count delta, unsupported-claim handling, deferred artifact rationale, residual risks and next action `T9-D6`. | Full verification commands below pass; `git diff --check` exits `0`. |
| `T9-D5-M16` | Expand final verification and staging scope | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md` | Step 6 final commands include focused T9-D5 tests, fixture eval, full unittest, transcript eval, Codex compatibility check, docs check and `git diff --check`; commit/staging remains deferred to explicit user request. | Plan review confirms no verification gap before a later `feat: integrate codex agentic workflow methodology` commit. |
| `T9-D5-M17` | Define readiness severity policy | `plugins/product-agent-os/assets/methodology/methodology-catalog.json`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | Codex workflow gates distinguish hard blockers from warnings: missing control plane/source of truth for multi-slice work, active automation, hook activation, side-effecting MCP, external writes, production data, overlapping subagents, missing approval boundary and completion claims without evidence are blocker/high-risk; lightweight docs/local work remains warning/not-applicable. | Focused audit tests assert priority mapping and no false hard blockers for simple docs/local fixtures. |
| `T9-D5-M18` | Add runtime routing decision matrix | `plugins/product-agent-os/assets/templates/control-plane/AGENTS.md`, `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`, `plugins/product-agent-os/assets/templates/artifact-templates/model-reasoning-policy.md`, `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_lifecycle_skills.py` | Runtime routing records when to use Codex App, IDE extension, CLI, `codex exec`, GitHub Action, MCP, Agents SDK and automation by ambiguity, local command needs, external permissions, repeatability and evidence needs. | Template and lifecycle tests assert every runtime surface and no default escalation to MCP, Agents SDK or automation. |
| `T9-D5-M19` | Add skill lifecycle test policy | `plugins/product-agent-os/assets/templates/artifact-templates/skill-promotion-record.md`, `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md`, `plugins/product-agent-os/skills/automation-promoter/SKILL.md`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_lifecycle_skills.py` | Skill promotion requires trigger tests, negative trigger tests, missing-input behavior, verification failure behavior and failure log evidence, not only a happy-path manual run. | Template/lifecycle tests assert trigger, negative trigger, missing-input and failure-log terms. |
| `T9-D5-M20` | Define automation manual stability threshold | `plugins/product-agent-os/assets/templates/artifact-templates/skill-promotion-record.md`, `plugins/product-agent-os/assets/templates/automations/automation-candidate.md`, `plugins/product-agent-os/skills/automation-promoter/SKILL.md`, `tests/product_agent_os/test_automation_policy.py`, `tests/product_agent_os/test_lifecycle_skills.py` | Automation promotion requires at least two successful manual runs or an explicit owner-approved accepted gap, plus durable prompt, cadence, environment, verification, owner and disable/rollback path. Active schedules remain out of scope. | Automation policy and lifecycle tests assert two-run or accepted-gap threshold and active automation remains blocked. |
| `T9-D5-M21` | Define hook governance review depth | `plugins/product-agent-os/assets/templates/artifact-templates/hook-governance.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Hook governance distinguishes staged hook templates, read-only validation hooks and blocking/side-effecting hooks. Activation requires trust review, event/matcher/command, failure behavior, disable path and explicit approval; blocking or side-effecting hooks require two-stage risk review. | Focused tests assert unapproved hook activation is high-risk/approval-required and staged templates remain allowed. |
| `T9-D5-M22` | Define MCP review applicability policy | `plugins/product-agent-os/assets/templates/artifact-templates/mcp-permission-review.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | MCP review is required for new MCP config, changed trust boundary, auth/secrets, remote servers, side-effecting tools, production/customer data or external writes. Read-only local docs MCP can be lower severity but still records capability/data boundary. | Focused tests assert side-effecting MCP is high-risk and read-only MCP is not over-blocked. |
| `T9-D5-M23` | Define worktree requirement policy for subagents | `plugins/product-agent-os/assets/templates/workflows/worktree-ownership.md`, `plugins/product-agent-os/assets/templates/artifact-templates/agent-task-packet.md`, `plugins/product-agent-os/skills/agent-team-designer/SKILL.md`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_lifecycle_skills.py` | Parallel subagents require worktrees or explicit ownership when edits can overlap, when generated files are shared, when migrations/contracts are touched, or when merge/rollback risk is high; read-only research can use packets without worktrees. | Template/lifecycle tests assert worktree requirement and sequential fallback rules. |
| `T9-D5-M24` | Add Codex-native subagents vs Agents SDK decision rule | `plugins/product-agent-os/assets/templates/artifact-templates/model-reasoning-policy.md`, `plugins/product-agent-os/assets/templates/control-plane/AGENTS.md`, `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_lifecycle_skills.py`, `tests/product_agent_os/test_codex_runtime_runner_contracts.py` | Codex-native subagents are the default for Codex App/CLI/IDE engineering delegation; Agents SDK is only for code-owned agent apps with application-owned orchestration, tools, guardrails, sessions, tracing and evals. Product-Agent OS must not require a standalone Agents SDK runner. | Tests assert Agents SDK is not treated as a Codex runtime surface and decision text is present. |
| `T9-D5-M25` | Expand agent eval workflow depth | `plugins/product-agent-os/assets/templates/artifact-templates/agent-eval-workflow.md`, `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_behavioral_workflow_evals.py` | Agent eval workflow covers baseline, trace-derived dataset, tool-call correctness, handoff correctness, expected/forbidden behavior, grader or deterministic assertion, threshold, rerun command, regression label, latency/cost and privacy/no-secrets handling. | Infrastructure and behavioral eval tests assert the full eval contract. |
| `T9-D5-M26` | Add official-source registry freshness check | `docs/sources/registry.md`, `docs/sources/product-agent-os-track-9-backlog.md`, `tests/product_agent_os/test_product_agent_os_docs.py`, `tools/check_docs.py` only if required paths change | T9-D5 records whether official OpenAI Codex/App/CLI/IDE/skills/subagents/MCP/hooks/plugins/approvals/memory/automation/Agents SDK/evals sources are already current or updated. New source-backed behavior outside existing registry entries updates the registry. | Docs tests or `python tools\check_docs.py` confirm source registry coverage; otherwise backlog records no registry update needed with reason. |

- [x] **Step 1: Add RED test for Codex workflow gates**

Assert `codex_agentic_workflow` gates include:

```python
[
    "agentic_scope_classified",
    "control_plane_present",
    "source_of_truth_present",
    "read_only_discovery_complete",
    "model_reasoning_policy_present",
    "fresh_context_handoff_present",
    "ownership_split_present",
    "subagent_parallelism_safe",
    "approval_boundary_present",
    "mcp_permission_review_present",
    "hook_activation_approval_present",
    "plugin_boundary_present",
    "skill_promotion_evidence_present",
    "automation_manual_stability_present",
    "agent_eval_workflow_present",
    "memory_policy_present",
    "agentic_evidence_before_completion",
]
```

- [x] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing Codex workflow gates.

- [x] **Step 3: Add catalog and templates**

Create and register:

- `model-reasoning-policy.md`;
- `mcp-permission-review.md`;
- `hook-governance.md`;
- `skill-promotion-record.md`;
- `agent-eval-workflow.md`.

Extend `AGENTS.md` and `.codex/config.toml` templates with model/reasoning policy and approval boundaries.

- [x] **Step 4: Add audit recommendations**

Recommendations:

- missing control-plane -> `P0_blocker`;
- MCP config or side-effecting tool without permission review -> `P1_high_risk`;
- hook activation without approval -> `P1_high_risk`;
- subagent/parallel intent without ownership split -> `P1_high_risk`;
- repeated workflow without evidence -> `P2_recommended` skill promotion record.

- [x] **Step 5: Update lifecycle skills**

All lifecycle skills must mention Track 9 methodology recommendations as context, but no skill should activate hooks, MCP, automation or external writes without approval.

- [x] **Step 6: Run verification; leave commit to explicit user request**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery -v
python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_automation_policy tests.product_agent_os.test_codex_runtime_runner_contracts -v
python -m unittest tests.product_agent_os.test_fixture_eval_runner.FixtureEvalRunnerTest.test_fixture_eval_checks_expected_renderer_behavior_by_fixture -v
python -m unittest tests.product_agent_os.test_fixture_eval_runner.FixtureEvalRunnerTest.test_cli_prints_json_and_exits_zero_when_all_fixtures_are_ok -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

Expected: focused tests, fixture eval, full unittest, transcript eval, compatibility check, docs check and diff hygiene pass before commit. Commit is intentionally deferred until explicitly requested in the current working branch.

---

### Task 13: T9-D6 Frontend Integration

**Files:**
- Source: `docs/methodologies/frontend.md`
- Modify: catalog, audit, `component-card.md`, `development-standards.md`
- Create: `frontend-flow-spec.md`
- Create: `frontend-state-matrix.md`
- Create: `frontend-visual-qa.md`
- Create: `frontend-accessibility-review.md`
- Create: `frontend-performance-budget.md`

Deep-audit update from `docs/methodologies/frontend.md` and `docs/sources/methodology-research/frontend.md`:

- The compact task list below must represent frontend as user-observable behavior and browser evidence, not as component hierarchy or code inspection.
- Required gates include `frontend_user_flow_acceptance_present`, `frontend_component_docs_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_fsd_boundary_reviewed`, `frontend_api_contract_alignment_present`, `frontend_accessibility_review_present`, `frontend_keyboard_focus_contract_present`, `frontend_responsive_viewport_matrix_present`, `frontend_visual_evidence_present`, `frontend_runtime_console_evidence_present`, `frontend_performance_budget_present`, `frontend_browser_support_present`, `frontend_content_i18n_boundary_present`, and `frontend_interaction_test_evidence_present`.
- Existing artifacts must be reused where possible: `component-card.md`, `acceptance-scenarios.md`, `api-contract-review.md`, `quality-strategy.md`, `test-eval-matrix.md`, `manual-qa-evidence.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, and `RUNLOG.md`.
- New template scope for this slice is intentionally five artifacts unless implementation proves separate ownership for additional candidates: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, and `frontend-performance-budget.md`.
- Candidate artifacts not in the compact task list must be explicitly mapped or deferred: `route-page-inventory.md`, `storybook-story-map.md`, `design-system-inventory.md`, `design-tokens-reference.md`, `frontend-boundary-map.md`, `fsd-boundary-record.md`, `frontend-api-dependency-map.md`, `responsive-viewport-matrix.md`, `keyboard-focus-map.md`, `visual-evidence-packet.md`, `frontend-interaction-test-matrix.md`, `frontend-browser-support-matrix.md`, and `frontend-content-i18n-record.md`.
- Discovery must recognize route/page/component directories, `.storybook/`, stories, Playwright, Vite, Next.js, Nuxt, SvelteKit, Astro, React, Vue, Svelte, Angular, Solid, Testing Library, axe, Chromatic, design tokens, themes, `components.json`, browser assets, viewport/accessibility/performance terms, and UI intent.
- False-positive behavior must preserve backend-only, data-only, CLI-only, docs-only, native-only, dependency-only and simple CRUD work. Storybook, FSD, Playwright, performance budgets and visual baselines must stay conditional.
- Recommendations must reject unsupported claims as evidence: FSD is mandatory for every frontend project, Storybook proves UI quality, automated accessibility addon output is enough, a desktop screenshot proves responsive UI, lab Web Vitals always represent production UX, and code inspection proves UI completion.
- The implementation must resolve source open questions instead of leaving them implicit: Storybook required/optional policy, minimum visual evidence thresholds, WCAG/default accessibility target, FSD boundary review depth, Web Vitals measurement path, browser/device support, content/i18n boundary and screenshot/story privacy policy.

#### T9-D6 Task Matrix

| ID | Task | Primary files | Критерии приемки | Verification |
| --- | --- | --- | --- | --- |
| `T9-D6-M0` | Refresh plan/backlog before implementation | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, `docs/sources/product-agent-os-track-9-backlog.md` | Deep-audit deltas are recorded: full gate set, reused artifacts, five-template scope, candidate artifact mapping/defer list, discovery signals, false-positive rules, unsupported claims, Storybook/FSD/a11y/visual/performance policies and verification scope. | `python tools\check_docs.py` |
| `T9-D6-M1` | Add RED catalog contract for `frontend` | `tests/product_agent_os/test_methodology_catalog.py` | Test asserts full gate set, applies/not-applicable rules, maturity/complexity impact, Track 8 scenarios, artifact list, eval field list and overlaps with requirements, quality, API, accessibility, performance, release and agent workflow domains. | `python -m unittest tests.product_agent_os.test_methodology_catalog -v` fails before catalog implementation on missing frontend gates, artifacts or eval fields. |
| `T9-D6-M2` | Add RED audit recommendation coverage | `tests/product_agent_os/test_methodology_audit.py` | Tests cover missing user flow, component state matrix, reusable component docs, design-system boundary, FSD boundary, API/data contract alignment, accessibility, keyboard/focus, responsive matrix, visual/runtime evidence, interaction test evidence, performance budget, browser support, content/i18n and unsupported claims. | `python -m unittest tests.product_agent_os.test_methodology_audit -v` fails before audit implementation on missing frontend recommendations. |
| `T9-D6-M3` | Add RED discovery-signal coverage | `tests/product_agent_os/test_discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/discovery.py` | Discovery reports `frontend` signals from routes, pages, components, UI assets, Storybook, Playwright, Vite, Next/Nuxt/SvelteKit/Astro, React/Vue/Svelte/Angular/Solid, Testing Library, axe, Chromatic, tokens/themes/components metadata and UI terms. Detection remains `present_unverified`. | `python -m unittest tests.product_agent_os.test_discovery -v` fails before signal implementation and passes after. |
| `T9-D6-M4` | Fill `frontend` catalog data | `plugins/product-agent-os/assets/methodology/methodology-catalog.json` | Domain records applies/not-applicable rules, Track 8 scenarios, artifacts, all gates, eval fields, maturity/complexity impact and overlaps. Includes Storybook, FSD, accessibility, responsive, visual/runtime, performance, browser support and content/i18n gates. | Focused catalog test passes for `frontend`. |
| `T9-D6-M5` | Implement read-only audit recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py` | Audit emits prioritized recommendations with stable shape and artifact mapping for user flow, state matrix, component docs, design-system boundary, FSD, API/data contract alignment, accessibility, keyboard/focus, responsive, visual/runtime, interaction testing, performance, browser support, content/i18n and completion evidence. | Focused audit tests pass and recommendation packets keep priority, domain, gate, artifact, evidence, approval, accepted-gap and residual-risk fields. |
| `T9-D6-M6` | Add and register frontend artifact templates | `plugins/product-agent-os/assets/templates/artifact-templates/frontend-flow-spec.md`, `plugins/product-agent-os/assets/templates/artifact-templates/frontend-state-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/frontend-visual-qa.md`, `plugins/product-agent-os/assets/templates/artifact-templates/frontend-accessibility-review.md`, `plugins/product-agent-os/assets/templates/artifact-templates/frontend-performance-budget.md`, `plugins/product-agent-os/scripts/product_agent_os/templates.py` | Templates include `Source status:`, owner, evidence, accepted gap, residual risk, approval boundary, verification, rollback/no-rollback rationale, no secrets/private data guidance and renderer targets under `.codex/artifact-templates/`. | Infrastructure template tests pass and rendered templates have no unresolved substitutions. |
| `T9-D6-M7` | Map or defer extra source artifacts | `docs/sources/product-agent-os-track-9-backlog.md`, `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md` | Route inventory, Storybook story map, design-system inventory, design tokens, frontend boundary/FSD records, API dependency map, responsive matrix, keyboard/focus map, visual evidence packet, interaction matrix, browser support matrix and content/i18n record are mapped to the five templates/existing artifacts or deferred with owner and reason. | `python tools\check_docs.py` passes and backlog contains mapping/defer decisions. |
| `T9-D6-M8` | Strengthen `component-card.md` | `plugins/product-agent-os/assets/templates/artifact-templates/component-card.md`, `tests/product_agent_os/test_infrastructure_templates.py` | Component card records user flow, route/page, reusable status, design-system boundary, props/events, state matrix summary, Storybook/Autodocs/MDX links, FSD boundary, linked API contract, accessibility and owner. | Infrastructure template tests assert required frontend terms. |
| `T9-D6-M9` | Strengthen generated control-plane and eval templates | `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`, `plugins/product-agent-os/assets/templates/control-plane/TEST.md`, `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` | Generated artifacts expose frontend gates, readiness statuses, Storybook/FSD/a11y/visual/runtime/performance/browser/content evidence and completion gap handling. Behavioral evals block UI completion from code inspection, desktop-only screenshots or Storybook-only evidence. | Infrastructure and behavioral workflow eval tests pass. |
| `T9-D6-M10` | Route Frontend through lifecycle skills | `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `plugins/product-agent-os/skills/requirements-author/SKILL.md`, `plugins/product-agent-os/skills/implementation-planner/SKILL.md`, `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`, `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`, `plugins/product-agent-os/skills/docs-maintainer/SKILL.md`, `plugins/product-agent-os/skills/pr-release-operator/SKILL.md` | Skills mention Track 9 frontend recommendations as context, enforce staged-first/write approval, keep FSD/Storybook/Playwright/performance conditional, and require browser/runtime/visual/a11y evidence or explicit gaps before UI completion claims. | Lifecycle skill tests pass for shared frontend wording. |
| `T9-D6-M11` | Add fixture eval contract | `plugins/product-agent-os/scripts/run_fixture_eval.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | `frontend_contract_present` validates catalog gates, artifacts, eval fields, templates, lifecycle skill coverage and false-positive behavior. `python-app` or a dedicated frontend fixture expected checks include the new contract and renderer file count increases by five from the T9-D5 baseline if no extra templates are added. | `python plugins\product-agent-os\scripts\run_fixture_eval.py` exits `0` after implementation with expected renderer file count. |
| `T9-D6-M12` | Add positive frontend fixture | `plugins/product-agent-os/assets/fixtures/frontend-ui-app/`, `tests/product_agent_os/test_fixtures.py`, `tests/product_agent_os/test_discovery.py` | Synthetic fixture includes framework/package signals, routes/pages/components, Storybook, Playwright, Testing Library/a11y signals, design token/theme or `components.json` signal, and no secrets/private data. | Fixture completeness and discovery tests pass. |
| `T9-D6-M13` | Add false-positive and approval-bound coverage | `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | Backend-only, data-only, CLI-only, docs-only, native-only, dependency-only and simple CRUD fixtures do not force frontend gates. Public UI, reusable components, side-effecting browser automation, external visual services or production data screenshots remain approval-bound or require owner evidence. | Focused audit/discovery/fixture tests pass and existing FSD false-positive tests remain green. |
| `T9-D6-M14` | Add unsupported-claim rejection | `tests/product_agent_os/test_methodology_audit.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py` | Unsupported claims are rejected as evidence: FSD mandatory, Storybook proves quality, automated a11y addon is enough, desktop screenshot proves responsive UI, lab Web Vitals always represent production UX, and code inspection proves UI completion. | Focused audit tests assert each unsupported claim creates a frontend recommendation or owner question. |
| `T9-D6-M15` | Define Storybook adoption policy | `plugins/product-agent-os/assets/templates/artifact-templates/frontend-state-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/component-card.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Storybook is required/recommended for reusable components and design-system primitives, optional for one-off UI, and not treated as complete quality proof without state, interaction, visual/accessibility and runtime evidence. | Focused tests assert Storybook required/optional/not-applicable routing and unsupported Storybook quality claim rejection. |
| `T9-D6-M16` | Define visual evidence threshold and privacy policy | `plugins/product-agent-os/assets/templates/artifact-templates/frontend-visual-qa.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Tiny UI change, page redesign, public route and design-system primitive have proportional evidence expectations. Screenshots/stories/mocks must be privacy-safe and must not include secrets, private customer data or raw private payloads. | Focused tests assert evidence threshold terms and no-secrets/private-data terms. |
| `T9-D6-M17` | Define accessibility review policy | `plugins/product-agent-os/assets/templates/artifact-templates/frontend-accessibility-review.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Public/interactive/form-heavy UI records WCAG target or accepted gap, keyboard path, focus visibility, accessible names, semantic controls, labels, error announcements, contrast and automated-check limitations. | Focused tests assert a11y recommendation depth and automated-addon-only rejection. |
| `T9-D6-M18` | Define performance budget policy | `plugins/product-agent-os/assets/templates/artifact-templates/frontend-performance-budget.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | User-facing/performance-sensitive routes record LCP/INP/CLS target or explicit non-applicability, measurement path, lab vs field/RUM status, risk and current evidence. | Focused tests assert LCP/INP/CLS, measurement path and lab-as-production unsupported claim handling. |
| `T9-D6-M19` | Define API/data state alignment policy | `plugins/product-agent-os/assets/templates/artifact-templates/frontend-flow-spec.md`, `plugins/product-agent-os/assets/templates/artifact-templates/frontend-state-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/component-card.md`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | UI data dependency maps loading, empty, error, permission denied, auth, cache/stale, pagination and success states to contract examples or accepted gaps. | Focused tests assert API/data state terms and recommendation mapping. |
| `T9-D6-M20` | Define browser/content/i18n policy | `plugins/product-agent-os/assets/templates/artifact-templates/frontend-flow-spec.md`, `plugins/product-agent-os/assets/templates/artifact-templates/frontend-visual-qa.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Public UI names supported browsers/devices or known gaps and records long text, user-generated content, wrapping/truncation, localization, pluralization, RTL/locales and non-overlap assumptions. | Focused tests assert browser support and content/i18n terms. |
| `T9-D6-M21` | Define FSD boundary review policy | `plugins/product-agent-os/assets/templates/artifact-templates/component-card.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_infrastructure_templates.py` | FSD is conditional on project size/coupling/owner decision; when applicable it records layer, slice, segment, public API and import direction. Empty layers for small MVP remain false positives. | Focused tests assert conditional FSD and no forced FSD for MVP/backend/native/simple CRUD. |
| `T9-D6-M22` | Sync docs and control-plane evidence | `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `docs/sources/product-agent-os-track-9-backlog.md`, Product-Agent OS README/docs only when behavior is user-facing | Current state records `T9-D6` completion, RED/GREEN evidence, renderer file count delta, unsupported-claim handling, deferred artifact rationale, residual risks and next action `T9-D7`. | Full verification commands below pass; `git diff --check` exits `0`. |
| `T9-D6-M23` | Expand final verification scope | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md` | Step 6 final commands include focused T9-D6 tests, fixture eval, full unittest, transcript eval, Codex compatibility check, docs check and `git diff --check`; commit/staging remains deferred to explicit user request. | Plan review confirms no verification gap before a later `feat: integrate frontend methodology` commit. |
| `T9-D6-M24` | Record source artifact alias mapping | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, `docs/sources/product-agent-os-track-9-backlog.md`, `plugins/product-agent-os/assets/templates/artifact-templates/frontend-flow-spec.md`, `plugins/product-agent-os/assets/templates/artifact-templates/frontend-state-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/frontend-accessibility-review.md` | Source artifacts are explicitly mapped to compact Product-Agent OS templates: `ui-flow-spec.md` to `frontend-flow-spec.md`, `component-state-matrix.md` to `frontend-state-matrix.md`, and `accessibility-review.md` to `frontend-accessibility-review.md`; aliases are not treated as missing templates. | `python tools\check_docs.py` and template tests confirm alias names appear in mapping/defer evidence. |
| `T9-D6-M25` | Bring `component-card.md` under full Track 9 template contract | `plugins/product-agent-os/assets/templates/artifact-templates/component-card.md`, `tests/product_agent_os/test_infrastructure_templates.py` | Component card keeps existing FSD/Storybook sections and adds `Source status:`, owner, evidence, accepted gap, residual risk, approval boundary, verification, rollback/no-rollback rationale and no-secrets/private-data guidance. | Infrastructure template tests assert the shared template contract and frontend-specific component fields. |
| `T9-D6-M26` | Define design-system governance policy | `plugins/product-agent-os/assets/templates/artifact-templates/component-card.md`, `plugins/product-agent-os/assets/templates/artifact-templates/frontend-visual-qa.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | New primitive, token, variant, icon, typography, spacing or theme work records existing design-system reuse, owner review, variant policy, breaking component API impact and migration notes or explicit accepted gap. | Focused audit/template tests assert design-system governance terms and reject unowned token/variant additions as sufficient evidence. |
| `T9-D6-M27` | Add route/page inventory depth to frontend flow spec | `plugins/product-agent-os/assets/templates/artifact-templates/frontend-flow-spec.md`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | Frontend flow spec records route/screen, route params, data dependencies, auth/permission assumptions, SEO/meta notes where applicable, linked acceptance scenario and visible state paths. | Focused template/audit tests assert route params, auth/permission, data dependency and SEO/meta fields. |
| `T9-D6-M28` | Add state ownership boundaries | `plugins/product-agent-os/assets/templates/artifact-templates/frontend-state-matrix.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Non-trivial form, cache, route, global or persisted state records owner boundary, source of truth, cache/stale behavior, persistence risk and accepted gaps instead of only listing visible states. | Focused tests assert local, route, server-cache, global and persisted state boundary terms. |
| `T9-D6-M29` | Define runtime console and trace evidence policy | `plugins/product-agent-os/assets/templates/artifact-templates/frontend-visual-qa.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Browser/dev-server or preview evidence records URL/context, browser/OS, viewport, console/runtime status, relevant network/runtime errors, Playwright trace path where available or explicit verification gap. | Focused tests assert runtime console evidence terms and block UI completion from code inspection only. |
| `T9-D6-M30` | Define visual baseline stability policy | `plugins/product-agent-os/assets/templates/artifact-templates/frontend-visual-qa.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Visual regression evidence records baseline owner, OS/browser/hardware/rendering environment, viewport list, known noisy diffs, baseline update rule and privacy-safe screenshot/story/mock constraints. | Focused tests assert baseline stability terms and external visual-service approval boundaries. |
| `T9-D6-M31` | Expand responsive preferences, input and theme coverage | `plugins/product-agent-os/assets/templates/artifact-templates/frontend-flow-spec.md`, `plugins/product-agent-os/assets/templates/artifact-templates/frontend-visual-qa.md`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | Responsive/content evidence covers mobile and desktop plus risk-based tablet, orientation, input modality, reduced motion/preferences, theme/dark mode, long text, user-generated content and non-overlap assumptions. | Focused tests assert orientation, input modality, reduced motion/preferences and theme terms. |
| `T9-D6-M32` | Decide default accessibility target | `plugins/product-agent-os/assets/templates/artifact-templates/frontend-accessibility-review.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Public UI defaults to WCAG 2.2 AA unless owner records an accepted exception; private/internal UI still records keyboard/focus/names/semantic/errors/contrast evidence or explicit gap. | Focused tests assert WCAG 2.2 AA default, accepted exceptions and automated-addon-only rejection. |
| `T9-D6-M33` | Decide FSD auto-detection depth | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `docs/sources/product-agent-os-track-9-backlog.md`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_methodology_audit.py` | T9-D6 either implements lightweight FSD structure signal only and defers TypeScript alias/import/public API violation analysis with owner/reason, or adds bounded detection without false positives; decision is recorded. | Focused discovery/audit tests assert the selected depth and no forced FSD for small MVP/backend/native/simple CRUD. |
| `T9-D6-M34` | Refresh source registry and Product-Agent OS docs | `docs/sources/registry.md`, `docs/product-agent-os/behavioral-evals.md`, `docs/product-agent-os/scenarios.md`, `plugins/product-agent-os/README.md`, `docs/sources/product-agent-os-track-9-backlog.md` | Source-backed frontend claims are checked against registry entries, Context7 remains retrieval evidence only, user-facing Product-Agent OS docs mention frontend behavioral eval/gate coverage where appropriate, and deferred docs are recorded with reason. | `python tools\check_docs.py`, strict MkDocs when navigation changes, and docs tests pass. |

- [x] **Step 1: Add RED test for frontend gates**

Assert `frontend` gates include:

```python
[
    "frontend_user_flow_acceptance_present",
    "frontend_component_docs_present",
    "frontend_component_state_matrix_present",
    "frontend_design_system_boundary_present",
    "frontend_fsd_boundary_reviewed",
    "frontend_api_contract_alignment_present",
    "frontend_accessibility_review_present",
    "frontend_keyboard_focus_contract_present",
    "frontend_responsive_viewport_matrix_present",
    "frontend_visual_evidence_present",
    "frontend_runtime_console_evidence_present",
    "frontend_performance_budget_present",
    "frontend_browser_support_present",
    "frontend_content_i18n_boundary_present",
    "frontend_interaction_test_evidence_present",
]
```

- [x] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing frontend gates.

- [x] **Step 3: Add catalog and false-positive rules**

Rules:

- frontend applies when UI framework, components, routes, Storybook, browser assets or UI intent exist;
- frontend is `not_applicable` for backend-only, data-only, CLI-only and docs-only work;
- Storybook is recommended only when components need reusable state docs or design-system review;
- public UI defaults to accessibility and visual evidence recommendations.

- [x] **Step 4: Add templates and audit rules**

Create and register:

- `frontend-flow-spec.md`;
- `frontend-state-matrix.md`;
- `frontend-visual-qa.md`;
- `frontend-accessibility-review.md`;
- `frontend-performance-budget.md`.

Update audit rules for React/Next.js, Vue/Nuxt, Svelte/SvelteKit, Angular, Storybook and Vite signals.

- [x] **Step 5: Add false-positive fixture checks**

Ensure backend, native, docs-only and simple CRUD fixtures do not trigger frontend gates. Keep existing FSD false-positive tests passing.

- [x] **Step 6: Run verification; leave commit to explicit user request**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery -v
python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

Expected: focused tests, fixture eval, full unittest, transcript eval, compatibility check, docs check and diff hygiene pass before commit. Commit is intentionally deferred until explicitly requested in the current working branch.

---

### Task 14: T9-D7 Backend Integration

**Files:**
- Source: `docs/methodologies/backend.md`
- Modify: catalog, audit
- Create: `backend-service-overview.md`
- Create: `backend-runtime-behavior.md`
- Create: `backend-dependency-failure-matrix.md`
- Create: `backend-observability-map.md`
- Create: `backend-slo-sheet.md`
- Create: `backend-health-check-contract.md`
- Create: `backend-job-queue-contract.md`
- Create: `backend-data-consistency-record.md`
- Create: `backend-config-secrets-manifest.md`
- Create: `backend-release-rollback-notes.md`
- Create: `backend-operational-runbook.md`

Deep-audit update from `docs/methodologies/backend.md` and `docs/sources/methodology-research/backend.md`:

- The compact task list below must represent backend as runtime behavior, production failure modes, operational evidence and owner-reviewed boundaries, not as package structure or service count.
- Required gates include `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_dependency_failure_matrix_present`, `backend_observability_contract_present`, `backend_slo_or_gap_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_strategy_present`, `backend_config_secrets_boundary_present`, `backend_security_reviewed`, and `backend_rollback_plan_present`.
- Backend unit classification must cover module, monolith subsystem, service, worker, scheduler, consumer, API backend, integration adapter and migration runner. Microservices stay conditional and must not be recommended as the default maturity badge.
- Existing artifacts must be reused where possible: `architecture-overview.md`, `domain-modeling.md`, `api-contract-review.md`, `quality-strategy.md`, `test-eval-matrix.md`, `manual-qa-evidence.md`, `migration-plan.md`, `security-risk-review.md`, `release-packet.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, and `RUNLOG.md`.
- New template scope for this slice is intentionally eleven artifacts unless implementation proves a separate owner for additional candidates: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, and `backend-operational-runbook.md`.
- Candidate artifact aliases must be explicitly mapped or deferred: module/service boundary map to `backend-service-overview.md` or `architecture-overview.md`, ports/adapters map to `backend-service-overview.md`, security notes to `security-risk-review.md`, SLO ownership overlaps to Delivery/Operations, and distributed workflow recovery evidence to `backend-data-consistency-record.md` plus `backend-operational-runbook.md`.
- Discovery must recognize backend/server/service/worker/job/queue/scheduler/consumer/adapter/repository/migration directories, Docker/Procfile/docker-compose/Kubernetes/Helm/serverless manifests, OpenAPI/AsyncAPI/protobuf contracts, backend frameworks, queue/job libraries, remote dependency clients and terms such as retry, timeout, idempotency, circuit breaker, health check, readiness, liveness, SLO and runbook.
- False-positive behavior must preserve frontend-only, docs-only, CLI-only, native-only, dependency-only, package-name-only and simple CRUD work. `src/domain/*` alone, a package named `service`, or documentation about backend must not force backend gates without runtime backend evidence.
- Recommendations must reject unsupported claims as evidence: backend means only business-logic files, microservices are the professional default, retries make systems reliable, a health endpoint solves readiness, logs are observability, and SLOs only matter for large companies.
- The implementation must resolve source open questions instead of leaving them implicit: modular-monolith default, stack-specific template neutrality, platform-neutral health checks versus Kubernetes vocabulary, bounded resilience library guidance, retry/idempotency detection depth, and Backend versus Delivery ownership for SLO/runbook evidence.

#### T9-D7 Task Matrix

| ID | Task | Primary files | Критерии приемки | Verification |
| --- | --- | --- | --- | --- |
| `T9-D7-M0` | Refresh plan/backlog before implementation | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, `docs/sources/product-agent-os-track-9-backlog.md` | Deep-audit deltas are recorded: full gate set, eleven-template scope, artifact alias mapping/defer list, discovery signals, false-positive rules, unsupported claims, backend unit classification, modular-monolith policy, runtime/failure evidence and verification scope. | `python tools\check_docs.py` |
| `T9-D7-M1` | Add RED catalog contract for `backend` | `tests/product_agent_os/test_methodology_catalog.py` | Test asserts full backend gate set, applies/not-applicable rules, maturity/complexity impact, Track 8 scenarios, artifact list, eval field list and overlaps with requirements, architecture, quality, API, data, security, delivery, operations and agent workflow domains. | `python -m unittest tests.product_agent_os.test_methodology_catalog -v` fails before catalog implementation on missing backend gates, artifacts or eval fields. |
| `T9-D7-M2` | Add RED audit recommendation coverage | `tests/product_agent_os/test_methodology_audit.py` | Tests cover missing service boundary, runtime behavior, dependency failure matrix, observability, SLO/gap, health probes, job/queue contract, data consistency, config/secrets boundary, security review, rollback/replay/runbook evidence and unsupported claims. | `python -m unittest tests.product_agent_os.test_methodology_audit -v` fails before audit implementation on missing backend recommendations. |
| `T9-D7-M3` | Add RED discovery-signal coverage | `tests/product_agent_os/test_discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/discovery.py` | Discovery reports backend signals from backend/server/service/worker/job/queue/scheduler/consumer/adapter/repository/migration paths, Docker/Procfile/docker-compose/Kubernetes/Helm/serverless files, OpenAPI/AsyncAPI/protobuf contracts, framework terms, queue/job libraries, remote dependency clients and reliability terms. Detection remains `present_unverified`. | `python -m unittest tests.product_agent_os.test_discovery -v` fails before signal implementation and passes after. |
| `T9-D7-M4` | Fill `backend` catalog data | `plugins/product-agent-os/assets/methodology/methodology-catalog.json` | Domain records applies/not-applicable rules, Track 8 scenarios, artifacts, all gates, eval fields, maturity/complexity impact and overlaps. Includes runtime behavior, dependencies, observability, SLO, health, queues/jobs, data consistency, config/secrets, security and rollback gates. | Focused catalog test passes for `backend`. |
| `T9-D7-M5` | Implement read-only audit recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py` | Audit emits prioritized recommendations with stable shape and artifact mapping for boundaries, runtime behavior, dependency failures, observability, SLO/gap, health probes, queues/jobs, data consistency, config/secrets, security review, rollback/recovery/replay and completion evidence. | Focused audit tests pass and recommendation packets keep priority, domain, gate, artifact, evidence, approval, accepted-gap and residual-risk fields. |
| `T9-D7-M6` | Add and register backend artifact templates | `plugins/product-agent-os/assets/templates/artifact-templates/backend-service-overview.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-runtime-behavior.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-dependency-failure-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-observability-map.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-slo-sheet.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-health-check-contract.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-job-queue-contract.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-data-consistency-record.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-config-secrets-manifest.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-release-rollback-notes.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-operational-runbook.md`, `plugins/product-agent-os/scripts/product_agent_os/templates.py` | Templates include `Source status:`, owner, evidence, accepted gap, residual risk, approval boundary, verification, rollback/replay/recovery notes, no-secrets/private-data guidance and renderer targets under `.codex/artifact-templates/`. | Infrastructure template tests pass and rendered templates have no unresolved substitutions. |
| `T9-D7-M7` | Map or defer extra source artifacts | `docs/sources/product-agent-os-track-9-backlog.md`, `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md` | Module/service boundary map, ports/adapters map, security notes, SLO ownership, distributed workflow recovery evidence and runbook overlap are mapped to the eleven templates/existing artifacts or deferred with owner and reason. | `python tools\check_docs.py` passes and backlog contains mapping/defer decisions. |
| `T9-D7-M8` | Strengthen architecture and API overlap | `plugins/product-agent-os/assets/templates/artifact-templates/backend-service-overview.md`, `plugins/product-agent-os/assets/templates/artifact-templates/architecture-overview.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-contract-review.md`, `tests/product_agent_os/test_infrastructure_templates.py` | Backend boundary records purpose, owner, inbound contracts, outbound dependencies, data ownership, deployment/runtime shape and linked API/event contracts without duplicating API domain ownership. | Infrastructure template tests assert boundary and API/event contract terms. |
| `T9-D7-M9` | Strengthen quality and runtime verification overlap | `plugins/product-agent-os/assets/templates/artifact-templates/quality-strategy.md`, `plugins/product-agent-os/assets/templates/artifact-templates/test-eval-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/manual-qa-evidence.md`, `tests/product_agent_os/test_infrastructure_templates.py` | Backend testing guidance distinguishes unit, integration, contract, migration, job/queue, runtime and operational checks; code inspection alone is not accepted as backend completion evidence. | Focused template tests assert backend verification terms. |
| `T9-D7-M10` | Strengthen security and secrets overlap | `plugins/product-agent-os/assets/templates/artifact-templates/security-risk-review.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-config-secrets-manifest.md`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | Auth, tokens, PII, money movement, privileged operations, external writes and irreversible side effects route to risk review; docs, prompts, fixtures and logs must not include secrets or private customer data. | Focused audit/template tests assert security-sensitive routing and no-secrets terms. |
| `T9-D7-M11` | Strengthen generated control-plane and eval templates | `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`, `plugins/product-agent-os/assets/templates/control-plane/TEST.md`, `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` | Generated artifacts expose backend gates, readiness statuses, runtime/failure/observability/SLO/health/job/consistency/security/rollback evidence and accepted-gap handling. Behavioral evals block backend completion from package docs, logs-only observability or health-endpoint-only readiness. | Infrastructure and behavioral workflow eval tests pass. |
| `T9-D7-M12` | Route Backend through lifecycle skills | `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `plugins/product-agent-os/skills/requirements-author/SKILL.md`, `plugins/product-agent-os/skills/implementation-planner/SKILL.md`, `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`, `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`, `plugins/product-agent-os/skills/docs-maintainer/SKILL.md`, `plugins/product-agent-os/skills/pr-release-operator/SKILL.md` | Skills mention Track 9 backend recommendations as context, keep microservices/resilience/tooling conditional, enforce staged-first/write approval and require runtime/failure/observability/security/rollback evidence or explicit gaps before backend completion claims. | Lifecycle skill tests pass for shared backend wording. |
| `T9-D7-M13` | Add fixture eval contract | `plugins/product-agent-os/scripts/run_fixture_eval.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | `backend_contract_present` validates catalog gates, artifacts, eval fields, templates, lifecycle skill coverage and false-positive behavior. Renderer file count increases by eleven from the T9-D6 baseline if no extra templates are added. | `python plugins\product-agent-os\scripts\run_fixture_eval.py` exits `0` after implementation with expected renderer file count. |
| `T9-D7-M14` | Add positive backend fixture | `plugins/product-agent-os/assets/fixtures/backend-service-app/`, `tests/product_agent_os/test_fixtures.py`, `tests/product_agent_os/test_discovery.py` | Synthetic fixture includes framework/API signal, runtime entrypoint, worker or queue signal, health probe, Docker or platform manifest, dependency client, observability/runbook evidence and no secrets/private data. | Fixture completeness and discovery tests pass. |
| `T9-D7-M15` | Add false-positive and approval-bound coverage | `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | Frontend-only, docs-only, CLI-only, native-only, dependency-only, package-name-only and simple CRUD fixtures do not force backend gates. Production data, external writes, hosted dependency introspection and real secrets remain approval-bound or require owner evidence. | Focused audit/discovery/fixture tests pass and existing non-backend false-positive tests remain green. |
| `T9-D7-M16` | Add unsupported-claim rejection | `tests/product_agent_os/test_methodology_audit.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py` | Unsupported claims are rejected as evidence: backend means only business logic files, microservices are the professional default, retries make systems reliable, a health endpoint solves readiness, logs are observability and SLOs only matter for large companies. | Focused audit tests assert each unsupported claim creates a backend recommendation or owner question. |
| `T9-D7-M17` | Define modular-monolith and microservices policy | `plugins/product-agent-os/assets/templates/artifact-templates/backend-service-overview.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Modular monolith boundaries are the default recommendation until independent deploy/scale/team/ownership evidence justifies microservices; microservices require explicit owner review and migration/rollback notes. | Focused tests assert default/conditional microservices routing. |
| `T9-D7-M18` | Define Ports and Adapters / DDD boundary policy | `plugins/product-agent-os/assets/templates/artifact-templates/backend-service-overview.md`, `plugins/product-agent-os/assets/templates/artifact-templates/domain-modeling.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | Domain logic independent from HTTP/DB/queue/vendor SDK concerns records ports/adapters boundary; complex domain changes link bounded context and ubiquitous language artifacts or accepted gaps. | Focused tests assert ports/adapters and DDD overlap terms. |
| `T9-D7-M19` | Define runtime/retry/idempotency/backpressure policy | `plugins/product-agent-os/assets/templates/artifact-templates/backend-runtime-behavior.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Retry/queue/job/distributed workflow evidence records timeout, backoff, max attempts, idempotency, deduplication, ordering, backpressure, replay and recovery or explicit accepted gaps. | Focused tests assert runtime and resilience terms. |
| `T9-D7-M20` | Define dependency failure policy | `plugins/product-agent-os/assets/templates/artifact-templates/backend-dependency-failure-matrix.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Each remote dependency records timeout, retry, circuit breaker or non-applicability, fallback, alert, owner and verification evidence. | Focused tests assert dependency failure matrix depth. |
| `T9-D7-M21` | Define job/queue/DLQ/replay policy | `plugins/product-agent-os/assets/templates/artifact-templates/backend-job-queue-contract.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Background jobs, queues, consumers and schedulers record payload contract, retry policy, dead-letter behavior, idempotency key, replay procedure and poison-message handling. | Focused tests assert job/queue contract terms. |
| `T9-D7-M22` | Define data consistency and saga policy | `plugins/product-agent-os/assets/templates/artifact-templates/backend-data-consistency-record.md`, `plugins/product-agent-os/assets/templates/artifact-templates/migration-plan.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Risky distributed data behavior records local transaction, outbox, saga, compensation, monitoring, reconciliation, migration impact and recovery path. | Focused tests assert data consistency and migration overlap. |
| `T9-D7-M23` | Define observability and no-secrets logging policy | `plugins/product-agent-os/assets/templates/artifact-templates/backend-observability-map.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Observability records traces, metrics, logs, correlation IDs, alert ownership and explicit no-secrets/no-private-payload logging constraints. Logs alone are not accepted as observability. | Focused tests assert observability depth and logs-only rejection. |
| `T9-D7-M24` | Define SLO, health and operations policy | `plugins/product-agent-os/assets/templates/artifact-templates/backend-slo-sheet.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-health-check-contract.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-operational-runbook.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Production/user-facing backend records SLI/SLO or explicit gap, health endpoint semantics, liveness/readiness/startup or platform equivalents, operational owner, escalation path and handoff to Delivery/Operations. | Focused tests assert SLO/gap, health semantics and operational runbook terms. |
| `T9-D7-M25` | Define rollback, release and recovery policy | `plugins/product-agent-os/assets/templates/artifact-templates/backend-release-rollback-notes.md`, `plugins/product-agent-os/assets/templates/workflows/release-packet.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Risky backend changes record rollback trigger, rollback command or manual procedure, data recovery/replay path, irreversible side effects, owner approval and residual risk. | Focused tests assert rollback/recovery/replay evidence. |
| `T9-D7-M26` | Sync docs and control-plane evidence | `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `docs/sources/product-agent-os-track-9-backlog.md`, Product-Agent OS README/docs only when behavior is user-facing | Current state records incremental `T9-D7` batch evidence, RED/GREEN evidence, renderer file count delta, unsupported-claim handling, deferred artifact rationale, residual risks and next backend batch. Final `T9-D7` completion and next action `T9-D8` remain deferred until rows `T9-D7-M40..M45` are complete. | Batch verification commands pass; `git diff --check` exits `0`; final closure verification still runs after the remaining backend rows. |
| `T9-D7-M27` | Expand final verification scope | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md` | Step 6 final commands include focused T9-D7 tests, fixture eval, full unittest, transcript eval, Codex compatibility check, docs check and `git diff --check`; commit/staging remains deferred to explicit user request. This batch may run the same commands as fresh evidence, but does not claim final `T9-D7` closure while `T9-D7-M40..M45` remain open. | Plan review confirms no verification gap before a later `feat: integrate backend methodology` commit. |
| `T9-D7-M28` | Add Twelve-Factor service discipline depth | `plugins/product-agent-os/assets/templates/artifact-templates/backend-service-overview.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-config-secrets-manifest.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-runtime-behavior.md`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | Backend guidance records config, dependencies, build-release-run boundary, process model, admin tasks, dev/prod parity and logs-as-event-stream vocabulary without turning Twelve-Factor into a mandatory framework. | Focused template/audit tests assert Twelve-Factor depth and conditional wording. |
| `T9-D7-M29` | Require service boundary owner review and ADR routing | `plugins/product-agent-os/assets/templates/artifact-templates/backend-service-overview.md`, `plugins/product-agent-os/assets/templates/artifact-templates/adr.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | New or changed backend responsibility records owner review, decision authority, boundary rationale and ADR link or accepted gap. Service boundary changes without owner review or ADR produce a recommendation. | Focused tests assert owner-review and ADR routing for boundary changes. |
| `T9-D7-M30` | Add requirements-author backend intake fields | `plugins/product-agent-os/skills/requirements-author/SKILL.md`, `plugins/product-agent-os/assets/templates/control-plane/REQUIREMENTS.md`, `tests/product_agent_os/test_lifecycle_skills.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Requirements intake records service/user behavior, non-goals, runtime constraints, affected backend unit, dependencies, data stores, operational assumptions and explicit gaps before implementation planning. | Lifecycle and template tests assert backend intake terms. |
| `T9-D7-M31` | Deepen security notes coverage | `plugins/product-agent-os/assets/templates/artifact-templates/security-risk-review.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-config-secrets-manifest.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Security-sensitive backend notes distinguish authn/authz, secrets, rate limits, audit logging, sensitive data, abuse cases, privileged operations and no-secrets evidence. | Focused audit/template tests assert security-note depth. |
| `T9-D7-M32` | Deepen observability contract | `plugins/product-agent-os/assets/templates/artifact-templates/backend-observability-map.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Observability template records traces, metrics, logs, dashboards, alerts, correlation IDs, context propagation, semantic conventions or accepted gaps, collector/instrumentation notes and redaction policy. | Focused tests assert observability depth beyond logs. |
| `T9-D7-M33` | Deepen SLO sheet fields | `plugins/product-agent-os/assets/templates/artifact-templates/backend-slo-sheet.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | SLO sheet records user journey, user-relevant SLI, SLO target, measurement window, alert policy, owner and explicit no-telemetry or not-yet-production gap. | Focused tests assert SLO field depth and no-telemetry gap wording. |
| `T9-D7-M34` | Add health-check verification policy | `plugins/product-agent-os/assets/templates/artifact-templates/backend-health-check-contract.md`, `plugins/product-agent-os/assets/templates/control-plane/TEST.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Health checks are tested where the platform/runtime is available, or the artifact records a platform-unavailable gap with owner, reason and follow-up. Documentation alone is not sufficient for deployable services. | Focused tests assert health verification or accepted gap. |
| `T9-D7-M35` | Deepen operational runbook coverage | `plugins/product-agent-os/assets/templates/artifact-templates/backend-operational-runbook.md`, `plugins/product-agent-os/assets/templates/workflows/release-packet.md`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | Runbook records common failures, dashboard links, log/query links or placeholders, recovery steps, escalation path, owner, severity assumptions and evidence freshness. | Focused tests assert runbook depth and operational handoff terms. |
| `T9-D7-M36` | Deepen config/secrets manifest coverage | `plugins/product-agent-os/assets/templates/artifact-templates/backend-config-secrets-manifest.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Manifest records env/config keys without values, secret source, rotation notes, local/prod parity, required/optional status, owner and no-secrets/no-private-data constraints for docs, prompts, fixtures, logs and examples. | Focused tests assert config/secrets field depth and secret redaction. |
| `T9-D7-M37` | Deepen release rollback notes | `plugins/product-agent-os/assets/templates/artifact-templates/backend-release-rollback-notes.md`, `plugins/product-agent-os/assets/templates/workflows/release-packet.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Release notes cover migration, feature flag, rollback trigger, rollback or no-rollback rationale, replay, data recovery, verification command, owner approval and residual risk. | Focused tests assert feature-flag, migration, replay and data-recovery terms. |
| `T9-D7-M38` | Add contract-aware backend development depth | `plugins/product-agent-os/assets/templates/artifact-templates/backend-service-overview.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-contract-review.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-job-queue-contract.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Backend contract evidence includes APIs/events/external providers and references OpenAPI, AsyncAPI, Pact, protobuf or provider contracts where applicable; contract changes must stay synced with code and tests. | Focused tests assert Pact/provider contract and API/event sync terms. |
| `T9-D7-M39` | Expand backend dependency discovery categories | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `tests/product_agent_os/test_discovery.py`, `plugins/product-agent-os/assets/fixtures/backend-service-app/` | Discovery distinguishes DB, message broker, cache, payment, email, storage, search and third-party HTTP/provider clients as backend dependency signals while keeping detection `present_unverified`. | Discovery tests assert dependency categories and false-positive behavior. |
| `T9-D7-M40` | Add CI/deployment command discovery and routing | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_lifecycle_skills.py` | Workspace discovery records backend stack, commands, CI, APIs, DB, queues, workers, deployment manifests and security signals without executing deployments or external writes. | Discovery/lifecycle tests assert command and deployment signal wording. |
| `T9-D7-M41` | Define backend severity policy | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `plugins/product-agent-os/assets/templates/evals/project-readiness.json` | Risky production backend without service boundary, runtime/failure evidence, security route or rollback is blocker/high-risk; missing SLO, health verification, observability or owner review is high-risk unless accepted gap is recorded; simple local/backend-light work stays warning or not applicable. | Focused audit/readiness tests assert severity levels and accepted-gap downgrade behavior. |
| `T9-D7-M42` | Decide stack-specific backend snippets policy | `plugins/product-agent-os/assets/templates/artifact-templates/backend-service-overview.md`, `plugins/product-agent-os/assets/templates/artifact-templates/backend-runtime-behavior.md`, `docs/sources/product-agent-os-track-9-backlog.md`, `tests/product_agent_os/test_infrastructure_templates.py` | T9-D7 templates stay framework-agnostic; Node.js, Python, Java, .NET and Go snippets are deferred until separate stack-specific research proves owner, examples and verification. | Template/docs tests assert framework-agnostic wording and backlog records snippet deferral. |
| `T9-D7-M43` | Decide retry/idempotency detection depth | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `docs/sources/product-agent-os-track-9-backlog.md`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_methodology_audit.py` | T9-D7 uses lightweight read-only signals for retry/idempotency terms and dependency/job context; deeper static analysis of retry correctness is deferred with owner/reason to avoid false positives. | Focused tests assert lightweight detection and backlog deferral. |
| `T9-D7-M44` | Refresh source registry and Product-Agent OS docs | `docs/sources/registry.md`, `docs/product-agent-os/behavioral-evals.md`, `docs/product-agent-os/scenarios.md`, `plugins/product-agent-os/README.md`, `docs/sources/product-agent-os-track-9-backlog.md` | Source-backed backend claims are checked against existing registry entries, user-facing Product-Agent OS docs mention backend behavioral eval/gate coverage where appropriate, and any deferred docs are recorded with reason. | `python tools\check_docs.py`, strict MkDocs when navigation changes and docs tests pass. |
| `T9-D7-M45` | Route semantic evidence sufficiency to shared owner-review backlog | `docs/sources/product-agent-os-track-9-backlog.md`, `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Backend completion evidence records whether owner reviewed test/eval/runtime evidence sufficiency for the real project risk, or captures accepted gap with owner, reason, review date, downstream risk and follow-up. Full shared semantic sufficiency normalization remains owned by cross-domain backlog/T9-S. | Focused tests assert routing without pretending T9-D7 fully solves cross-domain owner approval. |

- [x] **Step 1: Add RED test for backend gates**

Assert `backend` gates include:

```python
[
    "backend_service_boundary_present",
    "backend_runtime_behavior_present",
    "backend_dependency_failure_matrix_present",
    "backend_observability_contract_present",
    "backend_slo_or_gap_present",
    "backend_health_probe_contract_present",
    "backend_job_queue_contract_present",
    "backend_data_consistency_strategy_present",
    "backend_config_secrets_boundary_present",
    "backend_security_reviewed",
    "backend_rollback_plan_present",
]
```

- [x] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing backend gates.

- [x] **Step 3: Add backend catalog and recommendations**

Rules:

- default recommendation favors modular monolith boundaries before microservices;
- microservices require independent scaling/team/deploy evidence;
- retries, queues, jobs and distributed workflows require idempotency, timeout, replay and recovery evidence;
- auth, money, sensitive data and irreversible side effects route through risk review.

- [x] **Step 4: Add templates and discovery signals**

Create all backend templates listed in Files. Detect:

- `src/server`, `app/main.py`, `fastapi`, `express`, `django`, `flask`, `spring`, `.NET`, `go.mod`;
- `Dockerfile`, `Procfile`, `docker-compose.yml`, `k8s/*.yaml`;
- queue/job signals in `celery`, `bull`, `rq`, `sidekiq`, `cron`, `worker`.

- [x] **Step 5: Add false-positive checks**

Docs-only and frontend-only fixtures must not trigger backend service boundary gates.

- [x] **Step 6: Run verification; leave commit to explicit user request**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery -v
python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

Expected: focused tests, fixture eval, full unittest, transcript eval, compatibility check, docs check and diff hygiene pass before commit. Commit is intentionally deferred until explicitly requested in the current working branch.

---

### Task 15: T9-D8 API & Integrations Integration

**Files:**
- Source: `docs/methodologies/api-integrations.md`
- Modify: catalog, audit, `api-contract-review.md`, `migration-plan.md`
- Create: `api-inventory.md`
- Create: `api-error-catalog.md`
- Create: `api-auth-authorization-matrix.md`
- Create: `api-consumer-map.md`
- Create: `api-compatibility-record.md`
- Create: `api-contract-test-matrix.md`
- Create: `generated-sdk-manifest.md`
- Create: `webhook-event-contract.md`
- Create: `external-integration-approval.md`
- Create: `api-style-guide.md`

Deep-audit update from `docs/methodologies/api-integrations.md` and `docs/sources/methodology-research/api-integrations.md`:

- The compact task list below must use the full API & Integrations source contract, not only the initial subset.
- `api_contract_test_matrix_present` is a derived Product-Agent OS gate for Track 9 implementation. The methodology source lists `api-contract-test-matrix.md` and contract verification as artifact/eval evidence; implementation must make this explicit so schema validation, provider verification and consumer-driven tests are not collapsed into "contract file exists".
- API-only contract fixtures must not force Backend runtime blockers. OpenAPI/AsyncAPI/GraphQL/protobuf/Pact files make `api_integrations` applicable, but Backend gates require runtime/server/service/worker evidence.
- Unsupported claims must be rejected as evidence: rendered API docs are enough, internal APIs do not need compatibility review, schema validation is the same as contract testing, GraphQL/gRPC/event-driven is always better, OAuth means API security is handled, and generated SDKs are mechanical.
- External writes remain approval-bound. T9-D8 may stage `external-integration-approval.md`, but must not perform external writes, update external systems, run generated client publication, or mutate provider state without explicit approval.
- Final verification must not auto-commit. Commit remains a separate user-approved action, matching the recent T9-D5 through T9-D7 execution pattern.

#### T9-D8 Task Matrix

| ID | Task | Primary files | Критерии приемки | Verification |
| --- | --- | --- | --- | --- |
| `T9-D8-M0` | Refresh plan and backlog before implementation | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, `docs/sources/product-agent-os-track-9-backlog.md` | Deep-audit deltas are recorded: derived contract-test matrix gate, API-only/backend false-positive risk, no universal API style, Swagger UI not source of truth, external write approval boundary, unsupported claims and verification without implicit commit. | `python tools\check_docs.py` passes after documentation edits. |
| `T9-D8-M1` | Add RED catalog contract for `api_integrations` | `tests/product_agent_os/test_methodology_catalog.py` | Test asserts API gates, artifact list, explicit eval fields, applies/not-applicable rules, maturity/complexity impact, Track 8 scenarios and overlaps with quality, security, backend, delivery and data. | `python -m unittest tests.product_agent_os.test_methodology_catalog -v` fails before catalog implementation on missing API gates or eval fields. |
| `T9-D8-M2` | Add RED audit recommendation coverage | `tests/product_agent_os/test_methodology_audit.py` | Tests cover OpenAPI, AsyncAPI, GraphQL, protobuf, Pact, public breaking changes, internal API with consumers, webhook/event delivery, generated SDK, auth/error contract and external write approval recommendations. | `python -m unittest tests.product_agent_os.test_methodology_audit -v` fails before API audit implementation on missing recommendations. |
| `T9-D8-M3` | Add API false-positive and unsupported-claim tests | `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | Swagger UI/rendered docs alone is not source of truth, GraphQL/gRPC/events are not universal defaults, schema validation is not contract testing, OAuth alone is not security, internal APIs can still have consumers, and OpenAPI-only fixtures do not force Backend runtime P0 gates. | Focused audit/discovery/fixture tests fail before false-positive routing exists. |
| `T9-D8-M4` | Expand read-only API discovery signals | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_methodology_audit.py` | Discovery records OpenAPI, AsyncAPI, GraphQL schema, `.proto`, Pact/contract tests, webhooks/events/queues, SDK/generated clients, external providers, OAuth/scopes/token/rate-limit/error/deprecation/compatibility terms as `present_unverified` evidence. | Focused discovery and audit tests assert signal packets without executing tools or external writes. |
| `T9-D8-M5` | Fill `api_integrations` catalog data | `plugins/product-agent-os/assets/methodology/methodology-catalog.json` | Domain records applies/not-applicable rules, maturity/complexity impact, Track 8 scenarios, decision horizons, artifacts, all gates, eval fields and overlaps for quality, security, backend, data, delivery, frontend and architecture. | Focused catalog test passes for `api_integrations`. |
| `T9-D8-M6` | Implement API recommendation router | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | `_api_integrations_recommendations(...)` emits stable packets for contract source, consumer map, breaking review, error contract, security review, contract-test matrix, event delivery, generated client manifest and external write approval. | Focused audit tests pass and recommendation packets keep stable shape. |
| `T9-D8-M7` | Define API severity and accepted-gap policy | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, `tests/product_agent_os/test_methodology_audit.py` | Public, breaking, external-write, security, event and SDK gaps are high-risk or blocker as appropriate; simple local/internal prototype work can be `P2_recommended`, `not_applicable` or `explicit_gap_accepted` only with owner, reason, residual risk and follow-up. | Focused audit/readiness tests assert priority levels and accepted-gap downgrade behavior. |
| `T9-D8-M8` | Add API artifact templates | `plugins/product-agent-os/assets/templates/artifact-templates/api-inventory.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-error-catalog.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-auth-authorization-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-consumer-map.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-compatibility-record.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-contract-test-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/generated-sdk-manifest.md`, `plugins/product-agent-os/assets/templates/artifact-templates/webhook-event-contract.md`, `plugins/product-agent-os/assets/templates/artifact-templates/external-integration-approval.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-style-guide.md` | Templates include `Source status:`, owner, source-of-truth contract, status, evidence, accepted gap, residual risk, approval boundary, verification command/gap and no secrets/private data guidance. | Infrastructure template tests pass for required API terms and unresolved substitutions. |
| `T9-D8-M9` | Strengthen existing API and migration templates | `plugins/product-agent-os/assets/templates/artifact-templates/api-contract-review.md`, `plugins/product-agent-os/assets/templates/artifact-templates/migration-plan.md`, `tests/product_agent_os/test_infrastructure_templates.py` | Existing templates cover spec versions, JSON Schema dialect, RFC 9457 errors, OAuth/OWASP API risks, GraphQL complexity/deprecation/auth, gRPC/protobuf, SDK versioning, contract check command, staged external-write approval and release/rollback impact. | Infrastructure template tests assert the strengthened terms. |
| `T9-D8-M10` | Register API templates in renderer | `plugins/product-agent-os/scripts/product_agent_os/templates.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `plugins/product-agent-os/assets/templates/evals/renderer-fixtures.json` | All new API templates render to `.codex/artifact-templates/<name>`, `REQUIRED_TARGETS` includes them once, and renderer file count increases by ten from the T9-D7 baseline if no other templates are added. | Infrastructure and fixture eval tests pass with the updated renderer file count. |
| `T9-D8-M11` | Route API methodology through lifecycle skills | `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `plugins/product-agent-os/skills/implementation-planner/SKILL.md`, `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`, `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`, `plugins/product-agent-os/skills/pr-release-operator/SKILL.md`, `plugins/product-agent-os/skills/docs-maintainer/SKILL.md` | Skills require contract source, consumer map, compatibility classification, error/security/event/SDK/external-write evidence, staged-first approval and no compatibility/security/release claims from inspection alone. | Lifecycle skill tests pass for API methodology wording. |
| `T9-D8-M12` | Strengthen generated control-plane and eval templates | `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`, `plugins/product-agent-os/assets/templates/control-plane/TEST.md`, `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` | Generated artifacts expose API gates, readiness statuses, contract/source/consumer/compatibility/auth/error/event/SDK/external-write evidence and accepted-gap handling. Behavioral evals block API completion from rendered docs, OAuth-only claims or schema-only checks. | Infrastructure and behavioral workflow eval tests pass. |
| `T9-D8-M13` | Add API fixture eval contract | `plugins/product-agent-os/scripts/run_fixture_eval.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | `api_integrations_contract_present`, `api_contract_source_present` and `external_write_approval_present` checks validate catalog gates, artifacts, eval fields, templates, lifecycle skill coverage and API false-positive behavior. | `python plugins\product-agent-os\scripts\run_fixture_eval.py` exits `0` after implementation with expected API checks. |
| `T9-D8-M14` | Add API positive and negative fixtures | `plugins/product-agent-os/assets/fixtures/api-migration-repo/`, `plugins/product-agent-os/assets/fixtures/api-external-write-approval/`, `plugins/product-agent-os/assets/fixtures/swagger-ui-only-api-docs/`, `plugins/product-agent-os/assets/fixtures/graphql-grpc-style-choice/`, `tests/product_agent_os/test_fixtures.py`, `tests/product_agent_os/test_discovery.py` | Synthetic fixtures cover richer API migration, external-write approval, rendered-docs-only negative routing and GraphQL/gRPC style-choice non-default behavior. Fixtures remain synthetic and contain no secrets, tokens, private data or external-system credentials. | Fixture completeness and discovery tests pass. |
| `T9-D8-M15` | Sync docs and backlog evidence | `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `docs/sources/product-agent-os-track-9-backlog.md`, `plugins/product-agent-os/README.md`, `docs/product-agent-os/behavioral-evals.md`, `docs/product-agent-os/scenarios.md` | Current state records `T9-D8` completion, RED/GREEN evidence, renderer file count delta, unsupported-claim handling, API-only/backend false-positive handling, external-write approval boundary, residual risks and next action `T9-D9`. | `python tools\check_docs.py` passes; strict MkDocs runs only if navigation, Mermaid, Markdown extensions, MkDocs config or docs navigation changed. |
| `T9-D8-M16` | Sync source registry and operator docs tests | `docs/sources/registry.md`, `tests/product_agent_os/test_product_agent_os_docs.py`, `docs/product-agent-os/behavioral-evals.md`, `docs/product-agent-os/scenarios.md` | Source registry records the T9-D8 API & Integrations coverage, operator docs expose API methodology routing/eval expectations, and no new navigation page is introduced without MkDocs/docs-check updates. | `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` and `python tools\check_docs.py` pass. |
| `T9-D8-M17` | Add JSON Schema and contract-source detection depth | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_methodology_audit.py` | Discovery and audit treat JSON Schema files, schema folders, schema dialect declarations and Pact/contract sources as API contract evidence. JSON Schema stays `present_unverified` until dialect, owner and compatibility evidence exist. | Focused discovery/audit tests assert JSON Schema contract-source detection and dialect/gap handling. |
| `T9-D8-M18` | Add API inventory lifecycle and contract-drift policy | `plugins/product-agent-os/assets/templates/artifact-templates/api-inventory.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-compatibility-record.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | API inventory records provider, consumers, owners, generated clients, runtime environments, lifecycle state (`draft`, `experimental`, `stable`, `deprecated`, `removed`), compatibility policy and deprecation path. Contract drift between source, code and generated docs blocks completion claims or records an accepted gap. | Focused template/audit tests assert lifecycle states, runtime environments and contract-drift recommendation routing. |
| `T9-D8-M19` | Deepen API examples and error model evidence | `plugins/product-agent-os/assets/templates/artifact-templates/api-error-catalog.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-contract-review.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | Error evidence requires success, validation failure, auth failure and important domain failure examples. HTTP APIs record RFC 9457 Problem Details or compatibility reason for a different error model, with status codes, error types, extensions and examples. | Focused template/audit tests assert example coverage and Problem Details or explicit compatibility gap. |
| `T9-D8-M20` | Add API observability and integration alert evidence | `plugins/product-agent-os/assets/templates/artifact-templates/api-contract-review.md`, `plugins/product-agent-os/assets/templates/artifact-templates/integration-catalog.md`, `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | API/integration changes record request IDs, correlation IDs, error counters, latency, rate-limit metrics and integration failure alerts or an explicit not-applicable/accepted gap. Observability is API-level evidence, not only Backend/Delivery overlap. | Focused template/audit/readiness tests assert API observability terms and gap handling. |
| `T9-D8-M21` | Link API security schemes to contracts | `plugins/product-agent-os/assets/templates/artifact-templates/api-auth-authorization-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-contract-review.md`, `plugins/product-agent-os/assets/templates/artifact-templates/security-risk-review.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | Security review requires contract-linked OpenAPI security schemes, GraphQL auth or equivalent scheme evidence, scopes, token claims, object-level authorization, rate limits, sensitive fields and abuse cases. Prose-only security notes are unsupported evidence. | Focused template/audit tests assert security scheme linkage and prose-only rejection. |
| `T9-D8-M22` | Add generated SDK reproducibility and multi-repo impact policy | `plugins/product-agent-os/assets/templates/artifact-templates/generated-sdk-manifest.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-consumer-map.md`, `plugins/product-agent-os/assets/templates/artifact-templates/migration-plan.md`, `docs/sources/product-agent-os-track-9-backlog.md`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | Generated SDK evidence records generator, version, config, target languages, owner, regeneration command, reviewable diff, SemVer impact and release process. Multi-repository generated client handling is deferred with owner/reason unless the current fixture proves a safe in-repo flow. | Focused template/audit tests assert reproducibility/reviewable diff terms and backlog records multi-repo deferral. |
| `T9-D8-M23` | Deepen webhook and event contract envelope policy | `plugins/product-agent-os/assets/templates/artifact-templates/webhook-event-contract.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-contract-review.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | Event/webhook evidence records schema, headers, signature verification, correlation ID, idempotency key, retry policy, ordering guarantee, replay, dead-letter behavior and CloudEvents applicability or explicit non-applicability. | Focused template/audit tests assert envelope, signature, replay/DLQ and CloudEvents terms. |
| `T9-D8-M24` | Record API tooling and compatibility-rule deferrals | `docs/sources/product-agent-os-track-9-backlog.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-style-guide.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-contract-test-matrix.md`, `tests/product_agent_os/test_infrastructure_templates.py` | T9-D8 does not pick Spectral, Redocly, framework-native lint, schema compatibility rules, API security profile or test generator as a universal default. Backlog records deferred decisions for API lint tooling, JSON Schema/protobuf/GraphQL/AsyncAPI compatibility rules, API security profile and stack-specific contract test generators. | Template/docs tests assert no forced tooling default and backlog records deferral owner/reason. |
| `T9-D8-M25` | Run final T9-D8 verification without implicit commit | `tests/product_agent_os/`, `plugins/product-agent-os/scripts/run_fixture_eval.py`, `plugins/product-agent-os/scripts/run_transcript_eval.py`, `plugins/product-agent-os/scripts/validate_codex_compatibility.py`, `tools/check_docs.py` | Focused catalog/audit/discovery/template/fixture tests, fixture eval, full unittest, transcript eval, compatibility check, docs check and diff hygiene pass before any commit. Commit remains deferred until explicitly requested. | Run the Step 6 verification commands below and record exact results in `RUNLOG.md` when implementation is complete. |

- [ ] **Step 1: Add RED test for API gates**

Assert `api_integrations` gates include:

```python
[
    "api_contract_source_present",
    "api_consumer_map_present",
    "api_breaking_change_reviewed",
    "api_error_contract_present",
    "api_security_reviewed",
    "api_contract_test_matrix_present",
    "event_delivery_contract_present",
    "generated_client_manifest_present",
    "external_write_approval_present",
]
```

- [ ] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing API gates.

- [ ] **Step 3: Add API catalog and rules**

Rules:

- do not choose REST, GraphQL, gRPC or events as universal default;
- public contract changes trigger two-stage review;
- external writes require staged draft, approval and rollback path;
- Swagger UI alone is not source of truth;
- OpenAPI/AsyncAPI/protobuf/GraphQL schemas are `present_unverified` until owner and contract checks exist.

- [ ] **Step 4: Add templates and discovery signals**

Create all API templates listed in Files. Detect OpenAPI, AsyncAPI, GraphQL, `.proto`, Pact, webhook, SDK and external provider signals.

- [ ] **Step 5: Add fixture eval checks**

Existing `api-migration-repo` must expose:

- `api_integrations_contract_present`;
- `api_contract_source_present`;
- `external_write_approval_present` when external write terms appear.

- [ ] **Step 6: Run verification; leave commit to explicit user request**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_fixture_eval_runner -v
python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixtures -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

Expected: focused tests, fixture eval, full unittest, transcript eval, compatibility check, docs check and diff hygiene pass before commit. Commit is intentionally deferred until explicitly requested in the current working branch.

---

### Task 16: T9-D9 Database & Data Integration

**Files:**
- Source: `docs/methodologies/database-data.md`
- Modify: catalog, audit, `database-dictionary.md`, `data-migration.md`
- Create: `database-inventory.md`
- Create: `database-migration-plan.md`
- Create: `database-expand-contract-record.md`
- Create: `database-backfill-runbook.md`
- Create: `database-rollback-feasibility.md`
- Create: `database-backup-restore-evidence.md`
- Create: `database-data-classification-matrix.md`
- Create: `database-data-quality-checks.md`
- Create: `database-data-contract.md`
- Create: `database-lineage-map.md`
- Create: `database-query-performance-review.md`
- Create: `database-retention-deletion-policy.md`
- Create: `database-synthetic-fixtures-policy.md`
- Create: `database-production-access-approval.md`

Deep-audit update from `docs/methodologies/database-data.md` and `docs/sources/methodology-research/database-data.md`:

- `database_data` is currently a stub in the methodology catalog; implementation must promote it to a full domain, not only extend the existing `data_migration` usage-mode workflow.
- Database methodology applies beyond SQL migrations: schema source, data dictionary, migration/backfill safety, transaction/concurrency design, constraints/indexes, query performance, backup/restore, data quality, retention/deletion, lineage, privacy classification, synthetic fixtures and production data access are separate gates.
- Tooling choices are candidates, not defaults. T9-D9 must not force PostgreSQL, Liquibase, Flyway, Alembic, Prisma, Rails/Django migrations, dbt, Great Expectations, OpenLineage, DBML, dbdocs, SchemaSpy or schema-diff tooling as universal Product-Agent OS defaults.
- DB introspection, production DB access, production data access, migration execution, destructive cleanup, backup restore and retention mutation remain `approval_required`.
- SQL/ORM destructive-change detection must be lightweight and conservative: `DROP`, rename, truncate, destructive cleanup and unsafe retention signals create owner questions/recommendations, not automatic execution or full parser claims.
- Unsupported claims must be rejected as evidence: ORM schema is the database source of truth, migration applied means migration safe, rollback is just down migration, backups exist so restore is safe, manual SQL is enough, anonymized production data is safe by default and lineage can be reconstructed later.
- Analytics and AI/RAG data movement creates cross-domain overlap with `llm_ai_rag`; PII/sensitive/production data creates overlap with Security/Privacy; schema/API/data contract changes overlap with API, Backend, Quality and Delivery.

#### T9-D9 Task Matrix

| ID | Task | Files | Критерии приемки | Verification |
| --- | --- | --- | --- | --- |
| `T9-D9-M0` | Refresh plan and backlog before implementation | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, `docs/sources/product-agent-os-track-9-backlog.md` | Deep-audit deltas are recorded: database domain is not a workflow-only gate; production data never enters prompts/docs/templates/fixtures; DB introspection and production access are approval-bound; tooling defaults are deferred; destructive detection is conservative; unsupported claims are named. | `python tools\check_docs.py` passes after documentation edits. |
| `T9-D9-M1` | Add RED catalog contract for `database_data` | `tests/product_agent_os/test_methodology_catalog.py` | Test asserts applies/not-applicable rules, maturity/complexity impact, Track 8 scenarios, decision horizons, overlaps, artifacts, eval fields and database gates for inventory, dictionary, schema source, migration plan, expand/contract, transactions, rollback, backup/restore, classification, data quality, lineage, performance, retention/deletion, synthetic fixtures, production access and unsupported-claim rejection. | `python -m unittest tests.product_agent_os.test_methodology_catalog -v` fails before catalog implementation on missing database gates or fields. |
| `T9-D9-M2` | Add RED audit recommendation coverage | `tests/product_agent_os/test_methodology_audit.py` | Tests cover schema change, migration, backfill, retention/deletion, PII/sensitive fields, production data access, index/query performance, constraints, data quality, analytics/RAG lineage, backup/restore and rollback/compensation recommendations with stable priorities/artifacts. | `python -m unittest tests.product_agent_os.test_methodology_audit -v` fails before database audit implementation on missing recommendations. |
| `T9-D9-M3` | Add false-positive and unsupported-claim tests | `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | Schema-only files are `present_unverified`, not safety proof; README/docs-only work without data change does not force database blockers; simple local SQLite/demo fixtures do not force production gates; unsupported database claims produce deterministic recommendations. | Focused audit/discovery/fixture tests fail before false-positive routing exists. |
| `T9-D9-M4` | Expand read-only database discovery signals | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `tests/product_agent_os/test_discovery.py` | Discovery records migration tools and schema sources: Alembic, Prisma, Rails/Django migrations, Liquibase, Flyway, dbt, Great Expectations, OpenLineage, DBML, SQL DDL, SchemaSpy/dbdocs, schema folders, backfills, seeds, retention/deletion, backup/restore, query plans, production data/access hints and RAG ingestion data as `present_unverified`. | Focused discovery tests assert signal packets without DB connections, introspection, external writes or migration execution. |
| `T9-D9-M5` | Fill `database_data` catalog data | `plugins/product-agent-os/assets/methodology/methodology-catalog.json` | Domain records applies/not-applicable rules, maturity/complexity impact, Track 8 scenarios, decision horizons, artifacts, gates, eval fields and overlaps for Backend, API, Quality, Security/Privacy, Delivery and LLM/AI/RAG. | Focused catalog test passes for `database_data`. |
| `T9-D9-M6` | Implement database recommendation router | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | `_database_data_recommendations(...)` emits stable packets for database inventory, dictionary, schema source, migration plan, expand/contract, transaction boundary, rollback feasibility, backup/restore, classification, quality checks, data contract, lineage, performance, retention/deletion, synthetic fixtures and production access approval. | Focused audit tests pass and recommendation packets keep stable shape. |
| `T9-D9-M7` | Define database severity and accepted-gap policy | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Production data access, destructive migration, irreversible data loss, missing rollback, missing restore evidence, sensitive data leakage and broad prod credentials are blocker/high-risk. Simple local/non-production schema docs can be `P2_recommended`, `not_applicable` or `explicit_gap_accepted` only with owner, reason, residual risk, review date and follow-up. | Focused audit/readiness tests assert priority levels and accepted-gap downgrade behavior. |
| `T9-D9-M8` | Add destructive migration, drift and side-effect safety policy | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_methodology_audit.py` | Lightweight detection flags `DROP`, rename, truncate, destructive cleanup, retention purge, unsafe `EXPLAIN ANALYZE` on writes, ORM/schema drift and manual SQL-only changes as questions/recommendations. The implementation does not claim full SQL parser precision. | Focused discovery/audit tests assert destructive-risk routing and false-positive safe language. |
| `T9-D9-M9` | Add database artifact templates | `plugins/product-agent-os/assets/templates/artifact-templates/database-inventory.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-migration-plan.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-expand-contract-record.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-backfill-runbook.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-rollback-feasibility.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-backup-restore-evidence.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-data-classification-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-data-quality-checks.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-data-contract.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-lineage-map.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-query-performance-review.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-retention-deletion-policy.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-synthetic-fixtures-policy.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-production-access-approval.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-dictionary.md` | New templates include `Source status:`, owner, environment, source of truth, status, evidence, accepted gap, residual risk, approval boundary, verification command/gap and no secrets/private data guidance. Existing `database-dictionary.md` is strengthened with sensitivity, retention, constraints, owner and migration/drift fields. | Infrastructure template tests pass for required database terms and unresolved substitutions. |
| `T9-D9-M10` | Register database templates in renderer | `plugins/product-agent-os/scripts/product_agent_os/templates.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `plugins/product-agent-os/scripts/run_fixture_eval.py` | All new database templates render to `.codex/artifact-templates/<name>`, `REQUIRED_TARGETS` includes them once, and renderer file count increases by 14 from the T9-D8 baseline if no other templates are added. | Infrastructure and fixture eval tests pass with renderer file count 142. |
| `T9-D9-M11` | Strengthen generated control-plane and eval templates | `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`, `plugins/product-agent-os/assets/templates/control-plane/TEST.md`, `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` | Generated artifacts expose database gates, readiness statuses, schema/migration/backfill/classification/quality/lineage/production-access evidence, accepted-gap handling and no-production-data policy. Behavioral evals block completion from ORM-only, migration-applied-only, backup-exists-only or anonymized-prod-data-only claims. | Infrastructure and behavioral workflow eval tests pass. |
| `T9-D9-M12` | Route database methodology through lifecycle skills | `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `plugins/product-agent-os/skills/requirements-author/SKILL.md`, `plugins/product-agent-os/skills/implementation-planner/SKILL.md`, `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`, `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`, `plugins/product-agent-os/skills/docs-maintainer/SKILL.md`, `plugins/product-agent-os/skills/pr-release-operator/SKILL.md` | Skills require database inventory/source, migration/backfill/rollback/restore/classification/quality/lineage/performance evidence, staged-first production access approval and no data-safety/readiness claims from inspection alone. | Lifecycle skill tests pass for database methodology wording. |
| `T9-D9-M13` | Add database fixture eval contract | `plugins/product-agent-os/scripts/run_fixture_eval.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | `database_data_contract_present`, `database_schema_source_present`, `database_production_access_approval_present` and `database_synthetic_fixture_policy_present` checks validate catalog gates, artifacts, eval fields, templates, lifecycle skill coverage and false-positive behavior. | `python plugins\product-agent-os\scripts\run_fixture_eval.py` exits `0` after implementation with expected database checks. |
| `T9-D9-M14` | Add positive and negative database fixtures | `plugins/product-agent-os/assets/fixtures/data-migration-pii/`, `plugins/product-agent-os/assets/fixtures/database-schema-only/`, `plugins/product-agent-os/assets/fixtures/database-destructive-migration/`, `plugins/product-agent-os/assets/fixtures/database-production-access-approval/`, `plugins/product-agent-os/assets/fixtures/database-lineage-rag-overlap/`, `tests/product_agent_os/test_fixtures.py`, `tests/product_agent_os/test_discovery.py` | Synthetic fixtures cover richer data migration, schema-only `present_unverified`, destructive migration risk, production access approval, dbt/GX/OpenLineage-style data quality/lineage and RAG overlap. Fixtures remain synthetic and contain no secrets, tokens, private data, connection strings or production dumps. | Fixture completeness and discovery tests pass. |
| `T9-D9-M15` | Sync docs, source registry, backlog and root control-plane | `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `docs/sources/product-agent-os-track-9-backlog.md`, `docs/sources/registry.md`, `plugins/product-agent-os/README.md`, `docs/product-agent-os/behavioral-evals.md`, `docs/product-agent-os/scenarios.md` | Current state records `T9-D9` completion, RED/GREEN evidence, renderer file count delta, unsupported-claim handling, schema-only false-positive handling, production access approval boundary, residual risks and next action `T9-D10`. | `python tools\check_docs.py` passes; strict MkDocs runs only if navigation, Mermaid, Markdown extensions, MkDocs config or docs navigation changed. |
| `T9-D9-M16` | Define final T9-D9 verification command set without implicit commit | `tests/product_agent_os/`, `plugins/product-agent-os/scripts/run_fixture_eval.py`, `plugins/product-agent-os/scripts/run_transcript_eval.py`, `plugins/product-agent-os/scripts/validate_codex_compatibility.py`, `tools/check_docs.py` | Focused catalog/audit/discovery/template/lifecycle/fixture/docs tests, fixture eval, full unittest, transcript eval, compatibility check, docs check and diff hygiene are the required final command set after rows `T9-D9-M0..M24`. Commit remains deferred until explicitly requested. | Plan review confirms no verification gap before a later `feat: integrate database data methodology` commit. |
| `T9-D9-M17` | Add data contract and constraints/index integrity gates | `plugins/product-agent-os/assets/methodology/methodology-catalog.json`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/database-data-contract.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-dictionary.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-query-performance-review.md`, `tests/product_agent_os/test_methodology_catalog.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Catalog and audit include `database_data_contract_present` and `database_constraints_integrity_review_present`. Data contracts record columns, types, semantics, compatibility and owner. Constraint/index review records check, not-null, unique, primary key, foreign key, exclusion constraints where relevant, protected invariant/query, deployment impact and verification evidence. | Focused catalog/audit/template tests assert data contract fields and constraint/index integrity terms. |
| `T9-D9-M18` | Add migration tool evidence depth and deferrals | `plugins/product-agent-os/assets/templates/artifact-templates/database-migration-plan.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-rollback-feasibility.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `docs/sources/product-agent-os-track-9-backlog.md`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | Migration evidence records project-selected tooling without defaults: Liquibase `DATABASECHANGELOG`, preconditions, contexts and labels when Liquibase is present; Flyway schema history, versioned/repeatable migrations and dry-run/deployment report when Flyway is present; Alembic, Prisma, Rails and Django migration evidence only when detected. Stack-specific defaults and schema-diff tooling remain deferred with owner/reason. | Focused template/audit/docs tests assert tool-specific evidence terms and no universal migration-tool default. |
| `T9-D9-M19` | Migrate existing DB readiness gate without conflicting contracts | `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, `plugins/product-agent-os/scripts/run_fixture_eval.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | Existing `db_docs_when_schema_changes` is strengthened, renamed with compatibility mapping, or explicitly retained as an alias for `database_data_readiness_when_database_or_data_changes`. The eval template must not expose two conflicting database readiness contracts for the same workspace. | Infrastructure and fixture eval tests assert exactly one effective database readiness contract and preserved backward behavior for existing data-migration cases. |
| `T9-D9-M20` | Preserve Track 8 `data_migration` route compatibility | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/assets/templates/workflows/data-migration.md`, `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_behavioral_workflow_evals.py`, `tests/product_agent_os/test_lifecycle_skills.py` | Existing `data_migration` usage mode, minimum artifacts and behavioral eval case stay compatible. Generic `migration-plan.md` remains valid for non-database migration/release contexts, while database-specific work additionally stages or recommends `database-migration-plan.md` and related database artifacts. | Existing data migration discovery/behavioral/lifecycle tests continue passing, with new assertions for database-specific artifact routing. |
| `T9-D9-M21` | Add stable `database_data_signals` route packet | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_lifecycle_skills.py` | `route_inputs.workspace_signals.database_data_signals` is emitted alongside backward-compatible `data_migration_signals`. Packet fields cover schema source, migration tool, database client, ORM model, destructive risk, backfill, retention/deletion, data classification, quality checks, lineage, performance, backup/restore, production access and verification status as `present_unverified`, `applicable_missing` or `approval_required`. | Discovery and lifecycle skill tests assert stable packet shape and no DB connection, introspection or migration execution. |
| `T9-D9-M22` | Add runtime and data pipeline discovery signals | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/assets/fixtures/database-lineage-rag-overlap/`, `plugins/product-agent-os/assets/fixtures/data-migration-pii/`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_fixtures.py` | Discovery detects database clients, ORM models, data warehouse jobs, scheduled data pipelines, reporting tables, RAG ingestion sources and analytics models as read-only signals. These signals can make `database_data` applicable and create overlaps with `llm_ai_rag`, Backend, Delivery and Security without claiming runtime correctness. | Focused discovery/fixture tests assert pipeline and RAG overlap signals remain `present_unverified`. |
| `T9-D9-M23` | Deepen privacy classification and backup/restore evidence | `plugins/product-agent-os/assets/templates/artifact-templates/database-data-classification-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-retention-deletion-policy.md`, `plugins/product-agent-os/assets/templates/artifact-templates/database-backup-restore-evidence.md`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_methodology_audit.py` | Classification records legal basis, minimization, retention, deletion/export path, access boundary and owner review. Backup/restore records backup source, restore target, RPO/RTO, restore drill date/result and verification result. Completion is blocked by production/high-risk data work without restore evidence or an accepted gap. | Focused template/audit tests assert privacy and restore evidence depth. |
| `T9-D9-M24` | Expand docs sync scope and final evidence closure | `docs/product-agent-os/index.md`, `docs/product-agent-os/technical.md`, `docs/product-agent-os/development-standards.md`, `docs/product-agent-os/scenarios.md`, `docs/product-agent-os/behavioral-evals.md`, `plugins/product-agent-os/README.md`, `docs/sources/registry.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `tests/product_agent_os/test_product_agent_os_docs.py` | User-facing artifact inventories mention the new database templates when they become packaged artifacts; source registry records T9-D9 coverage; root control-plane files record final focused/full/fixture/transcript/compat/docs/diff evidence. Strict MkDocs runs only if navigation, Mermaid, Markdown extensions, MkDocs config or docs navigation changed. | Product-Agent OS docs tests, `python tools\check_docs.py` and the final T9-D9 command set pass before any commit. |

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

Expected: focused tests, fixture eval, full unittest, transcript eval, compatibility check, docs check and diff hygiene pass before commit. Commit is intentionally deferred until explicitly requested in the current working branch.

---

### Task 17: T9-D10 LLM / AI / RAG Integration

**Files:**
- Source: `docs/methodologies/llm-ai-rag.md`
- Modify: catalog, audit, `ai-eval-spec.md`
- Create: `ai-behavior-spec.md`
- Create: `ai-model-decision-record.md`
- Create: `ai-prompt-contract.md`
- Create: `ai-tool-contract.md`
- Create: `rag-source-inventory.md`
- Create: `rag-retrieval-config.md`
- Create: `rag-grounding-eval.md`
- Create: `ai-dataset-governance.md`
- Create: `ai-cost-latency-budget.md`
- Create: `ai-human-approval-boundary.md`
- Create: `ai-safety-review.md`

#### T9-D10 Task Matrix

This matrix maps the `docs/methodologies/llm-ai-rag.md` deep-audit findings to concrete implementation rows. The step checklist below remains the short execution outline; this table is the traceability layer for tests, implementation, templates, docs sync and verification.

| ID | Task | Files | Критерии приемки | Verification |
| --- | --- | --- | --- | --- |
| `T9-D10-M0` | Refresh plan and backlog before implementation | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, `docs/sources/product-agent-os-track-9-backlog.md` | Deep-audit deltas are recorded: source artifact template gaps, naming compatibility, eval/report/trace/guardrail depth, false-positive risks, unsupported claims, deferred tooling decisions and no implicit commit. | `python tools\check_docs.py` passes after documentation edits. |
| `T9-D10-M1` | Add RED catalog contract for `llm_ai_rag` | `tests/product_agent_os/test_methodology_catalog.py` | Test asserts applies/not-applicable rules, maturity/complexity impact, Track 8 scenarios, decision horizons, overlaps, artifacts, gates and eval fields for AI behavior, evals, prompts, models, structured outputs, tools, RAG, grounding, datasets, safety, traces and cost/latency. | `python -m unittest tests.product_agent_os.test_methodology_catalog -v` fails before catalog implementation on missing AI/RAG gates or fields. |
| `T9-D10-M2` | Add RED audit recommendation coverage | `tests/product_agent_os/test_methodology_audit.py` | Tests cover baseline eval, rerun command, dataset governance, prompt contract, model decision, structured output schema, tool contract, RAG source/retrieval/grounding, agent trace, safety review, private-data guard and cost/latency recommendations with stable priorities and artifacts. | Focused audit tests fail before AI/RAG recommendations exist. |
| `T9-D10-M3` | Add RED discovery packet tests | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `tests/product_agent_os/test_discovery.py` | Discovery exposes stable `llm_ai_rag_signals` while preserving backward-compatible `ai_eval_signals`; packets remain read-only and use `present_unverified`, `applicable_missing` or `approval_required`, never `present_verified` from detection alone. | Focused discovery tests fail before packet implementation. |
| `T9-D10-M4` | Add false-positive and unsupported-claim tests | `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | Docs-only AI mentions, frontend `model/` folders, vector math, non-behavior prompt docs and package-name-only signals do not force blockers. Manual spot checks, citations-only RAG proof, tool-schema-only safety and model-upgrade-is-better claims produce explicit unsupported-claim recommendations. | Focused audit/discovery/fixture tests fail before false-positive routing exists. |
| `T9-D10-M5` | Fill `llm_ai_rag` catalog data | `plugins/product-agent-os/assets/methodology/methodology-catalog.json` | Domain records source-backed applies/not-applicable rules, maturity/complexity impact, Track 8 scenario coverage, decision horizons, artifacts, gates, eval fields and overlaps with Quality, Codex workflow, Backend, API, Database, Security, Product and Delivery. | Focused catalog test passes for `llm_ai_rag`. |
| `T9-D10-M6` | Implement AI/RAG discovery signals | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `tests/product_agent_os/test_discovery.py` | Discovery detects prompts, eval configs, model config, OpenAI/AI SDKs, Agents SDK traces, tool/function calls, MCP tool surfaces, RAG corpora, retrieval, vector stores, embeddings, rerankers, grounding artifacts, safety/guardrail files and latency/cost evidence without running external tools. | Discovery tests assert packet shape and no network, model calls, vector DB access or external writes. |
| `T9-D10-M7` | Add methodology applicability gate | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `llm_ai_rag_readiness_when_ai_behavior_changes` records applicability reason, required evidence, owner, residual risk and accepted-gap path. Detection alone remains `present_unverified`. | Discovery/readiness tests assert status transitions and gate text. |
| `T9-D10-M8` | Implement baseline eval recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | Prompt, model, retrieval, tool, structured-output or agent behavior changes emit `ai_baseline_eval_present` blocker/high-risk recommendation unless baseline eval or explicit accepted gap exists. | Audit tests assert priority, artifact, evidence owner, residual risk and accepted-gap fields. |
| `T9-D10-M9` | Implement eval rerun and report recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/ai-eval-spec.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Eval-governed AI changes require rerun command, threshold, owner, baseline/current comparison, failed cases, residual risk and current-run evidence; inspection-only review must be marked as a gap. | Audit/template tests assert rerun/report terms and "prompt inspection is enough" rejection. |
| `T9-D10-M10` | Implement dataset governance recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | Eval/RAG datasets require source, privacy class, synthetic/sanitized status, retention, owner and no secrets, credentials, private customer data or raw private chats. | Audit tests assert dataset/privacy recommendation and synthetic fixture safety wording. |
| `T9-D10-M11` | Implement prompt contract recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | Production prompts require version, role/goal/context, variables, constraints, output format, examples, uncertainty/refusal policy and verification route. | Audit tests assert `ai_prompt_contract_present` mapping and false-positive prompt-doc exceptions. |
| `T9-D10-M12` | Implement model decision recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | Model/provider/reasoning changes require model or snapshot/alias policy, reasoning effort, modality, context window, tool support, latency/cost, fallback and rollback/migration note when release-bound. | Audit tests assert `ai_model_decision_record_present` and no automatic quality claim from model upgrade. |
| `T9-D10-M13` | Implement structured-output recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | AI output that feeds code, UI, API, eval grader or another agent requires schema/typed contract, strictness, parser validation, refusal/fallback and failure cases. | Audit tests assert `ai_structured_output_contract_present` and parser/refusal coverage. |
| `T9-D10-M14` | Implement tool/function/MCP contract recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | Tool-using AI requires schema, permissions, side effects, idempotency, retries, error handling and human approval boundary for writes, shell, money, data exposure or irreversible actions. | Audit tests assert `ai_tool_contract_present` and `ai_human_approval_boundary_present`. |
| `T9-D10-M15` | Implement RAG source, retrieval and grounding recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | RAG claims require source inventory, corpus authority, freshness, ingestion path, exclusions, chunking, embeddings, vector store, filters, top-k/reranking, metadata, retrieval metrics, grounding rubric and unsupported-claim behavior. | Audit tests assert RAG recommendations and citations-only rejection. |
| `T9-D10-M16` | Implement agent workflow trace recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | Agent workflow changes require smallest-useful workflow, final-answer owner, tool/handoff/state map, stop conditions and trace/run evidence. Codex runtime model/reasoning policy remains owned by `codex_agentic_workflow`. | Audit tests assert `agent_workflow_trace_present` and no forced multi-agent default. |
| `T9-D10-M17` | Implement safety and guardrail recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | User input, prompt injection, private data, risky tools, minors, cybersecurity, finance, healthcare, legal, support or irreversible side effects require safety/red-team review, fallback and owner approval boundary. | Audit tests assert `ai_safety_review_present` with overlap to Security/Privacy without claiming compliance closure. |
| `T9-D10-M18` | Implement cost/latency budget recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | User-facing or high-volume AI features require timeout, retry, caching, background/batch mode, fallback, token/cost budget and measurement or explicit unavailable gap. | Audit tests assert `ai_cost_latency_budget_present`. |
| `T9-D10-M19` | Add AI/RAG artifact templates | `plugins/product-agent-os/assets/templates/artifact-templates/ai-behavior-spec.md`, `plugins/product-agent-os/assets/templates/artifact-templates/prompt-contract.md`, `plugins/product-agent-os/assets/templates/artifact-templates/model-decision-record.md`, `plugins/product-agent-os/assets/templates/artifact-templates/eval-run-report.md`, `plugins/product-agent-os/assets/templates/artifact-templates/ai-dataset-manifest.md`, `plugins/product-agent-os/assets/templates/artifact-templates/structured-output-schema.md`, `plugins/product-agent-os/assets/templates/artifact-templates/ai-tool-contract.md`, `plugins/product-agent-os/assets/templates/artifact-templates/rag-source-inventory.md`, `plugins/product-agent-os/assets/templates/artifact-templates/rag-retrieval-config.md`, `plugins/product-agent-os/assets/templates/artifact-templates/rag-eval-report.md`, `plugins/product-agent-os/assets/templates/artifact-templates/grounding-rubric.md`, `plugins/product-agent-os/assets/templates/artifact-templates/agent-workflow-map.md`, `plugins/product-agent-os/assets/templates/artifact-templates/guardrail-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/trace-evidence-packet.md`, `plugins/product-agent-os/assets/templates/artifact-templates/ai-cost-latency-budget.md` | Templates include `Source status:`, owner, evidence, accepted gap, residual risk, approval boundary, verification command/gap and no secrets/private data guidance. | Infrastructure template tests pass for required terms and no unresolved substitutions. |
| `T9-D10-M20` | Resolve AI/RAG template naming compatibility | `plugins/product-agent-os/assets/methodology/methodology-catalog.json`, `plugins/product-agent-os/scripts/product_agent_os/templates.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Source-aligned names such as `prompt-contract.md`, `model-decision-record.md`, `rag-eval-report.md` are canonical, while plan-era names such as `ai-prompt-contract.md`, `ai-model-decision-record.md`, `rag-grounding-eval.md` are mapped, aliased or explicitly retired without duplicate conflicting contracts. | Template/catalog tests assert one effective contract per artifact purpose. |
| `T9-D10-M21` | Strengthen existing AI eval workflow and spec | `plugins/product-agent-os/assets/templates/artifact-templates/ai-eval-spec.md`, `plugins/product-agent-os/assets/templates/workflows/ai-eval-regression.md`, `tests/product_agent_os/test_infrastructure_templates.py` | Existing Track 8 AI eval workflow covers app path, baseline/current comparison, prompt/context inventory, retrieval metrics, dataset policy, judge rubric, thresholds, latency, cost, grounding, failed cases and one-factor-at-a-time change log. | Infrastructure tests assert strengthened terms and backward compatibility. |
| `T9-D10-M22` | Register AI/RAG templates in renderer | `plugins/product-agent-os/scripts/product_agent_os/templates.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `plugins/product-agent-os/scripts/run_fixture_eval.py` | New templates render to `.codex/artifact-templates/<name>`, `REQUIRED_TARGETS` includes them once and renderer file count increases from the T9-D9 baseline by the implemented template count. | Infrastructure and fixture eval tests pass with updated file count. |
| `T9-D10-M23` | Strengthen generated control-plane templates | `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`, `plugins/product-agent-os/assets/templates/control-plane/TEST.md`, `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `tests/product_agent_os/test_infrastructure_templates.py` | Generated artifacts expose AI behavior promise, eval baseline/rerun, dataset governance, prompt/model/schema/tool/RAG/agent/safety/cost evidence, current-run evidence and accepted-gap handling. | Infrastructure tests assert control-plane AI/RAG fields. |
| `T9-D10-M24` | Expand behavioral and transcript eval coverage | `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json`, `plugins/product-agent-os/assets/eval-fixtures/transcripts/product-agent-os-synthetic-sessions.json`, `tests/product_agent_os/test_behavioral_workflow_evals.py`, `tests/product_agent_os/test_transcript_session_evals.py` | Behavioral and transcript cases require baseline eval terms, app-backed path, RAG grounding, safety/cost evidence and forbid "prompt inspection is enough" or AI quality claims without current eval evidence. | Behavioral and transcript tests pass; transcript eval exits `0`. |
| `T9-D10-M25` | Add positive and negative AI/RAG fixtures | `plugins/product-agent-os/assets/fixtures/rag-quality-regression/`, `plugins/product-agent-os/assets/fixtures/ai-prompt-model-change/`, `plugins/product-agent-os/assets/fixtures/ai-tool-approval/`, `plugins/product-agent-os/assets/fixtures/ai-structured-output/`, `plugins/product-agent-os/assets/fixtures/ai-agent-trace/`, `plugins/product-agent-os/assets/fixtures/ai-latency-cost-budget/`, `tests/product_agent_os/test_fixtures.py`, `tests/product_agent_os/test_discovery.py` | Synthetic fixtures cover prompt/model change, RAG grounding regression, tool approval boundary, structured output, agent trace and latency/cost budget. Fixtures contain no secrets, tokens, raw private chats, customer data or live API keys. | Fixture completeness and discovery tests pass. |
| `T9-D10-M26` | Add AI/RAG fixture eval contract | `plugins/product-agent-os/scripts/run_fixture_eval.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | `llm_ai_rag_contract_present` validates catalog gates, artifacts, eval fields, templates, lifecycle skill coverage, false-positive behavior and privacy/no-secrets constraints. `python-app` expected checks include the new contract. | `python plugins\product-agent-os\scripts\run_fixture_eval.py` exits `0` after implementation. |
| `T9-D10-M27` | Route AI/RAG methodology through lifecycle skills | `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`, `plugins/product-agent-os/skills/requirements-author/SKILL.md`, `plugins/product-agent-os/skills/implementation-planner/SKILL.md`, `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`, `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`, `plugins/product-agent-os/skills/docs-maintainer/SKILL.md`, `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md` | Skills require AI behavior promise, baseline/rerun evidence, app-backed eval path, prompt/model/schema/tool/RAG/agent artifacts, safety and cost evidence; they do not force one eval runner, multi-agent architecture or live model/API calls. | Lifecycle skill tests pass for AI/RAG methodology wording. |
| `T9-D10-M28` | Sync docs, source registry, backlog and root control-plane | `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `docs/sources/product-agent-os-track-9-backlog.md`, `docs/sources/registry.md`, `plugins/product-agent-os/README.md`, `docs/product-agent-os/behavioral-evals.md`, `docs/product-agent-os/scenarios.md`, `docs/product-agent-os/development-standards.md` | Current state records `T9-D10` completion, RED/GREEN evidence, renderer file count delta, unsupported-claim handling, false-positive handling, AI/RAG residual risks and next action `T9-D11`. Source registry is refreshed only for new source-backed claims. | Product-Agent OS docs tests and `python tools\check_docs.py` pass; strict MkDocs runs only if navigation, Mermaid, Markdown extensions, MkDocs config or docs navigation changed. |
| `T9-D10-M29` | Define final T9-D10 verification command set without implicit commit | `tests/product_agent_os/`, `plugins/product-agent-os/scripts/run_fixture_eval.py`, `plugins/product-agent-os/scripts/run_transcript_eval.py`, `plugins/product-agent-os/scripts/validate_codex_compatibility.py`, `tools/check_docs.py` | Focused catalog/audit/discovery/template/lifecycle/behavioral/transcript/fixture/docs/report tests, fixture eval, full unittest, transcript eval, compatibility check, docs check and diff hygiene are required. Commit remains deferred until explicitly requested. | Plan review confirms no verification gap before a later user-requested commit. |
| `T9-D10-M30` | Resolve agent handoff artifact compatibility | `plugins/product-agent-os/assets/methodology/methodology-catalog.json`, `plugins/product-agent-os/assets/templates/artifact-templates/agent-workflow-map.md`, `plugins/product-agent-os/assets/templates/artifact-templates/agent-handoff-contract.md`, `plugins/product-agent-os/assets/templates/artifact-templates/handoff-contract.md`, `plugins/product-agent-os/assets/templates/artifact-templates/agent-task-packet.md`, `plugins/product-agent-os/scripts/product_agent_os/templates.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Source artifact `agent-handoff-contract.md` is either added as an AI-specific alias or explicitly mapped to existing `handoff-contract.md`/`agent-task-packet.md` without conflicting contracts. Agent handoff evidence records owner, inputs, output schema, stop condition and trace evidence. | Template/catalog tests assert one effective handoff contract and no duplicate ownership conflict. |
| `T9-D10-M31` | Add eval tooling selector and deferred runner policy | `plugins/product-agent-os/assets/methodology/methodology-catalog.json`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/ai-eval-spec.md`, `docs/sources/product-agent-os-track-9-backlog.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Promptfoo, OpenAI Evals, pytest/Jest app-backed evals, Ragas and LangSmith are treated as conditional tooling, not defaults. Recommendations require stack/privacy/CI fit, owner decision, selected/rejected runner rationale or deferred decision with reason and residual risk. | Focused audit/template/docs tests assert no forced eval runner and stable deferred decision wording. |
| `T9-D10-M32` | Add model migration and threshold policy | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/model-decision-record.md`, `plugins/product-agent-os/assets/templates/artifact-templates/eval-run-report.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Model migration records snapshot or approved alias policy, prompt migration impact, compatibility checks, rollback, baseline/current eval comparison, minimum threshold policy and temperature-equivalent or sampling parameter rationale where relevant. | Focused audit/template tests assert model migration terms and block "model upgrade automatically improves quality" claims. |
| `T9-D10-M33` | Add RAG corpus lifecycle, deletion and privacy path | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/rag-source-inventory.md`, `plugins/product-agent-os/assets/templates/artifact-templates/rag-retrieval-config.md`, `plugins/product-agent-os/assets/templates/artifact-templates/ai-dataset-manifest.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | RAG source inventory and retrieval config record deletion path, retention, source exclusion, stale-source pruning, privacy owner, vector store lifecycle and overlap with database/security gates when source data is sensitive or production-owned. | Focused audit/template tests assert RAG deletion/privacy terms and `present_unverified` status until owner evidence exists. |
| `T9-D10-M34` | Add AI behavior change diff-signal policy | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `docs/sources/product-agent-os-track-9-backlog.md`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_methodology_audit.py` | Plan records whether AI behavior change detection from code/config diffs is implemented, explicitly deferred, or limited to workspace/intent signals. Diff-based detection must not silently inspect external branches or claim certainty from filename changes alone. | Focused discovery/audit/docs tests assert diff-signal status, limitations and no external git/network dependency. |
| `T9-D10-M35` | Add AI incident workflow boundary | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/guardrail-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/eval-run-report.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Failed eval, hallucination report, unsafe output, tool misuse or data exposure routes to an incident boundary with owner, severity, evidence, mitigation, follow-up eval and Security/Privacy handoff when applicable. T9-D10 records the AI behavior incident contract without claiming full T9-D11 compliance closure. | Focused audit/template tests assert incident terms and security/privacy overlap language. |
| `T9-D10-M36` | Add methodology report/render coverage for AI/RAG | `plugins/product-agent-os/scripts/product_agent_os/methodology_report.py`, `tests/product_agent_os/test_methodology_report.py`, `tests/product_agent_os/test_methodology_audit.py` | Methodology audit reports render AI/RAG recommendations, approval boundaries, residual risks, accepted gaps and safe next actions without leaking prompts, traces, private data, credentials or raw customer text. | `python -m unittest tests.product_agent_os.test_methodology_report tests.product_agent_os.test_methodology_audit -v` passes after implementation. |

**T9-D10 execution batching policy:**

- Execute T9-D10 rows in batches of up to 10 matrix rows: `M0..M9`, `M10..M19`, `M20..M29`, then `M30..M36`.
- After each batch, stop broad implementation work and report to the user: rows completed, files changed, checks run, results, unresolved risks and the next batch.
- Do not start the next T9-D10 batch until the previous batch report is written in the thread.
- Commit, push and PR actions remain deferred until explicitly requested by the user.

**T9-D10 batch evidence so far:**

- `M0..M9`: catalog, discovery, readiness, baseline/rerun recommendations, unsupported-claim handling and false-positive guards implemented; fixture eval remains read-only and approval-bound.
- `M10..M19`: audit recommendation depth and 15 AI/RAG artifact templates implemented; renderer registration intentionally deferred to `M22`.
- `M20..M29`: template aliases, renderer registration, AI eval workflow/spec strengthening, generated control-plane fields, behavioral/transcript coverage, synthetic fixtures, fixture eval contract and lifecycle routing implemented. `llm_ai_rag_contract_present` is now covered, and renderer file count moves from 142 to 157.
- `M30..M36`: agent handoff compatibility, eval tooling selector policy, model migration thresholds, RAG deletion/privacy lifecycle, diff-signal policy, AI incident workflow and methodology report rendering implemented. Full final verification is recorded in `TEST.md`, `RUNLOG.md` and the Track 9 backlog.

- [ ] **Step 1: Add RED test for AI/RAG gates**

Assert `llm_ai_rag` gates include:

```python
[
    "ai_behavior_spec_present",
    "ai_baseline_eval_present",
    "ai_eval_rerun_command_present",
    "ai_model_decision_record_present",
    "ai_prompt_contract_present",
    "ai_structured_output_contract_present",
    "ai_tool_contract_present",
    "rag_source_inventory_present",
    "rag_retrieval_config_present",
    "rag_grounding_eval_present",
    "ai_dataset_governance_present",
    "ai_no_private_data_in_fixtures_present",
    "ai_cost_latency_budget_present",
    "ai_human_approval_boundary_present",
    "ai_safety_review_present",
    "agent_workflow_trace_present",
]
```

- [ ] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing AI/RAG gates.

- [ ] **Step 3: Add AI/RAG catalog and safety rules**

Rules:

- AI behavior changes require baseline or accepted baseline gap;
- private data in eval fixtures is blocked;
- model alias vs snapshot policy creates recommendation when release/rollback matters;
- tool-using AI requires tool contract and human approval boundary;
- RAG claims require source inventory and grounding evidence.

- [ ] **Step 4: Add templates and detection**

Create all AI/RAG templates listed in Files. Detect prompts, evals, RAG, vector, embeddings, model configs, tool calls and Agents SDK traces.

- [ ] **Step 5: Add transcript/eval coverage**

Extend transcript eval fixtures with one methodology-intelligence AI case that requires baseline eval terms and forbids "prompt inspection is enough".

- [x] **Step 6: Run verification without implicit commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_transcript_session_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures tests.product_agent_os.test_methodology_report -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

Expected: focused tests, fixture eval, full unittest, transcript eval, compatibility check, docs check and diff hygiene pass. Commit is intentionally deferred until explicitly requested in the current working branch.

---

### Task 18: T9-D11 Security, Privacy & Compliance Integration

**Files:**
- Source: `docs/methodologies/security-privacy-compliance.md`
- Modify: catalog, audit, `security-risk-review.md`
- Create: `threat-surface.md`
- Create: `asvs-ssdf-mapping.md`
- Create: `authz-negative-test-matrix.md`
- Create: `secrets-policy.md`
- Create: `privacy-impact-record.md`
- Create: `supply-chain-review.md`
- Create: `audit-logging-review.md`
- Create: `compliance-overlay.md`

Deep-audit update from `docs/methodologies/security-privacy-compliance.md` and `docs/sources/methodology-research/security-privacy-compliance.md`:

- The compact checklist below must use the full Security, Privacy & Compliance gate set from the methodology source, not only the initial subset in this task.
- Source references are methodology evidence and platform/security guidance, not legal advice. Compliance output must record applicability, owner, evidence, non-goals and review cadence without claiming GDPR, CCPA, HIPAA, PCI, SOC 2 or enterprise compliance certification.
- Template naming must be resolved before implementation: source-era artifact names such as `threat-model.md`, `asvs-mapping.md`, `secrets-inventory.md`, `authz-matrix.md`, `audit-log-policy.md` and `compliance-applicability-matrix.md` must either become canonical or be mapped to the plan-era names without duplicate conflicting contracts.
- Codex Security scan remains explicit opt-in. Security-sensitive routing can recommend a scan or record `not requested`, but must not imply a scan ran from security terminology alone.

This matrix maps the deep-audit findings to concrete implementation work. The numbered steps below remain the compact execution checklist; this table is the traceability layer for the focused T9-D11 slice.

| ID | Work | Files | Acceptance / Evidence | Verification |
| --- | --- | --- | --- | --- |
| `T9-D11-M0` | Refresh plan/backlog before implementation | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, `docs/sources/product-agent-os-track-9-backlog.md` | Deep-audit deltas record full gate set, artifact-name compatibility, legal/compliance boundary, false-positive risks, unsupported claims, Codex Security opt-in policy and exact verification commands. | `python tools\check_docs.py` |
| `T9-D11-M1` | Add RED catalog contract for `security_privacy_compliance` | `tests/product_agent_os/test_methodology_catalog.py` | Test asserts gates, artifacts, eval fields, applies/not-applicable rules, maturity levels, complexity impact and overlaps from the source artifact. | Focused catalog test fails before catalog implementation on missing security/privacy/compliance gates. |
| `T9-D11-M2` | Resolve security artifact naming compatibility | `plugins/product-agent-os/assets/methodology/methodology-catalog.json`, `plugins/product-agent-os/scripts/product_agent_os/templates.py`, `tests/product_agent_os/test_infrastructure_templates.py` | One effective contract exists per purpose for threat surface/model, ASVS/SSDF mapping, secrets policy/inventory, authz negative tests, audit logging and compliance overlay/applicability. No duplicate conflicting artifact ownership remains. | Template/catalog tests assert canonical names or explicit aliases. |
| `T9-D11-M3` | Fill `security_privacy_compliance` catalog data | `plugins/product-agent-os/assets/methodology/methodology-catalog.json` | Domain records applies/not-applicable rules, maturity impact `baseline/team/production/regulated`, complexity impact, Track 8 scenario coverage, decision horizons, artifacts, gates, eval fields and overlaps with Backend, API, Database, AI/RAG, Quality, Delivery, Architecture, Product and Codex workflow. | `python -m unittest tests.product_agent_os.test_methodology_catalog -v` |
| `T9-D11-M4` | Add security/privacy discovery depth | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `tests/product_agent_os/test_discovery.py` | Discovery exposes authn/authz, permissions, secrets, PII/sensitive data, payment/billing, abuse/rate limit, audit logging, supply chain, SBOM/provenance, CI permissions, compliance, AI/agent security and Codex approval-bound signals as `present_unverified`. | Focused discovery tests assert signal packets and no readiness claims from detection alone. |
| `T9-D11-M5` | Implement domain applicability routing | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | Auth, PII, payment, secrets, external writes, production data, AI agents, compliance terms, supply chain and CI permission signals route the domain; docs-only security articles and keyword-only claims do not become regulated automatically. | Audit tests assert applicable, `present_unverified` and `not_applicable` transitions. |
| `T9-D11-M6` | Implement granular security recommendations | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | Recommendations map every gate to stable priority, artifact, evidence owner, approval boundary, accepted-gap option, residual risk and safe next action. Payment/billing, production data, secret rotation, policy changes and external security-system mutations are `approval_required`. | Focused audit tests assert gate-to-artifact mapping and priorities. |
| `T9-D11-M7` | Add unsupported-claim rejection | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | Unsupported claims are rejected: security review after coding, no-secrets-in-code means safe, ASVS/OWASP proves compliance, SBOM once is enough, Codex Security scan is implied, OAuth proves API security and privacy compliance is universal. | Audit tests assert `P1_high_risk` recommendations with source/legal boundary wording. |
| `T9-D11-M8` | Create and strengthen security templates | `plugins/product-agent-os/assets/templates/artifact-templates/*.md`, `tests/product_agent_os/test_infrastructure_templates.py` | Templates cover threat surface, ASVS/SSDF mapping, authz negative tests, secrets policy, privacy impact, supply chain review, audit logging review, compliance overlay and strengthened `security-risk-review.md`; templates forbid raw secrets, credentials, payment data, raw PII and private customer data. | Infrastructure template tests assert required terms and no unresolved placeholders. |
| `T9-D11-M9` | Register security templates in renderer | `plugins/product-agent-os/scripts/product_agent_os/templates.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | New artifact templates are staged under `.codex/artifact-templates/`; renderer file count is updated intentionally and fixture eval checks include `security_privacy_compliance_contract_present`. | Renderer/template/fixture tests pass with updated file count. |
| `T9-D11-M10` | Harden source and no-secrets policy | `plugins/product-agent-os/scripts/product_agent_os/source_policy.py`, `tests/product_agent_os/test_source_policy.py` | Source policy rejects secret-like literals, credentials, access tokens, raw PII/private data/payment data markers in docs/templates/fixtures and keeps OpenAI/Codex/security freshness claims source-reviewed. | `python -m unittest tests.product_agent_os.test_source_policy -v` |
| `T9-D11-M11` | Update readiness and behavioral eval contracts | `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json`, `tests/product_agent_os/test_behavioral_workflow_evals.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Readiness records `security_privacy_compliance`, conditional gates, transition statuses, approval boundaries and false-positive behavior without replacing existing `security_review_when_sensitive_surface`. | Behavioral/template tests assert expected/forbidden terms. |
| `T9-D11-M12` | Add fixture coverage for security false positives and approvals | `plugins/product-agent-os/assets/fixtures/*`, `plugins/product-agent-os/scripts/run_fixture_eval.py`, `tests/product_agent_os/test_fixture_eval_runner.py`, `tests/product_agent_os/test_fixtures.py` | Fixtures cover security-docs-only mention, payment/billing high risk, docs-only security article not regulated, CI permissions, SBOM/provenance, compliance claim without owner and no raw secrets/private data. | Fixture eval asserts route, priorities, false positives and privacy safety. |
| `T9-D11-M13` | Route methodology through lifecycle skills | `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`, `plugins/product-agent-os/skills/requirements-author/SKILL.md`, `plugins/product-agent-os/skills/implementation-planner/SKILL.md`, `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`, `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`, `plugins/product-agent-os/skills/docs-maintainer/SKILL.md`, `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md` | Skills require planning-first security classification, threat surface, data classification, owner review, tests/evidence, rollback, approval boundary, compliance owner and explicit Codex Security scan status. | Lifecycle skill tests assert wording and stop conditions. |
| `T9-D11-M14` | Sync Product-Agent OS docs and control plane | `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `plugins/product-agent-os/README.md`, `docs/product-agent-os/methodology-intelligence.md`, `docs/product-agent-os/behavioral-evals.md`, `docs/product-agent-os/scenarios.md`, `docs/product-agent-os/development-standards.md`, `docs/sources/product-agent-os-track-9-backlog.md` | Current state records T9-D11 completion evidence, residual risks, false-positive coverage, source/legal boundary, renderer file count delta and next action T9-D12. Source registry changes only if new source-backed claims are added. | Product docs tests and `python tools\check_docs.py` pass. |
| `T9-D11-M15` | Run focused and final verification | `tests/product_agent_os/*`, `plugins/product-agent-os/scripts/run_fixture_eval.py` | Focused tests, fixture eval, full unittest as needed, docs check and diff hygiene pass before completion claim. Commit is intentionally deferred unless explicitly requested in the current branch. | `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_source_policy tests.product_agent_os.test_fixture_eval_runner -v`; `python plugins\product-agent-os\scripts\run_fixture_eval.py`; `python tools\check_docs.py` |
| `T9-D11-M16` | Map or defer the full source artifact set | `plugins/product-agent-os/assets/methodology/methodology-catalog.json`, `plugins/product-agent-os/scripts/product_agent_os/templates.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `docs/sources/product-agent-os-track-9-backlog.md` | Source artifacts `data-classification-register.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `ai-security-review.md`, `vulnerability-response-record.md` and `approval-record.md` are added, aliased to existing templates or explicitly deferred with owner, reason and residual risk. | Catalog/template/backlog tests or docs checks assert no source artifact is silently dropped. |
| `T9-D11-M17` | Add SSDF, SAMM and ASVS level policy | `plugins/product-agent-os/assets/methodology/methodology-catalog.json`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/asvs-ssdf-mapping.md`, `tests/product_agent_os/test_methodology_catalog.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Secure SDLC/SSDF and SAMM are represented as lifecycle/maturity vocabulary. ASVS Level 1/2/3 selection records applicability, project risk, owner, evidence and explicit gaps without claiming compliance. | Focused catalog/audit/template tests assert SSDF/SAMM terms and ASVS level selection behavior. |
| `T9-D11-M18` | Add API authorization negative-test depth | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/authz-negative-test-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/api-security-review.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Authz negative tests cover allowed and forbidden behavior, BOLA, BFLA, object property authorization, role/scope/resource ownership checks, rate limits and unsafe consumption. OAuth or API docs alone are not accepted as security evidence. | Focused audit/template tests assert negative-test matrix terms and unsupported OAuth/security claims. |
| `T9-D11-M19` | Add data classification and redaction lifecycle | `plugins/product-agent-os/scripts/product_agent_os/source_policy.py`, `plugins/product-agent-os/assets/templates/artifact-templates/data-classification-register.md`, `plugins/product-agent-os/assets/templates/artifact-templates/privacy-impact-record.md`, `tests/product_agent_os/test_source_policy.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Prompts, docs, fixtures, eval datasets, logs, traces and screenshots record data class, purpose, retention, access, sharing, no-secrets/no-private-data status and redaction policy. Raw secrets, credentials, payment data, raw PII, raw private chats and private customer data are blocked. | Source-policy/template tests assert redaction coverage across docs/templates/fixtures. |
| `T9-D11-M20` | Add SBOM and provenance decision policy | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/supply-chain-review.md`, `plugins/product-agent-os/assets/templates/artifact-templates/sbom-manifest.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Internal app, package, plugin, container and release artifact paths record vulnerability status, update path, license status, SBOM format, provenance, action pinning, release signing or an explicit not-applicable/accepted-gap reason. SBOM alone is not supply-chain closure. | Focused audit/template tests assert SBOM/provenance conditions and false-positive handling. |
| `T9-D11-M21` | Add vulnerability and security incident response workflow | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/vulnerability-response-record.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Security bug, advisory, leaked secret, abuse incident, dependency alert or data exposure routes to triage, severity, containment, fix evidence, verification, disclosure path, patch/release plan and post-incident lessons. This general incident path is separate from the AI incident workflow in T9-D10. | Focused audit/template tests assert vulnerability response terms and security/privacy handoff behavior. |
| `T9-D11-M22` | Add compliance overlay taxonomy and domain overlays | `plugins/product-agent-os/assets/methodology/methodology-catalog.json`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/compliance-overlay.md`, `tests/product_agent_os/test_methodology_catalog.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Compliance overlays separate legal/regulatory obligations, customer contractual obligations and internal policy. Finance, healthcare, minors, enterprise, public sector, marketplace and AI agent tooling are recorded as conditional overlays with owner, applicability, evidence, gaps, non-goals and review cadence. | Catalog/audit/template tests assert overlay taxonomy and no generic compliance certification claim. |
| `T9-D11-M23` | Add methodology report rendering coverage for security/privacy | `plugins/product-agent-os/scripts/product_agent_os/methodology_report.py`, `tests/product_agent_os/test_methodology_report.py`, `tests/product_agent_os/test_methodology_audit.py` | Methodology audit reports render security/privacy recommendations, Codex Security scan status, approval boundaries, accepted gaps, residual risks and safe next actions without leaking secrets, prompts, traces, payment data, raw PII or private customer data. | `python -m unittest tests.product_agent_os.test_methodology_report tests.product_agent_os.test_methodology_audit -v` passes after implementation. |
| `T9-D11-M24` | Align compact checklist and verification policy | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, `docs/sources/product-agent-os-track-9-backlog.md` | The compact Step 6 uses verification without implicit commit, includes diff hygiene, and does not conflict with the matrix policy that commit, push and PR actions remain deferred unless explicitly requested. | `python tools\check_docs.py`; plan review confirms no remaining commit-policy contradiction. |

- [x] **Step 1: Add RED test for security gates**

Assert `security_privacy_compliance` gates include:

```python
[
    "security_sensitive_classification_present",
    "threat_surface_present",
    "security_risk_review_present",
    "asvs_mapping_present",
    "api_security_scheme_present",
    "authz_negative_tests_present",
    "secrets_policy_present",
    "data_classification_present",
    "privacy_impact_record_present",
    "external_write_approval_present",
    "abuse_rate_limit_review_present",
    "audit_logging_review_present",
    "supply_chain_review_present",
    "ci_permission_review_present",
    "ai_security_review_present",
    "compliance_overlay_present",
    "security_evidence_before_completion",
]
```

- [x] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing security gates.

- [x] **Step 3: Add security catalog and rules**

Rules:

- auth, PII, payment, secrets, external writes, production data, AI agents and compliance terms trigger security/privacy domain;
- source references are methodology evidence, not legal advice;
- compliance overlay records applicability and owner, not certification;
- secrets in generated outputs are blocked.

- [x] **Step 4: Add templates and detection**

Create all security templates listed in Files. Detect auth, OAuth, JWT, payment, billing, secrets, PII, rate limit, audit log, SBOM, package lock and CI permission signals.

- [x] **Step 5: Add false-positive fixtures**

Add or extend fixtures:

- security docs mention without code path creates `present_unverified`;
- payment/billing signals create `P1_high_risk`;
- docs-only repository with security article does not become regulated automatically.

- [x] **Step 6: Run verification without implicit commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_source_policy tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

Expected: focused tests, fixture eval, full unittest, compatibility check, docs check and diff hygiene pass. Commit is intentionally deferred until explicitly requested in the current working branch.

---

### Task 19: T9-D12 Delivery, Release & Operations Integration

**Files:**
- Source: `docs/methodologies/delivery-release-operations.md`
- Research: `docs/sources/methodology-research/delivery-release-operations.md`
- Modify: `plugins/product-agent-os/assets/methodology/methodology-catalog.json`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/discovery.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/methodology_report.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/templates.py`
- Modify: `plugins/product-agent-os/scripts/run_fixture_eval.py`
- Modify: `plugins/product-agent-os/assets/templates/artifact-templates/release-readiness.md`
- Modify: `plugins/product-agent-os/assets/templates/workflows/release-packet.md`
- Modify: `plugins/product-agent-os/assets/templates/workflows/release-packaging.md`
- Modify: `plugins/product-agent-os/assets/templates/pr/release-notes.md`
- Modify: `plugins/product-agent-os/assets/templates/artifact-templates/approval-record.md`
- Modify: `plugins/product-agent-os/assets/templates/artifact-templates/ci-permissions-review.md`
- Modify: `plugins/product-agent-os/assets/templates/artifact-templates/supply-chain-review.md`
- Modify: `plugins/product-agent-os/assets/templates/artifact-templates/sbom-manifest.md`
- Modify: `plugins/product-agent-os/assets/templates/artifact-templates/vulnerability-response-record.md`
- Modify: lifecycle skills under `plugins/product-agent-os/skills/`
- Modify: generated control-plane templates under `plugins/product-agent-os/assets/templates/control-plane/`
- Modify: eval templates under `plugins/product-agent-os/assets/templates/evals/`
- Modify: `plugins/product-agent-os/README.md`
- Modify: `docs/product-agent-os/methodology-intelligence.md`
- Modify: `docs/product-agent-os/behavioral-evals.md`
- Modify: `docs/product-agent-os/scenarios.md`
- Modify: `docs/product-agent-os/development-standards.md`
- Modify: `docs/sources/product-agent-os-track-9-backlog.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/deployment-plan.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/rollout-plan.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/rollback-recovery-plan.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/environment-matrix.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/ci-cd-workflow-inventory.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/versioning-policy.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/release-artifact-manifest.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/observability-map.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/slo-spec.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/operations-runbook.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/incident-record.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/postmortem.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/post-release-review.md`
- Test: `tests/product_agent_os/test_methodology_catalog.py`
- Test: `tests/product_agent_os/test_methodology_audit.py`
- Test: `tests/product_agent_os/test_discovery.py`
- Test: `tests/product_agent_os/test_methodology_report.py`
- Test: `tests/product_agent_os/test_infrastructure_templates.py`
- Test: `tests/product_agent_os/test_lifecycle_skills.py`
- Test: `tests/product_agent_os/test_behavioral_workflow_evals.py`
- Test: `tests/product_agent_os/test_fixture_eval_runner.py`
- Test: `tests/product_agent_os/test_fixtures.py`

Deep-audit update from `docs/methodologies/delivery-release-operations.md` and `docs/sources/methodology-research/delivery-release-operations.md`:

- The compact checklist below must use the full Delivery, Release & Operations source scope, not only the initial release-packaging subset. The domain covers release engineering, DORA, SRE/SLO, OpenTelemetry, Twelve-Factor build-release-run, CI/CD governance, GitHub environments, GitOps, progressive delivery, feature flags, incident/postmortem learning and automation promotion.
- T9-D12 must deepen the methodology layer without duplicating the Track 8 `release_packaging` scenario. Existing `release-readiness.md`, `release-packet.md`, `release-packaging.md`, `ci-evidence-record.md`, `ci-permissions-review.md`, backend operations artifacts and security/supply-chain artifacts should be reused or cross-linked where ownership already exists.
- Template naming is resolved in favor of source-backed names: `release-artifact-manifest.md`, `rollout-plan.md`, `ci-cd-workflow-inventory.md`, `post-release-review.md`, `incident-record.md` and `postmortem.md`. Plan-era names such as `artifact-manifest.md`, `rollout-strategy.md`, `ci-cd-governance.md`, `incident-response-path.md` and `post-release-measurement.md` are aliases only if existing tests or docs need compatibility.
- Delivery readiness must reject unsupported shortcuts: CI green means release ready, rollback is just revert, feature flags remove risk, GitOps is automatically safe, generated changelog is enough for users, DORA proves individual performance and repeatable automation is automatically safe.
- External release actions remain approval-bound: publish, tag, GitHub Release creation, artifact upload, deploy, package registry mutation, marketplace/store submission, PR creation, branch push, CI/CD environment mutation and active automation.
- Detection alone can only justify `present_unverified`; release-ready, deployed, published, operational-ready and automated claims require current evidence, owner evidence or an explicit accepted gap with owner, reason, review date, residual risk and follow-up condition.
- Second-pass audit adds deeper release-operation coverage: release mode selection, Twelve-Factor build-release-run separation, desktop/mobile distribution evidence, release communication, versioning tooling decisions, GitHub environment protection details, DORA five-metric design, blameless incident learning, observability/on-call tooling decisions, security handoff for release integrity and owner-reviewed evidence sufficiency.

This matrix maps the deep-audit findings to concrete implementation work. The numbered steps below remain the compact execution checklist; this table is the traceability layer for the focused T9-D12 slice.

| ID | Work | Files | Acceptance / Evidence | Verification |
| --- | --- | --- | --- | --- |
| `T9-D12-M0` | Refresh plan/backlog before implementation | `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, `docs/sources/product-agent-os-track-9-backlog.md` | Deep-audit deltas record full source scope, source-backed artifact names, false-positive risks, unsupported claims, approval boundaries, accepted-gap policy and exact verification commands. | `python tools\check_docs.py` |
| `T9-D12-M1` | Add RED catalog contract for `delivery_release_operations` | `tests/product_agent_os/test_methodology_catalog.py` | Test asserts gates, artifacts, eval fields, applies/not-applicable rules, maturity levels, complexity impact, Track 8 scenarios and overlaps from the source artifact. | Focused catalog test fails before catalog implementation on missing Delivery/Release/Operations gates or artifacts. |
| `T9-D12-M2` | Resolve delivery artifact naming compatibility | `plugins/product-agent-os/assets/methodology/methodology-catalog.json`, `plugins/product-agent-os/scripts/product_agent_os/templates.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Source-backed artifact names are canonical. Existing plan-era names are either removed before implementation or mapped as explicit aliases without conflicting ownership. | Catalog/template tests assert canonical names or explicit aliases. |
| `T9-D12-M3` | Fill `delivery_release_operations` catalog data | `plugins/product-agent-os/assets/methodology/methodology-catalog.json` | Domain records applies/not-applicable rules, maturity impact `baseline/team/production/regulated`, complexity impact, Track 8 scenario coverage, decision horizons, artifacts, gates, eval fields and overlaps with Product, Quality, Architecture, Backend, API, Database, AI/RAG, Security and Codex workflow domains. | `python -m unittest tests.product_agent_os.test_methodology_catalog -v` |
| `T9-D12-M4` | Add release and operations discovery signals | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `tests/product_agent_os/test_discovery.py` | Discovery records release, deploy, publish, tag, version, SemVer, changelog, release notes, artifact, Docker, Kubernetes, GitHub Actions, GitHub environments, GitOps, feature flag, rollout, rollback, SLO, observability, incident, postmortem, DORA and automation promotion signals as `present_unverified`. | Focused discovery tests assert signal packets and no readiness claims from detection alone. |
| `T9-D12-M5` | Implement domain applicability and severity routing | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | Release/deploy/publish/CI/deployment/package/version intent and workspace signals route the domain. Docs-only and internal-only work use reduced evidence; production, regulated, public package, SDK, plugin, marketplace/store, data migration, infrastructure and automation promotion raise priority. | Audit tests assert applicable, `present_unverified`, `not_applicable`, lightweight and production/high-risk transitions. |
| `T9-D12-M6` | Add false-positive and unsupported-claim handling | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | `CHANGELOG.md`, docs-only release notes, CI config, Dockerfile, health check, generated changelog, feature flag or GitOps file alone cannot prove readiness. Unsupported claims get explicit recommendations and replacement evidence. | Focused audit tests assert negative cases and unsupported-claim recommendations. |
| `T9-D12-M7` | Implement release scope gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/release-readiness.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `release_scope_present` records release type, target, owner, external boundary, lifecycle stage and docs-only/internal/production distinction. | Focused audit/template tests assert scope fields and blocker behavior when missing. |
| `T9-D12-M8` | Implement version, changelog and release-notes gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/versioning-policy.md`, `plugins/product-agent-os/assets/templates/workflows/release-packet.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `version_impact_present` and `changelog_release_notes_present` record SemVer or non-SemVer policy, compatibility impact, deprecation, migration guidance, user impact, known issues and Keep a Changelog categories where applicable. | Focused audit/template tests assert SemVer/non-SemVer and user-facing release note terms. |
| `T9-D12-M9` | Implement current release evidence gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/release-readiness.md`, `plugins/product-agent-os/assets/templates/workflows/release-packet.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `release_evidence_present` and `release_evidence_before_completion` require current build/test/docs/eval/runtime/artifact evidence, owner evidence or explicit gap before release-ready/deployed/published claims. Inspection-only output stays labeled. | Focused audit/template tests assert no release readiness from inspection-only or stale evidence. |
| `T9-D12-M10` | Implement artifact manifest and integrity gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/release-artifact-manifest.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `artifact_manifest_present` records artifact names, versions, creation command, storage location, retention and integrity notes; checksums, signatures, SBOM/provenance are required only when applicable. | Focused audit/template tests assert artifact manifest and docs-only no-integrity fallback behavior. |
| `T9-D12-M11` | Implement rollout and progressive delivery gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/rollout-plan.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `rollout_strategy_present` records immediate release, release train, staged rollout, feature flag, canary, blue-green, shadow traffic or manual promotion, with cohorts/traffic, promotion, abort criteria and blast radius. | Focused audit/template tests assert rollout depth and that progressive delivery is not forced on docs-only/internal-only work. |
| `T9-D12-M12` | Implement rollback and recovery gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/rollback-recovery-plan.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `rollback_recovery_present` records revert, redeploy previous artifact, disable flag, unpublish/yank, restore backup, compensate data or incident mitigation path, with command/manual procedure, owner and residual risk. | Focused audit/template tests assert release-type-specific rollback and reject "rollback is just revert" claims. |
| `T9-D12-M13` | Implement environment and external approval gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/environment-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/approval-record.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `environment_approval_boundary_present` and `external_release_approval_present` record dev/stage/prod/local/mobile/store/registry targets, branch/tag rules, secret boundaries and approval_required external actions. | Focused audit/template tests assert publish/tag/deploy/upload/PR/push/store/registry approvals. |
| `T9-D12-M14` | Implement CI/CD governance gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/ci-cd-workflow-inventory.md`, `plugins/product-agent-os/assets/templates/artifact-templates/ci-permissions-review.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `ci_cd_governance_present` records workflow names, triggers, permissions, secrets, environments, required reviewers, branch/tag restrictions, artifacts, cache, concurrency and external action pinning. | Focused audit/template tests assert least-privilege and no remote CI mutation without approval. |
| `T9-D12-M15` | Implement GitOps and desired-state operations gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/deployment-plan.md`, `plugins/product-agent-os/assets/templates/artifact-templates/environment-matrix.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | GitOps-style signals record desired-state source, reconciliation controller, drift behavior, approval path and rollback/revert behavior. GitOps presence stays `present_unverified` until owner evidence exists. | Focused audit/template tests assert GitOps safety terms and reject "GitOps automatically safe" claims. |
| `T9-D12-M16` | Implement feature flag lifecycle gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/rollout-plan.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Feature flag evidence records default value, owner, targeting rules, cleanup date, observability, kill switch and failure mode. Flag presence alone does not remove release risk. | Focused audit/template tests assert flag owner/cleanup/kill-switch behavior and unsupported flag claim rejection. |
| `T9-D12-M17` | Implement observability and SLO/operational gap gates | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/observability-map.md`, `plugins/product-agent-os/assets/templates/artifact-templates/slo-spec.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `observability_release_evidence_present` and `slo_or_operational_gap_present` record logs, metrics, traces, dashboards, alert owner, redaction, sampling, user journey, SLI, SLO, measurement source, alert policy or accepted no-telemetry/not-yet-production gap. | Focused audit/template tests assert no logs-only observability and no-production-telemetry fallback language. |
| `T9-D12-M18` | Implement operations runbook, incident and postmortem gates | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/operations-runbook.md`, `plugins/product-agent-os/assets/templates/artifact-templates/incident-record.md`, `plugins/product-agent-os/assets/templates/artifact-templates/postmortem.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `operations_runbook_present` and `incident_response_path_present` record deploy, rollback, first response, escalation, diagnostics, incident criteria, communication path and postmortem trigger. | Focused audit/template tests assert runbook/incident/postmortem terms and that quick rollback does not skip learning. |
| `T9-D12-M19` | Implement post-release and DORA learning gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/post-release-review.md`, `plugins/product-agent-os/assets/templates/artifact-templates/metric-spec.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `post_release_measurement_present` records metrics, support signals, defects, latency/cost, review date, DORA measurement source, anti-Goodhart warning and links back to product/reliability hypotheses. | Focused audit/template tests assert DORA terms and reject individual performance/quota claims. |
| `T9-D12-M20` | Implement automation promotion operations gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/automations/automation-candidate.md`, `plugins/product-agent-os/assets/templates/artifact-templates/skill-promotion-record.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `automation_manual_stability_present` records manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence and rollback/disable path. Active schedules remain out of scope. | Focused audit/template tests assert candidate-only automation and reject "repeatable means safe" claims. |
| `T9-D12-M21` | Register and render delivery templates | `plugins/product-agent-os/scripts/product_agent_os/templates.py`, `plugins/product-agent-os/assets/templates/artifact-templates/*.md`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | New delivery artifacts are staged under `.codex/artifact-templates/`; renderer file count delta is intentional and fixture eval includes `delivery_release_operations_contract_present`. | Renderer/template/fixture tests pass with updated file count. |
| `T9-D12-M22` | Add methodology report rendering coverage | `plugins/product-agent-os/scripts/product_agent_os/methodology_report.py`, `tests/product_agent_os/test_methodology_report.py`, `tests/product_agent_os/test_methodology_audit.py` | Methodology reports render delivery recommendations, statuses, approval boundaries, accepted gaps, residual risks, safe next actions and unsupported claims without implying external actions occurred. | `python -m unittest tests.product_agent_os.test_methodology_report tests.product_agent_os.test_methodology_audit -v` |
| `T9-D12-M23` | Update control-plane templates | `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`, `plugins/product-agent-os/assets/templates/control-plane/TEST.md`, `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `tests/product_agent_os/test_infrastructure_templates.py` | Generated control plane records delivery gates, statuses, owners, accepted gaps, approval boundaries, rollout, rollback, operations, incidents, DORA/post-release measurement and unsupported release claims. | Infrastructure template tests assert required fields and no unresolved placeholders. |
| `T9-D12-M24` | Update readiness and behavioral eval contracts | `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json`, `tests/product_agent_os/test_behavioral_workflow_evals.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Readiness records `delivery_release_operations`, conditional delivery gate, transition statuses and forbidden external actions; behavioral eval checks route, artifacts, required fields and unsupported shortcuts. | Behavioral/template tests assert expected/forbidden terms. |
| `T9-D12-M25` | Add fixture eval contract and checks | `plugins/product-agent-os/scripts/run_fixture_eval.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | `python-app` exposes `delivery_release_operations_contract_present`; `package-release` exposes delivery recommendations, approval boundary, artifact manifest, release evidence before completion and rollout/rollback/operations terms. | Focused fixture eval tests pass and renderer file count is updated. |
| `T9-D12-M26` | Add synthetic fixture coverage for false positives and approvals | `plugins/product-agent-os/assets/fixtures/*`, `tests/product_agent_os/test_fixtures.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | Fixtures cover docs-only release note, CI-only workflow, deployment manifest without execution, feature flag without owner, GitOps without approval path, package release approval, and no raw secrets/private data. | Fixture tests and fixture eval assert false positives, approvals and synthetic/privacy safety. |
| `T9-D12-M27` | Route delivery methodology through lifecycle skills | `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`, `plugins/product-agent-os/skills/requirements-author/SKILL.md`, `plugins/product-agent-os/skills/implementation-planner/SKILL.md`, `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`, `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`, `plugins/product-agent-os/skills/pr-release-operator/SKILL.md`, `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md`, `plugins/product-agent-os/skills/automation-promoter/SKILL.md` | Skills require planning-first delivery classification, release scope, version impact, evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary and automation candidate-only behavior. | Lifecycle skill tests assert wording and stop conditions. |
| `T9-D12-M28` | Sync Product-Agent OS docs and Track 9 backlog | `plugins/product-agent-os/README.md`, `docs/product-agent-os/methodology-intelligence.md`, `docs/product-agent-os/behavioral-evals.md`, `docs/product-agent-os/scenarios.md`, `docs/product-agent-os/development-standards.md`, `docs/sources/product-agent-os-track-9-backlog.md` | Current state records T9-D12 scope, artifacts, false-positive coverage, source-backed naming, approval boundaries, renderer file count delta, residual risks and next action `T9-D12-M30..M40`. Source registry changes only if new source-backed claims are added. | Product docs tests and `python tools\check_docs.py` pass. |
| `T9-D12-M30` | Implement release mode policy gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/release-readiness.md`, `plugins/product-agent-os/assets/templates/workflows/release-packet.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `release_mode_policy_present` records release train, continuous deployment, manual approval, release candidate, draft release or accepted non-release mode with cadence, owner, promotion trigger, freeze/cutoff and residual risk. | Focused audit/template tests assert mode-specific fields and that no mode is forced on docs-only/internal-only work. |
| `T9-D12-M31` | Implement build-release-run separation gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/deployment-plan.md`, `plugins/product-agent-os/assets/templates/artifact-templates/release-artifact-manifest.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `build_release_run_boundary_present` records immutable artifact, release identifier, runtime configuration boundary, environment-specific config injection and explicit exception when a stack cannot follow Twelve-Factor build-release-run separation. | Focused audit/template tests reject rebuild-per-environment readiness claims unless an accepted exception is recorded. |
| `T9-D12-M32` | Add platform distribution evidence gate | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/release-readiness.md`, `plugins/product-agent-os/assets/templates/workflows/release-packaging.md`, `plugins/product-agent-os/assets/templates/artifact-templates/environment-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/rollback-recovery-plan.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `platform_distribution_evidence_present` records desktop/mobile/native distribution needs: signing, notarization, app store review, installer/update path, rollback/yank path, phased rollout, crash reporting and platform owner evidence where applicable. | Focused audit/template tests assert platform-specific evidence and no desktop/mobile release-ready claim from generic package evidence alone. |
| `T9-D12-M33` | Strengthen release communication artifacts | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/pr/release-notes.md`, `plugins/product-agent-os/assets/templates/workflows/release-packet.md`, `plugins/product-agent-os/assets/templates/artifact-templates/release-readiness.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `release_communication_present` records audience, user impact, support contact, known issues, migration/deprecation note, changelog link and release-notes ownership. Generated notes alone remain insufficient. | Focused audit/template tests assert communication fields and reject changelog-only user communication. |
| `T9-D12-M34` | Add versioning tooling selector | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/versioning-policy.md`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `versioning_tooling_decision_present` records Conventional Commits, semantic-release, release-please, manual versioning or non-package policy as selected/rejected/deferred with reason and owner; tooling is optional, not mandatory. | Focused discovery/audit/template tests assert selector terms and no forced SemVer tooling for non-package work. |
| `T9-D12-M35` | Deepen GitHub environment controls | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/ci-cd-workflow-inventory.md`, `plugins/product-agent-os/assets/templates/artifact-templates/ci-permissions-review.md`, `plugins/product-agent-os/assets/templates/artifact-templates/environment-matrix.md`, `plugins/product-agent-os/assets/templates/artifact-templates/approval-record.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `github_environment_controls_present` records required reviewers, wait timers, branch/tag restrictions, custom protection rules, environment secrets, deployment targets and approval_required mutation boundary. | Focused audit/template tests assert GitHub environment protection terms and no remote CI/CD environment mutation without explicit approval. |
| `T9-D12-M36` | Specify DORA five-metric measurement design | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/post-release-review.md`, `plugins/product-agent-os/assets/templates/artifact-templates/metric-spec.md`, `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_behavioral_workflow_evals.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `dora_measurement_design_present` records change lead time, deployment frequency, failed deployment recovery time, change fail rate and deployment rework rate with data source, trend review and anti-Goodhart/team-only interpretation. | Focused audit/template/eval tests assert all five metrics and reject individual quota/performance claims. |
| `T9-D12-M37` | Add incident severity and blameless postmortem shape | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/incident-record.md`, `plugins/product-agent-os/assets/templates/artifact-templates/postmortem.md`, `plugins/product-agent-os/assets/templates/artifact-templates/operations-runbook.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `incident_postmortem_learning_present` records severity, timeline, detection, mitigation, customer/user impact, root causes, contributing factors, action items, owner/date and blameless wording. | Focused audit/template tests assert severity/postmortem fields and reject incident closure without learning path. |
| `T9-D12-M38` | Add observability and on-call tooling selector | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/observability-map.md`, `plugins/product-agent-os/assets/templates/artifact-templates/slo-spec.md`, `plugins/product-agent-os/assets/templates/artifact-templates/operations-runbook.md`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `observability_on_call_tooling_present` records OpenTelemetry plus Prometheus, Grafana, Sentry, Datadog, PagerDuty, Opsgenie or manual monitoring as selected/rejected/deferred with owner, alert path and accepted no-tooling gap. | Focused discovery/audit/template tests assert tooling selector terms and no single observability/on-call tool is forced. |
| `T9-D12-M39` | Add release integrity handoff to Security | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/release-artifact-manifest.md`, `plugins/product-agent-os/assets/templates/artifact-templates/supply-chain-review.md`, `plugins/product-agent-os/assets/templates/artifact-templates/sbom-manifest.md`, `plugins/product-agent-os/assets/templates/artifact-templates/vulnerability-response-record.md`, `plugins/product-agent-os/assets/templates/artifact-templates/release-readiness.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `release_integrity_security_handoff_present` records release signing, vulnerability response, license/NOTICE, SBOM/provenance and package/container integrity as satisfied, not-applicable, accepted gap or handed off to T9-D11 security ownership. | Focused audit/template tests assert cross-domain handoff and no duplication or bypass of security gates. |
| `T9-D12-M40` | Add owner-reviewed release evidence sufficiency | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/assets/templates/artifact-templates/release-readiness.md`, `plugins/product-agent-os/assets/templates/workflows/release-packet.md`, `plugins/product-agent-os/assets/templates/artifact-templates/approval-record.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `tests/product_agent_os/test_methodology_audit.py`, `tests/product_agent_os/test_infrastructure_templates.py` | `release_evidence_sufficiency_owner_reviewed` records owner acceptance that evidence is sufficient for the real release risk, or an accepted gap with owner, reason, review date, residual risk and stop condition. | Focused audit/template tests assert owner-reviewed sufficiency before release-ready/deployed/published claims. |
| `T9-D12-M29` | Run focused and final verification | `tests/product_agent_os/*`, `plugins/product-agent-os/scripts/run_fixture_eval.py`, `plugins/product-agent-os/scripts/run_transcript_eval.py`, `plugins/product-agent-os/scripts/validate_codex_compatibility.py`, `tools/check_docs.py` | Focused tests, fixture eval, full unittest, transcript eval, compatibility, docs check and diff hygiene pass before completion claim. Commit is intentionally deferred unless explicitly requested in the current branch. | `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_methodology_report tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures -v`; `python plugins\product-agent-os\scripts\run_fixture_eval.py`; `python -m unittest discover -s tests -p "test_*.py" -v`; `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json`; `python plugins\product-agent-os\scripts\validate_codex_compatibility.py`; `python tools\check_docs.py`; `git diff --check` |

**T9-D12 execution batching policy:**

- Execute T9-D12 rows in implementation batches: `M0..M9`, `M10..M19`, `M20..M29`, then `M30..M40`. All T9-D12 batches are complete; `M29` final verification was rerun after `M30..M40` before closure.
- After each batch, stop broad implementation work and report to the user: rows completed, files changed, checks run, results, unresolved risks and the next batch.
- Do not start the next T9-D12 batch until the previous batch report is written in the thread.
- Commit, push and PR actions remain deferred until explicitly requested by the user.

- [x] **Step 1: Add RED test for delivery gates**

Assert `delivery_release_operations` gates include:

```python
[
    "release_scope_present",
    "version_impact_present",
    "changelog_release_notes_present",
    "artifact_manifest_present",
    "release_evidence_present",
    "release_evidence_before_completion",
    "rollout_strategy_present",
    "rollback_recovery_present",
    "environment_approval_boundary_present",
    "external_release_approval_present",
    "ci_cd_governance_present",
    "slo_or_operational_gap_present",
    "observability_release_evidence_present",
    "operations_runbook_present",
    "incident_response_path_present",
    "post_release_measurement_present",
    "automation_manual_stability_present",
    "release_mode_policy_present",
    "build_release_run_boundary_present",
    "platform_distribution_evidence_present",
    "release_communication_present",
    "versioning_tooling_decision_present",
    "github_environment_controls_present",
    "dora_measurement_design_present",
    "incident_postmortem_learning_present",
    "observability_on_call_tooling_present",
    "release_integrity_security_handoff_present",
    "release_evidence_sufficiency_owner_reviewed",
    "delivery_unsupported_claims_rejected",
]
```

- [x] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing delivery gates.

- [x] **Step 3: Add delivery catalog, release rules and false-positive guards**

Rules:

- release intent, package manifests, CI, deployment manifests and version changes trigger delivery domain;
- publish, tag, release creation, artifact upload, deploy, PR creation, branch push, package registry, marketplace/store submission and CI/CD environment mutation require explicit approval;
- docs-only release uses reduced evidence;
- production release requires release mode policy, rollout, rollback/recovery, owner review, current release evidence, operations evidence, incident path and post-release learning;
- build-release-run separation is required for deployable artifacts unless a stack-specific exception is explicitly accepted;
- desktop/mobile/native release requires platform distribution evidence where applicable: signing, notarization, store review, installer/update rollback and crash reporting;
- DORA is a team/system trend design, not an individual performance quota;
- release integrity concerns such as signing, vulnerability response, license/NOTICE, SBOM and provenance hand off to T9-D11 Security instead of being silently waived;
- CI config, Dockerfile, changelog, feature flag, GitOps files or generated release notes alone never prove readiness.

- [x] **Step 4: Add templates and detection**

Create all delivery templates listed in Files. Detect package/version files, changelog, CI, deployment manifests, release notes, package registry config, Docker/Kubernetes, GitHub environments, GitOps, feature flags, observability, SLOs, incident/postmortem, automation promotion, release mode, release candidate/draft, Conventional Commits, semantic-release, release-please, signing/notarization/store review, crash reporting, environment protection, on-call tooling, SBOM/provenance/license/NOTICE and vulnerability-response signals.

- [x] **Step 5: Add fixture eval checks**

Existing `package-release` fixture must expose:

- `delivery_release_operations_contract_present`;
- release approval boundary;
- artifact manifest recommendation;
- release evidence before completion;
- rollout, rollback, CI/CD governance, operations, incident and post-release learning terms;
- release mode, build-release-run, platform distribution, DORA five-metric design, blameless postmortem, tooling selector, release integrity handoff and owner-reviewed evidence sufficiency terms;
- false-positive fixtures for docs-only release notes, CI-only workflow, deployment manifests without execution, feature flag without owner, GitOps without approval path, generic mobile signing mention without platform evidence, DORA as individual quota, and tooling files without owner evidence.

- [x] **Step 6: Run verification without implicit commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_methodology_report tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures tests.product_agent_os.test_product_agent_os_docs -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

Result: focused tests ran 298 tests with `OK`; fixture eval exited `0` with 66 fixtures and renderer file count 186; full unittest ran 478 tests with `OK`; transcript eval passed 5 sessions; compatibility returned `status: compatible`; docs check passed; diff hygiene exited `0`. Commit is intentionally deferred until explicitly requested in the current working branch.

---

### Task 20: Cross-Domain Synthesis

**Files:**
- Modify: `plugins/product-agent-os/assets/methodology/methodology-catalog.json`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/methodology_catalog.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/methodology_report.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/discovery.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/templates.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`
- Modify: `plugins/product-agent-os/scripts/run_fixture_eval.py`
- Modify: `plugins/product-agent-os/assets/templates/control-plane/REQUIREMENTS.md`
- Modify: `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`
- Modify: `plugins/product-agent-os/assets/templates/control-plane/TEST.md`
- Modify: `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`
- Modify: `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`
- Modify: `plugins/product-agent-os/assets/templates/evals/project-readiness.json`
- Modify: `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json`
- Modify: `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`
- Modify: `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`
- Modify: `plugins/product-agent-os/skills/requirements-author/SKILL.md`
- Modify: `plugins/product-agent-os/skills/implementation-planner/SKILL.md`
- Modify: `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`
- Modify: `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`
- Modify: `plugins/product-agent-os/skills/docs-maintainer/SKILL.md`
- Modify: `plugins/product-agent-os/skills/pr-release-operator/SKILL.md`
- Modify: `plugins/product-agent-os/skills/agent-team-designer/SKILL.md`
- Modify: `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md`
- Modify: `plugins/product-agent-os/skills/automation-promoter/SKILL.md`
- Modify: `tests/product_agent_os/test_methodology_catalog.py`
- Modify: `tests/product_agent_os/test_methodology_audit.py`
- Modify: `tests/product_agent_os/test_methodology_report.py`
- Modify: `tests/product_agent_os/test_discovery.py`
- Modify: `tests/product_agent_os/test_infrastructure_templates.py`
- Modify: `tests/product_agent_os/test_lifecycle_skills.py`
- Modify: `tests/product_agent_os/test_behavioral_workflow_evals.py`
- Modify: `tests/product_agent_os/test_fixture_eval_runner.py`
- Modify: `tests/product_agent_os/test_fixtures.py`
- Modify: `tests/product_agent_os/test_product_agent_os_docs.py`
- Modify: `docs/sources/product-agent-os-track-9-backlog.md`
- Modify: `docs/product-agent-os/methodology-intelligence.md`
- Modify: `docs/product-agent-os/behavioral-evals.md`
- Modify: `docs/product-agent-os/development-standards.md`
- Create: `tests/product_agent_os/test_methodology_synthesis.py`

**Task matrix:**

| Row | Slice | Files | Критерии приемки | Verification |
| --- | --- | --- | --- | --- |
| `T9-S-M0` | Record current synthesis baseline | `docs/sources/product-agent-os-track-9-backlog.md`, `tests/product_agent_os/test_methodology_synthesis.py` | Backlog records the current duplicate gate, artifact and eval-field inventory before implementation: duplicate gates include `accepted_gap_recorded`, `automation_manual_stability_present`, `bounded_context_architecture_boundary_trace` and `external_write_approval_present`; duplicate artifacts include `approval-record.md`, `security-risk-review.md`, `api-contract-review.md`, `test-eval-matrix.md`, `release-readiness.md` and `architecture-overview.md`. Current fixture symptoms are recorded: backend FSD-like directories can trigger frontend P0s, security/payment can be ordered behind generic quality strategy, and RAG ingestion can miss AI/RAG routing when no explicit `rag/` directory exists. | RED synthesis tests assert the baseline gaps before implementation. |
| `T9-S-M1` | Add RED synthesis contract tests | `tests/product_agent_os/test_methodology_synthesis.py` | Tests assert shared gate ownership, artifact ownership, priority tie-breakers, conflict rules, grouped recommendation shape, semantic evidence sufficiency ownership, false-positive routing and safe-next-action ordering. Tests cover docs-only, backend FSD-like folders, CI-only workflow, tooling-only release, security/payment, package release and AI/RAG data/security overlap fixtures. | `python -m unittest tests.product_agent_os.test_methodology_synthesis -v` fails on missing synthesis layer. |
| `T9-S-M2` | Add machine-readable synthesis catalog contract | `plugins/product-agent-os/assets/methodology/methodology-catalog.json`, `plugins/product-agent-os/scripts/product_agent_os/methodology_catalog.py`, `tests/product_agent_os/test_methodology_catalog.py` | Catalog keeps existing domain `gates`, `artifacts` and `eval_fields` as string lists, and adds a top-level synthesis block with shared gate owners, consumer domains, artifact owners, artifact aliases, deferred-source artifact decisions, priority tie-breakers, conflict rules, false-positive rules, semantic evidence sufficiency rules, owner-question dedupe rules and supported output packet keys. Validator rejects missing owners, unknown domains, unknown priorities, unknown artifact ids and conflict rules that point to nonexistent gates. | Catalog tests assert schema compatibility and synthesis metadata. |
| `T9-S-M3` | Normalize source artifact compatibility and renderer aliases | `plugins/product-agent-os/assets/methodology/methodology-catalog.json`, `plugins/product-agent-os/scripts/product_agent_os/templates.py`, `tests/product_agent_os/test_methodology_synthesis.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Every source methodology artifact mention is classified as canonical template, alias, existing non-template project artifact, or deferred candidate with owner and reason. Source-era names such as `context-map.md`, `agent-eval-case.md`, `skill-candidate.md`, `ui-flow-spec.md`, `visual-evidence-packet.md`, `threat-model.md`, `asvs-mapping.md`, `runbook.md`, `slo.md` and `CHANGELOG.md` cannot appear as unexplained missing templates. Catalog aliases and `templates.py` renderer aliases stay consistent where renderer aliases exist. | Synthesis and infrastructure-template tests assert alias targets exist or are explicitly deferred. |
| `T9-S-M4` | Implement synthesis module | `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`, `tests/product_agent_os/test_methodology_synthesis.py` | New module exposes deterministic pure functions for loading synthesis metadata, validating shared ownership, grouping recommendations by artifact, merging evidence lists, preserving source domains/gates, resolving priority ties, deduping owner questions and returning a `methodology_synthesis` packet. No workspace writes, network calls, model calls, external approvals or renderer side effects are introduced. | Synthesis tests pass for pure functions with synthetic recommendation packets. |
| `T9-S-M5` | Integrate recommendation resolver into audit output | `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_audit.py` | `build_methodology_audit()` preserves existing output keys and adds stable grouped output such as `recommendation_groups` and `methodology_synthesis` without breaking current fixture eval consumers. Highest priority per artifact is preserved, evidence is deduplicated, reasons and gates are not lost, `questions_for_owner` are deduped, and `delivery_map.next_action_map` uses resolved safe next actions. | Audit tests assert grouped output, stable existing keys, report/JSON alignment and priority ordering. |
| `T9-S-M6` | Add risk-aware safe-next-action policy | `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_methodology_synthesis.py`, `tests/product_agent_os/test_methodology_audit.py` | When several blockers exist, security, approval, release/external-write, production-data and destructive-change blockers outrank generic `quality-strategy.md` blockers for `safe_next_action`. Generic quality evidence remains visible in recommendation groups, but it does not hide a more specific high-risk owner action. | Tests assert security/payment chooses `approval-record.md` or `security-risk-review.md`, package release chooses release approval/readiness, and docs-only work keeps the smallest verification action. |
| `T9-S-M7` | Normalize semantic evidence sufficiency | `plugins/product-agent-os/assets/methodology/methodology-catalog.json`, `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`, `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`, `plugins/product-agent-os/assets/templates/control-plane/TEST.md`, `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`, `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`, `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json`, `tests/product_agent_os/test_methodology_synthesis.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_behavioral_workflow_evals.py` | A shared owner-review rule covers high-risk, production, release, security-sensitive, AI behavior and public-contract slices. Required evidence is owner review that recorded tests/evals/manual/runtime evidence are sufficient for real project risk, or `explicit_gap_accepted` with owner, reason, review date, downstream risk and follow-up condition. Domain-specific gates consume the shared rule without pretending a template proves semantic sufficiency. Generated control-plane and eval assets expose the shared rule consistently. | Synthesis, infrastructure-template and behavioral-eval tests assert accepted-gap shape and consumer domains. |
| `T9-S-M8` | Align discovery, methodology applicability and audit synthesis packets | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_methodology_audit.py` | Discovery output carries synthesized methodology fields without losing existing `methodology_applicability`, `methodology_intelligence`, `methodology_domains`, `methodology_map` or usage-mode routing. `present_unverified` remains distinct from readiness evidence, and detection-only signals cannot become `present_verified`. | Discovery tests assert packet shape, backward compatibility and no readiness upgrade from detection alone. |
| `T9-S-M9` | Strengthen cross-domain false-positive routing | `plugins/product-agent-os/scripts/product_agent_os/discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`, `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`, `plugins/product-agent-os/assets/fixtures/*`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_fixture_eval_runner.py`, `tests/product_agent_os/test_fixtures.py` | Backend FSD-like folders do not trigger frontend blockers without UI/runtime evidence; CI-only workflow does not imply release/security P0 unless publish/deploy/secrets/external mutation evidence exists; docs-only release notes and tooling-only release files stay `present_unverified`; simple docs-only/internal CLI work receives no frontend/backend/API/database/security/release hard blockers. | Discovery, fixture and fixture-runner tests assert negative routing and no raw secrets/private data in new fixtures. |
| `T9-S-M10` | Add overlap fixtures for mixed-risk projects | `plugins/product-agent-os/assets/fixtures/*`, `plugins/product-agent-os/scripts/run_fixture_eval.py`, `tests/product_agent_os/test_fixture_eval_runner.py`, `tests/product_agent_os/test_fixtures.py` | Fixtures cover: small app with PII but low code complexity, complex monorepo without production users, internal CLI with no UI/API/release hard blockers, AI/RAG project with database lineage and security/privacy overlap, package release with security handoff, source artifact alias/deferred mapping, and owner-question dedupe. Fixture eval exposes named checks for `cross_domain_synthesis_contract_present`, `semantic_evidence_sufficiency_contract_present`, `safe_next_action_risk_ordered`, `source_artifact_mapping_contract_present` and `cross_domain_false_positive_guards_present`. | Fixture runner tests pass and `python plugins\product-agent-os\scripts\run_fixture_eval.py` returns `ok: true`. |
| `T9-S-M11` | Render grouped synthesis in methodology reports | `plugins/product-agent-os/scripts/product_agent_os/methodology_report.py`, `tests/product_agent_os/test_methodology_report.py` | Markdown reports include a Cross-Domain Synthesis section with grouped artifact recommendations, owner domain, consumer domains, merged gates, approval boundary, accepted-gap option, residual risk, source artifact alias/deferred decisions and safe next action. Reports still redact local paths, secrets, private customer data, raw PII and payment data, and still state that no external action is implied. | Report tests assert grouped output, redaction, report/JSON alignment and external-action boundary text. |
| `T9-S-M12` | Route synthesized packets through lifecycle skills | `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`, `plugins/product-agent-os/skills/requirements-author/SKILL.md`, `plugins/product-agent-os/skills/implementation-planner/SKILL.md`, `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`, `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`, `plugins/product-agent-os/skills/docs-maintainer/SKILL.md`, `plugins/product-agent-os/skills/pr-release-operator/SKILL.md`, `plugins/product-agent-os/skills/agent-team-designer/SKILL.md`, `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md`, `plugins/product-agent-os/skills/automation-promoter/SKILL.md`, `tests/product_agent_os/test_lifecycle_skills.py` | Lifecycle skills consume grouped recommendations, owner domains, consumer domains, semantic sufficiency status, alias/deferred artifact ledger and risk-aware safe next action. Skills must not dump every methodology gate, must not scaffold before approval and must not treat detection as verification. | Lifecycle skill tests assert wording and stop conditions. |
| `T9-S-M13` | Sync docs and behavioral eval contracts | `docs/sources/product-agent-os-track-9-backlog.md`, `docs/product-agent-os/methodology-intelligence.md`, `docs/product-agent-os/behavioral-evals.md`, `docs/product-agent-os/development-standards.md`, `tests/product_agent_os/test_product_agent_os_docs.py` | Docs explain the synthesis layer, shared ownership, grouped recommendations, false-positive protection, source artifact compatibility, semantic evidence sufficiency and approval-bound behavior. Backlog records deduplicated gates, merged artifacts, known accepted overlaps, false-positive fixture coverage, alias/deferred decisions and residual risks. Source registry changes only if new external source-backed claims are added. | Product docs tests and `python tools\check_docs.py` pass. |
| `T9-S-M14` | Final synthesis verification and handoff | `tests/product_agent_os/*`, `plugins/product-agent-os/scripts/run_fixture_eval.py`, `plugins/product-agent-os/scripts/run_transcript_eval.py`, `plugins/product-agent-os/scripts/validate_codex_compatibility.py`, `tools/check_docs.py`, `RUNLOG.md` | Focused synthesis suite, fixture eval, full unittest, transcript eval, compatibility, docs check and diff hygiene pass before any completion claim. Commit, push and PR actions remain deferred unless explicitly requested in the current branch. | Commands in Step 11 exit `0`; RUNLOG records evidence, unresolved semantic risks and next action `Task 21`. |

**Task 20 execution policy:**

- Keep synthesis implementation read-only: no staged artifacts, hooks, automations, external writes, CI mutations, package publishing, GitHub actions or source-of-truth updates outside checked-in docs.
- Preserve existing audit output keys so Track 9 fixture eval and runtime runner checks do not regress before Task 21.
- Prefer additive catalog metadata over changing all domain `gates`, `artifacts` and `eval_fields` from strings to objects.
- Run RED before implementation and record expected failures in the backlog or RUNLOG.
- Do not commit, push or open PR unless the user explicitly asks for that action.

- [ ] **Step 0: Record current synthesis baseline**

Before implementation, run a read-only inventory and record the result in `docs/sources/product-agent-os-track-9-backlog.md`.

Run:

```powershell
@'
import json
from collections import defaultdict
from pathlib import Path

catalog = json.loads(Path("plugins/product-agent-os/assets/methodology/methodology-catalog.json").read_text(encoding="utf-8"))

def duplicates(kind):
    seen = defaultdict(list)
    for domain in catalog["domains"]:
        for item in domain[kind]:
            seen[item].append(domain["id"])
    return {key: value for key, value in seen.items() if len(value) > 1}

print("duplicate_gates", duplicates("gates"))
print("duplicate_artifacts", duplicates("artifacts"))
print("duplicate_eval_fields", duplicates("eval_fields"))
'@ | python -
```

Expected: output includes duplicate gate, artifact and eval-field inventories that match the current pre-synthesis state.

- [ ] **Step 1: Add RED synthesis tests**

Create `tests/product_agent_os/test_methodology_synthesis.py` with tests that assert:

- no duplicate gate ids across domains unless listed in `overlaps`;
- no duplicate artifact ids with conflicting owners;
- `security_risk_review_present` maps to security domain as owner and backend/API/data/AI/delivery as consumers;
- `evidence_before_completion` concepts are normalized under quality/Codex/delivery rules;
- semantic evidence sufficiency review is normalized as a shared owner-review gate for high-risk, production, release, security-sensitive, AI behavior and public-contract slices; it can be satisfied by explicit owner review evidence or an accepted gap with owner, reason, review date, downstream risk and follow-up condition;
- mutually exclusive recommendations cannot both be `P0_blocker` for the same workspace;
- simple docs-only fixture receives no frontend/backend/API/database/security/release hard blockers;
- backend FSD-like folders do not trigger frontend P0/P1 recommendations without UI/runtime evidence;
- CI-only workflow does not trigger release/security P0 without publish, deploy, secret, external-write or CI environment mutation evidence;
- security/payment fixtures choose a security or approval safe next action before generic quality strategy;
- AI/RAG plus data lineage fixtures route AI/RAG, database and security/privacy overlap as `present_unverified` rather than proof.

- [ ] **Step 2: Run RED synthesis tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_synthesis -v
```

Expected: fail until synthesis rules exist.

- [ ] **Step 3: Add synthesis catalog metadata, source artifact compatibility and validator coverage**

Modify catalog:

- add owner domain for shared gates;
- add consumer domains for shared gates;
- add artifact owner and consumer metadata;
- add artifact alias metadata for plan-era names that map to canonical templates;
- classify every methodology-source artifact mention as canonical template, alias, existing non-template project artifact, or deferred candidate with owner and reason;
- add semantic evidence sufficiency owner-review rules for high-risk, production, release, security-sensitive, AI behavior and public-contract slices;
- add conflict rules for mutually exclusive frameworks;
- add safe-next-action tie-breakers for approval, security, release, production data and destructive changes;
- add false-positive rules for docs-only, internal CLI, backend FSD-like directories, CI-only, release tooling-only and deployment manifest-only work;
- add owner-question dedupe rules and supported output packet keys;
- merge duplicate artifacts where one template can serve multiple domains;
- keep domain-specific templates only when the evidence model differs;
- keep catalog aliases consistent with `templates.py` renderer aliases where renderer aliases exist.

- [ ] **Step 4: Add synthesis module and recommendation resolver**

Create `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py` and modify `methodology_audit.py` to sort, group and resolve recommendations:

1. `P0_blocker`;
2. `P1_high_risk`;
3. `P2_recommended`;
4. `P3_optional_maturity`;
5. `not_applicable`.

When two recommendations target the same artifact, keep the highest priority and merge evidence requirements without duplicating text. Preserve every source gate and domain in the grouped output. Expose enough metadata for reports and fixture evals to distinguish owner domain, consumer domains, approval boundary, accepted-gap option and residual risk.

- [ ] **Step 5: Add risk-aware safe-next-action policy**

Safe next action must prefer the highest-risk specific action over generic quality strategy when both exist:

- security/payment/external write -> `approval-record.md`, `security-risk-review.md` or another security owner artifact;
- package release/deploy/publish -> release approval/readiness artifact;
- production data/destructive migration -> database approval/rollback artifact;
- AI tool side effects or model release -> AI/RAG approval/eval artifact;
- docs-only/internal CLI -> smallest verification command or accepted gap.

- [ ] **Step 6: Normalize semantic evidence sufficiency and generated eval assets**

Update `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `project-readiness.json` and `behavioral-workflows.json` so shared semantic sufficiency is represented consistently:

- owner review confirms recorded tests, evals, manual checks and runtime evidence are sufficient for the actual project risk;
- accepted gaps require owner, reason, review date, downstream risk and follow-up condition;
- high-risk, production, release, security-sensitive, AI behavior and public-contract slices consume the shared rule;
- generated assets must not imply that a template alone proves semantic sufficiency.

- [ ] **Step 7: Align discovery, methodology applicability and false-positive routing**

Modify `discovery.py`, `methodology_audit.py` and synthesis rules so:

- `methodology_applicability`, `methodology_intelligence`, `methodology_domains`, `methodology_map`, `recommendation_groups` and `methodology_synthesis` remain backward-compatible packets;
- `present_unverified` stays distinct from readiness evidence;
- detection-only signals never become `present_verified`;
- backend FSD-like folders do not trigger frontend blockers without UI/runtime evidence;
- CI-only workflow does not imply release/security P0 without publish, deploy, secret, external-write or CI environment mutation evidence;
- docs-only release notes, tooling-only release files and deployment manifests stay `present_unverified` unless stronger evidence exists;
- simple docs-only/internal CLI work receives no frontend/backend/API/database/security/release hard blockers.

- [ ] **Step 8: Add cross-domain fixtures**

Add or extend fixtures for:

- docs-only no heavy methodology;
- internal CLI with no frontend/API/release hard blockers;
- small app with PII but low code complexity;
- complex monorepo without production users;
- AI/RAG project with data and security overlap;
- package release with security handoff;
- source artifact alias/deferred mapping;
- owner-question dedupe.

- [ ] **Step 9: Render synthesis in methodology reports and route lifecycle skills**

Modify `methodology_report.py` so reports show:

- grouped recommendations by artifact;
- owner domain and consumer domains;
- merged gates and evidence requirements;
- approval boundary and accepted-gap option;
- source artifact alias/deferred decisions;
- safe next action selected after synthesis;
- external action status remains read-only and approval-bound.

Update lifecycle skills so they consume grouped recommendations, owner domains, consumer domains, semantic sufficiency status, alias/deferred artifact ledger and risk-aware safe next action. Skills must not dump every methodology gate, scaffold before approval, or treat detection as verification.

- [ ] **Step 10: Update Track 9 backlog and docs**

Update `docs/sources/product-agent-os-track-9-backlog.md`:

- record deduplicated gates;
- record merged artifacts;
- record known accepted overlaps;
- record semantic evidence sufficiency review ownership, accepted-gap shape and consumer domains;
- record final false-positive coverage;
- record source artifact alias/deferred decisions;
- record safe-next-action tie-breakers and residual risks.

Update Product-Agent OS docs:

- `docs/product-agent-os/methodology-intelligence.md`: explain synthesis output and grouped recommendations;
- `docs/product-agent-os/behavioral-evals.md`: add synthesis fixture/eval contract;
- `docs/product-agent-os/development-standards.md`: add shared semantic evidence sufficiency and false-positive routing rules.

- [ ] **Step 11: Run synthesis verification**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_synthesis tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_methodology_report tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures tests.product_agent_os.test_product_agent_os_docs -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

Expected: all commands exit `0`.

- [ ] **Step 12: Prepare commit scope only if requested**

If the user explicitly asks for a commit after verification, use this scope:

```powershell
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md docs\product-agent-os\methodology-intelligence.md docs\product-agent-os\behavioral-evals.md docs\product-agent-os\development-standards.md RUNLOG.md
git commit -m "feat: synthesize track 9 methodology domains"
```

Expected: commit succeeds only when explicitly requested; otherwise leave changes uncommitted and report verification evidence.

---

### Task 21: Update Runtime Runner And Finish Options

**Files:**
- Modify: `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`
- Modify: `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`
- Modify: `plugins/product-agent-os/scripts/codex_runtime_runner/guards.py`
- Modify: `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`
- Modify: `plugins/product-agent-os/scripts/run_codex_runtime_runner.py`
- Modify: `plugins/product-agent-os/scripts/validate_codex_runtime_runner.py`
- Modify: `plugins/product-agent-os/scripts/run_fixture_eval.py`
- Add or modify: `plugins/product-agent-os/assets/fixtures/codex-runner-*`
- Modify: `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`
- Modify: `plugins/product-agent-os/assets/templates/control-plane/TEST.md`
- Modify: `plugins/product-agent-os/assets/templates/control-plane/EVALS.md`
- Modify: `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md`
- Modify: `plugins/product-agent-os/assets/templates/evals/project-readiness.json`
- Modify: `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json`
- Modify: `plugins/product-agent-os/assets/templates/artifact-templates/agent-task-packet.md`
- Modify: `tests/product_agent_os/test_codex_runtime_runner_contracts.py`
- Modify: `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`
- Modify: `tests/product_agent_os/test_codex_runtime_runner_cli.py`
- Modify: `tests/product_agent_os/test_codex_runtime_runner_fixture_eval.py`
- Modify when templates/evals/docs change: `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_behavioral_workflow_evals.py`, `tests/product_agent_os/test_product_agent_os_docs.py`
- Modify when user-facing runtime behavior changes: `plugins/product-agent-os/README.md`, `docs/product-agent-os/technical.md`, `docs/product-agent-os/architecture.md`
- Modify when evidence changes: `docs/sources/product-agent-os-track-9-backlog.md`, `RUNLOG.md`

| ID | Task | Files | Acceptance | Verification |
| --- | --- | --- | --- | --- |
| `T9-R-M0` | Define compact runtime methodology packet schema | `contracts.py`, `test_codex_runtime_runner_contracts.py` | Route packets can carry a bounded additive `methodology_packet` without changing runner schema version or existing top-level result field order. Required compact keys: `methodology_domains`, `methodology_recommendations`, `recommendation_groups`, `questions_for_owner`, `safe_next_action`, `semantic_evidence_sufficiency`, `source_artifact_ledger`, `write_policy`, `status`. | RED contract tests fail before schema support and pass after implementation. |
| `T9-R-M1` | Add RED propagation tests from discovery/audit to runtime route | `test_codex_runtime_runner_state_routes.py`, `test_codex_runtime_runner_fixture_eval.py` | Tests prove `run_contract()`/`plan_route()` do not drop `methodology_intelligence`, `recommendation_groups`, owner questions or risk-aware `safe_next_action` produced by Track 9 audit. | `python -m unittest tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_state_routes -v` fails RED before route support. |
| `T9-R-M2` | Add methodology packet validation and size/type guards | `contracts.py`, `guards.py`, `test_codex_runtime_runner_contracts.py` | Invalid packet types, missing required compact keys, oversized recommendation/group/question lists and non-read-only methodology packet write policy produce deterministic validation errors without traceback. | Contract tests assert valid and malformed packets. |
| `T9-R-M3` | Attach methodology packet to runtime routes | `routes.py`, `cli.py`, `test_codex_runtime_runner_state_routes.py` | `plan_route()` accepts optional methodology intelligence, emits `methodology_packet`, preserves `usage_mode`, `behavioral_route_inputs`, existing lifecycle statuses and current `route_ready`/`needs_context`/`needs_approval` behavior. No model calls, network calls or standalone runtime behavior are introduced. | Focused state-route tests pass. |
| `T9-R-M4` | Define finish options model | `routes.py`, `contracts.py`, `test_codex_runtime_runner_state_routes.py` | Route packets include ordered `finish_options`: `read_only_audit`, `ask_owner`, `stage_proposal`, `request_approval`, `run_verification`, `stop_blocked`. Options are derived from methodology packet risk, approval boundary and evidence status, not from filename-only detection. | Tests assert finish options for read-only, staged-only, approved-write and blocked paths. |
| `T9-R-M5` | Separate recommendation from staged artifact generation | `guards.py`, `routes.py`, `test_codex_runtime_runner_state_routes.py` | A methodology recommendation can suggest an artifact, but runtime route does not generate staged artifacts unless approval/stage target evidence exists. Missing approval yields `needs_approval` or a `request_approval` finish option, not a write. | Guard tests assert no staged generation from recommendation-only packets. |
| `T9-R-M6` | Block completion/readiness claims from detection-only methodology signals | `guards.py`, `contracts.py`, `test_codex_runtime_runner_contracts.py` | `completed` status and finish claims require current verification evidence. `present_unverified` methodology detection, recommendation text, or source artifact presence cannot satisfy completion evidence. | Tests assert `verification_evidence:required_for_completed` plus methodology-specific detection-only errors. |
| `T9-R-M7` | Block external writes and irreversible actions from recommendations | `guards.py`, `test_codex_runtime_runner_state_routes.py`, fixture eval | Recommendations mentioning publish, deploy, tag, release creation, PR/push, package registry mutation, marketplace/store submission, security scan, production data access, DB migration or external-system mutation produce approval-bound finish options and no external action. | Guard and fixture tests assert `approval_required`/`needs_approval` and no external mutation. |
| `T9-R-M8` | Block automation promotion without maturity evidence | `guards.py`, `test_codex_runtime_runner_state_routes.py`, fixture eval | Automation-related methodology recommendations require manual stability and value/maturity evidence before `automation-promoter` or automation finish options can advance. Active/scheduled automation remains blocked without explicit approval. | Runtime guard tests plus existing active automation fixture remain green. |
| `T9-R-M9` | Enforce redaction for methodology route payloads | `cli.py`, `contracts.py`, `test_codex_runtime_runner_contracts.py`, fixture eval | `methodology_packet`, owner questions, source artifact ledger and `safe_next_action` pass the existing redaction/no-secrets policy before JSON output. Absolute local paths, secret-like literals, private chat/customer markers and raw PII/payment markers are redacted or blocked. | Redaction tests and `codex-runner-secret-redaction` fixture pass. |
| `T9-R-M10` | Add runtime methodology fixtures | `plugins/product-agent-os/assets/fixtures/codex-runner-*`, `test_codex_runtime_runner_fixture_eval.py` | Add synthetic fixtures for: methodology synthesis ready route, staged artifact approval required, detection-only completion blocked, external-write recommendation blocked, automation maturity missing, malformed methodology packet. Fixtures contain no secrets/private data. | Fixture completeness and runner fixture tests pass. |
| `T9-R-M11` | Add named fixture eval checks for runtime methodology behavior | `run_fixture_eval.py`, `test_codex_runtime_runner_fixture_eval.py` | Fixture eval exposes stable checks: `runtime_methodology_packet_present`, `runtime_finish_options_approval_bound`, `runtime_detection_not_completion`, `runtime_external_write_blocked`, `runtime_automation_maturity_required`, `runtime_methodology_redaction_enforced`. | `python plugins\product-agent-os\scripts\run_fixture_eval.py` exits `0` and new checks are true. |
| `T9-R-M12` | Add malformed packet fallback behavior | `contracts.py`, `guards.py`, `cli.py`, tests | Malformed methodology packets return `blocked` or `failed` with redacted errors; runner does not emit traceback and does not downgrade validation errors to warnings when writes or completion claims are involved. | Contract/CLI-style tests assert stable error codes and redacted output. |
| `T9-R-M13` | Run full runtime verification | runtime tests, fixture eval, transcript eval, compatibility, docs check | Focused runtime suite, fixture eval, full unittest, transcript eval, Codex compatibility, docs check and diff hygiene pass before any completion claim. Strict MkDocs is required only if nav, Mermaid, Markdown extensions or MkDocs config change. | Commands listed in Task 21 verification policy exit `0`. |
| `T9-R-M14` | Sync Track 9 evidence and next action | `docs/sources/product-agent-os-track-9-backlog.md`, `RUNLOG.md`, optionally root control-plane files if current state changes | Backlog/RUNLOG record RED/GREEN evidence, fixture count, runtime methodology checks, residual risks and the next Task 21 expansion action `T9-R-M16..M25`; `Task 22` starts only after Task 21 expansion/closure. Source registry changes only if new external source-backed claims are added. | `python tools\check_docs.py` and `git diff --check` pass after docs sync. |
| `T9-R-M15` | Keep commit/push optional and explicit-only | plan, final handoff | Commit is not part of required implementation in this repository unless explicitly requested by the user. If requested, commit only after verification and with staged scope limited to Task 21 files. | No `git add`, commit, push or PR without explicit user request. |
| `T9-R-M16` | Add CLI and validator contract tests for methodology packet JSON output | `run_codex_runtime_runner.py`, `validate_codex_runtime_runner.py`, `test_codex_runtime_runner_cli.py` | CLI stdout and `--output` result include compact methodology packet and finish options after redaction; validator accepts additive schema v1 result and rejects malformed packets with stable errors. | CLI tests fail RED before support and pass after implementation. |
| `T9-R-M17` | Update generated control-plane templates for runtime methodology packet | control-plane templates, `test_infrastructure_templates.py` | Generated `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md` include runtime methodology packet, finish options, owner questions, safe next action, evidence gaps, approval boundary and detection-only warning. | Infrastructure template tests assert generated control-plane terms. |
| `T9-R-M18` | Add readiness and behavioral eval contracts for runtime packet safety | `project-readiness.json`, `behavioral-workflows.json`, `test_behavioral_workflow_evals.py`, `test_infrastructure_templates.py` | Readiness and behavioral evals encode `runtime_methodology_packet`, `finish_options`, `methodology_detection_not_completion`, approval boundary and no gate dump, scaffold or external action. | Behavioral/infrastructure tests pass and fixture eval includes stable checks when applicable. |
| `T9-R-M19` | Update agent task packet handoff compatibility | `agent-task-packet.md`, `test_infrastructure_templates.py` | Handoff packet can carry compact methodology packet, owner and consumer domains, finish options, safe next action, approval requirements and stop conditions without raw conversation history. | Template tests assert handoff fields and fresh-context contract remains intact. |
| `T9-R-M20` | Add backward compatibility tests for runner result schema v1 | `contracts.py`, `validate_codex_runtime_runner.py`, `test_codex_runtime_runner_contracts.py`, `test_codex_runtime_runner_cli.py` | Old valid result JSON without methodology packet remains valid; new additive route packet fields remain schema v1; malformed additive fields fail with stable errors. | Contract and CLI validator tests pass. |
| `T9-R-M21` | Define lifecycle-status to finish-options mapping | `routes.py`, `contracts.py`, runtime tests | `route_ready`, `needs_context`, `needs_approval`, `blocked`, `completed` and `failed` each map to bounded finish options and next action; `blocked` and `needs_context` do not offer write/stage actions. | State-route tests assert status-specific options. |
| `T9-R-M22` | Add runtime bridge checks for existing cross-domain fixtures | `run_fixture_eval.py`, codex-runner/cross-domain fixtures, `test_codex_runtime_runner_fixture_eval.py` | Runtime runner is evaluated against existing cross-domain fixtures such as `cross-domain-ai-rag-data-security`, `package-release-security-handoff`, `source-artifact-alias-mapping` or mirrored runner fixtures, proving synthesis survives runtime routing. | Fixture eval named checks pass for cross-domain runtime bridge. |
| `T9-R-M23` | Add compact first-response contract fields | `routes.py`, `cli.py`, behavioral evals, tests | First response contract exposes `owner_questions`, `safe_next_action`, `evidence_gaps`, `approval_boundary`, `finish_options`, and does not dump every methodology gate. | Route and behavioral tests assert compact first response. |
| `T9-R-M24` | Add structured high-risk action taxonomy for approval guards | `guards.py`, `contracts.py`, tests | Guards classify high-risk actions (`publish`, `deploy`, `tag`, `release_create`, `pr_or_push`, `package_registry_mutation`, `marketplace_submission`, `security_scan`, `production_data_access`, `db_migration`, `automation_activation`, `external_system_mutation`) instead of relying only on free-text matching. | Guard tests assert taxonomy decisions and false-positive safe text. |
| `T9-R-M25` | Add ownership and parallelism routing guard | `routes.py`, `guards.py`, `agent-task-packet.md`, tests | Multiple owner domains or overlapping artifact/file ownership route to owner review or `agent-team-designer` before builder/subagent work; parallel work requires fresh context handoff and explicit ownership. | Route/guard/template tests assert owner review and no unsafe parallel route. |

Task 21 verification policy:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_codex_runtime_runner_fixture_eval -v
python -m unittest tests.product_agent_os.test_codex_runtime_runner_cli -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

Expected: all commands exit `0`. Strict MkDocs is required only if navigation, Mermaid diagrams, Markdown extensions, MkDocs configuration or Product-Agent OS docs navigation change.

---

### Task 22: Final Track 9 Documentation Sync

**Files:**
- Modify: `docs/product-agent-os/index.md`
- Modify: `docs/product-agent-os/technical.md`
- Modify: `docs/product-agent-os/architecture.md`
- Modify: `docs/product-agent-os/scenarios.md`
- Modify: `docs/product-agent-os/behavioral-evals.md`
- Modify: `docs/product-agent-os/codex-compatibility.md`
- Modify: `docs/product-agent-os/methodology-intelligence.md`
- Modify: `plugins/product-agent-os/README.md`
- Modify: `README.md`
- Modify: `tests/product_agent_os/test_product_agent_os_docs.py`
- Modify: `REQUIREMENTS.md`
- Modify: `PLAN.md`
- Modify: `TEST.md`
- Modify: `EVALS.md`
- Modify: `RUNLOG.md`
- Modify: `docs/sources/registry.md`
- Modify: `docs/sources/product-agent-os-track-9-backlog.md`
- Modify: `AGENTS.md`
- Modify: `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md`

Task 22 consolidated implementation matrix (file/theme-based, preserving Track 1-9 traceability):

| ID | Task | Files | Acceptance | Covers |
| --- | --- | --- | --- | --- |
| `T22-U-M0` | Add consolidated docs regression tests | `tests/product_agent_os/test_product_agent_os_docs.py` | Tests assert final docs preserve Track 1-9 contracts, lifecycle skills, docs-maintainer, generated infrastructure, hardening, runtime runner, standards, scenarios, Track 9 packet behavior, stale-claim rejection and source registry closure. | Former docs-test and stale-claim rows: `F-M0`, `L-M0`, `L-M3`, `L-M7`, `G-M0`, `G-M5`, `H-M0`, `C-M0`, `C-M9`, `E-M0`, `E-M9`, `Q-M0`, `M0`, `M3`, `M5`, `M9`, `M10`, `M11`, `M22`. |
| `T22-U-M1` | Run RED docs tests before docs edits | `tests/product_agent_os/test_product_agent_os_docs.py` | Focused docs tests fail before user-facing docs, registry and README updates are applied; failures map to consolidated acceptance groups rather than 94 micro-rows. | Former Step 1/Step 2. |
| `T22-U-M2` | Rewrite Product-Agent OS product overview around user jobs | `docs/product-agent-os/index.md`, `README.md`, `plugins/product-agent-os/README.md` | Overview explains the full Product-Agent OS stack for real projects: inspect workspace, route safely, stage infrastructure, apply approved writes, run Codex-only routing, apply conditional methodology gates and require evidence before completion. Track history is provenance, not the primary user journey. | `L-M2`, `L-M6`, `G-M1`, `G-M4`, `C-M4`, `E-M1`, `E-M2`, `Q-M1`, `M6`, `M13`, `M19`. |
| `T22-U-M3` | Document Track 1-9 layer architecture without stale Track 1->8->9 shortcut | `docs/product-agent-os/architecture.md`, `docs/product-agent-os/technical.md`, `plugins/product-agent-os/README.md` | Architecture shows Track 1 foundation, Track 2 lifecycle, Track 3 staged generation, Track 4 approved merge, Track 5 Codex runtime, Track 6 standards, Track 7 hardening, Track 8 scenarios and Track 9 methodology intelligence as one ordered stack. | Resolves stale `F-M1`; covers `G-M1`, `E-M1`, `Q-M1`, `M1`, `M15`. |
| `T22-U-M4` | Document workspace audit, complexity vocabulary and route input separation | `docs/product-agent-os/technical.md`, `docs/product-agent-os/methodology-intelligence.md`, `docs/product-agent-os/scenarios.md` | Docs distinguish base workspace audit profile values from Track 9 methodology audit complexity values, and keep prompt intent, workspace signals and control-plane state separate; `--intent-hint` cannot override source, approval or write guards. | `F-M2`, `C-M7`, `M2`. |
| `T22-U-M5` | Document lifecycle skill governance and staged packet boundary | `docs/product-agent-os/architecture.md`, `docs/product-agent-os/technical.md`, `docs/product-agent-os/codex-compatibility.md`, `plugins/product-agent-os/README.md` | Docs cover lifecycle state -> skill/subagent route map, shared references, `allow_implicit_invocation: false`, source-sensitive skills, no hidden external writes, and that lifecycle skills produce staged packets/proposals rather than direct infrastructure writes. | `L-M1`, `L-M2`, `L-M3`, `L-M4`, `L-M5`, `L-M6`, `L-M7`, `C-M5`. |
| `T22-U-M6` | Document generated infrastructure and renderer contract | `docs/product-agent-os/technical.md`, `docs/product-agent-os/architecture.md`, `docs/product-agent-os/index.md`, `plugins/product-agent-os/README.md` | Docs cover template registry, dry-run, stage output outside target workspace, renderer JSON/status fields, managed sections, companion proposals, generated artifact categories, profile routing as depth and fixture eval renderer bridge. | `G-M1`, `G-M2`, `G-M3`, `G-M4`, `G-M6`, `G-M7`. |
| `T22-U-M7` | Document production hardening merge, rollback, source and automation controls | `docs/product-agent-os/technical.md`, `docs/product-agent-os/architecture.md`, `docs/product-agent-os/codex-compatibility.md`, `plugins/product-agent-os/README.md` | Docs cover stage manifest, approval record, read-only merge plan, approval-gated apply, merge safety invariants, rollback refusal on changed digest, hook activation gate, source-policy validator and automation promotion validator. | `H-M1`, `H-M2`, `H-M3`, `H-M4`, `H-M5`, `H-M6`, `H-M7`, `H-M8`. |
| `T22-U-M8` | Clarify Codex-only runtime and optional Agents SDK boundary | `docs/product-agent-os/architecture.md`, `docs/product-agent-os/technical.md`, `docs/product-agent-os/codex-compatibility.md`, `plugins/product-agent-os/README.md` | Docs state the runtime runner works only inside Codex App, CLI, IDE extension, skills and subagents context; it has contract mode, CLI/validator, `codex_runner_result`, lifecycle inference and guardrails. Optional Agents SDK runner remains design-only, inactive, no dependency install, no network default and no credential storage. | Resolves `H-M9` vs `C-M1`/`M18`; covers `H-M9`, `C-M1`, `C-M2`, `C-M3`, `C-M4`, `C-M6`, `C-M8`, `C-M9`, `M18`. |
| `T22-U-M9` | Document Methodology Intelligence final implemented contract | `docs/product-agent-os/methodology-intelligence.md`, `docs/product-agent-os/technical.md`, `docs/product-agent-os/architecture.md` | Page describes actual read-only audit, catalog/report/JSON, Delivery Map, two-axis classification, methodology synthesis, recommendation groups, runtime packet, owner questions, source artifact ledger, staged artifact boundary and safe next action. | `M1`, `M3`, `M12`, `M14`, `M15`. |
| `T22-U-M10` | Document scenario and finish-option application | `docs/product-agent-os/scenarios.md`, `docs/product-agent-os/index.md`, `README.md` | Scenarios map real project entry points such as bug, greenfield, PR review, API, AI/RAG, native/mobile, desktop, data, security, CI and release to route, methodology domains, finish options, safe next action and required evidence without forcing unrelated gates. | `M2`, `M5`, `M6`, `M16`. |
| `T22-U-M11` | Establish canonical safety and compatibility boundaries | `docs/product-agent-os/codex-compatibility.md`, `docs/product-agent-os/technical.md`, `docs/product-agent-os/development-standards.md` | One canonical section covers no standalone runtime activation, no API key/live model call, no silent MCP/hook/automation activation, no global config mutation, no unapproved external writes, no hosted docs/DB introspection without approval and no readiness claims from detection. Other pages link back to this boundary. | Consolidates safety rows: `F-M3`, `L-M2`, `L-M3`, `G-M5`, `H-M3`, `H-M5`, `H-M7`, `C-M1`, `C-M6`, `C-M7`, `C-M9`, `E-M8`, `Q-M11`, `M18`. |
| `T22-U-M12` | Establish canonical readiness status vocabulary for Track 6-9 | `docs/product-agent-os/development-standards.md`, `docs/product-agent-os/behavioral-evals.md`, `docs/product-agent-os/technical.md`, `docs/product-agent-os/index.md` | Docs define `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required` as a shared Track 6-9 contract; detection may produce `present_unverified` but never readiness or completion. | Resolves narrow `M7`; covers `E-M7`, `Q-M4`, `M7`. |
| `T22-U-M13` | Document engineering standards loop and generated control-plane fields | `docs/product-agent-os/development-standards.md`, `docs/product-agent-os/technical.md`, `plugins/product-agent-os/README.md` | Docs cover product hypothesis, architecture boundary, test/eval-first, bounded agentic implementation, docs-as-code, source context/source-backed claims, human review, measurement, learning loop and generated `AGENTS/REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG` fields. | `E-M2`, `E-M3`, `E-M4`, `E-M5`, `E-M6`. |
| `T22-U-M14` | Document no-forced-ceremony and false-positive protection | `docs/product-agent-os/development-standards.md`, `docs/product-agent-os/scenarios.md`, `docs/product-agent-os/behavioral-evals.md` | Docs/tests preserve that mechanical edits, inspection-only work, docs-light/internal work, backend/native work, simple CRUD and simple MVP can record `not_applicable` or accepted gaps instead of forcing DDD, FSD, docs portals or full standards ceremony. | `E-M9`, `Q-M3`, `Q-M7`, `Q-M10`, `M5`. |
| `T22-U-M15` | Document Track 7 artifact template catalog | `docs/product-agent-os/development-standards.md`, `docs/product-agent-os/technical.md`, `docs/product-agent-os/architecture.md` | One catalog documents ADR, architecture overview, domain modeling, metric spec, API contract review, component card and database dictionary templates with owners, evidence, accepted gaps, residual risks, no-secrets rules and verification expectations. | `Q-M6`, `Q-M7`, `Q-M8`, `Q-M9`, `Q-M10`, `Q-M11`. |
| `T22-U-M16` | Document methodology signal discovery and workspace gaps | `docs/product-agent-os/technical.md`, `docs/product-agent-os/development-standards.md`, `docs/product-agent-os/scenarios.md` | Docs list architecture docs, ADR, OpenAPI, AsyncAPI, Storybook, database docs, CODEOWNERS, CI, evals, metrics, domain model and optional `fsd_structure` signals; missing signals are audit risks/gaps, not automatic blockers for every small task. | `Q-M2`, `Q-M3`. |
| `T22-U-M17` | Document Red-Green-Refactor and evidence-before-completion model | `docs/product-agent-os/development-standards.md`, `docs/product-agent-os/behavioral-evals.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` | Docs require Red -> Green -> Refactor evidence or explicit gap for applicable bugfix/shared behavior; completion/fixed/ready/release claims need current command, eval, runtime, manual QA or explicit inspection-only gap evidence. | `Q-M5`, `M17`, parts of `F-M4`, `G-M7`, `H-M8`, `C-M8`. |
| `T22-U-M18` | Consolidate behavioral eval and fixture eval documentation | `docs/product-agent-os/behavioral-evals.md`, `plugins/product-agent-os/README.md` | Behavioral docs cover fixture eval limits, renderer checks, hardening statuses, runtime packet safety, transcript/session replay, deterministic privacy/no-secrets constraints and that synthetic regression evidence does not prove real project readiness. | `F-M4`, `G-M7`, `H-M8`, `C-M8`, `M4`, `M17`, `M23` verification scope. |
| `T22-U-M19` | Update technical commands, schemas and validators | `docs/product-agent-os/technical.md`, `plugins/product-agent-os/README.md` | Technical docs include real commands, JSON fields, schema v1 compatibility, validators, renderer output, runtime CLI, fixture eval checks, transcript eval and limitations without presenting implemented features as planned. | `F-M3`, `G-M2`, `C-M2`, `C-M3`, `M14`. |
| `T22-U-M20` | Update README quickstart and value proposition for the full stack | `README.md`, `plugins/product-agent-os/README.md` | README text explains Product-Agent OS value across Track 1-9, not only Track 8/9: package, lifecycle, staged generation, approved merge, runtime routing, engineering standards, hardening, scenarios and methodology intelligence. | Resolves narrow `M19`; covers README parts of many former rows. |
| `T22-U-M21` | Update source registry closure for Track 1-9 | `docs/sources/registry.md` | Registry includes Track 1-9 closure entries for inventory, design/backlog docs, implementation paths, docs pages, source policies, OpenAPI v3.2.0 freshness claim, eval/fixture/transcript evidence and current verification baseline. | Resolves narrow `M20`; covers `F-M5`, `G-M8`, `H-M6`, `H-M10`, `C-M10`, `E-M5`, `E-M10`, `Q-M9`, `Q-M12`, `M11`, `M20`. |
| `T22-U-M22` | Update root control-plane closure state | `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md` | Root control plane records Task 22 consolidated scope, Track 1-9 acceptance, verification commands, eval rubrics, residual risks, source inventory links and focused evidence; legacy Track 9 Task 23 baseline verification is absorbed into Task 22 so Track 10 can use Task 23 for the guided question/status dashboard capability. | `F-M5`, `G-M8`, `H-M10`, `C-M10`, `E-M10`, `Q-M12`, `M21`. |
| `T22-U-M23` | Run final docs verification and diff hygiene | docs tests, transcript eval, docs check, strict MkDocs, `git diff --check` | `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`, transcript eval, `python tools\check_docs.py`, strict MkDocs and `git diff --check` exit `0`; this absorbs the former verification expansion meta-task. | Resolves `M8`/`M23` duplication. |
| `T22-U-M24` | Keep commit/push explicit-only | Git only after user approval | Do not run `git add`, `git commit`, push or PR creation unless the user explicitly asks; if approved, commit only after all verification evidence is current. This row is a release guard, not a docs implementation task. | Clarifies `M24`. |

- [x] **Step 1: Add docs RED tests**

Extend `tests/product_agent_os/test_product_agent_os_docs.py` with consolidated grouped assertions for:

- Product-Agent OS full-stack overview and user jobs;
- Track 1-9 layer architecture;
- lifecycle routing, staged packets and docs-maintainer ownership;
- generated infrastructure and approved merge boundaries;
- Codex-only runtime and optional Agents SDK design-only boundary;
- engineering standards, Track 7 hardening and readiness statuses;
- scenario routing, methodology packet and finish options;
- behavioral evals, fixture eval limits and transcript eval;
- source registry closure and stale-claim rejection.

- [x] **Step 2: Run RED docs tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
```

Expected: fail until docs are updated.

- [x] **Step 3: Update user-facing docs**

Update Product-Agent OS docs by file/theme rather than by historical task row:

- `index.md` and READMEs: full Product-Agent OS value proposition for real projects, with Tracks 1-9 as implementation provenance rather than the primary user journey;
- `architecture.md`: ordered Track 1-9 stack, lifecycle -> staged generation -> approved merge -> Codex runtime -> standards -> scenarios -> methodology packet flow;
- `technical.md`: commands, JSON/schema fields, validators, renderer output, runtime CLI, readiness statuses and limitations;
- `methodology-intelligence.md`: final implemented audit/synthesis/runtime-packet contract, not planned wording;
- `scenarios.md`: user-job route map, route input separation, finish options and false-positive boundaries;
- `behavioral-evals.md`: fixture eval, transcript eval, runtime packet safety, detection-not-completion and evidence limits;
- `codex-compatibility.md`: canonical safety boundary for Codex App, CLI, IDE extension, skills, MCP, staged hooks, optional Agents SDK design-only path, approvals and no external activation;
- `development-standards.md`: Track 6/7 standards, artifact catalog, source-backed claims, Red-Green-Refactor, readiness status vocabulary and no-forced-ceremony rules.

- [x] **Step 4: Update root control-plane files**

Update:

- `REQUIREMENTS.md`: consolidated Task 22 goal, Track 1-9 scope and acceptance criteria.
- `PLAN.md`: consolidated Task 22 queue and current state.
- `TEST.md`: Task 22 verification commands, docs tests, transcript eval, docs check, strict MkDocs and diff hygiene.
- `EVALS.md`: docs/eval rubrics, readiness/evidence quality and residual risks.
- `RUNLOG.md`: latest Task 22 evidence, source inventory links and open risks.

- [x] **Step 5: Update source registry**

Add Track 1-9 implementation closure entries to `docs/sources/registry.md` referencing:

- pre-Track-8 implementation inventory;
- Track 9 methodology design spec and backlog;
- Product-Agent OS docs pages and READMEs;
- catalog/audit/discovery/runtime/report implementation paths;
- Track 6/7 methodology research, gap matrix and artifact templates;
- fixture/transcript eval paths and current verification baseline.

- [x] **Step 6: Run docs verification**

Run:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python tools\check_docs.py
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict
git diff --check
```

Expected: all commands exit `0`.

- [ ] **Step 7: Commit docs sync, explicit-only**

Do not run this step unless the user explicitly asks for a commit. If approved, run:


```powershell
git add README.md REQUIREMENTS.md PLAN.md TEST.md EVALS.md RUNLOG.md docs plugins\product-agent-os\README.md tests\product_agent_os\test_product_agent_os_docs.py mkdocs.yml tools\check_docs.py
git commit -m "docs: sync track 9 methodology intelligence"
```

Expected: commit succeeds.

---

### Legacy Track 9 Final Verification Baseline (absorbed into Task 22)

Track 10 uses `Task 23` for Guided Question Protocol And Project Status Dashboard. The former Track 9 final verification baseline below is retained as historical checklist material only; its required evidence is now part of `T22-U-M23`.

**Files:**
- Read-only verification across repository.
- Modify only `RUNLOG.md`, `TEST.md`, `EVALS.md` if evidence summaries need current command outputs.

- [x] **Step 1: Run full test suite**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: exit `0`; record total test count in `TEST.md` and `RUNLOG.md`.

- [x] **Step 2: Run fixture eval**

Run:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: exit `0`; record fixture count, failures and key Track 9 checks.

- [x] **Step 3: Run transcript eval**

Run:

```powershell
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
```

Expected: exit `0`; record session count and failures.

- [x] **Step 4: Run compatibility check**

Run:

```powershell
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
```

Expected: JSON output includes `"status": "compatible"`.

- [x] **Step 5: Run docs and MkDocs checks**

Run:

```powershell
python tools\check_docs.py
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict
```

Expected: both commands exit `0`.

- [x] **Step 6: Update final evidence if counts changed**

If test, fixture or MkDocs evidence counts changed, update:

- `TEST.md`;
- `EVALS.md`;
- `RUNLOG.md`;
- `docs/sources/product-agent-os-track-9-backlog.md`.

Do not write "tests pass" without the current outputs from Steps 1-5.

- [ ] **Step 7: Commit final baseline**

Run:

```powershell
git add TEST.md EVALS.md RUNLOG.md docs\sources\product-agent-os-track-9-backlog.md
git commit -m "test: refresh track 9 verification baseline"
```

Expected: commit succeeds if evidence files changed. If no evidence files changed, record in final response that no final baseline commit was needed.

---

## Self-Review Checklist For This Plan

Spec coverage:

- Goal, core product principle, two-step onboarding, classification model, Delivery Map, report/JSON outputs, recommendations, all 12 domains, adaptive deep-dive loop, cross-domain synthesis, safety, verification and definitions of done are mapped to tasks.

No unsupported broad implementation:

- The plan does not ask for direct target workspace writes.
- The plan keeps staged artifacts approval-bound.
- The plan keeps methodology conditional.
- The plan requires false-positive coverage.

Residual risks:

- Domain catalog entries will be large; review each domain diff carefully.
- Domain tasks can reveal more sub-slices than listed here; add them to `docs/sources/product-agent-os-track-9-backlog.md` before implementing.
- Deterministic tests prove contract shape; semantic methodology quality still needs human review and future eval refinement.

## Execution Handoff

Recommended execution: **Subagent-Driven** after creating an isolated worktree. Each task has a clear file boundary and can be reviewed independently.

Execution options:

1. **Subagent-Driven (recommended)** - dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** - execute tasks in this session using `superpowers:executing-plans`, with checkpoints after each task.
