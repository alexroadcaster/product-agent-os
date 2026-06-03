# Product-Agent OS CLI reference

Source status: `official + experiment`

Эта страница фиксирует локальные Product-Agent OS CLI surfaces, которые уже есть в `plugins/product-agent-os/scripts/`. Она описывает команды как stage/read-only tooling: они не публикуют plugin, не запускают внешние системы и не выполняют live provider/model/API calls без отдельного explicit approval.

## Назначение

CLI слой нужен для повторяемого локального evidence loop:

- read-only audit или dry-run packet перед изменениями;
- stage-only generation в явный output directory;
- approval-bound merge или rollback только через отдельный approval record;
- deterministic runtime contract для Codex App, CLI или IDE extension;
- project graph generation, queries, generated cockpit, local indexes and provider/mutation governance packets;
- docs/closure verification через отдельные docs-maintainer и tester slices.

Generated outputs are not source of truth. Source of truth remains checked-in source files, project docs, source registry, control-plane artifacts, current command evidence and owner-approved records.

## Core Commands

| Command | Purpose | Required inputs | Output / boundary |
| --- | --- | --- | --- |
| `python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --dry-run` | Print an infrastructure render plan. | Target workspace path. | Read-only JSON/text plan; no staged files. |
| `python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --stage <stage-dir>` | Stage generated control-plane/templates. | Workspace and explicit stage directory. | Writes only under `<stage-dir>`; direct target merge remains separate. |
| `python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --plan` | Build a read-only merge plan. | Workspace and stage directory. | No writes to target workspace. |
| `python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --apply --approval-file <approval.json>` | Apply approved merge decisions. | Approval file matching the plan. | Approved target writes only; rollback manifest can be produced by merge tooling. |
| `python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --rollback <rollback.json>` | Roll back a prior approved merge. | Rollback manifest. | Restores scoped files from recorded rollback data. |
| `python plugins\product-agent-os\scripts\run_codex_runtime_runner.py <workspace> --contract` | Produce deterministic Codex runtime route packet. | Workspace. | Offline contract; no external model call. |
| `python plugins\product-agent-os\scripts\run_codex_runtime_runner.py <workspace> --contract --allow-subagents` | Allow route recommendations that mention subagents. | Workspace and explicit subagent permission in the current workflow. | Recommendation only; does not create agents by itself. |
| `python plugins\product-agent-os\scripts\render_status_dashboard.py <workspace> --dry-run` | Print status dashboard plan. | Workspace. | No write. |
| `python plugins\product-agent-os\scripts\render_status_dashboard.py <workspace> --stage <stage-dir>` | Stage generated status dashboard HTML/JSON. | Workspace and explicit stage directory. | Generated view only, not source of truth. |
| `python plugins\product-agent-os\scripts\render_agent_skill_metrics_report.py <workspace> --dry-run` | Print metrics report plan. | Workspace. | No write. |
| `python plugins\product-agent-os\scripts\render_agent_skill_metrics_report.py <workspace> --stage <stage-dir>` | Stage agent/skill metrics report. | Workspace and explicit stage directory. | Candidate-only report; no modernization is applied. |

Runtime runner optional inputs include `--approval-status`, `--intent-hint` and `--output`. They change the emitted route packet or save JSON; they do not bypass source policy, sandbox, approvals or external-action boundaries.

## Project Graph CLI

`scan_project_code_graph.py` has exactly-one-mode semantics. Choose one mode per invocation.

