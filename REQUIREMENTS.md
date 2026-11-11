# REQUIREMENTS.md

## PAOS-AUD-G9 — принятое расширение сопровождения

Добавлены T11–T17 в [матрицу G9](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md#расширение-g9-точечное-сопровождение-после-каждой-задачи): после каждой задачи оценивать docs impact, обновлять только основной источник изменившихся сведений и сохранять данные. Владелец принял T10, затем T17 и ограничения проверки модельного поведения; G9 закрыта; детали и критерии находятся в матрице.

## PAOS-AUD-G9 — принятый результат

G8-T14/G8 явно приняты владельцем. G9 T01–T09 реализованы и локально проверены; T10 явно принят владельцем; расширение T11–T17 принято через T17; G9 закрыта. Единый маршрут анализа, выбора, docs/.codex структуры, staging, approval-bound apply и повторного формирования сохраняет существующие данные. [Матрица G9](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md#paos-aud-g9), [evidence и ограничения](research/product-agent-os-g9-execution-report.md). Fresh-session activation отдельно; реальные target/provider/Git действия не входят в выполненный slice.

## PAOS-AUD-G8 — реализация, 2026-11-10

Разрешённый scope: T01–T14 из [матрицы аудита](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md). Контракт: содержательные scoped documents, сохранение заполненного managed content, 40 000 UTF-8 bytes (warning 32 000; stricter wins), lossless proposal/apply/recovery, навигация и provenance. Реальные три проекта остаются read-only. Owner decision T14 и fresh-session activation отдельны; M1 сохраняет собственные source owners. Исторический compatibility block сохранён побайтно в [архиве требований](research/product-agent-os-requirements-history-2026-11-10.md).

Уточнение владельца 10.11.2026: подробные матрицы в `docs/planning/` сохраняются целиком, default 40k size trigger исключён; оглавления/control-plane и explicit per-file limits сохраняют ограничения. Audit matrix в `research/` остаётся целой; split отложен, прежний preview не разрешён. G8-T14 и закрытие G8 явно приняты владельцем; fresh-session activation отдельно.

## Текущий scope Web M1 — 2026-11-10

Дополнение 2026-11-11, 09:25 MSK: один разрешённый native vault roundtrip PAOS-M1-fixture и local synthetic broker auth квалифицированы; fixture удалена. Credential namespace изолирован по canonical profile identity, без legacy/default fallback или миграции существующих записей; старые unresolved default-account runs fail-closed. Реальные ключи/provider/browser и системные политики исключены. Детали в [execution report](research/product-agent-os-web-m1-execution-2026-11-11.md).

Уточнение исполнения 2026-11-11: владелец разрешил непрерывную локальную реализацию по DAG и синтетические native/headless проверки; системные политики, реальные ключи, provider и browser запрещены. Windows MXC write/deny проверен. Local engineering preview не требует commercial AUTH-G1–G6; выпуск остаётся gated PAOS-0046/0030. [Текущий пакет](research/product-agent-os-web-m1-execution-2026-11-11.md) не заменяет SW/UX end-to-end acceptance; M1 пока не закрыта.

Датированный baseline 10 ноября:

Source status: project-authored / implementation started under the approved order.

Owning scope: [PRD §17](research/product-agent-os-web-prd-2026-11-05.md), [архитектура §21](research/product-agent-os-web-architecture-2026-11-05.md), [wireframes v0.7](research/product-agent-os-web-m1-wireframes-2026-11-09.md). [Web-план v0.8](research/product-agent-os-web-task-manager-plan-2026-11-09.md) и [матрица задач](research/product-agent-os-web-task-manager-task-group-2026-11-09.json) владеют последовательностью и task status; revision scope=0.7, execution=0.8.

- M1: одно рабочее окно через Codex App Server; local launch/auth boundary; сессия, чат, связанные задачи, permissions, diff/checks, Stop/recovery; минимальные Task CRUD/доска, read-only каталоги и честный coverage.
- Local data: SQLite + FTS5, транзакционные команды, поиск, backup/restore, staged MD/JSON import и контролируемый cutover. До cutover legacy tasks file-owned; planning MD/JSON этого репозитория не мигрируются данной правкой.
- PAOS-0002 покрывает только M1 profile. Полная иерархия, attachments, linked issues, agent/skill CRUD, редактируемые workflows — M2; цепочки автономного выполнения — M3; PostgreSQL + pgvector — отдельный T1.
- 18 задач M1 / 234 engineering hours — плановая оценка. PAOS-0046 сразу после M1, PAOS-0036 в M2.
- Приёмка M1: матрица M1 DoD в плане, SW-AC-01–10, ST-AC-01–07 в M1 profile, UX-AC-01–18 в M1 slice, DATA-AC-01–05. Документы не закрывают runtime/browser/data acceptance.

Предыдущие Web receipts сохранены в [аудит и архив control-plane](research/product-agent-os-control-plane-maintenance-2026-11-10.md). Далее находятся evidence других направлений и исторические compatibility anchors; они не переопределяют этот scope.



Авторизация 2026-11-11: постоянные границы autonomous local synthetic server/browser/native/delegation по явному запросу владельца хранятся только в AGENTS.md. Для PAOS-0004/PAOS-0040 технические проверки выполняет агент; owner не обязан следовать test script. Native closed-App observation и browser verification различаются, manual rejection не подменяется приёмкой. Provider, реальные ключи, OS-store операции, системные политики и Git остаются исключены; managed controls неизменны.

## PAOS-AUD-G7 — closed / owner accepted, 2026-11-10

G7 T01–T08 owner accepted, локальная группа закрыта. T06 acceptance ограничена synthetic Python/JS; superiority G7 не доказана. Fresh-session activation открыта отдельно; T34 no-go сохраняется. [Evidence](research/product-agent-os-g7-execution-report-2026-11-09.md).

## PAOS-AUD-G6 — 2026-11-09

G6 partially_verified: GAP-06 implemented / owner accepted 10.11.2026; все три synthetic local pilots приняты владельцем. HOST-01 не является их зависимостью. T34 no-go и fresh-session activation HOST-01/HOST-02 остаются открытыми отдельно; manual_only сохраняется. [Результаты](docs/superpowers/specs/paos-aud-g6-pilot-results.json).

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G5 — 2026-11-09

F13/F14/F17: offline installer command contract, явный package entry route, RU/EN parity и актуальный local site. Acceptance: stub commands, docs tests, strict build, routes/links/anchors, Mermaid parse/render. Нет actual install, publication или host activation.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G4 — 2026-11-09

F05/F09/F10/F15: explicit minimal intake без JSON-файла, legacy compatibility receipt, English tests-specific instructions, canonical skill progressive disclosure и измеренное reuse inventory. Нет implicit invocation/cache/host/provider/Git activation; acceptance ограничена local contract/evidence checks.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G3 — 2026-11-09

PAOS-AUD-G3 разрешает локальные F03/F08/F16: строгие RU/EN dates, безопасные registry refs, claim classes; insufficient_evidence при нуле owner labels; current pointer с revision и раздельными task/run/verification/acceptance. Source presence не semantic proof; история и manual/candidate boundaries сохраняются.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G2 — 2026-11-09

PAOS-AUD-G2: разрешены локальные F01/F02/F04. Acceptance: supported MCP wrapper, unsupported отдельно от not_verified, surface-specific minimum, configured/observed model, bounded canonical/cache provenance и trust unknown/observed. Неподтверждённые publisher/URLs оставляют distribution gated; host activation и T30–T34 не входят в этот scope.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G1 — 2026-11-09

PAOS-AUD-G1: запрос владельца разрешает локальную реализацию F06/F12/F11/F07/F18. Acceptance: positive/negative contracts, active/package parity, native rules parser и synthetic merge/ACL tests. Реальные ACL, target apply, trust, hooks/rules activation и G6 host acceptance остаются отдельными границами.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## Session lifecycle isolation — 2026-11-09

`PAOS-SESSION-LIFECYCLE-2026-11-09`: user-authorized repair. Independent chats select their own marker from host session_id; no cross-chat fallback or reset. Preserve native sandbox/approvals, safety patterns, full/concise reporting, freshness and terminal checks. Legacy callers without session identity retain the legacy route. Acceptance and evidence: [owning record](research/product-agent-os-session-lifecycle-fix-2026-11-09.md). M1 wireframes remain documentation-only; Web implementation is not authorized.

<!-- product-agent-os:start requirements -->
Project: Codex Docs / Product-Agent OS
Last compacted: 2026-06-11

## Goal

- Develop Product-Agent OS from an agentic-workflow toolkit into a reproducible engineering operating system for Codex App, CLI and IDE extension.
- Support projects of different complexity through staged artifacts, methodology gates, tests/evals, source policy, approvals and human ownership.
- Keep this file as the compact current-scope layer. Historical ledgers, batch marker banks and detailed evidence belong in source-owned backlog files, `RUNLOG.md`, `prod_test.md` or registry entries.

## Current Scope

- Развивать Product-Agent OS как local engineering operating system; существующий plugin, контроль доказательств и approval boundaries сохраняются.
- На этапе подготовки control-plane согласовали Web M1 по PRD §17 / architecture §21 и очереди v0.8. Текущее состояние исполнения владеет раздел Web M1 выше.
- Поддерживать discovery, staged artifacts, skills, tests/evals и ручное управление решениями. Соблюдать source authority и ограничения из AGENTS.md.
- Состояния Batch 39/42/44/45 и Track 11 учитывать как отдельные направления с собственными evidence owners. Не возобновлять старые очереди автоматически при старте Web.
- Детальные исторические требования перенесены в [аудит и архив control-plane](research/product-agent-os-control-plane-maintenance-2026-11-10.md); критерии исторических пакетов ниже сохранены для трассировки. Они не расширяют M1.

## Current Product-Agent OS State

Исторические записи и результаты ниже относятся к указанным срезам. Они не меняют очередь Web M1 и не являются проверками текущего запуска. При расхождении используются текущие owning artifacts; перенос истории не закрывает оставшиеся gates.


| Area | Current state | Owning evidence |
| --- | --- | --- |
| Task 22 closure | Task 22 final documentation sync closure; Track 1-9 acceptance; legacy Track 9 `Task 23: Final Verification Baseline` is absorbed into Task 22. | Track 9/10 plans and registry |
| Task 23 guided questions | Task 23 guided question protocol and status dashboard; question_queue_contract_present; status_snapshot_present; status_dashboard_present; dashboard_not_source_of_truth; stale_evidence_no_success_claim. | Track 10 backlog and registry |
| Task 24 Batch 12 | `T10-SV-M58..M62`; `agent_skill_metrics_loop`; `timeout_ms: 1200000`; explicit-only. | Track 10 backlog and registry |
| Track 9 and Track 10 history | Source-owned historical context, not active root ledger content. | `docs/sources/product-agent-os-track-9-backlog.md`, `docs/sources/product-agent-os-track-10-backlog.md`, `docs/sources/registry.md` |
| Task 26 Batch 35 | Closed through `T10-LIVE-M41` as `owner_closed_no_op_git_release_pr`; no branch, stage, commit, push or PR was performed. | `docs/sources/product-agent-os-track-10-backlog.md`, `RUNLOG.md` |
| Batch 38 package-source and production-readiness work | Implemented/recorded with preserved historical blockers. `B38-S2` records `plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage`; historical `blocked_pending_explicit_cache_mutation_approval` remains preserved. | `docs/sources/product-agent-os-track-10-backlog.md`, `RUNLOG.md` |
| `B38-PILOT-NF01` | First target-specific docs-only pilot addendum against `Neural_Flow`; target apply remains blocked by `source_policy_status: blocked` and missing target control-plane/source registry artifacts. | `docs/sources/product-agent-os-track-10-backlog.md`, `RUNLOG.md` |
| Batch 39 | Executed through `B39-S5` as local/read-only/contract evidence. `B39-S5` closes source-doc sync, go/no-go and no-unapproved-actions proof as `closed_for_owner_feedback_testing_not_release_ready`: release/distribution is `no_go`, owner-feedback testing is `conditional_go`, and runtime/browser/provider/MCP/git/release/deploy/publish/automation surfaces remain approval-bound. | `PLAN.md`, `TEST.md`, `prod_test.md`, `docs/superpowers/specs/batch39-s5-closure-summary.json` |
| Batch 40 completion-skeptic foundation | B40-S2/S3/S4/S5 closed as local manual foundation, eval hardening, docs/site/source-transfer, synthetic-local pilot ledger, scorecard calibration and go/no-go closure; current promotion status is `manual_only` and `not_promoted`. | `docs/sources/product-agent-os-track-10-backlog.md`, `RUNLOG.md` |
| Batch 42 instruction/tool-use compliance | Historical planned-only baseline with GAP-03 local execution overlay; host M06 remains separate. Source matrix covers Product-Agent OS auto-engagement, skill exposure, implicit invocation policy, route/eval hardening, staged `self-learning-loop`, system-file hygiene triage and closure. | `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`, `docs/sources/product-agent-os-track-10-backlog.md`, `RUNLOG.md` |
| Batch 44 Self-Learning Loop state/trigger/manual progress/feedback/metrics/candidate/docs closure | `B44-S0` through `B44-S6` are implemented as local/schema/fixture/docs evidence. The loop is scoped only to eligible Product-Agent OS projects; due-check state is project-local, default `manual_only`; the manual runner writes progress/HTML only to an explicit stage root; feedback/preferences are privacy-safe summaries only; metrics/evals are append-only/source-backed synthetic contracts only; candidates are review-only and blocked by forbidden-action fixtures; docs/contracts/closure records that automation promotion gate is candidate-only with minimum manual successful runs: 3 and owner approval required before activation. Trigger/cadence/manual-run/feedback/metrics/candidate/docs UX must not imply active scheduling, global session analysis, raw private ingestion, real session import without consent, live eval/provider calls, target mutation, auto-apply, git/release/deploy/publish or external writes. | `docs/superpowers/specs/batch44-self-learning-loop-current-gap-audit.json`, `docs/superpowers/specs/batch44-self-learning-loop-scope-detector-summary.json`, `docs/superpowers/specs/batch44-self-learning-loop-state-trigger-ux-summary.json`, `docs/superpowers/specs/batch44-self-learning-loop-manual-runner-progress-summary.json`, `docs/superpowers/specs/batch44-self-learning-loop-feedback-preferences-summary.json`, `docs/superpowers/specs/batch44-self-learning-loop-metrics-evals-summary.json`, `docs/superpowers/specs/batch44-self-learning-loop-candidate-safety-summary.json`, `docs/superpowers/specs/batch44-self-learning-loop-docs-contracts-closure-summary.json`, `.codex/automation-candidates/self-learning-automation-candidate.md`, `plugins/product-agent-os/scripts/check_self_learning_due.py`, `plugins/product-agent-os/scripts/run_self_learning_loop.py`, `plugins/product-agent-os/scripts/product_agent_os/self_learning_feedback.py`, `plugins/product-agent-os/scripts/product_agent_os/self_learning_metrics.py`, `plugins/product-agent-os/scripts/product_agent_os/self_learning_candidates.py`, `TEST.md`, `RUNLOG.md` |
| Batch 45 Professional Code Authoring | Advisory-only/no-go remains active after T21 strict-schema abort and T22 blocked reviewer decision. `B45-S9` / `B45-CQRR-A01` now owns the planned corrective route T23-T34: executable schema/runtime alignment, compact generation contract, stack/risk-aware test and comment selection, artifact-test debt reduction, deterministic quality/performance metrics, blinded reviewer, representative multi-stack corpus, isolated treatment, local readiness and a separately approved final eval. | `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`, Track 11 plan, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` |
| Track 11 G1.1 documentation toolchain | Active implementation route for project-local docs tooling. `DOC-M35` installed the MkDocs runtime in `.venv-docs/` and passed a strict smoke build under `.docs-tools/reports/`; `DOC-M36` installed Node docs tooling in `.docs-tools/node/` and passed scoped README markdownlint/Prettier smoke; `DOC-M37` installed local Vale `3.15.1` in `.docs-tools/bin/` with advisory Product-Agent OS language rules and smoke evidence; `DOC-M38` installed local lychee `0.24.2` and gitleaks `8.30.0` with scoped fixture smokes; `DOC-M39` vendored Mermaid `10.9.6` under `docs/assets/javascripts/vendor/` and switched MkDocs off the floating CDN asset; `DOC-M40` recorded dependency audit/SBOM governance with Python inventory, `pip check`, Node CycloneDX SBOM generation, current `npm audit` findings and explicit accepted gaps; `DOC-M41` records that Docusaurus, Storybook and Structurizr DSL remain deferred until trigger evidence and owner approval exist. Docs automation, Redocly enforcement, broad docs lint/format, broad Vale enforcement, broad link/secret scans, raw report retention, Python vulnerability audit, dependency remediation, browser Mermaid rendering proof, deferred platform installation and root `site/` freshness remain approval-gated until their own current evidence exists. Product-Agent OS lifecycle hooks are tracked separately through `product_agent_os_LIFECYCLE-HOOKS-A01`. | `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`, `docs/superpowers/specs/documentation-refresh-g1-1-doc-m35-install-summary.json`, `docs/superpowers/specs/documentation-refresh-g1-1-doc-m36-node-tooling-summary.json`, `docs/superpowers/specs/documentation-refresh-g1-1-doc-m37-vale-language-summary.json`, `docs/superpowers/specs/documentation-refresh-g1-1-doc-m38-link-secret-summary.json`, `docs/superpowers/specs/documentation-refresh-g1-1-doc-m39-mermaid-summary.json`, `docs/superpowers/specs/documentation-refresh-g1-1-doc-m40-dependency-audit-summary.json`, `docs/superpowers/specs/documentation-refresh-g1-1-doc-m41-deferred-platform-triggers-summary.json`, `docs/superpowers/specs/product-agent-os-lifecycle-hooks-local-activation-summary.json`, `TEST.md`, `RUNLOG.md` |
| Track 11 G2 first-run cockpit and artifact docs | Implemented as source docs only through `documentation_refresh_G2-A01`: new RU/EN Architecture Intelligence Cockpit page, artifact contracts/gallery first-run atlas, graph/CLI/technical cockpit boundary updates, nav/check_docs/test sync and `DOC_M25_PENDING_SITE_PAGES` routing. Root `site`, search and sitemap freshness remain deferred to final `DOC-M25`; browser/runtime/Cosmos.gl/WebGL/WCAG proof remains unsupported. | `docs/superpowers/specs/documentation-refresh-g2-first-run-cockpit-artifact-docs-summary.json`, `docs/product-agent-os/first-run-architecture-cockpit.md`, `docs/product-agent-os/artifact-contracts.md`, `docs/product-agent-os/artifact-gallery.md`, `docs/product-agent-os/project-code-graph.md`, `docs/product-agent-os/cli-reference.md`, `docs/product-agent-os/technical.md`, `docs/sources/registry.md`, `TEST.md`, `RUNLOG.md` |
| Track 11 G3 diagram atlas and architecture maps | Implemented as source docs only through `documentation_refresh_G3-A01`: new RU/EN diagram pages for source/generated trust boundary, first-run cockpit architecture, evidence/risk lifecycle, skill exposure/invocation boundary and Architecture Intelligence atlas, plus diagram index, nav/check_docs/test sync and `DOC_M25_PENDING_SITE_PAGES` routing. Root `site`, search and sitemap freshness remain deferred to final `DOC-M25`; browser proof remains approval_required and Structurizr DSL remains deferred/uninstalled. | `docs/superpowers/specs/documentation-refresh-g3-diagram-atlas-architecture-maps-summary.json`, `docs/diagrams/source-generated-trust-boundary.md`, `docs/diagrams/first-run-cockpit-architecture.md`, `docs/diagrams/evidence-risk-lifecycle.md`, `docs/diagrams/skill-exposure-and-invocation.md`, `docs/diagrams/architecture-intelligence-diagram-atlas.md`, `docs/sources/registry.md`, `TEST.md`, `RUNLOG.md` |
| Track 11 G4 operator flows and system behavior docs | Implemented as source docs only through `documentation_refresh_G4-A01`: new RU/EN pages for instruction/tool-use compliance, operator command matrix, guided questions/answer ledger and source/cache/active-session state, plus Product-Agent OS index, scenarios, CLI reference, methodology integration map, nav/check_docs/test sync and `DOC_M25_PENDING_SITE_PAGES` routing. Root `site`, search and sitemap freshness remain deferred to final `DOC-M25`; auto-engagement/cache/global config/fresh-session proof remains unsupported. | `docs/superpowers/specs/documentation-refresh-g4-operator-flows-system-behavior-summary.json`, `docs/product-agent-os/instruction-tool-use-compliance.md`, `docs/product-agent-os/operator-command-matrix.md`, `docs/product-agent-os/guided-questions-answer-ledger.md`, `docs/product-agent-os/source-cache-session-state.md`, `docs/product-agent-os/index.md`, `docs/product-agent-os/scenarios.md`, `docs/product-agent-os/cli-reference.md`, `docs/product-agent-os/methodology-intelligence.md`, `docs/sources/registry.md`, `TEST.md`, `RUNLOG.md` |
| Track 11 G5 evidence quality and final site gate docs | Implemented as source docs only through `documentation_refresh_G5-A01`: generated artifact UX, graph intelligence, privacy/supply-chain/report-retention, local HTML interaction and residual follow-up/site-freshness routes now have RU/EN pages, nav/check_docs/test sync, registry markers and `DOC_M25_PENDING_SITE_PAGES` routing. Root `site`, search and sitemap freshness remain deferred to final `DOC-M25`; browser proof, dependency remediation, broad scans and raw report retention remain approval-required. | `docs/superpowers/specs/documentation-refresh-g5-evidence-quality-site-gate-summary.json`, `docs/product-agent-os/generated-artifact-ux-criteria.md`, `docs/product-agent-os/graph-intelligence-contract.md`, `docs/product-agent-os/privacy-supply-chain-retention.md`, `docs/product-agent-os/local-html-interaction-boundary.md`, `docs/product-agent-os/residual-follow-up-site-freshness.md`, `docs/sources/registry.md`, `TEST.md`, `RUNLOG.md` |
| Track 11 DOC-M25 generated site freshness | Implemented through `documentation_refresh_DOC-M25-A01`: root `site`, search and sitemap freshness are current for the former `DOC_M25_PENDING_SITE_PAGES` set after the owner-approved root MkDocs build. Browser proof, broad scans, dependency remediation, raw report retention, publication, release, deploy and git actions remain unsupported/out of scope. | `docs/superpowers/specs/documentation-refresh-doc-m25-site-freshness-summary.json`, `site/`, `site/search/search_index.json`, `site/sitemap.xml`, `docs/sources/registry.md`, `TEST.md`, `RUNLOG.md` |

## Users And Actors

- Owner/user: approves scope, external actions, target workspace mutations, git/release actions and promotion decisions.
- Vibe-coder: receives structured requirements, acceptance behavior, bounded implementation slices, bug-rescue evidence and clear next actions without needing to design the engineering control plane alone.
- AI Engineer / product engineer: receives source-backed architecture, AI/RAG, data, security, eval, operational and release contracts that can be implemented and verified against the target project.
- Codex: performs read-only discovery, staged planning, focused edits, verification and evidence summaries inside the active sandbox and approval model.
- Product-Agent OS skills: provide repeatable routing for requirements, planning, test/eval design, docs maintenance, risk review, completion skepticism and automation promotion.
- Target project maintainers: own any real-project source policy, control-plane artifacts and mutation approval.

## Constraints

- Respond to the user in Russian unless explicitly asked otherwise; keep canonical OpenAI/Codex terms and literal identifiers in English.
- Treat official OpenAI documentation as source of truth for OpenAI, Codex, Agents SDK, API, models, runtime, settings, security and product behavior.
- Treat memory, chat history, generated dashboards, generated reports and project graphs as orientation evidence unless backed by source artifacts or current command/runtime evidence.
- Do not store secrets, private keys, credentials, customer data, raw private chat logs or unredacted PII in prompts, docs, memory, examples, fixtures, evals or reports.
- Do not mutate target workspaces, canonical graph sources, live/provider/external systems, git state, releases, automations or hooks without exact approval for that action.
- Do not install further documentation dependencies, vendor further binaries/minified assets, activate docs hooks/automation, install Docusaurus/Storybook/Structurizr or claim generated `site/` freshness for G1.1 until an approved local-toolchain slice records current install, smoke and build evidence for that specific surface.
- Preserve unrelated dirty work. Do not revert user-authored changes unless explicitly requested and scoped.
- Keep root control-plane files compact:
  - `AGENTS.md`: durable rules and operating boundaries.
  - `REQUIREMENTS.md`: current scope, users, constraints, acceptance and non-goals.
  - `PLAN.md`: current sequencing, rollback and planning pointers.
  - `TEST.md`: current verification gates and escalation rules.
  - `EVALS.md`: subjective/AI/long-horizon rubrics and thresholds.
  - `RUNLOG.md`: current-cycle handoff, latest evidence summary and residual risks.
  - `prod_test.md`: Batch 39 production test attempt/failure/fix/retest ledger.

## Non-Goals

- Do not use this file as a historical changelog, detailed batch backlog, command transcript, generated status report or marker bank.
- Do not promote candidate automation to recurring/live automation until manual success, stable inputs/outputs, eval cases, owner, cadence, sandbox/approval policy, stop condition and rollback/disable path exist.
- Do not treat Batch 39 planning as permission to run browser automation, provider/API calls, target writes, git actions or external mutations.
- Do not resolve `B38-PILOT-NF01` target source-policy blockers inside this repository without target-owner artifacts and explicit approval.


[Preserved source block](research/product-agent-os-requirements-history-2026-11-10.md)
<a id="compatibility-marker-bank"></a>
[Moved section](research/product-agent-os-requirements-history-2026-11-10.md#compatibility-marker-bank)
## Acceptance Criteria

Текущие Web M1 критерии указаны в начале файла. Batch/Track criteria ниже — historical contracts соответствующих пакетов; прежнее ожидание DOC-M25 заменено его датированным closure, не гарантией свежести site после новых правок.

- Root control-plane files remain compact, current and source-routed.
- Batch 45 recovery preserves the research corpus as stack/risk knowledge, generates the smallest safe patch through a compact contract, selects only risk-justified tests/comments/performance evidence, treats warning/coverage/LOC/self-score as diagnostic signals, and blocks any new live eval until executable schema fixtures, seeded-fault checks, blinded review and the frozen multi-stack corpus pass locally.
- Product-Agent OS work names scope, owners, assumptions, acceptance criteria, non-goals, verification gates and residual risks before readiness claims.
- Batch 39 execution is traceable through `prod_test.md`, with each test attempt recording setup, action, evidence, failure/fix/retest status and owner/Codex split.
- Current readiness claims separate supported evidence, unsupported claims, stale evidence, accepted gaps and approval boundaries.
- G1.1 acceptance: root control-plane files name the local docs-toolchain route, folder contract, approval gates, verification commands, eval boundaries and evidence owners before any dependency installation occurs.
- G2 acceptance: first-run cockpit/artifact docs are source/nav/check_docs/test synced, EN counterparts exist and root `site` freshness remains explicitly pending until `DOC-M25`.
- G3 acceptance: diagram atlas pages for source/generated trust boundary, first-run cockpit architecture, evidence/risk lifecycle, skill exposure and Architecture Intelligence are source/nav/check_docs/test synced, EN counterparts exist and search and sitemap freshness remain deferred to final `DOC-M25`.
- G4 acceptance: instruction/tool-use compliance, operator command matrix, guided question/answer ledger, methodology integration map and source/cache/session docs are source/nav/check_docs/test synced, EN counterparts exist and search and sitemap freshness remain deferred to final `DOC-M25`.
- G5 acceptance: generated artifact UX, graph intelligence, privacy/supply-chain/report-retention, local HTML interaction and residual follow-up/site-freshness docs are source/nav/check_docs/test synced, EN counterparts exist and search and sitemap freshness remain deferred to final `DOC-M25`.
- DOC-M25 acceptance: root `site`, search and sitemap freshness are current for G2-G5 source pages after a strict MkDocs build to `site/`, with former `DOC_M25_PENDING_SITE_PAGES` rendered in RU/EN HTML and present in `site/search/search_index.json` and `site/sitemap.xml`.
- Verification for docs/control-plane changes runs:
  - `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`
  - `python tools\check_docs.py`
  - `git diff --check`

## Open Risks

Web M1: PAOS-0054 native-offline compatibility и synthetic migration/restore проверены 11 ноября; native vault/local auth проверены, actual provider/browser/owner acceptance и commercial gates не закрыты. Далее — отдельные риски поддерживаемого plugin/docs scope, не дополнительные задачи M1.

- Batch 39 real-project-adjacent execution is source-owned through `prod_test.md` and S5 closure artifacts. It includes synthetic archetype pilots, read-only `Neural_Flow` / `SOL 0.6` evidence, S4 hardening and S5 conditional owner-feedback closure. Target writes, runtime/browser/provider/model/vector/eval/live-database/migration/production-data/git/external actions and any broader target execution still require exact approval.
- `B38-PILOT-NF01` remains blocked for target apply by missing target control-plane/source registry artifacts and `source_policy_status: blocked`.
- Batch 40 completion-skeptic automation remains `manual_only` and `not_promoted`.
- Batch 42: историческая planning matrix дополнена GAP-03 local execution overlay; provenance/metadata/routing проверялись локально, M06 host receipt остаётся отдельным gate. Локальные проверки не доказывают auto-engagement во всех Codex surfaces. Owner: research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md и batch42 matrix.
- Track 11 G1.1 is a project-local docs-toolchain route. `DOC-M35`, `DOC-M36`, `DOC-M37`, `DOC-M38`, `DOC-M39`, `DOC-M40` and `DOC-M41` have evidence for `.venv-docs/`, `.docs-tools/node/`, local Vale language guards, local lychee/gitleaks fixture checks, vendored Mermaid runtime wiring, local dependency inventory, Node CycloneDX SBOM generation, current Node advisory counts and deferred platform trigger governance. Docusaurus, Storybook and Structurizr DSL remain deferred until concrete trigger evidence exists. Generated root `site` freshness, Python vulnerability audit, complete repository SBOM, dependency remediation, browser Mermaid rendering proof, broad lint/format enforcement, broad Vale enforcement, external URL crawling, broad link/secret scans, raw report retention and deferred platform install/runtime proof remain unclaimed until their specific slices run. Product-Agent OS lifecycle hooks are project-local and owner-approved, but Codex hook trust review / fresh-session execution is still not claimed.
- Track 11 G2–G5: прежнее ожидание финального DOC-M25 снято его датированным receipt; свежесть site после последующих изменений и browser/Cosmos.gl/WebGL proof этим не подтверждаются. Auto-engagement, cache/global changes, broad scans, dependency remediation, deferred platform installs и publication требуют своих evidence/authority.
- Track 11 DOC-M25 now closes only generated root `site`/search/sitemap freshness through `documentation_refresh_DOC-M25-A01`; it does not prove browser behavior, publication, release readiness, dependency remediation, raw report retention, target mutation, provider/API behavior, automation or git/release actions.
- Historical evidence is intentionally source-owned outside this file; use the registry/backlogs before making broad historical claims.

<!-- product-agent-os:end requirements -->

## Documentation refresh scope — 2026-11-03

Owner-authorized task `PAOS-DOCS-REFRESH-2026-11-03` applies the 20-item documentation audit. Acceptance: current source-backed guidance, syntactically valid examples, semantic RU/EN parity, model/runtime applicability, explicit implementation gaps and passing applicable local checks. Scope includes the detailed plan pair, task-group status, guides, navigation, source registries and control-plane evidence. No model switch, permission/config/profile change, executable template/runtime/hook edit, provider/model call, browser, publication or Git action. Historical evidence and the pre-existing 17 dirty config/profile/eval files remain intact. Docs-inventory test metadata may change solely to account for the three new page pairs; assertions and historical site counters remain intact. Detailed acceptance: [refresh plan](docs/superpowers/plans/2026-11-03-gpt6-documentation-refresh.md).
