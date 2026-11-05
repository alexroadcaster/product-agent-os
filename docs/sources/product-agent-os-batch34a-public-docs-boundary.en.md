---
title: "Archive - Product-Agent OS Batch 34A public docs boundary and IA packet"
---

# Archive - Product-Agent OS Batch 34A public docs boundary and IA packet {#product-agent-os-batch-34a-public-docs-boundary-and-ia-packet}

> Historical source record. Dates and verdicts below describe that run; use current guides for present behavior.

Source status: `internal`

## Scope

This packet records Batch 34A `B34-PROD-M16..M18` for Product-Agent OS documentation. It is an internal evidence packet for the public documentation boundary, presentation IA, page ownership map and forbidden-term policy.

This packet does not rewrite public copy, enable RU/EN localization, publish the docs site, start a live server, run browser automation, call providers or live external model/API endpoints, mutate the canonical graph, publish the plugin or perform git stage/commit/push/PR.

## B34-PROD-M16 Boundary

`public_product_candidates` are pages that can become presentation-facing Product-Agent OS documentation after Batch 34B copy cleanup and Batch 34C RU/EN localization:

| Page group | Candidate paths | Current state |
| --- | --- | --- |
| Product-Agent OS overview and references | `docs/product-agent-os/index.md`, `docs/product-agent-os/project-code-graph.md`, `docs/product-agent-os/live-runtime-governance.md`, `docs/product-agent-os/approval-bound-real-testing.md`, `docs/product-agent-os/agent-skill-modernization-loop.md`, `docs/product-agent-os/cli-reference.md`, `docs/product-agent-os/artifact-contracts.md`, `docs/product-agent-os/packaging-and-closure.md` | `cleanup_pending` |
| Product-Agent OS operating model | `docs/product-agent-os/technical.md`, `docs/product-agent-os/development-standards.md`, `docs/product-agent-os/methodology-intelligence.md`, `docs/product-agent-os/scenarios.md`, `docs/product-agent-os/behavioral-evals.md`, `docs/product-agent-os/codex-compatibility.md`, `docs/product-agent-os/architecture.md` | `cleanup_pending` |
| Product-agent bridge pages | `docs/product-agent/overview.md`, `docs/product-agent/lifecycle.md`, `docs/product-agent/roles.md`, `docs/product-agent/control-plane.md`, `docs/product-agent/product-agent-os-plugin-spec.md` | `cleanup_pending` |
| Practical implementation atlas | `docs/diagrams/index.md`, `docs/diagrams/architecture.md`, `docs/diagrams/product-delivery-lifecycle.md`, `docs/diagrams/agent-team-and-skills.md`, `docs/diagrams/runtime-decision-map.md`, `docs/diagrams/skill-lifecycle.md`, `docs/diagrams/context-memory-verification.md` | `cleanup_pending` |
| Supporting runtime and workflow bridges | `docs/runtime/overview.md`, `docs/runtime/non-interactive-and-mcp.md`, `docs/runtime/automations-github.md`, `docs/runtime/worktrees-hooks-rules.md`, `docs/agent-systems/subagents-skills.md`, `docs/playbooks/docs-update.md`, `docs/playbooks/use-case-to-plugin.md`, `docs/playbooks/workspace-readiness-audit.md` | `cleanup_pending` |

`internal_evidence` stays outside the public presentation journey or must be explicitly labeled as internal:

| Internal surface | Paths | Reason |
| --- | --- | --- |
| Source registry and source packets | `docs/sources/registry.md`, `docs/sources/*.md` | Provenance, verification and evidence retention. Not product copy. |
| Implementation plans and methodology worklogs | `docs/superpowers/plans/*.md`, `docs/superpowers/specs/*.md` | Internal delivery history and planning ledger. |
| Root control-plane files | `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` | Durable project rules, current verification evidence and run history. |
| Test and tooling contracts | `tests/product_agent_os/test_product_agent_os_docs.py`, `tools/check_docs.py`, `mkdocs.yml` | Verification/tooling surfaces. |
| Generated site output | `site/` | Review output only, not source of truth. |

Decision: public presentation docs are not allowed to depend on `docs/sources/`, `docs/superpowers/`, registry, backlog or root control-plane provenance for reader comprehension. Those internal surfaces remain evidence-retention assets until a separate owner decision changes the retention policy.

## B34-PROD-M17 IA Proposal

Proposed public navigation shape for the presentation-ready site after Batch 34B and Batch 34C:

```text
Product-Agent OS
  Start Here
  Principles
  Workflows
  Agent Teams And Skills
  Runtime And Approvals
  Artifacts And CLI
  Quality And Evaluation
  Packaging And Closure

Implementation Atlas
  Delivery Lifecycle
  Runtime Choices
  Agent Team Design
  Skill Lifecycle
  Context, Memory, Verification

Reference
  CLI
  Artifact Contracts
  Product-Agent OS Plugin Spec

Internal Evidence
  Source Registry
  Source Packets
  Plans And Run Logs
```

Reader journey map:

| Reader | Entry page | Next page | Exit artifact |
| --- | --- | --- | --- |
| Product or executive reviewer | `docs/product-agent-os/index.md` | `docs/product-agent-os/scenarios.md` | Presentation-level understanding of Product-Agent OS value, principles and approval boundaries. |
| Operator | `docs/product-agent-os/live-runtime-governance.md` | `docs/product-agent-os/approval-bound-real-testing.md` | Approval packet or accepted gap decision. |
| Builder | `docs/diagrams/index.md` | `docs/product-agent-os/cli-reference.md` | Smallest safe implementation slice with commands and verification. |
| Docs maintainer | this packet | `docs/sources/registry.md` | Registry/backlog/control-plane sync without leaking internal ledger language into public pages. |

