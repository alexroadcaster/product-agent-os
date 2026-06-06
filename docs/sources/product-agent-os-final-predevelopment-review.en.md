# Product-Agent OS: final pre-development review

Source status: `implementation planning + critical review`

Date: **2026-05-23**.
Based on the [Track 8 detailed backlog](product-agent-os-track-8-detailed-backlog.md), the [gap matrix](development-methodology-gap-matrix.md), Track 6/7 implementation notes and scenario review of Product-Agent OS.

## Final critical review

The Product-Agent OS idea is strong: the plugin turns Codex from a local task executor into a governed engineering operating layer. Its main value is not that the plugin knows OpenAPI, Docusaurus, DBML or Storybook, but that it can understand project context, choose applicable standards, create staged artifacts, connect work to tests/evals/docs and avoid dangerous external actions without approval.

Strengths of the current backlog:

- Clear separation of concerns: methodologies, standards/specs, documentation tooling, discovery, readiness gates, lifecycle skills and verification.
- A staged-first safety model: the plugin proposes artifacts and checks, but does not silently enable CI, hooks, hosted docs, DB introspection or automations.
- Applicability statuses instead of a primitive `present/missing` model, so Docusaurus, PlantUML, DBML, Storybook and similar tools do not become dogma.
- Scenario workflows for three important entry points: bug rescue, greenfield idea and complex system acceleration.
- A test-first implementation plan: new behavior changes must start with failing tests.

Critical risks before implementation:

| Risk | Why it is dangerous | How to close it in the backlog |
| --- | --- | --- |
| Artifact explosion | The user may receive too many files and lose momentum. | Introduce a per-mode minimum artifact set and progressive disclosure: minimum first, then advanced proposals. |
| False confidence | A template can look like quality even when runtime verification has not run. | Distinguish `present_unverified` from `present_verified` everywhere; final responses must require command evidence. |
| Over-governance | The plugin may start requiring enterprise artifacts for a small MVP. | Use applicability statuses, lightweight mode and `not_applicable` with a reason. |
| Mode ambiguity | One project can be bug rescue, complex system and security-sensitive at the same time. | Introduce `usage_mode.primary`, `usage_mode.secondary`, confidence and routing reasons. |
| Tool detection false positives | A `domain/` folder, `.stories.*` files or `docs/` do not prove mature methodology. | Discovery must distinguish signal presence, maturity evidence and verification command. |
| Secrets/data exposure | DB docs, integrations, env examples and logs may contain secrets or customer data. | Use secrets-safe inspection rules, redaction fields and approval gates for DB/external systems. |
| Weak user experience | If the plugin dumps every gate in the first response, the user will leave. | Use a scenario-specific first response and a short mode summary: what I found, what I need, next smallest step. |
| Missing plugin success metrics | There is no way to know whether the plugin makes work materially faster or better. | Add a metric spec for the plugin itself: time-to-first-useful-artifact, false positive gate rate and rescue resolution rate. |
| Runtime diversity | Web/API are covered better than mobile, desktop, CI, security, release and legacy onboarding. | Add 10 additional usage scenarios and fixture coverage. |
| Apply path ambiguity | Staging exists, but the user needs a clear path from proposal to approved apply. | Explicitly state the approval/apply/rollback boundary in every scenario workflow. |

Final conclusion: Track 8 is ready for implementation only after the scenario matrix is expanded. Methodologies and tooling are already organized well, but the plugin must be tested against typical real-life situations, not only against a list of standards.

### Addendum: behavioral evals and Codex-only scope

