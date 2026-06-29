# Product-Agent OS scenarios

Source status: `official + experiment`

Sources: [Codex workflows](https://developers.openai.com/codex/workflows), [Codex use cases](https://developers.openai.com/codex/use-cases), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Product-Agent OS plugin](index.md), [Behavioral evals](behavioral-evals.md), [Codex compatibility](codex-compatibility.md).

This page answers a practical question: which route should the Product-Agent OS plugin choose when Codex App, CLI or IDE extension sees a real workspace and the user asks for a verifiable outcome, not just "write code".

A scenario does not replace the lifecycle. It chooses the first small step, minimum artifacts, approval boundary and verification gates. If evidence is missing, the route must return a gap, not readiness.

## Operator Route Map

Scenarios are route decisions, not permission to run live systems. Each route must name source context, expected evidence, approval boundary and stop condition before it hands work to a subagent, skill or implementation slice.

| Route | When to choose | Minimum evidence | Stop condition |
| --- | --- | --- | --- |
| `code_graph_orientation` | Need to understand code/docs topology before build or review. | Existing source files plus generated graph/cockpit packet labeled as orientation evidence. | Do not claim source truth from generated graph; read source before implementation claims. |
| `live_runtime_read_only` | Need to check local runtime contract or graph-only API fallback. | Governance packet and disabled runtime contract. | Stop before live server launch unless separate approval packet exists. |
| `provider_retrieval_eval` | Need to evaluate embedding/reranker/LLM provider benefit. | Redaction, cache, budget, baseline and threshold fallback packet. | Stop before any provider/live external model/API call without explicit approval. |
| `canonical_graph_mutation_review` | Need to check proposal acceptance and mutation readiness. | Human review ledger, proposal diff, mutation dry-run plan and rollback proof. | Stop before canonical graph mutation unless owner accepted the proposal and rollback evidence is current. |
| `real_testing_approval` | Need to move from staged evidence to controlled real testing. | Target/data owner approval, runtime/browser/provider/mutation/git action packet and rollback plan. | Stop unless the specific action is approved; approvals are not bundled. |

## G4 Operator Flows

G4 adds four system routes. They do not approve cache refresh, global config writes, live runtime, browser automation, provider/API calls, target mutation, git, release or automation.

| Route | When to use | Evidence boundary |
| --- | --- | --- |
| `instruction_tool_use_compliance` | Check when a Product-Agent OS skill/plugin route may be selected implicitly and when it needs an explicit user request. | Uses official Codex docs, `allow_implicit_invocation`, `explicit_only`, `narrow_implicit` and `blocked_implicit`; fresh-session proof remains separate. |
| `operator_command_matrix` | Choose a safe command for first-run analysis, graph/cockpit or docs-tooling smoke. | Uses help/current command evidence, stages only generated artifacts, and keeps broad scans/root `site` rebuild approval-bound. |
| `guided_question_answer_ledger` | Ask a question without turning intake into a long questionnaire. | Enforces one blocking question maximum; `answers_require_staged_ledger_and_owner_review` before source promotion. |
| `source_cache_session_state` | Understand why source, installed cache and active session can diverge. | Requires read-only comparison fields and fresh-session proof before any fixed/ready claim. |
| `professional_code_authoring` | Limit custom code, dependency debt, shallow wrappers or risky refactor in a non-mechanical coding task. | Uses [Professional Code Authoring Standards](coding-standards.md), checklist evidence and shortcut evals; remains a source contract until runtime/owner-pilot proof exists. |

## Inputs

- user goal or `intent_hint`, if passed to the Codex runtime runner;
- read-only workspace audit: files, stack, test/build commands, docs, CI, contracts and control-plane files;
- current `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- source policy, sandbox, approvals and known external-system boundaries;
- previous failure notes, if already recorded in `RUNLOG.md`.

Key routing fields include `finish_options` and `safe_next_action`; they tell the next worker whether to answer, stage a proposal, request approval, run focused verification or stop on an evidence gap.

## Outputs

- `usage_mode.primary`, secondary mode, confidence and routing reasons;
- first response: one closest useful step without broad scaffold, rewrite or external mutation;
- minimum artifacts: concrete files or packets needed before build/review/release;
- approval boundary: what is read-only, staged-only or approval-required;
- verification gates: commands, evals, screenshots, logs, owner review or accepted gap;
- residual risk when route is based on detection rather than verified evidence.

## Guided Question Protocol And Status Dashboard

Guided question protocol uses typed `question_queue` packets so the first response can show only `next_blocking_question`, `question_counts` and `question_summary`. It asks at most one blocking question, keeps recommended and optional questions in the packet, and routes answers into artifacts or accepted gaps.

The status snapshot is the JSON source for a generated dashboard view. The dashboard stages `.codex/product-agent-os/status.html` and `.codex/product-agent-os/status.json` through the existing approval flow. `status.html` is a generated view only; underlying artifacts remain the source material.

## Self-Verification And Modernization Loop

The `agent_skill_metrics_loop` route reviews agents, skills, prompt/policy packs, router/tool policy and harness-version behavior. It starts from a read-only target registry, explicit run evidence, trace intake, dataset quality checks, local grader summaries and grader/judge calibration. It can stage scorecard ledger records, daily or weekly packets, `agent-skill-evaluation-report.html` and modernization candidates, but every output is staged evidence only.

## Project Code Graph And Cockpit

The graph route provides a read-only project graph foundation and generated cockpit for route orientation. It can produce staged graph JSON/JSONL with file-level nodes, overlays, conservative dependency edges, controlled schema validation, manifest freshness, observation lineage, partition scopes and aliases.

The cockpit renderer can stage offline `.codex/product-agent-os/project-cockpit.html` and `.codex/product-agent-os/project-cockpit.json` review surfaces with top-level pages, Code Flow, static projection, local vendor boundary, graph filters, selected-node evidence, fallback tables, mobile layout and no external assets.

Generated graph artifacts, runtime graph summaries, analysis reports and HTML cockpit views are review evidence only. The scanner and renderer do not mutate target workspaces.

## G5 Evidence-Quality Routes

Use these routes when the question is not about new plugin behavior, but about the quality and boundaries of generated evidence.

| route_id | When it applies | Minimum result | Boundary |
| --- | --- | --- | --- |
| `generated_artifact_ux_criteria` | HTML/report output looks too diagnostic or is being prepared for owner review. | Quality checklist, claim ceilings, Vale advisory status, Storybook trigger status. | Browser proof and Storybook install remain `approval_required`. |
| `graph_intelligence_contract` | Graph packets, ontology, rejected links, freshness or query packets are used. | Orientation summary, stale/rejected-link handling, source-read-before-edit reminder. | Graph packets do not replace source reads or authorize mutation. |
| `privacy_supply_chain_retention` | Cache/session evidence, SBOM, vulnerability audit, remediation or raw reports are discussed. | Redaction and retention boundary, approval gates, unsupported claims. | Broad scans, remediation and raw report retention require separate approval. |
| `local_html_interaction_boundary` | Generated HTML includes tabs, search, filters or diagrams. | Local-only interaction rules, no-network policy, fallback and browser-proof packet fields. | Static checks are not browser proof. |
| `residual_follow_up_site_freshness` | G1.1 residuals or final `DOC-M25` need closure. | Residual routing table, private-target redaction policy, site freshness gate. | Root `site`, search and sitemap are current after `documentation_refresh_DOC-M25-A01`; browser proof remains separate. |

## Scenario Matrix

| usage_mode | When it applies | first response | minimum artifacts | approval boundary | verification gates |
| --- | --- | --- | --- | --- | --- |
| `first-run-intake` | Empty workspace, broken verification, existing control-plane or complex first launch. | Name mode, confidence, next smallest action and evidence gaps. | Intake summary, lifecycle state, next action. | No scaffold, broad fix or parallel work before route is accepted. | Read-only audit, control-plane check, source policy. |
| `bug_rescue` | User reports broken behavior, failing tests or regression. | Reproduce or isolate before changing code. | `bug-rescue-report.md`, failure evidence, root-cause hypothesis. | No fix claim without reproduction evidence. | Failing command/log, focused regression check, current evidence. |
| `greenfield_idea` | Idea-stage or empty product direction. | Shape one vertical slice before scaffold. | `greenfield-idea-brief.md`, selected direction, non-goals. | Scaffold requires explicit approval. | Acceptance scenarios, first slice plan, lightweight-mode decision. |
| `complex_system_acceleration` | Existing multi-surface app, integrations, multiple services or unclear ownership. | Build map before parallelization. | `integration-catalog.md`, ownership split, release gates. | No parallel work with overlapping files or unclear external-system owners. | Integration inventory, ownership review, release risk gates. |
| `pr_review` | Review or merge-readiness request. | Stay read-only and review changed files. | PR review readiness, changed-files map, `pr-risk-review.md`. | No push, PR creation, merge or external comment without approval. | Two-stage review: spec compliance before quality/risk. |
| `legacy_onboarding` | Old, undocumented or unknown repository. | Orient before refactor. | `onboarding-map.md`, entry points, run commands, docs debt. | No cleanup/refactor until map and verification status are explicit. | Present-unverified labels, source map, run command evidence. |
| `api_migration` | HTTP API, event contract, generated client or consumer change. | Plan compatibility before implementation. | `migration-plan.md`, `api-contract-review.md`, consumers, rollout. | Release or breaking change needs owner review and approval. | Contract check, backward compatibility, deprecation and rollout evidence. |
| `ai_eval_regression` | AI/RAG quality, prompt, model, retrieval, dataset or judge changes. | Baseline first. | `ai-eval-spec.md`, dataset policy, rubric, thresholds. | No quality claim from inspection-only evidence. | Baseline, rerun command, latency/cost/grounding and failure examples. |
| `native_mobile_feature` | iOS, Android or native mobile behavior. | Record platform assumptions before implementation. | Platform runtime check, permissions, offline/device plan. | Permission, signing or store changes require approval. | Build command, simulator/emulator or device logs, screenshots, manual gap. |
| `desktop_local_first` | Desktop app, filesystem, local DB, indexing or packaging. | Map local data and OS assumptions first. | Local data risk note, runtime log check, recovery path. | Filesystem access, packaging, signing and distribution require approval. | App logs, build/run command, privacy and rollback evidence. |
| `data_migration` | Schema, backfill, sensitive data, retention or production data risk. | Plan migration and rollback before execution. | `migration-plan.md`, `database-dictionary.md`, data quality checks. | Production DB/data access and migration execution require approval. | Dry run, backup, validation, owner review, rollback evidence. |
| `security_sensitive_change` | Authn/authz, payment, billing, secrets, PII, abuse controls or permissions. | Threat surface and owner review before build. | `security-risk-review.md`, approval boundary, rollback plan. | Security scans or external security mutations only when explicitly requested. | Tests, audit logging, rate limit, privacy and owner review evidence. |
| `ci_stabilization` | Failing, flaky or unstable CI. | Gather failure evidence before changing code. | `ci-stabilization-report.md`, failing job, local reproduction. | Remote CI reruns, settings and branch rules require approval. | Logs, deterministic/flaky classification, isolation plan, rerun evidence. |
| `release_packaging` | Package, SDK, plugin, app, mobile, desktop or open-source release. | Build release readiness before publish. | `release-readiness.md`, package metadata, changelog, artifacts. | Publishing, tagging, release creation, upload or package registry mutation require approval. | Build/test/docs evidence, security/license notes, rollback and owner review. |
| `docs_only` | Documentation update without behavior change. | Update source-backed docs and run docs checks. | Source status, affected docs, registry entry when source-backed claims changed. | Hosted docs, CI activation and sharing changes require approval. | `python tools\check_docs.py`, strict MkDocs when nav/build-sensitive. |
| `standard_feature` | Bounded feature work without special scenario risk. | Use normal lifecycle route. | Requirements, plan, test/eval evidence. | Writes follow sandbox and project approval policy. | Unit/integration/contract checks, docs impact, review. |
| `professional_code_authoring` | Non-mechanical code work where the smallest safe implementation matters. | Check reuse before custom code. | Coding-standard checklist, existing-capability scan, one-line/native candidate, dependency and legacy-seam decisions. | No hook/runtime/automation activation from route selection. | Focused tests/evals/review evidence plus unsupported-claim ledger. |
| `maintenance` | Small upkeep, formatting or status sync. | Keep scope mechanical and evidence explicit. | RUNLOG note or control-plane sync. | No unrelated refactor. | Focused command or explicit inspection-only gap. |

## Database & Data Methodology Routing

Database/data work keeps `data_migration` as the route name and adds a dedicated Database & Data methodology packet when schema, migration, ORM, warehouse, data quality, lineage, retention, backup/restore or production-data signals appear. Production data access, DB introspection, migration execution, destructive cleanup, backup restore and retention mutation are approval-required.

## Backend Methodology Routing

Backend methodology routing applies when service behavior, background jobs, queues, auth, error handling, observability, deployment or rollback behavior changes. Minimum staged artifacts include `backend-service-overview.md`, `backend-runtime-behavior.md`, runtime/failure evidence, observability evidence, security evidence and rollback evidence.

## LLM / AI / RAG Methodology Routing

AI/RAG work keeps `ai_eval_regression` as the route name and adds a dedicated LLM / AI / RAG methodology packet when prompts, models, eval configs, structured outputs, tool/function/MCP calls, RAG corpora, retrieval, vector stores, embeddings, grounding, agent traces, guardrails or latency/cost signals appear. Live model calls, external eval services, vector DB access, raw prompts/traces/customer text, tool writes, shell/money/data exposure and irreversible side effects are approval-required.

## API & Integrations Methodology Routing

API & Integrations methodology routing applies when HTTP APIs, event contracts, webhooks, generated SDKs or external providers change. Minimum staged artifacts include `api-inventory.md`, `api-contract-review.md`, `api-consumer-map.md`, `api-contract-test-matrix.md`, `external-integration-approval.md` and compatibility/security/error/event/SDK evidence.

External writes are not automatic actions; they require an explicit approval boundary.

## Security, Privacy & Compliance Methodology Routing

Security-sensitive work keeps `security_sensitive_change` as the route name and adds a dedicated Security, Privacy & Compliance methodology packet when authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data, policy changes or compliance overlays appear.

Approval boundary stays explicit: payment/billing, production data, secret rotation, policy changes, external security-system mutations, external writes, publish actions and Codex Security scans are not automatic actions.

## Delivery, Release & Operations Methodology Routing

Release packaging keeps `release_packaging` as the route name and adds a dedicated Delivery, Release & Operations methodology packet when release, deploy, publish, package, versioning, changelog, artifact, rollout, rollback, CI/CD environment, release mode policy, platform distribution evidence, release communication, SLO/observability, runbook, incident, postmortem, release integrity or automation promotion signals appear.

Approval boundary stays explicit: publish, tag, release creation, artifact upload, deploy, package registry mutation, marketplace/store submission, CI/CD environment changes and active automation are not automatic actions.

## Verification

Run route and fixture checks after scenario behavior changes:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
python tools\check_docs.py
```

Run broader checks after lifecycle skills, templates or route logic change:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
```

## Risks

- A route can be plausible but wrong when workspace evidence is stale.
- Scenario detection can force heavy process onto simple work unless false-positive guards remain active.
- Generated dashboards and graphs can look authoritative; source-boundary labels must remain visible.
- Approval for one surface must not imply approval for another.

Next artifact: use [Behavioral evals](behavioral-evals.md) to test route behavior, [Development standards](development-standards.md) to select evidence gates and [Professional Code Authoring Standards](coding-standards.md) to inspect code-writing gates.
