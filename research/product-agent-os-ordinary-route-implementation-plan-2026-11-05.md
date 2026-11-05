# Product-Agent OS: план реализации после аудита документации

Source status: project-local implementation proposal, 2026-11-05; основан на текущем коде и source-owned task groups. План сохранён по запросу владельца; ORD-01–ORD-06 реализованы локально, GAP-01–GAP-05 реализованы локально с указанными ниже незакрытыми gates. T30–T34 и GAP-06 не начаты.

## GAP-03 approved metadata correction — 05.11.2026

Task ID: PAOS-GAP03-METADATA-2026-11-05. The owner explicitly approved the four-file diff below. Scope extension: only the four named `agents/openai.yaml` files plus existing status/evidence synchronization. Ordinary bounded fix; explicit-only remains false; no new implicit class, cache refresh, global settings, trust, host probe, Git or publication.

Implemented: moved `allow_implicit_invocation: false` from `interface` to `policy` in `agent-team-designer`, `docs-maintainer`, `implementation-planner`, `requirements-author`. Before editing, all four current SHA-256 matched the saved proposal. Before validation produced four errors per file; afterward all 12 canonical metadata validate with false and no errors. Source/cache normalized drift remains 11/12; cache hashes remain unchanged. This closes the metadata correction and M04 decision locally, not M06 host exposure/invocation or GAP-05 trust/probe. The earlier proposal/digests and GAP receipts below remain historical evidence.

Verification: `python -B -m unittest tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_validators -q` — 94 tests, 1.680s, OK, exit 0. Final docs/control-plane checks: 232 tests, 9.969s, OK, exit 0 (`test_product_agent_os_docs`, `test_task_plan_lifecycle`, `test_lifecycle_hooks`, `test_infrastructure_templates`). Both hook validators, task-matrix validator, check_docs and git diff --check passed. Exact approved diff confirmed; 2394 other baseline files unchanged; all 12 cache skill hashes unchanged. Receipt: `.docs-tools/reports/gap-metadata-preservation.json`. No full unittest/fixture rerun is needed for this bounded metadata correction; the earlier 1284/91/26 results are historical, not newly executed evidence.

Control-plane sync: PLAN/RUNLOG/TEST, B42 matrix, affected current RU/EN claims and registry updated. REQUIREMENTS/EVALS/prod_test: not_applicable (no new requirements/rubrics/historical Batch 39 evidence). No site rebuild or freshness claim; navigation and Mermaid unchanged. Self-review verifies exact approved diff and unchanged false policy; no independent reviewer or host activation claim.


## Исполнение GAP-01–GAP-05 — текущий запуск 05.11.2026

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
python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md
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

## Исполнение ORD-01–ORD-06 — текущий запуск 05.11.2026

Lifecycle task ID: `PAOS-ORD-01-06-2026-11-05`.

Status: implemented_locally_verified (ORD-01–ORD-06 only). Владелец отдельно разрешил реализацию только первого этапа, локальные проверки и RU/EN sync; без публикации. Ниже сохранены исходный план и planning receipts. Запрет реализации в историческом planning scope не относится к отдельно разрешённым ORD-01–ORD-06. PAOS-GAP и T30–T34 остаются planned, T23–T29 не переоткрыты.

- Existing capability: прочитаны discovery, T26/T27 inputs/validators, runtime state/routes/contracts/guards, renderer/merge boundaries, active/package workflow и существующие tests.
- Smallest safe patch: opt-in adapter и явный legacy fallback; selectors, promotion/model output и package T25 не переписаны.
- Invariants: нет target execution, runtime write authority из JSON, потери project rules или автоматического completed; stale evidence явно отделено.
- Dependency decision: no_new_dependency; stdlib и существующие selectors/validators.
- Risk-selected tests: public CLI ordinary/full/invalid/state/unsafe/source-policy/stale/no-op; renderer reuse/stage/user-preservation; существующие runtime/template/merge suites.
- Comment decision: docstrings для trust boundaries, provenance и inert commands; старые незатронутые функции не переписываются ради advisory.
- Performance applicability: not_applicable, hot path performance claim не делается; измеряется только bounded local check time.
- Evidence and gaps: focused RED/GREEN, final integrated gate и self-review завершены; receipts ниже. Fresh-host activation и GAP-05 report authority не входят в closure.

Implementation contract: task_context schema_version=1, required task_id/intent/change_mode/changed_paths/risk_level/risks/acceptance; optional checks, verification_paths, seam/comments, typed full-scope flags, bound state и caller check_results. State binding требует отдельный JSON task_id/lifecycle_state плюс sha256. При отсутствии task state используется только явно помеченная recommendation. Caller receipts не являются independent execution evidence.

Scope clarification: registry.md и registry.en.md получают только ORD claim/source rows согласно AGENTS.md Documentation Rules; это часть ORD-06 docs sync, не работа над GAP-04 source-policy implementation. Локальные ignored reports содержат baseline/check output; root site и docs dependencies не изменяются.

Initial evidence:

| Check | Result |
| --- | --- |
| Baseline | 2406 существующих nonignored files; hashes и owned original text сохранены в .docs-tools/reports/ordinary-route-baseline.json |
| Первый focused run | Exit 1: sandbox TEMP denied; это environment failure, не RED feature evidence |
| Повтор в isolated TEMP | CLI exit 2: --task-context отсутствовал; renderer TypeError: task_context отсутствовал; intended RED |
| Initial combined 60 tests | Exit 1: adapter неверно передал seam reason T27; docs fixture не объявляла check. T27 не менялся, исправлены adapter/fixture |
| Focused retest | 3 tests GREEN |
| Negative input shape | Списки/dicts в enum полях вызвали TypeError; shape guards исправлены; 10 tests GREEN |
| Guard RED | Подмена legacy trace не отклонялась; добавлен scoped contract validator и запрет completed для contract mode |
| Combined ordinary/renderer | 43 tests, 41.592s, OK; включая multi-stack, stage preservation и nested instructions |
| Active workflow | Отсутствующая active compact copy воспроизведена; после ORD-05 parity/local-guard check GREEN |

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

Final post-sync docs gate: python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q — 100 tests, 3.492s, exit 0; python -B tools/check_docs.py — exit 0; python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md — ok; python -B plugins/product-agent-os/scripts/validate_task_state_consistency.py . — ok; git diff --check — exit 0 (existing CRLF normalization notices only).

Final preservation check before terminal marker: 27 existing owned files changed and two new files (task_routing.py and active code-change-contract.md); 2367 out-of-scope file hashes unchanged, including 660 root site files. All 11 later task blocks are text-identical to the saved plan baseline; frozen implementation/test hashes match the final full gate. T23–T29 source implementation and task-group JSON were not changed. Receipt: .docs-tools/reports/ordinary-route-preservation.json.

Control-plane sync: PLAN.md, RUNLOG.md and TEST.md updated with current ORD pointers; REQUIREMENTS.md `not_applicable` (accepted scope unchanged), EVALS.md `not_applicable` (no rubric/threshold/promotion change), prod_test.md `not_applicable` (Batch 39 historical family out of scope). No overflow/refactor required; no ownership handoff required within ORD. Source registry pair receives only ORD provenance entries. Host activation, GAP-05 and all later tasks retain their own gates.

Review findings resolved: executable-seam adapter invariant, malformed enum types, forged legacy trace/result-completion claims, old CLI call compatibility, current plan ID, and sensitive Windows path normalization. Remaining limitations are deliberate: command extraction is conservative and cannot interpret arbitrary project instructions; instruction reads remain mandatory. Task declarations/receipts are proposals, not trusted truth. Digest covers declared changed/verification files, manifests and check/instruction sources, not the entire environment. No automatic executor, provider, promotion or fresh-host activation is claimed.

## Решение и граница

Начать со сквозного ordinary route, переиспользуя T25–T27. Затем устранить оставшиеся расхождения из IMP-04–IMP-09 и продолжить существующую очередь B45-CQRR-T30–T34. T23–T29 не открываются повторно. Новые ID PAOS-ORD и PAOS-GAP обозначают только интеграционные и корректирующие задачи этого плана, не заменяют существующие Batch IDs.

На этапе сохранения плана были разрешены только данный Markdown и служебный lifecycle marker. Тогда код, тесты, prompts, hooks, конфигурация, исходный отчёт, PLAN/RUNLOG, task-group JSON, site и installed cache не менялись. Само сохранение плана не разрешало исполнение задач, публикацию, target apply, provider/model/reviewer calls или смену trust.

Первый полезный результат: для ограниченного bugfix существующего проекта система читает реальные источники, выбирает уже реализованные stack/risk selectors, выдаёт компактный контракт и обоснованный набор проверок, переиспользует имеющиеся документы и показывает фактические evidence/gaps. Отсутствие EVALS.md или builder.toml само по себе не отправляет такую задачу на повторный onboarding. Обязательные правила конкретного проекта остаются обязательными.

## Источники и актуальность

- [Отчёт с IMP-01–IMP-11](product-agent-os-docs-implementation-gap-analysis-2026-11-05.md).
- [Текущий B45 task group](../docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json): владелец machine status и зависимостей T23–T34.
- [Последний implementation/evidence pointer B45](../docs/superpowers/plans/2026-08-17-product-agent-os-loop-remediation.md).
- [T25–T27, compact authoring](../docs/superpowers/plans/2026-08-11-batch45-s9-b-compact-authoring-runtime.md).
- [B42 compliance matrix](../docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json).
- [GPT-6/lifecycle receipts](../docs/superpowers/specs/gpt6-documentation-refresh-task-group.json).
- [PLAN](../PLAN.md), [RUNLOG](../RUNLOG.md), [TEST](../TEST.md), [EVALS](../EVALS.md).
- [Канонический implementation-planner](../plugins/product-agent-os/skills/implementation-planner/SKILL.md).

Текущие code seams повторно прочитаны при составлении плана: templates/infrastructure, state/context_loader/routes/cli, contracts/guards, T26/T27 inputs и B45 task group. Числа исторических тестов ниже — receipts предыдущей реализации, не новые результаты этого запуска. Внешние утверждения опираются на проверку официальных источников в отчёте от 2026-11-05; новый внешний research в планировании не выполнялся. При реализации format/host-sensitive совместимости источники нужно перепроверить.

## Исходный baseline до ORD

