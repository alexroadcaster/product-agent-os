---
title: "Archive - Product-Agent OS: pre-Track 8 implemented plans and specs inventory"
---

# Archive - Product-Agent OS: pre-Track 8 implemented plans and specs inventory {#product-agent-os-pre-track-8-implemented-plans-and-specs-inventory}

> Historical source record. Dates and verdicts below describe that run; use current guides for present behavior.

Source status: `internal project inventory + implementation-history index`

Date: **2026-05-27**.

Purpose of this artifact: record a verifiable queue of files that describe Product-Agent OS plans, specs and transitional pre-development artifacts implemented before Track 8. This list is needed for the following deep technical and product analysis of each file in sequence, and for expanding the `Task 22` matrix in the Track 9 methodology intelligence plan (`docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`).

This file is an input index for the analysis. It does not close gaps by itself: each file must be analyzed separately to extract user value, implemented behavior, technical contracts, remaining risks, required docs/evals/runtime synchronization and candidate rows for `Task 22`.

## Primary analysis queue

| Order | Block | Source file | Why analyze it for `Task 22` |
| --- | --- | --- | --- |
| 1 | Product-Agent OS base spec | [docs/product-agent/product-agent-os-plugin-spec.md](../product-agent/product-agent-os-plugin-spec.md) | Base product contract for the plugin: tracks, intended surfaces, lifecycle, generated artifacts and safety model. |
| 2 | Track 1: plugin core and contracts | `docs/superpowers/plans/2026-05-14-product-agent-os-plugin-core.md` | Initial implementation plan for package structure, contracts, validators, fixture harness and safe merge utilities. |
| 3 | Track 2: lifecycle skills design | [docs/superpowers/specs/2026-05-14-product-agent-os-lifecycle-skills-design.md](../superpowers/specs/2026-05-14-product-agent-os-lifecycle-skills-design.md) | Design intent for reusable lifecycle skills, handoffs, verification and role boundaries. |
| 4 | Track 2: lifecycle skills plan | `docs/superpowers/plans/2026-05-14-product-agent-os-lifecycle-skills.md` | Implementation plan for packaged skills and acceptance gates for lifecycle orchestration. |
| 5 | Track 3: generated infrastructure design | [docs/superpowers/specs/2026-05-14-product-agent-os-generated-infrastructure-design.md](../superpowers/specs/2026-05-14-product-agent-os-generated-infrastructure-design.md) | Source for staged-first infrastructure generation, renderer boundaries and no-hidden-write contract. |
| 6 | Track 3: generated infrastructure plan | `docs/superpowers/plans/2026-05-14-product-agent-os-generated-infrastructure.md` | Implementation slices for renderer, templates, registry, fixture evals and staged output checks. |
| 7 | Track 4: production hardening design | [docs/superpowers/specs/2026-05-14-product-agent-os-production-hardening-design.md](../superpowers/specs/2026-05-14-product-agent-os-production-hardening-design.md) | Design source for approval records, manifest validation, safe apply, rollback, source policy and automation gates. |
| 8 | Track 4: production hardening plan | `docs/superpowers/plans/2026-05-14-product-agent-os-production-hardening.md` | Implementation plan for safe merge/apply, rollback, hooks, source policy, automation promotion and verification. |
| 9 | Track 4 optional: Agents SDK runner design | [docs/superpowers/specs/2026-05-14-product-agent-os-agents-sdk-runner-design.md](../superpowers/specs/2026-05-14-product-agent-os-agents-sdk-runner-design.md) | Rejected/design-only runner boundary that helps prevent Task 22 docs from reintroducing a standalone runtime path. |
| 10 | Track 5: Codex runtime runner design | [docs/superpowers/specs/2026-05-15-product-agent-os-codex-runtime-runner-design.md](../superpowers/specs/2026-05-15-product-agent-os-codex-runtime-runner-design.md) | Source for Codex App, CLI, IDE extension and skills/subagents runtime boundary, result packet and no separate API app. |
| 11 | Track 5: Codex runtime runner plan | `docs/superpowers/plans/2026-05-15-product-agent-os-codex-runtime-runner.md` | Implementation slices for dependency-free runner, lifecycle routing, approval/source/redaction guards and CLI wrappers. |
| 12 | Track 6/7 implementation state | [docs/product-agent-os/technical.md](../product-agent-os/technical.md) | Product-Agent OS technical map records generated templates, renderer behavior and later Track 6/7 artifact expansion. |
| 13 | Track 6/7 standards guidance | [docs/product-agent-os/development-standards.md](../product-agent-os/development-standards.md) | User-facing engineering standards layer that may need final Task 22 sync after Track 9 methodology intelligence. |
| 14 | Track 6/7 methodology research log | [docs/sources/development-methodology-research-log.md](development-methodology-research-log.md) | Research history for methodology/tooling decisions before Track 8; useful for missing methodology gates and false-positive risks. |
| 15 | Track 6/7 gap matrix | [docs/sources/development-methodology-gap-matrix.md](development-methodology-gap-matrix.md) | Source claim to plugin artifact to eval/check map; likely source of Task 22 docs/eval closure gaps. |
| 16 | Final pre-development review | [docs/sources/product-agent-os-final-predevelopment-review.md](product-agent-os-final-predevelopment-review.md) | Product/technical critique that shaped Track 8; should be checked for unresolved risks still relevant after Track 9. |
| 17 | Track 8 detailed backlog as transition artifact | [docs/sources/product-agent-os-track-8-detailed-backlog.md](product-agent-os-track-8-detailed-backlog.md) | Not a pre-Track 8 implementation artifact, but required to understand how Track 6/7 findings became Track 8 scenario/eval work. |

