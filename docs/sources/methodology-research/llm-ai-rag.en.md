# LLM / AI / RAG Methodology Research

Source status: `official + vendor documentation + tool-assisted`

Research date: `2026-05-24`

Target methodology page: [../../methodologies/llm-ai-rag.md](../../methodologies/llm-ai-rag.md)

Target Product-Agent OS behavior: detect AI behavior changes, require a baseline before prompt/model/retrieval/tool changes, route RAG and agent work through source, eval, safety, tool-permission, cost/latency and tracing gates, and block completion claims without current eval or runtime evidence.

## Scope

This dossier covers LLM features, prompts, model selection, structured outputs, function/tool calling, Retrieval-Augmented Generation (RAG), vector stores, embeddings, agents, handoffs, guardrails, tracing, evals, red-team/safety checks, cost/latency budgets and AI behavior regression management.

It does not mandate OpenAI-only architecture, RAG for every feature, multi-agent orchestration, fine-tuning, Promptfoo, Ragas or OpenTelemetry. Those are conditional tools selected by behavior risk, product need, data sensitivity and existing stack.

## Supported facts

- OpenAI documentation recommends the Responses API for new text-generation projects and describes it as a unified interface for agent-like applications with built-in tools, multi-turn interactions, multimodal input and stateful context.
- OpenAI prompt guidance recommends pinning production applications to specific model snapshots for consistency and building evals to monitor prompt behavior during iteration and model upgrades.
- Structured Outputs constrain model responses to developer-supplied JSON Schema contracts and are recommended over JSON mode when possible.
- Function calling, also called tool calling, connects models to external systems and follows a multi-step flow: define tools, receive tool call, execute application-side code, send tool output back, then receive final response or more tool calls.
- OpenAI file search lets models search uploaded files through vector stores using semantic and keyword search; retrieval quality, result limits, token usage and latency are design tradeoffs.
- OpenAI embeddings measure relatedness of text strings and are commonly used for search, clustering, recommendations, anomaly detection and classification.
- OpenAI Codex eval guidance frames evals as systematic tests for AI application scenarios and recommends evaluating the application path users hit where possible, not only the raw model prompt.
- OpenAI evaluation guidance identifies instruction following, functional correctness, tool selection and tool argument precision as evaluation areas for agent workflows.
- OpenAI Agents SDK guidance frames agents as applications that plan, call tools, collaborate across specialists and keep enough state for multi-step work.
- Agents SDK guardrail guidance separates input, output and tool guardrails, and uses human review for sensitive side effects such as cancellations, edits, shell commands and sensitive MCP actions.
- Agents SDK tracing records model calls, tool calls, handoffs, guardrails and custom spans, and can feed higher-signal examples into systematic agent evaluation.
- OpenAI agent evaluation guidance recommends traces while debugging behavior, then datasets and eval runs once “good” behavior is known.
- OpenAI safety guidance recommends moderation, human oversight and adversarial testing for applications exposed to user input.
- Promptfoo is now part of OpenAI and is an open-source CLI/library for evaluating and red-teaming LLM apps, with declarative tests, assertions, latency/cost checks, RAG metrics and CI/CD usage.
- Ragas documents RAG and agentic workflow metrics such as context precision, context recall, response relevancy, faithfulness, tool call accuracy and agent goal accuracy.
- OpenTelemetry GenAI semantic conventions are still in development but define shared signals for model spans, agent spans, events, exceptions and metrics for generative AI systems.

## Methodologies

| Methodology | When to apply | Project-level behavior |
| --- | --- | --- |
| Eval-driven AI development | AI output quality can regress | Baseline first, one focused change, rerun eval, inspect failures, log residual risk. |
| Prompt-as-contract | Prompt controls product behavior | Versioned prompt with role, goal, context, constraints, uncertainty policy, tools, output format and verification. |
| Model selection by task/risk | Choosing or changing models | Record quality, latency, cost, modality, context window, tool support and reasoning needs. |
| One-factor-at-a-time iteration | Debugging prompt/model/RAG behavior | Change one variable per run unless explicitly doing a compatibility migration. |
| Structured-output-first integration | Output feeds code/UI/API | JSON Schema or equivalent contract, refusal/fallback path, parser validation and negative cases. |
| Tool-contract development | Model can call tools or trigger side effects | Tool schema, permissions, idempotency, approval boundary, error handling and tool-call evals. |
| RAG source-grounding | Answers depend on external knowledge | Source inventory, chunking, retrieval config, citations, unsupported-claim policy and grounding rubric. |
| Retrieval quality evaluation | Search/retrieval affects answer quality | Context precision/recall, faithfulness, answer relevance, failed queries and source coverage. |
| Agent workflow design | Multi-step work, tools, handoffs or state | Start simple, name owner, trace runs, add handoffs only when specialist ownership is needed. |
| Guardrails and human review | User input or tools can cause harm | Input/output/tool guardrails, red-team cases, approval for risky or irreversible actions. |
| Observability-driven AI debugging | AI behavior is hard to reproduce | Traces, spans, prompts, model settings, tool calls, retrieved context, latency/cost and redaction notes. |
| Cost/latency budget governance | AI feature is user-facing or high volume | Budget per workflow, token/cache strategy, model fallback, timeout and batching/background plan. |
| Dataset governance | Evals or RAG use examples/documents | Synthetic/sanitized data, no secrets, no raw private chats, versioned datasets and owner review. |

