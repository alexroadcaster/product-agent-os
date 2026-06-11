# Backend Dependency Failure Matrix

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

| Dependency | Failure mode | Expected handling | Evidence status |
| --- | --- | --- | --- |
| Task store | unavailable | return stable error payload | `present_unverified` |
| Queue worker | delayed | keep read endpoint stable | `present_unverified` |
| Metrics sink | unavailable | keep service path independent | `present_unverified` |

Unsupported claims:

- This matrix is not a failure drill and does not prove recovery behavior.

