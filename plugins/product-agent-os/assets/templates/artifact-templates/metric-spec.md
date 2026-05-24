# Metric Spec Template

Project: {project_name}

Methodology gate: `metric_hardening_when_product_behavior_changes`

## Product Hypothesis

- Hypothesis:
- User segment:
- Expected behavior change:
- Decision this metric will inform:

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

## Instrumentation

- Event taxonomy:
- Event source:
- Properties:
- Sampling:
- Dashboard or report:

## Data Protection

- Privacy classification: `public | internal | personal data | sensitive`
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
- Observed result:
- Input metric result:
- Counter-metric result:
- Guardrail result:
- Qualitative review result:
- Decision:
- Next experiment:
