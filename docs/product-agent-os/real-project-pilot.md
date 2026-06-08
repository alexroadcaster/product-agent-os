# Real-project pilot

Source status: `official + experiment`

## Назначение

Эта страница описывает безопасный первый pilot Product-Agent OS на реальном проекте. Она нужна оператору, который хочет проверить ценность plugin без чтения внутренних ledgers и без неявных изменений в целевой workspace.

Pilot по умолчанию является read-only и staged-first. Он помогает получить first-run operator packet, target consent matrix, success metrics и evidence ledger. Он не запускает live server, browser automation, provider/API calls, canonical graph mutation, external writes или git stage/commit/push/PR без отдельного explicit approval.

## First-Run Operator Packet

Стартовый prompt:

```text
Use Product-Agent OS for this project. Run a read-only first-run audit and return lifecycle state, usage_mode, risk map, methodology route, staged artifacts, verification route, approval boundary, rollback or remove path, evidence gaps and safe_next_action. Do not write files, start servers, call providers, run browser automation, mutate canonical sources or use git actions.
```

Ожидаемый first response:

| Field | Что должно быть в ответе |
| --- | --- |
| `lifecycle_state` | Текущий этап: intake, requirements, planning, build, review, release или learning. |
| `usage_mode` | Ближайший сценарий: web/frontend, backend/API, docs-only, AI/RAG, data/migration, PR/review или automation/release. |
| `source_boundary` | Какие файлы являются source of truth, какие generated views являются только orientation evidence. |
| `staged_artifact_route` | Какие artifacts предлагаются и куда они будут staged до target write. |
| `verification_route` | Команды, evals, runtime checks или owner review, которые докажут следующий шаг. |
| `approval_boundary` | Какие действия требуют отдельного approval. |
| `rollback_remove_path` | Как удалить staged outputs и вернуться к исходному состоянию. |
| `safe_next_action` | Один следующий шаг, который не перепрыгивает approvals. |

Staged artifact route должен использовать относительные project-scoped destinations, например `.codex/product-agent-os/pilots/<pilot-id>/`, `.codex/artifact-templates/` или proposed control-plane files. Absolute user-specific paths, secrets, raw private prompts, credentials, customer data and unredacted logs не допускаются.

## Target Consent Matrix

Перед pilot нужно выбрать target class и consent boundary.

| Archetype | Owner | Target class | Data policy | Allowed commands | Blocked commands | Evidence destination | Stop condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| web/frontend | Product owner + UI owner | non-production repo or clean worktree | no production data, no secrets, screenshots redacted | read-only inventory, tests already approved by owner | live server and browser automation without separate approval | `.codex/product-agent-os/pilots/web-frontend/` | UI/runtime action requested without approval |
| backend/API | Backend owner + security reviewer | non-production service repo | sanitized configs only, no credentials | read-only source/test/docs inventory | migrations, network calls, provider calls, production access | `.codex/product-agent-os/pilots/backend-api/` | auth, secrets or production data needed |
| docs-only | Docs owner | docs repo or docs folder | public or internal docs only | docs inventory, link/source-status checks | external publishing or canonical source rewrite without approval | `.codex/product-agent-os/pilots/docs-only/` | source-of-truth ambiguity remains unresolved |
| AI/RAG | AI owner + data owner | redacted evaluation workspace | approved corpus only, no private raw prompts | eval inventory, retrieval artifact review | live model/API calls, embedding generation, cache writes | `.codex/product-agent-os/pilots/ai-rag/` | provider or private corpus access requested |
| data/migration | Data owner + release owner | synthetic or staging dataset | synthetic fixtures or approved redacted data | schema/docs inventory and dry-run plan review | production writes, destructive migration, external export | `.codex/product-agent-os/pilots/data-migration/` | rollback or backup path missing |
| PR/review | Engineering owner | existing branch or PR diff | diff-only, no unrelated files | read-only review, test command proposal | staging, commit, push or PR mutation | `.codex/product-agent-os/pilots/pr-review/` | unrelated dirty changes block scope |
| automation/release | Release owner + security reviewer | staging workflow definition | no credentials, least privilege | automation candidate review, release packet draft | active schedule, GitHub Actions enablement, deploy, publish | `.codex/product-agent-os/pilots/automation-release/` | irreversible external action requested |

Owner consent must name owner, target class, data policy, allowed commands, blocked commands, evidence destination and stop condition. A pilot target is not approved by being listed in this matrix; the owner still approves the exact run.

## Success Criteria And Metrics

Pilot success is measured with reviewable criteria rather than a single score.

| Metric | Passing signal | Counter-metric |
| --- | --- | --- |
| `time_to_first_route` | Operator receives lifecycle state, risk map and safe next action quickly enough for the project context. | Fast answer that misses approval or data policy boundaries fails. |
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

## What Not To Expect

- No automatic installation, publication or plugin-cache refresh.
- No production data access.
- No live server launch.
- No browser automation.
- No provider/API calls.
- No canonical graph mutation.
- No external writes or active automation.
- No git stage/commit/push/PR.

## Verification

For docs-only pilot design changes, use docs contract tests, documentation structure checks, strict MkDocs when navigation/search/sitemap changes and diff hygiene. For any future real pilot execution, add target-specific command evidence, owner approval, rollback proof and redaction review before claiming readiness.

## Next Action

Use the first-run operator packet, then choose one pilot archetype and prepare a target-specific approval packet. The safe default remains read-only inventory plus staged artifacts.
