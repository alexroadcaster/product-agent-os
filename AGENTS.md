# AGENTS.md

## Project purpose

This repository is a Russian knowledge base for researching OpenAI Codex, advanced agentic workflows, multi-agent systems, memory, skills, subagents, prompt/context engineering, Codex runtime automation, and product-agent workflows.

## Documentation rules

- Write user-facing docs in Russian.
- Keep official OpenAI terms in English on first mention, for example Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, memory, sandbox, approvals.
- Treat official OpenAI documentation as source of truth.
- Keep community tricks and user reports under `docs/insights/` with `trust_level` and `verification_status`.
- Do not move community claims into core guides unless they are verified or explicitly marked as `community` or `experiment`.
- Update `docs/sources/registry.md` when adding or changing source-backed claims.
- Use `Source status:` on every non-index documentation page except source registry pages.
- Treat `docs/diagrams/` as the project implementation atlas. It must stay near the top of MkDocs navigation and should be the first route for readers who want to build products with Codex agents and skills.
- Keep product-agent operating guidance under `docs/product-agent/`, runtime execution guidance under `docs/runtime/`, and reusable artifact templates under `docs/artifact-templates/`.
- Treat `docs/codex/use-cases-deep-analysis.md` as the official use-case extraction map. New playbooks, skills, plugins, and automations should reference an official use-case archetype when one exists.
- Use `docs/playbooks/use-case-to-plugin.md` when turning a repeated workflow into a distributable plugin, and use `docs/artifact-templates/plugin-blueprint.md` for plugin design.
- Prefer behavior-level documentation over tool hype: every new workflow should name inputs, outputs, verification, risks, and the next artifact it produces.

## Diagram atlas rules

- Keep `docs/diagrams/index.md` as the entry point for end-to-end project implementation.
- Maintain separate Mermaid pages for project delivery, agent teams and skills, runtime choices, skill lifecycle, and context/memory/verification.
- Every diagram page must include `Source status:`, a Mermaid diagram, usage guidance, related artifacts or playbooks, and common failure modes.
- When adding a new product-agent workflow, check whether one of the diagram pages must change so the atlas remains a current operating map.
- Do not let diagrams become decorative. Each diagram must answer a practical project question and point to the next action or artifact.
- If a diagram introduces a new required page, add it to `mkdocs.yml` and `tools/check_docs.py`.

## Product-agent operating model

