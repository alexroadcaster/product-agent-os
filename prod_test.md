# Product-Agent OS Batch 39 Production Test Ledger

Source status: Batch 39 execution ledger template. This file becomes current execution evidence only when filled during actual Batch 39 test runs. Do not store secrets, tokens, private keys, customer data, raw private chat logs, raw private source bodies or unredacted absolute user-specific paths.

## Purpose

`prod_test.md` is the required ledger before any `B39-S1..B39-S5` execution starts. It records every Batch 39 test, every attempt, failed or blocked runs, Product-Agent OS changes made because of a failure, and the retest evidence that proves whether the change fixed the issue.

This file complements generated artifacts such as `pilot-run-manifest.json`, `command-results.jsonl`, `pilot-summary.json`, `pilot-scorecard.json`, `redaction-report.json`, `target-mutation-proof.json`, `batch39-rollup.json/md`, `doubt_verification_packet`, `completion_skeptic_manual_pilot_ledger`, `completion_skeptic_scorecard_calibration` and `completion_skeptic_go_no_go_closure`. Generated artifacts may be attached as evidence, but this ledger is the human-readable run history.

## Fill Rules

- Add one row to the test index before starting a test.
- Add one attempt row for every run, including failed, blocked, interrupted and approval-required runs.
- If a test fails and Product-Agent OS changes are needed, add a defect/change row before editing implementation files.
- Link every Product-Agent OS change back to the failed attempt that caused it.
- Increment `attempts_total` after every rerun.
- Do not mark a test `passed` until current verification evidence exists in this run.
- Do not hide expected safety blocks as success; use `blocked_expected` with reason and safe next action.
- Keep raw logs in staged artifacts only after redaction. In this file, store short summaries, digests and artifact paths.
- When a user asks for HTML artifacts, the final HTML files must be saved inside the user's project folder, or inside the explicit path requested by the user. External staging directories are allowed only as intermediate build locations; do not leave the user-facing deliverable in a third location unless the user explicitly asks for that location.
- Record exact approvals for any live server, browser automation, provider/API call, canonical graph mutation, external write, automation activation, target apply or git action.
- For any Batch 39 attempt that claims work is done, verified, release-ready, promotable or safe to hand off, record `completion-skeptic` evidence or an owner-reviewed accepted gap.
- Do not treat B40 synthetic-local calibration as real pilot value, automation readiness, public/team release readiness or broad semantic usefulness.
- Keep `completion-skeptic` promotion status `manual_only` / `not_promoted` unless real pilots, owner review and exact approval support a different decision.

## Status Taxonomy

| Status | Meaning | Release impact |
| --- | --- | --- |
| `planned` | Test is defined but not started. | No readiness evidence. |
| `running` | Test is currently in progress. | No readiness evidence yet. |
| `passed` | Current attempt passed all acceptance and verification gates. | Can support readiness only with artifacts and no-action proof. |
| `failed` | Test produced an unexpected technical or product failure. | Blocks readiness until fixed and retested or accepted by owner. |
| `fixed_pending_retest` | Product-Agent OS was changed, but the failing test has not passed again yet. | Blocks readiness. |
| `blocked_expected` | Test hit an intended safety or approval boundary. | Can support readiness if reason and safe next action are clear. |
| `blocked_unexpected` | Test could not run because of an unplanned blocker. | Blocks readiness until resolved or accepted. |
| `approval_required` | Test needs an exact approval before it can continue. | Blocks the relevant claim until approved and evidenced. |
| `warning` | Test passed core gate but found a non-blocking issue. | Requires owner review before closure. |
| `accepted_gap` | Owner accepted an unresolved limitation with residual risk. | Must be visible in go/no-go packet. |
| `deferred` | Test intentionally moved out of Batch 39 scope. | Blocks any claim that depends on it. |

## Batch 40 Completion-Skeptic Ledger Contract

Batch 40 added a local/manual Doubt / verifier loop. Batch 39 must preserve it as a production-hardening gate, not as release proof.

Required fields for any attempt that uses or should use `completion-skeptic`:

| Field | Meaning | Required when |
| --- | --- | --- |
| `doubt_packet_ref` | Relative reference to `doubt_verification_packet` or `none`. | Any completion/readiness claim is made. |
| `completion_skeptic_verdict` | `pass`, `revise`, `needs_more_context`, `blocked_by_approval`, `accepted_risk`, `blocked`, `not_run` or `accepted_gap`. | Every attempt row. |
| `completion_skeptic_trigger` | Explicit trigger, implicit completion claim, route recommendation, skipped or not applicable. | Every attempt row. |
| `unsupported_claims` | Count or short summary of unsupported claims kept visible. | Verdict is not `pass`. |
| `accepted_gap_refs` | Owner-reviewed accepted-gap refs with residual risk and follow-up. | Evidence is missing, stale, synthetic-only or approval-bound. |
| `scorecard_ref` | Pilot scorecard or `completion_skeptic_scorecard_calibration` reference. | Scorecard, rollup, metrics-loop or go/no-go rows. |
| `promotion_boundary` | `manual_only`, `not_promoted`, `synthetic_only_boundary`, `owner_review_required` or approved override ref. | Every Batch 39 closure and release-governance attempt. |

Required B40 failure classes:

