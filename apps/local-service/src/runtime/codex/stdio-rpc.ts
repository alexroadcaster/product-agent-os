import { createHash, randomUUID } from 'node:crypto';
import type { ChildProcessWithoutNullStreams } from 'node:child_process';
import { once } from 'node:events';

const clientMethods = new Set([
  'initialize', 'config/read', 'configRequirements/read', 'permissionProfile/list',
  'windowsSandbox/readiness',
  'account/read', 'account/login/start', 'account/logout', 'thread/start', 'thread/resume',
  'thread/read', 'thread/list', 'thread/items/list', 'thread/turns/list', 'turn/start', 'turn/interrupt',
]);
const serverMethods = new Set([
  'item/commandExecution/requestApproval', 'item/fileChange/requestApproval',
  'item/permissions/requestApproval', 'item/tool/requestUserInput', 'item/tool/call',
]);
type Id = string | number;
export type RpcMessage = Record<string, unknown>;
export type RpcListener = (message: RpcMessage) => void;
export type RpcClosedListener = (reason: string) => void;

export class RuntimeRpcError extends Error {
  readonly code: string;
  constructor(code: string) { super('The local runtime request could not be completed.'); this.code = code; }
}

export type RuntimeRpc = Readonly<{
  generation: string;
  request: (method: string, params: unknown) => Promise<RpcMessage>;
  notify: (method: 'initialized') => void;
  respond: (id: Id, result: unknown) => void;
  respondError: (id: Id, code?: number) => void;
  subscribe: (listener: RpcListener) => () => void;
  onClosed: (listener: RpcClosedListener) => () => void;
  close: () => Promise<void>;
  snapshot: () => Readonly<{ generation: string; status: 'open' | 'closed'; pending: number; stderrBytes: number }>;
}>;

function object(value: unknown): RpcMessage {
  return value !== null && typeof value === 'object' && !Array.isArray(value) ? value as RpcMessage : {};
}
function identifier(value: unknown): value is Id {
  return (typeof value === 'string' && value.length > 0) || (typeof value === 'number' && Number.isSafeInteger(value));
}

