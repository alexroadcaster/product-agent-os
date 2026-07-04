# B45-PCA-M37-A01 Runtime Validator Retest Audit

Source status: project-local read-only technical review.

Task ID: `B45-PCA-M37-A01-runtime-validator-review-02`
Date: 2026-07-04
Reviewer role: runtime validator audit, no code/test changes.
Scope: `comment_sufficiency.py`, local/template advisory hook, focused tests, M37 remediation packet and `TEST.md`.

## Executive Verdict

The M37 implementation is suitable for a limited local advisory retest of changed Python/JS/TS/TSX files, but it is not sufficient as the only mechanism for repeat refactor-quality testing.

Main reason: the active hook is deliberately fail-open, non-blocking and changed-file scoped. That is appropriate for safety, but repeated refactor-quality testing still needs explicit CLI corpus runs with caps disabled, targeted parser regression fixtures, and reviewer interpretation of warning noise before any stronger quality claim.

Closure level supported by this audit: `local_advisory_retest_candidate_with_gaps`.

Unsupported by this audit: blocker/CI promotion, broad false-positive rate, real AI-agent behavior improvement, browser/runtime/provider/target/git/release/deploy/automation readiness.

## Sources Read

- `plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py`
- `.codex/hooks/comment_sufficiency_advisory.py`
- `plugins/product-agent-os/assets/templates/hooks/comment_sufficiency_advisory.py`
- `tests/product_agent_os/test_comment_sufficiency.py`
- `tests/product_agent_os/test_lifecycle_hooks.py`
- `docs/superpowers/specs/batch45-review-remediation-summary.json`
- `TEST.md`
- Additional routing context: `.codex/config.toml`, `.codex/workflows/task-plan-lifecycle.md`, `.codex/workflows/review-slice.md`, `.codex/workflows/control-plane-sync.md`, `.codex/hooks.json`, `.codex/hooks/hooks.json`.

## Current Behavior Observed

The validator scans `.py`, `.js`, `.mjs`, `.cjs`, `.ts` and `.tsx` paths through `analyze_paths`, dispatching Python files to AST parsing and JS/TS/TSX files to regex-based detection (`comment_sufficiency.py:61-79`, `107-145`). Default broad-scan exclusions skip `tests/`, `docs/superpowers/specs/`, `.docs-tools/` and `site/` unless overridden (`comment_sufficiency.py:29-34`, `281-296`).

Python complexity is heuristic only: functions/classes need comments when they are in the hard-coded required symbol list or when line count is at least 14 and branch count is at least 4; functions named `run_*` are excluded from complexity detection (`comment_sufficiency.py:14-27`, `217-240`).

JS/TS complexity is also heuristic: detection covers a limited set of `function`, `const|let|var = (...) =>`, and class/object method-like patterns, then counts simple branch tokens and braces (`comment_sufficiency.py:132-145`, `244-260`).

The hook runs after tool use and scans only dirty, staged and untracked supported files from git (`comment_sufficiency_advisory.py:95-106`). It exits `0` in normal warning, invalid-root, missing-validator and validator-error paths (`comment_sufficiency_advisory.py:149-179`, `197-216`, `217-235`). `.codex/hooks.json` and `.codex/hooks/hooks.json` include it under `PostToolUse` after `post_tool_use_evidence.py`.

M37 remediation explicitly records local advisory-only hardening, no promotion claim, no runtime/product activation, and unsupported claims for runtime/browser/provider/target/git/release/deploy/automation surfaces (`batch45-review-remediation-summary.json:13-19`, `119-142`, `189-196`). `TEST.md` keeps the same boundary and requires focused unit/doc/diff checks for M37 (`TEST.md:216-230`).

## Findings

### Blocker 1: Hook changed-files strategy is not enough for repeat refactor-quality retest

