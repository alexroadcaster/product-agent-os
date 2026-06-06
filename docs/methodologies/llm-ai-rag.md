# LLM / AI / RAG

Source status: `official + vendor documentation + tool-assisted + experiment`

Источники: [OpenAI Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses), [OpenAI text generation](https://developers.openai.com/api/docs/guides/text), [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling), [OpenAI tools guide](https://developers.openai.com/api/docs/guides/tools), [OpenAI file search](https://developers.openai.com/api/docs/guides/tools-file-search), [OpenAI retrieval](https://developers.openai.com/api/docs/guides/retrieval), [OpenAI embeddings](https://developers.openai.com/api/docs/guides/embeddings), [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices), [OpenAI production best practices](https://developers.openai.com/api/docs/guides/production-best-practices), [OpenAI reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices), [Codex: Add evals to your AI application](https://developers.openai.com/codex/use-cases/ai-app-evals), [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents), [Agents SDK orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration), [Agents SDK guardrails](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals), [Agents SDK tracing](https://developers.openai.com/api/docs/guides/agents/integrations-observability), [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals), [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices), [Promptfoo](https://www.promptfoo.dev/docs/intro/), [Promptfoo expected outputs](https://www.promptfoo.dev/docs/configuration/expected-outputs/), [Ragas metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/), [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/), [Context7 research](../sources/context7-research.md), [research dossier](../sources/methodology-research/llm-ai-rag.md).

## Deep research цель

LLM / AI / RAG слой описывает, как проектировать, менять и проверять AI behavior: prompts, models, structured outputs, tools, retrieval, grounding, agents, guardrails, tracing, safety, latency, cost and regression risk.

Главный принцип: AI behavior нельзя менять “на ощущениях”. До изменения нужен baseline, после изменения нужен eval/runtime evidence, а для RAG и tools отдельно проверяются source grounding, retrieval quality, tool permissions и safety boundaries.

## Поддержанные факты

- OpenAI Responses API, text generation, prompt engineering, Structured Outputs, function calling, file search, retrieval and embeddings provide the primary OpenAI vocabulary for AI application behavior.
- OpenAI evaluation guidance and Codex AI app evals recommend baseline evals, datasets, graders, thresholds and rerun evidence before behavior-changing prompt/model/retrieval/tool changes merge.
- OpenAI Agents SDK docs separate agents, tools, handoffs, guardrails, tracing, human review and evals for code-owned agent applications.
- OpenAI safety and production best practices support safety, privacy, monitoring, rate limits, latency/cost and deployment readiness concerns.
- Promptfoo supports declarative LLM app evaluation with expected-output assertions; Ragas provides RAG quality metrics such as faithfulness and context precision/recall.
- OpenTelemetry GenAI semantic conventions give observability vocabulary for model calls, prompts, completions, tool calls and token/cost signals.

## Assumptions

- OpenAI is the primary source of truth for OpenAI APIs, Codex, Agents SDK, model behavior, tools, safety and production guidance; Context7 is useful only when the underlying source is official or vendor-owned.
- Product-Agent OS should support AI work without forcing one eval runner. Promptfoo, pytest/Jest app-backed evals, OpenAI eval guidance and Ragas cover different risk profiles.
- Agents SDK should be introduced when code-owned agent workflows need tools, handoffs, guardrails, sessions, tracing or evals; simple AI features can remain single-call or single-agent.
- RAG quality requires separate retrieval and answer evaluation. A grounded final answer can still fail if retrieval misses fresh, authoritative or permitted sources.
- Tool/function calling must be treated as product capability, not prompt decoration: permissions, side effects, idempotency, retries, errors and approvals are part of the contract.

## Инструкции применения на проекте

1. Классифицировать изменение: prompt, model, output schema, tool, RAG corpus, retrieval config, agent routing, guardrail, eval, latency/cost или safety behavior.
2. Зафиксировать user-visible AI behavior promise: что функция обещает пользователю, где должна отказаться, где должна попросить уточнение и какие ошибки недопустимы.
3. Перед prompt/model/retrieval/tool/agent change создать или найти baseline eval.
4. По возможности проверять application path, который видит пользователь, а не только raw model prompt.
5. Менять один фактор за раз, если цель - понять причинность. Если меняются сразу prompt, model и retrieval, это migration, а не простая итерация.
6. Prompt рассматривать как versioned contract: role, goal, context, constraints, uncertainty policy, tools, output format, examples, verification route.
7. Model decision фиксировать явно: model/snapshot or alias policy, reasoning effort, modality, context window, tool support, latency/cost, fallback.
8. Structured Outputs использовать, когда output идет в code, UI, API, eval grader или другой agent. Схема должна иметь refusal/fallback/parser failure behavior.
9. Tool/function calling документировать как capability contract: schema, permissions, side effects, idempotency, retries, errors and approval boundary.
10. Для RAG фиксировать corpus authority, freshness, ingestion path, chunking, embeddings, vector store, filters, top-k/reranking, citations and unsupported-claim behavior.
11. RAG quality делить на retrieval quality и answer quality: отдельно смотреть missing chunks, irrelevant chunks, faithfulness, answer relevance and citation correctness.
12. Agent workflow начинать с минимального single-agent or manager pattern. Handoffs добавлять только когда specialist должен владеть следующим ответом.
13. Traces использовать для debugging отдельного run; datasets/eval runs - когда поведение стабилизировано и нужно repeatability.
14. Safety/red-team cases добавлять для prompt injection, sensitive content, private data, risky tools, minors, cybersecurity and irreversible side effects.
15. Latency/cost считать product constraints: timeout, retry, caching, background/batch mode, smaller model fallback, budget threshold.
16. Datasets, prompts, examples, fixtures, traces и screenshots не должны содержать secrets, credentials, raw private chats или private customer data.
17. Quality improvement claim требует свежего eval evidence или explicit inspection-only gap.

## Применяемые методологии разработки

| Методология | Когда применять | Как выглядит в проекте |
| --- | --- | --- |
| Eval-driven AI development | AI output quality can regress | Baseline, dataset, rubric, threshold, rerun command, failed cases. |
| Prompt-as-contract | Prompt controls product behavior | Versioned prompt with role, goal, context, constraints, uncertainty and output contract. |
| Model selection by task/risk | Model/provider/reasoning changes | Decision record with quality, latency, cost, modality, tool support and fallback. |
| One-factor-at-a-time iteration | Debugging AI behavior | Prompt/model/RAG/tool change log isolates one variable. |
| Structured-output-first integration | Output feeds code/UI/API/agent | JSON Schema, parser validation, refusal and fallback path. |
| Tool-contract development | Model can call tools or trigger side effects | Tool schema, permissions, idempotency, approval boundary and tool-call evals. |
| RAG source-grounding | Answers depend on external knowledge | Source inventory, retrieval config, citations, grounding rubric and unsupported-claim handling. |
| Retrieval quality evaluation | Search/retrieval affects answer quality | Context precision/recall, failed queries, source coverage and freshness checks. |
| Agent workflow design | Multi-step work, tools, handoffs or state | Smallest useful agent workflow, trace evidence, explicit owner of final answer. |
| Guardrails and human review | User input or tools can cause harm | Input/output/tool guardrails, red-team cases, approval for risky actions. |
| Observability-driven AI debugging | Behavior is hard to reproduce | Trace IDs, prompts, model settings, tool calls, retrieved context, latency/cost, redaction notes. |
| Cost/latency governance | User-facing or high-volume AI feature | Budget per workflow, timeout, retry, cache/background/fallback plan. |
| Dataset governance | Evals or RAG use examples/documents | Synthetic/sanitized data, source policy, no secrets, owner and version. |

## Инструменты, артефакты и стандарты документирования

- `ai-behavior-spec.md`: user-visible promise, accepted outputs, fallback/refusal behavior, risk.
- `prompt-contract.md`: prompt version, variables, instructions, examples, tools, output format.
- `model-decision-record.md`: model/snapshot, reasoning effort, modality, context, tool support, latency/cost, fallback.
- `ai-eval-spec.md`: objective, dataset, rubric, threshold, rerun command, owner.
- `eval-run-report.md`: baseline/current score, passing/failing cases, diff, residual risk.
- `ai-dataset-manifest.md`: source, privacy class, synthetic/sanitized status, owner, retention.
- `structured-output-schema.md`: JSON Schema or typed contract, strictness, refusal/fallback, parser behavior.
- `ai-tool-contract.md`: name, purpose, schema, permissions, side effects, idempotency, approval policy.
- `rag-source-inventory.md`: corpus, authority, freshness, owner, ingestion path, exclusions.
- `rag-retrieval-config.md`: chunking, embeddings, vector store, filters, top-k, reranker, metadata, latency.
- `rag-eval-report.md`: context precision/recall, faithfulness, answer relevance, failed queries, source gaps.
- `grounding-rubric.md`: citation/source rules, unsupported claim handling, conflict handling, abstention policy.
- `agent-workflow-map.md`: agents, tools, handoffs, state, final-answer owner, stop conditions.
- `guardrail-matrix.md`: input/output/tool guardrails, human approvals, red-team cases, fallback.
- `trace-evidence-packet.md`: trace IDs, model/tool calls, retrieved context, latency, cost, errors, redaction.
- `ai-cost-latency-budget.md`: tokens, cache strategy, timeout, retry, batch/background mode, fallback, alert.

## Что еще включить в deep research

- Stack-specific eval templates: Promptfoo, pytest/Jest app-backed evals, OpenAI Evals, Ragas, LangSmith.
- RAG metrics policy by risk tier: context precision, context recall, faithfulness, answer relevance, citation correctness, freshness.
- Model migration policy: alias vs snapshot, compatibility checks, prompt migration, rollback.
- Agent trace schema: Agents SDK traces vs OpenTelemetry GenAI spans vs tool-specific reports.
- Human approval representation across Codex App, CLI, Agents SDK, MCP and external workflow tools.
- Safety profile by product domain: healthcare, finance, minors, cybersecurity, legal, customer support, internal automation.
- Dataset lifecycle: source review, synthetic generation, deduplication, stale-case pruning, privacy review.
- AI incident workflow: failed eval, hallucination report, unsafe output, tool misuse, data exposure.

## Product-Agent OS routing

- `workspace-discovery-auditor` detects OpenAI SDK, Agents SDK, Promptfoo, Ragas, vector stores, prompts, evals, RAG corpora, tools, traces and safety signals.
- `requirements-author` records AI behavior promise, refusal/fallback behavior, dataset policy and acceptance scenarios.
- `implementation-planner` blocks prompt/model/RAG/tool/agent changes when baseline eval, model decision, tool contract or RAG source inventory is missing.
- `test-eval-designer` defines eval dataset, rubric, threshold, rerun command, app-backed target and failure review path.
- `risk-reviewer` handles safety, private data, prompt injection, tool side effects, cost/latency and unsupported claims.
- `learning-loop-maintainer` records failed cases, prompt/model lessons, dataset updates, trace evidence and next eval candidates.

## Candidate readiness gates

- `ai_behavior_spec_present`: user-visible promise, accepted behavior and fallback/refusal behavior are present.
- `ai_baseline_eval_present`: prompt/model/RAG/tool/agent changes have baseline eval or explicit baseline gap.
- `ai_eval_rerun_command_present`: eval-governed change has local/CI command and threshold.
- `ai_dataset_governance_present`: eval/RAG dataset has source, privacy, synthetic/sanitized status and owner.
- `ai_prompt_contract_present`: production prompt includes version, variables, constraints, output format and uncertainty policy.
- `ai_model_decision_record_present`: model choice includes quality, latency, cost, context, modality, tool support and fallback.
- `ai_structured_output_contract_present`: downstream structured output has schema, strictness, refusal/fallback and parser behavior.
- `ai_tool_contract_present`: tool/function/MCP capability has schema, permissions, side effects, idempotency and errors.
- `ai_human_approval_boundary_present`: risky writes, shell, money, data exposure or irreversible actions have approval route.
- `rag_source_inventory_present`: RAG corpus has authority, freshness, owner, ingestion path and exclusions.
- `rag_retrieval_config_present`: chunking, embeddings, vector store, filters, top-k/reranking and metadata are documented.
- `rag_grounding_eval_present`: context precision/recall, faithfulness, answer relevance or grounding rubric exists.
- `agent_workflow_trace_present`: agent/tool/handoff routing change has trace, run log or equivalent runtime evidence.
- `ai_safety_review_present`: sensitive domains, user input, prompt injection, private data or risky tools have safety/red-team review.
- `ai_cost_latency_budget_present`: user-facing/high-volume AI feature has budget, timeout, cache or fallback policy.
- `ai_no_private_data_in_fixtures_present`: prompts/evals/RAG/examples/traces contain no secrets or private data.

## Candidate eval fields

- User-visible AI behavior promise is present.
- Baseline eval exists before prompt/model/RAG/tool/agent change or baseline gap is explicit.
- Eval rerun command, threshold and owner are recorded.
- Dataset source, privacy class, synthetic/sanitized status and retention are documented.
- Prompt contract includes role, goal, variables, constraints, output format and uncertainty policy.
- Model decision includes model/snapshot or alias policy, reasoning, quality, latency, cost and fallback.
- Structured output contract includes schema, strictness, refusal/fallback and parser behavior.
- Tool contract includes schema, permissions, side effects, idempotency, retries and errors.
- RAG eval separates retrieval failure from answer generation failure.
- Safety/red-team cases cover prompt injection, private data and risky tool actions.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| OpenAI application API | Responses API | Default vocabulary for OpenAI model/tool interactions in new apps. |
| Prompt and output contracts | Structured Outputs, function calling | Use when output feeds code, UI, API, eval grader or another agent. |
| RAG | File search, retrieval, embeddings, vector store stack | Needs source inventory, retrieval config, grounding eval and deletion/privacy path. |
| Agent workflows | Agents SDK orchestration and handoffs | Use when code-owned app needs tools, handoffs, guardrails, sessions and tracing. |
| Evals | OpenAI eval guidance, Codex AI app evals, Promptfoo, Ragas | Select by app path, AI behavior type and RAG/tool risk. |
| Promptfoo config | `promptfoo.yaml`, `promptfooconfig.yaml` | Discovery signals for declarative LLM eval suites. |
| Agent handoff | `agent-handoff-contract.md` | Handoff owner, inputs, output schema, stop condition and trace evidence. |
| Observability | OpenTelemetry GenAI semantic conventions, Agents SDK tracing | Trace IDs, prompts, model settings, tool calls, latency/cost and redaction notes. |
| Safety | OpenAI safety best practices, guardrails, red-team cases | Prompt injection, data leakage, tool misuse and human approval boundaries. |

## Проверки

- Baseline eval exists before AI behavior change.
- Eval dataset policy excludes secrets, credentials, raw private chats and private customer data.
- Rerun command, threshold and owner are explicit.
- Prompt contract and model decision record are updated when prompt/model changes.
- Structured output schema is validated with success and failure cases.
- Tool call tests cover tool selection, arguments, errors and permission boundary.
- RAG eval separates retrieval failures from generation failures.
- Grounded answers cite supported sources or refuse/flag unsupported claims.
- Agent workflow has trace evidence and handoff/ownership clarity.
- Safety/red-team cases cover prompt injection, private data and risky actions.
- Cost/latency budget is measured or explicitly marked as unavailable.

## Типовые сбои

- Manual spot checks are treated as eval evidence.
- Prompt, model and retrieval are changed together without migration framing.
- RAG answer quality is judged without source inspection.
- Retrieval eval misses missing-source, stale-source or irrelevant-chunk cases.
- Eval tests raw prompt while production behavior depends on tools, retrieval, state or UI transforms.
- Structured output schema exists but parser/refusal/fallback behavior is undocumented.
- Tool schema exists but permissions, idempotency and side effects are not reviewed.
- Multi-agent workflow is introduced before a simpler baseline fails.
- Guardrails ignore prompt injection, tool misuse or private data exposure.
- Eval dataset leaks private data or becomes stale.
- AI feature ships without latency/cost budget.

## Unsupported claims not adopted

- "Manual spot checks are enough for AI quality." Not adopted; behavior-changing prompt/model/RAG/tool/agent work needs baseline and rerun evidence or an explicit gap.
- "Multi-agent architecture is always better." Not adopted; smallest useful workflow remains the default until complexity justifies handoffs.
- "Citations alone prove RAG correctness." Not adopted; retrieval coverage, source authority, freshness, faithfulness and unsupported-claim handling are separate checks.
- "A tool schema is enough for safe tool use." Not adopted; permissions, side effects, idempotency, approval boundaries and failure behavior are required.
- "Model upgrade automatically improves product quality." Not adopted; model changes require eval comparison, latency/cost review and rollback policy.

## Open questions for future implementation

- Which eval templates should ship first: Promptfoo, pytest/Jest app-backed evals, OpenAI Evals, Ragas or framework-neutral?
- Which RAG metrics are required by risk tier: context precision, recall, faithfulness, answer relevance, citation correctness or freshness?
- How should model alias versus snapshot policy be represented for rollback and reproducibility?
- Should Agents SDK trace schema and OpenTelemetry GenAI spans be connected in one evidence packet?
- How should human approvals be represented consistently across Codex App, CLI, Agents SDK, MCP and external workflow tools?
- What AI incident workflow should capture hallucination reports, unsafe output, tool misuse and data exposure?
