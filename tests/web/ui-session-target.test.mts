import { test } from "node:test";
import assert from "node:assert/strict";
import {
  isExecutionTarget,
  attachTaskToSession,
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
