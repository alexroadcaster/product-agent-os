# Inventory и границы сканирования

Source status: repository_source / focused_synthetic_verification; 15.11.2026.

Владелец: graph-cockpit-engineer + docs-maintainer. Область: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении scanner, API, adapters, query contracts, тестов или статуса PoC. Результаты графа — производное evidence для навигации, не замена чтению исходников и проверкам.

## Общий Web inventory — FUNC-28

Нижний модуль `apps/local-service/src/project-inventory/service.mts` и контракт `packages/contracts/project-inventory.ts` разделяют metadata, право чтения и право индексирования. `createProjectInventory({policy, limits})` предоставляет `assertProject`, `inspect`, `listDirectory`, `snapshot` и `read`. Directory listing не зависит от graph и не читает байты всех исходников; вложенный или пустой каталог, конфигурация, бинарный либо неизвестный файл доступны как metadata в пределах root policy. `inspect(project, path)` проверяет конкретный путь без перечисления всей папки.

Каждая запись содержит normalized `relativePath`, имя, вид, размер, modifiedAt, revision и `access` с eligibility/reason. `readable` и `indexable` внутри `access` обозначают разрешённую попытку, а не уже успешное чтение или анализ. `counts.discovered`, `files`, `directories`, `readEligible`, `indexEligible`, `unsupported`, `excluded` и `error` описывают разные, иногда пересекающиеся стадии. `counts.readable` и `counts.indexed` остаются `null` до фактической работы consumer; их нельзя складывать как независимые количества файлов. Пустая завершённая выборка отличается от partial/error и от неизвестной стадии анализа.

### Policy, ignore и revisions

Приоритет: hard sensitive/link/root denial → project `exclude` → project `include` → `.gitignore` и default generated/vendor exclusions. Include не разрешает чтение `.env`, credential/key/cloud-файлов, `.npmrc`/`.pypirc`/`.netrc`, `auth.json` или содержимого БД. Metadata кандидата DB/schema не является разрешением открыть соединение или выполнить миграцию. Heavy directories видны как записи, но их дочерние записи по умолчанию не перечисляются рекурсивно. Явный include конкретного потомка позволяет пройти metadata к нему; прочие потомки не получают право чтения.

Поддерживаются вложенные `.gitignore`, комментарии, escaped `#`/`!` и пробелы, basename/anchored/directory patterns, `*`, `?`, character ranges, globstar и negation. Исключённый parent нельзя вернуть одним child-negation внутри ignore; project include — отдельный более высокий policy layer. Не читаются Git global excludes, `.git/info/exclude` и Git tracked state: это policy read/index, а не точная копия `git status`. POSIX named classes в ignore объявляются unsupported; такая policy становится partial и отклоняет content в затронутом scope. Ignore-файл с ошибкой/небезопасным handle также не выдаётся за успешно применённую policy.

`policyVersion` стабилен для algorithm и configured policy. Отдельный `ignoreRevision` учитывает фактически применённые ignore-файлы; revision записи связывает root identity, metadata и ancestor ignore context. Поэтому `inspect`/directory/`read(path, revision)` используют один pin, а изменение файла, policy или `.gitignore` инвалидирует старый pin. Snapshot revision включает наблюдавшийся bounded manifest. Перед публикацией metadata и ignore pins проверяются повторно; source/root/policy drift отклоняет результат. Это не глобальная блокировка файловой системы и не обещание live watcher.

### Чтение и безопасность

`read` отдельно проверяет все предки, canonical containment, identity зарегистрированного root, отсутствие symlink/junction/multiple hard links, opened handle и metadata до/после чтения. Traversal, абсолютные пути, ADS и Windows device/trailing-dot aliases не становятся relative authority. Display paths сохраняют имена; сравнение pins и правил учитывает Windows case semantics. Binary, invalid UTF-8, oversized и недоступные файлы получают отдельную ошибку, сохраняя другие записи и доступные результаты consumer.

По умолчанию known sensitive content отклоняется и не попадает в code index. Только для document/control-plane display consumer может явно выбрать `redactSensitive:true`: обычные credential assignments заменяются через существующий `safePersistedText`, ответ содержит `redacted:true`, а hash и byteSize по-прежнему относятся к оригинальным байтам. Private-key BEGIN markers, включая обрезанный блок без END, hard sensitive filenames, links и binary не становятся доступными даже в этом режиме. Фильтр известных credential forms не доказывает обнаружение любого возможного секрета. Возвращённый HTML — текст для безопасного UI, не документ для выполнения скриптов.

### Budgets и проверки

Default page — 100, maximum page — 200; direct directory — до 2000 записей, recursive metadata — до 10000 записей/1000 файлов и глубины32, 30 секунд. Отдельный source read — до512KiB, response — до1MiB, ignore data — до64KiB на файл и4096 правил на scope обхода. Lower limits допустимы; response budget не меньше8192bytes оставляет место для envelope. Превышение directory/manifest/response budget даёт explicit partial/reasons, отменённый snapshot не публикует success. Cursor подписан и привязан к проекту/root/policy/revision/path/query/filter/page size; поиск явно ограничен текущим каталогом.

