export type DraftRecord = { id: string; body: string; revision: number };
type Options = {
  read(): Promise<DraftRecord>;
  write(record: DraftRecord, body: string, key: string): Promise<DraftRecord>;
  restore(body: string): void;
  error(cause: unknown): void;
  busy?(busy: boolean): void;
  changed?(): void;
  schedule?: (callback: () => void, delay: number) => unknown;
  cancel?: (timer: unknown) => void;
};
/** Serial optimistic writes. Failed intents retain their key for explicit retry, never adopt a newer revision blindly. */
export function createDraftAutosave(options: Options) {
  let baseline: DraftRecord | undefined,
    wanted: string | undefined,
    job: { record: DraftRecord; body: string; key: string } | undefined,
    working: Promise<boolean> | undefined,
    timer: unknown,
    blocked = false,
    disposed = false;
  const schedule =
      options.schedule ?? ((callback, delay) => setTimeout(callback, delay)),
    cancel =
      options.cancel ??
      ((timer) => clearTimeout(timer as ReturnType<typeof setTimeout>));
  function clear() {
    if (timer !== undefined) {
      cancel(timer);
      timer = undefined;
    }
  }
  function error(cause: unknown) {
    if (!disposed) options.error(cause);
  }
  let loading: Promise<void> | undefined;
  function load(recovering = false): Promise<void> {
    loading ??= options
      .read()
      .then((record) => {
        // A failed initial read establishes no revision. Retrying must not discard a different saved draft.
        if (
          recovering &&
          wanted !== undefined &&
          record.body !== "" &&
          record.body !== wanted
        )
          throw new Error("DRAFT_RECOVERY_CONFLICT");
        baseline = record;
        blocked = false;
        if (wanted === undefined && !disposed) options.restore(record.body);
      })
      .catch((cause) => {
        blocked = true;
        error(cause);
      })
      .finally(() => {
        loading = undefined;
        options.changed?.();
      });
    return loading;
  }
  const ready = load();
  async function run(retry: boolean): Promise<boolean> {
    await ready;
    if (!baseline && retry) await load(true);
    if (!baseline || (blocked && !retry)) return false;
    if (working) return working;
    if (!job && (wanted === undefined || wanted === baseline.body)) return true;
    blocked = false;
    working = (async () => {
      if (!disposed) options.busy?.(true);
      try {
        while (job || (wanted !== undefined && wanted !== baseline!.body)) {
          job ??= {
            record: baseline!,
            body: wanted!,
            key: crypto.randomUUID(),
          };
          baseline = await options.write(job.record, job.body, job.key);
          job = undefined;
        }
        return true;
      } catch (cause) {
        blocked = true;
        error(cause);
        return false;
      } finally {
        working = undefined;
        if (!disposed) options.busy?.(false);
        options.changed?.();
      }
    })();
    return working;
  }
  return {
    edit(body: string) {
      if (disposed) return;
      wanted = body;
      clear();
      if (!blocked)
        timer = schedule(() => {
          timer = undefined;
          void run(false);
        }, 500);
      options.changed?.();
    },
    async flush(body?: string) {
      if (body !== undefined) wanted = body;
      clear();
      return run(true);
    },
    flushPending() {
      clear();
      return run(false);
    },
    isPending() {
      return Boolean(
        loading ||
        working ||
        job ||
        (wanted !== undefined && (!baseline || wanted !== baseline.body)),
      );
    },
    dispose() {
      clear();
      disposed = true;
      void run(false);
    },
  };
}
