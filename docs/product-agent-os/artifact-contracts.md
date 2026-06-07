# Product-Agent OS artifact contracts

Source status: `official + experiment`

Эта страница перечисляет основные generated artifacts Product-Agent OS для modernization loop, project code graph, live/runtime governance и approval-bound handoff. Это не JSON Schema spec, а operator-facing contract map: что создается, зачем нужно, где проходит source-of-truth boundary и какие approval gates действуют.

## Contract Boundary

Сгенерированные артефакты являются только staged evidence. Они не являются источником истины, пока более поздний owner-approved process явно не продвинет факт обратно в checked-in source documentation или другой canonical artifact.

Каноническими источниками остаются:

- project source files и checked-in contracts;
- `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- source registry entries с текущий verification status;
- command evidence из текущий run;
- owner decisions и accepted gaps с residual risk.

Artifacts должен не contain secrets, credentials, raw private chat logs, private customer data, unredacted PII, raw source bodies где redacted packet является required, или absolute local paths.

## Project Code Graph Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph.json` | `project_code_graph.py`, `scan_project_code_graph.py --stage` | Main graph packet с metadata, nodes, edges, observations, freshness и provenance. | Orientation evidence only; source files остаются canonical. |
| `.codex/product-agent-os/project-code-graph.jsonl` | `scan_project_code_graph.py --stage` | Bounded JSONL form для agent consumption. | Нет raw source body claim; используйте source reads до implementation claims. |
| `.codex/product-agent-os/project-cockpit.html` | `project_graph_renderer.py` | Offline generated cockpit view. | Generated view only; visual completeness не доказывает source correctness. |
| `.codex/product-agent-os/project-cockpit.json` | `project_graph_renderer.py` | Structured cockpit model, pages и projection data. | Только review surface. |
| `.codex/product-agent-os/project-code-graph-search-index.json` | `project_graph_index.py`, `--build-index` | Offline static search index с cache/fingerprint checks. | Generated cache; delete для rollback. |
| `.codex/product-agent-os/project-code-graph-backend.json` | `project_graph_backend.py`, `--build-backend` | Disabled-by-default local query backend file-store. | Не active production server; graph-only fallback должен оставаться включенным. |
| `.codex/product-agent-os/project-code-graph-semantic-index.json` | `project_graph_semantic.py`, `--build-semantic-index` | Local deterministic semantic retrieval cache. | Semantic hits являются `present_unverified`; нет canonical edge rewrites. |
| `.codex/product-agent-os/project-code-graph-llm-proposals.json` | `project_graph_llm_extraction.py`, `--build-llm-proposals` | Local deterministic semantic node/edge и rationale/comment proposals. | Proposal-only; never canonical graph fact. |
| `.codex/product-agent-os/project-code-graph-extension-closure.json` | `project_graph_extension_closure.py`, `--verify-extensions` | Extension verification, rollback/data deletion proof и graph-only fallback report. | Closure evidence only. |

## Live Governance And Runtime Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-live-governance.json` | `project_graph_live_governance.py`, `--validate-live-governance` | Approval, data classification, redaction, credential, cache и budget packet. | Нет live calls; проверяется только gate. |
| `.codex/product-agent-os/project-code-graph-live-cache.json` | `project_graph_live_governance.py` | Cache policy/deletion metadata. | Cache является generated evidence, не source truth. |
| `.codex/product-agent-os/project-code-graph-live-runtime.json` | `project_graph_live_runtime.py`, `--validate-live-runtime` | Local read-only runtime contract. | `disabled_by_default_not_started`; нет launch в docs slices. |
| `.codex/product-agent-os/project-code-graph-live-runtime.pid` | `project_graph_live_runtime.py` | Runtime lifecycle placeholder/evidence path. | Имеет смысл только после approved runtime execution. |
| `.codex/product-agent-os/project-code-graph-live-runtime.log` | `project_graph_live_runtime.py` | Runtime log path/evidence path. | Must быть redacted и local-only. |

