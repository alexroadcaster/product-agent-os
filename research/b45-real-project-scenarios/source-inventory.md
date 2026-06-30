# B45-PCA-M29 Source Inventory

Source status: project-authored read-only inventory. Evidence is based on current local filesystem inspection on 2026-06-30. This artifact stores relative paths and metadata only; it does not copy target source bodies.

## Scope

`B45-PCA-M29` inspects approved real-project candidates and records:

- candidate tasks;
- relevant code and test files by relative path;
- available commands and dependency shape;
- privacy risks and exclusion rules;
- approval boundaries for future copy, run, refactor, browser, runtime, provider, and git work.

No target code was modified. No target commands that build, test, launch, mutate, or call external services were run.

## Approval And Reproducibility Notes

Target-selection provenance: the target labels were named by the owner in the current B45-PCA thread for read-only inventory. That approval is limited to metadata inspection and does not authorize source-body copying, target command execution, runtime launches, browser automation, provider/API calls, git writes, deployment, publication, or automation.

Owned-source counts use `rg --files` with recursive exclusions such as `!**/node_modules/**`, not only folder-name globs. Hidden/ignored risk discovery used `rg --files --hidden --no-ignore` only to identify path-level denylist surfaces. No raw source bodies, matched secret values, raw prompts, raw messages, or payload bodies were captured.

The 2026-06-30 repeat pass also used two independent subagent reviews: one architecture coverage review and one privacy/evidence review. Both were read-only.

## Global Exclusion Rules

| Exclusion | Reason |
| --- | --- |
| `.git`, nested `.git`, worktrees | Git metadata and branch state are not scenario fixtures. |
| `**/node_modules/**`, `**/.next/**`, `**/dist/**`, `**/build/**`, `**/site/**`, `**/coverage/**`, cache folders | Generated or dependency material; too noisy and not owned source. |
| `.env`, `*.env`, `*.pem`, `*.key`, `*.p12`, `*.crt`, local DB files, sqlite WAL/SHM files, `.sol_data`, private logs | Potential secrets, credentials, private payloads, or local runtime state. |
| `.wrangler`, `.vercel`, `.turbo`, `.vite`, `.cache`, `.ruff_cache`, `.mypy_cache`, `playwright-report`, `test-results`, traces, videos, screenshots, HAR files | Runtime, build, browser, or generated evidence state; not source fixture material. |
| Bundled vendor/example corpora | Excluded unless explicitly selected as the scenario itself. |
| Raw chat/message bodies, raw customer/user data, private API payloads | Not allowed in prompts, docs, evals, fixtures, or reports. |
| Live Worker/model/provider results | Approval-gated and outside M29. |

## Target: myPartners

### Read-Only Shape

| Area | Observed metadata |
| --- | --- |
| Source availability | available and inspected read-only |
| Filtered source count | 1149 files after recursive generated/dependency exclusions |
| Focused app count | 260 files under `server/app`, `frontend/src`, and `worker/src` |
| Main languages | Python, Markdown, TypeScript, TSX, JSON, SQL |
| Main app layers | FastAPI server, Next.js frontend, Cloudflare Worker, docs, scripts/tools |
| Existing repo state | target had pre-existing modified/untracked files; no changes were made |

### Rereview Root Counts

| Root | Count |
| --- | --- |
| `server/app` | 170 |
| `server/tests` | 181 |
| `frontend/src` | 61 |
| `frontend/tests` | 46 |
| `worker/src` | 29 |
| `worker/test` | 15 |
| `tools` | 139 |
| `docs` | 440 |

### Manifests And Commands

| Layer | Manifest | Relevant declared commands |
| --- | --- | --- |
| Server | `server/pyproject.toml` | pytest is configured through `testpaths = ["tests"]` and `addopts = "-v --tb=short"` |
| Frontend | `frontend/package.json`, `frontend/tsconfig.json` | `dev`, `build`, `lint`, `typecheck`, `test`, `test:launcher`, `test:e2e` |
| Worker | `worker/package.json`, `worker/tsconfig.json`, `worker/wrangler.toml` | `dev`, `dev:diagnostic-rag`, `deploy`, `deploy:diagnostic-rag`, `test`, `test:watch`, `typecheck` |
| Docs/tools | `docs/package.json`, `docs/requirements.txt`, `tools/rag_pipeline/pyproject.toml` | documentation/tooling commands exist but were not run for M29 |

