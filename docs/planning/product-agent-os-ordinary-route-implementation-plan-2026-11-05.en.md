# Product-Agent OS: implementation plan after the documentation audit

## G6 handoff — 09.11.2026

G6 partially_verified: three synthetic pilots were run from the current project in host-target/pilots; all checks passed, results needs_user_acceptance. With owner approval, HOST-01 no longer blocks those pilots. Fresh-session activation for HOST-01/HOST-02 remains a separate open task; T34 no-go. Owner feedback/acceptance null; manual_only remains.

Source status: project-local implementation proposal, 2026-11-05; based on current code and source-owned task groups. The plan was saved at the owner's request; ORD-01–ORD-06 were implemented locally, GAP-01–GAP-05 were implemented locally with the outstanding gates listed below. Current G6: T30–T33 implemented locally, T34 no-go; three GAP-06 pilots passed and await owner acceptance.

## GAP-03 approved metadata correction — 05.11.2026

Task ID: PAOS-GAP03-METADATA-2026-11-05. The owner explicitly approved the four-file diff below. Scope extension: only the four named `agents/openai.yaml` files plus existing status/evidence synchronization. Ordinary bounded fix; explicit-only remains false; no new implicit class, cache refresh, global settings, trust, host probe, Git or publication.

Implemented: moved `allow_implicit_invocation: false` from `interface` to `policy` in `agent-team-designer`, `docs-maintainer`, `implementation-planner`, `requirements-author`. Before editing, all four current SHA-256 matched the saved proposal. Before validation produced four errors per file; afterward all 12 canonical metadata validate with false and no errors. Source/cache normalized drift remains 11/12; cache hashes remain unchanged. This closes the metadata correction and M04 decision locally, not M06 host exposure/invocation or GAP-05 trust/probe. The earlier proposal/digests and GAP receipts below remain historical evidence.

Verification: `python -B -m unittest tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_validators -q` — 94 tests, 1.680s, OK, exit 0. Final docs/control-plane checks: 232 tests, 9.969s, OK, exit 0 (`test_product_agent_os_docs`, `test_task_plan_lifecycle`, `test_lifecycle_hooks`, `test_infrastructure_templates`). Both hook validators, task-matrix validator, check_docs and git diff --check passed. Exact approved diff confirmed; 2394 other baseline files unchanged; all 12 cache skill hashes unchanged. Receipt: `.docs-tools/reports/gap-metadata-preservation.json`. No full unittest/fixture rerun is needed for this bounded metadata correction; the earlier 1284/91/26 results are historical, not newly executed evidence.

Control-plane sync: PLAN/RUNLOG/TEST, B42 matrix, affected current RU/EN claims and registry updated. REQUIREMENTS/EVALS/prod_test: not_applicable (no new requirements/rubrics/historical Batch 39 evidence). No site rebuild or freshness claim; navigation and Mermaid unchanged. Self-review verifies exact approved diff and unchanged false policy; no independent reviewer or host activation claim.


## GAP-01–GAP-05 execution — current run 05.11.2026

Lifecycle task ID: PAOS-GAP-01-05-2026-11-05. Status: partially_verified. Explicit user authority: local implementation of GAP-01–05, their tests and RU/EN sync. No T30–T34/GAP-06, cache/trust/provider/publication actions. GAP-03 M06 and GAP-05 fresh-host probes remain separate evidence gates. Baseline: .docs-tools/reports/gap-01-05-baseline.json. Ownership is the union of the five task scopes plus TEST.md, this plan and the service marker. One writer, self_review; no delegation.

### GAP design and scope decisions

- GAP-01: current product queue and B45 next=T30 are distinct. Old T28/Stop receipts stay historical; manifest becomes local-package wording, placeholder URLs are not invented away.
- GAP-02: one bounded read-only resolver owns portable/compatibility precedence. Recognized root plugin.json owns skills/ and mcp.json; inline extensions.com.openai replaces the overlay, never merges. Flat .mcp.json remains legacy_flat_observed/needs_review. No automatic migration or MCP execution. Official source checked 2026-11-05: https://developers.openai.com/plugins/build/plugins and https://agent-plugins.org/schemas/1.0.0/plugin.schema.json plus mcp.schema.json. Supported-subset checking is not full JSON Schema or host verification.
- GAP-03: preserve intended explicit-only policy. Source/cache normalized digests, declared selection and host exposure/invocation are separate. Four metadata files put allow_implicit_invocation under interface instead of policy; validator reports errors. Correcting those four agents/openai.yaml files is outside the five named task file lists and requires a concrete owner decision; no silent edit. M06 fresh-session evidence remains missing. Discovery's explicit compliance/learning overlay is shared GAP-02/03 ownership; recommendations grant no authority.
- GAP-04: exact HTTPS hostname parsing, presence vs semantic support vs freshness; 90-day date review is a local heuristic. Headers and lookalike/userinfo URLs do not prove evidence. No crawler or automatic freshness claim.
- GAP-05 decision: optional hook command arguments --report-authority and --report-authority-sha256 pin a bounded grant in the trusted hook definition. Arbitrary tool payload cannot grant permission. Grant binds workspace digest, exact new task ID, previous task ID, exact current marker SHA-256, exact new Markdown path, issued/expiry time (maximum 24h). Current read-only marker must be fresh/nonterminal and explicitly transitioned. Only one literal Add File patch is allowed; canonical nested functions.exec literal apply_patch is supported, dynamic/multiple/unknown mutating wrappers fail closed. Existing files, neighboring output, config/hook/control-plane paths, traversal/symlink/Windows aliases and expired/stale/terminal grants are denied. Existing safety guards run first. Default hook command has no grant and keeps prior behavior. A grant cannot change sandbox or host approvals.
- GAP-05 alternatives: payload boolean or unpinned workspace grant rejected as self-authorizing; broad directory grant rejected; automatic marker-reset rejected. Read-only target plus exact create-only report is the smallest implementable contract. Later append/update needs a separately reviewed contract; no automatic reusable write token.
- GAP-05 activation: prepare source patch, negative tests and exact hashes first. Do not alter hooks.json, trust records, active command arguments or installed cache. Fresh-host positive/negative probe is a separate exact-hash owner action. Local pass cannot close that gate.
- Verification ownership: primary agent, self_review. Existing capability scan completed for component consumers, source policy, skill contracts and hook parser. No new dependency; standard-library adapters; risk-selected malformed/precedence/provenance/spoof/path/terminal cases. Frontend/DDD/product-outcome/model promotion gates are not_applicable to this local contract slice; no product-effect claim is made.

## GAP closure matrix

| Task | Plan status | Strongest evidence | Remaining gate |
| --- | --- | --- | --- |
| GAP-01 | implemented | Local docs/manifest/pointers verified | No distribution/production readiness claim |
| GAP-02 | implemented | Shared resolver and consumers locally verified | Actual package MCP needs_review; host evidence separate |
| GAP-03 | blocked | Local provenance/metadata/routing verified; approved metadata correction applied | M06 host receipt |
| GAP-04 | implemented | Local source-policy positive/negative checks verified | Semantic source review remains manual |
| GAP-05 | blocked | implemented_not_runtime_verified | Separate trust and fresh-host report probe |

Parent closure_level=partially_verified; tester_verdict=partial_only; context_mode=self_review. Required host/owner children prevent parent completion. No global/cache/trust/provider/Git/publication action occurred.

## GAP final verification receipt — 05.11.2026

Final source/test gate: Python 3.13.5, isolated accessible host TEMP (`paos-gap-tests`), no bytecode writes. The implementation/test manifest records 20 selected input hashes; all still match the tested revision. Active/package hook and workflow sources match. No later implementation changes were made.

| Check | Observed result |
| --- | --- |
| Full unittest | 1284 tests, 848.832s, OK (skipped=1), exit 0 |
| Fixture eval | 91/91, exit 0 after renderer correction |
| Transcript eval | 26/26, exit 0; deterministic synthetic sessions |
| Final docs + task-plan tests | 106 tests, 3.198s, exit 0 |
| Hook definitions/source validators | exit 0; no activation proof |
| Task-matrix validator, check_docs, diff check | exit 0 |
| Final strict MkDocs preview | 18.60s, exit 0; root site unchanged |
| Final preview links/anchors | 10 RU/EN pages, 1554 checked, zero errors |
| Mermaid | Source blocks unchanged; runtime rendering not repeated |
| Package compatibility | exit 1, needs_review; current flat MCP declaration remains unresolved |

Commands executed for this GAP slice:

```powershell
python -B -m unittest discover -s tests -p 'test_*.py' -q
python -B plugins/product-agent-os/scripts/run_fixture_eval.py
python -B plugins/product-agent-os/scripts/run_transcript_eval.py
python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py
python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle -q
python -B plugins/product-agent-os/scripts/validate_hooks.py .codex/hooks.json
python -B plugins/product-agent-os/scripts/validate_hooks.py .codex/hooks
python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md
python -B tools/check_docs.py
.venv-docs/Scripts/python.exe -B -m mkdocs build --strict --site-dir .docs-tools/reports/gap-preview
python -B .docs-tools/reports/gap_check_links.py
git -c core.safecrlf=false diff --check
```

Preservation receipt: 33 existing owned files changed plus one new resolver; 2369 protected baseline file hashes unchanged, including 660 root-site files. All 12 non-GAP-01–05 task blocks are unchanged (completed ORD, T30–T34 and GAP-06). Installed-cache hashes for all 12 skills match the pre-check receipt; four metadata findings persist unchanged. Root control-plane files remain below 50 KiB. A separate untracked research artifact was not authored or changed by this slice. Detailed machine receipts: `.docs-tools/reports/gap-preservation.json`, `gap-links.json`, `gap-verified-inputs.json`, `gap-01-05-full-unittest-final.log`, `gap-fixture-final.json`, `gap-transcript.json`, `gap-compatibility.json`, `gap-mkdocs-final.log`.

Execution time: 4611.7 seconds from recorded baseline 2026-11-05T13:37:31.971993+00:00 to final closure preparation 2026-11-05T14:54:23.633068+00:00. Zero subagents; one observed context-compaction handoff. Exact model/reasoning and complete token/tool counters are not exposed in the available runtime trace.

## GAP control-plane sync

PLAN.md, RUNLOG.md and TEST.md updated with current queue, evidence and residual gates. REQUIREMENTS.md: not_applicable (approved scope/acceptance unchanged). EVALS.md: not_applicable (rubrics/thresholds unchanged; only representative local regression cases added). prod_test.md: not_applicable (historical Batch 39 evidence family unchanged). Registry RU/EN updated for component/metadata official sources and local heuristics. B42 source matrix owns current local inventory, preserving historical planning status. No overflow/refactor required; root files remain within compactness budget. Handoff: owner for four metadata files and separate host/trust decisions. T23–T29, ORD task blocks and later T30–T34/GAP-06 task blocks are preserved against baseline.

## GAP remaining owner decisions and local review packet

M04 proposed decision: preserve explicit-only behavior for all current skills; do not enable the read-only implicit candidate. Four malformed metadata files need only a policy-section correction. Their exact current hashes and proposed diff are below. These files are outside the saved GAP-03 owned-file list and have not been edited. Installed cache/global configuration are excluded. After a separately authorized correction, run the metadata validator and lifecycle tests; refresh cache only under a separate destination/hash/rollback approval.

- `plugins/product-agent-os/skills/agent-team-designer/agents/openai.yaml`: SHA-256 `2dad58c0e2e33e0e126dfff697dab6affe2f1a6820dd9a9e648f86baaf796e8a`.

```diff
--- plugins/product-agent-os/skills/agent-team-designer/agents/openai.yaml
+++ plugins/product-agent-os/skills/agent-team-designer/agents/openai.yaml
@@ -4,2 +4,3 @@
   default_prompt: "Use $agent-team-designer to design role ownership and handoffs for this plan."
+policy:
   allow_implicit_invocation: false
```

- `plugins/product-agent-os/skills/docs-maintainer/agents/openai.yaml`: SHA-256 `8354e8bce49c0743d62982c2d40de8a24b1651f5685e5b17a6e14e8f4b718d6f`.

```diff
--- plugins/product-agent-os/skills/docs-maintainer/agents/openai.yaml
+++ plugins/product-agent-os/skills/docs-maintainer/agents/openai.yaml
@@ -4,2 +4,3 @@
   default_prompt: "Use $docs-maintainer to align requirements, source registry, glossary, and traceability docs."
+policy:
   allow_implicit_invocation: false
```

- `plugins/product-agent-os/skills/implementation-planner/agents/openai.yaml`: SHA-256 `01329c0b3474d2354746962dc193ee654cb038986e8b678e6f35197f45ec50e5`.

