# Реестр источников

Этот реестр фиксирует источники, на которых основана v1 базы знаний. Поле `checked_at` означает дату ручной сверки.

## Официальные источники

```yaml
title: "Codex web / cloud"
url: "https://developers.openai.com/codex/cloud"
type: "documentation"
status: "official"
checked_at: "2026-05-14"
summary: "Codex cloud delegates coding tasks to OpenAI-managed background environments and can work in parallel."
relevance: "Cloud tasks, environments, internet access, GitHub-linked work."
trust_level: "high"
```

```yaml
title: "Codex app"
url: "https://developers.openai.com/codex/app"
type: "documentation"
status: "official"
checked_at: "2026-05-14"
summary: "Desktop command center for parallel Codex threads, worktrees, automations, Git functionality, artifacts, browser and skills."
relevance: "Primary local orchestration surface for advanced users."
trust_level: "high"
```

```yaml
title: "Codex CLI"
url: "https://developers.openai.com/codex/cli"
type: "documentation"
status: "official"
checked_at: "2026-05-14"
summary: "Local terminal coding agent that can read, edit, and run code in the selected directory."
relevance: "Terminal workflows, transcripted sessions, local automation."
trust_level: "high"
```

```yaml
title: "Codex IDE extension"
url: "https://developers.openai.com/codex/ide"
type: "documentation"
status: "official"
checked_at: "2026-05-14"
summary: "IDE-side Codex surface for editor context, model switching, reasoning effort, approvals, cloud delegation, and follow-up work."
relevance: "Codebase navigation and scoped implementation from editor context."
trust_level: "high"
```

```yaml
title: "Codex use cases"
url: "https://developers.openai.com/codex/use-cases"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Catalog of Codex workflows across engineering, evaluation, front-end, QA, automation, integrations, data, and knowledge work."
relevance: "Backlog of playbook candidates and project-agent workflow patterns."
trust_level: "high"
```

```yaml
title: "Codex models"
url: "https://developers.openai.com/codex/models"
type: "documentation"
status: "official"
checked_at: "2026-05-14"
summary: "Codex model guidance covering recommended models, local model configuration, temporary CLI model choice, and cloud-task model limitations."
relevance: "Model policy for Codex App, CLI, IDE, subagents, and project agent profiles."
trust_level: "high"
```

```yaml
title: "OpenAI API models"
url: "https://developers.openai.com/api/docs/models"
type: "documentation"
status: "official"
checked_at: "2026-05-14"
summary: "Current model catalog and general model-selection guidance, including GPT-5.5, GPT-5.4, GPT-5.4 mini, and supported reasoning levels."
relevance: "Project defaults and model/reasoning matrix."
trust_level: "high"
```

```yaml
title: "Agents SDK models and providers"
url: "https://developers.openai.com/api/docs/guides/agents/models"
type: "documentation"
status: "official"
checked_at: "2026-05-15"
summary: "Guidance for explicit model selection in SDK-based agent runs, including per-agent models, run-level defaults, and process-wide fallback."
relevance: "Background source for the rejected standalone runner path; Codex-only Track 5 does not implement an SDK app."
trust_level: "high"
```

```yaml
title: "Reasoning best practices"
url: "https://developers.openai.com/api/docs/guides/reasoning-best-practices"
type: "documentation"
status: "official"
checked_at: "2026-05-14"
summary: "Guidance on when to use reasoning models, planner/doer decomposition, complex code review, debugging, evaluation, and prompt style."
relevance: "Reasoning effort escalation and role-specific agent profiles."
trust_level: "high"
```

```yaml
title: "Agent Skills"
url: "https://developers.openai.com/codex/skills"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Skills package task-specific instructions, resources and optional scripts, use progressive disclosure, and are the authoring format for reusable Codex workflows."
relevance: "Workflow-to-skill lifecycle, trigger design, verification, failure modes and future project-specific skill creation."
trust_level: "high"
```

```yaml
title: "Codex build plugins"
url: "https://developers.openai.com/codex/plugins/build"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Codex plugins are packaged with a required .codex-plugin/plugin.json and optional bundled skills, MCP server config, apps, hooks, assets, marketplace wiring, and install-surface metadata."
relevance: "Product-Agent OS plugin packaging, manifest paths, assets, and lifecycle config boundaries."
trust_level: "high"
```

```yaml
title: "Codex MCP"
url: "https://developers.openai.com/codex/mcp"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Codex supports MCP servers through config.toml, including stdio and streamable HTTP servers, project-scoped trusted configuration, environment variables, authentication and server management commands."
relevance: "External tool/context boundary, Product-Agent OS bundled MCP configuration, Context7 integration and MCP permission review."
trust_level: "high"
```

```yaml
title: "Context7 MCP clients"
url: "https://context7.com/docs/resources/all-clients"
type: "documentation"
status: "official"
checked_at: "2026-05-15"
summary: "Context7 documents MCP client setup for Codex, including the local stdio command npx -y @upstash/context7-mcp and optional API-key configuration outside checked-in plugin packages."
relevance: "Product-Agent OS bundled Context7 MCP server configuration."
trust_level: "high"
```

```yaml
title: "Codex hooks"
url: "https://developers.openai.com/codex/hooks"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Codex hooks run deterministic lifecycle scripts, support events such as SessionStart, PreToolUse, PermissionRequest, PostToolUse, PreCompact, SubagentStart and Stop, and require trust review for non-managed command hooks."
relevance: "Hook template design, staged hook config, activation approval, event coverage, trust review and guardrail limitations."
trust_level: "high"
```

```yaml
title: "Subagents"
url: "https://developers.openai.com/codex/subagents"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Codex can spawn specialized agents in parallel when explicitly asked, collect their results, and apply inherited sandbox and approval controls from the parent workflow."
relevance: "Multi-agent workflow architecture, fresh-context handoffs, ownership boundaries and approval-aware parallelism."
trust_level: "high"
```

```yaml
title: "Subagent concepts"
url: "https://developers.openai.com/codex/concepts/subagents"
type: "documentation"
status: "official"
checked_at: "2026-05-14"
summary: "Conceptual tradeoffs: context pollution, context rot, read-heavy parallel work, write-heavy coordination risk."
relevance: "Design rules for agent role decomposition."
trust_level: "high"
```

```yaml
title: "Custom instructions with AGENTS.md"
url: "https://developers.openai.com/codex/guides/agents-md"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Codex reads layered AGENTS.md or AGENTS.override.md files from global and project scopes before work begins, with closer project guidance taking precedence."
relevance: "Durable instruction design, source-of-truth policy and nested project rule boundaries."
trust_level: "high"
```

```yaml
title: "Codex best practices"
url: "https://developers.openai.com/codex/learn/best-practices"
type: "guide"
status: "official"
checked_at: "2026-05-24"
summary: "Practical Codex guidance for goal/context/constraints/done prompts, planning difficult tasks, reusable AGENTS.md guidance, configuration, skills and automations."
relevance: "Task packet structure, planning discipline, AGENTS.md updates, model/reasoning routing, skill promotion and automation readiness."
trust_level: "high"
```

```yaml
title: "Codex customization"
url: "https://developers.openai.com/codex/concepts/customization"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Codex customization layers combine AGENTS.md, memories, skills, MCP and subagents, with skills and MCP working together for reusable workflows that use external tools."
relevance: "Agentic workflow layering, memory/source-of-truth separation, skill/MCP/subagent routing and plugin promotion order."
trust_level: "high"
```

```yaml
title: "Building an AI-native engineering team"
url: "https://developers.openai.com/codex/guides/build-ai-native-engineering-team"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Guide to how coding agents affect planning, design, build, test, review, deployment, and team ownership."
relevance: "Agent team roles, human ownership boundaries, and product delivery lifecycle."
trust_level: "high"
```

```yaml
title: "Codex workflows"
url: "https://developers.openai.com/codex/workflows"
type: "guide"
status: "official"
checked_at: "2026-05-24"
summary: "End-to-end workflow examples with use cases, prompts, context notes, constraints and verification expectations."
relevance: "Playbook structure, prompt packet fields and evidence-before-completion examples."
trust_level: "high"
```

```yaml
title: "Sandbox"
url: "https://developers.openai.com/codex/concepts/sandboxing"
type: "documentation"
status: "official"
checked_at: "2026-05-14"
summary: "Sandboxing defines what spawned commands can touch and when approvals are required."
relevance: "Security model for local and cloud agent work."
trust_level: "high"
```

```yaml
title: "Agent approvals and security"
url: "https://developers.openai.com/codex/agent-approvals-security"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Codex operational security guidance for sandboxing, approvals, network controls, risk levels and approval-aware agent work."
relevance: "Security model for Codex App, CLI, IDE extension, subagents, skills, MCP, external writes and approval-bound workflows."
trust_level: "high"
```

```yaml
title: "Codex memories"
url: "https://developers.openai.com/codex/memories"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Codex memories can carry useful context across threads, but required team guidance belongs in AGENTS.md or checked-in docs; generated memory files should be treated as local recall state and reviewed before sharing."
relevance: "Memory architecture, source-of-truth policy, privacy review and context retention boundaries."
trust_level: "high"
```

```yaml
title: "Agents SDK sessions"
url: "https://openai.github.io/openai-agents-js/guides/sessions/"
type: "documentation"
status: "official"
checked_at: "2026-05-14"
summary: "Sessions give Agents SDK applications persistent conversational memory via a common Session interface."
relevance: "Application memory layer."
trust_level: "high"
```

```yaml
title: "Agents SDK sandbox agent memory"
url: "https://openai.github.io/openai-agents-js/guides/sandbox-agents/memory/"
type: "documentation"
status: "official"
checked_at: "2026-05-14"
summary: "Sandbox agent memory distills lessons from prior runs into workspace files and is separate from conversational session memory."
relevance: "Long-term agent memory patterns."
trust_level: "high"
```

```yaml
title: "Codex changelog"
url: "https://developers.openai.com/codex/changelog"
type: "changelog"
status: "official"
checked_at: "2026-05-14"
summary: "Current release notes for Codex app, CLI, and general Codex capabilities."
relevance: "Maintenance loop and freshness checks."
trust_level: "high"
```

```yaml
title: "Codex create skill"
url: "https://developers.openai.com/codex/skills/create-skill"
type: "documentation"
status: "official"
checked_at: "2026-05-14"
summary: "Skill creation guidance including folder structure, SKILL.md, optional assets, scripts, and agents/openai.yaml metadata."
relevance: "Project-specific skill design, invocation policy, and MCP dependencies."
trust_level: "high"
```

```yaml
title: "Codex with Agents SDK"
url: "https://developers.openai.com/codex/guides/agents-sdk"
type: "guide"
status: "official"
checked_at: "2026-05-15"
summary: "Guide for using Codex as an execution backend through MCP inside an Agents SDK multi-agent workflow."
relevance: "Background source for external orchestration patterns; Codex-only Track 5 keeps execution inside Codex instead."
trust_level: "high"
```

```yaml
title: "OpenAI Agents SDK Python"
url: "https://github.com/openai/openai-agents-python"
type: "documentation"
status: "official"
checked_at: "2026-05-15"
summary: "Python SDK for agentic apps with agents, tools, handoffs, guardrails, sessions, tracing, and MCP integration."
relevance: "Background source for out-of-scope standalone agent app patterns."
trust_level: "high"
```

```yaml
title: "OpenAI Agents SDK agent definitions"
url: "https://openai.github.io/openai-agents-python/agents/"
type: "documentation"
status: "official"
checked_at: "2026-05-15"
summary: "Agent definition guidance for `Agent`, `Runner`, tools, MCP servers, guardrails, handoffs, output types, hooks, and model settings."
relevance: "Background source for the removed Agents SDK implementation path; retained for comparison only."
trust_level: "high"
```

```yaml
title: "OpenAI Agents SDK MCP"
url: "https://openai.github.io/openai-agents-python/mcp/"
type: "documentation"
status: "official"
checked_at: "2026-05-15"
summary: "MCP integration guidance for hosted, streamable HTTP, SSE, stdio transports, agent-level MCP config, approval policies, tool filtering, and tracing."
relevance: "Background source for the removed external MCP bridge; Codex-only Track 5 does not start MCP servers."
trust_level: "high"
```

```yaml
title: "OpenAI Agents SDK guardrails"
url: "https://openai.github.io/openai-agents-python/guardrails/"
type: "documentation"
status: "official"
checked_at: "2026-05-15"
summary: "Guardrail workflow boundaries for input, output, and tool guardrails, including tripwires and limitations around handoffs and hosted or built-in tools."
relevance: "Background source for validator design; Codex-only Track 5 implements deterministic local guards."
trust_level: "high"
```

```yaml
title: "OpenAI Agents SDK Python sessions"
url: "https://openai.github.io/openai-agents-python/sessions/"
type: "documentation"
status: "official"
checked_at: "2026-05-15"
summary: "Python Agents SDK session memory guidance, built-in session implementations, persistence patterns, and constraints around response continuation mechanisms."
relevance: "Background source for memory separation; Codex-only Track 5 does not add SDK sessions."
trust_level: "high"
```

```yaml
title: "OpenAI Agents SDK tracing"
url: "https://openai.github.io/openai-agents-python/tracing/"
type: "documentation"
status: "official"
checked_at: "2026-05-15"
summary: "Tracing guidance for agent runs, generations, tools, handoffs, guardrails, custom spans, trace processors, and sensitive data capture controls."
relevance: "Background source for evidence/redaction risks; Codex-only Track 5 does not persist SDK traces."
trust_level: "high"
```

```yaml
title: "OpenAI API Responses guide"
url: "https://developers.openai.com/api/docs/guides/migrate-to-responses"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Responses API guide describing unified agent-like application interface, tools, structured outputs, multimodal input, and multi-turn state."
relevance: "Low-level API layer for programmable tools and structured agent contracts."
trust_level: "high"
```

```yaml
title: "OpenAI API structured outputs"
url: "https://developers.openai.com/api/docs/guides/structured-outputs"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Structured output guidance for constraining model responses to JSON Schema contracts."
relevance: "Handoff payloads, verifier outputs, source cards, and machine-checkable agent results."
trust_level: "high"
```

```yaml
title: "OpenAI API prompting"
url: "https://developers.openai.com/api/docs/guides/prompting"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Prompting guide covering prompt objects, versioning, variables, eval-linked prompt iteration, and prompt refinement practices."
relevance: "Prompt governance, reusable prompt templates, version control, and eval-driven iteration."
trust_level: "high"
```

```yaml
title: "OpenAI API prompt engineering"
url: "https://developers.openai.com/api/docs/guides/prompt-engineering"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Prompt engineering guidance for clear instructions, examples, structured context, message roles, and reliability strategies."
relevance: "Question design, task packets, few-shot examples, and anti-hallucination prompts."
trust_level: "high"
```

```yaml
title: "OpenAI API model optimization"
url: "https://developers.openai.com/api/docs/guides/model-optimization"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Model optimization workflow using evals, prompt engineering, representative tests, and iterative improvement."
relevance: "Prompt eval loops, hallucination reduction, and reliability measurement."
trust_level: "high"
```

```yaml
title: "OpenAI API text generation"
url: "https://developers.openai.com/api/docs/guides/text"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Text generation guide for Responses API text outputs, prompt inputs, model behavior, structured content, and production text-generation patterns."
relevance: "LLM behavior specs, prompt contracts, response generation and app-backed eval scope."
trust_level: "high"
```

```yaml
title: "OpenAI API function calling"
url: "https://developers.openai.com/api/docs/guides/function-calling"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Function calling guide for defining tools, receiving tool calls, executing application code, returning tool outputs and continuing the response."
relevance: "Tool contracts, tool-call evals, side-effect review and approval boundaries."
trust_level: "high"
```

```yaml
title: "OpenAI API tools guide"
url: "https://developers.openai.com/api/docs/guides/tools"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "OpenAI tools guide covering built-in and hosted tools that models can call during Responses API workflows."
relevance: "Tool selection policy, hosted tool usage, permissions, approval boundaries and runtime evidence."
trust_level: "high"
```

```yaml
title: "OpenAI API file search"
url: "https://developers.openai.com/api/docs/guides/tools-file-search"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "File search guide for vector stores, semantic and keyword search over uploaded files, retrieval options and result tradeoffs."
relevance: "Hosted RAG source inventory, retrieval config, grounding and corpus governance."
trust_level: "high"
```

```yaml
title: "OpenAI API retrieval"
url: "https://developers.openai.com/api/docs/guides/retrieval"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Retrieval guide for grounding model answers in external information using file search, vector stores and search/retrieval workflow patterns."
relevance: "RAG source-grounding, citation behavior, source freshness and unsupported-claim handling."
trust_level: "high"
```

```yaml
title: "OpenAI API embeddings"
url: "https://developers.openai.com/api/docs/guides/embeddings"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Embeddings guide for measuring relatedness of text strings and supporting search, clustering, recommendations, anomaly detection and classification."
relevance: "RAG retrieval design, vector search, semantic similarity and embedding model decisions."
trust_level: "high"
```

```yaml
title: "OpenAI API evaluation best practices"
url: "https://developers.openai.com/api/docs/guides/evaluation-best-practices"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Evaluation guidance for building datasets, graders, thresholds and regression loops for AI applications and agent workflows."
relevance: "Baseline eval requirements, rerun commands, thresholds, failure analysis and evidence-before-completion gates."
trust_level: "high"
```

```yaml
title: "OpenAI Agents SDK guide"
url: "https://developers.openai.com/api/docs/guides/agents"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Agents guide for building agentic applications with tools, state, collaboration, guardrails, handoffs, tracing and evaluation."
relevance: "Agent workflow maps, handoff ownership, state policy, tool execution and trace evidence."
trust_level: "high"
```

