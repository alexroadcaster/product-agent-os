# Product-Agent OS

## Task 22 final documentation sync closure

Task 22 final documentation sync closure описывает Product-Agent OS full stack after Track 1-9: package contracts, lifecycle skills, staged generation, approved merge, Codex-only runtime, engineering standards, scenario workflows and methodology intelligence. Track 1-9 history is provenance; the user-facing flow is read-only audit -> staged proposal -> approval -> implementation -> evidence -> review/release/learning.

The system remains Codex-first: no standalone Agents SDK runtime, no separate OpenAI API key for local deterministic tooling, no silent hooks or automation, and no completion claim without current evidence.

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

Task 24 Self-Verification And Modernization Loop adds a self-verification metrics loop for Product-Agent OS agents, skills, prompt/policy packs, router/tool policies and harness versions. The `agent_skill_metrics_loop` route emits staged evidence only: target registry, trace/dataset/grader summaries, scorecard ledger, report packet and modernization candidates. It performs no live eval/model/API calls, creates no active schedules, applies no candidates by itself and allows no self-applied updates.

Task 25 Project Code Graph And HTML Cockpit Visualization now has Task 25 Batch 13, Batch 14, Batch 15 and Batch 16 as the prior graph/cockpit baseline, plus Task 25 Batch 17 implemented for fixture structural fields, search-quality eval loop and future backend and semantic gates. Task 25 Batch 18 `T10-CG-V2-M31..M32` closes the baseline with focused/full verification: full unittest ran 664 tests with `OK`, fixture eval exited `0` for 91 fixture directories, transcript eval exited `0` with 17 sessions and 0 failures, Codex compatibility returned `status: compatible`, strict MkDocs and diff hygiene passed, and the explicit-only git boundary was preserved. The current `scan_project_code_graph.py` path is read-only and stage-first: dry-run/stage can emit redacted graph JSON/JSONL with file nodes, Python AST package/module/class/function/method overlays, conservative import/call/test edges, structured docs/contracts/schema/diagram overlays, partition scopes, canonical aliases, manifest freshness/provenance, controlled ontology validation and observation lineage. Query mode can read an existing graph artifact for bounded `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `changed_since`, `why_changed`, `read_order`, `hotspots`, `node`, `status` and `search` packets without loading source text. Runtime/status packets and graph analysis reports remain orientation evidence only. The Batch 16 cockpit renderer stages offline `.codex/product-agent-os/project-cockpit.html` and `.codex/product-agent-os/project-cockpit.json` review surfaces with exactly eight top-level pages, Code Flow inside `Code Intelligence`, Graphology-compatible static projection, local Graphology/Sigma vendor boundary, filters, selected-node evidence, fallback table, mobile CSS and no external assets. Batch 17 adds local search-quality eval loop evidence for symbol recall, top-k/MRR, trace labels, affected-test precision and edge density thresholds. Batch 19 adds the generated offline static search index as a cache, not as source of truth. Batch 20 adds a generated local file-store backend gate as an approved, disabled-by-default orientation cache with read-only contract API and graph-only fallback. Batch 21 adds a generated semantic retrieval index as `present_unverified` orientation evidence with no canonical graph edge rewrites. Batch 22 adds local deterministic LLM extraction-style proposals as generated review evidence only. Batch 23 adds generated extension closure evidence only. Generated cockpit HTML/JSON and backend/index/semantic/LLM proposal/closure caches are not source of truth. Live production server, live external model/API extraction and canonical graph mutation from generated proposals remain future-gated outside the approved Batch 19-23 surfaces without explicit approval with redaction, cache, token budget, eval threshold and rollback path.

Product-Agent OS - локальный Codex plugin и методологическая система для тех, кто строит реальные продукты с Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, memory, sandbox, approvals, MCP и AI-assisted development.

Он превращает vibe-coding из хаотичного "попросил агента написать код" в управляемую product engineering delivery system: с требованиями, архитектурой, документацией, проверками, агентными командами, release evidence и понятным next action.

Product-Agent OS создан для четырех аудиторий:

| Пользователь | Что получает |
| --- | --- |
| Vibe-coder | Быстрый путь от идеи к работающему продукту без мусорных файлов, потерянного контекста и случайных правок. |
| Developer | Requirements, plan, ownership, tests/evals, rollback, review и release packet вместо расплывчатого prompt-to-code. |
| AI Engineer | Eval-first workflow, prompt/model/tool/RAG contracts, dataset governance, grounding evidence и latency/cost/safety gates. |
| PO/PM | Прозрачную карту проекта: что строим, зачем, где риск, какие документы есть, что проверено и что еще нужно утвердить. |

## Зачем Он Создан

Codex умеет быстро писать код. Но на реальных проектах проблема не в скорости генерации, а в управлении контекстом:

- требования живут в чате и теряются между сессиями;
- архитектурные решения не записаны;
- agent workers меняют одни и те же файлы без ownership;
- тесты и evals появляются после реализации;
- AI/RAG качество оценивается на глаз;
- security, privacy, release и rollback вспоминаются слишком поздно;
- "готово", "works", "fixed" звучит без текущего evidence;
- проект зарастает временными файлами, не связанными с продуктовой целью.

Product-Agent OS выносит работу из чата в проверяемые артефакты и превращает Codex в управляемый delivery loop:

```text
idea / bug / product request
  -> read-only workspace audit
  -> complexity and maturity classification
  -> Delivery Map
  -> methodology recommendations
  -> staged artifacts
  -> agent team and skills
  -> implementation slices
  -> tests / evals / review
  -> release packet
  -> learning loop
  -> automation candidate
