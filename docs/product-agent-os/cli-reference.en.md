# Product-Agent OS CLI reference

Source status: `official + experiment`

This page records the local Product-Agent OS CLI surfaces that already exist in `plugins/product-agent-os/scripts/`. It describes commands as stage/read-only tooling: they do not publish the plugin, start external systems or perform live provider/model/API calls without separate explicit approval.

## Ordinary route: a bounded task {#ordinary-route}

For an existing project, pass `--task-context task.json`. The JSON path is relative to the target workspace and must remain inside it. Omitting this argument preserves the previous route, marked `routing_trace.mode=legacy`.

```powershell
python plugins/product-agent-os/scripts/run_codex_runtime_runner.py ./sample --contract --task-context task.json
python plugins/product-agent-os/scripts/render_infrastructure.py ./sample --dry-run --task-context task.json
```

For this `sample` workspace example, `TEST.md` must already contain `python -m unittest test_calc -v`; `calc.py` and `test_calc.py` are the source and regression test. The runner does not create these files automatically.

```json
{
  "schema_version": 1,
  "task_id": "fix-addition",
  "intent": "Fix addition",
  "change_mode": "defect_fix",
  "changed_paths": [
    "calc.py"
  ],
  "verification_paths": [
    "test_calc.py"
  ],
  "risk_level": "low",
  "acceptance": [
    "total(2, 3) equals 5"
  ],
  "risks": [
    {
      "risk_id": "sum",
      "kind": "pure_logic",
      "description": "Addition regression",
      "protected_invariants": [
        "addition"
      ],
      "languages": [
        "python"
      ]
    }
  ],
  "executable_test_seam": true,
  "checks": [
    {
      "command": "python -m unittest test_calc -v",
      "source": "TEST.md",
      "test_kinds": [
        "unit"
      ]
    }
  ]
}
```

Selection uses the existing T26/T27 selectors. `routing_trace` reports `ordinary`, `full` or `needs_context`, the invoked selectors and absence of legacy fallback. `route_ready` means an action plan is available: commands have not run, sources have not changed and the task is not completed.

- `docs_only` accepts Markdown/text changes without behavioral risks; the code-change contract is not applicable. `no_op`, `reuse`, `configuration` and `deletion` support outcomes without new code.
- Unknown risk, missing checks or stale evidence produce an explicit gap. High-risk, boundary/critical-flow, sensitive paths/intent, financial/release and explicit-full context retain full reporting and applicable gates.
- `checks` maps a command from a real source to test kinds. Recognized command lines in `AGENTS.md`, `AGENTS.override.md`, `TEST.md` and nested instructions are retained conservatively. This is not a semantic policy parser: Codex must read all applicable instructions; they override selection.
- Optional `state` contains `value`, `source` and `sha256`, matching a JSON record with the same `task_id` and `lifecycle_state`. Neither state nor task-context data grants write authority.
- Unknown fields/versions and paths outside the workspace return exit 2. A ready route returns exit 0; `needs_context`, `needs_approval` and `blocked` return exit 1.
- `--stage` also accepts task context, but requires resolved gaps and an output directory outside the target. Existing ordinary projects normally reuse documents without generating a new package.

