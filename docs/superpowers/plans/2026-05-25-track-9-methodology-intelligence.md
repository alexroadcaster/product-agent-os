# Track 9 Methodology Intelligence Implementation Plan

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

Forbidden behavior:

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
- Modify: `plugins/product-agent-os/assets/templates/artifact-templates/metric-spec.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/product-brief.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/value-proposition.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/opportunity-tree.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/experiment-plan.md`
- Modify: lifecycle skills listed in File Structure
- Test: `tests/product_agent_os/test_methodology_catalog.py`
- Test: `tests/product_agent_os/test_methodology_audit.py`
- Test: `tests/product_agent_os/test_fixture_eval_runner.py`

- [ ] **Step 1: Add RED catalog test for business/product gates**

Add a test asserting `business_product` includes these gates:

```python
[
    "product_hypothesis_present",
    "target_user_segment_present",
    "opportunity_not_solution_present",
    "success_metric_present",
    "metric_hardening_when_product_behavior_changes",
    "privacy_classification_for_metrics_present",
    "ai_product_eval_when_ai_behavior_changes",
    "post_release_measurement_plan_present",
    "workflow_promotion_value_evidence_present",
]
```

Also assert artifacts include:

```python
[
    "product-brief.md",
    "value-proposition.md",
    "opportunity-tree.md",
    "experiment-plan.md",
    "metric-spec.md",
    "acceptance-scenarios.md",
]
```

- [ ] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog.MethodologyCatalogContractTest -v
```

Expected: fail because business/product gates and artifacts are missing.

- [ ] **Step 3: Add business/product catalog data**

Modify `methodology-catalog.json` domain `business_product` with:

- applies_when: behavior-changing feature, product-labeled request, MVP, release, AI behavior change, metric claim;
- not_applicable_when: mechanical formatting, typo-only docs edit, dependency pin without behavior impact;
- maturity_impact: `baseline`, `team`, `production`;
- complexity_impact: `standard`, `high_risk` when AI/product promise/measurement claims exist;
- track8_scenarios: `greenfield_idea`, `release_packaging`, `ai_eval_regression`, `standard_feature`;
- gates and artifacts from Step 1;
- overlaps: quality eval evidence, delivery measurement, requirements acceptance scenarios.

- [ ] **Step 4: Add artifact templates**

Create:

- `product-brief.md`: user/segment, problem/opportunity, outcome, non-goals, assumptions, evidence gaps, owner.
- `value-proposition.md`: jobs, pains, gains, pain relievers, gain creators, evidence source, owner.
- `opportunity-tree.md`: desired outcome, opportunities, candidate solutions, riskiest assumptions, tests, decision.
- `experiment-plan.md`: smallest build, metric, learning threshold, pivot/persevere rule, owner, review date.

Every template must include `Source status:`, owner, evidence, accepted gap and residual risk fields.

- [ ] **Step 5: Register templates**

Modify `plugins/product-agent-os/scripts/product_agent_os/templates.py` so the renderer can stage the new artifact templates under `.codex/artifact-templates/`.

- [ ] **Step 6: Add audit recommendations**

Modify `methodology_audit.py`:

- product/MVP/value/metric intent triggers `business_product`;
- missing product hypothesis creates `P2_recommended`;
- metric claim without guardrails creates `P1_high_risk`;
- AI behavior change creates `P1_high_risk` for `ai_product_eval_when_ai_behavior_changes`.

- [ ] **Step 7: Update lifecycle skills**

Add concise wording:

- `requirements-author`: product hypothesis before requirements for behavior-changing work.
- `test-eval-designer`: product behavior claims need metric/eval evidence.
- `risk-reviewer`: proxy metric and AI product value claims need counter-metric or accepted gap.
- `learning-loop-maintainer`: post-release measurement feeds workflow promotion.

- [ ] **Step 8: Run focused verification**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_infrastructure_renderer -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: all commands exit `0`; renderer file count increases by the number of registered templates.

- [ ] **Step 9: Update Track 9 backlog**

Modify `docs/sources/product-agent-os-track-9-backlog.md`:

- mark `T9-D1` as `done`;
- record gates added;
- record templates added;
- record verification evidence;
- record overlaps for synthesis.

- [ ] **Step 10: Commit T9-D1**

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
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/requirements-traceability-matrix.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/business-rules.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/requirement-change-impact.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/domain-review-record.md`
- Tests: methodology catalog, audit, renderer, fixture eval

