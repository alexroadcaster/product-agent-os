# Product-Agent Delivery Lifecycle

Source status: `official + experiment`

This diagram shows the end-to-end product delivery loop for Codex work, from idea to release notes and updated agent operating documentation.

```mermaid
flowchart TD
    A["Idea / user request"] --> B["REQUIREMENTS.md"]
    B --> C["Source review"]
    C --> D["PLAN.md"]
    D --> E["Agent team design"]
    E --> F["Candidate skills"]
    F --> G["Runtime choice"]
    G --> H["Focused implementation"]
    H --> I["TEST.md"]
    H --> J["EVALS.md"]
    I --> K{"Pass?"}
    J --> K
    K -->|No| L["Focused fix loop"]
    K -->|Yes| M["Review"]
    M --> N["Release packet"]
    N --> O["RUNLOG.md learning"]
    O --> P["Rules, skills or automation candidate"]
```

## Inputs

- Product goal, users, constraints and success metric.
- Source review, project rules and available runtime surface.

## Outputs

- A reviewable sequence of requirements, plan, implementation, evidence, review and learning artifacts.
- Candidate skills or automation only after repeated manual success.

## Verification

Confirm that requirements, plan, tests, evals and run log are current before claiming a slice is ready.

## Risks

- Starting implementation before requirements and plan can create broad unowned changes.
- Automating a workflow before evidence and failure handling can repeat mistakes.
