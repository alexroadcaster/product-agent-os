import {mkdtemp,mkdir,writeFile,readFile,rm,readdir,unlink} from 'node:fs/promises';
import {resolve,join,dirname,isAbsolute} from 'node:path';
import {pathToFileURL} from 'node:url';
import {randomUUID,createHash} from 'node:crypto';
import {startLocalService} from '../../../apps/local-service/src/main.mts';
import {newM2Task} from '../../../packages/contracts/issues/task-profile.ts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';
import {uiLabel} from '../../../apps/web/src/locales/messages.ts';
import {label} from '../../../apps/web/src/features/tasks/labels.ts';

/** Explicit one-job actual App-hosted M2 execution; native broker owns the sole fixture write. */
async function main(){
 const argv=process.argv.slice(2);if(argv.length!==7||argv[0]!=='--actual-app-m2b')throw Error('EXPLICIT_ACTUAL_APP_M2_REQUIRED');
 const args=Object.fromEntries([argv.slice(1,3),argv.slice(3,5),argv.slice(5,7)]);
 if(!['--binary','--playwright-core','--chromium'].every(k=>isAbsolute(args[k]??'')))throw Error('INSTALLED_PATHS_REQUIRED');
 const scratch=resolve('.tmp/paos-m2b');await mkdir(scratch,{recursive:true});
 const root=await mkdtemp(join(scratch,'actual-app-fixture-')),output=await mkdtemp(join(scratch,'actual-app-evidence-')),coordination=join(scratch,'actual-app-coordination.json');
 const workspace=join(root,'workspace'),profileDirectory=join(root,'profile'),home=join(root,'browser');await Promise.all([mkdir(workspace),mkdir(profileDirectory),mkdir(home)]);
 await writeFile(join(profileDirectory,'runtime-selection.json'),JSON.stringify({binaryPath:args['--binary'],providerAuthority:false,purpose:'sandbox_commands_only'}));
 const report:any={startedAt:new Date().toISOString(),actualAppAgent:false,actualNativeBroker:false,apiKey:false,externalProviderClient:false,realCredentials:false,hostIdentity:'attested_not_cryptographic',sandboxScope:'paos_mediated_commands',checks:[],screenshots:[],pageErrors:[],externalRequests:[],sourceHashes:{}};
 const check=(name:string,passed:boolean)=>{report.checks.push({name,passed});if(!passed)throw Error(name);};
 let service:Awaited<ReturnType<typeof startLocalService>>|undefined,context:any,page:any,csrf='',timer:ReturnType<typeof setTimeout>|undefined,shared:any,step='setup';
 const note=async(stage:string,extra={})=>writeFile(coordination,JSON.stringify({...shared,stage,...extra}));
 try{
  service=await startLocalService({profileDirectory,instanceId:randomUUID(),appCodexHome:join(root,'codex-home')},{assetRoots:[]});const origin='http://127.0.0.1:'+service.port;report.origin=origin;
  const {chromium}=await import(pathToFileURL(join(args['--playwright-core'],'index.mjs')).href);
  context=await chromium.launchPersistentContext(home,{headless:true,chromiumSandbox:true,serviceWorkers:'block',viewport:{width:1440,height:1000},locale:'ru-RU',executablePath:args['--chromium'],timeout:20000,env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:home,HOME:home,APPDATA:home,LOCALAPPDATA:home,TEMP:home,TMP:home}});
  timer=setTimeout(()=>void context?.close(),360000);
  await context.route('**/*',async(route:any)=>{const url=new URL(route.request().url());if(url.origin===origin)await route.continue();else{report.externalRequests.push(url.origin);await route.abort();}});
  page=context.pages()[0]??await context.newPage();page.setDefaultTimeout(15000);page.on('pageerror',(e:Error)=>report.pageErrors.push(e.message));
  await page.goto(origin);check('page_identity',(await page.title()).includes('Product-Agent OS'));
  await page.getByLabel(appLabel('ru','code'),{exact:true}).fill(service.pairingCode);const paired=page.waitForResponse((r:any)=>r.url()===origin+'/api/v1/bootstrap/exchange'&&r.status()===200);
  await page.getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();csrf=(await(await paired).json()).csrfToken;
  async function api(path:string,input?:unknown){return page.evaluate(async({path,input,csrf}:any)=>{const response=await fetch('/api/v1'+path,{method:input===undefined?'GET':'POST',headers:{'content-type':'application/json','x-paos-csrf':csrf},...(input===undefined?{}:{body:JSON.stringify(input)})});return {status:response.status,body:await response.json()};},{path,input,csrf});}
  async function nav(section:string){await page.locator('nav').getByRole('button',{name:uiLabel('ru',('nav.'+section) as any),exact:true}).click();}
  async function until(name:string,predicate:()=>Promise<boolean>,timeout=30000){const deadline=Date.now()+timeout;while(Date.now()<deadline){if(await predicate()){check(name,true);return;}await new Promise(r=>setTimeout(r,200));}check(name,false);}
  const registered=await api('/projects',{name:'Actual App M2 fixture',workspaceRoot:workspace,keyPrefix:'APPM'});check('project_saved',registered.status===201);const project=registered.body,sessionId=randomUUID();
  check('session_saved',(await api('/projects/'+project.id+'/commands',{expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:'m2-app-session',changes:[{expectedRevision:0,entity:{id:sessionId,kind:'session',title:'M2 actual App worker',data:{mode:'discussion'}}}]})).status===200);
  const snapshot=async()=>(await api('/projects/'+project.id+'/task-manager')).body;
  const command=async(input:any)=>api('/projects/'+project.id+'/task-manager/commands',{...input,expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:randomUUID()});
  let manager=await snapshot(),definition=structuredClone(manager.workflows.workflows[0].versions[0].definition);definition.name='Actual custom workflow';definition.states=definition.states.map((s:any)=>({...s,id:'custom_'+s.id}));definition.transitions=definition.transitions.map((t:any)=>({...t,from:'custom_'+t.from,to:'custom_'+t.to}));
  check('custom_draft',(await command({action:'workflow-save-draft',workflowId:'actual-custom',definition,expectedRevision:manager.settingsRevisions.workflows})).status===200);
  manager=await snapshot();await command({action:'board',expectedRevision:manager.settingsRevisions.board,board:{...manager.board,outOfBoard:true}});manager=await snapshot();let plan=(await command({action:'workflow-publish-preview',workflowId:'actual-custom',expectedRevision:manager.settingsRevisions.workflows})).body;
  check('custom_published',(await command({action:'workflow-publish',workflowId:'actual-custom',expectedRevision:manager.settingsRevisions.workflows,previewDigest:plan.previewDigest})).status===200);
  const taskId=randomUUID(),task={...newM2Task(project.id,taskId,'M2 actual execution','local-user'),summary:'Create one bounded synthetic proof file through the native command broker.',technicalValue:'Prove versioned M2 profile reaches App execution.',productValue:'New task types work with existing keyless App route.',files:[{relativePath:'m2-proof.txt',plannedOperation:'create' as const,actualOperation:null}],acceptanceCriteria:['Native proof file contains the correlated token and computed sum'],estimateSeconds:60,risks:['none']};
  let receipt=await api('/projects/'+project.id+'/task-manager/commands',{action:'save',task,workflowId:'actual-custom',expectedRevision:0,expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:'m2-app-task'});check('m2_task_saved',receipt.status===200);
  const getTask=async()=>(await api('/projects/'+project.id+'/entities/'+taskId)).body;
  receipt=await api('/projects/'+project.id+'/task-manager/commands',{action:'transition',taskId,expectedRevision:(await getTask()).revision,status:'custom_ready',reason:'Bounded actual M2 App acceptance',expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:'m2-app-ready'});check('m2_ready',receipt.status===200);
  await page.reload();await page.locator('.navigation select:enabled').waitFor();await page.locator('.navigation select').selectOption(project.id);await nav('settings');
  check('keyless_route_default',await page.getByLabel(appLabel('ru','connectionRoute'),{exact:true}).inputValue()==='codex_app_agent');check('no_api_key_input',await page.locator('input[name=apiKey]').count()===0);
  const opened=page.waitForResponse((r:any)=>r.url()===origin+'/api/v1/connection'&&r.request().method()==='POST');
  await page.locator('.panel').filter({has:page.getByLabel(appLabel('ru','connectionRoute'),{exact:true})}).getByRole('button',{name:appLabel('ru','openAppAgentChannel'),exact:true}).click();check('app_channel_opened',(await opened).status()===200);
  shared={descriptorPath:service.appAgentDescriptorPath,workerId:'m2b-actual-app-worker',output,scope:{projectId:project.id,sessionId},taskId,nodeBinary:process.execPath,expectedJobs:4};
  await note('waiting_for_agent');console.log(JSON.stringify({stage:'waiting_for_agent',coordination,output}));
  await until('actual_app_worker_attached',async()=>(await api('/connection')).body.verified===true,180000);
  let agentId='';
  for(const intent of ['create','update','delete']){
   await nav('agents');const team=page.getByTestId('agent-manager');if(agentId)await team.locator('[data-asset-id="'+agentId+'"]').click();
   const generator=team.getByTestId('agent-generator');await generator.locator('[name=agent-generation-description]').fill(intent==='create'?'Create an agent named Bounded reviewer. It reviews source read-only, preserves approvals, and reports concrete findings.':intent==='update'?'Update the selected Bounded reviewer to require an evidence path for each finding. Keep permission boundaries.':'Prepare deletion of the exact selected Bounded reviewer because the synthetic trial is ending. Do not delete until explicit Apply.');
   const started=page.waitForResponse((r:any)=>r.url().endsWith('/team/generation')&&r.request().method()==='POST');await generator.getByRole('button',{name:'Сгенерировать proposal',exact:true}).click();const generated=await started;check('generation_'+intent+'_dispatch',generated.status()===200);const job=await generated.json();
   await note('job_queued',{runId:job.id,intent});console.log(JSON.stringify({stage:'generation_queued',intent}));
   await until('generation_'+intent+'_completed',async()=>{const result=(await api('/projects/'+project.id+'/team/generation/'+job.id)).body;return result.state==='completed'&&Boolean(result.proposal);},180000);
   await generator.getByRole('button',{name:'Открыть draft в редакторе',exact:true}).click();const editor=team.getByTestId('asset-editor');await editor.waitFor();
   check('generation_'+intent+'_editable',await editor.locator('[name=asset-content]').isEditable());
   const catalog=(await api('/projects/'+project.id+'/team/catalog')).body;
   check('generation_'+intent+'_no_auto_apply',intent==='create'?!catalog.assets.some((a:any)=>a.management==='paos_managed'):catalog.assets.find((a:any)=>a.id===agentId)?.effectiveVersion===(intent==='update'?1:2));
   if(intent==='delete'){check('delete_proposal_exact_target',await editor.locator('[name=asset-action]').inputValue()==='delete');await editor.getByRole('button',{name:label('ru','discard'),exact:true}).click();continue;}
   await editor.getByRole('button',{name:'Проверить и показать diff',exact:true}).click();await team.getByTestId('asset-preview').locator('[name=asset-apply-confirm]').check();await team.getByRole('button',{name:'Применить proposal',exact:true}).click();
   await until('generation_'+intent+'_explicit_apply',async()=>{const rows=(await api('/projects/'+project.id+'/team/catalog')).body.assets;const a=rows.find((a:any)=>a.management==='paos_managed'&&a.kind==='agent');if(a){agentId=a.id;return a.effectiveVersion===(intent==='create'?1:2);}return false;});
  }
  let saved=await getTask();check('managed_assignment_saved',(await command({action:'save',task:{...saved.data,agentAssignments:[agentId]},expectedRevision:saved.revision,reason:'Pin actual managed profile'})).status===200);
  await nav('sessions');await page.locator('.session-list .records button').filter({hasText:'M2 actual App worker'}).click();await page.locator('.composer').waitFor();
  await page.locator('.composer select').first().selectOption('execution');
  const binding=page.waitForResponse((r:any)=>r.url()===origin+'/api/v1/runtime/bindings');await page.locator('.composer').getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();const bound=await binding;report.bindingReceipt={status:bound.status(),body:await bound.json()};check('execution_binding',bound.status()===200);
  await page.locator('.composer select').nth(1).selectOption(taskId);const attach=page.getByRole('button',{name:appLabel('ru','attachTask'),exact:true});if(await attach.isEnabled())await attach.click();
  const state=async()=>(await api('/runtime/state?'+new URLSearchParams(shared.scope))).body;
  await until('m2_can_send',async()=>(await state()).canSend===true);
  const nonce=randomUUID();const prompt=JSON.stringify({kind:'PAOS_M2_ACTUAL_ACCEPTANCE',nonce,numbers:[17,4,9],file:'m2-proof.txt',nodeBinary:process.execPath,instructions:'Calculate the sum of numbers yourself. Use ONLY callAppAgent command/operation APIs for target filesystem actions. Propose argv [nodeBinary,\"-e\",code] writing exactly nonce+\"|\"+computedSum+\"\\n\" once to relative m2-proof.txt and printing M2_NATIVE_OK. Wait for PAOS domain approval and observed operation exit0 before reporting completed. Never write target through host filesystem tools. Final text exactly M2_RESULT CORRELATION=<nonce>; SUM=<computed sum>. Do not change Task status, read credentials, call providers or access unrelated files.'});
  await page.locator('.composer textarea').fill(prompt);await until('send_enabled',()=>page.getByRole('button',{name:uiLabel('ru','action.send'),exact:true}).isEnabled());
  const sent=page.waitForResponse((r:any)=>r.url()===origin+'/api/v1/runtime/send'&&r.request().method()==='POST');await page.getByRole('button',{name:uiLabel('ru','action.send'),exact:true}).click();const response=await sent;check('m2_dispatch_ack',response.status()===200);const run=await response.json();
  check('real_m2_profile_not_legacy_fallback',(await getTask()).data.schemaVersion==='m2_task_profile_v1'&&(await getTask()).status==='custom_in_progress');
  const getJob=async()=>(await api('/projects/'+project.id+'/team/assets/'+agentId)).body;
  await note('job_queued',{runId:run.id,intent:'execution'});
  await until('actual_managed_pin_observed',async()=>(await getJob()).observedPins?.some((p:any)=>p.runId===run.id&&p.version===2));
  const beforeProfile=await getJob();manager=await snapshot();definition.name='New workflow for future tasks';await command({action:'workflow-save-draft',workflowId:'actual-custom',definition,expectedRevision:manager.settingsRevisions.workflows});manager=await snapshot();plan=(await command({action:'workflow-publish-preview',workflowId:'actual-custom',expectedRevision:manager.settingsRevisions.workflows})).body;check('publish_during_run',(await command({action:'workflow-publish',workflowId:'actual-custom',previewDigest:plan.previewDigest,expectedRevision:manager.settingsRevisions.workflows})).status===200);
  const changed={kind:'agent',action:'update',assetId:agentId,name:beforeProfile.name,description:beforeProfile.description,content:beforeProfile.content+'\nFuture version only.',dependencies:beforeProfile.dependencies,resources:beforeProfile.resources,source:beforeProfile.source,reason:'Verify immutable active run pin'};
  const pp=(await api('/projects/'+project.id+'/team/proposals/preview',{proposal:changed,expectedRevision:beforeProfile.revision})).body;check('profile_update_during_run',(await api('/projects/'+project.id+'/team/proposals/apply',{...pp,expectedRevision:beforeProfile.revision,epoch:project.authorityEpoch,idempotencyKey:randomUUID()})).status===200);
  check('active_pin_retains_v2',(await getJob()).observedPins.some((p:any)=>p.runId===run.id&&p.version===2));await note('execution_pins_checked',{runId:run.id,intent:'execution'});
console.log(JSON.stringify({stage:'job_queued'}));let approved=false;
  const deadline=Date.now()+180000;
  while(Date.now()<deadline){const current=await state();if(current.state==='recovery_required')throw Error('ACTUAL_APP_LEASE_OR_OUTCOME_UNKNOWN');
   if(current.pendingApprovals?.length){const approval=current.pendingApprovals[0];check('domain_approval_scope',approval.source==='paos_domain'&&approval.reviewable===true&&approval.runId===run.id);
    check('bounded_native_command',String(approval.details?.command??'').includes('m2-proof.txt'));await page.getByRole('button',{name:appLabel('ru','approve'),exact:true}).click();approved=true;}
   if(current.state==='completed')break;await new Promise(r=>setTimeout(r,200));
  }
  const final=await state();check('actual_app_completed',final.state==='completed');check('native_approval_observed',approved);
  check('native_file_exactly_once',await readFile(join(workspace,'m2-proof.txt'),'utf8')===nonce+'|30\n');
  check('native_observed_check',final.checks.some((c:any)=>c.source==='native_command_broker'&&c.exitCode===0));
  check('actual_file_operation_recorded',(await getTask()).data.files[0].actualOperation==='create');
  check('turn_did_not_auto_close_task',(await getTask()).status==='custom_in_progress');
  const messages=(await api('/projects/'+project.id+'/entities?kind=message&parentId='+sessionId)).body.items;
  check('actual_model_answer_correlated',messages.some((m:any)=>m.data?.role==='assistant'&&m.body==='M2_RESULT CORRELATION='+nonce+'; SUM=30'));
  await until('answer_rendered',async()=>(await page.locator('.transcript').innerText()).includes('M2_RESULT CORRELATION='+nonce));
  await nav('tasks');await page.locator('[data-task-id="'+taskId+'"]').click();await page.getByTestId('task-detail').getByRole('tab',{name:label('ru','acceptance'),exact:true}).click();
  const panel=page.getByTestId('task-transition');await panel.locator('[name=transition-reason]').fill('Observed actual App/native receipt');await panel.locator('[name=criterion-evidence-0]').fill('Actual native file bytes, exit0, correlated App result');await panel.locator('[name=criterion-passed-0]').check();await panel.getByRole('button',{name:label('ru','complete'),exact:true}).click();
  await until('explicit_manual_task_acceptance',async()=>(await getTask()).status==='custom_done');
  const screenshot=join(output,'actual-m2-app-result.png');await page.screenshot({path:screenshot,fullPage:false});report.screenshots.push(screenshot);
  check('no_browser_errors',report.pageErrors.length===0);check('no_external_browser_requests',report.externalRequests.length===0);
  report.actualAppAgent=true;report.actualNativeBroker=true;report.taskSchemaVersion='m2_task_profile_v1';report.taskId=taskId;report.runId=run.id;report.status='passed_actual_m2b_generation_and_pinned_native';report.limits=['App and active consumer required','Host identity attested, not cryptographic','Only PAOS-mediated native commands qualified; no claim about every App host tool','No commercial/account entitlement promotion'];
  await note('completed',{runId:run.id});
  const sources=['apps/local-service/src/runtime/app-agent-gateway.mts','apps/local-service/src/runtime/storage-ports.mts','apps/local-service/src/runtime/sandbox-broker.mts','apps/local-service/src/storage/sqlite-worker.mts','apps/local-service/src/storage/migrations/schema.mts','packages/contracts/issues/task-profile.ts','apps/web/src/api/session-target.ts','tests/web/single-window/m2b-app-acceptance.mts','apps/web/dist/index.html'];
  for(const name of await readdir('apps/web/dist/assets'))sources.push('apps/web/dist/assets/'+name);for(const name of sources)report.sourceHashes[name]=createHash('sha256').update(await readFile(name)).digest('hex');
 }catch(error){report.status='failed';report.failedStep=step;report.error=String((error as Error).message).slice(0,1200);process.exitCode=1;try{await note('failed');if(page&&!page.isClosed())await page.screenshot({path:join(output,'failed.png'),mask:[page.locator('input')]});}catch{}}
 finally{if(timer)clearTimeout(timer);try{await context?.close();report.browserClosed=true;}catch{report.browserClosed=false;process.exitCode=1;}try{await service?.quit();report.serviceClosed=true;}catch{report.serviceClosed=false;process.exitCode=1;}
  if(report.serviceClosed){if(dirname(resolve(root))!==scratch)throw Error('FIXTURE_CLEANUP_BOUNDARY');await rm(root,{recursive:true,force:true});report.fixtureCleaned=true;}
  report.finishedAt=new Date().toISOString();await writeFile(join(output,'m2-app-result.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({status:report.status,checks:report.checks.length,error:report.error,report:join(output,'m2-app-result.json'),fixtureCleaned:report.fixtureCleaned}));
 }
}
await main();
