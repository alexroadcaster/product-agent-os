# PAOS-AUD-G7 — реализация и приёмка, 09.11.2026

Source status: project-local current-run implementation evidence; owner acceptance pending; fresh-session activation excluded.

## Границы результата

Owning matrix: [PAOS-AUD-G7](product-agent-os-audit-remediation-task-plan-2026-11-09.md). Baseline — `a1c31b922953d1fd0afcd67c7485950677a6ca5b`; изменения G7 локальные. Root — единственный writer G7. Параллельные Web docs и чужие lifecycle markers сохранены. Git history, явные изменения cache/trust, установки и fresh-session activation не выполнялись. Денежный cap снят владельцем; разрешён только доступный Codex, создание API-ключа отклонено.

## Реализованные механизмы

| Задача | Изменение | Проверяемая ценность и предел |
| --- | --- | --- |
| T01 | Active/package standards, восьмиполевой compact contract, conditional checklist | Минимальное полное решение, invariants и owner/trigger долга вместо LOC/coverage quota. Текст сам по себе не доказывает поведение агента. |
| T02 | `test_strategy_selector.py`, existing task routing | Refactor/config не требуют искусственного RED; feature/defect сохраняют test-first. Уникальные regression/security checks не удаляются. |
| T03 | Evidence-based review workflow, reviewer profiles, отдельный `g7_quality_eval.py`, rubric v2 | Finding требует revision/source/scenario/consequence/action/evidence; preference не veto; deferred требует owner/trigger. Валидация структуры не доказывает истинность finding. |
| T04 | Active/package literal read classifier | Quoted regex/read pipeline доступны без ложного mutation gate; unknown executable, newline, quoting escape, redirection/custom shell остаются на защищённом маршруте. Это узкий PowerShell literal subset, не универсальный shell parser. |
| T05 | Bounded `capability_summary`, CLI integration, evidence invalidation | Scope/privacy/omitted/unknown явны; manifest читается один раз, lock/config/environment влияют на digest. Declaration не выдаётся за installation или reference coverage. |
| T06 | Stack tool candidates и profile policy | Import Linter/dependency-cruiser/Stryker распознаются как declarations. Actual installed/runnable/verified и transitive architecture-rule smoke пока не доказаны; инструменты не установлены автоматически. |
| T07 | Отдельные design/manifest/oracles, generation projection и denominators | Frozen T34 не изменён; reference проходит, stub/unsafe не проходят; unknown/skipped/missing не становятся pass. Строгая изоляция model runtime остаётся отдельным gap. |
| T08 | Воспроизводимое локальное сравнение и ограниченный Codex pilot | Локальные функции baseline/current сравниваются на одинаковых 10 случаях; observational Codex evidence отдельно от strict A/B и owner acceptance. |

## Сравнение локальных механизмов

Команда: `python -B plugins/product-agent-os/scripts/run_g7_quality_comparison.py --output docs/superpowers/specs/paos-aud-g7-code-quality-eval-results.json`.

[Design](../docs/superpowers/specs/paos-aud-g7-code-quality-eval-design.json), [результат](../docs/superpowers/specs/paos-aud-g7-code-quality-eval-results.json), [manifest](../tests/fixtures/product_agent_os/g7-code-quality-evolution/manifest.json). Baseline использует pinned функции и общий current profile factory, а не полный исторический runtime.

| Сценарии | Baseline | G7 |
| --- | --- | --- |
| Literal regex, read pipeline | 0/2 | 2/2 |
| Unknown executable, escaped option | 0/2 | 2/2 |
| Newline write, redirection | 2/2 | 2/2 |
| Behavior-preserving refactor | 0/1 | 1/1 |
| Configuration, defect, new behavior | 3/3 | 3/3 |
| Итого соответствуют ожидаемому поведению | 5/10 | 10/10 |

Все 10 eligible cases выполнены в каждом arm; missing/skipped = 0. Это targeted regression corpus, выбранный для данных дефектов; результат не означает двукратного роста качества генерации или ускорения продукта. Performance по длительности unittest не заявляется.

## Независимые мнения и обработка findings

Три агента запущены по запросу владельца, read-only ownership, `context_mode=separate_reused_context`. Они не являются blind generation reviewers.

| Reviewer | Мнение и findings | Действие |
| --- | --- | --- |
| `/root/g7_standards_review` | Поддержал минимальный контракт, но потребовал исправить privacy/scope inventory, deferred review и отделить tool declaration от evidence | Scoped projection исключает private/unrelated paths, deferred требует owner/trigger. Реальное architecture-tool evidence оставлено открытым. Последние исправления проверены root tests, без утверждения повторного независимого approve. |
| `/root/g7_guard_review` | Воспроизвёл старые false positives и bypass; нашёл newline, legacy quoting, escape и splat cases; после исправления одобрил ограниченный literal subset | Соответствующие отрицательные wire cases добавлены. Agent проверил 3 теста, exit 0; последующее переименование локальных переменных semantics-neutral проверяется общими gates. HOST activation не заявлялась. |
| `/root/g7_eval_review` | Независимо воспроизвёл 5/10 → 10/10 и 19 tests OK; потребовал точный output path, instrument hashes, ненулевой exit при treatment failure и честную empty-review label | Исправлено; executable oracle controls/context projection добавлены позднее и проверены root. Strict model isolation и стоимость следующего изменения не выводятся из локальных scores. |

