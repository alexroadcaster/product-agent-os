# Plan B1 CLI evidence

Source status: project-local implementation and synthetic verification evidence.

## PMETH-01 ownership and compatibility inventory

Inspected source revision `01d8e43d806774bb1ea36510999bb446e1357688`. All target inputs in this evidence are synthetic.

| Boundary | Existing owner and input | B1 disposition | Existing verification |
| --- | --- | --- | --- |
| CLI intake and host routing | run_contract and main (`plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`) take a workspace and optionally a v1 task JSON or inline task fields. task_routing (`plugins/product-agent-os/scripts/product_agent_os/task_routing.py`) validates, binds checks to source and invokes the quality/test selectors. routes (`plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`) consumes the route proposal. | Reuse the existing runner and intake. Extend normalization, the task profile and explicit task advice in this path. | `test_codex_runtime_runner_cli`, `test_render_infrastructure_cli` |
| Detection | analyze_workspace (`plugins/product-agent-os/scripts/product_agent_os/discovery.py`) enumerates paths, detects stack and classifies workspace signals. | Reuse its inventory for the task profile. | `test_product_agent_os`, existing discovery fixture cases |
| Repository methodology audit and synthesis | build_methodology_audit (`plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`) reads the workspace, classifies 12 domains and calls build_methodology_synthesis (`plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`) to group recommendations. Audit CLI (`plugins/product-agent-os/scripts/run_methodology_audit.py`) renders JSON or a report. | Preserve audit JSON, report, domain IDs, readiness semantics and existing runner packet. Task advice is an opt-in companion. | `test_methodology_audit`, `test_methodology_catalog`, `test_methodology_synthesis`, `test_methodology_report` |
| Web observed projection | Local-service application (`apps/local-service/src/http/application.mts`) serves revision-bound Project Analysis. Service (`apps/local-service/src/project-analysis/service.mts`) builds an owned, limited projection and runs bridge.py (`apps/local-service/src/project-analysis/bridge.py`) on it. Its allowlist carries stack, control-plane and manifest paths to Project Analysis (`apps/web/src/features/projects/ProjectAnalysis.tsx`), where Sources link to project files. Teams & Tasks consumes its own task/team endpoints. PMETH-19 owns connecting task advice to the current project/task path. | Reuse the Python adapter signature and add a TS decoder for B2. The Web bridge remains a project-only detector. | `tests/web/project-analysis-api.test.mts`, `tests/web/team-run-navigation.test.mts` |
| Proposal and execution | Infrastructure renderer (`plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`) creates separately routed proposals. F13's reviewed apply/G9 controls own target writes. | Task advice issues a requirements proposal and inert next step. Execution receipts and human verdicts are separate evidence. PMETH-16 owns staged artifacts and apply. | `test_render_infrastructure_cli`, reviewed apply/G9 suites |

Discovery's `_relative_files` filters names including `.venv`, `build`, `dist` and `site`; special dist evidence may be added explicitly. `_route_source_files` excludes generated first-run analysis from route signals. Audit `_relative_inventory` excludes `.git`, `node_modules`, `__pycache__` and supplied prefixes. A `.venv/pyproject.toml` path therefore falls outside ordinary discovery yet enters the audit's enumeration. The audit CLI passes no generated-prefix override; discovery's audit call supplies the first-run analysis prefix. The task profile consumes discovery rather than walking again. Presence of a path is detection. A projected file is observed evidence limited to that projection. A proposed next step supplies no execution or acceptance evidence.

The task input and quality/test owners stay in `task_routing.py` and the existing selectors. The scoped methodology decision uses one Python contract owner and a TypeScript reader. Legacy consumers include the audit report, runner guard/synthesis, first-run and status snapshot, the infrastructure renderer, and the Web Project Analysis bridge.

Baseline entrypoints from the repository root are `python -B plugins/product-agent-os/scripts/run_methodology_audit.py <fixture-project> --json` and `python -B plugins/product-agent-os/scripts/run_codex_runtime_runner.py <fixture-project> --contract --task-context <task-json>`.

