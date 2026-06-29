# Product-Agent OS artifact contracts

Source status: `official + experiment`

This page lists the main generated Product-Agent OS artifacts for the modernization loop, project code graph, live/runtime governance and approval-bound handoff. It is not a JSON Schema spec; it is an operator-facing contract map: what gets created, why it exists, where the source-of-truth boundary sits and which approval gates apply.

## Contract Boundary

Generated artifacts are staged evidence only. They are not source of truth unless a later owner-approved process explicitly promotes a fact back into checked-in source documentation or another canonical artifact.

Source of truth remains:

- project source files and checked-in contracts;
- `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- source registry entries with current verification status;
- command evidence from the current run;
- owner decisions and accepted gaps with residual risk.

Artifacts must not contain secrets, credentials, raw private chat logs, private customer data, unredacted PII, raw source bodies where a redacted packet is required, or absolute local paths.

## Project Code Graph Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph.json` | `project_code_graph.py`, `scan_project_code_graph.py --stage` | Main graph packet with metadata, nodes, edges, observations, freshness and provenance. | Orientation evidence only; source files remain canonical. |
| `.codex/product-agent-os/project-code-graph.jsonl` | `scan_project_code_graph.py --stage` | Bounded JSONL form for agent consumption. | No raw source body claim; use source reads before implementation claims. |
| `.codex/product-agent-os/project-cockpit.html` | `project_graph_renderer.py` | Offline generated cockpit view. | Generated view only; visual completeness does not prove source correctness. |
| `.codex/product-agent-os/project-cockpit.json` | `project_graph_renderer.py` | Structured cockpit model, pages and projection data. | Review surface only. |
| `.codex/product-agent-os/project-code-graph-search-index.json` | `project_graph_index.py`, `--build-index` | Offline static search index with cache/fingerprint checks. | Generated cache; delete for rollback. |
| `.codex/product-agent-os/project-code-graph-backend.json` | `project_graph_backend.py`, `--build-backend` | Disabled-by-default local query backend file-store. | Not an active production server; graph-only fallback must remain. |
| `.codex/product-agent-os/project-code-graph-semantic-index.json` | `project_graph_semantic.py`, `--build-semantic-index` | Local deterministic semantic retrieval cache. | Semantic hits are `present_unverified`; no canonical edge rewrites. |
| `.codex/product-agent-os/project-code-graph-llm-proposals.json` | `project_graph_llm_extraction.py`, `--build-llm-proposals` | Local deterministic semantic node/edge and rationale/comment proposals. | Proposal-only; never canonical graph fact. |
| `.codex/product-agent-os/project-code-graph-extension-closure.json` | `project_graph_extension_closure.py`, `--verify-extensions` | Extension verification, rollback/data deletion proof and graph-only fallback report. | Closure evidence only. |

## Live Governance And Runtime Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-live-governance.json` | `project_graph_live_governance.py`, `--validate-live-governance` | Approval, data classification, redaction, credential, cache and budget packet. | No live calls; validates gate only. |
| `.codex/product-agent-os/project-code-graph-live-cache.json` | `project_graph_live_governance.py` | Cache policy/deletion metadata. | Cache is generated evidence, not source truth. |
| `.codex/product-agent-os/project-code-graph-live-runtime.json` | `project_graph_live_runtime.py`, `--validate-live-runtime` | Local read-only runtime contract. | `disabled_by_default_not_started`; no launch in docs slices. |
| `.codex/product-agent-os/project-code-graph-live-runtime.pid` | `project_graph_live_runtime.py` | Runtime lifecycle placeholder/evidence path. | Only meaningful after approved runtime execution. |
| `.codex/product-agent-os/project-code-graph-live-runtime.log` | `project_graph_live_runtime.py` | Runtime log path/evidence path. | Must be redacted and local-only. |

## Provider And Retrieval Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-embedding-provider.json` | `project_graph_embedding_provider.py`, `--validate-embedding-provider` | Embedding provider gate and eval baseline. | Provider call remains blocked unless separately approved. |
| `.codex/product-agent-os/project-code-graph-embedding-provider-cache.json` | `project_graph_embedding_provider.py` | Provider cache metadata. | Must preserve redaction/cache/budget policy. |
| `.codex/product-agent-os/project-code-graph-reranker-provider.json` | `project_graph_reranker_provider.py`, `--validate-reranker-provider` | Reranker provider gate. | No external reranker call by default. |
| `.codex/product-agent-os/project-code-graph-reranker-provider-cache.json` | `project_graph_reranker_provider.py` | Reranker cache metadata. | Generated cache only. |
| `.codex/product-agent-os/project-code-graph-hybrid-retrieval.json` | `project_graph_hybrid_retrieval.py`, `--build-hybrid-retrieval` | Explainable fusion of graph/static/semantic/reranker signals. | No canonical mutation; fallback remains available. |
| `.codex/product-agent-os/project-code-graph-llm-proposal-provider.json` | `project_graph_llm_proposal_provider.py`, `--validate-llm-proposal-provider` | External LLM proposal provider gate. | Proposal-only; provider output is not canonical. |
| `.codex/product-agent-os/project-code-graph-llm-proposal-eval.json` | `project_graph_llm_proposal_provider.py` | Safety/grounding eval packet for proposal provider. | Unsafe output routes to incident/fallback. |