```yaml
title: "OpenAI Agents SDK guardrails and human review"
url: "https://developers.openai.com/api/docs/guides/agents/guardrails-approvals"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Guidance for input, output and tool guardrails plus human review for sensitive or side-effecting actions."
relevance: "Safety boundaries, human approval points, tool side effects and risk review gates."
trust_level: "high"
```

```yaml
title: "OpenAI Agents SDK integrations and observability"
url: "https://developers.openai.com/api/docs/guides/agents/integrations-observability"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Agents observability guidance covering trace inspection, model/tool/handoff spans, troubleshooting and higher-signal eval examples."
relevance: "Trace evidence packets, debugging, redaction planning and eval dataset extraction from runtime traces."
trust_level: "high"
```

```yaml
title: "OpenAI evaluate agent workflows"
url: "https://developers.openai.com/api/docs/guides/agent-evals"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Guidance for evaluating agent workflows across instruction following, functional correctness, tool selection, tool arguments and trace-derived datasets."
relevance: "Agent eval gates, tool-call accuracy, workflow correctness and regression thresholds."
trust_level: "high"
```

```yaml
title: "OpenAI Agents SDK orchestration and handoffs"
url: "https://developers.openai.com/api/docs/guides/agents/orchestration"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Agent orchestration and handoff guidance for manager patterns, specialist routing and final-answer ownership."
relevance: "Agent workflow design, handoff contracts, specialist routing and stop conditions."
trust_level: "high"
```

```yaml
title: "OpenAI API data controls"
url: "https://developers.openai.com/api/docs/guides/your-data"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "OpenAI API data controls guidance for data handling, storage, retention, model training, privacy controls and enterprise data governance options."
relevance: "OpenAI API privacy boundaries, AI/RAG data classification, no-private-data fixtures and customer-data review."
trust_level: "high"
```

```yaml
title: "OpenAI API safety best practices"
url: "https://developers.openai.com/api/docs/guides/safety-best-practices"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "OpenAI safety guidance covering moderation, human oversight, adversarial testing and safeguards for model applications."
relevance: "Safety review, red-team cases, refusal/fallback behavior and policy guardrail design."
trust_level: "high"
```

```yaml
title: "OpenAI API production best practices"
url: "https://developers.openai.com/api/docs/guides/production-best-practices"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "OpenAI production guidance for monitoring, rate limits, cost, latency, prompt caching, batching and reliability considerations."
relevance: "AI cost/latency budgets, production runtime checks, fallback planning and operational monitoring."
trust_level: "high"
```

```yaml
title: "Promptfoo"
url: "https://www.promptfoo.dev/docs/intro/"
type: "documentation"
status: "vendor documentation"
checked_at: "2026-05-24"
summary: "Promptfoo is an open-source CLI and library, now part of OpenAI, for evaluating and red-teaming LLM applications with declarative tests and assertions."
relevance: "AI eval runner, CI checks, red-team cases, RAG metrics and cost/latency assertions."
trust_level: "medium"
```

```yaml
title: "Promptfoo assertions and metrics"
url: "https://www.promptfoo.dev/docs/configuration/expected-outputs/"
type: "documentation"
status: "vendor documentation"
checked_at: "2026-05-24"
summary: "Promptfoo expected-output docs cover assertions and metrics for exact/semantic matches, LLM-as-judge, RAG retrieval, latency and cost checks."
relevance: "Declarative eval thresholds, regression assertions, cost/latency gates and RAG test design."
trust_level: "medium"
```

```yaml
title: "Ragas metrics"
url: "https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/"
type: "documentation"
status: "vendor documentation"
checked_at: "2026-05-24"
summary: "Ragas documents RAG and agent evaluation metrics including faithfulness, answer relevancy, context precision/recall, response groundedness, tool call accuracy and agent goal accuracy."
relevance: "Optional RAG quality metrics and failure analysis for retrieval-grounded answers."
trust_level: "medium"
```

```yaml
title: "OpenTelemetry GenAI semantic conventions"
url: "https://opentelemetry.io/docs/specs/semconv/gen-ai/"
type: "standard"
status: "official experimental"
checked_at: "2026-05-24"
summary: "OpenTelemetry GenAI semantic conventions define experimental spans, events and metrics for generative AI models, agents, tools and operations."
relevance: "AI observability, trace evidence, span naming and redaction-aware telemetry planning."
trust_level: "medium"
```

```yaml
title: "OpenAI Cookbook hallucination guardrails"
url: "https://github.com/openai/openai-cookbook"
type: "guide"
status: "official"
checked_at: "2026-05-24"
summary: "Cookbook examples for hallucination guardrails, LLM-as-judge validation, RAG grounding, citations, and structured answer generation."
relevance: "Verifier prompts, hallucination scoring, grounded answering playbook."
trust_level: "high"
```

```yaml
title: "How OpenAI uses Codex"
url: "https://openai.com/business/guides-and-resources/how-openai-uses-codex/"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "OpenAI teams use Codex for code understanding, refactors, migrations, performance, test coverage, velocity, flow, and exploration."
relevance: "Product-agent workflow design and practical Codex operating habits."
trust_level: "high"
```

```yaml
title: "A practical guide to building agents"
url: "https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Agent design guide covering when to build agents, models, tools, instructions, orchestration, guardrails, and human intervention."
relevance: "Production-grade agent roles, tools, guardrails, orchestration, and product-agent team design."
trust_level: "high"
```

```yaml
title: "AGENTS.md open format"
url: "https://agents.md/"
type: "documentation"
status: "community"
checked_at: "2026-05-14"
summary: "Open format for agent-focused repository instructions, including setup commands, tests, style, security, and nested instructions."
relevance: "Cross-agent operating manual patterns and examples."
trust_level: "medium"
```

```yaml
title: "Codex CLI features"
url: "https://developers.openai.com/codex/cli/features"
type: "documentation"
status: "official"
checked_at: "2026-05-14"
summary: "Codex CLI workflows including interactive mode, resume, non-interactive automation, remote app server, and session controls."
relevance: "Runtime selection, codex exec, resumable sessions, and app-server operations."
trust_level: "high"
```

```yaml
title: "Codex automations"
url: "https://developers.openai.com/codex/app/automations"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Codex app automations run recurring prompts on a schedule, can use skills/plugins, inherit sandbox settings, and should be manually tested and reviewed before stable scheduling."
relevance: "Recurring maintenance, release notes, bug scans, docs audits, skill-to-automation lifecycle and automation approval boundaries."
trust_level: "high"
```

```yaml
title: "Codex iterate on difficult problems"
url: "https://developers.openai.com/codex/use-cases/iterate-on-difficult-problems"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Use Codex as an eval-driven improvement loop with deterministic checks, LLM-as-judge, artifacts, logs, and explicit stopping rules."
relevance: "Long-horizon product-quality improvement loops and RUNLOG discipline."
trust_level: "high"
```

```yaml
title: "Codex add evals to your AI application"
url: "https://developers.openai.com/codex/use-cases/ai-app-evals"
type: "guide"
status: "official"
checked_at: "2026-05-24"
summary: "Use Codex to inspect an AI app and add a runnable eval suite before model, prompt, retrieval, or agent changes merge."
relevance: "Regression tests for model and reasoning policy changes."
trust_level: "high"
```

```yaml
title: "OpenAI Codex: Building an AI-Native Engineering Team"
url: "https://developers.openai.com/codex/guides/build-ai-native-engineering-team"
type: "guide"
status: "official"
checked_at: "2026-05-24"
summary: "OpenAI guidance on using coding agents across design, build, review and maintenance while humans retain ownership of product behavior, architecture, quality and long-term tradeoffs."
relevance: "Business/product methodology, AI-native team operating model, product behavior clarity and workflow promotion."
trust_level: "high"
```

```yaml
title: "Codex code review for GitHub pull requests"
url: "https://developers.openai.com/codex/use-cases/github-code-reviews"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Use Codex review to surface regressions, missing tests, documentation issues, and risky changes on pull requests."
relevance: "Reviewer role, AGENTS.md review guidance, and PR gates."
trust_level: "high"
```

```yaml
title: "Codex create a CLI Codex can use"
url: "https://developers.openai.com/codex/use-cases/agent-friendly-clis"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Create a composable CLI for repeated service, export, log, or repo-script work, then pair it with a companion skill."
relevance: "Tooling layer for product agents and skills."
trust_level: "high"
```

```yaml
title: "Codex keep documentation up-to-date"
url: "https://developers.openai.com/codex/use-cases/update-documentation"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Use Codex to compare code changes, docs, release notes, and PR context, then draft scoped documentation updates with verification."
relevance: "Docs Maintainer role and documentation update playbooks."
trust_level: "high"
```

```yaml
title: "Codex run verified operations"
url: "https://developers.openai.com/codex/use-cases/verified-operations-workflows"
type: "guide"
status: "official"
checked_at: "2026-05-24"
summary: "Codex use case for repeatable operations with structured inputs, explicit approvals, bounded retries, logs, artifacts, and audit-ready output."
relevance: "Release Operator, verified operations, approval-bound external actions, bounded retries, and evidence packets."
trust_level: "high"
```

```yaml
title: "Codex save workflows as skills"
url: "https://developers.openai.com/codex/use-cases/reusable-codex-skills"
type: "guide"
status: "official"
checked_at: "2026-05-24"
summary: "Turn working Codex threads, review rules, commands, checklists, design conventions, or repo scripts into reusable skills."
relevance: "Workflow-to-skill lifecycle and product skill design."
trust_level: "high"
```

```yaml
title: "Codex set up a teammate"
url: "https://developers.openai.com/codex/use-cases/proactive-teammate"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Connect work tools, teach one thread what matters, then use automation to surface changed docs, buried asks, blocked handoffs, and decisions."
relevance: "Long-running teammate pattern, memory, integrations, and automation readiness."
trust_level: "high"
```

```yaml
title: "Codex use cases taxonomy and collections"
url: "https://developers.openai.com/codex/use-cases"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Use case index with filters for category, native platforms, workflows, teams, and task types, plus collections for production systems, collaboration, web, native, and games."
relevance: "Source taxonomy for converting official use cases into playbooks, skills, plugins, and automations."
trust_level: "high"
```

```yaml
title: "Codex build responsive front-end designs"
url: "https://developers.openai.com/codex/use-cases/frontend-designs"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Use screenshots and design briefs to implement responsive UI in an existing design system, then validate with Playwright."
relevance: "Visual QA loop and frontend skill/plugin design."
trust_level: "high"
```

```yaml
title: "Codex turn Figma designs into code"
url: "https://developers.openai.com/codex/use-cases/figma-designs-to-code"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Use structured Figma context, screenshots, existing design system components, and Playwright checks to implement polished UI."
relevance: "Design-to-code workflow, Figma skill dependency, and visual verification."
trust_level: "high"
```

```yaml
title: "Codex follow a goal"
url: "https://developers.openai.com/codex/use-cases/follow-goals"
type: "guide"
status: "official"
checked_at: "2026-05-24"
summary: "Use /goal for long-running Codex CLI work with a durable objective, verifiable stopping condition, checkpoints, and pause/resume/clear controls."
relevance: "Long-running product-agent loops, migrations, prototypes, games, and prompt optimization."
trust_level: "high"
```

```yaml
title: "Codex create browser-based games"
url: "https://developers.openai.com/codex/use-cases/browser-games"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Use PLAN.md, AGENTS.md, Playwright, image generation, logs, and Context7 docs to build and iterate on browser-based games."
relevance: "Long-running build loop, visual assets, runtime verification, and durable project instructions."
trust_level: "high"
```

```yaml
title: "Codex debug in iOS simulator"
url: "https://developers.openai.com/codex/use-cases/ios-simulator-bug-debugging"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Use XcodeBuildMCP and the iOS app plugin to discover schemes, launch Simulator, inspect UI, capture screenshots/logs/LLDB state, patch, and rerun."
relevance: "Native QA loop and evidence-first debugging pattern."
trust_level: "high"
```

```yaml
title: "Codex build for macOS"
url: "https://developers.openai.com/codex/use-cases/native-macos-apps"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Build macOS SwiftUI apps with shell-first build/run loops, explicit scenes, desktop-native UI, AppKit bridges, logs, and signing checks."
relevance: "Native desktop product workflow and platform-specific verification."
trust_level: "high"
```

```yaml
title: "Codex automate bug triage"
url: "https://developers.openai.com/codex/use-cases/automation-bug-triage"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Sweep alerts, issues, failed checks, logs, and chat reports into a P0-P3 bug list with evidence and recommended next actions before scheduling automation."
relevance: "Operations agent workflow, connector safety, and automation readiness."
trust_level: "high"
```

```yaml
title: "Codex bring your app to ChatGPT"
url: "https://developers.openai.com/codex/use-cases/chatgpt-apps"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Plan a narrow ChatGPT app outcome, define MCP tools, scaffold server/widget pieces, and verify in ChatGPT developer mode."
relevance: "MCP app planning and plugin/tool metadata design."
trust_level: "high"
```

```yaml
title: "Codex use your computer"
url: "https://developers.openai.com/codex/use-cases/use-your-computer-with-codex"
type: "guide"
status: "official"
checked_at: "2026-05-14"
summary: "Use Computer Use for Mac app GUI tasks across apps, windows, browser sessions, and local files when no dedicated plugin exists."
relevance: "GUI fallback, app access approval, and no-parallel-runs safety rule."
trust_level: "high"
```

```yaml
title: "Agile Alliance Test-Driven Development"
url: "https://agilealliance.org/glossary/tdd/"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "Defines TDD as an intertwined cycle of coding, unit testing, and design/refactoring where tests precede programming."
relevance: "Test-first gates in Product-Agent OS `TEST.md` and build-slice workflow."
trust_level: "high"
```

```yaml
title: "Martin Fowler: The Practical Test Pyramid"
url: "https://martinfowler.com/articles/practical-test-pyramid.html"
type: "methodology"
status: "expert reference"
checked_at: "2026-05-24"
summary: "Practical guidance on building a balanced automated test portfolio across unit, integration, contract, UI, end-to-end, acceptance and exploratory testing."
relevance: "Quality/testing methodology, test portfolio design, regression scope, contract testing and E2E/runtime evidence."
trust_level: "medium"
```

```yaml
title: "Kent C. Dodds: Testing Trophy"
url: "https://kentcdodds.com/blog/the-testing-trophy-and-testing-classification"
type: "methodology"
status: "expert reference"
checked_at: "2026-05-24"
summary: "Testing Trophy heuristic for JavaScript/frontend test classification, emphasizing static checks and integration tests while treating test taxonomy as context-dependent."
relevance: "Frontend-oriented test portfolio design and caution against rigid universal test-layer ratios."
trust_level: "medium"
```

```yaml
title: "ISTQB Certified Tester Foundation Level Syllabus v4.0.1"
url: "https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "ISTQB Foundation Level syllabus covering testing fundamentals, test levels/types, confirmation and regression testing, risk-based testing, test techniques and tool support."
relevance: "Risk-based test scope, confirmation/regression distinction, impact analysis, exploratory testing vocabulary and test automation governance."
trust_level: "high"
```

```yaml
title: "pytest documentation"
url: "https://docs.pytest.org/en/stable/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "pytest documentation for readable Python tests, assertion introspection, auto-discovery, fixtures, parametrization, CI pipelines and flaky test guidance."
relevance: "Python test runner guidance, fixture strategy, parametrized test design and command evidence for Product-Agent OS quality gates."
trust_level: "high"
```

```yaml
title: "pytest fixtures"
url: "https://docs.pytest.org/en/stable/how-to/fixtures.html"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "pytest fixture guidance for reusable setup/teardown, dependency injection into tests, fixture scopes and parametrized resources."
relevance: "Test data setup, isolation, reusable fixtures and integration-test setup documentation."
trust_level: "high"
```

```yaml
title: "pytest parametrizing tests"
url: "https://docs.pytest.org/en/stable/example/parametrize.html"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "pytest examples for parametrizing test functions and fixtures across multiple input/output cases."
relevance: "Behavior matrix tests, edge-case coverage, data-driven checks and reduced duplicate test code."
trust_level: "high"
```

```yaml
title: "Vitest features"
url: "https://vitest.dev/guide/features.html"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Vitest feature guide covering watch mode, CI run mode, projects, snapshots, mocking, DOM environments, browser mode, parallelism and coverage."
relevance: "JavaScript/TypeScript test runner guidance, fast feedback loops, browser/component test routing and CI evidence."
trust_level: "high"
```

```yaml
title: "Vitest coverage"
url: "https://vitest.dev/guide/coverage.html"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Vitest coverage guidance for V8 and Istanbul coverage providers, reports, thresholds and coverage configuration."
relevance: "Coverage policy, coverage command selection and JS/TS quality gate documentation."
trust_level: "high"
```

```yaml
title: "Jest snapshot testing"
url: "https://jestjs.io/docs/snapshot-testing"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Jest snapshot testing documentation for capturing rendered output and comparing future test runs against checked-in snapshots."
relevance: "Snapshot governance, visual/structural regression evidence and warning against unreviewed snapshot churn."
trust_level: "high"
```

```yaml
title: "Playwright retries"
url: "https://playwright.dev/docs/test-retries"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Playwright Test retry guidance, including retry configuration and passed/flaky/failed test classification."
relevance: "Flaky test policy, retry evidence, CI failure classification and browser test quality gates."
trust_level: "high"
```

```yaml
title: "Stryker mutation testing"
url: "https://stryker-mutator.io/docs/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Stryker documentation explaining mutation testing by introducing changes to source code and checking whether the test suite detects them."
relevance: "Mutation testing guidance for critical deterministic logic, weak assertion detection and test effectiveness evidence."
trust_level: "high"
```

