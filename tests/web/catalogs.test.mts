import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile, rm, symlink, link } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { scanReadOnlyCatalogs } from "../../apps/local-service/src/http/catalogs.mts";
test("catalog exposes bounded role/skill metadata and excludes instructions and unrelated files", async () => {
  const root = await mkdtemp(join(tmpdir(), "paos-catalog-"));
  try {
    await mkdir(join(root, ".codex", "agents"), { recursive: true });
    await mkdir(join(root, ".agents", "skills", "review"), { recursive: true });
    await writeFile(
      join(root, ".codex", "agents", "reviewer.toml"),
      'name = "Reviewer"\ndescription = "Review changes"\ndeveloper_instructions = "PRIVATE SYNTHETIC PROMPT"',
    );
    await writeFile(
      join(root, ".codex", "agents", "hidden.toml"),
      'name = "Hidden"\ndeveloper_instructions = """\ndescription = "PRIVATE SYNTHETIC PROMPT"\n"""',
    );
    await writeFile(
      join(root, ".agents", "skills", "review", "SKILL.md"),
      "---\nname: Review skill\ndescription: Inspect a diff\n---\nPRIVATE SYNTHETIC BODY",
    );
    await writeFile(join(root, ".codex", "agents", "ignored.txt"), "ignore");
    const result = await scanReadOnlyCatalogs(root);
    assert.equal(
      result.agents.find((item) => item.id === "reviewer")?.description,
      "Review changes",
    );
    assert.equal(result.skills[0].description, "Inspect a diff");
    assert.equal(JSON.stringify(result).includes("PRIVATE"), false);
    assert.equal(result.agents.length, 2);
    assert.equal(result.graph.status, "unavailable");
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});
test("catalog rejects linked directory ancestors outside the workspace", async (t) => {
  const base = await mkdtemp(join(tmpdir(), "paos-catalog-link-"));
  const root = join(base, "workspace"),
    outside = join(base, "outside");
  try {
    await mkdir(join(root, ".codex"), { recursive: true });
    await mkdir(outside);
    await writeFile(join(outside, "escape.toml"), 'name = "Escape"');
    try {
      await symlink(outside, join(root, ".codex", "agents"), "junction");
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === "EPERM") {
        t.skip("Current Windows sandbox forbids creating junction fixtures");
        return;
      }
      throw error;
    }
    assert.deepEqual((await scanReadOnlyCatalogs(root)).agents, []);
  } finally {
    await rm(base, { recursive: true, force: true });
  }
});
test("large sources are marked partial and metadata reads stay bounded", async () => {
  const root = await mkdtemp(join(tmpdir(), "paos-catalog-large-"));
  try {
    await mkdir(join(root, ".codex", "agents"), { recursive: true });
    await writeFile(
      join(root, ".codex", "agents", "large.toml"),
      'description = "Brief"\ndeveloper_instructions = "' +
        "x".repeat(32768) +
        '"',
    );
    const result = await scanReadOnlyCatalogs(root);
    assert.equal(result.agents[0].coverage, "partial");
    assert.equal(result.agents[0].description, "Brief");
    assert.ok(JSON.stringify(result).length < 1024);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});
test("catalog excludes hardlinked files instead of disclosing outside metadata", async (t) => {
  const base = await mkdtemp(join(tmpdir(), "paos-catalog-hardlink-")),
    root = join(base, "workspace"),
    outside = join(base, "outside.toml");
  try {
    await mkdir(join(root, ".codex", "agents"), { recursive: true });
    await writeFile(
      outside,
      'name = "Outside synthetic"\ndescription = "Not project metadata"',
    );
    try {
      await link(outside, join(root, ".codex", "agents", "borrowed.toml"));
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === "EPERM") {
        t.skip("Current Windows sandbox forbids creating hardlink fixtures");
        return;
      }
      throw error;
    }
    const result = await scanReadOnlyCatalogs(root);
    assert.deepEqual(result.agents, []);
    assert.equal(result.coverage, "partial");
  } finally {
    await rm(base, { recursive: true, force: true });
  }
});
