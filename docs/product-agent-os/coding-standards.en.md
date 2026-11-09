# Professional Code Authoring Standards

Source status: `project-authored + research-backed + experiment`

Sources: Batch 45 research packets `plugins/product-agent-os/assets/research/ai-agent-coding-standards-research.md` and `plugins/product-agent-os/assets/research/ai-agent-coding-literature-research.md`, Batch 45 S5 packet `docs/superpowers/specs/batch45-professional-code-s5-learning-automation-summary.json`, S6 packets `docs/superpowers/specs/batch45-agent-behavior-eval-results.json` and `docs/superpowers/specs/batch45-comment-policy-promotion-decision.json`, S7 packets `docs/superpowers/specs/batch45-real-project-scorecard.json` and `docs/superpowers/specs/batch45-real-project-decision-packet.json`, M37 remediation packet `docs/superpowers/specs/batch45-review-remediation-summary.json`, [Development Standards](development-standards.md), [Artifact Contracts](artifact-contracts.md), [Behavioral Evals](behavioral-evals.md), [Scenarios](scenarios.md), [Code Review playbook](../playbooks/code-review.md).

Professional Code Authoring is the Product-Agent OS layer for non-mechanical coding tasks. Its main rule is simple: the agent checks existing capability, standard library support, framework primitives, configuration paths, current dependencies and project helpers before adding custom code. The best implementation may be one line, a deletion or a configuration change when that satisfies the acceptance criteria with less debt.

## Ordinary authoring and current integration {#ordinary-authoring}

For an ordinary change, the default generation context is `.codex/artifact-templates/code-change-contract.md`: eight T25 fields without repeated injection of the full checklist. The active workflow and packaged contract are aligned; `coding-standard-checklist.md` is reviewer/reference material when additional detail is needed.

