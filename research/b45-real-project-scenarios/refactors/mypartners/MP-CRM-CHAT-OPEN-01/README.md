# MP-CRM-CHAT-OPEN-01 Refactor Arms

Source status: fixture-local source arms for `B45-PCA-M33`.

The arms use the copied `contacts_routes.py` fixture from `B45-PCA-M31` and the
`B45-PCA-M32` baseline. They do not touch the `myPartners` target workspace.

| Arm | Artifact | Intent | Current evidence |
| --- | --- | --- | --- |
| `original` | `original/src/server/app/api/contacts_routes.py` | Baseline reference copied from the fixture. | Comment advisory replay: 2 warnings. |
| `checklist-guided` | `checklist-guided/src/server/app/api/contacts_routes.py` | Extract self-contact relationship-state guardrails into a small helper before the route writes state. | AST syntax check passed; comment advisory replay: 1 warning; diff stat: +9/-4. |
| `advisory-guided` | `advisory-guided/src/server/app/api/contacts_routes.py` | Add intent docstrings to the two advisory symbols without changing route logic. | AST syntax check passed; comment advisory replay: 0 warnings; diff stat: +2/-0. |

The checklist-guided arm is a structural candidate only. It still needs real
fixture-local or disposable-runtime test evidence before any target apply. The
advisory-guided arm is the lowest-churn local treatment and is not runtime proof.
