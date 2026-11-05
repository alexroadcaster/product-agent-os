---
title: "Архив — Quality, Testing & Evals Methodology Research"
---

# Архив — Quality, Testing & Evals Methodology Research {#quality-testing-evals-methodology-research}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

Source status: `official + expert reference + vendor documentation + tool-assisted`

Research date: `2026-05-24`

Target methodology page: [../../methodologies/quality-testing-evals.md](../../methodologies/quality-testing-evals.md)

Target Product-Agent OS behavior: route every meaningful change through the smallest useful verification path, require current evidence before completion claims, separate deterministic tests from subjective evals, and block risky work when traceability, runtime evidence, contract checks or residual-risk records are missing.

## Scope

This dossier covers deterministic tests, acceptance scenarios, contract tests, integration/runtime tests, browser/mobile/native evidence, documentation checks, AI and subjective evals, CI quality gates, flaky test management, coverage, mutation/property-based testing, manual QA evidence and evidence-before-completion.

It does not mandate one test runner, 100 percent coverage, universal TDD, universal E2E testing or mandatory AI evals for every project. The method selects checks by product risk, architecture surface, user-visible behavior, data sensitivity and release impact.

## Supported facts

- Agile Alliance defines Test-Driven Development (TDD) as a cycle where tests are written before programming and coding, unit testing and refactoring are intertwined.
- Agile Alliance defines Acceptance Test-Driven Development (ATDD) as expressing acceptance tests before implementation through customer, developer and tester perspectives.
- Agile Alliance describes Behavior-Driven Development (BDD) as using executable scenarios and shared behavior language to improve communication across business, testing and development.
- The practical Test Pyramid guidance emphasizes a balanced portfolio with tests at different granularity, many fast lower-level tests and fewer high-level tests.
- Modern frontend guidance such as the Testing Trophy emphasizes static checks and integration tests for browser-oriented applications, but it is an expert heuristic, not a universal standard.
- ISTQB Foundation Level guidance separates confirmation testing from regression testing, recommends impact analysis for regression scope and treats automated regression tests as a good fit for CI.
- pytest documentation states that pytest supports small readable tests, assertion introspection, auto-discovery, modular fixtures, parametrization, CI guidance and flaky-test guidance.
- Vitest documentation describes watch mode for development, run mode in CI, projects, snapshots, coverage through V8 or Istanbul, browser mode and isolation tradeoffs.
- Playwright Test supports retries, classifies tests as passed, flaky or failed, and can capture traces on retry. Trace Viewer, screenshots and visual comparisons provide browser runtime evidence.
- Playwright visual comparison guidance requires stable environments for reliable screenshot baselines.
- Pact documents consumer-driven contract testing and provider verification for HTTP and message integrations.
- Stryker mutation testing changes code under test and checks whether the test suite detects the mutants; mutation score is a signal about test effectiveness, not product correctness by itself.
- Hypothesis is a property-based testing library for Python that generates examples from stated properties and can reveal edge cases missed by example-based tests.
- GitHub Actions workflow syntax defines CI jobs, events, permissions, environments, matrix runs and reusable workflow structures. `GITHUB_TOKEN` permissions should be scoped deliberately.
- Code coverage measures executed code, but coverage alone does not prove requirements, critical paths, contracts or user-visible behavior.
- OpenAI evaluation guidance treats evals as systematic tests for AI applications and agent workflows, with datasets, graders, thresholds and regression loops.
- Codex AI app eval guidance recommends adding a runnable eval suite before prompt, model, retrieval or agent changes merge.
- Promptfoo provides declarative LLM app evaluation and red-team workflows with assertions, CI usage and metrics.
- Ragas documents RAG and agent metrics such as faithfulness, answer relevancy, context precision/recall and tool call accuracy.

## Assumptions

- Product-Agent OS should generate framework-neutral quality artifacts first, then specialize to pytest, Vitest, Playwright, JUnit, Promptfoo, Ragas or other stack tools when detected.
- Completion evidence should live in `RUNLOG.md` or a slice-specific evidence packet, while durable strategy belongs in `TEST.md` and `EVALS.md`.
- CI is a verification surface, not an approval surface. Creating or changing external CI workflows should remain staged until explicitly approved.
- Coverage thresholds are useful only when paired with requirement, critical-path and regression coverage.

