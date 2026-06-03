# Packaging and closure

Source status: `official + experiment`

## Назначение

Эта страница фиксирует packaging, documentation closure и owner handoff для Product-Agent OS. Closure делает систему понятной, проверяемой и готовой к approval-bound real testing, но сам по себе не запускает live execution.

Closure packet описывает обновленные source docs, packaging/install smoke definition, required verification, generated `site/` rebuild rule и approval packet для следующего execution step.

## Source-of-truth boundary

Source of truth:

- checked-in Product-Agent OS source docs;
- accepted implementation plan and docs closure scope;
- source registry and control-plane artifacts after their separate owner-approved/docs-maintainer slice;
- current command evidence from docs tests, `tools/check_docs.py`, strict MkDocs, optional full closure and packaging/install smoke;
- explicit owner approval packets for any later live/browser/provider/canonical/git action.

Not source of truth:

- generated `site/` pages by themselves;
- packaging/install smoke as a release or publish approval;
- plugin-cache contents without checked-in source comparison;
- staged evidence without owner review;
- planning matrix presence without implementation and verification evidence.

## Inputs

Closure consumes:

- modernization loop docs and metrics-report boundary;
- project code graph, cockpit, static search, backend gate, semantic retrieval, deterministic proposal and extension-closure docs;
- governance/runtime/provider/review/mutation/audit/real-testing-readiness/runtime-QA evidence;
- accepted docs closure scope;
- plugin README install and packaging guidance;
- MkDocs navigation/docs-check requirements from the Builder/Tester slice;
- known gaps: docs-maintainer plugin-cache gap and Mermaid external asset gap when still unresolved.

## Outputs And Artifacts

Expected closure outputs:

- updated docs pages for Product-Agent OS source docs;
- source registry/backlog/control-plane sync from the owning docs-maintainer slice;
- updated docs contract tests and `tools/check_docs.py` from the owning Builder/Tester slice;
- regenerated `site/` using the regular MkDocs `site_dir`;
- packaging/install smoke evidence packet;
- approval packet draft for real testing execution;
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

Install smoke does not publish the plugin, write to external systems, create a marketplace release, upload artifacts, activate hooks, create automations or approve real testing execution.

## Workflow And Cadence

Closure verification order is fixed:

1. Source docs.
2. Source registry.
3. Docs contract tests.
4. `python tools\check_docs.py`.
5. Strict MkDocs build.
6. Optional full closure.
7. Packaging/install smoke.
8. Approval-bound handoff packet.

The generated documentation site must be rebuilt with the regular MkDocs `site_dir`:

```powershell
python -m mkdocs build --strict
```

Using only a disposable `--site-dir` is not enough when closure explicitly requires `site/` refresh.

## Required Verification

Minimum closure evidence:

- focused docs contract test result for new pages, required source status and safety boundaries;
- `python tools\check_docs.py`;
- strict MkDocs build into `site/`;
- `git diff --check`;
- packaging/install smoke packet;
- explicit approval-bound handoff packet.

Optional full closure when risk or scope requires:

- full unittest with long timeout;
- fixture eval;
- transcript eval;
- Codex compatibility validation;
- reviewer pass over generated `site/`, long-line IA and accepted gaps.

Do not claim closure is complete unless the current run has matching command evidence or clearly states which verification was not run.

## Approval-Bound Handoff

Real testing execution remains approval-bound. The handoff packet should list separate approval surfaces:

- `approved_local_runtime_launch`;
- `actual_browser_automation_smoke`;
- `approved_provider_api_pilot`;
- `approved_canonical_mutation_pilot`;
- `explicit_git_release_pr_action`.

Each surface needs owner, approved target, data policy, redaction/cache/budget boundary where relevant, rollback/disable path, expected evidence, residual risk and stop condition.

Real testing can start only after governance, runtime contract, audit/observability, target consent, QA/performance/stabilization and packaging/docs closure evidence are current.

## Actions Not Performed Without Approval

Packaging and closure work does not perform these actions without a separate explicit owner approval:

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
- no real testing execution.

## Risks And Failure Modes

- Treating packaging smoke as publish approval can create an unauthorized release.
- Rebuilding a disposable site but not `site/` leaves stale generated docs.
- Missing docs registry/control-plane sync can make source-backed claims drift.
- Plugin-cache mismatch can hide missing checked-in skills, especially `docs-maintainer`.
- Mermaid external asset dependency can break offline documentation expectations.
- Real testing can accidentally start live execution if approval surfaces are bundled together instead of separated.

## Next Action

After docs and packaging evidence are current, the next safe artifact is the approval packet draft. Real testing execution, provider/API calls, canonical mutation and git release/PR actions remain blocked until their separate approvals exist.
