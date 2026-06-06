# Delivery, Release & Operations Methodology Research

Source status: `official + verified methodology + vendor documentation + tool-assisted`

Research date: `2026-05-24`

Target methodology page: [../../methodologies/delivery-release-operations.md](../../methodologies/delivery-release-operations.md)

Target Product-Agent OS behavior: detect release, deployment and operations work early; keep external release actions approval-bound; require current evidence before readiness claims; connect release scope, version impact, artifacts, rollout, rollback, observability, incident response and post-release learning into one auditable release packet.

## Scope

This dossier covers release engineering, continuous delivery, CI/CD workflow governance, deployment environments, release notes, changelog and versioning, progressive delivery, feature flags, rollout and rollback, observability, SLOs, runbooks, incident response, postmortems, GitOps-style desired-state operations, automation promotion and post-release measurement.

It does not prescribe one deployment platform, force Kubernetes or GitOps onto all projects, replace security/compliance review, or permit publishing, tagging, deploying, uploading artifacts, opening PRs, changing external systems or enabling automations without explicit approval.

## Supported facts

- DORA currently describes five software delivery performance metrics: change lead time, deployment frequency, failed deployment recovery time, change fail rate and deployment rework rate.
- DORA metrics should be treated as team/system improvement signals. They are not individual performance targets and can be gamed if used as quotas.
- Google SRE guidance uses SLIs, SLOs and SLAs to describe user-relevant service behavior and how teams react when targets are missed.
- Google SRE release engineering guidance treats reliable release processes as a prerequisite for reliable services and emphasizes reproducible, automated, intentional release processes.
- Google SRE postmortem guidance treats postmortems as written records of incident impact, mitigation, root causes and follow-up actions; blameless review and explicit criteria matter.
- OpenTelemetry defines a vendor-neutral observability framework for traces, metrics and logs; its semantic conventions are useful vocabulary for runtime evidence and runbooks.
- Twelve-Factor App includes build-release-run separation, config in environment, disposability, dev/prod parity, logs as event streams and one-off admin processes.
- GitHub Actions workflows are repository-defined automated processes. GitHub deployment environments can require reviewers, wait timers, branch/tag restrictions, custom protection rules and environment-scoped secrets.
- GitHub Releases bundle and deliver project iterations to users with tags, release notes and optional binary assets; draft releases can stage assets before publishing.
- Keep a Changelog provides human-oriented changelog categories and an `Unreleased` section; SemVer provides public API compatibility versioning vocabulary.
- Conventional Commits defines a machine-readable commit message convention that can support changelog generation and SemVer bump decisions, but it is optional and team-dependent.
- CNCF GitOps describes desired state stored in a source of truth and continuously reconciled with actual state, supporting traceability, rollback and reduced configuration drift.
- Argo Rollouts provides Kubernetes progressive delivery primitives such as blue-green, canary, weighted traffic shifting, analysis, manual judgement and automated rollback.
- OpenFeature provides a vendor-agnostic feature flag API with evaluation context, providers, hooks and events; this supports rollout documentation independent of a specific flag vendor.
- OpenAI Codex verified operations guidance describes repeatable operations with structured inputs, explicit approvals, bounded retries, logs, artifacts and audit-ready output.

## Assumptions

- Product-Agent OS should treat release readiness as an evidence packet, not as a status inferred from code inspection.
- Release and deployment actions should remain staged until the owner approves publish, tag, deployment, artifact upload, marketplace submission, store submission, package registry mutation, external workflow mutation or production operation.
- Teams can start with lightweight release packets and only add SLO, GitOps, progressive delivery or incident management depth when the product has runtime risk.
- DORA and SLO metrics are most useful as trend and learning inputs, not as hard gates for every small documentation-only change.
- Progressive delivery can be implemented through feature flags, environment targeting, traffic splitting or release train practices; Argo Rollouts is a concrete Kubernetes example, not a universal requirement.

## Unsupported claims not adopted

