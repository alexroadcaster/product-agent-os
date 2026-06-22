# Local HTML interaction boundary

Source status: `project evidence`

Generated HTML может иметь локальные tabs, search, filters, diagrams и disclosure controls. Эти interactions допустимы только как offline review surface и не являются runtime/browser proof без отдельного approved evidence packet.

## Разрешенные interactions

| Interaction | Условие |
| --- | --- |
| Tabs и section navigation | Работают внутри одного generated file и не скрывают claim ceilings. |
| Search/filter | Ищут только по embedded data, без network requests. |
| Diagram controls | Используют local/vendor assets или static fallback. |
| Copy/open helpers | Не мутируют files, не запускают shell и не отправляют data. |
| JS-disabled fallback | Основная информация остается читаемой без script execution. |

## Запрещенные interactions

- External fetch, provider/API call, telemetry или beacon.
- File mutation, cleanup execution, shell command или target apply.
- Скрытие unsupported claims, stale warnings или approval boundaries.
- Browser proof wording без approved browser run, screenshots, console/network evidence и viewport notes.

## Browser-proof packet

Если owner одобряет browser proof, evidence должен назвать URL/path, tool, viewport set, console errors, network requests, screenshots, source-boundary labels, mobile overflow status, JS-disabled fallback и cleanup. Без такого packet статус остается `static_docs_only`.

## Проверка

Для docs slice достаточно static docs checks и strict MkDocs smoke. Real browser automation, screenshots, WCAG proof, visual regression и external network checks остаются approval-required.

