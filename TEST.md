# TEST.md

<!-- product-agent-os:start test -->
Project: Codex Docs / Product-Agent OS
Last compacted: 2026-06-11

## Purpose

`TEST.md` is the compact verification routing layer. It defines which checks are required for current docs, control-plane, plugin/runtime, eval and Batch 39 work. Detailed historical evidence belongs in source-owned backlogs, eval reports, `RUNLOG.md` or `prod_test.md`.

## Required Checks After Docs Or Control-Plane Changes

Run these checks after changes to root control-plane files, docs/source registry, templates or test contracts:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v
python -m unittest tests.product_agent_os.test_lifecycle_hooks -v
python plugins\product-agent-os\scripts\validate_hooks.py .codex\hooks.json
python plugins\product-agent-os\scripts\validate_hooks.py .codex\hooks
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
python tools\check_docs.py
git diff --check
python -m unittest discover -s tests -p "test_*.py" -v
```

Run strict MkDocs only when navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search/sitemap behavior or generated `site/` evidence changes.

## Batch 44 S0 Self-Learning Loop Scope Checks

For `B44-S0-Discovery-And-Scope`, run:

```powershell
python -m unittest tests.product_agent_os.test_discovery -v
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
git diff --check
```

The scope detector must fail closed for unrelated projects, redact raw workspace
paths by default and remain a detector only. These checks do not prove any
active scheduler, Codex App automation, hidden session ingestion, provider call,
target mutation or auto-apply behavior.

## Control-Plane Size Budgets

`RUNLOG.md` has a `50 KB` budget, measured as `50 * 1024` UTF-8 bytes. If it exceeds that budget, run `.codex/workflows/control-plane-sync.md` as an overflow protocol: redistribute scope to `REQUIREMENTS.md`, sequencing to `PLAN.md`, verification to `TEST.md`, eval/claim ceilings to `EVALS.md`, detailed evidence to source-owned plans/specs/backlogs or `prod_test.md`, then shorten `RUNLOG.md` to current handoff and residual-risk pointers.

### MkDocs Runtime Location

`requirements.txt` declares the docs runtime:

```text
mkdocs>=1.6,<2
mkdocs-material>=9.5,<9.6
mkdocs-static-i18n>=1.2,<1.3
```

The default `python` in the current Codex App shell can be `C:\Python313\python.exe`; it does not necessarily have MkDocs installed, so plain `python -m mkdocs ...` may fail with `No module named mkdocs`.

Track 11 G1.1 `DOC-M35` installed the current project-local MkDocs runtime on 2026-06-21:

```powershell
.venv-docs\Scripts\python.exe -m mkdocs --version
.venv-docs\Scripts\python.exe -m mkdocs build --strict --site-dir .docs-tools\reports\mkdocs-strict-smoke-2026-06-21
```

The installed runtime evidence is `documentation_refresh_G1_1-DOC-M35-INSTALL-A01`: `mkdocs==1.6.1`, `mkdocs-material==9.5.50`, `mkdocs-static-i18n==1.2.3`, and strict smoke output under `.docs-tools/reports/`. This smoke build does not refresh root `site/`; generated `site/`, search and sitemap freshness require a current build to `site/` before being claimed.

Historical strict-site builds used target-install dependencies rather than the default Python environment:

```powershell
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'
$env:NO_MKDOCS_2_WARNING='1'
python -m mkdocs build --strict
```

The repository also has a prior workspace-local target install at `tmp\mkdocs_deps_b40s4`; it matches older generated `site/` metadata (`mkdocs-1.6.1`, `mkdocs-material-9.5.50`) and the Batch 40 S4 source evidence. In the 2026-06-20 shell, `tmp\mkdocs_deps_b40s4` was blocked by `PermissionError`, while `C:\tmp\codex_docs_mkdocs` existed but was not usable as a runnable `python -m mkdocs` module from the active process. Treat those paths as historical fallback evidence only; use `.venv-docs\Scripts\python.exe` for current docs-runtime checks.


### Track 11 G1.1 Project-Local Docs Toolchain Checks

G1.1 prepares a repository-owned documentation toolchain. System-file preparation does not install dependencies and does not prove generated `site/` freshness.

Planned local folders:

```text
.venv-docs/
.docs-tools/node/
.docs-tools/bin/
.docs-tools/reports/
docs/assets/javascripts/vendor/  # optional vendored diagram/runtime assets
```

After an approved install slice, verify each enabled layer from project-local paths only:

```powershell
.venv-docs\Scripts\python.exe -m mkdocs --version
.venv-docs\Scripts\python.exe -m mkdocs build --strict
npm.cmd --prefix .docs-tools\node run markdownlint:smoke
npm.cmd --prefix .docs-tools\node run prettier:check:readme
npm.cmd --prefix .docs-tools\node run markdownlint:version
npm.cmd --prefix .docs-tools\node run prettier:version
npm.cmd --prefix .docs-tools\node run redocly:version
.docs-tools\bin\vale.exe --version
.docs-tools\bin\vale.exe --config=.vale.ini .docs-tools\vale\fixtures\doc-m37-smoke.md
.docs-tools\bin\lychee.exe --version
.docs-tools\bin\gitleaks.exe version
.docs-tools\bin\lychee.exe --offline --no-progress .docs-tools\link-secret\fixtures\doc-m38-links.md
.docs-tools\bin\gitleaks.exe dir .docs-tools\link-secret\fixtures --config .gitleaks.toml --redact --no-banner --no-color --exit-code 1 --log-level error
powershell -NoProfile -ExecutionPolicy Bypass -File tools\docs_mermaid_install.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tools\docs_mermaid_install.ps1 -Install -AllowNetwork -Force
.venv-docs\Scripts\python.exe -m mkdocs build --strict --site-dir .docs-tools\reports\mkdocs-strict-smoke-doc-m39-2026-06-21
rg -n "https://unpkg.com/mermaid|cdn.jsdelivr.net/npm/mermaid|<script[^>]+src=['""]https?://" .docs-tools\reports\mkdocs-strict-smoke-doc-m39-2026-06-21
```

`DOC-M36` installed `markdownlint-cli2==0.22.1`, `prettier==3.8.4` and `@redocly/cli==2.34.0` under `.docs-tools/node/`. Use Redocly enforcement only when an OpenAPI source contract exists. Use broad docs lint/format checks, `lychee` external-link checks, broad `gitleaks` scans, binary vendoring, Mermaid runtime vendoring, dependency audit/SBOM generation and report retention only after the slice names approval boundary, source, expected output and redaction policy.

`DOC-M37` installed local Vale `3.15.1` under `.docs-tools/bin/` with `.vale.ini`,
`.docs-tools/vale/` rules and `.docs-tools/bin/vale.sha256`. The approved smoke
scope is the local fixture only. Broad docs language scans and any failure
enforcement remain out of scope until thresholds, false-positive handling and
report retention are approved.

`DOC-M38` installed local lychee `0.24.2` and gitleaks `8.30.0` under
`.docs-tools/bin/` with `.docs-tools/bin/lychee.sha256`,
`.docs-tools/bin/gitleaks.sha256`, `.gitleaks.toml` and
`.docs-tools/link-secret/` fixtures. The approved smoke scope is offline local
link fixture checking and redacted clean secret fixture checking only. External
URL crawling, broad docs link checks, broad repository secret scans, raw finding
publication and report retention remain out of scope until a later slice names
the scope, redaction policy and retention boundary.

`DOC-M39` vendored Mermaid `10.9.6` under `docs/assets/javascripts/vendor/`
with `mermaid-10.9.6.min.js.sha256`, `mermaid-10.9.6.LICENSE.txt` and
`mermaid-10.9.6.package.json`. The approved smoke scope is strict MkDocs build
to `.docs-tools/reports/mkdocs-strict-smoke-doc-m39-2026-06-21` plus static
external Mermaid/script audit. Browser rendering, console/network cleanliness,
responsive visual quality, root `site` freshness and dependency safety remain
out of scope until later approved evidence exists.

`DOC-M40` records dependency audit and SBOM governance for the docs toolchain.
Use `tools\docs_dependency_audit.ps1` for local Python inventory, `pip check`,
Node CycloneDX SBOM generation and checksum consistency. The approved network
audit evidence is `npm.cmd --prefix .docs-tools\node audit --audit-level=high
--json`: current Node audit reports 3 moderate findings and 0 high/critical
findings. Do not run `npm audit fix`, `npm update`, dependency upgrades,
`pip-audit` installation, raw report retention or remediation without a separate
approved dependency remediation slice. Python vulnerability audit, complete
repository SBOM, standalone binary SBOM and Mermaid vulnerability audit remain
unsupported.

`DOC-M41` records deferred platform trigger governance for Docusaurus,
Storybook and Structurizr DSL. It is a source-owned decision/trigger record
only: no deferred platform install, download, scaffold, root `site` rebuild,
browser proof, render proof or publication action is approved by this evidence.
If a future requirement triggers one of these tools, first create an
owner-approved platform decision record naming trigger evidence, local install
path, rollback, verification gates and unsupported claims.

## Required Checks After Plugin Or Runtime Changes

Use focused checks first, then broaden through the relevant project route:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_lifecycle_hooks -v
python -m unittest discover tests -v
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

If a slice changes Product-Agent OS plugin behavior, also inspect the matching fixture/eval/transcript checks referenced by the source plan or backlog before making readiness claims.

Use `timeout_ms: 1200000` for full Product-Agent OS unittest runs.

## Batch 39 Verification Contract

- `prod_test.md` is the required attempt/failure/fix/retest ledger for `B39-TEST-M01..M54`.
- Future Batch 39 pilots should include real-project target evidence where it improves Product-Agent OS confidence. Internal `codex_docs` fixtures remain valid for deterministic contracts, but they do not replace real target discovery when the route depends on project shape, source policy, runtime signals or user workflow.
- Every Batch 39 task must record:
  - setup and prerequisites;
  - owner action and Codex action;
  - exact command/manual step;
  - observed evidence;
  - result status;
  - failure, fix and retest loop if applicable;
  - residual risk or accepted gap.
- Do not treat a planned test matrix as execution evidence.
- Do not treat generated dashboards, generated reports or project graphs as proof unless backed by source artifacts, current command evidence, current runtime evidence or an explicit accepted gap.

## Runtime And External-Action Boundaries

Runtime And External-Action Verification Boundaries

Fresh explicit approval is required before:

- target workspace mutation;
- browser automation;
- provider/API calls;
- live server or dashboard launch;
- canonical graph-source mutation;
- git branch creation/switching, stage, commit, push, tag or PR;
- publication, deployment or external automation creation.

Approval for one surface does not authorize another. Runtime launch approval does not authorize browser automation; browser approval does not authorize provider calls; provider-call approval does not authorize canonical mutation or git/release actions.

For real-project target tests, the default verification mode is read-only: inventory, route classification, source-policy status, control-plane presence, safe artifact maps, counts, digests and redacted summaries. Build/test/runtime/browser/provider/database/git/release actions require exact approval before execution.

## Current Verification State

| Area | Current evidence state | Required next check |
| --- | --- | --- |
| Batch 35 `T10-LIVE-M41` | Closed as `owner_closed_no_op_git_release_pr`; no git writes occurred. | Fresh git preflight and exact approval before any future git write. |
| Batch 38 cache/readiness | `B38-S2` current evidence records `plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage`; historical `blocked_pending_explicit_cache_mutation_approval` remains preserved. | Treat as historical unless a new cache mutation is requested. |
| `B38-PILOT-NF01` | Docs-only pilot addendum; target apply blocked by `source_policy_status: blocked`. | Resolve target source policy and target control-plane artifacts before target mutation. |
| Batch 39 | `B39-S1` through `B39-S5` are current through `B39-S5-CLOSURE-A01`. S5 evidence closes source-doc sync, go/no-go and no-unapproved-actions proof as `closed_for_owner_feedback_testing_not_release_ready`: release is `no_go`, owner-feedback testing is `conditional_go`, runtime/browser pilot is `approval_required`, and promotion remains `manual_only_not_promoted`. | Run owner-feedback tests from `batch39-s5-owner-feedback-test-plan.json`; keep S4/S5 focused tests, full unittest, fixture/transcript eval, Codex compatibility, docs check and diff hygiene before any stronger readiness claim. |
| Batch 40 completion-skeptic | Local manual loop closed as `manual_only` and `not_promoted`. | Automation promotion requires manual success evidence, eval cases, owner, cadence, stop condition and rollback/disable path. |
| Batch 41 first-run orchestration | `B41-S1-M01..M05`, `B41-S2-M06..M09`, `B41-S3-M10..M16`, `B41-S4-M17..M20`, `B41-S5-M21..M23` and `B41-S6-M24..M30` are recorded as local/read-only/staged CLI/contract behavior. Owner review of the Neural_Flow artifact exposed that structurally valid first-run HTML is not product-usable; `B41-S7-M31..M40` added cockpit/static/browser evidence and conditional Neural_Flow acceptance. A later owner review still rejected the HTML as too text-file-like and missing architecture diagrams, so `B41-S8-M41..M47` is now planned for architecture-dossier redesign, diagram panels, visual shell, evidence/decision sections, graph runtime/fallback clarity, Playwright visual/a11y acceptance and regenerated Neural_Flow before/after proof. | S8 verification must include focused renderer tests, diagram render/fallback checks, Playwright desktop/mobile screenshots, interaction checks, console/network result, accessible-name/landmark checks, no-overlap visual review and completion-skeptic unsupported-claim review. Cosmos.gl/WebGL runtime execution remains blocked unless a later vendored-runtime slice is approved; no release readiness, target apply safety, provider/API call, git/release action, external write or installed-plugin readiness claim is approved. |
| Batch 42 instruction/tool-use compliance | `B42-S1-M01..M03`, `B42-S2-M04..M06`, `B42-S3-M07..M08`, `B42-S4-M09..M10` and `B42-S5-M11` are planned only in `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`. | When approved for execution, run source/cache/session inventory, official-doc source check, implicit-invocation metadata validation, runtime route tests, instruction/tool-use evals, hygiene checks, Codex compatibility, docs checks, diff hygiene and fresh-session proof if required. Do not claim Product-Agent OS auto-engagement is fixed from the planning matrix alone. |
| Agent lifecycle, hooks and control-plane sync | Current local agents, packaged agent templates, workflows, config templates and `agent-context-contract` require config-routed Task Brief / Completion Brief plus control-plane sync before completion. Project-local `.codex/hooks.json` is installed through `product_agent_os_LIFECYCLE-HOOKS-A01`; hook scripts and the Product-Agent OS policy mirror live under `.codex/hooks/`. `PreToolUse` blocks mutating Product-Agent OS commands when `.codex/product-agent-os/lifecycle-state.json` is missing or only has the legacy minimal marker; accepted marker schema is `task_start_brief_v1` with full `brief_fields_present`. | Rerun task lifecycle, `validate_hooks.py .codex\hooks.json`, `validate_hooks.py .codex\hooks`, infrastructure template, docs, docs-structure and diff hygiene checks after future changes to this contract. Codex hook trust review / new-session execution remains a manual runtime boundary. |
| Track 11 G1.1 docs toolchain | System files route project-local documentation tooling through `.venv-docs/`, `.docs-tools/node/`, `.docs-tools/bin/`, `.docs-tools/vale/`, `.docs-tools/link-secret/`, `.docs-tools/reports/` and `docs/assets/javascripts/vendor/`. `DOC-M35` installed the MkDocs runtime and passed a strict smoke build under `.docs-tools/reports/`; `DOC-M36` installed Node docs tooling and passed scoped README markdownlint/Prettier smoke; `DOC-M37` installed Vale and passed advisory fixture/negative wording smoke; `DOC-M38` installed lychee/gitleaks and passed scoped offline link plus redacted clean secret fixture smokes; `DOC-M39` vendored Mermaid and switched MkDocs to the local asset; `DOC-M40` records local dependency inventory, Node CycloneDX SBOM generation and current Node advisory counts; `DOC-M41` records deferred platform trigger governance for Docusaurus, Storybook and Structurizr DSL with no install or site rebuild. Root `site/`, browser Mermaid rendering, broad docs lint/format, broad Vale enforcement, broad link/secret scans, external URL crawling, report retention, Redocly enforcement, Python vulnerability audit, complete repository SBOM, dependency remediation and deferred platform runtime/readiness are not proven by that state. | Use `.venv-docs\Scripts\python.exe` for MkDocs checks, `npm.cmd --prefix .docs-tools\node run ...` for Node checks, `.docs-tools\bin\vale.exe --config=.vale.ini ...` for approved advisory Vale scopes, `.docs-tools\bin\lychee.exe --offline ...` for approved local link scopes, `.docs-tools\bin\gitleaks.exe dir ... --redact ...` for approved secret scopes, `docs/assets/javascripts/vendor/mermaid-10.9.6.min.js` as static vendor evidence and `tools\docs_dependency_audit.ps1` for local dependency/SBOM governance. Before claiming root `site`, search or sitemap freshness, run a current build to `site/`; before claiming Python vulnerability safety or remediation, run a separately approved audit/remediation slice; before claiming browser diagram rendering or deferred platform readiness, run an approved proof slice. |
| Track 11 G2 first-run cockpit/artifact docs | Source docs and nav/test routing are implemented through `documentation_refresh_G2-A01`; the new cockpit page is intentionally in `DOC_M25_PENDING_SITE_PAGES`. | Run docs unittest, `tools\check_docs.py`, strict MkDocs smoke to `.docs-tools\reports\mkdocs-strict-smoke-g2-2026-06-21` for source/nav proof and `git diff --check`; do not claim root `site`/search/sitemap freshness until final `DOC-M25`. |
| Track 11 G3 diagram atlas/architecture maps | Source docs and nav/test routing are implemented through `documentation_refresh_G3-A01`; the five new diagram pages are intentionally in `DOC_M25_PENDING_SITE_PAGES`. | Run docs unittest, `tools\check_docs.py`, strict MkDocs smoke to `.docs-tools\reports\mkdocs-strict-smoke-g3-2026-06-21` for source/nav proof and `git diff --check`; do not claim root `site`/search/sitemap freshness until final `DOC-M25`; browser proof and Structurizr DSL evidence remain approval-required. |
| Track 11 G4 operator flows/system behavior docs | Source docs and nav/test routing are implemented through `documentation_refresh_G4-A01`; the four new Product-Agent OS pages are intentionally in `DOC_M25_PENDING_SITE_PAGES`. | Run docs unittest, `tools\check_docs.py`, strict MkDocs smoke to `.docs-tools\reports\mkdocs-strict-smoke-g4-2026-06-22` for source/nav proof and `git diff --check`; do not claim root `site`/search/sitemap freshness until final `DOC-M25`; auto-engagement/cache/global config/fresh-session proof remains unsupported. |
| Track 11 G5 evidence quality/final site gate docs | Source docs and nav/test routing are implemented through `documentation_refresh_G5-A01`; the five new Product-Agent OS pages are intentionally in `DOC_M25_PENDING_SITE_PAGES`, while `DOC-M25` remains `approval_required_not_run`. | Run docs unittest, `tools\check_docs.py`, strict MkDocs smoke to `.docs-tools\reports\mkdocs-strict-smoke-g5-2026-06-22` for source/nav proof and `git diff --check`; do not claim root `site`/search/sitemap freshness until final `DOC-M25`; browser proof, broad scans, dependency remediation and raw report retention remain approval-required. |
| Track 11 DOC-M25 generated site freshness | Source-owned evidence is `documentation_refresh_DOC-M25-A01`; former `DOC_M25_PENDING_SITE_PAGES` are promoted into the root site parity contract. | Run `.venv-docs\Scripts\python.exe -m mkdocs --version`, `.venv-docs\Scripts\python.exe -m mkdocs build --strict`, `powershell -NoProfile -ExecutionPolicy Bypass -File tools\fix_site_i18n_links.ps1 -SiteDir site`, `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v`, `python -B tools\check_docs.py` and `git diff --check`; this proves root `site`/search/sitemap freshness and local-file i18n link hygiene only, not browser proof, broad scans, remediation, raw report retention, publication, release, deploy or git actions. |

## Historical Evidence Owners

| Marker | Evidence owner |
| --- | --- |
| `T10-LIVE-M41`, `owner_closed_no_op_git_release_pr` | `docs/sources/product-agent-os-track-10-backlog.md`, `RUNLOG.md` |
| `blocked_pending_explicit_cache_mutation_approval`, `B38-S2` | `docs/sources/product-agent-os-track-10-backlog.md`, `RUNLOG.md` |
| `B39-TEST-M01..M54`, `B39-S1..B39-S5` | `PLAN.md`, `prod_test.md` |
| `B40-S2..B40-S5`, `manual_only`, `not_promoted` | `docs/sources/product-agent-os-track-10-backlog.md`, `RUNLOG.md` |
| `B41-S1-M01..M05` | `docs/superpowers/specs/batch41-s1-command-contract-summary.json`, `docs/superpowers/specs/batch41-first-run-automation-matrix.json`, `RUNLOG.md` |
| `B41-S2-M06..M09` | `docs/superpowers/specs/batch41-s2-script-matrix-summary.json`, `docs/superpowers/specs/batch41-first-run-automation-matrix.json`, `RUNLOG.md` |
| `B41-S3-M10..M16` | `docs/superpowers/specs/batch41-s3-project-analysis-summary.json`, `docs/superpowers/specs/batch41-first-run-automation-matrix.json`, `RUNLOG.md` |
| `B41-S4-M17..M20` | `docs/superpowers/specs/batch41-s4-html-artifact-summary.json`, `docs/superpowers/specs/batch41-first-run-automation-matrix.json`, `RUNLOG.md` |
| `B41-S5-M21..M23` | `docs/superpowers/specs/batch41-s5-guided-questions-summary.json`, `docs/superpowers/specs/batch41-first-run-automation-matrix.json`, `RUNLOG.md` |
| `B41-S6-M24..M30` | `docs/superpowers/specs/batch41-s6-closure-summary.json`, `docs/superpowers/specs/batch41-s6-synthetic-e2e-summary.json`, `docs/superpowers/specs/batch41-s6-real-target-pilots-summary.json`, `docs/superpowers/specs/batch41-s6-usefulness-scorecard.json`, `docs/superpowers/specs/batch41-s6-verification-sweep-summary.json`, `docs/superpowers/specs/batch41-s6-plugin-cache-readiness.json`, `docs/superpowers/specs/batch41-s6-no-unapproved-actions-proof.json`, `docs/superpowers/specs/batch41-first-run-automation-matrix.json`, `RUNLOG.md` |
| `B41-S7-M31..M40` | `docs/superpowers/specs/batch41-s7-m31-m33-cockpit-foundation-summary.json`, `docs/superpowers/specs/batch41-s7-m34-m35-graph-rendering-summary.json`, `docs/superpowers/specs/batch41-s7-m36-m39-cockpit-ux-safety-summary.json`, `docs/superpowers/specs/batch41-s7-m40-owner-approval-packet.json`, `docs/superpowers/specs/batch41-s7-m40-neural-flow-acceptance-summary.json`, `docs/superpowers/specs/batch41-s7-m40-neural-flow-stage/`, `output/playwright/b41-s7-m40/playwright-runtime-proof.json`, `docs/superpowers/specs/batch41-s7-html-cockpit-analysis.txt`, `docs/superpowers/specs/batch41-first-run-automation-matrix.json`, focused cockpit renderer tests, `RUNLOG.md` |
| `B41-S8-M41..M47` | `docs/superpowers/specs/batch41-first-run-automation-matrix.json`; `docs/superpowers/specs/batch41-s8-m41-html-redesign-design-artifact.txt`; `docs/superpowers/specs/batch41-s8-m41-html-redesign-design-summary.json`; `docs/superpowers/specs/batch41-s8-m42-architecture-diagram-layer-summary.json`; `docs/superpowers/specs/batch41-s8-m43-cockpit-shell-redesign-summary.json`; `output/playwright/b41-s8-m42/playwright-diagram-proof.json`; `output/playwright/b41-s8-m43/playwright-shell-proof.json`; future S8 implementation summaries, regenerated Neural_Flow stage artifact, Playwright desktop/mobile screenshots, diagram render/fallback evidence, no-overlap proof, WCAG-oriented browser checks and completion-skeptic packet |
| `B42-S1..S5` | `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`; Track 10 plan Batch 42 addendum; Track 10 backlog Batch 42 planned addendum; future source/cache/session exposure packet; future official-doc source packet; future implicit-invocation validator evidence; future runtime route/eval evidence; future fresh-session proof if required |
| `DOC-M34..DOC-M41` | `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m34-folder-contract-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m35-preflight-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m35-install-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m36-node-tooling-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m37-vale-language-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m38-link-secret-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m39-mermaid-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m40-dependency-audit-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m41-deferred-platform-triggers-summary.json`; `.gitignore`; `.docs-tools/README.md`; `.docs-tools/node/package.json`; `.docs-tools/node/package-lock.json`; `.docs-tools/bin/vale.sha256`; `.docs-tools/bin/lychee.sha256`; `.docs-tools/bin/gitleaks.sha256`; `.gitleaks.toml`; `docs/assets/javascripts/vendor/README.txt`; `docs/assets/javascripts/vendor/mermaid-10.9.6.min.js`; `docs/assets/javascripts/vendor/mermaid-10.9.6.min.js.sha256`; `tools/docs_install.ps1`; `tools/docs_node_install.ps1`; `tools/docs_vale_install.ps1`; `tools/docs_link_secret_install.ps1`; `tools/docs_mermaid_install.ps1`; `tools/docs_dependency_audit.ps1`; `REQUIREMENTS.md`; `PLAN.md`; `TEST.md`; `EVALS.md`; `AGENTS.md`; `RUNLOG.md` |
| Track 8 | `docs/sources/product-agent-os-track-8-detailed-backlog.md` |
| Track 9 | `docs/sources/product-agent-os-track-9-backlog.md` |
| Source registry | `docs/sources/registry.md` |
| Batch 35 | `docs/sources/product-agent-os-batch35-approval-packet-draft.md` |

## Compatibility Marker Bank

- B37-S1 `T10-PLAN-M01..M03`, `T10-PLAN-M18`, task-matrix contract, `task-matrix-plan.md`.
- B37-S2 `T10-PLAN-M04..M05`, `T10-PLAN-M17`, `renderer_file_count: 195`, plugin cache remains stale until an explicit publication/cache refresh action is approved.
- B37-S3 `T10-PLAN-M06`, `T10-PLAN-M10`, `T10-PLAN-M13`, `validate_task_matrix.py`, `task_matrix_validator_contract_present`.
- B37-S4 `T10-PLAN-M07..M09`, `T10-PLAN-M20`, `task_matrix_planner_routing_contract_present`, `task_matrix_agent_handoff_contract_present`, `task_matrix_discovery_signal_contract_present`, `task_matrix_planning_control_governance_present`.
- B37-S5 `T10-PLAN-M11..M12`, `T10-PLAN-M14..M16`, `T10-PLAN-M19`, `task_matrix_docs_source_sync_present`, `task_matrix_backward_compatibility_policy_present`, `task_matrix_status_projection_deferred_present`, `task_matrix_system_file_hygiene_owner_present`, `task_matrix_lifecycle_archive_policy_present`.
- B38-S1 release gate/package metadata run; focused docs contract; Codex compatibility returned `status: compatible`; strict MkDocs was not run.
- M01 is owner-closed as no-op after historical missing release fields; M02 freezes the checked-in package source; M03 records the owner decision to keep Product-Agent OS local-only/internal R&D.
- M41 post-B38 audit; historical_preflight_snapshot; fresh git status/unrelated-change preflight; B37/B38/B38-S1 did not themselves close M41.
- B38-S2 verification/install smoke run; full unittest ran 846 tests with `OK`; fixture eval exited `0`; transcript eval exited `0` with 19 sessions and 0 failures; plugin cache inspection found stale installed cache; plugin_cache_refresh_attempt_status: blocked_sandbox_cache_write_denied_after_backup_stage; local_cache_refresh_result: REFRESH_OK; target_cache_still_stale: false.
- B38-S3 real-project pilot design run; docs contract; strict MkDocs; real project pilot execution was not run.
- B38-S4 safety and rollback run; validate_source_policy.py; validate_system_file_hygiene.py; secret_like_findings: 6; validate_codex_compatibility.py; not a security certification; No cache/global config mutation.
- B38-PILOT-NF01 `Neural_Flow` target pilot run; detect_project.py; run_methodology_audit.py; run_codex_runtime_runner.py; render_infrastructure.py --stage; scan_project_code_graph.py --stage; validate_source_policy.py; source_policy_status: blocked; false `pr_review` route; 481 nodes; Dashboard aggregation remains incomplete; staged hooks require exact approval; secret_like_findings: 0; No target mutation.
- B39 S2/S3 markers: `B39-TEST-M21-A01..A03`, `B39-TEST-M22-A01..A03`, `B39-TEST-M23..M33`; generated first-run views remain orientation-only, read-only real-target evidence is not release readiness, and S3 is functional regression/repeatability evidence only.
- B40-S4 implements Doubt / verifier loop docs/site/source-transfer; strict MkDocs.
- B40-S5 implements Doubt / verifier loop pilot metrics and closure; completion_skeptic_manual_pilot_ledger; completion_skeptic_go_no_go_closure.
- B41-S1 implements first-run command/UX contract rows `B41-S1-M01..M05`: `first_run_orchestrator_contract_v1`, no-args help, `--full-dry-run`, external `--stage <dir>`, `--write-analysis`, stage-inside-target block, and renderer stage output support.
- B41-S2 implements help-only script-matrix rows `B41-S2-M06..M09`: `first_run_script_registry_v1`, `first_run_command_matrix_v1`, `first_run_evidence_summary_v1`, `first_run_resume_ledger_v1`, skipped approval/live boundaries and no raw stdout/stderr retention.
- B41-S3 implements project-analysis rows `B41-S3-M10..M16`: `first_run_project_analysis_summary_v1`, `first_run_methodology_audit_summary_v1`, `first_run_source_policy_summary_v1`, `first_run_graph_dry_run_summary_v1`, `first_run_docs_logging_summary_v1`, `first_run_dependency_readiness_summary_v1` and `first_run_runtime_browser_boundary_v1`.
- B41-S4 implements HTML artifact rows `B41-S4-M17..M20`: orchestrator renderer output in stage/write-analysis modes, multi-page HTML project summaries, previous-baseline comparison in CLI/HTML/manifest, and cleanup/rollback guidance as preview-only with no deletion by default.
- B41-S5 implements guided question rows `B41-S5-M21..M23`: `first_run_guided_question_protocol_v1`, `first_run_answer_ledger_v1`, `first_run_ambiguous_route_intake_v1`, top-level `first_response`, packet `question_queue`, staged `answer-ledger-template.json` and route options without blocking deterministic read-only analysis.
- B41-S6 records first-run QA/closure rows `B41-S6-M24..M30`: `batch41_s6_synthetic_e2e_summary_v1`, `batch41_s6_real_target_pilot_summary_v1`, `batch41_s6_usefulness_scorecard_v1`, `batch41_s6_verification_sweep_summary_v1`, `batch41_s6_plugin_cache_readiness_v1`, `batch41_s6_no_unapproved_actions_proof_v1` and `batch41_s6_closure_packet_v1`; release remains `no_go`, owner-feedback testing is `conditional_go`, runtime/browser and target apply are `approval_required`, M26 is `blocked_timeout`, and M29 is `blocked_expected_approval_required`.
- B41-S7 cockpit-grade HTML artifact rows `B41-S7-M31..M40` are implemented with local/static and browser evidence for `first_run_cockpit_artifact_v1`, a primary single-file cockpit shell, a bounded view-model adapter, file/source graph, Cosmos.gl static adapter payload, selected-file panel, table fallback, code-graph empty/summary states, static search/filter controls, progressive diagnostics, static visual QA and offline/privacy/accessibility contracts. `B41-S7-M40` captured Playwright screenshots and static interaction evidence for the Neural_Flow cockpit artifact; Cosmos.gl/WebGL runtime execution remains blocked by missing vendored runtime asset and script-free fallback.
- B41-S8 architecture-dossier redesign rows `B41-S8-M41..M47` are implemented after owner review rejected the M40 HTML as still too text-file-like and missing project architecture diagrams. `B41-S8-M41` is implemented as design-contract-only with evidence in `docs/superpowers/specs/batch41-s8-m41-html-redesign-design-artifact.txt` and `docs/superpowers/specs/batch41-s8-m41-html-redesign-design-summary.json`. `B41-S8-M42` is implemented with static architecture diagram layer evidence in `docs/superpowers/specs/batch41-s8-m42-architecture-diagram-layer-summary.json` and desktop/mobile Playwright proof in `output/playwright/b41-s8-m42/playwright-diagram-proof.json`. `B41-S8-M43` is implemented with architecture-dossier shell evidence in `docs/superpowers/specs/batch41-s8-m43-cockpit-shell-redesign-summary.json` and desktop/mobile Playwright proof in `output/playwright/b41-s8-m43/playwright-shell-proof.json`. `B41-S8-M44` is implemented with visible evidence/decision/risk/source-blueprint section evidence in `docs/superpowers/specs/batch41-s8-m44-evidence-decision-risk-summary.json` and desktop/mobile Playwright proof in `output/playwright/b41-s8-m44/playwright-evidence-decision-proof.json`. `B41-S8-M45` is implemented with Graphology/Cosmos.gl static-vs-runtime boundary evidence in `docs/superpowers/specs/batch41-s8-m45-graph-runtime-boundary-summary.json` and desktop/mobile Playwright proof in `output/playwright/b41-s8-m45/playwright-graph-runtime-proof.json`; WebGL runtime execution remains explicitly not claimed. `B41-S8-M46` is implemented with visual/interaction/accessibility-oriented Playwright evidence in `docs/superpowers/specs/batch41-s8-m46-visual-a11y-acceptance-summary.json` and `output/playwright/b41-s8-m46/playwright-visual-a11y-proof.json`; WCAG certification remains explicitly not claimed. `B41-S8-M47` is implemented with regenerated Neural_Flow before/after evidence in `docs/superpowers/specs/batch41-s8-m47-neural-flow-before-after-summary.json`, staged artifact `docs/superpowers/specs/batch41-s8-m47-neural-flow-stage/` and proof `output/playwright/b41-s8-m47/playwright-neural-flow-before-after-proof.json`; final owner acceptance remains pending screenshot review.
- B42 instruction/tool-use compliance matrix is planned only. It must later verify Product-Agent OS source/cache/session skill exposure, official OpenAI/Codex source claims, implicit invocation policy, metadata validator behavior, runtime route/eval behavior for compliance prompts and `self-learning-loop`, system-file hygiene triage and fresh-session exposure before any fixed-auto-engagement claim.

## Completion Claim Rule

Do not say that a feature works, a bug is fixed, tests pass, a release is ready, or behavior is verified unless:

- the relevant check ran in the current run; or
- the claim is explicitly scoped to earlier evidence and the evidence owner is named; or
- the missing verification is recorded as an accepted gap.

<!-- product-agent-os:end test -->