Page ownership map:

| Owner | Pages | Responsibility |
| --- | --- | --- |
| Product Docs Lead | `docs/product-agent-os/index.md`, `docs/product-agent-os/scenarios.md`, `docs/product-agent/overview.md` | Value proposition, reader routes, product principles and presentation copy. |
| Architect | `docs/diagrams/*`, `docs/product-agent-os/architecture.md`, `docs/product-agent-os/live-runtime-governance.md` | Operating model, boundaries, decisions and failure modes. |
| Builder | `docs/product-agent-os/cli-reference.md`, `docs/product-agent-os/artifact-contracts.md`, `docs/product-agent-os/technical.md` | Commands, artifacts, install/runtime details and examples. |
| Tester / Reviewer | `docs/product-agent-os/behavioral-evals.md`, `docs/product-agent-os/packaging-and-closure.md`, tests and check scripts | Quality gates, forbidden-term policy and closure evidence. |

## B34-PROD-M18 Forbidden-Term Policy

`public_forbidden_terms` for pages marked `public_ready`:

```yaml
public_forbidden_terms:
  exact_words:
    - "Task"
    - "Track"
    - "Batch"
  ledger_patterns:
    - "T[0-9]+-[A-Z0-9-]+"
    - "B[0-9]+-[A-Z]+-M[0-9]+"
  similar_internal_markers:
    - "done_through_m"
    - "approval_required matrix row"
    - "implementation ledger"
```

Allowed contexts:

- internal evidence paths listed in `internal_evidence`;
- code identifiers, commands, filenames, JSON field names and literal artifact ids;
- official OpenAI terms preserved by project rules, including Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, memory, sandbox, approvals, MCP and Agents SDK;
- explicit internal/source links inside evidence packets, not public product prose.

Enforcement state for Batch 34A:

```yaml
public_ready_pages: []
cleanup_pending_public_candidates: "all public_product_candidates listed above"
test_policy: "public_ready pages fail docs tests if they contain public_forbidden_terms outside allowed contexts"
activation_condition: "Batch 34B rewrites a page and marks it public_ready; Batch 34C localizes the equivalent RU/EN page"
```

Batch 34A therefore adds the policy and the future failure condition without falsely claiming that current product-facing candidates are already clean. Batch 34B must remove internal ledger language from the candidate pages before any of them move from `cleanup_pending` to `public_ready`.

Current enforcement state after Batch 34B:

```yaml
public_ready_pages:
  - docs/product-agent-os/index.md
  - docs/product-agent-os/project-code-graph.md
  - docs/product-agent-os/live-runtime-governance.md
  - docs/product-agent-os/approval-bound-real-testing.md
  - docs/product-agent-os/agent-skill-modernization-loop.md
  - docs/product-agent-os/cli-reference.md
  - docs/product-agent-os/artifact-contracts.md
  - docs/product-agent-os/packaging-and-closure.md
  - docs/product-agent-os/technical.md
  - docs/product-agent-os/development-standards.md
  - docs/product-agent-os/methodology-intelligence.md
  - docs/product-agent-os/scenarios.md
  - docs/product-agent-os/behavioral-evals.md
  - docs/product-agent-os/codex-compatibility.md
  - docs/product-agent-os/architecture.md
  - docs/product-agent/overview.md
  - docs/product-agent/lifecycle.md
  - docs/product-agent/roles.md
  - docs/product-agent/control-plane.md
  - docs/product-agent/product-agent-os-plugin-spec.md
  - docs/diagrams/index.md
  - docs/diagrams/architecture.md
  - docs/diagrams/product-delivery-lifecycle.md
  - docs/diagrams/agent-team-and-skills.md
  - docs/diagrams/runtime-decision-map.md
  - docs/diagrams/skill-lifecycle.md
  - docs/diagrams/context-memory-verification.md
  - docs/runtime/overview.md
  - docs/runtime/non-interactive-and-mcp.md
  - docs/runtime/automations-github.md
  - docs/runtime/worktrees-hooks-rules.md
  - docs/agent-systems/subagents-skills.md
  - docs/playbooks/docs-update.md
  - docs/playbooks/use-case-to-plugin.md
  - docs/playbooks/workspace-readiness-audit.md
cleanup_pending_public_candidates: []
```

Batch 34A initial state intentionally keeps `public_ready_pages: []` above for provenance. Batch 34B records the current public-ready promotion in `docs/sources/product-agent-os-batch34b-public-copy-rewrite.md`; Batch 34C must use those public-ready pages as the RU/EN localization source.

## Acceptance

- `B34-PROD-M16`: public product candidates and internal evidence/control-plane surfaces are listed separately.
- `B34-PROD-M17`: presentation IA, reader journey and ownership map are recorded.
- `B34-PROD-M18`: forbidden-term policy, allowlist and future test activation rule are recorded.
- Internal evidence remains staged evidence only and not source of truth for public product copy.
- Boundary phrases for downstream tests and handoff: no live server, no browser automation, no provider/API call, no canonical graph mutation, no git stage/commit/push/PR.
- No plugin publication or external write is performed by this packet.
