# План B1 — проверка совета в CLI

Source status: project-local implementation and synthetic verification evidence.

## Владельцы и совместимость PMETH-01 {#pmeth-01-ownership-and-compatibility-inventory}

Исходная ревизия `01d8e43d806774bb1ea36510999bb446e1357688`. В проверках используются синтетические проекты.

| Граница | Владелец, вход и решение B1 | Проверки |
| --- | --- | --- |
| CLI и задача | `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py` принимает проект и JSON v1 или поля задачи. `plugins/product-agent-os/scripts/product_agent_os/task_routing.py` валидирует ввод и маршрутизирует проверку с опорой на исходники. `codex_runtime_runner/routes.py` использует существующий маршрут. B1 расширяет нормализацию и вывод совета. | `test_codex_runtime_runner_cli`, `test_render_infrastructure_cli`, `test_pmeth_b1` |
| Инвентаризация | `plugins/product-agent-os/scripts/product_agent_os/discovery.py` перечисляет пути и определяет стек и сигналы. Профиль B1 использует этот список. | `test_discovery`, `test_pmeth_b1` |
| Аудит и сводка | `product_agent_os/methodology_audit.py` определяет 12 доменов. `product_agent_os/methodology_synthesis.py` группирует рекомендации. `plugins/product-agent-os/scripts/run_methodology_audit.py` выводит JSON или отчёт по проекту. | `test_methodology_audit`, `test_methodology_catalog`, `test_methodology_synthesis`, `test_methodology_report` |
| Project Analysis | `apps/local-service/src/http/application.mts` обслуживает наблюдаемый анализ по ревизии. `apps/local-service/src/project-analysis/service.mts` передаёт собственную ограниченную проекцию в `apps/local-service/src/project-analysis/bridge.py`. Мост возвращает стек, контрольные документы и компоненты. `apps/web/src/features/projects/ProjectAnalysis.tsx` показывает источники с переходом к файлам. Teams & Tasks получает задачи и команду по своим endpoint; PMETH-19 связывает запрос совета с ними. | `tests/web/project-analysis-api.test.mts`, `tests/web/team-run-navigation.test.mts` |
| Предложение и запись | `product_agent_os/infrastructure.py` владеет отдельным маршрутом staged proposal. F13/G9 владеют разрешённым применением. B1 выводит требования и следующий шаг в stdout. PMETH-16 отвечает за подготовку, review и apply. | `test_render_infrastructure_cli`, проверки F13/G9 |

`_relative_files` в discovery пропускает каталоги по имени, в том числе `.venv`, `build`, `site` и `dist`. Из `dist` отдельно собираются некоторые признаки поставки. `_route_source_files` исключает сгенерированный анализ из признаков маршрутизации. `_relative_inventory` в аудите исключает `.git`, `node_modules`, `__pycache__` и заданные префиксы. Тест подтверждает, что `.venv/pyproject.toml` есть в обходе аудита и отсутствует в discovery. Отдельный CLI аудита не задаёт префикс, вызов из discovery исключает сгенерированный first-run анализ.

Обнаружение пути, наблюдаемая проекция файлов, предложение действия и факт выполнения имеют отдельные контракты. Маршрут B1 переиспользует существующие селекторы качества и тестирования. JSON, Markdown, 12 доменов, статусы готовности и потребители first-run/status продолжают использовать свои контракты.

Проверка совместимости выявила дублирование в renderer. Из-за старого списка событий он выдавал `missing hook event: PostToolUse`, тогда как действующий шаблон оставляет это событие необязательным. Первый fixture eval завершился с exit 1 и 0/91, а два renderer-теста отказались валидировать шаблон. `product_agent_os/infrastructure.py` теперь вызывает общий валидатор `validate_hook_json_text`, который проверяет обязательные события и структуру дополнительного события при его наличии. Повторный fixture eval дал 91/91, целевой Python-набор — 130/130.

## Baseline и матрица PMETH-22 {#pmeth-22-baseline-and-acceptance-matrix}

До добавления правил выбора снят baseline после нормализации. Источник сценариев — `tests/fixtures/product_agent_os/pmeth-b1-synthetic.json`. Сохранённые хеши исходников и проектных файлов, exit codes и вывод — `tests/fixtures/product_agent_os/pmeth-b1-baseline.json`. Оба прежних маршрута были компактными. Для docs-only выводился общий backend-тест из `TEST.md` без ссылки на источник. Аудит вернул 12 доменов. До нормализации падали обе проверки конфликтующего и эквивалентного intent, после неё конфликт отклоняется с exit 2.

| Сценарий | Ожидаемое поведение | Владелец |
| --- | --- | --- |
| Backend-ошибка | Именованный тест первым шагом, источник и файл теста подтверждены. Правильный RED требует `AssertionError: 5 != 4`, тот же assertion проходит после минимальной правки. | B1, CLI и Python unittest |
| Docs-only | Проверить `counter.py` как источник правила в руководстве. Общая инструкция проекта остаётся в прежнем пакете. | B1, CLI |
| Негативы B1 | Конфликтующий, смешанный, неполный ввод и запись отклоняются. Недостающий тест и устаревшее доказательство видны как пробелы. Пакет с чужой задачей, проектом, ревизией или битой ссылкой отклоняется. | B1, Python и TypeScript |
| Локальная правка UI, связанный legacy UX, несколько frontend features | Собрать baseline для каждого профиля. Проверить journey, рендеринг, владельца и связанные зависимости. | PMETH-08–11 |
| Native, AI/RAG | Перед квалификацией профиля нужны собственный baseline, проверка окружения или версии eval и критерии. | Профильные сценарии PMETH-23 |
| Дополнительные негативы | Ложные сигналы в путях, неизвестный alias, устаревшая спецификация, поддельный успех, prompt injection, dirty files, запрещённая запись и недоступный инструмент. Правила соответствующей ветки проверяются до её включения. | PMETH-10/11, 16/17, 21/23–26 |

