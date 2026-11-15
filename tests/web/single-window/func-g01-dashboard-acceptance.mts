import {mkdtemp,mkdir,writeFile,readFile,readdir,rm} from 'node:fs/promises';
import {resolve,join,dirname,isAbsolute} from 'node:path';
import {pathToFileURL} from 'node:url';
import {randomUUID,createHash} from 'node:crypto';
import {startLocalService} from '../../../apps/local-service/src/main.mts';
import {newM2Task} from '../../../packages/contracts/issues/task-profile.ts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';
import {uiLabel} from '../../../apps/web/src/locales/messages.ts';

// Real service/UI; only failed reads, deterministic timestamps and queue entries are synthetic HTTP fixtures.
const argv=process.argv.slice(2);
if(argv[0]!=='--synthetic-browser'||argv.length%2!==1)throw Error('EXPLICIT_SYNTHETIC_BROWSER_REQUIRED');
const args=Object.fromEntries(Array.from({length:(argv.length-1)/2},(_,i)=>argv.slice(1+i*2,3+i*2)));
for(const key of ['--playwright-core','--chromium'])if(!isAbsolute(args[key]??''))throw Error('INSTALLED_PATH_REQUIRED');
const scratch=resolve('.tmp/func-g01-dashboard');await mkdir(scratch,{recursive:true});
const fixture=await mkdtemp(join(scratch,'fixture-')),output=await mkdtemp(join(scratch,'evidence-'));
const workspace=join(fixture,'workspace'),otherRoot=join(fixture,'other'),profile=join(fixture,'profile'),home=join(fixture,'browser');
await Promise.all([workspace,otherRoot,profile,home].map(p=>mkdir(p)));
const report:any={startedAt:new Date().toISOString(),syntheticOnly:true,providerCalls:false,realCredentials:false,browserPlugin:'not_available',checks:[],pageErrors:[],consoleErrors:[],screenshots:[],externalRequests:[]};
const check=(name:string,passed:boolean,detail?:unknown)=>report.checks.push({name,passed,...(detail===undefined?{}:{detail})});
let service:any,context:any,page:any,timer:any,csrf='',locale:'ru'|'en'='ru',stage='setup';
try{
 service=await startLocalService({profileDirectory:profile,instanceId:randomUUID(),appCodexHome:join(fixture,'codex-home')},{assetRoots:[]});
 const origin='http://127.0.0.1:'+service.port;report.origin=origin;
 const {chromium}=await import(pathToFileURL(join(args['--playwright-core'],'index.mjs')).href);
 context=await chromium.launchPersistentContext(home,{headless:true,chromiumSandbox:true,serviceWorkers:'block',viewport:{width:1440,height:1000},executablePath:args['--chromium'],env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:home,HOME:home,APPDATA:home,LOCALAPPDATA:home,TEMP:home,TMP:home}});
 timer=setTimeout(()=>void context?.close(),180000);
 await context.route('**/*',async(route:any)=>{if(new URL(route.request().url()).origin===origin)await route.continue();else{report.externalRequests.push(new URL(route.request().url()).origin);await route.abort();}});
 page=context.pages()[0];page.setDefaultTimeout(12000);page.on('pageerror',(e:Error)=>report.pageErrors.push(e.message));page.on('console',(msg:any)=>{if(msg.type()==='error')report.consoleErrors.push(msg.text());});
 await page.goto(origin);check('page_identity',page.url().startsWith(origin)&&(await page.title()).includes('Product-Agent OS'));check('not_blank',(await page.locator('body').innerText()).includes('Product-Agent OS'));check('no_framework_overlay',await page.locator('vite-error-overlay').count()===0);
 await page.getByLabel(appLabel('ru','code'),{exact:true}).fill(service.pairingCode);
 const paired=page.waitForResponse((r:any)=>r.url().endsWith('/bootstrap/exchange')&&r.status()===200);
 await page.getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();csrf=(await(await paired).json()).csrfToken;
 // The unauthenticated initial bootstrap probe is an expected 401; evaluate console health after pairing.
 report.bootstrapConsoleErrors=[...report.consoleErrors];report.consoleErrors=[];
 async function api(path:string,input?:unknown){return page.evaluate(async({path,input,csrf}:any)=>{const r=await fetch('/api/v1'+path,{method:input===undefined?'GET':'POST',headers:{'content-type':'application/json','x-paos-csrf':csrf},...(input===undefined?{}:{body:JSON.stringify(input)})});return{status:r.status,body:await r.json()};},{path,input,csrf});}
 async function nav(id:string){await page.locator('.navigation nav').getByRole('button',{name:id==='portfolio'?(locale==='ru'?'Все проекты':'All projects'):uiLabel(locale,('nav.'+id) as any),exact:true}).click();}
 const dashboard=()=>page.getByTestId('project-dashboard');
 async function settled(){await dashboard().getByRole('button',{name:locale==='ru'?'Обновить дашборд':'Refresh dashboard',exact:true}).waitFor();await page.waitForFunction(()=>{const b=document.querySelector('[data-testid=project-dashboard] .dashboard-scope>button') as HTMLButtonElement|null;return b&&!b.disabled;});}
 async function refresh(){await dashboard().getByRole('button',{name:locale==='ru'?'Обновить дашборд':'Refresh dashboard',exact:true}).click();await settled();}
 async function shot(name:string){const path=join(output,name+'.png');await page.screenshot({path,animations:'disabled'});report.screenshots.push(path);}
 const project=(await api('/projects',{name:'Dashboard synthetic',workspaceRoot:workspace,keyPrefix:'DASH'})).body;
 const other=(await api('/projects',{name:'Unavailable synthetic',workspaceRoot:otherRoot,keyPrefix:'OTHR'})).body;
 const ids=['11111111-1111-4111-8111-111111111111','22222222-2222-4222-8222-222222222222','33333333-3333-4333-8333-333333333333','44444444-4444-4444-8444-444444444444'];
 const titles=['Newest','Second','Third','Oldest'];const times=new Map(ids.map((id,i)=>[id,`2026-11-${String(14-i).padStart(2,'0')}T12:00:00Z`]));
 const save=async(task:any,revision=0)=>api('/projects/'+project.id+'/task-manager/commands',{action:'save',task,expectedRevision:revision,expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:randomUUID()});
 for(let i=0;i<ids.length;i++){const reply=await save(newM2Task(project.id,ids[i],titles[i],'local-user'));if(reply.status!==200)throw Error('TASK_SETUP_'+JSON.stringify(reply));}
 let failure:'partial'|'all'|'none'='partial',reordered=false,hold:Promise<void>|undefined,release:(()=>void)|undefined;
 await context.route('**/api/v1/projects/*/task-manager',async(route:any)=>{
  if(hold)await hold;
  const id=new URL(route.request().url()).pathname.split('/')[4];
  if(failure==='all'||failure==='partial'&&id===other.id){await route.fulfill({status:503,contentType:'application/json',body:JSON.stringify({error:{code:'SYNTHETIC_UNAVAILABLE'}})});return;}
  const response=await route.fetch(),body=await response.json();body.tasks=body.tasks.toSorted((a:any,b:any)=>a.id.localeCompare(b.id)).map((t:any)=>({...t,updatedAt:times.get(t.id)}));await route.fulfill({response,json:body});
 });
 await context.route('**/api/v1/projects/*/scheduler',async(route:any)=>{
  const response=await route.fetch(),body=await response.json();
  const order=reordered?[1,0,2]:[0,1,2];body.items=order.map((i:number,index:number)=>({id:'queue-'+i,taskId:ids[i],taskKey:'DASH-'+(i+1),taskTitle:titles[i],revision:1,state:'queued',position:i===2?null:index+1,workflow:{id:'default',version:1},recipeId:'synthetic',sessionId:'fixture',steps:[],claims:[],ownershipScope:'entire_workspace',executionId:null,executionState:null,waitReasons:[],createdAt:1,updatedAt:1}));body.order=order.slice(0,2).map(i=>'queue-'+i);await route.fulfill({response,json:body});
 });
 await page.reload();await page.locator('.navigation select:enabled').waitFor();await page.locator('.navigation select').selectOption(project.id);
 for(const lang of ['ru','en'] as const){
  stage='portfolio_'+lang;
  if(locale!==lang){await nav('settings');await page.locator('[data-settings-section=general]').click();await page.getByLabel(uiLabel(locale,'preferences.language'),{exact:true}).selectOption(lang);await page.getByRole('button',{name:uiLabel(locale,'preferences.save'),exact:true}).click();await page.waitForFunction((l:string)=>document.documentElement.lang===l,lang);locale=lang;}
  failure='partial';await nav('portfolio');await settled();
  let summary=await dashboard().locator('.dashboard-progress-summary').innerText();
  check(lang+'_partial_coverage_next_to_totals',lang==='ru'?/1 из 2.*данные неполные/is.test(summary):/1 of 2.*incomplete/is.test(summary),summary);
  check(lang+'_progress_available_subset',lang==='ru'?summary.includes('доступным проектам'):summary.includes('available projects'),summary);
  check(lang+'_failed_project_unknown',await dashboard().locator('.ui-project-row').filter({hasText:'Unavailable synthetic'}).innerText().then((s:string)=>s.includes('—')));
  await shot(lang+'-partial');
  failure='all';await refresh();summary=await dashboard().locator('.dashboard-progress-summary').innerText();check(lang+'_all_failed_unknown',summary.includes('—')&&!await dashboard().locator('progress').count()&&(lang==='ru'?summary.includes('0 из 2'):summary.includes('0 of 2')),summary);
  failure='none';await refresh();summary=await dashboard().locator('.dashboard-progress-summary').innerText();check(lang+'_retry_restores_complete',lang==='ru'?summary.includes('2 из 2'):summary.includes('2 of 2'),summary);
  hold=new Promise<void>(r=>release=r);const refreshing=dashboard().getByRole('button',{name:lang==='ru'?'Обновить дашборд':'Refresh dashboard',exact:true});await refreshing.click();await page.waitForFunction(()=>!!(document.querySelector('.dashboard-scope>button') as HTMLButtonElement)?.disabled);summary=await dashboard().locator('.dashboard-progress-summary').innerText();check(lang+'_loading_expected_count',lang==='ru'?summary.includes('0 из 2'):summary.includes('0 of 2'),summary);release!();hold=undefined;await settled();
 }
 stage='queue_recent';await nav('overview');await settled();
 let queueRows=await dashboard().locator('.dashboard-queue-row').allTextContents();check('queue_positions_one_based',queueRows[0].includes('#1')&&queueRows[1].includes('#2'),queueRows);check('null_position_omitted',!queueRows[2].includes('#'),queueRows[2]);
 let recent=await dashboard().locator('.dashboard-recent li strong').allTextContents();check('recent_sorted_by_updatedAt',JSON.stringify(recent)===JSON.stringify(titles.slice(0,3)),recent);
 reordered=true;await refresh();queueRows=await dashboard().locator('.dashboard-queue-row').allTextContents();check('queue_reorder_preserves_positions',queueRows[0].includes('Second')&&queueRows[0].includes('#1')&&queueRows[1].includes('Newest')&&queueRows[1].includes('#2'),queueRows);
 await nav('settings');await page.locator('[data-settings-section=queue]').click();await page.getByTestId('queue-entry').first().waitFor();const queueHeadings=await page.getByTestId('queue-entry').locator('h3').allTextContents();check('queue_manager_same_positions',queueHeadings[0].startsWith('1 · DASH-2')&&queueHeadings[1].startsWith('2 · DASH-1'),queueHeadings);
 await nav('overview');await settled();
 const latestId='55555555-5555-4555-8555-555555555555';times.set(latestId,'2026-11-15T13:00:00Z');await save(newM2Task(project.id,latestId,'Created latest','local-user'));await refresh();recent=await dashboard().locator('.dashboard-recent li strong').allTextContents();check('recent_creation_after_refresh',recent[0]==='Created latest'&&recent[1]==='Newest',recent);
 const snap=(await api('/projects/'+project.id+'/task-manager')).body,old=snap.tasks.find((t:any)=>t.id===ids[3]);times.set(old.id,'2026-11-15T14:00:00Z');await save({...old.data,title:'Updated latest'},old.revision);await refresh();recent=await dashboard().locator('.dashboard-recent li strong').allTextContents();check('recent_edit_after_refresh',recent[0]==='Updated latest'&&recent[1]==='Created latest',recent);
 const note=await dashboard().locator('.dashboard-recent').innerText();check('recent_timestamp_semantics_label',note.includes('updatedAt'),note);await shot('en-dashboard');
 check('desktop_no_page_overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 await page.setViewportSize({width:390,height:844});await shot('en-dashboard-mobile');check('mobile_no_page_overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 check('mobile_totals_remain_readable',await dashboard().locator('.dashboard-progress-summary>span').evaluateAll((items:Element[])=>items.every(el=>el.getBoundingClientRect().height<=48)));
 check('mobile_main_column_remains_readable',await dashboard().locator('.dashboard-main').evaluate((el:Element)=>el.getBoundingClientRect().width>=280));
 check('no_page_errors',report.pageErrors.length===0,report.pageErrors);check('no_unexpected_console_errors',report.consoleErrors.every((s:string)=>s.includes('503')),report.consoleErrors);check('no_external_requests',report.externalRequests.length===0);
 report.status=report.checks.every((c:any)=>c.passed)?'passed':'failed';if(report.status==='failed')process.exitCode=1;
}catch(error){report.status='failed';report.failedStage=stage;report.error=String(error);process.exitCode=1;try{await page.screenshot({path:join(output,'failed.png')});}catch{}}
finally{
 if(timer)clearTimeout(timer);await context?.close();await service?.quit();
 if(dirname(resolve(fixture))!==scratch)throw Error('CLEANUP_BOUNDARY');await rm(fixture,{recursive:true,force:true});report.fixtureCleaned=true;report.finishedAt=new Date().toISOString();report.sourceHashes={};
 for(const path of ['tests/web/single-window/func-g01-dashboard-acceptance.mts','apps/web/src/features/dashboard/Dashboard.tsx','apps/web/src/features/dashboard/model.ts','apps/web/dist/index.html',...(await readdir('apps/web/dist/assets')).map(n=>'apps/web/dist/assets/'+n)])report.sourceHashes[path]=createHash('sha256').update(await readFile(path)).digest('hex');
 await writeFile(join(output,'result.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,checks:report.checks.length,failed:report.checks.filter((c:any)=>!c.passed).map((c:any)=>c.name),error:report.error,report:join(output,'result.json')}));
}
