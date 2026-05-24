# Worktrees, hooks, rules

Source status: `official + experiment`  
Источники: [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Codex worktrees](https://developers.openai.com/codex/app/worktrees), [Codex hooks](https://developers.openai.com/codex/config/hooks), [Codex rules](https://developers.openai.com/codex/config/rules), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security).

## Worktree strategy

Используйте worktrees, когда:

- несколько threads могут менять одни файлы;
- задача потенциально широкая;
- нужен изолированный PR;
- long-running job может продолжаться параллельно с локальной работой.

Не используйте один live thread на весь проект. Один thread должен соответствовать одному coherent unit of work.

## Hooks

Hooks подходят для deterministic checks around agent work:

- block generated-file edits without approval;
- run lightweight format/lint check;
- log command execution metadata;
- enforce forbidden paths;
- remind about required verification.

Hooks не заменяют human review и не должны хранить secrets.

## Rules

Rules описывают policy, которую Codex должен учитывать перед действиями. Хорошие rules:

- narrow;
- auditable;
- aligned with sandbox/approvals;
- tested on real workflows.

## Failure modes

| Failure | Prevention |
| --- | --- |
| Two agents edit same files | Worktree per task or explicit ownership |
| Hook blocks valid task | Narrow rule and allow documented approval |
| Agent misses project conventions | `AGENTS.md` + nested instructions |
| Long thread drifts | `/compact`, `/fork`, one thread per coherent task |
| Automation runs too early | Manual skill workflow first |

