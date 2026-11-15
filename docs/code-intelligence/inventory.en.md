# Inventory and scan boundaries

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: graph-cockpit-engineer + docs-maintainer. Scope: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when scanner, API, adapters, query contracts, tests or PoC status change. Graph outputs are derived orientation evidence, not substitutes for source reading and checks.

## Web source inventory

[sources.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/sources.mts) verifies registered root identity and ancestors; excludes sensitive directories/paths, symlinks and multiply hard-linked files, and checks UTF-8, drift and root containment. Traversal is bounded to depth 32, 10,000 directory entries and 1,000 eligible files. This is a bounded source inventory, not a visible tree of all files or a universal ignore-file implementation.

The graph [service.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/service.mts) limits total size to 8 MiB, one file to 512 KiB, 25,000 nodes, 50,000 edges and parser worker time to 10 seconds; up to eight snapshots. Other languages eligible for inventory receive `unsupported` coverage; linked sources can be `excluded`. A hard limit raises an error rather than guaranteeing a safe complete truncation.

## Python manifest

[project_graph_manifest.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_manifest.py) builds normalized file records, sizes, fingerprints, languages and generated flags; [project_code_graph.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_code_graph.py) uses them for the graph. Read the scanner for actual exclusion policies: Web and Python do not promise identical inventories. Generated paths may appear in the manifest without semantic overlays.

Compare revision/manifest, coverage and errors before using an index. Limits, encoding, omitted paths and drift must remain visible; results are not an audit of every project file. F26–F29 plan an independent file directory and managed scanning.

Checks: [Web source tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [manifest tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_manifest.py). This text does not claim a new runtime run.
