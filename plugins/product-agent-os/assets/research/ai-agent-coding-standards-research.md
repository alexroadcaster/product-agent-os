# Research: стандарты кодирования для AI-агентов

Source status: `official + primary methodology + local implementation audit`

```yaml
title: "AI-agent coding standards research corpus"
type: "research source packet"
status: "draft_research_packet"
checked_at: "2026-06-29"
source_count: 135
trust_level: "high for official vendor/language/security sources; medium for community methodology and author essays"
verification_status: "web corpus collected; local Product-Agent OS context audited; coding standard implementation not yet generated"
privacy_status: "metadata-only; no secrets, raw private logs or customer payloads included"
```

## Назначение

Этот файл фиксирует исследовательский корпус для будущего стандарта кодирования AI-агентов в Product-Agent OS plugin. Цель не в том, чтобы скопировать один style guide, а в том, чтобы собрать переносимый контракт: как агент должен проектировать, писать, рефакторить, комментировать, тестировать и доказывать изменения в коде без спагетти-роста, скрытых fallback и неподтвержденных заявлений.

Документ опирается на три слоя:

- внешние источники: официальные style guides, language conventions, refactoring methodology, testing, API contracts, security, supply chain, observability and maintainability guidance;
- локальные артефакты Product-Agent OS: `plugins/product-agent-os/assets/templates/workflows/development-standards.md`, `plugins/product-agent-os/assets/templates/workflows/review-slice.md`, `docs/playbooks/code-review.md`, `docs/sources/development-methodology-research-log.md`, `docs/sources/development-methodology-gap-matrix.md`;
- пользовательский опыт проекта: требование evidence-bound работы, контроль source-of-truth, отсутствие runtime claims без proof, сохранение приватности и запрет несанкционированных git, browser, provider, deployment and automation actions.

## Метод исследования

Исследование шло по семи корзинам:

1. AI-agent execution: Codex, `AGENTS.md`, skills, approvals, evals, guardrails, tracing.
2. Language style: Python, JavaScript, TypeScript, Go, Rust, Java, C#, C++, C, Swift, Kotlin, PHP, Ruby, R and SQL.
3. Refactoring and architecture: code smells, technical debt, DDD, bounded contexts, hexagonal architecture, SOLID, strangler and branch-by-abstraction patterns.
4. Testing and review: TDD, ATDD, BDD, test pyramid, browser tests, mutation tests, contract tests, coverage, PR review and ownership.
5. Commenting and documentation: docstrings, API docs, generated documentation, OpenAPI, AsyncAPI, JSON Schema, GraphQL, gRPC and event contracts.
6. Security and supply chain: NIST SSDF, OWASP, SLSA, Scorecard, SBOM, secret scanning and static analysis.
7. Maintainability and operability: cognitive complexity, quality models, architecture diagrams, 12-factor, DORA and OpenTelemetry.

## Журнал промежуточных результатов

| Шаг | Что проверялось | Урок для стандарта AI-агентов |
| --- | --- | --- |
| 1 | Локальный `development-standards.md` | В plugin уже есть lifecycle вокруг задачи, но нужен более низкоуровневый кодовый контракт: naming, comments, decomposition, tests and refactoring proof. |
| 2 | Локальные review/playbook источники | Review должен оставаться defect-first: сначала баги, регрессии, security, missing tests, затем стиль и красота. |
| 3 | OpenAI Codex guidance | Для AI-agent стандарта важнее не “умный паттерн”, а точный контекст, маленькие изменения, approvals, guardrails and verification evidence. |
| 4 | Language style guides | Универсальный стандарт должен делегировать форматирование языковым форматтерам и линтерам, а не заставлять агента спорить о пробелах вручную. |
| 5 | Refactoring sources | Рефакторинг считается безопасным только при preserved behavior, staged changes and test evidence; большой rewrite без characterization tests повышает риск. |
| 6 | OOP and architecture sources | OOP правила полезны как ограничения связности и инвариантов, но не как требование создавать классы ради классов. |
| 7 | Commenting sources | Комментарии должны объяснять intent, invariants, contracts, risk and surprising behavior; пересказ очевидного кода считается шумом. |
| 8 | Testing sources | Agent task packet должен заранее назвать test strategy, acceptance checks, negative cases and evidence per changed behavior. |
| 9 | Security sources | Secure coding для агента должен включать secret hygiene, least privilege, logging redaction, dependency trust and supply-chain evidence. |
| 10 | Maintainability sources | Complexity gates должны ловить спагетти-код: excessive branching, long functions, hidden state, cyclic dependencies and unclear ownership. |
| 11 | API contract sources | API changes должны сопровождаться schema/contract update, compatibility statement and client/server evidence. |
| 12 | Observability sources | Изменение runtime behavior должно иметь log/trace/metric plan, но observability не заменяет тесты и acceptance proof. |

