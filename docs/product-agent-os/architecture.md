# Product-Agent OS architecture

Source status: `official + experiment`

Источники: [Codex plugins](https://developers.openai.com/codex/plugins), [Agent Skills](https://developers.openai.com/codex/skills), [Subagents](https://developers.openai.com/codex/subagents), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md), [Codex hooks](https://developers.openai.com/codex/hooks), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex workflows](https://developers.openai.com/codex/workflows), [Technical features](technical.md).

Product-Agent OS plugin строит управляемый lifecycle вокруг Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, memory, sandbox, approvals, MCP и Agents SDK. Его архитектура не пытается "сразу сделать все": она сначала читает workspace, выбирает route, фиксирует ownership и evidence, затем stage-ит предложения или выполняет разрешенный slice.

Главное правило: generated surfaces помогают ориентироваться, но source files, owner decisions и current verification evidence остаются сильнее любого dashboard, graph, report или chat memory.

## Layered Model

| Layer | Purpose | Boundary |
| --- | --- | --- |
| Plugin package | Manifest, commands, packaged skills and validators. | Package compatibility does not activate external systems. |
| Lifecycle skills | Requirements, planning, test/eval, implementation, review and release handoffs. | Every handoff names files, evidence, risks and stop conditions. |
| Staged infrastructure | Templates for `AGENTS.md`, control-plane files, hooks, workflows and agent configs. | Existing user files are preserved; ambiguous writes become proposals. |
| Approved merge | Manifest, approval record, rollback and scoped apply. | No direct target-workspace merge without explicit approval. |
| Codex runtime runner | Deterministic route packet for Codex usage. | No separate live model call or hidden Agents SDK app. |
| Engineering standards | Hypothesis, architecture, tests, evals, docs, review and release measurement. | Standards become evidence requirements, not ceremony by default. |
| Scenario routes | `usage_mode` chooses first response and minimum artifacts. | Detection never equals readiness. |
| Methodology intelligence | Read-only audit, applicability, owner questions and staged recommendations. | Recommendations do not mutate target projects. |
| Graph and live governance | Generated graph, cockpit, runtime gates, provider gates, review, mutation dry-run and audit. | Live execution remains disabled until separate owner approval. |

This order prevents stale shortcuts. Runtime, standards, scenarios, methodology synthesis and live governance are one stack; every write still passes staged-first and approval boundaries.

## Operating Flow

```mermaid
flowchart LR
    A["Workspace context"] --> B["Read-only inventory"]
    B --> C["Route selection"]
    C --> D["Minimum artifacts"]
    D --> E["Ownership and evidence"]
    E --> F{"Write needed?"}
    F -->|No| G["Read-only answer"]
    F -->|Staged proposal| H["Staging directory"]
    F -->|Approved write| I["Scoped implementation"]
    H --> J["Review / accepted gap"]
    I --> K["Verification evidence"]
    J --> K
```

The route is derived from artifacts, not from chat memory. User intent can steer the next action, but source policy, sandbox, approvals and current evidence still decide what can run.

## Graph And Live Boundary

Generated graph and cockpit surfaces help readers understand topology, code flow and stale evidence. They do not become source of truth and they do not authorize live systems.

| Surface | Primary page | Architectural rule |
| --- | --- | --- |
| Static graph and cockpit | [Project Code Graph](project-code-graph.md) | Graph/cockpit are generated review surfaces; source files remain canonical. |
| Live runtime governance | [Live Runtime Governance](live-runtime-governance.md) | Runtime remains disabled-by-default, local-only and read-only until separate approval. |
| Provider gates | [Live Runtime Governance](live-runtime-governance.md) | Embedding, reranker and LLM proposal providers stay blocked until approval, redaction, cache, budget and eval threshold are current. |
| Human review | [Artifact Contracts](artifact-contracts.md) | Review ledger decisions are `accepted`, `rejected` or `accepted_gap`; proposal evidence is not a canonical fact. |
| Canonical mutation | [Artifact Contracts](artifact-contracts.md) | Mutation requires accepted proposal, dry-run plan, mutation journal and rollback proof before any pilot. |
| Audit and observability | [Live Runtime Governance](live-runtime-governance.md) | Live, provider and mutation actions must emit redacted audit and runtime evidence; unsafe cases block the route. |
| Real testing | [Approval-Bound Real Testing](approval-bound-real-testing.md) | Runtime launch, browser automation, provider/API pilot, canonical mutation pilot and git release/PR action are separate approvals. |

## Engineering Standards Route

```mermaid
flowchart LR
    S["Workspace signals"] --> A["REQUIREMENTS.md hypothesis and metrics"]
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

Product-agent work starts only after boundary, verification and documentation impact are visible to the next worker. If one element is unavailable, the route records an explicit gap instead of hiding it in chat.

## Lifecycle Routing

```mermaid
flowchart TD
    A["Workspace context"] --> B{"AGENTS.md exists?"}
    B -->|No| U["uninitialized"]
    B -->|Yes| C{"REQUIREMENTS.md has acceptance criteria?"}
    C -->|No| IP["infrastructure_planned"]
    C -->|Yes| D{"PLAN.md has verification?"}
    D -->|No| RR["requirements_ready"]
    D -->|Yes| E{".codex/agents/builder.toml exists?"}
    E -->|No| PR["plan_ready"]
    E -->|Yes| F{"TEST.md and EVALS.md have quality gates?"}
    F -->|No| TR["team_ready"]
    F -->|Yes| G{"RUNLOG.md lifecycle marker?"}
    G -->|build_active| BA["build_active"]
    G -->|quality_gate| QG["quality_gate"]
    G -->|review_ready| RV["review_ready"]
    G -->|release_ready| RL["release_ready"]
    G -->|learning_ready| LN["learning_ready"]
    G -->|none| M["maintenance"]
```

| State | Next worker | Write policy |
| --- | --- | --- |
| `uninitialized` | `workspace-discovery-auditor` | `read_only` |
| `infrastructure_planned` | `requirements-author` | `staged_only` |
| `requirements_ready` | `implementation-planner` | `staged_only` |
| `plan_ready` | `agent-team-designer` | `staged_only` |
| `team_ready` | `test-eval-designer` | `staged_only` |
| `build_active` | `builder` subagent when allowed | `approved_write` |
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
    R --> W["Write policy"]
    R --> V["Verification commands"]
    W --> P{"approved_write?"}
    P -->|No| O["read_only or staged_only"]
    P -->|Yes| G["explicit approval record required"]
```

The route packet carries `usage_mode`, confidence, routing reasons, minimum artifacts, approval boundary, expected evidence, residual risks and next safe action. It is a planning contract, not permission to mutate external systems.

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
    D --> S{"Write needed?"}
    S -->|No| O["Report only"]
    S -->|Yes| G["staged_only proposal"]
    G --> X["explicit approval boundary"]
```

Methodology intelligence runs before lifecycle mutation. It can read the workspace and produce `methodology_applicability`, `methodology-audit-report.md`, Delivery Map priorities and owner questions. It does not write target-project files, enable hooks, activate automations or touch external systems. Any generated artifact after the report remains staged-only until explicit approval.

## Usage Mode Coverage

```mermaid
flowchart TD
    W["Workspace and prompt signals"] --> U["usage_mode classifier"]
    U --> D["scenario workflow modes"]
    U --> M["methodology gates"]
    U --> P["readiness overlays"]
    U --> B["base modes"]
    D --> A["stage workflow + artifact proposal"]
    M --> E["enforce gate fields before build"]
    P --> G["name minimum artifacts + explicit evidence gaps"]
    B --> R["standard lifecycle route"]
```

| Coverage | Modes | Required behavior |
| --- | --- | --- |
| Scenario workflows | first-run intake plus `bug_rescue`, `greenfield_idea`, `complex_system_acceleration`, `pr_review`, `legacy_onboarding`, `api_migration`, `ai_eval_regression`, `native_mobile_feature`, `desktop_local_first`, `data_migration`, `security_sensitive_change`, `ci_stabilization`, `release_packaging` | Stage existing workflow/artifact templates, keep first response small and run behavior-level checks. |
| Methodology gates | no-placeholder planning, generalized two-stage review, fresh-context handoff, acceptance scenarios, conditional DDD domain modeling, bounded-context-to-architecture traceability, ubiquitous language traceability, conditional FSD structure routing | Require exact files, commands, expected outputs, rollback, evidence owner, accepted gaps and ownership before build or handoff. |
| Readiness overlays | quality, release, security, AI/RAG, data and runtime readiness | Route safely, name required artifacts, record evidence gaps and avoid completion claims without verification evidence. |
| Base modes | `standard_feature`, `docs_only`, `maintenance` | Use normal lifecycle route with minimum control-plane artifacts. |

## Staged-First Infrastructure

```mermaid
flowchart TD
    A["Target workspace"] --> B["Read-only audit"]
    B --> C["Template render"]
    C --> D{"Existing user file?"}
    D -->|No| E["Stage create"]
    D -->|Managed markers| F["Stage managed-section update"]
    D -->|Unmarked file| G["Stage companion proposal"]
    E --> H["Stage manifest"]
    F --> H
    G --> H
    H --> I["Read-only merge plan"]
    I --> J{"Explicit approval record?"}
    J -->|No| K["Stop at needs_approval"]
    J -->|Yes| L["Apply scoped decisions"]
    L --> M["Rollback manifest"]
```

Renderer may inspect a workspace and write only to an explicit staging directory. Direct target writes happen only through merge tooling after approval.

## Codex Runtime Runner

```mermaid
flowchart TD
    A["run_codex_runtime_runner.py --contract"] --> B["Load control-plane files"]
    B --> C["Infer lifecycle state"]
    C --> D["Plan route"]
    D --> E["Validate source policy"]
    E --> F["Validate approval boundary"]
    F --> G["Validate route packet"]
    G --> H["Build result contract"]
    H --> I["Redact secrets and local paths"]
    I --> J{"Errors?"}
    J -->|No| K["route_ready"]
    J -->|Approval missing| L["needs_approval"]
    J -->|Context missing| M["needs_context"]
    J -->|Policy blocked| N["blocked"]
```

The runner is Codex-only. It does not call an external model, does not require a separate OpenAI API key and does not become an Agents SDK app. It produces a deterministic contract packet that Codex can use to route the next action.

## Automation Promotion

```mermaid
flowchart TD
    A["Repeated workflow"] --> B{"Manual success evidence?"}
    B -->|No| C["Keep manual workflow"]
    B -->|Yes| D{"Stable inputs and outputs?"}
    D -->|No| C
    D -->|Yes| E{"Verification and failure modes named?"}
    E -->|No| C
    E -->|Yes| F{"Owner, cadence and rollback named?"}
    F -->|No| C
    F -->|Yes| G["Automation candidate packet"]
    G --> H["Manual approval required before active automation"]
```

Product-Agent OS can stage an automation candidate, but it must not create active recurring automation until the workflow has stability evidence and explicit approval.

## Common Failure Modes

| Failure | Required behavior |
| --- | --- |
| Missing requirements | Route to requirements author, do not build. |
| Missing verification | Route to planning or test/eval designer. |
| Source-backed claim lacks source | Mark needs review or block through source policy. |
| Approved write route lacks approval | Return `needs_approval`. |
| Active automation requested too early | Block and keep candidate-only. |
| Secret-like content appears in output | Redact and report redaction category. |
| Existing file has ambiguous managed markers | Stop and report conflict. |

Next artifact: use [Scenarios](scenarios.md) for route selection and [Behavioral evals](behavioral-evals.md) for expected/forbidden behavior.
