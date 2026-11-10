# PAOS-AUD-G8 — execution evidence

Source status: project-local implementation and verification, 10.11.2026. Owner acceptance pending; fresh-session activation separate.

## Latest owner scope and T14 packet — 2026-11-10

The owner has directed that detailed task matrices in `docs/planning/` remain intact and that the current audit matrix in `research/` must not be split. Those scope decisions are recorded; there is no pending split approval in G8. T14 result acceptance remains pending. Historical preview/earlier handoff sections below are retained as evidence and do not authorize apply.

Implementation: shared `is_detailed_planning_matrix` recognition serves hygiene and explicit compaction budget validation. It recognizes detailed cards/tables within `docs/planning/`, including nested files; index/README/control-plane filenames and fenced examples remain excluded. An explicit per-file project limit wins. Other content/link/security checks and exact apply authority remain unchanged. This is a size-only exception for active detail, not an archive relabel or automatic mutation. No real planning matrices were rewritten.

The research audit matrix remains oversized by owner-directed deferral; G8 does not claim a repository-wide zero-size-finding hygiene audit. It remains one source file with 48 cards and a current revision-pinned PLAN selector. Fresh-session activation is still separate.

## Scope and ownership

Owner: current primary session; no subagents. Baseline worktree clean before own lifecycle update. G8 task detail remains in the audit matrix; this document owns implementation decisions and check receipts, not a second status registry.

Owned first slice: `plugins/product-agent-os/scripts/product_agent_os/control_plane_documents.py` (new cohesive document-contract helper), `templates.py`, `infrastructure.py`, `validators.py`; `tests/product_agent_os/test_control_plane_documents.py` (new), existing infrastructure/validator tests. Later compaction owns a separate side-effect boundary, not an extension of template substitution. Shared roots/registries updated sequentially. Web apps/packages and foreign markers excluded.

## Code change contract

- existing_capability: inspected templates registry/selector, infrastructure `_plan_file` and validation path, merge_section, structural validator, system_file_hygiene and stage manifest boundary.
- smallest_safe_patch: reuse registry, merge, stdlib JSON/hashlib/pathlib and unittest; add one pure document-contract helper because readiness/population/ownership share a public schema. No new framework or dependencies.
- invariants: no target writes during render; unmarked user files remain proposals; explicit owner acceptance cannot be inferred; arbitrary project input cannot become instructions or substitution syntax; post-cutover task projections are not writable file authority.
- dependency_decision: no_new_dependency. One-line exists→is_file fixes directory detection but is insufficient for content/readiness or safe regeneration.
- risk_selected_tests: meaningful failures for directory/empty readiness, missing provenance, owner acceptance, actual-context dry-run parity and filled managed-section preservation. Existing merge/renderer/validator suites retain regression protection.
- comment_decision: comments/docstrings required at schema, preservation, authority and transaction boundaries; no syntax narration.
- performance_applicability: bounded file reads and no provider/model calls; content size metrics measured in UTF-8 bytes. No latency improvement claim.
- evidence_and_gaps: implementation in progress; tests below record actual results, not desired outcomes. Full suite/fixture/transcript/compatibility and affected docs gates required before final local-verification claim.

## Architecture decision and scenarios

T01/T03 domain: document contract (purpose/owner/fields), populated artifact (content with source refs), review receipt (source digest and reviewer/owner). Terms map directly to G8 matrix; source schema is descriptive, not a new registry of task statuses. Pure parsing/population is separate from staged IO and transactional compaction. Public compatibility remains opt-in for semantic readiness; legacy structural mode stays available and explicitly labelled. FSD/HTTP/cloud/DB implementation not_applicable: this slice is a local Python package, not Web M1.

Equivalent Given/When/Then mapping, evidence owner primary:

| Requirement | Given / action | Observable check |
| --- | --- | --- |
| T01 ownership | Six root documents / query contract | Unique owners, canonical required fields and conditional purpose; no duplicated current-state owner |
| T03 content | Empty/directory/scaffold / readiness | Not accepted; missing facts explicit; RU headings irrelevant |
| T03 acceptance | Draft plus stale or absent owner receipt / readiness | Cannot become accepted; current reviewed digest separate from acceptance |
| T04 preservation | User fills managed body / repeat render | Original bytes retained or explicit conflict; never replaced by blank template |
| T05 parity | Actual project text contains invalid marker / dry-run and stage | Same diagnostics against actual proposed bytes |

## M1 integration gates

G8-T01/T03/T10 and PAOS-0001/0002 share document/task source contract. G8-T09 format changes must be understood or explicitly unsupported by PAOS-0050. PAOS-0055 owns integration of readers/writers with SQL authority: G8 file writers must refuse DB-owned task projections. PAOS-0056 freezes only imported sources while checking hashes; no compaction of those sources during cutover. No dependency on full M1 closure. New adapters do not prove compatibility with unimplemented M1 services; fixture-level boundary evidence must be labelled.

## Checks and attempts

- First implementation tranche: `test_control_plane_documents` initial missing-module failure is setup evidence only; after module creation semantic API missing (TypeError) reproduced. Added semantic validator; 5 checks then passed within next run.
- T04/T05 RED: two focused renderer tests failed on existing update action and false-positive dry-run validation. GREEN: `python -B -m unittest tests.product_agent_os.test_control_plane_documents tests.product_agent_os.test_infrastructure_renderer tests.product_agent_os.test_validators -q` — 73 tests, 28.037s, exit 0. Later scoped-render edits require rerun before final closure.
- T06 RED: UTF-8 boundary and stricter project limit tests failed; implementation now uses bytes. Existing warning fixture changed from 41000 to 33000 ASCII bytes to retain warning-case protection under new thresholds, not to waive the new hard error.
- T07/T08: new compaction tests first had missing-module setup error; first functional run 5 passed. Additional independent loss oracle (rehashed source that drops a gate) and SQL/frozen/unknown authority cases produced 4 failures before fixes.
- Combined `python -B -m unittest tests.product_agent_os.test_control_plane_compaction tests.product_agent_os.test_control_plane_documents tests.product_agent_os.test_system_file_hygiene -q` — 29 tests, 0.959s, exit 0. All tests used process-local TEMP/TMP `.codex-tmp/g8-tests`; no package installation, provider or external project writes.

Compaction owned additions: `control_plane_compaction.py`, `test_control_plane_compaction.py`. Recovery journal stores exact before/after bytes locally under target `.codex/product-agent-os/compaction`; it must inherit source privacy and must not be published in evidence. Synthetic tests use isolated temporary roots. Recovery and source preservation do not imply arbitrary external-editor exclusion; callers must quiesce writers.

- Startup: `git status --short` exit 0, clean. No Git mutation performed.
- Read-only compound commands and inline hashing were denied by current lifecycle classification until the new authorized scope marker was complete. Corrected own marker fields to the existing contract; no guard bypass or foreign marker reset. Regression belongs to T12.

## Integration findings and correction receipts

