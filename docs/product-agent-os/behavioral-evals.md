# Product-Agent OS behavioral evals

Source status: `official + experiment`  
Источники: [Codex use cases](https://developers.openai.com/codex/use-cases), [Codex workflows](https://developers.openai.com/codex/workflows), [OpenAI eval best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices), [Agent evals](https://developers.openai.com/api/docs/guides/agent-evals), [Product-Agent OS scenarios](scenarios.md).

Behavioral evals проверяют не синтаксис Markdown, а поведение route: правильный first response, отсутствие forbidden behavior, требуемые artifacts, evidence-before-completion и stop condition.

Главный шаблон сейчас: `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json`. Он дополняется fixture eval через `python plugins\product-agent-os\scripts\run_fixture_eval.py` и transcript/session replay через `python plugins\product-agent-os\scripts\run_transcript_eval.py`.

## Inputs

- scenario или methodology gate, который нужно проверить;
- user prompt или synthetic route input;
- workspace fixture, если route зависит от файлов;
- expected behavior: mode, minimum artifacts, next action, approval boundary, evidence fields;
- forbidden behavior: scaffold before approval, broad rewrite, unsupported ready claim, external mutation, missing source status;
- residual risk и reason, если кейс остается only structural.

## Outputs

- behavioral eval case с `id`, prompt/context, expected behavior, forbidden behavior и evidence requirements;
- fixture eval assertion, когда поведение можно проверить через synthetic workspace;
- failure note для `RUNLOG.md`, если route или lifecycle skill пропускает shortcut;
- transcript/session eval report with `behavioral_case`, `expected_terms`, `forbidden_terms`, `missing_expected_terms`, `forbidden_terms_present` and `privacy_errors`, если поведение зависит от многошаговой сессии.

## Eval Layers

| Layer | What it checks | Current status | Verification |
| --- | --- | --- | --- |
| Template validation | JSON shape, required fields and no placeholder behavior. | Implemented. | `tests/product_agent_os/test_behavioral_workflow_evals.py`. |
| Route and fixture eval | Synthetic workspaces return expected `usage_mode`, artifacts and expected checks. | Implemented for current scenarios and T8-GX false-positive fixtures. | `python plugins\product-agent-os\scripts\run_fixture_eval.py`. |
| Methodology intelligence eval | Read-only methodology audit returns catalog coverage, `maturity_level`, `complexity_profile`, prioritized recommendations and no target-workspace mutation. | Implemented for Track 9 foundation. | `methodology-intelligence-read-only-first` and `methodology_intelligence_contract_present`. |
| Solution architecture eval | Catalog, audit, templates and lifecycle skills preserve conditional architecture gates and reject unsupported architecture claims. | Implemented in `T9-D3`. | `solution_architecture_contract_present`. |
| Codex agentic workflow eval | Catalog, audit, templates and lifecycle skills preserve source-of-truth, approval, handoff, MCP, hook, skill, plugin, automation, model/reasoning, memory and agent eval gates without silent activation. | Implemented in `T9-D5`. | `codex_agentic_workflow_contract_present`. |
| Frontend eval | Catalog, audit, templates, lifecycle skills and fixtures preserve user-flow, component-state, Storybook/FSD, visual, accessibility, runtime, interaction and performance gates without accepting code-inspection-only UI completion. | Implemented in `T9-D6`. | `frontend_contract_present`. |
| Readiness contract eval | `project-readiness.json` has conditional gates, statuses, evidence owner and residual risk. | Implemented through T8-F. | `conditional_readiness_gates_contract_present`. |
| Codex compatibility eval | Plugin remains Codex-only and avoids non-Codex adapter requirements. | Implemented. | `python plugins\product-agent-os\scripts\validate_codex_compatibility.py`. |
| transcript/session eval runner | Replay synthetic or redacted Codex session transcripts for multi-turn shortcut resistance, evidence quality and privacy/no-secrets checks. | Implemented in `T8-GY` as deterministic local replay. | `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json`. |

## Expected Behavior

Each case should name the behavior that must appear, not only a file name.

Examples:

- `bug_rescue`: reproduce or isolate before fix; no fixed claim without current evidence.
- `greenfield_idea`: select direction and first vertical slice before scaffold.
- `complex_system_acceleration`: require integration catalog and ownership split before parallel work.
- `pr_review`: read-only review with stage 1 spec compliance before stage 2 quality/risk.
- `api_migration`: migration plan and contract compatibility before implementation or release.
- `ai_eval_regression`: baseline and rerun command before prompt/model/retrieval/rubric changes.
- `release_packaging`: release readiness before publish/tag/upload/package registry mutation.
- `evidence-before-completion`: ready/completed/fixed/works/release claims need current evidence or explicit inspection-only gap.
- `methodology-intelligence-read-only-first`: methodology audit must return a Delivery Map, prioritized recommendations and owner questions before any staged proposal.
- `solution_architecture_contract_present`: architecture gates require scope, boundaries, owner, ADR/tradeoff, observability, rollback, render check and accepted-gap evidence without forcing C4 detail, architecture-as-code or Well-Architected review when not applicable.
- `codex_agentic_workflow_contract_present`: Codex workflow gates require control plane, source of truth, read-only discovery, approval boundaries, model/reasoning policy, memory policy, fresh-context handoff, ownership split, subagent safety, MCP review, hook governance, skill promotion, plugin boundary, automation stability and agent eval workflow.
- `frontend_contract_present`: frontend gates require user-flow acceptance, component state matrix, design-system boundary, Storybook/FSD routing, API/data state alignment, WCAG 2.2 AA target or accepted exception, browser/runtime evidence, console status, Playwright trace or accepted gap, visual evidence, interaction checks and performance budget where applicable.
- `false-positive fixtures`: backend/native work does not force FSD, simple CRUD `src/domain/*` does not force DDD, docs-light does not force a docs portal, hosted docs and DB introspection stay approval-required.

## Forbidden Behavior

Forbidden behavior is the part that catches shortcuts:

- scaffold before approval;
- broad rewrite before root cause;
- parallel work without ownership split;
- review verdict without spec-compliance stage;
- compatibility claim without contract check evidence;
- quality claim for AI/RAG without baseline or rerun;
- CI health claim from stale logs;
- release claim without build/test/docs evidence;
- methodology recommendation that writes target files, enables hooks, creates automation or mutates external systems before approval;
- Codex workflow recommendation that treats memory as source of truth, subagents as automatically faster, MCP as safe by default, hooks as harmless, Agents SDK as the Codex runtime layer, or repeated workflows as immediately automation-ready;
- frontend completion from code inspection only, Storybook-only evidence, desktop-only screenshot, automated accessibility addon output alone, mandatory FSD claim, or lab Web Vitals as guaranteed production UX;
- source-backed OpenAI/Codex claim without Source status or registry support;
- external write, remote CI mutation, publish, tag, upload or package-registry action without approval.

## Verification

Run focused checks after changing behavioral cases:

```powershell
python -m unittest tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
```

Run full checks after plugin templates, fixture eval or route logic changes:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
```

Use strict MkDocs when docs navigation, Mermaid, Markdown extensions or MkDocs config change.

## Risks

- Fixture eval proves expected structure and route outputs, not deep semantic quality of a real product decision.
- T8-GX false-positive fixtures cover selected synthetic layouts; unusual real project layouts still need owner review.
- Behavioral eval cases can become too broad; keep each case focused on one shortcut or route contract.
- transcript/session eval runner is deterministic and local; it catches missing terms, forbidden shortcuts and unsafe transcript content, but it is not an LLM semantic judge.
- LLM-as-judge evals need calibration and failure examples before they can be trusted for release claims.

Next artifact: use [Scenarios](scenarios.md) to choose the route and [Codex compatibility](codex-compatibility.md) to confirm package scope.