## Documentation artifacts and standards

| Artifact | Purpose | Candidate source/tool |
| --- | --- | --- |
| AI behavior spec | User-visible promise, accepted outputs, refusal/fallback behavior and risk. | `ai-behavior-spec.md` |
| Prompt contract | Prompt version, variables, instructions, examples, tool list and output format. | `prompt-contract.md` |
| Model decision record | Model, snapshot/alias, reasoning effort, modality, tool support, latency/cost and fallback. | ADR, `model-decision-record.md` |
| Eval spec | Objective, dataset, rubric, thresholds, command, owner and rerun cadence. | `ai-eval-spec.md`, `EVALS.md` |
| Eval run report | Baseline/current score, passing/failing cases, diff, regression and residual risk. | `eval-run-report.md` |
| Dataset manifest | Source, privacy class, synthetic/sanitized status, owner, retention and update policy. | `ai-dataset-manifest.md` |
| Structured output schema | JSON Schema or typed contract, strictness, refusal path and parser behavior. | OpenAI Structured Outputs, JSON Schema |
| Tool contract | Name, purpose, schema, permissions, side effects, idempotency and approval policy. | OpenAI function calling, Agents SDK guardrails |
| RAG source inventory | Corpus, authority, freshness, owner, ingestion path, exclusions and source policy. | `rag-source-inventory.md` |
| Retrieval config record | Chunking, embeddings, vector store, filters, top-k, reranker, metadata and latency budget. | File search/retrieval docs, vector DB docs |
| RAG eval report | Context precision/recall, faithfulness, answer relevance, failed queries and source gaps. | Ragas, Promptfoo, custom evals |
| Grounding rubric | Citation/source rules, unsupported claim handling, conflict handling and abstention policy. | `grounding-rubric.md` |
| Agent workflow map | Agents, tools, handoffs, state, owner of final answer and stop conditions. | Agents SDK, Mermaid |
| Guardrail matrix | Input/output/tool guardrails, human approvals, red-team cases and fallback behavior. | Safety best practices, Agents SDK guardrails |
| Trace evidence packet | Trace IDs, model/tool calls, retrieved context, latency, cost, errors and redaction notes. | Agents SDK tracing, OpenTelemetry |
| Cost/latency budget | Expected tokens, cache strategy, timeout, model fallback, batch/background mode and alert. | Production best practices |

## Project application instructions

1. Classify the change: prompt, model, output schema, tool, RAG corpus, retrieval config, agent routing, guardrail, eval, latency/cost or safety behavior.
2. Record the user-visible AI behavior promise before editing prompts or model settings.
3. Create or identify a baseline eval before changing prompt, model, retrieval, tool surface or agent routing.
4. Prefer app-backed evals that exercise the path users hit. Raw prompt evals are useful only when the prompt is the real product boundary.
5. Change one factor at a time for quality debugging. If multiple factors must change together, mark it as a migration and expand regression coverage.
6. Pin production model behavior deliberately: model ID/snapshot or approved alias policy, reasoning effort, temperature-equivalent parameters, tool support and fallback path.
7. Treat prompts as versioned contracts. Every production prompt should name role, goal, context, constraints, uncertainty behavior, tool policy, output contract and verification route.
8. Use Structured Outputs when model output feeds code, UI, API payloads, eval graders or downstream agents.
9. For tools, document schema, side effects, permissions, retries, idempotency, error handling and whether human approval is required.
10. For RAG, document corpus authority, freshness, ingestion path, chunking, embeddings, filters, top-k/reranking, citation rules and unsupported-claim behavior.
11. Split RAG evaluation into retrieval quality and answer quality. A good answer cannot compensate for consistently missing source chunks.
12. Start agent workflows with the smallest single-agent or manager pattern that can pass evals. Add handoffs only when a specialist needs to own the next response.
13. Use traces while debugging individual runs; move to datasets and repeatable eval runs when behavior stabilizes.
14. Add safety and red-team cases for user input, prompt injection, sensitive content, private data, tool misuse and irreversible side effects.
15. Track latency and cost as product constraints, not afterthoughts. Include timeout, retry, batching/background mode or smaller-model fallback where needed.
16. Keep eval datasets, prompts, fixtures, traces and screenshots free of secrets, private customer data, raw private chat logs and credentials.
17. Do not claim AI quality improvement without current eval evidence or an explicit inspection-only gap.

