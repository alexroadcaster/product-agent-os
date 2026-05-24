# TEST.md

<!-- product-agent-os:start test-plan -->
Project: Codex Docs / Product-Agent OS
Generated at: 2026-05-24

## Current Baseline

- Focused T8-D discovery/fixture suite: `python -m unittest tests.product_agent_os.test_discovery tests.product_agent_os.test_fixture_eval_runner -v` ran 48 tests with `OK`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 326 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; summary check showed 40 fixtures, 0 failures, renderer file count 75 and `methodology_applicability_contract_present: true`.
- Transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions, 4 passed and 0 failed.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs check: `python tools\check_docs.py` passed.
- Strict MkDocs: `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict` exited `0`.

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

## Evidence Format

- Command:
- Exit code:
- Relevant output:
- Files or artifacts inspected:
- Claims still `present_unverified`:
- Residual risk:
<!-- product-agent-os:end test-plan -->
