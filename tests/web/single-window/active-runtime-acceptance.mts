import {mkdtemp,mkdir,readFile,writeFile,rm,readdir} from 'node:fs/promises';
import {join,isAbsolute} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash,randomUUID} from 'node:crypto';
import {startLocalService} from '../../../apps/local-service/src/main.mts';
import {createLiveGateway} from '../../../apps/local-service/src/runtime/live-gateway.mts';
import type {RuntimeRpc} from '../../../apps/local-service/src/runtime/codex/stdio-rpc.ts';
import {fixtureTask,runtimeTaskId} from '../runtime-adapter-time.fixture.mts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';
import {uiLabel} from '../../../apps/web/src/locales/messages.ts';

/** Explicit synthetic RPC selection only. This is not native Codex or provider qualification. */
function fixtureTransport(generation:string,history:Map<string,any>,calls:any[],responses:any[]):RuntimeRpc&{emit:(event:any)=>void;eof:()=>void} {
 const listeners=new Set<(event:any)=>void>();const closed=new Set<(reason:string)=>void>();let stopped=false;
 const rpc={generation,notify(){},snapshot:()=>({generation,status:stopped?'closed' as const:'open' as const,pending:0,stderrBytes:0}),
  subscribe(next:any){listeners.add(next);return()=>listeners.delete(next);},onClosed(next:any){closed.add(next);return()=>closed.delete(next);},
  respond(id:any,result:any){responses.push({generation,id,result});},respondError(id:any){responses.push({generation,id,error:true});},
  async close(){if(!stopped){stopped=true;for(const next of closed)next('fixture_closed');}},
  emit(event:any){for(const next of listeners)next(event);},eof(){stopped=true;for(const next of closed)next('runtime_eof');},
  async request(method:string,params:any={}) {
   // Never retain login input or key-shaped values in the evidence ledger.
   calls.push({generation,method,...(method==='thread/start'?{permissions:params.permissions,approvalPolicy:params.approvalPolicy}:{}),
    ...(method==='turn/start'?{threadId:params.threadId,clientMessageId:params.clientUserMessageId}:{} )});
   if(method==='initialize')return {};
   if(method==='account/login/start')return {type:'apiKey'};
   if(method==='account/read')return {account:{type:'apiKey'},requiresOpenaiAuth:true};
   if(method==='account/logout')return {};
   if(method==='thread/start') {
    const id=`fixture-thread-${history.size+1}`;history.set(id,{id,turns:[]});
    return {thread:{id},cwd:params.cwd,runtimeWorkspaceRoots:[params.cwd],activePermissionProfile:{id:params.permissions},approvalPolicy:params.approvalPolicy,
     sandbox:{type:params.permissions==='paos_execution'?'workspaceWrite':'readOnly',networkAccess:false,writableRoots:[],excludeSlashTmp:true,excludeTmpdirEnvVar:true}};
   }
   if(method==='turn/start') {const thread=history.get(params.threadId);const turn={id:`fixture-turn-${thread.turns.length+1}`,status:'inProgress'};thread.turns.push(turn);return {turn};}
   if(method==='turn/interrupt')return {};
   if(method==='thread/read')return {thread:history.get(params.threadId)};
   throw new Error('FIXTURE_METHOD_NOT_ALLOWLISTED');
  }};
 return rpc as ReturnType<typeof fixtureTransport>;
}

