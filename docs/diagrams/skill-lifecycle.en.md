# Skill lifecycle

Source status: `official + experiment`

This diagram shows how a repeated workflow becomes a reusable skill and later an automation candidate only after evidence exists.

```mermaid
flowchart LR
    A["Manual workflow"] --> B["Playbook"]
    B --> C["Skill candidate"]
    C --> D["Trigger, inputs, outputs"]
    D --> E["Eval cases"]
    E --> F["Failure log"]
    F --> G{"Reliable?"}
    G -->|No| H["Refine manually"]
    G -->|Yes| I["Reusable skill"]
    I --> J{"Stable cadence?"}
    J -->|No| K["Assisted runs"]
    J -->|Yes| L["Automation candidate"]
```

## Inputs

- A successful manual workflow, playbook, source policy and failure examples.
- Candidate trigger words, inputs, outputs and verification command.

## Outputs

- A skill with one job, explicit boundaries, eval cases and failure modes.
- A promotion decision for keeping the method manual, packaging it or proposing automation.

## Verification

Run positive and negative eval cases before treating the skill as reusable. Automation still requires separate approval.

## Risks

- A broad skill can hide unrelated behavior under one trigger.
- Automation without stable inputs, outputs and rollback can create repeated unsafe actions.
