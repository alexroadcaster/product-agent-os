from pathlib import Path
updates={
'PLAN.md':('UI-01–UI-11 implemented; UI-12 owner acceptance in_progress.','UI-01–UI-12 повторно открыты: in_progress. Приоритет — структурное соответствие каждому экрану V3 и визуальное сравнение обеих тем.'),
'RUNLOG.md':('Дизайн V3/Sidebar утверждён; UI-01–UI-11 внедрены и локально проверены; UI-12 ожидает приёмки владельцем.','Дизайн V3/Sidebar утверждён; реализация возвращена на доработку после визуального расхождения. UI-01–UI-12 in_progress; прежние тесты не доказывают соответствие прототипу.'),
'REQUIREMENTS.md':('Приёмка реализации отдельно от утверждения дизайна.','Приёмка реализации отдельно от утверждения дизайна. Дополнительный критерий владельца: лично сравнить каждый продуктовый экран V3 в светлой и тёмной теме, включая сетки, поля, кнопки, состояния и анимации; проход тестов не заменяет визуальное сравнение.'),
'EVALS.md':('Synthetic verification не доказывает host telemetry, production performance или human acceptance.','Synthetic verification не доказывает host telemetry, production performance или human acceptance. Для V3 требуется поэкранный визуальный ledger обеих тем: captured не означает reviewed; отсутствующие или несовпадающие состояния запрещают общий verdict о соответствии.'),
'TEST.md':('Альбом не заменяет app gates; human acceptance отдельно.','Альбом не заменяет app gates; human acceptance отдельно. Расширенный `tests/web/single-window/v3-state-capture.mts` снимает внутренние состояния в одноразовом профиле; результаты stateViews и визуальный review учитываются отдельно от 15 основных destinations.')}
for file,(old,new) in updates.items():
 p=Path(file);s=p.read_text(encoding='utf-8')
 if new in s: continue
 assert old in s,file;p.write_text(s.replace(old,new,1),encoding='utf-8')
p=Path('design/2026-11-13-v3/implementation-evidence.md');s=p.read_text(encoding='utf-8');s=s.replace('Source status: current local implementation, 13.11.2026; implemented_locally_verified; UI-12 owner acceptance pending. Дизайн утверждён, приёмка реализации pending.','Source status: 13.11.2026; V3 parity repair in_progress. Предыдущая реализация возвращена на доработку; старые receipts ниже являются историческими, не доказательством текущего соответствия V3.',1)
entry='''
## Повторная доработка V3 — текущий незавершённый срез

Владелец потребовал строгое соответствие всех экранов, не CSS поверх старой структуры. UI-01–UI-12 reopened. Изменены сетки задач/редактора/overlay, внутренние вкладки, dashboard compositions, settings navigation, каталоги assets, sessions, документы, autonomy, decisions, import/backup и процесс master/detail. API/backend/contracts не менялись. Новые зависимости не устанавливались.

Текущие проверки (до полного визуального review):

- `npm run check:web-m1`: exit 0 после структурных правок.
- `npm run build:web`: exit 0; последняя сборка main 691.42 kB / gzip 211.72 kB, CSS 50.26 kB. Bundle warning сохраняется.
- `npm run test:web-m1`: sandbox attempt failed на создании symlink fixtures (EPERM); повтор с теми же тестами вне sandbox: 500 passed, 0 failed, 0 skipped, 50.704 s. Receipt `.codex-tmp/v3-parity-tests-unsandboxed.txt`.
- `m2c-browser-acceptance.mts --scenario ui-v3`: первый запуск sandbox завершился до браузера; второй дал 43 checks и timeout положения подсветки. Исправлены дробные координаты Sidebar. Повтор: 356 passed, `.tmp/paos-m2c/browser-evidence-fAceOh/result.json`. Этот прогон предшествует последним изменениям workflow/toolbar и не закрывает весь V3.
- `m2-task-manager-browser-acceptance.mts --scenario task-overlay`: RED на скрытом accordion noRisks после переноса формы; сценарий обновлён на явное раскрытие. Повтор выполняется; успех не заявлен.
- CUA: Chrome, существующий Neural_Flow, после reload наблюдается новая композиция overview в тёмной теме. Проектные данные не изменялись.

Визуально просмотрены текущие overview, tasks base, general settings и workflow baseline против соответствующих PNG прототипа. Найденные расхождения вызвали перенос toolbar в левую колонку, выравнивание navigation слева, удаление двойного overview heading и замену workflow accordion grid на master/detail. **Полное сравнение всех экранов и обеих тем ещё не завершено.**

Незакрытые проверки: current expanded capture run, all-state review, task/settings/team functional regression, документы/gates, финальная активация и пользовательская приёмка. Generated skill/recipe recovery и provider-dependent states требуют синтетических fixtures; вызовы провайдеров не разрешены и не нужны.

'''
s=s.replace('## Границы и baseline',entry+'## Границы и baseline',1);p.write_text(s,encoding='utf-8')
