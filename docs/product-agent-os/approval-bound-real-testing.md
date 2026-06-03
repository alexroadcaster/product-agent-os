# Approval-bound real testing

Source status: `official + experiment`

## Назначение

Эта страница описывает approval-bound real-testing execution matrix для Product-Agent OS. Matrix является planned, not implemented. Она не стартует local live server, не запускает browser automation, не выполняет provider/API calls, не мутирует canonical graph и не делает git stage/commit/push/PR без отдельного explicit owner approval для каждого действия.

Real testing начинается только после актуальной closure evidence по governance, runtime contract, audit/observability, target consent, QA/performance/stabilization и packaging/docs closure.

## Approvals And Source-Of-Truth Boundary

Каждый real-testing action имеет отдельный approval packet. Approval для live server pilot не разрешает browser automation. Approval для browser automation не разрешает provider/API calls. Approval для provider/API pilot не разрешает canonical mutation. Approval для canonical mutation не разрешает git release/PR action.

Source of truth:

- checked-in source docs and control-plane artifacts;
- owner approval packet for the exact action;
- generated evidence files only as staged evidence;
- audit/security/observability packets that cite source evidence.

Не являются source of truth:

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

Planned artifacts:

- `live-server-run-evidence.json` for `approved_local_runtime_launch`;
- `browser-automation-smoke.json` and screenshots for `actual_browser_automation_smoke`;
- `provider-call-evidence.json`, `provider-eval-report.json` and cache metadata for `approved_provider_api_pilot`;
- `canonical-mutation-run.json`, `graph-mutation-journal.jsonl` and `rollback-proof.json` for `approved_canonical_mutation_pilot`;
- `git-release-pr-evidence.md` and PR packet for `explicit_git_release_pr_action`.

These artifacts become evidence only after the separately approved action actually runs. Until then they are planned contract names, not implementation proof.

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

## Verification

For approval-bound real testing, a completion claim is valid only for the exact approved action and only after current-run evidence exists.

Expected checks:

- local runtime pilot: health, local-only bind, auth rejection where applicable, no write endpoints, clean shutdown, graph-only fallback;
- browser smoke: console errors, network requests, mobile overflow, generated-view labels, source-boundary labels, screenshots;
- provider/API pilot: redaction pass, no secrets/raw source/absolute paths, cache metadata, budget usage, eval threshold, fallback on failure, audit event;
- canonical mutation pilot: accepted ledger item, dry-run plan, previous/new digest, append-only journal, rollback proof;
- git action: current diff hygiene, explicit requested files, verification summary and no unrelated staging.

Docs-only preparation cannot claim these checks passed.

## Risks And Failure Modes

- Treating the matrix as implemented because it exists.
- Reusing approval from one action to authorize another action.
- Starting a local runtime before target/data policy and shutdown evidence are explicit.
- Running browser automation that makes unapproved external requests.
- Performing provider calls without redaction, cache, budget, threshold and audit evidence.
- Accepting provider or LLM output as canonical fact without human review ledger.
- Applying canonical mutation without rollback proof.
- Running git stage/commit/push/PR as part of testing instead of as a separately requested release action.

## Next Action

The next safe step is owner selection of one real-testing action and a narrow approval packet for that action. Until that packet exists, real testing remains planned/not implemented and all live server, browser automation, provider/API, canonical mutation and git actions remain blocked.
