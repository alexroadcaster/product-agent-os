# Архитектура проекта

Source status: `experiment`

Эта страница остается общей архитектурной картой базы знаний. Для реализации реальных проектов начинайте с [Diagram atlas](index.md), затем переходите к lifecycle, agent team, runtime, skill и verification схемам.

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

## Agent workflow pipeline

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
    M->>S: Write learning material
    S-->>M: Draft + source notes
    M->>KB: Apply approved docs changes
    M-->>U: Summary + verification evidence
```

## Runtime layer map

```mermaid
flowchart TD
    C["Codex App / CLI / IDE"] --> P["Playbooks and AGENTS.md"]
    P --> S["Skills"]
    S --> SA["Subagents"]
    SA --> ASDK["Agents SDK"]
    ASDK --> RAPI["Responses API"]
    ASDK --> MCP["Codex MCP"]
    RAPI --> TOOLS["Tools and structured outputs"]
    MCP --> WS["Workspace execution"]
    ASDK --> TR["Tracing and evals"]
```

## Hallucination control loop

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
