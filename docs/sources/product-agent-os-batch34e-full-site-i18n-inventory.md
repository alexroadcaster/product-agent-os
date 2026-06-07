# Product-Agent OS Batch 34E: full-site i18n inventory and translation gate M34-M49

Source status: `internal`

## Scope

Этот packet фиксирует Batch 34E `B34E-I18N-M34..M49` для корректировки полной RU/EN parity документации.

Covered ranges: `B34E-I18N-M34..M37`, `B34E-I18N-M38..M43`, `B34E-I18N-M44`, `B34E-I18N-M45`, `B34E-I18N-M46`, `B34E-I18N-M47`, `B34E-I18N-M48` and `B34E-I18N-M49`.

Batch 34C локализовал только promoted public-ready page set. Batch 34E расширяет требование на весь buildable corpus документации. Этот packet является source artifact для `full_site_i18n_inventory`, `full_site_i18n_red_gate`, `full_site_en_nav_configured`, `full_site_en_siblings_created`, `full_site_en_editorial_quality_sweep`, `full_site_ru_quality_sweep`, `full_site_language_switcher_parity`, `full_site_search_sitemap_parity`, `full_site_i18n_closure` и `full_site_i18n_final_evidence`.

Этот packet закрывает M48-M49 как strict build closure after source/control-plane sync and final full-site evidence. Batch 34E после M49 не имеет remaining Batch 34E gates; Batch 35 остается separate approval-bound work.

Он не запускает live server, не выполняет browser automation, не вызывает providers или live external model/API endpoints, не мутирует canonical graph, не публикует plugin и не выполняет git stage/commit/push/PR.

## B34E-I18N-M34 Corrective Scope Reset

Status: `done_through_m34`.

Корректирующий scope:

- Batch 34C остается валидным только для promoted public-ready page set.
- Full-site parity покрывает каждую localized RU Markdown page в `docs/`; seven English-original superpowers plan files remain base English sources and are excluded from the `.en.md` sibling requirement.
- Full-site parity не считается закрытой до M49, пока source pages, generated EN site, language switcher, search/sitemap и RU/EN content scans не пройдут closure gates.
- Acceptance gates: `full EN navigation/search/sitemap coverage`, `no missing-page language-switcher fallback`, `full_site_en_siblings_created`, EN quality sweep и RU quality sweep.

## B34E-I18N-M35 Full Inventory

Status: `done_through_m35`.

Initial M35 inventory keys:

```yaml
docs_ru_pages_total: 127
initial_m35_existing_en_siblings: 37
initial_m35_missing_en_siblings: 90
english_original_pages_total: 7
localized_ru_pages_total: 120
```

Inventory был собран из `docs/**/*.md`; существующие `*.en.md` pages исключены из RU count.

## B34E-I18N-M36 RED Gate

Status: `done_through_m36`.

Focused test suite содержит `full_site_i18n_red_gate` как `expected_red_full_site_i18n_parity`.

RED gate проверяет будущий closure condition:

- каждая localized RU Markdown page имеет `.en.md` sibling;
- English-original plan files in `docs/superpowers/plans/` are listed separately and do not require duplicate `.en.md` siblings;
- каждый EN sibling не содержит unapproved Cyrillic;
- generated `site/en/` содержит matching HTML page.

После M38-M43 source-level localized sibling gap закрыт. После M46 generated `site/en/` существует для всех 120 localized page pairs, а M47 фиксирует search/sitemap parity для того же регулярного `site/`.

## B34E-I18N-M37 EN Navigation Metadata

Status: `done_through_m37`.

EN `nav:` override в `mkdocs.yml` зеркалирует текущие RU top-level navigation sections:

- Home;
- Diagrams;
- Sources;
- Codex;
- Prompt And Context Engineering;
- Product-Agent Workflows;
- Product-Agent OS Plugin;
- Methodologies For Large Projects;
- Codex Automation And Runtime;
- Agent Systems;
- Playbooks;
- Templates;
- Insights.

`fallback_to_default: false` остается обязательным. Build не должен использовать RU fallback pages, чтобы скрыть отсутствующие translations.

## B34E-I18N-M38..M43 EN Sibling Translation Pass

Status: `done_through_m43`.

Current source inventory after M43:

```yaml
docs_ru_pages_total: 127
english_original_pages_total: 7
localized_ru_pages_total: 120
existing_en_siblings: 120
missing_localized_en_siblings: 0
full_site_en_siblings_created: true
en_source_cyrillic_hits: 0
```

