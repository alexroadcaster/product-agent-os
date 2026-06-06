# Security, Privacy & Compliance Methodology Research

Source status: `official + legal/regulatory reference + vendor documentation + tool-assisted`

Research date: `2026-05-24`

Target methodology page: [../../methodologies/security-privacy-compliance.md](../../methodologies/security-privacy-compliance.md)

Target Product-Agent OS behavior: detect security-sensitive work early, keep the workflow planning-first and approval-bound, require threat surface and data classification before implementation, prevent secrets/private data from entering artifacts, and block readiness claims without security/privacy evidence, owner review, rollback and residual-risk record.

## Scope

This dossier covers secure SDLC, threat modeling, authentication, authorization, permissions, secrets, PII and sensitive data handling, privacy-by-design, audit logging, abuse controls, rate limits, secure API and web verification, AI/LLM security, supply chain security, SBOM/provenance, CI permissions, compliance overlays, vulnerability response and approval boundaries.

It does not provide legal advice, replace security engineering review, replace privacy counsel, mandate one compliance framework for all projects or imply that a checklist proves compliance. Compliance overlays must be selected by jurisdiction, product domain, customer contract and owner/legal review.

## Supported facts

- NIST SSDF SP 800-218 defines a secure software development framework with high-level practices that can be integrated into SDLC implementations and used as a common vocabulary across producers, purchasers and consumers.
- NIST Cybersecurity Framework 2.0 is current NIST cybersecurity risk management guidance and adds governance as an explicit function around cybersecurity risk strategy, expectations and policy.
- NIST Privacy Framework 1.1 usage guidance supports profiles, accountability, privacy program improvement, SDLC alignment and data processing ecosystem roles.
- OWASP SAMM is a software assurance maturity model for analyzing and improving an organization's software security posture.
- OWASP ASVS provides a basis for testing web application technical security controls with versioned verification requirements.
- OWASP Top 10 is an awareness document for critical web application security risks, with OWASP's page listing Top 10 2025 as the most current released version as of this research date.
- OWASP API Security Top 10 2023 is an API-specific risk catalog and should complement, not replace, API contract tests and authorization tests.
- OWASP Cheat Sheet Series provides developer-focused guidance across application security topics, including secrets management and logging.
- OWASP Top 10 for LLM Applications 2025 documents AI application security risks and is relevant when prompts, tools, RAG, agents or model outputs affect product behavior.
- OpenAI Codex agent approvals and security guidance defines sandboxing, approvals and network controls for Codex work.
- OpenAI API data controls guidance documents platform data controls; OpenAI safety and production best practices cover moderation, human oversight, adversarial testing, monitoring, rate limits, latency and operational safeguards.
- GitHub Actions secure use guidance and `GITHUB_TOKEN` guidance support least-privilege CI design; GitHub secret scanning detects secret leaks and supports push protection workflows where enabled.
- SLSA v1.1 defines supply chain levels and provenance concepts for build integrity.
- OpenSSF Scorecard checks repository security practices such as branch protection, dangerous workflows, pinned dependencies, token permissions, vulnerabilities and security policy.
- SPDX and CycloneDX are SBOM standards/specifications. SPDX 3.0 is listed as current by SPDX, and CycloneDX 1.7 is listed as current by CycloneDX as of this research date.
- GDPR and CCPA are legal/regulatory sources for privacy obligations; engineering docs should map product/data behaviors to legal review, not claim compliance without qualified owner evidence.

## Assumptions

- Product-Agent OS should use NIST SSDF as lifecycle vocabulary, OWASP ASVS/API/Top 10/LLM Top 10 as application risk vocabulary, NIST Privacy Framework as privacy program vocabulary, and SLSA/OpenSSF/SBOM sources as supply-chain vocabulary.
- For most projects, a lightweight security risk review is more useful than a broad compliance checklist. Regulated projects can add overlays later.
- Security scans and Codex Security workflows should be explicit opt-in. A security-sensitive workflow alone is not evidence that a full security scan was run.
- Documentation should store classifications and evidence, not raw secrets, raw PII, payment data, access tokens or private customer data.

## Unsupported claims not adopted

