# Batch 45 S9-A Durable Contract Recovery

Source status: `active local implementation plan; no live or provider evidence`

## Scope

- Schema version: task_matrix_plan_v1
- Generated at: 10-08-2026 15:15 Europe/Moscow
- Project: Product-Agent OS
- Workspace: `C:\Users\user\Desktop\project\codex_docs`
- Profile: Batch 45 durable promotion-output contract recovery
- Detected stack: Python runtime and unittest tooling with JSON Schema compatible local contracts and synthetic fixtures
- Timezone: Europe/Moscow

### Task `B45-S9-A`

- Task: Implement `B45-CQRR-T23` and `B45-CQRR-T24` as one coupled red-green durable-contract slice.
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: The user explicitly authorized implementation of `B45.S9-A` with agents and skills after `B45-S9-0` established the T23/T24 fresh-context handoffs.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-08-2026 15:15
- Depends on: `B45-POSTQ4-T22-A02`; `B45-CQRR-A01`; `B45-CQRR-A02`; `B45-CQRR-A03`; completed `B45-S9-0` handoff readiness.
- Blocks: `B45-S9-B` and every later recovery group until the durable contract and focused regression evidence are independently reviewed.
- Source: `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`; `docs/superpowers/specs/batch45-code-quality-runtime-recovery-agent-team.json`; `docs/superpowers/specs/batch45-s9-0-fresh-context-handoffs.json`; Track 11 plan; current runner source and tests.
- Short description: Freeze one versioned promotion-result contract, prove the T21 schema failure red, integrate the contract into the real runner, then prove valid normalization and invalid-output quarantine with local deterministic tests.
- Technical value: Replaces a one-off schema boundary with one mutable schema/enum source and prevents invalid primary results from reaching pair aggregation, reviewer routing or promotion decisions.
- Product value: Makes the Batch 45 recovery gate depend on meaningful executable behavior rather than schema prose, test count, line coverage or model self-score.
- Scope: `promotion_contract.py`; `model_output.py`; `test_codex_runtime_runner_promotion_contract.py`; synthetic fixtures under `tests/fixtures/product_agent_os/batch45/promotion-contract/`; current-evidence task plan, verification and handoff updates.
- Non-goals: No T25-T34 implementation; no prompt redesign; no downstream deterministic-metric or corpus work; no live eval; no provider/model/external reviewer call; no browser/server; no dependency installation; no hook, automation, MCP or Agents SDK activation; no Git or release action.
- Expected result: The real runner imports one versioned contract and normalization implementation; the exact T21 `tests_or_checks.status` mismatch and every scoped invalid class fail locally before aggregation; fixtures remain synthetic and sanitized.
- Acceptance criteria: Contract version and enums have one mutable source; unknown fields, required fields, ranges, malformed arrays, timeout/no-op and normalization rules are executable; the observed red precedes production implementation; focused tests and seeded-corruption checks pass after the minimal fix; invalid pairs cannot reach reviewer or promotion logic; independent read-only review and claim-gate review report no blocking finding.
- Verification gates: `python -m unittest tests.product_agent_os.test_codex_runtime_runner_promotion_contract -v`; `python -m unittest tests.product_agent_os.test_codex_runtime_runner_model_output -v`; focused seeded-corruption proof; task-matrix validator; relevant Product-Agent OS docs/contracts tests; `python tools\check_docs.py`; `git diff --check`.
- Risks / approval gates: Stop on schema duplication, absent red evidence, implementation-shaped assertions, unsanitized fixture, aggregation leakage, writer-scope overlap or any external action. T23 production files and T24 test/fixture files have disjoint writers and execute sequentially.
- Complexity: high
- Estimated execution time: 45-90 minutes
- Agents: `architect` freezes the contract read-only; `tester` owns tests and fixtures; `plugin-runtime-builder` alone owns production files; `reviewer` and `completion-skeptic` are read-only; `docs-maintainer` owns post-gate evidence synchronization.
- Skills: `implementation-planner`; `agent-team-designer`; `python-design-patterns`; `python-code-style`; `tdd`; project-local control-plane sync and docs maintenance.
- Output artifacts: `plugins/product-agent-os/scripts/codex_runtime_runner/promotion_contract.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/model_output.py`; `tests/product_agent_os/test_codex_runtime_runner_promotion_contract.py`; `tests/fixtures/product_agent_os/batch45/promotion-contract/`; this plan; required current-evidence control-plane and registry updates.
- Next step: Start `B45-S9-B` / T25 through its `B45-CQRR-A03` fresh-context packet; retain Batch 45 as advisory-only/no-go.

#### Completion Report

