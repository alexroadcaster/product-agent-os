# Анализ Context7

Source status: `official + tool-assisted`

Дата анализа: **2026-05-14**.  
Канал анализа: Context7 documentation retrieval.

## Использованные библиотеки Context7

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/websites/developers_openai_codex` | Официальная документация Codex | Subagent prompting, skill metadata, granular approvals, Codex MCP multi-agent example |
| `/openai/openai-agents-python` | OpenAI Agents SDK for Python | Core primitives: `Agent`, tools, handoffs, guardrails, sessions, tracing, multi-agent patterns |
| `/websites/developers_openai_api` | OpenAI API documentation | Responses API, tool definitions, structured outputs, built-in tools, multimodal and stateful patterns |
| `/websites/developers_openai` | OpenAI Developers documentation | Prompt structure, prompt objects, prompt versioning, context sections, eval-linked iteration |
| `/openai/openai-cookbook` | OpenAI Cookbook | Hallucination guardrails, LLM-as-judge validation, RAG grounding, citation discipline |

## Новые выводы для базы знаний

### Codex

- Approval policy можно описывать более детально через granular config: `sandbox_approval`, `rules`, `mcp_elicitations`, `request_permissions`, `skill_approval`.
- Skill можно расширять `agents/openai.yaml`: UI metadata, invocation policy и dependencies, включая MCP tools.
- Для subagents официальный prompt pattern: явно попросить Codex создать одного agent на каждый пункт, дождаться всех результатов и затем сделать consolidated summary.
- Codex MCP можно использовать как execution backend внутри Agents SDK multi-agent системы, где специализированные agents вызывают Codex для работы с workspace.
- Custom agents могут иметь собственные `model`, `model_reasoning_effort`, `sandbox_mode`, MCP servers и skill config; если поля не заданы, они наследуются от parent session.
- Subagents наследуют sandbox/approval controls от parent workflow, а runtime overrides текущего turn применяются и к дочерним агентам.
- В Codex model guidance default для большинства задач - начинать с `gpt-5.5`, а для быстрых легких задач и subagents рассматривать `gpt-5.4-mini`.

### Agents SDK

- Agents SDK строится вокруг малого набора primitives: agents, tools, guardrails, handoffs, sessions и tracing.
- Есть две базовые схемы multi-agent orchestration: Manager pattern и Handoff pattern.
- Tools могут быть function tools, hosted tools, MCP tools или agents-as-tools.
- Sessions отвечают за conversation persistence, а tracing - за debugging, monitoring и анализ workflow.
- Для production workflows лучше задавать model явно: на уровне agent, run-level default или process fallback через `OPENAI_DEFAULT_MODEL`.
- Per-agent model подходит, когда specialist стабильно требует другой quality, latency или cost profile.

### Responses API

- Responses API является низкоуровневым unified interface для agent-like applications.
- Tools описываются как function, MCP, image generation и другие built-in tool types.
- Structured outputs через `text.format` с JSON Schema полезны для контрактов между агентами.
- Built-in tools и multi-turn state дополняют Agents SDK, когда нужен прямой API-level контроль.

### Prompt & Context Engineering

- Prompt лучше проектировать как контракт: role, goal, context, constraints, uncertainty policy, tools, output format и verification.
- OpenAI prompting guidance поддерживает versioned prompt objects, variables и eval-linked prompt iteration.
- Для hallucination reduction нужен не только prompt, а контур: grounded context, structured output, verifier/guardrail, evals and fallback behavior.
- Structured Outputs уменьшают format failures, но требуют fallback rules для несовместимого user input.
- Cookbook patterns полезны как практический слой: hallucination detector, LLM-as-judge, scoring factual accuracy, relevance, policy compliance and contextual coherence.

### Product-Agent Workflows

- Codex product work needs control-plane artifacts: requirements, plan, tests, evals, run log and PR evidence.
- OpenAI Codex best practices emphasize Ask Mode before Code Mode, `AGENTS.md` for durable context, worktrees for parallel live work, and automations only after a workflow is stable manually.
- Skills are the method layer; automations are the schedule layer; plugins are the distribution layer.
- Long-horizon tasks need scored loops: baseline, one focused change, rerun eval, inspect artifact, log result and continue until explicit thresholds.
- Production agents need model/tool/instruction foundations, guardrails, human intervention and incremental orchestration rather than immediate over-automation.
- Reasoning level должен зависеть от сложности: `low` для быстрых scoped tasks, `medium`/`high` для сложных changes/debugging, `xhigh` для long agentic reasoning-heavy tasks.
- Use cases показывают повторяющийся production pattern: structured inputs, explicit approval, smallest useful plan, runnable checks/evals, audit artifact, then skill or automation only after the workflow is stable.

### Codex Use Cases and plugin extraction

- Use cases index фактически задает taxonomy для plugin design: category, native platform, workflow family, team и task type.
- Большинство карточек use case можно разобрать в один контракт: outcome, best fit, inputs, skills/plugins, starter prompt, constraints, verification, related workflows.
- Для plugin важнее не список возможностей, а bundle из узких skills, app integrations, MCP/CLI tools, write policy, eval cases и update loop.
- Страницы Save workflows as skills и Create a CLI Codex can use показывают promotion path: рабочий thread или command surface сначала становится skill, а затем может быть packaged как plugin.
- Follow a goal добавляет durable long-running контракт: objective, verifiable stop condition, checkpoints, progress log, status inspection, pause/resume/clear.
- UI, native и game use cases требуют runtime evidence: Playwright, simulator screenshots, logs, `log stream`, build output, deployment URL или gameplay checks.
- Operations и collaboration use cases требуют staged drafts: агент сначала готовит reviewable artifact и не пишет во внешние systems без approval.

## Как использовать результаты

- Все утверждения из Context7, относящиеся к OpenAI, считаются `official`, если источник указывает на `developers.openai.com`, `github.com/openai/...` или `openai.github.io/...`.
- Фрагменты, похожие на recipe или пример архитектуры, переносить в playbooks как `official + experiment`, потому что локальная интеграция все равно требует проверки.
- Если Context7 и текущая официальная страница расходятся, проверять страницу напрямую перед изменением основной инструкции.

## Дополнение 2026-05-23: engineering standards layer

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/feature-sliced/documentation` | Feature-Sliced Design | Import rule on layers, public API rule on slices, controlled cross-slice exports |
| `/storybookjs/storybook` | Storybook | `autodocs` tag, MDX Doc Blocks, component documentation pattern |
| `/oai/openapi-specification/3.1.1` | OpenAPI Specification | Security Scheme Object and supported scheme types |

