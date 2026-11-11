import { test } from "node:test";
import assert from "node:assert/strict";
import {
  canSend,
  canAccept,
  eventReferencesEntity,
} from "../../apps/web/src/api/policy.ts";
import {
  runBlocksScopeChange,
  canStopRun,
} from "../../apps/web/src/api/policy.ts";
import { canAnswerApproval } from "../../apps/web/src/api/policy.ts";
test("approval acceptance requires current reviewed details, identity and unexpired pending request", () => {
  const state = {
      canSend: false,
      reason: null,
      bindingId: "b",
      runId: "r",
      generation: "g",
    },
    request = {
      requestId: 0,
      bindingId: "b",
      runId: "r",
      generation: "g",
      reviewable: true,
      kind: "command",
      details: { command: "synthetic command" },
      state: "pending",
      expiresAt: 200,
    };
  assert.equal(canAnswerApproval(state, request, "accept", 100), true);
  assert.equal(
    canAnswerApproval(state, { ...request, reviewable: false }, "accept", 100),
    false,
  );
  assert.equal(
    canAnswerApproval(state, { ...request, reviewable: false }, "decline", 100),
    true,
  );
  assert.equal(
    canAnswerApproval(state, { ...request, generation: "old" }, "accept", 100),
    false,
  );
  assert.equal(canAnswerApproval(state, request, "accept", 200), false);
  assert.equal(
    canAnswerApproval(
      state,
      { ...request, state: "response_sent" },
      "accept",
      100,
    ),
    false,
  );
});
test("historical terminal runs permit mode/target changes while active and unknown runs remain fenced", () => {
  for (const state of ["completed", "failed", "interrupted"]) {
    const snapshot = {
      canSend: true,
      reason: null,
      bindingId: "b",
      runId: "historical",
      state,
    };
    assert.equal(runBlocksScopeChange(snapshot), false);
    assert.equal(canStopRun(snapshot), false);
  }
  for (const state of [
    "dispatching",
    "running",
    "awaiting_approval",
    "interrupt_requested",
    "recovery_required",
    "future_unknown",
  ])
    assert.equal(
      runBlocksScopeChange({
        canSend: false,
        reason: null,
        bindingId: "b",
        runId: "r",
        state,
      }),
      true,
    );
  assert.equal(runBlocksScopeChange(null), true);
  assert.equal(
    runBlocksScopeChange({
      canSend: false,
      reason: "binding_required",
      state: "connected",
    }),
    false,
  );
  assert.equal(
    canStopRun({
      canSend: false,
      reason: null,
      bindingId: "b",
      runId: "r",
      state: "running",
    }),
    true,
  );
  assert.equal(
    canStopRun({
      canSend: false,
      reason: null,
      bindingId: "b",
      runId: "r",
      state: "recovery_required",
    }),
    false,
  );
});
test('App queue Stop stays available before claim and while cancellation awaits worker ACK',()=>{
  for(const state of ['queued','claimed','cancel_requested']) {
    const snapshot={canSend:false,reason:null,bindingId:'b',runId:'r',state};
    assert.equal(runBlocksScopeChange(snapshot),true);
    assert.equal(canStopRun(snapshot),true);
  }
});
test("history correlation uses exact entity identifiers rather than matching source text", () => {
  assert.equal(
    eventReferencesEntity(
      { changes: [{ entity: { id: "task-a" } }] },
      "task-a",
    ),
    true,
  );
  assert.equal(
    eventReferencesEntity(
      { entity: { parentId: "task-a", data: { category: "manual_check" } } },
      "task-a",
    ),
    true,
  );
  assert.equal(
    eventReferencesEntity({ body: "task-a", id: "task-ab" }, "task-a"),
    false,
  );
  assert.equal(eventReferencesEntity(null, "task-a"), false);
});
test("send requires explicitly verified idle connection and a nonempty draft", () => {
  assert.equal(canSend(null, "idle", "hello"), false);
  assert.equal(canSend({ verified: false }, "idle", "hello"), false);
  assert.equal(canSend({ verified: true }, "uncertain", "hello"), false);
  assert.equal(canSend({ verified: true }, "running", "hello"), false);
  assert.equal(canSend({ verified: true }, "idle", "  "), false);
  assert.equal(canSend({ verified: true }, "idle", "hello"), true);
});
test("acceptance is separate from checks and disallows uncertain or active runs", () => {
  assert.equal(
    canAccept("awaiting_acceptance", "idle", ["works"], [true]),
    true,
  );
  assert.equal(canAccept("verification", "idle", ["works"], [true]), false);
  assert.equal(
    canAccept("awaiting_acceptance", "uncertain", ["works"], [true]),
    false,
  );
  assert.equal(
    canAccept("awaiting_acceptance", "running", ["works"], [true]),
    false,
  );
  assert.equal(
    canAccept("awaiting_acceptance", "idle", ["works"], [false]),
    false,
  );
  assert.equal(canAccept("awaiting_acceptance", "idle", [], []), false);
});