```

Главный принцип:

```text
cover every methodology domain
force only what is clearly applicable
record gaps and assumptions honestly
stage artifacts only after approval
```

## От Vibe-Coding К Product Engineering

| Vibe-coding failure | Product-Agent OS behavior |
| --- | --- |
| "Сразу напиши код" | Сначала фиксирует goal, scope, non-goals, acceptance criteria и safe next action. |
| "Потом разберемся с архитектурой" | Требует architecture boundary, ADR/tradeoff record или explicit accepted gap. |
| "Запусти несколько агентов параллельно" | Создает ownership split, owned/forbidden files, handoff packet и stop conditions. |
| "Тесты потом" | Переводит работу в test-first, eval-first или явно помеченный verification gap. |
| "Вроде работает" | Блокирует completion claims без current command/eval/runtime/owner evidence. |
| "Нужно только чуть-чуть поменять API/DB/AI" | Включает contract, migration, data, safety, compatibility and rollback gates. |
| "Сгенерируй документацию" | Выбирает документационные frameworks по домену, а не создает Markdown ради Markdown. |
| "Давай автоматизируем" | Продвигает workflow по цепочке manual thread -> playbook -> skill -> plugin -> automation candidate. |
| "Просто включи hooks/CI/release" | Требует staged proposal, approval boundary, rollback и owner evidence. |

## Как Работает

1. **Read-only audit**
   Product-Agent OS сначала читает workspace без записей: stack, package managers, entrypoints, docs, CI, tests, runtime manifests, API/data/AI surfaces, existing control-plane files and risk signals.

2. **Complexity and maturity classification**
   Система определяет `maturity_level` и `complexity_profile`, отделяя observed evidence от user intent и unknowns.

3. **Delivery Map**
   Пользователь получает карту проекта: surface map, system map, lifecycle map, methodology map and next-action map.

4. **Methodology recommendations**
   Product-Agent OS рекомендует только те methodology gates, которые реально закрывают риск, ownership gap, verification gap или release boundary.

5. **Approval before generation**
   Документы и инфраструктура создаются как staged proposals. Target workspace не мутируется silently.

6. **Agent team and skills**
   Под проект создаются роли, skills, task packets, ownership boundaries and verification expectations.

7. **Evidence loop**
   Каждая meaningful slice проходит через tests/evals/review/RUNLOG before completion claims.

## Classification Model

Product-Agent OS оценивает проект по двум независимым осям.

| `maturity_level` | Когда выбирается | Что меняет |
| --- | --- | --- |
| `baseline` | MVP, solo project, low-risk internal tool | Минимальный control plane, lightweight requirements, plan, checks and runlog. |
| `team` | Несколько людей, subagents, worktrees, shared code ownership | Handoff, ownership, agent team, architecture and docs impact становятся обязательными. |
| `production` | Есть пользователи, deployment, data, release process, support | Требуются release evidence, rollback, security/privacy review, observability and operations. |
| `regulated` | PII, payments, finance, healthcare, minors, enterprise governance, legal/compliance | Включаются compliance overlays, privacy impact, audit evidence, approvals and stricter ownership. |

| `complexity_profile` | Когда выбирается | Что меняет |
| --- | --- | --- |
| `simple` | Узкая задача, мало зависимостей, низкий blast radius | Легкий workflow без heavy methodology. |
| `standard` | Обычный продукт, UI/API/data/docs/tests surfaces | Требуются базовые gates, artifacts, tests/evals and docs impact. |
| `complex` | Несколько подсистем, интеграций, data stores, teams, workflows | Включаются architecture, domain, ownership, integration and release gates. |
| `high_risk` | Security, privacy, money, production data, irreversible migration, public contract, AI behavior, release risk | Требуются P0/P1 recommendations, explicit approvals, rollback and current evidence. |

Система хранит:

- `observed_signals`: факты из файлов и структуры workspace;
- `intent_signals`: намерение пользователя, не доказательство;
- `unknowns`: недостающие факты;
- `questions_for_owner`: вопросы владельцу продукта/проекта;
- `provisional_assumptions`: консервативные допущения;
- `confidence`: уверенность классификации;
- `blocked_until_answered`: что нельзя делать без ответа;
- `safe_next_action`: следующий безопасный шаг.

## Readiness Statuses

Product-Agent OS не считает наличие файла доказательством готовности.

| Status | Значение |
| --- | --- |
| `not_applicable` | Gate не нужен для этого проекта или slice. |
| `applicable_missing` | Gate применим, но evidence/artifact отсутствует. |
| `present_unverified` | Найден файл/сигнал, но нет текущего evidence. |
| `present_verified` | Есть текущая команда, eval, owner evidence или проверенный artifact. |
| `proposal_staged` | Artifact создан как proposal, но еще не применен. |
| `explicit_gap_accepted` | Владелец принял gap с reason, scope, residual risk and review date. |
| `approval_required` | Действие или artifact требует явного approval перед записью/выпуском/внешним действием. |

## Methodology Intelligence

Product-Agent OS знает не одну "любимую" методологию. Он выбирает набор практик под риск, зрелость и домен проекта.

| Methodology / framework | Когда применяется | Что требует Product-Agent OS |
| --- | --- | --- |
| ATDD | Behavior-changing work before implementation | Acceptance scenario, expected behavior, check, evidence owner. |
| BDD / Specification by Example | Нужен общий язык между PO/PM, разработкой и тестированием | Given/When/Then или equivalent behavior table, business rules, examples, edge cases. |
| TDD | Изменяется логика, API, domain behavior, parser, data transform | Red-Green-Refactor path или explicit test gap. |
| Test Pyramid / Test Trophy | Нужно сбалансировать unit, integration, contract, E2E, visual and eval checks | Risk-based test strategy, not "only E2E" or "only unit". |
| Contract Testing | API/event/integration behavior affects consumers | Provider/consumer contract, compatibility check, examples and owner. |
| Property-Based Testing | Input space large, parser/validator/data transform sensitive | Properties, generators, invariants, seed/repro evidence. |
| DDD | Complex domain, enterprise/workflow/data-heavy/multi-context systems | Bounded contexts, ubiquitous language, aggregates, invariants, domain events, expert review. |
| EventStorming / Domain Storytelling | Сложные бизнес-процессы и события | Event catalog, actors, commands, policies, timeline, integration assumptions. |
| FSD | Web frontend grows by business features and ownership boundaries | Layers, slices, segments, public API, import rules, component ownership. |
| C4 Model | Нужно объяснить system/container/component boundaries | Context/container/component views as far as useful. |
| arc42 | Требуется структурированная architecture documentation | Architecture overview, constraints, quality attributes, risks, decisions. |
| ADR / MADR | Есть high-impact technical decision | Decision, context, options, consequences, owner, review date. |
| API-first / Contract-first | Public or shared API, SDK, integration or event contract | OpenAPI/AsyncAPI/GraphQL/protobuf source of truth before implementation. |
| OpenAPI | REST-like HTTP API | Operations, schemas, errors, auth, examples, compatibility. |
| AsyncAPI / CloudEvents | Events, webhooks, message-driven systems | Topics, payloads, ordering, retries, idempotency, signatures, dead-letter behavior. |
| GraphQL SDL | GraphQL schema is a public/internal contract | Schema, breaking-change review, resolver/data ownership. |
| gRPC / Protobuf | Binary/RPC contracts or generated clients | `.proto` ownership, compatibility, generated client manifest. |
| Docs-as-code | Documentation must be maintained with code | Source files, review path, docs check, build command, ownership. |
| AI eval-first development | Prompt/model/RAG/tool behavior changes | Baseline, dataset policy, rubric, threshold, rerun command, failure examples. |
| RAG evaluation | Retrieval, grounding, source quality or hallucination risk | Source inventory, chunking/retrieval config, grounding eval, data lineage. |
| SRE / SLO | Production service, reliability or operational risk | SLO, error budget/gap, observability, incident path, runbook. |
| DORA metrics | Delivery performance and release health matter | Deployment frequency, lead time, change failure, recovery evidence. |
| Twelve-Factor App | Service-style app or cloud runtime | Config, logs, dependencies, env parity, build-release-run boundaries. |
| Progressive Delivery | Canary/blue-green/feature flags/rollout risk | Rollout strategy, abort criteria, monitoring, rollback. |
| SemVer | Package, SDK, API, plugin or release artifact | Version impact and compatibility class. |
| Keep a Changelog | User-visible release history matters | Changelog/release notes tied to artifacts and evidence. |
| Conventional Commits | Release automation or history hygiene | Commit category policy only when it fits project governance. |
| OWASP ASVS / API Security / LLM Top 10 | Auth, API, AI, secrets, PII, public surface | Threat surface, negative tests, abuse cases, security evidence. |
| NIST SSDF / Cybersecurity Framework | Secure development and governed delivery | Secure SDLC practices, supply-chain review, risk ownership. |
| Privacy Impact Assessment | PII, sensitive data, retention, deletion, tracking | Data classification, legal/owner review, retention, minimization, deletion path. |
| DataOps / Migration-first / Expand-contract | Database/schema/data movement changes | Migration plan, dry run, rollback/compensation, data quality checks. |
| SBOM / SLSA / OpenSSF | Supply-chain and release trust matter | Dependency/provenance review, package risk, CI permission review. |

## 12 Domains Product-Agent OS Covers

| Domain | What it protects | Typical signals | Documents and artifacts | Checks and evidence |
| --- | --- | --- | --- | --- |
| Business & Product | Product value, target user, metric quality, post-release learning | Product prompts, metrics, analytics, growth/release goals | Product brief, value proposition, opportunity tree, experiment plan, metric spec, post-release measurement | Hypothesis clarity, success metric, counter-metric, privacy classification, owner signoff |
| Requirements & Domain | Behavior correctness and shared language | User stories, business rules, domain terms, workflows, bounded contexts | `REQUIREMENTS.md`, acceptance scenarios, traceability matrix, business rules, ubiquitous language, context map, event catalog | Requirement -> scenario -> check -> evidence owner, domain expert review |
| Solution Architecture | Boundaries, tradeoffs, quality attributes | ADRs, architecture docs, modules, services, integrations | Architecture overview, ADR/MADR, C4 views, arc42 sections, quality attribute scenarios, tradeoff record, trust-boundary map | Architecture boundary, public contract trace, fitness function, owner review |
| Quality, Testing & Evals | Proof that behavior works now | Test commands, CI, evals, Playwright, pytest, Vitest, promptfoo/Ragas | `TEST.md`, `EVALS.md`, quality strategy, test/eval matrix, CI evidence, flaky test policy, manual QA evidence | Current command output, eval rerun, runtime evidence, bug reproduction, test gap labels |
| Codex / Agentic Workflow | Safe AI-assisted delivery | `.codex`, skills, subagents, MCP, hooks, automations, AGENTS.md | `AGENTS.md`, agent task packet, handoff contract, worktree ownership, skill promotion record, automation candidate | Ownership split, model/reasoning policy, approval boundary, hook/MCP permission review |
| Frontend | UI behavior, accessibility, component contracts | React/Vue/Svelte/Next, routes, Storybook, Playwright, FSD folders | Component card, component state matrix, Storybook docs, accessibility review, visual evidence, performance budget | Component states, keyboard focus, responsive viewports, a11y, screenshots, console/runtime evidence |
| Backend | Service behavior, failure modes, operations | APIs, jobs, queues, services, env config, logs, health checks | Service overview, runtime behavior, dependency failure matrix, health check contract, SLO sheet, runbook | Integration tests, retries/idempotency, config/secrets boundary, observability, rollback |
| API & Integrations | Contracts and compatibility | OpenAPI, AsyncAPI, GraphQL, protobuf, webhooks, generated clients | API inventory, API contract review, consumer map, error catalog, auth matrix, SDK manifest, webhook event contract | Contract check, breaking-change review, auth/security scheme, external-write approval |
| Database & Data | Schema/data safety and lineage | Migrations, ORM schema, SQL, DBML, dbt, data pipelines, PII | Database dictionary, migration plan, schema source, data classification, data quality contract, lineage record, backup/restore evidence | Dry run, rollback/compensation, backup, data quality, production access approval |
| LLM / AI / RAG | AI behavior, grounding, safety, cost | Prompts, models, embeddings, vector stores, tools, evals, RAG pipeline | AI behavior spec, prompt contract, model decision record, tool contract, RAG source inventory, grounding eval, dataset governance | Baseline eval, rerun command, no-private-data fixtures, latency/cost, human approval boundary |
| Security, Privacy & Compliance | Abuse, data leakage, auth, governance | Auth, permissions, secrets, payments, PII, CI permissions, SBOM | Threat surface, security risk review, ASVS/SSDF mapping, privacy impact record, secrets policy, supply-chain review, audit logging review | Negative authz tests, secret scanning policy, privacy owner review, compliance overlay |
| Delivery, Release & Operations | Safe shipping and recovery | Changelog, versions, package manifests, deploy files, CI/CD, release intent | Release readiness, release packet, artifact manifest, rollout strategy, rollback recovery, CI/CD governance, incident response path | Build/test/docs evidence, SemVer impact, publish approval, rollback, observability release evidence |

## Documentation And Artifact Catalog

Product-Agent OS не генерирует "папку с документами ради документов". Artifact появляется, когда он закрывает gate, снижает риск, фиксирует ownership или дает следующий безопасный шаг.

| Artifact family | Files and outputs |
| --- | --- |
| Control plane | `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `.codex/config.toml` |
| Audit outputs | `methodology-audit-report.md`, `methodology-applicability.json`, Delivery Map, questions for owner, safe next action |
| Agent/team | `.codex/agents/*.toml`, agent task packet, handoff contract, worktree ownership, source context pack |
| Product | product brief, value proposition, opportunity tree, experiment plan, metric spec, analytics tracking plan, post-release measurement |
| Requirements/domain | acceptance scenarios, traceability matrix, business rules, ubiquitous language, context map, event catalog, domain review record |
| Architecture | architecture overview, ADR/MADR, C4 diagrams, arc42 sections, quality attribute scenarios, trust-boundary map, fitness functions |
| Planning/review | build slice, plan quality check, review slice, PR risk review, rollback plan, risk register |
| Frontend | component card, component state matrix, Storybook docs, visual evidence packet, accessibility review, performance budget |
| Backend | service overview, runtime behavior, dependency failure matrix, health check contract, SLO sheet, operational runbook |
| API/integration | API inventory, OpenAPI/AsyncAPI review, consumer map, error catalog, auth matrix, generated SDK manifest, webhook event contract |
| Database/data | database dictionary, migration plan, DBML/ERD, data classification matrix, data quality contract, lineage record, backup/restore evidence |
| AI/RAG | AI behavior spec, AI eval spec, prompt contract, model decision record, tool contract, RAG source inventory, grounding eval, dataset governance |
| Security/privacy | threat surface, security risk review, ASVS/SSDF mapping, privacy impact record, secrets policy, supply-chain review, audit logging review |
| Delivery/ops | release readiness, release packet, artifact manifest, rollout strategy, rollback recovery, CI/CD governance, incident response path |
| Automation | automation candidate, promotion evidence, owner/cadence contract, rollback, manual success log |