- "CI is green, therefore the release is ready." Release readiness also needs scope, owner, version impact, docs, artifacts, security/license notes, rollout, rollback and residual risk.
- "A rollback plan exists if we can revert the commit." Revert is only one rollback mechanism and may not recover data, external systems, package registries, mobile/desktop distribution, user state or migrations.
- "DORA metrics prove team quality." DORA metrics describe delivery system performance and can be distorted if used as individual targets.
- "Feature flags remove release risk." Flags add runtime control but need ownership, cleanup, default behavior, observability and failure handling.
- "GitOps automatically makes operations safe." Desired-state reconciliation still requires approvals, secrets policy, drift handling, rollback and incident response.
- "A changelog generated from commits is sufficient for users." User-facing release notes must explain impact, compatibility and action required.
- "Postmortem equals blame." The SRE source treats blameless postmortems as system learning records.

## Methodologies

| Methodology | When to apply | Project-level behavior |
| --- | --- | --- |
| Release engineering | Packages, apps, services, plugins, SDKs, installers or docs releases | Release scope, reproducible build, artifacts, version impact, owner, approvals and release process are explicit. |
| Continuous delivery discipline | Frequent changes, shared branches or deployment pipeline | Small batches, automated checks, release candidates, environment promotion and rollback/recovery path. |
| DORA measurement | Team wants delivery performance trend | Track change lead time, deployment frequency, failed deployment recovery time, change fail rate and deployment rework rate with anti-Goodhart notes. |
| SRE / SLO-driven operations | Runtime service has users, latency, availability or support expectations | SLIs/SLOs, error-budget thinking, alerts, runbooks and incident response connect release to reliability. |
| Observability-driven release | Runtime behavior must be diagnosable | Traces, metrics, logs, dashboards, alert owners and redaction policy are release evidence. |
| Progressive delivery | Blast radius must be controlled | Feature flags, staged rollout, canary, blue-green, traffic shifting, manual judgement and automated rollback where applicable. |
| GitOps / desired-state operations | Declarative infra/app state is managed via source control | Desired state, reconciliation mechanism, drift handling, approval and rollback are documented. |
| CI/CD governance | Workflow changes can publish, deploy, access secrets or mutate environments | Triggers, permissions, environments, reviewers, branch/tag rules, artifacts and external action policy are explicit. |
| Versioning and changelog discipline | Public API, package, SDK, plugin, app or docs release | SemVer impact, compatibility/deprecation notes, changelog categories and user-facing release notes. |
| Incident response and postmortem learning | Production incident, failed deployment or user-impacting regression | Incident record, timeline, mitigation, root causes, action items, owner and follow-up review. |
| Automation promotion | Repeated operations might become automation | Manual success evidence, stable inputs/outputs, owner, verification, approval and rollback/disable path before automation. |

## Documentation artifacts and standards

| Artifact | Purpose | Candidate source/tool |
| --- | --- | --- |
| Release readiness | Scope, owner, version, SemVer impact, evidence, artifacts, approval, rollback and residual risk. | `release-readiness.md` |
| Release packet | PR/release summary, user impact, checks, risks, docs changes and finish options. | `release-packet.md` |
| Deployment plan | Target environment, release candidate, deploy command, approval, rollout window and stop criteria. | CI/CD tool, GitHub environments |
| Rollout plan | Feature flag, canary, blue-green, staged percentage, cohort, traffic split, promotion/abort rules. | OpenFeature, Argo Rollouts |
| Rollback/recovery plan | Revert, disable flag, rollback deployment, unpublish, restore, data compensation or incident mitigation. | Runbook/release packet |
| Environment matrix | dev/stage/prod/local/mobile/store/registry targets, secrets, branch/tag rules and owner. | GitHub environments, platform docs |
| CI/CD workflow inventory | Jobs, triggers, permissions, secrets, artifacts, caches, concurrency and external actions. | GitHub Actions |
| Versioning policy | SemVer, calendar versioning, prerelease, deprecation, compatibility and support window. | SemVer, Conventional Commits |
| Changelog | Human-readable Added, Changed, Deprecated, Removed, Fixed, Security sections. | Keep a Changelog |
| Release notes | User-facing impact, migration steps, compatibility, known issues and support contact. | Product docs |
| Artifact manifest | Build outputs, hashes/signatures, SBOM/provenance notes, storage and retention. | Security/supply-chain workflow |
| Observability map | Dashboards, traces, logs, metrics, alert owners, redaction and sampling notes. | OpenTelemetry |
| SLO spec | User journey, SLI, SLO, measurement source, alert policy and accepted gap. | Google SRE |
| Operations runbook | Deploy, rollback, first response, escalation, common failures and diagnostics. | SRE/runbook practice |
| Incident record | Timeline, impact, mitigation, communications, owner and follow-up tasks. | SRE incident management |
| Postmortem | Impact, detection, root causes, contributing factors, action items and review status. | Google SRE postmortem |
| Automation candidate | Manual stability evidence, trigger/cadence, write policy, verification and disable path. | Product-Agent OS automation-promoter |
| Post-release review | Actual metrics, defects, support signals, latency/cost, feedback and next decision. | Business/product metrics, DORA |

