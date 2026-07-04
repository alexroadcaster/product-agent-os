# Batch 45 docs/source sync review

## Scope

Read-only audit for Batch 45 source-backed documentation, registry, RU/EN parity and control-plane consistency.

Allowed write: this report only.

Explicit no-change boundary: no edits to `docs/`, `docs/sources/registry.md`, `docs/sources/registry.en.md`, root control-plane files, `mkdocs.yml`, `site/` or git.

Review type: inspection-only. No docs checks were run because the request was an independent read-only audit and no source docs were changed.

## Sources read

- `AGENTS.md` lines 31-40, 52-58, 112-121.
- `PLAN.md` lines 34-38.
- `TEST.md` lines 144-214, 247-252, 261-281, 293-329, 438-444.
- `EVALS.md` lines 77-81, 83, 88-89, 107, 168-172.
- `RUNLOG.md` lines 9, 84-85, 150-153; file size observed as 51,123 bytes.
- `docs/sources/registry.md` lines 54-71 and 1579-1588.
- `docs/sources/registry.en.md` lines 54-71 and 1580-1589.
- `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md` lines 440-454 and 466-488.
- `docs/product-agent-os/coding-standards.md` lines 3-5, 22-41, 55-68.
- `docs/product-agent-os/coding-standards.en.md` lines 3-5, 22-41, 55-68.
- `docs/product-agent-os/technical.md` lines found by search for `Professional Code Authoring`.
- `docs/product-agent-os/technical.en.md` lines found by search for `Professional Code Authoring`.
- `docs/superpowers/specs/batch45-*.json`, especially:
  - `batch45-agent-behavior-eval-results.json` lines 1-24 and 81-106.
  - `batch45-comment-policy-promotion-decision.json` lines found by search for `status`, `no_go`, unsupported claims and approval boundary.
  - `batch45-real-project-decision-packet.json` lines 1-35.
  - `batch45-real-project-scorecard.json` lines found by search for `source_status`, unsupported claims and promotion decision.
- `mkdocs.yml` lines 116-130 and 264-278.
- `tests/product_agent_os/test_product_agent_os_docs.py` search hits for `coding-standards.md`, `Source status:` and generated site freshness checks.

## Consistency findings

### P0

None found.

No evidence found that public docs, registry or control-plane currently claim Batch 45 production readiness, CI/blocker promotion, target mutation, browser/runtime proof, deploy/release/publish, or real AI-agent behavior improvement.

### P1

None found.

Core Batch 45 status is consistent across source packets and root control-plane:

- `PLAN.md:34` records S6 as advisory/no-go and blocks real AI-agent behavior improvement, active automation, browser/runtime proof, target mutation, root site freshness and release-style claims.
- `PLAN.md:35` records S7 as fixture-local/source-only, with M35 keeping advisory-only/no-go and disposable runtime/browser pilot as approval-required.
- `EVALS.md:79` records M26 baseline `4.22`, treatment `3.88`, `15/16` completed, warnings `29 -> 15`, reviewer `no_go`, plus `promotion_no_go_keep_advisory_only`.
- `EVALS.md:80` records S7 M28-M35 as source/fixture-local only and rejects target/runtime/browser/provider/database/git/release/deploy/automation behavior claims.
- `RUNLOG.md:150-153` keeps the current handoff compact: S6 closed as no-go/advisory-only and S7 source-only with no target/runtime/browser/provider/db/git/release/deploy/automation proof.

### P2

1. Public Professional Code Authoring page is stale relative to S6/S7 decisions, although it does not overclaim.

   Evidence:
   - `docs/product-agent-os/coding-standards.md:5` and `docs/product-agent-os/coding-standards.en.md:5` cite Batch 45 research and S5 packets, but do not cite the S6 no-go or S7 decision packets.
   - `docs/product-agent-os/coding-standards.md:55-68` and `.en.md:55-68` cap evidence at `docs_contract_ready` / `synthetic_green` plus unsupported runtime/hook/automation/provider/cache/target/git/release claims. They do not name the later M26/M27 no-go or M35 advisory-only/no-go decision.
   - Source packets have moved on: `batch45-agent-behavior-eval-results.json:81-106` records treatment underperformance and reviewer `no_go`; `batch45-real-project-decision-packet.json:25-35` records `keep_advisory_only_no_go_for_treatment_v2_promotion` and approval-required runtime/browser pilot.

   Impact:
   - Not a false readiness claim. The page remains conservative.
   - It is still source drift for a public page because the current Batch 45 ceiling is stronger and more specific than the page says: advisory-only/no-go after live eval and fixture-local S7.

2. `RUNLOG.md` is effectively at the control-plane size boundary.

   Evidence:
   - Observed file size: 51,123 bytes.
   - The workflow budget is 50 KiB, i.e. 51,200 bytes.
   - `RUNLOG.md:9` says detailed historical ledgers and batch marker banks belong in source-owned files, `prod_test.md` and registry entries.
   - `RUNLOG.md:150-153` already uses a compact two-line Batch 45 handoff.

   Impact:
   - Any future Batch 45 sync to `RUNLOG.md` can exceed the budget with even a short paragraph.
   - Future fixes should route detail to source-owned packets or registry markers, not expand `RUNLOG.md`.

### P3

