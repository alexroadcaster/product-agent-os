# Product-Agent OS Agents SDK Runner Design

Source status: `official + experiment`

Sources: [Product-Agent OS production hardening design](2026-05-14-product-agent-os-production-hardening-design.md), [source registry](../../sources/registry.md) entries for "Codex with Agents SDK", "OpenAI Agents SDK Python", "Codex models", "Codex app", "Codex CLI", "Sandbox", "Agent approvals and security", and "Agents SDK sessions".

Этот документ фиксирует только design boundary для будущего Agents SDK runner. Он не активирует runner, не создает каталог `plugins/product-agent-os/scripts/agents_sdk_runner/`, не устанавливает зависимости и не меняет default workflow Product-Agent OS.

## Цель

Опциональный runner может понадобиться командам, которым нужна программируемая orchestration поверх Product-Agent OS. Базовый путь остается прежним: Codex App, CLI, IDE extension, skills, subagents, staged renderer, approval-gated merge и локальные validators.

Runner должен координировать роли Product-Agent OS, но не обходить sandbox, approvals, source policy, ownership и verification gates.

## Runtime Boundary

- Codex App, CLI, IDE extension, project skills и `.codex/agents` остаются default runtime.
- Agents SDK runner является advanced optional layer и включается только отдельным утвержденным планом.
- Codex MCP рассматривается как execution backend для работы с workspace, а не как bypass для approvals.
- Любая workspace mutation требует явного ownership, approval state и rollback/shutdown path.
- При неизвестных credentials, source status, approval state или file ownership runner должен fail closed.

## Manager Agent

Manager agent владеет lifecycle state и final output:

- читает `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` и `RUNLOG.md`;
- выбирает specialist role по ownership, inputs, outputs и stop conditions;
- отклоняет handoff без sources/context used, assumptions, files touched/proposed, verification evidence, open risks и recommended next role;
- сохраняет решения в checked-in artifacts, а не только в session memory.

## Specialist Roles

| Role | model and reasoning | Boundary |
| --- | --- | --- |
| Product Manager | project default, medium/high | requirements и acceptance criteria |
| Architect | project default, high/xhigh | decomposition, ownership, rollback |
| Builder | project default, medium/high | one approved implementation slice |
| Tester | project default, medium/high | deterministic checks и eval evidence |
| Reviewer | project default, high/xhigh | findings-first review |
| Docs Maintainer | project default, medium/high | source policy и documentation updates |
| Release Operator | project default, medium/high | staged PR/release packet |

Model policy должен задавать default model, reasoning effort, escalation rules, downgrade rules и cost/latency budget. Runner не должен молча повышать модель или reasoning для bounded mechanical work.

## Credentials

- Credentials читаются только из environment variables или platform configuration.
- Plaintext credential values не пишутся в prompts, docs, fixtures, runlogs, traces, sessions, memory или templates.
- Missing credentials останавливают runner до tool calls и до workspace mutation.
- Credential creation и key rotation не входят в default runner path.

## Sessions And Tracing

- Sessions дают application conversation continuity, но не заменяют `AGENTS.md`, source registry, `RUNLOG.md` или checked-in memory artifacts.
- Tracing фиксирует tool names, handoffs, latency, failures, approval events и stop reasons.
- redaction обязателен до persistence: secrets, private customer data, raw private chat logs и absolute user-specific paths удаляются или заменяются synthetic labels.
- Retention policy должен быть задан до использования runner на реальном проекте.

## Eval Gates

Runner нельзя считать готовым без eval gates:

- handoff completeness;
- source fidelity;
- tool boundary;
- approval handling;
- secret retention;
- rollback или shutdown behavior;
- trace/session redaction.

Каждый gate должен иметь deterministic fixture или reviewable evidence artifact.

## Non-Goals

- Нет default dependency installation.
- Нет default network access в plugin verification.
- Нет active automation scheduling.
- Нет silent changes в global Codex config.
- Нет замены Codex App, CLI, IDE extension, project skills или `.codex/agents`.
- Нет реализации runner directory в Track 4 Tasks 6-10.