| Failure class | Meaning | Release impact |
| --- | --- | --- |
| `false_pass_blocked` | A pass/readiness claim was blocked because current evidence was missing, stale or generated-view-only. | Supports safety only if the safe next action is clear. |
| `false_rewrite_blocked` | The verifier prevented unsupported rewrite churn. | Non-blocking if the original claim remains supported; otherwise follow up. |
| `fake_evidence_rejected` | User-claimed, invented or unverified command/source evidence was rejected. | Blocks readiness until current evidence exists or owner accepts the gap. |
| `missing_current_evidence` | A required check/source/tool trace was absent. | Blocks the dependent claim. |
| `generated_view_not_proof` | Dashboard/site/report/graph output was used as proof instead of underlying evidence. | Blocks readiness until source evidence is linked. |
| `synthetic_only_boundary` | Evidence is deterministic/synthetic-local and cannot prove real user value or release readiness. | Keeps promotion `manual_only` / `not_promoted`. |

## Global Run Metadata

| Field | Value |
| --- | --- |
| Batch | `B39-TEST-M01..M54` |
| Slices | `B39-S1..B39-S5` |
| Ledger status | `template_created_pending_execution` |
| Created at | `2026-06-08` |
| Current owner | `pending_owner_assignment` |
| Current Codex surface | `pending` |
| Current Product-Agent OS source ref | `pending` |
| Current installed cache ref | `pending` |
| Current session-visible skill root | `pending` |
| Target workspace(s) | `pending` |
| Default execution mode | `read_only_staged_first` |
| Approval packet refs | `none_yet` |
| Generated evidence root(s) | `pending` |
| Completion-skeptic rollout boundary | `manual_only_not_promoted_pending_batch39_real_pilot_evidence` |
| Completion-skeptic source packet | `docs/sources/product-agent-os-batch40-doubt-verifier-pilot-closure.md` |
| Completion-skeptic required archetypes | `docs_research`, `code_check`, `expected_block` |
| Final go/no-go status | `not_started` |

## Global Counters

| Metric | Count | Notes |
| --- | ---: | --- |
| Tests planned | 54 | `B39-TEST-M01..M54` |
| Tests started | 0 | Update when first attempt is recorded. |
| Tests passed | 0 | Current verified pass only. |
| Tests failed open | 0 | Unexpected failures not fixed or accepted. |
| Tests blocked expected | 0 | Intended approval/safety blocks. |
| Tests blocked unexpected | 0 | Environment/tooling/blocker issues. |
| Tests accepted gaps | 0 | Owner-reviewed accepted residual risks. |
| Total attempts | 0 | Every run counts, including reruns. |
| Product-Agent OS change sets | 0 | Every fix/change row counts. |
| Retests pending | 0 | Fix made but not rerun. |
| Unapproved actions found | 0 | Must stay zero or route to incident review. |
| Completion-skeptic attempts | 0 | Attempts that ran or explicitly evaluated the manual verifier gate. |
| Completion-skeptic accepted gaps | 0 | Owner-reviewed verifier gaps, including synthetic-only boundaries. |
| Completion-skeptic false passes blocked | 0 | `false_pass_blocked` failure class count. |
| Completion-skeptic false rewrites blocked | 0 | `false_rewrite_blocked` failure class count. |
| Completion-skeptic fake evidence rejected | 0 | `fake_evidence_rejected` failure class count. |
| Completion-skeptic promotions approved | 0 | Must stay zero unless real pilots, owner review and exact approval exist. |

## Test Index

