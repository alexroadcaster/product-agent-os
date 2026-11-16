# Discovery and first-run analysis

Source status: repository_source / focused_synthetic_verification; 2026-11-15. The FUNC-G03 owner verifies browser/API integration separately.

Owner: graph-cockpit-engineer + docs-maintainer. Scope: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when scanner, API, adapters, query contracts, tests or PoC status change. Graph outputs are derived orientation evidence, not substitutes for source reading and checks.

## Python: workspace inspection

[discovery.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/discovery.py) discovers stack markers, control-plane files, Codex assets and evidence gaps; [first_run_analysis.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py) assembles first-run orientation. The presence of a file or profile does not prove activation or correct behavior: statuses distinguish missing, present_unverified, present_verified, proposal_staged and approval_required. Decisions and evidence belong to sources and owners, not the dashboard.

## Web: registration and bounded scan

Registration and durable scan have distinct outcomes: scans are queued, retain inventory → documents → code → analysis stages and keep the last usable result separately. Cancellation and restart require explicit retry; partial coverage is not a complete inventory. Code indexing and Python analysis are independent: a ready index does not establish completed analysis. See [inventory](inventory.md) and [lifecycle](../backend/lifecycle.md).

## F29: Python analysis through a safe projection

`apps/local-service/src/project-analysis/service.mts` adapts existing `product_agent_os.discovery.analyze_workspace`. It never calls `run_first_project_analysis`, whose orchestration includes a script matrix even without writing results. Inputs are a registered project and an F28 inventory snapshot, not an arbitrary browser-supplied absolute path.

The adapter builds a separate temporary projection: at most 200 eligible files, 2 MiB text total and 64 KiB per text file. Safe root markers/control-plane files and plugin manifests use checked F28 reads; language, ORM and schema paths become empty metadata placeholders. Sensitive content is omitted explicitly. SQLite/DB files supply permitted metadata only and are never opened. Omission or `not_observed` does not establish absence from the project.

A fixed `bridge.py` runs on Python 3.11+ with `-I -S -B`, `shell:false`, `windowsHide:true`, an environment allowlist and an owned working directory. Project scripts and target Python/config modules are never imported. Isolated mode excludes cwd/user-site and `PYTHON*`; `-S` disables site processing. Flag behavior was checked through Context7 against the [official Python cmdline reference](https://github.com/python/cpython/blob/v3.13.14/Doc/using/cmdline.rst). This bounds inputs; it is not an OS sandbox for untrusted Python core.

The deadline is 15 s; combined stdout/stderr is limited to 128 KiB. Cancellation/timeout stops only the owned subprocess; cleanup removes only its created temporary directory. Projection/output memory is bounded, but there is no separate OS RSS ceiling (`SUBPROCESS_RSS_NOT_OS_LIMITED`). Root identity, policy, inventory revision and publication guards are checked around execution; stale or cancelled results cannot publish. Tracebacks and absolute temporary paths never reach the UI.

`paos_project_analysis_v1` is stored in `scan.latest.stages.analysis.data.analysis`, with no new table or namespace. It retains stack/language/component observations, control plane, findings, schema candidates, confidence, source paths with `line:null`, limitations and revisions. `sourceRevision` identifies inventory. `adapterSourceRevision` hashes a fixed bridge/core/direct dependency/catalog list with SHA256; `runtime` records actual Python version, module and `checkout_projection` deployment. Filename observations remain candidates, not runtime verification. Database navigation stays unavailable without a separate connection.

Checkout lookup uses only adjacent application core. The current desktop distribution omits plugin core/catalog and explicitly returns `ANALYSIS_CORE_UNAVAILABLE`; it never installs dependencies, searches global directories or substitutes another analyzer. Core packaging is a separate task.

Focused synthetic checks: `node --test tests/web/project-analysis.test.mts` (9/9), covering real Python/core, nested plugin manifests, missing runtime/core, deadline, excessive/invalid output, cancellation, root/policy/source changes and preserved target bytes. Receipt: `.tmp/func-g03/f29-service-green.log`. A distinct RED exposed loss of a nested manifest source; GREEN confirmed the fix. The UI passes scoped TypeScript checking; root owns browser integration and final statuses. These checks do not establish production readiness or human acceptance.

## Operational boundary

Discovery can enumerate available signals, but does not execute unknown project scripts or prove runtime, dependencies or readiness. Staged graphs and cockpits are generated evidence. Read current sources before making claims; output does not authorize target mutation or provider calls.

Related checks: [discovery tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_discovery.py), [first-run tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_first_run_analysis.py). References do not imply a new run.

## FUNC-G03 — final verification

Current integrated source, not the initial lower-module handoff: browser19/19; full Web594/594,0skip; backend TypeScript and production build passed. Source/build hashes and screenshots: `.tmp/func-g03/browser-final/evidence-IfLiEa/result.json`. Review policy-race findings are fixed and independently rechecked5/5. Native candidate and production-default receipts: `.tmp/func-g03/native-candidate-reviewed.log`, `native-default-reviewed.log`. Earlier pending/wiring statements describe their dated intermediate slice; final task reports own closure. Checkout core is available; packaged core remains explicitly unavailable. Human/provider acceptance and F14/F33/F34 are separate.
