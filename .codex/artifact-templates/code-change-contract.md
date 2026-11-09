# Code Change Contract

Source status: project-local active copy of the packaged T25 compact contract.

Use this compact contract as the default pre-edit generation context for
non-mechanical code work. It records the smallest evidence needed before editing.
Use `.codex/workflows/coding-standards.md` for routing and
`.codex/artifact-templates/coding-standard-checklist.md` for reviewer/reference
detail when it applies.

- `existing_capability`: bounded inventory candidates and inspected source/helper/configuration; omitted/stale/unknown is explicit, dynamic references need inspection.
- `smallest_safe_patch`: smallest local change and files deliberately excluded.
- `invariants`: behavior, compatibility, safety, state ownership and applicable interface ordering/error/configuration constraints.
- `dependency_decision`: `reuse | no_new_dependency | new_dependency_approval_required` and reason.
- `risk_selected_tests`: risk mapped to the lowest reliable check, independent oracle and unique regression protection; no artificial RED for behavior-preserving refactors/configuration.
- `comment_decision`: `comment_needed | comment_not_needed` and non-obvious intent or reason.
- `performance_applicability`: `required | not_applicable` and affected path or reason.
- `evidence_and_gaps`: `proceed | stop`, source/config/tool/environment provenance, missing evidence and accepted gap; rerun only on relevant invalidation, never count skipped as passed.
