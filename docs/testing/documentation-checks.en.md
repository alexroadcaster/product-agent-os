# Documentation and site checks

Source status: repository_source / static_contract_review; DG06, 2026-11-15.

Owner: docs-maintainer + verification owner. Scope/version: repository `259977f3b257ba7fc0e932396f8963262bd327ad`. Update when routing, MkDocs or localization tests change. [TEST.md](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/TEST.md) owns current commands and escalation; [check_docs.py](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tools/check_docs.py) and [site_checks.py](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/product_agent_os/site_checks.py) are execution sources. This is a route, not the result of a current run.

## From source to preview

1. Compare changed claims with source owners and revision; check Source status, owner, limits, RU/EN meaning and source links. For selected Markdown use `python -B tools/check_docs.py --paths <changed-files>`; `--paths` does not check site/archive.
2. For a changed matrix run `python -B plugins/product-agent-os/scripts/validate_task_matrix.py <changed-plan>` for each affected language, and compare IDs, dependencies, AC and preservation of related data. For a changed shared source-doc contract select the relevant unittest under TEST. `git diff --check` finds whitespace errors in tracked diff; check new files separately.
3. For nav, i18n, search/sitemap or other site-sensitive changes run strict MkDocs to an isolated output using the installed project-local environment, without promoting `site/`. For example, with the existing environment: `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir <isolated-output>`. Do not hide failures or warnings; installing dependencies has a separate authority boundary.
4. For local file links run the project script `tools/fix_site_i18n_links.ps1 -SiteDir <isolated-output>`, then point `PAOS_DOCS_SITE_DIR` to that output and run `python -B -m unittest tests.product_agent_os.site_checks -q`. Site tests cover their enumerated pages, language switching, search and sitemap; separately verify new RU/EN routes, links and anchors. Browser/render is needed when display or interaction changed.
5. Record exact commands, exit codes, warnings, output path, revision, limits and checked routes in the owning evidence. A site from an older run or root `site/` is not evidence for the new preview. Checks do not authorize publication.

## Failure triage

Separate baseline from the current run: retain the first failure and its conditions, determine whether the cause lies in changed docs, a stale expectation or the environment; fix the demonstrated cause and rerun the affected gate. Do not disable checks, substitute a placeholder for a substantive translation or change trust to obtain a pass. Record an unrelated defect separately; a failed mandatory gate limits closure.

For the move, DG01 stage DOCS-13/A completed repair and retained historical initial failures and the 15.11.2026 retest in [DG01 results](../planning/documentation-architecture-2026-11-15.md#dg01-results). Its receipt is not a new DG06 run. Parent DOCS-13 closes after B and current applicable checks for the original AC. The exact scope and outcomes of the current run belong in the [documentation plan](../planning/documentation-architecture-2026-11-15.md), not this general guide.
