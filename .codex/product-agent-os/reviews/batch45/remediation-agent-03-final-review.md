# Batch 45 Remediation Final Review

Source status: independent verifier report.

Review date: 2026-07-04
Role: review/verifier
Mode: local read-only inspection plus allowed local tests; only write is this report.

## Scope

Reviewed the Batch 45 remediation diff after the six prior audit reports, focusing on:

- hook/validator fail-open and no absolute path/privacy behavior;
- TS/TSX and modern JS detection coverage;
- lifecycle-state M37 marker and no-go boundaries;
- docs/control-plane/source registry consistency;
- tests that actually guard new behavior;
- unsupported runtime/browser/provider/target/git/release/automation claims.

No code, docs, tests, git state, browser/provider/live API, target workspace command, hook activation, automation, release, deploy or publication action was performed.

## Diff Reviewed

Changed tracked files at final inspection:

- `.codex/config.toml`
- `.codex/product-agent-os/lifecycle-state.json`
- `EVALS.md`
- `PLAN.md`
- `TEST.md`
- `docs/product-agent-os/coding-standards.md`
- `docs/product-agent-os/coding-standards.en.md`
- `docs/sources/registry.md`
- `docs/sources/registry.en.md`
- `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`
- `docs/superpowers/specs/batch45-review-remediation-summary.json`
- `plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py`
- `tests/product_agent_os/test_coding_standards_artifacts.py`

Untracked review directory existed before this report:

- `.codex/product-agent-os/reviews/batch45/agent-01-architecture-lifecycle.md`
- `.codex/product-agent-os/reviews/batch45/agent-02-runtime-code.md`
- `.codex/product-agent-os/reviews/batch45/agent-03-verification-evals.md`
- `.codex/product-agent-os/reviews/batch45/agent-04-docs-source-sync.md`
- `.codex/product-agent-os/reviews/batch45/agent-05-security-privacy-approvals.md`
- `.codex/product-agent-os/reviews/batch45/agent-06-product-scenarios-scorecard.md`

## Findings

### P0

No P0 found. I did not find a new claim that Batch 45 is release-ready, CI/blocker-promoted, runtime/browser/provider/target/git/deploy/automation verified, or behavior-improvement proven.

### P1

#### P1-1: M37 remediation checks fail and one referenced handoff artifact is still missing

Evidence:

- `docs/superpowers/specs/batch45-review-remediation-summary.json` now exists and is referenced from `docs/product-agent-os/coding-standards.md:5`, `.en.md:5`, `docs/sources/registry.md:72`, and `docs/sources/registry.en.md:72`.
- `.codex/product-agent-os/lifecycle-state.json:35` still lists `.codex/product-agent-os/reviews/batch45/remediation-agent-02-docs-control-plane.md` as completion evidence.
- `docs/sources/registry.md:72`, `docs/sources/registry.md:1593`, `docs/sources/registry.en.md:72`, and `docs/sources/registry.en.md:1594` also route to `.codex/product-agent-os/reviews/batch45/remediation-agent-02-docs-control-plane.md`.
- Current check: `Test-Path` returned `True` for `docs/superpowers/specs/batch45-review-remediation-summary.json` and `False` for `.codex/product-agent-os/reviews/batch45/remediation-agent-02-docs-control-plane.md`.
- `python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v` failed 3 assertions in the updated M37/public-docs tests.
- Failures: missing serialized strings `m36 remains reserved`, `promotion remains no_go/advisory-only`, and missing exact public-doc sentence `does not prove that ai agents now write enterprise-quality code in real projects`.

Impact: the new M37 validation suite is red, and source registry/lifecycle still point to a missing handoff artifact. This blocks closure of M37/source-sync claims.

Smallest repair: add the missing `remediation-agent-02-docs-control-plane.md` or remove/downgrade the references, then fix either the tests or the source text so the intended M37/no-go strings are consistently represented.

#### P1-2: The core fail-open/privacy/import findings are still unfixed in the active hook path

Evidence:

- `.codex/hooks/comment_sufficiency_advisory.py:152` still calls `warnings = analyze_paths(changed, root=root)` without a fail-open exception handler.
- Packaged template has the same call at `plugins/product-agent-os/assets/templates/hooks/comment_sufficiency_advisory.py:152`.
- `plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py:88-90` still reads and parses Python with `read_text` plus `ast.parse` without handling `OSError`, `UnicodeDecodeError` or `SyntaxError`.
- `plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py:113` still reads JS/TS text without handling file/encoding errors.
- Custom probe against invalid Python returned `SyntaxError invalid syntax (broken.py, line 1)`, proving the analyzer can still raise.
- `.codex/hooks/comment_sufficiency_advisory.py:114` and packaged template `:114` still emit `"workspace_root": str(root)`.
- `.codex/hooks/comment_sufficiency_advisory.py:53` and packaged template `:53` still insert a workspace-discovered scripts path into `sys.path`; validator-source trust is not pinned or allowlisted.

Impact: the original high-value runtime/security remediation targets are not closed. A malformed or unreadable changed file can still break the non-blocking advisory path, hook output can still retain absolute local paths, and target/workspace import trust remains ambiguous.

