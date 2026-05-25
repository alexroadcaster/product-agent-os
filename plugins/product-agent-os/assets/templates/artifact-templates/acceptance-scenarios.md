# Acceptance Scenarios

Source status: `local methodology artifact`

Use this artifact as the ATDD and BDD traceability layer before behavior changes. It does not replace requirements; it links requirements to observable behavior and verification evidence.

## Scope

- Feature or slice:
- Behavior changes:
- Source requirement:
- Non-goal:
- Explicit gap:

## Traceability

Use the chain `requirement -> scenario -> check -> evidence owner`.

| Requirement | Scenario | Check | Evidence owner | Status |
| --- | --- | --- | --- | --- |
|  |  |  |  | `pending | covered | explicit gap` |

## Behavior Scenario

- Scenario id:
- Gate: `declarative_acceptance_scenarios_present`
- Business rule:
- User or actor:
- Given:
- When:
- Then:
- Equivalent behavior format:
- Declarative scenario quality:
- Actor:
- Context:
- Trigger:
- Observable outcome:
- Edge case:
- Non-goal covered:
- Data, privacy, or approval boundary:

## Verification Mapping

- Deterministic check:
- Manual check:
- Contract check:
- Eval:
- Runtime or visual evidence:
- Command or artifact:
- Expected result:
- Evidence owner:

## Boundaries

- Does not replace requirements.
- Does not replace unit tests.
- Does not replace integration tests.
- Does not replace contract tests.
- Does not replace evals.
- BDD describes shared behavior language; it is not a substitute for implementation proof.
- Gherkin is optional; use an equivalent behavior format when it preserves actor, context, trigger, observable outcome and evidence.
- No UI selectors.
- No database internals.
- No function names.
- No test harness details.

## Stop Conditions

- Implementation before acceptance scenarios.
- Scenario without requirement.
- Scenario without check.
- Scenario without evidence owner.
- BDD replaces tests.
- Gherkin is mandatory.
- User story template is complete requirements.
- Behavior changes without explicit gap.
