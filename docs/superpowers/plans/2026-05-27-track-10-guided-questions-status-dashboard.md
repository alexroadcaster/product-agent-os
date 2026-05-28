# Track 10 Guided Questions And Status Dashboard Implementation Plan

Source status: `local implementation planning`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build Track 10 so Product-Agent OS can guide users with bounded, methodology-aware questions, maintain a single offline HTML status artifact for project progress, and stage a self-verification loop for agents, skills and harness modernization decisions.

**Architecture:** Extend the existing Track 8 usage-mode route and Track 9 methodology packet with a typed question protocol, answer ledger, status snapshot, staged static dashboard renderer, and a local-first metrics loop for self-verification. JSON and Markdown remain the source of truth; HTML artifacts are generated, reviewable views that are staged first and never silently mutate the target workspace.

**Tech Stack:** Python standard library, `unittest`, JSON contracts, Markdown control-plane artifacts, static HTML/CSS/vanilla JavaScript, existing `plugins/product-agent-os/scripts/product_agent_os/*` modules, existing Codex runtime runner, fixture eval runner, transcript eval runner, docs checks, MkDocs.

---

## Scope Check

Track 10 is a new user-facing capability, not part of Track 9 final documentation sync.

It includes these implementation tasks:

- `Task 23: Guided Question Protocol And Project Status Dashboard`
- `Task 24: Self-Verification And Modernization Loop`

Track 10 must start only after Track 9 `Task 22` closes the current Product-Agent OS documentation baseline. This prevents Task 22 from becoming a moving target while Track 10 changes runtime packets, renderer output, evals and docs.

## Numbering Note

The Track 9 plan now keeps the former `Task 23: Final Verification Baseline` only as a legacy checklist section under Task 22. Task 22 absorbs that verification baseline into `T22-U-M23`, so Track 10 uses `Task 23` for the next product capability:

- typed guided questions;
- answer ledger;
- status snapshot;
- offline `status.html` dashboard.
- agent/skill/harness self-verification and staged modernization candidates.

Do not implement Track 10 unless Track 9 docs keep the legacy final baseline absorbed into Task 22 and current verification evidence exists.

## Product Outcome

After Track 10, a user should be able to enable Product-Agent OS in a real project and see:

- one or zero blocking questions at a time;
- optional follow-up questions grouped by product, technical, verification, approval and ownership category;
- why each question matters and what artifact it affects;
- a stable status page showing current lifecycle state, usage mode, methodology readiness, evidence gaps, approvals, staged artifacts, open risks and next safe action;
- stale/evidence warnings when the dashboard is generated from inspection-only or old command evidence.
- staged self-verification reports for generated agents, skills, prompt or policy packs, router/tool policies and harness versions, with modernization candidates separated from approval.

The plugin must keep forward momentum. It should ask only questions that block safe planning, approval, evidence or the next artifact.

## Non-Goals

- Do not add a standalone web server.
- Do not add a database.
- Do not add a live model call, OpenAI API dependency, or Agents SDK app.
- Do not activate MCP servers, hooks, GitHub Actions, recurring automations or external writes.
- Do not make HTML the source of truth.
- Do not create browser-based editing of project files in this track.
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

Batch 11 status: implemented on 2026-05-28 with focused RED/GREEN coverage for status snapshots, discovery, methodology audit, runtime packets/routes, guided questions, lifecycle skills, fixture eval, behavioral eval and transcript sessions. Batch 12 remains the final docs/control-plane/full-verification closure slice.

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