```diff
--- plugins/product-agent-os/skills/implementation-planner/agents/openai.yaml
+++ plugins/product-agent-os/skills/implementation-planner/agents/openai.yaml
@@ -4,2 +4,3 @@
   default_prompt: "Use $implementation-planner to decompose these requirements into verified implementation slices."
+policy:
   allow_implicit_invocation: false
```

- `plugins/product-agent-os/skills/requirements-author/agents/openai.yaml`: SHA-256 `eeea4967fe77cd2c744a64bb473d4b77bc2c8945eda9b340292856cacd3832ba`.

```diff
--- plugins/product-agent-os/skills/requirements-author/agents/openai.yaml
+++ plugins/product-agent-os/skills/requirements-author/agents/openai.yaml
@@ -4,2 +4,3 @@
   default_prompt: "Use $requirements-author to turn this project goal into acceptance criteria."
+policy:
   allow_implicit_invocation: false
```

GAP-05 source patch is reviewable; report authority is **not installed**. Active/package source hashes match. The existing `hooks.json` definition/pin is unchanged. A future exact-host probe must identify client/version/auth, show a new-task scope, prepare a fresh marker transition and a bounded grant, review the complete command/pin in the host, then run one positive exact-report case and negatives for neighboring code/config/hook paths, stale/terminal state and nested wrappers. No successful report creation in an actual host is claimed by the current preflight fixtures. Approval for source edits is not approval for trust, cache or provider mutation.

| Artifact | SHA-256 | Boundary |
| --- | --- | --- |
| `.codex/hooks/pre_tool_use_policy.py` | `244ced9c58aedb2ace885fa4ad5e2f6d1bd1a03c3b8d7b858ef1ef0297bb0878` | source only / trust unchanged |
| `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py` | `244ced9c58aedb2ace885fa4ad5e2f6d1bd1a03c3b8d7b858ef1ef0297bb0878` | source only / trust unchanged |
| `.codex/hooks.json` | `8a40cbbb7bdc0b1d1b48d1ec873b109ee21358d85daae1479891e3a4fec74abb` | source only / trust unchanged |
| `plugins/product-agent-os/assets/templates/hooks/hooks.json` | `8a40cbbb7bdc0b1d1b48d1ec873b109ee21358d85daae1479891e3a4fec74abb` | source only / trust unchanged |

Grant schema: exactly `schema_version: 1`, `task_id`, `previous_task_id`, `workspace_sha256`, `marker_sha256`, `output_path`, `issued_at`, `expires_at`. Command arguments: `--report-authority <reviewed-workspace-relative-file> --report-authority-sha256 <exact-reviewed-grant-hash>`. The future grant is not pre-authorized: its marker, output, expiry and hash must be concrete before trust approval. Proposed probe output is a new `research/gap-05-report-authority-probe.md`; existing file means stop, not overwrite. Read-only report creation only; no append/update, implementation edits or target mutation. Rollback restores only these source changes against the recorded baseline; active command/trust rollback belongs to any later approved probe.

## GAP verification and self-review log

- Initial component RED: current flat MCP was incorrectly compatible. Added supported/unsupported, portable precedence and cross-consumer checks. Additional malformed metadata RED (`version: 1` wrongly present_unverified) fixed; 9 focused resolver/provenance tests passed.
- Source-policy RED: bare Sources headings, lookalike/userinfo/query URLs and missing source_evidence were accepted incorrectly. Exact-host/source-presence/date tests and discovery regressions passed (87 tests).
- B42 local route negative: unrelated business compliance was matched by an overbroad Russian fragment; narrowed to instruction-specific intent. Local provenance/lifecycle/validators passed (93 tests); RU/EN route subset passed (3 tests). M06 and actual model behavior remain not_verified.
- Hook report preflight: direct/nested literal patch accepted only with pinned authority; forged payload, wrong pin/path, terminal/stale/rebound marker, expired/workspace mismatch and unsafe shell commands denied. Wire-format focused tests passed (2 tests). Default no-flag read path remains unchanged.
- Combined focused route: 343 tests, four docs wording failures. Corrected public internal-batch wording and Russian explanatory text; docs rerun 100/100 passed. Tests and thresholds were not weakened.
- First fixture eval returned exit 1 for all 91 records because the renderer treated the hook regex quantifier `{64}` as an unresolved substitution marker. Isolated renderer diagnosis confirmed that single shared cause. Changed to length check plus hex-character regex; active/package source synchronized. Renderer/templates/hooks rerun: 157 tests, 36.539s, OK, exit 0. First broad unittest was interrupted after discovering this cause and is not completion evidence. Final full/fixture reruns use the corrected frozen inputs.
- A diagnostic render attempted in sandbox TEMP hit PermissionError before execution; repeated under the already-authorized isolated host TEMP. No sandbox protection was weakened.
- Transcript eval: 26/26, exit 0, deterministic synthetic sessions; no live model/provider invocation.
- Compatibility validator: exit 1, status needs_review, issue legacy_flat_mcp_requires_schema_review. This unresolved package-format finding is reported, not silently waived; the resolver implementation is evaluated against positive and negative fixtures.
- Initial strict MkDocs preview: exit 0, 22.05s. Ten changed RU/EN preview pages: 1554 local links/anchors, zero errors. First ad-hoc link check assumed directory URLs and failed before checking links; corrected to the repository's use_directory_urls=false, then passed. Mermaid source blocks are unchanged; no browser rendering claim.
- Self-review context_mode=self_review: checked path containment, portable precedence, metadata scalar/schema handling, source URL authority separation, route non-invocation, hook grant pin/task binding, default-route preservation and scope. No independent reviewer was used. Material residuals: bounded schema/YAML subsets, non-atomic hook preflight, current MCP finding, four metadata findings and absent fresh-host evidence.

Final integrated receipt: full unittest 1284 tests in 848.832s, OK (skipped=1), exit 0; fixture eval 91/91 exit 0; transcript 26/26 exit 0. Compatibility exit 1 needs_review remains an explicit package finding. Frozen final implementation/test hashes match after the gate. Inputs: `.docs-tools/reports/gap-verified-inputs.json`; logs use `.docs-tools/reports/gap-*`. No root site update or publication.

## ORD-01–ORD-06 execution — current run 05.11.2026

Lifecycle task ID: `PAOS-ORD-01-06-2026-11-05`.

Status: implemented_locally_verified (ORD-01–ORD-06 only). The owner separately authorized implementation of the first stage only, local checks and RU/EN sync; no publication. The original plan and planning receipts are preserved below. The implementation prohibition in historical planning scope does not apply to separately authorized ORD-01–ORD-06. PAOS-GAP and T30–T34 remain planned, T23–T29 were not reopened.

- Existing capability: read discovery, T26/T27 inputs/validators, runtime state/routes/contracts/guards, renderer/merge boundaries, active/package workflow and existing tests.
- Smallest safe patch: opt-in adapter and explicit legacy fallback; selectors, promotion/model output and package T25 were not rewritten.
- Invariants: no target execution, runtime write authority from JSON, loss of project rules or automatic completed; stale evidence explicitly distinguished.
- Dependency decision: no_new_dependency; stdlib and existing selectors/validators.
- Risk-selected tests: public CLI ordinary/full/invalid/state/unsafe/source-policy/stale/no-op; renderer reuse/stage/user-preservation; existing runtime/template/merge suites.
- Comment decision: docstrings for trust boundaries, provenance and inert commands; untouched existing functions are not rewritten for advisory.
- Performance applicability: not_applicable, no hot-path performance claim; only bounded local check time is measured.
- Evidence and gaps: focused RED/GREEN, final integrated gate and self-review complete; receipts below. Fresh-host activation and GAP-05 report authority are outside closure.

Implementation contract: task_context schema_version=1, required task_id/intent/change_mode/changed_paths/risk_level/risks/acceptance; optional checks, verification_paths, seam/comments, typed full-scope flags, bound state and caller check_results. State binding requires a separate JSON task_id/lifecycle_state plus sha256. In the absence of task state only an explicitly labeled recommendation is used. Caller receipts are not independent execution evidence.

Scope clarification: registry.md and registry.en.md receive only ORD claim/source rows according to AGENTS.md Documentation Rules; this is part of ORD-06 docs sync, not work on GAP-04 source-policy implementation. Local ignored reports contain baseline/check output; root site and docs dependencies remain unchanged.

Initial evidence:

| Check | Result |
| --- | --- |
| Baseline | 2406 existing nonignored files; hashes and owned original text preserved in .docs-tools/reports/ordinary-route-baseline.json |
| First focused run | Exit 1: sandbox TEMP denied; environment failure, not RED feature evidence |
| Retry in isolated TEMP | CLI exit 2: --task-context missing; renderer TypeError: task_context missing; intended RED |
| Initial combined 60 tests | Exit 1: adapter passed incorrect seam reason to T27; docs fixture did not declare check. T27 unchanged; adapter/fixture corrected |
| Focused retest | 3 tests GREEN |
| Negative input shape | Lists/dicts in enum fields caused TypeError; shape guards corrected; 10 tests GREEN |
| Guard RED | Substitution of legacy trace was not rejected; added scoped contract validator and prohibition on completed for contract mode |
| Combined ordinary/renderer | 43 tests, 41.592s, OK; including multi-stack, stage preservation and nested instructions |
| Active workflow | Missing active compact copy reproduced; after ORD-05 parity/local-guard check GREEN |

Current verification ceiling: local synthetic CLI integration; no host/plugin invocation or external service proof.

### Current-run integration evidence and review

Owning implementation/test reviewer: primary agent, `context_mode=self_review`; no independent reviewer or subagent run is claimed. No new dependency was introduced. The full registry and prior public callers remain available; task context is explicitly opt-in.

| Scenario / risk | Current check and result | Evidence owner |
| --- | --- | --- |
| OR-A1: broad route masks small regression | `OrdinaryRouteCliTest.test_ordinary_cli_selects_existing_helpers_without_full_fallback`: public subprocess CLI, both selectors, eight fields, no builder/EVALS requirement, zero target writes | CLI test + ORD-04/06 |
| OR-A2: English headings become authority | RU/EN fixtures produce identical task decisions; task state is separately hash/task-ID bound | CLI tests + state adapter |
| OR-A3: docs forces irrelevant code gates | docs-only strategy is `not_applicable`; existing project checks still win. Report-path hook authorization remains explicitly deferred to GAP-05 | CLI test + ORD-06; GAP-05 owner unchanged |
| OR-A4: low-risk proposal hides sensitive change | high/financial/full cases retain full gates; Windows path regression reproduced three failures, then canonical slash/case/dot-prefix classification fixed it | `test_sensitive_windows_paths_cannot_select_ordinary` + high-risk test |
| OR-A5: staging overwrites user content | API and public CLI dry-run/stage preserve target hashes; full selects eight proposals outside target, ordinary selects none in existing workspace; merge approval/companion tests retained | renderer/CLI/template/merge suites |
| OR-A6: missing data becomes success | malformed schema/types/paths fail clearly; unknown risk/check gaps and stale/conflicting task-state provenance stay explicit | negative CLI cases |
| OR-A7: fabricated verification | synthetic addition defect fails its assertion, minimal fixture fix passes the same test; receipt uses input digest but remains caller-reported, never independent proof or `completed` | isolated regression test |
| OR-A8: legacy incompatibility | old caller signature retained when context is absent; new scoped trace rejects forged legacy fallback. Initial 265-test run caught legacy mock signature mismatch; adapter invocation fixed | legacy CLI/route/result regression suites |
| OR-A9: stale or unsafe command | changed source or verification path invalidates receipt; unsafe command proposal blocked without execution; source-policy blocked is preserved | negative CLI cases |
| OR-A10: unnecessary new code | reuse/configuration/deletion/no-op accepted as modes with explicit invariants/checks; contract runner reports zero touched files | CLI mode cases; T31 quality comparison remains unstarted |

Measured on the same synthetic Python workspace: legacy requires six control-plane inputs and proposes two broad checks; ordinary requires the existing AGENTS.md and TEST.md and proposes one source-backed unit regression command. Legacy infrastructure inventory renders 209 proposals; ordinary reuses the existing workspace and renders zero. Explicit full selection renders eight applicable proposals. These are deterministic counts, not a quality, latency or mass-project usefulness claim. The actual regression remains detectable (RED → GREEN).

