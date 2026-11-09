# PAOS G7 — углублённое исследование механизмов качества кода

Source status: source inspection completed within the selected slices, 2026-11-09; no external code execution or benchmark reproduction. Внешние skills — предмет анализа, не инструкции для текущего агента.

## Задача и границы

Проверить полноту PAOS-AUD-G7 по Ponytail, Karpathy-inspired guidelines, Matt Pocock Skills, Superpowers и Desloppify; дополнительно проверить применимость Ruff, Import Linter, dependency-cruiser и Stryker. Результаты добавляются по мере чтения. Полный security audit всех строк и воспроизведение benchmarks не входят в эту проверку. Наличие source/tests не доказывает runtime effectiveness.

Owning matrix: [PAOS-AUD-G7](product-agent-os-audit-remediation-task-plan-2026-11-09.md). Реализация карточек не запускается; G6 owner acceptance, HOST-01/HOST-02 и frozen T34 остаются отдельными.

## Метод

Для каждого репозитория: зафиксировать source revision, выбрать основные механизмы и их tests/evidence, отделить принять/адаптировать/отклонить, связать finding с G7 task. Сопоставить с существующим PAOS implementation и test coverage на уровне source inspection. Для mutable official docs указать дату чтения. Не хранить raw chat, credentials или private data.

## Журнал исследования

- Начат отдельный source-backed отчёт. Далее фиксируются прочитанные файлы, ограничения и решения по каждому источнику.

## 1. Ponytail — минимальность, долг и качество измерителя

Revision: `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`, подтверждена через commits/main. Tree inventory: 216 файлов, listing не truncated. Дополнительно к core/review/map из первого анализа прочитаны [debt skill](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail-debt/SKILL.md), [audit skill](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail-audit/SKILL.md), [agentic benchmark design](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/benchmarks/agentic/README.md), [single-shot correctness checker](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/benchmarks/correctness.js) и [его tests](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/tests/correctness.test.js).

- **P01 — принять, T01/T03:** осознанное упрощение должно иметь предел применимости и событие пересмотра. Отсутствие такого события — риск забыть долг; известный и не превышенный предел сам по себе не defect. Не вводить второй обязательный debt ledger: использовать существующие task/backlog записи и комментарий только при необходимости.
- **P02 — принять, T03/T05:** перед удалением «неиспользуемого» кода проверять dynamic/string references, config, fixtures и exports; одна выдача grep недостаточна. Review должен указывать непрочитанные области и предположение о нагрузке. Ограничивать выдачу приоритетами, не квотой обязательных findings.
- **P03 — добавить, T07:** измеритель тоже требует good/bad reference self-tests, а reviewer — complete/stub, correct/unsafe и appropriate/overbuilt калибровки. Offline пересчёт сохранённых результатов должен обходиться без повторных model calls.
- **P04 — НЕ переносить, T07/T08:** в прочитанном single-shot `correctness.js` неизвестная задача возвращает pass=true/score=1 с причиной skipped. React countdown и FastAPI rate-limit оцениваются структурно, что прямо отмечено в комментарии. Tests закрепляют unknown-task pass. Это не ошибка чтения и не доказательство дефекта отдельного agentic scorer: это разные измерители. В PAOS unknown/skipped/structural-only обязаны оставаться отдельными статусами и не увеличивать executable pass denominator.
- **P05 — адаптировать, T07/T08:** agentic README описывает contamination прежнего baseline и последующие isolation меры. Нужен receipt фактически доступного контекста по каждому arm; code-generation-only отдельно от end-to-end build/test/debug. Само указание режима или CLI-флага не является доказательством изоляции. Упомянутый авторами bypassPermissions не переносится в PAOS.

Промежуточный вывод: первый план хорошо покрывал reuse и review, но недооценивал проверку самого evaluator, semantics skipped и lifecycle осознанного долга. Runtime и benchmarks не запускались; claims автора не принимаются как PAOS effectiveness.