### Candidate Area: CRM Chat And Contact Workflow

| Item | Relative paths |
| --- | --- |
| Backend route/domain | `server/app/api/contacts_routes.py`; `server/app/contacts/__init__.py`; `server/app/contacts/merge_candidates.py` |
| Backend tests | `server/tests/test_contacts_chats.py`; `server/tests/test_contacts_messages.py`; `server/tests/test_contacts_routes.py`; `server/tests/test_contacts_get_one.py`; `server/tests/test_contacts_insights.py`; `server/tests/test_contacts_list_extended.py`; `server/tests/test_contacts_merge.py`; `server/tests/test_contacts_patch.py`; `server/tests/test_contacts_tags_assoc.py` |
| Frontend tests/contracts | `frontend/tests/e2e/crm.spec.ts`; `frontend/tests/contracts/crm-api.test.ts`; `frontend/tests/contracts/crm-message-rendering.test.ts`; `frontend/tests/contracts/crm-model.test.ts` |
| Candidate scenario | `MP-CRM-CHAT-OPEN-01` |
| Why useful | Multi-layer workflow, existing tests, product behavior, and privacy-safe evidence challenge. |
| Approval boundary | Raw messages or local DB content must not be copied; browser/e2e/runtime execution requires exact approval. |

### Candidate Area: Relationship Graph And Sigma Workflow

| Item | Relative paths |
| --- | --- |
| Backend graph routes/domain | `server/app/api/graph_routes.py`; `server/app/graph/topics.py`; `server/app/graph/recomputer.py`; `server/app/graph/projection_lifecycle.py`; `server/app/graph/projection_jobs.py`; `server/app/graph/projection_cache.py`; `server/app/graph/projection_benchmark.py`; `server/app/graph/metrics.py`; `server/app/graph/engine.py`; `server/app/graph/edge_candidates.py` |
| Relationship signals | `server/app/api/relationship_signal_routes.py`; `server/app/relationship_signals/usefulness.py`; `server/app/relationship_signals/service.py`; `server/app/relationship_signals/scorer.py`; `server/app/relationship_signals/revisions.py` |
| Backend tests | `server/tests/test_graph_routes.py`; `server/tests/test_graph_edge_candidates.py`; `server/tests/test_relationship_signal_*` family |
| Frontend tests/contracts | `frontend/tests/e2e/sigma-graphology-payload-preview.spec.ts`; `frontend/tests/e2e/home-graph.spec.ts`; `frontend/tests/contracts/sigma-graphology-spike.test.ts`; `frontend/tests/contracts/sigma-graphology-payload-preview-source.test.ts`; `frontend/tests/contracts/sigma-graphology-layout.test.ts`; `frontend/tests/contracts/sigma-graphology-adapter.test.ts`; `frontend/tests/contracts/relationship-signal-lenses.test.ts`; `frontend/tests/contracts/home-graph-workspace-hydration.test.ts`; `frontend/tests/contracts/home-graph-engagement.test.ts`; `frontend/tests/contracts/graph-model.test.ts`; `frontend/tests/contracts/graph-api.test.ts` |
| Candidate scenario | `MP-REL-GRAPH-SIGMA-02` |
| Why useful | Tests architecture depth, entity relationships, visual/runtime split, and contract-vs-browser proof. |
| Approval boundary | Browser proof, screenshots, and runtime launches require exact approval. |

### Candidate Area: Advisor Local/Worker Boundary

