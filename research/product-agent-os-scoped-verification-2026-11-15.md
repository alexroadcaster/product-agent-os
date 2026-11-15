# Проверки по изменённому контракту — 15.11.2026

Source status: repository implementation and focused local checks.

Задача: `PAOS-SCOPED-VERIFICATION-2026-11-15`. Пользователь явно запросил
упрощение проверок и повторяющихся напоминаний с сохранением данных и разрешений.
Изменения ограничены локальными правилами, проверками, advisory hooks и связанными
контрактами. История Git, внешние сервисы, provider calls и пользовательское
приложение не изменялись этой работой.

## Поведение

- Единственный текущий маршрут — [TEST.md](../TEST.md). План и MD-отчёт не требуют
  общего docs/runtime suite. Исторические команды сохраняют provenance и не
  расширяют текущий маршрут. [AGENTS.md](../AGENTS.md) ссылается на него.
- `python -B tools/check_docs.py --paths <files...>` проверяет выбранные Markdown:
  UTF-8, применимый Source status, существование файлов и локальных ссылок,
  ограничение путей workspace. Примеры в code blocks не считаются реальными ссылками.
  HTML, anchors, внешние URL и семантическая истинность текста этой командой не проверяются.
  Вызов без `--paths` сохраняет прежний явный полный аудит документации.
- `test_product_agent_os_docs` содержит исходные source contracts. Installer —
  `test_docs_installer`. `site_checks` и `docs_archive_checks` запускаются явно и
  не попадают в обычный `test_*.py` discovery. Все 105 прежних имён методов сохранены;
  пять смешанных методов разделены между history/source и HTML. Повторные HTML
  assertions M48 уже покрыты switcher/search/parity сценариями. Удалены устаревшие
  ограничения количества текущих страниц и обязательного размера текущих root docs.
- Полный fixture/transcript набор выполняется внутри соответствующих unittest
  проверок; повторный runner после full discovery не нужен. CLI использует маленькие
  положительные/отрицательные fixtures. `run_fixture_eval.py --summary` выдаёт краткий
  JSON, сохраняет exit 1 для ошибок и пустого набора. Старый полный JSON совместим.
  Два fixture unittest-модуля используют общий test-only cache; весь baseline
  вычисляется один раз в процессе, изолированные mutation/single-fixture tests сохранены.
- Per-write PostToolUse удалён из active/mirror/package definitions. Старый evidence
  script — тихий compatibility no-op; comment advisory работает только с `--review`.
  Уже загруженные старые команды также не выводят обычные напоминания. PermissionRequest
  напоминает о сохранении существующей авторизации, не принимает approval decisions.
- PreToolUse дополнен точной no-output-file командой `python -B tools/check_docs.py --paths <workspace Markdown paths>`, чтобы новая проверка не блокировалась в report/terminal scope. Иной cwd, explicit shell, выход за root, лишние параметры и произвольный Python этой веткой не разрешаются. Остальные защитные условия, SessionStart и Stop implementation сохранены.
  Валидатор требует защитные события и не допускает пустые required event lists;
  необязательный PostToolUse проверяется, если указан.
- Default 40 000 bytes — advisory для обычных sync/formation. Явные per-file
  limits остаются обязательными, включая повторную проверку при apply. Явно
  запрошенная compaction сохраняет hard limit, byte preservation и recovery.
  Hygiene также сообщает warning для эвристики; explicit limit применяется ровно
  как настроен и не обходится архивной классификацией. Secret/invalid-policy/UTF-8
  ошибки остаются ошибками.
- Обычные contextual edits не требуют отдельного sync-пакета. Координированное
  изменение machine state/revision pins сохраняет digest, journal и conflict checks.
  Полный coding checklist остаётся справочным материалом для соответствующего риска.

## Проверки текущего запуска

Все перечисленные проверки выполнены без полного unittest discovery, полного
fixture/transcript runner, установки зависимостей или новой сборки сайта.

