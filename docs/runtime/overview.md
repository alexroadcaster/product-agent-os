# Codex Automation & Runtime

Source status: `official + experiment`  
Источники: [Codex CLI features](https://developers.openai.com/codex/cli/features), [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Codex automations](https://developers.openai.com/codex/app/automations), [Codex with Agents SDK](https://developers.openai.com/codex/guides/agents-sdk).

## Runtime decision matrix

| Runtime | Использовать когда | Главный риск |
| --- | --- | --- |
| Codex App | Parallel threads, worktrees, artifacts, automations | Too many long threads без task boundaries |
| CLI interactive | Local exploratory или implementation session | Context bloat |
| `codex exec` | Non-interactive scripted task | Weak prompt или missing environment setup |
| Cloud/Web | Background repository work | Missing setup, network, secrets, environment assumptions |
| GitHub Action | CI/PR automation | Overbroad permissions |
| Codex MCP | Agents SDK orchestrates Codex как tool | Tool boundary и approval policy |
| Automations | Stable recurring workflows | Automation до надежности workflow |

## Product-Agent OS runtime decision matrix

| Surface | Использовать когда | Разрешенный режим | Approval boundary |
| --- | --- | --- | --- |
| Static graph/cockpit | Нужно ориентировать agent team, review или docs update по workspace topology. | Read-only scan, staged `.codex/product-agent-os/` artifacts, generated view labels. | Generated graph/cockpit являются не является каноническим источником и не authorize implementation claims. |
| Disabled local runtime | Нужно проверить API contract, auth boundary, lifecycle и graph-only fallback. | Contract validation only; runtime stays `disabled_by_default_not_started`. | Live server launch требует separate approved runtime packet. |
| Browser smoke | Нужно проверить generated view labels, console/network expectations или mobile overflow. | Planned/staged QA evidence пока owner approves live runtime и browser automation. | Actual browser automation является separate approval surface. |
| Provider calls | Нужно оценить embedding/reranker/LLM provider value. | Stage redaction/cache/budget/baseline/threshold fallback packet. | External provider/API/model calls требуют explicit approval и текущий eval policy. |
| External systems и git | Нужно publish, tag, PR, CI mutation, hosted docs или package action. | Draft packet, release/readiness evidence и rollback plan. | External пишет и git stage/commit/push/PR являются explicit-only. |

## Rule из thumb

- Используйте App/CLI while discovering workflow.
- Turn repeated method в skill.
- Turn stable recurring work в automation.
- Используйте `codex exec` для scripted one-shot jobs.
- Используйте Codex MCP когда higher-level agent orchestrator требует workspace execution.
- Используйте GitHub Action когда trigger belongs к CI/PR events.

## Runtime artifacts

Every runtime следует leave evidence:

- prompt или task packet;
- loaded instruction sources;
- commands run;
- files changed;
- checks/evals;
- final decision или PR link.

## Карта API runtimes и степень реализации

[Agents API](https://developers.openai.com/api/docs/guides/agents) выполняет managed Codex harness на стороне OpenAI; Agents SDK запускает agent loop внутри приложения; Responses API дает прямой API-контракт с optional hosted orchestration. [Responses Multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent) — отдельная beta-возможность, не синоним Codex subagents.

Для выбора владельца state/tools/approvals используйте [таблицу SDK patterns](../agent-systems/sdk-patterns.md) и [диаграмму runtimes](../diagrams/runtime-decision-map.md). Product-Agent OS документирует эти маршруты, но данное обновление не реализует Agents API, async/steering или новый hosted runner. Статусы «документировано», «спроектировано», «реализовано», «проверено в runtime» требуют разных доказательств и не следуют друг из друга автоматически.
