# Privacy, Supply-Chain, And Report Retention

Source status: `project evidence`

This page defines the storage boundary for source, installed cache, active session, supply-chain reports, and raw findings. It does not authorize cache refresh, dependency remediation, full SBOM, vulnerability audit, or report retention.

## Storable Evidence

| Data | Allowed form | Forbidden form |
| --- | --- | --- |
| Source/cache/session | Counts, filenames, versions, hashes, exposure status, unsupported claims. | Raw private source bodies or private chat logs. |
| Synthetic fixtures | Synthetic names, bounded snippets, redacted paths. | Customer data, secrets, credentials, tokens, unredacted PII. |
| Dependency evidence | Package names, versions, advisory counts, `pip check`, scoped SBOM summary. | Remediation claim without command evidence and rollback. |
| Raw findings | Summary with severity, owner, redaction, and retention decision. | Retained raw scanner output without approval. |

## Approval Boundaries

Python vulnerability audit, complete repository SBOM, dependency remediation, `npm audit fix`, broad secret/link scans, external URL crawling, and raw report retention require separate approval. Each action must name scope, command, output path, retention policy, redaction policy, owner, and rollback.

## Distribution Labels

For local-only/internal R&D, use compact summaries and redacted evidence. Public/team trust labels should not be added automatically: they require owner decision and source registry update.

## Report Retention

If a report contains raw findings, local paths, dependency advisory details, or private target names, the default state is `not_retained`. Retaining a report needs an owner-approved retention window, redaction status, and cleanup path.

## Verification

This docs slice verifies only the documented boundary: docs unittest, `tools/check_docs.py`, JSON packet validation, strict MkDocs smoke, and `git diff --check`. It does not run vulnerability audit, SBOM completion, remediation, or external crawling.

## Current retained-data boundaries

Review after plugin script changes is a separate trust check. Local memory stores and cloud network secrets have different retention/delivery semantics; do not promise universal deletion or setup-only credential access. See [hooks](../runtime/worktrees-hooks-rules.md), [memory](../agent-systems/memory.md), [Cloud](../codex/surfaces.md).