Smallest repair: wrap the hook analyzer call in fail-open handling, redact/hash workspace paths by default, validate or allowlist validator import source, and mirror the fix in the packaged template with focused tests.

#### P1-3: Lifecycle marker says code/comment-sufficiency changes were forbidden, but the diff changes `comment_sufficiency.py`

Evidence:

- `.codex/product-agent-os/lifecycle-state.json:6` says `Forbidden: hook/code/comment-sufficiency changes`.
- The actual diff changes `plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py:28`, `:77`, and `:132-150` to add TS/TSX suffixes and a modern JS/TS detector.

Impact: the lifecycle approval boundary contradicts the implemented diff. That weakens M37 approval/readiness evidence and makes it unclear whether the code change was inside the authorized remediation slice.

Smallest repair: either update the lifecycle marker and source packet to truthfully include this code change with its test gates, or move the code change into a separately approved/code-owned remediation slice.

#### P1-4: M37 no-unapproved-actions packet contradicts the actual diff

Evidence:

- `docs/superpowers/specs/batch45-review-remediation-summary.json:78` records `"hook_or_code_files_changed": false`.
- `docs/superpowers/specs/batch45-review-remediation-summary.json:80` records `"comment_sufficiency_tests_changed": false`.
- The actual tracked diff changes `plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py:28`, `:77`, and `:132-150`.
- `tests/product_agent_os/test_coding_standards_artifacts.py` was also changed to add M37 assertions.

Impact: the summary packet's no-unapproved-actions ledger is not accurate for the current worktree. This is a source-integrity issue even if the code change was made by another implementer in parallel.

Smallest repair: reconcile the packet with the final diff, or split the code/test changes into a separate slice with its own approval boundary and evidence.

### P2

#### P2-1: TS/TSX and modern JS detection was added but not guarded by committed tests

Evidence:

- `plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py:28` adds `.ts` and `.tsx` to the scanned suffixes.
- `plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py:132-150` adds detection for `export/default/async function`, arrow functions and class/object-style methods.
- `tests/product_agent_os/test_comment_sufficiency.py:159-165` still covers only the old `.mjs` `function complexCase(value)` path.
- Search found no focused committed tests for `export function`, `async function`, arrow functions, `.ts`, `.tsx`, fail-open exceptions, path redaction, or `B45_COMMENT_ADVISORY_ROOT` trust behavior in the Batch 45 comment/hook tests.
- The new committed test coverage is for M37 docs/control-plane linkage in `tests/product_agent_os/test_coding_standards_artifacts.py:163-234`, not for the new comment-sufficiency analyzer behavior.

Impact: custom probes show the new detector can warn on simple TS/TSX examples, but there is no regression gate for the new behavior. Future edits can silently drop TS/TSX coverage.

Smallest repair: add tests for `.ts`, `.tsx`, `export function`, `async function`, `const name = (...) =>`, class methods, and one documented unsupported form.

#### P2-2: Existing tests pass, but they do not validate the new remediation claims

Evidence:

- Earlier `python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_coding_standards_artifacts -v` passed before the M37 test update.
- After the late M37 test update, `python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v` failed 3 assertions.
- `python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks -v` passed 20 tests.
- `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` passed 99 tests.
- `python tools\check_docs.py` passed.
- `git diff --check` passed, with CRLF replacement warnings for `docs/sources/registry*.md`.

Impact: the current green checks validate existing contracts and docs structure, but not the newly claimed remediation behaviors: missing evidence files, fail-open, absolute-path redaction, import-source trust, and modern JS/TS analyzer coverage.

Smallest repair: extend the relevant tests before accepting the remediation as closed.

#### P2-3: Public docs and registry remain conservative on no-go boundaries, but overstate M37 evidence freshness

Evidence:

- `docs/product-agent-os/coding-standards.md:57` and `.en.md:57` correctly state M26/M27/M35/M37 do not prove real-project code quality improvement.
- `docs/sources/registry.md:72` and `.en.md:72` correctly preserve no runtime/browser/provider/target/git/release/deploy/automation action or promotion claim.
- The same lines claim high-trust M37 docs/source/control-plane/test evidence through missing artifacts.

Impact: unsupported runtime/release claims are not introduced, but the evidence route is not source-backed until the referenced M37 artifacts exist.

Smallest repair: keep the no-go wording, but make the M37 source reference real or explicitly mark it missing/handoff-required.

### P3

#### P3-1: `.codex/config.toml` concurrency/runtime changes are unrelated to the requested remediation focus

Evidence:

- `.codex/config.toml` changes `max_threads` from `3` to `6` and `job_max_runtime_seconds` from `1800` to `3000`.

Impact: this may be intentional implementer coordination, but it does not remediate any Batch 45 finding and should not be counted as evidence for hook, validator, docs, test or no-go closure.

Smallest repair: document why this config change belongs in the slice, or keep it separate from remediation readiness claims.

## Spec Compliance

Partial.

Compliant:

- No new runtime/browser/provider/target/git/release/deploy/automation readiness claim found.
- Public docs preserve no-go/advisory-only boundaries.
- RU/EN coding-standards and registry edits are broadly parity-aligned.

Not compliant / incomplete:

- Lifecycle evidence references missing files.
- Lifecycle boundary contradicts the code change.
- Required hook fail-open/privacy/import-source remediation remains open.
- New TS/TSX detector lacks committed focused tests.
- The final source packet/report claimed by docs/registry/lifecycle is absent.

## Architecture Risk

Medium. The code change is small and conservative, but the architecture risk is in evidence routing: lifecycle, public docs and registry now depend on missing M37 artifacts, while the active hook path still retains the original fail-open/privacy/import-source problems.

## Security / Privacy / Compliance Risk

Medium.

- Absolute local path exposure remains in active and packaged hook output.
- Validator import-source trust remains workspace-dependent.
- Fail-open behavior is not guaranteed for parse/read errors.
- No broad secret scan was run; this review used scoped inspection only.

These are review findings, not certification/compliance claims.

## Quality Evidence

Commands run:

- `git status --short` - observed final tracked diff and untracked review directory.
- `git diff --stat` - reviewed changed-file set.
- `git diff -- ...` focused on lifecycle, comment analyzer, hooks/templates, docs, registry, tests and control-plane.
- `rg -n ...` searches for M37 refs, fail-open/path/import patterns, JS/TS test coverage and unsupported claims.
- `Test-Path -LiteralPath docs\superpowers\specs\batch45-review-remediation-summary.json` - `False`.
- `Test-Path -LiteralPath .codex\product-agent-os\reviews\batch45\remediation-agent-02-docs-control-plane.md` - `False`.
- Custom local Python probe for `.tsx` arrow detection - warning emitted for `evaluateAccess`.
- Custom local Python probe for invalid Python analyzer behavior - raised `SyntaxError`.
- Custom local Python probe for `export async function` and class method detection - warnings emitted for `normalizeEvent` and `redact`.
- `python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_coding_standards_artifacts -v` - exit 0, 30 tests OK before late M37 test changes.
- `python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v` - exit 1 after late M37 test changes; 11 tests run, 3 failures.
- `python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks -v` - exit 0, 20 tests OK.
- `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` - exit 0, 99 tests OK.
- `python tools\check_docs.py` - exit 0, documentation structure checks passed.
- `git diff --check` - exit 0; warnings only about future CRLF to LF replacement in `EVALS.md`, `PLAN.md`, registry files and Track 11 plan.

No `mkdocs`, browser automation, provider/live API, target command, git mutation, hook activation, release/deploy/publish or automation command was run.

## Professional Code Authoring Status

Status: incomplete evidence.

The non-mechanical code change in `comment_sufficiency.py` does not have a visible task-specific coding-standard checklist or equivalent evidence in the diff. Existing tests passed, but they do not prove the new detector forms or the fail-open/privacy/import-source remediation goals.

## Release / Readiness Recommendation

Recommendation: `no_go_for_remediation_closure`.

Required fixes before closing:

1. Fix the failing `tests.product_agent_os.test_coding_standards_artifacts` assertions.
2. Create or remove/downgrade the missing `.codex/product-agent-os/reviews/batch45/remediation-agent-02-docs-control-plane.md` references.
3. Reconcile the M37 packet's no-unapproved-actions ledger with the actual `comment_sufficiency.py` and test diffs.
4. Align lifecycle approval boundary with the actual code diff.
5. Implement hook fail-open handling for analyzer exceptions.
6. Redact/hash hook workspace paths by default.
7. Pin or allowlist validator import source for packaged/target hook use.
8. Add committed focused tests for new TS/TSX/modern JS detection and fail-open/privacy/import trust behavior.
9. Rerun focused comment/hook tests, M37 docs tests, docs checks and `git diff --check`.

## Control-Plane Sync Decision

- `REQUIREMENTS.md`: `not_applicable`; review did not change scope.
- `PLAN.md`: `handoff_required`; remediation remains no-go and may need owner/implementer routing.
- `TEST.md`: `handoff_required`; new regression tests are required before closure.
- `EVALS.md`: `not_applicable`; no eval threshold changed.
- `RUNLOG.md`: `handoff_required`; do not expand root details until the M37 source packet/report exists and RUNLOG budget is considered.
- `prod_test.md`: `not_applicable`; Batch 39 ledger unaffected.
- `.codex/product-agent-os/lifecycle-state.json`: `fix_required`; current marker references missing evidence and contradicts the code diff boundary.

## Residual Risks

- Implementer agents may still add the missing M37 artifacts after this report; this review is based on final workspace state checked after a short wait.
- Tests were local and focused; no full unittest suite or MkDocs strict build was run.
- No runtime/browser/provider/target behavior was executed or approved.
- Raw M26 provider traces remain outside repo by design, so this review checks current source packets and no-go consistency, not live eval replay.

## Next Role

Recommended next role: implementer for a narrow remediation repair pass, then reviewer/verifier rerun.

Do not route to release operator. Current state is not ready for closure or promotion.