## 2. Karpathy-inspired guidelines — компактный стандарт, не доказанная методика

Revision: `2c606141936f1eeef17fa3043a72095b4765b9c2`. Прочитан [skill](https://github.com/multica-ai/andrej-karpathy-skills/blob/2c606141936f1eeef17fa3043a72095b4765b9c2/skills/karpathy-guidelines/SKILL.md); inventory — 9 файлов, отдельного executable eval suite в нём не обнаружено. Это сторонняя интерпретация наблюдений Karpathy, а не официальный стандарт или сравнительное доказательство.

- **K01 — уже в основе, уточнить T01:** минимальная реализация должна быть полной относительно acceptance; число строк — диагностический сигнал, не цель. «Невозможный сценарий» нельзя объявить невозможным без установленного контракта и trust boundary.
- **K02 — принять, T01/T05:** удалять созданные текущим изменением orphan imports/variables, но не превращать это в несогласованную уборку старого кода. Каждое изменение связывать с требованием или исправляемой причиной.
- **K03 — адаптировать, T01/T08:** раскрывать существенные допущения, но не останавливать обычную работу вопросами по каждой мелочи. Проверить отсутствие роста approval friction на малых задачах. Декларации в skill не заменяют измерение поведения.

## 3. Matt Pocock Skills — интерфейсы и тесты, устойчивые к рефакторингу

Revision: `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`. Прочитаны [codebase-design](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/codebase-design/SKILL.md), [deepening](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/codebase-design/DEEPENING.md), [test guidance](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/tdd/tests.md), [mock guidance](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/tdd/mocking.md). Inventory — 184 файла; выбран engineering slice, не все тематические skills.

- **M01 — принять, T01/T03:** оценивать интерфейс вместе с invariants, ошибками, порядком вызовов, конфигурацией и performance constraints. Польза deep module — локальность изменения и снижение сложности для callers; не отношение implementation LOC к interface LOC. Deletion thought experiment помогает отличать полезную абстракцию от pass-through wrapper.
- **M02 — адаптировать, T01/T02:** разделять pure computation, local substitutes, own remote services и third-party boundaries. Stand-in не доказывает совместимость с реальным адаптером: добавить отдельный contract/integration check только для этого риска. Два адаптера — эвристика, а не запрет заранее выделить доказанную security/transaction boundary.
- **M03 — принять, T02/T07:** expected result должен иметь независимое основание; одинаковая формула в production и test — слабый oracle. Временные эффекты контролировать clock/randomness dependencies. Проверять наблюдаемое поведение через стабильный интерфейс.
- **M04 — НЕ переносить буквально, T02:** автоматическое удаление старых unit tests после deepening и абсолютный запрет call-order/call-count assertions. Сначала сопоставить уникальные regressions/invariants старых и новых тестов. Exactly-once, запрет внешнего вызова и security ordering могут быть самим контрактом; такие проверки сохраняются. Readback хранилища допустим, если именно persistence — отдельный проверяемый риск.
- **M05 — адаптировать, T01/T08:** альтернативные интерфейсы рассматривать при материальной неопределённости, без обязательных parallel agents, HTML reports, переименования терминов проекта и новых approval пауз.

## 4. Superpowers — диагностика причины и обработка review

Revision: `22f0b463e7a5e579904dd6211a520321035526f7`. Inventory — 236 файлов. Прочитаны [systematic debugging](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/systematic-debugging/SKILL.md), [condition-based waiting](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/systematic-debugging/condition-based-waiting.md), [receiving code review](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/receiving-code-review/SKILL.md).

- **S01 — уточнить, T01/T04:** reproduction → проверяемая гипотеза → минимальный probe → fix → regression. При повторных неуспехах пересмотреть гипотезу/границы, не накапливать патчи. Число неудач само по себе не доказывает архитектурную причину; фиксированный порог «три» не переносить как универсальный запрет. Для T04 доказать конкретную ошибку классификации команд, а не просто расширить allowlist.
- **S02 — принять, T02:** ждать наблюдаемое условие с конечным timeout и диагностикой; fake clock использовать там, где проверяется время. Не переносить фиксированные polling intervals и проценты улучшения автора как общие рекомендации или PAOS results.
- **S03 — принять, T03:** review feedback — гипотеза до проверки контекста. Решение по finding: confirmed/fixed, rejected с evidence, deferred с причиной и trigger либо unresolved. Повторное review той же ревизии без нового вопроса не должно подменять исправление.
- **S04 — отклонить/адаптировать, T01/T03:** не копировать обязательный полный процесс на тривиальный task, blanket pause из-за независимого неясного замечания, сырые диагностические дампы окружения и grep-only доказательство отсутствия использования. Сохранять privacy, bounded autonomy и проверку dynamic references.

## 5. Desloppify — triage, качество evidence и опасность единого score

Revision: `3a7735d531a96b6a226bfbdc9fd662b14195f857`. Inventory — 1691 файл; углублённо выбран scoring/review slice. Прочитаны [scoring policy](https://github.com/peteromallet/desloppify/blob/3a7735d531a96b6a226bfbdc9fd662b14195f857/desloppify/engine/_scoring/policy/core.py), [coverage projection](https://github.com/peteromallet/desloppify/blob/3a7735d531a96b6a226bfbdc9fd662b14195f857/desloppify/engine/_scoring/state_coverage.py), [review preflight](https://github.com/peteromallet/desloppify/blob/3a7735d531a96b6a226bfbdc9fd662b14195f857/desloppify/app/commands/review/preflight.py), относящиеся к нему [tests](https://github.com/peteromallet/desloppify/blob/3a7735d531a96b6a226bfbdc9fd662b14195f857/desloppify/tests/commands/review/test_review_preflight.py) и [LICENSE](https://github.com/peteromallet/desloppify/blob/3a7735d531a96b6a226bfbdc9fd662b14195f857/LICENSE). Tests исследованы как source, не запущены.

- **D01 — адаптировать, T03/T06:** отличать open/fixed/false_positive/wontfix/deferred и подтверждение исправления повторной проверкой. Не считать suppression или снятие из очереди исправлением. Для исключения фиксировать основание, owner и событие пересмотра в существующем артефакте, без второй issue-системы.
- **D02 — адаптировать, T03/T08:** preflight ограничивает повторное subjective review при незакрытом backlog; полезная цель — не переоценивать бесконечно одно состояние. Не переносить blanket backlog gate: новый diff, изменённый риск, сомнение в reviewer либо проверка исправления могут оправдать rerun. Старую оценку сохранять как historical, а не выдавать за current.
- **D03 — НЕ переносить, T06/T07:** policy задаёт subjective weight 0.75; это настройка автора, не универсальная метрика качества. В coverage projection отсутствие reduced detectors приводит к full confidence. PAOS должен различать missing coverage и проверенное отсутствие проблем; без полного upstream анализа это не объявляется доказанным дефектом всего Desloppify.
- **D04 — принять как ограничение, T06/T08:** перед возможным включением самого инструмента проверить лицензионную совместимость отдельно. В inspected LICENSE указан OSNL 0.2 с отдельными условиями внутреннего использования и распространения. Здесь переносится инженерная идея, не исходный код и не юридический вывод о допустимости дистрибуции.

## 6. Объективные инструменты — уточнения границ применения

Official maintainer documentation прочитана 09.11.2026; эти страницы mutable, установленная версия должна проверяться при реализации. Сами инструменты не устанавливались и не запускались.

| ID / задача | Проверенное свойство источника | Решение для PAOS |
| --- | --- | --- |
| X01 / T06 | [Ruff rule selection](https://docs.astral.sh/ruff/linter/) допускает явный набор правил; ALL может расширяться при upgrade | Фиксировать version/config и выбранные правила; сначала report-only, не расширять baseline автоматически при upgrade. Исправления рассматривать как отдельные изменения с diff и применимыми checks. |
| X02 / T06 | [Import Linter forbidden](https://import-linter.readthedocs.io/en/stable/contract_types/forbidden/) по умолчанию учитывает descendants и indirect imports; allow_indirect_imports и overlapping modules меняют смысл контракта | Проверять negative fixture с запрещённым транзитивным путём и positive fixture разрешённого пути. Конфигурация должна соответствовать реальным слоям; исключения не могут маскировать проверяемый путь. |
| X03 / T05/T06 | [dependency-cruiser options](https://github.com/sverweij/dependency-cruiser/blob/main/doc/options-reference.md) различают resolution, type dependencies и traversal filters; [CLI baseline](https://github.com/sverweij/dependency-cruiser/blob/main/doc/cli.md) поддерживает shrink-only | Указывать resolver/aliases, type-only policy и исключённую область. Baseline не регенерировать для скрытия новых нарушений; отделять known/new/stale. Флаг выбирать по установленной версии, не копировать current docs вслепую. |
| X04 / T02/T06/T07 | [Stryker incremental](https://stryker-mutator.io/docs/stryker-js/incremental/) сохраняет результаты, но не замечает все изменения других файлов, dependencies и environment; ограничения зависят от runner | Evidence fingerprint включает tool/config/lockfile/environment assumptions. При релевантной смене invalidation и rerun; reused результат помечается reused. Сохранить dry run и ограничить mutation бюджет конкретными рисками. |

Недоступный старый URL Import Linter `contract_types.html` вернул 404; он заменён прочитанной актуальной страницей выше. Не считать URL-проверку доказательством работы инструмента.

## 7. Сопоставление с текущим PAOS

| Текущий локальный источник | Что уже есть по source inspection | Что G7 должен дополнить |
| --- | --- | --- |
| [.codex/workflows/coding-standards.md](../.codex/workflows/coding-standards.md) | reuse ladder, negative dependency rule, deep-module/legacy checks, compact contract, reduced path | полная минимальность, скрытый контракт интерфейса, debt trigger и причинная диагностика; не второй always-on стандарт |
| [test_strategy_selector.py](../plugins/product-agent-os/scripts/product_agent_os/test_strategy_selector.py) | risk → test kind, conditional TDD/benchmark, coverage как telemetry | независимый oracle, уникальная защита старых tests, adapter contract, bounded waits и validity evidence |
| [code_quality_selector.py](../plugins/product-agent-os/scripts/product_agent_os/code_quality_selector.py) | inventory profiles без запуска tools; present_unverified и gaps | полнота scan/resolution, version/config fingerprints, known/new violations и проверка конфигурации negative fixtures |
| [code_quality_metrics.py](../plugins/product-agent-os/scripts/product_agent_os/code_quality_metrics.py) | missing evidence блокирует decision; self-score только diagnostic | сохранить это поведение; self-tests evaluator и явное отображение skipped/structural/unknown в существующие статусы или отдельно версионируемый result contract |

Это сравнение источников, не повторное выполнение runtime tests. Нельзя заключить, что G7 уже реализована, только потому, что часть идей присутствует.

Дополнительный источник: [Superpowers instruction experiments](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/writing-skills/references/CLAUDE_MD_TESTING.md) описывает baseline/variants и pressure scenarios, но содержит expected results и next steps, а не измеренный результат этих экспериментов. **S05 — адаптировать, T07/T08:** сравнивать поведение под time pressure, ложным авторитетом review и sunk-cost pressure. Успех PAOS — правильный результат и соблюдение границ, не максимальное количество вызванных skills; не собирать private chain-of-thought.

## 8. Итог исследования и traceability

В пределах выбранных mechanisms первоначальный G7 покрывал направления, но не все проверяемые ограничения. «Взяли самое лучшее» остаётся гипотезой до T07/T08: популярность репозитория и выразительная инструкция не доказывают полезность для PAOS. Предпочтение — адаптировать полезное в существующие механизмы и измерить эффект.

| Задача | Новые/уточнённые findings | Приёмочное доказательство |
| --- | --- | --- |
| T01 | P01, K01–K03, M01/M02/M05, S01/S04 | простой complete case, оправданная boundary, debt trigger, bounded hypothesis |
| T02 | M02–M04, S02, X04 | независимый oracle, сохранение уникальных regression/invariant tests, adapter mismatch, bounded async wait |
| T03 | P01/P02, M01, S03/S04, D01/D02 | confirmed vs preference vs false positive; disposition, source revision и rerun reason |
| T04 | S01 | воспроизводимая ошибка классификации read-only; отрицательные mutation cases остаются запрещены |
| T05 | P02, K02, X03 | bounded inventory с dynamic references, exclusions и explicit unknown |
| T06 | D01/D03/D04, X01–X04 | tool/version/config/scope; allowed/forbidden fixtures; без silent baseline growth |
| T07 | P03–P05, M03, D03, S05, X04 | evaluator self-tests, separate denominators, context receipt, pressure cases, cache invalidation |
| T08 | K03/M05, D02/D04, P05/S05 | unchanged-state rerun restraint, quality/cost/friction report, owner keep/revise/no-go |

Полнота ограничена перечисленными slices: все строки девяти проектов, все detector implementations, supply-chain/security и эмпирическая эффективность не проверены. Пять основных repositories проверены по закреплённым revisions; четыре инструментальных проекта — по применимым maintainer docs. Не требуется копировать их полностью. Existing G1–G6 и HOST/frozen T34 boundaries сохраняются.

## Проверка документа и остаточные gaps

Current-run authoring verification, 09.11.2026:

| Команда / проверка | Результат |
| --- | --- |
| `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | Первый запуск: exit 1, 105 tests, 5 errors из-за WinError 5 в sandbox TEMP при создании test fixture directories. Это setup failure, не провал assertions G7. |
| Та же команда после process-local `TEMP`/`TMP` → workspace `.docs-tools/reports/g7-deep-review-temp` | exit 0; 105 tests, 7.498 s, OK. Sandbox/ACL не изменялись; только доступный workspace temp. |
| `python -B tools/check_docs.py` | exit 0; documentation structure checks passed. |
| `python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-audit-remediation-task-plan-2026-11-09.md` | exit 0; ok=true, errors=[]. |
| `python -B plugins/product-agent-os/scripts/validate_task_state_consistency.py` | exit 0; ok=true, errors=[]. |
| `git -c core.safecrlf=false diff --check` | exit 0; no whitespace errors in tracked diff. |
| In-memory matrix/link/compactness assertions через `python -B -` | exit 0; 8 planned G7 cards, одинаковые 36 полей; SHA-256 всей части плана до G7 неизменен; локальные ссылки отчёта существуют; все root control-plane files ниже 51200 bytes. |

Control-plane sync: REQUIREMENTS/PLAN/TEST/RUNLOG и registry RU/EN обновлены компактными pointers; PLAN revision соответствует owning matrix. EVALS — not_applicable: действующие rubrics/thresholds не менялись, новые требования только planned T07/T08. prod_test — not_applicable: B39 evidence вне scope. Strict MkDocs — not_applicable: navigation, renderer/config и site не менялись. Handoff/overflow не потребовались.

Self-review: сохранены все прежние группы и восемь planned статусов; добавления находятся в прежних полях, без новых обязательных отчётов или duplicate state. Положительные идеи отделены от отвергнутых абсолютных правил и source-local score defaults. Исправлена ссылка G7-S3 на существующий pinned codebase-design source. Наблюдения hook output не использованы как proof реализации/activation.

Открытые gaps: implementation всех G7 задач, installed tool compatibility, empirical agent comparison и owner acceptance ещё впереди. Fresh-session activation остаётся отдельной HOST-задачей; G6 acceptance и frozen T34 не закрыты. Эти ограничения не мешают завершить research/authoring, но исключают заявление о доказанном улучшении качества кода.