async function main(argv:string[]) {
 if(argv.length!==5||argv[0]!=='--synthetic-browser')throw new Error('EXPLICIT_BROWSER_FIXTURE_REQUIRED');
 const args=Object.fromEntries([argv.slice(1,3),argv.slice(3,5)]);
 if(!args['--playwright-core']||!args['--chromium']||!Object.values(args).every(isAbsolute))throw new Error('EXPLICIT_BROWSER_PATHS_REQUIRED');
 const {chromium}=await import(pathToFileURL(join(args['--playwright-core'],'index.mjs')).href);
 const scratch=fileURLToPath(new URL('../../../.tmp/paos-m1/',import.meta.url));await mkdir(scratch,{recursive:true});
 const output=await mkdtemp(join(scratch,'active-runtime-evidence-'));const fixture=await mkdtemp(join(scratch,'active-runtime-fixture-'));
 const profile=join(fixture,'profile'),workspace=join(fixture,'workspace'),browserHome=join(fixture,'browser');
 await Promise.all([mkdir(profile),mkdir(workspace),mkdir(browserHome)]);
 await writeFile(join(workspace,'synthetic.txt'),'Synthetic fixture scope only.\n');
 const report:any={startedAt:new Date().toISOString(),fixtureSelected:true,actualCodex:false,externalProvider:false,realKeys:false,osStoreUsed:false,
  nativeQualificationClaim:false,fullM1AcceptanceClaim:false,nodeVersion:process.version,checks:[],screenshots:[],sourceHashes:{},blockedRequests:[],pageErrorCount:0};
 const check=(name:string,passed:boolean)=>{report.checks.push({name,passed});if(!passed)throw new Error(name);};
 let service:Awaited<ReturnType<typeof startLocalService>>|undefined,context:any,page:any,csrf='',timer:ReturnType<typeof setTimeout>|undefined;
 let activeStep='setup';const calls:any[]=[],responses:any[]=[],history=new Map<string,any>();let rpc:ReturnType<typeof fixtureTransport>;
 let credentialStoreCalls=0;
 try {
  const sourcePaths=['tests/web/single-window/active-runtime-acceptance.mts','apps/local-service/src/main.mts','apps/local-service/src/http/application.mts',
   'apps/local-service/src/runtime/live-gateway.mts','apps/local-service/src/runtime/codex/coordinator.ts','packages/contracts/runtime/events.ts','apps/local-service/src/runtime/storage-ports.mts','apps/web/dist/index.html'];
  for(const name of await readdir(fileURLToPath(new URL('../../../apps/web/dist/assets/',import.meta.url))))sourcePaths.push('apps/web/dist/assets/'+name);
  for(const path of sourcePaths)report.sourceHashes[path]=createHash('sha256').update(await readFile(fileURLToPath(new URL('../../../'+path,import.meta.url)))).digest('hex');
  service=await startLocalService({profileDirectory:profile,instanceId:randomUUID()},{createGateway:options=>createLiveGateway({...options,
   isEnabled:()=>true,providerAuthority:()=>true,
   credentialStore:{read:async()=>{credentialStoreCalls++;throw new Error('FIXTURE_STORE_FORBIDDEN');},write:async()=>{credentialStoreCalls++;throw new Error('FIXTURE_STORE_FORBIDDEN');},delete:async()=>{credentialStoreCalls++;throw new Error('FIXTURE_STORE_FORBIDDEN');}},
   rpcFactory:async()=>{rpc=fixtureTransport(`fixture-generation-${calls.filter(call=>call.method==='initialize').length+1}`,history,calls,responses);return rpc;}})});
  const origin=`http://127.0.0.1:${service.port}`;report.origin=origin;
  context=await chromium.launchPersistentContext(browserHome,{headless:true,chromiumSandbox:true,serviceWorkers:'block',viewport:{width:1440,height:1000},locale:'ru-RU',executablePath:args['--chromium'],timeout:20000,
   env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:browserHome,HOME:browserHome,APPDATA:browserHome,LOCALAPPDATA:browserHome,TEMP:browserHome,TMP:browserHome}});
  timer=setTimeout(()=>void context?.close(),180_000);
  await context.route('**/*',async(route:any)=>{const request=route.request(),url=new URL(request.url());const method=request.method();
   const allowed=url.origin===origin&&!url.username&&!url.password&&(
    method==='GET'&&(url.pathname==='/'||url.pathname==='/health'||/^\/assets\/[A-Za-z0-9_.-]+$/.test(url.pathname)||/^\/api\/v1\/(session|projects|preferences|connection|runtime\/state)$/.test(url.pathname)||/^\/api\/v1\/projects\/[^/]+\/(entities(?:\/[^/]+)?|history|catalogs|sources(?:\/[^/]+)?)$/.test(url.pathname))
    ||method==='POST'&&(/^\/api\/v1\/(bootstrap\/exchange|projects|connection|runtime\/(bindings|send|interrupt|approve|reconcile))$/.test(url.pathname)||/^\/api\/v1\/projects\/[^/]+\/commands$/.test(url.pathname)));
   if(allowed)await route.continue();else{report.blockedRequests.push({method,path:url.pathname});await route.abort();}});
  page=context.pages()[0]??await context.newPage();page.setDefaultTimeout(12000);page.on('pageerror',()=>{report.pageErrorCount++;});
  await page.goto(origin);await page.getByLabel(appLabel('ru','code'),{exact:true}).fill(service.pairingCode);
  const exchange=page.waitForResponse((response:any)=>response.url()===origin+'/api/v1/bootstrap/exchange'&&response.status()===200);
  await page.getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();csrf=(await(await exchange).json()).csrfToken;
  async function api(path:string,payload?:any){return page.evaluate(async({path,payload,csrf}:any)=>{const response=await fetch('/api/v1'+path,{method:payload===undefined?'GET':'POST',headers:{'content-type':'application/json','x-paos-csrf':csrf},...(payload===undefined?{}:{body:JSON.stringify(payload)})});return {status:response.status,body:await response.json()};},{path,payload,csrf});}
  async function nav(section:string){await page.locator('nav').getByRole('button',{name:uiLabel('ru',`nav.${section}` as any),exact:true}).click();}
  async function until(name:string,predicate:()=>Promise<boolean>){for(let i=0;i<100;i++){if(await predicate()){check(name,true);return;}await new Promise(resolve=>setTimeout(resolve,100));}check(name,false);}
  async function activeLayout(scene:string,control:any) {
   for(const width of [320,1440])for(const colorScheme of ['light','dark']) {
    await page.setViewportSize({width,height:1000});await page.emulateMedia({colorScheme});
    await page.waitForFunction((theme:string)=>document.documentElement.dataset.theme===theme,colorScheme);
    await control.scrollIntoViewIfNeeded();
    check(`${scene}_${width}_${colorScheme}_no_horizontal_overflow`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    const box=await control.boundingBox();check(`${scene}_${width}_${colorScheme}_control_reachable`,!!box&&box.x>=0&&box.x+box.width<=width+1&&box.y>=0&&box.y+box.height<=1001);
    if(width===320&&colorScheme==='dark'){const name=`${scene}-320-dark.png`;await page.screenshot({path:join(output,name),mask:[page.locator('input')]});report.screenshots.push(name);}
   }
   await page.setViewportSize({width:1440,height:1000});await page.emulateMedia({colorScheme:'light'});
  }
  const projectResult=await api('/projects',{name:'Active synthetic fixture',keyPrefix:'TEST',workspaceRoot:workspace});check('project_registered',projectResult.status===201);const project=projectResult.body;
  const sessionId=randomUUID(),task={...fixtureTask(project.id),files:[{relativePath:'synthetic.txt',plannedOperation:'modify',actualOperation:null}],sessionIds:[sessionId]};
  const seeded=await api(`/projects/${project.id}/commands`,{expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:'active-fixture-seed',changes:[
   {expectedRevision:0,entity:{id:sessionId,kind:'session',title:'Active fixture session',status:'idle',data:{mode:'execution',taskId:runtimeTaskId}}},
   {expectedRevision:0,entity:{id:runtimeTaskId,kind:'task',data:task}}]});check('task_session_seeded',seeded.status===200);
  await page.reload();await page.locator('.navigation select:enabled').waitFor();await page.locator('.navigation select').selectOption(project.id);
  async function connect(){await nav('settings');await page.getByLabel(appLabel('ru','connectionRoute'),{exact:true}).selectOption('local_api_byok');await page.locator('input[name=connectionId]').fill('synthetic');await page.locator('input[name=apiKey]').fill('fixture-only-canary');
   const response=page.waitForResponse((response:any)=>response.url()===origin+'/api/v1/connection'&&response.request().method()==='POST');
   await page.getByRole('button',{name:appLabel('ru','login'),exact:true}).click();check('fixture_connection_ack',(await response).status()===200);}
  await connect();await nav('sessions');await page.locator('.session-list .records button').filter({hasText:'Active fixture session'}).click();await page.locator('.composer').waitFor();
  const state=async()=>(await api(`/runtime/state?projectId=${project.id}&sessionId=${sessionId}`)).body;
  async function bind(mode:string){await page.locator('.composer select').first().selectOption(mode);await page.locator('.composer').getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();await until('binding_'+mode,async()=>{const value=await state();return value.mode===mode&&!!value.bindingId;});}
  async function send(text:string){await page.locator('.composer textarea').fill(text);await until('send_ready',()=>page.getByRole('button',{name:uiLabel('ru','action.send'),exact:true}).isEnabled());
   await page.getByRole('button',{name:uiLabel('ru','action.send'),exact:true}).click();await until('running_receipt',async()=>(await state()).state==='running');
   const turnStart=calls.filter(call=>call.method==='turn/start').at(-1);const thread=history.get(turnStart.threadId);return {threadId:thread.id,turnId:thread.turns.at(-1).id};}
  await bind('execution');
  await page.locator('.composer select').nth(1).selectOption(runtimeTaskId);
  const attach=page.getByRole('button',{name:appLabel('ru','attachTask'),exact:true});if(await attach.isEnabled())await attach.click();
  activeStep='execution';const first=await send('Synthetic bounded execution');
  rpc!.emit({method:'item/started',params:{...first,item:{id:'visible',type:'agentMessage',phase:'final_answer'}}});
  rpc!.emit({method:'item/agentMessage/delta',params:{...first,itemId:'visible',delta:'Synthetic streaming answer'}});
  rpc!.emit({method:'item/reasoning/textDelta',params:{...first,itemId:'hidden',delta:'HIDDEN_FIXTURE_REASONING'}});
  await until('visible_stream_rendered',async()=>(await page.locator('.transcript').innerText()).includes('Synthetic streaming answer'));
  rpc!.emit({id:71,method:'item/commandExecution/requestApproval',params:{...first,itemId:'check',cwd:workspace,command:'synthetic-check',reason:'Synthetic bounded command'}});
  await until('approval_pending',async()=>(await state()).pendingApprovals?.[0]?.state==='pending');
  const tokenCounts={inputTokens:10,outputTokens:2,cachedInputTokens:0,reasoningOutputTokens:0,totalTokens:12};
  for(const method of ['thread/status/changed','thread/tokenUsage/updated','turn/plan/updated','turn/diff/updated','thread/name/updated','thread/readState/changed']) {
   rpc!.emit({method,params:{...first,status:{type:'active',activeFlags:['waitingOnApproval']},tokenUsage:{last:tokenCounts,total:tokenCounts},plan:[],diff:'',threadName:'Synthetic fixture',readState:{revision:'fixture-read-1',firstUnread:null}}});
  }
  // Allow the informational reducer microtasks to drain before observing state over real HTTP.
  await new Promise(resolve=>setTimeout(resolve,0));
  await until('pending_approval_survives_informational_events',async()=>{const current=await state();return current.state==='awaiting_approval'&&current.pendingApprovals?.[0]?.state==='pending';});
  await page.getByRole('button',{name:appLabel('ru','approve'),exact:true}).click();
  await until('approval_response_sent',async()=>(await state()).pendingApprovals?.[0]?.state==='response_sent');
  check('approval_scoped_response',responses.some(item=>item.id===71&&item.result?.decision==='accept'));
  await activeLayout('approval-response-sent',page.getByRole('button',{name:appLabel('ru','approve'),exact:true}));
  await page.screenshot({path:join(output,'approval-response-sent.png')});report.screenshots.push('approval-response-sent.png');
  rpc!.emit({method:'serverRequest/resolved',params:{threadId:first.threadId,requestId:71}});
  await until('approval_cleared',async()=>(await state()).pendingApprovals.length===0);
  rpc!.emit({method:'item/completed',params:{...first,item:{id:'check',type:'commandExecution',status:'completed',exitCode:1}}});
  rpc!.emit({method:'item/completed',params:{...first,item:{id:'file',type:'fileChange',status:'completed',changes:[{path:'synthetic.txt',kind:{type:'add'},diff:'+synthetic'}]}}});
  await until('check_and_diff_projected',async()=>{const value=await state();return value.checks?.some((item:any)=>item.outcome==='exit_1')&&value.fileChanges?.length>0;});
  await until('failed_check_rendered',async()=>(await page.locator('body').innerText()).includes('exit_1'));
  await page.getByRole('button',{name:appLabel('ru','changes'),exact:true}).click();
  await until('file_diff_rendered',async()=>(await page.locator('body').innerText()).includes('synthetic.txt'));
  await page.screenshot({path:join(output,'runtime-reported-diff-check.png')});report.screenshots.push('runtime-reported-diff-check.png');
  await page.getByRole('button',{name:appLabel('ru','chat'),exact:true}).click();
  rpc!.emit({method:'item/completed',params:{...first,item:{id:'visible',type:'agentMessage',phase:'final_answer',text:'Synthetic completed answer'}}});
  history.get(first.threadId).turns.at(-1).status='completed';rpc!.emit({method:'turn/completed',params:{threadId:first.threadId,turn:{id:first.turnId,status:'completed'}}});
  await until('execution_terminal_released',async()=>!(await state()).runId);
  await until('completed_summary_rendered',()=>page.locator('.inspector section').first().getByText('completed',{exact:true}).isVisible());
  await until('final_message_persisted_and_rendered',async()=>(await page.locator('.transcript').innerText()).includes('Synthetic completed answer'));
  const storedTask=(await api(`/projects/${project.id}/entities/${runtimeTaskId}`)).body;check('failed_check_does_not_close_task',storedTask.data.status!=='done');
  check('hidden_reasoning_absent_ui',!(await page.locator('body').innerText()).includes('HIDDEN_FIXTURE_REASONING'));
  const messages=(await api(`/projects/${project.id}/entities?kind=message`)).body.items;check('hidden_reasoning_absent_storage',!JSON.stringify(messages).includes('HIDDEN_FIXTURE_REASONING'));
  await page.screenshot({path:join(output,'completed-result.png')});report.screenshots.push('completed-result.png');
  activeStep='stop';await bind('discussion');const second=await send('Synthetic stop request');
  await page.getByRole('button',{name:uiLabel('ru','action.stopRun'),exact:true}).click();
  await until('interrupt_rpc_ack',async()=>calls.some(call=>call.method==='turn/interrupt'));
  history.get(second.threadId).turns.at(-1).status='interrupted';rpc!.emit({method:'turn/completed',params:{threadId:second.threadId,turn:{id:second.turnId,status:'interrupted'}}});
  await until('interrupted_lease_released',async()=>!(await state()).runId);
  await until('interrupted_summary_rendered',()=>page.locator('.inspector section').first().getByText('interrupted',{exact:true}).isVisible());
  activeStep='recovery';await bind('planning');const third=await send('Synthetic recovery request');const dispatchCount=calls.filter(call=>call.method==='turn/start').length;
  rpc!.eof();await until('eof_requires_recovery',async()=>(await state()).state==='recovery_required');
  await activeLayout('recovery-required',page.getByRole('button',{name:appLabel('ru','recover'),exact:true}));
  await connect();await nav('sessions');await page.locator('.session-list .records button').filter({hasText:'Active fixture session'}).click();
  history.get(third.threadId).turns.at(-1).status='completed';
  await page.getByRole('button',{name:appLabel('ru','recover'),exact:true}).click();await until('reconciled_exact_turn',async()=>!(await state()).runId);
  check('reconnect_never_replays_turn',calls.filter(call=>call.method==='turn/start').length===dispatchCount);
  check('fresh_generation_created',calls.filter(call=>call.method==='initialize').length===2);
  const policies=calls.filter(call=>call.method==='thread/start');check('mode_policies_explicit',policies.length===3&&policies[0].permissions==='paos_execution'&&policies.slice(1).every(call=>call.permissions==='paos_readonly'&&call.approvalPolicy==='never'));
  check('credential_store_never_called',credentialStoreCalls===0);check('route_allowlist_clean',report.blockedRequests.length===0);check('no_page_errors',report.pageErrorCount===0);
  report.status='passed_local_active_runtime_fixture';report.rpcMethods=calls.map(({generation,method,permissions,approvalPolicy})=>({generation,method,permissions,approvalPolicy}));
 }catch(error){report.status='failed';report.failedStep=activeStep;report.error=(error as Error).message.replaceAll('fixture-only-canary','[fixture-redacted]').slice(0,400);process.exitCode=1;
  try{if(page&&!page.isClosed()){await page.screenshot({path:join(output,'failed-state.png'),mask:[page.locator('input')]});report.screenshots.push('failed-state.png');
   report.failureUi=(await page.locator('body').innerText()).replaceAll('fixture-only-canary','[fixture-redacted]').slice(0,12000);}}catch{}
 }
 finally {
  if(timer)clearTimeout(timer);try{await context?.close();}catch{report.browserCleanupFailed=true;report.status='failed';process.exitCode=1;}
  try{await service?.quit();report.serviceClosed=true;}catch{report.serviceCleanupFailed=true;report.status='failed';process.exitCode=1;}
  // Retain only this synthetic fixture when lifecycle closure is unknown; deletion must not hide a live worker.
  if(report.serviceClosed)try{await rm(fixture,{recursive:true,force:true});report.fixtureCleaned=true;}catch{report.fixtureCleaned=false;report.status='failed';process.exitCode=1;}
  else {report.fixtureCleaned=false;report.fixtureRetained=fixture;}
  report.finishedAt=new Date().toISOString();await writeFile(join(output,'active-runtime-result.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({status:report.status,checks:report.checks.length,failedStep:report.failedStep,error:report.error,report:join(output,'active-runtime-result.json'),fixtureCleaned:report.fixtureCleaned}));
 }
}
if(process.argv[1]&&fileURLToPath(import.meta.url)===fileURLToPath(pathToFileURL(process.argv[1])))await main(process.argv.slice(2));
