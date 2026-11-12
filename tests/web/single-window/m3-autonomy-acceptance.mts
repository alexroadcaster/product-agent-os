import assert from 'node:assert/strict';
import {mkdir,mkdtemp,readFile,writeFile,rm,readdir} from 'node:fs/promises';
import {join,resolve,dirname,isAbsolute} from 'node:path';
import {pathToFileURL} from 'node:url';
import {randomUUID,createHash} from 'node:crypto';
import {startLocalService} from '../../../apps/local-service/src/main.mts';
import {newM2Task} from '../../../packages/contracts/issues/task-profile.ts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';
import {uiLabel} from '../../../apps/web/src/locales/messages.ts';

/** Real production HTTP/UI/native broker, synthetic worker only. No model turn or existing credentials. */
const argv=process.argv.slice(2);
if(argv[0]!=='--synthetic-browser'||argv.length!==9)throw Error('EXPLICIT_SYNTHETIC_BROWSER_AND_LOCAL_PATHS_REQUIRED');
const args=Object.fromEntries(Array.from({length:4},(_,i)=>argv.slice(1+i*2,3+i*2)));
for(const key of ['--binary','--playwright-core','--chromium','--screenshots'])if(!isAbsolute(args[key]??''))throw Error('ABSOLUTE_PATH_REQUIRED');
const scratch=resolve('.tmp/paos-m3');await mkdir(scratch,{recursive:true});
const root=await mkdtemp(join(scratch,'browser-fixture-')),output=await mkdtemp(join(scratch,'browser-evidence-'));
const workspace=join(root,'workspace'),profile=join(root,'profile'),home=join(root,'browser');
await Promise.all([mkdir(workspace),mkdir(profile),mkdir(home),mkdir(args['--screenshots'],{recursive:true})]);
await writeFile(join(profile,'runtime-selection.json'),JSON.stringify({binaryPath:args['--binary'],providerAuthority:false,purpose:'sandbox_commands_only'}));
const report:any={startedAt:new Date().toISOString(),syntheticOnly:true,actualAppAgent:false,syntheticWorker:true,actualNativeBroker:false,
  modelTurns:0,providerCalls:0,credentialOperations:0,browserPlugin:'not_available',checks:[],pageErrors:[],consoleErrors:[],externalRequests:[],screenshots:[],sourceHashes:{}};