## Provider And Retrieval Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-embedding-provider.json` | `project_graph_embedding_provider.py`, `--validate-embedding-provider` | Embedding provider gate и eval baseline. | Provider call остается blocked пока separately approved. |
| `.codex/product-agent-os/project-code-graph-embedding-provider-cache.json` | `project_graph_embedding_provider.py` | Provider cache metadata. | Must preserve redaction/cache/budget policy. |
| `.codex/product-agent-os/project-code-graph-reranker-provider.json` | `project_graph_reranker_provider.py`, `--validate-reranker-provider` | Reranker provider gate. | Нет external reranker call через default. |
| `.codex/product-agent-os/project-code-graph-reranker-provider-cache.json` | `project_graph_reranker_provider.py` | Reranker cache metadata. | Generated cache only. |
| `.codex/product-agent-os/project-code-graph-hybrid-retrieval.json` | `project_graph_hybrid_retrieval.py`, `--build-hybrid-retrieval` | Explainable fusion из graph/static/semantic/reranker signals. | Нет canonical mutation; fallback остается available. |
| `.codex/product-agent-os/project-code-graph-llm-proposal-provider.json` | `project_graph_llm_proposal_provider.py`, `--validate-llm-proposal-provider` | External LLM proposal provider gate. | Proposal-only; provider output является не canonical. |
| `.codex/product-agent-os/project-code-graph-llm-proposal-eval.json` | `project_graph_llm_proposal_provider.py` | Safety/grounding eval packet для proposal provider. | Unsafe output routes к incident/fallback. |

## Review And Mutation Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-review-ledger.json` | `project_graph_review_ledger.py`, `--build-review-ledger` | Human review decisions: `accepted`, `rejected`, `accepted_gap`. | Нет accepted proposal без owner decision и evidence refs. |
| `.codex/product-agent-os/project-code-graph-proposal-diff.json` | `project_graph_review_ledger.py` | Proposal diff preview. | Preview только пока mutation dry-run. |
| `.codex/product-agent-os/project-code-graph-mutation-plan.json` | `project_graph_canonical_mutation.py`, `--build-canonical-mutation` | Mutation dry-run plan. | Staged plan only; не source mutation через itself. |
| `.codex/product-agent-os/project-code-graph-mutation-journal.jsonl` | `project_graph_canonical_mutation.py` | Append-only mutation journal. | Must cite accepted item и rollback path. |
| `.codex/product-agent-os/project-code-graph-canonical-mutated.json` | `project_graph_canonical_mutation.py` | Staged mutated graph copy. | Generated copy only; canonical graph/source не silently changed. |
| `.codex/product-agent-os/project-code-graph-rollback-proof.json` | `project_graph_canonical_mutation.py` | Rollback proof и digest comparison. | Required до mutation pilot completion claims. |

## Audit, Security And Observability Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-live-audit-log.jsonl` | `project_graph_live_audit.py`, `--build-live-audit` | Redacted append-only audit events. | Нет secrets, raw source или private data. |
| `.codex/product-agent-os/project-code-graph-live-security-privacy.json` | `project_graph_live_audit.py` | Security/privacy negative cases и findings. | Evidence packet, не full security certification. |
| `.codex/product-agent-os/project-code-graph-live-observability.json` | `project_graph_live_audit.py` | Runtime health, latency, provider error и degraded-mode visibility. | Generated observability evidence. |
| `.codex/product-agent-os/project-code-graph-agent-skill-handoff.json` | `project_graph_live_audit.py` | Agent/skill ownership, fresh context, verification и stop-condition routing. | Handoff guidance only; agents still нужны explicit work context. |

## Real Testing And Runtime QA Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/product-agent-os/project-code-graph-real-testing-readiness.json` | `project_graph_real_testing.py`, `--build-real-testing-readiness` | Readiness и no-hidden-gates packet. | Real testing остается blocked без target/data approval. |
| `.codex/product-agent-os/project-code-graph-real-testing-targets.json` | `project_graph_real_testing.py` | Owner-approved target/data-policy candidates. | Target consent evidence only. |
| `.codex/product-agent-os/project-code-graph-pilot-harness.json` | `project_graph_real_testing.py` | Dry-run pilot harness. | Stage-only; нет live execution. |
| `.codex/product-agent-os/project-code-graph-codex-surface-smoke.json` | `project_graph_real_testing.py` | Codex App, CLI и IDE extension smoke planning/evidence. | Does не imply live browser automation. |
| `.codex/product-agent-os/project-code-graph-real-testing-pilot-matrix.json` | `project_graph_real_testing.py` | Use-case pilot matrix. | Planning/readiness evidence. |
| `.codex/product-agent-os/project-code-graph-runtime-browser-qa.json` | `project_graph_runtime_qa.py`, `--build-runtime-qa` | Browser QA expectations/evidence. | Нет unapproved browser automation; labels и source boundary required. |
| `.codex/product-agent-os/project-code-graph-performance-budget.json` | `project_graph_runtime_qa.py` | Performance thresholds и fallback/accepted-gap handling. | Budget breach disables live layer или records owner gap. |
| `.codex/product-agent-os/project-code-graph-stabilization-ledger.json` | `project_graph_runtime_qa.py` | Stabilization defects и P0/P1 closure status. | Нет open P0/P1 до closure. |