The example and fields are a local Product-Agent OS contract, not an OpenAI API. See [artifact contracts](artifact-contracts.en.md#ordinary-route-contract).

## Purpose

The CLI layer supports a repeatable local evidence loop:

- read-only audit or dry-run packet before changes;
- stage-only generation into an explicit output directory;
- approval-bound merge or rollback only through a separate approval record;
- deterministic runtime contract for Codex App, CLI or IDE extension;
- project graph generation, queries, generated cockpit, local indexes and provider/mutation governance packets;
- docs/closure verification through separate docs-maintainer and tester slices.

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

## First-Run Analysis CLI

| Command | Purpose | Required inputs | Output / boundary |
| --- | --- | --- | --- |
| `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --full-dry-run` | Run safe first-run orchestration without writing files. | Target workspace path. | Read-only preview; no generated files are created. |
| `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --dry-run` | Print the first-run packet without writing files. | Target workspace path. | Read-only preview; no generated files are created. |
| `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --stage <dir>` | Stage first-run generated artifacts into an explicit stage directory. | Target workspace and stage directory. | Stage root must be outside the target workspace; stage-inside-target is blocked. |
| `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --write-analysis` | Write generated first-run packet and offline HTML to the local analysis folder. | Target workspace path. | Writes only under `.codex/product-agent-os/analysis/`; generated views remain `orientation_only_not_proof`. |
| `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --write` | Legacy write route for the first-run packet. | Target workspace path. | Writes generated packet, including `.codex/product-agent-os/analysis/first-run-analysis-packet.json`; not target source mutation. |

`run_first_project_analysis.py` chooses exactly one mode: `--full-dry-run`, `--dry-run`, `--stage <dir>`, `--write-analysis` or `--write`. `DOC-M26` owns the full operator command matrix: see [Operator command matrix](operator-command-matrix.md). Redocly `not_applicable` until an OpenAPI source contract exists. These commands do not approve live servers, browser automation, provider/API calls, target source mutation, git actions, release, promotion or root `site` rebuild.

Safe operator examples:

```powershell
python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --full-dry-run
python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --dry-run
python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --stage C:\tmp\product-agent-os-first-run
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --dry-run
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --stage C:\tmp\product-agent-os-graph-stage
```

These examples are not the broad command matrix. The full command-policy matrix, docs-tooling smokes, install/runtime variants and approval-state coverage belong to `DOC-M26`. CLI docs provide safe pointers only and do not expand permission for live servers, browser automation, provider/API calls, canonical mutation, git actions or root `site` rebuild.

## Self-Learning Loop Due-Check CLI

| Command | Purpose | Inputs | Output / boundary |
| --- | --- | --- | --- |
| `python plugins\product-agent-os\scripts\check_self_learning_due.py <workspace> --dry-run` | Checks whether the owner should be offered a manual Self-Learning Loop run. | Product-Agent OS workspace with `.codex/product-agent-os/self-learning-state.json`. | Prints `due`, `not_due`, `disabled` or `state_invalid`; does not run analysis, write state, create a schedule or enable auto-apply. |

In this contract, `weekly` means a due-check basis, not an active schedule.

## Self-Learning Loop Manual Runner CLI

| Command | Purpose | Inputs | Output / boundary |
| --- | --- | --- | --- |
| `python plugins\product-agent-os\scripts\run_self_learning_loop.py <workspace> --dry-run` | Builds a Self-Learning Loop run packet without writing files. | Product-Agent OS workspace with an explicit marker and self-learning state. | Prints `self_learning_run_packet_v1`, progress events and planned artifact targets; does not write the workspace or auto-apply anything. |
| `python plugins\product-agent-os\scripts\run_self_learning_loop.py <workspace> --stage <dir>` | Generates staged progress state and an offline HTML artifact. | Product-Agent OS workspace, stage directory outside the target workspace. | Writes only under the stage root: `progress.jsonl`, run `progress.json`, `self-learning-run-packet.json` and `self-learning-progress.html`. The target workspace is not changed. |

The manual runner starts with the Product-Agent OS scope detector and fails closed for `out_of_scope`, `missing_marker` and `needs_owner_review`. It does not create scheduler/hooks/Codex App automation, ingest raw sessions, call providers or perform git/release/deploy/publish actions.

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

## Cockpit Query Surface

The project graph CLI feeds cockpit data, but it does not turn the cockpit into proof:

- `--stage <stage-dir>` writes generated `project-code-graph.json`, `project-code-graph.jsonl`, `project-cockpit.html` and `project-cockpit.json` inside the stage root.
- `--query read_order --graph <project-code-graph.json>` returns bounded guided read order; use it as a reading hint, then inspect source files before edits or impact claims.
- `--query trace`, `--query impact` and `--query affected_tests` create static query packets; they do not prove runtime routes, dynamic dispatch or test results.
- `--query search` may use graph-only search, static index, semantic index or hybrid inputs when provided; returned hits remain orientation evidence.

Examples:

```powershell
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --query read_order --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --max-results 12
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --query trace --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --node-id function:app.main.main --max-depth 3
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --query status --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json
```

Static fallback is the supported visual boundary in this docs slice. Cosmos.gl/WebGL, browser screenshots, interactive canvas behavior, performance proof and accessibility visual proof remain unsupported until a separate approved runtime/browser evidence packet exists.

## Outputs

- Staged JSON, JSONL, HTML, report or validation packets under the approved stage boundary.
- Console output that can be cited as current command evidence when the command actually ran.

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

Run the smallest relevant set for the current task: source docs → registry → docs tests → `check_docs.py`. Strict MkDocs and site checks are required for navigation, diagrams, search or generated-site changes when the build is authorized; select other gates by affected behavior. [Documentation update workflow](../playbooks/docs-update.md).

## Risks And Failure Modes

- Running a stage command inside a target workspace can blur generated and source-of-truth boundaries.
- Supplying approval JSON is not enough if the owner, allowed surfaces, data policy, rollback and verification evidence are missing.
- Query packets can be stale if graph fingerprints no longer match current source.
- Provider gate commands are not permission to call providers.
- Canonical mutation dry-run is not permission to mutate checked-in source or graph facts.
- Git commands remain explicit-only and are outside these CLI reference commands.

## Next Action

Use this page as the operator reference for local scripts. Navigation, source registry entries, docs tests and generated `site/` refresh belong to their owning docs-maintainer and tester slices.