## Текущие проверки

Во всех тестах с temporary workspaces `TEMP`/`TMP` указывают на ignored `.docs-tools/reports/g7-deep-review-temp`; Windows sandbox temp оказался недоступен. Это process-local выбор writable directory, не изменение permissions.

| Проверка | Наблюдение |
| --- | --- |
| Guard literal classifier RED | Старый guard: 16 неуспешных subcases; после исправления focused GREEN |
| Refactor CLI RED | Старый selector возвращал required; после исправления not_applicable |
| Newline terminal wire RED | Воспроизведён false allow; исправлен и проверен |
| Codex event parser RED/GREEN | Incomplete tool start и known config warning проверены отдельно; unknown errors по-прежнему блокируют |
| Focused standards/behavior/CLI/G7/hooks/skills | 182 tests, 30.795 s, exit 0 до semantics-neutral lexer rename и новых pilot tests |
| G7 + frozen legacy eval/reviewer/metrics | 24 tests, 0.251 s, exit 0 после новых pilot tests |
| Первый full unittest | 1350 tests, 664.055 s, 25 failures, 1 skip: generated guard не прошёл secret-like literal validator из-за локальных имён token/tokens |
| Исправление integration failure | Переменные переименованы в lexeme/lexemes; secret validator не ослаблен |
| Fixture eval, первый запуск / повторный | Exit 1, 91/91 blocked; после исправления exit 0, 91/91 passed |
| Transcript eval | Exit 0, 26 passed, 0 failed |
| Codex compatibility | Exit 0; standalone skills/workflows scope, не native plugin activation |

Последующий full retest: 1354 tests, 545.077 s, 13 failures, 1 skip — новый внутренний report ошибочно попал в bilingual site inventory. Report перемещён в research (без ослабления tests); `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q`: 105 tests, 7.711 s, exit 0. Финальный frozen полный прогон завершился успешно: 1357 tests, 482.796 s, exit 0, один platform skip. `check_docs.py`, task-matrix/state validators, active/package agents и hooks validators — exit 0. G7 module после parser repair — 10 tests, 0.056 s, exit 0.

## Codex pilot — provenance и ограничения

Используется установленный `codex-cli 0.167.0`, ChatGPT authentication; requested `gpt-6.1-sol`, medium (effective server model/effort не attested), read-only, shell/agents/apps/browser выключены, web search disabled. `tools.disable_defaults=true` отклонён strict-config как unknown; полного пустого tool schema это не доказывает. Официальный источник: [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference), прочитан 09.11.2026; CLI help/config проверены локально.

Exact runner: `python -B plugins/product-agent-os/scripts/run_g7_codex_pilot.py --codex-executable <installed codex.exe>`. Первые две попытки — setup_error/Access denied до model events; повтор через approved execution permissions сохранил read-only child sandbox. Следующие две diagnostic генерации были ошибочно отнесены к ineligible: item.type=error содержал известное предупреждение об ignored metadata config. Narrow classifier исправлен RED/GREEN; обе попытки сохранены. Никакие outcome thresholds или prompts по ответам модели не улучшались.

Измеряемая серия: две цепочки (2 + 4 шага), baseline/treatment, 12 генераций, timeout 180 s/call; максимум 16 attempts вместе с setup/diagnostic attempts. Любой tool start или unknown error останавливает серию; кандидаты runner не исполняет. Все raw reasoning/ambient transcripts не сохраняются; retained candidate text, event kinds, usage, hashes и bounded redacted diagnostics. Source input предыдущего шага передаётся следующему в том же arm. Оба arm имеют общий ambient Codex context; это observational comparison, не strict isolated A/B.

### Фактический результат Codex pilot

[Полный receipt, кандидаты и frozen executed design v8](../docs/superpowers/specs/paos-aud-g7-codex-pilot-results.json). 16 attempts = 2 setup без generation + 2 diagnostic generation + 12 measured generation; всего 14 generation completions. Предыдущие receipts сохранены, но не все тела diagnostic candidates: reused candidate_file не считать оригинальным источником.

| Метрика одной серии | Baseline | G7 treatment |
| --- | --- | --- |
| Проверенные шаги двух последовательных цепочек | 6/6 | 6/6 |
| Наблюдавшиеся classified tool events | 0 | 0 |
| Latency, сумма секунд | 89.193 | 86.773 |
| Input tokens / cached input | 184033 / 22656 | 184234 / 22656 |
| Output tokens | 1221 | 1059 |
| Changed lines, advisory | 49 | 34 |
| Monetary cost | null | null |

Шаги зависимы, это не шесть независимых кейсов. В output code-only tasks нет вопросов по построению задания; это не доказательство снижения intervention в реальном workflow. Token/latency/churn различия не имеют статистического или причинного вывода по одной серии.