```yaml
title: "Stryker mutation metrics"
url: "https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Stryker documentation for mutant states and mutation metrics, including mutation score based on detected mutants over covered code."
relevance: "Mutation test report fields, surviving mutant triage and quality gate limitations."
trust_level: "high"
```

```yaml
title: "Hypothesis documentation"
url: "https://hypothesis.readthedocs.io/en/latest/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Hypothesis documentation for Python property-based testing, generated examples, strategies and edge-case discovery."
relevance: "Property-based test specs for invariants, parsers, serializers, permissions, state transitions and edge-case discovery."
trust_level: "high"
```

```yaml
title: "Codecov about code coverage"
url: "https://docs.codecov.com/docs/about-code-coverage"
type: "documentation"
status: "vendor documentation"
checked_at: "2026-05-24"
summary: "Codecov documentation describing code coverage as a measurement of which lines of code are executed by a test suite."
relevance: "Coverage policy, coverage-report interpretation and caution that execution coverage is only one quality signal."
trust_level: "medium"
```

```yaml
title: "GitHub Actions GITHUB_TOKEN permissions"
url: "https://docs.github.com/en/actions/tutorials/authenticate-with-github_token"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "GitHub Actions guidance for using `GITHUB_TOKEN` in workflows and modifying default permissions for least-privilege automation."
relevance: "CI quality gate permission policy, staged CI proposals and external write approval boundaries."
trust_level: "high"
```

```yaml
title: "Feature-Sliced Design documentation"
url: "https://fsd.how/docs/"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "Frontend architecture methodology with layers, slices, segments, public API, and import dependency rules."
relevance: "Architecture boundary guidance for UI projects and LLM-assisted feature placement."
trust_level: "high"
```

```yaml
title: "C4 model"
url: "https://c4model.com/"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "Hierarchical software architecture abstractions and diagrams covering software systems, containers, components, code, and supporting dynamic/deployment views."
relevance: "Solution architecture views, architecture boundary documentation, context/container/component diagram guidance and Product-Agent OS architecture gates."
trust_level: "high"
```

```yaml
title: "arc42 template overview"
url: "https://arc42.org/overview"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "Pragmatic template for architecture communication, including goals, constraints, context, decisions, quality requirements, risks, and glossary."
relevance: "Architecture overview and ADR/documentation-system workflow structure."
trust_level: "high"
```

```yaml
title: "ISO/IEC/IEEE 42010:2022"
url: "https://www.iso.org/standard/74393.html"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "International standard specifying requirements for the structure and expression of architecture descriptions, including architecture description frameworks, languages, viewpoints and model kinds."
relevance: "Solution architecture artifact structure, stakeholder concern/viewpoint framing and architecture description conformance guidance."
trust_level: "high"
```

```yaml
title: "SEI Architecture Tradeoff Analysis Method"
url: "https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "Structured method for understanding tradeoffs in software-intensive system architectures and evaluating fitness against competing quality attributes."
relevance: "Architecture tradeoff records, quality attribute scenario guidance and high-impact decision review gates."
trust_level: "high"
```

```yaml
title: "OpenAPI Initiative"
url: "https://www.openapis.org/"
type: "specification"
status: "official"
checked_at: "2026-05-23"
summary: "OpenAPI Specifications provide a formal standard for describing HTTP APIs and enabling documentation, tests, generated clients, and design standards."
relevance: "API contract source-of-truth guidance in documentation-system workflow."
trust_level: "high"
```

```yaml
title: "OpenAPI Specification v3.2.0"
url: "https://spec.openapis.org/oas/v3.2.0.html"
type: "specification"
status: "official"
checked_at: "2026-05-24"
summary: "Latest published OpenAPI Specification checked on 2026-05-24, defining a programming language-agnostic interface description for HTTP APIs."
relevance: "Current API contract source-of-truth guidance for Product-Agent OS documentation and contract review templates."
trust_level: "high"
```

```yaml
title: "OpenAPI Specification v3.1.1"
url: "https://spec.openapis.org/oas/v3.1.1.html"
type: "specification"
status: "official"
checked_at: "2026-05-23"
summary: "OpenAPI 3.1.1 specification retained as a compatibility reference for existing tooling and security scheme definitions."
relevance: "Security scheme and API contract verification guidance for projects not yet on OpenAPI 3.2.0."
trust_level: "high"
```

```yaml
title: "AsyncAPI Specification v3.1.0"
url: "https://www.asyncapi.com/docs/reference/specification/v3.1.0"
type: "specification"
status: "official"
checked_at: "2026-05-24"
summary: "Machine-readable, protocol-agnostic specification for message-driven APIs."
relevance: "Event contract source-of-truth guidance in documentation-system workflow."
trust_level: "high"
```

```yaml
title: "RFC 9110: HTTP Semantics"
url: "https://www.rfc-editor.org/rfc/rfc9110.html"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "IETF standard defining HTTP semantics, including resources, methods, status codes, fields, representation metadata, content negotiation, and authentication semantics."
relevance: "HTTP API design, method semantics, status code use, caching-sensitive behavior, and API contract review."
trust_level: "high"
```

```yaml
title: "RFC 9457: Problem Details for HTTP APIs"
url: "https://www.rfc-editor.org/rfc/rfc9457.html"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "IETF standard defining machine-readable problem detail formats for HTTP API error responses and obsoleting RFC 7807."
relevance: "API error model documentation, examples, negative tests, and client compatibility guidance."
trust_level: "high"
```

```yaml
title: "RFC 9700: Best Current Practice for OAuth 2.0 Security"
url: "https://www.rfc-editor.org/rfc/rfc9700.html"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "IETF Best Current Practice for OAuth 2.0 security, updating RFCs 6749, 6750, and 6819 with newer threat and mitigation guidance."
relevance: "API auth, OAuth flows, token handling, scopes, and security-sensitive integration review."
trust_level: "high"
```

```yaml
title: "OWASP API Security Top 10 2023"
url: "https://owasp.org/API-Security/editions/2023/en/0x00-header/"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "OWASP API-specific risk catalog for 2023, including object-level authorization, authentication, property-level authorization, resource consumption, function-level authorization, SSRF, security misconfiguration, inventory management, and unsafe API consumption."
relevance: "API threat modeling, security review gates, negative test planning, and external integration risk checks."
trust_level: "high"
```

```yaml
title: "JSON Schema Specification"
url: "https://json-schema.org/specification"
type: "specification"
status: "official"
checked_at: "2026-05-24"
summary: "JSON Schema specification index; the current version and latest meta-schema checked on 2026-05-24 is 2020-12."
relevance: "Shared JSON payload contracts, schema dialect pinning, API validation, and structured artifact contracts."
trust_level: "high"
```

```yaml
title: "CloudEvents"
url: "https://cloudevents.io/"
type: "specification"
status: "official"
checked_at: "2026-05-24"
summary: "CNCF CloudEvents project providing a standardized event metadata format; CloudEvents reached CNCF Graduated status in 2024 and lists CloudEvents 1.0.2 as a released specification."
relevance: "Event metadata, cross-system event interoperability, webhook/event documentation, and async integration design."
trust_level: "high"
```

```yaml
title: "GraphQL Specification Versions"
url: "https://spec.graphql.org/"
type: "specification"
status: "official"
checked_at: "2026-05-24"
summary: "Official GraphQL specification version index; latest release checked on 2026-05-24 is September 2025, with a working draft dated April 2026."
relevance: "GraphQL schema contract governance, version pinning, deprecation policy, and API style selection."
trust_level: "high"
```

```yaml
title: "gRPC Introduction"
url: "https://grpc.io/docs/what-is-grpc/introduction/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "gRPC documentation introducing Protocol Buffers as the default IDL and message interchange format for service definitions and generated client/server code."
relevance: "RPC API contract selection, `.proto` source-of-truth guidance, generated client/server stubs, and polyglot service integration."
trust_level: "high"
```

```yaml
title: "Pact Documentation"
url: "https://docs.pact.io/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Pact documentation for consumer-driven contract testing and provider verification across HTTP and message integrations."
relevance: "Consumer-driven contract tests, provider verification, contract-by-example guidance, and microservice/API compatibility gates."
trust_level: "high"
```

```yaml
title: "OpenAPI Generator"
url: "https://openapi-generator.tech/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "OpenAPI Generator documentation for generating clients, server stubs, documentation, and other artifacts from OpenAPI documents."
relevance: "Generated SDK manifest, reproducible client generation, server stub evaluation, and API documentation tooling."
trust_level: "high"
```

```yaml
title: "Stoplight Open Source API Toolkit"
url: "https://stoplight.io/open-source"
type: "documentation"
status: "vendor documentation"
checked_at: "2026-05-24"
summary: "Stoplight documentation for open-source API tooling, including Prism for mocking, Spectral for JSON/YAML linting, and Elements for generated API documentation."
relevance: "Candidate API lint, mock, and documentation tooling for projects that choose a Stoplight-based API workflow."
trust_level: "medium"
```

```yaml
title: "Google API Improvement Proposals"
url: "https://google.aip.dev/"
type: "methodology"
status: "vendor methodology"
checked_at: "2026-05-24"
summary: "Google AIPs document Google's API design decisions and provide a framework for recording API design rules and practices."
relevance: "API style-guide governance, API design rule documentation, and large-project API consistency model."
trust_level: "medium"
```

```yaml
title: "Storybook Autodocs"
url: "https://storybook.js.org/docs/writing-docs/autodocs"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Storybook can generate component documentation from stories tagged with autodocs, extendable with MDX and Doc Blocks."
relevance: "UI component documentation and docs-as-code workflow."
trust_level: "high"
```

```yaml
title: "Storybook accessibility tests"
url: "https://storybook.js.org/docs/writing-tests/accessibility-testing"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Storybook accessibility addon supports accessibility checks in the UI and CI-oriented component test workflows."
relevance: "Frontend verification gates and UI documentation quality."
trust_level: "high"
```

```yaml
title: "Storybook interaction tests"
url: "https://storybook.js.org/docs/writing-tests/interaction-testing"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Storybook interaction tests use stories and play functions to simulate user behavior and assert resulting component behavior."
relevance: "Frontend component behavior verification, user-flow evidence, and Storybook-as-test-surface guidance."
trust_level: "high"
```

```yaml
title: "Storybook visual tests"
url: "https://storybook.js.org/docs/writing-tests/visual-testing"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Storybook visual tests compare story snapshots against known good baselines and can turn every story into a visual regression check."
relevance: "Frontend visual evidence, component state regression checks, and design-system verification."
trust_level: "high"
```

```yaml
title: "Playwright visual comparisons"
url: "https://playwright.dev/docs/test-snapshots"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Playwright Test supports screenshot generation and visual comparison through `toHaveScreenshot()`, with environment-stability requirements for reliable baselines."
relevance: "Browser visual evidence, responsive UI verification, and screenshot baseline guidance."
trust_level: "high"
```

```yaml
title: "Playwright Trace Viewer"
url: "https://playwright.dev/docs/trace-viewer"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Playwright Trace Viewer is a GUI for inspecting recorded test traces, screenshots, DOM snapshots and debugging evidence after test runs."
relevance: "Frontend runtime evidence, CI failure analysis, browser behavior documentation, and verification packets."
trust_level: "high"
```

```yaml
title: "Testing Library guiding principles"
url: "https://testing-library.com/docs/guiding-principles/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Testing Library encourages tests that resemble how users use web pages and avoids component-instance-oriented APIs."
relevance: "User-observable frontend tests, accessibility-oriented queries, and interaction test design."
trust_level: "high"
```

```yaml
title: "WAI-ARIA Authoring Practices Guide"
url: "https://www.w3.org/WAI/ARIA/apg/"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "WAI-ARIA APG documents accessible design patterns, ARIA roles/states/properties, keyboard support, accessible names and landmarks."
relevance: "Frontend accessibility patterns, keyboard/focus contracts, and custom widget review."
trust_level: "high"
```

```yaml
title: "MDN accessible HTML"
url: "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "MDN explains semantic HTML, native controls, labels, source order and keyboard accessibility as a foundation for accessible UI."
relevance: "Frontend semantic markup, keyboard behavior, form labels and accessibility review guidance."
trust_level: "high"
```

```yaml
title: "MDN using media queries"
url: "https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Media_queries/Using"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "MDN documents CSS media queries for applying styles based on media type, viewport, orientation, input characteristics and user preferences."
relevance: "Responsive UI documentation, viewport matrix planning, and adaptive behavior checks."
trust_level: "high"
```

```yaml
title: "web.dev Web Vitals"
url: "https://web.dev/articles/vitals"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "web.dev documents Core Web Vitals as LCP, INP and CLS, covering loading performance, interactivity and visual stability."
relevance: "Frontend performance budgets, route verification, and user-facing performance evidence."
trust_level: "high"
```

```yaml
title: "web.dev Interaction to Next Paint"
url: "https://web.dev/articles/inp"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "web.dev defines INP as a metric assessing page responsiveness to click, tap and keyboard interactions throughout a user's visit."
relevance: "Interaction-heavy frontend performance risk, responsiveness budgets, and Core Web Vitals guidance."
trust_level: "high"
```

```yaml
title: "GitLab documentation site architecture"
url: "https://docs.gitlab.com/development/documentation/site_architecture/"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "GitLab documentation source files are stored in the same repositories as product code and flow through documentation merge requests."
relevance: "Docs-as-code source-of-truth guidance."
trust_level: "high"
```

```yaml
title: "GitHub Actions workflows"
url: "https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "GitHub Actions workflows are YAML-defined automated processes checked into `.github/workflows` and triggered by repository events, manual dispatch, or schedule."
relevance: "CI/CD workflow governance, docs validation proposals, release automation boundary and approval-aware operations."
trust_level: "high"
```

```yaml
title: "GitHub Actions deployments and environments"
url: "https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "GitHub deployment environments can require reviewers, wait timers, deployment branch/tag restrictions, custom protection rules, and environment-scoped secrets."
relevance: "Release approval gates, production environment controls, secret boundaries, deployment protection and CI/CD release policy."
trust_level: "high"
```

```yaml
title: "GitHub Releases"
url: "https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "GitHub Releases bundle and deliver project iterations with tags, release notes, optional binary assets, draft releases, prerelease markers and generated release notes."
relevance: "Release packet, tag boundary, artifact upload approval, public release notes and package/plugin distribution workflow."
trust_level: "high"
```

```yaml
title: "GitHub protected branches"
url: "https://docs.github.com/articles/about-required-reviews-for-pull-requests"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "Protected branch rules can require reviews, code owner review, and status checks before changes reach protected branches."
relevance: "Review gates, CODEOWNERS, and CI quality policy proposals."
trust_level: "high"
```

```yaml
title: "MkDocs"
url: "https://www.mkdocs.org/"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "Static site generator for project documentation written in Markdown and configured with YAML."
relevance: "Default docs portal option for smaller projects."
trust_level: "high"
```

```yaml
title: "Sphinx autodoc"
url: "https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "Sphinx autodoc includes documentation from Python docstrings by importing modules and inspecting docstrings."
relevance: "Python code reference documentation guidance."
trust_level: "high"
```

```yaml
title: "Antora documentation"
url: "https://docs.antora.org/antora/latest/"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "Antora supports docs-as-code authoring in AsciiDoc and is suited to multi-repository documentation sites."
relevance: "Enterprise and multi-repository documentation portal option."
trust_level: "high"
```

```yaml
title: "Agile Alliance Acceptance Test-Driven Development"
url: "https://agilealliance.org/glossary/atdd/"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "ATDD frames acceptance tests before implementation through customer, development, and testing perspectives."
relevance: "Acceptance criteria traceability from REQUIREMENTS.md to TEST.md and eval gates."
trust_level: "high"
```

```yaml
title: "Agile Alliance Behavior-Driven Development"
url: "https://agilealliance.org/glossary/bdd/"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "BDD emphasizes executable behavior scenarios and shared understanding across business, testing, and development roles."
relevance: "Behavior scenario templates and agent handoff acceptance language."
trust_level: "high"
```

```yaml
title: "Martin Fowler: Bounded Context"
url: "https://martinfowler.com/bliki/BoundedContext.html"
type: "methodology"
status: "expert reference"
checked_at: "2026-05-24"
summary: "Bounded Context defines the boundary within which a domain model applies consistently."
relevance: "Domain modeling and architecture boundary guidance for Product-Agent OS."
trust_level: "medium"
```

```yaml
title: "Martin Fowler: Ubiquitous Language"
url: "https://martinfowler.com/bliki/UbiquitousLanguage.html"
type: "methodology"
status: "expert reference"
checked_at: "2026-05-24"
summary: "Ubiquitous Language connects domain experts and developers through a shared language embedded in code and model discussions."
relevance: "Domain glossary and domain modeling template guidance."
trust_level: "medium"
```

```yaml
title: "Domain Language"
url: "https://www.domainlanguage.com/"
type: "methodology"
status: "expert reference"
checked_at: "2026-05-24"
summary: "Domain Language is Eric Evans' site for Domain-Driven Design references, training, and resources."
relevance: "Primary background source for DDD terminology and deep-dive follow-up."
trust_level: "medium"
```

```yaml
title: "Agile Alliance User Stories"
url: "https://agilealliance.org/glossary/user-stories/"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "Agile Alliance guidance frames user stories around user goals and acceptance criteria that can support automated acceptance checks."
relevance: "Requirements-domain workflow guidance for backlog items, story slicing and acceptance criteria readiness."
trust_level: "high"
```

```yaml
title: "Cucumber Gherkin Reference"
url: "https://cucumber.io/docs/gherkin/reference/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Gherkin structures executable specifications with features, rules, scenarios, Given/When/Then steps, backgrounds, scenario outlines and examples."
relevance: "Acceptance scenario format guidance for BDD/ATDD-compatible requirements documentation."
trust_level: "high"
```

