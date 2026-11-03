# Обновление документации GPT-6: подробный план и доказательства

Source status: `official + experiment`

Документационное выполнение 20 пунктов аудита от 3 ноября. Действующие model pins, permissions, агенты, hooks и реализация сохраняются. Пункты 1, 2 и 4 закрываются только на уровне документации; технические зависимости остаются открытыми.

- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Root task: PAOS-DOCS-REFRESH-2026-11-03
- Machine status: `docs/superpowers/specs/gpt6-documentation-refresh-task-group.json`
- Evidence owner: root documentation maintainer; one writer, no delegated agents.
- Skills: repository implementation-planner and docs-maintainer; openai-docs.

## Stages / Этапы

| Stage | Scope | Depends on | Gate |
| --- | --- | --- | --- |
| E0 | Baseline, sources, ownership and detailed plan | none | Baseline hashes, source review, valid task matrix |
| E1 | 1, 2, 5, 6, 7, 8, 9, 10 | E0 | Source agreement, TOML parsing, trust boundaries |
| E2 | 3, 4, 12 | E1 | One model matrix; no active model changes |
| E3 | 13, 14, 16 | E2 | Reproducible migration design; no live eval |
| E4 | 15, 17, 18, 19, 20 | E1-E3 | API/state/activation contracts and claim review |
| E5 | 11; semantic parity across all items | E1-E4 | RU/EN, registry, navigation and links |
| E6 | Acceptance, status and handoff | E5 | Mandatory checks, strict build, protected-file hashes |

## Verification commands / Команды проверки

Run from the repository root. Each command must exit 0; failures remain visible and are not waived. No provider, browser or live server is part of these checks.

```powershell
python plugins\product-agent-os\scripts\validate_task_matrix.py docs/superpowers/plans/2026-11-03-gpt6-documentation-refresh.md
python plugins\product-agent-os\scripts\validate_task_matrix.py docs/superpowers/plans/2026-11-03-gpt6-documentation-refresh.en.md
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v
python -m unittest tests.product_agent_os.test_lifecycle_hooks -v
python plugins\product-agent-os\scripts\validate_hooks.py .codex\hooks.json
python plugins\product-agent-os\scripts\validate_hooks.py .codex\hooks
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
python tools\check_docs.py
git diff --check
.venv-docs\Scripts\python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/gpt6-docs-preview
```

Additional checks: tomllib for complete TOML examples; JSON parsing; RU/EN claim parity; changed official links and anchors; all 20 IDs and acyclic dependencies; SHA-256 comparison of the 17 pre-existing dirty files and protected implementation/history/site files. Preview build proves local generation only.

## Ownership, rollback and exclusions / Границы

Owned: the page pairs named below, mkdocs.yml, this plan pair/task group, source registries, REQUIREMENTS.md, PLAN.md, TEST.md, EVALS.md, RUNLOG.md and the current lifecycle marker. Sources are rechecked before changing platform claims. Forbidden: implementation, validators, test logic (only page-inventory metadata is in scope), agent profiles, executable templates, active model/permission settings, hooks, frozen evidence, prod_test.md, root site output and Git publication. Rollback only this slice using the initial diff; preserve unrelated edits. No dependency installation.

TDD, FSD and domain-model scaffolding: not_applicable to this documentation-only slice. No new persistent validator or artificial RED tests. Plan quality: exact files, per-item acceptance, dependencies, owner, checks and rollback below. No broad release, account availability or runtime activation claim.

## Technical follow-up / Технические зависимости

