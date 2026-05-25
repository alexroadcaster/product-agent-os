# Release Packet

Project: {project_name}
Profile: {profile_name}

## Inputs

- Completed slice:
- Review verdict:
- Verification evidence:
- Release target:
- Approval requirements:

## Process

- Assemble a staged release draft.
- Summarize the pull request scope and user impact.
- Include checks, rollback, residual risks, and approval requirements.
- For backend rollback, include rollback command, manual procedure, data recovery/replay, irreversible side effects, owner approval and residual risk.
- Apply `evidence_before_completion` before any ready claim, completed claim,
  fixed claim, works claim, or release claim.
- Require current command evidence, current eval evidence, current runtime
  evidence, owner evidence, or an explicit test gap before claiming completion.
- If only code or docs were inspected, label the output `inspection-only` and
  list every unsupported completion claim.
- Apply `standards_trigger_policy` for public API, package, SDK, plugin,
  marketplace, release, or governance changes.
- Record SemVer impact as `major`, `minor`, `patch`, or `not_applicable` with
  rationale before release text.
- Use Keep a Changelog categories when relevant: Added, Changed, Deprecated,
  Removed, Fixed, and Security.
- For product behavior changes, require `metric_hardening_when_product_behavior_changes`
  evidence from `.codex/artifact-templates/metric-spec.md` before claiming impact.
- Check the North Star or primary value metric, input metric, counter-metric,
  proxy metric risk, guardrail, qualitative review, privacy classification,
  retention period, data minimization, owner signoff, and post-release review
  evidence.
- Do not claim success from a proxy metric without counter-metric, guardrail,
  qualitative review, and post-release review evidence.
- Keep external actions pending until explicitly approved.

## Outputs

- PR summary:
- Changed files:
- Checks:
- User impact:
- Rollback:
- Backend rollback:
- Rollback command:
- Manual procedure:
- Data recovery/replay:
- Irreversible side effects:
- Residual risks:
- Approval requirements:
- Evidence-before-completion:
  - Gate: `evidence_before_completion`
  - Ready claim:
  - Completed claim:
  - Fixed claim:
  - Works claim:
  - Release claim:
  - Current command evidence:
  - Current eval evidence:
  - Current runtime evidence:
  - Inspection-only:
  - Explicit test gap:
  - Unsupported completion claim:
- Metric hardening:
  - Gate: `metric_hardening_when_product_behavior_changes`
  - Metric spec: `.codex/artifact-templates/metric-spec.md`
  - North Star or primary value metric:
  - Input metric:
  - Counter-metric:
  - Proxy metric risk:
  - Guardrail:
  - Qualitative review:
  - Privacy classification:
  - Retention period:
  - Data minimization:
  - Owner signoff:
  - Post-release review evidence:
- Standards trigger policy:
  - Gate: `standards_trigger_policy`
  - SemVer impact: `major | minor | patch | not_applicable`
  - SemVer rationale:
  - Keep a Changelog categories:
    - Added:
    - Changed:
    - Deprecated:
    - Removed:
    - Fixed:
    - Security:
  - Governance proposal: `.codex/artifact-templates/governance-proposal.md`
  - No forced external activation:

## Verification

- Release packet matches current diff.
- Failed or skipped checks are named.
- Rollback is practical and scoped.
- SemVer impact and Keep a Changelog categories are explicit for release-bound
  public changes, or `not_applicable` has a reason.
- Ready, completed, fixed, works, and release claims cite current evidence, or
  the packet labels them `inspection-only` with an explicit test gap.
- There is no completion claim without current evidence.
- Product impact claims are backed by metric hardening evidence, not a single
  proxy metric.

## Stop Conditions

- Required approval is missing.
- Blocking check failed.
- Residual risk is unacceptable for the release target.
- Completion claim without current evidence.
- Ready claim, completed claim, fixed claim, works claim, or release claim would
  rely on inspection-only evidence without an explicit test gap.
- Product behavior changed but metric hardening, owner signoff, privacy
  classification, retention period, data minimization, qualitative review,
  counter-metric, or post-release review evidence is missing.
- Release-bound public contract changed but SemVer impact, Keep a Changelog
  category, consumer note, or accepted gap is missing.
