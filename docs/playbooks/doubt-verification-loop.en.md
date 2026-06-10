# Playbook: Doubt / verifier loop

Source status: `official + experiment`

Sources: [Grounded answering](grounded-answering.md), [Hallucination Control](../prompting/anti-hallucination.md), [Artifact Contracts](../product-agent-os/artifact-contracts.md), [Behavioral evals](../product-agent-os/behavioral-evals.md), [Batch 40 source-transfer packet](../sources/product-agent-os-batch40-doubt-verifier-source-transfer.md).

## Purpose

The Doubt / verifier loop turns a manual "check again" request into a reviewable completion gate. The operating shape is `worker_output -> doubt_verification_packet -> completion-skeptic -> revise_or_pass`.

The point is not to make the agent anxiously rewrite the answer. The point is to extract checkable claims, requirements, evidence gaps and approval boundaries, then change only the parts where the verifier found a concrete defect or missing evidence.

## Trigger

Use `completion-skeptic` when one of these signals appears:

- the user asks "check again", "did we miss anything", or "check before final";
- the agent is about to say "done", "ready", "works", "fixed", "verified" or an equivalent claim;
- code, docs/source registry, architecture contracts, security/release/eval layers changed;
- the answer depends on current facts, source-sensitive docs, tool output or generated views;
- there is false-pass, false-rewrite, stale-evidence or approval-bypass risk.

Skip the loop for a small deterministic answer when there is no completion claim, risk class or user-trigger.

## Workflow

1. Preserve the artifact under review: worker output, diff summary, doc draft, plan row or final answer candidate.
2. Extract the claim ledger: each checkable claim gets `claim_type`, `status`, `evidence_refs` and `residual_risk`.
3. Extract the requirement ledger: user request, acceptance criteria, non-goals, approval constraints and missing context.
4. Fill the evidence ledger: source registry, local files, current commands, eval runs, owner decisions, approved browser/runtime/web checks or explicit missing check.
5. Run the skeptic pass: `completion-skeptic` returns `pass | revise | needs_more_context | blocked_by_approval | accepted_risk`.
6. The reviser changes only confirmed gaps. Rule: do not rewrite first.
7. The final answer names what was checked, what changed and what remains an accepted_gap or residual risk.

## Packet Excerpt

```yaml
doubt_verification_packet_v1:
  artifact_under_review: "final answer candidate"
  claim_ledger:
    - id: "C1"
      claim: "The docs navigation includes the new playbook."
      claim_type: "docs_behavior"
      status: "supported"
      evidence_refs: ["mkdocs_nav_current_run"]
  requirement_ledger:
    - id: "R1"
      requirement: "Document architecture, diagrams and examples."
      status: "covered"
  evidence_ledger:
    - id: "mkdocs_nav_current_run"
      provider: "current_command"
      provenance_kind: "command"
      status: "available"
  verdict:
    status: "revise"
    reason: "One example category is missing."
  accepted_gaps:
    - owner: "Product owner"
      reason: "Manual pilot evidence is B40-S5 scope."
      residual_risk: "Usefulness is not proven by docs alone."
      follow_up: "Run the B40-S5 pilot ledger."
```

## Examples

| Example id | Task type | Trigger | Packet focus | Safe final style |
| --- | --- | --- | --- | --- |
| `docs_research_example` | docs/research answer | "Check sources" | source registry, official/community split, `needs_fresh_check` | Separate supported facts, assumptions and unsupported claims. |
| `code_check_example` | code change | "Done?" | current command evidence, lint/test gaps, approval boundary | Name commands run and missing checks; avoid a works claim without run evidence. |
| `architecture_review_example` | architecture/spec | "Did we miss anything?" | requirements, non-goals, dependency and rollback gaps | Revise only confirmed architecture gaps. |
| `product_planning_example` | feature plan | "Check the matrix" | acceptance criteria, user value, dependencies, stop conditions | Return missing tasks and accepted scope cuts. |
| `security_release_example` | release/security | "Can we ship?" | approval gates, source status, rollback, no-unapproved-actions proof | Block or accepted_risk instead of a release claim. |
| `ai_eval_example` | AI/eval work | "Check quality" | baseline, current eval, scorecard thresholds, false pass/rewrite | Keep manual-only until pilot and owner review. |

## Failure Modes

- False pass: the packet says `pass` while evidence is stale, generated-only or approval-blocked.
- False rewrite: the skeptic rewrites correct content without a confirmed gap.
- Fake evidence: command output, source IDs or tool traces are invented.
- Context leak: raw private chat logs, secrets or local absolute paths enter packet examples.
- Automation drift: manual success is skipped and the loop becomes an active hook, MCP server, Agents SDK runner or automation.

## Boundaries

No active hook, automation, MCP server, Agents SDK runner or provider call is created by this playbook. It documents the manual and plugin-local path only. Future guardrail or runtime integration requires a separate approval packet, privacy review, scorecard evidence and rollback/disable path.

## Next Artifact

For one task, produce a `doubt_verification_packet` and a short final answer update. For repeated success, record failure examples, eval cases and owner review, then consider the normal promotion chain: manual -> playbook -> skill -> plugin -> automation candidate.
