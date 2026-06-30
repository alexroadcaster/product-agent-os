# Batch 45 Professional Code Authoring architecture v2

Source status: `project-authored + derived_from_current_batch45_artifacts`

This internal architecture atlas implements `B45-PCA-M28`. It deepens the
orientation map in `research/batch45-professional-code-authoring-solution-map.md`
into a set of narrower architecture views for the future real-project scenario
harness.

It is not a source-copy approval, not a target-project execution record, not a
runtime proof, not a browser proof, not a provider/model run, not a CI or
blocker promotion, and not evidence that the Professional Code Authoring
treatment improves real AI-agent behavior. The source of truth remains the
Track 11 Batch 45 task matrix, current evidence packets, and current verification
commands.

## Reading Contract

Use this atlas to answer four practical questions before `B45-PCA-M29..M36`:

- What architecture boundary keeps real projects read-only until approval?
- Which components transform real project signals into sanitized fixtures?
- Which data contracts must exist before baseline, refactor and scorecard work?
- Which approval gates prevent `B45-S7` from bypassing the `M27` no-go decision?

The artifact family is a software/system architecture diagram set. The diagrams
are intentionally vertical and decomposed so they remain readable in Codex App
and in Markdown previews.

## Source Ledger

| Source | Role in this atlas |
| --- | --- |
| `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md` | Source of truth for `B45-PCA-M28..M36`, claim ceilings and stop conditions. |
| `research/batch45-professional-code-authoring-solution-map.md` | Prior whole-system orientation map and `M27` no-go context. |
| `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` | Current control-plane boundaries for Batch 45 and real-project evidence. |
| `docs/superpowers/specs/batch45-comment-policy-promotion-decision.json` | `M27` keep-advisory-only/no-go decision. |
| `docs/superpowers/specs/batch45-agent-behavior-eval-results.json` | `M26` baseline/treatment evidence that blocks stronger promotion. |
| `docs/superpowers/specs/batch45-comment-sufficiency-advisory-wiring-summary.json` | `M25` local non-blocking advisory evidence. |

## Architecture Decision

`B45-S7` should be implemented as a staged real-project scenario harness inside
`codex_docs`, not as direct mutation of `myPartners`, `SOL 0.6`, CI, hooks,
provider/model calls, browser automation or installed plugin cache state.

The first executable boundary is:

```text
read-only target inventory -> sanitized fixture policy -> approved fixture copy -> fixture-local baseline -> fixture-local refactor comparison -> scorecard -> decision
```

The current allowed state is architecture and planning evidence only. Source
copying starts only after `B45-PCA-M29` inventory and `B45-PCA-M30` fixture
policy are reviewed and an exact approval names the copy scope.

## Map 1: Context Boundary

```mermaid
flowchart TB
    classDef control fill:#edf2ff,stroke:#4263eb,color:#102a43
    classDef target fill:#fff4e6,stroke:#f08c00,color:#102a43
    classDef harness fill:#e6fcf5,stroke:#0ca678,color:#102a43
    classDef evidence fill:#f3f0ff,stroke:#7950f2,color:#102a43
    classDef blocked fill:#fff5f5,stroke:#c92a2a,color:#102a43

    Owner["Owner decision<br/>approves scope and boundaries"]
    Control["codex_docs control plane<br/>Batch 45 matrix<br/>registry<br/>evidence packets<br/>verification contracts"]
    B45["B45-S7 architecture harness<br/>M28-M36"]
    Targets["Real project candidates<br/>myPartners<br/>SOL 0.6"]
    ReadOnly["Read-only discovery only<br/>paths, tests, commands, risks<br/>no source bodies copied yet"]
    Fixtures["Sanitized fixture packs<br/>inside codex_docs<br/>only after M30 + exact approval"]
    Modules["B45-PCA modules<br/>checklist<br/>existing capability scan<br/>comment advisory<br/>dependency/custom-code review"]
    Score["Scorecard and decision<br/>baseline/refactor comparison<br/>promotion boundary"]
    NoGo["Blocked by default<br/>target mutation<br/>provider/browser/runtime<br/>CI/blocker<br/>git/release/deploy"]

    Owner --> Control --> B45
    B45 --> Targets
    Targets --> ReadOnly
    ReadOnly --> Fixtures
    Fixtures --> Modules --> Score
    B45 --> NoGo

    class Owner,Control,B45 control
    class Targets,ReadOnly target
    class Fixtures,Modules harness
    class Score evidence
    class NoGo blocked
```

