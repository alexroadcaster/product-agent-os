# Bug Rescue Workflow

Project: {project_name}
Profile: {profile_name}

## Inputs

- Symptom:
- Expected behavior:
- Actual behavior:
- Reproduction command:
- Manual reproduction:
- Failing evidence:
- Suspect boundary:
- Existing-capability scan:
- Smallest-fix leverage path:
- Files in scope:
- Files out of scope:
- Recent attempted fixes:
- Approval limits:

## Process

1. Restate the symptom, expected behavior and actual behavior.
2. Capture a reproduction command, manual reproduction steps, or the explicit evidence gap.
3. Inspect failing evidence without treating logs as verified truth until the command or manual repro is rerun.
4. Name the suspect boundary before editing files.
5. List hypotheses and eliminate at least one plausible cause before changing implementation.
6. Apply the coding-standard sub-gate: prefer a one-line existing API/helper/config fix, record rejected alternatives, and avoid broad rewrites before root cause evidence.
7. Add or select the smallest regression test or deterministic check for the failure.
8. Make the smallest fix inside files in scope.
9. Run the reproduction and regression check.
10. Record rollback notes and unresolved risks.

## Outputs

- Bug rescue report:
- Reproduction evidence:
- Root cause evidence:
- Existing-capability scan:
- Selected leverage path:
- Regression test:
- Changed files:
- Verification evidence:
- Rollback:
- Unresolved risks:

## Scenario Handoff

Keep the handoff concise enough for the next role to act without reading raw conversation history.

- Sources/context used:
- Assumptions:
- Files touched:
- Files proposed:
- Verification evidence:
- Open risks:
- Recommended next role:
- Stop reason:

## Verification

- Reproduction command or manual reproduction is present, or the workflow records a no-repro stop.
- Failing evidence is linked to a current command, log excerpt, screenshot, or manual repro.
- Suspect boundary is explicit before edits.
- Smallest-fix leverage path and rejected alternatives are recorded before implementation.
- Regression test or accepted verification gap is recorded before completion.
- Safety phrase: do not rewrite broad areas before root cause evidence exists.
- Safety phrase: stop at diagnosis when reproduction evidence is missing.

## Stop Conditions

- No reproduction command, manual reproduction, failing evidence, screenshot, or explicit user-confirmed symptom exists.
- File ownership or suspect boundary is unclear.
- The next fix would require broad rewrite before root cause evidence.
- The next fix adds custom logic or a dependency before existing APIs, helpers, framework behavior, config, or small adapter options are checked.
- Required external system, CI, production data, secret-bearing config, or write approval is unavailable.
- Verification cannot run and no accepted gap is recorded.
