# Coding Standard Checklist

Source status: project-local system artifact template.

## Purpose

Use this checklist for non-mechanical code authoring, refactoring, defect fixes, dependency changes, generated-code edits, and AI-agent handoffs that can create technical debt.

For docs-only, formatting-only, read-only research, or tiny mechanical edits, record `not_applicable` with the reason and reduced evidence path.

## Applicability

- Task row id:
- Task classification:
- Code surfaces:
- Owner:
- Related workflow: `.codex/workflows/coding-standards.md`
- `not_applicable` reason:
- Reduced evidence path:

## Enterprise Leverage Check

One line that uses an existing capability is preferred over fifty lines of custom code that create dependency, test, and legacy burden.

- `enterprise_leverage_check`:
- `existing_capability_scan`:
- Existing local patterns inspected:
- Existing tests/evals inspected:
- Source files read:
- Delete or reduce code option:
- Configuration option:
- Standard library or language construct option:
- Framework or platform API option:
- Current dependency option:
- Project helper or existing abstraction:
- Existing CLI/tooling option:
- `one_line_candidate`:
- Selected leverage path: `delete | configure | stdlib | language_construct | framework_api | platform_api | current_dependency | project_helper | tiny_adapter | small_custom_code | new_dependency | not_applicable`
- Rejected options and reasons:
- Why custom code is still needed:
- Maximum new custom-code surface:

## Dependency Decision

- `negative_dependency_rule`:
- Existing dependency can solve it:
- Standard library/framework can solve it:
- New dependency requested:
- Dependency owner:
- Transitive/runtime/security risk:
- License or policy concern:
- Install/build/runtime impact:
- Rollback/removal path:
- Approval requirement:
- Accepted dependency gap:

## Module And Legacy Safety

- `deep_module_check`:
- Public API or contract touched:
- Callers/consumers inspected:
- Error paths inspected:
- State, concurrency, cache, or migration risk:
- `legacy_seam_check`:
- Characterization test or existing regression evidence:
- Refactoring pattern: `small_safe_refactor | strangler | branch_by_abstraction | adapter | not_applicable`
- No big rewrite check:
- Compatibility impact:
- Rollback path:

## Code Style And Comments

- Naming/style source:
- Formatter/linter source:
- Local idioms followed:
- `comment_policy`:
- Comments added only for non-obvious intent, tradeoff, invariant, security, data, migration, concurrency, or compatibility risk:
- Obvious comments avoided:
- `cleverness_budget`:
- Simpler alternative considered:
- Abstraction added:
- Abstraction removal or inline option considered:

## Test And Evidence

- Test-first or eval-first path:
- Deterministic tests:
- Contract tests:
- Fixture or behavioral eval:
- Runtime/manual evidence:
- Commands to run:
- Expected output:
- Evidence owner:
- Current evidence:
- Missing evidence:
- Accepted gap:
- `unsupported_code_quality_claims`:

## Completion Gate

- Ready/fixed/complete/works claim:
- Evidence supporting the claim:
- Unsupported claim blocked:
- Fallback allowed:
- Fallback status: `product_intended | compatibility_only | forbidden | not_applicable`
- Activation proof needed:
- Negative proof needed:
- Closure level:

## Stop Conditions

- `enterprise_leverage_check` is missing for non-mechanical code work.
- `existing_capability_scan` is missing and new custom code or a new dependency is proposed.
- `one_line_candidate` is not considered for a small utility behavior.
- `negative_dependency_rule` is missing before adding a dependency.
- `deep_module_check` is missing before touching shared modules, APIs, data models, runtime contracts, or generated code.
- `legacy_seam_check` is missing before refactoring legacy or fragile code.
- Tests/evals are missing and no explicit accepted gap exists.
- Raw private research bodies, raw chat history, secrets, private customer data, or unredacted logs are required.