Additional current failures and corrections: initial integrated-focused run had one legacy CLI keyword-argument error and one lifecycle task-ID/plan mismatch; both corrected. A new CLI test initially asserted a nonexistent `selected_count` key; the test now checks the actual `selected` list. Sandbox fixture-eval attempt failed before a useful result (`UnboundLocalError` in the existing exception path); isolated authorized TEMP rerun passed without modifying the eval implementation. Neither setup failure is counted as feature RED. The separate platform-skip inspection also encountered sandbox TEMP denial; the same five-test suite was repeated with isolated accessible TEMP. The intentional skip is `test_apply_is_rejected_on_non_windows` with reason `non-Windows guard only`; Windows checks are otherwise applicable.

Current successful commands:

```text
python -B -m unittest tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_guards tests.product_agent_os.test_codex_runtime_runner_fixture_eval tests.product_agent_os.test_infrastructure_renderer tests.product_agent_os.test_render_infrastructure_cli tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_merge_infrastructure tests.product_agent_os.test_batch45_code_quality_behavior tests.product_agent_os.test_batch45_coding_standards tests.product_agent_os.test_task_plan_lifecycle -q
# exit 0; 267 tests, 215.258s. Later reuse/config/deletion + public scoped stage additions: two targeted tests, exit 0, 1.356s.
python -B plugins/product-agent-os/scripts/run_fixture_eval.py
# exit 0; 91 fixture records, no errors
python -B plugins/product-agent-os/scripts/run_transcript_eval.py
# exit 0; passed=26, failed=0
python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py
# exit 0; compatible
.venv-docs/Scripts/python.exe -B -m mkdocs build --strict --site-dir .docs-tools/reports/ordinary-route-preview
# exit 0; 22.43s; root site/ preserved
```

Preview link/anchor check: 10 changed RU/EN pages (four guide pairs plus registry pair), 1616 local links/anchors, zero errors. Existing Mermaid blocks are byte-equivalent as extracted from the pre-slice source baseline; no new diagram or navigation change. Browser/Mermaid runtime rendering was not repeated and is not claimed.

Frozen local verification inputs: Python 3.13.5; 24 implementation/test files plus existing selectors in the manifest `.docs-tools/reports/ordinary-route-verified-inputs.json`; combined manifest SHA-256 `6ab7b949b1b88b3c469ad7e6a4b16b967c5e686406a37e215b5d408e5dfeef11`. This is a reproducibility pointer for a future T32 baseline comparison, not execution of T32 or a promoted model baseline.

Intermediate full gate: `python -B -m unittest discover -s tests -p "test_*.py" -q`, exit 0; 1270 tests, 729.488s, OK (skipped=1). Final integrated gate: python -B -m unittest discover -s tests -p "test_*.py" -q — 1272 tests, 753.848s, OK (skipped=1), exit 0. Earlier full-suite run started before the final Windows-path correction and is retained only as intermediate evidence; the successful final full run was started after all code/test changes. Focused module evidence is not substituted for the mandatory final full gate.

Final post-sync docs gate: python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q — 100 tests, 3.492s, exit 0; python -B tools/check_docs.py — exit 0; python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md — ok; python -B plugins/product-agent-os/scripts/validate_task_state_consistency.py . — ok; git diff --check — exit 0 (existing CRLF normalization notices only).

Final preservation check before terminal marker: 27 existing owned files changed and two new files (task_routing.py and active code-change-contract.md); 2367 out-of-scope file hashes unchanged, including 660 root site files. All 11 later task blocks are text-identical to the saved plan baseline; frozen implementation/test hashes match the final full gate. T23–T29 source implementation and task-group JSON were not changed. Receipt: .docs-tools/reports/ordinary-route-preservation.json.

Control-plane sync: PLAN.md, RUNLOG.md and TEST.md updated with current ORD pointers; REQUIREMENTS.md `not_applicable` (accepted scope unchanged), EVALS.md `not_applicable` (no rubric/threshold/promotion change), prod_test.md `not_applicable` (Batch 39 historical family out of scope). No overflow/refactor required; no ownership handoff required within ORD. Source registry pair receives only ORD provenance entries. Host activation, GAP-05 and all later tasks retain their own gates.

Review findings resolved: executable-seam adapter invariant, malformed enum types, forged legacy trace/result-completion claims, old CLI call compatibility, current plan ID, and sensitive Windows path normalization. Remaining limitations are deliberate: command extraction is conservative and cannot interpret arbitrary project instructions; instruction reads remain mandatory. Task declarations/receipts are proposals, not trusted truth. Digest covers declared changed/verification files, manifests and check/instruction sources, not the entire environment. No automatic executor, provider, promotion or fresh-host activation is claimed.

## Decision and boundary

Start with the end-to-end ordinary route, reusing T25–T27. Then address remaining discrepancies IMP-04–IMP-09 and continue the existing B45-CQRR-T30–T34 queue. T23–T29 are not reopened. New PAOS-ORD and PAOS-GAP IDs denote only this plan's integration and corrective tasks; they do not replace existing Batch IDs.

When saving the plan, only this Markdown and the lifecycle marker were authorized. At that point code, tests, prompts, hooks, configuration, original report, PLAN/RUNLOG, task-group JSON, site and installed cache were unchanged. Saving the plan did not authorize task execution, publication, target apply, provider/model/reviewer calls or trust changes.

First useful outcome: for a bounded bugfix in an existing project, the system reads real sources, selects already implemented stack/risk selectors, produces a compact contract and justified checks, reuses existing documents, and shows actual evidence/gaps. Absence of EVALS.md or builder.toml alone does not send the task through onboarding again. Project-specific mandatory rules remain mandatory.

## Sources and currency

- [Report with IMP-01–IMP-11](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-docs-implementation-gap-analysis-2026-11-05.md).
- [Current B45 task group](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/batch45-code-quality-runtime-recovery-task-group.json): owner of machine status and T23–T34 dependencies.
- [Latest B45 implementation/evidence pointer](2026-08-17-product-agent-os-loop-remediation.md).
- [T25–T27, compact authoring](2026-08-11-batch45-s9-b-compact-authoring-runtime.md).
- [B42 compliance matrix](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json).
- [GPT-6/lifecycle receipts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/gpt6-documentation-refresh-task-group.json).
- [PLAN](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/PLAN.md), [RUNLOG](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/RUNLOG.md), [TEST](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/TEST.md), [EVALS](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/EVALS.md).
- [Canonical implementation-planner](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/skills/implementation-planner/SKILL.md).

Current code seams were reread while preparing the plan: templates/infrastructure, state/context_loader/routes/cli, contracts/guards, T26/T27 inputs and B45 task group. Historical test counts below are receipts from previous implementation, not new results of this run. External claims rely on official sources verified in the 2026-11-05 report; no new external research was performed while planning. Recheck sources when implementing format/host-sensitive compatibility.

## Baseline before ORD

| Task | Source-owned JSON state | Use in the plan | What this status does not prove |
| --- | --- | --- | --- |
| T23 | locally_implemented_focused_verified | promotion_contract.py and model_output.py are a single durable output contract | Validity of future live outputs |
| T24 | locally_implemented_focused_verified | Preserve schema/normalization and seeded-corruption regression fixtures | New end-to-end integration |
| T25 | locally_implemented_focused_verified | Reuse eight code-change-contract fields and packaged coding workflow | Active workspace not yet migrated |
| T26 | locally_implemented_focused_verified | ProjectInventory → select_code_quality_profile; add adapter/caller | Production routing does not yet use selector |
| T27 | locally_implemented_focused_verified | TestStrategyRequest → select_test_strategy; use decisions in route | Execution of selected checks and correctness of evidence |
| T28 | locally_implemented_focused_verified | Preserve fault detection and compacted test structure | Not a reason to reduce tests again for quantity |
| T29 | locally_implemented_focused_verified | Typed deterministic metrics and promotion wrapper underpin T30/T33 | Reviewer independence and live evidence provenance |

T28 receipt: 196 → 34 repeated families, 3 owned exceptions, combined test LOC 8130 → 5658, 48 focused tests. T29 receipt: 23 focused tests. Repeat these suites when their contract is affected or the relevant gate applies, not for every plan edit. Older unchecked boxes do not override newer receipts. ACT-F1–F6 are not reopened: the new bounded report authority task is a separate IMP-09 case.

## Order and dependencies

| Stage | Tasks | Outcome / exit gate |
| --- | --- | --- |
| 1. End-to-end ordinary route | PAOS-ORD-01 → 02 → 03 → 04 → 05 → 06 | Real CLI contract path + bounded fixture journey + explainable evidence; current local integration, no host activation claim |
| 2. Remaining discrepancies | PAOS-GAP-01, 02, 03, 04, 05 | Consistent pointers/claims, component inventory, B42 provenance, source policy; hook change is a separate approval scope |
| 3. Independent evaluation | T30 and T31 → T32 → T33 | Blinded reviewer, frozen corpus, one intervention, local preflight |
| 4. Authorized experiment | T34 only after T33 and new exact approval | Promotion/no-go from valid pairs and independent findings |
| 5. User outcome | PAOS-GAP-06 after ORD-06 and B42 evidence for selected surface | B39/B44 owner feedback, usefulness and manual learning; no automatic promotion |

This is the preferred execution order, not new B45 technical dependencies. T30 depends on T29; T31 on T27 and T29. T31 does not depend on T30. T32 depends on T25/T30/T31. T33 depends on T24/T28/T29/T30/T31/T32. T34 depends on T33. Freeze the ordinary-route baseline identically for both arms before T32; otherwise the new routing becomes a second hidden intervention. Do not mix B42/hook/cache changes with the experiment.

One executor by default; roles in tasks are ownership and handoff, not permission to launch subagents. Shared cli/routes/contracts and control-plane files are edited sequentially. T30/T31 may be prepared independently with separately assigned boundaries; this plan does not launch a parallel team.

## Proposed ordinary route contract

Architectural boundaries:
1. Discovery reads the workspace and returns signal provenance; it does not execute discovered commands.
2. New small adapter product_agent_os/task_routing.py maps inventory and task context to existing ProjectInventory / TestStrategyRequest. Pure T26/T27 selectors retain their responsibility.
3. state.py separates structural readiness, authoritative task state and inferred recommendation. Task-group status is not a lifecycle enum: completed T29 does not imply release_ready.
4. templates.py selects a registry subset by task scope and applicability; infrastructure.py retains dry-run/stage/managed-section/companion/merge boundaries.
5. routes.py forms required context, compact authoring, selected verification and reasons. CLI contract mode only plans and reports; it does not become a universal executor.
6. Codex performs authorized work and selected checks; evidence reflects actual command, exit, checked input digest and gaps. Route-ready is not task-completed.

Proposed task context v1: task_id, intent/change_mode, changed_paths, risks with protected invariants and provenance, explicit lifecycle state with source ref if present, approval scope. These are routing data, not authority. Unknown risk is not automatically reduced to low. Invalid/conflicting state → needs_context with one specific reason; unverified tools → present_unverified. Explicit state cannot bypass approval or source guards.

Compatibility: add opt-in structured task context to CLI and Python API, preserving existing calls. An old call without task context uses explicitly labeled legacy fallback, without claiming ordinary route activated. A successful ordinary check must show mode/selector/version/source/reason and absence of broad fallback. Unknown/new contract version yields a clear error, not silent downgrade.

Minimum artifacts:
- Existing project: reuse current files; compact contract and evidence may be sections in an existing task artifact, without requiring a new file set.
- Docs-only: source/link/text checks matched to the change; code-change contract and behavioral tests are not_applicable with reason if behavior is unaffected.
- Empty project: discovery and needed scope/acceptance; do not claim build-ready when requirements are missing.
- High-risk/financial/release/explicit full packet: full reporting and all applicable risk/approval gates. Full does not mean automatically generating all 209 templates, agents, hooks and automation candidates.
- Existing user files and project-mandated checks take precedence over convenience of a minimal route. In this repository mandatory TEST.md/AGENTS.md gates are not removed by a new selector.

## End-to-end acceptance scenarios