```yaml
title: "Cucumber Example Mapping"
url: "https://cucumber.io/docs/bdd/example-mapping/"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "Example Mapping clarifies a user story before development by separating story, rules, concrete examples and unresolved questions."
relevance: "Requirements discovery and acceptance criteria clarification before implementation planning."
trust_level: "high"
```

```yaml
title: "ISO/IEC/IEEE 29148:2018"
url: "https://www.iso.org/standard/72089.html"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "Requirements engineering standard for systems and software life-cycle processes, applicable across different project scopes, methodologies, sizes and complexities."
relevance: "Requirements engineering vocabulary, requirement quality and traceability guidance for large-project requirements-domain methodology."
trust_level: "high"
```

```yaml
title: "IEEE/ISO/IEC 29148-2018"
url: "https://standards.ieee.org/ieee/29148/6937/"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "IEEE public description of the requirements engineering standard covering processes, products, good requirement attributes and iterative requirements activities."
relevance: "Cross-check for requirements engineering claims used in the requirements-domain research dossier."
trust_level: "high"
```

```yaml
title: "IIBA BABOK"
url: "https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "BABOK is IIBA's globally recognized business analysis standard covering knowledge, skills, deliverables and techniques for business analysis professionals."
relevance: "Business analysis and stakeholder/requirements elicitation framing for requirements-domain methodology."
trust_level: "high"
```

```yaml
title: "Martin Fowler: Domain-Driven Design"
url: "https://martinfowler.com/bliki/DomainDrivenDesign.html"
type: "methodology"
status: "expert reference"
checked_at: "2026-05-24"
summary: "Domain-Driven Design centers software development on a domain model with rich understanding of domain processes and rules, especially for complex domains."
relevance: "Conditional DDD gate and domain modeling guidance for complex Product-Agent OS projects."
trust_level: "medium"
```

```yaml
title: "EventStorming"
url: "https://www.eventstorming.com/"
type: "methodology"
status: "creator reference"
checked_at: "2026-05-24"
summary: "EventStorming is presented as a flexible workshop format for collaborative exploration of complex business domains and event-driven software behavior."
relevance: "Optional domain discovery method for complex workflows, events, hotspots and candidate boundaries."
trust_level: "medium"
```

```yaml
title: "Domain Storytelling Requirements"
url: "https://domainstorytelling.org/requirements"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "Domain Storytelling guidance connects domain stories with learning domain language, shared understanding and deriving requirements or backlog items."
relevance: "Optional requirements elicitation and domain-language discovery method for requirements-domain workflow."
trust_level: "medium"
```

```yaml
title: "Google HEART framework paper"
url: "https://research.google.com/pubs/pub36299.html?frame=0"
type: "research"
status: "official"
checked_at: "2026-05-24"
summary: "The HEART framework organizes user-centered metrics around happiness, engagement, adoption, retention and task success, with a Goals -> Signals -> Metrics process."
relevance: "Business/product methodology, product hypothesis, metric specification and user-centered measurement guidance."
trust_level: "high"
```

```yaml
title: "Amplitude North Star Hub"
url: "https://amplitude.com/north-star-hub"
type: "documentation"
status: "vendor methodology"
checked_at: "2026-05-24"
summary: "North Star guidance focuses product teams on a primary value metric connected to delivered customer value and supporting input metrics."
relevance: "Business/product methodology, product hypothesis, primary value metric and release measurement workflow design."
trust_level: "medium"
```

```yaml
title: "Amplitude taxonomy planning"
url: "https://amplitude.com/docs/data/data-planning-playbook"
type: "documentation"
status: "vendor documentation"
checked_at: "2026-05-24"
summary: "Amplitude guidance for planning product analytics events, properties, taxonomy, naming conventions, key metrics and instrumentation priorities."
relevance: "Tracking-plan artifact, analytics governance, event/property contract design and product measurement evidence."
trust_level: "medium"
```

```yaml
title: "Amplitude implementation team organization"
url: "https://amplitude.com/docs/get-started/implementation-team-organization"
type: "documentation"
status: "vendor documentation"
checked_at: "2026-05-24"
summary: "Amplitude implementation guidance defines Project Lead, Data Governor and Instrumentation Lead responsibilities for tracking plans, naming conventions, data quality and privacy policy alignment."
relevance: "Analytics ownership model, Data Governor role, metric instrumentation responsibility and privacy-aware product analytics."
trust_level: "medium"
```

```yaml
title: "Product Talk Opportunity Solution Trees"
url: "https://www.producttalk.org/opportunity-solution-trees/"
type: "methodology"
status: "expert reference"
checked_at: "2026-05-24"
summary: "Opportunity Solution Trees connect desired outcome, opportunity space, solution space and assumption tests while distinguishing product outcomes from feature traction metrics."
relevance: "Product discovery, opportunity-to-solution traceability, roadmap decisions and assumption-test artifacts."
trust_level: "medium"
```

```yaml
title: "The Lean Startup methodology"
url: "https://theleanstartup.com/principles"
type: "methodology"
status: "expert reference"
checked_at: "2026-05-24"
summary: "Lean Startup methodology frames new product development as experiments using MVPs, Build-Measure-Learn, actionable metrics and pivot/persevere decisions."
relevance: "MVP experiments, product hypothesis validation, learning thresholds and release measurement loops."
trust_level: "medium"
```

```yaml
title: "Strategyzer Value Proposition Canvas"
url: "https://www.strategyzer.com/library/the-value-proposition-canvas"
type: "methodology"
status: "vendor methodology"
checked_at: "2026-05-24"
summary: "Value Proposition Canvas maps customer jobs, pains and gains to offering components, pain relievers and gain creators based on customer evidence."
relevance: "Value proposition artifact, target-user evidence, product hypothesis and customer-value traceability."
trust_level: "medium"
```

```yaml
title: "MADR"
url: "https://adr.github.io/madr/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Markdown Architectural Decision Records provide a lightweight ADR template for documenting architecturally significant decisions and their rationale."
relevance: "ADR artifact template, architecture decision trigger policy, tradeoff records and rollback documentation."
trust_level: "high"
```

```yaml
title: "Structurizr DSL"
url: "https://docs.structurizr.com/dsl"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Structurizr DSL defines C4 software architecture models, views, styles, documentation, and ADRs as text."
relevance: "Optional architecture-as-code path for larger projects."
trust_level: "high"
```

```yaml
title: "Structurizr as code"
url: "https://docs.structurizr.com/as-code"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Structurizr documents architecture-as-code workflows using text-based workspace definitions and related tooling."
relevance: "Architecture documentation tooling decision matrix."
trust_level: "high"
```

```yaml
title: "Mermaid syntax reference"
url: "https://mermaid.js.org/intro/syntax-reference.html"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Mermaid provides text-based diagram syntax for flowcharts, sequence diagrams, class diagrams, state diagrams, ER diagrams, C4, architecture and related diagram types."
relevance: "Markdown-native diagram guidance, architecture-as-code lightweight path and docs build/render checks."
trust_level: "high"
```

```yaml
title: "Thoughtworks: Fitness function-driven development"
url: "https://www.thoughtworks.com/en-us/insights/articles/fitness-function-driven-development"
type: "methodology"
status: "expert reference"
checked_at: "2026-05-24"
summary: "Architecture fitness functions are objective tests or metrics that measure alignment with architectural goals and provide continuous feedback against architecture drift."
relevance: "Architecture fitness function gates for dependency rules, observability, security, cost, performance, documentation freshness and conformance checks."
trust_level: "medium"
```

```yaml
title: "AWS Well-Architected Framework"
url: "https://docs.aws.amazon.com/wellarchitected/latest/framework/definitions.html"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "AWS framework for evaluating architectures through operational excellence, security, reliability, performance efficiency, cost optimization and sustainability pillars."
relevance: "Cloud workload review heuristics, quality attribute tradeoff framing and production-readiness checklist input."
trust_level: "high"
```

```yaml
title: "Azure Well-Architected Framework"
url: "https://learn.microsoft.com/en-us/azure/well-architected/"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "Microsoft framework of quality-driven tenets, architectural decision points and review tools for Azure workloads across reliability, security, cost, operations and performance."
relevance: "Cloud workload architecture review, solution architect checklist input and quality pillar framing."
trust_level: "high"
```

```yaml
title: "PlantUML sequence diagram documentation"
url: "https://plantuml.com/sequence-diagram"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "PlantUML supports text-based sequence diagrams and a broader UML-oriented diagram ecosystem."
relevance: "Optional UML-style documentation tooling for teams already using PlantUML."
trust_level: "high"
```

```yaml
title: "TypeDoc"
url: "https://typedoc.org/"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "TypeDoc generates documentation for TypeScript projects from source code and comments."
relevance: "TypeScript public API documentation guidance."
trust_level: "high"
```

```yaml
title: "JSDoc block and inline tags"
url: "https://jsdoc.app/about-block-inline-tags"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "JSDoc defines block and inline tags for JavaScript documentation comments."
relevance: "JavaScript code reference documentation guidance."
trust_level: "high"
```

```yaml
title: "Oracle Javadoc documentation comment specification"
url: "https://docs.oracle.com/en/java/javase/22/docs/specs/javadoc/doc-comment-spec.html"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "Javadoc defines documentation comment structure and tags for Java API documentation generation."
relevance: "Java public API documentation guidance."
trust_level: "high"
```

```yaml
title: "Microsoft C# XML documentation comments"
url: "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "C# XML documentation comments provide structured API documentation metadata for .NET code."
relevance: ".NET public API documentation guidance."
trust_level: "high"
```

```yaml
title: "DBML documentation"
url: "https://dbml.dbdiagram.io/docs/"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "DBML is a text language for defining database schemas, tables, relationships, indexes, enums, and notes."
relevance: "Database schema dictionary and relationship documentation option."
trust_level: "high"
```

```yaml
title: "dbdocs generate DBML from database"
url: "https://docs.dbdocs.io/features/generate-dbml-from-db/"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "dbdocs can generate DBML from database connections for supported database engines."
relevance: "Existing database documentation workflow option; requires careful secret handling."
trust_level: "high"
```

```yaml
title: "SchemaSpy documentation"
url: "https://schemaspy.readthedocs.io/en/v6.2.0/index.html"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "SchemaSpy analyzes relational database metadata and generates HTML schema documentation."
relevance: "Database documentation option for existing relational schemas."
trust_level: "high"
```

```yaml
title: "Docusaurus"
url: "https://docusaurus.io/docs"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "Docusaurus is a React-based static site generator for documentation sites with MDX, search, i18n, theming, and versioning support."
relevance: "Documentation portal option for React/MDX-heavy or public product docs."
trust_level: "high"
```

```yaml
title: "Docusaurus versioning"
url: "https://docusaurus.io/docs/versioning"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "Docusaurus docs versioning snapshots docs and sidebars into versioned directories and version metadata."
relevance: "Versioned documentation decision guidance and maintenance-cost warning."
trust_level: "high"
```

```yaml
title: "Read the Docs"
url: "https://docs.readthedocs.com/"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "Read the Docs builds, hosts, and versions documentation from version-controlled repositories."
relevance: "Hosted documentation workflow option for public and versioned docs."
trust_level: "high"
```

```yaml
title: "GitHub CODEOWNERS"
url: "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "CODEOWNERS files define repository ownership rules and can trigger automatic review requests."
relevance: "Governance signal and optional staged proposal for review ownership."
trust_level: "high"
```

```yaml
title: "GitHub workflow syntax"
url: "https://docs.github.com/actions/reference/workflows-and-actions/workflow-syntax"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "GitHub workflow syntax defines YAML structure for events, jobs, permissions, steps, environments, and reusable workflow features."
relevance: "Least-privilege CI proposal guidance for docs and product checks."
trust_level: "high"
```

```yaml
title: "Vale styles"
url: "https://vale.sh/docs/styles"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "Vale uses configurable styles to lint prose, spelling, terminology, and documentation quality rules."
relevance: "Optional documentation quality gate for Product-Agent OS proposals."
trust_level: "high"
```

```yaml
title: "markdownlint rules"
url: "https://github.com/markdownlint/markdownlint/blob/main/docs/RULES.md"
type: "documentation"
status: "official"
checked_at: "2026-05-23"
summary: "markdownlint provides a rule set for structural consistency in Markdown documents."
relevance: "Lightweight documentation linting option for docs-as-code checks."
trust_level: "high"
```

```yaml
title: "Keep a Changelog"
url: "https://keepachangelog.com/en/1.1.0/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Keep a Changelog defines a human-oriented changelog format with grouped change categories and an Unreleased section."
relevance: "Release packet and changelog guidance."
trust_level: "high"
```

```yaml
title: "Semantic Versioning 2.0.0"
url: "https://semver.org/"
type: "specification"
status: "official"
checked_at: "2026-05-24"
summary: "SemVer defines major, minor, and patch versioning rules around public API compatibility."
relevance: "Plugin, package, SDK, and public contract release policy."
trust_level: "high"
```

```yaml
title: "Conventional Commits 1.0.0"
url: "https://www.conventionalcommits.org/en/v1.0.0/"
type: "specification"
status: "official"
checked_at: "2026-05-24"
summary: "Conventional Commits defines a lightweight structured commit message convention that maps fixes, features and breaking changes to SemVer-oriented release automation."
relevance: "Optional release-note automation, changelog generation, semantic version bump decisions and commit hygiene policy."
trust_level: "high"
```

```yaml
title: "NIST Secure Software Development Framework SP 800-218"
url: "https://csrc.nist.gov/pubs/sp/800/218/final"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "NIST SSDF Version 1.1 recommends high-level secure software development practices that can be integrated into SDLC implementations."
relevance: "Security, privacy, secure SDLC, vulnerability response, and large-project governance gates."
trust_level: "high"
```

```yaml
title: "NIST Cybersecurity Framework 2.0"
url: "https://www.nist.gov/cyberframework"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "NIST CSF 2.0 provides cybersecurity risk management guidance organized around Govern, Identify, Protect, Detect, Respond and Recover functions."
relevance: "Security governance, risk strategy, policy expectations, incident response and security review vocabulary."
trust_level: "high"
```

```yaml
title: "OWASP SAMM"
url: "https://owaspsamm.org/model/"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "OWASP SAMM is a software assurance maturity model for analyzing and improving software security practices across governance, design, implementation, verification and operations."
relevance: "Secure SDLC maturity, security practice improvement and large-project security program planning."
trust_level: "high"
```

```yaml
title: "OWASP Application Security Verification Standard"
url: "https://owasp.org/www-project-application-security-verification-standard/"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "OWASP ASVS provides a basis for testing web application technical security controls and a versioned set of secure development requirements; stable 5.0.0 is listed by OWASP as of 2026-05-24."
relevance: "Security-sensitive workflow, web application verification requirements, and versioned security evidence."
trust_level: "high"
```

```yaml
title: "OWASP Top 10 Web Application Security Risks"
url: "https://owasp.org/www-project-top-ten/"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "OWASP Top 10 is an awareness document for critical web application security risks; OWASP lists Top 10 2025 as the current released version as of this research date."
relevance: "Security risk taxonomy, web app threat review, negative test planning and security-sensitive workflow triggers."
trust_level: "high"
```

```yaml
title: "OWASP API Security Top 10 2023"
url: "https://owasp.org/API-Security/editions/2023/en/0x00-header/"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "OWASP API Security Top 10 2023 documents API-specific security risks such as broken object-level authorization, broken authentication, broken function-level authorization, unrestricted resource consumption and unsafe API consumption."
relevance: "API security review, authz negative tests, rate-limit planning, webhook/integration risk review and contract evidence."
trust_level: "high"
```

```yaml
title: "OWASP Top 10 for LLM Applications 2025"
url: "https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "OWASP GenAI guidance documenting common LLM application risks such as prompt injection, sensitive information disclosure, supply chain issues, excessive agency and overreliance."
relevance: "AI/RAG/agent security review, prompt injection cases, tool-permission boundaries and red-team/eval planning."
trust_level: "high"
```

```yaml
title: "OWASP Secrets Management Cheat Sheet"
url: "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "OWASP guidance for managing secrets across creation, storage, access, rotation, auditing and incident response."
relevance: "Secrets inventory, no-secrets artifact policy, rotation planning and secret-handling readiness gates."
trust_level: "high"
```

```yaml
title: "OWASP Logging Cheat Sheet"
url: "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "OWASP logging guidance for security event logging, log content, exclusions, monitoring, protection and retention."
relevance: "Audit logging policy, sensitive-data redaction, security event taxonomy and incident investigation evidence."
trust_level: "high"
```

```yaml
title: "GitHub Actions secure use reference"
url: "https://docs.github.com/en/actions/reference/security/secure-use"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "GitHub Actions security guidance for secure workflow design, secrets handling, script injection risk, permissions, third-party actions and artifact exposure."
relevance: "CI permission review, staged workflow changes, external action policy and least-privilege automation."
trust_level: "high"
```

```yaml
title: "GitHub secret scanning"
url: "https://docs.github.com/en/code-security/concepts/secret-security/about-secret-scanning"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "GitHub secret scanning guidance for detecting leaked secrets, alerting maintainers and optionally blocking supported secrets before push."
relevance: "Secrets scanning policy, leaked-secret incident response and no-secret artifact gates."
trust_level: "high"
```

```yaml
title: "SLSA specification v1.1"
url: "https://slsa.dev/spec/v1.1/about"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "SLSA v1.1 describes supply chain security levels and provenance concepts for source, build, dependencies and package integrity."
relevance: "Supply chain review, build provenance, release integrity and package/plugin release gates."
trust_level: "high"
```

```yaml
title: "OpenSSF Scorecard"
url: "https://scorecard.dev/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "OpenSSF Scorecard evaluates repository security practices such as branch protection, dangerous workflows, dependency updates, pinned dependencies, token permissions, vulnerabilities and security policies."
relevance: "Repository supply-chain signals, CI security review, dependency/update governance and release readiness evidence."
trust_level: "high"
```

