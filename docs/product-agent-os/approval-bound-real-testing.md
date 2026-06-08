# Approval-bound real testing

Source status: `official + experiment`

## Назначение

Эта страница описывает approval-bound real-testing execution matrix для Product-Agent OS. Matrix не является bundled approval: каждое live/runtime/browser/provider/canonical/git действие остается отдельно scoped, отдельно approved и отдельно evidenced.

Real testing начинается только после актуальной closure evidence по governance, runtime contract, audit/observability, target consent, QA/performance/stabilization и packaging/docs closure.

Текущий source-backed статус: M37-M41 имеют execution evidence или owner closure: M37-M40 пройдены для approved local runtime, browser smoke, Codex-session provider pilot и staged canonical mutation pilot. M41 закрыт как `owner_closed_no_op_git_release_pr`, и git stage/commit/push/PR не выполнялись.

## Approvals And Source-Of-Truth Boundary

Каждый real-testing action имеет отдельный approval packet. Approval для live server pilot не разрешает browser automation. Approval для browser automation не разрешает provider/API calls. Approval для provider/API pilot не разрешает canonical mutation. Approval для canonical mutation не разрешает git release/PR action.

source of truth:

- checked-in source docs и control-plane artifacts;
- owner approval packet для exact action;
- generated evidence files только как staged evidence;
- audit/security/observability packets который cite source evidence.

Не являются source of truth:

- generated HTML/dashboard/cockpit views;
- provider output без human review;
- LLM proposals без accepted ledger item;
- screenshots или smoke output без source-boundary context;
- memory, chat recall или unstaged local cache.

## Входы

Before any real-testing action, collect:

- текущий governance и runtime evidence summary;
- owner-approved target workspace class и data policy;
- allowed commands и explicitly blocked commands;
- data classification и redaction policy;
- credential boundary и provider budget когда providers являются involved;
- rollback path и cleanup/deletion proof;
- audit event schema и evidence destination;
- accepted gaps с owner, reason, review date, residual risk и follow-up condition.

Входные данные должны быть sanitized. Не помещайте secrets, tokens, credentials, private keys, raw source bodies, private customer data или unredacted PII в approval packets, prompts, logs, screenshots, fixtures или generated evidence.

## Выходы и артефакты

Action artifacts and current evidence:

| Action | Evidence artifact | Current status |
| --- | --- | --- |
| `approved_local_runtime_launch` | `live-server-run-evidence.json` | M37 пройдено; короткий локальный server bound to `127.0.0.1`, проверки `health/query/auth/public-bind/write-block`, `server_shutdown_complete: true` и `redaction.ok: true`. |
| `actual_browser_automation_smoke` | `browser-automation-smoke.json`, `desktop.png`, `mobile.png` | M38 пройдено; Playwright Chromium, `console_errors: 0`, `network_failures: 0`, `mobile_overflow: false`, generated-view labels, source-boundary labels и clean shutdown. |
| `approved_provider_api_pilot` | `provider-call-evidence.json`, `provider-eval-report.json` | M39 пройдено; provider surface `codex_user_session`, `OPENAI_API_KEY used: false`, direct API call из workspace shell: false и `provider_secret_stored: false`. |
| `approved_canonical_mutation_pilot` | `canonical-mutation-run.json`, `graph-mutation-journal.jsonl`, `rollback-proof.json` | M40 пройдено как `stage_root_only`; `canonical_graph_source_mutated: false`, `operation_count: 1`, `journal_entry_count: 1` и `rollback_restores_previous_graph_digest: true`. |
| `explicit_git_release_pr_action` | `git-release-pr-evidence.md`, PR packet | M41 закрыт owner decision как `owner_closed_no_op_git_release_pr`; git stage/commit/push/PR не выполнялись. |

Эти artifacts являются evidence только для exact approved action, который действительно был выполнен. Они не approve any other action, а generated evidence остается staged/source-boundary evidence пока checked-in source docs или owner-reviewed packets не cite it.

## Workflow

1. Freeze текущий closure state и confirm нет hidden unresolved live-runtime gates.
2. Выберите exactly один real-testing action к request approval for.
3. Создайте approval packet с owner, target, allowed commands, data policy, source boundary, rollback, budget, audit destination и stop conditions.
4. Если approval является missing или incomplete, stop at `approval_required`.
5. Если approved, запуск только named action и collect только его evidence.
6. Validate cleanup, fallback и audit records.
7. Record result как passed, blocked, disabled, rollback-complete или owner-accepted gap.
8. Reassess до requesting approval для следующий action.