Evidence: `_changed_paths` only combines `git diff --name-only`, `git diff --cached --name-only` and `git ls-files --others` (`comment_sufficiency_advisory.py:95-106`). If the repo is clean, or if the retest must evaluate an approved historical corpus rather than current dirty files, the hook can produce an advisory success with no meaningful coverage. If more than 20 files are changed, it skips entirely with `skipped_too_many_changed_files` (`comment_sufficiency_advisory.py:181-195`).

Impact: a repeated refactor-quality test that relies on the hook can create false negatives by not scanning the target corpus.

Required hardening before retest: define the retest driver as explicit CLI corpus runs, not hook-only evidence. Use `--include-tests --no-default-excludes --max-warnings-per-file -1 --max-warnings -1` for broad audit passes, then separately run the hook to prove changed-file advisory wiring.

### Blocker 2: Parser is regex-only for TS/TSX and still has known false-negative classes

Evidence: JS/TS/TSX detection is intentionally implemented by regex without a JS parser dependency (`comment_sufficiency.py:132-145`). Current tests cover basic exported async function, exported arrow function and class method forms (`test_comment_sufficiency.py:29-60`; `test_lifecycle_hooks.py:124-152`).

Likely false negatives not covered by current tests:

- `const evaluateAccess: Handler = (...) => {}` because the arrow regex expects `name =`, not `name: Type =`.
- exported declarations with multiline signatures before `{` or `=>`.
- object-property functions such as `const policy = { evaluateAccess(value) { ... } }`.
- class field arrows such as `redact = (value) => { ... }`.
- higher-order exported wrappers where the required symbol is assigned through `memo`, `useCallback`, `pipe`, or similar wrappers.

Impact: TS/TSX coverage exists, but it is not broad enough to support a "runtime validator catches quality gaps in TS/TSX refactors" claim.

Required hardening before retest: add focused negative fixtures for the forms above, decide which are in scope, and record explicit out-of-scope cases if the project keeps regex-only parsing.

### Gap 3: False-positive suppression can be too broad

Evidence: `_has_preceding_comment` treats any non-empty comment in the previous six-line window as sufficient, and `comment_not_needed_reason` anywhere in that scanned line suppresses the warning (`comment_sufficiency.py:264-278`).

Impact: an unrelated nearby comment can suppress a genuinely undocumented complex function. This is a false-negative risk, not a fail-open safety issue.

Recommended hardening: require the nearest non-empty line immediately before the definition to be a comment, doc marker or `comment_not_needed_reason`, or require `comment_not_needed_reason:` to appear in the nearest preceding comment block. Add tests for unrelated comment blocks separated by decorators/imports/assignments.

### Gap 4: Python heuristic has intentional blind spots that need retest wording

Evidence: `_python_looks_complex` returns `False` for any `run_*` function before evaluating line/branch complexity (`comment_sufficiency.py:233-240`). The AST visitor walks top-level and class bodies, but it does not recursively inspect nested functions inside function bodies (`comment_sufficiency.py:93-103`).

Impact: complex `run_*` functions and nested complex functions can be missed. This may be acceptable for advisory noise control, but the retest must not treat absence of warnings as proof that complex Python code is fully documented.

Recommended hardening: add a test documenting the `run_*` exception as accepted behavior or remove/narrow the exception. Add nested-function fixture if nested implementation logic is in scope.

### Gap 5: CLI broad audit can fail hard on malformed Python

Evidence: `analyze_python_file` calls `ast.parse` directly (`comment_sufficiency.py:88-90`). The hook catches validator exceptions and returns fail-open JSON (`comment_sufficiency_advisory.py:197-216`), but the CLI `main` does not wrap `analyze_paths` in a diagnostic fail-open envelope (`comment_sufficiency.py:168-204`).

Impact: broad corpus retests over in-progress refactor files can stop on a single syntax error. That may be correct for a source-quality check, but it should be an explicit retest failure mode rather than a hidden parser limitation.