```yaml
title: "SPDX specifications"
url: "https://spdx.dev/use/specifications/"
type: "specification"
status: "official"
checked_at: "2026-05-24"
summary: "SPDX provides specifications for SBOM and software metadata exchange; SPDX 3.0 is listed as the current major specification by SPDX."
relevance: "SBOM format decision, license/dependency metadata and release package evidence."
trust_level: "high"
```

```yaml
title: "CycloneDX specification overview"
url: "https://cyclonedx.org/specification/overview/"
type: "specification"
status: "official"
checked_at: "2026-05-24"
summary: "CycloneDX is a full-stack BOM standard for component, service, dependency, vulnerability, formulation and metadata exchange; version 1.7 is listed as current by CycloneDX."
relevance: "SBOM manifest, dependency inventory, vulnerability metadata and supply-chain evidence."
trust_level: "high"
```

```yaml
title: "Web Content Accessibility Guidelines 2.2"
url: "https://www.w3.org/TR/WCAG22/"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "W3C Recommendation covering testable accessibility success criteria for making web content more accessible across devices and user needs."
relevance: "Frontend accessibility documentation and verification planning."
trust_level: "high"
```

```yaml
title: "DORA software delivery performance metrics"
url: "https://dora.dev/guides/dora-metrics/"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "DORA describes a current five-metric model for software delivery performance: change lead time, deployment frequency, failed deployment recovery time, change fail rate, and deployment rework rate."
relevance: "Delivery, release, operations, and post-release measurement guidance."
trust_level: "high"
```

```yaml
title: "Google SRE: Service Level Objectives"
url: "https://sre.google/sre-book/service-level-objectives/"
type: "guide"
status: "official"
checked_at: "2026-05-24"
summary: "Google SRE guidance on SLIs, SLOs, SLAs, and selecting a small number of indicators that represent what users care about."
relevance: "Reliability, operations, backend service health, and release readiness gates."
trust_level: "high"
```

```yaml
title: "Google SRE: Release Engineering"
url: "https://sre.google/sre-book/release-engineering/"
type: "guide"
status: "official"
checked_at: "2026-05-24"
summary: "Google SRE release engineering guidance describing reliable release processes, reproducible automated builds, intentional release process changes and release engineering collaboration with SRE."
relevance: "Release engineering methodology, reproducible build/release evidence, release ownership and operations readiness."
trust_level: "high"
```

```yaml
title: "Google SRE: Postmortem Culture"
url: "https://sre.google/sre-book/postmortem-culture/"
type: "guide"
status: "official"
checked_at: "2026-05-24"
summary: "Google SRE postmortem guidance for documenting incident impact, mitigation, root causes, follow-up actions and blameless review culture."
relevance: "Incident response, failed release learning, post-release review, postmortem templates and operational improvement loops."
trust_level: "high"
```

```yaml
title: "OpenTelemetry Documentation"
url: "https://opentelemetry.io/docs/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "OpenTelemetry is a vendor-neutral observability framework for instrumenting, generating, collecting, and exporting telemetry data such as traces, metrics, and logs."
relevance: "Backend observability, runtime evidence, service docs, and operations runbooks."
trust_level: "high"
```

```yaml
title: "The Twelve-Factor App"
url: "https://www.12factor.net/"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "Twelve-Factor is a methodology for building software-as-a-service apps with declarative setup, portability, dev/prod parity, continuous deployment, and scalable architecture practices."
relevance: "Backend, deployment, runtime configuration, and operations documentation."
trust_level: "high"
```

```yaml
title: "CNCF GitOps glossary"
url: "https://glossary.cncf.io/gitops/"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "CNCF glossary describes GitOps as practices for continuously evaluating and reconciling desired state from a source of truth against actual state, reducing drift and improving traceability."
relevance: "Declarative operations, desired-state release workflow, environment drift handling, rollback/revert and operations documentation."
trust_level: "high"
```

```yaml
title: "Argo Rollouts"
url: "https://argo-rollouts.readthedocs.io/en/latest/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Argo Rollouts is a Kubernetes controller for progressive delivery with blue-green, canary, weighted traffic shifting, analysis, manual judgement, automated promotion and rollback."
relevance: "Progressive delivery methodology, rollout strategy, canary/blue-green evidence, promotion/abort criteria and blast-radius control."
trust_level: "high"
```

```yaml
title: "OpenFeature"
url: "https://openfeature.dev/docs/reference/intro/"
type: "specification"
status: "official"
checked_at: "2026-05-24"
summary: "OpenFeature provides a vendor-agnostic feature flag API with evaluation context, providers, hooks and events."
relevance: "Feature flag lifecycle, staged rollout, kill-switch behavior, provider-neutral documentation and release controls."
trust_level: "high"
```

```yaml
title: "CNCF Cloud Native Definition"
url: "https://github.com/cncf/toc/blob/main/DEFINITION.md"
type: "methodology"
status: "official"
checked_at: "2026-05-24"
summary: "CNCF defines cloud-native practices as a way to develop, build, and deploy workloads at scale in a programmatic and repeatable manner, characterized by loosely coupled, secure, resilient, manageable, sustainable, and observable systems."
relevance: "Backend runtime architecture, cloud-native readiness, service coupling, automation, resilience, and observability guidance."
trust_level: "high"
```

```yaml
title: "Kubernetes liveness, readiness, and startup probes"
url: "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Kubernetes documentation for configuring liveness, readiness, and startup probes to manage container health and traffic readiness."
relevance: "Backend health-check contracts, production readiness, rollout safety, and runtime behavior documentation."
trust_level: "high"
```

```yaml
title: "Alistair Cockburn: Hexagonal Architecture"
url: "https://alistair.cockburn.us/hexagonal-architecture"
type: "methodology"
status: "expert reference"
checked_at: "2026-05-24"
summary: "Original Hexagonal Architecture / Ports and Adapters article describing an application core that can be driven through multiple ports and tested independently from UI, database, and runtime devices."
relevance: "Backend domain logic boundaries, adapter isolation, testability, and service/module architecture guidance."
trust_level: "medium"
```

```yaml
title: "Martin Fowler: Microservices Guide"
url: "https://martinfowler.com/microservices/"
type: "methodology"
status: "expert reference"
checked_at: "2026-05-24"
summary: "Microservices guide describing independently deployable services built around business capabilities, decentralized governance/data, infrastructure automation, design for failure, and evolutionary design."
relevance: "Conditional backend service decomposition, microservice readiness, service boundary review, and failure-design guidance."
trust_level: "medium"
```

```yaml
title: "Microsoft Azure Architecture Center: Retry pattern"
url: "https://learn.microsoft.com/en-us/azure/architecture/patterns/retry"
type: "documentation"
status: "vendor documentation"
checked_at: "2026-05-24"
summary: "Retry pattern guidance for handling transient failures, including retry after delay, exponential backoff, logging, idempotency, and when retries are inappropriate."
relevance: "Backend resilience docs, dependency failure matrix, retry/idempotency readiness gates, and integration testing guidance."
trust_level: "medium"
```

```yaml
title: "Microsoft Azure Architecture Center: Circuit Breaker pattern"
url: "https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker"
type: "documentation"
status: "vendor documentation"
checked_at: "2026-05-24"
summary: "Circuit Breaker pattern guidance for preventing repeated calls to operations that are likely to fail and allowing systems to recover."
relevance: "Backend dependency failure policy, resilience patterns, timeout/retry coordination, and operational runbook guidance."
trust_level: "medium"
```

```yaml
title: "Microsoft Azure Architecture Center: Queue-Based Load Leveling pattern"
url: "https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling"
type: "documentation"
status: "vendor documentation"
checked_at: "2026-05-24"
summary: "Queue-based load leveling guidance for buffering variable workloads between tasks and services to improve availability, scalability, and load control."
relevance: "Backend queue/worker contracts, backpressure, async job design, and overload protection guidance."
trust_level: "medium"
```

```yaml
title: "Microsoft Azure Architecture Center: Health Endpoint Monitoring pattern"
url: "https://learn.microsoft.com/en-us/azure/architecture/patterns/health-endpoint-monitoring"
type: "documentation"
status: "vendor documentation"
checked_at: "2026-05-24"
summary: "Health endpoint monitoring guidance for checking application status, dependent resources, response codes, response content, latency, DNS, TLS certificates, and external resources."
relevance: "Backend health-check contract, monitoring, production readiness, and runbook evidence."
trust_level: "medium"
```

```yaml
title: "Microsoft Azure Architecture Center: Saga pattern"
url: "https://learn.microsoft.com/en-us/azure/architecture/patterns/saga"
type: "documentation"
status: "vendor documentation"
checked_at: "2026-05-24"
summary: "Saga pattern guidance for coordinating distributed transactions through local transactions, events or orchestration, compensating actions, idempotency, and workflow monitoring."
relevance: "Backend distributed consistency, long-running workflows, compensation, idempotency, and recovery-plan documentation."
trust_level: "medium"
```

```yaml
title: "PostgreSQL Transaction Isolation"
url: "https://www.postgresql.org/docs/current/transaction-iso.html"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "PostgreSQL documentation for transaction isolation levels, concurrency phenomena, Read Committed, Repeatable Read, Serializable behavior and serialization failure retry considerations."
relevance: "Database transaction boundary, isolation, concurrency, retry and data consistency guidance."
trust_level: "high"
```

```yaml
title: "PostgreSQL Backup and Restore"
url: "https://www.postgresql.org/docs/current/backup.html"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "PostgreSQL backup and restore documentation covering SQL dump and file-system-level backup approaches."
relevance: "Backup/restore evidence, production migration readiness and rollback/recovery planning."
trust_level: "high"
```

```yaml
title: "PostgreSQL Constraints"
url: "https://www.postgresql.org/docs/current/ddl-constraints.html"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "PostgreSQL documentation for check, not-null, unique, primary key, foreign key and exclusion constraints."
relevance: "Database integrity design, schema documentation, data quality and migration review."
trust_level: "high"
```

```yaml
title: "PostgreSQL Indexes"
url: "https://www.postgresql.org/docs/current/indexes.html"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "PostgreSQL documentation for index usage, index types and query performance considerations."
relevance: "Database performance review, query/index documentation and migration lock/runtime planning."
trust_level: "high"
```

```yaml
title: "PostgreSQL EXPLAIN"
url: "https://www.postgresql.org/docs/current/sql-explain.html"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "PostgreSQL EXPLAIN documentation for displaying query execution plans, including ANALYZE, BUFFERS, WAL, MEMORY and output formats; ANALYZE executes the statement."
relevance: "Query-plan evidence, performance verification, index review and safe analysis procedure."
trust_level: "high"
```

```yaml
title: "Liquibase core concepts"
url: "https://www.liquibase.org/get-started/core-usage/liquibase-core-concepts-author-database-changes"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Liquibase documentation describing changelogs as ordered lists of changesets, supported formats, DATABASECHANGELOG tracking, preconditions, contexts and labels."
relevance: "Database migrations-as-code, changelog documentation, rollback planning and CI/CD database change governance."
trust_level: "high"
```

```yaml
title: "Liquibase rollback"
url: "https://docs.liquibase.com/commands/rollback/rollback.html"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Liquibase rollback command documentation for rolling back changes based on tags and user-defined rollback statements."
relevance: "Database rollback feasibility, migration planning and release recovery evidence."
trust_level: "high"
```

```yaml
title: "Redgate Flyway migrations"
url: "https://documentation.red-gate.com/flyway/flyway-concepts/migrations"
type: "documentation"
status: "vendor documentation"
checked_at: "2026-05-24"
summary: "Flyway documentation describing version-controlled migrations, versioned/repeatable/baseline/undo migrations, schema history, dry-run scripts, deployment reports and transaction handling."
relevance: "Database migration tooling, migration validation, dry-run artifacts and schema history guidance."
trust_level: "medium"
```

```yaml
title: "dbt data tests"
url: "https://docs.getdbt.com/docs/build/data-tests"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "dbt documentation describing data tests as SQL assertions that return failing rows and pass when zero failing rows are returned."
relevance: "Executable data quality gates, analytics model verification and data contract checks."
trust_level: "high"
```

```yaml
title: "dbt model contracts"
url: "https://docs.getdbt.com/docs/mesh/govern/model-contracts"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "dbt documentation for model contracts, including enforced column names and data types for supported SQL model materializations."
relevance: "Data contract documentation, analytics model compatibility and shared data product governance."
trust_level: "high"
```

```yaml
title: "Great Expectations Expectations overview"
url: "https://docs.greatexpectations.io/docs/cloud/expectations/expectations_overview/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "Great Expectations documentation defining Expectations as verifiable assertions about data, with completeness, schema, uniqueness, validity, volume, custom SQL and multi-source checks."
relevance: "Data quality gates, validation artifacts, migration comparison and data health reporting."
trust_level: "high"
```

```yaml
title: "OpenLineage documentation"
url: "https://openlineage.io/docs/"
type: "documentation"
status: "official"
checked_at: "2026-05-24"
summary: "OpenLineage documentation describing an open standard for lineage metadata collection using dataset, job and run entities with extensible facets."
relevance: "Data lineage, analytics/RAG traceability, dataset ownership and pipeline documentation."
trust_level: "high"
```

```yaml
title: "NIST Privacy Framework 1.1 usage guidance"
url: "https://www.nist.gov/privacy-framework/using-privacy-framework-11"
type: "guidance"
status: "official"
checked_at: "2026-05-24"
summary: "NIST guidance for using Privacy Framework 1.1 with profiles, accountability, privacy programs, SDLC alignment and data processing ecosystem roles."
relevance: "Data classification, privacy-by-design, retention/deletion policy, production data access and sensitive data governance."
trust_level: "high"
```

```yaml
title: "NIST Privacy Framework"
url: "https://www.nist.gov/privacy-framework/privacy-framework"
type: "standard"
status: "official"
checked_at: "2026-05-24"
summary: "NIST Privacy Framework provides a voluntary tool for improving privacy through enterprise risk management and privacy engineering practices."
relevance: "Privacy-by-design, data minimization, retention/deletion review, data processing ecosystem roles and privacy impact records."
trust_level: "high"
```

```yaml
title: "California Consumer Privacy Act"
url: "https://oag.ca.gov/privacy/ccpa"
type: "legal reference"
status: "official"
checked_at: "2026-05-24"
summary: "California Attorney General guidance for CCPA privacy rights and business obligations around personal information."
relevance: "Privacy/compliance overlay selection, data rights review and legal-owner routing for California personal information."
trust_level: "high"
```

```yaml
title: "GDPR Regulation 2016/679"
url: "https://eur-lex.europa.eu/eli/reg/2016/679/oj"
type: "legal reference"
status: "official"
checked_at: "2026-05-24"
summary: "Official EUR-Lex text of the EU General Data Protection Regulation for personal data processing obligations and data subject rights."
relevance: "Privacy/compliance overlay selection, legal-owner review and data processing evidence for EU personal data."
trust_level: "high"
```

```yaml
title: "Martin Fowler: Evolutionary Database Design"
url: "https://martinfowler.com/articles/evodb.html"
type: "methodology"
status: "expert reference"
checked_at: "2026-05-24"
summary: "Fowler and Sadalage article describing evolutionary database design, database refactoring, version-controlled migration scripts, CI/deployment pipelines, small database changes and transition phases."
relevance: "Database methodology, migration-first planning, expand/contract thinking and versioned schema/data change workflow."
trust_level: "medium"
```

```yaml
title: "Prisma Data Guide: expand and contract pattern"
url: "https://www.prisma.io/dataguide/types/relational/expand-and-contract-pattern"
type: "guide"
status: "vendor documentation"
checked_at: "2026-05-24"
summary: "Prisma Data Guide explains expand/contract schema changes as a multi-step process for adding new structures, updating clients, backfilling, switching reads/writes and removing old structures."
relevance: "Safe live database migration planning, destructive change compatibility and rollout/rollback documentation."
trust_level: "medium"
```

## Community and experiment intake

```yaml
title: "Product-Agent OS pre-Track 8 implemented plans and specs inventory"
url: "docs/sources/product-agent-os-pre-track-8-implementation-inventory.md; docs/product-agent/product-agent-os-plugin-spec.md; docs/superpowers/plans/2026-05-14-product-agent-os-plugin-core.md; docs/superpowers/plans/2026-05-14-product-agent-os-lifecycle-skills.md; docs/superpowers/plans/2026-05-14-product-agent-os-generated-infrastructure.md; docs/superpowers/plans/2026-05-14-product-agent-os-production-hardening.md; docs/superpowers/plans/2026-05-15-product-agent-os-codex-runtime-runner.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-05-27"
summary: "Internal inventory of Product-Agent OS plans, specs and implementation-history artifacts realized before Track 8, including Track 1 plugin core, Track 2 lifecycle skills, Track 3 generated infrastructure, Track 4 production hardening, Track 5 Codex runtime runner and Track 6/7 methodology standards evidence."
relevance: "Task 22 final documentation sync input queue for deep technical and product analysis before extending the Task 22 matrix."
trust_level: "high"
verification_status: "Backed by read-only checked-in file inventory and documentation structure checks in the Task 22 planning session."
```

