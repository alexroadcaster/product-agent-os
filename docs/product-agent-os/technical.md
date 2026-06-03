# Технические особенности и установка

Source status: `official + experiment`  

## Quick start

Для оператора эта страница отвечает на вопрос "какие локальные surfaces есть у plugin и где искать команду". Если нужна полная карта flags и approval boundaries, используйте [CLI Reference](cli-reference.md); если нужно понять generated outputs, используйте [Artifact Contracts](artifact-contracts.md).

| Задача | Стартовая команда или страница | Boundary |
| --- | --- | --- |
| Проверить staged infrastructure без writes | `render_infrastructure.py <workspace> --dry-run` | Read-only plan; target workspace не меняется. |
| Сгенерировать proposal outside target workspace | `render_infrastructure.py <workspace> --stage <stage-dir>` | Stage directory должен быть явным. |
| Построить static graph/cockpit | [Project Code Graph](project-code-graph.md) | Generated graph/cockpit are orientation evidence only. |
| Проверить live/runtime/provider gates | [Live Runtime Governance](live-runtime-governance.md) | No live server, no provider calls, no canonical graph mutation. |
| Подготовить Batch 34 closure | [Packaging And Closure](packaging-and-closure.md) | Source docs -> registry -> docs tests -> `check_docs.py` -> strict MkDocs -> optional full closure. |

## Implementation status archive

Task 26 Batch 32 `T10-LIVE-M27..M31` implements Real Testing Readiness, Target Consent, Pilot Harness And Codex Surface Smoke through `project_graph_real_testing.py`, covering `real-testing-readiness.json`, `real-testing-targets.json`, `pilot-harness.json`, `codex-surface-smoke.json` and `real-testing-pilot-matrix.json` artifact contracts. It stages `project_graph_real_testing_readiness`, `project_graph_real_testing_targets`, `project_graph_pilot_harness`, `project_graph_codex_surface_smoke` and `project_graph_real_testing_pilot_matrix` under approval boundary `batch32_real_testing_readiness_target_consent_pilot_harness_codex_surface_smoke`, with surfaces `real_testing_readiness`, `real_project_target_selection`, `pilot_harness`, `codex_surface_smoke` and `use_case_pilot_matrix`. Batch 32 is `approval_required`, staged evidence only and not source of truth: real testing cannot start with no hidden unresolved Track 10 gates; No real project test without owner-approved target and data policy; Pilot harness remains dry-run and stage-only; dry-run pilot harness evidence covers Codex App, CLI and IDE extension smoke; Track 8 archetypes web, backend, docs, pr_review, evals, automation and AI/RAG are mapped to pilots; `provider_call_allowed: false`, `external_call_performed: false`, no live server, no provider calls, no live external model/API calls, no canonical graph mutation, and git staging/commit/push/PR remains explicit-only.

Task 26 Batch 33 `T10-LIVE-M32..M34` implements Runtime Browser QA, Performance And Stabilization through `project_graph_runtime_qa.py`, covering `project-code-graph-runtime-browser-qa.json`, `project-code-graph-performance-budget.json` and `project-code-graph-stabilization-ledger.json` artifact contracts. It stages `project_graph_runtime_browser_qa`, `project_graph_performance_budget` and `project_graph_stabilization_ledger` under approval boundary `batch33_runtime_browser_qa_performance_stabilization`, with surfaces `runtime_browser_qa`, `runtime_performance_budget` and `runtime_stabilization_loop`. Batch 33 is `approval_required`, staged evidence only and not source of truth: browser smoke, console/network checks, mobile overflow checks, generated-view labels and source-boundary labels are recorded as QA evidence; budget breach disables live layer or records accepted gap; No open P0/P1 can remain before closure; `provider_call_allowed: false`, `external_call_performed: false`, no live server, no provider calls, no live external model/API calls, no canonical graph mutation, and git staging/commit/push/PR remains explicit-only.

Task 26 Batch 34 `T10-LIVE-M35..M36` is planned as Packaging, Docs, Source Registry, Closure And Batch 35 Handoff. The Batch 34 Detailed Task Matrix `B34-DOC-M01..M15` covers planned, not implemented updates for `project-code-graph.md`, `live-runtime-governance.md`, `approval-bound-real-testing.md`, `agent-skill-modernization-loop.md`, `cli-reference.md`, `artifact-contracts.md`, `packaging-and-closure.md`, existing docs IA, MkDocs nav, `tools/check_docs.py`, source registry, focused docs tests and regenerated `site/`. It preserves staged evidence only, not source of truth, no live server, no browser automation, no provider/live external model/API calls, no canonical graph mutation and no git stage/commit/push/PR.

Task 26 Batch 35 `T10-LIVE-M37..M41` is added as an Approval-Bound Real Testing Execution Matrix. It is planned, not implemented: `approved_local_runtime_launch`, `actual_browser_automation_smoke`, `approved_provider_api_pilot`, `approved_canonical_mutation_pilot` and `explicit_git_release_pr_action` are separate surfaces under approval boundary `batch35_approval_bound_real_testing_execution`. Batch 35 can run only after Batch 24 governance, Batch 25 runtime contract, Batch 31 audit/observability, Batch 32 target consent, Batch 33 QA/performance/stabilization and Batch 34 packaging/docs closure are current. Until separate explicit owner approval exists for each action, it starts no live server, runs no browser automation, performs no provider/live external model/API calls, performs no canonical graph mutation and performs no git stage/commit/push/PR.

Task 25 Batch 19 `T10-CG-V2-M33..M38` implements the approved offline static search index at `.codex/product-agent-os/project-code-graph-search-index.json`. The index is generated, cache-bound and not source of truth; it builds from graph artifact only, supports optional indexed search, blocks stale indexes, records cache hit/miss/invalidation and has a rollback/disable path. Batch 19 uses no live database/server, LLM, embedding or cross-encoder.

Task 25 Batch 20 `T10-CG-V2-M39..M44` implements the approved local query backend gate in `project_graph_backend.py`. The gate creates a generated local file-store at `.codex/product-agent-os/project-code-graph-backend.json` only from graph and static-index artifacts, records `project_graph_local_backend_gate_present`, requires an approval decision packet with storage path, port policy, process lifecycle, auth boundary, cleanup, logging, performance threshold and rollback path, and keeps server mode disabled by default. The backend store is not source of truth, no production server is started, read-only API handling is contract-only and graph-only fallback remains available.

Task 25 Batch 21 `T10-CG-V2-M45..M51` implements the approved semantic retrieval gate in `project_graph_semantic.py`. It records `project_graph_semantic_retrieval_gate_present`, a semantic corpus and chunk policy, embeddings cache metadata, semantic query packets and cross-encoder eval/reranking gate using local deterministic embeddings only. Semantic hits are `present_unverified` orientation evidence, there are no canonical graph edge rewrites, the rollback/disable path deletes `.codex/product-agent-os/project-code-graph-semantic-index.json`, and later Batch 22/23 closure work stays generated, approval-bound and non-source-of-truth.

Task 25 Batch 22 `T10-CG-V2-M52..M57` implements the approved local deterministic LLM semantic extraction proposal gate in `project_graph_llm_extraction.py`. It records `project_graph_llm_extraction_gate_present`, validates a Batch 22 explicit approval packet with prompt/model policy, emits structured JSON with provenance, uncertainty and unsupported-claim labels, stages semantic node and edge proposals plus rationale/comment proposals, and treats every output as staged proposals, not canonical graph facts. There is no canonical graph mutation, no live external model/API call and no source-of-truth claim; human review can accept, reject or mark `accepted_gap`, unsafe output routes to the AI incident workflow, and the rollback/disable path deletes `.codex/product-agent-os/project-code-graph-llm-proposals.json`.

Task 25 Batch 23 `T10-CG-V2-M58..M62` implements future extension verification, rollback and closure through `project_graph_extension_closure.py`. It adds `verify-extensions` and `disable-extensions`, fixture fields `project_graph_future_extension_closure_present`, `project_graph_extension_rollback_deletion_present`, `project_graph_unapproved_surface_blocking_present` and `project_graph_extension_full_verification_contract_present`, records rollback/data deletion proof, verifies graph-only fallback, keeps unapproved surfaces as `blocked_without_new_explicit_approval`, starts no live server, performs no live external model/API calls, mutates no canonical graph facts and preserves that git staging/commit/push/PR remains explicit-only.

