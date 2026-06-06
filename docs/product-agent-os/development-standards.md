# Product-Agent OS development standards

Source status: `official + verified methodology + experiment`

Источники: [Product-Agent OS architecture](architecture.md), [Product-Agent OS scenarios](scenarios.md), [Behavioral evals](behavioral-evals.md), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex workflows](https://developers.openai.com/codex/workflows).

Development standards turn methodology в concrete reviewable artifacts. Они define how Product-Agent OS handles product hypothesis, architecture, tests, evals, docs, security, release и post-release learning без forcing heavy ceremony onto simple work.

Red-Green-Refactor evidence является required где behavior или shared logic changes. Docs-only и inspection-only work может record explicit gap. Этот no-forced-ceremony rule остается active: mechanical edits может быть not_applicable, docs-light work может avoid heavy portals, backend/native work не force FSD, simple CRUD не force DDD, и high-risk work требует `owner_reviewed_evidence_sufficient_for_real_project_risk` или `explicit_gap_accepted`.

## Core Contract

| Standard | Required behavior | False-positive guard |
| --- | --- | --- |
| Product hypothesis | Name user/problem, acceptance scenario, metric или explicit gap. | Не invent product outcomes из code structure alone. |
| Architecture boundary | Name scope, ownership, alternatives, decision, rollback и observability когда architecture changes. | Не force heavyweight diagrams для small mechanical edits. |
| Test/eval-first | Establish failing или baseline evidence до changing behavior. | Docs-only или formatting work может mark gate не applicable с reason. |
| Documentation-as-code | Update source-backed docs, `Source status:` и registry когда claims change. | Не treat generated `site/` output как канонический источник. |
| Review | Separate spec compliance из quality/risk review для risky changes. | Не produce review verdicts без reading changed files. |
| Release measurement | Record build/test/docs evidence, rollout, rollback, owner review и accepted gaps до release claims. | CI green alone является не release readiness. |

## Artifact Templates

These templates convert recommendations в concrete outputs который может быть reviewed, tested и accepted или rejected:

| Template | Purpose |
| --- | --- |
| `.codex/artifact-templates/adr.md` | Architecture decision record с context, decision, consequences, verification и rollback. |
| `.codex/artifact-templates/architecture-overview.md` | System boundary, runtime, dependencies, observability и operational risk. |
| `.codex/artifact-templates/domain-modeling.md` | Domain terms, bounded contexts, ubiquitous language и business rules когда complexity warrants it. |
| `.codex/artifact-templates/metric-spec.md` | Product behavior metric, event source, owner, privacy и interpretation caveats. |
| `.codex/artifact-templates/api-contract-review.md` | API source-of-truth, consumers, compatibility, error model, security и rollout. |
| `.codex/artifact-templates/component-card.md` | UI component purpose, states, accessibility, visual evidence и interaction checks. |
| `.codex/artifact-templates/database-dictionary.md` | Table meaning, sensitive fields, retention, migration history и schema verification. |
| `.codex/artifact-templates/docs-tooling-decision.md` | Docs tooling selection, rejected tools, owner, command evidence и approval requirements. |
| `.codex/artifact-templates/governance-proposal.md` | Staged governance proposal для CODEOWNERS status и GitHub Actions least privilege без external activation. |

## Discovery Signals

`workspace-discovery-auditor` может identify methodology signals без claiming readiness:

- architecture docs, ADRs, C4/arc42-style files и runtime diagrams;
- OpenAPI, AsyncAPI, GraphQL schema, SDK generation или webhook/event contracts;
- Storybook, component libraries и optional FSD structure;
- database docs, migrations, DBML/SQL, retention и backup/restore evidence;
- CODEOWNERS, CI, release manifests, changelog и versioning files;
- eval configs, datasets, prompt/model artifacts, traces и RAG source inventories;
- security/privacy docs, secrets policies, SBOM/provenance, audit logging и compliance overlays;
- metrics dashboards, product event specs и post-release learning notes.

Signals create `present_unverified`. Verified readiness требует текущий command evidence, owner evidence, runtime/eval proof или accepted gap.

Detection alone остается `present_unverified`; detection alone остается `present_unverified`, и grouped methodology recommendations нужны source artifact compatibility, owner domains, consumer domains и approval-bound behavior до they become implementation work.

## Planning And Handoff Standards

Before build или review, Product-Agent OS expects:

- exact files owned и forbidden;
- exact commands и expected outputs;
- source constraints и approval boundary;
- rollback или disable path где relevant;
- ожидаемые доказательства и stop conditions;
- fresh-context handoff когда subagents или parallel workers являются used;
- placeholder scan или explicit reason это является не applicable;
- spec-compliance review до quality/risk review для risky public-contract, migration, security, data, release или parallel work.

Subagents являются useful только когда ownership является clear. A handoff без source context, files, ожидаемые доказательства и stop condition является не enough.

## Domain-Specific Gates

| Domain | Gate |
| --- | --- |
| Frontend | User-flow acceptance, component states, design-system boundary, accessibility target или accepted exception, browser/runtime evidence, visual evidence и performance budget когда applicable. |
| Backend | Runtime behavior, failure modes, observability, security, rollback, CI/deployment discovery и owner-reviewed evidence sufficiency. |
| API & Integrations | Source-of-truth contract, consumer map, compatibility, security, error model, events/webhooks, SDK generation и external-write approval. |
| Database & Data | Inventory, dictionary, migration plan, expand-contract rollout, data classification, quality, lineage, performance, retention и production access boundary. |
| LLM / AI / RAG | Baseline/current eval, prompt/model/tool/RAG contracts, grounding, trace evidence, guardrails, cost/latency, migration policy и AI incident path. |
| Security, Privacy & Compliance | Threat surface, risk review, ASVS/SSDF/SAMM mapping, authorization negative tests, secrets, privacy, supply chain, audit logging, scan status и compliance overlay. |
| Delivery, Release & Operations | Release scope, versioning, changelog, artifact manifest, rollout, rollback, CI/CD governance, SLO/observability, operations runbook, incident path, post-release review и release integrity handoff. |
| Cross-domain synthesis | Grouped recommendations, owner domains, consumer domains, source artifact compatibility, semantic evidence sufficiency и risk-aware safe следующий action. |

Exact gate identifiers:

- `llm_ai_rag_readiness_when_ai_behavior_changes`: AI/RAG behavior changes record `llm_ai_rag` evidence до quality claims.
- `security_privacy_compliance_when_sensitive_surface`: Security/Privacy/Compliance-sensitive slices record `security_privacy_compliance` evidence до completion claims.
- `delivery_release_operations_readiness_when_release_or_operations_changes`: Delivery/Release/Operations slices record `delivery_release_operations` evidence до release, deploy, publish, operational-ready или automation-ready claims.
- `automation_manual_stability_present` и `release_evidence_sufficiency_owner_reviewed` являются required когда automation или release readiness claims depend на operational evidence.
- False-positive guard: DORA metrics prove individual performance является не acceptable release/operations claim.

## Documentation Standard

Every non-index documentation page требует `Source status:`. Source-backed claims должен link к official или project-authored sources и update `docs/sources/registry.md` когда claims являются added или changed.

Используйте эта rule из thumb:

- official OpenAI/Codex behavior требует official docs как канонический источник;
- project package behavior может cite repository artifacts, tests и source packets;
- community claims stay в рамках `docs/insights/` с trust и verification labels;
- generated HTML, dashboards, memory и chat recall являются не является каноническим источником;
- secrets, tokens, private keys, credentials, customer data и raw private chats являются не allowed в docs, prompts, memory, examples, fixtures или templates.

## Release And Operations Standard

Release, deploy, publish, package и operations-ready claims требуют текущий evidence:

- release scope и versioning;
- changelog или заметки к release;
- artifact manifest;
- build/test/docs/eval evidence;
- rollout и rollback/recovery;
- environment approval boundary;
- observability/SLO и operations runbook;
- incident response и post-release review;
- owner-reviewed evidence sufficiency или accepted gap.

Automation candidates also нужны manual success evidence, stable inputs/outputs, owner, cadence, verification, failure modes, value evidence и rollback/disable path. Product-Agent OS может stage candidate; это должен не create active automation без explicit approval.

## Проверка

Запустите focused checks после changing docs standards:

```powershell
python tools\check_docs.py
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
```

Запустите broader checks после templates, lifecycle skills или fixture behavior change:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
```

Используйте strict MkDocs когда documentation navigation, Mermaid или site-generation behavior changes.

## Important Limits

- Standards являются evidence gates, не automatic work expansion.
- Detection alone не prove readiness.
- Owner approval является required для external writes, publishing, production data, live provider calls, hosted docs, CI activation, security scans и active automation.
- High-risk work требует explicit owner-reviewed evidence sufficiency или accepted gap.
- Product-Agent OS должен preserve staged-first behavior, политика источников, sandbox и approvals even когда recommendation является confident.

Следующий artifact: используйте [Methodology intelligence](methodology-intelligence.md) к decide который gates apply и [Behavioral evals](behavioral-evals.md) к check shortcut resistance.
