# Project formation

Source status: project-local implementation; local checks and synthetic pilots. Fresh-session host activation remains separate.

The unified route analyzes a workspace, selects documents, reconciles `docs/` and `.codex/`, previews changes and stages proposals. Applying them uses the existing merge engine with a separate approval record. Root documents own current state, `docs/` owns project material, and `.codex/` holds control proposals and templates.

## Input and selection

The request uses `schema_version: 1` and an existing task context v1 under `task`.

| Field | Meaning |
| --- | --- |
| `domains` | Confirmed applicability: `planning`, `architecture`, `decisions`, `api`, `data`, `operations`, `evidence`, `archive`, `ai`. An empty list selects no additional domains. |
| `canonical_paths` | Explicit document-owner paths; resolves ambiguous existing sources. |
| `document_facts` | A selected domain's `source` and `sections` mapping. Unknown facts stay missing. |
| `control_surfaces` | Explicit `agents`, `config`, `hooks` proposals. Config includes required role profiles without activating them. |

Without `domains`, the planner considers existing canonical documents, OpenAPI/schema/workspace manifests and explicit release scope. Reasons appear in `domain_decisions`. Unknown stack remains a question; file presence is not application behavior. Ambiguous owners require `canonical_paths`.

```json
{
  "schema_version": 1,
  "task": {
    "schema_version": 1,
    "task_id": "FORM-01",
    "intent": "Establish project documentation",
    "change_mode": "docs_only",
    "changed_paths": ["README.md"],
    "risk_level": "low",
    "acceptance": ["Preserve user decisions and document ownership"],
    "risks": [],
    "explicit_full_packet": true
  },
  "domains": ["architecture", "planning", "evidence"],
  "canonical_paths": {},
  "document_facts": {},
  "control_surfaces": []
}
```

This produces scaffolds, not accepted requirements. Missing verification commands remain `implementation_gaps`; scaffolding does not waive them. Scaffold, draft, review and owner acceptance are separate; an old receipt does not accept changed content.

## Commands

Request JSON paths are explicit and relative to the command's working directory when not absolute. Stage into a new directory outside the target workspace.

```powershell
python plugins/product-agent-os/scripts/render_infrastructure.py demo --analyze
python plugins/product-agent-os/scripts/render_infrastructure.py demo --dry-run --formation-context request.json
python plugins/product-agent-os/scripts/render_infrastructure.py demo --stage staging-demo --formation-context request.json --preview-digest sha256:DIGEST
python plugins/product-agent-os/scripts/render_infrastructure.py demo --merge-stage staging-demo
```

Use `formation.digest` from the reviewed preview. It binds observed sources, request and planner/template revisions. Changed inputs require a new preview. A digest grants no target-write authority.

After the owner approves the concrete merge plan:

```powershell
python plugins/product-agent-os/scripts/render_infrastructure.py demo --merge-stage staging-demo --apply --approval-file approval.json
python plugins/product-agent-os/scripts/render_infrastructure.py demo --rollback staging-demo/product-agent-os-rollback-manifest.json
```

Use the existing merge approval template to name the plan, owner, targets and actions. Rollback also requires applicable authority. The separate `merge_infrastructure.py` remains compatible and checks the same formation binding.

## Structure and preservation

The full route selects applicable root documents and quality templates; ordinary scope can reuse the existing control plane. `EVALS.md` is conditional on AI/eval scope; an existing eval document can be reused. Dependency closure explains additional files; there is no fixed file count.

Selected domains propose `docs/planning/README.md`, `docs/architecture/overview.md`, and indexes under `docs/decisions/`, `docs/api/`, `docs/data/`, `docs/operations/`, `docs/evidence/`, `docs/archive/`. Existing canonical names are reused. The navigation entry is existing `docs/index.md`/`docs/README.md`, otherwise new `docs/README.md`.

Formation preserves every existing file, including user-authored `AGENTS.md`. Changes remain companion proposals; `manual_updates` identifies review work. This does not claim that an existing index was updated. Only absent files are created through approved merge; regeneration does not authorize replacing accepted decisions.

