# Plan B4 — execution, evidence and recovery

Source status: local implementation, disposable target evidence and pinned Windows runtime qualification.

The implementation order followed `06`, `13 → 14 → 15`, `16`, `17 → 18`, and
`21`. Write checks used disposable projects. The owner-approved release status
remains `hold`. [Task cards and criteria](../../planning/user-project-methodologies-2026-11-15.en.md#delivery-groups) · [B2 decision](paos-pmeth-b2-evidence.en.md#rollout-decision)

## CLI and delivery plan {#cli-planning}

| Task | Observed behavior and verification |
| --- | --- |
| PMETH-06 | The stored snapshot binds the task, criteria, checks and observed revisions, including API contracts, schema and control settings. Comparison returns changed paths and criteria, rename candidates and owner reviews. An explicit delivery plan adds affected slices. Tests cover unchanged inputs, a foreign project, concurrent owner document and criterion edits, a missing owner and identical bytes at a new path. |
| PMETH-13 | The compact assignment describes scope, criteria, sources, checks, write boundaries and stop conditions. Local `--contract` inherits host policy and proposes serial execution. Tests distinguish unknown parallel capability, timeout and stale handoff. A report dispatches no retry. |
| PMETH-14 | The route selects packaged skills and workflows for applicable methods. Package discovery keeps installation, session exposure and invocation distinct. Offline routing supplies a manual next action and leaves host availability unknown. |
| PMETH-15 | An explicit flag builds one DAG using `formation_plan` and canonical ownership from `methodology_synthesis`. Tests cover reusing `requirements.md`, a RED prerequisite for a Python bug and the absence of design and FSD branches for this backend task. Extended branches need journey or import evidence. |

`test_pmeth_b4.py` exercises `run_contract` and the public CLI. Changed inputs
trigger review by the relevant owner. Each `AC-n` refers to the named task
revision. [Operator commands](../../product-agent-os/methodology-intelligence.en.md#methodology-execution)

## Preview and approved writes {#approved-writes}

PMETH-16 uses the existing writers. G9 forms the bundle through
`render_infrastructure.py`, stages it outside the target and passes it to
`merge_infrastructure.py`. Apply checks the reviewed approval, root identity,
input bytes and file state. The atomic publish refuses a name another writer has
already created. Each stage admits one attempt and keeps its rollback journal.
Tests verify exact rollback and preservation of a concurrent edit.

F13 accepts `methodology` with a task ID, revision and criteria for a linked
document only. The metadata enters the approval digest. SQLite checks the task
revision again at commit admission. A scoped rollback requires the applied bytes
to match its receipt. Existing proposals retain their wire contract. A synthetic
API test verifies stale approval rejection and document preservation after a task edit.

## Evidence, decisions and recovery {#evidence-and-recovery}

PMETH-17 binds a `native_command_broker` observation to one explicitly reviewed
criterion and pins the command, criterion, specification, source, environment and
authority. In the synthetic flow, owner acceptance covers two criteria. One
technical row is `passed` with a receipt and the other is `missing`. An edit or
profile change makes the first observation `stale`. The offline CLI reports
caller observations with their own provenance and freshness.

PMETH-18 adds a versioned record in the existing SQLite store. Tasks, scans and
check observations retain their owners. The decision records its reason, author,
time, scope and history. Tests cover compare-and-set, replay after acknowledgement,
project isolation and backup restore. Restore keeps history and makes the old scope
stale. The SQL schema stays at its current version.

PMETH-21 surfaces unresolved outcomes and routes users to the existing Sessions
controls. A lost result and an App-agent restart produced no second dispatch.
Recovery regressions cover checkpoints, Stop, permission changes, dropped
acknowledgements and a bounded retry budget. The browser shows an accepted gap
alongside the independent technical outcome.

## Verification {#local-verification}

- `python -B -m unittest discover -s tests -p 'test_*.py' -q` passed. The run covered 1,401 tests in 671.573 seconds with one Windows skip. Local plugin compatibility was `compatible`.
- The focused Python run passed **109/109** with isolated `TEMP` and `TMP`, covering B4, B1, formation, merge and the CLI contract. An earlier publication implementation received `WinError 5` from `os.link`. Windows now uses exclusive-name `os.rename`. The rerun passed, including a concurrent write immediately before publication.
- The full `node --test --test-concurrency=1 tests/web/*.test.mts` run passed **727/727** on authorized Windows with no skips. The final focused rerun passed **44/44**, including rollback after a later edit and preserving a newer record. `npm run check:web-m1` and `npm run build:web` passed.
- `tests/web/single-window/methodology-advice-browser-acceptance.mts` passed **53/53**. An isolated Chromium exercised the recommendation, keyboard, evidence view, gap disposition, reload and 400 px layout. The Windows sandbox blocked the initial startup. The authorized disposable-profile run passed. Report SHA-256 `7fccafce542f112e5f88fa538addac02b81bdb11c7aa3d458d609a85beeead43`.
- Candidate and default native admission passed for `28f94cf0ba8fcffc98f619ad9b08907c1f1b784c0b80d5567f9737a172461db8`. The harness exercised scoped writes, three manifest drift rejections and Stop. Candidate SHA-256 `6e9cd688ef2a3680ca73c40bc6c81da1c467078e160967351cc2803ca8ed1591`. Default SHA-256 `c787b54566aa3a7e8888514310bff037c55fcfc726b2183163e4c00125c2f56b`.
- Context7 `/nodejs/node/v26.0.0` supplied the `DatabaseSync` and prepared statement reference. The project runs on Node.js `26.5.0`. [Node.js reference](https://github.com/nodejs/node/blob/v26.0.0/doc/api/sqlite.md)

PMETH-23 profile acceptance, agent usefulness, real-project FSD migration and an
expanded release require their own evidence and owner decisions.
