# Agent team and skills

Source status: `official + experiment`

This page shows how to design an agent team around ownership, handoffs, model/reasoning policy, skills and stop conditions.

```mermaid
flowchart TD
    A["Work item"] --> B["Read project rules"]
    B --> C["Define ownership"]
    C --> D["Choose roles"]
    D --> E["Assign files or subsystems"]
    E --> F["Define handoff artifacts"]
    F --> G["Run focused work"]
    G --> H{"Repeated method?"}
    H -->|No| I["Keep as playbook"]
    H -->|Yes| J["Skill candidate"]
    J --> K["Eval cases and failure log"]
    K --> L{"Reliable enough?"}
    L -->|No| M["Improve method"]
    L -->|Yes| N["Package as reusable skill"]
```

## Inputs

- Implementation plan, source context, ownership boundaries and approval limits.
- Available skills, subagents and verification gates.

## Outputs

- Role cards with owned files, model policy, handoff schema and stop conditions.
- A safe route for skill promotion when a method repeats.

## Verification

Each handoff must include sources used, assumptions, files touched or proposed, verification evidence, open risks and recommended next role.

## Risks

- Parallel workers without disjoint ownership can overwrite each other.
- A skill created before manual success can encode a brittle method.
