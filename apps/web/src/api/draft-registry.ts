import { createDraftAutosave, type DraftRecord } from "./draft-autosave.ts";
export type DraftStorage = {
  read(): Promise<DraftRecord>;
  write(record: DraftRecord, body: string, key: string): Promise<DraftRecord>;
};
export type DraftSnapshot = Readonly<{
  body: string;
  version: number;
  saving: boolean;
  error: string | null;
}>;
export type SendTicket = {
  readonly clientMessageId: string;
  acknowledge(): Promise<boolean>;
  markUncertain(): void;
};
export type DraftLease = {
  snapshot(): DraftSnapshot;
  subscribe(listener: (snapshot: DraftSnapshot) => void): () => void;
  edit(body: string): void;
  flush(body?: string): Promise<boolean>;
  beginSend(input: string): SendTicket;
  release(): void;
};
type Entry = {
  key: string;
  controller: ReturnType<typeof createDraftAutosave>;
  state: DraftSnapshot;
  listeners: Set<(state: DraftSnapshot) => void>;
  leases: number;
  tickets: number;
};

/** One registry belongs to one authenticated local app client. Only active or unresolved scopes are retained. */
export function createDraftRegistry(limit = 16) {
  if (!Number.isSafeInteger(limit) || limit < 1)
    throw new Error("INVALID_DRAFT_SCOPE_LIMIT");
  const entries = new Map<string, Entry>();
  function collect(entry: Entry) {
    if (entries.get(entry.key) !== entry) return;
    if (
      entry.leases === 0 &&
      entry.tickets === 0 &&
      !entry.controller.isPending()
    ) {
      entries.delete(entry.key);
      entry.controller.dispose();
    }
  }
  function publish(entry: Entry, patch: Partial<DraftSnapshot>) {
    entry.state = { ...entry.state, ...patch };
    for (const listener of [...entry.listeners]) listener(entry.state);
  }
  function desired(entry: Entry, body: string) {
    if (body === entry.state.body) return;
    publish(entry, { body, version: entry.state.version + 1 });
    entry.controller.edit(body);
  }
  function create(key: string, storage: DraftStorage): Entry {
    const entry = {
      key,
      state: { body: "", version: 0, saving: false, error: null },
      listeners: new Set(),
      leases: 0,
      tickets: 0,
    } as Entry;
    entry.controller = createDraftAutosave({
      ...storage,
      restore: (body) => publish(entry, { body }),
      busy: (saving) =>
        publish(entry, { saving, ...(saving ? { error: null } : {}) }),
      error: (cause) => publish(entry, { error: String(cause) }),
      changed: () => collect(entry),
    });
    entries.set(key, entry);
    return entry;
  }
  return {
    get size() {
      return entries.size;
    },
    acquire(
      scope: readonly [string, string],
      storage: DraftStorage,
    ): DraftLease {
      if (scope.some((value) => !value)) throw new Error("INVALID_DRAFT_SCOPE");
      const key = JSON.stringify(scope);
      let entry = entries.get(key);
      if (!entry) {
        if (entries.size >= limit) throw new Error("DRAFT_SCOPE_CAPACITY");
        entry = create(key, storage);
      }
      const current = entry;
      current.leases++;
      let released = false;
      const ownListeners = new Set<(state: DraftSnapshot) => void>();
      function active() {
        if (released) throw new Error("DRAFT_LEASE_RELEASED");
      }
      return {
        snapshot: () => current.state,
        subscribe(listener) {
          active();
          ownListeners.add(listener);
          current.listeners.add(listener);
          listener(current.state);
          return () => {
            ownListeners.delete(listener);
            current.listeners.delete(listener);
          };
        },
        edit(body) {
          active();
          desired(current, body);
        },
        async flush(body) {
          active();
          if (body !== undefined) desired(current, body);
          return current.controller.flush();
        },
        release() {
          if (released) return;
          released = true;
          for (const listener of ownListeners)
            current.listeners.delete(listener);
          ownListeners.clear();
          current.leases--;
          // Keep this controller reusable until pending persistence/tickets settle; no stale re-read on reopen.
          void current.controller
            .flushPending()
            .finally(() => collect(current));
          collect(current);
        },
        beginSend(input) {
          active();
          if (input !== current.state.body)
            throw new Error("DRAFT_SEND_VERSION_MISMATCH");
          if (current.tickets) throw new Error("DRAFT_SEND_PENDING");
          const version = current.state.version;
          current.tickets++;
          let settled = false;
          const clientMessageId = crypto.randomUUID();
          return {
            clientMessageId,
            async acknowledge() {
              if (settled) return false;
              settled = true;
              try {
                if (
                  current.state.version === version &&
                  current.state.body === input
                ) {
                  desired(current, "");
                  return await current.controller.flush();
                }
                return true;
              } finally {
                current.tickets--;
                collect(current);
              }
            },
            markUncertain() {
              if (settled) return;
              settled = true;
              current.tickets--;
              collect(current);
            },
          };
        },
      };
    },
  };
}

/** A command ACK is consumed before any optional state refresh; unknown outcomes retain the draft. */
export function isSendAccepted(result: unknown): boolean {
  const state =
    result && typeof result === "object"
      ? (result as { state?: unknown }).state
      : undefined;
  return Boolean(
    typeof state === "string" &&
    [
      "running",
      "awaiting_approval",
      "interrupt_requested",
      "completed",
      "interrupted",
    ].includes(state),
  );
}
export async function sendWithDraftAck<T>(
  lease: DraftLease,
  input: string,
  send: (id: string) => Promise<T>,
) {
  const ticket = lease.beginSend(input);
  let result: T;
  try {
    result = await send(ticket.clientMessageId);
  } catch (error) {
    ticket.markUncertain();
    throw error;
  }
  if (!isSendAccepted(result)) {
    ticket.markUncertain();
    return { result, acknowledged: false, cleanupSaved: false };
  }
  const cleanupSaved = await ticket.acknowledge();
  return { result, acknowledged: true, cleanupSaved };
}
