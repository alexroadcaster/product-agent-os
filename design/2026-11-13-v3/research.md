# Исследование desktop UI V3

Source status: public first-party documentation and current repository source inspection, 13.11.2026; design proposal, not application activation.

## Выбор компонентов

| Источник | Подтверждённое свойство | Решение для PAOS |
| --- | --- | --- |
| [icons0](https://icons0.dev/), [исходный проект](https://github.com/marcoripa96/i0) | Поиск по коллекциям Iconify, выдача SVG/React, registry | Выбрана единая семья Duoicons. Иконки поставляются локально, обращения к сервису при просмотре нет. Повторное открытие сайта дало timeout; каталог подтверждён поисковым индексом и исходным проектом. |
| [Duoicons](https://icon-sets.iconify.design/duo-icons/) | 91 иконка, сетка 24px, MIT | Двухтонная геометрия, цвет по назначению раздела. Малые служебные стрелки остаются нейтральными. Декоративные иконки aria-hidden, действия имеют текст/accessible name. |
| [GSAP skills](https://github.com/greensock/gsap-skills), [core](https://raw.githubusercontent.com/greensock/gsap-skills/main/skills/gsap-core/SKILL.md), [performance](https://raw.githubusercontent.com/greensock/gsap-skills/main/skills/gsap-performance/SKILL.md) | Timeline/tween API, transform/opacity, lifecycle cleanup | Прочитаны как рекомендации; глобальная регистрация skills не изменялась. Библиотека GSAP установлена только в дизайн-прототип. |
| [gsap.matchMedia](https://gsap.com/docs/v3/GSAP/gsap.matchMedia()/) | Media conditions и автоматический revert | Анимация учитывает reduced motion; при смене экрана старые tween/context уничтожаются. |
| [D3](https://d3js.org/getting-started), [force](https://d3js.org/d3-force/simulation), [zoom](https://d3js.org/d3-zoom) | SVG selections, scales, axes, force layout, zoom | Графики сравнения и динамики, интерактивная карта. D3 отвечает за геометрию; GSAP — за появление UI. Две библиотеки не анимируют одно свойство одновременно. |
| [Mermaid](https://mermaid.js.org/config/usage.html) | Markdown-подобное описание схем, SVG, strict security, Tiny build | Tiny 12.3.0 для локального flowchart. Используется Dagre; ELK/3D не нужны. Strict сохраняется, HTML/click-код из схем не включается. |
| [DesignBookmark Motion](https://designbookmark.com/motion) | Каталог живых образцов: tab pill, segmented control, loading-to-success, expand card, step progress | Берём принципы непрерывности выбора, локальной обратной связи и появления overlay. Не копируем случайные исходники или лицензионно непроверенные компоненты. |
| [bb](https://getbb.app/), [Ratio](https://ratioteams.com/) | Публичные продуктовые страницы показывают проектный контекст, работу с агентами/задачами | Сохраняем контекст при открытии объекта; сокращаем смену всей страницы. Плавность закрытых приложений, FPS и точные easing не измерялись; обещаний превосходства по скорости нет. |

## Что делает интерфейс современным

Не количество эффектов, а согласованность пространственных переходов: выбранная строка остаётся на месте; карточка открывается поверх списка; подсветка объясняет выбранную область; данные читаются до взаимодействия. Мягкая глубина есть у overlay, а рабочие таблицы сохраняют ясные разделители. Цветная иконка помогает распознать раздел, цвет статуса имеет отдельный смысл.

Паттерны V3: компактный portfolio switcher; сравнительные полосы проектов; сравнение за фиксированный период; состав токенов и отдельный `tool_use`; список очереди с ответственными; карточка агента с drill-down; большая task dialog с локальным scroll; сегментированный выбор Graph/Mermaid/List; фильтр модуля; zoom/fit/reset; таблица данных рядом с графиком; синтетическая/недоступная аналитика как разные состояния.

## Motion contract

| Событие | Предложенное поведение | Сокращённое движение |
| --- | --- | --- |
| Смена рабочей поверхности | opacity + translateY до 6px, около 160–220ms | Мгновенная замена, фокус сохраняется |
| Открытие task dialog | Затемнение фона и небольшой translate/scale, около 180–240ms | Статичный overlay без масштабирования |
| Выбор вкладки/фильтра | Локальная подсветка и короткая смена содержимого | Только выбранное состояние |
| Loading | Skeleton повторяет итоговую геометрию, без ложного процента | Статичный skeleton и aria-busy |
| Подтверждение | Текстовый receipt/toast, локальная обратная связь | Тот же текст сразу |
| Граф | Раскладка стабилизируется; движение только при zoom/выборе | Доступны кнопки и список; без фонового дрейфа |

Эти длительности — наша спецификация для проверки макета, не измерения bb/Ratio. Не применяем scroll hijacking, магнитные кнопки для важных действий, бесконечный glow, spring на текстовых таблицах, анимирование width/height/top/left, счётчики с выдуманным ростом. Hover не скрывает важные значения. Опасные действия сохраняют отдельное подтверждение; анимация не заменяет preview или guard.

## Визуализации и технический контракт

| Слой | Вопрос | Представление и единицы | Проверка |
| --- | --- | --- | --- |
| Portfolio | Где осталась работа и расход? | Список проектов + горизонтальные полосы, задачи/токены/демо USD/tool_use отдельно | Общий итог равен сумме уникальных leaf records |
| Проект | Как движется работа, что следующее? | Прогресс done/весь scope; состав состояний; очередь + нагрузка | Cancelled не выдаётся за completed, неизвестная оценка не ноль |
| Агенты | Кто занят и с каким результатом? | Сравнение запусков/исходов, отдельный агент и его задачи | Учитывается период и coverage; shared run не суммируется дважды |
| Задача | На что ушёл расход? | Input/output/cache, tool_use и стоимость в отдельных блоках | Cached input — часть input, не повторный вклад в total |
| Карта | Как связаны части? | D3 node-link + Mermaid whole/module + список | Общий fixture graph, стабильные IDs, фильтр и выбранный узел |

Основной renderer SVG: масштабы и подписи важнее плотности точек. До трёх небольших диаграмм на аналитическом экране; небольшой фиксированный граф. Canvas/WebGL и 3D здесь увеличили бы стоимость без полезной дополнительной информации. Оси сравнения начинаются с нуля, нет двойной Y-оси; обязательны подписи, единицы и альтернативная таблица. Цвет не единственный канал.

Данные — детерминированный synthetic snapshot. Ни polling, ни provider вызовов. URL хранит выбранный экран и тему; фильтры макета имеют ограниченный локальный жизненный цикл. Нет обещания server persistence. Будущая интеграция требует периода, snapshot revision, coverage и updatedAt; stale данные должны оставаться видимыми с предупреждением, неизвестное значение — `—`, а не 0.

## Установленные зависимости

| Пакет | Версия | Назначение | Лицензия |
| --- | --- | --- | --- |
| gsap | 3.15.1 | Переходы и dialog | [GSAP Standard no-charge](https://gsap.com/community/standard-license/), не MIT библиотеки |
| d3 | 7.9.2 | Графики, graph layout/zoom | ISC |
| @mermaid-js/tiny | 12.3.0 | Mermaid SVG, без ELK | MIT |
| @iconify-json/duo-icons | 1.2.2 | Локальные SVG, upstream icons 1.1.4 | MIT |
| esbuild | 0.28.2 | Только сборка локального bundle | MIT |

Установка: `npm install --ignore-scripts --no-fund --no-audit` в этой папке; 44 packages, exit 0. Это не npm audit и не проверка безопасности всего supply chain. Node v26.5.0 удовлетворяет требованию Mermaid >=22.12.0. Версии и integrity закреплены в package-lock.json. Bundle 3 263 203 bytes до UI-кода — приемлем для локального альбома; перед внедрением в приложение необходимы выборочные imports, lazy loading Mermaid и измерение бюджета. `vendor/THIRD-PARTY-NOTICES.txt` сохраняет установленные license notices. Прототип не требует CDN или node_modules для просмотра.

## Skills и границы

Sidebar collapse, 13.11.2026: перед чтением кода альбома прочитаны [index.html](https://designbookmark.com/motion-src/sidebar-collapse/index.html), [side.css](https://designbookmark.com/motion-src/sidebar-collapse/side.css), [side.js](https://designbookmark.com/motion-src/sidebar-collapse/side.js), shared [tokens.css](https://designbookmark.com/motion-src/shared/tokens.css), [base.css](https://designbookmark.com/motion-src/shared/base.css), [motion.js](https://designbookmark.com/motion-src/shared/motion.js). Built-in web open вернул unavailable; машинные исходники получены bounded GET-only Python wrapper без credentials. Значения width 260/24 совпадают с shared spring-soft; rotation 300/22, highlight 380/28 и labels 300/26 заданы в side.js. Адаптация сохраняет unit mass, четыре Euler substeps и dt cap 1/30. Width 212→64 заменена на 216→64 под имеющуюся сетку PAOS. Цвета, шрифт и radius — существующие product tokens. Добавлены отмена старых задержек при быстром переключении, остановка rAF после settling, прямое переключение reduced motion, tooltip и scroll к клавиатурному фокусу. Demo autoplay, remote font, analytics beacon, parent messages и чужой theme storage не перенесены. Это локальная адаптация для review; глобальный shared CSS не подключён, лицензия каталога не объявляется лицензией всех компонентов.

Hallmark — композиция, токены, desktop craft; UI/UX Pro Max — формы, focus, плотность; Build Web Data Visualization → dashboards/D3/node-link — смысл графиков, данные и доступность; official GSAP core/performance — анимации. Правило Hallmark о ручном SVG уступает прямому запросу пользователя на D3. Мобильный scope исключён пользователем. Отдельный агент проверяет source inventory, отдельный владеет UI; root — зависимости, документы и проверка. Fresh review выполняется после первого рендера.