| Item | Relative paths |
| --- | --- |
| Server API/domain | `server/app/api/advisor_routes.py`; `server/app/advisor/worker_inference_client.py`; `server/app/advisor/v2_eval_gates.py`; `server/app/advisor/status.py`; `server/app/advisor/scope_resolver.py`; `server/app/advisor/run_store.py`; `server/app/advisor/run_citations.py`; `server/app/advisor/run_budget.py`; `server/app/advisor/role_policy.py`; `server/app/advisor/prompt_composer.py`; `server/app/advisor/product_help_eval.py`; `server/app/advisor/network_context.py`; `server/app/advisor/intent_router.py` |
| Server tests | `server/tests/test_advisor_*` family |
| Worker code/test | `worker/src/handlers/advisor_infer.ts`; `worker/test/advisor_infer.test.ts` |
| Live eval tools | `tools/advisor_question_lens_live_eval.mjs`; `tools/advisor_live_worker_eval.mjs` |
| Candidate scenario | `MP-ADVISOR-BOUNDARY-03` |
| Why useful | Strong boundary test for local orchestration, inference-only Worker role, eval gates, and live-provider denial. |
| Approval boundary | Live Worker/provider/model calls are not permitted without exact approval. |

### Candidate Area: RAG, Semantic Retrieval, And Vector Readiness

| Item | Relative paths |
| --- | --- |
| Retrieval/domain | `server/app/rag/card_retrieval.py`; `server/app/rag/card_practice_graph.py`; `server/app/rag/sqlite_vec_semantic_index.py`; `server/app/rag/semantic_retrieval_scorecards.py`; `server/app/rag/semantic_index_port.py`; `server/app/rag/retrieval_router.py`; `server/app/rag/retrieval_readiness.py`; `server/app/rag/retrieval_eval.py`; `server/app/rag/retrieval_contract.py`; `server/app/rag/retrieval_audit.py`; `server/app/rag/message_retrieval.py`; `server/app/rag/local_embedding_comparison_harness.py`; `server/app/rag/eval_retrieval_metrics.py`; `server/app/rag/eval_relationship_signal_contracts.py` |
| Tests | `server/tests/test_rag_*`; `server/tests/test_sqlite_vec_semantic_index.py`; `server/tests/test_semantic_retrieval_*` |
| Decision docs | `docs/adr/0056-phase-14-semantic-index-port-and-vector-readiness.md` and related ADR/review docs |
| Candidate scenario | `MP-RAG-SEMANTIC-04` |
| Why useful | Deep AI/eval/retrieval scenario with architecture, data policy, fallback, and benchmark gates. |
| Approval boundary | Private DBs, raw message payloads, embeddings over private content, and live model/provider calls are approval-gated. |

### Deferred / Explicitly Excluded Scenario Families

| Deferred id | Signals | Reason |
| --- | --- | --- |
| `MP-SETTINGS-DIAG-OBS-DEFERRED` | `server/app/api/diagnostics_routes.py`; `server/app/api/settings_routes.py`; `frontend/src/features/settings/*`; diagnostics/settings tests | Real settings/observability surface, but not selected for first code-authoring pilot. |
| `MP-APPDATA-SELFCONTEXT-DEFERRED` | `server/app/operations/appdata_activation.py`; `server/app/operations/self_context_activation.py`; `server/app/operations/advisor_history_activation.py`; memory/history/appdata tests | High-risk data/state workflow; requires stricter approval and metadata-only fixture design. |
| `MP-BOOTSTRAP-AUTH-SYNC-DEFERRED` | `server/app/bootstrap/*`; `worker/src/auth.ts`; `worker/src/commercial_auth.ts`; `tools/spike_beeper/*`; auth/scheduler/config tests | Credentials, local state, and integration boundaries make this a later scenario. |
| `MP-WORKER-INSIGHTS-DEFERRED` | Worker handlers and insights surfaces | Needs separate edge/runtime/provider boundary handling. |

### Hidden/Ignored Risk Surfaces

| Risk class | Path metadata examples |
| --- | --- |
| Local/runtime databases | `server/mypartners_dev.db`; `.pytest-basetemp-*`; `.tmp/pytest-of-user/*`; `worker/test/.wrangler/state/*` |
| Logs and generated evidence | `debug.log`; `frontend/debug.log`; `docs/.npm-cache/_logs/*` |
| Binary/mockup assets | `docs/agents/mockups/*.png`; `docs/superpowers/*.png` |