| Test ID | Slice | Priority | Current status | Attempts total | Latest attempt | Product-Agent OS changes | Evidence refs | Open blockers / next action |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| `B39-TEST-M01` | `B39-S1` | P0 | `planned` | 0 | `none` | `none` | `pending` | Normalize source/cache/package/session inventory. |
| `B39-TEST-M02` | `B39-S1` | P0 | `planned` | 0 | `none` | `none` | `pending` | Define `pilot-run-manifest.json` schema. |
| `B39-TEST-M03` | `B39-S1` | P0 | `planned` | 0 | `none` | `none` | `pending` | Build command result collector. |
| `B39-TEST-M04` | `B39-S1` | P0 | `planned` | 0 | `none` | `none` | `pending` | Add pre/post target mutation proof. |
| `B39-TEST-M05` | `B39-S1` | P0 | `planned` | 0 | `none` | `none` | `pending` | Standardize redaction and local-path scrub. |
| `B39-TEST-M06` | `B39-S1` | P0 | `planned` | 0 | `none` | `none` | `pending` | Verify install/update/uninstall and session visibility. |
| `B39-TEST-M07` | `B39-S1` | P0 | `planned` | 0 | `none` | `none` | `pending` | Build Batch 39 rollup aggregator. |
| `B39-TEST-M08` | `B39-S1` | P0 | `planned` | 0 | `none` | `none` | `pending` | Fix status dashboard aggregation for pilot evidence. |
| `B39-TEST-M09` | `B39-S1` | P0 | `planned` | 0 | `none` | `none` | `pending` | Define pilot failure taxonomy. |
| `B39-TEST-M10` | `B39-S1` | P0 | `planned` | 0 | `none` | `none` | `pending` | Define pilot and product-usability scorecard gates. |
| `B39-TEST-M11` | `B39-S2` | P1 | `planned` | 0 | `none` | `none` | `pending` | Prepare synthetic target fixture pack. |
| `B39-TEST-M12` | `B39-S2` | P1 | `planned` | 0 | `none` | `none` | `pending` | Run docs-only happy-path pilot. |
| `B39-TEST-M13` | `B39-S2` | P1 | `planned` | 0 | `none` | `none` | `pending` | Replay `Neural_Flow` expected-block baseline. |
| `B39-TEST-M14` | `B39-S2` | P1 | `planned` | 0 | `none` | `none` | `pending` | Run web/frontend archetype pilot. |
| `B39-TEST-M15` | `B39-S2` | P1 | `planned` | 0 | `none` | `none` | `pending` | Run backend/API archetype pilot. |
| `B39-TEST-M16` | `B39-S2` | P1 | `planned` | 0 | `none` | `none` | `pending` | Run AI/RAG archetype pilot. |
| `B39-TEST-M17` | `B39-S2` | P1 | `planned` | 0 | `none` | `none` | `pending` | Run data/migration archetype pilot. |
| `B39-TEST-M18` | `B39-S2` | P1 | `planned` | 0 | `none` | `none` | `pending` | Run PR/review archetype pilot. |
| `B39-TEST-M19` | `B39-S2` | P1 | `planned` | 0 | `none` | `none` | `pending` | Run automation/release archetype pilot. |
| `B39-TEST-M20` | `B39-S2` | P1 | `planned` | 0 | `none` | `none` | `pending` | Run desktop/native/local-first archetype pilot. |
| `B39-TEST-M21` | `B39-S2` | P1 | `planned` | 0 | `none` | `none` | `pending` | Run plugin/skill project archetype pilot. |
| `B39-TEST-M22` | `B39-S3` | P0 | `planned` | 0 | `none` | `none` | `pending` | Add route accuracy suite for `detect_project.py`. |
| `B39-TEST-M23` | `B39-S3` | P0 | `planned` | 0 | `none` | `none` | `pending` | Add methodology applicability suite. |
| `B39-TEST-M24` | `B39-S3` | P0 | `planned` | 0 | `none` | `none` | `pending` | Test runtime/approval-boundary routing. |
| `B39-TEST-M25` | `B39-S3` | P0 | `planned` | 0 | `none` | `none` | `pending` | Test infrastructure renderer dry-run/stage/apply boundaries. |
| `B39-TEST-M26` | `B39-S3` | P0 | `planned` | 0 | `none` | `none` | `pending` | Test safe merge and rollback workflow. |
| `B39-TEST-M27` | `B39-S3` | P0 | `planned` | 0 | `none` | `none` | `pending` | Test source policy and system-file hygiene. |
| `B39-TEST-M28` | `B39-S3` | P0 | `planned` | 0 | `none` | `none` | `pending` | Test generated status/dashboard surfaces. |
| `B39-TEST-M29` | `B39-S3` | P1 | `planned` | 0 | `none` | `none` | `pending` | Test base project graph scan/query/static index. |
| `B39-TEST-M30` | `B39-S3` | P1 | `planned` | 0 | `none` | `none` | `pending` | Test learning-loop metrics and owner decision support. |
| `B39-TEST-M31` | `B39-S3` | P1 | `planned` | 0 | `none` | `none` | `pending` | Extend fixture/transcript eval coverage. |
| `B39-TEST-M32` | `B39-S3` | P1 | `planned` | 0 | `none` | `none` | `pending` | Add repeatability/performance/output-budget checks. |
| `B39-TEST-M33` | `B39-S3` | P1 | `planned` | 0 | `none` | `none` | `pending` | Run full Product-Agent OS verification after Batch 39 changes. |
| `B39-TEST-M34` | `B39-S5` | P2 | `planned` | 0 | `none` | `none` | `pending` | Sync source-owned docs after full execution evidence exists. |
| `B39-TEST-M35` | `B39-S5` | P0 | `planned` | 0 | `none` | `none` | `pending` | Produce go/no-go decision packet for `B38-PROD-M12`. |
| `B39-TEST-M36` | `B39-S5` | P0 | `planned` | 0 | `none` | `none` | `pending` | Final no-unapproved-actions proof. |
| `B39-TEST-M37` | `B39-S4` | P0 | `planned` | 0 | `none` | `none` | `pending` | Add full public docs/site acceptance. |
| `B39-TEST-M38` | `B39-S4` | P0 | `planned` | 0 | `none` | `none` | `pending` | Add offline asset and dependency readiness. |
| `B39-TEST-M39` | `B39-S4` | P0 | `planned` | 0 | `none` | `none` | `pending` | Add full CLI contract matrix. |
| `B39-TEST-M40` | `B39-S4` | P0 | `planned` | 0 | `none` | `none` | `pending` | Add project graph extension approval-gate tests. |
| `B39-TEST-M41` | `B39-S4` | P0 | `planned` | 0 | `none` | `none` | `pending` | Add graph review, canonical mutation and rollback drills. |
| `B39-TEST-M42` | `B39-S4` | P0 | `planned` | 0 | `none` | `none` | `pending` | Add runtime/browser QA approval harness. |
| `B39-TEST-M43` | `B39-S4` | P0 | `planned` | 0 | `none` | `none` | `pending` | Add security/privacy/compliance/supply-chain matrix. |
| `B39-TEST-M44` | `B39-S4` | P0 | `planned` | 0 | `none` | `none` | `pending` | Validate artifact/workflow template completeness. |
| `B39-TEST-M45` | `B39-S4` | P0 | `planned` | 0 | `none` | `none` | `pending` | Add skill/subagent contract eval. |
| `B39-TEST-M46` | `B39-S4` | P1 | `planned` | 0 | `none` | `none` | `pending` | Add MCP and Context7 boundary tests. |
| `B39-TEST-M47` | `B39-S4` | P1 | `planned` | 0 | `none` | `none` | `pending` | Run mass-user onboarding pilot. |
| `B39-TEST-M48` | `B39-S4` | P1 | `planned` | 0 | `none` | `none` | `pending` | Add cross-platform environment matrix. |
| `B39-TEST-M49` | `B39-S4` | P1 | `planned` | 0 | `none` | `none` | `pending` | Add source freshness/current-docs audit. |
| `B39-TEST-M50` | `B39-S4` | P1 | `planned` | 0 | `none` | `none` | `pending` | Add accessibility/usability checks for generated HTML surfaces. |
| `B39-TEST-M51` | `B39-S4` | P1 | `planned` | 0 | `none` | `none` | `pending` | Add optional LLM-as-judge calibration plan. |
| `B39-TEST-M52` | `B39-S4` | P1 | `planned` | 0 | `none` | `none` | `pending` | Add data retention/cache/stage cleanup proof. |
| `B39-TEST-M53` | `B39-S4` | P1 | `planned` | 0 | `none` | `none` | `pending` | Add incident and recovery drills. |
| `B39-TEST-M54` | `B39-S4` | P0 | `planned` | 0 | `none` | `none` | `pending` | Add release and distribution governance. |