| ID | Given / When | Then and verifiable evidence | Owner / task |
| --- | --- | --- | --- |
| OR-A1 | Existing Python project; one pure-function regression; invariant and test seam known | Real CLI invokes T26/T27, selects regression/unit seam; does not require EVALS/builder; compact ≤8 fields; trace shows ordinary without full fallback | tester / ORD-02,04,06 |
| OR-A2 | Equivalent RU and EN structure, identical task context | Same route and reasons; English headings are not authority; single-agent allowed | tester / ORD-02,04 |
| OR-A3 | Docs-only with authorized output | No code tests/benchmark without reason; target writes remain prohibited. Special report-path authority is checked only after GAP-05 | tester / ORD-04; security reviewer / GAP-05 |
| OR-A4 | Authorization/data-loss/security/financial/release risk | Required negative/contract checks and full reporting retained; unsupported low-risk hint does not override risk | reviewer / ORD-01,04,06 |
| OR-A5 | Existing unmarked AGENTS/config/hooks and repeated dry-run | User hashes unchanged; companion proposals; stable selected manifest; target apply requires prior plan-bound approval | tester / ORD-03 |
| OR-A6 | No risk/command information; malformed task state or contradictory sources | needs_context/blocked with specific gap; no invented command, auto-install or success | tester / ORD-02,04 |
| OR-A7 | Baseline fixture contains known defect; selected regression check runs in isolated synthetic workspace | RED on intended assertion → minimal GREEN; evidence tied to final inputs; skipped/not_run does not become passed | tester / ORD-06 |
| OR-A8 | Legacy caller without new task context and high-risk fixture | Compatibility preserved; legacy fallback visible; ordinary activation not claimed | tester / ORD-04,06 |
| OR-A9 | Stale check receipt, changed source digest, unsafe shell command found | Stale/present_unverified/blocked, without executing command from untrusted text | security reviewer / ORD-04,06 |
| OR-A10 | Valid reuse/config/deletion/no-op decision | No code created for a score; outcome accepted by acceptance and invariant | tester / ORD-06, T31 |

OR-A7 verifies the connection of the production entry point and local synthetic fixture behavior; it does not replace fresh Codex host acceptance. A claim of current active workflow/skill loading requires a newly authorized session with provenance and observed path. Text edits alone do not prove it.

## General rules for executing future tasks

- All commands in task blocks are commands_to_run, not results of this run. First obtain observable RED for changed behavior, then minimal GREEN; docs-only changes are checked statically.
- Each block has its exact owned files set. Shared additional ownership of each future implementation slice: only its Completion Report in this plan and corresponding compact PLAN.md, RUNLOG.md, TEST.md records; one root writer, sequential updates. Those shared paths and block-listed files form the full scope. Other existing files are prohibited without a visible scope clarification; new files are marked proposed. Extend an existing test module when it owns the risk; do not create one test per field/word.
- Rollback: preserve baseline diff/hashes before the slice; revert only that slice's hunks, preserve others' changes. Preserve previous active workflow sections; retain legacy API compatibility for task context. Do not use destructive Git.
- For each completed implementation slice record current evidence in its owning artifact, update only its owned status and synchronize compact PLAN/RUNLOG pointers. This plan is not a new machine-status registry for T23–T34.
- Mandatory integrated gate once on the combined implementation state: `python -m unittest discover -s tests -p "test_*.py" -v`; `python plugins/product-agent-os/scripts/run_fixture_eval.py`; `python plugins/product-agent-os/scripts/run_transcript_eval.py`; `python plugins/product-agent-os/scripts/validate_codex_compatibility.py`; docs gate and diff. Expected exit 0; disclose skips and incompatibilities. Repeat only when relevant inputs change, a check fails or risk remains unresolved.
- Docs gate: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`, `python tools/check_docs.py`, `git diff --check`. Update named RU/EN pairs together. For changed source-backed claims, update registry.md and registry.en.md in the same slice.
- For nav/Mermaid/generated-site evidence changes: `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/ordinary-route-preview` after local build approval; links/anchors and diagram rendering through existing docs tooling. Do not install dependencies or publish.
- Documentation fields in each block identify a specific docs owner/path; requirements, scenarios, architecture decision, quality strategy and rollback reside here, so duplicate methodology packets are unnecessary.
- FSD, cloud architecture, DB migration and deployment: not_applicable, no such changes. Domain ownership is described above (discovery, routing, infrastructure, evidence); no separate DDD framework needed. Product hypothesis: reduce unnecessary preparation without harming correctness; ORD-06 checks local behavior, GAP-06 user outcomes. Marketing/release success remains not_verified.
- Professional authoring: reuse selectors, stdlib dataclasses/json/pathlib and existing validators; do not add dependencies, hosted runner or generator framework. Adapter is preferred over selector reimplementation; full-only leaves IMP-01/02, silent heuristic-only inference leaves IMP-03.

## Readiness, limitations and Control-Plane Sync

Historical status when saving the plan: proposal_saved. Current ORD-01–06 execution and new receipts appear at the start of the document. T30–T33 remain planned_not_started, T34 approval_required_not_started. The planned field in task_matrix_plan_v1 does not remove external approval gates.

Plan quality: exact owned files, proposed paths, acceptance, commands, expected outcomes, rollback and evidence owners are specified. FSD/DB/cloud/deployment are not_applicable. Architecture and requirements traceability are represented in this document rather than duplicate packets. Implementation/host verification is present_unverified; hook trust, live eval and target pilot are approval_required. Later transport/design gaps T32 and target scope GAP-06 block the respective executions, but not a separate ORD-01 start after an implementation request. The entire program is not unconditionally declared plan_ready.

ORD-01–06 estimate: 5–10 engineering working days sequentially, excluding approval waits and new environment blockers. This is a planning range, not a promised deadline or measured agent time. Revisit after the first vertical slice without adding mandatory stages merely for estimation.

Review mode of this plan: self_review. IMP-01–IMP-11, original IDs, T23–T29 status, T30–T34 dependencies, ordinary/full boundaries, file existence and no-provider/target boundaries checked. No independent reviewer or subagents in this run. Static structure checks do not prove future runtime quality.

| Control-plane file | Decision in this run | Handoff |
| --- | --- | --- |
| REQUIREMENTS.md | not_applicable | New implementation acceptance proposed here; current product unchanged |
| PLAN.md | handoff_required | Upon ORD-01 acceptance the lifecycle-orchestrator adds a compact pointer; B45 next=T30 remains a separate queue |
| TEST.md | handoff_required | Commands here proposed; actual implementation receipts added by ORD-06/T33 owners |
| EVALS.md | handoff_required | New reviewer/corpus/design gates recorded in T30–T32; rubrics unchanged now |
| RUNLOG.md | handoff_required | Current scope covers only new plan and marker; add brief pointer at implementation start |
| prod_test.md | not_applicable | B39 evidence unchanged; future GAP-06 separately scoped |
| registry RU/EN | not_applicable | No new external factual claims on site; future changes included in GAP-01/02/04 |
| site / MkDocs | not_applicable | Plan is outside docs navigation; site is not rebuilt and freshness is not claimed |

This document does not change source-owned machine statuses or close future tasks. Completion Report with planned status and pending_execution_timestamp is the required honest record of unfinished work. On the next request start with ORD-01; do not mix ordinary routing, hook/cache/model changes and promotion eval in one slice.

## Plan checks in the current run

Checked 2026-11-05, current run:

| Check | Command / method | Observed result |
| --- | --- | --- |
| Task matrix | `python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md` | Exit 0, ok=true, errors=[], task_matrix_plan_v1 |
| Docs contracts | `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | Exit 0, Ran 100 tests in 4.126s, OK |
| Docs structure | `python -B tools/check_docs.py` | Exit 0, documentation structure checks passed |
| Diff hygiene | `git diff --check` | Exit 0; Git CRLF/LF notices only, no whitespace errors |
| Source/dependency check | Read-only Python: Markdown scopes and source-owned B45 JSON | 17 unique tasks; T30–T34 dependencies match; 110 references to existing owned paths with none missing; proposed files identified separately |
| Links/text integrity | Read-only Python: local Markdown links, UTF-8, fences | 11 local links exist; U+FFFD absent; fences balanced |
| Preservation | SHA-256 over sorted Git tracked/nonignored untracked paths, excluding only new plan and marker | 2404 prior files: baseline and repeat check match, aggregate `feada09754aa46ffbfa5dc8b3b602eb7667cd4a9b5761257329ace52d7d0a95b` |

The first long shell save through a helper exited 1 in Windows MSIX launcher before Python ran; the write used apply_patch and separately passed the standard matrix validator. No lifecycle/sandbox bypass or environment change. Implementation commands in task blocks were not run. Implementation state, source-owned task group, source report and site were preserved; the check excludes ignored ephemeral runtime files and is not runtime/product acceptance.

## Detailed tasks

### Task `PAOS-ORD-01`

- Task: Establish the end-to-end ordinary route contract and reproduce gaps
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Saved plan; separate owner request authorizing only ORD-01–ORD-06 implementation
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 15:42
- Depends on: T25, T26, T27 — locally completed; IMP-01/02/03 report
- Blocks: PAOS-ORD-02, 03, 04
- Source: IMP-01, IMP-02, IMP-03; current state/routes/cli and selectors
- Short description: Reproduce OR-A1/A2/A4/A5/A6 in existing tests using compact synthetic fixtures. Specify task context v1, risk precedence, legacy fallback, authority vs evidence and exact expected selected artifact set in this plan. Record baseline response and extra required inputs; do not change production code during RED.
- Technical value: A visible reproducible problem instead of another layer of declarations.
- Product value: A visible reproducible problem instead of another layer of declarations.
- Scope: Owned files: `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`; `tests/product_agent_os/test_codex_runtime_runner_cli.py`; `tests/product_agent_os/test_infrastructure_renderer.py`; `docs/planning/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Contract and RED evidence in this plan; docs owner architect. No new task group for existing B45 tasks.
- Acceptance criteria: RED must reflect missing ordinary behavior, not import/setup error. Contract covers ordinary/docs/high-risk/unknown, RU/EN and no-builder. Acceptance maps risk → scenario → test → evidence owner; no hidden provider or host requirement.
- Verification gates: python -m unittest tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_infrastructure_renderer -v — expect specified RED ordinary assertions, existing unrelated cases remain GREEN; temporary RED checkpoint, not completion of integration.
- Risks / approval gates: Do not weaken existing tests for RED; if authority is ambiguous stop dependent build until contract resolution. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: medium
- Estimated execution time: 0.5–1 working day
- Agents: architect; evidence owner: tester; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Contract and RED evidence in this plan; docs owner architect. No new task group for existing B45 tasks.
- Next step: ORD-02; RED cases are closed before ORD-06.

#### Completion Report

- status: implemented
- what was done: Defined task_context v1 and OR-A1–A10; reproduced missing CLI/renderer contract and targeted negative regressions.
- files touched / work locations: tests/product_agent_os/test_codex_runtime_runner_cli.py; tests/product_agent_os/test_infrastructure_renderer.py; current plan
- technical value delivered: Reproducible risk/scenario/check mapping.
- product value delivered: Verifiable ordinary task without repeat onboarding.
- actual implementation date and time: 05-11-2026 15:42
- verification evidence: Final full unittest: 1272 tests, 753.848s, OK (skipped=1), exit 0; focused 267 OK + two later acceptance cases OK; fixture 91; transcript 26/26; compatibility compatible; docs 100 OK; check_docs/task matrix/state consistency/diff exit 0; strict isolated preview and 1616 local links/anchors OK. Exact commands/RED-GREEN: current-run evidence above.
- residual risks: Fresh Codex host/workflow activation not_verified; OR-A3 report-path hook portion deferred to GAP-05; no provider/model/promotion proof.
- follow-up: No remaining ORD implementation. Later PAOS-GAP/T30–T34 remain unstarted; T23–T29 preserved.

### Task `PAOS-ORD-02`

- Task: Connect discovery to existing selectors and separate task state from readiness
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Saved plan; separate owner request authorizing only ORD-01–ORD-06 implementation
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 15:42
- Depends on: PAOS-ORD-01; T26/T27
- Blocks: PAOS-ORD-03, PAOS-ORD-04
- Source: IMP-02/03
- Short description: Add a small validated adapter: audit inventory → ProjectInventory, task risks → TestStrategyRequest; call select_code_quality_profile/select_test_strategy without copying their logic. Pass source refs and present_unverified. In state resolver separate structural readiness, explicit task state and recommendation; accept only known values with verified task/source binding. Do not read latest RUNLOG substring as authoritative state; do not require builder for single-agent.
- Technical value: Real data drive existing selectors; a Russian single-agent project does not return to onboarding.
- Product value: Real data drive existing selectors; a Russian single-agent project does not return to onboarding.
- Scope: Owned files: `plugins/product-agent-os/scripts/product_agent_os/task_routing.py [proposed]`; `plugins/product-agent-os/scripts/codex_runtime_runner/state.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/context_loader.py`; `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Typed routing context and state provenance; docs owner architect, architecture contract in this plan, public pages in ORD-06.
- Acceptance criteria: OR-A2/A6 pass. Equivalent RU/EN data yield the same decision; stale/conflicting state does not become build/release. Source-owned T29 status is not directly converted into a lifecycle enum. Unknown risk cannot default to low. T26/T27 behavior regressions GREEN.
- Verification gates: python -m unittest tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_batch45_code_quality_behavior -v — exit 0; parameterized malformed, provenance, unknown-risk and RU/EN cases.
- Risks / approval gates: No execution of discovered project commands; reject paths outside workspace and unsupported schema version. Preserve legacy infer_lifecycle_state signature or add compatible wrapper. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: high
- Estimated execution time: 1–2 working days
- Agents: plugin-runtime-builder; review: architect; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Typed routing context and state provenance; docs owner architect, architecture contract in this plan, public pages in ORD-06.
- Next step: ORD-03 and then ORD-04, one writer for shared contracts.

