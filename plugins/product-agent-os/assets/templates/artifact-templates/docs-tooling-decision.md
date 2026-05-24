# Docs Tooling Decision

Project: {project_name}
Profile: {profile_name}
Detected stack: {detected_stack_text}

## Purpose

Use this artifact to make `docs_tooling_selector` decisions explicit and to close the `docs_as_code_impact` gate without forcing a docs portal, CI, CODEOWNERS, hosted docs, or database introspection where they do not apply.
Artifact: `docs-tooling-decision.md`.

## Status Vocabulary

- `not_applicable`: docs tooling is not justified for this slice or workspace.
- `present_unverified`: a docs artifact or tool is present, but no current command evidence proves it works.
- `present_verified`: a docs artifact or tool is present and current command evidence proves it works.
- `proposal_staged`: a tool or governance change is proposed but not applied.
- `explicit_gap_accepted`: the owner accepted the gap temporarily with residual risk.
- `approval_required`: external write, hosted docs approval, DB introspection approval, CI/CODEOWNERS activation, dependency install, publishing, sharing, or workflow activation needs explicit approval.

## Decision

- `docs_as_code_impact` status:
- Evidence owner:
- Maintenance owner:
- Selected tools:
- Rejected tools:
- Rejected because:
- Docs-light or internal-only reason:
- Accepted gap:
- Residual risk:

## Tool Matrix

| Tool or path | Applicability | Status | Command or evidence | Approval need |
| --- | --- | --- | --- | --- |
| MkDocs | Markdown docs, small/medium docs portal |  | `mkdocs build --strict` | no forced install |
| Docusaurus | React/MDX/product docs, versioning or i18n |  | `docusaurus build` | no forced install |
| Sphinx | Python package/library reference docs |  | `sphinx-build` | import-safety review |
| Antora | enterprise or multirepo AsciiDoc docs |  | `antora` | no forced install |
| Read the Docs | hosted public docs/versioning |  | hosted build evidence | hosted docs approval |
| OpenAPI | HTTP API source-of-truth contracts |  | OpenAPI lint/build | no forced install |
| AsyncAPI | event/message source-of-truth contracts |  | AsyncAPI lint/build | no forced install |
| Storybook | reusable UI components/design system states |  | Storybook build | no forced install |
| Mermaid | Markdown-native architecture and sequence diagrams |  | docs build/render check | no forced install |
| PlantUML | UML/sequence diagrams when the team already uses PlantUML |  | PlantUML render | no forced install |
| Structurizr DSL | larger architecture-as-code/C4 model workspaces |  | Structurizr validate | no forced install |
| DBML/dbdocs | lightweight database docs |  | DBML validation/docs build | no secrets |
| SchemaSpy | DB introspection docs path |  | SchemaSpy proposal | DB introspection approval |
| TypeDoc | public TypeScript package or SDK reference |  | TypeDoc build | no forced install |
| JSDoc | public JavaScript package or SDK reference |  | JSDoc build | no forced install |
| Javadoc | public Java API reference |  | Javadoc build | no forced install |
| XML docs | public .NET API reference |  | XML docs build | no forced install |
| Vale | public docs, regulated terminology, style governance |  | Vale lint | proposal staged |
| markdownlint | Markdown quality where existing lint culture exists |  | markdownlint | proposal staged |

## Safety Rules

- No forced install.
- No CI activation without approval.
- No CODEOWNERS activation without approval.
- Hosted docs approval is required before external sharing, hosted builds, or publishing.
- DB introspection approval is required before database access, schema introspection, or credentials-sensitive commands.
- Keep docs-light and internal-only projects on a lightweight path unless the owner explicitly asks for a portal or governance tooling.
- Do not store secrets, credentials, private customer data, raw private chat logs, connection strings, or unpublished roadmap details.

## Verification

- Current command evidence:
- Current eval evidence:
- Current runtime evidence:
- Link check or docs build:
- Owner review:
- Claims still `present_unverified`:
