# Business & Product

Source status: `official + verified methodology + local implementation evidence + tool-assisted`

Источники: [Google HEART framework paper](https://research.google.com/pubs/pub36299.html?frame=0), [Amplitude North Star Hub](https://amplitude.com/north-star-hub), [Amplitude taxonomy planning](https://amplitude.com/docs/data/data-planning-playbook), [Amplitude implementation team organization](https://amplitude.com/docs/get-started/implementation-team-organization), [Product Talk Opportunity Solution Trees](https://www.producttalk.org/opportunity-solution-trees/), [The Lean Startup methodology](https://theleanstartup.com/principles), [Strategyzer Value Proposition Canvas](https://www.strategyzer.com/library/the-value-proposition-canvas), [Building an AI-Native Engineering Team](https://developers.openai.com/codex/guides/build-ai-native-engineering-team), [Codex verified operations](https://developers.openai.com/codex/use-cases/verified-operations-workflows), [Codex AI app evals](https://developers.openai.com/codex/use-cases/ai-app-evals), [Product-Agent OS development standards](../product-agent-os/development-standards.md).

## Deep research цель

Business & Product слой отвечает на вопрос: зачем большой проект существует, для кого он строится, какая гипотеза проверяется, какой outcome должен измениться и какие evidence докажут, что change полезен, а не просто технически завершен.

В Product-Agent OS этот слой должен появляться до architecture, requirements slicing и implementation plan. Если пользователь, value proposition, opportunity, non-goal, success metric и guardrails не названы, Codex App, CLI, IDE extension или subagents могут построить правильный код для неправильной задачи.

## Поддержанные факты

- Google HEART описывает user-centered метрики и процесс Goals -> Signals -> Metrics для связи продуктовой цели с измеримыми сигналами.
- Amplitude North Star подход фокусирует команду на primary value metric и input metrics, которые объясняют, как команда влияет на эту value metric.
- Amplitude taxonomy guidance требует заранее определить events, properties, naming convention и data quality правила, иначе продуктовые решения строятся на неустойчивых данных.
- Opportunity Solution Tree связывает desired outcome, opportunity space, solution space и assumption tests; opportunity не должна подменяться feature-идеей.
- Lean Startup формулирует product development как эксперимент: "Should this product be built?", MVP, Build-Measure-Learn, actionable metrics, pivot/persevere.
- Strategyzer Value Proposition Canvas требует описывать customer jobs, pains, gains и то, как offering снимает pains и создает gains.
- OpenAI Codex guidance для AI-native engineering переводит инженеров от механического build-work к clarifying product behavior, architecture review, domain alignment and long-term quality.
- Codex AI app eval guidance рекомендует превращать конкретное user-visible promise в repeatable eval suite до prompt/model/retrieval/agent changes.
- Локальный Product-Agent OS уже содержит `metric-spec.md`, `REQUIREMENTS.md`, readiness gate `metric_hardening_when_product_behavior_changes` и release gate на post-release measurement.

## Assumptions

- Behavior-changing slice starts from target user, opportunity/problem, expected outcome, non-goals, acceptance scenario and metric status.
- Internal refactors, dependency bumps and mechanical docs changes can mark product metrics as `not_applicable` when the reason is explicit.
- Proxy metric is acceptable only with counter-metric, guardrail, qualitative review and post-release review.
- Product analytics events are project contracts and need taxonomy, owner, privacy classification and validation evidence.
- AI product behavior needs both eval evidence for behavior and product evidence for value when it affects a user-facing promise.
- Workflow promotion follows manual thread -> playbook -> skill -> plugin -> automation only when value, verification, owner and safety boundary are explicit.

## Инструкции применения на проекте

1. Начинайте meaningful behavior change с product hypothesis: target user, problem/opportunity, expected behavior change, outcome, non-goals.
2. Зафиксируйте value proposition: customer jobs, pains, gains, pain relievers, gain creators и evidence, откуда это известно.
3. Разделите business outcome, product outcome и feature traction metric. Для discovery предпочтительнее product outcome, который команда может реально изменить.
4. Для сложной или неопределенной области ведите Opportunity Solution Tree: desired outcome -> opportunities -> candidate solutions -> riskiest assumptions -> tests.
5. Для MVP формулируйте Lean experiment: hypothesis, smallest build, measure plan, learning threshold, pivot/persevere decision.
6. Назовите decision horizon: discovery, MVP, beta, production, scale. Не требуйте одинакового уровня формальности для всех горизонтов.
7. Разделите primary value metric, input metrics, counter-metrics и guardrails. Primary metric показывает value, input metrics объясняют рычаги, counter-metrics ловят деградацию.
8. Обязательно опишите proxy metric risk: как команда может улучшить метрику и одновременно ухудшить пользовательскую или бизнес-ценность.
9. Добавьте qualitative feedback loop: interviews, support tickets, sales/customer-success signals, review notes или explicit evidence gap.
10. Для analytics заранее создайте tracking plan: event name, owner, business question, properties, property types, privacy classification, retention, dashboard/report.
11. Для AI-facing behavior добавьте eval plan: user-visible promise, seed cases, assertions/graders, baseline command, threshold, failure review owner.
12. Для privacy-sensitive метрик укажите data minimization, consent/policy source, retention/deletion rule и privacy/legal owner.
13. После release сравните actual signals с гипотезой и внесите lessons, failures и accepted gaps в `RUNLOG.md`.
14. Не заявляйте product success по одному proxy metric без guardrail, qualitative review и post-release evidence.

## Применяемые методологии разработки

| Методология | Когда применять | Как выглядит в проекте |
| --- | --- | --- |
| Product hypothesis | Любая feature, которая должна изменить пользовательское или бизнес-поведение | `REQUIREMENTS.md` содержит user, problem/opportunity, expected outcome, non-goals, assumptions and evidence gaps. |
| Value Proposition Canvas | Новая аудитория, новый продукт, новая capability или сомнение в value | `value-proposition.md` описывает jobs, pains, gains, pain relievers, gain creators and evidence source. |
| Opportunity Solution Tree | Discovery, roadmap choice, ambiguous user need, competing feature ideas | `opportunity-tree.md` связывает outcome, opportunity, solution, assumption test and decision. |
| Lean Build-Measure-Learn | MVP, experiment, risky assumption, uncertain market/user value | `experiment-plan.md` фиксирует smallest build, metric, learning threshold, pivot/persevere rule. |
| HEART metrics | UX/product quality нужно измерять через user-centered goals | Выбираются релевантные Happiness, Engagement, Adoption, Retention или Task success; не все категории обязательны. |
| North Star / primary value metric | Продукту нужна единая value metric и driver tree | `metric-spec.md` содержит primary value metric, input metrics, owner, baseline, target and time window. |
| Metric hardening | Любое product behavior изменение с measurement claim | Counter-metric, guardrails, proxy risk, qualitative review, privacy classification and post-release review are required. |
| Product analytics governance | Usage data становится источником решений | Tracking plan, taxonomy, naming convention, data owner, instrumentation owner and validation evidence. |
| Data-informed decision making | После появления usage data, feedback loop или release evidence | Decisions cite metric, user research, support signal, eval result or accepted evidence gap. |
| Outcome-driven planning | Roadmap нужно разбить на measurable outcomes | `PLAN.md` slice связан с expected behavior, measurement, acceptance scenario and release review. |
| AI product evals | Prompt/model/retrieval/tool/agent behavior влияет на пользователя | Baseline eval exists before behavior change; suite tests app path users hit where feasible. |

## Инструменты, артефакты и стандарты документирования

| Артефакт | Назначение | Минимальное содержимое |
| --- | --- | --- |
| `REQUIREMENTS.md` | Product intent and behavior scope | Target user, problem/opportunity, hypothesis, non-goals, constraints, acceptance criteria, metric status. |
| `metric-spec.md` | Metric hardening | Primary metric, input metrics, counter-metric, guardrails, proxy risk, privacy classification, owner, post-release review. |
| `value-proposition.md` | Customer value fit | Jobs, pains, gains, pain relievers, gain creators, segment, evidence source, open assumptions. |
| `opportunity-tree.md` | Discovery traceability | Desired outcome, opportunities, candidate solutions, assumptions, tests, decisions. |
| `experiment-plan.md` | Lean MVP / assumption test | Hypothesis, smallest build, measure plan, learning threshold, pivot/persevere rule, owner. |
| `tracking-plan.md` | Product analytics governance | Events, properties, naming convention, owner, dashboard, validation command/report, privacy review. |
| `acceptance-scenarios.md` | Requirement -> scenario -> evidence | Actor, context, trigger, observable outcome, deterministic/manual/eval check, evidence owner. |
| `EVALS.md` | AI behavior and subjective quality | Dataset, rubric, grader/assertion, baseline, threshold, failure review, regression command. |
| `RUNLOG.md` | Current cycle evidence | Decisions, experiments, failures, post-release measurement, accepted gaps and next review date. |
| Release notes | User-facing change and measurement plan | What changed, who is affected, rollout scope, measurement window, rollback/disable signal. |

## Product-Agent OS routing

- `requirements-author` owns the first `product_hypothesis` packet and must mark `metric_scope` as `required`, `not_applicable` or `accepted_gap`.
- `implementation-planner` must stop when a behavior-changing slice lacks product hypothesis, acceptance scenario, metric/gap or owner.
- `test-eval-designer` maps product behavior to deterministic checks, exploratory checks, product analytics validation or AI evals.
- `solution-architect` uses product outcome, constraints and guardrails to choose architecture tradeoffs; architecture should not invent product goals.
- `pr-release-operator` checks release measurement, metric hardening and post-release review before product success claims.
- `learning-loop-maintainer` captures actual measurement results and decides whether the workflow should become playbook, skill, plugin or automation.

## Candidate readiness gates

- `product_hypothesis_present`: target user, opportunity/problem, expected outcome and non-goals exist.
- `target_user_segment_present`: primary, secondary and explicitly excluded users are named when scope matters.
- `value_proposition_evidence_present`: jobs/pains/gains and source or accepted gap are recorded.
- `opportunity_not_solution_present`: at least one problem/opportunity statement is not just a feature request.
- `success_metric_present`: primary metric or explicit `not_applicable` reason is present.
- `metric_hardening_when_product_behavior_changes`: input metric, counter-metric, guardrail, proxy risk and owner exist.
- `analytics_tracking_plan_present`: events/properties/taxonomy/owner/privacy are defined when product usage data is claimed.
- `qualitative_feedback_loop_present`: user research, support/sales signal or accepted qualitative gap is recorded.
- `ai_product_eval_when_ai_behavior_changes`: AI behavior changes have baseline eval or accepted baseline gap.
- `post_release_measurement_plan_present`: review window, dashboard/report, owner and rollback/decision rule exist.
- `release_measurement_evidence_present`: actual metrics, eval result, user feedback or explicit evidence gap exists before success claim.

## Candidate eval fields

- `product_hypothesis_contract_present`
- `target_user_segment_contract_present`
- `value_proposition_trace_present`
- `opportunity_solution_assumption_trace_present`
- `metric_hardening_contract_present`
- `analytics_tracking_plan_contract_present`
- `privacy_classification_for_metrics_present`
- `ai_behavior_eval_contract_present`
- `post_release_measurement_contract_present`
- `workflow_promotion_value_evidence_present`

## Проверки

- `REQUIREMENTS.md` names target user, problem/opportunity, outcome, non-goal, assumptions and metric status.
- Every behavior change has an acceptance scenario or explicit accepted gap.
- `metric-spec.md` includes primary metric, input metric, counter-metric, guardrail, proxy risk and privacy classification.
- Tracking events have stable names, property definitions, owner and validation plan.
- AI behavior claims cite eval baseline/current results, not only prompt inspection.
- Completion claims cite current evidence; planned measurement alone is not product success.

## Failure modes

- Feature idea masquerades as opportunity, so discovery starts from solution bias.
- One metric becomes the goal and damages product quality, trust, support load or privacy.
- Product hypothesis is written after implementation to justify existing work.
- North Star metric is used for a small isolated slice where a local product outcome would be clearer.
- Analytics events are added without taxonomy, property definitions, privacy classification or owner.
- AI eval score is treated as product value without user outcome, qualitative review or post-release evidence.
- Codex velocity is treated as business value without measuring what changed for the user or team.
- Community claims or memory are promoted into core guidance without source status.

## Unsupported claims not adopted

- "A single metric proves product success." It is only useful with context, counter-metrics, guardrails and qualitative review.
- "More usage always means more value." Usage can grow while satisfaction, accuracy, cost, trust or retention degrade.
- "Product discovery can be skipped because Codex can build quickly." Faster implementation increases the cost of unclear intent.
- "Evals replace product metrics." Evals test AI behavior; product value still needs user/business outcome evidence.
- "Automation should follow every repeated workflow." Automation follows only after value, verification, ownership and safety boundaries are stable.

## Open questions for future implementation

- Should `product_hypothesis_present` become universal for every behavior-changing slice, or only user-facing/product-labeled changes?
- Should Product-Agent OS generate separate `value-proposition.md`, `opportunity-tree.md` and `product-brief.md`, or keep them optional inside `REQUIREMENTS.md` until project growth demands separation?
- What threshold should route a slice from simple `metric-spec.md` to full analytics `tracking-plan.md`?
- How should post-release measurement be represented when the project has no production telemetry yet?
- Should workflow promotion into skill/plugin require product metric evidence, or is explicit engineering time saved enough for internal workflows?