## Batch 40 Overlay Coverage

Use this table while executing Batch 39 to prove that B40 completion-skeptic changes are covered by the existing `B39-TEST-M01..M54` matrix instead of being treated as separate release evidence.

| Overlay ID | Batch 39 rows | Required coverage | Current status | Evidence refs | Open blocker / next action |
| --- | --- | --- | --- | --- | --- |
| `B39-B40-OV01` | `B39-TEST-M02` | Manifest schema includes `completion_skeptic` packet ref, verdict, trigger level, risk classes, accepted gap refs, scorecard ref and promotion boundary. | `planned` | `pending` | Add schema fixture before pilot execution. |
| `B39-B40-OV02` | `B39-TEST-M03` | Command collector separates current command evidence from user-claimed, fake, generated-view and stale evidence. | `planned` | `pending` | Add fake-evidence rejection fixture. |
| `B39-B40-OV03` | `B39-TEST-M04`, `B39-TEST-M36` | No-unapproved-actions proof covers automation, MCP, Agents SDK runner, provider call, browser automation, target apply, canonical graph mutation and git action. | `planned` | `pending` | Extend final no-action packet. |
| `B39-B40-OV04` | `B39-TEST-M05` | Redaction covers `doubt_verification_packet`, pilot ledger, scorecard calibration, go/no-go closure and metrics-loop records. | `planned` | `pending` | Add redaction fixtures for verifier artifacts. |
| `B39-B40-OV05` | `B39-TEST-M07`, `B39-TEST-M08` | Rollup/dashboard show verdicts, blockers, accepted gaps and safe next action without making generated views proof. | `planned` | `pending` | Add generated-view-not-proof assertion. |
| `B39-B40-OV06` | `B39-TEST-M09` | Failure taxonomy includes `false_pass_blocked`, `false_rewrite_blocked`, `fake_evidence_rejected`, `missing_current_evidence`, `generated_view_not_proof` and `synthetic_only_boundary`. | `planned` | `pending` | Add taxonomy fixture. |
| `B39-B40-OV07` | `B39-TEST-M10`, `B39-TEST-M30` | Scorecard and metrics loop track B40 numerator/denominator metrics and keep synthetic-only promotion blocked. | `planned` | `pending` | Add real-vs-synthetic scorecard fixture. |
| `B39-B40-OV08` | `B39-TEST-M11..M21` | Archetype pilots include or explicitly gap completion-skeptic checks for `docs_research`, `code_check` and `expected_block`. | `planned` | `pending` | Add packet refs to pilot manifest templates. |
| `B39-B40-OV09` | `B39-TEST-M22..M24` | Runtime route keeps `completion_skeptic_recommendation` additive, read-only and approval-bounded. | `planned` | `pending` | Add route compatibility fixture. |
| `B39-B40-OV10` | `B39-TEST-M27`, `B39-TEST-M49` | Source-sensitive claims use official/source-registry evidence or become `needs_fresh_check`; community claims stay intake-only. | `planned` | `pending` | Add source freshness verifier case. |
| `B39-B40-OV11` | `B39-TEST-M31..M33` | Fixture/transcript/repeatability checks cover check-again triggers, generated-site-only proof, release claims, max revise loops and route/verdict drift. | `planned` | `pending` | Extend eval fixtures after B39 runner exists. |
| `B39-B40-OV12` | `B39-TEST-M37`, `B39-TEST-M44`, `B39-TEST-M45`, `B39-TEST-M39` | Docs/site, templates, skills and CLI matrix include `completion-skeptic`, `doubt-verification-packet.md` and `validate_doubt_verification_packet.py`. | `planned` | `pending` | Include verifier artifacts in hardening inventory. |
| `B39-B40-OV13` | `B39-TEST-M35`, `B39-TEST-M42`, `B39-TEST-M46`, `B39-TEST-M54` | Go/no-go, runtime/browser QA, MCP and release governance preserve `manual_only` / `not_promoted` until real pilots, owner review and exact approval exist. | `planned` | `pending` | Keep release decision blocked by synthetic-only evidence. |

