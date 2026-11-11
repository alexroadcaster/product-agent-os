import { test } from "node:test";
import assert from "node:assert/strict";
import { plannedFiles, newTask } from "../../apps/web/src/api/task.ts";
test("editing task text preserves recorded rename and actual file operations", () => {
  const recorded = {
    relativePath: "src/new.ts",
    previousRelativePath: "src/old.ts",
    plannedOperation: "rename",
    actualOperation: "rename",
  };
  assert.deepEqual(plannedFiles("src/new.ts\nsrc/add.ts", [recorded]), [
    recorded,
    {
      relativePath: "src/add.ts",
      plannedOperation: "create_or_modify_after_discovery",
      actualOperation: null,
    },
  ]);
});
test("new task leaves operational evidence and actual duration unknown", () => {
  const task = newTask(
    "p",
    "A task",
    "Brief",
    ["Proof"],
    "00000000-0000-4000-8000-000000000001",
  );
  assert.equal(task.status, "backlog");
  assert.equal(task.revision, 0);
  assert.deepEqual(task.data?.actual, {
    startedAt: null,
    endedAt: null,
    durationSeconds: null,
  });
  assert.deepEqual(task.data?.acceptanceCriteria, ["Proof"]);
  assert.deepEqual(task.data?.sessionIds, []);
});
