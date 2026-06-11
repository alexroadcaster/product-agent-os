# API Auth Authorization Matrix

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

| Endpoint | Access boundary | Evidence status |
| --- | --- | --- |
| `/health` | unauthenticated synthetic readiness path | `present_unverified` |
| `/tasks/{task_id}` | synthetic internal reader role | `present_unverified` |

Unsupported claims:

- This matrix is not an access-control test and does not prove authorization behavior.