| Mode | Purpose | Required inputs | Output / boundary |
| --- | --- | --- | --- |
| `--dry-run` | Build graph packet without writing files. | `<workspace>`. | Prints graph JSON; no write. |
| `--stage <stage-dir>` | Stage graph and cockpit artifacts. | `<workspace>`, explicit stage directory. | Writes generated graph/cockpit files under stage root. |
| `--query <kind>` | Read bounded query packet from existing graph. | `--graph <project-code-graph.json>` plus query args. | Reads existing graph artifact; does not rescan source. |
| `--build-index` | Build offline static search index. | `--stage`, `--graph`. | Generated index cache; not source of truth. |
| `--build-backend` | Stage disabled-by-default local query backend store. | `--stage`, `--graph`, `--backend-approval`. | Generated file-store; no active server by default. |
| `--build-semantic-index` | Stage local deterministic semantic retrieval index. | `--stage`, `--graph`, `--semantic-approval`. | Generated semantic cache; provider calls remain blocked unless separately approved. |
| `--build-llm-proposals` | Stage local deterministic LLM-style proposal packets. | `--stage`, `--graph`, `--llm-approval`. | Proposals only, never canonical facts. |
| `--verify-extensions` | Stage extension verification and rollback closure. | `--stage`, `--graph`, `--verification-evidence`. | Closure packet and rollback/data deletion proof. |
| `--validate-live-governance` | Stage live governance packet. | `--stage`, `--live-approval`. | No live calls; validates approval/data/redaction/cache/budget boundary. |
| `--validate-live-runtime` | Stage local read-only runtime contract. | `--stage`, `--live-runtime-approval`, `--live-governance`. | Disabled-by-default local runtime contract; no launch. |
| `--validate-embedding-provider` | Stage embedding provider gate. | `--stage`, `--embedding-provider-approval`, graph/semantic inputs as required. | Provider gate/eval packet; no provider call unless approved in later execution. |
| `--validate-reranker-provider` | Stage reranker provider gate. | `--stage`, `--reranker-provider-approval`. | Provider gate packet; no external call by default. |
| `--build-hybrid-retrieval` | Stage hybrid retrieval pipeline. | `--stage`, graph/index/semantic/reranker inputs. | Generated explainable fusion packet; no canonical mutation. |
| `--validate-llm-proposal-provider` | Stage LLM proposal provider gate. | `--stage`, `--llm-proposal-provider-approval`, proposal/eval inputs. | Provider gate and safety eval; proposal-only. |
| `--build-review-ledger` | Stage human review ledger and proposal diff. | `--stage`, `--review-ledger-approval`, `--review-decisions`. | Owner decision ledger; still non-mutating. |
| `--build-canonical-mutation` | Stage mutation dry-run, journal and rollback artifacts. | `--stage`, `--canonical-mutation-approval`, review ledger and proposal diff. | Staged mutated graph copy only; canonical source graph is not silently changed. |
| `--build-live-audit` | Stage audit/security/observability/handoff packets. | `--stage`, `--live-audit-approval`, live runtime/actions/security inputs. | Redacted audit and operability evidence. |
| `--build-real-testing-readiness` | Stage readiness, target consent and pilot artifacts. | `--stage`, `--real-testing-approval` and target/gate/pilot inputs. | Dry-run pilot/readiness evidence only. |
| `--build-runtime-qa` | Stage runtime QA, performance and stabilization artifacts. | `--stage`, `--runtime-qa-approval` and QA/performance/stabilization inputs. | Staged QA evidence; no live browser automation in docs work. |

Disable modes delete generated artifacts under the stage root: `--disable-backend`, `--disable-semantic-index`, `--disable-llm-proposals`, `--disable-extensions`, `--disable-live-governance`, `--disable-live-runtime`, `--disable-embedding-provider`, `--disable-reranker-provider`, `--disable-hybrid-retrieval`, `--disable-llm-proposal-provider`, `--disable-review-ledger`, `--disable-canonical-mutation`, `--disable-live-audit`, `--disable-real-testing-readiness` and `--disable-runtime-qa`.

## Query Inputs

Graph query mode accepts:

- `--graph` for `project-code-graph.json` or `project-code-graph.jsonl`;
- optional `--index`, `--backend`, `--semantic-index`, `--hybrid-retrieval` and `--reranker-provider`;
- `--node-id`, `--target-id` and `--text` for query-specific selectors;
- `--max-results`, `--max-depth`, `--max-tokens`, `--hub-threshold`, `--node-type`, `--edge-type`, `--confidence` and `--path-prefix` for bounded output.

Supported query kinds include `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `changed_since`, `why_changed`, `read_order`, `hotspots`, `node`, `status` and `search`.

## Verification Commands

Common local verification commands:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
python -m mkdocs build --strict
git diff --check
```

Run the smallest relevant set for the current slice. A closure claim requires the full source docs -> registry -> docs tests -> `check_docs.py` -> strict MkDocs -> optional full closure order.

## Risks And Failure Modes

- Running a stage command inside a target workspace can blur generated and source-of-truth boundaries.
- Supplying approval JSON is not enough if the owner, allowed surfaces, data policy, rollback and verification evidence are missing.
- Query packets can be stale if graph fingerprints no longer match current source.
- Provider gate commands are not permission to call providers.
- Canonical mutation dry-run is not permission to mutate checked-in source or graph facts.
- Git commands remain explicit-only and are outside these CLI reference commands.

## Next Action

Use this page as the operator reference for local scripts. Navigation, source registry entries, docs tests and generated `site/` refresh belong to their owning docs-maintainer and tester slices.