## Map 2: Container Architecture

```mermaid
flowchart TB
    classDef component fill:#e6fcf5,stroke:#0ca678,color:#102a43
    classDef data fill:#edf2ff,stroke:#4263eb,color:#102a43
    classDef gate fill:#fff4e6,stroke:#f08c00,color:#102a43
    classDef stop fill:#fff5f5,stroke:#c92a2a,color:#102a43

    subgraph TargetSide["Target side: read-only until approval"]
        direction TB
        T1["Target project path"]
        T2["Project shape inventory"]
        T3["Candidate task and file references"]
        T4["Privacy and source-policy risk notes"]
        T1 --> T2 --> T3 --> T4
    end

    subgraph ControlSide["codex_docs side: controlled writes"]
        direction TB
        H1["Scenario Harvester"]
        H2["Source Sanitizer"]
        H3["Fixture Builder"]
        H4["B45 Standards Engine"]
        H5["Existing Capability Detector"]
        H6["Refactor Planner"]
        H7["Test Runner Adapter"]
        H8["Scorecard and Evidence Ledger"]
        H9["Promotion Governor"]
        H1 --> H2 --> H3 --> H4 --> H5 --> H6 --> H7 --> H8 --> H9
    end

    subgraph Gates["Mandatory gates"]
        direction TB
        G1["M29 read-only inventory"]
        G2["M30 fixture policy"]
        G3["M31 exact copy approval"]
        G4["M32 baseline before refactor"]
        G5["M35 decision before promotion"]
        G6["M36 exact runtime/browser approval"]
        G1 --> G2 --> G3 --> G4 --> G5 --> G6
    end

    T4 --> H1
    Gates --> ControlSide

    Stop1["Stop: no unbounded repo copy"]
    Stop2["Stop: no raw private data"]
    Stop3["Stop: no target mutation"]
    Stop4["Stop: no CI/blocker promotion after M27 no-go"]

    G2 --> Stop1
    G2 --> Stop2
    G3 --> Stop3
    G5 --> Stop4

    class H1,H2,H3,H4,H5,H6,H7,H8,H9 component
    class T1,T2,T3,T4 data
    class G1,G2,G3,G4,G5,G6 gate
    class Stop1,Stop2,Stop3,Stop4 stop
```

## Component Responsibility Matrix

| Component | Owns | Inputs | Outputs | Stop condition |
| --- | --- | --- | --- | --- |
| Scenario Harvester | Real-project candidate discovery | Target paths, current plans, tests, package/config files | `scenario-candidates.json` | Requires mutation, runtime or private data to understand the scenario |
| Source Sanitizer | Privacy and source-policy filtering | Candidate files and risk notes | redaction policy, allowed/forbidden file classes | Secrets, credentials, raw chats, customer data or production databases are required |
| Fixture Builder | Minimal copied scenario context | Approved scenario list, fixture policy | fixture directories and manifests | Copy scope is unapproved or dependency closure is too large |
| B45 Standards Engine | Professional Code Authoring checks | Fixture source and task packet | checklist findings and accepted gaps | No baseline or checklist fields exist |
| Existing Capability Detector | Reuse and deletion-first review | Source graph, imports, project APIs | reuse options, rejected options, custom-code risk | Project capability cannot be inspected safely |
| Refactor Planner | Fixture-local refactor variants | Baseline findings, accepted scenarios | original/checklist/advisory arms | Refactor would require target mutation or external services |
| Test Runner Adapter | Safe local checks | Fixture commands, test metadata | pass/fail/skip evidence | Test command leaves fixture boundary or calls live services |
| Scorecard and Evidence Ledger | Comparable outcome evidence | Baseline/refactor results | scorecard, gaps, reviewer notes | Score hides critical regression or unsupported claim |
| Promotion Governor | Next-state decision | Scorecard, M27 boundary, owner review | keep advisory, treatment v2, more pilots, no-go | Promotion bypasses approval or M27 no-go evidence |

## Map 3: Data Contract Topology

