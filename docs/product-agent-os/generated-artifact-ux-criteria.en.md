# Generated Artifact UX Criteria

Source status: `project evidence`

This page defines acceptance criteria for local Product-Agent OS HTML, JSON, and report artifacts. It does not prove that a specific file has already been accepted: acceptance still needs current evidence, owner review, or an explicit accepted gap.

Generated artifacts are review surfaces. They can expose structure, claim ceilings, source links, and next safe action, but they do not replace source files, command evidence, or owner decisions.

## Usable Artifact

| Area | Requirement | Do not claim |
| --- | --- | --- |
| Navigation | Main reading path, visible risk section, owning source links, and safe next action. | That an artifact replaces source files or review. |
| Readability | Dense tables need short headings, stable columns, and clear empty states. | That HTML is public-ready without current checks. |
| Offline | The artifact should work without external URLs, external scripts, or provider calls. | That browser proof ran without evidence. |
| Print | Print output should preserve headings, claim ceilings, and evidence refs. | That a printable view is a release artifact. |
| Claim language | `ready`, `fixed`, `verified`, `complete`, and `release-ready` require current command/runtime/eval evidence or an accepted gap. | That a generated view is proof by itself. |

## Vale And Language Guard

Local Vale is currently advisory. Warnings help find readiness wording, but they are not an automatic blocker until an owner-approved threshold, report retention policy, and rollback path exist.

## Storybook Trigger

Storybook remains deferred. Revisit it only when a component surface, repeated visual states, owner-approved install path, and browser/visual evidence plan exist. Until then, generated artifact UX is checked through docs tests, static HTML checks, and owner review.

## Acceptance Checklist

- `generated_view_policy` explicitly says `orientation_only_not_proof`.
- Source-boundary labels and unsupported claims are visible.
- The artifact gives a next safe action, not a hidden mutation recommendation.
- It contains no raw private chat logs, secrets, credentials, unredacted PII, or raw source bodies.
- Cleanup guidance is marked preview-only.
- Browser, runtime, provider, target mutation, release, and publication claims are absent without separate approval.

## Verification

Minimum gate for this docs slice: docs unittest, `tools/check_docs.py`, strict MkDocs smoke under `.docs-tools/reports`, JSON packet validation, and `git diff --check`. Browser proof, screenshots, broad Vale enforcement, and Storybook remain approval-required.

## Site completeness check

Compare expected RU/EN routes with HTML, then check internal links/anchors, search and Mermaid rendering. Existing-link checks miss a new page when navigation is also stale. A build pass is not browser proof. [Docs update](../playbooks/docs-update.md).
