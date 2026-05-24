# OpenAI Codex Knowledge Base

Markdown + HTML knowledge base for advanced OpenAI Codex, product-agent workflows, skills, runtime automation, prompt/context engineering, and agentic product delivery.

## Purpose

This project collects official OpenAI Codex documentation, converts it into Russian learning and operating instructions, and keeps community insights separate from authoritative guidance. The current milestone treats Codex as an operating system for product-agent workflows: `AGENTS.md` defines persistent rules, skills define reusable methods, automations define schedule, runtime tools execute work, and eval loops prove quality.

The knowledge base covers:

- Codex surfaces: App, CLI, IDE, cloud, workflows, approvals, sandboxing.
- Codex use-case extraction: official taxonomy, reusable workflow patterns, and path from use case to skill/plugin.
- Prompt and context engineering: question design, context packing, grounded answering, hallucination control.
- Agent systems: subagents, skills, AGENTS.md, memory, sessions, handoffs, guardrails, tracing, eval loops.
- Product-agent workflows: idea, spec, plan, implementation, review, eval, PR, release notes, lessons.
- Codex runtime: App, CLI, `codex exec`, Codex MCP, app-server, GitHub Action, automations, worktrees, hooks, rules.
- Playbooks: full feature delivery, workflow-to-skill, use-case-to-plugin, eval-driven improvement, product-ready PR, docs update, code review.
- Templates: prompt packet, control-plane files, RUNLOG, product skill, plugin blueprint.
- HTML rendering through MkDocs Material with Mermaid diagrams.

## Documentation Map

| Section | Purpose |
| --- | --- |
| `docs/diagrams/` | Diagram atlas for project delivery, agent teams, runtime choices, skills, and verification |
| `docs/codex/` | Codex concepts, surfaces, configuration, security, workflows, use-case analysis |
| `docs/prompting/` | Prompt and context engineering practices |
| `docs/product-agent/` | Product-agent lifecycle, roles, control-plane files |
| `docs/product-agent-os/` | User-facing Product-Agent OS plugin docs, installation boundary, technical features, and architecture diagrams |
| `docs/methodologies/` | Large-project methodology plans for business, domain, architecture, frontend, backend, API, data, LLM, quality, security, delivery, and Codex workflows |
| `docs/runtime/` | Codex runtime and automation choices |
| `docs/agent-systems/` | Multi-agent architecture, skills, memory, sessions, evals |
| `docs/playbooks/` | Repeatable operating procedures |
| `docs/artifact-templates/` | Copyable templates for project artifacts |
| `docs/sources/` | Official source registry and Context7 research log |
| `docs/insights/` | Community and experiment layer |

## Local Usage

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run checks:

```powershell
python tools/check_docs.py
```

Build HTML:

```powershell
python -m mkdocs build --strict
```

Serve locally:

```powershell
python -m mkdocs serve
```

## Source Policy

Official OpenAI pages are treated as source of truth. Community tricks and user reports live under `docs/insights/` with explicit trust and verification status.

## Operating Model

Use this repository as a living operating manual:

1. Add official sources to `docs/sources/registry.md`.
2. Convert stable methods into playbooks.
3. Promote repeated playbooks into skills.
4. Promote reliable skills into plugins when they need distribution, bundled integrations, MCP, or multiple skills.
5. Promote stable plugin workflows into automations only after manual verification is reliable.
6. Track long-running work with `RUNLOG.md` and eval thresholds.
7. Keep durable project rules in `AGENTS.md`, not in ad hoc prompts.
