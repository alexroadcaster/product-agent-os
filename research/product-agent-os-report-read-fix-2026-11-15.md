# Исправление MD-отчётов и обычного чтения — 15.11.2026

Source status: project source, current-run synthetic checks and current-host probe; fresh-session activation not yet verified.

## Проверка текущего host

Обычный report_authoring scope этого чата; точный report_output_path; hook command без report flags. Один Add File и два Update File через literal `functions.exec` → `tools.apply_patch` успешно выполнены. Содержимое затем прочитано: второе обновление присутствует. Инструмент возвращает `{}` без process exit code: success подтверждён чтением файла, не выдуманным exit 0.

Negative: Add File соседнего `research/paos-report-negative-probe-2026-11-15.md` отклонён действующим PreToolUse: `patch destination is outside the requested report scope`. Файл отсутствует в status; отсутствие дополнительно проверяется final validation. Marker и код другого чата не менялись.

Чтение при report_authoring marker: `rg -n report_authoring .codex/hooks --glob '*.py' | rg work_type`; `Get-ChildItem -Path .codex/hooks/pre_tool* -Name`; `Get-Content .codex\config.toml | Select-String -SimpleMatch lifecycle_contract` — exit 0 с ожидаемым выводом. Предыдущая команда `rg ... .codex/hooks/*.py` прошла hook, но сам Windows rg вернул os error 123: native rg не раскрывает такой glob; исправленная команда использует `--glob`. Это различие shell/runtime и guard, не успешная проверка поиска.

При возврате report → fix patch без `task_start_brief_shown` был отклонён bootstrap guard. Повторный patch с существующей строкой `task_start_brief_shown: true` в контексте прошёл. Это остающийся синтаксический контракт marker bootstrap, не запрос нового согласия владельца.

## Scope и критерии

Task: `PAOS-REPORT-READ-FIX-2026-11-15` — исправление явно запрошенных Markdown-отчётов и обычного чтения. Пользователь разрешил scoped исправление guard; остальные ограничения только проанализированы. Политика по-прежнему не делает запрос на анализ без артефакта разрешением произвольно менять файлы.

Acceptance: create → update → update одного exact MD без per-report hook arguments; распознанное чтение без marker; обычные reads в legacy pinned modes; deny neighboring/protected/foreign/stale/terminal/alias/mixed/delete/move/shell-executor cases. Host sandbox и approval enforcement сохраняются. Маркер — объявление scope, не независимая authority. Ordinary patches используют контекст инструмента; атомарный CAS и защита от всех concurrent writers не заявляются.

Plan exception: ограниченный repair существующего маршрута; sequencing и rollback записаны в PLAN.md, отдельная task matrix не нужна. Новая зависимость не устанавливалась; hook definitions, trust, global config, Git history, providers и реальные target workspaces не менялись.

## Компактный code-change contract

- existing_capability: переиспользованы `_literal_call`, `_report_path`, `_lifecycle_marker_ok`, session selector и существующий unittest harness.
- smallest_safe_patch: default report branch, shared read classifier, active/package parity; legacy grants сохранены.
- invariants: exact path/session, freshness/terminal, protected instructions, sandbox, no shell/external widening, no foreign marker writes.
- dependency_decision: no_new_dependency; Python standard library и существующие helpers.
- risk_selected_tests: subprocess hook wire для positive/negative; read matrix для default/v1/v2; hardlink stat boundary и symlink rejection; current-host actual patch sequence.
- comment_decision: comment_needed для scope-vs-authority, pipeline consumers, POSIX glob option injection и link-count test seam.
- performance_applicability: read fast path сохраняется; распознавание pipeline ограничено 8 сегментами и существующим лимитом длины; benchmark не требуется для этого исправления.
- evidence_and_gaps: proceed; текущий Windows host, Python313 в прогонах; fresh-session activation отдельно не доказана, инструкции других уже открытых чатов могут быть устаревшими.

## RED, GREEN и неуспешные попытки