Task 26 Batch 24 `T10-LIVE-M01..M06` implements Approval, Data Classification, Redaction, Credentials, Cache And Budget Governance through `project_graph_live_governance.py`. It records `project_graph_live_approval_packet_present`, `project_graph_live_data_classification_policy_present`, `project_graph_live_redaction_guard_present`, `project_graph_provider_credentials_boundary_present`, `project_graph_live_cache_deletion_policy_present`, `project_graph_live_budget_guard_present` and `project_graph_live_governance_no_live_calls_present`. Batch 24 is staged evidence only and not source of truth: no live server, no provider calls, no live external model/API calls, no canonical graph mutation, and git staging/commit/push/PR remains explicit-only.

Task 26 Batch 25 `T10-LIVE-M07..M10` implements Live Local Read-Only Runtime, Auth And Fallback through `project_graph_live_runtime.py`. It records `project_graph_live_runtime_contract_present`, `project_graph_live_runtime_governance_prerequisite_present`, `project_graph_live_runtime_read_only_routes_present`, `project_graph_live_runtime_lifecycle_controls_present`, `project_graph_live_runtime_auth_policy_present`, `project_graph_live_runtime_graph_only_fallback_present` and `project_graph_live_runtime_no_public_or_mutation_surface_present`. Batch 25 is staged evidence only and not source of truth: `disabled_by_default_not_started`, local-only access, rejects unauthorized access, no write endpoints, `graph_only_query_mode`, no provider calls, no live external model/API calls, no canonical graph mutation, and git staging/commit/push/PR remains explicit-only.

Task 26 Batch 26 `T10-LIVE-M11..M12` implements External Embedding Provider Gate And Eval through `project_graph_embedding_provider.py`. It records `project_graph_external_embedding_provider_gate_present`, `project_graph_external_embedding_governance_prerequisite_present`, `project_graph_external_embedding_redaction_cache_budget_present`, `project_graph_external_embedding_eval_baseline_present`, `project_graph_external_embedding_threshold_fallback_present` and `project_graph_external_embedding_no_live_calls_present`. Batch 26 is staged evidence only and not source of truth: No external call without approval/redaction/cache/budget, Must beat approved threshold or stay disabled, `semantic_retrieval_or_graph_only`, `provider_call_allowed: false`, `external_call_performed: false`, no provider calls, no live external model/API calls, no canonical graph mutation, and git staging/commit/push/PR remains explicit-only.

Task 26 Batch 27 `T10-LIVE-M13..M14` implements Cross-Encoder Reranker And Hybrid Retrieval through `project_graph_reranker_provider.py` (`reranker_provider.py` artifact contract) and `project_graph_hybrid_retrieval.py` (`hybrid_retrieval.py` artifact contract). It records `project_graph_external_reranker_provider_gate_present`, `project_graph_external_reranker_governance_prerequisite_present`, `project_graph_external_reranker_redaction_cache_budget_present`, `project_graph_external_reranker_eval_baseline_present`, `project_graph_external_reranker_threshold_fallback_present`, `project_graph_external_reranker_no_live_calls_present`, `project_graph_hybrid_retrieval_pipeline_present`, `project_graph_hybrid_retrieval_explainable_fusion_present`, `project_graph_hybrid_retrieval_fallback_present` and `project_graph_hybrid_retrieval_no_canonical_mutation_present`. Batch 27 is `approval_required`, staged evidence only and not source of truth: Precision/MRR improves or fallback remains active, results are source-backed, bounded and explainable, fallback remains `semantic_retrieval_or_graph_only`, `provider_call_allowed: false`, `external_call_performed: false`, No live provider calls, no provider calls, no live external model/API calls, no canonical graph mutation, and git staging/commit/push/PR remains explicit-only.

