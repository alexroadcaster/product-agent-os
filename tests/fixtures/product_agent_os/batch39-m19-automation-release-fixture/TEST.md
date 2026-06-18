# Test Plan

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

## Deterministic Checks

- Run source-policy validation.
- Run Product-Agent OS runtime runner in contract mode.
- Run methodology audit.
- Run automation candidate validation through the smoke script.
- Compile Python scripts.

## Expected Result

The fixture passes local deterministic checks and records unsupported release,
deployment, publish, tag, external write and active automation claims as blocked
by approval boundaries.
