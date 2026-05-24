# Product-Agent OS Complexity Routing

Use this reference when adapting lifecycle depth to the project profile.

Profiles:

- `guided-small`: keep packets concise; propose minimal control-plane files; avoid custom agent generation.
- `standard-product`: require requirements, implementation plan, tests, release notes, and runlog evidence.
- `production-team`: require ownership boundaries, handoff fields, reviewer gates, and write-scope separation.
- `ai-product`: require prompt/context policy, deterministic checks, subjective eval criteria, and source fidelity.
- `enterprise-governed`: require approval gates, forbidden paths, audit evidence, and stricter source policy.
- `autonomous-maintenance`: require manual stability evidence before an automation candidate.

Rules:

- Complexity changes depth and risk gates. It does not change lifecycle order.
- Use the smallest profile that covers project risk, team size, external impact, and verification needs.
- Escalate depth when work touches production, external systems, sensitive data, security, billing, or irreversible operations.
- Downgrade depth only when scope, risk, and verification evidence support a lighter Product-Agent OS route.
