# Code Quality Profile

Project: `{project_name}`

- `schema_version`: `code_quality_profile_v1`
- `inventory_status`: `present_unverified`
- `installation_performed: false`
- `commands_executed: false`

This is an inventory-derived profile. It records declared evidence only and does
not execute, install, or verify any tool or project utility.

## Stack Profiles

| family | languages | status | marker_evidence |
| --- | --- | --- | --- |
| `<family>` | `<languages>` | `present_unverified` | `<marker_evidence>` |

## Existing Project-Native Tools

| family | category | name | status | sources | proposed_commands_not_run |
| --- | --- | --- | --- | --- | --- |
| `<family>` | `<category>` | `<name>` | `present_unverified` | `<sources>` | `<proposed_commands_not_run>` |

Missing applicable categories remain `applicable_missing`; an empty tool row is
not evidence that a tool is absent from the project.

## Project Utilities

| name | status | source | proposed_command |
| --- | --- | --- | --- |
| `<name>` | `present_unverified` | `<source>` | `<proposed_command>` |

Project utilities are inert profile data. A listed command is not authorization
to run it.

## Gaps

- `applicable_missing`: `<family>:<category>`
- No declared inventory signal establishes operational behavior or correctness.

## Evidence Ceiling

Record installed version and actual command receipt separately from declared inventory. Use version/config/resolver/aliases/type-only policy, scan scope and exclusions when interpreting a tool result. Missing or reduced coverage is unknown. Use allowed and forbidden/transitive control fixtures for architecture rules. Distinguish known/new/stale violations; never grow a baseline or mark suppression as a fix automatically. Before adopting Desloppify, inspect license/distribution fit and cost. Upgrade or unsafe-fix changes need scoped diff and applicable verification; this profile only proposes report-only checks.

- `evidence_ceiling`: declared inventory only; no tool execution or verification.
- `proposed_commands_not_run`: `true`
- `installation_performed: false`
- `commands_executed: false`

## Optional Architecture Receipt

Use `capability_summary(..., architecture_context=..., architecture_receipts=(...), architecture_baseline=...)` only with independently computed current context and reviewed scoped scanner observations. The normal discovery route remains declaration-only; it does not load reports or execute tools automatically. `architecture_evidence` binds tool/version/config/input/policy digests. Policy includes dependency lock, scope/exclusions, resolver/aliases and type-only semantics. Controls must contain allowed/forbidden/transitive evidence. Completed scans with complete coverage may be verified even with findings; verified_clean additionally requires no findings. Baseline comparison never modifies historical findings: known/new_or_changed/absent_candidate, the last is not a fix claim. Failed or incomplete baseline is not comparable. Receipt contents are trusted local observations, not arbitrary uploaded reports; validate privacy and scope before supplying them.