- [ ] **Step 1: Add RED test for requirements/domain gates**

Assert `requirements_domain` gates include:

```python
[
    "requirements_scope_present",
    "requirements_owner_present",
    "requirement_ids_present",
    "acceptance_scenarios_when_behavior_changes",
    "requirements_traceability_present",
    "business_rules_present",
    "non_goals_constraints_present",
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

- [ ] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing requirements/domain gates.

- [ ] **Step 3: Add catalog data and false-positive rules**

Rules:

- applies for behavior changes, domain terms, workflows, API/UI/data changes, AI behavior changes;
- not applicable for docs typo, formatting-only, pure dependency metadata without behavior impact;
- do not force DDD for simple CRUD/MVP when accepted gap exists;
- overloaded domain terms become owner questions, not verified evidence.

- [ ] **Step 4: Add and register templates**

Create templates:

- `requirements-traceability-matrix.md`;
- `business-rules.md`;
- `requirement-change-impact.md`;
- `domain-review-record.md`.

Each template must include source, owner, linked requirements, evidence owner, accepted gap and residual risk.

- [ ] **Step 5: Extend audit recommendations**

Add recommendations:

- behavior intent with missing acceptance scenarios -> `P0_blocker`;
- domain/API/UI/data crossing without traceability -> `P1_high_risk`;
- complex domain without domain model or accepted gap -> `P1_high_risk`;
- changed requirement after planning -> `P1_high_risk` for impact review.

- [ ] **Step 6: Update lifecycle skills**

Update:

- `requirements-author`: requirement quality and domain artifacts.
- `implementation-planner`: block implementation when behavior scenarios or traceability are missing.
- `agent-team-designer`: use bounded contexts for ownership split.
- `test-eval-designer`: map scenarios to tests/evals.
- `risk-reviewer`: check domain claims and accepted gaps.

- [ ] **Step 7: Add false-positive fixture**

Create or extend a fixture for simple CRUD that has `src/domain/` but no complex domain indicators. Assert DDD remains `not_applicable` or accepted gap, not `applicable_missing`.

- [ ] **Step 8: Run verification**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: all commands exit `0`.

- [ ] **Step 9: Commit T9-D2**

Run:

```powershell
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md
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

- [ ] **Step 1: Add RED test for architecture gates**

Assert `solution_architecture` gates include:

```python
[
    "solution_architecture_scope_present",
    "architecture_context_view_present",
    "architecture_container_boundary_present",
    "architecture_boundary_per_slice",
    "boundary_responsibility_owner_present",
    "dependency_rules_present",
    "public_contract_boundary_trace_present",
    "data_ownership_boundary_present",
    "runtime_deployment_topology_present",
    "quality_attribute_scenarios_present",
    "tradeoff_record_for_high_impact_decision",
    "trust_boundary_security_review_present",
    "domain_to_architecture_trace_present",
    "diagram_render_check_present",
    "architecture_fitness_function_present",
    "architecture_docs_as_code_present",
    "architecture_owner_review_present",
    "accepted_gap_recorded",
]
```

- [ ] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing architecture gates.

- [ ] **Step 3: Add architecture catalog data**

Rules:

- applies for complex/team/production/API/data/AI/runtime/ownership changes;
- not applicable for small text-only docs edits and mechanical formatting;
- high-impact decisions trigger ADR or architecture review;
- diagram presence alone is `present_unverified`.

