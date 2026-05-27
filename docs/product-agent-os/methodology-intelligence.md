# Methodology Intelligence

Source status: `local product design + experiment`

Methodology Intelligence is the Track 9 layer of Product-Agent OS. It reads workspace evidence, maps it to the methodology atlas, and returns a read-only route packet before any staged artifact or target-project write is proposed.

## Inputs

- Workspace files and lightweight signals such as stack markers, control-plane files, docs files, API specs, release files and deployment markers.
- Product-Agent OS methodology catalog entries for business, requirements, architecture, quality, Codex / agentic workflow, frontend, backend, API, data, AI, security and delivery domains.
- Current user request, when it changes applicability or risk classification.
- Existing lifecycle artifacts such as `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md`.

## Outputs

- `methodology_applicability` packet with `maturity_level`, `complexity_profile`, applicable domains, missing gates, owner questions and residual risks.
- Delivery Map that groups recommendations into immediate blockers, high-risk gaps, useful maturity improvements and non-applicable items.
- `methodology-audit-report.md` as a human-readable report template for current evidence and next actions.
- `methodology-applicability.json` as the planned stable machine-readable packet for lifecycle skills.
- Questions for owner when evidence is missing, ambiguous or approval-bound.

## Read-Only First

The audit is read-only by default. It can inspect the target workspace and generate reports, but it must not write into the target project, enable hooks, create automations, contact external systems or change GitHub/CI/package registries. If a recommendation needs files, the next step is a staged proposal with explicit owner approval.

`maturity_level` describes how much Product-Agent OS evidence is present, from early/uninitialized workspaces to projects with current requirements, plan, tests, evals and runlog. `complexity_profile` records why a workspace looks simple, product-heavy, multi-service, data-sensitive, release-oriented, AI/RAG-heavy or governance-heavy.

## Delivery Map

Delivery Map turns methodology findings into an execution order:

| Priority | Meaning | Required behavior |
| --- | --- | --- |
| `P0_blocker` | Missing evidence blocks responsible implementation or completion claims. | Stop at read-only report or staged proposal. |
| `P1_high_risk` | Work can continue only with explicit risk handling, owner question or artifact gap. | Add the gate to plan, tests, evals or review packet before build/release. |
| `P2_recommended` | Useful improvement for maturity, maintainability or observability. | Stage when it fits the current slice. |
| `P3_optional_maturity` | Helpful for advanced teams, but not required for the immediate task. | Keep as backlog unless owner asks. |
| `not_applicable` | Domain or gate does not fit the workspace or request. | Record reason; do not force process. |

## Methodology Recommendations

Recommendations must name the domain, reason, evidence used, priority, suggested artifact and verification path. A good recommendation says what to inspect next and what artifact would make the gap measurable.

Examples:

- business/product work needs a hypothesis, success metric, counter-metric and measurement owner;
- complex domain work needs domain model and bounded-context traceability;
- solution architecture work needs scope, context/container boundaries, boundary owner, ADR/tradeoff evidence, public contract trace, data ownership, trust boundary review, observability, rollback and diagram render evidence when applicable;
- AI/RAG work needs baseline eval, dataset policy, grounding evidence and cost/latency guardrails;
- Security/Privacy/Compliance work needs threat surface, security-sensitive classification, data classification, authorization negative tests, privacy impact, supply-chain evidence, Codex Security scan status and compliance overlay ownership;
- release or migration work needs rollback, compatibility and owner approval evidence.

## Implemented Domain Contracts

| Domain | Fixture eval check | Current artifact coverage |
| --- | --- | --- |
| Business/Product | `business_product_contract_present` | `product-brief.md`, `value-proposition.md`, `opportunity-tree.md`, `experiment-plan.md`, `tracking-plan.md`, `metric-spec.md`. |
| Requirements/Domain | `requirements_domain_contract_present` | `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `domain-modeling.md`, `domain-review-record.md`. |
| Solution Architecture | `solution_architecture_contract_present` | `architecture-overview.md`, `adr.md`, `architecture-review-record.md`, `architecture-fitness-functions.md`, `trust-boundary-map.md`, `architecture-docs-tooling-decision.md`. |
| Backend | `backend_contract_present` | `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-operational-runbook.md`. |
| API & Integrations | `api_integrations_contract_present` | `api-inventory.md`, `api-contract-review.md`, `api-consumer-map.md`, `api-contract-test-matrix.md`, `external-integration-approval.md`. |
| Database & Data | `database_data_contract_present` | `database-inventory.md`, `database-dictionary.md`, `database-migration-plan.md`, `database-data-contract.md`, `database-production-access-approval.md`. |
| LLM / AI / RAG | `llm_ai_rag_contract_present` | `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `rag-source-inventory.md`, `guardrail-matrix.md`. |
| Security/Privacy/Compliance | `security_privacy_compliance_contract_present` | `security-risk-review.md`, `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `supply-chain-review.md`, `sbom-manifest.md`, `compliance-overlay.md`, `vulnerability-response-record.md`, `approval-record.md`. |
| Delivery/Release/Operations | `delivery_release_operations_contract_present` | `versioning-policy.md`, `release-readiness.md`, `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `environment-matrix.md`, `deployment-plan.md`, `ci-cd-workflow-inventory.md`, `observability-map.md`, `slo-spec.md`, `operations-runbook.md`, `incident-record.md`, `postmortem.md`, `post-release-review.md`, `automation-candidate.md`. |

Delivery/Release/Operations reports also preserve release mode policy, build-release-run boundary, platform distribution evidence, release communication, versioning tooling decision, GitHub environment controls, DORA measurement design, incident postmortem learning, observability/on-call tooling, release integrity security handoff and owner-reviewed release evidence sufficiency. Detection of those terms is not readiness evidence by itself.

## Approval Boundary

Methodology Intelligence can recommend `staged_only` or `approval_required`, but it cannot silently move from advice to mutation. Hosted docs, production database access, remote CI mutation, package publishing, release creation, tags, artifact upload, deploys, package registry mutation, active automations, hook activation and external writes remain approval-bound.

Owner questions are part of the output, not a failure. They keep ambiguity visible: who owns a missing methodology gate, which requirement is source-backed, which system is production, which data is sensitive, and which risk is accepted rather than fixed in the current slice.

## Verification

For docs-only changes to this page, run:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict
```

For implementation changes to methodology audit or catalog behavior, also run focused Product-Agent OS unit tests and fixture evals:

```powershell
python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

## Risks

- Static workspace signals can miss product intent, hidden dependencies, regulatory context and production risk.
- Over-eager methodology routing can force heavy process onto simple work; every domain recommendation needs applicability and false-positive handling.
- Read-only reports can become stale quickly; completion or release claims still need fresh command, runtime, eval or owner evidence.
- `methodology-applicability.json` is planned as a stable packet, but domain slices can refine its schema before Track 9 synthesis.
