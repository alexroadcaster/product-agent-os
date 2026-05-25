# Architecture Docs Tooling Decision

Source status: `local methodology artifact`

Project: {project_name}

Use this artifact for `architecture_docs_as_code_present`, `diagram_render_check_present`, architecture-as-code, render check, stale-doc detection and accepted gap decisions. Architecture-as-code is conditional: use it when diagrams must survive review, diff, build or CI; otherwise record `not_applicable` or `explicit_gap_accepted`.

## Decision

- Architecture docs status:
- Evidence owner:
- Maintenance owner:
- Selected tool:
- Rejected tools:
- Docs-light reason:
- Accepted gap:
- Residual risk:

## Tool Matrix

| Tool | Applicability | Render check | Validation evidence | Approval need |
| --- | --- | --- | --- | --- |
| Mermaid | Markdown-native C4-lite, sequence and flow diagrams | docs build/render check |  | no forced install |
| Structurizr DSL | C4 architecture-as-code for larger models | Structurizr validate |  | no forced install |
| PlantUML | UML or sequence diagrams when already used | PlantUML render |  | no forced install |
| arc42 Markdown | Structured architecture docs | docs build/check_docs |  | no forced install |
| C4 static image | Inspection-only or early sketch | owner review |  | accepted gap if no render check |

## Render Check

- Diagram source:
- Command:
- Output:
- Failure mode:
- Owner:
- Status: `not_applicable | present_unverified | present_verified | proposal_staged | explicit_gap_accepted | approval_required`

## Stale-Doc Detection

- Boundary or ADR files watched:
- Contract files watched:
- Runtime/deployment files watched:
- Review cadence:
- Owner:

## Safety Rules

- Do not force architecture-as-code for docs-light prototypes.
- Do not force Well-Architected review for non-cloud work.
- Do not claim rendered diagram proves correctness; owner review and source-backed evidence are still required.
- No forced install.
- No CI activation without approval.
- No secrets, credentials, private customer data, raw private chat logs, connection strings or unpublished roadmap details stored in this artifact.

## Verification

- Current command evidence:
- Current eval evidence:
- Current runtime evidence:
- Owner review:
- Accepted gap:
- Residual risk:
