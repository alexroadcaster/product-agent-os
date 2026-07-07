# Product-Agent OS scenarios

Source status: `official + experiment`

Источники: [Codex workflows](https://developers.openai.com/codex/workflows), [Codex use cases](https://developers.openai.com/codex/use-cases), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Product-Agent OS plugin](index.md), [Behavioral evals](behavioral-evals.md), [Codex compatibility](codex-compatibility.md).

Эта страница отвечает на практический вопрос: какой route должен выбрать Product-Agent OS plugin, когда Codex App, CLI или IDE extension видит реальный workspace и пользователь просит не просто "написать код", а довести работу до проверяемого результата.

Scenario не заменяет lifecycle. Он выбирает первый малый шаг, minimum artifacts, approval boundary и verification gates. Если evidence нет, route должен вернуть gap, а не готовность.

## Operator Route Map

Scenarios являются route decisions, а не permission на запуск live systems. Каждый route должен назвать source context, ожидаемые доказательства, approval boundary и stop condition до передачи work в subagent, skill или implementation slice.

| Route | Когда выбирать | Minimum evidence | Остановиться condition |
| --- | --- | --- | --- |
| `code_graph_orientation` | Нужно понять code/docs topology до build или review. | Existing source files plus generated graph/cockpit packet labeled как orientation evidence. | Не claim source truth из generated graph; read source до implementation claims. |
| `live_runtime_read_only` | Нужно проверить local runtime contract или graph-only API fallback. | Governance packet и disabled runtime contract. | Остановиться до live server launch пока separate approval packet exists. |
| `provider_retrieval_eval` | Нужно оценить embedding/reranker/LLM provider benefit. | Redaction, cache, budget, baseline и threshold fallback packet. | Остановиться до any provider/live external model/API call без explicit approval. |
| `canonical_graph_mutation_review` | Нужно проверить proposal acceptance и mutation readiness. | Human review ledger, proposal diff, mutation dry-run plan и rollback proof. | Остановиться до canonical graph mutation пока owner accepted proposal и rollback evidence является current. |
| `real_testing_approval` | Нужно перейти от staged evidence к controlled real testing. | Target/data owner approval, runtime/browser/provider/mutation/git action packet и rollback plan. | Остановиться пока specific action является approved; approvals являются не bundled. |

## G4 Operator Flows

G4 routes добавляют четыре системных маршрута. Они не дают approval на cache refresh, global config write, live runtime, browser automation, provider/API calls, target mutation, git, release или automation.

| Route | Когда применять | Evidence boundary |
| --- | --- | --- |
| `instruction_tool_use_compliance` | Нужно проверить, когда Product-Agent OS skill/plugin route можно выбрать implicitly, а когда нужен explicit user request. | Использует официальные Codex docs, `allow_implicit_invocation`, `explicit_only`, `narrow_implicit` и `blocked_implicit`; fresh-session proof остается отдельным. |
| `operator_command_matrix` | Нужно выбрать безопасную команду для first-run analysis, graph/cockpit или docs-tooling smoke. | Использует help/current command evidence, stage только для generated artifacts и оставляет широкие scans/root `site` rebuild внутри approval-boundary. |
| `guided_question_answer_ledger` | Нужно задать вопрос без превращения intake в длинную анкету. | Ограничивает blocking question одной штукой; `answers_require_staged_ledger_and_owner_review` действует до source promotion. |
| `source_cache_session_state` | Нужно понять, почему source, installed cache и active session могут расходиться. | Требует read-only comparison fields и fresh-session proof до любого claim `fixed` или `ready`. |
| `professional_code_authoring` | Нужно ограничить custom code, dependency debt, shallow wrappers или risky refactor в не механической coding task. | Использует [Professional Code Authoring standards](coding-standards.md), checklist evidence и shortcut evals; остается source contract пока нет runtime или owner-pilot proof. |

## Входы

- цель пользователя или `intent_hint`, если он передан в Codex runtime runner;
- read-only workspace audit: files, stack, test/build commands, docs, CI, contracts и control-plane files;
- текущие `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- политика источников, sandbox, approvals и known external-system boundaries;
- previous failure notes, если already recorded в `RUNLOG.md`.

Key routing fields включают `finish_options` и `safe_next_action`; they tell next worker следует ли к answer, stage proposal, request approval, запуск focused verification или stop на evidence gap.

## Выходы

- `usage_mode.primary`, secondary mode, confidence и routing reasons;
- first response: один ближайший полезный шаг без широкого scaffold, rewrite или external mutation;
- minimum artifacts: concrete files или packets needed до build/review/release;
- approval boundary: what является read-only, staged-only или approval-required;
- verification gates: commands, evals, screenshots, logs, owner review или accepted gap;
- residual risk когда route является based на detection rather than verified evidence.

## Guided Question Protocol And Status Dashboard

Guided question protocol использует typed `question_queue` packets so first response может show только `next_blocking_question`, `question_counts` и `question_summary`. Это asks один blocking question maximum, keeps recommended и optional questions в packet, и routes answers в artifacts или accepted gaps. Guided questions являются не workspace evidence и не replace read-only audit, текущий command evidence, runtime evidence, owner review или accepted gaps.

Этот status snapshot является JSON source для generated dashboard view. Этот dashboard stages `.codex/product-agent-os/status.html` и `.codex/product-agent-os/status.json` через existing approval flow. `status.html` является generated view only: underlying artifacts остаются source material, dashboard является не editable database, и stale или inspection-only evidence не может produce success claim.

## Self-verification и modernization loop

`agent_skill_metrics_loop` route reviews agents, skills, prompt/policy packs, router/tool policy и harness-version behavior. Он начинается с read-only target registry, explicit запуск evidence, trace intake, dataset quality checks, local grader summaries и grader/judge calibration. Это может stage scorecard ledger records, daily или weekly packets, `agent-skill-evaluation-report.html` и modernization candidates, но every output является staged evidence only.

Этот route использует политика канонического источника: control-plane artifacts, запуск records, trace/eval packets и accepted gaps может support metrics loop; dashboard HTML, report HTML, memory, raw chat logs и unsupported community claims не могут. Этот report является не является каноническим источником и не может turn stale или generated evidence в completion claim.

Этот approval boundary stays strict. Product-Agent OS records cadence recommendation values `L0`, `L1`, `L2` и `L3`, но это creates нет active schedules. Это performs нет live eval/model/API calls, makes нет external writes, applies нет modernization candidates через itself и allows нет self-applied updates. Owner review, rollback target и explicit approval state являются required до any proposed update moves beyond staged review.

## Project Code Graph And Cockpit

Этот graph route provides read-only project graph foundation и generated cockpit для route orientation. Это может produce staged graph JSON/JSONL с file-level nodes, Python AST overlays, conservative import/call/test edges, structured Markdown/OpenAPI/AsyncAPI/DBML/SQL/JSON/YAML/Mermaid/PlantUML overlays, controlled ontology/schema validation, manifest freshness/provenance, observation lineage, temporal edge helpers, partition scopes и canonical aliases.

Этот cockpit renderer может stage offline `.codex/product-agent-os/project-cockpit.html` и `.codex/product-agent-os/project-cockpit.json` review surfaces с top-level pages, Code Flow, static projection, local vendor boundary, graph filters, focused subgraphs, selected-node evidence, fallback tables, mobile layout и нет external assets. Эта helps routes point agents toward source files и stale graph gaps без treating generated artifacts как канонический источник.

Этот boundary остается conservative: generated graph artifacts, runtime graph summaries, analysis reports и HTML cockpit views являются только review evidence. Scanner и cockpit renderer не мутируют target workspaces. Live database/server, live external model/API embedding или cross-encoder providers, LLM semantic extraction, rationale/comment extraction и canonical graph mutation остаются approval-bound future actions, пока explicit approval не задаст redaction, cache, token budget, eval threshold и rollback path.

## G5 evidence-quality routes

Эти маршруты применяются, когда пользователь спрашивает не о новом поведении plugin, а о качестве и границах generated evidence.

| route_id | Когда применять | Минимальный результат | Граница |
| --- | --- | --- | --- |
| `generated_artifact_ux_criteria` | HTML/report выглядит слишком диагностическим или готовится owner review. | Checklist качества, claim ceilings, `Vale` advisory status, `Storybook` trigger status. | Browser proof и Storybook install остаются `approval_required`. |
| `graph_intelligence_contract` | Используются graph packets, ontology, rejected links, freshness или query packets. | Orientation summary, stale/rejected-link handling, source-read-before-edit reminder. | Graph packet не заменяет source read и не разрешает mutation. |
| `privacy_supply_chain_retention` | Обсуждаются cache/session evidence, SBOM, vulnerability audit, remediation или raw reports. | Redaction and retention boundary, approval gates, unsupported claims. | Broad scans, remediation и raw report retention требуют отдельного approval. |
| `local_html_interaction_boundary` | Generated HTML содержит tabs, search, filters или diagrams. | Local-only interaction rules, no-network policy, fallback и browser-proof packet fields. | Static check не равен browser proof. |
| `residual_follow_up_site_freshness` | Нужно закрыть G1.1 residuals или понять final `DOC-M25`. | Residual routing table, private-target redaction policy, site freshness gate. | Root `site`, search и sitemap свежие после `documentation_refresh_DOC-M25-A01`; `documentation_refresh_DOC-M25-A02` обновляет их после T15 source sync; browser proof отдельно. |

## Scenario Matrix

| usage_mode | Когда применять | first response | minimum artifacts | approval boundary | verification gates |
| --- | --- | --- | --- | --- | --- |
| `first-run-intake` | Empty workspace, broken verification, existing control-plane или complex first launch. | Name mode, confidence, next smallest action и evidence gaps. | Intake summary, текущий lifecycle state, следующий action. | Нет scaffold, broad fix или parallel work до route является accepted. | Read-only audit, control-plane check, политика источников. |
| `bug_rescue` | User reports broken behavior, failing tests или regression. | Reproduce или isolate до changing code. | `bug-rescue-report.md`, failure evidence, root-cause hypothesis. | Нет fix claim без reproduction evidence. | Failing command/log, focused regression check, текущий evidence. |
| `greenfield_idea` | Idea-stage или empty product direction. | Shape один vertical slice до scaffold. | `greenfield-idea-brief.md`, selected direction, non-goals. | Scaffold требует explicit approval. | Acceptance scenarios, first slice plan, lightweight-mode decision. |
| `complex_system_acceleration` | Existing multi-surface app, integrations, multiple services или unclear ownership. | Build map до parallelization. | `integration-catalog.md`, ownership split, release gates. | Нет parallel work с overlapping files или unclear external-system owners. | Integration inventory, ownership review, release risk gates. |
| `pr_review` | Review или merge-readiness request. | Stay read-only и review changed files. | PR review readiness, changed-files map, `pr-risk-review.md`. | Нет push, PR creation, merge или external comment без approval. | Two-stage review: spec compliance до quality/risk. |
| `legacy_onboarding` | Old, undocumented или unknown repository. | Orient до refactor. | `onboarding-map.md`, entry points, запуск commands, docs debt. | Нет cleanup/refactor пока map и verification status являются explicit. | Present-unverified labels, source map, запуск command evidence. |
| `api_migration` | HTTP API, event contract, generated client или consumer change. | Plan compatibility до implementation. | `migration-plan.md`, `api-contract-review.md`, consumers, rollout. | Release или breaking change требует owner review и approval. | Contract check, backward compatibility, deprecation и rollout evidence. |
| `ai_eval_regression` | AI/RAG quality, prompt, model, retrieval, dataset или judge changes. | Baseline first. | `ai-eval-spec.md`, dataset policy, rubric, thresholds. | Нет quality claim из inspection-only evidence. | Baseline, rerun command, latency/cost/grounding и failure examples. |
| `native_mobile_feature` | iOS, Android или native mobile behavior. | Record platform assumptions до implementation. | Platform runtime check, permissions, offline/device plan. | Permission, signing или store changes требуют approval. | Build command, simulator/emulator или device logs, screenshots, manual gap. |
| `desktop_local_first` | Desktop app, filesystem, local DB, indexing или packaging. | Map local data и OS assumptions first. | Local data risk note, runtime log check, recovery path. | Filesystem access, packaging, signing и distribution требуют approval. | App logs, build/run command, privacy и rollback evidence. |
| `data_migration` | Schema, backfill, sensitive data, retention или production data risk. | Plan migration и rollback до execution. | `migration-plan.md`, `database-dictionary.md`, data quality checks. | Production DB/data access и migration execution требуют approval. | Dry run, backup, validation, owner review, rollback evidence. |
| `security_sensitive_change` | Authn/authz, payment, billing, secrets, PII, abuse controls или permissions. | Threat surface и owner review до build. | `security-risk-review.md`, approval boundary, rollback plan. | Security scans или external security mutations только когда explicitly requested. | Tests, audit logging, rate limit, privacy и owner review evidence. |
| `ci_stabilization` | Failing, flaky или unstable CI. | Gather failure evidence до changing code. | `ci-stabilization-report.md`, failing job, local reproduction. | Remote CI reruns, settings и branch rules требуют approval. | Logs, deterministic/flaky classification, isolation plan, rerun evidence. |
| `release_packaging` | Package, SDK, plugin, app, mobile, desktop или open-source release. | Build release readiness до publish. | `release-readiness.md`, package metadata, changelog, artifacts. | Publishing, tagging, release creation, upload или package registry mutation требуют approval. | Build/test/docs evidence, security/license notes, rollback и owner review. |
| `docs_only` | Documentation update без behavior change. | Update source-backed docs и запуск docs checks. | Source status, affected docs, registry entry когда source-backed claims changed. | Hosted docs, CI activation и sharing changes требуют approval. | `python tools\check_docs.py`, strict MkDocs когда nav/build-sensitive. |
| `standard_feature` | Bounded feature work без special scenario risk. | Используйте normal lifecycle route. | Requirements, plan, test/eval evidence. | Writes follow sandbox и project approval policy. | Unit/integration/contract checks, влияние на docs, review. |
| `professional_code_authoring` | Не механическая работа с кодом, где важна самая маленькая безопасная реализация. | Проверить reuse до custom code. | Coding-standard checklist, existing-capability scan, one-line/native candidate, dependency и legacy-seam decisions. | Выбор route не активирует `hook`, runtime или automation. | Focused tests/evals/review evidence плюс unsupported-claim ledger. |
| `maintenance` | Small upkeep, formatting или status sync. | Keep scope mechanical и evidence explicit. | RUNLOG note или control-plane sync. | Нет unrelated refactor. | Focused command или explicit inspection-only gap. |

## Database & Data Methodology Routing

Database/data work keeps `data_migration` как route name и adds dedicated Database & Data methodology packet когда schema, migration, ORM, warehouse, data quality, lineage, retention, backup/restore или production-data signals appear.

Minimum staged artifacts включают `database-inventory.md`, `database-dictionary.md`, `database-migration-plan.md`, `database-data-contract.md`, `database-backup-restore-evidence.md`, `database-lineage-map.md`, `database-query-performance-review.md`, `database-retention-deletion-policy.md`, `database-synthetic-fixtures-policy.md` и `database-production-access-approval.md` когда production data, production DB access, backup restore или destructive migration является involved.

Approval boundary stays explicit: DB introspection, production DB access, production data access, migration execution, destructive cleanup, backup restore и retention mutation являются не automatic actions.

## Backend Methodology Routing

Backend methodology routing applies когда service behavior, background jobs, queues, auth, error handling, observability, deployment или rollback behavior changes. Minimum staged artifacts включают `backend-service-overview.md`, `backend-runtime-behavior.md`, runtime/failure evidence, observability evidence, security evidence и rollback evidence.

## LLM / AI / RAG Methodology Routing

AI/RAG work keeps `ai_eval_regression` как route name и adds dedicated LLM / AI / RAG methodology packet когда prompts, models, eval configs, structured outputs, tool/function/MCP calls, RAG corpora, retrieval, vector stores, embeddings, grounding, agent traces, guardrails или latency/cost signals appear.

Minimum staged artifacts включают `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-task-packet.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, `ai-cost-latency-budget.md` и existing `ai-eval-spec.md` когда user-visible AI behavior changes. `agent-handoff-contract.md` является legacy/source alias к `agent-task-packet.md`, не duplicate generated contract.

Eval tooling остается conditional: Promptfoo, OpenAI Evals, pytest/Jest app-backed evals, Ragas и LangSmith являются recorded как selected, rejected или deferred choices based на stack/privacy/CI fit. Model migration records snapshot или approved alias, prompt migration impact, compatibility checks, rollback, minimum threshold и sampling parameter rationale. RAG evidence records deletion path, retention, source exclusion, stale-source pruning, privacy owner, vector store lifecycle и deletion propagation. Failed evals, hallucination reports, unsafe outputs, tool misuse или data exposure route к AI incident workflow с severity, mitigation, follow-up eval и Security/Privacy handoff.

AI/RAG route evidence должен reject filename-only diffs как quality proof.

Approval boundary stays explicit: live model calls, external eval services, vector DB access, raw prompts/traces/customer text, tool writes, shell/money/data exposure и irreversible side effects являются не automatic actions.

## API & Integrations Methodology Routing

API & Integrations methodology routing applies когда HTTP APIs, event contracts, webhooks, generated SDKs или external providers change. Minimum staged artifacts включают `api-inventory.md`, `api-contract-review.md`, `api-consumer-map.md`, `api-contract-test-matrix.md`, `external-integration-approval.md` и compatibility/security/error/event/SDK evidence.

External пишет являются не automatic actions; they требуют explicit approval boundary.

## Security, Privacy & Compliance Methodology Routing

Security-sensitive work keeps `security_sensitive_change` как route name и adds dedicated Security, Privacy & Compliance methodology packet когда authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data, policy changes или compliance overlays appear.

Minimum staged artifacts включают `security-risk-review.md`, `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md` и `approval-record.md` когда corresponding risk applies. Source-era names such как `threat-model.md`, `asvs-mapping.md`, `secrets-inventory.md`, `authz-matrix.md`, `audit-log-policy.md` и `compliance-applicability-matrix.md` являются aliases, не duplicate generated contracts.

Codex Security scans остаются explicit opt-in: route may recommend scan или record `not requested`, но это должен не imply который scan ran из security terminology alone. Compliance overlays record applicability, owner, evidence, non-goals, gaps и review cadence без claiming legal compliance или certification.

Approval boundary stays explicit: payment/billing, production data, secret rotation, policy changes, external security-system mutations, external writes, publish actions и Codex Security scans являются не automatic actions.

## Delivery, Release & Operations Methodology Routing

Release packaging keeps `release_packaging` как route name и adds dedicated Delivery, Release & Operations methodology packet когда release, deploy, publish, package, versioning, changelog, artifact, rollout, rollback, CI/CD environment, release mode policy, build-release-run boundary, platform distribution evidence, release communication, versioning tooling, GitHub environment controls, SLO/observability, observability/on-call tooling, runbook, incident, postmortem, DORA, release integrity или automation promotion signals appear.

Minimum staged artifacts включают `versioning-policy.md`, `release-readiness.md`, `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `environment-matrix.md`, `deployment-plan.md`, `ci-cd-workflow-inventory.md`, `observability-map.md`, `slo-spec.md`, `operations-runbook.md`, `incident-record.md`, `postmortem.md`, `post-release-review.md`, `approval-record.md` и `automation-candidate.md` когда automation promotion является proposed.

Approval boundary stays explicit: publish, tag, release creation, artifact upload, deploy, package registry mutation, marketplace/store submission, CI/CD environment mutation и active automation остаются approval_required. Automation candidates требуют manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence и rollback/disable path.

Final release/operations depth also требует owner-reviewed release evidence sufficiency для real risk. Mobile signing, DORA dashboard notes, release tooling config, generated заметки к release или single observability tool остаются `present_unverified` пока platform owner evidence, team/process measurement design, selected/rejected/deferred tooling decisions, alert path и accepted gaps являются recorded.

## Проверка

- Route selection является covered через discovery tests, `usage_mode` fixture checks и false-positive fixtures для selected methodology/tooling gates.
- Scenario behavior является covered через `behavioral-workflows.json` и `run_fixture_eval.py`.
- Frontend methodology routing является covered через `frontend_contract_present` и synthetic `frontend-ui-app` fixture.
- Backend methodology routing является covered через `backend_contract_present` и synthetic `backend-service-app` fixture.
- API & Integrations methodology routing является covered через `api_integrations_contract_present` и synthetic API fixtures.
- Database & Data methodology routing является covered через `database_data_contract_present` и synthetic database fixtures.
- LLM / AI / RAG methodology routing является covered через `llm_ai_rag_contract_present` и synthetic AI/RAG fixtures.
- Security, Privacy & Compliance methodology routing является covered через `security_privacy_compliance_contract_present` и synthetic security fixtures.
- Delivery, Release & Operations methodology routing является covered через `delivery_release_operations_contract_present` и synthetic release fixtures.
- Docs и source claims являются checked через `tools/check_docs.py`, политика источников и strict MkDocs когда navigation changes.
- Completion language должен pass evidence-before-completion: текущий command evidence, текущий eval evidence, текущий runtime evidence, owner evidence или explicit inspection-only gap.

## Риски

- Workspace signals может identify likely scenario но не может prove readiness через themselves.
- A scenario may быть correct while selected minimum artifacts являются low quality; owner review still matters.
- Approval boundaries являются project-specific. Product-Agent OS может mark them, но пользователь или workspace policy decides следует ли к proceed.
- Transcript/session eval runner replays synthetic или redacted session fixtures с deterministic expected/forbidden term checks и privacy/no-secrets guards; semantic judgment still требует reviewer или future calibrated judge coverage.

Следующий artifact: используйте [Behavioral evals](behavioral-evals.md), чтобы проверить, что scenario route resists shortcuts, и [Professional Code Authoring standards](coding-standards.md), чтобы проверить code-writing gates.
