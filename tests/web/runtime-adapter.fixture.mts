import { createInterface } from 'node:readline';

const send = (message: unknown) => process.stdout.write(`${JSON.stringify(message)}\n`);
const input = createInterface({ input: process.stdin });
let turn = 0;
input.on('line', (line) => {
  const request = JSON.parse(line);
  if (request.id === undefined || request.method === undefined) return;
  switch (request.method) {
    case 'initialize':
      send({ id: request.id, result: { userAgent: 'synthetic', codexHome: 'synthetic-profile' } });
      break;
    case 'account/read':
      send({ id: request.id, result: { account: null, requiresOpenaiAuth: true } });
      break;
    case 'account/login/start':
      send({ id: request.id, result: { type: 'apiKey' } });
      break;
    case 'account/logout':
      send({ id: request.id, result: {} });
      break;
    case 'thread/start':
      send({ id: request.id, result: {
        thread: { id: `thread-${request.params.cwd.endsWith('foreign') ? 'foreign' : 'own'}`, cwd: request.params.cwd },
        cwd: request.params.cwd, approvalPolicy: request.params.approvalPolicy, modelProvider: 'openai',
        runtimeWorkspaceRoots: [request.params.cwd], activePermissionProfile: { id: request.params.permissions },
        sandbox: { type: request.params.permissions === 'paos_execution' ? 'workspaceWrite' : 'readOnly', networkAccess: false,
          writableRoots: [], excludeSlashTmp: true, excludeTmpdirEnvVar: true },
      } });
      break;
    case 'turn/start':
      turn += 1;
      send({ id: request.id, result: { turn: { id: `turn-${turn}`, status: 'inProgress' } } });
      break;
    case 'turn/interrupt':
      send({ id: request.id, result: {} });
      break;
    case 'thread/read':
      send({ id: request.id, result: { thread: { id: request.params.threadId, turns: [{ id: `turn-${turn}`, status: 'interrupted' }] } } });
      break;
    default:
      send({ id: request.id, error: { code: -32601, message: 'synthetic unknown method' } });
  }
});
process.on('message', (message: { message?: unknown; disconnect?: boolean }) => {
  if (message.message) send(message.message);
  if (message.disconnect) process.exit(0);
});
input.on('close', () => process.exit(0));
