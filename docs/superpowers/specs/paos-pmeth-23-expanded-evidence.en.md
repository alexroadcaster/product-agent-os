# PMETH-23 — B3 and B4 end-to-end profile qualification

Source status: bounded synthetic profile qualification, implemented_locally_verified, release_hold.

## Qualification after the recipe recovery fix {#create-recovery-closure}

2026-11-19. The verified sources include base Git commit
`4f2d3400b29e014fb9887dcaca681cd8a525818d` and the working-tree fix with
adapter revision `05fbd1d086c8411c1ad689bbdf02671e17db3da706a5691c467f30080846d5a9`.
Codex CLI `0.170.0` kept its pinned binary hash. Candidate and standard
native admission passed.

A completed creation can supply a declared read input to a later step of
the same recipe. Admission requires a completed producer attempt and a
successful native observation with matching content hash and file revision.
The service checks both again at approval and before native dispatch.
Same-byte replacement is rejected. An ordinary create still rejects an
existing destination. A legacy attempt without a recorded file revision
cannot supply that proof.

- `create` and `modify` passed **68/68** each with Chromium, the native
  broker and a synthetic worker. The create fixture used exclusive `wx`.
  After restart and a lost response to Resume, the original request replayed
  its decision. The first child ran once. The successor read its artifact
  and moved the task to review.
- **56/56** focused tests passed, including same-byte substitution before
  admission, after command proposal and just before native dispatch.
  Ordinary create collisions, Stop and unknown-outcome fencing also passed.
- The current recommendation browser passed **53/53**. FSD, the F13
  apply-to-evidence-and-rollback chain, Web typecheck and build passed.
  Full Windows Web passed **733/733** with no skips. Focused Python for
  CLI and G9 passed **109/109**.

The verified synthetic scope covers all seven declared profiles and AC01–AC04.
PMETH-23 is locally closed. Live skill invocation, actual-agent usefulness,
human acceptance and migration of a user workspace remain separate evidence
for evaluation and rollout. The release disposition remains `hold`.
[B2 decision](paos-pmeth-b2-evidence.en.md#rollout-decision) ·
[Results and hashes](paos-pmeth-23-expanded-evidence.md#create-recovery-closure)

## Initial qualification before the fix {#initial-qualification}

2026-11-19. Tested Git source `4f2d3400b29e014fb9887dcaca681cd8a525818d`,
Node.js `26.5.0`, Chromium `148.0.7778.96`, and Codex CLI `0.170.0`.
The standard loader admitted adapter revision
`fb6db331a76a9acac5d5244400741483524a91fd53ae57aebd3bc8cb080b839b`
and binary SHA-256 `8d06dc231dba649c7d48d3eecab239c452a1ac498c41dd6492a6f301b90a22ce`.
The run used disposable projects, services and browser profiles on loopback.
The Browser plugin was unavailable, so the existing Playwright harness used
installed Chromium. A synthetic worker drove the production broker without
provider calls.
[Task and dependency graph](../../planning/user-project-methodologies-2026-11-15.en.md#task-paos-pmeth-23)

### Profiles and acceptance criteria {#profiles}

The required tasks and their transitive prerequisites are implemented.
The results below apply to the observed scenarios.

| Profile | Plan prerequisite | Result |
| --- | --- | --- |
| `read_only_bug_docs` | PMETH-26 | Current CLI and HTTP/Web agreed for equivalent Python bug and documentation inputs. Chromium exercised the recommendation on a saved task. |
| `design` | PMETH-09 after 08 | Verified RU/EN, light/dark, keyboard navigation, loading, missing analysis, denial, stale response, desktop, and 400 px. A deliberately wrong region order failed the composition check. |
| `fsd_migration` | PMETH-12 after 10 → 11, PMETH-16 for apply | F14 selected one page. A reviewed fixture edit switched it to the public API. Both builds preserved behavior and the legacy entry. F14 retained a modular area. Rollback restored original bytes and the compiled result. |
| `skill_tool_routing` | PMETH-14 after 13 | Offline applicability, packaged discovery, manual routing, stale handoff and limits passed. Live session and skill invocation remain open. |
| `target_write_apply` | PMETH-16 after 06 and 15 | G9 passed three synthetic profiles plus approval, drift and rollback checks. F13 exercised CLI planning, HTTP preview, saved proposal, digest-bound apply and rollback on one document. The wrong digest and missing CSRF were rejected. The BOM, authored `AGENTS.md`, and outside canary retained their bytes. |
| `criterion_readiness` | PMETH-17 after 06 and 15 | A real broker command checked the applied F13 document. AC-1 received a native `passed` receipt. AC-2 stayed `missing` after an `accepted_gap` decision. A foreign project was rejected. An AC change made the evidence `stale`. |
| `durable_override_recovery` | PMETH-21 after 16, 18 and 20, PMETH-18 after 17 and 19 | Decision and receipt survived service restart. The AC edit made the decision stale and retained its history. The browser `modify` recipe recovered from a lost response with two distinct child runs. The `create` recipe was blocked before the successor run. |

- **AC01** covers base parity, the F13 apply and native check chain, persisted
  override, and AC drift in the observed scope. The findings limit expansion.
- **AC02** covers Design, one incremental FSD pilot, retention of modular
  boundaries, and approved writes. The FSD edit was manual and hash-bound on a
  disposable page. G9 and F13 exercised their dedicated routes. Backend/CLI
  required no FSD gate. AI quality remains an evidence gap.
- **AC03** covers privacy, CSRF, foreign scope, false readiness, user bytes,
  version identity and cleanup. The `create` finding blocks that recovery branch.
- **AC04** observed F14, Python runner, the HTTP API, F13 `document_apply`
  and `native_command_broker`. Binary, lockfile and adapter drift were rejected
  before spawn. Live use, model value and human acceptance remain separate.

### Findings and disposition {#findings}

1. **The `create` recovery branch is blocked.** After creating `proof.txt`
   and restarting, the first child result survived without replay. The review
   child inherited the task-wide `create` preflight, which saw the existing
   file and returned `FILE_PREFLIGHT_BLOCKED`. The recipe entered
   `recovery_required` and the successor remained `planned`. The recipe and
   App-agent preflight owners need to qualify the transition from a verified
   creation to a subsequent read while preserving collision and no-replay guards.
2. **Skill invocation and actual-agent usefulness remain open.** The evidence
   supports offline routing. Live exposure and invocation require their own
   observation.
3. **Human acceptance remains open.** Browser checks cover rendered behavior,
   geometry and keyboard operation. Recommendation comprehension, real-project
   use and a user-workspace FSD migration need their own scope and evidence.

Expanded qualification is `partially_verified`. The PMETH-25 owner decision
remains `hold`. [B2 decision](paos-pmeth-b2-evidence.en.md#rollout-decision)

### Evidence {#receipts}

Full Web 729/729 with no skips, focused Python 109/109, and Web typecheck and
build passed. Recommendation browser 53/53. Standard native admission passed
in all three modes and Stop. Recovery `modify` passed 68/68. Recovery `create`
passed 46/47 and exited 1. [Commands](../../../TEST.md#pmeth-23-expanded)

[Russian evidence matrix](paos-pmeth-23-expanded-evidence.md#receipts) lists
the exact local receipts and SHA-256 hashes of results and harnesses.