## Target: SOL 0.6

### Read-Only Shape

| Area | Observed metadata |
| --- | --- |
| Source availability | available and inspected read-only |
| Filtered source count | 92 files after recursive generated/dependency/vendor exclusions |
| Focused app count | 49 files under `backend/src`, `frontend/src`, and `scripts` |
| Main languages | TypeScript, TSX, Python, JSON, CSS |
| Main app layers | Node/TypeScript backend, Next.js frontend, Python helper scripts |
| Git status | root is not a git repository; `frontend` contains a nested `.git` folder |

The earlier broad SOL count was inflated by nested `backend/node_modules`, generated `dist`, and vendor/example surfaces. The repeat pass supersedes it for fixture planning.

### Rereview Root Counts

| Root | Count |
| --- | --- |
| `backend/src` | 19 |
| `backend/test project` | 3 |
| `frontend/src` | 28 |
| `scripts` | 2 |
| `docs` | 21 |

### Manifests And Commands

| Layer | Manifest | Relevant declared commands |
| --- | --- | --- |
| Backend | `backend/package.json`, `backend/tsconfig.json` | `dev`, `build`, `start`, placeholder `test` that exits with failure |
| Frontend | `frontend/package.json`, `frontend/tsconfig.json` | `dev`, `build`, `start`, `lint` |
| Scripts | `scripts/auto_skill_loader.py`; `scripts/filter_offline_skills.py` | no command contract was confirmed in M29 |

### Candidate Area: Backend Agent Orchestration

| Item | Relative paths |
| --- | --- |
| Entry/services | `backend/src/index.ts`; `backend/src/services/ai.ts`; `backend/src/services/taskMaster.ts`; `backend/src/services/orchestrator.ts`; `backend/src/services/db.ts`; `backend/src/services/agent-registry.ts` |
| Tool dispatch | `backend/src/services/tools/dispatcher.ts`; `backend/src/services/tools/createSubtasksTool.ts` |
| Agent implementations | `backend/src/services/agents/developer-agent.ts`; `backend/src/services/agents/designer-agent.ts`; `backend/src/services/agents/data-analyst-agent.ts`; `backend/src/services/agents/ba-agent.ts`; `backend/src/services/agents/architect-agent.ts`; `backend/src/services/agents/optimizer-agent.ts`; `backend/src/services/agents/marketer-agent.ts`; `backend/src/services/agents/product-owner-agent.ts`; `backend/src/services/agents/qa-agent.ts`; `backend/src/services/agents/router-agent.ts`; `backend/src/services/agents/security-agent.ts` |
| Candidate scenario | `SOL-AGENT-ORCH-01` |
| Why useful | Compact but real multi-agent architecture for dependency analysis, refactor planning, and typed build comparison. |
| Approval boundary | `backend/.env`, `backend/sol.env`, `backend/.sol_data`, `dist`, and `node_modules` must stay excluded. |

### Candidate Area: Frontend Chat/Workspace UI

| Item | Relative paths |
| --- | --- |
| Stores/socket | `frontend/src/store/useAppStore.ts`; `frontend/src/store/useAgentStore.ts`; `frontend/src/lib/socket.ts`; `frontend/src/lib/utils.ts` |
| App/layout | `frontend/src/app/layout.tsx`; `frontend/src/app/page.tsx`; `frontend/src/app/globals.css`; `frontend/src/components/layout/sidebar.tsx`; `frontend/src/components/layout/main-layout.tsx` |
| Views | `frontend/src/components/views/projects-view.tsx`; `frontend/src/components/views/chat-view.tsx`; `frontend/src/components/views/tasks-view.tsx`; `frontend/src/components/views/team-view.tsx` |
| UI components | `frontend/src/components/ui/button.tsx`; `frontend/src/components/ui/card.tsx`; `frontend/src/components/ui/badge.tsx`; `frontend/src/components/ui/avatar.tsx`; `frontend/src/components/ui/input.tsx`; `frontend/src/components/ui/dialog.tsx`; `frontend/src/components/ui/label.tsx`; `frontend/src/components/ui/resizable.tsx`; `frontend/src/components/ui/scroll-area.tsx`; `frontend/src/components/ui/select.tsx`; `frontend/src/components/ui/textarea.tsx`; `frontend/src/components/ui/tabs.tsx`; `frontend/src/components/ui/sheet.tsx`; `frontend/src/components/ui/separator.tsx` |
| Candidate scenario | `SOL-FRONTEND-CHAT-02` |
| Why useful | Frontend component/store architecture with lint/build gates and no confirmed test suite. |
| Approval boundary | Browser/runtime proof requires exact approval; generated `.next`, logs, and nested git metadata stay excluded. |