## Project application instructions

1. Classify release work before implementation. Release triggers include package publishing, tags, GitHub Releases, app store/marketplace submission, artifact upload, deployment, CI workflow mutation, production config, release notes, public API change, plugin release, SDK release, installer build, migration release or automation promotion.
2. Keep external release actions read-only/staged until release scope, owner, target environment, approval boundary, version impact, evidence, rollback and residual risk are explicit.
3. Determine release type: internal deploy, public package, SDK, plugin, app, desktop installer, mobile build, docs release, model/prompt release, database migration, infrastructure change or automation candidate.
4. Record versioning policy and compatibility impact. For public API/package/plugin/SDK, include SemVer impact or an explicit non-SemVer policy.
5. Maintain changelog and release notes separately when needed: changelog captures notable changes; release notes explain user impact, migration and operational instructions.
6. Require current build/test/docs/eval/runtime evidence before release readiness claims. Inspection-only release readiness is blocked.
7. Require artifact evidence for release outputs: filenames, versions, checksums/signatures where used, storage location, retention and recreation command.
8. For deployable services, separate build, release and run stages unless the platform intentionally combines them and the risk is accepted.
9. For production services, define SLIs/SLOs or an explicit accepted gap before claiming operational readiness.
10. Define observability evidence: logs, metrics, traces, dashboard links, alert owner, data redaction and expected post-release signals.
11. Define rollout strategy: immediate release, release train, staged rollout, feature flag, canary, blue-green, shadow traffic or manual promotion.
12. Define stop criteria and rollback/recovery path before release. Rollback can be revert, redeploy previous artifact, disable flag, unpublish, restore backup, compensate data or activate incident mitigation.
13. For GitHub Actions or CI/CD changes, document triggers, permissions, environments, required reviewers, branch/tag restrictions, secrets, artifacts, concurrency and external action pinning.
14. For GitHub deployment environments, treat required reviewers, wait timers, branch/tag restrictions, custom protection rules and environment secrets as release controls.
15. For GitOps-style workflows, document desired state source, reconciliation controller, drift behavior, approval path and rollback/revert behavior.
16. For progressive delivery, document cohorts, traffic weights, health checks, analysis metrics, manual judgement points, promotion/abort rules and blast radius.
17. For feature flags, document default value, owner, targeting rules, cleanup date, observability, kill-switch behavior and failure mode.
18. For incidents and failed releases, create an incident record and postmortem when impact criteria are met; do not hide failed deploys from learning records.
19. For DORA metrics, record definitions and measurement source. Use trends for process improvement, not individual performance.
20. Promote recurring release/ops workflows only after manual success evidence, stable inputs/outputs, owner, approval requirements, verification and rollback/disable path exist.

## Product-Agent OS candidate rules

### Discovery signals

