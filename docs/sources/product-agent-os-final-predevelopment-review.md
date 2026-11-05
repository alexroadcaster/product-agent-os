---
title: "Архив — Product-Agent OS: финальный pre-development review"
---

# Архив — Product-Agent OS: финальный pre-development review {#product-agent-os-pre-development-review}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

Source status: `implementation planning + critical review`

Дата: **2026-05-23**.  
Основано на [Track 8 detailed backlog](product-agent-os-track-8-detailed-backlog.md), [gap matrix](development-methodology-gap-matrix.md), Track 6/7 implementation notes и сценарной проверке Product-Agent OS.

## Финальный критический анализ идеи

Идея Product-Agent OS сильная: plugin превращает Codex из исполнителя локальных задач в управляемую engineering operating layer. Главная ценность не в том, что plugin знает OpenAPI, Docusaurus, DBML или Storybook, а в том, что он умеет понять контекст проекта, выбрать применимые стандарты, создать staged artifacts, связать работу с tests/evals/docs и не активировать опасные внешние действия без approval.

Сильные стороны текущего backlog:

- Есть separation of concerns: methodologies, standards/specs, documentation tooling, discovery, readiness gates, lifecycle skills, verification.
- Есть staged-first safety model: plugin предлагает artifacts и checks, но не включает CI, hooks, hosted docs, DB introspection или automations молча.
- Есть applicability statuses вместо примитивного `present/missing`, поэтому Docusaurus, PlantUML, DBML, Storybook и другие инструменты не становятся dogma.
- Есть scenario workflows для трех наиболее важных входов: bug rescue, greenfield idea, complex system acceleration.
- Есть test-first implementation plan: новые behavior changes должны начинаться с failing tests.

Критические риски перед разработкой:

| Risk | Почему опасно | Как закрывать в backlog |
| --- | --- | --- |
| Artifact explosion | Пользователь может получить слишком много файлов и потерять momentum. | Ввести per-mode minimum artifact set и progressive disclosure: сначала минимум, затем advanced proposals. |
| False confidence | Наличие template может выглядеть как качество, хотя runtime verification не запускалась. | Везде разделять `present_unverified` и `present_verified`; финальные ответы должны требовать command evidence. |
| Over-governance | Plugin может начать требовать enterprise-артефакты для маленького MVP. | Applicability statuses, lightweight mode, `not_applicable` с reason. |
| Mode ambiguity | Один проект может быть одновременно bug rescue, complex system и security-sensitive. | Ввести `usage_mode.primary`, `usage_mode.secondary`, confidence и routing reasons. |
| Tool detection false positives | `domain/` folder, `.stories.*` или `docs/` не доказывают зрелую методологию. | Discovery должен различать signal presence, maturity evidence и verification command. |
| Secrets/data exposure | DB docs, integrations, env examples and logs могут содержать secrets/customer data. | Secrets-safe inspection rules, redaction fields, approval gates for DB/external systems. |
| Weak user experience | Если plugin первым сообщением вывалит все gates, пользователь уйдет. | Scenario-specific first response и short mode summary: what I found, what I need, next smallest step. |
| Missing plugin success metrics | Нельзя понять, делает ли plugin реально быстрее и качественнее. | Добавить metric spec для самого plugin: time-to-first-useful-artifact, false positive gate rate, rescue resolution rate. |
| Runtime diversity | Web/API покрыты лучше, чем mobile, desktop, CI, security, release and legacy onboarding. | Добавить 10 дополнительных usage scenarios и fixture coverage. |
| Apply path ambiguity | Staging уже есть, но пользователю нужен понятный путь от proposal к approved apply. | В каждом scenario workflow явно указать approval/apply/rollback boundary. |

Финальный вывод: Track 8 готов к разработке только после расширения сценарной матрицы. Методологии и tooling уже разложены хорошо, но plugin должен быть проверен на типовых жизненных ситуациях, а не только на списке стандартов.

### Addendum: behavioral evals and Codex-only scope

