# Coding Standards Workflow

Source status: project-local system workflow.

## Purpose

Use this workflow for non-mechanical code authoring, refactoring, defect fixes, dependency changes, generated-code edits, and AI-agent handoffs where code-quality, maintainability, dependency, or legacy risk matters.

This is a coding sub-gate. It does not replace Task Brief / Completion Brief lifecycle, planning control, review slice, control-plane sync, security approval, or release gates.

## Applicability

- Use for implementation or refactoring tasks that can change behavior, public contracts, runtime behavior, dependency graph, shared abstractions, generated code, or long-term maintainability.
- Use `not_applicable` for docs-only, formatting-only, read-only research, or tiny mechanical edits; record the reason and reduced evidence path.

## Inputs

- Task row id:
- Source contract:
- Architecture boundary:
- Owned files:
- Forbidden files:
- Existing local patterns:
- Existing test/eval path:
- Checklist artifact: `.codex/artifact-templates/coding-standard-checklist.md`
- Agent task packet:
- Approval requirements:

## Process

1. Classify the work: mechanical, code authoring, refactor, defect fix, dependency change, generated-code edit, legacy modernization, or `not_applicable`.
2. Read the nearest source-of-truth docs, local implementation patterns, existing helpers, public contracts, and tests before proposing code.
3. Run `enterprise_leverage_check` before implementation: delete or reduce code, configure existing behavior, use standard library/language/framework/platform API, reuse current dependency or project helper, write a tiny adapter, write small custom code, or propose a new dependency only when previous options are insufficient and approval is explicit.
4. Record `one_line_candidate` when the behavior can plausibly be implemented by an existing API, helper, selector, query, schema option, CLI flag, config key, or framework primitive.
5. Apply `negative_dependency_rule`: default to no new dependency; justify any new dependency with risk, owner, license/policy fit, rollback, and approval.
6. Apply `deep_module_check` before shared-module, public API, schema, runtime, concurrency, cache, generated-code, or cross-boundary edits.
7. Apply `legacy_seam_check` before refactoring fragile or legacy code; prefer characterization tests, small seams, adapters, or branch-by-abstraction over broad rewrites.
8. Add abstractions only when they remove real duplication, reduce meaningful complexity, or match an existing pattern.
9. Apply `comment_policy`: this is not "comment everything". State machines, algorithms, security/privacy/data/concurrency logic, and functions with non-obvious invariants need a docstring, intent comment, or explicit `comment_not_needed_reason`; avoid comments that repeat code.
10. Update tests, evals, docs, and evidence artifacts before ready/fixed/complete/works claims.

## Outputs

- Completed coding-standard checklist or `not_applicable` reason.
- Selected leverage path and rejected alternatives.
- Dependency decision and approval status.
- Module, public-contract, and legacy risk notes.
- Test/eval evidence or accepted gap.
- Unsupported code-quality claims.
- Handoff notes for reviewer or next agent.

## Evidence Ceiling

- Template registration proves the workflow can be staged; it does not prove runtime activation or code-quality behavior.
- A completed checklist records task evidence; it does not prove implementation correctness without tests, evals, review, runtime evidence, or owner evidence.
- Hooks, skills, subagents, runtime routes, HTML artifacts, and automation need separate approval and verification before active enforcement claims.

## Stop Conditions

- Existing capability scan is missing and custom code or a new dependency is proposed.
- A large rewrite is proposed without reproduction or characterization evidence, seam strategy, rollback, and owner acceptance.
- Code-quality, refactoring, performance, security, or maintainability claims lack current evidence or accepted gaps.
- Raw private research bodies, raw conversation history, secrets, private customer data, or unredacted logs are requested for a handoff.
