# Quality, Testing & Evals

Source status: `official + expert reference + vendor documentation + tool-assisted + experiment`

Источники: [Agile Alliance TDD](https://agilealliance.org/glossary/tdd/), [Agile Alliance ATDD](https://agilealliance.org/glossary/atdd/), [Agile Alliance BDD](https://agilealliance.org/glossary/bdd/), [Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html), [Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classification), [ISTQB CTFL v4.0.1](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf), [pytest](https://docs.pytest.org/en/stable/), [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html), [pytest parametrization](https://docs.pytest.org/en/stable/example/parametrize.html), [Vitest](https://vitest.dev/guide/features.html), [Vitest coverage](https://vitest.dev/guide/coverage.html), [Playwright retries](https://playwright.dev/docs/test-retries), [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer-intro), [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots), [Jest snapshot testing](https://jestjs.io/docs/snapshot-testing), [Pact](https://docs.pact.io/), [Stryker mutation testing](https://stryker-mutator.io/docs/), [Stryker mutation score](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/), [Hypothesis](https://hypothesis.readthedocs.io/en/latest/), [Codecov coverage guidance](https://docs.codecov.com/docs/about-code-coverage), [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [GitHub Actions GITHUB_TOKEN](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token), [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices), [Codex AI app evals use case](https://developers.openai.com/codex/use-cases/ai-app-evals), [Promptfoo](https://www.promptfoo.dev/docs/intro/), [Promptfoo expected outputs](https://www.promptfoo.dev/docs/configuration/expected-outputs/), [Ragas metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/), [Context7 research](../sources/context7-research.md), [research dossier](../sources/methodology-research/quality-testing-evals.md).

## Deep research цель

Quality, Testing & Evals слой определяет, как проект доказывает correctness, behavior, contracts, runtime quality, subjective quality and AI quality before completion claims.

Главный принцип: quality claim требует current evidence. Тесты, evals, screenshots, traces, manual QA and CI logs являются evidence только тогда, когда понятны command, environment, expected result, actual result, owner, residual risk and freshness.

## Поддержанные факты

- TDD, ATDD and BDD describe complementary loops for deterministic tests, acceptance tests and shared behavior language before implementation.
- Test Pyramid and Testing Trophy are portfolio heuristics, not universal mandates; useful verification mixes static, unit, integration, contract, E2E, manual and eval checks by risk.
- ISTQB separates confirmation testing, regression testing and impact analysis, which supports bugfix and refactor verification.
- pytest, Vitest, Playwright, Pact, Hypothesis and Stryker provide concrete mechanisms for unit, integration, browser, contract, property-based and mutation testing.
- Coverage indicates executed code, but does not prove requirements, assertions, contracts or user outcomes.
- GitHub Actions workflow permissions and `GITHUB_TOKEN` scope are part of CI quality gate evidence.
- OpenAI eval guidance, Codex AI app evals, Promptfoo and Ragas support AI, RAG and subjective quality evaluation with datasets, assertions, metrics and thresholds.

## Assumptions

- Product-Agent OS should select the smallest useful verification path by risk and feedback speed.
- Completion evidence belongs in `RUNLOG.md` or evidence packet; durable quality strategy belongs in `TEST.md` and `EVALS.md`.
- CI is a verification surface, not automatically an approval surface; external CI writes stay approval-bound.
- Coverage thresholds are useful only when paired with requirement, critical-path and regression coverage.
- Manual QA can be evidence when it has charter, environment, criteria, reviewer, notes and result.

## Инструкции применения на проекте

1. Для каждого slice назвать user-visible behavior или technical contract, который надо доказать.
2. Выбрать smallest useful verification path: static/unit/integration/contract/E2E/runtime/manual/eval.
3. Связать каждое acceptance criterion с deterministic check, contract check, runtime check, eval, manual charter или explicit gap.
4. Для bugfix сначала получить reproduction evidence, если это практически возможно: failing test, command, log, screenshot, trace или точные шаги.
5. TDD использовать для deterministic logic, parsers, validators, business rules and bugfixes: Red-Green-Refactor evidence важнее самого факта наличия теста.
6. ATDD/BDD использовать для behavior scenarios, где product/business language должна перейти в executable checks или eval criteria.
7. Test portfolio строить по risk and feedback speed: больше быстрых targeted checks, меньше дорогих high-level checks, но без потери critical path coverage.
8. Для refactor, migration, dependency update or shared-code change фиксировать regression impact map.
9. Для API/event/package changes требовать contract source и consumer/provider compatibility evidence.
10. Для UI changes фиксировать runtime, responsive, visual, keyboard/focus and accessibility evidence, если изменение затрагивает пользователя.
11. Для backend/runtime behavior проверять unit/integration/API/log/observability path, а не только code inspection.
12. Для native/mobile/desktop behavior использовать platform build/run/log/screenshot evidence.
13. Для AI, docs, UX, search, ranking or subjective outputs использовать eval spec: dataset, rubric, grader, threshold, rerun command.
14. Coverage использовать как gap-finding signal, а не как proof of correctness. Coverage threshold должен быть связан с critical paths.
15. Mutation/property-based testing применять выборочно для critical deterministic logic, где ordinary examples могут пропустить weak assertions или edge cases.
16. Flaky tests не скрывать retries. Ретрай может собрать evidence, но нужен owner, root-cause class, expiry and follow-up.
17. Manual QA принимать как evidence только с charter, environment, criteria, reviewer, notes and result.
18. CI workflow changes держать staged, пока нет explicit approval на внешние writes. CI claims требуют свежего run evidence.
19. Fixtures, eval datasets, traces, screenshots and logs не должны содержать secrets, credentials, raw private chats или private customer data.
20. Не писать "works", "tested", "verified", "ready" или "quality improved", если в текущем run нет relevant evidence или explicit inspection-only gap.

## Применяемые методологии разработки

| Методология | Когда применять | Как выглядит в проекте |
| --- | --- | --- |
| TDD / Red-Green-Refactor | Deterministic logic or bugfix | Failing test first, failing output, minimal fix, passing output, refactor with checks green. |
| ATDD / BDD | Product behavior, workflows, business rules | Acceptance scenarios map requirements to checks/evals and forbidden behavior. |
| Test portfolio design | Любой большой проект | Static, unit, integration, contract, E2E, manual and eval checks selected by risk. |
| Risk-based testing | Ограничены time/CI budget или high-risk change | Test scope follows impact, likelihood, user harm, data/security exposure and failure history. |
| Confirmation + regression testing | Bugfix, migration, refactor, dependency update | Original failure is checked, then impacted unchanged behavior is rerun. |
| Contract testing | API/event/schema/public package changes | OpenAPI/AsyncAPI/Pact/schema checks and consumer/provider compatibility evidence. |
| Integration testing | Behavior depends on database/service/filesystem/queue/network | Real or high-fidelity dependency with reset strategy and failure evidence. |
| E2E/runtime testing | User-visible workflow or platform behavior | Browser/simulator/API/runtime path, logs, screenshots, traces, reports. |
| Visual and accessibility testing | UI layout, design system, custom widgets | Stable screenshots, component states, keyboard/focus/a11y checks, accepted diffs. |
| Property-based testing | Invariants, parsers, serializers, permissions, state machines | Generated inputs, properties, seed/shrink evidence, preserved failing examples. |
| Mutation testing | Tests pass but assertion quality is doubtful | Mutants, mutation score, surviving mutants and follow-up tests. |
| Flaky test management | Intermittent CI/runtime failures | Classification, owner, quarantine expiry, rerun evidence and root-cause tracking. |
| CI quality gates | Shared branches, PRs, release readiness | Commands, jobs, permissions, artifacts, exit codes and rerun path. |
| Eval-driven quality | AI/docs/UX/search/subjective quality | Dataset, rubric, grader, threshold, baseline/current run and failure analysis. |
| Exploratory testing | Unknown risk, new workflow, usability | Time-boxed charter, environment, notes, findings and follow-up checks. |
| Evidence-before-completion | Every meaningful slice | Current command/eval/runtime/manual evidence or explicit gap before success claims. |

## Инструменты, артефакты и стандарты документирования

- `TEST.md`: quality strategy, test portfolio, risk tiers, required checks, accepted gaps.
- `EVALS.md`: subjective/AI/domain quality rubrics, datasets, thresholds, rerun cadence.
- `ai-eval-spec.md`: AI behavior objective, app path, dataset, assertions/graders, threshold and owner.
- `test-eval-matrix.md`: requirement -> scenario -> check/eval/manual evidence -> owner.
- `acceptance-scenarios.md`: user/business behavior, expected result, forbidden result.
- `red-green-refactor-log.md`: failing command, fix command, passing command, refactor evidence.
- `bug-reproduction.md`: original failure, reproduction steps, environment, fixture, fixed evidence.
- `risk-based-test-plan.md`: risk areas, impact, likelihood, selected checks, accepted gaps.
- `regression-impact-map.md`: changed files/contracts/data and impacted behavior to rerun.
- `contract-test-map.md`: API/event/schema contracts, consumers, providers, verification command.
- `runtime-evidence.md`: browser/API/native/desktop/server command, environment, logs, screenshots, traces.
- `visual-a11y-evidence.md`: viewports, component states, screenshots, keyboard/focus/a11y results.
- `coverage-policy.md`: coverage type, threshold, exclusions, critical-path mapping, non-goals.
- `mutation-test-report.md`: scope, mutation score, surviving mutants, ignored mutants, follow-up tests.
- `property-test-spec.md`: invariants, input generators, seed handling, shrink/failure examples.
- `flaky-test-ledger.md`: test, symptom, suspected class, owner, quarantine expiry, rerun evidence.
- `ci-quality-gates.md`: jobs, triggers, permissions, artifacts, cache, matrix, rollback.
- `eval-run-report.md`: baseline/current score, passing/failing cases, regressions, residual risk.
- `manual-qa-charter.md`: scope, environment, checklist, notes, findings, reviewer.
- `evidence-packet.md` or `RUNLOG.md`: commands, exit codes, outputs, artifacts, accepted gaps, residual risks.

## Что еще включить в deep research

- Quality maturity levels: `baseline`, `team`, `production`, `regulated`.
- Stack-specific templates: pytest, Vitest/Jest, Playwright, JUnit, Storybook, Pact, Promptfoo, Ragas.
- Test portfolio defaults by project type: backend/API, frontend, database, native, desktop, AI/RAG, docs-only.
- Risk taxonomy: user harm, money, data loss, security, compliance, operational outage, migration, public contract.
- Flaky test policy: retry rules, quarantine limits, owner, expiry, CI visibility.
- Coverage policy: statement/branch/function/critical path/requirement coverage and when thresholds are misleading.
- Mutation/property-based testing triggers for critical deterministic code.
- CI evidence model: local check, CI check, artifact, logs, screenshots, traces, rerun command.
- Manual QA evidence format for workflows that cannot be fully automated yet.
- Eval failure triage: data, prompt, model, retrieval, tool, grader, threshold, product expectation.
- Test data governance: synthetic/sanitized fixtures, log redaction, retention, owner.

## Product-Agent OS routing

- `workspace-discovery-auditor` detects test runners, CI, coverage, evals, contract files, Playwright, Storybook, Pact, Promptfoo, Ragas and flaky-test signals.
- `requirements-author` maps requirements to acceptance scenarios and evidence owners.
- `implementation-planner` blocks plan-ready status when acceptance traceability, contract checks, regression scope or eval gates are missing.
- `test-eval-designer` owns test/eval matrix, risk-based verification path, eval rubric and rerun commands.
- `risk-reviewer` checks unsupported readiness claims, missing evidence, flaky hidden failures, private test data and high-risk gaps.
- `docs-maintainer` keeps `TEST.md`, `EVALS.md`, `RUNLOG.md` and evidence packets aligned with source-backed claims.
- `release-operator` carries current evidence, accepted gaps and residual risk into release readiness.

## Candidate readiness gates

- `quality_strategy_present`: project/slice has test portfolio, risk tier and evidence owner.
- `acceptance_traceability_present`: acceptance criteria map to check, eval, manual charter or explicit gap.
- `bug_reproduction_evidence_present`: bugfix has reproduction command, failing test, logs, screenshot, trace or explicit reproduction gap.
- `test_first_or_gap_present`: deterministic bugfix/business rule has Red-Green-Refactor evidence or reasoned exception.
- `contract_check_present`: API/event/schema/public package change has contract source and compatibility check.
- `risk_based_scope_present`: risky, broad or constrained slice has impact/risk-based test scope.
- `regression_impact_present`: refactor/migration/dependency/shared-code change has impacted behavior and regression checks.
- `runtime_evidence_present`: runtime behavior claim has current command, logs, screenshots, traces or API evidence.
- `visual_a11y_evidence_present`: UI layout/design/accessibility change has relevant visual/responsive/keyboard/focus/a11y evidence.
- `eval_spec_present`: AI/docs/UX/search/subjective quality change has dataset, rubric, grader, threshold or explicit eval gap.
- `eval_rerun_evidence_present`: eval-governed change has baseline/current result, failed cases and rerun command.
- `coverage_policy_present`: coverage claim has coverage type, threshold, exclusions and critical-path mapping.
- `flaky_test_policy_present`: retries/quarantine/intermittent failures have classification, owner, expiry and follow-up.
- `ci_quality_gate_present`: shared branch/release/PR claim has CI command/job, trigger, artifact and permission policy.
- `manual_qa_evidence_present`: manual QA has charter, environment, reviewer, notes and result.
- `current_evidence_before_completion`: completion/readiness claim has current evidence or explicit inspection-only gap.
- `test_data_privacy_present`: tests/evals/fixtures/logs/traces/screenshots have no secrets/private data or have sanitization status.

## Candidate eval fields

- Every acceptance criterion maps to a check, eval, manual charter or accepted gap.
- Bugfix includes reproduction evidence or explicit reproduction gap.
- Red-Green-Refactor evidence exists for deterministic bugfix/business rule or exception is recorded.
- API/event/schema/public package change has contract source and compatibility evidence.
- Regression impact map exists for refactor, migration, dependency or shared-code changes.
- Runtime claim has current command, logs, screenshots, traces or API evidence.
- Visual/a11y claim has viewport, keyboard/focus and screenshot evidence where relevant.
- Eval-governed change has dataset, rubric, grader/assertion, threshold, baseline/current result and failed-case review.
- CI gate records command/job, trigger, permissions, artifacts and exit code.
- Final claim includes current command/eval/runtime/manual evidence or explicit gap.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| Python tests | pytest, fixtures, parametrization | Good default vocabulary for Python test structure and data variation. |
| JS/TS tests | Vitest, Jest snapshots | Unit/component checks, coverage and snapshot evidence where appropriate. |
| Browser/runtime | Playwright retries, Trace Viewer, snapshots | Evidence for UI/runtime behavior, traces and visual diffs. |
| Contract tests | Pact | Consumer/provider compatibility evidence. |
| Property tests | Hypothesis | Invariants, parsers, serializers, permissions and state transitions. |
| Mutation tests | Stryker | Assertion strength and surviving mutants for critical deterministic logic. |
| Coverage | Codecov or stack-native coverage | Gap-finding signal; not proof of correctness. |
| CI gates | GitHub Actions workflow syntax and `GITHUB_TOKEN` permissions | Jobs, triggers, permissions, artifacts and approval boundaries. |
| AI evals | OpenAI eval guidance, Promptfoo, Ragas | Dataset, assertions, RAG metrics, thresholds and rerun evidence. |
| Eval config signals | `promptfoo.yaml`, `promptfooconfig.yaml`, `pytest.ini`, `tox.ini` | Discovery signals for local verification suites. |

## Проверки

- Every acceptance criterion has a check/eval/manual charter or explicit gap.
- Bugfix evidence includes reproduction or explicit reproduction gap.
- Deterministic behavior change uses test-first where feasible.
- Contract changes have source contract and compatibility evidence.
- Regression scope follows impact analysis.
- Runtime claims include current runtime evidence.
- UI claims include visual/a11y evidence where relevant.
- AI/subjective quality claims include eval spec and rerun result.
- Coverage is tied to critical paths, not only global percentage.
- Flaky tests are classified and not silently hidden by retries.
- CI gates list command, job, trigger, permissions, artifacts and exit code.
- Manual QA names charter, environment, reviewer and result.
- Test/eval data contains no secrets or private customer data.
- Final response carries current evidence, accepted gaps and residual risks.

## Типовые сбои

- Tests are listed after implementation without proving behavior.
- Unit tests mock away the real risk while integration/contract behavior is untested.
- E2E suite becomes slow, flaky and ignored.
- Coverage threshold becomes a proxy for quality.
- Regression scope is selected by habit, not impact analysis.
- Contract compatibility is inferred from generated clients only.
- Visual tests run in unstable environments and produce noisy diffs.
- Retries hide intermittent failures without owner or expiry.
- CI status is assumed from an old run.
- Manual QA has no charter, criteria, environment or reviewer.
- AI evals have no baseline, threshold, rerun command or failed-case analysis.
- Test fixtures, traces or eval datasets leak secrets or private data.
- Final answer claims "works" from inspection only while runtime verification was available.

## Unsupported claims not adopted

- "More tests always means better quality." Useful signal is risk coverage, fast feedback and failure usefulness.
- "100 percent line coverage proves correctness." It does not prove assertions, behavior, contracts or outcomes.
- "E2E tests are most realistic, so they should dominate." They are valuable but slower and more brittle.
- "Manual QA is not evidence." It can be evidence with charter, criteria, environment and captured result.
- "AI evals are optional for AI behavior changes." Prompt/model/retrieval/tool changes need baseline or explicit baseline gap.

## Open questions for future implementation

- Which stack-specific templates should be generated first: pytest, Vitest/Jest, Playwright, JUnit, Storybook, Pact, Promptfoo or Ragas?
- What default test portfolio should apply by project type: backend/API, frontend, database, native, desktop, AI/RAG or docs-only?
- How should flaky tests be classified, quarantined and expired without hiding failures?
- Which mutation/property-based testing triggers should become readiness gates?
- How should CI evidence distinguish local command evidence, remote job evidence, artifacts, logs and rerun commands?
- Which eval failure labels should be standardized: data, prompt, model, retrieval, tool, grader, threshold or product expectation?
