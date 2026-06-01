# Product-Agent OS plugin

Source status: `official + experiment`  

## Task 24 Self-Verification And Modernization Loop

Task 24 Self-Verification And Modernization Loop adds a self-verification metrics loop for Product-Agent OS agents, skills, prompt/policy packs, router/tool policies and harness versions. The `agent_skill_metrics_loop` route produces staged evidence only: target registry, trace/dataset/grader summaries, scorecard ledger, report packet and modernization candidates. It performs no live eval/model/API calls, creates no active schedules, applies no candidates by itself and allows no self-applied updates.

## Task 25 Project Code Graph Foundation

Task 25 Batch 13 and Batch 14 add the first project code graph foundation plus Python/structured overlay support. `scan_project_code_graph.py` is read-only and stage-only: dry-run emits redacted graph JSON, and stage mode writes `.codex/product-agent-os/project-code-graph.json` plus JSONL only under an explicit stage directory outside the target workspace. The graph currently records file-level nodes, Python AST package/module/class/function/method overlays, conservative import/call/test edges, structured docs/contracts/schema/diagram overlays, controlled ontology/schema validation, manifest freshness/provenance, observation lineage, temporal edge delta helpers, partition scopes, canonical aliases and synthetic scale fixtures.

This is not a complete semantic code intelligence layer. Dependency query packets, analysis reports, search-quality evals, Graphology/Sigma visualization and the eight-page HTML cockpit remain later Task 25 batches. Generated graph artifacts and future HTML views are review surfaces, not source of truth.

## Task 22 final documentation sync closure

Task 22 final documentation sync closure фиксирует Product-Agent OS full stack как рабочий путь для реальных проектов: inspect workspace, отделить prompt intent от workspace evidence, stage infrastructure, получить approved merge, пройти Codex-only runtime routing, применить conditional methodology gates и потребовать evidence before completion.

