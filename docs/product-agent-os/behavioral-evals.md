# Product-Agent OS behavioral evals

Source status: `official + experiment`

Источники: [Codex use cases](https://developers.openai.com/codex/use-cases), [Codex workflows](https://developers.openai.com/codex/workflows), [OpenAI eval best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices), [Agent evals](https://developers.openai.com/api/docs/guides/agent-evals), [Product-Agent OS scenarios](scenarios.md).

Behavioral evals проверяют не Markdown-синтаксис, а поведение Product-Agent OS route: правильный first response, отсутствие forbidden shortcuts, требуемые artifacts, evidence-before-completion и stop condition. Главный шаблон для этих проверок - `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json`.

Fixture eval and docs tests prove structure, expected terms, forbidden terms and route safety. They do not prove real project readiness. Real projects still need current command evidence, runtime evidence, owner review or explicit accepted gaps.

## Runtime Packet Safety

Runtime packet safety is covered by deterministic checks for `methodology_packet`, `finish_options`, approval-bound high-risk actions, redaction and malformed packet fallback. The explicit guard is detection-not-completion plus approval-bound routing for high-risk actions.

Transcript/session replay stays local and deterministic. The transcript/session replay catches missing expected behavior, forbidden shortcuts and privacy/no-secrets issues; it is not a semantic judge.

## Live And Graph Behavior Coverage

Generated graph, cockpit, local runtime contracts, provider gates, review ledgers, mutation plans, audit packets and real-testing readiness are evidence surfaces with explicit limits.

| Route or gate | Expected behavior | Forbidden behavior |
| --- | --- | --- |
| `code_graph_orientation` | Use graph/cockpit as source map, label stale or generated evidence, then read source files before implementation claims. | Treat `project-code-graph.json`, cockpit HTML or generated labels as source of truth. |
| `live_runtime_read_only` | Require governance prerequisite, disabled-by-default lifecycle, local-only auth boundary and graph-only fallback. | Start a live server, expose public routes, add write endpoints or claim runtime proof from contract inspection. |
| `provider_retrieval_eval` | Require redaction, credentials boundary, cache deletion, budget, baseline, threshold and fallback before provider consideration. | Perform provider/live external model/API calls or claim quality from proposal-only evidence. |
| `canonical_graph_mutation_review` | Require accepted owner decision, diff preview, dry-run mutation plan, mutation journal and rollback proof. | Mutate canonical graph from LLM proposal, semantic hit or accepted gap. |
| `real_testing_approval` | Split runtime launch, browser automation smoke, provider/API pilot, canonical mutation pilot and explicit git release/PR action into separate approvals. | Bundle approvals, run browser automation, call providers, mutate graph or stage/commit/push without separate approval. |
| `agent_skill_handoff_routing` | Require ownership, fresh context, expected evidence, files owned/forbidden and stop conditions before subagent or skill work. | Delegate with only a generated handoff packet and no work context. |

## Inputs

- scenario or methodology gate that needs validation;
- user prompt or synthetic route input;
- workspace fixture when behavior depends on files;
- expected behavior: mode, minimum artifacts, next action, approval boundary and evidence fields;
- forbidden behavior: scaffold before approval, broad rewrite, unsupported ready claim, external mutation or missing source status;
- residual risk and reason when a case remains structural only.

## Outputs

- behavioral eval case with `id`, prompt/context, expected behavior, forbidden behavior and evidence requirements;
- fixture eval assertion when behavior can be checked through a synthetic workspace;
- failure note for `RUNLOG.md` when a route or lifecycle skill misses a shortcut;
- transcript/session eval report with `behavioral_case`, `expected_terms`, `forbidden_terms`, `missing_expected_terms`, `forbidden_terms_present` and `privacy_errors`.

## Eval Layers

| Layer | What it checks | Current status | Verification |
| --- | --- | --- | --- |
| Template validation | JSON shape, required fields and no placeholder behavior. | Implemented. | `tests/product_agent_os/test_behavioral_workflow_evals.py`. |
| Route and fixture eval | Synthetic workspaces return expected `usage_mode`, artifacts and expected checks. | Implemented for current scenarios and false-positive fixtures. | `python plugins\product-agent-os\scripts\run_fixture_eval.py`. |
| Methodology intelligence eval | Read-only methodology audit returns catalog coverage, `maturity_level`, `complexity_profile`, prioritized recommendations and no target-workspace mutation. | Implemented. | `methodology-intelligence-read-only-first` and `methodology_intelligence_contract_present`. |
| Solution architecture eval | Catalog, audit, templates and lifecycle skills preserve conditional architecture gates and reject unsupported architecture claims. | Implemented. | `solution_architecture_contract_present`. |
| Codex agentic workflow eval | Catalog, audit, templates and lifecycle skills preserve source-of-truth, approval, handoff, MCP, hook, skill, plugin, automation, model/reasoning, memory and agent eval gates without silent activation. | Implemented. | `codex_agentic_workflow_contract_present`. |
| Frontend eval | Catalog, audit, templates, lifecycle skills and fixtures preserve user-flow, component-state, Storybook/FSD, visual, accessibility, runtime, interaction and performance gates without accepting code-inspection-only UI completion. | Implemented. | `frontend_contract_present`. |
| Backend eval | Catalog, audit, templates, lifecycle skills and fixtures preserve service boundary, runtime/failure/observability/security/rollback evidence, dependency failure policy, CI/deployment discovery, severity policy and owner reviewed evidence sufficiency. | Implemented. | `backend_contract_present`. |
| API & Integrations eval | Catalog, audit, templates, lifecycle skills and fixtures preserve contract source, consumer, compatibility, security, error, event, SDK and external-write evidence. | Implemented. | `api_integrations_contract_present`. |
| Database & Data eval | Catalog, audit, templates, lifecycle skills and fixtures preserve database inventory, schema source, migration plan, expand-contract rollout, data contract, privacy, lineage, performance, retention and production approval evidence. | Implemented. | `database_data_contract_present`. |
| LLM / AI / RAG eval | Catalog, audit, templates, lifecycle skills, fixtures and transcript replay preserve AI behavior, baseline/current eval, prompt/model/tool/RAG/grounding, guardrail, trace, handoff, tooling, migration, lifecycle and incident evidence. | Implemented. | `llm_ai_rag_contract_present`. |
| Security, Privacy & Compliance eval | Catalog, audit, templates, lifecycle skills and fixtures preserve security-sensitive classification, threat surface, ASVS/SSDF/SAMM mapping, authorization negative tests, secrets, privacy, supply chain, SBOM/provenance, audit logging, Codex Security scan status and compliance overlay evidence. | Implemented. | `security_privacy_compliance_contract_present`. |
| Delivery, Release & Operations eval | Catalog, audit, templates, lifecycle skills and fixtures preserve release scope, versioning, changelog, artifact manifest, current evidence, rollout, rollback, environments, CI/CD governance, SLO/observability, operations, incidents, post-release review, automation promotion, release mode policy, build-release-run boundary, platform distribution evidence, release communication, DORA measurement design, release integrity handoff and owner-reviewed evidence sufficiency. | Implemented. | `delivery_release_operations_contract_present`. |
| Cross-domain synthesis eval | Catalog, audit, reports, lifecycle skills and fixtures preserve grouped recommendations, owner domains, consumer domains, source artifact compatibility, semantic evidence sufficiency, risk-aware safe next action and false-positive routing. | Implemented. | `cross_domain_synthesis_contract_present`, `safe_next_action_risk_ordered`, `source_artifact_mapping_contract_present`, `cross_domain_false_positive_guards_present`. |
| Readiness contract eval | `project-readiness.json` has conditional gates, statuses, evidence owner and residual risk. | Implemented. | `conditional_readiness_gates_contract_present`. |
| Codex compatibility eval | Plugin remains Codex-only and avoids non-Codex adapter requirements. | Implemented. | `python plugins\product-agent-os\scripts\validate_codex_compatibility.py`. |
| transcript/session eval runner | Replay synthetic or redacted Codex session transcripts for multi-turn shortcut resistance, evidence quality and privacy/no-secrets checks. | Implemented. | `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json`. |
| Guided question and status dashboard eval | Typed question packets, compact first response, generated dashboard boundaries and stale-evidence language. | Implemented. | `question_queue_contract_present`, `status_snapshot_present`, `status_dashboard_present`, `dashboard_no_external_assets`, `dashboard_not_source_of_truth`, `stale_evidence_no_success_claim`. |
| Self-verification metrics loop eval | `agent_skill_metrics_loop` target registry, trace intake, dataset quality, grader/judge calibration, cadence recommendation, scorecard ledger, report safety, staged modernization candidates and approval boundary. | Implemented. | `agent_skill_metrics_loop_contract_present`, `metrics_report_redacted`, `trace_normalization_contract_present`, `judge_calibration_gate_present`, `scorecard_ledger_contract_present`, `metrics_loop_runtime_route_contract_present`, `metrics_loop_lifecycle_contract_present`. |

## Guided Questions And Dashboard

Guided question protocol uses typed `question_queue` packets. The first response shows only `next_blocking_question`, `question_counts` and `question_summary`; optional questions stay in the packet and answers route into artifacts or accepted gaps.

Behavioral cases include `guided-question-smallest-blocking-question`, `guided-question-no-broad-methodology-interview`, `status-dashboard-generated-view-only`, `status-dashboard-stale-evidence-no-success-claim` and `runtime-first-response-no-question-dump`.

Expected behavior: one blocking question maximum, no broad methodology interview, no full queue dump in first response, no dashboard-as-source-of-truth and no success claim from stale evidence.

The status dashboard stages `.codex/product-agent-os/status.html` and `.codex/product-agent-os/status.json` from a `status_snapshot`. Dashboard HTML is a generated view over underlying artifacts, not an editable database and not source of truth. Stale or inspection-only evidence cannot produce a success claim.

## Self-Verification Metrics Loop

`agent_skill_metrics_loop` is a staged self-verification metrics loop for agents, skills, prompt/policy packs, router/tool policy and harness-version review. Expected behavior starts with read-only target registry, trace intake, dataset quality blockers, local grader outputs, grader/judge calibration, cadence recommendation levels `L0`, `L1`, `L2` and `L3`, scorecard ledger, `agent-skill-evaluation-report.html` and modernization candidates with evidence, rollback and owner-review state.

The source-of-truth policy is part of the eval contract: control-plane artifacts, run records, trace/eval packets and accepted gaps are allowed evidence; generated dashboard/report HTML, memory, raw chat logs and unsupported community claims are not. Every metrics report is staged evidence only, and the report is not source of truth.

Forbidden behavior includes headline-metric-only approval, raw trace leakage, uncalibrated judge approval, no self-applied updates, missing rollback target, no live eval/model/API calls, no active schedules and modernization candidates that cross approval boundary without explicit owner review.

## Expected Behavior

Each case should name behavior, not only a file name.

- `bug_rescue`: reproduce or isolate before fix; no fixed claim without current evidence.
- `greenfield_idea`: select direction and first vertical slice before scaffold.
- `complex_system_acceleration`: require integration catalog and ownership split before parallel work.
- `pr_review`: read-only review with spec compliance before quality/risk.
- `api_migration`: migration plan and contract compatibility before implementation or release.
- `ai_eval_regression`: baseline and rerun command before prompt/model/retrieval/rubric changes.
- `release_packaging`: release readiness before publish, tag, upload or package registry mutation.
- `evidence-before-completion`: ready/completed/fixed/works/release claims need current evidence or explicit inspection-only gap.
- `methodology-intelligence-read-only-first`: methodology audit must return a Delivery Map, prioritized recommendations and owner questions before any staged proposal.
- `solution_architecture_contract_present`: architecture gates require scope, boundaries, owner, ADR/tradeoff, observability, rollback, render check and accepted-gap evidence without forcing heavyweight architecture ceremony when not applicable.
- `codex_agentic_workflow_contract_present`: Codex workflow gates require control plane, source of truth, read-only discovery, approval boundaries, model/reasoning policy, memory policy, fresh-context handoff, ownership split, subagent safety, MCP review, hook governance, skill promotion, plugin boundary, automation stability and agent eval workflow.
- `frontend_contract_present`: frontend gates require user-flow acceptance, component state matrix, design-system boundary, Storybook/FSD routing, API/data state alignment, WCAG 2.2 AA target or accepted exception, browser/runtime evidence, console status, Playwright trace or accepted gap, visual evidence, interaction checks and performance budget where applicable.
- `backend_contract_present`: backend gates require `backend-service-overview.md`, `backend-runtime-behavior.md`, runtime/failure/observability/security/rollback evidence, framework-agnostic backend policy, severity routing, CI/deployment discovery signals and owner reviewed evidence sufficiency for real project risk or accepted gap.
- `api_integrations_contract_present`: API gates require a source-of-truth contract, consumer map, compatibility review, security schemes, error contract, contract test matrix, event/webhook delivery evidence, generated SDK manifest, observability and `approval_required` handling for external writes.
- `database_data_contract_present`: Database & Data gates require `database-inventory.md`, `database-dictionary.md`, `database-migration-plan.md`, `database-data-contract.md`, rollback/backup evidence, data classification, data quality, lineage, query performance, retention/deletion, synthetic fixtures and `database-production-access-approval.md` where applicable.
- `llm_ai_rag_contract_present`: LLM / AI / RAG gates require AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, prompt contract, model decision record, structured output schema, tool/function/MCP contract, human approval boundary, RAG source inventory, retrieval config, grounding rubric, agent work packet, workflow trace, guardrail matrix, trace evidence packet, cost/latency budget, eval tooling selector, model migration policy, RAG lifecycle/privacy, AI incident workflow and reportable approval/gap/risk evidence.
- `security_privacy_compliance_contract_present`: Security, Privacy & Compliance gates require security-sensitive classification, threat surface, security risk review, ASVS/SSDF/SAMM mapping, API security scheme, authorization negative tests, secrets policy, data classification, redaction lifecycle, privacy impact, external-write approval, abuse/rate-limit review, audit logging, supply-chain review, SBOM/provenance decision, CI permission review, AI security review, compliance overlay taxonomy, vulnerability response workflow, explicit Codex Security scan status and current evidence before completion.
- `delivery_release_operations_contract_present`: Delivery, Release & Operations gates require release scope, SemVer/versioning, changelog/release notes, artifact manifest, release evidence before completion, rollout strategy, rollback/recovery, environment approval boundary, external release approval, CI/CD governance, observability/SLO, operations runbook, incident response, post-release review, automation manual stability, release mode policy, build-release-run boundary, platform distribution evidence, release communication, versioning tooling decision, GitHub environment controls, DORA measurement design, incident postmortem learning, observability on-call tooling, release integrity security handoff and owner-reviewed evidence sufficiency.
- `cross_domain_synthesis_contract_present`: Cross-domain synthesis gates require `methodology_synthesis`, `recommendation_groups`, owner domains, consumer domains, `source_artifact_ledger`, semantic evidence sufficiency, risk-aware safe next action and source artifact alias/deferred decisions.
- `question_queue_contract_present`: guided question protocol exposes `next_blocking_question`, `question_counts` and `question_summary` while preserving the full typed packet outside the first response.
- `status_dashboard_present`: status dashboard generation stages `.codex/product-agent-os/status.html` and `.codex/product-agent-os/status.json` from a `status_snapshot`; dashboard is a generated view and not source of truth.
- `false-positive fixtures`: backend/native work does not force FSD, simple CRUD `src/domain/*` does not force DDD, docs-light does not force a docs portal, hosted docs and DB introspection stay approval-required.

## Forbidden Behavior

Forbidden behavior is the part that catches shortcuts:

- scaffold before approval;
- broad rewrite before root cause;
- parallel work without ownership split;
- review verdict without spec-compliance stage;
- compatibility claim without contract check evidence;
- quality claim for AI/RAG without baseline or rerun;
- CI health claim from stale logs;
- release claim without build/test/docs evidence;
- methodology recommendation that writes target files, enables hooks, creates automation or mutates external systems before approval;
- Codex workflow recommendation that treats memory as source of truth, subagents as automatically faster, MCP as safe by default, hooks as harmless, Agents SDK as the Codex runtime layer or repeated workflows as immediately automation-ready;
- frontend completion from code inspection only, Storybook-only evidence, desktop-only screenshot, automated accessibility addon output alone, mandatory FSD claim or lab Web Vitals as guaranteed production UX;
- API completion from Swagger UI/rendered docs, schema validation alone, OAuth-only security notes, universal GraphQL/gRPC/event defaults or external writes without `approval_required`;
- database completion from schema-only files, ORM introspection, generated ERD/dbdocs, unapplied migration scripts, down-migration-only rollback claims, backup-exists claims without restore evidence, unsafe production data access or destructive migration without owner approval;
- AI/RAG completion from prompt inspection, stale eval output, citations-only grounding, schema-only tool safety, automatic model-upgrade quality claims or missing current baseline/current eval evidence;
- security/privacy/compliance completion from after-the-fact review, no-secrets-in-code, ASVS/OWASP name-dropping, one-time SBOM, implied Codex Security scan, OAuth-only security notes, universal privacy compliance, docs-only security article or compliance certification claim without legal/compliance owner;
- delivery/release/operations completion from CI green, local test evidence alone, generated changelog, feature flag file, GitOps file, deploy manifest or repeatable script without release evidence, artifact manifest, rollout, rollback, owner review, approval boundary and automation manual stability evidence where applicable;
- source-backed OpenAI/Codex claim without Source status or registry support;
- external write, remote CI mutation, publish, tag, upload or package-registry action without approval;
- full question queue dump in first response, broad methodology interview, dashboard as source of truth or ready/completed/success claim from stale evidence.

## Domain Contract Phrases

These exact phrases are kept as public quality contract language for route/eval maintenance:

- owner reviewed test/eval/runtime evidence sufficiency;
- Swagger UI is not source of truth;
- external writes are approval_required;
- schema-only artifact is not safety proof;
- production access approval_required;
- Prompt inspection is not enough;
- citations alone do not prove grounding;
- security_sensitive_classification_present;
- Codex Security scan is implied;
- privacy compliance is universal;
- generic quality strategy hides security approval;
- automation_manual_stability_present;
- DORA metrics prove individual performance;
- single observability tool is mandatory;
- owner-reviewed release evidence sufficiency;
- GitOps is automatically safe;
- repeatable automation is automatically safe.

## Verification

Run focused checks after changing behavioral cases:

```powershell
python -m unittest tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
```

Run full checks after plugin templates, fixture eval or route logic changes:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
```

Use strict MkDocs when docs navigation, Mermaid, Markdown extensions or MkDocs config change.

## Risks

- Fixture eval proves expected structure and route outputs, not deep semantic quality of a real product decision.
- False-positive fixtures cover selected synthetic layouts; unusual real project layouts still need owner review.
- Behavioral eval cases can become too broad; keep each case focused on one shortcut or route contract.
- Transcript/session eval runner is deterministic and local; it catches missing terms, forbidden shortcuts and unsafe transcript content, but it is not an LLM semantic judge.
- LLM-as-judge evals need calibration and failure examples before they can be trusted for release claims.

Next artifact: use [Scenarios](scenarios.md) to choose the route and [Codex compatibility](codex-compatibility.md) to confirm package scope.