Выводы:

- FSD guidance можно переносить в Product-Agent OS только как UI/default architecture boundary, а не как универсальный backend standard.
- Storybook findings подтверждают docs-as-code подход для UI states, но accessibility и visual checks остаются project-specific gates.
- OpenAPI findings подтверждают machine-readable API contract и security scheme documentation, но source-of-truth status требует прямой ссылки на OpenAPI Specification или OpenAPI Initiative.
- Прямая web-сверка 2026-05-23 показала, что latest published OpenAPI Specification - v3.2.0. Context7-запрос по v3.1.1 оставлен как compatibility/security-scheme reference, но core guidance должен ссылаться на v3.2.0 как текущий источник.

## Дополнение 2026-05-23: documentation tooling research

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/websites/docusaurus_io` | Docusaurus | Static documentation site generator, React/MDX orientation, versioned docs structure, versioning cost warning |
| `/mkdocs/mkdocs` | MkDocs | Markdown source, YAML config, static HTML build, dev server/live reload, themes/plugins/Markdown extensions |
| `/storybookjs/storybook` | Storybook | Autodocs through `tags: ['autodocs']`, MDX Doc Blocks, a11y parameters and component documentation pattern |

Выводы:

- Docusaurus подходит как docs portal для React/MDX-heavy product docs, public docs, i18n и versioned documentation, но versioning повышает maintenance cost и не должен включаться автоматически.
- MkDocs остается сильным default для небольших и средних repos: Markdown + single YAML config + strict static build хорошо ложатся на Product-Agent OS docs-as-code gate.
- Storybook следует учитывать не только как UI docs, но и как verification surface: stories фиксируют component states, Autodocs превращает их в documentation, a11y checks могут стать CI proposal.
- Context7 findings по tooling не заменяют primary docs links в `docs/sources/registry.md`; registry должен хранить официальные URL и checked_at.

## Дополнение 2026-05-24: large-project methodology section research

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/feature-sliced/documentation` | Feature-Sliced Design | Layer import rule, slices as business-domain partitions, public API rule and controlled cross-slice exports |
| `/storybookjs/storybook` | Storybook | `tags: ['autodocs']`, `!autodocs`, MDX documentation templates and Doc Blocks |
| `/websites/spec_openapis_oas_v3_2_0` | OpenAPI Specification 3.2.0 | Components Object, reusable schemas/responses/parameters/examples/security schemes and security scheme examples |

