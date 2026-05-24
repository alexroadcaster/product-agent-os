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
- Classify `usage_mode` before choosing methodology gates or assigning subagents.
- Distinguish completed packaged workflows from partial or pending gates; partial gates can name required artifacts but must record evidence gaps.
- Existing control-plane files: {existing_control_plane}
- Missing control-plane files at generation time: {missing_control_plane}
- Existing Codex assets: {existing_codex_assets}
- Initial risk note: {risk_text}

## Verification Policy

- Run the smallest relevant deterministic check after each meaningful change.
- Do not claim successful checks or working behavior unless the check ran in the current cycle.
- Record skipped or unavailable checks with reason, risk, and next action.
- Use runtime, visual, or manual checks when code inspection is not enough.
- Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.

## Engineering Standards Baseline

- Work from product hypothesis to architecture boundary to test-first specification to implementation to review to release measurement.
- Use data-informed product decisions: define success metrics, privacy constraints, and post-release measurement before broad implementation.
- Use a stack-appropriate architecture boundary before writing code: feature slices for UI, service or domain boundaries for backend, and explicit data ownership for storage.
- Prefer test-first or eval-first work for behavior changes. Use deterministic tests for stable behavior and evals for AI, UX, documentation, or subjective quality.
- Treat documentation as part of done: architecture decisions, API contracts, UI component states, database schema meaning, and release notes must change with behavior.
- Keep LLM-agent work bounded by owned files, stop conditions, approval needs, and command evidence.

## Usage Mode Rules

- Completed scenario workflows: bug rescue, greenfield idea, complex system acceleration, PR review, legacy onboarding, API migration, AI/RAG eval regression, native/mobile feature work, desktop local-first work, data migration, security-sensitive change, CI stabilization, and release packaging.
- For partial or pending gates, stage the next smallest artifact or gap record before implementation; do not claim completion or readiness until evidence exists.
- Use `present_unverified` for inferred entry points, commands, docs, contracts, runtime behavior, release status, or CI state until command evidence or owner evidence verifies the claim.
- Conditional readiness gates use `readiness_statuses`: `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`.
- Detection alone can only support `present_unverified`; a gate reaches `present_verified` only with required evidence, owner, applicability reason, and residual risk recorded.
- Record `applicable_missing` when the gate applies but evidence is absent, `not_applicable` only with a reason, and `explicit_gap_accepted` only with owner, reason, residual risk, and follow-up condition.
- Standards trigger policy (`standards_trigger_policy`) applies ADR trigger policy, C4/arc42, OpenAPI source of truth, AsyncAPI, SemVer impact, Keep a Changelog, CODEOWNERS status, GitHub Actions least privilege, `governance-proposal.md`, no external activation without approval, and no forced external activation only when project context makes them relevant.

## Agent Handoff

- Return sources or context used, assumptions, files touched or proposed, verification evidence, open risks, and recommended next role.
- Stop and coordinate before editing files owned by another worker.
- Keep handoffs concise enough for the next role to act without reading raw conversation history.
<!-- product-agent-os:end project-rules -->
