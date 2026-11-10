# TEST.md

## GAP-06 acceptance и исправление проверок — 2026-11-10

GAP-06 принят владельцем; T34 и fresh-session activation отдельно открыты. Исправления locally verified: full 1450 tests (skip 1), fixtures 91/91, transcripts 26/26; актуальные проверки: [owning evidence](research/product-agent-os-audit-closeout-tooling-2026-11-10.md). Regression command: `python -B -m unittest tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_fixture_eval_runner -v`; затем обязательные full/fixture/transcript/compatibility/docs gates. TEMP/TMP — `.codex-tmp/audit-closeout-2026-11-10`.

## G9 T11–T17 — принятые результаты реализации

G9 закрыта после приёмки T17; текущие docs-only checks: 131 tests, strict preview и static gates passed. Receipt — [G9 report](research/product-agent-os-g9-execution-report.md#приёмка-t17-и-закрытие-g9). Runtime/eval результаты ниже — ранее выполненные и принятые.

Полный suite: 1448 tests / 504.318s, OK (skipped=1); финальные affected/docs/lifecycle checks: 224 tests / 23.886s, OK; fixtures 91/91, transcripts 26/26, compatibility compatible, strict preview passed. Версии, команды и неуспешные попытки: [G9 execution report](research/product-agent-os-g9-execution-report.md). Использовать workspace TEMP/TMP `.codex-tmp/g9-tests/documentation-sync` и существующие полные gates; focused tests: `test_document_navigation`, `test_task_plan_lifecycle`, `test_control_plane_compaction`, `test_project_formation`.

## PAOS-AUD-G9 — принятый первоначальный пакет

Первоначальный принятый пакет T01–T10: Ran 1435 tests in 803.716s, OK (skipped=1); post-fix focused 57 OK; fixtures 91/91, transcripts 26/26; compatibility compatible; strict MkDocs isolated preview passed. [Точные команды, failed attempts, final docs/matrix checks и evidence ceiling](research/product-agent-os-g9-execution-report.md). Проверены actual process crash/recovery, source binding, preservation, conditional selection и три synthetic formation profiles. Host activation и M1 SQL runtime не доказаны.

## PAOS-AUD-G8 — verification, 2026-11-10

G8 commands: `python -B -m unittest discover -s tests -p "test_*.py" -q`; focused `test_control_plane_documents`, `test_control_plane_compaction`, `test_document_navigation`, `test_g8_control_plane`, renderer/merge/hygiene/lifecycle/state suites. Pilot packet: `python -B -m tests.product_agent_os.test_g8_control_plane --report docs/superpowers/specs/paos-aud-g8-control-plane-results.json --baseline .codex-tmp/g8-tests/g8-baseline`. Use process-local TEMP/TMP `.codex-tmp/g8-tests`; no dependencies installed. Fixture/transcript/compatibility, docs tests/checker, task matrix and diff gates remain mandatory. Strict MkDocs builds only to `.codex-tmp/g8-tests/site`. Exact outcomes and failed attempts: [execution report](research/product-agent-os-g8-execution-report.md).

Уточнение владельца 10.11.2026: подробные матрицы в `docs/planning/` сохраняются целиком, default 40k size trigger исключён; оглавления/control-plane и explicit per-file limits сохраняют ограничения. Audit matrix в `research/` остаётся целой; split отложен, прежний preview не разрешён. G8-T14 и закрытие G8 явно приняты владельцем; fresh-session activation отдельно.

## Проверки Web M1 — актуальный маршрут 2026-11-10

Source status: planned acceptance / no Web runtime evidence.

[Web-план v0.8](research/product-agent-os-web-task-manager-plan-2026-11-09.md), раздел «Матрица M1 DoD», владеет соответствием acceptance → owner task. PRD §17 / architecture §21 задают M1 profile. До implementation использовать существующие docs/control-plane checks ниже; не придумывать npm/build/E2E команды для отсутствующего приложения. PAOS-0001/0054 фиксируют реальные версии, команды и evidence paths.

| Проверяемая граница | Задачи-владельцы и evidence |
| --- | --- |
| Manifest, policy и secrets | 0001/0054/0039/0041: exact tuple, positive/negative contracts, credential isolation |
| Сессия, permissions, Stop, recovery | 0042/0043/0044/0055: SW-AC и UX-AC, duplicate/cleared/outcome; fixture отдельно от actual runtime |
| SQLite, FTS5 и данные | 0048/0049/0050/0051/0056: ST-AC и DATA-AC, conflicts/crash, restore rehearsal до switch, no lost deltas |
| UI и сквозная приёмка | 0004/0043/0045: M1 RU/EN, обе темы, a11y; real runtime + browser journey при закрытом Codex App по утверждённой матрице |

Live/provider/browser actions требуют применимой отдельной authority; их отсутствие — явный открытый gate, а не условный pass. Исторические проверки других направлений ниже не подтверждают Web M1. Текущие maintenance receipts: [аудит и архив control-plane](research/product-agent-os-control-plane-maintenance-2026-11-10.md).


## PAOS-AUD-G7 — current-run verification, 2026-11-10

T08 docs/acceptance-only: reuse unchanged T07 runtime suite; current frozen hashes verified. Current docs unittest 105 tests / 13.036 s; check_docs, matrix/state validators and diff check exit 0. Final acceptance edits checked below in execution report.

T07: full unittest 1379 / 516.855 s / exit 0 (1 platform skip); docs 105 / 7.834 s, fixture 91/91, transcript 26/26, compatibility passed. Exact commands, RED/GREEN и attempts — [execution report](research/product-agent-os-g7-execution-report-2026-11-09.md). TEMP/TMP: workspace `.docs-tools/reports/g7-deep-review-temp`. Attested comparison 12 admitted; oracle 6/6 на arm. Offline rescore hash-guards inputs, provider=0, published writes=0. T06 10/10 tool cases — прежний receipt, в этом T07 не повторялся.

## PAOS-AUD-G6 — 2026-11-09

G6 partially_verified: GAP-06 implemented / owner accepted 10.11.2026; все три synthetic local pilots приняты владельцем. HOST-01 не является их зависимостью. T34 no-go и fresh-session activation HOST-01/HOST-02 остаются открытыми отдельно; manual_only сохраняется. [Результаты](docs/superpowers/specs/paos-aud-g6-pilot-results.json).

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G5 — 2026-11-09

G5: 105 docs tests passed; check_docs, README CLI dry-run, compatibility и strict MkDocs exit 0; 368 HTML / 220 routes без link/anchor/search gaps; 93/93 Mermaid renders. Команды, RED/GREEN, retries и final logs — owning evidence и .docs-tools/reports/paos-aud-g5/. Installer tests используют stubs, не установку.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G4 — 2026-11-09

Full final: 1326 tests, 540.818 s, OK (skipped=1), exit 0; final focused 253 OK; template contracts 95 OK; fixtures 91/91; transcripts 26/26; compatibility exit 0, local structure only. Failed attempts и measurement provenance — owning plan. Final docs/matrix/consistency/diff checks обязательны после closure edits.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G3 — 2026-11-09

PAOS-AUD-G3: Full unittest: 1320 tests, 725.771 s, OK (skipped=1); final focused 78 tests OK; fixture 91/91; transcript 26/26; compatibility passed (local structure only). Current pointer только в PLAN.md; mismatch запрещает fallback. Source-policy needs_review не равен failed parser test. Failed attempts, UTC fixture correction, final checks и provenance — owning evidence.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G2 — 2026-11-09

PAOS-AUD-G2: full discovery 1305 tests, 748.949 s, OK (skipped=1), exit 0; final affected+docs 122 passed, после refactor final contracts 22 passed; fixture 91/91, transcript 26/26; compatibility exit 0, local structure only. Docs checker, hook validators и diff check passed. Проверять malformed/duplicate MCP, precedence, IDE unsupported conflict, unknown/old/version-surface, model mismatch, cache drift и read-only CLI; TEMP/TMP под ignored .docs-tools/reports/paos-aud-g2. Точные результаты и failed attempts — owning evidence.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G1 — 2026-11-09

PAOS-AUD-G1: full discovery 1297 tests, 532.640 s, OK (skipped=1), exit 0; affected suite 216 tests passed; final merge/renderer 67 tests passed после последнего alias-hardening. Fixture 91/91, transcript 26/26, docs 100/100; hook validators, parity/AST и native rules checks passed. Compatibility exit 1 needs_review — существующий G2/F01 legacy MCP gap. Даты, команды, failed attempts и provenance — owning evidence. Для повторения использовать ignored workspace TEMP/TMP под .docs-tools/reports/paos-aud-g1/tmp и PYTHONDONTWRITEBYTECODE=1; прежние TEMP cleanup failures не скрыты.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## Session lifecycle regression — 2026-11-09

`PAOS-SESSION-LIFECYCLE-2026-11-09`: run `python -m unittest tests.product_agent_os.test_lifecycle_hooks -v` for two-chat isolation, invalid/foreign identity, exact bootstrap, Windows case handling and SessionStart/Stop agreement, then required docs/template and plugin suites below. Current receipts: full discovery 1288 tests, one skip, exit 0; final affected suite 236 passed; fixture 91/91, transcript 26/26; hook validators/docs/diff passed. Compatibility exit 1 remains the existing legacy MCP gap. Exact state provenance and current-host versus synthetic evidence: `research/product-agent-os-session-lifecycle-fix-2026-11-09.md`. No trust or sandbox bypass is part of verification.

## Ordinary route integration — 2026-11-05

`PAOS-ORD-01-06-2026-11-05`: verify public contract and infrastructure CLIs, malformed/unknown/stale task inputs, RU/EN/no-builder parity, sensitive Windows paths, mandatory project checks, approval/source-policy guards, isolated RED/GREEN behavior and target-file preservation. Commands and current receipts: [owning plan](research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md). Final integrated verification passed: 1272 tests, 753.848s, OK (skipped=1), exit 0; fixture 91, transcript 26/26, compatibility and docs gates passed. Run the full unittest suite, fixture/transcript evals, compatibility validator, docs tests, docs checker and diff check. This slice uses an isolated TEMP and `PYTHONDONTWRITEBYTECODE=1`; sandbox TEMP failures are setup failures, not behavior evidence. Strict MkDocs output is isolated under `.docs-tools/reports/ordinary-route-preview`; root `site/` remains the earlier documentation build. Host activation and provider/model comparisons are separate gates.

## Documentation site refresh — 2026-11-05

For `PAOS-SITE-DOCS-REFRESH-2026-11-05`, run docs unittest and check_docs.py, approved strict MkDocs, existing `tools/fix_site_i18n_links.ps1`, then route/link/anchor/search checks, offline Mermaid parse/render and git diff --check. Run site-dependent docs tests after the build and postprocessing, not concurrently. Preserve plugin/tools/tests/config hashes. Evidence: `docs/superpowers/specs/site-docs-refresh-2026-11-05.json`. Observed: 100 docs tests passed; check_docs.py, strict build, 220 routes, all internal links/anchors/search routes and 93 Mermaid renders passed. Local RU/EN search and representative desktop/mobile pages checked. No runtime or hosted activation claim.


<!-- product-agent-os:start test -->
Project: Codex Docs / Product-Agent OS
Last compacted: 2026-07-07

## Purpose

`TEST.md` is the compact verification routing layer. It defines current checks, escalation boundaries and evidence owners. Detailed historical command logs and batch-specific command archives belong in [current control-plane state](docs/product-agent-os/control-plane-current-state.md), source backlogs, evidence packets and `prod_test.md`.

## Required Checks After Docs Or Control-Plane Changes

Run these checks after changes to root control-plane files, docs/source registry, templates or test contracts:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v
python -m unittest tests.product_agent_os.test_lifecycle_hooks -v
python plugins\product-agent-os\scripts\validate_hooks.py .codex\hooks.json
python plugins\product-agent-os\scripts\validate_hooks.py .codex\hooks
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
python tools\check_docs.py
git diff --check
```

Run strict MkDocs only when navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search/sitemap behavior or generated `site/` evidence changes. Full discovery remains the broad route:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Compatibility gate after PAOS-AUD-G2: `validate_codex_compatibility.py` exits 0 for the checked-in wrapped MCP declaration. This proves bounded local structure only; distribution remains gated and host diagnostics remain separate. Legacy flat, ambiguous and malformed inputs must still fail closed. Dated earlier needs_review receipts remain historical evidence, not current status.

## Required Checks After Plugin Or Runtime Changes

Use focused checks first, then broaden through the relevant project route:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_lifecycle_hooks -v
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

Use `timeout_ms: 1200000` for full Product-Agent OS unittest runs.

## Current Verification State

Исторические записи и результаты ниже относятся к указанным срезам. Они не меняют очередь Web M1 и не являются проверками текущего запуска. При расхождении используются текущие owning artifacts; перенос истории не закрывает оставшиеся gates.


| Area | Current evidence state | Required next check |
| --- | --- | --- |
| Batch 35 `T10-LIVE-M41` | Closed as `owner_closed_no_op_git_release_pr`; no git writes occurred. | Fresh git preflight and exact approval before any future git write. |
| Batch 38 cache/readiness | `B38-S2` records `plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage`; historical `blocked_pending_explicit_cache_mutation_approval` remains preserved. | Treat as historical unless a new cache mutation is requested. |
| Batch 39 | `B39-S1` through `B39-S5` are source-owned; S5 is `closed_for_owner_feedback_testing_not_release_ready`. | Use `prod_test.md`, S5 packets, focused tests, full unittest, fixture/transcript eval, Codex compatibility, docs check and diff hygiene before stronger claims. |
| Batch 41 | S9 modernization and Neural_Flow comparison are generated-artifact evidence. | Use focused first-run/cockpit renderer tests and docs checks; browser/Cosmos.gl/WebGL/target-apply proof requires approval. |
| Batch 42 | Historical planned-only snapshot plus GAP-03 local inventory/metadata/routing evidence in current_execution. | M04 explicit-only decision and four metadata corrections are locally verified; M06 fresh-host evidence remains open; no fixed-auto-engagement claim. |
| Batch 44 | Self-Learning Loop S0-S7 are local/staged/manual evidence. | Run focused state/extensions/docs tests before S8 decision; no automation claim without owner approval and activation proof. |
| Batch 45 | A04-A06 locally implement/focused-verify T23-T29. T28: families 34 (limit 98), exceptions 3 (limit 10), combined test LOC 5658 (<8130 baseline), focused route 48/48. T29/promotion: 23/23. | Local contracts only; T30-T33, live/CLI/provider/external reviewer/model behavior/promotion and T34 exact approval remain open. |
| Track 11 DOC-M25 | Root `site`, search and sitemap freshness are source-owned by DOC-M25 packet. | Root site freshness checks prove generated site/search/sitemap only; browser proof and broad scans remain separate. |
| GPT-5.6 `.codex` remediation | R1-R6 current evidence: agent validator 15/15 with zero config errors; focused contracts 184 OK; docs 100 OK; hooks 19 OK plus both hook validators; strict doctor 0 fail; fixture eval exit 0; transcript eval 26/26; compatibility `compatible`; full discovery 1195 OK with 1 skip; docs structure OK. Source: `docs/superpowers/plans/2026-08-05-gpt56-r1-r6-remediation.md`. | Maintain final diff/task-plan hygiene. Separately restart Codex for fresh MCP/`SessionStart` activation proof and run same-effort/one-lower-effort behavioral comparisons before promotion. |
| Lifecycle hooks / `B45-S9-H01` | Focused lifecycle/template suite 121/121 OK; both hook validators OK; docs 100/100 and checker OK; fixture eval exit 0; transcript eval 26/26; compatibility `compatible`. Broad discovery ran 1199 tests with one `Source status` formatting failure in the existing Batch 45 plan; the marker was corrected and the exact source-policy regression test reran green. Direct five-run script timing is diagnostic only: read fast path averaged 93.5 ms and current-file advisory 110.7 ms. | Use `/hooks` to review and trust changed hashes, then start a fresh task to collect real hook-runtime latency/activation evidence. Do not treat direct script timing as Codex App hook activation proof. |

## Batch-Specific Check Routes

| Batch or route | Compact check route | Evidence owner |
| --- | --- | --- |
| Batch 39 | `prod_test.md` attempt ledger, focused schema/collector/dashboard/route tests, fixture eval, transcript eval, Codex compatibility, docs check, diff hygiene. | `prod_test.md`; B39 packets. |
| Batch 44 | `python -m unittest tests.product_agent_os.test_self_learning_state tests.product_agent_os.test_self_learning_extensions -v`, staged initializer/runner/export checks as scoped by packet, docs check, diff hygiene. | B44 packets; `docs/product-agent-os/self-learning-loop.md`. |
| Batch 45 Professional Code Authoring | Focused `test_comment_sufficiency`, `test_batch45_s3_professional_code_authoring`, `test_coding_standards_artifacts`, automation/self-learning tests where touched, docs check, diff hygiene. | B45 packets; `docs/product-agent-os/coding-standards.md`. |
| Batch 45 retest/post-Q4 | `python -m json.tool` for changed B45 packets, including `docs\superpowers\specs\batch45-postq4-t17-frozen-heldout-corpus.json`, `docs\superpowers\specs\batch45-postq4-t18-promotion-grade-eval-design.json`, `docs\superpowers\specs\batch45-postq4-t19-cost-timeout-retention-policy.json`, `docs\superpowers\specs\batch45-postq4-t20-promotion-grade-eval-approval-packet.json`, `docs\superpowers\specs\batch45-postq4-t20-promotion-grade-eval-approval-packet-1000s.json`, `docs\superpowers\specs\batch45-postq4-t21-promotion-grade-eval-run-preflight-blocked.json`, `docs\superpowers\specs\batch45-postq4-t21-promotion-grade-eval-run-preflight-timeout-mismatch.json`, `docs\superpowers\specs\batch45-postq4-t21-promotion-grade-eval-results.json` and `docs\superpowers\specs\batch45-postq4-t22-promotion-grade-decision-packet.json`, `python -m unittest tests.product_agent_os.test_codex_runtime_runner_model_output -v`, `python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v`, docs check, diff hygiene. | Q0-Q4 and T01-T22 packets. |
| Batch 45 code-quality runtime recovery | T28 semantic/seeded-fault route 48/48; T29/promotion route 23/23; execution-loop/report route 7/7; final affected-contract route 208/208; Product-Agent OS docs 100/100; strict MkDocs build exit 0 with 652 generated files restored. | Task-group owns machine status; plans own detail; RUNLOG owns evidence; TEST owns ceiling. Hook activation remains a clean-session gap. |
| Track 11 docs toolchain | Project-local `.venv-docs`, `.docs-tools/node`, `.docs-tools/bin`, `.docs-tools/reports`, `docs/assets/javascripts/vendor` checks only within approved scopes. | Track 11 plan and DOC-M34..DOC-M41 packets. |

## Control-Plane Size Budgets

Root control-plane files use a compactness budget. `RUNLOG.md` keeps the historical `50 KB` (`50 * 1024` UTF-8 bytes) guard; the same overflow discipline applies to `PLAN.md`, `TEST.md`, `EVALS.md` and `REQUIREMENTS.md`. If a required update would exceed the budget, run `.codex/workflows/control-plane-sync.md` as `overflow_refactor_required`: route scope to `REQUIREMENTS.md`, sequencing to `PLAN.md`, verification to `TEST.md`, eval/claim ceilings to `EVALS.md`, detailed evidence to source-owned plans/specs/backlogs or `prod_test.md`, then keep root files as current pointers.

## MkDocs Runtime Location

Use the project-local docs runtime for current docs checks:

```powershell
.venv-docs\Scripts\python.exe -m mkdocs --version
.venv-docs\Scripts\python.exe -m mkdocs build --strict
```

The default `python` may not have MkDocs installed. Historical fallback paths such as `C:\tmp\codex_docs_mkdocs` or `tmp\mkdocs_deps_b40s4` are historical evidence only.

## Runtime And External-Action Verification Boundaries

Fresh explicit approval is required before:

- target workspace mutation;
- browser automation;
- provider/API calls;
- live server or dashboard launch;
- canonical graph-source mutation;
- git branch creation/switching, stage, commit, push, tag or PR;
- publication, deployment or external automation creation.

Approval for one surface does not authorize another. Runtime launch approval does not authorize browser automation; browser approval does not authorize provider calls; provider-call approval does not authorize canonical mutation or git/release actions.

For real-project target tests, the default verification mode is read-only: inventory, route classification, source-policy status, control-plane presence, safe artifact maps, counts, digests and redacted summaries.

## Historical Evidence Owners

| Marker | Evidence owner |
| --- | --- |
| `T10-LIVE-M41`, `owner_closed_no_op_git_release_pr` | `docs/sources/product-agent-os-track-10-backlog.md`, `docs/sources/product-agent-os-batch35-approval-packet-draft.md` |
| `blocked_pending_explicit_cache_mutation_approval`, `B38-S2` | `docs/sources/product-agent-os-track-10-backlog.md`, `docs/product-agent-os/control-plane-current-state.md` |
| `B39-TEST-M01..M54`, `B39-S1..B39-S5` | `prod_test.md`, B39 packets |
| `B40-S2..B40-S5`, `manual_only`, `not_promoted` | `docs/sources/product-agent-os-track-10-backlog.md` |
| `B41-S1..S9` | B41 packets and Track 10 backlog |
| `B42-S1..S5` | `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json` |
| `B44-S0..S7` | B44 packets and Track 11 plan |
| `B45-PCA-M24..M27`, `B45-PCA-M37-A01`, `B45-POSTQ4-T15-A01`, `B45-POSTQ4-T16-T22-A01`, `B45-POSTQ4-T17-A01`, `B45-POSTQ4-T18-A01`, `B45-POSTQ4-T19-A01`, `B45-POSTQ4-T20-A01`, `B45-POSTQ4-T20-A02`, `B45-POSTQ4-T20-A03`, `B45-POSTQ4-T21-PREFLIGHT-A01`, `B45-POSTQ4-T21-PREFLIGHT-A02`, `B45-POSTQ4-T21-PREFLIGHT-A03`, `B45-POSTQ4-T21-COST-WAIVED-RUN-A01`, `B45-POSTQ4-T22-A02`, `B45-CQRR-A01`, `B45-CQRR-A02`, `B45-CQRR-A03`, `B45-CQRR-T23..T34` | B45 packets, Track 11 plan and registry |
| `DOC-M34..DOC-M41`, `DOC-M25` | Track 11 plan and documentation-refresh packets |
| Track 8 / Track 9 / Track 10 | `docs/sources/product-agent-os-track-8-detailed-backlog.md`, `docs/sources/product-agent-os-track-9-backlog.md`, `docs/sources/product-agent-os-track-10-backlog.md` |
| Source registry | `docs/sources/registry.md`, `docs/sources/registry.en.md` |

## Compatibility Anchors

Compact route anchors: `B37-S1`, `T10-PLAN-M01..M03`, `T10-PLAN-M18`, `task-matrix contract`, `task-matrix-plan.md`, `B39-TEST-M21-A01..A03`, `B39-TEST-M22-A01..A03`, `B39-TEST-M23..M33`, `B41-S5-M21..M23`, `B41-S6-M24..M30`, `B41-S7-M31..M40`, `B41-S8-M41..M47`, `B42-S1..S5`, `B44-S0` through `B44-S7`, `B45-RETEST-Q0-Q2-A01`, `B45-RETEST-Q3-FIXTURE-STATIC-A01`, `B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01`, `B45-POST-Q4-NEXT-TASKS-A01`, `B45-POSTQ4-T01-T04-A01`, `B45-POSTQ4-T05-A01`, `B45-POSTQ4-T05B-A01`, `B45-POSTQ4-T06-A01`, `B45-POSTQ4-T08-A01`, `B45-POSTQ4-T10-A01`, `B45-POSTQ4-T11-A01`, `B45-POSTQ4-T12-RUN-A01`, `B45-POSTQ4-T13-A01`, `B45-POSTQ4-T14-A01`, `B45-POSTQ4-T14-RUN-A01`, `B45-POSTQ4-T15-A01`, `B45-POSTQ4-T16-T22-A01`, `B45-POSTQ4-T17-A01`, `B45-POSTQ4-T18-A01`, `B45-POSTQ4-T19-A01`, `B45-POSTQ4-T20-A01`, `B45-POSTQ4-T20-A02`, `B45-POSTQ4-T20-A03`, `B45-POSTQ4-T21-PREFLIGHT-A01`, `B45-POSTQ4-T21-PREFLIGHT-A02`, `B45-POSTQ4-T21-PREFLIGHT-A03`, `B45-POSTQ4-T21-COST-WAIVED-RUN-A01`, `B45-POSTQ4-T22-A02`.

## Completion Claim Rule

Do not say that a feature works, a bug is fixed, tests pass, a release is ready, or behavior is verified unless:

- the relevant check ran in the current run; or
- the claim is explicitly scoped to earlier evidence and the evidence owner is named; or
- the missing verification is recorded as an accepted gap.

<!-- product-agent-os:end test -->

## Documentation refresh verification — 2026-11-03

Task: `PAOS-DOCS-REFRESH-2026-11-03`. Run the mandatory docs/control-plane route above, both new task-matrix validators, changed TOML/JSON example parsing, semantic RU/EN review, official-link/source comparison, protected-file hashes and strict MkDocs with `--site-dir .docs-tools/reports/gpt6-docs-preview`. The existing `.venv-docs` runtime is used without dependency installation. A preview build does not update or prove freshness of root `site/` and is not browser evidence.

Initial check after plan creation: combined four-module suite ran 224 tests, exit 1 (15 failures, 33 errors); errors include Windows temporary-directory permissions, new-page counts and a legacy validator hardcoding the August plan. Both hook validators and docs checker passed. Agent validator remains exit 1: `project config must set sandbox_mode = workspace-write`; this was already found in the read-only audit and is outside implementation scope. These are initial observations, not final acceptance. Current final evidence belongs to the [refresh plan](docs/superpowers/plans/2026-11-03-gpt6-documentation-refresh.md) and RUNLOG.

Docs inventory maintenance accounts for three new localized page pairs while preserving historical site-promoted counts and pending-site semantics. It does not weaken assertions. Temporary files use an authorized workspace directory if the inherited TEMP cannot support the tests. Repeat only checks whose inputs or execution environment changed.

Final refresh evidence: 224 tests passed across the four required modules (100 + 5 + 25 + 94); both hook validators, task matrices, task-state consistency, docs structure and diff checks passed. Strict preview build passed; 20 official sources and 10 complete TOML/JSON examples checked. Root site and runtime activation remain unverified/unchanged. The agent-validator failure is a separate retained technical gap, not a green result.