Выводы:

- FSD should remain frontend-specific and conditional: it is useful for growing UI architecture, but the project should not force FSD folder structures onto backend, database, API, LLM or simple MVP work.
- Storybook should be documented as both component documentation and a verification surface: stories define component states, Autodocs generates baseline docs, and MDX/Doc Blocks add narrative guidance where automatic docs are insufficient.
- OpenAPI 3.2.0 should be the current HTTP API contract source for new API documentation guidance, while project-specific tooling may still require compatibility notes for older OpenAPI versions.
- Context7 was used as a retrieval layer only. The new `docs/methodologies/` pages cite primary sources directly and keep source-backed claims in `docs/sources/registry.md`.

## Дополнение 2026-05-24: API integrations methodology research

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/websites/spec_openapis_oas_v3_2_0` | OpenAPI Specification 3.2.0 | Operation Object, Components Object, reusable schemas/responses/parameters/examples/security schemes, operation-level security and deprecation fields |
| `/asyncapi/spec` | AsyncAPI Specification | Channels, operations, messages, payload schemas, headers, correlation IDs, examples, reusable components and security schemes |
| `/websites/pact_io` | Pact | Consumer-driven contract testing, provider verification, contract-by-example, and when Pact complements OpenAPI/AsyncAPI schema contracts |

Выводы:

- OpenAPI should be treated as the HTTP API source of truth when an HTTP API has human or machine consumers; generated docs are a rendering of the contract, not the contract itself.
- AsyncAPI should be used or explicitly considered for message-driven APIs, events and webhooks when channel/message semantics matter.
- Pact complements OpenAPI and AsyncAPI rather than replacing them: schema contracts define possible shapes, while consumer-driven contracts capture expectations actually used by consumers.
- API & Integrations methodology needs Product-Agent OS gates for contract source, consumer map, compatibility classification, auth/security review, error examples, event delivery semantics, generated client manifest and external write approval.

## Дополнение 2026-05-24: backend methodology research

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/websites/12factor_net` | The Twelve-Factor App | Codebase, dependencies, config, backing services, build-release-run, stateless processes, port binding, concurrency, disposability, dev/prod parity, logs and admin processes |
| `/websites/opentelemetry_io` | OpenTelemetry | Traces, metrics, logs, baggage, context propagation, instrumentation, collector and telemetry pipeline concepts |
| `/websites/kubernetes_io` | Kubernetes | Liveness, readiness and startup probes, including the distinction between a process being alive and being ready to receive traffic |

Выводы:

- Backend methodology should require runtime behavior documentation, not only module/code-structure documentation.
- Twelve-Factor gives a compact default vocabulary for config, dependencies, backing services, process model, logs, disposability and dev/prod parity.
- OpenTelemetry should become the default cross-stack vocabulary for backend observability contracts: traces, metrics, logs, context propagation, collector path and redaction notes.
- Kubernetes probe semantics are useful as a production-readiness model even when the final deployment target is not Kubernetes; Product-Agent OS should treat health checks as contracts with distinct liveness/readiness/startup meanings where applicable.
- Backend readiness gates should cover service boundary, runtime behavior, dependency failure matrix, observability, SLO/gap, health probes, security review, data consistency, config/secrets and rollback.

