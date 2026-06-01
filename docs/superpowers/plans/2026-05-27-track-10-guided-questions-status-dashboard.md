# Track 10 Guided Questions And Status Dashboard Implementation Plan

Source status: `local implementation planning`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build Track 10 so Product-Agent OS can guide users with bounded, methodology-aware questions, maintain a single offline HTML status artifact for project progress, stage a self-verification loop for agents, skills and harness modernization decisions, and generate a read-only project code graph for dependency-aware navigation.

**Architecture:** Extend the existing Track 8 usage-mode route and Track 9 methodology packet with a typed question protocol, answer ledger, status snapshot, staged static dashboard renderer, local-first metrics loop for self-verification, and staged code-graph pipeline: read-only scanner, graph JSON/index artifacts, compact agent query packets and static HTML visualization. JSON, JSONL and Markdown remain the source of truth; HTML artifacts are generated, reviewable views that are staged first and never silently mutate the target workspace.

**Tech Stack:** Python standard library, `ast`, `unittest`, JSON/JSONL contracts, Markdown control-plane artifacts, static HTML/CSS/vanilla JavaScript, optional locally bundled `graphology`/`sigma.js` for graph rendering, existing `plugins/product-agent-os/scripts/product_agent_os/*` modules, existing Codex runtime runner, fixture eval runner, transcript eval runner, docs checks, MkDocs.

---

## Scope Check

Track 10 is a new user-facing capability, not part of Track 9 final documentation sync.

It includes these implementation tasks:

- `Task 23: Guided Question Protocol And Project Status Dashboard`
- `Task 24: Self-Verification And Modernization Loop`
- `Task 25: Project Code Graph And HTML Cockpit Visualization`

Track 10 must start only after Track 9 `Task 22` closes the current Product-Agent OS documentation baseline. This prevents Task 22 from becoming a moving target while Track 10 changes runtime packets, renderer output, evals and docs.

## Numbering Note

The Track 9 plan now keeps the former `Task 23: Final Verification Baseline` only as a legacy checklist section under Task 22. Task 22 absorbs that verification baseline into `T22-U-M23`, so Track 10 uses `Task 23` for the next product capability:

- typed guided questions;
- answer ledger;
- status snapshot;
- offline `status.html` dashboard.
- agent/skill/harness self-verification and staged modernization candidates.
- project code graph scanner, compact graph packets and offline HTML cockpit visualization.

Do not implement Track 10 unless Track 9 docs keep the legacy final baseline absorbed into Task 22 and current verification evidence exists.

## Product Outcome

After Track 10, a user should be able to enable Product-Agent OS in a real project and see:

- one or zero blocking questions at a time;
- optional follow-up questions grouped by product, technical, verification, approval and ownership category;
- why each question matters and what artifact it affects;
- a stable status page showing current lifecycle state, usage mode, methodology readiness, evidence gaps, approvals, staged artifacts, open risks and next safe action;
- stale/evidence warnings when the dashboard is generated from inspection-only or old command evidence.
- staged self-verification reports for generated agents, skills, prompt or policy packs, router/tool policies and harness versions, with modernization candidates separated from approval.
- a project code graph that shows code, docs, templates, contracts and generated artifacts as dependency nodes with confidence-labelled edges and compact agent read-order hints.

The plugin must keep forward momentum. It should ask only questions that block safe planning, approval, evidence or the next artifact.

## Non-Goals

- Do not add a standalone web server.
- Do not add a database.
- Do not add a live model call, OpenAI API dependency, or Agents SDK app.
- Do not activate MCP servers, hooks, GitHub Actions, recurring automations or external writes.
- Do not make HTML the source of truth.
- Do not create browser-based editing of project files in this track.
- Do not claim universal semantic code intelligence from file/path scans, unsupported language parsers or inferred dependency edges.
- Do not store secrets, credentials, private customer data, raw private chat logs, production screenshots or absolute user-specific paths.
- Do not automatically apply self-modernization candidates, rewrite skills, enable recurring evaluation schedules or promote automation without explicit owner approval and rollback evidence.

## File Structure

### New Plugin Files

- `plugins/product-agent-os/scripts/product_agent_os/question_protocol.py`  
  Builds typed `question_queue` packets from methodology audit, usage mode, runtime status and control-plane gaps.

- `plugins/product-agent-os/scripts/product_agent_os/question_ledger.py`  
  Loads, validates and renders a staged answer ledger without writing to the target workspace by default.

- `plugins/product-agent-os/scripts/product_agent_os/status_snapshot.py`  
  Builds a deterministic `status_snapshot` JSON packet from workspace audit, runtime route, methodology packet, renderer result and optional answer ledger.

- `plugins/product-agent-os/scripts/product_agent_os/status_dashboard.py`  
  Renders static offline `status.html` and `status.json` from the snapshot.

- `plugins/product-agent-os/scripts/render_status_dashboard.py`  
  CLI wrapper for dry-run and staged dashboard rendering.

- `plugins/product-agent-os/assets/templates/status-dashboard/status.html`  
  Static dashboard template with no CDN, no external requests and no inline private data.

- `plugins/product-agent-os/assets/templates/status-dashboard/status.css`  
  Static CSS for readable desktop and mobile states.

- `plugins/product-agent-os/assets/templates/artifact-templates/question-ledger.md`  
  Human-readable answer ledger companion artifact for teams that prefer Markdown review.

### Modified Plugin Files

- `plugins/product-agent-os/scripts/product_agent_os/discovery.py`  
  Attach `question_queue` seed data to workspace discovery without changing source policy or route input separation.

- `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`  
  Preserve current `questions_for_owner` and add typed question source metadata.

- `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`  
  Preserve owner-question dedupe while allowing stable question IDs.

- `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`  
  Validate bounded `question_queue`, `status_snapshot_ref` and schema-v1 compatibility.

- `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`  
  Add question-aware first response fields and status dashboard finish option when safe.

- `plugins/product-agent-os/scripts/product_agent_os/templates.py`  
  Register `question-ledger.md` and optional status dashboard templates.

- `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`  
  Include staged question ledger and status dashboard files in renderer output only after validation.

- `plugins/product-agent-os/scripts/run_fixture_eval.py`  
  Add fixture checks for bounded questions, dashboard presence, no external assets and stale evidence warnings.

### Modified Skills

- `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`
- `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`
- `plugins/product-agent-os/skills/requirements-author/SKILL.md`
- `plugins/product-agent-os/skills/implementation-planner/SKILL.md`
- `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`
- `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`
- `plugins/product-agent-os/skills/docs-maintainer/SKILL.md`
- `plugins/product-agent-os/skills/pr-release-operator/SKILL.md`
- `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md`

Each skill should consume typed questions instead of inventing broad interview prompts. The first response can ask one blocking question only when the answer changes safe next action, evidence, approval, scope or ownership.

### New Or Modified Tests

- `tests/product_agent_os/test_question_protocol.py`
- `tests/product_agent_os/test_question_ledger.py`
- `tests/product_agent_os/test_status_snapshot.py`
- `tests/product_agent_os/test_status_dashboard.py`
- `tests/product_agent_os/test_codex_runtime_runner_contracts.py`
- `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`
- `tests/product_agent_os/test_discovery.py`
- `tests/product_agent_os/test_infrastructure_renderer.py`
- `tests/product_agent_os/test_infrastructure_templates.py`
- `tests/product_agent_os/test_fixture_eval_runner.py`
- `tests/product_agent_os/test_lifecycle_skills.py`
- `tests/product_agent_os/test_product_agent_os_docs.py`

### New Or Modified Docs

- `docs/product-agent-os/index.md`
- `docs/product-agent-os/technical.md`
- `docs/product-agent-os/architecture.md`
- `docs/product-agent-os/scenarios.md`
- `docs/product-agent-os/behavioral-evals.md`
- `docs/product-agent-os/codex-compatibility.md`
- `docs/product-agent-os/methodology-intelligence.md`
- `plugins/product-agent-os/README.md`
- `docs/sources/product-agent-os-track-10-backlog.md`
- `docs/sources/registry.md`
- root `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`

## Shared Contracts

### Question Queue

```json
{
  "schema_version": 1,
  "status": "ready",
  "policy": {
    "max_blocking_questions_in_first_response": 1,
    "max_total_questions": 8,
    "ask_only_if_blocks_next_artifact": true
  },
  "questions": [
    {
      "id": "verification_command",
      "priority": "blocking",
      "category": "verification",
      "question": "Which local command is the source of truth for verification?",
      "answer_type": "single_choice_or_text",
      "options": ["npm test", "pytest", "python -m unittest discover -s tests -p \"test_*.py\" -v"],
      "blocks": ["completion_claim", "implementation_ready"],
      "writes_to": ["TEST.md", "RUNLOG.md"],
      "source": "methodology_audit",
      "evidence_required": ["current command or explicit gap"],
      "stale_when": "command list or test framework changes"
    }
  ]
}
```

Allowed `priority` values:

```python
QUESTION_PRIORITIES = [
    "blocking",
    "recommended",
    "optional",
]
```

Allowed `category` values:

```python
QUESTION_CATEGORIES = [
    "scope",
    "product",
    "verification",
    "approval",
    "ownership",
    "risk",
    "release",
]
```

Allowed `answer_type` values:

```python
QUESTION_ANSWER_TYPES = [
    "text",
    "single_choice",
    "single_choice_or_text",
    "multi_choice",
    "approval",
    "not_applicable_or_gap",
]
```

### Answer Ledger

```json
{
  "schema_version": 1,
  "answers": [
    {
      "question_id": "verification_command",
      "answer": "python -m unittest discover -s tests -p \"test_*.py\" -v",
      "answered_by": "project owner",
      "answered_at": "2026-05-27T00:00:00Z",
      "confidence": "owner_confirmed",
      "writes_to": ["TEST.md", "RUNLOG.md"],
      "stale_when": "test framework changes",
      "private_data_status": "none"
    }
  ]
}
```

### Status Snapshot

```json
{
  "schema_version": 1,
  "generated_at": "2026-05-27T00:00:00Z",
  "workspace": "[redacted-local-path]",
  "lifecycle_state": "requirements_ready",
  "usage_mode": {
    "primary": "greenfield_idea",
    "confidence": "high"
  },
  "next_safe_action": "Stage quality-strategy.md with verification command or accepted gap.",
  "question_summary": {
    "blocking": 1,
    "recommended": 2,
    "optional": 1
  },
  "readiness_summary": {
    "present_verified": 0,
    "present_unverified": 3,
    "applicable_missing": 2,
    "approval_required": 1
  },
  "evidence_summary": {
    "current_command_evidence": false,
    "current_eval_evidence": false,
    "inspection_only": true
  },
  "dashboard_policy": {
    "source_of_truth": "json_and_markdown_control_plane",
    "html_is_generated_view": true,
    "external_assets": false
  }
}
```

