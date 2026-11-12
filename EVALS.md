# EVALS.md

## G9 T17 — граница сравнения

Детерминированное сравнение на одинаковых входах: обнаружение межфайлового дубликата 0/1 → 1/1; canonical aliases 1/4 → 4/4; изменён один раздел одного файла, изменений соседних bytes и повторных записей нет. Отсутствующему section route baseline не присваиваются выдуманные оценки. Шесть сценариев инструкций проверены статически; модельный поведенческий прогон не выполнялся. Смысловая полнота требует review и не доказывается digest; эта граница явно принята владельцем в T17; модельный прогон по-прежнему не выполнен. [Проверки](research/product-agent-os-g9-execution-report.md), [результаты](docs/superpowers/specs/paos-aud-g9-project-formation-results.json).

## PAOS-AUD-G9 — результаты для приёмки

G9 comparison: одинаковые synthetic workspace и факты task context; desired domains отдельно отмечены как неподдерживаемые baseline. Baseline snapshot/revision сохранён до edits. Профили: empty, existing docs, monorepo+AI. Проверки: состав и объяснимость, ссылки, exact-byte preservation, stale/authority failures, repeat/no writes, process-crash recovery, next change. [Результаты](docs/superpowers/specs/paos-aud-g9-project-formation-results.json); [границы](research/product-agent-os-g9-execution-report.md). Количество файлов не является quality score; model/token/cost superiority не заявляется. Initial G9/T10 accepted; extension T17 accepted with stated model-behavior limits; G9 closed.

## PAOS-AUD-G8 — comparison contract, 2026-11-10

Frozen synthetic profiles: Trade-like strict 20 000 bytes/history, myPartners-like mirrors/eval gate, site-like duplicates/cross-repo refs. Same-input legacy/scoped renderer comparison and before/after exact-byte preservation; no model A/B or token/cost advantage claim. Required: 3/3 flows, zero lost original bytes/gates/IDs/evidence, fail-closed stale hash/unknown authority/broken links, exact recovery and next-change continuation. [Results](docs/superpowers/specs/paos-aud-g8-control-plane-results.json), [limits and failures](research/product-agent-os-g8-execution-report.md). Simulated redirect detection is separate from real filesystem symlink/junction evidence; owner acceptance and fresh-session activation are not inferred.

Уточнение владельца 10.11.2026: подробные матрицы в `docs/planning/` сохраняются целиком, default 40k size trigger исключён; оглавления/control-plane и explicit per-file limits сохраняют ограничения. Audit matrix в `research/` остаётся целой; split отложен, прежний preview не разрешён. G8-T14 и закрытие G8 явно приняты владельцем; fresh-session activation отдельно.

## Web M1 — scope v0.7 / очередь v0.8, 2026-11-10

PAOS-0025 correctness baseline: existing no-replay/Stop/ownership + explicit checkpoint continuation, real fixture process crash и actual App jobs через restart. Identity/evidence/policy drift negatives обязательны; retry остаётся bounded и расходует прежний budget. [Evidence](research/product-agent-os-web-m3-0025-execution-2026-11-12.md). Model-quality/token/cost/SLO promotion не заявляется.

Исторический срез до PAOS-0025 (provenance сохранён): PAOS-0024 eval ceiling: deterministic queue/assignment/physical ownership с manual/single-workspace baseline; distinct-root concurrent native commands и exact-run Stop дополнены actual App worker proof. Five-project cap и root/alias negatives обязательны. Это correctness/routing evidence, не model-quality/cost/latency promotion. [Evidence](research/product-agent-os-web-m3-0024-execution-2026-11-12.md).

Исторический срез до PAOS-0024 (provenance сохранён): Source status: project-authored / PAOS-0037 local orchestration verified. Recipe/ordinary Send и Manual сравниваются по admission, pinned context, policy, replay и outcomes; representative/edge/negative fixtures дополняются actual App two-step proof. Это функциональная проверка маршрута, не улучшение качества модели; scores/cost/latency не измерены. [Evidence и ограничения](research/product-agent-os-web-m3-0037-execution-2026-11-12.md).

