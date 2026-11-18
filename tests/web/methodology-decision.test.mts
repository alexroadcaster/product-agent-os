import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {mkdtempSync, readFileSync, realpathSync, rmSync, writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {dirname, join} from 'node:path';
import test from 'node:test';
import {fileURLToPath} from 'node:url';
import {decodeMethodologyDecision, type MethodologyScope} from '../../packages/contracts/methodology-decision.ts';

const fixture = JSON.parse(readFileSync(new URL('../fixtures/product_agent_os/pmeth-b1-synthetic.json', import.meta.url), 'utf8'));
const runner = fileURLToPath(new URL('../../plugins/product-agent-os/scripts/run_codex_runtime_runner.py', import.meta.url));
const cases: Record<string, {task: Record<string, unknown>; expected: {step_kind: string; target: string}}> = fixture.cases;

test('the TypeScript reader accepts real Python CLI advice for both B1 tasks and refuses mismatched wire evidence', t => {
  const temp = realpathSync(tmpdir());
  const workspace = mkdtempSync(join(temp, 'paos-b1-'));
  t.after(() => {
    assert.equal(dirname(realpathSync(workspace)), temp);
    rmSync(workspace, {recursive: true});
  });
  for (const [name, contents] of Object.entries<string>(fixture.files)) {
    writeFileSync(join(workspace, name), contents);
  }
  for (const [name, data] of Object.entries(cases)) {
    writeFileSync(join(workspace, `${name}.json`), JSON.stringify(data.task));
  }
  for (const [name, data] of Object.entries(cases)) {
    const cli = spawnSync('python', ['-B', runner, workspace, '--contract', '--task-context', `${name}.json`], {
      encoding: 'utf8', timeout: 30_000,
    });
    assert.ifError(cli.error);
    assert.equal(cli.status, 0, cli.stderr);
    const packet = JSON.parse(cli.stdout).route_packet.methodology_decision;
    const expected: MethodologyScope = {...packet.scope, task_id: String(data.task.task_id)};
    const decoded = decodeMethodologyDecision(packet, expected);
    assert.deepEqual(JSON.parse(JSON.stringify(decoded)), packet);
    assert.equal(decoded.plan.next_step.kind, data.expected.step_kind);
    assert.equal(decoded.plan.next_step.target, data.expected.target);
    assert.equal(decoded.execution, 'not_started');
    for (const key of Object.keys(expected) as Array<keyof MethodologyScope>) {
      assert.throws(() => decodeMethodologyDecision(packet, {...expected, [key]: 'wrong'}), /scope_mismatch/);
    }
    assert.throws(() => decodeMethodologyDecision({...packet, schema_version: 'future'}, expected), /unsupported_version/);
    assert.throws(() => decodeMethodologyDecision({...packet, execution: 'passed'}, expected), /invalid_projection/);
    assert.throws(() => decodeMethodologyDecision({...packet, evidence: []}, expected), /invalid_evidence/);
    const bad = structuredClone(packet);
    bad.plan.next_step.evidence_refs = ['file:dangling.py'];
    assert.throws(() => decodeMethodologyDecision(bad, expected), /invalid_projection/);
  }
});
