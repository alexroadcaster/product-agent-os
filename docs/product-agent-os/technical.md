# Технические особенности и установка

Source status: `official + experiment`  

## Task 22 operator contract

Task 22 operator contract различает base workspace audit profile и Track 9 methodology audit complexity. Первый слой читает stack, files, control-plane state and route inputs; второй слой классифицирует methodology risk, maturity, recommendations and owner questions. `--intent-hint` может помочь routing, но не переопределяет source policy, approvals, sandbox, write guards or external-action boundaries.

Текущие machine-readable surfaces: renderer JSON includes `renderer_file_count`, stage manifest and status fields; runtime JSON includes `codex_runner_result`, `methodology_packet`, `finish_options`, compact first-response fields and schema v1 additive compatibility; audit/report tooling includes `run_methodology_audit.py`; behavioral evidence includes `run_transcript_eval.py` and fixture eval checks. Docs should describe implemented commands and fields, not planned features.
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

## Task 24 self-verification metrics loop

Task 24 adds a local, read-only `agent_skill_metrics_loop` contract for reviewing agents, skills, prompt/policy packs, router/tool policies and harness versions after real work leaves evidence. The loop collects a target registry, validates trace intake, checks dataset quality, records local grader summaries, blocks uncalibrated grader/judge calibration, builds cadence recommendation values `L0`, `L1`, `L2` and `L3`, and writes staged scorecard ledger or report packets.

Main files and commands:

- `plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics.py` - source priority, target registry, trace intake, dataset quality, grader/judge calibration, metrics, scorecards, cadence recommendation and run-record contracts.
- `plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics_report.py` - redacted offline report rendering for `agent-skill-evaluation-report.html`.
- `plugins/product-agent-os/scripts/render_agent_skill_metrics_report.py` - dry-run or stage-only report CLI.
- `.codex/artifact-templates/agent-skill-scorecard-ledger.md`, `.codex/artifact-templates/agent-skill-metrics-daily.md`, `.codex/artifact-templates/agent-skill-metrics-weekly.md` and `.codex/artifact-templates/agent-skill-update-candidate.md` - generated review artifacts.

The source-of-truth policy remains explicit: control-plane artifacts, run records, trace/eval packets and accepted gaps can support metrics; generated dashboard/report HTML, memory, raw chat logs and unsupported community claims cannot. A report is not source of truth. All metrics outputs are staged evidence only, not proof that a real project is semantically ready.

Approval boundary: Product-Agent OS performs no live eval/model/API calls, creates no active schedules, makes no external writes, applies no modernization candidates, and allows no self-applied updates. A modernization candidate needs owner review, rollback target and explicit approval state before any target workspace, skill, prompt/policy pack, router/tool policy or harness configuration changes.

## Task 25 project code graph foundation

Task 25 Batch 13 adds a local read-only graph foundation for project navigation. The scanner inventories files, emits stable file-level graph nodes and `contains` edges, validates a controlled ontology, records manifest freshness/provenance, stores observation records with relative paths/spans/fingerprints and supports temporal edge invalidation/supersession helpers. It excludes raw source bodies by default and redacts local absolute paths or secret-like values from returned packets.

Main files and commands:

- `plugins/product-agent-os/scripts/product_agent_os/project_code_graph.py` - graph JSON/JSONL packet builder.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_manifest.py` - file fingerprints, freshness and provenance.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_observations.py` - observation records and edge delta lineage.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_ontology.py` - controlled ontology and graph schema validation.
- `plugins/product-agent-os/scripts/scan_project_code_graph.py` - dry-run or stage-only scanner CLI.

```powershell
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --dry-run
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --stage C:\tmp\product-agent-os-graph-stage
```

Stage mode must use an output directory outside the target workspace. Existing graph artifacts in the target workspace are not modified. Batch 13 is file-level only: Python AST symbol scanning, query packets, runtime/status integration, graph analysis, HTML cockpit rendering and visual QA remain later Task 25 batches.

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
