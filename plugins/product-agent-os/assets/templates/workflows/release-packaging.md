# Release Packaging Workflow

Source status: `codex-plugin-template`

Use this workflow when a package, SDK, plugin, app, desktop build, mobile build, or open-source project needs release readiness review before tagging, publishing, creating releases, uploading artifacts, or claiming release readiness.

## Inputs

- User goal, release scope, release owner, package or app type, target package registry, and publish approval boundary.
- Package metadata, version, SemVer impact, changelog, release notes, public API or compatibility notes, docs and examples.
- Build evidence, test evidence, docs evidence, artifact evidence, security notes, license notes, provenance or SBOM notes when available.
- Rollout plan, rollback or unpublish path, owner review, residual risk, and approvals needed before external release actions.

## Process

1. Keep the workflow read-only until release scope, package metadata, version, SemVer impact, changelog, build evidence, test evidence, docs evidence, security notes, license notes, artifacts, owner review, publish approval, package registry, rollback, and residual risk are explicit.
2. Inventory release files, package manifests, version files, changelog, release docs, security notes, license files, artifacts, package registry settings, rollback notes, and approval notes as `present_unverified`.
3. Determine the release scope: package, SDK, plugin, app, desktop installer, mobile build, docs release, or open-source release.
4. Check version impact using SemVer terms: major, minor, patch, prerelease, deprecation, compatibility, generated clients, and public API impact.
5. Require changelog and release notes to match the release scope and owner-approved version impact.
6. Require build evidence, test evidence, docs evidence, artifact evidence, security notes, license notes, and package metadata before a release readiness verdict.
7. Check package registry and distribution boundaries: npm, PyPI, crates.io, GitHub Releases, app store, internal registry, plugin marketplace, or private artifact storage.
8. Keep external actions approval-bound: do not publish, do not tag, do not create release, do not upload artifacts, do not push branches, do not open pull requests, and do not mutate package registry settings without explicit approval.
9. Do not claim release readiness from code inspection only. If evidence is missing, record the gap and stop at the smallest evidence-gathering step.
10. Keep the Scenario Handoff concise when another role must continue release prep.

## Outputs

- Staged release readiness artifact with:
  - release scope;
  - package metadata;
  - version;
  - SemVer impact;
  - changelog;
  - build evidence;
  - test evidence;
  - docs evidence;
  - security notes;
  - license notes;
  - artifacts;
  - package registry;
  - owner review;
  - publish approval;
  - tag boundary;
  - rollback or unpublish path;
  - residual risk.
- Finish options that remain staged only:
  - keep branch;
  - PR packet;
  - approved apply;
  - rollback;
  - cleanup.
- Scenario Handoff:
  - sources/context used;
  - assumptions;
  - files touched;
  - files proposed;
  - verification evidence;
  - open risks;
  - recommended next role;
  - stop reason.

## Verification

- Release scope, package metadata, version, SemVer impact, changelog, build evidence, test evidence, docs evidence, security notes, license notes, artifacts, package registry, owner review, publish approval, rollback, and residual risk are explicit.
- Release readiness claims cite current build evidence, test evidence, docs evidence, artifact evidence, owner review, and approval status.
- Tagging, publishing, package registry mutation, release creation, artifact upload, PR creation, branch push, marketplace submission, and store submission remain approval-bound.
- No external release action occurred unless approval evidence is recorded.

## Stop Conditions

- Release scope, package metadata, version, SemVer impact, changelog, build evidence, test evidence, docs evidence, security notes, license notes, artifacts, package registry, owner review, publish approval, rollback, or residual risk is missing.
- A release readiness verdict would rely on inspection-only evidence.
- The task requires tagging, publishing, release creation, artifact upload, package registry mutation, PR creation, branch push, marketplace submission, store submission, signing, notarization, or external distribution without explicit approval.