```mermaid
erDiagram
    REAL_PROJECT_TARGET ||--o{ SCENARIO_CANDIDATE : provides
    SCENARIO_CANDIDATE ||--|| SOURCE_POLICY_REVIEW : requires
    SOURCE_POLICY_REVIEW ||--o{ FIXTURE_MANIFEST : allows
    FIXTURE_MANIFEST ||--o{ BASELINE_RUN : tested_by
    BASELINE_RUN ||--o{ REFACTOR_ARM : compared_with
    REFACTOR_ARM ||--o{ COMPARISON_RESULT : produces
    COMPARISON_RESULT ||--|| SCORECARD : summarized_by
    SCORECARD ||--|| DECISION_PACKET : informs

    REAL_PROJECT_TARGET {
        string target_label
        string absolute_path_not_persisted
        string read_only_status
        string approval_boundary
    }
    SCENARIO_CANDIDATE {
        string scenario_id
        string project_label
        string task_class
        string relative_paths
        string expected_checks
    }
    SOURCE_POLICY_REVIEW {
        string allowed_file_classes
        string forbidden_data
        string redaction_notes
        string copy_approval_status
    }
    FIXTURE_MANIFEST {
        string fixture_id
        string source_digest
        string copied_paths
        string omissions
        string runnable_status
    }
    BASELINE_RUN {
        string run_id
        string command_scope
        string standards_findings
        string test_status
    }
    REFACTOR_ARM {
        string arm_id
        string arm_type
        string diff_summary
        string dependency_delta
    }
    COMPARISON_RESULT {
        string scenario_id
        string baseline_status
        string refactor_status
        string regression_signal
    }
    SCORECARD {
        string existing_capability_reuse
        string custom_code_reduction
        string privacy_safety
        string reviewer_usefulness
    }
    DECISION_PACKET {
        string decision_state
        string next_approval_boundary
        string unsupported_claims
        string rollback_or_delete_path
    }
```

## Map 4: Execution Sequence

```mermaid
sequenceDiagram
    participant Owner
    participant Codex as Codex App
    participant Target as Real target project
    participant Research as codex_docs research
    participant Fixture as Sanitized fixture
    participant B45 as B45-PCA modules
    participant Score as Scorecard

    Owner->>Codex: Start B45-PCA-M28
    Codex->>Research: Create Architecture v2 atlas
    Research-->>Owner: Architecture only, no source copy

    Owner->>Codex: Later approve M29 read-only inventory
    Codex->>Target: Inspect files and task signals read-only
    Target-->>Codex: Relative paths, commands, risks, counts
    Codex->>Research: Write scenario candidates

    Owner->>Codex: Later approve M31 copy scope
    Codex->>Fixture: Copy minimal sanitized files
    Fixture-->>B45: Provide local scenario input
    B45-->>Score: Baseline and refactor comparison
    Score-->>Owner: M35 decision packet
```

## Map 5: Approval Boundary

```mermaid
flowchart TB
    classDef allowed fill:#d3f9d8,stroke:#2f9e44,color:#102a43
    classDef gated fill:#fff4e6,stroke:#f08c00,color:#102a43
    classDef forbidden fill:#fff5f5,stroke:#c92a2a,color:#102a43

    Start["B45-S7 work item"]
    A1["Allowed now<br/>architecture atlas<br/>source-backed planning<br/>claim ceiling"]
    A2["Allowed after M29 approval<br/>read-only target inventory<br/>no source bodies copied"]
    A3["Allowed after M30 + M31 approval<br/>minimal sanitized fixture copy<br/>inside codex_docs"]
    A4["Allowed after fixture exists<br/>fixture-local baseline and refactor comparison"]
    A5["Allowed after M35<br/>treatment v2 proposal or no-go"]

    F1["Forbidden without exact approval<br/>target mutation"]
    F2["Forbidden without exact approval<br/>browser/runtime/provider/API"]
    F3["Forbidden by M27 unless fresh evidence changes state<br/>CI/blocker promotion"]
    F4["Forbidden always in fixtures<br/>secrets, credentials, raw private chats, customer data"]

    Start --> A1 --> A2 --> A3 --> A4 --> A5
    Start --> F1
    Start --> F2
    Start --> F3
    Start --> F4

    class A1 allowed
    class A2,A3,A4,A5 gated
    class F1,F2,F3,F4 forbidden
```

## Map 6: `B45-S7` Dependency Path