1. Registry RU/EN parity is mostly good, but the registry has two Batch 45 marker layers with different freshness.

   Evidence:
   - Current discoverability entries exist in both registries: `docs/sources/registry.md:54-71` and `docs/sources/registry.en.md:54-71` cover S0-S7 including baseline, refactor comparison, scorecard and decision packet.
   - A lower detailed marker block includes S6 at `docs/sources/registry.md:1579-1588` and `docs/sources/registry.en.md:1580-1589`, but does not continue with equivalent S7 M28-M35 marker details before switching to Batch 44.

   Impact:
   - This is not a blocking parity failure because the top-level S7 entries exist in both RU and EN registries.
   - It is a maintenance smell: readers relying on the lower detailed marker bank may think S7 is absent or less canonical than S6.

2. Public nav includes Professional Code Authoring in RU and EN, but the label remains English in the RU nav.

   Evidence:
   - `mkdocs.yml:125` and `mkdocs.yml:273` both route `product-agent-os/coding-standards.md` as `Professional Code Authoring`.
   - This is acceptable for canonical English terms, but it differs from nearby localized labels in the RU nav.

   Impact:
   - Low. No routing break found.
   - If the docs team wants stricter RU UI consistency, keep the canonical term but consider a mixed label such as `Professional Code Authoring standards`.

3. `Source status:` policy appears satisfied for relevant Batch 45 public pages.

   Evidence:
   - `docs/product-agent-os/coding-standards.md:3` and `.en.md:3` include `Source status:`.
   - Search for missing `Source status:` under `docs/` returned only `docs/index.md`, which is an index page and outside the non-index requirement in `AGENTS.md:34`.

   Impact:
   - No docs edit required for this policy.

## Docs/source debt

- Update the public Professional Code Authoring RU/EN page to cite S6 and S7 current evidence packets, especially:
  - `docs/superpowers/specs/batch45-agent-behavior-eval-results.json`
  - `docs/superpowers/specs/batch45-comment-policy-promotion-decision.json`
  - `docs/superpowers/specs/batch45-real-project-scorecard.json`
  - `docs/superpowers/specs/batch45-real-project-decision-packet.json`
- Keep the page concise: one sentence in `Evidence ceiling` is enough to say the current outcome is `advisory-only/no-go`, S7 is fixture-local/source-only, and runtime/browser/provider/target/git/release claims remain unsupported.
- Consider normalizing the lower registry marker bank so it either includes a compact S7 M28-M35 block or clearly points readers back to the current top-level S7 entries.
- Preserve `RUNLOG.md` as a compact handoff layer. Do not add Batch 45 details there unless old content is first redistributed.

## Recommended doc/control-plane fixes

1. `docs/product-agent-os/coding-standards.md`
   - Add S6/S7 packets to the `Источники:` line or a compact "Current evidence" sentence.
   - Replace the current `Evidence ceiling` sentence with one that names:
     - S6 live eval no-go.
     - M27 keep-advisory-only decision.
     - S7 fixture-local decision no-go for treatment v2.
     - runtime/browser/provider/target/git/release/deploy/automation still unsupported.

2. `docs/product-agent-os/coding-standards.en.md`
   - Apply the same parity update in English.

3. `docs/sources/registry.md` and `docs/sources/registry.en.md`
   - Optional, not blocking: add a compact detailed S7 marker after the S6 marker block, or remove dependence on the lower marker bank by making the top current entries the only Batch 45 discoverability surface.

4. Root control-plane
   - `PLAN.md`, `EVALS.md`, and `RUNLOG.md` do not need urgent Batch 45 correction based on this audit.
   - Avoid expanding `RUNLOG.md`; it has only about 77 bytes of headroom against the configured 50 KiB budget.

## Checks to run

If the recommended docs/registry fixes are applied:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
git diff --check
```

Run strict MkDocs only if `mkdocs.yml`, localized nav, Markdown extensions, search/sitemap behavior or generated `site/` evidence changes:

```powershell
.venv-docs\Scripts\python.exe -m mkdocs build --strict
```

Do not claim root `site/` freshness unless a current build writes to `site/` and the required site/search/sitemap checks run. Smoke builds under `.docs-tools/reports/` are source/nav proof, not root-site freshness.

## No-change boundaries

- Did not edit `docs/`.
- Did not edit `docs/sources/registry.md` or `docs/sources/registry.en.md`.
- Did not edit root control-plane files.
- Did not edit `mkdocs.yml`.
- Did not inspect or modify generated `site/`.
- Did not stage, commit, branch, push or open PR.
- Did not run browser automation, provider/model calls, live servers, external writes, dependency installs or target-workspace commands.
- Observed pre-existing dirty worktree entry: `.codex/config.toml`. It was not touched by this review.

## Control-plane sync decision

- `REQUIREMENTS.md`: `not_applicable` - audit did not change scope or acceptance.
- `PLAN.md`: `handoff_required` only if owner accepts the public-page/registry cleanup as a follow-up; no direct edit in this read-only review.
- `TEST.md`: `not_applicable` - existing docs checks remain sufficient for the recommended fix.
- `EVALS.md`: `not_applicable` - Batch 45 no-go and S7 source-only ceilings are already present.
- `RUNLOG.md`: `handoff_required` if any future current-cycle handoff must mention this review; do not expand until size budget is handled.
- `prod_test.md`: `not_applicable`.
- `RUNLOG.md` overflow decision: near-budget risk; keep details in this source-owned review report and source packets, not in `RUNLOG.md`.

## Confidence

High for root control-plane and source packet consistency: current Batch 45 no-go/advisory-only boundaries are present in `PLAN.md`, `EVALS.md`, `RUNLOG.md`, registry top entries and source-owned JSON packets.

Medium-high for public docs debt: the public Professional Code Authoring page is conservative but stale relative to S6/S7. The recommended change is a small source-sync update, not a behavioral or readiness change.

Report written to `.codex/product-agent-os/reviews/batch45/agent-04-docs-source-sync.md`.
