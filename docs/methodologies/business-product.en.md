# Business & Product

Source status: `official + verified methodology + local implementation evidence + tool-assisted`

Research date: `2026-05-24`

Product-Agent OS behavior: require product intent, measurable user/business value, analytics or eval evidence, metric hardening and post-release learning before agents implement meaningful behavior changes or promote workflows into skills, plugins or automations.

## Scope

This dossier covers product hypothesis, value proposition, opportunity discovery, Lean MVP experiments, outcome-driven planning, HEART, North Star metrics, metric hardening, analytics taxonomy, qualitative feedback, AI product evals, release measurement and learning loops.

It does not mandate heavyweight product management for every code change, one universal North Star metric for all work, mandatory analytics instrumentation for internal-only mechanical changes or AI evals for non-AI behavior. The method is conditional: it becomes required when a change claims product value, user behavior change, business outcome, AI behavior quality, release impact or reusable workflow promotion.

## Supported facts

- Google HEART describes a user-centered metrics framework and a Goals -> Signals -> Metrics process for mapping product goals to measurable signals.
- Amplitude North Star guidance frames a primary value metric and supporting inputs around customer value and product/business outcomes.
- Amplitude taxonomy guidance says product analytics starts with planned events, properties, naming conventions and key metrics; inconsistent event names or missing properties create data quality problems.
- Amplitude implementation guidance assigns Data Governor ownership for tracking plan design, naming convention, taxonomy, data quality, privacy policy alignment and feature-success measurement challenge.
- Product Talk Opportunity Solution Trees connect desired outcome, opportunity space, solution space and assumption tests. They also require a target customer/value proposition theory, a defined outcome and story-based customer interviews as useful inputs.
- Product Talk distinguishes business outcomes, product outcomes and traction metrics; product outcomes are usually the right discovery scope because teams can influence them more directly.
- The Lean Startup methodology frames product development as experiments that ask whether a product should be built, uses MVP to learn quickly, and uses Build-Measure-Learn, actionable metrics and pivot/persevere decisions.
- Strategyzer Value Proposition Canvas identifies customer jobs, pains and gains, then maps product/service offering, pain relievers and gain creators against customer evidence.
- OpenAI Codex AI-native engineering guidance says agents can handle mechanical build work, while engineers retain responsibility for product behavior clarity, architecture implications, domain alignment, guardrails and long-term quality.
- OpenAI Codex verified operations guidance recommends structured inputs, approved scope, dry runs where possible, audit-ready outputs and reusable workflows only after a successful manual run.
- OpenAI Codex AI app eval guidance recommends turning concrete user-visible AI behavior into repeatable eval suites before prompt, model, retrieval or agent changes merge.
- OpenAI Evals/Promptfoo-style eval workflows are relevant for AI product behavior, but they do not replace product analytics, user research or post-release measurement.
- The local Product-Agent OS implementation already has `metric-spec.md`, `REQUIREMENTS.md`, `acceptance-scenarios.md`, `RUNLOG.md`, `metric_hardening_when_product_behavior_changes` and release/operator checks for metric hardening.

## Assumptions

- A behavior-changing slice should start from target user, opportunity/problem, expected outcome, non-goals, acceptance scenario and metric status before architecture or implementation tasks.
- For internal refactors, dependency updates or mechanical docs changes, product metrics can be marked `not_applicable` when the reason is explicit.
- A proxy metric is useful only when paired with counter-metric, guardrail, qualitative review and post-release review.
- Product analytics events are project contracts. They require taxonomy, owner, property definitions, privacy classification and validation evidence.
- AI product changes need both eval evidence for behavior and product evidence for value when they affect a user-facing promise.
- Workflow promotion should follow the chain manual thread -> playbook -> skill -> plugin -> automation only when value, verification, owner and safety boundary are explicit.

## Unsupported claims not adopted

- "A single metric proves product success." Metrics need context, guardrails, qualitative review and a decision horizon.
- "More usage always means more value." Increased engagement can hide degraded trust, quality, latency, cost or support load.
- "A feature request is an opportunity." Feature requests are possible solutions; opportunities describe unmet needs, pains or desires.
- "North Star is mandatory for every slice." Small changes often need a local product outcome or explicit `not_applicable` metric status.
- "Analytics data is reliable by default." Event/property drift, naming inconsistency and missing governance can invalidate decisions.
- "Evals replace product metrics." Evals test AI behavior; product value needs user/business outcome evidence.
- "Codex speed equals product value." Faster implementation is useful only when it advances the right outcome with current evidence.
- "Automation follows any repeated workflow." Repetition alone is not enough; automation needs approved scope, rollback/disable path and audit evidence.

