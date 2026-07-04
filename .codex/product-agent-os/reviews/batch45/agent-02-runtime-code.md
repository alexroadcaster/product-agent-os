# Batch 45 Agent 02 Runtime/Code Review

## Scope

Read-only runtime/code audit for Batch 45 focused on:

- `plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py`
- `.codex/hooks/comment_sufficiency_advisory.py`
- `plugins/product-agent-os/assets/templates/hooks/comment_sufficiency_advisory.py`
- `plugins/product-agent-os/scripts/product_agent_os/automation_policy.py`
- `plugins/product-agent-os/scripts/product_agent_os/self_learning_candidates.py`
- `plugins/product-agent-os/scripts/product_agent_os/self_learning_metrics.py`
- `plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py`
- `plugins/product-agent-os/scripts/product_agent_os/status_dashboard.py`
- `plugins/product-agent-os/scripts/product_agent_os/discovery.py`
- Batch 45 tests named in the review request.

No code, docs, tests, git, hook activation, provider, browser, live server, runtime or automation mutation was performed. The only write was this report.

## Sources read

- `.codex/config.toml`
- `.codex/workflows/task-plan-lifecycle.md`
- `.codex/workflows/review-slice.md`
- `.codex/workflows/coding-standards.md`
- `.codex/workflows/control-plane-sync.md`
- `plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py`
- `.codex/hooks/comment_sufficiency_advisory.py`
- `plugins/product-agent-os/assets/templates/hooks/comment_sufficiency_advisory.py`
- `plugins/product-agent-os/scripts/product_agent_os/automation_policy.py`
- `plugins/product-agent-os/scripts/product_agent_os/self_learning_candidates.py`
- `plugins/product-agent-os/scripts/product_agent_os/self_learning_metrics.py`
- `plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py`
- `plugins/product-agent-os/scripts/product_agent_os/status_dashboard.py`
- `plugins/product-agent-os/scripts/product_agent_os/discovery.py`
- `tests/product_agent_os/test_comment_sufficiency.py`
- `tests/product_agent_os/test_lifecycle_hooks.py`
- `tests/product_agent_os/test_automation_policy.py`
- `tests/product_agent_os/test_self_learning_state.py`
- `tests/product_agent_os/test_batch45_coding_standards.py`
- `tests/product_agent_os/test_batch45_s3_professional_code_authoring.py`
- `tests/product_agent_os/test_coding_standards_artifacts.py`

Memory was used only as orientation for current Batch 45 context; findings below are based on current workspace files and commands.

## Code findings

### P0

No P0 findings found.

### P1

1. Advisory hook can fail closed on parser/read errors even though it claims non-blocking fail-open behavior.

   Evidence:
   - `.codex/hooks/comment_sufficiency_advisory.py:152` calls `warnings = analyze_paths(changed, root=root)` without `try/except`.
   - `plugins/product-agent-os/assets/templates/hooks/comment_sufficiency_advisory.py:152` has the same behavior in the packaged template.
   - `plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py:87-89` reads and `ast.parse`s Python files without catching `OSError`, `UnicodeDecodeError`, or `SyntaxError`.
   - `plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py:111-114` reads JavaScript files without catching file/encoding errors.

   Impact: a syntactically invalid changed Python file, unreadable file, transient encoding issue, or deleted file race can make the PostToolUse advisory exit non-zero. That contradicts the hook's own output contract that warnings are reviewer signals only and "must not be used as blocker proof". Existing tests cover the happy path where the hook returns 0 with advisory warnings, but not analyzer exceptions.

   Recommended fix: wrap the hook's `analyze_paths` call in a narrow fail-open exception handler that emits `status: "validator_error_fail_open"`, `blocking: false`, redacted error class/message, and exits 0. Add focused tests for invalid Python syntax, unreadable/missing file race, and invalid UTF-8.

2. JavaScript comment sufficiency detection misses common modern function forms.

   Evidence:
   - `plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py:114` only matches `function name(`.
   - `tests/product_agent_os/test_comment_sufficiency.py:159-165` tests only a `function complexCase(value) {` fixture.

   Impact: required or complex code written as `export function foo`, `async function foo`, `const foo = (...) =>`, `export const foo = (...) =>`, class methods, or object methods is invisible to the analyzer. This is material for JS runner code because the required-symbol model includes JS names (`evaluateAccess`, `redact`, `normalizeEvent`) and the B45 advisory is meant to reduce comment-noise while preserving intent comments in complex runner code.

   Recommended fix: either use a small JS parser already available in the project/toolchain, or extend the detector conservatively for `export`, `async`, `const/let/var name = (...) =>`, `name(...) {` class/object methods, and named exports. Add tests for each supported form and one unsupported-form fixture that explicitly documents the accepted gap.

### P2

