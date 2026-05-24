---
name: workspace-discovery-auditor
description: Perform a read-only Product-Agent OS workspace audit and return a staged discovery packet for lifecycle planning.
---

# Workspace Discovery Auditor

## Trigger

Use this skill when a workspace is uninitialized, when project state is uncertain, or when a Product-Agent OS lifecycle run needs a read-only audit before requirements or planning.

## Boundaries

This is a Track 2 skill. Produce a staged workspace audit packet only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not write files, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim detected commands pass, runtime behavior works, or control-plane readiness without evidence from the current run.
Ask for approval before external writes, permission changes, deployment, billing, auth, database, production operations, or expanded read scope.

Read shared references when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

## Inputs

- Workspace path and allowed read scope.
- User goal, constraints, target runtime, and known project archetype when available.
- Existing `AGENTS.md`, README, package manifests, build files, tests, docs, `.codex/`, CI files, and prior lifecycle packets.
- Preferred discovery helper: `plugins/product-agent-os/scripts/detect_project.py`.

## Process

1. Keep the audit read-only.
2. Prefer `plugins/product-agent-os/scripts/detect_project.py` for stack and control-plane discovery when it is available.
3. Inventory project type, languages, frameworks, tests, build commands, documentation, existing Codex assets, and control-plane files.
4. Identify missing control-plane artifacts for the next lifecycle state.
5. Infer complexity profile with confidence and source notes.
6. Return a staged `workspace_audit` packet and route back to `project-lifecycle-orchestrator`.

## Outputs

Return a workspace audit packet:

```yaml
workspace_audit:
  status: "ready_for_plan | blocked | needs_user_input"
  detected_stack: []
  existing_control_plane: []
  missing_control_plane: []
  existing_codex_assets: []
  risks: []
  complexity_profile:
    name: ""
    confidence: ""
  next_action: ""
```

## Verification

Check that every detected stack or control-plane claim cites observed files, command output, or explicit user input. Do not claim without evidence.

## Failure Modes

- If the workspace path is inaccessible, stop and request a valid path.
- If read scope is unclear, ask a blocking question before broader inspection.
- If `detect_project.py` is unavailable, use read-only inventory and report that fallback.
- If secrets appear in inspected files, stop and request redaction without repeating secret values.
- If the project needs writes, return proposed next files only.

## Final Response Contract

Return status, detected stack, existing and missing control-plane assets, Codex assets, risks, complexity profile, evidence notes, approval requirements, and next lifecycle action.
