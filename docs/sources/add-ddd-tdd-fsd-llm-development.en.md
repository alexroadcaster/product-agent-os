# ADD, DDD, TDD And FSD In LLM-Assisted Development

Source status: `mixed source-backed draft`  
Status: incoming research document. Before moving claims into core guidance, verify primary sources and explicitly separate Data-Driven Development from Domain-Driven Design.

## Table Of Contents

1. Short summary
2. Terms
3. ADD - Agentic-Driven Development
4. DDD - Data-Driven Development
5. TDD - Test-Driven Development
6. FSD - Feature-Sliced Design / Development
7. Key differences
8. Strengths and limitations
9. How the approaches fit together
10. Use with LLM agents
11. Web, mobile and desktop use
12. Practical workflow
13. Example: search across chat conversations
14. Final recommendation
15. Sources and useful links

## Short Summary

These approaches answer different engineering questions:

```txt
DDD -> what to build and why it matters to users
FSD -> where code lives and how the app is structured
TDD -> how to prove behavior works correctly
ADD -> how to implement faster with LLM agents under human control
```

For modern LLM-assisted work, the useful sequence is:

```txt
Product hypothesis
  -> Feature boundary
    -> Acceptance tests
      -> Agentic implementation
        -> Human review
          -> Post-release metrics
```

For AI apps, semantic search, RAG, local indexing and user-data workflows, the high-value combination is TDD plus evaluation-driven testing, FSD for UI boundaries, controlled ADD and data-informed metrics.

## Terms

| Abbreviation | Meaning | Practical Use |
| --- | --- | --- |
| **ADD** | Agentic-Driven Development / Agentic Coding Driven Development | LLM agents help plan, code, test, repair and document work. |
| **DDD** | Data-Driven Development | Product and engineering decisions use data, metrics and feedback. Do not confuse this with Domain-Driven Design. |
| **TDD** | Test-Driven Development | Write a failing test first, then implementation, then refactor. |
| **FSD** | Feature-Sliced Design / Feature-Sliced Development | Frontend/UI architecture organized by layers, features and business entities. |

Important: in established frontend practice, **FSD** almost always means **Feature-Sliced Design**. If a team uses another phrase such as "Future Sliced Development", clarify it because it is not the common standard term.

## ADD - Agentic-Driven Development

ADD treats the LLM agent as an active implementation participant, not just a code generator. A useful agent can inspect the repository, plan changes, write code, run tests, read failures, repair implementation, prepare a diff or PR, write documentation and suggest architecture improvements.

The human remains accountable for architecture, quality, security and final decisions.

Typical loop:

```txt
1. Goal / intent
2. Specification / acceptance criteria
3. Agent planning
4. Implementation loop
5. Test run
6. Error repair
7. Human review
8. CI / merge
9. Monitoring / feedback
```

ADD is especially useful when the task has clear boundaries, runnable checks, enough repository context and a review path. It is risky when the prompt is vague, tests are missing, secrets can leak, or the agent can perform external writes without approval.

## DDD - Data-Driven Development

In this draft, DDD means Data-Driven Development. Product decisions start with a hypothesis, select metrics, instrument behavior, collect data, analyze results and decide whether to keep, change or remove the feature.

Useful loop:

```txt
hypothesis -> metric -> instrumentation -> data -> analysis -> decision
```

Data-driven work is strongest for product iteration, funnel changes, search relevance, onboarding, monetization, retention, AI quality thresholds and post-release learning. It is weakest when the metric is a proxy for user value, privacy is unclear, data is too small, or the team treats one number as proof without qualitative review.

Product-Agent OS should express this through a metric spec with primary value metric, input metrics, guardrails, counter-metrics, privacy classification, retention, owner signoff and post-release review.

## TDD - Test-Driven Development

TDD is the Red-Green-Refactor loop:

```txt
1. Write a failing test for the intended behavior.
2. Write the smallest implementation that makes it pass.
3. Refactor while tests stay green.
```

TDD is strongest for business rules, parsers, transformations, shared libraries, bug fixes, API contracts and regressions. It is weaker for visual polish, exploratory prototypes and ambiguous product discovery unless paired with acceptance scenarios or evals.

For LLM/RAG systems, unit tests are not enough. Use eval-driven checks for retrieval quality, factuality, grounding, citation quality, refusal behavior, tool selection and regression prevention.

## FSD - Feature-Sliced Design / Development

Feature-Sliced Design organizes frontend code around layers, slices and segments. A common structure is:

```txt
app/
pages/
widgets/
features/
entities/
shared/
```

The dependency rule is that higher layers can depend on lower layers, while lower layers should not import higher layers. Public APIs on slices make imports explicit and reduce accidental coupling.

FSD is useful for growing UI products, multi-team frontends, business-domain UI flows and apps with many reusable entities/features. It is excessive for tiny prototypes, backend-only work, simple scripts and teams that do not yet have a meaningful UI domain boundary.

## Key Differences

