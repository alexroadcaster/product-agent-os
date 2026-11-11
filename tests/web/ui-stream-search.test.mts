import { test } from "node:test";
import assert from "node:assert/strict";
import { createLatestRequest } from "../../apps/web/src/api/latest-request.ts";
import { visibleAssistantDrafts } from "../../apps/web/src/api/visible-drafts.ts";
test("old query/project results cannot publish after cancellation or disposal", async () => {
  const latest = createLatestRequest(),
    seen: string[] = [];
  let resolveOld!: (value: string) => void, oldSignal: AbortSignal | undefined;
  const old = latest.run(
    (signal) => {
      oldSignal = signal;
      return new Promise<string>((resolve) => (resolveOld = resolve));
    },
    (value) => seen.push(value),
    assert.fail,
  );
  await latest.run(
    async () => "new",
    (value) => seen.push(value),
    assert.fail,
  );
  resolveOld("old");
  await old;
  assert.deepEqual(seen, ["new"]);
  assert.equal(oldSignal?.aborted, true);
  let resolveLate!: (value: string) => void;
  const late = latest.run(
    () => new Promise<string>((resolve) => (resolveLate = resolve)),
    (value) => seen.push(value),
    assert.fail,
  );
  latest.dispose();
  resolveLate("late");
  await late;
  assert.deepEqual(seen, ["new"]);
});
test("stream UI shows final_answer only and suppresses an exact persisted run/item pair", () => {
  const state: any = {
    canSend: false,
    reason: null,
    visibleDrafts: [
      {
        runId: "r",
        sourceItemId: "i",
        role: "assistant",
        text: "safe partial",
        revision: 1,
        status: "streaming",
        phase: "final_answer",
      },
      {
        runId: "r",
        sourceItemId: "hidden",
        role: "assistant",
        text: "hidden",
        revision: 1,
        status: "streaming",
        phase: "unknown",
      },
    ],
  };
  assert.equal(visibleAssistantDrafts(state, []).length, 1);
  assert.equal(
    visibleAssistantDrafts(state, [
      {
        id: "m",
        projectId: "p",
        kind: "message",
        revision: 1,
        data: { runId: "r", sourceItemId: "other" },
      },
    ]).length,
    1,
  );
  assert.equal(
    visibleAssistantDrafts(state, [
      {
        id: "m",
        projectId: "p",
        kind: "message",
        revision: 1,
        data: { runId: "r", sourceItemId: "i" },
      },
    ]).length,
    0,
  );
});
