---
title: "Archive - Product-Agent OS Agents SDK Runner Design"
---

# Archive - Product-Agent OS Agents SDK Runner Design {#product-agent-os-agents-sdk-runner-design}

> Historical source record. Dates and verdicts below describe that run; use current guides for present behavior.

Source status: `official + experiment`

Sources: [Product-Agent OS production hardening design](2026-05-14-product-agent-os-production-hardening-design.md), [source registry](../../sources/registry.md) entries for "Codex with Agents SDK", "OpenAI Agents SDK Python", "Codex models", "Codex app", "Codex CLI", "Sandbox", "Agent approvals and security", and "Agents SDK sessions".

This document records only the design boundary for a future Agents SDK runner. It does not activate the runner, create the `plugins/product-agent-os/scripts/agents_sdk_runner/` directory, install dependencies, or change the default Product-Agent OS workflow.

## Goal

An optional runner may be useful for teams that need programmable orchestration on top of Product-Agent OS. The baseline path remains unchanged: Codex App, CLI, IDE extension, skills, subagents, staged renderer, approval-gated merge, and local validators.

The runner should coordinate Product-Agent OS roles, but it must not bypass sandbox, approvals, source policy, ownership, or verification gates.

## Runtime Boundary

- Codex App, CLI, IDE extension, project skills, and `.codex/agents` remain the default runtime.
- The Agents SDK runner is an advanced optional layer and is enabled only by a separately approved plan.
- Codex MCP is treated as an execution backend for workspace work, not as a bypass for approvals.
- Any workspace mutation requires explicit ownership, approval state, and a rollback/shutdown path.
- With unknown credentials, source status, approval state, or file ownership, the runner must fail closed.

## Manager Agent

The manager agent owns lifecycle state and final output:

- reads `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, and `RUNLOG.md`;
- selects a specialist role by ownership, inputs, outputs, and stop conditions;
- rejects handoffs without sources/context used, assumptions, files touched/proposed, verification evidence, open risks, and recommended next role;
- persists decisions in checked-in artifacts, not only in session memory.

## Specialist Roles

| Role | model and reasoning | Boundary |
| --- | --- | --- |
| Product Manager | project default, medium/high | requirements and acceptance criteria |
| Architect | project default, high/xhigh | decomposition, ownership, rollback |
| Builder | project default, medium/high | one approved implementation slice |
| Tester | project default, medium/high | deterministic checks and eval evidence |
| Reviewer | project default, high/xhigh | findings-first review |
| Docs Maintainer | project default, medium/high | source policy and documentation updates |
| Release Operator | project default, medium/high | staged PR/release packet |

Model policy must define the default model, reasoning effort, escalation rules, downgrade rules, and cost/latency budget. The runner must not silently increase model tier or reasoning effort for bounded mechanical work.

## Credentials

- Credentials are read only from environment variables or platform configuration.
- Plaintext credential values are not written to prompts, docs, fixtures, runlogs, traces, sessions, memory, or templates.
- Missing credentials stop the runner before tool calls and before workspace mutation.
- Credential creation and key rotation are not part of the default runner path.

## Sessions And Tracing

- Sessions provide application conversation continuity, but they do not replace `AGENTS.md`, the source registry, `RUNLOG.md`, or checked-in memory artifacts.
- Tracing records tool names, handoffs, latency, failures, approval events, and stop reasons.
- Redaction is required before persistence: secrets, private customer data, raw private chat logs, and absolute user-specific paths are removed or replaced with synthetic labels.
- Retention policy must be defined before the runner is used on a real project.

## Eval Gates

The runner cannot be considered ready without eval gates:

- handoff completeness;
- source fidelity;
- tool boundary;
- approval handling;
- secret retention;
- rollback or shutdown behavior;
- trace/session redaction.

Each gate must have a deterministic fixture or reviewable evidence artifact.

## Non-Goals

- No default dependency installation.
- No default network access in plugin verification.
- No active automation scheduling.
- No silent changes to global Codex config.
- No replacement for Codex App, CLI, IDE extension, project skills, or `.codex/agents`.
- No implementation of the runner directory in Track 4 Tasks 6-10.
