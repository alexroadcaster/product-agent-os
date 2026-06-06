# Context7 Analysis

Source status: `official + tool-assisted`

Analysis date: **2026-05-14**.  
Analysis channel: Context7 documentation retrieval.

## Context7 Libraries Used

| Library ID | Purpose | Extracted Signal |
| --- | --- | --- |
| `/websites/developers_openai_codex` | Official Codex documentation | Subagent prompting, skill metadata, granular approvals and Codex MCP multi-agent example |
| `/openai/openai-agents-python` | OpenAI Agents SDK for Python | Core primitives: `Agent`, tools, handoffs, guardrails, sessions, tracing and multi-agent patterns |
| `/websites/developers_openai_api` | OpenAI API documentation | Responses API, tool definitions, Structured Outputs, built-in tools, multimodal and stateful patterns |
| `/websites/developers_openai` | OpenAI Developers documentation | Prompt structure, prompt objects, prompt versioning, context sections and eval-linked iteration |
| `/openai/openai-cookbook` | OpenAI Cookbook | Hallucination guardrails, LLM-as-judge validation, RAG grounding and citation discipline |

## Findings For The Knowledge Base

### Codex

- Approval policy should be described through granular config: `sandbox_approval`, `rules`, `mcp_elicitations`, `request_permissions` and `skill_approval`.
- A skill can extend `agents/openai.yaml` with UI metadata, invocation policy and dependencies, including MCP tools.
- Official subagent prompting pattern: ask Codex to create one agent per item, wait for all results and then produce a consolidated summary.
- Codex MCP can be used as an execution backend inside an Agents SDK multi-agent system where specialized agents call Codex for workspace work.
- Custom agents can define their own `model`, `model_reasoning_effort`, `sandbox_mode`, MCP servers and skill config; unspecified fields inherit from the parent session.
- Subagents inherit sandbox/approval controls from the parent workflow, while current-turn runtime overrides also apply to child agents.
- Model guidance can start with a strong default for most tasks and use cheaper models for fast, bounded subtasks.

### Agents SDK

- Agents SDK is organized around a small set of primitives: agents, tools, guardrails, handoffs, sessions and tracing.
- Two common multi-agent orchestration schemes are Manager pattern and Handoff pattern.
- Tools can be function tools, hosted tools, MCP tools or agents-as-tools.
- Sessions handle conversation persistence; tracing supports debugging, monitoring and workflow analysis.
- Production workflows should set model choice explicitly at agent, run-level default or process fallback level.
- Per-agent model selection is useful when a specialist consistently needs a different quality, latency or cost profile.

### Responses API

- Responses API is a low-level unified interface for agent-like applications.
- Tools are described as function tools, MCP tools, image generation and other built-in tool types.
- Structured Outputs through `text.format` with JSON Schema are useful for contracts between agents.
- Built-in tools and multi-turn state complement Agents SDK when direct API-level control is needed.

### Prompt And Context Engineering

- A prompt should behave like a contract: role, goal, context, constraints, uncertainty policy, tools, output format and verification.
- OpenAI prompting guidance supports versioned prompt objects, variables and eval-linked prompt iteration.
- Hallucination reduction needs a system: grounded context, structured output, verifier/guardrail, evals and fallback behavior.
- Structured Outputs reduce format failures, but still need fallback rules for incompatible user input.
- Cookbook patterns are useful as practical layers for hallucination detection, LLM-as-judge scoring, factual accuracy, relevance, policy compliance and contextual coherence.

### Product-Agent Workflows

- Codex product work needs control-plane artifacts: requirements, plan, tests, evals, run log and PR evidence.
- OpenAI Codex best practices emphasize Ask Mode before Code Mode, `AGENTS.md` for durable context, worktrees for parallel live work, and automations only after manual workflow stability.
- Skills are the method layer; automations are the schedule layer; plugins are the distribution layer.
- Long-horizon tasks need scored loops: baseline, one focused change, rerun eval, inspect artifact, log result and continue until explicit thresholds.
- Production agents need model/tool/instruction foundations, guardrails, human intervention and incremental orchestration rather than immediate over-automation.
- Reasoning level should match risk: low for fast scoped tasks, medium/high for complex changes and debugging, xhigh for long reasoning-heavy agentic work.
- Use-case pages show a repeated production pattern: structured inputs, explicit approval, smallest useful plan, runnable checks/evals, audit artifact, then skill or automation only after the workflow is stable.

