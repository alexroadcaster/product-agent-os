# Approval-bound real testing

Source status: `official + experiment`

## Purpose

This page describes the approval-bound real-testing execution matrix for Product-Agent OS. The matrix is not a bundled approval: each live/runtime/browser/provider/canonical/git action remains separately scoped, separately approved and separately evidenced.

Real testing starts only after current closure evidence exists for governance, runtime contract, audit/observability, target consent, QA/performance/stabilization and packaging/docs closure.

Current source-backed status: M37-M41 have execution evidence or owner closure: M37-M40 passed for approved local runtime, browser smoke, Codex-session provider pilot and staged canonical mutation pilot. M41 is closed as `owner_closed_no_op_git_release_pr`, and no git stage/commit/push/PR has been performed.

## Approvals And Source-Of-Truth Boundary

Each real-testing action has a separate approval packet. Approval for a live server pilot does not allow browser automation. Approval for browser automation does not allow provider/API calls. Approval for a provider/API pilot does not allow canonical mutation. Approval for canonical mutation does not allow git release/PR action.

Source of truth:

- checked-in source docs and control-plane artifacts;
- owner approval packet for the exact action;
- generated evidence files only as staged evidence;
- audit/security/observability packets that cite source evidence.

Not source of truth:

- generated HTML/dashboard/cockpit views;
- provider output without human review;
- LLM proposals without accepted ledger item;
- screenshots or smoke output without source-boundary context;
- memory, chat recall or unstaged local cache.

## Inputs

Before any real-testing action, collect:

- current governance and runtime evidence summary;
- owner-approved target workspace class and data policy;
- allowed commands and explicitly blocked commands;
- data classification and redaction policy;
- credential boundary and provider budget when providers are involved;
- rollback path and cleanup/deletion proof;
- audit event schema and evidence destination;
- accepted gaps with owner, reason, review date, residual risk and follow-up condition.

Inputs must be sanitized. Do not place secrets, tokens, credentials, private keys, raw source bodies, private customer data or unredacted PII into approval packets, prompts, logs, screenshots, fixtures or generated evidence.

## Outputs And Artifacts

Action artifacts and current evidence:

| Action | Evidence artifact | Current status |
| --- | --- | --- |
| `approved_local_runtime_launch` | `live-server-run-evidence.json` | Passed in M37; short-lived local server bound to `127.0.0.1`, health/query/auth/public-bind/write-block checks, `server_shutdown_complete: true` and `redaction.ok: true`. |
| `actual_browser_automation_smoke` | `browser-automation-smoke.json`, `desktop.png`, `mobile.png` | Passed in M38; Playwright Chromium, `console_errors: 0`, `network_failures: 0`, `mobile_overflow: false`, generated-view labels, source-boundary labels and clean shutdown. |
| `approved_provider_api_pilot` | `provider-call-evidence.json`, `provider-eval-report.json` | Passed in M39; provider surface `codex_user_session`, `OPENAI_API_KEY used: false`, direct API call from workspace shell: false and `provider_secret_stored: false`. |
| `approved_canonical_mutation_pilot` | `canonical-mutation-run.json`, `graph-mutation-journal.jsonl`, `rollback-proof.json` | Passed in M40 as `stage_root_only`; `canonical_graph_source_mutated: false`, `operation_count: 1`, `journal_entry_count: 1` and `rollback_restores_previous_graph_digest: true`. |
| `explicit_git_release_pr_action` | `git-release-pr-evidence.md`, PR packet | Closed in M41 by owner decision as `owner_closed_no_op_git_release_pr`; no git stage/commit/push/PR. |

These artifacts are evidence only for the exact approved action that actually ran. They do not approve any other action, and generated evidence remains staged/source-boundary evidence until checked-in source docs or owner-reviewed packets cite it.

## Workflow

1. Freeze current closure state and confirm no hidden unresolved live-runtime gates.
2. Select exactly one real-testing action to request approval for.
3. Write an approval packet with owner, target, allowed commands, data policy, source boundary, rollback, budget, audit destination and stop conditions.
4. If approval is missing or incomplete, stop at `approval_required`.
5. If approved, run only the named action and collect only its evidence.
6. Validate cleanup, fallback and audit records.
7. Record result as passed, blocked, disabled, rollback-complete or owner-accepted gap.
8. Reassess before requesting approval for the next action.

## Action Matrix

