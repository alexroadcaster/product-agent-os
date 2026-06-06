# Playbook: обновление документации

Source status: `official + experiment`  
Источники: [Codex changelog](https://developers.openai.com/codex/changelog), [Codex workflows](https://developers.openai.com/codex/workflows).

## Цель

Поддерживать базу знаний актуальной при изменениях Codex, Agents SDK и связанных workflows.

## Trigger

- Новая запись в Codex changelog.
- Изменение официальной страницы.
- Новый verified insight.
- Пользователь просит обновить раздел.

## Procedure

1. Откройте `docs/sources/registry.md`.
2. Найдите source cards, связанные с темой.
3. Сверьте официальные страницы.
4. Обновите `checked_at`.
5. Измените только затронутые разделы.
6. Если появляется новая спорная практика, добавьте insight card, а не основную инструкцию.
7. Запустите:

```powershell
python tools/check_docs.py
python -m mkdocs build --strict
```

## Documentation closure order

Для Product-Agent OS docs closure используйте порядок: source docs -> registry -> docs tests -> `check_docs.py` -> strict MkDocs -> optional full closure. Этот порядок нужен, чтобы source-backed claims, navigation, generated site и final package evidence не расходились.

| Step | Что проверить |
| --- | --- |
| Исходные docs | Обновлены только затронутые страницы, каждая non-index page имеет `Source status:`. |
| Registry | Новые или измененные source-backed claims отражены в `docs/sources/registry.md`. |
| Тесты docs | Сфокусированные проверки покрывают новые required pages, route terms или правила структуры. |
| `check_docs.py` | Structure checks pass до claiming documentation closure. |
| Strict MkDocs | Запускается, когда могут измениться nav, MkDocs config, Mermaid, Markdown extensions или generated site. |
| Опциональная полная closure | Full unittest/fixture/transcript/compatibility/diff checks нужны только при изменении plugin contracts или route logic. |

Docs closure не запускает live server, browser automation, provider calls, canonical graph mutation или git stage/commit/push/PR. Пересобирайте `site/` только в dedicated site/nav slice или когда пользователь явно просит для generated HTML output.

## Prompt

```text
Обнови раздел "{section}" по официальным источникам.

Constraints:
- Official docs являются source of truth.
- Update source registry checked_at values для touched sources.
- Put community claims в docs/insights/.
- Keep Russian prose и English OpenAI terms.

Verification:
- Запустите python tools/check_docs.py.
- Запустите python -m mkdocs build --strict.
```

## Выход

Итоговый отчет должен содержать:

- измененные файлы;
- источники;
- что устарело;
- что добавлено;
- команды проверки и их результат.
