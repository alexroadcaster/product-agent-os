# Product-Agent OS Handoff Contract

Use this reference when a skill hands work to the next lifecycle role or reports a stop condition.

Required fields:

- `lifecycle_state`
- `goal`
- `constraints`
- `allowed_sources`
- `inputs_used`
- `verified_claims`
- `unsupported_claims`
- `files_touched`
- `files_proposed`
- `commands_run`
- `verification_evidence`
- `risks`
- `next_agent_task`
- `stop_reason`

Rules:

- `goal`, `constraints`, and `verification_evidence` must not be empty when a skill claims readiness.
- At least one of `files_touched` or `files_proposed` must be non-empty.
- `unsupported_claims` must be explicit when sources or runtime checks are missing.
- `commands_run` records command strings, not invented outcomes.
- `verification_evidence` records observed results from the current run.
- `stop_reason` is required when the skill cannot advance the lifecycle.
- Reject handoffs that claim readiness without evidence, hide unsupported claims, omit stop conditions, or blur touched files with proposed files.