## Attempt Log

Copy one row per attempt. Use deterministic attempt IDs: `B39-TEST-M01-A01`, `B39-TEST-M01-A02`, and so on.

| Attempt ID | Test ID | Slice | Started at | Finished at | Runner / surface | Environment | Target / fixture | Approval ref | Commands / checks | Expected result | Actual result | Status | Failure class | Evidence refs | Doubt packet ref | Completion-skeptic verdict | Accepted gap refs | Promotion boundary | Mutation proof | Redaction status | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `B39-TEST-MXX-A01` | `B39-TEST-MXX` | `B39-SX` | `pending` | `pending` | `pending` | `pending` | `pending` | `none` | `pending` | `pending` | `pending` | `planned` | `none` | `pending` | `none` | `not_run` | `none` | `manual_only_not_promoted` | `pending` | `pending` | `pending` |

## Current Product-Agent OS Formation Issues

This section records owner-observed Product-Agent OS formation problems discovered before Batch 39 execution. These rows are not production-pilot pass evidence and do not change the Batch 39 counters until a formal attempt/retest is recorded.

| Issue ID | Related test / slice | Problem summary | Root cause hypothesis | Product-Agent OS files changed | Docs/tests changed | Risk level | Evidence / source basis | Current status | Retest / next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `B39-FORM-AGENTS-001` | `B39-TEST-M45` / `B39-S4` | Initial project custom agent profiles were too narrow and used Product-Agent OS routing metadata (`ownership`, `inputs`, `outputs`, `stop_conditions`, `model_policy`, `handoff_requirements`) as ad-hoc top-level TOML fields instead of keeping the official custom-agent surface centered on `name`, `description` and `developer_instructions`. | Agent templates were copied as compact role cards, not as Codex custom-agent profiles. The `description` field described ownership rather than the trigger/use case, which could weaken agent selection and handoff clarity. | `.codex/agents/*.toml`; `plugins/product-agent-os/assets/templates/agents/*.toml`; `plugins/product-agent-os/scripts/product_agent_os/validators.py` | `tests/product_agent_os/test_infrastructure_templates.py`; `prod_test.md` | P1 | Official Codex manual cache from 2026-06-09, sections `Subagents`, `Subagent concepts`, `AGENTS.md` and `Skills`; fresh fetch on 2026-06-11 was unavailable from local shell. Focused template validation passed in this run. | `fixed_pending_retest` | Parse generated packaged custom-agent TOML files, check no legacy top-level Product-Agent OS metadata fields, verify no unexpected MCP/automation activation, and keep `B39-TEST-M45` as the formal skill/subagent contract eval gate. |
| `B39-FORM-AGENTS-002` | `B39-TEST-M22`, `B39-TEST-M23`, `B39-TEST-M44`, `B39-TEST-M45` / `B39-S3..S4` | Product-Agent OS does not yet have a first-start project formation workflow that automatically performs a full project audit, runs the relevant local audit/discovery scripts, and returns a project-specific recommendation packet for agents, skills, templates, documentation, and development methodologies. | Current agent creation can be performed manually from owner intent and packaged templates, but the system did not yet force the correct ordering: audit the project first, create or stage project-specific templates/docs second, then assemble custom agents with official fields, ownership, tools, docs, skills, methodologies, stop conditions, and approval boundaries. | `plugins/product-agent-os/assets/templates/workflows/project-formation.md`; `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/assets/templates/config/config.toml` | `tests/product_agent_os/test_infrastructure_templates.py`; `prod_test.md` | P0 | Owner observation from 2026-06-11 agent formation work; current `.codex/agents/*.toml` profiles were improved manually after audit and official Codex/custom-agent schema review. Focused project-formation template validation passed in this run. | `fixed_pending_retest` | Run formal `B39-TEST-M22/M23/M44/M45` coverage against a fresh staged install and prove project formation produces recommendation and retest artifacts before agent assembly. |
| `B39-FORM-PERMISSIONS-001` | `B39-TEST-M22`, `B39-TEST-M23`, `B39-TEST-M44`, `B39-TEST-M45` / `B39-S3..S4` | A new user installing Product-Agent OS would not automatically learn that project-scoped `.codex` artifact directories need sandbox permission-profile exceptions, and on Windows inherited ACL deny entries can still block ordinary shell writes even after config is updated. | Product-Agent OS generated `.codex/config.toml` did not include a scoped permission profile for its artifact directories, and there was no packaged Windows ACL preflight/fix script. The workaround existed only as session guidance. | `plugins/product-agent-os/assets/templates/config/config.toml`; `plugins/product-agent-os/scripts/product_agent_os/windows_codex_permissions.py`; `plugins/product-agent-os/scripts/prepare_windows_codex_permissions.py` | `tests/product_agent_os/test_windows_codex_permissions.py`; `tests/product_agent_os/test_infrastructure_templates.py`; `docs/product-agent-os/technical.en.md`; `prod_test.md` | P0 | Owner observation from 2026-06-11 permission troubleshooting; active managed profile kept `.codex` read-only while Product-Agent OS needs project artifact writes under scoped subdirectories. | `fixed_pending_retest` | Retest generated config TOML, run the Windows permissions CLI in read-only check mode, verify non-Windows `--apply` guard, and keep sensitive `.codex/config.toml`, `.codex/hooks`, `.codex/automations` and `.codex/plugins` closed by default. |
| `B39-FORM-CONTROLS-001` | `B39-TEST-M22`, `B39-TEST-M23`, `B39-TEST-M44`, `B39-TEST-M45` / `B39-S3..S4` | Product-Agent OS still needs to update how it forms `agents`, `config` and `rules` from working examples. The current baseline can repeatedly request many permissions or block execution because generated project assets are not aligned with the proven global control examples. | The initial formation flow treated agent profiles, permission profiles and command rules as separate template outputs instead of one coordinated Codex control surface. The new formation workflow records safe pattern harvesting without copying private/user-specific content or weakening approvals. | `plugins/product-agent-os/assets/templates/workflows/project-formation.md`; `plugins/product-agent-os/assets/templates/config/config.toml`; `plugins/product-agent-os/assets/templates/agents/*.toml`; `plugins/product-agent-os/scripts/product_agent_os/validators.py` | `tests/product_agent_os/test_infrastructure_templates.py`; `prod_test.md` | P0 | Owner observation from 2026-06-11 after permission troubleshooting: the original setup repeatedly prompted for approvals and blocked execution until scoped config/rules/ACL behavior was corrected manually. Focused control-surface template validation passed in this run. | `fixed_pending_retest` | Retest with a fresh install/first-start scenario; verify project formation produces project-safe `agents`, `.codex/config.toml` and `.rules` guidance/templates while keeping destructive/external actions approval-bound. |
| `B39-FORM-HTML-001` | `B39-TEST-M28`, `B39-TEST-M44`, `B39-TEST-M50` / `B39-S3..S4` | HTML artifact delivery semantics are wrong when final user-facing files are left or treated as if they belong in a third staging location instead of the user's project folder. If the user explicitly names a project path, generated HTML must be saved there; if the user does not name a path, Product-Agent OS must choose a project-scoped destination rather than an unrelated external location. | Staged-first safety policy was being over-applied to final deliverables. The new export contract distinguishes intermediate stage from final project-scoped or explicit user-requested destination. | `plugins/product-agent-os/scripts/product_agent_os/offline_artifact_export.py`; `plugins/product-agent-os/scripts/product_agent_os/project_graph_renderer.py`; `plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics_report.py` | `tests/product_agent_os/test_offline_artifact_export.py`; `tests/product_agent_os/test_project_graph_renderer.py`; `tests/product_agent_os/test_agent_skill_metrics_report.py`; `prod_test.md` | P0 | Owner observation from 2026-06-11 HTML artifact generation. Current artifact refs: `docs/superpowers/specs/product-agent-os-project-cockpit.html`; `docs/superpowers/specs/product-agent-os-agent-skill-evaluation-report.html`. Focused export/renderer tests passed in this run. | `fixed_pending_retest` | Run formal `B39-TEST-M28/M44/M50` coverage and prove final HTML export lands in the project or explicit requested path, while external stage remains intermediate only. |
| `B39-FORM-HTML-002` | `B39-TEST-M44`, `B39-TEST-M50` / `B39-S4` | Generated HTML artifact design is unacceptable and differs sharply from the accepted template/source-of-truth design direction. The generated `project-cockpit` and `agent-skill-evaluation-report` surfaces need a design-system pass, not only structural HTML validation. | Current renderer validation focused on offline safety, eight-page structure, escaped JSON and no external assets. The agent-skill metrics report now has a dashboard/cockpit-aligned visual baseline, but formal visual/usability review evidence is still pending. | `plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics_report.py`; `plugins/product-agent-os/scripts/product_agent_os/offline_artifact_export.py` | `tests/product_agent_os/test_agent_skill_metrics_report.py`; `tests/product_agent_os/test_offline_artifact_export.py`; `prod_test.md` | P0 | Owner observation from 2026-06-11. Current artifact refs: `docs/superpowers/specs/product-agent-os-project-cockpit.html`; `docs/superpowers/specs/product-agent-os-agent-skill-evaluation-report.html`. Template/source refs: `plugins/product-agent-os/assets/templates/project-graph/project-cockpit.html`; `plugins/product-agent-os/assets/templates/project-graph/project-graph.css`; `plugins/product-agent-os/assets/templates/status-dashboard/status.html`; `plugins/product-agent-os/assets/templates/status-dashboard/status.css`; `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md`. Focused report design checks passed in this run. | `fixed_pending_retest` | Add formal visual/usability review evidence before treating generated HTML surfaces as product-quality artifacts; project-cockpit visual baseline still needs explicit conformance review. |