## Дополнение 2026-05-24: database methodology research

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/websites/postgresql` | PostgreSQL official documentation | Transaction isolation, constraints, indexes, `EXPLAIN`, backup/restore and official documentation scope |
| `/liquibase/liquibase-docs` | Liquibase documentation | Changelog/changeset structure, rollback sections, preconditions and CI/CD migration workflow examples |
| `/dbt-labs/docs.getdbt.com` | dbt documentation | Data tests, model contracts, model/source YAML documentation and data quality assertions |

Выводы:

- Database methodology should treat schema and data changes as production-risk work, not as local code edits.
- PostgreSQL findings support readiness gates for transaction boundary, constraint/index design, query-plan evidence and backup/restore evidence.
- Liquibase findings support migrations-as-code language: changelog, changeset, rollback, preconditions, contexts and labels.
- dbt findings support executable data quality and data contract guidance for analytical models and shared data products.
- Context7 findings are retrieval evidence only; the methodology page cites primary PostgreSQL, Liquibase, Flyway, dbt, Great Expectations, OpenLineage, NIST, Fowler and Prisma sources directly.

## Дополнение 2026-05-24: frontend methodology research

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/feature-sliced/documentation` | Feature-Sliced Design | Layer import rule, public API rule, slices as business-domain partitions, controlled cross-slice `@x` exports |
| `/storybookjs/storybook` | Storybook | `tags: ['autodocs']`, MDX/Doc Blocks, stories as documentation units, `play` interaction tests, accessibility parameters |
| `/websites/playwright_dev` | Playwright | `toHaveScreenshot()` visual comparisons, screenshot baseline stability constraints, Trace Viewer and trace capture for browser evidence |

Выводы:

- FSD remains a conditional frontend architecture methodology. Product-Agent OS should use it when UI scale and feature/business boundaries justify layers, slices and public API rules, not as a universal folder mandate.
- Storybook is both documentation and verification surface: stories define component states, Autodocs renders baseline docs, MDX/Doc Blocks add narrative, and `play` functions can capture user-observable interaction behavior.
- Playwright evidence is the browser/runtime layer: screenshots and visual comparisons support layout claims, while traces help debug CI/runtime failures and should be referenced in visual evidence packets where available.
- Context7 findings are retrieval evidence only. The frontend methodology page cites primary FSD, Storybook, Playwright, W3C, MDN, Testing Library and web.dev sources directly.

## Дополнение 2026-05-24: LLM / AI / RAG methodology research

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/openai/openai-agents-python` | OpenAI Agents SDK | Agents, tools, handoffs, guardrails, sessions, tracing, human-in-the-loop, agent-as-tool and MCP integration signals |
| `/openai/openai-cookbook` | OpenAI Cookbook | Structured output examples, embeddings/vector search examples, RAG/source citation recipes and practical eval/RAG patterns |
| `/vibrantlabsai/ragas` | Ragas | Faithfulness, answer relevancy, context precision/recall/relevance, response groundedness, factual correctness and test dataset fields |

Выводы:

- OpenAI Agents SDK findings support agent workflow gates for tool contracts, handoff ownership, sessions/state, tracing and guardrails, but primary source status remains official OpenAI docs/GitHub.
- OpenAI Cookbook findings are recipe-level, not normative API contracts; use them as experiment/practice material and cite current OpenAI API docs for production guidance.
- Ragas findings are vendor/open-source methodology input for RAG metrics; use as optional tool evidence, not as the only quality standard.
- Context7 findings are retrieval evidence only. The methodology page cites primary OpenAI, Promptfoo, Ragas and OpenTelemetry sources directly.

## Дополнение 2026-05-24: Quality, Testing & Evals methodology research

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/websites/pytest_en_stable` | pytest documentation | Small readable tests, assertion introspection, modular fixtures, parametrization, CI pipeline guidance, flaky-test guidance and report metadata hooks |
| `/websites/playwright_dev` | Playwright documentation | E2E runner evidence, retries, flaky/passed/failed classification, trace-on-retry, Trace Viewer, screenshots and visual comparisons |
| `/websites/vitest_dev` | Vitest documentation | Watch mode, CI run mode, projects, coverage, snapshots, browser mode, isolation and fast feedback loops |

Выводы:

- pytest findings support Python-specific test/evidence templates, but Product-Agent OS should preserve the repo's existing runner instead of forcing pytest.
- Playwright findings support browser/runtime evidence packets: traces, screenshots, retry classification and stable visual baselines.
- Vitest findings support JS/TS fast-feedback and CI modes, but coverage and snapshots must be governed as evidence signals, not treated as proof of correctness.
- Context7 findings are retrieval evidence only. The methodology page cites primary pytest, Playwright, Vitest, Agile Alliance, Fowler, ISTQB, Stryker, Hypothesis, GitHub, OpenAI, Promptfoo and Ragas sources directly.

