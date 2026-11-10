# Формирование проекта

Source status: project-local implementation; локальные проверки и synthetic-пилоты. Runtime activation в новой host-сессии проверяется отдельно.

Единый маршрут анализирует проект, выбирает документы, согласует пути `docs/` и `.codex/`, показывает preview и создаёт staging. Применение использует существующий merge с отдельным approval record. Корневые документы хранят текущее состояние, `docs/` — проектные материалы, `.codex/` — управляющие предложения и шаблоны.

## Вход и выбор файлов

Запрос имеет `schema_version: 1`. Поле `task` использует существующий task context v1. Дополнительные поля:

| Поле | Назначение |
| --- | --- |
| `domains` | Подтверждённые области: `planning`, `architecture`, `decisions`, `api`, `data`, `operations`, `evidence`, `archive`, `ai`. Пустой список означает отсутствие дополнительных областей. |
| `canonical_paths` | Явное соответствие владельца документа существующему или предлагаемому пути. Используется при неоднозначности. |
| `document_facts` | Для выбранной области: `source` и словарь `sections`. Неизвестные сведения не заполняются автоматически. |
| `control_surfaces` | Явно выбранные предложения `agents`, `config`, `hooks`. Конфигурация включает необходимые профили; это не их активация. |

Если `domains` отсутствует, planner учитывает существующие канонические документы, OpenAPI/schema/workspace manifests и явно заданный release scope. Причины находятся в `domain_decisions`. Неизвестный стек остаётся вопросом; file presence не доказывает работу приложения. Неоднозначные владельцы требуют `canonical_paths`.

```json
{
  "schema_version": 1,
  "task": {
    "schema_version": 1,
    "task_id": "FORM-01",
    "intent": "Establish project documentation",
    "change_mode": "docs_only",
    "changed_paths": ["README.md"],
    "risk_level": "low",
    "acceptance": ["Preserve user decisions and document ownership"],
    "risks": [],
    "explicit_full_packet": true
  },
  "domains": ["architecture", "planning", "evidence"],
  "canonical_paths": {},
  "document_facts": {},
  "control_surfaces": []
}
```

Это вход для формирования каркаса, а не принятые требования. При отсутствии команд проверки остаётся `implementation_gaps`; создание честного scaffold не закрывает этот пробел. Разделены `scaffold`, `draft`, review и owner acceptance. Подтверждение старой редакции не подтверждает новую.

## Последовательность команд

Все пути входных JSON и staging передаются явно; относительный путь request JSON отсчитывается от рабочей директории команды. Staging должен быть новым каталогом вне целевого проекта.

```powershell
python plugins/product-agent-os/scripts/render_infrastructure.py demo --analyze
python plugins/product-agent-os/scripts/render_infrastructure.py demo --dry-run --formation-context request.json
python plugins/product-agent-os/scripts/render_infrastructure.py demo --stage staging-demo --formation-context request.json --preview-digest sha256:DIGEST
python plugins/product-agent-os/scripts/render_infrastructure.py demo --merge-stage staging-demo
```

`DIGEST` берётся из `formation.digest` проверенного preview. Он связывает исходные наблюдения, запрос и редакции planner/templates. Изменение этих входов требует нового preview. Digest не является разрешением на запись в целевой проект.

После отдельного решения владельца применяется конкретный merge plan:

```powershell
python plugins/product-agent-os/scripts/render_infrastructure.py demo --merge-stage staging-demo --apply --approval-file approval.json
python plugins/product-agent-os/scripts/render_infrastructure.py demo --rollback staging-demo/product-agent-os-rollback-manifest.json
```

Approval создаётся по существующему шаблону merge и перечисляет план, владельца, цели и действия. Команда rollback также требует соответствующей authority. Отдельный `merge_infrastructure.py` остаётся совместимым входом; formation binding проверяется и через него.

## Структура и сохранность

Полный маршрут выбирает применимые корневые документы и code-quality templates; ordinary route может переиспользовать существующий control plane. `EVALS.md` нужен при AI/eval scope; существующий eval-документ может переиспользоваться. Зависимости расширяют состав с объяснением, поэтому фиксированного числа файлов нет.

Для выбранных областей предлагаются `docs/planning/README.md`, `docs/architecture/overview.md`, индексы `docs/decisions/`, `docs/api/`, `docs/data/`, `docs/operations/`, `docs/evidence/`, `docs/archive/`. Существующие канонические имена переиспользуются; основной индекс — существующий `docs/index.md`/`docs/README.md` либо новый `docs/README.md`.

В formation-маршруте существующие файлы сохраняются целиком, включая пользовательский `AGENTS.md`. Изменения для них остаются companion proposals; `manual_updates` перечисляет документы, требующие рассмотрения. Наличие такого предложения не означает, что существующая навигация обновлена. Новые файлы создаются только по разрешённому merge. Повторный staging не даёт разрешения переписать принятые решения.