После сравнительного анализа [`obra/superpowers`](https://github.com/obra/superpowers) backlog требует не multi-harness adapters, а behavioral workflow evals внутри Codex-only scope. Product-Agent OS должен проверять правильное поведение plugin в Codex App, CLI, IDE extension и `.codex-plugin`: route selection, first response, shortcut resistance, root-cause bug rescue, no-placeholder plans, two-stage review, fresh-context handoffs and finish options.

Ограничение: идеи из Superpowers используются как community/opensource intake, а не как source of truth. Product-Agent OS не должен добавлять обязательные Claude/Cursor/OpenCode/Gemini adapters, aggressive always-on hooks или unconditional skill triggers. Любая session-start/bootstrap логика остается staged/approval-bound Codex hook proposal.

## Еще 10 сценариев применения plugin

### 1. PR review before merge

Контекст: разработчик открыл PR, но хочет быстро проверить риски перед review.

Plugin:

1. Делает audit diff/changed files.
2. Классифицирует режим как `pr_review`.
3. Строит risk map: behavior, API, DB, UI, security, docs, release impact.
4. Проверяет acceptance scenarios and tests/evals coverage.
5. Если затронут API, требует OpenAPI/AsyncAPI update или explicit gap.
6. Если есть public contract, требует changelog/SemVer impact.
7. Возвращает review packet: findings, missing checks, commands to run, docs impact, release risk.

### 2. Legacy repo onboarding and documentation debt

Контекст: команда получила старый repo без актуальной документации.

Plugin:

1. Делает read-only inventory.
2. Классифицирует режим как `legacy_onboarding`.
3. Строит system map: entrypoints, services, scripts, tests, config, docs, known risks.
4. Не пытается сразу переписывать код.
5. Создает staged `onboarding-map.md`: как запустить, где архитектурные границы, где отсутствует source of truth.
6. Предлагает minimum docs set: README, architecture overview, runbook, docs tooling decision.
7. Помечает claims как `present_unverified`, пока commands не запускались.

### 3. API contract migration

Контекст: нужно изменить или версионировать HTTP API.

Plugin:

1. Классифицирует режим как `api_migration`.
2. Находит OpenAPI/Swagger tooling, generated clients, consumers, integration tests.
3. Создает migration plan: backward compatibility, breaking changes, deprecation, examples, auth/errors.
4. Обновляет API contract proposal before code.
5. Требует contract tests and client impact review.
6. Добавляет release/version impact and changelog section.

### 4. AI/RAG quality regression

Контекст: AI feature стала хуже отвечать, retrieval ошибается или вырос hallucination risk.

Plugin:

1. Классифицирует режим как `ai_eval_regression`.
2. Не правит prompt вслепую.
3. Создает/обновляет `ai-eval-spec.md`: dataset, baseline, rubric, thresholds, no-secrets policy.
4. Запускает или предлагает eval command.
5. Меняет только один фактор за цикл: prompt, retrieval, reranker, chunking, model или tool.
6. Сравнивает baseline vs new result and logs residual risk.

### 5. Mobile/native feature with permissions and offline states

Контекст: нужно добавить feature в iOS/Android/native app.

Plugin:

1. Классифицирует режим как `native_mobile_feature`.
2. Проверяет platform build commands, simulator/emulator assumptions, permissions, offline states, screenshots/logs.
3. Создает acceptance scenarios for flows and permission states.
4. Требует runtime verification beyond code inspection.
5. Docs tooling selector не навязывает web tooling unless shared docs exist.

### 6. Desktop/local-first app with filesystem and background jobs

Контекст: desktop app работает с local DB, файловой системой, индексатором или background tasks.

Plugin:

1. Классифицирует режим как `desktop_local_first`.
2. Карта рисков: filesystem permissions, local DB migration, indexing, privacy, long-running work, app logs.
3. Создает architecture boundary and data protection notes.
4. Требует runtime check: app launch, logs, sample file path, rollback of local data migration.
5. Документация фиксирует user data handling and recovery path.

### 7. Database migration and data model change

Контекст: меняется schema, migration, retention, backfill или critical query.

Plugin:

1. Классифицирует режим как `data_migration`.
2. Требует migration plan before implementation.
3. Обновляет database dictionary/DBML proposal.
4. Проверяет PII/sensitive fields, retention, backfill, rollback, data quality checks.
5. Не запускает DB introspection или production DB commands без approval.

### 8. Security/auth/payment-sensitive change

Контекст: затрагиваются auth, permissions, payments, secrets, personal data или external writes.

Plugin:

1. Классифицирует режим как `security_sensitive_change`.
2. Усиливает reasoning/review path and stop conditions.
3. Создает security risk review: threat surface, authz/authn, sensitive fields, abuse controls, rollback.
4. Требует explicit approval for external writes and secret-sensitive operations.
5. Не сохраняет secrets in artifacts.

### 9. CI stabilization and flaky tests

Контекст: CI падает нестабильно, tests flaky, build pipeline unreliable.

Plugin:

1. Классифицирует режим как `ci_stabilization`.
2. Собирает failure evidence: job, command, logs, timing, environment.
3. Разделяет deterministic failures and flaky symptoms.
4. Предлагает smallest isolation plan: reproduce locally, narrow test, stabilize dependency/time/network assumptions.
5. Не меняет GitHub Actions settings без approval.

### 10. Package, SDK, plugin or open-source release

Контекст: нужно подготовить release public artifact.

Plugin:

1. Классифицирует режим как `release_packaging`.
2. Проверяет public API, SemVer impact, changelog, docs, examples, package metadata, license/security notes.
3. Требует tests/build/docs evidence.
4. Готовит release packet and rollback notes.
5. Не публикует package/release/tag без explicit approval.

## Что нужно добавить в backlog

| Category | Additions |
| --- | --- |
| Usage modes | `pr_review`, `legacy_onboarding`, `api_migration`, `ai_eval_regression`, `native_mobile_feature`, `desktop_local_first`, `data_migration`, `security_sensitive_change`, `ci_stabilization`, `release_packaging`. |
| Mode model | `usage_mode.primary`, `usage_mode.secondary`, confidence, reasons, fallback mode. |
| Workflow templates | PR review, legacy onboarding, API migration, AI eval regression, native/mobile feature, desktop/local-first, data migration, security-sensitive change, CI stabilization, release packaging. |
| Artifact templates | `onboarding-map.md`, `migration-plan.md`, `security-risk-review.md`, `ci-stabilization-report.md`, `release-readiness.md`. |
| Readiness gates | PR risk review, migration plan, security review, native/desktop runtime verification, CI evidence, release readiness, plugin success metrics. |
| Fixtures | Synthetic fixture workspace for each scenario, with no secrets and no private customer data. |
| UX | Scenario-specific first response and minimum artifact set per mode. |

## Development readiness decision

Before code work begins, backlog should be expanded one final time with the rows above. After that, implementation should start with failing tests for:

1. usage mode classification;
2. per-mode minimum artifacts;
3. scenario workflow template registration;
4. conditional readiness gates;
5. fixture eval for representative workspaces.