- "Using OWASP Top 10 means the app is secure." OWASP Top 10 is awareness/risk guidance, not a full verification standard.
- "ASVS mapping proves compliance." ASVS helps verification, but compliance depends on scope, evidence and review.
- "No secrets in code means no secrets risk." Secrets can leak through prompts, logs, traces, screenshots, fixtures, CI config and generated docs.
- "SBOM alone proves supply-chain security." SBOM improves transparency but needs vulnerability, provenance, signing and update workflows.
- "Agent approvals are optional UX." For privileged tools, external writes, customer data or payment/billing behavior, approvals are security controls.
- "Privacy compliance is universal." Privacy obligations vary by jurisdiction, user type, domain and data processing purpose.

## Methodologies

| Methodology | When to apply | Project-level behavior |
| --- | --- | --- |
| Secure SDLC / SSDF | Any production software or shared plugin | Security practices are integrated into requirements, design, implementation, tests, release and vulnerability response. |
| Security-sensitive planning-first workflow | Auth, authz, payments, billing, secrets, PII, audit logs, abuse controls or external writes | Read-only inventory, threat surface, owner review, approval boundary, rollback and verification plan before implementation. |
| Threat modeling | New trust boundary, external integration, multi-tenant data, privileged tools or agent workflows | Actors, assets, entry points, trust boundaries, abuse cases, mitigations and residual risk are explicit. |
| ASVS-driven verification | Web application controls are in scope | Versioned ASVS requirement IDs map to tests, review evidence and accepted gaps. |
| API security review | Public/private APIs, webhooks, integrations and generated clients | Auth scheme, object/function-level authorization, rate limits, unsafe consumption and negative tests are reviewed. |
| Privacy-by-design | PII, sensitive data, analytics, telemetry, user content or customer data exists | Data classification, minimization, purpose, retention, deletion/export rights, access and consent/notice review. |
| Secrets management | Credentials, tokens, keys, signing material, webhooks or CI secrets exist | No raw secrets in artifacts; storage, rotation, access, scanning and incident path are documented. |
| Least privilege and approval-bound operations | CI, MCP, tools, agents, external writes, production access | Scoped permissions, human approvals, staged drafts and audit-ready evidence. |
| Abuse-control design | Public endpoints, AI agents, payments, signup, search, uploads, messaging | Rate limits, fraud/misuse cases, monitoring, escalation and kill switch. |
| Audit logging and monitoring | Sensitive actions, admin actions, payments, data access, permission changes | Event taxonomy, retention, redaction, alerting and investigation path. |
| Supply chain security | Dependencies, package release, containers, plugins, CI actions | SBOM, dependency review, provenance, pinned actions, vulnerability workflow and release integrity. |
| AI/LLM security review | Prompts, tools, RAG, agents, model output controls | Prompt injection, data leakage, tool misuse, excessive agency, overreliance and red-team cases. |
| Compliance overlay mapping | Finance, healthcare, minors, enterprise, international privacy or contractual obligations | Legal/regulatory source, applicability, owner, evidence, gaps and review date are tracked. |
| Vulnerability response | Security bug, advisory, dependency alert, leaked secret or abuse incident | Triage, severity, containment, fix evidence, disclosure path and post-incident lessons. |

## Documentation artifacts and standards

| Artifact | Purpose | Candidate source/tool |
| --- | --- | --- |
| Security risk review | Threat surface, auth/authz, secrets, PII, abuse controls, audit logs, tests, rollback and approval. | `security-risk-review.md` |
| Threat model | Actors, assets, trust boundaries, entry points, abuse cases, mitigations and residual risk. | STRIDE-style review, Mermaid/C4 |
| Data classification register | Field/data class, sensitivity, purpose, retention, access, deletion/export and storage location. | `data-classification-register.md` |
| Privacy impact record | Processing purpose, data minimization, consent/notice, retention, sharing, cross-border and legal owner. | NIST Privacy Framework, legal overlay |
| Secrets inventory | Secret type, storage, owner, rotation, access scope, scan coverage and incident action. | OWASP Secrets Management, GitHub secret scanning |
| Authn/authz matrix | Roles, permissions, scopes, resource ownership, denied actions and tests. | ASVS/API security |
| API security review | Auth scheme, authorization checks, rate limits, input/output validation, errors and unsafe-consumption risks. | OpenAPI, OWASP API Top 10 |
| ASVS mapping | Versioned ASVS controls, applicability, test evidence and gaps. | OWASP ASVS |
| Abuse/rate-limit plan | Abuse cases, limits, monitoring, fallback, kill switch and escalation. | Product-specific |
| Audit logging policy | Security events, sensitive-data exclusions, retention, alerting and investigation owner. | OWASP Logging |
| Supply chain review | Dependencies, licenses, vulnerabilities, SBOM, provenance, CI action pinning and release signing. | SLSA, Scorecard, SPDX/CycloneDX |
| SBOM manifest | Format/version, generation command, validation command, release artifact and storage. | SPDX, CycloneDX |
| CI permissions review | Workflow triggers, `GITHUB_TOKEN` permissions, secrets, external actions, artifacts and approval gates. | GitHub Actions secure use |
| AI security review | Prompt injection, tool permissions, RAG data exposure, model output handling, eval/red-team cases. | OWASP LLM Top 10, OpenAI safety docs |
| Compliance applicability matrix | Regulation/contract, applicability, owner, evidence, non-goals and review cadence. | GDPR/CCPA/sector overlays |
| Vulnerability response record | Finding, severity, affected versions, containment, fix, verification, disclosure and postmortem. | SSDF, GitHub advisories |
| Approval record | External write, production data, billing/payment, customer data or policy change approval. | Product-Agent OS approval boundary |