The compatibility check found a duplicate renderer validator. Its obsolete event list reported `missing hook event: PostToolUse` for the current template, which makes that event optional. The first fixture eval returned exit 1 with 0/91 and two renderer tests rejected the template. The renderer now calls the canonical `validate_hook_json_text` validator, which checks mandatory events and validates the optional event if configured. The rerun passed 91/91 fixtures and 130/130 focused Python tests.

## PMETH-22 baseline and acceptance matrix

The fixture (`tests/fixtures/product_agent_os/pmeth-b1-synthetic.json`) defines both positive cases, their task AC, exact expected step, expected source and gap state. The baseline ledger (`tests/fixtures/product_agent_os/pmeth-b1-baseline.json`) was captured after intent normalization and before methodology decision policy. It preserves the source and original matrix hashes, exit codes, stdout projection, errors and pre/post file proof. The replay checks the actual synthetic project-file hashes, so edits to deferred-case metadata leave baseline inputs intact. Both routes were concise. The legacy docs route surfaced the backend test from TEST.md and had no task-specific source step. The repository audit provided 12 domains. Conflicting intent failed with exit 2. Before normalization, both the conflicting-intent and same-intent digest assertions failed.

| Slice | Synthetic acceptance oracle | Owner/gate |
| --- | --- | --- |
| Backend defect | Counter check first, with named source and no unfulfilled criteria. RED must be `AssertionError: 5 != 4` for the named test. The same assertion passes after the minimal fix. Setup/import failures are separate. | B1, existing runner and unittest |
| Docs-only | Check `counter.py` as the source of the guide behavior. A repo-wide policy check stays visible in the legacy route. | B1, existing runner |
| B1 negatives | Reject mixed/incomplete/conflicting context. Surface missing tests and partial/stale evidence. Reject a mismatched project, task or revision. No target writes. | B1, runner and both contract readers |
| Localized UI, coupled legacy UX, cross-feature UI | Existing UI/journey, rendering, ownership and boundary checks selected per scenario. Require a baseline on each profile before candidate and activation. | PMETH-08–11 |
| Native and AI/RAG | Native/device capability and meaningful eval/fixture readiness respectively. Require separate baseline capture before candidate and activation. | PMETH-23 profile-specific acceptance |
| Extension and safety cases | Misleading folders, unknown alias, stale spec, forged success, prompt injection, dirty files, denied writes and unavailable tools are candidate gates for the responsible branch. B1 checks stale evidence, forged reports and read-only execution boundary. | PMETH-10/11 (folders), PMETH-16/17 (aliases, permissions, dirty/output evidence), PMETH-21/23–26 (override, injection, tools, pilot) |

Synthetic threshold is all scoped checks with exact step/source and zero writes or false completion. The PMETH-24 pilot owner must record the actual sample, thresholds for first correct independent choice, time to next verifiable step, unnecessary steps and recommendation overrides before running any real pilot. This fixture uses no provider, accounts or personal data.

## B1 CLI and contract

Run the existing `run_codex_runtime_runner.py <workspace> --contract --task-context <workspace-relative-json>` with v1 task context. The equivalent Python entry point is `codex_runtime_runner.cli.run_contract(..., task_context=...)`. Suitable bounded tasks can use `--task`, `--change-mode`, `--changed-path`, `--acceptance` and `--risk-level`; use the context file for structured risks, checks and verification paths. A matching legacy hint is redundant. A conflicting hint, incomplete inline input or mixed inline/JSON input returns exit 2. Scoped output goes to stdout. Repository-only `--contract` retains its optional `--output`.

The task view is `route_packet.methodology_decision`. Python contract (`plugins/product-agent-os/scripts/product_agent_os/methodology_contract.py`) owns shape and version. TypeScript decoder (`packages/contracts/methodology-decision.ts`) consumes that wire contract and requires the caller's current scope. The opaque local project identity derives from the resolved root. Source revision binds the discovery inventory and content fingerprints of the scoped files, check sources and relevant project configuration. Task revision binds the normalized task without caller-reported test results. The file references identify content fingerprints for observed files. They establish provenance for a proposed check, with semantic or execution verification handled separately.

