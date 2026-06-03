# Packaging and closure

Source status: `official + experiment`

## Назначение

Эта страница фиксирует Batch 34 `T10-LIVE-M35..M36`: Packaging, Docs, Source Registry, Closure And Batch 35 Handoff. Batch 34 делает систему понятной, проверяемой и готовой к owner handoff перед approval-bound real testing, но сам по себе не запускает Batch 35 и не является доказательством live execution.

Batch 34 закрывает docs updated packet, packaging/install smoke definition, required verification, generated `site/` rebuild rule и handoff packet для Batch 35.

## Source-of-truth boundary

Source of truth:

- checked-in Product-Agent OS source docs;
- Track 10 plan and accepted Batch 34 matrix;
- source registry and control-plane artifacts after их отдельного owner-approved/docs-maintainer slice;
- current command evidence from docs tests, `tools/check_docs.py`, strict MkDocs, optional full closure and packaging/install smoke;
- explicit owner approval packets for any later live/browser/provider/canonical/git action.

Not source of truth:

- generated `site/` pages by themselves;
- packaging/install smoke as a release or publish approval;
- plugin-cache contents without checked-in source comparison;
- staged evidence without owner review;
- planning matrix presence without implementation and verification evidence.

## Inputs

Batch 34 closure consumes:

- Task 24 modernization loop docs and metrics-report boundary;
- Task 25 project code graph, cockpit, static search, backend gate, semantic retrieval, deterministic proposal and extension-closure docs;
- Task 26 Batch 24-33 governance/runtime/provider/review/mutation/audit/real-testing-readiness/runtime-QA evidence;
- Batch 34 Detailed Task Matrix `B34-DOC-M01..M15`;
- plugin README install and packaging guidance;
- MkDocs navigation/docs-check requirements from the Builder/Tester slice;
- known gaps: docs-maintainer plugin-cache gap and Mermaid external asset gap when still unresolved.

## Outputs And Artifacts

Expected Batch 34 outputs:

- updated docs pages for Product-Agent OS source docs;
- source registry/backlog/control-plane sync from the owning docs-maintainer slice;
- updated docs contract tests and `tools/check_docs.py` from the owning Builder/Tester slice;
- regenerated `site/` using the regular MkDocs `site_dir`;
- packaging/install smoke evidence packet;
- Batch 35 approval packet draft;
- explicit list of actions not performed without approval.

This worker page covers only the docs packet. It does not update navigation, tests, registry, README, `site/`, git state or plugin distribution.

## Packaging And Install Smoke

Packaging/install smoke is evidence only. It should answer:

- plugin manifest exists and points to the expected bundled skills/MCP metadata;
- checked-in `docs-maintainer` guidance is available, or the docs-maintainer plugin-cache gap is recorded;
- local install path or marketplace candidate can be inspected without publishing;
- staged templates and scripts remain package-readable;
- no secrets, credentials or private data are bundled;
- plugin hooks and automations remain inactive unless explicitly approved;
- install smoke result records command, environment, output summary, gaps and residual risk.

Install smoke does not publish the plugin, write to external systems, create a marketplace release, upload artifacts, activate hooks, create automations or approve Batch 35.

## Workflow And Cadence

Batch 34 verification order is fixed:

1. Source docs.
2. Source registry.
3. Docs contract tests.
4. `python tools\check_docs.py`.
5. Strict MkDocs build.
6. Optional full closure.
7. Packaging/install smoke.
8. Batch 35 handoff packet.

The generated documentation site must be rebuilt with the regular MkDocs `site_dir`:

```powershell
python -m mkdocs build --strict
```

Using only a disposable `--site-dir` is not enough when Batch 34 explicitly requires `site/` refresh.

## Required Verification

Minimum Batch 34 closure evidence:

- focused docs contract test result for new pages, required source status and safety boundaries;
- `python tools\check_docs.py`;
- strict MkDocs build into `site/`;
- `git diff --check`;
- packaging/install smoke packet;
- explicit Batch 35 handoff packet.

Optional full closure when risk or scope requires:

- full unittest with long timeout;
- fixture eval;
- transcript eval;
- Codex compatibility validation;
- reviewer pass over generated `site/`, long-line IA and accepted gaps.

Do not claim Batch 34 is complete unless the current run has matching command evidence or clearly states which verification was not run.

## Batch 35 Handoff

Batch 35 remains approval-bound real testing execution. The handoff packet should list separate approval surfaces:

- `approved_local_runtime_launch`;
- `actual_browser_automation_smoke`;
- `approved_provider_api_pilot`;
- `approved_canonical_mutation_pilot`;
- `explicit_git_release_pr_action`.

Each surface needs owner, approved target, data policy, redaction/cache/budget boundary where relevant, rollback/disable path, expected evidence, residual risk and stop condition.

Batch 35 can start only after Batch 24 governance, Batch 25 runtime contract, Batch 31 audit/observability, Batch 32 target consent, Batch 33 QA/performance/stabilization and Batch 34 packaging/docs closure are current.

## Actions Not Performed Without Approval

Batch 34 does not perform these actions without a separate explicit owner approval:

- no live server launch;
- no browser automation;
- no provider calls;
- no live external model/API calls;
- no canonical graph mutation;
- no plugin publication;
- no external write;
- no package registry or marketplace upload;
- no hook activation;
- no active schedules, automations or GitHub Actions creation;
- no `git add`, commit, push or PR;
- no Batch 35 execution.

## Risks And Failure Modes

- Treating packaging smoke as publish approval can create an unauthorized release.
- Rebuilding a disposable site but not `site/` leaves stale generated docs.
- Missing docs registry/control-plane sync can make source-backed claims drift.
- Plugin-cache mismatch can hide missing checked-in skills, especially `docs-maintainer`.
- Mermaid external asset dependency can break offline documentation expectations.
- Batch 35 can accidentally start live execution if approval surfaces are bundled together instead of separated.

## Next Action

After Batch 34 docs and packaging evidence are current, the next safe artifact is the Batch 35 approval packet draft. Real testing execution, provider/API calls, canonical mutation and git release/PR actions remain blocked until their separate approvals exist.
