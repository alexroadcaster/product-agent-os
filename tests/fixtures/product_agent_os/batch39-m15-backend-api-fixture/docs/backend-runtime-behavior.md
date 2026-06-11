# Backend Runtime Behavior

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

Expected synthetic behavior:

- `/health` returns a readiness-oriented payload shape.
- `/tasks/{task_id}` returns a task payload or an error payload.
- Dependency failure behavior is represented as planning evidence only.

Unsupported claims:

- No live process was started.
- No request/response runtime trace exists.
- No load, concurrency or failure-mode drill exists.

