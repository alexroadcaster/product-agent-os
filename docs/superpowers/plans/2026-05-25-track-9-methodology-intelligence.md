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

| ID | Task | Primary files | Acceptance criteria | Verification |
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

| ID | Task | Primary files | Acceptance criteria | Verification |
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

| ID | Task | Primary files | Acceptance criteria | Verification |
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
- semantic evidence sufficiency review is normalized as a shared owner-review gate for high-risk, production, release, security-sensitive, AI behavior and public-contract slices; it can be satisfied by explicit owner review evidence or an accepted gap with owner, reason, review date, downstream risk and follow-up condition;
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
- add semantic evidence sufficiency owner-review rules for high-risk, production, release, security-sensitive, AI behavior and public-contract slices;
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
- record semantic evidence sufficiency review ownership, accepted-gap shape and consumer domains;
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
