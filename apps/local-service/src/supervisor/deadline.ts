export class LifecycleDeadlineError extends Error {}

/** Enforce a local lifecycle deadline and tell the owning adapter to cancel any pending effects. */
export async function withinDeadline<T>(milliseconds: number, operation: (signal: AbortSignal) => Promise<T>): Promise<T> {
  const controller = new AbortController();
  let timer: ReturnType<typeof setTimeout> | undefined;
  const deadline = new Promise<never>((_, reject) => {
    timer = setTimeout(() => {
      reject(new LifecycleDeadlineError('Local service lifecycle deadline exceeded.'));
      controller.abort();
    }, milliseconds);
  });
  try {
    return await Promise.race([deadline, operation(controller.signal)]);
  } finally {
    clearTimeout(timer);
  }
}