1. До исправления: `python -B -m unittest tests.product_agent_os.test_lifecycle_hooks.LifecycleHooksTest.test_requested_report_default_route_creates_and_updates_only_owned_markdown tests.product_agent_os.test_lifecycle_hooks.LifecycleHooksTest.test_ordinary_reads_without_marker_and_in_pinned_modes -q` — exit 1, 2 tests, 25 failing assertions/subtests: requested create и ordinary reads отклонены. Это intended RED.
2. Первая реализация: `python -B -m unittest tests.product_agent_os.test_lifecycle_hooks -q` — exit 0, 44 tests, 16.656 s, до дополнительных boundary tests.
3. Read-only independent review `/root/rules_review` выявил P1 instruction-template destination и POSIX leading-glob option injection. Исправлено: implementation/instruction directories исключены из ordinary reports; leading unquoted globs запрещены, directory-prefixed/quoted glob поддержаны. Добавлены negative cases; final self-review проверяет эти конкретные изменения.
4. Дополнительный hardlink fixture через `os.link` — WinError 5 как в sandbox TEMP, так и workspace TEMP. Это setup limitation, не behavior RED. Заменён stat boundary test; реальный hardlink не создан. В одном прогоне workspace TEMP был также WinError 32 при cleanup существующего comment-advisory fixture; сохранён как transient setup failure.
5. Запись workflow через shell Python — exit 1, PermissionError для `.codex/workflows/task-plan-lifecycle.md`; использован разрешённый инструмент `apply_patch`. ACL и sandbox не менялись.
6. После исправлений: `python -B -m unittest tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_infrastructure_templates -q` — exit 0, 148 tests, 20.567 s. TEMP/TMP: workspace `.codex-tmp/report-read-fix`.
7. Docs gate `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q` — exit 1, 105 tests, 4 failures из-за отсутствующих `web/accessibility.html`/`web/pilot.html` в старом canonical `site/`. Повтор с предусмотренным TEST.md `PAOS_DOCS_SITE_DIR=.tmp/paos-m4-0030/site-final` — exit 0, 105 tests, 10.476 s. Использован существующий output из PAOS-0030, не новая сборка и не доказательство свежести изменённых страниц; source docs проверены отдельно.
8. `python -B plugins/product-agent-os/scripts/run_transcript_eval.py` — exit 0, 26/26. `validate_codex_compatibility.py` — exit 0, compatible/local_structure_only. `validate_hooks.py .codex/hooks.json`, `.codex/hooks`, `plugins/product-agent-os/assets/templates/hooks` — exit 0, errors=[].
9. `python -B tools/check_docs.py` и `git diff --check` — exit 0. Active/package hook и workflow побайтово совпали; negative probe artifact отсутствует. TEST.md собственная новая запись сокращена до указателя: 39 928 bytes, существующая история сохранена.
10. После уточнения workflow `python -B -m unittest tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_infrastructure_templates -q` — exit 0, 104 tests, 5.553 s. `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` — exit 0. Полный первый unittest `python -B -m unittest discover -s tests -p 'test_*.py' -q` — exit 1, 1452 tests / 846.351 s, failures=4, errors=1, skipped=1. Четыре failures — прежний site mismatch, подтверждён и устранён выбором уже проверенного isolated output. Ошибка `test_explicit_control_surfaces_are_proposals_only`: formation применял document budget 40k к Python hook, baseline 39 966 bytes, новый код выше порога. Исправление в `_budget`: default document ceiling не применяется к `.py`; явный project limit сохраняется. Отдельный RED `test_python_hook_is_not_a_document_but_explicit_limit_still_applies` — exit1, intended assertion failure.
11. Первоначальный affected rerun ошибочно включил несуществующий модуль `test_documentation_sync`: exit1, 184 tests, одна ImportError; остальные tests прошли. Правильные владельцы sync checks — `test_document_navigation` и `test_task_plan_lifecycle`. Исправленная команда `python -B -m unittest tests.product_agent_os.test_control_plane_compaction tests.product_agent_os.test_project_formation tests.product_agent_os.test_document_navigation tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_product_agent_os_docs -q` — exit 0, 209 tests, 56.378 s. Fixture final rerun — exit 0, 91/91, failed=0; raw synthetic receipt сохранён в ignored `.codex-tmp/report-read-fix/fixture-final.log`. Full final rerun `python -B -m unittest discover -s tests -p 'test_*.py' -v` — exit 0, 1453 tests / 946.243 s, OK (skipped=1: non-Windows guard only, текущая платформа Windows). Environment: workspace TEMP/TMP, PYTHONDONTWRITEBYTECODE=1, PAOS_DOCS_SITE_DIR=.tmp/paos-m4-0030/site-final.

## Другие ограничения правил: рекомендации, не выполненные изменения

Различать машинный deny и противоречивые инструкции: approval_contract и PermissionRequest summary сами по себе не доказывают дополнительный технический запрет. Их формулировки создают риск повторного согласования уже разрешённой работы; данный риск установлен статически. Узкий validator route и destructive/marker checks — исполняемые ограничения hook.

