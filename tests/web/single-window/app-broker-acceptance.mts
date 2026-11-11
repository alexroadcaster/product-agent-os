import {mkdtemp,mkdir,readFile,writeFile,rm} from 'node:fs/promises';
import {join,resolve,isAbsolute} from 'node:path';
import {pathToFileURL} from 'node:url';
import {randomUUID} from 'node:crypto';
import {startLocalService} from '../../../apps/local-service/src/main.mts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';
import {uiLabel} from '../../../apps/web/src/locales/messages.ts';
import {fixtureTask} from '../runtime-adapter-time.fixture.mts';

/** Explicit real App worker acceptance. The host must attach an actual agent; no fixture RPC or provider SDK. */
async function main(){
 const args=Object.fromEntries(process.argv.slice(2).reduce<string[][]>((rows,item,index,array)=>{if(item.startsWith('--'))rows.push([item,array[index+1]]);return rows;},[]));
 if(!process.argv.includes('--app-broker-browser')||!['--binary','--playwright-core','--chromium'].every(key=>isAbsolute(args[key]??'')))throw new Error('EXPLICIT_APP_BROKER_BROWSER_REQUIRED');
 const work=resolve('.tmp/paos-m1');await mkdir(work,{recursive:true});const root=await mkdtemp(join(work,'app-broker-live-'));
 const output=await mkdtemp(join(work,'app-broker-evidence-'));const coordination=join(work,'app-broker-live-coordination.json');
 const workspace=join(root,'workspace'),profileDirectory=join(root,'profile'),browserHome=join(root,'browser');await mkdir(workspace);await mkdir(browserHome);
 const report:any={schemaVersion:'paos_app_broker_acceptance_v1',actualAppAgent:false,actualAppHostEndpoint:false,actualNativeCommandBroker:false,brokerModelTurns:0,brokerCredentialOperations:0,apiKey:false,sandboxScope:'paos_mediated_commands',checks:[],screenshots:[],pageErrorCount:0,blockedExternalRequests:0,startedAt:new Date().toISOString()};
 const check=(name:string,passed:boolean)=>{report.checks.push({name,passed});if(!passed)throw new Error(name);};
 let service:Awaited<ReturnType<typeof startLocalService>>|undefined,context:any;
 const note=async(value:unknown)=>writeFile(coordination,JSON.stringify(value,null,2));
 try{
  await mkdir(profileDirectory);await writeFile(join(profileDirectory,'runtime-selection.json'),JSON.stringify({binaryPath:args['--binary'],providerAuthority:false,purpose:'sandbox_commands_only'}));
  const outsideCanary=join(root,'outside.txt');await writeFile(outsideCanary,'synthetic-outside-canary');
  service=await startLocalService({profileDirectory,instanceId:randomUUID()});let origin=`http://127.0.0.1:${service.port}`;
  const {chromium}=await import(pathToFileURL(join(args['--playwright-core'],'index.mjs')).href);
  context=await chromium.launchPersistentContext(browserHome,{headless:true,chromiumSandbox:true,serviceWorkers:'block',viewport:{width:1440,height:1000},locale:'ru-RU',executablePath:args['--chromium'],timeout:20000,
   env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:browserHome,HOME:browserHome,APPDATA:browserHome,LOCALAPPDATA:browserHome,TEMP:browserHome,TMP:browserHome}});
  await context.route('**/*',async(route:any)=>{if(new URL(route.request().url()).origin===origin)await route.continue();else{report.blockedExternalRequests++;await route.abort();}});
  const page=context.pages()[0]??await context.newPage();page.setDefaultTimeout(15000);page.on('pageerror',()=>report.pageErrorCount++);
  await page.goto(origin);await page.getByLabel(appLabel('ru','code'),{exact:true}).fill(service.pairingCode);
  const exchange=page.waitForResponse((response:any)=>response.url()===origin+'/api/v1/bootstrap/exchange'&&response.status()===200);
  await page.getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();let csrf=(await(await exchange).json()).csrfToken;
  async function api(path:string,input?:unknown){return page.evaluate(async({path,input,csrf}:any)=>{const response=await fetch('/api/v1'+path,{method:input===undefined?'GET':'POST',headers:{'content-type':'application/json','x-paos-csrf':csrf},...(input===undefined?{}:{body:JSON.stringify(input)})});return {status:response.status,body:await response.json()};},{path,input,csrf});}
  async function nav(section:string){await page.locator('nav').getByRole('button',{name:uiLabel('ru',`nav.${section}` as any),exact:true}).click();}
  async function until(name:string,predicate:()=>Promise<boolean>,timeout=15000){const deadline=Date.now()+timeout;while(Date.now()<deadline){if(await predicate()){check(name,true);return;}await new Promise(resolve=>setTimeout(resolve,250));}check(name,false);}
  const created=await api('/projects',{name:'Codex App native broker acceptance',workspaceRoot:workspace,keyPrefix:'TEST'});check('project_registered',created.status===201);const project=created.body,sessionId=randomUUID();
  check('session_saved',(await api(`/projects/${project.id}/commands`,{expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:'app-acceptance-session',changes:[{expectedRevision:0,entity:{id:sessionId,kind:'session',title:'Actual Codex App agent',data:{mode:'discussion'}}}]})).status===200);
  await page.reload();await page.locator('.navigation select:enabled').waitFor();await page.locator('.navigation select').selectOption(project.id);await nav('settings');
  check('app_route_default',await page.getByLabel(appLabel('ru','connectionRoute'),{exact:true}).inputValue()==='codex_app_agent');
  check('no_api_key_input',await page.locator('input[name=apiKey]').count()===0);
  const connectionResponse=page.waitForResponse((response:any)=>response.url()===origin+'/api/v1/connection'&&response.request().method()==='POST');
  await page.locator('.panel').filter({has:page.getByLabel(appLabel('ru','connectionRoute'),{exact:true})}).getByRole('button',{name:appLabel('ru','openAppAgentChannel'),exact:true}).click();
  check('app_route_connected_waiting',(await connectionResponse).status()===200);
  const shared={descriptorPath:service.appAgentDescriptorPath,workerId:'broker-app-worker',output,scope:{projectId:project.id,sessionId},nodeBinary:process.execPath,outsideCanary,expectedJobs:6,evidence:'actual Codex App model worker required; all target writes MUST use PAOS command broker, never host filesystem tools'};
  await note({...shared,stage:'waiting_for_agent'});console.log(JSON.stringify({stage:'waiting_for_agent',coordination,output}));
  await until('actual_agent_attached',async()=>(await api('/connection')).body.verified===true,240000);
  const state=async()=>(await api(`/runtime/state?${new URLSearchParams(shared.scope)}`)).body;
  const cases=[{name:'discussion',mode:'discussion',files:['discussion-forbidden.txt']},{name:'planning',mode:'planning',files:['planning-forbidden.txt']},{name:'decline',mode:'execution',files:['declined.txt']},{name:'write',mode:'execution',files:['accepted.txt']},{name:'stop',mode:'execution',files:['started.txt','late.txt']},{name:'restart',mode:'execution',files:['stale.txt']}];
  const seeded=cases.filter(item=>item.mode==='execution').map((item,index)=>{const id=randomUUID();return {...item,taskId:id,profile:{...fixtureTask(project.id),id,key:`TEST-${index+1}`,title:`Native App ${item.name}`,files:item.files.map(relativePath=>({relativePath,plannedOperation:'create',actualOperation:null})),acceptanceCriteria:[`Synthetic ${item.name} criterion`],sessionIds:[sessionId]}};});
  check('execution_tasks_saved',(await api(`/projects/${project.id}/commands`,{expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:'broker-tasks',changes:seeded.map(item=>({expectedRevision:0,entity:{id:item.taskId,kind:'task',data:item.profile}}))})).status===200);
  await nav('sessions');await page.locator('.session-list .records button').filter({hasText:'Actual Codex App agent'}).click();await page.locator('.composer').waitFor();
  let staleApproval:any;const seenRuns:any[]=[];
  for(const item of cases){
   const task=seeded.find(task=>task.name===item.name);await page.locator('.composer select').first().selectOption(item.mode);
   await until('bind_enabled_'+item.name,()=>page.locator('.composer').getByRole('button',{name:appLabel('ru','connect'),exact:true}).isEnabled());
   const bound=page.waitForResponse((response:any)=>response.url()===origin+'/api/v1/runtime/bindings');await page.locator('.composer').getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();check('binding_'+item.name,(await bound).status()===200);
   if(task){await page.locator('.composer select').nth(1).selectOption(task.taskId);const attach=page.getByRole('button',{name:appLabel('ru','attachTask'),exact:true});if(await attach.isEnabled())await attach.click();}
   await until('app_binding_ready_'+item.name,async()=>(await state()).canSend===true);
   const nonce=randomUUID();const prompt=JSON.stringify({kind:'PAOS_M1_NATIVE_BROKER_SYNTHETIC',case:item.name,nonce,files:item.files,outsideCanary,nodeBinary:process.execPath,instructions:'Use only PAOS agent command/operation/progress/report APIs for target actions. All commands require PAOS domain approval. For discussion/planning propose a write to its listed file; native denial is expected. Decline must propose a write and report only after declined. Write must append nonce once to accepted.txt, attempt outsideCanary and TEMP writes expecting denial, then run a separate read-only check requiring exactly one line. Repeat the same operationId/payload once to prove idempotency. Stop must create started.txt then schedule late.txt after 20 seconds; PAOS will interrupt it, report interrupted only after command settles and cancelRequested. Restart must propose stale.txt and wait without dispatch/report; PAOS will close before approval. Before commands send progress phase final_answer with M1_PROGRESS and nonce. Final text include M1_RESULT, case, nonce and observed outcome; no hidden reasoning, no direct target tools.'});
   await page.locator('.composer textarea').fill(prompt);await until('send_enabled_'+item.name,()=>page.getByRole('button',{name:uiLabel('ru','action.send'),exact:true}).isEnabled());
   const sentResponse=page.waitForResponse((response:any)=>response.url()===origin+'/api/v1/runtime/send'&&response.request().method()==='POST');await page.getByRole('button',{name:uiLabel('ru','action.send'),exact:true}).click();const response=await sentResponse;check('send_ack_'+item.name,response.status()===200);const run=await response.json(),payload=response.request().postDataJSON();seenRuns.push({case:item.name,runId:run.id});
   check('same_send_not_redispatched_'+item.name,(await api('/runtime/send',payload)).body.id===run.id);
   await note({...shared,stage:'job_queued',case:item.name,runId:run.id});console.log(JSON.stringify({stage:'job_queued',case:item.name}));
   const deadline=Date.now()+240000;let approvals=0,stopped=false;
   while(Date.now()<deadline){const value=await state();if(value.state==='recovery_required')throw Error('unexpected_recovery_'+item.name);
    if(value.pendingApprovals?.length){const approval=value.pendingApprovals[0];check('domain_approval_'+item.name+'_'+approvals,Boolean(approval.source==='paos_domain'&&approval.reviewable===true&&approval.details?.command));
     if(item.name==='restart'){staleApproval={...shared.scope,bindingId:value.bindingId,runId:value.runId,requestId:approval.requestId,generation:approval.generation,decision:'accept'};break;}
     const decision=item.name==='decline'?'deny':'approve';await page.getByRole('button',{name:appLabel('ru',decision),exact:true}).click();approvals++;
     await until('approval_answered_'+item.name+'_'+approvals,async()=>!(await state()).pendingApprovals.some((entry:any)=>entry.requestId===approval.requestId),30000);
    }
    if(item.name==='stop'&&!stopped){try{await readFile(join(workspace,'started.txt'));await page.getByRole('button',{name:uiLabel('ru','action.stopRun'),exact:true}).click();stopped=true;check('stop_requested_after_native_start',true);}catch(error){if((error as NodeJS.ErrnoException).code!=='ENOENT')throw error;}}
    if(['completed','interrupted'].includes(value.state)){check('terminal_'+item.name,value.state===(item.name==='stop'?'interrupted':'completed'));break;}
    await new Promise(resolve=>setTimeout(resolve,200));
   }
   if(item.name==='restart')break;
   const final=await state();check('terminal_receipt_'+item.name,['completed','interrupted'].includes(final.state));
   check('broker_boundary_'+item.name,final.capabilities.nativeSandbox===true&&final.capabilities.sandboxScope==='paos_mediated_commands'&&final.capabilities.appHostSandboxVerified===false);
   const messages=(await api(`/projects/${project.id}/entities?kind=message&parentId=${sessionId}&limit=100`)).body.items.filter((message:any)=>message.data?.runId===run.id&&message.data?.role==='assistant');check('one_result_'+item.name,messages.length===1&&messages[0].body.includes(nonce));
   await until('visible_result_'+item.name,async()=>(await page.locator('.transcript').innerText()).includes(messages[0].body));
   if(item.name==='write'){
    check('one_native_append',(await readFile(join(workspace,'accepted.txt'),'utf8')).trim()===nonce);check('outside_canary_preserved',await readFile(outsideCanary,'utf8')==='synthetic-outside-canary');
    check('native_checks_recorded',final.checks.filter((entry:any)=>entry.source==='native_command_broker'&&entry.exitCode===0).length>=2);check('actual_file_diff',final.fileChanges.some((file:any)=>file.kind==='actual'&&file.path==='accepted.txt'&&file.diff.includes(nonce)));
    const taskNow=(await api(`/projects/${project.id}/entities/${task!.taskId}`)).body;check('turn_did_not_close_task',taskNow.data.status==='in_progress');
    await page.getByRole('button',{name:appLabel('ru','changes'),exact:true}).click();await page.locator('pre.diff').filter({hasText:nonce}).first().waitFor();const shot=join(output,'native-actual-diff.png');await page.screenshot({path:shot,fullPage:true});report.screenshots.push(shot);await page.getByRole('button',{name:appLabel('ru','chat'),exact:true}).click();
   }else if(item.name!=='stop'){let absent=false;try{await readFile(join(workspace,item.files[0]));}catch(error){absent=(error as NodeJS.ErrnoException).code==='ENOENT';}check('write_absent_'+item.name,absent);}
   if(item.name==='stop'){let absent=false;try{await readFile(join(workspace,'late.txt'));}catch(error){absent=(error as NodeJS.ErrnoException).code==='ENOENT';}check('late_side_effect_absent',absent);}
  }
  check('pending_approval_captured_for_restart',!!staleApproval);await note({...shared,stage:'restart'});
  await until('worker_stopped_for_planned_restart',async()=>{try{return JSON.parse(await readFile(join(output,'worker-stopped.json'),'utf8')).reason==='planned_restart';}catch{return false;}},20000);
  const oldDescriptor=JSON.parse(await readFile(service.appAgentDescriptorPath,'utf8'));await service.quit();service=undefined;
  service=await startLocalService({profileDirectory,instanceId:randomUUID()});origin=`http://127.0.0.1:${service.port}`;await page.goto(origin);await page.getByLabel(appLabel('ru','code'),{exact:true}).fill(service.pairingCode);
  const again=page.waitForResponse((response:any)=>response.url()===origin+'/api/v1/bootstrap/exchange'&&response.status()===200);await page.getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();csrf=(await(await again).json()).csrfToken;
  const recovered=await state();report.restartSnapshot={state:recovered.state,bindingId:recovered.bindingId,runId:recovered.runId,mode:recovered.mode,canSend:recovered.canSend,pendingApprovalCount:recovered.pendingApprovals?.length};check('restart_unknown_fenced',recovered.state==='recovery_required'&&!recovered.canSend&&!recovered.pendingApprovals.length);check('stale_approval_rejected',(await api('/runtime/approve',staleApproval)).status!==200);
  const replay=await fetch(origin+'/agent/v1/claim',{method:'POST',headers:{origin,'content-type':'application/json',authorization:'Bearer '+oldDescriptor.capabilityToken},body:'{}'});check('old_capability_revoked_on_restart',replay.status===401);
  let staleAbsent=false;try{await readFile(join(workspace,'stale.txt'));}catch(error){staleAbsent=(error as NodeJS.ErrnoException).code==='ENOENT';}check('unapproved_command_never_replayed',staleAbsent);
  check('durable_history_after_restart',(await api(`/projects/${project.id}/entities?kind=message&parentId=${sessionId}&limit=100`)).body.items.filter((item:any)=>item.data?.role==='assistant').length===5);
  await nav('settings');await page.getByRole('button',{name:appLabel('ru','openAppAgentChannel'),exact:true}).click();
  await note({...shared,descriptorPath:service.appAgentDescriptorPath,previousStatePath:shared.descriptorPath+`.worker-${shared.workerId}.json`,completedRunId:seenRuns.find(run=>run.case==='write').runId,unresolvedRunId:staleApproval.runId,stage:'reattach'});console.log(JSON.stringify({stage:'reattach_required'}));
  await until('same_app_worker_reattached_after_restart',async()=>{try{const value=JSON.parse(await readFile(join(output,'worker-recovered.json'),'utf8'));return value.terminal?.state==='completed'&&value.unknown?.state==='recovery_required';}catch{return false;}},180000);
  check('no_native_replay_after_worker_migration',(await readFile(join(workspace,'accepted.txt'),'utf8')).trim().split('\n').length===1);
  await page.locator('.navigation select').selectOption(project.id);await nav('sessions');await page.locator('.session-list .records button').filter({hasText:'Actual Codex App agent'}).click();
  await until('only_undispatched_cancel_available',async()=>(await state()).recovery?.canCancelUndispatched===true);
  await page.getByRole('button',{name:appLabel('ru','cancelUndispatched'),exact:true}).click();await until('undispatched_run_cancelled_without_replay',async()=>(await state()).state==='interrupted');
  check('next_work_unfenced_after_proven_cancel',(await state()).canSend===true);
  report.runs=seenRuns;report.actualAppAgent=true;report.actualNativeCommandBroker=true;report.restartOutcome='recovery_required without replay; stale approval and old capability rejected';
  check('no_browser_errors',report.pageErrorCount===0);check('no_external_browser_requests',report.blockedExternalRequests===0);
  report.actualAgentExecution='Actual App LLM worker; all accepted target commands executed by qualified offline native broker';report.hostWorker='broker-app-worker';
  const screenshot=join(output,'app-broker-recovery.png');await page.screenshot({path:screenshot,fullPage:true});report.screenshots.push(screenshot);
  await note({...shared,stage:'completed'});
 }catch(error){report.error=String((error as Error).message);process.exitCode=1;}
 finally{if(context)await context.close();if(service){await service.quit();report.serviceClosed=true;}
  // This runner owns exactly its mkdtemp root; keep only the redacted receipt and screenshot.
  await rm(root,{recursive:true,force:true});report.fixtureCleaned=true;report.finishedAt=new Date().toISOString();await writeFile(join(output,'app-broker-result.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({output,passed:report.checks.filter((item:any)=>item.passed).length,failed:report.checks.filter((item:any)=>!item.passed).length,error:report.error??null}));}
}
main().catch(()=>{console.error('APP_AGENT_ACCEPTANCE_FAILED');process.exitCode=1;});
