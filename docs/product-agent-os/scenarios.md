# Product-Agent OS scenarios

Source status: `official + experiment`  
Источники: [Codex workflows](https://developers.openai.com/codex/workflows), [Codex use cases](https://developers.openai.com/codex/use-cases), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Product-Agent OS plugin](index.md), [Behavioral evals](behavioral-evals.md), [Codex compatibility](codex-compatibility.md).

Эта страница отвечает на практический вопрос: какой route должен выбрать Product-Agent OS plugin, когда Codex App, CLI или IDE extension видит реальный workspace и пользователь просит не просто "написать код", а довести работу до проверяемого результата.

Сценарий не заменяет lifecycle. Он выбирает первый малый шаг, minimum artifacts, approval boundary и verification gates. Если evidence нет, route должен вернуть gap, а не готовность.

## Inputs

- цель пользователя или `intent_hint`, если он передан в Codex runtime runner;
- read-only workspace audit: файлы, stack, test/build commands, docs, CI, contracts, control-plane files;
- текущие `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- source policy, sandbox, approvals и known external-system boundaries;
- предыдущие failure notes, если они уже записаны в `RUNLOG.md`.

## Outputs

- `usage_mode.primary`, `secondary`, confidence и routing reasons;
- first response: один ближайший полезный шаг без широкого scaffold, rewrite или external mutation;
- minimum artifacts: конкретные файлы или packets, которые нужны до build/review/release;
- approval boundary: что можно делать read-only или staged-only, а что требует explicit approval;
- verification gates: команды, evals, screenshots, logs, owner review или accepted gap;
- residual risk, если route основан на detection, а не на verified evidence.

## Scenario Matrix

| usage_mode | When it applies | first response | minimum artifacts | approval boundary | verification gates |
| --- | --- | --- | --- | --- | --- |
| `first-run-intake` | Empty workspace, broken verification, existing control-plane or complex first launch. | Name mode, confidence, next smallest action and evidence gaps. | Intake summary, current lifecycle state, next action. | No scaffold, broad fix or parallel work before route is accepted. | Read-only audit, control-plane check, source policy. |
| `bug_rescue` | User reports broken behavior, failing tests or regression. | Reproduce or isolate before changing code. | `bug-rescue-report.md`, failure evidence, root-cause hypothesis. | No fix claim without reproduction evidence. | Failing command/log, focused regression check, current evidence. |
| `greenfield_idea` | Idea-stage or empty product direction. | Shape one vertical slice before scaffold. | `greenfield-idea-brief.md`, selected direction, non-goals. | Scaffold requires explicit approval. | Acceptance scenarios, first slice plan, lightweight-mode decision. |
| `complex_system_acceleration` | Existing multi-surface app, integrations, multiple services or unclear ownership. | Build map before parallelization. | `integration-catalog.md`, ownership split, release gates. | No parallel work with overlapping files or unclear external-system owners. | Integration inventory, ownership review, release risk gates. |
| `pr_review` | Review or merge-readiness request. | Stay read-only and review changed files. | PR review readiness, changed-files map, `pr-risk-review.md`. | No push, PR creation, merge or external comment without approval. | Two-stage review: spec compliance before quality/risk. |
| `legacy_onboarding` | Old, undocumented or unknown repository. | Orient before refactor. | `onboarding-map.md`, entry points, run commands, docs debt. | No cleanup/refactor until map and verification status are explicit. | Present-unverified labels, source map, run command evidence. |
| `api_migration` | HTTP API, event contract, generated client or consumer change. | Plan compatibility before implementation. | `migration-plan.md`, `api-contract-review.md`, consumers, rollout. | Release or breaking change needs owner review and approval. | Contract check, backward compatibility, deprecation and rollout evidence. |
| `ai_eval_regression` | AI/RAG quality, prompt, model, retrieval, dataset or judge changes. | Baseline first. | `ai-eval-spec.md`, dataset policy, rubric, thresholds. | No quality claim from inspection-only evidence. | Baseline, rerun command, latency/cost/grounding and failure examples. |
| `native_mobile_feature` | iOS, Android or native mobile behavior. | Record platform assumptions before implementation. | Platform runtime check, permissions, offline/device plan. | Permission, signing or store changes require approval. | Build command, simulator/emulator or device logs, screenshots, manual gap. |
| `desktop_local_first` | Desktop app, filesystem, local DB, indexing or packaging. | Map local data and OS assumptions first. | Local data risk note, runtime log check, recovery path. | Filesystem access, packaging, signing and distribution require approval. | App logs, build/run command, privacy and rollback evidence. |
| `data_migration` | Schema, backfill, sensitive data, retention or production data risk. | Plan migration and rollback before execution. | `migration-plan.md`, `database-dictionary.md`, data quality checks. | Production DB/data access and migration execution require approval. | Dry run, backup, validation, owner review, rollback evidence. |
| `security_sensitive_change` | Authn/authz, payment, billing, secrets, PII, abuse controls or permissions. | Threat surface and owner review before build. | `security-risk-review.md`, approval boundary, rollback plan. | Security scans or external security mutations only when explicitly requested. | Tests, audit logging, rate limit, privacy and owner review evidence. |
| `ci_stabilization` | Failing, flaky or unstable CI. | Gather failure evidence before changing code. | `ci-stabilization-report.md`, failing job, local reproduction. | Remote CI reruns, settings and branch rules require approval. | Logs, deterministic/flaky classification, isolation plan, rerun evidence. |
| `release_packaging` | Package, SDK, plugin, app, mobile, desktop or open-source release. | Build release readiness before publish. | `release-readiness.md`, package metadata, changelog, artifacts. | Publishing, tagging, release creation, upload or package registry mutation require approval. | Build/test/docs evidence, security/license notes, rollback and owner review. |
| `docs_only` | Documentation update without behavior change. | Update source-backed docs and run docs checks. | Source status, affected docs, registry entry when source-backed claims changed. | Hosted docs, CI activation and sharing changes require approval. | `python tools\check_docs.py`, strict MkDocs when nav/build-sensitive. |
| `standard_feature` | Bounded feature work without special scenario risk. | Use normal lifecycle route. | Requirements, plan, test/eval evidence. | Writes follow sandbox and project approval policy. | Unit/integration/contract checks, docs impact, review. |
| `maintenance` | Small upkeep, formatting or status sync. | Keep scope mechanical and evidence explicit. | RUNLOG note or control-plane sync. | No unrelated refactor. | Focused command or explicit inspection-only gap. |

## Database & Data methodology routing

Database/data work keeps the Track 8 `data_migration` route for compatibility, but Track 9 also adds a dedicated Database & Data methodology packet. When schema, migration, ORM, warehouse, data quality, lineage, retention, backup/restore or production-data signals appear, the route should stage or request database-specific evidence before implementation or execution.

Minimum staged artifacts include `database-inventory.md`, `database-dictionary.md`, `database-migration-plan.md`, `database-data-contract.md`, `database-backup-restore-evidence.md`, `database-lineage-map.md`, `database-query-performance-review.md`, `database-retention-deletion-policy.md`, `database-synthetic-fixtures-policy.md` and `database-production-access-approval.md` when production data, production DB access, backup restore or destructive migration is involved.

Approval boundary stays explicit: DB introspection, production DB access, production data access, migration execution, destructive cleanup, backup restore and retention mutation are not automatic actions.

## Verification

- Route selection is covered by discovery tests, `usage_mode` fixture checks, and T8-GX false-positive fixtures for selected methodology/tooling gates.
- Scenario behavior is covered by `behavioral-workflows.json` and `run_fixture_eval.py`.
- Frontend methodology routing is covered by `frontend_contract_present` and the synthetic `frontend-ui-app` fixture: UI completion requires user-flow, component state, visual/accessibility/runtime/interaction evidence or an accepted gap, not Storybook-only or inspection-only evidence.
- Backend methodology routing is covered by `backend_contract_present` and the synthetic `backend-service-app` fixture: backend completion requires `backend-service-overview.md`, `backend-runtime-behavior.md`, runtime/failure evidence, observability/SLO/health evidence, security/rollback evidence and owner reviewed sufficiency or accepted gap, not package docs or logs-only evidence.
- API & Integrations methodology routing is covered by `api_integrations_contract_present` and synthetic API fixtures: API completion requires `api-inventory.md`, `api-contract-review.md`, `api-consumer-map.md`, `api-contract-test-matrix.md`, `external-integration-approval.md` and related compatibility/security/error/event/SDK evidence, not Swagger UI or schema-only evidence.
- Database & Data methodology routing is covered by `database_data_contract_present` and synthetic database fixtures: database completion requires inventory, dictionary, schema source, migration plan, expand-contract, data contract, rollback/backup, classification, data quality, lineage, performance, retention, synthetic fixtures and production access approval evidence where applicable.
- Docs and source claims are checked by `tools/check_docs.py`, source policy and strict MkDocs when navigation changes.
- Completion language must pass evidence-before-completion: current command evidence, current eval evidence, current runtime evidence, owner evidence or explicit inspection-only gap.

## Risks

- Workspace signals can identify a likely scenario but cannot prove readiness by themselves.
- A scenario may be correct while the selected minimum artifacts are low quality; owner review still matters.
- Approval boundaries are project-specific. Product-Agent OS can mark them, but the user or workspace policy decides whether to proceed.
- Transcript/session eval runner now replays synthetic or redacted session fixtures with deterministic expected/forbidden term checks and privacy/no-secrets guards; semantic judgment still needs reviewer or future calibrated judge coverage.

Next artifact: use [Behavioral evals](behavioral-evals.md) to validate that the scenario route resists shortcuts and produces the expected evidence.
