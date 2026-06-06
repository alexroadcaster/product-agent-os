# Development And Documentation Methodology Research Plan

Source status: `official + verified methodology + tool-assisted research in progress`

Start date: **2026-05-23**.  
Purpose: keep a managed research backlog for the next Product-Agent OS hardening stage, so the plugin supports a reproducible engineering process for web, desktop, mobile, backend, AI/evals, docs and operations work.

## Working Backlog

| Status | Item | Result |
| --- | --- | --- |
| done | Review the current Track 6/7 implementation and source documents. | Standards were already represented in workflows, templates and evals; a separate research backlog is still useful for deeper methodology coverage. |
| done | Map development methodologies and documentation tooling. | The tables below record methodology tracks, documentation/tooling tracks and expected Product-Agent OS artifacts. |
| done | Start primary-source verification. | Primary or official sources were reviewed for OpenAI Codex, Agile Alliance, Feature-Sliced Design, C4, arc42, OpenAPI, AsyncAPI, Storybook, GitLab/GitHub docs, MkDocs, Docusaurus, Antora, Read the Docs and release/documentation tooling. |
| done | Preserve the Context7 slice. | Context7 was used for Docusaurus, MkDocs and Storybook retrieval; the conclusions are recorded in [context7-research.md](context7-research.md). |
| in_progress | Add missing sources to the registry. | New entries cover ATDD/BDD, DDD, metrics, ADR/MADR, Structurizr, diagram tools, code/API/DB docs, docs portals, lint and release policy. |
| planned | Prepare a deep-dive card for each methodology. | Expected shape: source, short meaning, when to use, when not to use, plugin artifact, eval/gate and residual risk. |
| done | Compare research with the implemented plugin. | The gap matrix is stored in [development-methodology-gap-matrix.md](development-methodology-gap-matrix.md). |
| done | Detail Track 8 by methodology, standard and tool. | The execution backlog is stored in [product-agent-os-track-8-detailed-backlog.md](product-agent-os-track-8-detailed-backlog.md). |
| done | Extend Track 8 scenario workflows. | The backlog now includes bug rescue, greenfield idea, complex system acceleration, usage-mode classifier, integration catalog and scenario-specific readiness gates. |
| done | Run final pre-development review. | Critical analysis, ten extra scenarios and final recommendations are stored in [product-agent-os-final-predevelopment-review.md](product-agent-os-final-predevelopment-review.md). |
| done | Extend the backlog before implementation. | The backlog includes PR review, legacy onboarding, API migration, AI eval regression, native/mobile feature work, desktop local-first work, data migration, security-sensitive change, CI stabilization, release packaging, mode stack, fixture coverage and plugin success metrics. |
| in_progress | Implement Track 8. | T8-S1..T8-S16 and the follow-up hardening slices are implemented through standards-trigger hardening and transcript/session eval replay. |

## Research Method

Use the same protocol for each methodology or tool:

1. Find a primary or official source.
2. Extract five to ten verifiable claims without promoting community summaries to rules.
3. Label each claim as `official`, `methodology`, `tool convention`, `community` or `experiment`.
4. Map applicability to web/front-end, native/mobile, desktop, backend/API, data, AI/evals, docs and operations.
5. Connect the claim to a Product-Agent OS template, workflow, skill, eval, discovery signal, docs page or staged CI proposal.
6. Record failure modes: where the method is harmful, excessive or requires a human decision.
7. Add a verification surface: test, eval gate, docs check, contract check, browser/runtime check or review checklist.

## Development Methodologies