## Product-Agent OS candidate rules

### Discovery signals

- Directories: `prompts/`, `evals/`, `rag/`, `retrieval/`, `vector/`, `agents/`, `tools/`, `guardrails/`, `datasets/`, `fixtures/`, `benchmarks/`
- Files: `promptfooconfig.yaml`, `promptfoo.yaml`, `EVALS.md`, `*.prompt.*`, `*.eval.*`, `openai.*`, `agents.*`, `vector_store.*`, `embeddings.*`, `ragas.*`, `langsmith.*`
- Terms: prompt, model, reasoning, eval, grader, rubric, hallucination, grounding, citation, retrieval, embeddings, vector store, chunking, rerank, tool call, function call, guardrail, handoff, trace, MCP, red team
- Dependency signals: OpenAI SDK, Agents SDK, Promptfoo, Ragas, LangChain, LlamaIndex, vector DB clients, OpenTelemetry, eval runners

### Readiness gates

| Gate | Trigger | Block condition |
| --- | --- | --- |
| `ai_behavior_spec_present` | New or changed AI feature | User-visible promise, accepted behavior or fallback/refusal behavior is missing. |
| `ai_baseline_eval_present` | Prompt/model/RAG/tool/agent behavior change | No baseline eval, seed cases or explicit baseline gap. |
| `ai_eval_rerun_command_present` | Any eval-governed AI change | No local or CI command and threshold. |
| `ai_dataset_governance_present` | Eval/RAG dataset or fixtures | Privacy/source/synthetic/sanitized status and owner are missing. |
| `ai_prompt_contract_present` | Production prompt change | Prompt role, goal, variables, constraints, output format or version is missing. |
| `ai_model_decision_record_present` | Model, snapshot, reasoning or provider change | Model choice, fallback, latency/cost and compatibility rationale are missing. |
| `ai_structured_output_contract_present` | Output feeds code/UI/API/agent | Schema, strictness, refusal/fallback and parser behavior are missing. |
| `ai_tool_contract_present` | Tool/function/MCP capability change | Tool schema, permissions, side effects, idempotency or error handling are missing. |
| `ai_human_approval_boundary_present` | Tool can write, delete, spend money, call shell, expose data or affect users | No approval route or staged-draft behavior. |
| `rag_source_inventory_present` | RAG/file search/vector store change | Corpus, authority, freshness, owner or exclusions are missing. |
| `rag_retrieval_config_present` | Chunking, embeddings, vector store, filters or reranking change | Retrieval config and metadata assumptions are missing. |
| `rag_grounding_eval_present` | Source-grounded answers | Context precision/recall, faithfulness, answer relevance or grounding rubric is missing. |
| `agent_workflow_trace_present` | Agent/tool/handoff routing change | No trace, run log or equivalent runtime evidence. |
| `ai_safety_review_present` | User input, sensitive domains, minors, cybersecurity, private data or tool side effects | No safety/red-team cases or risk reviewer route. |
| `ai_cost_latency_budget_present` | User-facing/high-volume AI feature | No budget, timeout, retry, cache or fallback policy. |
| `ai_no_private_data_in_fixtures_present` | Prompts/evals/RAG/examples/traces | Secrets, credentials, raw private chats or customer data are present or unclassified. |

### Candidate templates

- `ai-behavior-spec.md`
- `prompt-contract.md`
- `model-decision-record.md`
- `ai-eval-spec.md`
- `eval-run-report.md`
- `ai-dataset-manifest.md`
- `structured-output-schema.md`
- `ai-tool-contract.md`
- `rag-source-inventory.md`
- `rag-retrieval-config.md`
- `rag-eval-report.md`
- `grounding-rubric.md`
- `agent-workflow-map.md`
- `agent-handoff-contract.md`
- `guardrail-matrix.md`
- `trace-evidence-packet.md`
- `ai-cost-latency-budget.md`

### Candidate eval fields