Translation pass created EN siblings for:

- `B34E-I18N-M38`: `docs/codex/*.en.md` and `docs/prompting/*.en.md`;
- `B34E-I18N-M39`: `docs/agent-systems/*.en.md`, `docs/artifact-templates/*.en.md` and `docs/insights/*.en.md`;
- `B34E-I18N-M40`: `docs/playbooks/*.en.md`;
- `B34E-I18N-M41`: `docs/methodologies/*.en.md`;
- `B34E-I18N-M42`: `docs/sources/*.en.md` and `docs/sources/methodology-research/*.en.md`;
- `B34E-I18N-M43`: `docs/superpowers/specs/*.en.md`; `docs/superpowers/plans/*.md` files are English-original source plans and no longer require duplicated `.en.md` siblings.

M38-M43 preserves official OpenAI terms, source links, commands, IDs, code fences, paths, status keys, schema keys and verification vocabulary.

Methodology EN pages use the checked-in English methodology research dossiers as their source-backed basis. Large historical source/superpowers documents are source-level parity artifacts and were included in the M44 editorial quality sweep before final product-quality closure.

English-original plan files excluded from localized sibling parity:

- `superpowers/plans/2026-05-14-product-agent-os-generated-infrastructure.md`
- `superpowers/plans/2026-05-14-product-agent-os-lifecycle-skills.md`
- `superpowers/plans/2026-05-14-product-agent-os-plugin-core.md`
- `superpowers/plans/2026-05-14-product-agent-os-production-hardening.md`
- `superpowers/plans/2026-05-15-product-agent-os-codex-runtime-runner.md`
- `superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`
- `superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md`

## B34E-I18N-M44 EN Editorial Quality Sweep

Status: `done_through_m44`.

M44 records `full_site_en_editorial_quality_sweep` for the full `.en.md` corpus. The sweep checks source-level EN pages for unapproved Cyrillic, mojibake markers, Latinized Russian/machine-transliteration artifacts and unresolved internal Markdown links outside fenced code examples.

Current source quality inventory after M44:

```yaml
en_source_cyrillic_hits: 0
en_source_mojibake_hits: 0
en_source_transliteration_hits: 0
en_internal_link_failures: 0
```

M44 is an editorial/source quality gate only. It does not rebuild regular `site/`, does not claim generated `site/en/` parity, and does not close RU quality or language-switcher/search/sitemap closure gates.

## B34E-I18N-M45 RU Quality Sweep

Status: `done_through_m45`.

M45 records `full_site_ru_quality_sweep` for the full RU `.md` corpus that has `.en.md` siblings. The sweep checks source-level RU pages for non-term English explanatory headings and table labels outside official terms, commands, URLs, source titles, paths, IDs and code examples.

Current source quality inventory after M45:

```yaml
ru_source_forbidden_english_phrase_hits: 0
```

M45 is a source quality gate only. It does not rebuild regular `site/`, does not claim generated `site/en/` parity, and does not close language-switcher/search/sitemap closure gates.

## B34E-I18N-M46 Full-Site Language Switcher Parity

Status: `done_through_m46`.

M46 records `full_site_language_switcher_parity` for the generated regular `site/` output after a strict MkDocs rebuild. The static check covers every localized RU Markdown page with an `.en.md` sibling and verifies that Material header language-switcher links route RU pages to the matching EN page, EN pages back to the matching RU page, and `file://` resolution stays inside `site/`.

Current generated-site language-switcher report after M46:

```yaml
english_original_pages_total: 7
localized_ru_pages_total: 120
static_language_switcher_pairs_checked: 120
rendered_ru_pages_checked: 120
rendered_en_pages_checked: 120
language_switcher_pair_failures: 0
file_url_escape_failures: 0
```

M46 does not claim search/sitemap parity or final closure. Search/sitemap parity is closed by M47; final closure remains M48-M49.

## B34E-I18N-M47 Search, Sitemap And Strict Build Parity

Status: `done_through_m47`.

M47 records `full_site_search_sitemap_parity` for the generated regular `site/` output after a strict MkDocs rebuild. The static check compares every localized RU Markdown page with an `.en.md` sibling against page-level entries in `site/search/search_index.json` and `site/sitemap.xml`.

M47 also updates the search policy to `reconfigure_search: false` while keeping `fallback_to_default: false`. This preserves real EN sibling entries that `mkdocs-static-i18n` duplicate reduction removes when internal evidence text matches the RU page. Because fallback remains disabled, the EN search entries are real translated pages, not RU fallback pollution.

