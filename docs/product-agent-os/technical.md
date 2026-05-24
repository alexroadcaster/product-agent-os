# Технические особенности и установка

Source status: `official + experiment`  
Additional sources: [Codex MCP](https://developers.openai.com/codex/mcp), [Context7 MCP clients](https://context7.com/docs/resources/all-clients).  
Источники: [Codex plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://developers.openai.com/codex/skills), [Subagents](https://developers.openai.com/codex/subagents), [Codex hooks](https://developers.openai.com/codex/hooks), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex automations](https://developers.openai.com/codex/app/automations), [Product-Agent OS plugin](index.md).

## Package layout

Реализация находится в `plugins/product-agent-os/`.

```text
plugins/product-agent-os/
  .codex-plugin/plugin.json
  skills/
  scripts/
  assets/
    templates/
    fixtures/
```

Официальный contract Codex plugin требует `.codex-plugin/plugin.json`; остальные bundled components лежат в plugin root. В текущем package manifest указывает на bundled `skills` и `.mcp.json`, а пользовательская логика lives in local scripts and templates.

## Bundled MCP

`.mcp.json` registers Context7 as a bundled MCP server:

```json
{
  "context7": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp"],
    "startup_timeout_sec": 20
  }
}
```

This keeps the plugin package free of API keys and follows the Codex MCP Context7 example. Projects that need higher Context7 limits or private sources should provide credentials through their own trusted Codex MCP configuration, not through this repository.

## Packaged skills

| Skill | Назначение |
| --- | --- |
| `project-lifecycle-orchestrator` | Определяет lifecycle state и следующий bounded step |
| `workspace-discovery-auditor` | Делает read-only audit workspace |
| `requirements-author` | Готовит requirements packet |
| `implementation-planner` | Готовит executable plan |
| `agent-team-designer` | Проектирует project-scoped roles and handoffs |
| `test-eval-designer` | Определяет deterministic checks and quality gates |
| `risk-reviewer` | Проверяет diff, risks, source fidelity and missing tests |
| `pr-release-operator` | Готовит PR or release packet |
| `learning-loop-maintainer` | Переносит устойчивые lessons в durable artifacts |
| `automation-promoter` | Делает candidate-only automation readiness analysis |

Каждый skill задает trigger, inputs, outputs, failure modes and final response contract. Source-sensitive skills не должны превращать community claims в project rules без verification status.

## Generated infrastructure

Renderer может создать или предложить:

- `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- `.codex/config.toml`;
- `.codex/agents/*.toml`;
- `.codex/hooks/*`;
- `.codex/workflows/*.md`;
- `.codex/artifact-templates/*.md`;
- `.codex/evals/*.json`;
- `.codex/pr/*`;
- `.codex/automation-candidates/automation-candidate.md`.

В Track 6 workflow inventory расширен двумя методическими packets:

- `.codex/workflows/development-standards.md` - product hypothesis, architecture boundary, test-first/eval-first path, bounded agentic implementation, review and measurement.
- `.codex/workflows/documentation-system.md` - docs-as-code routing for architecture docs, API contracts, UI component docs, database docs, code reference and release docs.

Track 7 добавляет concrete artifact templates, чтобы методологии не оставались только checklist:

- `.codex/artifact-templates/adr.md`;
- `.codex/artifact-templates/architecture-overview.md`;
- `.codex/artifact-templates/domain-modeling.md`;
- `.codex/artifact-templates/metric-spec.md`;
- `.codex/artifact-templates/api-contract-review.md`;
- `.codex/artifact-templates/component-card.md`;
- `.codex/artifact-templates/database-dictionary.md`;
- `.codex/artifact-templates/docs-tooling-decision.md`.

Track 8 добавляет scenario routing and workflow coverage:

| Status | Generated or routed surface |
| --- | --- |
| `done` | `.codex/workflows/first-run-intake.md`, `.codex/workflows/bug-rescue.md`, `.codex/workflows/greenfield-idea-to-plan.md`, `.codex/workflows/complex-system-acceleration.md`, `.codex/workflows/pr-review-readiness.md`, `.codex/workflows/legacy-onboarding.md`, `.codex/workflows/api-migration.md`, `.codex/workflows/ai-eval-regression.md`, `.codex/workflows/native-mobile-feature.md`, `.codex/workflows/desktop-local-first.md`, `.codex/workflows/data-migration.md`, `.codex/workflows/security-sensitive-change.md`, `.codex/workflows/ci-stabilization.md`, `.codex/workflows/release-packaging.md`. |
| `done` | `.codex/artifact-templates/bug-rescue-report.md`, `greenfield-idea-brief.md`, `integration-catalog.md`, `pr-risk-review.md`, `onboarding-map.md`, `migration-plan.md`, `ai-eval-spec.md`, `security-risk-review.md`, `ci-stabilization-report.md`, `release-readiness.md`. |
| `done methodology gate` | `acceptance-scenarios.md`, `domain-modeling.md`, `architecture-overview.md`, `component-card.md`, `metric-spec.md`, `release-packet.md`, `docs-tooling-decision.md`, `plan-quality-check.md`, `agent-task-packet.md`, `project-readiness.json` and `behavioral-workflows.json` cover ATDD/BDD traceability, conditional DDD domain modeling, bounded-context-to-architecture traceability, ubiquitous language traceability, optional `fsd_structure`, metric hardening, evidence-before-completion, docs tooling selection, conditional readiness statuses, no-placeholder planning, two-stage review and fresh-context handoff. |

First-run intake is visible in the runtime route packet, lifecycle skills and behavioral evals for empty, broken, existing control-plane and complex system starts. Release packaging is visible in `usage_mode`, fixture evals, renderer output, lifecycle skills, and the packaged `release-packaging.md` / `release-readiness.md` templates. Dedicated operator docs now live in [scenarios](scenarios.md), [behavioral evals](behavioral-evals.md) and [Codex compatibility](codex-compatibility.md).

Generation is staged-first. Existing user-authored files are preserved outside managed sections:

```markdown
<!-- product-agent-os:start section-id -->
...
<!-- product-agent-os:end section-id -->
```

Если existing file не имеет managed markers, plugin stages a companion proposal instead of overwriting it.

## Local commands

Read-only infrastructure plan:

```powershell
python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --dry-run
```

Stage generated artifacts outside the target workspace:

```powershell
python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --stage <stage-dir>
```

Plan merge from staged artifacts:

```powershell
python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --plan
```

Apply requires an approval record:

```powershell
python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --apply --approval-file <approval.json>
```

Run Codex-only runtime contract mode:

```powershell
python plugins\product-agent-os\scripts\run_codex_runtime_runner.py <workspace> --contract
```

Allow route recommendation to a Codex subagent when the current Codex thread explicitly permits it:

```powershell
python plugins\product-agent-os\scripts\run_codex_runtime_runner.py <workspace> --contract --allow-subagents
```

Run plugin fixture evals:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

## Codex installation boundary

Для Codex installation plugin должен быть доступен через plugin marketplace or curated plugin list, а package root должен содержать `.codex-plugin/plugin.json`. В этом репозитории package уже подготовлен локально under `plugins/product-agent-os/`; подключение к конкретной Codex App installation остается отдельным environment step and should follow current official Codex plugin docs.

Этот project intentionally keeps runtime code Codex-only:

- no separate OpenAI API key;
- no standalone Agents SDK application;
- no background MCP server started by plugin scripts; Context7 is declared as a bundled Codex MCP server and starts only when Codex enables that MCP configuration;
- no active automation created from templates;
- no plugin-root hook activation without explicit approval.

## Guardrails

| Guardrail | Enforcement |
| --- | --- |
| Source policy | `validate_source_policy.py` blocks unsupported OpenAI/Codex claims and secret-like content |
| Automation policy | `validate_automation_candidate.py` requires manual success evidence, owner, cadence, verification, rollback and approval |
| Staged manifest | stage paths must stay inside stage root and target paths inside workspace |
| Approval record | approved writes require explicit decisions and matching plan digest |
| Rollback | apply can produce rollback manifest for later rollback |
| Runtime runner | validates lifecycle route, approval boundary, source policy, handoff shape and redaction |
| Transcript/session eval runner | `run_transcript_eval.py` replays synthetic or redacted sessions against `behavioral-workflows.json` without external model calls |
| Redaction | secret assignments, local absolute paths and private data markers are redacted from runner result |
| Engineering standards | templates require product metrics, architecture boundary, test/eval gates, docs impact and measurement notes |
| Methodology discovery | workspace audit reports architecture docs, ADR, domain model, architecture context maps, optional `fsd_structure`, OpenAPI, AsyncAPI, Storybook, DB docs, CODEOWNERS, CI, evals and metrics signals |
| Scenario routing | `usage_mode` distinguishes completed workflows, partial methodology gates, and base modes; it returns minimum artifacts plus evidence gaps |

## Verification commands for this repo

After docs or nav changes:

```powershell
python tools\check_docs.py
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; python -m mkdocs build --strict
```

After plugin scripts, templates, fixtures or tests change:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
```
