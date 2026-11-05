---
title: "Архив — План исследования методологий разработки и документации"
---

# Архив — План исследования методологий разработки и документации {#_1}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

Source status: `official + verified methodology + tool-assisted research in progress`

Дата старта: **2026-05-23**.  
Назначение: зафиксировать управляемый research backlog для следующего усиления Product-Agent OS, чтобы plugin строил не только agentic-разработку, а воспроизводимый инженерный процесс для проектов web, desktop, mobile, backend, AI/evals, docs и operations.

## Рабочий список задач

| Статус | Задача | Результат |
| --- | --- | --- |
| done | Сверить текущую реализацию Track 6/7 и входные source-документы. | Подтверждено: стандарты уже перенесены в workflow/templates/evals, но нужен отдельный research backlog для дальнейшего углубления. |
| done | Составить карту методологий и documentation tooling. | Ниже зафиксированы methodology tracks, documentation/tool tracks и ожидаемые Product-Agent OS artifacts. |
| done | Начать проверку первоисточников. | Проверены официальные/первичные источники OpenAI Codex, Agile Alliance, Feature-Sliced Design, C4, arc42, OpenAPI, AsyncAPI, Storybook, GitLab/GitHub docs, MkDocs, Docusaurus, Antora, Read the Docs и release/documentation tooling. |
| done | Сохранить Context7-срез. | Context7 использован для Docusaurus, MkDocs и Storybook; выводы продублированы в `docs/sources/context7-research.md`. |
| in_progress | Добавить недостающие источники в registry. | В registry добавляются новые источники для ATDD/BDD, DDD, metrics, ADR/MADR, Structurizr, diagram tools, code/API/DB docs, docs portals, lint/release policy. |
| planned | Для каждой методологии подготовить deep-dive карточку. | Ожидаемый формат: источник, краткая суть, когда применять, когда не применять, артефакт plugin, eval/gate, риски. |
| done | Сопоставить research с уже реализованным plugin. | Gap matrix сохранена в [development-methodology-gap-matrix.md](development-methodology-gap-matrix.md). |
| done | Детализировать Track 8 по методологиям, стандартам и инструментам. | Execution backlog сохранен в [product-agent-os-track-8-detailed-backlog.md](product-agent-os-track-8-detailed-backlog.md). |
| done | Расширить Track 8 scenario workflows. | Backlog дополнен режимами `bug_rescue`, `greenfield_idea`, `complex_system_acceleration`, usage mode classifier, integration catalog и scenario-specific readiness gates. |
| done | Провести финальный pre-development review. | Критический анализ, 10 дополнительных сценариев и итоговые рекомендации сохранены в [product-agent-os-final-predevelopment-review.md](product-agent-os-final-predevelopment-review.md). |
| done | Финально расширить backlog перед разработкой. | Backlog дополнен режимами `pr_review`, `legacy_onboarding`, `api_migration`, `ai_eval_regression`, `native_mobile_feature`, `desktop_local_first`, `data_migration`, `security_sensitive_change`, `ci_stabilization`, `release_packaging`, mode stack, fixture coverage and plugin success metrics. |
| in_progress | Реализовать Track 8. | T8-S1..T8-S16, `T8-A13`, `T8-A14`, `T8-A15`, `T8-A3/T8-A4`, `T8-A5`, `T8-A6`, `T8-A7`, `T8-A8`, `T8-A9`, `T8-A16`, `T8-C`, `T8-F`, `T8-H` and `T8-GY` реализованы; следующий execution queue начинается с `T8-B` standards trigger hardening. |

## Общий метод исследования

Для каждой методологии и инструмента применяется один и тот же протокол:

1. Найти первичный или официальный источник.
2. Снять 5-10 проверяемых утверждений без community-обобщений.
3. Разделить статус утверждения: `official`, `methodology`, `tool convention`, `community`, `experiment`.
4. Определить применимость: web/front-end, native/mobile, desktop, backend/API, data, AI/evals, docs, operations.
5. Привязать к Product-Agent OS: template, workflow, skill, eval, discovery signal, docs page или staged CI proposal.
6. Зафиксировать failure modes: где методология вредна, избыточна или требует человеческого решения.
7. Добавить проверку: тест, eval gate, docs check, contract check, browser/runtime check или review checklist.

## Методологии разработки

