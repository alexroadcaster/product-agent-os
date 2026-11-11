# Product-Agent OS Web — M1

Autonomous follow-up 2026-11-11: initial SESSION_REQUIRED UX fixed; browser669/autonomous launcher56/Web197 passed. PAOS-0040 technical implemented using separate native closed-App and current browser receipts. No manual tester steps required; human/provider/M1 acceptance remains separate. Evidence: research/product-agent-os-web-m1-execution-2026-11-11.md.

PAOS-0004 browser acceptance 2026-11-11:667/667, Web195/195, strict/build35 passed; themes/locales implemented. PAOS-0040 external recorder prepared; real closed-App receipt still required. See research/product-agent-os-web-m1-execution-2026-11-11.md.

Follow-up 2026-11-11 10:36 MSK: shared draft lifecycle/late Send ACK и runtime shutdown/approval/reconnect/time-cap guards исправлены. Общий Web suite192/192, strict/build35 и native headless33 passed. PAOS-0004/0040/0042/0043/0044 остаются in_progress до обязательной browser/provider/native-window приёмки; детали в research/product-agent-os-web-m1-execution-2026-11-11.md.

Дополнение 2026-11-11 09:25 MSK: исправлены credential namespace разных PAOS-профилей и закрытие SQLite после HTTP drain. Новый Web suite 166/166, native headless33 passed; legacy default-account recovery отклоняется без автоматической миграции. Предыдущие результаты ниже сохраняют исходный provenance.

Source status: локальная реализация и детерминированные проверки; браузерная и provider-приёмка не выполнены.

Дополнение 2026-11-11 08:46 MSK: local auth components PAOS-0041 квалифицированы. Однократный отдельно разрешённый `node tests/web/single-window/vault-roundtrip.mts --synthetic-vault` выполнил native OS-store write/read/delete только случайной fixture; cleanup подтверждён. Этот executable требует отдельной authority, стандартный unittest его не запускает. `node tests/web/single-window/auth-metadata.mts --synthetic-auth --binary <pinned-codex.exe>` проверил actual stdio/broker login/read/logout с synthetic API value, loopback-only fixture provider и отключённым API-key model discovery, без turn и vault calls. Это local login, model access остаётся unverified. Новый полный Web suite — 159/159, no skips; прежние build/UI receipts ниже сохраняют исходный provenance.

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