## Ключевые выводы

1. Стандарт для AI-агента должен быть не “единым вкусом”, а dispatch-моделью: сначала определить язык, framework, ownership boundary and source-of-truth, затем применить ближайший официальный style guide и локальные правила проекта.
2. Форматирование должно быть автоматизировано. Agent не должен вручную оптимизировать пробелы, если есть Black, Ruff, Prettier, ESLint, gofmt, rustfmt, Clippy, Checkstyle, dotnet analyzers, clang-tidy, ktlint or equivalent.
3. Спагетти-код нужно определять поведенчески: много неявного состояния, длинные функции, смешение уровней абстракции, циклические зависимости, глобальные side effects, повторение бизнес-правил, слабые имена и отсутствие локальных тестовых точек.
4. ООП полезно, когда класс защищает инвариант и уменьшает coupling. ООП вредно, когда вводит inheritance, mutable state and indirection без domain reason.
5. Рефакторинг должен начинаться с characterization or regression tests, особенно если код legacy, shared or user-visible. Без тестов допустима только малая механическая правка с явным risk note.
6. Комментарии не должны дублировать код. Хороший комментарий фиксирует why, contract, invariant, lifecycle, failure mode, migration reason, security/privacy caveat or external protocol nuance.
7. Public API, SDK and plugin surfaces должны быть строже внутреннего кода: compatibility, versioning, deprecation path, docs, examples and contract tests.
8. Generated-by-agent code должен оставлять evidence trail: task scope, files touched, tests run, skipped checks, activation/fallback status and unresolved risks.
9. Для Product-Agent OS важно встроить standards в agent packet and review gate, а не только в один документ. Иначе агент прочитает правила как advice, но не докажет compliance.
10. Нельзя превращать standard в бюрократию: baseline должен быть коротким, enforceable and testable; расширенные правила включаются по risk profile.

## Draft contract для Product-Agent OS coding standard

Будущий стандарт можно оформить как `coding-standards.md` или skill/playbook и подключать его из Product-Agent OS task packet. Минимальный контракт:

```yaml
coding_standard_contract:
  language_profile:
    required: true
    examples: ["python", "typescript", "go", "rust", "java", "csharp", "cpp"]
  source_of_truth:
    required: true
    fields: ["nearest AGENTS.md", "framework docs", "existing patterns", "owned files", "test contract"]
  design_boundary:
    required: true
    fields: ["module owner", "public API", "state owner", "side effects", "fallback policy"]
  style_tools:
    required: true
    fields: ["formatter", "linter", "type checker", "static analyzer", "project command"]
  refactoring_policy:
    required: true
    fields: ["behavior preserved", "test before/after", "migration path", "rollback path"]
  comments_policy:
    required: true
    fields: ["why", "contract", "invariant", "security/privacy", "external protocol", "no obvious restatement"]
  testing_policy:
    required: true
    fields: ["unit", "integration", "contract", "e2e/browser where relevant", "negative cases"]
  security_policy:
    required: true
    fields: ["no secrets", "input validation", "least privilege", "redacted logs", "dependency trust"]
  evidence_policy:
    required: true
    fields: ["commands run", "results", "skipped gates", "activation proof", "fallback proof", "closure_level"]
```

## Standards matrix для AI-агентов