| Задача | Состояние source-owned JSON | Использование в плане | Что не доказано этим статусом |
| --- | --- | --- | --- |
| T23 | locally_implemented_focused_verified | promotion_contract.py и model_output.py — единый durable output contract | Валидность будущих live outputs |
| T24 | locally_implemented_focused_verified | Сохранить schema/normalization и seeded-corruption regression fixtures | Новая end-to-end интеграция |
| T25 | locally_implemented_focused_verified | Переиспользовать 8 полей code-change-contract и packaged coding workflow | Активный workspace ещё не мигрирован |
| T26 | locally_implemented_focused_verified | ProjectInventory → select_code_quality_profile; добавить adapter/caller | Production routing пока не использует selector |
| T27 | locally_implemented_focused_verified | TestStrategyRequest → select_test_strategy; использовать решения в route | Исполнение выбранных проверок и корректность их evidence |
| T28 | locally_implemented_focused_verified | Сохранить fault detection и сокращённую структуру тестов | Не повод снова уменьшать тесты ради количества |
| T29 | locally_implemented_focused_verified | Typed deterministic metrics и promotion wrapper — основа T30/T33 | Независимость reviewer и происхождение live evidence |

T28 receipt: 196 → 34 repeated families, 3 owned exceptions, combined test LOC 8130 → 5658, 48 focused tests. T29 receipt: 23 focused tests. Эти suites повторяются при затронутом контракте или соответствующем gate, а не при каждом редактировании плана. Старые unchecked boxes не отменяют более новые receipts. ACT-F1–F6 не открываются повторно: новая задача bounded report authority — отдельный случай IMP-09.

## Порядок и зависимости

| Этап | Задачи | Результат / exit gate |
| --- | --- | --- |
| 1. Сквозной ordinary route | PAOS-ORD-01 → 02 → 03 → 04 → 05 → 06 | Реальный CLI contract path + bounded fixture journey + объяснимое evidence; текущая локальная интеграция, без заявления о host activation |
| 2. Остальные расхождения | PAOS-GAP-01, 02, 03, 04, 05 | Непротиворечивые pointers/claims, component inventory, B42 provenance, source policy; hook change — самостоятельный approval scope |
| 3. Независимая оценка | T30 и T31 → T32 → T33 | Blinded reviewer, frozen corpus, одна intervention, local preflight |
| 4. Разрешённый эксперимент | T34 только после T33 и нового exact approval | Promotion/no-go из валидных pairs и независимых findings |
| 5. Пользовательский результат | PAOS-GAP-06 после ORD-06 и B42 evidence для выбранной поверхности | B39/B44 owner feedback, usefulness и ручное обучение; без автоматического promotion |

Это предпочтительный порядок исполнения, а не новые технические зависимости B45. T30 зависит от T29; T31 — от T27 и T29. T31 не зависит от T30. T32 зависит от T25/T30/T31. T33 зависит от T24/T28/T29/T30/T31/T32. T34 зависит от T33. Ordinary-route baseline должен быть заморожен одинаково для обеих arms до T32; иначе новый routing станет второй скрытой intervention. B42/hook/cache изменения не смешивать с экспериментом.

По умолчанию один исполнитель, роли в задачах — ответственность и handoff, не разрешение на запуск subagents. Общие файлы cli/routes/contracts и control-plane редактируются последовательно. T30/T31 допускают независимую подготовку при отдельно назначенных границах; план не запускает параллельную команду.

## Предлагаемый контракт ordinary route

Архитектурные границы:
1. Discovery читает workspace и возвращает происхождение сигналов; не исполняет найденные команды.
2. Новый небольшой adapter product_agent_os/task_routing.py преобразует inventory и task context в существующие ProjectInventory / TestStrategyRequest. Чистые selectors T26/T27 сохраняют свою ответственность.
3. state.py отделяет structural readiness, authoritative task state и inferred recommendation. task-group status не является lifecycle enum: завершённая T29 не означает release_ready.
4. templates.py выбирает подмножество registry по task scope и applicability; infrastructure.py сохраняет dry-run/stage/managed-section/companion/merge boundaries.
5. routes.py формирует required context, compact authoring, selected verification и reasons. CLI contract mode только планирует и сообщает; не становится универсальным executor.
6. Codex выполняет разрешённую работу и выбранные проверки; evidence отражает actual command, exit, checked input digest и gaps. Route-ready не равно task-completed.

Предлагаемый task context v1: task_id, intent/change_mode, changed_paths, risks с защищаемыми invariants и provenance, explicit lifecycle state с source ref при наличии, approval scope. Это данные для routing, не источник полномочий. Unknown risk не понижается автоматически до low. Неверный/конфликтующий state → needs_context с одной конкретной причиной; непроверенные инструменты → present_unverified. Явно указанный state не может обойти approval или source guards.

Совместимость: добавить opt-in structured task context к CLI и Python API, сохранив существующие вызовы. Старый вызов без task context использует явно помеченный legacy fallback, без утверждения «ordinary route activated». Успешная ordinary проверка должна показать mode/selector/version/source/reason и отсутствие широкого fallback. Unknown/new contract version даёт понятную ошибку, а не беззвучный downgrade.

Минимальные artifacts:
- Уже существующий проект: reuse текущих файлов; compact contract и evidence могут быть секциями существующего task artifact, новый набор файлов не обязателен.
- Docs-only: source/link/text checks по изменению; code-change contract и behavioral tests — not_applicable с причиной, если поведение не затронуто.
- Пустой проект: discovery и нужный scope/acceptance; не выдавать build-ready при отсутствующих требованиях.
- High-risk/financial/release/explicit full packet: full reporting и все применимые risk/approval gates. Full не означает автоматическую генерацию всех 209 templates, agents, hooks и automation candidates.
- Existing user files и project-mandated checks имеют приоритет над удобством минимального маршрута. В этом репозитории обязательные TEST.md/AGENTS.md gates не убираются новым selector.

## Сквозные acceptance scenarios

| ID | Given / When | Then и проверяемое evidence | Владелец / задача |
| --- | --- | --- | --- |
| OR-A1 | Существующий Python проект; одна регрессия pure function; известны invariant и test seam | Реальный CLI вызывает T26/T27, выбирает regression/unit seam; не требует EVALS/builder; compact ≤8 полей; trace показывает ordinary, без full fallback | tester / ORD-02,04,06 |
| OR-A2 | Аналогичная RU и EN структура, одинаковый task context | Одинаковый route и reasons; English headings не служат authority; single-agent разрешён | tester / ORD-02,04 |
| OR-A3 | Docs-only с разрешённым output | Нет code tests/benchmark без причины; target writes по-прежнему запрещены. Специальное разрешение report path проверяется только после GAP-05 | tester / ORD-04; security reviewer / GAP-05 |
| OR-A4 | Authorization/data-loss/security/financial/release risk | Нужные negative/contract checks и full reporting сохраняются; неподтверждённый low-risk hint не отменяет риск | reviewer / ORD-01,04,06 |
| OR-A5 | Existing unmarked AGENTS/config/hooks и повторный dry-run | User hashes неизменны; companion proposals; стабильный selected manifest; target apply требует прежний plan-bound approval | tester / ORD-03 |
| OR-A6 | Нет сведений о риске/команде; malformed task state или противоречивые источники | needs_context/blocked с конкретным gap; нет invented command, auto-install или success | tester / ORD-02,04 |
| OR-A7 | Baseline fixture имеет известную ошибку; выбранная regression проверка исполняется в изолированном synthetic workspace | RED на нужном assertion → минимальный GREEN; evidence связан с final inputs; skipped/not_run не становится passed | tester / ORD-06 |
| OR-A8 | Legacy caller без нового task context и high-risk fixture | Compatibility сохранена; legacy fallback видим; ordinary activation не заявлена | tester / ORD-04,06 |
| OR-A9 | Stale check receipt, changed source digest, обнаруженная unsafe shell command | Stale/present_unverified/blocked, без исполнения команды из untrusted текста | security reviewer / ORD-04,06 |
| OR-A10 | Корректное решение reuse/config/deletion/no-op | Не создаётся код ради оценки; результат принимается по acceptance и invariant | tester / ORD-06, T31 |

OR-A7 проверяет соединение production entry point и поведения локального synthetic fixture; это не замена fresh Codex host acceptance. Для утверждения о текущей загрузке активного workflow/skill потребуется свежая разрешённая сессия с provenance и observed path. Изменение текстов само по себе этого не доказывает.

## Общие правила исполнения будущих задач