Порог B1 — совпадение точного шага и источника, прохождение применимых негативов, сохранение целевых файлов и отсутствие ложного исполнения. Владелец PMETH-24 фиксирует размер выборки, порог верного самостоятельного выбора, время до первого проверяемого шага, лишние шаги и отмену рекомендации до actual-agent пилота.

## Контракт и CLI B1 {#b1-cli-and-contract}

Используйте `python -B plugins/product-agent-os/scripts/run_codex_runtime_runner.py <workspace> --contract --task-context <workspace-relative-json>`. Эквивалентный Python API — `codex_runtime_runner.cli.run_contract(..., task_context=...)`. Для простых задач доступны `--task`, `--change-mode`, `--changed-path`, `--acceptance`, `--risk-level`. Для проверок, инвариантов и путей источников используется JSON задачи. Эквивалентный `intent_hint` допустим; конфликт, смешанный и неполный ввод возвращают exit 2. Для задачи вывод идёт в stdout. В прежнем режиме анализа проекта остаётся опция `--output`.

Рекомендация находится в `route_packet.methodology_decision`. Владелец v1 — `plugins/product-agent-os/scripts/product_agent_os/methodology_contract.py`. Адаптер `packages/contracts/methodology-decision.ts` требует проверяемый scope. Идентификатор проекта вычисляется по каноническому локальному корню. Ревизия источников связывает инвентарь и содержимое файлов в области задачи. Ревизия задачи связывает нормализованный ввод без присланных результатов исполнения.

| Данные | Семантика |
| --- | --- |
| `facts`, `evidence` | Факты, происхождение и хеши источников. |
| `decisions`, `requirements`, `plan` | Пять объяснимых решений, предложение требований и проверка по каждому критерию или явный пробел. При нехватке данных выдаётся один блокирующий вопрос. |
| `execution`, `acceptance`, `authority` | `not_started`, `not_evaluated`, `read_only`. Результат исполнения и приёмка требуют своих доказательств. |

Backend-сценарий выдаёт `run_regression` с именованным unittest, источником команды и файлом теста. Docs-only выдаёт `check_source` с `counter.py`. Refactor получает characterization, конфигурация — проверку источника, явно заданный eval — ссылку на рубрику. Для недоступной проверки или критерия без связи остаётся пробел.

## Результат RED/GREEN {#observed-tdd-receipt}

Команда `python -B -m unittest test_counter.CounterTest.test_increment_by_one` выполнена на синтетических копиях, Python 3.13.5.

| Шаг | Ревизия fixture | Наблюдение |
| --- | --- | --- |
| RED | `4f8db147541e5e342cc5ad7ed0952d013b19f94e8f79165a47872c513e99dfa7` | Exit 1, `AssertionError: 5 != 4` у названного теста. |
| GREEN | `d0cade800c8abf9d5c556305fad54f1f7ecf2b4a5974927b2e29fb9297db9177` | Exit 0, `OK` после замены `+ 2` на `+ 1` в `counter.py`. |
| Ошибка подготовки | `6c2a4918627f3c95924a8bd10d77766a775b889bb2043b38383bfbc1b957c499` | Exit 1, `ModuleNotFoundError: No module named 'counter'`. Сохранена отдельно от RED. |

SHA-256 теста `ad7057f56ef3dc92f74e548c968d59cede253a212e25d2fd0d1f6763734c233e` совпал во всех запусках. Каждый запуск сохранил байты fixture. GREEN изменил только одну строку реализации, дополнительный refactor не потребовался.

## Передача B2 {#b2-handoff}

PAOS-PMETH-19 передаёт текущие идентификаторы и ревизии из существующего API и проверяет границу доступа. PAOS-PMETH-20 выводит совет в задаче. PAOS-PMETH-26 публикует примеры RU/EN после проверки паритета. В B1 проверены локальный CLI, Python и TypeScript; отображение в Web и оценка полезности для реальных агентов принадлежат последующим этапам.

## Прогоны B1 {#verification-runs}

Кандидат проверен на рабочем дереве от `01d8e43d806774bb1ea36510999bb446e1357688`. SHA-256 отсортированных пар «путь и SHA-256 файла» для 15 изменённых исходников и тестовых входов — `62c61532f2e23efa271a612334e2b5bbd912b6b6a6063a38a34a2835aec3c17a`. Проверка плана подтвердила 7 выполненных задач B1, прежнее содержимое 19 карточек и все 31 ребро зависимостей. JSON-зеркала побайтово совпали.

Целевой Python-набор — 130/130, fixture eval — 91/91, transcript eval — 26/26, Python→TypeScript и регрессия Project Analysis — 2/2. Проверка типов, локальная совместимость, RU/EN матрицы и сборка MkDocs прошли. Первый строгий MkDocs завершился предупреждениями о ссылках на файлы вне каталога документации и отсутствующей EN-странице. В публикации пути к исходникам указаны текстом, а языки имеют свои страницы доказательств.

`python -B -m unittest discover -s tests -p 'test_*.py' -q` с process-local `TEMP` и `TMP` прошёл, exit 0. Выполнено 1386 тестов, один пропущен, время 599.363 с. В первом прогоне до исправления renderer было 26 ошибок проверок, в том числе расхождение регистра пути временного каталога Windows. Повторный прогон использовал исправленный валидатор и отдельный рабочий временный каталог.