#### Completion Report

- status: implemented
- what was done: Discovery connected to existing T26/T27; structural readiness separated from hash/task-bound state and explicitly non-authoritative recommendation.
- files touched / work locations: plugins/product-agent-os/scripts/product_agent_os/task_routing.py; plugins/product-agent-os/scripts/codex_runtime_runner/state.py; tests/product_agent_os/test_codex_runtime_runner_cli.py
- technical value delivered: Selectors reused; RU/EN, malformed/unknown/stale handling.
- product value delivered: Small known task does not require builder/EVALS; uncertainty remains a gap.
- actual implementation date and time: 05-11-2026 15:42
- verification evidence: Final full unittest: 1272 tests, 753.848s, OK (skipped=1), exit 0; focused 267 OK + two later acceptance cases OK; fixture 91; transcript 26/26; compatibility compatible; docs 100 OK; check_docs/task matrix/state consistency/diff exit 0; strict isolated preview and 1616 local links/anchors OK. Exact commands/RED-GREEN: current-run evidence above.
- residual risks: Fresh Codex host/workflow activation not_verified; OR-A3 report-path hook portion deferred to GAP-05; no provider/model/promotion proof.
- follow-up: No remaining ORD implementation. Later PAOS-GAP/T30–T34 remain unstarted; T23–T29 preserved.

### Task `PAOS-ORD-03`

- Task: Select minimally sufficient infrastructure artifacts
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Saved plan; separate owner request authorizing only ORD-01–ORD-06 implementation
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 15:42
- Depends on: PAOS-ORD-01, PAOS-ORD-02
- Blocks: PAOS-ORD-04, PAOS-ORD-06
- Source: IMP-01
- Short description: Preserve the full template registry and legacy caller contract. Add selection by task context separately from project profile; show selected/omitted/reason in plan manifest. Existing-project ordinary reuse does not create a full package. For new requirements select applicable artifacts only; full risk does not activate hooks/automation. Carry selection through dry-run and stage, preserving current protections.
- Technical value: Fewer unnecessary documents while retaining governed staging and rollback.
- Product value: Fewer unnecessary documents while retaining governed staging and rollback.
- Scope: Owned files: `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`; `plugins/product-agent-os/scripts/render_infrastructure.py`; `tests/product_agent_os/test_infrastructure_templates.py`; `tests/product_agent_os/test_infrastructure_renderer.py`; `tests/product_agent_os/test_render_infrastructure_cli.py`; `tests/product_agent_os/test_merge_infrastructure.py`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Selection manifest and reasoned exclusions; docs owner docs-maintainer, artifact-contracts RU/EN updated in ORD-06.
- Acceptance criteria: OR-A5 GREEN: dry-run changes no user-authored byte; repeated manifest deterministic; stage outside target; unmarked files produce companion. Ordinary has no auto-added agents/hooks/automations; high-risk includes required gates. Legacy all-template inventory remains explicitly available without ordinary activation claim. Existing merge approval binding is not weakened.
- Verification gates: python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_infrastructure_renderer tests.product_agent_os.test_render_infrastructure_cli tests.product_agent_os.test_merge_infrastructure -v — exit 0; synthetic temporary targets created by tests. Native dry-run/stage paths checked through public CLI test; target apply not performed.
- Risks / approval gates: Do not change merge engine semantics for selection convenience; changing selected manifest invalidates prior approval. Bulk deletion of templates prohibited. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: medium-high
- Estimated execution time: 1–2 working days
- Agents: plugin-runtime-builder; evidence owner: tester; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Selection manifest and reasoned exclusions; docs owner docs-maintainer, artifact-contracts RU/EN updated in ORD-06.
- Next step: ORD-04.

#### Completion Report

- status: implemented
- what was done: Task-scoped selection manifest: ordinary reuse, full eight proposals, legacy 209; staging with gaps is prohibited and remains outside target.
- files touched / work locations: plugins/product-agent-os/scripts/product_agent_os/templates.py; plugins/product-agent-os/scripts/product_agent_os/infrastructure.py; plugins/product-agent-os/scripts/render_infrastructure.py; tests/product_agent_os/test_infrastructure_renderer.py; tests/product_agent_os/test_render_infrastructure_cli.py
- technical value delivered: Deterministic artifact selection; merge/companion/approval contracts preserved.
- product value delivered: No unnecessary agents/hooks/automations or overwriting user files.
- actual implementation date and time: 05-11-2026 15:42
- verification evidence: Final full unittest: 1272 tests, 753.848s, OK (skipped=1), exit 0; focused 267 OK + two later acceptance cases OK; fixture 91; transcript 26/26; compatibility compatible; docs 100 OK; check_docs/task matrix/state consistency/diff exit 0; strict isolated preview and 1616 local links/anchors OK. Exact commands/RED-GREEN: current-run evidence above.
- residual risks: Fresh Codex host/workflow activation not_verified; OR-A3 report-path hook portion deferred to GAP-05; no provider/model/promotion proof.
- follow-up: No remaining ORD implementation. Later PAOS-GAP/T30–T34 remain unstarted; T23–T29 preserved.

### Task `PAOS-ORD-04`

- Task: Connect ordinary decision to real CLI, route and result contracts
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Saved plan; separate owner request authorizing only ORD-01–ORD-06 implementation
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 15:42
- Depends on: PAOS-ORD-02, PAOS-ORD-03; T25/T26/T27
- Blocks: PAOS-ORD-05, PAOS-ORD-06
- Source: IMP-01/02/03
- Short description: Add opt-in --task-context JSON and corresponding Python parameter; validate schema, source refs and workspace containment. Form route from adapter outputs. _status_for checks missing required inputs of selected route, not all six. Return compact contract, quality strategy, command provenance/applicability and routing trace. Contract-mode does not execute commands or alter target. Evidence statuses distinguish recommended/detected/executed/stale.
- Technical value: First genuinely connected discovery → selectors → route → result path.
- Product value: First genuinely connected discovery → selectors → route → result path.
- Scope: Owned files: `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/guards.py`; `tests/product_agent_os/test_codex_runtime_runner_cli.py`; `tests/product_agent_os/test_codex_runtime_runner_contracts.py`; `tests/product_agent_os/test_codex_runtime_runner_guards.py`; `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Production caller and machine-readable reasons/evidence gaps; docs owner docs-maintainer, cli-reference RU/EN in ORD-06.
- Acceptance criteria: OR-A1/A2/A4/A6/A8/A9 GREEN through public CLI, not only direct selector calls. Trace includes ordinary/legacy path and selector provenance; ordinary is not masked by full fallback. Full checklist remains reference; ≤8 compact fields. Mandatory project checks and approval guards take precedence; blocked source policy remains blocked. Existing result consumers retain compatibility or receive explicitly versioned contract error.
- Verification gates: python -m unittest tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_guards tests.product_agent_os.test_codex_runtime_runner_state_routes -v — exit 0; one public subprocess CLI case with validated structured context and negative legacy-fallback detector.
- Risks / approval gates: Do not treat allow_workspace_writes or approval_status from input JSON as authority. Do not add command executor; unknown/unsafe command remains proposal or blocked. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: high
- Estimated execution time: 1–2 working days
- Agents: plugin-runtime-builder; evidence owner: tester; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Production caller and machine-readable reasons/evidence gaps; docs owner docs-maintainer, cli-reference RU/EN in ORD-06.
- Next step: ORD-05, then ORD-06.

#### Completion Report

- status: implemented
- what was done: Public --task-context connected to route/result guards, trace, compact contract, risk checks and freshness receipts; sensitive Windows paths normalized.
- files touched / work locations: plugins/product-agent-os/scripts/codex_runtime_runner/cli.py; plugins/product-agent-os/scripts/codex_runtime_runner/routes.py; plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py; plugins/product-agent-os/scripts/codex_runtime_runner/guards.py; tests/product_agent_os/test_codex_runtime_runner_cli.py
- technical value delivered: Legacy compatibility; forged fallback/completed rejected.
- product value delivered: Explicit route reasons, selected checks and gaps without executing untrusted commands.
- actual implementation date and time: 05-11-2026 15:42
- verification evidence: Final full unittest: 1272 tests, 753.848s, OK (skipped=1), exit 0; focused 267 OK + two later acceptance cases OK; fixture 91; transcript 26/26; compatibility compatible; docs 100 OK; check_docs/task matrix/state consistency/diff exit 0; strict isolated preview and 1616 local links/anchors OK. Exact commands/RED-GREEN: current-run evidence above.
- residual risks: Fresh Codex host/workflow activation not_verified; OR-A3 report-path hook portion deferred to GAP-05; no provider/model/promotion proof.
- follow-up: No remaining ORD implementation. Later PAOS-GAP/T30–T34 remain unstarted; T23–T29 preserved.

### Task `PAOS-ORD-05`

- Task: Synchronize active and packaged compact authoring workflow
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Saved plan; separate owner request authorizing only ORD-01–ORD-06 implementation
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 15:42
- Depends on: PAOS-ORD-04; T25
- Blocks: PAOS-ORD-06
- Source: IMP-02; active/package mismatch
- Short description: Apply completed T25 compact contract to active copy, retaining mandatory project-specific rules. Full reference checklist is not injected by default. Specify ordinary authoring, high-risk gates and full lifecycle reporting separately. Sync packaged wording only for actual semantic mismatch; do not rewrite T25.
- Technical value: Current workspace operator receives the same compact process already provided by the package.
- Product value: Current workspace operator receives the same compact process already provided by the package.
- Scope: Owned files: `.codex/workflows/coding-standards.md`; `.codex/artifact-templates/code-change-contract.md [proposed]`; `plugins/product-agent-os/assets/templates/workflows/coding-standards.md`; `plugins/product-agent-os/assets/templates/artifact-templates/code-change-contract.md`; `tests/product_agent_os/test_batch45_coding_standards.py`; `tests/product_agent_os/test_task_plan_lifecycle.py`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Active compact artifact and aligned workflow; preservation diff with local-rule inventory.
- Acceptance criteria: Active and staged workflow select compact generation identically. No local approval/test/source guard lost. Static tests and synthetic transcript cases cover ordinary/high-risk/not-applicable context. File changes are not recorded as fresh-session activation.
- Verification gates: python -m unittest tests.product_agent_os.test_batch45_coding_standards tests.product_agent_os.test_task_plan_lifecycle -v; python plugins/product-agent-os/scripts/run_transcript_eval.py — exit 0; docs gate. Fresh-host invocation only through a separately authorized check; until then implemented_locally_verified.
- Risks / approval gates: Durable instruction change: baseline contexts and intent documented before edits. .codex filesystem approval remains applicable. Do not change hooks/trust/config or installed cache. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: medium
- Estimated execution time: 0.5–1 working day
- Agents: architect; docs owner: docs-maintainer; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Active compact artifact and aligned workflow; preservation diff with local-rule inventory.
- Next step: ORD-06.

#### Completion Report

- status: implemented
- what was done: Active coding workflow uses eight-field contract by default; full checklist remains reference. Local guards and packaged T25 retained.
- files touched / work locations: .codex/workflows/coding-standards.md; .codex/artifact-templates/code-change-contract.md; tests/product_agent_os/test_batch45_coding_standards.py
- technical value delivered: Static active/staged parity without changes to hooks/trust/cache.
- product value delivered: Short pre-edit contract retains applicable checks and lifecycle.
- actual implementation date and time: 05-11-2026 15:42
- verification evidence: Final full unittest: 1272 tests, 753.848s, OK (skipped=1), exit 0; focused 267 OK + two later acceptance cases OK; fixture 91; transcript 26/26; compatibility compatible; docs 100 OK; check_docs/task matrix/state consistency/diff exit 0; strict isolated preview and 1616 local links/anchors OK. Exact commands/RED-GREEN: current-run evidence above.
- residual risks: Fresh Codex host/workflow activation not_verified; OR-A3 report-path hook portion deferred to GAP-05; no provider/model/promotion proof.
- follow-up: No remaining ORD implementation. Later PAOS-GAP/T30–T34 remain unstarted; T23–T29 preserved.

### Task `PAOS-ORD-06`

- Task: Complete end-to-end local ordinary acceptance and RU/EN documentation
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Saved plan; separate owner request authorizing only ORD-01–ORD-06 implementation
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 15:42
- Depends on: PAOS-ORD-01–05
- Blocks: Freeze ordinary baseline for T32; PAOS-GAP-06
- Source: IMP-01/02/03; OR-A1–A10
- Short description: Run public CLI on synthetic existing Python project: reproduce bug → task context → ordinary selectors → compact output → bounded local fix/check → final evidence. Use TemporaryDirectory and standard subprocess tests; no real target writes. Check RU/EN, docs-only, single-agent, high-risk, no-op and stale result. Record positive selector activation and negative full-fallback proof. Sync user pages and current pointers without rewriting historical receipts.
- Technical value: Completed local user journey with evidence instead of separate functions alone.
- Product value: Completed local user journey with evidence instead of separate functions alone.
- Scope: Owned files: `tests/product_agent_os/test_codex_runtime_runner_cli.py`; `tests/product_agent_os/test_codex_runtime_runner_fixture_eval.py`; `docs/product-agent-os/cli-reference.md`; `docs/product-agent-os/cli-reference.en.md`; `docs/product-agent-os/artifact-contracts.md`; `docs/product-agent-os/artifact-contracts.en.md`; `docs/product-agent-os/coding-standards.md`; `docs/product-agent-os/coding-standards.en.md`; `docs/product-agent-os/architecture.md`; `docs/product-agent-os/architecture.en.md`; `PLAN.md`; `RUNLOG.md`; `TEST.md`; `docs/planning/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: This plan's Completion Report, compact PLAN/RUNLOG/TEST pointers; RU/EN parity. Frozen runner baseline data for T32.
- Acceptance criteria: All OR scenarios in applicable local scope GREEN; OR-A3 path-specific hook part explicitly belongs to GAP-05. Final result contains selected tests with risk reasons, actual exit/result/digest; no-op accepted on correctness. Excess artifact/check counts reduced on same fixtures without loss of fault detection; these are local measurements, not a time/quality promise across projects. Mandatory integrated gate GREEN; host activation separately not_verified.
- Verification gates: python -m unittest tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_codex_runtime_runner_fixture_eval -v — exit 0; then mandatory integrated gate from section above once and docs gate. Strict MkDocs preview only when diagram/navigation affected or build scope authorized.
- Risks / approval gates: Stop closure on failed guard, stale evidence or masked fallback. Do not claim product release-ready, behavioral promotion or host workflow activation. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: medium-high
- Estimated execution time: 1–2 working days
- Agents: tester; docs owner: docs-maintainer; final review: completion-skeptic or explicit self_review; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: This plan's Completion Report, compact PLAN/RUNLOG/TEST pointers; RU/EN parity. Frozen runner baseline data for T32.
- Next step: PAOS-GAP-01/02/03/04; T30/T31 may be prepared according to their DAG.