Исторический срез до PAOS-0037 (provenance сохранён): Source status: planned evaluation route; implementation_not_started.

Owning acceptance — матрица M1 DoD в [Web-план v0.8](research/product-agent-os-web-task-manager-plan-2026-11-09.md); UX определяется [wireframes v0.7](research/product-agent-os-web-m1-wireframes-2026-11-09.md). Старый Web v0.5 receipt архивирован; критерии M2–T1 не являются критериями M1.

- Детерминированные contracts, migration/restore, policy enforcement, dedup и project isolation проверяются по TEST.md; количество тестов и synthetic pass не заменяют runtime evidence.
- Пользовательский путь оценивается на ясность source/coverage, роли агента, permission vs product decision, результата действия, lossless recovery и ручной приёмки задачи. Empty/partial/unknown не должны выглядеть как полный контекст или success.
- При изменении agent prompts/routing сравнивать доступный baseline на representative/edge/negative cases; отделять корректность orchestration от качества ответа модели. Пока таких Web runs нет, scores/cost/latency не указывать.
- Для PAOS-0045 требуется evidence по всем применимым M1 acceptance IDs. Отсутствующая capability, потеря данных, нарушение project/permission boundary или неподтверждённый action outcome блокируют соответствующий gate.
- AUTH/commercial evidence принадлежит PAOS-0039/0046 и повторной проверке PAOS-0030; documentation alignment не даёт commercial acceptance.

Существующие Thresholds, rubrics и запреты promotion ниже сохранены. Новые численные пороги этой правкой не вводятся. Текущая maintenance-проверка и архив: [аудит и архив control-plane](research/product-agent-os-control-plane-maintenance-2026-11-10.md).


## PAOS-AUD-G7 — separate instrument

T08: T06/T07/final decision owner accepted; G7 closed locally. Thresholds/design unchanged, no new model run. Component decisions and acceptance boundary: [report](research/product-agent-os-g7-execution-report-2026-11-09.md).

G7 attested design v2: 12 sequential paired generations, gpt-6.1-sol/medium/tools=[], одинаковый общий context после bound marker/transport normalization. Frozen oracle: 6/6 на arm; 2 prior ineligible attempts и 10 diagnostic calls отдельно. Pressure/reuse passed; superiority и component effect insufficient_evidence. No OS isolation/E2E; 1 repetition, rehearsed corpus, uneven prompt caching. Prior observational pilot не переименован. [Evidence](research/product-agent-os-g7-execution-report-2026-11-09.md).

## PAOS-AUD-G6 — 2026-11-09

G6 partially_verified: GAP-06 implemented / owner accepted 10.11.2026; все три synthetic local pilots приняты владельцем. HOST-01 не является их зависимостью. T34 no-go и fresh-session activation HOST-01/HOST-02 остаются открытыми отдельно; manual_only сохраняется. [Результаты](docs/superpowers/specs/paos-aud-g6-pilot-results.json).

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G5 — 2026-11-09

G5 проверяет command routing и documentation/build integrity. Offline failures не дают network fallback; successful CLI exit не снимает context gaps. Mermaid render не доказывает host activation. Новые model/behavioral evals не применимы; прежний G4 run имеет прежнюю provenance; G6 gates открыты.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G4 — 2026-11-09

Source read-set comparison отделён от live behavioral evaluation. 93 moved sections сохранены; 12 metadata unchanged. Typical/edge/adversarial contract gates должны сохраняться. Model/effort/B45 compact-contract treatment не меняется. Partial input не разрешает legacy fallback; unchanged evidence требует original provenance.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G3 — 2026-11-09

