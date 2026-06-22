# Residual Follow-Up And Site Freshness

Source status: `project evidence`

This page closes G5 residual routing: which G1.1 follow-ups remain approval-required, how to summarize real-target static comparison without exposing private targets, and why final `DOC-M25` does not run automatically.

## Residual Routing

| Residual | Owning row | Current state |
| --- | --- | --- |
| Root `site`, search, and sitemap freshness | `DOC-M25` | `approval_required_not_run` after G2-G5 source updates. |
| Browser Mermaid/HTML proof | `DOC-M08`, `DOC-M23`, `DOC-M29` | Approval-required; static smoke does not prove browser rendering. |
| Broad lint/format/Vale enforcement | `DOC-M21`, `DOC-M26`, `DOC-M30` | Advisory or scoped-only until owner thresholds exist. |
| Link/secret scans and raw report retention | `DOC-M24`, `DOC-M30` | Do not run broad scans or retain raw reports without approval. |
| Python audit, full SBOM, Node remediation | `DOC-M24`, `DOC-M30` | Do not claim remediation or complete SBOM without commands and rollback. |
| Docusaurus, Storybook, Structurizr | `DOC-M21`, `DOC-M30` | Deferred trigger governance; no install. |

## Static Comparison Summary

For private or real-target comparison, store only redacted target class, run IDs, digest deltas, page/key deltas, unsupported claims preserved, actions performed, and explicit no-unapproved-actions. Do not publish target names, raw paths, private screenshots, raw source excerpts, or private data.

## Final `DOC-M25`

Final `DOC-M25` may rebuild root `site` only after separate approval. Until then, source docs may be current while generated `site`, search index, and sitemap remain stale/unsupported for new G2-G5 pages.

## DOC-M25 Closure Update

`DOC-M25` is closed through `documentation_refresh_DOC-M25-A01` with status `implemented_root_site_search_sitemap_freshness`. Root `site`, search index and sitemap now include the former `DOC_M25_PENDING_SITE_PAGES`; browser proof, broad scans, dependency remediation, raw report retention, publication, release, deploy and git actions remain outside this closure.

## Closure Rule

G5 can close source docs, nav, tests, registry, and control-plane sync without a root `site` freshness claim. Full generated-site freshness requires current strict MkDocs build to root `site`, search/sitemap evidence, and `git diff --check` in the same approved slice.
