# Prompt and output contracts

Source status: repository_source / current_source_inspection; DG05, 2026-11-15.

Owner: runtime/LLM owner + docs-maintainer. Scope: PAOS implementation at `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update with route, prompt/output, credential, budget or telemetry contracts. Test links identify verification routes, not a new runtime run.

## Ownership inventory

| Surface / owner | Input and instructions | Output and gate |
| --- | --- | --- |
| [M1 recipe](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/m1-recipe.mts) + [coordinator](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/codex/coordinator.ts) | Fixed `m1_fixed_v1`, analyst/planner/builder for discussion/planning/execution; developerInstructions separate from JSON-quoted task/user data | Correlated thread/turn events, messages and evidence; turn completion is not owner acceptance |
| [App gateway team proposal](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-gateway.mts) | `team_proposal_generation_v1`, catalog/target/request as untrusted data, planning-only policy | One JSON proposal or clarification; kind/action/target/content/dependencies/reason, separate preview/apply |
| [Skill generation](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/team/skill-generation.mts) | REQUIREMENTS revision/lines or description, existing skill metadata, stable generationKey | SKILL.md create with YAML name/description and requirementIds; or noGap/reason, clarification; stale/invalid/duplicate_candidate not silently applied |
| [Recipe step input](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-gateway.mts) | `bounded_recipe_step`, frozen step/task/pins, iteration/attempt and predecessorArtifacts | Correlated run/report; successful prose is not checks/Done evidence |
| [Python extraction](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py) | Redacted graph + semantic index, approved `local_deterministic`, external calls false | Semantic node/edge/rationale proposals, review_required and fingerprints; not live generation |
| [Python provider gate](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_proposal_provider.py) | Approved redacted prompt schema/evidence IDs, governance and budget/eval policies | Structured JSON proposal contract/safety eval; canonical mutation forbidden, this builder does not make an external call |

## Context and validation

`quotedTaskInput` redacts and JSON-encodes task context, bounds saved context at 64 KiB and separates user text from fixed instructions. Instructions are not a sandbox mechanism: runtime guards and the host own enforced boundaries. [Agent context](../agents/context.md), [tools/approvals](../agents/tools-approvals.md).

Skill generation checks the current requirement digest before returning a result, validates schema/frontmatter and provenance, presents a preview, then a separate Apply checks its digest and uses a stable key. A completed run does not imply automatic installation or application of model prose. This path requires an App-side consumer.

Python extraction checks approval and graph/semantic fingerprints, then produces proposals locally. The provider gate retains `provider_enabled:false`, `accepted_for_canonical_graph:false`, and excludes raw source/secrets/absolute paths. `ready` means contract readiness, not a network call. [Retrieval boundaries](../rag/index.md).

The packaged [prompt-contract template](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/assets/templates/artifact-templates/prompt-contract.md) is a target-project template, not an active Web prompt. Fixture prompts do not establish production model calls either. Do not duplicate complete instructions in documentation as a second owner; change source and related evals in a separately scoped change.

Checks: [M1 recipe](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/runtime-adapter-gateway.test.mts), [skill generation](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/skill-generation-artifacts.test.mts), [local extraction](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_llm_extraction.py), [provider gate](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_llm_proposal_provider.py). These are verification references; no new model/eval calls were made.
