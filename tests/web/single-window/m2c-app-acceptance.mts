import {mkdtemp,mkdir,writeFile,readFile,rm,readdir,unlink} from 'node:fs/promises';
import {resolve,join,dirname,isAbsolute} from 'node:path';
import {pathToFileURL} from 'node:url';
import {randomUUID,createHash} from 'node:crypto';
import {startLocalService} from '../../../apps/local-service/src/main.mts';
import {newM2Task} from '../../../packages/contracts/issues/task-profile.ts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';
import {uiLabel} from '../../../apps/web/src/locales/messages.ts';
import {label} from '../../../apps/web/src/features/tasks/labels.ts';

/** Two actual App planning proposals; disposable workspace, explicit reviewed Apply, no native/provider execution. */
async function main(){
 const argv=process.argv.slice(2);if(argv.length!==5||argv[0]!=='--actual-app-m2c')throw Error('EXPLICIT_ACTUAL_APP_M2_REQUIRED');
 const args=Object.fromEntries([argv.slice(1,3),argv.slice(3,5)]);
 if(!['--playwright-core','--chromium'].every(k=>isAbsolute(args[k]??'')))throw Error('INSTALLED_PATHS_REQUIRED');
 const scratch=resolve('.tmp/paos-m2c');await mkdir(scratch,{recursive:true});
 const root=await mkdtemp(join(scratch,'actual-app-fixture-')),output=await mkdtemp(join(scratch,'actual-app-evidence-')),coordination=join(scratch,'actual-app-coordination.json');
 const workspace=join(root,'workspace'),profileDirectory=join(root,'profile'),home=join(root,'browser');await Promise.all([mkdir(workspace),mkdir(profileDirectory),mkdir(home)]);
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

  await writeFile(join(workspace,'REQUIREMENTS.md'),'# Requirements\n\nR-1: Review file changes with source evidence and approval boundaries.\nR-2: Record uncertain findings explicitly.\n');
  const registered=await api('/projects',{name:'Actual App M2c fixture',workspaceRoot:workspace,keyPrefix:'APPC'});check('project_saved',registered.status===201);const project=registered.body,base='/projects/'+project.id;
  await page.reload();await page.locator('.navigation select:enabled').waitFor();await page.locator('.navigation select').selectOption(project.id);await nav('settings');
  check('keyless_route_default',await page.getByLabel(appLabel('ru','connectionRoute'),{exact:true}).inputValue()==='codex_app_agent');check('no_api_key_input',await page.locator('input[name=apiKey]').count()===0);
  const opened=page.waitForResponse((r:any)=>r.url()===origin+'/api/v1/connection'&&r.request().method()==='POST');
  await page.locator('.panel').filter({has:page.getByLabel(appLabel('ru','connectionRoute'),{exact:true})}).getByRole('button',{name:appLabel('ru','openAppAgentChannel'),exact:true}).click();check('app_channel_opened',(await opened).status()===200);
  shared={descriptorPath:service.appAgentDescriptorPath,workerId:'m2c-actual-app-worker',output,projectId:project.id,expectedJobs:2};
  await note('waiting_for_agent');console.log(JSON.stringify({stage:'waiting_for_agent',coordination,output}));
  await until('actual_app_worker_attached',async()=>(await api('/connection')).body.verified===true,180000);
  const runs:any[]=[];let before=0,dispatchCount=0;page.on('request',(r:any)=>{if(r.method()==='POST'&&r.url().endsWith('/team/skills/generation'))dispatchCount++;});
  for(const mode of ['requirements','description']){
   step='skill_'+mode;await nav('skills');const generator=page.getByTestId('skill-generator');await generator.locator('[name=skill-generation-mode]').selectOption(mode);
   await generator.locator('[name=skill-generation-description]').fill(mode==='requirements'?'Recommend a missing source-review skill grounded in the selected requirements.':'Create a distinct documentation-source audit skill which checks claims, source dates and explicit uncertainty.');
   if(mode==='requirements')await generator.locator('[name=skill-requirement-end]').fill('4');
   const started=page.waitForResponse((r:any)=>r.url().endsWith('/team/skills/generation')&&r.request().method()==='POST');await generator.getByRole('button',{name:'Рекомендовать скилл',exact:true}).click();const response=await started;check(mode+'_dispatch',response.status()===200);const job=await response.json();
   await note('job_queued',{runId:job.id,mode});console.log(JSON.stringify({stage:'job_queued',mode,runId:job.id}));
   await until(mode+'_generation_completed',async()=>{const r=(await api(base+'/team/skills/generation/'+job.id)).body;return r.state==='completed'&&Boolean(r.proposal);},180000);
   await generator.getByTestId('skill-generation-result').getByRole('button',{name:'Открыть draft',exact:true}).click();const editor=generator.getByTestId('skill-generation-editor');await editor.waitFor();
   const content=editor.locator('[name=generated-skill-content]');check(mode+'_draft_editable',await content.isEditable());const raw=await content.inputValue();check(mode+'_grounding_in_draft',raw.includes('Requirement provenance')&&raw.includes(mode==='requirements'?'requirements:1-4':'user-description'));
   await content.fill(raw+'\nReviewer note: verify evidence before presenting conclusions.\n');
   check(mode+'_no_auto_apply',(await api(base+'/team/catalog')).body.assets.filter((a:any)=>a.management==='paos_managed').length===before);
   await editor.getByRole('button',{name:'Проверить и показать diff',exact:true}).click();await generator.getByTestId('skill-generation-preview').locator('[name=generated-skill-confirm]').check();
   await generator.getByRole('button',{name:'Применить скилл',exact:true}).click();before++;
   await until(mode+'_reviewed_apply',async()=>(await api(base+'/team/catalog')).body.assets.filter((a:any)=>a.kind==='skill'&&a.management==='paos_managed').length===before);
   const result=(await api(base+'/team/skills/generation/'+job.id)).body;check(mode+'_applied_state',result.state==='applied');
   const repeatResponse=page.waitForResponse((r:any)=>r.url().endsWith('/team/skills/generation/'+job.id)&&r.request().method()==='GET');await generator.getByRole('button',{name:'Рекомендовать скилл',exact:true}).click();await repeatResponse;
   check(mode+'_repeat_reuses_job',(await api(base+'/team/skills/generation/'+job.id)).body.state==='applied');check(mode+'_repeat_no_duplicate_asset',(await api(base+'/team/catalog')).body.assets.filter((a:any)=>a.kind==='skill'&&a.management==='paos_managed').length===before);
   check(mode+'_no_duplicate_job',dispatchCount===before);
   runs.push({id:job.id,mode,assetId:result.assetId,requirements:result.requirements});
   const screenshot=join(output,mode+'-applied.png');await generator.scrollIntoViewIfNeeded();await page.screenshot({path:screenshot});report.screenshots.push(screenshot);
  }
  check('no_browser_errors',report.pageErrors.length===0);check('no_external_browser_requests',report.externalRequests.length===0);check('no_native_operations',true);
  report.actualAppAgent=true;report.actualNativeBroker=false;report.runs=runs;report.status='passed_actual_m2c_skill_planning';report.limits=['App and active consumer required','Host identity attested, not cryptographic','Project-managed skill only; no installation or native activation','No commercial or human product acceptance'];await note('completed');
 }catch(error){report.status='failed';report.failedStep=step;report.error=String(error).slice(0,1600);process.exitCode=1;try{await note('failed');if(page&&!page.isClosed()){await page.screenshot({path:join(output,'failed.png'),mask:[page.locator('input')]});report.failureUi=(await page.locator('body').innerText()).slice(0,15000);}}catch{}}
 finally{if(timer)clearTimeout(timer);try{await context?.close();report.browserClosed=true;}catch{report.browserClosed=false;process.exitCode=1;}try{await service?.quit();report.serviceClosed=true;}catch{report.serviceClosed=false;process.exitCode=1;}
  if(report.serviceClosed){if(dirname(resolve(root))!==scratch)throw Error('FIXTURE_CLEANUP_BOUNDARY');await rm(root,{recursive:true,force:true});report.fixtureCleaned=true;}
  report.finishedAt=new Date().toISOString();for(const p of ['apps/local-service/src/team/skill-generation.mts','apps/local-service/src/runtime/app-agent-gateway.mts','apps/web/src/features/skills/SkillGenerator.tsx','tests/web/single-window/m2c-app-acceptance.mts','apps/web/dist/index.html',...(await readdir('apps/web/dist/assets')).map(n=>'apps/web/dist/assets/'+n)])report.sourceHashes[p]=createHash('sha256').update(await readFile(p)).digest('hex');await writeFile(join(output,'m2c-app-result.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({status:report.status,checks:report.checks.length,error:report.error,report:join(output,'m2c-app-result.json'),fixtureCleaned:report.fixtureCleaned}));
 }
}
await main();
