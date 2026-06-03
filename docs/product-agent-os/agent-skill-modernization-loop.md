# Agent/skill modernization loop

Source status: `official + experiment`

## Назначение

Эта страница описывает `agent_skill_metrics_loop` для Product-Agent OS: локальный read-only контур оценки agents, subagents, skills, prompt/policy packs, router/tool policies, memory policies, dataset/grader surfaces и harness versions после того, как реальная работа оставила проверяемые evidence records.

Цель контура - не autonomous auto-update. Цель - собрать source-backed evidence, показать scorecards, выявить modernization candidates и подготовить daily/weekly candidate packets для owner review. Это staged candidate-only pipeline без self-applied updates, active schedules и live eval/model/API calls.

## Source-of-truth boundary

Source of truth для метрик:

- control-plane artifacts: `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- run records, trace packets и eval packets;
- accepted gaps с owner, датой review и residual risk;
- staged scorecard ledger records, если они ссылаются на явные run/eval/trace evidence.

Не являются source of truth:

- generated dashboard/report HTML;
- memory и raw chat logs;
- unsupported community claims;
- один noisy daily report;
- modernization candidate без rollback target, owner review и approval state.

Любой generated report является review view. Он не доказывает, что проект готов, skill качественный или update можно применять.

## Inputs

Минимальный входной пакет:

- target registry: agents, skills, prompt/policy packs, router/tool policies, automation candidates, config и harness targets;
- trace intake: `agents_sdk`, `opentelemetry_genai`, `tool_report` или `accepted_gap` trace sources с model/tool/handoff/final_response spans;
- evidence dataset: implemented work items, real trace samples, prior failures, critical slices, edge/adversarial cases, holdout cases, synthetic regression cases и known flaky cases;
- grader/judge calibration: human labels, judge labels, thresholds for precision, recall, Cohen kappa and sample size;
- version context: baseline, current and candidate versions;
- cost/latency/safety/reliability records when the target can affect production, external systems or user-visible quality.

Raw prompts, raw tool outputs, secrets, private customer data and unredacted PII are not valid inputs.

## Outputs And Artifacts

The loop stages review artifacts only:

- target registry packet from `collect_target_registry`;
- trace packet from `build_trace_packet`;
- evidence dataset and quality packet from `build_evidence_dataset` and `evaluate_dataset_quality`;
- judge calibration summary from `build_judge_calibration_summary`;
- metric aggregation and scorecards from `build_metric_aggregation` and `calculate_scorecards`;
- cadence recommendation packet with `L0`, `L1`, `L2` or `L3`;
- append-only scorecard ledger record via `agent-skill-scorecard-ledger.md`;
- offline reports, including `agent-skill-evaluation-report.html` rendered by `render_agent_skill_metrics_report.py`;
- daily candidate packet via `agent-skill-daily-eval-report.md`;
- weekly verification packet via `agent-skill-weekly-verification.md`;
- modernization proposal via `agent-skill-update-candidate.md`.

Modernization candidates may target skill text, agent instructions, prompt/policy packs, router/tool policies, memory policy, dataset, grader or harness configuration. They cannot apply patches by themselves.

## Workflow And Cadence

1. Inventory targets with read-only local inspection.
2. Build trace and evidence packets from current control-plane, run/eval artifacts and accepted gaps.
3. Run redaction and dataset quality checks before scoring.
4. Calibrate grader/judge output against human labels. If calibration is missing or below threshold, judge-derived metrics stay `reportable_gap_only`.
5. Calculate scorecards and guardrail blockers. Headline score improvement cannot override safety, false-pass, flake, trace completeness, cost or owner-review blockers.
6. Recommend cadence:
   - `L0`: on-change or low-risk review;
   - `L1`: periodic review for medium risk or mild flake/trace gaps;
   - `L2`: elevated review for high risk, high usage or approval-bound/write tools;
   - `L3`: production/reliability risk, automation candidates or major trace/flake issues.
7. Emit daily packet for triage: no-op, investigate, block promotion, stage candidate for review or request human audit.
8. Emit weekly verification only when rollback target, owner review, holdout check, false-pass audit, flake replay and cost regression check are present or explicitly accepted as gaps.

Cadence is a recommendation, not an active schedule. The loop must not create Codex App automations, GitHub Actions, recurring jobs or external workflows.

## Verification

Expected verification evidence:

- dataset quality status is `ready`, or blockers are recorded as accepted gaps;
- duplicate rate, leakage status, missing splits and real trace coverage are visible;
- judge calibration is `calibrated` before judge-derived metrics support candidate approval;
- scorecards include guardrail blockers and denominator/numerator evidence;
- daily/weekly packets cite evidence windows and current versions;
- each update candidate has owner, affected targets, metric deltas, expected impact, risk, approval state and rollback target;
- report rendering is dry-run or stage-only, with no write into the target workspace unless a later approved merge path exists.

Read-only smoke command for the report plan:

```powershell
python plugins\product-agent-os\scripts\render_agent_skill_metrics_report.py <workspace> --dry-run
```

Stage-only report rendering must use an output directory outside the target workspace:

```powershell
python plugins\product-agent-os\scripts\render_agent_skill_metrics_report.py <workspace> --stage C:\tmp\product-agent-os-metrics-stage
```

## Risks And Failure Modes

- Treating a report as proof of quality creates false readiness.
- Low sample size, duplicate cases, holdout leakage or missing real traces can make scorecards misleading.
- Uncalibrated LLM-as-judge output can produce false passes or false regressions.
- A daily noisy run can trigger unnecessary changes if it is mistaken for weekly acceptance evidence.
- Modernization candidates can become unsafe if they lack rollback target, owner review or cost/safety regression checks.
- Running live eval/model/API calls would violate the read-only modernization boundary unless a later explicit approval packet changes scope.
- Auto-applying candidate updates would turn the loop into autonomous auto-update, which is explicitly out of scope.

## Next Action

Use this page when agent/skill evidence needs to be interpreted or packaged for owner review. The next safe artifact is a staged scorecard ledger, daily report, weekly verification packet or update candidate. Applying any update remains a separate owner-approved implementation slice.
