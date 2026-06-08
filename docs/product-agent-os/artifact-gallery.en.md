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

## How To Read Outputs

1. Start with the output category and the user question it answers.
2. Open the owning source: source file, control-plane artifact, command evidence, eval report or owner decision.
3. Check the trust boundary: what the output proves and what it only helps review.
4. Take the nearest safe action instead of treating the whole project map as a command.

## Related Pages

- [Artifact Contracts](artifact-contracts.md) describes JSON, HTML and ledger packet formats.
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