## Task 23: Guided Question Protocol And Project Status Dashboard

**Files:**
- Create: `plugins/product-agent-os/scripts/product_agent_os/question_protocol.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/question_ledger.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/status_snapshot.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/status_dashboard.py`
- Create: `plugins/product-agent-os/scripts/render_status_dashboard.py`
- Create: `plugins/product-agent-os/assets/templates/status-dashboard/status.html`
- Create: `plugins/product-agent-os/assets/templates/status-dashboard/status.css`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/question-ledger.md`
- Create: `tests/product_agent_os/test_question_protocol.py`
- Create: `tests/product_agent_os/test_question_ledger.py`
- Create: `tests/product_agent_os/test_status_snapshot.py`
- Create: `tests/product_agent_os/test_status_dashboard.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/discovery.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`
- Modify: `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`
- Modify: `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/templates.py`
- Modify: `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`
- Modify: `plugins/product-agent-os/scripts/run_fixture_eval.py`
- Modify: lifecycle skills under `plugins/product-agent-os/skills/`
- Modify: Product-Agent OS docs and root control-plane files

Task 23 implementation matrix:

| ID | Task | Files | Acceptance |
| --- | --- | --- | --- |
| `T10-Q-M-1` | Run baseline contract audit | existing tests and source inventory | Confirm Track 10 files are still absent, previous-track surfaces are available (`questions_for_owner`, `unknowns`, `safe_next_action`, `methodology_synthesis`, `recommendation_groups`, `source_artifact_ledger`, `usage_mode`, `route_inputs`, `methodology_packet`, `finish_options`, staged renderer, manifest, approval flow, redaction), and focused baseline tests pass before implementation. |
| `T10-Q-M0` | Add question protocol tests | `tests/product_agent_os/test_question_protocol.py` | Tests define stable question IDs, priorities, categories, answer types, one-blocking-question first response, bounded queue size, priority trimming, and deterministic mapping from existing audit/runtime sources. |
| `T10-Q-M1` | Implement question protocol adapter | `question_protocol.py` | Module adapts existing owner questions, audit unknowns, recommendation groups, usage mode and runtime gaps into typed question packets without duplicating methodology logic or writing workspace files. Stable question IDs come from canonical source/category/block/artifact metadata, not arbitrary prompt text. |
| `T10-Q-M2` | Preserve existing owner question compatibility | `methodology_audit.py`, `methodology_synthesis.py`, tests | Existing `questions_for_owner` and `dedupe_owner_questions` remain present; typed queue is additive and schema-v1 compatible. Modify synthesis only if typed source metadata requires it. |
| `T10-Q-M3` | Add answer ledger contract tests | `test_question_ledger.py` | Ledger validates schema, stale policy, private data status, secret-like values, stale answers, malicious answers, and answer-to-artifact mapping. |
| `T10-Q-M4` | Implement answer ledger helpers | `question_ledger.py`, `question-ledger.md`, `templates.py` | Ledger can render JSON and Markdown proposal artifacts, staged-only by default. |
| `T10-Q-M5` | Attach question queue to discovery | `discovery.py`, `test_discovery.py` | Workspace discovery returns `question_queue` derived from `methodology_intelligence`, `usage_mode` and control-plane gaps while keeping `route_inputs` separation intact. Mature existing control-plane and inspection-only fixtures can produce zero blocking questions. |
| `T10-Q-M6` | Add runtime contract validation | `contracts.py`, runtime contract tests | Runtime validates bounded `question_queue` and optional `status_snapshot_ref` as additive sibling fields in `route_packet`; `methodology_packet` stays strict/read-only and rejects unknown fields, invalid answer types or too many questions. |
| `T10-Q-M7` | Route question-aware first response | `routes.py`, runtime route tests | First response exposes only `next_blocking_question` plus remaining counts and question summary; it does not dump the full queue. Add a dashboard finish option only when the route can safely stage or view the dashboard. |
| `T10-Q-M8` | Add status snapshot tests | `test_status_snapshot.py` | Snapshot summarizes lifecycle, usage mode, readiness, evidence freshness, approvals, staged artifacts, renderer file count, stage manifest digests, source artifact ledger, semantic evidence sufficiency, redaction summary and stale state. |
| `T10-Q-M9` | Implement status snapshot builder | `status_snapshot.py` | Builder consumes audit/runtime/renderer/manifest/ledger packets, reuses existing redaction, avoids raw local paths/private data, and labels inspection-only or stale evidence without success claims. |
| `T10-Q-M10` | Add dashboard renderer tests | `test_status_dashboard.py` | Tests assert valid offline HTML, no external URLs, embedded JSON safety, mobile sections and stale evidence banner. |
| `T10-Q-M11` | Implement static dashboard renderer | `status_dashboard.py`, dashboard templates | Renderer creates `status.html` and `status.json` from snapshot without external assets, scripts from external origins, raw local paths, secrets or private data. |
| `T10-Q-M12` | Add CLI wrapper | `render_status_dashboard.py`, CLI tests | CLI supports `--dry-run`, `--stage <dir>`, JSON output and non-zero exit for validation errors. |
| `T10-Q-M13` | Integrate staged dashboard with renderer | `infrastructure.py`, `templates.py`, renderer tests | Dashboard files are staged under `.codex/product-agent-os/` only through an opt-in dashboard path or explicit status dashboard CLI; baseline `required_templates()` rendering does not silently add dashboard files to every infrastructure render. |
| `T10-Q-M14` | Extend stage manifest and merge safety coverage | `stage_manifest.py`, merge tests | Dashboard artifacts are covered by stage manifest digests or an equivalent dashboard manifest; no direct target writes, path escape is blocked, stale digest blocks apply and existing approval flow protects dashboard apply. |
| `T10-Q-M15` | Add fixture eval coverage | `run_fixture_eval.py`, fixtures/eval tests | Fixture eval reports `question_queue_contract_present`, `status_snapshot_present`, `status_dashboard_present`, `dashboard_no_external_assets`, `question_budget_false_positive_guard_present`, `dashboard_not_source_of_truth`, and `stale_evidence_no_success_claim`. |
| `T10-Q-M16` | Add false-positive and abuse fixtures | fixture directories, fixture eval tests | Simple docs, mechanical maintenance, inspection-only work and mature existing control-plane work do not trigger broad interviews or dashboard success claims; malicious/secret-like answers, stale ledger answers and oversized question queues are rejected or trimmed safely. |
| `T10-Q-M17` | Update lifecycle skills | skills, `test_lifecycle_skills.py` | Skills consume typed question packets as `next_blocking_question` plus counts, ask at most one blocking question, keep optional questions in the packet, route answers into artifacts or accepted gaps and avoid broad interview loops. |
| `T10-Q-M18` | Update behavioral eval contracts | `behavioral-workflows.json`, tests | Behavioral evals forbid "ask every methodology question", hidden scaffold, dashboard-as-source-of-truth, full queue dumps in first response, and success from stale or inspection-only evidence. |
| `T10-Q-M19` | Add transcript eval session | transcript fixture, transcript tests | Synthetic session checks guided question flow and dashboard status language without private data. |
| `T10-Q-M20` | Update Product-Agent OS docs | docs and README | Docs explain question protocol, answer ledger, dashboard, source-of-truth boundary and user workflow. |
| `T10-Q-M21` | Update root control-plane evidence | `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` | Root files record Track 10 scope, acceptance, verification and residual risks after Task 22 closure. |
| `T10-Q-M22` | Update source registry and backlog | `docs/sources/registry.md`, `docs/sources/product-agent-os-track-10-backlog.md`, docs checks | Registry records local implementation sources and verification evidence; create Track 10 backlog if absent, capture deferred dashboard/editor capabilities, and update MkDocs/docs checks if new docs pages are added. |
| `T10-Q-M23` | Run focused verification | focused test commands | Question, runtime, dashboard, renderer, lifecycle and docs tests pass. |
| `T10-Q-M24` | Run full Product-Agent OS verification | full tests/evals/docs commands | Full unit suite, fixture eval, transcript eval, Codex compatibility, docs check and diff hygiene pass. |
| `T10-Q-M25` | Keep commit/push explicit-only | Git | Do not stage, commit, push or create PR unless the user explicitly asks after verification. |

## Task 24: Self-Verification And Modernization Loop

Task 24 adds a staged control-plane capability for Product-Agent OS to evaluate the agents, skills, prompt or policy packs, router/tool policies and harness versions that were created or used during real user work. The mechanism is not an autonomous mutation system. It reads implemented task evidence, optional redacted traces and synthetic regression cases; computes per-target scorecards; stages daily and weekly review packets; and generates modernization candidates only when evidence, rollback and approval state are explicit.

Design input comes from the local `agentic_harness_metrics.md` research brief and from the implemented Track 9/Track 10 contracts. The implementation must reuse existing boundaries: `agent_eval_workflow_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, redaction policy, staged renderer behavior, status snapshot, offline dashboard, fixture eval runner, transcript eval runner and explicit-only git boundary.

Task 24 product outcome:

- show a registry of evaluated targets with status `healthy`, `watch`, `regression`, `blocked` or `no_data`;
- separate agent outcome metrics, trajectory metrics, harness reliability metrics and skill-specific metrics;
- explain the recommended self-verification cadence with `L0`, `L1`, `L2` or `L3` maturity;
- preserve an append-only scorecard ledger with raw counts, confidence evidence, baseline, current and candidate versions;
- generate an offline HTML evaluation report as a review artifact, not an approval record or source of truth;
- stage modernization candidates with reason, expected impact, risk, rollback target and approval state;
- keep active schedules, external eval systems, live model calls, Agents SDK apps, GitHub Actions, MCP activation and write updates approval-bound.

Task 24 implementation surfaces:

- Create: `plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics_report.py`
- Create: `plugins/product-agent-os/scripts/render_agent_skill_metrics_report.py`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/agent-skill-metrics-loop.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/agent-skill-daily-eval-report.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/agent-skill-weekly-verification.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/agent-skill-scorecard-ledger.md`
- Create: `plugins/product-agent-os/assets/templates/artifact-templates/agent-skill-update-candidate.md`
- Create: `plugins/product-agent-os/assets/templates/reports/agent-skill-evaluation-report.html`
- Create: `plugins/product-agent-os/assets/templates/automations/daily-agent-skill-eval.md`
- Create: `plugins/product-agent-os/assets/templates/automations/weekly-agent-skill-verification.md`
- Create: focused tests for registry, evidence intake, redaction, scorecard, report rendering, CLI, fixtures and lifecycle wording.
- Modify: `discovery.py`, `methodology_audit.py`, `codex_runtime_runner/contracts.py`, `codex_runtime_runner/routes.py`, `templates.py`, `status_snapshot.py`, `status_dashboard.py`, `run_fixture_eval.py`, lifecycle skills, Product-Agent OS docs and root control-plane files.

Task 24 implementation matrix:

| ID | Task | Files | Acceptance |
| --- | --- | --- | --- |
| `T10-SV-M-1` | Run Task 24 baseline audit | existing source inventory, Task 23 evidence | Confirm Task 23 is closed, no `agent_skill_metrics_loop` implementation exists, and reusable surfaces are available: status snapshot, dashboard renderer, redaction, fixture eval, transcript eval, `agent-eval-workflow.md`, `skill-promotion-record.md`, `trace-evidence-packet.md`, `eval-run-report.md`, `automation-candidate.md`. |
| `T10-SV-M0` | Add Task 24 planning closure | this plan, Track 10 backlog | Task 24 description, implementation surfaces, matrix, risks and verification expectations are documented before implementation. |
| `T10-SV-G1` | Enforce reuse-first implementation boundary | this plan, implementation notes, focused tests | Implementation must modernize existing Product-Agent OS primitives before adding new subsystems: reuse `codex_runtime_runner/redaction.py`, `question_protocol.py`, `status_snapshot.py`, `status_dashboard.py`, `automation_policy.py`, runtime contracts/routes, fixture eval runner, transcript eval runner and existing agentic workflow artifacts. New code is limited to metrics-loop domain logic, report rendering and CLI surfaces. |
| `T10-SV-G2` | Add source-priority and source-of-truth policy | `test_agent_skill_metrics.py`, docs | Tests define source priority: explicit control-plane artifacts, run records, trace/eval packets and accepted gaps are evidence; dashboard/report HTML is a generated review view only; memory, raw chat logs and unsupported community claims are not source of truth. |
| `T10-SV-G3` | Add metrics packet bounds and schema contract | `test_agent_skill_metrics.py`, `agent_skill_metrics.py` | Metrics packets have schema version, max target count, max evidence records, max questions, max update candidates, max embedded JSON size and deterministic trimming with warning fields; oversized packets cannot reach runtime route, report renderer or dashboard summary unbounded. |
| `T10-SV-G4` | Add trace data-classification gate | `test_agent_skill_metrics.py`, `data-classification-register.md` reuse | Real trace or real customer/task evidence requires `data-classification-register.md`, `secrets-policy.md` or explicit accepted gap before dataset ingestion; synthetic fixtures remain allowed when marked synthetic. |
| `T10-SV-G5` | Add shared offline artifact safety helper | `offline_artifact_safety.py`, `status_dashboard.py`, `agent_skill_metrics_report.py`, tests | Status dashboard and metrics report share one helper for HTML escaping, embedded JSON safety, no external URL/CDN checks, redaction validation, size bounds and generated-view-only wording; do not fork private dashboard helpers into the metrics report renderer. |
| `T10-SV-G6` | Add no-baseline-renderer-pollution gate | `templates.py`, infrastructure tests, fixture eval | Metrics reports and daily/weekly automation candidates are opt-in staged artifacts only; baseline `required_templates()` or default infrastructure rendering must not silently add eval reports or automation candidates to every project render. |
| `T10-SV-M1` | Add target registry contract tests | `test_agent_skill_metrics.py` | Tests define `target_id`, target type, owner, version, risk level, expected artifacts, eval suite, source artifacts, maturity level, usage volume, tool permission level, production-impact flag and no-data status. |
| `T10-SV-M2` | Implement target registry collector | `agent_skill_metrics.py` | Collector finds local agents, skills, prompt or policy packs, subagent teams, router/tool policy evidence, model/reasoning policy, sandbox/approval policy, automation candidates and harness versions from project artifacts without external calls or target workspace writes. |
| `T10-SV-M3` | Add implemented-task evidence intake tests | `test_agent_skill_metrics.py`, synthetic fixtures | Tests cover `RUNLOG.md`, `TEST.md`, `EVALS.md`, fixture eval summaries, transcript eval summaries, generated artifacts, failed verification evidence, stale evidence, explicit accepted gaps and evidence source priority. |
| `T10-SV-M4` | Implement evidence intake | `agent_skill_metrics.py` | Intake produces a bounded evidence packet from explicit project artifacts only; memory, raw chat logs, dashboard HTML and metrics report HTML are not treated as source of truth. |
| `T10-SV-M5` | Add trace intake and normalization tests | `test_agent_skill_metrics.py`, trace fixtures | Tests cover OpenAI Agents SDK trace shape, OpenTelemetry GenAI span shape, tool-specific reports and accepted-gap traces with `trace_source_type`, required span types, missing span types, trace ids, group ids and replayability fields. |
| `T10-SV-M6` | Implement trace intake normalizer | `agent_skill_metrics.py`, existing `trace-evidence-packet.md` | Normalizer maps supported trace evidence into a portable trace packet and labels unsupported or incomplete traces without live Agents SDK, MCP, network or external eval calls. |
| `T10-SV-M7` | Add redaction gate tests | `test_agent_skill_metrics.py`, redaction fixtures | Secret-like text, raw private chat markers, local user paths, raw prompts, tool outputs and private customer data are blocked or redacted before dataset, ledger or report generation. |
| `T10-SV-M8` | Implement metrics redaction gate | `agent_skill_metrics.py`, existing redaction helpers | Every metrics packet includes redaction summary; scoring, report rendering and update candidates are blocked when redaction fails. |
| `T10-SV-M9` | Add evidence dataset builder tests | `test_agent_skill_metrics.py` | Builder creates stratified groups for implemented tasks, real-trace sample, prior failures, critical slices, edge/adversarial cases, holdout, synthetic regression cases and known flaky cases. |
| `T10-SV-M10` | Implement evidence dataset builder | `agent_skill_metrics.py` | Dataset builder records source counts, split labels, duplicate/leakage status and avoids overfitting by keeping holdout and prior-failure labels separate. |
| `T10-SV-M11` | Add dataset quality gate tests | `test_agent_skill_metrics.py` | Tests cover `dataset_coverage`, `dataset_duplicate_rate`, leakage check, missing expected splits, low real-trace coverage and insufficient sample statuses. |
| `T10-SV-M12` | Implement dataset quality gates | `agent_skill_metrics.py` | Dataset gates block confident decisions when duplicates, leakage, missing holdout, insufficient sample or missing critical slices exceed thresholds. |
| `T10-SV-M13` | Add grader runner contract tests | `test_agent_skill_metrics.py` | Tests define metric graders, trace graders, human audit sample and optional LLM-as-judge as metadata-only/local contract; live model calls are not introduced in Track 10. |
| `T10-SV-M14` | Implement grader runner adapter | `agent_skill_metrics.py` | Adapter consumes existing local eval outputs and manual/human audit labels, records grader type, rubric id, sample size and unsupported live judge gaps without external calls. |
| `T10-SV-M15` | Add judge calibration tests | `test_agent_skill_metrics.py` | Tests cover `judge_human_agreement`, `judge_precision`, `judge_recall`, `cohen_kappa`, calibration sample size and `judge_not_calibrated` blocking status. |
| `T10-SV-M16` | Implement judge calibration summary | `agent_skill_metrics.py` | Calibration summary is required before judge-derived metrics can approve candidates; missing calibration remains a reportable gap. |
| `T10-SV-M17` | Add metric schema tests | `test_agent_skill_metrics.py` | Tests require separate outcome, trajectory, harness reliability, harness optimizer, skill, cost/latency and safety sections with numerator and denominator fields. |
| `T10-SV-M18` | Implement metric aggregation | `agent_skill_metrics.py` | Aggregator computes task success, regression-free success, final state accuracy, tool selection/argument accuracy, instruction violation, trace completeness, false-pass, false-fail, flake, replayable trace, cost, latency and skill trigger/adherence metrics when evidence exists. |
| `T10-SV-M19` | Add repeatability metrics tests | `test_agent_skill_metrics.py` | Tests cover `pass@k`, `pass^k`, replay success, repeated-run instability and no lucky-run promotion from a single successful run. |
| `T10-SV-M20` | Implement repeatability calculations | `agent_skill_metrics.py` | Repeatability metrics are calculated only when replay evidence exists and are surfaced as insufficient data otherwise. |
| `T10-SV-M21` | Add scorecard formula tests | `test_agent_skill_metrics.py` | Tests cover Harness Quality Score, Agentic Task Score and Harness Optimization Score components, weights, missing-data behavior and safety guardrails. |
| `T10-SV-M22` | Implement scorecard calculators | `agent_skill_metrics.py` | Scorecards compute bounded component scores and never hide blocking safety, false-pass, flake, trace or cost regressions behind a headline average. |
| `T10-SV-M23` | Add confidence and gate tests | `test_agent_skill_metrics.py` | Tests cover Wilson lower bound, delta comparison, bootstrap CI if available, insufficient sample, critical regression, false-pass threshold, flake threshold, trace completeness threshold, cost regression and safety violation. |
| `T10-SV-M24` | Implement confidence and decision gates | `agent_skill_metrics.py` | Weekly acceptance requires confidence evidence, zero critical regressions, bounded false-pass and flake rates, trace completeness, cost guardrail, no high-risk instruction/approval violation and owner review or explicit gap. |
| `T10-SV-M25` | Add cadence recommendation tests | `test_agent_skill_metrics.py` | Tests cover `L0`, `L1`, `L2`, `L3` routing from usage volume, risk level, tool permissions, production impact, flakiness, trace coverage, automation candidates and owner override. |
| `T10-SV-M26` | Implement cadence recommender | `agent_skill_metrics.py` | Recommender explains daily, weekly, on-change and incident-triggered cadence as suggested policy only; active schedules remain approval-bound. |
| `T10-SV-M27` | Add run record schema tests | `test_agent_skill_metrics.py` | Tests require run id, timestamp, cadence, window, dataset split, target, versions, model, reasoning effort, repo sha or accepted gap, environment, trace metadata, artifacts, scores, statistical evidence, cost/latency, update decision and review fields. |
| `T10-SV-M28` | Implement run record builder | `agent_skill_metrics.py` | Builder emits deterministic JSON-ready records with redacted evidence and no absolute user paths, secrets, private chat logs or dashboard-as-source claims. |
| `T10-SV-M29` | Add scorecard ledger template tests | `test_infrastructure_templates.py`, `test_agent_skill_metrics.py` | Ledger template requires append-only policy, baseline/current/candidate versions, raw counts, confidence intervals, cost, latency, evidence links, redaction status, run record ids, report anchors and no-secrets policy. |
| `T10-SV-M30` | Implement scorecard ledger renderer | `agent_skill_metrics.py`, `agent-skill-scorecard-ledger.md`, `templates.py` | Renderer emits deterministic JSON or Markdown-ready records and never overwrites existing target project evidence directly. |
| `T10-SV-M31` | Add daily report tests | `test_agent_skill_metrics.py` | Daily packet reports per-target status and recommendations: no-op, investigate, block promotion, stage candidate for review or request human audit; it never auto-fixes from one noisy run. |
| `T10-SV-M32` | Implement daily report builder | `agent_skill_metrics.py`, `agent-skill-daily-eval-report.md` | Daily report summarizes evidence window, deployed target inventory, trace source mix, changed versions, failure groups, evidence gaps, confidence status and next safe action. |
| `T10-SV-M33` | Add weekly verifier tests | `test_agent_skill_metrics.py` | Weekly packet compares 7-day rolling window, baseline, previous week and holdout; audits false passes, replays flaky cases and separates regression findings from update candidates. |
| `T10-SV-M34` | Implement weekly verifier | `agent_skill_metrics.py`, `agent-skill-weekly-verification.md` | Weekly verifier blocks update acceptance without rollback target, owner review, current evidence, holdout check, false-pass audit, flake replay and cost regression check. |
| `T10-SV-M35` | Add component prioritization tests | `test_agent_skill_metrics.py` | Tests rank likely improvement components: prompt, skill, agent config, router, tool policy, memory policy, logging, dataset, grader, harness or approval policy. |
| `T10-SV-M36` | Implement component prioritization | `agent_skill_metrics.py` | Prioritizer uses failure taxonomy, affected metrics and evidence sufficiency to explain why a component should be changed, deferred or left unchanged. |
| `T10-SV-M37` | Add modernization candidate tests | `test_agent_skill_metrics.py` | Candidates require reason, metric deltas, affected targets, component priority, expected impact, risk, approval state, rollback target, no external write action and no headline-only improvement. |
| `T10-SV-M38` | Implement modernization candidate generator | `agent_skill_metrics.py`, `agent-skill-update-candidate.md` | Generator emits staged candidates for skill, agent, prompt, router, tool policy, memory policy, dataset, grader or harness updates and cannot apply patches by itself. |
| `T10-SV-M39` | Add report manifest and archive tests | `test_agent_skill_metrics_report.py` | Tests require `report_id`, generated_at, project id or redacted id, eval window, cadence, source datasets, trace sources, redaction status, current report path and optional timestamped archive policy. |
| `T10-SV-M40` | Add unified HTML report tests | `test_agent_skill_metrics_report.py` | Tests assert one self-contained report under `.codex/eval-reports/agent-skill-evaluation-report.html`, embedded redacted JSON, anchors by target, no external URLs, no secrets, bounded embedded payload, numerator/denominator for every metric, insufficient-data banners, previous/current/candidate comparisons and no approval claim. |
| `T10-SV-M41` | Implement unified HTML report renderer | `agent_skill_metrics_report.py`, `reports/agent-skill-evaluation-report.html` | Renderer creates a reviewable offline report with manifest, executive verdict, target inventory, metrics, version comparison, improvements, regressions, skill analysis, trajectory analysis, trace evidence, update candidates and raw redacted appendix. |
| `T10-SV-M42` | Add CLI dry-run and stage tests | `test_agent_skill_metrics_cli.py` | CLI supports `--dry-run`, `--stage <dir>`, `--window`, `--cadence`, JSON output, validation errors and no target workspace writes by default. |
| `T10-SV-M43` | Implement CLI wrapper | `render_agent_skill_metrics_report.py` | CLI returns stable JSON and stages report artifacts only under the requested stage root, including current report and optional archive copy only inside stage root. |
| `T10-SV-M44` | Register templates and stage artifacts | `templates.py`, infrastructure tests | Metrics loop templates, daily/weekly reports, scorecard ledger, update candidate, eval report template and candidate automation templates are registered with safe target paths under `.codex/artifact-templates/`, `.codex/eval-reports/` and `.codex/automation-candidates/`; default baseline rendering does not silently include eval reports or automation candidates. |
| `T10-SV-M45` | Add automation candidate validator updates | `automation_policy.py`, `test_automation_policy.py` | Daily/weekly metrics automation candidates validate as candidate-only, require manual stability evidence and never create active schedules, GitHub Actions, Codex App automations or external workflows. |
| `T10-SV-M46` | Integrate status snapshot summary | `status_snapshot.py`, `status_dashboard.py`, tests | Status snapshot includes bounded metrics-loop summary and report references while preserving dashboard generated-view-only, stale-evidence and not-source-of-truth policies. |
| `T10-SV-M47` | Add discovery readiness gate | `discovery.py`, `project-readiness.json`, tests | `agent_skill_metrics_loop` is applicable when agents, skills, subagents, automation candidates, router/tool policies, prompt/policy packs or harness versions are detected; docs-only and simple maintenance false positives remain not applicable. |
| `T10-SV-M48` | Add methodology audit recommendations | `methodology_audit.py`, tests | Missing metrics loop produces a high-risk recommendation only for real agentic surfaces; detection alone remains `present_unverified` until current evidence, owner, cadence and approval boundary exist. |
| `T10-SV-M49` | Add runtime packet validation | `codex_runtime_runner/contracts.py`, runtime tests | Route packet can carry bounded metrics-loop status, report reference, cadence recommendation, update candidate summary and finish options without breaking schema-v1 compatibility. |
| `T10-SV-M50` | Add runtime route behavior | `codex_runtime_runner/routes.py`, runtime tests | Runtime can recommend stage metrics report, request owner review, block automation promotion, keep current or investigate regression; it cannot offer apply/update actions without approval. |
| `T10-SV-M51` | Add guided question integration | `question_protocol.py`, question tests | Question queue asks at most one blocker about owner, evidence source, trace source, cadence, approval, rollback or accepted gap; optional metrics-loop questions stay in the packet. |
| `T10-SV-M52` | Update lifecycle skills | lifecycle skills, `test_lifecycle_skills.py` | Skills route self-verification as staged evidence and reject autonomous mutation, active schedules, live eval calls, dashboard-as-proof claims and modernization without rollback. |
| `T10-SV-M53` | Add fixture eval coverage | `run_fixture_eval.py`, fixture tests | Fixture eval exposes `agent_skill_metrics_loop_contract_present`, `metrics_report_redacted`, `trace_normalization_contract_present`, `judge_calibration_gate_present`, `scorecard_ledger_contract_present`, `source_priority_contract_present`, `metrics_packet_bounds_present`, `trace_data_classification_gate_present`, `offline_artifact_safety_shared`, `no_baseline_renderer_pollution`, `update_candidate_rollback_required`, `active_metrics_automation_blocked` and `metrics_loop_false_positive_guards_present`. |
| `T10-SV-M54` | Add false-positive and abuse fixtures | fixture directories | Docs-only work, simple maintenance, no deployed targets, stale evidence, headline-only improvement, private-data evidence, judge-not-calibrated evidence and trace-missing-span cases do not produce unsafe readiness or update claims. |
| `T10-SV-M55` | Add behavioral eval contracts | `behavioral-workflows.json`, tests | Behavioral evals forbid headline-metric-only approval, self-applied updates, active automation, live eval calls, dashboard success claims, raw trace leakage, uncalibrated judge approval and update candidates without rollback. |
| `T10-SV-M56` | Add transcript eval sessions | transcript fixtures, transcript tests | Synthetic sessions cover self-verification request, regression finding, no-data target, trace-missing-span target, judge-not-calibrated gap, approval-required modernization and automation-candidate-only flow. |
| `T10-SV-M57` | Add Task 24 execution batches | this plan | Batch plan groups work into foundation, trace/dataset/judge, metrics/gates, reports/CLI/templates, runtime/lifecycle/evals and docs/full verification without mixing with completed Task 23 batches. |
| `T10-SV-M58` | Update Product-Agent OS docs | docs, README, source registry | Docs explain metrics loop, target registry, trace intake, dataset quality, grader/judge calibration, cadence recommendation, scorecard ledger, report, update candidates, approval boundary and source-of-truth policy. |
| `T10-SV-M59` | Update root control-plane evidence | `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` | Root files record Task 24 scope, acceptance, verification evidence, residual risk and explicit-only git boundary. |
| `T10-SV-M60` | Run focused verification | focused test commands | New registry, trace, dataset, grader, metrics, report, CLI, automation-policy, fixture, lifecycle, transcript and docs tests pass before broad verification. |
| `T10-SV-M61` | Run full Product-Agent OS verification | full checks | Full unit suite, fixture eval, transcript eval, Codex compatibility, docs check, strict MkDocs when docs/nav-sensitive changes are made and diff hygiene pass. |
| `T10-SV-M62` | Keep commit/push explicit-only | Git | Do not stage, commit, push or create PR unless the user explicitly asks after verification. |

Task 24 implementation batches:

- **Batch 7: Foundation And Registry** (`T10-SV-M-1..M4`, plus reuse/source/bounds guardrails `T10-SV-G1..G3`)
- **Batch 8: Trace, Redaction, Dataset And Judge Contracts** (`T10-SV-M5..M16`)
- **Batch 9: Metrics, Scorecards, Confidence And Cadence** (`T10-SV-M17..M28`)
- **Batch 10: Ledger, Reports, Candidates And CLI** (`T10-SV-M29..M45`, plus trace-classification/offline-artifact/rendering guardrails `T10-SV-G4..G6`)
- **Batch 11: Runtime, Discovery, Lifecycle And Eval Coverage** (`T10-SV-M46..M57`)
- **Batch 12: Docs, Control Plane And Full Verification** (`T10-SV-M58..M62`)

Batch 11 status: implemented on 2026-05-28 with focused RED/GREEN coverage for status snapshots, discovery, methodology audit, runtime packets/routes, guided questions, lifecycle skills, fixture eval, behavioral eval and transcript sessions. Batch 12 is closed with docs/control-plane/full-verification evidence. Task 25 Batch 13 is implemented with file-level graph foundation, Task 25 Batch 14 is implemented with Python AST scanner overlays, conservative dependency edges, structured overlays, partition scopes, canonical aliases and bounded readiness metadata, Task 25 Batch 15 is implemented with graph query packets, query CLI mode, runtime/status/lifecycle graph summaries and bounded analysis reports, Task 25 Batch 16 is implemented with generated cockpit visualization, Graphology-compatible static projection, local vendor boundary, selected evidence, fallback tables and mobile/no-external-assets rendering, Task 25 Batch 17 is implemented with fixture structural fields, local search-quality evals and future backend/semantic gates, Task 25 Batch 18 is closed with `T10-CG-V2-M31..M32` focused/full verification, Task 25 Batch 19 is implemented with `T10-CG-V2-M33..M38` offline static search index after explicit user approval, Task 25 Batch 20 is implemented with `T10-CG-V2-M39..M44` local query backend gate after explicit user approval, and Task 25 Batch 21 is implemented with `T10-CG-V2-M45..M51` semantic retrieval, embeddings cache metadata and cross-encoder eval after explicit user approval. Batch 22 through Batch 23 are future-gated extension batches that require explicit approval before implementation.

## Task 25: Project Code Graph And HTML Cockpit Visualization

Task 25 adds a staged, read-only mechanism for scanning a user project, building a graph of dependent code and documentation entities, and rendering that graph into the Product-Agent OS HTML cockpit. It closes the gap between the existing workspace discovery model, which is mostly file/path/marker based, and the user-visible need for a dependency map that helps both humans and coding agents find relevant code faster.

The mechanism must not become a live IDE, database, autonomous editor or source-of-truth replacement. Source code, checked-in docs and generated JSON/JSONL graph artifacts remain the evidence layer. HTML is a generated review surface.

Task 25 product outcome:

- scan a workspace without mutating it and produce `.codex/product-agent-os/project-code-graph.json`;
- represent project entities as stable nodes: workspace, package, module/file, class, function, method, test, fixture, template, generated artifact, Markdown page, MkDocs page, OpenAPI/Swagger or AsyncAPI contract, DBML or SQL schema, Mermaid/PlantUML diagram and control-plane artifact;
- represent dependencies as confidence-labelled edges: `contains`, `imports`, `calls`, `exports`, `tests`, `verifies`, `documents`, `renders`, `generates`, `configures`, `owns`, `references` and `impacts`;
- expose compact agent query packets for `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `read_order`, `hotspots`, `node`, `status` and `search`;
- expose graph freshness, workspace/worktree provenance, validation, analysis report and code-flow views so humans and agents can distinguish current evidence from stale, cross-worktree, unsupported or inferred topology;
- expose observation lineage, scan-to-scan deltas and advisory temporal validity so removed or changed dependencies are invalidated/superseded in generated graph artifacts rather than silently erased;
- render a generated eight-page project cockpit shell with top-level pages `Overview`, `Project Map`, `Docs & Sources`, `Code Intelligence`, `Contracts`, `Quality & Metrics`, `Operations & Risk` and `Proposal Ledger`, while preserving all detailed sections as local page sections;
- render an offline HTML project cockpit graph with filters, clustering and level-of-detail so 1k, 5k and 10k node graphs stay navigable;
- produce a Graphology-compatible visual projection with layout, size, color, community, label-priority and level-of-detail metadata derived from the canonical graph artifact, not from browser state;
- initialize a local Sigma-based interactive renderer when bundled assets are available, with selected-node evidence, filter state, graph navigation commands, mobile behavior and static fallback views;
- keep graph visualization assets local. `graphology` and `sigma.js` may be used only when vendored or locally bundled; no CDN, network fetch or external runtime dependency is allowed.