## Review And Mutation Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-review-ledger.json` | `project_graph_review_ledger.py`, `--build-review-ledger` | Human review decisions: `accepted`, `rejected`, `accepted_gap`. | No accepted proposal without owner decision and evidence refs. |
| `.codex/product-agent-os/project-code-graph-proposal-diff.json` | `project_graph_review_ledger.py` | Proposal diff preview. | Preview only until mutation dry-run. |
| `.codex/product-agent-os/project-code-graph-mutation-plan.json` | `project_graph_canonical_mutation.py`, `--build-canonical-mutation` | Mutation dry-run plan. | Staged plan only; not source mutation by itself. |
| `.codex/product-agent-os/project-code-graph-mutation-journal.jsonl` | `project_graph_canonical_mutation.py` | Append-only mutation journal. | Must cite accepted item and rollback path. |
| `.codex/product-agent-os/project-code-graph-canonical-mutated.json` | `project_graph_canonical_mutation.py` | Staged mutated graph copy. | Generated copy only; canonical graph/source not silently changed. |
| `.codex/product-agent-os/project-code-graph-rollback-proof.json` | `project_graph_canonical_mutation.py` | Rollback proof and digest comparison. | Required before mutation pilot completion claims. |

## Audit, Security And Observability Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-live-audit-log.jsonl` | `project_graph_live_audit.py`, `--build-live-audit` | Redacted append-only audit events. | No secrets, raw source or private data. |
| `.codex/product-agent-os/project-code-graph-live-security-privacy.json` | `project_graph_live_audit.py` | Security/privacy negative cases and findings. | Evidence packet, not a full security certification. |
| `.codex/product-agent-os/project-code-graph-live-observability.json` | `project_graph_live_audit.py` | Runtime health, latency, provider error and degraded-mode visibility. | Generated observability evidence. |
| `.codex/product-agent-os/project-code-graph-agent-skill-handoff.json` | `project_graph_live_audit.py` | Agent/skill ownership, fresh context, verification and stop-condition routing. | Handoff guidance only; agents still need explicit work context. |

## Real Testing And Runtime QA Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-real-testing-readiness.json` | `project_graph_real_testing.py`, `--build-real-testing-readiness` | Readiness and no-hidden-gates packet. | Real testing remains blocked without target/data approval. |
| `.codex/product-agent-os/project-code-graph-real-testing-targets.json` | `project_graph_real_testing.py` | Owner-approved target/data-policy candidates. | Target consent evidence only. |
| `.codex/product-agent-os/project-code-graph-pilot-harness.json` | `project_graph_real_testing.py` | Dry-run pilot harness. | Stage-only; no live execution. |
| `.codex/product-agent-os/project-code-graph-codex-surface-smoke.json` | `project_graph_real_testing.py` | Codex App, CLI and IDE extension smoke planning/evidence. | Does not imply live browser automation. |
| `.codex/product-agent-os/project-code-graph-real-testing-pilot-matrix.json` | `project_graph_real_testing.py` | Use-case pilot matrix. | Planning/readiness evidence. |
| `.codex/product-agent-os/project-code-graph-runtime-browser-qa.json` | `project_graph_runtime_qa.py`, `--build-runtime-qa` | Browser QA expectations/evidence. | No unapproved browser automation; labels and source boundary required. |
| `.codex/product-agent-os/project-code-graph-performance-budget.json` | `project_graph_runtime_qa.py` | Performance thresholds and fallback/accepted-gap handling. | Budget breach disables live layer or records owner gap. |
| `.codex/product-agent-os/project-code-graph-stabilization-ledger.json` | `project_graph_runtime_qa.py` | Stabilization defects and P0/P1 closure status. | No open P0/P1 before closure. |

