# Архитектура проекта

Source status: `official + experiment`

Карта разделяет источники, выполняемую работу и evidence. Для обычной задачи один агент может последовательно выполнить research, verification и synthesis. Командный sequence — условный пример, не обязательный runtime.

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

## Как использовать и проверить

Выберите [delivery route](product-delivery-lifecycle.md) по размеру задачи. Runtime app выбирайте по [владению loop/state](../agent-systems/sdk-patterns.md): Codex subagents не требуют Agents SDK. JSON schema, guardrail и отдельный Verifier не гарантируют factual correctness. Проверяйте источники, наблюдаемый результат и применимые checks. Документы и схемы не активируют hooks, providers, Git или deployment.

## Типовые ошибки

Обязательная команда без независимых задач; смешение generated artifacts и source truth; рост verification loop без budget/stop condition; автоматическая публикация результата без authority.

## Входы

Цель пользователя, текущие источники, ограничения, ownership и применимые разрешения.

## Выходы

Выбранный маршрут, проверяемый artifact и evidence с явными ограничениями.

## Проверка

Сверьте маршрут с исходниками и наблюдаемым результатом; после изменения синтаксиса проверьте render.

## Риски

Диаграмма помогает навигации, но не доказывает runtime activation или release.