Root прочитал все 12 candidate sources до исполнения; использованы только synthetic in-memory state и callbacks без внешних эффектов. Воспроизведение: `python -B docs/superpowers/specs/paos-aud-g7-codex-pilot-verification.py` — exit 0, replayed 12, passed 12. Скрипт разрешает только точные SHA девяти уникальных прочитанных исходников, не является sandbox для произвольного generated code.

Дополнительная callback snapshot (вне frozen score): baseline во время notify показывает balance=70/seen=[one], treatment balance=100/seen=[]. Первый контракт требовал notify до записи успеха. Поэтому 6/6 frozen checks не означает полное соблюдение ordering: итоговый oracle пропускал этот риск. Пересчитывать score задним числом не стали. Reviewer предпочитает treatment для заданного synchronous scope: на failure step он не меняет уже достаточный код. Reentrancy/concurrency/ambiguous external delivery не исследованы; exactly-once не заявляется.

Дополнительный reviewer `/root/g7_eval_review` независимо подтвердил design/runner hashes, 12 sequential prompt hashes, candidate SHA/AST и aggregates (read-only `python -B -`, exit 0). Он нашёл acceptance неполного/malformed event stream в runner. Воспроизведён RED, исправлен GREEN; current design v9 относится к будущим запускам, measured v8 и source runner сохранены в receipt. Новых provider calls после repair нет.

Reviewer `/root/g7_standards_review` независимо поддержал treatment за сохранение порядка эффектов и no-change на уже выполненном требовании; superiority компонентов и strict A/B оставил insufficient_evidence.

## Открытые условия приёмки

- Owner decision keep/revise/no-go пока null; manual_only сохранён.
- T06: actual tool version/config/resolver и allowed/forbidden/transitive fixtures не выполнены при отсутствующих tools; declared profile не означает verified architecture.
- T07/T08: strict runtime context/tools isolation и полноценные end-to-end cost/intervention metrics требуют отдельного доказательства. Time/sunk-cost/incorrect-review pressure сценарии и отдельный justified/overbuilt evaluator control в текущем 2-chain corpus не исполнены; их acceptance остаётся открытой. Одно повторение и общий ambient context не позволяют причинный вывод о superiority.
- Fresh-session activation HOST-01/HOST-02 остаётся отдельно; G6 и frozen T34 не закрываются через G7.

Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG и registry RU/EN обновляются компактными pointers. prod_test — not_applicable (Batch 39 evidence не меняется); strict MkDocs — not_applicable (G7 не меняет navigation/rendering/config/site). Rollback — только G7 hunks, без чужих Web изменений и без удаления отрицательных receipts.

## Scope и сохранность

Проверено current-run `python -B -`: G1–G6 prefix совпадает с HEAD; все восемь карточек G7 сохранили ровно 36 полей и исходные имена/порядок. `git diff --quiet HEAD -- <path>` подтвердил неизменность T34 eval_design/reviewer_contract/code_quality_metrics и исторического results. Active/package validators — exit 0.

T06 discovery: `Get-Command ruff, lint-imports, depcruise, stryker` не нашёл команды; importlib.metadata не нашёл ruff/import-linter в текущем Python; project node_modules bins и .venv-docs Scripts не содержат этих tools. Это проверенные locations, не утверждение об отсутствии на всём компьютере. Новый install/CI/config не выполнялся.

Final targeted regression: `python -B -m unittest tests.product_agent_os.test_g7_code_quality_evolution tests.product_agent_os.test_batch45_code_quality_eval_design tests.product_agent_os.test_batch45_code_quality_reviewer tests.product_agent_os.test_batch45_code_quality_metrics tests.product_agent_os.test_lifecycle_hooks -q` — 66 tests, 11.764 s, exit 0. Это также покрывает последний parser repair после начала full discovery; тот full run импортировал предыдущую версию test module.

Последний mixed-state full run: 1356 tests, 527.344 s, 1 failure, 1 skip. Единственный failure — старый загруженный test_known_cli_config_warning... против уже исправленного parser, добавившего обязательный turn.completed. Current targeted 66 tests прошли; окончательный full rerun после freeze всех runtime/test файлов завершился: 1357 tests, 482.796 s, exit 0, 1 platform skip. Skip — test_apply_is_rejected_on_non_windows, причина non-Windows guard only (текущая среда Windows).

## Предложение для приёмки (не решение владельца)

