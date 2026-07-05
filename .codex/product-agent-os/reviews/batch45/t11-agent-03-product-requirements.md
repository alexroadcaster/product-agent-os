# B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN - Product Requirements

Source status: source-owned product requirements packet based on current Batch 45 packets; inspection-only, no live/model/provider/runtime/browser/target/git/CI/automation action performed.

## Product Decision

Treatment v3 should solve one narrow product problem: make Professional Code Authoring guidance useful to the agent at the moment it plans and reviews code, without adding a broad generation-time prompt overlay that increases cognitive load, latency, timeout risk, or generic compliance text.

The current Batch 45 decision remains `advisory_only_no_go`. M26/M27/M35 do not prove real AI-agent behavior improvement, CI/blocker readiness, runtime/browser readiness, or target-apply safety. T11 is therefore only a source design requirements slice for a future treatment candidate.

## Source Basis

| Source | Product claim used | Confidence | Boundary |
| --- | --- | --- | --- |
| `docs/superpowers/specs/batch45-postq4-architecture-next-actions.json` | T11 is optional P2 `source_only_design` before a future behavior rerun; v3 should reduce prompt friction and map standards to behaviors, negative examples, and reviewer checks. | High | No implementation or proof. |
| `docs/superpowers/specs/batch45-post-q4-next-tasks.json` | T11 depends on T08 and must not activate hooks, CI, blocker enforcement, or live/model calls. | High | Future eval plan update is required before any run. |
| `docs/superpowers/specs/batch45-comment-policy-promotion-decision.json` | M27 kept M25 local, non-blocking, reversible and rejected stronger advisory/CI/blocker promotion after M26 no-go. | High | Does not approve promotion. |
| `docs/superpowers/specs/batch45-real-project-decision-packet.json` | M35 selected no-go for treatment v2 promotion; smaller treatment may be source-only future design. | High | Does not approve target apply or runtime/browser pilot. |
| `docs/product-agent-os/coding-standards.md` | Professional Code Authoring value is senior leverage: check existing capability, prefer delete/reuse/native/configuration, avoid shallow wrappers and noisy comments. | High | Evidence ceiling remains docs_contract_ready / synthetic_green unless later approved evidence exists. |

## Product Goal

Create a treatment v3 design that helps agents choose smaller, higher-leverage code changes by turning Professional Code Authoring into decision scaffolding:

- prompt the agent to inspect existing capabilities before custom implementation;
- favor deletion, reuse, native/library/framework paths, and configuration over new code;
- require concise rationale only where it changes the decision;
- move most quality pressure to reviewer/checklist behavior instead of stuffing every rule into generation-time context;
- preserve source-only status until a future eval packet proves behavior improvement.

## User Value

For the project owner, treatment v3 should make future agent runs easier to judge and less likely to create code churn. The value is not "more standards in the prompt"; the value is better observable decisions:

- the agent can name the existing path it checked before writing code;
- the agent can explain why a smaller/native/deletion option was rejected;
- reviewer output can identify concrete missed leverage, shallow abstraction, dependency risk, or comment noise;
- future evals can compare behavior quality instead of merely counting warning reduction;
- no target project, runtime, provider, CI, or automation surface is touched by design work.

## Non-Goals

- Do not claim treatment v3 improves real AI-agent behavior until a later approved paired eval proves it.
- Do not run live/model/provider/API calls.
- Do not launch runtime/live server or browser automation.
- Do not run commands in or mutate SOL, myPartners, or any other target workspace.
- Do not create CI, blocker enforcement, hooks activation, schedules, automations, release, deploy, publish, branch, commit, push, or PR.
- Do not replace human review.
- Do not make comment-sufficiency warning reduction a proxy for product quality.
- Do not import the full coding standards document into every generation prompt.
- Do not turn Professional Code Authoring into generic "write better code" prose without observable behavior checks.

## Requirement Slice

| Requirement ID | Requirement | Rationale | Acceptance behavior | Evidence owner |
| --- | --- | --- | --- | --- |
| `T11-PR-01` | Treatment v3 must be source-only and explicitly carry the current advisory-only/no-go ceiling. | M26/M27/M35 block promotion claims. | Given the v3 design is reviewed, when it describes status, then it says `source_only_design` and does not state readiness, promotion, or proven behavior improvement. | Product Manager / Reviewer |
| `T11-PR-02` | Treatment v3 must optimize for decision leverage, not prompt volume. | M26 treatment underperformed despite warning reduction; overprompting is a plausible failure mode. | Given a task prompt needs v3 guidance, when the guidance is applied, then it asks for the smallest relevant existing-capability scan and one concise decision rationale, not the full standards body. | Product Manager / Architect |
| `T11-PR-03` | Treatment v3 must map standards to concrete behaviors and negative examples. | Future evals need observable behavior, not principle labels. | Given a Professional Code Authoring gate applies, when v3 defines it, then it names the desired behavior, a common bad pattern, and a reviewer check. | Product Manager / Tester |
| `T11-PR-04` | Treatment v3 must separate authoring scaffolding from reviewer enforcement. | Reviewer checks can catch missed leverage without burdening generation. | Given the agent authors code, when v3 is used, then generation-time guidance stays compact and reviewer-time checks carry the fuller checklist. | Product Manager / Architect |
| `T11-PR-05` | Treatment v3 must define promotion boundaries before any future run. | Static quality and advisory wiring cannot substitute for behavior proof. | Given a future owner wants to run v3, when the approval packet is prepared, then it names paired baseline/treatment tasks, timeout handling, reviewer timing, cost/privacy boundaries, and no-promotion conditions. | Product Manager / Tester |

