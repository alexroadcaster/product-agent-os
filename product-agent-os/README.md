# Product-Agent OS

Product-Agent OS is a local Codex plugin for turning a real project workspace into a governed product delivery loop. It packages lifecycle skills, project infrastructure templates, safe merge tooling, fixture evals, and a Codex-only runtime contract runner.

The plugin is designed for Codex App, CLI, and IDE extension workflows. It does not require a separate OpenAI API key and does not run as a standalone Agents SDK app.

Official references:

- [Codex plugins](https://developers.openai.com/codex/plugins)
- [Build plugins](https://developers.openai.com/codex/plugins/build)
- [Agent Skills](https://developers.openai.com/codex/skills)
- [Subagents](https://developers.openai.com/codex/subagents)
- [Codex MCP](https://developers.openai.com/codex/mcp)
- [Codex hooks](https://developers.openai.com/codex/hooks)
- [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [Context7 MCP clients](https://context7.com/docs/resources/all-clients)

## What Problem It Solves

Codex can implement large tasks, but real product work fails when the operating context lives only in chat. Product-Agent OS moves durable state into explicit artifacts:

| Problem | Product-Agent OS behavior |
| --- | --- |
| Requirements are implicit or lost between sessions | Create or update `REQUIREMENTS.md` with scope, non-goals, constraints, and acceptance criteria |
| Implementation starts before planning | Route to `PLAN.md` before build work |
| Subagents edit overlapping files | Create role and ownership boundaries before parallel work |
| Tests are guessed after the fact | Define deterministic checks in `TEST.md` and subjective gates in `EVALS.md` |
| Reviews lack evidence | Require commands, reports, risks, and handoff data in `RUNLOG.md` |
| Hooks and automations are activated too early | Keep hooks staged and automations candidate-only until explicitly approved |
| Existing project files might be overwritten | Stage proposals first and preserve user-authored content outside managed sections |

## Current Capabilities

### Lifecycle Skills

The plugin bundles these skills under `skills/`:

| Skill | Role |
| --- | --- |
| `project-lifecycle-orchestrator` | Determine lifecycle state and next action |
| `workspace-discovery-auditor` | Inspect a workspace without writing |
| `requirements-author` | Draft or refine requirements |
| `implementation-planner` | Produce an executable implementation plan |
| `agent-team-designer` | Define project-scoped agent roles and handoff boundaries |
| `test-eval-designer` | Define tests, evals, and quality gates |
| `risk-reviewer` | Review risk, unsupported claims, and missing verification |
| `pr-release-operator` | Prepare PR or release packets |
| `learning-loop-maintainer` | Capture lessons, failures, and durable rules |
| `automation-promoter` | Produce candidate-only automation readiness packets |

Codex loads skills through progressive disclosure: it sees each skill's name and description first, then loads the full `SKILL.md` only when the task matches or the user invokes it.

### Staged Infrastructure Renderer

The renderer can propose a project control plane:

```text
AGENTS.md
REQUIREMENTS.md
PLAN.md
TEST.md
EVALS.md
RUNLOG.md
.codex/config.toml
.codex/agents/*.toml
.codex/hooks/*
.codex/workflows/*.md
.codex/evals/*.json
.codex/pr/*
.codex/automation-candidates/automation-candidate.md
```

It is staged-first by design:

1. Inspect target workspace.
2. Render proposed artifacts to a separate stage directory.
3. Write `product-agent-os-stage-manifest.json`.
4. Build a read-only merge plan.
5. Require an explicit approval record before target workspace writes.
6. Write a rollback manifest after approved apply.

Existing files are preserved unless they contain Product-Agent OS managed sections:

```markdown
<!-- product-agent-os:start section-id -->
...
<!-- product-agent-os:end section-id -->
```

### Safe Merge and Rollback

`merge_infrastructure.py` protects the target workspace by validating:

- stage manifest shape and digests;
- workspace binding;
- stale workspace state;
- path traversal;
- symlink escapes;
- parent/child target conflicts;
- approved targets and actions;
- hook activation metadata when hooks are explicitly enabled.

An approved apply writes `product-agent-os-rollback-manifest.json` into the stage directory. Rollback refuses to proceed if target files changed after apply.

### Codex Runtime Runner

Track 5 adds a Codex-only runner:

```powershell
python scripts\run_codex_runtime_runner.py <workspace> --contract
```

The runner does not call a model. It reads workspace artifacts, infers lifecycle state, plans the next route, validates source and approval boundaries, redacts sensitive output, and returns a deterministic result contract.

Possible statuses:

| Status | Meaning |
| --- | --- |
| `route_ready` | A next skill/subagent route is available |
| `needs_context` | Required control-plane context is missing |
| `needs_approval` | Route requires explicit approval before writes |
| `blocked` | Source, automation, approval, or handoff guard failed |
| `completed` | Reserved for future verified completion packets |
| `failed` | Reserved for runtime failures |

### Source, Automation, and Redaction Guards

The plugin includes local validators for:

- OpenAI/Codex/source-backed claims;
- community claim metadata;
- secret-like literal detection;
- automation candidate readiness;
- active automation boundary;
- handoff completeness;
- local path and private data redaction in runner output.

### Bundled Context7 MCP

The plugin manifest points to `.mcp.json`, which registers a `context7` MCP server with:

```json
{
  "context7": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp"],
    "startup_timeout_sec": 20
  }
}
```

This follows the Codex MCP example for Context7 and keeps secrets out of the plugin package. A project or user can still configure an API key separately in their Codex MCP configuration when higher Context7 limits or private sources are required.

## Repository Layout

```text
product-agent-os/
  .codex-plugin/
    plugin.json
  .mcp.json
  README.md
  assets/
    fixtures/
    templates/
  hooks/
  scripts/
    product_agent_os/
    codex_runtime_runner/
    render_infrastructure.py
    merge_infrastructure.py
    run_codex_runtime_runner.py
    run_fixture_eval.py
    validate_*.py
  skills/
    project-lifecycle-orchestrator/
    workspace-discovery-auditor/
    requirements-author/
    implementation-planner/
    agent-team-designer/
    test-eval-designer/
    risk-reviewer/
    pr-release-operator/
    learning-loop-maintainer/
    automation-promoter/
```

`plugin.json` is the required Codex plugin manifest. The current manifest points to bundled skills and `.mcp.json`; `.mcp.json` registers Context7 for up-to-date developer documentation. Hook scripts are present as templates and examples, but plugin-bundled hooks are opt-in in Codex and this plugin does not silently activate them.

## Install in Codex

Codex installs plugins through marketplaces. For local development, use either a repo marketplace or a personal marketplace.

### Option A: Repo-Scoped Marketplace

Use this when the plugin should be discoverable from a specific repository.

1. Put the plugin under the repository's `plugins/` directory:

```text
<repo>/
  .agents/
    plugins/
      marketplace.json
  plugins/
    product-agent-os/
      .codex-plugin/
        plugin.json
```

2. Add or update `<repo>/.agents/plugins/marketplace.json`:

```json
{
  "name": "local-product-agent-plugins",
  "interface": {
    "displayName": "Local Product-Agent Plugins"
  },
  "plugins": [
    {
      "name": "product-agent-os",
      "source": {
        "source": "local",
        "path": "./plugins/product-agent-os"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

3. Restart Codex.
4. Open the plugin directory.
5. Select `Local Product-Agent Plugins`.
6. Install or enable `Product-Agent OS`.

Codex resolves `source.path` relative to the marketplace root, not relative to `.agents/plugins/`.

### Option B: Personal Marketplace

Use this when you want the plugin available across projects on your machine.

1. Copy the plugin to a personal plugin directory, for example:

```powershell
New-Item -ItemType Directory -Force -Path $HOME\.codex\plugins | Out-Null
Copy-Item -Recurse -Force plugins\product-agent-os $HOME\.codex\plugins\product-agent-os
```

2. Add or update `$HOME\.agents\plugins\marketplace.json`:

```json
{
  "name": "personal-product-agent-plugins",
  "interface": {
    "displayName": "Personal Product-Agent Plugins"
  },
  "plugins": [
    {
      "name": "product-agent-os",
      "source": {
        "source": "local",
        "path": "./.codex/plugins/product-agent-os"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

3. Restart Codex and enable the plugin from the plugin directory.

### Option C: Add a Marketplace From CLI

When you maintain a local marketplace root, Codex can track it:

```powershell
codex plugin marketplace add <local-marketplace-root>
```

Then restart Codex and install the plugin from that marketplace.

## Apply to a Project

There are two supported ways to apply the plugin to a project.

### Guided Codex Flow

After installing the plugin, open the target project in Codex and start with one of the manifest prompts:

```text
Use Product-Agent OS to audit this workspace and propose a safe infrastructure plan.
```

or:

```text
Use Product-Agent OS to guide this feature from requirements to PR packet.
```

Expected first behavior:

1. Codex uses `workspace-discovery-auditor` or the local discovery helper.
2. It reports detected stack, existing control-plane files, missing artifacts, risks, and blockers.
3. It proposes staged infrastructure instead of writing directly.
4. It asks for approval before target workspace writes.

### Scripted Local Flow

Use scripts when you want deterministic local artifacts and machine-checkable output.

From this plugin directory:

```powershell
cd plugins\product-agent-os
```

Inspect a target workspace without writing:

```powershell
python scripts\render_infrastructure.py <workspace> --dry-run
```

Stage proposed infrastructure outside the target workspace:

```powershell
python scripts\render_infrastructure.py <workspace> --stage <stage-dir>
```

Build a read-only merge plan:

```powershell
python scripts\merge_infrastructure.py <workspace> <stage-dir> --plan
```

The merge plan writes `product-agent-os-approval-template.json` into the stage directory. Fill it in as `product-agent-os-approval.json` or another approval file. The approval record must name the current merge plan id, approved targets, approved actions, approver, timestamp, accepted risks, denied targets, notes, and hook activation decision.

Apply approved changes:

```powershell
python scripts\merge_infrastructure.py <workspace> <stage-dir> --apply --approval-file <approval.json>
```

Rollback an applied merge:

```powershell
python scripts\merge_infrastructure.py <workspace> <stage-dir> --rollback <rollback-manifest.json>
```

Run the Codex-only route contract:

```powershell
python scripts\run_codex_runtime_runner.py <workspace> --contract
```

Validate a runner result:

```powershell
python scripts\validate_codex_runtime_runner.py <result.json>
```

## Recommended First Run

For a real project, start with this sequence:

1. Run dry-run:

```powershell
python scripts\render_infrastructure.py <workspace> --dry-run
```

2. Review the `infrastructure_plan.status`, `create`, `update`, `leave_unchanged`, `warnings`, and `blocked` fields.
3. If the plan is acceptable, stage to a directory outside the workspace:

```powershell
python scripts\render_infrastructure.py <workspace> --stage C:\tmp\product-agent-os-stage
```

4. Build a merge plan:

```powershell
python scripts\merge_infrastructure.py <workspace> C:\tmp\product-agent-os-stage --plan
```

5. Inspect staged files and the approval template.
6. Fill approval only for the exact targets and actions you intend to apply.
7. Apply with approval.
8. Run the project's normal tests and update `RUNLOG.md` with evidence.

## Lifecycle State Routing

The Codex runtime runner maps project state to next work:

| Lifecycle state | Next worker | Write policy |
| --- | --- | --- |
| `uninitialized` | `workspace-discovery-auditor` | `read_only` |
| `infrastructure_planned` | `requirements-author` | `staged_only` |
| `requirements_ready` | `implementation-planner` | `staged_only` |
| `plan_ready` | `agent-team-designer` | `staged_only` |
| `team_ready` | `test-eval-designer` | `staged_only` |
| `build_active` | `builder` subagent when allowed | `approved_write` |
| `quality_gate` | `risk-reviewer` | `read_only` |
| `review_ready` | `pr-release-operator` | `staged_only` |
| `release_ready` | `learning-loop-maintainer` | `staged_only` |
| `learning_ready` | `automation-promoter` | `staged_only` |
| `maintenance` | `project-lifecycle-orchestrator` | `read_only` |

`approved_write` always requires explicit approval. Automation promotion remains candidate-only.

## Safety Rules

- Do not stage artifacts inside the target workspace.
- Do not apply a merge plan without reviewing staged files.
- Do not enable hook activation unless the approval record includes hook-specific metadata.
- Do not create active recurring automations from this plugin.
- Do not store secrets, tokens, private keys, customer data, or raw private chat logs in generated artifacts.
- Do not treat memory or chat history as source of truth for OpenAI product behavior.
- Do not claim checks passed unless they were run in the current lifecycle step.

## Validate This Plugin

From the repository root:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python tools\check_docs.py
```

The fixture eval suite covers greenfield setup, existing files, source-policy conflicts, failed verification logs, unsafe writes, safe merge behavior, rollback, automation candidate readiness, and Codex runtime runner guardrails.

## Development Notes

- Keep plugin scripts dependency-free unless a future track explicitly justifies a dependency.
- Keep bundled MCP config free of secrets; users should provide Context7 credentials through their own Codex MCP configuration when needed.
- Keep all templates synthetic and free of private data.
- Keep Product-Agent OS documentation user-facing; implementation plans and specs should remain internal history unless intentionally exposed.
- Prefer behavior-level tests and fixture evals over snapshot-only tests.
- Update source-backed docs when official OpenAI Codex plugin, skills, hooks, approvals, or automation behavior changes.