### Codex Use Cases And Plugin Extraction

- The use-case index provides a taxonomy for plugin design: category, native platform, workflow family, team and task type.
- Most use-case cards can be reduced to one contract: outcome, best fit, inputs, skills/plugins, starter prompt, constraints, verification and related workflows.
- A plugin should be a bundle of narrow skills, app integrations, MCP/CLI tools, write policy, eval cases and update loop, not a list of generic capabilities.
- The Save workflows as skills and Create a CLI Codex can use pages show the promotion path: a working thread or command surface first becomes a skill, then can be packaged as a plugin.
- Follow a goal adds a durable long-running contract: objective, verifiable stop condition, checkpoints, progress log, status inspection, pause/resume/clear.
- UI, native and game use cases require runtime evidence such as Playwright, simulator screenshots, logs, build output, deployment URL or gameplay checks.
- Operations and collaboration use cases require staged drafts: the agent prepares a reviewable artifact first and does not write to external systems without approval.

## How To Use These Results

- Claims from Context7 are treated as `official` only when the underlying source is `developers.openai.com`, `github.com/openai/...` or `openai.github.io/...`.
- Recipe-like fragments and architecture examples can move into playbooks as `official + experiment` because local integration still needs verification.
- If Context7 and the current official page disagree, verify the official page directly before changing core instructions.

## Addendum 2026-05-23: Engineering Standards Layer

| Library ID | Purpose | Extracted Signal |
| --- | --- | --- |
| `/feature-sliced/documentation` | Feature-Sliced Design | Layer import rule, public API rule on slices, controlled cross-slice exports |
| `/storybookjs/storybook` | Storybook | `autodocs` tag, MDX Doc Blocks, component documentation pattern |
| `/oai/openapi-specification/3.1.1` | OpenAPI Specification | Security Scheme Object and supported scheme types |

Findings:

- FSD guidance should be used in Product-Agent OS only as a UI/default architecture boundary, not as a universal backend standard.
- Storybook supports docs-as-code for UI states, while accessibility and visual checks remain project-specific gates.
- OpenAPI findings support machine-readable API contracts and security scheme documentation, but source-of-truth status requires a direct OpenAPI Specification or OpenAPI Initiative link.
- Direct web verification on 2026-05-23 found the latest published OpenAPI Specification was v3.2.0. The v3.1.1 Context7 query remains a compatibility/security-scheme reference, while core guidance should cite v3.2.0 as the current source.

## Addendum 2026-05-23: Documentation Tooling Research

| Library ID | Purpose | Extracted Signal |
| --- | --- | --- |
| `/websites/docusaurus_io` | Docusaurus | Static documentation site generator, React/MDX orientation, versioned docs structure, versioning cost warning |
| `/mkdocs/mkdocs` | MkDocs | Markdown source, YAML config, static HTML build, dev server/live reload, themes/plugins/Markdown extensions |
| `/storybookjs/storybook` | Storybook | Autodocs through `tags: ['autodocs']`, MDX Doc Blocks, a11y parameters and component documentation pattern |

Findings:

- Docusaurus fits React/MDX-heavy product docs, public docs, i18n and versioned documentation, but versioning increases maintenance cost and should not be enabled automatically.
- MkDocs remains a strong default for small and medium repos: Markdown plus one YAML config and strict static build map well to Product-Agent OS docs-as-code gates.
- Storybook is both component documentation and a verification surface: stories define component states, Autodocs generates baseline docs, and a11y checks can become CI proposals.
- Context7 tooling findings do not replace primary documentation links in `docs/sources/registry.md`; the registry must store official URLs and `checked_at`.

