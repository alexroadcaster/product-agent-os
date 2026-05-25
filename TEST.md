# TEST.md

<!-- product-agent-os:start test-plan -->
Project: Codex Docs / Product-Agent OS
Generated at: 2026-05-25

## Current Baseline

- T9-D4 RED check: focused catalog/audit/discovery/template/lifecycle/behavioral/fixture checks failed as expected before implementation on missing `quality_testing_evals` gates, audit recommendations, quality discovery signals, five quality templates, lifecycle skill routing, behavioral eval coverage and fixture eval check.
- Combined focused T9-D4 suite: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner -v` ran 168 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; renderer file count is 97 and `quality_testing_evals_contract_present` is true.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 370 tests with `OK`.
- Transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Docs check: `python tools\check_docs.py` passed.
- Diff hygiene: `git diff --check` exited `0`.

## Required Checks After Docs Changes

```powershell
python tools\check_docs.py
```

Run strict MkDocs when navigation, Mermaid diagrams, Markdown extensions or MkDocs config change:

```powershell
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict
```

## Required Checks After Plugin Changes

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
```

## Track 9 Section Verification Protocol

Before implementing a Track 9 section:

- Inspect the relevant task block in `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`.
- Inspect the matching source file under `docs/methodologies/`.
- If the deep audit changes scope, update the plan or Track 9 backlog first and run `python tools\check_docs.py`.

For each Track 9 implementation section:

