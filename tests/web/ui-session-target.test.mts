import { test } from "node:test";
import assert from "node:assert/strict";
import {
  isExecutionTarget,
  attachTaskToSession,
  loadSavedSessionTarget,
} from "../../apps/web/src/api/session-target.ts";
import type { StoredEntity } from "../../apps/web/src/api/client.ts";
const task: StoredEntity = {
  id: "t",
  projectId: "p",
  kind: "task",
  revision: 3,
  status: "ready",
  data: {
    schemaVersion: "m1_task_profile_v1",
    acceptanceCriteria: ["Proof"],
    files: [{ relativePath: "src/app.ts", plannedOperation: "modify" }],
    sessionIds: ["s"],
  },
};
test("execution requires saved criteria and a bounded relative file allowlist", () => {
  assert.equal(isExecutionTarget(task), true);
  assert.equal(isExecutionTarget(undefined), false);
  assert.equal(
    isExecutionTarget({
      ...task,
      data: { ...task.data, acceptanceCriteria: [] },
    }),
    false,
  );
  assert.equal(
    isExecutionTarget({ ...task, data: { ...task.data, files: [] } }),
    false,
  );
  assert.equal(
    isExecutionTarget({
      ...task,
      data: {
        ...task.data,
        files: [{ relativePath: "../secret", plannedOperation: "read" }],
      },
    }),
    false,
  );
  assert.equal(isExecutionTarget({ ...task, status: "done" }), false);
});
test("new Execution dispatch requires ready and no recovery review marker", () => {
  for (const status of [
    "backlog",
    "in_progress",
    "review",
    "verification",
    "awaiting_acceptance",
    "done",
    "cancelled",
  ])
    assert.equal(isExecutionTarget({ ...task, status }), false, status);
  assert.equal(
    isExecutionTarget({
      ...task,
      data: { ...task.data, risks: ["recovery_review"] },
    }),
    false,
  );
});
test("saved targets outside the first list page are loaded directly and active context stays readable", async () => {
  const calls: string[] = [];
  const current = { ...task, id: "target-51", status: "in_progress" };
  const found = await loadSavedSessionTarget(
    {
      entity: async (projectId, id) => {
        calls.push(`${projectId}/${id}`);
        return current;
      },
    },
    "p",
    "target-51",
  );
  assert.equal(found?.id, "target-51");
  assert.equal(found?.status, "in_progress");
  assert.equal(isExecutionTarget(found), false);
  assert.deepEqual(calls, ["p/target-51"]);
  for (const invalid of [
    { ...current, projectId: "foreign" },
    { ...current, kind: "session" as const },
    { ...current, id: "wrong" },
  ])
    await assert.rejects(
      loadSavedSessionTarget({ entity: async () => invalid }, "p", "target-51"),
      /TASK_SCOPE/,
    );
});
test("task/session relation is a single revision-bound command and preserves prior history links", () => {
  const session: StoredEntity = {
    id: "s",
    projectId: "p",
    kind: "session",
    revision: 2,
    data: { mode: "planning" },
  };
  const changes = attachTaskToSession(session, task);
  assert.deepEqual(
    changes.map((value) => value.expectedRevision),
    [2, 3],
  );
  assert.equal(changes[0].entity.data?.taskId, "t");
  assert.deepEqual(changes[1].entity.data?.sessionIds, ["s"]);
  assert.equal(session.data?.taskId, undefined);
  assert.throws(
    () => attachTaskToSession(session, { ...task, projectId: "foreign" }),
    /scope/,
  );
});
