# Product-Agent OS Artifact Gallery

Source status: `official + experiment`

This page shows the reviewable outputs a user normally gets from Product-Agent OS and why each output matters. It is not an execution ledger or proof of readiness. Source of truth remains in project source files, current control-plane artifacts, the source registry, fresh command/eval/runtime evidence, owner decisions and accepted gaps.

## Quick Overview

| Category | Example outputs | User-facing value | Trust boundary |
| --- | --- | --- | --- |
| Control plane | `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` | The project gets durable rules, scope, plan, checks, quality gates and current handoff. | Authoritative only when current, owner-reviewed and consistent with source code. |
| First-run route | lifecycle state, risk map, `usage_mode`, evidence gaps, `safe_next_action` | The user can see where to start without a broad rewrite. | Detection is not verification; the next step still needs evidence. |
| Methodology packet | recommendations, owner questions, methodology-to-artifact mapping | Only risk-relevant gates are activated: DDD, TDD, ADD, FSD, eval-driven work and related practices. | `present_unverified` does not become `present_verified` without an artifact or owner decision. |
| Status dashboard | `status.html`, `status.json`, route snapshot | The route state, gaps and nearest action are visible quickly. | It is an orientation surface; it does not prove completion or readiness. |
| Graph and cockpit | `project-code-graph.json`, `project-cockpit.html`, query packets | Large projects become easier to read through hotspots, read order and affected tests. | Generated views help navigation, but canonical files remain authoritative. |
| Real-testing evidence | runtime, browser, provider, mutation and git evidence packets | Every external or mutating action is visible as a separate decision. | One approval never authorizes another action; each run has its own boundary. |
| Scorecards | metrics report, scorecard ledger, modernization candidate | Agents and skills can improve from evidence instead of impression. | Candidate-only: proposals do not self-apply. |
| Release and closure | readiness packet, artifact manifest, rollback, handoff | PR, package or release decisions have scope, checks and residual risks. | No publish, git stage, commit, push or PR occurs without separate explicit approval. |

## First-run Packet And Cockpit

First-run outputs help a reader understand a project before changing files. They are not source truth and do not prove readiness by themselves.

| Artifact | Where to find it | What it shows | Producer / consumer | What it proves | What it does not prove |
| --- | --- | --- | --- | --- | --- |
| First-run packet | `.codex/product-agent-os/analysis/first-run-analysis-packet.json` | Inventory, route, source-policy state, gaps, safe next action and unsupported claims. | `run_first_project_analysis.py --write`, `first_run_analysis.py` -> `analysis_artifact_renderer.py`. | A local diagnostic packet was assembled for operator review. | Source truth, readiness, completion, release, runtime/browser/provider proof or target mutation safety. |
| Render manifest | `.codex/product-agent-os/analysis/analysis-manifest.json` | Pages, page/source digests, `manifest_digest`, `redaction_report`, `source_policy_gate`, baseline comparison and cleanup guidance. | `analysis_artifact_renderer.py` -> docs maintainer, reviewer, cleanup handoff. | The renderer recorded generated files and guardrails. | Generated-site freshness, semantic source review or public readiness. |
| Primary HTML cockpit | `.codex/product-agent-os/analysis/index.html` | Self-contained architecture cockpit: overview, project map, code intelligence, contracts, methodology, quality, risk and recommendations. | `analysis_artifact_renderer.py` -> human reader. | The generated view is available as an orientation surface. | WebGL/Cosmos.gl runtime execution, browser screenshots, WCAG certification or release readiness. |
| Diagnostic HTML pages | `.codex/product-agent-os/analysis/*.html` | Detail pages for inventory, architecture, methodology, runtime route, control plane, graph, code flow, quality/evals, risks and recommendations. | `analysis_artifact_renderer.py` -> maintainer diagnostics. | Sections can be read separately during review. | Source files or the primary cockpit. |
| Answer ledger | `answer-ledger-template.json` next to staged first-run outputs | Owner questions, answer status, `target_artifact`, redaction metadata and validation errors. | Guided question protocol -> owner handoff. | Questions are prepared and private-data boundaries are marked. | Owner decision, accepted gap or artifact update before an answer is reviewed. |
| Comparison packet | `batch41-s9-m57-neural-flow-comparison.json` or similar target comparison | Digest/key/HTML marker deltas between staged runs, preserved unsupported claims and no-unapproved-actions surface. | Maintainer comparison result -> reviewer. | A specific read-only rerun compared staged outputs and recorded mutation/runtime/browser/provider/git boundaries. | General freshness for another target or after a new rerun. |