```yaml
title: "Product-Agent OS Track 9 methodology intelligence design and backlog"
url: "docs/superpowers/specs/2026-05-25-track-9-methodology-intelligence-design.md; docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md; docs/sources/product-agent-os-track-9-backlog.md; docs/product-agent-os/methodology-intelligence.md; plugins/product-agent-os/scripts/product_agent_os/methodology_catalog.py; plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py; plugins/product-agent-os/scripts/run_methodology_audit.py"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-05-25"
summary: "Internal Track 9 design, implementation plan, backlog, operator docs and local audit tooling for Product-Agent OS methodology intelligence, including read-only methodology catalog, workspace audit, Delivery Map, prioritized recommendations, owner questions, staged artifact boundary, and domain integration through T9-D5 Codex / Agentic Workflow."
relevance: "Track 9 foundation, methodology audit docs, fixture eval expectations, read-only first guidance, implemented T9-D1 through T9-D5 methodology gates, and future domain integration queue."
trust_level: "high"
verification_status: "Backed by Track 9 focused unit tests, fixture eval integration, product docs contract tests, documentation structure checks, strict MkDocs build in the Track 9 foundation verification loop, and current T9-D5 focused/full verification evidence recorded in the Track 9 backlog."
```

```yaml
title: "Product-Agent OS Track 9 backend methodology coverage"
url: "docs/methodologies/backend.md; docs/sources/product-agent-os-track-9-backlog.md; docs/product-agent-os/behavioral-evals.md; docs/product-agent-os/scenarios.md; plugins/product-agent-os/scripts/product_agent_os/discovery.py; plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py; plugins/product-agent-os/scripts/run_fixture_eval.py"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-05-25"
summary: "Internal T9-D7 Backend methodology coverage for Product-Agent OS, including backend_contract_present, service boundary gates, runtime/failure/observability/security/rollback evidence, CI/deployment discovery signals, severity policy, framework-agnostic snippet policy, retry/idempotency detection limits and owner-reviewed evidence sufficiency routing."
relevance: "Track 9 Backend methodology implementation, Product-Agent OS backend behavioral eval coverage, source-backed operator docs, discovery packets and audit recommendation contracts."
trust_level: "high"
verification_status: "Backed by focused T9-D7 tests, fixture eval coverage, full Product-Agent OS unittest discovery, transcript eval, Codex compatibility validation, docs checks and git diff hygiene recorded in the Track 9 backlog."
```

```yaml
title: "Product-Agent OS Track 9 API & Integrations methodology coverage"
url: "docs/methodologies/api-integrations.md; docs/sources/product-agent-os-track-9-backlog.md; docs/product-agent-os/behavioral-evals.md; docs/product-agent-os/scenarios.md; plugins/product-agent-os/scripts/product_agent_os/discovery.py; plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py; plugins/product-agent-os/scripts/run_fixture_eval.py"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-05-25"
summary: "Internal T9-D8 API & Integrations methodology coverage for Product-Agent OS, including api_integrations_contract_present, contract source, consumer map, compatibility review, security schemes, error contract, event/webhook delivery, generated SDK manifest, API observability, external-write approval and unsupported API claim rejection."
relevance: "Track 9 API & Integrations methodology implementation, Product-Agent OS API behavioral eval coverage, source-backed operator docs, discovery packets and audit recommendation contracts."
trust_level: "high"
verification_status: "Backed by focused T9-D8 catalog, audit, discovery, template, lifecycle, docs and fixture tests, fixture eval coverage, full Product-Agent OS unittest discovery, transcript eval, Codex compatibility validation, docs checks and git diff hygiene recorded in the Track 9 backlog."
```

```yaml
title: "Product-Agent OS Track 9 Database & Data methodology coverage"
url: "docs/methodologies/database-data.md; docs/sources/product-agent-os-track-9-backlog.md; docs/product-agent-os/behavioral-evals.md; docs/product-agent-os/scenarios.md; plugins/product-agent-os/scripts/product_agent_os/discovery.py; plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py; plugins/product-agent-os/scripts/run_fixture_eval.py"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-05-26"
summary: "Internal T9-D9 Database & Data methodology coverage for Product-Agent OS, including database_data_contract_present, database_data_signals, inventory, dictionary, schema source, migration plan, expand-contract, data contract, rollback/backup, classification, data quality, lineage, query performance, retention/deletion, synthetic fixture policy, production access approval and unsupported database claim rejection."
relevance: "Track 9 Database & Data methodology implementation, Product-Agent OS database behavioral eval coverage, source-backed operator docs, discovery packets and audit recommendation contracts."
trust_level: "high"
verification_status: "Backed by focused T9-D9 catalog, audit, discovery, template, lifecycle, docs and fixture tests, fixture eval coverage, full Product-Agent OS unittest discovery, Codex compatibility validation, docs checks and git diff hygiene recorded in the Track 9 backlog."
```

```yaml
title: "Product-Agent OS Track 8 scenario, eval and transcript docs with discovery status"
url: "docs/product-agent-os/scenarios.md; docs/product-agent-os/behavioral-evals.md; docs/product-agent-os/codex-compatibility.md; plugins/product-agent-os/scripts/product_agent_os/discovery.py; plugins/product-agent-os/scripts/run_transcript_eval.py; plugins/product-agent-os/scripts/run_fixture_eval.py"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-05-24"
summary: "Internal T8-H/T8-GY/T8-D documentation and runner coverage for Product-Agent OS scenario routing, behavioral eval contracts, forbidden behaviors, fixture eval coverage, deterministic transcript/session replay, discovery methodology applicability packets and Codex-only compatibility boundaries."
relevance: "T8-H, T8-GY and T8-D closure, operator docs, source-backed scenario guidance, behavioral eval documentation, transcript/session replay, discovery status packets and Codex App/CLI/IDE extension compatibility notes."
trust_level: "high"
verification_status: "Backed by product-agent-os docs contract tests, transcript/session eval runner tests, focused discovery status tests, fixture eval coverage, docs structure checks and strict MkDocs build in the T8-D verification loop."
```

```yaml
title: "OpenAI Codex GitHub repository"
url: "https://github.com/openai/codex"
type: "repository"
status: "official"
checked_at: "2026-05-14"
summary: "Open-source Codex CLI repository and issue/discussion entry point."
relevance: "Implementation details, issues, examples, and release artifacts."
trust_level: "high"
```

```yaml
title: "obra/superpowers"
url: "https://github.com/obra/superpowers"
type: "repository"
status: "community"
checked_at: "2026-05-23"
summary: "Open-source agentic skills framework with composable skills, skill-triggering rules, TDD/debugging/planning/review workflows, hook/bootstrap examples, plugin manifests and behavior-oriented tests."
relevance: "Comparative intake for Product-Agent OS Track 8 behavioral workflow evals, route testing, root-cause bug rescue, no-placeholder planning, two-stage review and Codex-only compatibility checks."
trust_level: "medium"
verification_status: "Repository inspected locally and via GitHub; not authoritative for Codex platform rules."
```

```yaml
title: "Community search backlog: Codex CLI tips and workflows"
url: "https://community.openai.com/"
type: "discussion"
status: "community"
checked_at: "2026-05-14"
summary: "Candidate source for user reports and operational tricks. Individual claims must be captured as insight cards before reuse."
relevance: "Future user-insight harvesting."
trust_level: "low"
```

```yaml
title: "Product-Agent OS Track 1-9 final documentation closure"
url: "docs/sources/product-agent-os-pre-track-8-implementation-inventory.md; docs/superpowers/specs/2026-05-25-track-9-methodology-intelligence-design.md; docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md; docs/sources/product-agent-os-track-9-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/architecture.md; docs/product-agent-os/scenarios.md; docs/product-agent-os/behavioral-evals.md; docs/product-agent-os/codex-compatibility.md; docs/product-agent-os/development-standards.md; docs/product-agent-os/methodology-intelligence.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/methodology_catalog.py; plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py; plugins/product-agent-os/scripts/product_agent_os/methodology_report.py; plugins/product-agent-os/scripts/product_agent_os/discovery.py; plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py; plugins/product-agent-os/scripts/run_methodology_audit.py; plugins/product-agent-os/scripts/run_fixture_eval.py; plugins/product-agent-os/scripts/run_transcript_eval.py; plugins/product-agent-os/scripts/validate_codex_compatibility.py; tests/product_agent_os/test_product_agent_os_docs.py"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-05-27"
summary: "Task 22 final documentation sync closure for Product-Agent OS Track 1-9, covering pre-Track-8 implementation inventory, Track 9 methodology intelligence design and backlog, user-facing Product-Agent OS docs, READMEs, runtime runner, methodology audit/report/discovery paths, fixture/transcript evals, Codex compatibility validation and root control-plane closure."
relevance: "Final Track 9 documentation/source-registry closure before Track 10 Task 23 starts; records that legacy Track 9 Task 23 baseline verification is absorbed into Task 22 final verification evidence."
trust_level: "high"
verification_status: "Backed by Task 22 RED/GREEN docs tests, transcript eval, docs check, strict MkDocs, full unittest, fixture eval and git diff hygiene in the current closure run. OpenAPI v3.2.0 freshness claim remains sourced by the checked official OpenAPI specification entry and Track 6/7 methodology registry evidence."
```

```yaml
title: "Product-Agent OS Track 10 guided question and status dashboard coverage"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/scenarios.md; docs/product-agent-os/behavioral-evals.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/question_protocol.py; plugins/product-agent-os/scripts/product_agent_os/question_ledger.py; plugins/product-agent-os/scripts/product_agent_os/status_snapshot.py; plugins/product-agent-os/scripts/product_agent_os/status_dashboard.py; plugins/product-agent-os/scripts/run_fixture_eval.py; plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json; plugins/product-agent-os/assets/eval-fixtures/transcripts/product-agent-os-synthetic-sessions.json; tests/product_agent_os/test_fixture_eval_runner.py; tests/product_agent_os/test_lifecycle_skills.py; tests/product_agent_os/test_product_agent_os_docs.py; tests/product_agent_os/test_transcript_session_evals.py"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-05-28"
summary: "T10-Q-M15..M22 Batch 5 closure and T10-Q-M23..M25 Batch 6 closure for Task 23 guided question protocol and status dashboard coverage, including question_queue_contract_present, status_snapshot_present, status_dashboard_present, dashboard_no_external_assets, question_budget_false_positive_guard_present, dashboard_not_source_of_truth, stale_evidence_no_success_claim, lifecycle skill wording, behavioral eval cases, transcript sessions and full verification."
relevance: "Track 10 Task 23 eval, skill, docs, README, source registry, root control-plane sync and Batch 6 verification for guided questions, answer ledger, status snapshot and generated offline dashboard behavior."
trust_level: "high"
verification_status: "Backed by focused Batch 5 RED/GREEN tests and Batch 6 full verification in the current implementation run: 543-unit full suite OK, fixture eval exit 0 with renderer_file_count 187, transcript eval 10 sessions with 0 failures, Codex compatibility status compatible, docs check, strict MkDocs and git diff hygiene exit 0. Commit/push/PR remains explicit-only and was not executed."
```

```yaml
title: "Product-Agent OS Track 10 self-verification metrics-loop Batch 7 foundation"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics.py; tests/product_agent_os/test_agent_skill_metrics.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-05-28"
summary: "T10-SV-M-1..M4 Batch 7 foundation and registry coverage for Task 24 Self-Verification And Modernization Loop, including read-only source-priority policy, target registry collection, explicit evidence intake, stale/failed/accepted-gap evidence markers, generated-view source rejection and bounded metrics packet trimming."
relevance: "Track 10 Task 24 Batch 7 implementation evidence, source-priority contract, metrics packet bounds, target registry and explicit evidence intake before trace/dataset/judge, metrics, report/CLI and runtime integration batches."
trust_level: "high"
verification_status: "Backed by focused RED/GREEN tests: missing module and stale-evidence checks failed before implementation, `python -m unittest tests.product_agent_os.test_agent_skill_metrics -v` ran 5 tests with OK, and adjacent reuse-first suites for status snapshot/dashboard, templates and automation policy ran 103 tests with OK. Full Product-Agent OS verification for the current slice ran 548 unit tests with OK; fixture eval, transcript eval, Codex compatibility, docs check and git diff hygiene exited 0."
```

```yaml
title: "Product-Agent OS Track 10 self-verification metrics-loop Batch 8 trace redaction dataset judge contracts"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics.py; tests/product_agent_os/test_agent_skill_metrics.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-05-28"
summary: "T10-SV-M5..M16 Batch 8 coverage for Task 24 Self-Verification And Modernization Loop, including portable trace normalization, metrics redaction blocking, evidence dataset grouping, dataset quality gates, local grader summaries and judge calibration blocking."
relevance: "Track 10 Task 24 Batch 8 implementation evidence before metric aggregation, scorecards, report/CLI, runtime integration, lifecycle/eval coverage and final documentation batches."
trust_level: "high"
verification_status: "Backed by focused RED/GREEN tests: Batch 8 imports failed before implementation, then `python -m unittest tests.product_agent_os.test_agent_skill_metrics -v` ran 11 tests with OK. Adjacent status/dashboard, template/automation and fixture/transcript runner suites ran 22, 87 and 21 tests with OK; full unittest ran 554 tests with OK using timeout_ms 600000; fixture eval, transcript eval, Codex compatibility, docs check and git diff hygiene exited 0."
```

```yaml
title: "Product-Agent OS Track 10 self-verification metrics-loop Batch 9 metrics scorecards confidence cadence contracts"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics.py; tests/product_agent_os/test_agent_skill_metrics.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-05-28"
summary: "T10-SV-M17..M28 Batch 9 coverage for Task 24 Self-Verification And Modernization Loop, including metric aggregation sections, repeatability metrics, guarded scorecards, Wilson confidence gates, cadence recommendation and redacted run records."
relevance: "Track 10 Task 24 Batch 9 implementation evidence before scorecard ledger, report/CLI, runtime integration, lifecycle/eval coverage and final documentation batches."
trust_level: "high"
verification_status: "Backed by focused RED/GREEN tests: Batch 9 imports failed before implementation, then `python -m unittest tests.product_agent_os.test_agent_skill_metrics -v` ran 17 tests with OK. Adjacent status/dashboard, template/automation and fixture/transcript runner suites ran 28, 87 and 21 tests with OK; full unittest ran 560 tests with OK in 809.106s using timeout_ms 900000; fixture eval, transcript eval, Codex compatibility, docs check and git diff hygiene exited 0."
```

```yaml
title: "Product-Agent OS Track 10 self-verification metrics-loop Batch 10 ledger reports candidates cli contracts"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics.py; plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics_report.py; plugins/product-agent-os/scripts/product_agent_os/offline_artifact_safety.py; plugins/product-agent-os/scripts/render_agent_skill_metrics_report.py; tests/product_agent_os/test_agent_skill_metrics.py; tests/product_agent_os/test_agent_skill_metrics_report.py; tests/product_agent_os/test_agent_skill_metrics_cli.py; tests/product_agent_os/test_fixture_eval_runner.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-05-28"
summary: "T10-SV-M29..M45 Batch 10 coverage for Task 24 Self-Verification And Modernization Loop, including trace data-classification, shared offline artifact safety, scorecard ledger, daily/weekly metrics packets, component prioritization, modernization candidates, redacted offline report rendering, dry-run/stage CLI and metrics automation candidate-only blocking."
relevance: "Track 10 Task 24 Batch 10 implementation evidence before runtime/discovery/lifecycle/eval integration and final documentation closure batches."
trust_level: "high"
verification_status: "Backed by focused RED/GREEN tests: Batch 10 imports/modules/templates and metrics automation blocking failed before implementation, then the focused suite ran 127 tests with OK. Fixture runner unit suite ran 17 tests with OK; full unittest ran 575 tests with OK in 612.098s using timeout_ms 1200000; fixture eval exited 0 with 80 fixtures and renderer_file_count 191; transcript eval exited 0 with 10 sessions and 0 failures; Codex compatibility returned status compatible; docs check and git diff hygiene exited 0."
```

```yaml
title: "Product-Agent OS Track 10 self-verification metrics-loop Batch 11 runtime discovery lifecycle eval contracts"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; plugins/product-agent-os/scripts/product_agent_os/status_snapshot.py; plugins/product-agent-os/scripts/product_agent_os/discovery.py; plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py; plugins/product-agent-os/scripts/product_agent_os/question_protocol.py; plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py; plugins/product-agent-os/scripts/codex_runtime_runner/routes.py; plugins/product-agent-os/scripts/run_fixture_eval.py; plugins/product-agent-os/assets/templates/evals/project-readiness.json; plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json; plugins/product-agent-os/assets/eval-fixtures/transcripts/product-agent-os-synthetic-sessions.json; plugins/product-agent-os/skills; tests/product_agent_os/test_status_snapshot.py; tests/product_agent_os/test_discovery.py; tests/product_agent_os/test_methodology_audit.py; tests/product_agent_os/test_codex_runtime_runner_contracts.py; tests/product_agent_os/test_codex_runtime_runner_state_routes.py; tests/product_agent_os/test_question_protocol.py; tests/product_agent_os/test_lifecycle_skills.py; tests/product_agent_os/test_behavioral_workflow_evals.py; tests/product_agent_os/test_transcript_session_evals.py; tests/product_agent_os/test_fixture_eval_runner.py; tests/product_agent_os/test_infrastructure_templates.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-05-28"
summary: "T10-SV-M46..M57 Batch 11 coverage for Task 24 Self-Verification And Modernization Loop, including bounded status snapshot metrics summaries, discovery and methodology audit applicability, runtime packet validation, review-only route finish options, guided question integration, lifecycle staged-evidence wording, fixture false-positive coverage, behavioral eval cases and transcript sessions."
relevance: "Track 10 Task 24 Batch 11 implementation evidence before final Task 24 docs/control-plane/full-verification closure."
trust_level: "high"
verification_status: "Backed by focused RED/GREEN tests: Batch 11 status/discovery/audit/runtime/lifecycle/eval checks failed before implementation, then the focused suite ran 306 tests with OK. Full unittest ran 583 tests with OK in 636.067s using timeout_ms 1200000; fixture eval exited 0 with 85 fixtures, 0 failures and renderer_file_count 191; transcript eval exited 0 with 17 sessions and 0 failures; Codex compatibility returned status compatible; docs/source-policy slice ran 22 tests with OK; docs check and git diff hygiene exited 0."
```

```yaml
title: "Product-Agent OS Track 10 self-verification metrics-loop final closure"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; docs/product-agent-os/behavioral-evals.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics.py; plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics_report.py; plugins/product-agent-os/scripts/render_agent_skill_metrics_report.py; plugins/product-agent-os/scripts/run_fixture_eval.py; plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json; plugins/product-agent-os/assets/eval-fixtures/transcripts/product-agent-os-synthetic-sessions.json; tests/product_agent_os/test_agent_skill_metrics.py; tests/product_agent_os/test_agent_skill_metrics_report.py; tests/product_agent_os/test_agent_skill_metrics_cli.py; tests/product_agent_os/test_product_agent_os_docs.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-05-28"
summary: "T10-SV-M58..M62 final Task 24 docs, README, source registry, backlog and root control-plane closure for the self-verification metrics loop. The closure documents agent_skill_metrics_loop_contract_present, metrics_report_redacted, trace_normalization_contract_present, judge_calibration_gate_present, scorecard_ledger_contract_present, source_priority_contract_present, metrics_packet_bounds_present, trace_data_classification_gate_present, offline_artifact_safety_shared, no_baseline_renderer_pollution, active_metrics_automation_blocked, update_candidate_rollback_required, metrics_loop_runtime_route_contract_present, metrics_loop_lifecycle_contract_present and metrics_loop_false_positive_guards_present."
relevance: "Track 10 Task 24 final user-facing source-backed documentation and control-plane closure for staged self-verification reports, scorecards, target registry, trace intake, dataset quality, grader/judge calibration, cadence recommendation, modernization candidates, approval boundary and source-of-truth policy."
trust_level: "high"
verification_status: "Backed by Batch 12 focused RED/GREEN docs checks, 23-test docs/source-policy slice, full unittest with timeout_ms 1200000 running 584 tests with OK in 551.714s and rerunning after evidence notes with 584 tests OK in 504.793s, fixture eval exit 0 for 85 fixture directories with renderer_file_count 191, transcript eval exit 0 with 17 sessions and 0 failures, Codex compatibility status compatible, docs check and git diff hygiene exit 0. Commit, push and PR actions remain explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 project code graph Batch 13-14 foundation and overlays"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/project_code_graph.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_adapters.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_chunking.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_manifest.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_observations.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_ontology.py; plugins/product-agent-os/scripts/scan_project_code_graph.py; tests/product_agent_os/test_project_code_graph.py; tests/product_agent_os/test_project_graph_python_scanner.py; tests/product_agent_os/test_project_graph_overlays.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-01"
summary: "Track 10 Task 25 Batch 13-14 implementation evidence for the Product-Agent OS project code graph: read-only stage-only graph JSON/JSONL, controlled ontology/schema validation, manifest freshness/provenance, observation lineage, temporal edge delta helpers, Python AST package/module/class/function/method overlays, conservative import/call/test edges, unsupported-language adapter boundaries, structured Markdown/OpenAPI/AsyncAPI/DBML/SQL/JSON/YAML/Mermaid/PlantUML overlays, partition scopes, canonical aliases and bounded readiness metadata."
relevance: "Task 25 project code graph scanner and overlay docs/control-plane closure before Batch 15 query/runtime/analysis work."
trust_level: "high"
verification_status: "Backed by focused scanner/overlay tests running 14 tests with OK, focused graph suite running 47 tests with OK, adjacent graph plus infrastructure renderer/CLI suite running 77 tests with OK, full unittest with timeout_ms 1200000 running 631 tests with OK in 554.103s, fixture eval exit 0 for 91 fixture directories with renderer_file_count 191, transcript eval exit 0 with 17 sessions and 0 failures, Codex compatibility status compatible, docs check, strict MkDocs and git diff hygiene exit 0. Commit, push and PR actions remain explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 project code graph Batch 15 query runtime analysis"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/project_graph_queries.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_analysis.py; plugins/product-agent-os/scripts/product_agent_os/status_snapshot.py; plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py; plugins/product-agent-os/scripts/codex_runtime_runner/routes.py; plugins/product-agent-os/scripts/codex_runtime_runner/guards.py; plugins/product-agent-os/scripts/scan_project_code_graph.py; plugins/product-agent-os/skills; tests/product_agent_os/test_project_graph_queries.py; tests/product_agent_os/test_project_graph_analysis.py; tests/product_agent_os/test_project_graph_cli.py; tests/product_agent_os/test_status_snapshot.py; tests/product_agent_os/test_codex_runtime_runner_contracts.py; tests/product_agent_os/test_codex_runtime_runner_state_routes.py; tests/product_agent_os/test_lifecycle_skills.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-01"
summary: "Track 10 Task 25 Batch 15 implementation evidence for bounded Product-Agent OS project graph query/runtime/analysis behavior: graph JSON/JSONL query packets, query CLI mode, token/output budgets, hub suppression, filter validation, trace/impact/affected-test/delta/read-order packets, runtime project_graph_status validation, status snapshot graph summaries, lifecycle source-of-truth wording and source-free graph analysis reports."
relevance: "Task 25 project code graph Batch 15 docs/control-plane sync before Batch 16 HTML cockpit and visual graph implementation."
trust_level: "high"
verification_status: "Backed by focused RED/GREEN query/runtime/status/lifecycle suite: missing query/analysis/runtime/status/lifecycle graph contracts failed before implementation, reviewer-driven regression tests exposed budget/filter/path/unsupported-language issues, then the focused suite ran 108 tests with OK. Full unittest ran 646 tests with OK in 558.013s using timeout_ms 1200000; fixture eval exited 0 for 91 fixture directories with renderer_file_count 191; transcript eval exited 0 with 17 sessions and 0 failures; Codex compatibility returned status compatible; docs check, strict MkDocs and git diff hygiene exited 0. Commit, push and PR actions remain explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 project code graph Batch 16 cockpit visualization"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/project_cockpit_model.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_visual_model.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_renderer.py; plugins/product-agent-os/assets/templates/project-graph/project-cockpit.html; plugins/product-agent-os/assets/templates/project-graph/project-graph.html; plugins/product-agent-os/assets/templates/project-graph/project-code-flow.html; plugins/product-agent-os/assets/templates/project-graph/project-graph.css; tests/product_agent_os/test_project_cockpit_model.py; tests/product_agent_os/test_project_graph_visual_model.py; tests/product_agent_os/test_project_graph_renderer.py; tests/product_agent_os/test_product_agent_os_docs.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-01"
summary: "Track 10 Task 25 Batch 16 `T10-CG-V2-M19..M26` implementation evidence for generated Product-Agent OS project graph cockpit behavior: exactly eight top-level cockpit pages, Code Flow inside Code Intelligence, offline no-external-assets HTML renderer, Graphology-compatible static visual projection, local Graphology/Sigma vendor boundary, filters, focused subgraphs, selected-node evidence, fallback static table, mobile CSS and stage-only HTML/JSON review surfaces."
relevance: "Task 25 project code graph Batch 16 docs/control-plane sync before Batch 17 fixture structural fields, search-quality evals, future backend/semantic gates and final closure."
trust_level: "high"
verification_status: "Backed by focused RED/GREEN cockpit/visual/renderer tests: missing cockpit model, visual model and renderer modules failed before implementation; focused suite then ran 12 tests with OK after reviewer-driven fixes for visual projection sanitization, unsafe cockpit Code Flow paths, analysis payload allowlisting, manifest tamper rejection, hard visual caps, renderer active page/section anchor propagation and working filter/navigation commands; adjacent graph integration suite ran 60 tests with OK. Playwright visual smoke on staged cockpit HTML found 0 console errors after navigation, 0 external scripts, 8 pages, 14 nodes, 8 filters, selected-node evidence/filter behavior and no mobile horizontal overflow. Full unittest ran 659 tests with OK in 698.951s using timeout_ms 1200000; fixture eval exited 0 for 91 fixture directories with renderer file count 191 and 16 codex-runner fixtures; transcript eval exited 0 with 17 sessions and 0 failures; Codex compatibility returned status compatible; docs check, strict MkDocs and git diff hygiene exited 0. Commit, push and PR actions remain explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 project code graph Batch 17 evals and future gates"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/project_graph_search_quality.py; plugins/product-agent-os/scripts/run_fixture_eval.py; tests/product_agent_os/test_project_graph_search_quality.py; tests/product_agent_os/test_fixture_eval_runner.py; tests/product_agent_os/test_product_agent_os_docs.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-01"
summary: "Track 10 Task 25 Batch 17 `T10-CG-V2-M27..M30` implementation evidence for fixture structural fields, search-quality eval loop, explicit future backend and semantic gates, and docs/source/control-plane sync. Fixture eval exposes `project_graph_search_quality_present`, `project_graph_future_backend_semantic_gates_present`, graph contract, no external assets, redaction, scale bounds, generated-view-only, eight-page cockpit structure, section preservation and cockpit generated-view boundary."
relevance: "Task 25 project code graph Batch 17 docs/control-plane sync before Batch 18 focused/full verification and final closure."
trust_level: "high"
verification_status: "Backed by current-run RED/GREEN and broad verification: search-quality module was missing before implementation, fixture structural fields and docs/control-plane terms were absent before sync, focused graph/cockpit/search/docs suite ran 63 tests with OK, docs contract suite ran 17 tests with OK after restoring Batch 16 exact phrases, full unittest rerun ran 662 tests with OK in 671.629s using timeout_ms 1200000, fixture eval exited 0 for 91 fixture directories with renderer_file_count 191, transcript eval exited 0 with 17 sessions and 0 failures, Codex compatibility returned status compatible, docs check, strict MkDocs with disposable .mkdocs_task25_batch17_site and git diff hygiene exited 0. Batch 17 does not activate a static search index, live database/server, LLM, embedding, cross-encoder, semantic extraction or rationale/comment extraction. Commit, push and PR actions remain explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 project code graph Batch 18 final verification closure"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; tests/product_agent_os/test_product_agent_os_docs.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-01"
summary: "Track 10 Task 25 Batch 18 `T10-CG-V2-M31..M32` focused/full verification closure for the read-only Product-Agent OS project code graph and generated HTML cockpit baseline. Closure confirms scanner, schema, manifest, overlays, query packets, renderer, status/runtime integration, fixture eval, transcript eval, Codex compatibility, docs check, strict MkDocs, diff hygiene and explicit-only git boundary."
relevance: "Final Task 25 baseline docs/control-plane closure before any future-gated Batch 19-23 static index, backend, semantic retrieval or LLM extraction work can be considered."
trust_level: "high"
verification_status: "Backed by Batch 18 focused/full verification: graph/cockpit/search suite ran 70 tests with OK, status/runtime suite ran 47 tests with OK, fixture/lifecycle/docs suite ran 86 tests with OK, full unittest ran 664 tests with OK using timeout_ms 1200000, fixture eval exited 0 for 91 fixture directories with renderer_file_count 191, transcript eval exited 0 with 17 sessions and 0 failures, Codex compatibility returned status compatible, docs check, strict MkDocs with disposable .mkdocs_task25_batch18_site and git diff hygiene exited 0. Batch 18 does not activate future-gated Batch 19-23 surfaces. Commit, push and PR actions remain explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 project code graph Batch 19 offline static search index"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/project_graph_index.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_queries.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_search_quality.py; plugins/product-agent-os/scripts/scan_project_code_graph.py; plugins/product-agent-os/scripts/run_fixture_eval.py; tests/product_agent_os/test_project_graph_index.py; tests/product_agent_os/test_project_graph_queries.py; tests/product_agent_os/test_project_graph_cli.py; tests/product_agent_os/test_project_graph_search_quality.py; tests/product_agent_os/test_fixture_eval_runner.py; tests/product_agent_os/test_product_agent_os_docs.py; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-01"
summary: "Track 10 Task 25 Batch 19 `T10-CG-V2-M33..M38` implementation evidence for an offline static search index. The explicit user approval to execute Batch 19 is scoped to a generated cache built from redacted graph artifact only, optional indexed search packets, cache hit/miss/invalidation, stale-index blocking and indexed search-quality evals."
relevance: "Task 25 project code graph extension after Batch 18 baseline closure, before future-gated local database/server, semantic retrieval and LLM extraction batches."
trust_level: "high"
verification_status: "Backed by current-run RED/GREEN and broad verification: missing project_graph_index module and CLI --build-index failed before implementation, stale docs/control-plane terms failed before sync, focused index/query/CLI/search-quality tests ran 27 tests with OK, adjacent graph/cockpit/index suite ran 78 tests with OK, fixture/lifecycle/docs suite ran 87 tests with OK, full unittest ran 673 tests with OK in 643.591s using timeout_ms 1200000, fixture eval exited 0 with renderer file count 191 and all emitted fixture records ok true, transcript eval exited 0 with 17 sessions and 0 failures, Codex compatibility returned status compatible, docs check, strict MkDocs with disposable .mkdocs_task25_batch19_site and git diff hygiene exited 0. Fixture eval exposes project_graph_static_search_index_present and project_graph_static_search_index_quality_present. The offline static search index is generated, cache-bound and not source of truth; it uses no live database/server, LLM, embedding or cross-encoder; rollback/disable path is deleting .codex/product-agent-os/project-code-graph-search-index.json. Commit, push and PR actions remain explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 project code graph Batch 20 local query backend gate"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/project_graph_backend.py; plugins/product-agent-os/scripts/scan_project_code_graph.py; plugins/product-agent-os/scripts/run_fixture_eval.py; tests/product_agent_os/test_project_graph_backend.py; tests/product_agent_os/test_project_graph_cli.py; tests/product_agent_os/test_fixture_eval_runner.py; tests/product_agent_os/test_product_agent_os_docs.py; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-01"
summary: "Track 10 Task 25 Batch 20 `T10-CG-V2-M39..M44` implementation evidence for the local query backend gate. The approved surface is a generated local file-store at `.codex/product-agent-os/project-code-graph-backend.json`, built from graph/static-index artifacts only, with `project_graph_local_backend_gate_present`, disabled-by-default server lifecycle, read-only API contract, graph-only fallback and rollback/disable path."
relevance: "Task 25 project code graph extension after Batch 19 static index and before Batch 21 semantic retrieval plus future-gated LLM extraction batches."
trust_level: "high"
verification_status: "Backed by current-run RED/GREEN and broad verification: missing project_graph_backend module and CLI --build-backend/--backend controls failed before implementation, stale docs/control-plane terms failed before sync, focused backend/CLI/fixture checks ran 21 tests with OK, docs contract suite ran 21 tests with OK, full unittest ran 680 tests with OK in 638.899s using timeout_ms 1200000, fixture eval exited 0 with renderer file count 191 and all emitted fixture records ok true, transcript eval exited 0 with 17 sessions and 0 failures, Codex compatibility returned status compatible, docs check, strict MkDocs with disposable .mkdocs_task25_batch20_site and git diff hygiene exited 0. Fixture eval exposes project_graph_local_backend_gate_present, project_graph_backend_decision_packet_present, project_graph_backend_disabled_by_default, project_graph_backend_operational_controls_present, project_graph_backend_graph_only_fallback_present and project_graph_backend_no_production_or_source_truth_claims. The generated local file-store is not source of truth, server mode is disabled by default, no production server is started, graph-only fallback remains available and rollback/disable path is deleting .codex/product-agent-os/project-code-graph-backend.json. Commit, push and PR actions remain explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 project code graph Batch 21 semantic retrieval, embeddings and cross-encoder eval"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_queries.py; plugins/product-agent-os/scripts/scan_project_code_graph.py; plugins/product-agent-os/scripts/run_fixture_eval.py; tests/product_agent_os/test_project_graph_semantic.py; tests/product_agent_os/test_project_graph_cli.py; tests/product_agent_os/test_fixture_eval_runner.py; tests/product_agent_os/test_product_agent_os_docs.py; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-01"
summary: "Track 10 Task 25 Batch 21 `T10-CG-V2-M45..M51` implementation evidence for semantic retrieval, embeddings cache metadata and cross-encoder eval. The approved surface is a generated semantic retrieval index at `.codex/product-agent-os/project-code-graph-semantic-index.json`, built from redacted graph/static-index artifacts only, with `project_graph_semantic.py`, `project_graph_semantic_retrieval_gate_present`, semantic corpus/chunk policy, embeddings cache metadata, semantic query packets, cross-encoder eval, `present_unverified` routing, no canonical graph edge rewrites and rollback/disable path."
relevance: "Task 25 project code graph extension after Batch 20 local backend gate, before future-gated LLM semantic extraction and rationale/comment proposal batches."
trust_level: "high"
verification_status: "Backed by current-run RED/GREEN and broad verification: missing project_graph_semantic module, CLI semantic index controls, fixture fields and stale docs/control-plane terms failed before implementation; focused semantic/CLI/fixture/docs checks ran 27 tests with OK; docs contract suite ran 22 tests with OK; full unittest ran 688 tests with OK in 639.625s using timeout_ms 1200000; fixture eval exited 0 with renderer file count 191 and all emitted fixture records ok true; transcript eval exited 0 with 17 sessions and 0 failures; Codex compatibility returned status compatible; docs check, strict MkDocs with disposable .mkdocs_task25_batch21_site and git diff hygiene exited 0. Fixture eval exposes project_graph_semantic_retrieval_gate_present, project_graph_semantic_retrieval_eval_present and project_graph_semantic_present_unverified_routing_present. The generated semantic retrieval index is not source of truth, uses local deterministic embeddings and cross-encoder eval only, stores no raw source bodies or absolute local paths, marks semantic hits as present_unverified orientation evidence, performs no canonical graph edge rewrites and rolls back by deleting .codex/product-agent-os/project-code-graph-semantic-index.json. Commit, push and PR actions remain explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 project code graph Batch 22 LLM semantic extraction"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py; plugins/product-agent-os/scripts/scan_project_code_graph.py; plugins/product-agent-os/scripts/run_fixture_eval.py; tests/product_agent_os/test_project_graph_llm_extraction.py; tests/product_agent_os/test_project_graph_cli.py; tests/product_agent_os/test_fixture_eval_runner.py; tests/product_agent_os/test_product_agent_os_docs.py; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-02"
summary: "Track 10 Task 25 Batch 22 `T10-CG-V2-M52..M57` implementation evidence for local deterministic LLM semantic extraction and rationale/comment proposals. The approved surface is a generated proposal artifact at `.codex/product-agent-os/project-code-graph-llm-proposals.json`, built from redacted graph/semantic-index artifacts only, with `project_graph_llm_extraction.py`, `project_graph_llm_extraction_gate_present`, prompt/model policy, structured JSON, semantic node and edge proposals, rationale/comment proposals, human review, AI incident workflow, rollback/disable path and staged proposals, not canonical graph facts."
relevance: "Task 25 project code graph extension after Batch 21 semantic retrieval and before Batch 23 future extension verification, rollback and closure."
trust_level: "high"
verification_status: "Backed by current-run RED/GREEN and broad verification: missing project_graph_llm_extraction module, CLI --build-llm-proposals/--disable-llm-proposals controls, fixture fields and stale docs/control-plane terms failed before implementation; focused Batch 22 module/CLI/fixture/docs suite ran 29 tests with OK; Product-Agent OS docs contract suite ran 23 tests with OK; adjacent graph/backend/semantic/LLM suite ran 45 tests with OK; full unittest ran 697 tests with OK in 880.817s using timeout_ms 1200000; fixture eval exited 0 for 91 fixture directories with renderer_file_count 191 and emitted fixture records ok true; transcript eval exited 0 with 17 sessions and 0 failures; Codex compatibility returned status compatible; docs check passed; strict MkDocs with disposable .mkdocs_task25_batch22_site exited 0 and the site directory was removed; git diff hygiene exited 0. Batch 22 exposes project_graph_llm_extraction_gate_present, project_graph_llm_proposal_schema_present, project_graph_rationale_comment_proposals_present and project_graph_llm_extraction_eval_present. The generated proposal artifact is not source of truth, uses local deterministic prompt/model policy only, stores no raw source bodies or absolute local paths, labels unsupported claims, performs no canonical graph mutation, routes unsafe output to the AI incident workflow, and rolls back by deleting .codex/product-agent-os/project-code-graph-llm-proposals.json. Commit, push and PR actions remain explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 project code graph Batch 23 future extension verification"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/project_graph_extension_closure.py; plugins/product-agent-os/scripts/scan_project_code_graph.py; plugins/product-agent-os/scripts/run_fixture_eval.py; tests/product_agent_os/test_project_graph_extension_closure.py; tests/product_agent_os/test_project_graph_cli.py; tests/product_agent_os/test_fixture_eval_runner.py; tests/product_agent_os/test_product_agent_os_docs.py; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-02"
summary: "Track 10 Task 25 Batch 23 `T10-CG-V2-M58..M62` implementation evidence for future extension verification, rollback and closure. The approved surface is a generated closure artifact at `.codex/product-agent-os/project-code-graph-extension-closure.json`, built from approved generated Batch 19-22 extension artifacts and explicit verification evidence only, with `project_graph_extension_closure.py`, `verify-extensions`, `disable-extensions`, rollback/data deletion proof, graph-only fallback and unapproved-surface blocking."
relevance: "Task 25 project code graph extension closure after Batch 19 offline static search index, Batch 20 local backend gate, Batch 21 semantic retrieval and Batch 22 LLM proposal artifacts."
trust_level: "high"
verification_status: "Backed by current-run RED/GREEN and full verification evidence: missing project_graph_extension_closure module, CLI --verify-extensions/--disable-extensions controls, fixture fields and stale docs/control-plane terms failed before implementation; focused Batch 23 module/CLI/fixture slice ran 6 tests with OK; Product-Agent OS docs contract suite ran 24 tests with OK; adjacent graph extension suite ran 50 tests with OK; full unittest ran 703 tests with OK in 724.475s using timeout_ms 1200000; fixture eval exited 0 with renderer file count 191 and all emitted fixture records ok true; transcript eval exited 0 with 17 sessions and 0 failures; Codex compatibility returned status compatible; docs check, strict MkDocs with disposable .mkdocs_task25_batch23_site and git diff --check exited 0. Batch 23 exposes project_graph_future_extension_closure_present, project_graph_extension_rollback_deletion_present, project_graph_unapproved_surface_blocking_present and project_graph_extension_full_verification_contract_present. The generated closure artifact is not source of truth, stores no raw source bodies or absolute local paths, starts no live server, permits no live external model/API calls, performs no canonical graph mutation, proves generated-artifact deletion and graph-only fallback, and marks unapproved live/model/canonical-mutation surfaces as blocked_without_new_explicit_approval. Commit, push and PR actions remain explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 Task 26 Batch 24 live governance"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/project_graph_live_governance.py; plugins/product-agent-os/scripts/scan_project_code_graph.py; plugins/product-agent-os/scripts/run_fixture_eval.py; tests/product_agent_os/test_project_graph_live_governance.py; tests/product_agent_os/test_fixture_eval_runner.py; tests/product_agent_os/test_product_agent_os_docs.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-02"
summary: "Track 10 Task 26 Batch 24 `T10-LIVE-M01..M06` implementation evidence for live governance approval, data classification, redaction, credentials, cache and budget policy. The approved surface is governance-only: `project_graph_live_governance.py`, `project_graph_live_approval_packet_present`, `project_graph_live_data_classification_policy_present`, `project_graph_live_redaction_guard_present`, `project_graph_provider_credentials_boundary_present`, `project_graph_live_cache_deletion_policy_present`, `project_graph_live_budget_guard_present` and `project_graph_live_governance_no_live_calls_present`."
relevance: "Task 26 Batch 24 prepares approval and safety contracts before any later live provider, live server or canonical graph mutation work can be considered."
trust_level: "high"
verification_status: "Backed by current-run RED/GREEN and broad verification evidence: missing project_graph_live_governance module failed before implementation; focused live governance plus adjacent CLI suite ran 27 tests with OK; focused fixture/docs contract suite ran 2 tests with OK; full unittest ran 710 tests with OK in 924.506s using timeout_ms 1200000; fixture eval exited 0 with renderer file count 191 and all emitted fixture records ok true; transcript eval exited 0 with 17 sessions and 0 failures; Codex compatibility returned status compatible; docs check passed; strict MkDocs with disposable .mkdocs_task26_batch24_site exited 0 and the site directory was removed; git diff --check exited 0. Batch 24 starts no live server, performs no provider calls, permits no live external model/API calls, performs no canonical graph mutation and keeps git staging/commit/push/PR explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 Task 26 Batch 25 live runtime"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/project_graph_live_runtime.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_live_governance.py; plugins/product-agent-os/scripts/scan_project_code_graph.py; plugins/product-agent-os/scripts/run_fixture_eval.py; tests/product_agent_os/test_project_graph_live_runtime.py; tests/product_agent_os/test_project_graph_cli.py; tests/product_agent_os/test_fixture_eval_runner.py; tests/product_agent_os/test_product_agent_os_docs.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-02"
summary: "Track 10 Task 26 Batch 25 `T10-LIVE-M07..M10` implementation evidence for Live Local Read-Only Runtime, Auth And Fallback. The approved surface is contract-only and disabled by default through `project_graph_live_runtime.py`, with `project_graph_live_runtime_contract_present`, `project_graph_live_runtime_governance_prerequisite_present`, `project_graph_live_runtime_read_only_routes_present`, `project_graph_live_runtime_lifecycle_controls_present`, `project_graph_live_runtime_auth_policy_present`, `project_graph_live_runtime_graph_only_fallback_present` and `project_graph_live_runtime_no_public_or_mutation_surface_present`."
relevance: "Task 26 Batch 25 adds a local read-only runtime contract after Batch 24 governance. It remains generated staged evidence only, not source of truth, and does not start a live production server, call providers or mutate canonical graph facts."
trust_level: "high"
verification_status: "Backed by current-run RED/GREEN and broad verification evidence: missing project_graph_live_runtime module failed before implementation; focused live runtime tests ran 4 tests with OK; focused live runtime plus adjacent CLI suite ran 25 tests with OK; focused fixture eval contract ran 1 test with OK; docs/control-plane RED failed before sync; combined live runtime/CLI/fixture/docs suite ran 27 tests with OK; full unittest ran 715 tests with OK in 534.575s using timeout_ms 1200000; fixture eval exited 0 for 91 fixture directories with renderer file count 191 and all emitted fixture records ok true; transcript eval exited 0 with 17 sessions and 0 failures; Codex compatibility returned status compatible; docs check passed; strict MkDocs with disposable .mkdocs_task26_batch25_site exited 0 and the site directory was removed; git diff --check exited 0. Batch 25 keeps disabled_by_default_not_started, local-only access, rejects unauthorized access, no write endpoints, graph_only_query_mode, no provider calls, no live external model/API calls, no canonical graph mutation and git staging/commit/push/PR explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 Task 26 Batch 26 external embedding provider gate and eval"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/project_graph_embedding_provider.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_live_governance.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py; plugins/product-agent-os/scripts/scan_project_code_graph.py; plugins/product-agent-os/scripts/run_fixture_eval.py; tests/product_agent_os/test_project_graph_embedding_provider.py; tests/product_agent_os/test_project_graph_cli.py; tests/product_agent_os/test_fixture_eval_runner.py; tests/product_agent_os/test_product_agent_os_docs.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-02"
summary: "Track 10 Task 26 Batch 26 `T10-LIVE-M11..M12` implementation evidence for External Embedding Provider Gate And Eval. The contract uses `project_graph_embedding_provider.py` and fixture fields `project_graph_external_embedding_provider_gate_present`, `project_graph_external_embedding_governance_prerequisite_present`, `project_graph_external_embedding_redaction_cache_budget_present`, `project_graph_external_embedding_eval_baseline_present`, `project_graph_external_embedding_threshold_fallback_present` and `project_graph_external_embedding_no_live_calls_present`."
relevance: "Batch 26 adds an approval-bound external embedding provider gate and eval baseline after Batch 24 governance and Batch 21 semantic retrieval. It remains generated staged evidence only, not source of truth. No external call without approval/redaction/cache/budget. Must beat approved threshold or stay disabled with `semantic_retrieval_or_graph_only` fallback."
trust_level: "high"
verification_status: "Backed by current-run RED/GREEN and broad verification evidence: missing project_graph_embedding_provider module failed before implementation; focused provider module suite ran 4 tests with OK; focused provider plus adjacent CLI suite ran 26 tests with OK; focused fixture eval contract ran 1 test with OK; docs/control-plane RED failed before sync; combined provider/CLI/fixture/docs suite ran 28 tests with OK; full unittest ran 721 tests with OK in 496.212s using timeout_ms 1200000; fixture eval exited 0 for 91 fixture directories with renderer file count 191 and all emitted fixture records ok true; transcript eval exited 0 with 17 sessions and 0 failures; Codex compatibility returned status compatible; docs check passed; strict MkDocs with disposable .mkdocs_task26_batch26_site exited 0 and the site directory was removed; git diff --check exited 0. Batch 26 keeps provider_call_allowed false, external_call_performed false, no provider calls, no live external model/API calls, no canonical graph mutation and git staging/commit/push/PR explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 Task 26 Batch 27 cross-encoder reranker and hybrid retrieval"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/project_graph_reranker_provider.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_hybrid_retrieval.py; plugins/product-agent-os/scripts/scan_project_code_graph.py; plugins/product-agent-os/scripts/run_fixture_eval.py; tests/product_agent_os/test_project_graph_reranker_provider.py; tests/product_agent_os/test_project_graph_cli.py; tests/product_agent_os/test_fixture_eval_runner.py; tests/product_agent_os/test_product_agent_os_docs.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-03"
summary: "Track 10 Task 26 Batch 27 `T10-LIVE-M13..M14` implementation evidence for Cross-Encoder Reranker And Hybrid Retrieval. The contract uses `project_graph_reranker_provider.py` (`reranker_provider.py` artifact contract) and `project_graph_hybrid_retrieval.py` (`hybrid_retrieval.py` artifact contract), with fixture fields `project_graph_external_reranker_provider_gate_present`, `project_graph_external_reranker_governance_prerequisite_present`, `project_graph_external_reranker_redaction_cache_budget_present`, `project_graph_external_reranker_eval_baseline_present`, `project_graph_external_reranker_threshold_fallback_present`, `project_graph_external_reranker_no_live_calls_present`, `project_graph_hybrid_retrieval_pipeline_present`, `project_graph_hybrid_retrieval_explainable_fusion_present`, `project_graph_hybrid_retrieval_fallback_present` and `project_graph_hybrid_retrieval_no_canonical_mutation_present`."
relevance: "Batch 27 adds an approval_required external reranker provider gate/eval and hybrid retrieval fusion after Batch 24 governance, Batch 19 static search and Batch 21 semantic retrieval. Precision/MRR improves or fallback remains active; results are source-backed, bounded and explainable. It remains staged evidence only, not source of truth, with `semantic_retrieval_or_graph_only` fallback."
trust_level: "high"
verification_status: "Backed by current-run RED/GREEN and broad verification evidence: missing project_graph_hybrid_retrieval module failed before implementation; focused Batch 27 module suite ran 5 tests with OK; focused Batch 27 module plus CLI scenario ran 6 tests with OK; focused fixture eval contract ran 1 test with OK; docs/control-plane RED failed before sync; combined module/CLI/fixture/docs suite ran 8 tests with OK; full unittest ran 728 tests with OK in 553.596s using timeout_ms 1200000; fixture eval exited 0 for 91 fixture directories with renderer file count 191 and all emitted fixture records ok true; transcript eval exited 0 with 17 sessions and 0 failures; Codex compatibility returned status compatible; docs check passed; strict MkDocs with disposable .mkdocs_task26_batch27_site exited 0 and the site directory was removed; git diff --check exited 0. Batch 27 keeps provider_call_allowed false, external_call_performed false, No live provider calls, no provider calls, no live external model/API calls, no canonical graph mutation and git staging/commit/push/PR explicit-only."
```