## Unsupported claims not adopted

- "More tests always means better quality." The useful signal is risk coverage, fast feedback and failure usefulness.
- "100 percent line coverage proves correctness." It does not prove assertions, behavior, contracts or user outcomes.
- "E2E tests are the most realistic, so they should dominate." High-level tests are valuable but slower and more brittle.
- "Manual QA is not evidence." Manual QA can be evidence when it has a charter, criteria, environment and captured result.
- "AI evals are optional for AI behavior changes." For AI-facing behavior, prompt/model/retrieval/tool changes need baseline or explicit baseline gap.

## Methodologies

| Methodology | When to apply | Project-level behavior |
| --- | --- | --- |
| TDD / Red-Green-Refactor | Deterministic logic, bugfixes, parser/validator/business rules | Write failing test, run failure, implement minimal fix, rerun pass, refactor with tests green. |
| ATDD / BDD | Product behavior, workflow, business rules | Acceptance scenario maps requirement to executable check or explicit manual/eval evidence. |
| Test portfolio design | Any non-trivial project | Select static, unit, integration, contract, E2E, manual and eval checks by risk and feedback speed. |
| Risk-based testing | Time, CI budget or risk is constrained | Prioritize checks by user impact, change risk, data/security exposure and historical failure rate. |
| Confirmation and regression testing | Bugfixes, migrations, refactors, dependency changes | Reproduce original failure, prove fix, then check impacted unchanged behavior. |
| Contract testing | APIs, events, generated clients, external consumers | Validate provider/consumer expectations and compatibility before integration or release claims. |
| Integration testing | Behavior depends on database, filesystem, queue, network or service boundary | Exercise real or high-fidelity dependencies with reset strategy and failure evidence. |
| E2E/runtime testing | User-visible workflow or platform-specific behavior | Browser/simulator/API/runtime path evidence with logs, screenshots, traces or reports. |
| Visual and accessibility testing | UI layout, design system or custom widget behavior | Stable screenshots, component states, keyboard/focus/a11y checks and accepted diffs. |
| Property-based testing | Invariants, parsers, serializers, permissions, math, state transitions | Generate many inputs from declared properties and keep shrinking/failing examples. |
| Mutation testing | Tests pass but assertion quality is uncertain | Mutate source behavior and inspect surviving mutants for weak assertions or missing cases. |
| Flaky test management | Intermittent failures, timing, network, parallelism, browser tests | Classify source, isolate, quarantine only with owner and expiry, keep flaky evidence visible. |
| CI quality gates | Shared branches, PRs, releases, packages | Run deterministic checks with scoped permissions, artifacts, exact commands and exit codes. |
| Eval-driven quality | AI, docs, UX, search relevance, subjective outputs | Dataset, rubric, grader, threshold, baseline/current run and failure review. |
| Exploratory testing | New workflows, unknown risk, usability, edge discovery | Time-boxed charter, environment, notes, findings and follow-up checks. |
| Evidence-before-completion | Every meaningful slice | Current command/eval/runtime/manual evidence or explicit inspection-only gap before success claims. |

## Documentation artifacts and standards

