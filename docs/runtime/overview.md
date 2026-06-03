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

## Product-Agent OS runtime decision matrix

| Surface | Использовать когда | Разрешенный режим | Approval boundary |
| --- | --- | --- | --- |
| Static graph/cockpit | Нужно ориентировать agent team, review или docs update по workspace topology. | Read-only scan, staged `.codex/product-agent-os/` artifacts, generated view labels. | Generated graph/cockpit are not source of truth and do not authorize implementation claims. |
| Disabled local runtime | Нужно проверить API contract, auth boundary, lifecycle and graph-only fallback. | Contract validation only; runtime stays `disabled_by_default_not_started`. | Live server launch needs a separate approved runtime packet. |
| Browser smoke | Нужно проверить generated view labels, console/network expectations or mobile overflow. | Planned/staged QA evidence unless owner approves live runtime and browser automation. | Actual browser automation is a separate approval surface. |
| Provider calls | Нужно оценить embedding/reranker/LLM provider value. | Stage redaction/cache/budget/baseline/threshold fallback packet. | External provider/API/model calls require explicit approval and current eval policy. |
| External systems and git | Нужно publish, tag, PR, CI mutation, hosted docs or package action. | Draft packet, release/readiness evidence and rollback plan. | External writes and git stage/commit/push/PR are explicit-only. |

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