Tracks 1-9 are implementation provenance, а не основной пользовательский сценарий. Для оператора путь выглядит так: read-only audit -> staged proposal -> approval -> bounded implementation -> checks/evals -> review -> release or learning packet. История Track 1-9 объясняет, откуда появились package contracts, lifecycle skills, generated infrastructure, hardening, runtime runner, engineering standards, scenario workflows и methodology intelligence.
Источники: [Codex plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://developers.openai.com/codex/skills), [Subagents](https://developers.openai.com/codex/subagents), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md), [Codex hooks](https://developers.openai.com/codex/hooks), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex workflows](https://developers.openai.com/codex/workflows), [Product-Agent Workflows](../product-agent/overview.md).

`product-agent-os` - локальный Codex plugin для проектов, где Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, hooks, evals и automation candidates должны работать как управляемая система delivery, а не как набор разовых prompts.

Плагин не заменяет владельца продукта и не включает автономные изменения сам по себе. Его задача - превратить workspace в управляемый lifecycle: read-only audit, требования, план, team ownership, staged infrastructure, проверки, review, release packet, learning loop и только затем automation candidate. Новый слой [Engineering standards layer](development-standards.md) добавляет product hypothesis, architecture boundary, test-first/eval-first gates, docs-as-code, release measurement, discovery signals и concrete artifact templates как обязательные элементы зрелой разработки.

## Какие боли решает

| Боль | Что делает plugin |
| --- | --- |
| Длинная Codex-сессия теряет контекст | Выносит цель, план, проверки и решения в control-plane files |
| Требования живут только в чате | Создает `REQUIREMENTS.md` с scope, non-goals и acceptance criteria |
| Планирование смешивается с implementation | Требует `PLAN.md`, ownership, verification и rollback до build slice |
| Subagents работают без границ | Проектирует роли через ownership, handoff artifacts и stop conditions |
| Проверки называются задним числом | Разделяет deterministic checks в `TEST.md` и quality gates в `EVALS.md` |
| Агент пишет код без инженерной методологии | Добавляет product hypothesis, architecture boundary, test/eval-first path, docs impact и measurement |
| Проектные правила размазаны по memory | Переносит durable rules в `AGENTS.md`, а текущие решения в `RUNLOG.md` |
| Hooks и automations включаются слишком рано | Ставит staged-first и candidate-only boundary до ручного approval |
| Невозможно доказать, что работа verified | Требует evidence: команды, fixture evals, source policy и review findings |

## Кому подходит

| Сценарий | Польза |
| --- | --- |
| Solo developer | Быстро структурировать feature и не потерять acceptance criteria |
| Product engineer | Вести работу от идеи до PR packet через проверяемые artifacts |
| Engineering team | Разделить worktrees, roles и write scopes без конфликтов |
| AI product team | Добавить eval-driven loop и source/context policy |
| Governed workspace | Сохранить approvals, staged writes, rollback и audit trail |

## Основной lifecycle

```mermaid
flowchart LR
    A["Idea"] --> B["Workspace audit"]
    B --> C["REQUIREMENTS.md"]
    C --> D["PLAN.md"]
    D --> E["Agent team"]
    E --> F["Build slice"]
    F --> G["TEST.md / EVALS.md"]
    G --> H["Review"]
    H --> I["PR or release packet"]
    I --> J["RUNLOG.md learning"]
    J --> K["Automation candidate"]
```

Plugin держит lifecycle последовательным. Он не должен перескакивать из `uninitialized` сразу в `build_active`: сначала нужны context, requirements, plan, ownership и quality gates.

## Текущий Track 8 статус

Новый план различает готовые workflows, done methodology gates, partial methodology gates и pending сценарии:

| Уровень | Что это означает | Сценарии |
| --- | --- | --- |
| `done` | Есть route, staged workflow/artifact templates, behavioral evals и текущая verification evidence. | first-run intake, bug rescue, greenfield idea, complex system acceleration, PR review, legacy onboarding, API migration, AI/RAG eval regression, native/mobile, desktop local-first, data migration, security-sensitive change, CI stabilization, release packaging. |
| `done` methodology gate | Есть reusable gate, templates, behavioral eval и fixture coverage. | no-placeholder planning, generalized two-stage review, fresh-context handoff, acceptance scenarios, conditional DDD domain modeling, bounded-context-to-architecture traceability, ubiquitous language traceability, conditional FSD structure routing, metric hardening, evidence-before-completion, docs tooling selector, conditional readiness statuses. |
| `partial` | Есть часть системного поведения, но не весь planned contract. | lifecycle trigger hardening. |

## Что входит сейчас

- Plugin package under `plugins/product-agent-os/` with `.codex-plugin/plugin.json`.
- Packaged lifecycle skills: orchestrator, discovery auditor, requirements author, implementation planner, team designer, test/eval designer, risk reviewer, release operator, learning loop maintainer and automation promoter.
- Staged infrastructure renderer for control-plane files, project-scoped `.codex/agents/`, hook templates, workflows, eval templates, PR/release templates and automation candidates.
- Engineering standards workflow templates: `.codex/workflows/development-standards.md` and `.codex/workflows/documentation-system.md`.
- Engineering standards artifact templates: `.codex/artifact-templates/adr.md`, `architecture-overview.md`, `domain-modeling.md`, `metric-spec.md`, `api-contract-review.md`, `component-card.md` and `database-dictionary.md`.
- Safe merge tooling with approval record, manifest validation, workspace-bound paths and rollback support.
- Source policy, automation candidate validation, fixture evals and Codex-only runtime runner contract mode.
- Track 8 workflow templates for first-run intake, bug rescue, greenfield idea shaping, complex system acceleration, PR review readiness, legacy onboarding, API migration, AI/RAG eval regression, native/mobile feature work, desktop local-first work, data migration, security-sensitive change, CI stabilization and release packaging.
- First-run route contract for empty, broken, existing control-plane and complex system starts: mode, confidence, next smallest action, minimum artifacts, evidence gaps and approval boundary.
- No-placeholder planning gate in `implementation-planner`, `PLAN.md`, `build-slice.md`, `plan-quality-check.md`, behavioral eval and fixture eval: non-trivial slices need exact files, owned/forbidden files, exact commands, expected outputs, rollback, evidence owner and placeholder scan before build.
- Generalized two-stage review gate in `risk-reviewer`, `review-slice.md`, `RUNLOG.md`, `pr-risk-review.md` and behavioral eval: risky PR/public-contract/migration/security/data/release/parallel slices need spec compliance before quality/risk, and missing evidence blocks ready verdicts.
- Fresh-context handoff gate in `agent-team-designer`, `handoff-contract.md`, `agent-task-packet.md`, `worktree-ownership.md` and behavioral eval: subagents and parallel workers need complete task context, source constraints, allowed sources, inputs used, owned/forbidden files, expected evidence, handoff output schema, stop conditions and sequential fallback before work starts.
- Acceptance scenarios gate in `requirements-author`, `implementation-planner`, `test-eval-designer`, generated `REQUIREMENTS/TEST/EVALS`, `development-standards.md`, `acceptance-scenarios.md`, readiness eval and behavioral eval: behavior changes need `requirement -> scenario -> check -> evidence owner`, Given/When/Then or equivalent behavior format, business rule, edge case, non-goal, explicit gap and evidence owner before implementation.
- Conditional DDD domain modeling gate in `discovery.py`, `domain-modeling.md`, `architecture-overview.md`, `project-readiness.json`, `implementation-planner` and fixture eval: complex backend/workflow/enterprise/data-heavy/multi-service/multi-context work needs bounded context, bounded-context-to-architecture traceability, ubiquitous language traceability, invariant or accepted gap, while simple CRUD/MVP work is not forced into DDD.
- Ubiquitous language traceability gate in `domain-modeling.md`, generated `PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, `implementation-planner` and fixture eval: every domain term maps to requirement/source plus API/event/contract, UI label, code module or owner, or records accepted gap with domain expert review.
- Conditional FSD structure routing in `discovery.py`, `component-card.md`, `development-standards.md`, `project-readiness.json`, `workspace-discovery-auditor` and `implementation-planner`: web UI work can use optional `fsd_structure` when Feature-Sliced Design layer directories are present, while backend, native, simple CRUD and simple MVP work records FSD as not applicable or accepted gap.
- Metric hardening gate in `metric-spec.md`, `release-packet.md`, generated `REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, lifecycle skills and fixture eval: product behavior changes need `metric_hardening_when_product_behavior_changes`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff and post-release review evidence before product success claims.
- Evidence-before-completion gate in `release-packet.md`, `development-standards.md`, generated `AGENTS/PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, lifecycle skills, behavioral eval and fixture eval: ready/completed/fixed/works/release claims need current command evidence, current eval evidence, current runtime evidence, owner evidence or explicit test gap; inspection-only answers must stay labeled.
- Docs tooling selector in `docs-tooling-decision.md`, `documentation-system.md`, generated `PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, lifecycle skills, discovery and fixture eval: `docs_as_code_impact` can be `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` or `approval_required`; docs-light/internal-only projects are not forced into heavy portals, and hosted docs or DB introspection require approval.
- Conditional readiness gates in `project-readiness.json`, generated `AGENTS/PLAN/TEST/EVALS/RUNLOG`, lifecycle skills and fixture eval: `readiness_statuses` include `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required`; every gate names applicability, required evidence, owner and residual risk, and detection alone cannot claim readiness.
- Transcript/session eval runner in `product_agent_os/transcript_evals.py`, `run_transcript_eval.py`, `product-agent-os-synthetic-sessions.json` and fixture eval: synthetic or redacted sessions replay against `behavioral-workflows.json`, check `expected_terms`, `forbidden_terms`, `missing_expected_terms`, `forbidden_terms_present` and `privacy_errors`, and avoid external systems.
- Track 9 methodology intelligence foundation with read-only methodology catalog, workspace audit, `maturity_level`, `complexity_profile`, Delivery Map, prioritized recommendations, owner questions, `methodology-audit-report.md` and fixture eval coverage.
- API migration artifact templates for migration plans and contract reviews with OpenAPI/AsyncAPI, consumers, generated clients, compatibility, deprecation, rollout, release impact and owner review gates.
- AI eval artifact templates for baseline, no-secrets dataset policy, rubric, threshold, rerun command, latency, cost, grounding, failure examples and residual risk.
- Native/mobile workflow coverage for platform assumptions, permissions, offline state, simulator/emulator, device, logs, screenshots, build command, runtime evidence, manual device gaps and approval boundaries.
- Desktop local-first workflow coverage for filesystem permissions, local data, local DB, indexing, background jobs, privacy, app logs, runtime log checks, recovery path, rollback, runtime evidence and manual OS gaps.
- Data migration workflow coverage for schema changes, backfill, data quality, PII, sensitive fields, retention, rollback, validation, dry run, backup, database dictionary, owner review, production DB boundary and approval.
- Security-sensitive workflow coverage for threat surface, authn/authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, audit logging, tests, rollback, owner review, approval and explicit Codex Security boundaries.
- CI stabilization workflow coverage for failing job, command, logs, environment, deterministic/flaky classification, isolation plan, local reproduction, rerun evidence, remote CI/GitHub Actions boundary and approval.
- Release packaging workflow coverage for release scope, package metadata, version/SemVer, changelog, build/test/docs evidence, security and license notes, artifacts, package registry, publish approval, tag boundary, rollback and residual risk.

## Границы

- Plugin работает внутри Codex. Он не требует отдельного OpenAI API key и не запускает standalone Agents SDK runner.
- Infrastructure generation is staged-first: dry-run or staging directory before any target workspace write.
- Hooks are packaged as templates and examples; they are not silently activated.
- Automation artifacts are candidate-only until manual workflow is stable and explicitly approved.
- Secrets, private customer data, raw private chat logs and local absolute paths must not попадать в docs, fixtures, prompts, memory or templates.

## Куда идти дальше

- [Технические особенности и установка](technical.md) - реальные файлы, команды, capabilities и install boundary.
- [Engineering standards layer](development-standards.md) - как plugin внедряет DDD/FSD/TDD/ADD, docs-as-code и eval-driven quality без превращения их в dogma.
- [Methodology intelligence](methodology-intelligence.md) - read-only audit, Delivery Map, recommendations, owner questions and staged artifact boundary for Track 9.
- [Scenarios and usage modes](scenarios.md) - first response, minimum artifacts, approval boundary and verification gates for Track 8 scenarios.
- [Behavioral evals](behavioral-evals.md) - expected behavior, forbidden behavior, fixture eval and transcript/session replay.
- [Codex compatibility](codex-compatibility.md) - Codex App, CLI, IDE extension, `.codex-plugin`, skills, MCP and staged hooks support boundary.
- [Диаграммы и принципы работы](architecture.md) - state routing, staged-first merge, approval gates and runtime runner flow.
- [Product-Agent Workflows](../product-agent/overview.md) - общий operating model без привязки к plugin package.
