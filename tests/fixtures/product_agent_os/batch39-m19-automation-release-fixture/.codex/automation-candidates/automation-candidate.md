# Automation Candidate

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

Candidate status: candidate-only.

Accountable owner: Product-Agent OS maintainer.

Successful manual workflow runs: 1

## Cadence

Trigger: manual owner request only.

Frequency: none until a separate activation approval exists.

## Stable Inputs

Inputs: release packet, source-policy result, methodology audit result, runtime
guardrail result and command-results ledger.

## Stable Outputs

Outputs: local evidence summary and unsupported-claims ledger.

## Verification

Deterministic checks: source-policy, runtime contract, methodology audit,
automation candidate validation and fixture smoke check.

## Failure Modes

Known failure: missing owner approval, missing manual stability evidence,
missing rollback or disable path, active runtime marker, external write marker
or secret-like literal.

## Rollback Or Disable Path

Disable path: delete this candidate file and remove M19 evidence artifacts.

## Explicit Write Policy

Allowed write targets: local Batch 39 fixture and evidence artifacts only.

## Explicit Approval

Approval status: not approved for activation.

Accepted residual risks: none.
