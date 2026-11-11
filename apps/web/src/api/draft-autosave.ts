export type DraftRecord = { id: string; body: string; revision: number };
type Options = {
  read(): Promise<DraftRecord>;
  write(record: DraftRecord, body: string, key: string): Promise<DraftRecord>;
  restore(body: string): void;
  error(cause: unknown): void;
  busy?(busy: boolean): void;
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
  const ready = options
    .read()
    .then((record) => {
      baseline = record;
      if (wanted === undefined && !disposed) options.restore(record.body);
    })
    .catch((cause) => {
      blocked = true;
      error(cause);
    });
  async function run(retry: boolean): Promise<boolean> {
    await ready;
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
    },
    async flush(body?: string) {
      if (body !== undefined) wanted = body;
      clear();
      return run(true);
    },
    dispose() {
      clear();
      disposed = true;
      void run(false);
    },
  };
}
