# Frontend: дизайн, темы и локализация

Source status: repository_source / static_source_review; 15.11.2026.

Владелец: frontend owner и design owner. Область: применение V3 в Web UI на revision `ad78d5d15aced23febae90d319f2aba00bd64d0b`. Обновлять при изменении утверждённого дизайна, preference contracts, CSS или проверки реализации.

## Где находится источник дизайна

[DESIGN.md](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/DESIGN.md) и [V3 design assets](https://github.com/alexroadcaster/product-agent-os/tree/ad78d5d15aced23febae90d319f2aba00bd64d0b/design/2026-11-13-v3) владеют направлением, визуальными материалами и картой полей. Эта страница маршрутизирует к реализации, а не копирует токены или скриншоты. [Implementation evidence](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/design/2026-11-13-v3/implementation-evidence.md) датировано 13.11.2026 и сообщает локальные проверки и `needs_user_acceptance`; оно не является новой приёмкой DG04.

## Применение

[main.tsx](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/main.tsx) подключает `theme.css`, `app.css`, `workspace.css`, `parity.css`. [theme.css](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/design/theme.css) определяет семантические CSS variables для Porcelain/Obsidian и focus; остальные таблицы и feature CSS применяют их к конкретным поверхностям. При изменении компонента сначала проверяйте существующие tokens и стили, визуальный образец, состояния loading/empty/error/disabled и обе темы; изменять значения следует в исходном владельце, а не в копии документации.

В [preferences.ts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/design/preferences.ts) поддерживаются `ru`/`en` и `light`/`dark`/`system`; недопустимые либо отсутствующие сохранённые значения отдельно возвращаются к `ru` и `system`. Применение устанавливает `lang` и разрешённый `data-theme` у корневого элемента; System следует текущему OS color scheme. [preference-controls.ts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/design/preference-controls.ts) различает черновик и применённые настройки: применённое значение меняется после успешной записи через local service; ошибка не объявляет сохранение успешным.

[messages.ts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/locales/messages.ts) и [app.ts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/locales/app.ts), а также локализованные строки компонентов содержат подписи интерфейса. Имена, текст, пути и технические идентификаторы пользователя не переводятся автоматически. При добавлении UI-текста проверить обе локали и доступное имя, сохраняя schema keys и коды ошибок.

## Motion и графика

[Sidebar](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/Sidebar.tsx) использует локальный `requestAnimationFrame` для движения и при `prefers-reduced-motion` переключает состояние без анимации; `App` использует GSAP для входа при разрешённом motion. [GraphViews](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/graph/GraphViews.tsx) содержит D3 и ленивую загрузку локального Mermaid, который получает активную тему. Сам факт наличия библиотеки не доказывает render на конкретном устройстве.

Связанные проверки: [theme-locale.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/theme-locale.test.mts), [ui-v3-diagram.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-v3-diagram.test.mts); ссылки не означают новый прогон. [Доступность](accessibility.md) описывает исторический охват, человеческие проверки и ограничения. Запланированные Files/Map/Database/usages F26–F34 не следует считать реализованными по дизайну.
