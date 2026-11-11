import { test } from "node:test";
import assert from "node:assert/strict";
import { startSessionPolling } from "../../apps/web/src/api/session-poll.ts";
import { mergeJournalMessages } from "../../apps/web/src/api/message-history.ts";
test("newest bounded polling includes late results past 1000 and journal order ignores random IDs", async () => {
  const all = Array.from({ length: 2001 }, (_, index) => ({
    id: `random-${2001 - index}`,
    projectId: "p",
    kind: "message" as const,
    revision: 1,
    journalOrder: index + 1,
    body: index === 2000 ? "newest final" : String(index + 1),
  })).reverse();
  let update: any;
  const dispose = startSessionPolling({
    state: async () => ({ canSend: false, reason: null }),
    messages: async (offset) => ({
      items: all.slice(offset, offset + 50),
      hasMore: offset + 50 < all.length,
    }),
    publish: (value) => {
      update = value;
    },
    error: assert.fail,
    schedule: () => 0,
    cancel: () => {},
  });
  for (let i = 0; i < 60; i++) await Promise.resolve();
  assert.equal(update.messages.length, 1000);
  assert.equal(update.messages[0].journalOrder, 1002);
  assert.equal(update.messages.at(-1).body, "newest final");
  assert.equal(update.historyOffset, 1000);
  assert.equal(update.hasMore, true);
  const older = all.slice(update.historyOffset, update.historyOffset + 50);
  const visible = mergeJournalMessages(older, update.messages);
  assert.equal(visible.length, 1050);
  assert.equal(visible[0].journalOrder, 952);
  assert.equal(visible.at(-1)?.journalOrder, 2001);
  dispose();
});
const settle = async () => {
  for (let i = 0; i < 15; i++) await Promise.resolve();
};
test("older page replacement keeps the latest tail bounded and missing journal order remains unknown", () => {
  const row = (order: number) => ({
    id: `id-${order}`,
    projectId: "p",
    kind: "message" as const,
    revision: 1,
    journalOrder: order,
  });
  const tail = Array.from({ length: 1000 }, (_, i) => row(i + 1001)),
    page1 = Array.from({ length: 50 }, (_, i) => row(i + 951)),
    page2 = Array.from({ length: 50 }, (_, i) => row(i + 901));
  assert.equal(mergeJournalMessages(page1, tail).length, 1050);
  const next = mergeJournalMessages(page2, tail);
  assert.equal(next.length, 1050);
  assert.equal(next[0].journalOrder, 901);
  assert.equal(next.at(-1)?.journalOrder, 2000);
  assert.equal(
    next.some((item) => item.journalOrder === 1000),
    false,
  );
  const duplicate = mergeJournalMessages(
    [row(2000)],
    [{ ...row(2000), revision: 2, body: "latest" }],
  );
  assert.equal(duplicate.length, 1);
  assert.equal(duplicate[0].body, "latest");
  const unknown = mergeJournalMessages([
    { id: "z", projectId: "p", kind: "message", revision: 1 },
    { id: "a", projectId: "p", kind: "message", revision: 1 },
  ]);
  assert.deepEqual(
    unknown.map((item) => item.id),
    ["a", "z"],
  );
  assert.ok(unknown.every((item) => item.journalOrder === undefined));
});
test("poll publishes late approvals/final messages without duplicates and stops after disposal", async () => {
  const timers: (() => void)[] = [],
    updates: unknown[] = [];
  let round = 0,
    signal: AbortSignal | undefined;
  const dispose = startSessionPolling({
    state: async (current) => {
      signal = current;
      return {
        canSend: false,
        reason: null,
        pendingApprovals: round ? [{ requestId: "a" }] : [],
      };
    },
    messages: async () => ({
      items: [
        {
          id: "m",
          projectId: "p",
          kind: "message",
          revision: ++round,
          body: round > 1 ? "final" : "user",
        },
        {
          id: "m",
          projectId: "p",
          kind: "message",
          revision: round,
          body: round > 1 ? "final" : "user",
        },
      ],
      hasMore: false,
    }),
    publish: (update) => updates.push(update),
    error: assert.fail,
    schedule: (callback, delay) => {
      assert.ok(delay <= 1000);
      timers.push(callback);
      return callback;
    },
    cancel: (timer) => {
      const index = timers.indexOf(timer as () => void);
      if (index >= 0) timers.splice(index, 1);
    },
  });
  await settle();
  assert.equal(updates.length, 1);
  assert.equal((updates[0] as any).messages.length, 1);
  assert.equal(timers.length, 1);
  timers.shift()!();
  await settle();
  assert.equal((updates[1] as any).messages[0].body, "final");
  assert.equal((updates[1] as any).state.pendingApprovals.length, 1);
  dispose();
  assert.equal(signal?.aborted, true);
  assert.equal(timers.length, 0);
});
test("disposing aborts an in-flight poll and prevents late publication", async () => {
  let finish!: (value: any) => void,
    signal: AbortSignal | undefined,
    published = 0;
  const dispose = startSessionPolling({
    state: (current) => {
      signal = current;
      return new Promise((resolve) => {
        finish = resolve;
      });
    },
    messages: async () => ({ items: [], hasMore: false }),
    publish: () => published++,
    error: assert.fail,
  });
  dispose();
  finish({ canSend: true, reason: null });
  await settle();
  assert.equal(signal?.aborted, true);
  assert.equal(published, 0);
});
test("a slow state request never overlaps cycles and message paging stops at its explicit bound", async () => {
  let finish!: (value: any) => void,
    pageCalls = 0;
  const timers: (() => void)[] = [],
    updates: any[] = [];
  const dispose = startSessionPolling({
    state: () =>
      new Promise((resolve) => {
        finish = resolve;
      }),
    messages: async (offset) => {
      pageCalls++;
      return {
        items: [
          { id: String(offset), projectId: "p", kind: "message", revision: 1 },
        ],
        hasMore: true,
      };
    },
    publish: (update) => updates.push(update),
    error: assert.fail,
    schedule: (callback) => {
      timers.push(callback);
      return callback;
    },
    cancel: () => {
      timers.length = 0;
    },
  });
  for (let i = 0; i < 60; i++) await Promise.resolve();
  assert.equal(timers.length, 0);
  assert.equal(pageCalls, 20);
  finish({ canSend: false, reason: null });
  await settle();
  assert.equal(updates[0].messages.length, 20);
  assert.equal(updates[0].hasMore, true);
  assert.equal(timers.length, 1);
  dispose();
});
