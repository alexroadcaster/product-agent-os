import {mkdtemp,mkdir,readFile,writeFile,rm,readdir} from 'node:fs/promises';
import {join,isAbsolute} from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {createHash,randomUUID} from 'node:crypto';
import {startLocalService} from '../../../apps/local-service/src/main.mts';
import {openLocalStore,type LocalStore} from '../../../apps/local-service/src/storage/local-store.mts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';
import {uiLabel} from '../../../apps/web/src/locales/messages.ts';

/** Explicit local UI acceptance. No runtime connection, model, provider, auth cache or OS credential use. */
async function main(argv:string[]){
 if(argv.length!==5||argv[0]!=='--synthetic-browser')throw new Error('EXPLICIT_SYNTHETIC_BROWSER_REQUIRED');
 const args=Object.fromEntries([argv.slice(1,3),argv.slice(3,5)]) as Record<string,string>;
 if(!args['--playwright-core']||!args['--chromium']||!Object.values(args).every(isAbsolute))throw new Error('EXPLICIT_BROWSER_PATHS_REQUIRED');
 const scratch=fileURLToPath(new URL('../../../.tmp/paos-m1/',import.meta.url));await mkdir(scratch,{recursive:true});
 const output=await mkdtemp(join(scratch,'task-lifecycle-evidence-')),fixture=await mkdtemp(join(scratch,'task-lifecycle-fixture-'));
 const profile=join(fixture,'profile'),workspace=join(fixture,'workspace'),browserHome=join(fixture,'browser');
 await Promise.all([mkdir(profile),mkdir(workspace),mkdir(browserHome)]);await writeFile(join(workspace,'REQUIREMENTS.md'),'# Synthetic source\nOnly local task lifecycle acceptance.\n');
 const report:any={startedAt:new Date().toISOString(),syntheticOnly:true,actualAppAgent:false,actualModel:false,providerUsed:false,apiKey:false,osStoreUsed:false,
  browserPlugin:'not_available',browserDriver:'installed_playwright_core',checks:[],screenshots:[],sourceHashes:{},blockedRequests:[],httpErrors:[],pageErrorCount:0,
  nonUiSetup:['project registration via paired HTTP','synthetic archived transcript via real LocalStore API; not model output'],apiConcurrency:['second writer through authenticated commands endpoint']};
 const check=(name:string,passed:boolean)=>{report.checks.push({name,passed});if(!passed)throw new Error(name);};
 let service:Awaited<ReturnType<typeof startLocalService>>|undefined,store:LocalStore|undefined,context:any,page:any,timer:ReturnType<typeof setTimeout>|undefined,csrf='',step='setup';
 try{
  const paths=['tests/web/single-window/task-lifecycle-browser-acceptance.mts','apps/local-service/src/main.mts','apps/local-service/src/http/application.mts','apps/local-service/src/tasks/user-commands.mts','apps/local-service/src/storage/sqlite-worker.mts','apps/web/src/ui/App.tsx','apps/web/src/ui/Operations.tsx','apps/web/src/ui/TaskRelations.tsx','apps/web/src/api/task.ts','apps/web/src/api/client.ts','apps/web/src/locales/app.ts','apps/web/dist/index.html'];
  for(const name of await readdir(fileURLToPath(new URL('../../../apps/web/dist/assets/',import.meta.url))))paths.push('apps/web/dist/assets/'+name);
  for(const name of paths)report.sourceHashes[name]=createHash('sha256').update(await readFile(fileURLToPath(new URL('../../../'+name,import.meta.url)))).digest('hex');
  service=await startLocalService({profileDirectory:profile,instanceId:randomUUID()},{openStore:async options=>{store=await openLocalStore(options);return store;}});
  const origin=`http://127.0.0.1:${service.port}`;report.origin=origin;
  const {chromium}=await import(pathToFileURL(join(args['--playwright-core'],'index.mjs')).href);
  context=await chromium.launchPersistentContext(browserHome,{headless:true,chromiumSandbox:true,serviceWorkers:'block',viewport:{width:1440,height:1000},locale:'ru-RU',executablePath:args['--chromium'],timeout:20000,
   env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:browserHome,HOME:browserHome,APPDATA:browserHome,LOCALAPPDATA:browserHome,TEMP:browserHome,TMP:browserHome}});
  timer=setTimeout(()=>void context?.close(),180000);
  await context.route('**/*',async(route:any)=>{const request=route.request(),url=new URL(request.url()),method=request.method();
   const allowed=url.origin===origin&&!url.username&&!url.password&&(
    method==='GET'&&(url.pathname==='/'||url.pathname==='/health'||/^\/assets\/[A-Za-z0-9_.-]+$/.test(url.pathname)||/^\/api\/v1\/(session|projects|preferences|connection|runtime\/state)$/.test(url.pathname)||/^\/api\/v1\/projects\/[^/]+\/(entities(?:\/[^/]+)?|events|history|catalogs|sources(?:\/[^/]+)?)$/.test(url.pathname))
    ||method==='POST'&&(/^\/api\/v1\/(bootstrap\/exchange|projects)$/.test(url.pathname)||/^\/api\/v1\/projects\/[^/]+\/(commands|tasks\/[^/]+\/(check|accept))$/.test(url.pathname)));
   if(allowed)await route.continue();else{report.blockedRequests.push({method,path:url.pathname});await route.abort();}});
  page=context.pages()[0]??await context.newPage();page.setDefaultTimeout(12000);page.on('pageerror',()=>report.pageErrorCount++);
  page.on('response',(response:any)=>{if(response.status()>=400)report.httpErrors.push({path:new URL(response.url()).pathname,status:response.status()});});
  await page.goto(origin);check('page_identity',(await page.title()).includes('Product-Agent OS'));
  await page.getByLabel(appLabel('ru','code'),{exact:true}).fill(service.pairingCode);const exchange=page.waitForResponse((response:any)=>response.url()===origin+'/api/v1/bootstrap/exchange'&&response.status()===200);
  await page.getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();csrf=(await(await exchange).json()).csrfToken;
  async function api(path:string,payload?:unknown){return page.evaluate(async({path,payload,csrf}:any)=>{const response=await fetch('/api/v1'+path,{method:payload===undefined?'GET':'POST',headers:{'content-type':'application/json','x-paos-csrf':csrf},...(payload===undefined?{}:{body:JSON.stringify(payload)})});return {status:response.status,body:await response.json()};},{path,payload,csrf});}
  async function nav(section:string){await page.locator('nav').getByRole('button',{name:uiLabel('ru',`nav.${section}` as any),exact:true}).click();}
  async function until(name:string,predicate:()=>Promise<boolean>){for(let i=0;i<80;i++){if(await predicate()){check(name,true);return;}await new Promise(resolve=>setTimeout(resolve,100));}check(name,false);}
  const projectResponse=await api('/projects',{name:'Synthetic task lifecycle',keyPrefix:'TEST',workspaceRoot:workspace});check('project_setup',projectResponse.status===201);const project=projectResponse.body;
  await page.reload();await page.locator('.navigation select:enabled').waitFor();await page.locator('.navigation select').selectOption(project.id);await nav('tasks');
  const tasks=async()=>(await api(`/projects/${project.id}/entities?kind=task`)).body.items as any[];
  const entity=async(id:string)=>(await api(`/projects/${project.id}/entities/${id}`)).body;
  const detail=()=>page.locator('.task-detail');
  async function openTask(title:string){await page.locator('.task-list .records button').filter({hasText:title}).click();await detail().waitFor();}
  async function create(title:string){await page.locator('.task-list').getByRole('button',{name:appLabel('ru','create'),exact:true}).click();const form=page.locator('.task-list form');
   await form.locator('input[name=title]').fill(title);await form.locator('textarea[name=body]').fill('Synthetic user-authored scope');await form.locator('textarea[name=criteria]').fill('Synthetic criterion is evidenced');
   await form.locator('details summary').click();await form.locator('textarea[name=files]').fill('synthetic.txt');await form.locator('input[name=estimate]').fill('60');
   await form.getByRole('button',{name:appLabel('ru','save'),exact:true}).click();await until('ui_created_'+title,async()=>(await tasks()).some(task=>task.title===title));return (await tasks()).find(task=>task.title===title)!;}
  step='create_edit';const first=await create('Lifecycle primary'),second=await create('Lifecycle linked');check('unique_stable_keys',first.publicKey==='TEST-1'&&second.publicKey==='TEST-2'&&first.id!==second.id);
  await openTask(first.title);await detail().locator('input[name=title]').fill('Lifecycle edited');await detail().locator('form').first().getByRole('button',{name:appLabel('ru','save'),exact:true}).click();
  await until('ui_edit_committed',async()=>(await entity(first.id)).title==='Lifecycle edited');
  check('title_only_edit_preserves_canonical_description',(await entity(first.id)).data.summary==='Synthetic user-authored scope');
  step='conflict';await detail().locator('input[name=title]').fill('Stale UI edit must not win');const before=await entity(first.id);
  const concurrent=await api(`/projects/${project.id}/commands`,{expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:'concurrent-writer',changes:[{expectedRevision:before.revision,entity:{...before,data:{...before.data,title:'Concurrent winning edit'},title:'Concurrent winning edit'}}]});check('distinct_api_writer_committed',concurrent.status===200);
  const conflict=page.waitForResponse((response:any)=>response.url()===origin+`/api/v1/projects/${project.id}/commands`&&response.status()===409);
  await detail().locator('form').first().getByRole('button',{name:appLabel('ru','save'),exact:true}).click();await conflict;
  await until('revision_conflict_rendered',async()=>(await detail().innerText()).includes('REVISION_CONFLICT'));
  check('conflict_preserves_winning_data',(await entity(first.id)).title==='Concurrent winning edit');check('conflict_preserves_unsaved_ui_edit',await detail().locator('input[name=title]').inputValue()==='Stale UI edit must not win');
  await page.screenshot({path:join(output,'revision-conflict.png')});report.screenshots.push('revision-conflict.png');await nav('overview');await nav('tasks');await openTask('Concurrent winning edit');
  step='comments_links_history';await detail().getByRole('button',{name:appLabel('ru','comments'),exact:true}).click();await detail().locator('textarea[name=comment]').fill('Synthetic review comment');await detail().getByRole('button',{name:appLabel('ru','comment'),exact:true}).click();
  await until('comment_rendered',async()=>(await detail().locator('.comments').innerText()).includes('Synthetic review comment'));
  await detail().getByRole('button',{name:appLabel('ru','history'),exact:true}).click();await until('history_shows_committed_revision_chain',async()=>{
   const rows=await detail().locator('pre.diff').allTextContents();const revisions=rows.flatMap((value:string)=>{try{return JSON.parse(value).revisions??[];}catch{return [];}}).filter((value:any)=>value.id===first.id).map((value:any)=>value.revision);
   return [1,2,3].every(value=>revisions.includes(value));});
  await until('history_before_after_titles_rendered',async()=>{const text=await detail().innerText();return text.includes('Lifecycle primary')&&text.includes('Lifecycle edited')&&text.includes('Concurrent winning edit');});
  check('history_actor_time_source_reason_revision_visible',(await detail().locator('time[datetime]').count())>=3
   &&(await detail().innerText()).includes('transactional_command')&&(await detail().innerText()).includes(appLabel('ru','historyActor'))
   &&(await detail().innerText()).includes(appLabel('ru','historyReason'))&&(await detail().innerText()).includes(appLabel('ru','historyNotRecorded')));
  report.historyCoverage='durable scoped field changes, actor/time/revision/correlation/source; absent original reason explicitly not recorded';
  await page.screenshot({path:join(output,'history-before-after.png')});report.screenshots.push('history-before-after.png');
  await detail().getByRole('button',{name:appLabel('ru','details'),exact:true}).click();const relations=()=>detail().locator('.task-relations');
  await relations().locator('select[name=taskId]').selectOption(second.id);await relations().locator('select[name=relation]').selectOption('related');await relations().getByRole('button',{name:appLabel('ru','addRelation'),exact:true}).click();
  await until('relation_persisted_and_rendered',async()=>{const stored=await entity(first.id);return stored.data.links.some((link:any)=>link.taskId===second.id&&link.relation==='related')&&(await relations().locator('ul').innerText()).includes('TEST-2');});
  await relations().locator('ul').getByRole('button',{name:appLabel('ru','remove'),exact:true}).click();await until('relation_remove_committed',async()=>(await entity(first.id)).data.links.length===0);
  step='manual_acceptance';await detail().locator('select:has(option[value="awaiting_acceptance"])').selectOption('awaiting_acceptance');await until('awaiting_acceptance_committed',async()=>(await entity(first.id)).status==='awaiting_acceptance');
  const acceptance=()=>detail().locator('.acceptance');check('missing_evidence_accept_disabled',await acceptance().getByRole('button',{name:appLabel('ru','accept'),exact:true}).isDisabled());
  await acceptance().locator('input[name=evidence]').fill('synthetic:missing-criterion');await acceptance().getByRole('button',{name:appLabel('ru','check'),exact:true}).click();
  await until('failed_manual_check_recorded',async()=>(await api(`/projects/${project.id}/entities?kind=comment&parentId=${first.id}`)).body.items.some((comment:any)=>comment.data.category==='manual_check'&&comment.data.outcome==='failed'));
  check('failed_check_accept_disabled',await acceptance().getByRole('button',{name:appLabel('ru','accept'),exact:true}).isDisabled());check('failed_check_not_done',(await entity(first.id)).status==='awaiting_acceptance');
  await acceptance().locator('input[name=check-0]').check();await acceptance().locator('input[name=evidence]').fill('synthetic:criterion-reviewed-by-automated-test-actor');await acceptance().getByRole('button',{name:appLabel('ru','check'),exact:true}).click();
  await until('passed_check_enables_acceptance',()=>acceptance().getByRole('button',{name:appLabel('ru','accept'),exact:true}).isEnabled());await acceptance().locator('textarea').fill('Synthetic fixture actor accepts this criterion; not human product acceptance.');
  await acceptance().getByRole('button',{name:appLabel('ru','accept'),exact:true}).click();await until('manual_acceptance_done',async()=>(await entity(first.id)).status==='done');
  await openTask('Concurrent winning edit');await detail().getByRole('button',{name:appLabel('ru','comments'),exact:true}).click();
  await until('acceptance_and_checks_visible_comments',async()=>{const text=await detail().locator('.comments').innerText();return text.includes('passed')&&text.includes('failed')&&text.includes('Synthetic fixture actor accepts');});
  await detail().locator('textarea[name=comment]').fill('Reason for reopening: synthetic follow-up verification.');await detail().getByRole('button',{name:appLabel('ru','comment'),exact:true}).click();
  await until('reopening_reason_recorded',async()=>(await detail().locator('.comments').innerText()).includes('Reason for reopening'));
  await detail().getByRole('button',{name:appLabel('ru','details'),exact:true}).click();await detail().locator('select:has(option[value="awaiting_acceptance"])').selectOption('ready');await until('task_reopened_ready',async()=>(await entity(first.id)).status==='ready');
  await page.screenshot({path:join(output,'task-reopened.png')});report.screenshots.push('task-reopened.png');
  step='draft_context';await nav('sessions');await page.getByRole('button',{name:uiLabel('ru','action.newSession'),exact:true}).click();await page.locator('.composer textarea').waitFor();
  const sessions=(await api(`/projects/${project.id}/entities?kind=session`)).body.items;check('session_created_ui',sessions.length===1);const sessionId=sessions[0].id;
  await store!.write({projectId:project.id,actorId:'synthetic-history-import',expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:'archived-transcript-setup',changes:Array.from({length:24},(_,index)=>({expectedRevision:0,entity:{id:randomUUID(),kind:'message' as const,parentId:sessionId,body:`Archived synthetic message ${index}: ${'sample '.repeat(18)}`,data:{role:index%2?'assistant':'user',coverage:'synthetic_import'}}}))});
  await until('archived_transcript_rendered',async()=>(await page.locator('.transcript').innerText()).includes('Archived synthetic message 23'));
  await page.locator('.composer textarea').fill('Synthetic draft survives source context and return.');await page.locator('.composer').getByRole('button',{name:appLabel('ru','save'),exact:true}).click();
  await until('draft_durable',async()=>(await api(`/projects/${project.id}/entities?kind=draft&parentId=${sessionId}`)).body.items.some((draft:any)=>draft.body==='Synthetic draft survives source context and return.'));
  const scrollBefore=await page.locator('.transcript').evaluate((element:HTMLElement)=>{element.scrollTop=180;element.dispatchEvent(new Event('scroll'));return element.scrollTop;});check('transcript_scroll_fixture_nonzero',scrollBefore>0);
  await page.getByRole('button',{name:appLabel('ru','context'),exact:true}).click();await page.locator('.source-row').filter({hasText:'REQUIREMENTS.md'}).getByRole('button',{name:appLabel('ru','readSource'),exact:true}).click();
  await until('source_context_read',async()=>(await page.locator('pre.diff').first().innerText()).includes('Only local task lifecycle acceptance.'));
  await page.getByRole('button',{name:appLabel('ru','chat'),exact:true}).click();await until('draft_retained_after_context_return',async()=>await page.locator('.composer textarea').inputValue()==='Synthetic draft survives source context and return.');
  await until('scroll_retained_after_context_return',async()=>Math.abs(await page.locator('.transcript').evaluate((element:HTMLElement)=>element.scrollTop)-scrollBefore)<3);
  check('no_accidental_runtime_send',(await store!.list(project.id,{kind:'run'})).length===0);
  await page.screenshot({path:join(output,'draft-context-return.png')});report.screenshots.push('draft-context-return.png');
  step='delete';await nav('tasks');await openTask('Lifecycle linked');await detail().getByRole('button',{name:appLabel('ru','remove'),exact:true}).first().click();
  await detail().locator('.confirm').getByRole('button',{name:appLabel('ru','confirmDelete'),exact:true}).click();await until('task_deleted_ui',async()=>!(await tasks()).some(task=>task.id===second.id));
  check('no_page_errors',report.pageErrorCount===0);check('route_allowlist_clean',report.blockedRequests.length===0);check('expected_http_errors_only',report.httpErrors.every((item:any)=>item.path==='/api/v1/session'&&item.status===401||item.path.endsWith('/commands')&&item.status===409));
  report.mandatoryGaps=[];report.status='passed_task_lifecycle_browser';
 }catch(error){report.status='failed';report.failedStep=step;report.error=(error as Error).message.slice(0,700);process.exitCode=1;
  try{if(page&&!page.isClosed()){await page.screenshot({path:join(output,'failed-state.png'),mask:[page.locator('input')]});report.screenshots.push('failed-state.png');report.failureUi=(await page.locator('body').innerText()).slice(0,16000);}}catch{}
 }finally{
  if(timer)clearTimeout(timer);try{await context?.close();}catch{report.status='failed';report.browserCleanupFailed=true;process.exitCode=1;}
  try{await service?.quit();report.serviceClosed=true;}catch{report.status='failed';report.serviceCleanupFailed=true;process.exitCode=1;}
  if(report.serviceClosed)try{await rm(fixture,{recursive:true,force:true});report.fixtureCleaned=true;}catch{report.fixtureCleaned=false;report.status='failed';process.exitCode=1;}
  else{report.fixtureCleaned=false;report.fixtureRetained=fixture;}
  report.finishedAt=new Date().toISOString();await writeFile(join(output,'task-lifecycle-result.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({status:report.status,checks:report.checks.length,failedStep:report.failedStep,error:report.error,fixtureCleaned:report.fixtureCleaned,report:join(output,'task-lifecycle-result.json')}));
 }
}
if(process.argv[1]&&fileURLToPath(import.meta.url)===fileURLToPath(pathToFileURL(process.argv[1])))await main(process.argv.slice(2));
