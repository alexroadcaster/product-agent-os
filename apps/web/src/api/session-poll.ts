import type { Page, RuntimeState, StoredEntity } from "./client.ts";
import { mergeJournalMessages } from "./message-history.ts";
export type SessionUpdate = {
  state: RuntimeState;
  messages: StoredEntity[];
  hasMore: boolean;
  historyOffset: number;
};
type Options = {
  state(signal: AbortSignal): Promise<RuntimeState>;
  messages(offset: number, signal: AbortSignal): Promise<Page>;
  publish(update: SessionUpdate): void;
  error(error: unknown): void;
  schedule?: (callback: () => void, delay: number) => unknown;
  cancel?: (timer: unknown) => void;
};
/** One in-flight cycle, at most 20 pages/cycle, one 750ms retry timer; disposal aborts all requests. */
export function startSessionPolling(options: Options): () => void {
  const controller = new AbortController();
  const schedule =
    options.schedule ?? ((callback, delay) => setTimeout(callback, delay));
  const cancel =
    options.cancel ??
    ((timer) => clearTimeout(timer as ReturnType<typeof setTimeout>));
  let timer: unknown;
  async function messages() {
    const rows = new Map<string, StoredEntity>();
    let more = false;
    let historyOffset = 0;
    for (let page = 0; page < 20; page++) {
      const result = await options.messages(page * 50, controller.signal);
      if (controller.signal.aborted)
        return { items: [], hasMore: false, historyOffset: 0 };
      historyOffset = page * 50 + result.items.length;
      for (const item of result.items) {
        const prior = rows.get(item.id);
        if (!prior || item.revision >= prior.revision) rows.set(item.id, item);
      }
      more = result.hasMore;
      if (!more) break;
    }
    return {
      items: mergeJournalMessages([...rows.values()]),
      hasMore: more,
      historyOffset,
    };
  }
  async function tick() {
    try {
      const [state, page] = await Promise.all([
        options.state(controller.signal),
        messages(),
      ]);
      if (!controller.signal.aborted)
        options.publish({
          state,
          messages: page.items,
          hasMore: page.hasMore,
          historyOffset: page.historyOffset,
        });
    } catch (error) {
      if (!controller.signal.aborted) options.error(error);
    } finally {
      if (!controller.signal.aborted)
        timer = schedule(() => {
          void tick();
        }, 750);
    }
  }
  void tick();
  return () => {
    controller.abort();
    if (timer !== undefined) cancel(timer);
  };
}
