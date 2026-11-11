/** Superseded or disposed requests cannot publish into a newly selected project/query. */
export function createLatestRequest() {
  let sequence = 0;
  let controller: AbortController | undefined;
  return {
    async run<T>(
      load: (signal: AbortSignal) => Promise<T>,
      publish: (value: T) => void,
      error: (cause: unknown) => void,
    ) {
      controller?.abort();
      controller = new AbortController();
      const own = ++sequence;
      const signal = controller.signal;
      try {
        const value = await load(signal);
        if (own === sequence && !signal.aborted) publish(value);
      } catch (cause) {
        if (own === sequence && !signal.aborted) error(cause);
      }
    },
    dispose() {
      sequence++;
      controller?.abort();
    },
  };
}
