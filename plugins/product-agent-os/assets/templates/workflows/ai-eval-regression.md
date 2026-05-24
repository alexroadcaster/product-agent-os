# AI Eval Regression

Project: {project_name}
Profile: {profile_name}

## Inputs

- User goal:
- AI/RAG behavior under review:
- App path:
- Current prompt/context:
- Retrieval path:
- Dataset policy:
- Baseline result:
- Judge rubric:
- Threshold:
- Latency and cost constraints:
- Failure examples:
- Rerun command:
- Approval boundary:

## Process

1. Keep the workflow read-only until baseline, dataset policy, threshold, rerun command, and approval boundary are explicit.
2. Record the current app path, prompt/context, retrieval path, model or tool boundary, and evaluation command.
3. Confirm dataset policy before use: synthetic or approved source, no-secrets, no credentials, no private customer data, and no raw private chat logs.
4. Establish baseline result before changing model, prompt, retrieval, tools, chunking, ranking, or context assembly.
5. Define judge rubric, assertions, retrieval metrics, grounding metric, latency threshold, cost threshold, and blocking threshold before rerun.
6. Change one-factor-at-a-time so the regression source is attributable.
7. Capture failure examples, expected behavior, observed behavior, and residual risk for each failed case.
8. Rerun command after each focused change and compare against baseline result and threshold.
9. Do not change model, prompt, retrieval, dataset, judge rubric, or threshold without recording the reason.
10. Do not claim quality, do not claim regression fixed, and do not release AI behavior without eval evidence from the current run.

## Outputs

- AI eval spec:
- App path:
- Prompt/context inventory:
- Retrieval metrics:
- Dataset policy:
- Baseline result:
- Judge rubric:
- Assertions:
- Judge policy:
- Threshold:
- Latency:
- Cost:
- Grounding:
- Failure examples:
- Rerun command:
- Regression handling:
- Eval evidence:
- One-factor-at-a-time change log:
- Approval requirements:
- Residual risk:

## Verification

- Dataset policy includes no-secrets handling and approved data source.
- Baseline result exists before behavior changes.
- Rubric, assertions, judge policy, threshold, latency, cost, grounding, and retrieval metrics are explicit.
- Rerun command is named and linked to the same dataset and baseline comparison.
- Failure examples are recorded without secrets or private customer data.
- Quality claims cite eval evidence from the current run.

## Stop Conditions

- Dataset source is unknown or may contain secrets, credentials, private customer data, or raw private chat logs.
- Baseline result is missing.
- Judge rubric, threshold, or rerun command is missing.
- Multiple factors changed before rerun.
- The request asks to change model, prompt, retrieval, or threshold before baseline evidence exists.
- The request asks to claim quality, release, or close the regression without eval evidence.
