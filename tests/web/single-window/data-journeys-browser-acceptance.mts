import {createHash,randomUUID} from 'node:crypto';
import {mkdtemp,mkdir,readFile,writeFile,rm,readdir,lstat} from 'node:fs/promises';
import {join,resolve,isAbsolute} from 'node:path';
import {pathToFileURL} from 'node:url';
import {startLocalService} from '../../../apps/local-service/src/main.mts';
import {newTask} from '../../../apps/web/src/api/task.ts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';

// Synthetic browser acceptance. Setup mutations and fault injection are named separately from UI evidence.
if(process.argv[2]!=='--synthetic-browser'||process.argv.length!==7)throw Error('Explicit synthetic browser and installed paths required');
const args:Record<string,string>=Object.fromEntries([process.argv.slice(3,5),process.argv.slice(5,7)]);
if(!args['--playwright-core']||!args['--chromium']||!Object.values(args).every(isAbsolute))throw Error('Absolute installed paths required');
const scratch=resolve('.tmp/paos-m1');await mkdir(scratch,{recursive:true});
const root=await mkdtemp(join(scratch,'data-journeys-fixture-')),output=await mkdtemp(join(scratch,'data-journeys-evidence-'));
const profile=join(root,'profile'),home=join(root,'browser'),workspace=join(root,'legacy'),otherRoot=join(root,'other');
await Promise.all([profile,home,workspace,otherRoot].map(path=>mkdir(path)));
const report:any={startedAt:new Date().toISOString(),syntheticOnly:true,providerUsed:false,realCredentialsUsed:false,
 browserPlugin:'absent',browserDriver:'installed Playwright',checks:[],gaps:[],pageErrors:[],screenshots:[],setup:'API project/entity seeding; filesystem legacy fixtures; no production mutation'};