## Manifest Fields To Check

When reading the manifest, check `schema_version`, `pages`, `page_digests`, `source_digests`, `primary_cockpit`, `cockpit_contract`, `redaction_report`, `source_policy_gate`, `baseline_comparison` and `cleanup_guidance`. These fields describe generated evidence and guardrails; they do not replace source review, owner decisions or current commands.

## Generated-view Policy

Generated dashboards, graphs, cockpits, scorecards, reports and comparison packets are orientation evidence. They help choose the next action, but they do not replace source files, checked-in contracts, control-plane artifacts, source registry entries, current command/eval/runtime evidence, owner decisions or accepted gaps.

If a first-run artifact looks convincing, the next step must still be source-backed: read the owning source, check the current command or record an explicit accepted gap. Generated `site/` freshness remains the final `DOC-M25` gate after G2-G5 and does not follow from this gallery.

## Cleanup Guidance

`first_run_artifact_cleanup_guidance_v1` in the manifest is guidance, not permission to delete files. Without separate approval, do not delete user-authored files, source docs, project config, `.git` or anything outside the generated analysis directory. A cleanup list helps reviewers understand renderer output; it is not rollback proof for release, mutation or external-write actions.

## How To Read Outputs

1. Start with the output category and the user question it answers.
2. Open the owning source: source file, control-plane artifact, command evidence, eval report or owner decision.
3. Check the trust boundary: what the output proves and what it only helps review.
4. Take the nearest safe action instead of treating the whole project map as a command.

## Completion-skeptic Examples

These completion-skeptic examples are synthetic and source-safe. They show how a `doubt_verification_packet` changes final answer style without claiming that pilot value is proven.

| Example id | Artifact type | Trigger | Packet excerpt | Verdict |
| --- | --- | --- | --- | --- |
| `docs_research_example` | Docs/research answer | "Check sources" | source registry evidence, community `intake_only`, `needs_fresh_check` for current facts | `revise` if unsupported claims are present |
| `code_check_example` | Code/change claim | "Done?" | command evidence, missing lint/test checks, approval boundary | `blocked_by_approval` or `accepted_risk` when checks cannot run |
| `architecture_review_example` | Architecture/spec | "Did we miss anything?" | requirement ledger, non-goals, dependencies, rollback gaps | `revise` only confirmed architecture gaps |
| `product_planning_example` | Product plan | "Check the matrix" | acceptance criteria, user value, stop conditions, dependencies | `revise` for missing tasks or `accepted_risk` for scoped cuts |
| `security_release_example` | Security/release | "Can we ship?" | source status, rollback, no-unapproved-actions proof, owner approval | `blocked_by_approval` until release evidence exists |
| `ai_eval_example` | AI/eval work | "Check quality" | baseline/current eval, scorecard thresholds, false pass/rewrite signals | manual-only until scorecard and owner review |

## Related Pages

- [Artifact Contracts](artifact-contracts.md) describes JSON, HTML and ledger packet formats.
- [Doubt verification loop](../playbooks/doubt-verification-loop.md) shows the manual workflow behind these examples.
- [Project Code Graph](project-code-graph.md) explains the generated graph, cockpit and query packets.
- [Methodology Intelligence](methodology-intelligence.md) shows how DDD, TDD, ADD, FSD and other methods are selected.
- [Approval-Bound Real Testing](approval-bound-real-testing.md) fixes the runtime, browser, provider, mutation and git action boundaries.
- [Packaging And Closure](packaging-and-closure.md) connects final checks, release packet, rollback and handoff.

## Verification

For a documentation change, this page must remain represented in `mkdocs.yml`, `tools/check_docs.py`, the paired `.en.md` page and the focused docs contract. If navigation or rendered `site/` output changes, strict MkDocs build is required.

## Risks

- The gallery can be mistaken for proof of readiness.
- Generated dashboard, graph, cockpit, scorecard or report output can become stale faster than source files.
- Historical evidence and public product copy must stay separate: history explains provenance, while public docs should route the user to the next action.
