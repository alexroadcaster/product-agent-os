# Product-Agent OS Codex compatibility

Source status: `official + experiment`

Sources: [Codex plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://developers.openai.com/codex/skills), [Subagents](https://developers.openai.com/codex/subagents), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md), [Codex hooks](https://developers.openai.com/codex/hooks), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex with Agents SDK](https://developers.openai.com/codex/guides/agents-sdk), [Product-Agent OS architecture](architecture.md).

Compatibility means the package fits Codex surfaces. It does not approve live execution, provider calls, external writes, hosted docs, database access, automation activation or git actions.

## Inputs

- current `.codex-plugin/plugin.json` and packaged plugin metadata;
- local skills, scripts, templates, MCP declarations and staged hooks;
- Codex App, CLI and IDE extension workflow expectations;
- current `AGENTS.md`, sandbox, approvals and source policy;
- compatibility validator output and any accepted gaps.

## Outputs

- package compatibility status;
- supported Codex surfaces and non-goals;
- approval boundary for live systems, provider calls, external writes, hosted docs, database access, active automation and git actions;
- verification commands for package and docs closure;
- residual risks when a compatibility claim depends on current official Codex behavior.

## Canonical Safety Boundary

Product-Agent OS keeps a conservative Codex boundary:

- no live model call from compatibility checks;
- no separate OpenAI API key requirement for the Codex runtime runner;
- no standalone Agents SDK activation hidden behind the plugin;
- no global config mutation;
- no silent MCP/server/hook/automation activation;
- no unapproved external writes;
- no hosted docs or DB introspection bypass;
- no readiness claims from detection.

Codex App, CLI, IDE extension, skills, MCP declarations and staged hooks are supported package surfaces. They are not permission to mutate target workspaces, GitHub, CI, package registries, production databases, hosted documentation, security systems or schedules without explicit approval and current verification evidence.

## Compatible Surfaces

| Surface | Supported use | Boundary |
| --- | --- | --- |
| `.codex-plugin/plugin.json` | Plugin manifest and packaged capability declaration. | Manifest presence is compatibility evidence, not publication approval. |
| Codex App | Interactive steering, ambiguity resolution, review and local workspace work. | User approvals and sandbox still govern actions. |
| CLI | Local deterministic checks, renderers, validators and staged artifact generation. | Commands must respect project policy and approval scope. |
| IDE extension | Code navigation, review and implementation support. | IDE context is not source of truth by itself. |
| skills | Repeatable methods with inputs, outputs, verification and failure modes. | A skill can recommend actions but cannot grant external permission. |
| subagents | Parallel or specialized work when ownership is clear. | Handoff must include files, context, expected evidence and stop conditions. |
| `AGENTS.md` | Durable project rules and operating constraints. | Local project rules cannot override stronger system/developer instructions. |
| staged hooks | Hook templates and staged proposals. | Hooks are not silently activated. |
| MCP | Declared tool context and integration boundaries. | MCP access is not automatically safe or approval-free. |
| Agents SDK | Product/runtime app architecture when explicitly chosen. | It is not the hidden runtime layer for this plugin. |

## Non-Goals

Product-Agent OS compatibility checks do not:

- publish plugins or docs;
- create schedules, recurring automations or GitHub Actions;
- start local servers for verification;
- run browser automation;
- call external providers or live model/API endpoints;
- mutate canonical graph facts;
- stage, commit, push or open PRs;
- certify legal, security or compliance readiness.

Those actions require explicit owner approval, current evidence and a rollback or stop condition.

## Verification

Use these checks when package boundaries or docs change:

```powershell
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
```

Use strict MkDocs when navigation, Mermaid, Markdown extensions or generated site output changes:

```powershell
python -m mkdocs build --strict
```

The compatibility validator should stay deterministic. If it needs live provider, browser, hosted docs or database evidence, that evidence belongs in a separate approval-bound route, not in baseline compatibility.

## Live Execution Boundaries

The live layer stays disabled until each action has its own owner-approved packet:

- local runtime launch;
- browser automation smoke;
- external embedding/reranker/LLM provider pilot;
- canonical graph mutation pilot;
- git release, push, PR or publication action.

Approvals are not bundled. Approval for one surface does not grant another.

## Risks

- A compatible package can still be operationally unsafe if a user activates hooks, MCP servers, automations or external systems without evidence.
- Generated cockpit/dashboard/report outputs can look authoritative; the docs must keep source-boundary labels visible.
- Agent handoff quality matters more than the number of subagents. Parallel work without ownership can increase risk.
- Official Codex behavior can evolve; source-backed claims should be reviewed against current official docs when product surfaces change.

Next artifact: use [Packaging And Closure](packaging-and-closure.md) for release evidence and [Approval-Bound Real Testing](approval-bound-real-testing.md) before any live execution.