| Approach | Primary Question | Main Artifact | Main Risk |
| --- | --- | --- | --- |
| ADD | How can agents safely implement this work? | Plan, task packet, test evidence, review packet | Autonomous changes without enough verification or approval |
| Data-driven development | Why should this feature exist or change? | Hypothesis, metrics, experiment/review result | Goodhart effects and privacy issues |
| TDD | How do we prove behavior works? | Failing/passing tests and refactor evidence | Writing tests for the wrong behavior |
| FSD | Where should UI code live? | Layer/slice/segment structure and import rules | Forcing UI architecture onto non-UI or small work |

## How The Approaches Fit Together

The practical order for feature work:

1. State a product hypothesis and success/guardrail metrics.
2. Define the feature boundary and target user flow.
3. Choose architecture placement, such as FSD slice for frontend work.
4. Write acceptance scenarios and tests/evals first.
5. Let an LLM agent implement inside the scoped boundary.
6. Run tests/evals and inspect the diff.
7. Record review evidence and release notes.
8. Measure post-release behavior and iterate.

## Use With LLM Agents

### ADD + LLM

Good LLM-agent tasks:

- implement a narrow feature slice;
- add tests and repair failures;
- update docs and examples;
- refactor inside a known boundary;
- prepare a reviewable patch.

Unsafe delegation without more control:

- irreversible migrations;
- production data access;
- external messages or tickets;
- security-sensitive changes without review;
- broad architecture rewrites without a plan.

### Data-Driven Development + LLM

LLM agents can draft metric specs, instrumentation plans, experiment notes and post-release review packets. They should not invent user data, treat generated numbers as facts or bypass privacy review.

### TDD + LLM

LLM agents are useful for writing a regression test, running it, implementing the fix and proving the red -> green transition. The human should still inspect whether the test captures the real behavior.

### FSD + LLM

FSD helps agents place code predictably. The task packet can name the target layer/slice/segment, public API boundary, allowed imports and forbidden cross-layer shortcuts.

## Web, Mobile And Desktop Use

| Platform | Useful Combination | Notes |
| --- | --- | --- |
| Web apps | FSD + TDD/evals + ADD + metrics | Strong fit for feature slices, UI states, Storybook and product metrics. |
| Mobile apps | TDD/evals + ADD + platform build/simulator evidence | FSD may apply for shared React Native/Flutter architecture but should not be forced onto native code. |
| Desktop apps | TDD/evals + ADD + OS-specific runtime checks | Local filesystem, permissions, signing/update and GUI behavior need explicit evidence. |

## Practical Workflow

Recommended loop:

1. Product hypothesis.
2. Metrics definition.
3. Feature boundary.
4. Test/eval design.
5. Agentic implementation.
6. Human review.
7. CI/evals.
8. Release.
9. Measurement.
10. Iteration.

## Example: Search Across Chat Conversations

Feature: "Find commitments in chat exports."

- Data-driven hypothesis: users need to find decisions and commitments faster than manual chat review.
- Metrics: search success rate, time to answer, false positive rate, privacy incidents and qualitative review.
- FSD boundary: UI feature slice for search, entity model for conversations/messages, shared UI for result list.
- TDD/evals: parser tests, date normalization tests, search ranking eval, privacy/no-secret fixture.
- ADD task: implement within the named files, run tests, update docs and produce a review packet.
- Post-release review: compare user success and false positives against guardrails.

## When To Use Which Approach

| Situation | Best Default |
| --- | --- |
| Unclear product value | Data-driven development and product discovery first |
| Complex UI architecture | FSD or another explicit frontend boundary |
| Bug fix or shared behavior | TDD with regression evidence |
| AI/RAG behavior change | Eval-driven tests plus TDD where deterministic |
| Well-scoped implementation | ADD with explicit plan, tests and review |
| High-risk/security/data change | Human review, approval boundary and rollback evidence before agent execution |

## Final Recommendation

Do not treat ADD, data-driven development, TDD and FSD as competing methodologies. Use them as complementary controls:

- data-driven development decides why a change matters;
- FSD or another architecture method decides where code belongs;
- TDD/evals prove behavior;
- ADD accelerates implementation while keeping human ownership and verification.

Product-Agent OS should encode this as behavior-level contracts: inputs, outputs, ownership, verification, risks and the next artifact produced.

## Sources And Useful Links

- [OpenAI Codex build plugins](https://developers.openai.com/codex/plugins/build)
- [OpenAI Codex skills](https://developers.openai.com/codex/skills)
- [Building an AI-Native Engineering Team](https://developers.openai.com/codex/guides/build-ai-native-engineering-team)
- [Codex AI app evals](https://developers.openai.com/codex/use-cases/ai-app-evals)
- [OpenAI eval best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Agile Alliance TDD](https://agilealliance.org/glossary/tdd/)
- [Agile Alliance ATDD](https://agilealliance.org/glossary/atdd/)
- [Agile Alliance BDD](https://agilealliance.org/glossary/bdd/)
- [Feature-Sliced Design documentation](https://feature-sliced.github.io/documentation/)
- [Google HEART paper](https://research.google.com/pubs/pub36299.htmlyaframe=0)
- [Amplitude North Star](https://amplitude.com/north-star-hub)
