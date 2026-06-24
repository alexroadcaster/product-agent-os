# Product-Agent OS artifact contracts

Source status: `official + experiment`

Эта страница перечисляет основные generated artifacts Product-Agent OS для modernization loop, project code graph, live/runtime governance и approval-bound handoff. Это не JSON Schema spec, а operator-facing contract map: что создается, зачем нужно, где проходит source-of-truth boundary и какие approval gates действуют.

## Contract Boundary

Сгенерированные артефакты являются только staged evidence. Они не являются источником истины, пока более поздний owner-approved process явно не продвинет факт обратно в checked-in source documentation или другой canonical artifact.

Каноническими источниками остаются:

- project source files и checked-in contracts;
- `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- source registry entries с текущий verification status;
- command evidence из текущий run;
- owner decisions и accepted gaps с residual risk.

Artifacts должен не contain secrets, credentials, raw private chat logs, private customer data, unredacted PII, raw source bodies где redacted packet является required, или absolute local paths.

## Project Code Graph Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph.json` | `project_code_graph.py`, `scan_project_code_graph.py --stage` | Main graph packet с metadata, nodes, edges, observations, freshness и provenance. | Orientation evidence only; source files остаются canonical. |
| `.codex/product-agent-os/project-code-graph.jsonl` | `scan_project_code_graph.py --stage` | Bounded JSONL form для agent consumption. | Нет raw source body claim; используйте source reads до implementation claims. |
| `.codex/product-agent-os/project-cockpit.html` | `project_graph_renderer.py` | Offline generated cockpit view. | Generated view only; visual completeness не доказывает source correctness. |
| `.codex/product-agent-os/project-cockpit.json` | `project_graph_renderer.py` | Structured cockpit model, pages и projection data. | Только review surface. |
| `.codex/product-agent-os/project-code-graph-search-index.json` | `project_graph_index.py`, `--build-index` | Offline static search index с cache/fingerprint checks. | Generated cache; delete для rollback. |
| `.codex/product-agent-os/project-code-graph-backend.json` | `project_graph_backend.py`, `--build-backend` | Disabled-by-default local query backend file-store. | Не active production server; graph-only fallback должен оставаться включенным. |
| `.codex/product-agent-os/project-code-graph-semantic-index.json` | `project_graph_semantic.py`, `--build-semantic-index` | Local deterministic semantic retrieval cache. | Semantic hits являются `present_unverified`; нет canonical edge rewrites. |
| `.codex/product-agent-os/project-code-graph-llm-proposals.json` | `project_graph_llm_extraction.py`, `--build-llm-proposals` | Local deterministic semantic node/edge и rationale/comment proposals. | Proposal-only; never canonical graph fact. |
| `.codex/product-agent-os/project-code-graph-extension-closure.json` | `project_graph_extension_closure.py`, `--verify-extensions` | Extension verification, rollback/data deletion proof и graph-only fallback report. | Closure evidence only. |

## Live Governance And Runtime Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-live-governance.json` | `project_graph_live_governance.py`, `--validate-live-governance` | Approval, data classification, redaction, credential, cache и budget packet. | Нет live calls; проверяется только gate. |
| `.codex/product-agent-os/project-code-graph-live-cache.json` | `project_graph_live_governance.py` | Cache policy/deletion metadata. | Cache является generated evidence, не source truth. |
| `.codex/product-agent-os/project-code-graph-live-runtime.json` | `project_graph_live_runtime.py`, `--validate-live-runtime` | Local read-only runtime contract. | `disabled_by_default_not_started`; нет launch в docs slices. |
| `.codex/product-agent-os/project-code-graph-live-runtime.pid` | `project_graph_live_runtime.py` | Runtime lifecycle placeholder/evidence path. | Имеет смысл только после approved runtime execution. |
| `.codex/product-agent-os/project-code-graph-live-runtime.log` | `project_graph_live_runtime.py` | Runtime log path/evidence path. | Must быть redacted и local-only. |

