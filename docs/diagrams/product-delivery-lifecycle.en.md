# Product-Agent Delivery Lifecycle

Source status: `official + experiment`

Choose a route by task and risk. The diagram describes a workflow; it does not grant authority.

```mermaid
flowchart TD
    A["User goal and current sources"] --> B{"Scope size and risk"}
    B -->|Ordinary| C["Concise scope; reuse artifacts"]
    B -->|Large or high risk| D["Requirements, plan and ownership"]
    D --> E{"Independent work benefits from delegation?"}
    E -->|No| F["One agent"]
    E -->|Yes and authorized| G["Bounded team with handoffs"]
    C --> F
    F --> H["Focused change in authorized workspace"]
    G --> H
    H --> I["Affected tests; eval or visual check when applicable"]
    I --> J{"Required checks pass?"}
    J -->|No| K["Repair or report blocker"]
    K --> H
    J -->|Yes| L["Review and evidence"]
    L --> M["Result and limits"]
    M --> N["PR or release only with separate authority"]
```

## Usage

For an ordinary change use scope, the change, relevant verification and the result. Reuse existing `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md`; create artifacts when they capture actual requirements, dependencies or evidence. For larger work define acceptance, ownership, risks and rollback first. A worktree provides file isolation with the required Git authority; it is not mandatory for every task.

One role can cover several stages. Add a team, skills and evals when applicable. Repeat required checks after a new change, failure or unresolved risk. A PR draft is not publication.

## Outputs and verification

A reviewable diff or artifact, observed checks, limits and the next action. Runtime/model activation needs separate evidence; a plan or diagram does not prove it.

## Failure modes

Mandatory teams without independent tasks; duplicate control-plane files; an unbounded general gate; publication without authority.

Related guidance: [lifecycle](../product-agent/lifecycle.md), [Product-Agent OS plugin](../product-agent-os/index.md), [model guidance](https://developers.openai.com/api/docs/guides/latest-model), [eval guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices).

## Inputs

User goal, current sources, constraints, ownership and applicable approvals.

## Outputs

A selected route, reviewable artifact and evidence with explicit limits.

## Verification

Check the selected route against source files and observed task results; render the diagram after syntax changes.

## Risks

A diagram is orientation, not runtime activation or release evidence.