- [ ] **Step 4: Add and register templates**

Create:

- `architecture-review-record.md`;
- `architecture-fitness-functions.md`;
- `trust-boundary-map.md`;
- `architecture-docs-tooling-decision.md`.

Extend `architecture-overview.md` and `adr.md` with owner, boundary, quality attribute, verification and rollback fields.

- [ ] **Step 5: Add audit recommendations**

Recommendations:

- multi-surface project without architecture overview -> `P1_high_risk`;
- public contract or data boundary without owner -> `P1_high_risk`;
- architecture docs without render check -> `P2_recommended`;
- repeated boundary drift signals -> `P2_recommended` for fitness functions.

- [ ] **Step 6: Update skills and evals**

Update planner and risk reviewer to require architecture boundary and owner evidence for high-impact slices. Add fixture eval check `solution_architecture_contract_present`.

- [ ] **Step 7: Run verification and commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md
git commit -m "feat: integrate solution architecture methodology"
```

Expected: tests and fixture eval pass before commit.

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

- [ ] **Step 1: Add RED test for quality gates**

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

- [ ] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing quality gates.

- [ ] **Step 3: Add quality catalog and recommendations**

Rules:

- quality domain applies to every non-trivial project;
- missing test command is `P0_blocker`;
- AI changes without eval baseline are `P1_high_risk`;
- UI changes without visual/a11y evidence are `P1_high_risk` for public UI and `P2_recommended` for internal UI;
- flaky tests produce owner question and `P2_recommended` policy recommendation.

- [ ] **Step 4: Add templates and skill updates**

Create and register:

- `test-eval-matrix.md`;
- `quality-strategy.md`;
- `ci-evidence-record.md`;
- `flaky-test-policy.md`;
- `manual-qa-evidence.md`.

Update `test-eval-designer`, `risk-reviewer` and `implementation-planner` with current evidence rules.

- [ ] **Step 5: Add eval runner checks**

Update fixture eval with `quality_testing_evals_contract_present` and assert current evidence before completion remains active.

- [ ] **Step 6: Run verification and commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md
git commit -m "feat: integrate quality testing evals methodology"
```

Expected: tests, fixture eval and transcript eval pass before commit.

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

- [ ] **Step 1: Add RED test for Codex workflow gates**

Assert `codex_agentic_workflow` gates include:

```python
[
    "control_plane_present",
    "source_of_truth_present",
    "model_reasoning_policy_present",
    "fresh_context_handoff_present",
    "ownership_split_present",
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

- [ ] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing Codex workflow gates.

- [ ] **Step 3: Add catalog and templates**

Create and register:

- `model-reasoning-policy.md`;
- `mcp-permission-review.md`;
- `hook-governance.md`;
- `skill-promotion-record.md`;
- `agent-eval-workflow.md`.

Extend `AGENTS.md` and `.codex/config.toml` templates with model/reasoning policy and approval boundaries.

- [ ] **Step 4: Add audit recommendations**

Recommendations:

- missing control-plane -> `P0_blocker`;
- MCP config or side-effecting tool without permission review -> `P1_high_risk`;
- hook activation without approval -> `P1_high_risk`;
- subagent/parallel intent without ownership split -> `P1_high_risk`;
- repeated workflow without evidence -> `P2_recommended` skill promotion record.

- [ ] **Step 5: Update lifecycle skills**

All lifecycle skills must mention Track 9 methodology recommendations as context, but no skill should activate hooks, MCP, automation or external writes without approval.

- [ ] **Step 6: Run verification and commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_codex_compatibility -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md
git commit -m "feat: integrate codex agentic workflow methodology"
```

Expected: tests, fixture eval and compatibility pass before commit.

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

- [ ] **Step 1: Add RED test for frontend gates**

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

- [ ] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing frontend gates.

- [ ] **Step 3: Add catalog and false-positive rules**

Rules:

- frontend applies when UI framework, components, routes, Storybook, browser assets or UI intent exist;
- frontend is `not_applicable` for backend-only, data-only, CLI-only and docs-only work;
- Storybook is recommended only when components need reusable state docs or design-system review;
- public UI defaults to accessibility and visual evidence recommendations.

- [ ] **Step 4: Add templates and audit rules**

Create and register:

- `frontend-flow-spec.md`;
- `frontend-state-matrix.md`;
- `frontend-visual-qa.md`;
- `frontend-accessibility-review.md`;
- `frontend-performance-budget.md`.

Update audit rules for React/Next.js, Vue/Nuxt, Svelte/SvelteKit, Angular, Storybook and Vite signals.

- [ ] **Step 5: Add false-positive fixture checks**

Ensure backend, native, docs-only and simple CRUD fixtures do not trigger frontend gates. Keep existing FSD false-positive tests passing.

- [ ] **Step 6: Run verification and commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md
git commit -m "feat: integrate frontend methodology"
```

Expected: tests and fixture eval pass before commit.

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

- [ ] **Step 1: Add RED test for backend gates**

Assert `backend` gates include:

```python
[
    "backend_service_boundary_present",
    "backend_runtime_behavior_present",
    "backend_dependency_failure_matrix_present",
    "backend_observability_contract_present",
    "backend_slo_or_gap_present",
    "backend_health_probe_contract_present",
    "backend_data_consistency_strategy_present",
    "backend_config_secrets_boundary_present",
    "backend_security_reviewed",
    "backend_rollback_plan_present",
]
```

- [ ] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing backend gates.

- [ ] **Step 3: Add backend catalog and recommendations**

Rules:

- default recommendation favors modular monolith boundaries before microservices;
- microservices require independent scaling/team/deploy evidence;
- retries, queues, jobs and distributed workflows require idempotency, timeout, replay and recovery evidence;
- auth, money, sensitive data and irreversible side effects route through risk review.

- [ ] **Step 4: Add templates and discovery signals**

Create all backend templates listed in Files. Detect:

- `src/server`, `app/main.py`, `fastapi`, `express`, `django`, `flask`, `spring`, `.NET`, `go.mod`;
- `Dockerfile`, `Procfile`, `docker-compose.yml`, `k8s/*.yaml`;
- queue/job signals in `celery`, `bull`, `rq`, `sidekiq`, `cron`, `worker`.

- [ ] **Step 5: Add false-positive checks**

Docs-only and frontend-only fixtures must not trigger backend service boundary gates.

- [ ] **Step 6: Run verification and commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md
git commit -m "feat: integrate backend methodology"
```

Expected: tests and fixture eval pass before commit.

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

- [ ] **Step 6: Run verification and commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md
git commit -m "feat: integrate api integrations methodology"
```

Expected: tests and fixture eval pass before commit.

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

- [ ] **Step 1: Add RED test for database gates**

Assert `database_data` gates include:

```python
[
    "database_schema_source_present",
    "database_migration_plan_present",
    "database_expand_contract_reviewed",
    "database_transaction_boundary_present",
    "database_rollback_feasibility_present",
    "database_backup_restore_evidence_present",
    "database_data_classification_present",
    "database_data_quality_contract_present",
    "database_lineage_present",
    "database_performance_review_present",
    "database_synthetic_fixture_policy_present",
    "database_production_access_approval_present",
]
```

- [ ] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing database gates.

- [ ] **Step 3: Add database catalog and safety rules**

Rules:

- production data must never appear in prompts, docs, templates or fixtures;
- migrations are staged planning artifacts until approved;
- destructive migration detection creates questions and high-risk recommendation;
- DB introspection and production access are approval-required.

- [ ] **Step 4: Add templates and detection**

Create all database templates listed in Files. Detect Alembic, Prisma, Rails/Django migrations, Liquibase, Flyway, dbt, DBML, SQL DDL, SchemaSpy, Great Expectations and OpenLineage signals.

- [ ] **Step 5: Add false-positive and approval-bound fixtures**

Extend data migration fixtures:

- schema file alone is `present_unverified`;
- production DB terms trigger `approval_required`;
- RAG ingestion data triggers overlap with `llm_ai_rag`.

- [ ] **Step 6: Run verification and commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md
git commit -m "feat: integrate database data methodology"
```

Expected: tests and fixture eval pass before commit.

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

- [ ] **Step 6: Run verification and commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_transcript_session_evals tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md
git commit -m "feat: integrate ai rag methodology"
```

Expected: tests, fixture eval and transcript eval pass before commit.

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

- [ ] **Step 1: Add RED test for security gates**

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

- [ ] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing security gates.

- [ ] **Step 3: Add security catalog and rules**

Rules:

- auth, PII, payment, secrets, external writes, production data, AI agents and compliance terms trigger security/privacy domain;
- source references are methodology evidence, not legal advice;
- compliance overlay records applicability and owner, not certification;
- secrets in generated outputs are blocked.

- [ ] **Step 4: Add templates and detection**

Create all security templates listed in Files. Detect auth, OAuth, JWT, payment, billing, secrets, PII, rate limit, audit log, SBOM, package lock and CI permission signals.

- [ ] **Step 5: Add false-positive fixtures**

Add or extend fixtures:

- security docs mention without code path creates `present_unverified`;
- payment/billing signals create `P1_high_risk`;
- docs-only repository with security article does not become regulated automatically.

- [ ] **Step 6: Run verification and commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_source_policy tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md
git commit -m "feat: integrate security privacy compliance methodology"
```

Expected: tests and fixture eval pass before commit.

---

### Task 19: T9-D12 Delivery, Release & Operations Integration

**Files:**
- Source: `docs/methodologies/delivery-release-operations.md`
- Modify: catalog, audit, `release-readiness.md`, `release-packet.md`
- Create: `release-scope.md`
- Create: `version-impact-record.md`
- Create: `artifact-manifest.md`
- Create: `rollout-strategy.md`
- Create: `rollback-recovery-plan.md`
- Create: `ci-cd-governance.md`
- Create: `operations-runbook.md`
- Create: `incident-response-path.md`
- Create: `post-release-measurement.md`

- [ ] **Step 1: Add RED test for delivery gates**

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
]
```

- [ ] **Step 2: Run RED test**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog -v
```

Expected: fail on missing delivery gates.

- [ ] **Step 3: Add delivery catalog and release rules**

Rules:

- release intent, package manifests, CI, deployment manifests and version changes trigger delivery domain;
- publish, tag, release creation, artifact upload and package registry mutation require explicit approval;
- docs-only release uses reduced evidence;
- production release requires rollback/recovery, owner review and release evidence.

- [ ] **Step 4: Add templates and detection**

Create all delivery templates listed in Files. Detect package/version files, changelog, CI, deployment manifests, release notes, package registry config and Docker/Kubernetes signals.

- [ ] **Step 5: Add fixture eval checks**

Existing `package-release` fixture must expose:

- `delivery_release_operations_contract_present`;
- release approval boundary;
- artifact manifest recommendation;
- release evidence before completion.

- [ ] **Step 6: Run verification and commit**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md
git commit -m "feat: integrate delivery release operations methodology"
```

Expected: tests and fixture eval pass before commit.

---

### Task 20: Cross-Domain Synthesis

**Files:**
- Modify: `plugins/product-agent-os/assets/methodology/methodology-catalog.json`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`
- Modify: `plugins/product-agent-os/scripts/run_fixture_eval.py`
- Modify: `docs/sources/product-agent-os-track-9-backlog.md`
- Modify: `docs/product-agent-os/methodology-intelligence.md`
- Create: `tests/product_agent_os/test_methodology_synthesis.py`

- [ ] **Step 1: Add RED synthesis tests**

Create `tests/product_agent_os/test_methodology_synthesis.py` with tests that assert:

- no duplicate gate ids across domains unless listed in `overlaps`;
- no duplicate artifact ids with conflicting owners;
- `security_risk_review_present` maps to security domain as owner and backend/API/data/AI/delivery as consumers;
- `evidence_before_completion` concepts are normalized under quality/Codex/delivery rules;
- mutually exclusive recommendations cannot both be `P0_blocker` for the same workspace;
- simple docs-only fixture receives no frontend/backend/API/database/security/release hard blockers.

- [ ] **Step 2: Run RED synthesis tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_synthesis -v
```

Expected: fail until synthesis rules exist.

- [ ] **Step 3: Normalize overlaps**

Modify catalog:

- add owner domain for shared gates;
- add consumer domains for shared gates;
- add conflict rules for mutually exclusive frameworks;
- merge duplicate artifacts where one template can serve multiple domains;
- keep domain-specific templates only when the evidence model differs.

- [ ] **Step 4: Add priority resolver**

Modify `methodology_audit.py` to sort and resolve recommendations:

1. `P0_blocker`;
2. `P1_high_risk`;
3. `P2_recommended`;
4. `P3_optional_maturity`;
5. `not_applicable`.

When two recommendations target the same artifact, keep the highest priority and merge evidence requirements without duplicating text.

- [ ] **Step 5: Add cross-domain fixtures**

Add or extend fixtures for:

- docs-only no heavy methodology;
- internal CLI with no frontend/API/release hard blockers;
- small app with PII but low code complexity;
- complex monorepo without production users;
- AI/RAG project with data and security overlap.

- [ ] **Step 6: Run synthesis verification**

Run:

```powershell
python -m unittest tests.product_agent_os.test_methodology_synthesis tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: all commands exit `0`.

- [ ] **Step 7: Update Track 9 backlog**

Update `docs/sources/product-agent-os-track-9-backlog.md`:

- record deduplicated gates;
- record merged artifacts;
- record known accepted overlaps;
- record final false-positive coverage.

- [ ] **Step 8: Commit synthesis**

Run:

```powershell
git add plugins\product-agent-os tests\product_agent_os docs\sources\product-agent-os-track-9-backlog.md docs\product-agent-os\methodology-intelligence.md
git commit -m "feat: synthesize track 9 methodology domains"
```

Expected: commit succeeds.

---

### Task 21: Update Runtime Runner And Finish Options

**Files:**
- Modify: `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`
- Modify: `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`
- Modify: `plugins/product-agent-os/scripts/codex_runtime_runner/guards.py`
- Modify: `tests/product_agent_os/test_codex_runtime_runner_contracts.py`
- Modify: `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`
- Modify: `tests/product_agent_os/test_codex_runtime_runner_fixture_eval.py`

- [ ] **Step 1: Add RED runtime route tests**

Add tests that assert runtime route packets can include:

- `methodology_intelligence`;
- `methodology_recommendations`;
- `questions_for_owner`;
- `safe_next_action`;
- `write_policy=read_only` before approval;
- `needs_approval` before staged artifact generation.

- [ ] **Step 2: Run RED runtime tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_state_routes -v
```

Expected: fail because runtime contracts do not expose Track 9 methodology fields.

- [ ] **Step 3: Extend runtime contracts**

Modify contracts so `route_ready` can carry methodology intelligence while preserving current statuses:

- `route_ready`;
- `needs_context`;
- `needs_approval`;
- `blocked`;
- `completed`;
- `failed`.

Do not introduce model calls or standalone runtime behavior.

- [ ] **Step 4: Extend guards**

Guards must block:

- staged artifact generation without approval;
- completion claims based on methodology detection;
- automation promotion without maturity evidence;
- external writes from methodology recommendations.

- [ ] **Step 5: Run runtime verification**

Run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_codex_runtime_runner_fixture_eval -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: all commands exit `0`.

- [ ] **Step 6: Commit runtime integration**

Run:

```powershell
git add plugins\product-agent-os\scripts\codex_runtime_runner tests\product_agent_os
git commit -m "feat: expose methodology intelligence in runtime route"
```

Expected: commit succeeds.

---

### Task 22: Final Track 9 Documentation Sync

**Files:**
- Modify: `docs/product-agent-os/index.md`
- Modify: `docs/product-agent-os/technical.md`
- Modify: `docs/product-agent-os/architecture.md`
- Modify: `docs/product-agent-os/scenarios.md`
- Modify: `docs/product-agent-os/behavioral-evals.md`
- Modify: `docs/product-agent-os/codex-compatibility.md`
- Modify: `plugins/product-agent-os/README.md`
- Modify: `README.md`
- Modify: `REQUIREMENTS.md`
- Modify: `PLAN.md`
- Modify: `TEST.md`
- Modify: `EVALS.md`
- Modify: `RUNLOG.md`
- Modify: `docs/sources/registry.md`

- [ ] **Step 1: Add docs RED tests**

Extend `tests/product_agent_os/test_product_agent_os_docs.py` to assert Track 9 is documented in:

- Product-Agent OS index;
- technical page;
- architecture page;
- methodology intelligence page;
- behavioral evals page;
- plugin README.

- [ ] **Step 2: Run RED docs tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
```

Expected: fail until docs are updated.

- [ ] **Step 3: Update user-facing docs**

Update Product-Agent OS docs so they explain:

- read-only first audit;
- two-axis classification;
- Delivery Map;
- human report and JSON output;
- recommendation priorities;
- staged artifacts after approval;
- 12 methodology domains;
- cross-domain synthesis;
- false-positive protection.

- [ ] **Step 4: Update root control-plane files**

Update:

- `REQUIREMENTS.md`: Track 9 goal, scope and acceptance criteria.
- `PLAN.md`: Track 9 queue and current state.
- `TEST.md`: Track 9 verification commands.
- `EVALS.md`: Track 9 eval rubrics and residual risks.
- `RUNLOG.md`: latest Track 9 completion evidence.

- [ ] **Step 5: Update source registry**

Add Track 9 implementation closure entries to `docs/sources/registry.md` referencing:

- methodology design spec;
- Track 9 backlog;
- methodology intelligence docs;
- catalog/audit implementation paths;
- verification baseline.

- [ ] **Step 6: Run docs verification**

Run:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict
```

Expected: all commands exit `0`.

- [ ] **Step 7: Commit docs sync**

Run:

```powershell
git add README.md REQUIREMENTS.md PLAN.md TEST.md EVALS.md RUNLOG.md docs plugins\product-agent-os\README.md tests\product_agent_os\test_product_agent_os_docs.py mkdocs.yml tools\check_docs.py
git commit -m "docs: sync track 9 methodology intelligence"
```

Expected: commit succeeds.

---

### Task 23: Final Verification Baseline

**Files:**
- Read-only verification across repository.
- Modify only `RUNLOG.md`, `TEST.md`, `EVALS.md` if evidence summaries need current command outputs.

- [ ] **Step 1: Run full test suite**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: exit `0`; record total test count in `TEST.md` and `RUNLOG.md`.

- [ ] **Step 2: Run fixture eval**

Run:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: exit `0`; record fixture count, failures and key Track 9 checks.

- [ ] **Step 3: Run transcript eval**

Run:

```powershell
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
```

Expected: exit `0`; record session count and failures.

- [ ] **Step 4: Run compatibility check**

Run:

```powershell
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
```

Expected: JSON output includes `"status": "compatible"`.

- [ ] **Step 5: Run docs and MkDocs checks**

Run:

```powershell
python tools\check_docs.py
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict
```

Expected: both commands exit `0`.

- [ ] **Step 6: Update final evidence if counts changed**

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