## Project application instructions

1. Classify the slice before implementation. Mark as security-sensitive when it touches authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limits, audit logs, CI permissions, package release, external writes or agent tool permissions.
2. Keep security-sensitive work read-only until threat surface, data classification, approval boundary, rollback and verification plan are explicit.
3. Identify actors, assets, entry points, trust boundaries, privileged operations, data exposed, external systems and abuse cases.
4. Classify data before examples, fixtures, evals, logs, traces, screenshots or docs are created.
5. Do not store raw secrets, credentials, private keys, raw PII, payment data, raw private chats, access tokens or private customer data in docs, prompts, memory, fixtures, examples or templates.
6. For auth/authz changes, document allowed and forbidden behavior, role/scope matrix, object ownership checks and negative tests.
7. For API/security scheme changes, update OpenAPI or equivalent contract and include security scheme, scopes, error behavior and negative examples.
8. For web app technical controls, map checks to versioned ASVS requirements when ASVS applies.
9. For public APIs, webhooks or integrations, add OWASP API Security risks to threat review and require object/function-level authorization checks where relevant.
10. For AI/RAG/agent workflows, include OWASP LLM Top 10 risks and OpenAI safety/data-control boundaries where OpenAI services are used.
11. For Codex App, CLI, IDE extension, subagents, skills, MCP or automations, treat sandbox, approvals, external writes and network access as security controls.
12. For CI, GitHub Actions or release workflows, document least-privilege permissions, secret use, artifact exposure, external action pinning and approval boundary.
13. For dependencies and releases, document vulnerability status, update path, SBOM/provenance status and release integrity evidence where applicable.
14. For privacy-impacting work, document purpose, data minimization, retention, deletion/export expectations, access, sharing and legal/regulatory owner.
15. For compliance-sensitive work, create an applicability matrix. Do not claim GDPR, CCPA, HIPAA, PCI, SOC 2 or enterprise compliance from engineering inspection alone.
16. Require security tests or explicit test gaps for touched authn, authz, permission, secret handling, PII handling, abuse control, rate limit, audit logging and external write behavior.
17. Require owner review for security-sensitive changes and explicit approval for external systems, production data, payment/billing, secret rotation and policy changes.
18. Record rollback and mitigation: feature flag, kill switch, permission rollback, secret rollback, payment disable path, data access rollback or release revert.
19. Record residual risk in `RUNLOG.md`, risk review or release packet before completion.
20. Use Codex Security scan workflows only when explicitly requested and evidenced; do not imply that a scan ran from a methodology page alone.

## Product-Agent OS candidate rules

### Discovery signals