- Directories: `.github/workflows/`, `.github/actions/`, `.github/dependabot.yml`, `deploy/`, `deployment/`, `release/`, `releases/`, `ops/`, `runbooks/`, `infra/`, `charts/`, `k8s/`, `helm/`, `terraform/`, `argocd/`, `flux/`, `observability/`, `monitoring/`, `alerts/`, `packages/`, `dist/`
- Files: `CHANGELOG.md`, `RELEASE.md`, `SECURITY.md`, `CODEOWNERS`, `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Dockerfile`, `docker-compose.*`, `mkdocs.yml`, `openapi.*`, `release-readiness.md`, `release-packet.md`, `runbook.md`, `slo.md`, `postmortem.md`, `sbom.*`, `cyclonedx.*`, `spdx.*`
- Terms: release, deploy, publish, tag, version, SemVer, changelog, release notes, artifact, rollback, rollout, canary, blue-green, feature flag, SLO, SLI, incident, postmortem, runbook, DORA, CI, CD, GitHub Actions, environment, approval, registry, package, marketplace, app store, notarization
- Dependency/tool signals: GitHub Actions, GitHub Releases, GitHub environments, npm/PyPI/crates.io/package registries, Docker/OCI registries, OpenTelemetry, Prometheus, Grafana, Argo Rollouts, Argo CD, Flux, OpenFeature, LaunchDarkly, Sentry, Datadog, PagerDuty, Opsgenie, semantic-release, release-please

### Readiness gates

| Gate | Trigger | Block condition |
| --- | --- | --- |
| `release_scope_present` | Any release/deployment/publish request | Release type, target, owner or external boundary is missing. |
| `release_evidence_present` | Release readiness claim | Current build, test, docs, eval, runtime or artifact evidence is missing. |
| `version_impact_present` | Public API, package, SDK, plugin, app or docs release | SemVer/non-SemVer policy, compatibility impact or deprecation notes are missing. |
| `changelog_release_notes_present` | User-visible or public release | Changelog/release notes omit user impact, migration, compatibility or known issues. |
| `artifact_manifest_present` | Artifact, package, installer, image, binary or docs build | Artifact names, versions, creation command, storage or integrity notes are missing. |
| `rollout_strategy_present` | Runtime deployment or staged launch | Strategy, cohorts/traffic, promotion, abort criteria or blast radius is missing. |
| `rollback_recovery_present` | Any release with user/runtime/external impact | Revert, redeploy, flag disable, unpublish, restore, compensation or mitigation path is missing. |
| `environment_approval_boundary_present` | CI/CD environment, production, registry, marketplace or store | Required approval, branch/tag rule, secret boundary or external-write policy is missing. |
| `ci_cd_governance_present` | Workflow/action/pipeline change | Triggers, permissions, secrets, artifacts, caches, concurrency or external action policy is missing. |
| `observability_release_evidence_present` | Production service, job, API, AI agent or user-facing runtime | Logs, metrics, traces, dashboard, alert owner or redaction notes are missing. |
| `slo_or_operational_gap_present` | Production service with reliability expectations | SLIs/SLOs or explicit accepted gap is missing. |
| `operations_runbook_present` | Production deploy, incident-prone path or on-call service | Deploy, rollback, first response, escalation and diagnostics are missing. |
| `incident_response_path_present` | Production/runtime release | Incident criteria, owner, communication path and postmortem trigger are missing. |
| `post_release_measurement_present` | Product-facing or operationally risky release | Metrics, support signals, defects, latency/cost or review date are missing. |
| `external_release_approval_present` | Tag, publish, release creation, artifact upload, deployment, PR, push, package registry, marketplace or store action | Explicit approval and rollback/unpublish path are missing. |
| `automation_manual_stability_present` | Release/ops workflow promotion to automation | Manual success evidence, stable inputs/outputs, owner, verification or disable path is missing. |
| `release_evidence_before_completion` | Any release-ready/works/deployed/published claim | Current evidence or explicit gap is missing. |

## Candidate eval fields

