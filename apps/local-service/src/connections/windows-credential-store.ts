import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import type { CredentialStore } from './broker.ts';
import { ConnectionError } from './broker.ts';
export type CredentialBridge = (input: Readonly<{ operation: 'read'|'write'|'delete'; target: string; secret?: string }>) => Promise<{secret?: string|null}>;

/** Secrets cross the child boundary only through stdin; stdout is consumed privately, stderr is discarded. */
export function createWindowsCredentialStore(bridge: CredentialBridge = nativeCredentialBridge): CredentialStore {
  const validate = (target: string) => {
    if (!/^PAOS\/[A-Za-z0-9_-]{1,100}\/[A-Za-z0-9_-]{1,100}$/.test(target)) throw new ConnectionError('credential_target_invalid');
  };
  return {
    async read(target) { validate(target); return (await bridge({ operation: 'read', target })).secret ?? null; },
    async write(target, secret) {
      validate(target);
      if (typeof secret !== 'string' || !secret || Buffer.byteLength(secret) > 2560) throw new ConnectionError('credential_invalid');
      await bridge({ operation: 'write', target, secret });
    },
    async delete(target) { validate(target); await bridge({ operation: 'delete', target }); },
  };
}

/** Requires an explicit caller action. This adapter never runs during service construction. */
export async function nativeCredentialBridge(input: Parameters<CredentialBridge>[0]): ReturnType<CredentialBridge> {
  if (process.platform !== 'win32' || !process.env.SystemRoot) throw new ConnectionError('secure_store_unavailable');
  const { join } = await import('node:path');
  const executable = join(process.env.SystemRoot, 'System32', 'WindowsPowerShell', 'v1.0', 'powershell.exe');
  const script = fileURLToPath(new URL('./windows-credential-bridge.ps1', import.meta.url));
  return new Promise((resolve, reject) => {
    const child = spawn(executable, ['-NoLogo', '-NoProfile', '-NonInteractive', '-File', script], {
      windowsHide: true, shell: false, env: { SystemRoot: process.env.SystemRoot }, stdio: ['pipe','pipe','ignore'],
    });
    let output = ''; let settled = false;
    const finish = (error?: Error, result?: {secret?: string|null}) => {
      if (settled) return; settled = true; clearTimeout(timer); output = '';
      if (error) { child.kill(); reject(error); } else resolve(result ?? {});
    };
    const timer = setTimeout(() => finish(new ConnectionError('secure_store_timeout')), 10_000);
    child.stdout.setEncoding('utf8');
    child.stdout.on('data', (chunk: string) => {
      output += chunk;
      if (Buffer.byteLength(output) > 16384) finish(new ConnectionError('secure_store_failed'));
    });
    child.on('error', () => finish(new ConnectionError('secure_store_failed')));
    child.on('close', (code) => {
      if (code !== 0) { finish(new ConnectionError('secure_store_failed')); return; }
      try {
        const value = JSON.parse(output);
        if (value.ok !== true || (value.secret != null && typeof value.secret !== 'string')) throw new Error();
        finish(undefined, value.secret == null ? {} : {secret: value.secret});
      } catch { finish(new ConnectionError('secure_store_failed')); }
    });
    child.stdin.on('error', () => finish(new ConnectionError('secure_store_failed')));
    child.stdin.end(JSON.stringify(input));
  });
}