## Documentation Framework Selector

Product-Agent OS выбирает documentation tooling по домену и сложности проекта.

| Tool / framework | Где применяется | Product-Agent OS behavior |
| --- | --- | --- |
| MkDocs | Internal/product engineering docs, Python-heavy/docs-as-code repos | Stages docs structure, nav impact, docs check and strict build path. |
| Docusaurus | Developer portal, SDK/API docs, product docs | Recommends when a JS docs portal is already present or external developer docs matter. |
| Sphinx / Read the Docs | Python libraries, API reference, research-heavy docs | Connects source docs, generated reference and build verification. |
| Antora | Large multi-repo enterprise docs | Used when versioned component docs and multi-repo docs governance matter. |
| Mermaid | Lightweight diagrams in Markdown | Workflows, state machines, sequence diagrams, system maps, Delivery Map visuals. |
| PlantUML | More formal UML/C4-ish sequence/component diagrams | Recommended when diagram review and versioned architecture diagrams matter. |
| C4 Model | Architecture communication | Context, container and component views tied to boundaries and ownership. |
| Structurizr DSL | C4 as code | Useful when architecture model should be machine-readable and versioned. |
| arc42 | Architecture documentation structure | Applied for production/complex systems needing constraints, quality attributes and risks. |
| ADR / MADR | Decision records | Required for high-impact architecture/API/data/security/release decisions. |
| OpenAPI / Swagger UI | HTTP API contracts and docs | OpenAPI file is source of truth; rendered docs are output, not source. |
| AsyncAPI | Event-driven APIs, webhooks, message contracts | Captures topics, payloads, retries, idempotency, ordering and dead-letter behavior. |
| GraphQL SDL | GraphQL schema documentation | Tracks schema, breaking changes, deprecation and resolver/data ownership. |
| Protobuf / gRPC | RPC contracts and generated code | Requires `.proto` ownership, generated client manifest and compatibility review. |
| JSON Schema | Payload/schema validation | Used for contract checks, config schemas and fixture validation. |
| Pact | Consumer-driven contracts | Applied when provider/consumer compatibility is the main risk. |
| Storybook / MDX | Frontend component docs | Documents states, variants, interactions, a11y and visual evidence. |
| TypeDoc / JSDoc / Javadoc / XML docs | Code reference | Used for public SDKs/libraries where API reference matters. |
| DBML / dbdocs / SchemaSpy | Database documentation | Generates schema maps and dictionaries only from safe sources, with secrets excluded. |
| dbt docs / Great Expectations | Analytics and data quality docs | Tracks data models, tests, contracts and data quality gates. |
| OpenLineage | Data lineage | Used for analytics/RAG/data movement ownership and incident visibility. |
| Vale / markdownlint | Documentation quality | Adds style/lint checks when docs quality is part of delivery. |

