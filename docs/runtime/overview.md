# Codex Automation & Runtime

Source status: `official + experiment`  
Источники: [Codex CLI features](https://developers.openai.com/codex/cli/features), [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Codex automations](https://developers.openai.com/codex/app/automations), [Codex with Agents SDK](https://developers.openai.com/codex/guides/agents-sdk).

## Runtime decision matrix

| Runtime | Использовать когда | Главный риск |
| --- | --- | --- |
| Codex App | Parallel threads, worktrees, artifacts, automations | Too many long threads without task boundaries |
| CLI interactive | Local exploratory or implementation session | Context bloat |
| `codex exec` | Non-interactive scripted task | Weak prompt or missing environment setup |
| Cloud/Web | Background repository work | Missing setup, network, secrets, environment assumptions |
| GitHub Action | CI/PR automation | Overbroad permissions |
| Codex MCP | Agents SDK orchestrates Codex as tool | Tool boundary and approval policy |
| Automations | Stable recurring workflows | Automating before workflow is reliable |

## Rule of thumb

- Use App/CLI while discovering the workflow.
- Turn repeated method into a skill.
- Turn stable recurring work into automation.
- Use `codex exec` for scripted one-shot jobs.
- Use Codex MCP when a higher-level agent orchestrator needs workspace execution.
- Use GitHub Action when the trigger belongs to CI/PR events.

## Runtime artifacts

Every runtime should leave evidence:

- prompt or task packet;
- loaded instruction sources;
- commands run;
- files changed;
- checks/evals;
- final decision or PR link.

