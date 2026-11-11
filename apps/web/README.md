# Product-Agent OS Web — M1

Source status: локальная реализация и детерминированные проверки; браузерная и provider-приёмка не выполнены.

React/TypeScript SPA использует same-origin `/api/v1` локального сервиса. Production entrypoint — `dist/index.html`; сервис раздаёт `dist/` и API на одном origin. Runtime не содержит демонстрационных задач или сообщений. Без сервиса показываются сопряжение и наблюдаемая ошибка.

Сборка из `apps/web`:

```powershell
npm run build
```

Точные версии зависимостей закреплены в `package-lock.json`. Установка выполнена родительским агентом через разрешённый registry-маршрут с `--ignore-scripts --no-audit`. Dev server для сборки не требуется.

Пример команды native launcher из корня репозитория — **иллюстрация, здесь не выполнялась**:

```powershell
node apps/launcher/main.mts --profile C:\paos-synthetic\profile
```

Файл профиля `runtime-selection.json` явно выбирает `binaryPath`; `providerAuthority` по умолчанию false. Минимальный синтетический пример:

```json
{
  "binaryPath": "C:\\paos-synthetic\\runtime\\codex.exe",
  "providerAuthority": false
}
```

Для runtime требуется проверенная совместимость выбранного бинарника и manifest. Launcher не ищет Codex и не устанавливает его автоматически. Missing/unqualified runtime оставляет `qualification_required`; это не подтверждение provider activation. Ключи и provider authority в этом frontend-срезе не использовались.

Интерфейс включает flat Task CRUD, fixed Kanban, related/blocks references, Comments/History, отдельные ручную проверку и owner acceptance, проекты, read-only catalogs, документы и поиск. Записи используют paired cookie, `X-PAOS-CSRF`, project authority epoch и expected revision. API login и disconnect доступны в Settings; ключ существует в native password input до запроса и очищается после него. Login state отличается от model access. Quit требует явного подтверждения; `OWNER_UNAVAILABLE` не превращается в успешную остановку.

Execution требует saved task scope/criteria и явного mode binding. Сервер вычисляет scope digest. Исторический terminal run не запрещает следующий mode; active/unknown run остаётся fenced. Опрос каждые 750 мс не пересекает циклы, ограничен 20 страницами, отменяется при dispose. Streaming допускает только подтверждённый `final_answer`; persisted message заменяет draft по точной паре run/item. Diff различает proposal, runtime-reported actual и external. Runtime outcomes, product decisions, ручные checks и tool permissions показываются отдельно. Allow требует текущих reviewable details, binding/run/generation, pending state и неистёкшего срока.

Черновик сессии сохраняется с debounce 500 мс и flush при закрытии. Записи последовательны и привязаны к revision; после lost ACK повтор использует тот же idempotency key. Конфликт не перезаписывает чужую новую revision. ACK отправки очищает только отправленный текст, сохраняя последующие правки. Scroll сохраняется при переключении context/diff. Источники показываются escaped read-only с hash/coverage/redaction marker; добавление reference в draft явное, без автоматической отправки файла. Upload attachments в M1 недоступен.

Импорт поддерживает один source или JSON records + optional MD projection с явными project-relative paths. Preview не меняет target. Cutover требует отдельного подтверждения, повторного чтения источников, server freeze и writer inventory. `WRITER_INVENTORY_INCOMPLETE` сопровождается следующим действием. Normalized reverse proposal не включает автоматический cutover. Экспорт SQL JSON можно просмотреть и скачать. Source status показывает drift после переноса. Backup возвращает manifest и candidate IDs; `retention:pending` остаётся до отдельного подтверждения ротации. UI сначала показывает managed candidates, затем отправляет только подтверждённые IDs и показывает rotated IDs из receipt. Restore создаёт отдельный профиль и показывает `requiresRestart:true`, `activeProfileChanged:false`. Граф unavailable без owning source. Source/capability metadata не доказывает активацию агентов или skills.

Проверки из корня репозитория:

```powershell
node --experimental-strip-types --test tests/web/ui-api.test.mts tests/web/ui-policy.test.mts tests/web/ui-stream-search.test.mts tests/web/ui-draft-autosave.test.mts tests/web/ui-import-sources.test.mts tests/web/ui-session-poll.test.mts tests/web/ui-session-target.test.mts tests/web/ui-task.test.mts tests/web/theme-locale.test.mts tests/web/catalogs.test.mts
```

Наблюдаемый полный frontend baseline: **34 теста, 33 PASS, 1 SKIP, 0 FAIL**. SKIP — создание junction fixture запрещено текущим Windows sandbox (`EPERM`). Затем отдельно исправлен catalog hardlink guard: `node --experimental-strip-types --test --test-name-pattern=hardlinked tests/web/catalogs.test.mts` дал наблюдаемый RED с чужими синтетическими metadata, затем GREEN, 1 PASS. Полный catalog запуск после добавления кейса: 4 теста, 3 PASS, 1 junction SKIP.

RED→GREEN также наблюдались для gate отправки/приёмки, pairing, корреляции истории, сохранения file metadata, service error code, import/restore API, отменяемого опроса, Execution target, Quit, terminal run scope fence, approval details, final-only streaming и autosave/lost ACK. Проверки не запускают браузер или provider.

Последнее расширение backup rotation проверено отдельно: `node --experimental-strip-types --test tests/web/ui-api.test.mts` — 7 PASS после RED `Rotation route not connected`. Создание backup не вызывает rotation автоматически. Session/comment history показывает partial и More для следующих страниц, сохраняя выбранную сессию и её черновик; обе поверхности остаются keyed к project/task.

Исправление длинной истории: polling использует отдельный scoped messages API с `order=newest`, получает последние ≤1000 сообщений и сортирует по server `journalOrder`. Manual Older/Newer читает отдельное окно 50 более ранних записей; одновременно отображается ≤1050 persisted rows, без накопления 100k DOM nodes. Неизвестный journal order явно отмечается и использует fallback по ID. Новые final messages не скрываются за первым тысячным окном. TDD-воспроизведение на 2001 synthetic messages сначала показало неверный порядок, затем GREEN; дополнительно проверены bounded older-page replacement, dedup/revision и scoped offset/abort API.

Последний `npm run build`: exit 0, TypeScript + Vite, 34 modules. Responsive layout, keyboard/focus, accessibility, 200% zoom, refresh/recovery и реальные HTTP/UI journeys требуют отдельной разрешённой браузерной проверки. Полная приёмка PAOS-0043/PAOS-0045 этим результатом не подтверждается.
