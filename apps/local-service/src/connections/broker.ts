import { createHash } from 'node:crypto';
import {createMessageStreamRedactor} from '../runtime/message-stream.mts';
export type ConnectionState = 'unverified' | 'connecting' | 'connected' | 'disconnected' | 'error';
export type CredentialStore = Readonly<{
  read: (target: string) => Promise<string | null>;
  write: (target: string, secret: string) => Promise<void>;
  delete: (target: string) => Promise<void>;
}>;
export class ConnectionError extends Error {
  readonly code: string;
  constructor(code: string) { super('The local connection is unavailable.'); this.code = code; }
}
const identifier = (value: string) => /^[A-Za-z0-9_-]{1,100}$/.test(value);

/** Only explicit App Server API-key login establishes this generation's connection; it proves no model access. */
export function createConnectionBroker(options: Readonly<{
  profileId: string;
  request: (method: string, params: unknown) => Promise<Record<string, unknown>>;
  store?: CredentialStore;
  onDisconnected?: () => void;
}>) {
  if (!identifier(options.profileId)) throw new ConnectionError('profile_invalid');
  let state: ConnectionState = 'unverified';
  let connectionId: string | null = null;
  let accountScope: string | null = null;
  let busy = false;
  const redactionSecrets = new Set<string>();
  const target = (id: string) => `PAOS/${options.profileId}/${id}`;
  async function connect(input: Readonly<{connectionId: string; apiKey?: string; remember?: boolean}>) {
    if (busy) throw new ConnectionError('connection_busy');
    if (!identifier(input.connectionId)) throw new ConnectionError('connection_invalid');
    if (input.remember && !options.store) throw new ConnectionError('secure_store_unavailable');
    busy = true; state = 'connecting'; connectionId = null; accountScope=null;
    let secret: string | null | undefined = input.apiKey;
    try {
      if (secret === undefined) secret = await options.store?.read(target(input.connectionId));
      if (typeof secret !== 'string' || secret.length === 0 || Buffer.byteLength(secret) > 2560 || /[\r\n\0]/.test(secret)) {
        throw new ConnectionError('credential_invalid');
      }
      if(redactionSecrets.size>=16&&!redactionSecrets.has(secret))throw new ConnectionError('connection_restart_required');
      redactionSecrets.add(secret);
      const login = await options.request('account/login/start', { type: 'apiKey', apiKey: secret });
      if (login.type !== 'apiKey') throw new ConnectionError('auth_route_mismatch');
      const read = await options.request('account/read', { refreshToken: false });
      const account = read.account as Record<string, unknown> | null;
      if (!account || account.type !== 'apiKey') throw new ConnectionError('auth_route_mismatch');
      if (input.remember) await options.store!.write(target(input.connectionId), secret);
      accountScope=createHash('sha256').update(JSON.stringify([options.profileId,input.connectionId,secret])).digest('hex');
      connectionId = input.connectionId; state = 'connected';
    } catch {
      state = 'error'; connectionId = null; accountScope=null;
      try { await options.request('account/logout', {}); } catch { /* No inherited account fallback. */ }
      throw new ConnectionError('connection_failed');
    } finally { secret = null; busy = false; }
    return snapshot();
  }
  function snapshot() { return { state, connectionId, modelAccess: 'unverified' as const, route: 'local_api_byok' as const }; }
  async function disconnect(input: Readonly<{forget?: boolean}> = {}) {
    if (busy) throw new ConnectionError('connection_busy');
    busy = true;
    const previous = connectionId;
    state = 'disconnected'; connectionId = null; accountScope=null; options.onDisconnected?.();
    try {
      await options.request('account/logout', {});
      if (input.forget && previous && options.store) await options.store.delete(target(previous));
    } catch { throw new ConnectionError('disconnect_unverified'); }
    finally { busy = false; }
    return snapshot();
  }
  return { connect, disconnect, snapshot,
    // Keep prior credentials only in private process memory so late runtime frames can still be scrubbed.
    redact(text: string) {
      const stream=createMessageStreamRedactor({secrets:()=>[...redactionSecrets]});
      return stream.push(text)+stream.finish();
    },
    // Factory retains the private registry; neither the stream nor any DTO exposes credential values.
    createStreamRedactor:()=>createMessageStreamRedactor({secrets:()=>[...redactionSecrets]}),
    // Internal scope only; never expose this credential-derived identity in a browser DTO or log.
    accountScopeId: () => accountScope,
    authorize: (id: string) => !busy && state === 'connected' && id === accountScope,
    runtimeClosed() { state = 'disconnected'; connectionId = null; accountScope=null; options.onDisconnected?.(); },
  };
}
