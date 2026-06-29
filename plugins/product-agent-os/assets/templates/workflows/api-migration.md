# API Migration

Project: {project_name}
Profile: {profile_name}

## Inputs

- User goal:
- Current OpenAPI sources:
- Current AsyncAPI sources:
- Current examples and documentation:
- Proposed target contract:
- Framework-native or current-tooling option:
- Custom protocol or custom client rationale:
- Consumers:
- Generated clients or SDKs:
- Versioning and deprecation policy:
- Backwards compatibility constraints:
- Rollout and release impact:
- Owner review and approval boundary:

## Process

1. Keep the workflow read-only until the migration plan, owner review, and approval boundary are explicit.
2. Inventory current state from OpenAPI, AsyncAPI, examples, generated clients, docs, changelog, and release files.
3. Describe target state before implementation: endpoints, events, schemas, examples, generated clients, and observable behavior.
4. Build the consumer impact map: direct consumers, generated clients, SDKs, integrations, docs, examples, and unknown consumers.
5. Classify backwards compatibility for each contract change as compatible, additive, deprecated, breaking, or unknown.
6. Mark compatibility as `present_unverified` until contract check evidence, generated client checks, consumer review, or owner evidence supports it.
7. Prefer OpenAPI/AsyncAPI/framework-native tooling, existing SDK generation, current clients, and compatibility adapters before custom protocol, custom serializer, or new dependency choices.
8. Define idempotency, error/retry/timeout behavior, deprecation, rollout, release impact, validation, and rollback before code changes.
9. Do not implement contract changes, do not update generated clients, and do not release before the migration plan, contract check evidence, owner review, and approval exist.
10. Do not publish docs, packages, SDKs, schemas, or release notes to external systems without explicit approval.

## Outputs

- Migration plan:
- API contract review:
- Current state:
- Target state:
- Consumer impact map:
- Generated clients impact:
- Backwards compatibility table:
- Framework-native leverage decision:
- Idempotency/error/retry/timeout decision:
- Deprecation plan:
- Examples and docs updates:
- Rollout plan:
- Release impact:
- Validation plan:
- Contract check evidence:
- Rollback plan:
- Owner review:
- Approval requirements:
- Residual risk:

## Verification

- OpenAPI and AsyncAPI sources are listed or marked `applicable_missing`.
- Each contract change has a compatibility classification and evidence status.
- Consumers and generated clients are mapped before implementation.
- Examples, docs, deprecation, rollout, release impact, validation, and rollback are explicit.
- Contract check evidence names the command, tool, manual review, or owner evidence required.
- Custom protocol, custom client, custom serializer, or new dependency choices have rejected native/current-tooling alternatives and owner-reviewed risk.
- External publishing and release actions remain blocked until explicit approval.

## Stop Conditions

- Contract sources are missing or ambiguous.
- Consumers, generated clients, or release impact are unknown for a public contract.
- Backwards compatibility is claimed without contract check evidence.
- Custom protocol, custom client, or new dependency is proposed before framework-native/current-tooling options are evaluated.
- Owner review or approval is missing for breaking, deprecated, or externally visible changes.
- The request asks to implement or release before the migration plan is complete.
