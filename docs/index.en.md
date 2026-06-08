# Product-Agent OS

Source status: `official + experiment`

Product-Agent OS is the operating model for running Codex work as product delivery: requirements, planning, agent ownership, verification evidence, review, packaging and learning stay connected from the first request to the final handoff.

Start with [Product-Agent OS](product-agent-os/index.md) for the product overview, then use the [implementation atlas](diagrams/index.md) to choose the workflow, agent team, runtime surface and verification path.

The documentation keeps internal evidence separate from presentation copy. Public pages explain product value, capabilities, boundaries, outputs and next action. Internal evidence pages under `docs/sources/` store the source registry, packets, backlogs and verification records; they should not be the first route for a new user.

Generated `site/`, dashboards, graphs, cockpit views, reports and smoke results are review artifacts, not source of truth. Source of truth remains in Markdown source files, the source registry, current command/eval/runtime evidence, owner decisions and accepted gaps. Live runtime launch, browser automation, provider/API calls, canonical graph mutation, publication and git release actions stay approval-bound.

## Inputs

- A real project or documentation workflow that needs Codex governance.
- Product-Agent OS pages, diagrams, runtime guidance and playbooks.

## Outputs

- A safe route through product intent, agent team design, implementation, verification and handoff.
- A clear boundary between public product documentation and internal evidence.

## Verification

Use the focused docs tests, `python tools\check_docs.py` and strict MkDocs build after localization or navigation changes.

## Risks

- Treating generated evidence as source of truth can hide stale or unsupported claims.
- Launching live systems, provider calls or git release actions without approval breaks the operating boundary.
