# Batch 45 Professional Code Authoring solution map

Source status: `project-authored + derived_from_current_batch45_artifacts`

This internal artifact is a visual orientation map for Batch 45 Professional Code Authoring.
It is not a readiness claim, not a runtime proof and not a promotion decision by
itself. The source of truth remains the Track 11 task matrix, the Batch 45
evidence packets, the coding standards templates, public docs and current
verification evidence listed below.

## Reading Contract

Use this map when you need to see the full Product-Agent OS coding-standard
system at once:

- what the standard asks an agent to do before writing code;
- which `B45-PCA-*` task rows produced each surface;
- which artifacts are normative task inputs;
- which artifacts are evidence packets;
- which runtime or hook surfaces are only advisory;
- which promotion routes are explicitly blocked by current evidence.

The diagrams use four claim levels:

| Marker | Meaning |
| --- | --- |
| `docs_contract_ready` | Source/docs/template/eval contract exists and has local checks. |
| `synthetic_green` | Local synthetic tests or manual pilot evidence exists. |
| `runtime_enabled_local` | Approved local runtime surface ran in current evidence. |
| `no_go` | Stronger promotion or behavior-improvement claim is rejected by evidence. |

## Source Artifacts

| Layer | Artifacts |
| --- | --- |
| Research inputs | `plugins/product-agent-os/assets/research/ai-agent-coding-standards-research.md`; `plugins/product-agent-os/assets/research/ai-agent-coding-literature-research.md` |
| Standards workflow | `plugins/product-agent-os/assets/templates/workflows/development-standards.md`; `plugins/product-agent-os/assets/templates/workflows/coding-standards.md` |
| Task checklist | `plugins/product-agent-os/assets/templates/artifact-templates/coding-standard-checklist.md` |
| Handoff contract | `plugins/product-agent-os/assets/templates/artifact-templates/agent-task-packet.md`; subagent context/result packet templates |
| Public docs | `docs/product-agent-os/coding-standards.md`; `docs/product-agent-os/coding-standards.en.md`; related cross-links in Product-Agent OS docs and code-review playbook |
| Task matrix | `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`; `PLAN.md`; `TEST.md`; `EVALS.md`; `RUNLOG.md` |
| Evidence packets | `docs/superpowers/specs/batch45-*.json` evidence packets |
| Tests | `tests/product_agent_os/test_batch45_coding_standards.py`; `tests/product_agent_os/test_batch45_s2_existing_workflow_retrofit.py`; `tests/product_agent_os/test_batch45_s3_professional_code_authoring.py`; `tests/product_agent_os/test_coding_standards_artifacts.py`; `tests/product_agent_os/test_comment_sufficiency.py`; `tests/product_agent_os/test_lifecycle_hooks.py` |

## Map 1: Whole-System Topology

```mermaid
flowchart TB
    classDef source fill:#edf2ff,stroke:#4263eb,color:#102a43
    classDef contract fill:#e6fcf5,stroke:#0ca678,color:#102a43
    classDef surface fill:#fff4e6,stroke:#f08c00,color:#102a43
    classDef evidence fill:#f3f0ff,stroke:#7950f2,color:#102a43
    classDef allowed fill:#d3f9d8,stroke:#2f9e44,color:#102a43
    classDef blocked fill:#fff5f5,stroke:#c92a2a,color:#102a43

    R["Source layer<br/>135-source research<br/>60-book literature<br/>local Product-Agent OS audit<br/>Development Standards<br/>AGENTS / approvals / source policy"]
    C["Professional Code Authoring contract<br/>M01 synthesis ledger<br/>M20 activation policy<br/>senior leverage ladder<br/>evidence ceiling"]
    A["Normative task artifacts<br/>coding-standards workflow<br/>coding-standard checklist<br/>agent-task packet<br/>role and subagent handoff fields<br/>RU/EN public docs"]
    I["Integration surfaces<br/>workflow and artifact templates<br/>agent profiles and handoffs<br/>behavioral evals<br/>agent-context contract<br/>discovery/runtime/HTML visibility<br/>candidate-only learning-loop policy"]
    V["Advisory validation lane<br/>M24 broad audit<br/>M24 tuning<br/>M25 local PostToolUse advisory<br/>M26 baseline/treatment eval<br/>M27 no-go decision"]
    OK["Current allowed state<br/>local non-blocking advisory<br/>manual checklist/reviewer aid<br/>discovery as present_unverified<br/>HTML as orientation_only_not_proof"]
    NO["Blocked or approval-required<br/>CI promotion<br/>blocker enforcement<br/>stronger advisory claim<br/>real behavior-improvement claim<br/>provider/browser/target/git/release actions<br/>active automation or auto-apply"]

    E1["Evidence: S1 template/workflow tests"]
    E2["Evidence: S2 retrofit tests"]
    E3["Evidence: S3 eval/discovery/HTML tests"]
    E4["Evidence: S4 docs/nav/source tests"]
    E5["Evidence: S5 self-learning/automation tests"]
    E6["Evidence: manual pilot, 6 real code tasks"]
    E7["Evidence: M25 replay exits 0, blocking false"]
    E8["Evidence: M26 treatment below baseline"]

    R --> C --> A --> I --> V
    I --> E1
    I --> E2
    I --> E3
    I --> E4
    I --> E5
    I --> E6
    V --> E7 --> OK
    V --> E8 --> NO
    V --> OK
    V --> NO

    class R source
    class C,A contract
    class I,V surface
    class E1,E2,E3,E4,E5,E6,E7,E8 evidence
    class OK allowed
    class NO blocked
```