## Provider And Retrieval Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-embedding-provider.json` | `project_graph_embedding_provider.py`, `--validate-embedding-provider` | Embedding provider gate и eval baseline. | Provider call остается blocked пока separately approved. |
| `.codex/product-agent-os/project-code-graph-embedding-provider-cache.json` | `project_graph_embedding_provider.py` | Provider cache metadata. | Must preserve redaction/cache/budget policy. |
| `.codex/product-agent-os/project-code-graph-reranker-provider.json` | `project_graph_reranker_provider.py`, `--validate-reranker-provider` | Reranker provider gate. | Нет external reranker call через default. |
| `.codex/product-agent-os/project-code-graph-reranker-provider-cache.json` | `project_graph_reranker_provider.py` | Reranker cache metadata. | Generated cache only. |
| `.codex/product-agent-os/project-code-graph-hybrid-retrieval.json` | `project_graph_hybrid_retrieval.py`, `--build-hybrid-retrieval` | Explainable fusion из graph/static/semantic/reranker signals. | Нет canonical mutation; fallback остается available. |
| `.codex/product-agent-os/project-code-graph-llm-proposal-provider.json` | `project_graph_llm_proposal_provider.py`, `--validate-llm-proposal-provider` | External LLM proposal provider gate. | Proposal-only; provider output является не canonical. |
| `.codex/product-agent-os/project-code-graph-llm-proposal-eval.json` | `project_graph_llm_proposal_provider.py` | Safety/grounding eval packet для proposal provider. | Unsafe output routes к incident/fallback. |

## Review And Mutation Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-review-ledger.json` | `project_graph_review_ledger.py`, `--build-review-ledger` | Human review decisions: `accepted`, `rejected`, `accepted_gap`. | Нет accepted proposal без owner decision и evidence refs. |
| `.codex/product-agent-os/project-code-graph-proposal-diff.json` | `project_graph_review_ledger.py` | Proposal diff preview. | Preview только пока mutation dry-run. |
| `.codex/product-agent-os/project-code-graph-mutation-plan.json` | `project_graph_canonical_mutation.py`, `--build-canonical-mutation` | Mutation dry-run plan. | Staged plan only; не source mutation через itself. |
| `.codex/product-agent-os/project-code-graph-mutation-journal.jsonl` | `project_graph_canonical_mutation.py` | Append-only mutation journal. | Must cite accepted item и rollback path. |
| `.codex/product-agent-os/project-code-graph-canonical-mutated.json` | `project_graph_canonical_mutation.py` | Staged mutated graph copy. | Generated copy only; canonical graph/source не silently changed. |
| `.codex/product-agent-os/project-code-graph-rollback-proof.json` | `project_graph_canonical_mutation.py` | Rollback proof и digest comparison. | Required до mutation pilot completion claims. |

## Audit, Security And Observability Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-live-audit-log.jsonl` | `project_graph_live_audit.py`, `--build-live-audit` | Redacted append-only audit events. | Нет secrets, raw source или private data. |
| `.codex/product-agent-os/project-code-graph-live-security-privacy.json` | `project_graph_live_audit.py` | Security/privacy negative cases и findings. | Evidence packet, не full security certification. |
| `.codex/product-agent-os/project-code-graph-live-observability.json` | `project_graph_live_audit.py` | Runtime health, latency, provider error и degraded-mode visibility. | Generated observability evidence. |
| `.codex/product-agent-os/project-code-graph-agent-skill-handoff.json` | `project_graph_live_audit.py` | Agent/skill ownership, fresh context, verification и stop-condition routing. | Handoff guidance only; agents still нужны explicit work context. |

## Real Testing And Runtime QA Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-real-testing-readiness.json` | `project_graph_real_testing.py`, `--build-real-testing-readiness` | Readiness и no-hidden-gates packet. | Real testing остается blocked без target/data approval. |
| `.codex/product-agent-os/project-code-graph-real-testing-targets.json` | `project_graph_real_testing.py` | Owner-approved target/data-policy candidates. | Target consent evidence only. |
| `.codex/product-agent-os/project-code-graph-pilot-harness.json` | `project_graph_real_testing.py` | Dry-run pilot harness. | Stage-only; нет live execution. |
| `.codex/product-agent-os/project-code-graph-codex-surface-smoke.json` | `project_graph_real_testing.py` | Codex App, CLI и IDE extension smoke planning/evidence. | Does не imply live browser automation. |
| `.codex/product-agent-os/project-code-graph-real-testing-pilot-matrix.json` | `project_graph_real_testing.py` | Use-case pilot matrix. | Planning/readiness evidence. |
| `.codex/product-agent-os/project-code-graph-runtime-browser-qa.json` | `project_graph_runtime_qa.py`, `--build-runtime-qa` | Browser QA expectations/evidence. | Нет unapproved browser automation; labels и source boundary required. |
| `.codex/product-agent-os/project-code-graph-performance-budget.json` | `project_graph_runtime_qa.py` | Performance thresholds и fallback/accepted-gap handling. | Budget breach disables live layer или records owner gap. |
| `.codex/product-agent-os/project-code-graph-stabilization-ledger.json` | `project_graph_runtime_qa.py` | Stabilization defects и P0/P1 closure status. | Нет open P0/P1 до closure. |