## Track 6/7 generated artifact files to inspect when needed

Track 6 and Track 7 do not have dedicated checked-in `docs/superpowers/plans/*track-6*` or `docs/superpowers/specs/*track-7*` files. Their implementation is distributed across docs, packaged templates, discovery/readiness behavior and evals. When the primary analysis queue reaches Track 6/7, inspect these generated template sources as implementation evidence:

| Area | Source file |
| --- | --- |
| Workflow standards | `plugins/product-agent-os/assets/templates/workflows/development-standards.md` |
| Documentation system workflow | `plugins/product-agent-os/assets/templates/workflows/documentation-system.md` |
| ADR template | `plugins/product-agent-os/assets/templates/artifact-templates/adr.md` |
| Architecture overview template | `plugins/product-agent-os/assets/templates/artifact-templates/architecture-overview.md` |
| Domain modeling template | `plugins/product-agent-os/assets/templates/artifact-templates/domain-modeling.md` |
| Metric spec template | `plugins/product-agent-os/assets/templates/artifact-templates/metric-spec.md` |
| API contract review template | `plugins/product-agent-os/assets/templates/artifact-templates/api-contract-review.md` |
| Component card template | `plugins/product-agent-os/assets/templates/artifact-templates/component-card.md` |
| Database dictionary template | `plugins/product-agent-os/assets/templates/artifact-templates/database-dictionary.md` |
| Docs tooling decision template | `plugins/product-agent-os/assets/templates/artifact-templates/docs-tooling-decision.md` |

## Task 22 extraction contract

For each source file in the queue, produce a concise analysis packet before editing the `Task 22` matrix:

| Field | Required output |
| --- | --- |
| `source_file` | Exact path and role of the file in Product-Agent OS history. |
| `product_capability` | What user-facing capability this file enabled for real projects. |
| `technical_contracts` | Runtime, artifact, safety, ownership, verification or compatibility contracts that must survive final docs sync. |
| `implemented_surface` | Scripts, templates, skills, docs, tests or evals that already implement the contract. |
| `missing_task_22_sync` | What is not yet represented in Task 22 final docs sync, Track 8 bridge, Track 9 docs, eval docs, README, source registry or control-plane templates. |
| `false_positive_or_overreach_risk` | Where docs could force too much process, resurrect rejected runtime paths, or claim unverified capability. |
| `candidate_task_rows` | Concrete `T22-*` row candidates with acceptance criteria and verification commands. |