## Map 2: `B45-PCA` Task Dependency DAG

```mermaid
flowchart TB
    classDef p0 fill:#fff5f5,stroke:#e03131,color:#102a43
    classDef p1 fill:#fff9db,stroke:#f08c00,color:#102a43
    classDef p2 fill:#e7f5ff,stroke:#1c7ed6,color:#102a43
    classDef done fill:#e6fcf5,stroke:#0ca678,color:#102a43
    classDef nogo fill:#ffe3e3,stroke:#c92a2a,color:#102a43

    subgraph S0["B45-S0: Research and activation policy"]
        direction TB
        M01["M01<br/>synthesis ledger"]
        M20["M20<br/>activation trigger policy"]
    end

    subgraph S1["B45-S1: Artifact and workflow contracts"]
        direction TB
        M02["M02<br/>checklist contract"]
        M03["M03<br/>workflow contract"]
        M04["M04<br/>task packet contract"]
    end

    subgraph S2["B45-S2: Existing workflow retrofit"]
        direction TB
        M05["M05<br/>development standards"]
        M06["M06<br/>planning/review artifacts"]
        M07["M07<br/>implementation workflows"]
        M08["M08<br/>legacy/refactor workflows"]
        M09["M09<br/>API/dependency/quality"]
        M15["M15<br/>agent/subagent handoff"]
        M17["M17<br/>high-risk domain workflows"]
    end

    subgraph S3["B45-S3: Evals, visibility and governance"]
        direction TB
        M10["M10<br/>behavioral eval cases"]
        M11["M11<br/>agent-context contract"]
        M16["M16<br/>acceptance/test/eval matrix"]
        M18["M18<br/>readiness/discovery routes"]
        M21["M21<br/>hook governance plan"]
        M22["M22<br/>runtime route and HTML visibility"]
    end

    subgraph S4["B45-S4: Public docs and regression tests"]
        direction TB
        M12["M12<br/>public docs"]
        M13["M13<br/>focused regression tests"]
        M19["M19<br/>cross-links"]
        M14a["M14<br/>closure through S4"]
    end

    subgraph S5["B45-S5: Learning candidates and closure"]
        direction TB
        M23["M23<br/>candidate-only improvement policy"]
        M14b["M14<br/>full source closure after M23"]
        PILOT["Manual pilot<br/>6 code tasks"]
    end

    subgraph S6["B45-S6: Advisory validation and behavior proof"]
        direction TB
        M24["M24<br/>broad false-positive audit"]
        M24T["M24 tuning<br/>reviewer-sized defaults"]
        M25["M25<br/>local non-blocking advisory"]
        M26["M26<br/>live baseline/treatment eval"]
        M27["M27<br/>promotion no-go decision"]
    end

    M01 --> M20
    M20 --> M02
    M02 --> M03
    M03 --> M04
    M04 --> M05
    M04 --> M15
    M05 --> M06
    M06 --> M07
    M07 --> M08
    M07 --> M09
    M08 --> M17
    M09 --> M17
    M10 --> M16
    M11 --> M16
    M15 --> M11
    M17 --> M18
    M16 --> M18
    M18 --> M21
    M18 --> M22
    M21 --> M22
    M12 --> M19
    M13 --> M19
    M19 --> M14a
    M14a --> M23
    M23 --> M14b
    M14b --> PILOT
    PILOT --> M24
    M24 --> M24T
    M24T --> M25
    M25 --> M26
    M26 --> M27

    S0NOTE["Reading order is top to bottom.<br/>Side edges show cross-slice dependencies,<br/>not permission to skip earlier rows."]
    S0NOTE -.-> M01

    class M01,M02,M03,M04,M10,M13,M15,M16,M20,M21,M23,M24,M25,M26 p0
    class M05,M06,M07,M08,M09,M11,M12,M17,M18,M19,M22,M27 p1
    class M14a,M14b p0
    class PILOT p2
    class M01,M02,M03,M04,M05,M06,M07,M08,M09,M10,M11,M12,M13,M14a,M14b,M15,M16,M17,M18,M19,M20,M21,M22,M23,M24,M24T,M25,M26 done
    class M27 nogo
```