| Компонент | Рекомендация root | Основание / граница |
| --- | --- | --- |
| T01 minimal-complete contract | keep локальный контракт | Восемь полей сохранены; treatment распознал уже достаточный код. Причинный эффект общего стандарта insufficient_evidence. |
| T02 risk-based tests | keep локальный selector | Refactor/config без artificial RED; feature/defect сохраняют test-first; mandatory checks не сняты. |
| T03 evidence-based review | keep контракт v2 | Stale/unsupported/deferred findings не считаются закрытыми; preference не veto. Semantic review остаётся человеческим/агентным. |
| T04 literal read guard | keep локальный patch | RED/GREEN и negative wire coverage; fresh-session отдельно. |
| T05 bounded capability | keep локальную проекцию | Scope/privacy/omitted/unknown сохранены; current CLI подключён. Dynamic references не доказаны. |
| T06 architecture tools | revise / завершить проверку tools | Declarations/profile готовы; actual allowed/forbidden/transitive smoke и resolver coverage ещё нет. |
| T07 extended evaluator | revise / расширить следующий frozen corpus | Текущий pilot не покрывает pressure cases и strict isolation; добавить callback ordering без ретроспективного изменения исходного score. |
| T08 adoption decision | needs_user_acceptance | Принять bounded local results возможно; глобальное superiority и закрытие всей группы пока unsupported. |

Owner decision во всех пунктах — null до явной приёмки. Эти рекомендации не являются auto-promotion, installed cache update или fresh-session activation.

## Итоговый уровень закрытия

`closure_level = partially_verified`. T01–T05 — implemented_locally_verified; T06–T08 — in_progress с названными acceptance gaps. Full command: `python -B -m unittest discover -s tests -p 'test_*.py' -v`, exit 0, 1357 tests, 482.796 s, OK (skipped=1). Log: `.docs-tools/reports/g7-full-frozen.log`. Все перечисленные provider/model attempts завершены; дальнейших вызовов нет. Owner acceptance null; запуск свежей host session не выполнялся.

Control-plane sync выполнен для REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG и registry RU/EN. Root compactness ниже 50 KiB; prod_test not_applicable. Коммиты/ветки/stage/push не выполнялись.