| Existing field or route | Compatibility |
| --- | --- |
| Audit CLI JSON and Markdown, `methodology_domains`, readiness and synthesis | Continue on existing code paths. No remapping to the five task methods. |
| Runner `methodology_packet` and `task_routing` | Retain existing roles and readiness semantics. The scoped recommendation is a separate v1 field emitted only for structured task intake. |
| `facts`, `decisions`, `requirements`, `plan` | Facts derive from discovery and explicit task inputs. Decisions explain applicability. Requirements link each criterion to a proposed check or a gap. The plan shows the next step, assumptions and one blocking question if needed. |
| `execution`, `acceptance`, `authority` | Fixed at `not_started`, `not_evaluated` and `read_only`. Unknown versions, wrong scope and unresolved evidence references fail validation. |

The synthetic backend case emits `run_regression` with the named unittest and the `TEST.md` and test-file references. The docs case emits `check_source` with `counter.py`. Unmatched or absent checks and unmapped criteria remain explicit gaps. Refactors use characterization, configuration changes use source checks, and an explicitly required evaluation points at the rubric. Applying proposals, automatic execution and technical acceptance belong to later tasks.

## Observed TDD receipt

Command was `python -B -m unittest test_counter.CounterTest.test_increment_by_one` in a disposable synthetic project using Python 3.13.5.

| Stage | Fixture revision | Expected and observed result |
| --- | --- | --- |
| RED | `4f8db147541e5e342cc5ad7ed0952d013b19f94e8f79165a47872c513e99dfa7` | Exit 1, `AssertionError: 5 != 4` in the named behavior check. |
| GREEN | `d0cade800c8abf9d5c556305fad54f1f7ecf2b4a5974927b2e29fb9297db9177` | Exit 0, `OK` for the same check after changing `+ 2` to `+ 1` in `counter.py`. |
| Setup failure control | `6c2a4918627f3c95924a8bd10d77766a775b889bb2043b38383bfbc1b957c499` | Exit 1, `ModuleNotFoundError: No module named 'counter'`. Classified separately from the behavioral RED. |

Test SHA-256 remained `ad7057f56ef3dc92f74e548c968d59cede253a212e25d2fd0d1f6763734c233e`. Each invocation preserved all fixture bytes. The minimal GREEN changed only the counter implementation, so no further refactor was warranted.

## B2 handoff

PMETH-19 owns passing current project/task/source identities through the local service and authenticating that request on the existing API. PMETH-20 owns rendering recommendations in the existing task interface. PMETH-26 owns the user-facing RU/EN CLI and Web guide after parity. The current B1 receipt covers local CLI and Python/TS wire decoding. Web rendering, actual-agent usefulness and owner acceptance have separate evidence.

## Verification runs

The working tree was based on `01d8e43d806774bb1ea36510999bb446e1357688`. SHA-256 of the sorted path and file-SHA-256 pairs for the 15 candidate source and test files is `62c61532f2e23efa271a612334e2b5bbd912b6b6a6063a38a34a2835aec3c17a`. The plan check found seven implemented B1 tasks, 19 unchanged task records and 31 unchanged dependency edges. The JSON mirrors matched byte for byte.

Focused Python checks passed 130/130, fixture eval 91/91, transcript eval 26/26, and the Python→TypeScript and existing Project Analysis tests 2/2. Type checking, local compatibility, RU/EN matrices and the strict MkDocs build passed. The initial docs build reported source links outside the site and a missing English evidence page. The published pages list source paths as text and provide locale-specific evidence.

`python -B -m unittest discover -s tests -p 'test_*.py' -q` with process-local `TEMP` and `TMP` exited 0. It ran 1,386 tests with one skip in 599.363 seconds. The initial run before the renderer correction had 26 failures, including Windows temporary path casing discrepancies. The rerun used the corrected renderer and a separate workspace temporary directory.