- Все команды в task blocks — commands_to_run, не результаты этого запуска. Сначала observable RED для изменяемого поведения, затем минимальный GREEN; docs-only проверяются статически.
- У каждого блока свой точный owned files set. Общая дополнительная ownership каждого будущего implementation slice: только его Completion Report в этом плане и относящиеся к нему компактные записи PLAN.md, RUNLOG.md, TEST.md; root writer один, обновления последовательные. Эти общие пути и перечисленные в блоке файлы образуют полный scope. Остальные существующие файлы запрещены без видимого уточнения scope; новые файлы помечены как proposed. Существующий test module расширяется, если он уже владеет риском; не создавать отдельный тест на каждое поле/слово.
- Rollback: сохранить baseline diff/hashes перед slice; откатить только hunks этого slice, сохранить чужие изменения. Для active workflow сохранить прежние sections; для task context сохранять legacy API compatibility. Не использовать destructive Git.
- Для каждого завершённого implementation slice записать current evidence в его owning artifact, обновить только принадлежащий status, синхронизировать короткие PLAN/RUNLOG pointers. Этот план не является новым machine-status registry для T23–T34.
- Mandatory integrated gate один раз на объединённом implementation состоянии: `python -m unittest discover -s tests -p "test_*.py" -v`; `python plugins/product-agent-os/scripts/run_fixture_eval.py`; `python plugins/product-agent-os/scripts/run_transcript_eval.py`; `python plugins/product-agent-os/scripts/validate_codex_compatibility.py`; docs gate и diff. Ожидается exit 0; skips и несовместимости раскрываются. Повторять только при изменении relevant inputs, failure или unresolved risk.
- Docs gate: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`, `python tools/check_docs.py`, `git diff --check`. RU/EN обновлять одновременно в названных парах. Если меняются source-backed claims — registry.md и registry.en.md в том же slice.
- При изменении nav/Mermaid/generated-site evidence: `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/ordinary-route-preview` после разрешения на локальную сборку; links/anchors и diagram rendering по существующему docs tooling. Не устанавливать зависимости и не публиковать.
- Documentation fields каждого блока задают конкретный docs owner/path; требования, сценарии, архитектурное решение, quality strategy и rollback размещены здесь, не требуется создавать дублирующие методологические packets.
- FSD, cloud architecture, DB migration и deployment: not_applicable, таких изменений нет. Domain ownership описан выше (discovery, routing, infrastructure, evidence); отдельный DDD framework не нужен. Product hypothesis: уменьшить ненужную подготовку без ухудшения correctness; проверка локального поведения ORD-06, пользовательские outcomes GAP-06. Marketing/release success остаётся not_verified.
- Professional authoring: reuse selectors, stdlib dataclasses/json/pathlib и существующие validators; не добавлять dependencies, hosted runner или генератор framework. Adapter предпочтён повторной реализации selectors; full-only вариант оставляет IMP-01/02, silent heuristic-only inference оставляет IMP-03.

## Готовность, ограничения и Control-Plane Sync

Исторический статус при сохранении плана — proposal_saved. Текущее исполнение ORD-01–06 и новые receipts вынесены в начало документа. T30–T33 сохраняют planned_not_started, T34 — approval_required_not_started. Поле planned в task_matrix_plan_v1 не снимает внешние approval gates.

Plan quality: exact owned files, proposed paths, acceptance, commands, expected outcomes, rollback и evidence owners заданы. FSD/DB/cloud/deployment — not_applicable. Architecture и requirements traceability представлены в этом документе вместо новых дублирующих packets. Implementation/host verification — present_unverified; hook trust, live eval и target pilot — approval_required. Поздние transport/design gaps T32 и target scope GAP-06 блокируют соответствующие исполнения, но не отдельный старт ORD-01 после запроса на реализацию. План всей программы не объявляется безусловно plan_ready.

Оценка ORD-01–06: 5–10 инженерных рабочих дней последовательно, без approval waiting и новых environment blockers. Это планировочный диапазон, не обещанный срок и не измерение агентного времени. По факту первого vertical slice оценку пересмотреть, не добавляя обязательных стадий ради оценки.

Review mode текущего плана: self_review. Сверены IMP-01–IMP-11, исходные IDs, T23–T29 status, зависимости T30–T34, границы ordinary/full, наличие файлов, no-provider/target boundaries. Независимый reviewer и subagents в этом запуске не использовались. Статическая проверка структуры не доказывает качество будущего runtime.

| Control-plane файл | Решение в этом запуске | Handoff |
| --- | --- | --- |
| REQUIREMENTS.md | not_applicable | Новые implementation acceptance предложены здесь; текущий продукт не изменён |
| PLAN.md | handoff_required | При принятии ORD-01 lifecycle-orchestrator добавляет компактный pointer; B45 next=T30 остаётся отдельной очередью |
| TEST.md | handoff_required | Команды здесь proposed; реальные implementation receipts добавляют ORD-06/T33 owners |
| EVALS.md | handoff_required | Новые reviewer/corpus/design gates фиксируются в T30–T32, сейчас rubrics не изменены |
| RUNLOG.md | handoff_required | В текущем scope только новый план и marker; краткий pointer добавить при начале implementation |
| prod_test.md | not_applicable | B39 evidence не изменилось; будущий GAP-06 отдельно scoped |
| registry RU/EN | not_applicable | Новых внешних factual claims в site нет; будущие изменения входят в GAP-01/02/04 |
| site / MkDocs | not_applicable | План хранится вне docs navigation; site не пересобирается и freshness не заявляется |

Документ не меняет source-owned machine statuses и не закрывает будущие задачи. Completion Report со статусом planned и pending_execution_timestamp — обязательная честная запись невыполненной работы. При следующем запросе начать с ORD-01; не смешивать в одном slice ordinary routing, hook/cache/model changes и promotion eval.

## Проверки плана в текущем запуске

Проверено 2026-11-05, текущий запуск:

| Проверка | Команда / метод | Наблюдаемый результат |
| --- | --- | --- |
| Task matrix | `python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md` | Exit 0, ok=true, errors=[], task_matrix_plan_v1 |
| Docs contracts | `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | Exit 0, Ran 100 tests in 4.126s, OK |
| Docs structure | `python -B tools/check_docs.py` | Exit 0, documentation structure checks passed |
| Diff hygiene | `git diff --check` | Exit 0; только Git CRLF/LF notices, без whitespace errors |
| Source/dependency check | Read-only Python: Markdown scopes и source-owned B45 JSON | 17 уникальных задач; T30–T34 dependencies совпадают; 110 ссылок на существующие owned paths без пропусков; proposed файлы выделены отдельно |
| Links/text integrity | Read-only Python: local Markdown links, UTF-8, fences | 11 локальных ссылок существуют; U+FFFD отсутствует; fences сбалансированы |
| Preservation | SHA-256 по sorted Git tracked/nonignored untracked paths, исключены только новый план и marker | 2404 прежних файла: baseline и повторная проверка одинаковы, aggregate `feada09754aa46ffbfa5dc8b3b602eb7667cd4a9b5761257329ace52d7d0a95b` |

Первый длинный shell-вызов сохранения через helper завершился exit 1 на Windows MSIX launcher до выполнения Python; запись выполнена через apply_patch и отдельно прошла штатный matrix validator. Никакой обход lifecycle/sandbox или изменение окружения не выполнялись. Команды реализации из task blocks не запускались. Состояние implementation, source-owned task-group, исходного отчёта и site сохранено; проверка не охватывает ignored ephemeral runtime files и не является runtime/product acceptance.

## Подробные задачи

### Task `PAOS-ORD-01`

- Task: Зафиксировать контракт сквозного ordinary route и воспроизвести разрывы
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранённый план; отдельный запрос владельца реализовать только ORD-01–ORD-06
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 15:42
- Depends on: T25, T26, T27 — локально выполнены; отчёт IMP-01/02/03
- Blocks: PAOS-ORD-02, 03, 04
- Source: IMP-01, IMP-02, IMP-03; текущие state/routes/cli и selectors
- Short description: В existing tests воспроизвести OR-A1/A2/A4/A5/A6 на компактных synthetic fixtures. Уточнить task context v1, risk precedence, legacy fallback, authority vs evidence и точный expected selected artifact set в этом плане. Зафиксировать baseline response и перечень лишних required inputs; не менять production code в RED-подшаге.
- Technical value: Видимая воспроизводимая проблема вместо нового слоя деклараций.
- Product value: Видимая воспроизводимая проблема вместо нового слоя деклараций.
- Scope: Owned files: `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`; `tests/product_agent_os/test_codex_runtime_runner_cli.py`; `tests/product_agent_os/test_infrastructure_renderer.py`; `research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Contract и RED evidence в текущем плане; docs owner architect. Нет нового task-group для уже существующих B45 задач.
- Acceptance criteria: RED должен объясняться missing ordinary behavior, а не import/setup error. Контракт охватывает ordinary/docs/high-risk/unknown, RU/EN и no-builder. Acceptance имеет risk → scenario → test → evidence owner; нет скрытого provider или host requirement.
- Verification gates: python -m unittest tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_infrastructure_renderer -v — ожидаются заранее названные RED ordinary assertions, существующие unrelated cases остаются GREEN; это временный RED checkpoint, не completion всей интеграции.
- Risks / approval gates: Не ослаблять existing tests ради RED; при неоднозначной authority остановить зависимый build до решения в контракте. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: medium
- Estimated execution time: 0.5–1 рабочего дня
- Agents: architect; evidence owner: tester; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Contract и RED evidence в текущем плане; docs owner architect. Нет нового task-group для уже существующих B45 задач.
- Next step: ORD-02; RED cases закрываются до ORD-06.

#### Completion Report

- status: implemented
- what was done: Зафиксирован task_context v1 и OR-A1–A10; воспроизведены missing CLI/renderer contract и targeted negative regressions.
- files touched / work locations: tests/product_agent_os/test_codex_runtime_runner_cli.py; tests/product_agent_os/test_infrastructure_renderer.py; текущий план
- technical value delivered: Воспроизводимый risk/scenario/check mapping.
- product value delivered: Проверяемая ordinary задача без повторного onboarding.
- actual implementation date and time: 05-11-2026 15:42
- verification evidence: Final full unittest: 1272 tests, 753.848s, OK (skipped=1), exit 0; focused 267 OK + two later acceptance cases OK; fixture 91; transcript 26/26; compatibility compatible; docs 100 OK; check_docs/task matrix/state consistency/diff exit 0; strict isolated preview and 1616 local links/anchors OK. Exact commands/RED-GREEN: current-run evidence above.
- residual risks: Fresh Codex host/workflow activation not_verified; OR-A3 report-path hook portion deferred to GAP-05; no provider/model/promotion proof.
- follow-up: No remaining ORD implementation. Later PAOS-GAP/T30–T34 remain unstarted; T23–T29 preserved.

### Task `PAOS-ORD-02`

- Task: Соединить discovery с готовыми selectors и отделить task state от readiness
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранённый план; отдельный запрос владельца реализовать только ORD-01–ORD-06
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 15:42
- Depends on: PAOS-ORD-01; T26/T27
- Blocks: PAOS-ORD-03, PAOS-ORD-04
- Source: IMP-02/03
- Short description: Добавить небольшой validated adapter: audit inventory → ProjectInventory, task risks → TestStrategyRequest; вызвать select_code_quality_profile/select_test_strategy без переноса их логики. Передавать source refs и present_unverified. В state resolver разделить structural readiness, explicit task state и recommendation; принимать только известные значения с проверенным task/source binding. Не читать latest RUNLOG substring как authoritative state; не требовать builder для single-agent.
- Technical value: Реальные данные начинают управлять готовыми selectors; русский single-agent проект не возвращается на onboarding.
- Product value: Реальные данные начинают управлять готовыми selectors; русский single-agent проект не возвращается на onboarding.
- Scope: Owned files: `plugins/product-agent-os/scripts/product_agent_os/task_routing.py [proposed]`; `plugins/product-agent-os/scripts/codex_runtime_runner/state.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/context_loader.py`; `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Typed routing context и state provenance; docs owner architect, архитектурный контракт в этом плане, публичные страницы — ORD-06.
- Acceptance criteria: OR-A2/A6 проходят. Одинаковые RU/EN данные дают одинаковое решение; stale/conflicting state не превращается в build/release. Source-owned T29 status не преобразуется напрямую в lifecycle enum. Нельзя получить low-risk по умолчанию при unknown risk. T26/T27 behavior regressions GREEN.
- Verification gates: python -m unittest tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_batch45_code_quality_behavior -v — exit 0; параметризованные malformed, provenance, unknown-risk и RU/EN случаи.
- Risks / approval gates: Никакого exec найденных project commands; paths вне workspace и неподдерживаемая schema version отклоняются. Сохранить signature legacy infer_lifecycle_state либо добавить совместимый wrapper. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: high
- Estimated execution time: 1–2 рабочих дня
- Agents: plugin-runtime-builder; review: architect; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Typed routing context и state provenance; docs owner architect, архитектурный контракт в этом плане, публичные страницы — ORD-06.
- Next step: ORD-03 и затем ORD-04, один writer общих контрактов.

