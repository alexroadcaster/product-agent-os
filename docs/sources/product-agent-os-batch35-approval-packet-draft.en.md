# Product-Agent OS Batch 35 approval packet draft

Source status: `internal`

## Scope

This is the staged Batch 35 approval packet draft for `T10-LIVE-M37..M41`. It is not an approval and not execution evidence. Batch 35 remains planned/not implemented until the owner selects exactly one action and approves that action with target, data policy, allowed commands, rollback, audit destination and stop conditions.

## Current Handoff State

Batch 34 is current through `B34-DOC-M15` when the following evidence is present:

- Batch 34 docs packet and source registry/backlog/control-plane sync;
- focused Batch 34 docs contract tests;
- `python tools\check_docs.py`;
- regular strict MkDocs build into `site/`;
- `git diff --check`;
- packaging/install smoke packet;
- this Batch 35 approval packet draft.

The handoff does not start a live server, run browser automation, call providers/live external model/API endpoints, mutate the canonical graph or perform git stage/commit/push/PR.

## Common Approval Fields

Every Batch 35 action must define:

- owner and reviewer;
- exact action id;
- target workspace or artifact scope;
- data classification and redaction policy;
- allowed commands and explicitly forbidden commands;
- credential boundary, with secret values stored outside the packet;
- cache and budget policy when providers are involved;
- expected evidence files;
- audit event destination;
- rollback or clean shutdown proof;
- stop conditions;
- accepted gaps with owner, reason, review date, residual risk and follow-up condition.

Do not include secrets, tokens, private keys, raw private chat logs, private customer data, unredacted PII, raw source bodies or absolute private paths in approval packets, logs, screenshots, prompts, fixtures or generated evidence.

## Action Matrix

| Action | Required approval contents | Evidence after approved execution | Hard boundary until approval |
| --- | --- | --- | --- |
| `approved_local_runtime_launch` | approved target, local bind/auth/port policy, no-write endpoint policy, PID/log path, health check, clean shutdown plan, graph-only fallback | `live-server-run-evidence.json` | No local live server launch. |
| `actual_browser_automation_smoke` | approved runtime URL, browser tool, viewports, allowed network, screenshot path, console/network capture, mobile overflow checks, generated-view/source-boundary labels | `browser-automation-smoke.json` and screenshots | No browser automation. |
| `approved_provider_api_pilot` | provider, model, credential env var name, redaction, cache, budget, eval threshold, audit path, fallback behavior | `provider-call-evidence.json`, `provider-eval-report.json`, cache metadata | No provider/live external model/API calls. |
| `approved_canonical_mutation_pilot` | accepted ledger item, dry-run plan, conflict checks, journal path, previous/new digest comparison, rollback plan | `canonical-mutation-run.json`, `graph-mutation-journal.jsonl`, `rollback-proof.json` | No canonical graph mutation. |
| `explicit_git_release_pr_action` | exact files, unrelated-change check, verification summary, commit message, push target, PR intent and release boundary | `git-release-pr-evidence.md` and PR packet | No git stage/commit/push/PR. |

## Owner Decision Template

```yaml
batch35_action_id: ""
owner: ""
reviewer: ""
target_scope: ""
data_policy: ""
allowed_commands: []
forbidden_commands:
  - "live server launch without approved_local_runtime_launch"
  - "browser automation without actual_browser_automation_smoke approval"
  - "provider/API call without approved_provider_api_pilot approval"
  - "canonical graph mutation without approved_canonical_mutation_pilot approval"
  - "git stage/commit/push/PR without explicit_git_release_pr_action approval"
credential_policy:
  env_vars_only: true
  secret_values_in_packet: false
rollback_or_shutdown: ""
audit_destination: ""
stop_conditions: []
accepted_gaps: []
approval_status: "approval_required"
```

## Verification Before Execution

Before any selected action runs, verify:

- Batch 24 governance evidence is current;
- Batch 25 runtime contract evidence is current;
- Batch 31 audit/observability evidence is current;
- Batch 32 target consent evidence is current;
- Batch 33 QA/performance/stabilization evidence is current;
- Batch 34 packaging/docs closure evidence is current;
- approval packet names one action only.

## Residual Risks

- A draft approval packet can be mistaken for approval. Keep `approval_status: approval_required` until the owner explicitly approves one action.
- Reusing approval across action ids can silently expand scope.
- Screenshots, provider output and generated graph artifacts are not source of truth without source-boundary evidence and owner review.
- Git release/PR action is separate from docs closure and remains explicit-only.

## Next Action

Owner chooses one Batch 35 action to approve or leaves Batch 35 blocked. No Task 27/28 planning should start from this packet.