- AI behavior promise is explicit and tied to product acceptance criteria.
- Baseline eval exists before prompt/model/retrieval/tool/agent changes.
- Eval command, dataset, rubric, thresholds and owner are documented.
- Prompt contract includes variables, constraints, output format and uncertainty policy.
- Model choice includes quality, latency, cost, context, modality and tool support.
- Structured output has schema, refusal handling and parser validation.
- Tool calls have schema, permission boundary, idempotency and error cases.
- RAG corpus has source authority, freshness and ingestion metadata.
- Retrieval eval separates missing context from bad generation.
- Grounded answers cite or reference sources and refuse/flag unsupported claims.
- Agent workflow has trace evidence and explicit handoff/ownership boundaries.
- Safety/red-team cases cover prompt injection, sensitive data and risky tools.
- Cost/latency budget is tracked for user-facing workflows.
- Fixtures and traces are free of secrets and private data.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| API foundation | OpenAI Responses API | Default for new OpenAI text/agent-like integrations; supports tools and state. |
| Output contracts | Structured Outputs, JSON Schema, Pydantic/Zod | Use when output feeds code, UI, API or eval graders. |
| Tool execution | Function calling, Agents SDK tools, MCP | Requires schema, permission, approval and error handling. |
| RAG hosted path | OpenAI File search and vector stores | Good when hosted retrieval fits corpus and governance needs. |
| Embeddings/vector search | OpenAI embeddings plus project vector DB | Use when custom retrieval, filters, hybrid search or ownership is needed. |
| Eval runner | Promptfoo, OpenAI Evals, custom app-backed tests | Choose by stack, CI fit, privacy and assertion style. |
| RAG evaluation | Ragas, Promptfoo RAG assertions, custom judged evals | Track retrieval and generation metrics separately. |
| Agent runtime | OpenAI Agents SDK | Use when the app owns orchestration, tool execution, approvals and state. |
| Observability | Agents SDK tracing, OpenTelemetry GenAI semantic conventions | Traces support debugging, audits and later eval dataset creation. |
| Safety | Moderation API, guardrails, red-team suites, human review | Select by domain risk and side-effect surface. |
| Cost/latency | Prompt caching, batching/background mode, model fallback | Treat as product constraints and release gates. |

## Failure modes

- Prompt/model/retrieval/tool changes ship without baseline eval.
- Manual spot checks are described as eval evidence.
- Prompt, model and retrieval settings change together, making causality unclear.
- RAG quality is judged only from final answers without inspecting retrieved context.
- Retrieval eval lacks failed queries, missing-source cases or freshness checks.
- Structured output schema exists but refusal/fallback/parser failure behavior is not documented.
- Tool schemas are present but permissions, idempotency, retries and error handling are missing.
- Agents are split into multiple specialists before a single-agent baseline is known to fail.
- Handoffs have vague ownership and no trace evidence.
- Guardrails block easy cases but miss prompt injection, tool misuse or private data exposure.
- Evals use raw prompts while the real product path includes tools, retrieval, state or UI transformations.
- Eval fixtures, traces or prompts contain secrets, credentials, raw private chat logs or customer data.
- Latency and cost are measured after release rather than used as design constraints.

## Open questions for deeper research

- Should Product-Agent OS generate Promptfoo-first eval templates or framework-neutral eval specs first?
- Which RAG metrics should be required by default: context precision/recall, faithfulness, answer relevance, source coverage, citation correctness or all by risk tier?
- How should the plugin detect AI behavior changes automatically from code and config diffs?
- Should model decision records live under architecture ADRs or under AI-specific docs?
- Which trace format should become the project default: Agents SDK traces, OpenTelemetry GenAI spans or tool-specific reports?
- How should human review approvals be represented across Codex App, CLI, Agents SDK and external workflow tools?
- What is the minimum eval threshold policy for model migration, prompt migration and RAG corpus updates?

## Sources

- [OpenAI: Migrate to the Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses)
- [OpenAI: Text generation](https://developers.openai.com/api/docs/guides/text)
- [OpenAI: Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [OpenAI: Reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices)
- [OpenAI: Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [OpenAI: Function calling](https://developers.openai.com/api/docs/guides/function-calling)
- [OpenAI: Using tools](https://developers.openai.com/api/docs/guides/tools)
- [OpenAI: File search](https://developers.openai.com/api/docs/guides/tools-file-search)
- [OpenAI: Retrieval](https://developers.openai.com/api/docs/guides/retrieval)
- [OpenAI: Embeddings](https://developers.openai.com/api/docs/guides/embeddings)
- [OpenAI: Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Codex: Add evals to your AI application](https://developers.openai.com/codex/use-cases/ai-app-evals)
- [OpenAI: Agents SDK](https://developers.openai.com/api/docs/guides/agents)
- [OpenAI: Agents SDK guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
- [OpenAI: Agents SDK integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability)
- [OpenAI: Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)
- [OpenAI: Orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration)
- [OpenAI: Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [OpenAI: Production best practices](https://developers.openai.com/api/docs/guides/production-best-practices)
- [Promptfoo intro](https://www.promptfoo.dev/docs/intro/)
- [Promptfoo assertions and metrics](https://www.promptfoo.dev/docs/configuration/expected-outputs/)
- [Ragas available metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Context7 research](../context7-research.md)
