import type { Page, RuntimeState, StoredEntity, Connection } from "./client.ts";
import { mergeJournalMessages } from "./message-history.ts";
export type SessionUpdate = {
  state: RuntimeState;
  messages: StoredEntity[];
  hasMore: boolean;
  historyOffset: number;
  messagesError?: string;
  messagesLoading?: boolean;
};
type Options = {
  state(signal: AbortSignal): Promise<RuntimeState>;
  messages(offset: number, signal: AbortSignal): Promise<Page>;
  publish(update: SessionUpdate): void;
  error(error: unknown): void;
  schedule?: (callback: () => void, delay: number) => unknown;
  cancel?: (timer: unknown) => void;
};
type ConnectionPollOptions = {
  read(): Promise<Connection>;
  publish(connection: Connection): void;
  error(cause: unknown): void;
  version?: () => number;
  schedule?: (callback: () => void, delay: number) => unknown;
  cancel?: (timer: unknown) => void;
};
/** Local broker status only: one read in flight, no auth actions, and no late result across mutation/disposal. */
export function startConnectionPolling(
  options: ConnectionPollOptions,
): () => void {
  let active = true,
    timer: unknown;
  const schedule =
      options.schedule ?? ((callback, delay) => setTimeout(callback, delay)),
    cancel =
      options.cancel ??
      ((timer) => clearTimeout(timer as ReturnType<typeof setTimeout>));
  async function tick() {
    const version = options.version?.() ?? 0;
    try {
      const value = await options.read();
      if (active && version === (options.version?.() ?? 0))
        options.publish(value);
    } catch (cause) {
      if (active && version === (options.version?.() ?? 0))
        options.error(cause);
    } finally {
      if (active)
        timer = schedule(() => {
          void tick();
        }, 750);
    }
  }
  void tick();
  return () => {
    active = false;
    if (timer !== undefined) cancel(timer);
  };
}
/** Runtime state and bounded transcript reads have independent single-flight lanes and shared cancellation. */
export function startSessionPolling(options: Options): () => void {
  const controller = new AbortController();
  const schedule =
    options.schedule ?? ((callback, delay) => setTimeout(callback, delay));
  const cancel =
    options.cancel ??
    ((timer) => clearTimeout(timer as ReturnType<typeof setTimeout>));
  let timer: unknown;
  let state: RuntimeState | undefined, messageFlight: Promise<void> | undefined;
  let transcript: {
    items: StoredEntity[];
    hasMore: boolean;
    historyOffset: number;
  } = { items: [], hasMore: false, historyOffset: 0 };
  let messagesLoading = true,
    messagesError: string | undefined;
  function publish() {
    if (!controller.signal.aborted && state)
      options.publish({
        state,
        messages: transcript.items,
        hasMore: transcript.hasMore,
        historyOffset: transcript.historyOffset,
        messagesLoading,
        messagesError,
      });
  }
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
  async function refreshMessages() {
    messagesLoading = true;
    try {
      const page = await messages();
      if (controller.signal.aborted) return;
      transcript = page;
      messagesError = undefined;
    } catch (error) {
      if (!controller.signal.aborted) messagesError = String(error);
    } finally {
      messagesLoading = false;
      publish();
    }
  }
  async function tick() {
    if (!messageFlight)
      messageFlight = refreshMessages().finally(() => {
        messageFlight = undefined;
      });
    try {
      const current = await options.state(controller.signal);
      if (!controller.signal.aborted) {
        state = current;
        publish();
      }
    } catch (error) {
      if (!controller.signal.aborted) {
        if (state)
          state = {
            ...state,
            canSend: false,
            state: "recovery_required",
            reason: "runtime_state_unavailable",
            pendingApprovals: [],
          };
        options.error(error);
        publish();
      }
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
