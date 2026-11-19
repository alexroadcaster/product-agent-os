import assert from 'node:assert/strict';
import {execFile} from 'node:child_process';
import {createHash,randomUUID} from 'node:crypto';
import {access,mkdir,mkdtemp,readFile,realpath,rm,writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {dirname,isAbsolute,join,resolve} from 'node:path';
import {setTimeout as delay} from 'node:timers/promises';
import {promisify} from 'node:util';
import {startLocalService} from '../../../apps/local-service/src/main.mts';
import {newM2Task} from '../../../packages/contracts/issues/task-profile.ts';

const [flag,option,binary,...extras]=process.argv.slice(2);
assert.ok(flag==='--synthetic-write'&&option==='--binary'&&binary&&isAbsolute(binary)&&!extras.length);
const exec=promisify(execFile);
const temp=await realpath(tmpdir());
const root=await mkdtemp(join(temp,'paos-pmeth23-write-'));
const workspace=join(root,'workspace'),profile=join(root,'profile');
const document='docs/guide.md',initial='# Fixture guide\n\nSource status: synthetic fixture.\n';
const proposed=initial+'\nThe counter adds two.\n';
const before=Buffer.concat([Buffer.from([239,187,191]),Buffer.from(initial)]);
const after=Buffer.concat([Buffer.from([239,187,191]),Buffer.from(proposed)]);
const manual=Buffer.from('# User-authored fixture\r\n');
const outside=Buffer.from('Outside fixture canary\r\n');
const taskId=randomUUID(),sessionId=randomUUID();
const criteria=['The guide describes the current increment behavior','A reviewer can understand the wording'];
const hashes=(bytes:Uint8Array)=>createHash('sha256').update(bytes).digest('hex');
const checks:string[]=[];
let service:Awaited<ReturnType<typeof startLocalService>>|undefined;
let origin='',cookie='',csrf='',receipt:Record<string,unknown>={};

async function start() {
 service=await startLocalService({profileDirectory:profile,instanceId:randomUUID(),
  appCodexHome:join(root,'fixture-codex-home')},{assetRoots:[]});
 origin='http://127.0.0.1:'+service.port;
 const paired=await fetch(origin+'/bootstrap/exchange',{method:'POST',headers:{origin,'content-type':'application/json'},
  body:JSON.stringify({code:service.pairingCode})});
 assert.equal(paired.status,200);
 cookie=paired.headers.getSetCookie()[0].split(';')[0];
 csrf=(await paired.json()).csrfToken;
}

async function api(path:string,input?:unknown,expected=200,withCsrf=true) {
 const response=await fetch(origin+'/api/v1'+path,{method:input===undefined?'GET':'POST',
  headers:{origin,cookie,...(withCsrf?{'x-paos-csrf':csrf}:{}),'content-type':'application/json'},
  body:input===undefined?undefined:JSON.stringify(input)});
 const body=await response.json();
 assert.equal(response.status,expected,path+' '+(body.error?.code??''));
 return body;
}

async function checkUserBytes() {
 assert.deepEqual(await readFile(join(workspace,'AGENTS.md')),manual);
 assert.deepEqual(await readFile(join(root,'outside.txt')),outside);
}

try {
 await Promise.all([mkdir(join(workspace,'docs'),{recursive:true}),mkdir(profile),mkdir(join(root,'other'))]);
 await writeFile(join(profile,'runtime-selection.json'),JSON.stringify({binaryPath:binary,providerAuthority:false}));
 await writeFile(join(workspace,document),before);
 await writeFile(join(workspace,'counter.py'),'def increment(value):\n    return value + 2\n');
 await writeFile(join(workspace,'AGENTS.md'),manual);
 await writeFile(join(root,'outside.txt'),outside);
 const scenario={schema_version:1,task_id:taskId,intent:'Clarify the local usage guide',change_mode:'docs_only',
  changed_paths:[document],risk_level:'low',risks:[],acceptance:criteria,verification_paths:['counter.py']};
 await writeFile(join(workspace,'fixture-task.json'),JSON.stringify(scenario));
 const plan=await exec('python',['-B',resolve('plugins/product-agent-os/scripts/run_codex_runtime_runner.py'),workspace,
  '--contract','--task-context','fixture-task.json','--methodology-delivery-plan'],{timeout:30_000}).catch((error:unknown)=>{
   const result=error as {code?:number;stdout?:string};
   if(result.code!==1||!result.stdout)throw error;
   return {stdout:result.stdout};
  });
 const route=JSON.parse(plan.stdout);
 assert.notEqual(route.status,'blocked',JSON.stringify(route.errors));
 const packet=route.route_packet;
 assert.equal(packet.methodology_decision.plan.next_step.target,'counter.py');
 assert.equal(packet.methodology_delivery_plan.authority,'read_only');
 assert.ok(packet.methodology_delivery_plan.slices.length>0);
 assert.deepEqual(await readFile(join(workspace,document)),before);
 checks.push('current CLI delivery plan leaves the target unchanged');

 await start();
 const project=await api('/projects',{name:'PMETH-23 write fixture',keyPrefix:'PMWR',workspaceRoot:workspace,scan:false},201);
 const other=await api('/projects',{name:'PMETH-23 foreign fixture',keyPrefix:'PMOT',workspaceRoot:join(root,'other'),scan:false},201);
 const base='/projects/'+project.id,entity=base+'/entities/'+taskId;
 const decisionPath=base+'/tasks/'+taskId+'/methodology/decision';
 const evidencePath=base+'/tasks/'+taskId+'/methodology/evidence';
 const task={...newM2Task(project.id,taskId,scenario.intent,'local-user'),summary:'Synthetic qualification',
  technicalValue:'Observe the write route',productValue:'Review the document',acceptanceCriteria:criteria,
  files:[{relativePath:document,plannedOperation:'modify',actualOperation:null}],sessionIds:[sessionId],
  estimateSeconds:30,risks:['Synthetic fixture only']};
 const commands={expectedAuthorityEpoch:project.authorityEpoch};
 await api(base+'/commands',{...commands,idempotencyKey:'pmeth23-session',
  changes:[{expectedRevision:0,entity:{kind:'session',id:sessionId,title:'PMETH-23 synthetic worker',data:{mode:'execution'}}}]});
 await api(base+'/task-manager/commands',{...commands,action:'save',expectedRevision:0,idempotencyKey:'pmeth23-task',task});
 await api(base+'/task-manager/commands',{...commands,action:'transition',taskId,expectedRevision:1,
  idempotencyKey:'pmeth23-ready',status:'ready',reason:'Prepared the fixture'});
 const taskRevision=(await api(entity)).revision;
 await api('/projects/'+other.id+'/tasks/'+taskId+'/methodology/evidence',undefined,404);
 const catalog=await api(base+'/artifacts?kind=documents');
 const item=catalog.items.find((entry:{source:{path?:string}})=>entry.source.path===document);
 assert.ok(item);
 const method={taskId,taskRevision,criterionIds:['AC-1']};
 const request={documentId:item.id,sourceVersion:item.source.version,body:proposed,methodology:method};
 const preview=await api(base+'/artifacts/proposals/preview',request);
 assert.deepEqual(preview.methodology,method);
 assert.equal(preview.writer,'document_apply');
 const proposal=await api(base+'/artifacts/proposals',{...request,epoch:project.authorityEpoch,
  previewDigest:preview.previewDigest,idempotencyKey:'pmeth23-stage'});
 const selection={proposalId:proposal.id,proposalRevision:1};
 const review=await api(base+'/artifacts/proposals/apply-preview',selection);
 assert.equal(review.beforeHash,hashes(before));
 assert.equal(review.afterHash,hashes(after));
 assert.deepEqual(await readFile(join(workspace,document)),before);
 const approval={...selection,previewDigest:review.previewDigest,epoch:project.authorityEpoch,idempotencyKey:'pmeth23-apply'};
 await api(base+'/artifacts/proposals/apply',approval,403,false);
 await api(base+'/artifacts/proposals/apply',{...approval,previewDigest:'0'.repeat(64)},409);
 assert.deepEqual(await readFile(join(workspace,document)),before);
 const applied=await api(base+'/artifacts/proposals/apply',approval);
 assert.equal(applied.state,'applied');
 assert.equal(applied.accepted,false);
 assert.deepEqual(await api(base+'/artifacts/proposals/apply',approval),applied);
 assert.deepEqual(await readFile(join(workspace,document)),after);
 await checkUserBytes();
 checks.push('paired F13 digest approval applies once and preserves BOM and user files');

 const connection=await api('/connection',{route:'codex_app_agent'});
 assert.equal(connection.route,'codex_app_agent');
 const descriptor=JSON.parse(await readFile(service!.appAgentDescriptorPath,'utf8'));
 async function worker(action:string,input:unknown) {
  const result=await fetch(origin+'/agent/v1/'+action,{method:'POST',
   headers:{origin,authorization:'Bearer '+descriptor.capabilityToken,'content-type':'application/json'},
   body:JSON.stringify(input)});
  const body=await result.json();
  assert.equal(result.status,200,action+' '+(body.error?.code??''));
  return body;
 }
 const lease=await worker('attach',{hostIdentity:'codex_app',workerId:'pmeth23-fixture',generation:'pmeth23-synthetic'});
 const auth={workerId:lease.workerId,generation:lease.generation,leaseToken:lease.leaseToken};
 const scope={projectId:project.id,sessionId};
 const binding=await api('/runtime/bindings',{...scope,mode:'execution'});
 const run=await api('/runtime/send',{...scope,bindingId:binding.bindingId,taskId,
  clientMessageId:randomUUID(),input:'Run the fixture check after the reviewed document apply.'});
 assert.equal((await worker('claim',auth)).job.runId,run.id);
 const operation={...auth,runId:run.id,operationId:'check-guide'};
 const argv=[process.execPath,'-e',`
  const assert = require('node:assert/strict');
  const {readFileSync} = require('node:fs');
  assert.match(readFileSync('counter.py','utf8'),/return value \\+ 2/);
  assert.match(readFileSync('docs/guide.md','utf8'),/The counter adds two/);
  console.log('PMETH23_CHECKED_GUIDE');
 `];
 assert.equal((await worker('command',{...operation,criterionId:'AC-1',argv})).state,'awaiting_approval');
 assert.deepEqual((await api(evidencePath)).criteria.map((row:{technical:string})=>row.technical),['partial','missing']);
 const runtime=await api('/runtime/state?'+new URLSearchParams(scope));
 assert.equal(runtime.pendingApprovals[0].source,'paos_domain');
 await api('/runtime/approve',{...scope,bindingId:binding.bindingId,runId:run.id,
  requestId:operation.operationId,generation:auth.generation,decision:'accept'});
 let result=await worker('operation',operation);
 for(let attempt=0;attempt<150&&!['completed','recovery_required','cancelled'].includes(result.state);attempt++){
  await delay(100);
  result=await worker('operation',operation);
 }
 assert.equal(result.state,'completed');
 assert.equal(result.exitCode,0);
 assert.equal(result.stdout.trim(),'PMETH23_CHECKED_GUIDE');
 assert.equal((await api('/runtime/state?'+new URLSearchParams(scope))).capabilities.nativeSandbox,true);
 await worker('report',{...auth,runId:run.id,seq:1,idempotencyKey:'pmeth23-report',status:'completed',text:'Observed the guide check.'});
 const observed=await api(evidencePath);
 assert.deepEqual(observed.criteria.map((row:{technical:string})=>row.technical),['passed','missing']);
 assert.equal(observed.criteria[0].receipt.route,'native_command_broker');
 assert.equal(observed.criteria[0].receipt.operationId,operation.operationId);
 assert.equal(observed.humanAcceptance,'not_observed');
 assert.equal(observed.releaseAcceptance,'not_evaluated');
 checks.push('real native process turns only AC-1 into observed evidence');

 const blankDecision=await api(decisionPath);
 const saved=await api(decisionPath,{expectedRevision:blankDecision.revision,taskRevision:observed.taskRevision,
  scopeDigest:blankDecision.scopeDigest,idempotencyKey:'pmeth23-decision',disposition:'accepted_gap',
  criterionId:'AC-2',reason:'Synthetic reviewer accepts the outstanding wording check'});
 assert.equal(saved.status,'current');
 assert.deepEqual((await api(evidencePath)).criteria.map((row:{technical:string})=>row.technical),['passed','missing']);
 await service!.quit();
 service=undefined;
 await start();
 assert.deepEqual(await api(decisionPath),saved);
 assert.deepEqual((await api(evidencePath)).criteria[0].receipt,observed.criteria[0].receipt);
 const currentTask=await api(entity);
 await api(base+'/task-manager/commands',{...commands,action:'save',expectedRevision:currentTask.revision,
  idempotencyKey:'pmeth23-change-ac',task:{...currentTask.data,acceptanceCriteria:['New guide requirement',criteria[1]]}});
 const stale=await api(decisionPath);
 assert.equal(stale.status,'stale');
 assert.deepEqual(stale.history,saved.history);
 assert.deepEqual((await api(evidencePath)).criteria.map((row:{technical:string})=>row.technical),['stale','missing']);
 checks.push('decision and receipt survive service restart and become stale after AC revision');

 const currentProposal=await api(base+'/artifacts/'+proposal.id);
 const proposalRevision=Number(currentProposal.item.source.version.slice('entity:'.length));
 assert.ok(Number.isSafeInteger(proposalRevision)&&proposalRevision>selection.proposalRevision);
 const rollbackSelection={proposalId:proposal.id,proposalRevision};
 const rollbackPreview=await api(base+'/artifacts/proposals/rollback-preview',rollbackSelection);
 const rolled=await api(base+'/artifacts/proposals/rollback',{...rollbackSelection,previewDigest:rollbackPreview.previewDigest,
  epoch:project.authorityEpoch,idempotencyKey:'pmeth23-rollback'});
 assert.equal(rolled.state,'rolled_back');
 assert.deepEqual(await readFile(join(workspace,document)),before);
 await checkUserBytes();
 checks.push('reviewed native rollback restores exact bytes without modifying authored files');
 receipt={writer:preview.writer,nativeRoute:observed.criteria[0].receipt.route,
  sourceRevision:observed.sourceRevision,taskSpecRevision:observed.taskSpecRevision,
  inputDigest:observed.criteria[0].receipt.inputDigest,beforeHash:hashes(before),afterHash:hashes(after)};
} finally {
 await service?.quit();
 assert.equal(dirname(await realpath(root)),temp);
 await rm(root,{recursive:true});
 await assert.rejects(access(root),{code:'ENOENT'});
}
console.log(JSON.stringify({status:'passed',checks,fixtureCleaned:true,syntheticWorker:true,providerCalls:0,...receipt},null,2));