## Agent/Skill Metrics Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/eval-reports/agent-skill-evaluation-report.html` | `agent_skill_metrics_report.py` | Offline report view for `agent_skill_metrics_loop`. | Report is not proof; candidate-only. |
| `.codex/artifact-templates/agent-skill-scorecard-ledger.md` | Template registry | Append-only scorecard ledger template. | Must cite current evidence window. |
| `.codex/artifact-templates/agent-skill-daily-eval-report.md` | Template registry | Daily triage packet. | No active schedule by default. |
| `.codex/artifact-templates/agent-skill-weekly-verification.md` | Template registry | Weekly owner-review packet. | Requires rollback/holdout/flake/cost evidence or accepted gaps. |
| `.codex/artifact-templates/agent-skill-update-candidate.md` | Template registry | Modernization candidate packet. | No self-applied updates. |

## Professional Code Authoring Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/workflows/coding-standards.md` | Template registry / `workflow-coding-standards` | Workflow for existing-capability scan, one-line/native candidate, dependency refusal, deep-module check, legacy seam evidence and unsupported code-quality claims. | Source contract only; not live enforcement, hook activation or proof of real agent behavior. |
| `.codex/artifact-templates/coding-standard-checklist.md` | Template registry / `artifact-coding-standard-checklist` | Review checklist for `enterprise_leverage_check`, `existing_capability_scan`, `one_line_candidate`, `negative_dependency_rule`, `legacy_seam_check`, `comment_policy` and `cleverness_budget`. | Checklist organizes evidence; it does not prove code quality without current tests/evals/review. |
| `professional_code_authoring` route/eval visibility | Discovery, readiness, runtime route, status dashboard and HTML renderer surfaces | Indicates that Professional Code Authoring is applicable or available for a code-owning task. | `present_unverified` / generated-view evidence only; public map: [Professional Code Authoring Standards](coding-standards.md). |

## First-run analysis artifact

The first-run analysis artifact is a local generated orientation pack for first project review. It helps an operator see inventory, runtime route, control-plane state, graph summary, risks and a safe next action, but it remains `orientation_only_not_proof`.

This map describes artifact families and view-model contracts used by `analysis_artifact_renderer.py` and staged B41/B42 evidence. It is not a complete JSON Schema: the repository has contract fields, tests and staged examples, but no standalone exhaustive JSON Schema validation for every nested first-run surface.

