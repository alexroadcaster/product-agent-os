# Automation Candidate

Source status: `experiment`

Readiness: candidate_only

## Owner

- Accountable owner: Docs Maintainer

## Cadence

- Trigger: manual after docs changes
- Frequency: on demand

## Stable Inputs

- Inputs: changed Markdown files and source registry entries

## Stable Outputs

- Outputs: validation report only

## Verification

- Deterministic checks: python tools/check_docs.py
- Successful manual workflow runs: 2

## Failure Modes

- Known failure: missing Source status

## Rollback Or Disable Path

- Disable path: keep candidate packet and do not create a schedule

## Explicit Write Policy

- Allowed write targets: none during candidate validation

## Explicit Approval

- Approval status: ready for manual approval packet