## Map 3: Task-Level Standard Execution Pipeline

```mermaid
flowchart TD
    classDef gate fill:#e7f5ff,stroke:#1c7ed6,color:#102a43
    classDef artifact fill:#e6fcf5,stroke:#0ca678,color:#102a43
    classDef stop fill:#ffe3e3,stroke:#c92a2a,color:#102a43
    classDef proof fill:#f3f0ff,stroke:#7950f2,color:#102a43

    T0["Incoming task"]
    T1{"Non-mechanical code work?"}
    NA["Record not_applicable reason<br/>and reduced evidence path"]
    G1["Read source-of-truth docs,<br/>local patterns, helpers and tests"]
    G2["enterprise_leverage_check"]
    L1["Try delete/reduce"]
    L2["Try config"]
    L3["Try stdlib/language construct"]
    L4["Try framework/platform API"]
    L5["Try current dependency"]
    L6["Try project helper/existing abstraction"]
    L7["Tiny adapter or small custom code"]
    L8["New dependency only with approval"]
    G3["one_line_candidate"]
    G4["negative_dependency_rule"]
    G5{"Shared module, API, schema,<br/>runtime, data or generated code?"}
    G6["deep_module_check"]
    G7{"Legacy/refactor risk?"}
    G8["legacy_seam_check<br/>characterization or regression evidence"]
    G9["comment_policy<br/>why/invariant/risk, not obvious restatement"]
    G10["cleverness_budget<br/>simplest readable solution"]
    G11["tests/evals/runtime/manual evidence"]
    G12["completion gate<br/>claim only what evidence proves"]

    S1["STOP: no existing-capability scan<br/>before custom code"]
    S2["STOP: dependency without owner,<br/>risk and rollback"]
    S3["STOP: shared/runtime change<br/>without deep module check"]
    S4["STOP: legacy rewrite<br/>without characterization evidence"]
    S5["STOP: ready/fixed/works claim<br/>without current evidence"]

    T0 --> T1
    T1 -- "no" --> NA
    T1 -- "yes" --> G1
    G1 --> G2
    G2 --> L1 --> L2 --> L3 --> L4 --> L5 --> L6 --> L7 --> L8
    G2 --> G3
    G3 --> G4
    G4 --> G5
    G5 -- "yes" --> G6
    G5 -- "no" --> G7
    G6 --> G7
    G7 -- "yes" --> G8
    G7 -- "no" --> G9
    G8 --> G9
    G9 --> G10
    G10 --> G11
    G11 --> G12

    G1 -. missing .-> S1
    G4 -. missing .-> S2
    G5 -. yes and missing proof .-> S3
    G7 -. yes and no characterization .-> S4
    G12 -. unsupported claim .-> S5

    class G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 gate
    class NA,L1,L2,L3,L4,L5,L6,L7,L8 artifact
    class G11,G12 proof
    class S1,S2,S3,S4,S5 stop
```

## Map 4: Activation And Promotion State Machine