## Documentation Tooling By Domain

| Domain | Documentation frameworks | What gets documented |
| --- | --- | --- |
| Business & Product | Opportunity Solution Tree, Lean Startup experiment notes, HEART/North Star metric sheets, MkDocs/Docusaurus | Product hypothesis, target segment, value proposition, opportunity, metric, guardrail and post-release learning. |
| Requirements & Domain | ATDD, BDD, Gherkin, Example Mapping, EventStorming, Domain Storytelling, Mermaid, C4 | Acceptance scenarios, examples, business rules, domain events, bounded contexts, ubiquitous language and traceability. |
| Solution Architecture | C4 Model, arc42, ADR/MADR, Structurizr DSL, Mermaid, PlantUML | System context, containers, components, constraints, quality attributes, decisions, tradeoffs and architecture risks. |
| Quality, Testing & Evals | Test Pyramid, Test Trophy, contract testing, Playwright reports, pytest/Vitest reports, promptfoo/Ragas eval reports | Test strategy, coverage by risk, eval baseline, CI evidence, runtime evidence, flaky tests and evidence gaps. |
| Codex / Agentic Workflow | `AGENTS.md`, Codex skills, subagent task packets, MCP permission review, workflow templates | Agent roles, model/reasoning policy, handoff contracts, ownership, approvals, hooks, skill promotion and automation readiness. |
| Frontend | Storybook Autodocs/MDX, FSD docs, Playwright screenshots, axe/a11y reports, Mermaid user flows | Component states, UI flows, design-system boundaries, accessibility, responsive behavior, visual evidence and performance budget. |
| Backend | Twelve-Factor notes, SRE runbooks, OpenTelemetry docs, health check contracts, Mermaid/PlantUML sequence diagrams | Service boundaries, runtime behavior, dependencies, failure modes, jobs/queues, observability, SLOs and rollback. |
| API & Integrations | OpenAPI, AsyncAPI, GraphQL SDL, Protobuf, JSON Schema, CloudEvents, Pact, OpenAPI Generator | API contract, event contract, schemas, errors, auth, consumers, generated clients, compatibility and external writes. |
| Database & Data | DBML, dbdocs, SchemaSpy, SQL DDL, ORM schema docs, dbt docs, Great Expectations, OpenLineage | Tables, fields, relationships, migrations, data quality, classification, lineage, retention and backup/restore evidence. |
| LLM / AI / RAG | Prompt contracts, model decision records, RAG source inventory, promptfoo/Ragas/OpenAI eval artifacts, OpenTelemetry traces | AI behavior, prompts, model choice, tool contracts, retrieval config, grounding, datasets, safety and cost/latency. |
| Security, Privacy & Compliance | STRIDE/threat modeling, OWASP ASVS/API/LLM mappings, NIST SSDF, NIST Privacy Framework, SBOM formats SPDX/CycloneDX | Threat surface, authn/authz, secrets, privacy impact, supply chain, audit logging, abuse controls and compliance overlay. |
| Delivery, Release & Operations | SemVer, Keep a Changelog, Conventional Commits, DORA, SRE runbooks, rollout/rollback plans, CI/CD governance docs | Release scope, version impact, changelog, artifact manifest, rollout, rollback, incident path and operational readiness. |

