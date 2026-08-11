# Coding Standards Workflow

Project: {project_name}
Profile: {profile_name}
Detected stack: {detected_stack_text}

## Purpose

Use this workflow for non-mechanical code authoring, refactoring, defect fixes, dependency changes, generated-code edits, and AI-agent handoffs where code-quality, maintainability, dependency, or legacy risk matters.

The workflow routes the professional code authoring standard. Its default generation
context is `.codex/artifact-templates/code-change-contract.md`; use the retained
checklist only as reviewer/reference material and reference this workflow from
`.codex/artifact-templates/agent-task-packet.md` when needed.

## Applicability

- Use for implementation or refactoring tasks that can change behavior, public contracts, runtime behavior, dependency graph, shared abstractions, generated code, or long-term maintainability.
- Use `not_applicable` for docs-only, formatting-only, read-only research, or tiny mechanical edits; record the reason and reduced evidence path.
- This workflow is a coding sub-gate. It does not replace the task lifecycle, planning control, review slice, control-plane sync, security approval, or release gates.

## Inputs

- Task row id:
- Source contract:
- Architecture boundary:
- Owned files:
- Forbidden files:
- Existing local patterns:
- Existing test/eval path:
- Default generation context: `.codex/artifact-templates/code-change-contract.md`
- Agent task packet:
- Approval requirements:

For reviewer/reference detail, use `.codex/artifact-templates/coding-standard-checklist.md`.

## Process

1. Classify the work: mechanical, code authoring, refactor, defect fix, dependency change, generated-code edit, legacy modernization, or `not_applicable`.
2. Read the nearest source-of-truth docs, local implementation patterns, existing helpers, public contracts, and tests before proposing code.
3. Run the `enterprise_leverage_check` before implementation:
   - delete or reduce code,
   - configure existing behavior,
   - use the standard library or language construct,
   - use the framework/platform API,
   - use a current dependency,
   - reuse a project helper or existing abstraction,
   - write a tiny adapter,
   - write small custom code,
   - propose a new dependency only when the previous options are insufficient and approval is explicit.
4. Record a `one_line_candidate` when the requested behavior can plausibly be implemented by an existing API, helper, selector, query, schema option, CLI flag, config key, or framework primitive.
5. Apply the `negative_dependency_rule`: default to no new dependency; justify any new dependency with risk, owner, license/policy fit, rollback, and approval.
6. Apply `deep_module_check` before shared-module, public API, schema, runtime, concurrency, cache, generated-code, or cross-boundary edits.
7. Apply `legacy_seam_check` before refactoring fragile or legacy code; prefer characterization tests, small seams, strangler patterns, adapters, or branch-by-abstraction over big rewrites.
8. Keep the implementation boring, local, and reviewable. Add abstractions only when they remove real duplication or match an existing pattern.
9. Apply `comment_policy`: this is not "comment everything". State machines, algorithms, security/privacy/data/concurrency logic, and functions with non-obvious invariants need a docstring, intent comment, or explicit `comment_not_needed_reason`; avoid obvious comments that repeat code.
10. Apply `cleverness_budget`: choose the simplest readable solution that satisfies the contract; record why any clever or generic solution is justified.
11. Update tests, evals, docs, and evidence artifacts before making ready/fixed/complete/works claims.

## Outputs

- Completed compact code-change contract or `not_applicable` reason.
- Reviewer/reference checklist when the task needs its additional detail.
- Selected leverage path and rejected alternatives.
- Dependency decision and approval status.
- Module, public-contract, and legacy risk notes.
- Test/eval evidence or accepted gap.
- Unsupported code-quality claims.
- Handoff notes for reviewer or next agent.

## Review Gate

- `enterprise_leverage_check` exists for non-mechanical code work.
- `existing_capability_scan` names concrete files, helpers, framework APIs, dependencies, or source docs inspected.
- `one_line_candidate` is recorded or explicitly not applicable.
- `negative_dependency_rule` is recorded before any new dependency is proposed.
- `deep_module_check` exists for shared, public, runtime, generated, data, or cross-boundary edits.
- `legacy_seam_check` exists for legacy/refactoring work.
- `comment_policy` and `cleverness_budget` are recorded for code-quality claims.
- Tests/evals or accepted gaps are tied to each code-quality claim.
- Unsupported completion or code-quality claims are listed.

## Evidence Ceiling

- Template registration proves the workflow can be staged; it does not prove runtime activation or code-quality behavior.
- A completed checklist proves task evidence was recorded; it does not prove the implementation is correct without tests, evals, review, runtime evidence, or owner evidence.
- Hooks, skills, subagents, runtime routes, HTML artifacts, and automation need separate approval and verification before they can be treated as active enforcement.

## Stop Conditions

- Stop if this workflow becomes a parallel lifecycle system instead of a coding sub-gate.
- Stop if the task needs a new dependency without explicit dependency evidence and approval.
- Stop if implementation starts before existing capability scan and local pattern inspection.
- Stop if a large rewrite is proposed without characterization evidence, seam strategy, rollback, and owner acceptance.
- Stop if code-quality, refactoring, performance, security, or maintainability claims lack current evidence or accepted gaps.
- Stop if raw private research bodies, raw conversation history, secrets, private customer data, or unredacted logs are requested for a handoff.
