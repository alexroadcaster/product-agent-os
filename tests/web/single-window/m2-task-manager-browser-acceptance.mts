import {mkdtemp,mkdir,writeFile,readFile,rm,readdir} from 'node:fs/promises';
import {resolve,join,dirname,isAbsolute} from 'node:path';
import {pathToFileURL} from 'node:url';
import {randomUUID,createHash} from 'node:crypto';
import {startLocalService} from '../../../apps/local-service/src/main.mts';
import {openLocalStore,type LocalStore} from '../../../apps/local-service/src/storage/local-store.mts';
import {newTask} from '../../../apps/web/src/api/task.ts';
import {label as word,type Locale} from '../../../apps/web/src/features/tasks/labels.ts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';
import {uiLabel} from '../../../apps/web/src/locales/messages.ts';

/** Real built UI and local HTTP/SQLite; disposable data, no provider/auth-cache/OS credential use. */
async function main(){
 const argv=process.argv.slice(2);
 if(![5,7].includes(argv.length)||argv[0]!=='--synthetic-browser')throw Error('EXPLICIT_SYNTHETIC_BROWSER_REQUIRED');
 const args=Object.fromEntries([argv.slice(1,3),argv.slice(3,5)]);
 const scenario=argv.length===7&&argv[5]==='--scenario'?argv[6]:'full';if(!['full','settings-cas','markdown'].includes(scenario))throw Error('INVALID_SCENARIO');
 if(!['--playwright-core','--chromium'].every(k=>isAbsolute(args[k]??'')))throw Error('INSTALLED_BROWSER_PATHS_REQUIRED');
 const scratch=resolve('.tmp/paos-m2');await mkdir(scratch,{recursive:true});
 const fixture=await mkdtemp(join(scratch,'browser-fixture-')),output=await mkdtemp(join(scratch,'browser-evidence-'));
 const workspace=join(fixture,'workspace'),profile=join(fixture,'profile'),home=join(fixture,'browser');
 await Promise.all([mkdir(workspace),mkdir(profile),mkdir(home)]);await writeFile(join(workspace,'a.txt'),'Synthetic M2 source\n');
 const sourceHash=createHash('sha256').update('Synthetic M2 source\n').digest('hex');
 const report:any={scenario,startedAt:new Date().toISOString(),syntheticOnly:true,actualAppAgent:false,providerCalls:false,apiKey:false,osCredentials:false,browserPlugin:'not_available',checks:[],screenshots:[],pageErrors:[],consoleErrors:[],httpErrors:[],blockedRequests:[],sourceHashes:{},nonUiSetup:['project registration','one legacy M1 fixture','one concurrent writer']};
 let service:Awaited<ReturnType<typeof startLocalService>>|undefined,store:LocalStore|undefined,context:any,page:any,timer:ReturnType<typeof setTimeout>|undefined,csrf='',step='setup',locale:Locale='ru';
 const check=(name:string,passed:boolean,detail?:unknown)=>{report.checks.push({name,passed,...(detail===undefined?{}:{detail})});if(!passed)throw Error(name);};
 try{
  service=await startLocalService({profileDirectory:profile,instanceId:randomUUID()},{openStore:async options=>{store=await openLocalStore(options);return store;}});
  const origin='http://127.0.0.1:'+service.port;report.origin=origin;
  const {chromium}=await import(pathToFileURL(join(args['--playwright-core'],'index.mjs')).href);
  context=await chromium.launchPersistentContext(home,{headless:true,chromiumSandbox:true,serviceWorkers:'block',viewport:{width:1440,height:1000},locale:'ru-RU',executablePath:args['--chromium'],timeout:20000,env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:home,HOME:home,APPDATA:home,LOCALAPPDATA:home,TEMP:home,TMP:home}});
  timer=setTimeout(()=>void context?.close(),240000);
  await context.route('**/*',async(route:any)=>{const r=route.request(),url=new URL(r.url());if(url.origin!==origin||url.username||url.password||r.method()!=='GET'&&/^\/api\/v1\/(runtime|connection)(\/|$)/.test(url.pathname)){report.blockedRequests.push({path:url.pathname,method:r.method()});await route.abort();}else await route.continue();});
  page=context.pages()[0]??await context.newPage();page.setDefaultTimeout(12000);
  page.on('pageerror',(e:Error)=>report.pageErrors.push(e.message.slice(0,800)));
  page.on('console',(e:any)=>{if(e.type()==='error')report.consoleErrors.push(e.text().slice(0,800));});
  page.on('response',(r:any)=>{if(r.status()>=400)report.httpErrors.push({path:new URL(r.url()).pathname,status:r.status()});});
  await page.goto(origin);check('page_identity',page.url()===origin+'/'&&(await page.title()).includes('Product-Agent OS'));
  await page.getByLabel(appLabel('ru','code'),{exact:true}).fill(service.pairingCode);
  const paired=page.waitForResponse((r:any)=>r.url()===origin+'/api/v1/bootstrap/exchange'&&r.status()===200);
  await page.getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();csrf=(await(await paired).json()).csrfToken;
  async function api(path:string,payload?:unknown){return page.evaluate(async({path,payload,csrf}:any)=>{const r=await fetch('/api/v1'+path,{method:payload===undefined?'GET':'POST',headers:{'content-type':'application/json','x-paos-csrf':csrf},...(payload===undefined?{}:{body:JSON.stringify(payload)})});return {status:r.status,body:await r.json()};},{path,payload,csrf});}
  async function until(name:string,predicate:()=>Promise<boolean>){const deadline=Date.now()+15000;while(Date.now()<deadline){if(await predicate()){check(name,true);return;}await new Promise(r=>setTimeout(r,100));}check(name,false);}
  async function nav(section:string){const menu=page.getByRole('button',{name:appLabel(locale,'menu'),exact:true});if(await menu.isVisible()&&await menu.getAttribute('aria-expanded')!=='true')await menu.click();await page.locator('nav').getByRole('button',{name:uiLabel(locale,('nav.'+section) as any),exact:true}).click();}
  const created=await api('/projects',{name:'Synthetic M2 acceptance',keyPrefix:'TEST',workspaceRoot:workspace});check('project_registered',created.status===201);const project=created.body;
  const snap=async()=>(await api('/projects/'+project.id+'/task-manager')).body;
  const task=async(id:string)=>(await snap()).tasks.find((t:any)=>t.id===id);
  const command=async(input:unknown)=>api('/projects/'+project.id+'/task-manager/commands',{expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:randomUUID(),...input as any});
  const manager=()=>page.getByTestId('task-manager'),detail=()=>page.getByTestId('task-detail');
  const w=(key:Parameters<typeof word>[1])=>word(locale,key);
  async function open(id:string,tab='summary'){await manager().locator('[data-task-id="'+id+'"]').first().click();await detail().waitFor();if((await task(id)).data.schemaVersion==='m2_task_profile_v1')await detail().getByRole('tab',{name:w(tab as any),exact:true}).click();}
  async function tab(name:string){await detail().getByRole('tab',{name:w(name as any),exact:true}).click();}
  async function create(title:string,type='task',parentId='',full=true){
   await manager().getByRole('button',{name:w('create'),exact:true}).click();const editor=page.locator('.task-list').getByTestId('task-editor');
   await editor.locator('[name=title]').fill(title);await editor.locator('[name=type]').selectOption(type);
   if(parentId)await editor.locator('[name=parentId]').selectOption(parentId);
   await editor.locator('[name=body]').fill('Synthetic scope '+title);await editor.locator('[name=criteria]').fill('Observed synthetic result');
   if(full){await editor.locator('[name=technicalValue]').fill('Correct persistent behavior');await editor.locator('[name=productValue]').fill('Reviewable user result');await editor.locator('[name=estimate]').fill('00:01:00');await editor.locator('[name=noRisks]').check();await editor.getByTestId('add-file').click();await editor.locator('[name=file-path-0]').fill('a.txt');await editor.locator('[name=file-planned-0]').selectOption('read');await editor.locator('[name=file-revision-0]').fill(sourceHash);}
   await editor.getByRole('button',{name:w('save'),exact:true}).click();
   await until('created_'+title,async()=>(await snap()).tasks.some((t:any)=>t.title===title));
   return (await snap()).tasks.find((t:any)=>t.title===title);
  }
  async function lifecycle(id:string,next:string,manual=false){
   await open(id,'acceptance');const panel=page.getByTestId('task-transition');
   await panel.locator('[name=transition-reason]').fill('Synthetic observed decision');
   if(next==='done'){await panel.locator('[name=criterion-evidence-0]').fill('Verified through synthetic UI/API acceptance');await panel.locator('[name=criterion-passed-0]').check();}
   if(manual)await panel.getByRole('button',{name:w('complete'),exact:true}).click();
   else {await panel.locator('[name=transition-status]').selectOption(next);await panel.locator('form').getByRole('button',{name:['done','cancelled'].includes((await task(id)).status)?w('reopen'):w('transition'),exact:true}).click();}
  }
  async function screenshot(name:string){await page.screenshot({path:join(output,name),fullPage:false});report.screenshots.push(join(output,name));}
  async function geometry(name:string){const size=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));check(name,size.scroll<=size.width+1,size);}
  await page.reload();await page.locator('.navigation select:enabled').waitFor();await page.locator('.navigation select').selectOption(project.id);await nav('tasks');
  await manager().waitFor();check('new_manager_is_default',await page.getByTestId('task-filters').count()===1);
  check('no_framework_overlay',await page.locator('vite-error-overlay,nextjs-portal').count()===0);
  if(scenario==='settings-cas'){
   step='settings_cas';const settings=page.getByTestId('manager-settings');await settings.locator('summary').first().click();
   const row=settings.locator('.m2-catalog-row').filter({has:page.locator('input[name=component-name]')}).first();await row.locator('[name=component-name]').fill('Local retained draft');
   const before=await snap(),original=before.components[0];
   check('other_catalog_writer_committed',(await command({action:'component',expectedRevision:before.settingsRevisions.components,item:{...original,name:'Server winner'}})).status===200);
   let refreshed=page.waitForResponse((r:any)=>r.url().endsWith('/task-manager')&&r.request().method()==='GET'&&r.status()===200);
   await manager().getByRole('button',{name:w('refresh'),exact:true}).first().click();await refreshed;
   await until('catalog_refresh_settled',async()=>!(await manager().locator('[role=status]').first().innerText()).includes(w('loading')));
   check('catalog_dirty_draft_retained',await row.locator('[name=component-name]').inputValue()==='Local retained draft');
   const saved=page.waitForResponse((r:any)=>r.url().endsWith('/task-manager/commands')&&r.request().postDataJSON()?.action==='component');
   await row.getByRole('button',{name:w('save'),exact:true}).click();const response=await saved;
   check('catalog_stale_save_rejected',response.status()===409,{status:response.status(),serverName:(await snap()).components.find((c:any)=>c.id===original.id).name});
   check('catalog_server_winner_preserved',(await snap()).components.find((c:any)=>c.id===original.id).name==='Server winner');
   await row.getByRole('button',{name:w('discard'),exact:true}).click();check('catalog_explicit_discard_adopts_server',await row.locator('[name=component-name]').inputValue()==='Server winner');
   const board=page.getByTestId('board-settings');await board.locator('[name=column-wip-0]').fill('5');
   const latest=await snap(),otherBoard=structuredClone(latest.board);otherBoard.columns[0].wipLimit=3;otherBoard.columns[0].wipMode='hard';
   check('other_board_writer_committed',(await command({action:'board',expectedRevision:latest.settingsRevisions.board,board:otherBoard})).status===200);
   refreshed=page.waitForResponse((r:any)=>r.url().endsWith('/task-manager')&&r.request().method()==='GET'&&r.status()===200);await manager().getByRole('button',{name:w('refresh'),exact:true}).first().click();await refreshed;
   await until('board_refresh_settled',async()=>!(await manager().locator('[role=status]').first().innerText()).includes(w('loading')));
   check('board_dirty_draft_retained',await board.locator('[name=column-wip-0]').inputValue()==='5');
   const boardSaved=page.waitForResponse((r:any)=>r.url().endsWith('/task-manager/commands')&&r.request().postDataJSON()?.action==='board');
   await board.getByRole('button',{name:w('save')+' · '+w('settings'),exact:true}).click();check('board_stale_save_rejected',(await boardSaved).status()===409);
   check('board_server_winner_preserved',(await snap()).board.columns[0].wipLimit===3);
   await board.getByRole('button',{name:w('discard'),exact:true}).click();check('board_explicit_discard_adopts_server',await board.locator('[name=column-wip-0]').inputValue()==='3');
   await screenshot('settings-cas.png');check('no_page_errors',report.pageErrors.length===0);report.status='passed_settings_cas';return;
  }
  if(scenario==='markdown'){
   step='markdown';const work=await create('Markdown acceptance');await open(work.id,'comments');const comments=page.getByTestId('task-comments');
   const body='**Safe bold** [reference](https://example.test/proof) <script>throw new Error("unsafe")</script> ![image](https://example.test/image.png)';
   await comments.locator('[name=comment]').fill(body);await comments.locator('form').getByRole('button',{name:w('comment'),exact:true}).click();
   await until('markdown_comment_saved',async()=>(await snap()).comments.some((c:any)=>c.body===body));
   check('markdown_strong_rendered',await comments.locator('.m2-comment-body strong').count()===1);
   check('markdown_html_and_images_inert',await comments.locator('script,img').count()===0);
   check('markdown_safe_link',await comments.locator('.m2-comment-body a').getAttribute('href')==='https://example.test/proof');
   check('no_external_markdown_requests',report.blockedRequests.length===0);check('no_page_errors',report.pageErrors.length===0);
   await screenshot('markdown-safe.png');report.status='passed_markdown_browser';return;
  }
  step='catalogs';const settings=page.getByTestId('manager-settings');await settings.locator('summary').first().click();
  check('eleven_initial_components',(await snap()).components.length===11);
  for(const name of ['v1.2','v1.3']){await settings.locator('[name=new-version-name]').fill(name);await settings.getByRole('button',{name:w('add')+' · '+w('versions'),exact:true}).click();await until('version_'+name,async()=>(await snap()).versions.some((v:any)=>v.name===name));}
  const versions=(await snap()).versions,v12=versions.find((v:any)=>v.name==='v1.2').id,v13=versions.find((v:any)=>v.name==='v1.3').id;
  const versionRow=settings.locator('form.m2-catalog-row').filter({has:page.locator('[name=version-name]')}).last();await versionRow.locator('[name=version-description]').fill('Synthetic target release');await versionRow.getByRole('button',{name:w('save'),exact:true}).click();await until('version_description_saved',async()=>(await snap()).versions.find((v:any)=>v.id===v13).description==='Synthetic target release');
  await settings.locator('summary').first().click();
  step='hierarchy';const epic=await create('M2 Epic','epic'),bug=await create('M2 Bug','bug',epic.id),sub=await create('M2 Subtask','sub_task',bug.id),draft=await create('M2 Incomplete','task','',false);
  check('unique_monotonic_keys',new Set([epic.publicKey,bug.publicKey,sub.publicKey,draft.publicKey]).size===4);
  check('m2_identity_server_owned',(await task(bug.id)).data.schemaVersion==='m2_task_profile_v1'&&(await task(bug.id)).data.creator.actorId==='local-user'&&!!(await task(bug.id)).data.createdAt);
  await lifecycle(draft.id,'ready');await until('incomplete_ready_explained',async()=>(await page.getByTestId('task-transition').innerText()).includes('READY_FIELDS_REQUIRED'));check('draft_stays_backlog',(await task(draft.id)).status==='backlog');
  await lifecycle(epic.id,'done',true);await until('parent_guard_visible',async()=>(await page.getByTestId('task-transition').innerText()).includes('CHILDREN_INCOMPLETE'));check('parent_not_false_done',(await task(epic.id)).status==='backlog');
  await open(bug.id);let editor=detail().getByTestId('task-editor');await editor.locator('[name=affectsVersions]').selectOption([v12]);await editor.locator('[name=fixVersions]').selectOption([v13]);await editor.locator('[name=components]').selectOption(['BackEnd','QA']);await editor.getByRole('button',{name:w('save'),exact:true}).click();await until('versions_and_components_saved',async()=>{const p=(await task(bug.id)).data;return p.affectsVersions.includes(v12)&&p.fixVersions.includes(v13)&&p.components.length===2;});
  step='draft_state';editor=detail().getByTestId('task-editor');await editor.locator('[name=title]').fill('Unsaved retained title');await tab('files');await tab('summary');check('draft_survives_tabs',await detail().locator('[name=title]').inputValue()==='Unsaved retained title');
  await nav('settings');await nav('tasks');check('draft_survives_navigation',await detail().locator('[name=title]').inputValue()==='Unsaved retained title');
  await detail().getByRole('button',{name:w('discard'),exact:true}).click();
  step='conflict';editor=detail().getByTestId('task-editor');await editor.locator('[name=title]').fill('Local conflict draft');const current=await task(bug.id);
  const concurrent=await command({action:'save',expectedRevision:current.revision,task:{...current.data,title:'Concurrent winning title'},reason:'Independent synthetic writer'});check('concurrent_writer_committed',concurrent.status===200);
  await editor.getByRole('button',{name:w('save'),exact:true}).click();await until('revision_conflict_visible',async()=>(await editor.innerText()).includes('REVISION_CONFLICT'));
  check('conflict_preserves_local_input',await editor.locator('[name=title]').inputValue()==='Local conflict draft');check('conflict_preserves_server_winner',(await task(bug.id)).title==='Concurrent winning title');await screenshot('revision-conflict.png');
  await manager().getByRole('button',{name:w('refresh'),exact:true}).first().click();await detail().getByRole('button',{name:w('discard'),exact:true}).click();
  step='preview';editor=detail().getByTestId('task-editor');await editor.locator('[name=parentId]').selectOption('');await editor.getByRole('button',{name:w('save'),exact:true}).click();await until('structural_preview_required',async()=>(await editor.innerText()).includes('PREVIEW_REQUIRED'));
  await editor.getByRole('button',{name:w('preview'),exact:true}).click();await editor.getByRole('button',{name:w('applyPreview'),exact:true}).click();await until('reviewed_reparent_applied',async()=>(await task(bug.id)).data.parentId===null);
  await tab('files');await page.getByTestId('task-references').getByRole('button',{name:w('readReference'),exact:true}).first().click();await until('exact_source_revision_read',async()=>(await page.getByTestId('task-references').innerText()).includes('Synthetic M2 source'));
  await tab('summary');editor=detail().getByTestId('task-editor');await editor.locator('[name=parentId]').selectOption(epic.id);await editor.locator('[name=reason]').fill('Reviewed restore to Epic');await editor.getByRole('button',{name:w('preview'),exact:true}).click();await editor.getByRole('button',{name:w('applyPreview'),exact:true}).click();await until('hierarchy_restored_after_preview',async()=>(await task(bug.id)).data.parentId===epic.id);
  step='saved_filters';const filters=page.getByTestId('task-filters');await filters.locator('summary').click();await filters.locator('[name=filter-type]').selectOption('bug');await filters.locator('[name=filter-fixVersion]').selectOption(v13);
  await filters.getByRole('button',{name:w('saveView'),exact:true}).click();await until('view_saved',async()=>(await snap()).board.view?.fixVersion===v13);await page.reload();await nav('tasks');await manager().waitFor();await filters.locator('summary').click();check('saved_filter_restored',await filters.locator('[name=filter-fixVersion]').inputValue()===v13);check('distinct_release_filter',await manager().locator('.task-list [data-task-id]').count()===1);await filters.locator('[name=filter-affectsVersion]').selectOption(v13);check('affects_does_not_equal_fix',await manager().locator('.task-list [data-task-id]').count()===0);await filters.getByRole('button',{name:w('reset'),exact:true}).click();
  step='manual_lifecycle';await lifecycle(sub.id,'done',true);await until('manual_subtask_done',async()=>(await task(sub.id)).status==='done');
  check('manual_end_observed_without_invented_duration',!!(await task(sub.id)).data.actual.endedAt&&(await task(sub.id)).data.actual.durationSeconds===null);
  await lifecycle(bug.id,'done',true);await until('manual_standard_done',async()=>(await task(bug.id)).status==='done');
  await lifecycle(epic.id,'done',true);await until('parent_done_after_required_scope',async()=>(await task(epic.id)).status==='done');
  await lifecycle(epic.id,'ready');await until('reopen_resolution_cleared',async()=>{const t=await task(epic.id);return t.status==='ready'&&t.data.resolution===null&&t.data.actual.endedAt===null;});
  step='links';const a=await create('M2 Prerequisite'),b=await create('M2 Dependent'),work=await create('M2 Activity');
  await open(a.id,'links');let links=page.getByTestId('task-links');await links.locator('[name=link-relation]').selectOption('blocks');await links.locator('[name=link-target]').selectOption(b.id);await links.locator('[name=link-reason]').fill('Synthetic prerequisite');await links.locator('form').getByRole('button').click();await until('canonical_link_saved',async()=>(await snap()).links.some((l:any)=>l.sourceId===a.id&&l.targetId===b.id));
  await open(b.id,'links');check('inverse_link_visible',(await page.getByTestId('task-links').innerText()).includes(a.publicKey));
  links=page.getByTestId('task-links');await links.locator('[name=link-relation]').selectOption('blocks');await links.locator('[name=link-target]').selectOption(a.id);await links.locator('[name=link-reason]').fill('Must reject cycle');await links.locator('form').getByRole('button').click();await until('cycle_rejected',async()=>(await links.innerText()).includes('TASK_LINK_CYCLE'));
  await lifecycle(b.id,'ready');await until('dependent_ready',async()=>(await task(b.id)).status==='ready');await lifecycle(b.id,'in_progress');await until('dependency_blocks_start',async()=>(await page.getByTestId('task-transition').innerText()).includes('DEPENDENCY_BLOCKED'));
  await lifecycle(a.id,'cancelled');await until('cancel_reason_resolution_saved',async()=>(await task(a.id)).status==='cancelled'&&(await task(a.id)).data.resolution==='cancelled');
  await lifecycle(b.id,'in_progress');await until('cancelled_blocker_still_blocks',async()=>(await page.getByTestId('task-transition').innerText()).includes('DEPENDENCY_BLOCKED'));
  await lifecycle(a.id,'backlog');await until('cancelled_reopened',async()=>(await task(a.id)).status==='backlog');await lifecycle(a.id,'done',true);await until('prerequisite_completed',async()=>(await task(a.id)).status==='done');
  await lifecycle(b.id,'in_progress');await until('dependent_started_after_proof',async()=>(await task(b.id)).status==='in_progress');const firstStart=(await task(b.id)).data.actual.startedAt;
  await lifecycle(b.id,'done',true);await until('dependent_completed',async()=>(await task(b.id)).status==='done');await lifecycle(b.id,'ready');await until('first_actual_start_preserved',async()=>(await task(b.id)).data.actual.startedAt===firstStart&&(await task(b.id)).data.actual.endedAt===null);
  step='comments';await open(work.id,'comments');const comments=page.getByTestId('task-comments');const markdown='**Synthetic review** [safe](https://example.test/proof) <script>unsafe()</script> ![image](https://example.test/image.png)';
  await comments.locator('[name=comment]').fill(markdown);await comments.locator('form').getByRole('button',{name:w('comment'),exact:true}).click();await until('comment_persisted',async()=>(await snap()).comments.some((c:any)=>c.body===markdown));
  check('markdown_strong_rendered',await comments.locator('.m2-comment-body strong').count()>0);check('markdown_raw_html_inert',await comments.locator('script,img').count()===0);check('markdown_safe_link',await comments.locator('.m2-comment-body a').getAttribute('href')==='https://example.test/proof');
  await comments.locator('.comments li').first().getByRole('button',{name:w('edit'),exact:true}).click();await comments.locator('[name=comment]').fill('Edited synthetic review');await comments.locator('form').getByRole('button',{name:w('save'),exact:true}).click();await until('comment_revision_visible',async()=>(await comments.innerText()).includes('Edited synthetic review'));
  await comments.locator('.comments li').first().getByRole('button',{name:w('remove'),exact:true}).click();await until('comment_tombstone',async()=>(await snap()).comments.some((c:any)=>c.data.deleted===true&&c.body===''));
  check('deleted_body_absent_public_history',!JSON.stringify((await api('/projects/'+project.id+'/history')).body).includes(markdown));await tab('history');await until('separate_history_visible',async()=>(await page.getByTestId('task-history').innerText()).includes('local-user'));
  step='attachments';await tab('attachments');const attachments=page.getByTestId('task-attachments');
  const file={name:'note.txt',mimeType:'text/plain',buffer:Buffer.from('Synthetic managed copy')};
  for(let i=0;i<2;i++){await attachments.locator('[name=attachment-file]').setInputFiles(file);await attachments.locator('form button').filter({hasText:w('upload')}).click();await until('same_name_upload_'+i,async()=>(await snap()).attachments.filter((a:any)=>a.data.taskId===work.id&&a.data.status==='available').length===i+1);}
  check('duplicate_filenames_do_not_overwrite',(await snap()).attachments.filter((a:any)=>a.data.taskId===work.id).length===2);
  let dropped=false;const uploadPattern=origin+'/api/v1/projects/'+project.id+'/tasks/'+work.id+'/attachments';
  const loseAck=async(route:any)=>{if(!dropped&&route.request().method()==='POST'){const response=await route.fetch();check('lost_ack_server_accepted',response.status()===200);dropped=true;await route.abort('failed');}else await route.continue();};
  await context.route(uploadPattern,loseAck);await attachments.locator('[name=attachment-file]').setInputFiles({name:'lost-ack.txt',mimeType:'text/plain',buffer:Buffer.from('Exactly once managed upload')});await attachments.locator('form button').filter({hasText:w('upload')}).click();
  await until('lost_ack_committed_once',async()=>(await snap()).attachments.filter((a:any)=>a.data.filename==='lost-ack.txt').length===1);
  await attachments.locator('form').getByRole('button',{name:w('retry'),exact:true}).waitFor();await tab('comments');await tab('attachments');
  await page.getByTestId('task-attachments').locator('form').getByRole('button',{name:w('retry'),exact:true}).click();
  await until('lost_ack_retry_acknowledged',async()=>await page.getByTestId('task-attachments').locator('form').getByRole('button',{name:w('upload'),exact:true}).count()===1);
  check('lost_ack_retry_did_not_duplicate',(await snap()).attachments.filter((a:any)=>a.data.filename==='lost-ack.txt').length===1);
  await context.unroute(uploadPattern,loseAck);
  const download=page.waitForEvent('download');await attachments.locator('.records li').filter({has:page.locator('strong',{hasText:'note.txt'})}).getByRole('link',{name:w('download'),exact:true}).first().click();const saved=await download;const downloadPath=join(output,'downloaded-note.txt');await saved.saveAs(downloadPath);check('attachment_download_exact',await readFile(downloadPath,'utf8')==='Synthetic managed copy');
  await attachments.locator('[name=attachment-file]').setInputFiles({name:'bad.png',mimeType:'image/png',buffer:Buffer.from('not a png')});await attachments.locator('form button').filter({hasText:w('upload')}).click();await until('mime_mismatch_explained',async()=>(await attachments.innerText()).includes('MIME_CONTENT_MISMATCH'));
  await attachments.locator('[name=attachment-reason]').fill('Synthetic remove');await attachments.locator('.records li').first().getByRole('button',{name:w('remove'),exact:true}).click();await until('attachment_tombstone',async()=>(await snap()).attachments.some((a:any)=>a.data.taskId===work.id&&a.data.status==='deleted'));
  step='legacy';const legacy=newTask(project.id,'Legacy preserved','M1 original',['M1 criterion']);legacy.data!.creator={kind:'imported_unknown',actorId:null};legacy.data!.key='TEST-90';
  await store!.write({projectId:project.id,actorId:'fixture-import',expectedAuthorityEpoch:1,idempotencyKey:'legacy-seed',changes:[{expectedRevision:0,entity:{id:legacy.id,kind:'task',data:legacy.data}}]});await manager().getByRole('button',{name:w('refresh'),exact:true}).first().click();await open(legacy.id);check('legacy_readable',(await detail().innerText()).includes('M1 original'));
  await detail().getByRole('button',{name:w('upgrade'),exact:true}).click();await until('legacy_upgrade_committed',async()=>(await task(legacy.id)).data.schemaVersion==='m2_task_profile_v1');check('legacy_unknown_author_not_forged',(await task(legacy.id)).data.creator.kind==='imported_unknown'&&(await task(legacy.id)).data.createdAt===null);
  step='archive';const archive=page.getByTestId('manager-archive');await archive.locator('summary').click();check('archive_all_projects_disclosed',/всех проектов|все проекты|all projects/i.test(await archive.innerText()));await archive.getByRole('button',{name:w('exportArchive'),exact:true}).click();await until('archive_id_visible',async()=>!!await archive.locator('[name=full-backup-id]').inputValue());await archive.locator('[name=full-restore-confirm]').check();await archive.getByRole('button',{name:w('restoreArchive'),exact:true}).click();await until('inactive_restore_explained',async()=>(await archive.innerText()).includes(w('restartRequired')));
  step='board';await manager().getByRole('button',{name:w('board'),exact:true}).click();check('seven_default_columns',await manager().locator('.kanban-column').count()===7);
  await manager().locator('li[draggable=true]').filter({has:page.locator('[data-task-id="'+work.id+'"]')}).dragTo(manager().locator('[data-column-id=ready] h3'));
  await page.getByTestId('task-transition').locator('[name=transition-status]').waitFor();check('drag_opens_same_transition_contract',await page.getByTestId('task-transition').locator('[name=transition-status]').inputValue()==='ready'&&(await task(work.id)).status==='backlog');
  const dragged=page.getByTestId('task-transition');await dragged.locator('[name=transition-reason]').fill('Observed drag transition');await dragged.locator('form button').click();await until('drag_guarded_transition_saved',async()=>(await task(work.id)).status==='ready');
  await open(work.id);await detail().locator('[name=board-move]').selectOption('closed');await page.locator('[name=board-target-status]').waitFor();check('closed_column_requires_outcome_choice',await page.locator('[name=board-target-status]').inputValue()==='');await page.getByRole('dialog').getByRole('button',{name:w('cancel'),exact:true}).click();
  await screenshot('desktop-board.png');await geometry('desktop_no_document_overflow');
  step='locale_theme';await nav('settings');await page.getByLabel(uiLabel(locale,'preferences.language'),{exact:true}).selectOption('en');await page.getByLabel(uiLabel(locale,'preferences.theme'),{exact:true}).selectOption('dark');await page.getByRole('button',{name:uiLabel(locale,'preferences.save'),exact:true}).click();locale='en';await page.waitForFunction(()=>document.documentElement.lang==='en'&&document.documentElement.dataset.theme==='dark');await nav('tasks');await manager().getByRole('button',{name:w('create'),exact:true}).waitFor();check('english_task_manager',await manager().getByRole('button',{name:w('create'),exact:true}).count()===1);await screenshot('english-dark.png');
  await page.setViewportSize({width:390,height:844});await geometry('mobile_no_document_overflow');await screenshot('mobile-dark.png');
  check('expected_http_errors_only',report.httpErrors.every((e:any)=>e.path.endsWith('/session')&&e.status===401||e.path.endsWith('/task-manager/commands')&&[400,409,422].includes(e.status)||/attachments$/.test(e.path)&&[400,413,422].includes(e.status)));check('no_page_errors',report.pageErrors.length===0);check('no_unexpected_external_or_provider_requests',report.blockedRequests.length===0);check('no_framework_console_errors',report.consoleErrors.every((s:string)=>/^Failed to load resource:/.test(s)));
  report.status='passed_m2_task_manager_browser';report.mandatoryGaps=[];
  const sources=['tests/web/single-window/m2-task-manager-browser-acceptance.mts','packages/contracts/issues/task-profile.ts','packages/contracts/issues/manager.ts','apps/local-service/src/task-manager/service.mts','apps/local-service/src/storage/sqlite-worker.mts','apps/local-service/src/http/application.mts','apps/web/src/ui/App.tsx','apps/web/src/api/client.ts','apps/web/src/features/tasks/TaskManager.tsx','apps/web/src/features/tasks/Editor.tsx','apps/web/src/features/tasks/Panels.tsx','apps/web/src/features/tasks/Settings.tsx','apps/web/dist/index.html'];
  for(const name of await readdir('apps/web/dist/assets'))sources.push('apps/web/dist/assets/'+name);
  for(const name of sources)report.sourceHashes[name]=createHash('sha256').update(await readFile(name)).digest('hex');
 }catch(error){report.status='failed';report.failedStep=step;report.error=String((error as Error).message).slice(0,1200);process.exitCode=1;try{if(page&&!page.isClosed()){await page.screenshot({path:join(output,'failed.png'),fullPage:false,mask:[page.locator('input')]});report.failureUi=(await page.locator('body').innerText()).slice(0,14000);}}catch{}}
 finally{
  if(timer)clearTimeout(timer);try{await context?.close();report.browserClosed=true;}catch{report.browserClosed=false;process.exitCode=1;}
  try{await service?.quit();report.serviceClosed=true;}catch{report.serviceClosed=false;process.exitCode=1;}
  if(report.serviceClosed){if(dirname(resolve(fixture))!==scratch)throw Error('FIXTURE_CLEANUP_BOUNDARY');await rm(fixture,{recursive:true,force:true});report.fixtureCleaned=true;}else report.fixtureCleaned=false;
  if(!report.sourceHashes||!Object.keys(report.sourceHashes).length){const files=['tests/web/single-window/m2-task-manager-browser-acceptance.mts','apps/web/src/features/tasks/Settings.tsx','apps/web/src/features/tasks/Panels.tsx','apps/web/src/features/tasks/TaskManager.tsx','apps/web/dist/index.html'];for(const name of await readdir('apps/web/dist/assets'))files.push('apps/web/dist/assets/'+name);for(const name of files)report.sourceHashes[name]=createHash('sha256').update(await readFile(name)).digest('hex');}
  report.finishedAt=new Date().toISOString();await writeFile(join(output,'m2-browser-result.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({status:report.status,checks:report.checks.length,failedStep:report.failedStep,error:report.error,report:join(output,'m2-browser-result.json'),fixtureCleaned:report.fixtureCleaned}));
 }
}
await main();
