---
title: "Archive - GPT-6 documentation refresh: detailed plan and evidence"
---

# Archive - GPT-6 documentation refresh: detailed plan and evidence {#gpt-6-documentation-refresh-detailed-plan-and-evidence}

> Historical source record. Dates and verdicts below describe that run; use current guides for present behavior.

Source status: `official + experiment`

Documentation-only execution of the 20 findings from the 3 November audit. Existing model pins, permissions, agents, hooks and implementation remain unchanged. Findings 1, 2 and 4 close only at documentation level; their technical dependencies remain open.

- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Root task: PAOS-DOCS-REFRESH-2026-11-03
- Machine status: `docs/superpowers/specs/gpt6-documentation-refresh-task-group.json`
- Evidence owner: root documentation maintainer; one writer, no delegated agents.
- Skills: repository implementation-planner and docs-maintainer; openai-docs.

## Stages

| Stage | Scope | Depends on | Gate |
| --- | --- | --- | --- |
| E0 | Baseline, sources, ownership and detailed plan | none | Baseline hashes, source review, valid task matrix |
| E1 | 1, 2, 5, 6, 7, 8, 9, 10 | E0 | Source agreement, TOML parsing, trust boundaries |
| E2 | 3, 4, 12 | E1 | One model matrix; no active model changes |
| E3 | 13, 14, 16 | E2 | Reproducible migration design; no live eval |
| E4 | 15, 17, 18, 19, 20 | E1-E3 | API/state/activation contracts and claim review |
| E5 | 11; semantic parity across all items | E1-E4 | RU/EN, registry, navigation and links |
| E6 | Acceptance, status and handoff | E5 | Mandatory checks, strict build, protected-file hashes |

## Verification commands

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

## Ownership, rollback and exclusions

Owned: the page pairs named below, mkdocs.yml, this plan pair/task group, source registries, REQUIREMENTS.md, PLAN.md, TEST.md, EVALS.md, RUNLOG.md and the current lifecycle marker. Sources are rechecked before changing platform claims. Forbidden: implementation, validators, test logic (only page-inventory metadata is in scope), agent profiles, executable templates, active model/permission settings, hooks, frozen evidence, prod_test.md, root site output and Git publication. Rollback only this slice using the initial diff; preserve unrelated edits. No dependency installation.

TDD, FSD and domain-model scaffolding: not_applicable to this documentation-only slice. No new persistent validator or artificial RED tests. Plan quality: exact files, per-item acceptance, dependencies, owner, checks and rollback below. No broad release, account availability or runtime activation claim.

## Technical follow-up

