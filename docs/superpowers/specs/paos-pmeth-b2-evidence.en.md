# Plan B2 task recommendation and rollout disposition

Source status: local implementation evidence, synthetic browser qualification, approved synthetic actual-agent pilot and owner decision.

## Route and UI {#route-and-ui}

| Task | Outcome |
| --- | --- |
| PMETH-19 | `POST /api/v1/projects/{projectId}/analysis/task-advice` uses the existing session, origin and CSRF checks. The service binds the saved task to its revision, current inventory, analysis stage and adapter revision. |
| PMETH-20 | **Tasks → Summary → Task recommendation** shows the next check, method applicability and depth, sources, reasons and limitations. Project facts remain in **Overview → Sources**. |
| PMETH-26 | The canonical guide shows both synthetic cases in CLI and Web. [User and operator instructions](../../product-agent-os/methodology-intelligence.en.md#task-advice) |

The temporary projection lives outside the target. Its limits are 200 files, 64 KiB per file and 2 MiB of total content. Required sources pass through the existing inventory policy. Other permitted paths may appear as metadata. Sensitive and prohibited content stays out of the projection. Isolated Python receives bounded stdin and uses the same methodology code as the CLI. A named Python unittest must be declared in `TEST.md`. The advice path performs no project commands or writes.

The host checks project, task and revision bindings and validates digests for files actually read. Cancellation stops the Python child. Missing evidence produces a partial or unavailable result with a reason. A subsequent schema or code-database scan preserves the last applicable analysis stage when the source revision still matches. An observed analysis failure is explicit. The existing scan record gains an optional stage observation. The recommendation remains transient.

## PMETH-23 synthetic qualification {#synthetic-qualification}

- CLI and Web matched decisions, reasons, requirements and next checks for equivalent inputs. The task adapter uses the declared behavioral criterion as its observed invariant. The next checks were `python -B -m unittest test_counter.CounterTest.test_increment_by_one` and comparison of `guide.md` with `counter.py`.
- `tests/web/project-task-advice.test.mts` covered the body limit, session, origin, CSRF, cross-project tasks, stale source and Python failure. It rejected unknown versions, mismatched projects, tasks and revisions, and proved cleanup on cancellation and unchanged project state.
- Chromium and the existing Playwright installation passed 35 checks against the real API and built frontend. Russian and English were both exercised in light and dark themes, plus a 400 px layout check and keyboard navigation. Loading, absent analysis, partial coverage, permission failure, wrong scope and stale evidence were observed. The target hashes matched, the disposable profile was removed, and there were no external requests. Receipt `pmeth-b2-x1GxOd/result.json`, SHA-256 `96ae96b323a6ea1f28f69be81efd3124b57a68268ad6033606e21c507122b60e`, contains build, source and harness identities.
- Chromium exited during the initial sandboxed launch. Native execution used the same binary, Chromium sandbox enabled and a disposable profile. The harness distinguishes expected session-before-pairing and permission response errors.
- HTTP and contract changes required native requalification. The candidate and default native gates passed for adapter revision `7a41dce01fdff0220427f66bed70d986361ca8559c6511298774d3ce48c7c448` using a hash-matched cached binary. Candidate SHA-256 `0e3a4f63375048bd069441695a18bf8b53a0e988bdebd05141a41f448a87a1d5`, default `32d031ecb7671e67ec6812dc8748ff353b272dcd5ef42d99cc67a1bbf5c52472`. The earlier packaging tests reported `ADAPTER_NOT_QUALIFIED` before the pin refresh.
- Final native `node --test --test-concurrency=1 tests/web/*.test.mts` passed 718/718 with no skips. Focused HTTP, Python bridge and pin tests passed 17/17. Two B1 Python suites passed 40/40. Type checking and the production build passed.
- The initial sandboxed Web run was stopped after native SQLite checks failed. The partial log is `.tmp/pmeth-b2-web.log`. The completed native run supplies the full verification result.
- Qualification covers read-only Python defect and docs tasks. Human comprehension remains an evidence gap for PMETH-20. Design-DD, FSD, native/AI advice, apply, override and recovery require their own profile checks before any rollout expansion.

## PMETH-24 usefulness pilot {#usefulness-pilot}

The owner authorized four isolated Codex runs using synthetic files. All inherited the same model and reasoning. Paired file hashes, order, first-step oracle, one-check budget and 120-second cap were recorded before dispatch. A benefit signal required retention of the correct choice and either one fewer unnecessary step or at least 20% comparable time reduction.

| Case | Baseline | With advice | Observation |
| --- | --- | --- | --- |
| Backend defect | Named unittest, intended `5 != 4`. Upper bound 36 s. | Same test and outcome. Upper bound 24 s. | One read invocation before the choice and one check per arm. |
| Documentation | Compared `guide.md` with `counter.py`. Upper bound 30 s. | Same comparison. Upper bound 43 s. | Both found the guide omitted the increment by two. |

All four selected the expected first step. No extra steps, reversals, owner interventions or byte changes were observed. The upper bounds include variable dispatch overhead and cannot establish comparative speed. Exact latency, tokens and cost are unavailable. Implementation acceptance, defects/reopens and repair effort were outside the read-only experiment. Usefulness is `insufficient_evidence` for both cases. Protocol SHA-256 `61a09239c428f74058893c3d95c1880e5da6741ae7080b1c12e50efabb5f48d3`, results `956511674c9451bf8ef70ad3952b31d44bf10bb61e04ff10aa39d74b81e82d23`, retained under `.tmp/pmeth-b2-pilot/`.

## PMETH-25 owner disposition {#rollout-decision}

On 2026-11-19 the owner approved a **release `hold`** for local adapter revision `7a41dce01fdff0220427f66bed70d986361ca8559c6511298774d3ce48c7c448`. Technical qualification covers read-only Python defect and documentation advice in the local build. Broader usefulness, human comprehension and expanded profiles require separate evidence.

To disable or roll back, remove the scoped UI and endpoint together and restore a matching qualified pin. Older scan records remain readable and the additional observation is compatible with existing storage. Preserve authored target files and evidence. Requalify the exact sources, lock and executable tuple before another release review. Installation, publication, active hooks and new target permissions require their own decisions.

| Gap | Owner and reevaluation condition |
| --- | --- |
| Usefulness, model cost and comprehension | Product owner agrees on comparable sampling, aligned timing, cost measurements and a comprehension check. |
| Privacy, licensing and distribution | Product and release owners review data minimization, rights and the release channels. |
| Activation in another environment and profile expansion | Release owner qualifies the exact host tuple. Profile owner repeats PMETH-23 for that scope and revision. |
