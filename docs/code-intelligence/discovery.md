# Discovery и first-run анализ

Source status: repository_source / focused_synthetic_verification; 15.11.2026. Browser/API integration подтверждает владелец FUNC-G03 отдельно.

Владелец: graph-cockpit-engineer + docs-maintainer. Область: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении scanner, API, adapters, query contracts, тестов или статуса PoC. Результаты графа — производное evidence для навигации, не замена чтению исходников и проверкам.

## Python: обследование workspace

[discovery.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/discovery.py) обнаруживает stack markers, control-plane files, Codex assets и evidence gaps; [first_run_analysis.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py) собирает ориентирующие результаты первого запуска. Наличие файла или профиля не равно его активации или корректной работе: статусы различают missing, present_unverified, present_verified, proposal_staged и approval_required. Решение и evidence принадлежат source и владельцу, не dashboard.

## Web: регистрация и ограниченный scan

Регистрация проекта и durable scan имеют разные результаты: scan ставится в очередь, сохраняет стадии inventory → documents → code → analysis и отдельно последний пригодный результат. Отмена и restart требуют явного повтора; частичное покрытие не означает полный проектный inventory. Индекс кода и Python analysis независимы: готовый индекс не доказывает завершение анализа. Подробности — [inventory](inventory.md) и [lifecycle](../backend/lifecycle.md).

## F29: Python analysis через безопасную проекцию

Адаптер `apps/local-service/src/project-analysis/service.mts` использует существующий `product_agent_os.discovery.analyze_workspace`. Он не вызывает `run_first_project_analysis`: тот orchestration path включает script matrix даже при отсутствии записи результатов. Вход адаптера — зарегистрированный проект и снимок F28 inventory, а не произвольный абсолютный путь из браузера.

Адаптер создаёт отдельную временную проекцию: до 200 допустимых файлов, до 2 MiB текста, до 64 KiB на текстовый файл. Безопасные корневые markers/control-plane files и plugin manifests читаются только через проверенный F28 read; для языков, ORM и схем используются пустые placeholders с исходными относительными путями. Sensitive content не переносится и отмечается как пропуск. Файлы SQLite/DB представлены только допустимыми метаданными; они не открываются. Пропуск или `not_observed` не доказывает отсутствия файла в проекте.

Фиксированный `bridge.py` запускается через Python 3.11+ с `-I -S -B`, `shell:false`, `windowsHide:true`, разрешёнными переменными окружения и отдельным рабочим каталогом. Ни project scripts, ни target Python/config modules не импортируются. Изолированный режим исключает cwd/user-site и `PYTHON*`, а `-S` отключает обработку site; описание флагов проверено через Context7 по [официальному Python cmdline reference](https://github.com/python/cpython/blob/v3.13.14/Doc/using/cmdline.rst). Это ограничение входа, а не OS sandbox для недоверенного Python core.

Время ограничено 15 s, суммарный stdout/stderr — 128 KiB. При отмене/таймауте прекращается только собственный subprocess; cleanup удаляет только созданную адаптером временную папку. Объём проекции и вывода ограничен, но отдельного OS RSS limit нет (`SUBPROCESS_RSS_NOT_OS_LIMITED`). Root identity, policy, inventory revision и publication guard проверяются до/после работы; устаревший или отменённый результат не публикуется. Traceback и абсолютные временные пути не передаются UI.

Контракт `paos_project_analysis_v1` хранится в `scan.latest.stages.analysis.data.analysis`; отдельной таблицы или namespace нет. Он содержит stack/language/component observations, control plane, findings, schema candidates, confidence, source paths с `line:null`, ограничения и revision. `sourceRevision` относится к inventory. `adapterSourceRevision` — SHA256 фиксированного списка bridge/core/direct dependencies/catalog; `runtime` фиксирует фактическую версию Python, модуль и deployment `checkout_projection`. Наблюдения по имени файла остаются candidates, не runtime verification. Database navigation недоступна без отдельного соединения.

Checkout lookup использует только core рядом с приложением. Текущий desktop distribution не включает plugin core/catalog: такая установка явно возвращает `ANALYSIS_CORE_UNAVAILABLE`, без установки зависимостей, поиска в глобальных каталогах или альтернативного анализатора. Упаковка core — отдельная задача.

Focused synthetic checks: `node --test tests/web/project-analysis.test.mts` (9/9), включая реальный Python/core, вложенный plugin manifest, missing runtime/core, таймаут, переполнение/ошибку вывода, отмену, изменение root/policy/source и сохранность target bytes. Receipt: `.tmp/func-g03/f29-service-green.log`. Отдельный RED показал потерю вложенного manifest source; GREEN подтвердил исправление. UI component проходит scoped TypeScript check; browser integration и итоговые статусы принадлежат root. Эти проверки не доказывают production readiness или human acceptance.

## Операционные границы

Discovery может перечислить доступные признаки, но не запускает неизвестные project scripts и не доказывает runtime, зависимости или готовность. Staged graph и cockpit — generated evidence. Перед выводами перечитайте текущие исходники; не используйте output как разрешение на target mutation или provider calls.

Связанные проверки: [discovery tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_discovery.py), [first-run tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_first_run_analysis.py). Ссылки не означают новый прогон.

## FUNC-G03 — итоговая проверка

Текущий интегрированный source, после первоначального lower-module handoff: browser19/19; полный Web594/594,0skip; backend TypeScript и production build прошли. Source/build hashes и screenshots: `.tmp/func-g03/browser-final/evidence-IfLiEa/result.json`. Policy-race findings исправлены и независимо перепроверены5/5. Native candidate и production-default receipts: `.tmp/func-g03/native-candidate-reviewed.log`, `native-default-reviewed.log`. Прежние pending/wiring формулировки описывают датированный промежуточный slice; закрытием владеют итоговые task reports. Checkout core доступен; packaged core явно unavailable. Human/provider acceptance и F14/F33/F34 отдельно.