#### Completion Report

- status: implemented
- what was done: Public CLI RED/GREEN and negative acceptance checked; four RU/EN guide pairs, registry and control-plane pointers synchronized; frozen input manifest retained.
- files touched / work locations: docs/product-agent-os/{cli-reference,artifact-contracts,coding-standards,architecture}{,.en}.md; docs/sources/registry{,.en}.md; PLAN.md; RUNLOG.md; TEST.md; current plan; tests/product_agent_os/test_codex_runtime_runner_cli.py
- technical value delivered: Full integrated + fixture/transcript/compatibility/docs evidence; same-fixture comparison.
- product value delivered: End-to-end ordinary route locally verified with explicit limitations.
- actual implementation date and time: 05-11-2026 15:42
- verification evidence: Final full unittest: 1272 tests, 753.848s, OK (skipped=1), exit 0; focused 267 OK + two later acceptance cases OK; fixture 91; transcript 26/26; compatibility compatible; docs 100 OK; check_docs/task matrix/state consistency/diff exit 0; strict isolated preview and 1616 local links/anchors OK. Exact commands/RED-GREEN: current-run evidence above.
- residual risks: Fresh Codex host/workflow activation not_verified; OR-A3 report-path hook portion deferred to GAP-05; no provider/model/promotion proof.
- follow-up: No remaining ORD implementation. Later PAOS-GAP/T30–T34 remain unstarted; T23–T29 preserved.

### Task `PAOS-GAP-01`

- Task: Reconcile current pointers and remove unsupported maturity claims
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Separate owner request to implement GAP-01–GAP-05
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 17:48
- Depends on: Preferably after ORD-06; technically independent of ordinary route implementation
- Blocks: Honest handoff and GAP-02 compatibility description
- Source: IMP-05/07
- Short description: Identify product integration queue separately from B45 next=T30. Mark old Start T28 and previous Stop contract superseded with current receipt. Remove Production-ready claim from manifest; do not replace placeholder URLs with invented real endpoints, document local-package limitation instead. Preserve historical receipts and unresolved backlog.
- Technical value: User and next executor do not return to closed tasks and incorrect claims.
- Product value: User and next executor do not return to closed tasks and incorrect claims.
- Scope: Owned files: `PLAN.md`; `RUNLOG.md`; `plugins/product-agent-os/.codex-plugin/plugin.json`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Consistent current RU/EN pointers and honest local maturity metadata.
- Acceptance criteria: The sole current B45 pointer points to T30; T23–T29 remain completed under their prior evidence ceiling. ACT repair is not called unverified generic hook history. Manifest does not promise production readiness; no distribution readiness claim with placeholder metadata.
- Verification gates: python -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_codex_compatibility -v; python tools/check_docs.py; git diff --check — exit 0. Manually review current-vs-historical sections against source-owned JSON; do not add a large validator for a few lines.
- Risks / approval gates: Do not rewrite history; do not change T23–T34 statuses based on the new plan; do not release a new version or publish package. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: low-medium
- Estimated execution time: 0.5 working day
- Agents: docs-maintainer; evidence owner: lifecycle-orchestrator; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Consistent current RU/EN pointers and honest local maturity metadata.
- Next step: GAP-02 and subsequent B45 queue.

#### Completion Report

- status: implemented
- what was done: Current product/B45 pointers reconciled; historical T28/Stop receipts retained; manifest production-readiness wording replaced by local-package limits.
- files touched / work locations: `PLAN.md`; `RUNLOG.md`; `plugins/product-agent-os/.codex-plugin/plugin.json`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`
- technical value delivered: Current product/B45 pointers reconciled; historical T28/Stop receipts retained; manifest production-readiness wording replaced by local-package limits.
- product value delivered: User and next executor do not return to closed tasks and incorrect claims. Local scope only.
- actual implementation date and time: 05-11-2026 17:48
- verification evidence: Final full unittest: 1284 tests, 848.832s, OK (skipped=1), exit 0; fixture 91/91 exit 0; transcript 26/26 exit 0; focused RED/GREEN and docs receipts in GAP verification log. Compatibility exit 1 needs_review explicitly remains open.
- residual risks: Historical runtime/site receipts remain dated; placeholder distribution URLs unchanged.
- follow-up: Continue from T30 only under its separate task scope.

### Task `PAOS-GAP-02`

- Task: Reconcile MCP/component inventory and capability matrix
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Separate owner request to implement GAP-01–GAP-05
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 17:48
- Depends on: GAP-01 for maturity wording; code parser independent of ORD
- Blocks: Reliable B42 inventory and future distribution review
- Source: IMP-04/05
- Short description: First recheck official legacy/portable schema; shared read-only resolver returns format/version, normalized components and issues. Mark current flat .mcp.json legacy observed, explicitly check schema support, do not validate solely from presence of context7. Connect resolver to consumers and check legacy/portable/absent/conflicting/malformed fixtures. Separate executor/orchestrator and App/CLI/IDE/component support; native plugin and standalone skill are different capabilities.
- Technical value: Diagnostics no longer simultaneously report compatible and empty MCP inventory.
- Product value: Diagnostics no longer simultaneously report compatible and empty MCP inventory.
- Scope: Owned files: `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py [proposed]`; `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py`; `plugins/product-agent-os/scripts/product_agent_os/batch39_inventory.py`; `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/scripts/product_agent_os/system_file_hygiene.py`; `tests/product_agent_os/test_codex_compatibility.py`; `tests/product_agent_os/test_batch39_inventory.py`; `tests/product_agent_os/test_discovery.py`; `tests/product_agent_os/test_system_file_hygiene.py`; `docs/product-agent-os/codex-compatibility.md`; `docs/product-agent-os/codex-compatibility.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Normalized component contract and RU/EN capability matrix; source registry records checked scope/date.
- Acceptance criteria: One package produces identical inventory in all consumers. Malformed/unsupported does not become compatible. Distinguish absent, present_unverified, needs_review and host_verified; last only with separate host receipt. Legacy package is not migrated automatically; priority for two formats documented and checked against official schema.
- Verification gates: python -m unittest tests.product_agent_os.test_codex_compatibility tests.product_agent_os.test_batch39_inventory tests.product_agent_os.test_discovery tests.product_agent_os.test_system_file_hygiene -v; python plugins/product-agent-os/scripts/validate_codex_compatibility.py; docs gate — fixtures pass/reject as expected by class, current-package outcome recorded honestly, not necessarily compatible until schema conflict resolved.
- Risks / approval gates: Do not run npx/MCP, install, edit global config or perform portable migration. Unsupported current format is a finding, not grounds to weaken validator. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: high
- Estimated execution time: 1–2 working days
- Agents: plugin-runtime-builder; review: security-privacy-supply-chain-reviewer; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Normalized component contract and RU/EN capability matrix; source registry records checked scope/date.
- Next step: GAP-03.

#### Completion Report

- status: implemented
- what was done: One supported-subset resolver feeds compatibility, package inventory, discovery, methodology and hygiene; portable/overlay precedence and malformed/escape cases tested.
- files touched / work locations: `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py`; `plugins/product-agent-os/scripts/product_agent_os/batch39_inventory.py`; `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/scripts/product_agent_os/system_file_hygiene.py`; `tests/product_agent_os/test_codex_compatibility.py`; `docs/product-agent-os/codex-compatibility.md`; `docs/product-agent-os/codex-compatibility.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`
- technical value delivered: One supported-subset resolver feeds compatibility, package inventory, discovery, methodology and hygiene; portable/overlay precedence and malformed/escape cases tested.
- product value delivered: Diagnostics no longer simultaneously report compatible and empty MCP inventory. Local scope only.
- actual implementation date and time: 05-11-2026 17:48
- verification evidence: Final full unittest: 1284 tests, 848.832s, OK (skipped=1), exit 0; fixture 91/91 exit 0; transcript 26/26 exit 0; focused RED/GREEN and docs receipts in GAP verification log. Compatibility exit 1 needs_review explicitly remains open.
- residual risks: Current flat MCP declaration remains needs_review; no full-schema or native-host claim.
- follow-up: Owner decides MCP migration before stronger package compatibility claim.

### Task `PAOS-GAP-03`

- Task: Continue existing B42 M02/M04–M08 for provenance and skill exposure
- Status: blocked
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Separate owner request to implement GAP-01–GAP-05
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 17:48
- Depends on: B42 source matrix; GAP-02 for shared component inventory; ORD-05 for intended compact workflow
- Blocks: Fresh-host ordinary claim; current-project GAP-06 pilots have separate owner approval and do not depend on fresh-host receipt
- Source: IMP-06; B42-S1-M02/M04/M05/M06/M07/M08 — existing task IDs retained
- Short description: M02: source/package/cache normalized digest and effective selection path. M04/M05: separately define safe read-only implicit class and explicit-only write/release/automation; change metadata only if owner chooses that policy, not by default. M07/M08: routing and synthetic regression cases. M06: separately authorized fresh-session probe for exposure plus invocation, saving results in owning B42 matrix without raw chat. This block coordinates existing tasks; it does not replace them with a new status.
- Technical value: Clear which skill version governs the task and what is actually available to users.
- Product value: Clear which skill version governs the task and what is actually available to users.
- Scope: Owned files: `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`; `plugins/product-agent-os/scripts/product_agent_os/validators.py`; `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`; `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`; `tests/product_agent_os/test_lifecycle_skills.py`; `tests/product_agent_os/test_validators.py`; `docs/product-agent-os/instruction-tool-use-compliance.md`; `docs/product-agent-os/instruction-tool-use-compliance.en.md`; approved follow-up extension: `plugins/product-agent-os/skills/agent-team-designer/agents/openai.yaml`; `plugins/product-agent-os/skills/docs-maintainer/agents/openai.yaml`; `plugins/product-agent-os/skills/implementation-planner/agents/openai.yaml`; `plugins/product-agent-os/skills/requirements-author/agents/openai.yaml`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Existing B42 task evidence and RU/EN guidance; cache unchanged without separate exact authority.
- Acceptance criteria: Recheck 11/12 drift from report rather than treating it as permanent; distinguish installed, exposed, selected and invoked. No implicit invocation for explicit-only is not failure. Source/cache mismatch is not silently fixed. Local metadata/eval evidence and fresh-host receipt have different statuses.
- Verification gates: python -m unittest tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_validators -v; python plugins/product-agent-os/scripts/run_transcript_eval.py; docs gate — exit 0 for local scope. Fresh session with fixed source hashes and intended route: separate manual evidence gate; do not close M06 without it.
- Risks / approval gates: Installed cache/global settings/trust outside workspace slice. If refresh needed, first prepare concrete diff/destination/hash/rollback and approval; do not mix with T32–T34. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: medium-high
- Estimated execution time: 1–2 working days local; host/owner waiting separately
- Agents: lifecycle-orchestrator; evidence owner: tester; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Existing B42 task evidence and RU/EN guidance; cache unchanged without separate exact authority.
- Next step: Fresh-host probe remains separate; current-project GAP-06 pilots performed with explicit host gap.