## Agent/Skill Metrics Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| `.codex/eval-reports/agent-skill-evaluation-report.html` | `agent_skill_metrics_report.py` | Offline report view для `agent_skill_metrics_loop`. | Report является не proof; candidate-only. |
| `.codex/artifact-templates/agent-skill-scorecard-ledger.md` | Template registry | Append-only scorecard ledger template. | Must cite текущий evidence window. |
| `.codex/artifact-templates/agent-skill-daily-eval-report.md` | Template registry | Daily triage packet. | Нет active schedule через default. |
| `.codex/artifact-templates/agent-skill-weekly-verification.md` | Template registry | Weekly owner-review packet. | Requires rollback/holdout/flake/cost evidence или accepted gaps. |
| `.codex/artifact-templates/agent-skill-update-candidate.md` | Template registry | Modernization candidate packet. | Нет self-applied updates. |

## System File Hygiene Artifacts

| Artifact | Producer | Contract role | Boundary |
| --- | --- | --- | --- |
| JSON-вывод `validate_system_file_hygiene.py` | `system_file_hygiene.py` | Read-only inventory и findings по поддерживаемым классам системных файлов. | `schedule_status: not_created`; без edits, schedules, hooks и external-write. |
| `.codex/workflows/system-file-hygiene-audit.md` | Template registry | Operator workflow для hybrid periodic, on-change, size и release/automation triggers. | Только recommendation до owner approval на реальный schedule. |
| `.codex/artifact-templates/system-file-hygiene-report.md` | Template registry | Staged report для size, duplication, mojibake/BOM, secret, historical-ledger и ownership findings. | Только review artifact; compaction остается отдельным slice. |
| `.codex/automation-candidates/system-file-hygiene-audit.md` | Template registry | Candidate-only automation packet для будущих scheduled hygiene checks. | Active schedules остаются out of scope до explicit approval и rollback/disable evidence. |

JSON-валидатор `system_file_hygiene_audit` проверяет вложенную форму trigger records, class records, inventory, findings и `summary.status`; malformed packet блокируется до compaction или automation promotion.

Поля JSON для `system_file_hygiene_audit`: `audit_trigger`, `finding_type`, `compaction_decision`, `approval_boundary`, `no_secrets_status` и `active_schedule_markers`. CLI `--trigger` записывает причину запуска без записи в рабочую область. Шаблон `system-file-hygiene-report.md` фиксирует audit trigger, класс системного файла, тип finding, владельца, решение о compaction, active schedule markers, no-secrets status и границу отдельного approved slice.

## Planned Execution Evidence Files

| Planned artifact | Surface | Status до approval |
| --- | --- | --- |
| `live-server-run-evidence.json` | `approved_local_runtime_launch` | Planned only; требует local runtime approval packet. |
| `browser-automation-smoke.json` | `actual_browser_automation_smoke` | Planned only; требует browser automation approval packet. |
| `provider-call-evidence.json` | `approved_provider_api_pilot` | Planned only; provider call blocked пока approval/redaction/cache/budget/eval threshold exists. |
| `canonical-mutation-run.json` | `approved_canonical_mutation_pilot` | Planned only; требует accepted ledger item, dry-run plan, journal и rollback proof. |
| `git-release-pr-evidence.md` | `explicit_git_release_pr_action` | Planned only; нет git stage/commit/push/PR без explicit пользователь command. |

## Проверка

Artifact verification следует check:

- expected `artifact_kind` и `approval_boundary`;
- stage root confinement и rollback/disable path;
- redaction из secrets, raw source bodies, absolute paths и private data;
- generated-view или staged-evidence label;
- source-boundary label когда screenshots, cockpit, dashboard или runtime QA evidence является present;
- fallback path когда live/provider/runtime layers являются disabled;
- `schedule_status: not_created` для system file hygiene outputs, пока approved automation slice не зафиксировал другое;
- текущий command evidence до readiness, works, complete или release claims.

## Риски And Failure Modes

- A generated HTML/JSON view может быть mistaken для source truth.
- Stale graph fingerprints или caches может make old source look current.
- Provider artifacts может leak private data если redaction/cache/budget gates являются skipped.
- Review ledger decisions являются invalid без owner и evidence refs.
- Mutation artifacts являются unsafe без rollback proof.
- Planned artifact names может быть mistaken для executed evidence.

## Next Action

Используйте эта contract map когда writing docs tests, source registry entries и packaging/closure checks. Navigation и generated `site/` refresh являются intentionally handled после source docs packet является stable.