| Methodology | Short Description | Primary Sources | Product-Agent OS Signal |
| --- | --- | --- | --- |
| Agentic / AI-native development | SDLC work where Codex App, CLI, IDE extension, subagents and skills help plan, build, test, review and document changes while a human keeps ownership of architecture, product and quality. | [Codex build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://developers.openai.com/codex/skills), [Building an AI-Native Engineering Team](https://developers.openai.com/codex/guides/build-ai-native-engineering-team), [Codex AI app evals](https://developers.openai.com/codex/use-cases/ai-app-evals) | Require scoped inputs, ownership, tests/evals, source policy, approval policy, run evidence and the promotion path manual workflow -> skill -> plugin -> automation. |
| Data-informed development | Product decisions made through goals, signals, metrics, guardrails and post-release learning. | [Google HEART paper](https://research.google.com/pubs/pub36299.htmlyaframe=0), [Amplitude North Star](https://amplitude.com/north-star-hub) | Use metric specs, guardrail metrics, privacy notes and anti-Goodhart protection. Do not confuse it with Domain-Driven Design. |
| Domain-Driven Design | Modeling complex business logic around a domain model, ubiquitous language and bounded contexts. | [Martin Fowler: Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html), [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html), [Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html), [Domain Language](https://www.domainlanguage.com/) | Apply only when domain complexity justifies it. Require a glossary, bounded contexts, aggregate/event choices only when useful, and explicit mapping to architecture boundaries. |
| TDD | Red-Green-Refactor loop: write a failing test, implement the smallest code that passes, then refactor with tests green. | [Agile Alliance TDD](https://agilealliance.org/glossary/tdd/) | Require red -> green -> refactor evidence in RUNLOG or an explicit gap, especially for bug fixes and shared behavior. |
| ATDD | Acceptance tests written before implementation with product/customer, development and testing perspectives. | [Agile Alliance ATDD](https://agilealliance.org/glossary/atdd/) | Connect REQUIREMENTS.md and TEST.md through acceptance scenarios before code changes. |
| BDD | Behavior scenarios and business outcomes expressed in a shared language for domain experts, testers and developers. | [Agile Alliance BDD](https://agilealliance.org/glossary/bdd/) | Use for user behavior and business rules. It complements, but does not replace, unit/integration/contract tests. |
| Feature-Sliced Design | Frontend architecture methodology using layers, slices, segments, public API and import rules. | [Feature-Sliced Design documentation](https://feature-sliced.github.io/documentation/) | Treat as a strong default for growing UI apps, but do not force it onto backend/native/simple MVP work. |
| Eval-driven AI development | Repeatable eval suites for prompt/model/tool/RAG/agent behavior before changing production behavior. | [Codex AI app evals](https://developers.openai.com/codex/use-cases/ai-app-evals), [OpenAI eval best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | Require a baseline, target path, no-secrets fixtures, assertions, run command and threshold. |
| Docs-as-code | Documentation lives with code, changes through review, and is built/checked as part of engineering workflow. | [GitLab documentation architecture](https://docs.gitlab.com/development/documentation/site_architecture/), [GitHub Actions workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows), [GitHub protected branches](https://docs.github.com/articles/about-required-reviews-for-pull-requests) | Stage docs CI/CODEOWNERS proposals, but never enable external workflows without approval. |

## Documentation And Engineering Artifacts

| Tool | Short Description | Source | Product-Agent OS Signal |
| --- | --- | --- | --- |
| C4 model | Software architecture diagrams at system context, container, component and code levels; not every level is required. | [C4 diagrams](https://c4model.com/diagrams) | Architecture overview should require at least context/container views for meaningful system changes. |
| arc42 | Architecture communication template covering goals, constraints, context, strategy, building blocks, runtime, deployment, decisions, quality and risks. | [arc42 overview](https://arc42.org/overview) | Useful structure for architecture-overview template and review checklist. |
| ADR / MADR | Markdown decision records for context, decision, alternatives and consequences. | [MADR](https://adr.github.io/madr/) | Add trigger policy and ADR index/check for irreversible choices. |
| Structurizr DSL | Text DSL for C4 architecture model, diagrams and Markdown/AsciiDoc docs as code. | [Structurizr DSL](https://docs.structurizr.com/dsl), [Structurizr as code](https://docs.structurizr.com/as-code) | Optional advanced path for architecture-as-code; not a default for small repos. |
| Mermaid | Text syntax for diagrams in Markdown/docs portals. | [Mermaid syntax](https://mermaid.js.org/intro/syntax-reference.html) | Good repo-native default, but syntax/build checks are needed. |
| PlantUML | Text-to-diagram tooling for sequence, component and UML-style views. | [PlantUML sequence diagram](https://plantuml.com/sequence-diagram) | Keep optional for teams already using UML/sequence diagrams. |
| OpenAPI | Machine-readable HTTP API contract. | [OpenAPI Specification latest](https://spec.openapis.org/oas/latest) | API changes need contract updates or explicit gaps. |
| AsyncAPI | Machine-readable event/message-driven API contract. | [AsyncAPI v3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0) | Event-driven systems need channel/message ownership, producer/consumer roles and compatibility checks. |
| Storybook | UI component workshop and docs/testing surface with Autodocs, MDX/Doc Blocks and a11y workflows. | [Storybook Autodocs](https://storybook.js.org/docs/writing-docs/autodocs), [Storybook a11y tests](https://storybook.js.org/docs/writing-tests/accessibility-testing) | UI changes should declare component states and visual/a11y checks when Storybook exists or should be proposed. |
| TypeDoc | Generates HTML docs or JSON model from TypeScript source comments/exports. | [TypeDoc](https://typedoc.org/) | Good for TS library/API packages and public interfaces. |
| JSDoc | JavaScript documentation comment tag system. | [JSDoc tags](https://jsdoc.app/about-block-inline-tags) | Use for public JS interfaces and editor hints; avoid noisy comments for obvious internals. |
| Sphinx autodoc | Python doc generator that imports modules and inspects docstrings. | [Sphinx autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) | Good for Python package/reference docs; requires import-safe modules. |
| Javadoc | Standard Java doc comments and API HTML generation. | [Oracle Javadoc spec](https://docs.oracle.com/en/java/javase/22/docs/specs/javadoc/doc-comment-spec.html) | Applies to public Java APIs. |
| C# XML docs | Structured comments compiled into XML API docs. | [Microsoft C# XML docs](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/) | Useful for .NET public APIs and IntelliSense/reference docs. |
| DBML / dbdocs | Text DSL and hosted docs workflow for database schema documentation. | [DBML syntax](https://dbml.dbdiagram.io/docs/), [dbdocs DBML generation](https://docs.dbdocs.io/features/generate-dbml-from-db/) | Database changes need schema dictionary, relation map and migration notes. |
| SchemaSpy | Generates database schema documentation from metadata. | [SchemaSpy docs](https://schemaspy.readthedocs.io/en/v6.2.0/index.html) | Useful for existing relational DBs; requires explicit data/secrets safeguards. |
| MkDocs | Markdown + YAML static site generator. | [MkDocs](https://www.mkdocs.org/) | Default docs portal for smaller repos and this project; strict build should be a quality gate. |
| Docusaurus | React/MDX documentation site generator with versioning, i18n, search and interactive pages. | [Docusaurus docs](https://docusaurus.io/docs), [Docusaurus versioning](https://docusaurus.io/docs/versioning) | Strong for product docs; versioning adds maintenance cost and should not be automatic. |
| Antora | Multi-repository, multi-version docs site generator for AsciiDoc. | [Antora](https://antora.org/), [Antora features](https://docs.antora.org/antora/latest/features/) | Enterprise/multirepo option; heavier than MkDocs for small repos. |
| Read the Docs | Hosted docs platform that builds docs from VCS and supports versions. | [Read the Docs](https://docs.readthedocs.com/) | External hosting is proposal-only until explicitly approved. |
| CODEOWNERS | GitHub ownership file for reviewer requests and optional code owner approval. | [GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) | Stage CODEOWNERS proposals but do not enforce without approval. |
| GitHub Actions | YAML workflows for build/test/deploy/docs checks. | [GitHub Actions workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows), [workflow syntax](https://docs.github.com/actions/reference/workflows-and-actions/workflow-syntax) | CI proposals should be staged and least-privilege. |
| Vale | Prose/style linter with configurable styles and spelling checks. | [Vale styles](https://vale.sh/docs/styles) | Optional docs quality gate after team style decisions. |
| markdownlint | Markdown structural linting rule set. | [markdownlint rules](https://github.com/markdownlint/markdownlint/blob/main/docs/RULES.md) | Lightweight docs quality gate and CI proposal. |
| Keep a Changelog | Human-readable changelog convention with grouped change types and Unreleased section. | [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) | Release packets should capture user-visible changes, not raw git logs. |
| SemVer | Versioning contract around major/minor/patch and public API compatibility. | [Semantic Versioning](https://semver.org/) | Relevant for plugins, packages, SDKs and public contracts. |

## Initial Gaps For Product-Agent OS

| Gap | Why It Matters | Research Action |
| --- | --- | --- |
| Conditional DDD, bounded context, ubiquitous language, FSD, metrics, evidence-before-completion, docs tooling and readiness statuses are now represented, but semantic sufficiency still needs owner review. | Artifacts prove shape and traceability, not the correctness of domain terms, UI boundaries, metrics or evidence interpretation. | Continue routing semantic sufficiency to owner review and accepted-gap records. |
| ATDD/BDD need durable acceptance-scenario quality. | Scenarios connect product requirements to test/eval-first work better than a generic checklist. | Keep `acceptance-scenarios.md` and require product/development/testing review for important behavior. |
| Docs tooling decisions need stack-aware routing. | MkDocs, Docusaurus, Sphinx, Antora, Storybook, OpenAPI, DBML, Mermaid, PlantUML and Structurizr have different maintenance costs. | Keep `docs-tooling-decision.md` and record `present_unverified` until commands run. |
| Metrics need privacy and anti-Goodhart guardrails. | One metric can distort behavior and telemetry can create privacy risk. | Keep counter-metric, guardrail, qualitative review, retention and owner signoff fields. |
| CI/CODEOWNERS/docs lint stay proposal-only. | This preserves approval boundaries for external workflows and governance changes. | Use explicit `proposed_not_enabled` or equivalent status in CI/governance templates. |

## Next Research Slice

1. Deep-dive cards for DDD, ATDD/BDD, data-informed metrics and docs-as-code governance.
2. Decision matrix for documentation stack selection.
3. Gap matrix: [development-methodology-gap-matrix.md](development-methodology-gap-matrix.md).
4. Track 8 detailed backlog: [product-agent-os-track-8-detailed-backlog.md](product-agent-os-track-8-detailed-backlog.md).
5. Final pre-development review: [product-agent-os-final-predevelopment-review.md](product-agent-os-final-predevelopment-review.md).
6. Track 8 implementation: tests first, then templates/evals/discovery updates, scenario fixture eval, docs and full verification.
