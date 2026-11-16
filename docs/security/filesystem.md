# Файловая система и идентичность корня

Source status: repository_source / static_source_review + FUNC-10_inspector_focused_verified; API_gateway_UI_locally_verified; 15.11.2026.; FUNC-G05 locally_verified_with_explicit_limits, 16.11.2026.

Владелец: security/runtime owner + docs-maintainer. Область: исходники PAOS на `259977f3b257ba7fc0e932396f8963262bd327ad`; обновлять при изменении guards, tests или policy. Ссылки на тесты обозначают маршруты проверки, а не новый прогон. Реальные профили, credentials и provider-вызовы не исследовались.

## Регистрация и чтение

[project-sources](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/adapters/project-sources.ts) разрешает локальный абсолютный путь и связывает canonical root с identity каталога (device/inode); перед чтением фиксированных control-plane файлов сверяет binding, проверяет regular file, отсутствие symlink и hardlinks, размер до 1 MiB, identity открытого handle и изменения в процессе чтения. Хеш относится к исходным байтам, а возвращаемый текст может быть redacted. Это отдельный ограниченный reader, а не полный проводник проекта.

[app-agent-files](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/runtime/app-agent-files.mts) снимает наблюдение только pinned task files: максимум 32 файла, 64 KiB на файл и 512 KiB суммарно. Он исключает private paths, links, binary/private-key содержимое, проверяет путь, handle и повторный binding; вывод diff ограничен и redacted. Отказ или excluded означает отсутствие допустимого наблюдения, а не доказательство отсутствия изменений.

[profile identity](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/connections/profile-identity.mts) отдельно проверяет идентичность каталога профиля и namespace credential store. Admission check не является атомарной файловой блокировкой. Для изменений нужны [project source tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/project-sources.test.mts), [file tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/app-agent-files.test.mts), [profile tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/profile-identity.test.mts) и проверка соответствующей пользовательской поверхности; эти ссылки не означают их запуск сейчас. Реальный проект здесь не сканировался, а полный файловый каталог и будущие интеграции описаны в плане, а не доказаны этим reader.

## FUNC-G03 / F28 — shared inventory boundary

Текущая F28 заменяет раздельные source policies общим checked inventory. Видимость metadata не выдаёт права чтения содержимого, индексации или исполнения. Hard sensitive names, linked paths, canonical aliases, root drift и private-key BEGIN markers остаются запрещены; include не отменяет запреты. Обычные credential assignments документа могут отображаться только с явной redaction и hash исходных байтов; code analyzers такие contents отклоняют. Fixed control-plane display read использует общий bounded512KiB policy.

Root/policy/ignore/file revisions связывают страницы и чтение; policy change инвалидирует graph и artifact cursors. Durable policy CAS хранится в профиле PAOS без записи в target и изменения schema migrations. На этапе закрытия F28 synthetic source/consumer checks57/57 включали реальные Windows hardlink/junction; это не human acceptance, аудит реального проекта или полное обнаружение secrets. [Inventory contract](../code-intelligence/inventory.md).

## FUNC-10 — общий execution file preflight

Текущий `preflightTaskFiles(project, files)` в `apps/local-service/src/runtime/app-agent-files.mts` повторно использует F28 root/policy/read boundary. Публичный `paos_file_preflight_v1` возвращает только metadata: allowed, limits/counts, per-path operation/state/reason, raw SHA256 и metadata pins там, где они наблюдались, rootIdentity/policyVersion, digest и revision выбранного scope. Ни source text, ни diff в отчёт не входят. Для проверки binary/encoding/hash инспектор внутренне читает только bounded байты выбранных файлов; это не передача проекта модели.

Execution limits не повышены: **32 пути,65536 raw bytes на файл,524288 raw bytes суммарно**. UTF-8 characters не подменяют byte count. Rename включает source и destination и расходует два path slots. Превышение count останавливает проверку содержимого; `not_checked` означает отсутствие наблюдения, а не успешный read. `counts.totalBytes` — сумма известных raw sizes, `bytesComplete=false` указывает неполное знание; неизвестный размер запрещённого пути не становится доказанным нулём.

| Planned operation | Условие допуска |
| --- | --- |
| `create` | Destination отсутствует, виртуальный путь разрешён policy, существующие предки проверены. Уже существующий файл — conflict. |
| `read`, `modify`, `delete` | Нужен существующий regular readable source в limits. Missing source блокирует dispatch. |
| `rename` | Старый source присутствует и допустим, новый destination отсутствует и разрешён; проверяются оба пути. |
| `create_or_modify_after_discovery` | Явно допускает существующий либо отсутствующий target с теми же policy/root/budget checks. |
| `null` / отсутствует | Совместимый read/observe смысл; это не неявное разрешение создать отсутствующий файл. |