## Agent Teams And Skills

Product-Agent OS не создает "команду агентов" из красивых названий. Он проектирует roles вокруг ownership, handoff artifacts, verification and stop conditions.

| Skill | Role in delivery |
| --- | --- |
| `project-lifecycle-orchestrator` | Determines lifecycle state and next bounded step. |
| `workspace-discovery-auditor` | Runs read-only audit and records signals, risks, missing artifacts and owner questions. |
| `requirements-author` | Turns idea/request into requirements, non-goals, acceptance scenarios and domain questions. |
| `implementation-planner` | Produces executable plan with exact files, commands, rollback, evidence owner and placeholder scan. |
| `agent-team-designer` | Creates subagent roles, ownership split, handoff packets, worktree boundaries and sequential fallback. |
| `test-eval-designer` | Defines deterministic tests, subjective evals, AI/RAG evals and current evidence requirements. |
| `risk-reviewer` | Performs two-stage review: spec compliance first, quality/risk second. |
| `pr-release-operator` | Prepares PR/release packet, changelog, SemVer impact, publish boundary and rollback evidence. |
| `learning-loop-maintainer` | Moves failures, lessons and durable rules into the right long-lived artifacts. |
| `automation-promoter` | Creates automation candidates only after manual success evidence and rollback are clear. |