- First full discovery: `python -B -m unittest discover -s tests -p 'test_*.py' -q`, 1399 tests / 825.112s, exit 1, failures=8, errors=1, skipped=1. Failures: old heading-based lifecycle expectations, optional EVALS selection count, public-doc wording. Error: transient Windows temporary-directory cleanup lock. This run overlapped implementation and is discovery evidence, not final verification.
- Explicit route intent now uses `--requested-state` (or `requested_state` API); it is not acceptance or write permission. Legacy RUNLOG/config headings no longer claim readiness. Fixture intent was made explicit while preserving approval assertions.
- First strict MkDocs: exit 1, 11 unresolved G6/G7 repository-artifact links. Replaced broken site hrefs with named repository paths, retaining evidence files/outcomes. Second `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .codex-tmp/g8-tests/site`: exit 0, 32.19s. Final docs edits require final rerun; canonical `site/` not refreshed.
- Budget/schema RED: stricter compaction limit was not enforced and malformed raw boolean facts became draft (2 functional failures). Hardlink creation was denied by Windows sandbox (setup limitation, not guard proof). Fixed limits and schema validation; redirect-guard tests use simulated path metadata and explicitly do not claim real junction/hardlink creation.
- `python -B -m unittest tests.product_agent_os.test_control_plane_compaction tests.product_agent_os.test_control_plane_documents tests.product_agent_os.test_document_navigation tests.product_agent_os.test_g8_control_plane -q`: 22 tests / 5.420s, exit 0 at that revision.
- Expanded focused run: 75 tests / 29.158s, one old CLI intent expectation failed; fixed by explicit route intent. A test-indent setup error in an earlier attempt was corrected before this run.
- Later focused run: 145 tests / 69.792s, one failure exposed CRLF data-block parsing with raw-byte semantic validation. Fixed parser newline normalization while keeping receipt digests bound to original bytes. Final affected checks are listed below.
- Initial exported comparison: 3/3 profiles passed but supporting suite 22/23 passed; report exit 1 for the same CRLF defect. The next exported comparison passed after the fix. Failed attempt is retained here rather than counted as success.
- Actual child-process interruption: `os._exit(23)` after the first atomic file replacement; recovery required exact abandoned-lock handoff. `python -B -m unittest tests.product_agent_os.test_control_plane_compaction -q`: 11 tests / 1.018s, exit 0. Journal restores before bytes; it cannot exclude arbitrary external editors or guarantee cross-file ACID.
- Docs unit run after root history redistribution: 105 tests / 12.556s, exit 0. `python -B tools/check_docs.py`: exit 0. Later final documentation sync is checked again.
- `python -B plugins/product-agent-os/scripts/run_transcript_eval.py`: exit 0, 26/26. `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py`: exit 0, compatible. These are local contracts, not host activation.

## G8 acceptance mapping

| Card | Implemented contract and evidence destination | Boundary |
| --- | --- | --- |
| T01 | `control_plane_documents.DOCUMENT_CONTRACTS`; technical RU/EN ownership/fields/inputs/outputs/triggers table; docs inventory | Schema v1; legacy names preserved; no second task-status registry |
| T02 | `templates.selected_templates`, scoped renderer; per-file selection reasons and reference dependency status; project-formation workflow | Ordinary reuse; EVALS conditional; missing optional workflow refs are explicit `gap_not_staged`, no activation |
| T03 | `populate_document`, `document_readiness`, semantic validator `--document`; missing/directory/CRLF/malformed-schema tests | Source facts are supplied, not invented; review and owner receipts digest-bound; no automatic acceptance |
| T04 | `_plan_file` preserves managed body; stage manifest `preserve_existing`; bulk merge companion-only; renderer/merge regression tests | No ancestral baseline: conservative companion plus owner review, not automatic three-way merge |
| T05 | Actual proposed-content validation; deterministic rendering; byte/digest manifest; existing stale-target merge guards | Dry-run/stage are proposals; target remains unchanged without approved merge |
| T06 | UTF-8 bytes, 39999/40000/40001 RU/EN/emoji/BOM/CRLF tests, stricter 20k; indexed classification policy | Root active documents cannot be exempted; historical class metadata remains deprecated compatibility output |
| T07 | Exact-byte proposal, hashes/diff/forecast/ranges/retention and independent conservation replay; dirty inputs included | Source-private backup bodies stay local; summaries cannot replace originals |
| T08 | Exact manifest authority, compare-and-swap checks, journal/lock, real process-crash recovery, rollback conflict checks | Simulated redirect flags; actual multi-file ACID and arbitrary external-writer exclusion not claimed |
| T09 | `task_plan_moves` whole-card split/anchor migration; local link checking; triggered docs taxonomy | Current audit matrix deliberately not split: separate owner decision required by its own acceptance criterion 6 |
| T10 | Legacy readiness removed; digest-bound task/document state; duplicate paragraph diagnostics; navigation-only indexes | Age does not revoke an accepted decision; semantic dedup is owner-reviewed |
| T11 | Mirror/reference checks, relative-path/digest `offline_bundle` profile, cross-repo unknown; repaired G6/G7 docs navigation | Offline synthetic profile, not unpublished Git checkout or live cross-repository integration |
| T12 | Active/package sync+compaction workflows; changed-document byte audit; bounded read-only terminal sequences; existing mutation/foreign-marker tests | Manual-only; no schedule or cache refresh; fresh-session loading not asserted |
| T13 | Three frozen profiles in `test_g8_control_plane`; exported source-bound JSON; negative controls in compaction/navigation/renderer suites | Same-input local comparison; no live project write or model quality superiority claim |
| T14 | This report, results JSON, task matrix, root sync, technical RU/EN and source registries | `needs_user_acceptance` until owner explicitly accepts the results and evidence limits |

