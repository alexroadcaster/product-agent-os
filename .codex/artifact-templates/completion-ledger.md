# Completion Ledger

Source status: project-local reporting contract template.

Use this visible closing packet when the root lifecycle scope requires it,
paired with the applicable Task Start Brief. Ordinary fixes and read-only/partial/
blocked work need concise results, evidence and gaps unless that scope applies.
A ledger reports evidence; it does not declare that the product is ready.

Start with `closure_contract: product-agent-os-completion-ledger-v2`.
Show each field as a separate list item: `- Field:` or `- **Field:**`. Chat values may be Russian; durable
records follow the project language policy. Use N/A with a reason when inapplicable.

- Result: actual outcome and task status.
- Scope: owning contract, parent/task IDs, child status and excluded work.
- Evidence: exact changed paths, current commands/results and scenario evidence.
- Review: context_mode = self_review / separate_reused_context /
  separate_fresh_context / fresh_blind_review; reviewer task/thread identifier
  when present; findings; and tester_verdict = closed_allowed / partial_only /
  blocked / not_reviewed. Never imply a stronger review mode than observed.
- Limits: unsupported claims, missing evidence, residual risk and acceptance gaps.
- Tech debt: none / yes / accepted / blocked / deferred; name remaining owner/row.
- Activation / fallback: intended path, prior path, selector, policy, positive
  and negative proof, live alignment; N/A for no runtime change. Instruction
  changes report static evidence versus fresh-session behavior separately.
- Docs impact: updated with canonical docs, paths, evidence destination and
  successful gate / no_change_needed with reason / accepted_gap with affected
  doc, owner, residual risk and next action. Detailed run evidence belongs under
  the owning task evidence artifact, such as `docs/superpowers/specs/`; the root RUNLOG receives only the compact handoff.
- Context integrity: effective instruction chain observed; selected skills and
  directly required instructions fully read; needed truncations recovered; compaction
  and structured handoff status; or exact unavailable reason.
- Runtime metrics: model, reasoning, elapsed, input/cached/output/reasoning tokens,
  tool calls, agent spawns, waits/timeouts, compactions and skill reads/truncations.
  Use `not_available` only when the trace is unavailable and state why.
  Summarize available metrics; do not create scripts or raw transcript copies
  solely to populate unavailable counters.
- Closure: `closure_level = <strongest_supported_level>`; state the permitted final wording. The explicit key and equals sign are required.
- Next step: smallest safe follow-up, or none with a reason.
- Execution time: measured elapsed time; otherwise `not_available` with the
  trace limitation. Never invent duration.

Required partial, blocked or unreviewed children prevent parent completion. For
a docs-only task, docs_static_verified may close artifact work while runtime
activation remains not_verified. An accepted docs gap can close a bounded handoff
but cannot close the parent that requires that document.

Primary records project delivery evidence in RUNLOG.md only when the task scope
authorizes that file, and updates only the owning task status. No hook validates
chat automatically; the marker is a reporting convention.
