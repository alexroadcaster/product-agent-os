# Product-Agent OS — tasks and remediation groups from the full audit

Source status: project-local planning artifact, 09.11.2026; prepared from saved audit and current owning plans. Document status: `G1/G2/G3/G4/G5 implemented_locally_verified`; G6 — partially_verified: T30–T33 locally completed; T34/HOST-01/HOST-02 remain open; GAP-06: three local pilots passed / owner accepted 10.11.2026, without HOST-01 dependency. Preserving cards does not mean completion, promotion or authorization for listed external actions.

Document ID: `PAOS-AUDIT-REMEDIATION-2026-11-09`. Authoring task: `PAOS-AUDIT-TASK-MATRIX-2026-11-09`. Timezone: `Europe/Moscow`.

## Purpose and sources

This document contains **9 groups and 65 cards**: 18 F01–F18 tasks, five existing B45-CQRR-T30–T34, three host/usefulness stages, eight G7 implementation-quality tasks, 14 G8 control-plane tasks and 17 G9 tasks for unified project documentation formation and focused maintenance. Each group and task specifies ID, name, description, technical and product value, affected files and acceptance criteria. task_matrix_plan_v1 fields preserve compatibility with the existing validator. G7 closed with owner acceptance; G8 closed / owner accepted; G6 open gates and statuses retained. G9 T01–T09 implemented_locally_verified; T10 owner accepted; T11–T16 implemented_locally_verified; T17 owner accepted; G9 closed. G8-T14 and G8 closure explicitly accepted by owner.

- [Full audit 09.11.2026](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-full-audit-2026-11-09.md): F01–F18 and evidence boundaries.
- [Subsequent per-chat lifecycle repair](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-session-lifecycle-fix-2026-11-09.md): completed session isolation and exact marker bootstrap.
- [Ordinary/GAP implementation plan](product-agent-os-ordinary-route-implementation-plan-2026-11-05.md): ORD, GAP-03 M06, GAP-05 and GAP-06.
- [Canonical B45 task group](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/batch45-code-quality-runtime-recovery-task-group.json): IDs, names, dependencies and acceptance T30–T34.
- [PLAN.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/PLAN.md), [TEST.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/TEST.md), [EVALS.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/EVALS.md), [RUNLOG.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/RUNLOG.md): current owning pointers and mandatory verification routes.

## Work not to repeat

- T23–T29 and ORD-01–ORD-06 are already locally implemented. The new task reuses them; a discovered regression requires concrete evidence and a bounded fix.
- Session-bound markers, host-envelope identity, own/foreign/mixed marker bootstrap and Windows case handling were implemented in a separate lifecycle slice. F06 now covers remaining command/patch classification defects; F18 covers the new bounded authoring contract.
- Existing GAP-05 create-only grant is not deemed broken merely because it does not support Update File; extending it requires an explicit new contract.
- PAOS-AUD-F01–F18 are IDs for new corrective slices tied to corresponding F in the 09.11.2026 audit; they do not replace identically named older findings from other research.
- T30–T34 and PAOS-GAP-06 appear here for overall ordering. Their source-owned machine status and canonical acceptance remain in original artifacts. PAOS-AUD-HOST-01/02 address remaining verification stages of existing GAP gates; they do not create a second status registry.
- Planned in a card means the described remaining work was not performed by this plan; it does not cancel previously completed portions of the parent task.

## Group matrix

| ID | Group | Cards | Main outcome |
| --- | --- | --- | --- |
| PAOS-AUD-G1 | Reliable hooks, rules and installation | PAOS-AUD-F06, PAOS-AUD-F12, PAOS-AUD-F11, PAOS-AUD-F07, PAOS-AUD-F18 | Aligned active/package contracts, exact write boundaries and correct staging/merge paths. |
| PAOS-AUD-G2 | Package compatibility and host diagnostics | PAOS-AUD-F01, PAOS-AUD-F02, PAOS-AUD-F04 | One source of package schema and surface capability diagnostics without a new doctor framework. |
| PAOS-AUD-G3 | Reliable evidence and current statuses | PAOS-AUD-F03, PAOS-AUD-F08, PAOS-AUD-F16 | Remove false-positive and false missing signals without a new status registry. |
| PAOS-AUD-G4 | Simple ordinary route and compact instructions | PAOS-AUD-F05, PAOS-AUD-F09, PAOS-AUD-F10, PAOS-AUD-F15 | Minimal task context, caller compatibility, lower instruction and repeated-scan load. |
| PAOS-AUD-G5 | Documentation, offline tooling and current site | PAOS-AUD-F13, PAOS-AUD-F14, PAOS-AUD-F17 | Reproducible offline command contract and aligned source/build output. |
| PAOS-AUD-G6 | GPT-6, host activation and user usefulness verification | B45-CQRR-T30, B45-CQRR-T31, B45-CQRR-T32, B45-CQRR-T33, B45-CQRR-T34, PAOS-AUD-HOST-01, PAOS-AUD-HOST-02, PAOS-GAP-06 | Separate reproducible evidence for configuration, activation, quality and acceptance. |
| PAOS-AUD-G7 | Implementation quality, architectural simplicity and sufficient verification | PAOS-AUD-G7-T01–T08 | Minimal complete solution, risk-based checks, evidence-backed review, safe guards and separate comparative evaluation. |
| PAOS-AUD-G8 | Structure and safe maintenance of control plane | PAOS-AUD-G8-T01–T14 | Substantive adaptive documents, navigation, 40 000 UTF-8 byte limit, data-preserving reduction and verifiable recovery. |
| PAOS-AUD-G9 | Unified project formation mechanism | PAOS-AUD-G9-T01–T17 | Formation and focused maintenance of docs/ and .codex/ without duplication; T01–T09 locally verified, T10 accepted; T11–T16 verified; T17 accepted; G9 closed. |

## Order, dependencies and acceleration

G7 closed with owner acceptance; historical order and evidence retained in cards. G8 is authorized implementation based on two control-plane analyses; dependencies are in G8. Local G8 tasks do not require full G6 completion; T34, HOST-01/HOST-02 and G6 owner acceptance retain their gates.

1. G1 and G2 are first local corrective slices. G3 may run independently on core files; shared control-plane updates are sequential.
2. Do not combine all G1 guard changes in an indistinguishable diff: F06 → F18; generated hooks F12 checked against agreed contract. F07 and F11 independent and do not require actual ACL/rules activation for code-level verification.
3. G2 F01 and F02 may be prepared independently; F04 uses both results. No separate doctor framework.
4. G4: F10 → F09; intake F05 may run independently, incremental report scenario requires F18; F15 measurements can precede edits, which require demonstrated benefit. Do not combine skill shortening, model switch and compact-contract intervention in one eval treatment.
5. T30 and T31 can be prepared before local fixes complete on independent files. Canonical dependency graph: T29 → T30; T27/T29 → T31; T25/T30/T31 → T32; T24/T28/T29/T30/T31/T32 → T33; T33 → T34. G4 freeze is an additional reproducibility condition for selected environment, not a hidden canonical B45 dependency edit.
6. Documentation follows behavior in each slice. Final local G5 site build follows G1–G4 stabilization; new host/eval receipts are then added through small targeted synchronization.
7. AUD-HOST-01 follows final package/skills; AUD-HOST-02 follows final hooks/definitions. Changed source/hash reopens its activation gate.
8. GAP-06 begins with one pilot within the previously planned set of 3–5 tasks. One successful case does not close the set; T34 is not a prerequisite for ordinary usefulness verification.

Independent work means permissible ownership separation, not a subagent launch by this document. Minimum team is one executor. In future authorized parallel work distinct owners do not edit the same file concurrently; hooks/lifecycle tests, compatibility module, canonical skills, README and root pointers have one writer per slice.

## Shared implementation and verification boundaries

- All paths below are workspace-relative. Existing paths checked during authoring. Missing T30–T34 files explicitly marked `proposed new` and not yet created. Directory scope requires an exact file manifest before the slice starts.
- Each future implementation scope covers listed files and related tests. For changed source-backed claims synchronize affected RU/EN pairs and both registries. One writer changes shared PLAN/TEST/EVALS/REQUIREMENTS/RUNLOG pointers only on applicable control-plane-sync trigger; historical ledger is not rewritten.
- New behavior/bug fixes: observable RED → minimal GREEN → scoped refactor. Behavior-neutral documentation and formatting use static checks. Select relevant regression, fixture/transcript and compatibility gates via TEST.md; do not repeat unchanged checks without reason.
- Local contract tests, schema validation and generated artifacts do not prove actual host loading, trust, model selection or product acceptance. Such claims require separate receipts for the selected checked state.
- Listed roles are future ownership recommendations, not launched subagents. Select a skill for the actual substage; take canonical Product-Agent OS skills from the repository, not mixed with installed cache.
- The original authoring request authorized saving the plan, not implementation, provider/model/reviewer calls, cache/global edits, target apply, ACL/trust/rules activation, browser/server, Git or publication. Requests on 09.11.2026 authorized local G1, G2, G3 and G4 implementation; other groups require the applicable implementation request; specific external boundaries remain.
- Future slice rollback: revert only its own changes against recorded baseline, preserving others' hunks and historical evidence. ACL/target/trust needs a separate rollback route in advance.
- Duration estimates not set: insufficient measured baseline. Do not substitute invented deadlines; assess actual scope after the first slice.

## Verification of this document

Authoring does not change implementation. Current validator, docs checks and scope review results are recorded below after execution; future checks in cards are criteria, not acquired evidence.

Verification status: `plan_static_verified`; document quality and completeness only, not card implementation.

| Check performed 09.11.2026 | Result |
| --- | --- |
| `python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md` | Exit 0; ok=true; errors=[]; task_matrix_plan_v1. After dependencies clarified, final text checked using same validate_task_matrix_text in memory-only checker: errors=[] |
| `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q` | Exit 0; 100 tests, 3.476 s, OK. Later edits affect only this research plan, not implementation/docs fixtures |
| `python -B tools/check_docs.py` | Exit 0; OK: documentation structure checks passed |
| `git diff --check` | Exit 0. New untracked Markdown additionally checked directly for trailing whitespace |
| Memory-only Python integrity checker via `python -B -` | Exit 0: 6 groups, 26 unique cards, F01–F18 completely covered, seven requested fields present, all task statuses planned, exact T30–T34 titles retained, existing/proposed paths and relative links valid, UTF-8 without replacement characters |
| `git diff --name-only` and `git ls-files --others --exclude-standard` | Existing tracked files unchanged; only this Markdown and own session marker added for authoring |

Self-review: new corrective slices separated from already completed session isolation/ORD/T23–T29; existing T30–T34 and GAP-06 did not receive a second machine status. Artificial hard dependencies removed: generated path F12 and intake F05 can be fixed independently, shared host/authoring gates remain for relevant scenarios. External actions and new files explicitly marked. No independent reviewer launched.

Evidence boundary: no task implementation, full runtime suite, fresh host, live model/reviewer, browser, site build or publication ran. Those are not needed for this authoring; all future acceptance gates remain open.

## Control-plane sync for saving the plan

- REQUIREMENTS.md, TEST.md, EVALS.md, prod_test.md: not_applicable — product requirements, mandatory gates, thresholds and historical evidence unchanged by this authoring.
- PLAN.md and RUNLOG.md: handoff_required — compact link to this separate plan and selection of first execution slice needed when starting implementation; current authority limited to new file and service marker.
- Registry RU/EN: not_applicable for this research plan — no new official behavior claims added; audit remains source of findings. Registry updates included in respective future slices.
- Site/navigation/diagrams: not_applicable for authoring; plan not in site and no build freshness claim.
- Overflow/refactor: not_applicable. Historical artifacts, machine status and other files retained.

## PAOS-AUD-G4 — execution evidence 09.11.2026

Status: `implemented_locally_verified`; F05/F09/F10/F15. G5 may start. Start: 11:30:07 UTC after preflight. One executor, zero delegation, self_review. Baseline git status: only own lifecycle marker dirty; G1–G3 and parallel Web documentation were already in current checkout. History unchanged.

### Scope and decisions

- F05: existing `task_routing.py` shared adapter for `--task`, `--change-mode`, repeated `--changed-path` / `--acceptance`, optional `--task-id`, `--risk-level`. Missing risk=unknown; behavioral invariants/checks/state remain in rich `--task-context`. Partial/mixed/unsafe input rejected without fallback. Both public callers: `codex_runtime_runner/cli.py`, `render_infrastructure.py`; explicit/legacy receipt also in `infrastructure.py`. Legacy default retained for compatibility: automatic prompt-based scope guessing does not replace a checked contract. Existing selectors/state/routes/templates not rewritten. Empty ordinary stage creates manifest directory after gates; target unchanged.
- F10/F09 manifest: all 12 canonical `plugins/product-agent-os/skills/*/SKILL.md`; existing `references/complexity-routing.md`, `references/source-policy.md`, `references/handoff-contract.md`; `tests/AGENTS.md`; relevant `test_lifecycle_skills.py`, `test_validators.py`; related contract consumer `test_infrastructure_templates.py`. test_validators.py was not changed; its checks reused. `agent-team-designer` writes only explicitly assigned local team/handoff artifacts; dispatch/config activation unauthorized. Completion skeptic and other assurance roles read-only. Instruction precedence separated from factual authority. Relevant unchanged evidence may be reused with original provenance.
- F09: 93 conditional domain sections moved without semantic edits into role-specific sections of existing complexity reference. Entry points contain triggers, authority, inputs/outputs, stop/verification and applicability index. Mixed work reads all affected subsections; unknown requires inspection. Role-specific contract reader in `validators.py` and callers in `test_lifecycle_skills.py` / `run_fixture_eval.py` verify preserved gates, not host skill loading. Metadata of all 12 skills byte-identical; implicit invocation/cache unchanged. No new refs/framework.
- F15: only `discovery.py` extracts a pure scope detector and reuses current inventory frozenset within one call. Public scope API still scans fresh data. Methodology/first-run inventories have different exclusions; not merged. No new cross-call cache, database or module framework.
- Tests: `test_codex_runtime_runner_cli.py`, `test_methodology_audit.py`, `test_lifecycle_skills.py`; existing renderer/state/validator tests. Read-only fixture work and ignored measurements under `.docs-tools/reports/paos-aud-g4/`; TEMP/TMP under `tmp` and `eval-tmp`, Python -B/PYTHONDONTWRITEBYTECODE=1.

### Checks and failed attempts

| Command / check | Observed result |
| --- | --- |
| Three new intake tests | RED exit 1: 3 tests, 4 errors; flags/helper/fallback receipt missing |
| `python -B -m unittest tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_infrastructure_renderer -v` | First GREEN attempt: 77 tests, 2 errors; empty ordinary stage did not create manifest directory. Fixed and included in passing combined run |
| `test_discovery_reuses_inventory_for_scope_without_stale_cross_call_cache` | RED exit 1: scan count 2 != 1; then GREEN in combined run, including fresh second call after filesystem change |
| Runtime modules above plus `tests.product_agent_os.test_methodology_audit` | Exit 0: 134 tests, 28.223 s (`runtime-green.log`) |
| Conditional role-section reader | RED import error; first implementation exposed CRLF regex mismatch. Normalization fixed; final role isolation/missing section checks pass |
| `python -B -m unittest tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_validators -v` | Exit 0: 95 tests, 2.498 s (`skills-final.log`) |
| `skill-creator/scripts/quick_validate.py` validate_skill on each canonical skill, PYTHONUTF8=1 | 12/12 valid, exit 0; metadata unchanged |
| `measure_scans.py baseline/after` | First measurement attempt: sandbox TEMP PermissionError (setup failure). Retry with workspace TEMP: exit 0; baseline before discovery change retained. Five-run timings and exact outputs in JSON |
| `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` | Attempt 1 exit 1: typo in readiness reader fixed. Attempt 2 exit 1: 82/91 due to remaining f-string readers; connected to role-specific reader, assertions preserved. Final exit 0: 91/91 (`fixtures-verified.log`) |
| `python -B -m unittest discover -s tests -p "test_*.py" -v` | Initial exit 1: 1326 tests, 469.721 s, failures=9, skipped=1; old fixture readers and one template test consumer fixed before final. Full final: 1326 tests, 540.818 s, OK (skipped=1), exit 0 (`full-final.log`) |
| `python -B -m unittest tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_infrastructure_renderer tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_validators tests.product_agent_os.test_product_agent_os_docs -v` | Exit 0: 253 tests, 34.476 s (`final-focused.log`), includes docs and empty explicit task-context regression |
| `python -B -m unittest tests.product_agent_os.test_infrastructure_templates -v` | Exit 0: 95 tests, 1.399 s; backend assertions retained, reader follows relocation |
| `python -B plugins/product-agent-os/scripts/run_transcript_eval.py`; `validate_codex_compatibility.py` | Each exit 0; transcripts 26/26; compatibility local structure only, host not_verified |
| `validate_agents.py .codex/agents`; `validate_hooks.py .codex/hooks.json`; `validate_hooks.py plugins/product-agent-os/assets/templates/hooks` | Each exit 0; 15 active agents, errors/config_errors=[]; hooks errors=[]; no activation performed |
| `python -B tools/check_docs.py`; `validate_task_state_consistency.py`; `validate_task_matrix.py` with this plan | Exit 0; structure passed; validators ok=true/errors=[] |
| `git diff --check` | Initial: one trailing blank line in complexity reference removed. Final exit 0 |
| Self-review empty explicit file argument | RED exit 1: `--task-context ""` incorrectly selected legacy. None check instead of truthiness fixes denial; final focused passed |

### Measurements and claim ceiling

Fixed synthetic workspace: 304 files, 300 source files in 10 directories; one environment, five discovery samples. Calls `_relative_files`: 2 → 1. Median discovery: 114.448 ms → 103.959 ms (~9.2% in this local fixture). Full discovery output before/after equal. Methodology scan separately retained; no universal speedup promise.

On the same fixture legacy renderer proposes 209 artifacts, explicit ordinary 0, questions=[] in both. Timing diagnostic: legacy 593.0/588.5 ms before/after; ordinary 127.6/118.3 ms. No question reduction claimed; baseline already zero. CLI-to-stage RU/EN/no-builder test creates no task.json and preserves target bytes.

93 moved section bodies compared to baseline; all matched. Entrypoint raw UTF-8 bytes: 292137 → 194355. Deterministic measurement read sets below: SKILL.md + specified shared refs + selected conditional subsection bodies. This is source-loading simulation, not fresh-host/model token/latency/quality evidence.

| Read set | Before bytes | After bytes | Reduction |
| --- | --- | --- | --- |
| ordinary-doc-plan: implementation-planner + Docs Tooling Selector + source-policy | 42401 | 29541 | 30.33% |
| backend-review: risk-reviewer + Backend + Quality Testing/Evals + source-policy | 34927 | 24137 | 30.89% |
| security-ai-review: risk-reviewer + Security + LLM/AI/RAG + Quality + source-policy | 34927 | 25458 | 27.11% |
| team-handoff: agent-team-designer + Codex Agentic Workflow + source-policy + handoff-contract | 26947 | 26863 | 0.31% |

No claim that every skill or path shrinks equally. All-domain reads can cost more due to the index; applicability remains the selector. Local typical/edge/adversarial contract comparisons preserve role ownership, missing evidence, approvals, unsafe paths and conditional domain gates. Live behavioral comparison/fresh-session discovery belongs to G6, not this source-level check. Model/effort and B45 treatment unchanged.

Rollback: G4 hunks only. Snapshot baseline and file hashes in ignored reports. B42/B45 source JSON, G1–G3, installed cache, global instructions, trust, hooks/rules and Git history unchanged.


### Closure, sync and provenance

Final closure checks after status recording: docs unittest exit 0, 100 tests, 3.511 s (`docs-final.log`); check_docs, task matrix, task-state consistency and git diff --check each exit 0. Source/test hashes match verified manifest; current projection contains 43 tasks without issues.

Self-review: context_mode=self_review; tester_verdict=closed_allowed for local scope. Checked public caller compatibility, fail-closed intake, source/read-only boundaries, unchanged metadata, role-scoped references and snapshot lifetime. Blocking findings corrected. Source bodies 93/93 preserved; current projection updated after owning-plan write.

Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG updated; CLI/architecture/current-state RU/EN and registry RU/EN updated. prod_test.md not_applicable (Batch 39 unaffected); handoffs none; overflow not_required (<50 KiB roots). Strict MkDocs not_applicable: nav/Mermaid/extensions/site unchanged. Generated site freshness not claimed.

Measured interval 11:30:07–11:58:37 UTC: 28 min 30 s; preflight and final evidence checks after checkpoint excluded. Model/reasoning inherited, subagents=0; token/tool telemetry unavailable. Skills: skill-creator read; Python advisory skills read previously.

SHA-256 of verified source/test manifest (raw bytes); source bodies and metadata have separate baseline comparison:

| Path | SHA-256 |
| --- | --- |
| `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py` | `a7ce19682281a554894d8c15d45dbb8d1cdf6cb7cb86019d387797e771c382e2` |
| `plugins/product-agent-os/scripts/product_agent_os/discovery.py` | `38311ab28a2b80f9fd61f73c6b39c9b38bae1e139c5e32044e5260aec16aa6e8` |
| `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py` | `b9c8c4a211c5c042148ec9fd0034943b67d577498b8b346bcc51c646b8a58326` |
| `plugins/product-agent-os/scripts/product_agent_os/task_routing.py` | `bcf5740677a3651558643f8d259b744faff0fd916c5090d622de5328e439e097` |
| `plugins/product-agent-os/scripts/product_agent_os/validators.py` | `9fa8cf833a99f1188d00b24b18a5cdf18fdf305627501f145d109e7a3e888deb` |
| `plugins/product-agent-os/scripts/render_infrastructure.py` | `7238888560086dcf97bbcfb0000b2c6a469366bb2d969de33dd57603dc6687a5` |
| `plugins/product-agent-os/scripts/run_fixture_eval.py` | `34216b5ddc01dd64abf2c2e29e53c0671c812d9064b95552276f42658eff0bc2` |
| `plugins/product-agent-os/skills/agent-team-designer/SKILL.md` | `8767197ce0ef37475a24dfc9daa5614ba259ce4dd9fd4437389242342031658e` |
| `plugins/product-agent-os/skills/automation-promoter/SKILL.md` | `01911c2074257c5318dee54fb3b914cf30281f97cbab4fdc257106fdf5393838` |
| `plugins/product-agent-os/skills/completion-skeptic/SKILL.md` | `3f88af990e13b8cb51c2cf320579fdca550b321fbc153ae195b7bee38711f9c8` |
| `plugins/product-agent-os/skills/docs-maintainer/SKILL.md` | `7871f1d7a1df5f794cace515248b82973d7410834cd70f62cbf6c3c2ba91f1fa` |
| `plugins/product-agent-os/skills/implementation-planner/SKILL.md` | `e6e846e712e9988f6dccb8336e2580ef760fa83225c01edcb5a2b4ab2832c151` |
| `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md` | `d132400fd3ee5117a43dc885c82a63929ed2da196c714c30ec3f78bde12ffd98` |
| `plugins/product-agent-os/skills/pr-release-operator/SKILL.md` | `538eee5bffbdaa07e57dbea8ee69c9dd6f740a0568559900ad747de034cafc27` |
| `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md` | `de0ddc5ac698a5f23e1dcf86c8f7d68d6a649054405129bca97209561f2cf7e8` |
| `plugins/product-agent-os/skills/references/complexity-routing.md` | `cb8fe7a0fd0435385726f19727d2650c79e56a05de0a3d4202b024fc43fa0cb2` |
| `plugins/product-agent-os/skills/references/handoff-contract.md` | `fa7529e299eea52b329d0cfec64810ce8642a92e5a00889b50210d740d9fffe6` |
| `plugins/product-agent-os/skills/references/lifecycle-states.md` | `649cb4d7ba706ee6c7fe88a2cd8640daab5c011c51c04a92d0097c70cfa21cd8` |
| `plugins/product-agent-os/skills/references/source-policy.md` | `c31766c27ba09fa0a2ad7ce1798482177be9e5d22d93bea075f7fd45f85b8e35` |
| `plugins/product-agent-os/skills/requirements-author/SKILL.md` | `50c13a4f52ed81f0d6bfa459620b48f13619312827c92c3f35c5bb45bf1b1e82` |
| `plugins/product-agent-os/skills/risk-reviewer/SKILL.md` | `6a3e6d8ff4f5c6796a154d842e3632a3efcb553e0432cfdd0207ec03487f902b` |
| `plugins/product-agent-os/skills/test-eval-designer/SKILL.md` | `0d969a53d66e33fe14fab1501896ec7f33299b2bf405ead63018a513c6c6df19` |
| `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md` | `cca08a7300df6c2a1fc6d55513dda1ffeb2e21c0fd6d0319a8f90a59713b5187` |
| `tests/AGENTS.md` | `305aced71d08747c36eeb0c0fe8659e349d2fb19e60c6b538b785c9512a01005` |
| `tests/product_agent_os/test_codex_runtime_runner_cli.py` | `0ae558423c1b4e90b49c80bed04120d24617a1ecc60e984f80dd505bd5351177` |
| `tests/product_agent_os/test_infrastructure_templates.py` | `b3441d7c35b1ef187100f43af1de1c2ae15371d3bea13c5a2d242a957bb87879` |
| `tests/product_agent_os/test_lifecycle_skills.py` | `ee777fbf3a7dcec93e1427d6a3d8e704ae551c2fccc3f1c743619d45b68ed6cd` |
| `tests/product_agent_os/test_methodology_audit.py` | `b11b58305b1f411e1434f5a3237a475963e7918f84271b4e51d894d450e8caa4` |

## PAOS-AUD-G3 — execution evidence 09.11.2026

Status: `implemented_locally_verified`; F03/F08/F16. Start: 10:19:14 UTC (after preflight). Ready to move to G4.
One executor, self_review, zero delegation; Python advisory skills previously read.
Scope: three owning modules and focused tests; related read-only caller `render_status_dashboard.py` and UTC timestamps of two synthetic predicates in `run_fixture_eval.py`; current-state and self-learning docs RU/EN; registry RU/EN; five root control-plane files and this plan. Baseline: dirty G1/G2 plus parallel Web documentation. Other changes preserved. Git/provider/host/cache/permission mutations unauthorized.

### Fixes and criteria

- F03: ISO and DD.MM.YYYY after RU/EN labels; strict calendar validation; missing/invalid/future/stale/date_present_not_verified. Undated source prose is not a date. Multiple dates use earliest, future/invalid are not concealed. Registry resolution is one local workspace hop only to canonical RU/EN registry, bounded read, exact heading/table-ID anchor; broken/unsafe refs visible. Claim classes heuristic; project/historical/mention do not equal official behavior, claim_supported always not_verified. Exact-host URL and secret checks retained.
- F08: zero owner labels → insufficient_evidence; owner_sentiment and owner_label_counts separate from denominator/coverage and record validity. Negative labels can be owner_label_supported but not positive sentiment. Missing/empty/wholly rejected public summary preserves this semantics. Invalid JSON types in ledger rejected without traceback or copying rejected payload. Manual-only/candidate-only unchanged.
- F16: one PLAN current pointer contains only owning paths and SHA-256 revisions. B42/B45 machine JSON retained. Newer dated execution_evidence outranks historical status; equal-date contradictions and duplicate ownership → conflict; invalid/future/unknown/stale revision → unknown. Task/run/verification/acceptance separate; prose acceptance criteria do not become acceptance. Markdown task matrices and existing JSON task groups supported by bounded resolver. Existing dashboard CLI wired to workspace pointer; no-pointer B37 deferred route retained. Undated/naive/future verification evidence is not current.

### RED/GREEN and current gates

Logs: ignored `.docs-tools/reports/paos-aud-g3/`; TEMP/TMP within `tmp`, Python `-B`, PYTHONDONTWRITEBYTECODE=1. All fixtures synthetic; not actual host acceptance.

| Command / check | Result |
| --- | --- |
| `python -B -m unittest tests.product_agent_os.test_source_policy tests.product_agent_os.test_self_learning_state tests.product_agent_os.test_self_learning_extensions -v` | RED exit 1: 46 tests, failures=4/errors=2. GREEN exit 0: 46 tests, 3.997 s |
| `python -B -m unittest tests.product_agent_os.test_status_snapshot -v` | RED exit 1: 14 tests, failure=1/errors=4. GREEN exit 0: 14 tests, 0.060 s |
| `test_source_policy.SourcePolicyTest.test_russian_dotted_dates_and_undated_source_prose` | RED exit 1: invalid instead of date_present_not_verified; then included in passing focused suite |
| `python -B -m unittest tests.product_agent_os.test_source_policy tests.product_agent_os.test_self_learning_state tests.product_agent_os.test_self_learning_extensions tests.product_agent_os.test_status_snapshot tests.product_agent_os.test_status_dashboard -v` | Exit 0; 75 tests, 7.362 s (`focused.log`) |
| Final status integration module | Exit 0; 16 tests, 0.141 s (`status-integration.log`); actual `_snapshot_for_workspace` wiring and byte-for-byte synthetic workspace preservation |
| `python -B -m unittest discover -s tests -v` | Exit 0; 1320 tests, 725.771 s, OK (skipped=1); `full.log`. Run before final ownership/UTC edit; final focused and final fixture separately check those changes |
| Final five-module focused command above | Exit 0; 78 tests, 6.538 s (`final-focused.log`); includes scope-prefix ownership regression |
| `test_pointer_scope_preserves_canonical_owner_over_planning_cross_reference` | RED exit 1, then GREEN in final focused; PAOS-AUD-* scope excludes B45 cross-reference cards, not real conflicts |
| `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` | First exit 1: 90/91; two stale predicates had naive timestamps. Assertions preserved, synthetic dates assigned UTC. Repeat `fixtures-final.log`: 91/91 ok=true, JSON result separately asserted (exit 0); CLI exit of repeat run not retained after compaction |
| `python -B plugins/product-agent-os/scripts/run_transcript_eval.py` | Exit 0; 26/26 (`transcripts.log`) |
| `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py` | Exit 0; local_structure_only_not_host_or_distribution_readiness (`compatibility.json`) |
| `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | Exit 0; 100 tests, 3.890 s (`docs.log`); closure rerun recorded below |
| `python -B tools/check_docs.py`; `validate_task_state_consistency.py`; hooks validators `.codex/hooks.json`, `.codex/hooks`; `git diff --check` | Exit 0; source state errors=[]; hook errors=[]; final closure check below |

### Scan delta on one set of 310 docs before documentation sync

`validate_source_policy('.', as_of=date(2026,11,9))` read-only baseline: needs_review; 188 registry review rows, 151 missing official hints, 310 missing dates, zero secrets. After parser fix: needs_review; 133 review rows, 89 missing official hints, 281 missing + 29 date_present_not_verified, zero secrets. Removed 55 review rows, no new rows. Examples: project architecture/first-run/evidence-boundary diagrams no longer demand official behavior evidence solely for a project contract. 29 recognized dates do not imply semantic verification. Remaining 133 findings are a manual review queue, not automatically confirmed defects; G3 does not mass-fix source claims. JSON baseline/after preserve file-level provenance; documentation sync after comparison recorded separately.

Self-review: context_mode=self_review; tester_verdict=closed_allowed for local scope. Checked unsafe paths, bounded reads, stale revisions without fallback, conflicting ownership, missing labels, RU/EN parity and history preservation. No open blocking finding. Rollback: G3 hunks only; preserve B42/B45 bytes, G1/G2 and Web work. Source-state pointer invalidation requires repeat review and pin, not auto-refresh. Semantic source verification, fresh host and promotion remain outside local claim ceiling. Strict MkDocs not_applicable: navigation, Mermaid, extensions and site unchanged.


### Final G3 reconciliation

- Final source scan after docs sync: 310 docs, needs_review, 133 review rows, 281 missing dates + 29 date_present_not_verified, zero secrets. Matched baseline delta above is not called semantic audit.
- Current pointer: 43 tasks, 3 revision-pinned sources, no ownership conflicts; audit source scope PAOS-AUD-*. B42/B45 bytes checked against pre-slice SHA-256; T23–T29 retained.
- Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG updated for respective scope/sequence/checks/evals/handoff triggers; registry and current-state/self-learning RU/EN updated. prod_test.md not_applicable (Batch 39 unaffected); handoffs none; overflow not_required, root budget 50 KiB. Strict MkDocs not_applicable: nav/Mermaid/extensions/site unchanged.
- Model/reasoning inherited; provider/token/tool-count telemetry unavailable. Subagents=0; one restored compacted handoff in G3. Local tests do not prove fresh-host loading or product acceptance.


### Closure checks and provenance

Final closure docs: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` — exit 0, 100 tests, 4.065 s (`docs-final.log`). `python -B tools/check_docs.py`, `python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md`, `python -B plugins/product-agent-os/scripts/validate_task_state_consistency.py` and `git diff --check` — exit 0; validators errors=[]. Revision projection after closure: 43 tasks, 3 sources, issues=[]; F03/F08/F16 implemented, B45-T30 planned, B42-S2-M04 implemented from newer receipt. Root UTF-8 budgets <50 KiB; largest REQUIREMENTS.md 48010 bytes.

Measured interval: 10:19:14–10:47:28 UTC, 28 min 14 s; preflight before start and final evidence recording after checkpoint excluded. Final source scan unchanged: 133 review rows; semantic review remains separate work.

SHA-256 binds code/tests to checked local state. Full suite started import before last scope-prefix test and UTC fixture correction; final focused/fixture cover those deltas. Owning-plan source revision pinned in PLAN.md after recording this evidence.

| File | SHA-256 |
| --- | --- |
| `plugins/product-agent-os/scripts/product_agent_os/source_policy.py` | `6ba02af321a592cc59666179b9b9111bed660a4a2be24b48dca1f41c7e68dd00` |
| `plugins/product-agent-os/scripts/product_agent_os/self_learning_feedback.py` | `1f0936316930475379341e635da9608cfa623c46d62559257095b3631386bcf5` |
| `plugins/product-agent-os/scripts/product_agent_os/status_snapshot.py` | `0a3ea0049ab34e50f4599d57908694e8731925d173503ee34a09b2a82c772a11` |
| `plugins/product-agent-os/scripts/render_status_dashboard.py` | `5cbd426fec36ae49f15430e5392b4e2f0f439df50e123c0c72ad73901cf84304` |
| `plugins/product-agent-os/scripts/run_fixture_eval.py` | `8e74c99346c320ad9335dad105a54b77eeb22abb0bdbaa12be7d41db3432f489` |
| `tests/product_agent_os/test_source_policy.py` | `faa97e18c29445f1b6f74f6d30f62c994ce36a979dd35c28c0bc4dc37f6df5a4` |
| `tests/product_agent_os/test_self_learning_state.py` | `237667633f7b2b9038e64237010b8c900dc3cae3abc7475c6b0ddfb0777f4cbc` |
| `tests/product_agent_os/test_self_learning_extensions.py` | `84f37167864361a00c7eeb7a881ea655362dc608884c6abe5992596f19776580` |
| `tests/product_agent_os/test_status_snapshot.py` | `35bb009f88f26a875c0f3d1e78379906de42dc61458bc0807d30db87ac1943ce` |

## PAOS-AUD-G2 — execution evidence 09.11.2026

Status: `implemented_locally_verified`; F01/F02/F04 closed for local scope. Ready to move to G3. One executor, zero delegation, self_review.
Measured interval: 09:57:07–10:17:15 UTC, 20 min 8 s. Preflight and official source check preceded it and are excluded. Model/reasoning inherited; provider/token/tool-count telemetry unavailable. Subagents=0; one restored compacted handoff; Python skills previously read, OpenAI Docs read for G2.
Baseline: dirty G1 implementation and parallel Web documents preserved. Scope: card files, related `test_plugin_structure.py`, README, compatibility RU/EN, models RU/EN, registry RU/EN and root control-plane. No new framework, model migration or T23–T29 change.

### Implementation and source decisions

- F01: existing Codex compatibility manifest retained; `.mcp.json` uses `mcpServers`. TOML-only startup timeout not carried into bounded plugin JSON subset. Duplicate keys, transport mixtures and unknown options require review; portable root/inline OpenAI precedence unchanged. Contacts/URLs with unverified owners removed. Required author/developerName use explicit `Unverified local publisher` sentinel. Publisher, listing URLs, distribution icons and release review remain gated; not a full submission validator.
- F02: support and observation separated. Native plugin documented in App/CLI, unsupported in IDE; standalone skills documented separately. Caller observation for unsupported yields conflict, not promotion. Unknown surface does not inherit CLI/App support.
- F04: read-only diagnostics accepts up to 16 KiB JSON with allowlisted non-secret fields; duplicate/malformed input rejected, values outside allowlist not printed. Surface/version, configured/observed model, trust and account access separated. Only Terra/CLI has documented minimum 0.159.0. Optional explicit cache directory compared by manifests/MCP/SKILL.md; bounded component provenance, not full package/runtime digest. No cache writes, provider calls, subprocess host discovery or model/effort changes.
- Primary sources fetched 09.11.2026: [Build plugins](https://developers.openai.com/plugins/build/plugins), [submission metadata](https://developers.openai.com/plugins/deploy/submission), [plugin surfaces](https://learn.chatgpt.com/docs/plugins#use-plugins-from-a-supported-surface), [standalone skills](https://learn.chatgpt.com/docs/build-skills), [models](https://learn.chatgpt.com/docs/models). Sources/claims indexed in both registries. Historical model catalog facts dated 03.11.2026 are not claimed newly checked.

### Checks of the current run

Logs: ignored `.docs-tools/reports/paos-aud-g2/`. TEMP/TMP directed to ignored `tmp`/`eval-tmp`; `PYTHONDONTWRITEBYTECODE=1`, Python `-B`. Local synthetic/deterministic checks, not host receipts.

| Command / check | Observed result |
| --- | --- |
| `python -B -m unittest tests.product_agent_os.test_codex_compatibility -v` before implementation | RED: 11 tests; failures=2, errors=9. Package needs_review instead of compatible; mixed transport incorrectly accepted; new observations/cache API absent. Shell wrapper returned 0 after Get-Content, so that exit is not unittest success. `red.log` retains FAILED |
| Same focused command after implementation | Exit 0; 11 tests, 1.438 s, OK (`green.log`) |
| `python -B -m unittest tests.product_agent_os.test_codex_compatibility tests.product_agent_os.test_plugin_structure -v` | Exit 0; 21 tests, 1.839 s, OK (`focused.log`) |
| `python -B plugins/product-agent-os/scripts/run_transcript_eval.py` | Exit 0; 26/26, failed=0 (`transcripts.log`) |
| `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py` | Exit 0; compatible, local_structure_only_not_host_or_distribution_readiness; distribution gated; surface unknown, model not_verified, trust unknown, cache_not_provided (`compatibility.json`) |
| `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` | Exit 0; 91 fixtures (`fixtures.log`) |
| `python -B -m unittest tests.product_agent_os.test_codex_compatibility.CodexCompatibilityTest.test_cache_junction_is_not_followed -v` | RED exit 1; observed instead of needs_review. After Windows junction guard included in passing final suites |
| `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | First run exit 1, 100 tests, one README phrase assertion. Exact surface phrase retained with correct native/standalone distinction; final combined docs suite passed. After control-plane closure: exit 0, 100 tests, 3.566 s, OK (`docs-final.log`) |
| `python -B -m unittest tests.product_agent_os.test_codex_compatibility tests.product_agent_os.test_plugin_structure tests.product_agent_os.test_product_agent_os_docs -v` | Exit 0; 122 tests, 10.234 s (`final-focused.log`), includes junction and docs regression |
| `python -B -m unittest tests.product_agent_os.test_codex_compatibility tests.product_agent_os.test_plugin_structure -v` after readability refactor and surface scope label | Exit 0; 22 tests, 2.796 s (`final-contracts.log`) |
| `python -B plugins/product-agent-os/scripts/validate_hooks.py .codex/hooks.json`; `.codex/hooks`; `plugins/product-agent-os/assets/templates/hooks` | Each exit 0, ok=true, errors=[]; hooks unchanged in G2 |
| `python -B tools/check_docs.py` | Exit 0; documentation structure checks passed |
| `git diff --check` | Exit 0; unlike early G1, other Web EOF errors no longer present at this point. G2 did not fix them |
| `python -B -m unittest discover -s tests -p 'test_*.py' -v` | Exit 0; 1305 tests, 748.949 s, OK (skipped=1: non-Windows guard only), `full.log` |
| Final `validate_task_matrix.py` on this plan; `tools/check_docs.py`; `git -c core.safecrlf=false diff --check`; `validate_codex_compatibility.py`; memory-only integrity checker | All exit 0; matrix errors=[], docs OK, diff clean, compatible; 26 statuses, only eight G1/G2 tasks implemented, seven final source hashes match; UTF-8 and root budgets OK |

Self-review: `context_mode=self_review`; no separate reviewer. Checked precedence, absence of MCP/subprocess/provider execution, output allowlist, IDE conflict, model/trust claim ceiling, bounded cache traversal, preservation of T23–T29 and Git/host boundary. Windows junction case found and fixed; final diff does not broaden model policy or approval authority. Cache comparison is not a race-proof authorization mechanism and does not replace full package receipt.

### Control-plane sync G2

- REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG: update_required → updated; scope, sequence G3, checks, claim ceilings and handoff synchronized.
- Registry RU/EN, compatibility RU/EN, models RU/EN and README: updated with current primary sources and local diagnostic contracts.
- `prod_test.md`: not_applicable — Batch 39 evidence unchanged. T23–T29 and canonical T30–T34 machine status unchanged.
- Overflow/refactor: not_applicable; all five root files below 50 KiB. Handoffs required: none within G2; G6/owner gates remain open under original acceptance.
- Strict MkDocs/site/navigation/diagrams: not_applicable — only prose/source/control-plane changed, site not rebuilt and freshness not claimed.
- Review: self_review, tester_verdict=closed_allowed for local group; closure_level=implemented_locally_verified. Not host/product/release readiness.

### Binding to verified source state

Full discovery started before final junction guard and readability refactor. Final 122 tests cover junction/docs repair, then 22 affected contracts checked after last refactor; full-suite result is not represented as a rerun of all tests on the last revision. Fixture/transcript behavior unchanged by last refactor. SHA-256 of final implementation/test files:

| File | SHA-256 |
| --- | --- |
| `plugins/product-agent-os/.mcp.json` | `14b1ca834d9867a3f382a7ebbf7d2f149e1b7ac0d2ae9deef5cdc030e670a546` |
| `plugins/product-agent-os/.codex-plugin/plugin.json` | `b3f07a4a2e6ba8a96b27ecfbd3b2065e94676f8d88dafd18a6e33e04bd1fd693` |
| `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py` | `e58c19c216b863f15ecfe30b93655ac2180d9df0d8f2c09aa0756024fb819d7f` |
| `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py` | `dacb7b39f2b1905b89d72aa26a00bb05477f18d8f821841fc1ed195e4008788e` |
| `plugins/product-agent-os/scripts/validate_codex_compatibility.py` | `9ab5e67a3fb5359efa5ad82158f48a0b650cf8bebda0efd24f52aeccd7863265` |
| `tests/product_agent_os/test_codex_compatibility.py` | `ff483c80a22392779320d6e8d48a4388ce910228e49b78e0013d0527786afb3b` |
| `tests/product_agent_os/test_plugin_structure.py` | `d988222e1182cf681e6c67bc0494713320aba8ce21ab09212a4281c72387bc89` |

Lifecycle preflight: two incorrect forms of own new marker (status `implementation_in_progress`, then missing updated_at) rejected by hook. Only own-session marker corrected to `in_progress` with updated_at and retained prior_closure G1. Compound bootstrap rejected; exact patch applied. Process evidence, not new activation check.

Rollback: revert only G2 hunks against G1 baseline; preserve other Web/G1 changes and historical receipts. `prod_test.md`, model pins/effort, installed cache, global config and host trust unchanged. G6/AUD-HOST-01 owns actual host receipts; distribution requires confirmed owner data and separate authorization.

## G5 execution evidence — 2026-11-09

Status: `implemented_locally_verified`; F13/F14/F17. One executor, zero delegation,
context_mode=self_review. Baseline worktree was clean; Git history unchanged.
Current-run reports: `.docs-tools/reports/paos-aud-g5/`; render inputs:
`output/playwright/paos-aud-g5/`. Detailed source/build hashes: `verified-source-hashes.json`.

| Gate / command | Current run observation |
| --- | --- |
| `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs.DocsInstallerContractTest -v` | RED: 3 tests, 2 failures — offline pip upgrade without --no-index; GREEN: 3/3, later expanded to 5 regression cases in docs suite |
| `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | 105 tests passed, exit 0; post-build/control-plane rerun: 18.137 s, docs-final.log |
| `python -B tools/check_docs.py` | exit 0, documentation structure checks passed |
| README renderer `--help`, full example `--dry-run ... --risk-level low` | exit 0; valid JSON; context/safety gaps do not become permission or activation |
| `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py` | exit 0; local structure only, MCP not run |
| `.venv-docs/Scripts/python.exe -m mkdocs build --strict` | exit 0; 28.16 s; existing project-local dependencies, no install |
| `tools/fix_site_i18n_links.ps1 -SiteDir site` | final retry: updated_files=2, no error; before retry two Windows HTML files temporarily locked |
| `python -B .docs-tools/reports/paos-aud-g5/check-site.py` | 368 HTML; 220 nav routes; missing files/routes/anchors/search routes = 0; 310 search pages |
| `python -B .docs-tools/reports/paos-aud-g5/run_render.py` | installed Chromium headless shell 1223; local Mermaid 10.9.6; 93/93 parse/render with nonzero SVG dimensions; browser exit 0 |
| `git -c core.safecrlf=false diff --check` | exit 0 |

F13: offline branch uses --no-index/--find-links, does not upgrade pip; bootstrap
uses venv/bundled ensurepip without --upgrade-deps. Offline overrides AllowNetwork.
Missing directory is rejected before bootstrap; install error stops the route without
network fallback. Stub replaces only subprocess boundary: actual installation
was not performed, global environment unchanged. Online upgrade remains explicit.

F14: README first screen contains explicit skill invocation, ordinary inline intake,
support/observation matrix and current-state pointer. MCP example matches .mcp.json;
startup_timeout_sec removed from JSON. Archive receipts/counts retained in details with explicit
dated applicability scope. Publisher and distribution remain gated.

F17 semantic review: current-state RU/EN agree on G1–G5 scope, pointer semantics,
source-policy/feedback limits and next G6; hooks RU/EN agree on session selector,
legacy prohibition, trust and explicit activation boundary; models RU/EN agree on
G2 diagnostics/cache scope and lack of host proof. Hooks/models sources already aligned
in G1/G2, no repeat editing needed; new build includes them. Registry updated
as pairs. 10 English-original plans retain exception from translation inventory.
Diagrams/mkdocs.yml/vendor assets unchanged; 93 navigation diagrams rechecked.

Failures/recovery: initial README dry-run failed on sandbox TEMP cleanup;
retry with workspace TEMP/TMP passed. Shell Chrome dump yielded no DOM; normal Chrome/Edge
and sandbox headless exited before render. Authorized local headless run outside shell
sandbox passed with browser sandbox retained, separate workspace profile and DNS
blocking; no dependencies/servers installed. This is render evidence, not host activation.
Two mapped-file errors during i18n were fixed by retry; final check of all links
and anchors passed. Failed attempts do not count as acceptance.

Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG updated; prod_test.md
not_applicable (Batch 39 outside scope); AGENTS/config/hooks not_applicable. Root size
budget checked by docs suite. B42/B45 canonical source hashes preserved. Rollback:
revert only G5 source hunks, then rebuild local site; do not change trust/cache.
Full plugin unittest/fixture/transcript and live behavioral eval: not_applicable for
installer/docs change; G4 evidence remains prior run, not claimed new.
Next slice is G6; owner acceptance, actual installation, fresh-host loading,
model quality, publication and production readiness not demonstrated by this run.

Task-matrix self-review: evidence moved before cards so parser does not include it in adjacent F15 card; original placement caused unresolved-placeholder diagnostic. Final validator result: task-matrix-final.json.

## G6 current-project pilots — 2026-11-09

G6 partially_verified: GAP-06 implemented / owner accepted 10.11.2026; all three synthetic local pilots accepted by owner. HOST-01 is not their dependency. T34 no-go and fresh-session activation HOST-01/HOST-02 remain separately open; manual_only retained.

Results and commands: [pilot-results](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/superpowers/specs/paos-aud-g6-pilot-results.json). Baseline bug: 64 instead of 8; final 1/4/8/8 and bounded large attempt passed. Config info/7; native encoder /, space, empty passed and SHA-256 unchanged. Historical HOST receipts below are not current pilot status.

## G6 refined HOST execution — 2026-11-09

G6 partially_verified: refined HOST packet authorized and applied — two cache files and 210 target files verified by readback. Fresh target session did not launch: App API cannot select arbitrary cwd, elevated CLI stopped by auto-review, sandbox CLI cannot open local state. Normal user launch of existing host-target in Codex App needed without repeat authorization. Pilots not_run; acceptance null; T34 no-go.

[Current receipt](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/superpowers/specs/paos-aud-g6-refined-host-execution.json). Cache backup and target rollback manifest retained. First apply attempt rejected due to incorrect blocking_hooks value type; field corrected to PreToolUse, then apply exit 0 and 210/210 byte readback. Full unittest rerun unnecessary: runtime sources unchanged since previous verified fix. Docs checks — refined-docs.log; check_docs/matrix/state/diff — refined-checks.log. Historical blockers below not renamed as success; HOST/GAP tasks remain blocked.

## G6 approved execution — 2026-11-09

Final local verification: full unittest 1342 tests, 796.146 s, exit 1 (one obsolete expected file count 209→210; one expected platform skip). Corrected exact regression rerun: 1 test, 58.423 s, exit 0. Focused 108 and docs/lifecycle 112 passed; fixtures 91/91, transcripts 26/26; docs/matrix/state/hook/diff gates passed. Full suite was not rerun after the count-only test correction. Final docs refresh is in approved-docs-final.log.

G6 partially_verified: all three packets owner-authorized. Cache: 185 files updated with backup/readback; after local handler fix new two-file diff awaits review. T34: approved/unconsumed, no-go pending tools/context isolation; 0 primary/reviewer calls. HOST-01 invocation unconfirmed. HOST-02: handler omission fixed locally, target activation unproven. Three pilots not_run due to host dependency; owner acceptance absent.

Owning evidence: [approved execution](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/superpowers/specs/paos-aud-g6-approved-execution.json),
[T34 results](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/superpowers/specs/batch45-code-quality-eval-results.json) and
[no-go decision](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/superpowers/specs/batch45-code-quality-promotion-decision.json).
Two owner-approved verification chats have independent IDs and their own markers:
`01a1c072-9005-7d22-bc0b-f832e57bbcb1`, `01a1c072-b0d8-7732-822c-af95aa89a639`.
Their observations do not replace complete positive/negative generated-target acceptance.

CLI `--version`, `login status`, `exec --help` — exit 0: 0.167.0, ChatGPT login.
`debug prompt-input` initially exit 1 (Access denied to service paths), after approved
escalation exit 0: ambient project context discovered. Raw prompt not retained;
receipt stores only hash/size/boolean indicators. Frozen readiness/design/context hashes matched.
Specified design requires tools=[] and no ambient skills/hooks/AGENTS;
supported exact transport with demonstrated isolation was not confirmed. No guards
were disabled and no-tool prompt was not represented as an empty tool schema.
Official reference: [configuration controls](https://learn.chatgpt.com/docs/config-file/config-reference).
This is a local preflight gap, not a claim that future CLI versions cannot support this mode.

Continuation checks: docs suite, check_docs.py, task-matrix/state consistency and
git diff --check; exact results in approved-*.log under reports. Full local suite
1341/91/26 above belongs to previous run; full gate rerun after new handler fix (approved-full.log).
HOST-02 found missing staged comment advisory handler. Registration fixed;
runtime formatting preserved without ambiguous template marker, active/template parity maintained.
RED: missing-handler assertion; GREEN: 108 focused tests; dry-run/stage exit 0,
all six handlers present. [Repair receipt](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/superpowers/specs/paos-aud-g6-handler-repair.json).
After fix cache differs by two files: [exact preview](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/superpowers/specs/paos-aud-g6-cache-repair-preview.json).
Original host packet requires stop on source drift; new bytes not installed,
trust not updated. Source hashes from two fresh chats refer to state before fix.
Control plans, RU/EN current-state/registry and B44 followup synchronized.
prod_test.md: not_applicable. Site not rebuilt. Cache backup retained; rollback
only reviewed changed rows. Neither T34 nor HOST/GAP parent declared complete.

## G6 execution evidence — 2026-11-09 (historical local phase)

Status: `partially_verified`; audit not wholly closed. T30–T33 implemented locally;
T34 — approved_preflight_blocked / no-go; HOST-01/HOST-02 separately open; GAP-06 owner accepted 10.11.2026.
Canonical B45 evidence: `B45-CQRR-A07`, `docs/superpowers/specs/batch45-code-quality-local-readiness.json`.
One executor, zero delegation, context_mode=self_review; worktree clean at start.

| Gate | Current-run observation |
| --- | --- |
| Reviewer RED/GREEN | Initial missing-API smoke was setup error, not RED. Then 7 intended assertion failures for leaks/invalid pairs; GREEN 4 tests, rubric assertion later added to full suite |
| Versioned schema RED/GREEN | New CQ03 no-op initially quarantined; additive schema and explicit evaluator no-change contract passed, legacy schema retained |
| `python -B -m unittest` focused modules | 50 tests passed, 11.969 s; reviewer/corpus/design/metrics/behavior/promotion/model-output |
| Corpus replay | 12 input outcomes, 12 reference passes and 12 seeded oracle failures; Python/JavaScript/SQLite/PowerShell, 7 risk classes; no model outputs |
| `python -B -m unittest discover -s tests -p 'test_*.py' -v` | 1341 tests, 1581.125 s, OK (skipped=1), exit 0 |
| Task-state follow-up | A07 metadata support RED/GREEN; all 7 lifecycle tests passed after full-suite import; unknown IDs remain rejected |
| Docs tests | 105 passed; final sync rerun recorded in `.docs-tools/reports/paos-aud-g6/docs-final.log` |
| Fixture / transcript eval | 91/91 and 26/26, exit 0 |
| Compatibility / hook validators | exit 0, local structure only; explicit cache observation reports drift |
| Source/build hygiene | check_docs.py and git diff --check passed; final pointer/matrix/docs checks recorded after synchronization |

T30 uses closed allowlisted blinded packets, random opaque IDs, patch-bound deterministic
receipts and a hash-bound reviewer response. Labels/self-scores are excluded; text leaks
fail closed. Critical/high findings override scores. Receipt authentication and actual
reviewer independence require separate execution evidence; no live reviewer ran.
T31 source/check/reference/seeded files are synthetic, hashes frozen before any generation.
Scoped privacy scan and manual authored-content review found no secrets/private data.
T32 changes only the compact pre-edit instruction; both arms use proposed gpt-6.1-sol/medium,
same runner/timeout/tools/corpus. Compiler checks source hashes and exposes only intent,
acceptance and input source; no oracle or ambient skills/hooks. T33 is local readiness,
not behavioral promotion. Performance oracle counts equality work, not elapsed speedup.

HOST-01: read-only cache comparison found drift; full preview lists 185 add/replace rows,
0 extras. No cache write. Preview: `docs/superpowers/specs/paos-aud-g6-host-approval-preview.json`;
exact per-file digests: `.docs-tools/reports/paos-aud-g6/cache-file-preview.json`.
Observed current-session terminal-marker denial is not fresh-host evidence. Client version,
actual selected skill, trust and observed model remain unverified; two fresh chats and
disposable generated-target activation remain open. Exact report-grant hash requires fresh
session IDs and a separately reviewed definition; no blanket trust permission is inferred.

Automatic approval review rejected `codex --version; codex exec --help` as a potential
separate autonomous-agent launch outside the declared scope. It was not executed or
retried indirectly. The separate bounded CLI scope is included in the pending packet.

T34 approval packet was prepared only after local preflight passed:
`docs/superpowers/specs/batch45-code-quality-eval-approval-packet.json`. Proposed cap:
24 primary + 12 independent reviewer calls, 180 s/call; existing Codex allowance only,
no separately billed API. Missing cost/usage evidence keeps no-go. Approval is absent,
not consumed; no results or promotion-decision success is fabricated.
Pilot proposal: `docs/superpowers/specs/paos-aud-g6-pilot-proposal.json`; three bounded
synthetic bug/config/no-new-code targets. Owner approval and feedback are missing.
Pilot inputs were separated from the held-out corpus before any model outputs;
T34 is not a dependency of this owner pilot.

Control-plane sync: five root files and RU/EN current-state/registry updated; ordinary
and lifecycle owning plans receive scoped handoff. B44 gets a pending proposal pointer,
not new acceptance. prod_test.md not_applicable: no B39 production evidence created.
Root site remains the G5 build; G6 source updates are not claimed as a new site build.
Rollback only G6 files/hunks; restore prior owning pointers after review. No Git actions,
dependency installation, cache/trust changes, live calls or publication performed.

## PAOS-AUD-G1 — execution evidence 09.11.2026

Scope: five G1 cards; exact file manifest matches card Scope, two related F12 callers and
shared docs/control-plane scope. One executor, self_review; no subagents launched.
Baseline: clean worktree. Runtime/model/provider, trust, ACL and target changes
not authorized by this record. Host acceptance remains AUD-HOST-02/G6.

### RED and fixes

- F06: new test_read_classification_rejects_compound_and_unknown_writes — exit 1,
  five failures; after fix exit 0. Attempt to add inert dangerous-command example
  to patch initially blocked by active hook — current false-deny evidence.
  After source classification fix test_patch_prose_is_not_an_executable_command
  checks data and actual execution separately. Source mirror synchronized;
  this is not a fresh-host activation receipt.
- F12: expected discovery path fixed in tests before implementation. First
  merge suite run: 35 setup errors due to sandbox TEMP; not RED. After workspace TEMP
  test_unapproved_hooks_json_remains_companion_only_and_not_written — exit 1,
  approved_targets mismatch. After mapping fix all 35 merge tests exit 0.
- F11: native `codex execpolicy check --rules .rules -- rg --files` — exit 1,
  invalid not_match. After first fix another parser defect found:
  unquoted Windows backslashes in match examples. Examples and semantics fixed.
  Result: rg --files → prompt; rg --replace value → no matched rules;
  python create_task_plan.py new --output ../outside.md → prompt;
  icacls example /remove:d S-1-5-21-123 → forbidden; all four checks exit 0.
  Command arguments were not executed. CLI reported inaccessible
  user-level arg0 TEMP warning; policy JSON obtained. Proposal not installed/activated.
  Decision: do not retain broad allow rules that fail to constrain trailing arguments.
- F07: new repair contract test — exit 1, missing _acl_text/API; GREEN:
  exact target/SID/digest, backup/restore, foreign DENY preservation for generated
  commands, drift/reparse denial. No actual ACL mutation performed.
- F18: authoring scenario — exit 1, missing separate API; builder test — exit 1,
  missing build_report_authoring_call. GREEN: v2 opt-in, create and two updates,
  stale digest, path/session/marker mismatch, expiry, terminal, aliases/reparse,
  mixed patch rejection. Legacy v1 suite preserved. CAS preflight is not
  atomic write: one writer required; race after hook return is an explicit limitation.

### Intermediate checks

- `python -B -m unittest tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_infrastructure_templates -q`: 132 tests, exit 1, three failures (old active mirror, bounded Select-Object pipeline, template placeholder regex). Parity, bounded pipeline and digest regex corrected.
- Five affected modules: 183 tests, 13.604 s, OK (skipped=1), exit 0.
- After extra negative/rollback tests four changed modules: 89 tests, 12.465 s, OK (skipped=1), exit 0.
- All Python checks use `PYTHONDONTWRITEBYTECODE=1`, `TEMP=TMP=<workspace>/.codex-tmp/paos-aud-g1`; real target files and ACL unchanged.

### Final checks

- Native rules parser, three validate_hooks targets, transcript eval 26/26,
  check_docs.py — exit 0.
- validate_codex_compatibility.py — exit 1, needs_review:
  legacy_flat_mcp_requires_schema_review. Existing G2/F01 contract gap;
  G1 does not change MCP package or declare compatibility proven.
- Task matrix initially rejected: appended evidence entered last task card
  and was detected as unresolved placeholder. Evidence moved before
  cards; repeat validator exit 0, errors=[].
- Dry-run and staging CLI on existing-codex-config fixture — both exit 0;
  manifest and staged .codex/hooks.json exist, nested mirror absent.
- Self-review added F06 regression for tool metadata/unknown tool: RED exit 1,
  executable text included workdir/justification; payload extraction fixed.
- Final affected rerun initially: 185 tests, failures=2, errors=1, skipped=1.
  Windows TEMP cleanup sharing violation reproducibility unconfirmed;
  isolated TEMP for concurrent checks. Two contract regressions corrected:
  legacy command envelope without tool_name and Python null-value word in rendered
  template, incorrectly recognized by old placeholder assertion.
- First fixture eval failed with UnboundLocalError; full discovery stopped after
  repeated fixture errors. F12 cause: two fixture exercise callers still
  used old hooks path. Additional necessary file scope:
  plugins/product-agent-os/scripts/run_fixture_eval.py and
  tests/product_agent_os/test_infrastructure_renderer.py. Only
  expected paths/callers corrected; error handling and other gates not weakened.
- After path fixes: fixture eval — exit 0, 91/91 passed.
- Affected suite after TEMP isolation: 216 tests, 40.024 s, OK (skipped=1), exit 0.
  Intermediate 216-test run had only Windows cleanup WinError 32;
  new TEMP: .docs-tools/reports/paos-aud-g1/tmp, ignored directory.
- `icacls /?` (read-only help) and Microsoft official reference confirm
  /inheritance:d (copies ACEs), /remove:d *SID, DACL /save and /restore;
  snapshot does not preserve owner/SACL/integrity labels and helper does not modify them.
- `python -B -m unittest discover -s tests -p 'test_*.py' -v`: 1297 tests,
  532.640 s, OK (skipped=1), exit 0. Sole skip is non-Windows guard on Windows.
  This run started before final F12 alias hardening; its evidence does not
  replace subsequent focused retest of changed merge module.
- Final F12 self-review: ./, case, separator and trailing-dot aliases of discovery
  path bypassed special hook gate (4 RED failures). Canonical-path
  rejection added. After change `python -B -m unittest
  tests.product_agent_os.test_merge_infrastructure
  tests.product_agent_os.test_infrastructure_renderer -q`: 67 tests,
  16.645 s, OK, exit 0. Other unchanged modules were not rerun.
- `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v`:
  100 tests, 4.415 s, OK, exit 0; final status-only docs gate recorded below.
- Final validate_hooks: active definition, active scripts and packaged hooks —
  exit 0 each. AST/parity hook/workflow — PASS. .codex/hooks.json,
  .codex/hooks/hooks.json and .codex/config.toml match baseline HEAD
  with line endings normalized. Root site not rebuilt and freshness not claimed.

### Acceptance mapping and self-review

| Task | Local result | Evidence | Separate boundary |
| --- | --- | --- | --- |
| F06 | Whole bounded command, metadata separation, unknown mutation scope, inert patch prose | Lifecycle positive/negative suite; active/package parity | Not a universal shell parser; native sandbox/approval retained |
| F12 | One discovery path, manifest/config agreement, existing file preservation, synthetic apply/rollback, alias denial | Dry-run/stage CLI; 36 merge and 31 renderer tests | Trust/real target apply not performed |
| F11 | Valid native parser; no broad allow; proposal retained | Four execpolicy decisions above | Discovery rules not installed |
| F07 | Explicit single target/SID, digest, DACL backup/restore, preservation and reparse guards | 9 Windows permissions tests, including one platform skip; mocked icacls | Real ACL and rollback acceptance separate |
| F18 | Pinned v2 authoring, previous digest, exact session/path, full-file update, legacy v1 preserved | Lifecycle and builder/validator regressions | Preflight non-atomic; exclusive writer; host gate G6 |

Review context: self_review; tester_verdict=closed_allowed only for local G1.
No blocking local findings after fixes. Independent reviewer was not
launched. Existing MCP compatibility gap remains G2/F01. LLM behavioral thresholds
unchanged; live model/provider calls were unnecessary and not run.
Rollback: revert only listed G1 hunks, preserving foreign session marker and
parallel .hallmark/other artifacts. Own session marker is service record,
not evidence of hook activation.



### Final status-only closure check

After updating five cards: validate_task_matrix.py — exit 0, errors=[];
check_docs.py — exit 0; docs unittest — 100 tests, 3.118 s, OK, exit 0.
Checked 5 implemented / 21 planned, five root files below 50 KB,
UTF-8 without replacement characters, changed Python AST and parity mirrors.
Global `git diff --check` — exit 2 due to new blank line at EOF in concurrently
changed Web architecture/M1-wireframes/PRD research docs (outside G1). They were
not edited. `git diff --check --` with exact manifest of 30 G1-owned files — exit 0.
This separates scope explicitly; neither successful global check nor G1 gate waiver.
Foreign lifecycle marker, .hallmark and other parallel changes preserved.

### Verified source state

SHA-256 exact file bytes; active/package parity confirmed separately.

| File | SHA-256 |
| --- | --- |
| `.codex/hooks/pre_tool_use_policy.py` | `cd78b4f34db916c622f17dfa8e275f97e30143525caaf60b25a13b416d23326b` |
| `.codex/workflows/task-plan-lifecycle.md` | `962e90330c7a6e5838252eb8f866c111742d3fc65a164e991ab8f020c149e741` |
| `.rules` | `0613c81e78076f22c4597e5b209b425f3370e00c569128cb05e764890f409d4f` |
| `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py` | `01140b699c8379e1d2dd379855f7230a575a4a8038100e01a1947edb80c58b3d` |
| `plugins/product-agent-os/scripts/product_agent_os/windows_codex_permissions.py` | `2343e407678ca325b49fdaf088d88fbe7471d8bd06b132af16b0f478c33d5ecb` |
| `plugins/product-agent-os/scripts/product_agent_os/task_plan_lifecycle.py` | `182ee6132e5508544198567c929a53c8850666062235a7c369f237286ceb885a` |
| `plugins/product-agent-os/scripts/product_agent_os/validators.py` | `0add6b2bb429bf12867ea4cfa83087c5eab1f918c330e556c2d9e5f3600e2ed2` |
| `plugins/product-agent-os/scripts/product_agent_os/templates.py` | `05dd4f9754b7826efbe90ff165464d4d72db6c45b5f7ffd7381ec77aa3ce36bc` |
| `plugins/product-agent-os/assets/templates/config/config.toml` | `68673ae1a9941a1424b8b9536204657e3d84a5aa1c7a397233eba7abcb9ef5c0` |

Local raw outputs retained under ignored `.docs-tools/reports/paos-aud-g1/`;
early and integrated logs moved from own TEMP into `initial-and-integrated-runs/`.
Durable receipt is this plan; raw logs are not a second status registry.

### Control-plane sync

REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG: update_required and updated for scope, sequencing,
verification, failure classes and handoff. prod_test.md: not_applicable (Batch 39
unaffected). Registry RU/EN and runtime docs RU/EN synchronized; workflow mirrors
aligned. Site/navigation/diagrams: not_applicable; no build/activation claimed.
Overflow: all five root files below 50 KB; redistribution unnecessary. Handoff: G2 after local gates, G6 for
host acceptance; no other mandatory local handoffs.


## PAOS-AUD-G1 — Reliable hooks, rules and installation

- **ID:** `PAOS-AUD-G1`
- **Execution status:** `implemented_locally_verified`; five local acceptance contracts closed. Next group: G2; host acceptance remains G6.
- **Group name:** Reliable hooks, rules and installation
- **Group description:** Resolve remaining action classification and generated onboarding defects; bound ACL repair and add safe sequential report maintenance. Preserve implemented session isolation.
- **Technical value (for the project):** Aligned active/package contracts, exact write boundaries and correct staging/merge paths.
- **Product value (for the user):** Fewer false blocks and repeat approvals without weakening user-file protection.
- **Affected files:** `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`; `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/scripts/product_agent_os/windows_codex_permissions.py`; `.rules`. Full task-specific scope in cards.
- **Group acceptance criteria:** All five cards have local positive/negative evidence; active/package mirrors aligned; no automatic hooks/rules activation or working ACL changes. Host acceptance closes separately in G6.
- **Dependencies and order:** Start first. F06 before F18; F12 independently fixable in owned files, integrated host probe after final hooks. ACL and rules are independent bounded changes.
- **Suggested ownership:** plugin-runtime-builder; assurance — security-privacy-supply-chain-reviewer.

### Task `PAOS-AUD-F06`

- ID: `PAOS-AUD-F06`
- Task: **Task name:** Fix remaining command and patch classification defects
- Short description: **Task description:** Distinguish executable command, arguments and patch content. Do not classify a whole compound command as read-only by initial prefix; route unknown forms to bounded review. Preserve session-bound selector, exact bootstrap, sandbox and approvals; do not write universal shell interpreter.
- Technical value: **Technical value (for the project):** Eliminate PreToolUse false allow and false deny without expanding authority.
- Product value: **Product value (for the user):** Ordinary reads and documentation examples are not incorrectly blocked, while potential writes are consistently checked.
- Scope: **Affected files:** `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `tests/product_agent_os/test_lifecycle_hooks.py`. Shared docs/control-plane scope under rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Inert cases: pure read allowed; compound read/write line not classified as pure read; unknown write not allowed via no match. 2) Mention of dangerous command as data in ordinary Markdown not treated as execution; actual destructive/path/secret checks retained. 3) Own/foreign/mixed marker, Windows case handling and session isolation regressions pass; active/package files match.
- Group: PAOS-AUD-G1
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for full local PAOS-AUD-G1 implementation.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 12:47
- Depends on: No new mandatory tasks in this plan. PAOS-SESSION-LIFECYCLE-2026-11-09 — reuse, do not redo.
- Blocks: PAOS-AUD-F18, PAOS-AUD-HOST-02; for F05 only incremental report scenario.
- Source: F06; subsequent session-lifecycle repair already closed exact marker bootstrap and chat isolation.
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Eliminate PreToolUse false allow and false deny without expanding authority. Missing host/product gates remain open.
- Verification gates: RED/GREEN in test_lifecycle_hooks; validate_hooks.py for active/package definitions; AST/parity; fresh host separately AUD-HOST-02. Shared gates — TEST.md and rules above.
- Risks / approval gates: high; definition/trust change and host probe excluded from local repair. Rollback per shared rules.
- Complexity: high
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: plugin-runtime-builder; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Scope files and evidence in owning plan; proposed paths not yet present.
- Next step: Local G1 closed; G2 subsequently completed, host acceptance separate G6.

#### Completion Report

- status: implemented
- what was done: Fixed whole-command classification, metadata extraction, conservative unknown route and patch destination/data separation; session isolation preserved.
- files touched / work locations: .codex/hooks/pre_tool_use_policy.py; packaged mirror; test_lifecycle_hooks.py
- technical value delivered: False allow/deny eliminated in stated local cases.
- product value delivered: Reads and Markdown examples do not demand false mutation approval.
- actual implementation date and time: 09-11-2026 12:47
- verification evidence: Lifecycle suite, full 1297, final source parity; RED/GREEN in execution evidence.
- residual risks: Local verification only; host/trust and real ACL not proven. MCP compatibility gap resolved in G2. Detailed limits in execution evidence.
- follow-up: G2 completed; AUD-HOST-02 and real ACL acceptance remain separate authorized scenarios.


### Task `PAOS-AUD-F12`

- ID: `PAOS-AUD-F12`
- Task: **Task name:** Align generated hooks config and safe merge
- Short description: **Task description:** Fix templates/merge mapping to discovered .codex/hooks.json; align manifest and generated config. Preserve existing user-authored hooks. Explicitly separate staging, approved apply and actual activation.
- Technical value: **Technical value (for the project):** Remove mismatch between generated filesystem layout and loading contract.
- Product value: **Product value (for the user):** Installation does not imply a hook is enabled when host will not load it.
- Scope: **Affected files:** `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`; `plugins/product-agent-os/assets/templates/config/config.toml`; `tests/product_agent_os/test_merge_infrastructure.py`; `tests/product_agent_os/test_infrastructure_templates.py`; related callers `plugins/product-agent-os/scripts/run_fixture_eval.py` and `tests/product_agent_os/test_infrastructure_renderer.py`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Dry-run, staging manifest and config specify one correct path; mirror is not discovery config. 2) Existing unmarked config not overwritten; approved merge/rollback tested in synthetic workspace. 3) Test checks actual expected discovery path; installation result does not claim trust/activation proven.
- Group: PAOS-AUD-G1
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for full local PAOS-AUD-G1 implementation.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 12:47
- Depends on: No hard local code dependency; integration/host probe follows final F06.
- Blocks: PAOS-AUD-HOST-02
- Source: F12
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Remove mismatch between generated filesystem layout and loading contract. Missing host/product gates remain open.
- Verification gates: Focused infrastructure/merge tests and dry-run on synthetic fixtures; actual target activation separately AUD-HOST-02. Shared gates — TEST.md and rules above.
- Risks / approval gates: high; real target apply and trust require their own exact authority. Rollback per shared rules.
- Complexity: medium
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: plugin-runtime-builder; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Scope files and evidence in owning plan; proposed paths not yet present.
- Next step: Local G1 closed; G2 subsequently completed, host acceptance separate G6.

#### Completion Report

- status: implemented
- what was done: Generated hook definition moved to .codex/hooks.json; merge approval/rollback and alias rejection aligned; renderer/eval callers updated.
- files touched / work locations: templates.py; merge_infrastructure.py; template config.toml; run_fixture_eval.py; test_merge_infrastructure.py; test_infrastructure_templates.py; test_infrastructure_renderer.py
- technical value delivered: Manifest/config/merge use one discovery path with separate activation gate.
- product value delivered: Installation preserves existing hooks and explicitly separates staging from activation.
- actual implementation date and time: 09-11-2026 12:47
- verification evidence: Dry-run/staging exit 0; full 1297; final 67 merge/renderer tests after alias fix; fixture 91/91.
- residual risks: Local verification only; host/trust and real ACL not proven. MCP compatibility gap resolved in G2. Detailed limits in execution evidence.
- follow-up: G2 completed; AUD-HOST-02 and real ACL acceptance remain separate authorized scenarios.


### Task `PAOS-AUD-F11`

- ID: `PAOS-AUD-F11`
- Task: **Task name:** Fix rules-file semantics and status
- Short description: **Task description:** Remove use of not_match as exclusion; choose narrow patterns and correct check examples. Separately determine whether file remains proposal or moves to discovery path under authorized activation. Do not activate broad allows by simply moving it.
- Technical value: **Technical value (for the project):** Native parser accepts policy and permissions match verifiable contract.
- Product value: **Product value (for the user):** User understands which commands are actually permitted and whether policy is active.
- Scope: **Affected files:** `.rules`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) codex execpolicy check accepts file and gives expected decisions for positive/negative cases. 2) Patterns do not expand previous declared authority; potentially dangerous variants receive no broad allow. 3) Actual loading status stated separately; .codex/rules/default.rules not created without separate activation decision.
- Group: PAOS-AUD-G1
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for full local PAOS-AUD-G1 implementation.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 12:47
- Depends on: No new mandatory tasks in this plan.
- Blocks: No mandatory downstream implementation dependency in this document; own acceptance gate retained.
- Source: F11
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Native parser accepts policy and permissions match verifiable contract. Missing host/product gates remain open.
- Verification gates: Native execpolicy parser/check on fixed inert arguments; docs checks. No execution of allowed commands required. Shared gates — TEST.md and rules above.
- Risks / approval gates: high; rules relocation/activation is separate approval boundary. Rollback per shared rules.
- Complexity: medium
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: security-privacy-supply-chain-reviewer for read-only review; plugin-runtime-builder for edits; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Scope files and evidence in owning plan; proposed paths not yet present.
- Next step: Local G1 closed; G2 subsequently completed, host acceptance separate G6.

#### Completion Report

- status: implemented
- what was done: Fixed not_match semantics and Windows path examples; broad allows replaced with review decisions; .rules retained as proposal.
- files touched / work locations: .rules; docs/runtime/worktrees-hooks-rules.md and .en.md; registry RU/EN
- technical value delivered: Native parser accepts proposal; dangerous trailing arguments do not receive broad allow.
- product value delivered: Loading status and need for review explicitly stated.
- actual implementation date and time: 09-11-2026 12:47
- verification evidence: Four codex execpolicy checks: exit 0; prompt/no-match/prompt/forbidden; docs tests/checker.
- residual risks: Local verification only; host/trust and real ACL not proven. MCP compatibility gap resolved in G2. Detailed limits in execution evidence.
- follow-up: G2 completed; AUD-HOST-02 and real ACL acceptance remain separate authorized scenarios.


### Task `PAOS-AUD-F07`

- ID: `PAOS-AUD-F07`
- Task: **Task name:** Exclude broad ACL repair from onboarding
- Short description: **Task description:** Remove normal-onboarding broad ACL repair recommendation. If helper remains available as repair tool, constrain target/SID, prohibit ambiguous reparse paths, add preview, ACL snapshot/restore and apply binding to agreed plan digest.
- Technical value: **Technical value (for the project):** Preserve system and project deny ACE; reversible bounded permissions repair.
- Product value: **Product value (for the user):** Product-Agent OS setup does not remove user access restrictions or require dangerous universal repair.
- Scope: **Affected files:** `plugins/product-agent-os/scripts/product_agent_os/windows_codex_permissions.py`; `plugins/product-agent-os/scripts/prepare_windows_codex_permissions.py`; `tests/product_agent_os/test_windows_codex_permissions.py`; `plugins/product-agent-os/README.md`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Default/help/onboarding do not propose broad apply; dry-run leaves ACL unchanged. 2) Foreign DENY SID not removed; unexpected target, digest drift and reparse ambiguity stop apply. 3) Backup/restore and command construction tested via existing mock/stub layer; actual ACL acceptance explicitly remains separate authorized scenario.
- Group: PAOS-AUD-G1
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for full local PAOS-AUD-G1 implementation.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 12:47
- Depends on: No new mandatory tasks in this plan.
- Blocks: No mandatory downstream implementation dependency in this document; own acceptance gate retained.
- Source: F07
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Preserve system and project deny ACE; reversible bounded permissions repair. Missing host/product gates remain open.
- Verification gates: test_windows_codex_permissions: command contract, SID/path allowlist, digest mismatch, rollback preservation. No actual icacls apply. Shared gates — TEST.md and rules above.
- Risks / approval gates: high; real ACL/permissions changes require exact target, owner and rollback. Rollback per shared rules.
- Complexity: high
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: plugin-runtime-builder; independent review security-privacy-supply-chain-reviewer; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Scope files and evidence in owning plan; proposed paths not yet present.
- Next step: Local G1 closed; G2 subsequently completed, host acceptance separate G6.

#### Completion Report

- status: implemented
- what was done: Broad onboarding apply replaced by single-target/SID repair with plan digest, DACL snapshot/restore, reparse/drift rejection and rollback on failure.
- files touched / work locations: windows_codex_permissions.py; prepare_windows_codex_permissions.py; test_windows_codex_permissions.py; plugin README.md
- technical value delivered: Foreign DENY SID not removed; operations restricted to reviewed plan.
- product value delivered: Ordinary onboarding remains diagnostic; repair has preview and recovery route.
- actual implementation date and time: 09-11-2026 12:47
- verification evidence: Permissions mock tests in affected 216 and full 1297; default no-apply, selected SID, drift, reparse, restore failure tests; native help readback.
- residual risks: Local verification only; host/trust and real ACL not proven. MCP compatibility gap resolved in G2. Detailed limits in execution evidence.
- follow-up: G2 completed; AUD-HOST-02 and real ACL acceptance remain separate authorized scenarios.


### Task `PAOS-AUD-F18`

- ID: `PAOS-AUD-F18`
- Task: **Task name:** Add bounded sequential authoring of one report
- Short description: **Task description:** Design separate opt-in report-authoring scope for one exact Markdown path: create/update, expected previous digest, expiry, session ownership and terminal handling. Define honest representation of this work type in lifecycle schema. Do not silently extend existing create-only grant.
- Technical value: **Technical value (for the project):** Support incremental research without general write permission or disguising documentation as runtime implementation.
- Product value: **Product value (for the user):** Observations saved during work without manually unlocking each write.
- Scope: **Affected files:** `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/scripts/product_agent_os/task_plan_lifecycle.py`; `plugins/product-agent-os/scripts/product_agent_os/validators.py`; `.codex/workflows/task-plan-lifecycle.md`; `plugins/product-agent-os/assets/templates/workflows/task-plan-lifecycle.md`; `tests/product_agent_os/test_lifecycle_hooks.py`; `tests/product_agent_os/test_task_plan_lifecycle.py`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Multiple sequential updates to own exact report pass with matching digest and valid scope. 2) Foreign marker/path, stale digest, expired grant, terminal state, symlink/alias and mixed patch denied. 3) Legacy create-only behavior preserved; new authoring authority explicit and does not change sandbox/trust. 4) Concurrent report edit yields conflict, not silent overwrite; host behavior closes separately.
- Group: PAOS-AUD-G1
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for full local PAOS-AUD-G1 implementation.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 12:47
- Depends on: PAOS-AUD-F06
- Blocks: PAOS-AUD-HOST-02; for F05 only incremental report scenario.
- Source: F18; GAP-05 create-only grant; session isolation already implemented.
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Support incremental research without general write permission or disguising documentation as runtime implementation. Missing host/product gates remain open.
- Verification gates: Contract design + focused lifecycle/validators RED/GREEN tests; source parity; AUD-HOST-02 after final hashes. Shared gates — TEST.md and rules above.
- Risks / approval gates: high; changing opt-in grant does not authorize activation in hook definition. Rollback per shared rules.
- Complexity: high
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: lifecycle-orchestrator; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Scope files and evidence in owning plan; proposed paths not yet present.
- Next step: Local G1 closed; G2 subsequently completed, host acceptance separate G6.

#### Completion Report

- status: implemented
- what was done: Added separate opt-in work_type report_authoring, v2 grant/session/expiry, previous-digest conflict check and whole-report create/update builder; v1 retained.
- files touched / work locations: active/package pre_tool_use_policy.py and workflow; task_plan_lifecycle.py; validators.py; lifecycle/task-plan tests
- technical value delivered: Sequential writes to one report bounded by exact path, grant and session.
- product value delivered: Report can be accumulated without general mutation scope or reissuing grant for every version.
- actual implementation date and time: 09-11-2026 12:47
- verification evidence: Create + two updates, stale digest, foreign path/session/marker, expiry, terminal, alias/reparse/mixed denial; affected 216; full 1297.
- residual risks: Local verification only; host/trust and real ACL not proven. MCP compatibility gap resolved in G2. Detailed limits in execution evidence.
- follow-up: G2 completed; AUD-HOST-02 and real ACL acceptance remain separate authorized scenarios.

## PAOS-AUD-G2 — Package compatibility and host diagnostics

- **ID:** `PAOS-AUD-G2`
- **Status:** `implemented_locally_verified`; F01/F02/F04 complete, next G3.
- **Group name:** Package compatibility and host diagnostics
- **Group description:** Fix MCP declaration, capability matrix and extend existing compatibility report with observed host/model/provenance data.
- **Technical value (for the project):** One package schema and surface capability diagnostic source without new doctor framework.
- **Product value (for the user):** User sees what is available, unsupported and not yet verified.
- **Affected files:** `plugins/product-agent-os/.mcp.json`; `plugins/product-agent-os/.codex-plugin/plugin.json`; `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py`; `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py`; `plugins/product-agent-os/scripts/validate_codex_compatibility.py`; `tests/product_agent_os/test_codex_compatibility.py`. Full task-specific scope in cards.
- **Group acceptance criteria:** Supported local package passes compatibility check; unsupported and not_verified distinguished; version/model/cache/trust do not receive invented values.
- **Dependencies and order:** Independent of G1 with separate owner. F01 and F02 before F04. Output used by G5/G6.
- **Suggested ownership:** plugin-runtime-builder.


### Task `PAOS-AUD-F01`

- ID: `PAOS-AUD-F01`
- Task: **Task name:** Fix MCP declaration and distribution metadata
- Short description: **Task description:** Fix flat .mcp.json within supported current manifest format; check resolver precedence. Check placeholder publisher/URLs: use only confirmed owner data, otherwise explicitly leave distribution gate open.
- Technical value: **Technical value (for the project):** Compatible package without unnecessary wholesale migration to portable format.
- Product value: **Product value (for the user):** Package installs under clear contract and does not mislead about publisher.
- Scope: **Affected files:** `plugins/product-agent-os/.mcp.json`; `plugins/product-agent-os/.codex-plugin/plugin.json`; `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py`; `tests/product_agent_os/test_codex_compatibility.py`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Current package passes local MCP-shape compatibility check; malformed/ambiguous fixtures remain rejected/needs_review. 2) Legacy manifest preserved without separate portability requirement; two independent manifest authorities not mixed. 3) Publisher/URLs checked or distribution explicitly gated; structure check does not launch MCP server.
- Group: PAOS-AUD-G2
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for full local G2 implementation with checks; external boundaries retained.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 13:16
- Depends on: No new mandatory tasks in this plan.
- Blocks: PAOS-AUD-F04, PAOS-AUD-F14, PAOS-AUD-HOST-01
- Source: F01
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Compatible package without unnecessary wholesale migration to portable format. Missing host/product gates remain open.
- Verification gates: validate_codex_compatibility.py; existing component/compatibility fixtures; JSON syntax and resolver regression. Shared gates — TEST.md and rules above.
- Risks / approval gates: medium; do not invent unknown identity/URL; publication and MCP execution out of scope. Rollback per shared rules.
- Complexity: low
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: plugin-runtime-builder; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Implemented scope files; G2 execution evidence and SHA-256 in this plan.
- Next step: G3 completed; actual host acceptance and distribution gates separate.

#### Completion Report

- status: implemented
- what was done: Fixed MCP wrapper; rejected duplicate/ambiguous/unknown inputs; preserved portable precedence. Unconfirmed publisher/URLs replaced with explicit gated status.
- files touched / work locations: plugins/product-agent-os/.mcp.json; .codex-plugin/plugin.json; scripts/product_agent_os/plugin_components.py; tests/product_agent_os/test_codex_compatibility.py; test_plugin_structure.py; shared docs/control-plane.
- technical value delivered: Supported local structure without mixing authority.
- product value delivered: Clear package contract without false publisher attribution.
- actual implementation date and time: 09-11-2026 13:16
- verification evidence: G2 execution evidence above: RED; full 1305 OK (1 platform skip), 748.949 s, exit 0; final focused 122 OK, final contracts 22 OK; fixtures 91, transcript 26/26; compatibility exit 0; docs/hooks passed. Source state provenance and hashes retained.
- residual risks: Distribution publisher/URLs/icons gated; host activation/trust/account access and full package receipts not proven. T30–T34/G6 remain source-owned.
- follow-up: G3 completed. For actual host evidence — AUD-HOST-01/G6; publication and model promotion require their own gates.

### Task `PAOS-AUD-F02`

- ID: `PAOS-AUD-F02`
- Task: **Task name:** Separate support from verification of host capabilities
- Short description: **Task description:** In existing capability matrix distinguish documented support, unsupported and observed/not_verified for Codex App, CLI and IDE extension; distinguish native plugin and standalone skills.
- Technical value: **Technical value (for the project):** Typed capability contract without mixing impossible and not yet tested.
- Product value: **Product value (for the user):** User does not waste time trying to enable an unsupported feature.
- Scope: **Affected files:** `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py`; `tests/product_agent_os/test_codex_compatibility.py`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) App/CLI/IDE receive documented different capabilities; unsupported not replaced by requires_host_receipt. 2) Host receipt cannot promote documented unsupported to supported without updating source-backed contract. 3) Local structure scope and absence of activation evidence retained.
- Group: PAOS-AUD-G2
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for full local G2 implementation with checks; external boundaries retained.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 13:16
- Depends on: No new mandatory tasks in this plan.
- Blocks: PAOS-AUD-F04, PAOS-AUD-F14, PAOS-AUD-HOST-01
- Source: F02
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Typed capability contract without mixing impossible and not yet tested. Missing host/product gates remain open.
- Verification gates: Focused compatibility tests: surface/component matrix, unknown surface, unsupported versus unverified; current official sources at implementation. Shared gates — TEST.md and rules above.
- Risks / approval gates: medium; recheck capability facts on implementation date. Rollback per shared rules.
- Complexity: low
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: plugin-runtime-builder; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Implemented scope files; G2 execution evidence and SHA-256 in this plan.
- Next step: G3 completed; actual host acceptance and distribution gates separate.

#### Completion Report

- status: implemented
- what was done: Separated documented support and observation; IDE native plugin unsupported; receipt conflict does not promote capability; standalone skills separate.
- files touched / work locations: plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py; tests/product_agent_os/test_codex_compatibility.py; shared docs/control-plane.
- technical value delivered: Separate App/CLI/IDE capability contract.
- product value delivered: Unsupported feature not offered as awaiting activation.
- actual implementation date and time: 09-11-2026 13:16
- verification evidence: G2 execution evidence above: RED; full 1305 OK (1 platform skip), 748.949 s, exit 0; final focused 122 OK, final contracts 22 OK; fixtures 91, transcript 26/26; compatibility exit 0; docs/hooks passed. Source state provenance and hashes retained.
- residual risks: Distribution publisher/URLs/icons gated; host activation/trust/account access and full package receipts not proven. T30–T34/G6 remain source-owned.
- follow-up: G3 completed. For actual host evidence — AUD-HOST-01/G6; publication and model promotion require their own gates.

### Task `PAOS-AUD-F04`

- ID: `PAOS-AUD-F04`
- Task: **Task name:** Extend GPT-6 diagnostics and provenance without promotion claims
- Short description: **Task description:** Extend existing compatibility report with client version/surface, configured versus observed model, canonical/cache provenance and trust unknown/observed. Check client minimum only for specific documented surface. Do not change model pins or effort.
- Technical value: **Technical value (for the project):** One observable compatibility contract links configuration to available evidence.
- Product value: **Product value (for the user):** Shows why selected model or skill is not yet confirmed in current environment.
- Scope: **Affected files:** `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py`; `plugins/product-agent-os/scripts/validate_codex_compatibility.py`; `tests/product_agent_os/test_codex_compatibility.py`; `docs/codex/models-and-reasoning.md`; `docs/codex/models-and-reasoning.en.md`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Missing/old/unknown version, unavailable model receipt, source/cache drift and unknown trust explicitly shown. 2) Installed CLI not represented as verified App version or account availability. 3) No provider calls, cache writes, automatic effort increase or promotion based on model ID alone. 4) Read-only inputs/report process only allowlisted non-secret data; baseline T23–T29 preserved.
- Group: PAOS-AUD-G2
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for full local G2 implementation with checks; external boundaries retained.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 13:16
- Depends on: PAOS-AUD-F01, PAOS-AUD-F02
- Blocks: PAOS-AUD-F14, PAOS-AUD-HOST-01
- Source: F04 — local diagnostics; treatment quality remains B45-CQRR-T30–T34.
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: One observable compatibility contract links configuration to available evidence. Missing host/product gates remain open.
- Verification gates: Focused version/capability/provenance fixtures and read-only CLI output; actual host receipt — AUD-HOST-01. Shared gates — TEST.md and rules above.
- Risks / approval gates: medium; diagnostics require neither credential use nor changes to active profiles. Rollback per shared rules.
- Complexity: medium
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: plugin-runtime-builder; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Implemented scope files; G2 execution evidence and SHA-256 in this plan.
- Next step: G3 completed; actual host acceptance and distribution gates separate.

#### Completion Report

- status: implemented
- what was done: Added bounded allowlisted observations and explicit cache read-only comparison, version/model/trust diagnostics; CLI minimum applies only Terra/CLI. Symlink/junction rejected; model pins/effort retained.
- files touched / work locations: plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py; scripts/validate_codex_compatibility.py; tests/product_agent_os/test_codex_compatibility.py; docs/codex/models-and-reasoning.md and .en.md; shared docs/control-plane.
- technical value delivered: Configured/observed and canonical/cache evidence separated, unknown explicitly shown.
- product value delivered: Reasons for unconfirmed model, trust and selected skill source visible.
- actual implementation date and time: 09-11-2026 13:16
- verification evidence: G2 execution evidence above: RED; full 1305 OK (1 platform skip), 748.949 s, exit 0; final focused 122 OK, final contracts 22 OK; fixtures 91, transcript 26/26; compatibility exit 0; docs/hooks passed. Source state provenance and hashes retained.
- residual risks: Distribution publisher/URLs/icons gated; host activation/trust/account access and full package receipts not proven. T30–T34/G6 remain source-owned.
- follow-up: G3 completed. For actual host evidence — AUD-HOST-01/G6; publication and model promotion require their own gates.

## PAOS-AUD-G3 — Reliable evidence and current statuses

- **ID:** `PAOS-AUD-G3`
- **Group name:** Reliable evidence and current statuses
- **Group description:** Fix freshness parser, empty feedback and current-state precedence over historical receipts.
- **Technical value (for the project):** Eliminate false-positive and false missing signals without new status registry.
- **Product value (for the user):** Clear what was actually verified and what remains; absent data does not look like success.
- **Affected files:** `plugins/product-agent-os/scripts/product_agent_os/source_policy.py`; `plugins/product-agent-os/scripts/product_agent_os/self_learning_feedback.py`; `plugins/product-agent-os/scripts/product_agent_os/status_snapshot.py`; `PLAN.md`; `RUNLOG.md`; `TEST.md`. Full task-specific scope in cards.
- **Group acceptance criteria:** Unknown/empty/stale/conflicting cases produce correct results; current projections tied to source revision; history preserved.
- **Dependencies and order:** Independent of G1/G2 on core modules. One owner updates shared control-plane pointers sequentially.
- **Suggested ownership:** plugin-runtime-builder; feedback — learning-loop-engineer; projections — graph-cockpit-engineer.

### Task `PAOS-AUD-F03`

- ID: `PAOS-AUD-F03`
- Task: **Task name:** Fix freshness and source evidence classification
- Short description: **Task description:** Support used RU/EN date labels, strict calendar date validation and local registry references. Separate official behavior, project contract and historical receipt; do not treat mere Codex mention as behavioral claim.
- Technical value: **Technical value (for the project):** Fewer false missing/review results; date presence, freshness and semantic support remain distinct dimensions.
- Product value: **Product value (for the user):** User sees real source gaps instead of mass false warnings.
- Scope: **Affected files:** `plugins/product-agent-os/scripts/product_agent_os/source_policy.py`; `tests/product_agent_os/test_source_policy.py`; `docs/sources/registry.md`; `docs/sources/registry.en.md`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Russian 'Checked YYYY-MM-DD.' and actual EN forms recognized; invalid/future/missing/stale cases distinguished under explicit policy. 2) Registry reference resolved safely inside workspace; broken refs reported as missing evidence. 3) Project-local and historical claims receive no false official verdict; date/URL do not set claim_supported to verified without semantic review.
- Group: PAOS-AUD-G3
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for full local G3 implementation with checks.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 13:47
- Depends on: No new mandatory tasks in this plan.
- Blocks: PAOS-AUD-F17
- Source: F03
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Fewer false missing/review results; date presence, freshness and semantic support remain distinct dimensions. Missing host/product gates remain open.
- Verification gates: test_source_policy: formats, dates, registry resolution, claim classes; scan current docs and analyze changed findings, docs checks. Shared gates — TEST.md and rules above.
- Risks / approval gates: medium; retain exact-host URL and secret protections; do not turn scanner into crawler. Rollback per shared rules.
- Complexity: medium
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: plugin-runtime-builder; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Scope files and G3 execution evidence in this plan.
- Next step: PAOS-AUD-G4 completed; host/promotion gates separate.

#### Completion Report

- status: implemented
- what was done: RU/EN dates, strict freshness, bounded registry resolution and heuristic claim classes; URL/date not semantic proof.
- files touched / work locations: source_policy.py; test_source_policy.py; registry RU/EN; shared control-plane and owning plan
- technical value delivered: False date/source gaps removed while retaining review boundaries.
- product value delivered: Source report distinguishes missing date, staleness and unverified semantics.
- actual implementation date and time: 09-11-2026 13:47
- verification evidence: G3 execution evidence above: RED/GREEN, Full unittest: 1320 tests, 725.771 s, OK (skipped=1); final focused 78 tests OK; fixture 91/91; transcript 26/26; compatibility passed (local structure only).
- residual risks: Semantic source support requires manual review; generated state is not acceptance. Host/promotion outside scope.
- follow-up: PAOS-AUD-G4 completed; preserve revision pin and canonical B42/B45 ownership.

### Task `PAOS-AUD-F08`

- ID: `PAOS-AUD-F08`
- Task: **Task name:** Fix positive signal in absence of owner feedback
- Short description: **Task description:** Return insufficient_evidence when eligible owner label count is zero. Separate record validity, human label count and sentiment; public summary must retain semantics.
- Technical value: **Technical value (for the project):** Missing evidence no longer appears to justify promotion.
- Product value: **Product value (for the user):** System does not infer user satisfaction until valid feedback is provided.
- Scope: **Affected files:** `plugins/product-agent-os/scripts/product_agent_os/self_learning_feedback.py`; `tests/product_agent_os/test_self_learning_extensions.py`; `tests/product_agent_os/test_self_learning_state.py`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Empty ledger, missing ledger and wholly rejected records give insufficient_evidence and no positive promotion signal. 2) Eligible positive/negative/mixed labels retain correct denominator/counts and summary. 3) Candidate-only/manual-only safeguards unchanged; fixtures contain no actual personal data.
- Group: PAOS-AUD-G3
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for full local G3 implementation with checks.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 13:47
- Depends on: No new mandatory tasks in this plan.
- Blocks: PAOS-GAP-06
- Source: F08
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Missing evidence no longer appears to justify promotion. Missing host/product gates remain open.
- Verification gates: RED on evaluate_satisfaction([]) and public summary; focused self-learning regression. Shared gates — TEST.md and rules above.
- Risks / approval gates: medium; output enum change requires checking existing consumers. Rollback per shared rules.
- Complexity: low
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: learning-loop-engineer; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Scope files and G3 execution evidence in this plan.
- Next step: PAOS-AUD-G4 completed; host/promotion gates separate.

#### Completion Report

- status: implemented
- what was done: Zero owner labels yield insufficient_evidence; sentiment/coverage/row validity separated; malformed ledger safely rejected.
- files touched / work locations: self_learning_feedback.py; test_self_learning_state.py; test_self_learning_extensions.py; self-learning-loop RU/EN; shared control-plane and owning plan
- technical value delivered: No positive evidence signal for empty/rejected data.
- product value delivered: User sees absence of feedback without false promotion signal.
- actual implementation date and time: 09-11-2026 13:47
- verification evidence: G3 execution evidence above: RED/GREEN, Full unittest: 1320 tests, 725.771 s, OK (skipped=1); final focused 78 tests OK; fixture 91/91; transcript 26/26; compatibility passed (local structure only).
- residual risks: Semantic source support requires manual review; generated state is not acceptance. Host/promotion outside scope.
- follow-up: PAOS-AUD-G4 completed; preserve revision pin and canonical B42/B45 ownership.

### Task `PAOS-AUD-F16`

- ID: `PAOS-AUD-F16`
- Task: **Task name:** Define current status and historical receipt precedence
- Short description: **Task description:** Define source ownership and precedence of newer execution evidence in existing projections. Add compact current pointer with revision, without creating second registry. Distinguish task/run/verification/acceptance; show conflict/unknown on conflict.
- Technical value: **Technical value (for the project):** Reproducible current state computation from owning sources rather than choosing first Current record.
- Product value: **Product value (for the user):** Clear what is complete, awaiting verification and next task.
- Scope: **Affected files:** `plugins/product-agent-os/scripts/product_agent_os/status_snapshot.py`; `tests/product_agent_os/test_status_snapshot.py`; `PLAN.md`; `RUNLOG.md`; `TEST.md`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Historical planned plus newer execution receipt does not return completed task to planned. 2) Current result includes source/revision and distinguishes implemented, verified, accepted; ambiguous/conflicting evidence not concealed. 3) Historical B42/B45 receipts retained; T23–T29 and machine statuses not rewritten due to new projection.
- Group: PAOS-AUD-G3
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for full local G3 implementation with checks.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 13:47
- Depends on: No new mandatory tasks in this plan.
- Blocks: PAOS-AUD-F17
- Source: F16
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Reproducible current state computation from owning sources rather than choosing first Current record. Missing host/product gates remain open.
- Verification gates: test_status_snapshot with historical/current/conflict cases; validate_task_state_consistency.py; docs checks. Shared gates — TEST.md and rules above.
- Risks / approval gates: medium; control-plane files shared — edits sequential only. Rollback per shared rules.
- Complexity: medium
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: graph-cockpit-engineer; one control-plane writer; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Scope files and G3 execution evidence in this plan.
- Next step: PAOS-AUD-G4 completed; host/promotion gates separate.

#### Completion Report

- status: implemented
- what was done: Revision-pinned PLAN pointer, scoped ownership and dated-receipt precedence; task/run/verification/acceptance separated; dashboard caller connected.
- files touched / work locations: status_snapshot.py; render_status_dashboard.py; run_fixture_eval.py; test_status_snapshot.py; PLAN.md; current-state RU/EN; shared control-plane and owning plan
- technical value delivered: Current projection tied to source; conflict and drift not masked by history.
- product value delivered: Historical planned does not hide later scoped execution evidence.
- actual implementation date and time: 09-11-2026 13:47
- verification evidence: G3 execution evidence above: RED/GREEN, Full unittest: 1320 tests, 725.771 s, OK (skipped=1); final focused 78 tests OK; fixture 91/91; transcript 26/26; compatibility passed (local structure only).
- residual risks: Semantic source support requires manual review; generated state is not acceptance. Host/promotion outside scope.
- follow-up: PAOS-AUD-G4 completed; preserve revision pin and canonical B42/B45 ownership.

## PAOS-AUD-G4 — Simple ordinary route and compact instructions

- **ID:** `PAOS-AUD-G4`
- **Group name:** Simple ordinary route and compact instructions
- **Group description:** Simplify entry into the existing ordinary route, remove repetitive instructions and only measured unnecessary module work.
- **Technical value (for the project):** Minimal task context, caller compatibility, lower instruction and repeated-scan overhead.
- **Product value (for the user):** Fewer unnecessary questions, files and less waiting for ordinary tasks while retaining high-risk escalation.
- **Affected files:** `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`; `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/state.py`; `plugins/product-agent-os/skills/`; `tests/AGENTS.md`; `plugins/product-agent-os/scripts/product_agent_os/discovery.py`. Full task-specific scope is in the cards.
- **Group acceptance criteria:** Representative ordinary/edge/adversarial cases retain correctness and boundaries; context/scanning reduction is measured; no unsupported refactoring.
- **Dependencies and sequence:** F05 intake is independent; the modified authoring scenario follows required G1 gates. F10 precedes or accompanies F09; F15 starts with measurement. Final baseline before T32.
- **Proposed responsibility:** plugin-runtime-builder; instructions — lifecycle-orchestrator.

### Task `PAOS-AUD-F05`

- ID: `PAOS-AUD-F05`
- Task: Simplify entry into the existing ordinary route
- Short description: Add minimal explicit intake/task-context at the existing public entrypoint. Explain and diagnose legacy fallback; verify callers before any default change. Support RU/EN/no-builder without new onboarding for every task.
- Technical value: Use existing selectors through a minimal contract instead of the full template registry by default.
- Product value: An ordinary task starts with a small number of required actions and does not create hundreds of unnecessary file proposals.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`; `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/state.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`; `tests/product_agent_os/test_codex_runtime_runner_cli.py`; `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`; `tests/product_agent_os/test_infrastructure_renderer.py`. Shared docs/control-plane scope follows the rules above.
- Acceptance criteria: 1) A small ordinary case selects the agreed minimal artifact set; high-risk/unknown cases retain escalation. 2) RU/EN projects and the absence of a builder do not trigger hidden full onboarding. 3) Legacy callers have an explicit fallback receipt; the default changes only after compatibility regression and a separate task decision. 4) No automatic target apply or reimplementation of T25–T29.
- Group: PAOS-AUD-G4
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request on 09.11.2026 for full local G4 implementation with checks.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 14:58
- Depends on: ORD-01–ORD-06 completed. Intake can be implemented independently; the incremental report scenario uses completed F06/F18.
- Blocks: PAOS-AUD-F15, PAOS-AUD-F14, PAOS-GAP-06
- Source: F05; ORD-01–ORD-06 and T23–T29 already implemented.
- Non-goals: See shared boundaries; do not rework the completed baseline.
- Expected result: Use existing selectors through a minimal contract instead of the full template registry by default. Missing host/product gates remain open.
- Verification gates: Existing ORD positive/negative cases, CLI-to-selector-to-staging integration; compare artifact count and unnecessary questions against baseline. Shared gates are TEST.md and the rules above.
- Risks / approval gates: medium; authority and readiness are not inferred solely from task context. Rollback follows the shared rules.
- Complexity: medium
- Estimated execution time: not_estimated; after preflight of the specific slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation not started.
- Skills: According to the slice type and shared rules above; not used during authoring.
- Output artifacts: Scope files and G4 execution evidence in this plan.
- Next step: PAOS-AUD-G5 completed; host/behavioral gates remain separate in G6.

#### Completion Report

- status: implemented
- what was done: Inline intake and an explicit fallback receipt in two public CLIs; rich JSON and selectors preserved. Empty/partial/mixed/escaping input rejected; empty ordinary stage manifest fixed.
- files touched / work locations: task_routing.py; codex_runtime_runner/cli.py; infrastructure.py; render_infrastructure.py; test_codex_runtime_runner_cli.py; docs/control-plane and owning plan
- technical value delivered: The explicit ordinary path reuses existing selectors without legacy inference.
- product value delivered: A small docs task works without task.json and a builder; 0 instead of 209 file proposals.
- actual implementation date and time: 09-11-2026 14:58
- verification evidence: G4 execution evidence above. Full final: 1326 tests, 540.818 s, OK (skipped=1), exit 0; final focused 253 OK; template contracts 95 OK; fixtures 91/91; transcripts 26/26; compatibility exit 0, local structure only.
- residual risks: Source-level/local contracts verified; fresh host discovery and live behavioral evaluation not performed, owned by G6. No provider/cache/activation/Git actions.
- follow-up: PAOS-AUD-G5 completed; T34 and G6 host gates remain separately open.

### Task `PAOS-AUD-F09`

- ID: `PAOS-AUD-F09`
- Task: Reduce repetitive skill instructions
- Short description: Keep trigger, authority, inputs, outputs and stop in canonical SKILL.md; move shared repetitions and long conditional procedures into existing references. First capture the baseline of files actually read; do not change implicit invocation or installed cache.
- Technical value: Progressive disclosure without reloading identical policies or artificially increasing the context budget.
- Product value: Less delay and fewer unnecessary steps while preserving quality and predictable results.
- Scope: `plugins/product-agent-os/skills/`; `tests/product_agent_os/test_lifecycle_skills.py`; `tests/product_agent_os/test_validators.py`. Shared docs/control-plane scope follows the rules above.
- Acceptance criteria: 1) All 12 canonical skills retain their role boundaries and metadata; reference links are valid. 2) Reduction in actually loaded context is measured for selected tasks, including conditional reference reads. 3) Typical/edge/adversarial cases retain authority and required gates; local checks and live behavioral evaluation are marked separately. 4) No implicit enable, cache install or context-limit increase as a substitute for reduction.
- Group: PAOS-AUD-G4
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request on 09.11.2026 for full local G4 implementation with checks.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 14:58
- Depends on: PAOS-AUD-F10
- Blocks: PAOS-AUD-HOST-01
- Source: F09
- Non-goals: See shared boundaries; do not rework the completed baseline.
- Expected result: Progressive disclosure without reloading identical policies or artificially increasing the context budget. Missing host/product gates remain open.
- Verification gates: Skill metadata/links/contract tests, baseline/source digest comparison; behavioral comparison through a separate frozen treatment, without mixing with the B45 compact-contract intervention. Shared gates are TEST.md and the rules above.
- Risks / approval gates: medium; directory scope covers only 12 canonical skills and directly used references; the exact file manifest is fixed before edits. Rollback follows the shared rules.
- Complexity: high
- Estimated execution time: not_estimated; after preflight of the specific slice.
- Agents: lifecycle-orchestrator; ownership recommendation, delegation not started.
- Skills: According to the slice type and shared rules above; not used during authoring.
- Output artifacts: Scope files and G4 execution evidence in this plan.
- Next step: PAOS-AUD-G5 completed; host/behavioral gates remain separate in G6.

#### Completion Report

- status: implemented
- what was done: 93 conditional sections moved verbatim into the existing role-specific reference; entrypoints retain triggers/authority/I/O/stop. Metadata 12/12 unchanged; contract readers follow relocation.
- files touched / work locations: 12 canonical SKILL.md; references/complexity-routing.md; validators.py; run_fixture_eval.py; test_lifecycle_skills.py; test_infrastructure_templates.py; docs/control-plane and owning plan
- technical value delivered: Selected read sets reduced by 0.31–30.89%; baseline and conditional reads accounted for.
- product value delivered: Less irrelevant context while preserving domain gates and explicit gaps.
- actual implementation date and time: 09-11-2026 14:58
- verification evidence: G4 execution evidence above. Full final: 1326 tests, 540.818 s, OK (skipped=1), exit 0; final focused 253 OK; template contracts 95 OK; fixtures 91/91; transcripts 26/26; compatibility exit 0, local structure only.
- residual risks: Source-level/local contracts verified; fresh host discovery and live behavioral evaluation not performed, owned by G6. No provider/cache/activation/Git actions.
- follow-up: PAOS-AUD-G5 completed; T34 and G6 host gates remain separately open.

### Task `PAOS-AUD-F10`

- ID: `PAOS-AUD-F10`
- Task: Eliminate duplication and conflicting instruction authority
- Short description: Replace obsolete tests/AGENTS.md with concise English test-specific rules. Separate the default read-only role from an explicitly authorized task in canonical skills; align reuse of unchanged evidence. Do not remove deliberate role restrictions.
- Technical value: A single instruction hierarchy; factual source authority is not confused with instruction precedence.
- Product value: Fewer conflicting instructions and repeated requests for already granted permission.
- Scope: `tests/AGENTS.md`; `plugins/product-agent-os/skills/agent-team-designer/SKILL.md`; `plugins/product-agent-os/skills/completion-skeptic/SKILL.md`; `plugins/product-agent-os/skills/`. Shared docs/control-plane scope follows the rules above.
- Acceptance criteria: 1) tests/AGENTS.md is in English and contains only appropriate test-specific instructions and the correct hierarchy. 2) Shared rules do not conflict with current root policy; read-only assurance and approval boundaries are preserved. 3) Other canonical skills are checked for duplicate contradictions; only identified cases are edited. 4) Static correction is not claimed as runtime discovery proof; that claim requires a fresh-session receipt.
- Group: PAOS-AUD-G4
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request on 09.11.2026 for full local G4 implementation with checks.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 14:58
- Depends on: No new mandatory tasks in this plan.
- Blocks: PAOS-AUD-F09
- Source: F10
- Non-goals: See shared boundaries; do not rework the completed baseline.
- Expected result: A single instruction hierarchy; factual source authority is not confused with instruction precedence. Missing host/product gates remain open.
- Verification gates: Static instruction comparison, skill contract tests; snapshot baseline; source loading checked separately when needed. Shared gates are TEST.md and the rules above.
- Risks / approval gates: medium; global AGENTS.md and host settings are out of scope. Rollback follows the shared rules.
- Complexity: medium
- Estimated execution time: not_estimated; after preflight of the specific slice.
- Agents: lifecycle-orchestrator; ownership recommendation, delegation not started.
- Skills: According to the slice type and shared rules above; not used during authoring.
- Output artifacts: Scope files and G4 execution evidence in this plan.
- Next step: PAOS-AUD-G5 completed; host/behavioral gates remain separate in G6.

#### Completion Report

- status: implemented
- what was done: tests/AGENTS.md became a concise English test-specific file. Instruction hierarchy separated from factual evidence; task-authorized team writing distinguished from read-only assurance; unchanged evidence retains provenance.
- files touched / work locations: tests/AGENTS.md; 12 canonical SKILL.md; references/source-policy.md; references/handoff-contract.md; docs/control-plane and owning plan
- technical value delivered: tests/AGENTS.md: 8471→1483 bytes; removed duplicated global rules and the ban on assigned team artifacts.
- product value delivered: Fewer contradictory instructions; approval and assurance boundaries preserved.
- actual implementation date and time: 09-11-2026 14:58
- verification evidence: G4 execution evidence above. Full final: 1326 tests, 540.818 s, OK (skipped=1), exit 0; final focused 253 OK; template contracts 95 OK; fixtures 91/91; transcripts 26/26; compatibility exit 0, local structure only.
- residual risks: Source-level/local contracts verified; fresh host discovery and live behavioral evaluation not performed, owned by G6. No provider/cache/activation/Git actions.
- follow-up: PAOS-AUD-G5 completed; T34 and G6 host gates remain separately open.

### Task `PAOS-AUD-F15`

- ID: `PAOS-AUD-F15`
- Task: Eliminate measured repeated scans and module duplication
- Short description: Measure repeated inventory/scans and ordinary-route cost on a fixed synthetic workspace. Reuse an immutable inventory snapshot and extract detector/render contracts only where measurements and callers demonstrate benefit. File size alone is not grounds for edits.
- Technical value: Less repeated work and coupling without a new database, workflow engine or provider abstraction.
- Product value: Faster project analysis and fewer contradictory conclusions across views.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py`; `plugins/product-agent-os/scripts/product_agent_os/code_quality_metrics.py`; `tests/product_agent_os/test_methodology_audit.py`; `tests/product_agent_os/test_infrastructure_renderer.py`. Shared docs/control-plane scope follows the rules above.
- Acceptance criteria: 1) Before changes, record baseline scan counts/runtime/output on the same fixture and environment. 2) After changes, output contracts and safety boundaries are preserved; fewer repeated operations are measured. 3) If significant duplication is not confirmed, close the task as accepted_gap with rationale and no refactoring. 4) Extract a new module only after recording its specific boundary and dedicated test coverage; add no live semantic/provider claims.
- Group: PAOS-AUD-G4
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request on 09.11.2026 for full local G4 implementation with checks.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 14:58
- Depends on: PAOS-AUD-F05
- Blocks: No mandatory downstream implementation dependency in this document; its own acceptance gate remains.
- Source: F15
- Non-goals: See shared boundaries; do not rework the completed baseline.
- Expected result: Less repeated work and coupling without a new database, workflow engine or provider abstraction. Missing host/product gates remain open.
- Verification gates: Existing characterization tests, deterministic output comparison, bounded repeated timing/scan measurement; expand file scope only for identified callers. Shared gates are TEST.md and the rules above.
- Risks / approval gates: medium; conditional optimization, not mandatory rewriting of large modules. Rollback follows the shared rules.
- Complexity: medium
- Estimated execution time: not_estimated; after preflight of the specific slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation not started.
- Skills: According to the slice type and shared rules above; not used during authoring.
- Output artifacts: Scope files and G4 execution evidence in this plan.
- Next step: PAOS-AUD-G5 completed; host/behavioral gates remain separate in G6.

#### Completion Report

- status: implemented
- what was done: Within analyze_workspace scope the detector uses one immutable inventory snapshot. The public API is fresh on every call; distinct methodology/first-run inventories were not combined.
- files touched / work locations: discovery.py; test_methodology_audit.py; docs/control-plane and owning plan
- technical value delivered: Discovery inventory calls 2→1, identical output; median 114.448→103.959 ms on a fixed synthetic fixture.
- product value delivered: Less repeated work without a new cache/framework or loss of freshness.
- actual implementation date and time: 09-11-2026 14:58
- verification evidence: G4 execution evidence above. Full final: 1326 tests, 540.818 s, OK (skipped=1), exit 0; final focused 253 OK; template contracts 95 OK; fixtures 91/91; transcripts 26/26; compatibility exit 0, local structure only.
- residual risks: Source-level/local contracts verified; fresh host discovery and live behavioral evaluation not performed, owned by G6. No provider/cache/activation/Git actions.
- follow-up: PAOS-AUD-G5 completed; T34 and G6 host gates remain separately open.

## PAOS-AUD-G5 — Documentation, offline tooling and current site

- **ID:** `PAOS-AUD-G5`
- **Group name:** Documentation, offline tooling and current site
- **Group description:** Fix the offline installer, update the package README and synchronize RU/EN, registry and generated site after local edits.
- **Technical value (for the project):** Reproducible offline command contract and aligned source/build output.
- **Product value (for the user):** The user follows the current start route and receives equivalent instructions in Russian and English.
- **Affected files:** `tools/docs_install.ps1`; `plugins/product-agent-os/README.md`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`; `site/`. Full task-specific scope is in the cards.
- **Group acceptance criteria:** The offline path generates no network install commands; README/examples align; strict build, RU/EN links/anchors and Mermaid check pass; no publication.
- **Dependencies and sequence:** F13 can run earlier. Update documentation with each group; final F14/F17 follows G1–G4. After G6, update only new receipts and affected pages.
- **Proposed responsibility:** docs-maintainer; installer — plugin-runtime-builder.

### Task `PAOS-AUD-F13`

- ID: `PAOS-AUD-F13`
- Task: Ensure the documentation installer offline contract
- Short description: Remove the unconditional pip upgrade before the offline branch or route the entire install through the specified wheelhouse. Verify command construction with a stub, preserving project-local tooling.
- Technical value: Offline mode actually generates no network package-install commands.
- Product value: In a restricted network, installation does not stall on an unexpected package-index request.
- Scope: `tools/docs_install.ps1`; `tests/product_agent_os/test_product_agent_os_docs.py`. Shared docs/control-plane scope follows the rules above.
- Acceptance criteria: 1) The OfflineWheelhouse path excludes index/network for every pip call, including upgrade/bootstrap. 2) Online mode remains explicit; a missing required wheel yields a clear local error. 3) The command-contract test installs no dependencies and changes no global environment.
- Group: PAOS-AUD-G5
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request on 09.11.2026 for G5 implementation with local checks and a build.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 15:24
- Depends on: No new mandatory tasks in this plan.
- Blocks: PAOS-AUD-F17
- Source: F13
- Non-goals: See shared boundaries; do not rework the completed baseline.
- Expected result: Offline mode actually generates no network package-install commands. Missing host/product gates remain open.
- Verification gates: Stubbed installer command inspection + existing docs tests; actual installation is not required for the local command contract. Shared gates are TEST.md and the rules above.
- Risks / approval gates: low; dependency installation is outside this planning task and requires separate approval if needed. Rollback follows the shared rules.
- Complexity: low
- Estimated execution time: not_estimated; after preflight of the specific slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation not started.
- Skills: According to the slice type and shared rules above; not used during authoring.
- Output artifacts: Scope files and evidence in the owning plan; proposed paths do not yet exist.
- Next step: G6 T34 and host gates remain open; GAP-06 accepted.

#### Completion Report

- status: implemented
- what was done: Offline pip routing fixed; online upgrade isolated, directory/error guards and a command-stub regression.
- files touched / work locations: tools/docs_install.ps1; tests/product_agent_os/test_product_agent_os_docs.py; control-plane and owning plan.
- technical value delivered: A verifiable local contract without hidden network installation or activation claims.
- product value delivered: An up-to-date short start route and reproducible local documentation.
- actual implementation date and time: 09-11-2026 15:24
- verification evidence: G5 execution evidence above; 105 docs tests, strict build, site integrity and 93 Mermaid renders passed.
- residual risks: Actual install/host activation/publication not performed; generated site is not the source of truth.
- follow-up: PAOS-AUD-G6 through its own gates.


### Task `PAOS-AUD-F14`

- ID: `PAOS-AUD-F14`
- Task: Update the package README and start route
- Short description: Provide a short start path with explicit skill invocation and ordinary task context. Align the MCP example, supported surfaces and manifest variants; remove historical counts from the current summary while retaining links to owning evidence.
- Technical value: The package entrypoint matches the public CLI and current compatibility contracts.
- Product value: A new user starts with a working minimal path and understands installation limitations.
- Scope: `plugins/product-agent-os/README.md`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`. Shared docs/control-plane scope follows the rules above.
- Acceptance criteria: 1) Args/JSON examples match implementation and pass local syntax/CLI contract checks. 2) supported/unsupported/not_verified are visible; explicit-only skills are invoked explicitly; the ordinary route is not hidden behind full generation. 3) Historical receipts remain linked and are not presented as the current run; unknown distribution data is not invented.
- Group: PAOS-AUD-G5
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request on 09.11.2026 for G5 implementation with local checks and a build.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 15:24
- Depends on: PAOS-AUD-F01, PAOS-AUD-F02, PAOS-AUD-F04, PAOS-AUD-F05
- Blocks: PAOS-AUD-F17
- Source: F14
- Non-goals: See shared boundaries; do not rework the completed baseline.
- Expected result: The package entrypoint matches the public CLI and current compatibility contracts. Missing host/product gates remain open.
- Verification gates: Docs tests/check_docs, example syntax, local CLI help/dry-run verification; no MCP execution. Shared gates are TEST.md and the rules above.
- Risks / approval gates: low; do not claim activation based on source tests. Rollback follows the shared rules.
- Complexity: medium
- Estimated execution time: not_estimated; after preflight of the specific slice.
- Agents: docs-maintainer; ownership recommendation, delegation not started.
- Skills: According to the slice type and shared rules above; not used during authoring.
- Output artifacts: Scope files and evidence in the owning plan; proposed paths do not yet exist.
- Next step: G6 T34 and host gates remain open; GAP-06 accepted.

#### Completion Report

- status: implemented
- what was done: Concise explicit start, ordinary task intake, current MCP JSON and support matrix; archive receipts separated.
- files touched / work locations: plugins/product-agent-os/README.md; current-state RU/EN; registry RU/EN; control-plane and owning plan.
- technical value delivered: A verifiable local contract without hidden network installation or activation claims.
- product value delivered: An up-to-date short start route and reproducible local documentation.
- actual implementation date and time: 09-11-2026 15:24
- verification evidence: G5 execution evidence above; 105 docs tests, strict build, site integrity and 93 Mermaid renders passed.
- residual risks: Actual install/host activation/publication not performed; generated site is not the source of truth.
- follow-up: PAOS-AUD-G6 through its own gates.


### Task `PAOS-AUD-F17`

- ID: `PAOS-AUD-F17`
- Task: Synchronize RU/EN and rebuild the local site
- Short description: Align changed user guides and registry; check affected Mermaid diagrams. After local changes, rebuild the site with existing project-local tools and check routes, links, anchors and diagrams. Update only new claims after host receipts.
- Technical value: The generated site reproducibly matches verified source files.
- Product value: Equally current instructions and working navigation are available in Russian and English.
- Scope: `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`; `docs/codex/models-and-reasoning.md`; `docs/codex/models-and-reasoning.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`; `docs/diagrams/`; `mkdocs.yml`; `site/`. Shared docs/control-plane scope follows the rules above.
- Acceptance criteria: 1) Manual semantic parity of affected RU/EN pairs and Source status are current; 10 English-original plans are not reported as missing translations. 2) Docs checks and strict MkDocs build pass; internal routes/links/anchors are checked against generated output. 3) Affected Mermaid diagrams parse/render successfully with an authorized tool; missing runtime rendering explicitly leaves the corresponding gate open. 4) The site receipt is bound to the source revision; the site is not published; dependencies/automation/hooks are not activated automatically.
- Group: PAOS-AUD-G5
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request on 09.11.2026 for G5 implementation with local checks and a build.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 15:24
- Depends on: PAOS-AUD-F03, PAOS-AUD-F13, PAOS-AUD-F14, PAOS-AUD-F16 Final local build after all actually completed G1–G4 changes, including F09/F10/F15; host receipts updated through separate small synchronization.
- Blocks: No mandatory downstream implementation dependency in this document; its own acceptance gate remains.
- Source: F17
- Non-goals: See shared boundaries; do not rework the completed baseline.
- Expected result: The generated site reproducibly matches verified source files. Missing host/product gates remain open.
- Verification gates: The current 100-case docs suite, check_docs, strict MkDocs, generated link/anchor check and Mermaid rendering with exact authority; git diff --check. Shared gates are TEST.md and the rules above.
- Risks / approval gates: medium; edit mkdocs.yml/diagrams only when affected by new documentation; saving the plan does not authorize browser/server/install/publication. Rollback follows the shared rules.
- Complexity: medium
- Estimated execution time: not_estimated; after preflight of the specific slice.
- Agents: docs-maintainer; ownership recommendation, delegation not started.
- Skills: According to the slice type and shared rules above; not used during authoring.
- Output artifacts: Scope files and evidence in the owning plan; proposed paths do not yet exist.
- Next step: G6 T34 and host gates remain open; GAP-06 accepted.

#### Completion Report

- status: implemented
- what was done: RU/EN semantic review, strict site rebuild, links/anchors/search and 93 Mermaid renders.
- files touched / work locations: current-state RU/EN; registry RU/EN; site/; source hashes and render receipts; control-plane and owning plan.
- technical value delivered: A verifiable local contract without hidden network installation or activation claims.
- product value delivered: An up-to-date short start route and reproducible local documentation.
- actual implementation date and time: 09-11-2026 15:24
- verification evidence: G5 execution evidence above; 105 docs tests, strict build, site integrity and 93 Mermaid renders passed.
- residual risks: Actual install/host activation/publication not performed; generated site is not the source of truth.
- follow-up: PAOS-AUD-G6 through its own gates.


## PAOS-AUD-G6 — GPT-6, host activation and user usefulness verification

- **ID:** `PAOS-AUD-G6`
- **Group name:** GPT-6, host activation and user usefulness verification
- **Group description:** Continue existing T30–T34 and remaining GAP gates; separately demonstrate local readiness, host behavior, treatment quality and ordinary-flow usefulness.
- **Technical value (for the project):** Separate reproducible evidence for configuration, activation, quality and acceptance.
- **Product value (for the user):** Improvement evaluated by successful work and user costs, not GPT-6 ID presence or test count.
- **Affected files:** `docs/planning/batch45-code-quality-runtime-recovery-task-group.json`; `docs/planning/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`; `research/product-agent-os-session-lifecycle-fix-2026-11-09.md`; `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json`; `EVALS.md`; `RUNLOG.md`. Full task-specific scope in cards.
- **Group acceptance criteria:** T30–T34 close only under canonical gates; fresh-host receipts bound to versions/hashes; pilot has owner acceptance; missing evidence retains no-go/partial.
- **Dependencies and order:** Prepare T30/T31 parallel to local fixes on independent files; T32 after stable baseline, T33 after T32, T34 only after T33 and exact approval. Host gates after final G1/G2.
- **Suggested ownership:** Existing T30–T34 roles; host — tester; pilot — product-manager.

### Task `B45-CQRR-T30`

- ID: `B45-CQRR-T30`
- Task: **Task name:** Implement an independent blinded reviewer contract
- Short description: **Task description:** Implement independent reviewer contract for baseline/treatment patches without arm labels and primary self-scores. Reviewer allowed only after valid deterministic pair evidence; critical findings override averages.
- Technical value: **Technical value (for the project):** Independent quality review separated from generating-model self-assessment.
- Product value: **Product value (for the user):** Correctness, security and unnecessary complexity problems are not hidden by a good average score.
- Scope: **Affected files:** `plugins/product-agent-os/assets/templates/evals/code-quality-reviewer-rubric.json` (proposed new); `plugins/product-agent-os/scripts/codex_runtime_runner/reviewer_contract.py` (proposed new); `tests/product_agent_os/test_batch45_code_quality_reviewer.py` (proposed new); `docs/planning/batch45-code-quality-runtime-recovery-task-group.json`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Reviewer input contains no baseline/treatment labels or primary self-scores. 2) Verdict blocked until valid deterministic pair evidence. 3) Critical correctness/security/data-loss/regression findings override averages.
- Group: PAOS-AUD-G6
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for G6; local implementation authorized, exact live/host/owner gates remain separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 16:04
- Depends on: No new mandatory tasks in this plan. B45-CQRR-T29 locally completed.
- Blocks: B45-CQRR-T32, B45-CQRR-T33
- Source: Existing B45-CQRR-T30; canonical title/depends_on/acceptance retained from task-group JSON. Original owning plan/JSON retains authority; this card is not new machine status.
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Independent quality review separated from generating-model self-assessment. Missing host/product gates remain open.
- Verification gates: Blinding, invalid pair gate and critical override tests on synthetic pairs. Shared gates — TEST.md and rules above.
- Risks / approval gates: medium; live reviewer call requires separate exact approval, local implementation does not authorize it. Rollback per shared rules.
- Complexity: medium
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: architect; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Review exact approval packets; execute only the separately authorized runtime scope.

#### Completion Report

- status: implemented
- what was done: Blinded reviewer module/rubric and negative gates implemented.
- files touched / work locations: Named task artifacts; G6 evidence, owning plans and control-plane.
- technical value delivered: Frozen reproducible local contracts and explicit missing runtime evidence.
- product value delivered: Reviewable next action without invented activation, quality or acceptance.
- actual implementation date and time: 09-11-2026 16:04
- verification evidence: G6 execution evidence above; A07 readiness receipt and current-run logs.
- residual risks: T34 primary/reviewer calls and fresh-host activation not verified; GAP-06 pilots owner accepted 10.11.2026.
- follow-up: Exact owner approval; preserve no-go until each remaining gate passes.


### Task `B45-CQRR-T31`

- ID: `B45-CQRR-T31`
- Task: **Task name:** Build a representative multi-stack held-out corpus
- Short description: **Task description:** Prepare 12–16 sanitized/synthetic tasks from at least four stack families and five risk classes. Include small change, legacy bug, boundary, unnecessary-abstraction and performance cases, plus reuse/config/delete/no-new-code solutions. Freeze before viewing treatment outputs.
- Technical value: **Technical value (for the project):** Evaluation on representative held-out set instead of tuning to eight internal tasks.
- Product value: **Product value (for the user):** Evaluation closer to varied real projects and does not reward unnecessary code.
- Scope: **Affected files:** `tests/fixtures/product_agent_os/batch45/code-quality-corpus/` (proposed new); `docs/superpowers/specs/batch45-code-quality-heldout-corpus.json` (proposed new); `tests/product_agent_os/test_batch45_code_quality_corpus.py` (proposed new); `docs/planning/batch45-code-quality-runtime-recovery-task-group.json`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) At least four stack families and five risk classes; 12–16 tasks with verifiable expected result. 2) Corpus frozen with hashes before treatment inspection; subsequent tuning to outcome forbidden. 3) No secrets/private source/raw chats/customer data/absolute user paths. 4) Cases include correct refusal of new code, reuse, config and deletion.
- Group: PAOS-AUD-G6
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for G6; local implementation authorized, exact live/host/owner gates remain separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 16:04
- Depends on: No new mandatory tasks in this plan. B45-CQRR-T27 and T29 locally completed; independent of T30.
- Blocks: B45-CQRR-T32, B45-CQRR-T33
- Source: Existing B45-CQRR-T31. Original owning plan/JSON retains authority; this card is not new machine status.
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Evaluation on representative held-out set instead of tuning to eight internal tasks. Missing host/product gates remain open.
- Verification gates: Schema, privacy/secret scan, difficulty/risk matrix and hash freeze validation. Shared gates — TEST.md and rules above.
- Risks / approval gates: medium; do not use unauthorized target source to populate corpus. Rollback per shared rules.
- Complexity: high
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: tester; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Review exact approval packets; execute only the separately authorized runtime scope.

#### Completion Report

- status: implemented
- what was done: 12 synthetic tasks frozen; 4 stacks, 7 risk classes; all reference/seeded outcomes verified.
- files touched / work locations: Named task artifacts; G6 evidence, owning plans and control-plane.
- technical value delivered: Frozen reproducible local contracts and explicit missing runtime evidence.
- product value delivered: Reviewable next action without invented activation, quality or acceptance.
- actual implementation date and time: 09-11-2026 16:04
- verification evidence: G6 execution evidence above; A07 readiness receipt and current-run logs.
- residual risks: T34 primary/reviewer calls and fresh-host activation not verified; GAP-06 pilots owner accepted 10.11.2026.
- follow-up: Exact owner approval; preserve no-go until each remaining gate passes.


### Task `B45-CQRR-T32`

- ID: `B45-CQRR-T32`
- Task: **Task name:** Freeze an isolated treatment and executable prompt contract
- Short description: **Task description:** Freeze exact baseline/treatment prompt/context templates. Primary comparison changes only compact pre-edit contract; reviewer assistance and comment advisory remain separate later factors. Final G4 skill/route changes must match in both arms or be excluded from comparison.
- Technical value: **Technical value (for the project):** Result cause measurable: one factor rather than simultaneous model, effort, prompt and route changes.
- Product value: **Product value (for the user):** Improvement decision based on verifiable effect rather than impression of new model.
- Scope: **Affected files:** `plugins/product-agent-os/assets/templates/evals/code-quality-baseline-prompt.md` (proposed new); `plugins/product-agent-os/assets/templates/evals/code-quality-treatment-prompt.md` (proposed new); `docs/superpowers/specs/batch45-code-quality-eval-design.json` (proposed new); `tests/product_agent_os/test_batch45_code_quality_eval_design.py` (proposed new); `docs/planning/batch45-code-quality-runtime-recovery-task-group.json`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Baseline/treatment use same model, effort, runner, timeout, tools and corpus. 2) Exactly one planned intervention differs; exact templates/context digests reproducible without private raw data. 3) Full research/checklist not inserted into every generation prompt. 4) Model/effort changes or separate skill-shortening treatment require new isolated design, not attributed to this comparison.
- Group: PAOS-AUD-G6
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for G6; local implementation authorized, exact live/host/owner gates remain separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 16:04
- Depends on: B45-CQRR-T30, B45-CQRR-T31 B45-CQRR-T25 completed; freeze after stable baseline of affected G1–G4. Do not call external sequencing recommendation a change to canonical depends_on.
- Blocks: B45-CQRR-T33
- Source: Existing B45-CQRR-T32. Original owning plan/JSON retains authority; this card is not new machine status.
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Result cause measurable: one factor rather than simultaneous model, effort, prompt and route changes. Missing host/product gates remain open.
- Verification gates: Prompt/context diff, digest reproducibility and no-extra-variable contract tests. Shared gates — TEST.md and rules above.
- Risks / approval gates: medium; do not adjust prompts after viewing held-out treatment outputs. Rollback per shared rules.
- Complexity: medium
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: architect; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Review exact approval packets; execute only the separately authorized runtime scope.

#### Completion Report

- status: implemented
- what was done: Isolated prompts, deterministic compiler and versioned schema frozen; no generation calls.
- files touched / work locations: Named task artifacts; G6 evidence, owning plans and control-plane.
- technical value delivered: Frozen reproducible local contracts and explicit missing runtime evidence.
- product value delivered: Reviewable next action without invented activation, quality or acceptance.
- actual implementation date and time: 09-11-2026 16:04
- verification evidence: G6 execution evidence above; A07 readiness receipt and current-run logs.
- residual risks: T34 primary/reviewer calls and fresh-host activation not verified; GAP-06 pilots owner accepted 10.11.2026.
- follow-up: Exact owner approval; preserve no-go until each remaining gate passes.


### Task `B45-CQRR-T33`

- ID: `B45-CQRR-T33`
- Task: **Task name:** Run the local promotion-readiness preflight
- Short description: **Task description:** Verify local reproducibility of executable schema, normalization, deterministic metrics, reviewer gate, frozen corpus and isolated prompt contract. Preserve readiness evidence before preparing new live approval packet.
- Technical value: **Technical value (for the project):** Local contract defects found before provider/model/reviewer call costs.
- Product value: **Product value (for the user):** Fewer futile runs and clearer decision on readiness for experiment.
- Scope: **Affected files:** `docs/superpowers/specs/batch45-code-quality-local-readiness.json` (proposed new); `docs/planning/batch45-code-quality-runtime-recovery-task-group.json`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) All valid fixtures pass, all invalid produce expected failure class. 2) Seeded faults caught by intended test/metric. 3) Blinding/reviewer gate work on synthetic pairs; corpus/prompt hashes reproducible. 4) No provider/model/reviewer calls; any required failed/missing gate retains no-go.
- Group: PAOS-AUD-G6
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for G6; local implementation authorized, exact live/host/owner gates remain separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 16:04
- Depends on: B45-CQRR-T30, B45-CQRR-T31, B45-CQRR-T32 B45-CQRR-T24, T28, T29 completed.
- Blocks: B45-CQRR-T34
- Source: Existing B45-CQRR-T33. Original owning plan/JSON retains authority; this card is not new machine status.
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Local contract defects found before provider/model/reviewer call costs. Missing host/product gates remain open.
- Verification gates: Focused contract/strategy tests, seeded-fault replay, freeze checks, docs/source registry checks and diff hygiene. Shared gates — TEST.md and rules above.
- Risks / approval gates: medium; local readiness is not behavioral promotion or product acceptance. Rollback per shared rules.
- Complexity: medium
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: completion-skeptic; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Review exact approval packets; execute only the separately authorized runtime scope.

#### Completion Report

- status: implemented
- what was done: Local preflight passed; A07 readiness receipt saved.
- files touched / work locations: Named task artifacts; G6 evidence, owning plans and control-plane.
- technical value delivered: Frozen reproducible local contracts and explicit missing runtime evidence.
- product value delivered: Reviewable next action without invented activation, quality or acceptance.
- actual implementation date and time: 09-11-2026 16:04
- verification evidence: G6 execution evidence above; A07 readiness receipt and current-run logs.
- residual risks: T34 primary/reviewer calls and fresh-host activation not verified; GAP-06 pilots owner accepted 10.11.2026.
- follow-up: Exact owner approval; preserve no-go until each remaining gate passes.


### Task `B45-CQRR-T34`

- ID: `B45-CQRR-T34`
- Task: **Task name:** Prepare, execute and decide a new promotion eval only after exact approval
- Short description: **Task description:** After T33 prepare concrete reviewable approval packet; run frozen same-model comparison only after exact owner approval. Reviewer called after valid pairs. Promotion/no-go decision rests on deterministic evidence and independent findings.
- Technical value: **Technical value (for the project):** Quality/cost/latency evidence tied to checked state for selected GPT-6 configuration.
- Product value: **Product value (for the user):** Only improvement with acceptable correctness, cost and response time is promoted.
- Scope: **Affected files:** `docs/superpowers/specs/batch45-code-quality-eval-approval-packet.json` (proposed new); `docs/superpowers/specs/batch45-code-quality-eval-results.json` (proposed new); `docs/superpowers/specs/batch45-code-quality-promotion-decision.json` (proposed new); `docs/planning/batch45-code-quality-runtime-recovery-task-group.json`; `EVALS.md`; `RUNLOG.md`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Exact approval sets model, effort, call cap, timeout, cost, retention and reviewer policy before calls. 2) All counted pairs schema-valid with deterministic acceptance; reviewer completed without unresolved critical findings. 3) Latency/token/cost/performance outside frozen tolerance block promotion or have separately owner-accepted exception. 4) Incomplete/invalid/mixed evidence retains no-go; raw private outputs not stored. 5) Same-model result is not proof of superiority for entire GPT-6 family; model/effort changes compared separately.
- Group: PAOS-AUD-G6
- Status: blocked
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for G6; local implementation authorized, exact live/host/owner gates remain separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 16:04
- Depends on: B45-CQRR-T33
- Blocks: No mandatory downstream implementation dependency in this document; own acceptance gate retained.
- Source: Existing B45-CQRR-T34; behavioral part of F04. Original owning plan/JSON retains authority; this card is not new machine status.
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Quality/cost/latency evidence tied to checked state for selected GPT-6 configuration. Missing host/product gates remain open.
- Verification gates: Approval preflight, sanitized results validation, independent reviewer evidence, retention/no-unapproved-actions checks, control-plane sync. Shared gates — TEST.md and rules above.
- Risks / approval gates: high; approved_preflight_blocked; tools/context isolation unconfirmed; current maintenance scope does not launch live calls. Rollback per shared rules.
- Complexity: high
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: release-operator; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Resolve recorded runtime/host evidence gap within approved bounds; GAP-06 pilots already owner accepted.

#### Completion Report

- status: blocked
- what was done: Owner approved execution; runtime/cache/fresh-host preflight performed, exact observations in approved execution receipt.
- files touched / work locations: Named task artifacts; G6 evidence, owning plans and control-plane.
- technical value delivered: Frozen reproducible local contracts and explicit missing runtime evidence.
- product value delivered: Reviewable next action without invented activation, quality or acceptance.
- actual implementation date and time: 09-11-2026 16:04
- verification evidence: G6 approved execution receipt and approved-*.log; previous A07 remains local-only evidence.
- residual risks: T34/runtime and fresh-host gaps remain; GAP-06 pilots passed and owner accepted 10.11.2026.
- follow-up: Resolve observed technical blocker; do not request the already granted packet authority again.


### Task `PAOS-AUD-HOST-01`

- ID: `PAOS-AUD-HOST-01`
- Task: **Task name:** Close remaining GAP-03 M06: exposure and invocation on selected host
- Short description: **Task description:** On selected supported surface verify canonical/installed source provenance, skill exposure and explicit invocation. Record client/surface, hashes, observed model when receipt available. If cache update needed, first prepare concrete preview/rollback and obtain exact authority.
- Technical value: **Technical value (for the project):** Link source package to components actually loaded by host.
- Product value: **Product value (for the user):** User knows installed skills match fixed version and are invoked as expected.
- Scope: **Affected files:** `docs/planning/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `TEST.md`; `RUNLOG.md`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Selected host/surface supported; version/source/cache digests and invocation evidence bound to checked state. 2) Configured model distinct from observed; without model receipt field stays not_verified. 3) Explicit-only skill not declared implicit; source/cache mismatch has explicit decision, not concealed. 4) GAP-03 M06 closes only on own evidence; parent status updated in owning plan, not independent registry.
- Group: PAOS-AUD-G6
- Status: blocked
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for G6; local implementation authorized, exact live/host/owner gates remain separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 16:04
- Depends on: PAOS-AUD-F01, PAOS-AUD-F02, PAOS-AUD-F04, PAOS-AUD-F09
- Blocks: Fresh-session native exposure claim; does not block three approved current-project PAOS-GAP-06 pilots
- Source: GAP-03 M06; F02/F04/F09. ID addresses specific stage in this plan, not new replacement for parent GAP-03.
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Link source package to components actually loaded by host. Missing host/product gates remain open.
- Verification gates: Bounded fresh-host exposure/invocation receipt; exact commands/target chosen after host scope, not invented in general plan. Shared gates — TEST.md and rules above.
- Risks / approval gates: high; installation/cache/trust/provider actions have separate exact authority. Rollback per shared rules.
- Complexity: medium
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: tester; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Resolve recorded runtime/host evidence gap within approved bounds; GAP-06 pilots already owner accepted.

#### Completion Report

- status: blocked
- what was done: Owner approved execution; runtime/cache/fresh-host preflight performed, exact observations in approved execution receipt.
- files touched / work locations: Named task artifacts; G6 evidence, owning plans and control-plane.
- technical value delivered: Frozen reproducible local contracts and explicit missing runtime evidence.
- product value delivered: Reviewable next action without invented activation, quality or acceptance.
- actual implementation date and time: 09-11-2026 16:04
- verification evidence: G6 approved execution receipt and approved-*.log; previous A07 remains local-only evidence.
- residual risks: T34/runtime and fresh-host gaps remain; GAP-06 pilots passed and owner accepted 10.11.2026.
- follow-up: Resolve observed technical blocker; do not request the already granted packet authority again.


### Task `PAOS-AUD-HOST-02`

- ID: `PAOS-AUD-HOST-02`
- Task: **Task name:** Close remaining GAP-05 and fresh-host lifecycle gates
- Short description: **Task description:** After final source hashes verify actual hook loading, positive/negative scenarios, report-authoring and independence of new chats. Separately verify generated target route on exact authorized disposable target. Preserve distinction between current-host observation and fresh-host evidence.
- Technical value: **Technical value (for the project):** Confirm active fixed path and absence of masking legacy fallback.
- Product value: **Product value (for the user):** New chats do not interfere; authorized report saved, foreign/out-of-scope writes blocked.
- Scope: **Affected files:** `docs/planning/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`; `research/product-agent-os-session-lifecycle-fix-2026-11-09.md`; `TEST.md`; `RUNLOG.md`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Receipt has version, exact definition/source hashes, selected config path, trust observation and workspace scope. 2) Fresh positive and safe negative probe confirmed by output/absence evidence; filesystem failure not represented as hook denial. 3) Two new session-aware chats isolated; foreign marker and old shared marker do not authorize mutation. 4) Generated config actually loads; previously inactive mirror/legacy route does not mask result. 5) Report create/update succeeds only within agreed bounds; hash change after verification reopens affected gate.
- Group: PAOS-AUD-G6
- Status: blocked
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 for G6; local implementation authorized, exact live/host/owner gates remain separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 16:04
- Depends on: PAOS-AUD-F06, PAOS-AUD-F12, PAOS-AUD-F18. If F11 rules activated, effective-policy probe is separate bounded substage with its own authority.
- Blocks: No mandatory downstream implementation dependency in this document; own acceptance gate retained.
- Source: GAP-05; F06/F12/F18; PAOS-SESSION-LIFECYCLE-2026-11-09. ID is combined verification stage, not repeat implementation of parent tasks.
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Confirm active fixed path and absence of masking legacy fallback. Missing host/product gates remain open.
- Verification gates: Fresh-host bounded positive/negative receipts and source hashes; repeat synthetic tests only for changed contract. Shared gates — TEST.md and rules above.
- Risks / approval gates: high; actual target writes, hook trust/definitions and fresh-host execution require exact authorization; permission not inferred from plan status. Rollback per shared rules.
- Complexity: high
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: tester; security review read-only; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Resolve recorded runtime/host evidence gap within approved bounds; GAP-06 pilots already owner accepted.

#### Completion Report

- status: blocked
- what was done: Owner approved execution; runtime/cache/fresh-host preflight performed, exact observations in approved execution receipt.
- files touched / work locations: Named task artifacts; G6 evidence, owning plans and control-plane.
- technical value delivered: Frozen reproducible local contracts and explicit missing runtime evidence.
- product value delivered: Reviewable next action without invented activation, quality or acceptance.
- actual implementation date and time: 09-11-2026 16:04
- verification evidence: G6 approved execution receipt and approved-*.log; previous A07 remains local-only evidence.
- residual risks: T34/runtime and fresh-host gaps remain; GAP-06 pilots passed and owner accepted 10.11.2026.
- follow-up: Resolve observed technical blocker; do not request the already granted packet authority again.


### Task `PAOS-GAP-06`

- ID: `PAOS-GAP-06`
- Task: **Task name:** Check ordinary user outcomes through existing B39/B44 manual packets
- Short description: **Task description:** First agree 3–5 representative tasks and specific targets: bugfix, docs, legacy, no-new-code, boundary change. Start with one bounded ordinary pilot, then continue selected set. Measure time to useful result, extra questions/artifacts, repeated checks, correctness and owner intervention.
- Technical value: **Technical value (for the project):** Check end-to-end user journey after local contract gates.
- Product value: **Product value (for the user):** Confirm Product-Agent OS actually reduces user effort and produces useful results.
- Scope: **Affected files:** `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json`; `prod_test.md`; `RUNLOG.md`; `docs/planning/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`. Shared docs/control-plane scope per rules above.
- Acceptance criteria: **Acceptance criteria:** 1) Tasks/targets/allowed actions/rollback and baseline measurements agreed before run. 2) Per-task outcome, owner feedback/acceptance and failed cases retained; one pilot not declared completion of full representative set. 3) Improvements enter existing manual candidate loop; no automatic promotion/schedules/auto-apply. 4) prod_test.md changed only if evidence for its B39 family actually created; other history not rewritten.
- Group: PAOS-AUD-G6
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner authorized three pilots from current project to host-target; HOST-01 dependency removed, activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 17:11
- Depends on: ORD-06 and local F05/F08 completed; HOST-01/HOST-02 and T34 are not gates for these three synthetic local pilots.
- Blocks: No mandatory downstream implementation dependency in this document; own acceptance gate retained.
- Source: Existing PAOS-GAP-06 from ordinary implementation plan; canonical scope preserved. Original owning plan/JSON retains authority; this card is not new machine status.
- Non-goals: See shared boundaries; do not redo completed baseline.
- Expected result: Check end-to-end user journey after local contract gates. Missing host/product gates remain open.
- Verification gates: Actual baseline/final checks, source hashes and file inventories in pilot-results; mandatory docs/matrix/state gates; owner feedback separately.
- Risks / approval gates: Current local pilot scope expressly authorized; owner acceptance received 10.11.2026; fresh-session/provider/browser/Git excluded. Rollback by initial_source proposal; preserve receipts.
- Complexity: medium
- Estimated execution time: not_estimated; after specific slice preflight.
- Agents: product-manager; evidence — learning-loop-engineer; acceptance — user; ownership recommendation, delegation not launched.
- Skills: Per slice type and shared rules above; not applied during authoring.
- Output artifacts: Named local task artifacts and G6 evidence; owner receipt recorded; live/host receipts remain separate.
- Next step: Three results accepted by owner 10.11.2026; T34 and fresh-session activation remain separately open.

#### Completion Report

- status: implemented
- what was done: Three approved pilots performed in host-target/pilots from current session; HOST-01 dependency removed by owner decision.
- files touched / work locations: candidate.py, candidate.json, unchanged candidate.cjs and three receipt.json; pilot proposal/results; owning plans and control-plane.
- technical value delivered: Observed bug RED/GREEN; config JSON/invariant checks; no-new-code SHA-256 preservation.
- product value delivered: Three verified and owner-accepted outcomes without unnecessary questions during pilots.
- actual implementation date and time: 09-11-2026 17:11
- verification evidence: docs/superpowers/specs/paos-aud-g6-pilot-results.json; python -B .docs-tools/reports/paos-aud-g6/run_pilots.py baseline and verify, both exit 0; baseline includes expected bug/config assertion exit 1.
- residual risks: Owner accepted all three local pilots 10.11.2026. Synthetic cases do not prove mass usefulness; fresh-session activation and T34 remain separately open.
- follow-up: Acceptance received for all three outcomes; findings remain manual candidates without promotion.

## PAOS-AUD-G7 — Implementation quality, architectural simplicity and sufficient verification

- **ID:** `PAOS-AUD-G7`
- **Group name:** Implementation quality, architectural simplicity and sufficient verification
- **Group description:** Implement verifiable improvements to existing PAOS mechanisms based on analysis of Ponytail and analogues: complete minimal solution, responsibility boundaries, useful checks, evidence-based review and the cost of the next change.
- **Technical value (for the project):** Reduce implicit coupling, duplicated rules and false process gates; reuse existing selectors, inventory and test/eval infrastructure.
- **Product value (for the user):** Obtain a useful result with less unnecessary code, questions, documentation and repeated checks without reducing correctness or safety.
- **Affected files:** Exact scope in each card below; shared docs/control-plane synchronized by one writer. `AGENTS.md`, hook definitions/trust, installed cache, frozen T34 inputs and other workspaces are excluded unless later exact authority changes the boundary.
- **Group acceptance criteria:** T01–T06 have applicable current-run contract/regression evidence; T07 has a frozen separate design; T08 has actual results and an owner decision. Open behavioral evaluation leaves the group partially_verified. Static text checks do not prove generation quality or fresh-session loading.
- **Dependencies and order:** T01 → T02/T03/T05/T06 → T07 → T08. T04 is an independent early security-sensitive fix; its live activation has a separate HOST-02 gate. Edit shared T01/T02/T05 and T03/T07 files sequentially. Unfinished G6 acceptance/HOST/T34 do not create an artificial blanket prohibition on local G7.
- **Proposed ownership:** One implementer by default; named roles below describe ownership, not authorization to automatically start agents.
- **Execution status:** `implemented`, closure_level=implemented_locally_verified / owner_accepted; T01–T08 accepted, G7 closed within the checked local scope. The current request authorized local implementation, checks, comparison and three independent reviews. Owner acceptance and fresh-session activation are separate. [Current-run evidence](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md).

### G7 sources and claim boundaries

Clarification 09.11.2026: [separate in-depth research](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-repository-deep-review-2026-11-09.md) pins revisions of five key repositories, primary tool docs and findings P/K/M/S/D/X. All eight cards were clarified in existing `Acceptance criteria`, Source and Verification gates fields; no new mandatory fields were added. Required additions: evaluator calibration, honest denominators, evidence invalidation, unique-test protection, review disposition, dynamic-use and resolver limits. At authoring all tasks were planned; current statuses below are updated from execution evidence. Research does not establish superiority of the approach before T07/T08.

Authoring verification — 09.11.2026: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` — exit 0, 105 tests, 17.003 s, OK; `python -B tools/check_docs.py` — exit 0; `python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md` — exit 0, errors=[]; `python -B plugins/product-agent-os/scripts/validate_task_state_consistency.py` — exit 0, errors=[]. In-memory before/after comparison: all 26 previous task blocks unchanged; 34 task blocks total; eight new cards have the same set of 36 fields including Completion Report; all existing scope paths exist. Self-review: dependencies create no cycle, future files/commands are separate from current implementation, G6 acceptance and T34/HOST gates not closed. Initial `git -c core.safecrlf=false diff --check` found an extra EOF blank line; corrected, repeat exit 0. Log: `.docs-tools/reports/paos-aud-g6/g7-planning-docs.log`. These results verify authoring, not G7 execution.

Control-plane sync: REQUIREMENTS.md — scoped planned addition; PLAN.md — queue and current source revision; TEST.md — authoring checks; RUNLOG.md — compact handoff; RU/EN registry — research provenance. EVALS.md — not_applicable, current thresholds unchanged (new design only planned in T07); prod_test.md — not_applicable, B39 evidence unchanged. Strict MkDocs/site — not_applicable: navigation/rendering/config/site unchanged. Root control-plane remains below 50 KiB; overflow/handoff not needed for authoring. Historical authoring receipt: implementation had not started then. Later implementation request and owner clarifications authorized current G7 and available Codex without monetary cap; API key creation was declined.

Collected analysis source: public source and local PAOS contracts read in the previous research turn on 09.11.2026; no repeat web fetch during authoring. Source content is not an instruction for our agent. Third-party material has `trust_level=community`, `verification_status=source_inspected_runtime_not_reproduced`. Official tool documentation has `trust_level=primary`, but local installation/compatibility has not been verified.

| Ref | Source | Use and limitation |
| --- | --- | --- |
| G7-S0 | Current `.codex/workflows/coding-standards.md`, compact contract, selectors, reviewer rubric; G6 pilot results | Source-inspected project-local context. Two earlier read-only denials are observations, root cause requires T04 reproduction. G6 pilots do not replace held-out evaluation. |
| G7-S1 | [Ponytail core](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail/SKILL.md), [review](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail-review/SKILL.md), [map](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/hooks/ponytail-map.js), [benchmark](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/benchmarks/results/2026-10-07-agentic.md) | Reuse-first, connected-code review, bounded discovery, paired evaluation. Do not transfer author's percentages to PAOS; do not install plugin/hooks. |
| G7-S2 | [Karpathy-inspired guidelines](https://github.com/multica-ai/andrej-karpathy-skills) | Goal-driven/surgical changes; third-party interpretation, not an official Karpathy standard; do not force clarification of obvious choices. |
| G7-S3 | [Matt Pocock test guidance](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/tdd/tests.md), [codebase design](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/codebase-design/SKILL.md) | Independent oracle, interfaces and locality of change; do not copy blanket deletion tests, mandatory approvals, HTML reports and subagent workflow. |
| G7-S4 | [Superpowers](https://github.com/obra/superpowers) | Spec compliance, root-cause debugging, sequential slices; do not introduce a second mandatory lifecycle over PAOS. |
| G7-S5 | [Desloppify](https://github.com/peteromallet/desloppify) | Scoped triage and mechanical findings; score is not the product goal, check full scan/license/cost before use. |
| G7-S6 | [Ruff](https://docs.astral.sh/ruff/), [Import Linter](https://import-linter.readthedocs.io/en/stable/contract_types/forbidden/), [dependency-cruiser](https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md) | Stack-specific profile candidates; no automatic installation, universal defaults or custom linter clone. |
| G7-S8 | [Stryker mutation testing](https://stryker-mutator.io/docs/) | Test-sensitivity checks on bounded risky areas; not a mandatory full-project mutation run. |

### G7 execution scope clarification — 09.11.2026

The current owner request authorizes implementation, necessary checks, comparison and three independent analyses; fresh-session activation remains separate. Root is the sole writer. Source preflight:

- T02/T05/T06 additionally own `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`, `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py` and `tests/product_agent_os/test_codex_runtime_runner_cli.py`: these are the existing production caller and CLI integration checks, without which selector changes do not reach the user.
- T03/T07 do NOT change frozen `eval_design.py`, `reviewer_contract.py`, `code_quality_metrics.py`, `promotion_contract.py` and rubric v1. Instead exact new scope: `plugins/product-agent-os/scripts/codex_runtime_runner/g7_quality_eval.py`; rubric v2 and G7 test/manifest/design/results from original cards remain. This resolves the internal conflict between changing the module and preserving its SHA for T34.
- Local comparison checks real mechanisms before/after on identical inputs. It is separate from model A/B: CLI help does not prove absence of ambient context or generator access to hidden oracle. Model A/B runs only after specific design/context/budget authorization; independent analysts are not generators or blind reviewers.
- Additional exact local evidence runner: `plugins/product-agent-os/scripts/run_g7_quality_comparison.py`; it runs only checked baseline/current repository code, not generated candidate code, and does not call a provider.

### Shared G7 execution gates

- Each acceptance states condition/action/expected result; a separate acceptance file is unnecessary when the card fully defines scenario → check → evidence owner.
- T01/T02/T03/T05/T06 change agent behavior/contracts: retain before baseline, change one factor at a time, do not claim improvement from keyword tests. Behavioral comparison belongs to T07/T08.
- T04 requires reproducible RED → GREEN with negative safety cases. Check text standards statically; do not invent RED.
- For runtime changes run the card's focused command first; then mandatory full unittest, fixture/transcript eval and compatibility gates from current TEST.md. This plan does not cancel them. Record results in existing evidence paths, without one file per command.
- For docs/control-plane changes: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v`, `python -B tools/check_docs.py`, `git -c core.safecrlf=false diff --check`; expected exit 0. Strict MkDocs only for navigation/rendering/config/site scope, which current authoring does not change.
- New files are marked `proposed new`; before fixture authoring T07 fixes the exact manifest rather than unbounded directory write scope. Frozen T34 design/corpus/prompts/rubric/results are not rewritten; version routing preserves legacy tests.
- Tool installation, current-host trust, fresh-session activation, additional model/provider/reviewer run, browser/server/Git/CI/publication are separate boundaries. T08 command gap is deliberately linked to T07 output and approval packet, not presented as completed or unconditionally ready to run.
- Product hypothesis: reduce unnecessary code/process costs while preserving correctness/security. Evidence owner is tester; acceptance is owner. Analytics/telemetry, production release, DB migration, FSD and domain-model scaffolding are not_applicable to this group; architectural boundaries are named in owning modules of cards.
- Each task rollback is limited to its hunks and named artifacts; do not delete historical receipts, unrelated dirty work or G6 results. Do not create a new framework or second state registry for methodology.

### Task `PAOS-AUD-G7-T01`

- ID: `PAOS-AUD-G7-T01`
- Task: **Task name:** Clarify the minimum complete implementation and architectural-boundary standard
- Short description: **Task description:** Reconcile Ponytail and analogue guidance with current PAOS rules; replace duplication with concrete criteria for simplicity, responsibility, state and cost of the next change. Preserve the eight-field compact contract; load detailed rules by risk.
- Technical value: **Technical value (for the project):** One active/package contract without a competing always-on layer; clear boundaries between business rules and external effects.
- Product value: **Product value (for the user):** The task is solved completely without unnecessary abstractions, configuration and approvals for obvious actions.
- Scope: **Affected files:** `.codex/workflows/coding-standards.md`; `.codex/artifact-templates/code-change-contract.md`; `.codex/artifact-templates/coding-standard-checklist.md`; `plugins/product-agent-os/assets/templates/workflows/coding-standards.md`; `plugins/product-agent-os/assets/templates/artifact-templates/code-change-contract.md`; `plugins/product-agent-os/assets/templates/artifact-templates/coding-standard-checklist.md`; `tests/product_agent_os/test_batch45_coding_standards.py`; `tests/product_agent_os/test_coding_standards_artifacts.py`. Shared docs/control-plane scope follows shared G7 execution gates; update RU/EN registry and coding-standards only for affected claims.
- Acceptance criteria: **Acceptance criteria:** 1) Compact contract remains eight fields; existing_capability/smallest_safe_patch/invariants include reuse search, affected callers and state owner. 2) Standard permits a necessary abstraction with one implementation and small duplication instead of false generality; LOC/function size are not hard gates. 3) Trust-boundary validation, data-loss handling, security, accessibility and agreed scope are not reduced. 4) Debt is recorded with limitation and review trigger, without mandatory comments on every line. 5) Typical bug/config/no-new-code/shared-module cases receive proportionate depth; active/package parity preserved. 6) Interface contract includes applicable ordering/error/config/performance assumptions; pure/local/remote-owned/external dependencies are distinguished without a mandatory port for every call. 7) Complete minimal case passes acceptance, stub does not; created orphans are removed only in scope. 8) Bug route uses reproduction → hypothesis → bounded probe; repeated failures require revisiting the hypothesis, not automatic redesign.
- Group: PAOS-AUD-G7
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 to implement G7 with checks, comparison and three independent opinions; fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 19:39
- Depends on: Local PAOS-AUD-F05/F09/F10 and existing compact contract; G6 completion is not required.
- Blocks: PAOS-AUD-G7-T02, PAOS-AUD-G7-T03, PAOS-AUD-G7-T05, PAOS-AUD-G7-T06
- Source: G7-S1, G7-S2, G7-S3; existing enterprise_leverage_check/deep_module_check/legacy_seam_check; [deep review](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-repository-deep-review-2026-11-09.md), findings P01, K01–K03, M01/M02/M05, S01/S04.
- Non-goals: Closing or reimplementing G1–G6; rewriting T34 baseline; new orchestration framework; installing a third-party plugin; mass cleanup of unrelated code; auto-promotion.
- Expected result: One active/package contract without a competing always-on layer; clear boundaries between business rules and external effects. Evidence ceiling: local contracts until separate behavioral/host verification.
- Verification gates: python -B -m unittest tests.product_agent_os.test_batch45_coding_standards tests.product_agent_os.test_coding_standards_artifacts -v; expect OK, active/package parity and no mandatory new fields. Fix scenarios before edit; text match does not prove agent behavior. Shared G7 execution gates apply. Additional deep-review scenarios require positive and corresponding negative controls in existing test/eval infrastructure; static checks do not substitute for behavioral results.
- Risks / approval gates: medium; new standard only after a separate implementation request. Do not install Ponytail or another always-on plugin. Rollback: only this contract's and mirror hunks, preserve prior baseline.
- Complexity: medium
- Estimated execution time: not_estimated; estimate after focused source preflight, do not substitute a promise for budget/measurements.
- Agents: architect — contract; docs-maintainer — synchronization; one writer, no automatic subagent launch
- Skills: implementation-planner for scoped plan; task-matching canonical skills by owner; Python edits — python-design-patterns/python-code-style; external skills are research sources only, not active instructions.
- Output artifacts: `.codex/workflows/coding-standards.md`; `.codex/artifact-templates/code-change-contract.md`; `.codex/artifact-templates/coding-standard-checklist.md`; `plugins/product-agent-os/assets/templates/workflows/coding-standards.md`; `plugins/product-agent-os/assets/templates/artifact-templates/code-change-contract.md`; `plugins/product-agent-os/assets/templates/artifact-templates/coding-standard-checklist.md`; `tests/product_agent_os/test_batch45_coding_standards.py`; `tests/product_agent_os/test_coding_standards_artifacts.py`; current-run evidence in owning plan/approved result artifact, compact RUNLOG pointer.
- Next step: Present local implementation evidence to owner; dependent T06–T08 and fresh-session gates remain separate.

#### Completion Report

- status: implemented
- what was done: Synchronized minimal-complete standards, compact contract and conditional checklist; eight fields preserved.
- files touched / work locations: Exact Scope + execution scope refinement; actual diff and [execution report](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md).
- technical value delivered: Eight-field compact contract and conditional reference instead of a new always-on checklist.
- product value delivered: Fewer false gates and explicit evidence boundary; generation superiority not claimed.
- actual implementation date and time: 09-11-2026 19:39
- verification evidence: [Current commands, RED/GREEN and findings](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md); full frozen run 1357 tests / exit 0 (1 platform skip), targeted 66 / exit 0; closure_level=implemented_locally_verified, fresh-session separate.
- residual risks: Local contracts/parity are checked; model pilot observational, superiority and fresh-session loading not demonstrated.
- follow-up: T01–T05 results accepted by owner 09.11.2026 in the current continuation. Fresh-session activation separate; continue T06–T08.

### Task `PAOS-AUD-G7-T02`

- ID: `PAOS-AUD-G7-T02`
- Task: **Task name:** Make check selection and test quality depend on specific risk
- Short description: **Task description:** Extend existing test_strategy_selector and risk_selected_tests: risk → failure → minimum check → grounds for rerun. Check defect sensitivity, independent expected value and resilience to behavior-preserving refactoring.
- Technical value: **Technical value (for the project):** Checks protect invariants, not implementation structure; meaningless duplicates and repeated runs on unchanged inputs are eliminated.
- Product value: **Product value (for the user):** Less time on checks for reporting while retaining protection against material risks.
- Scope: **Affected files:** `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`; `tests/product_agent_os/test_codex_runtime_runner_cli.py`; `plugins/product-agent-os/scripts/product_agent_os/test_strategy_selector.py`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`; `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`; `plugins/product-agent-os/assets/templates/artifact-templates/code-change-contract.md`; `.codex/artifact-templates/code-change-contract.md`; `TEST.md`. Shared docs/control-plane scope follows shared G7 execution gates; update RU/EN registry and coding-standards only for affected claims.
- Acceptance criteria: **Acceptance criteria:** 1) Bug has observable RED for the right reason and GREEN; config has parse/invariant checks without artificial RED; refactor reuses characterization/behavior tests. 2) Test plan names risk, independent oracle, level and reason for rerun; changed input/failure/flakiness/unresolved risk justify rerun. 3) No-new-code and mechanical edits do not create artificial new tests. 4) Selector does not cancel project-mandated gates; unknown impact is a gap. 5) Risky rules have bounded mutation/defect-injection checks; equivalent/invalid mutants are analyzed separately, no universal coverage or test-count quota. 6) Existing public contract/backward compatibility preserved. 7) Before deleting an old test compare unique protection; exactly-once, forbidden-call and security-ordering assertions remain when contractual. 8) A stand-in does not replace a separate adapter-compatibility risk check. 9) Async tests wait for observable conditions with bounded timeout; timing semantics uses controlled clock or a justified interval. 10) Evidence reuse is bound to source/config/tool/dependency fingerprints and relevant environment; invalidation reason and reused provenance are explicit.
- Group: PAOS-AUD-G7
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 to implement G7 with checks, comparison and three independent opinions; fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 19:39
- Depends on: PAOS-AUD-G7-T01
- Blocks: PAOS-AUD-G7-T07
- Source: G7-S1 review; G7-S3 TDD; G7-S8 mutation testing; current test_strategy_selector; [deep review](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-repository-deep-review-2026-11-09.md), findings M02–M04, S02, X04.
- Non-goals: Closing or reimplementing G1–G6; rewriting T34 baseline; new orchestration framework; installing a third-party plugin; mass cleanup of unrelated code; auto-promotion.
- Expected result: Checks protect invariants, not implementation structure; meaningless duplicates and repeated runs on unchanged inputs are eliminated. Evidence ceiling: local contracts until separate behavioral/host verification.
- Verification gates: python -B -m unittest tests.product_agent_os.test_batch45_code_quality_behavior -v; expect OK for bug/config/refactor/no-new-code, mandatory-gate preservation and rerun reasons. Use existing fixtures; new cases cover distinct failure modes, not mirror code. Shared G7 execution gates apply. Additional deep-review scenarios require positive and corresponding negative controls in existing test/eval infrastructure; static checks do not substitute for behavioral results.
- Risks / approval gates: medium; do not silently weaken TEST.md, remove unique test protection or declare unverified code sufficient by score. Rollback: selector/skill/contract hunks and related fixtures; preserve previous run results.
- Complexity: medium
- Estimated execution time: not_estimated; estimate after focused source preflight, do not substitute a promise for budget/measurements.
- Agents: tester — test strategy and evidence; plugin-runtime-builder — selector, sequentially
- Skills: implementation-planner for scoped plan; task-matching canonical skills by owner; Python edits — python-design-patterns/python-code-style; external skills are research sources only, not active instructions.
- Output artifacts: `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`; `plugins/product-agent-os/scripts/product_agent_os/test_strategy_selector.py`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`; `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`; `plugins/product-agent-os/assets/templates/artifact-templates/code-change-contract.md`; `.codex/artifact-templates/code-change-contract.md`; `TEST.md`; current-run evidence in owning plan/approved result artifact, compact RUNLOG pointer.
- Next step: Present local implementation evidence to owner; dependent T06–T08 and fresh-session gates remain separate.

#### Completion Report

- status: implemented
- what was done: Refactor/config test-first routing fixed; evidence reuse depends on source/config/dependency/environment inputs.
- files touched / work locations: Exact Scope + execution scope refinement; actual diff and [execution report](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md).
- technical value delivered: False RED for refactor eliminated; feature/defect remain test-first, reused evidence invalidates on relevant drift.
- product value delivered: Fewer false gates and explicit evidence boundary; generation superiority not claimed.
- actual implementation date and time: 09-11-2026 19:39
- verification evidence: [Current commands, RED/GREEN and findings](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md); full frozen run 1357 tests / exit 0 (1 platform skip), targeted 66 / exit 0; closure_level=implemented_locally_verified, fresh-session separate.
- residual risks: External tool/environment provenance is caller-reported or unknown; mandatory project checks are not cancelled.
- follow-up: T01–T05 results accepted by owner 09.11.2026 in the current continuation. Fresh-session activation separate; continue T06–T08.

### Task `PAOS-AUD-G7-T03`

- ID: `PAOS-AUD-G7-T03`
- Task: **Task name:** Strengthen review evidence and distinguish defects from subjective recommendations
- Short description: **Task description:** Clarify current reviewer: spec compliance before quality/risk; read related callers and data flow; concrete scenario, source, consequence and confidence for findings. Prioritize correctness/security/data loss over lean/style.
- Technical value: **Technical value (for the project):** Fewer false blockers and stylistic rework; review finds changed public behavior and real coupling.
- Product value: **Product value (for the user):** Findings explain what breaks and why to fix it; unnecessary refactoring is not proposed.
- Scope: **Affected files:** `plugins/product-agent-os/scripts/codex_runtime_runner/g7_quality_eval.py`; `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`; `.codex/workflows/review-slice.md`; `plugins/product-agent-os/assets/templates/workflows/review-slice.md`; `.codex/agents/reviewer.toml`; `plugins/product-agent-os/assets/templates/agents/reviewer.toml`; `tests/product_agent_os/test_batch45_code_quality_reviewer.py`; `tests/product_agent_os/test_lifecycle_skills.py`; `plugins/product-agent-os/assets/templates/evals/code-quality-reviewer-rubric-v2.json` (G7 local artifact). Shared docs/control-plane scope follows shared G7 execution gates; update RU/EN registry and coding-standards only for affected claims.
- Acceptance criteria: **Acceptance criteria:** 1) Finding contains source, reachable scenario or explicitly labeled hypothesis, consequence, action and confidence; vague style concern is not a blocker. 2) Contract change checks callers; scope/load assumptions explicit. 3) Fewer LOC do not offset correctness/security/data-loss regression. 4) A clean case does not require an invented finding; design limitation is not a defect without crossing an agreed boundary. 5) Old reviewer rubric and frozen T34 hashes unchanged; v2 versioned and backward-compatible. 6) Role profiles pass existing validation; their presence is not presented as independent runtime review. 7) Finding is bound to checked revision; confirmed/fixed, rejected/false_positive, deferred and unresolved are distinct. Suppression is not a fix; rejection has evidence, deferred has owner/revisit trigger in an existing artifact. 8) Dead-code finding checks exports/config/dynamic references or marks incompleteness; grep miss does not prove unused. 9) Rerun requires changed state/new risk/fix verification or reviewer doubt; unrelated backlog is not a blanket gate.
- Group: PAOS-AUD-G7
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 to implement G7 with checks, comparison and three independent opinions; fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 19:39
- Depends on: PAOS-AUD-G7-T01
- Blocks: PAOS-AUD-G7-T07
- Source: G7-S1 review, G7-S4 Superpowers; current two-stage review and blinded rubric; [deep review](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-repository-deep-review-2026-11-09.md), findings P01/P02, M01, S03/S04, D01/D02.
- Non-goals: Closing or reimplementing G1–G6; rewriting T34 baseline; new orchestration framework; installing a third-party plugin; mass cleanup of unrelated code; auto-promotion.
- Expected result: Fewer false blockers and stylistic rework; review finds changed public behavior and real coupling. Evidence ceiling: local contracts until separate behavioral/host verification.
- Verification gates: python -B -m unittest tests.product_agent_os.test_batch45_code_quality_reviewer tests.product_agent_os.test_lifecycle_skills -v; expect OK for valid finding, unsupported blocker, empty findings and legacy rubric. Determine exact profile validator via TEST.md before profile edits; a missing command is a gate before execution. Shared G7 execution gates apply. Additional deep-review scenarios require positive and corresponding negative controls in existing test/eval infrastructure; static checks do not substitute for behavioral results.
- Risks / approval gates: medium; do not weaken critical override, grant reviewer write authority or change model simultaneously with prompt. Rollback: v2 route and changed hunks; v1 frozen artifacts remain baseline.
- Complexity: medium
- Estimated execution time: not_estimated; estimate after focused source preflight, do not substitute a promise for budget/measurements.
- Agents: reviewer — read-only criteria and self-review; plugin-runtime-builder — contract; one assigned writer
- Skills: implementation-planner for scoped plan; task-matching canonical skills by owner; Python edits — python-design-patterns/python-code-style; external skills are research sources only, not active instructions.
- Output artifacts: `plugins/product-agent-os/scripts/codex_runtime_runner/g7_quality_eval.py`; `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`; `.codex/workflows/review-slice.md`; `plugins/product-agent-os/assets/templates/workflows/review-slice.md`; `.codex/agents/reviewer.toml`; `plugins/product-agent-os/assets/templates/agents/reviewer.toml`; `tests/product_agent_os/test_batch45_code_quality_reviewer.py`; `tests/product_agent_os/test_lifecycle_skills.py`; `plugins/product-agent-os/assets/templates/evals/code-quality-reviewer-rubric-v2.json` (G7 local artifact); current-run evidence in owning plan/approved result artifact, compact RUNLOG pointer.
- Next step: Present local implementation evidence to owner; dependent T06–T08 and fresh-session gates remain separate.

#### Completion Report

- status: implemented
- what was done: Evidence-based review, dispositions and rubric v2 implemented separately from frozen T34; deferred requires owner/trigger.
- files touched / work locations: Exact Scope + execution scope refinement; actual diff and [execution report](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md).
- technical value delivered: Checked revision, concrete scenario, dispositions and deferred owner/trigger are checked without self-score veto.
- product value delivered: Fewer false gates and explicit evidence boundary; generation superiority not claimed.
- actual implementation date and time: 09-11-2026 19:39
- verification evidence: [Current commands, RED/GREEN and findings](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md); full frozen run 1357 tests / exit 0 (1 platform skip), targeted 66 / exit 0; closure_level=implemented_locally_verified, fresh-session separate.
- residual risks: Validating finding structure does not prove evidence truth; independent semantic review and owner acceptance remain necessary.
- follow-up: T01–T05 results accepted by owner 09.11.2026 in the current continuation. Fresh-session activation separate; continue T06–T08.

### Task `PAOS-AUD-G7-T04`

- ID: `PAOS-AUD-G7-T04`
- Task: **Task name:** Eliminate false blocking of read-only commands without weakening write protection
- Short description: **Task description:** Reproduce observed blocking of rg and Get-Content | Select-String with terminal marker. Establish cause from parser/hook input; fix general classification of provably read-only commands while preserving separate path, secret and mutation guards.
- Technical value: **Technical value (for the project):** Read-only inspection does not need false mutation authority; compound/unknown/write payload cannot masquerade as reading.
- Product value: **Product value (for the user):** Analysis and diagnosis continue without pointless lifecycle resets or permission requests.
- Scope: **Affected files:** `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `tests/product_agent_os/test_lifecycle_hooks.py`; `tests/product_agent_os/test_task_plan_lifecycle.py`; `research/product-agent-os-session-lifecycle-fix-2026-11-09.md`. Shared docs/control-plane scope follows shared G7 execution gates; update RU/EN registry and coding-standards only for affected claims.
- Acceptance criteria: **Acceptance criteria:** 1) Reproduce the same false-positive class before fixing; marker/environment schema error is not called parser bug. 2) Safe rg with quoted patterns and Get-Content with read-only Select-String pass in terminal/read-only context if path/secret policy permits. 3) Redirection, writes, command substitution, compound mutation, aliases/unknown executables and nested tool wrappers have separate negative cases; blanket allowlist/prefix bypass forbidden. 4) Own/foreign marker, exact bootstrap and scope protections remain. 5) Active/package parity and adversarial regression suite pass; actual fresh-session activation remains HOST-02 and is not inferred from unit tests. 6) Evidence binds exact sanitized command, parser classification and policy decision. Minimal reproducer and mutation near-miss prove the cause fixed without blanket shell exception; successful reading after marker activation alone does not prove parser fix.
- Group: PAOS-AUD-G7
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 to implement G7 with checks, comparison and three independent opinions; fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 19:39
- Depends on: Existing PAOS-AUD-F06/F18; independent of G7-T01 and unfinished G6 acceptance.
- Blocks: Safe verification of G7-T08 read-only path; does not block other local project tasks.
- Source: G7-S0: two read-only denial observations in previous research; root cause not yet established; F06/F18 regression contracts; [deep review](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-repository-deep-review-2026-11-09.md), findings S01.
- Non-goals: Closing or reimplementing G1–G6; rewriting T34 baseline; new orchestration framework; installing a third-party plugin; mass cleanup of unrelated code; auto-promotion.
- Expected result: Read-only inspection does not need false mutation authority; compound/unknown/write payload cannot masquerade as reading. Evidence ceiling: local contracts until separate behavioral/host verification.
- Verification gates: python -B -m unittest tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_task_plan_lifecycle -v; expect RED specifically on permitted read, then GREEN while retaining negative denials. Check active/package bytes and parser outputs; actual host probe separately under exact authority. Shared G7 execution gates apply. Additional deep-review scenarios require positive and corresponding negative controls in existing test/eval infrastructure; static checks do not substitute for behavioral results.
- Risks / approval gates: high; do not weaken sandbox/approvals/path/secret controls or expand trust. Rollback: only both guard copies and tests; do not change hook definitions/cache/trust. Bind fresh-session receipt to new hashes in HOST-02.
- Complexity: high
- Estimated execution time: not_estimated; estimate after focused source preflight, do not substitute a promise for budget/measurements.
- Agents: plugin-runtime-builder — guard; tester — reproduction; security-privacy-supply-chain-reviewer — read-only review under separate assignment
- Skills: implementation-planner for scoped plan; task-matching canonical skills by owner; Python edits — python-design-patterns/python-code-style; external skills are research sources only, not active instructions.
- Output artifacts: `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `tests/product_agent_os/test_lifecycle_hooks.py`; `tests/product_agent_os/test_task_plan_lifecycle.py`; `research/product-agent-os-session-lifecycle-fix-2026-11-09.md`; current-run evidence in owning plan/approved result artifact, compact RUNLOG pointer.
- Next step: Present local implementation evidence to owner; dependent T06–T08 and fresh-session gates remain separate.

#### Completion Report

- status: implemented
- what was done: Narrow literal classifier fixed with RED/GREEN and negative wire cases; active/package parity preserved.
- files touched / work locations: Exact Scope + execution scope refinement; actual diff and [execution report](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md).
- technical value delivered: Useful literal reads pass; known unsafe wire cases do not receive read-only exemption.
- product value delivered: Fewer false gates and explicit evidence boundary; generation superiority not claimed.
- actual implementation date and time: 09-11-2026 19:39
- verification evidence: [Current commands, RED/GREEN and findings](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md); full frozen run 1357 tests / exit 0 (1 platform skip), targeted 66 / exit 0; closure_level=implemented_locally_verified, fresh-session separate.
- residual risks: Classifier is limited to literal subset; arbitrary shells/aliases/ambient configuration not covered; HOST activation separate.
- follow-up: T01–T05 results accepted by owner 09.11.2026 in the current continuation. Fresh-session activation separate; continue T06–T08.

### Task `PAOS-AUD-G7-T05`

- ID: `PAOS-AUD-G7-T05`
- Task: **Task name:** Reuse discovery for concise search of existing capabilities
- Short description: **Task description:** Give coding route a bounded capability summary from existing inventory/discovery: suitable helper, config, platform feature or dependency plus source path. Do not create a second project map or treat regex/graph as proof of absence.
- Technical value: **Technical value (for the project):** One inventory source with explicit completeness and provenance; fewer repeated scans and less code duplication.
- Product value: **Product value (for the user):** Agent finds existing solutions faster and correctly chooses no-new-code or configuration route.
- Scope: **Affected files:** `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`; `tests/product_agent_os/test_codex_runtime_runner_cli.py`; `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/code_quality_selector.py`; `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`; `tests/product_agent_os/test_discovery.py`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`; `plugins/product-agent-os/assets/templates/artifact-templates/code-change-contract.md`; `.codex/artifact-templates/code-change-contract.md`. Shared docs/control-plane scope follows shared G7 execution gates; update RU/EN registry and coding-standards only for affected claims.
- Acceptance criteria: **Acceptance criteria:** 1) Existing helper/config/dependency cases return verifiable path and selection reason. 2) Bounded summary uses collected inventory; budget/omitted/stale/unknown are represented, no mandatory full rescan. 3) Absence from summary does not mean absence in project; read owning source before change. 4) Out-of-scope files, secrets and raw private data do not enter context. 5) Existing helper with incompatible contract is not selected merely for reuse; a new dependency follows existing approval policy. 6) Summary distinguishes static/dynamic/config references and unknown; exclusions/truncation/resolution limitations are available to reviewer. Lack of evidence does not trigger automatic deletion. 7) Source/resolver/config change invalidates the relevant summary; unchanged inventory is reused with original provenance.
- Group: PAOS-AUD-G7
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 to implement G7 with checks, comparison and three independent opinions; fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 19:39
- Depends on: PAOS-AUD-G7-T01; reuse PAOS-AUD-F15
- Blocks: PAOS-AUD-G7-T07
- Source: G7-S1 ponytail-map; existing discovery/F15 and code_quality_selector; [deep review](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-repository-deep-review-2026-11-09.md), findings P02, K02, X03.
- Non-goals: Closing or reimplementing G1–G6; rewriting T34 baseline; new orchestration framework; installing a third-party plugin; mass cleanup of unrelated code; auto-promotion.
- Expected result: One inventory source with explicit completeness and provenance; fewer repeated scans and less code duplication. Evidence ceiling: local contracts until separate behavioral/host verification.
- Verification gates: python -B -m unittest tests.product_agent_os.test_discovery tests.product_agent_os.test_batch45_code_quality_behavior -v; expect OK for reuse/config/no-change, incomplete/stale map, unsuitable helper and reuse of one inventory. Performance claim only after measured before/after on identical input. Shared G7 execution gates apply. Additional deep-review scenarios require positive and corresponding negative controls in existing test/eval infrastructure; static checks do not substitute for behavioral results.
- Risks / approval gates: medium; no new indexer/automatic scanner/hidden storage of sources outside scope is needed. Rollback: remove only added summary route, preserve prior discovery API and canonical graph.
- Complexity: medium
- Estimated execution time: not_estimated; estimate after focused source preflight, do not substitute a promise for budget/measurements.
- Agents: graph-cockpit-engineer — inventory projection; plugin-runtime-builder — caller integration, sequentially
- Skills: implementation-planner for scoped plan; task-matching canonical skills by owner; Python edits — python-design-patterns/python-code-style; external skills are research sources only, not active instructions.
- Output artifacts: `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`; `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/code_quality_selector.py`; `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`; `tests/product_agent_os/test_discovery.py`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`; `plugins/product-agent-os/assets/templates/artifact-templates/code-change-contract.md`; `.codex/artifact-templates/code-change-contract.md`; current-run evidence in owning plan/approved result artifact, compact RUNLOG pointer.
- Next step: Present local implementation evidence to owner; dependent T06–T08 and fresh-session gates remain separate.

#### Completion Report

- status: implemented
- what was done: Scope-bounded privacy-aware capability summary connected to production CLI; unknown/omitted explicit.
- files touched / work locations: Exact Scope + execution scope refinement; actual diff and [execution report](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md).
- technical value delivered: Existing production CLI receives bounded scoped candidates without rereading manifests.
- product value delivered: Fewer false gates and explicit evidence boundary; generation superiority not claimed.
- actual implementation date and time: 09-11-2026 19:39
- verification evidence: [Current commands, RED/GREEN and findings](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md); full frozen run 1357 tests / exit 0 (1 platform skip), targeted 66 / exit 0; closure_level=implemented_locally_verified, fresh-session separate.
- residual risks: Summary bounded by scope and limit; dynamic/config references remain unknown until read, omitted does not mean capability absent.
- follow-up: T01–T05 results accepted by owner 09.11.2026 in the current continuation. Fresh-session activation separate; continue T06–T08.

### Task `PAOS-AUD-G7-T06`

- ID: `PAOS-AUD-G7-T06`
- Task: **Task name:** Select objective code and architecture checks by stack and project boundaries
- Short description: **Task description:** Extend existing code-quality profile with selection of confirmed project-local tools and dependency rules. Ruff, Import Linter, dependency-cruiser and mutation tools are candidates; use existing tools first. Separate new violations from historical backlog.
- Technical value: **Technical value (for the project):** Verifiable import boundaries, cycles and common defects without a universal score gate or a new custom linter.
- Product value: **Product value (for the user):** Changes do not worsen architecture, and a small task does not turn into mass cleanup of an old project.
- Scope: **Affected files:** `tests/fixtures/product_agent_os/g7-architecture/`; `plugins/product-agent-os/scripts/run_g7_architecture_checks.py`; `docs/superpowers/specs/paos-aud-g7-architecture-results.json`; approved local `.docs-tools/g7-architecture-tools/` install/locks; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`; `tests/product_agent_os/test_codex_runtime_runner_cli.py`; `plugins/product-agent-os/scripts/product_agent_os/code_quality_selector.py`; `plugins/product-agent-os/assets/templates/artifact-templates/code-quality-profile.md`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`; `docs/product-agent-os/coding-standards.md`; `docs/product-agent-os/coding-standards.en.md`. Shared docs/control-plane scope follows shared G7 execution gates; update RU/EN registry and coding-standards only for affected claims.
- Acceptance criteria: **Acceptance criteria:** 1) Selection distinguishes declared, installed, runnable and verified; unconfirmed tool is not treated as available. 2) Python and JS/TS have profile scenarios with existing tool, missing tool and ambiguous configuration; other stacks do not receive unrelated commands. 3) Import cycle/forbidden dependency are concrete reproducible findings; line count/score advisory only. 4) New/changed violation is separated from legacy baseline; full scan is allowed if tool lacks diff-only, but cost and scope are explicit. 5) No silent install, config overwrite, CI activation or auto-fix; exact target config staging separately agreed after discovery. 6) Profile records version/config, scan scope/exclusions, resolver/aliases and type-only policy; missing/reduced coverage does not become verified clean. 7) Architectural rule has allowed and forbidden/transitive fixtures; configuration does not silently exclude the checked path. 8) Baseline does not automatically expand to hide new violations; suppression/deferred has reason/owner/trigger. 9) Report-only does not run auto-fix; unsafe fixes/tool upgrades require scoped diff/checks. 10) Before Desloppify integration separately check license/distribution fit and cost; sources are not automatically copied.
- Group: PAOS-AUD-G7
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 to implement G7 with checks, comparison and three independent opinions; fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 20:23
- Depends on: PAOS-AUD-G7-T01; existing code_quality_selector
- Blocks: PAOS-AUD-G7-T07
- Source: G7-S5 Desloppify (scoped triage only); G7-S6 Ruff/Import Linter/dependency-cruiser; G7-S8 Stryker; [deep review](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-repository-deep-review-2026-11-09.md), findings D01/D03/D04, X01–X04.
- Non-goals: Closing or reimplementing G1–G6; rewriting T34 baseline; new orchestration framework; installing a third-party plugin; mass cleanup of unrelated code; auto-promotion.
- Expected result: Verifiable import boundaries, cycles and common defects without a universal score gate or a new custom linter. Evidence ceiling: local contracts until separate behavioral/host verification.
- Verification gates: python -B -m unittest tests.product_agent_os.test_batch45_code_quality_behavior -v; expect OK on stack/tool/baseline fixtures. For actual tool smoke: first read-only version and command inventory; record exact command/target/rollback before running, leave missing tool as explicit gap, do not install automatically. Shared G7 execution gates apply. Additional deep-review scenarios require positive and corresponding negative controls in existing test/eval infrastructure; static checks do not substitute for behavioral results.
- Risks / approval gates: medium; dependency/license/tool-version review before selected installation. Do not call structural warnings proven runtime bugs. Rollback: selector/profile/docs hunks and only explicitly approved target config, if added.
- Complexity: medium
- Estimated execution time: not_estimated; estimate after focused source preflight, do not substitute a promise for budget/measurements.
- Agents: architect — boundary rules; tester — fixtures; plugin-runtime-builder — selector
- Skills: implementation-planner for scoped plan; task-matching canonical skills by owner; Python edits — python-design-patterns/python-code-style; external skills are research sources only, not active instructions.
- Output artifacts: `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/product_agent_os/code_quality_selector.py`; `plugins/product-agent-os/assets/templates/artifact-templates/code-quality-profile.md`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`; `docs/product-agent-os/coding-standards.md`; `docs/product-agent-os/coding-standards.en.md`; current-run evidence in owning plan/approved result artifact, compact RUNLOG pointer.
- Next step: T06 accepted 10.11.2026 within synthetic Python/JS scope; no further mandatory G7 actions.

#### Completion Report

- status: implemented
- what was done: Approved tools installed locally; actual 10/10 architecture controls, bounded receipt projection and immutable baseline implemented. Full gate: 1372 tests OK, one platform skip; owner accepted 10.11.2026.
- files touched / work locations: Exact Scope + execution scope refinement; actual diff and [execution report](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md).
- technical value delivered: Stack candidates expanded conservatively; declaration is not presented as installed/runnable/verified.
- product value delivered: Fewer false gates and explicit evidence boundary; generation superiority not claimed.
- actual implementation date and time: 09-11-2026 20:23
- verification evidence: [Current commands, RED/GREEN and findings](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md); current full frozen run 1372 tests / 783.819 s / exit 0 (1 platform skip), focused 37 / exit 0; actual tools 10/10. T06 closure: implemented_locally_verified; owner accepted 10.11.2026.
- residual risks: Actual evidence limited to Python/JavaScript .mjs; TypeScript resolver/type-only not checked. Normal discovery is declaration-only, trusted receipt API explicit; owner accepted 10.11.2026.
- follow-up: Results accepted by owner; TypeScript runtime and ordinary-route automatic receipts are not claimed.

### Task `PAOS-AUD-G7-T07`

- ID: `PAOS-AUD-G7-T07`
- Task: **Task name:** Prepare a separate comparative evaluation of sequential code changes
- Short description: **Task description:** Version a new G7 design over existing eval mechanisms, preserving T34 baseline. Prepare chains feature → new requirement → failure → format change → regression fix with hidden checks, bounded mutations and next-change cost evaluation.
- Technical value: **Technical value (for the project):** Check maintainability and check effectiveness over multiple steps, not only quality of one patch.
- Product value: **Product value (for the user):** Choose the standard based on correctness, work cost and usefulness instead of line/test count.
- Scope: **Affected files:** `plugins/product-agent-os/scripts/run_g7_attested_comparison.py`; `docs/superpowers/specs/paos-aud-g7-attested-design.json`; `docs/superpowers/specs/paos-aud-g7-attested-results.json`; `tests/fixtures/product_agent_os/g7-pressure/sequence_oracle.py`; ignored `.docs-tools/reports/g7-t07-2026-11-10/`; `docs/superpowers/specs/paos-aud-g7-isolation-preflight-results.json`; `tests/fixtures/product_agent_os/g7-pressure/`; `plugins/product-agent-os/scripts/g7_codex_trace_receipt.py`; `tests/product_agent_os/test_g7_codex_trace_receipt.py`; exact synthetic corpus `initial.py`, `reference.py`, `stub.py`, `unsafe.py`, `oracle.py` in `tests/fixtures/product_agent_os/g7-code-quality-evolution/`; `plugins/product-agent-os/scripts/codex_runtime_runner/g7_quality_eval.py`; `tests/product_agent_os/test_batch45_code_quality_eval_design.py`; `tests/product_agent_os/test_batch45_code_quality_reviewer.py`; `tests/product_agent_os/test_batch45_code_quality_metrics.py`; `docs/superpowers/specs/paos-aud-g7-code-quality-eval-design.json` (G7 local artifact); `tests/fixtures/product_agent_os/g7-code-quality-evolution/manifest.json` (G7 local artifact); `tests/product_agent_os/test_g7_code_quality_evolution.py` (G7 local artifact). Shared docs/control-plane scope follows shared G7 execution gates; update RU/EN registry and coding-standards only for affected claims.
- Acceptance criteria: **Acceptance criteria:** 1) Before generation manifest pins exact fixture file list/hashes, scope, chain steps, independent oracle and hidden checks; synthetic fixtures only. 2) Include no-change/config case and tasks with callers/state/partial failure, protected boundary and justified abstraction. 3) Current PAOS baseline and one treatment compared with identical model/effort/tool/context conditions; component effect requires separate pair, not aggregate score. 4) Thresholds, repetitions, stop budget, failure/timeout denominator, reviewer blinding and contamination policy frozen before run. Critical security/data-loss regressions = 0; correctness non-regression mandatory, cost/LOC cannot offset failure. 5) Measure correctness, completeness, change spread, repeated checks, intervention, latency/cost when provenance is available; unavailable stays null. 6) All T34 hashes preserved; old design compatibility tests pass. 7) Before model runs evaluator passes good/bad self-tests: full/stub, correct/unsafe, justified/overbuilt, unknown/structural-only; skipped is not executable pass. Eligible/attempted/executed/skipped/failed denominators explicit; missing required evidence blocks conclusions. 8) Receipt of actually available arm context, code-generation-only separate from end-to-end; hidden oracle not disclosed to generator. 9) Time/sunk-cost/incorrect-review pressure cases evaluate outcome/safety, not number of skill calls. 10) Offline rescore does not call provider; cache reuse invalidates on relevant config/dependency/environment drift; instrument version retained.
- Group: PAOS-AUD-G7
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 to implement G7 with checks, comparison and three independent opinions; fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 15:00
- Depends on: PAOS-AUD-G7-T02, PAOS-AUD-G7-T03, PAOS-AUD-G7-T05, PAOS-AUD-G7-T06; HOST-01 and T34 completion not needed for offline design.
- Blocks: PAOS-AUD-G7-T08
- Source: G7-S1 benchmark limitations; G7-S3; existing T30–T34 eval contracts and G6 pilot claim ceiling; [deep review](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-repository-deep-review-2026-11-09.md), findings P03–P05, M03, D03, S05, X04.
- Non-goals: Closing or reimplementing G1–G6; rewriting T34 baseline; new orchestration framework; installing a third-party plugin; mass cleanup of unrelated code; auto-promotion.
- Expected result: Check maintainability and check effectiveness over multiple steps, not only quality of one patch. Evidence ceiling: local contracts until separate behavioral/host verification.
- Verification gates: python -B -m unittest tests.product_agent_os.test_g7_code_quality_evolution tests.product_agent_os.test_batch45_code_quality_eval_design tests.product_agent_os.test_batch45_code_quality_reviewer tests.product_agent_os.test_batch45_code_quality_metrics -v; expect OK, no-provider self-test and unchanged frozen T34 hashes. New test module proposed new: command runnable after implementation. Shared G7 execution gates apply. Additional deep-review scenarios require positive and corresponding negative controls in existing test/eval infrastructure; static checks do not substitute for behavioral results.
- Risks / approval gates: high for future quality conclusion; execution with available Codex authorized by owner; do not create API key. Do not reuse already exposed G6 pilots as held-out. Rollback: only G7 design/fixtures and version routing, preserve baseline/results.
- Complexity: high
- Estimated execution time: not_estimated; estimate after focused source preflight, do not substitute a promise for budget/measurements.
- Agents: tester — design/oracles; learning-loop-engineer — metrics; separate reviewer only with authorized run
- Skills: implementation-planner for scoped plan; task-matching canonical skills by owner; Python edits — python-design-patterns/python-code-style; external skills are research sources only, not active instructions.
- Output artifacts: `plugins/product-agent-os/scripts/codex_runtime_runner/g7_quality_eval.py`; `tests/product_agent_os/test_batch45_code_quality_eval_design.py`; `tests/product_agent_os/test_batch45_code_quality_reviewer.py`; `tests/product_agent_os/test_batch45_code_quality_metrics.py`; `docs/superpowers/specs/paos-aud-g7-code-quality-eval-design.json` (G7 local artifact); `tests/fixtures/product_agent_os/g7-code-quality-evolution/manifest.json` (G7 local artifact); `tests/product_agent_os/test_g7_code_quality_evolution.py` (G7 local artifact); current-run evidence in owning plan/approved result artifact, compact RUNLOG pointer.
- Next step: T07/T08 accepted; fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Frozen design v2, actual tools=[]/same common context, 12 sequential generations, independent oracle baseline 6/6 = G7 6/6. All 10 diagnostics and 2 ineligible attempts preserved; offline replay hash-protected and does not overwrite evidence.
- files touched / work locations: Exact Scope + execution scope refinement; actual diff and [execution report](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md).
- technical value delivered: New versioned instrument and synthetic controls isolated from frozen T34; invalid outcomes do not count as pass.
- product value delivered: Fewer false gates and explicit evidence boundary; generation superiority not claimed.
- actual implementation date and time: 10-11-2026 15:00
- verification evidence: [Current commands, RED/GREEN and findings](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md); full 1379 tests / 516.855 s / exit 0 (1 platform skip), docs 105, fixture 91/91, transcript 26/26, compatibility passed. [Results](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/superpowers/specs/paos-aud-g7-attested-results.json). Closure: implemented_locally_verified / owner_accepted; explicit user acceptance 10.11.2026.
- residual risks: Generation-only, no filesystem/E2E/activation claim; 1 repetition, rehearsed Python corpus, uneven prompt caching, component/superiority insufficient_evidence. T34 preserved.
- follow-up: T08 owner accepted, G7 closed; do not extend conclusions to other stacks or production.

### Task `PAOS-AUD-G7-T08`

- ID: `PAOS-AUD-G7-T08`
- Task: **Task name:** Run a bounded comparison and decide on updated standards
- Short description: **Task description:** After offline gates run G7 comparison in the agreed local target/current-project route and present results to owner. For additional model/provider/reviewer calls fix exact command, destination, context, cost cap and rollback first. Close only the evidence-supported result level.
- Technical value: **Technical value (for the project):** State-hash-bound evidence and reproducible keep/revise/no-go decision without automatic promotion.
- Product value: **Product value (for the user):** Owner receives concrete evidence of the standard's benefit and cost; need not trust checklist or others' benchmark percentages.
- Scope: **Affected files:** `docs/superpowers/specs/paos-aud-g7-attested-results.json` (acceptance metadata only); `plugins/product-agent-os/scripts/run_g7_quality_comparison.py`; `plugins/product-agent-os/scripts/run_g7_codex_pilot.py`; `research/product-agent-os-g7-execution-report-2026-11-09.md`; ignored `.docs-tools/reports/g7-codex-pilot/` candidates/receipts; `EVALS.md`; `TEST.md`; `RUNLOG.md`; `PLAN.md`; `docs/product-agent-os/coding-standards.md`; `docs/product-agent-os/coding-standards.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`; `docs/superpowers/specs/paos-aud-g7-code-quality-eval-results.json`; `docs/superpowers/specs/paos-aud-g7-codex-pilot-results.json`; `docs/superpowers/specs/paos-aud-g7-codex-pilot-verification.py` (G7 local artifacts). Shared docs/control-plane scope follows shared G7 execution gates; update RU/EN registry and coding-standards only for affected claims.
- Acceptance criteria: **Acceptance criteria:** 1) Before calls, frozen T07 design and exact execution authority with budget/stop conditions exist; absent isolation/tool-restriction evidence leaves the corresponding arm blocked. 2) Preserve all completed and failed/timeout cases; synthetic smoke separate from agent outcomes, reviewer scores separate from executable correctness. 3) No new critical/security/data-loss regressions; other thresholds only from frozen design, not selected after result. 4) Owner accepts results; keep/revise/no-go and remaining gaps explicitly recorded. 5) Fresh-session activation remains separate HOST task; local pilots do not depend on HOST-01 but do not prove activation. 6) Final active/package/docs references aligned; no automatic installation, publication or promotion. 7) Report discloses instrument/context provenance, denominators and reused evidence; structural smoke/skipped/missing not represented as successful behavioral outcome. 8) Show next-change cost, unnecessary questions/artifacts/reruns, available cost/latency and all unsuccessful runs. 9) Per component decide keep/revise/no-go or insufficient_evidence; aggregate score/source popularity is not adoption basis, conclusion bounded to tested corpus.
- Group: PAOS-AUD-G7
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 09.11.2026 to implement G7 with checks, comparison and three independent opinions; fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 15:27
- Depends on: PAOS-AUD-G7-T07; PAOS-AUD-G7-T04 only for checking fixed read-only host path. Does not require full G6 closure; T34 no-go is not renamed pass.
- Blocks: G7 acceptance and decision on further use of updated standards; does not automatically close HOST-01/HOST-02/T34.
- Source: G7-S0 user goals; T07 frozen design; G6 separate activation policy; [deep review](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-repository-deep-review-2026-11-09.md), findings K03/M05, D02/D04, P05/S05.
- Non-goals: Closing or reimplementing G1–G6; rewriting T34 baseline; new orchestration framework; installing a third-party plugin; mass cleanup of unrelated code; auto-promotion.
- Expected result: State-hash-bound evidence and reproducible keep/revise/no-go decision without automatic promotion. Evidence ceiling: local contracts until separate behavioral/host verification.
- Verification gates: Repeat G7-T07 offline self-test only when inputs change; T07 attested design/results pin exact runner/arm/model/context/budget; repeated model run without changed inputs is unnecessary. Before closure run docs unittest, check_docs, task-matrix/state validators and diff --check; expect exit 0 and separate owner acceptance. Shared G7 execution gates apply. Additional deep-review scenarios require positive and corresponding negative controls in existing test/eval infrastructure; static checks do not substitute for behavioral results.
- Risks / approval gates: high; exact live/provider/reviewer approval is not inferred from request to save plan or prior T34 budget. Rollback: restore only G7 treatment route from retained hashes; do not delete results or negative cases. No-go is an acceptable experiment result, not proof of all G7 implemented.
- Complexity: high
- Estimated execution time: not_estimated; estimate after focused source preflight, do not substitute a promise for budget/measurements.
- Agents: tester — execution; reviewer — separate authorized review; owner — acceptance; release-operator — draft decision only
- Skills: implementation-planner for scoped plan; task-matching canonical skills by owner; Python edits — python-design-patterns/python-code-style; external skills are research sources only, not active instructions.
- Output artifacts: `plugins/product-agent-os/scripts/run_g7_quality_comparison.py`; `plugins/product-agent-os/scripts/run_g7_codex_pilot.py`; `docs/superpowers/specs/paos-aud-g7-codex-pilot-results.json`; `docs/superpowers/specs/paos-aud-g7-codex-pilot-verification.py`; `research/product-agent-os-g7-execution-report-2026-11-09.md`; `EVALS.md`; `TEST.md`; `RUNLOG.md`; `PLAN.md`; `docs/product-agent-os/coding-standards.md`; `docs/product-agent-os/coding-standards.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`; `docs/superpowers/specs/paos-aud-g7-code-quality-eval-results.json` (G7 local artifact); current-run evidence in owning plan/approved result artifact, compact RUNLOG pointer.
- Next step: No mandatory tasks within G7; fresh-session activation remains a separate open HOST task.

#### Completion Report

- status: implemented
- what was done: Final packet checked; owner accepted T06 and T08 decision 10.11.2026. T01–T08 accepted; keep tested local mechanisms, superiority insufficient_evidence; G7 closed.
- files touched / work locations: Exact Scope + execution scope refinement; actual diff and [execution report](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md).
- technical value delivered: Actual comparisons, negative attempts and reviewer opinions retained; owner receives a verifiable packet.
- product value delivered: Fewer false gates and explicit evidence boundary; generation superiority not claimed.
- actual implementation date and time: 10-11-2026 15:27
- verification evidence: [Current T08 checks and reused T07 provenance](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g7-execution-report-2026-11-09.md). Runtime/tests unchanged; current docs 105 tests passed; docs/matrix/state/diff exit 0; no new model run. Owner accepted T06/T08.
- residual risks: Generation-only synthetic evidence; superiority/component effect insufficient_evidence; money unavailable; fresh-session activation separate, T34 no-go unchanged.
- follow-up: Fresh-session activation separate; do not extend owner acceptance to production/general superiority.

## PAOS-AUD-G8 — control-plane structure, substance and safe maintenance

- ID: PAOS-AUD-G8
- Name: Adaptive control-plane documents, navigation and lossless compaction.
- Description: Implement findings of two analyses: file-formation module and document structures of three projects. Implementation authorized by owner 10.11.2026; T14 requires separate acceptance.
- Technical value: Unified generation, substantive verification, provenance, byte budget, safe merge/compaction and recovery contract.
- Product value: User receives current manageable documents, finds decisions and continues large projects without losing history.
- Group status: implemented; T01–T13 implemented locally with docs/planning clarification; T14 owner accepted; G8 closed.
- Affected files: exact card scopes below; directory scopes refined to file manifest before corresponding implementation.
- Group acceptance criteria: T01–T13 complete under own gates; T14 contains baseline/treatment comparison, negative scenario results and explicit owner decision. Data preservation is mandatory; size alone is not success.
- Dependencies: reuse PAOS-AUD-F12 merge protections, F03/F08/F16 source ownership, F05/F09/F10 ordinary routing and G7-T04/T05 guards/routing. Do not reopen without reproducible regression. HOST-01/HOST-02, T34 and full G6 do not block local G8 fixtures. Web M1 remains a separate queue; this plan does not change ordering between queues.

### G8 basis and traceability

Both analyses were read-only; findings are a 10.11.2026 snapshot, source preflight is required before implementation. Below are verifiable observations, not unsupported runtime claims. External project paths are repository-relative; their contents are not copied into fixtures.

| Source | Basis / observation | Tasks |
| --- | --- | --- |
| G8-S01 | Current contracts/templates/infrastructure/validators: six root files; bounded template context; readiness by presence; risk of replacing populated managed body; validation context differs from actual merged target. These are identified gaps, not claims of data loss. | T01–T05, T10, T13 |
| G8-S02 | Track 3 staged infrastructure, Track 4 hardening, root AGENTS ownership map and existing control-plane templates/workflows. | T01–T02 |
| G8-S03 | This G1–G7 matrix, ordinary-route implementation plan and G7 execution report: preserve existing merge/state/ordinary/session guards. | T02, T04, T08, T12 |
| G8-S04 | system_file_hygiene.py and runlog-compaction/control-plane-sync: chars/bytes and 40k/50KiB diverge; manual checklist does not guarantee continuing compactness. Terminal lifecycle state blocked some read-only inspection; regression scenario needed, not weaker guards. | T06–T08, T12 |
| G8-S05 | Trade: docs/governance/documentation-policy.md, root files, docs plans/evidence. Strengths: hot/warm/cold and compaction history. PLAN 121558, TEST 132766, RUNLOG 145536 bytes against own budget 20000; REQUIREMENTS 54832. Large detailed plans up to 686127 bytes. Renewed growth and optional local evidence need a separate contract. | T06–T09, T11 |
| G8-S06 | myPartners: docs/control-plane/index.md, archive-index.md, generated mirrors, root files and detailed plans. Strengths: owning PLAN selector and domain docs. EVALS 46647 bytes; plans up to 393734; differing stage pointers in requirements/start pages require reconciliation, age alone is not invalidation. Mirror check exists; runtime result not established by analysis. | T06–T11 |
| G8-S07 | myai-partners.app: README.md, root files, docs and src. README describes no frontend despite App Router source; runtime readiness does not follow. Repeated correction blocks, flat docs navigation, plan up to 312826 bytes and ambiguous cross-repo filenames. | T09–T11 |
| G8-S08 | [Last control-plane maintenance](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-control-plane-maintenance-2026-11-10.md), current Web plan and docs checks: preserve parallel work; known G6/G7 links outside docs_dir need targeted handling, not rewriting evidence. | T11, T14 |

### G8 size and preservation contract

This contract covers implemented local mechanisms; fresh-session hooks/config loading remains separate. **40 KB = 40 000 UTF-8 bytes** per active document; warning at 32 000, stricter project budget wins. Do not equate character count or 40 KiB. Compaction means moving to owning artifacts and compact pointers, not deleting facts. Active tasks, acceptance, approvals, gates, decisions and negative evidence retain provenance; original bytes remain recoverable. Archive/evidence may exceed limit under explicit classification but must be indexed; detailed matrices in docs/planning/ remain intact and exempt from default size trigger; they remain active detail. Tables of contents and control-plane retain the limit. Renaming another active matrix as archive does not create an exemption. This expanded matrix remains in existing format; owner deferred its split 10.11.2026 and it is outside remaining G8 closure; the prior preview is not authorized for apply.

Order: T01 → T02 → T03 → T04 → T05; T01 → T06 → T07 → T08; T02/T07 → T09 → T10 → T11; T06/T07 → T12; T05/T08/T10/T11/T12 → T13 → T14. Shared files change sequentially. Named roles do not mean subagents are started.

### Shared G8 verification and approval gates

- For behavior changes: meaningful RED/GREEN and existing focused suites; each card specifies exact focused test command, expect OK. Proposed new T13 module is created only during implementation.
- For each affected docs/control-plane slice: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v`, `python -B tools/check_docs.py`, task-matrix validator and `git diff --check`; expect exit 0. Full runtime/fixture/transcript/compatibility gates follow TEST.md and changed contract, not check count.
- Strict MkDocs mandatory when navigation/links/build evidence changes under current TEST.md; dependencies are not installed without separate authority. Unchanged behavior is not rechecked without reason.
- Proposed results: `docs/superpowers/specs/paos-aud-g8-control-plane-results.json`; proposed report: `research/product-agent-os-g8-execution-report.md`. Results bound to source hashes, fixture revision and environment; failed cases preserved.
- Real Trade, myPartners and myai-partners.app remain read-only sources. G8 does not authorize their cleanup/apply, providers, host cache edits, activation, Git, publication or automation. Compaction apply requires exact reviewable manifest and authority.
- Rollback of each slice restores only owned changes and preserves concurrent work; compaction must additionally prove recovery of all original bytes. HOST fresh-session proof remains separate.

### Task `PAOS-AUD-G8-T01`

- ID: `PAOS-AUD-G8-T01`
- Task: **Task name:** Document structure and ownership contract.
- Short description: **Task description:** Define document classes and the single source of each state type.
- Technical value: **Technical value (for the project):** Eliminates conflicts among generator, workflow and navigation.
- Product value: **Product value (for the user):** It is clear where to find the current decision and what to update.
- Scope: **Affected files:** contracts.py; templates.py; docs/product-agent-os/technical.md. Bare module names refer to `plugins/product-agent-os/scripts/product_agent_os/`, `scripts/` and `assets/` to plugin root; remaining paths are workspace-relative. Corresponding existing test: `tests/product_agent_os/test_infrastructure_templates.py`. Refine directory scope to file manifest before edits.
- Acceptance criteria: **Acceptance criteria:** 1) Inventory covers six control-plane files and existing docs; specifies purpose, owner, required/conditional sections, inputs, outputs and update triggers. 2) Durable rules, current scope, task queue, checks, evals, handoff and history are separate. 3) Status, evidence and owner acceptance are not mixed; existing canonical owners reused. 4) Schema version/migration and compatibility of existing names defined; no new mandatory registry without demonstrated need.
- Group: PAOS-AUD-G8
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 10.11.2026 to complete G8; separate owner acceptance and adoption gates remain.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 17:41
- Depends on: No internal prerequisites; inherited contracts are listed in group section.
- Blocks: PAOS-AUD-G8-T02; PAOS-AUD-G8-T06; PAOS-AUD-G8-T07; PAOS-AUD-G8-T09
- Source: G8-S01, G8-S02; traceability and observation boundaries in group section.
- Non-goals: Changing three external projects, fresh-session activation, automatic history deletion, a new competing status system, Git/provider/publication actions.
- Expected result: Define document classes and the single source of each state type. Result limited to checked local contracts; authorization and owner acceptance are not inferred from file existence.
- Verification gates: `python -B -m unittest tests.product_agent_os.test_infrastructure_templates -v` — OK; positive/negative scenarios from `Acceptance criteria`; shared G8 gates as applicable. Preserve actual commands, results and source revision.
- Risks / approval gates: medium; risk of loss or falsely current documents. Implementation request separate; target apply, sensitive backups and activation have separate boundaries. Rollback only own slice; full T07/T08 recovery contract applies to compaction.
- Complexity: medium
- Estimated execution time: not_estimated; estimate after focused source preflight, no invented deadlines.
- Agents: architect — primary slice owner; primary coordinates shared files; independent review only under authorized dispatch, owner accepts T14 result.
- Skills: canonical implementation-planner; task-matching repository lifecycle skills; for future Python edits python-design-patterns/python-code-style. Implementation approved; canonical skills and Python guidance applied.
- Output artifacts: Changed owning files from Scope; evidence in proposed G8 execution report/results and short RUNLOG pointer; do not create duplicate ledger.
- Next step: Owner accepted T14 / G8 closed; research matrix retained unsplit by owner decision.

#### Completion Report

- status: implemented
- what was done: Owner/field/schema v1 contract and conditional docs inventory.
- files touched / work locations: Owning implementation/test/workflow paths mapped per card in research/product-agent-os-g8-execution-report.md; source hashes in docs/superpowers/specs/paos-aud-g8-control-plane-results.json.
- technical value delivered: Local contract implemented: Owner/field/schema v1 contract and conditional docs inventory.
- product value delivered: Current compact documents, explicit readiness and recoverable history in checked synthetic scenarios.
- actual implementation date and time: 10-11-2026 17:41
- verification evidence: Focused verification and synthetic comparisons recorded in G8 execution report/results; final integrated receipts belong to that report.
- residual risks: Synthetic/local evidence only; T14 owner accepted; fresh-session activation separate; research matrix split deferred by owner; docs/planning detailed matrices remain intact; actual M1 integration owned by M1.
- follow-up: T14 owner accepted; research matrix remains unsplit by owner decision; separate fresh-session activation.

### Task `PAOS-AUD-G8-T02`

- ID: `PAOS-AUD-G8-T02`
- Task: **Task name:** Adaptive templates and dependency closure.
- Short description: **Task description:** Form the minimum sufficient file set for the task, project size and stack.
- Technical value: **Technical value (for the project):** Removes empty mandatory packets and references to nonexistent procedures.
- Product value: **Product value (for the user):** A small project receives a compact start, a large one the necessary routes.
- Scope: **Affected files:** templates.py; task_routing.py; assets/templates/control-plane/; assets/templates/workflows/. Bare module names refer to `plugins/product-agent-os/scripts/product_agent_os/`, `scripts/` and `assets/` to plugin root; remaining paths are workspace-relative. Corresponding existing test: `tests/product_agent_os/test_infrastructure_templates.py`. Refine directory scope to file manifest before edits.
- Acceptance criteria: **Acceptance criteria:** 1) Ordinary route reuses documents; full route explains every added file. 2) Every config/workflow/template reference resolves to an existing file, staged companion or explicit gap. 3) AGENTS contains durable routing, no task ledger. 4) Conditional EVALS, architecture, decisions and operations are not created empty for completeness. 5) Hooks/automation are not activated during generation.
- Group: PAOS-AUD-G8
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 10.11.2026 to complete G8; separate owner acceptance and adoption gates remain.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 17:41
- Depends on: PAOS-AUD-G8-T01
- Blocks: PAOS-AUD-G8-T03; PAOS-AUD-G8-T09
- Source: G8-S01, G8-S03; traceability and observation boundaries in group section.
- Non-goals: Changing three external projects, fresh-session activation, automatic history deletion, a new competing status system, Git/provider/publication actions.
- Expected result: Form the minimum sufficient file set for the task, project size and stack. Result limited to checked local contracts; authorization and owner acceptance are not inferred from file existence.
- Verification gates: `python -B -m unittest tests.product_agent_os.test_infrastructure_templates -v` — OK; positive/negative scenarios from `Acceptance criteria`; shared G8 gates as applicable. Preserve actual commands, results and source revision.
- Risks / approval gates: medium; risk of loss or falsely current documents. Implementation request separate; target apply, sensitive backups and activation have separate boundaries. Rollback only own slice; full T07/T08 recovery contract applies to compaction.
- Complexity: medium
- Estimated execution time: not_estimated; estimate after focused source preflight, no invented deadlines.
- Agents: plugin-runtime-builder — primary slice owner; primary coordinates shared files; independent review only under authorized dispatch, owner accepts T14 result.
- Skills: canonical implementation-planner; task-matching repository lifecycle skills; for future Python edits python-design-patterns/python-code-style. Implementation approved; canonical skills and Python guidance applied.
- Output artifacts: Changed owning files from Scope; evidence in proposed G8 execution report/results and short RUNLOG pointer; do not create duplicate ledger.
- Next step: Owner accepted T14 / G8 closed; research matrix retained unsplit by owner decision.

#### Completion Report

- status: implemented
- what was done: Scoped templates, conditional EVALS, per-file reasons and dependency-gap diagnostics.
- files touched / work locations: Owning implementation/test/workflow paths mapped per card in research/product-agent-os-g8-execution-report.md; source hashes in docs/superpowers/specs/paos-aud-g8-control-plane-results.json.
- technical value delivered: Local contract implemented: Scoped templates, conditional EVALS, per-file reasons and dependency-gap diagnostics.
- product value delivered: Current compact documents, explicit readiness and recoverable history in checked synthetic scenarios.
- actual implementation date and time: 10-11-2026 17:41
- verification evidence: Focused verification and synthetic comparisons recorded in G8 execution report/results; final integrated receipts belong to that report.
- residual risks: Synthetic/local evidence only; T14 owner accepted; fresh-session activation separate; research matrix split deferred by owner; docs/planning detailed matrices remain intact; actual M1 integration owned by M1.
- follow-up: T14 owner accepted; research matrix remains unsplit by owner decision; separate fresh-session activation.

### Task `PAOS-AUD-G8-T03`

- ID: `PAOS-AUD-G8-T03`
- Task: **Task name:** Substantive population and readiness levels.
- Short description: **Task description:** Connect approved intake/packets to document fields and verify substantive readiness.
- Technical value: **Technical value (for the project):** Distinguishes scaffold from verified current control plane.
- Product value: **Product value (for the user):** File existence no longer creates a false impression of readiness.
- Scope: **Affected files:** templates.py; validators.py; discovery.py; scripts/validate_control_plane.py. Bare module names refer to `plugins/product-agent-os/scripts/product_agent_os/`, `scripts/` and `assets/` to plugin root; remaining paths are workspace-relative. Corresponding existing test: `tests/product_agent_os/test_validators.py`. Refine directory scope to file manifest before edits.
- Acceptance criteria: **Acceptance criteria:** 1) Approved decisions, scope, IDs, constraints and acceptance transfer with provenance; unknown is marked missing, not invented. 2) A directory instead of a file, empty file and unpopulated scaffold do not pass readiness. 3) scaffold/draft/reviewed/accepted/stale are separate; accepted requires owner evidence. 4) RU/EN headings preserve meaning. 5) Legacy structural validation remains in explicit mode and is not presented as semantic validation.
- Group: PAOS-AUD-G8
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 10.11.2026 to complete G8; separate owner acceptance and adoption gates remain.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 17:41
- Depends on: PAOS-AUD-G8-T02
- Blocks: PAOS-AUD-G8-T04; PAOS-AUD-G8-T10
- Source: G8-S01; traceability and observation boundaries in group section.
- Non-goals: Changing three external projects, fresh-session activation, automatic history deletion, a new competing status system, Git/provider/publication actions.
- Expected result: Connect approved intake/packets to document fields and verify substantive readiness. Result limited to checked local contracts; authorization and owner acceptance are not inferred from file existence.
- Verification gates: `python -B -m unittest tests.product_agent_os.test_validators -v` — OK; positive/negative scenarios from `Acceptance criteria`; shared G8 gates as applicable. Preserve actual commands, results and source revision.
- Risks / approval gates: high; risk of loss or falsely current documents. Implementation request separate; target apply, sensitive backups and activation have separate boundaries. Rollback only own slice; full T07/T08 recovery contract applies to compaction.
- Complexity: high
- Estimated execution time: not_estimated; estimate after focused source preflight, no invented deadlines.
- Agents: plugin-runtime-builder — primary slice owner; primary coordinates shared files; independent review only under authorized dispatch, owner accepts T14 result.
- Skills: canonical implementation-planner; task-matching repository lifecycle skills; for future Python edits python-design-patterns/python-code-style. Implementation approved; canonical skills and Python guidance applied.
- Output artifacts: Changed owning files from Scope; evidence in proposed G8 execution report/results and short RUNLOG pointer; do not create duplicate ledger.
- Next step: Owner accepted T14 / G8 closed; research matrix retained unsplit by owner decision.

#### Completion Report

- status: implemented
- what was done: Provenance population and semantic readiness with digest-bound review/owner receipts.
- files touched / work locations: Owning implementation/test/workflow paths mapped per card in research/product-agent-os-g8-execution-report.md; source hashes in docs/superpowers/specs/paos-aud-g8-control-plane-results.json.
- technical value delivered: Local contract implemented: Provenance population and semantic readiness with digest-bound review/owner receipts.
- product value delivered: Current compact documents, explicit readiness and recoverable history in checked synthetic scenarios.
- actual implementation date and time: 10-11-2026 17:41
- verification evidence: Focused verification and synthetic comparisons recorded in G8 execution report/results; final integrated receipts belong to that report.
- residual risks: Synthetic/local evidence only; T14 owner accepted; fresh-session activation separate; research matrix split deferred by owner; docs/planning detailed matrices remain intact; actual M1 integration owned by M1.
- follow-up: T14 owner accepted; research matrix remains unsplit by owner decision; separate fresh-session activation.

### Task `PAOS-AUD-G8-T04`

- ID: `PAOS-AUD-G8-T04`
- Task: **Task name:** Safe regeneration of populated sections.
- Short description: **Task description:** Preserve entered values when updating managed sections.
- Technical value: **Technical value (for the project):** Prevents loss of decisions during rerender/merge.
- Product value: **Product value (for the user):** User can update infrastructure without filling everything again.
- Scope: **Affected files:** templates.py; merge_markdown.py; merge_infrastructure.py; stage_manifest.py. Bare module names refer to `plugins/product-agent-os/scripts/product_agent_os/`, `scripts/` and `assets/` to plugin root; remaining paths are workspace-relative. Corresponding existing test: `tests/product_agent_os/test_merge_markdown.py`. Refine directory scope to file manifest before edits.
- Acceptance criteria: **Acceptance criteria:** 1) A full managed body is not replaced with an empty template. 2) Template version/baseline and user changes yield safe merge or explicit conflict. 3) User-authored regions preserved byte-for-byte. 4) Rerun is idempotent, no time-only diff. 5) Missing/duplicate/malformed markers cause conflict without write. 6) Dirty uncommitted data is included in baseline.
- Group: PAOS-AUD-G8
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 10.11.2026 to complete G8; separate owner acceptance and adoption gates remain.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 17:41
- Depends on: PAOS-AUD-G8-T03
- Blocks: PAOS-AUD-G8-T05; PAOS-AUD-G8-T08
- Source: G8-S01, G8-S03; traceability and observation boundaries in group section.
- Non-goals: Changing three external projects, fresh-session activation, automatic history deletion, a new competing status system, Git/provider/publication actions.
- Expected result: Preserve entered values when updating managed sections. Result limited to checked local contracts; authorization and owner acceptance are not inferred from file existence.
- Verification gates: `python -B -m unittest tests.product_agent_os.test_merge_markdown -v` — OK; positive/negative scenarios from `Acceptance criteria`; shared G8 gates as applicable. Preserve actual commands, results and source revision.
- Risks / approval gates: high; risk of loss or falsely current documents. Implementation request separate; target apply, sensitive backups and activation have separate boundaries. Rollback only own slice; full T07/T08 recovery contract applies to compaction.
- Complexity: high
- Estimated execution time: not_estimated; estimate after focused source preflight, no invented deadlines.
- Agents: plugin-runtime-builder — primary slice owner; primary coordinates shared files; independent review only under authorized dispatch, owner accepts T14 result.
- Skills: canonical implementation-planner; task-matching repository lifecycle skills; for future Python edits python-design-patterns/python-code-style. Implementation approved; canonical skills and Python guidance applied.
- Output artifacts: Changed owning files from Scope; evidence in proposed G8 execution report/results and short RUNLOG pointer; do not create duplicate ledger.
- Next step: Owner accepted T14 / G8 closed; research matrix retained unsplit by owner decision.

#### Completion Report

- status: implemented
- what was done: Preservation of filled managed body and companion-only bulk merge, without automatic replacement.
- files touched / work locations: Owning implementation/test/workflow paths mapped per card in research/product-agent-os-g8-execution-report.md; source hashes in docs/superpowers/specs/paos-aud-g8-control-plane-results.json.
- technical value delivered: Local contract implemented: Preservation of filled managed body and companion-only bulk merge, without automatic replacement.
- product value delivered: Current compact documents, explicit readiness and recoverable history in checked synthetic scenarios.
- actual implementation date and time: 10-11-2026 17:41
- verification evidence: Focused verification and synthetic comparisons recorded in G8 execution report/results; final integrated receipts belong to that report.
- residual risks: Synthetic/local evidence only; T14 owner accepted; fresh-session activation separate; research matrix split deferred by owner; docs/planning detailed matrices remain intact; actual M1 integration owned by M1.
- follow-up: T14 owner accepted; research matrix remains unsplit by owner decision; separate fresh-session activation.

### Task `PAOS-AUD-G8-T05`

- ID: `PAOS-AUD-G8-T05`
- Task: **Task name:** Dry-run, stage and final-document parity.
- Short description: **Task description:** Check actual project context and merged content.
- Technical value: **Technical value (for the project):** Preview report matches future apply.
- Product value: **Product value (for the user):** Preview shows actual changes and actual gaps.
- Scope: **Affected files:** infrastructure.py; stage_manifest.py; scripts/render_infrastructure.py. Bare module names refer to `plugins/product-agent-os/scripts/product_agent_os/`, `scripts/` and `assets/` to plugin root; remaining paths are workspace-relative. Corresponding existing test: `tests/product_agent_os/test_infrastructure_renderer.py`. Refine directory scope to file manifest before edits.
- Acceptance criteria: **Acceptance criteria:** 1) Dry-run and stage on one baseline yield identical selection, dependencies, byte sizes and validation outcomes. 2) Validation uses actual project context and merged text; synthetic validation context does not mask an error. 3) Dry-run does not write to target; stage is outside target. 4) Unicode paths and Markdown escaping covered. 5) Changed target makes old preview stale.
- Group: PAOS-AUD-G8
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 10.11.2026 to complete G8; separate owner acceptance and adoption gates remain.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 17:41
- Depends on: PAOS-AUD-G8-T04
- Blocks: PAOS-AUD-G8-T13
- Source: G8-S01; traceability and observation boundaries in group section.
- Non-goals: Changing three external projects, fresh-session activation, automatic history deletion, a new competing status system, Git/provider/publication actions.
- Expected result: Check actual project context and merged content. Result limited to checked local contracts; authorization and owner acceptance are not inferred from file existence.
- Verification gates: `python -B -m unittest tests.product_agent_os.test_infrastructure_renderer -v` — OK; positive/negative scenarios from `Acceptance criteria`; shared G8 gates as applicable. Preserve actual commands, results and source revision.
- Risks / approval gates: medium; risk of loss or falsely current documents. Implementation request separate; target apply, sensitive backups and activation have separate boundaries. Rollback only own slice; full T07/T08 recovery contract applies to compaction.
- Complexity: medium
- Estimated execution time: not_estimated; estimate after focused source preflight, no invented deadlines.
- Agents: tester — primary slice owner; primary coordinates shared files; independent review only under authorized dispatch, owner accepts T14 result.
- Skills: canonical implementation-planner; task-matching repository lifecycle skills; for future Python edits python-design-patterns/python-code-style. Implementation approved; canonical skills and Python guidance applied.
- Output artifacts: Changed owning files from Scope; evidence in proposed G8 execution report/results and short RUNLOG pointer; do not create duplicate ledger.
- Next step: Owner accepted T14 / G8 closed; research matrix retained unsplit by owner decision.

#### Completion Report

- status: implemented
- what was done: Actual-content dry-run/stage validation, deterministic bytes and stale-target guards.
- files touched / work locations: Owning implementation/test/workflow paths mapped per card in research/product-agent-os-g8-execution-report.md; source hashes in docs/superpowers/specs/paos-aud-g8-control-plane-results.json.
- technical value delivered: Local contract implemented: Actual-content dry-run/stage validation, deterministic bytes and stale-target guards.
- product value delivered: Current compact documents, explicit readiness and recoverable history in checked synthetic scenarios.
- actual implementation date and time: 10-11-2026 17:41
- verification evidence: Focused verification and synthetic comparisons recorded in G8 execution report/results; final integrated receipts belong to that report.
- residual risks: Synthetic/local evidence only; T14 owner accepted; fresh-session activation separate; research matrix split deferred by owner; docs/planning detailed matrices remain intact; actual M1 integration owned by M1.
- follow-up: T14 owner accepted; research matrix remains unsplit by owner decision; separate fresh-session activation.

### Task `PAOS-AUD-G8-T06`

- ID: `PAOS-AUD-G8-T06`
- Task: **Task name:** Unified UTF-8 40 KB budget.
- Short description: **Task description:** Replace chars/KiB ambiguity with explicit byte contract for active documents.
- Technical value: **Technical value (for the project):** Makes the limit measurable and consistent across surfaces.
- Product value: **Product value (for the user):** Working documents remain manageable in size.
- Scope: **Affected files:** system_file_hygiene.py; scripts/validate_system_file_hygiene.py; assets/templates/workflows/runlog-compaction.md; .codex/workflows/runlog-compaction.md. Bare module names refer to `plugins/product-agent-os/scripts/product_agent_os/`, `scripts/` and `assets/` to plugin root; remaining paths are workspace-relative. Corresponding existing test: `tests/product_agent_os/test_system_file_hygiene.py`. Refine directory scope to file manifest before edits.
- Acceptance criteria: **Acceptance criteria:** 1) Default hard budget 40 000 UTF-8 bytes, warning 32 000; exactly 40 000 allowed, 40 001 requires proposal. 2) Stricter project limit retained, including 20 000 in Trade; old char/50KiB settings have explicit migration. 3) Test 39 999/40 000/40 001, RU/EN/emoji/BOM/CRLF. 4) Policy covers active control-plane and navigation files; detailed docs/planning/ matrices remain intact; exception does not apply to indexes, root files or explicit per-file limits. 5) History/evidence/generated/datasets classified separately, exception has owner/reason and does not hide active dump. 6) Exceeding limit does not delete data or block read-only inspection.
- Group: PAOS-AUD-G8
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 10.11.2026 to complete G8; separate owner acceptance and adoption gates remain.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 17:41
- Depends on: PAOS-AUD-G8-T01
- Blocks: PAOS-AUD-G8-T07; PAOS-AUD-G8-T12
- Source: G8-S04, G8-S05, G8-S06; traceability and observation boundaries in group section.
- Non-goals: Changing three external projects, fresh-session activation, automatic history deletion, a new competing status system, Git/provider/publication actions.
- Expected result: Replace chars/KiB ambiguity with explicit byte contract for active documents. Result limited to checked local contracts; authorization and owner acceptance are not inferred from file existence.
- Verification gates: `python -B -m unittest tests.product_agent_os.test_system_file_hygiene -v` — OK; positive/negative scenarios from `Acceptance criteria`; shared G8 gates as applicable. Preserve actual commands, results and source revision.
- Risks / approval gates: medium; risk of loss or falsely current documents. Implementation request separate; target apply, sensitive backups and activation have separate boundaries. Rollback only own slice; full T07/T08 recovery contract applies to compaction.
- Complexity: medium
- Estimated execution time: not_estimated; estimate after focused source preflight, no invented deadlines.
- Agents: plugin-runtime-builder — primary slice owner; primary coordinates shared files; independent review only under authorized dispatch, owner accepts T14 result.
- Skills: canonical implementation-planner; task-matching repository lifecycle skills; for future Python edits python-design-patterns/python-code-style. Implementation approved; canonical skills and Python guidance applied.
- Output artifacts: Changed owning files from Scope; evidence in proposed G8 execution report/results and short RUNLOG pointer; do not create duplicate ledger.
- Next step: Owner accepted T14 / G8 closed; research matrix retained unsplit by owner decision.

#### Completion Report

- status: implemented
- what was done: UTF-8 budget 40000/32000, stricter limits, RU/EN/emoji/BOM/CRLF, indexed exemptions and size-only exception for detailed docs/planning matrices.
- files touched / work locations: Owning implementation/test/workflow paths mapped per card in research/product-agent-os-g8-execution-report.md; source hashes in docs/superpowers/specs/paos-aud-g8-control-plane-results.json.
- technical value delivered: Local contract implemented: UTF-8 budget 40000/32000, stricter limits, RU/EN/emoji/BOM/CRLF, indexed exemptions and size-only exception for detailed docs/planning matrices.
- product value delivered: Current compact documents, explicit readiness and recoverable history in checked synthetic scenarios.
- actual implementation date and time: 10-11-2026 17:41
- verification evidence: Focused verification and synthetic comparisons recorded in G8 execution report/results; final integrated receipts belong to that report.
- residual risks: Synthetic/local evidence only; T14 owner accepted; fresh-session activation separate; research matrix split deferred by owner; docs/planning detailed matrices remain intact; actual M1 integration owned by M1.
- follow-up: T14 owner accepted; research matrix remains unsplit by owner decision; separate fresh-session activation.

### Task `PAOS-AUD-G8-T07`

- ID: `PAOS-AUD-G8-T07`
- Task: **Task name:** Lossless compaction proposal and preservation map.
- Short description: **Task description:** Build baseline, destinations and verifiable transfer map before compaction.
- Technical value: **Technical value (for the project):** Provides proof of fact preservation and recovery.
- Product value: **Product value (for the user):** Compaction does not lose requirements, decisions or unfinished tasks.
- Scope: **Affected files:** system_file_hygiene.py; assets/templates/workflows/runlog-compaction.md; .codex/workflows/control-plane-sync.md. Bare module names refer to `plugins/product-agent-os/scripts/product_agent_os/`, `scripts/` and `assets/` to plugin root; remaining paths are workspace-relative. Corresponding existing test: `tests/product_agent_os/test_system_file_hygiene.py`. Refine directory scope to file manifest before edits.
- Acceptance criteria: **Acceptance criteria:** 1) Read-only proposal contains before hashes/bytes, exact diff, after forecast, destination and retention reason for every moved block. 2) Lossless baseline includes dirty/untracked input; Git history is not the only backup. 3) Preserve task IDs/DAG, constraints, approvals, open gates, negative attempts, evidence hashes and owner decisions. 4) Reuse existing owning artifact; semantic summary does not replace original evidence. 5) Ambiguous classification stops transfer of that block. 6) Backup does not expand disclosure/storage boundary; recovery verified before apply.
- Group: PAOS-AUD-G8
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 10.11.2026 to complete G8; separate owner acceptance and adoption gates remain.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 17:41
- Depends on: PAOS-AUD-G8-T01; PAOS-AUD-G8-T06
- Blocks: PAOS-AUD-G8-T08; PAOS-AUD-G8-T09; PAOS-AUD-G8-T12
- Source: G8-S04, G8-S05, G8-S06; traceability and observation boundaries in group section.
- Non-goals: Changing three external projects, fresh-session activation, automatic history deletion, a new competing status system, Git/provider/publication actions.
- Expected result: Build baseline, destinations and verifiable transfer map before compaction. Result limited to checked local contracts; authorization and owner acceptance are not inferred from file existence.
- Verification gates: `python -B -m unittest tests.product_agent_os.test_system_file_hygiene -v` — OK; positive/negative scenarios from `Acceptance criteria`; shared G8 gates as applicable. Preserve actual commands, results and source revision.
- Risks / approval gates: high; risk of loss or falsely current documents. Implementation request separate; target apply, sensitive backups and activation have separate boundaries. Rollback only own slice; full T07/T08 recovery contract applies to compaction.
- Complexity: high
- Estimated execution time: not_estimated; estimate after focused source preflight, no invented deadlines.
- Agents: architect — primary slice owner; primary coordinates shared files; independent review only under authorized dispatch, owner accepts T14 result.
- Skills: canonical implementation-planner; task-matching repository lifecycle skills; for future Python edits python-design-patterns/python-code-style. Implementation approved; canonical skills and Python guidance applied.
- Output artifacts: Changed owning files from Scope; evidence in proposed G8 execution report/results and short RUNLOG pointer; do not create duplicate ledger.
- Next step: Owner accepted T14 / G8 closed; research matrix retained unsplit by owner decision.

#### Completion Report

- status: implemented
- what was done: Lossless proposal, before/after bytes, diff, preservation map and independent conservation replay.
- files touched / work locations: Owning implementation/test/workflow paths mapped per card in research/product-agent-os-g8-execution-report.md; source hashes in docs/superpowers/specs/paos-aud-g8-control-plane-results.json.
- technical value delivered: Local contract implemented: Lossless proposal, before/after bytes, diff, preservation map and independent conservation replay.
- product value delivered: Current compact documents, explicit readiness and recoverable history in checked synthetic scenarios.
- actual implementation date and time: 10-11-2026 17:41
- verification evidence: Focused verification and synthetic comparisons recorded in G8 execution report/results; final integrated receipts belong to that report.
- residual risks: Synthetic/local evidence only; T14 owner accepted; fresh-session activation separate; research matrix split deferred by owner; docs/planning detailed matrices remain intact; actual M1 integration owned by M1.
- follow-up: T14 owner accepted; research matrix remains unsplit by owner decision; separate fresh-session activation.

### Task `PAOS-AUD-G8-T08`

- ID: `PAOS-AUD-G8-T08`
- Task: **Task name:** Transactional compaction apply and rollback.
- Short description: **Task description:** Apply only an approved proposal with concurrent-change protection.
- Technical value: **Technical value (for the project):** Prevent partial source loss on failure.
- Product value: **Product value (for the user):** Compaction can be safely rolled back as a whole.
- Scope: **Affected files:** merge_infrastructure.py; stage_manifest.py; system_file_hygiene.py. Bare module names refer to `plugins/product-agent-os/scripts/product_agent_os/`, `scripts/` and `assets/` to plugin root; other paths workspace-relative. Corresponding existing test: `tests/product_agent_os/test_merge_infrastructure.py`. Refine directory scope to file manifest before edits.
- Acceptance criteria: **Acceptance criteria:** 1) Explicit apply authority binds exact manifest; source/destination hashes checked before writing. 2) Shared files have one writer; concurrent changes yield conflict, not overwrite. 3) Journal/staging and fault injection demonstrate recovery after failure between writes; no multi-file atomicity claim without proof. 4) Rollback restores original bytes and handles created files while preserving others' changes. 5) Repeat apply safe; path traversal, junction/symlink and Windows case collisions rejected. 6) No automatic history deletion; completion only after preservation, links and size checks.
- Group: PAOS-AUD-G8
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 10.11.2026 to complete G8; separate owner acceptance and adoption gates retained.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 17:41
- Depends on: PAOS-AUD-G8-T04; PAOS-AUD-G8-T07
- Blocks: PAOS-AUD-G8-T13
- Source: G8-S03, G8-S04; traceability and observation boundaries in group section.
- Non-goals: Changes to three external projects, fresh-session activation, automatic history deletion, new competing status system, Git/provider/publication actions.
- Expected result: Apply only approved proposal with concurrent-change protection. Outcome bounded by verified local contracts; authorization and owner acceptance not inferred from file presence.
- Verification gates: `python -B -m unittest tests.product_agent_os.test_merge_infrastructure -v` — OK; positive/negative `Acceptance criteria` scenarios; shared G8 gates as applicable. Preserve actual commands, results and source revision.
- Risks / approval gates: high; risk of loss or false currency of documents. Separate implementation request; target apply, sensitive backups and activation have separate boundaries. Rollback own slice only; full T07/T08 recovery contract applies to compaction.
- Complexity: high
- Estimated execution time: not_estimated; assess after focused source preflight, no invented timelines.
- Agents: plugin-runtime-builder — primary slice owner; primary coordinates shared files; independent review only under authorized dispatch, owner accepts T14 outcome.
- Skills: canonical implementation-planner; task-matching repository lifecycle skills; for future Python edits python-design-patterns/python-code-style. Implementation approved; canonical skills and Python guidance applied.
- Output artifacts: Changed owning files from Scope; evidence in proposed G8 execution report/results and compact RUNLOG pointer; no duplicate ledger.
- Next step: Owner accepted T14 / G8 closed; research matrix retained unsplit by owner decision.

#### Completion Report

- status: implemented
- what was done: Exact-digest apply, CAS/lock/journal, process-crash recovery, rollback and conflict scenarios.
- files touched / work locations: Owning implementation/test/workflow paths mapped per card in research/product-agent-os-g8-execution-report.md; source hashes in docs/superpowers/specs/paos-aud-g8-control-plane-results.json.
- technical value delivered: Local contract implemented: Exact-digest apply, CAS/lock/journal, process-crash recovery, rollback and conflict scenarios.
- product value delivered: Current compact documents, explicit readiness and recoverable history in verified synthetic scenarios.
- actual implementation date and time: 10-11-2026 17:41
- verification evidence: Focused verification and synthetic comparisons recorded in G8 execution report/results; final integrated receipts belong to that report.
- residual risks: Synthetic/local evidence only; T14 owner accepted; fresh-session activation separate; research matrix split deferred by owner; docs/planning detailed matrices remain intact; actual M1 integration owned by M1.
- follow-up: T14 owner accepted; research matrix remains unsplit by owner decision; separate fresh-session activation.

### Task `PAOS-AUD-G8-T09`

- ID: `PAOS-AUD-G8-T09`
- Task: **Task name:** Documentation navigation and large plan decomposition.
- Short description: **Task description:** Define discoverable docs structure and division by responsibility.
- Technical value: **Technical value (for the project):** Reduces duplication and preserves links as project grows.
- Product value: **Product value (for the user):** Next executor quickly finds relevant contract and evidence.
- Scope: **Affected files:** assets/templates/control-plane/; assets/templates/workflows/project-formation.md; docs/product-agent-os/architecture.md; task_plan_lifecycle.py. Bare module names refer to `plugins/product-agent-os/scripts/product_agent_os/`, `scripts/` and `assets/` to plugin root; other paths workspace-relative. Corresponding existing test: `tests/product_agent_os/test_task_plan_lifecycle.py`. Refine directory scope to file manifest before edits.
- Acceptance criteria: **Acceptance criteria:** 1) docs index leads to current requirements, architecture/components, ADR, contracts/data, operations/runbooks, verification/evidence and archive only as applicable. 2) Each conditional file has trigger, owner and canonical source; docs taxonomy adapts to existing structure. 3) Splitting mechanism available only for separately approved documents, preserving IDs, dependencies and selector; detailed docs/planning/ matrices not split due to size. 4) Incoming links/anchors receive checked migration map/redirect; old receipts available. 5) Archive does not become another unnamed megadocument; map and search support history. 6) Owner decision 10.11.2026: current research/ audit matrix not split; cards and layout retained, preview remains historical proposal.
- Group: PAOS-AUD-G8
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 10.11.2026 to complete G8; separate owner acceptance and adoption gates retained.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 17:41
- Depends on: PAOS-AUD-G8-T01; PAOS-AUD-G8-T02; PAOS-AUD-G8-T07
- Blocks: PAOS-AUD-G8-T10; PAOS-AUD-G8-T11
- Source: G8-S05, G8-S06, G8-S07; traceability and observation boundaries in group section.
- Non-goals: Changes to three external projects, fresh-session activation, automatic history deletion, new competing status system, Git/provider/publication actions.
- Expected result: Define discoverable docs structure and division by responsibility. Outcome bounded by verified local contracts; authorization and owner acceptance not inferred from file presence.
- Verification gates: `python -B -m unittest tests.product_agent_os.test_task_plan_lifecycle -v` — OK; positive/negative `Acceptance criteria` scenarios; shared G8 gates as applicable. Preserve actual commands, results and source revision.
- Risks / approval gates: high; risk of loss or false currency of documents. Separate implementation request; target apply, sensitive backups and activation have separate boundaries. Rollback own slice only; full T07/T08 recovery contract applies to compaction.
- Complexity: high
- Estimated execution time: not_estimated; assess after focused source preflight, no invented timelines.
- Agents: docs-maintainer — primary slice owner; primary coordinates shared files; independent review only under authorized dispatch, owner accepts T14 outcome.
- Skills: canonical implementation-planner; task-matching repository lifecycle skills; for future Python edits python-design-patterns/python-code-style. Implementation approved; canonical skills and Python guidance applied.
- Output artifacts: Changed owning files from Scope; evidence in proposed G8 execution report/results and compact RUNLOG pointer; no duplicate ledger.
- Next step: Owner accepted T14 / G8 closed; research matrix retained unsplit by owner decision.

#### Completion Report

- status: implemented
- what was done: Adaptive docs navigation and whole-card split/anchor migration; actual matrix preview retained historically; owner kept research matrix whole; docs/planning detailed matrices exempt.
- files touched / work locations: Owning implementation/test/workflow paths mapped per card in research/product-agent-os-g8-execution-report.md; source hashes in docs/superpowers/specs/paos-aud-g8-control-plane-results.json.
- technical value delivered: Local contract implemented: Adaptive docs navigation and whole-card split/anchor migration; actual matrix preview retained historically; owner kept research matrix whole; docs/planning detailed matrices exempt.
- product value delivered: Current compact documents, explicit readiness and recoverable history in verified synthetic scenarios.
- actual implementation date and time: 10-11-2026 17:41
- verification evidence: Focused verification and synthetic comparisons recorded in G8 execution report/results; final integrated receipts belong to that report.
- residual risks: Synthetic/local evidence only; T14 owner accepted; fresh-session activation separate; research matrix split deferred by owner; docs/planning detailed matrices remain intact; actual M1 integration owned by M1.
- follow-up: T14 owner accepted; research matrix remains unsplit by owner decision; separate fresh-session activation.

### Task `PAOS-AUD-G8-T10`

- ID: `PAOS-AUD-G8-T10`
- Task: **Task name:** Status freshness and legacy state resolution.
- Short description: **Task description:** Reconcile start pages and legacy state with canonical owner and revision.
- Technical value: **Technical value (for the project):** Removes false stage/readiness conclusions from headings and old README.
- Product value: **Product value (for the user):** User sees what is actually done and open.
- Scope: **Affected files:** discovery.py; task_plan_lifecycle.py; scripts/codex_runtime_runner/state.py; docs/product-agent-os/control-plane-current-state.md. Bare module names refer to `plugins/product-agent-os/scripts/product_agent_os/`, `scripts/` and `assets/` to plugin root; other paths workspace-relative. Corresponding existing test: `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`. Refine directory scope to file manifest before edits.
- Acceptance criteria: **Acceptance criteria:** 1) README/start-here and root pointers do not store competing statuses. 2) Legacy state does not infer readiness from English heading/config presence alone. 3) Current source/revision and historical receipt distinguishable; missing/stale/unknown do not become pass. 4) Accepted decisions not invalidated solely by age. 5) Repeated blocks yield diagnostic; semantic dedup requires review, not automatic deletion. 6) Existing current-state mechanism reused without second status registry.
- Group: PAOS-AUD-G8
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 10.11.2026 to complete G8; separate owner acceptance and adoption gates retained.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 17:41
- Depends on: PAOS-AUD-G8-T03; PAOS-AUD-G8-T09
- Blocks: PAOS-AUD-G8-T11; PAOS-AUD-G8-T13
- Source: G8-S01, G8-S06, G8-S07; traceability and observation boundaries in group section.
- Non-goals: Changes to three external projects, fresh-session activation, automatic history deletion, new competing status system, Git/provider/publication actions.
- Expected result: Reconcile start pages and legacy state with canonical owner and revision. Outcome bounded by verified local contracts; authorization and owner acceptance not inferred from file presence.
- Verification gates: `python -B -m unittest tests.product_agent_os.test_codex_runtime_runner_state_routes -v` — OK; positive/negative `Acceptance criteria` scenarios; shared G8 gates as applicable. Preserve actual commands, results and source revision.
- Risks / approval gates: medium; risk of loss or false currency of documents. Separate implementation request; target apply, sensitive backups and activation have separate boundaries. Rollback own slice only; full T07/T08 recovery contract applies to compaction.
- Complexity: medium
- Estimated execution time: not_estimated; assess after focused source preflight, no invented timelines.
- Agents: plugin-runtime-builder — primary slice owner; primary coordinates shared files; independent review only under authorized dispatch, owner accepts T14 outcome.
- Skills: canonical implementation-planner; task-matching repository lifecycle skills; for future Python edits python-design-patterns/python-code-style. Implementation approved; canonical skills and Python guidance applied.
- Output artifacts: Changed owning files from Scope; evidence in proposed G8 execution report/results and compact RUNLOG pointer; no duplicate ledger.
- Next step: Owner accepted T14 / G8 closed; research matrix retained unsplit by owner decision.

#### Completion Report

- status: implemented
- what was done: Legacy heading readiness removed; source-bound state and duplicate diagnostics.
- files touched / work locations: Owning implementation/test/workflow paths mapped per card in research/product-agent-os-g8-execution-report.md; source hashes in docs/superpowers/specs/paos-aud-g8-control-plane-results.json.
- technical value delivered: Local contract implemented: Legacy heading readiness removed; source-bound state and duplicate diagnostics.
- product value delivered: Current compact documents, explicit readiness and recoverable history in verified synthetic scenarios.
- actual implementation date and time: 10-11-2026 17:41
- verification evidence: Focused verification and synthetic comparisons recorded in G8 execution report/results; final integrated receipts belong to that report.
- residual risks: Synthetic/local evidence only; T14 owner accepted; fresh-session activation separate; research matrix split deferred by owner; docs/planning detailed matrices remain intact; actual M1 integration owned by M1.
- follow-up: T14 owner accepted; research matrix remains unsplit by owner decision; separate fresh-session activation.

### Task `PAOS-AUD-G8-T11`

- ID: `PAOS-AUD-G8-T11`
- Task: **Task name:** Portability of mirrors, evidence and cross-project references.
- Short description: **Task description:** Check generated mirrors and evidence availability without mixing sources.
- Technical value: **Technical value (for the project):** Removes verification dependency on unrecorded local files.
- Product value: **Product value (for the user):** Documents remain useful after clone and project transfer.
- Scope: **Affected files:** validators.py; docs/product-agent-os/technical.md; tools/check_docs.py; tests/product_agent_os/test_product_agent_os_docs.py. Bare module names refer to `plugins/product-agent-os/scripts/product_agent_os/`, `scripts/` and `assets/` to plugin root; other paths workspace-relative. Corresponding existing test: `tests/product_agent_os/test_product_agent_os_docs.py`. Refine directory scope to file manifest before edits.
- Acceptance criteria: **Acceptance criteria:** 1) Mirror contains canonical path/revision and read-only drift check; copied AGENTS does not create unintended instruction scope. 2) Required evidence available in declared clean-checkout/offline profile; local optional evidence explicitly separated. 3) Cross-repo refs include repo identity, relative path, revision and claim boundary; unavailable source yields unknown. 4) Check does not copy private data or absolute user paths into fixtures. 5) Known G6/G7 docs links outside docs_dir classified and fixed in owning navigation without changing historical outcomes; strict build as applicable.
- Group: PAOS-AUD-G8
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 10.11.2026 to complete G8; separate owner acceptance and adoption gates retained.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 17:41
- Depends on: PAOS-AUD-G8-T09; PAOS-AUD-G8-T10
- Blocks: PAOS-AUD-G8-T13
- Source: G8-S05, G8-S06, G8-S07, G8-S08; traceability and observation boundaries in group section.
- Non-goals: Changes to three external projects, fresh-session activation, automatic history deletion, new competing status system, Git/provider/publication actions.
- Expected result: Check generated mirrors and evidence availability without mixing sources. Outcome bounded by verified local contracts; authorization and owner acceptance not inferred from file presence.
- Verification gates: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` — OK; positive/negative `Acceptance criteria` scenarios; shared G8 gates as applicable. Preserve actual commands, results and source revision.
- Risks / approval gates: medium; risk of loss or false currency of documents. Separate implementation request; target apply, sensitive backups and activation have separate boundaries. Rollback own slice only; full T07/T08 recovery contract applies to compaction.
- Complexity: medium
- Estimated execution time: not_estimated; assess after focused source preflight, no invented timelines.
- Agents: docs-maintainer — primary slice owner; primary coordinates shared files; independent review only under authorized dispatch, owner accepts T14 outcome.
- Skills: canonical implementation-planner; task-matching repository lifecycle skills; for future Python edits python-design-patterns/python-code-style. Implementation approved; canonical skills and Python guidance applied.
- Output artifacts: Changed owning files from Scope; evidence in proposed G8 execution report/results and compact RUNLOG pointer; no duplicate ledger.
- Next step: Owner accepted T14 / G8 closed; research matrix retained unsplit by owner decision.

#### Completion Report

- status: implemented
- what was done: Mirror/reference/offline-bundle checks and G6/G7 navigation repairs without changing outcomes.
- files touched / work locations: Owning implementation/test/workflow paths mapped per card in research/product-agent-os-g8-execution-report.md; source hashes in docs/superpowers/specs/paos-aud-g8-control-plane-results.json.
- technical value delivered: Local contract implemented: Mirror/reference/offline-bundle checks and G6/G7 navigation repairs without changing outcomes.
- product value delivered: Current compact documents, explicit readiness and recoverable history in verified synthetic scenarios.
- actual implementation date and time: 10-11-2026 17:41
- verification evidence: Focused verification and synthetic comparisons recorded in G8 execution report/results; final integrated receipts belong to that report.
- residual risks: Synthetic/local evidence only; T14 owner accepted; fresh-session activation separate; research matrix split deferred by owner; docs/planning detailed matrices remain intact; actual M1 integration owned by M1.
- follow-up: T14 owner accepted; research matrix remains unsplit by owner decision; separate fresh-session activation.

### Task `PAOS-AUD-G8-T12`

- ID: `PAOS-AUD-G8-T12`
- Task: **Task name:** Maintenance lifecycle without false blocks.
- Short description: **Task description:** Integrate size/freshness checks into applicable transitions with safe read-only route.
- Technical value: **Technical value (for the project):** Maintains compactness after each subsequent change.
- Product value: **Product value (for the user):** Project can be researched after a closed task without bypassing guards.
- Scope: **Affected files:** system_file_hygiene.py; .codex/workflows/control-plane-sync.md; .codex/hooks/pre_tool_use_policy.py; assets/templates/workflows/control-plane-sync.md; assets/templates/hooks/. Bare module names refer to `plugins/product-agent-os/scripts/product_agent_os/`, `scripts/` and `assets/` to plugin root; other paths workspace-relative. Corresponding existing test: `tests/product_agent_os/test_lifecycle_hooks.py`. Refine directory scope to file manifest before edits.
- Acceptance criteria: **Acceptance criteria:** 1) Changed-document check recommends maintenance on applicable limit breach; docs/planning detailed matrices exempt from default size trigger; repeated growth detected. 2) Read-only commands after terminal marker allowed without new mutation grant. 3) New mutation requires proper own-session scope marker; foreign/mixed markers and unknown mutating wrappers remain fail-closed. 4) Approval/path/secret protections not weakened. 5) Maintenance does not become mandatory full packet for every question. 6) Automation/manual promotion boundaries retained; cache/host activation outside slice.
- Group: PAOS-AUD-G8
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 10.11.2026 to complete G8; separate owner acceptance and adoption gates retained.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 17:41
- Depends on: PAOS-AUD-G8-T06; PAOS-AUD-G8-T07
- Blocks: PAOS-AUD-G8-T13
- Source: G8-S03, G8-S04; traceability and observation boundaries in group section.
- Non-goals: Changes to three external projects, fresh-session activation, automatic history deletion, new competing status system, Git/provider/publication actions.
- Expected result: Integrate size/freshness checks into applicable transitions with safe read-only route. Outcome bounded by verified local contracts; authorization and owner acceptance not inferred from file presence.
- Verification gates: `python -B -m unittest tests.product_agent_os.test_lifecycle_hooks -v` — OK; positive/negative `Acceptance criteria` scenarios; shared G8 gates as applicable. Preserve actual commands, results and source revision.
- Risks / approval gates: high; risk of loss or false currency of documents. Separate implementation request; target apply, sensitive backups and activation have separate boundaries. Rollback own slice only; full T07/T08 recovery contract applies to compaction.
- Complexity: high
- Estimated execution time: not_estimated; assess after focused source preflight, no invented timelines.
- Agents: plugin-runtime-builder — primary slice owner; primary coordinates shared files; independent review only under authorized dispatch, owner accepts T14 outcome.
- Skills: canonical implementation-planner; task-matching repository lifecycle skills; for future Python edits python-design-patterns/python-code-style. Implementation approved; canonical skills and Python guidance applied.
- Output artifacts: Changed owning files from Scope; evidence in proposed G8 execution report/results and compact RUNLOG pointer; no duplicate ledger.
- Next step: Owner accepted T14 / G8 closed; research matrix retained unsplit by owner decision.

#### Completion Report

- status: implemented
- what was done: Active/package 40k workflows, repeated-growth checks and terminal read-only guard regressions.
- files touched / work locations: Owning implementation/test/workflow paths mapped per card in research/product-agent-os-g8-execution-report.md; source hashes in docs/superpowers/specs/paos-aud-g8-control-plane-results.json.
- technical value delivered: Local contract implemented: Active/package 40k workflows, repeated-growth checks and terminal read-only guard regressions.
- product value delivered: Current compact documents, explicit readiness and recoverable history in verified synthetic scenarios.
- actual implementation date and time: 10-11-2026 17:41
- verification evidence: Focused verification and synthetic comparisons recorded in G8 execution report/results; final integrated receipts belong to that report.
- residual risks: Synthetic/local evidence only; T14 owner accepted; fresh-session activation separate; research matrix split deferred by owner; docs/planning detailed matrices remain intact; actual M1 integration owned by M1.
- follow-up: T14 owner accepted; research matrix remains unsplit by owner decision; separate fresh-session activation.

### Task `PAOS-AUD-G8-T13`

- ID: `PAOS-AUD-G8-T13`
- Task: **Task name:** End-to-end synthetic pilots and negative scenarios.
- Short description: **Task description:** Verify full lifecycle on three analogues of researched projects.
- Technical value: **Technical value (for the project):** Demonstrates integration of generation, compaction and continuation.
- Product value: **Product value (for the user):** Comparable evidence of benefit and preservation.
- Scope: **Affected files:** tests/fixtures/product_agent_os/g8-control-plane/ (proposed new); tests/product_agent_os/test_g8_control_plane.py (proposed new); docs/superpowers/specs/paos-aud-g8-control-plane-results.json (proposed new). Bare module names refer to `plugins/product-agent-os/scripts/product_agent_os/`, `scripts/` and `assets/` to plugin root; other paths workspace-relative. Corresponding existing test: `tests/product_agent_os/test_g8_control_plane.py` (proposed new). Refine directory scope to file manifest before edits.
- Acceptance criteria: **Acceptance criteria:** 1) Three synthetic profiles: Trade-like large history/strict budget, myPartners-like mirrors/AI gates, site-like duplicates/cross-repo refs. 2) Frozen cases: initial render → fill → regeneration → new task → overflow → proposal → approved local apply → resume. 3) Negative controls: loss of gate/ID/evidence, stale hash, broken link, interrupted write, conflicting writer, duplicate marker. 4) Byte-for-byte recovery and preservation of critical facts checked by oracle independent of summary. 5) Baseline/treatment use identical inputs; failed cases and denominators retained. 6) Synthetic local workspace only, no writes to real three projects; HOST-01 not prerequisite and activation not proven.
- Group: PAOS-AUD-G8
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 10.11.2026 to complete G8; separate owner acceptance and adoption gates retained.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 17:41
- Depends on: PAOS-AUD-G8-T05; PAOS-AUD-G8-T08; PAOS-AUD-G8-T10; PAOS-AUD-G8-T11; PAOS-AUD-G8-T12
- Blocks: PAOS-AUD-G8-T14
- Source: G8-S01–G8-S08; traceability and observation boundaries in group section.
- Non-goals: Changes to three external projects, fresh-session activation, automatic history deletion, new competing status system, Git/provider/publication actions.
- Expected result: Verify full lifecycle on three analogues of researched projects. Outcome bounded by verified local contracts; authorization and owner acceptance not inferred from file presence.
- Verification gates: `python -B -m unittest tests.product_agent_os.test_g8_control_plane -v` — OK; positive/negative `Acceptance criteria` scenarios; shared G8 gates as applicable. Preserve actual commands, results and source revision.
- Risks / approval gates: high; risk of loss or false currency of documents. Separate implementation request; target apply, sensitive backups and activation have separate boundaries. Rollback own slice only; full T07/T08 recovery contract applies to compaction.
- Complexity: high
- Estimated execution time: not_estimated; assess after focused source preflight, no invented timelines.
- Agents: tester — primary slice owner; primary coordinates shared files; independent review only under authorized dispatch, owner accepts T14 outcome.
- Skills: canonical implementation-planner; task-matching repository lifecycle skills; for future Python edits python-design-patterns/python-code-style. Implementation approved; canonical skills and Python guidance applied.
- Output artifacts: Changed owning files from Scope; evidence in proposed G8 execution report/results and compact RUNLOG pointer; no duplicate ledger.
- Next step: Owner accepted T14 / G8 closed; research matrix retained unsplit by owner decision.

#### Completion Report

- status: implemented
- what was done: Three frozen synthetic profiles, controlled pre-G8/G8 comparison, source-bound JSON and negative controls.
- files touched / work locations: Owning implementation/test/workflow paths mapped per card in research/product-agent-os-g8-execution-report.md; source hashes in docs/superpowers/specs/paos-aud-g8-control-plane-results.json.
- technical value delivered: Local contract implemented: Three frozen synthetic profiles, controlled pre-G8/G8 comparison, source-bound JSON and negative controls.
- product value delivered: Current compact documents, explicit readiness and recoverable history in verified synthetic scenarios.
- actual implementation date and time: 10-11-2026 17:41
- verification evidence: Focused verification and synthetic comparisons recorded in G8 execution report/results; final integrated receipts belong to that report.
- residual risks: Synthetic/local evidence only; T14 owner accepted; fresh-session activation separate; research matrix split deferred by owner; docs/planning detailed matrices remain intact; actual M1 integration owned by M1.
- follow-up: T14 owner accepted; research matrix remains unsplit by owner decision; separate fresh-session activation.

### Task `PAOS-AUD-G8-T14`

- ID: `PAOS-AUD-G8-T14`
- Task: **Task name:** Final G8 integration, comparison and acceptance.
- Short description: **Task description:** Align active/package/docs and present results to owner.
- Technical value: **Technical value (for the project):** Closes demonstrable maintainability contract without false promotion.
- Product value: **Product value (for the user):** Owner accepts concrete improvements and remaining limits.
- Scope: **Affected files:** docs/product-agent-os/technical.md; docs/product-agent-os/technical.en.md; docs/product-agent-os/architecture.md; docs/product-agent-os/architecture.en.md; docs/sources/registry.md; docs/sources/registry.en.md; research/product-agent-os-g8-execution-report.md (proposed new); root control-plane pointers. Bare module names refer to `plugins/product-agent-os/scripts/product_agent_os/`, `scripts/` and `assets/` to plugin root; other paths workspace-relative. Corresponding existing test: `tests/product_agent_os/test_product_agent_os_docs.py`. Refine directory scope to file manifest before edits.
- Acceptance criteria: **Acceptance criteria:** 1) All T01–T13 have evidence within acceptance; blocked/partial not hidden by aggregate score. 2) Comparison shows before/after UTF-8 bytes, completeness of facts, navigation/link correctness, recovery and effort of next change; token/cost savings only if measured. 3) Active/package templates/workflows and RU/EN claims aligned; G1–G7 evidence preserved. 4) Owner explicitly accepts results/accepted gaps; absent decision status needs_user_acceptance. 5) Fresh-session activation separate, T34 no-go and G6 acceptance not closed by G8. 6) No automatic publication, target adoption or broad production claim.
- Group: PAOS-AUD-G8
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner request 10.11.2026 to complete G8; separate owner acceptance and adoption gates retained.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 17:41
- Depends on: PAOS-AUD-G8-T13
- Blocks: G8 acceptance; does not close separate HOST/production gates.
- Source: G8-S01–G8-S08; traceability and observation boundaries in group section.
- Non-goals: Changes to three external projects, fresh-session activation, automatic history deletion, new competing status system, Git/provider/publication actions.
- Expected result: Align active/package/docs and present results to owner. Outcome bounded by verified local contracts; authorization and owner acceptance not inferred from file presence.
- Verification gates: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` — OK; positive/negative `Acceptance criteria` scenarios; shared G8 gates as applicable. Preserve actual commands, results and source revision.
- Risks / approval gates: high; risk of loss or false currency of documents. Separate implementation request; target apply, sensitive backups and activation have separate boundaries. Rollback own slice only; full T07/T08 recovery contract applies to compaction.
- Complexity: high
- Estimated execution time: not_estimated; assess after focused source preflight, no invented timelines.
- Agents: reviewer — primary slice owner; primary coordinates shared files; independent review only under authorized dispatch, owner accepts T14 outcome.
- Skills: canonical implementation-planner; task-matching repository lifecycle skills; for future Python edits python-design-patterns/python-code-style. Implementation approved; canonical skills and Python guidance applied.
- Output artifacts: Changed owning files from Scope; evidence in proposed G8 execution report/results and compact RUNLOG pointer; no duplicate ledger.
- Next step: Owner accepted T14 / G8 closed; research matrix retained unsplit by owner decision.

#### Completion Report

- status: implemented
- what was done: Final comparison/report, source ownership, docs/control-plane sync; owner decision: accepted; owner explicitly accepted T14 and G8 closure in current request.
- files touched / work locations: Owning implementation/test/workflow paths mapped per card in research/product-agent-os-g8-execution-report.md; source hashes in docs/superpowers/specs/paos-aud-g8-control-plane-results.json.
- technical value delivered: Local contract implemented: Final comparison/report, source ownership, docs/control-plane sync; owner decision: accepted; owner explicitly accepted T14 and G8 closure in current request.
- product value delivered: Current compact documents, explicit readiness and recoverable history in verified synthetic scenarios.
- actual implementation date and time: 10-11-2026 17:41
- verification evidence: Focused verification and synthetic comparisons recorded in G8 execution report/results; final integrated receipts belong to that report.
- residual risks: Synthetic/local evidence only; T14 owner accepted; fresh-session activation separate; research matrix split deferred by owner; docs/planning detailed matrices remain intact; actual M1 integration owned by M1.
- follow-up: T14 owner accepted; research matrix remains unsplit by owner decision; separate fresh-session activation.


## PAOS-AUD-G9

**Unified project formation mechanism**

Source status: project-local implementation and verification. T01–T09 implemented_locally_verified; T10 owner accepted; T11–T16 implemented_locally_verified; T17 owner accepted; G9 closed; fresh-session activation separately open.

Goal: one route from project analysis → selecting required files → agreeing on the docs/ and .codex/ structure → preview → staging → authorized application → result verification. Reuse the implemented G8 mechanisms; do not create a second status system or a parallel generator.

### G9 sources and boundaries

- G9-S01: [catalog and scoped selection](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/templates.py), [generator](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/infrastructure.py). The historical baseline without task_context proposed the entire catalog. Missing context now blocks generation; the full catalog is available through explicit legacy mode.
- G9-S02: [content/readiness contracts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/control_plane_documents.py), [navigation](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/document_navigation.py), [stage manifest](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/stage_manifest.py), [merge](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py).
- G9-S03: [project formation workflow](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/assets/templates/workflows/project-formation.md); [G8 results and limitations](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g8-execution-report.md). The workflow routes to the shared planner; existing documents are preserved, updates remain companion proposals.
- G9-S04: [Web M1 owning plan](product-agent-os-web-task-manager-plan-2026-11-09.md) and [PLAN](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/PLAN.md): respect source ownership during freeze/cutover; completing all of M1 is not a prerequisite for local G9 slices. Do not substitute synthetic authority checks for M1 SQL/runtime integration.

Boundaries: G8-T14 explicitly accepted by the owner; G8 closed. G9 closed after explicit acceptance of T10/T17. HOST/fresh-session activation, the T34 no-go and G6 acceptance remain separate. The research matrix remains a single file. The limit for applicable control-plane/navigation documents is 40 000 UTF-8 bytes, warning at 32 000; explicit per-file limits take precedence. Detailed docs/planning/ matrices remain intact and are exempt only from the default size trigger; content/link/security checks remain.

Sequence: T01 → T02 → T03 → T04 → T05 → T06 → T07 → T08 → T09 → T10. Full dependencies are specified in the cards; transitive Blocks through T09 lead to T10. The listed Agents are owners of future slices, not authorization to dispatch. Edit shared files sequentially; establish the exact file manifest and existing tests before edits. Bare module paths refer to plugins/product-agent-os/scripts/product_agent_os/; scripts/, assets/ and skills/ refer to the plugin root. Determine new module names after source preflight; do not create empty implementations from the plan.


### G9 extension: focused maintenance after every task

Source status: owner-authorized implementation, 10.11.2026; T11–T16 implemented_locally_verified; T17 owner accepted; G9 closed. The owner accepted T10 and authorized full implementation of the extension with checks. T01–T09 and evidence of the original package are preserved; T10 implemented / owner accepted. T17 owns final acceptance of the extended group without replacing the separate T10 decision.

Historical baseline: G9-S05–G9-S08 below describe gaps before T11–T17 implementation. The accepted result and actual evidence are in the G9 execution report.

- G9-S05: [control-plane sync](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/.codex/workflows/control-plane-sync.md), [task lifecycle](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/.codex/workflows/task-plan-lifecycle.md), [completion implementation](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/task_plan_lifecycle.py). A checklist exists; the completion helper alone does not check docs impact or update the PLAN revision.
- G9-S06: [formation impact](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_formation.py), [navigation and duplicate_blocks](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/document_navigation.py), [document checker](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/check_documents.py). manual_updates/source_changed are not section-level impact; duplicate_blocks currently operates within a file; G8/G9 aliases differ.
- G9-S07: [hygiene policy](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/system_file_hygiene.py), [Stop reminder](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/.codex/hooks/stop_runlog_reminder.py), [canonical planner](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/skills/implementation-planner/SKILL.md). Periodic schedule not_created; hooks advisory; the RUNLOG evidence rule needs alignment with compact handoff.
- G9-S08: [status projection](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/status_snapshot.py) and [G9 current evidence](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g9-execution-report.md). The source revision guard remains; prior G9 passes do not prove the extension that had not yet been implemented.

Principle: assess documentation impact after every task; write only when information owned by the relevant owner changes. One fact has one primary source; other documents contain necessary concise context and a link. The full matrix retains its own cards. Docs impact belongs in the existing task/completion artifact, not a new file for every task. The primary owns overall synchronization; a delegated owner returns only assigned-file impact. New instructions, write routes and validators are implemented locally; the owner accepted the result and limitations.

Extension sequence: T11 → T12 → T13/T14 → T15 → T16 → T17. T13/T14 allow separate planning, but shared document_navigation.py requires sequential edits or explicit coordination; this does not authorize parallel dispatch. Owner decisions for T10 and T17 were received; G9 closed with accepted model/semantic evidence limitations. M1 freeze/SQL ownership, no auto deletion, 40 000 UTF-8 bytes, the docs/planning size exception, research retained unsplit and separate fresh-session activation remain.

Original planning-stage verification contract: risk-based RED/GREEN for new testable contracts, checks at the lowest reliable layer and existing tests; full integration according to TEST.md. Do not introduce file/test quotas, run all checks after every sentence or claim cost/savings/quality based on file count. The planning addition used docs, matrix, links, dependency/pin consistency and diff checks; actual implementation gates and acceptance are recorded in Completion Reports. Authoring rollback covers only added T11–T17 and related summary/pointer hunks; prior task cards and current implementation are preserved. DDD/FSD/frontend/provider/live benchmarks do not apply to this authoring slice.

### Verification of the G9 planning addition

Authoring scope T11–T17, 10.11.2026: implementation_not_started. `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_status_snapshot -v` — 130 tests / 12.817s, OK, exit 0. `python -B tools/check_docs.py` — OK; `python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md` — ok=true, errors=[]; `git diff --check` — exit 0. Read-only assertions: 65 cards, 58 prior task blocks textually preserved, 7 new planned; dependencies point to earlier tasks; 82 current-state rows, issues=[]; changed local links resolve; root control-plane files below 40 000 bytes; 39 previously modified files outside authoring scope retained their hashes. The first helper comparison included group headings with the cards; parser boundaries were corrected, the rerun passed, and prior cards were not edited. Strict MkDocs not_applicable: nav/config/public docs unchanged. Runtime suites, new pilots and activation were not run; prior G9 results were not presented as T11–T17 evidence. Control-plane sync: REQUIREMENTS/PLAN/RUNLOG updated; TEST/EVALS/AGENTS/prod_test not_applicable. No registry update: no new public implementation/source claims added.

### Shared G9 checks and results

Verification contract: risk-based RED/GREEN and existing focused tests for new behavior; then mandatory TEST.md gates, fixture/transcript eval and compatibility where applicable. For docs/control-plane: python -m unittest tests.product_agent_os.test_product_agent_os_docs -v; python tools/check_docs.py; python plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md; git diff --check. Strict MkDocs is mandatory for navigation/MkDocs/site evidence changes. Retain commands and actual receipts in the owning evidence; do not present this list as executed checks.

G9-T09 results must include source/config/fixture revisions and environment, identical baseline/treatment inputs, failed cases and limitations. Do not call providers or create API keys; do not claim savings or quality solely from fewer files. Target apply requires a specific manifest and authority; rollback preserves unrelated/concurrent work. Actual receipts and failed attempts: [G9 execution report](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-g9-execution-report.md); [comparison JSON](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/superpowers/specs/paos-aud-g9-project-formation-results.json). Do not turn local verification into owner acceptance or activation.

### Task `PAOS-AUD-G9-T01`

- ID: `PAOS-AUD-G9-T01`
- Task: Unified project formation contract.
- Short description: Define the shared input, result, stages and boundaries of the formation mechanism.
- Technical value: Removes divergence between the generator, template selection and workflow.
- Product value: The user gets one understandable process with an explainable result.
- Scope: Existing plugin contracts; infrastructure.py; templates.py; assets/templates/workflows/project-formation.md. Actual file ownership and checks are listed in the Completion Report and G9 execution report; implementation was authorized by the owner.
- Acceptance criteria: 1) Modes for new, existing and repeatedly formed projects are defined. 2) Inputs have provenance; unknown information and contradictions are explicit. 3) The result contains selected and excluded files, selection reasons, dependencies, questions and application boundaries. 4) Plan readiness, staging readiness, application and runtime activation are separate. 5) Reused existing G8 components are documented.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: G9 planning, followed by the owner’s explicit request to implement T01–T10 with checks and present a comparison; G8 accepted, fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 20:11
- Depends on: PAOS-AUD-G8-T01–T04 contracts; check current evidence and G8 state before use.
- Blocks: PAOS-AUD-G9-T02; PAOS-AUD-G9-T03; PAOS-AUD-G9-T06
- Source: G9-S01–G9-S04; owner-approved task list; current source preflight before implementation.
- Non-goals: Application business-logic generation; publication; providers; hook activation; schedules; external target writes without authority; splitting the research matrix; a new status system; closing G8/G6/HOST gates.
- Expected result: A versioned contract in the existing contract layer and an aligned workflow.
- Verification gates: Schema, invalid-input and compatibility checks. Shared G9 gates where applicable; actual commands/results and limitations are in the G9 execution report.
- Risks / approval gates: medium; creating a parallel state source. Local implementation authorized by the owner; target apply/activation/external actions retain separate boundaries; rollback only the owned slice.
- Complexity: medium
- Estimated execution time: not_estimated; estimate after focused source preflight.
- Agents: architect — responsibility role; the primary actually performed the slice and is responsible for reconciling evidence and shared files. No dispatch performed; independent review only within authorized scope.
- Skills: Applicable lifecycle skills from canonical plugins/product-agent-os/skills; python-design-patterns and python-code-style for Python edits. Canonical implementation-planner and Python guidance applied; zero delegation.
- Output artifacts: A versioned contract in the existing contract layer and an aligned workflow. Use existing owners; implementation evidence in the G9 execution report, a short pointer in RUNLOG.
- Next step: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: project_formation_v1 contract: task, domains, canonical paths, facts, control proposals; a unified result with provenance, gaps and boundaries.
- files touched / work locations: project_formation.py; assets/templates/workflows/project-formation.md; full paths and reuse boundaries in research/product-agent-os-g9-execution-report.md.
- technical value delivered: project_formation_v1 contract: task, domains, canonical paths, facts, control proposals; a unified result with provenance, gaps and boundaries.
- product value delivered: A coherent route and explainable result instead of separate generators.
- actual implementation date and time: 10-11-2026 20:11
- verification evidence: Ran 1435 tests in 803.716s, OK (skipped=1); fixtures 91/91; transcripts 26/26; compatibility compatible; focused/crash/pilots and docs gates — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic evidence; Initial G9/T10 owner accepted; T17 extension accepted; G9 closed; existing files require reviewed companion adoption; real M1 SQL/host activation not proven; no model/token/cost superiority.
- follow-up: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

### Task `PAOS-AUD-G9-T02`

- ID: `PAOS-AUD-G9-T02`
- Task: Project analysis and normalization of input facts.
- Short description: Collect facts about the stack, structure, documentation, checks and existing Codex settings.
- Technical value: File selection relies on verified information rather than directory names.
- Product value: The system accounts for the specific project structure and shows what information is missing.
- Scope: Existing discovery/audit modules; task_routing.py; the formation input contract. Actual file ownership and checks are listed in the Completion Report and G9 execution report; implementation was authorized by the owner.
- Acceptance criteria: 1) An empty project, an existing application and a monorepo are handled. 2) Existing owners of requirements, plans, architecture, checks and history are identified. 3) A missing document, an empty scaffold, a populated document and an inaccessible source are distinguished. 4) An unknown stack or contradiction does not silently select the full catalog. 5) Analysis does not modify the project or copy secrets or raw private logs into results.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: G9 planning, followed by the owner’s explicit request to implement T01–T10 with checks and present a comparison; G8 accepted, fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 20:11
- Depends on: PAOS-AUD-G9-T01
- Blocks: PAOS-AUD-G9-T03; PAOS-AUD-G9-T04
- Source: G9-S01–G9-S04; owner-approved task list; current source preflight before implementation.
- Non-goals: Application business-logic generation; publication; providers; hook activation; schedules; external target writes without authority; splitting the research matrix; a new status system; closing G8/G6/HOST gates.
- Expected result: Normalized facts and gaps in the existing analysis result.
- Verification gates: Fixtures for an empty project, an application, a monorepo and incomplete sources; verify that source files remain unchanged. Shared G9 gates where applicable; actual commands/results and limitations are in the G9 execution report.
- Risks / approval gates: high; incorrect conclusions and data disclosure. Local implementation authorized by the owner; target apply/activation/external actions retain separate boundaries; rollback only the owned slice.
- Complexity: high
- Estimated execution time: not_estimated; estimate after focused source preflight.
- Agents: plugin-runtime-builder — responsibility role; the primary actually performed the slice and is responsible for reconciling evidence and shared files. No dispatch performed; independent review only within authorized scope.
- Skills: Applicable lifecycle skills from canonical plugins/product-agent-os/skills; python-design-patterns and python-code-style for Python edits. Canonical implementation-planner and Python guidance applied; zero delegation.
- Output artifacts: Normalized facts and gaps in the existing analysis result. Use existing owners; implementation evidence in the G9 execution report, a short pointer in RUNLOG.
- Next step: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Bounded read-only inventory and existing discovery/routing: digest, document states, detected stack, questions and ambiguous owners.
- files touched / work locations: project_formation.py: source_inventory, formation_plan; full paths and reuse boundaries in research/product-agent-os-g9-execution-report.md.
- technical value delivered: Bounded read-only inventory and existing discovery/routing: digest, document states, detected stack, questions and ambiguous owners.
- product value delivered: Input information and unknown data are visible before staging.
- actual implementation date and time: 10-11-2026 20:11
- verification evidence: Ran 1435 tests in 803.716s, OK (skipped=1); fixtures 91/91; transcripts 26/26; compatibility compatible; focused/crash/pilots and docs gates — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic evidence; Initial G9/T10 owner accepted; T17 extension accepted; G9 closed; existing files require reviewed companion adoption; real M1 SQL/host activation not proven; no model/token/cost superiority.
- follow-up: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

### Task `PAOS-AUD-G9-T03`

- ID: `PAOS-AUD-G9-T03`
- Task: Selection of the minimum sufficient file set.
- Short description: Select documents and infrastructure according to project tasks, risks and facts.
- Technical value: Removes the implicit switch to the full catalog when task_context is absent.
- Product value: The project receives required files without unnecessary instructions and empty templates.
- Scope: templates.py; task_routing.py; the existing assets/templates/ catalog. Actual file ownership and checks are listed in the Completion Report and G9 execution report; implementation was authorized by the owner.
- Acceptance criteria: 1) Every selected file has a purpose, data source and inclusion reason. 2) An exclusion reason is available for omitted applicable options. 3) EVALS.md, agents, hooks, config and specialized documents have separate selection conditions. 4) Dependencies of selected files are resolved or shown as gaps; missing workflows are not presented as available. 5) The full catalog is available only as an explicitly selected compatible mode. 6) Identical input facts and rule versions yield identical selections.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: G9 planning, followed by the owner’s explicit request to implement T01–T10 with checks and present a comparison; G8 accepted, fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 20:11
- Depends on: PAOS-AUD-G9-T01; PAOS-AUD-G9-T02; PAOS-AUD-G8-T02 mechanisms.
- Blocks: PAOS-AUD-G9-T04; PAOS-AUD-G9-T05; PAOS-AUD-G9-T06
- Source: G9-S01–G9-S04; owner-approved task list; current source preflight before implementation.
- Non-goals: Application business-logic generation; publication; providers; hook activation; schedules; external target writes without authority; splitting the research matrix; a new status system; closing G8/G6/HOST gates.
- Expected result: A unified selection plan with explanations and dependencies.
- Verification gates: An expected-selection table for typical and edge cases; legacy-mode regressions. Shared G9 gates where applicable; actual commands/results and limitations are in the G9 execution report.
- Risks / approval gates: high; missing required files or excessive generation. Local implementation authorized by the owner; target apply/activation/external actions retain separate boundaries; rollback only the owned slice.
- Complexity: high
- Estimated execution time: not_estimated; estimate after focused source preflight.
- Agents: plugin-runtime-builder — responsibility role; the primary actually performed the slice and is responsible for reconciling evidence and shared files. No dispatch performed; independent review only within authorized scope.
- Skills: Applicable lifecycle skills from canonical plugins/product-agent-os/skills; python-design-patterns and python-code-style for Python edits. Canonical implementation-planner and Python guidance applied; zero delegation.
- Output artifacts: A unified selection plan with explanations and dependencies. Use existing owners; implementation evidence in the G9 execution report, a short pointer in RUNLOG.
- Next step: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Reused selected_templates; explicit control surfaces, conditional EVALS, dependency closure and an explicit legacy catalog.
- files touched / work locations: project_formation.py; infrastructure.py; compatibility callers/tests; full paths and reuse boundaries in research/product-agent-os-g9-execution-report.md.
- technical value delivered: Reused selected_templates; explicit control surfaces, conditional EVALS, dependency closure and an explicit legacy catalog.
- product value delivered: No implicit full catalog; every additional file has a reason.
- actual implementation date and time: 10-11-2026 20:11
- verification evidence: Ran 1435 tests in 803.716s, OK (skipped=1); fixtures 91/91; transcripts 26/26; compatibility compatible; focused/crash/pilots and docs gates — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic evidence; Initial G9/T10 owner accepted; T17 extension accepted; G9 closed; existing files require reviewed companion adoption; real M1 SQL/host activation not proven; no model/token/cost superiority.
- follow-up: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

### Task `PAOS-AUD-G9-T04`

- ID: `PAOS-AUD-G9-T04`
- Task: Aligned docs/ and .codex/ structure.
- Short description: Define the location of documents, templates and control files in one plan.
- Technical value: Prevents duplicated state, incompatible paths and broken navigation.
- Product value: The user understands where project decisions are stored and how to reach details.
- Scope: Path planning in infrastructure.py; control_plane_documents.py; document_navigation.py; assets/templates/workflows/documentation-system.md. Actual file ownership and checks are listed in the Completion Report and G9 execution report; implementation was authorized by the owner.
- Acceptance criteria: 1) The root control plane, actual documents in docs/ and supporting templates in .codex/ are separate. 2) Existing canonical paths are reused; the new structure does not force renaming. 3) Architecture, decisions, API, data, operations, evidence and archive sections are created only where applicable. 4) Every created document has an owner, navigation entry point and update event. 5) Path collisions are checked, including Windows case handling, forbidden paths and links outside the agreed scope. 6) Detailed docs/planning/ matrices remain intact; active documents are not disguised as archives.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: G9 planning, followed by the owner’s explicit request to implement T01–T10 with checks and present a comparison; G8 accepted, fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 20:11
- Depends on: PAOS-AUD-G9-T02; PAOS-AUD-G9-T03; G8 ownership/navigation contracts.
- Blocks: PAOS-AUD-G9-T05; PAOS-AUD-G9-T06
- Source: G9-S01–G9-S04; owner-approved task list; current source preflight before implementation.
- Non-goals: Application business-logic generation; publication; providers; hook activation; schedules; external target writes without authority; splitting the research matrix; a new status system; closing G8/G6/HOST gates.
- Expected result: An aligned file-tree and link plan.
- Verification gates: Fixtures for alternative structures, monorepos, collisions and navigation links. Shared G9 gates where applicable; actual commands/results and limitations are in the G9 execution report.
- Risks / approval gates: high; competing documents and damaged navigation. Local implementation authorized by the owner; target apply/activation/external actions retain separate boundaries; rollback only the owned slice.
- Complexity: high
- Estimated execution time: not_estimated; estimate after focused source preflight.
- Agents: architect — responsibility role; the primary actually performed the slice and is responsible for reconciling evidence and shared files. No dispatch performed; independent review only within authorized scope.
- Skills: Applicable lifecycle skills from canonical plugins/product-agent-os/skills; python-design-patterns and python-code-style for Python edits. Canonical implementation-planner and Python guidance applied; zero delegation.
- Output artifacts: An aligned file-tree and link plan. Use existing owners; implementation evidence in the G9 execution report, a short pointer in RUNLOG.
- Next step: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Canonical aliases, selected docs domains, navigation index, URL-encoded links, case/path collision checks.
- files touched / work locations: project_formation.py: _owner_path, _document, formation_plan; full paths and reuse boundaries in research/product-agent-os-g9-execution-report.md.
- technical value delivered: Canonical aliases, selected docs domains, navigation index, URL-encoded links, case/path collision checks.
- product value delivered: The existing structure is preserved; new sections are available through the contents.
- actual implementation date and time: 10-11-2026 20:11
- verification evidence: Ran 1435 tests in 803.716s, OK (skipped=1); fixtures 91/91; transcripts 26/26; compatibility compatible; focused/crash/pilots and docs gates — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic evidence; Initial G9/T10 owner accepted; T17 extension accepted; G9 closed; existing files require reviewed companion adoption; real M1 SQL/host activation not proven; no model/token/cost superiority.
- follow-up: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

### Task `PAOS-AUD-G9-T05`

- ID: `PAOS-AUD-G9-T05`
- Task: Populate documents and verify data sufficiency.
- Short description: Generate the content of selected files from confirmed facts and decisions.
- Technical value: Connects generation with G8 readiness contracts.
- Product value: The user receives useful documents with clear gaps.
- Scope: control_plane_documents.py; templates.py; validators.py; relationships between documents. Actual file ownership and checks are listed in the Completion Report and G9 execution report; implementation was authorized by the owner.
- Acceptance criteria: 1) Facts, constraints, IDs and acceptance criteria retain provenance. 2) Unknown decisions are not invented; missing mandatory data is marked. 3) Requirements, plan, checks and handoff align in links and identifiers. 4) Scaffold, draft, reviewed, accepted and stale states are not conflated. 5) Repeated formation preserves user content and identifies conflicting changes. 6) Missing data can be added without recreating the whole project.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: G9 planning, followed by the owner’s explicit request to implement T01–T10 with checks and present a comparison; G8 accepted, fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 20:11
- Depends on: PAOS-AUD-G9-T03; PAOS-AUD-G9-T04; PAOS-AUD-G8-T03–T05.
- Blocks: PAOS-AUD-G9-T06; PAOS-AUD-G9-T08
- Source: G9-S01–G9-S04; owner-approved task list; current source preflight before implementation.
- Non-goals: Application business-logic generation; publication; providers; hook activation; schedules; external target writes without authority; splitting the research matrix; a new status system; closing G8/G6/HOST gates.
- Expected result: Populated document proposals and a gap report.
- Verification gates: Positive and negative scenarios, content preservation, cross-document consistency. Shared G9 gates where applicable; actual commands/results and limitations are in the G9 execution report.
- Risks / approval gates: high; data loss and false readiness. Local implementation authorized by the owner; target apply/activation/external actions retain separate boundaries; rollback only the owned slice.
- Complexity: high
- Estimated execution time: not_estimated; estimate after focused source preflight.
- Agents: plugin-runtime-builder — responsibility role; the primary actually performed the slice and is responsible for reconciling evidence and shared files. No dispatch performed; independent review only within authorized scope.
- Skills: Applicable lifecycle skills from canonical plugins/product-agent-os/skills; python-design-patterns and python-code-style for Python edits. Canonical implementation-planner and Python guidance applied; zero delegation.
- Output artifacts: Populated document proposals and a gap report. Use existing owners; implementation evidence in the G9 execution report, a short pointer in RUNLOG.
- Next step: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Reused G8 scoped_document/readiness; supplied facts remain data with a source; new proposals do not receive acceptance.
- files touched / work locations: infrastructure.py; project_formation.py; existing control_plane_documents.py reused; full paths and reuse boundaries in research/product-agent-os-g9-execution-report.md.
- technical value delivered: Reused G8 scoped_document/readiness; supplied facts remain data with a source; new proposals do not receive acceptance.
- product value delivered: Unknowns are not invented, user data is not overwritten.
- actual implementation date and time: 10-11-2026 20:11
- verification evidence: Ran 1435 tests in 803.716s, OK (skipped=1); fixtures 91/91; transcripts 26/26; compatibility compatible; focused/crash/pilots and docs gates — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic evidence; Initial G9/T10 owner accepted; T17 extension accepted; G9 closed; existing files require reviewed companion adoption; real M1 SQL/host activation not proven; no model/token/cost superiority.
- follow-up: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

### Task `PAOS-AUD-G9-T06`

- ID: `PAOS-AUD-G9-T06`
- Task: Single entry point and migration from old routes.
- Short description: Connect analysis, selection, structure and content generation through one public route.
- Technical value: Eliminates independent implementations of the same rules in different commands.
- Product value: The user does not need to know the internal script sequence.
- Scope: scripts/render_infrastructure.py and affected existing CLI entrypoints; infrastructure.py; canonical lifecycle skills and workflows. Actual file ownership and checks are listed in the Completion Report and G9 execution report; implementation was authorized by the owner.
- Acceptance criteria: 1) A single entry point provides analysis, preview and staging. 2) CLI and workflow use one decision mechanism. 3) Insufficient context yields explicit gaps rather than a hidden full-catalog fallback. 4) Old commands have a verified compatible route or a clear migration message. 5) Preview shows created, preserved, modified and blocked files. 6) Plan formation does not activate hooks, agents or automations.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: G9 planning, followed by the owner’s explicit request to implement T01–T10 with checks and present a comparison; G8 accepted, fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 20:11
- Depends on: PAOS-AUD-G9-T01; PAOS-AUD-G9-T03; PAOS-AUD-G9-T04; PAOS-AUD-G9-T05.
- Blocks: PAOS-AUD-G9-T07; PAOS-AUD-G9-T09
- Source: G9-S01–G9-S04; owner-approved task list; current source preflight before implementation.
- Non-goals: Application business-logic generation; publication; providers; hook activation; schedules; external target writes without authority; splitting the research matrix; a new status system; closing G8/G6/HOST gates.
- Expected result: One public route and a compatibility description.
- Verification gates: CLI integration checks and comparison of results from different entrypoints. Shared G9 gates where applicable; actual commands/results and limitations are in the G9 execution report.
- Risks / approval gates: high; changes to existing user behavior. Local implementation authorized by the owner; target apply/activation/external actions retain separate boundaries; rollback only the owned slice.
- Complexity: high
- Estimated execution time: not_estimated; estimate after focused source preflight.
- Agents: plugin-runtime-builder — responsibility role; the primary actually performed the slice and is responsible for reconciling evidence and shared files. No dispatch performed; independent review only within authorized scope.
- Skills: Applicable lifecycle skills from canonical plugins/product-agent-os/skills; python-design-patterns and python-code-style for Python edits. Canonical implementation-planner and Python guidance applied; zero delegation.
- Output artifacts: One public route and a compatibility description. Use existing owners; implementation evidence in the G9 execution report, a short pointer in RUNLOG.
- Next step: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Unified CLI analyze/preview/stage/merge/rollback; formation and legacy/scoped modes explicitly separated; the workflow points to the shared planner.
- files touched / work locations: scripts/render_infrastructure.py; assets/templates/workflows/project-formation.md; skills/implementation-planner/SKILL.md; full paths and reuse boundaries in research/product-agent-os-g9-execution-report.md.
- technical value delivered: Unified CLI analyze/preview/stage/merge/rollback; formation and legacy/scoped modes explicitly separated; the workflow points to the shared planner.
- product value delivered: One route from analysis to a verifiable change package.
- actual implementation date and time: 10-11-2026 20:11
- verification evidence: Ran 1435 tests in 803.716s, OK (skipped=1); fixtures 91/91; transcripts 26/26; compatibility compatible; focused/crash/pilots and docs gates — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic evidence; Initial G9/T10 owner accepted; T17 extension accepted; G9 closed; existing files require reviewed companion adoption; real M1 SQL/host activation not proven; no model/token/cost superiority.
- follow-up: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

### Task `PAOS-AUD-G9-T07`

- ID: `PAOS-AUD-G9-T07`
- Task: Safe application and repeated formation.
- Short description: Connect the unified formation plan to existing staging, merge and rollback.
- Technical value: Preserves data during initial and repeated application.
- Product value: The user sees a concrete change package and can safely accept it.
- Scope: stage_manifest.py; merge_infrastructure.py; existing authority and rollback checks. Actual file ownership and checks are listed in the Completion Report and G9 execution report; implementation was authorized by the owner.
- Acceptance criteria: 1) Preview and the applied package are bound by a digest and the original file state. 2) A source change after preview stops stale application. 3) Unmarked user files are preserved; proposals are separate. 4) Reapplying an identical package creates no duplicates. 5) Interrupted application has an explicit result and verifiable recovery. 6) Unchanged and unrelated files remain untouched; runtime activation is separate.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: G9 planning, followed by the owner’s explicit request to implement T01–T10 with checks and present a comparison; G8 accepted, fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 20:11
- Depends on: PAOS-AUD-G9-T06; G8 preservation mechanisms.
- Blocks: PAOS-AUD-G9-T08; PAOS-AUD-G9-T09
- Source: G9-S01–G9-S04; owner-approved task list; current source preflight before implementation.
- Non-goals: Application business-logic generation; publication; providers; hook activation; schedules; external target writes without authority; splitting the research matrix; a new status system; closing G8/G6/HOST gates.
- Expected result: A verified formation-plan application route.
- Verification gates: Stale preview, conflicts, repeated application, mid-operation failure and rollback. Shared G9 gates where applicable; actual commands/results and limitations are in the G9 execution report.
- Risks / approval gates: high; data loss; actual target writes require separate authority. Local implementation authorized by the owner; target apply/activation/external actions retain separate boundaries; rollback only the owned slice.
- Complexity: high
- Estimated execution time: not_estimated; estimate after focused source preflight.
- Agents: plugin-runtime-builder — responsibility role; the primary actually performed the slice and is responsible for reconciling evidence and shared files. No dispatch performed; independent review only within authorized scope.
- Skills: Applicable lifecycle skills from canonical plugins/product-agent-os/skills; python-design-patterns and python-code-style for Python edits. Canonical implementation-planner and Python guidance applied; zero delegation.
- Output artifacts: A verified formation-plan application route. Use existing owners; implementation evidence in the G9 execution report, a short pointer in RUNLOG.
- Next step: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Source/stack/target binding, preview digest, preserve-existing merge; write-ahead journal, atomic create, bounded journal retry and crash recovery.
- files touched / work locations: project_formation.py; infrastructure.py; merge_infrastructure.py; full paths and reuse boundaries in research/product-agent-os-g9-execution-report.md.
- technical value delivered: Source/stack/target binding, preview digest, preserve-existing merge; write-ahead journal, atomic create, bounded journal retry and crash recovery.
- product value delivered: Repeated formation and recovery verified without loss of original bytes.
- actual implementation date and time: 10-11-2026 20:11
- verification evidence: Ran 1435 tests in 803.716s, OK (skipped=1); fixtures 91/91; transcripts 26/26; compatibility compatible; focused/crash/pilots and docs gates — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic evidence; Initial G9/T10 owner accepted; T17 extension accepted; G9 closed; existing files require reviewed companion adoption; real M1 SQL/host activation not proven; no model/token/cost superiority.
- follow-up: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

### Task `PAOS-AUD-G9-T08`

- ID: `PAOS-AUD-G9-T08`
- Task: Maintain the generated structure throughout the project lifecycle.
- Short description: Ensure aligned document updates when requirements, stack and work stage change.
- Technical value: Prevents the result becoming stale after the first run.
- Product value: The structure continues to help as the project grows.
- Scope: Control-plane sync workflows; document_navigation.py; control_plane_documents.py; system_file_hygiene.py; existing M1 authority contract (reuse, without independent SQL implementation). Actual file ownership and checks are listed in the Completion Report and G9 execution report; implementation was authorized by the owner.
- Acceptance criteria: 1) Changed input facts show affected documents and update reasons. 2) Accepted documents are not automatically overwritten or reaccepted. 3) Reducing applicable files preserves history, IDs, links and recoverability. 4) A profile change proposes adding or revising documents without automatic deletion. 5) An active M1 freeze or another write owner stops the independent file writer. 6) G9 does not create a competing SQL projection or a new current-status registry.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: G9 planning, followed by the owner’s explicit request to implement T01–T10 with checks and present a comparison; G8 accepted, fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 20:11
- Depends on: PAOS-AUD-G9-T05; PAOS-AUD-G9-T07.
- Blocks: PAOS-AUD-G9-T09
- Source: G9-S01–G9-S04; owner-approved task list; current source preflight before implementation.
- Non-goals: Application business-logic generation; publication; providers; hook activation; schedules; external target writes without authority; splitting the research matrix; a new status system; closing G8/G6/HOST gates.
- Expected result: Update scenarios and handoff between data owners.
- Verification gates: Scope/stack changes, stale receipts, exceeded limits, M1 authority conflicts. Shared G9 gates where applicable; actual commands/results and limitations are in the G9 execution report.
- Risks / approval gates: high; double writes and stale documentation. Local implementation authorized by the owner; target apply/activation/external actions retain separate boundaries; rollback only the owned slice.
- Complexity: high
- Estimated execution time: not_estimated; estimate after focused source preflight.
- Agents: lifecycle-orchestrator — responsibility role; the primary actually performed the slice and is responsible for reconciling evidence and shared files. No dispatch performed; independent review only within authorized scope.
- Skills: Applicable lifecycle skills from canonical plugins/product-agent-os/skills; python-design-patterns and python-code-style for Python edits. Canonical implementation-planner and Python guidance applied; zero delegation.
- Output artifacts: Update scenarios and handoff between data owners. Use existing owners; implementation evidence in the G9 execution report, a short pointer in RUNLOG.
- Next step: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Previous-plan change impact, review-only removal and manual updates; G8 budgets/compaction/authority reused; freeze/SQL conflicts block the writer.
- files touched / work locations: project_formation.py; existing control_plane_compaction.py reused; public workflow/docs; full paths and reuse boundaries in research/product-agent-os-g9-execution-report.md.
- technical value delivered: Previous-plan change impact, review-only removal and manual updates; G8 budgets/compaction/authority reused; freeze/SQL conflicts block the writer.
- product value delivered: Project growth does not imply automatic deletion or reacceptance of documents.
- actual implementation date and time: 10-11-2026 20:11
- verification evidence: Ran 1435 tests in 803.716s, OK (skipped=1); fixtures 91/91; transcripts 26/26; compatibility compatible; focused/crash/pilots and docs gates — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic evidence; Initial G9/T10 owner accepted; T17 extension accepted; G9 closed; existing files require reviewed companion adoption; real M1 SQL/host activation not proven; no model/token/cost superiority.
- follow-up: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

### Task `PAOS-AUD-G9-T09`

- ID: `PAOS-AUD-G9-T09`
- Task: End-to-end pilots and comparison with the current mechanism.
- Short description: Verify the entire route and compare it with a fixed baseline.
- Technical value: Reveals errors between stages that individual tests cannot expose.
- Product value: Shows which problems of new and existing projects are actually solved.
- Scope: Existing tests/product_agent_os/ and tests/fixtures/product_agent_os/; a separate G9 evidence package without copying private projects. Actual file ownership and checks are listed in the Completion Report and G9 execution report; implementation was authorized by the owner.
- Acceptance criteria: 1) An empty project, an existing documented project and a complex project/monorepo are covered. 2) Ordinary and AI profiles, incomplete context, conflicts and repeated formation are verified. 3) Baseline and the new mechanism receive identical inputs. 4) Comparison covers required completeness, unnecessary files, resolved dependencies, link correctness, preservation and the result of the next change. 5) Failures and partial results are retained; an aggregate score does not hide a mandatory failure. 6) File count is not a standalone quality metric; time and token savings are claimed only when measured.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: G9 planning, followed by the owner’s explicit request to implement T01–T10 with checks and present a comparison; G8 accepted, fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 20:11
- Depends on: PAOS-AUD-G9-T06; PAOS-AUD-G9-T07; PAOS-AUD-G9-T08.
- Blocks: PAOS-AUD-G9-T10
- Source: G9-S01–G9-S04; owner-approved task list; current source preflight before implementation.
- Non-goals: Application business-logic generation; publication; providers; hook activation; schedules; external target writes without authority; splitting the research matrix; a new status system; closing G8/G6/HOST gates.
- Expected result: Results in docs/superpowers/specs/paos-aud-g9-project-formation-results.json and research/product-agent-os-g9-execution-report.md; contain actual results.
- Verification gates: Focused tests, end-to-end fixtures and mandatory shared TEST.md gates for affected behavior. Shared G9 gates where applicable; actual commands/results and limitations are in the G9 execution report.
- Risks / approval gates: medium; overstated conclusions from synthetic pilots; external projects read-only. Local implementation authorized by the owner; target apply/activation/external actions retain separate boundaries; rollback only the owned slice.
- Complexity: high
- Estimated execution time: not_estimated; estimate after focused source preflight.
- Agents: tester — responsibility role; the primary actually performed the slice and is responsible for reconciling evidence and shared files. No dispatch performed; independent review only within authorized scope.
- Skills: Applicable lifecycle skills from canonical plugins/product-agent-os/skills; python-design-patterns and python-code-style for Python edits. Canonical implementation-planner and Python guidance applied; zero delegation.
- Output artifacts: Results in docs/superpowers/specs/paos-aud-g9-project-formation-results.json and research/product-agent-os-g9-execution-report.md; contain actual results. Use existing owners; implementation evidence in the G9 execution report, a short pointer in RUNLOG.
- Next step: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Three end-to-end synthetic pilots with a frozen baseline; preview/stage/apply/repeat/next change/rollback, original and proposed navigation.
- files touched / work locations: tests/product_agent_os/test_project_formation.py; tests/fixtures/product_agent_os/g9-project-formation/cases.json; docs/superpowers/specs/paos-aud-g9-project-formation-results.json; full paths and reuse boundaries in research/product-agent-os-g9-execution-report.md.
- technical value delivered: Three end-to-end synthetic pilots with a frozen baseline; preview/stage/apply/repeat/next change/rollback, original and proposed navigation.
- product value delivered: Comparison shows concrete improvements and retains limitations.
- actual implementation date and time: 10-11-2026 20:11
- verification evidence: Ran 1435 tests in 803.716s, OK (skipped=1); fixtures 91/91; transcripts 26/26; compatibility compatible; focused/crash/pilots and docs gates — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic evidence; Initial G9/T10 owner accepted; T17 extension accepted; G9 closed; existing files require reviewed companion adoption; real M1 SQL/host activation not proven; no model/token/cost superiority.
- follow-up: G9 closed with owner acceptance of T10/T17; fresh-session activation separate.

### Task `PAOS-AUD-G9-T10`

- ID: `PAOS-AUD-G9-T10`
- Task: Documentation, final reconciliation and acceptance.
- Short description: Align implementation, public instructions and comparison results.
- Technical value: Establishes a unified contract and verifiable limitations.
- Product value: The user understands what the system will generate and which decisions remain theirs.
- Scope: docs/product-agent-os/technical.md and technical.en.md; architecture.md and architecture.en.md; docs/sources/registry.md and registry.en.md; workflows; root control-plane pointers; G9 report. Actual file ownership and checks are listed in the Completion Report and G9 execution report; implementation was authorized by the owner.
- Acceptance criteria: 1) All tasks have relevant evidence; unfinished tasks remain explicitly open. 2) Documentation shows compact and extended modes, actual selection conditions and tree examples. 3) Active/package workflows and public descriptions align. 4) Documentation, matrix, link checks and applicable runtime gates pass; strict MkDocs runs for affected navigation. 5) The owner receives the comparison and explicitly accepts the result or specific gaps. 6) needs_user_acceptance remains until the owner decision; fresh-session activation is separate.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: G9 planning, followed by the owner’s explicit request to implement T01–T10 with checks and present a comparison; G8 accepted, fresh-session activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 20:11
- Depends on: PAOS-AUD-G9-T01–T09; explicit resolution of PAOS-AUD-G8-T14 acceptance state (owner decision, do not assume acceptance).
- Blocks: Closure of PAOS-AUD-G9; does not close separate activation/production gates.
- Source: G9-S01–G9-S04; owner-approved task list; current source preflight before implementation.
- Non-goals: Application business-logic generation; publication; providers; hook activation; schedules; external target writes without authority; splitting the research matrix; a new status system; closing G8/G6/HOST gates.
- Expected result: Final G9 acceptance package and a concise RUNLOG handoff.
- Verification gates: Reconcile criteria of each card, final review and owner decision; docs/matrix/links and applicable runtime gates; strict MkDocs for affected navigation. Shared G9 gates where applicable; actual commands/results and limitations are in the G9 execution report.
- Risks / approval gates: high; premature group closure. Local implementation authorized by the owner; target apply/activation/external actions retain separate boundaries; rollback only the owned slice.
- Complexity: medium
- Estimated execution time: not_estimated; estimate after focused source preflight.
- Agents: reviewer — responsibility role; the primary actually performed the slice and is responsible for reconciling evidence and shared files. No dispatch performed; independent review only within authorized scope.
- Skills: Applicable lifecycle skills from canonical plugins/product-agent-os/skills; python-design-patterns and python-code-style for Python edits. Canonical implementation-planner and Python guidance applied; zero delegation.
- Output artifacts: Final G9 acceptance package and a concise RUNLOG handoff. Use existing owners; implementation evidence in the G9 execution report, a short pointer in RUNLOG.
- Next step: T10/T17 accepted; G9 closed. Fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Owner accepted 10.11.2026; RU/EN docs, registry, packaged workflow, canonical skill and control plane synchronized; the final package is handed to the owner.
- files touched / work locations: docs/product-agent-os/project-formation.md/.en.md; technical.md/.en.md; architecture.md/.en.md; cli-reference.md/.en.md; docs/runtime/worktrees-hooks-rules.md/.en.md; docs/sources/registry.md/.en.md; root control-plane; G9 report; full paths and reuse boundaries in research/product-agent-os-g9-execution-report.md.
- technical value delivered: RU/EN docs, registry, packaged workflow, canonical skill and control plane synchronized; the final package is handed to the owner.
- product value delivered: The owner receives comparison results for explicit acceptance; owner decision accepted 10.11.2026.
- actual implementation date and time: 10-11-2026 20:11
- verification evidence: Ran 1435 tests in 803.716s, OK (skipped=1); fixtures 91/91; transcripts 26/26; compatibility compatible; focused/crash/pilots and docs gates — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic evidence; Initial G9/T10 owner accepted; T17 extension accepted; G9 closed; existing files require reviewed companion adoption; real M1 SQL/host activation not proven; no model/token/cost superiority.
- follow-up: T10/T17 accepted; G9 closed. Fresh-session activation separate.

### Task `PAOS-AUD-G9-T11`

- ID: `PAOS-AUD-G9-T11`
- Task: **Task name:** Unified documentation ownership and synchronization-result contract.
- Short description: **Task description:** Establish one primary source for each changed fact and compact docs impact in the existing task card.
- Technical value: **Technical value (for the project):** Eliminates ownership disagreement between formation, navigation and task completion without a new status registry.
- Product value: **Product value (for the user):** After each task it is clear what to update, where truth is stored and why other documents remain unchanged.
- Scope: **Affected files:** control_plane_documents.py; document_navigation.py; project_formation.py; task_plan_lifecycle.py; assets/templates/artifact-templates/task-matrix-plan.md; tests/product_agent_os/test_task_plan_lifecycle.py; tests/product_agent_os/test_document_navigation.py. Bare module paths refer to plugins/product-agent-os/scripts/product_agent_os/, scripts/assets paths to plugin root; root/project paths are explicit. Before implementation verify actual ownership and existing helpers/tests; do not create a new writer/state registry without demonstrated need.
- Acceptance criteria: **Acceptance criteria:** 1) Define canonical owner, aliases, section/anchor, update trigger and permitted summaries/mirrors; unknown or conflicting owner explicitly blocks dependent update. 2) Existing card/Completion Report contains changed fact, task ID, source refs, path/section, updated/no_change_needed/handoff_required decision, reason and evidence/revision; a separate file per task is not mandatory. 3) Impact assessment is mandatory after every completed task; write a document only when its information changes. 4) Contract distinguishes technical implementation, docs sync and owner acceptance. 5) Old cards and historical receipts remain readable; the new requirement applies to the new route, not retroactively to all earlier tasks. 6) Core, docs and M1 authority have one agreed owner; no new SQL/file status system.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested analysis and adding G9 tasks for targeted documentation updates after each task without duplication; planning only at the time.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 21:17
- Depends on: PAOS-AUD-G9-T04; PAOS-AUD-G9-T08; reusable PAOS-AUD-G8-T01–T05.
- Blocks: PAOS-AUD-G9-T12; PAOS-AUD-G9-T14; PAOS-AUD-G9-T16
- Source: G9-S05–G9-S08; current source-backed analysis and owner request; implemented G8/G9 mechanisms are a reuse baseline, not evidence of new capabilities.
- Non-goals: Implementation during current authoring; mass documentation rewriting; new status registry; automatic semantic deletion; provider calls; cache/host/hooks/schedules activation; real-target/Git/publication actions; research matrix split; closing G6/T34/HOST or M1 SQL integration.
- Expected result: Docs impact contract and shared ownership model in existing layers; compatibility fixtures.
- Verification gates: Focused test_task_plan_lifecycle and test_document_navigation: valid/invalid contract, ambiguous owner and legacy rows; existing task-matrix validator must remain compatible. Actual implementation/check receipts are in the G9 execution report; T17 owner acceptance obtained.
- Risks / approval gates: medium; knowledge loss, false freshness or duplicated authority. Local implementation authorized, performed and owner-accepted; specific target writes/activation/external actions retain their boundaries. Rollback only the owning slice, checking concurrent changes and preserving history.
- Complexity: medium
- Estimated execution time: not_estimated; refine through focused source preflight without invented deadlines.
- Agents: architect — proposed responsibility role; primary owns overall synchronization and evidence. No dispatch performed; modify shared paths sequentially or under a separate ownership agreement.
- Skills: canonical implementation-planner for decomposition; only task-matching lifecycle skills used during implementation; Python guidance for Python changes. This field does not launch skills, agents or hooks.
- Output artifacts: Docs impact contract and shared ownership model in existing layers; compatibility fixtures. Detailed actual execution receipts belong in the existing G9 execution report/results; concise handoff in RUNLOG; no per-command/per-task report proliferation.
- Next step: T17 acceptance obtained; G9 closed with accepted limitations. Fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Impact contract: fact/source/revision, canonical owner/section, decision/reason; aliases reused; receipt in existing card.
- files touched / work locations: documentation_sync.py; document_navigation.py; project_formation.py; task-matrix templates
- technical value delivered: Impact contract: fact/source/revision, canonical owner/section, decision/reason; aliases reused; receipt in existing card.
- product value delivered: After the task the single source and reason for a write or no write are clear.
- actual implementation date and time: 10-11-2026 21:17
- verification evidence: Current run: full 1448 tests / 504.318s, OK (skipped=1); final affected/docs 164 tests / 22.975s, OK; fixtures 91/91, transcripts 26/26, compatibility compatible, strict MkDocs preview 11.81s. Exact provenance/deltas — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic/source review only; semantic completeness and model behavior not proven; T17 owner accepted; model-behavior limits accepted; fresh-session activation and real M1 SQL adapter separate. Exact section changes require applicable authority; no new writer/status registry.
- follow-up: Explicit T17 acceptance obtained; G9 closed. Model behavior was not tested; the limitation was accepted. Fresh-session activation separate.

### Task `PAOS-AUD-G9-T12`

- ID: `PAOS-AUD-G9-T12`
- Task: **Task name:** Identify affected documents and sections from task outcome.
- Short description: **Task description:** Connect task context and actual changes to the minimal set of documented facts and exact sections.
- Technical value: **Technical value (for the project):** Replaces generic source_changed and a list of every existing file with explainable impact analysis.
- Product value: **Product value (for the user):** The system proposes edits to the relevant API, architecture or plan section without requiring all documentation to be updated.
- Scope: **Affected files:** project_formation.py; document_navigation.py; control_plane_documents.py; tests/product_agent_os/test_project_formation.py; tests/product_agent_os/test_document_navigation.py. Bare module paths refer to plugins/product-agent-os/scripts/product_agent_os/, scripts/assets paths to plugin root; root/project paths are explicit. Before implementation verify actual ownership and existing helpers/tests; do not create a new writer/state registry without demonstrated need.
- Acceptance criteria: **Acceptance criteria:** 1) Result contains affected document/section, changed contract or fact, provenance, reason and permitted related links. 2) Use actual changed files and task acceptance; mtime or directory name alone does not prove semantic change. 3) Bug fix without public contract change and a test rerun may yield no_change_needed with reason; API/schema/requirements changes select corresponding owners. 4) Reuse existing docs/adr, docs/runbooks, docs/ops, docs/testing, docs/history and docs/archive under T11; do not silently create a competing section. 5) Select PLAN/REQUIREMENTS/TEST/EVALS/RUNLOG/AGENTS and index by their events, not one bulk list. 6) Unknown impact or conflicting owners require review/handoff; heuristic is not proven document freshness. 7) Identical inputs and rule versions yield identical structured impact; proposals do not modify the project.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested analysis and adding G9 tasks for targeted documentation updates after each task without duplication; planning only at the time.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 21:17
- Depends on: PAOS-AUD-G9-T11; PAOS-AUD-G9-T02; PAOS-AUD-G9-T08.
- Blocks: PAOS-AUD-G9-T13; PAOS-AUD-G9-T14; PAOS-AUD-G9-T15
- Source: G9-S05–G9-S08; current source-backed analysis and owner request; implemented G8/G9 mechanisms are a reuse baseline, not evidence of new capabilities.
- Non-goals: Implementation during current authoring; mass documentation rewriting; new status registry; automatic semantic deletion; provider calls; cache/host/hooks/schedules activation; real-target/Git/publication actions; research matrix split; closing G6/T34/HOST or M1 SQL integration.
- Expected result: Explainable section-level impact in existing formation/navigation result.
- Verification gates: Focused test_project_formation and test_document_navigation: ordinary fix, API/schema change, alias reuse, unknown source and unchanged retry; check target bytes before/after preview. Actual implementation/check receipts are in G9 execution report; T17 owner acceptance obtained.
- Risks / approval gates: high; knowledge loss, false freshness or duplicated authority. Local implementation authorized, performed and owner-accepted; specific target writes/activation/external actions retain their boundaries. Rollback only the owning slice, checking concurrent changes and preserving history.
- Complexity: high
- Estimated execution time: not_estimated; refine through focused source preflight without invented deadlines.
- Agents: plugin-runtime-builder — proposed responsibility role; primary owns overall synchronization and evidence. No dispatch performed; modify shared paths sequentially or under a separate ownership agreement.
- Skills: canonical implementation-planner for decomposition; only task-matching lifecycle skills used during implementation; Python guidance for Python changes. This field does not launch skills, agents or hooks.
- Output artifacts: Explainable section-level impact in existing formation/navigation result. Detailed actual execution receipts belong in the existing G9 execution report/results; concise handoff in RUNLOG; no per-command/per-task report proliferation.
- Next step: T17 acceptance obtained; G9 closed with accepted limitations. Fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Explicit event classes and section-level candidates; no-change requires reason/coverage; unknown owner triggers handoff; read-only assessment.
- files touched / work locations: documentation_sync.py; project_formation.py; document_navigation.py
- technical value delivered: Explicit event classes and section-level candidates; no-change requires reason/coverage; unknown owner triggers handoff; read-only assessment.
- product value delivered: An API change does not require rewriting every document; repeated verification does not alter commands.
- actual implementation date and time: 10-11-2026 21:17
- verification evidence: Current run: full 1448 tests / 504.318s, OK (skipped=1); final affected/docs 164 tests / 22.975s, OK; fixtures 91/91, transcripts 26/26, compatibility compatible, strict MkDocs preview 11.81s. Exact provenance/deltas — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic/source review only; semantic completeness and model behavior not proven; T17 owner accepted; model-behavior limits accepted; fresh-session activation and real M1 SQL adapter separate. Exact section changes require applicable authority; no new writer/status registry.
- follow-up: Explicit T17 acceptance obtained; G9 closed. Model behavior was not tested; the limitation was accepted. Fresh-session activation separate.

### Task `PAOS-AUD-G9-T13`

- ID: `PAOS-AUD-G9-T13`
- Task: **Task name:** Targeted document updates with data preservation and idempotency.
- Short description: **Task description:** Apply agreed changes only to selected sections, preserving remaining content and history.
- Technical value: **Technical value (for the project):** Adds verifiable maintenance over existing merge/recovery without regenerating the whole document.
- Product value: **Product value (for the user):** The document receives the needed edit while user explanations, decisions and links remain in place.
- Scope: **Affected files:** merge_markdown.py; merge_infrastructure.py; control_plane_compaction.py; document_navigation.py; tests/product_agent_os/test_merge_infrastructure.py; tests/product_agent_os/test_control_plane_compaction.py; tests/product_agent_os/test_project_formation.py. Bare module paths refer to plugins/product-agent-os/scripts/product_agent_os/, scripts/assets paths to plugin root; root/project paths are explicit. Before implementation verify actual ownership and existing helpers/tests; do not create a new writer/state registry without demonstrated need.
- Acceptance criteria: **Acceptance criteria:** 1) Preview shows exact document/section and before/after diff; unmarked user content is not rewritten without explicit authorization for that edit. 2) Maintenance route uses existing write/merge/recovery primitives; G9 formation preserve-existing contract is not weakened or turned into hidden overwrite. 3) Outside the authorized section original bytes persist; IDs, history, evidence, links and acceptance are not lost. 4) Repeat with identical inputs creates no writes, duplicates, timestamp churn or new reports. 5) Stale digest, concurrent edit, ambiguous section and freeze/SQL authority stop apply; interruption has verifiable recovery without overwriting later user edits. 6) Preserve 40 000-byte limit/32 000 warning and explicit limits; excess routes to lossless compaction, not silent truncation. 7) Detailed docs/planning/ matrices remain whole; research matrix is not split; semantic dedup does not automatically delete data.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested analysis and adding G9 tasks for targeted documentation updates after each task without duplication; planning only at the time.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 21:17
- Depends on: PAOS-AUD-G9-T11; PAOS-AUD-G9-T12; PAOS-AUD-G9-T07; PAOS-AUD-G8-T07–T08.
- Blocks: PAOS-AUD-G9-T15; PAOS-AUD-G9-T17
- Source: G9-S05–G9-S08; current source-backed analysis and owner request; implemented G8/G9 mechanisms are a reuse baseline, not evidence of new capabilities.
- Non-goals: Implementation during current authoring; mass documentation rewriting; new status registry; automatic semantic deletion; provider calls; cache/host/hooks/schedules activation; real-target/Git/publication actions; research matrix split; closing G6/T34/HOST or M1 SQL integration.
- Expected result: Bounded section-change preview/apply/recovery and no-op receipts in the existing route.
- Verification gates: Focused merge/compaction/formation tests: authorized section update, exact bytes outside section, no-op repeat, stale/concurrent edit, interrupted recovery, size boundary and planning exemption; all writes only synthetic fixtures. Actual implementation/check receipts are in G9 execution report; T17 owner acceptance obtained.
- Risks / approval gates: high; knowledge loss, false freshness or duplicated authority. Local implementation authorized, performed and owner-accepted; specific target writes/activation/external actions retain their boundaries. Rollback only the owning slice, checking concurrent changes and preserving history.
- Complexity: high
- Estimated execution time: not_estimated; refine through focused source preflight without invented deadlines.
- Agents: plugin-runtime-builder — proposed responsibility role; primary owns overall synchronization and evidence. No dispatch performed; modify shared paths sequentially or under a separate ownership agreement.
- Skills: canonical implementation-planner for decomposition; only task-matching lifecycle skills used during implementation; Python guidance for Python changes. This field does not launch skills, agents or hooks.
- Output artifacts: Bounded section-change preview/apply/recovery and no-op receipts in the existing route. Detailed actual execution receipts belong in the existing G9 execution report/results; concise handoff in RUNLOG; no per-command/per-task report proliferation.
- Next step: T17 acceptance obtained; G9 closed with accepted limitations. Fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Exact section replay, UTF-8/CRLF preservation, CAS/digest, shared journal/rollback, no-op, freeze/SQL guards, budgets and planning exception.
- files touched / work locations: documentation_sync.py; control_plane_compaction.py; existing navigation/compaction tests
- technical value delivered: Exact section replay, UTF-8/CRLF preservation, CAS/digest, shared journal/rollback, no-op, freeze/SQL guards, budgets and planning exception.
- product value delivered: Adjacent text and recovery history are preserved; repetition creates no clutter.
- actual implementation date and time: 10-11-2026 21:17
- verification evidence: Current run: full 1448 tests / 504.318s, OK (skipped=1); final affected/docs 164 tests / 22.975s, OK; fixtures 91/91, transcripts 26/26, compatibility compatible, strict MkDocs preview 11.81s. Exact provenance/deltas — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic/source review only; semantic completeness and model behavior not proven; T17 owner accepted; model-behavior limits accepted; fresh-session activation and real M1 SQL adapter separate. Exact section changes require applicable authority; no new writer/status registry.
- follow-up: Explicit T17 acceptance obtained; G9 closed. Model behavior was not tested; the limitation was accepted. Fresh-session activation separate.

### Task `PAOS-AUD-G9-T14`

- ID: `PAOS-AUD-G9-T14`
- Task: **Task name:** Check duplication between documents and permitted concise summaries.
- Short description: **Task description:** Extend duplicate search across affected documents, accounting for ownership, summaries and managed mirrors.
- Technical value: **Technical value (for the project):** Detects copied statuses and evidence across files that current intra-file duplicate_blocks misses.
- Product value: **Product value (for the user):** Users get one primary source for a fact instead of multiple diverging copies.
- Scope: **Affected files:** document_navigation.py; system_file_hygiene.py; scripts/check_documents.py; tests/product_agent_os/test_document_navigation.py; tests/product_agent_os/test_system_file_hygiene.py. Bare module paths refer to plugins/product-agent-os/scripts/product_agent_os/, scripts/assets paths to plugin root; root/project paths are explicit. Before implementation verify actual ownership and existing helpers/tests; do not create a new writer/state registry without demonstrated need.
- Acceptance criteria: **Acceptance criteria:** 1) Exact duplicate detection works across selected files and returns both positions/sections and canonical owner; preserve intra-file checks. 2) Intentional short summaries, links, code examples, repeated matrix structure and declared mirrors are not automatically defects. 3) Summary links to the primary source; stale mirror/revision or conflicting statuses produce separate findings. 4) Semantic duplicates and contradictions require agent review; no automatic proof of semantic uniqueness claimed. 5) Restrict checks to affected docs and explicit sources; full scan requires separate grounds. 6) A finding does not authorize deletion, overwrite history or disappear behind generic ok=true without disposition of an applicable blocking finding.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested analysis and adding G9 tasks for targeted documentation updates after each task without duplication; planning only at the time.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 21:17
- Depends on: PAOS-AUD-G9-T11; PAOS-AUD-G9-T12; existing G8 duplicate/navigation checks.
- Blocks: PAOS-AUD-G9-T15; PAOS-AUD-G9-T17
- Source: G9-S05–G9-S08; current source-backed analysis and owner request; implemented G8/G9 mechanisms are a reuse baseline, not evidence of new capabilities.
- Non-goals: Implementation during current authoring; mass documentation rewriting; new status registry; automatic semantic deletion; provider calls; cache/host/hooks/schedules activation; real-target/Git/publication actions; research matrix split; closing G6/T34/HOST or M1 SQL integration.
- Expected result: Cross-file findings and review dispositions in the existing checker without a separate duplicate registry.
- Verification gates: Focused navigation/hygiene tests: cross-file repeated evidence, intentional summaries, tables/examples, stale mirrors, conflicting status and semantic-review-required cases; false-positive/negative cases explicitly retained. Actual implementation/check receipts are in G9 execution report; T17 owner acceptance obtained.
- Risks / approval gates: medium; knowledge loss, false freshness or duplicated authority. Local implementation authorized, performed and owner-accepted; specific target writes/activation/external actions retain their boundaries. Rollback only the owning slice, checking concurrent changes and preserving history.
- Complexity: medium
- Estimated execution time: not_estimated; refine through focused source preflight without invented deadlines.
- Agents: plugin-runtime-builder — proposed responsibility role; primary owns overall synchronization and evidence. No dispatch performed; modify shared paths sequentially or under a separate ownership agreement.
- Skills: canonical implementation-planner for decomposition; only task-matching lifecycle skills used during implementation; Python guidance for Python changes. This field does not launch skills, agents or hooks.
- Output artifacts: Cross-file findings and review dispositions in the existing checker without a separate duplicate registry. Detailed actual execution receipts belong in the existing G9 execution report/results; concise handoff in RUNLOG; no per-command/per-task report proliferation.
- Next step: T17 acceptance obtained; G9 closed with accepted limitations. Fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Cross-file duplicate/conflicting-state findings; verified mirror disposition; linked fresh summary; bounded scan and blocking unresolved findings.
- files touched / work locations: document_navigation.py; check_documents.py; system_file_hygiene.py; test_document_navigation.py
- technical value delivered: Cross-file duplicate/conflicting-state findings; verified mirror disposition; linked fresh summary; bounded scan and blocking unresolved findings.
- product value delivered: Conflicting copies are visible to the owner; no automatic deletion.
- actual implementation date and time: 10-11-2026 21:17
- verification evidence: Current run: full 1448 tests / 504.318s, OK (skipped=1); final affected/docs 164 tests / 22.975s, OK; fixtures 91/91, transcripts 26/26, compatibility compatible, strict MkDocs preview 11.81s. Exact provenance/deltas — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic/source review only; semantic completeness and model behavior not proven; T17 owner accepted; model-behavior limits accepted; fresh-session activation and real M1 SQL adapter separate. Exact section changes require applicable authority; no new writer/status registry.
- follow-up: Explicit T17 acceptance obtained; G9 closed. Model behavior was not tested; the limitation was accepted. Fresh-session activation separate.

### Task `PAOS-AUD-G9-T15`

- ID: `PAOS-AUD-G9-T15`
- Task: **Task name:** Verifiable task completion and coordinated pointer updates.
- Short description: **Task description:** Connect task closure to applicable docs impact and current revision-pinned representations.
- Technical value: **Technical value (for the project):** Prevents missing a mandatory document update or leaving the PLAN selector on an old matrix revision.
- Product value: **Product value (for the user):** A completed task represents consistent knowledge and status, not only a card mark.
- Scope: **Affected files:** task_plan_lifecycle.py; validators.py; status_snapshot.py; stage_manifest.py; existing merge/recovery primitives; tests/product_agent_os/test_task_plan_lifecycle.py; tests/product_agent_os/test_status_snapshot.py; tests/product_agent_os/test_merge_infrastructure.py. Bare module paths refer to plugins/product-agent-os/scripts/product_agent_os/, scripts/assets paths to plugin root; root/project paths are explicit. Before implementation verify actual ownership and existing helpers/tests; do not create a new writer/state registry without demonstrated need.
- Acceptance criteria: **Acceptance criteria:** 1) New completion route checks applicable docs impact: source/section exists, revision/evidence matches verified state, no_change_needed has specific basis. 2) Mandatory unresolved update/handoff prevents a stronger completion claim; technical result and unfinished docs may be partial without false implemented/accepted. 3) Update card and corresponding PLAN revision as a coordinated recoverable packet; other pinned sources/prefixes unchanged. 4) Stale source, freeze, competing writer and interrupted update cause explicit stop/recovery; no independent SQL projection. 5) Legacy create_task_plan complete has an explicitly documented compatible route or understandable migration error, without silent gate bypass. 6) docs_synced=true or hash alone does not prove semantic completeness; review responsibility remains explicit. 7) Owner acceptance and fresh-session activation are not inferred from a machine gate; hooks remain advisory without separate activation decision.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested analysis and adding G9 tasks for targeted documentation updates after each task without duplication; planning only at the time.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 21:17
- Depends on: PAOS-AUD-G9-T11; PAOS-AUD-G9-T12; PAOS-AUD-G9-T13; PAOS-AUD-G9-T14.
- Blocks: PAOS-AUD-G9-T16; PAOS-AUD-G9-T17
- Source: G9-S05–G9-S08; current source-backed analysis and owner request; implemented G8/G9 mechanisms are a reuse baseline, not evidence of new capabilities.
- Non-goals: Implementation during current authoring; mass documentation rewriting; new status registry; automatic semantic deletion; provider calls; cache/host/hooks/schedules activation; real-target/Git/publication actions; research matrix split; closing G6/T34/HOST or M1 SQL integration.
- Expected result: Source-owned completion validation and recoverable revision sync without a new status authority.
- Verification gates: Focused lifecycle/status/merge tests: updated/no-change/handoff, missing or forged receipt, stale digest, interrupted two-source update, unrelated source preservation, legacy migration and SQL/freeze refusal; current-state projection without issues after successful flow. Actual implementation/check receipts are in G9 execution report; T17 owner acceptance obtained.
- Risks / approval gates: high; knowledge loss, false freshness or duplicated authority. Local implementation authorized, performed and owner-accepted; specific target writes/activation/external actions retain their boundaries. Rollback only the owning slice, checking concurrent changes and preserving history.
- Complexity: high
- Estimated execution time: not_estimated; refine through focused source preflight without invented deadlines.
- Agents: lifecycle-orchestrator — proposed responsibility role; primary owns overall synchronization and evidence. No dispatch performed; modify shared paths sequentially or under a separate ownership agreement.
- Skills: canonical implementation-planner for decomposition; only task-matching lifecycle skills used during implementation; Python guidance for Python changes. This field does not launch skills, agents or hooks.
- Output artifacts: Source-owned completion validation and recoverable revision sync without a new status authority. Detailed actual execution receipts belong in the existing G9 execution report/results; concise handoff in RUNLOG; no per-command/per-task report proliferation.
- Next step: T17 acceptance obtained; G9 closed with accepted limitations. Fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Preview/apply completion connects docs, card and matching PLAN pin; handoff/stale/no-op conflicts prohibit strong closure; legacy flag explicit.
- files touched / work locations: documentation_sync.py; sync_task_documents.py; task_plan_lifecycle.py; validators.py; status_snapshot.py; lifecycle tests
- technical value delivered: Preview/apply completion connects docs, card and matching PLAN pin; handoff/stale/no-op conflicts prohibit strong closure; legacy flag explicit.
- product value delivered: Task status stays connected to the current document and pointer.
- actual implementation date and time: 10-11-2026 21:17
- verification evidence: Current run: full 1448 tests / 504.318s, OK (skipped=1); final affected/docs 164 tests / 22.975s, OK; fixtures 91/91, transcripts 26/26, compatibility compatible, strict MkDocs preview 11.81s. Exact provenance/deltas — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic/source review only; semantic completeness and model behavior not proven; T17 owner accepted; model-behavior limits accepted; fresh-session activation and real M1 SQL adapter separate. Exact section changes require applicable authority; no new writer/status registry.
- follow-up: Explicit T17 acceptance obtained; G9 closed. Model behavior was not tested; the limitation was accepted. Fresh-session activation separate.

### Task `PAOS-AUD-G9-T16`

- ID: `PAOS-AUD-G9-T16`
- Task: **Task name:** Unified post-task update rules without accumulating history in the root.
- Short description: **Task description:** Align active/package workflows, canonical skills and user documentation with targeted synchronization.
- Technical value: **Technical value (for the project):** Resolves conflicting RUNLOG evidence-storage guidance and separates mandatory event review from calendar recommendations.
- Product value: **Product value (for the user):** The agent routinely checks documentation and explains only necessary changes without imposing bureaucracy on every task.
- Scope: **Affected files:** .codex/workflows/control-plane-sync.md; .codex/workflows/task-plan-lifecycle.md; plugins/product-agent-os/assets/templates/workflows/control-plane-sync.md; plugins/product-agent-os/assets/templates/workflows/task-plan-lifecycle.md; plugins/product-agent-os/skills/implementation-planner/SKILL.md; plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md; plugins/product-agent-os/skills/completion-skeptic/SKILL.md; docs/product-agent-os/project-formation.md/.en.md; technical.md/.en.md; cli-reference.md/.en.md; docs/sources/registry.md/.en.md; tests/product_agent_os/test_task_plan_lifecycle.py; tests/product_agent_os/test_product_agent_os_docs.py. Bare module paths refer to plugins/product-agent-os/scripts/product_agent_os/, scripts/assets paths to plugin root; root/project paths are explicit. Before implementation verify actual ownership and existing helpers/tests; do not create a new writer/state registry without demonstrated need.
- Acceptance criteria: **Acceptance criteria:** 1) One rule: assess impact after each completed task; update only affected owner/section or record no_change_needed with reason. 2) Matrix stores task result, owning evidence stores verification detail, TEST stores commands/conditions and pointers, RUNLOG stores a compact current handoff; full command logs and duplicate statuses are not multiplied. 3) Resolve conflicting canonical skill and active/package workflow wording; ordinary tasks do not require a separate report or full closure packet. 4) Separate event, soft/hard size and periodic reviews; weekly/monthly policy remains not_created/read_only, no schedule activation. 5) Mandatory docs gap blocks only dependent closure; unrelated docs do not create artificial gates. 6) Examples cover bug fix, API change, test rerun, new docs area, repeat task and handoff with exact owning files. 7) Static parity is not presented as fresh-session loading; activation remains separate.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested analysis and adding G9 tasks for targeted documentation updates after each task without duplication; planning only at the time.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 21:17
- Depends on: PAOS-AUD-G9-T11; PAOS-AUD-G9-T15.
- Blocks: PAOS-AUD-G9-T17
- Source: G9-S05–G9-S08; current source-backed analysis and owner request; implemented G8/G9 mechanisms are a reuse baseline, not evidence of new capabilities.
- Non-goals: Implementation during current authoring; mass documentation rewriting; new status registry; automatic semantic deletion; provider calls; cache/host/hooks/schedules activation; real-target/Git/publication actions; research matrix split; closing G6/T34/HOST or M1 SQL integration.
- Expected result: Aligned durable workflow instructions and RU/EN guide; no new schedules/hooks activation.
- Verification gates: Docs/lifecycle tests, tools/check_docs.py, task matrix validation, changed local links and git diff --check; strict MkDocs for navigation/config/rendered-doc changes. Representative baseline/treatment for materially changed agent instructions per T17, without live providers by default. Actual implementation/check receipts are in G9 execution report; T17 owner acceptance obtained.
- Risks / approval gates: medium; knowledge loss, false freshness or duplicated authority. Local implementation authorized, performed and owner-accepted; specific target writes/activation/external actions retain their boundaries. Rollback only the owning slice, checking concurrent changes and preserving history.
- Complexity: medium
- Estimated execution time: not_estimated; refine through focused source preflight without invented deadlines.
- Agents: docs-maintainer — proposed responsibility role; primary owns overall synchronization and evidence. No dispatch performed; modify shared paths sequentially or under a separate ownership agreement.
- Skills: canonical implementation-planner for decomposition; only task-matching lifecycle skills used during implementation; Python guidance for Python changes. This field does not launch skills, agents or hooks.
- Output artifacts: Aligned durable workflow instructions and RU/EN guide; no new schedules/hooks activation. Detailed actual execution receipts belong in the existing G9 execution report/results; concise handoff in RUNLOG; no per-command/per-task report proliferation.
- Next step: T17 acceptance obtained; G9 closed with accepted limitations. Fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Active/packaged workflows, canonical skills and handoff reference, templates and RU/EN docs/registry aligned; full logs do not go into RUNLOG.
- files touched / work locations: .codex workflows/templates; plugin workflows/templates/skills/references; public RU/EN docs/registry
- technical value delivered: Active/packaged workflows, canonical skills and handoff reference, templates and RU/EN docs/registry aligned; full logs do not go into RUNLOG.
- product value delivered: Only changed information is updated; separate report and full packet are not imposed on small tasks.
- actual implementation date and time: 10-11-2026 21:17
- verification evidence: Current run: full 1448 tests / 504.318s, OK (skipped=1); final affected/docs 164 tests / 22.975s, OK; fixtures 91/91, transcripts 26/26, compatibility compatible, strict MkDocs preview 11.81s. Exact provenance/deltas — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic/source review only; semantic completeness and model behavior not proven; T17 owner accepted; model-behavior limits accepted; fresh-session activation and real M1 SQL adapter separate. Exact section changes require applicable authority; no new writer/status registry.
- follow-up: Explicit T17 acceptance obtained; G9 closed. Model behavior was not tested; the limitation was accepted. Fresh-session activation separate.

### Task `PAOS-AUD-G9-T17`

- ID: `PAOS-AUD-G9-T17`
- Task: **Task name:** End-to-end targeted synchronization verification and acceptance of expanded G9.
- Short description: **Task description:** Verify task completion → impact → section update → dedup → revision sync and present comparison to the owner.
- Technical value: **Technical value (for the project):** Demonstrates mechanisms working together without data loss, unnecessary writes or stale projections.
- Product value: **Product value (for the user):** Users see that necessary knowledge is updated after a task without documentation growing without cause.
- Scope: **Affected files:** Existing tests/product_agent_os/test_project_formation.py, test_task_plan_lifecycle.py, test_document_navigation.py, test_merge_infrastructure.py, test_system_file_hygiene.py, test_status_snapshot.py; synthetic fixtures under tests/fixtures/product_agent_os/g9-project-formation/; research/product-agent-os-g9-execution-report.md; docs/superpowers/specs/paos-aud-g9-project-formation-results.json; current audit matrix and root pointers. Bare module paths refer to plugins/product-agent-os/scripts/product_agent_os/, scripts/assets paths to plugin root; root/project paths are explicit. Before implementation verify actual ownership and existing helpers/tests; do not create a new writer/state registry without demonstrated need.
- Acceptance criteria: **Acceptance criteria:** 1) Establish current G9 baseline before extension; comparison uses identical task facts/workspaces and source/config/fixture revisions without retroactively revising old receipts. 2) Cover no-contract bug fix, API/schema change, requirement change, test rerun, unknown owner, existing aliases, cross-file duplicates, allowed summary/mirror, concurrent edit/freeze, interruption and next task cycle. 3) Measure missed mandatory updates, excess changed files/sections, bytes outside authorized sections, repeated writes, conflicting copies, links and current-state revisions; mandatory failure is not hidden by an aggregate. 4) Repeating the same sync yields zero unnecessary writes; then a new task updates only changed facts without repeated closure-block accumulation. 5) Preserve history/IDs/evidence, 40 000-byte contract, docs/planning exception and research-split prohibition; no changes to real external projects. 6) Separate representative instruction comparisons from deterministic fixtures; absent behavioral evidence is an explicit owner gap, not a model-improvement claim. 7) Pass applicable TEST.md runtime/fixture/transcript/compatibility and docs/matrix/link gates; retain failures and retries. 8) T10 owner decision expressly accepts the initial packet; new T11–T17 result is separately presented and accepted by the owner; until then expanded G9 needs_user_acceptance, with fresh-session activation separate.
- Group: PAOS-AUD-G9
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested analysis and adding G9 tasks for targeted documentation updates after each task without duplication; planning only at the time.
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 21:17
- Depends on: PAOS-AUD-G9-T11–T16; PAOS-AUD-G9-T10 owner decision required for final group closure but does not block local T11–T16 implementation after separate authorization.
- Blocks: Expanded PAOS-AUD-G9 closure; does not close HOST/fresh-session activation or M1 SQL gates.
- Source: G9-S05–G9-S08; current source-backed analysis and owner request; implemented G8/G9 mechanisms are a reuse baseline, not evidence of new capabilities.
- Non-goals: Implementation during current authoring; mass documentation rewriting; new status registry; automatic semantic deletion; provider calls; cache/host/hooks/schedules activation; real-target/Git/publication actions; research matrix split; closing G6/T34/HOST or M1 SQL integration.
- Expected result: Versioned comparison and owner acceptance packet in existing G9 evidence artifacts; no empty new report now.
- Verification gates: Focused listed test modules; then python -B -m unittest discover -s tests -p test_*.py, run_fixture_eval.py, run_transcript_eval.py, validate_codex_compatibility.py per TEST.md; docs unittest, check_docs.py, validate_task_matrix.py and diff check; strict MkDocs for navigation/site scope. Actual receipts only after execution. Actual implementation/check receipts are in G9 execution report; T17 owner acceptance obtained.
- Risks / approval gates: high; knowledge loss, false freshness or duplicated authority. Local implementation authorized, performed and owner-accepted; specific target writes/activation/external actions retain their boundaries. Rollback only the owning slice, checking concurrent changes and preserving history.
- Complexity: high
- Estimated execution time: not_estimated; refine through focused source preflight without invented deadlines.
- Agents: reviewer — proposed responsibility role; primary owns overall synchronization and evidence. No dispatch performed; modify shared paths sequentially or under a separate ownership agreement.
- Skills: canonical implementation-planner for decomposition; only task-matching lifecycle skills used during implementation; Python guidance for Python changes. This field does not launch skills, agents or hooks.
- Output artifacts: Versioned comparison and owner acceptance packet in existing G9 evidence artifacts; no empty new report now. Detailed actual execution receipts belong in the existing G9 execution report/results; concise handoff in RUNLOG; no per-command/per-task report proliferation.
- Next step: T17 acceptance obtained; G9 closed with accepted limitations. Fresh-session activation separate.

#### Completion Report

- status: implemented
- what was done: Same-input baseline comparison, regressions and verification packet prepared; owner accepted, including explicitly accepted model/semantic evidence limitations; G9 closed.
- files touched / work locations: g9_documentation_comparison.py; existing G9 results/report; root control plane; audit matrix
- technical value delivered: Same-input baseline comparison, regressions and verification packet prepared; owner accepted, including explicitly accepted model/semantic evidence limitations; G9 closed.
- product value delivered: Owner accepted the reproducible comparison and limitations; expanded G9 closed.
- actual implementation date and time: 10-11-2026 21:17
- verification evidence: Current run: full 1448 tests / 504.318s, OK (skipped=1); final affected/docs 164 tests / 22.975s, OK; fixtures 91/91, transcripts 26/26, compatibility compatible, strict MkDocs preview 11.81s. Exact provenance/deltas — research/product-agent-os-g9-execution-report.md.
- residual risks: Local synthetic/source review only; semantic completeness and model behavior not proven; T17 owner accepted; model-behavior limits accepted; fresh-session activation and real M1 SQL adapter separate. Exact section changes require applicable authority; no new writer/status registry.
- follow-up: Explicit T17 acceptance obtained; G9 closed. Model behavior was not tested; the limitation was accepted. Fresh-session activation separate.