### Agent Formation Workflow Candidate

This candidate records the expected future Product-Agent OS behavior for first use on a real project. It is not implementation evidence yet.

| Step | Required behavior | Expected artifact / owner | Verification gate |
| --- | --- | --- | --- |
| 1. Project audit | Run a full read-only project audit before creating agents. The audit should inspect active instructions, control-plane files, source/docs structure, stack/runtime signals, existing tests/evals, security/privacy/release surfaces, current dirty state, available Product-Agent OS templates, and approval/sandbox boundaries. | Recommendation packet owned by `explorer` and `architect`; likely staged as a project formation report under an approved `.codex/` evidence path. | Audit scripts run with current evidence; no mutation, no provider calls, no browser automation, no git action, no external writes. |
| 2. Recommendation list | Return project-specific recommendations for agents, skills, artifact templates, documentation, methodology domains, verification gates, approval boundaries, and missing owner questions. | Human-readable recommendation file plus optional machine-readable packet. | Every recommendation links to source evidence, template source, owner, risk, next action, and `present_unverified` / `proposal_staged` / `explicit_gap_accepted` status. |
| 3. Project templates and docs | Create or stage only the templates and documentation skeletons that match the project risk profile, such as requirements, acceptance scenarios, traceability, architecture, ADR, quality/eval, model policy, approval record, API/security/release/frontend docs where applicable. | `docs-maintainer`, `product-manager`, `architect`, `tester`, `reviewer`, and `release-operator` own their domains. | Template completeness test, source-policy check, UTF-8/hygiene check, no secrets/raw private data, and explicit docs owner map. |
| 4. Agent assembly | Build `.codex/agents/*.toml` after the audit and docs/template stage. Agents must use official custom-agent fields, then put ownership, inputs, outputs, tools, docs, skills, methodologies, stop conditions, model policy, sandbox/MCP boundaries, and handoff requirements inside `developer_instructions`. | `.codex/agents/*.toml` owned by agent-team design workflow; role owners remain domain-specific. | TOML parse, schema/field check, template-reference check, no unexpected MCP/automation activation, and skill/subagent contract eval. |
| 5. Handoff and retest | Produce a fresh-context handoff for the next role and record retest requirements in `prod_test.md`. | `agent-task-packet.md`, `task-matrix-plan.md`, `doubt-verification-packet.md` where needed. | Current command evidence before any `ready`, `done`, `works`, `release-ready`, or `safe to hand off` claim. |