- Use `AGENTS.md` for durable project rules.
- Use `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, and `RUNLOG.md` templates for long-running product work.
- Use skills for repeatable methods and automations only after a skill or manual workflow is stable.
- Do not create or switch to a new git branch or worktree unless the user explicitly asks for it. By default, work in the current branch and only report when isolation would be useful.
- Use worktrees or explicit ownership when parallel agents may edit overlapping files, but only after explicit user approval for the worktree or branch change.
- Design agent teams around ownership, handoff artifacts, verification, and stop conditions rather than vague roles.
- Give every durable project agent an explicit model/reasoning policy: default model, reasoning effort, escalation rules, downgrade rules, and cost/latency budget.
- Use stronger reasoning for planning, architecture, review, debugging, eval judging, security, and ambiguous multi-step work; use lower reasoning for bounded, mechanical, or read-only collection tasks.
- For Python implementation work, use the `python-design-patterns` and `python-code-style` skills when available as advisory coding guidance, while preserving existing project patterns and verification requirements.
- Promote project knowledge in this order: manual workflow, playbook, skill, automation, durable rule.
- Use eval-driven loops for subjective or long-horizon tasks: baseline, one focused change, rerun eval, inspect artifacts, log result, stop only at threshold.
- Promote reusable product workflows in this order: official use-case archetype, manual thread, playbook, skill, plugin, automation.

## Windows Codex shell guard

- In Codex App Windows PowerShell sessions, the inherited process environment may contain both `PATH` and `Path`. This breaks PowerShell/.NET environment enumeration and `Start-Process` when redirecting stdout or stderr with `An item with the same key has already been added`.
- Before running PowerShell commands that use `Get-ChildItem Env:`, `[System.Environment]::GetEnvironmentVariables()`, `Start-Process` with `-RedirectStandardOutput` or `-RedirectStandardError`, long-running background helpers, or dashboard/dev-server launches, normalize `PATH`/`Path` in the same PowerShell invocation.
- Use this guard as a process-local workaround only. Do not edit Windows registry `Path`, user environment variables, or machine environment variables for this issue unless the user explicitly asks for a system-level change.
- Minimal pattern:

```powershell
$pathValue = [System.Environment]::GetEnvironmentVariable('Path', 'Process')
if ([string]::IsNullOrEmpty($pathValue)) {
    $pathValue = [System.Environment]::GetEnvironmentVariable('PATH', 'Process')
}
if (-not [string]::IsNullOrEmpty($pathValue)) {
    [System.Environment]::SetEnvironmentVariable('Path', $null, 'Process')
    [System.Environment]::SetEnvironmentVariable('PATH', $null, 'Process')
    [System.Environment]::SetEnvironmentVariable('Path', $pathValue, 'Process')
}
# command that enumerates env or uses Start-Process redirect follows here
```

## Product-Agent OS plugin rules

- Treat `plugins/product-agent-os/` as the implementation package for the local Product-Agent OS plugin.
- Treat `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md` as the active Track 9 implementation plan.
- Track 9 methodology intelligence work is section-by-section. Before implementing any Track 9 section, read only that section's task block in the plan, then perform a deep audit of the matching source file under `docs/methodologies/`.
- If the deep audit finds concepts, gates, artifacts, false-positive risks, tooling choices or conflicts that are not represented in the Track 9 plan, update the plan or Track 9 backlog before implementation. Do not implement from an outdated task list.
- After the plan/backlog is current for that section, implement the focused slice with tests/evals/docs sync and record verification evidence.
- Track 3 infrastructure generation is staged-first. The renderer may inspect a target workspace and write staged artifacts only to an explicit staging directory; it must not silently mutate the target project.
- Use `python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --dry-run` before staging infrastructure for a project.
- Use `--stage <output-dir>` only with an output directory outside the target workspace unless a later Track 4 merge workflow explicitly proves a safe approved write path.
- Preserve user-authored files outside managed sections. Existing unmarked `AGENTS.md`, `.codex/config.toml`, hooks, workflows, and automation files must be treated as user content and staged as companion proposals rather than overwritten.
- Packaged hooks are examples and staged target-project assets. Do not add plugin-root hook activation or enable target-project hooks without explicit approval.
- Automation artifacts under `assets/templates/automations/` are candidate-only. Do not create schedules, recurring jobs, GitHub Actions, Codex App automations, or external workflows from Track 3 templates.
- Template files, fixtures, and generated examples must remain synthetic and must not contain secrets, private customer data, raw private chat logs, or absolute user-specific paths.

## Product-Agent OS implementation status

- Track 1 plugin core and contracts are implemented under `plugins/product-agent-os/`.
- Track 2 lifecycle skills are implemented under `plugins/product-agent-os/skills/`.
- Track 3 generated infrastructure is implemented with template registry, staged renderer, CLI wrapper, fixture eval coverage, and templates under `plugins/product-agent-os/assets/templates/`.
- The Track 3 renderer supports dry-run JSON output and staged artifact generation; direct project merge is still outside current scope.
- Track 3 baseline was refreshed on 2026-05-14: `python -m unittest discover -s tests -p "test_*.py" -v` ran 113 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` returned `ok: true` for all fixtures, `python tools\check_docs.py` passed, and strict MkDocs build exited `0`.
- Track 4 production hardening is implemented with staged manifest, explicit approval record, safe merge planner/apply, rollback, hook activation gate, workspace-bound stage manifest validation, source-policy validation, automation promotion validation, behavior-level fixture eval coverage, and optional Agents SDK runner design artifact.
- Track 4 baseline was refreshed on 2026-05-15: `python -m unittest discover -s tests -p "test_*.py" -v` ran 194 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with all fixtures `ok: true` and behavior-level merge/hook/path checks, `python tools\check_docs.py` passed, and strict MkDocs build exited `0`.
- Track 5 Codex runtime runner is implemented with dependency-free contract mode, lifecycle routing, handoff/source/approval/automation/redaction guards, CLI wrappers, inactive-by-default plugin boundary, and fixture eval coverage.
- Track 5 baseline was refreshed on 2026-05-15: focused Track 5 tests ran 25 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 221 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`, `python tools\check_docs.py` passed, strict MkDocs build exited `0`, and removed standalone/live runner path grep returned no matches.
- Track 6 engineering standards layer is implemented with methodology-backed workflow templates for product hypothesis, architecture boundaries, test/eval-first development, documentation-as-code, source-backed claims, and post-release measurement.
- Track 6 baseline was refreshed on 2026-05-23: `python tools\check_docs.py` passed, `python -m unittest discover -s tests -p "test_*.py" -v` ran 223 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 36 and all fixtures `ok: true`, and strict MkDocs build exited `0`.
- Track 7 engineering standards hardening is implemented with methodology signal discovery, methodology gaps in workspace audit risks, readiness eval gates, Red-Green-Refactor guidance, concrete artifact templates for ADR/architecture/domain/metrics/API/UI/database documentation, OpenAPI v3.2.0 source update, and source-doc hygiene fixes.
- Track 7 baseline was refreshed on 2026-05-23: `python -m unittest discover -s tests -p "test_*.py" -v` ran 227 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 43 and all fixtures `ok: true`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0`.
- Track 8 scenario workflows through T8-S16 are implemented with packaged workflows/artifacts for first-run intake, bug rescue, greenfield idea, complex system acceleration, PR review, legacy onboarding, API migration, AI/RAG eval regression, native/mobile feature work, desktop local-first work, data migration, security-sensitive change, CI stabilization, and release packaging.
- Track 8 T8-S16 baseline was refreshed on 2026-05-23: focused T8-S16 tests ran 98 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 283 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 72, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-A13 no-placeholder planning hardening is implemented with implementation-planner plan-quality enforcement, strengthened `PLAN.md`, `build-slice.md`, `plan-quality-check.md`, expanded behavioral eval fields, and fixture eval coverage for `plan_quality_contract_present`.
- Track 8 T8-A13 baseline was refreshed on 2026-05-23: focused T8-A13 tests ran 71 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 285 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 72, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-A14 generalized two-stage review is implemented with risk-reviewer generalized review routing, strengthened `review-slice.md`, `RUNLOG.md`, `pr-risk-review.md`, and expanded `two-stage-review` behavioral eval fields for risky/public-contract/migration/security/data/release/parallel slices.
- Track 8 T8-A14 baseline was refreshed on 2026-05-23: focused T8-A14 tests ran 63 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 287 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 72, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-A15 fresh-context handoff hardening is implemented with agent-team-designer enforcement for any subagent or parallel worker, strengthened `handoff-contract.md`, `agent-task-packet.md`, `worktree-ownership.md`, and expanded `fresh-context-handoff` behavioral eval fields for complete task context, source constraints, ownership, expected evidence, handoff output schema, stop conditions, and sequential fallback.
- Track 8 T8-A15 baseline was refreshed on 2026-05-24: focused T8-A15 tests ran 65 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 289 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 72, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-A3/T8-A4 acceptance scenario hardening is implemented with `acceptance-scenarios.md`, generated `REQUIREMENTS/TEST/EVALS` traceability fields, `development-standards.md`, `project-readiness.json`, `behavioral-workflows.json`, fixture eval coverage, and lifecycle skill enforcement in `requirements-author`, `implementation-planner`, and `test-eval-designer`.
- Track 8 T8-A3/T8-A4 baseline was refreshed on 2026-05-24: focused T8-A3/T8-A4 tests ran 77 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 291 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 73, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-A5 conditional DDD domain modeling gate is implemented with `domain_model` discovery signal, complex-domain gap detection, `domain_model_when_complex_domain` readiness gate, strengthened `domain-modeling.md`, implementation-planner stop condition, and fixture eval coverage for `domain_model_gate_contract_present`.
- Track 8 T8-A5 baseline was refreshed on 2026-05-24: focused T8-A5 tests ran 104 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 294 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 73, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-A6 bounded context architecture traceability is implemented with architecture context-map discovery, `bounded_context_architecture_boundary_trace` readiness gate, strengthened `domain-modeling.md` and `architecture-overview.md`, implementation-planner stop condition, and fixture eval coverage for `bounded_context_trace_contract_present`.
- Track 8 T8-A6 baseline was refreshed on 2026-05-24: focused T8-A6 tests ran 106 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 296 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 73, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-A7 ubiquitous language traceability is implemented with `ubiquitous_language_traceability` readiness gate, strengthened `domain-modeling.md`, generated `PLAN/TEST/EVALS/RUNLOG` fields, implementation-planner stop condition, and fixture eval coverage for `ubiquitous_language_traceability_contract_present`.
- Track 8 T8-A7 baseline was refreshed on 2026-05-24: focused T8-A7 tests ran 79 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 298 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 73, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-A8 FSD structure routing is implemented with optional `fsd_structure` discovery, positive/negative false-positive tests, conditional Feature-Sliced Design guidance in `component-card.md` and `development-standards.md`, lifecycle skill routing, and readiness signal coverage.
- Track 8 T8-A8 baseline was refreshed on 2026-05-24: focused T8-A8 tests ran 102 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 302 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 73, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-A9 metric hardening is implemented with strengthened `metric-spec.md`, `release-packet.md`, generated `REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG` metric fields, `project-readiness.json` gate/signal coverage, lifecycle skill enforcement, and fixture eval coverage for `metric_hardening_contract_present`.
- Track 8 T8-A9 baseline was refreshed on 2026-05-24: focused T8-A9 tests ran 83 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 304 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 73, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-A16 evidence-before-completion generalization is implemented with `evidence-before-completion` behavioral eval coverage, `evidence_before_completion` readiness gate/signal coverage, strengthened `release-packet.md`, `development-standards.md`, generated `AGENTS/PLAN/TEST/EVALS/RUNLOG`, lifecycle skill enforcement across all Product-Agent OS skills, and fixture eval coverage for `completion_evidence_contract_present`.
- Track 8 T8-A16 baseline was refreshed on 2026-05-24: focused T8-A16 tests ran 87 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 306 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 73, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-C docs tooling selector with T8-A11 closure is implemented with `docs-tooling-decision.md`, `docs_tooling_decision` discovery output, `docs_tooling_selector` readiness contract, `docs_as_code_impact` statuses, strengthened `documentation-system.md`, generated `PLAN/TEST/EVALS/RUNLOG`, lifecycle skill enforcement, stack-aware docs tool routing and fixture eval coverage for `docs_tooling_selector_contract_present`.
- Track 8 T8-C baseline was refreshed on 2026-05-24: focused T8-C tests ran 122 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 312 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 74, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-F conditional readiness gates are implemented with `readiness_statuses`, structured `conditional_readiness_gates` in `project-readiness.json`, generated `AGENTS/PLAN/TEST/EVALS/RUNLOG` fields, lifecycle skill enforcement, and fixture eval coverage for `conditional_readiness_gates_contract_present`.
- Track 8 T8-F baseline was refreshed on 2026-05-24: focused T8-F tests ran 88 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 313 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 35 fixtures, 0 failures and renderer file count 74, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-H scenario/eval docs are implemented with dedicated `docs/product-agent-os/scenarios.md`, `behavioral-evals.md`, and `codex-compatibility.md`, MkDocs navigation, docs structure enforcement, source registry closure note, Product-Agent OS README/docs sync, and focused docs contract coverage.
- Track 8 T8-H baseline was refreshed on 2026-05-24: focused T8-H docs tests ran 3 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 316 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 35 fixtures, 0 failures and renderer file count 74, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-GY transcript/session eval runner is implemented with `product_agent_os/transcript_evals.py`, `run_transcript_eval.py`, packaged synthetic transcript sessions, deterministic expected/forbidden term replay, privacy/no-secrets guards, docs sync, and fixture eval coverage for `transcript_session_eval_runner_contract_present`.
- Track 8 T8-GY baseline was refreshed on 2026-05-24: focused T8-GY transcript/fixture tests ran 14 tests with `OK`, focused docs closure tests ran 3 tests with `OK`, `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures, `python -m unittest discover -s tests -p "test_*.py" -v` ran 320 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 35 fixtures, 0 failures and renderer file count 74, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-B standards trigger hardening is implemented with `governance-proposal.md`, strengthened ADR/C4/arc42/OpenAPI/AsyncAPI/SemVer/Keep a Changelog/CODEOWNERS/GitHub Actions trigger policy in packaged templates, `standards_trigger_policy_when_architecture_api_release_or_governance_changes`, lifecycle skill routing, and fixture eval coverage for `standards_trigger_contract_present`.
- Track 8 T8-B baseline was refreshed on 2026-05-24: focused T8-B template/fixture/lifecycle tests ran 90 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 322 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 35 fixtures, 0 failures and renderer file count 75, `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-GX scenario fixture coverage hardening is implemented with synthetic false-positive and approval-bound fixtures: `backend-no-fsd`, `native-no-fsd`, `simple-crud-no-ddd`, `docs-light-no-portal`, and `hosted-docs-approval`; fixture eval now asserts FSD is not forced on backend/native work, DDD is not forced on simple CRUD `src/domain/*`, docs-light does not select heavy docs portals, and hosted docs/DB introspection remain approval-required.
- Track 8 T8-GX baseline was refreshed on 2026-05-24: focused T8-GX fixture tests ran 27 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 324 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 40 fixtures, 0 failures and renderer file count 75, `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 8 T8-D detailed discovery model status depth is implemented with top-level `methodology_applicability` packets in discovery output, status transitions for methodology/tooling readiness, and fixture eval coverage for `methodology_applicability_contract_present`.
- Track 8 T8-D baseline was refreshed on 2026-05-24: focused T8-D discovery/fixture tests ran 48 tests with `OK`, `python -m unittest discover -s tests -p "test_*.py" -v` ran 326 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 40 fixtures, 0 failures, renderer file count 75 and `methodology_applicability_contract_present: true`, transcript eval exited `0` with 4 sessions and 0 failures, `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` passed, and strict MkDocs exited `0` with `NO_MKDOCS_2_WARNING=1`.
- Track 9 T9-D12 Delivery, Release & Operations methodology integration is implemented with release scope, versioning, changelog/release notes, artifact manifest, release evidence, rollout, rollback, CI/CD governance, observability/SLO, operations runbooks, incidents, post-release learning, release mode, build-release-run, platform distribution, DORA, release integrity handoff, owner-reviewed release evidence sufficiency, synthetic false-positive fixtures, lifecycle routing and fixture eval coverage.
- Track 9 T9-D12 baseline was refreshed on 2026-05-27: focused delivery suite ran 298 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 66 fixtures, 0 failures and renderer file count 186, `python -m unittest discover -s tests -p "test_*.py" -v` ran 478 tests with `OK`, transcript eval exited `0` with 5 sessions and 0 failures, Codex compatibility returned `status: compatible`, `python tools\check_docs.py` passed, and `git diff --check` exited `0`.
- Track 9 Task 20 Cross-Domain Synthesis is implemented through `T9-S-M14` with grouped recommendation synthesis, owner/consumer/source domains, source artifact ledger, alias/deferred artifact decisions, semantic evidence sufficiency, owner-question dedupe, risk-aware safe next action, cross-domain false-positive fixtures, methodology report rendering, lifecycle skill consumption and docs/eval sync.
- Track 9 T9-S-M10..M14 baseline was refreshed on 2026-05-27: focused synthesis suite ran 316 tests with `OK`, `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 73 fixtures, 0 failures and renderer file count 186, `python -m unittest discover -s tests -p "test_*.py" -v` ran 496 tests with `OK`, transcript eval exited `0` with 5 sessions and 0 failures, Codex compatibility returned `status: compatible`, `python tools\check_docs.py` passed, and `git diff --check` exited `0`.
- Root project control-plane files were updated on 2026-05-27: `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, and `RUNLOG.md` now track the active Product-Agent OS Track 9 implementation state after `T9-S-M14`.
- Track 9 methodology intelligence design is captured in `docs/superpowers/specs/2026-05-25-track-9-methodology-intelligence-design.md`.
- Track 9 implementation plan is captured in `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`.
- Next Product-Agent OS implementation work is Track 9 `Task 21: Update Runtime Runner And Finish Options`. For every Track 9 section, first read the relevant plan task, deeply audit the matching checked-in source or backlog context, update the plan/backlog if gaps are found, and only then implement.

## Source and insight policy

- Official OpenAI docs, OpenAI GitHub repositories, and OpenAI-authored guides are authoritative.
- Context7 findings are accepted as official only when their underlying source is official.
- Community sources are intake material, not instructions, until captured as insight cards and verified.
- Never store secrets, tokens, private keys, or private customer data in docs, insights, memory notes, examples, or templates.

## Verification

After editing documentation, run:

```powershell
python tools\check_docs.py
```

After editing `plugins/product-agent-os/` scripts, templates, fixtures, or tests, also run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

After changing navigation, Mermaid diagrams, Markdown extensions, or MkDocs configuration, also run:

```powershell
python -m mkdocs build --strict
```

If `mkdocs` is installed into the temporary project runtime, use:

```powershell
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; python -m mkdocs build --strict
```
