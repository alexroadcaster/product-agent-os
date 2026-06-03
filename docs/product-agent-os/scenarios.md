# Product-Agent OS scenarios

Source status: `official + experiment`

Источники: [Codex workflows](https://developers.openai.com/codex/workflows), [Codex use cases](https://developers.openai.com/codex/use-cases), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Product-Agent OS plugin](index.md), [Behavioral evals](behavioral-evals.md), [Codex compatibility](codex-compatibility.md).

Эта страница отвечает на практический вопрос: какой route должен выбрать Product-Agent OS plugin, когда Codex App, CLI или IDE extension видит реальный workspace и пользователь просит не просто "написать код", а довести работу до проверяемого результата.

Scenario не заменяет lifecycle. Он выбирает первый малый шаг, minimum artifacts, approval boundary и verification gates. Если evidence нет, route должен вернуть gap, а не готовность.

## Operator Route Map

Scenarios are route decisions, not permission to run live systems. Each route must name source context, expected evidence, approval boundary and stop condition before it hands work to a subagent, skill or implementation slice.

| Route | Когда выбирать | Minimum evidence | Stop condition |
| --- | --- | --- | --- |
| `code_graph_orientation` | Нужно понять code/docs topology before build or review. | Existing source files plus generated graph/cockpit packet labeled as orientation evidence. | Do not claim source truth from generated graph; read source before implementation claims. |
| `live_runtime_read_only` | Нужно проверить local runtime contract or graph-only API fallback. | Governance packet and disabled runtime contract. | Stop before live server launch unless separate approval packet exists. |
| `provider_retrieval_eval` | Нужно оценить embedding/reranker/LLM provider benefit. | Redaction, cache, budget, baseline and threshold fallback packet. | Stop before any provider/live external model/API call without explicit approval. |
| `canonical_graph_mutation_review` | Нужно проверить proposal acceptance and mutation readiness. | Human review ledger, proposal diff, mutation dry-run plan and rollback proof. | Stop before canonical graph mutation unless owner accepted the proposal and rollback evidence is current. |
| `real_testing_approval` | Нужно перейти от staged evidence к controlled real testing. | Target/data owner approval, runtime/browser/provider/mutation/git action packet and rollback plan. | Stop unless the specific action is approved; approvals are not bundled. |

## Inputs

- цель пользователя или `intent_hint`, если он передан в Codex runtime runner;
- read-only workspace audit: files, stack, test/build commands, docs, CI, contracts and control-plane files;
- текущие `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- source policy, sandbox, approvals and known external-system boundaries;
- previous failure notes, if already recorded in `RUNLOG.md`.

Key routing fields include `finish_options` and `safe_next_action`; they tell the next worker whether to answer, stage a proposal, request approval, run focused verification or stop on an evidence gap.

## Outputs

- `usage_mode.primary`, secondary mode, confidence and routing reasons;
- first response: один ближайший полезный шаг без широкого scaffold, rewrite or external mutation;
- minimum artifacts: concrete files or packets needed before build/review/release;
- approval boundary: what is read-only, staged-only or approval-required;
- verification gates: commands, evals, screenshots, logs, owner review or accepted gap;
- residual risk when route is based on detection rather than verified evidence.

## Guided Question Protocol And Status Dashboard

Guided question protocol uses typed `question_queue` packets so the first response can show only `next_blocking_question`, `question_counts` and `question_summary`. It asks one blocking question maximum, keeps recommended and optional questions in the packet, and routes answers into artifacts or accepted gaps. Guided questions are not workspace evidence and do not replace read-only audit, current command evidence, runtime evidence, owner review or accepted gaps.

The status snapshot is the JSON source for a generated dashboard view. The dashboard stages `.codex/product-agent-os/status.html` and `.codex/product-agent-os/status.json` through the existing approval flow. `status.html` is generated view only: underlying artifacts remain the source material, the dashboard is not an editable database, and stale or inspection-only evidence cannot produce a success claim.

## Self-Verification And Modernization Loop

The `agent_skill_metrics_loop` route reviews agents, skills, prompt/policy packs, router/tool policy and harness-version behavior. It starts from a read-only target registry, explicit run evidence, trace intake, dataset quality checks, local grader summaries and grader/judge calibration. It can stage scorecard ledger records, daily or weekly packets, `agent-skill-evaluation-report.html` and modernization candidates, but every output is staged evidence only.

The route uses source-of-truth policy: control-plane artifacts, run records, trace/eval packets and accepted gaps can support the metrics loop; dashboard HTML, report HTML, memory, raw chat logs and unsupported community claims cannot. The report is not source of truth and cannot turn stale or generated evidence into a completion claim.

The approval boundary stays strict. Product-Agent OS records cadence recommendation values `L0`, `L1`, `L2` and `L3`, but it creates no active schedules. It performs no live eval/model/API calls, makes no external writes, applies no modernization candidates by itself and allows no self-applied updates. Owner review, rollback target and explicit approval state are required before any proposed update moves beyond staged review.

## Project Code Graph And Cockpit

The graph route provides a read-only project graph foundation and generated cockpit for route orientation. It can produce staged graph JSON/JSONL with file-level nodes, Python AST overlays, conservative import/call/test edges, structured Markdown/OpenAPI/AsyncAPI/DBML/SQL/JSON/YAML/Mermaid/PlantUML overlays, controlled ontology/schema validation, manifest freshness/provenance, observation lineage, temporal edge helpers, partition scopes and canonical aliases.

The cockpit renderer can stage offline `.codex/product-agent-os/project-cockpit.html` and `.codex/product-agent-os/project-cockpit.json` review surfaces with top-level pages, Code Flow, static projection, local vendor boundary, graph filters, focused subgraphs, selected-node evidence, fallback tables, mobile layout and no external assets. This helps routes point agents toward source files and stale graph gaps without treating generated artifacts as source of truth.

The boundary remains conservative: generated graph artifacts, runtime graph summaries, analysis reports and HTML cockpit views are review evidence only. The scanner and cockpit renderer do not mutate target workspaces. Live database/server, live external model/API embedding or cross-encoder providers, LLM semantic extraction, rationale/comment extraction and canonical graph mutation remain approval-bound future actions unless explicit approval defines redaction, cache, token budget, eval threshold and rollback path.

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

## Database & Data Methodology Routing

Database/data work keeps `data_migration` as the route name and adds a dedicated Database & Data methodology packet when schema, migration, ORM, warehouse, data quality, lineage, retention, backup/restore or production-data signals appear.

Minimum staged artifacts include `database-inventory.md`, `database-dictionary.md`, `database-migration-plan.md`, `database-data-contract.md`, `database-backup-restore-evidence.md`, `database-lineage-map.md`, `database-query-performance-review.md`, `database-retention-deletion-policy.md`, `database-synthetic-fixtures-policy.md` and `database-production-access-approval.md` when production data, production DB access, backup restore or destructive migration is involved.

Approval boundary stays explicit: DB introspection, production DB access, production data access, migration execution, destructive cleanup, backup restore and retention mutation are not automatic actions.

## Backend Methodology Routing

Backend methodology routing applies when service behavior, background jobs, queues, auth, error handling, observability, deployment or rollback behavior changes. Minimum staged artifacts include `backend-service-overview.md`, `backend-runtime-behavior.md`, runtime/failure evidence, observability evidence, security evidence and rollback evidence.

## LLM / AI / RAG Methodology Routing

AI/RAG work keeps `ai_eval_regression` as the route name and adds a dedicated LLM / AI / RAG methodology packet when prompts, models, eval configs, structured outputs, tool/function/MCP calls, RAG corpora, retrieval, vector stores, embeddings, grounding, agent traces, guardrails or latency/cost signals appear.

Minimum staged artifacts include `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-task-packet.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, `ai-cost-latency-budget.md` and the existing `ai-eval-spec.md` when user-visible AI behavior changes. `agent-handoff-contract.md` is a legacy/source alias to `agent-task-packet.md`, not a duplicate generated contract.

Eval tooling remains conditional: Promptfoo, OpenAI Evals, pytest/Jest app-backed evals, Ragas and LangSmith are recorded as selected, rejected or deferred choices based on stack/privacy/CI fit. Model migration records snapshot or approved alias, prompt migration impact, compatibility checks, rollback, minimum threshold and sampling parameter rationale. RAG evidence records deletion path, retention, source exclusion, stale-source pruning, privacy owner, vector store lifecycle and deletion propagation. Failed evals, hallucination reports, unsafe outputs, tool misuse or data exposure route to an AI incident workflow with severity, mitigation, follow-up eval and Security/Privacy handoff.

AI/RAG route evidence must reject filename-only diffs as quality proof.

Approval boundary stays explicit: live model calls, external eval services, vector DB access, raw prompts/traces/customer text, tool writes, shell/money/data exposure and irreversible side effects are not automatic actions.

## API & Integrations Methodology Routing

API & Integrations methodology routing applies when HTTP APIs, event contracts, webhooks, generated SDKs or external providers change. Minimum staged artifacts include `api-inventory.md`, `api-contract-review.md`, `api-consumer-map.md`, `api-contract-test-matrix.md`, `external-integration-approval.md` and compatibility/security/error/event/SDK evidence.

External writes are not automatic actions; they require an explicit approval boundary.

## Security, Privacy & Compliance Methodology Routing

Security-sensitive work keeps `security_sensitive_change` as the route name and adds a dedicated Security, Privacy & Compliance methodology packet when authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data, policy changes or compliance overlays appear.

Minimum staged artifacts include `security-risk-review.md`, `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md` and `approval-record.md` when the corresponding risk applies. Source-era names such as `threat-model.md`, `asvs-mapping.md`, `secrets-inventory.md`, `authz-matrix.md`, `audit-log-policy.md` and `compliance-applicability-matrix.md` are aliases, not duplicate generated contracts.

Codex Security scans remain explicit opt-in: the route may recommend a scan or record `not requested`, but it must not imply that a scan ran from security terminology alone. Compliance overlays record applicability, owner, evidence, non-goals, gaps and review cadence without claiming legal compliance or certification.

Approval boundary stays explicit: payment/billing, production data, secret rotation, policy changes, external security-system mutations, external writes, publish actions and Codex Security scans are not automatic actions.

## Delivery, Release & Operations Methodology Routing

Release packaging keeps `release_packaging` as the route name and adds a dedicated Delivery, Release & Operations methodology packet when release, deploy, publish, package, versioning, changelog, artifact, rollout, rollback, CI/CD environment, release mode policy, build-release-run boundary, platform distribution evidence, release communication, versioning tooling, GitHub environment controls, SLO/observability, observability/on-call tooling, runbook, incident, postmortem, DORA, release integrity or automation promotion signals appear.

Minimum staged artifacts include `versioning-policy.md`, `release-readiness.md`, `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `environment-matrix.md`, `deployment-plan.md`, `ci-cd-workflow-inventory.md`, `observability-map.md`, `slo-spec.md`, `operations-runbook.md`, `incident-record.md`, `postmortem.md`, `post-release-review.md`, `approval-record.md` and `automation-candidate.md` when automation promotion is proposed.

Approval boundary stays explicit: publish, tag, release creation, artifact upload, deploy, package registry mutation, marketplace/store submission, CI/CD environment mutation and active automation remain approval_required. Automation candidates require manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence and rollback/disable path.

Final release/operations depth also requires owner-reviewed release evidence sufficiency for the real risk. Mobile signing, DORA dashboard notes, release tooling config, generated release notes or a single observability tool remain `present_unverified` until platform owner evidence, team/process measurement design, selected/rejected/deferred tooling decisions, alert path and accepted gaps are recorded.

## Verification

- Route selection is covered by discovery tests, `usage_mode` fixture checks and false-positive fixtures for selected methodology/tooling gates.
- Scenario behavior is covered by `behavioral-workflows.json` and `run_fixture_eval.py`.
- Frontend methodology routing is covered by `frontend_contract_present` and the synthetic `frontend-ui-app` fixture.
- Backend methodology routing is covered by `backend_contract_present` and the synthetic `backend-service-app` fixture.
- API & Integrations methodology routing is covered by `api_integrations_contract_present` and synthetic API fixtures.
- Database & Data methodology routing is covered by `database_data_contract_present` and synthetic database fixtures.
- LLM / AI / RAG methodology routing is covered by `llm_ai_rag_contract_present` and synthetic AI/RAG fixtures.
- Security, Privacy & Compliance methodology routing is covered by `security_privacy_compliance_contract_present` and synthetic security fixtures.
- Delivery, Release & Operations methodology routing is covered by `delivery_release_operations_contract_present` and synthetic release fixtures.
- Docs and source claims are checked by `tools/check_docs.py`, source policy and strict MkDocs when navigation changes.
- Completion language must pass evidence-before-completion: current command evidence, current eval evidence, current runtime evidence, owner evidence or explicit inspection-only gap.

## Risks

- Workspace signals can identify a likely scenario but cannot prove readiness by themselves.
- A scenario may be correct while the selected minimum artifacts are low quality; owner review still matters.
- Approval boundaries are project-specific. Product-Agent OS can mark them, but the user or workspace policy decides whether to proceed.
- Transcript/session eval runner replays synthetic or redacted session fixtures with deterministic expected/forbidden term checks and privacy/no-secrets guards; semantic judgment still needs reviewer or future calibrated judge coverage.

Next artifact: use [Behavioral evals](behavioral-evals.md) to validate that the scenario route resists shortcuts and produces the expected evidence.
