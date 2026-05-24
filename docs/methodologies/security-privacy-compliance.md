# Security, Privacy & Compliance

Source status: `official + legal/regulatory reference + vendor documentation + tool-assisted + experiment`

Источники: [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final), [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework), [NIST Privacy Framework](https://www.nist.gov/privacy-framework/privacy-framework), [NIST Privacy Framework 1.1 usage guidance](https://www.nist.gov/privacy-framework/using-privacy-framework-11), [OWASP SAMM](https://owaspsamm.org/model/), [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/), [OWASP Top 10](https://owasp.org/www-project-top-ten/), [OWASP API Security](https://owasp.org/www-project-api-security/), [OWASP LLM Top 10 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/), [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html), [OWASP Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html), [Codex agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [OpenAI data controls](https://developers.openai.com/api/docs/guides/your-data), [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices), [OpenAI production best practices](https://developers.openai.com/api/docs/guides/production-best-practices), [SLSA](https://slsa.dev/spec/v1.1/about), [OpenSSF Scorecard](https://scorecard.dev/), [SPDX](https://spdx.dev/use/specifications/), [CycloneDX](https://cyclonedx.org/specification/overview/), [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use), [GitHub secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/about-secret-scanning), [CCPA](https://oag.ca.gov/privacy/ccpa), [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj), [Context7 research](../sources/context7-research.md), [research dossier](../sources/methodology-research/security-privacy-compliance.md).

## Deep research цель

Security, Privacy & Compliance слой определяет gates для authn, authz, permissions, secrets, PII, sensitive data, payments, billing, abuse controls, audit logging, supply chain, CI security, AI/agent security and regulated delivery.

Главный принцип: security-sensitive work сначала планируется и классифицируется, потом реализуется. Нельзя менять auth, permissions, production data, payments, secrets, policy, external systems или agent tool permissions без threat surface, approval boundary, rollback and current evidence.

## Поддержанные факты

- NIST SSDF and NIST Cybersecurity Framework provide security lifecycle and risk-management vocabulary for secure development.
- NIST Privacy Framework and usage guidance support privacy profiles, SDLC alignment, accountability and data-processing ecosystem roles.
- OWASP SAMM, ASVS, Top 10, API Security and LLM Top 10 provide security practice, verification and risk catalogs for web/API/AI systems.
- OWASP Secrets Management and Logging cheat sheets support no-secrets and redaction policies for prompts, logs, traces, screenshots and artifacts.
- Codex agent approvals and security treats sandbox, approvals and external-write boundaries as security controls for Codex App, CLI, IDE extension, subagents, skills, MCP and automations.
- OpenAI data controls, safety and production best practices support AI product data handling, monitoring, abuse and operational readiness concerns.
- SLSA, OpenSSF Scorecard, SPDX, CycloneDX and GitHub Actions security docs support supply-chain, SBOM, provenance and CI-permission review.
- GDPR and CCPA are legal references; project docs must not claim compliance without applicability, qualified owner and evidence.

## Assumptions

- Security-sensitive work starts read-only until threat surface, data classification, approval boundary, rollback and verification plan are explicit.
- Security readiness is not proven by code inspection; it requires tests, review, scan, owner evidence or explicit gap.
- Compliance claims require applicability matrix and qualified owner review.
- Secrets/private data can leak through prompts, screenshots, traces, logs, fixtures and docs even when code is clean.
- Codex Security scan should be explicit: run with evidence, not requested or blocked.

## Инструкции применения на проекте

1. Классифицировать slice до реализации. Security-sensitive triggers: authn, authz, permissions, payment, billing, secrets, PII, sensitive data, audit logs, rate limits, abuse controls, CI permissions, package release, external writes, agent tool permissions.
2. Для security-sensitive work держать workflow read-only, пока threat surface, data classification, approval boundary, rollback and verification plan не стали explicit.
3. Зафиксировать actors, assets, entry points, trust boundaries, privileged operations, data exposed, external systems and abuse cases.
4. Classify data before examples, fixtures, evals, logs, traces, screenshots or docs.
5. Не хранить raw secrets, credentials, private keys, raw PII, payment data, raw private chats, access tokens или private customer data в docs, prompts, memory, fixtures, examples, logs or templates.
6. Для auth/authz changes описать allowed behavior, forbidden behavior, role/scope matrix, object ownership checks and negative tests.
7. Для API/security scheme changes обновить OpenAPI/equivalent contract: scheme, scopes, error behavior, negative examples.
8. Для web app technical controls использовать versioned ASVS mapping, если ASVS применим.
9. Для public APIs, webhooks and integrations использовать OWASP API Security risks в threat review.
10. Для AI/RAG/agent workflows проверять prompt injection, data leakage, tool misuse, excessive agency and overreliance.
11. Для Codex App, CLI, IDE extension, subagents, skills, MCP and automations считать sandbox, approvals and external-write boundaries security controls.
12. Для CI/release workflows фиксировать least-privilege permissions, secret use, artifacts, cache, external action pinning and approval boundary.
13. Для dependencies/releases фиксировать vulnerability status, update path, SBOM/provenance status and release integrity evidence where applicable.
14. Для privacy-impacting work фиксировать purpose, data minimization, retention, deletion/export expectations, access, sharing and legal/regulatory owner.
15. Для compliance-sensitive work создать applicability matrix. Не заявлять GDPR, CCPA, HIPAA, PCI, SOC 2 или enterprise compliance из code inspection alone.
16. Требовать tests or explicit gaps для touched authn, authz, permission, secret handling, PII handling, abuse control, rate limit, audit logging and external writes.
17. Требовать owner review для security-sensitive changes и explicit approval для production data, payment/billing, secret rotation, policy changes and external security systems.
18. Фиксировать rollback/mitigation: feature flag, kill switch, permission rollback, secret rollback, payment disable path, data access rollback or release revert.
19. Security readiness claim требует current tests, review evidence, scan evidence, owner evidence или explicit gap.
20. Codex Security scan использовать только когда пользователь явно попросил scan/security review; не подразумевать scan из одного факта security workflow.

## Применяемые методологии разработки

| Методология | Когда применять | Как выглядит в проекте |
| --- | --- | --- |
| Secure SDLC / SSDF | Production/shared software | Security practices integrated into requirements, design, implementation, tests, release and vulnerability response. |
| Security-sensitive planning-first workflow | Auth, data, payment, secrets, audit, CI, agents | Read-only inventory, threat surface, approval boundary, rollback and verification plan before implementation. |
| Threat modeling | New trust boundary, external integration, privileged operation | Actors, assets, entry points, trust boundaries, abuse cases, mitigations, residual risk. |
| ASVS-driven verification | Web application security controls | Versioned ASVS controls mapped to tests, owner evidence and explicit gaps. |
| API security review | APIs, webhooks, integrations, generated clients | Auth scheme, object/function authorization, rate limits, unsafe consumption, negative tests. |
| Privacy-by-design | PII, sensitive data, analytics, telemetry, user content | Classification, minimization, purpose, retention, deletion/export, access, sharing. |
| Secrets management | Tokens, keys, credentials, signing material | Storage, rotation, access scope, scanning, incident path, no raw secrets in artifacts. |
| Least privilege and approval-bound operations | CI, MCP, tools, agents, external writes | Scoped permissions, human approvals, staged drafts and audit-ready evidence. |
| Abuse-control design | Public endpoints, signup, payments, AI tools, uploads | Abuse cases, rate limits, monitoring, escalation and kill switch. |
| Audit logging and monitoring | Sensitive/admin/payment/data-access actions | Event taxonomy, redaction, retention, alerting and investigation path. |
| Supply chain security | Dependencies, packages, containers, CI actions | SBOM, dependency review, provenance, pinned actions, vulnerability workflow, release integrity. |
| AI/LLM security review | Prompts, tools, RAG, agents, model outputs | Prompt injection, data leakage, tool misuse, excessive agency, red-team/eval cases. |
| Compliance overlay mapping | Regulated domain or contract obligation | Applicable source, owner, evidence, non-goals, review cadence. |
| Vulnerability response | Security bug, advisory, leaked secret, abuse incident | Triage, severity, containment, fix evidence, disclosure path, post-incident lessons. |

## Инструменты, артефакты и стандарты документирования

- `security-risk-review.md`: threat surface, auth/authz, secrets, PII, abuse controls, audit logs, tests, rollback, approval.
- `threat-model.md`: actors, assets, trust boundaries, entry points, abuse cases, mitigations, residual risk.
- `data-classification-register.md`: field/data class, sensitivity, purpose, retention, access, deletion/export, storage.
- `privacy-impact-record.md`: purpose, minimization, notice/consent, retention, sharing, cross-border, legal owner.
- `secrets-inventory.md`: secret type, storage, owner, rotation, access scope, scan coverage, incident action.
- `authz-matrix.md`: roles, permissions, scopes, resource ownership, denied actions, tests.
- `api-security-review.md`: auth scheme, authorization checks, rate limits, validation, errors, unsafe consumption.
- `asvs-mapping.md`: ASVS version, applicable controls, test evidence, accepted gaps.
- `abuse-rate-limit-plan.md`: abuse cases, limits, monitoring, fallback, kill switch, escalation.
- `audit-log-policy.md`: security events, sensitive-data exclusions, retention, alerting, investigation owner.
- `supply-chain-review.md`: dependencies, licenses, vulnerabilities, SBOM, provenance, CI action pinning, release signing.
- `sbom-manifest.md`: format/version, generation command, validation command, release artifact, storage policy.
- `ci-permissions-review.md`: workflow triggers, token permissions, secrets, external actions, artifacts, approvals.
- `ai-security-review.md`: prompt injection, tool permissions, RAG data exposure, model output handling, red-team cases, links to `llm-ai-rag` behavior/eval evidence.
- `compliance-applicability-matrix.md`: regulation/contract, applicability, owner, evidence, non-goals, review cadence.
- `vulnerability-response-record.md`: finding, severity, affected versions, containment, fix, verification, disclosure.
- `approval-record.md`: production data, external write, payment/billing, secret rotation or policy change approval.

## Что еще включить в deep research

- Maturity levels: `baseline`, `team`, `production`, `regulated`.
- Domain overlays: finance, healthcare, minors, enterprise, public sector, marketplace, AI agent tooling.
- ASVS level selection policy: when Level 1 is enough and when Level 2/3 should be considered.
- API security negative test templates: BOLA, BFLA, object property authorization, rate limits, unsafe consumption.
- Secret scanning and redaction policy across prompts, logs, screenshots, traces, eval datasets and docs.
- SBOM/provenance decision policy: internal app vs package/plugin/release artifact.
- Agent security model: MCP allow/deny, tool permissions, shell approvals, external writes, data exposure.
- Privacy lifecycle: data discovery, classification, minimization, retention, deletion/export, incident response.
- Compliance evidence model: source, applicability, owner, review date, current evidence, gaps, non-goals.
- Vulnerability response workflow: triage, containment, disclosure, patch release, postmortem.

## Product-Agent OS routing

- `workspace-discovery-auditor` detects auth, permissions, secrets, CI, payments, PII, sensitive data, security docs, SBOM/provenance, ASVS/SSDF/OWASP signals and agent tool permissions.
- `requirements-author` records privacy constraints, security-sensitive scope, compliance overlays, approval boundaries and forbidden behavior.
- `implementation-planner` blocks plan-ready status when security-sensitive classification, threat surface, data classification, rollback, owner review or approval boundary is missing.
- `test-eval-designer` defines authz negative tests, abuse/rate-limit tests, audit logging checks, privacy fixture policy and AI/agent red-team cases.
- `risk-reviewer` owns security/privacy quality verdict, missing evidence, unsupported compliance claims and residual risk.
- `release-operator` carries security notes, license notes, SBOM/provenance notes, owner approvals and rollback into release readiness.
- Codex Security plugin workflows are used only when explicitly requested; otherwise scan status is `not requested`.

## Candidate readiness gates

- `security_sensitive_classification_present`: sensitive boundary impact is classified before implementation.
- `security_risk_review_present`: threat surface, owner review, tests, rollback and residual risk are present.
- `threat_surface_present`: actors, entry points, assets, trust boundaries and abuse cases are explicit.
- `data_classification_present`: data class, purpose, retention, access and no-secrets status are present.
- `privacy_impact_record_present`: PII/telemetry/user-content/customer-data changes include minimization, retention, deletion/export, sharing and legal owner.
- `secrets_policy_present`: secrets/tokens/keys/webhooks/signing material have storage, rotation, access scope, scanning and no-artifact-secrets policy.
- `authz_negative_tests_present`: auth/authz/role/scope/resource ownership changes include denied actions and privilege escalation tests.
- `api_security_scheme_present`: API/integration auth change has contract security scheme, scopes, error behavior and negative examples.
- `asvs_mapping_present`: web security controls have ASVS version, applicable controls, evidence and gaps.
- `abuse_rate_limit_review_present`: public endpoint/payment/AI/tool/upload/messaging path has abuse cases, limits, monitoring and fallback.
- `audit_logging_review_present`: sensitive/admin/payment/data-access action has event taxonomy, redaction, retention and alerting.
- `supply_chain_review_present`: dependency/package/container/CI action/release change has vulnerability status, SBOM/provenance or update path.
- `ci_permission_review_present`: CI/workflow/action change has token permissions, secrets, triggers, artifacts and approval boundary.
- `ai_security_review_present`: prompt/RAG/tool/agent/model-output security change covers prompt injection, data leakage, tool misuse and excessive agency.
- `compliance_overlay_present`: regulated/contractual claim has applicable source, owner, evidence and non-goals.
- `external_write_approval_present`: production data, payment/billing, secret rotation, policy change or external security-system mutation has approval and rollback.
- `security_evidence_before_completion`: security readiness claim has current tests/review/scan/owner evidence or explicit gap.

## Candidate eval fields

- Security-sensitive classification exists before implementation.
- Threat surface includes actors, assets, entry points, trust boundaries, privileged operations and abuse cases.
- Data classification covers purpose, retention, access, sharing and no-secrets status.
- Privacy-impacting work includes minimization, retention, deletion/export and legal owner.
- Auth/authz changes include allowed behavior, forbidden behavior, object ownership and negative tests.
- API security change has contract security scheme, scopes, error behavior and negative examples.
- ASVS mapping includes version, applicable controls, evidence and gaps where applicable.
- Abuse/rate-limit review covers public endpoints, payments, uploads, messaging and AI/tool actions.
- Audit logging review includes event taxonomy, redaction, retention and alerting.
- Supply-chain review includes vulnerability status, pinned actions, SBOM/provenance or update path.
- AI security review covers prompt injection, data leakage, tool misuse and excessive agency.
- Security readiness claim cites current tests/review/scan/owner evidence or explicit gap.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| Secure development | NIST SSDF, OWASP SAMM | Lifecycle practices and maturity model. |
| Web/API verification | OWASP ASVS, OWASP API Security | Controls, negative tests, auth/authz and API risk mapping. |
| AI security | OWASP LLM Top 10, OpenAI safety/production guidance | Prompt injection, data leakage, tool misuse and overreliance cases. |
| Privacy governance | NIST Privacy Framework, GDPR, CCPA | Applicability, owner and evidence, not generic compliance claim. |
| Secrets/logging | OWASP Secrets Management, OWASP Logging | Storage, rotation, redaction, retention and no-artifact-secrets policy. |
| Supply chain | SLSA, OpenSSF Scorecard, SPDX, CycloneDX | Provenance, SBOM, dependency review and release integrity. |
| CI security | GitHub Actions secure use, `dependabot.yml` | Permissions, pinned actions, secret boundaries, update automation. |
| Codex security boundary | Codex sandbox and approvals | External writes, MCP, hooks, automations and privileged actions. |

## Проверки

- Security-sensitive scope is classified before implementation.
- Threat surface includes actors, assets, entry points, trust boundaries, privileged operations, data exposed and abuse cases.
- Docs, prompts, fixtures, evals, logs and screenshots contain no raw secrets or private data.
- Auth/authz changes include allowed behavior, forbidden behavior and negative tests.
- Privacy-impacting work includes purpose, minimization, retention, deletion/export and owner review.
- API security changes include contract security scheme and negative examples.
- Supply chain review includes vulnerability status, SBOM/provenance status and release integrity notes where applicable.
- CI changes include least-privilege permissions and staged external-write policy.
- AI/agent security review covers prompt injection, data leakage, tool misuse and excessive agency.
- Compliance claims cite applicable legal/regulatory/contract source and qualified owner evidence.
- Rollback/mitigation path is explicit.
- Codex Security scan status is explicit: run with evidence, not requested, or blocked.

## Failure modes

- Security review is only a checklist after coding.
- Threat model omits actors, trust boundaries or abuse cases.
- Authorization tests cover happy path only.
- API docs list auth scheme but omit scopes, error behavior or negative examples.
- Secrets are absent from code but leak through prompts, logs, traces, screenshots, fixtures or generated docs.
- Privacy review records data fields but omits purpose, retention, deletion/export or sharing.
- Compliance claim is made without applicability matrix and qualified owner evidence.
- SBOM is generated once but not tied to release, vulnerability triage or provenance.
- CI workflow uses broad permissions or unpinned actions without review.
- AI/agent workflow ignores prompt injection, tool misuse, data leakage or excessive agency.
- Codex Security scan is implied but not explicitly requested or evidenced.
- External security systems, production policy, customer data, payment/billing or secret rotation are changed without approval.

## Unsupported claims not adopted

- "Security review can happen after coding." Security-sensitive work needs planning, classification and approval boundary before implementation.
- "No secrets in code means no secret leakage." Prompts, logs, traces, screenshots, fixtures and docs can leak secrets too.
- "ASVS/OWASP mapping proves compliance." It supports verification, but compliance needs applicability, owner and evidence.
- "SBOM generated once means supply chain is handled." SBOM must connect to release, vulnerability triage and provenance.
- "Codex Security scan happened because the topic is security." Scan status must be explicit.

## Open questions for future implementation

- Which maturity labels should security methodology use: `baseline`, `team`, `production`, `regulated`?
- Which domain overlays should ship first: finance, healthcare, minors, enterprise, public sector, marketplace or AI agent tooling?
- How should ASVS level selection be encoded for small versus regulated projects?
- Which API security negative test templates should Product-Agent OS generate by default?
- When should SBOM/provenance be required for internal apps, packages, plugins or release artifacts?
- How should vulnerability response records connect to release and postmortem workflows?