## Root history redistribution

Owned ordinary documentation edit from reviewed proposal `sha256:52274ac9576548edf8c235e816374a4c2b5804c4c6b926b7862b11f2afff1dba`: REQUIREMENTS 48567 → 33375 bytes before the current-scope update. Exact 15423-byte Compatibility Marker Bank moved to `research/product-agent-os-requirements-history-2026-11-10.md`; original SHA256 `11beabf2a32ac9a64278529f537d98d0963f8f930f146db13cb2face98a0f577`. Root keeps an anchor/pointer, archive keeps original bytes plus provenance footer. Before/after backup remains local under ignored `.codex-tmp/g8-tests`; this edit is not a claimed invocation of transactional target apply. Existing legacy assertions now follow that exact owning artifact; the real root byte-budget test remains strict (40000).

## Remaining decisions and exclusions

Owner acceptance T14 pending. Current audit-matrix split requires its separately specified approval; no file was renamed to disguise an active oversized matrix. Fresh-session activation remains separate, T34 no-go and prior G6/G7 decisions unchanged. Actual M1 SQL adapter/cutover integration remains owned by M1; G8 proves the declared file-authority boundary only. No Git mutation operations, external project mutation, installed dependency, provider call, public site publication or automation activation occurred.

## Final integration receipts

- Second full discovery: 1407 tests / 879.268s, exit 1, two wording assertions in `test_task_plan_lifecycle` (same test) failed after the 40k workflow wording changed. Restored the invariant “budget crossing is a compaction trigger … not permission to skip” in both active/packaged workflows. Focused lifecycle retest: 7 / 0.576s, exit 0.
- Final full discovery command: `python -B -m unittest discover -s tests -p 'test_*.py' -q` — **1409 tests / 668.686s, OK (skipped=1), exit 0**. This run started before the last selector expansion; the affected selector/navigation/dashboard suite was rerun at the final selector revision (38 tests below), not silently treated as covered by the earlier imported modules.
- Final affected document/compaction/navigation/pilot/hygiene/runtime-CLI/renderer/validator suite: **146 tests / 76.979s, exit 0**. Exact module list is recorded in TEST.md and the earlier focused-run receipt; the last selector addition has its separate check below.
- `python -B plugins/product-agent-os/scripts/run_fixture_eval.py`: **91/91**, exit 0. Transcript **26/26** and compatibility **compatible**, exit 0. Both `validate_hooks.py .codex/hooks` and `validate_hooks.py plugins/product-agent-os/assets/templates/hooks`: `ok: true`, no errors, exit 0. Static hook validation does not prove fresh-session activation.
- Public CLI smoke in a temporary synthetic root: `compact_control_plane.py propose`, `apply --approve <exact digest>`, `rollback --approve <exact digest>` all exit 0; proposal is read-only and rollback restores exact input bytes. `check_documents.py . .codex-tmp/g8-tests/document-check-manifest.json`: exit 0 for REQUIREMENTS links and digest-bound required offline evidence.
- Selector integration RED: nine pinned sources returned `unknown`; the original bound was eight. The read-only status reader now permits up to 32 source refs while retaining the former aggregate bound of **16 MiB** and existing per-source/row limits. `split_source_references` proposes pins in the existing PLAN selector without a second task-state registry. Actual split→old pins stale→new pins projected preserves IDs/states. `python -B -m unittest tests.product_agent_os.test_status_snapshot tests.product_agent_os.test_document_navigation tests.product_agent_os.test_status_dashboard -q`: **38 tests / 2.079s, exit 0**. An earlier invocation named a nonexistent CLI test module; that setup error was corrected, not counted as behavioral evidence.

