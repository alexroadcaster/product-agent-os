# Product-Agent OS development standards

Source status: `official + verified methodology + experiment`

Sources: [Product-Agent OS architecture](architecture.md), [Product-Agent OS scenarios](scenarios.md), [Behavioral evals](behavioral-evals.md), [Professional Code Authoring Standards](coding-standards.md), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex workflows](https://developers.openai.com/codex/workflows).

Development standards turn methodology into concrete reviewable artifacts. They define how Product-Agent OS handles product hypothesis, architecture, tests, evals, docs, security, release and post-release learning without forcing heavy ceremony onto simple work.

Red-Green-Refactor evidence is required where behavior or shared logic changes. Docs-only and inspection-only work can record an explicit gap. The no-forced-ceremony rule remains active: mechanical edits can be not_applicable, docs-light work can avoid heavy portals, backend/native work does not force FSD, simple CRUD does not force DDD, and high-risk work needs `owner_reviewed_evidence_sufficient_for_real_project_risk` or `explicit_gap_accepted`.

## Core Contract

| Standard | Required behavior | False-positive guard |
| --- | --- | --- |
| Product hypothesis | Name user/problem, acceptance scenario, metric or explicit gap. | Do not invent product outcomes from code structure alone. |
| Architecture boundary | Name scope, ownership, alternatives, decision, rollback and observability when architecture changes. | Do not force heavyweight diagrams for small mechanical edits. |
| Test/eval-first | Establish failing or baseline evidence before changing behavior. | Docs-only or formatting work can mark the gate not applicable with reason. |
| Documentation-as-code | Update source-backed docs, `Source status:` and registry when claims change. | Do not treat generated `site/` output as source of truth. |
| Review | Separate spec compliance from quality/risk review for risky changes. | Do not produce review verdicts without reading changed files. |
| Release measurement | Record build/test/docs evidence, rollout, rollback, owner review and accepted gaps before release claims. | CI green alone is not release readiness. |

## Artifact Templates

These templates convert recommendations into concrete outputs that can be reviewed, tested and accepted or rejected:

| Template | Purpose |
| --- | --- |
| `.codex/artifact-templates/adr.md` | Architecture decision record with context, decision, consequences, verification and rollback. |
| `.codex/artifact-templates/architecture-overview.md` | System boundary, runtime, dependencies, observability and operational risk. |
| `.codex/artifact-templates/domain-modeling.md` | Domain terms, bounded contexts, ubiquitous language and business rules when complexity warrants it. |
| `.codex/artifact-templates/metric-spec.md` | Product behavior metric, event source, owner, privacy and interpretation caveats. |
| `.codex/artifact-templates/api-contract-review.md` | API source-of-truth, consumers, compatibility, error model, security and rollout. |
| `.codex/artifact-templates/component-card.md` | UI component purpose, states, accessibility, visual evidence and interaction checks. |
| `.codex/artifact-templates/database-dictionary.md` | Table meaning, sensitive fields, retention, migration history and schema verification. |
| `.codex/artifact-templates/docs-tooling-decision.md` | Docs tooling selection, rejected tools, owner, command evidence and approval requirements. |
| `.codex/artifact-templates/governance-proposal.md` | Staged governance proposal for CODEOWNERS status and GitHub Actions least privilege without external activation. |
| `.codex/workflows/coding-standards.md` | Professional code authoring workflow for non-mechanical code work: leverage existing capabilities before custom code. |
| `.codex/artifact-templates/coding-standard-checklist.md` | Evidence checklist for `enterprise_leverage_check`, `one_line_candidate`, dependency decisions, deep-module checks and legacy seams. |

## Discovery Signals

`workspace-discovery-auditor` can identify methodology signals without claiming readiness:

- architecture docs, ADRs, C4/arc42-style files and runtime diagrams;
- OpenAPI, AsyncAPI, GraphQL schema, SDK generation or webhook/event contracts;
- Storybook, component libraries and optional FSD structure;
- database docs, migrations, DBML/SQL, retention and backup/restore evidence;
- CODEOWNERS, CI, release manifests, changelog and versioning files;
- eval configs, datasets, prompt/model artifacts, traces and RAG source inventories;
- security/privacy docs, secrets policies, SBOM/provenance, audit logging and compliance overlays;
- metrics dashboards, product event specs and post-release learning notes.

Signals create `present_unverified`. Verified readiness needs current command evidence, owner evidence, runtime/eval proof or accepted gap.

Detection alone remains `present_unverified`, and grouped methodology recommendations need source artifact compatibility, owner domains, consumer domains and approval-bound behavior before they become implementation work.

## Planning And Handoff Standards

Before build or review, Product-Agent OS expects:

- exact files owned and forbidden;
- exact commands and expected outputs;
- source constraints and approval boundary;
- rollback or disable path where relevant;
- expected evidence and stop conditions;
- fresh-context handoff when subagents or parallel workers are used;
- placeholder scan or explicit reason it is not applicable;
- spec-compliance review before quality/risk review for risky public-contract, migration, security, data, release or parallel work.

Subagents are useful only when ownership is clear. A handoff without source context, files, expected evidence and stop condition is not enough.

## Professional Code Authoring

For non-mechanical code work, Product-Agent OS expects the coding-standard workflow and checklist to be loaded before edits. The default ladder is: delete unnecessary code, configure existing behavior, use standard library or platform capability, use framework API, use an existing dependency, use a project helper, then add a tiny adapter or custom code only when the earlier options are insufficient.

The checklist records `enterprise_leverage_check`, `existing_capability_scan`, `one_line_candidate`, selected leverage path, rejected alternatives, `negative_dependency_rule`, `deep_module_check`, `legacy_seam_check`, `cleverness_budget`, test/eval evidence and unsupported code-quality claims. Mechanical, docs-only or generated-file sync work can mark the gate `not_applicable` with a reason.

Template availability is not runtime enforcement. These artifacts do not activate hooks, automation, subagents, HTML reporting or plugin-cache behavior by themselves; they give agents a compact source-of-truth contract when the workflow, skill or role profile is explicitly loaded.

## Domain-Specific Gates

| Domain | Gate |
| --- | --- |
| Frontend | User-flow acceptance, component states, design-system boundary, accessibility target or accepted exception, browser/runtime evidence, visual evidence and performance budget when applicable. |
| Backend | Runtime behavior, failure modes, observability, security, rollback, CI/deployment discovery and owner-reviewed evidence sufficiency. |
| API & Integrations | Source-of-truth contract, consumer map, compatibility, security, error model, events/webhooks, SDK generation and external-write approval. |
| Database & Data | Inventory, dictionary, migration plan, expand-contract rollout, data classification, quality, lineage, performance, retention and production access boundary. |
| LLM / AI / RAG | Baseline/current eval, prompt/model/tool/RAG contracts, grounding, trace evidence, guardrails, cost/latency, migration policy and AI incident path. |
| Security, Privacy & Compliance | Threat surface, risk review, ASVS/SSDF/SAMM mapping, authorization negative tests, secrets, privacy, supply chain, audit logging, scan status and compliance overlay. |
| Delivery, Release & Operations | Release scope, versioning, changelog, artifact manifest, rollout, rollback, CI/CD governance, SLO/observability, operations runbook, incident path, post-release review and release integrity handoff. |
| Cross-domain synthesis | Grouped recommendations, owner domains, consumer domains, source artifact compatibility, semantic evidence sufficiency and risk-aware safe next action. |

Exact gate identifiers:

- `llm_ai_rag_readiness_when_ai_behavior_changes`: AI/RAG behavior changes record `llm_ai_rag` evidence before quality claims.
- `security_privacy_compliance_when_sensitive_surface`: Security/Privacy/Compliance-sensitive slices record `security_privacy_compliance` evidence before completion claims.
- `delivery_release_operations_readiness_when_release_or_operations_changes`: Delivery/Release/Operations slices record `delivery_release_operations` evidence before release, deploy, publish, operational-ready or automation-ready claims.
- `automation_manual_stability_present` and `release_evidence_sufficiency_owner_reviewed` are required when automation or release readiness claims depend on operational evidence.
- False-positive guard: DORA metrics prove individual performance is not an acceptable release/operations claim.

## Documentation Standard

Every non-index documentation page needs `Source status:`. Source-backed claims must link to official or project-authored sources and update `docs/sources/registry.md` when claims are added or changed.

Use this rule of thumb:

- official OpenAI/Codex behavior needs official docs as source of truth;
- project package behavior can cite repository artifacts, tests and source packets;
- community claims stay under `docs/insights/` with trust and verification labels;
- generated HTML, dashboards, memory and chat recall are not source of truth;
- secrets, tokens, private keys, credentials, customer data and raw private chats are not allowed in docs, prompts, memory, examples, fixtures or templates.

## Release And Operations Standard

Release, deploy, publish, package and operations-ready claims require current evidence:

- release scope and versioning;
- changelog or release notes;
- artifact manifest;
- build/test/docs/eval evidence;
- rollout and rollback/recovery;
- environment approval boundary;
- observability/SLO and operations runbook;
- incident response and post-release review;
- owner-reviewed evidence sufficiency or accepted gap.

Automation candidates also need manual success evidence, stable inputs/outputs, owner, cadence, verification, failure modes, value evidence and rollback/disable path. Product-Agent OS can stage a candidate; it must not create active automation without explicit approval.

## Verification

Run focused checks after changing docs standards:

```powershell
python tools\check_docs.py
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
```

Run broader checks after templates, lifecycle skills or fixture behavior change:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
```

Use strict MkDocs when documentation navigation, Mermaid or site-generation behavior changes.

## Important Limits

- Standards are evidence gates, not automatic work expansion.
- Detection alone does not prove readiness.
- Owner approval is required for external writes, publishing, production data, live provider calls, hosted docs, CI activation, security scans and active automation.
- High-risk work needs explicit owner-reviewed evidence sufficiency or accepted gap.
- Product-Agent OS must preserve staged-first behavior, source policy, sandbox and approvals even when a recommendation is confident.

Next artifact: use [Methodology intelligence](methodology-intelligence.md) to decide which gates apply, [Professional Code Authoring Standards](coding-standards.md) to inspect code-writing gates and [Behavioral evals](behavioral-evals.md) to check shortcut resistance.

## Inputs

- Product scope, source evidence, risk classification and methodology signals.
- Current checks, evals, owner decisions and accepted gaps.

## Outputs

- Proportional engineering gates for requirements, architecture, testing, release and operations.
- Evidence expectations that can be reviewed without forcing irrelevant ceremony.

## Risks

- Treating standards as automatic work expansion can slow low-risk changes.
- Detection alone does not prove that the chosen gate is semantically sufficient.