let service:any,context:any,page:any,csrf='',worker:any,timer:ReturnType<typeof setInterval>|undefined,guard:ReturnType<typeof setTimeout>|undefined,step='setup';
const check=(name:string,passed:boolean,detail?:unknown)=>{report.checks.push({name,passed,...(detail===undefined?{}:{detail})});if(!passed)throw Error(name);};
async function until(name:string,predicate:()=>Promise<boolean>,timeout=18000){const end=Date.now()+timeout;while(Date.now()<end){if(await predicate()){check(name,true);return;}await new Promise(r=>setTimeout(r,100));}throw Error(name);}
try{
 service=await startLocalService({profileDirectory:profile,instanceId:randomUUID(),appCodexHome:join(root,'synthetic-codex-home')},{assetRoots:[]});
 const origin='http://127.0.0.1:'+service.port;report.origin=origin;
 const {chromium}=await import(pathToFileURL(join(args['--playwright-core'],'index.mjs')).href);
 context=await chromium.launchPersistentContext(home,{headless:true,chromiumSandbox:true,serviceWorkers:'block',viewport:{width:1440,height:1000},executablePath:args['--chromium'],
  env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:home,HOME:home,APPDATA:home,LOCALAPPDATA:home,TEMP:home,TMP:home}});
 guard=setTimeout(()=>void context?.close(),180000);
 await context.route('**/*',async(route:any)=>{const url=new URL(route.request().url());if(url.origin===origin)await route.continue();else{report.externalRequests.push(url.origin);await route.abort();}});
 page=context.pages()[0]??await context.newPage();page.setDefaultTimeout(15000);page.on('pageerror',(error:Error)=>report.pageErrors.push(error.message));
 page.on('console',(message:any)=>{if(message.type()==='error'&&!message.text().includes('Failed to load resource'))report.consoleErrors.push(message.text());});
 await page.goto(origin);check('page_identity',(await page.title()).includes('Product-Agent OS'));check('not_blank',(await page.locator('body').innerText()).includes('Product-Agent OS'));check('no_overlay',await page.locator('vite-error-overlay').count()===0);
 await page.getByLabel(appLabel('ru','code'),{exact:true}).fill(service.pairingCode);
 const paired=page.waitForResponse((response:any)=>response.url().endsWith('/bootstrap/exchange')&&response.status()===200);
 await page.getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();csrf=(await(await paired).json()).csrfToken;
 async function api(path:string,input?:unknown){return page.evaluate(async({path,input,csrf}:any)=>{const response=await fetch('/api/v1'+path,{method:input===undefined?'GET':'POST',headers:{'content-type':'application/json','x-paos-csrf':csrf},...(input===undefined?{}:{body:JSON.stringify(input)})});return {status:response.status,body:await response.json()};},{path,input,csrf});}
 let locale:'ru'|'en'='ru';
 async function nav(section:string){const menu=page.getByRole('button',{name:appLabel(locale,'menu'),exact:true});if(await menu.isVisible()&&await menu.getAttribute('aria-expanded')!=='true')await menu.click();await page.locator('nav').getByRole('button',{name:uiLabel(locale,('nav.'+section) as any),exact:true}).click();}
 async function shot(name:string){const file=join(args['--screenshots'],name);await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:file,fullPage:false});report.screenshots.push(file);}
 async function geometry(name:string){const geometry=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));check(name,geometry.scroll<=geometry.width+1,geometry);}
 const created=await api('/projects',{name:'Autonomy synthetic acceptance',keyPrefix:'AUTO',workspaceRoot:workspace});check('project_created',created.status===201);
 const project=created.body,base='/projects/'+project.id,taskId=randomUUID(),sessionId=randomUUID();
 const task={...newM2Task(project.id,taskId,'Bounded native fixture','local-user'),summary:'Observe policy guards',technicalValue:'Server admission',productValue:'Bounded work',files:[{relativePath:'proof.txt',plannedOperation:'create' as const,actualOperation:null}],acceptanceCriteria:['Native command creates proof only after approval'],estimateSeconds:30,risks:['none']};
 check('task_saved',(await api(base+'/task-manager/commands',{action:'save',task,expectedRevision:0,expectedAuthorityEpoch:1,idempotencyKey:'task'})).status===200);
 check('task_ready',(await api(base+'/task-manager/commands',{action:'transition',taskId,status:'ready',reason:'Synthetic acceptance',expectedRevision:1,expectedAuthorityEpoch:1,idempotencyKey:'ready'})).status===200);
 check('session_saved',(await api(base+'/commands',{expectedAuthorityEpoch:1,idempotencyKey:'session',changes:[{expectedRevision:0,entity:{id:sessionId,kind:'session',title:'Autonomy fixture session',data:{mode:'discussion'}}}]})).status===200);
 await page.reload();await page.locator('.navigation select:enabled').waitFor();await page.locator('.navigation select').selectOption(project.id);await nav('autonomy');
 const panel=page.getByTestId('autonomy-manager');await panel.locator('[name=autonomy-tasks]').selectOption([taskId]);
 await panel.locator('[name=autonomy-commands]').check();await panel.locator('[name=autonomy-maxRuns]').fill('2');await panel.locator('[name=autonomy-maxCommandsPerRun]').fill('2');await panel.locator('[name=autonomy-maxRunSeconds]').fill('60');
 step='narrow-preview';await panel.locator('[name=autonomy-paths]').fill('src');await panel.getByRole('button',{name:'Предпросмотр политики',exact:true}).click();
 await panel.getByTestId('autonomy-preview').waitFor();check('narrow_boundary_explicit',(await panel.innerText()).includes('AUTONOMY_PATH_BOUNDARY_UNAVAILABLE'));
 check('unsupported_save_disabled',await panel.getByRole('button',{name:'Сохранить на паузе',exact:true}).isDisabled());
 await panel.locator('[name=autonomy-paths]').fill('.');check('edit_invalidates_preview',await panel.getByTestId('autonomy-preview').count()===0);
 await panel.getByRole('button',{name:'Предпросмотр политики',exact:true}).click();await panel.getByRole('button',{name:'Сохранить на паузе',exact:true}).click();
 await until('save_is_paused',async()=>Boolean((await api(base+'/autonomy')).body.policy)&&(await api(base+'/autonomy')).body.paused);
 check('save_does_not_dispatch',(await api(base+'/autonomy')).body.usedRuns===0);
 await panel.getByRole('button',{name:'Разрешить новые запуски',exact:true}).click();await until('resume_admission_only',async()=>(await api(base+'/autonomy')).body.paused===false);
 check('permissions_boundary_visible',(await panel.innerText()).includes('host permissions не меняются'));
 step='stale-preview';await panel.locator('[name=autonomy-maxRuns]').fill('3');let state=(await api(base+'/autonomy')).body;
 await api(base+'/autonomy/pause',{expectedRevision:state.revision,expectedAuthorityEpoch:1,idempotencyKey:'external-pause'});
 await panel.getByRole('button',{name:'Предпросмотр политики',exact:true}).click();await until('stale_revision_explained',async()=>(await panel.innerText()).includes('AUTONOMY_REVISION_CONFLICT'));
 check('stale_draft_retained',await panel.locator('[name=autonomy-maxRuns]').inputValue()==='3');
 await panel.getByRole('button',{name:'Обновить состояние, сохранив черновик',exact:true}).click();
 await panel.getByRole('button',{name:'Предпросмотр политики',exact:true}).click();await panel.getByRole('button',{name:'Сохранить на паузе',exact:true}).click();
 await until('reviewed_draft_saved',async()=>(await api(base+'/autonomy')).body.policy?.maxRuns===3);
 await panel.getByRole('button',{name:'Разрешить новые запуски',exact:true}).click();await until('policy_armed',async()=>(await api(base+'/autonomy')).body.paused===false);
 await geometry('desktop_geometry');await shot('paos-0023-desktop.png');
 step='native-route';check('app_route_selected',(await api('/connection',{route:'codex_app_agent'})).status===200);
 const descriptor=JSON.parse(await readFile(service.appAgentDescriptorPath,'utf8'));
 async function agent(action:string,input:Record<string,unknown>={}){const response=await fetch(origin+'/agent/v1/'+action,{method:'POST',headers:{origin,authorization:'Bearer '+descriptor.capabilityToken,'content-type':'application/json'},body:JSON.stringify(action==='attach'?{hostIdentity:'codex_app',workerId:'synthetic-policy-worker',generation:'synthetic-generation'}:{...input,workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken})});const body=await response.json();if(!response.ok)throw Error('AGENT_'+action+'_'+(body.error?.code??response.status));return body;}
 worker=await agent('attach');timer=setInterval(()=>void agent('heartbeat').catch(()=>{}),10000);
 await page.reload();await page.locator('.navigation select:enabled').waitFor();await page.locator('.navigation select').selectOption(project.id);await nav('sessions');
 await page.locator('.session-list .records button').filter({hasText:'Autonomy fixture session'}).click();await page.locator('.composer').waitFor();
 await page.locator('.composer select').first().selectOption('execution');
 const bindingResponse=page.waitForResponse((response:any)=>response.url().endsWith('/runtime/bindings'));
 await page.locator('.composer').getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();const bindingReceipt=await bindingResponse;check('qualified_native_binding',bindingReceipt.status()===200);
 const binding=await bindingReceipt.json(),scope={projectId:project.id,sessionId,bindingId:binding.bindingId};
 await page.locator('.composer select').nth(1).selectOption(taskId);const attach=page.getByRole('button',{name:appLabel('ru','attachTask'),exact:true});if(await attach.isEnabled())await attach.click();
 const optin=page.locator('[name=session-autonomy]');await until('optin_available',()=>optin.isEnabled());await optin.check();
 await page.locator('.composer textarea').fill('Perform one synthetic bounded native command.');await until('send_enabled',()=>page.getByRole('button',{name:uiLabel('ru','action.send'),exact:true}).isEnabled());
 const sendResponse=page.waitForResponse((response:any)=>response.url().endsWith('/runtime/send')&&response.request().method()==='POST');await page.getByRole('button',{name:uiLabel('ru','action.send'),exact:true}).click();const send=await sendResponse;check('policy_dispatch',send.status()===200);
 const run=await send.json();check('autonomy_explicit_payload',send.request().postDataJSON().autonomy===true);check('policy_pin',typeof run.autonomy?.budgetId==='string');
 check('claimed_existing_gateway',(await agent('claim')).job.runId===run.id);check('budget_charged_once',(await api(base+'/autonomy')).body.usedRuns===1);
 const command={runId:run.id,operationId:'native-proof',argv:[process.execPath,'-e',"require('node:fs').writeFileSync('proof.txt','policy-native-proof');console.log('POLICY_NATIVE_OK')"],timeoutMs:10000};
 check('command_awaits_approval',(await agent('command',command)).state==='awaiting_approval');
 try{await readFile(join(workspace,'proof.txt'));check('no_unapproved_file',false);}catch(error){if((error as NodeJS.ErrnoException).code==='ENOENT')check('no_unapproved_file',true);else throw error;}
 const approved=await api('/runtime/approve',{...scope,runId:run.id,requestId:'native-proof',generation:worker.generation,decision:'accept'});check('explicit_approval',approved.status===200);
 await until('native_command_observed',async()=>(await agent('operation',{runId:run.id,operationId:'native-proof'})).state==='completed');
 const operation=await agent('operation',{runId:run.id,operationId:'native-proof'});check('native_command_exit_zero',operation.exitCode===0);check('native_output',operation.stdout.includes('POLICY_NATIVE_OK'));check('actual_fixture_write',await readFile(join(workspace,'proof.txt'),'utf8')==='policy-native-proof');report.actualNativeBroker=true;
 step='pause-before-approval';await agent('command',{runId:run.id,operationId:'blocked-after-pause',argv:[process.execPath,'-e',"require('node:fs').writeFileSync('forbidden.txt','must-not-run')"]});
 await nav('autonomy');await panel.getByRole('button',{name:'Пауза',exact:true}).click();await until('pause_durable',async()=>(await api(base+'/autonomy')).body.paused===true);
 const denied=await api('/runtime/approve',{...scope,runId:run.id,requestId:'blocked-after-pause',generation:worker.generation,decision:'accept'});check('pause_denies_pending_approval',denied.status===409);
 const runtimeState=(await api('/runtime/state?'+new URLSearchParams({projectId:project.id,sessionId}))).body;check('stop_request_not_terminal',runtimeState.state==='cancel_requested');
 await agent('report',{runId:run.id,seq:1,idempotencyKey:'interrupted',status:'interrupted'});
 check('terminal_only_after_ack',(await api('/runtime/state?'+new URLSearchParams({projectId:project.id,sessionId}))).body.state==='interrupted');
 try{await readFile(join(workspace,'forbidden.txt'));check('paused_command_absent',false);}catch(error){if((error as NodeJS.ErrnoException).code==='ENOENT')check('paused_command_absent',true);else throw error;}
 check('task_acceptance_separate',(await api(base+'/entities/'+taskId)).body.status==='in_progress');
 step='responsive-locale';await nav('settings');await page.getByLabel(uiLabel('ru','preferences.language'),{exact:true}).selectOption('en');await page.getByLabel(uiLabel('ru','preferences.theme'),{exact:true}).selectOption('dark');await page.getByRole('button',{name:uiLabel('ru','preferences.save'),exact:true}).click();locale='en';
 await nav('autonomy');await page.getByTestId('autonomy-manager').getByRole('heading',{name:'Autonomous work',exact:true}).waitFor();check('english_dark',await page.locator('html').getAttribute('data-theme')==='dark');
 await page.setViewportSize({width:390,height:844});await geometry('mobile_geometry');await shot('paos-0023-mobile.png');
 await page.getByTestId('autonomy-manager').getByRole('button',{name:'Refresh state, keeping draft',exact:true}).focus();check('keyboard_focus',await page.evaluate(()=>document.activeElement?.textContent?.includes('Refresh state')));
 check('no_page_errors',report.pageErrors.length===0,report.pageErrors);check('no_console_errors',report.consoleErrors.length===0,report.consoleErrors);check('no_external_requests',report.externalRequests.length===0);
 report.status='passed';report.finalPolicy=(await api(base+'/autonomy')).body;
}catch(error){report.status='failed';report.failedStep=step;report.error=String(error).slice(0,1200);process.exitCode=1;try{await shotFailure();}catch{}}
finally{
 if(timer)clearInterval(timer);if(guard)clearTimeout(guard);await context?.close();await service?.quit();
 assert.equal(dirname(resolve(root)),scratch);await rm(root,{recursive:true,force:true});report.fixtureCleaned=true;report.finishedAt=new Date().toISOString();
 for(const file of ['packages/contracts/autonomy/policy.ts','apps/local-service/src/autonomy-policy/service.mts','apps/local-service/src/runtime/app-agent-gateway.mts','apps/web/src/features/autonomy/AutonomyManager.tsx','apps/web/src/ui/App.tsx','apps/web/dist/index.html',...(await readdir('apps/web/dist/assets')).map(name=>'apps/web/dist/assets/'+name)])report.sourceHashes[file]=createHash('sha256').update(await readFile(file)).digest('hex');
 await writeFile(join(output,'result.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,checks:report.checks.length,failedStep:report.failedStep,error:report.error,report:join(output,'result.json')}));
}
async function shotFailure(){const file=join(args['--screenshots'],'paos-0023-failed.png');await page.screenshot({path:file});report.failureUi=(await page.locator('body').innerText()).slice(0,12000);report.screenshots.push(file);}
