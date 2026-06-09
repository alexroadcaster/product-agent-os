# Doubt Verification Packet

Source status: generated local artifact template; not source of truth by itself.

Project: {{ project_name }}
Workspace: {{ workspace_path }}
Profile: {{ profile_name }}
Generated at: {{ generated_at }}

## Schema

- schema_version: `doubt_verification_packet_v1`
- packet kind: `doubt_verification_packet`
- write policy: read-only evidence ledger
- source policy: doubt verification packet is evidence ledger, not generated dashboard proof
- completion skeptic recommendation: route this packet before any final completion claim when evidence is missing, stale, high-risk, approval-bound, or based on generated views.
- No secrets, credentials, private customer data, raw private chat logs, unredacted local absolute paths, or provider tokens.

## Artifact Under Review

- kind: task_row | runtime_result | handoff_packet | docs_page | code_change | staged_artifact | not_available
- path: relative path only
- label:
- owner:
- review trigger:

## Verdict

Allowed values:

- pass
- revise
- needs_more_context
- blocked_by_approval
- accepted_risk
- blocked

Verdict:

## Claim Ledger

Use `claim_ledger` for every statement that would otherwise become "done", "ready", "verified", "implemented", "safe", "complete", or "nothing missed".

| claim_id | claim | status | provenance | notes |
| --- | --- | --- | --- | --- |
| claim-001 |  | supported / unsupported / contradicted / needs_fresh_check / assumption / accepted_gap | command/source/ref + checked_at |  |

Supported claims require current command evidence, source-backed artifact evidence, owner evidence, or explicit accepted gaps.
Unsupported claims must remain visible in handoff mapping and final response risks.

## Requirement Ledger

Use `requirement_ledger` to map user acceptance criteria, task rows, plans, docs promises, architecture requirements, and approval boundaries.

| requirement_id | requirement | status | provenance | evidence owner |
| --- | --- | --- | --- | --- |
| req-001 |  | covered / partial / missing / not_applicable / accepted_gap | source/ref + checked_at |  |

Partial or missing requirements block a `pass` verdict unless the gap is explicitly accepted with owner, reason, residual risk, and follow-up.

## Evidence Ledger

Use `evidence_ledger` to record proof, orientation evidence, stale evidence, missing evidence, approval-required evidence, and accepted gaps.

| evidence_id | evidence_provider | evidence_role | status | evidence_ref | provenance |
| --- | --- | --- | --- | --- | --- |
| ev-001 | command / source_registry / local_file / fixture_eval / transcript_eval / codex_compatibility / owner_evidence / accepted_gap | proof / orientation / gap | available / missing / stale / approval_required / not_applicable / accepted_gap | relative ref or command | kind/ref/checked_at |

generated dashboards are not completion proof.
Generated site, status dashboard, status snapshot, reports, and project graph output are orientation evidence only unless backed by the underlying source artifact or current command evidence.

## Gap Ledger

Accepted gaps must name owner, reason, residual risk, and follow-up condition.

| gap_id | related_claim_or_requirement | owner | reason | residual_risk | follow_up |
| --- | --- | --- | --- | --- | --- |
| gap-001 |  |  |  |  |  |

## Approval Boundary

- status: not_required | required | approval_blocked
- hits:
- explicit approval artifact:
- forbidden actions without approval: live automation, provider/live external model/API calls, browser automation, external writes, target workspace mutation, canonical graph mutation, git stage/commit/push/PR.

## Handoff Mapping

Map the packet into the standard handoff contract:

- verified_claims:
- unsupported_claims:
- commands_run:
- verification_evidence:
- approval_requirements:
- open_risks:
- stop_reason:
- recommended_next_role:

## Completion Report Integration

Before marking a task `implemented`, link this packet from the task Completion Report:

- what was rechecked:
- details found on second pass:
- files touched / work locations:
- verification evidence:
- accepted gaps:
- residual risks:
- follow-up:

Do not use inspection-only review, generated dashboard/site output, route detection, or the presence of this template as completion evidence.