Recommended hardening: either keep syntax errors as CLI hard failures and document them as retest blockers, or return structured `validator_error` diagnostics from the CLI while preserving non-blocking advisory semantics.

### Gap 6: Path redaction is improved but not a complete privacy boundary

Evidence: validator outside-root display paths are reduced to `<outside-root>/<filename>` (`comment_sufficiency.py:356-362`), hook display paths outside workspace are `<outside-workspace>/<filename>` (`comment_sufficiency_advisory.py:109-116`), and hook error messages replace the resolved root plus `USERPROFILE` (`comment_sufficiency_advisory.py:126-131`). Tests cover no raw temp root in main hook outputs (`test_lifecycle_hooks.py:120-122`, `152`, `169-175`, `194-199`) and outside-root validator path redaction (`test_comment_sufficiency.py:62-79`).

Residual risk: redaction is string replacement, not path-aware canonicalization across case variants, short paths, symlinks, `%HOMEDRIVE%%HOMEPATH%`, `%TEMP%`, or exception messages containing adjacent absolute paths outside `root` and `USERPROFILE`.

Recommended hardening: add a redaction helper test matrix for mixed-case root string, temp paths outside `USERPROFILE`, and exception messages containing multiple absolute paths.

### Gap 7: Self-noise exists in the current validator

Current-run CLI replay over the validator and hook files returned 6 advisory warnings, all in `comment_sufficiency.py`: `analyze_paths`, `analyze_javascript_file`, `_maybe_warn_python`, `_has_preceding_comment`, `_should_skip_path`, `_cap_warnings`. Current-run hook replay over dirty changed files returned 5 visible warnings and 1 suppressed warning, also from `comment_sufficiency.py`.

Impact: this does not block advisory operation, but it lowers reviewer usefulness during retest because the validator flags its own implementation. That is a concrete false-positive/noise issue for repeat testing.

Recommended hardening: either add real intent comments/docstrings where these functions encode policy, or add explicit `comment_not_needed_reason` with tests that the self-audit warning count is expected.

## Existing Test Coverage

Covered:

- TS/TSX suffix dispatch and basic exported function/arrow/class-method detection (`test_comment_sufficiency.py:29-60`, `test_lifecycle_hooks.py:124-152`).
- outside-root path redaction (`test_comment_sufficiency.py:62-79`).
- Python complex function warning and suppression marker (`test_comment_sufficiency.py:80-140`).
- default exclusions and warning caps (`test_comment_sufficiency.py:142-208`).
- CLI exits `0` with advisory warning payload and rejects zero warning cap (`test_comment_sufficiency.py:210-252`).
- active hook matches packaged template and is wired into `PostToolUse` (`test_lifecycle_hooks.py:57-70`).
- hook fail-open on invalid root and validator error without raw root path (`test_lifecycle_hooks.py:154-199`).

Missing or insufficient before repeat refactor-quality retest:

- TS/TSX typed const assignment, multiline signature, class field arrow, object property method, exported wrapper forms.
- JS brace counting with braces in strings/comments/template literals.
- unrelated preceding comments that should not suppress warnings.
- nested Python functions and `run_*` exception behavior.
- clean-tree hook result and `>20` changed-files skip as explicit retest non-coverage.
- CLI syntax-error behavior over broad corpus.
- redaction matrix beyond root and `USERPROFILE`.

## Commands Run In This Audit

```powershell
python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks -v
```

Result: exit code `0`; 26 tests ran; `OK`.

```powershell
python plugins\product-agent-os\scripts\product_agent_os\comment_sufficiency.py plugins\product-agent-os\scripts\product_agent_os\comment_sufficiency.py .codex\hooks\comment_sufficiency_advisory.py plugins\product-agent-os\assets\templates\hooks\comment_sufficiency_advisory.py --root . --max-warnings-per-file -1 --max-warnings -1
```

Result: exit code `0`; 6 advisory warnings, all in `plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py`.