```mermaid
flowchart TB
    classDef done fill:#d3f9d8,stroke:#2f9e44,color:#102a43
    classDef planned fill:#edf2ff,stroke:#4263eb,color:#102a43
    classDef gated fill:#fff4e6,stroke:#f08c00,color:#102a43
    classDef stop fill:#fff5f5,stroke:#c92a2a,color:#102a43

    M27["M27<br/>keep advisory-only no-go"]
    M28["M28<br/>Architecture v2 atlas"]
    M29["M29<br/>read-only real-project inventory"]
    M30["M30<br/>fixture source-policy contract"]
    M31["M31<br/>approved fixture packs"]
    M32["M32<br/>baseline analysis"]
    M33["M33<br/>fixture-local refactor comparison"]
    M34["M34<br/>scorecard calibration"]
    M35["M35<br/>treatment v2 decision"]
    M36["M36<br/>optional runtime/browser pilot approval packet"]

    M27 --> M28 --> M29 --> M30 --> M31 --> M32 --> M33 --> M34 --> M35 --> M36

    StopA["Stop if copy approval missing"]
    StopB["Stop if baseline missing"]
    StopC["Stop if promotion bypasses M35"]
    StopD["Stop if runtime/browser lacks M36 approval"]

    M30 --> StopA
    M32 --> StopB
    M35 --> StopC
    M36 --> StopD

    class M27 done
    class M28 planned
    class M29,M30,M32,M33,M34,M35 planned
    class M31,M36 gated
    class StopA,StopB,StopC,StopD stop
```

## Scorecard Dimensions

| Dimension | Why it exists | Primary evidence |
| --- | --- | --- |
| Existing-capability reuse | Proves the agent found simpler project/framework paths before custom code. | Checklist findings, imports, local APIs inspected, rejected options. |
| Custom-code reduction | Measures whether refactor reduces surface area instead of adding ceremony. | Diff size, deleted code, wrapper count, dependency delta. |
| Dependency avoidance | Prevents new packages or services where standard APIs already work. | Dependency manifest delta, rejected package notes. |
| Comment sufficiency | Preserves useful comments while avoiding noisy obvious comments. | Comment advisory warnings, accepted gaps, reviewer notes. |
| Test and scenario coverage | Keeps code-quality claims tied to executable or accepted-gap evidence. | Fixture-local test runs, skipped commands, baseline/refactor comparison. |
| Unsupported-claim discipline | Prevents generated reports from becoming runtime or promotion proof. | Claim ledger, source status, decision packet. |
| Privacy and source safety | Keeps real-project evidence usable without exposing private data. | Source-policy review, redaction manifest, forbidden-data scan. |
| Reviewer usefulness | Measures whether the output helps a human make a better code decision. | Reviewer score, actionability notes, false-positive notes. |
| Runtime gap | Separates fixture proof from live/browser/provider behavior. | M36 approval status and explicit unsupported claims. |

## Fitness Functions

`B45-S7` architecture is healthy only if these checks remain true:

1. Every real-project scenario has a target label, task class, relative path
   list and approval boundary before any fixture exists.
2. No fixture copies `.env`, credentials, private keys, raw private chats,
   customer data, production databases, private logs or unbounded repository
   contents.
3. Every fixture has a manifest that names copied paths, omitted paths, source
   digest policy, redactions and delete/rollback path.
4. Every refactor comparison has a baseline result first.
5. Every scorecard separates supported evidence from unsupported runtime,
   browser, provider, CI, blocker, git, release and production-readiness claims.
6. `M27` remains the controlling promotion boundary until `M35` records a new
   owner-reviewed decision with fresh evidence.

## `B45-PCA-M28` Completion Scope

This `M28` implementation provides:

- Architecture v2 context, container, data-contract, sequence, approval-boundary
  and scorecard views.
- Component responsibilities and stop conditions for the future harness.
- A dependency path for `B45-PCA-M29..M36`.
- Claim ceilings that preserve `M27` no-go and approval-required boundaries.

This `M28` implementation does not provide:

- read-only inventory of `myPartners` or `SOL 0.6`;
- copied source fixtures;
- sanitized fixture manifests;
- baseline analysis;
- fixture-local refactor results;
- real target runtime, browser, provider/API or git proof;
- CI, blocker, stronger advisory or production-readiness promotion.

The next safe action is `B45-PCA-M29`: read-only scenario inventory for the
approved real-project candidates.