```mermaid
stateDiagram-v2
    [*] --> PlannedContract: B45-S0
    PlannedContract --> StagedArtifacts: S1 templates
    StagedArtifacts --> RetrofittedWorkflows: S2 retrofit
    RetrofittedWorkflows --> VisibleRecommendation: S3 discovery/runtime/HTML visibility
    VisibleRecommendation --> PublicDocs: S4 docs and cross-links
    PublicDocs --> CandidateLearning: S5 candidate-only learning policy
    CandidateLearning --> BroadAudit: M24 broad audit
    BroadAudit --> TunedAdvisory: M24 tuning
    TunedAdvisory --> LocalAdvisory: M25 approved local PostToolUse advisory
    LocalAdvisory --> LiveBehaviorEval: M26 approved baseline/treatment eval
    LiveBehaviorEval --> KeepAdvisoryOnly: M27 no-go decision

    KeepAdvisoryOnly --> [*]

    LocalAdvisory --> BlockerRejected: non-zero blocker not approved
    LocalAdvisory --> CIRejected: CI workflow not approved
    CandidateLearning --> AutomationRejected: auto-apply and schedules not approved
    LiveBehaviorEval --> ImprovementRejected: treatment 3.88 below baseline 4.22

    state KeepAdvisoryOnly {
        [*] --> AllowedLocal
        AllowedLocal: local non-blocking advisory
        AllowedLocal --> DisablePath
        DisablePath: B45_COMMENT_ADVISORY_DISABLED=1
    }
```

## Map 5: Entity Dependency Inventory

| Entity | Depends on | Produces | Current claim ceiling |
| --- | --- | --- | --- |
| Research packet | External style, refactoring, testing, security and maintainability sources; local audit | Professional coding synthesis | Research support, not implementation proof |
| `development-standards.md` | Product hypothesis, architecture boundary, tests, review, evidence-before-completion | Parent workflow loop | Workflow guidance only |
| `coding-standards.md` workflow template | B45 synthesis, development standards, source policy | Task-level coding sub-gate | Staged workflow contract |
| `coding-standard-checklist.md` | Coding workflow and task context | Task evidence packet | Review artifact, not correctness proof |
| `agent-task-packet.md` | Task lifecycle, ownership, approval boundaries, coding checklist | Fresh-context handoff | Handoff contract, not raw conversation history |
| Agent profiles and subagent packets | Coding contract plus role ownership | Builder/reviewer/architect/tester prompts carry fields | Prompt/template contract, not auto-dispatch |
| Behavioral eval cases | Shortcut anti-patterns and expected failures | Deterministic checks for bloat/dependency/comment/rewrite issues | Local eval coverage |
| Discovery/readiness route | Methodology catalog, synthesis, discovery, first-run analysis | `present_unverified` recommendation | Detection, not enforcement |
| Runtime route and HTML | Analysis renderer, status dashboard, runtime contracts | Visible coding-standard state | `orientation_only_not_proof` |
| Self-Learning Loop policy | Metrics, owner feedback, eval failures, manual pilot evidence | Candidate update packet | Candidate-only; no auto-apply |
| Comment sufficiency validator | Python/JS source parser and tuned defaults | Advisory warnings | Reviewer signal only |
| Local PostToolUse advisory | M24 tuning, approved hook wiring, rollback | Exit 0 warning surface | `runtime_enabled_local`, non-blocking |
| M26 eval plan/results | Held-out tasks, baseline/treatment runs, reviewer rubric | Behavior-improvement measurement | `no_go`, no promotion |
| M27 decision | M24, M25, M26 evidence | Keep advisory-only state | Blocks CI/blocker/stronger promotion |

## Map 6: Evidence Plane And Claim Boundaries

```mermaid
flowchart TD
    classDef green fill:#d3f9d8,stroke:#2f9e44,color:#102a43
    classDef amber fill:#fff3bf,stroke:#f08c00,color:#102a43
    classDef red fill:#ffe3e3,stroke:#c92a2a,color:#102a43
    classDef neutral fill:#edf2ff,stroke:#4263eb,color:#102a43

    E0["Current verification evidence"]
    E1["Template and artifact tests"]
    E2["Docs/check_docs/diff hygiene"]
    E3["Fixture/behavioral/discovery/status tests"]
    E4["Manual pilot: six real code tasks"]
    E5["M24 broad audit: 130 warnings"]
    E6["M24 tuning: visible warnings 30"]
    E7["M25 local advisory: exit 0, blocking false"]
    E8["M26 live eval: baseline 4.22, treatment 3.88"]
    E9["M27 decision: keep advisory-only"]

    C1["Can claim: standards are source-owned and test-visible"]
    C2["Can claim: local advisory mechanics work"]
    C3["Can claim: warning volume can be tuned to reviewer-sized output"]
    C4["Cannot claim: treatment improved AI-agent behavior"]
    C5["Cannot claim: CI or blocker enforcement"]
    C6["Cannot claim: production/runtime/browser/readiness"]
    C7["Cannot claim: automation or Self-Learning auto-apply"]

    E0 --> E1 --> C1
    E0 --> E2 --> C1
    E0 --> E3 --> C1
    E0 --> E4 --> C1
    E5 --> E6 --> C3
    E6 --> E7 --> C2
    E8 --> C4
    E9 --> C2
    E9 --> C5
    E9 --> C6
    E9 --> C7

    class E0,E1,E2,E3,E4 neutral
    class E6,E7,E9 green
    class E5 amber
    class E8,C4,C5,C6,C7 red
    class C1,C2,C3 green
```