/** A generation-bound stdio connection. Errors expose categories; raw stderr and provider error text are discarded. */
export function createStdioRpc(
  child: ChildProcessWithoutNullStreams,
  options: Readonly<{ timeoutMs?: number; maxFrameBytes?: number }> = {},
): RuntimeRpc {
  const generation = randomUUID();
  const timeoutMs = options.timeoutMs ?? 15_000;
  const maxFrameBytes = options.maxFrameBytes ?? 1024 * 1024;
  const pending = new Map<Id, { resolve: (value: RpcMessage) => void; reject: (error: Error) => void; timer: ReturnType<typeof setTimeout> }>();
  const requests = new Map<Id, { digest: string; status: 'pending' | 'answered' | 'resolved' }>();
  const listeners = new Set<RpcListener>();
  const closedListeners = new Set<RpcClosedListener>();
  let sequence = 0;
  let status: 'open' | 'closed' = 'open';
  let closeReason = 'runtime_closed';
  let buffer = '';
  let stderrBytes = 0;

  function terminate(reason: string): void {
    if (status === 'closed') return;
    status = 'closed'; closeReason = reason;
    for (const item of pending.values()) {
      clearTimeout(item.timer); item.reject(new RuntimeRpcError(reason));
    }
    pending.clear();
    for (const listener of closedListeners) { try {listener(reason);} catch { /* A consumer cannot retain the child or pending calls. */ } }
    if (child.exitCode === null && child.signalCode === null) child.kill();
  }

  function write(message: unknown): void {
    if (status !== 'open') throw new RuntimeRpcError('runtime_closed');
    const encoded = JSON.stringify(message);
    if (Buffer.byteLength(encoded) > maxFrameBytes) throw new RuntimeRpcError('frame_too_large');
    child.stdin.write(`${encoded}\n`, (error) => { if (error) terminate('runtime_write_failed'); });
  }

  function deliver(message: RpcMessage): void {
    for (const listener of listeners) {
      try { listener(message); } catch { terminate('runtime_consumer_failed'); }
    }
  }

  function accept(raw: unknown): void {
    const message = object(raw);
    const { id, method } = message;
    if (typeof method === 'string') {
      if (identifier(id)) {
        if (!serverMethods.has(method)) {
          write({ id, error: { code: -32601, message: 'Unsupported local runtime request.' } });
          return;
        }
        const digest = createHash('sha256').update(JSON.stringify({ method, params: message.params })).digest('hex');
        const old = requests.get(id);
        if (old) {
          if (old.digest !== digest) terminate('runtime_request_conflict');
          return;
        }
        if (requests.size >= 1024) { terminate('runtime_request_limit'); return; }
        requests.set(id, { digest, status: 'pending' });
      } else if (id !== undefined) {
        terminate('runtime_invalid_frame'); return;
      }
      if (method === 'serverRequest/resolved') {
        const requestId = object(message.params).requestId;
        if (identifier(requestId)) {
          const old = requests.get(requestId);
          if (old) old.status = 'resolved';
        }
      }
      deliver(message);
      return;
    }
    if (!identifier(id) || !pending.has(id)) { terminate('runtime_unmatched_response'); return; }
    const item = pending.get(id)!;
    clearTimeout(item.timer); pending.delete(id);
    if (message.error !== undefined) item.reject(new RuntimeRpcError('rpc_rejected'));
    else if (Object.hasOwn(message, 'result')) item.resolve(object(message.result));
    else { item.reject(new RuntimeRpcError('runtime_invalid_frame')); terminate('runtime_invalid_frame'); }
  }

  child.stdout.setEncoding('utf8');
  child.stdout.on('data', (chunk: string) => {
    if (status === 'closed') return;
    buffer += chunk;
    while (buffer.includes('\n')) {
      const newline = buffer.indexOf('\n');
      const line = buffer.slice(0, newline); buffer = buffer.slice(newline + 1);
      if (Buffer.byteLength(line) > maxFrameBytes) { terminate('runtime_frame_too_large'); return; }
      try { accept(JSON.parse(line)); } catch { terminate('runtime_invalid_frame'); return; }
    }
    if (Buffer.byteLength(buffer) > maxFrameBytes) terminate('runtime_frame_too_large');
  });
  child.stderr.on('data', (chunk: Buffer) => { stderrBytes += chunk.length; });
  child.on('error', () => terminate('runtime_process_failed'));
  child.on('exit', () => terminate(buffer.trim() ? 'runtime_incomplete_frame' : 'runtime_eof'));

  function answer(id: Id, payload: RpcMessage): void {
    const state = requests.get(id);
    if (!state || state.status !== 'pending') throw new RuntimeRpcError('runtime_request_stale');
    state.status = 'answered';
    write({ id, ...payload });
  }

  return {
    generation,
    request(method, params) {
      if (!clientMethods.has(method)) return Promise.reject(new RuntimeRpcError('method_denied'));
      if (status !== 'open') return Promise.reject(new RuntimeRpcError('runtime_closed'));
      if (pending.size >= 64) return Promise.reject(new RuntimeRpcError('runtime_request_limit'));
      const id = `paos-${++sequence}`;
      return new Promise((resolve, reject) => {
        const timer = setTimeout(() => terminate('runtime_timeout'), timeoutMs);
        pending.set(id, { resolve, reject, timer });
        try { write({ id, method, params }); }
        catch (error) { clearTimeout(timer); pending.delete(id); reject(error); }
      });
    },
    notify(method) { write({ method }); },
    respond(id, result) { answer(id, { result }); },
    respondError(id, code = -32601) { answer(id, { error: { code, message: 'The local request is unavailable.' } }); },
    subscribe(listener) { listeners.add(listener); return () => { listeners.delete(listener); }; },
    onClosed(listener) {
      closedListeners.add(listener);
      if (status === 'closed') listener(closeReason);
      return () => { closedListeners.delete(listener); };
    },
    async close() {
      if (status === 'open') { child.stdin.end(); terminate('runtime_closed'); }
      if (child.exitCode === null && child.signalCode === null) {
        let timer:ReturnType<typeof setTimeout>|undefined;
        try {await Promise.race([once(child, 'exit'), new Promise<void>((resolve) => {timer=setTimeout(resolve,1000);})]);}
        finally {if(timer)clearTimeout(timer);}
      }
    },
    snapshot: () => ({ generation, status, pending: pending.size, stderrBytes }),
  };
}
