# Discovery and first-run analysis

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: graph-cockpit-engineer + docs-maintainer. Scope: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when scanner, API, adapters, query contracts, tests or PoC status change. Graph outputs are derived orientation evidence, not substitutes for source reading and checks.

## Python: workspace inspection

[discovery.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/discovery.py) discovers stack markers, control-plane files, Codex assets and evidence gaps; [first_run_analysis.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py) assembles first-run orientation. The presence of a file or profile does not prove activation or correct behavior: statuses distinguish missing, present_unverified, present_verified, proposal_staged and approval_required. Decisions and evidence belong to sources and owners, not the dashboard.

## Web: registration and bounded scan

During project registration with scan, [HTTP application](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/http/application.mts) invokes source inspection and the [code index service](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/service.mts). Registration and scan have distinct outcomes: failures and partial coverage do not constitute a complete project inventory. Memory snapshots require rebuild after restart. See [inventory](inventory.md) for bounds and F26–F29.

## Operational boundary

Discovery can enumerate available signals, but does not execute unknown project scripts or prove runtime, dependencies or readiness. Staged graphs and cockpits are generated evidence. Read current sources before making claims; output does not authorize target mutation or provider calls.

Related checks: [discovery tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_discovery.py), [first-run tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_first_run_analysis.py). References do not imply a new run.