## Current Solution Reading

The full solution is a governance and evidence system, not a single linter.
It has three nested loops:

1. `development-standards.md` is the parent product/architecture/test/review
   loop.
2. `coding-standards.md` is the non-mechanical code authoring sub-gate.
3. `comment_sufficiency` is one local advisory signal inside that sub-gate,
   not the whole standard.

The important dependency is directional:

```text
research -> synthesis -> task artifacts -> workflow/agent/eval visibility
-> advisory validation -> behavior eval -> promotion decision
```

The reverse direction is forbidden. A green local advisory replay cannot
retroactively prove real agent behavior, and a generated HTML section cannot
become source truth.

## Operational Conditions

| Condition | Required evidence | If missing |
| --- | --- | --- |
| Non-mechanical code task | Checklist or explicit `not_applicable` reason | Stop or reduce claim |
| New custom code | Existing capability scan, leverage path, rejected options | Stop |
| New dependency | Negative dependency rule, owner, risk, rollback, approval | Stop |
| Shared/public/runtime module | Deep module check, consumers, error paths, tests | Stop or accepted gap |
| Legacy/refactor work | Characterization/regression evidence, seam strategy, rollback | Stop or accepted gap |
| Comment sufficiency warning | Reviewer handling or explicit reason | Advisory only |
| Completion claim | Current tests/evals/runtime/owner evidence or accepted gap | Do not claim complete |
| Promotion to CI/blocker | Positive behavior eval, false-positive/flake/cost proof, rollback, approval | Forbidden by current M27 |
| Provider/model rerun | Fresh exact approval and privacy-safe eval packet | Approval required |
| Target/browser/runtime proof | Exact surface, owner, rollback and evidence path | Approval required |

## Current State Summary

| Slice | Status | What it proves | What it does not prove |
| --- | --- | --- | --- |
| S0 | `docs_contract_ready` | Research synthesis and activation policy exist. | Runtime or behavior improvement. |
| S1 | `docs_contract_ready` | Core workflow/checklist/task-packet contracts exist and are registered. | Automatic agent compliance. |
| S2 | `docs_contract_ready` | Existing workflows, agent roles and high-risk templates carry the contract. | Hook activation or live behavior. |
| S3 | `docs_contract_ready` | Eval cases, discovery/readiness and HTML visibility exist. | Generated views as proof. |
| S4 | `docs_contract_ready` | Public docs and cross-links exist. | Root site freshness beyond approved evidence or live enforcement. |
| S5 | `synthetic_green` | Learning-loop improvements are candidate-only and gated. | Active automation or auto-apply. |
| M24 | `local_audit_evidence_no_enforcement` | Broad false-positive profile is known. | Blocking readiness. |
| M24 tuning | `synthetic_green` | Default advisory warning volume is reduced. | Behavior improvement. |
| M25 | `runtime_enabled_local` | Approved local non-blocking advisory runs and exits 0. | CI/blocker enforcement. |
| M26 | `live_dependency_aligned` with `no_go` | Live eval falsified current treatment promotion. | Positive AI-agent behavior improvement. |
| M27 | `docs_contract_ready` no-go decision | Keep advisory-only decision is recorded. | Stronger advisory, CI or blocker approval. |

## Practical Next View

If the team wants the next map to become executable rather than descriptive,
the next artifact should be a `B45 treatment v2 design packet` with:

- a smaller treatment surface than the full coding-standard context;
- changed-file advisory response protocol;
- timeout and flake budget;
- deterministic validation-selection rubric;
- explicit handling for read-only `.codex` or target workspaces;
- same held-out task set or a new approved held-out set;
- promotion threshold that requires treatment above baseline, no critical
  regressions and zero blocker-worthy timeouts.

Until that packet exists and passes, the correct operating state remains:

```text
local advisory only -> reviewer signal -> no CI -> no blocker -> no real behavior-improvement claim
```