- status: implemented
- what was done: `B45-CQRR-A04` implements the T23 versioned promotion-result contract and T24 local red-green regression coverage. The runner now uses the shared parse/quarantine gateway before scoring; invalid results cannot enter reviewer or promotion routing.
- files touched / work locations: `plugins/product-agent-os/scripts/codex_runtime_runner/promotion_contract.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/model_output.py`; `tests/product_agent_os/test_codex_runtime_runner_promotion_contract.py`; synthetic promotion-contract fixtures; current-evidence documents listed in this report.
- technical value delivered: one mutable contract/enum source, executable normalization and quarantine, T21 `tests_or_checks.status` regression coverage, and defensive pair revalidation.
- product value delivered: the local recovery gate now rejects malformed primary results deterministically instead of allowing a schema mismatch to masquerade as promotion evidence.
- actual implementation date and time: 10-08-2026 15:15
- red histories: initial absent module: exit 1, Ran 1, errors 1 (`ModuleNotFoundError`); intermediate complete-contract run: exit 1, Ran 13, failures 59/errors 1; independent-review bypass probes: exit 1, Ran 15, failures 25; oversized integer: exit 1, Ran 15, errors 1 (`OverflowError`).
- verification evidence: final `python -m unittest tests.product_agent_os.test_codex_runtime_runner_promotion_contract -v` exit 0, Ran 15, OK; final `python -m unittest tests.product_agent_os.test_codex_runtime_runner_model_output -v` exit 0, Ran 8, OK; after the final edge repair, the combined promotion+legacy command exit 0, Ran 23, OK; direct structural check `schema_equal=True`; scoped `git diff --check` exit 0. Independent read-only reviewer verdict: `GO_local_code_gate`, no blocking code findings. Completion-skeptic verdict: `GO_local_code_gate` for the local provider-free executable-contract claim.
- unsupported claims: no CLI/runtime activation, live/model/provider/reviewer behavior, promotion result, M26/T22 reversal, browser/target/CI/Git/release/deploy/automation or production-readiness proof.
- completion claim state: `partially_verified` until this evidence sync is accepted in the control plane; all timestamps use the task's Europe/Moscow timezone.
- residual risks: Batch 45 remains advisory-only/no-go and a live rerun remains separately exact-approval-only.
- follow-up: `B45-S9-B` / T25 through its A03 packet, without treating A04 as authorization for T25-T34.

### Professional Code Authoring Checklist (completed)

- `enterprise_leverage_check`: completed — the slice removes a promotion-evidence failure mode at the shared output boundary; it does not claim enterprise-quality generation.
- Existing source, model-output and tests inspected before the patch: completed.
- Implementation choice: Python standard library and small custom contract module; no new dependency and no one-line JSON-Schema validator.
- `negative_dependency_rule`: completed — no dependency installation or activation.
- `deep_module_check` and `legacy_seam_check`: completed — the real runner import path and existing model-output behavior were retained and joined by the parse/quarantine gateway.
- Comments / cleverness decision: comments explain the forged-dataclass and post-parse-mutation invariant; no clever abstraction or policy prose was added.
- Rollback: revert only the T23/T24 production, test/fixture and A04 evidence changes as one slice; preserve the historical T21 literal limitation and A01-A03 roles.
- Claim ceiling: `locally_implemented_and_focused_verified` only; after this sync the task remains `partially_verified` pending the parent completion handoff. No live, CLI, provider, promotion or broad-quality claim.

## Ownership And Sequential Handoff

| Step | Agent | Write scope | Required evidence | Stop condition |
| --- | --- | --- | --- | --- |
| Contract freeze | `architect` | none | Version, fields, enum/range rules, normalization and quarantine boundary | Missing or duplicated source of truth |
| T24 red | `tester` | `test_codex_runtime_runner_promotion_contract.py`; synthetic fixture directory | Exact observed failing assertion for T21 class | No red, schema-text-only assertion or private output |
| T23 implementation | `plugin-runtime-builder` | `promotion_contract.py`; `model_output.py` | Minimal diff using T24 red as the executable target | Test rewrite request, aggregation leak or external call |
| T24 green | `tester` | same T24 scope only | Focused green plus seeded corruption | Fault class not detected |
| Independent review | `reviewer`; `completion-skeptic` | none | Findings, supported/unsupported claims and residual risk | Any blocking correctness or claim-boundary finding |
| Evidence sync | `docs-maintainer` | current-evidence plan/control-plane/registry paths only | Validated completion report and compact handoff | Missing verification or overlap with unrelated dirty work |

## Safety And Evidence Boundaries

- This plan authorizes only local owned-file work inside T23/T24.
- Synthetic fixtures must not contain raw model outputs, private prompts, credentials, customer data or absolute user-specific paths.
- No live/provider/runtime/reviewer call, Git action, activation, deployment, publication or promotion is authorized.
- Current local tests can prove the executable contract only; they cannot prove improved model code quality or release readiness.
