# AGENTS.md

<!-- product-agent-os:start project-rules -->
Project: {project_name}
Workspace: {workspace_path}
Profile: {profile_name}
Detected stack: {detected_stack_text}
Generated at: {generated_at}

## Durable Rules

- Keep durable project rules in this file and keep temporary decisions in `RUNLOG.md`.
- Use official documentation as source of truth for platform behavior.
- Do not store credentials, customer data, or private keys in prompts, templates, fixtures, memory, or examples.
- Prefer manual thread -> playbook -> skill -> plugin -> automation candidate.
- Existing control-plane files: {existing_control_plane}
- Missing control-plane files at generation time: {missing_control_plane}
- Existing Codex assets: {existing_codex_assets}
- Initial risk note: {risk_text}

## Verification Policy

- Run the smallest relevant deterministic check after each meaningful change.
- Do not claim successful checks or working behavior unless the check ran in the current cycle.
- Record skipped or unavailable checks with reason, risk, and next action.
- Use runtime, visual, or manual checks when code inspection is not enough.

## Agent Handoff

- Return sources or context used, assumptions, files touched or proposed, verification evidence, open risks, and recommended next role.
- Stop and coordinate before editing files owned by another worker.
- Keep handoffs concise enough for the next role to act without reading raw conversation history.
<!-- product-agent-os:end project-rules -->