Task 25 future-gated extension analysis:

- Product reason: the Batch 13-18 baseline is enough for safe navigation, source orientation and agent read-order. Static indexes, runtime backends and semantic extraction become useful only when users need repeated low-latency search over larger graphs, better natural-language retrieval or summarized rationale across code/docs. These are product accelerators, not baseline correctness requirements.
- Product risk: each extension can make generated graph output look more authoritative than source. The UI and runtime must keep "generated orientation evidence" wording, stale/fresh labels, source-read safe next actions and owner-review gates visible.
- Technical reason for sequencing: a static search index should come before any live database/server because it proves index schema, freshness, cache invalidation and search-quality thresholds without process lifecycle risk. A local backend should come before embeddings because it provides stable storage/query contracts and rollback controls. Embeddings and cross-encoder reranking should come before LLM extraction because they can be evaluated with deterministic retrieval metrics before introducing generative interpretation.
- Technical risk: live server/database work adds process lifecycle, port, persistence, cleanup, concurrency, API contract and rollback risks. Embedding/cross-encoder/LLM work adds privacy, cost, latency, model drift, cache invalidation, dataset leakage, false-positive semantic links and unsupported completion-claim risks.
- Approval gate: Batch 19 was approved by the explicit user request to execute Batch 19 and is limited to an offline static search index. Batch 20 was approved by the explicit user request to execute Batch 20 and is limited to a generated local file-store backend gate with disabled-by-default server lifecycle, no production server and graph-only fallback. Batch 21 was approved by the explicit user request to execute Batch 21 and is limited to a generated semantic retrieval index using local deterministic embeddings/cross-encoder eval, redacted graph/static-index inputs, cache policy, token budget, eval threshold and rollback/disable path. Batch 22 through Batch 23 remain `approval_required` before implementation. Approval must name allowed surfaces, data classification, redaction boundary, cache policy, token budget, eval threshold, rollback/disable path, owner and accepted residual risks. Planning matrix presence is not implementation evidence.
- Source boundary: approved Batch 21 semantic retrieval artifacts are generated orientation evidence only. Semantic hits are `present_unverified`, point back to graph observation IDs, source spans, redaction status and current-run eval evidence, and do not rewrite canonical graph edges. Future LLM semantic nodes, rationale snippets or comment summaries are never source of truth.
- Stop condition: do not start live database/server, live model/API calls beyond the approved local deterministic Batch 21 surface, semantic extraction or rationale/comment extraction from Task 25 baseline closure alone. Start only when the explicit approval packet exists and the RED tests for that future batch are written first.