## Defect And Product-Agent OS Change Ledger

Add one row before changing Product-Agent OS because of a failed or blocked-unexpected attempt. If the change only updates docs/tests, still record it so the retest chain remains visible.

| Change ID | Caused by attempt | Failure summary | Root cause hypothesis | Product-Agent OS files changed | Docs/tests changed | Risk level | Verification run | Retest required | Status | Rollback note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `B39-FIX-001` | `pending` | `pending` | `pending` | `pending` | `pending` | `pending` | `pending` | `yes` | `planned` | `pending` |
| `B39-FIX-AGENTS-001` | `B39-FORM-AGENTS-001`; `B39-FORM-AGENTS-002` | Project custom-agent profile formation was not aligned with the official Codex custom-agent schema and trigger-description guidance, and packaged templates could reproduce the old schema on fresh install. | Top-level role metadata fields belonged in `developer_instructions` or a team-design artifact, while `description` needed to say when to use the agent. | `.codex/agents/explorer.toml`; `.codex/agents/product-manager.toml`; `.codex/agents/architect.toml`; `.codex/agents/builder.toml`; `.codex/agents/tester.toml`; `.codex/agents/reviewer.toml`; `.codex/agents/docs-maintainer.toml`; `.codex/agents/release-operator.toml`; `plugins/product-agent-os/assets/templates/agents/*.toml`; `plugins/product-agent-os/scripts/product_agent_os/validators.py`; `plugins/product-agent-os/assets/templates/workflows/project-formation.md`; `plugins/product-agent-os/scripts/product_agent_os/templates.py` | `tests/product_agent_os/test_infrastructure_templates.py`; `prod_test.md` | P1 | TOML parse required/optional fields OK; focused packaged agent/template tests OK; project formation workflow registration OK; earlier docs checks remain historical until rerun. | `yes` | `fixed_pending_retest` | Delete or restore `.codex/agents/*.toml` and packaged agent template changes if custom agent loading or subagent routing regresses. |
| `B39-FIX-PERMISSIONS-001` | `B39-FORM-PERMISSIONS-001` | Product-Agent OS permission setup was not productized for new users. | Default generated config lacked scoped Product-Agent OS `.codex` write exceptions, and Windows ACL cleanup was manual chat guidance rather than a packaged read-only check plus explicit apply script. | `plugins/product-agent-os/assets/templates/config/config.toml`; `plugins/product-agent-os/scripts/product_agent_os/windows_codex_permissions.py`; `plugins/product-agent-os/scripts/prepare_windows_codex_permissions.py` | `tests/product_agent_os/test_windows_codex_permissions.py`; `tests/product_agent_os/test_infrastructure_templates.py`; `docs/product-agent-os/technical.en.md`; `prod_test.md` | P0 | `test_windows_codex_permissions` OK; full `test_infrastructure_templates` 86 OK; `test_render_infrastructure_cli` 6 OK; Product-Agent OS docs unittest 78 OK; `python tools\check_docs.py` OK; `git diff --check` OK with pre-existing CRLF warnings; read-only permissions CLI returned current inherited deny SID evidence. | `yes` | `fixed_pending_retest` | Remove the new permission profile block from the config template and delete the Windows permissions script/tests/docs row if the scoped path list proves too broad. |
| `B39-FIX-CONTROLS-001` | `B39-FORM-CONTROLS-001` | Product-Agent OS control-surface generation was not yet aligned with the manually proven `agents`, `config` and `rules` examples. | The first-start formation flow did not synthesize a coherent permission/approval/command-rule package, so a fresh user could see excessive approval prompts or blocked execution. | `plugins/product-agent-os/assets/templates/workflows/project-formation.md`; `plugins/product-agent-os/assets/templates/config/config.toml`; `plugins/product-agent-os/assets/templates/agents/*.toml`; `plugins/product-agent-os/scripts/product_agent_os/validators.py`; `plugins/product-agent-os/scripts/product_agent_os/templates.py` | `tests/product_agent_os/test_infrastructure_templates.py`; `prod_test.md` | P0 | Focused infrastructure template tests OK: agent templates validate, legacy top-level metadata blocked, project formation workflow registered, required targets registered, config TOML valid. Fresh-install retest not yet performed. | `yes` | `fixed_pending_retest` | Remove the project-formation workflow registration and packaged agent template changes if fresh-start formation proves too broad or weakens approval boundaries. |
| `B39-FIX-HTML-001` | `B39-FORM-HTML-001`; `B39-FORM-HTML-002` | HTML artifact output policy and visual quality gaps needed implementation, not just ledger classification. | The generation flow had structural/safety checks, but lacked a final project-scoped export contract and agent-skill report visual baseline checks. | `plugins/product-agent-os/scripts/product_agent_os/offline_artifact_export.py`; `plugins/product-agent-os/scripts/product_agent_os/project_graph_renderer.py`; `plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics_report.py` | `tests/product_agent_os/test_offline_artifact_export.py`; `tests/product_agent_os/test_agent_skill_metrics_report.py`; `tests/product_agent_os/test_project_graph_renderer.py`; `prod_test.md` | P0 | Focused export/report/renderer tests OK. Formal visual/usability review and Batch 39 attempt rows are still pending. | `yes` | `fixed_pending_retest` | Remove the export contract module and renderer/report contract fields if final HTML export semantics conflict with owner-approved deployment flow. |

