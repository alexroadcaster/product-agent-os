from pathlib import Path
import json, hashlib

root=Path('design/2026-11-13-v3')
p=root/'implementation-evidence.md'
s=p.read_text(encoding='utf-8')
entry='''# Внедрение UI-01–UI-12 — V3 и Sidebar collapse

Source status: local UI repair and visual comparison, 13.11.2026. Current result: locally_verified / needs_user_acceptance. Строгое пиксельное совпадение и новая пользовательская приёмка не заявлены.

## Повторная доработка — результат текущего среза

Перенесены рабочие композиции всех 85 продуктовых экранов V3: shell и sidebar, список/доска/полная карточка задачи, настройки задач, процессы, сессии, assets, генератор, документы, проверки, решения, autonomy, import/backup, dashboards и graph views. Два оставшихся route из 87 — component-lab и motion-lab альбома, не продуктовые разделы.

Исправления затрагивают `apps/web/src/design/{theme,workspace,parity}.css`, `ui/{App,Sidebar,Modal,Operations,ConnectionControls,SessionContext}.tsx` и presentation-компоненты `features/{tasks,workflows,sessions,team,skills,graph,artifacts,autonomy,decisions,dashboard}`. Статический diff для `apps/local-service` и `packages/contracts` пуст. Во время repair зависимости не устанавливались. Сохранены формы, обработчики, previews, подтверждения, CAS/revision и идемпотентность.

- Задачи: toolbar в колонке списка, компактный инспектор; одна форма в большом dialog по двойному клику, две колонки полей, контекст справа, закреплённые заголовок/вкладки/действия. Остались все 8 функциональных вкладок и отдельный экран расхода.
- Процессы: отдельные разделы вместо единой длинной формы, список состояний/переходов рядом с редактором, таблицы назначений/версий, двухколоночная миграция. Все поля остаются в исходной форме; hidden-панели не создают вторых редакторов.
- Сессии: список слева, рабочая область в центре, запуск/проверки/вопрос справа. Контекст и вопрос разделены; история открывает выбранную сессию, сохраняются anchors и поиск.
- Assets/документы: каталог и контекст справа, редактор и diff слева; генератор с тремя шагами; proposal/apply остаются отдельными действиями.
- Dashboards: 4 метрики, аналитика/очередь/нагрузка и таблицы; неизвестные показатели показываются как unavailable, не как ноль. Визуальные демонстрационные суммы не переносятся в реальные данные.
- Карта: D3, Mermaid и список с одним источником узлов; модуль, zoom и локальная прокрутка. Список ограничен по высоте рабочей области. Схема процесса первоначально вписывается целиком, кнопка 100% позволяет читать мелкие подписи.
- Обе темы: компактный ритм, двухтонные локальные SVG, общий набор borders/focus/disabled/notice. Sidebar216↔64, исходные spring constants, GSAP lifecycle и reduced motion сохранены.

## Поэкранный визуальный review

[Альбом сравнения](implementation-gallery.html) содержит V3 и actual app рядом, выбор всех 85 экранов, light/dark и полноразмерные PNG. [Машиночитаемый ledger](implementation-visual-review.json) перечисляет каждый экран, тему, hash изображения, audit и source hashes. Это статические изображения; анимации проверяются отдельно в приложении.

Root лично сопоставил все 170 состояний из `browser-evidence-V81wgT` с PNG V3: 29 сравнительных листов, дополнительно 13 листов нижних частей 37 длинных экранов; task overlay и runtime question проверены полноразмерно. После последнего исправления graph-list/workflow-diagram/asset editor повторены full capture и automated audit (`NqJx7X`), затронутые композиции вновь просмотрены в обеих темах. Для остальных неизменённых композиционных областей использован уже выполненный review; новые временные метки и fixture IDs не считаются изменением дизайна. Review mode: `self_review`; предыдущие независимые reviews не выдаются за review последней сборки.

За время сравнения исправлены: потеря начала dialog из-за autofocus, избыточные row grids редакторов, двойные заголовки, каталог с неправильной стороны, смешанные context/question/checks, нечитаемый масштаб Mermaid, цвет текста Mermaid в dark, растянутая таблица graph-list, duplicate asset IDs при скрытом втором каталоге. **Captured не использовалось как синоним reviewed.**

## Текущая проверка

| Проверка | Команда / receipt | Результат |
| --- | --- | --- |
| TypeScript | `npm run check:web-m1`; `.codex-tmp/v3-final-typecheck.txt` | exit 0 |
| Production frontend build | `npm run build:web`; `.codex-tmp/v3-parity-build.txt` | exit 0; JS `index-B7jp5dfA.js`, CSS `index-xRVpE75C.css` |
| Полный web suite | `npm run test:web-m1`; `.codex-tmp/v3-final-layout-tests.txt` | 500 passed, 0 failed/skipped; 56.512 s |
| V3 browser | `node --experimental-strip-types tests/web/single-window/m2c-browser-acceptance.mts --synthetic-browser --scenario ui-v3 --playwright-core <installed-playwright-core> --chromium <installed-chromium>`; `.tmp/paos-m2c/browser-evidence-NqJx7X/result.json` | passed, 378 checks; 170 captures; no page errors / external requests / root overflow / audited contrast findings |
| Existing team/workflow actions | `m2b-browser-acceptance.mts --synthetic-browser` with same browser arguments; `.tmp/paos-m2b/browser-evidence-UIqzYt/result.json` | passed, 51 checks; before final presentation-only graph/asset grid tweaks; command handlers unchanged |
| Task overlay | `m2-task-manager-browser-acceptance.mts --scenario task-overlay`; `.tmp/paos-m2/browser-evidence-gueRa6/m2-browser-result.json` | 19 passed; reused evidence for unchanged task handlers |
| Settings layout / CAS | `.tmp/paos-m2/browser-evidence-Z6vkxH/`, `.tmp/paos-m2/browser-evidence-ONAWBD/` | 14 / 17 passed earlier in this repair; later tables covered by V3 capture and M2b actions |

Installed paths: `C:/Users/user/AppData/Local/npm-cache/_npx/eb7983f9b02fb67f/node_modules/playwright-core` and `C:/Users/user/AppData/Local/ms-playwright/chromium-1223/chrome-win64/chrome.exe`. Runs use disposable loopback profiles; fixtures cleaned. No provider/model calls, real credentials or real project mutations. Generated skill, binding response and recipe recovery GET are explicit visual-only mocks listed in the receipt. They prove rendering, not provider execution.

Browser checks cover RU1280/1440/1920 and EN1440, both themes, 15 destinations; 85 internal product states at1440, keyboard tabs/dialog focus, Sidebar sizes/reduced motion, renderer activation and zoom. RGB contrast audit excludes native widget paint/gradients and does not establish full WCAG certification. Motion interpolation was observed earlier in this repair on actual Sidebar; the final automated run confirms endpoints/reduced motion. Static captures cannot prove subjective smoothness.

Intermediate failed receipts retained: sandbox symlink EPERM; build-inventory failure when tests overlapped rebuilding (stable rerun500); old harness navigation timeouts after pages split into tabs (M2b UIqzYt passed after explicit navigation); earlier Mermaid contrast/selector/duplicate asset failures. None is relabelled as a pass. The latest two final runs are successful.

## Различия и границы приёмки

| Область | Что отличается от демонстрационного V3 и почему |
| --- | --- |
| Метрики | API не даёт полноценные tokens/cost/tool_use. Карточки и chart frames присутствуют; вымышленные полосы/цены не добавлены. Сбор telemetry — отдельное функциональное изменение. |
| Наборы данных | Количество задач, статусов, агентов, узлов, документов и очередь определяются существующими источниками. Поэтому длина списков и геометрия графа не совпадают с примером. |
| Поля | Существующие metadata/confirmations сохранены даже там, где пример их опускает. Поля, не имеющие контракта (например, описание компонента или причина recovery), не добавлены как фиктивно работающие. Названия отдельных legacy полей сохранены. |
| Runtime | При неподключённом агенте question/run/checks показывают недоступность. Активный provider runtime не запускался. |
| Native controls | Select/file/multi-select сохраняют системную реализацию и клавиатурное поведение. Assignment mapping редактируется в строках таблицы; backend semantics прежние. |
| Настоящий профиль | Final dist проверен в synthetic service. Повторное управление существующей Chrome-вкладкой вернуло `Debugger unattached`; финальный reload этой вкладки не наблюдался. Для просмотра текущей сборки нужен reload по прежнему адресу `http://127.0.0.1:52961/`. Профиль не заменялся. |
| Производительность | Vite предупреждает о размере chunks: main716.04kB, CSS70.15kB, lazy Mermaid2852.57kB. Большие реальные проекты и длительное использование не измерялись. |

Статус UI-01–UI-12 в плане остаётся `in_progress` до отдельного решения по результату внедрения. Это не блокировка инженерных проверок и не заявление о незапущенных тестах: текущая реализация локально проверена, а полное соответствие ожиданиям владельца / UI-12 требует просмотра. Не объявляем все визуальные отличия автоматически принятыми.

## Синхронизация документов

PLAN/RUNLOG/TEST: обновить текущий срез и evidence pointer. REQUIREMENTS/EVALS: `no_change_needed` после уже внесённого в этом repair требования all-screen review, функциональные границы не расширены. `prod_test.md`: `not_applicable`, Batch39 не затрагивался. Документация API/architecture/source registry: `no_change_needed`, внешних продуктовых утверждений и контрактов этот repair не меняет. Старые отчёты ниже сохранены как исторические, их результаты не относятся к final build.

Документальные gates записываются после текущего apply; до получения receipts они не считаются пройденными.

## Исторические записи предыдущего внедрения и промежуточного repair

'''
# Preserve all historical content rather than silently rewriting prior failed receipts.
p.write_text(entry+s[s.index('Source status:'):],encoding='utf-8')
p=root/'implementation-plan.md';s=p.read_text(encoding='utf-8')
s=s.replace('strict V3 parity repair in_progress.','V3 repair locally verified; UI-12 needs_user_acceptance; общий статус in_progress до приёмки.',1)
anchor='## Повторное открытие после визуального аудита\n'
s=s.replace(anchor,anchor+'\nТекущий checkpoint: полный визуальный review85 экранов ×2 темы выполнен; финальная сборка, web500 и V3 browser378 passed. Повторно проверены все170 состояний. [Попарный альбом](implementation-gallery.html), [ledger](implementation-visual-review.json), [актуальные проверки и отличия](implementation-evidence.md). UI-01–UI-11 имеют локальное evidence; карточки остаются in_progress до разрешения отличий при приёмке, UI-12 не закрыт. Старые Completion Reports ниже не подменяют текущую сверку.\n',1)
s=s.replace('- Next step: Исправить композицию по V3 и сверить каждый экран в обеих темах.','- Next step: Приёмка текущей реализации по попарному альбому и учёт отмеченных отличий; локальные проверки см. implementation-evidence.md.')
p.write_text(s,encoding='utf-8')
# Complete visual provenance without claiming every final timestamp was separately reviewed.
p=root/'implementation-visual-review.json';m=json.loads(p.read_text(encoding='utf-8'))
m['reviewBasis']={'allStates':'.tmp/paos-m2c/browser-evidence-V81wgT/result.json','finalRetest':'.tmp/paos-m2c/browser-evidence-NqJx7X/result.json','recheckedAfterLastPresentationChange':['agents-edit','skills-edit','graph-list','workflow-diagram'],'unchangedAreas':'prior reviewed evidence reused; all final captures and audits regenerated'}
m['frontendSourceHashes']={str(f).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('apps/web/src').rglob('*') if f.is_file()}
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Evidence, plan checkpoint and visual provenance updated; human acceptance remains open.')
