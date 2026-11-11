import type { StoredEntity } from "./client.ts";
/** Journal ordinals establish local chronology. Missing ordinals use ID ordering and must be labeled unknown by the UI. */
export function mergeJournalMessages(
  ...pages: readonly (readonly StoredEntity[])[]
): StoredEntity[] {
  const rows = new Map<string, StoredEntity>();
  for (const item of pages.flat()) {
    const previous = rows.get(item.id);
    if (!previous || item.revision >= previous.revision)
      rows.set(item.id, item);
  }
  return [...rows.values()].sort((a, b) => {
    const left = Number.isSafeInteger(a.journalOrder),
      right = Number.isSafeInteger(b.journalOrder);
    return left && right
      ? a.journalOrder! - b.journalOrder!
      : left
        ? -1
        : right
          ? 1
          : a.id.localeCompare(b.id);
  });
}
