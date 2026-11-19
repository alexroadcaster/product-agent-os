import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {randomUUID} from 'node:crypto';
import {readFile,writeFile,rename,readdir,mkdir,mkdtemp,realpath,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {dirname,join,resolve} from 'node:path';
import test from 'node:test';
import {newM2Task} from '../../packages/contracts/issues/task-profile.ts';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {g03Fixture,until} from './project-g03-fixture.mts';

const scenarioPath=new URL('../fixtures/product_agent_os/pmeth-b1-synthetic.json',import.meta.url);
const route='/projects/p/analysis/task-advice';

async function seed(f:Awaited<ReturnType<typeof g03Fixture>>){
 const fixture=JSON.parse(await readFile(scenarioPath,'utf8'));
 for(const [path,data] of Object.entries<string>(fixture.files))await writeFile(join(f.workspace,path),data);
 const cases=[];
 for(const [name,value] of Object.entries<any>(fixture.cases)){
  const id=randomUUID(),context={...value.task,task_id:id,risks:value.task.risks.map((risk:any)=>({
   ...risk,protected_invariants:value.task.acceptance,
  }))};
  const type=name==='docs_only'?'task':'bug';
  const task={...newM2Task('p',id,context.intent,'local-user'),type,summary:'Synthetic B2 case',technicalValue:'Verify the decision',
   productValue:'Review the next step',acceptanceCriteria:context.acceptance,
   files:context.changed_paths.map((relativePath:string)=>({relativePath,plannedOperation:'modify',actualOperation:null})),
   risks:context.risks.map((risk:any)=>risk.description)};
  const created=await f.request('/projects/p/task-manager/commands',{action:'save',task,expectedRevision:0,
   expectedAuthorityEpoch:1,idempotencyKey:randomUUID()});
  assert.equal(created.status,200,await created.text());
  const filename=name+'.json';
  await writeFile(join(f.workspace,filename),JSON.stringify(context));
  const input={taskId:id,taskRevision:1,mode:context.change_mode,...(name==='docs_only'?{sourcePath:'counter.py'}
   :{testPath:'test_counter.py',testCommand:value.expected.target})};
  cases.push({filename,input,expected:value.expected});
 }
 return cases;
}

async function scan(f:Awaited<ReturnType<typeof g03Fixture>>,suffix='scans'){
 const started=await f.request('/projects/p/'+suffix,{requestId:randomUUID()});
 assert.equal(started.status,202,await started.text());
 return until(async()=>await(await f.request('/projects/p/scans')).json(),state=>
  ['completed','partial','failed'].includes(state.latest?.state));
}

test('task advice uses the existing session, origin and CSRF gates and resolves tasks inside the project', async t=>{
 const f=await g03Fixture(t);
 const path=route;
 const input={taskId:'missing-task',taskRevision:1,mode:'docs_only'};
 assert.equal((await f.request(path,input,{cookie:''})).status,401);
 assert.equal((await f.request(path,input,{origin:'http://127.0.0.1:44000'})).status,403);
 assert.equal((await f.request(path,input,{'x-paos-csrf':''})).status,403);
 const nonexistent=await f.request(path,input);
 assert.equal(nonexistent.status,404);
 assert.equal((await nonexistent.json()).error.code,'TASK_NOT_FOUND');
 const bad=await f.request(path,{...input,sourcePath:'../other.py'});
 assert.equal((await bad.json()).error.code,'TASK_ADVICE_INPUT_INVALID');
 assert.equal((await f.request(path,{...input,sourcePath:'x'.repeat(5000)})).status,413);
});

test('read-only HTTP bridge matches the CLI and retains analysis across schema and code scans',async t=>{
 const f=await g03Fixture(t),cases=await seed(f);
 const empty=await(await f.request(route,cases[0].input)).json();
 assert.equal(empty.status,'unavailable');
 assert.equal(empty.decision,null);
 const observed=await scan(f);
 await mkdir(join(f.root,'other'));
 const other=await bindProject('q',join(f.root,'other'));
 await f.store.registerProject({id:'q',keyPrefix:'OTHR',canonicalRoot:other.workspaceRoot,rootIdentity:other.directoryIdentity,authorityMode:'sql'});
 assert.equal((await f.request('/projects/q/analysis/task-advice',cases[0].input)).status,404);
 const workload=await Promise.all(cases.map(async data=>({data, before:await readFile(join(f.workspace,data.filename))})));
 const freshness=await(await f.request('/projects/p/freshness')).json();
 for(const {data,before} of workload){
  const response=await f.request(route,data.input);
  assert.equal(response.status,200);
  const advice=await response.json();
  assert.equal(advice.status,'ready',JSON.stringify(advice));
  assert.equal(advice.selector,'project_analysis_task_bridge');
  assert.equal(advice.analysisScanId,observed.latest.scanId);
  assert.equal(advice.taskId,data.input.taskId);
  assert.equal(advice.decision.plan.next_step.target,data.expected.target);
  assert.ok(!JSON.stringify(advice).includes(f.workspace));
  assert.deepEqual(await readFile(join(f.workspace,data.filename)),before);
  const cli=spawnSync('python',['-B',resolve('plugins/product-agent-os/scripts/run_codex_runtime_runner.py'),f.workspace,'--contract','--task-context',data.filename],{encoding:'utf8',timeout:10000});
  assert.equal(cli.status,0,cli.stderr);
  const expected=JSON.parse(cli.stdout).route_packet.methodology_decision;
  assert.deepEqual(advice.decision.decisions,expected.decisions);
  assert.deepEqual(advice.decision.plan.next_step,expected.plan.next_step);
  assert.deepEqual(advice.decision.requirements,expected.requirements);
 }
 assert.deepEqual(await(await f.request('/projects/p/freshness')).json(),freshness);
 await scan(f,'database/scan');
 await scan(f,'code-database/scan');
 await f.restart();
 const refreshed=await(await f.request(route,cases[0].input)).json();
 assert.equal(refreshed.status,'ready',JSON.stringify(refreshed));
 assert.equal(refreshed.analysisScanId,observed.latest.scanId);
 assert.equal((await(await f.request('/projects/p/analysis')).json()).availability,'available');
 const missing=await(await f.request(route,{...cases[1].input,sourcePath:'.env'})).json();
 assert.equal(missing.status,'partial');
 assert.equal(missing.decision.plan.next_step.kind,'clarify');
 const staleTask=await f.request(route,{...cases[0].input,taskRevision:99});
 assert.equal(staleTask.status,409);
 await rename(join(f.workspace,'counter.py'),join(f.workspace,'counter-renamed.py'));
 const staleSource=await(await f.request(route,cases[0].input)).json();
 assert.equal(staleSource.status,'stale');
 assert.equal(staleSource.decision,null);
});

test('failed or mismatched Python replies cannot fall back to old advice',async t=>{
 const tmp=await realpath(tmpdir()),scripts=await mkdtemp(join(tmp,'paos-b2-bridge-')),bridge=join(scripts,'bridge.py');
 t.after(async()=>{assert.equal(dirname(await realpath(scripts)),tmp);await rm(scripts,{recursive:true,force:true});});
 const f=await g03Fixture(t,{projectAnalysisRuntime:{bridgePath:bridge}}),cases=await seed(f);
 const trusted=JSON.stringify(resolve('apps/local-service/src/project-analysis/bridge.py'));
 const prefix=`import contextlib, io, json, runpy, sys, time
from pathlib import Path
real = runpy.run_path(${trusted})
if sys.argv[3:] != ["--task-advice"]:
    real["main"]()
    sys.exit()
`;
 const forge=`sys.path.insert(0, sys.argv[1])
with contextlib.redirect_stdout(io.StringIO()) as stream:
    real["emit_task_advice"](Path(sys.argv[2]))
packet = json.loads(stream.getvalue())
`;
 for(const [script,warning] of [
  ['sys.exit(1)\n','ANALYSIS_CORE_FAILED'],
  [forge+'packet["schemaVersion"] = "future"\nprint(json.dumps(packet))\n','TASK_ADVICE_OUTPUT_INVALID'],
  ...['project_id','task_id','source_revision','task_revision'].map(key=>
   [forge+`packet["decision"]["scope"]["${key}"] = "forged"\nprint(json.dumps(packet))\n`,'TASK_ADVICE_OUTPUT_INVALID']),
 ]){
  await writeFile(bridge,prefix+script);
  await scan(f);
  const view=await(await f.request(route,cases[1].input)).json();
  assert.equal(view.status,'unavailable');
  assert.deepEqual(view.warnings,[warning]);
  assert.equal(view.decision,null);
 }
 const marker=join(scripts,'started');
 await writeFile(bridge,prefix+`Path(${JSON.stringify(marker)}).write_text("started")\ntime.sleep(10)\n`);
 await scan(f);
 const before=new Set(await readdir(tmp)),controller=new AbortController();
 const waiting=f.request(route,cases[1].input,{},controller.signal);
 try{
  await until(()=>readFile(marker,'utf8').catch(()=>''),value=>value==='started');
 }finally{controller.abort();}
 const cancelled=await(await waiting).json();
 assert.equal(cancelled.error.code,'TASK_ADVICE_CANCELLED');
 assert.deepEqual((await readdir(tmp)).filter(name=>name.startsWith('paos-advice-')&&!before.has(name)),[]);
});
