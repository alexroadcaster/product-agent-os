# Acceptance Scenarios

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
- Business rule:
- User or actor:
- Given:
- When:
- Then:
- Equivalent behavior format:
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

## Stop Conditions

- Implementation before acceptance scenarios.
- Scenario without requirement.
- Scenario without check.
- Scenario without evidence owner.
- BDD replaces tests.
- Behavior changes without explicit gap.