Current generated-site search/sitemap report after M47:

```yaml
strict_mkdocs_build_exit_code: 0
english_original_pages_total: 7
localized_ru_pages_total: 120
search_index_ru_pages_present: 120
search_index_en_pages_present: 120
sitemap_ru_pages_present: 120
sitemap_en_pages_present: 120
search_index_missing_ru_pages: 0
search_index_missing_en_pages: 0
sitemap_missing_ru_pages: 0
sitemap_missing_en_pages: 0
search_index_ru_fallback_pollution: 0
sitemap_ru_fallback_pollution: 0
```

M47 does not claim final closure. M48-M49 close strict-build closure evidence after source/control-plane sync and final full-site evidence.

## B34E-I18N-M48 Control-Plane And Source Sync

Status: `done_through_m48`.

M48 records source/control-plane sync after the M47 generated-site evidence. It converts the remaining `B34E-I18N-M48..M49` range from a planned closure gate into a final closure workflow while preserving historical remaining ranges as provenance.

Current M48 sync report:

```yaml
control_plane_sync_status: done_through_m48
source_registry_synced: true
track10_backlog_synced: true
track10_plan_synced: true
root_control_plane_synced: true
root_readme_synced: true
plugin_readme_synced: true
batch34c_scope_note: public_ready_slice_only
batch34e_scope_note: full_site_i18n_parity
```

M48 performs no live server launch, browser automation, provider/live external model/API call, canonical graph mutation, plugin publication, external write or git stage/commit/push/PR.

## B34E-I18N-M49 Final Full-Site I18N Closure

Status: `done_through_m49`.

M49 records `full_site_i18n_closure` and `full_site_i18n_final_evidence` for the full documentation site. The final closure gate requires source parity, generated RU/EN pages, language-switcher parity, search/sitemap coverage, RU/EN content scans, `python tools\check_docs.py`, strict MkDocs and `git diff --check`.

Current final closure report:

```yaml
full_site_i18n_closure: true
full_site_i18n_final_evidence: true
strict_mkdocs_final_closure_exit_code: 0
docs_ru_pages_total: 127
english_original_pages_total: 7
localized_ru_pages_total: 120
existing_en_siblings: 120
missing_localized_en_siblings: 0
rendered_ru_pages_checked: 120
rendered_en_pages_checked: 120
static_language_switcher_pairs_checked: 120
language_switcher_pair_failures: 0
file_url_escape_failures: 0
search_index_ru_pages_present: 120
search_index_en_pages_present: 120
sitemap_ru_pages_present: 120
sitemap_en_pages_present: 120
search_index_missing_ru_pages: 0
search_index_missing_en_pages: 0
sitemap_missing_ru_pages: 0
sitemap_missing_en_pages: 0
search_index_ru_fallback_pollution: 0
sitemap_ru_fallback_pollution: 0
en_source_cyrillic_hits: 0
en_source_mojibake_hits: 0
en_source_transliteration_hits: 0
en_internal_link_failures: 0
ru_source_forbidden_english_phrase_hits: 0
no_remaining_batch34e_gates: true
```

M49 closes Batch 34E full-site bilingual documentation parity. Batch 35 remains a separate approval-bound real-testing matrix and is not authorized by this closure.

## Initial M35 Missing EN Siblings By Section

### agent-systems (6)

- `agent-systems/evals-observability.md`
- `agent-systems/memory.md`
- `agent-systems/overview.md`
- `agent-systems/sdk-patterns.md`
- `agent-systems/session-control.md`
- `agent-systems/templates.md`

### artifact-templates (5)

- `artifact-templates/control-plane-files.md`
- `artifact-templates/plugin-blueprint.md`
- `artifact-templates/product-skill.md`
- `artifact-templates/prompt-packet.md`
- `artifact-templates/runlog.md`

### codex (6)

- `codex/configuration.md`
- `codex/overview.md`
- `codex/security.md`
- `codex/surfaces.md`
- `codex/use-cases-deep-analysis.md`
- `codex/workflows.md`

### insights (3)

- `insights/index.md`
- `insights/insight-card-template.md`
- `insights/seed-insights.md`

### methodologies (13)