- Release scope, target, owner and external boundary are explicit.
- Release readiness claim cites current build/test/docs/eval/runtime/artifact evidence or an explicit gap.
- Version impact and compatibility/deprecation notes are documented.
- Changelog/release notes are user-facing and not just commit log summaries.
- Artifact manifest includes version, location and recreation/integrity notes.
- Rollout strategy includes promotion, abort and blast-radius control.
- Rollback/recovery path is executable for the release type.
- GitHub Actions or CI/CD change includes triggers, permissions, secrets, environments, approvals and artifacts.
- Observability evidence includes traces, metrics, logs, dashboards, alert owner and redaction notes where applicable.
- SLO or operational gap is explicit for production services.
- Incident and postmortem criteria are defined for runtime releases.
- Post-release measurement links actual signals back to product/reliability hypothesis.
- External publish/tag/deploy/upload/PR/push/store actions remain approval-bound.
- Automation candidate remains candidate-only until manual stability evidence exists.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| Delivery metrics | DORA metrics, internal deployment data | Define measurement source and avoid individual performance targeting. |
| Release readiness | `release-readiness.md`, `release-packet.md` | Evidence packet before tag/publish/deploy/readiness claim. |
| Versioning | SemVer, Conventional Commits, release-please/semantic-release candidates | Use when public compatibility matters; do not force on private apps. |
| Changelog/release notes | Keep a Changelog, GitHub Releases | Human-readable user impact and migration notes. |
| CI/CD | GitHub Actions, environments, protected branches, required reviewers | Treat workflow changes and deployment environments as controlled release surfaces. |
| Progressive delivery | OpenFeature, Argo Rollouts, feature flag provider, traffic router | Pick by stack; document owner, cleanup and abort path. |
| GitOps | CNCF GitOps, Argo CD, Flux | Useful for declarative infra/app state, not mandatory for every project. |
| Observability | OpenTelemetry, Prometheus/Grafana, vendor dashboards | Runtime evidence for release and incident response. |
| Reliability | SLO docs, runbooks, incident records, postmortems | Needed when users depend on runtime behavior. |
| Automation | Product-Agent OS automation candidate packet | Manual success before active automation. |

## Типовые сбои

- Release readiness is claimed from code inspection or passing local tests only.
- Release notes are commit summaries with no user impact or migration guidance.
- SemVer bump ignores public API, generated client, plugin or data compatibility.
- Rollback is named but cannot recover the actual release target.
- Package publish, tag, release creation, artifact upload, deployment or store submission happens without explicit approval.
- CI workflow change silently expands permissions, secrets access or deployment triggers.
- Feature flag ships without owner, cleanup date or kill-switch behavior.
- Progressive delivery relies on health checks that do not represent user/business outcomes.
- Observability is added after release, so no runtime evidence exists during incident response.
- DORA metrics become quotas or individual performance metrics.
- Postmortem is skipped because the release was rolled back quickly.
- Automation is activated before manual workflow stability is proven.

## Open questions for deeper research

- Should Product-Agent OS generate a universal `release-readiness.md` for every release-mode workflow and keep `release-packet.md` for PR/user-facing summary?
- Which release types require artifact integrity metadata: docs site, plugin package, SDK, desktop installer, mobile build, container image?
- Should `rollout_strategy_present` be required for all production services or only user-impacting behavior changes?
- How should Product-Agent OS distinguish release train, continuous deployment and manual approval workflows during discovery?
- Should DORA metrics live in this section or in Business & Product measurement when they are used for organizational improvement?
- Which operations evidence should be mandatory for local-first desktop and mobile releases: signing, notarization, app store review, installer rollback, crash reporting?
- How should Codex automations connect to release operations without becoming an unapproved production scheduler?

## Sources

- [DORA software delivery performance metrics](https://dora.dev/guides/dora-metrics/)
- [Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
- [Google SRE: Release Engineering](https://sre.google/sre-book/release-engineering/)
- [Google SRE: Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [The Twelve-Factor App](https://www.12factor.net/)
- [GitHub Actions workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows)
- [GitHub deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [CNCF GitOps glossary](https://glossary.cncf.io/gitops/)
- [Argo Rollouts](https://argo-rollouts.readthedocs.io/en/latest/)
- [OpenFeature introduction](https://openfeature.dev/docs/reference/intro/)
- [Codex: Run verified operations](https://developers.openai.com/codex/use-cases/verified-operations-workflows)
- [Context7 research](../context7-research.md)