| Методология | Краткое описание | Первичные источники | Ключевая информация для plugin |
| --- | --- | --- | --- |
| Agentic / AI-native development | Организация SDLC, где Codex App, CLI, IDE extension, subagents и skills помогают планировать, строить, тестировать, ревьюить и документировать изменения, а человек сохраняет ownership архитектуры, продукта и качества. | [Codex build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://developers.openai.com/codex/skills), [Building an AI-Native Engineering Team](https://developers.openai.com/codex/guides/build-ai-native-engineering-team), [Codex AI app evals](https://developers.openai.com/codex/use-cases/ai-app-evals) | Не превращать agentic work в blind generation. Нужны scoped inputs, ownership, tests/evals, source policy, approval policy, run evidence и promotion path: manual workflow -> skill -> plugin -> automation. |
| Data-informed development | Принятие продуктовых решений через goals, signals, metrics, guardrails и post-release learning. | [Google HEART paper](https://research.google.com/pubs/pub36299.html?frame=0), [Amplitude North Star](https://amplitude.com/north-star-hub) | Использовать термин `data-informed product decisions`, чтобы не смешивать с Domain-Driven Design. В plugin нужны metric spec, guardrail metrics, privacy notes и защита от оптимизации одного proxy metric. |
| Domain-Driven Design | Проектирование сложной бизнес-логики вокруг domain model, ubiquitous language и bounded contexts. | [Martin Fowler: Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html), [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html), [Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html), [Domain Language](https://www.domainlanguage.com/) | DDD нужен для сложной предметной области, а не для каждого CRUD. Plugin должен требовать domain glossary, bounded contexts, aggregates/domain events only when justified, и explicit mapping к architecture boundary. |
| TDD | Red-Green-Refactor цикл: тест до реализации, минимальный код, refactor при зеленых тестах. | [Agile Alliance TDD](https://agilealliance.org/glossary/tdd/) | Уже частично внедрено в Track 7. Следующий шаг: требовать evidence red -> green -> refactor в RUNLOG или gap, особенно для bugfix и shared behavior. |
| ATDD | Acceptance tests пишутся до реализации совместно с customer/product, development и testing perspectives. | [Agile Alliance ATDD](https://agilealliance.org/glossary/atdd/) | Хороший мост между REQUIREMENTS.md и TEST.md. Plugin должен поддерживать acceptance scenarios до кода и traceability от requirement к test/eval. |
| BDD | Уточнение TDD/ATDD через behavior scenarios, business outcomes и общий язык для domain experts, testers и developers. | [Agile Alliance BDD](https://agilealliance.org/glossary/bdd/) | Применять для пользовательского поведения и бизнес-правил. Не заменяет unit tests; дает acceptance language и сценарии для agent handoff. |
| Feature-Sliced Design | Frontend architecture methodology с layers, slices, segments, public API и import rules. | [Feature-Sliced Design documentation](https://feature-sliced.github.io/documentation/) | Использовать как strong default для растущего UI, но не навязывать backend/native/MVP. Discovery должен видеть FSD structure, а planner должен фиксировать layer/slice boundary. |
| Eval-driven AI development | Повторяемые eval suites для prompt/model/tool/RAG/agent behavior до изменения production behavior. | [Codex AI app evals](https://developers.openai.com/codex/use-cases/ai-app-evals), [OpenAI eval best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | Для AI/RAG нельзя ограничиться unit tests. Нужны baseline, app-path target, fixtures без secrets/customer data, assertions, run command и threshold. |
| Docs-as-code | Документация живет рядом с кодом, меняется через review, собирается и проверяется как часть engineering workflow. | [GitLab documentation architecture](https://docs.gitlab.com/development/documentation/site_architecture/), [GitHub Actions workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows), [GitHub protected branches](https://docs.github.com/articles/about-required-reviews-for-pull-requests) | Plugin должен stage proposals для docs CI/CODEOWNERS, но не включать external workflows без approval. Docs impact должен быть gate в PLAN/TEST/RUNLOG. |

## Инструменты документации и инженерных артефактов

| Инструмент | Краткое описание | Источник | Ключевая информация для plugin |
| --- | --- | --- | --- |
| C4 model | Уровни software architecture diagrams: system context, container, component, code; не все уровни обязательны. | [C4 diagrams](https://c4model.com/diagrams) | Default architecture overview должен требовать минимум context/container для значимых системных изменений. |
| arc42 | Template для architecture communication: goals, constraints, context, solution strategy, building blocks, runtime, deployment, decisions, quality, risks. | [arc42 overview](https://arc42.org/overview) | Полезен как структура architecture-overview template и review checklist. |
| ADR / MADR | Markdown decision records для фиксации контекста, решения, альтернатив и последствий. | [MADR](https://adr.github.io/madr/) | Plugin уже генерирует ADR template; нужен next step: ADR trigger policy и ADR index/check. |
| Structurizr DSL | Text-based DSL для C4 architecture model, diagrams и Markdown/AsciiDoc docs as code. | [Structurizr DSL](https://docs.structurizr.com/dsl), [Structurizr as code](https://docs.structurizr.com/as-code) | Optional advanced path для architecture-as-code; не должен быть default для маленьких repos. |
| Mermaid | Text syntax for diagrams embedded in Markdown/docs portals. | [Mermaid syntax](https://mermaid.js.org/intro/syntax-reference.html) | Хороший default для repo-native diagrams, но нужен syntax/build check, потому что small syntax errors ломают rendering. |
| PlantUML | Text-to-diagram tooling, особенно для sequence/component/UML-style views. | [PlantUML sequence diagram](https://plantuml.com/sequence-diagram) | Useful for teams already using UML/sequence diagrams; should remain optional. |
| OpenAPI | Machine-readable HTTP API contract. | [OpenAPI Specification latest](https://spec.openapis.org/oas/latest) | API changes need contract update or explicit gap; core guidance should prefer latest spec reference while preserving compatibility notes. |
| AsyncAPI | Machine-readable event/message-driven API contract. | [AsyncAPI v3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0) | Event-driven systems need channel/message ownership, producer/consumer roles and compatibility check. |
| Storybook | UI component workshop and docs/testing surface with Autodocs, MDX/Doc Blocks and a11y workflows. | [Storybook Autodocs](https://storybook.js.org/docs/writing-docs/autodocs), [Storybook a11y tests](https://storybook.js.org/docs/writing-tests/accessibility-testing) | UI changes should declare component states and visual/a11y checks when Storybook exists or should be proposed. |
| TypeDoc | Generates HTML docs or JSON model from TypeScript source comments/exports. | [TypeDoc](https://typedoc.org/) | Good for TS library/API packages; less useful for purely internal app code unless public interfaces exist. |
| JSDoc | Tag system for JavaScript documentation comments. | [JSDoc tags](https://jsdoc.app/about-block-inline-tags) | Use for public JS interfaces and editor hints; avoid low-value comments on obvious internals. |
| Sphinx autodoc | Python doc generator can import modules and inspect docstrings. | [Sphinx autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) | Good for Python package/reference docs; requires import-safe modules and documented public API. |
| Javadoc | Standard Java doc comments and API HTML generation. | [Oracle Javadoc spec](https://docs.oracle.com/en/java/javase/22/docs/specs/javadoc/doc-comment-spec.html) | Applies to public Java APIs; first sentence summary and tags matter for generated docs. |
| C# XML docs | Structured comments compiled into XML API docs. | [Microsoft C# XML docs](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/) | Good for .NET public APIs and IntelliSense/reference docs. |
| DBML / dbdocs | Text DSL and hosted docs workflow for database schema documentation. | [DBML syntax](https://dbml.dbdiagram.io/docs/), [dbdocs DBML generation](https://docs.dbdocs.io/features/generate-dbml-from-db/) | Database changes need schema dictionary, relation map and migration notes; DBML is a strong lightweight option. |
| SchemaSpy | Generates database schema documentation from metadata. | [SchemaSpy docs](https://schemaspy.readthedocs.io/en/v6.2.0/index.html) | Useful for existing relational DBs; requires DB access and no secret leakage in generated artifacts. |
| MkDocs | Markdown + YAML static site generator with dev server and static HTML output. | [MkDocs](https://www.mkdocs.org/) | Default docs portal for smaller repos and this project. Strict build should be docs quality gate. |
| Docusaurus | React/MDX documentation site generator with versioning, i18n, search and interactive pages. | [Docusaurus docs](https://docusaurus.io/docs), [Docusaurus versioning](https://docusaurus.io/docs/versioning) | Strong for product docs with React/MDX and versioned public docs; versioning adds maintenance cost and should not be automatic. |
| Antora | Multi-repository, multi-version docs site generator for AsciiDoc. | [Antora](https://antora.org/), [Antora features](https://docs.antora.org/antora/latest/features/) | Enterprise/multirepo option; heavier than MkDocs for small repos. |
| Read the Docs | Hosted docs platform that builds docs from VCS workflow and supports versions. | [Read the Docs](https://docs.readthedocs.com/) | Good for public/open docs hosting; plugin should propose, not assume external hosting. |
| CODEOWNERS | GitHub ownership file for auto-requesting reviewers and optional code owner approval. | [GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) | Useful governance signal; Product-Agent OS may stage CODEOWNERS proposals but not enforce without approval. |
| GitHub Actions | YAML-defined workflows in `.github/workflows` for build/test/deploy/docs checks. | [GitHub Actions workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows), [workflow syntax](https://docs.github.com/actions/reference/workflows-and-actions/workflow-syntax) | CI proposals should be staged and least-privilege. Required checks are a governance decision, not automatic plugin behavior. |
| Vale | Prose/style linter with configurable styles and spelling checks. | [Vale styles](https://vale.sh/docs/styles) | Good optional docs quality gate for product docs; requires team style decisions. |
| markdownlint | Markdown rule set and linter for structural consistency. | [markdownlint rules](https://github.com/markdownlint/markdownlint/blob/main/docs/RULES.md) | Lightweight docs quality gate; useful for CI proposal and local docs checks. |
| Keep a Changelog | Human-readable changelog convention with grouped change types and Unreleased section. | [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) | Release packet should capture user-visible changes, deprecations, removals and security notes, not raw git logs. |
| SemVer | Versioning contract around major/minor/patch and public API compatibility. | [Semantic Versioning](https://semver.org/) | Relevant for plugins, packages, SDKs and public contracts; major changes require explicit migration notes. |

## Initial gaps to investigate against Product-Agent OS

| Gap | Почему важно | Research action |
| --- | --- | --- |
| DDD conditional lifecycle gate закрыт в `T8-A5`, bounded context traceability закрыта в `T8-A6`, ubiquitous language traceability закрыта в `T8-A7`, conditional FSD structure routing закрыт в `T8-A8`, metric hardening закрыт в `T8-A9`, evidence-before-completion закрыт в `T8-A16`, docs tooling selector закрыт в `T8-C`, conditional readiness statuses закрыты в `T8-F`, dedicated scenario/eval/Codex compatibility docs закрыты в `T8-H`, transcript/session eval replay закрыт в `T8-GY`. | Для сложной предметной области нужны не только bounded contexts, но и проверяемая связь domain terms с requirements, API/events, UI labels, code modules or owners; для растущего UI FSD должен быть route clue, а не forced ceremony; для product behavior metrics нужны counter-metric, guardrail, privacy and owner signoff; для completion claims нужны current command/eval/runtime evidence or inspection-only gap; для docs-as-code нужны stack-aware tooling decisions and approval statuses; для readiness нужны `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required`; для operator docs нужны scenario route, behavioral eval and compatibility boundaries; для transcripts нужен deterministic replay без raw private logs. | Следить за human domain expert review, UI owner review, product owner metric review, docs owner review, evidence sufficiency, semantic transcript quality and standards trigger hardening; следующий Track 8 slice: `T8-B` standards trigger hardening. |
| ATDD/BDD не выделены как отдельные tracks. | Acceptance scenarios связывают product requirements и test/eval-first loop лучше, чем generic checklist. | Implemented in `acceptance-scenarios.md`, control-plane templates, lifecycle skills, readiness eval and behavioral eval; residual risk is scenario quality review. |
| Docs tooling decision matrix и `docs_as_code_impact` status contract закрыты в `T8-C`. | Разным стекам нужны разные defaults: MkDocs, Docusaurus, Sphinx, Antora, Storybook, TypeDoc, OpenAPI, DBML, Mermaid, PlantUML and Structurizr; простым/internal-only проектам нужен `not_applicable` или lightweight docs path. | Следить за качеством owner review, maintenance cost and real build evidence; selector records `present_unverified` until commands run. |
| Metrics layer требует privacy and anti-Goodhart guardrails. | Одна метрика может искажать поведение, а telemetry может нарушать privacy. | Расширить metric-spec privacy/legal/security/guardrail fields. |
| CI/CODEOWNERS/docs lint пока только staged proposals. | Это правильно по approvals, но plugin должен ясно отличать recommendation от enforced gate. | Добавить explicit `proposed_not_enabled` status в CI/governance templates. |
| Architecture-as-code не классифицировано. | Structurizr/Mermaid/PlantUML имеют разный вес и maintenance cost. | Исследовать profile: small repo -> Mermaid, large C4 -> Structurizr, UML-heavy -> PlantUML. |

## Следующий research slice

1. Deep-dive карточки по DDD, ATDD/BDD, data-informed metrics, docs-as-code governance.
2. Decision matrix для documentation stack selection.
3. Gap matrix: source claim -> plugin artifact -> eval/check -> residual risk - сохранена в [development-methodology-gap-matrix.md](development-methodology-gap-matrix.md).
4. Track 8 detailed backlog: [product-agent-os-track-8-detailed-backlog.md](product-agent-os-track-8-detailed-backlog.md).
5. Final pre-development review: [product-agent-os-final-predevelopment-review.md](product-agent-os-final-predevelopment-review.md).
6. Track 8 implementation: tests first, then templates/evals/discovery updates, scenario fixture eval, docs and full verification.
