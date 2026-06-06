# Agent/skill modernization loop

Source status: `official + experiment`

## Назначение

Эта страница описывает `agent_skill_metrics_loop` для Product-Agent OS: локальный read-only контур оценки agents, subagents, skills, prompt/policy packs, router/tool policies, memory policies, dataset/grader surfaces и harness versions после того, как реальная работа оставила проверяемые evidence records.

Цель контура - не autonomous auto-update. Цель - собрать source-backed evidence, показать scorecards, выявить modernization candidates и подготовить daily/weekly candidate packets для owner review. Это staged candidate-only pipeline без self-applied updates, active schedules и live eval/model/API calls.

## Source-of-truth boundary

source of truth для метрик:

- control-plane artifacts: `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- запуск records, trace packets и eval packets;
- accepted gaps с owner, датой review и residual risk;
- staged scorecard ledger records, если они ссылаются на явные run/eval/trace evidence.

Не являются source of truth:

- generated dashboard/report HTML;
- memory и raw chat logs;
- unsupported community claims;
- один noisy daily report;
- modernization candidate без rollback target, owner review и approval state.

Любой generated report является review view. Он не доказывает, что проект готов, skill качественный или update можно применять.

## Входы

Минимальный входной пакет:

- target registry: agents, skills, prompt/policy packs, router/tool policies, automation candidates, config и harness targets;
- trace intake: `agents_sdk`, `opentelemetry_genai`, `tool_report` или `accepted_gap` trace sources с model/tool/handoff/final_response spans;
- evidence dataset: implemented work items, real trace samples, prior failures, critical slices, edge/adversarial cases, holdout cases, synthetic regression cases и known flaky cases;
- grader/judge calibration: human labels, judge labels, thresholds для precision, recall, Cohen kappa и sample size;
- version context: baseline, текущий и candidate versions;
- cost/latency/safety/reliability records когда target может affect production, external systems или user-visible quality.

Raw prompts, raw tool outputs, secrets, private customer data и unredacted PII являются не valid inputs.

## Выходы и артефакты

Цикл stages review artifacts only:

- target registry packet из `collect_target_registry`;
- trace packet из `build_trace_packet`;
- evidence dataset и quality packet из `build_evidence_dataset` и `evaluate_dataset_quality`;
- judge calibration summary из `build_judge_calibration_summary`;
- metric aggregation и scorecards из `build_metric_aggregation` и `calculate_scorecards`;
- cadence recommendation packet с `L0`, `L1`, `L2` или `L3`;
- append-only scorecard ledger record via `agent-skill-scorecard-ledger.md`;
- offline reports, including `agent-skill-evaluation-report.html` rendered через `render_agent_skill_metrics_report.py`;
- daily candidate packet via `agent-skill-daily-eval-report.md`;
- weekly verification packet via `agent-skill-weekly-verification.md`;
- modernization proposal via `agent-skill-update-candidate.md`.

Modernization candidates may target skill text, agent instructions, prompt/policy packs, router/tool policies, memory policy, dataset, grader или harness configuration. Они не может apply patches через themselves.

## Workflow и cadence

1. Inventory targets с read-only local inspection.
2. Build trace и evidence packets из текущий control-plane, run/eval artifacts и accepted gaps.
3. Запустите redaction и dataset quality checks до scoring.
4. Calibrate grader/judge output against human labels. Если calibration является missing или below threshold, judge-derived metrics stay `reportable_gap_only`.
5. Calculate scorecards и guardrail blockers. Headline score improvement не может override safety, false-pass, flake, trace completeness, cost или owner-review blockers.
6. Recommend cadence:
   - `L0`: on-change или low-risk review;
   - `L1`: periodic review для medium risk или mild flake/trace gaps;
   - `L2`: elevated review для high risk, high usage или approval-bound/write tools;
   - `L3`: production/reliability risk, automation candidates или major trace/flake issues.
7. Emit daily packet для triage: no-op, investigate, block promotion, stage candidate для review или request human audit.
8. Emit weekly verification только когда rollback target, owner review, holdout check, false-pass audit, flake replay и cost regression check являются present или explicitly accepted как gaps.

Cadence является recommendation, не active schedule. Цикл должен не create Codex App automations, GitHub Actions, recurring jobs или external workflows.

## Проверка

Expected verification evidence:

- dataset quality status является `ready`, или blockers являются recorded как accepted gaps;
- duplicate rate, leakage status, missing splits и real trace coverage являются visible;
- judge calibration является `calibrated` до judge-derived metrics support candidate approval;
- scorecards включают guardrail blockers и denominator/numerator evidence;
- daily/weekly packets cite evidence windows и текущий versions;
- каждый update candidate имеет owner, affected targets, metric deltas, expected impact, risk, approval state и rollback target;
- report rendering остается dry-run или stage-only; писать в target workspace запрещен, пока нет later approved merge path.

Read-only smoke command для report plan:

```powershell
python plugins\product-agent-os\scripts\render_agent_skill_metrics_report.py <workspace> --dry-run
```

Stage-only report rendering должен использовать output directory вне target workspace:

```powershell
python plugins\product-agent-os\scripts\render_agent_skill_metrics_report.py <workspace> --stage C:\tmp\product-agent-os-metrics-stage
```

## Риски And Failure Modes

- Трактовка report как proof из quality creates false readiness.
- Low sample size, duplicate cases, holdout leakage или missing real traces может make scorecards misleading.
- Uncalibrated LLM-as-judge output может produce false passes или false regressions.
- Daily noisy запуск может вызвать unnecessary changes, если его ошибочно принять за weekly acceptance evidence.
- Modernization candidates может become unsafe если they lack rollback target, owner review или cost/safety regression checks.
- Running live eval/model/API calls would violate read-only modernization boundary пока later explicit approval packet changes scope.
- Auto-applying candidate updates would turn loop в autonomous auto-update, который является explicitly out из scope.

## Next Action

Используйте эта page когда agent/skill evidence требует к быть interpreted или packaged для owner review. Следующий safe artifact - staged scorecard ledger, daily report, weekly verification packet или update candidate. Applying any update остается separate owner-approved implementation slice.
