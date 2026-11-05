---
title: "Архив — Product-Agent OS Batch 34C RU/EN I18N localization packet"
---

# Архив — Product-Agent OS Batch 34C RU/EN I18N localization packet {#product-agent-os-batch-34c-ruen-i18n-localization-packet}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

Source status: `internal`

## Scope

This packet records Batch 34C `B34-I18N-M24..M30` for Product-Agent OS documentation localization. It is internal evidence for the i18n architecture, RU/EN page pair policy, terminology allowlist, navigation/search metadata and parity checks.

Batch 34C localizes the promoted `public_ready_pages` from `docs/sources/product-agent-os-batch34b-public-copy-rewrite.md`. Internal evidence surfaces such as `docs/sources/`, `docs/superpowers/`, source registry, backlog and root control-plane files keep provenance and are not treated as public presentation copy.

This packet does not publish the docs site, start a live server, run browser automation, call providers or live external model/API endpoints, mutate the canonical graph, publish the plugin or perform git stage/commit/push/PR.

## B34-I18N-M24 Architecture Decision

Decision: use `mkdocs-static-i18n` with suffix structure.

Rationale:

- Material for MkDocs supports a header language selector through alternate language links.
- `mkdocs-static-i18n` supports default language output at the site root and localized output under each locale path.
- The suffix structure keeps the current RU page as the canonical base file and stores EN equivalents as `*.en.md` siblings.
- `fallback_to_default: false` prevents untranslated RU pages from being copied into the EN output and avoids duplicate fallback pollution in search.

Configuration contract:

```yaml
i18n_architecture:
  plugin: mkdocs-static-i18n
  docs_structure: suffix
  ru_default_at_site_root: true
  en_under: /en/
  fallback_to_default: false
  reconfigure_material: true
  reconfigure_search: false
```

Status terms for verification after the full-site B34E M47 correction: RU default at site root, EN under /en/, fallback_to_default: false, reconfigure_material: true, reconfigure_search: false.

## B34-I18N-M25 Build And Switcher

`requirements.txt` declares `mkdocs-static-i18n`. `mkdocs.yml` configures:

- `locale: ru` as the default build at `/`;
- `locale: en` as the English build at `/en/`;
- Material language switcher links for `RU` and `EN`;
- localized EN navigation over the public-ready page set;
- localized `site_name` and `site_description` values;
- search configuration with fallback protection through `fallback_to_default: false` and full-site page parity through `reconfigure_search: false`.

The language switcher is a documentation UI affordance only. It is not runtime automation and does not imply publication.

## B34-I18N-M26 RU Canonical Product Copy

RU pages remain the canonical base pages. The RU localization policy is:

- prose should be Russian;
- English remains only for approved technical terms, product names, commands, filenames, code identifiers and official OpenAI terms;
- public pages must not expose internal implementation ledger language;
- `Source status:` labels remain visible on every public page.

## B34-I18N-M27 EN Canonical Product Copy

EN pages use the same suffix path as their RU equivalent:

```text
docs/product-agent-os/index.md -> docs/product-agent-os/index.en.md
```

EN pages must be complete product-facing equivalents, not fallback placeholders. They keep matching structure, links and product claims, while avoiding Cyrillic text and internal implementation ledger terms.

## B34-I18N-M28 terminology_allowlist

Approved terms that may remain English in RU pages:

- Product-Agent OS;
- Codex App;
- CLI;
- IDE extension;
- subagents;
- skills;
- `AGENTS.md`;
- memory;
- sandbox;
- approvals;
- MCP;
- Agents SDK;
- MkDocs;
- `mkdocs-static-i18n`;
- Source status;
- source of truth when used as a fixed documentation governance term;
- owner, evidence, runtime, eval, plugin, prompt, automation and approval when used as established Product-Agent OS terminology;
- filenames, code identifiers, commands, JSON keys, artifact names and URLs.

Forbidden non-term English prose examples in RU pages:

- broad explanatory English sentences where a Russian sentence is available;
- marketing-style English copy outside product names;
- untranslated navigation labels unless they are product or tool names.

## B34-I18N-M29 Navigation, Search And Metadata

Navigation policy:

- RU default build keeps the current documentation structure and Russian labels where the page is public-facing;
- EN build uses an English nav override for the public-ready Product-Agent OS presentation set;
- internal evidence pages are not pulled into the EN public nav by fallback;
- links in localized Markdown reference base `.md` paths, not `.en.md` paths.

Search policy:

- `fallback_to_default: false` blocks RU fallback pages in EN search;
- `reconfigure_search: false` keeps real EN sibling entries in search even when their internal evidence text matches the RU page;
- RU/EN search configuration remains static and local to MkDocs.

Metadata policy:

- RU uses `Product-Agent OS` with Russian `site_description`;
- EN uses `Product-Agent OS Documentation` and `Product documentation for Product-Agent OS.`;
- per-page language metadata is handled by the i18n plugin and Material reconfiguration.

## B34-I18N-M30 localized_page_parity

Every public-ready page has an EN sibling:

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

Parity checks:

- every listed RU page keeps `Source status:`;
- every EN page keeps `Source status:`;
- EN pages contain no Cyrillic text;
- RU and EN public pages contain no internal implementation ledger terms;
- links use base `.md` targets so the i18n plugin can resolve localized equivalents;
- shared Mermaid and static assets remain referenced through base paths.

## Agent And Skill Evidence

Batch 34C used Product-Agent OS implementation planning, agent-team-design, docs-maintainer guidance, subagent-driven development, dispatching-parallel-agents, test-driven-development and verification-before-completion guidance.

Agent ownership:

- Product-Agent OS reference group: Product-Agent OS overview, graph, governance, approval, modernization, CLI, artifacts and closure pages.
- Product model group: technical, standards, methodology, scenarios, evals, compatibility, architecture and product-agent bridge pages.
- Atlas/runtime/playbook group: diagram atlas, runtime bridge, agent-system bridge and selected playbooks.
- Local orchestrator: tests, `mkdocs.yml`, `requirements.txt`, source registry, backlog and control-plane synchronization.

## Verification Evidence

- Focused B34C docs test first failed on the missing B34C packet, then passed.
- EN Cyrillic scan, `.en.md` link scan and public forbidden-term scan returned no matches.
- EN sibling presence scan reported `missing: []` for 35 public-ready pages.
- `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 42 tests with `OK`.
- `python tools\check_docs.py` returned `OK: documentation structure checks passed`.
- Strict MkDocs built RU root and EN `/en/` with workspace-local `.mkdocs_deps_b34c` dependencies into disposable `.mkdocs_task26_b34c_site` and exited `0`.
- Temporary `.mkdocs_deps_b34c` and `.mkdocs_task26_b34c_site` directories were removed after verification.

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
- no dependency installation in this packet itself.