| Artifact / schema | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/analysis/first-run-analysis-packet.json` | `run_first_project_analysis.py --write`, `first_run_analysis.py` | First analysis packet: target, source artifacts, summaries, generated pages, evidence/redaction status and safe next action. | Orientation evidence only; does not prove readiness, release, target mutation, runtime/browser/provider proof or source truth. |
| `.codex/product-agent-os/self-learning-state.json` | State initializer or future approved state writer; consumed read-only by `check_self_learning_due.py --dry-run` and `run_self_learning_loop.py` | `self_learning_state_v1`: install timestamp, last analysis/success/failure, next due timestamp, cadence, report/metrics refs, approval state and disable reason. | Due-check/manual-run state only; current CLIs do not write this file, create active schedules, ingest sessions, call providers, mutate targets or enable auto-apply. |
| `.codex/product-agent-os/self-learning/progress.jsonl` | `run_self_learning_loop.py --stage <dir>` | Append-style `self_learning_progress_v1` phase events for `scope_check`, `due_check`, evidence, metrics, feedback, candidates, reporting and owner review. | Stage-only in B44-S2; no raw chat, hidden telemetry, absolute target paths or auto-approval controls. |
| `.codex/product-agent-os/self-learning/runs/<run_id>/progress.json` | `run_self_learning_loop.py --stage <dir>` | Per-run progress snapshot with run ID, project scope hash, owner approval state, blockers and latest artifact paths. | Generated inspection evidence only; it does not prove quality improvement, owner satisfaction or readiness. |
| `.codex/product-agent-os/self-learning/runs/<run_id>/self-learning-run-packet.json` | `run_self_learning_loop.py --stage <dir>` | `self_learning_run_packet_v1` with scope packet, due-check packet, evidence refs, unsupported claims, metrics placeholders and candidate summary. | Manual-only/staged-only; provider calls, live eval services, target mutation and auto-apply remain not performed. |
| `.codex/product-agent-os/self-learning/self-learning-progress.html` | `run_self_learning_loop.py --stage <dir>` | Offline generated progress view for scope eligibility, due status, phase progress, blockers and owner-review state. | Generated review view only; not source of truth and cannot approve, apply or prove work complete. |
| `.codex/product-agent-os/self-learning-candidates.json` | `self_learning_candidates.py` / runner `candidate_summary` | `self_learning_candidate_packet_v1` and `self_learning_forbidden_action_report_v1` for review-only modernization candidates and forbidden-action fixtures. | Candidate-only; cannot apply changes to skills, prompts, routes, memory, config, hooks or automation. |
| `docs/superpowers/specs/batch44-self-learning-loop-docs-contracts-closure-summary.json` | Self-Learning Loop docs closure | `self_learning_docs_contracts_closure_v1` records docs sync, registry parity and promotion gate status. | Closure evidence only; it does not prove activation, real session import, provider calls, target mutation or automation readiness. |
| `.codex/automation-candidates/self-learning-automation-candidate.md` | Self-Learning Loop automation promotion proposal | Candidate-only promotion packet with owner approval record, `minimum_manual_successful_runs`, rollback/disable path, false-positive audit, flake replay and cost check. | `active schedule remains not_created`; owner approval record is required before any schedule, hook, Codex App automation, GitHub Action or external workflow. |
| `.codex/product-agent-os/analysis/analysis-manifest.json` | `analysis_artifact_renderer.py` | `first_run_analysis_manifest_v1`: pages, digests, source digests, `manifest_digest`, `redaction_report`, `source_policy_gate`, baseline comparison and cleanup guidance. | Generated-view boundary; source files and current command evidence are stronger. |
| `.codex/product-agent-os/analysis/index.html` | `analysis_artifact_renderer.py` | `first_run_cockpit_artifact_v1`: primary self-contained architecture cockpit. | Local review surface; not WebGL/Cosmos.gl, browser screenshot, WCAG, runtime, release or target-apply proof. |
| `first_run_cockpit_artifact_contract_v1` | `build_first_run_cockpit_artifact_contract()` | Contract map for primary cockpit pages, graph layers, renderer choice, large-graph policy and unsupported claims. | Contract map only; not proof that browser/runtime dependencies executed. |
| `architecture_intelligence_design_contract_v1` | `_architecture_intelligence_design_contract()` | Design contract for the architecture cockpit shell, section hierarchy and component grammar. | Design intent; not browser proof or public readiness. |
| `first_run_schema_contract_surface_v1` | `_first_run_schema_contract_surface()` | Inventory of API/schema/config/diagram contracts by path and digest. | Path-and-digest inventory only; not API compatibility, migration safety or schema completeness. |
| `first_run_graph_file_code_surface_v1` | `_first_run_graph_code_surface()` | Project Map and Code Intelligence graph/code surfaces. | Static fallback unless separate approved browser/WebGL evidence exists. |
| `first_run_guided_tour_surface_v1` | `_first_run_guided_tour_surface()` | Guided read order and safe next action surface. | Does not prove a human completed review or approved action. |
| `first_run_evidence_decision_layer_v1` / `first_run_evidence_risk_hierarchy_v1` | Renderer evidence helpers | Supported/unsupported claims, blockers, risks and proposal-only decision surfaces. | Evidence organization only; no completion, fixed, verified or ready claim without current evidence. |
| `first_run_artifact_cleanup_guidance_v1` | `_cleanup_guidance()` | Cleanup preview listing generated files and rollback policy. | `approval_required: true`; `deletion_performed: false`; no automatic cleanup. |
| `first_run_redaction_report_v1` | `_redaction_report()` | Redaction guardrail for generated manifest/model payloads. | Blocks local absolute paths, raw source fields and secret-like values, but is not full DLP/security certification. |
| `batch41_s9_m57_neural_flow_comparison_v1` | B41/S9 comparison artifact | Read-only staged rerun comparison with digests, key deltas, marker checks and no-unapproved-actions surface. | Historical target evidence; not general readiness or freshness after a new rerun. |
| `answer-ledger-template.json` | Guided question protocol | Staged owner-question ledger with `question_id`, status, `target_artifact`, redaction and validation errors. | Not an owner decision or accepted gap until answered and reviewed. |
| `first_run_artifact_scorecard_v1` | `batch39_scorecard.py` | Operator usability scorecard: clarity, completeness, actionability, approval boundary, onboarding time and navigation. | `not release approval`; does not replace owner review or real-project evidence. |

`source_policy_gate` may allow diagnostic artifacts while keeping apply/promotion disabled. `redaction_report` must record blocked secret-like values, raw source fields and local absolute paths before a packet is finalized. `cleanup_guidance` is preview-only: file deletion, target cleanup and rollback actions require separate explicit approval.

## Doubt Verification Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/artifact-templates/doubt-verification-packet.md` | Template registry / `completion-skeptic` | Human-readable `doubt_verification_packet_v1` with claim ledger, requirement ledger, evidence ledger, verdict, accepted gaps and residual risks. | Staged/generated-view boundary; the packet organizes evidence but does not become source truth by itself. |
| `doubt_verification_packet_v1` JSON/YAML packet | `validate_doubt_verification_packet.py` and `doubt_verification.py` | Contract-checked evidence packet for `pass`, `revise`, `needs_more_context`, `blocked_by_approval` and `accepted_risk`. | Reject pass without evidence, fake command evidence, approval-blocked pass and `accepted_gap` without owner/reason/residual risk/follow-up. |
| `completion_skeptic_recommendation` route field | Codex runtime runner | Additive route recommendation for manual completion-skeptic review. | Recommendation only; it does not authorize tools, providers, browser automation, Agents SDK runner or workspace mutation. |