Use `--previous-plan previous.json` to obtain `changes`: added paths, changed sources and `review_only_removed`. Nothing is automatically deleted. History transfer uses separate [lossless compaction](technical.md). Detailed `docs/planning/` matrices are exempt only from the default size trigger; explicit limits and content checks remain.

Compact mode reuses an ordinary existing project with `AGENTS.md` and `domains: []`; it need not create another file catalog. The extended request above produces this tree for the empty synthetic project (14 proposals, without AI or control surfaces):

```text
project/
├── AGENTS.md
├── REQUIREMENTS.md
├── PLAN.md
├── TEST.md
├── RUNLOG.md
├── docs/
│   ├── README.md
│   ├── architecture/overview.md
│   ├── planning/README.md
│   └── evidence/README.md
└── .codex/
    ├── artifact-templates/
    │   ├── agent-task-packet.md
    │   ├── code-change-contract.md
    │   ├── coding-standard-checklist.md
    │   └── quality-strategy.md
    └── workflows/coding-standards.md
```

AI/eval scope adds `EVALS.md`; other domains and control proposals extend the tree only when selected. These files are scaffolds and proposals, not accepted project content.

## Boundaries and errors

- Missing formation/scoped input never selects the full catalog. Explicit `--legacy-catalog` preserves that compatibility route; `--task`/`--task-context` retain G8 scoped APIs.
- Discovery is bounded to 20,000 visited entries, 512 relevant files, 2 MiB per file and 8 MiB total reads. Exceeding limits requires a narrower workspace. Inventory records states/digests, not private raw bodies.
- Ambiguous paths, redirects, invalid schemas, secret-like input and stale previews stop the applicable operation.
- Frozen authority prevents writes; declared SQL projections follow the local M1 authority contract. This does not prove the actual M1 SQL adapter.
- Formation creates use a write-ahead recovery receipt and atomic file replacement for the tested post-write/pre-receipt crash window. No cross-file ACID claim; exclude external writers. Rollback preserves later user changes by refusing mismatched state.
- SessionStart-owned state is a runtime dependency, not a generated accepted state. Hooks/config/agents remain proposals; fresh-session activation is separate.

Implementation sources: `plugins/product-agent-os/scripts/product_agent_os/project_formation.py`, `infrastructure.py`, `merge_infrastructure.py`. Checks: `tests/product_agent_os/test_project_formation.py`; comparison: `docs/superpowers/specs/paos-aud-g9-project-formation-results.json`; evidence/acceptance: `research/product-agent-os-g9-execution-report.md`.

See [technical contract](technical.md), [architecture](architecture.md), and [source registry](../sources/registry.md).

## Targeted documentation maintenance after a task

Assess documentation impact after every task; write only changed canonical sections. Reuse the task Completion Report for changed fact, owner/path/section, source revision/evidence, decision and reason. `no_change_needed` needs justification; required `handoff_required` prevents implemented closure. Small tasks do not require another report.

`sync_task_documents.py` previews exact existing-section diffs and uses the shared recovery journal. Completion updates the selected task card and matching PLAN revision in one recoverable package. Other sections, user bytes and other pins remain intact. Stale input, freeze/SQL projections and conflicts stop writes; identical repeats write nothing. The old `create_task_plan.py complete` requires explicit `--legacy-card-only` and does not prove synchronization.

Route requirements to REQUIREMENTS, sequencing to PLAN, commands to TEST, eval policy to EVALS, current handoff to RUNLOG, and API/schema/operations to their canonical domain source. Detailed checks stay in their evidence owner. Reuse docs/adr, docs/runbooks, docs/ops, docs/testing and docs/archive. New owners use formation staging; ambiguity requires review.

Cross-file duplicates in affected/source paths need disposition; current authorized mirrors and linked brief summaries have separate checks. No automatic semantic deletion. Keep 40 000-byte / 32 000-warning budgets and the detailed docs/planning matrix exception; no automatic research matrix split. Event sync, size triggers and read-only periodic hygiene are distinct; no schedules are created. Digests establish integrity, not semantic completeness or acceptance. Fresh-session activation remains separate.

Source: `plugins/product-agent-os/scripts/product_agent_os/documentation_sync.py`; checks `test_document_navigation.py`, `test_task_plan_lifecycle.py`; evidence `research/product-agent-os-g9-execution-report.md`.
