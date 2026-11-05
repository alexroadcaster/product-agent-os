# Security, permissions and approvals

Source status: `official + experiment`

Checked 2026-11-03: [Permissions](https://learn.chatgpt.com/docs/permissions), [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference).

Sandbox and permissions are technical controls on local command execution. Approval policy controls eligible prompts. A role description, source document or skill does not grant privileges. This repository requires separate authorization for external writes, provider/model calls, browser, Git and activation changes.

## Choose one configuration scheme

Permission profiles are beta. Select either `default_permissions` / `[permissions]` or legacy `sandbox_mode` / `[sandbox_workspace_write]`, not both. Inspect all effective layers and managed policy; examples are in [configuration](configuration.md). `:workspace` protects `.git`, `.agents`, `.codex`, `.aws`; a project directory being writable does not make every child writable. Legacy `read-only`, `workspace-write` and `danger-full-access` remain distinct modes; the last removes local sandbox restrictions and is not a remedy for approval friction.

Custom agents inherit parent permissions and approvals. A reviewer instructed to avoid edits is behaviorally read-only, not a separately enforced read-only sandbox. Agent-local sandbox/MCP settings do not override the parent. Actual isolation requires applicable execution controls and fresh-session evidence.

## Network and tool surfaces

| Surface | Control boundary | What not to infer |
| --- | --- | --- |
| Local commands | Effective filesystem/network policy and command sandbox | A writable workspace does not imply network access |
| Command destination filtering | Active network proxy and domain rules | `network.enabled = true` alone does not activate domain filtering |
| Web search | Product/tool policy | Not governed by the command proxy allowlist |
| MCP | Parent MCP configuration, tool/server policy and approvals | Declaration is not connection or successful execution |
| Apps/connectors | App/tool authorization and approval settings | Command network policy is not a connector policy |
| Browser/computer tools | Tool-specific controls and task authorization | Local command sandbox is not universal browser isolation |

Domain rules require `features.network_proxy = true` or an enabled managed proxy. An active proxy without allow entries blocks domain requests; deny rules take precedence. Local, cloud setup and cloud agent phases have different network controls: inspect the chosen surface rather than asserting a universal default.

## Approval and data review

Before a sensitive action, identify destination, data, side effects, existing authority and the narrowest usable permission. A public documentation lookup and an install/provider operation are different actions. Never include secrets or unnecessary private data in prompts, docs, memory or evidence. `approvals_reviewer` does not widen the sandbox or re-review already allowed actions.

## Verification boundary

Static config parsing cannot prove effective runtime policy. Record client/version/auth, loaded configuration, parent permissions, selected tool and observed permitted/denied behavior before an activation claim. The current documentation refresh changes no permissions; unresolved project contracts are listed in [Codex compatibility](../product-agent-os/codex-compatibility.md).

## Cloud and hooks

Current Cloud network secrets and direct variables use different delivery mechanisms; the legacy setup-only rule is not universal. See [Cloud setup](surfaces.md) and [hook trust/failure boundaries](../runtime/worktrees-hooks-rules.md). Check execution and orchestration separately.
