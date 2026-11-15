import {randomUUID} from 'node:crypto';
import {auditRenderedPage} from '../accessibility/audit.mts';

/** Visual inventory on the existing disposable service. No provider is attached or called. */
export async function captureV3States({page,api,project,base,taskId,store,shot,report,nav,appearance}:any){
 const assets:Record<string,string>={};
 for(const kind of ['agent','skill']){
  const proposal={kind,action:'create',name:kind==='agent'?'Builder':'Review skill',description:'Синтетический профиль для проверки интерфейса',content:kind==='agent'?'Review the scoped changes and preserve approvals.':'---\nname: review-skill\ndescription: Review scoped changes\n---\n\n# Review\nInspect changes and record evidence.\n',dependencies:[],reason:'Disposable visual fixture'};
  const preview=await api(base+'/team/proposals/preview',{proposal,expectedRevision:0});
  if(preview.status!==200)throw Error('VISUAL_ASSET_PREVIEW '+JSON.stringify(preview.body));
  const saved=await api(base+'/team/proposals/apply',{proposal:preview.body.proposal,previewDigest:preview.body.previewDigest,expectedRevision:0,epoch:project.authorityEpoch,expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:randomUUID()});
  if(saved.status!==200)throw Error('VISUAL_ASSET_APPLY '+JSON.stringify(saved.body));assets[kind]=saved.body.assetId;
 }
 await store.write({projectId:project.id,actorId:'synthetic-fixture',expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:'v3-session-fixture',changes:[{expectedRevision:0,entity:{id:'v3-session',kind:'session',title:'Обновление навигации проекта',status:'idle',data:{mode:'discussion',taskId,agentId:assets.agent}}},{expectedRevision:0,entity:{id:'v3-message',kind:'message',parentId:'v3-session',body:'Проверить сетку, поля и состояния интерфейса в обеих темах.',data:{role:'user',sessionId:'v3-session'}}}]});
 const decision=await api(base+'/decisions',{kind:'product',title:'Утвердить результат проверки',body:'Проверить интерфейс по утверждённому V3. Синтетическое решение.',taskId,sessionId:'v3-session',proposedDiff:'UI layout only',evidenceIds:[taskId],expiresInSeconds:3600,expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:randomUUID()});
 if(decision.status!==200&&decision.status!==201)throw Error('VISUAL_DECISION '+JSON.stringify(decision.body));
 const snapshot=(await api(base+'/task-manager')).body;
 const board={...snapshot.board,columns:snapshot.board.columns.filter((c:any)=>c.id!=='cancelled').map((c:any)=>({...c,statuses:c.id==='ready'?['ready','cancelled']:c.statuses.filter((s:string)=>s!=='cancelled')}))};
 const configured=await api(base+'/task-manager/commands',{action:'board',board,expectedRevision:snapshot.settingsRevisions.board,expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:randomUUID()});
 if(configured.status!==200)throw Error('VISUAL_BOARD_FIXTURE '+JSON.stringify(configured.body));
 // Provider-dependent presentation is supplied by an explicit visual-only fixture.
 // No Start/Apply/Resume action is sent to a provider or to the recipe executor.
 const generated={id:'visual-generation',state:'completed',sessionId:'v3-session',requirements:[{id:'R-1',relativePath:'REQUIREMENTS.md',revision:'synthetic-fixture'}],proposal:{kind:'skill',action:'create',name:'Review evidence',description:'Проверить интерфейс по утверждённому макету',content:'---\nname: review-evidence\ndescription: Review visual evidence\n---\n\n# Review\nCompare both themes and record differences.\n',dependencies:[],reason:'Synthetic visual fixture'}};
 const bindingPattern='**/api/v1/runtime/bindings',generationPattern='**/api/v1/projects/*/team/skills/generation**',recipePattern='**/api/v1/projects/*/execution-recipes';
 await page.route(bindingPattern,(route:any)=>route.fulfill({json:{bindingId:'visual-binding'}}));
 await page.route(generationPattern,(route:any)=>route.fulfill({json:generated}));
 const recovery={id:'visual-recovery',projectId:project.id,taskId,sessionId:'v3-session',mode:'recipe',state:'recovery_required',revision:1,workflow:{id:'default',version:1},recipeId:'review',transitionId:'backlog-ready',steps:[],iterations:{},attempts:[],createdAt:Date.now(),updatedAt:Date.now(),reason:'Синтетический checkpoint: требуется сверка',outcome:null,recoveryDecisions:[],recovery:{checkpoint:'unresolved',canResume:false,canCancel:true,runId:'visual-run',childState:'outcome_unknown'}};
 await page.route(recipePattern,(route:any)=>route.request().method()==='GET'?route.fulfill({json:{items:[recovery]}}):route.abort());
 report.visualMockSources=['binding response','completed skill generation','recipe recovery GET'];
 const settings=(await api(base+'/task-manager')).body;
 const version=await api(base+'/task-manager/commands',{action:'version',item:{id:'visual-version',name:'V3 review',status:'unreleased',description:'Synthetic visual review',startDate:null,releaseDate:null},expectedRevision:settings.settingsRevisions.versions,expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:randomUUID()});if(version.status!==200)throw Error('VISUAL_VERSION');
 const workflow=settings.workflows.workflows.find((w:any)=>w.id==='default');
 const savedDraft=await api(base+'/task-manager/commands',{action:'workflow-save-draft',workflowId:'default',definition:workflow.versions[0].definition,expectedRevision:settings.settingsRevisions.workflows,expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:randomUUID()});if(savedDraft.status!==200)throw Error('VISUAL_WORKFLOW_DRAFT');
 report.stateViews=[];page.setDefaultTimeout(6000);
 for(const theme of ['light','dark']){
  await appearance('ru',theme);await page.setViewportSize({width:1440,height:1000});
  const capture=async(id:string,prepare?:()=>Promise<void>,note?:string)=>{
   try{await prepare?.();await page.evaluate(async()=>{await document.fonts.ready;document.querySelectorAll('dialog').forEach(e=>e.scrollTop=0);await Promise.all(document.getAnimations().filter(a=>a.effect?.getComputedTiming().iterations!==Infinity).map(a=>a.finished.catch(()=>{})));});const audit=await page.evaluate(auditRenderedPage);await shot('parity-'+theme+'-'+id+'.png',{fullPage:true,reset:false});report.stateViews.push({id,theme,status:'captured',note,audit});}
   catch(error){report.stateViews.push({id,theme,status:'capture_failed',error:String(error).slice(0,600)});}
  };
  const click=async(selector:string)=>{await page.locator(selector).click();};
  await nav('overview');
  for(const [id,tab] of [['overview','dashboard'],['overview-sources','sources'],['project-analytics','usage']])await capture(id,()=>click('[data-overview-section='+tab+']'));
  await capture('portfolio-dashboard',()=>nav('portfolio'));
  await nav('tasks');await page.locator('[data-task-id="'+taskId+'"]').first().click();
  await capture('tasks-list');await capture('tasks-board',()=>page.locator('.segmented').getByRole('button',{name:'Доска',exact:true}).click());
  await page.locator('.segmented').getByRole('button',{name:'Список',exact:true}).click();
  await page.locator('[data-task-id="'+taskId+'"]').first().dblclick();
  await capture('task-summary',()=>click('[data-tab=summary]'));await page.keyboard.press('Escape');
  for(const tab of ['files','acceptance','comments','history','attachments','links','sessions'])await capture('task-'+tab,()=>click('[data-tab='+tab+']'));
  await capture('task-move',async()=>{await page.locator('[name=board-move]').selectOption('ready');await page.locator('[name=board-target-status]').waitFor();});await page.keyboard.press('Escape');
  await capture('task-usage',()=>page.getByTestId('task-usage-open').click(),'Usage measurements remain unavailable, never fabricated.');await page.getByRole('button',{name:'Вернуться к задаче',exact:true}).click();
  await capture('task-delete',async()=>{await page.getByTestId('task-delete-open').click();await page.getByTestId('task-delete').scrollIntoViewIfNeeded();});
  await page.keyboard.press('Escape');
  await capture('task-create',async()=>{await page.locator('.task-page-title button.primary').click();await page.locator('.task-list [name=title]').fill('Улучшить навигацию проекта');});
  await page.locator('.task-back').click();await page.locator('.task-workspace-tabs').getByRole('button',{name:'Настройки задач',exact:true}).click();
  for(const [id,label] of [['task-components','Компоненты'],['task-versions','Версии продукта'],['task-release','Политика целевого выпуска'],['task-columns','Доска']])await capture(id,async()=>{const panel=page.getByTestId('manager-settings');await panel.locator('nav').getByRole('button',{name:label,exact:true}).click();if(id==='task-versions'){const edit=panel.locator('.catalog-item-summary:visible button').first();await edit.click();}});
  await capture('task-archive',()=>page.locator('.task-workspace-tabs').getByRole('button',{name:'Полный архив',exact:true}).click());
  await nav('sessions');await page.locator('[data-session-id="v3-session"]').click();
  await capture('sessions-work');
  for(const pane of ['run','checks','question'])await capture('session-'+pane,()=>click('[data-inspector-pane='+pane+']'));
  for(const [id,name] of [['session-context','Контекст'],['session-changes','Изменения']])await capture(id,()=>page.locator('.chat-panel>.tabs').getByRole('button',{name,exact:true}).click());
  await capture('sessions-history',()=>page.getByTestId('sessions-catalog').locator('.section-tabs').getByRole('button',{name:'Полная доступная история',exact:true}).click());
  await capture('session-usage',()=>page.getByTestId('sessions-catalog').locator('.section-tabs').getByRole('button',{name:'Tokens / tool_use',exact:true}).click());
  for(const kind of ['agent','skill']){
   await nav(kind==='agent'?'agents':'skills');const manager=page.getByTestId(kind+'-manager');
   if(kind==='agent')await capture('agents-dashboard');
   await manager.locator('[data-resource-section=profiles]').click();await manager.locator('[data-asset-id="'+assets[kind]+'"]').click();
   for(const [id,name] of [['profile','Профиль'],['edit','Редактор'],['history','Версии'],['activity','Использование']])await capture((kind==='agent'?'agents':'skills')+'-'+id,()=>manager.locator('.tabs').getByRole('button',{name,exact:true}).click());
   if(kind==='agent'){
    await capture('agent-dashboard',()=>manager.locator('[data-resource-section=agent]').click());
    await capture('agents-generate',()=>manager.locator('[data-resource-section=generate]').click());
   }else{
    await capture('skills-discover',async()=>{await manager.locator('[data-resource-section=discover]').click();await manager.getByRole('button',{name:'Найти в доступных источниках',exact:true}).click();});
    await capture('skills-import',async()=>{await manager.locator('[name=skill-source-root]').selectOption('project-skills-agents');await manager.locator('[name=skill-source-path]').fill('review-import');await manager.getByRole('button',{name:'Проверить источник',exact:true}).click();await page.getByTestId('skill-source-preview').waitFor();},'Local synthetic SKILL.md source preview, import not applied.');
    await capture('skill-requirements',async()=>{await manager.locator('[data-resource-section=requirements]').click();await page.locator('[data-generator-step=requirements]').click();});
    await capture('skill-draft',async()=>{const generator=page.getByTestId('skill-generator');await generator.getByRole('button',{name:'Рекомендовать скилл',exact:true}).click();await generator.getByRole('button',{name:'Открыть draft',exact:true}).click();await page.getByTestId('skill-generation-editor').scrollIntoViewIfNeeded();},'Visual-only completed-generation response; no provider call.');
    await capture('skill-diff',async()=>{await page.getByTestId('skill-generation-editor').getByRole('button',{name:'Проверить и показать diff',exact:true}).click();await page.getByTestId('skill-generation-preview').waitFor();await page.getByTestId('skill-generation-preview').scrollIntoViewIfNeeded();},'Real local preview of a synthetic proposal; Apply not clicked.');
   }
  }
  await nav('projectMap');for(const [id,view] of [['graph-map','graph'],['graph-mermaid','mermaid'],['graph-list','list']])await capture(id,async()=>{await page.locator('[data-graph-view='+view+']').click();if(id==='graph-mermaid')await page.locator('[data-renderer=mermaid] svg').waitFor();});
  await nav('documents');await capture('documents-list');await capture('document-reader',async()=>{await page.locator('[data-artifact-id]').filter({hasText:'REQUIREMENTS.md'}).first().click();await page.getByTestId('artifact-reader').getByRole('heading').first().waitFor();});
  await capture('document-proposal',async()=>{if(!await page.getByTestId('document-proposal-editor').isVisible()){const propose=page.getByTestId('artifact-reader').getByRole('button',{name:'Предложить изменение',exact:true});if(await propose.isEnabled())await propose.click();else await page.locator('button[data-artifact-pane=proposal]').click();}await page.getByTestId('document-proposal-editor').getByRole('button',{name:'Предпросмотр изменения',exact:true}).click();await page.getByTestId('document-proposal-preview').waitFor();});
  await nav('checks');await capture('checks-list');await capture('check-detail',async()=>{await page.locator('[data-artifact-id]').first().click();await page.getByTestId('artifact-reader').getByRole('heading').first().waitFor();});
  await nav('autonomy');await page.locator('[name=autonomy-tasks]').selectOption(taskId);await page.locator('[name=autonomy-paths]').fill('.');for(const pane of ['policy','preview','runs'])await capture('autonomy-'+pane,async()=>{if(pane==='preview'){await page.getByRole('button',{name:'Предпросмотр политики',exact:true}).click();await page.getByTestId('autonomy-preview').waitFor();}else await click('[data-autonomy-pane='+pane+']');});
  await nav('decisions');await capture('decisions-list');await capture('decision-detail',()=>page.getByTestId('decision-detail').scrollIntoViewIfNeeded());await capture('decision-history',async()=>{await page.getByTestId('decision-board').locator('.section-tabs').getByRole('button',{name:'История',exact:true}).click();});await capture('decision-create',()=>page.getByTestId('decision-board').locator('.section-tabs').getByRole('button',{name:'Создать',exact:true}).click());
  await capture('search',()=>nav('search'));
  await nav('import');for(const [id,index] of [['import-source',0],['import-preview',1],['import-export',2]] as const)await capture(id,async()=>{const panel=page.getByTestId('import-workspace');if(index===1){await panel.locator('input[name=file]').setInputFiles({name:'tasks.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify({schema_version:'paos_web_task_groups_v1',tasks:[{id:'VIS-0001',title:'Проверить макет',status:'planned',depends_on:[]}]}))});await panel.locator('form').getByRole('button',{name:'Проверить импорт',exact:true}).click();await panel.locator('.import-preview').waitFor();}else await panel.locator('.section-tabs button').nth(index).click();});
  await nav('backup');for(const [id,index] of [['backup-create',0],['backup-restore',1]] as const)await capture(id,async()=>{const panel=page.getByTestId('backup-workspace');await panel.locator('.section-tabs button').nth(index).click();if(index===0){await panel.locator('button.primary').click();await panel.getByRole('status').filter({hasText:'Копия создана'}).waitFor();}});
  await nav('settings');for(const [id,tab] of [['settings-general','general'],['settings-projects','projects'],['settings-connection','connection'],['settings-quit','service']])await capture(id,()=>click('[data-settings-section='+tab+']'));
  await click('[data-settings-section=processes]');for(const tab of ['catalog','assignments','states','transitions','diagram','recipes','publication','migration','versions'])await capture('workflow-'+tab,async()=>{await click('[data-workflow-section='+tab+']');if(tab==='publication'){await page.getByTestId('workflow-publication').getByRole('button',{name:'Предпросмотр публикации',exact:true}).click();await page.getByTestId('workflow-publication').getByRole('button',{name:'Опубликовать проверенную версию',exact:true}).waitFor();}if(tab==='diagram')await page.getByTestId('workflow-manager').locator('[data-renderer=mermaid] svg').waitFor();});
  await click('[data-settings-section=execution]');await capture('recipe-preview',async()=>{const runner=page.getByTestId('recipe-runner');await runner.locator('[name=recipe-task]').selectOption(taskId);await runner.locator('[name=recipe-transition]').selectOption('backlog-ready');await runner.locator('[name=recipe-reason]').fill('Синтетический предпросмотр');await runner.getByRole('button',{name:'Предпросмотр перехода',exact:true}).click();await page.getByTestId('recipe-preview').waitFor();});await capture('recipe-history',()=>click('[data-recipe-pane=history]'));await capture('recipe-recovery',()=>click('[data-recipe-pane=recovery]'),'Visual-only recovery GET fixture; no recovery action invoked.');await capture('execution-queue',()=>click('[data-settings-section=queue]'));
 }
 await page.unroute(bindingPattern);await page.unroute(generationPattern);await page.unroute(recipePattern);
 page.setDefaultTimeout(12000);
}