After comparative analysis of [`obra/superpowers`](https://github.com/obra/superpowers), the backlog needs behavioral workflow evals inside the Codex-only scope, not multi-harness adapters. Product-Agent OS must verify correct plugin behavior in Codex App, CLI, IDE extension and `.codex-plugin`: route selection, first response, shortcut resistance, root-cause bug rescue, no-placeholder plans, two-stage review, fresh-context handoffs and finish options.

Constraint: ideas from Superpowers are used as community/opensource intake, not as a source of truth. Product-Agent OS must not add mandatory Claude/Cursor/OpenCode/Gemini adapters, aggressive always-on hooks or unconditional skill triggers. Any session-start/bootstrap logic remains a staged, approval-bound Codex hook proposal.

## 10 additional plugin usage scenarios

### 1. PR review before merge

Context: a developer opened a PR and wants to quickly check risks before review.

Plugin:

1. Audits the diff/changed files.
2. Classifies the mode as `pr_review`.
3. Builds a risk map: behavior, API, DB, UI, security, docs, release impact.
4. Checks acceptance scenarios and tests/evals coverage.
5. If an API is touched, requires an OpenAPI/AsyncAPI update or explicit gap.
6. If a public contract exists, requires changelog/SemVer impact.
7. Returns a review packet: findings, missing checks, commands to run, docs impact, release risk.

### 2. Legacy repo onboarding and documentation debt

Context: a team received an old repository with no current documentation.

Plugin:

1. Performs a read-only inventory.
2. Classifies the mode as `legacy_onboarding`.
3. Builds a system map: entry points, services, scripts, tests, config, docs, known risks.
4. Does not try to rewrite code immediately.
5. Creates a staged `onboarding-map.md`: how to run, where architecture boundaries are, where the source of truth is missing.
6. Proposes a minimum docs set: README, architecture overview, runbook, docs tooling decision.
7. Marks claims as `present_unverified` until commands have been run.

### 3. API contract migration

Context: an HTTP API must be changed or versioned.

Plugin:

1. Classifies the mode as `api_migration`.
2. Finds OpenAPI/Swagger tooling, generated clients, consumers and integration tests.
3. Creates a migration plan: backward compatibility, breaking changes, deprecation, examples, auth/errors.
4. Updates the API contract proposal before code.
5. Requires contract tests and client impact review.
6. Adds release/version impact and a changelog section.

### 4. AI/RAG quality regression

Context: an AI feature started answering worse, retrieval is wrong or hallucination risk increased.

Plugin:

1. Classifies the mode as `ai_eval_regression`.
2. Does not edit the prompt blindly.
3. Creates/updates `ai-eval-spec.md`: dataset, baseline, rubric, thresholds, no-secrets policy.
4. Runs or proposes an eval command.
5. Changes only one factor per cycle: prompt, retrieval, reranker, chunking, model or tool.
6. Compares baseline vs new result and logs residual risk.

### 5. Mobile/native feature with permissions and offline states

Context: a feature must be added to an iOS/Android/native app.

Plugin:

1. Classifies the mode as `native_mobile_feature`.
2. Checks platform build commands, simulator/emulator assumptions, permissions, offline states and screenshots/logs.
3. Creates acceptance scenarios for flows and permission states.
4. Requires runtime verification beyond code inspection.
5. The docs tooling selector does not force web tooling unless shared docs exist.

### 6. Desktop/local-first app with filesystem and background jobs

Context: a desktop app works with a local DB, filesystem, indexer or background tasks.

Plugin:

1. Classifies the mode as `desktop_local_first`.
2. Builds a risk map: filesystem permissions, local DB migration, indexing, privacy, long-running work, app logs.
3. Creates architecture boundary and data protection notes.
4. Requires a runtime check: app launch, logs, sample file path, rollback of local data migration.
5. Documentation records user data handling and recovery path.

### 7. Database migration and data model change

Context: schema, migration, retention, backfill or a critical query changes.

Plugin:

1. Classifies the mode as `data_migration`.
2. Requires a migration plan before implementation.
3. Updates the database dictionary/DBML proposal.
4. Checks PII/sensitive fields, retention, backfill, rollback and data quality checks.
5. Does not run DB introspection or production DB commands without approval.

### 8. Security/auth/payment-sensitive change

Context: auth, permissions, payments, secrets, personal data or external writes are affected.

Plugin:

1. Classifies the mode as `security_sensitive_change`.
2. Strengthens the reasoning/review path and stop conditions.
3. Creates a security risk review: threat surface, authz/authn, sensitive fields, abuse controls, rollback.
4. Requires explicit approval for external writes and secret-sensitive operations.
5. Does not store secrets in artifacts.

### 9. CI stabilization and flaky tests

Context: CI fails intermittently, tests are flaky or the build pipeline is unreliable.

Plugin:

1. Classifies the mode as `ci_stabilization`.
2. Collects failure evidence: job, command, logs, timing, environment.
3. Separates deterministic failures from flaky symptoms.
4. Proposes the smallest isolation plan: reproduce locally, narrow the test, stabilize dependency/time/network assumptions.
5. Does not change GitHub Actions settings without approval.

### 10. Package, SDK, plugin or open-source release

Context: a public release artifact must be prepared.

Plugin:

1. Classifies the mode as `release_packaging`.
2. Checks public API, SemVer impact, changelog, docs, examples, package metadata and license/security notes.
3. Requires tests/build/docs evidence.
4. Prepares a release packet and rollback notes.
5. Does not publish a package/release/tag without explicit approval.

## What must be added to the backlog

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