| Изменённый сценарий | Результат |
| --- | --- |
| `test_docs_check_routing` + новый source-only `test_product_agent_os_docs` | 8 tests, 0.821 s, passed; после review дополнительно reference links RED → GREEN, окончательный routing module 6 tests, 0.211 s. Проверены выбранный отчёт без сайта/посторонних docs, broken links, missing/outside paths, Source status, code examples, suite isolation |
| `test_lifecycle_hooks` после отключения автоматических advisories | 44 tests, 27.052 s, passed; включены report/read, foreign sessions, protected paths, destructive commands и permission boundaries |
| 6 точных hooks/template tests после изменения permission summary и definitions | 6 tests, 0.720 s, passed; parity active/package и тихий PostToolUse |
| 4 финальных PreToolUse scenarios после добавления exact docs-check command | 4 tests, 13.883 s, passed; RED4 subcases до исправления. Проверены argv/cwd/shell/path restrictions, report create/update, mutation boundary и foreign session spoofing |
| 5 точных validator tests | 5 tests, 1.098 s, passed; optional advisory, required protection events, CLI shape и secret literals |
| `site_checks` с `PAOS_DOCS_SITE_DIR=.tmp/paos-m4-0030/site-final` | 7 tests, 1.496 s, passed на существующей сборке; новая сборка/свежесть сайта не заявляются |
| 4 изменённых fixture/transcript CLI/summary tests | 4 tests, 15.489 s, passed; success/failure/empty, evaluator once, single-fixture CLI |
| 2 затронутых fixture main/renderer failure tests | 2 tests, 0.506 s, passed |
| Общий cache двух fixture modules + summary regression | RED отдельные результаты → GREEN 2 tests, 0.307 s; evaluator вызывается один раз, mock cache восстанавливается |
| `test_document_navigation`, `test_control_plane_compaction` и 3 выбранных formation tests | 35 tests, 13.270 s, passed; oversized default, explicit limit, recovery, stale/tampered proposal, concurrent edit, SQL/frozen authority, traversal, secrets |
| 10 выбранных hygiene size/CLI/safety/trigger tests и финальный повтор изменённого archive-limit scenario | 5 tests/2.116 s + 5 tests/0.467 s + 1 test/0.231 s, passed; explicit50000 RED3 → GREEN, default warning, secret/UTF-8/policy errors сохранены |
| 3 выбранных lifecycle/infrastructure/professional eval-contract tests | 3 tests, passed; advisory default и explicit hard limits |
| 5 изменённых archive current-policy methods | 5 tests, passed; полный исторический аудит не запускался |
| Active/mirror/package hook validators | Все три exit 0 после исправления требования PostToolUse |
| `python -B tools/check_docs.py --paths` для 17 изменённых Markdown | exit 0; без сайта/архива |
| `git diff --check` | exit 0; Git уведомляет только о CRLF/LF |

RED/исправления: старый checker пытался читать отсутствующий посторонний registry
при проверке одного отчёта; прежние hooks выводили напоминания; validator требовал
PostToolUse; sync отвергал большой документ без explicit limit. Эти наблюдаемые
отказы воспроизведены до исправлений. Новая summary API сначала отсутствовала.
В процессе исправлены устаревшие literal assertions политик и неверный owner path
в formation fixture. Shell-запись protected `.codex/hooks.json` получила
PermissionError; точное явно запрошенное изменение применено через разрешённую
sandbox escalation, без изменения sandbox или trust.
Review воспроизвёл пропуск reference-style Markdown links; новый regression
сначала падал на missing/outside targets, после исправления прошёл. Статическая
проверка полной идентичности active/package eval/workflow обнаружила их прежние
project/template различия; проверены общие изменённые поля и полная идентичность
hook mirrors, без перезаписи различающихся по назначению контрактов.

## Review, сохранность и границы

Независимые workstreams: policy, eval CLI, document limits; root интегрирует docs
split/checker и hooks. Review выявил и устранил stale size/count assertions,
старые mandatory full gates в EVALS и противоречия current-state RU/EN.
При переносе тестов проверено сохранение исходных имён; изменения соседнего чата
в функциональной матрице и root handoff сохранены.
AST-сравнение PreToolUse подтвердило изменение только `_local_validation_read`;
остальные функции безопасности и session/path/mutation guards сохранены, package
mirror совпадает. После этой правки hook validator снова прошёл.

Control-plane sync: TEST/EVALS обновлены как владельцы маршрутов и eval-политики,
RUNLOG содержит краткий handoff; source registry и RU/EN operating docs согласованы.
REQUIREMENTS/PLAN — no_change_needed: отдельные продуктовые требования, очередь и
machine task status этим maintenance-срезом не менялись; prod_test не относится к задаче.

Это локальная проверка изменённых контрактов. Fresh-session discovery/trust/loading,
общая продуктовая приёмка, свежесть canonical `site/` и полный исторический аудит
не заявляются. Уже открытые чаты могут сохранять старые текстовые инструкции.
Rollback — только изменения этого среза с сохранением последующих пользовательских
правок; compatibility scripts оставлены, чтобы старые hook bindings не ломались.