## Agent/Skill Metrics Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/eval-reports/agent-skill-evaluation-report.html` | `agent_skill_metrics_report.py` | Offline report view для `agent_skill_metrics_loop`. | Report является не proof; candidate-only. |
| `.codex/artifact-templates/agent-skill-scorecard-ledger.md` | Template registry | Append-only scorecard ledger template. | Must cite текущий evidence window. |
| `.codex/artifact-templates/agent-skill-daily-eval-report.md` | Template registry | Daily triage packet. | Нет active schedule через default. |
| `.codex/artifact-templates/agent-skill-weekly-verification.md` | Template registry | Weekly owner-review packet. | Requires rollback/holdout/flake/cost evidence или accepted gaps. |
| `.codex/artifact-templates/agent-skill-update-candidate.md` | Template registry | Modernization candidate packet. | Нет self-applied updates. |

## First-run analysis artifact

First-run analysis artifact - это локальный generated orientation pack для первого анализа проекта. Он помогает оператору увидеть inventory, runtime route, control-plane state, graph summary, risks и safe next action, но остается `orientation_only_not_proof`.

Эта карта описывает фактические artifact families и view-model contracts, найденные в `analysis_artifact_renderer.py` и staged B41/B42 evidence. Это не полная JSON Schema: в репозитории есть contract fields, tests и staged examples, но нет отдельного исчерпывающего JSON Schema validation для всех вложенных first-run surfaces.