- Directories: `.github/workflows/`, `auth/`, `security/`, `permissions/`, `billing/`, `payments/`, `secrets/`, `policies/`, `compliance/`, `privacy/`, `audit/`, `rate-limit/`, `middleware/`, `infra/`
- Files: `.env*`, `SECURITY.md`, `CODEOWNERS`, `dependabot.yml`, `openapi.*`, `asyncapi.*`, `Dockerfile`, `cosign.*`, `sbom.*`, `cyclonedx.*`, `spdx.*`, `security-risk-review.md`, `privacy-impact-record.md`
- Terms: authn, authz, permission, role, scope, token, secret, key, PII, sensitive data, customer data, payment, billing, refund, audit, abuse, rate limit, compliance, GDPR, CCPA, HIPAA, PCI, SOC 2, ASVS, SSDF, SBOM, SLSA, provenance, prompt injection
- Dependency/tool signals: OpenAI SDK, Agents SDK, MCP servers, OAuth libraries, payment SDKs, auth providers, secret managers, dependency scanners, CodeQL, Dependabot, Scorecard, Snyk, Trivy, Grype, CycloneDX, SPDX, cosign

### Readiness gates

| Gate | Trigger | Block condition |
| --- | --- | --- |
| `security_sensitive_classification_present` | Any slice touching sensitive boundary | No classification of auth/authz/secrets/PII/payment/audit/CI/external-write impact. |
| `security_risk_review_present` | Security-sensitive change | Threat surface, owner review, tests, rollback or residual risk is missing. |
| `threat_surface_present` | New trust boundary, privileged operation, external integration or agent tool | Actors, entry points, assets, trust boundaries or abuse cases are missing. |
| `data_classification_present` | Any fixture/log/eval/doc/user data/customer data handling | Data class, purpose, retention, access and no-secrets status are missing. |
| `privacy_impact_record_present` | PII, telemetry, analytics, user content or customer data | Data minimization, retention, deletion/export, sharing and legal owner are missing. |
| `secrets_policy_present` | Secrets, tokens, keys, webhooks, CI credentials or signing material | Storage, rotation, access scope, scanning and no-artifact-secrets policy are missing. |
| `authz_negative_tests_present` | Auth/authz/role/scope/tenant/resource ownership change | Denied actions, object ownership and privilege escalation tests are missing. |
| `api_security_scheme_present` | API or integration auth change | Contract security scheme, scopes, error behavior or negative examples are missing. |
| `asvs_mapping_present` | Web app security controls in scope | ASVS version, applicable controls, evidence and gaps are missing. |
| `abuse_rate_limit_review_present` | Public endpoint, signup, payment, AI/tool action, upload or messaging | Abuse cases, rate limits, monitoring and fallback are missing. |
| `audit_logging_review_present` | Sensitive action, admin action, payment, data access or permission change | Event taxonomy, redaction, retention and alerting are missing. |
| `supply_chain_review_present` | Dependency, package, container, CI action or release artifact change | Vulnerability status, pinned action policy, SBOM/provenance or update path is missing. |
| `ci_permission_review_present` | CI/workflow/action/automation change | Token permissions, secrets, triggers, artifacts and approval boundary are missing. |
| `ai_security_review_present` | Prompt/RAG/tool/agent/model-output security-sensitive change | Prompt injection, data leakage, tool misuse, excessive agency and red-team/eval path are missing. |
| `compliance_overlay_present` | Regulated domain or contractual compliance claim | Applicable regulation/contract, owner, evidence and non-goals are missing. |
| `external_write_approval_present` | Production data, payment/billing, secret rotation, policy change or external security system mutation | Explicit approval and rollback are missing. |
| `security_evidence_before_completion` | Security readiness claim | Current tests/review/scan/owner evidence or explicit gap is missing. |

## Candidate eval fields