Packaged project roles include product manager, architect, builder, tester, reviewer, docs maintainer and release operator. Each handoff must carry:

- sources/context used;
- assumptions;
- owned files and forbidden files;
- expected evidence;
- output schema;
- stop conditions;
- open risks;
- recommended next role.

Raw chat history is not a valid worker context.

## Scenarios It Handles

Product-Agent OS ships scenario workflows for common real-world project starts and rescue situations:

- first-run intake;
- greenfield idea to first vertical slice;
- bug rescue and root-cause work;
- complex system acceleration;
- PR review readiness;
- legacy onboarding;
- API migration;
- AI/RAG eval regression;
- native/mobile feature work;
- desktop local-first work;
- data migration;
- security-sensitive change;
- CI stabilization;
- release packaging;
- docs-only and maintenance work.

Each scenario defines first response, minimum artifacts, approval boundary, forbidden shortcuts and verification gates.

Task 23 guided question protocol and status dashboard is implemented as a staged Product-Agent OS capability. `question_queue_contract_present` keeps first responses compact with one blocking question maximum; `status_snapshot_present` and `status_dashboard_present` stage `.codex/product-agent-os/status.html` and `.codex/product-agent-os/status.json`; `dashboard_not_source_of_truth` and `stale_evidence_no_success_claim` preserve underlying artifacts as source material and block success claims from stale evidence.