Closure docs recheck: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q` — 105 tests, 7.304 s, exit 0 после итогового status sync. Matrix/state/check_docs/diff checks — exit 0. Custom root compactness, measured v8 design/runner hashes, guard byte parity и report local-link checks passed. Попытка сравнить весь active workflow с неотрендеренным packaged template дала AssertionError из-за ожидаемых project placeholders/active routing preamble; scoped G7 Minimal Complete Changes section совпадает, existing template tests прошли.

## Продолжение T06–T08: приёмка T01–T05

09.11.2026 владелец явно принял результаты T01–T05 и поручил завершить T06–T08. Предыдущие owner=null записи — исторический pre-acceptance receipt; текущий owner decision T01–T05=accepted. Доступный Codex разрешён, создание API-ключа исключено, fresh-session activation отдельно. Runtime/test work будет заморожен до итогового full gate, чтобы исключить mixed-state результаты.

### T06 installation/test packet (до установки)

Exact synthetic scope: tests/fixtures/product_agent_os/g7-architecture/manifest.json перечисляет каждый файл и SHA. Python Import Linter 2.16 (BSD-2-Clause, Python >=3.11), JS dependency-cruiser 18.6.0 (MIT, Node ^22/^24/>=26). Текущие Python 3.13.5, Node 26.5.0. Предлагаемая изолированная установка: `.docs-tools/g7-architecture-tools/python` (venv, wheels-only import-linter==2.16) и `.docs-tools/g7-architecture-tools/javascript` (npm --ignore-scripts --no-audit --no-fund --save-exact dependency-cruiser@18.6.0). Только synthetic report-only commands, без target config/CI/global PATH/auto-fix. Rollback — перестать использовать эти отдельные tool dirs, не менять системные пакеты. До явного разрешения установка не выполняется.

### T06: approved installation and first actual scan

Владелец разрешил exact local installation/test packet в текущем продолжении. Import Linter 2.16 установлен offline из SHA256-pinned wheelhouse; dependency-cruiser 18.6.0 установлен через npm ci --ignore-scripts --no-audit --no-fund (43 packages, registry/integrity проверены). Version probes: 2.16 / 18.6.0. Первый ensurepip запуск не прошёл из-за TEMP permissions; повтор с workspace TEMP прошёл. Первый guessed JS entrypoint отсутствовал; package bin прочитан, правильный entrypoint проверен. Ни один из этих setup failures не является behavioral pass.

Первый scan обнаружил дефект synthetic JS config: includeOnly исключал unresolved #missing edge до проверки. Фильтр удалён; scope остаётся src, doNotFollow node_modules. JSON process exit 0 не означает clean: читается summary. Python 4 controls распознаны: allowed KEPT, direct/transitive BROKEN с конкретными цепочками, cycle с двумя opposing edges. Результаты повторного полного scan сохраняются отдельно.

### T06: реализация и исправления после review

Команда `python -B plugins/product-agent-os/scripts/run_g7_architecture_checks.py --run-approved-fixtures` распознала 10/10 ожидаемых результатов, exit 0. [Receipt](../docs/superpowers/specs/paos-aud-g7-architecture-results.json) закрепляет manifest, runner, версии, конфигурацию, lock, scope/resolver/type-only policy и concrete findings. Точный состав файлов и cases проверяется до scan. Неожиданный файл инвалидирует корпус; пустой набор controls не проходит. Проверяются точные endpoints, transitive path через bridge, оба ребра цикла, alias #db и unresolved #missing. Setup failure предварительно инвалидирует прежний green receipt.

Pure projection различает installed/runnable/verified/verified_clean, отклоняет stale/ambiguous/incomplete observations. Baseline сопоставим только после completed full scan с controls; known/new_or_changed/absent_candidate не изменяют baseline. Ordinary discovery остаётся declaration-only; optional API предназначен для доверенных локальных receipts с независимо вычисленным current context, не для произвольных загруженных отчётов.

RED: до реализации assertion verified_clean провалился; setup failures не засчитаны behavioral RED. Final focused GREEN: 37 tests (projection, evolution, trace). Первый evolution run с default sandbox TEMP дал PermissionError; workspace TEMP исправил среду без изменения ACL. Первый fixture evaluator с default TEMP завершился вторичным UnboundLocalError; повтор с workspace TEMP прошёл. Это setup limitations, не successful checks.

Независимый reviewer обнаружил exact-set, stale-green, witness и baseline defects; они исправлены. Дополнительный прогон выявил недетерминированный порядок вывода двух рёбер Python cycle: 9/10 при тех же правильных рёбрах. Cycle сравнивается по точной паре без порядка; transitive path остаётся ordered. CLI --help теперь не запускает checks: требуется явный --run-approved-fixtures. Full suite и fixture evaluator остановлены до правки, затем запущены заново на frozen corrected files; прерванные запуски не считаются passed.

Финальный независимый read-only review подтвердил 10/10 и актуальные hashes runner/manifest. Verdict: локальная реализация Python/.mjs и trusted API допустима после обязательных gates. 10/10 означает совпадение с ожидаемыми outcomes, не 10 clean scans. Shared domain-no-infra имеет allowed/forbidden/transitive controls. Дополнительный Python independence contract подтверждён конкретным отрицательным cycle case, без отдельной полной qualification matrix. Unresolved case распознан, но verified=false. TypeScript resolver/type-only, target project и activation не проверены.

### T07: дополнительные evaluator controls

[Pressure manifest](../tests/fixtures/product_agent_os/g7-pressure/manifest.json) закрепляет deadline, sunk-cost и incorrect-review inputs с явным callback/state ordering contract и требованием batch reuse. Reviewed justified и overbuilt реализации обе проходят executable correctness; лишняя структура advisory и не переопределяет correctness. Unsafe candidate проваливает callback boundary. Это новый supplementary corpus, не ретроспективный held-out score прежних генераций.

### T07: фактический trace и остановка модельного сравнения

Проверка узкой filesystem isolation в текущем проекте не прошла: elevated backend требует effective root read; MXC недоступен на executor. ACL и проект не менялись. Первый обычный trace preflight завершился nonzero; inference count не установлен. Второй bounded preflight через существующий Codex ChatGPT login сохранил read-only child, hooks/rules и отключил известные MCP/access channels. [Безопасный receipt](../docs/superpowers/specs/paos-aud-g7-isolation-preflight-results.json) подтвердил gpt-6.1-sol, medium, один inference и **два additional tools**. Парсер также выдал provider_mismatch: ожидаемый identifier не совпал; actual label не сохранялся, поэтому это не доказательство другого provider.

Tool activity не обнаружена. Заданные hidden markers не обнаружены, но это не доказывает filesystem isolation или отсутствие любой contamination. Strict model comparison остаётся blocked по прежнему isolation/tool restriction gate. После этого pressure/comparative generations не запускались. Новых preflight attempts — 2; один completed/attested inference, первый nonzero с неизвестным inference count. Raw context/reasoning/trace удалены; API-ключ, auth/trust/ACL и отдельный проект не создавались. Прежние 12 observational generations сохранены без изменения оценок.

### Решения по компонентам для приёмки

| Компонент | Рекомендация | Доказательства и границы |
| --- | --- | --- |
| T01–T05: contracts, risk-based checks, review, guard, capability map | keep | Уже приняты владельцем; local mechanism comparison 5/10 → 10/10, без общего generation-quality claim |
| T06: архитектурные проверки Python/JS и receipt projection | keep в проверенной области | 10/10 external-tool scenarios; immutable baseline, report-only, trusted receipt API |
| TypeScript resolver/type-only execution | insufficient_evidence | Inventory routing существует; actual corpus .mjs, TS compiler не устанавливался |
| T07: pressure и evaluator controls | keep как подготовленный instrument | Correct/unsafe и justified/overbuilt проверены; модельные outcomes не получены |
| Превосходство модели / component effect | insufficient_evidence | Strict preflight blocked; прежние 6/6 на arm observational, без causal advantage |
| T08: окончательное закрытие G7 | no-go пока | Required T07 evidence и owner decision по T06–T08 остаются открыты |

Запрос на реализацию не заменяет приёмку ещё не предъявленных результатов. T01–T05 accepted; T06 предъявляется для приёмки; T07/T08 открыты. Fresh-session activation — самостоятельная открытая задача и не используется как зависимость локальных пилотов.

### Control-plane sync этого продолжения

REQUIREMENTS.md — authority/scope; PLAN.md — T06–T08 очередь и revision pointer; TEST.md — actual commands и workspace TEMP; EVALS.md — supplementary corpus и trace admission; RUNLOG.md — handoff/gaps: update_required, обновлены. Registry RU/EN и coding-standards RU/EN синхронизированы. prod_test.md — not_applicable: Batch 39 evidence не меняется. REQUIREMENTS.md был выше 50 KiB после добавления authority; собственный G7 paragraph сокращён, детали остаются в этом отчёте; все root files ниже 50 KiB. Чужие Web sections/marker сохранены. Strict MkDocs — not_applicable: nav, Mermaid, extensions, config, search/sitemap и site evidence не изменялись. Локальные ссылки затронутых report/coding pages проверены, отсутствующих нет. Остаточных raw trace directories нет.

Текущие завершённые gates: focused 37 tests; docs 105 tests; fixture 91/91; transcript 26/26; compatibility exit 0; active agents 15/15 и packaged 8/8; оба hook validators; task matrix/state consistency; docs structure; diff --check. Полная suite на final frozen runtime выполняется; её итог будет добавлен отдельным receipt ниже. Ранее опубликованные 1357 tests относятся к предыдущему запуску, не к этому продолжению.

### Итоговая проверка frozen runtime

`python -B -m unittest discover -s tests -p 'test_*.py' -v` с workspace TEMP/TMP: **1372 tests за 783.819 s, exit 0, OK (skipped=1)**. Skip: non-Windows guard на Windows. Журнал: `.docs-tools/reports/g7-continuation-full-final.txt`. Исходники runtime/tests не менялись после запуска. T06 — implemented_locally_verified / needs_user_acceptance. T07 — blocked на фактическом isolation gate; T08 — in_progress, owner decision pending; G7 — partially_verified.

Повторное локальное сравнение на актуальном instrument digest: baseline 5/10 → treatment 10/10; это deterministic repository mechanisms, не новая модельная оценка. Прежние 6/6 на arm остаются историческим observational pilot. Независимый T06 reviewer подтвердил текущий receipt и все 68 fixture hashes; другой агент реализовал trace parser/tests, security reviewer дал read-only design. Context mode: separate_reused_context, не fresh_blind_review. Общий tester_verdict=partial_only из-за обязательного незакрытого T07.

Финальный docs rerun: 105 tests / 11.341 s / exit 0. Docs structure/state consistency/diff passed. Первый финальный matrix validator отклонил ISO timestamp для implemented T06; формат приведён к требуемому DD-MM-YYYY HH:mm (09-11-2026 20:23), factual timestamp не изменён; matrix retest записан ниже.

Финальный matrix retest: validate_task_matrix.py → ok=true / exit 0; check_docs.py → OK / exit 0; diff --check → exit 0. Scope включает sanitized preflight receipt, revision pointer обновлён. Финальный diff review: только собственные G7 hunks/новые synthetic artifacts; чужие Web sections и marker не откатывались. Installed packages/caches исключены локальным .gitignore; reviewable locks/receipts остаются. Git staging/commit/push не выполнялись.

## T07: продолжение 10.11.2026

Current authority: выполнить T07 через доступный Codex, без API-ключа; T08 owner acceptance и fresh-session activation отдельно. Предыдущие результаты сохранены. Состояние G7 на старте уже зафиксировано в Git другим действием владельца; текущие чужие Web edits сохранены, Git history actions здесь не выполнялись.

Диагностика: первый compound read отклонён terminal lifecycle marker; раздельные read-only команды прошли, собственный marker открыт после видимого brief. Actual CLI 0.167.0. Документированный [model_catalog_json](https://learn.chatgpt.com/docs/config-file/config-reference) позволяет startup capability reduction для той же gpt-6.1-sol: только tool_mode=direct, apply_patch_tool_type=null, experimental_supported_tools=[], остальные metadata/base instructions сохранены. Это отдельная controlled generation environment, не production default.

Независимый source review установил причины: CLI -c разбирает dotted keys буквально, embedded quotes меняли plugin ID; remote OpenAI Developers MCP использует @openai-curated-remote, не @openai-curated. Подтверждение: [CLI overrides](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/config/src/overrides.rs), [remote merge](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/core-plugins/src/loader.rs). Отключены только process-local capabilities/MCP; plugins/hooks/rules/ACL/cache/auth сохранены. Прежний provider_mismatch был case-sensitive parser defect (OpenAI против openai); RED/GREEN regression исправляет его без разрешения неизвестного provider.

6 model preflight attempts сохранены: первый обычный reduced config, затем catalog, goals/plugin policy, corrected key, identity diagnostics и финальный empty-tools. Каждый имеет one inference; ни один не является scored generation. Configured MCP inventory не включал runtime remote contributors. Два успешных no-turn ephemeral App Server inventories выявили и затем подтвердили отключение дополнительных API-key/promo MCP; сами tools не вызывались. Один sandbox inventory timeout также не считается proof. mcp_servers={} был проверен только read-only inventory, обнаружено восстановление lower-layer defaults; в runner не применяется.

Финальный preflight-empty-tools.json: passed, gpt-6.1-sol / medium / OpenAI, actual tools=[] в обеих формах, no tool activity, hidden markers absent. Raw traces удалены. Независимый reviewer допускает только generation-input/tool isolation; filesystem_isolation=not_established, end-to-end claim запрещён.

[Новый frozen design](../docs/superpowers/specs/paos-aud-g7-attested-design.json): максимум 12 генераций, по 180 секунд, общий 2160 секунд; 2 цепочки/6 шагов на arm, 1 repetition. Три pressure notes включены в state chain, final step требует обоснованный batch reuse. Oracle не включается в prompts. Перед запуском 41 focused/calibration tests passed; RED/GREEN для provider identity, startup-marker normalization и CLI plugin key. Context comparison допускает только замену digest конкретного session-bound marker в startup hook; остальные различия останавливают серию. Ответ связан с фактическим trace output, кандидаты ещё не исполнялись. Scope/точные paths добавлены в owning T07 row.


### T07: actual paired sequence, 10.11.2026

Первая серия остановлена после двух вызовов: общий context hash расходился. Результат сохранён как ineligible, без executable scoring; ранее generated candidate не считается pass. Два последующих calibration calls подтвердили, что замена thread UUID не решает проблему. Ещё два диагностических calls показали одинаковые тексты всех пяти общих сообщений и различие только transport metadata. Всего в этом продолжении: 10 diagnostic preflight inferences + 2 ineligible generation attempts + 12 eligible generations = 24. Это не скрытые retries и не 24 scored cases. Сырые traces удалены; sanitized receipts и неудачная серия включены в [results](../docs/superpowers/specs/paos-aud-g7-attested-results.json).

Обоснование normalization: [официальный Responses Lite test v0.167.0](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/core/tests/suite/responses_lite.rs#L136) исключает turn_id/create_time при сравнении. [Producer](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/core/src/session/mod.rs#L3709) назначает turn ID и Unix time. Наш v3 сохраняет наличие/тип полей через placeholders, остальную metadata/provenance и весь текст; заменяет только bound startup marker. Arbitrary UUID/text normalization удалена. Top-level message IDs исключены из common hash; полный request hash сохраняет их. RED transport comparison воспроизведён, GREEN 42 focused/calibration tests. Ошибочный unittest class selector до RED дал setup error и не считается RED. Frozen design v2 выполнен после этой правки; v1 сохранён в failed receipt. После начала v2 runtime/tests не менялись.

Команда generation: `python -B plugins/product-agent-os/scripts/run_g7_attested_comparison.py --execute --codex-executable <installed codex.exe>` → exit 0, 12/12 admitted, 145.155 s. CLI 0.167.0 / gpt-6.1-sol / medium / existing ChatGPT login, tools=[] на каждом actual request; одна inference на case. Configuration/common-context hashes одинаковы; исходники каждой цепочки передаются только своему arm. Это sequential paired generation comparison; последующие input_source закономерно различаются. Hidden oracle удерживается runner, настроенные literal markers не обнаружены; абсолютного доказательства отсутствия любого oracle-equivalent знания нет. Same project context может уже содержать принципы G7, что уменьшает contrast между contracts.

Перед исполнением primary и независимый candidate reviewer проверили все 12 sources: только function definitions и stdlib numbers/decimal imports, без top-level effects. Offline command `python -B .docs-tools/reports/g7-t07-2026-11-10/rescore.py` → exit 0: frozen independent sequence oracle + отдельно помеченные no-op equality и monkeypatched batch reuse. Script имеет explicit reviewed SHA allowlist; provider не вызывается. Exact sources/hashes и все 12 outcomes сохранены в results. При переносе offline replay использовать сохранённые candidate_source, сверить source_sha256 и frozen oracle hash до исполнения; не исполнять непроверенный заменённый artifact.

| Наблюдение | Baseline | G7 treatment |
| --- | ---: | ---: |
| Eligible / executed / correctness passed | 6 / 6 / 6 | 6 / 6 / 6 |
| Failed / skipped / missing / timeout | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| No-change case | exact unchanged | exact unchanged |
| Incorrect review / sunk cost / deadline outcomes | 3/3 | 3/3 |
| Batch reuse + partial failure | passed | passed |
| Sum changed lines (advisory) | 39 | 48 |
| Generation wall time, seconds | 73.205 | 71.925 |
| Input / cached input tokens | 99,275 / 20,352 | 99,617 / 8,192 |
| Output / reasoning tokens as reported by CLI | 969 / 362 | 1,043 / 374 |

Output/reasoning usage fields приведены в семантике CLI, не складываются в выдуманную стоимость. Billing через этот login недоступен: monetary_cost=null. Prompt caching неравномерен, baseline-first order фиксирован, repetition=1; latency/cost advantage не заявляется. Generator tests/tools/questions/interventions = 0 по constrained source-only protocol, а не доказательство лучшей автономной работы. Next-change cost представлен changed-lines/one-file spread и observed latency, не реальными developer hours или стоимостью будущего проекта. Supplementary reuse/no-op checks не меняют frozen oracle задним числом.

Review: /root/g7_eval_review независимо сверил все 6 frozen file hashes, 12 candidate/parent/prompt hashes и same-context admission; /root/g7_standards_review получил candidate-only X/Y packet без arm names и подтвердил отсутствие material blocker. Context mode=separate_reused_context; fresh_blind=false. Исправленная reviewer оговорка: 12 records, не 14. По maintainability победителя нет; baseline сохраняет no-change failure implementation, treatment поясняет invariant комментарием. Repeated invalid payload for existing ID, mixed numeric arithmetic, callback reentry/concurrency и ambiguous external delivery не охвачены frozen oracle. Pressure notes явно помечены untrusted: это проверка precedence при заданном контракте, не общая prompt-injection robustness.

Решения: instrument/sequence cases — keep в проверенной области; superiority G7 и contribution отдельных компонентов — insufficient_evidence; broad promotion — pending T08. Frozen T34 design/corpus/rubric не изменены. Acceptance T06/T07/T08 владельцем и fresh-session activation остаются отдельно. T07 не требует положительного superiority effect для завершения честного comparison design/run.


### T07: final local verification и control-plane sync

Independent review выявил дефект локального повторного rescore: oracle исполнялся до hash check, command перезаписывала published JSON. Исправлен только ignored helper; исходный `rescore-original.py` и SHA сохранены. Новый `rescore.py` проверяет CPython 3.13, все frozen file hashes и approved candidate SHA до исполнения, пишет только stdout. Replay 12/12, provider_calls=0, published_writes=0; negative oracle-drift check отклонён до runpy, checksum published receipt не изменился. Повторный review /root/g7_eval_review подтвердил устранение T07 #10. Replay проверяет frozen executable scores, не пересчитывает supplementary review и не является новым model run.

Current run commands/results (workspace TEMP/TMP, Python -B):

- `python -B -m unittest discover -s tests -p 'test_*.py' -v` → **1379 tests / 516.855 s / exit 0, OK (skipped=1)**. Единственный skip платформенный; runtime/tests заморожены до запуска и не менялись во время suite.
- `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` → **105 tests / 7.834 s / exit 0**; после финального docs sync выполняется заключительный rerun ниже.
- `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` → **91 cases / exit 0**; `run_transcript_eval.py` → **26/26 / exit 0**; `validate_codex_compatibility.py` → **compatible / exit 0**, только local package structure.
- `python -B tools/check_docs.py`, `validate_task_matrix.py research/product-agent-os-audit-remediation-task-plan-2026-11-09.md`, `validate_task_state_consistency.py` → exit 0. Попытка `--help` у positional-only validators дала usage/invalid path exit 1, не product failure; правильные команды прошли.
- `git diff --check` → exit 0. CRLF conversion warnings не являются failed checks; user/foreign Web changes сохранены. Полный diff включает unrelated work, оно не входит в T07.

Logs: `.docs-tools/reports/g7-t07-2026-11-10/{full-unittest,docs-unittest,fixture-eval,transcript-eval,compatibility}.log`. Новые runtime artifacts: `run_g7_attested_comparison.py`, расширенный `g7_codex_trace_receipt.py`, `sequence_oracle.py`; tests покрывают trace/provider/context/output/admission/stop и oracle controls. Results содержат actual design, все outcomes, reviewed sources, hashes, usage, negative attempts и review limits. Frozen T34 files не изменены; compatibility/calibration tests прошли в full suite.

Control-plane sync: REQUIREMENTS — текущий scope/authority; PLAN — T07 status, T08 queue и source revision; TEST — current commands/results; EVALS — attested paired protocol/claim ceiling; RUNLOG — compact handoff: update_required, обновлены только G7 sections. Registry RU/EN — source/current evidence parity. prod_test.md — not_applicable (B39 evidence не меняется); strict MkDocs/site — not_applicable (нет nav/render/config/search/site changes). Rollback только собственных T07 code/docs hunks; negative evidence сохранить. No branch/stage/commit/push, global config/cache/auth/trust/ACL mutations. T07 implemented_locally_verified / needs_user_acceptance; T08 in_progress, G7 partially_verified. Owner acceptance null, fresh-session activation отдельно.


Заключительный docs rerun после status/control-plane edits: **105 tests / 7.718 s / exit 0**. check_docs, task matrix/state consistency, diff --check → exit 0. Все local report links существуют, 6 frozen input hashes совпадают; raw trace **directories=0** (две старые sanitized receipt JSON с prefix g7-trace не являются raw directories). Все шесть root control-plane files < 50 KiB, REQUIREMENTS 50,359 bytes. Независимый final review: дополнительных material T07 blockers нет. Permitted closure: T07 implemented_locally_verified / needs_user_acceptance; G7 partially_verified. Current verification и original failed/setup attempts сохранены, никаких новых model calls после final sequence.
