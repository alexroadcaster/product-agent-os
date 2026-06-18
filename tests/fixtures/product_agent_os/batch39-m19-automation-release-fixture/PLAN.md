# Plan

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

## Slice

`B39-TEST-M19-A01` stages a local automation/release fixture and validates that
release and automation signals are recognized while approval-bound actions are
blocked.

## Owned Files

- Fixture files under `tests/fixtures/product_agent_os/batch39-m19-automation-release-fixture`.
- Evidence files under `docs/superpowers/specs/batch39-m19-*`.

## Forbidden Files And Surfaces

- No target project files.
- No real root `.github/workflows` changes.
- No git, GitHub, deploy, publish, tag, release creation or active automation.

## Rollback

Delete the M19 fixture directory and M19 evidence artifacts.