Task 25 implementation surfaces:

- Create: `plugins/product-agent-os/scripts/product_agent_os/project_code_graph.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/project_graph_manifest.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/project_graph_analysis.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/project_graph_queries.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/project_graph_search.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/project_graph_adapters.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/project_graph_observations.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/project_graph_ontology.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/project_graph_chunking.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/project_cockpit_model.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/project_graph_renderer.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/project_graph_visual_model.py`
- Future-gated create: `plugins/product-agent-os/scripts/product_agent_os/project_graph_index.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/project_graph_backend.py`
- Create: `plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py`
- Future-gated create: `plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py`
- Create: `plugins/product-agent-os/scripts/scan_project_code_graph.py`
- Create: `plugins/product-agent-os/assets/templates/project-graph/project-cockpit.html`
- Create: `plugins/product-agent-os/assets/templates/project-graph/project-graph.html`
- Create: `plugins/product-agent-os/assets/templates/project-graph/project-code-flow.html`
- Create: `plugins/product-agent-os/assets/templates/project-graph/project-graph.css`
- Optional create after local-bundle decision: `plugins/product-agent-os/assets/vendor/graphology/` and `plugins/product-agent-os/assets/vendor/sigma/`
- Modify: `discovery.py`, `status_snapshot.py`, `status_dashboard.py`, `codex_runtime_runner/contracts.py`, `codex_runtime_runner/routes.py`, `run_fixture_eval.py`, lifecycle skills, Product-Agent OS docs and root control-plane files.

Task 25 implementation matrix:

| ID | Task | Files | Acceptance |
| --- | --- | --- | --- |
| `T10-CG-V2-M01` | Baseline audit and planning closure | existing discovery, status dashboard, ignored `.understand-anything` graph, this plan, root control-plane files | Confirm Product-Agent OS currently has file-based discovery but no supported dependency graph scanner, query API or HTML code graph renderer; Task 25 scope, batches, risks, verification expectations and non-goals are documented before implementation. |
| `T10-CG-V2-M02` | Graph schema, ontology and validator | `project_code_graph.py`, `project_graph_ontology.py`, tests | Node, edge, source span, artifact, confidence, status, language support, graph metadata, ontology registration and ID/label/count bounds are deterministic and validated. |
| `T10-CG-V2-M03` | Stable IDs, manifest, freshness and provenance | `project_graph_manifest.py`, scanner/query/status tests | Node IDs and file fingerprints stay stable across unchanged runs; manifest records root fingerprint, branch/commit/worktree when available, build metadata, unchanged/changed/added/deleted sets and stale/current status. |
| `T10-CG-V2-M04` | Read-only stage, ignore policy and path safety | `scan_project_code_graph.py`, scanner/export safety tests | Scanner never mutates the target workspace; dry-run prints JSON; staged writes stay inside explicit stage root; generated/low-value files are safely classified; shrink guard and backup behavior prevent silent destructive overwrites. |
| `T10-CG-V2-M05` | Privacy, redaction and source boundary | graph artifact, renderer and docs tests | Graph artifacts exclude raw file bodies by default, redact local absolute paths and secret-like values, store spans/fingerprints only and keep HTML as generated review output rather than source of truth. |
| `T10-CG-V2-M06` | Observation ledger and temporal invalidation | `project_graph_observations.py`, manifest/delta tests | Every node/edge can point to deterministic observation records with scan ID, relative path, span, fingerprint, extractor, confidence and redaction status; removed or changed dependencies are invalidated or superseded rather than silently erased. |
| `T10-CG-V2-M07` | Synthetic and scale fixtures | fixture dirs, fixture tests | Minimal Python, docs-heavy, mixed docs/contracts and 1k/5k/10k synthetic graph fixtures validate graph contracts and scale bounds without forcing all nodes into prompts or first render. |
| `T10-CG-V2-M08` | Python package, module and symbol scanner | scanner tests | Python package roots, modules, files, classes, functions and methods become stable nodes with source spans and `contains`/parent edges. |
| `T10-CG-V2-M09` | Imports, calls and conservative resolver | scanner/resolver tests, `project_graph_adapters.py` | Absolute/relative imports and resolvable direct calls create confidence-labelled edges; ambiguous calls, callbacks, events, observers and interface/override heuristics stay bounded and are never guessed as verified. |
| `T10-CG-V2-M10` | Tests, fixtures and smoke scan | scanner tests, smoke test | Test files, fixture files and eval fixtures link to implementation targets when naming/import evidence exists; Product-Agent OS package scan produces a non-empty graph with modules, functions, imports and calls. |
| `T10-CG-V2-M11` | Unsupported language and adapter extension point | scanner/query tests, `project_graph_adapters.py` | Non-Python code is represented at file/module level until parser support exists; framework/language adapters are optional extension points with confidence labels and no false completeness claims. |
| `T10-CG-V2-M12` | Docs, contracts, schemas and diagrams overlays | docs/contract/schema/diagram scanner tests, `project_graph_chunking.py` | MkDocs, Markdown, OpenAPI/Swagger, AsyncAPI, DBML, SQL, JSON/YAML, Mermaid and PlantUML inputs become structured nodes/chunks/edges where parseable and explicit references exist. |
| `T10-CG-V2-M13` | Methodology, readiness, partitions and aliases | discovery/status/query tests, `project_graph_ontology.py` | Graph summaries expose methodology gates, accepted gaps and readiness status at bounded depth; workspace/repository/worktree/package/docs/artifact scopes and canonical aliases prevent unrelated partitions from polluting agent context. |
| `T10-CG-V2-M14` | Query engine and CLI | `project_graph_queries.py`, `scan_project_code_graph.py`, CLI tests | `neighbors`, `path`, `node`, `status`, `search`, `hotspots` and `read_order` run from graph JSON/JSONL without loading source text and produce deterministic JSON output for humans and agents. |
| `T10-CG-V2-M15` | Budgeted query packets and filter safety | `project_graph_queries.py`, runtime/CLI safety tests | Query packets enforce token/output budgets, omitted counts, hub suppression, context filters, seed scoring, truncation metadata, query length limits and validated node/edge/confidence/partition/path filters. |
| `T10-CG-V2-M16` | Read order, trace, delta and impact packets | `project_graph_queries.py`, CLI tests | Read-order, `trace`, `impact`, `affected_tests`, `as_of_scan`, `changed_since`, `invalidated_edges`, `new_edges` and `why_changed` packets are bounded, confidence-labelled and deterministic. |
| `T10-CG-V2-M17` | Runtime, status and lifecycle integration | `status_snapshot.py`, `status_dashboard.py`, codex runtime runner, lifecycle skill tests | Status/runtime packets carry bounded graph freshness, counts, unsupported languages, artifact references, top gaps and safe next action without schema-v1 breakage; stale, ambiguous or unsupported graph output routes agents back to source reads or owner questions. |
| `T10-CG-V2-M18` | Analysis report | `project_graph_analysis.py`, report tests | Report surfaces god nodes, hotspots, surprising cross-module links, ambiguous edge inventory, unsupported-language summary and suggested agent questions. |
| `T10-CG-V2-M19` | Cockpit information architecture and eight-page shell | `project_cockpit_model.py`, `project_graph_renderer.py`, `project-cockpit.html`, template tests | Renderer exposes exactly eight top-level pages and maps all detailed sections into those pages exactly once; active page and optional section anchor remain stable. |
| `T10-CG-V2-M20` | Cockpit page content contracts | `project_cockpit_model.py`, renderer tests | `Overview`, `Project Map`, `Docs & Sources`, `Code Intelligence`, `Contracts`, `Quality & Metrics`, `Operations & Risk` and `Proposal Ledger` each expose their role, source links, stale flags, graph/query packets, approval boundaries and action surfaces. |
| `T10-CG-V2-M21` | Offline renderer and no-external-assets gate | `project_graph_renderer.py`, `project-graph.html`, `project-graph.css`, renderer tests | Offline HTML/CSS/JS contains no CDN URLs, external scripts, network fetches, browser edit/write controls or unsafe embedded JSON. |
| `T10-CG-V2-M22` | Visual projection and Graphology/Sigma boundary | `project_graph_visual_model.py`, renderer tests, optional `assets/vendor/graphology/`, optional `assets/vendor/sigma/` | Derived visual projection stores layout, size, color, community, `lod_tier`, label priority and renderer hints from canonical graph evidence; Graphology/Sigma are local/vendor-only with version/license/hash records and static fallback. |
| `T10-CG-V2-M23` | Graph filters, focused subgraphs and node evidence | `project_graph_queries.py`, HTML template tests | UI supports node/edge/confidence/language/artifact/partition/stale/text filters, bounded selected-node neighborhoods, trace/read-order subgraphs, fit/isolate/expand/reset/copy commands and evidence panel without raw source bodies. |
| `T10-CG-V2-M24` | Large graph, clustering, fallback and mobile | `project_graph_analysis.py`, renderer/performance/mobile tests | 1k/5k/10k graphs use overview clusters, level-of-detail, stable communities, hidden labels where needed, performance budget packets, WebGL/vendor failure fallback tables and mobile layouts without overlap. |
| `T10-CG-V2-M25` | Code Flow inside Code Intelligence | `project-code-flow.html`, renderer tests | Code Flow is a section inside `Code Intelligence`, links module/call-flow summaries to graph nodes and preserves generated-view/source-boundary wording. |
| `T10-CG-V2-M26` | Visual QA path | docs, optional Playwright checks | Browser verification covers nonblank graph, no console errors, no external requests, working filters, selected panel behavior, page grouping, local section navigation and desktop/mobile layouts. |
| `T10-CG-V2-M27` | Fixture eval structural fields | `run_fixture_eval.py`, fixture tests | Fixture eval reports graph contract, no external assets, redaction, scale bounds, generated-view-only, eight-page cockpit structure, section preservation and cockpit generated-view boundary. |
| `T10-CG-V2-M28` | Search quality eval loop | `run_fixture_eval.py`, search/eval tests | Fixture eval records symbol recall, top-k/MRR, edge density, trace success/failure labels, affected-test precision and explicit quality thresholds before Task 25 closure. |
| `T10-CG-V2-M29` | Future backend and semantic gates | docs/eval/runtime tests | Static search index, live database/server, LLM, embedding, cross-encoder, semantic extraction and rationale/comment extraction stay outside Task 25 baseline unless a later explicit approval defines redaction, cache, token budget, eval threshold and rollback path. |
| `T10-CG-V2-M30` | Docs, source registry and control-plane sync | Product-Agent OS docs, README, `docs/sources/registry.md`, root control-plane files | Docs explain scanner inputs, graph artifacts, query packets, cockpit navigation, visualization, scale policy, unsupported languages, source-of-truth boundary and any new external source-backed claims. |
| `T10-CG-V2-M31` | Focused verification | focused test commands | Scanner, schema, manifest, query, renderer, status/runtime, fixture eval and docs suites pass before broad verification. |
| `T10-CG-V2-M32` | Full verification and explicit git boundary | full checks, Git | Full unit suite, fixture eval, transcript eval, Codex compatibility, docs check, strict MkDocs when docs/nav-sensitive changes are made and diff hygiene pass; full unittest wrappers use `timeout_ms: 1200000`; do not stage, commit, push or create PR unless explicitly requested. |

Task 25 future-gated extension matrix:

| ID | Task | Files | Acceptance |
| --- | --- | --- | --- |
| `T10-CG-V2-M33` | Static search index approval and design | approval packet, `project_graph_index.py`, docs tests | Approved for Batch 19 by explicit user request. Approval scope is graph artifact only, generated cache-bound output, no live database/server, no LLM/embedding/cross-encoder, explicit eval thresholds and rollback/disable path. |
| `T10-CG-V2-M34` | Offline index schema and builder | `project_graph_index.py`, index tests | Builds a deterministic local index from redacted graph JSON/JSONL only; stores node IDs, labels, aliases, partitions, confidence, stale status and observation IDs without raw source bodies or absolute local paths. |
| `T10-CG-V2-M35` | Index freshness, cache and invalidation | `project_graph_index.py`, manifest tests | Index cache fingerprints graph artifacts, invalidates on graph manifest changes, records cache hit/miss evidence and never silently serves stale results as current. |
| `T10-CG-V2-M36` | Indexed search query packets | `project_graph_queries.py`, `scan_project_code_graph.py`, CLI tests | `search` can optionally use the static index while preserving deterministic JSON shape, output budgets, filter safety, source-free payloads and graph-only fallback. |
| `T10-CG-V2-M37` | Indexed search quality evals | `project_graph_search_quality.py`, fixture tests | Eval compares graph-only search and indexed search for symbol recall, top-k/MRR, affected-test precision, trace labels, false-positive rate and edge-density impact against explicit thresholds. |
| `T10-CG-V2-M38` | Static index docs and control-plane sync | docs, source registry, control-plane files | Docs explain that the index is offline, generated, cache-bound and not source of truth; source registry/backlog/control-plane record evidence and rollback notes. |
| `T10-CG-V2-M39` | Local query backend approval and architecture | approval packet, `project_graph_backend.py`, API contract tests | Batch 20 is approved by explicit user request and limited to a generated local file-store gate. Approval names storage path, port policy, process lifecycle, auth boundary, cleanup, logging, eval threshold and rollback path. |
| `T10-CG-V2-M40` | Local database schema and storage safety | `project_graph_backend.py`, storage tests | Stores graph/index artifacts in a generated local file store with schema version, migration guard, backup/restore plan, path safety, size caps and deletion/cleanup command; no live database is started. |
| `T10-CG-V2-M41` | Server process lifecycle and no-active-default gate | backend CLI, runtime tests | Server mode is disabled by default, starts no production server, writes no global config, records disabled PID/port/log paths and has a deterministic disable path. |
| `T10-CG-V2-M42` | Query API contract and security boundary | backend API tests, runtime contracts | Contract API handling exposes read-only graph/index query endpoints with bounded payloads, request IDs, no browser edit/write controls, no external network dependency and stable JSON error responses without local path leaks. |
| `T10-CG-V2-M43` | Backend performance, concurrency and rollback evals | backend tests, fixture eval | Generated-store queries meet approved latency/payload thresholds; concurrent reads stay deterministic; rollback returns to graph-only query mode. |
| `T10-CG-V2-M44` | Backend docs and operational evidence | docs, RUNLOG, TEST, EVALS | Docs and control-plane record approval, disabled-by-default server mode, cleanup, logs, rollback, residual risks and no-production-server/non-source-of-truth boundaries. |
| `T10-CG-V2-M45` | Semantic retrieval approval and model decision | approval packet, `project_graph_semantic.py`, model decision record | Batch 21 is approved by explicit user request and limited to local deterministic embeddings/cross-encoder eval. Approval names local models, data classification, redaction, token/cost budget, cache, eval threshold, failure handling and rollback. |
| `T10-CG-V2-M46` | Semantic corpus and chunk policy | `project_graph_semantic.py`, chunking tests | Builds semantic corpus from redacted graph labels, structured chunks and approved snippets only; excludes raw private text, secrets, absolute paths and generated HTML as source. |
| `T10-CG-V2-M47` | Embedding generation and cache artifacts | `project_graph_semantic.py`, cache tests | Generates or imports embeddings only for approved corpus records; caches vectors with model/version/hash metadata, source observation IDs, expiration policy and deterministic deletion path. |
| `T10-CG-V2-M48` | Semantic search query packets | `project_graph_queries.py`, semantic tests | Adds optional semantic query packets with similarity scores, source observation IDs, confidence labels, top-k caps, fallback to lexical/indexed search and no completion claims from semantic matches alone. |
| `T10-CG-V2-M49` | Cross-encoder reranking gate | `project_graph_semantic.py`, rerank tests | Optional reranking runs only after approval, records model/version/cost/latency evidence, improves or blocks based on thresholded evals and never rewrites canonical graph edges. |
| `T10-CG-V2-M50` | Semantic retrieval eval suite | eval fixtures, `project_graph_search_quality.py` | Eval covers recall@k, MRR, nDCG where applicable, false-positive semantic links, privacy redaction, stale corpus behavior, cost/latency budget and regression thresholds. |
| `T10-CG-V2-M51` | Semantic retrieval docs and lifecycle routing | docs, lifecycle skills, runtime contracts | Docs and lifecycle skills route semantic hits as `present_unverified` orientation evidence until source reads, owner review or accepted gaps exist. |
| `T10-CG-V2-M52` | LLM extraction approval and schema | approval packet, `project_graph_llm_extraction.py`, schema tests | Implementation is blocked until approval defines extraction schema, prompt/model policy, redaction, token budget, eval threshold, incident path, owner and rollback/disable path. |
| `T10-CG-V2-M53` | Prompt/model/tool contract for extraction | prompt contract, extraction tests | Prompts use approved redacted context only, forbid secrets/private data retention, record model/sampling/version, and produce structured JSON with provenance, uncertainty and unsupported-claim labels. |
| `T10-CG-V2-M54` | Semantic node and edge proposal generation | `project_graph_llm_extraction.py`, graph proposal tests | Generated semantic nodes/edges are staged as proposals with confidence, source observation IDs, rationale, review status and no mutation of canonical graph until owner acceptance. |
| `T10-CG-V2-M55` | Rationale and comment extraction | extraction tests, docs tests | Extracts rationale/comment summaries only from approved public or redacted source spans; labels inferred intent as unverified; blocks private comments, secrets, unsupported claims and source-of-truth wording. |
| `T10-CG-V2-M56` | Human review, acceptance and incident workflow | review packet, EVALS, RUNLOG | Owner review can accept, reject or mark generated semantics as accepted gap; failed extraction, data leak or unsafe output routes to AI incident workflow and disables extraction until fixed. |
| `T10-CG-V2-M57` | LLM extraction evals and docs sync | eval fixtures, docs, source registry | Eval covers extraction precision, hallucination/unsupported-claim rate, privacy, cost/latency, stale context, rollback and docs/source registry/control-plane evidence. |
| `T10-CG-V2-M58` | Future extension focused verification | focused command set | Static index, backend, semantic retrieval and LLM extraction focused suites pass only for approved surfaces; unapproved surfaces remain skipped/blocked with explicit evidence. |
| `T10-CG-V2-M59` | Future extension full verification | full checks | Full unit suite, fixture eval, transcript eval, Codex compatibility, docs check, strict MkDocs and diff hygiene pass with `timeout_ms: 1200000`; generated artifacts remain source-free and staged. |
| `T10-CG-V2-M60` | Runtime and visual QA for approved extensions | backend/runtime/browser checks | Approved backend or semantic UI surfaces have runtime/browser evidence, no console errors, no external requests beyond approved model/provider calls and visible generated-view/source-boundary labels. |
| `T10-CG-V2-M61` | Disable, rollback and data deletion proof | rollback tests, RUNLOG | Every approved extension can be disabled, cache/index/database/vector artifacts can be deleted, graph-only baseline still works and rollback evidence is recorded. |
| `T10-CG-V2-M62` | Future extension docs/source/control-plane closure | docs, source registry, root control-plane files | Docs separate baseline, approved extension and deferred capabilities; source registry and root control-plane record evidence, unsupported claims, approval status and explicit-only git boundary. |

Task 25 implementation batches:

- **Batch 13: Graph Foundation, Schema And Staging** (`T10-CG-V2-M01..M07`)
- **Batch 14: Python AST Scanner, Dependency Edges And Overlays** (`T10-CG-V2-M08..M13`)
- **Batch 15: Agent Query Packets, Runtime Integration And Analysis** (`T10-CG-V2-M14..M18`)
- **Batch 16: HTML Cockpit, Code Graph Visualization And Project Map** (`T10-CG-V2-M19..M26`)
- **Batch 17: Evals, Docs, Control Plane And Future Gates** (`T10-CG-V2-M27..M30`)
- **Batch 18: Focused, Full Verification And Closure** (`T10-CG-V2-M31..M32`)
- **Batch 19: Offline Static Search Index** (`T10-CG-V2-M33..M38`, approved and implemented)
- **Batch 20: Local Query Backend And Live Database/Server Gate** (`T10-CG-V2-M39..M44`, approved and implemented)
- **Batch 21: Semantic Retrieval, Embeddings And Cross-Encoder Eval** (`T10-CG-V2-M45..M51`, approved and implemented)
- **Batch 22: LLM Semantic Extraction And Rationale/Comment Proposals** (`T10-CG-V2-M52..M57`, future-gated)
- **Batch 23: Future Extension Verification, Rollback And Closure** (`T10-CG-V2-M58..M62`, future-gated)

Task 25 starts only after Task 24 final verification evidence remains current. The Batch 13-18 baseline must preserve the Track 10 non-goals: no standalone web server, no database, no live model/API calls, no external writes, no hook/automation activation and no HTML-as-source-of-truth claim. Batch 19 adds only an offline generated static search index and does not relax database/server/model-call non-goals. Batch 20 adds only a generated local file-store backend gate with disabled-by-default server mode, no production server and graph-only fallback. Batch 21 adds only a generated semantic retrieval cache with local deterministic embeddings/cross-encoder eval, `present_unverified` routing and no canonical graph edge rewrites. Batch 22-23 extensions may relax only future LLM extraction or closure surfaces after explicit approval with redaction, cache, token budget, eval threshold and rollback path; all other boundaries remain staged-first, source-free where possible, rollbackable and evidence-bound.

## Execution Batches

### Batch 1: Question Protocol Foundation (`T10-Q-M-1..M4`)

- [ ] **Step 0: Run baseline contract audit**

Confirm before implementation:

- Track 10 implementation files are not already present;
- `questions_for_owner`, `unknowns`, `safe_next_action`, `methodology_synthesis`, `recommendation_groups`, `source_artifact_ledger`, `usage_mode`, `route_inputs`, `methodology_packet`, `finish_options`, staged renderer, stage manifest, approval flow and redaction are already available;
- focused discovery/runtime/renderer/lifecycle baseline tests pass.

- [ ] **Step 1: Write RED question protocol tests**

Create `tests/product_agent_os/test_question_protocol.py` with tests for:

```python
def test_question_queue_limits_first_response_to_one_blocking_question():
    packet = build_question_queue(
        owner_questions=[
            "Which local command is the source of truth for verification?",
            "Who owns the highest-priority missing methodology gate?",
        ],
        unknowns=["current verification command"],
        runtime_status="route_ready",
    )
    blocking = [item for item in packet["questions"] if item["priority"] == "blocking"]
    assert packet["policy"]["max_blocking_questions_in_first_response"] == 1
    assert len(blocking) == 1
```

- [ ] **Step 2: Run RED tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_question_protocol -v
```

Expected: fail with missing `product_agent_os.question_protocol`.

- [ ] **Step 3: Implement minimal question protocol**

Create `question_protocol.py` as an adapter over existing audit/runtime signals with:

```python
QUESTION_PRIORITIES = ["blocking", "recommended", "optional"]
QUESTION_CATEGORIES = ["scope", "product", "verification", "approval", "ownership", "risk", "release"]
QUESTION_ANSWER_TYPES = ["text", "single_choice", "single_choice_or_text", "multi_choice", "approval", "not_applicable_or_gap"]
MAX_TOTAL_QUESTIONS = 8
MAX_FIRST_RESPONSE_BLOCKING = 1
```

Implement `build_question_queue()` as a pure function with no filesystem writes. It must consume existing `questions_for_owner`, `unknowns`, recommendation groups, `usage_mode` and runtime gaps instead of duplicating methodology-audit rules.

- [ ] **Step 4: Add ledger RED tests and implementation**

Create `tests/product_agent_os/test_question_ledger.py` and `question_ledger.py`.

Run:

```powershell
python -m unittest tests.product_agent_os.test_question_protocol tests.product_agent_os.test_question_ledger -v
```

Expected: pass after implementation.

### Batch 2: Discovery And Runtime Integration (`T10-Q-M5..M7`)

- [ ] **Step 1: Extend discovery tests**

Update `tests/product_agent_os/test_discovery.py` to assert:

```python
result = analyze_workspace(workspace)
self.assertIn("question_queue", result)
self.assertLessEqual(len(result["question_queue"]["questions"]), 8)
self.assertIn("route_inputs", result)
```

- [ ] **Step 2: Attach question queue in discovery**

Modify `discovery.py` after methodology audit is built. Use owner questions and unknowns from `methodology_intelligence`.

- [ ] **Step 3: Extend runtime contract tests**

Update runtime tests so `route_packet` accepts bounded `question_queue` and optional `status_snapshot_ref` as additive sibling fields. `route_packet.first_response_contract` must include `next_blocking_question` plus counts and must not dump every question. Keep `methodology_packet` strict and read-only.

- [ ] **Step 4: Run focused runtime tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_discovery tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_state_routes -v
```

Expected: all focused tests pass.

### Batch 3: Status Snapshot (`T10-Q-M8..M9`)

- [ ] **Step 1: Write status snapshot tests**

Create `tests/product_agent_os/test_status_snapshot.py`.

Assert snapshot fields:

- `schema_version`;
- `generated_at`;
- redacted `workspace`;
- `lifecycle_state`;
- `usage_mode`;
- `question_summary`;
- `readiness_summary`;
- `evidence_summary`;
- `next_safe_action`;
- `dashboard_policy`;
- `renderer_file_count`;
- stage manifest digests or equivalent dashboard manifest digest;
- `source_artifact_ledger`;
- `semantic_evidence_sufficiency`;
- redaction summary.

- [ ] **Step 2: Implement status snapshot builder**

Create `status_snapshot.py` as a pure builder. It must accept dict packets, return JSON-serializable output, reuse existing redaction behavior and label stale or inspection-only evidence without implying success.

- [ ] **Step 3: Run snapshot tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_status_snapshot -v
```

Expected: pass.

### Batch 4: Static HTML Dashboard (`T10-Q-M10..M14`)

- [ ] **Step 1: Write dashboard tests**

Create `tests/product_agent_os/test_status_dashboard.py`.

Required assertions:

- HTML starts with `<!doctype html>`;
- no `http://` or `https://`;
- no `<script src=`;
- contains lifecycle, usage mode, questions, readiness, evidence, approvals and next action sections;
- includes stale evidence warning when `inspection_only` is true;
- contains a `<meta name="viewport">`.

- [ ] **Step 2: Create HTML/CSS templates**

Create:

- `plugins/product-agent-os/assets/templates/status-dashboard/status.html`;
- `plugins/product-agent-os/assets/templates/status-dashboard/status.css`.

Use static CSS, semantic headings, tables/lists and embedded escaped JSON.

- [ ] **Step 3: Implement renderer and CLI**

Create:

- `status_dashboard.py`;
- `render_status_dashboard.py`.

CLI contract:

```powershell
python plugins\product-agent-os\scripts\render_status_dashboard.py <workspace> --dry-run
python plugins\product-agent-os\scripts\render_status_dashboard.py <workspace> --stage C:\tmp\product-agent-os-status-stage
```

- [ ] **Step 4: Integrate stage renderer**

Modify `templates.py` and `infrastructure.py` only if needed for an explicit dashboard staging path. Dashboard files must appear under:

```text
.codex/product-agent-os/status.html
.codex/product-agent-os/status.json
```

Existing unmarked files must be preserved as companion proposals. Baseline `required_templates()` rendering must not silently add dashboard files to every infrastructure render unless the implementation has an explicit opt-in flag/path with test coverage.

- [ ] **Step 5: Run focused dashboard and renderer tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_status_dashboard tests.product_agent_os.test_infrastructure_renderer tests.product_agent_os.test_infrastructure_templates -v
```

Expected: pass.

### Batch 5: Evals, Skills And Docs (`T10-Q-M15..M22`)

- [x] **Step 1: Extend fixture eval**

Update `run_fixture_eval.py` and fixture eval tests with:

- `question_queue_contract_present`;
- `status_snapshot_present`;
- `status_dashboard_present`;
- `dashboard_no_external_assets`;
- `question_budget_false_positive_guard_present`;
- `dashboard_not_source_of_truth`;
- `stale_evidence_no_success_claim`.

- [x] **Step 2: Add behavioral and transcript coverage**

Update behavioral eval JSON and synthetic transcript fixtures so they cover:

- one blocking question maximum;
- no broad methodology interview;
- dashboard as generated view only;
- no success claim from stale evidence;
- no full question queue dump in first response.

- [x] **Step 3: Update lifecycle skills**

Lifecycle skills must state:

- ask the smallest blocking question only;
- keep optional questions in the packet;
- route answers into artifacts or accepted gaps;
- do not use guided questions as a substitute for workspace evidence.

- [x] **Step 4: Update docs and root control plane**

Update Product-Agent OS docs, README and root control-plane files after implementation.

- [x] **Step 5: Run focused docs/eval checks**

Run:

```powershell
python -m unittest tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_transcript_session_evals -v
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python tools\check_docs.py
git diff --check
```

Expected: all commands exit `0`.

### Batch 6: Full Verification (`T10-Q-M23..M25`)

- [x] **Step 1: Run full unit suite**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: exit `0`.

Current evidence: on 2026-05-28, the command ran 543 tests with `OK`.

- [x] **Step 2: Run fixture eval**

Run:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: exit `0`, all fixtures `ok: true`.

Current evidence: on 2026-05-28, the command exited `0`; runner output kept `renderer_file_count: 187` and all emitted fixture records had `ok: true`.

- [x] **Step 3: Run transcript eval**

Run:

```powershell
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
```

Expected: exit `0`.

Current evidence: on 2026-05-28, the command exited `0` with 10 sessions and 0 failures.

- [x] **Step 4: Run compatibility and docs checks**

Run:

```powershell
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict
git diff --check
```

Expected: compatibility JSON includes `"status": "compatible"` and all commands exit `0`.

Current evidence: on 2026-05-28, Codex compatibility returned `"status": "compatible"`, `python tools\check_docs.py` passed, strict MkDocs exited `0` with disposable `--site-dir .mkdocs_task23_site`, the disposable site directory was removed, and `git diff --check` exited `0`.

- [x] **Step 5: Commit explicit-only boundary preserved**

Do not run this step unless the user explicitly requests a commit.

Current evidence: no `git add`, `git commit`, `git push` or PR creation was executed in Batch 6.

If approved after all verification is current:

```powershell
git add docs plugins tests REQUIREMENTS.md PLAN.md TEST.md EVALS.md RUNLOG.md
git commit -m "feat: add guided questions and status dashboard"
```

Expected: commit succeeds.

## Risk Register

| Risk | Mitigation |
| --- | --- |
| The plugin asks too many questions and stalls the user. | Enforce one blocking question in first response and max eight total questions. |
| HTML dashboard becomes stale and misleading. | Show `generated_at`, evidence freshness, inspection-only banner and source digests. |
| Dashboard is treated as source of truth. | Docs and snapshot policy state JSON/Markdown control-plane is source of truth. |
| Dashboard leaks local paths or private data. | Reuse runtime redaction and add dashboard-specific tests for path/secret leakage. |
| Existing project dashboard files are overwritten. | Preserve unmarked files as companion proposals and use staged-first merge flow. |
| Question answers become hidden memory. | Store answers only in explicit ledger artifacts, never user-level memory. |
| New runtime fields break schema-v1 compatibility. | Add fields only inside existing route packet surfaces and validate bounded shape. |
| Self-verification is mistaken for approval to rewrite agents, skills or harness policy. | Stage scorecards and update candidates only; require owner approval, rollback target and current evidence before any later apply flow. |
| Metrics overfit to recently implemented tasks and miss regressions. | Keep holdout, prior-failure, synthetic regression and flaky-case groups separate; require raw numerator/denominator counts and confidence evidence. |
| Agent/skill evidence leaks private traces or local user paths. | Reuse redaction gates before dataset, ledger, report or dashboard generation and block scoring when redaction fails. |
| Metrics-loop automation is activated before the manual workflow is stable. | Ship daily and weekly automation files as candidate templates only and require `automation_manual_stability_present` plus explicit approval before promotion. |
| Docs-only or simple maintenance work triggers agentic modernization overhead. | Add discovery false-positive fixtures and keep `agent_skill_metrics_loop` applicable only when real agent, skill, subagent, router/tool policy, automation candidate or harness surfaces are detected. |
| Code graph overwhelms the browser or agent context on large projects. | Use graph summaries, chunked JSON/JSONL, clustering, top-N subgraphs, hidden labels and query packets for 1k, 5k and 10k node cases. |
| Code graph implies false dependency precision. | Require confidence labels, unsupported-language statuses and tests that distinguish AST/static evidence from inferred edges. |
| Static analysis invents cross-file call edges in ambiguous code. | Prefer import-guided resolution, emit inferred global calls only on single-candidate matches and record ambiguous calls as explicit uncertainty. |
| Incremental cache reports stale topology as fresh. | Store manifest freshness with separate AST/semantic hashes, changed/unchanged/added/deleted file sets and graph freshness status. |
| Failed scans silently replace a rich graph with a much smaller artifact. | Add shrink guard and stage-local backups before overwrite; require explicit acceptance for suspicious graph collapse. |
| Agent graph queries expand through high-degree hub nodes and waste context. | Add token-budgeted BFS/DFS traversal, hub suppression, context filters, seed scoring and truncation metadata. |
| Graph artifacts leak source code, secrets or local user paths. | Exclude raw file contents by default, keep line spans/hashes only, reuse redaction policy and block secret-like values in renderer/query output. |
| HTML graph is treated as source of truth. | Keep code/docs plus graph JSON/JSONL as source/evidence layers; HTML remains generated cockpit review output. |
| Graph visualization libraries introduce network or supply-chain risk. | Use `graphology`/`sigma.js` only as locally bundled, version-recorded assets with no CDN; keep a fallback renderer. |
| Cockpit navigation hides important warnings after page grouping. | Preserve every detailed section exactly once, add local section navigation and test Source Conflicts, Verification Gates and Security/Risk visibility. |
| Eight-page cockpit shell becomes a second documentation site instead of a project map. | Keep pages action-oriented: source links, graph packets, stale flags, verification gates, approval boundaries and proposal lifecycle must remain visible. |

## Verification Summary

Track 10 completion requires current-run evidence for:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict
git diff --check
```

Do not claim Track 10 works from code inspection only.

Task 24 implementation must also add focused current-run evidence before full verification:

```powershell
python -m unittest tests.product_agent_os.test_agent_skill_metrics tests.product_agent_os.test_agent_skill_metrics_report tests.product_agent_os.test_agent_skill_metrics_cli -v
python -m unittest tests.product_agent_os.test_status_dashboard tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_automation_policy -v
python -m unittest tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_transcript_session_evals -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python tools\check_docs.py
git diff --check
```

Task 25 implementation must also add focused current-run evidence before full verification:

```powershell
python -m unittest tests.product_agent_os.test_project_code_graph tests.product_agent_os.test_project_graph_manifest tests.product_agent_os.test_project_graph_observations tests.product_agent_os.test_project_graph_ontology tests.product_agent_os.test_project_graph_overlays tests.product_agent_os.test_project_graph_analysis tests.product_agent_os.test_project_graph_queries tests.product_agent_os.test_project_graph_visual_model tests.product_agent_os.test_project_graph_renderer tests.product_agent_os.test_project_cockpit_model tests.product_agent_os.test_project_graph_cli tests.product_agent_os.test_project_graph_safety -v
python -m unittest tests.product_agent_os.test_status_snapshot tests.product_agent_os.test_status_dashboard tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_state_routes -v
python -m unittest tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_product_agent_os_docs -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python tools\check_docs.py
git diff --check
```
