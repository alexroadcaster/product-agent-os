# Real-Project Pilot

Source status: `official + experiment`

## Purpose

This page describes a safe first Product-Agent OS pilot on a real project. It is for an operator who wants to validate plugin value without reading internal ledgers and without hidden changes in the target workspace.

The pilot is read-only and staged-first by default. It produces a first-run operator packet, target consent matrix, success metrics and evidence ledger. It does not launch a live server, run browser automation, call providers or APIs, mutate canonical graph sources, perform external writes or run git stage/commit/push/PR without separate explicit approval.

## First-Run Operator Packet

Starting prompt:

```text
Use Product-Agent OS for this project. Run a read-only first-run audit and return lifecycle state, usage_mode, risk map, methodology route, staged artifacts, verification route, approval boundary, rollback or remove path, evidence gaps and safe_next_action. Do not write files, start servers, call providers, run browser automation, mutate canonical sources or use git actions.
```

Expected first response:

| Field | Required content |
| --- | --- |
| `lifecycle_state` | Current stage: intake, requirements, planning, build, review, release or learning. |
| `usage_mode` | Nearest scenario: web/frontend, backend/API, docs-only, AI/RAG, data/migration, PR/review or automation/release. |
| `source_boundary` | Which files are source of truth and which generated views are orientation evidence only. |
| `staged_artifact_route` | Which artifacts are proposed and where they will be staged before target writes. |
| `verification_route` | Commands, evals, runtime checks or owner review that will prove the next step. |
| `approval_boundary` | Which actions require separate approval. |
| `rollback_remove_path` | How to remove staged outputs and return to the previous state. |
| `safe_next_action` | One next step that does not cross approvals. |

The staged artifact route should use relative project-scoped destinations such as `.codex/product-agent-os/pilots/<pilot-id>/`, `.codex/artifact-templates/` or proposed control-plane files. Absolute user-specific paths, secrets, raw private prompts, credentials, customer data and unredacted logs are not allowed.

## Target Consent Matrix

Before the pilot, choose a target class and consent boundary.

| Archetype | Owner | Target class | Data policy | Allowed commands | Blocked commands | Evidence destination | Stop condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| web/frontend | Product owner + UI owner | non-production repo or clean worktree | no production data, no secrets, screenshots redacted | read-only inventory, tests already approved by owner | live server and browser automation without separate approval | `.codex/product-agent-os/pilots/web-frontend/` | UI/runtime action requested without approval |
| backend/API | Backend owner + security reviewer | non-production service repo | sanitized configs only, no credentials | read-only source/test/docs inventory | migrations, network calls, provider calls, production access | `.codex/product-agent-os/pilots/backend-api/` | auth, secrets or production data needed |
| docs-only | Docs owner | docs repo or docs folder | public or internal docs only | docs inventory, link/source-status checks | external publishing or canonical source rewrite without approval | `.codex/product-agent-os/pilots/docs-only/` | source-of-truth ambiguity remains unresolved |
| AI/RAG | AI owner + data owner | redacted evaluation workspace | approved corpus only, no private raw prompts | eval inventory, retrieval artifact review | live model/API calls, embedding generation, cache writes | `.codex/product-agent-os/pilots/ai-rag/` | provider or private corpus access requested |
| data/migration | Data owner + release owner | synthetic or staging dataset | synthetic fixtures or approved redacted data | schema/docs inventory and dry-run plan review | production writes, destructive migration, external export | `.codex/product-agent-os/pilots/data-migration/` | rollback or backup path missing |
| PR/review | Engineering owner | existing branch or PR diff | diff-only, no unrelated files | read-only review, test command proposal | staging, commit, push or PR mutation | `.codex/product-agent-os/pilots/pr-review/` | unrelated dirty changes block scope |
| automation/release | Release owner + security reviewer | staging workflow definition | no credentials, least privilege | automation candidate review, release packet draft | active schedule, GitHub Actions enablement, deploy, publish | `.codex/product-agent-os/pilots/automation-release/` | irreversible external action requested |

Owner consent must name owner, target class, data policy, allowed commands, blocked commands, evidence destination and stop condition. A pilot target is not approved just because it appears in this matrix; the owner still approves the exact run.

## Success Criteria And Metrics

Pilot success is measured with reviewable criteria rather than a single score.

| Metric | Passing signal | Counter-metric |
| --- | --- | --- |
| `time_to_first_route` | The operator receives lifecycle state, risk map and safe next action quickly enough for the project context. | A fast answer that misses approval or data policy boundaries fails. |
| `route_accuracy` | Suggested route matches repo type, current lifecycle and owner intent. | Generic methodology lecture or wrong runtime route fails. |
| `artifact_usefulness` | Proposed artifacts are few, reviewable and tied to source files or verification. | Artifact sprawl or internal ledger dumping fails. |
| `methodology_selection_precision` | DDD, TDD, eval, architecture or release gates appear only when relevant. | Methodology forced without project evidence fails. |
| `owner_question_usefulness` | Questions are few, blocking and tied to a decision the owner can make. | Broad intake questionnaire fails. |
| `false_positive_rate` | Generated claims are marked source-backed, proposal, accepted gap or unsupported. | Generated views treated as source of truth fail. |
| `evidence_sufficiency` | Each readiness claim names command evidence, source evidence or owner review. | Completion claim without fresh evidence fails. |