| Action | Planned purpose | Separate approval must name | Hard boundary |
| --- | --- | --- | --- |
| `approved_local_runtime_launch` | Start the disabled-by-default local read-only runtime on an approved target. | target, bind/auth/port policy, PID/log path, health check, shutdown evidence, fallback. | No launch without owner approval; local-only; no write endpoints; no provider calls. |
| `actual_browser_automation_smoke` | Replace staged browser QA assumptions with real browser evidence. | runtime URL, browser tool, viewports, allowed network, screenshots, console/network capture. | No browser automation without approval; no unapproved external requests; labels and no mobile overflow must be checked. |
| `approved_provider_api_pilot` | Measure approved embedding/reranker/LLM provider behavior under real gates. | provider, model, credential env var, redaction, cache, budget, eval threshold, audit path. | `external_call_performed` may become true only inside this packet; no secrets/raw source/absolute paths. |
| `approved_canonical_mutation_pilot` | Apply and rollback an owner-accepted graph change. | accepted ledger item, dry-run plan, conflict checks, journal path, digest comparison, rollback proof. | No mutation without accepted item and dry-run; `accepted_gap` remains non-mutating. |
| `explicit_git_release_pr_action` | Publish only the verified owner-approved change set. | exact files, verification summary, unrelated-change check, commit/push/PR intent. | No `git add`, `git commit`, `git push` or PR without explicit user command. |

## Current Execution Status

| Step | Action | Status | Evidence boundary |
| --- | --- | --- | --- |
| M37 | `approved_local_runtime_launch` | `passed` | Local-only runtime evidence; no browser automation, provider/API call, canonical graph mutation or git action from this approval. |
| M38 | `actual_browser_automation_smoke` | `passed` | Browser evidence only; no provider/API call, canonical graph mutation or git action from this approval. |
| M39 | `approved_provider_api_pilot` | `passed` | Codex-session provider pilot evidence only; no canonical graph mutation or git action from this approval. |
| M40 | `approved_canonical_mutation_pilot` | `passed` | Staged canonical mutation/rollback proof only; `canonical_graph_source_mutated: false` and no git action. |
| M41 | `explicit_git_release_pr_action` | `owner_closed_no_op_git_release_pr` | Git release/PR did not run; future git write requires fresh preflight, release branch or push target, commit message, PR base branch, PR title/intent and explicit branch/write policy. |

## Verification

For approval-bound real testing, a completion claim is valid only for the exact approved action and only after current-run evidence exists.

Expected checks:

- local runtime pilot: health, local-only bind, auth rejection where applicable, no write endpoints, clean shutdown, graph-only fallback;
- browser smoke: console errors, network requests, mobile overflow, generated-view labels, source-boundary labels, screenshots;
- provider/API pilot: redaction pass, no secrets/raw source/absolute paths, cache metadata, budget usage, eval threshold, fallback on failure, audit event;
- canonical mutation pilot: accepted ledger item, dry-run plan, previous/new digest, append-only journal, rollback proof;
- git action: current diff hygiene, explicit requested files, verification summary and no unrelated staging.

A docs-only update cannot create new passed evidence. It can only cite current-run evidence from the source packet and must keep new live/browser/provider/canonical/git actions approval-bound.

## Risks And Failure Modes

- Treating all real testing as complete because M37-M40 passed; M41 and any new live/browser/provider/canonical/git action remain separate approvals.
- Treating the matrix as implemented because it exists.
- Reusing approval from one action to authorize another action.
- Starting a local runtime before target/data policy and shutdown evidence are explicit.
- Running browser automation that makes unapproved external requests.
- Performing provider calls without redaction, cache, budget, threshold and audit evidence.
- Accepting provider or LLM output as canonical fact without human review ledger.
- Applying canonical mutation without rollback proof.
- Running git stage/commit/push/PR as part of testing instead of as a separately requested release action.

## Next Action

The next safe step is either documentation/source closure for the current real-testing evidence, or owner-provided M41 git release fields. Until those fields are supplied, git release/PR stays blocked. Any new live server, browser automation, provider/API, canonical mutation or git action still needs its own narrow approval packet.

## Current route and evidence

Evidence distinguishes a trusted definition, an authorized tool and observed execution/denial. An MCP-hook error is not fail-closed. Use the [hook guide](../runtime/worktrees-hooks-rules.md) for the local receipt and remaining limits.