## Дополнение 2026-05-24: Security, Privacy & Compliance methodology research

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/owasp/cheatsheetseries` | OWASP Cheat Sheet Series | Web/API risk vocabulary, authentication/session/input validation/cryptographic storage guidance, secrets/logging examples and sensitive-data exclusion in logs |
| `/ossf/scorecard` | OpenSSF Scorecard | Repository security checks: branch protection, code review, dangerous workflows, dependency update tools, pinned dependencies, SAST, security policy, token permissions and vulnerabilities |
| `/cyclonedx/cyclonedx-cli` | CycloneDX CLI | SBOM validation, merge, signing, verification and CI-suitable exit-code evidence |

Выводы:

- OWASP Cheat Sheet findings support implementation-level security review vocabulary, but the methodology page cites primary OWASP pages and cheat sheets directly.
- OpenSSF Scorecard findings support supply-chain readiness signals and CI evidence, not a standalone compliance claim.
- CycloneDX findings support SBOM evidence packets: generation, validation, signing, verification, release storage and failure handling.
- Context7 did not return a useful SLSA library ID in this run, so SLSA guidance is cited directly from the official SLSA spec.
- Context7 findings are retrieval evidence only. The methodology page cites primary NIST, OWASP, OpenAI, GitHub, SLSA, OpenSSF, SPDX, CycloneDX, GDPR and CCPA sources directly.

## Дополнение 2026-05-24: Delivery, Release & Operations methodology research

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/websites/opentelemetry_io` | OpenTelemetry | Traces, metrics, logs, exporters, trace-context-enriched logs, metrics export behavior and semantic conventions as runtime evidence vocabulary |
| `/websites/github_en_actions` | GitHub Actions | Deployment environments, required reviewers, wait timers, branch/tag restrictions, environment secrets, workflow environment approvals and deployment API surface |
| `/argoproj/argo-rollouts` | Argo Rollouts | Progressive delivery concepts, canary weighted steps, blue-green pre-promotion analysis, manual promotion, automated rollback and traffic shifting |

Выводы:

- OpenTelemetry findings support release evidence packets that name dashboards, traces, metrics, logs, exporters/collectors, alert owners and redaction/sampling gaps.
- GitHub Actions findings support Product-Agent OS release gates around environments, deployment protection rules, required reviewers, branch/tag restrictions, environment secrets and workflow permission boundaries.
- Argo Rollouts findings support progressive-delivery gates: rollout strategy, traffic percentage/cohort, analysis metrics, promotion/abort rules, manual judgement and rollback behavior.
- Context7 findings are retrieval evidence only. The methodology page cites primary DORA, Google SRE, OpenTelemetry, Twelve-Factor, GitHub, Keep a Changelog, SemVer, Conventional Commits, CNCF GitOps, Argo Rollouts, OpenFeature and OpenAI Codex sources directly.

## Дополнение 2026-05-24: Codex / Agentic Workflow methodology research

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/websites/developers_openai_codex` | Official OpenAI Codex documentation | `AGENTS.md`, customization layers, skills, subagents, MCP, hooks, plugins, approvals, sandbox, automations, memories, best practices, use-case promotion signals |
| `/openai/openai-agents-python` | OpenAI Agents SDK for Python | Agents, tools, handoffs, guardrails, sessions, tracing, human-in-the-loop approvals, agent-as-tool pattern and Codex tool/MCP integration signals |

Выводы:

- Codex methodology should keep chat as a work surface, not source of truth. Durable rules and state belong in `AGENTS.md`, control-plane files, task packets, run logs and source-backed docs.
- Codex customization layers are complementary: `AGENTS.md` shapes persistent project behavior, memories carry local recall, skills package repeatable workflows, MCP connects external systems and subagents delegate specialized work.
- Skills should be promoted from proven manual workflows; plugins distribute stable workflows and bundled capabilities; automations should follow only after manual prompt/tool stability and early-run review.
- Subagents are useful for independent exploration, review and specialized slices, but require fresh-context task packets, explicit ownership, expected evidence and stop conditions.
- MCP and hooks are capability surfaces, not just documentation features. They require trust, data-boundary, approval, side-effect and disable/rollback review before activation or external writes.
- Agents SDK findings support vocabulary for code-owned agent applications: handoffs, agents-as-tools, guardrails, human review, sessions, tracing and evals. The Codex methodology keeps this layer distinct from Codex App/CLI/IDE runtime workflows.
- Context7 findings are retrieval evidence only. The methodology page cites primary OpenAI docs directly and uses Context7 as a cross-check for practical concepts.

## Дополнение 2026-05-24: Requirements & Domain methodology research

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/websites/cucumber_io` | Cucumber/Gherkin documentation | `Feature`, `Rule`, `Scenario`, `Given`, `When`, `Then`, `Scenario Outline`, `Examples`, executable specification, declarative behavior style |
| `/websites/c4model` | C4 model | System Context, Container, Component, Code abstraction levels and guidance to use only the diagrams that add value |
| `/websites/spec_openapis_oas_v3_2_0` | OpenAPI 3.2.0 | Operation, tags, `operationId`, parameters, `requestBody`, responses, schemas/components, security and deprecation as downstream traceability artifacts |

