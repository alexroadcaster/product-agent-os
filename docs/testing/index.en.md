# Product-Agent OS verification

Source status: repository_source / static_contract_review; DG06, 2026-11-15.

Owner: verification owner + docs-maintainer. Scope: Web, local service and packaged Python plugin at revision `259977f3b257ba7fc0e932396f8963262bd327ad`. Update when test routes or evidence boundaries change. Links to checks identify their owners; they do not imply a new run.

[TEST.md](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/TEST.md) owns current command selection and escalation conditions. [EVALS.md](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/EVALS.md) owns rubrics, thresholds and claim boundaries. Dated results retain their original revision, environment and scope; a result does not become current when relevant inputs change.

1. Select the changed contract and consumers in the [test map](test-map.md), then consult TEST for the current route.
2. Establish what [synthetic, runtime and human evidence](synthetic-vs-live.md) can support and which checks remain open.
3. For AI changes define a baseline, cases, thresholds and limits using [AI evals](ai-evals.md); for documentation use [documentation checks](documentation-checks.md).
4. Record actual commands, results, revision, environment, data, failures and residual risk in the owning evidence artifact. Follow the separate authority boundaries for the selected action.

When a check is missing, use `not_verified` or `blocked` with its reason and next action. A passing test proves only its assertions and setup; it does not establish autonomous success on another project or release readiness. Related sources: [behavioral evals](../product-agent-os/behavioral-evals.md), [retrieval evaluation](../ai/rag/evaluation.md), [frontend accessibility](../frontend/accessibility.md). Wider product claims need relevant actual checks, owner review and, where applicable, human acceptance.
