# Backend Health Check Contract

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

Health semantics:

- `200` means the synthetic service boundary is ready.
- `503` means the synthetic service boundary is unavailable.
- The response body avoids sensitive fields.

Unsupported claims:

- The health route is not exercised by a live runtime check.

