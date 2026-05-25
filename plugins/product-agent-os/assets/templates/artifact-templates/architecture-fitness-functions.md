# Architecture Fitness Functions

Source status: `local methodology artifact`

Project: {project_name}

Use this artifact for `architecture_fitness_function_present`, `dependency_rules_present`, `observability_architecture_present`, contract drift, docs freshness, dependency rule checks and runtime evidence.

## Owner

- Architecture owner:
- Test/eval owner:
- Operations owner:
- Evidence owner:
- Follow-up owner:

## Dependency Rules

| Boundary | Allowed dependencies | Forbidden dependencies | Owner | Verification command |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Fitness Function Catalog

| Fitness function | Gate | Trigger | Command or evidence | Status | Residual risk |
| --- | --- | --- | --- | --- | --- |
| Dependency rule check | `dependency_rules_present` | Boundary or module change |  |  |  |
| Contract drift check | `public_contract_boundary_trace_present` | API/event/SDK change |  |  |  |
| Docs freshness check | `architecture_docs_as_code_present` | Architecture docs change |  |  |  |
| Observability check | `observability_architecture_present` | Runtime behavior change |  |  |  |
| Security gate check | `trust_boundary_security_review_present` | Trust boundary change |  |  |  |
| AI eval threshold | `quality_attribute_scenarios_present` | AI behavior or agent workflow change |  |  |  |

## Observability Architecture

- Logs:
- Metrics:
- Traces:
- Dashboards:
- Alerts:
- Health checks:
- Owner:

## Verification

- Current command evidence:
- Current eval evidence:
- Current runtime evidence:
- Known failing check:
- Accepted gap:

## Residual Risk

- Risk:
- Mitigation:
- Follow-up condition:
- No secrets, credentials, private customer data, raw private chat logs, connection strings or unpublished roadmap details stored in this artifact:
