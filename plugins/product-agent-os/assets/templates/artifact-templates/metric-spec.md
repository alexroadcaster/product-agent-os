# Metric Spec Template

Project: {project_name}

Methodology gate: `metric_hardening_when_product_behavior_changes`

## Product Hypothesis

- Product hypothesis gate (`product_hypothesis_present`):
- Hypothesis:
- User segment:
- Explicitly excluded users:
- Problem or opportunity:
- Opportunity is not only a solution request (`opportunity_not_solution_present`):
- Expected behavior change:
- Decision this metric will inform:
- Decision horizon (`decision_horizon_present`): `discovery | MVP | beta | production | scale`
- Business outcome:
- Product outcome:
- Feature traction metric:
- Outcome metric level separated (`outcome_metric_level_separated`):
- Metric scope (`metric_scope_classified`): `required | not_applicable | accepted_gap`
- Value proposition evidence (`value_proposition_evidence_present`):

## Primary Metric

- North Star or primary value metric:
- Metric name:
- Definition:
- Baseline:
- Target:
- Measurement window:
- Owner:
- Owner signoff:
- Proxy metric risk:

## Input Metrics, Counter-Metric, And Guardrails

| Type | Metric | Why it matters | Baseline | Target or blocking threshold | Owner |
| --- | --- | --- | --- | --- | --- |
| Input metric |  |  |  |  |  |
| Counter-metric |  |  |  |  |  |
| Guardrail |  |  |  |  |  |

- Input metric:
- Counter-metric:
- Guardrail:
- Qualitative review:
- Qualitative feedback loop (`qualitative_feedback_loop_present`):

## Optional HEART Metrics

Use HEART metrics only when they fit the product question; not every category is required.

- Happiness:
- Engagement:
- Adoption:
- Retention:
- Task success:

## Instrumentation

- Event taxonomy:
- Analytics tracking plan (`analytics_tracking_plan_present`):
- Event source:
- Properties:
- Sampling:
- Dashboard or report:

## Data Protection

- Privacy classification: `public | internal | personal data | sensitive`
- Privacy classification for metrics (`privacy_classification_for_metrics_present`):
- PII or sensitive fields:
- Data minimization:
- Retention period:
- Deletion or TTL:
- Consent or policy requirement:
- Data owner:
- Privacy owner:
- Owner signoff:
- Redaction:

## Goodhart Check

- Proxy metric risk:
- How this metric can be gamed:
- Counter-metric:
- Guardrail:
- Qualitative review:
- Owner signoff:
- Stop condition:
- Do not claim success from a proxy metric without counter-metric, guardrail, qualitative review, and post-release review evidence.

## Post-Release Review

- Review date:
- Post-release review evidence:
- Release measurement evidence (`release_measurement_evidence_present`):
- No-production-telemetry fallback:
- AI product eval gate (`ai_product_eval_when_ai_behavior_changes`):
- Workflow promotion value evidence (`workflow_promotion_value_evidence_present`):
- Observed result:
- Input metric result:
- Counter-metric result:
- Guardrail result:
- Qualitative review result:
- Decision:
- Next experiment:

## DORA Process Metrics

- DORA measurement source:
- Change lead time:
- Deployment frequency:
- Failed deployment recovery time:
- Change fail rate:
- Deployment rework rate:
- Anti-Goodhart warning:
- Individual performance quota prohibition:

DORA metrics are process-learning signals. Do not use DORA metrics as an individual performance quota or personal productivity score.