## Example: What A User Sees

User request:

```text
I have a Next.js app with a backend API, PostgreSQL, Stripe payments and an AI assistant.
Help me turn it into a product-ready project.
```

Product-Agent OS should not start by generating code. It should:

1. Run a read-only audit.
2. Classify the project as at least `production` maturity and `high_risk` complexity.
3. Build a Delivery Map: UI routes, API surface, database, payment integration, AI/RAG surface, CI/release status, docs gaps.
4. Recommend only relevant gates: product metrics, requirements traceability, architecture boundary, API contract, database migration safety, AI eval baseline, security/privacy review, release readiness.
5. Stage artifacts such as `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `api-contract-review.md`, `database-dictionary.md`, `ai-eval-spec.md`, `security-risk-review.md`, `release-readiness.md`.
6. Ask for approval before target workspace writes, external actions, CI changes, payment/security changes or release operations.
7. Create an agent team with owned/forbidden files and handoff packets before parallel implementation.

## Safety Model

Product-Agent OS is intentionally conservative.

- Read-only audit comes before generation.
- Recommendations come before artifacts.
- Staged artifacts come before target workspace writes.
- Explicit approval is required for writes, hooks, external systems, production data, publishing, release actions and active automations.
- Existing user files are preserved outside managed sections.
- Secrets, tokens, private keys, customer data, raw private chats and absolute user-specific paths must not enter docs, fixtures, prompts, templates or examples.
- Detection is not verification.
- Completion claims require current evidence.
- Community claims do not become project rules without `trust_level` and `verification_status`.
- Official OpenAI docs remain source of truth for Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, memory, sandbox, approvals, MCP and Agents SDK behavior.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `plugins/product-agent-os/` | Working local Codex plugin package. |
| `plugins/product-agent-os/.codex-plugin/plugin.json` | Plugin manifest. |
| `plugins/product-agent-os/skills/` | Lifecycle skills used by Codex. |
| `plugins/product-agent-os/assets/templates/` | Control-plane, workflow, artifact, eval, agent, hook and PR/release templates. |
| `plugins/product-agent-os/scripts/` | Renderer, merge tooling, validators, fixture evals, transcript evals and runtime contract runner. |
| `docs/methodologies/` | Source methodology research across 12 domains. |
| `docs/product-agent-os/` | Operator docs for scenarios, architecture, evals and compatibility. |
| `docs/superpowers/specs/` | Product/design specs. |
| `docs/superpowers/plans/` | Implementation plans. |
| `tests/product_agent_os/` | Unit and contract tests for plugin behavior. |
| `site/` | Tracked MkDocs HTML output. |
| `AGENTS.md` | Durable project rules. |
| `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` | Control-plane files for this repository's own development. |

## Quick Start

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run a read-only infrastructure plan:

```powershell
python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --dry-run
```

Stage proposed artifacts outside the target workspace:

```powershell
python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --stage C:\tmp\product-agent-os-stage
```

Build a read-only merge plan:

```powershell
python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> C:\tmp\product-agent-os-stage --plan
```

Apply only with an approval record:

```powershell
python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> C:\tmp\product-agent-os-stage --apply --approval-file <approval.json>
```

Run the Codex-only route contract:

```powershell
python plugins\product-agent-os\scripts\run_codex_runtime_runner.py <workspace> --contract
```

Run methodology audit:

```powershell
python plugins\product-agent-os\scripts\run_methodology_audit.py <workspace> --report
python plugins\product-agent-os\scripts\run_methodology_audit.py <workspace> --json
```

## Verification

Documentation check:

```powershell
python tools\check_docs.py
```

Plugin verification:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
```

MkDocs strict build:

```powershell
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict
```

## What Product-Agent OS Is Not

- It is not a replacement for product ownership, domain expertise, security review or legal review.
- It does not make every methodology mandatory.
- It does not silently write into target projects.
- It does not activate hooks, GitHub Actions, schedules, recurring automations, publishing or external writes without approval.
- It does not treat files, folders or prompt intent as proof of readiness.
- It does not use chat memory as source of truth.
- It is not a standalone Agents SDK app and does not require a separate OpenAI API key for its local deterministic tooling.

## Product Direction

Product-Agent OS is moving toward a full methodology-aware operating system for AI-assisted product delivery:

- first-run project intelligence;
- 12-domain methodology selection;
- staged documentation and artifact generation;
- agent team design;
- eval-driven quality;
- safety and approval boundaries;
- release and learning loops;
- automation only after manual success evidence.

The end state is simple: a user can connect Product-Agent OS to a messy project and get a credible path toward a product that can be reviewed, tested, released and explained.
