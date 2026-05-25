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
| `planned` | `T9-D1` | `business-product.md` | Product hypothesis, value, opportunities, metrics, guardrails and measurement. |
| `planned` | `T9-D2` | `requirements-domain.md` | Requirements quality, acceptance scenarios, business rules, domain model, traceability and change impact. |
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

No domain deep audit has been recorded yet. Each `T9-D*` slice must first read its task block in `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, then audit the matching file under `docs/methodologies/`, then update this backlog if the audit finds missing gates, artifacts, false-positive risks, tooling choices or conflicts.

## Cross-Domain Synthesis Backlog

| Status | Item | Reason |
| --- | --- | --- |
| `planned` | Normalize repeated methodology gates across domains. | Avoid duplicate recommendations for owner questions, evidence, metrics, source status and approval boundaries. |
| `planned` | Add cross-domain false-positive fixtures. | Ensure one methodology signal does not force unrelated heavy process on simple work. |
| `planned` | Synthesize final `methodology-applicability.json` contract. | Give lifecycle skills a stable packet for route decisions and staged artifact suggestions. |
| `planned` | Update operator docs after all domain slices. | Keep the public docs aligned with the implemented domain catalog. |

## Verification Evidence

Current foundation evidence is recorded in the branch commits for Tasks 1 through 7. The required checks for this docs slice are:

- `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`
- `python tools\check_docs.py`
- `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict`

Domain slices must also run the focused catalog/audit tests, fixture evals and any domain-specific docs checks added by that slice.

## Residual Risks

- The catalog currently represents foundation behavior and selected generic gates; domain slices can still reveal missing artifacts or conflicts.
- Read-only audit can classify workspace signals, but owner intent, product risk and regulatory constraints still require human confirmation.
- Recommendation priority order is deterministic, but real-world severity can change when a project has production traffic, sensitive data or external consumers.
