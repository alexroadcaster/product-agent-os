# Security, sandbox and approvals

Source status: `official`  
Sources: [Sandbox](https://developers.openai.com/codex/concepts/sandboxing), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex cloud](https://developers.openai.com/codex/cloud).

## Baseline model

Sandbox is a technical boundary: which files Codex can modify, which commands it can run and whether network access is available. Approval policy is a governance boundary: when Codex must stop and ask for permission.

A safe baseline for local work:

```text
sandbox_mode = "workspace-write"
approval_policy = "on-request"
approvals_reviewer = "user"
```

This mode allows work inside the workspace, but requires approval for actions outside the boundary, network commands or other sensitive operations.

## Sandbox modes

| Mode | Meaning | Use for |
| --- | --- | --- |
| `read-only` | Codex can read, but should not change files or run substantial commands without permission | Planning, review, audit |
| `workspace-write` | Codex can read, modify the workspace and run routine commands within the project boundary | Most local tasks |
| `danger-full-access` | Codex runs without sandbox restrictions | Only deliberately and for a short time |

## Network access

Under the official model, Codex should not freely access the network by default during agentic work. In cloud setup, network access may be available during environment preparation, while the agent phase usually requires a separate internet access decision.

Practical rule:

- documentation can be checked against official sources;
- install and package manager commands require explicit understanding of what will be downloaded;
- secrets must not end up in prompts, docs, memory or artifacts.

## Approval checklist

Before approval, ask:

- Does the command write outside the workspace?
- Does the command use the network?
- Can the command delete, overwrite or send data?
- Is there a narrower way to grant access?
- Can broad access be replaced with a command prefix rule?

