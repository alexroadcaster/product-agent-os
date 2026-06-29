# Research: книжный корпус по senior-level написанию кода для AI-агентов

Source status: `book literature + local implementation audit`

```yaml
title: "AI-agent senior coding literature research corpus"
type: "research source packet"
status: "draft_research_packet"
checked_at: "2026-06-29"
book_count: 60
relationship_to_previous_packet: "extends ai-agent-coding-standards-research.md"
trust_level: "high for publisher/author pages and widely cited primary books; medium for marketplace pages used as bibliographic anchors"
verification_status: "book corpus collected; delta standards extracted; plugin enforcement not yet implemented"
privacy_status: "metadata-only; no secrets, raw private logs or customer payloads included"
```

## Назначение

Этот packet добавляет книжный слой к `ai-agent-coding-standards-research.md`. Предыдущий корпус уже закрыл style guides, formatters, linters, API contracts, testing, security and observability. Здесь фокус другой: как заставить AI-агента писать код как enterprise-разработчик с большим стажем, который сначала ищет leverage, стандартную возможность, существующий abstraction boundary или удаление кода, и только потом пишет новый код.

Главный принцип этого packet:

```text
Senior leverage rule:
  delete code > configure existing behavior > call standard library/framework >
  reuse existing project abstraction > add a tiny adapter > write custom logic >
  add a new dependency > invent a new framework.
```

Если агент может решить задачу одной строкой через стандартную библиотеку, SQL primitive, framework helper, language construct, existing service method или проверенный project utility, он должен доказать, почему не выбрал этот путь, прежде чем писать 50 строк нового кода.

## Что уже было учтено в предыдущем research packet

Предыдущий packet уже содержит:

- language style guides and formatters: PEP 8, Black, Ruff, ESLint, Prettier, gofmt, Clippy, Checkstyle, .NET conventions and others;
- refactoring and architecture basics: code smells, technical debt, DDD, bounded contexts, hexagonal architecture, SOLID, strangler and branch by abstraction;
- testing and review: TDD, ATDD, BDD, test pyramid, Playwright, mutation tests, contract tests, code review and ownership;
- comments and docs: docstrings, JSDoc, TSDoc, Javadoc, rustdoc, Go doc comments, OpenAPI, AsyncAPI, JSON Schema, GraphQL and gRPC;
- security and supply chain: NIST SSDF, OWASP, SLSA, Scorecard, SBOM, secret scanning and CodeQL.

## Новая дельта из книг

| Delta | Что добавить в стандарт | Почему предыдущего корпуса недостаточно |
| --- | --- | --- |
| Leverage-before-code | Перед кастомной реализацией агент обязан выполнить “existing capability scan”: stdlib, framework, current dependency, project helper, SQL/database primitive, cloud/platform primitive. | Style guides говорят как писать код; они слабее отвечают на вопрос, стоит ли писать этот код вообще. |
| Code-budget thinking | Для каждой задачи агент должен назвать минимальный working expression and smallest safe patch. | Предыдущий corpus ограничивал scope, но не требовал искать one-line/zero-line solution. |
| Strategic programming | Агент не должен принимать первый working patch, если он увеличивает complexity surface. | Тесты могут быть зелеными даже для плохой архитектурной сделки. |
| Deep modules | Разрешать abstraction только если она уменьшает cognitive load за простым интерфейсом. | SOLID/DDD могут быть истолкованы как повод плодить мелкие shallow classes. |
| Data-structure-first | Сначала выбрать правильное представление данных, потом писать алгоритм. | Линтеры не поймают ситуацию, где 50 строк цикла заменяются `set`, `Counter`, map, index or SQL aggregate. |
| Library literacy | Стандарт должен поощрять знание standard library and ecosystem primitives. | Предыдущий packet сказал “используй formatters”, но не закрепил “не изобретай стандартную операцию”. |
| Negative dependency rule | Новая dependency допустима только если она уменьшает total lifecycle cost and risk. | “Не изобретай велосипед” не означает “добавь пакет на любую мелочь”. |
| Legacy seam discipline | В legacy коде сначала создать seam/characterization proof, потом менять. | Общие refactoring правила не достаточно сильны для старого enterprise кода. |
| Operational code cost | Код, который работает сегодня, но не имеет timeout, retry policy, idempotency, logging and rollback semantics, создает будущий incident debt. | Web/security sources закрывают часть темы, но книги по enterprise operations усиливают runtime discipline. |
| Human readability budget | Код должен помещаться в голову reviewer; hidden cleverness запрещена даже при малом количестве строк. | One-line solution хороша только если она idiomatic, obvious and tested. |

