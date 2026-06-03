# Product-Agent OS artifact contracts

Source status: `official + experiment`

Эта страница перечисляет основные generated artifacts Product-Agent OS для modernization loop, project code graph, live/runtime governance и approval-bound handoff. Это не JSON Schema spec, а operator-facing contract map: что создается, зачем нужно, где проходит source-of-truth boundary и какие approval gates действуют.

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
- current command evidence before readiness, works, complete or release claims.

## Risks And Failure Modes

- A generated HTML/JSON view can be mistaken for source truth.
- Stale graph fingerprints or caches can make old source look current.
- Provider artifacts can leak private data if redaction/cache/budget gates are skipped.
- Review ledger decisions are invalid without owner and evidence refs.
- Mutation artifacts are unsafe without rollback proof.
- Planned artifact names can be mistaken for executed evidence.

## Next Action

Use this contract map when writing docs tests, source registry entries and packaging/closure checks. Navigation and generated `site/` refresh are intentionally handled after the source docs packet is stable.