1. `B45_COMMENT_ADVISORY_ROOT` is trusted as an arbitrary scan root and the hook emits raw absolute workspace paths.

   Evidence:
   - `.codex/hooks/comment_sufficiency_advisory.py:13` defines `ROOT_ENV`.
   - `.codex/hooks/comment_sufficiency_advisory.py:21` returns `Path(env_root).resolve()` without containment or existence checks.
   - `.codex/hooks/comment_sufficiency_advisory.py:114` emits `"workspace_root": str(root)`.
   - Template copy has the same behavior at `plugins/product-agent-os/assets/templates/hooks/comment_sufficiency_advisory.py:13`, `:21`, and `:114`.
   - `tests/product_agent_os/test_lifecycle_hooks.py:94` relies on the env override for temp test repos, so the override is intentional but not bounded.

   Impact: a process-level env var can point the advisory at an unrelated git workspace or path outside the intended project, and the JSON output can leak local absolute paths into captured hook logs or reports. This is not an external write/security exploit by itself, but it weakens sandbox/path hygiene and privacy posture.

   Recommended fix: keep the env override for tests, but require `root.exists()` and `root.is_dir()`, return a redacted/hash workspace ref by default, and include a `raw_workspace_path_included: false` policy unless a test-only flag opts in. Consider requiring a `.codex` or `.git` marker for env-root execution.

2. Project-local hook and packaged hook are duplicated source copies without an explicit drift guard.

   Evidence:
   - `.codex/hooks/comment_sufficiency_advisory.py:12-152` and `plugins/product-agent-os/assets/templates/hooks/comment_sufficiency_advisory.py:12-152` are functionally identical copies.
   - `tests/product_agent_os/test_lifecycle_hooks.py:47-62` checks installation and PostToolUse wiring, but does not assert that the project-local hook content matches the packaged template.

   Impact: future edits can fix the packaged hook while leaving the active project-local hook stale, or vice versa. Because this code is advisory/runtime-facing, drift can create false confidence about the actual active path.

   Recommended fix: add a golden drift test comparing normalized content or a content digest between the packaged template and `.codex/hooks/comment_sufficiency_advisory.py`, or move shared behavior into an importable module and keep hook wrappers thin.

3. Automation candidate policy is effective but string-fragile.

   Evidence:
   - `plugins/product-agent-os/scripts/product_agent_os/automation_policy.py:44-53` detects required sections by exact Markdown substrings such as `"Accountable owner:"`, `"## Cadence"`, `"Inputs:"`, and `"Outputs:"`.
   - `plugins/product-agent-os/scripts/product_agent_os/automation_policy.py:231-238` counts manual runs with regexes over free text.
   - `plugins/product-agent-os/scripts/product_agent_os/automation_policy.py:275-288` detects active schedules through substring/regex matching.
   - `plugins/product-agent-os/scripts/product_agent_os/automation_policy.py:320-327` infers owner approval from one `Approval status:` line.

   Impact: small heading wording changes, localized text, multiple approval lines, or reordered sections can change validation results without a schema error. The tests are good for current templates, but the module is brittle as a general policy validator.

   Recommended fix: parse candidate Markdown into a small structured section map first, normalize headings/fields once, and validate that structure. Keep regexes as compatibility helpers behind that parser.

### P3

1. Broad professional-code detection may create noisy `present_unverified` routing.

   Evidence:
   - `plugins/product-agent-os/scripts/product_agent_os/discovery.py:662-678` treats any code suffix (`.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.go`, `.rs`, `.java`, `.cs`) as a professional-code-authoring signal.
   - `plugins/product-agent-os/scripts/product_agent_os/discovery.py:3514-3529` maps that signal into `professional_code_authoring: present_unverified` with required evidence.

   Impact: this is conservative and aligned with "code work needs evidence", but it can also mark routine code-bearing repos as professional-code-authoring contexts even when the specific coding-standards workflow/checklist is absent. That increases advisory/dashboard noise and can dilute signal quality.

   Recommended fix: split detection into `code_surface_present` and `professional_code_authoring_contract_present`; then route code-only projects to `applicable_missing` or a more precise "needs checklist if editing code" state.

2. Several runtime orchestration modules are deep, multi-responsibility files.

   Evidence:
   - `plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py` is 2038 lines and contains schema constants, packet builders, script registry, command execution, redaction policy, first-response routing, and helper utilities.
   - `plugins/product-agent-os/scripts/product_agent_os/discovery.py` is 3598 lines and contains filesystem walking, stack detection, route classification, methodology signals, readiness packets, and CLI entrypoint behavior.
   - `plugins/product-agent-os/scripts/product_agent_os/status_dashboard.py` is 790 lines and mixes renderer, staging/manifest planning, dashboard HTML sections, redaction validation, path safety, and date formatting.

   Impact: current focused tests provide useful coverage, but changes in these files have a wide blast radius. The module size makes it hard to reason about coupling and encourages additional helper growth instead of clearer ownership boundaries.

   Recommended fix: do not rewrite broadly. For the next functional change, extract only along active seams: `first_run_script_matrix`, `first_run_professional_code_summary`, `discovery_signals`, or `status_dashboard_sections`, with characterization tests before extraction.

## Maintainability debt

