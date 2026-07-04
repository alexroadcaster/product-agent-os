# Batch 45 Product / Scenario Scorecard Review

Source status: independent read-only product/scenario review. Target workspaces, code, docs, git, runtime, browser automation, provider/API calls, databases, deployments, publications and automations were not changed or executed.

## Scope

Review focus: product usefulness of Batch 45 Professional Code Authoring and the `B45-S7` real-project scenario harness, especially scenario coverage, representativeness, scorecard decision quality, unproven user/owner value, smaller treatment v2 route, and material fixes that would improve outcome rather than only documentation.

Allowed write: this report only: `.codex/product-agent-os/reviews/batch45/agent-06-product-scenarios-scorecard.md`.

Out of scope: editing Batch 45 source packets, code, root control-plane files, source registry, git state, runtime/browser proof, provider/model calls, target command execution, target mutation, database access, release/deploy/publish or automation activation.

## Sources read

- `research/b45-real-project-scenarios/README.md`
- `research/b45-real-project-scenarios/source-inventory.md`
- `research/b45-real-project-scenarios/source-policy.md`
- `research/b45-real-project-scenarios/scenario-candidates.json`
- `research/b45-real-project-scenarios/fixtures/sol/SOL-AGENT-ORCH-01/README.md`
- `research/b45-real-project-scenarios/fixtures/sol/SOL-AGENT-ORCH-01/scenario-manifest.json`
- `research/b45-real-project-scenarios/fixtures/sol/SOL-AGENT-ORCH-01/fixture-manifest.json`
- `research/b45-real-project-scenarios/results/SOL-AGENT-ORCH-01-baseline.json`
- `research/b45-real-project-scenarios/refactors/sol/SOL-AGENT-ORCH-01/original/README.md`
- `research/b45-real-project-scenarios/refactors/sol/SOL-AGENT-ORCH-01/checklist-guided/README.md`
- `research/b45-real-project-scenarios/refactors/sol/SOL-AGENT-ORCH-01/advisory-guided/README.md`
- `research/b45-real-project-scenarios/fixtures/mypartners/MP-CRM-CHAT-OPEN-01/README.md`
- `research/b45-real-project-scenarios/fixtures/mypartners/MP-CRM-CHAT-OPEN-01/scenario-manifest.json`
- `research/b45-real-project-scenarios/fixtures/mypartners/MP-CRM-CHAT-OPEN-01/fixture-manifest.json`
- `research/b45-real-project-scenarios/results/MP-CRM-CHAT-OPEN-01-baseline.json`
- `research/b45-real-project-scenarios/refactors/mypartners/MP-CRM-CHAT-OPEN-01/README.md`
- `research/b45-real-project-scenarios/refactors/mypartners/MP-CRM-CHAT-OPEN-01/manifest.json`
- `docs/superpowers/specs/batch45-real-project-baseline-results.json`
- `docs/superpowers/specs/batch45-real-project-refactor-comparison.json`
- `docs/superpowers/specs/batch45-real-project-scorecard.json`
- `docs/superpowers/specs/batch45-real-project-decision-packet.json`
- `docs/superpowers/specs/batch45-agent-behavior-eval-results.json`
- `PLAN.md`
- `EVALS.md`

## Product findings

### P0

No P0 product blocker found in the decision itself. The current decision does not overclaim promotion: M35 keeps advisory-only/no-go, rejects CI/blocker promotion, and leaves runtime/browser pilot approval-required (`docs/superpowers/specs/batch45-real-project-decision-packet.json:26`, `docs/superpowers/specs/batch45-real-project-decision-packet.json:31`, `docs/superpowers/specs/batch45-real-project-decision-packet.json:124`, `docs/superpowers/specs/batch45-real-project-decision-packet.json:143`).

### P1

1. The scorecard is product-wise correct to block promotion, but the average scores can mislead an owner if read outside the blocker policy. The scorecard shows a best static arm at `7.4` and checklist arm at `6.8`, while also saying aggregate score is not a promotion gate and critical blockers override averages (`docs/superpowers/specs/batch45-real-project-scorecard.json:87`, `docs/superpowers/specs/batch45-real-project-scorecard.json:88`, `docs/superpowers/specs/batch45-real-project-scorecard.json:158`, `docs/superpowers/specs/batch45-real-project-scorecard.json:191`). Product impact: a reviewer could mistake "good static score" for "safe to apply", although the evidence only supports no-go/static routing.

