# Residual follow-up and site freshness

Source status: `project evidence`

Эта страница закрывает G5 residual routing: какие G1.1 follow-ups остаются approval-required, как summarise real-target static comparison без раскрытия private targets и почему final `DOC-M25` не выполняется автоматически.

## Residual Routing

| Residual | Owning row | Current state |
| --- | --- | --- |
| Root `site`, search и sitemap freshness | `DOC-M25` | `approval_required_not_run` после G2-G5 source updates. |
| Browser Mermaid/HTML proof | `DOC-M08`, `DOC-M23`, `DOC-M29` | Approval-required; static smoke не доказывает browser rendering. |
| Broad lint/format/Vale enforcement | `DOC-M21`, `DOC-M26`, `DOC-M30` | Advisory или scoped-only до owner thresholds. |
| Link/secret scans и raw report retention | `DOC-M24`, `DOC-M30` | Не запускать broad scans и не хранить raw reports без approval. |
| Python audit, full SBOM, Node remediation | `DOC-M24`, `DOC-M30` | Не заявлять remediation или complete SBOM без commands и rollback. |
| Docusaurus, Storybook, Structurizr | `DOC-M21`, `DOC-M30` | Deferred trigger governance; no install. |

## Static Comparison Summary

Для private или real-target comparison храните только redacted target class, run ids, digest deltas, page/key deltas, unsupported claims preserved, actions performed и explicit no-unapproved-actions. Не публикуйте target names, raw paths, private screenshots, raw source excerpts или private data.

## Final `DOC-M25`

Final `DOC-M25` может rebuild root `site` только после отдельного approval. До этого source docs могут быть current, а generated `site`, search index и sitemap остаются stale/unsupported для новых G2-G5 pages.

## DOC-M25 Closure Update

`DOC-M25` закрыт через `documentation_refresh_DOC-M25-A01` со статусом `implemented_root_site_search_sitemap_freshness`. Root `site`, search index и sitemap теперь включают former `DOC_M25_PENDING_SITE_PAGES`; browser proof, broad scans, dependency remediation, raw report retention, publication, release, deploy и git actions остаются вне этого closure.

## Closure Rule

G5 может закрыть source docs, nav, tests, registry и control-plane sync без root `site` freshness claim. Полная generated-site freshness требует current strict MkDocs build to root `site`, search/sitemap evidence и `git diff --check` в том же approved slice.