- OPEN-PERM: .codex/config.toml, .codex/agents/*.toml and agent-context-contract.json versus inherited parent permissions; owner: runtime maintainer; separate authorized implementation and fresh-session proof.
- OPEN-MCP: plugins/product-agent-os/scripts/product_agent_os/validators.py requires agent-local MCP; owner: runtime maintainer; align parent MCP contract and focused tests in a separate task.
- OPEN-MODEL: model allowlist, active and packaged profiles, both model-reasoning-policy templates remain GPT-5.6; owner: model migration reviewer; no switch until availability, fixed baseline and authorized eval.
- OPEN-RUNTIME: documented API capabilities are not newly activated Product-Agent OS paths; owner: architect; separate implementation acceptance.
- OPEN-BASELINE: current agent validator requires sandbox_mode while dirty config uses default_permissions; record failure separately; do not weaken checks.

### Task `DOC6-01`

- Task: DOC6-01 — Изоляция custom agents
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: E0 baseline
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/agent-configuration/subagents
- Short description: Разделить поведенческий запрет записи и наследуемые технические permissions. Для заявления об изоляции требовать доказательство из свежей сессии.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/product-agent/roles.md, docs/product-agent/roles.en.md, docs/codex/security.md, docs/codex/security.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Разделить поведенческий запрет записи и наследуемые технические permissions. Для заявления об изоляции требовать доказательство из свежей сессии.
- Acceptance criteria: Разделить поведенческий запрет записи и наследуемые технические permissions. Для заявления об изоляции требовать доказательство из свежей сессии. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/product-agent/roles.md, docs/product-agent/roles.en.md, docs/codex/security.md, docs/codex/security.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Разделить поведенческий запрет записи и наследуемые технические permissions. Для заявления об изоляции требовать доказательство из свежей сессии.
- files touched / work locations: docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/product-agent/roles.md, docs/product-agent/roles.en.md, docs/codex/security.md, docs/codex/security.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-02`

- Task: DOC6-02 — Наследование MCP
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-01
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/agent-configuration/subagents
- Short description: Описать наследование MCP родителя; декларация не доказывает доступность инструмента. Несоответствие валидатора оставить технической зависимостью.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Описать наследование MCP родителя; декларация не доказывает доступность инструмента. Несоответствие валидатора оставить технической зависимостью.
- Acceptance criteria: Описать наследование MCP родителя; декларация не доказывает доступность инструмента. Несоответствие валидатора оставить технической зависимостью. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Описать наследование MCP родителя; декларация не доказывает доступность инструмента. Несоответствие валидатора оставить технической зависимостью.
- files touched / work locations: docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-03`

- Task: DOC6-03 — Актуальные рекомендации моделей
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-12
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/models
- Short description: Заменить устаревшие действующие рекомендации ссылкой на модельную матрицу; указать продукт и auth mode для retirement; сохранить исторические ID.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E2; docs/product-agent/roles.md, docs/product-agent/roles.en.md, docs/diagrams/agent-team-and-skills.md, docs/diagrams/agent-team-and-skills.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Заменить устаревшие действующие рекомендации ссылкой на модельную матрицу; указать продукт и auth mode для retirement; сохранить исторические ID.
- Acceptance criteria: Заменить устаревшие действующие рекомендации ссылкой на модельную матрицу; указать продукт и auth mode для retirement; сохранить исторические ID. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/product-agent/roles.md, docs/product-agent/roles.en.md, docs/diagrams/agent-team-and-skills.md, docs/diagrams/agent-team-and-skills.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Заменить устаревшие действующие рекомендации ссылкой на модельную матрицу; указать продукт и auth mode для retirement; сохранить исторические ID.
- files touched / work locations: docs/product-agent/roles.md, docs/product-agent/roles.en.md, docs/diagrams/agent-team-and-skills.md, docs/diagrams/agent-team-and-skills.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-04`

- Task: DOC6-04 — Действующая и кандидатная политика
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-12, DOC6-01, DOC6-02
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/latest-model
- Short description: Разделить действующие GPT-5.6 pins, кандидатов GPT-6 и подтвержденное promotion; перечислить config, templates и validators без их изменения.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E2; docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Разделить действующие GPT-5.6 pins, кандидатов GPT-6 и подтвержденное promotion; перечислить config, templates и validators без их изменения.
- Acceptance criteria: Разделить действующие GPT-5.6 pins, кандидатов GPT-6 и подтвержденное promotion; перечислить config, templates и validators без их изменения. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Разделить действующие GPT-5.6 pins, кандидатов GPT-6 и подтвержденное promotion; перечислить config, templates и validators без их изменения.
- files touched / work locations: docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-05`

- Task: DOC6-05 — Значения approval policy
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-10
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/config-file/config-reference
- Short description: Убрать untrusted из действующих примеров; описать версионную границу и смысл on-request/never.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/codex/configuration.md, docs/codex/configuration.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Убрать untrusted из действующих примеров; описать версионную границу и смысл on-request/never.
- Acceptance criteria: Убрать untrusted из действующих примеров; описать версионную границу и смысл on-request/never. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/codex/configuration.md, docs/codex/configuration.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Убрать untrusted из действующих примеров; описать версионную границу и смысл on-request/never.
- files touched / work locations: docs/codex/configuration.md, docs/codex/configuration.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-06`

- Task: DOC6-06 — Granular TOML и категории запросов
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-05
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/config-file/config-reference
- Short description: Обеспечить разбор полных TOML-примеров через tomllib; описать skill_approval как skill-script approval prompts, а не вызов skill.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/codex/configuration.md, docs/codex/configuration.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Обеспечить разбор полных TOML-примеров через tomllib; описать skill_approval как skill-script approval prompts, а не вызов skill.
- Acceptance criteria: Обеспечить разбор полных TOML-примеров через tomllib; описать skill_approval как skill-script approval prompts, а не вызов skill. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/codex/configuration.md, docs/codex/configuration.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Обеспечить разбор полных TOML-примеров через tomllib; описать skill_approval как skill-script approval prompts, а не вызов skill.
- files touched / work locations: docs/codex/configuration.md, docs/codex/configuration.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-07`

- Task: DOC6-07 — Permission profiles
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-01, DOC6-05
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/permissions
- Short description: Описать beta profiles, legacy selection, защищенные пути и несовместимость смешивания; действующие настройки не менять.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/codex/configuration.md, docs/codex/configuration.en.md, docs/codex/security.md, docs/codex/security.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Описать beta profiles, legacy selection, защищенные пути и несовместимость смешивания; действующие настройки не менять.
- Acceptance criteria: Описать beta profiles, legacy selection, защищенные пути и несовместимость смешивания; действующие настройки не менять. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/codex/configuration.md, docs/codex/configuration.en.md, docs/codex/security.md, docs/codex/security.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Описать beta profiles, legacy selection, защищенные пути и несовместимость смешивания; действующие настройки не менять.
- files touched / work locations: docs/codex/configuration.md, docs/codex/configuration.en.md, docs/codex/security.md, docs/codex/security.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-08`

- Task: DOC6-08 — Сетевые поверхности
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-07
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/permissions
- Short description: Отдельно описать локальные команды, web, MCP, connectors и browser; domain rules требуют активного command network proxy.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/codex/security.md, docs/codex/security.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Отдельно описать локальные команды, web, MCP, connectors и browser; domain rules требуют активного command network proxy.
- Acceptance criteria: Отдельно описать локальные команды, web, MCP, connectors и browser; domain rules требуют активного command network proxy. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/codex/security.md, docs/codex/security.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Отдельно описать локальные команды, web, MCP, connectors и browser; domain rules требуют активного command network proxy.
- files touched / work locations: docs/codex/security.md, docs/codex/security.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-09`

- Task: DOC6-09 — Условия делегации
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-01, DOC6-10
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/agent-configuration/subagents
- Short description: Исправить few-shot и общее правило; разделить явный запрос/применимые инструкции, строгую политику проекта и Work Ultra.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/prompting/question-design.md, docs/prompting/question-design.en.md, docs/diagrams/agent-team-and-skills.md, docs/diagrams/agent-team-and-skills.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Исправить few-shot и общее правило; разделить явный запрос/применимые инструкции, строгую политику проекта и Work Ultra.
- Acceptance criteria: Исправить few-shot и общее правило; разделить явный запрос/применимые инструкции, строгую политику проекта и Work Ultra. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/prompting/question-design.md, docs/prompting/question-design.en.md, docs/diagrams/agent-team-and-skills.md, docs/diagrams/agent-team-and-skills.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Исправить few-shot и общее правило; разделить явный запрос/применимые инструкции, строгую политику проекта и Work Ultra.
- files touched / work locations: docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/prompting/question-design.md, docs/prompting/question-design.en.md, docs/diagrams/agent-team-and-skills.md, docs/diagrams/agent-team-and-skills.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-10`

- Task: DOC6-10 — Инструкции и достоверность фактов
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: E0 baseline
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/agent-configuration/agents-md
- Short description: Разделить полномочия инструкций и источники фактов; описать discovery AGENTS, override, scope и лимит 32 KiB по умолчанию.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/diagrams/context-memory-verification.md, docs/diagrams/context-memory-verification.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Разделить полномочия инструкций и источники фактов; описать discovery AGENTS, override, scope и лимит 32 KiB по умолчанию.
- Acceptance criteria: Разделить полномочия инструкций и источники фактов; описать discovery AGENTS, override, scope и лимит 32 KiB по умолчанию. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/diagrams/context-memory-verification.md, docs/diagrams/context-memory-verification.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Разделить полномочия инструкций и источники фактов; описать discovery AGENTS, override, scope и лимит 32 KiB по умолчанию.
- files touched / work locations: docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/diagrams/context-memory-verification.md, docs/diagrams/context-memory-verification.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-11`

- Task: DOC6-11 — RU/EN, ссылки и навигация
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-01, DOC6-02, DOC6-03, DOC6-04, DOC6-05, DOC6-06, DOC6-07, DOC6-08, DOC6-09, DOC6-10, DOC6-12, DOC6-13, DOC6-14, DOC6-15, DOC6-16, DOC6-17, DOC6-18, DOC6-19, DOC6-20
- Blocks: E6 final acceptance
- Source: https://learn.chatgpt.com/docs/models
- Short description: Сверить смысловую RU/EN-парность и canonical source mapping; сохранить исторические ссылки; включить новые страницы в обе навигации; проверить strict build.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E5; docs/sources/registry.md, docs/sources/registry.en.md, docs/diagrams/index.md, docs/diagrams/index.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, mkdocs.yml
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Сверить смысловую RU/EN-парность и canonical source mapping; сохранить исторические ссылки; включить новые страницы в обе навигации; проверить strict build.
- Acceptance criteria: Сверить смысловую RU/EN-парность и canonical source mapping; сохранить исторические ссылки; включить новые страницы в обе навигации; проверить strict build. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: high
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/sources/registry.md, docs/sources/registry.en.md, docs/diagrams/index.md, docs/diagrams/index.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, mkdocs.yml
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Сверить смысловую RU/EN-парность и canonical source mapping; сохранить исторические ссылки; включить новые страницы в обе навигации; проверить strict build.
- files touched / work locations: docs/sources/registry.md, docs/sources/registry.en.md, docs/diagrams/index.md, docs/diagrams/index.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, mkdocs.yml
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-12`

- Task: DOC6-12 — Матрица моделей и reasoning
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-07, DOC6-09
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/latest-model
- Short description: Создать единую матрицу model ID, surface/auth, условий клиента, effort, tools, context и непроверенной доступности аккаунту; не переносить Ultra в API effort.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E2; docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/codex/configuration.md, docs/codex/configuration.en.md, docs/codex/surfaces.md, docs/codex/surfaces.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Создать единую матрицу model ID, surface/auth, условий клиента, effort, tools, context и непроверенной доступности аккаунту; не переносить Ultra в API effort.
- Acceptance criteria: Создать единую матрицу model ID, surface/auth, условий клиента, effort, tools, context и непроверенной доступности аккаунту; не переносить Ultra в API effort. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: high
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/codex/configuration.md, docs/codex/configuration.en.md, docs/codex/surfaces.md, docs/codex/surfaces.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Создать единую матрицу model ID, surface/auth, условий клиента, effort, tools, context и непроверенной доступности аккаунту; не переносить Ultra в API effort.
- files touched / work locations: docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/codex/configuration.md, docs/codex/configuration.en.md, docs/codex/surfaces.md, docs/codex/surfaces.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-13`

- Task: DOC6-13 — Миграция и оценка
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-04, DOC6-12
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/latest-model
- Short description: Определить frozen baseline, сравнения одной переменной, заранее выбранные пороги, corpus, stop/rollback и границу доказательств; без вызовов моделей.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E3; docs/playbooks/model-migration.md, docs/playbooks/model-migration.en.md, docs/agent-systems/evals-observability.md, docs/agent-systems/evals-observability.en.md, EVALS.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Определить frozen baseline, сравнения одной переменной, заранее выбранные пороги, corpus, stop/rollback и границу доказательств; без вызовов моделей.
- Acceptance criteria: Определить frozen baseline, сравнения одной переменной, заранее выбранные пороги, corpus, stop/rollback и границу доказательств; без вызовов моделей. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/playbooks/model-migration.md, docs/playbooks/model-migration.en.md, docs/agent-systems/evals-observability.md, docs/agent-systems/evals-observability.en.md, EVALS.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Определить frozen baseline, сравнения одной переменной, заранее выбранные пороги, corpus, stop/rollback и границу доказательств; без вызовов моделей.
- files touched / work locations: docs/playbooks/model-migration.md, docs/playbooks/model-migration.en.md, docs/agent-systems/evals-observability.md, docs/agent-systems/evals-observability.en.md, EVALS.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-14`

- Task: DOC6-14 — Prompting GPT-6
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-09, DOC6-10, DOC6-13
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/latest-model
- Short description: Описать инициативу в scope, подготовку до approval, конфликт инструкций и соразмерную проверку без изменения действующих prompts.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E3; docs/prompting/overview.md, docs/prompting/overview.en.md, docs/prompting/question-design.md, docs/prompting/question-design.en.md, docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Описать инициативу в scope, подготовку до approval, конфликт инструкций и соразмерную проверку без изменения действующих prompts.
- Acceptance criteria: Описать инициативу в scope, подготовку до approval, конфликт инструкций и соразмерную проверку без изменения действующих prompts. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/prompting/overview.md, docs/prompting/overview.en.md, docs/prompting/question-design.md, docs/prompting/question-design.en.md, docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Описать инициативу в scope, подготовку до approval, конфликт инструкций и соразмерную проверку без изменения действующих prompts.
- files touched / work locations: docs/prompting/overview.md, docs/prompting/overview.en.md, docs/prompting/question-design.md, docs/prompting/question-design.en.md, docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-15`

- Task: DOC6-15 — API-совместимость
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-12, DOC6-19
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/latest-model
- Short description: Сопоставить model/endpoint/tools/reasoning/sampling; разделить ключи Responses и Chat Completions; не заменять CLI runner.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E4; docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Сопоставить model/endpoint/tools/reasoning/sampling; разделить ключи Responses и Chat Completions; не заменять CLI runner.
- Acceptance criteria: Сопоставить model/endpoint/tools/reasoning/sampling; разделить ключи Responses и Chat Completions; не заменять CLI runner. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Сопоставить model/endpoint/tools/reasoning/sampling; разделить ключи Responses и Chat Completions; не заменять CLI runner.
- files touched / work locations: docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-16`

- Task: DOC6-16 — Стоимость, caching и контекст
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-12, DOC6-13
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/prompt-caching
- Short description: Описать cache reads/writes, retention, tiers, условия стоимости контекста и стоимость завершенной задачи; отделить API billing от подписки, cache от memory.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E3; docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/agent-systems/evals-observability.md, docs/agent-systems/evals-observability.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/playbooks/model-migration.md, docs/playbooks/model-migration.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Описать cache reads/writes, retention, tiers, условия стоимости контекста и стоимость завершенной задачи; отделить API billing от подписки, cache от memory.
- Acceptance criteria: Описать cache reads/writes, retention, tiers, условия стоимости контекста и стоимость завершенной задачи; отделить API billing от подписки, cache от memory. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/agent-systems/evals-observability.md, docs/agent-systems/evals-observability.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/playbooks/model-migration.md, docs/playbooks/model-migration.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Описать cache reads/writes, retention, tiers, условия стоимости контекста и стоимость завершенной задачи; отделить API billing от подписки, cache от memory.
- files touched / work locations: docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/agent-systems/evals-observability.md, docs/agent-systems/evals-observability.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/playbooks/model-migration.md, docs/playbooks/model-migration.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-17`

- Task: DOC6-17 — Async tools и steering
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-15, DOC6-19
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/async-tool-calling
- Short description: Описать pending calls, call_id, deadlines, повторные/поздние результаты и accepted/applied steering; не обещать отмену или hosted tool execution.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E4; docs/agent-systems/session-control.md, docs/agent-systems/session-control.en.md, docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Описать pending calls, call_id, deadlines, повторные/поздние результаты и accepted/applied steering; не обещать отмену или hosted tool execution.
- Acceptance criteria: Описать pending calls, call_id, deadlines, повторные/поздние результаты и accepted/applied steering; не обещать отмену или hosted tool execution. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/agent-systems/session-control.md, docs/agent-systems/session-control.en.md, docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Описать pending calls, call_id, deadlines, повторные/поздние результаты и accepted/applied steering; не обещать отмену или hosted tool execution.
- files touched / work locations: docs/agent-systems/session-control.md, docs/agent-systems/session-control.en.md, docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-18`

- Task: DOC6-18 — Reasoning updates и compaction
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-16, DOC6-17
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/reasoning
- Short description: Разделить steering, reset, summary, compaction и memory; описать совместимость configuration_update и восстановление после explicit compaction.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E4; docs/agent-systems/session-control.md, docs/agent-systems/session-control.en.md, docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/diagrams/context-memory-verification.md, docs/diagrams/context-memory-verification.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Разделить steering, reset, summary, compaction и memory; описать совместимость configuration_update и восстановление после explicit compaction.
- Acceptance criteria: Разделить steering, reset, summary, compaction и memory; описать совместимость configuration_update и восстановление после explicit compaction. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/agent-systems/session-control.md, docs/agent-systems/session-control.en.md, docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/diagrams/context-memory-verification.md, docs/diagrams/context-memory-verification.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Разделить steering, reset, summary, compaction и memory; описать совместимость configuration_update и восстановление после explicit compaction.
- files touched / work locations: docs/agent-systems/session-control.md, docs/agent-systems/session-control.en.md, docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/diagrams/context-memory-verification.md, docs/diagrams/context-memory-verification.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-19`

- Task: DOC6-19 — Карта agent runtimes
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-01, DOC6-02, DOC6-12, DOC6-13
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/agents
- Short description: Сравнить Agents API, SDK, Responses API/Multi-agent и Codex subagents по владению state/tools/execution; отметить beta и пробелы реализации проекта.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E4; docs/runtime/overview.md, docs/runtime/overview.en.md, docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md, docs/diagrams/runtime-decision-map.md, docs/diagrams/runtime-decision-map.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Сравнить Agents API, SDK, Responses API/Multi-agent и Codex subagents по владению state/tools/execution; отметить beta и пробелы реализации проекта.
- Acceptance criteria: Сравнить Agents API, SDK, Responses API/Multi-agent и Codex subagents по владению state/tools/execution; отметить beta и пробелы реализации проекта. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: high
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/runtime/overview.md, docs/runtime/overview.en.md, docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md, docs/diagrams/runtime-decision-map.md, docs/diagrams/runtime-decision-map.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Сравнить Agents API, SDK, Responses API/Multi-agent и Codex subagents по владению state/tools/execution; отметить beta и пробелы реализации проекта.
- files touched / work locations: docs/runtime/overview.md, docs/runtime/overview.en.md, docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md, docs/diagrams/runtime-decision-map.md, docs/diagrams/runtime-decision-map.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-20`

- Task: DOC6-20 — Trust и активация hooks
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-01, DOC6-07
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/hooks
- Short description: Описать hash trust, events/handlers, timeouts и coverage; разделить static/script/fresh-session evidence и эффекты PreToolUse/PostToolUse/Stop.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E4; docs/runtime/worktrees-hooks-rules.md, docs/runtime/worktrees-hooks-rules.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md, TEST.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Описать hash trust, events/handlers, timeouts и coverage; разделить static/script/fresh-session evidence и эффекты PreToolUse/PostToolUse/Stop.
- Acceptance criteria: Описать hash trust, events/handlers, timeouts и coverage; разделить static/script/fresh-session evidence и эффекты PreToolUse/PostToolUse/Stop. RU/EN agree; official source and applicability are visible; protected files unchanged.
- Verification gates: Official source comparison; changed example parsing; mandatory commands above exit 0; semantic RU/EN review; strict preview build for nav/diagram edits
- Risks / approval gates: Platform drift and existing implementation mismatch; no silent promotion; live verification remains separately approval-bound
- Complexity: medium
- Estimated execution time: 30-90 minutes; shared checks run once per changed package
- Agents: Root docs maintainer; sequential source and self-review responsibilities
- Skills: implementation-planner; docs-maintainer; openai-docs
- Output artifacts: docs/runtime/worktrees-hooks-rules.md, docs/runtime/worktrees-hooks-rules.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md, TEST.md
- Next step: Review linked technical dependencies without changing runtime

#### Completion Report

- status: implemented
- what was done: Описать hash trust, events/handlers, timeouts и coverage; разделить static/script/fresh-session evidence и эффекты PreToolUse/PostToolUse/Stop.
- files touched / work locations: docs/runtime/worktrees-hooks-rules.md, docs/runtime/worktrees-hooks-rules.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md, TEST.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

## Completion assurance / Проверка завершения

Doubt packet: not_required as a separate artifact; explicit root self-review uses the 20-item acceptance matrix, current command receipts and protected-file comparison. Supported claim: documentation corrections only. Unsupported: model promotion, live isolation/MCP/hook activation, release readiness. No provider/model/browser/server/Git/external writes performed.

## Результаты проверки — 2026-11-03

Все 20 документационных пунктов выполнены. Этапы Э0–Э6 завершены в документационном scope; технические зависимости остаются открытыми. Ниже результаты текущего запуска, а не повторное использование исторических результатов. После записи статусов выполняется финальная проверка затронутых документов; результаты hooks/templates переиспользуются при неизменных исходниках.

| Command | Exit | Observed result |
| --- | --- | --- |
| `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | 0 | Ran 100 tests in 2.711s; OK |
| `python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v` | 0 | Ran 5 tests in 0.665s; OK |
| `python -m unittest tests.product_agent_os.test_lifecycle_hooks -v` | 0 | Ran 25 tests in 3.245s; OK |
| `python plugins/product-agent-os/scripts/validate_hooks.py .codex/hooks.json` | 0 | No errors reported |
| `python plugins/product-agent-os/scripts/validate_hooks.py .codex/hooks` | 0 | No errors reported |
| `python -m unittest tests.product_agent_os.test_infrastructure_templates -v` | 0 | Ran 94 tests in 1.846s; OK |
| `python tools/check_docs.py` | 0 | OK: documentation structure checks passed |
| `python plugins/product-agent-os/scripts/validate_task_matrix.py docs/superpowers/plans/2026-11-03-gpt6-documentation-refresh.md` | 0 | No errors reported |
| `python plugins/product-agent-os/scripts/validate_task_matrix.py docs/superpowers/plans/2026-11-03-gpt6-documentation-refresh.en.md` | 0 | No errors reported |
| `python plugins/product-agent-os/scripts/validate_task_state_consistency.py` | 0 | No errors reported |
| `git diff --check` | 0 | No errors reported |
| `.venv-docs\Scripts\python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/gpt6-docs-preview` | 0 | Documentation built in 25.42 seconds |


Статическая приемка: прочитаны 20 официальных источников; 48 измененных/новых Markdown-файлов прочитаны как UTF-8; разобраны 10 полных TOML/JSON-блоков; официальные URL совпадают в RU/EN-парах. Проверены все 20 строк приемки, границы source/runtime, сочетания параметров, примеры делегации и отсутствие promotion claims. Это явная самопроверка основного агента, не независимый reviewer run. Проверены Mermaid source и strict generation; browser rendering не запускался.

Первая попытка после создания плана: 224 теста, 15 failures/33 errors. Причины включали права inherited TEMP, счетчики страниц, русские заголовки в EN-плане и legacy validator с привязкой к августовскому плану. Исправления сохранили assertions и реализацию. Pass1 выявил 10 редакционных failures, четыре ошибки hook-fixtures и две strict-link warnings. Тексты/ссылки исправлены; hooks прошли с изолированным OS TEMP вне репозитория. TEMP внутри Git-корня приводил к чтению реального marker вместо fixture; поведение hook ради тестов не менялось.

Изменения тестовых метаданных: 160 buildable / 150 localized source pages; исторический site-promoted count остается 143. Три новые пары явно ожидают root-site promotion. Августовский план дополнен только датированным указателем для discovery текущей задачи. Эти ограниченные корректировки не меняют логику тестов или исторические результаты.

Сверка SHA-256: сохранены все 17 исходных измененных config/profile/eval файлов и 1658 защищенных файлов implementation/tests/hooks/templates/root site; исключения — разрешенный lifecycle marker и явно указанный файл метаданных inventory. Не выполнялись переключение моделей, изменение permissions/config/profiles/hooks, live model/provider calls, browser automation, запуск сервера, операции с Git-историей проекта, публикация или deployment. Тесты могут создавать временные fixture repositories.

Известная диагностика вне scope: `python plugins/product-agent-os/scripts/validate_agents.py .codex/agents` возвращает 1 и `project config must set sandbox_mode = workspace-write`. Прежнее расхождение реализации остается OPEN-BASELINE и не выдается за успешную проверку. OPEN-PERM, OPEN-MCP и OPEN-MODEL не решены. Завершение документации не означает общую compatibility, isolation, activation, promotion или release acceptance.

Control-plane sync: REQUIREMENTS, PLAN, TEST, EVALS, RUNLOG обновлены; prod_test.md — not_applicable; overflow refactor не потребовался. Далее — отдельно разрешенная корректировка технических контрактов и оценка; очередь Batch 45 T30 сохранена. Откат касается только этого slice, без потери чужих изменений и исторических evidence.


## Разрешённое техническое продолжение — 2026-11-03

Предыдущие результаты документационного этапа сохраняются как история. Эта отдельно разрешённая задача меняет реализацию и конфигурацию.

### Task `PAOS-CONTRACT-MODEL-ALIGNMENT-2026-11-03`

- Task: PAOS-CONTRACT-MODEL-ALIGNMENT-2026-11-03 — Согласование permissions, MCP, валидаторов и профилей моделей
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner authorizes technical follow-up and model switches on 2026-11-03
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 18:44
- Depends on: DOC6-01, DOC6-02, DOC6-04
- Blocks: fresh-session activation and behavioral promotion
- Source: https://learn.chatgpt.com/docs/agent-configuration/subagents; https://learn.chatgpt.com/docs/permissions; https://learn.chatgpt.com/docs/models
- Short description: Исправлены родительские permissions/MCP и контракты моделей в активных и staged-профилях.
- Technical value: Validators reject unsupported custom-agent overrides and validate inherited parent contracts.
- Product value: Оператор получает согласованные активные профили и безопасные staged-предложения.
- Scope: .codex/config.toml; .codex/agents; .codex/evals/agent-context-contract.json; model policy templates; plugin templates and validators; affected tests; docs and control-plane
- Non-goals: No provider calls, global settings, target mutations, hook activation, Git writes or deployment.
- Expected result: Parent permissions and MCP; preserved effort; role-aware GPT-6 pins; local verification.
- Acceptance criteria: Active and rendered agents validate; legacy composition and agent overrides fail; inherited MCP and disabled skills accepted; mandatory gates pass; runtime gaps explicit.
- Verification gates: RED/GREEN validators; infrastructure tests; full unittest; fixture/transcript evals; Codex compatibility; docs checker; task matrix; state consistency; git diff --check
- Risks / approval gates: Local pins do not prove account access, activation or model quality. Existing dirty work preserved.
- Complexity: high
- Estimated execution time: 45-90 minutes
- Agents: root only
- Skills: openai-docs; python-design-patterns; python-code-style
- Output artifacts: existing plan pair and task group; active/staged contracts; tests; REQUIREMENTS.md, PLAN.md, TEST.md, EVALS.md, RUNLOG.md
- Next step: Collect authorized fresh-session evidence; compare quality/cost/latency before behavioral promotion.

#### Completion Report

- status: implemented
- what was done: Согласованы родительские permissions и наследование MCP; 23 активных и staged-профиля переведены на GPT-6.1 Sol/Terra с сохранением effort. Skills перенесены к родителю. Валидаторы отклоняют неподдерживаемые overrides, renderer проверяет семантику конфигурации, lifecycle validator использует путь к текущему плану.
- files touched / work locations: AGENTS.md; .codex/config.toml, agents, eval contract, lifecycle workflow and two artifact templates; plugin config/agent/eval/workflow/artifact templates; validators.py, infrastructure.py, validate_task_state_consistency.py; five test modules; model/configuration/compatibility/source pages; five control-plane files
- technical value delivered: Supported parent-only controls and model policy enforced locally across active and rendered configurations.
- product value delivered: Consistent reusable profiles and explicit separation of role behavior from sandbox isolation.
- actual implementation date and time: 03-11-2026 18:44
- verification evidence: Ran 1247 tests in 611.387s; OK (skipped=1); fixture/transcript eval, compatibility, 15 active agents, both hook validators, RU/EN task matrices, state consistency, docs checker and diff check exit 0.
- residual risks: Эффективные permissions, MCP, доступность моделей и качество/стоимость/задержка в новой сессии не проверены. Provider-вызовы, browser, активация hooks, изменения целевых проектов, Git publication и обновление корневого site/ не выполнялись.
- follow-up: Authorized fresh-session activation receipt, then fixed-input same-effort comparison before promotion. Batch 45 T30 queue unchanged.


#### Technical verification receipt — 2026-11-03T18:44:23.883770+03:00

| Gate | Exit | Current evidence |
| --- | --- | --- |
| `python -m unittest discover -s tests -p test_*.py -v` | 0 | Ran 1247 tests in 611.387s; OK (skipped=1) |
| `python plugins/product-agent-os/scripts/run_fixture_eval.py` | 0 | 91 fixtures; all ok |
| `python plugins/product-agent-os/scripts/run_transcript_eval.py` | 0 | 26 synthetic transcripts; 26 passed; 0 failed |
| `python plugins/product-agent-os/scripts/validate_codex_compatibility.py` | 0 | 0.12 seconds; local log in .docs-tools/reports/contract-alignment |
| `python plugins/product-agent-os/scripts/validate_agents.py .codex/agents` | 0 | 0.14 seconds; local log in .docs-tools/reports/contract-alignment |
| `python plugins/product-agent-os/scripts/validate_hooks.py .codex/hooks.json` | 0 | 0.11 seconds; local log in .docs-tools/reports/contract-alignment |
| `python plugins/product-agent-os/scripts/validate_hooks.py .codex/hooks` | 0 | 0.16 seconds; local log in .docs-tools/reports/contract-alignment |
| `python plugins/product-agent-os/scripts/validate_task_matrix.py docs/superpowers/plans/2026-11-03-gpt6-documentation-refresh.md` | 0 | 0.12 seconds; local log in .docs-tools/reports/contract-alignment |
| `python plugins/product-agent-os/scripts/validate_task_matrix.py docs/superpowers/plans/2026-11-03-gpt6-documentation-refresh.en.md` | 0 | 0.12 seconds; local log in .docs-tools/reports/contract-alignment |
| `python plugins/product-agent-os/scripts/validate_task_state_consistency.py` | 0 | 0.09 seconds; local log in .docs-tools/reports/contract-alignment |
| `python tools/check_docs.py` | 0 | OK: documentation structure checks passed |
| `git diff --check` | 0 | 0.24 seconds; local log in .docs-tools/reports/contract-alignment |

RED/GREEN: validator suite initially reported 15 expected assertion failures across 34 tests, then 34/34 passed. The first RED shell wrapper returned 0 after printing the log tail; the unittest failure output is the RED evidence. Explicit-plan regression and rendered-config semantic regression each exited 1 before fixes, then the combined lifecycle/templates suite passed 100 tests and renderer/validators suite passed 62 tests.

Static checks: 23 preserved effort baselines, 31 inherited skill paths retained, parent approval contract unchanged, active/staged model-policy and test/eval templates equal, no changes to hooks, original fixtures, historical review evidence, prod_test.md or site/. Python 3.13.5; Codex CLI 0.166.0. CLI startup emitted sandbox temp/PATH-alias warnings; no doctor/network probe or model execution was used.

Initial full discovery: 1247 tests, one failure (obsolete renderer inventory expected 205, actual 207), one Windows-specific skip. The registry hash matched the task-start baseline and registered 207 templates before this task. The exact-count assertion was corrected to 207; the full suite was rerun. The platform skip is test_apply_is_rejected_on_non_windows, correctly skipped on Windows. Standalone fixture eval: 91/91; synthetic transcript eval: 26/26.

Self-review: checked parent-vs-role authority, shared MCP, disabled capability contract, project-policy model allowlist, rendered config validation, explicit-plan containment, preserved baseline and negative tests. Existing APIs/validators reused; standard library only; no dependencies. Comment advisories were reviewed for changed functions; unrelated functions were not rewritten.

Control-plane sync: REQUIREMENTS.md, PLAN.md, TEST.md, EVALS.md and RUNLOG.md updated; prod_test.md not_applicable; no handoff_required or overflow. Rollback only this slice against its captured baseline. Prior model/effort map is in the task-group technical_followup.model_changes; a model rollback also needs an explicit validator-policy exception and must not restore unsupported agent-local access fields.

Evidence ceiling: Fresh-session effective permissions/MCP/model availability and quality/cost/latency comparison remain unverified. No provider calls, browser, hook activation, target mutation, Git publication or root site update.


## Trade lifecycle parity — separately authorized follow-up

### Task `PAOS-TRADE-LIFECYCLE-PARITY-2026-11-03`

- Task: PAOS-TRADE-LIFECYCLE-PARITY-2026-11-03 — Align Task Start Brief and Completion Ledger with Trade
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User requests Trade lifecycle parity
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 19:41
- Depends on: Current contract/model alignment completed
- Blocks: Fresh-session lifecycle activation acceptance
- Source: Trade AGENTS.md, task-start-brief.md, completion-ledger.md and delivery workflow; current PAOS hooks and tests
- Short description: Adopt nine-field start, thirteen-field ledger and conditional packet applicability.
- Technical value: One explicit reporting contract across active/staged workflows and checks.
- Product value: Consistent task communication without unnecessary packets for ordinary work.
- Scope: AGENTS.md; active and packaged lifecycle config/workflows/templates/hooks/evals; lifecycle generator; affected tests; existing docs, plan, task group and control-plane
- Non-goals: No Trade edits, model/permission changes, hook trust activation, providers or Git writes.
- Expected result: Full packets for large/high-risk/financially material implementation, release/readiness or explicit requests; concise ordinary work; legacy compatibility for current sessions.
- Acceptance criteria: Nine start fields; thirteen ledger items; scope classification; empty/missing fields fail; no repeated Stop loop; safety guards preserved; no invented metrics or review; Trade source hashes unchanged.
- Verification gates: Focused RED/GREEN lifecycle and renderer tests; mandatory docs tests and checker; final full unittest and offline evals; plan/state validators; diff check.
- Risks / approval gates: Changed hook and instruction files need fresh trusted-session evidence; local shape checks do not prove semantics or activation.
- Complexity: high
- Estimated execution time: 40-70 minutes
- Agents: root only; no delegation
- Skills: docs-maintainer; python-design-patterns; python-code-style
- Output artifacts: Existing plan pair/task group, lifecycle artifacts, tests and REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG
- Next step: Baseline -> regression tests -> active/staged implementation -> consolidated verification -> status sync.

#### Completion Report

- status: implemented
- what was done: Aligned nine-field scoped Task Start Brief and thirteen-item Completion Ledger; concise ordinary route; advisory Stop; compatible legacy markers; explicit local packet validation; no generated chat duplicates.
- files touched / work locations: Active .codex and packaged lifecycle templates/config/workflows/hooks/evals/profiles; task_plan_lifecycle.py, templates.py, validators.py; affected tests; source registries, docs and five root control-plane files. Exact list: task-group lifecycle_parity.changed_files.
- technical value delivered: One active/staged reporting contract with scoped mutation metadata and terminal guards; no new dependency.
- product value delivered: Trade-style reporting proportional to task scope, without repeated final-answer correction.
- actual implementation date and time: 03-11-2026 19:41
- verification evidence: Final affected-contract gate: 298 tests passed (including 100 documentation tests); 91/91 fixtures and 26/26 synthetic transcripts passed; compatibility is compatible; 15 active agents, hook validators, RU/EN task matrices, task-state consistency, docs structure and diff checks passed. Initial full discovery remains recorded as 1253 tests with two obsolete-name assertion failures and one platform skip; both changed modules and the final 298-test set passed afterward. No live model or fresh-session activation claim.
- residual risks: Fresh trusted-session full/ordinary task behavior, live model compliance and latency remain not_verified; review is self_review. Local checks do not prove product readiness.
- follow-up: After applicable hook trust review, verify one full-scope task and one ordinary task in a fresh Codex session; do not change Trade or trust automatically.


#### Решения lifecycle и границы доказательств

| Контракт | Прежнее поведение PAOS | Эталон Trade и реализованное поведение PAOS |
| --- | --- | --- |
| Старт | 13 полей field-list для немеханической работы | 9 жирных labels с содержимым на следующей строке; условная применимость |
| Завершение | 7 полей и буквальный заголовок Completion Brief | 13 отдельных пунктов ledger; namespace Product-Agent OS |
| Обычная работа | Полный пакет и marker | Краткие Scope/Evidence/Limits и scoped marker перед разрешёнными изменениями |
| Stop | Отклонение формата чата и одна corrective continuation | Только напоминание; явный валидатор пакета работает отдельно |
| Планирование | Генерация копий пакетов чата | Только task detail и Completion Report; без выдуманных delivery, metrics и review |
| Старые сессии | Marker v1 | Совместимость v1; новые задачи используют scoped v2 или concise v1 |
| Защита | Правила command/path/secret, sandbox и approvals | Сохранены; completion_ready дополнительно запрещает дальнейшие изменения |

Trade изучен без изменений. Его актуальный ledger содержит 13 полей; старое описание eleven fields из eval не перенесено. По проверенным путям `.codex/hooks.json` / `.codex/hooks` файлов Trade hooks нет: переносится поведение отчётности, а не предполагаемая реализация hooks Trade. Официальная документация Hooks получена через OpenAI Developers 2026-11-03: https://learn.chatgpt.com/docs/hooks. Stop continuation и hash trust — возможности host; проект выбирает рекомендательную отчётность. Trust, permissions, выбор моделей, providers и Git publication в этом срезе не менялись.

Регрессии: начальные full/concise и Stop tests падали на старом поведении; проверки packet validator и generator падали до реализации; concise bootstrap regression падала до исправления. Первая попытка bootstrap test использовала неверное имя класса и была ошибкой запуска, а не RED; после исправления адреса теста получен ожидаемый отказ missing marker. Последующие фокусные проверки прошли. Полный прогон и итоговые проверки записаны в `lifecycle_parity` существующего task group.

Self-review: переиспользованы lifecycle generator, templates и validators; зависимости не добавлены. Чистый packet validator отделён от hook I/O. С baseline начала задачи сравнены active/staged parity, шесть хешей Trade, настройки 23 профилей, parent configuration вне lifecycle, команды hooks и защитные regex. Изменения только переводов строк восстановлены из baseline. Renderer inventory вырос с 207 до 209 только из-за двух новых packet templates. Canonical graph, корневой site, исходники fixtures, предыдущие receipts и production ledger вне этого среза.

Control-plane sync: REQUIREMENTS — scope/acceptance; PLAN — последовательность и gate; TEST — команды и граница evidence; EVALS — критерии отчётности; RUNLOG — текущая передача результата. `prod_test.md`: not_applicable, поскольку Batch 39 evidence не менялись. Подробности находятся в этом плане и существующем task-group JSON. Отдельная копия пакета чата не сохраняется.

Rollback: восстановить только файлы этого среза из baseline начала задачи с сохранением прежних dirty changes; два новых active/staged packet templates удалять лишь вместе с откатом регистрации и routing. Не использовать destructive Git reset и не менять trust. После отката проверить parity и focused lifecycle contracts. Отдельная приёмка в новой сессии: проверить применимый hash trust hooks, затем наблюдать одну full-scope и одну обычную задачу с реальными markers и финальным ответом. Static fixtures не доказывают соблюдение моделью, независимое review, host activation, latency или production readiness.


### Task `PAOS-LIFECYCLE-ACTIVATION-2026-11-03`

- Task: PAOS-LIFECYCLE-ACTIVATION-2026-11-03 — Verify lifecycle activation in a fresh session
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Explicit user request for fresh-session large and ordinary scenarios
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 20:04
- Depends on: PAOS-TRADE-LIFECYCLE-PARITY-2026-11-03
- Blocks: Closure of activation_pending
- Source: Current lifecycle templates/config and observed Codex host events
- Short description: Observe full and concise reporting plus hook loading in one fresh local chat.
- Technical value: Distinguish host activation from static fixture evidence.
- Product value: Reliable proportionate start and completion reporting.
- Scope: One new local chat, two sequential scenarios, read-only scoped runtime evidence, existing plan/task group/control-plane status updates.
- Non-goals: No implementation, trust, model, permission, Trade, Git, provider or global configuration changes.
- Expected result: Evidence-qualified activation status with explicit failures or unavailable events.
- Acceptance criteria: Large scenario full start/ledger; ordinary concise reporting; host hook event evidence; no post-final tools or corrective format continuation.
- Verification gates: Observe fresh-thread turns and scoped host events; validate packet shape; docs unittest, docs checker, task matrices and diff check.
- Risks / approval gates: No trust bypass; unsupported event evidence remains unverified; one writer owns shared marker.
- Complexity: high
- Estimated execution time: 15-30 minutes
- Agents: root and one user-requested fresh chat, sequential; no subagents
- Skills: openai-docs
- Output artifacts: Existing November plan pair/task group and root control-plane; compact scenario receipts only, no raw transcripts.
- Next step: Fresh large scenario -> ordinary scenario -> inspect host evidence -> status sync.

#### Completion Report

- status: implemented
- what was done: Executed requested fresh-session acceptance and recorded activation_failed; verification task completed, runtime enforcement not accepted.
- files touched / work locations: Existing November plan pair/task-group JSON, root REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG, current-state docs and source registries; synthetic ignored evidence and lifecycle marker.
- technical value delivered: Separated actual injected hook context, displayed reporting, strict parser results and failed host enforcement.
- product value delivered: Prevents promoting activation from static checks while preserving working full/concise reporting.
- actual implementation date and time: 03-11-2026 20:04
- verification evidence: Fresh desktop chat 01a1a250-2429-73b1-91de-3ab6b06c660b: large 9-label start and 13-item ledger observed; strict ledger parser fails presentation/closure syntax; ordinary concise route passed. SessionStart and PostToolUse context observed. Terminal-marker apply_patch negative probe FAILED (sentinel created); direct hook script returns deny. Each scenario has one final, no corrective Stop prompt and no post-final tools. Implementation/trust/model settings unchanged.
- residual risks: ACT-F1 P1 runtime guard failure; ACT-F2 ledger syntax mismatch; four source-contract findings ACT-F3..F6. Exact trust state and silent Stop execution unverified.
- follow-up: Diagnose trust/matcher/response handling without bypass, reconcile contracts under authorized fix scope, rerun same fresh cases; no implementation changes in this verification task.

#### Приёмка активации в новой сессии

Fresh desktop chat 01a1a250-2429-73b1-91de-3ab6b06c660b: large 9-label start and 13-item ledger observed; strict ledger parser fails presentation/closure syntax; ordinary concise route passed. SessionStart and PostToolUse context observed. Terminal-marker apply_patch negative probe FAILED (sentinel created); direct hook script returns deny. Each scenario has one final, no corrective Stop prompt and no post-final tools. Implementation/trust/model settings unchanged.

| Сценарий | Результат | Граница |
| --- | --- | --- |
| Крупный | 9 стартовых полей, 13 пунктов ledger, один финал | Строгий validator отвергает bold labels и отсутствие literal closure_level |
| Обычный | Краткий старт/результат, task_scope_note_v1, точный текст артефакта | Один наблюдаемый малорисковый сценарий |
| Загрузка hooks | Наблюдаются SessionStart и 3 PostToolUse contexts | Exact trusted hashes не доступны |
| Негативный PreToolUse | FAILED: terminal marker не остановил nested apply_patch | Прямой запуск скрипта выдаёт deny; причина в host не установлена |
| Результат Stop | Нет corrective loop и tools после финала | Выполнение молчащего hook не доказано |

Общий результат activation_failed; прежние локальные проверки реализации остаются историческими evidence и не переименовываются. Findings ACT-F1..F6 и точные thread/turn receipts находятся в lifecycle_parity.activation_check. Повтор общего suite не применим: реализация не менялась. Обязательные проверки документов/статусов записываются туда после выполнения. При откате затрагивать только receipts этой проверки и её синтетические файлы; trust и чужие файлы не менять.


### Task `PAOS-LIFECYCLE-REPAIR-2026-11-03`

- Task: PAOS-LIFECYCLE-REPAIR-2026-11-03 — Repair lifecycle guard and six activation findings
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Explicit user request to repair ACT-F1 through ACT-F6 without weakening protection
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 20:52
- Depends on: PAOS-LIFECYCLE-ACTIVATION-2026-11-03 findings
- Blocks: Promotion of runtime lifecycle activation
- Source: Previous fresh-session activation_check and current official Hooks documentation
- Short description: Repair host mutation enforcement and reporting/profile/eval contracts, then repeat fresh-session acceptance.
- Technical value: Align host payload and denial behavior with tested guard semantics.
- Product value: Reliable full/concise reporting and terminal mutation protection.
- Scope: Active/packaged pre-tool hook, ledger validator/template, evals, product-manager profile, skill-routing prose, tests, existing docs/control-plane and fresh local acceptance chat.
- Non-goals: No sandbox/approval weakening, trust bypass, model changes, Trade writes, Git history, providers, deployments or unrelated cleanup.
- Expected result: ACT-F1..F6 repaired with actual host denial and absent sentinel; valid full/ordinary reporting.
- Acceptance criteria: RED/GREEN regressions; preserve safety patterns; full/concise markers; bold/plain ledger and explicit closure; parent-owned skills; Sol identifier; fresh negative probe denied without retries.
- Verification gates: Focused tests, required integrated unittest/fixtures/transcripts/compatibility, docs checks, profiles/hooks/task matrices/state/diff, fresh large/ordinary/negative cases.
- Risks / approval gates: Hook trust review may be required; do not bypass. Static success cannot promote runtime activation.
- Complexity: high
- Estimated execution time: 30-60 minutes
- Agents: root only plus user-requested fresh acceptance chat; no subagents
- Skills: openai-docs; python-design-patterns; python-code-style
- Output artifacts: Existing November plan pair and task group, implementation/tests, root control-plane and source registries.
- Next step: Baseline -> reproduce -> minimal fixes -> local gates -> fresh acceptance -> status sync.

#### Completion Report

- status: implemented
- what was done: ACT-F1..F6 repaired. PreToolUse/Stop were skipped because cosmetic statusMessage changes made exact definitions modified. Restored the prior trusted definitions; commands, matchers, timeouts, policy scripts and trust records unchanged. Full 9/13 and concise cases passed; terminal-marker nested apply_patch was denied and sentinel is absent.
- files touched / work locations: Active/staged hooks definitions, ledger templates/validator/regression test, evals, staged product-manager, config routing; existing control plane, plan/spec and RU/EN source docs.
- technical value delivered: Actual guard restored without policy weakening; contracts agree.
- product value delivered: Large and ordinary tasks report at the appropriate scope and terminal writes are blocked.
- actual implementation date and time: 03-11-2026 20:52
- verification evidence: Ran 1253 tests in 772.501s; OK (skipped=1); focused 165 passed; fixture 91/91; transcript 26/26; compatibility/agents/hooks passed. Final docs/matrix/state/diff receipts are recorded in final_checks.
- residual risks: Local Codex Desktop acceptance for the tested routes only. Silent Stop execution is not independently traced; no correction loop or post-final tools observed. General mutation-channel completeness, hosted/production delivery and model benchmarking are not claimed. Legacy statusMessage wording is retained for exact-definition compatibility.
- follow-up: No remaining repair gate; later hook-definition changes require trust review and fresh acceptance.


#### Приёмка исправления

ACT-F1..F6 repaired. PreToolUse/Stop were skipped because cosmetic statusMessage changes made exact definitions modified. Restored the prior trusted definitions; commands, matchers, timeouts, policy scripts and trust records unchanged. Full 9/13 and concise cases passed; terminal-marker nested apply_patch was denied and sentinel is absent.

Ran 1253 tests in 772.501s; OK (skipped=1); focused 165 passed; fixture 91/91; transcript 26/26; compatibility/agents/hooks passed. Final docs/matrix/state/diff receipts are recorded in final_checks.

Local Codex Desktop acceptance for the tested routes only. Silent Stop execution is not independently traced; no correction loop or post-final tools observed. General mutation-channel completeness, hosted/production delivery and model benchmarking are not claimed. Legacy statusMessage wording is retained for exact-definition compatibility.

Exact trust hashes, three turns, source hashes and six resolved findings: `lifecycle_parity.repair` in the existing November task-group JSON. Previous failed activation remains immutable historical evidence. An interactive CLI diagnostic was rejected by automatic review and stopped; bounded read-only initialize/hooks/list diagnostics were separately approved and succeeded. No trust-store edits or bypass flags.

| Finding | Status | Resolution |
| --- | --- | --- |
| ACT-F1 | resolved | Restore only the two prior statusMessage strings; exact definitions trusted again; actual terminal denial observed. |
| ACT-F2 | resolved | Accept plain/bold ledger labels; retain required closure_level, review/partial/docs-gap checks; template spells out assignment. |
| ACT-F3 | resolved | Scope packaged full lifecycle case and both general eval pass conditions; resolve fresh-case REPAIR-LARGE-R1. |
| ACT-F4 | resolved | Staged product-manager may edit only parent-assigned requirements/acceptance files; permissions inherited. |
| ACT-F5 | resolved | Parent enables skills; custom agents may only disable inherited skills. |
| ACT-F6 | resolved | Both eval identifiers name generic_subagent_sol_medium_default; model pins unchanged. |

Final evidence-update checks: 100 documentation tests passed after correcting one Cyrillic heading in the English plan (initial docs run: 3 locale/parity failures). check_docs.py, RU/EN task matrices and task-state consistency passed. Baseline-preservation and git diff --check passed; no unrelated edits or baseline deletions.
