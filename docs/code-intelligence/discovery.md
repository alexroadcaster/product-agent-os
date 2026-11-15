# Discovery и first-run анализ

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: graph-cockpit-engineer + docs-maintainer. Область: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении scanner, API, adapters, query contracts, тестов или статуса PoC. Результаты графа — производное evidence для навигации, не замена чтению исходников и проверкам.

## Python: обследование workspace

[discovery.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/discovery.py) обнаруживает stack markers, control-plane files, Codex assets и evidence gaps; [first_run_analysis.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py) собирает ориентирующие результаты первого запуска. Наличие файла или профиля не равно его активации или корректной работе: статусы различают missing, present_unverified, present_verified, proposal_staged и approval_required. Решение и evidence принадлежат source и владельцу, не dashboard.

## Web: регистрация и ограниченный scan

[HTTP application](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/http/application.mts) при регистрации проекта с scan вызывает inspection sources и [code index service](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/service.mts). Регистрация и scan — разные результаты: ошибки и partial coverage не делают полный проектный inventory. После restart snapshot памяти требуется rebuild. Подробности ограничений и связи с F26–F29 — [inventory](inventory.md).

## Операционные границы

Discovery может перечислить доступные признаки, но не запускает неизвестные project scripts и не доказывает runtime, зависимости или готовность. Staged graph и cockpit — generated evidence. Перед выводами перечитайте текущие исходники; не используйте output как разрешение на target mutation или provider calls.

Связанные проверки: [discovery tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_discovery.py), [first-run tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_first_run_analysis.py). Ссылки не означают новый прогон.
