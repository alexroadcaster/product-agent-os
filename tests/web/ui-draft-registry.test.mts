import { test } from "node:test";
import assert from "node:assert/strict";
import {
  createDraftRegistry,
  sendWithDraftAck,
  isSendAccepted,
} from "../../apps/web/src/api/draft-registry.ts";
const settle = async () => {
  for (let i = 0; i < 30; i++) await Promise.resolve();
};
test("reopen before dispose flush ACK shares the latest text and the single writer", async () => {
  let stored = { id: "d", body: "base", revision: 1 },
    reads = 0,
    finish!: (value: typeof stored) => void;
  const registry = createDraftRegistry();
  const storage = {
    read: async () => {
      reads++;
      return stored;
    },
    write: async (record: typeof stored, body: string) =>
      new Promise<typeof stored>((resolve) => {
        finish = () => {
          stored = { ...record, body, revision: record.revision + 1 };
          resolve(stored);
        };
      }),
  };
  const first = registry.acquire(["p", "s"], storage);
  await settle();
  first.edit("latest");
  first.release();
  await settle();
  const reopened = registry.acquire(["p", "s"], storage);
  assert.equal(reopened.snapshot().body, "latest");
  assert.equal(reads, 1);
  finish(stored);
  await settle();
  assert.equal(reopened.snapshot().body, "latest");
  assert.equal(stored.body, "latest");
  reopened.release();
  await settle();
  assert.equal(registry.size, 0);
});
test('App durable queued ACK clears the draft but unknown native dispatch does not',async()=>{
 assert.equal(isSendAccepted({state:'queued',route:'codex_app_agent'}),true);
 assert.equal(isSendAccepted({state:'dispatching'}),false);
 assert.equal(isSendAccepted({state:'queued'}),false);
 let stored={id:'d',body:'queued input',revision:1};const registry=createDraftRegistry();
 const lease=registry.acquire(['p','app-session'],{read:async()=>stored,write:async(record,body)=>stored={...record,body,revision:record.revision+1}});
 await settle();await sendWithDraftAck(lease,'queued input',async()=>({id:'app-job',state:'queued',route:'codex_app_agent'}));
 await settle();assert.equal(stored.body,'');lease.release();
});
test("late Send ACK clears durably after release and before a failing state refresh", async () => {
  let stored = { id: "d", body: "sent", revision: 1 },
    ack!: (value: { state: string }) => void;
  const registry = createDraftRegistry(),
    storage = {
      read: async () => stored,
      write: async (record: typeof stored, body: string) =>
        (stored = { ...record, body, revision: record.revision + 1 }),
    };
  const lease = registry.acquire(["p", "s"], storage);
  await settle();
  let oldCallbacks = 0;
  lease.subscribe(() => oldCallbacks++);
  const sending = sendWithDraftAck(
    lease,
    "sent",
    () => new Promise<{ state: string }>((resolve) => (ack = resolve)),
  );
  const refreshed = sending.then(() => {
    assert.equal(stored.body, "");
    throw new Error("state refresh unavailable");
  });
  lease.release();
  const count = oldCallbacks;
  ack({ state: "running" });
  await assert.rejects(refreshed, /state refresh unavailable/);
  await settle();
  assert.equal(stored.body, "");
  assert.equal(oldCallbacks, count);
  assert.equal(registry.size, 0);
});
test("accepted Send with lost cleanup ACK reopens as cleared and retries its existing write intent", async () => {
  let stored = { id: "d", body: "sent", revision: 1 },
    fail = true;
  const keys: string[] = [],
    receipts = new Map<string, typeof stored>();
  const storage = {
    read: async () => stored,
    write: async (record: typeof stored, body: string, key: string) => {
      keys.push(key);
      if (receipts.has(key)) return receipts.get(key)!;
      stored = { ...record, body, revision: record.revision + 1 };
      receipts.set(key, stored);
      if (fail) {
        fail = false;
        throw new Error("cleanup ACK lost");
      }
      return stored;
    },
  };
  const registry = createDraftRegistry(),
    lease = registry.acquire(["p", "s"], storage);
  await settle();
  const result = await sendWithDraftAck(lease, "sent", async () => ({
    state: "running",
  }));
  assert.equal(result.acknowledged, true);
  assert.equal(result.cleanupSaved, false);
  lease.release();
  await settle();
  const reopened = registry.acquire(["p", "s"], storage);
  assert.equal(reopened.snapshot().body, "");
  assert.equal(await reopened.flush(), true);
  assert.equal(keys[0], keys[1]);
  reopened.release();
  await settle();
  assert.equal(registry.size, 0);
});
test("ACK does not clear newer edits even when text returns to the same value; failed sends retain text", async () => {
  let stored = { id: "d", body: "sent", revision: 1 },
    ack!: (value: { state: string }) => void;
  const registry = createDraftRegistry(),
    lease = registry.acquire(["p", "s"], {
      read: async () => stored,
      write: async (record, body) =>
        (stored = { ...record, body, revision: record.revision + 1 }),
    });
  await settle();
  const sending = sendWithDraftAck(
    lease,
    "sent",
    () => new Promise<{ state: string }>((resolve) => (ack = resolve)),
  );
  lease.edit("newer");
  lease.edit("sent");
  ack({ state: "running" });
  await sending;
  await lease.flush();
  assert.equal(lease.snapshot().body, "sent");
  assert.equal(stored.body, "sent");
  await assert.rejects(
    sendWithDraftAck(lease, "sent", async () => {
      throw new Error("unknown send");
    }),
  );
  assert.equal(lease.snapshot().body, "sent");
  lease.release();
  await settle();
});
test("registry bounds unresolved scopes and releases clean scopes without stale subscriptions", async () => {
  const registry = createDraftRegistry(1);
  let writes = 0;
  const storage = {
    read: async () => ({ id: "d", body: "", revision: 0 }),
    write: async () => {
      writes++;
      throw new Error("offline");
    },
  };
  const lease = registry.acquire(["p", "s"], storage);
  await settle();
  lease.edit("retained");
  await lease.flush();
  lease.release();
  assert.throws(
    () => registry.acquire(["p", "other"], storage),
    /DRAFT_SCOPE_CAPACITY/,
  );
  assert.equal(registry.size, 1);
  assert.equal(writes, 1);
});
test("resolved uncertain/failed Send responses retain draft without replay or replacement IDs", async () => {
  let stored = { id: "d", body: "text", revision: 1 },
    writes = 0,
    calls = 0;
  const registry = createDraftRegistry(),
    lease = registry.acquire(["p", "s"], {
      read: async () => stored,
      write: async (record, body) => {
        writes++;
        return (stored = { ...record, body, revision: record.revision + 1 });
      },
    });
  await settle();
  for (const state of [
    "failed",
    "dispatching",
    "recovery_required",
    "future_unknown",
  ]) {
    const result = await sendWithDraftAck(lease, "text", async () => {
      calls++;
      return { state };
    });
    assert.equal(result.acknowledged, false);
    assert.equal(lease.snapshot().body, "text");
  }
  assert.equal(writes, 0);
  assert.equal(calls, 4);
  assert.equal(isSendAccepted({ state: "completed" }), true);
  assert.equal(isSendAccepted({}), false);
  lease.release();
  await settle();
  assert.equal(registry.size, 0);
});
test("lost draft ACK intent survives release/reopen with its key and no extra read", async () => {
  let stored = { id: "d", body: "base", revision: 1 },
    first = true,
    reads = 0;
  const receipts = new Map<string, typeof stored>(),
    keys: string[] = [];
  const storage = {
    read: async () => {
      reads++;
      return stored;
    },
    write: async (record: typeof stored, body: string, key: string) => {
      keys.push(key);
      if (receipts.has(key)) return receipts.get(key)!;
      assert.equal(record.revision, stored.revision);
      stored = { ...record, body, revision: record.revision + 1 };
      receipts.set(key, stored);
      if (first) {
        first = false;
        throw new Error("lost ACK");
      }
      return stored;
    },
  };
  const registry = createDraftRegistry(),
    one = registry.acquire(["p", "s"], storage);
  await settle();
  one.edit("pending");
  assert.equal(await one.flush(), false);
  one.release();
  await settle();
  const reopened = registry.acquire(["p", "s"], storage);
  assert.equal(reopened.snapshot().body, "pending");
  reopened.edit("newer");
  assert.equal(await reopened.flush(), true);
  assert.equal(keys[0], keys[1]);
  assert.equal(reads, 1);
  assert.equal(stored.body, "newer");
  reopened.release();
  await settle();
  assert.equal(registry.size, 0);
});
