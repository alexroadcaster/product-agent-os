# AI Eval Regression

Project: {project_name}
Profile: {profile_name}

## Inputs

- User goal:
- Methodology: `llm_ai_rag`
- Readiness gate: `llm_ai_rag_readiness_when_ai_behavior_changes`
- AI behavior promise:
- AI/RAG behavior under review:
- App path:
- App-backed path:
- Current prompt/context:
- Prompt/context inventory:
- Retrieval path:
- Dataset policy:
- Dataset governance:
- Baseline result:
- Baseline/current comparison:
- Judge rubric:
- Threshold:
- Thresholds:
- Latency and cost constraints:
- Current eval evidence:
- Failed cases:
- Failure examples:
- Rerun command:
- Approval boundary:
- Accepted-gap handling:
- Required artifacts: `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, `ai-cost-latency-budget.md`

## Process

1. Keep the workflow read-only until baseline, dataset policy, threshold, rerun command, and approval boundary are explicit.
2. Record the current app-backed path, prompt/context inventory, retrieval path, model or tool boundary, and evaluation command.
3. Confirm dataset policy before use: synthetic or approved source, no-secrets, no credentials, no private customer data, and no raw private chat logs.
4. Establish baseline result before changing model, prompt, retrieval, tools, chunking, ranking, or context assembly.
5. Define judge rubric, assertions, retrieval metrics, grounding metric, latency threshold, cost threshold, thresholds, and blocking threshold before rerun.
6. Change one-factor-at-a-time so the regression source is attributable.
7. Capture failed cases, failure examples, expected behavior, observed behavior, and residual risk for each failed case.
8. Rerun command after each focused change and compare against baseline result, baseline/current comparison and threshold.
9. Do not change model, prompt, retrieval, dataset, judge rubric, or threshold without recording the reason.
10. Do not claim quality, do not claim regression fixed, and do not release AI behavior without eval evidence from the current run.
11. Reject unsupported shortcuts: prompt inspection is enough, ai quality claim without current eval evidence, citations alone prove grounding, and model upgrade automatically improves quality.

## Outputs

- AI eval spec:
- App path:
- App-backed path:
- Prompt/context inventory:
- AI behavior promise:
- Baseline eval:
- Eval rerun:
- Dataset governance:
- Retrieval metrics:
- Dataset policy:
- Baseline result:
- Baseline/current comparison:
- Judge rubric:
- Assertions:
- Judge policy:
- Threshold:
- Thresholds:
- Latency:
- Cost:
- Grounding:
- Failed cases:
- Failure examples:
- Rerun command:
- Regression handling:
- Eval evidence:
- Current eval evidence:
- Current-run evidence:
- One-factor-at-a-time change log:
- Accepted-gap handling:
- Approval requirements:
- Safety evidence:
- Cost evidence:
- Residual risk:

## Verification

- Dataset policy includes no-secrets handling and approved data source.
- Baseline result exists before behavior changes.
- Rubric, assertions, judge policy, threshold, latency, cost, grounding, and retrieval metrics are explicit.
- Rerun command is named and linked to the same dataset and baseline comparison.
- Failed cases and failure examples are recorded without secrets or private customer data.
- Quality claims cite eval evidence from the current run.

## Stop Conditions

- Dataset source is unknown or may contain secrets, credentials, private customer data, or raw private chat logs.
- Baseline result is missing.
- Judge rubric, threshold, or rerun command is missing.
- Multiple factors changed before rerun.
- The request asks to change model, prompt, retrieval, or threshold before baseline evidence exists.
- The request asks to claim quality, release, or close the regression without eval evidence.