`node --test tests/web/project-inventory.test.mts` — **15/15 passed, 0 skipped** в текущем focused run: metadata неизвестных/binary файлов и пустых папок, ignore/precedence, sensitive denial, inspect/read pins, Unicode/inert HTML, file/policy changes, binary/encoding/size errors, cursor isolation, limits/cancel, реальные hardlink/junction и root replacement, document-only redaction, source preservation и Windows case/device boundaries. Первоначальный metadata RED наблюдал ожидаемое отсутствие записей; отдельная regression поправила порядок linked-source admission до чтения ignore. Интеграцию существующих consumers, HTTP и UI проверяет владелец [FUNC-G03](../planning/functional-remediation-2026-11-15.md) отдельно; эти15 тестов не являются browser/native release qualification.

Context7 использован для [Node26 fs](https://github.com/nodejs/node/blob/v26.0.0/doc/api/fs.md), [Node path.matchesGlob](https://github.com/nodejs/node/blob/v26.0.0/doc/api/path.md) и [официальной gitignore semantics](https://git-scm.com/docs/gitignore). `path.matchesGlob('*')` не включает dotfiles, поэтому он не подменяет gitignore: небольшой position-set matcher реализует нужную wildcard grammar без regex backtracking и без новой зависимости. Rules/configs анализируются только как данные, команды проекта не исполняются, исходники не меняются.

Финальный lower receipt после private-key fence: `.tmp/func-g03/f28-lower-native-key-fence-final.log`,15/15,0skip. Отдельный default-executor повтор получил14pass/1setup EPERM при создании junction; этот setup failure не является поведенческим RED или green suite. Его summary сохранён в `.tmp/func-g03/f28-lower-evidence.json`; точный lower native retest выполнил настоящие link boundaries. Остальные integration/browser/native gates группы принадлежат root.

## Исторический Web source inventory

[sources.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/sources.mts) проверяет identity зарегистрированного root и его предков; исключает чувствительные каталоги/пути, symlinks и файлы с несколькими hard links, контролирует UTF-8, drift и root containment. Обход ограничен глубиной 32, 10 000 directory entries и 1000 подходящими файлами. Это ограниченный source inventory, а не видимое дерево всех файлов или универсальная обработка ignore-файлов.

Graph [service.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/service.mts) ограничивает общий размер 8 MiB, один файл 512 KiB, 25 000 nodes, 50 000 edges и работу parser worker 10 сек; до восьми snapshots. Подходящие для inventory другие языки получают coverage `unsupported`; связанные источники могут быть `excluded`. Достижение hard limit вызывает ошибку, а не гарантирует безопасное полное усечение до лимита.

## Python manifest

[project_graph_manifest.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_manifest.py) формирует normalized file records, размер, fingerprints, language и generated flags; [project_code_graph.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_code_graph.py) использует их для графа. Сбор по умолчанию ограничен 10 000 файлами и записывает truncation/omitted counts. Конкретные исключения и policy следует читать у scanner: Web и Python не обещают одинаковый inventory. Каталог generated может быть отражён в manifest без семантического overlay.

Сравнивайте revision/manifest, coverage и сообщения об ошибках до использования индекса. Лимиты, encoding, пропущенные пути и drift должны оставаться видимыми; результаты не являются аудитом всех файлов проекта. Исторические pinned Web-источники выше описывают прежний контракт; текущее внедрение общего слоя и зависимых F26–F29 принадлежит FUNC-G03.

Проверки: [Web source tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [manifest tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_manifest.py). Нового runtime-прогона этот текст не заявляет.

## F28 — shared consumer integration

Graph, artifact catalog и fixed control-plane sources используют нижний inventory. Graph manifest содержит metadata inventory/policy revision; size/encoding failures становятся явными per-file exclusions. Artifact cursors привязаны к root/policy/inventory revision; прежняя policy не сохраняет право чтения документа. Profile-owned include/exclude/respectGitignore сохраняются через CAS без изменения immutable SQL migrations и без task/document pseudo-entities. Display-only readers сохраняют redacted before-images; analyzer reads не используют этот режим.

Текущий общий regression:57/57,0skip (`.tmp/func-g03/f28-verified-final.log`), TypeScript прошёл. Finite G02 corpus projection проверена как более строгий subset F28 read authority, с sensitive denial и без выполнения config; исторические engine benchmarks не повторялись и не переписывались. Прежние sandbox EPERM и настоящие RED receipts сохранены.

Текущее дополнение: virtual `access(project,path)` проверяет policy и существующих ancestors для отсутствующего create target. Общий final registry fence отклоняет захваченные права после asynchronous work; metadata pins не заменяют raw content hashes. Полный текущий Web594/594,0skip; independent policy-race regressions5/5.
