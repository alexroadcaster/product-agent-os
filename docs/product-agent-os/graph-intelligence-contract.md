# Graph intelligence contract

Source status: `project evidence`

Graph intelligence помогает ориентироваться в проекте, но остается generated orientation evidence. Этот слой не заменяет чтение source files, tests, checked-in docs, approval records или owner decisions.

## Контракт слоя

| Сигнал | Роль | Граница |
| --- | --- | --- |
| Ontology | Типы nodes, edges, observations, contracts и semantic overlays. | Не гарантирует runtime behavior. |
| Coverage map | Какие языки, docs, schemas и tests попали в scanner. | Не доказывает полноту проекта. |
| Freshness | Digest, timestamp, changed-since и supersession metadata. | Stale graph блокирует readiness wording. |
| Rejected links | Ledger консервативно отклоненных edges. | Rejection является evidence осторожности, не failure само по себе. |
| Query packets | Bounded `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `read_order`, `hotspots`, `status`, `search`. | Query result не заменяет source read. |

## Safe Use

Используйте graph для выбора файлов к чтению, оценки blast radius, поиска hotspots и подготовки handoff. Перед edit, fix, readiness или release claim нужно открыть owning source и запустить текущий verification gate.

## Unsafe Use

Нельзя делать mutation, provider call, browser proof, target apply или git action из graph evidence alone. Нельзя повышать `present_unverified` до `present_verified`, если нет command evidence, owner review или accepted gap.

## Freshness Gates

Graph считается stale, если source files изменились после generation, manifest digest не совпадает, query packet не связан с текущим graph или baseline comparison показывает нерассмотренные deltas. В таком случае next safe action: refresh generated graph only with approved/local scope or read source directly.

## Проверка

Минимальный docs gate для этой страницы: source registry marker, docs tests, `tools/check_docs.py`, strict MkDocs smoke и `git diff --check`. Focused graph tests нужны только если меняется scanner, ontology или query code.