## Retest Chain

Use this table to prove that fixes were actually retested against the failed gate, not only inspected.

| Original attempt | Change ID | Retest attempt(s) | Pass criteria | Retest status | Remaining risk | Owner decision |
| --- | --- | --- | --- | --- | --- | --- |
| `pending` | `pending` | `pending` | `pending` | `pending` | `pending` | `pending` |

## Per-Slice Closeout

| Slice | Required before closeout | Current status | Evidence refs | Open risks |
| --- | --- | --- | --- | --- |
| `B39-S1` | Manifest, command collector, mutation proof, redaction, session visibility, rollup, dashboard, taxonomy, scorecard, B40 overlay fields and at least one synthetic evidence package. | `not_started` | `pending` | `pending` |
| `B39-S2` | Archetype pilot coverage or owner-accepted gaps, including one clean positive, one expected-block negative pilot and completion-skeptic coverage for `docs_research`, `code_check` and `expected_block`. | `not_started` | `pending` | `pending` |
| `B39-S3` | Functional regression, repeatability, eval, performance, completion-skeptic route/packet/scorecard regressions and full verification evidence after Batch 39 changes. | `not_started` | `pending` | `pending` |
| `B39-S4` | Production/mass-user hardening gates pass or carry owner-reviewed blockers/accepted gaps, while B40 promotions stay blocked without exact approval. | `not_started` | `pending` | `pending` |
| `B39-S5` | Source-owned closure, go/no-go packet, completion-skeptic `manual_only` / `not_promoted` review and final no-unapproved-actions proof. | `not_started` | `pending` | `pending` |

## No-Unapproved-Actions Ledger

| Boundary | Default | Exceptions / approval refs | Current evidence |
| --- | --- | --- | --- |
| Target workspace mutation | Forbidden without exact approval. | `none` | `pending` |
| Live server launch | Forbidden without exact approval. | `none` | `pending` |
| Browser automation | Forbidden without exact approval. | `none` | `pending` |
| Provider/API/model call | Forbidden without exact approval. | `none` | `pending` |
| MCP server activation | Forbidden without exact approval. | `none` | `pending` |
| Agents SDK runner activation | Forbidden without exact approval. | `none` | `pending` |
| Canonical graph mutation | Forbidden without exact approval. | `none` | `pending` |
| Hook or automation activation | Forbidden without exact approval. | `none` | `pending` |
| Completion-skeptic promotion beyond manual-only | Forbidden without real pilots, owner review and exact approval. | `none` | `pending` |
| External write or publication | Forbidden without exact approval. | `none` | `pending` |
| Git stage/commit/push/PR | Forbidden without exact approval. | `none` | `pending` |

## Open Blockers

| Blocker ID | Test ID | Severity | Summary | Owner | Next action | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `B39-BLOCKER-001` | `pending` | `pending` | `pending` | `pending` | `pending` | `planned` |

## Accepted Gaps

Accepted gaps require owner review. Do not use this table to bypass failed verification.

| Gap ID | Test ID | Gap | Residual risk | Why accepted | Owner / date | Revisit trigger |
| --- | --- | --- | --- | --- | --- | --- |
| `B39-GAP-001` | `pending` | `pending` | `pending` | `pending` | `pending` | `pending` |

## Final Decision Summary

| Field | Value |
| --- | --- |
| Clean positive pilot recorded | `no` |
| Expected-block negative pilot recorded | `no` |
| Representative archetype coverage | `no` |
| Functional regression/repeatability evidence | `no` |
| Production/mass-user hardening evidence | `no` |
| Product-Agent OS fixes retested | `no` |
| No-unapproved-actions proof | `no` |
| Completion-skeptic real pilot evidence | `no` |
| Completion-skeptic scorecard calibrated beyond synthetic-local | `no` |
| Completion-skeptic promotion status | `manual_only_not_promoted` |
| Completion-skeptic accepted gaps visible | `no` |
| Open P0/P1 blockers | `pending` |
| Recommended `B38-PROD-M12` decision | `not_ready_not_executed` |
