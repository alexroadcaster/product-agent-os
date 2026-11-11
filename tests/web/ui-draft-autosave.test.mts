import { test } from "node:test";
import assert from "node:assert/strict";
import { createDraftAutosave } from "../../apps/web/src/api/draft-autosave.ts";
const settle = async () => {
  for (let i = 0; i < 25; i++) await Promise.resolve();
};

test("explicit Save retries a failed initial read and saves local text against a verified empty baseline", async () => {
  let reads = 0;
  let stored = { id: "d", body: "", revision: 2 };
  let writes = 0;
  const draft = createDraftAutosave({
    read: async () => {
      if (++reads === 1) throw new Error("offline");
      return stored;
    },
    write: async (record, body) => {
      writes++;
      assert.equal(record.revision, 2);
      return (stored = { ...record, body, revision: 3 });
    },
    restore() {},
    error() {},
  });
  await settle();
  draft.edit("local text");
  assert.equal(await draft.flush(), true);
  assert.equal(reads, 2);
  assert.equal(writes, 1);
  assert.equal(stored.body, "local text");
  draft.dispose();
});

test("initial-read recovery cannot blindly overwrite a different existing server draft", async () => {
  let reads = 0;
  let writes = 0;
  const draft = createDraftAutosave({
    read: async () => {
      if (++reads === 1) throw new Error("offline");
      return { id: "d", body: "server text", revision: 9 };
    },
    write: async () => {
      writes++;
      throw new Error("must not overwrite");
    },
    restore() {},
    error() {},
  });
  await settle();
  draft.edit("local text");
  assert.equal(await draft.flush(), false);
  assert.equal(await draft.flush(), false);
  assert.equal(writes, 0);
  draft.dispose();
});
test("autosave debounces edits, flushes on session disposal and restores on reopen", async () => {
  let stored = { id: "draft", body: "saved", revision: 1 };
  const timers: (() => void)[] = [],
    restored: string[] = [],
    errors: unknown[] = [];
  const options = {
    read: async () => stored,
    write: async (record: typeof stored, body: string) => {
      assert.equal(record.revision, stored.revision);
      stored = { ...record, body, revision: record.revision + 1 };
      return stored;
    },
    restore: (body: string) => restored.push(body),
    error: (error: unknown) => errors.push(error),
    schedule: (callback: () => void, delay: number) => {
      assert.equal(delay, 500);
      timers.push(callback);
      return callback;
    },
    cancel: (timer: unknown) => {
      const index = timers.indexOf(timer as () => void);
      if (index >= 0) timers.splice(index, 1);
    },
  };
  const draft = createDraftAutosave(options);
  await settle();
  assert.deepEqual(restored, ["saved"]);
  draft.edit("one");
  draft.edit("latest");
  assert.equal(timers.length, 1);
  draft.dispose();
  await settle();
  assert.equal(stored.body, "latest");
  const reopened = createDraftAutosave(options);
  await settle();
  assert.equal(restored.at(-1), "latest");
  reopened.dispose();
  assert.deepEqual(errors, []);
});
test("lost ACK retries the same intent and serializes newer text; conflicts never silently overwrite", async () => {
  let stored = { id: "d", body: "base", revision: 1 },
    first = true;
  const keys: string[] = [],
    errors: unknown[] = [];
  const receipts = new Map<string, typeof stored>();
  const draft = createDraftAutosave({
    read: async () => stored,
    write: async (record, body, key) => {
      keys.push(key);
      if (receipts.has(key)) return receipts.get(key)!;
      if (record.revision !== stored.revision)
        throw new Error("REVISION_CONFLICT");
      stored = { ...record, body, revision: record.revision + 1 };
      receipts.set(key, stored);
      if (first) {
        first = false;
        throw new Error("lost ACK");
      }
      return stored;
    },
    restore: () => {},
    error: (error) => errors.push(error),
  });
  await settle();
  await draft.flush("first");
  assert.equal(errors.length, 1);
  draft.edit("newer");
  await draft.flush();
  assert.equal(keys[0], keys[1]);
  assert.equal(stored.body, "newer");
  stored = { ...stored, body: "concurrent", revision: stored.revision + 1 };
  await draft.flush("preserved local");
  assert.equal(stored.body, "concurrent");
  assert.equal(errors.length, 2);
  draft.dispose();
});
