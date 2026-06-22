# Graph Intelligence Contract

Source status: `project evidence`

Graph intelligence helps operators orient inside a project, but it remains generated orientation evidence. It does not replace source files, tests, checked-in docs, approval records, or owner decisions.

The graph ontology, rejected-link ledger, freshness gates, and bounded queries are navigation aids. Graph packets remain orientation evidence until source reads, command evidence, owner review, or accepted gaps support a stronger claim.

## Layer Contract

| Signal | Role | Boundary |
| --- | --- | --- |
| Ontology | Node, edge, observation, contract, and semantic overlay types. | Does not guarantee runtime behavior. |
| Coverage map | Which languages, docs, schemas, and tests the scanner saw. | Does not prove full project coverage. |
| Freshness | Digest, timestamp, changed-since, and supersession metadata. | A stale graph blocks readiness wording. |
| Rejected links | Ledger of conservatively rejected edges. | Rejection is caution evidence, not failure by itself. |
| Query packets | Bounded `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `read_order`, `hotspots`, `status`, `search`. | A query result does not replace source reads. |

## Safe Use

Use the graph to choose files to read, estimate blast radius, find hotspots, and prepare handoff. Before an edit, fix, readiness, or release claim, open the owning source and run the current verification gate.

## Unsafe Use

Do not perform mutation, provider calls, browser proof, target apply, or git actions from graph evidence alone. Do not upgrade `present_unverified` to `present_verified` without command evidence, owner review, or an accepted gap.

## Freshness Gates

A graph is stale when source files changed after generation, manifest digests do not match, the query packet is not tied to the current graph, or baseline comparison shows unreviewed deltas. The next safe action is to refresh the generated graph only within approved/local scope or read source directly.

## Verification

Minimum docs gate for this page: source registry marker, docs tests, `tools/check_docs.py`, strict MkDocs smoke, and `git diff --check`. Focused graph tests are needed only when scanner, ontology, or query code changes.