PAOS-AUD-G3: invalid/future/stale/missing dates, local registry escape/broken refs, empty/rejected feedback и historical/current/conflict cases различены. Date/URL не semantic verification; owner_label_supported не positive sentiment/promotion; source status не owner acceptance. No-pointer B37 fallback сохраняется; malformed/stale pointer не разрешает historical fallback.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G2 — 2026-11-09

PAOS-AUD-G2: receipt не повышает documented unsupported; model ID/config не доказывает account access или promotion. Для missing/unknown version, unknown trust и отсутствующего cache запрещён fabricated pass. Match component digest не доказывает full package или host selection. Deterministic fixtures сравниваются с RED baseline; provider quality/cost thresholds и T23–T29 сохраняются.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G1 — 2026-11-09

PAOS-AUD-G1: deterministic guard comparisons покрывают compound/unknown commands, inert patch prose, exact hooks discovery path, selected-SID ACL repair/restore и pinned report-authoring create/update. Сохраняются legacy create-only и session isolation. Local checks не доказывают hook trust, fresh-host activation, реальные ACL или атомарную запись между hook и tool; AUD-HOST-02 остаётся открытым. Порогов model/provider evals эта группа не меняет.

[Owning plan и evidence](research/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## Session lifecycle contract cases — 2026-11-09

`PAOS-SESSION-LIFECYCLE-2026-11-09`: another chat's terminal/active marker must neither block nor authorize this chat. Missing/invalid/foreign own identity denies recognized mutations; exact own-marker bootstrap remains possible. Preserve legacy behavior only for payloads without session_id and preserve pinned-report restrictions. These deterministic regression cases supplement existing gates; they do not establish fresh-host multi-chat activation. Evidence: `research/product-agent-os-session-lifecycle-fix-2026-11-09.md`.

<!-- product-agent-os:start evals -->
Project: Codex Docs / Product-Agent OS
Last compacted: 2026-07-07

## Purpose

`EVALS.md` is the compact evaluation routing layer for current Product-Agent OS work. It stores rubrics, thresholds, active eval routes and unsupported-claim rules. Historical eval narratives and batch evidence live in [current control-plane state](docs/product-agent-os/control-plane-current-state.md), source backlogs, registry entries and evidence packets.

## Rubrics

- Source grounding: official sources and checked-in docs drive durable rules; community claims stay in insight/research layer.
- Evidence before completion: ready/completed/fixed/works/release claims require current command evidence, current eval evidence, current runtime evidence or explicit inspection-only gap.
- Conditional applicability: methodology gates can be `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, `applicable_missing` or `approval_required`.
- Owner sufficiency: artifacts prove evidence shape and routing; a human owner still judges whether evidence is sufficient for real project risk.
- Source boundary: generated dashboards, graph outputs, HTML views, scorecards and `site/` builds are orientation evidence unless an owning source document says otherwise.
- Real-project evidence: deterministic fixtures prove contract shape, but Product-Agent OS product confidence requires real-project target evidence where the route depends on actual project structure, source policy, workflow, runtime signals or owner judgment.
- Approval boundary: live servers, browser automation, provider/live external model/API calls, production data access, canonical graph source mutation, external writes and git stage/commit/push/PR remain approval-bound.
- Documentation quality: user-facing docs are Russian, behavior-level and name inputs, outputs, verification, risks and next artifact.
- Safety: secrets, private data, raw prompts/traces and absolute user-specific paths are not eval fixtures, examples or templates.

## Thresholds

- Blocking failure: unit test failure, fixture eval failure, transcript eval failure, docs check failure, strict MkDocs failure after nav/MkDocs-sensitive changes, Codex compatibility regression or approval-bound action performed without approval.
- Accepted gap: allowed only when reason, owner, evidence owner, downstream risk and follow-up are explicit.
- Residual risk: must be carried into `RUNLOG.md` and the final response.
- Unsupported claim: any quality, readiness, release, security, AI/RAG, runtime or product-success claim without current evidence must be rejected or labeled inspection-only.
- Synthetic-only limitation: internal `codex_docs` fixtures cannot support broad real-project usefulness, product-success, release-readiness, automation promotion or mass-user readiness without representative real-project evidence or owner-reviewed accepted gap.
- Batch 45 promotion: no promotion unless current approved comparable evidence clears deterministic correctness/regression gates and an independent blinded reviewer gate. T14 `+3.27%` with reviewer `0` remains non-promotional; T21 aborted with `valid_pair_count=0`; T22-A02 remains no-go. A06 locally implements T28/T29: acceptance, regression, seeded-fault, reviewer and dependency evidence are required; performance and cost/latency are typed by applicability; missing evidence blocks; primary-model self-scores, warning reduction, coverage, test count and patch/test LOC remain diagnostic only.

## Current Evaluation State

Исторические записи и результаты ниже относятся к указанным срезам. Они не меняют очередь Web M1 и не являются проверками текущего запуска. При расхождении используются текущие owning artifacts; перенос истории не закрывает оставшиеся gates.


| Workstream | Eval state | Claim ceiling |
| --- | --- | --- |
| Batch 35 / Batch 38 | `T10-LIVE-M41` owner-closed no-op as `owner_closed_no_op_git_release_pr`; `B38-S2` cache refresh current; historical cache blocker preserved. | No future git/cache action without fresh approval. |
| Batch 39 | S5 decision: release `no_go`, owner-feedback `conditional_go`, runtime/browser `approval_required`. | Owner-feedback only; no release/runtime/browser/promotion claim. |
| Batch 41 | S9 generated-artifact modernization and Neural_Flow comparison. | Generated-artifact acceptance evidence only; no release/target-apply/Cosmos.gl-WebGL runtime proof. |
| Batch 42 | Planned-only instruction/tool-use matrix. | No fixed-auto-engagement claim. |
| Batch 44 | S0-S7 local/staged/manual Self-Learning Loop evidence. | No active automation, hidden telemetry, real session import, provider/model call, target mutation or auto-apply proof. |
| Batch 45 | M26/M27/M35/T12/T15 remain advisory-only/no-go; T21 has zero valid pairs and T22-A02 reviewer gate did not run. A04-A06 locally implement/focused-verify T23-T29. | Deterministic local contracts do not prove model improvement or promotion. T30-T33 remain required local gates; T34 requires a new exact approval and may still end no-go. |
| Track 11 DOC-M25 | Generated root `site`, search and sitemap freshness packet exists. | No browser proof, broad scans, remediation, raw retention, publication/release/deploy/git claim. |
| GPT-5.6 model/config migration | Role-aware Sol/Terra pins remain; R1-R6 requires one native permission model, generic Terra/medium defaults, explicit write-skill authority, Docs MCP on source roles, resolvable paths, phase-neutral prompts and a 7000-character developer-prompt budget. Luna remains an unevaluated high-volume candidate. | Static contract evidence may support configuration consistency only. No quality, cost, latency, fresh-session MCP/hook, broad agent-behavior or promotion claim until bounded comparative/runtime evidence exists. |
| Lifecycle/control-plane sync | Config-routed Task Brief, lifecycle marker, control-plane sync and Completion Brief contract. | Hook output is reminder/evidence context only, not completion proof. |

## Active Eval Routes

| Change type | Required eval route |
| --- | --- |
| Docs, source registry, control-plane or docs tests | `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`, `python tools\check_docs.py`, `git diff --check` |
| MkDocs navigation, Mermaid, localization, search/sitemap or generated `site` evidence | Docs route plus strict MkDocs build |
| Plugin scripts, templates, lifecycle skills, runtime behavior or CLI contracts | Focused tests, full unittest, fixture eval, transcript eval, Codex compatibility, docs check and diff hygiene as routed by `TEST.md` |
| Batch 39 pilot/hardening matrix | `prod_test.md` attempt/failure/fix/retest ledger review plus focused tests, fixture/transcript eval, redaction/no-mutation proof and docs/diff hygiene |
| Self-Learning Loop | Focused state/extensions tests, staged initializer/runner/export checks where applicable, docs check and diff hygiene |
| Batch 45 Professional Code Authoring | Focused comment-sufficiency, coding-standards, behavioral, discovery/status/dashboard/template/fixture, self-learning, automation-policy, docs/source-link, manual-pilot ledger and diff hygiene |
| AI/RAG behavior, provider gates or model migration | Baseline eval, one focused change, rerun eval, inspect artifacts, record threshold/fallback and approval boundary |
| Frontend/browser/runtime UX | Build/test/lint where available, browser/runtime evidence, console/network checks, responsive/overflow evidence and screenshot/trace evidence or explicit gap |
| Release, external write, automation or git action | Explicit owner approval packet, current evidence, rollback/recovery path and no silent stage/commit/push/PR |

## Methodology Eval Map

| Area | Gate or evidence key | Primary evidence owner |
| --- | --- | --- |
| Track 8 scenario routing | `T8-S16`, `T8-A3..A16`, `T8-B`, `T8-C`, `T8-D`, `T8-F`, `T8-GX`, `T8-GY`, `T8-H` | Track 8 detailed backlog, Product-Agent OS docs and fixture/transcript evals |
| Track 9 methodologies | `business_product_contract_present`, `requirements_domain_contract_present`, `solution_architecture_contract_present`, `quality_testing_evals_contract_present`, `codex_agentic_workflow_contract_present`, `frontend_contract_present`, `backend_contract_present`, `api_integrations_contract_present`, `database_data_contract_present`, `llm_ai_rag_contract_present`, `security_privacy_compliance_contract_present`, `delivery_release_operations_contract_present`, `cross_domain_synthesis_contract_present` | Track 9 backlog, methodology docs, templates and eval fixtures |
| Track 10 guided questions/dashboard | `question_queue_contract_present`, `status_dashboard_present`, stale-evidence guard | Track 10 backlog and Product-Agent OS docs |
| Track 10 live layer | `T10-LIVE-M01..M41`, approval-bound live/runtime/provider/mutation/git gates | Track 10 backlog, registry and Batch 35 packet |
| Batch 39 | `B39-S1..S5`, `B39-TEST-M01..M54`, generated-view-only, source-policy and no-unapproved-actions gates | `prod_test.md`, B39 packets |
| Batch 44 | Self-Learning Loop state, due-check, manual pilot, Promptfoo export, HALO-style packet and candidate-only repair routing | B44 packets and `docs/product-agent-os/self-learning-loop.md` |
| Batch 45 | Professional Code Authoring checklist, advisory validator, historical behavior eval/no-go, S8 failed promotion route and S9 code-quality runtime recovery plan with deterministic evidence and blinded review gates | B45 packets, `B45-CQRR-A01` and `docs/product-agent-os/coding-standards.md` |
| Track 11 docs/site | G1.1 docs-toolchain, G2-G5 source docs, DOC-M25 site freshness | Track 11 plan, registry and documentation-refresh packets |

## Unsupported Claims

Use this triage shape when a claim lacks evidence:

```text
Claim:
Missing source:
Verification needed:
Current status: unsupported | inspection-only | explicit_gap_accepted | approval_required
Owner:
Follow-up:
```

Reject or downgrade these claim patterns unless current evidence exists:

- Tests pass, build works, feature works, release ready, deployment safe or security reviewed from inspection alone.
- AI/RAG quality, grounding, model improvement, prompt safety or tool safety without baseline and rerun eval evidence.
- Generated graph/dashboard/site output as source of truth.
- Approval-bound live/provider/runtime/canonical-mutation/git action implied by a planning packet or generated artifact.
- Methodology artifact presence as proof that a human owner accepted semantic correctness.
- Batch 45 promotion from T14/T15/T16-T22/T17/T18/T19/T20/T21/T22 or the planned T23-T34 route; current result has no valid pair set and the reviewer gate did not run. `B45-CQRR-T23..T33` must first close the local executable-contract, fault-detection, deterministic-evidence, blinding and corpus/prompt-freeze gates; T34 then still needs a new exact approval before any provider/model/reviewer call.

## Historical Eval Evidence Owners

- Track 8 scenario, readiness, false-positive and transcript/session evidence: `docs/sources/product-agent-os-track-8-detailed-backlog.md`.
- Track 9 methodology intelligence evidence across all domains, synthesis and runtime runner: `docs/sources/product-agent-os-track-9-backlog.md` and `docs/sources/registry.md`.
- Track 10 evidence, including project graph, live-layer gates, Batch 34 docs/i18n/product-docs closure and Batch 35 real-testing execution: `docs/sources/product-agent-os-track-10-backlog.md` and `docs/sources/registry.md`.
- Batch 35 approval-bound local runtime, browser automation, provider pilot, canonical mutation pilot and git preflight evidence: `docs/sources/product-agent-os-batch35-approval-packet-draft.md`.
- Batch 39 production-test evidence: `prod_test.md` and B39 packets.
- Batch 44/45 and Track 11 evidence: `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`, `docs/product-agent-os/control-plane-current-state.md` and `docs/superpowers/specs/*.json`. Batch 45 compact anchors: `B45-PCA-M37-A01`, `B45-RETEST-Q0-Q2-A01`, `B45-RETEST-Q3-FIXTURE-STATIC-A01`, `B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01`, `B45-POST-Q4-NEXT-TASKS-A01`, `B45-POSTQ4-T01-T04-A01`, `B45-POSTQ4-T05-A01`, `B45-POSTQ4-T05B-A01`, `B45-POSTQ4-T06-A01`, `B45-POSTQ4-T08-A01`, `B45-POSTQ4-T10-A01`, `B45-POSTQ4-T11-A01`, `B45-POSTQ4-T12-RUN-A01`, `B45-POSTQ4-T13-A01`, `B45-POSTQ4-T14-A01`, `B45-POSTQ4-T14-RUN-A01`, `B45-POSTQ4-T15-A01`, `B45-POSTQ4-T16-T22-A01`, `B45-POSTQ4-T17-A01`, `B45-POSTQ4-T18-A01`, `B45-POSTQ4-T19-A01`, `B45-POSTQ4-T20-A01`, `B45-POSTQ4-T20-A02`, `B45-POSTQ4-T20-A03`, `B45-POSTQ4-T21-PREFLIGHT-A01`, `B45-POSTQ4-T21-PREFLIGHT-A02`, `B45-POSTQ4-T21-PREFLIGHT-A03`, `B45-POSTQ4-T21-COST-WAIVED-RUN-A01`, `B45-POSTQ4-T22-A02`.

## Verification For This EVALS Maintenance

For this control-plane compaction, the required route is:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v
python -m unittest tests.product_agent_os.test_lifecycle_hooks -v
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
python tools\check_docs.py
git diff --check
```

Full unittest, fixture eval, transcript eval and strict MkDocs are required only if the focused checks expose contract drift or the slice changes plugin/runtime behavior or MkDocs-sensitive site surfaces.

<!-- product-agent-os:end evals -->

## Candidate model migration rubric — 2026-11-03

The [model migration playbook](docs/playbooks/model-migration.md) and [model matrix](docs/codex/models-and-reasoning.md) define candidate-only guidance. Freeze corpus/prompt/tools/skills/permissions and effective effort before a model comparison; separately tune effort and prompt. Predeclare quality thresholds, cost/time/token budgets, stop conditions and independent review. Track correctness, task completion, unsupported claims, tool failures, excess approvals/check loops, latency, cache read/write and cost per completed task, including failed attempts/subagents. Missing measurements are not zero. No model eval or promotion occurred in this documentation task; account availability and fresh-session activation remain unverified. Existing Batch 45 no-go and historical results are unchanged.