| Artifact | Purpose | Candidate location |
| --- | --- | --- |
| Test strategy | Quality model, test portfolio, risk tiers, ownership and CI gates. | `TEST.md` |
| Test/eval matrix | Requirement to scenario to check to evidence owner mapping. | `test-eval-matrix.md` |
| Acceptance scenarios | Business/user behavior expressed as examples with expected and forbidden outcomes. | `acceptance-scenarios.md` |
| Red-Green-Refactor log | Bug or deterministic behavior proof with failing and passing command evidence. | `RUNLOG.md`, `red-green-refactor-log.md` |
| Bug reproduction record | Original failure, reproduction steps, environment, fixture and fixed evidence. | `bug-reproduction.md` |
| Risk-based test plan | Risk areas, impact, likelihood, selected checks and accepted gaps. | `risk-based-test-plan.md` |
| Regression impact map | Changed files/contracts/data and impacted behavior to rerun. | `regression-impact-map.md` |
| Contract test map | API/event/schema contracts, consumers, providers and verification command. | `contract-test-map.md` |
| Runtime evidence packet | Browser/API/native/desktop/server command, environment, logs, screenshots and traces. | `runtime-evidence.md` |
| Visual/a11y evidence packet | Viewports, component states, screenshots, accepted diffs, keyboard/focus/a11y result. | `visual-a11y-evidence.md` |
| Coverage policy | Coverage type, threshold, excluded files, critical-path mapping and non-goals. | `coverage-policy.md` |
| Mutation test report | Scope, mutation score, surviving mutants, ignored mutants and follow-up tests. | `mutation-test-report.md` |
| Property test spec | Invariants, input generators, shrink/failure examples and seed handling. | `property-test-spec.md` |
| Flaky test ledger | Test, symptom, suspected source, owner, quarantine expiry and rerun evidence. | `flaky-test-ledger.md` |
| CI quality gate proposal | Jobs, permissions, triggers, artifacts, cache, matrix and rollback. | `ci-quality-gates.md` |
| Eval spec | Objective, dataset, grader, rubric, threshold, command and owner. | `EVALS.md`, `ai-eval-spec.md` |
| Eval run report | Baseline/current score, passing/failing cases, regressions and residual risk. | `eval-run-report.md` |
| Manual QA charter | Scope, environment, checklist, notes, findings and reviewer. | `manual-qa-charter.md` |
| Completion evidence packet | Commands run, exit codes, outputs, artifacts, accepted gaps and residual risks. | `RUNLOG.md`, `evidence-packet.md` |

## Project application instructions

1. Start each slice by naming the user-visible behavior or technical contract that needs evidence.
2. Choose the smallest useful verification path. A pure parser may need unit/property tests; a checkout flow may need integration/E2E; an AI answer may need evals.
3. Map every acceptance criterion to a deterministic check, contract check, runtime check, eval, manual charter or explicit gap.
4. For bugfixes, capture reproduction evidence first when feasible. If reproduction is impossible, record the gap and risk before changing code.
5. Use TDD when behavior is deterministic and the failure can be expressed cheaply. Do not force TDD for exploratory UI, visual design or ambiguous product discovery.
6. Keep test layers purposeful. Unit tests check local rules, integration tests check collaboration, contract tests check compatibility, E2E tests check user/runtime path.
7. For API or event changes, require contract source and consumer/provider verification or an explicit compatibility gap.
8. For UI changes, capture runtime evidence for layout, responsive states, interaction, keyboard/focus and accessibility when relevant.
9. For native/mobile/desktop changes, use platform build/run/log/screenshot evidence rather than code inspection only.
10. For AI, search, ranking, docs quality or subjective behavior, use eval datasets, rubrics, graders and thresholds.
11. Use coverage as a gap-finding tool, not as the only quality target. Pair coverage with requirement and critical-path coverage.
12. Use mutation/property-based testing when ordinary examples are likely to miss edge cases or weak assertions.
13. Treat flaky tests as product-quality debt. Retries may collect evidence, but they do not remove the need to classify and fix the cause.
14. CI changes should specify triggers, permissions, artifacts, cache, matrix, failure behavior and rollback. External CI mutation requires explicit approval.
15. Manual QA must name charter, environment, evidence and reviewer. "Manual review" alone is not enough.
16. Do not claim "works", "tested", "verified", "ready" or "quality improved" without current evidence from this run or an explicit inspection-only gap.
17. Record residual risk in `RUNLOG.md`, `EVALS.md` or release packet so the next role does not inherit hidden assumptions.

## Product-Agent OS candidate rules

### Discovery signals

- Directories: `tests/`, `test/`, `spec/`, `e2e/`, `playwright/`, `cypress/`, `coverage/`, `evals/`, `.github/workflows/`, `fixtures/`, `__tests__/`, `snapshots/`
- Files: `TEST.md`, `EVALS.md`, `RUNLOG.md`, `pytest.ini`, `tox.ini`, `vitest.config.*`, `jest.config.*`, `playwright.config.*`, `coverage.*`, `promptfoo.yaml`, `promptfooconfig.yaml`, `pact.*`, `openapi.*`, `asyncapi.*`
- Terms: failing test, red-green-refactor, acceptance scenario, test matrix, coverage, mutation, property-based, flaky, retry, trace, screenshot, contract test, eval rubric, threshold, grader, manual QA, current evidence
- Dependency signals: pytest, unittest, JUnit, Jest, Vitest, Playwright, Testing Library, Storybook, Pact, Stryker, Hypothesis, Promptfoo, Ragas, Codecov, GitHub Actions

