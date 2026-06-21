# Architecture Intelligence diagram atlas

Source status: `project-plan + local-docs-boundary`

Эта страница собирает `DOC-M23` diagram atlas для `architecture_intelligence_design_contract_v1`. Она показывает first-run flow, artifact pipeline, graph depth, methodology routing, approval gates, site sync, source registry loop и deferred `Structurizr DSL` trigger criteria без установки `Structurizr DSL` и без копирования stale generated site views.

## First-run flow

```mermaid
flowchart TD
    A["workspace source context"] --> B["architecture_intelligence_design_contract_v1"]
    B --> C["first_run_cockpit_artifact_v1"]
    C --> D["analysis renderer"]
    D --> E["Architecture Intelligence cockpit"]
    E --> F{"Evidence boundary"}
    F -->|source files| G["source-backed guidance"]
    F -->|strict MkDocs| H["local Markdown/Mermaid render"]
    F -->|browser screenshot proof| I["browser proof approval_required"]
    F -->|missing evidence| J["unsupported claims"]
```

## Artifact pipeline

```mermaid
flowchart LR
    A["source packet"] --> B["artifact manifest"]
    B --> C["renderer"]
    C --> D["view model"]
    D --> E["status rollup"]
    D --> F["scorecard"]
    D --> G["diagram atlas notes"]
    E --> H["handoff"]
    F --> H
    G --> H
```

## Graph depth and methodology routing

```mermaid
flowchart TD
    A["project graph input"] --> B{"Depth requested"}
    B -->|bounded| C["graph depth traversal"]
    B -->|unsafe or broad| D["approval gate"]
    C --> E["entity overlay"]
    E --> F["methodology routing"]
    F --> G{"Detected domain"}
    G -->|docs/source| H["docs-maintainer"]
    G -->|architecture boundary| I["architect"]
    G -->|quality/eval| J["tester or reviewer"]
    G -->|runtime/browser| K["DOC-M25 approval path"]
```

## Approval gates, site sync and source registry loop

```mermaid
flowchart TD
    A["doc or artifact claim"] --> B{"Source-backed?"}
    B -->|Yes| C["source registry loop"]
    B -->|No| D["unsupported claims"]
    C --> E{"Registry update in scope?"}
    E -->|Yes| F["update registry with owner evidence"]
    E -->|No| G["handoff_required"]
    D --> H["record safe next action"]
    H --> I{"Needs browser proof?"}
    I -->|Yes| J["browser proof approval_required"]
    I -->|No| K["local docs-only closure"]
    J --> L["DOC-M25"]
    F --> M{"Site sync approved?"}
    G --> M
    M -->|No| N["generated `site` freshness deferred"]
    M -->|Yes| O["strict MkDocs and site evidence"]
```

## Structurizr DSL trigger criteria

```mermaid
flowchart TD
    A["architecture question"] --> B{"Mermaid enough?"}
    B -->|Yes| C["local Mermaid diagram"]
    B -->|No| D{"Needs durable system model?"}
    D -->|No| C
    D -->|Yes| E{"Owner approved architecture-as-code?"}
    E -->|No| F["Structurizr DSL deferred"]
    E -->|Yes| G["Structurizr DSL candidate"]
    G --> H["separate tooling and source-registry plan"]
```

## Как применять

Используйте atlas как маршрутную карту, когда Architecture Intelligence output затрагивает несколько доказательных поверхностей. Сначала определите источник claim: source file, first-run artifact, generated view, `strict MkDocs`, browser runtime или owner evidence. Затем выберите next role и не повышайте generated view до source truth.

`local Mermaid` подходит для текущих diagram atlas pages и reviewer handoff. `Cosmos.gl/WebGL` относится к интерактивной graph/cockpit поверхности и не доказывается через Markdown. `browser screenshot proof` и browser proof approval_required остаются отдельным `DOC-M25` маршрутом.

## Related artifacts

- Track 11 G3 source context for `DOC-M23`.
- `architecture_intelligence_design_contract_v1`.
- `first_run_cockpit_artifact_v1`.
- `DOC-M25` browser proof follow-up.
- Source registry loop in `docs/sources/registry.md` and `docs/sources/registry.en.md` when registry edits are in scope.
- Local Mermaid diagram pages under `docs/diagrams/`.

## Common failure modes

- Stale generated `site` view is copied into source docs instead of being re-derived from source context.
- Graph depth output is treated as complete architecture understanding without source-file inspection.
- Methodology routing detects a domain but skips ownership, evidence boundary or handoff.
- `strict MkDocs` rendering is conflated with browser screenshot proof or `Cosmos.gl/WebGL` runtime behavior.
- `Structurizr DSL` is installed or introduced before trigger criteria and owner approval exist.
- Source registry loop is skipped for a source-backed claim when registry edits are in scope.
- `unsupported claims` are hidden instead of kept as explicit risks and safe next actions.