## Addendum 2026-05-24: Large-Project Methodology Section Research

| Library ID | Purpose | Extracted Signal |
| --- | --- | --- |
| `/feature-sliced/documentation` | Feature-Sliced Design | Layer import rule, slices as business-domain partitions, public API rule and controlled cross-slice exports |
| `/storybookjs/storybook` | Storybook | `tags: ['autodocs']`, `!autodocs`, MDX documentation templates and Doc Blocks |
| `/websites/spec_openapis_oas_v3_2_0` | OpenAPI Specification 3.2.0 | Components Object, reusable schemas/responses/parameters/examples/security schemes and security scheme examples |

Findings:

- FSD should remain frontend-specific and conditional: useful for growing UI architecture, but not forced onto backend, database, API, LLM or simple MVP work.
- Storybook should be documented as component documentation and verification surface.
- OpenAPI 3.2.0 should be the current HTTP API contract source for new API documentation guidance, while project tooling can still require compatibility notes for older versions.
- Context7 was used as a retrieval layer only. The `docs/methodologies/` pages cite primary sources directly and keep source-backed claims in `docs/sources/registry.md`.

## Addendum 2026-05-24: API Integrations Methodology Research

| Library ID | Purpose | Extracted Signal |
| --- | --- | --- |
| `/websites/spec_openapis_oas_v3_2_0` | OpenAPI Specification 3.2.0 | Operation Object, Components Object, reusable schemas/responses/parameters/examples/security schemes, operation-level security and deprecation fields |
| `/asyncapi/spec` | AsyncAPI Specification | Channels, operations, messages, payload schemas, headers, correlation IDs, examples, reusable components and security schemes |
| `/websites/pact_io` | Pact | Consumer-driven contract testing, provider verification, contract-by-example and how Pact complements OpenAPI/AsyncAPI schema contracts |

Findings:

- OpenAPI should be treated as the HTTP API source of truth when an HTTP API has human or machine consumers; generated docs render the contract, not replace it.
- AsyncAPI should be used or explicitly considered for message-driven APIs, events and webhooks when channel/message semantics matter.
- Pact complements OpenAPI and AsyncAPI: schema contracts define possible shapes, while consumer-driven contracts capture expectations actually used by consumers.
- API & Integrations methodology needs gates for contract source, consumer map, compatibility classification, auth/security review, error examples, event delivery semantics, generated client manifest and external write approval.

## Addendum 2026-05-24: Backend Methodology Research

| Library ID | Purpose | Extracted Signal |
| --- | --- | --- |
| `/websites/12factor_net` | The Twelve-Factor App | Codebase, dependencies, config, backing services, build-release-run, stateless processes, port binding, concurrency, disposability, dev/prod parity, logs and admin processes |
| `/websites/opentelemetry_io` | OpenTelemetry | Traces, metrics, logs, baggage, context propagation, instrumentation, collector and telemetry pipeline concepts |
| `/websites/kubernetes_io` | Kubernetes | Liveness, readiness and startup probes, including the distinction between process liveness and traffic readiness |

Findings:

- Backend methodology should require runtime behavior documentation, not only module/code structure.
- Twelve-Factor gives compact default vocabulary for config, dependencies, backing services, process model, logs, disposability and dev/prod parity.
- OpenTelemetry should be the default cross-stack vocabulary for backend observability contracts.
- Kubernetes probe semantics are useful as a production-readiness model even outside Kubernetes.
- Backend readiness gates should cover service boundary, runtime behavior, dependency failure matrix, observability, SLO/gap, health probes, security review, data consistency, config/secrets and rollback.

## Addendum 2026-05-24: Database Methodology Research

| Library ID | Purpose | Extracted Signal |
| --- | --- | --- |
| `/websites/postgresql` | PostgreSQL official documentation | Transaction isolation, constraints, indexes, `EXPLAIN`, backup/restore and official documentation scope |

Finding:

- Database methodology needs explicit migration, rollback, restore, indexing, data quality and privacy gates. Generated schema documentation is useful, but it must never expose secrets or production connection details.
