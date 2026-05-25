# Product-Agent OS Track 9 Backlog

Source status: `local implementation planning`

This backlog tracks methodology intelligence work for the local Product-Agent OS plugin. It is planning evidence, not an official OpenAI source.

## Track 9 Goal

Track 9 turns the methodology atlas in `docs/methodologies/` into read-only Product-Agent OS guidance: a catalog, workspace audit, prioritized recommendations, owner questions, staged artifact suggestions and behavioral eval coverage. The plugin must inspect a workspace and explain which methodology gates apply before it proposes any write.

## Foundation Slices

| Status | Slice | Output |
| --- | --- | --- |
| `done` | Task 0 baseline and cleanup | Clean branch baseline before Track 9 implementation. |
| `done` | Task 1 catalog tests | Contract tests for methodology domain metadata. |
| `done` | Task 2 catalog foundation | `methodology_catalog.py` and initial catalog contract. |
| `done` | Task 3 audit tests | Contract tests for read-only methodology audit packets. |
| `done` | Task 4 read-only audit | `methodology_audit.py` with workspace signals, `maturity_level`, `complexity_profile`, recommendations and owner questions. |
| `done` | Task 5 report and CLI | `methodology-audit-report.md`, `methodology_report.py` and `run_methodology_audit.py`. |
| `done` | Task 6 fixture eval integration | Fixture eval fields for methodology catalog, read-only audit and prioritized recommendations. |
| `done` | Task 7 docs foundation | Operator docs, MkDocs navigation, required docs check and Track 9 source registry entry. |

## Domain Integration Queue

| Status | ID | Source file | Scope |
| --- | --- | --- | --- |
| `done` | `T9-D1` | `business-product.md` | Product hypothesis, value, opportunities, metrics, guardrails and measurement. |
| `done` | `T9-D2` | `requirements-domain.md` | Requirements quality, acceptance scenarios, business rules, domain model, traceability and change impact. |
| `planned` | `T9-D3` | `solution-architecture.md` | Architecture boundaries, views, ADRs, quality attributes, tradeoffs, ownership and fitness checks. |
| `planned` | `T9-D4` | `quality-testing-evals.md` | Risk-based tests, evals, current evidence, runtime/manual/visual evidence and CI quality gates. |
| `planned` | `T9-D5` | `codex-agentic-workflow.md` | Control-plane maturity, model/reasoning policy, handoffs, subagents, MCP, hooks, skills, plugins and automation promotion. |
| `planned` | `T9-D6` | `frontend.md` | UI behavior, component states, Storybook applicability, visual/a11y evidence, responsive checks, performance and FSD boundaries. |
| `planned` | `T9-D7` | `backend.md` | Service boundaries, modular monolith vs microservices, runtime behavior, queues, observability, SLOs and rollback. |
| `planned` | `T9-D8` | `api-integrations.md` | OpenAPI/AsyncAPI/GraphQL/gRPC contracts, consumers, compatibility, errors, generated clients and external writes. |
| `planned` | `T9-D9` | `database-data.md` | Database inventory, schema source, migrations, transactions, data quality, classification and production access. |
| `planned` | `T9-D10` | `llm-ai-rag.md` | AI behavior spec, eval baseline, prompts, models, tools, RAG sources, grounding, datasets, approvals and cost/latency. |
| `planned` | `T9-D11` | `security-privacy-compliance.md` | Threat surface, ASVS/SSDF, authorization tests, secrets, privacy impact, supply chain, audit logging and compliance overlays. |
| `planned` | `T9-D12` | `delivery-release-operations.md` | Release readiness, versioning, changelog, artifact manifest, rollout, rollback, CI/CD governance, runbooks and operations. |

## Domain Deep-Audit Log

### `T9-D1` Business and Product Domain Integration

Status: `done`

Source audited: `docs/methodologies/business-product.md`

Implemented scope:

- Added `business_product` catalog coverage for product hypothesis, target segment, value proposition, opportunity-not-solution framing, metrics, analytics tracking, qualitative feedback, privacy classification, AI product eval, release measurement evidence, workflow promotion value evidence, decision horizon, outcome metric levels and metric scope.
- Added `decision_horizons`: `discovery`, `MVP`, `beta`, `production`, `scale`.
- Added staged artifact templates: `product-brief.md`, `value-proposition.md`, `opportunity-tree.md`, `experiment-plan.md`, and `tracking-plan.md`.
- Strengthened `REQUIREMENTS.md`, `PLAN.md`, `EVALS.md`, `RUNLOG.md`, `metric-spec.md`, and `release-notes.md` with product hypothesis, value evidence, analytics, feedback, release measurement, no-production-telemetry fallback and outcome-level fields.
- Added read-only audit recommendations and false-positive coverage for product/MVP/value/metric intent, product analytics, AI product claims, release measurement claims, internal workflow promotion and typo/format/dependency-only work.
- Routed Business/Product methodology into `requirements-author`, `implementation-planner`, `test-eval-designer`, `risk-reviewer`, `learning-loop-maintainer`, and `automation-promoter`.
- Added fixture eval check `business_product_contract_present`.

