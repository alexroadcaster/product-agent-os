/** Admission limits for PAOS-mediated work. These never grant host permissions. */
export type AutonomyPolicy = Readonly<{
  schemaVersion: 'autonomy_policy_v1';
  allowedTaskIds: readonly string[];
  allowedPaths: readonly string[];
  allowedActions: readonly ('execution' | 'command')[];
  maxRuns: number;
  maxCommandsPerRun: number;
  maxRunSeconds: number;
  concurrency: 1;
  stopOnFailedCommand: boolean;
}>;
export type AutonomyReservation = {
  runId: string; bindingId: string; sessionId: string; taskId: string;
  startedAt: number; deadlineAt: number; operationIds: string[]; stopReason?: string;
};
export type AutonomySnapshot = {
  revision: number; policy: AutonomyPolicy | null; paused: boolean; budgetId: string;
  runs: AutonomyReservation[]; usedRuns: number;
  enforcement: 'paos_mediated_commands';
  hostToolsConstrained: false; perFileSandbox: false;
};
export type AutonomyPreview = {
  previewDigest: string; policy: AutonomyPolicy; executable: boolean; reasons: string[];
  boundaries: { hostPermissionsChanged: false; nativeApprovalRequired: true; concurrency: 1;
    scope: 'entire_workspace' | 'unsupported_narrow_paths'; tokenCostMetering: 'unavailable' };
};
export const defaultAutonomyPolicy = (): AutonomyPolicy => ({
  schemaVersion: 'autonomy_policy_v1', allowedTaskIds: [], allowedPaths: ['.'],
  allowedActions: ['execution'], maxRuns: 1, maxCommandsPerRun: 0, maxRunSeconds: 300,
  concurrency: 1, stopOnFailedCommand: true,
});
const fail = (): never => { throw Object.assign(new Error('Invalid autonomy policy'), { code: 'AUTONOMY_POLICY_INVALID' }); };
/** Reject unknown fields (including pretend token/cost limits) instead of silently ignoring them. */
export function decodeAutonomyPolicy(value: unknown): AutonomyPolicy {
  if (!value || typeof value !== 'object' || Array.isArray(value)) fail();
  const v = value as Record<string, unknown>;
  const keys = Object.keys(defaultAutonomyPolicy());
  if (Object.keys(v).length !== keys.length || Object.keys(v).some(key => !keys.includes(key))) fail();
  const strings = (raw: unknown, max: number): string[] => {
    if (!Array.isArray(raw) || raw.length > max || raw.some(s => typeof s !== 'string' || !s || s.length > 200 || /[\0\r\n]/.test(s))
      || new Set(raw).size !== raw.length) fail();
    return [...raw as string[]];
  };
  const tasks = strings(v.allowedTaskIds, 1000), paths = strings(v.allowedPaths, 100), actions = strings(v.allowedActions, 2);
  if (!paths.length || paths.some(p => p !== '.' && (p.includes('\\') || p.includes(':') || p.startsWith('/')
    || p.split('/').some(part => !part || part === '.' || part === '..') || /[<>|?*]/.test(p)))) fail();
  if (!actions.length || actions.some(a => !['execution', 'command'].includes(a)) || !actions.includes('execution')) fail();
  const bounded = (n: unknown, min: number, max: number): number => {
    if (typeof n !== 'number' || !Number.isSafeInteger(n) || n < min || n > max) fail();
    return n as number;
  };
  if (v.schemaVersion !== 'autonomy_policy_v1' || v.concurrency !== 1 || typeof v.stopOnFailedCommand !== 'boolean') fail();
  const commands = bounded(v.maxCommandsPerRun, 0, 64);
  if (!actions.includes('command') && commands !== 0) fail();
  return { schemaVersion: 'autonomy_policy_v1', allowedTaskIds: tasks, allowedPaths: paths,
    allowedActions: actions as ('execution' | 'command')[], maxRuns: bounded(v.maxRuns, 1, 1000),
    maxCommandsPerRun: commands, maxRunSeconds: bounded(v.maxRunSeconds, 1, 3600),
    concurrency: 1, stopOnFailedCommand: v.stopOnFailedCommand as boolean };
}