- `methodologies/api-integrations.md`
- `methodologies/backend.md`
- `methodologies/business-product.md`
- `methodologies/codex-agentic-workflow.md`
- `methodologies/database-data.md`
- `methodologies/delivery-release-operations.md`
- `methodologies/frontend.md`
- `methodologies/index.md`
- `methodologies/llm-ai-rag.md`
- `methodologies/quality-testing-evals.md`
- `methodologies/requirements-domain.md`
- `methodologies/security-privacy-compliance.md`
- `methodologies/solution-architecture.md`

### playbooks (10)

- `playbooks/ai-team-design.md`
- `playbooks/build-full-feature.md`
- `playbooks/code-review.md`
- `playbooks/context7-deep-research.md`
- `playbooks/eval-driven-improvement.md`
- `playbooks/grounded-answering.md`
- `playbooks/maintain-agent-operating-docs.md`
- `playbooks/product-ready-pr.md`
- `playbooks/research-loop.md`
- `playbooks/workflow-to-skill.md`

### prompting (4)

- `prompting/anti-hallucination.md`
- `prompting/context-engineering.md`
- `prompting/overview.md`
- `prompting/question-design.md`

### sources (30)

- `sources/add-ddd-tdd-fsd-llm-development.md`
- `sources/context7-research.md`
- `sources/deep-research-report.md`
- `sources/development-methodology-gap-matrix.md`
- `sources/development-methodology-research-log.md`
- `sources/methodology-research/api-integrations.md`
- `sources/methodology-research/backend.md`
- `sources/methodology-research/business-product.md`
- `sources/methodology-research/codex-agentic-workflow.md`
- `sources/methodology-research/database-data.md`
- `sources/methodology-research/delivery-release-operations.md`
- `sources/methodology-research/frontend.md`
- `sources/methodology-research/llm-ai-rag.md`
- `sources/methodology-research/quality-testing-evals.md`
- `sources/methodology-research/requirements-domain.md`
- `sources/methodology-research/security-privacy-compliance.md`
- `sources/methodology-research/solution-architecture.md`
- `sources/product-agent-os-batch34-packaging-install-smoke.md`
- `sources/product-agent-os-batch34a-public-docs-boundary.md`
- `sources/product-agent-os-batch34b-public-copy-rewrite.md`
- `sources/product-agent-os-batch34c-i18n-localization.md`
- `sources/product-agent-os-batch34d-product-docs-qa-closure.md`
- `sources/product-agent-os-batch35-approval-packet-draft.md`
- `sources/product-agent-os-final-predevelopment-review.md`
- `sources/product-agent-os-pre-track-8-implementation-inventory.md`
- `sources/product-agent-os-track-10-backlog.md`
- `sources/product-agent-os-track-8-detailed-backlog.md`
- `sources/product-agent-os-track-9-backlog.md`
- `sources/registry.md`
- `sources/source-card-template.md`

### superpowers (13)

- `superpowers/plans/2026-05-14-product-agent-os-generated-infrastructure.md`
- `superpowers/plans/2026-05-14-product-agent-os-lifecycle-skills.md`
- `superpowers/plans/2026-05-14-product-agent-os-plugin-core.md`
- `superpowers/plans/2026-05-14-product-agent-os-production-hardening.md`
- `superpowers/plans/2026-05-15-product-agent-os-codex-runtime-runner.md`
- `superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`
- `superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md`
- `superpowers/specs/2026-05-14-product-agent-os-agents-sdk-runner-design.md`
- `superpowers/specs/2026-05-14-product-agent-os-generated-infrastructure-design.md`
- `superpowers/specs/2026-05-14-product-agent-os-lifecycle-skills-design.md`
- `superpowers/specs/2026-05-14-product-agent-os-production-hardening-design.md`
- `superpowers/specs/2026-05-15-product-agent-os-codex-runtime-runner-design.md`
- `superpowers/specs/2026-05-25-track-9-methodology-intelligence-design.md`

## Boundary

- staged evidence only;
- source-level EN sibling parity is complete after M43;
- full bilingual closure is reached after M49;
- `no missing-page language-switcher fallback` is supported by final M49 closure evidence;
- M44 has run EN editorial quality sweep;
- M45 has run RU quality sweep;
- M46 has run full-site language switcher parity on generated `site/`;
- M47 has verified search and sitemap parity on generated `site/`;
- M48 has synchronized source/control-plane artifacts;
- M49 has recorded `full_site_i18n_closure` and `full_site_i18n_final_evidence`;
- no remaining Batch 34E gates;
- no live server;
- no browser automation;
- no provider/live external model/API calls;
- no canonical graph mutation;
- no plugin publication;
- external write is not performed;
- no git stage/commit/push/PR.