| Артефакт / schema | Producer | Schema / status | Source input | Renderer / consumer | Redaction / freshness | Stable fields | Experimental fields | Forbidden claims |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `.codex/product-agent-os/analysis/first-run-analysis-packet.json` | `run_first_project_analysis.py --write`, `first_run_analysis.py` | Пакет first-run; метка schema живет в выводе пакета, а не в полной JSON Schema. | Workspace inventory, route snapshot, source-policy summary, graph summary при наличии, evidence status и safe next action. | `analysis_artifact_renderer.py`; оператор читает пакет через manifest и HTML cockpit. | Нужна очистка от secrets, raw private logs и raw source bodies; свежесть зависит от команды, создавшей пакет. | `target`, `section_summaries`, `source_artifacts`, `safe_next_action`, `evidence_status`, `unsupported_claims`. | Optional graph depth, methodology и route summaries могут отсутствовать. | Не доказывает readiness, release, target mutation, runtime/browser/provider proof или source truth. |
| `.codex/product-agent-os/analysis/analysis-manifest.json` | `analysis_artifact_renderer.py` | `first_run_analysis_manifest_v1`; digest manifest является generated evidence. | First-run packet, page digests, source digests, previous manifest/baseline при наличии. | Artifact gallery, cleanup review, comparison packets и operator handoff. | Содержит `redaction_report`, `source_policy_gate`, `baseline_comparison` и `cleanup_guidance`; устаревший digest или пустой baseline не доказывает свежесть. | `schema_version`, `renderer_version`, `pages`, `page_digests`, `source_digests`, `manifest_digest`, `redaction_report`, `source_policy_gate`. | `graph_depth_summary`, `primary_cockpit`, `cockpit_contract` и route summaries развиваются вместе с renderer slices. | Не доказывает generated-site freshness, publication readiness или semantic review source files. |
| `.codex/product-agent-os/analysis/index.html` | `analysis_artifact_renderer.py` | `first_run_cockpit_artifact_v1`; primary self-contained cockpit. | Manifest model, first-run packet, graph/code summaries, contract surfaces и design contract. | Читатель HTML cockpit; optional local JS tabs/search/filtering внутри generated file. | `generated_view_policy: orientation_only_not_proof`; source files и current command evidence сильнее. | `schema_version`, `path`, `page_count`, `generated_view_policy`, `source_truth_policy`, `contract`, `overview`, `source_artifacts`, `baseline_comparison`, `cleanup_guidance`. | `navigation_search`, `progressive_diagnostics`, `visual_accessibility_acceptance`, graph runtime/detail layers. | Не доказывает WebGL/Cosmos.gl runtime proof, browser screenshot proof, WCAG certification, target apply safety или release readiness. |
| `first_run_cockpit_artifact_contract_v1` | `build_first_run_cockpit_artifact_contract()` | Карта контракта primary cockpit; не является полной JSON Schema. | Renderer constants и page IDs. | Manifest `cockpit_contract`; docs/tests проверяют intent renderer. | Фиксирует `generated_view_policy`, fallback states и unsupported claims. | `artifact_schema_version`, `primary_artifact`, `artifact_mode`, `primary_pages`, `graph_layers`, `selected_graph_renderer`, `large_graph_policy`, `unsupported_claims`. | Renderer policy details, vendoring requirements и large-graph thresholds меняются только после evidence. | Не доказывает, что Cosmos.gl выполнялся, зависимости установлены или full graph rendering безопасен для каждого проекта. |
| `architecture_intelligence_design_contract_v1` | `_architecture_intelligence_design_contract()` | Design contract для architecture cockpit. | Renderer design choices и hierarchy cockpit. | `index.html` hero, tabs, sections и visual hierarchy. | Generated-view boundary явный; design contract не является browser proof. | `artifact_family`, `generated_view_boundary`, `first_viewport`, `navigation_modes`, `section_hierarchy`, `component_grammar`. | Component mapping и future runtime migration экспериментальны до browser/runtime evidence. | Не доказывает public-ready статус, визуальное browser approval или замену architecture source docs. |
| `first_run_schema_contract_surface_v1` | `_first_run_schema_contract_surface()` | Инвентарь contracts. | Найденные schema/openapi/config paths и digests, без raw bodies. | Страница Contracts в cockpit. | `source_boundary: path_and_digest_inventory_only`; без runtime introspection и migration execution. | `status`, `source_boundary`, `runtime_introspection_performed`, `migration_execution_performed`, category counts. | Detected categories и aliases остаются эвристикой до owner/test evidence. | Не доказывает API compatibility, migration safety или schema completeness. |
| `first_run_graph_file_code_surface_v1` | `_first_run_graph_code_surface()` | Graph/code поверхность для навигации. | Source-file graph и code graph summaries. | Страницы Project Map и Code Intelligence в cockpit. | Runtime boundary остается static fallback без approved browser/WebGL evidence; source reads обязательны. | `status`, `renderer`, `runtime_boundary`, `selected_node_panel`, `source_read_required`. | Cosmos.gl adapter payloads, selected-neighborhood UX и large-graph policy развиваются с renderer tests. | Не доказывает source-read semantic completeness, affected-test proof или target mutation safety. |
| `first_run_guided_tour_surface_v1` | `_first_run_guided_tour_surface()` | Guided read-order surface. | Page order и safe next-action guidance. | Cockpit navigation и recommendations. | User completion не отслеживается; evidence по-прежнему берется из source и commands. | `status`, `interaction_mode`, `completion_tracking_enabled`, `steps`. | Tour steps и labels могут меняться вместе с page IA. | Не доказывает, что человек завершил review или approved next action. |
| `first_run_evidence_decision_layer_v1` / `first_run_evidence_risk_hierarchy_v1` | Renderer evidence helpers. | Evidence/risk summary surfaces. | Packet evidence status, unsupported claims, blockers и section risk. | Страницы Operations & Risk и Proposal Ledger в cockpit. | Держит supported и unsupported claims видимыми; generated layer сам не является proof. | `generated_view_policy`, `supported_claims`, `unsupported_claims`, `section_blockers`, `target_apply_allowed`. | Risk groupings и labels могут меняться с completion-skeptic docs. | Нет completion, fixed, verified, ready или safe-to-apply claim без current evidence или owner gap. |
| `first_run_artifact_cleanup_guidance_v1` | `_cleanup_guidance()` | Только cleanup preview. | Список generated pages из renderer constants. | Manifest, HTML cleanup section и handoff. | `approval_required: true`; `deletion_performed: false`; перечислены только generated files. | `generated_files`, `cleanup_command_preview`, `rollback_policy`, `forbidden_scope`. | File list меняется при изменении first-run pages. | Нет automatic cleanup, destructive deletion или cleanup вне generated analysis artifacts. |
| `first_run_redaction_report_v1` | `_redaction_report()` | Redaction guardrail packet. | Render payloads и generated manifest model. | Manifest gate перед записью artifact. | Блокирует local absolute paths, raw source fields и secret-like values. | `status`, `blocked_categories`, `policy`, `accepted_false_positives`. | Pattern coverage не является full DLP/security scan. | Нет security certification, privacy compliance proof или гарантии нахождения всего sensitive context. |
| `batch41_s9_m57_neural_flow_comparison_v1` | B41/S9 comparison artifact. | Read-only rerun comparison packet. | Старые/новые staged first-run outputs и digest/key/marker checks. | Maintainer review и docs evidence. | Фиксирует отсутствие target mutation, runtime/browser/provider/git/release actions. | `target`, `stages`, `digests`, `view_model_key_delta`, `html_marker_results`, `unsupported_claims_preserved`, `actions_performed`. | Target-specific deltas являются historical evidence и могут устареть после rerun. | Нет general readiness, publication, live runtime, browser proof или target apply safety. |
| `answer-ledger-template.json` | Question protocol / staged first-run packet. | `schema_version: 1`; staged answer ledger template. | Owner questions, target artifact hints, redaction metadata и answer status. | Guided question handoff; позже routing owner answer. | `write_policy: staged_only`; private-data status должен оставаться bounded. | `entries`, `question_id`, `category`, `status`, `target_artifact`, `redaction`, `validation_errors`, `summary`. | Question wording и categories меняются по route. | Нет owner decision, accepted gap или artifact update до фактического ответа и review. |
| `first_run_artifact_scorecard_v1` | `batch39_scorecard.py` | Scorecard удобства оператора. | First-run artifact review inputs, usability criteria и missing-evidence visibility. | Maintainer/reviewer читает как вспомогательную оценку. | Статус: `not release approval`; owner review и real-project evidence остаются сильнее. | Clarity, completeness, actionability, approval boundary, onboarding time, navigation. | Thresholds и вес критериев могут меняться по eval policy. | Не является release approval, production readiness или доказательством полезности для каждого target. |