### Candidate Area: Offline Skill Loader Scripts

| Item | Relative paths |
| --- | --- |
| Scripts | `scripts/filter_offline_skills.py`; `scripts/auto_skill_loader.py` |
| Candidate scenario | `SOL-SKILL-LOADER-03` |
| Why useful | Small Python scenario for command discovery, static analysis, and style/refactor evaluation. |
| Approval boundary | Do not load external registries or mutate skill/plugin folders without explicit approval. |

### Deferred / Explicitly Excluded Scenario Families

| Deferred id | Signals | Reason |
| --- | --- | --- |
| `SOL-DOCS-TASK-TRACE-DEFERRED` | `docs/Tasks/*`; `docs/prd.md`; `docs/architecture_diagram.md`; `docs/taskmaster_plan.md`; `backend/mytest2/*`; `backend/test project/*`; `tmp-ai-test.ts`; `sol-ide.json` | Useful for requirements/architecture traceability, but not selected as first-pass code fixture material. |

### Hidden/Ignored Risk Surfaces

| Risk class | Path metadata examples |
| --- | --- |
| Env/config secrets | `backend/.env`; `backend/sol.env` |
| Generated logs/evidence | `frontend/build_output.log` |
| Generated/dependency/vendor state | nested `node_modules`, `dist`, `.next`, nested `.git`, `antigravity-awesome-skills-main` |

## M29 Findings

| Finding | Impact |
| --- | --- |
| `myPartners` has richer existing tests and sharper privacy/runtime boundaries. | Best for validating whether Product-Agent OS can separate source evidence, runtime proof, eval proof, and approval gates. |
| `SOL 0.6` is smaller at the focused-app layer and has clearer build/lint entry points. | Best first target for low-risk architecture/refactor scenario design. |
| Both targets include generated/dependency/env surfaces. | Future copy steps need an explicit denylist and metadata-only policy. |
| Several high-value scenarios require browser/runtime/provider proof for full closure. | Later tasks must label those gates as approval-required unless exact approval is granted. |
| Repeat review found deferred families, not a failed M29 selection. | M29 is sufficient as selection layer; M30 must choose scope and run denylist checks before fixture copying. |
| Machine-readable denylist must match the human policy. | JSON and copy tooling must include logs, secrets, traces, browser artifacts, sqlite sidecars, and nested generated folders. |

## Recommended Next Actions

1. Select one scenario for `B45-PCA-M30` fixture policy and copy plan.
2. Build a redaction checklist before any target source body is copied.
3. Prefer `SOL-AGENT-ORCH-01` as the first low-risk module-through-run candidate.
4. Use `MP-CRM-CHAT-OPEN-01` or `MP-RAG-SEMANTIC-04` when testing privacy-safe evidence handling is the main goal.
5. Keep browser/runtime/provider/live Worker proof out of scope until a later approval names the exact command and rollback boundary.
6. Before M30/M31, rerun the recursive path-only denylist scan over the selected paths and store the exact copy scope.

M30 follow-up: `source-policy.md`, `scenario-manifest.schema.json`, `fixture-manifest.schema.json`, and `redaction-manifest.schema.json` now define the pre-copy contract. They do not approve or perform source-body copying.