Accepted-gap rules: each gap needs owner, reason, reduced evidence path, residual risk, follow-up condition and review date. An accepted gap cannot authorize a live server, browser automation, provider call, canonical mutation, external write or git action.

## Pilot Harness And Evidence Ledger

The harness is a dry-run plan, not active automation.

Required ledger fields:

| Field | Required content |
| --- | --- |
| `pilot_id` | Stable id for the pilot run. |
| `target_class` | Archetype and target class from the consent matrix. |
| `read_only_pilot_commands` | Commands that only inspect source, docs, tests, config or generated staged outputs. |
| `staged_output_locations` | Relative destinations for proposed artifacts and evidence. |
| `runlog_evidence_schema` | Time, command, exit code, files inspected, files proposed, approvals checked, residual risks and next action. |
| `screenshot_log_redaction` | Rule for redacting screenshots, logs and console output when visual/runtime evidence is separately approved. |
| `cleanup_steps` | How staged outputs, generated caches and pilot evidence can be removed. |
| `approval_checks` | Confirmation that no approval-bound action is performed by default. |

The harness must not become active automation, a live server launcher, a provider gateway, a browser runner, a canonical graph writer, an external writer or a git release tool. It may propose those actions only as separate approval packets.

## Rollback And Cache Recovery Procedure

Before a production pilot, the operator needs a clear rollback/remove path for the plugin and local cache. This procedure does not approve deletion, cache mutation, global config mutation, hook activation/deactivation, automation, publication or git actions. It names what must be confirmed before a separate owner approval.

| Step | Required boundary |
| --- | --- |
| `pre_rollback_read_only_inspection` | Inspect the installed plugin cache path, package name/version, expected file count, skill count, manifest, `.mcp.json`, backup path, staged source digest and active hook/automation status. |
| `rollback_evidence_preservation` | Preserve approval text, inspected paths, before/after counts, command transcript, backup pointer, moved-aside path and residual risks in the staged evidence destination. |
| `installed_plugin_remove_path` | Any remove action uses move-aside/quarantine for the exact approved version path only; silent delete is not allowed. |
| `stale_cache_restore_path` | Restore only from a named backup tied to evidence; after restore, verify file count, skill count and manifest status. |
| `cache_clear_recovery_path` | Cache clear/replace is allowed only for the exact cache root and version id; the path must be resolved and checked before any write. |
| `disable_hooks_automations_if_ever_approved` | If hooks or automations were ever activated, the disable path must name the exact surface, owner, command boundary, evidence target and rollback owner. |
| `post_restore_verification` | After an approved mutation, run cache inspection, Codex compatibility smoke, docs/test checks when docs changed, diff hygiene and record residual risks. |

Stop immediately on missing owner approval, unresolved path outside the approved cache root, missing backup, digest/count mismatch, destructive delete request, active automation without owner, secret/customer data in evidence, external write request, provider/API call, live server/browser request, canonical mutation or git stage/commit/push/PR request.

## What Not To Expect

- No automatic installation, publication or plugin-cache refresh.
- No production data access.
- No live server launch.
- No browser automation.
- No provider/API calls.
- No canonical graph mutation.
- No external writes or active automation.
- No git stage/commit/push/PR.

## Target-Specific Pilot Evidence

The first owner-approved docs-only pilot addendum `B38-PILOT-NF01` ran read-only on target label `Neural_Flow`. Durable docs do not store the absolute user-specific target path; evidence is recorded as workspace-local staged output.

| Field | Evidence |
| --- | --- |
| `target_class` | docs-only / legacy onboarding |
| `staged_evidence_root` | `tmp/neural-flow-product-agent-os-pilot-20260608-191510` |
| `usage_mode` | `legacy_onboarding` after a clean docs-only intent |
| `complexity_profile` | `guided-small` |
| `source_policy_status` | `blocked` |
| `staged_outputs` | infrastructure, status dashboard and project graph validated outside the target |
| `target_apply_status` | blocked until target source-policy/control-plane cleanup |
| `target_workspace_mutation_performed` | false |

What this proves: after the local cache refresh, Product-Agent OS can run read-only discovery, methodology audit, runtime routing, staged artifact rendering and static content checks on a real docs-only target. What it does not prove: production readiness, public/team release readiness, target apply safety or product success. The next safe target step is to add or accept gaps for `Source status`, source registry/control-plane ownership and the smallest local verification contract inside the target.

## Verification

For docs-only pilot design changes, use docs contract tests, documentation structure checks, strict MkDocs when navigation/search/sitemap changes and diff hygiene. For any future real pilot execution, add target-specific command evidence, owner approval, rollback proof and redaction review before claiming readiness.

## Next Action

Use the first-run operator packet, then choose one pilot archetype and prepare a target-specific approval packet. The safe default remains read-only inventory plus staged artifacts.