`source_policy_gate` может разрешать diagnostic artifact, сохраняя apply/promotion выключенными. `redaction_report` обязан фиксировать заблокированные secret-like values, raw source fields и локальные absolute paths до финализации пакета. `cleanup_guidance` является preview-only: удаление файлов, target cleanup и rollback действия требуют отдельного explicit approval.

## Артефакт состояния Self-Learning Loop

| Артефакт | Создатель / потребитель | Роль контракта | Граница |
| --- | --- | --- | --- |
| `.codex/product-agent-os/self-learning-state.json` | Будущий approved state initializer/manual runner; `check_self_learning_due.py --dry-run` читает файл только для проверки. | `self_learning_state_v1`: `installed_at`, `last_analysis_at`, `last_success_at`, `last_failure_at`, `next_due_at`, `cadence_level`, `last_report_id`, `last_metrics_digest`, `approval_state`, `disable_reason`. | Только состояние для due-check; due-check CLI не пишет этот файл, не запускает analysis, не создает active schedule, не импортирует sessions, не вызывает providers, не меняет targets и не включает auto-apply. |

## Doubt verification artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/artifact-templates/doubt-verification-packet.md` | Template registry / `completion-skeptic` | Human-readable `doubt_verification_packet_v1` с claim ledger, requirement ledger, evidence ledger, verdict, accepted gaps и residual risks. | Staged/generated-view boundary; packet организует evidence, но сам не становится source truth. |
| `doubt_verification_packet_v1` JSON/YAML packet | `validate_doubt_verification_packet.py` и `doubt_verification.py` | Contract-checked evidence packet для `pass`, `revise`, `needs_more_context`, `blocked_by_approval` и `accepted_risk`. | Reject pass without evidence, fake command evidence, approval-blocked pass и `accepted_gap` без owner/reason/residual risk/follow-up. |
| `completion_skeptic_recommendation` route field | Codex runtime runner | Additive route recommendation для manual completion-skeptic review. | Только recommendation; она не authorizes tools, providers, browser automation, Agents SDK runner или workspace mutation. |