- OPEN-PERM: .codex/config.toml, .codex/agents/*.toml and agent-context-contract.json versus inherited parent permissions; owner: runtime maintainer; separate authorized implementation and fresh-session proof.
- OPEN-MCP: plugins/product-agent-os/scripts/product_agent_os/validators.py requires agent-local MCP; owner: runtime maintainer; align parent MCP contract and focused tests in a separate task.
- OPEN-MODEL: model allowlist, active and packaged profiles, both model-reasoning-policy templates remain GPT-5.6; owner: model migration reviewer; no switch until availability, fixed baseline and authorized eval.
- OPEN-RUNTIME: documented API capabilities are not newly activated Product-Agent OS paths; owner: architect; separate implementation acceptance.
- OPEN-BASELINE: current agent validator requires sandbox_mode while dirty config uses default_permissions; record failure separately; do not weaken checks.

### Task `DOC6-01`

- Task: DOC6-01 — Custom-agent isolation
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: E0 baseline
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/agent-configuration/subagents
- Short description: Separate behavioral read-only instructions from inherited technical permissions. Require fresh-session evidence before an isolation claim.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/product-agent/roles.md, docs/product-agent/roles.en.md, docs/codex/security.md, docs/codex/security.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Separate behavioral read-only instructions from inherited technical permissions. Require fresh-session evidence before an isolation claim.
- Acceptance criteria: Separate behavioral read-only instructions from inherited technical permissions. Require fresh-session evidence before an isolation claim. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Separate behavioral read-only instructions from inherited technical permissions. Require fresh-session evidence before an isolation claim.
- files touched / work locations: docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/product-agent/roles.md, docs/product-agent/roles.en.md, docs/codex/security.md, docs/codex/security.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-02`

- Task: DOC6-02 — Inherited MCP
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-01
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/agent-configuration/subagents
- Short description: Document parent MCP inheritance; a declaration does not prove tool availability. Keep the incompatible validator as an open technical dependency.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Document parent MCP inheritance; a declaration does not prove tool availability. Keep the incompatible validator as an open technical dependency.
- Acceptance criteria: Document parent MCP inheritance; a declaration does not prove tool availability. Keep the incompatible validator as an open technical dependency. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Document parent MCP inheritance; a declaration does not prove tool availability. Keep the incompatible validator as an open technical dependency.
- files touched / work locations: docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-03`

- Task: DOC6-03 — Current model recommendations
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-12
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/models
- Short description: Replace active obsolete recommendations with links to the model matrix; scope retirement by product and auth mode; preserve historical IDs.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E2; docs/product-agent/roles.md, docs/product-agent/roles.en.md, docs/diagrams/agent-team-and-skills.md, docs/diagrams/agent-team-and-skills.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Replace active obsolete recommendations with links to the model matrix; scope retirement by product and auth mode; preserve historical IDs.
- Acceptance criteria: Replace active obsolete recommendations with links to the model matrix; scope retirement by product and auth mode; preserve historical IDs. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Replace active obsolete recommendations with links to the model matrix; scope retirement by product and auth mode; preserve historical IDs.
- files touched / work locations: docs/product-agent/roles.md, docs/product-agent/roles.en.md, docs/diagrams/agent-team-and-skills.md, docs/diagrams/agent-team-and-skills.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-04`

- Task: DOC6-04 — Current and candidate policy
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-12, DOC6-01, DOC6-02
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/latest-model
- Short description: Distinguish active GPT-5.6 pins, GPT-6 candidates and evaluated promotion; inventory config, template and validator dependencies without editing them.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E2; docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Distinguish active GPT-5.6 pins, GPT-6 candidates and evaluated promotion; inventory config, template and validator dependencies without editing them.
- Acceptance criteria: Distinguish active GPT-5.6 pins, GPT-6 candidates and evaluated promotion; inventory config, template and validator dependencies without editing them. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Distinguish active GPT-5.6 pins, GPT-6 candidates and evaluated promotion; inventory config, template and validator dependencies without editing them.
- files touched / work locations: docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-05`

- Task: DOC6-05 — Approval policy values
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-10
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/config-file/config-reference
- Short description: Remove untrusted from current runnable examples; describe the version boundary and on-request/never semantics.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/codex/configuration.md, docs/codex/configuration.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Remove untrusted from current runnable examples; describe the version boundary and on-request/never semantics.
- Acceptance criteria: Remove untrusted from current runnable examples; describe the version boundary and on-request/never semantics. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Remove untrusted from current runnable examples; describe the version boundary and on-request/never semantics.
- files touched / work locations: docs/codex/configuration.md, docs/codex/configuration.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-06`

- Task: DOC6-06 — Granular TOML and prompt categories
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-05
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/config-file/config-reference
- Short description: Make complete TOML examples parse with tomllib; describe skill_approval as skill-script approval prompts rather than skill invocation.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/codex/configuration.md, docs/codex/configuration.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Make complete TOML examples parse with tomllib; describe skill_approval as skill-script approval prompts rather than skill invocation.
- Acceptance criteria: Make complete TOML examples parse with tomllib; describe skill_approval as skill-script approval prompts rather than skill invocation. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Make complete TOML examples parse with tomllib; describe skill_approval as skill-script approval prompts rather than skill invocation.
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
- Short description: Document beta profiles, legacy selection, protected paths and non-composition; do not change actual settings.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/codex/configuration.md, docs/codex/configuration.en.md, docs/codex/security.md, docs/codex/security.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Document beta profiles, legacy selection, protected paths and non-composition; do not change actual settings.
- Acceptance criteria: Document beta profiles, legacy selection, protected paths and non-composition; do not change actual settings. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Document beta profiles, legacy selection, protected paths and non-composition; do not change actual settings.
- files touched / work locations: docs/codex/configuration.md, docs/codex/configuration.en.md, docs/codex/security.md, docs/codex/security.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-08`

- Task: DOC6-08 — Network surfaces
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-07
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/permissions
- Short description: Map local commands, web, MCP, connectors and browser separately; domain rules require the active command network proxy.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/codex/security.md, docs/codex/security.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Map local commands, web, MCP, connectors and browser separately; domain rules require the active command network proxy.
- Acceptance criteria: Map local commands, web, MCP, connectors and browser separately; domain rules require the active command network proxy. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Map local commands, web, MCP, connectors and browser separately; domain rules require the active command network proxy.
- files touched / work locations: docs/codex/security.md, docs/codex/security.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-09`

- Task: DOC6-09 — Delegation triggers
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-01, DOC6-10
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/agent-configuration/subagents
- Short description: Correct the few-shot example and platform rule; distinguish explicit/applicable instruction triggers from stricter project policy and Work Ultra.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/prompting/question-design.md, docs/prompting/question-design.en.md, docs/diagrams/agent-team-and-skills.md, docs/diagrams/agent-team-and-skills.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Correct the few-shot example and platform rule; distinguish explicit/applicable instruction triggers from stricter project policy and Work Ultra.
- Acceptance criteria: Correct the few-shot example and platform rule; distinguish explicit/applicable instruction triggers from stricter project policy and Work Ultra. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Correct the few-shot example and platform rule; distinguish explicit/applicable instruction triggers from stricter project policy and Work Ultra.
- files touched / work locations: docs/agent-systems/subagents-skills.md, docs/agent-systems/subagents-skills.en.md, docs/prompting/question-design.md, docs/prompting/question-design.en.md, docs/diagrams/agent-team-and-skills.md, docs/diagrams/agent-team-and-skills.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-10`

- Task: DOC6-10 — Instructions and factual authority
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: E0 baseline
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/agent-configuration/agents-md
- Short description: Separate instruction priority from factual authority; document AGENTS discovery, overrides, scope and 32 KiB default limit.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E1; docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/diagrams/context-memory-verification.md, docs/diagrams/context-memory-verification.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Separate instruction priority from factual authority; document AGENTS discovery, overrides, scope and 32 KiB default limit.
- Acceptance criteria: Separate instruction priority from factual authority; document AGENTS discovery, overrides, scope and 32 KiB default limit. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Separate instruction priority from factual authority; document AGENTS discovery, overrides, scope and 32 KiB default limit.
- files touched / work locations: docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/diagrams/context-memory-verification.md, docs/diagrams/context-memory-verification.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-11`

- Task: DOC6-11 — RU/EN, links and navigation
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-01, DOC6-02, DOC6-03, DOC6-04, DOC6-05, DOC6-06, DOC6-07, DOC6-08, DOC6-09, DOC6-10, DOC6-12, DOC6-13, DOC6-14, DOC6-15, DOC6-16, DOC6-17, DOC6-18, DOC6-19, DOC6-20
- Blocks: E6 final acceptance
- Source: https://learn.chatgpt.com/docs/models
- Short description: Reconcile semantic RU/EN parity and canonical source mapping; preserve historical links; wire new pages into both navigation trees; check strict build.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E5; docs/sources/registry.md, docs/sources/registry.en.md, docs/diagrams/index.md, docs/diagrams/index.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, mkdocs.yml
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Reconcile semantic RU/EN parity and canonical source mapping; preserve historical links; wire new pages into both navigation trees; check strict build.
- Acceptance criteria: Reconcile semantic RU/EN parity and canonical source mapping; preserve historical links; wire new pages into both navigation trees; check strict build. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Reconcile semantic RU/EN parity and canonical source mapping; preserve historical links; wire new pages into both navigation trees; check strict build.
- files touched / work locations: docs/sources/registry.md, docs/sources/registry.en.md, docs/diagrams/index.md, docs/diagrams/index.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, mkdocs.yml
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-12`

- Task: DOC6-12 — Model and reasoning matrix
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-07, DOC6-09
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/latest-model
- Short description: Create one source-backed matrix for model ID, surface/auth, client conditions, effort, tools, context and unverified account availability; do not treat Ultra as API effort.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E2; docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/codex/configuration.md, docs/codex/configuration.en.md, docs/codex/surfaces.md, docs/codex/surfaces.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Create one source-backed matrix for model ID, surface/auth, client conditions, effort, tools, context and unverified account availability; do not treat Ultra as API effort.
- Acceptance criteria: Create one source-backed matrix for model ID, surface/auth, client conditions, effort, tools, context and unverified account availability; do not treat Ultra as API effort. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Create one source-backed matrix for model ID, surface/auth, client conditions, effort, tools, context and unverified account availability; do not treat Ultra as API effort.
- files touched / work locations: docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/codex/configuration.md, docs/codex/configuration.en.md, docs/codex/surfaces.md, docs/codex/surfaces.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-13`

- Task: DOC6-13 — Migration and evaluation
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-04, DOC6-12
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/latest-model
- Short description: Define frozen baseline, one-variable comparisons, predefined thresholds, task corpus, stop/rollback and evidence ceiling; no model runs.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E3; docs/playbooks/model-migration.md, docs/playbooks/model-migration.en.md, docs/agent-systems/evals-observability.md, docs/agent-systems/evals-observability.en.md, EVALS.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Define frozen baseline, one-variable comparisons, predefined thresholds, task corpus, stop/rollback and evidence ceiling; no model runs.
- Acceptance criteria: Define frozen baseline, one-variable comparisons, predefined thresholds, task corpus, stop/rollback and evidence ceiling; no model runs. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Define frozen baseline, one-variable comparisons, predefined thresholds, task corpus, stop/rollback and evidence ceiling; no model runs.
- files touched / work locations: docs/playbooks/model-migration.md, docs/playbooks/model-migration.en.md, docs/agent-systems/evals-observability.md, docs/agent-systems/evals-observability.en.md, EVALS.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-14`

- Task: DOC6-14 — GPT-6 prompting
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-09, DOC6-10, DOC6-13
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/latest-model
- Short description: Document bounded initiative, concrete preparation before approval, conflicting instructions and proportionate verification without changing active prompts.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E3; docs/prompting/overview.md, docs/prompting/overview.en.md, docs/prompting/question-design.md, docs/prompting/question-design.en.md, docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Document bounded initiative, concrete preparation before approval, conflicting instructions and proportionate verification without changing active prompts.
- Acceptance criteria: Document bounded initiative, concrete preparation before approval, conflicting instructions and proportionate verification without changing active prompts. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Document bounded initiative, concrete preparation before approval, conflicting instructions and proportionate verification without changing active prompts.
- files touched / work locations: docs/prompting/overview.md, docs/prompting/overview.en.md, docs/prompting/question-design.md, docs/prompting/question-design.en.md, docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-15`

- Task: DOC6-15 — API compatibility
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-12, DOC6-19
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/latest-model
- Short description: Map model/endpoint/tool/reasoning/sampling compatibility; separate Responses and Chat Completions parameter names; do not replace CLI runner.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E4; docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Map model/endpoint/tool/reasoning/sampling compatibility; separate Responses and Chat Completions parameter names; do not replace CLI runner.
- Acceptance criteria: Map model/endpoint/tool/reasoning/sampling compatibility; separate Responses and Chat Completions parameter names; do not replace CLI runner. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Map model/endpoint/tool/reasoning/sampling compatibility; separate Responses and Chat Completions parameter names; do not replace CLI runner.
- files touched / work locations: docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md, docs/runtime/non-interactive-and-mcp.md, docs/runtime/non-interactive-and-mcp.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-16`

- Task: DOC6-16 — Cost, caching and context
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-12, DOC6-13
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/prompt-caching
- Short description: Describe cache reads/writes, retention, tiers, context pricing conditions and cost per completed task; separate API billing from subscriptions and cache from memory.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E3; docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/agent-systems/evals-observability.md, docs/agent-systems/evals-observability.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/playbooks/model-migration.md, docs/playbooks/model-migration.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Describe cache reads/writes, retention, tiers, context pricing conditions and cost per completed task; separate API billing from subscriptions and cache from memory.
- Acceptance criteria: Describe cache reads/writes, retention, tiers, context pricing conditions and cost per completed task; separate API billing from subscriptions and cache from memory. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Describe cache reads/writes, retention, tiers, context pricing conditions and cost per completed task; separate API billing from subscriptions and cache from memory.
- files touched / work locations: docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/agent-systems/evals-observability.md, docs/agent-systems/evals-observability.en.md, docs/codex/models-and-reasoning.md, docs/codex/models-and-reasoning.en.md, docs/playbooks/model-migration.md, docs/playbooks/model-migration.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-17`

- Task: DOC6-17 — Async tools and steering
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-15, DOC6-19
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/async-tool-calling
- Short description: Describe pending calls, call_id, deadlines, duplicate/late results and accepted versus applied steering; no cancellation or hosted execution claims.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E4; docs/agent-systems/session-control.md, docs/agent-systems/session-control.en.md, docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Describe pending calls, call_id, deadlines, duplicate/late results and accepted versus applied steering; no cancellation or hosted execution claims.
- Acceptance criteria: Describe pending calls, call_id, deadlines, duplicate/late results and accepted versus applied steering; no cancellation or hosted execution claims. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Describe pending calls, call_id, deadlines, duplicate/late results and accepted versus applied steering; no cancellation or hosted execution claims.
- files touched / work locations: docs/agent-systems/session-control.md, docs/agent-systems/session-control.en.md, docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-18`

- Task: DOC6-18 — Reasoning updates and compaction
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-16, DOC6-17
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/reasoning
- Short description: Distinguish steering, reset, summary, compaction and memory; document configuration_update compatibility and explicit compaction restoration.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E4; docs/agent-systems/session-control.md, docs/agent-systems/session-control.en.md, docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/diagrams/context-memory-verification.md, docs/diagrams/context-memory-verification.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Distinguish steering, reset, summary, compaction and memory; document configuration_update compatibility and explicit compaction restoration.
- Acceptance criteria: Distinguish steering, reset, summary, compaction and memory; document configuration_update compatibility and explicit compaction restoration. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Distinguish steering, reset, summary, compaction and memory; document configuration_update compatibility and explicit compaction restoration.
- files touched / work locations: docs/agent-systems/session-control.md, docs/agent-systems/session-control.en.md, docs/prompting/context-engineering.md, docs/prompting/context-engineering.en.md, docs/diagrams/context-memory-verification.md, docs/diagrams/context-memory-verification.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-19`

- Task: DOC6-19 — Agent runtime map
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-01, DOC6-02, DOC6-12, DOC6-13
- Blocks: E5/E6 documentation acceptance
- Source: https://developers.openai.com/api/docs/guides/agents
- Short description: Compare Agents API, SDK, Responses API/Multi-agent and Codex subagents by state/tool/execution ownership; label beta and project implementation gaps.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E4; docs/runtime/overview.md, docs/runtime/overview.en.md, docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md, docs/diagrams/runtime-decision-map.md, docs/diagrams/runtime-decision-map.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Compare Agents API, SDK, Responses API/Multi-agent and Codex subagents by state/tool/execution ownership; label beta and project implementation gaps.
- Acceptance criteria: Compare Agents API, SDK, Responses API/Multi-agent and Codex subagents by state/tool/execution ownership; label beta and project implementation gaps. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Compare Agents API, SDK, Responses API/Multi-agent and Codex subagents by state/tool/execution ownership; label beta and project implementation gaps.
- files touched / work locations: docs/runtime/overview.md, docs/runtime/overview.en.md, docs/agent-systems/sdk-patterns.md, docs/agent-systems/sdk-patterns.en.md, docs/diagrams/runtime-decision-map.md, docs/diagrams/runtime-decision-map.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

### Task `DOC6-20`

- Task: DOC6-20 — Hook trust and activation
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-approved documentation refresh following 20-item audit
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 16:58
- Depends on: DOC6-01, DOC6-07
- Blocks: E5/E6 documentation acceptance
- Source: https://learn.chatgpt.com/docs/hooks
- Short description: Describe hash trust, supported events/handlers, timeouts and coverage; distinguish static/script/fresh-session proof and PreToolUse/PostToolUse/Stop effects.
- Technical value: Source-aligned contracts and reproducible examples; implementation remains unchanged
- Product value: Operators can select a supported route without false activation or permission claims
- Scope: E4; docs/runtime/worktrees-hooks-rules.md, docs/runtime/worktrees-hooks-rules.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md, TEST.md
- Non-goals: No config/model/runtime/template/test logic changes, live calls, browser, Git or publication
- Expected result: Describe hash trust, supported events/handlers, timeouts and coverage; distinguish static/script/fresh-session proof and PreToolUse/PostToolUse/Stop effects.
- Acceptance criteria: Describe hash trust, supported events/handlers, timeouts and coverage; distinguish static/script/fresh-session proof and PreToolUse/PostToolUse/Stop effects. RU/EN agree; official source and applicability are visible; protected files unchanged.
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
- what was done: Describe hash trust, supported events/handlers, timeouts and coverage; distinguish static/script/fresh-session proof and PreToolUse/PostToolUse/Stop effects.
- files touched / work locations: docs/runtime/worktrees-hooks-rules.md, docs/runtime/worktrees-hooks-rules.en.md, docs/product-agent-os/codex-compatibility.md, docs/product-agent-os/codex-compatibility.en.md, TEST.md
- technical value delivered: Documentation contracts reconciled; no implementation promotion
- product value delivered: Source-backed operator guidance
- actual implementation date and time: 03-11-2026 16:58
- verification evidence: Current run: docs 100/100; lifecycle plan 5/5; hooks 25/25 (isolated external TEMP); infrastructure templates 94/94; both hook validators, docs checker, RU/EN task matrices, state consistency and diff check exit 0; strict preview MkDocs exit 0; source review 20 official pages. See Verification receipt below. No runtime/model promotion.
- residual risks: OPEN-PERM, OPEN-MCP, OPEN-MODEL and OPEN-RUNTIME remain open; availability/runtime not tested
- follow-up: Separate technical implementation/eval decision; preserve historical evidence

## Completion assurance

Doubt packet: not_required as a separate artifact; explicit root self-review uses the 20-item acceptance matrix, current command receipts and protected-file comparison. Supported claim: documentation corrections only. Unsupported: model promotion, live isolation/MCP/hook activation, release readiness. No provider/model/browser/server/Git/external writes performed.

## Verification receipt — 2026-11-03

All 20 documentation findings are implemented. E0-E6 documentation work is complete; technical dependencies remain open. The command results below are current-run evidence, not historical reuse. A final affected-doc/status validation follows status recording; unchanged hook/template results remain reusable because their source inputs did not change.

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


Static acceptance: 20 official source pages fetched; 48 changed/new Markdown files read as UTF-8; 10 complete TOML/JSON blocks parsed; paired official source URLs agree. Review covered all 20 acceptance rows, source/runtime boundaries, parameter combinations, delegation examples and no-promotion wording. This is explicit root self-review, not an independent reviewer run. Mermaid source and strict generation were checked; browser rendering was not run.

Initial attempt after plan creation: 224 tests, 15 failures/33 errors. Problems included inherited TEMP permissions, page counters, Cyrillic headings in the EN plan and a legacy validator hardcoding the August plan. Corrections preserved assertions and implementation. Pass1 found 10 editorial test failures, four hook-fixture errors and two strict-link warnings. Documentation text/links were corrected; hook tests passed with isolated OS TEMP outside the repository. Using a nested repository TEMP caused Git-root discovery to read the real project marker; no hook behavior was changed to make tests pass.

Inventory-only test diff: 160 buildable / 150 localized source pages; historical site-promoted count stays 143. Three new page pairs are explicitly pending root-site promotion. The only change to the August plan pair is a dated forward pointer for current lifecycle discovery. These bounded maintenance adjustments do not change test logic or historical results.

Protected SHA-256 comparison: all 17 pre-existing dirty config/profile/eval files unchanged; 1,658 protected implementation/test/hook/template/root-site files unchanged, excluding the authorized lifecycle marker and documented inventory metadata file. No active model switch, permissions/config/profile/hook change, live model/provider call, browser automation, live server, project Git history/publication or deployment occurred. Tests may create disposable fixture repositories.

Known diagnostic outside scope: `python plugins/product-agent-os/scripts/validate_agents.py .codex/agents` exits 1 with `project config must set sandbox_mode = workspace-write`. This pre-existing implementation mismatch remains OPEN-BASELINE; it is not waived as a passing check. OPEN-PERM, OPEN-MCP and OPEN-MODEL remain unresolved. Documentation completion does not imply broad compatibility, isolation, activation, promotion or release acceptance.

Control-plane sync: REQUIREMENTS, PLAN, TEST, EVALS and RUNLOG updated; prod_test.md not_applicable; no overflow refactor required. Next route: separately authorized technical contract repair and then project evaluation; Batch 45 T30 queue remains intact. Rollback only this slice, preserving unrelated changes and historical evidence.


## Authorized technical follow-up — 2026-11-03

The preceding documentation receipt remains historical. This separately authorized task changes implementation and configuration.

### Task `PAOS-CONTRACT-MODEL-ALIGNMENT-2026-11-03`

- Task: PAOS-CONTRACT-MODEL-ALIGNMENT-2026-11-03 — Align permissions, MCP, validators and model profiles
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner authorizes technical follow-up and model switches on 2026-11-03
- Validator target: detailed task blocks
- Date and time of task implementation: 03-11-2026 18:44
- Depends on: DOC6-01, DOC6-02, DOC6-04
- Blocks: fresh-session activation and behavioral promotion
- Source: https://learn.chatgpt.com/docs/agent-configuration/subagents; https://learn.chatgpt.com/docs/permissions; https://learn.chatgpt.com/docs/models
- Short description: Repair parent-only permissions/MCP and modernize active/staged model contracts.
- Technical value: Validators reject unsupported custom-agent overrides and validate inherited parent contracts.
- Product value: Operators receive consistent active profiles and safe staged proposals.
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
- what was done: Parent permissions and MCP inheritance aligned; 23 active/staged profiles pinned to GPT-6.1 Sol/Terra with preserved effort; inherited skills moved to parent; validators and renderer reject unsupported contracts; lifecycle validator follows the explicit current plan.
- files touched / work locations: AGENTS.md; .codex/config.toml, agents, eval contract, lifecycle workflow and two artifact templates; plugin config/agent/eval/workflow/artifact templates; validators.py, infrastructure.py, validate_task_state_consistency.py; five test modules; model/configuration/compatibility/source pages; five control-plane files
- technical value delivered: Supported parent-only controls and model policy enforced locally across active and rendered configurations.
- product value delivered: Consistent reusable profiles and explicit separation of role behavior from sandbox isolation.
- actual implementation date and time: 03-11-2026 18:44
- verification evidence: Ran 1247 tests in 611.387s; OK (skipped=1); fixture/transcript eval, compatibility, 15 active agents, both hook validators, RU/EN task matrices, state consistency, docs checker and diff check exit 0.
- residual risks: Fresh-session effective permissions/MCP/model availability and quality/cost/latency comparison remain unverified. No provider calls, browser, hook activation, target mutation, Git publication or root site update.
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


#### Lifecycle design and evidence boundaries

| Contract | Previous PAOS behavior | Trade reference and implemented PAOS behavior |
| --- | --- | --- |
| Start packet | 13 field-list labels for non-mechanical work | 9 bold labels with content on the next line; conditional scope |
| Closing packet | 7 fields and a literal Completion Brief heading | 13 separate ledger items; Product-Agent OS namespace |
| Ordinary work | Full packet and marker | Concise Scope/Evidence/Limits note and scoped marker for authorized mutations |
| Stop | Chat-format rejection and one corrective continuation | Advisory only; explicit packet validator remains separate |
| Durable planning | Generated copies of chat packets | Task detail and Completion Report only; no fabricated delivery, metrics or review |
| Legacy sessions | v1 marker | v1 remains compatible; new tasks use scoped v2 or concise v1 |
| Safety | Command/path/secret rules, approval and sandbox boundaries | Preserved; terminal completion_ready now also denies mutations |

Trade was inspected read-only. Its current ledger has 13 fields; the older eleven-field eval wording was not copied. No Trade hook files were found at the inspected `.codex/hooks.json` / `.codex/hooks` paths; parity concerns reporting behavior, not an assumed Trade hook implementation. Official Hooks documentation was fetched through OpenAI Developers on 2026-11-03: https://learn.chatgpt.com/docs/hooks. Stop continuation and hash trust are host capabilities; this project chooses advisory reporting. No trust, permissions, model selection, provider or Git publication was changed in this slice.

Regression evidence: initial full/concise and Stop tests failed on the old behavior; packet validation and generator regressions failed before their implementations; the concise bootstrap regression failed before its fix. The first attempted bootstrap test used a wrong class name and was setup error, not RED evidence; the correctly addressed test then failed for the intended missing-marker denial. Subsequent focused checks passed. Full-suite and final status receipts are recorded in `lifecycle_parity` of the owning task group.

Self-review: existing lifecycle generator, templates and validator infrastructure reused; no dependency added. Pure packet validation is separate from hook I/O. Active/staged parity, six Trade hashes, 23 profile settings, parent non-lifecycle configuration, hook command wiring and safety regex constants are compared with the task-start baseline. Newline-only changes were restored from that baseline. Renderer inventory increases from 207 to 209 solely for the two packet templates. Canonical graph, root site, fixture sources, prior task receipts and production ledger remain outside this slice.

Control-plane sync: REQUIREMENTS scope/acceptance, PLAN sequence and gate, TEST commands/evidence ceiling, EVALS reporting rubric, RUNLOG current handoff updated. `prod_test.md`: not_applicable (no Batch 39 evidence changed). Detailed evidence stays in this plan and its existing task-group JSON. No separate packet transcript is persisted.

Rollback: restore only this slice's changed files from the task-start baseline, preserving earlier dirty work; remove only the two newly introduced active/staged packet templates if rolling back their registrations and routing together. Do not use destructive Git reset or alter trust. Recheck active/staged parity and focused lifecycle contracts after rollback. Fresh-session acceptance remains separate: inspect applicable hook hash trust, then observe one full-scope task and one ordinary task with their actual markers and terminal output. Static fixtures do not prove model compliance, independent review, host activation, latency or production readiness.


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

#### Fresh-session activation acceptance

Fresh desktop chat 01a1a250-2429-73b1-91de-3ab6b06c660b: large 9-label start and 13-item ledger observed; strict ledger parser fails presentation/closure syntax; ordinary concise route passed. SessionStart and PostToolUse context observed. Terminal-marker apply_patch negative probe FAILED (sentinel created); direct hook script returns deny. Each scenario has one final, no corrective Stop prompt and no post-final tools. Implementation/trust/model settings unchanged.

| Case | Result | Boundary |
| --- | --- | --- |
| Large | 9 start labels; 13 ledger items; one final | Strict validator mismatch: bold labels and no literal closure_level assignment |
| Ordinary | Concise start/result; task_scope_note_v1; exact artifact content | One observed low-risk case |
| Hook loading | SessionStart and 3 PostToolUse contexts observed | Exact trusted hashes not exposed |
| PreToolUse negative probe | FAILED: terminal marker did not stop nested apply_patch | Direct script returns deny; host root cause unknown |
| Stop outcome | No correction loop or tools after final | Silent event execution not proven |

Overall activation_failed; prior local implementation evidence remains historical and is not revoked or relabeled. Source-owned findings ACT-F1..F6 and precise thread/turn receipts are in lifecycle_parity.activation_check. Full-suite rerun is not applicable: implementation was unchanged. Required document/status checks are recorded there after execution. Rollback only this verification receipt and synthetic files if needed; never alter trust or delete unrelated user files.


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


#### Repair acceptance

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
