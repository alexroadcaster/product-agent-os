import { constants } from "node:fs";
import { lstat, open, opendir, realpath } from "node:fs/promises";
import { join, relative, resolve, sep } from "node:path";
export type CatalogItem = {
  id: string;
  label: string;
  description: string;
  coverage: "complete" | "partial" | "unavailable";
};
const maxEntries = 128;
const maxBytes = 16_384;
/** Fixed project paths only. Linked ancestors and files are excluded; prompts are never returned. */
export async function scanReadOnlyCatalogs(workspaceRoot: string): Promise<{
  agents: CatalogItem[];
  skills: CatalogItem[];
  graph: { status: "unavailable"; reason: string };
  coverage: "complete" | "partial";
}> {
  const root = await realpath(workspaceRoot);
  let partial = false;
  async function safe(parts: string[], directory: boolean) {
    let path = root;
    for (const part of parts) {
      path = join(path, part);
      const stat = await lstat(path);
      if (stat.isSymbolicLink()) throw new Error("linked_source");
    }
    const canonical = await realpath(path);
    const within = relative(root, canonical);
    if (
      within === ".." ||
      within.startsWith(`..${sep}`) ||
      resolve(root, within) !== canonical
    )
      throw new Error("source_escape");
    const stat = await lstat(path);
    if (!directory && stat.nlink > 1) throw new Error("linked_source");
    if (directory ? !stat.isDirectory() : !stat.isFile())
      throw new Error("unsupported_source");
    return { path, stat };
  }
  async function entries(parts: string[]) {
    try {
      const { path } = await safe(parts, true);
      const names: string[] = [];
      for await (const entry of await opendir(path)) {
        if (names.length >= maxEntries) {
          partial = true;
          break;
        }
        names.push(entry.name);
      }
      return names.sort();
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "ENOENT") partial = true;
      return [];
    }
  }
  async function metadata(
    parts: string[],
    id: string,
    format: "toml" | "markdown",
  ): Promise<CatalogItem | null> {
    try {
      const { path, stat } = await safe(parts, false);
      const file = await open(
        path,
        constants.O_RDONLY | (constants.O_NOFOLLOW ?? 0),
      );
      try {
        const current = await file.stat();
        if (
          current.ino !== stat.ino ||
          current.dev !== stat.dev ||
          current.nlink > 1 ||
          !current.isFile()
        ) {
          partial = true;
          return null;
        }
        const bytes = Buffer.alloc(Math.min(current.size, maxBytes));
        const result = await file.read(bytes, 0, bytes.length, 0);
        const text = bytes.subarray(0, result.bytesRead).toString("utf8");
        if (current.size > maxBytes) partial = true;
        const header =
          format === "markdown"
            ? (/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(text)?.[1] ?? "")
            : text.split(/^(?:developer_instructions\s*=|\[)/m)[0];
        function field(name: string) {
          const line =
            new RegExp(
              `^${name}\\s*${format === "toml" ? "=" : ":"}\\s*(.*?)\\s*$`,
              "m",
            ).exec(header)?.[1] ?? "";
          if (line.startsWith('"""') || line.startsWith("'''")) return "";
          return line.replace(/^(["'])(.*)\1$/, "$2").slice(0, 512);
        }
        return {
          id,
          label: field("name") || id,
          description: field("description"),
          coverage: current.size > maxBytes ? "partial" : "complete",
        };
      } finally {
        await file.close();
      }
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "ENOENT") partial = true;
      return null;
    }
  }
  const agents: CatalogItem[] = [],
    skills: CatalogItem[] = [];
  for (const name of await entries([".codex", "agents"])) {
    if (!/^[\w-]+\.toml$/.test(name)) continue;
    const item = await metadata(
      [".codex", "agents", name],
      name.slice(0, -5),
      "toml",
    );
    if (item) agents.push(item);
  }
  for (const prefix of [".agents", ".codex"])
    for (const name of await entries([prefix, "skills"])) {
      if (!/^[\w.-]+$/.test(name) || name === "." || name === "..") continue;
      const item = await metadata(
        [prefix, "skills", name, "SKILL.md"],
        `${prefix}/skills/${name}`,
        "markdown",
      );
      if (item) skills.push(item);
    }
  return {
    agents,
    skills,
    graph: { status: "unavailable", reason: "owning_source_unverified" },
    coverage: partial ? "partial" : "complete",
  };
}