## System File Hygiene Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| JSON-вывод `validate_system_file_hygiene.py` | `system_file_hygiene.py` | Read-only inventory и findings по поддерживаемым классам системных файлов. | `schedule_status: not_created`; без edits, schedules, hooks и external-write. |
| `.codex/workflows/system-file-hygiene-audit.md` | Template registry | Operator workflow для hybrid periodic, on-change, size и release/automation triggers. | Только recommendation до owner approval на реальный schedule. |
| `.codex/artifact-templates/system-file-hygiene-report.md` | Template registry | Staged report для size, duplication, mojibake/BOM, secret, historical-ledger и ownership findings. | Только review artifact; compaction остается отдельным slice. |
| `.codex/automation-candidates/system-file-hygiene-audit.md` | Template registry | Candidate-only automation packet для будущих scheduled hygiene checks. | Active schedules остаются out of scope до explicit approval и rollback/disable evidence. |

JSON-валидатор `system_file_hygiene_audit` проверяет вложенную форму trigger records, class records, inventory, findings и `summary.status`; malformed packet блокируется до compaction или automation promotion.

Поля JSON для `system_file_hygiene_audit`: `audit_trigger`, `finding_type`, `compaction_decision`, `approval_boundary`, `no_secrets_status` и `active_schedule_markers`. CLI `--trigger` записывает причину запуска без записи в рабочую область. Шаблон `system-file-hygiene-report.md` фиксирует audit trigger, класс системного файла, тип finding, владельца, решение о compaction, active schedule markers, no-secrets status и границу отдельного approved slice.

HTML/JSON status dashboard projection использует только bounded `file_statuses`: relative path, class, owner, state, severity, finding count, `mtime_utc`, `age_days`, `content_digest` и `top_finding`. Даты берутся из filesystem metadata и являются подсказками свежести, а не семантическим доказательством корректности содержимого, source ownership или completion readiness.

## Planned Execution Evidence Files

| Planned artifact | Surface | Status до approval |
| --- | --- | --- |
| `live-server-run-evidence.json` | `approved_local_runtime_launch` | Planned only; требует local runtime approval packet. |
| `browser-automation-smoke.json` | `actual_browser_automation_smoke` | Planned only; требует browser automation approval packet. |
| `provider-call-evidence.json` | `approved_provider_api_pilot` | Planned only; provider call blocked пока approval/redaction/cache/budget/eval threshold exists. |
| `canonical-mutation-run.json` | `approved_canonical_mutation_pilot` | Planned only; требует accepted ledger item, dry-run plan, journal и rollback proof. |
| `git-release-pr-evidence.md` | `explicit_git_release_pr_action` | Planned only; нет git stage/commit/push/PR без explicit пользователь command. |

## Проверка

Artifact verification следует check:

- expected `artifact_kind` и `approval_boundary`;
- stage root confinement и rollback/disable path;
- redaction из secrets, raw source bodies, absolute paths и private data;
- generated-view или staged-evidence label;
- source-boundary label когда screenshots, cockpit, dashboard или runtime QA evidence является present;
- fallback path когда live/provider/runtime layers являются disabled;
- `schedule_status: not_created` для system file hygiene outputs, пока approved automation slice не зафиксировал другое;
- текущий command evidence до readiness, works, complete или release claims.

## Риски And Failure Modes

- A generated HTML/JSON view может быть mistaken для source truth.
- Stale graph fingerprints или caches может make old source look current.
- Provider artifacts может leak private data если redaction/cache/budget gates являются skipped.
- Review ledger decisions являются invalid без owner и evidence refs.
- Mutation artifacts являются unsafe без rollback proof.
- Planned artifact names может быть mistaken для executed evidence.

## Next Action

Используйте эта contract map когда writing docs tests, source registry entries и packaging/closure checks. Navigation и generated `site/` refresh являются intentionally handled после source docs packet является stable.