- Add focused RED tests for new catalog, discovery, readiness gate, artifact template, lifecycle skill or eval behavior before implementation.
- Add false-positive tests when a methodology can be over-applied.
- Run focused tests for the touched section before the full suite.
- Run full plugin verification after plugin scripts, templates, fixtures or tests change:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
```

## Completed Focused Checks For T8-C

- Added RED then GREEN tests for `docs-tooling-decision.md` and `T8-A11` docs-as-code applicability statuses.
- Confirmed `docs_as_code_impact` supports `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required`.
- Added docs tooling selector tests for stack-appropriate recommendations, including MkDocs, Storybook, OpenAPI, DBML/dbdocs, Mermaid, PlantUML and Structurizr DSL.
- Confirmed docs tooling is not forced on backend, native, simple MVP, docs-light or internal-only work when not applicable.
- Confirmed hosted docs and DB introspection stay `approval_required`, not activated.
- Added readiness/eval/fixture coverage through `project-readiness.json` and `docs_tooling_selector_contract_present`.

## Completed Focused Checks For T8-F

- Added RED then GREEN tests for conditional readiness statuses across remaining methodology/tooling gates.
- Confirmed `project-readiness.json` defines `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required`.
- Confirmed every conditional readiness gate records `applies_when`, `pass_condition`, `accepted_gap`, `required_evidence`, `owner` and `residual_risk`.
- Confirmed fixture eval exposes `conditional_readiness_gates_contract_present`.
- Confirmed lifecycle guidance says detection alone only supports `present_unverified`, not readiness.

## Completed Focused Checks For T8-H

- Added RED then GREEN docs contract tests for `scenarios.md`, `behavioral-evals.md` and `codex-compatibility.md`.
- Confirmed each page has `Source status:`, Inputs, Outputs, Verification and Risks sections.
- Confirmed MkDocs nav and `tools/check_docs.py` include the new pages.
- Confirmed source registry and Track 8 backlog record T8-H closure.

## Completed Focused Checks For T8-GY

- Added RED then GREEN tests for `evaluate_transcript_sessions`, synthetic session fixture replay, privacy/no-secrets rejection and CLI exit codes.
- Confirmed packaged transcript sessions map to `behavioral_case` entries in `behavioral-workflows.json`.
- Confirmed fixture eval exposes `transcript_session_eval_runner_contract_present`.
- Confirmed unsafe transcript content is reported through `privacy_errors` without echoing raw secret-like text, local user paths or raw private chat log markers.

## Completed Focused Checks For T8-B

- Added RED then GREEN tests for `governance-proposal.md`, standards trigger template coverage, readiness gate coverage, fixture eval coverage and lifecycle skill wording.
- Confirmed ADR trigger policy covers architecture boundary, API contract, storage, auth/security, irreversible migration and automation activation with `not_applicable` or accepted-gap options.
- Confirmed C4/arc42, OpenAPI source of truth vs Swagger UI, AsyncAPI producer/consumer compatibility fields, SemVer impact and Keep a Changelog categories are represented in templates.
- Confirmed CODEOWNERS status and GitHub Actions least-privilege proposals stay staged through `governance-proposal.md` with no forced external activation.
- Confirmed fixture eval exposes `standards_trigger_contract_present`.

## Completed Focused Checks For T8-GX

- Added RED then GREEN tests requiring five false-positive/approval-bound fixtures and fixture eval keys.
- Confirmed `backend-no-fsd` and `native-no-fsd` do not set `fsd_structure`.
- Confirmed `simple-crud-no-ddd` does not force `domain_model_when_complex_domain`.
- Confirmed `docs-light-no-portal` does not select MkDocs, Docusaurus, Sphinx, Antora or Read the Docs.
- Confirmed `hosted-docs-approval` keeps hosted docs and DB introspection as `approval_required`.
- Confirmed new fixtures are synthetic and secret-free.

## Completed Focused Checks For T8-D

- Added RED then GREEN tests for top-level `methodology_applicability` discovery packets.
- Confirmed every packet has `status`, `applies_when`, `reason`, `evidence`, `required_evidence`, `owner` and `residual_risk`.
- Confirmed status transitions for complex-domain DDD (`applicable_missing`), applicable FSD structure (`present_unverified`), docs tooling approval boundaries (`approval_required`) and standards trigger context (`present_unverified`).
- Confirmed fixture eval exposes `methodology_applicability_contract_present`.

## Completed Focused Checks For T9-D1

- Added RED then GREEN tests for `business_product` catalog contract, audit recommendations, staged product templates, lifecycle skill wording and fixture eval coverage.
- Confirmed `business_product_contract_present` covers product hypothesis, value proposition, opportunity framing, decision horizon, metric scope, analytics tracking, qualitative feedback, release measurement and workflow-promotion value evidence.
- Confirmed typo-only docs edits, formatting-only edits and dependency pins without behavior impact keep Business/Product methodology not applicable.

## Completed Focused Checks For T9-D2

- Added RED then GREEN tests for `requirements_domain` catalog contract, audit recommendations, staged requirements/domain templates, lifecycle skill wording and fixture eval coverage.
- Confirmed behavior-changing work without acceptance scenarios is a `P0_blocker`.
- Confirmed risky/public-contract work requires requirement quality, stable IDs, constraints traceability and API/UI/data traceability.
- Confirmed unclear stories, business rules, domain events, owner review, accepted gaps, declarative scenario quality and requirement change impact produce deterministic recommendations.
- Confirmed unsupported methodology claims are rejected as evidence: BDD replaces testing, Gherkin is mandatory, user story template is complete requirements, glossary is ubiquitous language and OpenAPI is requirements source of truth.

## Completed Focused Checks For T9-D3

- Added RED then GREEN tests for `solution_architecture` catalog contract, audit recommendations, staged architecture templates, lifecycle skill wording and fixture eval coverage.
- Confirmed multi-surface public API/data/runtime work produces architecture recommendations for scope, context/container boundaries, boundary owner, public contract trace, data ownership, trust boundary review, ADR, observability, rollback, diagram render checks and fitness functions.
- Confirmed typo-only docs edits, formatting-only edits, docs-light prototypes without reviewed/diffable diagrams and non-cloud work without Well-Architected review keep Solution Architecture methodology not applicable.
- Confirmed unsupported architecture claims are rejected as evidence: architecture means diagrams, rendered diagram proves correctness, C4 code diagrams are always required, ADR is bureaucracy, Well-Architected review proves architecture quality, architecture-as-code is always required and AI can design architecture from chat alone.
- Confirmed fixture eval exposes `solution_architecture_contract_present`.

## Completed Focused Checks For T9-D4

- Added RED then GREEN tests for `quality_testing_evals` catalog contract, audit recommendations, discovery signals, staged quality templates, lifecycle skill wording, behavioral eval coverage and fixture eval coverage.
- Confirmed missing local command/evidence and completion claims without current evidence are `P0_blocker`.
- Confirmed risky scope, acceptance traceability, deterministic change, API/event/schema contracts, runtime/manual/visual evidence, AI eval reruns, CI gates, test data privacy, bug reproduction and regression impact produce deterministic recommendations with stable artifacts.
- Confirmed typo-only docs edits, formatting-only edits, docs-only source cleanup and dependency metadata without behavior impact keep Quality, Testing & Evals methodology not applicable.
- Confirmed unsupported quality claims are rejected as evidence: more tests always means better quality, 100 percent line coverage proves correctness, E2E tests should dominate, manual QA is not evidence and AI evals are optional for AI behavior changes.
- Confirmed fixture eval exposes `quality_testing_evals_contract_present`.

## Evidence Format

- Command:
- Exit code:
- Relevant output:
- Files or artifacts inspected:
- Claims still `present_unverified`:
- Residual risk:
<!-- product-agent-os:end test-plan -->
