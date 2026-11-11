import type { RuntimeState, StoredEntity } from "./client.ts";
export function visibleAssistantDrafts(
  state: RuntimeState | null,
  messages: readonly StoredEntity[],
) {
  const rows = new Map<
    string,
    NonNullable<RuntimeState["visibleDrafts"]>[number]
  >();
  for (const item of state?.visibleDrafts ?? []) {
    if (
      item.phase !== "final_answer" ||
      item.role !== "assistant" ||
      messages.some(
        (message) =>
          message.data?.runId === item.runId &&
          message.data?.sourceItemId === item.sourceItemId,
      )
    )
      continue;
    const key = `${item.runId}:${item.sourceItemId}`,
      previous = rows.get(key);
    if (!previous || item.revision >= previous.revision) rows.set(key, item);
  }
  return [...rows.values()];
}