Task 26 Batch 28 `T10-LIVE-M15..M16` implements Live LLM Proposal Adapter And Safety Eval through `project_graph_llm_proposal_provider.py` (`llm_proposal_provider.py` artifact contract) and `llm-proposal-eval.json`. It records `project_graph_live_llm_proposal_provider_gate`, `project_graph_live_llm_proposal_provider_gate_present`, `project_graph_live_llm_proposal_governance_prerequisite_present`, `project_graph_live_llm_proposal_prompt_schema_present`, `project_graph_live_llm_proposal_redaction_cache_budget_present`, `project_graph_live_llm_proposal_safety_eval_present`, `project_graph_live_llm_proposal_threshold_fallback_present`, `project_graph_live_llm_proposal_incident_path_present`, `project_graph_live_llm_proposal_no_live_calls_present` and `project_graph_live_llm_proposal_no_canonical_mutation_present`. Batch 28 is `approval_required`, staged evidence only and not source of truth: provider `external_llm`, surfaces `external_llm_proposal_adapter` and `llm_proposal_safety_eval`, approval boundary `batch28_live_llm_proposal_adapter_and_safety_eval`, output format `structured_json`, label `unsupported_claim`, proposal-only, never canonical fact, hallucination, privacy, grounding and stale-context tests, unsafe evidence routes to `incident_blocked` and AI incident workflow, fallback remains `local_llm_proposals_or_semantic_retrieval_or_graph_only`, `provider_call_allowed: false`, `external_call_performed: false`, No live provider calls, no provider calls, no live external model/API calls, no canonical graph mutation, and git staging/commit/push/PR remains explicit-only.

Task 26 Batch 29 `T10-LIVE-M17..M18` implements Human Review Ledger And Proposal Diff Preview through `project_graph_review_ledger.py` with `graph-review-ledger.json` and `proposal-diff.json` artifact contracts. It stages `project_graph_human_review_ledger` and `project_graph_proposal_diff_preview` under approval boundary `batch29_human_review_ledger_and_proposal_diff_preview`, with surfaces `human_review_ledger` and `proposal_diff_preview`. Batch 29 is `approval_required`, staged evidence only and not source of truth: decisions are `accepted`, `rejected` or `accepted_gap`; No accepted proposal without owner decision; Accept, reject or accepted_gap decisions with evidence refs; Human can inspect before mutation; proposal-only until Batch 30 dry-run mutation; `provider_call_allowed: false`, `external_call_performed: false`, no provider calls, no live external model/API calls, no canonical graph mutation, and git staging/commit/push/PR remains explicit-only.

Task 26 Batch 30 `T10-LIVE-M19..M22` implements Canonical Graph Mutation, Journal And Rollback Engine through `project_graph_canonical_mutation.py`, covering the planned `canonical_graph_mutation.py` and `graph_rollback.py` surfaces with `mutation_plan.json`, `graph-mutation-journal.jsonl`, a staged mutated graph copy and rollback proof. It stages `project_graph_canonical_mutation_plan`, `project_graph_mutation_journal` and `project_graph_rollback_proof` under approval boundary `batch30_canonical_graph_mutation_journal_and_rollback`, with surfaces `canonical_mutation_dry_run`, `mutation_journal`, `accepted_mutation_apply` and `rollback_engine`. Batch 30 is `approval_required`, staged evidence only and not source of truth: No mutation without dry-run plan; Every mutation has rollback patch; Only accepted proposals mutate graph; Rollback restores previous graph digest; accepted_gap remains non-mutating; stage-root generated graph copy only; `provider_call_allowed: false`, `external_call_performed: false`, no provider calls, no live external model/API calls, and git staging/commit/push/PR remains explicit-only.

Task 26 Batch 31 `T10-LIVE-M23..M26` implements Audit Logging, Security/Privacy Tests, Observability And Agent/Skill Routing through `project_graph_live_audit.py`, covering `audit-log.jsonl`, `security-privacy.json`, `runtime-observability.json` and `agent-skill-handoff.json` artifact contracts. It stages `project_graph_live_audit_log`, `project_graph_live_security_privacy_tests`, `project_graph_runtime_observability` and `project_graph_agent_skill_handoff_routing` under approval boundary `batch31_audit_security_observability_agent_skill_routing`, with surfaces `audit_logging`, `security_privacy_tests`, `runtime_observability` and `agent_skill_handoff_routing`. Batch 31 is `approval_required`, staged evidence only and not source of truth: every live/provider/mutation action emits a redacted append-only audit event; unsafe secret/path/raw-source/prompt-injection cases are blocked; runtime health, latency, provider errors, budget usage and degraded graph-only mode are visible; agent/skill handoffs require ownership, verification evidence, fresh context and stop conditions; `provider_call_allowed: false`, `external_call_performed: false`, no live server, no provider calls, no live external model/API calls, no canonical graph mutation, and git staging/commit/push/PR remains explicit-only.