## Methodologies

| Methodology | When to apply | Product-Agent OS behavior |
| --- | --- | --- |
| Product hypothesis | Any user/business behavior change | Require target user, opportunity/problem, expected outcome, non-goals, assumptions and evidence gaps in `REQUIREMENTS.md`. |
| Value Proposition Canvas | New product, segment, capability or unclear value | Record jobs, pains, gains, pain relievers, gain creators and evidence source. |
| Opportunity Solution Tree | Discovery, roadmap choice, multiple candidate solutions | Trace desired outcome -> opportunities -> solutions -> assumptions -> tests -> decision. |
| Lean Build-Measure-Learn | MVP, risky assumption, uncertain demand/value | Define smallest build, measure plan, actionable metric, learning threshold and pivot/persevere rule. |
| HEART | UX/user-centered product quality | Choose relevant Happiness, Engagement, Adoption, Retention or Task success metrics through Goals -> Signals -> Metrics. |
| North Star / primary value metric | Product-level value alignment | Define primary value metric, input metrics, baseline, target, owner, window and guardrails. |
| Metric hardening | Product behavior change with measurement claim | Require counter-metric, guardrails, proxy risk, qualitative review, privacy classification and post-release review. |
| Analytics taxonomy/governance | Usage data informs product decisions | Define events, properties, naming convention, owner, validation workflow, privacy constraints and dashboard/report. |
| Qualitative feedback loop | Metrics are ambiguous or early | Add interviews, support/sales/customer-success signals, review notes or accepted evidence gap. |
| Outcome-driven planning | Roadmap/large project decomposition | Plan slices around measurable behavior/outcome, not only components or tasks. |
| AI product evals | Prompt/model/retrieval/tool/agent behavior changes | Baseline first, one focused behavior, app-path eval where feasible, threshold, failure review and rerun before release claims. |
| Release measurement | Launch, rollout, beta, production change | Define measurement window, dashboard/report, owner, rollback/decision rule and RUNLOG update. |

## Documentation artifacts and standards

| Artifact | Purpose | Candidate location |
| --- | --- | --- |
| Product brief | One-page intent, audience, value and decision horizon. | `REQUIREMENTS.md` or `product-brief.md` |
| Value proposition | Customer jobs, pains, gains, pain relievers and gain creators. | `value-proposition.md` |
| Opportunity tree | Discovery map from outcome to assumptions and tests. | `opportunity-tree.md` |
| Experiment plan | Lean MVP or riskiest-assumption test definition. | `experiment-plan.md` |
| Metric spec | Primary metric, input metrics, counter-metrics, guardrails and proxy risk. | `metric-spec.md` |
| Tracking plan | Events, properties, taxonomy, owner and validation workflow. | `tracking-plan.md` |
| Acceptance scenarios | Requirement -> behavior -> evidence trace. | `acceptance-scenarios.md` |
| Eval plan | AI behavior dataset, assertions/graders, baseline, threshold and command. | `EVALS.md` |
| Decision log | Product tradeoffs, alternatives, owner and consequences. | `RUNLOG.md` or ADR |
| Release measurement plan | Rollout scope, review window, dashboard/report and rollback signal. | release checklist / `RUNLOG.md` |
| Privacy/consent note | Data minimization, classification, retention, deletion and policy source. | `metric-spec.md` or privacy note |

## Product-Agent OS candidate rules

- `requirements-author` should output a `product_hypothesis` block for behavior-changing work.
- `requirements-author` should mark `metric_scope` as `required`, `not_applicable` or `accepted_gap`; empty metric status should fail readiness.
- `implementation-planner` should stop when a behavior-changing slice lacks user, opportunity/problem, expected outcome, non-goals, acceptance scenario or metric/gap.
- `test-eval-designer` should map product behavior to deterministic tests, analytics validation, manual/exploratory evidence or AI evals.
- `pr-release-operator` should block product success claims when only planned measurement exists.
- `learning-loop-maintainer` should compare actual post-release signals with hypothesis and decide whether to continue, pivot, rollback or promote the workflow.
- Promotion to skill/plugin/automation should require repeatable value, stable inputs/outputs, verification command/artifact, owner, safety boundary and failure mode.

## Candidate readiness gates

| Gate | Required when | Evidence |
| --- | --- | --- |
| `product_hypothesis_present` | Behavior-changing work | Target user, problem/opportunity, expected outcome, non-goals. |
| `target_user_segment_present` | User scope matters | Primary, secondary and excluded users or accepted gap. |
| `value_proposition_evidence_present` | New segment/product/capability | Jobs, pains, gains and evidence source/gap. |
| `opportunity_not_solution_present` | Discovery/roadmap work | Opportunity statement has more than one possible solution. |
| `success_metric_present` | Product value claim | Primary metric or explicit `not_applicable` reason. |
| `metric_hardening_when_product_behavior_changes` | Behavior change with metric claim | Input metric, counter-metric, guardrail, proxy risk, qualitative review, owner. |
| `analytics_tracking_plan_present` | Usage data will be claimed | Event/property taxonomy, naming convention, validation plan and privacy classification. |
| `qualitative_feedback_loop_present` | Early/ambiguous product signal | Interviews, support/sales signal, review notes or accepted gap. |
| `ai_product_eval_when_ai_behavior_changes` | AI behavior changes | Baseline eval, cases, assertions/graders, threshold and command or accepted gap. |
| `post_release_measurement_plan_present` | Release/rollout | Window, dashboard/report, owner, decision rule and rollback/disable signal. |
| `release_measurement_evidence_present` | Success claim after release | Actual metrics/eval/user feedback or explicit evidence gap in `RUNLOG.md`. |

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

## Failure modes

- **Solution bias:** plan starts from implementation tasks and backfills product intent later.
- **Vanity metric:** metric is easy to move but weakly connected to customer or business value.
- **Proxy optimization:** team improves the metric while degrading quality, trust, cost, privacy or support load.
- **Data drift:** events/properties change without taxonomy review and analytics dashboards become misleading.
- **Evidence gap hidden:** release claim says "works" while measurement is planned but not yet observed.
- **Eval/product mismatch:** AI eval improves while user outcome, support load or retention degrades.
- **Over-process:** formal product artifacts are forced onto trivial mechanical changes instead of marking `not_applicable`.
- **Unsafe automation:** repeated workflow is automated before ownership, verification, approvals and rollback are stable.

## Open questions for implementation

- Should `product_hypothesis_present` become a universal gate for every behavior-changing slice, or only for user-facing/product-labeled changes?
- Should Product-Agent OS generate separate `value-proposition.md` and `opportunity-tree.md`, or keep them as optional sections inside `REQUIREMENTS.md` until the project grows?
- What threshold should route a slice from simple `metric-spec.md` to a full analytics `tracking-plan.md`?
- How should post-release measurement be represented when the project has no production telemetry yet?
- Should workflow promotion into skill/plugin require a business/product metric, or is repeated engineering time saved enough when evidence is explicit?

## Sources

- [Google HEART framework paper](https://research.google.com/pubs/pub36299.html?frame=0)
- [Amplitude North Star Hub](https://amplitude.com/north-star-hub)
- [Amplitude taxonomy planning](https://amplitude.com/docs/data/data-planning-playbook)
- [Amplitude implementation team organization](https://amplitude.com/docs/get-started/implementation-team-organization)
- [Product Talk Opportunity Solution Trees](https://www.producttalk.org/opportunity-solution-trees/)
- [The Lean Startup methodology](https://theleanstartup.com/principles)
- [Strategyzer Value Proposition Canvas](https://www.strategyzer.com/library/the-value-proposition-canvas)
- [OpenAI Codex: Building an AI-Native Engineering Team](https://developers.openai.com/codex/guides/build-ai-native-engineering-team)
- [OpenAI Codex: Run verified operations](https://developers.openai.com/codex/use-cases/verified-operations-workflows)
- [OpenAI Codex: Add evals to your AI application](https://developers.openai.com/codex/use-cases/ai-app-evals)
- [Product-Agent OS development standards](../product-agent-os/development-standards.md)