#### Completion Report

- status: implemented
- what was done: Discovery подключён к готовым T26/T27; structural readiness отделена от hash/task-bound state и явно неавторитетной recommendation.
- files touched / work locations: plugins/product-agent-os/scripts/product_agent_os/task_routing.py; plugins/product-agent-os/scripts/codex_runtime_runner/state.py; tests/product_agent_os/test_codex_runtime_runner_cli.py
- technical value delivered: Selectors переиспользованы; RU/EN, malformed/unknown/stale handling.
- product value delivered: Небольшая известная задача не требует builder/EVALS; uncertainty остаётся gap.
- actual implementation date and time: 05-11-2026 15:42
- verification evidence: Final full unittest: 1272 tests, 753.848s, OK (skipped=1), exit 0; focused 267 OK + two later acceptance cases OK; fixture 91; transcript 26/26; compatibility compatible; docs 100 OK; check_docs/task matrix/state consistency/diff exit 0; strict isolated preview and 1616 local links/anchors OK. Exact commands/RED-GREEN: current-run evidence above.
- residual risks: Fresh Codex host/workflow activation not_verified; OR-A3 report-path hook portion deferred to GAP-05; no provider/model/promotion proof.
- follow-up: No remaining ORD implementation. Later PAOS-GAP/T30–T34 remain unstarted; T23–T29 preserved.

### Task `PAOS-ORD-03`

- Task: Выбирать минимально достаточные инфраструктурные artifacts
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранённый план; отдельный запрос владельца реализовать только ORD-01–ORD-06
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 15:42
- Depends on: PAOS-ORD-01, PAOS-ORD-02
- Blocks: PAOS-ORD-04, PAOS-ORD-06
- Source: IMP-01
- Short description: Сохранить полный template registry и legacy caller contract. Добавить selection по task context отдельно от project profile; показать selected/omitted/reason в plan manifest. Existing-project ordinary reuse не создаёт полный пакет. Для новых requirements выбирать только применимые artifacts; full risk не включает hook/automation activation. Провести selection через dry-run и stage, сохранив нынешние protections.
- Technical value: Меньше ненужных документов при сохранении управляемого staging и rollback.
- Product value: Меньше ненужных документов при сохранении управляемого staging и rollback.
- Scope: Owned files: `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`; `plugins/product-agent-os/scripts/render_infrastructure.py`; `tests/product_agent_os/test_infrastructure_templates.py`; `tests/product_agent_os/test_infrastructure_renderer.py`; `tests/product_agent_os/test_render_infrastructure_cli.py`; `tests/product_agent_os/test_merge_infrastructure.py`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Selection manifest и reasoned exclusions; docs owner docs-maintainer, artifact-contracts RU/EN обновляются в ORD-06.
- Acceptance criteria: OR-A5 GREEN: ни один user-authored byte не изменён dry-run; repeated manifest детерминирован; stage вне target; unmarked files дают companion. Ordinary не содержит auto-added agents/hooks/automations; high-risk содержит необходимые gates. Legacy all-template inventory остаётся доступен явно, без ordinary activation claim. Existing merge approval binding не ослаблен.
- Verification gates: python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_infrastructure_renderer tests.product_agent_os.test_render_infrastructure_cli tests.product_agent_os.test_merge_infrastructure -v — exit 0; synthetic temporary targets создаются тестами. Native dry-run/stage paths проверяются through public CLI test, target apply не производится.
- Risks / approval gates: Не менять merge engine семантически для удобства selection; changing selected manifest invalidates прежний approval. Запрещено массово удалять templates. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: medium-high
- Estimated execution time: 1–2 рабочих дня
- Agents: plugin-runtime-builder; evidence owner: tester; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Selection manifest и reasoned exclusions; docs owner docs-maintainer, artifact-contracts RU/EN обновляются в ORD-06.
- Next step: ORD-04.

#### Completion Report

- status: implemented
- what was done: Task-scoped selection manifest: ordinary reuse, full восемь proposals, legacy 209; staging с gaps запрещён и остаётся вне target.
- files touched / work locations: plugins/product-agent-os/scripts/product_agent_os/templates.py; plugins/product-agent-os/scripts/product_agent_os/infrastructure.py; plugins/product-agent-os/scripts/render_infrastructure.py; tests/product_agent_os/test_infrastructure_renderer.py; tests/product_agent_os/test_render_infrastructure_cli.py
- technical value delivered: Детерминированный выбор artifacts; merge/companion/approval contracts сохранены.
- product value delivered: Нет лишних agents/hooks/automations или перезаписи пользовательских файлов.
- actual implementation date and time: 05-11-2026 15:42
- verification evidence: Final full unittest: 1272 tests, 753.848s, OK (skipped=1), exit 0; focused 267 OK + two later acceptance cases OK; fixture 91; transcript 26/26; compatibility compatible; docs 100 OK; check_docs/task matrix/state consistency/diff exit 0; strict isolated preview and 1616 local links/anchors OK. Exact commands/RED-GREEN: current-run evidence above.
- residual risks: Fresh Codex host/workflow activation not_verified; OR-A3 report-path hook portion deferred to GAP-05; no provider/model/promotion proof.
- follow-up: No remaining ORD implementation. Later PAOS-GAP/T30–T34 remain unstarted; T23–T29 preserved.

### Task `PAOS-ORD-04`

