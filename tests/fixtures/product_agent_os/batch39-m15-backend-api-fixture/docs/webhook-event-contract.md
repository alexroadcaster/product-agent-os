# Webhook Event Contract

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

Event contract:

- `asyncapi/asyncapi.yaml` models a synthetic `task.completed` event.
- Replay, idempotency, dead-letter handling, signature verification and stream delivery are planning concerns only.

Unsupported claims:

- No event was emitted, received, replayed or delivered to an external system.