#### Completion Report

- status: blocked
- what was done: Owner-approved four-file metadata correction subsequently applied (94 focused tests); local provenance and metadata validation, source/cache digests and explicit compliance/learning routing implemented; B42 current_execution preserves original task IDs and historical snapshot.
- files touched / work locations: `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`; `plugins/product-agent-os/scripts/product_agent_os/validators.py`; `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`; `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`; `tests/product_agent_os/test_lifecycle_skills.py`; `docs/product-agent-os/instruction-tool-use-compliance.md`; `docs/product-agent-os/instruction-tool-use-compliance.en.md`; `plugins/product-agent-os/scripts/product_agent_os/discovery.py (shared with GAP-02)`; approved follow-up: `plugins/product-agent-os/skills/agent-team-designer/agents/openai.yaml`; `plugins/product-agent-os/skills/docs-maintainer/agents/openai.yaml`; `plugins/product-agent-os/skills/implementation-planner/agents/openai.yaml`; `plugins/product-agent-os/skills/requirements-author/agents/openai.yaml`
- technical value delivered: Local provenance and metadata validation, source/cache digests and explicit compliance/learning routing implemented; B42 current_execution preserves original task IDs and historical snapshot.
- product value delivered: Clear which skill version governs the task and what is actually available to users. Local scope only.
- actual implementation date and time: 05-11-2026 17:48
- verification evidence: Final full unittest: 1284 tests, 848.832s, OK (skipped=1), exit 0; fixture 91/91 exit 0; transcript 26/26 exit 0; focused RED/GREEN and docs receipts in GAP verification log. Compatibility exit 1 needs_review explicitly remains open.
- residual risks: Local implementation verified; M04 explicit-only decision and four metadata corrections completed locally; M06 fresh-host exposure/invocation remains required.
- follow-up: Four-file correction applied with explicit owner approval; authorize fresh-host probe separately; no cache/global write.

### Task `PAOS-GAP-04`

- Task: Fix local source-policy heuristic without false fact verification
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Separate owner request to implement GAP-01–GAP-05
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 17:48
- Depends on: IMP-08 report; independent of B45
- Blocks: Source-status consistency for subsequent claims
- Source: IMP-08
- Short description: Parse URL with standard parser; exact hostname for official domains from verified source map. Separate source_present, claim_supported evidence and freshness; source header alone does not confer verified. RU/EN equivalent; suffix spoof, userinfo URL, malformed URL, plain Sources and stale checked date are negative cases.
- Technical value: Current official links are not rejected, and an empty header does not mask missing evidence.
- Product value: Current official links are not rejected, and an empty header does not mask missing evidence.
- Scope: Owned files: `plugins/product-agent-os/scripts/product_agent_os/source_policy.py`; `tests/product_agent_os/test_source_policy.py`; `docs/sources/registry.md`; `docs/sources/registry.en.md`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Honest source-presence classification and synchronized registry; docs owner research-source-analyst.
- Acceptance criteria: learn.chatgpt.com/platform.openai.com/developers.openai.com recognized in agreed scope; evil suffix and Sources-only do not support a claim. Do not declare semantic verification where only link/presence was checked. Existing policies not weakened.
- Verification gates: python -m unittest tests.product_agent_os.test_source_policy -v; docs gate — exit 0; every before/after behavior reproduced by focused tests.
- Risks / approval gates: Do not create crawler, external updater or automatically treat an undated claim as fresh. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: medium
- Estimated execution time: 0.5–1 working day
- Agents: plugin-runtime-builder; source review: research-source-analyst; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Honest source-presence classification and synchronized registry; docs owner research-source-analyst.
- Next step: Use corrected source policy in subsequent local gate.

#### Completion Report

- status: implemented
- what was done: Exact official HTTPS hostname classification separates source_present, claim_supported and freshness; header/spoof/date negatives tested.
- files touched / work locations: `plugins/product-agent-os/scripts/product_agent_os/source_policy.py`; `tests/product_agent_os/test_source_policy.py`; `docs/sources/registry.md`; `docs/sources/registry.en.md`
- technical value delivered: Exact official HTTPS hostname classification separates source_present, claim_supported and freshness; header/spoof/date negatives tested.
- product value delivered: Current official links are not rejected, and an empty header does not mask missing evidence. Local scope only.
- actual implementation date and time: 05-11-2026 17:48
- verification evidence: Final full unittest: 1284 tests, 848.832s, OK (skipped=1), exit 0; fixture 91/91 exit 0; transcript 26/26 exit 0; focused RED/GREEN and docs receipts in GAP verification log. Compatibility exit 1 needs_review explicitly remains open.
- residual risks: Presence/date heuristics do not validate source contents or semantic claim support; no crawler or freshness guarantee.
- follow-up: Use claim-level source review when stronger evidence is needed.

### Task `PAOS-GAP-05`