2. Product value remains unproven for actual user workflow outcomes. M32 ran no target commands and no runtime/browser/provider actions (`docs/superpowers/specs/batch45-real-project-baseline-results.json:40`, `docs/superpowers/specs/batch45-real-project-baseline-results.json:41`), and M33 states it cannot prove target behavior, production safety, release readiness or real AI-agent behavior improvement (`docs/superpowers/specs/batch45-real-project-refactor-comparison.json:18`). Product impact: the harness currently proves risk discipline and reviewer orientation, not that Professional Code Authoring improves shipped code behavior.

3. SOL coverage is representative for TypeScript backend orchestration as a risk-control scenario, but not as a treatment-success scenario. The SOL baseline records 3 blockers, 2 accepted gaps, no runnable fixture test path, TypeScript advisory gap and provider/vector runtime boundary (`docs/superpowers/specs/batch45-real-project-baseline-results.json:51`, `docs/superpowers/specs/batch45-real-project-baseline-results.json:53`; `research/b45-real-project-scenarios/results/SOL-AGENT-ORCH-01-baseline.json:185`, `research/b45-real-project-scenarios/results/SOL-AGENT-ORCH-01-baseline.json:188`). Product impact: the SOL no-code outcome is useful churn prevention, but cannot validate a code-authoring treatment v2.

### P2

1. Scenario coverage is intentionally narrow and honest, but not broad enough for a general product-success claim. The inventory lists seven scenario candidates plus deferred families, while S7 executed two scenarios (`research/b45-real-project-scenarios/scenario-candidates.json:178`, `research/b45-real-project-scenarios/scenario-candidates.json:238`, `docs/superpowers/specs/batch45-real-project-scorecard.json:16`). The README explicitly says the repeat pass prioritizes high-signal Professional Code Authoring scenarios rather than complete whole-project topology (`research/b45-real-project-scenarios/README.md:13`). Product impact: coverage supports a conservative decision gate, not representative rollout confidence.

2. The selected pair is defensible as a first harness: `SOL-AGENT-ORCH-01` covers backend agent orchestration, while `MP-CRM-CHAT-OPEN-01` covers a richer CRM workflow with backend/frontend and privacy-sensitive evidence boundaries (`research/b45-real-project-scenarios/README.md:47`, `research/b45-real-project-scenarios/README.md:51`, `research/b45-real-project-scenarios/README.md:74`, `research/b45-real-project-scenarios/README.md:77`). Product impact: representativeness is good for "first evidence slice", not for "Professional Code Authoring works across codebases".

3. myPartners fixture quality is stronger than SOL for scenario harness usefulness because it includes many focused backend/frontend tests as copied context, but those tests were not run as behavior proof. The manifest copies focused CRM backend and frontend tests (`research/b45-real-project-scenarios/fixtures/mypartners/MP-CRM-CHAT-OPEN-01/fixture-manifest.json:88`, `research/b45-real-project-scenarios/fixtures/mypartners/MP-CRM-CHAT-OPEN-01/fixture-manifest.json:169`, `research/b45-real-project-scenarios/fixtures/mypartners/MP-CRM-CHAT-OPEN-01/fixture-manifest.json:178`), while the fixture README says runtime/browser/provider/target command success remain unproven (`research/b45-real-project-scenarios/fixtures/mypartners/MP-CRM-CHAT-OPEN-01/README.md:20`). Product impact: strong candidate for next proof, but still not a target-safe refactor.

4. The scorecard correctly identifies the comment-only arm risk. The best low-churn MP arm removes warnings, but the scorecard itself says it improves review intent more than behavior structure and lacks proof of safer/correct route behavior (`docs/superpowers/specs/batch45-real-project-scorecard.json:196`, `docs/superpowers/specs/batch45-real-project-scorecard.json:200`). Product impact: this is a good source-only treatment v2 seed only if framed as reviewer-signal calibration, not product behavior improvement.

### P3

1. The source policy is strong and product-safe: it separates allowed source classes, forbidden classes, read-only proof, and explicitly states read-only proof is not runtime proof (`research/b45-real-project-scenarios/source-policy.md:30`, `research/b45-real-project-scenarios/source-policy.md:42`, `research/b45-real-project-scenarios/source-policy.md:102`, `research/b45-real-project-scenarios/source-policy.md:112`). This materially improves privacy and approval discipline.

2. The decision packet has useful future-go criteria, but the next experiment should be phrased as a measurable hypothesis, not a generic "more pilots" route. M35 already requires a specific owner-chosen route and a promotion packet above baseline without critical regressions (`docs/superpowers/specs/batch45-real-project-decision-packet.json:131`). This is enough to prevent plan drift if the next slice stays narrow.

## Scenario coverage assessment

Coverage quality: adequate for a conservative first S7 harness and no-go decision; insufficient for broad product usefulness.

Represented well:

- TypeScript backend agent orchestration and role-agent complexity through `SOL-AGENT-ORCH-01`.
- Python/FastAPI CRM route workflow with frontend/test context through `MP-CRM-CHAT-OPEN-01`.
- Privacy/source-policy handling across two targets with different risk profiles.
- Churn prevention, unsupported-claim discipline, dependency avoidance and reviewer-orientation signals.

Underrepresented or not proven:

- Runtime/browser behavior: explicitly absent from M32/M33 and approval-required in M35.
- Provider/live API, database and production-data safety: deliberately out of scope.
- TypeScript comment/advisory coverage: missing for SOL, making zero warnings weak evidence.
- AI/RAG/retrieval behavior and Worker/provider boundaries: candidate families exist but were not selected.
- Visual/frontend behavior: frontend tests were copied for MP, but browser/e2e was not executed.
- Real AI-agent behavior improvement: M26 already produced a live no-go, and S7 does not reverse that.

## Decision quality

The M35 decision is product-wise justified: keep advisory-only/no-go, do not promote CI/blocker, and allow smaller treatment v2 only as source-only future design. This follows the live M26 no-go and the M34 promotion-blocking scorecard (`docs/superpowers/specs/batch45-agent-behavior-eval-results.json:98`, `docs/superpowers/specs/batch45-agent-behavior-eval-results.json:100`, `docs/superpowers/specs/batch45-real-project-decision-packet.json:33`).

The strongest part of the decision is that it treats S7 as a promotion-risk calibration layer, not a success story. This matches `EVALS.md`, which says real-project confidence requires target evidence where project structure, source policy, workflow, runtime signals or owner judgment matter (`EVALS.md:34`) and that S7 does not prove target/runtime/browser/provider/database/git/release/deploy/automation behavior or real AI-agent improvement (`EVALS.md:80`).

The weakest part is communication risk: static averages and "best current arm" language are useful internally, but they need a visible "blocker-first" interpretation in any owner-facing summary. Without that, the `7.4` advisory-guided score could be read as readiness.

## Recommended next experiments/fixes

1. Run a tiny source-only treatment v2 design on `MP-CRM-CHAT-OPEN-01`, but measure it as reviewer-signal quality, not behavior improvement. Hypothesis: a smaller advisory can reduce decorative comments and unsupported claims without pushing structural churn. Stop before target apply unless characterization/runtime approval exists.

2. Create a fixture-local characterization route for MP CRM before any structural refactor claim. Best material fix: adapt the copied focused tests into a runnable isolated fixture test or write a minimal static/import-safe characterization check. This improves outcome more than adding more decision prose because it turns copied tests from context into evidence.

3. Add TypeScript advisory coverage or an explicit TS static-test substitute before using SOL for treatment v2. Without this, SOL should remain a churn-prevention case only.

4. If owner wants product confidence rather than scorecard confidence, prepare `B45-PCA-M36` as a disposable runtime/browser pilot approval packet for MP CRM only. It must name target, commands/browser actions, rollback/delete path, data boundary, provider/API boundary, evidence artifacts and stop conditions, matching M35's approval boundary (`docs/superpowers/specs/batch45-real-project-decision-packet.json:143`).

5. Recalibrate the scorecard display so blocker status dominates averages. Material product fix: show `promotion_result` and `critical_blockers` before average scores, or compute a capped "promotion confidence" of `blocked` whenever runtime/test/reviewer/behavior blockers are present.

## Stop/continue criteria

Stop / no-go remains correct while any of these are true:

- No runtime/browser/provider-safe evidence for the selected treatment.
- No runnable characterization evidence for a structural MP CRM refactor.
- No TypeScript advisory/static substitute for SOL.
- No owner/reviewer agreement that score weights match real project risk.
- Any route would imply CI/blocker promotion after M26/M27 no-go.

Continue only if the next slice is one of:

- Source-only smaller treatment v2 design with explicit no-target-apply ceiling.
- Fixture-local characterization/test route for MP CRM.
- TypeScript/static advisory coverage for SOL.
- Approval-gated disposable runtime/browser pilot packet, not execution, unless the owner grants exact execution approval.

## Confidence

Confidence: medium-high for the no-go/product decision assessment, because the scorecard, decision packet, baseline and EVALS/PLAN claim ceilings are internally consistent. Confidence is medium for representativeness conclusions because the audit is read-only and does not rerun tests, runtime, browser, target commands, provider calls, or owner-review calibration.

Control-plane sync decision: `not_applicable_for_root_updates` for this review. The task is an independent read-only report and does not change requirements, sequencing, verification policy, eval thresholds, Batch 39 ledger state, or canonical Batch 45 evidence. Detailed output is source-owned by this review artifact.

Report path written: `.codex/product-agent-os/reviews/batch45/agent-06-product-scenarios-scorecard.md`.
