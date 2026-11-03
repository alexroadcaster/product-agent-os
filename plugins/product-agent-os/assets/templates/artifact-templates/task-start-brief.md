# Task Start Brief

Source status: project-local reporting contract template.

Use when required by the root lifecycle scope: large/high-risk or financially
material implementation, release/readiness closure, or an explicit packet request.
Ordinary fixes and read-only/partial/blocked work need concise results, evidence
and gaps unless that scope applies. Show an applicable packet before broad
exploration or edits. First read applicable instructions, this template and the
source needed to identify the task. Mark uncertain fields as inferred.

Keep all nine bold field labels with content on the next line. Chat values may
be Russian; stored artifacts follow the project language policy. Preserve relevant user
wording in chat under Raw; persist only an explicitly authorized
paraphrase when necessary, without private raw chat. Use N/A with a reason.

**Request**

Raw: relevant user wording. Agent-ready: one to three executable sentences.

**Goal**

The single verifiable outcome or decision.

**Context**

Owning plan, parent/task IDs, selected children, current sources and evidence
gaps. State the observed instruction chain and any compaction/handoff dependency.

**Scope**

In scope, out of scope, exact owned/shared paths and forbidden stronger claims.

**Value**

Technical value and product value relevant to the decision, or N/A with reason.

**Execution**

Request type and bounded approach. Record:

- Agent budget: primary plus maximum concurrent workers/reviewer; or zero delegation.
- Selected skill: canonical name, observed path/package/version when available,
  why selected and directly required references. Add `skill_read_complete:` only
  if an active machine contract explicitly requires it; full reading is still required.
- Model/reasoning: inherited baseline or evaluated override with rationale.
- Expected artifacts (reuse existing destinations) and bounded wait/sequential
  fallback policy. Do not persist a duplicate of this visible packet by default.

**Acceptance**

Expected result, scenarios, exact checks with expected outputs, review and
human acceptance when applicable. Name the evidence owner.

**Risks / approvals**

Material risks, allowed side effects, stop conditions, preservation and rollback.
For runtime changes: intended route, old path, selector, fallback policy,
positive activation proof, old-path negative proof and live dependency gaps.
For prompt/agent/LLM changes: behavior, allowed/forbidden context, output contract,
grounding/privacy constraints, baseline cases and model/runtime verification gaps.

**Next step**

The first concrete action after this brief.

A heading alone, merged progress paragraph or missing field is not a brief.
Update changed scope visibly before dependent work. This template creates no
hook, scheduler, permission or automatic delegation.
