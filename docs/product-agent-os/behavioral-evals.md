# Product-Agent OS behavioral evals

Source status: `official + experiment`  

## Task 22 eval closure

Task 22 eval closure treats fixture eval limits as part of the contract. Fixture eval and docs tests prove structure, expected terms, forbidden terms and route safety; synthetic regression evidence does not prove real project readiness. Real projects still need current command evidence, runtime evidence, owner review or explicit accepted gaps.

Runtime packet safety is covered by deterministic checks for `methodology_packet`, `finish_options`, approval-bound high-risk actions, redaction and malformed packet fallback. The explicit runtime packet safety guard is detection-not-completion plus approval-bound high-risk routing. transcript/session replay stays local and deterministic; it catches missing expected behavior, forbidden shortcuts and privacy/no-secrets issues, not nuanced semantic quality.
Источники: [Codex use cases](https://developers.openai.com/codex/use-cases), [Codex workflows](https://developers.openai.com/codex/workflows), [OpenAI eval best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices), [Agent evals](https://developers.openai.com/api/docs/guides/agent-evals), [Product-Agent OS scenarios](scenarios.md).

Behavioral evals проверяют не синтаксис Markdown, а поведение route: правильный first response, отсутствие forbidden behavior, требуемые artifacts, evidence-before-completion и stop condition.

Главный шаблон сейчас: `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json`. Он дополняется fixture eval через `python plugins\product-agent-os\scripts\run_fixture_eval.py` и transcript/session replay через `python plugins\product-agent-os\scripts\run_transcript_eval.py`.

## Inputs

- scenario или methodology gate, который нужно проверить;
- user prompt или synthetic route input;
- workspace fixture, если route зависит от файлов;
- expected behavior: mode, minimum artifacts, next action, approval boundary, evidence fields;
- forbidden behavior: scaffold before approval, broad rewrite, unsupported ready claim, external mutation, missing source status;
- residual risk и reason, если кейс остается only structural.

## Outputs

- behavioral eval case с `id`, prompt/context, expected behavior, forbidden behavior и evidence requirements;
- fixture eval assertion, когда поведение можно проверить через synthetic workspace;
- failure note для `RUNLOG.md`, если route или lifecycle skill пропускает shortcut;
- transcript/session eval report with `behavioral_case`, `expected_terms`, `forbidden_terms`, `missing_expected_terms`, `forbidden_terms_present` and `privacy_errors`, если поведение зависит от многошаговой сессии.

## Eval Layers

| Layer | What it checks | Current status | Verification |
| --- | --- | --- | --- |
| Template validation | JSON shape, required fields and no placeholder behavior. | Implemented. | `tests/product_agent_os/test_behavioral_workflow_evals.py`. |
| Route and fixture eval | Synthetic workspaces return expected `usage_mode`, artifacts and expected checks. | Implemented for current scenarios and T8-GX false-positive fixtures. | `python plugins\product-agent-os\scripts\run_fixture_eval.py`. |
| Methodology intelligence eval | Read-only methodology audit returns catalog coverage, `maturity_level`, `complexity_profile`, prioritized recommendations and no target-workspace mutation. | Implemented for Track 9 foundation. | `methodology-intelligence-read-only-first` and `methodology_intelligence_contract_present`. |
| Solution architecture eval | Catalog, audit, templates and lifecycle skills preserve conditional architecture gates and reject unsupported architecture claims. | Implemented in `T9-D3`. | `solution_architecture_contract_present`. |
| Codex agentic workflow eval | Catalog, audit, templates and lifecycle skills preserve source-of-truth, approval, handoff, MCP, hook, skill, plugin, automation, model/reasoning, memory and agent eval gates without silent activation. | Implemented in `T9-D5`. | `codex_agentic_workflow_contract_present`. |
| Frontend eval | Catalog, audit, templates, lifecycle skills and fixtures preserve user-flow, component-state, Storybook/FSD, visual, accessibility, runtime, interaction and performance gates without accepting code-inspection-only UI completion. | Implemented in `T9-D6`. | `frontend_contract_present`. |
| Backend eval | Catalog, audit, templates, lifecycle skills and fixtures preserve service boundary, runtime/failure/observability/security/rollback evidence, dependency failure policy, CI/deployment discovery, severity policy and owner reviewed test/eval/runtime evidence sufficiency without accepting package-docs-only backend completion. | Implemented in `T9-D7`. | `backend_contract_present`. |
| API & Integrations eval | Catalog, audit, templates, lifecycle skills and fixtures preserve contract source, consumer, compatibility, security, error, event, SDK and external-write evidence without accepting rendered docs, OAuth-only notes or schema-only checks as completion proof. | Implemented in `T9-D8`. | `api_integrations_contract_present`. |
| Database & Data eval | Catalog, audit, templates, lifecycle skills and fixtures preserve database inventory, schema source, migration plan, expand-contract rollout, data contract, privacy, lineage, performance, retention and production approval evidence. | Implemented in `T9-D9`. | `database_data_contract_present`. |
| LLM / AI / RAG eval | Catalog, audit, templates, lifecycle skills, fixtures and transcript replay preserve AI behavior, baseline/current eval, prompt/model/tool/RAG/grounding, guardrail, trace, handoff, tooling, migration, lifecycle and incident evidence without accepting prompt-inspection-only quality claims. | Implemented through `T9-D10-M36`. | `llm_ai_rag_contract_present`. |
| Security, Privacy & Compliance eval | Catalog, audit, templates, lifecycle skills and fixtures preserve security-sensitive classification, threat surface, ASVS/SSDF/SAMM mapping, authorization negative tests, secrets, privacy, supply chain, SBOM/provenance, audit logging, Codex Security scan status and compliance overlay evidence without accepting implied scan or certification claims. | Implemented in `T9-D11`. | `security_privacy_compliance_contract_present`. |
| Delivery, Release & Operations eval | Catalog, audit, templates, lifecycle skills and fixtures preserve release scope, versioning, changelog, artifact manifest, current evidence, rollout, rollback, environments, CI/CD governance, SLO/observability, operations, incidents, post-release review, automation promotion, release mode policy, build-release-run boundary, platform distribution evidence, release communication, tooling selectors, DORA measurement design, release integrity handoff and owner-reviewed release evidence sufficiency. | Implemented through `T9-D12-M40`. | `delivery_release_operations_contract_present`. |
| Cross-domain synthesis eval | Catalog, audit, reports, lifecycle skills and fixtures preserve grouped recommendations, owner domains, consumer domains, source artifact compatibility, semantic evidence sufficiency, risk-aware safe next action and false-positive routing. | Implemented through `T9-S-M10..M14`. | `cross_domain_synthesis_contract_present`, `safe_next_action_risk_ordered`, `source_artifact_mapping_contract_present`, `cross_domain_false_positive_guards_present`. |
| Readiness contract eval | `project-readiness.json` has conditional gates, statuses, evidence owner and residual risk. | Implemented through T8-F. | `conditional_readiness_gates_contract_present`. |
| Codex compatibility eval | Plugin remains Codex-only and avoids non-Codex adapter requirements. | Implemented. | `python plugins\product-agent-os\scripts\validate_codex_compatibility.py`. |
| transcript/session eval runner | Replay synthetic or redacted Codex session transcripts for multi-turn shortcut resistance, evidence quality and privacy/no-secrets checks. | Implemented in `T8-GY` as deterministic local replay. | `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json`. |

## Expected Behavior

Each case should name the behavior that must appear, not only a file name.

Examples:

- `bug_rescue`: reproduce or isolate before fix; no fixed claim without current evidence.
- `greenfield_idea`: select direction and first vertical slice before scaffold.
- `complex_system_acceleration`: require integration catalog and ownership split before parallel work.
- `pr_review`: read-only review with stage 1 spec compliance before stage 2 quality/risk.
- `api_migration`: migration plan and contract compatibility before implementation or release.
- `ai_eval_regression`: baseline and rerun command before prompt/model/retrieval/rubric changes.
- `release_packaging`: release readiness before publish/tag/upload/package registry mutation.
- `evidence-before-completion`: ready/completed/fixed/works/release claims need current evidence or explicit inspection-only gap.
- `methodology-intelligence-read-only-first`: methodology audit must return a Delivery Map, prioritized recommendations and owner questions before any staged proposal.
- `solution_architecture_contract_present`: architecture gates require scope, boundaries, owner, ADR/tradeoff, observability, rollback, render check and accepted-gap evidence without forcing C4 detail, architecture-as-code or Well-Architected review when not applicable.
- `codex_agentic_workflow_contract_present`: Codex workflow gates require control plane, source of truth, read-only discovery, approval boundaries, model/reasoning policy, memory policy, fresh-context handoff, ownership split, subagent safety, MCP review, hook governance, skill promotion, plugin boundary, automation stability and agent eval workflow.
- `frontend_contract_present`: frontend gates require user-flow acceptance, component state matrix, design-system boundary, Storybook/FSD routing, API/data state alignment, WCAG 2.2 AA target or accepted exception, browser/runtime evidence, console status, Playwright trace or accepted gap, visual evidence, interaction checks and performance budget where applicable.
- `backend_contract_present`: backend gates require `backend-service-overview.md`, `backend-runtime-behavior.md`, runtime/failure/observability/security/rollback evidence, framework-agnostic backend policy, severity routing, CI/deployment discovery signals and owner reviewed test/eval/runtime evidence sufficiency for real project risk or an accepted gap.
- `api_integrations_contract_present`: API gates require a source-of-truth contract, consumer map, compatibility review, security schemes, error contract, contract test matrix, event/webhook delivery evidence, generated SDK manifest, observability and `approval_required` handling for external writes. Swagger UI is not source of truth, and external writes are approval_required.
- `database_data_contract_present`: Database & Data gates require `database-inventory.md`, `database-dictionary.md`, `database-migration-plan.md`, `database-data-contract.md`, rollback/backup evidence, data classification, data quality, lineage, query performance, retention/deletion, synthetic fixtures and `database-production-access-approval.md` where applicable. A schema-only artifact is not safety proof, and production access approval_required remains explicit.
- `llm_ai_rag_contract_present`: LLM / AI / RAG gates require AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, prompt contract, model decision record, structured output schema, tool/function/MCP contract, human approval boundary, RAG source inventory, retrieval config, grounding rubric, agent task packet, agent workflow trace, guardrail matrix, trace evidence packet, cost/latency budget, eval tooling selector, model migration policy, RAG lifecycle/privacy, AI incident workflow and reportable approval/gap/risk evidence. Prompt inspection is not enough, citations alone do not prove grounding, and live model calls or external eval systems remain approval_required.
- `security_privacy_compliance_contract_present`: Security, Privacy & Compliance gates require `security_sensitive_classification_present`, threat surface, security risk review, ASVS/SSDF/SAMM mapping, API security scheme, authorization negative tests, secrets policy, data classification, redaction lifecycle, privacy impact, external-write approval, abuse/rate-limit review, audit logging, supply-chain review, SBOM/provenance decision, CI permission review, AI security review, compliance overlay taxonomy, vulnerability response workflow, explicit Codex Security scan status and current evidence before completion. Docs-only security articles stay false positives; Codex Security scan is implied, OAuth proves API security and privacy compliance is universal are forbidden claims.
- `delivery_release_operations_contract_present`: Delivery, Release & Operations gates require release scope, SemVer/versioning, changelog/release notes, artifact manifest, release evidence before completion, rollout strategy, rollback/recovery, environment approval boundary, external release approval, CI/CD governance, observability/SLO, operations runbook, incident response, post-release review, `automation_manual_stability_present`, release mode policy, build-release-run boundary, platform distribution evidence, release communication, versioning tooling decision, GitHub environment controls, DORA measurement design, incident postmortem learning, observability on-call tooling, release integrity security handoff and owner-reviewed release evidence sufficiency. CI green means release ready, tests passed so release is ready, rollback is just revert, feature flags remove risk, GitOps is automatically safe, generated changelog is enough for users, DORA metrics prove individual performance, single observability tool is mandatory, release-ready without owner-reviewed evidence sufficiency and repeatable automation is automatically safe are forbidden claims.
- `cross_domain_synthesis_contract_present`: Cross-domain synthesis gates require `methodology_synthesis`, `recommendation_groups`, owner domains, consumer domains, `source_artifact_ledger`, semantic evidence sufficiency, risk-aware safe next action and source artifact alias/deferred decisions. Forbidden shortcuts include dumping every methodology gate, scaffolding before approval, detection becomes verification and generic quality strategy hides security approval.
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
- Codex workflow recommendation that treats memory as source of truth, subagents as automatically faster, MCP as safe by default, hooks as harmless, Agents SDK as the Codex runtime layer, or repeated workflows as immediately automation-ready;
- frontend completion from code inspection only, Storybook-only evidence, desktop-only screenshot, automated accessibility addon output alone, mandatory FSD claim, or lab Web Vitals as guaranteed production UX;
- API completion from Swagger UI/rendered docs, schema validation alone, OAuth-only security notes, universal GraphQL/gRPC/event defaults, or external writes without `approval_required`;
- database completion from schema-only files, ORM introspection, generated ERD/dbdocs, unapplied migration scripts, "down migration exists" rollback claims, backup-exists claims without restore evidence, unsafe production data access, destructive migration without owner approval, or treating runtime pipeline/RAG lineage as verified when it is only `present_unverified`;
- AI/RAG completion from prompt inspection, stale eval output, citations-only grounding, schema-only tool safety, automatic model-upgrade quality claims, or missing current baseline/current eval evidence;
- security/privacy/compliance completion from security review after coding, no-secrets-in-code, ASVS/OWASP name-dropping, one-time SBOM, implied Codex Security scan, OAuth-only security notes, universal privacy compliance, docs-only security article or compliance certification claim without legal/compliance owner;
- delivery/release/operations completion from CI green, local test evidence alone, generated changelog, feature flag file, GitOps file, deploy manifest or repeatable script without release evidence, artifact manifest, rollout, rollback, owner review, approval boundary and automation manual stability evidence where applicable;
- source-backed OpenAI/Codex claim without Source status or registry support;
- external write, remote CI mutation, publish, tag, upload or package-registry action without approval.

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
- T8-GX false-positive fixtures cover selected synthetic layouts; unusual real project layouts still need owner review.
- Behavioral eval cases can become too broad; keep each case focused on one shortcut or route contract.
- transcript/session eval runner is deterministic and local; it catches missing terms, forbidden shortcuts and unsafe transcript content, but it is not an LLM semantic judge.
- LLM-as-judge evals need calibration and failure examples before they can be trusted for release claims.

Next artifact: use [Scenarios](scenarios.md) to choose the route and [Codex compatibility](codex-compatibility.md) to confirm package scope.