Severity and false-positive resolution:

- Missing `product_hypothesis_present` is `P2_recommended` for discovery-only or empty-workspace MVP intent, but becomes `P1_high_risk` for implementation or release intent without product hypothesis evidence.
- Product analytics or usage data claims trigger `analytics_tracking_plan_present` and `tracking-plan.md`; plain metric hardening remains in `metric-spec.md`.
- Release success claims require `release_measurement_evidence_present`; no production telemetry must be recorded as an explicit fallback rather than treated as success evidence.
- Internal workflow promotion requires value evidence such as `engineering time saved`, and stays candidate-only until manual stability, owner, verification and rollback evidence exist.
- Typo-only docs edits, formatting-only edits and dependency pin changes without behavior impact keep `business_product` not applicable.

### `T9-D2` Requirements and Domain Integration

Status: `done`

Source audited: `docs/methodologies/requirements-domain.md`

Deep-audit deltas to implement:

- Extend Track 8 acceptance scenarios, conditional DDD, bounded-context traceability, ubiquitous-language traceability and false-positive protection instead of duplicating them.
- Represent requirement taxonomy when relevant: functional, non-functional, compliance, operational, AI behavior, data/privacy and release/rollback.
- Add requirement quality criteria as a first-class gate: atomicity, clarity, testability, feasibility, traceability, source and owner.
- Require stable requirement IDs for multi-slice, regulatory, risky, long-lived or public-contract work.
- Add a requirement registry with status, owner, source and linked artifacts.
- Treat stakeholder/owner mapping as a first-class artifact for source-backed domain meaning and business rules.
- Preserve story slicing evidence: value slice, risk slice, MVP boundary, deferred slices, non-goals and acceptance scenario links.
- Record business rules with source, owner, enforcement layer, exceptions, failure mode and tests/evals.
- Use Example Mapping for unclear, large or disputed stories: story -> rules -> examples -> questions.
- Require domain discovery workshop evidence for complex workflow, cross-silo process or overloaded domain language.
- Track constraints across compliance, privacy, security, operational, performance, platform, accessibility, data retention, localization, cost, rollout and rollback.
- Require declarative acceptance scenarios with no UI selectors, database internals, function names or test harness details.
- Record invariants and failure modes when domain state transitions matter.
- Require domain event contract evidence when events cross boundaries: meaning, producer, consumers, schema link, ordering/idempotency and privacy classification.
- Add API/UI/data traceability distinct from DDD traceability: requirement/domain term -> API/event/schema/UI/data/code/test/eval.
- Require domain expert or owner review for business-critical, compliance, finance/legal and AI-generated domain claims.
- Require requirement change impact review after planning changes: tests/evals, API, DB, UI, docs, rollout and rollback.
- Allow accepted gaps only with owner, reason, scope, review date, downstream risk and follow-up condition.
- Route `docs-maintainer` to maintain requirement IDs, source registry, glossary/ubiquitous-language docs and traceability docs after the requirements packet exists.
- Reject unsupported claims as evidence: BDD replaces testing, Gherkin is mandatory, a user-story template is complete requirements, a glossary is ubiquitous language, and OpenAPI is requirements source of truth.

Implemented scope:

- Added `requirements_domain` catalog coverage for requirements scope/owner, requirement quality, stable IDs, acceptance scenarios, declarative scenario quality, requirements traceability, business rules, non-goals/constraints, open questions, Example Mapping, domain discovery, conditional DDD, invariants/failure modes, domain events, API/UI/data traceability, domain expert review, change impact, accepted gaps and evidence-before-implementation.
- Added staged artifact templates: `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, and `domain-review-record.md`.
- Strengthened `acceptance-scenarios.md`, `domain-modeling.md`, generated `REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG`, Product-Agent OS README and lifecycle skills with Requirements & Domain gates.
- Added a `docs-maintainer` lifecycle skill for requirement IDs, source registry, glossary/ubiquitous-language and traceability docs after the requirements packet exists.
- Added read-only audit recommendations and false-positive coverage for behavior changes, risky/public-contract work, unclear stories, business rules, domain events, owner review, change impact, accepted gaps, declarative scenarios, unsupported methodology claims and typo/format/dependency-only work.
- Added fixture eval check `requirements_domain_contract_present`; renderer file count is now 88 after adding eight Requirements & Domain artifact templates.

Severity and false-positive resolution:

- Behavior-changing work without acceptance scenarios is a `P0_blocker`.
- Requirement quality, stable requirement IDs for risky/public-contract work, constraints traceability, API/UI/data traceability, business rules, domain event contracts, domain expert review, change impact, accepted gaps and declarative scenario quality are `P1_high_risk` when applicable.
- Stakeholder/owner map, story-slice map, Example Mapping and domain discovery workshop evidence are `P2_recommended` unless other risk gates raise severity.
- Typo-only docs edits, formatting-only edits and dependency metadata without behavior impact keep `requirements_domain` not applicable for README-only work.
- Unsupported claims are rejected as evidence: BDD replaces testing, Gherkin is mandatory, user story template is complete requirements, glossary is ubiquitous language, and OpenAPI is requirements source of truth.

## Cross-Domain Synthesis Backlog

| Status | Item | Reason |
| --- | --- | --- |
| `planned` | Normalize repeated methodology gates across domains. | Avoid duplicate recommendations for owner questions, evidence, metrics, source status and approval boundaries. |
| `planned` | Add cross-domain false-positive fixtures. | Ensure one methodology signal does not force unrelated heavy process on simple work. |
| `planned` | Reuse decision horizon across requirements, architecture, release and operations domains. | Product formalism should scale by `discovery`, `MVP`, `beta`, `production` and `scale` rather than forcing production ceremony on early discovery. |
| `planned` | Normalize outcome metric levels across product, quality, release and workflow automation domains. | Separate `business_outcome`, `product_outcome` and `feature_traction_metric` to reduce proxy metric risk. |
| `planned` | Standardize no-production-telemetry fallback language. | Product, release and operations domains need the same rule: lack of telemetry is a gap, not success evidence. |
| `planned` | Carry workflow-promotion value evidence into agentic workflow and operations domains. | Automation promotion should require manual stability plus value evidence such as engineering time saved before any schedule or external action. |
| `planned` | Synthesize requirement/API/UI/data traceability across Requirements, Architecture, API, UI and Data domains. | T9-D2 introduces the trace chain before later domains own contract, UI and schema-specific enforcement. |
| `planned` | Reuse stakeholder/owner mapping across Product, Requirements, Security, Release and Operations domains. | Owner review appears repeatedly and should have one durable shape for source, decision authority and escalation. |
| `planned` | Carry story-slice and MVP boundary evidence into Product, Frontend and Delivery domains. | Requirements slicing should inform UI scope, rollout scope and release notes without forcing heavy ceremonies. |
| `planned` | Normalize domain event requirements across Requirements, API/Integrations and Data domains. | Event meaning, schema, ordering, idempotency and privacy classification will be shared by multiple later slices. |
| `planned` | Normalize accepted-gap records across all methodology gates. | Accepted gaps need owner, reason, scope, review date, downstream risk and follow-up condition everywhere, not only in T9-D2. |
| `planned` | Normalize owner/domain expert review across business-critical, compliance, finance/legal and AI-generated claims. | Later Security, AI and Release domains need the same human-review evidence packet. |
| `planned` | Normalize change-impact review across requirements, API, data, UI, docs, release and rollback. | Requirement changes after planning should produce a shared impact review rather than domain-specific fragments. |
| `planned` | Synthesize final `methodology-applicability.json` contract. | Give lifecycle skills a stable packet for route decisions and staged artifact suggestions. |
| `planned` | Update operator docs after all domain slices. | Keep the public docs aligned with the implemented domain catalog. |

## Verification Evidence

Current foundation evidence is recorded in the branch commits for Tasks 1 through 7. The required checks for this docs slice are:

- `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`
- `python tools\check_docs.py`
- `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict`

Domain slices must also run the focused catalog/audit tests, fixture evals and any domain-specific docs checks added by that slice.

`T9-D1` evidence:

- `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_fixture_eval_runner -v` ran 105 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; fixture renderer file count is now 80 after adding five Business/Product artifact templates.
- `python -m unittest discover -s tests -p "test_*.py" -v` ran 347 tests with `OK`.
- `python tools\check_docs.py` passed.
- `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.

`T9-D2` evidence:

- RED run: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_fixture_eval_runner -v` failed as expected before implementation on missing `requirements_domain` gates, artifact templates, audit recommendations, `docs-maintainer` skill and fixture check; the run reached fixture eval and timed out after 120 seconds after showing the expected failures.
- Focused catalog/audit run: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit -v` ran 18 tests with `OK`.
- Focused renderer/lifecycle/fixture run: `python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_fixture_eval_runner -v` ran 97 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; fixture renderer file count is now 88 and `requirements_domain_contract_present` is true for `python-app`.
- `python -m unittest discover -s tests -p "test_*.py" -v` ran 357 tests with `OK`.
- `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.

## Residual Risks

- The catalog currently represents foundation behavior and selected generic gates; domain slices can still reveal missing artifacts or conflicts.
- Read-only audit can classify workspace signals, but owner intent, product risk and regulatory constraints still require human confirmation.
- Recommendation priority order is deterministic, but real-world severity can change when a project has production traffic, sensitive data or external consumers.