## Acceptance Behaviors

1. Source-only status is visible.
   - Given a reader opens the v3 requirements packet, when they look for status, then they see that T11 is design-only and does not reverse M26/M27/M35 no-go.
   - Check: review packet inspection.
   - Evidence owner: Product Manager.

2. Prompt friction is reduced.
   - Given a future treatment prompt is drafted, when it uses v3, then it includes only the task-relevant leverage gates and a compact decision rubric, not a pasted standards manual.
   - Check: future prompt diff against v3 design.
   - Evidence owner: Architect / Tester.

3. Standards become behavior checks.
   - Given `enterprise_leverage_check`, `existing_capability_scan`, `one_line_candidate`, `negative_dependency_rule`, `deep_module_check`, `legacy_seam_check`, `comment_policy`, or `cleverness_budget` applies, when v3 describes the gate, then it includes expected behavior, unacceptable shortcut, and reviewer question.
   - Check: source design review.
   - Evidence owner: Product Manager / Reviewer.

4. Warning reduction is not treated as success.
   - Given a future eval sees fewer advisory warnings, when promotion is considered, then behavior score, reviewer decision, regressions, timeout handling, and runtime/target boundaries remain separate gates.
   - Check: future eval plan and decision packet.
   - Evidence owner: Tester / Reviewer.

5. Approval-gated surfaces stay closed.
   - Given T11 completes, when the artifact is inspected, then it contains no claim of live/model/provider/runtime/browser/target/git/CI/automation execution or authorization.
   - Check: review packet inspection.
   - Evidence owner: Product Manager.

## Risk Of Overprompting

Treatment v3 should treat overprompting as a first-class product risk. The failure mode is that agents spend context and attention on generic standards text, then produce slower, more verbose, or less task-specific changes. M26 already shows that fewer advisory warnings did not translate into better aggregate behavior, so v3 must avoid assuming that more guidance equals better code.

Controls:

- use short gate names plus task-specific decision questions instead of long policy prose;
- include only gates triggered by the current task type;
- move exhaustive checks to reviewer/checklist phase;
- prefer negative examples and before/after decision patterns over broad principles;
- measure future success by paired behavior outcomes, not prompt completeness or warning count alone.

## Promotion Boundaries

Treatment v3 can be promoted only after a separate approved evidence route. Current T11 output may support future planning, but not activation.

Required before any stronger claim:

- owner-approved future eval packet;
- paired baseline/treatment comparison with timeout handling defined before the run;
- independent reviewer decision that is not `no_go`;
- evidence that treatment v3 improves task outcomes without critical regressions;
- false-positive/flake/cost/privacy review for the exact promoted surface;
- rollback/disable path for any advisory, hook, CI, blocker, or automation route;
- separate approval and evidence for runtime/browser/target/provider/git/CI/automation if those surfaces are involved.

Forbidden from T11 alone:

- `real_ai_agent_behavior_improvement_claimed`;
- `ci_wiring_promoted`;
- `blocker_enforcement_promoted`;
- `active_automation_promoted`;
- `target_workspace_apply_approved`;
- `runtime_browser_readiness_claimed`;
- `release_deploy_publish_ready`.

## Assumptions

- The next consumer is likely Architect or Tester preparing a compact treatment v3 source design or future eval packet.
- The owner wants product clarity and acceptance boundaries, not implementation in this slice.
- Existing Batch 45 no-go decisions remain active unless a later approved evidence packet reverses them.

## Product Risks

- A v3 prompt may still be too broad if it tries to cover every coding standard in every task.
- A future static-only win may again be mistaken for behavior improvement.
- Reviewer checks may become subjective unless mapped to concrete examples and eval scoring.
- If future live eval timeout policy is not redesigned first, v3 could remain unmeasured even if the design is better.

## Verification Expectations

For this packet: inspection-only source review is sufficient because T11 is requirements/design-only.

For future v3 proof: verification must be a separate approved route with behavior eval evidence, reviewer evidence, and explicit no-promotion boundaries. Runtime/browser/target/provider/git/CI/automation evidence remains approval-required and unavailable from this packet.

## Control-Plane Sync Decision

- `REQUIREMENTS.md`: `handoff_required` only if owner wants this T11 slice promoted into root current scope; not updated in this task because the user allowed only this review packet.
- `PLAN.md`: `handoff_required` if T11 becomes the selected next queue item after this requirements packet.
- `TEST.md`: `not_applicable` for this source-only requirements artifact; future eval route must update verification expectations.
- `EVALS.md`: `handoff_required` before any treatment v3 behavior run.
- `RUNLOG.md`: `handoff_required` due compactness and user write-scope restriction.
- `prod_test.md`: `not_applicable`.

## Recommended Next Role

Architect should translate these product requirements into a compact treatment v3 source design. Tester should then update the future eval plan before any approved live/model/provider run.