### Readiness gates

| Gate | Trigger | Block condition |
| --- | --- | --- |
| `quality_strategy_present` | New project, major feature, shared subsystem | No test/eval portfolio, risk tier or evidence owner. |
| `acceptance_traceability_present` | User-visible behavior change | Acceptance criterion is not mapped to check, eval, manual charter or explicit gap. |
| `bug_reproduction_evidence_present` | Bugfix | No reproduction command, failing test, logs, screenshot or explicit reproduction gap. |
| `test_first_or_gap_present` | Deterministic bugfix or business rule | No failing test first and no reason why test-first was not feasible. |
| `contract_check_present` | API/event/schema/public package change | Contract source or compatibility check is missing. |
| `risk_based_scope_present` | Risky, broad or constrained slice | No impact/risk-based test scope and no accepted gaps. |
| `regression_impact_present` | Refactor, migration, dependency or shared-code change | Impacted behavior and regression checks are missing. |
| `runtime_evidence_present` | UI/native/desktop/backend runtime behavior claim | No current runtime command, logs, screenshot, trace or API evidence. |
| `visual_a11y_evidence_present` | UI layout, design system or accessibility-sensitive change | No visual, responsive, keyboard/focus or accessibility evidence where relevant. |
| `eval_spec_present` | AI, docs, UX, search, ranking or subjective quality change | No dataset/rubric/grader/threshold or explicit eval gap. |
| `eval_rerun_evidence_present` | Eval-governed change | No current baseline/current result, failed cases or rerun command. |
| `coverage_policy_present` | Coverage threshold or coverage claim | No coverage type, threshold, exclusions and critical-path mapping. |
| `flaky_test_policy_present` | Retries, intermittent failures or quarantined tests | No classification, owner, expiry and follow-up evidence. |
| `ci_quality_gate_present` | Shared branch/release/PR quality claim | No CI command/job, trigger, artifact or permission policy. |
| `manual_qa_evidence_present` | Manual QA is used as evidence | No charter, environment, reviewer, notes and result. |
| `current_evidence_before_completion` | Completion or readiness claim | No current command/eval/runtime/manual evidence and no explicit inspection-only gap. |
| `test_data_privacy_present` | Tests/evals use fixtures, user data, logs or traces | Secrets/private data classification, sanitization or owner is missing. |

## Candidate eval fields

- Every acceptance criterion maps to a check, eval, manual charter or accepted gap.
- Bugfix includes reproduction evidence or explicit reproduction gap.
- Deterministic behavior change uses Red-Green-Refactor where feasible.
- Contract changes include source contract and compatibility verification.
- Regression scope follows impact analysis.
- Runtime claims include current runtime evidence.
- UI claims include visual/a11y evidence where relevant.
- AI or subjective quality claims include eval spec and rerun evidence.
- Coverage threshold is paired with critical-path coverage.
- Flaky tests are classified and not hidden by retries.
- CI gates list commands, triggers, artifacts and permissions.
- Manual QA evidence includes charter, environment, reviewer and findings.
- Test fixtures, eval datasets, traces and screenshots are free of secrets/private data.
- Final claims include current command/eval/runtime/manual evidence or explicit gap.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| Python tests | pytest, unittest, coverage.py, tox/nox | pytest is a strong default when already present; preserve existing runner. |
| Java/Kotlin tests | JUnit, Gradle/Maven test tasks | Use project build tool as source of truth. |
| JS/TS tests | Vitest, Jest, Node test runner | Choose by existing stack; Vitest fits Vite-native projects. |
| Browser/runtime tests | Playwright, Cypress, WebdriverIO | Playwright gives traces, screenshots, retries and cross-browser evidence. |
| Component tests | Storybook, Testing Library, Vitest Browser Mode | Prefer user-observable behavior and documented component states. |
| API contracts | OpenAPI, AsyncAPI, Pact, schema validators | Contracts should be source-of-truth, generated docs are derived. |
| Property-based tests | Hypothesis, fast-check, jqwik | Use for invariants, parsers, serializers, permissions and state machines. |
| Mutation testing | Stryker, mutmut, PIT | Use selectively on critical logic to reveal weak assertions. |
| Coverage reporting | coverage.py, Istanbul/V8, Codecov | Coverage is a signal, not proof of behavior. |
| AI evals | OpenAI Evals, Promptfoo, Ragas, custom app-backed evals | Choose by privacy, CI fit, rubric type and stack. |
| CI | GitHub Actions, GitLab CI, Buildkite, Azure Pipelines | Keep permissions scoped and evidence artifacts accessible. |
| Reports | JUnit XML, HTML reports, Allure, Playwright report | Store enough evidence to debug failures without rerunning immediately. |