- `comment_sufficiency.py` has clear small functions, but its JS implementation is regex-only while Python uses AST. That asymmetry should be explicit in docs/tests or closed with a parser-backed approach.
- The hook uses runtime import path mutation (`sys.path.insert(0, ...)`) at `.codex/hooks/comment_sufficiency_advisory.py:53` and template `:53`. This is pragmatic for a standalone hook, but it should restore `sys.path` after import or isolate import loading to reduce side effects in long-lived hook processes.
- `self_learning_candidates.py` centralizes policy constants well, but `PROFESSIONAL_CODE_ALLOWED_UPDATE_TARGETS` at `:14-25` is a hard-coded list that can drift from template registration unless a test asserts parity with `product_agent_os.templates.required_templates()` where applicable.
- `self_learning_candidates.py:396` truncates professional-code findings to 5 after dedupe. This is a reasonable noise cap, but the packet does not expose a suppressed count, so reviewers cannot tell whether six or fifty findings were collapsed.
- `first_run_analysis.py` and `discovery.py` are now core policy/router modules. They need extraction-by-seam, not a broad cleanup, because the existing tests depend on their current packet shapes.

## Test gaps

- Add hook fail-open tests for invalid Python syntax, invalid encoding, unreadable/missing changed file, and analyzer exception.
- Add JS analyzer tests for `export function`, `async function`, arrow functions, class methods, and required-symbol detection in those forms.
- Add packaged-vs-project-local hook drift test for `comment_sufficiency_advisory.py`.
- Add root override/path hygiene tests: invalid `B45_COMMENT_ADVISORY_ROOT`, outside-workspace env root, path redaction in hook JSON.
- Add structured automation-policy parsing tests for reordered sections, duplicated `Approval status`, and localized/non-exact heading variants if those are expected inputs.
- Add suppressed-count coverage for `_professional_code_findings` truncation if the cap remains at 5.

## Recommended code fixes

1. Make `comment_sufficiency_advisory.py` fail open around analyzer execution and report a bounded diagnostic.
2. Expand or replace JS function detection before relying on the advisory for JS runner code.
3. Redact or hash `workspace_root` in hook output and validate env-root overrides.
4. Add drift guard between packaged hook template and project-local active hook.
5. Convert `automation_policy.py` from direct string checks to a tiny normalized Markdown section parser.
6. Split `professional_code_authoring` discovery into signal presence vs contract/checklist presence.
7. Extract only the next touched seam from `first_run_analysis.py` / `discovery.py`; avoid a large architecture rewrite.

## Quick wins

- Wrap `warnings = analyze_paths(changed, root=root)` in `try/except Exception as exc` and emit `status: "validator_error_fail_open"`.
- Add three JS regex alternatives before a parser migration: optional `export`, optional `async`, and `const|let|var name = (...) =>`.
- Add one digest equality test for `.codex/hooks/comment_sufficiency_advisory.py` vs packaged template.
- Add `suppressed_professional_code_finding_count` to candidate packets when `_professional_code_findings` drops findings beyond the first five.
- Replace `"workspace_root": str(root)` with a hash/ref object matching the redaction pattern used elsewhere.

## Commands run

- `Get-Content .codex/config.toml` - exit 0.
- `Get-Content .codex/workflows/task-plan-lifecycle.md`, `review-slice.md`, `coding-standards.md`, `control-plane-sync.md` - exit 0.
- `Select-String C:\Users\user\.codex\memories\MEMORY.md ...` - exit 0, orientation only.
- `git status --short` - exit 0; pre-existing dirty file observed: `.codex/config.toml`.
- `rg --files plugins/product-agent-os scripts tests/product_agent_os .codex/hooks | Select-String ...` - exit 1 because `scripts` path does not exist; still returned the relevant matching files before the path error.
- Multiple `Get-Content` and `Select-String` source/test inspections - exit 0 unless noted above.
- `python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_automation_policy tests.product_agent_os.test_self_learning_state tests.product_agent_os.test_batch45_coding_standards tests.product_agent_os.test_batch45_s3_professional_code_authoring tests.product_agent_os.test_coding_standards_artifacts -v` - exit 0, `Ran 83 tests in 9.130s`, `OK`.
- `Get-Content ... | Measure-Object -Line` for `first_run_analysis.py`, `discovery.py`, `status_dashboard.py` - exit 0.

## Control-plane sync decision

- `REQUIREMENTS.md`: `not_applicable`; review did not change scope or acceptance criteria.
- `PLAN.md`: `not_applicable`; review did not change sequencing.
- `TEST.md`: `not_applicable`; tests were run as review evidence, no command contract change proposed as source truth.
- `EVALS.md`: `not_applicable`; no eval rubric change.
- `RUNLOG.md`: `not_applicable`; detailed handoff is this source-owned review artifact, and root compactness should be preserved.
- `prod_test.md`: `not_applicable`; Batch 39 ledger not touched.

## Confidence

High for `comment_sufficiency.py`, hook behavior, automation policy, self-learning candidate/metrics policy, and the named B45 tests because the source and focused unittest suite were read and executed locally. Medium for `first_run_analysis.py`, `discovery.py`, and `status_dashboard.py` architectural debt because the files are large and review was scoped to Batch 45 runtime/code concerns rather than a full line-by-line audit.

Report path written: `C:\Users\user\Desktop\project\codex_docs\.codex\product-agent-os\reviews\batch45\agent-02-runtime-code.md`.
