# Instruction and tool-use compliance

Source status: `official + project evidence`

Sources: [Agent Skills](https://developers.openai.com/codex/skills), [Plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [`AGENTS.md`](https://developers.openai.com/codex/guides/agents-md), [Hooks](https://developers.openai.com/codex/hooks), [Permissions](https://developers.openai.com/codex/permissions), [Subagents](https://developers.openai.com/codex/subagents), [Skill exposure and invocation boundary](../diagrams/skill-exposure-and-invocation.en.md), `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`.

This page documents how Product-Agent OS should handle instruction compliance, tool-use compliance, skill/plugin exposure and self-learning-loop requests. It does not claim that auto-engagement is already fixed. Current status is `planned-only` for Batch 42 execution and `implemented_source_docs_no_site_rebuild` for this documentation page.

## Checked Layers

| Layer | Proves | Does not prove |
| --- | --- | --- |
| Source bundle | The repository contains the plugin, skills, scripts, templates and docs. | The skill is available in the installed cache or active session. |
| Installed plugin cache | A local installed copy may exist. | The current Codex session sees every skill or invokes it implicitly. |
| Active session | The session actually received some skill/plugin metadata. | The route is correct for every prompt. |
| Route/eval evidence | The prompt is classified through the intended lifecycle/compliance path. | Config/cache mutation, release readiness or external action approval. |
| Fresh-session proof | A new session sees the expected state after changes. | Older sessions refreshed automatically. |

## Invocation Policy

Official Codex docs describe explicit invocation, where the user names a skill, and implicit invocation, where the task matches the skill `description`. Product-Agent OS uses a stricter local policy:

| Mode | Use when | Gate |
| --- | --- | --- |
| `explicit_only` | High-risk skills, release, automation, external writes, cache/config mutation, provider/API, browser/runtime or security-sensitive work. | The user explicitly requests the skill/plugin/agent route. |
| `narrow_implicit` | Read-only discovery, docs maintenance, planning, compliance audit or learning-loop triage when the prompt clearly matches the Product-Agent OS boundary. | Route/eval evidence and no-unapproved-actions proof. |
| `blocked_implicit` | Any skill with `allow_implicit_invocation: false`, unclear ownership or missing evidence. | Explicit user request or policy-change approval. |

`allow_implicit_invocation` is policy metadata, not quality proof. Even when implicit invocation is allowed, approval settings, sandbox, permissions, hook trust and external-service auth still apply.

## No-Auto-Apply Learning Loop

The Product-Agent OS self-learning-loop may record a lesson, candidate rule, skill update candidate, eval follow-up or owner question. It must not itself:

- change `~/.codex/config.toml`, project `.codex/config.toml`, installed plugin cache or global guidance;
- activate hooks, automations, MCP servers, an Agents SDK runner or external workflows;
- stage, commit, push, create a PR, publish, deploy or share a plugin;
- store secrets, raw private chat logs, customer data or unredacted findings.

Every candidate needs owner review, a rollback/disable path and separate approval.

## Compliance Packet

A claim that "Product-Agent OS now engages correctly" needs a packet with these fields:

| Field | Required evidence |
| --- | --- |
| `source_bundle_status` | Source tree path, manifest/skill list, agent metadata and policy class. |
| `installed_cache_status` | Read-only cache inventory or explicit not-inspected gap. |
| `active_session_status` | Fresh-session exposure, missing skills and restart/new-thread boundary. |
| `route_eval_status` | Prompt fixtures or transcript evals for compliance/tool-use prompts. |
| `official_source_status` | Current official Codex docs checked date and supported/unsupported claims. |
| `approval_boundary` | Exact surfaces that remain approval_required. |
| `no_unapproved_actions` | Cache/config/global/external/git/release/browser/provider/automation flags all false unless explicitly approved. |

## Unsupported Claims

This page does not support claims that:

- all Product-Agent OS skills are visible in every active session;
- auto-engagement is fixed;
- the installed cache has been refreshed;
- global Codex policy or project config has been changed;
- hooks are trusted in every new session;
- the self-learning-loop can mutate skills, memory, rules, hooks or automations automatically;
- docs/source evidence proves runtime/browser/provider behavior, publication or release readiness.

## Next Safe Action

If an operator sees Product-Agent OS fail to engage for a relevant prompt, the first safe step is a read-only source/cache/session packet, followed by a route/eval packet. Cache refresh, global config writes, plugin sharing, hook trust changes and fresh-session proof remain separate approvals.

## Current route and evidence

Applicable full/concise lifecycle, trust and terminal markers are in the [hook guide](../runtime/worktrees-hooks-rules.md). The 2026-11-03 local receipt covers tested Desktop routes; completeness of all mutation channels and silent Stop tracing are not claimed.
