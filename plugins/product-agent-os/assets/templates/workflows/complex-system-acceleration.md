# Complex System Acceleration

Project: {project_name}
Profile: {profile_name}

## Inputs

- Goal:
- Experienced owner:
- Web slice:
- API slice:
- Integration slice:
- Database slice:
- Docs slice:
- Eval slice:
- Release slice:
- External systems:
- Approval boundary:

## Process

1. Map web slice, API slice, integration slice, database slice, docs slice, eval slice and release slice before assigning parallel work.
2. Build or update the integration catalog for every external system, webhook, event stream, queue, generated client, SDK or data exchange.
3. Define ownership boundaries by subsystem and exact files.
4. Define parallelization rules: independent files, independent systems, independent verification commands and explicit merge order.
5. Check OpenAPI for HTTP contracts and AsyncAPI for event or message contracts.
6. Check DB/docs impact for schema, migration, retention, database dictionary and docs-as-code changes.
7. Define eval and test gates for each slice.
8. Define release gates: compatibility, migration, changelog, rollback, monitoring and approval needs.
9. Produce fresh-context task packets before parallel work.

## Outputs

- Integration catalog:
- Ownership boundaries:
- Parallelization rules:
- OpenAPI impact:
- AsyncAPI impact:
- DB/docs impact:
- Eval gates:
- Release gates:
- Agent task packets:
- Approval needs:

## Scenario Handoff

Keep the handoff concise enough for the next role to act without reading raw conversation history.

- Sources/context used:
- Assumptions:
- Files touched:
- Files proposed:
- Verification evidence:
- Open risks:
- Recommended next role:
- Stop reason:

## Verification

- Every planned parallel worker has owned files and forbidden files.
- Every external system has an integration catalog entry.
- Contract changes name OpenAPI, AsyncAPI or an explicit not-applicable status.
- DB/docs impact is named even when not applicable.
- Release gates include rollback and approval needs.
- Safety phrase: do not parallelize when files, external systems, migrations or release gates overlap.

## Stop Conditions

- Ownership boundaries are unclear.
- Integration catalog is missing for a touched external system.
- Parallel workers would edit overlapping files.
- Contract, database, docs, eval or release impact is unknown.
- Required external system, production data, secret-bearing config, deployment, hosted docs or publish approval is unavailable.