## Task 22 operator contract

Task 22 operator contract различает base workspace audit profile и Track 9 methodology audit complexity. Первый слой читает stack, files, control-plane state and route inputs; второй слой классифицирует methodology risk, maturity, recommendations and owner questions. `--intent-hint` может помочь routing, но не переопределяет source policy, approvals, sandbox, write guards or external-action boundaries.

Текущие machine-readable surfaces: renderer JSON includes `renderer_file_count`, stage manifest and status fields; runtime JSON includes `codex_runner_result`, `methodology_packet`, `finish_options`, compact first-response fields and schema v1 additive compatibility; audit/report tooling includes `run_methodology_audit.py`; behavioral evidence includes `run_transcript_eval.py` and fixture eval checks. Docs should describe implemented commands and fields, not planned features.
Additional sources: [Codex MCP](https://developers.openai.com/codex/mcp), [Context7 MCP clients](https://context7.com/docs/resources/all-clients).  
Источники: [Codex plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://developers.openai.com/codex/skills), [Subagents](https://developers.openai.com/codex/subagents), [Codex hooks](https://developers.openai.com/codex/hooks), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex automations](https://developers.openai.com/codex/app/automations), [Product-Agent OS plugin](index.md).

## Package layout

Реализация находится в `plugins/product-agent-os/`.

```text
plugins/product-agent-os/
  .codex-plugin/plugin.json
  skills/
  scripts/
  assets/
    templates/
    fixtures/
```

Официальный contract Codex plugin требует `.codex-plugin/plugin.json`; остальные bundled components лежат в plugin root. В текущем package manifest указывает на bundled `skills` и `.mcp.json`, а пользовательская логика lives in local scripts and templates.

## Bundled MCP

`.mcp.json` registers Context7 as a bundled MCP server:

```json
{
  "context7": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp"],
    "startup_timeout_sec": 20
  }
}
```

This keeps the plugin package free of API keys and follows the Codex MCP Context7 example. Projects that need higher Context7 limits or private sources should provide credentials through their own trusted Codex MCP configuration, not through this repository.

## Packaged skills

| Skill | Назначение |
| --- | --- |
| `project-lifecycle-orchestrator` | Определяет lifecycle state и следующий bounded step |
| `workspace-discovery-auditor` | Делает read-only audit workspace |
| `requirements-author` | Готовит requirements packet |
| `implementation-planner` | Готовит executable plan |
| `agent-team-designer` | Проектирует project-scoped roles and handoffs |
| `test-eval-designer` | Определяет deterministic checks and quality gates |
| `risk-reviewer` | Проверяет diff, risks, source fidelity and missing tests |
| `pr-release-operator` | Готовит PR or release packet |
| `learning-loop-maintainer` | Переносит устойчивые lessons в durable artifacts |
| `automation-promoter` | Делает candidate-only automation readiness analysis |

Каждый skill задает trigger, inputs, outputs, failure modes and final response contract. Source-sensitive skills не должны превращать community claims в project rules без verification status.

## Generated infrastructure

Renderer может создать или предложить:

- `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- `.codex/config.toml`;
- `.codex/agents/*.toml`;
- `.codex/hooks/*`;
- `.codex/workflows/*.md`;
- `.codex/artifact-templates/*.md`;
- `.codex/evals/*.json`;
- `.codex/pr/*`;
- `.codex/automation-candidates/automation-candidate.md`.

В Track 6 workflow inventory расширен двумя методическими packets:

- `.codex/workflows/development-standards.md` - product hypothesis, architecture boundary, test-first/eval-first path, bounded agentic implementation, review and measurement.
- `.codex/workflows/documentation-system.md` - docs-as-code routing for architecture docs, API contracts, UI component docs, database docs, code reference and release docs.

Track 7 добавляет concrete artifact templates, чтобы методологии не оставались только checklist:

- `.codex/artifact-templates/adr.md`;
- `.codex/artifact-templates/architecture-overview.md`;
- `.codex/artifact-templates/domain-modeling.md`;
- `.codex/artifact-templates/metric-spec.md`;
- `.codex/artifact-templates/api-contract-review.md`;
- `.codex/artifact-templates/component-card.md`;
- `.codex/artifact-templates/database-dictionary.md`;
- `.codex/artifact-templates/docs-tooling-decision.md`.

Track 8 добавляет scenario routing and workflow coverage:

| Status | Generated or routed surface |
| --- | --- |
| `done` | `.codex/workflows/first-run-intake.md`, `.codex/workflows/bug-rescue.md`, `.codex/workflows/greenfield-idea-to-plan.md`, `.codex/workflows/complex-system-acceleration.md`, `.codex/workflows/pr-review-readiness.md`, `.codex/workflows/legacy-onboarding.md`, `.codex/workflows/api-migration.md`, `.codex/workflows/ai-eval-regression.md`, `.codex/workflows/native-mobile-feature.md`, `.codex/workflows/desktop-local-first.md`, `.codex/workflows/data-migration.md`, `.codex/workflows/security-sensitive-change.md`, `.codex/workflows/ci-stabilization.md`, `.codex/workflows/release-packaging.md`. |
| `done` | `.codex/artifact-templates/bug-rescue-report.md`, `greenfield-idea-brief.md`, `integration-catalog.md`, `pr-risk-review.md`, `onboarding-map.md`, `migration-plan.md`, `ai-eval-spec.md`, `security-risk-review.md`, `ci-stabilization-report.md`, `release-readiness.md`. |
| `done methodology gate` | `acceptance-scenarios.md`, `domain-modeling.md`, `architecture-overview.md`, `component-card.md`, `metric-spec.md`, `release-packet.md`, `docs-tooling-decision.md`, `plan-quality-check.md`, `agent-task-packet.md`, `project-readiness.json` and `behavioral-workflows.json` cover ATDD/BDD traceability, conditional DDD domain modeling, bounded-context-to-architecture traceability, ubiquitous language traceability, optional `fsd_structure`, metric hardening, evidence-before-completion, docs tooling selection, conditional readiness statuses, no-placeholder planning, two-stage review and fresh-context handoff. |

First-run intake is visible in the runtime route packet, lifecycle skills and behavioral evals for empty, broken, existing control-plane and complex system starts. Release packaging is visible in `usage_mode`, fixture evals, renderer output, lifecycle skills, and the packaged `release-packaging.md` / `release-readiness.md` templates. Dedicated operator docs now live in [scenarios](scenarios.md), [behavioral evals](behavioral-evals.md) and [Codex compatibility](codex-compatibility.md).

Generation is staged-first. Existing user-authored files are preserved outside managed sections:

```markdown
<!-- product-agent-os:start section-id -->
...
<!-- product-agent-os:end section-id -->
```

Если existing file не имеет managed markers, plugin stages a companion proposal instead of overwriting it.

## Local commands

Read-only infrastructure plan:

```powershell
python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --dry-run
```

Stage generated artifacts outside the target workspace:

```powershell
python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --stage <stage-dir>
```

Plan merge from staged artifacts:

```powershell
python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --plan
```

Apply requires an approval record:

```powershell
python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --apply --approval-file <approval.json>
```

Run Codex-only runtime contract mode:

```powershell
python plugins\product-agent-os\scripts\run_codex_runtime_runner.py <workspace> --contract
```

Allow route recommendation to a Codex subagent when the current Codex thread explicitly permits it:

```powershell
python plugins\product-agent-os\scripts\run_codex_runtime_runner.py <workspace> --contract --allow-subagents
```

Run plugin fixture evals:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

## Task 24 self-verification metrics loop

Task 24 adds a local, read-only `agent_skill_metrics_loop` contract for reviewing agents, skills, prompt/policy packs, router/tool policies and harness versions after real work leaves evidence. The loop collects a target registry, validates trace intake, checks dataset quality, records local grader summaries, blocks uncalibrated grader/judge calibration, builds cadence recommendation values `L0`, `L1`, `L2` and `L3`, and writes staged scorecard ledger or report packets.

Main files and commands:

- `plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics.py` - source priority, target registry, trace intake, dataset quality, grader/judge calibration, metrics, scorecards, cadence recommendation and run-record contracts.
- `plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics_report.py` - redacted offline report rendering for `agent-skill-evaluation-report.html`.
- `plugins/product-agent-os/scripts/render_agent_skill_metrics_report.py` - dry-run or stage-only report CLI.
- `.codex/artifact-templates/agent-skill-scorecard-ledger.md`, `.codex/artifact-templates/agent-skill-metrics-daily.md`, `.codex/artifact-templates/agent-skill-metrics-weekly.md` and `.codex/artifact-templates/agent-skill-update-candidate.md` - generated review artifacts.

The source-of-truth policy remains explicit: control-plane artifacts, run records, trace/eval packets and accepted gaps can support metrics; generated dashboard/report HTML, memory, raw chat logs and unsupported community claims cannot. A report is not source of truth. All metrics outputs are staged evidence only, not proof that a real project is semantically ready.

Approval boundary: Product-Agent OS performs no live eval/model/API calls, creates no active schedules, makes no external writes, applies no modernization candidates, and allows no self-applied updates. A modernization candidate needs owner review, rollback target and explicit approval state before any target workspace, skill, prompt/policy pack, router/tool policy or harness configuration changes.

## Task 25 project code graph and cockpit

Task 25 Batch 13, Batch 14, Batch 15 and Batch 16 add a local read-only graph foundation and generated cockpit for project navigation. The scanner inventories files, emits stable file-level graph nodes and `contains` edges, adds Python AST package/module/class/function/method overlays, adds conservative import/call/test edges, builds structured overlays for parseable Markdown, OpenAPI/Swagger, AsyncAPI, DBML, SQL, JSON, YAML, Mermaid and PlantUML inputs, validates a controlled ontology, records manifest freshness/provenance, stores observation records with relative paths/spans/fingerprints and supports temporal edge invalidation/supersession helpers. Query mode reads existing JSON/JSONL graph artifacts to produce bounded `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `changed_since`, `why_changed`, `read_order`, `hotspots`, `node`, `status` and `search` packets. It excludes raw source bodies by default and redacts local absolute paths or secret-like values from returned packets.

Main files and commands:

- `plugins/product-agent-os/scripts/product_agent_os/project_code_graph.py` - graph JSON/JSONL packet builder.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_adapters.py` - Python AST scanner and unsupported-language adapter boundary.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_chunking.py` - structured docs/contracts/schema/diagram overlays, partitions, aliases and readiness summaries.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_manifest.py` - file fingerprints, freshness and provenance.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_observations.py` - observation records and edge delta lineage.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_ontology.py` - controlled ontology and graph schema validation.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_queries.py` - bounded graph-only query packets.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_analysis.py` - source-free graph analysis report.
- `plugins/product-agent-os/scripts/product_agent_os/project_cockpit_model.py` - eight-page cockpit information architecture and Code Flow section model.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_visual_model.py` - Graphology-compatible static projection, large-graph bounds, selected evidence and local Graphology/Sigma vendor boundary.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_renderer.py` - offline stage-only cockpit HTML/JSON renderer with no external assets.
- `plugins/product-agent-os/scripts/scan_project_code_graph.py` - dry-run, stage-only scanner and graph query CLI.
- `plugins/product-agent-os/assets/templates/project-graph/` - local cockpit, graph, Code Flow and CSS templates.

```powershell
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --dry-run
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --stage C:\tmp\product-agent-os-graph-stage
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --query neighbors --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --node-id function:app.main.main
```

Stage mode must use an output directory outside the target workspace. Query mode reads an existing graph artifact and does not scan source text. Existing graph artifacts in the target workspace are not modified. Batch 15 remains conservative: dynamic dispatch, framework wiring, runtime routes and semantic/rationale extraction are not verified dependency proof. Runtime/status summaries and graph analysis reports are orientation evidence only.

Batch 16 cockpit rendering uses `render_project_graph_cockpit_plan()` for dry-run plans and `stage_project_graph_cockpit()` for explicit stage directories outside the target workspace. It stages `.codex/product-agent-os/project-cockpit.html` and `.codex/product-agent-os/project-cockpit.json`. The staged HTML exposes exactly eight top-level pages, keeps Code Flow inside `Code Intelligence`, embeds safe JSON, uses static local CSS/JS, has filter/reset/copy/select commands, selected-node evidence, fallback static table, mobile layout and generated-view-only wording. Graphology and Sigma are recorded as local Graphology/Sigma vendor-only capabilities; no vendored assets are currently bundled, so the verified renderer uses the static fallback path with Graphology-compatible static projection data.

Task 25 Batch 17 adds fixture structural fields, a search-quality eval loop and future backend and semantic gates. Fixture eval records graph contract, no external assets, redaction, scale bounds, generated-view-only, eight-page cockpit structure, section preservation, cockpit generated-view boundary, `project_graph_search_quality_present` and `project_graph_future_backend_semantic_gates_present`. Search-quality evals are local and deterministic: they record symbol recall, top-k/MRR, trace success or failure labels, affected-test precision, edge density and explicit thresholds. Batch 19, Batch 20 and Batch 21 later implement the approved static index, local backend gate and local deterministic semantic retrieval gate; live database/server, live external model/API embedding or cross-encoder providers, LLM semantic extraction and rationale/comment extraction stay outside the approved surface unless explicit approval defines redaction, cache, token budget, eval threshold and rollback path.

Task 25 Batch 18 `T10-CG-V2-M31..M32` is the focused/full verification closure for the same baseline. Batch 18 evidence records graph/cockpit/search, status/runtime and fixture/lifecycle/docs focused suites, then full unittest ran 664 tests with `OK`; fixture eval exited `0` for 91 fixture directories; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; strict MkDocs and diff hygiene passed. The explicit-only git boundary remains in force. Batch 19, Batch 20, Batch 21, Batch 22 and Batch 23 are approved implemented extensions; Batch 22 is limited to staged proposals, not canonical graph facts, and Batch 23 is limited to generated extension closure evidence, rollback/data deletion proof and graph-only fallback. Live production server, live external model/API extraction and canonical graph mutation still require separate explicit approval.

## Codex installation boundary

Для Codex installation plugin должен быть доступен через plugin marketplace or curated plugin list, а package root должен содержать `.codex-plugin/plugin.json`. В этом репозитории package уже подготовлен локально under `plugins/product-agent-os/`; подключение к конкретной Codex App installation остается отдельным environment step and should follow current official Codex plugin docs.

Этот project intentionally keeps runtime code Codex-only:

- no separate OpenAI API key;
- no standalone Agents SDK application;
- no background MCP server started by plugin scripts; Context7 is declared as a bundled Codex MCP server and starts only when Codex enables that MCP configuration;
- no active automation created from templates;
- no plugin-root hook activation without explicit approval.

## Guardrails

| Guardrail | Enforcement |
| --- | --- |
| Source policy | `validate_source_policy.py` blocks unsupported OpenAI/Codex claims and secret-like content |
| Automation policy | `validate_automation_candidate.py` requires manual success evidence, owner, cadence, verification, rollback and approval |
| Staged manifest | stage paths must stay inside stage root and target paths inside workspace |
| Approval record | approved writes require explicit decisions and matching plan digest |
| Rollback | apply can produce rollback manifest for later rollback |
| Runtime runner | validates lifecycle route, approval boundary, source policy, handoff shape and redaction |
| Transcript/session eval runner | `run_transcript_eval.py` replays synthetic or redacted sessions against `behavioral-workflows.json` without external model calls |
| Redaction | secret assignments, local absolute paths and private data markers are redacted from runner result |
| Engineering standards | templates require product metrics, architecture boundary, test/eval gates, docs impact and measurement notes |
| Methodology discovery | workspace audit reports architecture docs, ADR, domain model, architecture context maps, optional `fsd_structure`, OpenAPI, AsyncAPI, Storybook, DB docs, CODEOWNERS, CI, evals and metrics signals |
| Scenario routing | `usage_mode` distinguishes completed workflows, partial methodology gates, and base modes; it returns minimum artifacts plus evidence gaps |

## Verification commands for this repo

After docs or nav changes:

```powershell
python tools\check_docs.py
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; python -m mkdocs build --strict
```

After plugin scripts, templates, fixtures or tests change:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
```