## Типовые сбои

- A plan lists tests after implementation but never proves failure or behavior.
- Unit tests mock away the real risk while integration/contract behavior is untested.
- E2E tests dominate the suite and become slow, flaky and ignored.
- Coverage threshold becomes the goal and weak assertions still pass.
- Contract compatibility is inferred from generated clients without provider/consumer checks.
- Regression scope is selected by habit, not impact analysis.
- Browser visual tests run in unstable environments and produce noisy diffs.
- Retries hide intermittent failures without owner, classification or expiry.
- CI is treated as green based on an old run.
- Manual QA has no charter, criteria, environment or reviewer.
- AI evals have no baseline, threshold, rerun command or failed-case analysis.
- Test fixtures, traces or eval datasets contain secrets or private customer data.
- Final response claims "works" from inspection only while runtime verification was available.

## Open questions for deeper research

- Should Product-Agent OS generate a framework-neutral `test-eval-matrix.md` first, then stack-specific runner files later?
- Which changes should require Red-Green-Refactor as a blocker rather than a recommendation?
- Should mutation/property-based testing be a conditional gate only for critical deterministic logic?
- How should flaky test quarantine be represented in generated `TEST.md` and `RUNLOG.md`?
- What minimum AI eval threshold policy should apply before model/prompt/retrieval migrations?
- Should CI workflow proposals include least-privilege permissions by default, even when the target repo already has broader permissions?
- How should manual QA evidence be normalized across web, desktop, native, backend and docs workflows?

## Sources

- [Agile Alliance: Test-Driven Development](https://agilealliance.org/glossary/tdd/)
- [Agile Alliance: Acceptance Test-Driven Development](https://agilealliance.org/glossary/atdd/)
- [Agile Alliance: Behavior-Driven Development](https://agilealliance.org/glossary/bdd/)
- [Martin Fowler: The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Kent C. Dodds: The Testing Trophy and Testing Classifications](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classification)
- [ISTQB Certified Tester Foundation Level Syllabus v4.0.1](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf)
- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [pytest parametrizing tests](https://docs.pytest.org/en/stable/example/parametrize.html)
- [Vitest features](https://vitest.dev/guide/features.html)
- [Vitest coverage](https://vitest.dev/guide/coverage.html)
- [Jest snapshot testing](https://jestjs.io/docs/snapshot-testing)
- [Playwright retries](https://playwright.dev/docs/test-retries)
- [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer-intro)
- [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots)
- [Pact documentation](https://docs.pact.io/)
- [Stryker mutation testing](https://stryker-mutator.io/docs/)
- [Stryker mutation states and metrics](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/)
- [Hypothesis documentation](https://hypothesis.readthedocs.io/en/latest/)
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [GitHub Actions GITHUB_TOKEN permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
- [Codecov: About Code Coverage](https://docs.codecov.com/docs/about-code-coverage)
- [OpenAI: Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Codex: Add evals to your AI application](https://developers.openai.com/codex/use-cases/ai-app-evals)
- [Promptfoo intro](https://www.promptfoo.dev/docs/intro/)
- [Promptfoo assertions and metrics](https://www.promptfoo.dev/docs/configuration/expected-outputs/)
- [Ragas available metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)
- [Context7 research](../context7-research.md)