const check=(name:string,passed:boolean)=>{report.checks.push({name,passed});if(!passed)throw Error(name);};
const t=(key:Parameters<typeof appLabel>[1])=>appLabel('ru',key);
let service:Awaited<ReturnType<typeof startLocalService>>|undefined,context:any,page:any,csrf='';
const source=JSON.stringify({schema_version:'paos_web_task_groups_v1',tasks:[{id:'DATA-0001',title:'Legacy searchneedle проверка',status:'planned',depends_on:[]}]});
const projection=['### Task `DATA-0001`','- Task: Legacy searchneedle проверка','- Status: planned','- Schema version: task_matrix_plan_v1','- Depends on: none'].join('\n');
await writeFile(join(workspace,'tasks.json'),source);await writeFile(join(workspace,'tasks.md'),projection);
async function api(path:string,input?:unknown){return page.evaluate(async({path,input,csrf}:any)=>{const response=await fetch('/api/v1'+path,{method:input===undefined?'GET':'POST',headers:{'content-type':'application/json','x-paos-csrf':csrf},...(input===undefined?{}:{body:JSON.stringify(input)})});return {status:response.status,body:await response.json()};},{path,input,csrf});}
async function nav(name:'import'|'backup'|'search'){await page.locator('nav').getByRole('button',{name:t(name),exact:true}).click();}
async function click(key:Parameters<typeof appLabel>[1]){await page.locator('main').getByRole('button',{name:t(key),exact:true}).click();}
async function shot(name:string){await page.screenshot({path:join(output,name+'.png'),fullPage:true});report.screenshots.push(name+'.png');}
async function scenario(name:string,fn:()=>Promise<void>){try{await fn();}catch(error){report.gaps.push({scenario:name,error:String(error).slice(0,800)});if(page)await shot(name+'-failure').catch(()=>{});}}
try{
 const sourcePaths=['apps/web/src/ui/Operations.tsx','apps/web/src/ui/App.tsx','apps/local-service/src/main.mts','apps/web/dist/index.html'];
 report.sourceHashes=Object.fromEntries(await Promise.all(sourcePaths.map(async path=>[path,createHash('sha256').update(await readFile(path)).digest('hex')])));
 service=await startLocalService({profileDirectory:profile,instanceId:randomUUID()},{sandboxBrokerFactory:false});
 const origin=`http://127.0.0.1:${service.port}`;
 const {chromium}=await import(pathToFileURL(join(args['--playwright-core'],'index.mjs')).href);
 context=await chromium.launchPersistentContext(home,{headless:true,chromiumSandbox:true,executablePath:args['--chromium'],serviceWorkers:'block',viewport:{width:1440,height:1000},locale:'ru-RU',timeout:20000,
  env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:home,HOME:home,APPDATA:home,LOCALAPPDATA:home,TEMP:home,TMP:home}});
 report.browserVersion=context.browser()?.version();
 await context.route('**/*',async(route:any)=>{const u=new URL(route.request().url());if(u.origin!==origin){report.gaps.push({unexpectedNetwork:u.origin});await route.abort();}else await route.continue();});
 page=await context.newPage();page.setDefaultTimeout(15000);page.on('pageerror',(error:Error)=>report.pageErrors.push(error.message));
 await page.goto(origin);await page.getByLabel(t('code'),{exact:true}).fill(service.pairingCode!);
 const paired=page.waitForResponse((r:any)=>r.url().endsWith('/bootstrap/exchange')&&r.status()===200);await page.getByRole('button',{name:t('connect'),exact:true}).click();csrf=(await(await paired).json()).csrfToken;
 const project=(await api('/projects',{name:'Data journeys synthetic',keyPrefix:'DATA',workspaceRoot:workspace,legacySource:true})).body;
 const other=(await api('/projects',{name:'Other synthetic',keyPrefix:'OTHR',workspaceRoot:otherRoot})).body;
 check('api_setup_projects',Boolean(project.id&&other.id));
 await page.reload();await page.locator('.navigation select:enabled').selectOption(project.id);
 await scenario('S29',async()=>{
  await nav('import');
  async function preview(content:string,name='tasks.json',md?:string){
   await page.getByLabel(t('sourceFile'),{exact:true}).setInputFiles({name,mimeType:name.endsWith('.md')?'text/markdown':'application/json',buffer:Buffer.from(content)});
   await page.getByLabel(t('projectionFile'),{exact:true}).setInputFiles(md===undefined?[]:{name:'tasks.md',mimeType:'text/markdown',buffer:Buffer.from(md)});
   const response=page.waitForResponse((r:any)=>r.url().endsWith('/imports/preview'));
   await click('preview');const result=await(await response).json();await page.locator('main button').filter({hasText:t('preview')}).waitFor();return result;
  }
  const unsupported=await preview('{"schema_version":"unknown"}');
  await page.getByRole('alert').filter({hasText:'IMPORT_UNSUPPORTED'}).waitFor();check('S29_unsupported_visible_blocked',unsupported.error?.code==='IMPORT_UNSUPPORTED'&&await page.locator('.import-preview').count()===0);
  const md=await preview(projection,'tasks.md');check('S29_supported_markdown_preview',md.items?.length===1);
  const conflict=await preview(source,'tasks.json',projection.replace('Legacy searchneedle проверка','Conflicting source'));
  check('S29_conflict_visible_and_commit_disabled',conflict.blocked?.length>0&&await page.getByRole('button',{name:t('confirmImport'),exact:true}).isDisabled());
  const bundle=await preview(source,'tasks.json',projection);
  check('S29_json_markdown_dedup_visible',bundle.items?.length===1&&bundle.blocked?.length===0&&await page.locator('.import-preview .records li').count()===1);
  await page.getByLabel(t('confirmScope'),{exact:true}).check();
  await writeFile(join(workspace,'tasks.json'),source+' ');
  const driftResponse=page.waitForResponse((r:any)=>r.url().endsWith('/imports/commit'),{timeout:65000});await click('confirmImport');const drift=await driftResponse;
  await page.getByRole('alert').filter({hasText:'SOURCE_DRIFT'}).waitFor();check('S29_source_drift_blocked_visible',drift.status()===409);await shot('S29-source-drift');
  await writeFile(join(workspace,'tasks.json'),source);
  // Lose only the first successful ACK; retry remains an actual user click with the same mounted commit key.
  let lostReceipt:any;let dropped=false;
  await page.route('**/imports/commit',async(route:any)=>{if(dropped){await route.continue();return;}const result=await route.fetch({timeout:65000});if(result.ok()){lostReceipt=await result.json();dropped=true;await route.abort('failed');}else await route.fulfill({response:result});});
  await click('confirmImport');await page.getByRole('alert').filter({hasText:/fetch|network|Failed/i}).waitFor({timeout:65000});
  const retryResponse=page.waitForResponse((r:any)=>r.url().endsWith('/imports/commit'),{timeout:65000});await click('confirmImport');const retry=await(await retryResponse).json();
  await page.getByRole('status').filter({hasText:t('backupId')}).waitFor({timeout:65000});
  check('S29_lost_ack_retry_idempotent_mapping',dropped&&retry.mappingCount===1&&JSON.stringify(retry.receipt)===JSON.stringify(lostReceipt.receipt));
  const backupReceiptPreserved=retry.backupId===lostReceipt.backupId;report.checks.push({name:'S29_lost_ack_retry_preserves_backup_id',passed:backupReceiptPreserved});if(!backupReceiptPreserved)report.gaps.push({scenario:'S29',defect:'Committed cutover retry returns backupId:null; saved UI loses backup identifier',firstBackupPresent:typeof lostReceipt.backupId==='string',retryBackupPresent:typeof retry.backupId==='string'});
  await page.unroute('**/imports/commit');await page.locator('main form button:enabled').waitFor({timeout:65000});
  await writeFile(join(workspace,'tasks.json'),source+' ');await click('reload');await page.locator('.source-row .badge').filter({hasText:/^changed$/}).waitFor({timeout:65000});
  check('S29_postcutover_source_change_visible',true);await shot('S29-cutover-source-change');
  await click('reverseExport');await page.locator('.reverse-export pre').waitFor();const exported=await page.locator('.reverse-export pre').innerText();
  const proposal=await preview(exported,'export.json');await page.getByRole('status').filter({hasText:t('proposalHint')}).waitFor();
  check('S29_export_reimport_proposal_not_apply',proposal.mode==='normalized_proposal'&&await page.getByRole('button',{name:t('confirmImport'),exact:true}).isDisabled());await shot('S29-export-proposal');
 });
 await scenario('S30',async()=>{
  await nav('backup');const backupResponse=page.waitForResponse((r:any)=>r.url().endsWith('/backups'));await click('createBackup');const backup=await(await backupResponse).json();
  await page.getByRole('status').filter({hasText:t('backupCreated')}).waitFor();const visible=await page.locator('main pre').innerText();
  report.backupManifestKeys=Object.keys(backup.manifest??{});check('S30_backup_manifest_visible',visible.includes(backup.manifest.schemaVersion??'schema')&&visible.length>100);
  check('S30_backup_exclusions_visible',/exclud|credential|pairing/i.test(visible));
  await page.getByLabel(t('confirmRestore'),{exact:true}).check();const restoreResponse=page.waitForResponse((r:any)=>r.url().endsWith('/restores'));await click('restore');const restored=await(await restoreResponse).json();
  await page.getByRole('status').filter({hasText:t('restartPending')}).waitFor();
  check('S30_restore_separate_profile_visible',restored.requiresRestart===true&&restored.activeProfileChanged===false&&Boolean(restored.restoreId));
  report.restoreDirectoryEntries=await readdir(join(profile,'restores')).catch(()=>[]);check('S30_restore_new_directory_exists',report.restoreDirectoryEntries.length>0);await shot('S30-restore');
 });
 await scenario('S31',async()=>{
  // Separate SQL project setup avoids depending on S29 success and makes project isolation explicit.
  const task=newTask(other.id,'searchneedle проверка target','Synthetic searchable body',['Verify scope']);
  const seed=await api(`/projects/${other.id}/commands`,{expectedAuthorityEpoch:other.authorityEpoch,idempotencyKey:'search-seed',changes:[{expectedRevision:0,entity:task}]});check('S31_api_seed',seed.status===200);
  await page.locator('.navigation select').selectOption(other.id);await nav('search');
  async function search(query:string){await page.getByLabel(t('query'),{exact:true}).fill(query);const response=page.waitForResponse((r:any)=>r.url().includes('/search?q='));await page.locator('main form').getByRole('button',{name:t('search'),exact:true}).click();const value=await(await response).json();await page.locator('main form button:enabled').waitFor();return value;}
  const exact=await search('OTHR-1');check('S31_exact_public_key',exact.items?.[0]?.id===task.id&&await page.locator('main .records li').count()===1);
  const fts=await search('searchneedle');check('S31_fts_project_scope',fts.items?.length===1&&fts.items[0].id===task.id);
  const ru=await search('проверка');check('S31_russian_literal_fts',ru.items?.length===1);
  await search('notpresenttoken');check('S31_empty_visible',await page.locator('main [role=status]').innerText()===t('empty'));
  const partialId=randomUUID();const partialSetup=await api(`/projects/${other.id}/commands`,{expectedAuthorityEpoch:other.authorityEpoch,idempotencyKey:'partial-setup',changes:[{expectedRevision:0,entity:{id:partialId,kind:'session',title:'Incomplete synthetic session',coverage:'partial'}}]});report.partialSetupCode=partialSetup.body.error?.code;check('S31_api_partial_setup',partialSetup.status===200);
  await search('OTHR-1');check('S31_partial_distinct_from_empty_and_exact_works',await page.locator('main [role=status]').innerText()===t('partial')&&await page.locator('main .records li').count()===1);await shot('S31-partial');
  const storedTask=(await api(`/projects/${other.id}/entities/${task.id}`)).body;
  const removal=await api(`/projects/${other.id}/commands`,{expectedAuthorityEpoch:other.authorityEpoch,idempotencyKey:'delete-setup',changes:[{expectedRevision:1,entity:storedTask,delete:true},{expectedRevision:1,entity:{id:partialId,kind:'session',title:'Incomplete synthetic session',coverage:'partial'},delete:true}]});check('S31_api_deletion_setup',removal.status===200);
  await search('OTHR-1');check('S31_deleted_task_absent',await page.locator('main .records li').count()===0&&await page.locator('main [role=status]').innerText()===t('empty'));
  const rebuildResponse=page.waitForResponse((r:any)=>r.url().endsWith('/search/rebuild'));await click('rebuildSearch');const rebuild=await(await rebuildResponse).json();await page.locator('main [role=status]').filter({hasText:'complete'}).waitFor();check('S31_rebuild_action_complete',rebuild.coverage==='complete');await shot('S31-rebuild');
 });
 check('no_browser_page_errors',report.pageErrors.length===0);
}catch(error){report.gaps.push({scenario:'setup',error:String(error).slice(0,800)});}
finally{
 report.browserClosed=!context;report.serviceClosed=!service;report.fixtureCleaned=false;
 if(context)await context.close().then(()=>{report.browserClosed=true;}).catch((error:Error)=>report.gaps.push({scenario:'browser_cleanup',error:error.name}));
 if(service)await service.quit().then(()=>{report.serviceClosed=true;}).catch((error:Error)=>report.gaps.push({scenario:'service_cleanup',error:error.name}));
 report.fixtureContainmentVerified=resolve(root,'..')===scratch;
 if(report.fixtureContainmentVerified){
  await rm(root,{recursive:true,force:true,maxRetries:30,retryDelay:200}).catch((error)=>report.gaps.push({scenario:'cleanup',code:error.code,fixture:root}));
  try{await lstat(root);}catch(error){if((error as NodeJS.ErrnoException).code==='ENOENT')report.fixtureCleaned=true;else report.gaps.push({scenario:'cleanup_verification',code:(error as NodeJS.ErrnoException).code});}
 }else report.gaps.push({scenario:'cleanup',code:'FIXTURE_CONTAINMENT_REJECTED'});
 report.cleanup=report.browserClosed&&report.serviceClosed&&report.fixtureCleaned&&report.fixtureContainmentVerified;
 report.finishedAt=new Date().toISOString();report.status=report.gaps.length?'partially_verified':'passed_browser_synthetic';
 const text=JSON.stringify(report,null,2);await writeFile(join(output,'receipt.json'),text);console.log(JSON.stringify({receipt:join(output,'receipt.json'),sha256:createHash('sha256').update(text).digest('hex'),status:report.status,checks:report.checks,gaps:report.gaps}));if(report.gaps.length)process.exitCode=1;
}

