# Privacy, supply-chain and report retention

Source status: `project evidence`

Эта страница задает границу хранения evidence для source, installed cache, active session, supply-chain reports и raw findings. Она не разрешает cache refresh, dependency remediation, full SBOM, vulnerability audit или report retention.

## Что можно хранить

| Данные | Разрешенный вид | Запрещенный вид |
| --- | --- | --- |
| Source/cache/session | Counts, filenames, versions, hashes, exposure status, unsupported claims. | Raw private source bodies или private chat logs. |
| Synthetic fixtures | Synthetic names, bounded snippets, redacted paths. | Customer data, secrets, credentials, tokens, unredacted PII. |
| Dependency evidence | Package names, versions, advisory counts, `pip check`, scoped SBOM summary. | Remediation claim без command evidence и rollback. |
| Raw findings | Summary with severity, owner, redaction and retention decision. | Retained raw scanner output without approval. |

## Approval Boundaries

Python vulnerability audit, complete repository SBOM, dependency remediation, `npm audit fix`, broad secret/link scans, external URL crawling and raw report retention требуют отдельного approval. Каждый action должен назвать scope, command, output path, retention policy, redaction policy, owner и rollback.

## Distribution Labels

Для local-only/internal R&D используйте короткие summaries и redacted evidence. Public/team trust labels не следует добавлять автоматически: они требуют owner decision и source registry update.

## Report Retention

Если report содержит raw findings, local paths, dependency advisory details или private target names, default state: `not_retained`. Чтобы сохранить report, нужен owner-approved retention window, redaction status и cleanup path.

## Проверка

Docs slice проверяет только documented boundary: docs unittest, `tools/check_docs.py`, JSON packet validation, strict MkDocs smoke и `git diff --check`. Он не выполняет vulnerability audit, SBOM completion, remediation или external crawl.

## Актуальные retained-data границы

Review после изменения plugin scripts — отдельная trust проверка. Local memory stores и cloud network secrets имеют разные retention/delivery semantics; не обещайте универсальное удаление или setup-only credential access. [Hooks](../runtime/worktrees-hooks-rules.md), [memory](../agent-systems/memory.md), [Cloud](../codex/surfaces.md).
