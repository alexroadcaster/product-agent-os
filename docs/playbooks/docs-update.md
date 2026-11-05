# Playbook: обновление документации

Source status: `official + experiment`

Источники: [официальная документация](https://learn.chatgpt.com/docs), [AGENTS discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Цель и входы

Изменение официального source или поведения проекта, список affected pages, действующие project rules и разрешённый scope. Изменяйте только подтверждённые claims; недоступный source остаётся явным пробелом. Research report не является автоматически разрешением на реализацию или публикацию.

## Procedure

1. Прочитайте owning source и обе языковые версии. Отделите current guide от dated archive.
2. Проверьте официальный claim для product/client/version/auth. В registry обновите URL, claim scope и `checked_at` только для реально проверенного материала.
3. Исправьте RU/EN вместе: commands, identifiers, permissions, prerequisites, results и limitations должны совпадать по смыслу.
4. Сохраните history. Уточните даты и current pointers; не переименовывайте code tokens при переводе.
5. Выполните docs contract checks и `git diff --check`.
6. Если scope включает nav, Mermaid, MkDocs config или generated output, выполните разрешённый strict build в owning `site_dir`.
7. Сравните expected routes с generated HTML, затем links/anchors, search и language switching. Для диаграмм нужен parse/render check; build exit 0 сам по себе не доказывает render.
8. Запишите current evidence, изменённые страницы, пропуски и границу публикации.

## Documentation closure order

Source docs → registry RU/EN → docs tests → `check_docs.py` → applicable strict MkDocs → links/diagrams → optional full closure при implementation changes.

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools/check_docs.py
git diff --check
# При разрешённом site/nav/diagram scope:
.venv-docs/Scripts/python.exe -m mkdocs build --strict
```

Не устанавливайте dependencies автоматически. Полный plugin/runtime suite нужен только при изменении соответствующего поведения. Browser/server, provider calls, Git и публикация остаются отдельными действиями; используйте уже предоставленную точную authority без повторного запроса.

## Prompt

```text
Обнови затронутые страницы по текущим официальным источникам.
Синхронизируй RU/EN и registry; сохрани историю и canonical identifiers.
Выполни обязательные docs checks.
Пересобери site только если это входит в разрешённый scope.
При сборке проверь expected routes, links/anchors и диаграммы.
Верни изменения, evidence и оставшиеся ограничения; не публикуй.
```

## Результат и типовые ошибки

Результат: обновлённые guides/registry и датированные проверки. Ошибки: обновить дату без source review; проверить только существующие links и пропустить missing new routes; считать generated view источником истины; объявить runtime activation по текстовым правкам.

## Проверка

Выполните применимые команды выше и проверьте generated output перед итогом.

## Риски

Неподтверждённые claims, устаревшая сборка и отсутствующие routes остаются явными пробелами до проверки.