The opt-in [ordinary CLI route](cli-reference.en.md#ordinary-route) connects discovery to the existing T26/T27 selectors. Each selected check needs a risk/invariant and a source; missing tools do not authorize auto-installation. Docs-only can be `not_applicable`, while reuse/deletion/no-op can be correct outcomes. Project-mandated checks remain required.

High-risk and full lifecycle reporting are selected independently of coding-contract length. Local CLI/fixture checks establish integration; updating the active file does not prove fresh-session loading. T23–T29 are not reopened; T30–T34 and behavioral promotion remain separate work. Historical Batch 45 receipts below retain their own evidence ceiling.

## Applied Gates

G7 refines local contracts: a bounded capability summary reuses current inventory through the existing `existing_capability` field; reference coverage stays unknown until source inspection. Refactors reuse existing/characterization checks without artificial RED. Fingerprints include known lockfiles/config and explicit `verification_paths`; `verification_environment` is caller-reported, not automatic tool-version proof. Missing coverage does not mean clean.

Review distinguishes confirmed defects, preferences, rejected findings and unresolved risks, tied to a checked revision and scenario. T34 evaluator bytes remain frozen; G7 uses a separate versioned evidence contract. See the [research and limits](../../research/product-agent-os-g7-repository-deep-review-2026-11-09.md) and [G7 plan](../../research/product-agent-os-audit-remediation-task-plan-2026-11-09.md). Local mechanism checks do not prove better model generation or fresh-session loading.

| Gate | What the agent records | When it can be skipped |
| --- | --- | --- |
| `enterprise_leverage_check` | The existing path checked before custom implementation. | Mechanical docs/format-only work with a `not_applicable` reason. |
| `existing_capability_scan` | Standard library, framework, current dependency, project helper, config and deletion/reuse options. | Tiny isolated fix where source and reason are obvious and recorded. |
| `one_line_candidate` | The shortest direct expression or native call before a multi-line helper. | Not applicable for behavioral workflow, migration or UI composition work. |
| `negative_dependency_rule` | Why a new dependency is needed, rejected alternatives and rollback/removal path. | No new dependency. |
| `deep_module_check` | Why an abstraction hides real complexity instead of creating a shallow wrapper. | Direct call is better than abstraction. |
| `legacy_seam_check` | Characterization evidence, seam strategy, rollback or accepted gap. | No legacy/refactor impact. |
| `comment_policy` | Comments explain intent, invariant, hazard or trade-off; state machines, algorithms, security/privacy/data/concurrency logic, and functions with non-obvious invariants need a docstring, intent comment, or `comment_not_needed_reason`. | The code is self-explanatory and obvious comments would be noise. |
| `cleverness_budget` | Payoff, tests, naming clarity and reviewer rationale. | Direct/simple path chosen. |

## Activation Path

Product-Agent OS applies this standard through staged source artifacts:

| Surface | How it appears | Boundary |
| --- | --- | --- |
| Workflow | `.codex/workflows/coding-standards.md` from the packaged template. | Template registration proves the workflow can be staged, not live enforcement. |
| Checklist | `.codex/artifact-templates/coding-standard-checklist.md`. | Review artifact; not source truth without current evidence. |
| Agent task packet | `.codex/artifact-templates/agent-task-packet.md` carries compact handoff fields. | Handoff contract, not raw research body. |
| Skills and agents | Builder/reviewer/architect/tester/docs-maintainer prompts reference the compact contract. | Skills activate by selection/context; they do not launch subagents automatically. |
| Evals | `behavioral-workflows.json`, agent-context contract and focused tests reject shortcut behavior. | Local deterministic coverage only. |
| Runtime route and HTML | `professional_code_authoring` appears as recommendation/visibility. | Generated view is `orientation_only_not_proof`. |

## Learning-Loop Improvement Policy

Self-Learning Loop may propose future Professional Code Authoring improvements only as review candidates. Candidate inputs are aggregate metrics, owner feedback, eval failures and manual pilot evidence; raw private chat bodies and hidden telemetry are forbidden.

The candidate may point only to staged update targets: the coding standards workflow, coding-standard checklist, behavioral/agent-context evals, hook-governance candidate docs and learning-loop/automation-promoter skill guidance. Before promotion review, it needs `minimum_manual_successful_runs: 3`, owner review, rollback/disable path, false-positive audit, flake replay and cost check.

Until a separate approval-gated batch, Product-Agent OS must not auto-apply these candidates, activate hooks, create schedules, change global config, call providers, mutate target projects, ingest raw private chat or perform external writes.

## Senior Leverage Ladder

Use this order before writing new code:

1. Delete or avoid the code path entirely.
2. Use a language construct, standard library or framework primitive.
3. Reuse a current dependency or project helper already accepted by the repo.
4. Configure existing behavior instead of adding logic.
5. Compose a small direct expression.
6. Add a deep module only when it hides real complexity behind a stable interface.
7. Add a dependency only after alternatives, lifecycle risk, security and removal path are recorded.

## Evidence Ceiling

Batch 45 currently supports `docs_contract_ready` / `synthetic_green` claims for local source artifacts, templates, eval cases, discovery/readiness visibility, runtime route visibility, generated HTML visibility and candidate-only learning-loop/automation policy. M26 records a live behavior-eval no-go, M27 keeps the M25 advisory local/non-blocking and rejects stronger advisory, CI and blocker promotion, M35 keeps S7 fixture-local/source-only with no-go for treatment v2 promotion, and M37 records local hook/validator hardening plus review remediation docs/control-plane sync only. T17 freezes the metadata-only held-out corpus manifest in `docs/superpowers/specs/batch45-postq4-t17-frozen-heldout-corpus.json` / `B45-POSTQ4-T17-A01`; T18 defines the same-model promotion-grade eval design and strict schema in `docs/superpowers/specs/batch45-postq4-t18-promotion-grade-eval-design.json` / `B45-POSTQ4-T18-A01`; T19 defines the cost/timeout/raw-temp-only retention policy in `docs/superpowers/specs/batch45-postq4-t19-cost-timeout-retention-policy.json` / `B45-POSTQ4-T19-A01`; T20 stages historical exact approval packets in `docs/superpowers/specs/batch45-postq4-t20-promotion-grade-eval-approval-packet.json` / `B45-POSTQ4-T20-A01` and `docs/superpowers/specs/batch45-postq4-t20-promotion-grade-eval-approval-packet-1000s.json` / `B45-POSTQ4-T20-A02`, then records the consumed cost-waived approval in `docs/superpowers/specs/batch45-postq4-t20-promotion-grade-eval-approval-packet-cost-waived.json` / `B45-POSTQ4-T20-A03`; T21 records blocked preflight history in `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-run-preflight-blocked.json` / `B45-POSTQ4-T21-PREFLIGHT-A01`, `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-run-preflight-timeout-mismatch.json` / `B45-POSTQ4-T21-PREFLIGHT-A02` and `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-run-preflight-cost-unknown.json` / `B45-POSTQ4-T21-PREFLIGHT-A03`, plus current strict-schema abort evidence in `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-results.json` / `B45-POSTQ4-T21-COST-WAIVED-RUN-A01` with `approved_primary_calls_started=1`, `reviewer_calls_started=0`, `valid_pair_count=0`, `invalid_pair_count=8` and `schema_failure_count=1`; T22 records a blocked reviewer/no-go decision in `docs/superpowers/specs/batch45-postq4-t22-promotion-grade-decision-packet.json` / `B45-POSTQ4-T22-A02` with `reviewer_gate_status=not_run_due_t21_invalid_schema_abort` and `promotion_allowed=false`. They are not valid baseline/treatment pair evidence, reviewer-gate evidence or promotion evidence. They do not prove that AI agents now write enterprise-quality code in real projects; M26/M27/M35/M37/T17/T18/T19/T20/T21/T22 only sharpen that ceiling.

Unsupported without a later approval-gated batch:

- live runtime or browser behavior;
- hook activation or blocking enforcement;
- active automation, schedule creation or Self-Learning Loop auto-apply;
- provider/model/API calls;
- installed plugin cache refresh;
- target workspace mutation;
- git, release, deploy or publish action;
- replacement of human review.

## Quick Checklist

Before a non-mechanical code edit, the agent should be able to answer:

- What existing capability was checked?
- What is the one-line/native candidate?
- Why is custom code still needed?
- What dependency or legacy debt is added, avoided or removed?
- What test/eval/runtime evidence will support the claim?
- Which claims remain unsupported?

Next artifact: use [Development Standards](development-standards.md) to decide whether the gate applies, [Artifact Contracts](artifact-contracts.md) to inspect the checklist boundary and [Behavioral Evals](behavioral-evals.md) to verify shortcut resistance.

## G7 architecture evidence

The approved local Import Linter 2.16 and dependency-cruiser 18.6.0 synthetic corpus verifies allowed, direct/transitive and cyclic dependencies; JavaScript alias and unresolved-import controls are included. JSON process exit alone is not a clean result. The optional profile API validates supplied current receipts and immutable baseline comparisons; ordinary discovery stays declaration-only. `.mjs` controls do not prove TypeScript resolver or type-only behavior. [Recorded results](../../research/product-agent-os-g7-execution-report-2026-11-09.md).
