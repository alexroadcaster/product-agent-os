import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createHttpApi} from '../../apps/web/src/api/client.ts';
import {draftTask,selectTasks,defaultView,durationText,readView,safeExternalUrl,hierarchyStats} from '../../apps/web/src/features/tasks/model.ts';
import {isExecutionTarget} from '../../apps/web/src/api/session-target.ts';

test('Task Manager commands share paired CSRF and authority without exposing data in URLs',async()=>{
  const calls:{url:string;options?:RequestInit}[]=[];
  const api=createHttpApi((async(url:string,options?:RequestInit)=>{
    calls.push({url,options});
    return Response.json(url.endsWith('/session')?{csrfToken:'synthetic-csrf'}:url.endsWith('/projects')?{items:[{id:'p/one',authorityEpoch:7}]}:{tasks:[],coverage:'complete'});
  }) as typeof fetch);
  await assert.rejects(()=>api.taskManagerCommand('p/one',{action:'transition',expectedRevision:3,status:'done'},'replay-safe'));
  await api.pair();await api.projects();await api.taskManager('p/one');
  await api.taskManagerCommand('p/one',{action:'transition',expectedRevision:3,status:'done',reason:'synthetic evidence'},'replay-safe');
  assert.equal(calls.at(-1)?.url,'/api/v1/projects/p%2Fone/task-manager/commands');
  assert.deepEqual(JSON.parse(String(calls.at(-1)?.options?.body)),{action:'transition',expectedRevision:3,status:'done',reason:'synthetic evidence',expectedAuthorityEpoch:7,idempotencyKey:'replay-safe'});
  assert.equal((calls.at(-1)?.options?.headers as Record<string,string>)['X-PAOS-CSRF'],'synthetic-csrf');
  assert.equal(calls.at(-1)?.options?.credentials,'same-origin');
  assert.equal(api.attachmentUrl('p/one','task/2','a?three'),'/api/v1/projects/p%2Fone/tasks/task%2F2/attachments/a%3Fthree');
});

test('hierarchy totals count each descendant once and keep parent effort separate',()=>{
  const task=(id:string,parentId:string|null,estimateSeconds:number|null,status='backlog')=>({id,projectId:'p',kind:'task' as const,revision:1,status,data:{...draftTask('p',id),parentId,estimateSeconds,status}});
  const values=[task('epic',null,200),task('standard','epic',100,'done'),task('sub','standard',40),task('other',null,999)];
  assert.deepEqual(hierarchyStats(values,'epic'),{descendants:2,done:1,cancelled:0,estimateSeconds:140,unknownEstimates:0,actualSeconds:null,ownEstimateSeconds:200});
});

test('attachment unknown-outcome retry preserves bytes, original revision, key and authenticated envelope',async()=>{
 const bodies:unknown[]=[],api=createHttpApi((async(url:string,options?:RequestInit)=>{
  if(url.endsWith('/session'))return Response.json({csrfToken:'synthetic'});
  if(url.endsWith('/projects'))return Response.json({items:[{id:'p',authorityEpoch:4}]});
  bodies.push(JSON.parse(String(options?.body)));if(bodies.length===1)throw new TypeError('synthetic lost response');return Response.json({receipt:'same-command'});
 }) as typeof fetch);
 await api.pair();await api.projects();const payload={filename:'proof.txt',mediaType:'text/plain',base64:'cHJvb2Y='};
 await assert.rejects(()=>api.uploadAttachment('p','t',7,payload,'same-upload'));
 await api.uploadAttachment('p','t',7,payload,'same-upload');
 assert.deepEqual(bodies[0],bodies[1]);assert.deepEqual(bodies[1],{...payload,expectedRevision:7,expectedAuthorityEpoch:4,idempotencyKey:'same-upload'});
});

test('pending-link Stop is server-derived and sends no fabricated run context',async()=>{
 let url='',payload:unknown;const api=createHttpApi((async(path:string,options?:RequestInit)=>{url=path;payload=options?.body?JSON.parse(String(options.body)):undefined;return Response.json(path.endsWith('/session')?{csrfToken:'synthetic'}:{stopRequested:true});}) as typeof fetch);
 await api.pair();await api.stopPendingLink('p/one','link/two');
 assert.equal(url,'/api/v1/projects/p%2Fone/task-manager/links/link%2Ftwo/stop');assert.deepEqual(payload,{});
});

test('Task Manager preserves separate release filters, hierarchy, draft semantics and execution eligibility',()=>{
  const first=draftTask('p','first');first.title='Bug';first.type='bug';first.affectsVersions=['v12'];first.fixVersions=['v13'];first.parentId='epic';
  first.summary='Reproduce';first.technicalValue='Correct result';first.productValue='Useful';first.acceptanceCriteria=['Checked'];first.files=[{relativePath:'src/a.ts',plannedOperation:'modify',actualOperation:null}];first.risks=['none'];first.estimateSeconds=60;first.status='ready';
  const record={id:'first',projectId:'p',kind:'task' as const,revision:1,title:'Bug',status:'ready',data:first};
  const second={...record,id:'second',title:'Story',data:{...first,id:'second',type:'user_story',affectsVersions:['v13'],fixVersions:[],parentId:null}};
  assert.deepEqual(selectTasks([record,second],{...defaultView,fixVersion:'v13'},[]).map(t=>t.id),['first']);
  assert.deepEqual(selectTasks([record,second],{...defaultView,affectsVersion:'v13'},[]).map(t=>t.id),['second']);
  assert.equal(selectTasks([record,second],{...defaultView,parent:'epic'},[]).length,1);
  assert.equal(isExecutionTarget(record),true);
  assert.equal(isExecutionTarget({...record,data:{...first,type:'epic'}}),false);
  assert.equal(draftTask('p','new').actual.durationSeconds,null);
  assert.equal(durationText(90061),'25:01:01');
  assert.equal(durationText(null),'—');
  assert.equal(readView({type:'bug',sort:'invented'}).type,'bug');
  assert.equal(readView({type:'bug',sort:'invented'}).sort,'rank');
  assert.equal(safeExternalUrl('javascript:alert(1)'),null);
  assert.equal(safeExternalUrl('https://user:secret@example.test'),null);
  assert.equal(safeExternalUrl('https://example.test/proof'),'https://example.test/proof');
});
