# Code Change Contract

Use this compact contract as the default pre-edit generation context for
non-mechanical code work. It records the smallest evidence needed before editing.
Use `.codex/workflows/coding-standards.md` for routing and
`.codex/artifact-templates/coding-standard-checklist.md` for reviewer/reference
detail when it applies.

- `existing_capability`: inspected source, helper, configuration, or dependency and result.
- `smallest_safe_patch`: smallest local change and files deliberately excluded.
- `invariants`: behavior, compatibility, safety, or data constraints that must hold.
- `dependency_decision`: `reuse | no_new_dependency | new_dependency_approval_required` and reason.
- `risk_selected_tests`: risk or invariant mapped to the smallest relevant checks.
- `comment_decision`: `comment_needed | comment_not_needed` and non-obvious intent or reason.
- `performance_applicability`: `required | not_applicable` and affected path or reason.
- `evidence_and_gaps`: `proceed | stop`, current evidence, missing evidence, and accepted gap.