- Task: Подключить ordinary decision к настоящему CLI, route и result contracts
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранённый план; отдельный запрос владельца реализовать только ORD-01–ORD-06
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 15:42
- Depends on: PAOS-ORD-02, PAOS-ORD-03; T25/T26/T27
- Blocks: PAOS-ORD-05, PAOS-ORD-06
- Source: IMP-01/02/03
- Short description: Добавить opt-in --task-context JSON и соответствующий Python parameter; валидировать schema, source refs и workspace containment. Сформировать route из adapter outputs. _status_for проверяет missing required inputs выбранного маршрута, не все шесть. Выдавать compact contract, quality strategy, command provenance/applicability и routing trace. Contract-mode не исполняет commands и не меняет target. Evidence statuses отличают recommended/detected/executed/stale.
- Technical value: Первый реально связанный путь discovery → selectors → route → result.
- Product value: Первый реально связанный путь discovery → selectors → route → result.
- Scope: Owned files: `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/guards.py`; `tests/product_agent_os/test_codex_runtime_runner_cli.py`; `tests/product_agent_os/test_codex_runtime_runner_contracts.py`; `tests/product_agent_os/test_codex_runtime_runner_guards.py`; `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Production caller и machine-readable reasons/evidence gaps; docs owner docs-maintainer, cli-reference RU/EN в ORD-06.
- Acceptance criteria: OR-A1/A2/A4/A6/A8/A9 GREEN через public CLI, а не только direct selector calls. Trace содержит ordinary/legacy path и selector provenance; ordinary не замаскирован full fallback. Полный checklist остаётся reference; ≤8 compact fields. Mandatory project checks и approval guards приоритетны; source policy blocked остаётся blocked. Старые result consumers сохраняют совместимость или получают явно versioned contract error.
- Verification gates: python -m unittest tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_guards tests.product_agent_os.test_codex_runtime_runner_state_routes -v — exit 0; один subprocess public CLI case с validated structured context, отрицательный legacy-fallback detector.
- Risks / approval gates: Не считать allow_workspace_writes или approval_status из входного JSON полномочием. Не добавлять command executor; unknown/unsafe command остаётся proposal или blocked. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: high
- Estimated execution time: 1–2 рабочих дня
- Agents: plugin-runtime-builder; evidence owner: tester; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Production caller и machine-readable reasons/evidence gaps; docs owner docs-maintainer, cli-reference RU/EN в ORD-06.
- Next step: ORD-05, затем ORD-06.

#### Completion Report

- status: implemented
- what was done: Public --task-context подключён к route/result guards, trace, compact contract, risk checks и freshness receipts; sensitive Windows paths нормализованы.
- files touched / work locations: plugins/product-agent-os/scripts/codex_runtime_runner/cli.py; plugins/product-agent-os/scripts/codex_runtime_runner/routes.py; plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py; plugins/product-agent-os/scripts/codex_runtime_runner/guards.py; tests/product_agent_os/test_codex_runtime_runner_cli.py
- technical value delivered: Legacy совместимость; forged fallback/completed отклоняются.
- product value delivered: Явные причины маршрута, выбранные проверки и gaps без исполнения untrusted commands.
- actual implementation date and time: 05-11-2026 15:42
- verification evidence: Final full unittest: 1272 tests, 753.848s, OK (skipped=1), exit 0; focused 267 OK + two later acceptance cases OK; fixture 91; transcript 26/26; compatibility compatible; docs 100 OK; check_docs/task matrix/state consistency/diff exit 0; strict isolated preview and 1616 local links/anchors OK. Exact commands/RED-GREEN: current-run evidence above.
- residual risks: Fresh Codex host/workflow activation not_verified; OR-A3 report-path hook portion deferred to GAP-05; no provider/model/promotion proof.
- follow-up: No remaining ORD implementation. Later PAOS-GAP/T30–T34 remain unstarted; T23–T29 preserved.

### Task `PAOS-ORD-05`

- Task: Синхронизировать активный и packaged compact authoring workflow
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранённый план; отдельный запрос владельца реализовать только ORD-01–ORD-06
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 15:42
- Depends on: PAOS-ORD-04; T25
- Blocks: PAOS-ORD-06
- Source: IMP-02; active/package mismatch
- Short description: Применить уже выполненный T25 compact contract к активной копии, сохраняя project-specific обязательные правила. Reference full checklist не инжектируется по умолчанию. Указать отдельно ordinary authoring, high-risk gates и full lifecycle reporting. Синхронизировать packaged формулировки лишь при реальном semantic mismatch; не переписывать T25.
- Technical value: Оператор текущего workspace получает тот же компактный процесс, который уже предусмотрен package.
- Product value: Оператор текущего workspace получает тот же компактный процесс, который уже предусмотрен package.
- Scope: Owned files: `.codex/workflows/coding-standards.md`; `.codex/artifact-templates/code-change-contract.md [proposed]`; `plugins/product-agent-os/assets/templates/workflows/coding-standards.md`; `plugins/product-agent-os/assets/templates/artifact-templates/code-change-contract.md`; `tests/product_agent_os/test_batch45_coding_standards.py`; `tests/product_agent_os/test_task_plan_lifecycle.py`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Активный compact artifact и согласованный workflow; preservation diff с local-rule inventory.
- Acceptance criteria: Активный и staged workflow одинаково выбирают compact generation. Ни один локальный approval/test/source guard не потерян. Static tests и synthetic transcript cases подтверждают обычный/высокорисковый/неприменимый контекст. Изменение файлов не записывается как fresh-session activation.
- Verification gates: python -m unittest tests.product_agent_os.test_batch45_coding_standards tests.product_agent_os.test_task_plan_lifecycle -v; python plugins/product-agent-os/scripts/run_transcript_eval.py — exit 0; docs gate. Fresh-host invocation только отдельной разрешённой проверкой, до неё implemented_locally_verified.
- Risks / approval gates: Durable instruction change: baseline contexts и intent documented до edits. .codex filesystem approval остаётся применимым. Не менять hooks/trust/config или installed cache. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: medium
- Estimated execution time: 0.5–1 рабочего дня
- Agents: architect; docs owner: docs-maintainer; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Активный compact artifact и согласованный workflow; preservation diff с local-rule inventory.
- Next step: ORD-06.

#### Completion Report

- status: implemented
- what was done: Active coding workflow использует eight-field contract по умолчанию; полный checklist остаётся reference. Local guards и packaged T25 сохранены.
- files touched / work locations: .codex/workflows/coding-standards.md; .codex/artifact-templates/code-change-contract.md; tests/product_agent_os/test_batch45_coding_standards.py
- technical value delivered: Статическая active/staged parity без изменения hooks/trust/cache.
- product value delivered: Короткий pre-edit contract сохраняет применимые проверки и lifecycle.
- actual implementation date and time: 05-11-2026 15:42
- verification evidence: Final full unittest: 1272 tests, 753.848s, OK (skipped=1), exit 0; focused 267 OK + two later acceptance cases OK; fixture 91; transcript 26/26; compatibility compatible; docs 100 OK; check_docs/task matrix/state consistency/diff exit 0; strict isolated preview and 1616 local links/anchors OK. Exact commands/RED-GREEN: current-run evidence above.
- residual risks: Fresh Codex host/workflow activation not_verified; OR-A3 report-path hook portion deferred to GAP-05; no provider/model/promotion proof.
- follow-up: No remaining ORD implementation. Later PAOS-GAP/T30–T34 remain unstarted; T23–T29 preserved.

### Task `PAOS-ORD-06`

- Task: Закрыть сквозную локальную ordinary приёмку и RU/EN описание
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранённый план; отдельный запрос владельца реализовать только ORD-01–ORD-06
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 15:42
- Depends on: PAOS-ORD-01–05
- Blocks: Freeze ordinary baseline для T32; PAOS-GAP-06
- Source: IMP-01/02/03; OR-A1–A10
- Short description: Пройти public CLI на synthetic existing Python project: reproduce bug → task context → ordinary selectors → compact output → bounded local fix/check → final evidence. Использовать TemporaryDirectory и стандартные subprocess tests; никаких реальных target writes. Проверить RU/EN, docs-only, single-agent, high-risk, no-op и stale result. Зафиксировать positive selector activation и negative full-fallback proof. Синхронизировать пользовательские страницы и current pointers без rewriting historical receipts.
- Technical value: Завершённый локальный пользовательский путь с доказательствами вместо наличия отдельных функций.
- Product value: Завершённый локальный пользовательский путь с доказательствами вместо наличия отдельных функций.
- Scope: Owned files: `tests/product_agent_os/test_codex_runtime_runner_cli.py`; `tests/product_agent_os/test_codex_runtime_runner_fixture_eval.py`; `docs/product-agent-os/cli-reference.md`; `docs/product-agent-os/cli-reference.en.md`; `docs/product-agent-os/artifact-contracts.md`; `docs/product-agent-os/artifact-contracts.en.md`; `docs/product-agent-os/coding-standards.md`; `docs/product-agent-os/coding-standards.en.md`; `docs/product-agent-os/architecture.md`; `docs/product-agent-os/architecture.en.md`; `PLAN.md`; `RUNLOG.md`; `TEST.md`; `research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Completion Report данного плана, компактные PLAN/RUNLOG/TEST pointers; RU/EN parity. Данные замороженного runner baseline для T32.
- Acceptance criteria: Все OR scenarios в применимом локальном scope GREEN; OR-A3 path-specific hook часть явно относится к GAP-05. Итог содержит selected tests с risk reasons, actual exit/result/digest; no-op принят по correctness. Лишние artifact/check counts снижены на тех же fixtures без падения fault detection; это локальные измерения, не обещание времени/качества на всех проектах. Mandatory integrated gate GREEN; host activation отдельно not_verified.
- Verification gates: python -m unittest tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_codex_runtime_runner_fixture_eval -v — exit 0; затем обязательный integrated gate из раздела выше один раз и docs gate. Строгая MkDocs preview только при затронутой диаграмме/навигации или разрешённом build scope.
- Risks / approval gates: Остановить closure при failed guard, stale evidence или masked fallback. Не объявлять product release-ready, behavioral promotion или host workflow activation. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: medium-high
- Estimated execution time: 1–2 рабочих дня
- Agents: tester; docs owner: docs-maintainer; итоговая проверка: completion-skeptic либо явно self_review; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Completion Report данного плана, компактные PLAN/RUNLOG/TEST pointers; RU/EN parity. Данные замороженного runner baseline для T32.
- Next step: PAOS-GAP-01/02/03/04; T30/T31 могут готовиться по своему DAG.

#### Completion Report

- status: implemented
- what was done: Public CLI RED/GREEN и negative acceptance проверены; четыре RU/EN guide pairs, registry и control-plane pointers синхронизированы; frozen input manifest сохранён.
- files touched / work locations: docs/product-agent-os/{cli-reference,artifact-contracts,coding-standards,architecture}{,.en}.md; docs/sources/registry{,.en}.md; PLAN.md; RUNLOG.md; TEST.md; текущий план; tests/product_agent_os/test_codex_runtime_runner_cli.py
- technical value delivered: Full integrated + fixture/transcript/compatibility/docs evidence; same-fixture comparison.
- product value delivered: Сквозной ordinary route локально проверен с явными ограничениями.
- actual implementation date and time: 05-11-2026 15:42
- verification evidence: Final full unittest: 1272 tests, 753.848s, OK (skipped=1), exit 0; focused 267 OK + two later acceptance cases OK; fixture 91; transcript 26/26; compatibility compatible; docs 100 OK; check_docs/task matrix/state consistency/diff exit 0; strict isolated preview and 1616 local links/anchors OK. Exact commands/RED-GREEN: current-run evidence above.
- residual risks: Fresh Codex host/workflow activation not_verified; OR-A3 report-path hook portion deferred to GAP-05; no provider/model/promotion proof.
- follow-up: No remaining ORD implementation. Later PAOS-GAP/T30–T34 remain unstarted; T23–T29 preserved.

### Task `PAOS-GAP-01`

- Task: Свести current pointers и убрать неподтверждённые maturity claims
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Отдельный запрос владельца реализовать GAP-01–GAP-05
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 17:48
- Depends on: Предпочтительно после ORD-06; технически независимо от реализации ordinary route
- Blocks: Честный handoff и compatibility описание GAP-02
- Source: IMP-05/07
- Short description: Указать product integration queue отдельно от B45 next=T30. Старое Start T28 и прежний Stop contract пометить superseded с current receipt. Удалить Production-ready claim из manifest; placeholder URLs не заменять выдуманными реальными endpoints, а отразить local-package limitation. Сохранить historical receipts и unresolved backlog.
- Technical value: Пользователь и следующий исполнитель не возвращаются к закрытым задачам и неверным claims.
- Product value: Пользователь и следующий исполнитель не возвращаются к закрытым задачам и неверным claims.
- Scope: Owned files: `PLAN.md`; `RUNLOG.md`; `plugins/product-agent-os/.codex-plugin/plugin.json`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Согласованные current RU/EN pointers и честная local maturity metadata.
- Acceptance criteria: Единственный current pointer для B45 ведёт на T30; T23–T29 остаются завершёнными в прежнем evidence ceiling. ACT repair не назван unverified generic hook history. Manifest не обещает production readiness; никакого утверждения distribution readiness при placeholder metadata.
- Verification gates: python -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_codex_compatibility -v; python tools/check_docs.py; git diff --check — exit 0. Review current-vs-historical sections вручную по source-owned JSON; не добавлять большой validator лишь ради пары строк.
- Risks / approval gates: Не rewriting history; не менять T23–T34 statuses по новому плану; не выпускать новую версию и не публиковать package. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: low-medium
- Estimated execution time: 0.5 рабочего дня
- Agents: docs-maintainer; evidence owner: lifecycle-orchestrator; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Согласованные current RU/EN pointers и честная local maturity metadata.
- Next step: GAP-02 и дальнейшая очередь B45.

#### Completion Report