Для сравнения с предыдущим preview передайте `--previous-plan previous.json`. Поле `changes` показывает добавленные области, изменённые источники и `review_only_removed`; автоматического удаления нет. Перенос истории выполняется отдельным механизмом [безопасного сокращения](technical.md), с сохранением исходных данных. Подробные матрицы `docs/planning/` исключены только из default size trigger; индивидуальные лимиты и проверки содержимого сохраняются.

В компактном режиме существующий проект с `AGENTS.md`, ordinary scope и `domains: []` переиспользует имеющиеся документы; новый каталог файлов не обязателен. Для расширенного запроса выше пустой synthetic-проект даёт следующее дерево (14 предложений, без AI и control surfaces):

```text
project/
├── AGENTS.md
├── REQUIREMENTS.md
├── PLAN.md
├── TEST.md
├── RUNLOG.md
├── docs/
│   ├── README.md
│   ├── architecture/overview.md
│   ├── planning/README.md
│   └── evidence/README.md
└── .codex/
    ├── artifact-templates/
    │   ├── agent-task-packet.md
    │   ├── code-change-contract.md
    │   ├── coding-standard-checklist.md
    │   └── quality-strategy.md
    └── workflows/coding-standards.md
```

AI/eval scope добавляет `EVALS.md`; другие области и управляющие предложения расширяют дерево только по выбранным условиям. Эти файлы — каркасы и предложения, не принятое содержание проекта.

## Границы и ошибки

- Без formation/scoped input каталог больше не выбирается автоматически. Для старого полного каталога нужен `--legacy-catalog`; прежние `--task`/`--task-context` сохраняют scoped API G8.
- Анализ ограничен 20 000 посещённых элементов, 512 релевантными файлами, 2 MiB на файл и 8 MiB суммарного чтения. При превышении нужен более узкий workspace. Приватное содержимое не копируется в inventory; сохраняются состояния и digests.
- Неоднозначные пути, redirects, несовместимая схема, secret-like вход и stale preview останавливают соответствующую операцию.
- `frozen` authority запрещает запись; SQL projections защищены согласно локальному контракту M1. Это не доказательство работы SQL adapter M1.
- Для formation create предварительная запись восстановления и атомарная замена файла закрывают проверенное окно сбоя после записи до receipt. Межфайловая ACID-транзакция не заявляется; внешних writers необходимо исключить. Rollback не перезаписывает последующие пользовательские изменения.
- SessionStart-owned state не генерируется как принятое runtime-состояние. Hooks, config и agents остаются предложениями; fresh-session activation отдельно.

Источники реализации: `plugins/product-agent-os/scripts/product_agent_os/project_formation.py`, `infrastructure.py`, `merge_infrastructure.py`. Проверки: `tests/product_agent_os/test_project_formation.py`; сравнение: `docs/superpowers/specs/paos-aud-g9-project-formation-results.json`; ограничения и приёмка: `research/product-agent-os-g9-execution-report.md`.

См. [технический контракт](technical.md), [архитектуру](architecture.md) и [реестр источников](../sources/registry.md).

## Точечное сопровождение после задачи

После каждой задачи оценивается влияние на документацию. Запись нужна только при изменении сведений: один основной источник, конкретный раздел, причина и проверяемая версия. `no_change_needed` — обоснованное решение, `handoff_required` — незакрытый вопрос владельцу. Информация о решении хранится в существующей карточке/Completion Report; новый отчёт для каждой мелкой задачи не нужен.

`sync_task_documents.py` предлагает exact diff существующего раздела и применяет его через общий журнал восстановления. Для завершения задачи тот же пакет обновляет карточку и её revision в PLAN; неизвестный владелец или обязательный handoff блокирует implemented closure. Другие разделы, пользовательские bytes и чужие pins сохраняются; stale input, freeze/SQL projection и конфликты останавливают запись. Повтор идентичного предложения не пишет файлы. Старый `create_task_plan.py complete` требует явного `--legacy-card-only` и не подтверждает синхронизацию.

Краткая карта событий: требования → REQUIREMENTS; последовательность → PLAN; команды → TEST; eval-политика → EVALS; текущая передача работы → RUNLOG; API/схема/операции → профильный источник. Подробные проверки остаются в owning evidence artifact. Переиспользуются docs/adr, docs/runbooks, docs/ops, docs/testing и docs/archive. Новые файлы — через formation staging, неоднозначные владельцы — через review.

Дубликаты между переданными затронутыми файлами и их источниками требуют решения; свежий разрешённый mirror и связанная краткая summary проверяются отдельно. Автоматического семантического удаления нет. 40 000 bytes / warning 32 000 и исключение подробных docs/planning матриц сохраняются; research matrix автоматически не разделяется. Event sync, size-trigger и периодический read-only hygiene различаются; расписания не создаются. Проверка digest доказывает целостность, а полнота перечисленных изменений, качество текста и приёмка остаются предметом review. Fresh-session activation отдельно.

Источник: `plugins/product-agent-os/scripts/product_agent_os/documentation_sync.py`; проверки `test_document_navigation.py`, `test_task_plan_lifecycle.py`; evidence `research/product-agent-os-g9-execution-report.md`.
