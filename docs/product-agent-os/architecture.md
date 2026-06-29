# Product-Agent OS architecture

Source status: `official + experiment`

Источники: [Codex plugins](https://developers.openai.com/codex/plugins), [Agent Skills](https://developers.openai.com/codex/skills), [Subagents](https://developers.openai.com/codex/subagents), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md), [Codex hooks](https://developers.openai.com/codex/hooks), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex workflows](https://developers.openai.com/codex/workflows), [Technical features](technical.md).

Product-Agent OS plugin строит управляемый lifecycle вокруг Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, memory, sandbox, approvals, MCP и Agents SDK. Его архитектура не пытается "сразу сделать все": она сначала читает workspace, выбирает route, фиксирует ownership и evidence, затем stage-ит предложения или выполняет разрешенный slice.

Главное правило: generated surfaces помогают ориентироваться, но source files, owner decisions и текущий verification evidence остаются сильнее любого dashboard, graph, report или chat memory.

## Layered Model

| Layer | Purpose | Boundary |
| --- | --- | --- |
| Пакет plugin | Manifest, commands, packaged skills и validators. | Package compatibility не активирует external systems. |
| Lifecycle skills | Requirements, planning, test/eval, implementation, review и release handoffs. | Every handoff names files, evidence, risks и stop conditions. |
| Staged infrastructure | Templates для `AGENTS.md`, control-plane files, hooks, workflows и agent configs. | Existing пользователь files являются preserved; ambiguous пишет become proposals. |
| Approved merge | Manifest, approval record, rollback и scoped apply. | Нет direct target-workspace merge без explicit approval. |
| Codex runtime runner | Deterministic route packet для Codex usage. | Нет separate live model call или hidden Agents SDK app. |
| Engineering standards | Hypothesis, architecture, tests, evals, docs, review и release measurement. | Standards become evidence requirements, не ceremony через default. |
| Scenario routes | `usage_mode` chooses first response и minimum artifacts. | Detection never equals readiness. |
| Methodology intelligence | Read-only audit, applicability, owner questions и staged recommendations. | Recommendations не mutate target projects. |
| Graph и live governance | Generated graph, cockpit, runtime gates, provider gates, review, mutation dry-run и audit. | Live execution остается disabled пока separate owner approval. |

Этот порядок prevents stale shortcuts. Runtime, standards, scenarios, methodology synthesis и live governance являются один stack; every писать still passes staged-first и approval boundaries.

## Operating Flow

```mermaid
flowchart LR
    A["Workspace context"] --> B["Read-only inventory"]
    B --> C["Route selection"]
    C --> D["Minimum artifacts"]
    D --> E["Ownership и evidence"]
    E --> F{"Нужно создать?"}
    F -->|No| G["Read-only answer"]
    F -->|Staged proposal| H["Staging directory"]
    F -->|Approved write| I["Scoped implementation"]
    H --> J["Review / accepted gap"]
    I --> K["Доказательства проверки"]
    J --> K
```

Этот route является derived из artifacts, не из chat memory. User intent может steer следующий action, но политика источников, sandbox, approvals и текущий evidence по-прежнему определяют, что можно запускать.

## Архитектура планов и задач

Эта схема фиксирует, как Product-Agent OS создает файлы-планы, ведет матрицу задач, очищает накопленную историю и возвращает пользователю отчет после реализации. Она применяется для работы, где есть методология разработки, несколько связанных задач, архитектурные решения, роли агентов, `skills`, `subagents`, approval boundaries или поэтапная поставка.

```mermaid
flowchart TD
    A["Запрос пользователя или методологическая работа"] --> B["Read-only inventory и аудит методологии"]
    B --> C{"Нужна матрица задач?"}
    C -->|Нет| D["Lightweight exception: причина, сокращенная проверка, residual risk"]
    C -->|Да| E["implementation-planner готовит plan-file proposal"]

    E --> F["Шаблон task-matrix-plan.md"]
    F --> G["Staged artifact в .codex/artifact-templates"]
    G --> H["Утвержденный concrete plan file"]

    H --> I["Validator: поля, статус, время, зависимости, evidence"]
    I --> J{"Валидно?"}
    J -->|Нет| K["Исправить план до implementation"]
    J -->|Да| L["Выполнить focused slice"]

    L --> M["Обновить строку: статус, файлы, проверки, фактическое время"]
    M --> N["RUNLOG.md: краткое current-cycle evidence"]
    M --> O["agent-task-packet.md для handoff в subagents"]
    M --> P["Docs, registry или backlog для source-backed claims"]
    M --> Q["Read-only status projection при необходимости"]

    P --> R["Закрытие пакета: accepted gaps, residual risks, next slice"]
    N --> R
    O --> R
    Q --> R
```

Plan file создается, когда работа требует staged delivery, архитектурной фиксации, нескольких ролей, нескольких verification gates, rollback, eval или user-facing completion report. Для маленькой механической правки допустимо исключение, но причина, сниженный набор evidence и residual risk должны быть названы в ответе или `RUNLOG.md`.

План очищается переносом detail в owning artifact, а не удалением полезной истории: текущая последовательность остается в `PLAN.md` или batch-specific plan file, краткие решения и failures идут в `RUNLOG.md`, source-backed история идет в `docs/sources/registry.md` или backlog, а повторяемые workflow продвигаются по цепочке manual workflow, playbook, skill, plugin, automation candidate.

| Элемент | Что контролирует | Защита от засорения |
| --- | --- | --- |
| Матрица задач | Source, scope, non-goals, expected result, acceptance criteria, verification, risks, agents, skills и dependencies | Каждая строка ограничивает scope и owner |
| Completion report | Что сделано, какие файлы затронуты, technical value, product value, фактическая дата и время | Заполняется после реализации, не заранее |
| `RUNLOG.md` | Current-cycle decisions, latest evidence и failures | Не хранит полный historical ledger |
| `docs/sources/registry.md` | Source-backed claims и historical evidence pointers | Не принимает unsupported claims |
| Status projection | Read-only operational status | Не заменяет plan file, tests или source registry |

Связь с методологиями остается практической: Scrum и Kanban дают sequencing и WIP discipline, ADR фиксирует architecture decisions и non-goals, test-driven development задает verification gates, docs-as-code требует обновления output artifacts и registry, eval-driven AI work добавляет baseline, rubric, threshold и residual quality risk.

`task-matrix-plan.md` -- staged artifact для планирования. Его наличие помогает вести planning, handoff и validation, но само по себе не является source of truth, execution evidence, verification evidence, dashboard readiness или release approval.

## Graph And Live Boundary

Generated graph и cockpit surfaces help readers understand topology, code flow и stale evidence. Они не become source of truth и they не authorize live systems.

| Surface | Primary page | Architectural rule |
| --- | --- | --- |
| Static graph и cockpit | [Project Code Graph](project-code-graph.md) | Graph/cockpit являются generated review surfaces; source files остаются canonical. |
| Live runtime governance | [Live Runtime Governance](live-runtime-governance.md) | Runtime остается disabled-by-default, local-only и read-only пока separate approval. |
| Provider gates | [Live Runtime Governance](live-runtime-governance.md) | Embedding, reranker и LLM proposal providers stay blocked пока approval, redaction, cache, budget и eval threshold являются current. |
| Human review | [Artifact Contracts](artifact-contracts.md) | Review ledger decisions являются `accepted`, `rejected` или `accepted_gap`; proposal evidence является не canonical fact. |
| Canonical mutation | [Artifact Contracts](artifact-contracts.md) | Mutation требует accepted proposal, dry-run plan, mutation journal и rollback proof до any pilot. |
| Audit и observability | [Live Runtime Governance](live-runtime-governance.md) | Live, provider и mutation actions должен emit redacted audit и runtime evidence; unsafe cases block route. |
| Real testing | [Approval-Bound Real Testing](approval-bound-real-testing.md) | Runtime launch, browser automation, provider/API pilot, canonical mutation pilot и git release/PR action являются separate approvals. |

## Completion-skeptic route

```mermaid
flowchart LR
    W["worker_output"] --> P["doubt_verification_packet"]
    P --> C["completion-skeptic"]
    C --> V{"verdict"}
    V -->|pass| A["final answer with evidence"]
    V -->|revise| R["reviser changes only confirmed gaps"]
    V -->|needs_more_context| Q["ask or record missing_context"]
    V -->|blocked_by_approval| B["stop at approval boundary"]
    V -->|accepted_risk| G["accepted_gap with owner and follow-up"]
```

Packet содержит `claim ledger`, `requirement ledger` и `evidence ledger`. `claim ledger` фиксирует `supported`, `unsupported`, `contradicted` и `needs_fresh_check`; `requirement ledger` держит видимыми user requirements, non-goals и approval constraints; `evidence ledger` указывает на source registry, local files, current commands, evals, owner decisions или explicit missing checks.

Completion-skeptic route - ручной и локальный gate Product-Agent OS, а не live runtime proof.

Reviser changes only confirmed gaps. Если verifier находит только speculative concerns, route возвращает residual risk вместо rewrite корректного content.

### Agents SDK output guardrail candidate

Это design-only направление. Тот же packet позже может стать Agents SDK output guardrail candidate с `tripwire` для fake evidence, pass without evidence, approval-blocked pass, missing source status или unsafe private data. Текущая граница: docs/site work не создает Agents SDK runner, MCP server, tracing export, provider call или live guardrail.

## Engineering Standards Route

```mermaid
flowchart LR
    S["Workspace signals"] --> A["REQUIREMENTS.md hypothesis и metrics"]
    A --> B["PLAN.md architecture boundary"]
    B --> C["TEST.md test-first checks"]
    B --> D["EVALS.md quality gates"]
    C --> E["Build slice"]
    D --> E
    E --> F["Documentation system workflow"]
    F --> T["Artifact templates"]
    T --> G["Risk review"]
    G --> H["RUNLOG.md measurement notes"]
```

Product-agent work начинается только после того, как boundary, verification и documentation impact видны следующему worker. Если один element является unavailable, route records explicit gap instead из hiding это в chat.

## Lifecycle Routing

```mermaid
flowchart TD
    A["Workspace context"] --> B{"AGENTS.md exists?"}
    B -->|No| U["uninitialized"]
    B -->|Yes| C{"REQUIREMENTS.md имеет acceptance criteria?"}
    C -->|No| IP["infrastructure_planned"]
    C -->|Yes| D{"PLAN.md имеет verification?"}
    D -->|No| RR["requirements_ready"]
    D -->|Yes| E{".codex/agents/builder.toml exists?"}
    E -->|No| PR["plan_ready"]
    E -->|Yes| F{"TEST.md и EVALS.md имеют quality gates?"}
    F -->|No| TR["team_ready"]
    F -->|Yes| G{"RUNLOG.md lifecycle marker?"}
    G -->|build_active| BA["build_active"]
    G -->|quality_gate| QG["quality_gate"]
    G -->|review_ready| RV["review_ready"]
    G -->|release_ready| RL["release_ready"]
    G -->|learning_ready| LN["learning_ready"]
    G -->|none| M["maintenance"]
```

| State | Next worker | Создайте policy |
| --- | --- | --- |
| `uninitialized` | `workspace-discovery-auditor` | `read_only` |
| `infrastructure_planned` | `requirements-author` | `staged_only` |
| `requirements_ready` | `implementation-planner` | `staged_only` |
| `plan_ready` | `agent-team-designer` | `staged_only` |
| `team_ready` | `test-eval-designer` | `staged_only` |
| `build_active` | `builder` subagent когда allowed | `approved_write` |
| `quality_gate` | `risk-reviewer` | `read_only` |
| `review_ready` | `pr-release-operator` | `staged_only` |
| `release_ready` | `learning-loop-maintainer` | `staged_only` |
| `learning_ready` | `automation-promoter` | `staged_only` |
| `maintenance` | `project-lifecycle-orchestrator` | `read_only` |

## Route Packet

```mermaid
flowchart LR
    S["Lifecycle state"] --> R["Route planner"]
    U["usage_mode"] --> R
    R --> K["Recommended skill"]
    R --> A["Recommended subagent role"]
    R --> W["Создайте policy"]
    R --> V["Verification commands"]
    W --> P{"approved_write?"}
    P -->|No| O["read_only или staged_only"]
    P -->|Yes| G["explicit approval record required"]
```

Этот route packet carries `usage_mode`, confidence, routing reasons, minimum artifacts, approval boundary, ожидаемые доказательства, residual risks и next safe action. Это является planning contract, не permission к mutate external systems.

## Methodology Intelligence

```mermaid
flowchart LR
    W["Workspace signals"] --> C["Methodology catalog"]
    C --> A["Read-only audit"]
    A --> M["maturity_level"]
    A --> P["complexity_profile"]
    A --> R["Prioritized recommendations"]
    R --> Q["Owner questions"]
    R --> D["Delivery Map"]
    D --> S{"Нужно создать?"}
    S -->|No| O["Только report"]
    S -->|Yes| G["staged_only proposal"]
    G --> X["explicit approval boundary"]
```

Methodology intelligence запускается до lifecycle mutation. Он может read workspace и produce `methodology_applicability`, `methodology-audit-report.md`, Delivery Map priorities и owner questions. Он не пишет target-project files, не включает hooks, не активирует automations и не touch external systems. Any generated artifact после report остается staged-only пока explicit approval.

## Usage Mode Coverage

```mermaid
flowchart TD
    W["Workspace и prompt signals"] --> U["usage_mode classifier"]
    U --> D["scenario workflow modes"]
    U --> M["methodology gates"]
    U --> P["readiness overlays"]
    U --> B["base modes"]
    D --> A["stage workflow + artifact proposal"]
    M --> E["enforce gate fields до build"]
    P --> G["name minimum artifacts + explicit evidence gaps"]
    B --> R["standard lifecycle route"]
```

| Coverage | Modes | Required behavior |
| --- | --- | --- |
| Scenario workflows | first-run intake plus `bug_rescue`, `greenfield_idea`, `complex_system_acceleration`, `pr_review`, `legacy_onboarding`, `api_migration`, `ai_eval_regression`, `native_mobile_feature`, `desktop_local_first`, `data_migration`, `security_sensitive_change`, `ci_stabilization`, `release_packaging` | Stage existing workflow/artifact templates, keep first response small и запуск behavior-level checks. |
| Methodology gates | no-placeholder planning, generalized two-stage review, fresh-context handoff, acceptance scenarios, conditional DDD domain modeling, bounded-context-to-architecture traceability, ubiquitous language traceability, conditional FSD structure routing | Require exact files, commands, expected outputs, rollback, evidence owner, accepted gaps и ownership до build или handoff. |
| Readiness overlays | quality, release, security, AI/RAG, data и runtime readiness | Route safely, name required artifacts, record evidence gaps и avoid completion claims без verification evidence. |
| Base modes | `standard_feature`, `docs_only`, `maintenance` | Используйте normal lifecycle route с minimum control-plane artifacts. |

## Staged-First Infrastructure

```mermaid
flowchart TD
    A["Target workspace"] --> B["Read-only audit"]
    B --> C["Template render"]
    C --> D{"Existing пользователь file?"}
    D -->|No| E["Stage create"]
    D -->|Managed markers| F["Stage managed-section update"]
    D -->|Unmarked file| G["Stage companion proposal"]
    E --> H["Stage manifest"]
    F --> H
    G --> H
    H --> I["Read-only merge plan"]
    I --> J{"Explicit approval record?"}
    J -->|No| K["Остановиться at needs_approval"]
    J -->|Yes| L["Применить scoped decisions"]
    L --> M["Rollback manifest"]
```

Renderer может inspect workspace и писать только в explicit staging directory. Direct target пишет выполняются только через merge tooling после approval.

## Codex Runtime Runner

```mermaid
flowchart TD
    A["run_codex_runtime_runner.py --contract"] --> B["Load control-plane files"]
    B --> C["Infer lifecycle state"]
    C --> D["Plan route"]
    D --> E["Validate политика источников"]
    E --> F["Validate approval boundary"]
    F --> G["Validate route packet"]
    G --> H["Build result contract"]
    H --> I["Redact secrets и local paths"]
    I --> J{"Errors?"}
    J -->|No| K["route_ready"]
    J -->|Approval missing| L["needs_approval"]
    J -->|Context missing| M["needs_context"]
    J -->|Policy blocked| N["blocked"]
```

Этот runner является Codex-only. Это не call external model, не требуют separate OpenAI API key и не become Agents SDK app. Это produces deterministic contract packet который Codex может использовать к route следующий action.

## Automation Promotion

```mermaid
flowchart TD
    A["Repeated workflow"] --> B{"Manual success evidence?"}
    B -->|No| C["Keep manual workflow"]
    B -->|Yes| D{"Stable inputs и outputs?"}
    D -->|No| C
    D -->|Yes| E{"Verification и failure modes named?"}
    E -->|No| C
    E -->|Yes| F{"Owner, cadence и rollback named?"}
    F -->|No| C
    F -->|Yes| G["Automation candidate packet"]
    G --> H["Manual approval required до active automation"]
```

Product-Agent OS может stage automation candidate, но это должен не create active recurring automation пока workflow имеет stability evidence и explicit approval.

## Common Failure Modes

| Failure | Required behavior |
| --- | --- |
| Missing requirements | Route к requirements author, не build. |
| Missing verification | Route к planning или test/eval designer. |
| Source-backed claim lacks source | Mark требует review или block через политика источников. |
| Approved писать route lacks approval | Return `needs_approval`. |
| Active automation requested too early | Block и keep candidate-only. |
| Secret-like content appears в output | Redact и report redaction category. |
| Existing file имеет ambiguous managed markers | Остановиться и report conflict. |

Следующий artifact: используйте [Scenarios](scenarios.md) для route selection, [Professional Code Authoring standards](coding-standards.md) для code-writing gates и [Behavioral evals](behavioral-evals.md) для expected/forbidden behavior.
