# Backend Release Rollback Notes

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

Rollback notes:

- Revert the synthetic service source and OpenAPI contract together.
- Keep contract consumers pinned until compatibility evidence exists.
- Do not promote this fixture beyond manual local testing.

Unsupported claims:

- No release, deployment, rollback drill or production change was performed.

