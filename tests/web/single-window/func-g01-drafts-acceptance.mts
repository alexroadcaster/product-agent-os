import {mkdtemp,mkdir,writeFile,readFile,rm,readdir} from 'node:fs/promises';
import {resolve,join,dirname,isAbsolute} from 'node:path';
import {pathToFileURL} from 'node:url';
import {randomUUID,createHash} from 'node:crypto';
import {startLocalService} from '../../../apps/local-service/src/main.mts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';
import {uiLabel} from '../../../apps/web/src/locales/messages.ts';
import {label} from '../../../apps/web/src/features/tasks/labels.ts';

/** Production UI/HTTP/SQLite against disposable projects; no provider, OS vault or existing profile. */
const argv=process.argv.slice(2);
if(argv.length!==5||argv[0]!=='--synthetic-browser')throw Error('EXPLICIT_SYNTHETIC_BROWSER_REQUIRED');
const args=Object.fromEntries([argv.slice(1,3),argv.slice(3,5)]);
if(!['--playwright-core','--chromium'].every(k=>isAbsolute(args[k]??'')))throw Error('INSTALLED_BROWSER_PATHS_REQUIRED');
const scratch=resolve('.tmp/func-g01-drafts');await mkdir(scratch,{recursive:true});
const fixture=await mkdtemp(join(scratch,'fixture-')),output=await mkdtemp(join(scratch,'evidence-'));
const profile=join(fixture,'profile'),home=join(fixture,'browser'),workspace=join(fixture,'workspace'),otherRoot=join(fixture,'other');
await Promise.all([mkdir(profile),mkdir(home),mkdir(workspace),mkdir(otherRoot)]);
const report:any={startedAt:new Date().toISOString(),syntheticOnly:true,providerCalls:false,realCredentials:false,browserPlugin:'not_available',checks:[],pageErrors:[],consoleErrors:[],screenshots:[],sourceHashes:{}};
let service:any,context:any,page:any,timer:any,csrf='',step='setup';
const check=(name:string,passed:boolean,detail?:unknown)=>{report.checks.push({name,passed,...(detail===undefined?{}:{detail})});};
const required=(name:string,passed:boolean)=>{check(name,passed);if(!passed)throw Error(name);};
try{
 service=await startLocalService({profileDirectory:profile,instanceId:randomUUID(),appCodexHome:join(fixture,'codex-home')},{assetRoots:[]});
 const origin='http://127.0.0.1:'+service.port;report.origin=origin;
 const {chromium}=await import(pathToFileURL(join(args['--playwright-core'],'index.mjs')).href);
 context=await chromium.launchPersistentContext(home,{headless:true,chromiumSandbox:true,serviceWorkers:'block',viewport:{width:1440,height:1000},executablePath:args['--chromium'],env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:home,HOME:home,APPDATA:home,LOCALAPPDATA:home,TEMP:home,TMP:home}});
 timer=setTimeout(()=>void context?.close(),240000);
 await context.route('**/*',async(route:any)=>{if(new URL(route.request().url()).origin!==origin){check('no_external_requests',false);await route.abort();}else await route.continue();});
 page=context.pages()[0];page.setDefaultTimeout(12000);page.on('pageerror',(e:Error)=>report.pageErrors.push(e.message));page.on('console',(e:any)=>{if(e.type()==='error')report.consoleErrors.push(e.text());});
 await page.goto(origin);check('page_identity',page.url()===origin+'/'&&(await page.title()).includes('Product-Agent OS'));
 await page.getByLabel(appLabel('ru','code'),{exact:true}).fill(service.pairingCode);
 const paired=page.waitForResponse((r:any)=>r.url().endsWith('/bootstrap/exchange')&&r.status()===200);
 await page.getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();csrf=(await(await paired).json()).csrfToken;
 async function api(path:string,input?:any){return page.evaluate(async({path,input,csrf}:any)=>{const r=await fetch('/api/v1'+path,{method:input===undefined?'GET':'POST',headers:{'content-type':'application/json','x-paos-csrf':csrf},...(input===undefined?{}:{body:JSON.stringify(input)})});return {status:r.status,body:await r.json()};},{path,input,csrf});}
 async function until(name:string,fn:()=>Promise<boolean>){const end=Date.now()+15000;while(Date.now()<end){if(await fn()){check(name,true);return;}await new Promise(r=>setTimeout(r,75));}throw Error(name);}
 async function shot(name:string){const path=join(output,name);await page.screenshot({path,fullPage:false});report.screenshots.push(path);}
 async function nav(key:string){const menu=page.getByRole('button',{name:appLabel('ru','menu'),exact:true});if(await menu.isVisible()&&await menu.getAttribute('aria-expanded')!=='true')await menu.click();await page.locator('nav').getByRole('button',{name:uiLabel('ru',('nav.'+key) as any),exact:true}).click();if(key==='settings')await page.locator('[data-settings-section=processes]').click();}
 const created=await api('/projects',{name:'FUNC drafts',workspaceRoot:workspace,keyPrefix:'DFTS'}),other=await api('/projects',{name:'Other drafts',workspaceRoot:otherRoot,keyPrefix:'OTHR'});
 required('projects_created',created.status===201&&other.status===201);const project=created.body,base='/projects/'+project.id;
 const snap=async()=>(await api(base+'/task-manager')).body;
 const cmd=async(input:any)=>api(base+'/task-manager/commands',{...input,expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:randomUUID()});
 await page.reload();await page.locator('.navigation select:enabled').waitFor();await page.locator('.navigation select').selectOption(project.id);
 step='task_reset';await nav('tasks');const manager=page.getByTestId('task-manager');
 await manager.getByRole('button',{name:label('ru','create'),exact:true}).click();let editor=page.locator('.task-list').getByTestId('task-editor');
 await editor.locator('[name=title]').fill('Discarded title');await editor.locator('[name=criteria]').fill('Discarded criterion');await editor.locator('[name=reason]').fill('Discarded reason');
 await editor.locator('.task-risks>summary').click();await editor.locator('[name=risks]').fill('Discarded risk');
 await editor.locator('details:has(textarea[name=artifacts])>summary').click();await editor.locator('[name=artifacts]').fill('discarded.md');
 await editor.locator('[name=estimate]').fill('invalid');await editor.getByRole('button',{name:label('ru','save'),exact:true}).click();
 await until('invalid_estimate_error_visible',async()=>Boolean((await editor.locator('[role=alert]').innerText()).trim()));
 await editor.getByRole('button',{name:label('ru','discard'),exact:true}).click();
 for(const name of ['title','criteria','risks','artifacts','estimate','reason'])check('discard_clears_'+name,await editor.locator('[name='+name+']').inputValue()==='');
 check('discard_clears_error',!(await editor.locator('[role=alert]').innerText()).trim());check('discard_clears_dirty',await editor.getByText(label('ru','unsaved'),{exact:true}).count()===0);
 await shot('task-discard.png');
 await editor.locator('[name=title]').fill('After discard');await editor.locator('[name=criteria]').fill('Fresh criterion');await editor.getByRole('button',{name:label('ru','save'),exact:true}).click();
 await until('post_discard_task_saved',async()=>(await snap()).tasks.some((t:any)=>t.title==='After discard'));
 let saved=(await snap()).tasks.find((t:any)=>t.title==='After discard');check('discarded_values_not_saved',saved.data.acceptanceCriteria.join()==='Fresh criterion'&&!saved.data.risks.length&&!saved.data.artifactReferences.length&&saved.data.estimateSeconds===null);
 step='task_revision';await manager.locator('[data-task-id="'+saved.id+'"]').first().click();const detail=page.getByTestId('task-detail');await detail.getByRole('button',{name:'Открыть полностью',exact:true}).click();editor=detail.getByTestId('task-editor');
 await editor.locator('[name=title]').fill('Unsaved local title');const external={...saved.data,title:'Concurrent title',acceptanceCriteria:['Concurrent criterion']};
 required('concurrent_task_save',(await cmd({action:'save',task:external,expectedRevision:saved.revision,reason:'Synthetic second writer'})).status===200);
 await detail.getByRole('button',{name:label('ru','close'),exact:true}).click();await manager.getByRole('button',{name:label('ru','refresh'),exact:true}).click();await until('task_refresh_complete',async()=>!(await manager.getAttribute('aria-busy')==='true')&&(await manager.locator('[data-task-id="'+saved.id+'"]').first().innerText()).includes('Concurrent title'));await manager.locator('[data-task-id="'+saved.id+'"]').first().click();await detail.getByRole('button',{name:'Открыть полностью',exact:true}).click();
 check('dirty_task_preserved_after_refresh',await editor.locator('[name=title]').inputValue()==='Unsaved local title');
 await editor.getByRole('button',{name:label('ru','save'),exact:true}).click();await until('stale_task_save_error_visible',async()=>Boolean((await editor.locator('[role=alert]').innerText()).trim()));
 check('stale_task_save_keeps_input',await editor.locator('[name=title]').inputValue()==='Unsaved local title');
 await editor.getByRole('button',{name:label('ru','discard'),exact:true}).click();check('existing_discard_adopts_server_title',await editor.locator('[name=title]').inputValue()==='Concurrent title');check('existing_discard_adopts_server_criteria',await editor.locator('[name=criteria]').inputValue()==='Concurrent criterion');
 await editor.locator('[name=title]').fill('After current revision');await editor.getByRole('button',{name:label('ru','save'),exact:true}).click();await until('discard_adopts_current_cas_revision',async()=>(await snap()).tasks.find((t:any)=>t.id===saved.id).title==='After current revision');
 await detail.getByRole('button',{name:label('ru','close'),exact:true}).click();
 step='workflow_setup';let state=await snap(),definition=structuredClone(state.workflows.workflows[0].versions[0].definition);definition.name='Alternative';
 required('alternative_workflow_draft',(await cmd({action:'workflow-save-draft',workflowId:'alternative',definition,expectedRevision:state.settingsRevisions.workflows})).status===200);
 state=await snap();let preview=(await cmd({action:'workflow-publish-preview',workflowId:'alternative',expectedRevision:state.settingsRevisions.workflows})).body;
 required('alternative_workflow_published',(await cmd({action:'workflow-publish',workflowId:'alternative',previewDigest:preview.previewDigest,expectedRevision:state.settingsRevisions.workflows})).status===200);
 await nav('settings');let workflow=page.getByTestId('workflow-manager');await workflow.locator('[data-workflow-section=assignments]').click();await workflow.locator('[name=workflow-type-task]').selectOption('alternative');
 await nav('tasks');await nav('settings');await workflow.locator('[data-workflow-section=assignments]').click();
 check('mapping_survives_navigation',await workflow.locator('[name=workflow-type-task]').inputValue()==='alternative');
 check('mapping_dirty_visible_after_navigation',(await workflow.innerText()).includes(label('ru','unsaved')));
 // Restore the expected pending value after the RED oracle so subsequent distinct cases still execute.
 await workflow.locator('[name=workflow-type-task]').selectOption('alternative');
 await workflow.locator('[name=workflow-default]').selectOption('alternative');await until('default_workflow_saved',async()=>(await snap()).workflows.defaultWorkflowId==='alternative');
 check('default_change_preserves_mapping_draft',await workflow.locator('[name=workflow-type-task]').inputValue()==='alternative');
 await workflow.getByRole('button',{name:'Сохранить назначения',exact:true}).click();await until('mapping_saved',async()=>(await snap()).workflows.typeMapping.task==='alternative');
 await until('mapping_save_clears_dirty',async()=>!(await workflow.innerText()).includes(label('ru','unsaved')));
 step='workflow_conflict';await workflow.locator('[name=workflow-type-bug]').selectOption('alternative');const beforeConflict=(await snap()).settingsRevisions.workflows;
 required('concurrent_workflow_assignment',(await cmd({action:'workflow-assign',defaultWorkflowId:'default',expectedRevision:beforeConflict})).status===200);
 await workflow.getByRole('button',{name:label('ru','refresh'),exact:true}).click();
 await until('workflow_refreshed',async()=>await workflow.locator('[name=workflow-default]').inputValue()==='default');
 await workflow.getByRole('button',{name:'Сохранить назначения',exact:true}).click();
 await until('stale_mapping_save_settled',async()=>Boolean((await workflow.locator('[role=alert]').innerText()).trim())||(await snap()).workflows.typeMapping.bug==='alternative');
 check('stale_mapping_conflict_visible',Boolean((await workflow.locator('[role=alert]').innerText()).trim()));check('stale_mapping_not_applied',(await snap()).workflows.typeMapping.bug!=='alternative');check('stale_mapping_input_preserved',await workflow.locator('[name=workflow-type-bug]').inputValue()==='alternative');
 await page.locator('.navigation select').selectOption(other.body.id);await page.getByTestId('workflow-manager').locator('[data-workflow-section=assignments]').click();
 check('mapping_does_not_cross_project',await page.getByTestId('workflow-manager').locator('[name=workflow-type-bug]').inputValue()==='');
 await page.locator('.navigation select').selectOption(project.id);workflow=page.getByTestId('workflow-manager');await workflow.locator('[data-workflow-section=assignments]').click();check('mapping_restored_to_original_project',await workflow.locator('[name=workflow-type-bug]').inputValue()==='alternative');
 const discard=workflow.getByRole('button',{name:'Отменить назначения',exact:true});check('mapping_has_explicit_discard',await discard.count()===1);
 if(await discard.count()){await discard.click();check('mapping_discard_adopts_server',await workflow.locator('[name=workflow-type-bug]').inputValue()==='');check('mapping_discard_clears_error',!(await workflow.locator('[role=alert]').innerText()).trim());check('mapping_discard_clears_dirty',!(await workflow.innerText()).includes(label('ru','unsaved')));await workflow.locator('[name=workflow-type-bug]').selectOption('alternative');await workflow.getByRole('button',{name:'Сохранить назначения',exact:true}).click();await until('mapping_discard_adopts_current_revision',async()=>(await snap()).workflows.typeMapping.bug==='alternative'&&await workflow.locator('[name=workflow-type-bug]').isEnabled()&&!(await workflow.innerText()).includes(label('ru','unsaved')));}
 step='workflow_default_ack_race';await workflow.locator('[name=workflow-type-sub_task]').selectOption('alternative');let inserted=false;
 const commandPattern='**/projects/'+project.id+'/task-manager/commands';
 const interleave=async(route:any)=>{const input=route.request().postDataJSON();if(inserted||input.action!=='workflow-assign'||input.defaultWorkflowId!=='alternative'){await route.continue();return;}inserted=true;const response=await route.fetch();const current=await snap();required('interleaved_mapping_write',(await cmd({action:'workflow-assign',typeMapping:{...current.workflows.typeMapping,epic:'alternative'},expectedRevision:current.settingsRevisions.workflows})).status===200);await route.fulfill({response});};
 await context.route(commandPattern,interleave);await workflow.locator('[name=workflow-default]').selectOption('alternative');await until('interleaved_default_ack_received',async()=>inserted&&await workflow.locator('[name=workflow-default]').inputValue()==='alternative'&&await workflow.locator('[name=workflow-default]').isEnabled());await context.unroute(commandPattern,interleave);
 await workflow.getByRole('button',{name:'Сохранить назначения',exact:true}).click();await until('interleaved_mapping_save_settled',async()=>Boolean((await workflow.locator('[role=alert]').innerText()).trim())||(await snap()).workflows.typeMapping.sub_task==='alternative');
 check('default_ack_does_not_adopt_other_writer_revision',Boolean((await workflow.locator('[role=alert]').innerText()).trim()));check('interleaved_mapping_not_overwritten',(await snap()).workflows.typeMapping.epic==='alternative');const retained=await workflow.locator('[name=workflow-type-sub_task]').inputValue();check('interleaved_mapping_input_retained',retained==='alternative',{input:retained,server:(await snap()).workflows.typeMapping,error:await workflow.locator('[role=alert]').innerText(),dirty:(await workflow.innerText()).includes(label('ru','unsaved'))});
 if(await discard.count()&&await discard.isEnabled())await discard.click();await shot('workflow-assignments.png');
 step='workflow_late_project_response';await nav('tasks');let releaseOld:()=>void=()=>{},oldRequested:()=>void=()=>{};
 const held=new Promise<void>(r=>{releaseOld=r;}),requested=new Promise<void>(r=>{oldRequested=r;});
 const oldPattern='**/projects/'+project.id+'/task-manager';
 const delayOld=async(route:any)=>{const response=await route.fetch();oldRequested();await held;await route.fulfill({response});};
 await context.route(oldPattern,delayOld);await nav('settings');await requested;
 await page.locator('.navigation select').selectOption(other.body.id);workflow=page.getByTestId('workflow-manager');await workflow.locator('[data-workflow-section=assignments]').click();await workflow.locator('[name=workflow-type-bug]').waitFor();const oldResponse=page.waitForResponse((r:any)=>r.url()===origin+'/api/v1'+base+'/task-manager');releaseOld();await(await oldResponse).finished();await page.evaluate(()=>new Promise<void>(r=>requestAnimationFrame(()=>r())));await context.unroute(oldPattern,delayOld);
 check('late_project_snapshot_ignored',await workflow.locator('[name=workflow-type-bug]').inputValue()===''&&await workflow.locator('[name=workflow-default]').inputValue()==='default');
 await page.setViewportSize({width:390,height:844});await shot('workflow-assignments-mobile.png');check('mobile_no_page_overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 check('nonblank_app',(await page.locator('main').innerText()).length>100);check('no_framework_overlay',await page.locator('vite-error-overlay').count()===0);check('no_page_errors',report.pageErrors.length===0,report.pageErrors);
 // 409 is intentional evidence of concurrency rejection, not a browser runtime failure.
 check('no_unexpected_console_errors',report.consoleErrors.every((message:string)=>message.includes('409')||message.includes('401')),report.consoleErrors);
 report.status=report.checks.every((c:any)=>c.passed)?'passed':'failed';if(report.status==='failed')process.exitCode=1;
}catch(error){report.status='failed';report.failedStep=step;report.error=String(error);process.exitCode=1;try{await shotFailure();}catch{}}
finally{
 if(timer)clearTimeout(timer);await context?.close();await service?.quit();if(dirname(resolve(fixture))!==scratch)throw Error('CLEANUP_BOUNDARY');await rm(fixture,{recursive:true,force:true});report.fixtureCleaned=true;report.finishedAt=new Date().toISOString();
 for(const p of ['tests/web/single-window/func-g01-drafts-acceptance.mts','apps/web/src/features/tasks/Editor.tsx','apps/web/src/features/workflows/WorkflowManager.tsx','apps/web/dist/index.html',...(await readdir('apps/web/dist/assets')).map(n=>'apps/web/dist/assets/'+n)])report.sourceHashes[p]=createHash('sha256').update(await readFile(p)).digest('hex');
 await writeFile(join(output,'result.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,checks:report.checks.length,failed:report.checks.filter((c:any)=>!c.passed).map((c:any)=>c.name),error:report.error,failedStep:report.failedStep,report:join(output,'result.json')}));
}
async function shotFailure(){const path=join(output,'failed.png');await page.screenshot({path,fullPage:false});report.screenshots.push(path);report.failureUi=(await page.locator('body').innerText()).slice(0,18000);}
