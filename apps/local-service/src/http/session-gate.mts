import { createHash, randomBytes, timingSafeEqual } from 'node:crypto';

type Session = { csrfToken: string; createdAt: number; touchedAt: number };
type Options = { origin: string; instanceId: string; now?: () => number };

function rejected(code: string): never {
  throw Object.assign(new Error(code), { code });
}

function equal(first: string, second: string): boolean {
  const hash = (value: string) => createHash('sha256').update(value).digest();
  return timingSafeEqual(hash(first), hash(second));
}

/** Own loopback sessions in memory. Restart and re-pair invalidate every prior cookie. */
export function createSessionGate({ origin, instanceId, now = Date.now }: Options) {
  const url = new URL(origin);
  if (url.protocol !== 'http:' || url.hostname !== '127.0.0.1' || url.origin !== origin
    || !/^[a-zA-Z0-9-]{1,80}$/.test(instanceId)) rejected('INVALID_LOCAL_ORIGIN');
  const cookieName = `paos_session_${instanceId}`;
  const sessions = new Map<string, Session>();
  let pairing: { code: string; expiresAt: number; attempts: number } | undefined;

  function validateOrigin(request: Request, mutation: boolean) {
    const requested = new URL(request.url);
    if (requested.origin !== origin || request.headers.get('host') !== url.host
      || request.headers.has('x-forwarded-host') || request.headers.has('forwarded')
      || request.headers.get('sec-fetch-site') === 'cross-site') rejected('ORIGIN_REJECTED');
    const supplied = request.headers.get('origin');
    if ((mutation && supplied !== origin) || (supplied !== null && supplied !== origin)) rejected('ORIGIN_REJECTED');
  }

  function issuePairingCode(): string {
    sessions.clear();
    const code = randomBytes(16).toString('hex');
    pairing = { code, expiresAt: now() + 60_000, attempts: 0 };
    return code;
  }

  /** Session admission is internal: legacy pairing and guarded desktop navigation share these invariants. */
  function createSession() {
    for (const [token,session] of sessions) if (now()-session.touchedAt>=30*60_000 || now()-session.createdAt>=8*60*60_000) sessions.delete(token);
    if (sessions.size>=64) sessions.delete(sessions.keys().next().value!);
    const token = randomBytes(32).toString('hex');
    const csrfToken = randomBytes(32).toString('hex');
    sessions.set(token, { csrfToken, createdAt: now(), touchedAt: now() });
    return { csrfToken, cookie: `${cookieName}=${token}; HttpOnly; SameSite=Strict; Path=/` };
  }

  function exchange(request: Request, code: unknown) {
    validateOrigin(request, true);
    if (request.method !== 'POST' || request.headers.get('content-type')?.split(';')[0].trim() !== 'application/json') {
      rejected('JSON_REQUIRED');
    }
    if (!pairing || pairing.expiresAt <= now() || pairing.attempts >= 5) rejected('PAIRING_INVALID');
    pairing.attempts++;
    if (typeof code !== 'string' || code.length > 64 || !equal(code, pairing.code)) rejected('PAIRING_INVALID');
    pairing = undefined;
    return createSession();
  }

  function authorize(request: Request) {
    const mutation = request.method !== 'GET' && request.method !== 'HEAD';
    validateOrigin(request, mutation);
    const cookies = (request.headers.get('cookie') ?? '').split(';').map((part) => part.trim());
    const matches = cookies.filter((part) => part.startsWith(`${cookieName}=`));
    if (matches.length !== 1) rejected('SESSION_REQUIRED');
    const token = matches[0].slice(cookieName.length + 1);
    const session = sessions.get(token);
    if (!session || now() - session.touchedAt >= 30 * 60_000 || now() - session.createdAt >= 8 * 60 * 60_000) {
      sessions.delete(token);
      rejected('SESSION_REQUIRED');
    }
    if (mutation && !equal(request.headers.get('x-paos-csrf') ?? '', session.csrfToken)) rejected('CSRF_INVALID');
    session.touchedAt = now();
    return { actorId: 'local-user', csrfToken: session.csrfToken, instanceId } as const;
  }

  return { issuePairingCode, exchange, createSession, authorize, validateOrigin, revokeAll: () => sessions.clear() };
}
