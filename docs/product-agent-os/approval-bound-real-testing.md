# Approval-bound real testing

Source status: `official + experiment`

## Назначение

Эта страница описывает approval-bound real-testing execution matrix для Product-Agent OS. Matrix является planned, не implemented. Она не стартует local live server, не запускает browser automation, не выполняет provider/API calls, не мутирует canonical graph и не делает git stage/commit/push/PR без отдельного explicit owner approval для каждого действия.

Real testing начинается только после актуальной closure evidence по governance, runtime contract, audit/observability, target consent, QA/performance/stabilization и packaging/docs closure.

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

Planned artifacts:

- `live-server-run-evidence.json` для `approved_local_runtime_launch`;
- `browser-automation-smoke.json` и screenshots для `actual_browser_automation_smoke`;
- `provider-call-evidence.json`, `provider-eval-report.json` и cache metadata для `approved_provider_api_pilot`;
- `canonical-mutation-run.json`, `graph-mutation-journal.jsonl` и `rollback-proof.json` для `approved_canonical_mutation_pilot`;
- `git-release-pr-evidence.md` и PR packet для `explicit_git_release_pr_action`.

These artifacts become evidence только после separately approved action actually runs. Until затем they являются planned contract names, не implementation proof.

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

## Проверка

Для approval-bound real testing completion claim валиден только для exact approved action и только при наличии evidence текущего run.

Expected checks:

- local runtime pilot: health, local-only bind, auth rejection где applicable, нет писать endpoints, clean shutdown, graph-only fallback;
- browser smoke: console errors, network requests, mobile overflow, generated-view labels, source-boundary labels, screenshots;
- provider/API pilot: redaction pass, нет secrets/raw source/absolute paths, cache metadata, budget usage, eval threshold, fallback на failure, audit event;
- canonical mutation pilot: accepted ledger item, dry-run plan, previous/new digest, append-only journal, rollback proof;
- git action: текущий diff hygiene, explicit requested files, verification summary и нет unrelated staging.

Docs-only preparation не может claim these checks passed.

## Риски And Failure Modes

- Трактовка matrix как implemented because это exists.
- Reusing approval из один action к authorize another action.
- Starting local runtime до target/data policy и shutdown evidence являются explicit.
- Running browser automation который makes unapproved external requests.
- Performing provider calls без redaction, cache, budget, threshold и audit evidence.
- Accepting provider или LLM output как canonical fact без human review ledger.
- Applying canonical mutation без rollback proof.
- Running git stage/commit/push/PR как part из testing instead из как separately requested release action.

## Next Action

Этот next safe step является owner selection из один real-testing action и narrow approval packet для который action. Until который packet exists, real testing остается planned/not implemented и all live server, browser automation, provider/API, canonical mutation и git actions остаются blocked.