## Controlled comparison and reproducibility

Baseline is the read-only Git HEAD snapshot **4b03c75c11a0a38cbf87bee2a3700e05af940b0a**, extracted locally with `git archive --format=tar --output=.codex-tmp/g8-tests/g8-baseline.tar HEAD plugins/product-agent-os` and Python tarfile `filter='data'`. This is a read operation, not a branch/stage/commit or publication action. The revision receipt is `BASELINE_REVISION.txt` in that isolated snapshot. A current re-run must use this exact revision, not assume a later HEAD is the baseline.

Reproduce comparison: `python -B -m tests.product_agent_os.test_g8_control_plane --report docs/superpowers/specs/paos-aud-g8-control-plane-results.json --baseline .codex-tmp/g8-tests/g8-baseline`, with workspace-local TEMP/TMP as above. It passes the **same common task packet and identical target bytes** to pre-G8 and G8 staging; document-fact population and explicit AI applicability are additional acceptance scenarios. No model/provider call is involved. The 210-file legacy inventory is supplemental compatibility data, not the controlled A/B denominator.

| Profile | Pre-G8 common packet: files / UTF-8 bytes | G8 common packet: files / UTF-8 bytes | Oversized RUNLOG → active pointer | Recovery / continuation |
| --- | --- | --- | --- | --- |
| Trade-like | 8 / 101013 | 7 / 7940 | 94473 → 129; strict 20000 | exact original bytes; next change +39 bytes, one file |
| myPartners-like | 8 / 101073 | 7 / 7940 | 106273 → 129; limit 40000 | exact original bytes; explicit AI pilot separately includes EVALS |
| Site-like | 8 / 101001 | 7 / 7940 | 118073 → 129; limit 40000 | exact original bytes; duplicate diagnostic and unavailable cross-repo unknown |

Three profiles / ten frozen flow checkpoints each pass. Original history bytes remain in a named owning artifact; the 129-byte active file is not a lossy summary. Critical IDs, pending owner gate and negative evidence are checked against exact bytes, not a model-authored summary. The comparison measures artifact volume and deterministic behavior, not engineering quality, model superiority, token savings or dollar savings.

## Historical audit-matrix adoption preview — deferred by owner

T09 criterion 6 explicitly requires separate agreement before applying this split. Preview is local only: `.codex-tmp/g8-tests/audit-matrix-preview/`, full before/after proposal `.codex-tmp/g8-tests/audit-matrix-split-proposal.json`, compact review `.codex-tmp/g8-tests/audit-matrix-split-review.json`.

Proposal `sha256:cc3b285323fa7d1c5dbb2bc004e741250c5585072f546cfd2d92f1418d2b7de5`: active index 421692 → 38357 bytes, 48 unchanged task cards in 11 parts (maximum 35242 bytes), historical execution evidence 69271 bytes separately indexed. PLAN selector preview is 25901 bytes. All **65** current projection rows, IDs/states/acceptance states preserved; local-link errors=0; per-part task-matrix errors=0. Whole task cards, dependency text and old anchor redirects remain. After adoption, validate the detailed part files; the original path becomes a navigation index. Future M1 importer must consume those owning part sources, not assume all cards remain inline in the index. No automatic adoption is implied by producing this preview.

## Self-review and control-plane sync

`context_mode=self_review`; primary is the only writer/reviewer, no independent-agent claim. Review found and fixed the bulk-merge preservation gap, CRLF schema parsing, strict-budget enforcement, rehashed loss acceptance, preview-integrity checks, stale journal idempotency and the split/selector source-count boundary. Remaining evidence limits are explicit: simulated redirected-path metadata, source-private journals, offline/synthetic profile, manual exclusion of external writers, M1 service integration, owner acceptance and fresh-session activation. No multi-file ACID or universal cleanup claim.