```yaml
title: "Product-Agent OS Track 10 Task 26 Batch 28 live LLM proposal adapter and safety eval"
url: "docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md; docs/sources/product-agent-os-track-10-backlog.md; docs/product-agent-os/index.md; docs/product-agent-os/technical.md; docs/product-agent-os/scenarios.md; README.md; plugins/product-agent-os/README.md; plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_proposal_provider.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_live_governance.py; plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py; plugins/product-agent-os/scripts/scan_project_code_graph.py; plugins/product-agent-os/scripts/run_fixture_eval.py; tests/product_agent_os/test_project_graph_llm_proposal_provider.py; tests/product_agent_os/test_project_graph_cli.py; tests/product_agent_os/test_fixture_eval_runner.py; tests/product_agent_os/test_product_agent_os_docs.py; AGENTS.md; REQUIREMENTS.md; PLAN.md; TEST.md; EVALS.md; RUNLOG.md"
type: "internal documentation"
status: "checked-in project source"
checked_at: "2026-06-03"
summary: "Track 10 Task 26 Batch 28 `T10-LIVE-M15..M16` implementation evidence for Live LLM Proposal Adapter And Safety Eval. The contract uses `project_graph_llm_proposal_provider.py` (`llm_proposal_provider.py` artifact contract) and `llm-proposal-eval.json`, with fixture fields `project_graph_live_llm_proposal_provider_gate_present`, `project_graph_live_llm_proposal_governance_prerequisite_present`, `project_graph_live_llm_proposal_prompt_schema_present`, `project_graph_live_llm_proposal_redaction_cache_budget_present`, `project_graph_live_llm_proposal_safety_eval_present`, `project_graph_live_llm_proposal_threshold_fallback_present`, `project_graph_live_llm_proposal_incident_path_present`, `project_graph_live_llm_proposal_no_live_calls_present` and `project_graph_live_llm_proposal_no_canonical_mutation_present`."
relevance: "Batch 28 adds an approval_required external_llm proposal provider gate and safety eval after Batch 24 governance and Batch 22 local proposal generation. Output is proposal-only, never canonical fact; hallucination, privacy, grounding and stale-context tests route unsafe evidence to incident_blocked and AI incident workflow. It remains staged evidence only, not source of truth, with `local_llm_proposals_or_semantic_retrieval_or_graph_only` fallback."
trust_level: "high"
verification_status: "Backed by current-run RED/GREEN and broad verification evidence: missing project_graph_llm_proposal_provider module failed before implementation; focused Batch 28 module suite ran 4 tests with OK; focused Batch 28 CLI scenario ran 1 test with OK; focused fixture eval contract ran 1 test with OK; docs/control-plane RED failed before sync; combined module/CLI/fixture/docs suite ran 7 tests with OK; full unittest ran 734 tests with OK in 530.251s using timeout_ms 1200000; fixture eval exited 0 with renderer file count 191; transcript eval exited 0 with 17 sessions and 0 failures; Codex compatibility returned status compatible; docs check passed; strict MkDocs with disposable .mkdocs_task26_batch28_site exited 0 and the site directory was removed; git diff --check exited 0. Batch 28 keeps provider_call_allowed false, external_call_performed false, No live provider calls, no provider calls, no live external model/API calls, no canonical graph mutation and git staging/commit/push/PR explicit-only."
```
