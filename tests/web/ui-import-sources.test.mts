import { test } from "node:test";
import assert from "node:assert/strict";
import {
  prepareImportSources,
  canCommitImport,
} from "../../apps/web/src/api/import-sources.ts";
test("normalized proposals and unknown preview modes never enable cutover", () => {
  const preview: any = { blocked: [], mode: "normalized_proposal" };
  assert.equal(canCommitImport(preview), false);
  assert.equal(canCommitImport({ ...preview, mode: undefined }), false);
  assert.equal(canCommitImport({ ...preview, mode: "legacy_import" }), true);
  assert.equal(
    canCommitImport({ ...preview, mode: "legacy_import", blocked: [{}] }),
    false,
  );
});
const file = (name: string) => ({
  name,
  size: 10,
  text: async () => `synthetic ${name}`,
});
test("bundle pins separate JSON records and MD projection with explicit project-relative paths", async () => {
  const sources = await prepareImportSources(
    file("tasks.json"),
    "research/tasks.json",
    file("plan.md"),
    "research/plan.md",
  );
  assert.deepEqual(
    sources.map(({ role, sourceRelativePath }) => ({
      role,
      sourceRelativePath,
    })),
    [
      { role: "records", sourceRelativePath: "research/tasks.json" },
      { role: "projection", sourceRelativePath: "research/plan.md" },
    ],
  );
});
test("unsafe/duplicate paths and inverted source roles are rejected before requests", async () => {
  await assert.rejects(
    prepareImportSources(file("tasks.json"), "../outside"),
    /RELATIVE/,
  );
  await assert.rejects(
    prepareImportSources(file("tasks.json"), "C:\\outside"),
    /RELATIVE/,
  );
  await assert.rejects(
    prepareImportSources(file("tasks.json"), "same", file("plan.md"), "SAME"),
    /DUPLICATE/,
  );
  await assert.rejects(
    prepareImportSources(
      file("plan.md"),
      "plan.md",
      file("tasks.json"),
      "tasks.json",
    ),
    /REQUIRES/,
  );
});