Control-plane sync: REQUIREMENTS scope/history routing, PLAN order/revision pin, TEST commands, EVALS comparison limits and RUNLOG handoff updated. AGENTS unchanged (`not_applicable`: existing durable ownership is sufficient); prod_test.md unchanged (`not_applicable`: G8 does not change Batch39 evidence). Technical RU/EN, source registries and active/packaged formation/compaction/sync contracts updated. Required docs/matrix/diff final checks are recorded after the final sync. Narrow `.gitignore` rule covers only local G8 test outputs and source-private proposal bodies.

- Additional direct filesystem probe: creating a real synthetic symlink succeeded; `propose` rejected the redirected destination before mutation (`redirected path forbidden`), and original target bytes stayed unchanged. Actual hardlink creation was denied; junction/hardlink metadata guard cases remain simulated. The full-suite single skip is the explicitly non-Windows-only permission guard on this Windows host.

## Earlier documentation gate and handoff — superseded by owner scope above

Final docs+lifecycle suite: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle -q` — 112 tests / 21.718s, exit 0. `python -B tools/check_docs.py` — exit 0. `python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-audit-remediation-task-plan-2026-11-09.md` — ok, no errors. Final strict MkDocs to the isolated G8 site directory — exit 0, 40.46s. No canonical site publication. A transient matrix-authoring CRLF matching error was corrected before the successful validator result.

The owner asked for the consequences of the T09 adoption preview; no apply authority was inferred from that clarification. Independent implementation/checks are complete locally. The exact split proposal and PLAN selector remain unapplied pending the owner choice; T14 owner acceptance is also pending. Fresh-session activation stays separate.

## Planning exception verification — current run

- RED: the new detailed-matrix test failed because docs/planning was absent from hygiene inventory. Added bounded discovery and the size-only classification.
- RED: explicitly moving a closed receipt while retaining a large detailed matrix failed the old universal compaction budget. Shared recognition now preserves that matrix without relaxing approval, preservation or explicit project limits.
- Focused document/hygiene/compaction/navigation/pilot suite: 46 tests / 6.648s, exit 0. Expanded renderer/merge integration: 116 tests / 78.842s, exit 0. Latest hygiene retest after adding broken-link/duplicate diagnostics: 19 tests / 1.267s, exit 0.
- Initial docs/lifecycle/status run: 130 tests / 20.439s, five public-copy/localization assertions failed on an uppercase internal term and mixed-language explanation. Corrected RU/EN prose without weakening tests. Retest: 130 tests / 20.804s, exit 0.
- Fixture eval: 91/91, exit 0. Transcript eval: 26/26, exit 0. Compatibility: compatible, exit 0. Updated pilot export: 3/3 profiles and 26 supporting tests, no failures/errors/skips; source hashes verified current.
- Strict MkDocs initially passed (39.69s); after the final prose change it is rerun below. Documentation checker and 48-card matrix validator passed. The full suite is running; final receipt is appended before handoff.

T14 acceptance proposal: accept T01–T13 as locally implemented/verified under the revised scope; retain detailed docs/planning matrices and the research audit matrix intact; accept the documented synthetic/offline evidence ceiling and separately open fresh-session activation. No production, universal concurrency/ACID, M1 runtime integration or owner-acceptance claim is inferred from these checks.

Final scope checks: all 48 audit cards remain in the single research matrix; current-state projection has 65 rows and no issues. The six root control-plane files are below 40000 bytes. Task-matrix validation and documentation structure checks passed; git diff --check returned 0. Final strict MkDocs log reports successful completion in 38.95s after the prose correction. No research split was applied.

Final full-suite receipt (current scope): `python -B -m unittest discover -s tests -p "test_*.py" -q` — 1414 tests / 1321.762s, OK (skipped=1), exit 0. The one skip remains the non-Windows-only permission guard. Final documentation handoff suite: 105 tests / 19.108s, exit 0. Earlier 1409-test receipts above are historical, not the current result. Self-review confirms size-only exception, retained explicit limits, preserved approval/data guards and no research split. T01–T13 local implementation/verification is complete under the revised scope; T14 owner acceptance is pending.