- Security-sensitive scope is classified before implementation.
- Threat surface includes actors, assets, entry points, trust boundaries, privileged operations, data exposed, external systems and abuse cases.
- Data classification includes no-secrets/no-private-data status for prompts, docs, fixtures, evals, logs and screenshots.
- Auth/authz changes include allowed behavior, forbidden behavior and negative tests.
- Privacy-impacting behavior includes purpose, minimization, retention, deletion/export expectations and owner review.
- API security changes include contract security schemes and negative examples.
- ASVS mapping includes version, controls, evidence and explicit gaps where applicable.
- Supply chain review includes dependency/vulnerability status, SBOM/provenance status and release integrity notes where applicable.
- CI workflow changes include least-privilege permissions and staged external-write policy.
- AI/agent security review covers prompt injection, data leakage, tool misuse, excessive agency and red-team/eval path.
- Compliance claims cite applicable legal/regulatory/contract source and qualified owner evidence.
- Rollback/mitigation path is explicit.
- Codex Security scan status is explicit: run with evidence, not requested, or blocked.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| Lifecycle framework | NIST SSDF, OWASP SAMM | SSDF for secure SDLC practices; SAMM for maturity improvement. |
| Web verification | OWASP ASVS, OWASP Top 10 | ASVS for controls/evidence; Top 10 for awareness/risk taxonomy. |
| API security | OWASP API Security Top 10, OpenAPI security schemes, OAuth BCP | Use with contract tests and negative authorization tests. |
| Privacy governance | NIST Privacy Framework, data classification register, privacy impact record | Legal obligations require qualified owner review. |
| Secrets | Secret manager, GitHub secret scanning, gitleaks/trufflehog candidates | Do not store raw secrets in docs or generated artifacts. |
| Supply chain | SLSA, OpenSSF Scorecard, Dependabot, CodeQL, Trivy/Grype candidates | Choose by stack and repo hosting. |
| SBOM | SPDX, CycloneDX, syft/cdxgen/cyclonedx-cli candidates | SBOM requires validation and release storage policy. |
| CI security | GitHub Actions secure use, scoped `GITHUB_TOKEN`, pinned actions | Workflow edits remain staged unless approved. |
| AI security | OWASP LLM Top 10, OpenAI safety/data controls, Promptfoo/red-team candidates | Pair with LLM/AI/RAG eval policy. |
| Agent runtime controls | Codex sandbox, approvals, MCP allow/deny, staged drafts | Treat approvals and sandbox as security controls. |
| Evidence | `security-risk-review.md`, `RUNLOG.md`, release packet, audit log policy | Current evidence required before readiness claims. |

## Типовые сбои

- Security review happens as a checklist after implementation.
- Threat model omits actors, trust boundaries or abuse cases.
- Authorization tests cover happy path only.
- API docs list auth scheme but omit scopes, error behavior or negative examples.
- Secrets are excluded from source but leak through prompts, logs, traces, screenshots, fixtures or generated docs.
- Privacy review records data fields but omits purpose, retention, deletion/export or sharing.
- Compliance claim is made without applicability matrix and qualified owner evidence.
- SBOM is generated once but not tied to release, vulnerability triage or provenance.
- CI workflow uses broad permissions or unpinned actions without review.
- AI/agent workflow ignores prompt injection, tool misuse, data leakage or excessive agency.
- Codex Security scan is implied but not explicitly requested or evidenced.
- External security systems, production policy, customer data, payment/billing or secret rotation are changed without approval.

## Open questions for deeper research

- Should Product-Agent OS generate a universal `security-risk-review.md` first, then optional ASVS/SAMM/NIST overlays later?
- Which security-sensitive triggers should block implementation until owner approval vs allow implementation with staged-only artifacts?
- Should SBOM/provenance be required only for release/package workflows or also for internal plugin builds?
- How should privacy-impacting local-first desktop data be represented differently from cloud/customer data?
- Which AI/agent security checks should be part of `llm-ai-rag` vs this security section?
- Should Codex Security plugin scans be routed automatically only when the user says "security scan", or suggested when readiness gates fail?
- How should compliance matrices separate legal obligations, customer contractual obligations and internal policy?

## Sources

- [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework/privacy-framework)
- [NIST Privacy Framework 1.1 usage guidance](https://www.nist.gov/privacy-framework/using-privacy-framework-11)
- [OWASP SAMM model](https://owaspsamm.org/model/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Top 10 Web Application Security Risks](https://owasp.org/www-project-top-ten/)
- [OWASP API Security Project](https://owasp.org/www-project-api-security/)
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [OpenAI Codex: Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [OpenAI API: data controls](https://developers.openai.com/api/docs/guides/your-data)
- [OpenAI API: safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [OpenAI API: production best practices](https://developers.openai.com/api/docs/guides/production-best-practices)
- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/about-secret-scanning)
- [SLSA specification v1.1](https://slsa.dev/spec/v1.1/about)
- [OpenSSF Scorecard](https://scorecard.dev/)
- [SPDX specifications](https://spdx.dev/use/specifications/)
- [CycloneDX specification overview](https://cyclonedx.org/specification/overview/)
- [California Consumer Privacy Act](https://oag.ca.gov/privacy/ccpa)
- [GDPR Regulation 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [Context7 research](../context7-research.md)