- status: implemented
- what was done: Current product/B45 pointers reconciled; historical T28/Stop receipts retained; manifest production-readiness wording replaced by local-package limits.
- files touched / work locations: `PLAN.md`; `RUNLOG.md`; `plugins/product-agent-os/.codex-plugin/plugin.json`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`
- technical value delivered: Current product/B45 pointers reconciled; historical T28/Stop receipts retained; manifest production-readiness wording replaced by local-package limits.
- product value delivered: Пользователь и следующий исполнитель не возвращаются к закрытым задачам и неверным claims. Local scope only.
- actual implementation date and time: 05-11-2026 17:48
- verification evidence: Final full unittest: 1284 tests, 848.832s, OK (skipped=1), exit 0; fixture 91/91 exit 0; transcript 26/26 exit 0; focused RED/GREEN and docs receipts in GAP verification log. Compatibility exit 1 needs_review explicitly remains open.
- residual risks: Historical runtime/site receipts remain dated; placeholder distribution URLs unchanged.
- follow-up: Continue from T30 only under its separate task scope.

### Task `PAOS-GAP-02`

- Task: Согласовать MCP/component inventory и capability matrix
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Отдельный запрос владельца реализовать GAP-01–GAP-05
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 17:48
- Depends on: GAP-01 для текста maturity; кодовый parser независим от ORD
- Blocks: Надёжная inventory часть B42 и будущая distribution review
- Source: IMP-04/05
- Short description: Сначала перепроверить официальную legacy/portable schema; общий read-only resolver возвращает format/version, normalized components и issues. Текущий flat .mcp.json обозначить legacy observed, schema support проверять явно, не легализовать по одному наличию context7. Подключить resolver к consumers и проверить legacy/portable/absent/conflicting/malformed fixtures. Разделить executor/orchestrator и App/CLI/IDE/component support; native plugin и standalone skill — разные capabilities.
- Technical value: Диагностика перестаёт одновременно сообщать compatible и пустой MCP inventory.
- Product value: Диагностика перестаёт одновременно сообщать compatible и пустой MCP inventory.
- Scope: Owned files: `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py [proposed]`; `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py`; `plugins/product-agent-os/scripts/product_agent_os/batch39_inventory.py`; `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/scripts/product_agent_os/system_file_hygiene.py`; `tests/product_agent_os/test_codex_compatibility.py`; `tests/product_agent_os/test_batch39_inventory.py`; `tests/product_agent_os/test_discovery.py`; `tests/product_agent_os/test_system_file_hygiene.py`; `docs/product-agent-os/codex-compatibility.md`; `docs/product-agent-os/codex-compatibility.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Normalized component contract и RU/EN capability matrix; source registry содержит checked scope/date.
- Acceptance criteria: Один package даёт одинаковый inventory во всех consumers. Malformed/unsupported не становится compatible. Отличаются absent, present_unverified, needs_review и host_verified, последний только при отдельном host receipt. Legacy package не мигрируется автоматически; priority при двух formats задокументирован и проверен по официальной schema.
- Verification gates: python -m unittest tests.product_agent_os.test_codex_compatibility tests.product_agent_os.test_batch39_inventory tests.product_agent_os.test_discovery tests.product_agent_os.test_system_file_hygiene -v; python plugins/product-agent-os/scripts/validate_codex_compatibility.py; docs gate — expected fixtures pass/reject по классу, current-package outcome честно recorded, не обязательно compatible до разрешения schema conflict.
- Risks / approval gates: Не запускать npx/MCP, не делать install, global config edit или portable migration. Unsupported current format — finding, а не основание ослабить validator. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: high
- Estimated execution time: 1–2 рабочих дня
- Agents: plugin-runtime-builder; review: security-privacy-supply-chain-reviewer; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Normalized component contract и RU/EN capability matrix; source registry содержит checked scope/date.
- Next step: GAP-03.

#### Completion Report

- status: implemented
- what was done: One supported-subset resolver feeds compatibility, package inventory, discovery, methodology and hygiene; portable/overlay precedence and malformed/escape cases tested.
- files touched / work locations: `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py`; `plugins/product-agent-os/scripts/product_agent_os/batch39_inventory.py`; `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/scripts/product_agent_os/system_file_hygiene.py`; `tests/product_agent_os/test_codex_compatibility.py`; `docs/product-agent-os/codex-compatibility.md`; `docs/product-agent-os/codex-compatibility.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`
- technical value delivered: One supported-subset resolver feeds compatibility, package inventory, discovery, methodology and hygiene; portable/overlay precedence and malformed/escape cases tested.
- product value delivered: Диагностика перестаёт одновременно сообщать compatible и пустой MCP inventory. Local scope only.
- actual implementation date and time: 05-11-2026 17:48
- verification evidence: Final full unittest: 1284 tests, 848.832s, OK (skipped=1), exit 0; fixture 91/91 exit 0; transcript 26/26 exit 0; focused RED/GREEN and docs receipts in GAP verification log. Compatibility exit 1 needs_review explicitly remains open.
- residual risks: Current flat MCP declaration remains needs_review; no full-schema or native-host claim.
- follow-up: Owner decides MCP migration before stronger package compatibility claim.

### Task `PAOS-GAP-03`

- Task: Продолжить существующие B42 M02/M04–M08 по provenance и skill exposure
- Status: blocked
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Отдельный запрос владельца реализовать GAP-01–GAP-05
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 17:48
- Depends on: B42 source matrix; GAP-02 для общего component inventory; ORD-05 для intended compact workflow
- Blocks: Fresh-host ordinary claim и GAP-06 target pilot на выбранной поверхности
- Source: IMP-06; B42-S1-M02/M04/M05/M06/M07/M08 — прежние task IDs сохраняются
- Short description: M02: source/package/cache normalized digest и effective selection path. M04/M05: отдельно определить safe read-only implicit class и explicit-only write/release/automation; изменить metadata только если owner выбрал такую policy, не по умолчанию. M07/M08: routing и synthetic regression cases. M06: отдельный разрешённый fresh-session probe exposure плюс invocation, результаты сохранять в owning B42 matrix, без raw chat. Этот блок — координация прежних задач, не их замена новым статусом.
- Technical value: Понятно, какая версия skill управляет задачей, и что действительно доступно пользователю.
- Product value: Понятно, какая версия skill управляет задачей, и что действительно доступно пользователю.
- Scope: Owned files: `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`; `plugins/product-agent-os/scripts/product_agent_os/validators.py`; `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`; `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`; `tests/product_agent_os/test_lifecycle_skills.py`; `tests/product_agent_os/test_validators.py`; `docs/product-agent-os/instruction-tool-use-compliance.md`; `docs/product-agent-os/instruction-tool-use-compliance.en.md`; approved follow-up extension: `plugins/product-agent-os/skills/agent-team-designer/agents/openai.yaml`; `plugins/product-agent-os/skills/docs-maintainer/agents/openai.yaml`; `plugins/product-agent-os/skills/implementation-planner/agents/openai.yaml`; `plugins/product-agent-os/skills/requirements-author/agents/openai.yaml`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Existing B42 task evidence и RU/EN guidance; cache остаётся неизменным без отдельной exact authority.
- Acceptance criteria: 11/12 drift из отчёта повторно проверен, а не принят за вечную константу; различаются installed, exposed, selected и invoked. Explicit-only отсутствие implicit invocation не считается поломкой. Source/cache mismatch не исправляется молча. Local metadata/eval evidence и fresh-host receipt имеют разные статусы.
- Verification gates: python -m unittest tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_validators -v; python plugins/product-agent-os/scripts/run_transcript_eval.py; docs gate — exit 0 для local scope. Fresh session с фиксированными source hashes и intended route: отдельный manual evidence gate, без него M06 не закрывать.
- Risks / approval gates: Installed cache/global settings/trust — вне workspace slice. Если нужен refresh, сначала concrete diff/destination/hash/rollback и approval; не смешивать его с T32–T34. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: medium-high
- Estimated execution time: 1–2 рабочих дня local; host/owner ожидание отдельно
- Agents: lifecycle-orchestrator; evidence owner: tester; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Existing B42 task evidence и RU/EN guidance; cache остаётся неизменным без отдельной exact authority.
- Next step: GAP-06 после successful intended-host probe либо сохранить explicit host gap.

#### Completion Report

- status: blocked
- what was done: Owner-approved four-file metadata correction subsequently applied (94 focused tests); local provenance and metadata validation, source/cache digests and explicit compliance/learning routing implemented; B42 current_execution preserves original task IDs and historical snapshot.
- files touched / work locations: `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`; `plugins/product-agent-os/scripts/product_agent_os/validators.py`; `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`; `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`; `tests/product_agent_os/test_lifecycle_skills.py`; `docs/product-agent-os/instruction-tool-use-compliance.md`; `docs/product-agent-os/instruction-tool-use-compliance.en.md`; `plugins/product-agent-os/scripts/product_agent_os/discovery.py (shared with GAP-02)`; approved follow-up: `plugins/product-agent-os/skills/agent-team-designer/agents/openai.yaml`; `plugins/product-agent-os/skills/docs-maintainer/agents/openai.yaml`; `plugins/product-agent-os/skills/implementation-planner/agents/openai.yaml`; `plugins/product-agent-os/skills/requirements-author/agents/openai.yaml`
- technical value delivered: Local provenance and metadata validation, source/cache digests and explicit compliance/learning routing implemented; B42 current_execution preserves original task IDs and historical snapshot.
- product value delivered: Понятно, какая версия skill управляет задачей, и что действительно доступно пользователю. Local scope only.
- actual implementation date and time: 05-11-2026 17:48
- verification evidence: Final full unittest: 1284 tests, 848.832s, OK (skipped=1), exit 0; fixture 91/91 exit 0; transcript 26/26 exit 0; focused RED/GREEN and docs receipts in GAP verification log. Compatibility exit 1 needs_review explicitly remains open.
- residual risks: Local implementation verified; M04 explicit-only decision and four metadata corrections completed locally; M06 fresh-host exposure/invocation remains required.
- follow-up: Four-file correction applied with explicit owner approval; authorize fresh-host probe separately; no cache/global write.

### Task `PAOS-GAP-04`

- Task: Исправить локальную source-policy эвристику без ложной проверки фактов
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Отдельный запрос владельца реализовать GAP-01–GAP-05
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 17:48
- Depends on: Отчёт IMP-08; независима от B45
- Blocks: Source-status consistency для последующих claims
- Source: IMP-08
- Short description: Разобрать URL стандартным parser; точный hostname для официальных domains из проверенного source map. Разделить source_present, claim_supported evidence и freshness; source header сам по себе не даёт verified. RU/EN одинаковы; suffix spoof, userinfo URL, malformed URL, plain Sources и stale checked date — negative cases.
- Technical value: Актуальные официальные ссылки не отклоняются, пустой заголовок не маскирует отсутствие evidence.
- Product value: Актуальные официальные ссылки не отклоняются, пустой заголовок не маскирует отсутствие evidence.
- Scope: Owned files: `plugins/product-agent-os/scripts/product_agent_os/source_policy.py`; `tests/product_agent_os/test_source_policy.py`; `docs/sources/registry.md`; `docs/sources/registry.en.md`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Honest source-presence classification и синхронный registry; docs owner research-source-analyst.
- Acceptance criteria: learn.chatgpt.com/platform.openai.com/developers.openai.com распознаются в согласованном scope; evil suffix и Sources-only не подтверждают claim. Не объявлять semantic verification там, где выполнена только link/presence проверка. Existing policies не ослаблены.
- Verification gates: python -m unittest tests.product_agent_os.test_source_policy -v; docs gate — exit 0; каждое before/after поведение воспроизводится focused tests.
- Risks / approval gates: Не создавать crawler, external updater или автоматически считать свежим недатированный claim. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: medium
- Estimated execution time: 0.5–1 рабочего дня
- Agents: plugin-runtime-builder; source review: research-source-analyst; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Honest source-presence classification и синхронный registry; docs owner research-source-analyst.
- Next step: Использовать corrected source policy в subsequent local gate.

#### Completion Report