```powershell
python .codex\hooks\comment_sufficiency_advisory.py
```

Result: exit code `0`; `status=advisory_complete`; `changed_file_count=6`; `scanned_paths` were current dirty Python hook/test/runtime files; validator returned 5 visible warnings and 1 suppressed warning, all in `comment_sufficiency.py`.

```powershell
git status --short
```

Result: exit code `0`; worktree already contains multiple B45/M37 modified files plus untracked `.codex/product-agent-os/reviews/` and `docs/superpowers/specs/batch45-review-remediation-summary.json`. This audit did not revert or normalize unrelated dirty files.

## Recommended Commands Before Retest

Focused implementation checks:

```powershell
python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks -v
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
python tools\check_docs.py
git diff --check -- .codex/hooks/comment_sufficiency_advisory.py .codex/product-agent-os/lifecycle-state.json docs/product-agent-os/coding-standards.md docs/product-agent-os/coding-standards.en.md docs/sources/registry.md docs/sources/registry.en.md docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md PLAN.md EVALS.md TEST.md docs/superpowers/specs/batch45-review-remediation-summary.json plugins/product-agent-os/assets/templates/hooks/comment_sufficiency_advisory.py plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py tests/product_agent_os/test_comment_sufficiency.py tests/product_agent_os/test_lifecycle_hooks.py tests/product_agent_os/test_coding_standards_artifacts.py
```

Retest-specific corpus checks:

```powershell
python plugins\product-agent-os\scripts\product_agent_os\comment_sufficiency.py <approved-refactor-corpus-paths> --root . --include-tests --no-default-excludes --max-warnings-per-file -1 --max-warnings -1
python .codex\hooks\comment_sufficiency_advisory.py
```

The second command proves changed-file hook wiring only. It must not replace the explicit corpus CLI run.

## Retest Suitability

Suitable now:

- local advisory smoke retest;
- changed-file hook wiring retest;
- basic TS/TSX coverage retest;
- fail-open and no-raw-root-path regression retest.

Not suitable yet without hardening or accepted gaps:

- broad false-positive/false-negative rate claim;
- TS/TSX parser completeness claim;
- refactor-quality blocker or CI enforcement claim;
- clean-tree or large-change retest relying only on hook output;
- real AI-agent quality improvement claim.

## Concrete Hardening Backlog

1. Add TS/TSX fixtures for typed const assignment, multiline signatures, class field arrows, object-property methods and exported wrappers; decide in-scope vs accepted limitation.
2. Add suppression-precision tests for unrelated preceding comments and tighten `_has_preceding_comment` if the current broad suppression is not intended.
3. Add explicit tests/documentation for `run_*` and nested Python function behavior.
4. Decide CLI syntax-error contract for broad corpus retests and test it.
5. Add redaction tests for non-`USERPROFILE` absolute temp paths and case variants.
6. Reduce self-noise in `comment_sufficiency.py` with intent comments/docstrings or explicit `comment_not_needed_reason`.
7. Add retest protocol text that the hook is changed-file advisory only and broad retest evidence must come from explicit CLI corpus runs.

## Control-Plane Sync Decision

- `REQUIREMENTS.md`: `not_applicable`; audit did not change scope or acceptance.
- `PLAN.md`: `not_applicable`; audit artifact only, no sequencing change.
- `TEST.md`: `not_applicable`; recommended commands are recorded in this review artifact, but no root verification route changed.
- `EVALS.md`: `not_applicable`; no eval threshold or claim ceiling changed.
- `RUNLOG.md`: `handoff_required_not_updated`; root runlog is near budget per M37 packet and this detailed audit belongs in the review artifact.
- `prod_test.md`: `not_applicable`; Batch 39 surface not touched.

## Next Recommended Role

Builder/tester for focused hardening if repeat refactor-quality testing is requested. Until then, keep M37 as advisory-only local hardening with explicit gaps.
