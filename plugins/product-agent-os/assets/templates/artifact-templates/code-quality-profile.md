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

- `evidence_ceiling`: declared inventory only; no tool execution or verification.
- `proposed_commands_not_run`: `true`
- `installation_performed: false`
- `commands_executed: false`
