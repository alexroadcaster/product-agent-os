import type { ImportSource, ImportPreview } from "./client.ts";
export const canCommitImport = (preview: ImportPreview) =>
  preview.mode === "legacy_import" && preview.blocked.length === 0;
type SourceFile = { name: string; size: number; text(): Promise<string> };
export async function prepareImportSources(
  records: SourceFile,
  recordsPath: string,
  projection?: SourceFile | null,
  projectionPath?: string,
): Promise<ImportSource[]> {
  const safe = (path: string) =>
    path.trim() &&
    !/^(?:[A-Za-z]:|[/\\])/.test(path) &&
    !/[\0\r\n:]/.test(path) &&
    !path.split(/[/\\]/).some((part) => !part || part === "." || part === "..");
  const inputs = [
    { file: records, path: recordsPath, role: "records" as const },
    ...(projection
      ? [
          {
            file: projection,
            path: projectionPath ?? projection.name,
            role: "projection" as const,
          },
        ]
      : []),
  ];
  if (
    (projection && !/\.json$/i.test(records.name)) ||
    (projection && !/\.md$/i.test(projection.name))
  )
    throw new Error("BUNDLE_REQUIRES_JSON_RECORDS_AND_MD_PROJECTION");
  if (
    inputs.some((input) => input.file.size > 1024 * 1024 || !safe(input.path))
  )
    throw new Error("INVALID_PROJECT_RELATIVE_SOURCE");
  if (
    new Set(
      inputs.map((input) => input.path.replaceAll("\\", "/").toLowerCase()),
    ).size !== inputs.length
  )
    throw new Error("DUPLICATE_SOURCE_PATH");
  return Promise.all(
    inputs.map(async (input) => ({
      role: input.role,
      sourceName: input.file.name,
      sourceRelativePath: input.path,
      content: await input.file.text(),
    })),
  );
}
