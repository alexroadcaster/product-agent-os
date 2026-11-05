# Product-Agent OS Codex compatibility

Source status: `official + experiment`

## Component inventory — GAP-02, 2026-11-05

Input: a local package path. The shared `plugin_components.py` resolver supplies compatibility, package inventory, discovery, methodology audit and system-file hygiene. Output separates format/version, selected component paths, skill/MCP server names, transports, issues and `host_status: not_verified`. Commands, endpoint URLs, environment values and secrets are neither returned nor executed.

| Input | Rule | Result |
| --- | --- | --- |
| Recognized root `plugin.json` | Agent Plugins 1.0.0 identity; portable `skills/` and `mcp.json` take precedence | `present_unverified` for supported structure |
| `extensions.com.openai` | Replaces compatibility settings as a whole; no field merging | Explicit `settings_source` |
| `.codex-plugin/plugin.json` | Compatibility format when root manifest is absent | Paths constrained to package |
| MCP `mcpServers` wrapper | Portable schema or Codex compatibility wrapper | Transport checked separately from host |
| Flat `.mcp.json`, unknown schema, invalid types, escaping paths | Preserve observation without silent fallback | `needs_review` |

The current package remains `needs_review`: `context7` is observed in legacy flat `.mcp.json`. No automatic migration occurs. Validation covers a bounded structural subset, not full JSON Schema validation. Auth extensions and unsupported constructs need separate review.

| Component / surface | Codex App | CLI | IDE extension |
| --- | --- | --- | --- |
| Standalone skills | Documented mechanism; selection and invocation checked separately | Same | Same |
| Local executors/scripts | Project-specific checks required | Project-specific checks required | Project-specific checks required |
| Native package, MCP, hooks | Client/version/auth/component receipt required | Separate receipt required | Separate receipt required |

Output: reviewable inventory; next decide MCP declaration migration, then verify the intended host. Neither `supported_surfaces` nor manifest presence proves runtime acceptance. Sources checked 2026-11-05: [Build plugins](https://developers.openai.com/plugins/build/plugins), [manifest schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json), [MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json).

Sources: [Codex plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://learn.chatgpt.com/docs/build-skills), [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Codex hooks](https://learn.chatgpt.com/docs/hooks), [Agent approvals and security](https://learn.chatgpt.com/docs/permissions), [Codex with Agents SDK](https://developers.openai.com/codex/guides/agents-sdk), [Product-Agent OS architecture](architecture.md).

Compatibility describes checked local package structure; each component still needs host evidence. It does not approve live execution, provider calls, external writes, hosted docs, database access, automation activation or git actions.

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

Codex App, CLI and IDE extension are intended workflow surfaces; native package, skills, MCP and hooks require separate component evidence. They are not permission to mutate target workspaces, GitHub, CI, package registries, production databases, hosted documentation, security systems or schedules without explicit approval and current verification evidence.

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

## Contract freshness: 2026-11-03

The documentation audit does not promote package compatibility into proven operation on every current Codex surface. Acceptance records client/version/auth, selected model, effective permissions, parent MCP and scenario-specific evidence. Official sources: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Permissions](https://learn.chatgpt.com/docs/permissions), [Hooks](https://learn.chatgpt.com/docs/hooks).

| Audit ID | Current state | Separate follow-up |
| --- | --- | --- |
| OPEN-PERM | Parent `:workspace`; role restrictions are behavioral; unsupported overrides removed | Fresh-session effective permissions evidence |
| OPEN-MCP | MCP configured on parent; agents inherit it; validator no longer requires agent-local MCP | Fresh-session effective tool availability |
| OPEN-MODEL | GPT-6.1 Sol/Terra pins selected; prior efforts preserved in 23 active/staged profiles | Authorized same-effort quality/cost/latency comparison |
| OPEN-BASELINE | Legacy requirement repaired; parent and rendered config semantics validated | Local regression gates; no runtime claim |
| OPEN-RUNTIME | New Agents API/Responses capabilities are documented | Separate implementation and runtime evidence if the route is selected |

The owner authorized technical follow-up on 2026-11-03. Configuration, profiles, templates and validators are updated; activation and behavioral promotion remain open. Exact commands and results belong to the [plan](../superpowers/plans/2026-11-03-gpt6-documentation-refresh.md).

## Components and runtime evidence

Record compatibility by client/version/authentication/component. A local fixture or manifest does not prove native installation, trust or runtime success. The current package is needs_review as described above; native host support cannot be inferred from standalone skills. See [surface matrix](../codex/surfaces.md) and [package contract](technical.md).
