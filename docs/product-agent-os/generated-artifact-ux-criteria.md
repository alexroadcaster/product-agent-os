# Критерии качества generated artifacts

Source status: `project evidence`

Эта страница задает критерии приемки для локальных HTML, JSON и report-артефактов Product-Agent OS. Она не доказывает, что конкретный файл уже принят: приемка требует текущего evidence, owner review или явно принятого gap.

## Что считать пригодным

| Область | Требование | Что не следует заявлять |
| --- | --- | --- |
| Навигация | Главный путь чтения, видимый раздел риска, ссылки на owning source и безопасный следующий шаг. | Что artifact заменяет source files или review. |
| Читаемость | Плотные таблицы должны иметь короткие заголовки, устойчивые колонки и понятные пустые состояния. | Что HTML уже public-ready без текущей проверки. |
| Offline | Артефакт должен работать без внешних URL, внешних scripts и provider calls. | Что browser proof выполнен без отдельного evidence. |
| Печать | Print output должен сохранять заголовки, claim ceilings и evidence refs. | Что printable view является release artifact. |
| Язык claims | `ready`, `fixed`, `verified`, `complete` и `release-ready` разрешены только при текущем command/runtime/eval evidence или accepted gap. | Что generated view сам по себе является proof. |

## Vale и language guard

Локальный Vale сейчас advisory. Его warnings помогают найти readiness wording, но не являются автоматическим блокером до owner-approved threshold, report retention policy и rollback path.

## Storybook trigger

Storybook остается deferred. Его можно пересмотреть только если появится компонентная surface, повторяемые visual states, owner-approved install path и browser/visual evidence plan. До этого generated artifact UX проверяется через docs tests, static HTML checks и ручной owner review.

## Acceptance checklist

- `generated_view_policy` явно говорит `orientation_only_not_proof`.
- Есть source-boundary label и список unsupported claims.
- Виден next safe action, а не скрытая mutation recommendation.
- Нет raw private chat logs, secrets, credentials, unredacted PII или raw source bodies.
- Cleanup guidance помечен как preview-only.
- Browser, runtime, provider, target mutation, release и publication claims отсутствуют без отдельного approval.

## Проверка

Минимальный gate для docs slice: docs unittest, `tools/check_docs.py`, strict MkDocs smoke в `.docs-tools/reports`, JSON packet validation и `git diff --check`. Browser proof, screenshots, broad Vale enforcement и Storybook остаются approval-required.

