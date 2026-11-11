import { test } from "node:test";
import assert from "node:assert/strict";
import { createDraftAutosave } from "../../apps/web/src/api/draft-autosave.ts";
const settle = async () => {
  for (let i = 0; i < 25; i++) await Promise.resolve();
};
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
