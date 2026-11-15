# Проверки документации и сайта

Source status: repository_source / static_contract_review; DG06, 2026-11-15.

Владелец: docs-maintainer + verification owner. Scope/version: repository `259977f3b257ba7fc0e932396f8963262bd327ad`. Обновлять при изменении routing, MkDocs или тестов локализации. [TEST.md](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/TEST.md) остаётся владельцем актуальных команд и расширения проверок; [check_docs.py](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tools/check_docs.py) и [site_checks.py](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/product_agent_os/site_checks.py) — источники исполнения. Ниже маршрут, а не результат текущего запуска.

## От source к preview

1. Сверить изменённые утверждения с владельцами исходников и ревизией; проверить Source status, владельца, ограничения, RU/EN смысл и source links. Для отдельных Markdown использовать `python -B tools/check_docs.py --paths <changed-files>`; `--paths` не проверяет site/archive.
2. Для изменённой матрицы выполнить `python -B plugins/product-agent-os/scripts/validate_task_matrix.py <changed-plan>` для каждого затронутого языка, сверить ID, зависимости, AC и сохранность связанных данных. Для затронутого общего контракта source docs выбрать соответствующий unittest по TEST. `git diff --check` выявляет ошибки whitespace в tracked diff; новые файлы проверяйте отдельно.
3. При изменении nav, i18n, search/sitemap или иных site-sensitive частей выполнить strict MkDocs в отдельный output через установленное project-local окружение, не продвигая `site/`. Например, для имеющегося окружения: `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir <isolated-output>`. Ошибки и warnings не скрывать; установка зависимостей имеет отдельную границу разрешений.
4. Для локальных file-ссылок выполнить project script `tools/fix_site_i18n_links.ps1 -SiteDir <isolated-output>`, затем указать `PAOS_DOCS_SITE_DIR` на этот output и запустить `python -B -m unittest tests.product_agent_os.site_checks -q`. Site tests проверяют свои перечисленные страницы, language switch, search и sitemap; для новых страниц отдельно проверьте новые RU/EN routes, ссылки и якоря. Browser/render нужен, когда затронуто отображение или взаимодействие.
5. Записать точные commands, exit codes, warnings, output path, revision, ограничения и проверенные маршруты в owning evidence. Сайт старого run или root `site/` не является evidence нового preview. Проверки не дают права на публикацию.

## Failure triage

Различайте baseline и текущий запуск: сохраните первый failure и его условия, определите, источник ли проблемы в изменённых документах, устаревшем ожидании или среде; исправляйте доказанную причину и запускайте затронутый gate заново. Не отключайте checks, не подменяйте содержательный перевод заглушкой и не меняйте trust ради passing результата. Несвязанный дефект фиксируется отдельно; обязательный непройденный gate ограничивает closure.

Для переноса DG01 этап DOCS-13/A выполнил repair и сохранил исторические initial failures и retest от 15.11.2026 в [DG01 results](../planning/documentation-architecture-2026-11-15.md#dg01-results). Его receipt не является новым прогоном DG06. Родитель DOCS-13 закрывается после B и текущих применимых проверок исходных AC. Точный объём и результаты текущего запуска принадлежат [плану документации](../planning/documentation-architecture-2026-11-15.md), а не этой общей инструкции.
