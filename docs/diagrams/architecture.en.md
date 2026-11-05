# Project architecture

Source status: `official + experiment`

The map separates sources, execution and evidence. One agent can perform research, verification and synthesis sequentially for an ordinary task. The team sequence is a conditional example, not a mandatory runtime.

## Knowledge base pipeline

```mermaid
flowchart TD
    A["Official OpenAI docs"] --> B["Source registry"]
    C["Community sources"] --> D["Insight intake"]
    D --> E{"Verified?"}
    E -->|No| F["docs/insights"]
    E -->|Yes| G["Playbook candidate"]
    B --> H["Codex docs"]
    B --> I["Agent systems docs"]
    G --> J["Playbooks"]
    H --> K["MkDocs build"]
    I --> K
    J --> K
    F --> K
    K --> L["HTML site"]
```

## Optional agent workflow

```mermaid
sequenceDiagram
    participant U as User
    participant M as Main orchestrator
    participant R as Research agent
    participant V as Verification agent
    participant S as Synthesis agent
    participant KB as Knowledge base

    U->>M: Goal + constraints
    M->>R: Source discovery task
    R-->>M: Source cards + claims
    M->>V: Verify claims
    V-->>M: Verified / unsupported / conflicts
    M->>S: Draft learning material
    S-->>M: Draft + source notes
    M->>KB: Apply authorized docs changes
    M-->>U: Summary + verification evidence
```

## Runtime ownership choices

```mermaid
flowchart TD
    C["Codex App / CLI / IDE"] --> P["Playbooks and AGENTS.md"]
    P --> S["Skills"]
    S --> SA["Optional Codex subagents"]
    C --> ASDK["Optional agent application"]
    ASDK --> CHOICE["Choose Agents API / SDK / Responses"]
    CHOICE --> RAPI["Responses API when applicable"]
    ASDK --> MCP["Codex MCP"]
    RAPI --> TOOLS["Tools and structured outputs"]
    MCP --> WS["Workspace execution"]
    ASDK --> TR["Tracing and evals"]
```

## Claim verification loop

```mermaid
flowchart TD
    Q["User question"] --> PC["Prompt contract"]
    SRC["Official sources"] --> CTX["Packed context"]
    MEM["Session / memory"] --> CTX
    CTX --> PC
    PC --> MODEL["GPT model"]
    MODEL --> OUT["Structured answer"]
    OUT --> VER["Verifier / guardrail"]
    VER -->|pass| FINAL["Final answer"]
    VER -->|fail| FIX["Retrieve more / ask clarification / refuse"]
    FIX --> PC
```

## Product-agent operating system

```mermaid
flowchart TD
    REQ["REQUIREMENTS.md"] --> PLAN["PLAN.md"]
    AG["AGENTS.md"] --> PLAN
    PLAN --> SK["Skills"]
    SK --> RUN["Codex runtime"]
    RUN --> DIFF["Code/docs diff"]
    DIFF --> TEST["TEST.md checks"]
    DIFF --> EVAL["EVALS.md"]
    TEST --> LOG["RUNLOG.md"]
    EVAL --> LOG
    LOG --> PR["Product-ready PR"]
    PR --> LEARN["Update AGENTS.md / skills / insights"]
    LEARN --> AG
```

## Usage and verification

Choose a [delivery route](product-delivery-lifecycle.md) by task size. Select an app runtime by [loop/state ownership](../agent-systems/sdk-patterns.md): Codex subagents do not require Agents SDK. JSON schemas, guardrails and a separate Verifier do not guarantee factual correctness. Check sources, observed results and applicable verification. Documents and diagrams do not activate hooks, providers, Git or deployment.

## Failure modes

Mandatory teams without independent tasks; confusing generated artifacts with source truth; verification loops without a budget/stop condition; publishing results without authority.

## Inputs

User goal, current sources, constraints, ownership and applicable approvals.

## Outputs

A selected route, reviewable artifact and evidence with explicit limits.

## Verification

Check the selected route against source files and observed task results; render the diagram after syntax changes.

## Risks

A diagram is orientation, not runtime activation or release evidence.