Новый metadata-only lower seam `inventory.access(project,path)` применяет ancestor ignore/project policy к отсутствующему create target без открытия несуществующего файла или создания parent directories. Существующие предки/root и applied ignore pins перепроверяются; появление ранее отсутствовавшего parent во время проверки даёт drift. Sensitive paths, symlink/junction/hardlink, binary/private-key content, invalid UTF-8 и ненадёжная revision блокируют admission с отдельной причиной. Include не обходит hard denial; игнорируемый отсутствующий `*.log` не становится разрешённым только потому, что его ещё нет.

Optional file `revision` сравнивается с raw-byte SHA256, `fileRevision` — отдельно с metadata/policy pin. Scope digest не включает время наблюдения и стабилен для неизменившихся входов; `inventoryRevision` относится к выбранным task paths, не является revision полного scan проекта. Проверку task expectedRevision/CAS, actual gateway/native dispatch и повторный preflight непосредственно перед side effect выполняет root integration. Сам по себе положительный отчёт не стартует run, не выдаёт sandbox approval и не устраняет TOCTOU атомарной файловой блокировкой.

`captureTaskFiles` сохраняет observational before/after смысл через тот же checked inspector. После planned create созданный файл может быть `present`; planned operation и старый source pin не запрещают наблюдать фактический after-state. Rename отображается как observed delete старого и add нового пути. Excluded source не даёт fake diff и не доказывает отсутствие изменений; компактный diff остаётся bounded/redacted, hash — исходных байтов. Обычные credential assignments redacted для diff-display, private-key BEGIN запрещён даже без END. Native broker ownership должен учитывать оба rename paths независимо от UI-видимости.

Current focused evidence: `node --test tests/web/file-preflight.test.mts tests/web/app-agent-files.test.mts` — **13/13 native,0skip**, `.tmp/func-g03/f10-inspector-final-native.log`; targeted TypeScript для inspector/transitive lower tree — exit0. Проверены32/33,65536/65537,524288/524289, create/missing/rename, stale pins, source preservation, no-content report и настоящие link/root boundaries. Новый lower access test имеет наблюдённый RED/GREEN. Отдельный combined29-case default run имел26pass/3junction setupEPERM и сохранён как `.tmp/func-g03/f10-focused-sandbox.log`; ровно3 boundary cases повторены native,3/3,0skip в `f10-link-boundary-native-retest.log`. Он не объявляется одним green sandbox run. Gateway/API/browser и текущая native runtime qualification ещё принадлежат root [FUNC-G03](../planning/functional-remediation-2026-11-15.md). Node26 fs/checked-handle semantics ранее сверены через Context7; новые dependencies и actual project execution не использовались этим focused slice.

## FUNC-G03 — окончательная registry authority

Захваченный project/policy не считается текущим после asynchronous I/O. Task preflight в конце атомарно перечитывает task и registry; перед native dispatch scope сверяется после dependency/autonomy waits. Task references, Files, artifact body/cursor previews, direct graph rebuild/source, control-plane HTTP reads и requirement grounding используют общий final registry fence. Отзыв policy во время чтения не выдаёт body и не заменяет предыдущий graph. Найденная independent review гонка подтверждена RED и исправлена; reviewer cycle2 проверил5/5 regressions, closed_allowed.

API/gateway/production UI integration завершена: blocked preflight сохраняет draft и не вызывает runtime Send. Final browser19/19 (`.tmp/func-g03/browser-final/evidence-IfLiEa/result.json`); полный Web594/594,0skip. Текущий native tuple64cd3b58… прошёл candidate и production-default offline проверки write/deny/drift/interrupt; Python bridge теперь входит в executable source pin. Это не provider/human acceptance.

## FUNC-G05 — реализованные контракты

F13 разрешает изменение только существующих readable .md/.txt до512KiB по F28, без create/delete/rename. Linked/hardlinked/reparse paths, ignored/private/generated/redacted content и durable instruction/config/hook/rule/skill/plugin targets отклоняются. PLAN/REQUIREMENTS/TEST/EVALS/RUNLOG допускаются только через точный document preview. Preview связывает rootIdentity, policyVersion, fileRevision и raw SHA256; перед native commit metadata перепроверяется после получения эксклюзивного handle. Внешнее изменение .gitignore проверяется непосредственно перед записью, но не является атомарным механизмом отзыва уже начавшейся операции. SQL-origin не зеркалируется в workspace, filesystem-origin не меняет параллельный SQL-документ.

Текущие focused evidence и оставшаяся квалификация: [FUNC-G05](../planning/functional-remediation-2026-11-15.md#func-g05-results).