## System File Hygiene Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| JSON output from `validate_system_file_hygiene.py` | `system_file_hygiene.py` | Read-only inventory and findings for maintained system file classes. | `schedule_status: not_created`; no edits, schedules, hooks or external writes. |
| `.codex/workflows/system-file-hygiene-audit.md` | Template registry | Operator workflow for hybrid periodic, on-change, size and release/automation triggers. | Recommendation only until owner approval enables a real schedule. |
| `.codex/artifact-templates/system-file-hygiene-report.md` | Template registry | Staged report for size, duplication, mojibake/BOM, secret, historical-ledger and ownership findings. | Review artifact only; compaction remains a separate slice. |
| `.codex/automation-candidates/system-file-hygiene-audit.md` | Template registry | Candidate-only automation packet for future scheduled hygiene checks. | active schedules remain out of scope until explicit approval and rollback/disable evidence exist. |

The `system_file_hygiene_audit` JSON validator checks nested trigger records, class records, inventory, findings and `summary.status`; malformed packets are blocked before compaction or automation promotion.

System hygiene JSON fields: `audit_trigger`, `finding_type`, `compaction_decision`, `approval_boundary`, `no_secrets_status` and `active_schedule_markers`. CLI `--trigger` records the run reason without workspace writes. Staged `system-file-hygiene-report.md` captures audit trigger, system file class, finding type, owner, compaction decision, active schedule markers, no-secrets status and owner-approved slice boundary.

The HTML/JSON status dashboard projection uses only bounded `file_statuses`: relative path, class, owner, state, severity, finding count, `mtime_utc`, `age_days`, `content_digest` and `top_finding`. Dates come from filesystem metadata and are freshness hints, not semantic proof of content correctness, source ownership or completion readiness.

## Planned Execution Evidence Files

| Planned artifact | Surface | Status before approval |
| --- | --- | --- |
| `live-server-run-evidence.json` | `approved_local_runtime_launch` | Planned only; requires local runtime approval packet. |
| `browser-automation-smoke.json` | `actual_browser_automation_smoke` | Planned only; requires browser automation approval packet. |
| `provider-call-evidence.json` | `approved_provider_api_pilot` | Planned only; provider call blocked until approval/redaction/cache/budget/eval threshold exists. |
| `canonical-mutation-run.json` | `approved_canonical_mutation_pilot` | Planned only; requires accepted ledger item, dry-run plan, journal and rollback proof. |
| `git-release-pr-evidence.md` | `explicit_git_release_pr_action` | Planned only; no git stage/commit/push/PR without explicit user command. |

## Verification

Artifact verification should check:

- expected `artifact_kind` and `approval_boundary`;
- stage root confinement and rollback/disable path;
- redaction of secrets, raw source bodies, absolute paths and private data;
- generated-view or staged-evidence label;
- source-boundary label when screenshots, cockpit, dashboard or runtime QA evidence is present;
- fallback path when live/provider/runtime layers are disabled;
- `schedule_status: not_created` for system file hygiene outputs unless a later approved automation slice records otherwise;
- current command evidence before readiness, works, complete or release claims.

## Inputs

- Checked-in source docs, control-plane files and generated artifact packets.
- Approval records, run evidence, redaction state and owner decisions where required.

## Outputs

- Reviewable artifact contracts with producer, purpose, boundary and verification expectations.
- A stable map for docs tests, source registry entries and closure checks.

## Risks And Failure Modes

- A generated HTML/JSON view can be mistaken for source truth.
- Stale graph fingerprints or caches can make old source look current.
- Provider artifacts can leak private data if redaction/cache/budget gates are skipped.
- Review ledger decisions are invalid without owner and evidence refs.
- Mutation artifacts are unsafe without rollback proof.
- Planned artifact names can be mistaken for executed evidence.

## Next Action

Use this contract map when writing docs tests, source registry entries and packaging/closure checks. Navigation and generated `site/` refresh are intentionally handled after the source docs packet is stable.