## 60-book corpus

| ID | Book | Source anchor | New lesson for AI-agent coding standard |
| --- | --- | --- | --- |
| B001 | John Ousterhout, `A Philosophy of Software Design` | [book site](https://web.stanford.edu/~ouster/cgi-bin/book.php) | Complexity is accumulated through dependencies and obscurity; prefer deep modules with simple interfaces over shallow abstractions. |
| B002 | Steve McConnell, `Code Complete` | [Microsoft Press](https://www.microsoftpressstore.com/store/code-complete-9780735619678) | Construction quality comes from deliberate design, routine-level discipline, defensive programming and choosing the right primitive before coding. |
| B003 | David Thomas and Andrew Hunt, `The Pragmatic Programmer` | [PragProg](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) | DRY, orthogonality, tracer bullets and broken-window discipline create a bias toward smaller, reusable, testable code. |
| B004 | Brian Kernighan and Rob Pike, `The Practice of Programming` | [Addison-Wesley](https://www.informit.com/store/practice-of-programming-9780201615869) | Clarity, simplicity, interfaces and tool composition beat clever custom implementation. |
| B005 | Robert C. Martin, `Clean Code` | [Pearson](https://www.pearson.com/en-us/subject-catalog/p/clean-code-a-handbook-of-agile-software-craftsmanship/P200000009984) | Naming, function size and responsibility matter, but AI-agent usage must avoid turning clean-code advice into excessive micro-abstractions. |
| B006 | Mark Seemann, `Code That Fits in Your Head` | [Pearson](https://www.pearson.com/en-us/subject-catalog/p/code-that-fits-in-your-head/P200000003488) | Reviewer cognition is a hard constraint; code should be small enough to reason about without hidden state. |
| B007 | Tom Long, `Good Code, Bad Code` | [Manning](https://www.manning.com/books/good-code-bad-code) | Robust code is written for future readers and failure modes, not only for happy-path execution. |
| B008 | Dustin Boswell and Trevor Foucher, `The Art of Readable Code` | [O'Reilly](https://www.oreilly.com/library/view/the-art-of/9781449318482/) | Readability is a first-class performance metric for maintenance. |
| B009 | Christian Clausen, `Five Lines of Code` | [Manning](https://www.manning.com/books/five-lines-of-code) | Tiny refactoring steps are safer than large rewrites; line count can be used as a design smell signal. |
| B010 | Martin Fowler, `Refactoring` | [refactoring.com](https://martinfowler.com/books/refactoring.html) | Behavior-preserving changes require named moves and test-backed small steps. |
| B011 | Joshua Kerievsky, `Refactoring to Patterns` | [Addison-Wesley](https://www.informit.com/store/refactoring-to-patterns-9780321213358) | Patterns should emerge from repeated pressure, not be inserted before the simpler design fails. |
| B012 | Michael Feathers, `Working Effectively with Legacy Code` | [Pearson](https://www.pearson.com/en-us/subject-catalog/p/working-effectively-with-legacy-code/P200000009987) | Legacy code needs seams and characterization tests before meaningful refactor. |
| B013 | Sandi Metz and Katrina Owen, `99 Bottles of OOP` | [book site](https://sandimetz.com/99bottles) | Good design can be practiced through tiny changes that reduce duplication without premature abstraction. |
| B014 | Sandi Metz, `Practical Object-Oriented Design` | [Pearson](https://www.pearson.com/en-us/subject-catalog/p/practical-object-oriented-design-an-agile-primer-using-ruby/P200000009590) | Objects should have clear responsibilities, stable dependencies and minimal knowledge of each other. |
| B015 | Erich Gamma et al., `Design Patterns` | [Addison-Wesley](https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-software-9780201633610) | Patterns are vocabulary for recurring design forces, not a checklist to apply everywhere. |
| B016 | Martin Fowler, `Patterns of Enterprise Application Architecture` | [martinfowler.com](https://martinfowler.com/books/eaa.html) | Enterprise code must make transaction, data access, mapping and domain boundaries explicit. |
| B017 | Gregor Hohpe and Bobby Woolf, `Enterprise Integration Patterns` | [book site](https://www.enterpriseintegrationpatterns.com/) | Integration code should use known message, routing and transformation patterns instead of ad hoc glue. |
| B018 | Eric Evans, `Domain-Driven Design` | [Addison-Wesley](https://www.informit.com/store/domain-driven-design-tackling-complexity-in-the-heart-9780321125217) | Domain language and model boundaries prevent duplicated business logic and inconsistent terminology. |
| B019 | Vaughn Vernon, `Implementing Domain-Driven Design` | [Addison-Wesley](https://www.informit.com/store/implementing-domain-driven-design-9780321834577) | DDD needs tactical patterns, aggregates and bounded contexts tied to real domain constraints. |
| B020 | Vlad Khononov, `Learning Domain-Driven Design` | [O'Reilly](https://www.oreilly.com/library/view/learning-domain-driven-design/9781098100124/) | Choose patterns by business complexity; not every component deserves heavyweight modeling. |
| B021 | Harry Percival and Bob Gregory, `Architecture Patterns with Python` | [book site](https://www.cosmicpython.com/) | Ports, adapters, unit of work and repositories are useful when they protect core logic from infrastructure churn. |
| B022 | Rebecca Wirfs-Brock and Alan McKean, `Object Design` | [Addison-Wesley](https://www.informit.com/store/object-design-roles-responsibilities-and-collaborations-9780201379433) | Responsibilities and collaborations are often clearer than class taxonomies. |
| B023 | Bertrand Meyer, `Object-Oriented Software Construction` | [Prentice Hall](https://www.pearson.com/en-us/subject-catalog/p/object-oriented-software-construction/P200000003240) | Contracts and invariants are stronger design tools than comments that merely describe intent. |
| B024 | Joshua Bloch, `Effective Java` | [Addison-Wesley](https://www.informit.com/store/effective-java-9780134685991) | Use standard libraries, immutable objects, builders and clear API contracts before custom machinery. |
| B025 | Brett Slatkin, `Effective Python` | [Pearson](https://www.pearson.com/en-us/subject-catalog/p/effective-python-90-specific-ways-to-write-better-python/P200000009615) | Pythonic leverage often means built-ins, comprehensions, generators, context managers and standard library types. |
| B026 | Scott Meyers, `Effective Modern C++` | [O'Reilly](https://www.oreilly.com/library/view/effective-modern-c/9781491908419/) | Modern language features can delete boilerplate and make ownership explicit. |
| B027 | Dan Vanderkam, `Effective TypeScript` | [O'Reilly](https://www.oreilly.com/library/view/effective-typescript/9781492053736/) | Type systems should remove invalid states and repetitive runtime checks where practical. |
| B028 | Jon Bentley, `Programming Pearls` | [Addison-Wesley](https://www.informit.com/store/programming-pearls-9780201657883) | Problem framing, data representation and back-of-envelope reasoning can replace large naive implementations. |
| B029 | Steven Skiena, `The Algorithm Design Manual` | [Springer](https://link.springer.com/book/10.1007/978-3-030-54256-6) | Algorithm selection is a senior skill; the right data structure can collapse many lines of procedural code. |
| B030 | Robert Sedgewick and Kevin Wayne, `Algorithms` | [book site](https://algs4.cs.princeton.edu/home/) | Standard algorithmic vocabulary helps agents avoid custom inefficient loops. |
| B031 | Harold Abelson, Gerald Jay Sussman and Julie Sussman, `Structure and Interpretation of Computer Programs` | [MIT Press](https://mitpress.mit.edu/9780262510875/structure-and-interpretation-of-computer-programs/) | Abstraction, composition and evaluation models are core to writing less but more powerful code. |
| B032 | Eric S. Raymond, `The Art of Unix Programming` | [book site](http://www.catb.org/~esr/writings/taoup/html/) | Compose tools, prefer text/data protocols and keep programs focused. |
| B033 | Brian Kernighan and Rob Pike, `The Unix Programming Environment` | [Prentice Hall](https://www.pearson.com/en-us/subject-catalog/p/unix-programming-environment/P200000003220) | Tool composition can replace bespoke application logic. |
| B034 | Martin Kleppmann, `Designing Data-Intensive Applications` | [O'Reilly](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) | Data systems require explicit thinking about consistency, indexes, streams, replication and failure. |
| B035 | Michael Nygard, `Release It!` | [PragProg](https://pragprog.com/titles/mnee2/release-it-second-edition/) | Production code must consider timeouts, retries, bulkheads, circuit breakers and stability patterns. |
| B036 | Sam Newman, `Building Microservices` | [O'Reilly](https://www.oreilly.com/library/view/building-microservices-2nd/9781492034018/) | Service splitting is justified by independent change/deploy needs, not by fashion. |
| B037 | Sam Newman, `Monolith to Microservices` | [O'Reilly](https://www.oreilly.com/library/view/monolith-to-microservices/9781492047834/) | Migration should be incremental and reversible, not a broad rewrite. |
| B038 | Dan Bergh Johnsson, Daniel Deogun and Daniel Sawano, `Secure by Design` | [Manning](https://www.manning.com/books/secure-by-design) | Security can be embedded into domain modeling through invariants and secure defaults. |
| B039 | JJ Geewax, `API Design Patterns` | [Manning](https://www.manning.com/books/api-design-patterns) | APIs should reuse proven resource, pagination, filtering, idempotency and long-running operation patterns. |
| B040 | Arnaud Lauret, `The Design of Web APIs` | [Manning](https://www.manning.com/books/the-design-of-web-apis) | API design starts with consumer goals and consistent contracts, not controller code. |
| B041 | Bill Karwin, `SQL Antipatterns` | [PragProg](https://pragprog.com/titles/bksqla/sql-antipatterns-volume-1/) | Database primitives should replace application-level reinvention, but schema and query antipatterns must be avoided. |
| B042 | Scott Ambler and Pramod Sadalage, `Refactoring Databases` | [Addison-Wesley](https://www.informit.com/store/refactoring-databases-evolutionary-database-design-9780321293534) | Data changes need migration, compatibility and rollback discipline. |
| B043 | Kent Beck, `Test Driven Development: By Example` | [Addison-Wesley](https://www.informit.com/store/test-driven-development-by-example-9780321146533) | Tests can drive smaller code by forcing the simplest passing implementation. |
| B044 | Gerard Meszaros, `xUnit Test Patterns` | [Addison-Wesley](https://www.informit.com/store/xunit-test-patterns-refactoring-test-code-9780131495050) | Test code has design smells too; bad tests create maintenance debt. |
| B045 | Steve Freeman and Nat Pryce, `Growing Object-Oriented Software, Guided by Tests` | [Addison-Wesley](https://www.informit.com/store/growing-object-oriented-software-guided-by-tests-9780321503626) | Tests can shape ports, adapters and object collaborations from outside-in behavior. |
| B046 | Jez Humble and David Farley, `Continuous Delivery` | [Addison-Wesley](https://www.informit.com/store/continuous-delivery-reliable-software-releases-through-9780321601919) | Code quality includes deployability, repeatable builds and safe release paths. |
| B047 | Nicole Forsgren, Jez Humble and Gene Kim, `Accelerate` | [IT Revolution](https://itrevolution.com/product/accelerate/) | High performance comes from small batches, fast feedback and reliability, not heroic large changes. |
| B048 | Dave Farley, `Modern Software Engineering` | [Pearson](https://www.pearson.com/en-us/subject-catalog/p/modern-software-engineering/P200000009421) | Engineering means optimizing for learning, feedback and empirical quality gates. |
| B049 | Mary and Tom Poppendieck, `Lean Software Development` | [Addison-Wesley](https://www.informit.com/store/lean-software-development-an-agile-toolkit-9780321150783) | Eliminate waste: unused abstractions, handoffs, waiting, overbuilt code and partially done work. |
| B050 | Titus Winters, Tom Manshreck and Hyrum Wright, `Software Engineering at Google` | [O'Reilly](https://www.oreilly.com/library/view/software-engineering-at/9781492082781/) | Code is maintained over time by many people; local cleverness must yield to maintainability at scale. |
| B051 | Frederick Brooks, `The Mythical Man-Month` | [Addison-Wesley](https://www.informit.com/store/mythical-man-month-essays-on-software-engineering-anniversary-9780201835953) | Conceptual integrity beats adding people, features or complexity to compensate for weak design. |
| B052 | Tom DeMarco and Timothy Lister, `Peopleware` | [Addison-Wesley](https://www.informit.com/store/peopleware-productive-projects-and-teams-9780321934116) | Code standards should protect team cognition and ownership, not only compiler output. |
| B053 | Matthew Skelton and Manuel Pais, `Team Topologies` | [IT Revolution](https://itrevolution.com/product/team-topologies/) | Architecture should match team boundaries to reduce cognitive load and accidental coupling. |
| B054 | Gene Kim et al., `The DevOps Handbook` | [IT Revolution](https://itrevolution.com/product/the-devops-handbook-second-edition/) | Flow, feedback and continuous learning should influence code structure and release safety. |
| B055 | Eric Normand, `Grokking Simplicity` | [Manning](https://www.manning.com/books/grokking-simplicity) | Separate data, calculations and actions to reduce hidden side effects. |
| B056 | Paul Chiusano and Runar Bjarnason, `Functional Programming in Scala` | [Manning](https://www.manning.com/books/functional-programming-in-scala) | Pure functions, composition and types can remove mutable-state code and reduce tests needed for simple transformations. |
| B057 | Scott Wlaschin, `Domain Modeling Made Functional` | [PragProg](https://pragprog.com/titles/swdddf/domain-modeling-made-functional/) | Make invalid states unrepresentable and encode domain workflows in types. |
| B058 | Jenifer Tidwell, `Designing Interfaces` | [O'Reilly](https://www.oreilly.com/library/view/designing-interfaces-3rd/9781492051954/) | User-facing code should reuse known interaction patterns instead of custom UI mechanics. |
| B059 | Steve Krug, `Don't Make Me Think` | [book site](https://sensible.com/dont-make-me-think/) | Interface and flow decisions should reduce user cognition; clever custom UI is often product debt. |
| B060 | Tanya Reilly, `The Staff Engineer's Path` | [O'Reilly](https://www.oreilly.com/library/view/the-staff-engineers/9781098118723/) | Senior engineering leverage is often choosing the right small intervention rather than writing more code. |

## New standards to add to AI-agent coding rules

### 1. Existing Capability Scan

Before writing custom logic, the agent must check:

1. Can the behavior be deleted because it is already handled elsewhere?
2. Can configuration, schema, query, framework routing or platform setting do it?
3. Does the language standard library already provide it?
4. Does the project already have a helper/service/repository/query for it?
5. Does a current dependency already provide it?
6. If a new dependency is considered, does it reduce total lifecycle risk?
7. If custom code remains necessary, what is the smallest local implementation?

Completion evidence should include one line:

```yaml
existing_capability_scan: "stdlib/project-helper/framework checked; custom code justified because ..."
```

### 2. One-Line Candidate Rule

For small transformations, parsing, filtering, grouping, aggregation, validation and formatting tasks, the agent must first write down a one-line or zero-new-code candidate. It may reject the candidate only if it is less readable, less safe, less performant, not idiomatic for the project, or violates error/security requirements.

Examples:

```python
# Prefer a standard type over a manual counting loop.
counts = Counter(event.type for event in events)
```

```python
# Prefer built-in aggregation over custom max tracking.
best = max(candidates, key=attrgetter("score"), default=None)
```

```python
# Prefer a set operation over nested loops for membership.
missing = required_ids - seen_ids
```

```typescript
// Prefer platform URL parsing over custom query parsing.
const params = new URLSearchParams(url.search);
```

```sql
-- Prefer database atomicity over read-then-write application races.
INSERT INTO settings (key, value) VALUES (:key, :value)
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;
```

These examples are patterns, not universal prescriptions. If project style, performance profile or compatibility constraints disagree, local source-of-truth wins.

### 3. Negative Dependency Rule

The agent must not solve “do not reinvent the wheel” by blindly adding packages. A new dependency needs:

- clear owner and maintenance status;
- license and supply-chain review appropriate to project risk;
- security posture or vulnerability check where available;
- compatibility with runtime, bundling and deployment constraints;
- proof that standard library, framework and existing project dependency options are worse;
- removal/rollback path.

Small custom code can be better than a dependency when the behavior is tiny, stable, well-tested and domain-specific. A dependency can be better when the domain is complex, security-sensitive, standardized or already project-approved.

### 4. Strategic Programming Gate

Borrowing from strategic programming and lean software development, the agent must not stop at “tests pass” if the patch increases future complexity. A patch is suspect when it:

- adds a new abstraction with only one call site and no clear future pressure;
- duplicates business rules already present in schema, domain service or API contract;
- moves logic across layers to avoid using the existing boundary;
- adds mutable shared state for convenience;
- introduces fallback behavior without activation/fallback proof;
- creates code that is hard to delete when the feature changes.

### 5. Deep Module Gate

An abstraction is allowed when it makes the interface simpler than the implementation. It is suspicious when the interface is almost as complex as the implementation.

Agent checklist:

- Can the caller understand the module without reading its internals?
- Does the module own a real invariant, lifecycle, policy or integration boundary?
- Is the abstraction hiding complexity or merely renaming it?
- Would one direct standard-library call be clearer?

### 6. Data-Structure-First Rule

Before writing loops or condition-heavy code, the agent should choose the data representation:

- `set` for membership and difference;
- `dict`/`Map` for lookup;
- `Counter`/grouping primitive for frequency;
- sorted/indexed structure for range queries;
- SQL aggregate/window/upsert when the database owns the data;
- type/value object when invalid states should be impossible;
- state machine when lifecycle transitions matter.

### 7. Legacy Seam Rule

For legacy code, the agent must not do broad cleanup first. It should:

1. find the seam;
2. add characterization or regression coverage;
3. make the smallest behavior-preserving change;
4. name remaining debt explicitly;
5. avoid combining cleanup with feature behavior unless approved by the source contract.

### 8. Enterprise Runtime Rule

Enterprise code includes operational behavior. For network, queue, job, database, file, provider, payment or external API code, the agent must consider:

- idempotency;
- timeout and cancellation;
- retry policy and backoff;
- circuit breaker or bulkhead where scale justifies it;
- transaction boundary;
- data consistency;
- observability;
- privacy-safe logging;
- rollback and compatibility.

### 9. Code Deletion Bias

The best senior fix may be deletion:

- remove dead branch after proving route is unused;
- replace custom helper with framework/stdlib call;
- collapse duplicate business rule into one source of truth;
- remove feature flag only after activation/fallback proof;
- delete test fixture noise that hides meaningful assertions.

Agent completion should record whether deletion/reuse was considered.

### 10. Cleverness Budget

One-line code is not automatically senior code. It is acceptable only when it is idiomatic, readable, testable and obvious to the project team. If the one-liner hides tricky behavior, prefer two or three clear lines with named intermediate values.

## Enterprise leverage checklist for future plugin template

```yaml
enterprise_leverage_check:
  existing_capability_scan:
    stdlib_checked: true
    framework_checked: true
    current_dependencies_checked: true
    project_helpers_checked: true
    database_or_platform_primitive_checked: true
  implementation_choice:
    selected_path: "delete | configure | stdlib | framework | project_helper | current_dependency | tiny_custom_code | new_dependency"
    reason: ""
    rejected_simpler_paths: []
  debt_controls:
    new_abstraction_count: 0
    new_dependency_count: 0
    duplicate_business_rule_count: 0
    legacy_seam_or_gap: ""
  evidence:
    tests_or_gap: ""
    runtime_or_gap: ""
    reviewer_focus: ["correctness", "maintainability", "debt", "dependency risk"]
```

## New review questions for AI-agent code

| Question | Bad answer | Good answer |
| --- | --- | --- |
| What existing capability was checked? | “I wrote a helper.” | “Project already uses `Counter`/repository method/framework validator; reused it.” |
| Why is this custom code necessary? | “It was straightforward.” | “Stdlib and project helper do not cover domain-specific validation; custom code is 8 lines with tests.” |
| Did this add debt? | “No, tests pass.” | “Adds a temporary adapter; removal condition is version X migration.” |
| Is this abstraction deep? | “It has a class.” | “It hides provider retry/idempotency behind a small domain interface.” |
| Is the one-liner readable? | “It is short.” | “It uses a common project idiom; added named variable where expression became dense.” |
| Did this add dependency risk? | “Package is popular.” | “Existing dependency already covered it, so no new dependency was added.” |

## Standards not to add blindly

- Do not mandate microservices, DDD, functional programming, TDD, design patterns, Clean Architecture or heavy OOP for every task.
- Do not turn line count into a mechanical metric. It is a smell, not proof.
- Do not prefer one-liners when they reduce clarity or hide failure modes.
- Do not add dependencies for trivial code.
- Do not use patterns as decoration.
- Do not refactor legacy code broadly without seam and characterization evidence.
- Do not claim enterprise readiness without operational semantics for failure-prone boundaries.

## Candidate updates to previous coding standard contract

Add these fields to the previous `coding_standard_contract`:

```yaml
leverage_policy:
  required: true
  fields:
    - "existing_capability_scan"
    - "one_line_candidate_or_reason_not_applicable"
    - "selected_path"
    - "new_dependency_justification"
    - "code_deletion_considered"
    - "deep_module_check"
    - "legacy_seam_check"
```

## Closure level

`docs_contract_ready`: this packet adds a 60-book literature corpus and extracts delta standards for senior-level AI-agent coding. It does not implement plugin routing, task packet enforcement, evals, hooks, browser/runtime proof, provider calls, git release actions or automation.
