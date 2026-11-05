# Delivery, Release & Operations

Source status: `official + verified methodology + vendor documentation + tool-assisted + experiment`

Источники: [DORA software delivery performance metrics](https://dora.dev/guides/dora-metrics/), [Google SRE SLO chapter](https://sre.google/sre-book/service-level-objectives/), [Google SRE Release Engineering](https://sre.google/sre-book/release-engineering/), [Google SRE Postmortem Culture](https://sre.google/sre-book/postmortem-culture/), [OpenTelemetry documentation](https://opentelemetry.io/docs/), [Twelve-Factor App](https://www.12factor.net/), [GitHub Actions workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows), [GitHub deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments), [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository), [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), [Semantic Versioning](https://semver.org/), [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), [CNCF GitOps](https://glossary.cncf.io/gitops/), [Argo Rollouts](https://argo-rollouts.readthedocs.io/en/latest/), [OpenFeature](https://openfeature.dev/docs/reference/intro/), [Codex verified operations](https://developers.openai.com/codex/use-cases/verified-operations-workflows), [Context7 research](../sources/context7-research.md), [research dossier](../sources/methodology-research/delivery-release-operations.md).

## Deep research цель

Delivery, Release & Operations слой описывает how the system ships, runs, recovers and learns. Для большого проекта release readiness не равен passing tests: нужны scope, owner, version impact, artifacts, rollout, rollback, observability, approvals, incident path and post-release learning.

Главный принцип: release/deploy/publish work сначала собирает auditable evidence packet, потом делает external action. Нельзя tag, publish, create release, upload artifact, deploy, mutate package registry, open PR, push branch, submit to marketplace/store or activate automation без explicit approval and rollback/recovery path.

## Поддержанные факты

- DORA metrics define delivery performance through change lead time, deployment frequency, failed deployment recovery time, change fail rate and deployment rework rate.
- Google SRE guidance treats SLOs as user-relevant reliability targets and release engineering as a discipline for repeatable, auditable releases.
- OpenTelemetry provides cross-stack vocabulary for traces, metrics and logs as runtime release evidence.
- GitHub Actions workflows, environments and deployments define release controls such as triggers, permissions, required reviewers, wait timers, branch/tag restrictions and environment secrets.
- Keep a Changelog, Semantic Versioning and Conventional Commits provide compatible but different release communication and versioning practices.
- CNCF GitOps and Argo Rollouts support desired-state operations and progressive delivery concepts such as canary, blue-green, promotion and rollback.
- OpenFeature gives a feature-flag vocabulary for runtime rollout, targeting and kill-switch behavior.
- Codex verified operations supports approval-bound, auditable operational workflows before external actions.

## Assumptions

- Release readiness is broader than tests passing; it includes scope, owner, version impact, artifacts, rollout, rollback, observability, approvals and post-release learning.
- External release actions should be staged or draft-first until approval boundary and rollback path are explicit.
- DORA metrics are for process learning, not individual quotas.
- Feature flags and progressive delivery reduce blast radius only when owner, cleanup, observability and abort criteria exist.
- Automation promotion is unsafe without manual success evidence, stable inputs/outputs, owner, verification and disable path.

## Инструкции применения на проекте

1. Классифицировать release work до реализации. Triggers: publish, deploy, tag, GitHub Release, artifact upload, package registry, marketplace, app store, installer, SDK, plugin, public API, migration release, CI workflow mutation, production config, automation promotion.
2. Держать external release actions read-only/staged, пока release scope, owner, target, approval boundary, version impact, evidence, rollback and residual risk не стали explicit.
3. Определить release type: internal deploy, public package, SDK, plugin, app, desktop installer, mobile build, docs release, model/prompt release, database migration, infrastructure change or automation candidate.
4. Для public API/package/plugin/SDK/app release фиксировать SemVer impact или explicit non-SemVer policy.
5. Держать changelog и release notes раздельно, если это помогает: changelog фиксирует notable changes, release notes объясняют user impact, migration, compatibility and known issues.
6. Не заявлять release readiness from inspection-only evidence. Нужны current build/test/docs/eval/runtime/artifact evidence или explicit gap.
7. Для artifacts фиксировать filenames, versions, creation command, storage location, retention and integrity notes where applicable.
8. Для deployable services разделять build, release and run stages, либо явно фиксировать accepted platform exception.
9. Для production services определить SLIs/SLOs или explicit accepted gap.
10. Для runtime release определить observability evidence: logs, metrics, traces, dashboards, alert owner, redaction and expected post-release signals.
11. Определить rollout strategy: immediate release, release train, staged rollout, feature flag, canary, blue-green, shadow traffic or manual promotion.
12. Определить stop criteria and rollback/recovery path before release: revert, redeploy previous artifact, disable flag, unpublish, restore backup, compensate data or incident mitigation.
13. Для GitHub Actions/CI/CD changes фиксировать triggers, permissions, environments, required reviewers, branch/tag rules, secrets, artifacts, concurrency and external action pinning.
14. Для GitHub deployment environments считать required reviewers, wait timers, branch/tag restrictions, custom protection rules and environment secrets release controls.
15. Для GitOps-style workflows фиксировать desired state source, reconciliation controller, drift behavior, approval path and rollback/revert behavior.
16. Для progressive delivery фиксировать cohorts, traffic weights, health checks, analysis metrics, manual judgement, promotion/abort rules and blast radius.
17. Для feature flags фиксировать default value, owner, targeting rules, cleanup date, observability, kill-switch behavior and failure mode.
18. Для incidents и failed releases создавать incident record and postmortem, когда impact criteria выполнены; не скрывать failed deploys из learning loop.
19. Для DORA metrics фиксировать definitions and measurement source. Использовать trends for process improvement, not individual performance.
20. Promote recurring release/ops workflows only after manual success evidence, stable inputs/outputs, owner, approval requirements, verification and rollback/disable path exist.

## Применяемые методологии разработки

| Методология | Когда применять | Как выглядит в проекте |
| --- | --- | --- |
| Release engineering | Packages, apps, services, plugins, SDKs, installers, docs releases | Release scope, reproducible build, artifacts, version impact, owner, approvals and release process. |
| Continuous delivery discipline | Frequent changes, shared branches, deployment pipeline | Small batches, automated checks, release candidates, environment promotion, rollback/recovery path. |
| DORA measurement | Team wants delivery performance trend | Change lead time, deployment frequency, failed deployment recovery time, change fail rate, deployment rework rate. |
| SRE / SLO-driven operations | Runtime service has availability, latency or support expectations | SLIs/SLOs, error-budget thinking, alerts, runbooks and incident response. |
| Observability-driven release | Runtime behavior must be diagnosable | OpenTelemetry-style traces, metrics, logs, dashboards, alert owners and redaction policy. |
| Progressive delivery | Release blast radius must be controlled | Feature flags, staged rollout, canary, blue-green, traffic shifting, manual judgement and automated rollback. |
| GitOps / desired-state operations | Declarative infra/app state is managed via source control | Desired state, reconciliation mechanism, drift handling, approval and rollback are documented. |
| CI/CD governance | Workflow can publish, deploy, access secrets or mutate environments | Triggers, permissions, environments, reviewers, branch/tag rules, artifacts and external action policy. |
| Versioning and changelog discipline | Public API, package, SDK, plugin, app or docs release | SemVer impact, compatibility/deprecation notes, changelog categories and user-facing release notes. |
| Incident response and postmortem learning | Production incident, failed deployment, user-impacting regression | Incident record, timeline, mitigation, root causes, action items, owner and follow-up review. |
| Automation promotion | Repeated operations may become automation | Manual success evidence, stable inputs/outputs, owner, verification, approval and rollback/disable path. |

## Инструменты, артефакты и стандарты документирования

- `release-readiness.md`: scope, owner, version, SemVer impact, evidence, artifacts, approval, rollback, residual risk.
- `release-packet.md`: PR/release summary, user impact, checks, risks, docs changes, finish options.
- `deployment-plan.md`: target environment, release candidate, deploy command, approval, rollout window, stop criteria.
- `rollout-plan.md`: feature flag, canary, blue-green, staged percentage, cohort, traffic split, promotion/abort rules.
- `rollback-recovery-plan.md`: revert, disable flag, rollback deployment, unpublish, restore, data compensation, mitigation.
- `environment-matrix.md`: dev/stage/prod/local/mobile/store/registry targets, secrets, branch/tag rules, owner.
- `ci-cd-workflow-inventory.md`: jobs, triggers, permissions, secrets, artifacts, caches, concurrency, external actions.
- `versioning-policy.md`: SemVer, calendar versioning, prerelease, deprecation, compatibility, support window.
- `CHANGELOG.md`: Added, Changed, Deprecated, Removed, Fixed, Security sections.
- `release-notes.md`: user impact, migration steps, compatibility, known issues, support contact.
- `release-artifact-manifest.md`: build outputs, hashes/signatures, SBOM/provenance notes, storage, retention.
- `observability-map.md`: dashboards, traces, logs, metrics, alert owners, redaction, sampling notes.
- `slo-spec.md`: user journey, SLI, SLO, measurement source, alert policy, accepted gap.
- `operations-runbook.md`: deploy, rollback, first response, escalation, common failures, diagnostics.
- `incident-record.md`: timeline, impact, mitigation, communications, owner, follow-up tasks.
- `postmortem.md`: impact, detection, root causes, contributing factors, action items, review status.
- `automation-candidate.md`: manual stability evidence, trigger/cadence, write policy, verification, disable path.
- `post-release-review.md`: actual metrics, defects, support signals, latency/cost, feedback, next decision.

## Что еще включить в deep research

- Maturity levels: `baseline`, `team`, `production`, `regulated`.
- Release types: docs-only, internal app, production service, public package, plugin, SDK, desktop installer, mobile app, AI model/prompt release, infrastructure release, data migration.
- Release train vs continuous deployment vs manual approval policy.
- Feature flag lifecycle: owner, default, cohort, cleanup, kill switch, observability, debt removal.
- Progressive delivery decision policy: when simple release is enough and when canary/blue-green/manual promotion is required.
- GitHub environments policy: required reviewers, wait timers, branch/tag restrictions, secrets, custom protection rules.
- Artifact integrity policy: checksums, signatures, SBOM/provenance, storage and retention by release type.
- Incident severity and postmortem triggers: user-visible degradation, data loss, rollback, manual intervention, monitoring failure.
- DORA measurement design: source of data, team scope, anti-Goodhart warning, interpretation cadence.
- Automation promotion path: manual thread -> playbook -> skill -> plugin -> automation, with disable/rollback path.

## Product-Agent OS routing

- `workspace-discovery-auditor` detects release packaging signals: package metadata, versions, changelog, build evidence, test evidence, docs evidence, security/license notes, artifacts, rollback, owner review and publish approval.
- `requirements-author` records release target, user impact, compatibility, operational constraints, approval boundary and post-release measurement.
- `implementation-planner` blocks plan-ready status when release scope, version impact, evidence, rollout, rollback, environment approval or ownership is missing.
- `test-eval-designer` defines release evidence: build/test/docs/eval/runtime checks, artifact verification, smoke checks, rollback verification and post-release monitoring.
- `risk-reviewer` checks release risk, unsupported readiness claims, external action approvals, migration/security/data impacts and residual risk.
- `pr-release-operator` prepares release packet, changelog/release notes, finish options and staged external action plan.
- `learning-loop-maintainer` records release outcomes, failures, DORA/post-release signals and postmortem follow-ups.
- `automation-promoter` can only create candidate-only automation after manual release/ops workflow stability is evidenced.

## Candidate readiness gates

- `release_scope_present`: release type, target, owner and external boundary are explicit.
- `release_evidence_present`: current build, test, docs, eval, runtime or artifact evidence exists.
- `version_impact_present`: SemVer/non-SemVer policy, compatibility impact and deprecation notes are documented.
- `changelog_release_notes_present`: changelog/release notes include user impact, migration, compatibility and known issues where applicable.
- `artifact_manifest_present`: artifact names, versions, creation command, storage and integrity notes are present.
- `rollout_strategy_present`: strategy, cohorts/traffic, promotion, abort criteria and blast radius are explicit.
- `rollback_recovery_present`: revert, redeploy, flag disable, unpublish, restore, compensation or mitigation path is executable.
- `environment_approval_boundary_present`: approval, branch/tag rule, secret boundary and external-write policy are explicit.
- `ci_cd_governance_present`: triggers, permissions, secrets, artifacts, caches, concurrency and external action policy are reviewed.
- `observability_release_evidence_present`: logs, metrics, traces, dashboard, alert owner and redaction notes exist where applicable.
- `slo_or_operational_gap_present`: SLIs/SLOs or explicit accepted gap exists for production service.
- `operations_runbook_present`: deploy, rollback, first response, escalation and diagnostics are documented.
- `incident_response_path_present`: incident criteria, owner, communication path and postmortem trigger are present.
- `post_release_measurement_present`: metrics, support signals, defects, latency/cost or review date are defined.
- `external_release_approval_present`: tag, publish, release creation, artifact upload, deployment, PR, push, package registry, marketplace or store action has explicit approval and rollback/unpublish path.
- `automation_manual_stability_present`: manual success evidence, stable inputs/outputs, owner, verification and disable path exist before automation.
- `release_evidence_before_completion`: any release-ready/works/deployed/published claim cites current evidence or explicit gap.

## Candidate eval fields

- Release scope, target, owner and external boundary are present.
- Current build/test/docs/eval/runtime/artifact evidence is linked.
- Version impact and compatibility/deprecation notes are documented.
- Changelog and release notes include user impact and migration guidance where applicable.
- Artifact manifest includes names, versions, creation command, storage and integrity notes.
- Rollout strategy includes cohorts/traffic, promotion, abort criteria and blast radius.
- Rollback/recovery path is executable for this release type.
- CI/CD governance includes triggers, permissions, secrets, artifacts, caches, concurrency and approvals.
- Observability evidence includes logs, metrics, traces, dashboards, alert owner and redaction notes.
- External release action has explicit approval and rollback/unpublish path.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| Delivery metrics | DORA | Trend-level process improvement; avoid individual performance use. |
| Reliability target | SLO/SLI sheet | User journey, measurement source, alerting and accepted gap. |
| CI/CD governance | GitHub Actions environments | Required reviewers, wait timers, branch/tag restrictions, environment secrets. |
| Release communication | Keep a Changelog, SemVer, Conventional Commits | Use each for its appropriate layer: change categories, version impact, commit signal. |
| GitOps | Desired-state source + reconciliation controller | Requires drift, approval and rollback model. |
| Progressive delivery | Argo Rollouts or platform equivalent | Canary, blue-green, analysis, promotion and abort behavior. |
| Feature flags | OpenFeature or platform equivalent | Owner, targeting, cleanup, kill switch and observability. |
| Operations docs | `runbook.md`, `slo.md`, `release-readiness.md` | Common local filenames and templates for release evidence. |
| Package signals | `package.json`, `pyproject.toml`, `go.mod`, `mkdocs.yml` | Discovery signals for versioning/build/release impact. |
| Verified operations | Codex verified operations | Approval-bound, auditable external actions and retries. |

## Проверки

- Release scope, target, owner and external boundary are explicit.
- Release readiness cites current build/test/docs/eval/runtime/artifact evidence or explicit gaps.
- Version impact and compatibility/deprecation notes are documented.
- Changelog/release notes are user-facing and not only commit summaries.
- Artifact manifest includes version, location, creation command and integrity notes where relevant.
- Rollout strategy includes promotion, abort and blast-radius control.
- Rollback/recovery path is executable for this release type.
- GitHub Actions/CI/CD changes include triggers, permissions, secrets, environments, approvals and artifacts.
- Observability evidence includes traces, metrics, logs, dashboards, alert owner and redaction notes where applicable.
- SLO or operational gap is explicit for production services.
- Incident and postmortem criteria are defined for runtime releases.
- Post-release measurement links actual signals back to product/reliability hypothesis.
- External publish/tag/deploy/upload/PR/push/store actions remain approval-bound.
- Automation candidate remains candidate-only until manual stability evidence exists.

## Типовые сбои

- Release readiness is claimed from code inspection or passing local tests only.
- Release notes summarize commits but omit user impact and migration guidance.
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

## Unsupported claims not adopted

- "Tests passed, so release is ready." Release readiness also requires artifact, rollout, rollback, observability and approval evidence.
- "Rollback is just revert." Some releases need unpublish, redeploy, flag disable, restore or compensation.
- "Feature flags remove release risk." They need owner, kill switch, observability and cleanup.
- "DORA metrics prove individual performance." They are process metrics and should not be used as personal quotas.
- "Automation is safer because it is repeatable." Repeatability without approvals and disable path can repeat damage.

## Open questions for future implementation

- Which release maturity labels should Product-Agent OS use: `baseline`, `team`, `production`, `regulated`?
- Which release types need separate templates: docs-only, package, plugin, SDK, desktop/mobile, AI prompt/model, infrastructure or data migration?
- When should progressive delivery be required instead of simple release?
- Which artifact integrity evidence should be default: checksums, signatures, SBOM, provenance or none for docs-only releases?
- How should incident severity and postmortem triggers be encoded for small projects?
- Should DORA measurement live in delivery docs, metrics docs or both?

## Scheduled и Cloud delivery

Native schedule — отдельный route с local/cloud prerequisites. Publish cloud environment фиксирует reusable setup для новых tasks; это не публикация продукта. [Schedules](../runtime/automations-github.md), [Cloud](../codex/surfaces.md). Release по-прежнему требует current evidence и authority.
