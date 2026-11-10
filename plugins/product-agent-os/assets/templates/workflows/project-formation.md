# Product-Agent OS Project Formation

Source status: `codex-plugin-template`

Project: {project_name}
Profile: {profile_name}

## Purpose

Use this workflow on first use of Product-Agent OS in a real project. It keeps project formation staged-first and prevents agent, config, rules, hooks, or template generation from outrunning workspace evidence.

## Formation Order

Use the single `render_infrastructure.py` route: `--analyze`, then `--dry-run --formation-context request.json`, then authorized `--stage` with the exact `--preview-digest`. The request combines task context, applicable domains, canonical paths, supplied facts and explicit control-surface proposals. `formation.gaps` blocks staging; `implementation_gaps` remains open after an honest scaffold. Unknown facts and ambiguous owners never trigger the full catalog.

Review `selection_reasons`, `owners`, `manual_updates` and `runtime_dependencies`. Existing files remain companion proposals. `--previous-plan` reports review-only removal candidates, never deletion. `--merge-stage` uses the existing approval/rollback engine, including source-digest and file-authority checks. Absent input produces a clarification gap; only explicit `--legacy-catalog` selects all legacy templates. Existing `--task`/`--task-context` retains the scoped compatibility route. SessionStart runtime output and fresh-session activation stay separate.

1. Read-only project audit
   - Inspect active instructions, nearest `AGENTS.md`, control-plane files, source/docs structure, stack/runtime signals, tests/evals, security/privacy/release surfaces, dirty state, sandbox and approval boundaries.
   - Run only approved local discovery/audit commands.
   - Do not mutate target files, launch live servers, run browser automation, call providers, activate hooks, create automations, perform git actions, or write external systems.

2. Recommendation packet
   - Keep detailed task matrices under `docs/planning/` intact even above the default 40 000-byte budget. Keep entrypoints compact; do not classify active matrix detail as archived merely to bypass a limit. Explicit per-file limits still apply.
   - Reuse the existing docs index and canonical names. Recommend architecture/components, ADR, API/data contracts, operations/runbooks, evidence and archive navigation only when the domain applies; name each source owner and update trigger.
   - For scoped staging, supply confirmed document facts and provenance through task-context `documents`; leave unknown facts missing. EVALS is conditional on AI/subjective quality gates (`evals_required`), not ordinary formatting work. Dependency closure must not imply activation of config, agents or hooks.
   - Distinguish scaffold, draft, reviewed, accepted and stale. Headings and file presence do not establish readiness; owner decisions and review receipts bind the current source digest.
   - Produce a project-specific recommendation list for agents, skills, artifact templates, documentation, methodology domains, verification gates, approval boundaries, and missing owner questions.
   - Every recommendation must name source evidence, template source, owner, risk, next action, and status: `present_unverified`, `proposal_staged`, `approval_required`, or `explicit_gap_accepted`.

3. Project templates and docs
   - Stage only the templates and documentation skeletons that match the project risk profile.
   - Preserve existing user-authored `AGENTS.md`, `.codex/config.toml`, `.rules`, hooks, workflows, automation candidates, and project docs.
   - Existing unmarked files are user content; stage companion proposals instead of overwriting them.

4. Control surface synthesis
   - Synthesize `agents`, `.codex/config.toml`, and `.rules` as one coordinated Codex control surface.
   - Use safe patterns from owner-provided working examples only as pattern evidence; do not copy private paths, personal preferences, secrets, raw chat, machine-specific values, or broad permissions.
   - Keep `.codex/config.toml`, `.codex/hooks`, `.codex/automations`, `.codex/plugins`, external writes, destructive commands, provider calls, browser automation, live servers, target apply, canonical graph mutation, and git actions approval-bound.

5. Agent assembly
   - Build `.codex/agents/*.toml` only after audit and recommendation packet exist.
   - Use official custom-agent fields at top level: `name`, `description`, optional model/sandbox/tool fields, and `developer_instructions`.
   - Put Product-Agent OS ownership, inputs, outputs, tools, docs, skills, methodologies, stop conditions, model policy, sandbox/MCP boundaries, and handoff requirements inside `developer_instructions`.

6. Handoff and retest
   - Produce a fresh-context handoff for the next role.
   - Record retest requirements in the project-specific production evidence ledger when one is active.
   - Do not claim ready, done, fixed, works, release-ready, or safe to hand off without current command evidence, owner evidence, or an owner-reviewed accepted gap.

## Outputs

- Formation recommendation packet:
- Project audit evidence refs:
- Template/doc proposals:
- Control surface proposal:
- Agent assembly proposal:
- Approval boundaries:
- Owner questions:
- Retest requirements:

## Verification

- Audit ran before agent/template/control-surface generation.
- Recommendations cite source evidence and owner.
- Generated agent TOML uses official top-level custom-agent fields.
- Product-Agent OS role metadata is inside `developer_instructions`.
- Generated config keeps sensitive `.codex` paths closed unless scoped write access is required and documented.
- `.rules` proposals keep destructive, external, provider, browser, live-server, target-apply, canonical-mutation, automation, and git actions approval-bound.
- No secrets, private paths, raw private chat, customer data, or machine-specific values are copied from examples.
- Staged artifacts are proposals until exact owner approval applies them.

## Stop Conditions

- Project audit cannot run or source evidence is stale.
- Owner-provided examples are unavailable, private, or unsafe to reuse as pattern evidence.
- Required write, browser, provider, live-server, target apply, canonical mutation, automation, or git approval is missing.
- Recommended control surface would weaken sandbox, approvals, rules, hooks, or source policy.
- Agent roles have overlapping ownership without a fresh-context handoff and sequential fallback.