## Action Matrix

| Action | Planned purpose | Separate approval должен name | Hard boundary |
| --- | --- | --- | --- |
| `approved_local_runtime_launch` | Запустить disabled-by-default local read-only runtime на approved target. | target, bind/auth/port policy, PID/log path, health check, shutdown evidence, fallback. | Нет launch без owner approval; local-only; нет писать endpoints; нет provider calls. |
| `actual_browser_automation_smoke` | Replace staged browser QA assumptions с real browser evidence. | runtime URL, browser tool, viewports, allowed network, screenshots, console/network capture. | Нет browser automation без approval; нет unapproved external requests; labels и нет mobile overflow должен быть checked. |
| `approved_provider_api_pilot` | Measure approved embedding/reranker/LLM provider behavior в рамках real gates. | provider, model, credential env var, redaction, cache, budget, eval threshold, audit path. | `external_call_performed` may become true только inside эта packet; нет secrets/raw source/absolute paths. |
| `approved_canonical_mutation_pilot` | Применить и rollback owner-accepted graph change. | accepted ledger item, dry-run plan, conflict checks, journal path, digest comparison, rollback proof. | Нет mutation без accepted item и dry-run; `accepted_gap` остается non-mutating. |
| `explicit_git_release_pr_action` | Publish только verified owner-approved change set. | exact files, verification summary, unrelated-change check, commit/push/PR intent. | Нет `git add`, `git commit`, `git push` или PR без explicit пользователь command. |

## Current Execution Status

| Step | Action | Status | Evidence boundary |
| --- | --- | --- | --- |
| M37 | `approved_local_runtime_launch` | `passed` | Local-only runtime evidence; no browser automation, provider/API call, canonical graph mutation или git action из этого approval. |
| M38 | `actual_browser_automation_smoke` | `passed` | Только browser evidence; provider/API call, canonical graph mutation и git action не разрешались этим approval. |
| M39 | `approved_provider_api_pilot` | `passed` | Только Codex-session provider pilot evidence; canonical graph mutation и git action не разрешались этим approval. |
| M40 | `approved_canonical_mutation_pilot` | `passed` | Только staged canonical mutation/rollback proof; `canonical_graph_source_mutated: false`, git action не выполнялся. |
| M41 | `explicit_git_release_pr_action` | `owner_closed_no_op_git_release_pr` | Git release/PR не выполнялся; future git write требует fresh preflight, release branch или push target, commit message, PR base branch, PR title/intent и explicit branch/write policy. |

## Проверка

Для approval-bound real testing completion claim валиден только для exact approved action и только при наличии evidence текущего run.

Expected checks:

- local runtime pilot: health, local-only bind, auth rejection где applicable, нет писать endpoints, clean shutdown, graph-only fallback;
- browser smoke: console errors, network requests, mobile overflow, generated-view labels, source-boundary labels, screenshots;
- provider/API pilot: redaction pass, нет secrets/raw source/absolute paths, cache metadata, budget usage, eval threshold, fallback на failure, audit event;
- canonical mutation pilot: accepted ledger item, dry-run plan, previous/new digest, append-only journal, rollback proof;
- git action: текущий diff hygiene, explicit requested files, verification summary и нет unrelated staging.

A docs-only update не может create new passed evidence. Он может только cite current-run evidence из source packet и должен keep new live/browser/provider/canonical/git actions approval-bound.

## Риски And Failure Modes

- Трактовка all real testing как complete because M37-M40 passed; M41 и any new live/browser/provider/canonical/git action остаются separate approvals.
- Трактовка matrix как implemented because это exists.
- Reusing approval из один action к authorize another action.
- Starting local runtime до target/data policy и shutdown evidence являются explicit.
- Running browser automation который makes unapproved external requests.
- Performing provider calls без redaction, cache, budget, threshold и audit evidence.
- Accepting provider или LLM output как canonical fact без human review ledger.
- Applying canonical mutation без rollback proof.
- Running git stage/commit/push/PR как part из testing instead из как separately requested release action.

## Next Action

Следующий safe step: documentation/source closure для текущей real-testing evidence или owner-provided M41 git release fields. Until эти fields supplied, git release/PR остается blocked. Any new live server, browser automation, provider/API, canonical mutation или git action все еще требует own narrow approval packet.