- Task: Design and separately verify bounded report authority for read-only analysis
- Status: blocked
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Separate owner request to implement GAP-01–GAP-05
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 17:48
- Depends on: IMP-09 report; ORD-06 for stable ordinary semantics; separate authorization for durable hook change
- Blocks: Full OR-A3 path-specific acceptance; does not block other ordinary cases
- Source: IMP-09; new case, not reopening ACT-F1–F6
- Short description: First design review: read-only target + exact authorized output paths, current task binding, explicit new-task transition and scope expiry. Implementation only after separate scope approval. Canonicalize paths/aliases, reject traversal, broad directory grant and terminal-task reuse; authority comes from explicit permission, not a data payload field. Synchronize active/staged policy. Test direct tool and nested functions.exec mutations; then fresh-host probe on approved exact hashes.
- Technical value: An explicitly requested report is saved without confusing read-only research and authorized result writing.
- Product value: An explicitly requested report is saved without confusing read-only research and authorized result writing.
- Scope: Owned files: `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `.codex/workflows/task-plan-lifecycle.md`; `plugins/product-agent-os/assets/templates/workflows/task-plan-lifecycle.md`; `tests/product_agent_os/test_lifecycle_hooks.py`; `tests/product_agent_os/test_task_plan_lifecycle.py`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Design and local/host receipts in this block's Completion Report; docs owner docs-maintainer.
- Acceptance criteria: One authorized Markdown is created; neighboring output, target source, config/hook, stale marker, terminal marker and escaped path denied. PreToolUse guards not weakened, Stop remains advisory. Local pass does not close fresh-host gate. A report.md name or work_type=planning alone is insufficient authority.
- Verification gates: python -m unittest tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_task_plan_lifecycle -v; docs gate; then approved positive/negative host probe with exact hash receipt. Until trust/fresh-session evidence status is implemented_not_runtime_verified, not repaired runtime.
- Risks / approval gates: High permission regression risk. Do not introduce this hook change as an ordinary-route side effect. First prepare reviewable patch/negative evidence, with trust approval as final separate step; if refused preserve prior guards. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: high
- Estimated execution time: 1–2 working days local; trust/fresh-session separately
- Agents: architect; implementation owner: plugin-runtime-builder; review: security-privacy-supply-chain-reviewer; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Design and local/host receipts in this block's Completion Report; docs owner docs-maintainer.
- Next step: Close OR-A3 only within evidenced host scope.

#### Completion Report

- status: blocked
- what was done: Pinned report grant, explicit task transition and one literal create-only Markdown patch implemented; active/package source mirrored; direct/nested wire and negative/default-route cases passed.
- files touched / work locations: `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `.codex/workflows/task-plan-lifecycle.md`; `plugins/product-agent-os/assets/templates/workflows/task-plan-lifecycle.md`; `tests/product_agent_os/test_lifecycle_hooks.py`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`
- technical value delivered: Pinned report grant, explicit task transition and one literal create-only Markdown patch implemented; active/package source mirrored; direct/nested wire and negative/default-route cases passed.
- product value delivered: An explicitly requested report is saved without confusing read-only research and authorized result writing. Local scope only.
- actual implementation date and time: 05-11-2026 17:48
- verification evidence: Final full unittest: 1284 tests, 848.832s, OK (skipped=1), exit 0; fixture 91/91 exit 0; transcript 26/26 exit 0; focused RED/GREEN and docs receipts in GAP verification log. Compatibility exit 1 needs_review explicitly remains open.
- residual risks: implemented_not_runtime_verified: no report-mode trusted command installed, no fresh-host positive/negative receipt; preflight is not atomic.
- follow-up: Separate exact-hash command/grant trust approval and fresh-host probe before closing OR-A3.

### Task `B45-CQRR-T30`

- Task: Implement an independent blinded reviewer contract
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Report-based plan; future implementation not yet authorized
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: B45-CQRR-T29 — satisfied locally
- Blocks: B45-CQRR-T32, B45-CQRR-T33
- Source: B45 task-group T30, IMP-10
- Short description: Use T23 output validation and typed T29 evidence. Define blinded reviewer request/result: neutral pair IDs, sanitized patch/context, deterministic evidence refs, structured findings and severity. Arm mapping remains outside reviewer input; self-scores/target verdict excluded. Separate pair suitability gate before review from final promotion gate after reviewer to avoid T29 reviewer-required → T30 review-blocked cycle.
- Technical value: Independent evaluation instead of primary model self-assessment.
- Product value: Independent evaluation instead of primary model self-assessment.
- Scope: Owned files: `plugins/product-agent-os/assets/templates/evals/code-quality-reviewer-rubric.json [proposed]`; `plugins/product-agent-os/scripts/codex_runtime_runner/reviewer_contract.py [proposed]`; `tests/product_agent_os/test_batch45_code_quality_reviewer.py [proposed]`; `docs/planning/batch45-code-quality-runtime-recovery-task-group.json`; `PLAN.md`; `RUNLOG.md`; `TEST.md`; `EVALS.md`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Reviewer schema/rubric and synthetic gates; after completion update only T30 in existing B45 task group and compact RUNLOG/TEST; docs owner architect, EVALS.md with new gate.
- Acceptance criteria: Invalid schema or missing deterministic pair evidence blocks review; arm permutation does not expose labels; primary self-score does not affect verdict. Critical correctness/security/data-loss/regression finding blocks promotion independently of average. Synthetic requests demonstrably label-free, no live blinding claim yet.
- Verification gates: python -m unittest tests.product_agent_os.test_batch45_code_quality_reviewer tests.product_agent_os.test_codex_runtime_runner_promotion_contract tests.product_agent_os.test_batch45_code_quality_metrics -v — exit 0; seeded label/self-score leakage, incomplete pair and critical override cases.
- Risks / approval gates: No live reviewer call. If T29 API cannot separate pre/post review, first show minimal extension of promotion_contract.py and its test as dependency amendment, without rewriting T29. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: high
- Estimated execution time: 1–2 working days
- Agents: architect; evidence owner: tester; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Reviewer schema/rubric and synthetic gates; after completion update only T30 in existing B45 task group and compact RUNLOG/TEST; docs owner architect, EVALS.md with new gate.
- Next step: T32 after T31; T31 does not wait for T30 in dependency graph.

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending

### Task `B45-CQRR-T31`

- Task: Build a representative multi-stack held-out corpus
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Report-based plan; future implementation not yet authorized
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: B45-CQRR-T27, B45-CQRR-T29 — satisfied locally
- Blocks: B45-CQRR-T32, B45-CQRR-T33
- Source: B45 task-group T31, IMP-10
- Short description: Assemble 12–16 synthetic/sanitized tasks, ≥4 stack families and ≥5 risk classes. Manifest per case: stable ID, stack/risk, acceptance, oracle/check command, expected fault classes, allowed files, privacy status, digest. Include small fix, legacy, boundary/security, abstraction trap, perf applicability and reuse/config/deletion/no-new-code. List exact member files per fixture in manifest before freeze; a directory does not grant arbitrary write scope. Freeze hashes before treatment outputs.
- Technical value: Quality checked across diverse tasks, not only internal project structure.
- Product value: Quality checked across diverse tasks, not only internal project structure.
- Scope: Owned files: `tests/fixtures/product_agent_os/batch45/code-quality-corpus/ [proposed bounded fixture directory]`; `docs/superpowers/specs/batch45-code-quality-heldout-corpus.json [proposed]`; `tests/product_agent_os/test_batch45_code_quality_corpus.py [proposed]`; `docs/planning/batch45-code-quality-runtime-recovery-task-group.json`; `PLAN.md`; `RUNLOG.md`; `TEST.md`; `EVALS.md`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Frozen corpus manifest and fixtures; only T31 status in existing B45 task group; docs owner tester, EVALS.md corpus policy.
- Acceptance criteria: Every case executable or has explicit readiness blocker before T33; no dependency on private target/service. Required stacks/risks represented; correct no-op not penalized. No secrets/PII/raw chat/absolute user paths. A changed frozen case creates a new corpus version and invalidates comparison, never replaces prior hash.
- Verification gates: python -m unittest tests.product_agent_os.test_batch45_code_quality_corpus -v — exit 0; manifest/schema, hash freeze, seeded fixture corruption, privacy/path and risk-coverage checks. Missing toolchain is blocked case, not silently skipped valid pair.
- Risks / approval gates: Do not tune corpus after viewing treatment; do not install missing toolchain without approval. Baseline/treatment leakage invalidates run. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: high
- Estimated execution time: 2–3 working days
- Agents: tester; privacy review: security-privacy-supply-chain-reviewer; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Frozen corpus manifest and fixtures; only T31 status in existing B45 task group; docs owner tester, EVALS.md corpus policy.
- Next step: T32 after T30.

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending

### Task `B45-CQRR-T32`

- Task: Freeze an isolated treatment and executable prompt contract
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Report-based plan; future implementation not yet authorized
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: B45-CQRR-T25, B45-CQRR-T30, B45-CQRR-T31
- Blocks: B45-CQRR-T33
- Source: B45 task-group T32, IMP-10
- Short description: Freeze exact prompts/context digests, runner/config/source hashes, corpus/toolchain versions, primary model/effort and timeout policy. Both arms use one ordinary routing baseline. The only difference is compact pre-edit intervention T25; no reviewer assistance/comment advisory/model switch added. Define measured outcomes, tolerance, invalid-pair policy and no-op scoring before run. Separately fix future transport binding: current durable runner/model_output path; if reusable driver missing, dependency gap must block T33, not be bypassed by temporary script.
- Technical value: Experiment outcome attributable to one process change.
- Product value: Experiment outcome attributable to one process change.
- Scope: Owned files: `plugins/product-agent-os/assets/templates/evals/code-quality-baseline-prompt.md [proposed]`; `plugins/product-agent-os/assets/templates/evals/code-quality-treatment-prompt.md [proposed]`; `docs/superpowers/specs/batch45-code-quality-eval-design.json [proposed]`; `tests/product_agent_os/test_batch45_code_quality_eval_design.py [proposed]`; `docs/planning/batch45-code-quality-runtime-recovery-task-group.json`; `PLAN.md`; `RUNLOG.md`; `TEST.md`; `EVALS.md`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Frozen eval design; update only T32 in B45 task group and EVALS.md pointer; docs owner architect.
- Acceptance criteria: Prompt diff contains only stated intervention; digest reproducible; models/effort/tools/timeouts identical. Full research/checklist does not enter every prompt. Runner path and invocation contract reproducible; no ephemeral adapter or hidden change from ORD/cache/hooks.
- Verification gates: python -m unittest tests.product_agent_os.test_batch45_code_quality_eval_design -v — exit 0; single-factor diff, context digest and transport-contract cases. Check offline fixture reproduction of baseline/treatment without model call.
- Risks / approval gates: Do not guess provider/model values from old approval. Fix concrete design values before T33; approve exact costs/call scope before T34. Missing reusable driver is an explicit blocking gap, not a plan shortcut. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: medium-high
- Estimated execution time: 1–2 working days
- Agents: architect; independent evidence check: completion-skeptic; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Frozen eval design; update only T32 in B45 task group and EVALS.md pointer; docs owner architect.
- Next step: T33.

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending

### Task `B45-CQRR-T33`

- Task: Run the local promotion-readiness preflight
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Report-based plan; future implementation not yet authorized
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: B45-CQRR-T24, T28, T29, T30, T31, T32
- Blocks: B45-CQRR-T34 preparation
- Source: B45 task-group T33, IMP-10
- Short description: On one pinned state run schema/normalization, deterministic metrics, reviewer pre/post gate, corpus freeze, prompt single-factor and synthetic transport end-to-end checks. Confirm no review-gate cycle. Bind command exit/results to checked hashes. Record pass/fail/blocked per gate; create approval packet only after green local preflight.
- Technical value: Expensive experiment is not launched on a known broken contract.
- Product value: Expensive experiment is not launched on a known broken contract.
- Scope: Owned files: `docs/superpowers/specs/batch45-code-quality-local-readiness.json [proposed]`; `docs/planning/batch45-code-quality-runtime-recovery-task-group.json`; `PLAN.md`; `RUNLOG.md`; `TEST.md`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Local readiness packet, existing T33 status and compact RUNLOG/TEST; docs owner completion-skeptic.
- Acceptance criteria: Valid fixtures pass; every required invalid class and seeded fault is caught by expected check. Blinding and reproducibility confirmed. All 12–16 cases have available local prerequisites; missing tools do not become readiness. No provider/model/reviewer call. One missing gate maintains no-go.
- Verification gates: python -m unittest tests.product_agent_os.test_codex_runtime_runner_promotion_contract tests.product_agent_os.test_codex_runtime_runner_model_output tests.product_agent_os.test_batch45_code_quality_behavior tests.product_agent_os.test_batch45_packet_contracts tests.product_agent_os.test_batch45_code_quality_metrics tests.product_agent_os.test_batch45_code_quality_reviewer tests.product_agent_os.test_batch45_code_quality_corpus tests.product_agent_os.test_batch45_code_quality_eval_design -v — exit 0; docs gate; verify reuse of integrated evidence only on unchanged relevant state.
- Risks / approval gates: Do not claim behavioral promotion from local preflight. Do not create new live approval packet with failed/blocked prerequisites. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: medium
- Estimated execution time: 0.5–1 working day
- Agents: completion-skeptic; evidence owner: tester; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Local readiness packet, existing T33 status and compact RUNLOG/TEST; docs owner completion-skeptic.
- Next step: Prepare concrete T34 approval packet; no calls before new approval.

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending

### Task `B45-CQRR-T34`

- Task: Prepare, execute and decide a new promotion eval only after exact approval
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Report-based plan; future implementation not yet authorized
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: B45-CQRR-T33 and new exact owner approval
- Blocks: Promotion decision; this does not close production readiness
- Source: B45 task-group T34; prior T21 invalid pairs and T22 no-go
- Short description: T34a after T33: prepare reviewable packet with exact transport invocation, model/effort, total primary/reviewer calls, wall/timeout/cost caps, data/retention, corpus/design/runner hashes, approved retries and stop policy. T34b only after exact approval: run frozen comparison, validate every output before aggregation, reviewer only after valid required pairs. Approval binds one run and is marked consumed at first call; subsequent authorized calls within the same bounded run count against its cap and do not require repurchasing authority. A new run/retry outside approved policy requires new approval. T34c: deterministic+reviewer decision.
- Technical value: Promotion decision based on comparable experiment and independent verification.
- Product value: Promotion decision based on comparable experiment and independent verification.
- Scope: Owned files: `docs/superpowers/specs/batch45-code-quality-eval-approval-packet.json [proposed]`; `docs/superpowers/specs/batch45-code-quality-eval-results.json [proposed]`; `docs/superpowers/specs/batch45-code-quality-promotion-decision.json [proposed]`; `docs/planning/batch45-code-quality-runtime-recovery-task-group.json`; `PLAN.md`; `RUNLOG.md`; `TEST.md`; `EVALS.md`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Approval/results/decision packets; existing T34 machine status, EVALS/RUNLOG pointers; docs owner release-operator.
- Acceptance criteria: All promotion-counted pairs schema-valid with current deterministic evidence; independent review without unresolved critical findings. Any frozen tolerance exceedance, invalid/missing pair or privacy issue remains no-go or a prearranged explicit owner exception; do not hide exceptions. Old T20 approval is not reused.
- Verification gates: After preparation: python -m json.tool docs/superpowers/specs/batch45-code-quality-eval-approval-packet.json — exit 0 plus semantic/hash/cap review. Exact live command comes from validated T32/T34 packet; it is currently absent and unauthorized. After run: promotion contract/metrics/reviewer tests, sanitized results validation, cap/retention ledger, docs/control-plane sync.
- Risks / approval gates: Source status remains approval_required_not_started; task-matrix planned is only schema representation, not removal of gate. Stop on first invalid output, unapproved drift, privacy breach or critical finding. Publish/deploy/automation not separately authorized. Rollback: only this slice's changes against saved baseline; preserve others' hunks and historical receipts.
- Complexity: high
- Estimated execution time: 0.5–1 day preparation/analysis; live duration and cost only under approved packet
- Agents: release-operator; independent reviewer under approved policy; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Approval/results/decision packets; existing T34 machine status, EVALS/RUNLOG pointers; docs owner release-operator.
- Next step: Save promotion/no-go decision with evidence ceiling; assess GAP-06 user outcomes independently.

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending

### Task `PAOS-GAP-06`

- Task: Check ordinary user outcomes through existing B39/B44 manual packets
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner authorized three pilots from current project to host-target; HOST-01 dependency removed, activation separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 17:11
- Depends on: ORD-06 and local F05/F08 completed; HOST-01/HOST-02 and T34 are not gates for these three synthetic local pilots.
- Blocks: Decision on next improvement; does not grant automatic promotion
- Source: IMP-11; existing B39 feedback and B44 manual pilot
- Short description: First read-only owner review of existing packets. Identify 3–5 representative ordinary tasks: bugfix, docs, legacy, no-new-code, boundary change; choose specific targets and actions with owner before pilot. With exact authority perform bounded target journey; measure time to useful outcome, extra questions/artifacts, repeat checks, acceptance correctness and owner intervention. Send findings to existing manual learning loop as candidates.
- Technical value: Check actual usability and usefulness after local engineering acceptance.
- Product value: Check actual usability and usefulness after local engineering acceptance.
- Scope: Owned files: `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json`; `prod_test.md`; `RUNLOG.md`; `docs/planning/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`
- Non-goals: Unlisted files, automatic target/cache/global writes, provider/browser/Git/publication and reimplementation of T23–T29 are outside scope. Exceptions require explicitly scoped later approval.
- Expected result: Existing manual pilot/feedback receipts and concise RUNLOG; no new automatic learning framework.
- Acceptance criteria: Each outcome tied to task/host/source version and evidence, failures not excluded from denominator. No system-wide causal inference from one pilot. Target/browser/provider actions only under named authority. B39 no-go/release ceiling and B44 manual_only retained pending separate decisions.
- Verification gates: Actual baseline/final checks, source hashes and file inventories in pilot-results; mandatory docs/matrix/state gates; owner feedback separately.
- Risks / approval gates: Current local pilot scope expressly authorized; owner acceptance received 10.11.2026; fresh-session/provider/browser/Git excluded. Rollback by initial_source proposal; preserve receipts.
- Complexity: medium
- Estimated execution time: 0.5–1 day preparation; pilot duration depends on approved targets
- Agents: product-manager; evidence owner: learning-loop-engineer; owner acceptance belongs to user; roles denote ownership, not launched subagents
- Skills: implementation-planner for scope/handoff; Python implementation: python-design-patterns and python-code-style; docs-maintainer for named docs impact; only task-matching canonical skills
- Output artifacts: Existing manual pilot/feedback receipts and concise RUNLOG; no new automatic learning framework.
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
