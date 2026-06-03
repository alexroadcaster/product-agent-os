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
| Source docs | Обновлены только затронутые pages, каждая non-index page имеет `Source status:`. |
| Registry | Новые или измененные source-backed claims отражены в `docs/sources/registry.md`. |
| Docs tests | Focused tests покрывают новые required pages, route terms or structure rules. |
| `check_docs.py` | Structure checks pass before claiming documentation closure. |
| Strict MkDocs | Run when nav, MkDocs config, Mermaid, Markdown extensions or generated site may change. |
| Optional full closure | Full unittest/fixture/transcript/compatibility/diff checks only when plugin contracts or route logic changed. |

Docs closure does not launch a live server, run browser automation, call providers, mutate canonical graph, or perform git stage/commit/push/PR. Rebuild `site/` only in the dedicated site/nav slice or when the user explicitly asks for generated HTML output.

## Prompt

```text
Обнови раздел "{section}" по официальным источникам.

Constraints:
- Official docs are source of truth.
- Update source registry checked_at values for touched sources.
- Put community claims into docs/insights/.
- Keep Russian prose and English OpenAI terms.

Verification:
- Run python tools/check_docs.py.
- Run python -m mkdocs build --strict.
```

## Output

Итоговый отчет должен содержать:

- измененные файлы;
- источники;
- что устарело;
- что добавлено;
- команды проверки и их результат.
