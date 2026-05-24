# First-Run Intake

Source status: `codex-plugin-template`

Project: {project_name}
Profile: {profile_name}

## Inputs

- User request:
- Workspace signals:
- Existing control-plane files:
- Missing control-plane files:
- Approval limits:

## Process

1. Classify `usage_mode` with `primary`, `secondary`, `confidence`, `reasons` and `fallback`.
2. Return the first response contract before any method dump: mode, confidence, next smallest action, minimum artifacts, evidence gaps and approval boundary.
3. If confidence is low, ask at most one blocking question or choose the safest read-only fallback.
4. Mark scenario coverage as `done`, `partial`, `pending` or `not_applicable`.
5. State the next smallest action and the minimum artifacts for the selected mode.
6. For `partial` or `pending` modes, name the required artifact and the evidence, workflow, or template gap.
7. Name the approval boundary before any write, scaffold, hook activation, automation, parallelization or external action.
8. Keep advanced methodology gates as later proposals unless the selected mode requires them.

## Entry Scenarios

| Entry signal | Primary mode | First safe action | Safety boundary |
| --- | --- | --- | --- |
| Empty workspace or idea note | `greenfield_idea` | Draft `greenfield idea brief` and first vertical slice. | Do not scaffold before product direction, minimum artifacts and approval boundary are explicit. |
| Failed verification, stuck bug work or candidate failing logs | `bug_rescue` | Draft `bug rescue report`, list reproduction evidence and missing current evidence. | Do not fix, do not rewrite broadly and do not claim a fix before reproduction or owner evidence. |
| Existing control-plane files such as `AGENTS.md` or `.codex/config.toml` | `maintenance` | Preserve existing control-plane, report missing control-plane files and propose one next action. | Do not regenerate, overwrite or ignore existing control-plane content without approval. |
| Complex system, monorepo, web/API/integration-heavy workspace | `complex_system_acceleration` | Draft integration catalog, ownership split and release gates. | Do not parallelize before ownership boundaries, external systems, release gates and overlapping files are explicit. |

## Outputs

- `usage_mode`:
- Confidence:
- Reasons:
- Fallback:
- Scenario status:
- Next smallest action:
- Minimum artifacts:
- Missing workflow or template gap:
- Approval boundary:
- Evidence gaps:
- Missing evidence:

## Verification

- The first response names mode, confidence and evidence gaps.
- The first response names next smallest action, minimum artifacts and approval boundary.
- The first response distinguishes packaged workflows from partial or pending gates.
- The first response asks at most one necessary question.
- The first response does not dump every methodology gate.
- The first response does not scaffold before approval.
- The first response does not fix before reproduction evidence.
- The first response does not regenerate existing control-plane files without approval.
- The first response does not parallelize complex system work before ownership split.
- Safety phrase: do not scaffold until product direction, minimum artifacts and approval boundary are explicit.
- Safety phrase: do not fix until reproduction evidence or owner-confirmed failure evidence is explicit.
- Safety phrase: do not regenerate existing control-plane files without approval.
- Safety phrase: do not parallelize until ownership split, external system boundaries and release gates are explicit.
- Safety phrase: do not dump every methodology gate before the selected mode needs it.

## Stop Conditions

- Workspace path is unclear.
- User intent conflicts with safety, source, sandbox or approval rules.
- Required write approval is missing.
- Secrets, customer data or external systems are required before a safe plan exists.