| Область | Baseline rule | Агентский анти-паттерн | Gate |
| --- | --- | --- | --- |
| Имена | Имена раскрывают domain role and unit of meaning. | `data`, `thing`, `manager`, `helper` без контекста. | Reviewer checks readability and domain alignment. |
| Функции | Одна причина изменения, один уровень абстракции внутри блока. | Long method, boolean flag branching, hidden global dependencies. | Complexity, tests, local call-site review. |
| Модули | Модуль владеет coherent responsibility and explicit public boundary. | Kitchen-sink utility files, circular imports, cross-layer shortcuts. | Dependency graph or import review for shared code. |
| ООП | Класс защищает invariant, lifecycle or polymorphic contract. | Inheritance for reuse only, mutable God object, anemic wrappers. | Constructor invariants, tests for behavior and substitutions. |
| Рефакторинг | Small behavior-preserving slices with tests. | Large rewrite under “cleanup” label. | Before/after tests and scoped diff. |
| Комментарии | Explain why, constraints, contracts and hazards. | Comment repeats code or hides unclear naming. | Comment audit in review. |
| Ошибки | Explicit error model and recoverability. | Swallowed exceptions, generic catch, silent fallback. | Negative tests and logs/diagnostics. |
| API | Schema-first or contract-first when public/integrated. | Breaking shape changes without version/deprecation. | Contract tests and compatibility statement. |
| Security | Validate boundaries, protect secrets, redact logs. | Prompt/source payloads stored raw, tokens in fixtures. | Secret scan/static analysis where available. |
| Evidence | Claim only what current run proved. | “Verified” after reading docs only. | Completion ledger and command evidence. |

## 135-source corpus