Выводы:

- Requirements-domain methodology should connect `requirement -> scenario -> check -> evidence owner` before behavior changes.
- Gherkin can be accepted as one behavior format, but methodology should allow equivalent behavior formats and avoid implementation-detail scenarios.
- C4 supports `bounded_context_architecture_boundary_trace`: bounded context should map to architecture boundary; use only useful diagram levels.
- OpenAPI supports downstream traceability from domain terms/requirements to API operations, schemas, errors and security contracts, but is not itself the full requirement source.
- Context7 findings are retrieval evidence only; the methodology page cites primary Agile Alliance, Cucumber, ISO, IIBA, Fowler, Domain Language, EventStorming, Domain Storytelling, C4 and OpenAPI sources directly.

## Дополнение 2026-05-24: Solution Architecture methodology research

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/websites/c4model` | C4 model | Software systems, containers, components, code; system context/container/component/code diagrams; supporting dynamic/deployment views; notation/tooling independence; compatibility with arc42 |
| `/websites/arc42` | arc42 documentation | Solution strategy, building block hierarchy, context/scope alignment, runtime/deployment views, cross-cutting concepts, architecture decisions, quality requirements and risks |
| `/structurizr/structurizr` | Structurizr / Structurizr DSL | Models-as-code for C4, text-based DSL, workspace/model/views concepts, documentation/ADR support and validate/export workflow signals |

Выводы:

- Solution architecture methodology should treat architecture as a reviewable artifact: boundary, owner, public contract, data ownership, quality attributes, runtime topology, verification and rollback.
- C4 provides the default view stack; context/container views are the normal minimum for complex systems, while component/code views should be conditional.
- arc42 complements C4 with structured communication: goals, constraints, solution strategy, building blocks, runtime/deployment, concepts, decisions, quality and risks.
- Structurizr DSL is the heavier architecture-as-code path when one model must generate multiple C4 views; Mermaid remains enough for lightweight Markdown-native diagrams.
- Context7 findings are retrieval evidence only; the methodology page cites primary C4, arc42, ISO 42010, SEI ATAM, MADR, Structurizr, Mermaid, Thoughtworks, AWS, Azure and OpenTelemetry sources directly.

## Дополнение 2026-05-24: Business & Product methodology research

| Library ID | Назначение | Что извлечено |
| --- | --- | --- |
| `/websites/developers_openai_codex` | Official OpenAI Codex documentation | AI-native engineering team guidance, reusable workflow promotion, verified operations, AI app eval workflow and documentation currency workflow |
| `/amplitude/amplitude-docs` | Amplitude product analytics documentation | Event tracking risks, tracking taxonomy, data quality ownership, Data Governor responsibilities, segmentation, funnel, retention and cohort analysis signals |
| `/openai/evals` | OpenAI Evals | Custom evals, expected outputs, thresholds, baseline comparison and metric/violation-rate style evidence for AI product behavior |

Выводы:

- Business/product methodology should require product hypothesis before architecture or implementation for meaningful behavior changes.
- Metric hardening should separate North Star/primary value metric, input metrics, counter-metrics, guardrails, proxy risk, qualitative review, privacy, retention, data minimization and post-release review.
- Product analytics instrumentation must include taxonomy, ownership and data quality checks because event typos, property drift and missing governance can invalidate product decisions.
- Codex product-agent workflows should promote manual success -> reusable playbook/skill -> plugin/automation only when product value, verification, ownership and safety boundaries are explicit.
- AI product behavior needs eval datasets, baselines and thresholds in addition to product metrics and qualitative feedback.
- Context7 findings are retrieval evidence only; the methodology page cites primary Google HEART, Amplitude, OpenAI, Product Talk, Lean Startup and Strategyzer sources directly.