- status: implemented
- what was done: Exact official HTTPS hostname classification separates source_present, claim_supported and freshness; header/spoof/date negatives tested.
- files touched / work locations: `plugins/product-agent-os/scripts/product_agent_os/source_policy.py`; `tests/product_agent_os/test_source_policy.py`; `docs/sources/registry.md`; `docs/sources/registry.en.md`
- technical value delivered: Exact official HTTPS hostname classification separates source_present, claim_supported and freshness; header/spoof/date negatives tested.
- product value delivered: Актуальные официальные ссылки не отклоняются, пустой заголовок не маскирует отсутствие evidence. Local scope only.
- actual implementation date and time: 05-11-2026 17:48
- verification evidence: Final full unittest: 1284 tests, 848.832s, OK (skipped=1), exit 0; fixture 91/91 exit 0; transcript 26/26 exit 0; focused RED/GREEN and docs receipts in GAP verification log. Compatibility exit 1 needs_review explicitly remains open.
- residual risks: Presence/date heuristics do not validate source contents or semantic claim support; no crawler or freshness guarantee.
- follow-up: Use claim-level source review when stronger evidence is needed.

### Task `PAOS-GAP-05`

- Task: Спроектировать и отдельно проверить bounded report authority для read-only анализа
- Status: blocked
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Отдельный запрос владельца реализовать GAP-01–GAP-05
- Validator target: detailed task blocks
- Date and time of task implementation: 05-11-2026 17:48
- Depends on: Отчёт IMP-09; ORD-06 для стабильной ordinary semantics; отдельное разрешение durable hook change
- Blocks: Полная OR-A3 path-specific acceptance; не блокирует остальные ordinary cases
- Source: IMP-09; новый случай, не переоткрытие ACT-F1–F6
- Short description: Сначала design review: read-only target + exact authorized output paths, current task binding, explicit new-task transition и scope expiry. Реализация только после отдельного scope approval. Canonicalize paths/aliases, отвергать traversal, broad directory grant и terminal-task reuse; права берутся из явной authority, не из поля data payload. Синхронизировать active/staged policy. Проверить прямой tool и nested functions.exec мутации; потом fresh-host probe на approved exact hashes.
- Technical value: Явно запрошенный отчёт сохраняется без путаницы между read-only исследованием и разрешённой записью результата.
- Product value: Явно запрошенный отчёт сохраняется без путаницы между read-only исследованием и разрешённой записью результата.
- Scope: Owned files: `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `.codex/workflows/task-plan-lifecycle.md`; `plugins/product-agent-os/assets/templates/workflows/task-plan-lifecycle.md`; `tests/product_agent_os/test_lifecycle_hooks.py`; `tests/product_agent_os/test_task_plan_lifecycle.py`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Design и локальные/host receipts в Completion Report этого блока; docs owner docs-maintainer.
- Acceptance criteria: Один разрешённый Markdown создаётся; соседний output, target source, config/hook, stale marker, terminal marker и escaped path запрещены. PreToolUse guards не ослаблены, Stop остаётся advisory. Local pass не закрывает fresh-host gate. Одного имени report.md или work_type=planning недостаточно для authority.
- Verification gates: python -m unittest tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_task_plan_lifecycle -v; docs gate; затем утверждённый positive/negative host probe с exact hash receipt. До trust/fresh-session evidence статус implemented_not_runtime_verified, не repaired runtime.
- Risks / approval gates: Высокий риск permission regression. Не вносить этот hook change как побочный эффект ordinary route. Сначала подготовить reviewable patch/negative evidence, trust approval финальным отдельным шагом; при отказе сохранить прежние guards. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: high
- Estimated execution time: 1–2 рабочих дня local; trust/fresh-session отдельно
- Agents: architect; implementation owner: plugin-runtime-builder; review: security-privacy-supply-chain-reviewer; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Design и локальные/host receipts в Completion Report этого блока; docs owner docs-maintainer.
- Next step: Закрыть OR-A3 только в пределах доказанного host scope.

#### Completion Report

- status: blocked
- what was done: Pinned report grant, explicit task transition and one literal create-only Markdown patch implemented; active/package source mirrored; direct/nested wire and negative/default-route cases passed.
- files touched / work locations: `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `.codex/workflows/task-plan-lifecycle.md`; `plugins/product-agent-os/assets/templates/workflows/task-plan-lifecycle.md`; `tests/product_agent_os/test_lifecycle_hooks.py`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`
- technical value delivered: Pinned report grant, explicit task transition and one literal create-only Markdown patch implemented; active/package source mirrored; direct/nested wire and negative/default-route cases passed.
- product value delivered: Явно запрошенный отчёт сохраняется без путаницы между read-only исследованием и разрешённой записью результата. Local scope only.
- actual implementation date and time: 05-11-2026 17:48
- verification evidence: Final full unittest: 1284 tests, 848.832s, OK (skipped=1), exit 0; fixture 91/91 exit 0; transcript 26/26 exit 0; focused RED/GREEN and docs receipts in GAP verification log. Compatibility exit 1 needs_review explicitly remains open.
- residual risks: implemented_not_runtime_verified: no report-mode trusted command installed, no fresh-host positive/negative receipt; preflight is not atomic.
- follow-up: Separate exact-hash command/grant trust approval and fresh-host probe before closing OR-A3.

### Task `B45-CQRR-T30`

- Task: Implement an independent blinded reviewer contract
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: План по отчёту; будущая реализация пока не разрешена
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: B45-CQRR-T29 — satisfied locally
- Blocks: B45-CQRR-T32, B45-CQRR-T33
- Source: B45 task-group T30, IMP-10
- Short description: Использовать T23 output validation и typed T29 evidence. Определить blinded reviewer request/result: neutral pair IDs, sanitized patch/context, deterministic evidence refs, structured findings и severity. Arm mapping хранится вне reviewer input; self-scores/target verdict исключены. Развести gate пригодности пары до review и final promotion gate после reviewer, чтобы не создать цикл T29 reviewer-required → T30 review-blocked.
- Technical value: Независимая оценка вместо самооценки primary model.
- Product value: Независимая оценка вместо самооценки primary model.
- Scope: Owned files: `plugins/product-agent-os/assets/templates/evals/code-quality-reviewer-rubric.json [proposed]`; `plugins/product-agent-os/scripts/codex_runtime_runner/reviewer_contract.py [proposed]`; `tests/product_agent_os/test_batch45_code_quality_reviewer.py [proposed]`; `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`; `PLAN.md`; `RUNLOG.md`; `TEST.md`; `EVALS.md`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Reviewer schema/rubric и synthetic gates; после выполнения — обновить только T30 в existing B45 task-group и краткий RUNLOG/TEST; docs owner architect, EVALS.md с новым gate.
- Acceptance criteria: Invalid schema или missing deterministic pair evidence блокирует review; перестановка arms не раскрывает labels; primary self-score не влияет на verdict. Critical correctness/security/data-loss/regression finding блокирует promotion независимо от среднего. Synthetic requests доказуемо label-free, реальные live blinding утверждения пока отсутствуют.
- Verification gates: python -m unittest tests.product_agent_os.test_batch45_code_quality_reviewer tests.product_agent_os.test_codex_runtime_runner_promotion_contract tests.product_agent_os.test_batch45_code_quality_metrics -v — exit 0; seeded label/self-score leakage, incomplete pair и critical override cases.
- Risks / approval gates: Никакого live reviewer call. Если T29 API не позволяет разделить pre/post review, сначала показать минимальное расширение promotion_contract.py и его теста как dependency amendment, без переписывания T29. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: high
- Estimated execution time: 1–2 рабочих дня
- Agents: architect; evidence owner: tester; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Reviewer schema/rubric и synthetic gates; после выполнения — обновить только T30 в existing B45 task-group и краткий RUNLOG/TEST; docs owner architect, EVALS.md с новым gate.
- Next step: T32 после T31; T31 не ждёт T30 по dependency graph.

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
- Plan trigger: План по отчёту; будущая реализация пока не разрешена
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: B45-CQRR-T27, B45-CQRR-T29 — satisfied locally
- Blocks: B45-CQRR-T32, B45-CQRR-T33
- Source: B45 task-group T31, IMP-10
- Short description: Собрать 12–16 synthetic/sanitized задач, ≥4 stack families и ≥5 risk classes. Manifest для каждого case: stable ID, stack/risk, acceptance, oracle/check command, expected fault classes, allowed files, privacy status, digest. Включить small fix, legacy, boundary/security, abstraction trap, perf applicability и reuse/config/deletion/no-new-code. Для каждой fixture перечислить exact member files в manifest до freeze; директория не даёт произвольный write scope. Заморозить hashes до treatment outputs.
- Technical value: Качество проверяется на разнообразных задачах, а не только внутренней структуре проекта.
- Product value: Качество проверяется на разнообразных задачах, а не только внутренней структуре проекта.
- Scope: Owned files: `tests/fixtures/product_agent_os/batch45/code-quality-corpus/ [proposed bounded fixture directory]`; `docs/superpowers/specs/batch45-code-quality-heldout-corpus.json [proposed]`; `tests/product_agent_os/test_batch45_code_quality_corpus.py [proposed]`; `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`; `PLAN.md`; `RUNLOG.md`; `TEST.md`; `EVALS.md`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Frozen corpus manifest и fixtures; status только T31 в existing B45 task-group; docs owner tester, EVALS.md corpus policy.
- Acceptance criteria: Каждый case executable либо имеет explicit readiness blocker до T33; нет зависимости на private target/service. Представительность покрывает требуемые stacks/risks; correct no-op не штрафуется. Нет secrets/PII/raw chat/absolute user paths. Изменение frozen case создаёт новую corpus version и инвалидирует сравнение, не подменяет прежний hash.
- Verification gates: python -m unittest tests.product_agent_os.test_batch45_code_quality_corpus -v — exit 0; manifest/schema, hash freeze, seeded fixture corruption, privacy/path и risk-coverage checks. Toolchain absence — blocked case, не silently skipped valid pair.
- Risks / approval gates: Не настраивать corpus после просмотра treatment; не устанавливать отсутствующий toolchain без разрешения. Baseline/treatment leakage invalidates run. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: high
- Estimated execution time: 2–3 рабочих дня
- Agents: tester; privacy review: security-privacy-supply-chain-reviewer; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Frozen corpus manifest и fixtures; status только T31 в existing B45 task-group; docs owner tester, EVALS.md corpus policy.
- Next step: T32 после T30.

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
- Plan trigger: План по отчёту; будущая реализация пока не разрешена
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: B45-CQRR-T25, B45-CQRR-T30, B45-CQRR-T31
- Blocks: B45-CQRR-T33
- Source: B45 task-group T32, IMP-10
- Short description: Freeze exact prompts/context digests, runner/config/source hashes, corpus/toolchain versions, primary model/effort и timeout policy. Обе arms используют один ordinary routing baseline. Единственное различие — compact pre-edit intervention T25; reviewer assistance/comment advisory/model switch не добавляются. Определить measured outcomes, tolerance, invalid-pair policy и no-op scoring до run. Отдельно зафиксировать будущий transport binding: текущий durable runner/model_output path; если reusable driver отсутствует, dependency gap должен блокировать T33, а не обходиться временным скриптом.
- Technical value: Результат эксперимента можно связать с одним изменением процесса.
- Product value: Результат эксперимента можно связать с одним изменением процесса.
- Scope: Owned files: `plugins/product-agent-os/assets/templates/evals/code-quality-baseline-prompt.md [proposed]`; `plugins/product-agent-os/assets/templates/evals/code-quality-treatment-prompt.md [proposed]`; `docs/superpowers/specs/batch45-code-quality-eval-design.json [proposed]`; `tests/product_agent_os/test_batch45_code_quality_eval_design.py [proposed]`; `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`; `PLAN.md`; `RUNLOG.md`; `TEST.md`; `EVALS.md`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Frozen eval design; обновить только T32 в B45 task-group и EVALS.md pointer; docs owner architect.
- Acceptance criteria: Prompt diff содержит только заявленную intervention; digest reproducible; модели/effорт/tools/timeouts одинаковы. Полный research/checklist не попадает в каждый prompt. Runner path и invocation contract воспроизводимы; нет ephemeral adapter или hidden change from ORD/cache/hooks.
- Verification gates: python -m unittest tests.product_agent_os.test_batch45_code_quality_eval_design -v — exit 0; single-factor diff, context digest и transport-contract cases. Проверить fixture воспроизведение baseline/treatment offline без вызова model.
- Risks / approval gates: Нельзя угадать provider/model values из старого approval. Конкретные значения design фиксируются перед T33, exact costs/call scope одобряются перед T34. Недоступный reusable driver — явный blocking gap, не plan shortcut. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: medium-high
- Estimated execution time: 1–2 рабочих дня
- Agents: architect; independent evidence check: completion-skeptic; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Frozen eval design; обновить только T32 в B45 task-group и EVALS.md pointer; docs owner architect.
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
- Plan trigger: План по отчёту; будущая реализация пока не разрешена
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: B45-CQRR-T24, T28, T29, T30, T31, T32
- Blocks: B45-CQRR-T34 preparation
- Source: B45 task-group T33, IMP-10
- Short description: На одном pinned state выполнить schema/normalization, deterministic metrics, reviewer pre/post gate, corpus freeze, prompt single-factor и synthetic transport end-to-end checks. Убедиться в отсутствии review-gate cycle. Привязать command exit/results к проверенным hashes. Записать pass/fail/blocked отдельно по gate; создать approval packet только после green local preflight.
- Technical value: Дорогой эксперимент не запускается на заведомо сломанном контракте.
- Product value: Дорогой эксперимент не запускается на заведомо сломанном контракте.
- Scope: Owned files: `docs/superpowers/specs/batch45-code-quality-local-readiness.json [proposed]`; `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`; `PLAN.md`; `RUNLOG.md`; `TEST.md`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Local readiness packet, existing T33 status и compact RUNLOG/TEST; docs owner completion-skeptic.
- Acceptance criteria: Valid fixtures проходят; каждая required invalid class и seeded fault ловится ожидаемым check. Blinding и reproducibility подтверждены. Все 12–16 cases имеют доступные локальные prerequisites; missing tools не превращаются в readiness. No provider/model/reviewer call. Одно missing gate сохраняет no-go.
- Verification gates: python -m unittest tests.product_agent_os.test_codex_runtime_runner_promotion_contract tests.product_agent_os.test_codex_runtime_runner_model_output tests.product_agent_os.test_batch45_code_quality_behavior tests.product_agent_os.test_batch45_packet_contracts tests.product_agent_os.test_batch45_code_quality_metrics tests.product_agent_os.test_batch45_code_quality_reviewer tests.product_agent_os.test_batch45_code_quality_corpus tests.product_agent_os.test_batch45_code_quality_eval_design -v — exit 0; docs gate; проверить reuse integrated evidence только на неизменном relevant state.
- Risks / approval gates: Не выдавать behavioral promotion из local preflight. Не создавать новый live approval packet при failed/blocked prerequisites. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: medium
- Estimated execution time: 0.5–1 рабочего дня
- Agents: completion-skeptic; evidence owner: tester; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Local readiness packet, existing T33 status и compact RUNLOG/TEST; docs owner completion-skeptic.
- Next step: Подготовить конкретный T34 approval packet; никаких calls до нового approval.

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
- Plan trigger: План по отчёту; будущая реализация пока не разрешена
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: B45-CQRR-T33 и новое exact owner approval
- Blocks: Promotion decision; production readiness этим не закрывается
- Source: B45 task-group T34; прежние T21 invalid pairs и T22 no-go
- Short description: T34a после T33: подготовить reviewable packet с exact transport invocation, model/effort, total primary/reviewer calls, wall/timeout/cost caps, data/retention, corpus/design/runner hashes, approved retries и stop policy. T34b только после exact approval: run frozen comparison, validate every output до aggregation, reviewer только после valid required pairs. Approval связывается с одним run и помечается consumed при первом call; последующие разрешённые calls внутри этого же bounded run учитываются в его cap, а не требуют повторной покупки authority. Новый run/retry вне approved policy требует нового approval. T34c: deterministic+reviewer decision.
- Technical value: Решение о promotion основано на сопоставимом эксперименте и независимой проверке.
- Product value: Решение о promotion основано на сопоставимом эксперименте и независимой проверке.
- Scope: Owned files: `docs/superpowers/specs/batch45-code-quality-eval-approval-packet.json [proposed]`; `docs/superpowers/specs/batch45-code-quality-eval-results.json [proposed]`; `docs/superpowers/specs/batch45-code-quality-promotion-decision.json [proposed]`; `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`; `PLAN.md`; `RUNLOG.md`; `TEST.md`; `EVALS.md`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Approval/results/decision packets; existing T34 machine status, EVALS/RUNLOG pointers; docs owner release-operator.
- Acceptance criteria: Все promotion-counted pairs schema-valid и имеют current deterministic evidence; независимый review без unresolved critical findings. Любое превышение frozen tolerance, invalid/missing pair или privacy issue оставляет no-go либо заранее предусмотренный explicit owner exception; exceptions не скрывать. Старый T20 approval не переиспользуется.
- Verification gates: После подготовки: python -m json.tool docs/superpowers/specs/batch45-code-quality-eval-approval-packet.json — exit 0 плюс semantic/hash/cap review. Exact live command берётся из validated T32/T34 packet, сейчас отсутствует и не разрешён. После run: promotion contract/metrics/reviewer tests, sanitized results validation, cap/retention ledger, docs/control-plane sync.
- Risks / approval gates: Source status остаётся approval_required_not_started; task-matrix planned лишь представление схемы, не снятие gate. Остановиться на первом invalid output, unapproved drift, privacy breach или critical finding. Publish/deploy/automation отдельно не разрешены. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: high
- Estimated execution time: 0.5–1 день подготовки/анализа; live длительность и стоимость только по approved packet
- Agents: release-operator; independent reviewer по approved policy; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Approval/results/decision packets; existing T34 machine status, EVALS/RUNLOG pointers; docs owner release-operator.
- Next step: Сохранить promotion/no-go decision с evidence ceiling; независимо оценить user outcomes GAP-06.

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

- Task: Проверить ordinary user outcomes через существующие B39/B44 manual packets
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: План по отчёту; будущая реализация пока не разрешена
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: ORD-06; GAP-03 для provenance выбранного host; GAP-05 только для report-authority сценариев
- Blocks: Решение о следующем улучшении; не даёт automatic promotion
- Source: IMP-11; существующие B39 feedback и B44 manual pilot
- Short description: Сначала read-only owner review existing packets. Зафиксировать 3–5 представительных ordinary задач: bugfix, docs, legacy, no-new-code, boundary change; конкретные targets и действия выбрать с owner до pilot. При точной authority выполнить bounded target journey; измерить время до полезного результата, лишние вопросы/artifacts, повторные проверки, acceptance correctness и owner intervention. Передать findings в существующий manual learning loop как candidates.
- Technical value: Проверка реального удобства и полезности после локальной инженерной приёмки.
- Product value: Проверка реального удобства и полезности после локальной инженерной приёмки.
- Scope: Owned files: `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json`; `prod_test.md`; `RUNLOG.md`; `research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`
- Non-goals: Неуказанные файлы, автоматические target/cache/global writes, provider/browser/Git/publication и повторная реализация T23–T29 вне scope. Исключения только по явно scoped later approval.
- Expected result: Существующие manual pilot/feedback receipts и краткий RUNLOG; без нового автоматического learning framework.
- Acceptance criteria: Каждый outcome связан с task/host/source version и evidence, failure не исключается из denominator. Нет причинного вывода о всей системе из одного pilot. Target/browser/provider actions выполнены только в названной authority. B39 no-go/release ceiling и B44 manual_only сохраняются до отдельных решений.
- Verification gates: Для report-only updates: docs gate и JSON parse existing summary. Для нового target pilot exact commands, target paths, owner, rollback и verification формируются в существующем packet до исполнения; до этого readiness=approval_required, concrete live command намеренно отсутствует — нельзя честно выдумать target.
- Risks / approval gates: Это сознательно gated future task, не plan_ready для target execution. Не считать один pilot достаточным основанием включить schedules или auto-apply. Rollback: только изменения данного slice относительно сохранённого baseline; чужие hunks и historical receipts сохранить.
- Complexity: medium
- Estimated execution time: 0.5–1 день подготовки; длительность pilot определяется approved targets
- Agents: product-manager; evidence owner: learning-loop-engineer; owner acceptance у пользователя; роли обозначают ownership, не запущенных subagents
- Skills: implementation-planner для scope/handoff; Python implementation: python-design-patterns и python-code-style; docs-maintainer для названного docs impact; только task-matching canonical skills
- Output artifacts: Существующие manual pilot/feedback receipts и краткий RUNLOG; без нового автоматического learning framework.
- Next step: Owner выбирает следующий candidate; promotion/automation остаются отдельными решениями.

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
