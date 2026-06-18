# B39 M19 Automation Release Fixture

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

This fixture is a local-only Product-Agent OS Batch 39 automation and release
contract pilot. It contains release, operations and automation-candidate
signals without creating a release, deployment, schedule, hook, GitHub Action
activation, external write, tag, branch push or publication.

## Boundaries

- Target workspace mutation: not allowed.
- Git, GitHub, tag, release creation, publish and deploy actions: not allowed.
- Active automation, recurring automation, hook activation and external workflow
  creation: not allowed.
- Provider, API, model, browser and live server actions: not allowed.
- Local evidence artifact writes inside the codex_docs workspace are allowed.

## Expected Use

Use this fixture to verify that automation/release evidence remains
candidate-only until owner approval, current release evidence, rollback or
disable evidence and activation boundaries exist.
