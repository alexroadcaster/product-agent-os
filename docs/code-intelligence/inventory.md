# Inventory и границы сканирования

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: graph-cockpit-engineer + docs-maintainer. Область: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении scanner, API, adapters, query contracts, тестов или статуса PoC. Результаты графа — производное evidence для навигации, не замена чтению исходников и проверкам.

## Web source inventory

[sources.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/sources.mts) проверяет identity зарегистрированного root и его предков; исключает чувствительные каталоги/пути, symlinks и файлы с несколькими hard links, контролирует UTF-8, drift и root containment. Обход ограничен глубиной 32, 10 000 directory entries и 1000 подходящими файлами. Это ограниченный source inventory, а не видимое дерево всех файлов или универсальная обработка ignore-файлов.

Graph [service.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/service.mts) ограничивает общий размер 8 MiB, один файл 512 KiB, 25 000 nodes, 50 000 edges и работу parser worker 10 сек; до восьми snapshots. Подходящие для inventory другие языки получают coverage `unsupported`; связанные источники могут быть `excluded`. Достижение hard limit вызывает ошибку, а не гарантирует безопасное полное усечение до лимита.

## Python manifest

[project_graph_manifest.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_manifest.py) формирует normalized file records, размер, fingerprints, language и generated flags; [project_code_graph.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_code_graph.py) использует их для графа. Сбор по умолчанию ограничен 10 000 файлами и записывает truncation/omitted counts. Конкретные исключения и policy следует читать у scanner: Web и Python не обещают одинаковый inventory. Каталог generated может быть отражён в manifest без семантического overlay.

Сравнивайте revision/manifest, coverage и сообщения об ошибках до использования индекса. Лимиты, encoding, пропущенные пути и drift должны оставаться видимыми; результаты не являются аудитом всех файлов проекта. F26–F29 планируют самостоятельную файловую директорию и управляемое сканирование.

Проверки: [Web source tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [manifest tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_manifest.py). Нового runtime-прогона этот текст не заявляет.