| ID | Source | Status | Coding-standard lesson |
| --- | --- | --- | --- |
| S001 | [OpenAI Codex best practices](https://developers.openai.com/codex/learn/best-practices) | official | Agent work needs clear context, scoped prompts, repo conventions and verification loops. |
| S002 | [OpenAI Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md) | official | Project instructions should be close to code and treated as durable execution context. |
| S003 | [OpenAI Codex skills](https://developers.openai.com/codex/skills) | official | Repeatable coding workflows belong in skills/playbooks instead of bloated global prompts. |
| S004 | [OpenAI Codex workflows](https://developers.openai.com/codex/workflows) | official | Coding standards should map to repeatable work surfaces and evidence-producing flows. |
| S005 | [OpenAI Codex use cases](https://developers.openai.com/codex/use-cases) | official | Agent coding guidance must cover implementation, review, testing, migration and docs use cases. |
| S006 | [OpenAI Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security) | official | Standards must preserve sandbox, approvals and explicit external-action boundaries. |
| S007 | [OpenAI AI-native engineering team guide](https://developers.openai.com/codex/guides/build-ai-native-engineering-team) | official | Agent team design needs role boundaries, review loops and human control points. |
| S008 | [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | official | Subjective code-quality improvements need eval criteria, baselines and repeatable scoring. |
| S009 | [OpenAI Agents SDK guardrails](https://openai.github.io/openai-agents-python/guardrails/) | official | Guardrails can block unsafe inputs/outputs, but they do not replace code review. |
| S010 | [OpenAI Agents SDK tracing](https://openai.github.io/openai-agents-python/tracing/) | official | Agent-generated code changes should be inspectable through traceable steps and evidence. |
| S011 | [PEP 8](https://peps.python.org/pep-0008/) | official | Python style prioritizes readability, consistency and project-local convention. |
| S012 | [PEP 257](https://peps.python.org/pep-0257/) | official | Python docstrings document public modules, classes, functions and usage contracts. |
| S013 | [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) | official | Python agent output should handle imports, naming, comments, tests and type usage consistently. |
| S014 | [Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) | official | Formatting debates should be delegated to an opinionated formatter where the project uses one. |
| S015 | [Ruff rules](https://docs.astral.sh/ruff/rules/) | official | Lint rules can enforce correctness, modernization and maintainability patterns automatically. |
| S016 | [pytest documentation](https://docs.pytest.org/) | official | Python refactoring should usually be protected by focused unit and fixture-driven tests. |
| S017 | [Hypothesis documentation](https://hypothesis.readthedocs.io/) | official | Property-based tests are useful for invariants, parsers, serializers and edge-heavy code. |
| S018 | [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html) | official | JavaScript standards need naming, module, typing and documentation consistency. |
| S019 | [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript) | community-maintained | Widely used community rules help normalize JS idioms, imports and object/array patterns. |
| S020 | [ESLint rules](https://eslint.org/docs/latest/rules/) | official | JavaScript style and bug prevention should be lint-enforced, not manually argued. |
| S021 | [Prettier documentation](https://prettier.io/docs/) | official | Formatting should be stable, automatic and separate from semantic review. |
| S022 | [StandardJS](https://standardjs.com/) | community-maintained | Zero-config style is useful when consistency matters more than custom preference. |
| S023 | [TypeScript coding guidelines](https://github.com/microsoft/TypeScript/wiki/Coding-guidelines) | official project guidance | TypeScript changes should respect compiler/project idioms and avoid unnecessary abstraction. |
| S024 | [Effective Go](https://go.dev/doc/effective_go) | official | Go code emphasizes simple names, composition, clear errors and idiomatic small interfaces. |
| S025 | [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments) | official wiki | Go review culture catches idiom, concurrency, error and API issues beyond formatting. |
| S026 | [gofmt](https://go.dev/blog/gofmt) | official | Mandatory formatting can remove style debate and keep review focused on behavior. |
| S027 | [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/) | official project guidance | Rust public APIs need naming, ownership, traits, errors and future compatibility discipline. |
| S028 | [Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/) | official | Rust style should be formatter-compatible and consistent with language tooling. |
| S029 | [Clippy](https://doc.rust-lang.org/clippy/) | official | Rust linting catches correctness, complexity and idiom issues before review. |
| S030 | [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) | official | Java style needs clear source structure, naming, imports and class/interface discipline. |
| S031 | [Oracle Code Conventions for Java](https://www.oracle.com/java/technologies/javase/codeconventions-contents.html) | official historical | Older conventions remain useful for readability, layout and naming background. |
| S032 | [Javadoc doc comment specification](https://docs.oracle.com/en/java/javase/22/docs/specs/javadoc/doc-comment-spec.html) | official | Public Java APIs need structured docs that tooling can render and validate. |
| S033 | [Checkstyle checks](https://checkstyle.sourceforge.io/checks.html) | official project docs | Java style gates can be encoded as automated checks for CI and agent verification. |
| S034 | [C# coding conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions) | official | C# standards combine naming, layout, language features and analyzer expectations. |
| S035 | [C# XML documentation comments](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/) | official | .NET public APIs should carry structured XML docs when exposed to consumers. |
| S036 | [.NET design guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/) | official | API shape, naming, exceptions and extensibility require stricter review than internal code. |
| S037 | [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) | official/community project | C++ code needs explicit ownership, lifetime, resource and safety rules. |
| S038 | [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html) | official | C++ style should constrain headers, ownership, naming and complexity. |
| S039 | [LLVM Coding Standards](https://llvm.org/docs/CodingStandards.html) | official project docs | Large C++ projects need explicit readability, comment and abstraction rules. |
| S040 | [SEI CERT C Coding Standard](https://wiki.sei.cmu.edu/confluence/display/c) | authoritative | C code requires security-oriented constraints around undefined behavior and memory safety. |
| S041 | [MISRA](https://misra.org.uk/) | standards body | Safety-critical standards show why some projects need strict subsets and compliance evidence. |
| S042 | [Swift API Design Guidelines](https://swift.org/documentation/api-design-guidelines/) | official | API naming should communicate use at call sites, not only declaration sites. |
| S043 | [Google Swift Style Guide](https://google.github.io/swift/) | official | Swift code needs conventions for naming, optionals, comments and file organization. |
| S044 | [Kotlin coding conventions](https://kotlinlang.org/docs/coding-conventions.html) | official | Kotlin standards cover idiomatic naming, layout, classes, functions and multiplatform consistency. |
| S045 | [Android Kotlin style guide](https://developer.android.com/kotlin/style-guide) | official | Platform style can override generic language style for Android codebases. |
| S046 | [PHP PSR-12](https://www.php-fig.org/psr/psr-12/) | official FIG standard | PHP code benefits from shared extended coding style rules across frameworks. |
| S047 | [PHP PER Coding Style](https://www.php-fig.org/per/coding-style/) | official FIG recommendation | Evolving style recommendations should be versioned and tool-aligned. |
| S048 | [Ruby Style Guide](https://rubystyle.guide/) | community-maintained | Community conventions can be effective when paired with RuboCop-style automation. |
| S049 | [Tidyverse style guide](https://style.tidyverse.org/) | official project guidance | R style demonstrates naming, pipes, functions and documentation as readability tools. |
| S050 | [SQLFluff rules](https://docs.sqlfluff.com/en/stable/reference/rules.html) | official | SQL formatting and anti-patterns need lint support because SQL diffs are otherwise noisy. |
| S051 | [Martin Fowler Refactoring book](https://martinfowler.com/books/refactoring.html) | primary methodology | Refactoring is behavior-preserving restructuring, not feature delivery disguised as cleanup. |
| S052 | [Refactoring catalog](https://refactoring.com/catalog/) | primary methodology | Agents should choose named, small refactorings instead of broad rewrite moves. |
| S053 | [Technical Debt](https://martinfowler.com/bliki/TechnicalDebt.html) | primary methodology | Debt language should distinguish deliberate tradeoffs from reckless quality loss. |
| S054 | [Code Smell](https://martinfowler.com/bliki/CodeSmell.html) | primary methodology | Smells are review prompts, not automatic proof that code is wrong. |
| S055 | [Strangler Fig Application](https://martinfowler.com/bliki/StranglerFigApplication.html) | primary methodology | Legacy replacement should route traffic incrementally with explicit fallback/retirement rules. |
| S056 | [Branch by Abstraction](https://martinfowler.com/bliki/BranchByAbstraction.html) | primary methodology | Large migrations can preserve mainline flow by abstracting seams before replacement. |
| S057 | [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html) | primary methodology | Domain concepts should shape names, boundaries and invariants. |
| S058 | [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html) | primary methodology | Model terms are only safe inside the context where they are defined. |
| S059 | [Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html) | primary methodology | Code names should align with the team's domain language. |
| S060 | [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture) | primary methodology | Core logic should be protected from external adapters and delivery mechanisms. |
| S061 | [SOLID relevance](https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html) | author methodology | SOLID should guide dependency and responsibility decisions, not force ceremony. |
| S062 | [Liskov Substitution Principle paper](https://www.cs.utexas.edu/~downing/papers/LSP-1996.pdf) | academic | Subtypes must preserve behavioral expectations, not only signatures. |
| S063 | [Dependency Inversion Principle](https://objectmentor.com/resources/articles/dip.pdf) | author methodology | High-level policy should not depend directly on low-level detail. |
| S064 | [DIP in the Wild](https://martinfowler.com/articles/dipInTheWild.html) | primary methodology | Dependency inversion must be grounded in real change pressure, not reflexive interface creation. |
| S065 | [Interface Segregation Principle](https://blog.cleancoder.com/uncle-bob/2014/05/12/TheInterfaceSegregationPrinciple.html) | author methodology | Clients should not depend on methods they do not use. |
| S066 | [Agile Alliance TDD](https://agilealliance.org/glossary/tdd/) | methodology glossary | TDD creates design feedback through short failing-test and implementation cycles. |
| S067 | [Agile Alliance ATDD](https://agilealliance.org/glossary/atdd/) | methodology glossary | Acceptance criteria should be clarified before building user-visible behavior. |
| S068 | [Agile Alliance BDD](https://agilealliance.org/glossary/bdd/) | methodology glossary | Behavioral examples can align product language, implementation and tests. |
| S069 | [Gherkin reference](https://cucumber.io/docs/gherkin/reference) | official | Scenario language should be precise enough for automation and human review. |
| S070 | [Example Mapping](https://cucumber.io/docs/bdd/example-mapping) | official | Ambiguous requirements can be decomposed into rules, examples and questions before coding. |
| S071 | [Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html) | primary methodology | Test suites need a balanced distribution, not only slow end-to-end checks. |
| S072 | [ISTQB Foundation Level](https://www.istqb.org/certifications/certified-tester-foundation-level) | certification body | Standard test vocabulary helps separate unit, integration, system and acceptance evidence. |
| S073 | [Testing Library guiding principles](https://testing-library.com/docs/guiding-principles) | official | UI tests should prefer user-observable behavior over implementation details. |
| S074 | [Playwright best practices](https://playwright.dev/docs/best-practices) | official | Browser tests should be resilient, isolated and user-oriented. |
| S075 | [Vitest guide](https://vitest.dev/guide/) | official | Modern JS/TS unit tests should integrate with project-native module and tooling setup. |
| S076 | [Jest snapshot testing](https://jestjs.io/docs/snapshot-testing) | official | Snapshots are useful only when reviewed as intentional behavior artifacts. |
| S077 | [Stryker mutation testing](https://stryker-mutator.io/docs/) | official | Mutation testing can reveal tests that execute code without asserting behavior. |
| S078 | [Pact documentation](https://docs.pact.io/) | official | Consumer-driven contracts help prevent integration drift across services. |
| S079 | [Codecov code coverage](https://docs.codecov.com/docs/code-coverage) | official | Coverage is a signal for test reach, not proof of correctness by itself. |
| S080 | [GitHub Actions token permissions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication) | official | CI automation should use least privilege by default. |
| S081 | [GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) | official | Ownership routing is part of code quality for shared or sensitive files. |
| S082 | [GitHub PR reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews) | official | Review workflows should produce explicit approvals, comments and requested changes. |
| S083 | [Google Engineering Practices Code Review](https://google.github.io/eng-practices/review/) | official | Reviews should optimize for codebase health while moving work forward. |
| S084 | [GitLab code review guidelines](https://docs.gitlab.com/development/code_review/) | official | Review guidance can encode severity, maintainability and collaboration expectations. |
| S085 | [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) | official spec | Change intent should be machine-readable enough for release and history tooling. |
| S086 | [JSDoc tags](https://jsdoc.app/about-block-inline-tags) | official | JavaScript comments can document API contracts when type systems are absent or partial. |
| S087 | [TSDoc](https://tsdoc.org/) | official | TypeScript API comments should follow a parser-friendly standard. |
| S088 | [TypeDoc](https://typedoc.org/) | official | Documentation generation should align with TypeScript symbol structure. |
| S089 | [Sphinx autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) | official | Python docs can be generated from code, but only if code comments remain meaningful. |
| S090 | [numpydoc format](https://numpydoc.readthedocs.io/en/latest/format.html) | official | Scientific Python APIs need structured parameters, returns, examples and notes. |
| S091 | [Google Python comments and docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) | official | Comments should explain tricky parts, not state what is already obvious. |
| S092 | [Doxygen documentation blocks](https://www.doxygen.nl/manual/docblocks.html) | official | Multi-language generated docs need consistent comment block structure. |
| S093 | [rustdoc guide](https://doc.rust-lang.org/rustdoc/how-to-write-documentation.html) | official | Rust docs can include examples that compile as documentation tests. |
| S094 | [Go doc comments](https://go.dev/doc/comment) | official | Go comments are part of the package API and should start from the declared identifier. |
| S095 | [Swift DocC](https://www.swift.org/documentation/docc/) | official | Documentation can be integrated into API browsing and tutorials. |
| S096 | [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) | official spec | REST-like APIs need explicit request, response, auth and error contracts. |
| S097 | [AsyncAPI Specification](https://www.asyncapi.com/docs/reference/specification/latest) | official spec | Event-driven systems need message/channel contracts, not only REST docs. |
| S098 | [JSON Schema](https://json-schema.org/specification) | official spec | Data shapes should be validated and shared across producers and consumers. |
| S099 | [GraphQL Specification](https://spec.graphql.org/) | official spec | Schema-first APIs need resolver behavior and compatibility discipline. |
| S100 | [gRPC core concepts](https://grpc.io/docs/what-is-grpc/core-concepts/) | official | RPC systems need service, method, streaming and type contracts. |
| S101 | [Google API Improvement Proposals](https://google.aip.dev/general) | official | Public API design benefits from consistent resource, naming, pagination and error rules. |
| S102 | [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/) | official company guidance | REST standards should include compatibility, security, errors and lifecycle rules. |
| S103 | [RFC 9110 HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) | official RFC | HTTP API behavior should align with standard method, status and caching semantics. |
| S104 | [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457) | official RFC | Error responses should be structured and machine-readable. |
| S105 | [CloudEvents](https://cloudevents.io/) | official spec project | Event metadata should be standardized for cross-system routing and observability. |
| S106 | [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) | government standard | Secure software practices should cover planning, protection, production and response. |
| S107 | [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | official | Security requirements should be verifiable, not only aspirational. |
| S108 | [OWASP Top 10](https://owasp.org/www-project-top-ten/) | official | Common web risk categories should influence review and negative tests. |
| S109 | [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) | official | API code needs explicit authorization, object-level access and rate/flow controls. |
| S110 | [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | official | AI-integrated code needs prompt injection, data leakage and tool-use risk controls. |
| S111 | [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) | official | Secrets must stay out of code, tests, docs, logs and generated artifacts. |
| S112 | [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | official | Logs should be useful, structured and privacy-safe. |
| S113 | [SLSA specification v1.1](https://slsa.dev/spec/v1.1/) | official spec | Build provenance and tamper resistance matter for release-ready code. |
| S114 | [OpenSSF Scorecard](https://scorecard.dev/) | official project | Repository health can be checked through automated supply-chain risk signals. |
| S115 | [SPDX 3.0.1](https://spdx.github.io/spdx-spec/v3.0.1/) | official spec | Dependency and license metadata should be machine-readable. |
| S116 | [CycloneDX specification](https://cyclonedx.org/specification/overview/) | official spec | SBOMs support dependency, vulnerability and supply-chain analysis. |
| S117 | [Semantic Versioning](https://semver.org/) | official spec | Public API changes should map to explicit versioning promises. |
| S118 | [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) | official project | Human-readable change history should separate added, changed, fixed and security items. |
| S119 | [GitHub secret scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning) | official | Repositories should guard against accidental credential disclosure. |
| S120 | [CodeQL documentation](https://codeql.github.com/docs/) | official | Semantic static analysis can catch security and correctness classes missed by linters. |
| S121 | [Sonar Cognitive Complexity](https://www.sonarsource.com/resources/cognitive-complexity/) | vendor methodology | Readability risk is not captured by cyclomatic complexity alone. |
| S122 | [Visual Studio maintainability index](https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-maintainability-index-range-and-meaning?view=vs-2022) | official | Maintainability metrics are trend signals, not final quality judgment. |
| S123 | [ISO/IEC 25010 overview](https://www.iso.org/standard/78176.html) | standards body | Software quality includes maintainability, reliability, security, usability and portability. |
| S124 | [ISO 25010 quality model portal](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) | standards portal | Quality attributes can be translated into review rubrics and acceptance criteria. |
| S125 | [NASA Power of Ten](https://spinroot.com/p10/) | primary safety guidance | Critical code benefits from strict simplicity, bounded loops and analyzability. |
| S126 | [Feature-Sliced Design](https://feature-sliced.github.io/documentation/) | official project | Frontend code can use domain/feature layers to reduce cross-feature coupling. |
| S127 | [C4 model](https://c4model.com/diagrams) | primary methodology | Architecture docs should connect code to containers, components and responsibilities. |
| S128 | [arc42 overview](https://arc42.org/overview) | official methodology | Architecture documentation can be lightweight but systematic. |
| S129 | [MADR](https://adr.github.io/madr/) | official project | Architecture decisions should record context, decision and consequences. |
| S130 | [Structurizr DSL](https://docs.structurizr.com/dsl) | official | Architecture models can be stored as code and reviewed with the repo. |
| S131 | [Mermaid syntax reference](https://mermaid.js.org/intro/syntax-reference.html) | official | Lightweight diagrams can be maintained in Markdown when used with discipline. |
| S132 | [PlantUML sequence diagrams](https://plantuml.com/sequence-diagram) | official | Sequence diagrams clarify runtime interactions and hidden coupling. |
| S133 | [Twelve-Factor App](https://12factor.net/) | primary methodology | Runtime code should separate config, backing services, logs and disposability concerns. |
| S134 | [DORA Four Keys](https://dora.dev/guides/dora-metrics-four-keys/) | official research project | Delivery quality needs flow and stability metrics, not only code style checks. |
| S135 | [OpenTelemetry documentation](https://opentelemetry.io/docs/) | official | Observability standards help connect code paths to traces, metrics and logs. |

## Предлагаемые plugin artifacts

| Artifact | Purpose | Evidence gate |
| --- | --- | --- |
| `docs/product-agent-os/coding-standards.md` | User-facing Russian guide for AI-agent coding standards. | Registry entry, docs check, review against this source packet. |
| `plugins/product-agent-os/assets/templates/workflows/coding-standards.md` | Reusable workflow template loaded during implementation and refactoring tasks. | Unit test that template is discoverable and renders required gates. |
| `plugins/product-agent-os/assets/templates/artifacts/coding-standard-checklist.md` | Agent-facing checklist for task packets and completion reports. | Fixture/eval that generated packet includes style, refactoring, comments, tests and evidence sections. |
| `tests/product_agent_os/test_coding_standards_artifacts.py` | Deterministic guard for new artifact presence and required markers. | Local unittest. |
| `docs/sources/registry.md` and `docs/sources/registry.en.md` | Compact source-route marker. | `tools/check_docs.py` and registry sync review. |

## Candidate coding rules

### Universal rules

- Read nearest instructions and existing code before editing.
- Prefer project-local patterns and official framework guidance over generic advice.
- Keep changes narrow; separate behavior change, refactor, formatting and docs when practical.
- Use automated formatters and linters where available.
- Preserve public API compatibility unless task explicitly authorizes breaking change.
- Do not introduce new abstraction without named pressure: duplication, complexity, domain invariant, testability, public contract or runtime boundary.
- Do not hide fallback or silent behavior changes.
- Do not store secrets, raw private data, raw chat logs or unredacted payloads in code, docs, fixtures, evals or generated artifacts.

### Refactoring rules

- Identify the smell before changing code: long method, duplicated logic, feature envy, shotgun surgery, primitive obsession, cyclic dependency, hidden temporal coupling, global mutable state or unclear ownership.
- Name the intended refactoring move when possible: extract function, extract class, move function, introduce parameter object, replace conditional with polymorphism, separate adapter, strangler routing or branch by abstraction.
- Add or locate tests before risky refactor.
- Keep behavior-preserving refactor separate from new feature behavior unless the source contract requires both.
- Record skipped verification as a gap instead of claiming success.

### OOP rules

- Use classes to model lifecycle, invariant, cohesive state or polymorphic protocol.
- Prefer composition over inheritance unless substitutability is explicit and tested.
- Keep constructors small and invariants explicit.
- Avoid service objects that accumulate unrelated behavior.
- Avoid interface extraction until there are multiple consumers, a test boundary or a real substitution/migration need.
- Keep domain language visible in class, method and value-object names.

### Commenting rules

- Comment why the code exists, what invariant it preserves, what contract it implements, what external behavior is surprising or what risk it mitigates.
- Do not comment every line or repeat code in prose.
- Public APIs require structured docs appropriate to the language.
- Complex migrations require comment or ADR context explaining temporary compatibility paths.
- Security and privacy comments should name boundary assumptions without exposing sensitive details.

### Testing rules

- Unit tests protect pure logic, invariants, parser/serializer behavior and error paths.
- Integration or contract tests protect service boundaries, schemas, database behavior and adapters.
- Browser/e2e tests are required for user-visible UI behavior when the task claims UI proof.
- Mutation/property tests are candidates for high-risk logic, rules engines and parsers.
- Coverage improves confidence only when assertions check meaningful behavior.

### Review and completion rules

- Review findings lead with correctness, security, data loss, regression and missing tests.
- Style feedback should cite project standard, automated rule or maintainability risk.
- Completion requires files changed, checks run, result, gaps and activation/fallback status when runtime behavior changed.
- If a gate was not run, report it as an accepted gap or blocker.

## Open gaps before turning this into an enforced standard

| Gap | Why it matters | Suggested next action |
| --- | --- | --- |
| Language-specific enforcement map is not yet wired into plugin templates. | The research packet is source evidence, not runtime behavior. | Add a generated checklist that dispatches by detected language and project tooling. |
| No current eval verifies that agents follow the coding standard. | A document alone will not change agent behavior reliably. | Add transcript/fixture evals for refactor, comment, API and security scenarios. |
| No plugin artifact yet records complexity thresholds. | Complexity gates can become arbitrary without per-language tooling. | Start with qualitative gates, then add tool-specific metrics where available. |
| Public docs page is not generated from this packet yet. | Users need a compact readable standard, not a 135-source research table. | Create a shorter `docs/product-agent-os/coding-standards.md` derived from this packet. |
| Runtime activation is not claimed. | This slice changes documentation only. | Treat closure as `docs_contract_ready` until templates/evals are implemented and verified. |

## Closure level

`docs_contract_ready`: this packet provides the source corpus, intermediate lessons and draft contract for a future Product-Agent OS coding standard. It does not implement plugin runtime routing, agent prompt injection, eval enforcement, browser proof, provider calls, git release actions or automation.
