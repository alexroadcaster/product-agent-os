---
title: "Архив — Product-Agent OS Batch 34D product docs QA and closure packet"
---

# Архив — Product-Agent OS Batch 34D product docs QA and closure packet {#product-agent-os-batch-34d-product-docs-qa-and-closure-packet}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

Source status: `internal`

## Scope

This packet records Batch 34D `B34-QA-M31..M33` for Product-Agent OS product documentation QA and closure. It is internal evidence for product-docs quality gates, RU/EN page parity, static rendered-site language switcher checks, strict MkDocs closure and Batch 35 handoff boundaries.

Batch 34D closes the promoted public-ready documentation set from `docs/sources/product-agent-os-batch34b-public-copy-rewrite.md` and the RU/EN localization architecture from `docs/sources/product-agent-os-batch34c-i18n-localization.md`.

This packet does not publish the docs site, start a live server, run browser automation, call providers or live external model/API endpoints, mutate the canonical graph, publish the plugin or perform git stage/commit/push/PR.

## B34-QA-M31 Product Docs Quality Gates

The focused docs test gate enforces:

- `public_forbidden_terms`: public-ready RU and EN pages must not contain internal implementation-history markers such as `Task`, `Track`, `Batch`, `T10-*` or `B34-*` outside internal evidence surfaces.
- `localized_page_parity`: every public-ready RU page has an EN sibling with the same source path plus `.en.md`.
- `Source status`: every public-ready RU and EN page keeps a visible `Source status:` marker.
- EN pages contain no Cyrillic text.
- `localized_nav_coverage`: `mkdocs.yml` keeps `mkdocs-static-i18n`, suffix structure, RU root, EN `/en/`, Material language switcher links and localized EN navigation.
- no unapproved live/provider/git actions: Batch 34D records no live server, no browser automation, no provider/live external model/API calls, no canonical graph mutation and no git stage/commit/push/PR.

## B34-QA-M32 Rendered Site And Language Switcher

Batch 34D uses static HTML inspection because browser automation is not separately approved for this slice.

`static_html_language_switcher_evidence` requires the regular MkDocs output under `site/` to contain:

- `site/index.html`;
- `site/en/index.html`;
- `site/product-agent-os/index.html`;
- `site/en/product-agent-os/index.html`;
- Material language selector markup (`md-select`);
- alternate RU and EN links (`hreflang="ru"` and `hreflang="en"`);
- equivalent EN route links under `/en/`.

The closure evidence surface is named `regular site/ rebuild evidence`. Actual command results are recorded after the M32 strict MkDocs run.

## B34-QA-M33 Closure And Handoff

Closure sync touches:

- `docs/sources/registry.md`;
- `docs/sources/product-agent-os-track-10-backlog.md`;
- `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md`;
- `tools/check_docs.py`;
- `tests/product_agent_os/test_product_agent_os_docs.py`;
- root control-plane files: `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- root and plugin readmes when status wording needs current closure state;
- generated `site/` after the regular strict MkDocs build.

Batch 35 execution remains separate and approval-required. Batch 34D closure is evidence that the product docs and RU/EN localization are ready for owner review; it is not approval to start live runtime, browser automation, provider calls, canonical mutation, plugin publication, external writes or git release actions.

## Public-Ready RU/EN Parity Set

| RU page | EN page |
| --- | --- |
| `docs/product-agent-os/index.md` | `docs/product-agent-os/index.en.md` |
| `docs/product-agent-os/project-code-graph.md` | `docs/product-agent-os/project-code-graph.en.md` |
| `docs/product-agent-os/live-runtime-governance.md` | `docs/product-agent-os/live-runtime-governance.en.md` |
| `docs/product-agent-os/approval-bound-real-testing.md` | `docs/product-agent-os/approval-bound-real-testing.en.md` |
| `docs/product-agent-os/agent-skill-modernization-loop.md` | `docs/product-agent-os/agent-skill-modernization-loop.en.md` |
| `docs/product-agent-os/cli-reference.md` | `docs/product-agent-os/cli-reference.en.md` |
| `docs/product-agent-os/artifact-contracts.md` | `docs/product-agent-os/artifact-contracts.en.md` |
| `docs/product-agent-os/packaging-and-closure.md` | `docs/product-agent-os/packaging-and-closure.en.md` |
| `docs/product-agent-os/technical.md` | `docs/product-agent-os/technical.en.md` |
| `docs/product-agent-os/development-standards.md` | `docs/product-agent-os/development-standards.en.md` |
| `docs/product-agent-os/methodology-intelligence.md` | `docs/product-agent-os/methodology-intelligence.en.md` |
| `docs/product-agent-os/scenarios.md` | `docs/product-agent-os/scenarios.en.md` |
| `docs/product-agent-os/behavioral-evals.md` | `docs/product-agent-os/behavioral-evals.en.md` |
| `docs/product-agent-os/codex-compatibility.md` | `docs/product-agent-os/codex-compatibility.en.md` |
| `docs/product-agent-os/architecture.md` | `docs/product-agent-os/architecture.en.md` |
| `docs/product-agent/overview.md` | `docs/product-agent/overview.en.md` |
| `docs/product-agent/lifecycle.md` | `docs/product-agent/lifecycle.en.md` |
| `docs/product-agent/roles.md` | `docs/product-agent/roles.en.md` |
| `docs/product-agent/control-plane.md` | `docs/product-agent/control-plane.en.md` |
| `docs/product-agent/product-agent-os-plugin-spec.md` | `docs/product-agent/product-agent-os-plugin-spec.en.md` |
| `docs/diagrams/index.md` | `docs/diagrams/index.en.md` |
| `docs/diagrams/architecture.md` | `docs/diagrams/architecture.en.md` |
| `docs/diagrams/product-delivery-lifecycle.md` | `docs/diagrams/product-delivery-lifecycle.en.md` |
| `docs/diagrams/agent-team-and-skills.md` | `docs/diagrams/agent-team-and-skills.en.md` |
| `docs/diagrams/runtime-decision-map.md` | `docs/diagrams/runtime-decision-map.en.md` |
| `docs/diagrams/skill-lifecycle.md` | `docs/diagrams/skill-lifecycle.en.md` |
| `docs/diagrams/context-memory-verification.md` | `docs/diagrams/context-memory-verification.en.md` |
| `docs/runtime/overview.md` | `docs/runtime/overview.en.md` |
| `docs/runtime/non-interactive-and-mcp.md` | `docs/runtime/non-interactive-and-mcp.en.md` |
| `docs/runtime/automations-github.md` | `docs/runtime/automations-github.en.md` |
| `docs/runtime/worktrees-hooks-rules.md` | `docs/runtime/worktrees-hooks-rules.en.md` |
| `docs/agent-systems/subagents-skills.md` | `docs/agent-systems/subagents-skills.en.md` |
| `docs/playbooks/docs-update.md` | `docs/playbooks/docs-update.en.md` |
| `docs/playbooks/use-case-to-plugin.md` | `docs/playbooks/use-case-to-plugin.en.md` |
| `docs/playbooks/workspace-readiness-audit.md` | `docs/playbooks/workspace-readiness-audit.en.md` |

## Verification Evidence

- Focused B34D docs test first failed on the missing B34D packet.
- After adding the packet and control-plane sync, focused B34D docs test failed on missing `site/en/index.html` and `site/en/product-agent-os/index.html`, proving the rendered-site gate was active before rebuild.
- Workspace-local dependency install succeeded into `.mkdocs_deps_b34d` with `mkdocs-static-i18n`.
- Regular strict MkDocs build ran with workspace-local `PYTHONPATH=.mkdocs_deps_b34d` and `NO_MKDOCS_2_WARNING=1`, rebuilt `site/`, produced RU root plus EN `/en/`, and exited `0`.
- Focused B34D docs test passed after the rebuild.
- `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 43 tests with `OK`.
- `python tools\check_docs.py` returned `OK: documentation structure checks passed`.
- Static HTML inspection found `md-select`, `hreflang="ru"`, `hreflang="en"` and `/en/` routes in `site/index.html`, `site/en/index.html`, `site/product-agent-os/index.html` and `site/en/product-agent-os/index.html`.
- Local `file://` switcher follow-up added `docs/assets/javascripts/local-file-i18n.js` and `mkdocs.yml` wiring so RU-only pages with Material's global `/en/` fallback rewrite to a relative `en/index.html` target inside `site/` instead of `file:///C:/en`.
- Static `file://` hreflang simulation checked 652 RU/EN language links and confirmed 182 absolute EN fallback links are guarded and resolve inside `site/`.
- Post-evidence strict MkDocs rebuild exited `0`.
- `git diff --check` first failed on MkDocs-generated HTML trailing whitespace, then passed after mechanical normalization of 163 generated `site/**/*.html` files.

## Boundary

- staged evidence only;
- not source of truth beyond the listed docs/source artifacts;
- no live server;
- no browser automation;
- no provider/live external model/API calls;
- no canonical graph mutation;
- no git stage/commit/push/PR;
- no plugin publication;
- no active automation creation;
- no external write.
