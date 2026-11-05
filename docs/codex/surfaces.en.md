# Codex Work Surfaces

Source status: `official`  
Sources: [Codex app](https://developers.openai.com/codex/app), [Codex CLI](https://developers.openai.com/codex/cli), [Codex IDE extension](https://developers.openai.com/codex/ide), [Codex cloud](https://developers.openai.com/codex/cloud).

## Choosing a surface

| Surface | When to use | Strength | Risk |
| --- | --- | --- | --- |
| Codex App | Multiple threads, review, worktrees, automations, artifacts | Command center for parallel work | Requires discipline in branch management and approvals |
| CLI | Local terminal work, reproducible commands, transcript | Explicit context, command control, convenience for power users | Files and boundaries must be specified explicitly |
| IDE extension | Work next to the editor, open files, selections, `@file` | Fast code context and local follow-up | It is easy to rely on incomplete editor context |
| Codex cloud | Long background tasks, PR, GitHub-linked work | Parallelism and isolation from the local machine | Setup, network and secrets must be described in advance |

## Codex App

Official documentation describes Codex App as a desktop command center for parallel Codex threads, built-in worktree support, automations and Git functionality. For an advanced user, this is the main surface for managing several independent tasks.

Operational guidance:

- each thread must have a concrete outcome;
- enable worktree isolation for write-heavy tasks;
- use automations for repeated checks;
- before accepting the result, inspect the diff, verification commands and artifacts.

## CLI

Codex CLI runs locally from the terminal and can read, modify and run code in the selected directory. This is the best mode for reproducible workflows because commands, approvals and context are easier to keep explicit.

CLI task template:

```text
Goal: ...
Context: @path/to/file.md @path/to/schema.json
Constraints: do not change the public API, do not install dependencies without approval.
Definition of done: ...
Verification: run ...
```

## IDE extension

IDE extension is useful when editor context matters: open files, selections, `@file` references and follow-up on cloud work. For complex tasks, record the context in writing because open files do not replace requirements.

## Codex cloud

Cloud fits background tasks, especially when work can proceed independently from the current local session. For cloud tasks, record separately:

- repository and branch;
- setup steps;
- internet access policy;
- secrets availability only where needed;
- expected PR or artifact.

## Models and surface boundaries

CLI version does not establish Codex App or IDE extension version. API-key and ChatGPT sign-in can have different availability/retirement conditions. Match client/auth/model/effort using the [shared reference](models-and-reasoning.md); account availability and runtime activation need their own evidence.

## Choose a surface: checked 2026-11-05

| Scenario | Surface | Check before work |
| --- | --- | --- |
| Local files and commands | Desktop Codex / CLI / IDE extension | Workspace, effective permissions, project instructions |
| Install a plugin | Supported Desktop/CLI, ChatGPT web/mobile | Components, authentication and plan; IDE has no native plugins |
| Work in a prepared environment | Current Codex Cloud | Published environment, network policy, variables/secrets |
| Cloud orchestration with local access | Work Cloud + local computer access | Local execution and cloud orchestration controls separately |
| Repeat a tested workflow | Scheduled tasks | Local/cloud mode, machine availability, destination and authority |
| Build an agent application | Agents API / Agents SDK / Responses | Ownership of loop/state, deployment, tools and approvals |

Sources: [Plugins](https://learn.chatgpt.com/docs/plugins), [MCP](https://learn.chatgpt.com/docs/extend/mcp), [Cloud](https://learn.chatgpt.com/docs/environments/cloud-environments). Availability depends on account, client, authentication, rollout and managed policy. Discovering a Desktop only plugin on the web does not make it usable there.

### Set up a current Cloud environment

1. Choose **Work in → Cloud → Create environment** and authorized repositories.
2. Specify dependencies, versions and services in the conversation. Codex prepares and tests setup; writing an install script manually is optional.
3. Review **Install script**, **Start skill**, network policy and configuration.
4. **Save** stores settings; **Publish** captures the prepared environment for new tasks. After changes use **Republish** and a new task; existing tasks retain their state.
5. Check a project command in a new task and access only to authorized destinations.

Environment variables reach programs directly. Network secrets use placeholders and proxy substitution for allowed HTTPS destinations (port 443), during setup and tasks. Do not apply the legacy setup-only secret rule to current Cloud. Network policy, credential delivery and service permissions are separate checks. When access is missing, identify the required destination and identity rather than broadening policy automatically.

Legacy Cloud has separate setup/maintenance/network rules. Do not mix [current Cloud documentation](https://learn.chatgpt.com/docs/environments/cloud-environments) and [legacy internet settings](https://learn.chatgpt.com/docs/cloud/internet-access) in one recipe.