| Приоритет | Наблюдение и owning source | Рекомендуемое изменение |
| --- | --- | --- |
| P1 | `AGENTS.md` разрешает bounded synthetic loopback/browser/native/subagent checks; `.codex/config.toml` approval_contract и skill external_action_policy продолжают писать explicit/exact approval; `permission_request_summary.py` сообщает Approval remains undecided. | Согласовать wording с действующей standing authorization; повторно спрашивать только при выходе за её границы. |
| P1 | Default report route покрывает один Markdown; явно запрошенные JSON/CSV и изменения защищённых control-plane artifacts не получают write scope от research/planning marker. | Отделить разрешённые выходные артефакты от типа исследования; typed artifact-authoring scope с точными путями. Запрос на артефакт уже является разрешением в его границах, но не на изменение hooks или произвольного кода. |
| P2 | `_local_validation_read` допускает только два Python validators; tests и `tsc --noEmit` не являются обычным чтением, report/research scope их не разрешает. | Отдельный bounded verification scope: известная команда, допустимые TEMP/cache outputs и отсутствие provider/installation, без blanket Python/Node allow. |
| P2 | `build-slice.md` требует full coding-standard-checklist, а `coding-standards.md` допускает eight-field compact contract. | Согласовать build workflow с owning compact contract; full checklist только по применимому риску. |
| P2 | Destructive regex безусловно отклоняет `Remove-Item -Recurse`, несмотря на текст require explicit approval. | Отдельный проверенный маршрут очистки собственных fixtures или точное сообщение о неподдерживаемой форме; не agent-controlled approved=true. |
| P2 | Bootstrap own marker требует буквального shown-поля в patch, даже когда поле уже есть в файле. | Проверять результирующий marker и разрешённый переход собственной задачи; сохранить защиту foreign/mixed changes. |
| P3 | Control-plane size trigger может превратить небольшой update в lossless compaction; полные gates запускаются и для некоторых узких изменений. | Отдельно пересмотреть changed-contract routing и bounded handoff без потери evidence. В этом исправлении обязательные gates не отменяются. |

Sandbox read-only для `.codex` через shell, host trust, секреты, внешний scope, Git/publication, destructive production и реальные credentials остаются отдельными защитными границами. Снимать их ради удобства не предлагается.

## Control-plane sync и rollback

REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG и RU/EN runtime guide/registry обновляются по изменённому контракту и evidence. `prod_test.md`: not_applicable, исторический Batch39 не затронут. Formation/compaction уточнён: default document ceiling не относится к Python hook, explicit per-file limits сохраняются. Core AGENTS/config standing authorizations остаются прежними; другие найденные конфликты — рекомендации для следующего bounded slice.

Rollback: вернуть только текущие hunks active/package hook, workflow, тестов и документации; сохранить чужой untracked marker и исходный audit report другого чата. Hook definitions/trust не менялись. Действующий host подтвердил positive/negative route; отдельный запуск новой Codex session и общее AUD-HOST-02 не закрыты этим receipt.

## Проверенная ревизия

SHA-256 active/package `pre_tool_use_policy.py`: `1d47249acdeb13dd67d7e8c92f14a7561db6b34e76dcda6f28c36ac3f8898494`.
`hooks.json` без изменения: `8a40cbbb7bdc0b1d1b48d1ec873b109ee21358d85daae1479891e3a4fec74abb`.
Tests: `5936bf948fa80d01c1511d08be6a9216ab97f3a77de6fe20ab5d29e9325ad034`.

Параллельная работа: другой чат обновляет functional-remediation plan и общие control-plane/registry. Его строки сохраняются; они не входят в данный implementation slice. Последние проверки documentation отражают совместное рабочее дерево, а code/hash evidence выше относится только к report/read fix.

Scope integration repair: `control_plane_compaction.py` и его существующий test module включены после реального full-suite regression; `_restore` advisory относится к неизменённому recovery коду, его semantics не менялись. Повторный full run использует `-v` и `PAOS_DOCS_SITE_DIR=.tmp/paos-m4-0030/site-final`; log `.codex-tmp/report-read-fix/full-unittest-final.log`.

Budget self-review: `_budget` продолжает валидировать config/limits, explicit per-file limit учитывается до исключения, PLAN.md >40k по-прежнему отвергается. Только default `.py` ceiling исключён; compaction writers по-прежнему принимают Markdown и не получили права менять Python.

## Итог

Status: implemented_current_host_verified. Current-host create/update/update и neighboring-path deny подтверждены; active/package source совпадает. Final full1453/skip1, focused209, fixtures91/91, transcripts26/26, compatibility/hooks/check_docs/diff пройдены; после финальных status updates combined docs/lifecycle/hooks/infrastructure checks — exit 0, 253 tests / 34.907 s (`python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_infrastructure_templates -q`). Initial failures и setup limitations выше сохранены. Fresh-session activation, чужие уже открытые контексты и полный AUD-HOST-02 не заявляются.

Review: separate_reused_context, один read-only reviewer, два прохода; два P1 исправлены и проверены root self-review/regressions. Интеграционная правка document budget прошла отдельный RED/GREEN и повторный full gate. tester_verdict=closed_allowed для данного scope. Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG, RU/EN runtime/registry updated; prod_test not_applicable. Дальнейшие правила из таблицы — рекомендации, не скрытые изменения политики.
