import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {createHash,randomUUID} from 'node:crypto';
import {mkdir,mkdtemp,readFile,readdir,realpath,rm,writeFile} from 'node:fs/promises';
import {basename,dirname,isAbsolute,join,resolve} from 'node:path';
import {tmpdir} from 'node:os';
import {pathToFileURL} from 'node:url';
import {createLocalApplication} from '../../../apps/local-service/src/http/application.mts';
import {toFetchRequest} from '../../../apps/local-service/src/main.mts';
import {openLocalStore} from '../../../apps/local-service/src/storage/local-store.mts';
import {newM2Task} from '../../../packages/contracts/issues/task-profile.ts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';
import {uiLabel} from '../../../apps/web/src/locales/messages.ts';
import {compositionFindings} from '../../../tools/project-methodology/design.mts';

const args=process.argv.slice(2);
assert.equal(args[0],'--synthetic-browser');
assert.equal(args.length,7);
const provided=Object.fromEntries([[args[1],args[2]],[args[3],args[4]],[args[5],args[6]]]);
for(const key of ['--playwright-core','--chromium','--evidence'])assert.ok(isAbsolute(provided[key]));
const temp=await realpath(tmpdir()),root=await mkdtemp(join(temp,'paos-b2-browser-'));
const workspace=join(root,'workspace'),profile=join(root,'profile'),home=join(root,'browser');
await Promise.all([workspace,profile,home].map(dir=>mkdir(dir)));
const dist=resolve('apps/web/dist'), out=await mkdtemp(join(await realpath(provided['--evidence']),'pmeth-b3-'));
const fixture=JSON.parse(await readFile(new URL('../../fixtures/product_agent_os/pmeth-b1-synthetic.json',import.meta.url),'utf8'));
const composition=JSON.parse(await readFile(new URL('../../fixtures/product_agent_os/pmeth-b3-composition.json',import.meta.url),'utf8'));
for(const [name,data] of Object.entries<string>(fixture.files))await writeFile(join(workspace,name),data);
await writeFile(join(workspace,'.env'),'B2_SYNTHETIC_CANARY=do_not_project');
const sha=(input:Buffer)=>createHash('sha256').update(input).digest('hex');
const hashes=async()=>Object.fromEntries(await Promise.all((await readdir(workspace)).sort().map(async file=>[file,sha(await readFile(join(workspace,file)))])));
const original=await hashes();
const report={passed:false,checks:[] as string[],screenshots:[] as string[],errors:[] as string[],externalRequests:[] as string[],
 targetPreserved:false,cleanup:false,buildHashes:{} as Record<string,string>,sourceHashes:{} as Record<string,string>,
 adapterSourceRevision:null as string|null,browserVersion:null as string|null};
let store:Awaited<ReturnType<typeof openLocalStore>>|undefined;
let app:Awaited<ReturnType<typeof createLocalApplication>>|undefined;
let context:any;
let origin='';
const server=createServer(async(incoming,outgoing)=>{
 const controller=new AbortController();
 outgoing.once('close',()=>{if(!outgoing.writableFinished)controller.abort();});
 try{
  const result=await app!.handleRequest(await toFetchRequest(incoming,origin,controller.signal));
  outgoing.statusCode=result.status;
  for(const [key,value] of result.headers)if(key!=='set-cookie')outgoing.setHeader(key,value);
  const cookies=result.headers.getSetCookie();if(cookies.length)outgoing.setHeader('Set-Cookie',cookies);
  outgoing.end(Buffer.from(await result.arrayBuffer()));
 }catch{if(!outgoing.destroyed){outgoing.writeHead(500);outgoing.end();}}
});
function checked(name:string,ok:unknown){assert.ok(ok,name);report.checks.push(name);}
try{
 await new Promise<void>((done,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',done);});
 const address=server.address();assert.ok(address&&typeof address==='object');
 origin='http://127.0.0.1:'+address.port;
 store=await openLocalStore({databasePath:join(profile,'state.sqlite')});
 app=await createLocalApplication({store,origin,instanceId:randomUUID(),profileDirectory:profile,staticDirectory:dist,assetRoots:[]});
 const {chromium}=await import(pathToFileURL(join(provided['--playwright-core'],'index.mjs')).href);
 context=await chromium.launchPersistentContext(home,{headless:true,chromiumSandbox:true,serviceWorkers:'block',
  viewport:{width:1360,height:1000},executablePath:provided['--chromium'],
  env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:home,HOME:home,APPDATA:home,LOCALAPPDATA:home,TEMP:home,TMP:home}});
 await context.route('**/*',async(r:any)=>{
  if(new URL(r.request().url()).origin===origin)await r.continue();
  else{report.externalRequests.push(new URL(r.request().url()).origin);await r.abort();}
 });
 const page=context.pages()[0]??await context.newPage();
 page.setDefaultTimeout(12_000);
 const cdp=await context.newCDPSession(page);
 report.browserVersion=(await cdp.send('Browser.getVersion')).product;
 await cdp.detach();
 page.on('pageerror',(error:Error)=>report.errors.push(error.message));
 page.on('console',(message:any)=>{
  if(message.type()!=='error')return;
  const url=message.location().url,text=message.text();
  if(url.endsWith('/api/v1/session')&&text.includes('status of 401'))return; // Pairing begins without a local session.
  if(url.endsWith('/analysis/task-advice')&&text.includes('status of 403'))return; // Intentional permission fixture.
  report.errors.push(text);
 });
 await page.goto(origin);
 checked('page identity',page.url()===origin+'/'&&(await page.title()).includes('Product-Agent OS'));
 const exchange=page.waitForResponse((response:any)=>response.url().endsWith('/bootstrap/exchange')&&response.status()===200);
 await page.getByLabel(appLabel('ru','code'),{exact:true}).fill(app.issuePairingCode());
 await page.getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();
 const csrf=(await(await exchange).json()).csrfToken;
 async function api(path:string,input?:unknown,method=input===undefined?'GET':'POST'){
  const response=await context.request.fetch(origin+'/api/v1'+path,{method,headers:{origin,'x-paos-csrf':csrf},data:input});
  return {status:response.status(),body:await response.json()};
 }
 const added=await api('/projects',{name:'B2 synthetic',keyPrefix:'PMBX',workspaceRoot:workspace,scan:false,requestId:randomUUID()});
 assert.equal(added.status,201,added.body?.error?.code);
 const id=added.body.id,base='/projects/'+id;
 const tasks:Record<string,string>={};
 for(const [name,row] of Object.entries<any>(fixture.cases)){
  const taskId=randomUUID();tasks[name]=taskId;
  const task={...newM2Task(id,taskId,row.task.intent,'local-user'),type:name==='backend_bug'?'bug':'task',
   summary:'Synthetic scenario',technicalValue:'Decision parity',productValue:'Review the next step',
   files:row.task.changed_paths.map((relativePath:string)=>({relativePath,plannedOperation:'modify',actualOperation:null})),
   acceptanceCriteria:row.task.acceptance};
  assert.equal((await api(base+'/task-manager/commands',{action:'save',idempotencyKey:randomUUID(),expectedAuthorityEpoch:1,expectedRevision:0,task})).status,200);
 }
 async function completedScan(path:string){
  assert.equal((await api(base+path,{requestId:randomUUID()})).status,202);
  for(let attempt=0;attempt<100;attempt++){
   const snapshot=(await api(base+'/scans')).body;
   if(['completed','partial','failed'].includes(snapshot.latest?.state))return snapshot.latest;
   await new Promise(done=>setTimeout(done,50));
  }
  throw Error('SCAN_TIMEOUT');
 }
 async function openTask(locale:'ru'|'en',caseName:string){
  await page.locator('.navigation select:enabled').selectOption(id);
  await page.locator('nav').getByRole('button',{name:uiLabel(locale,'nav.tasks'),exact:true}).click();
  const card=page.locator('[data-task-id="'+tasks[caseName]+'"]').first();
  await card.focus();await page.keyboard.press('Enter');
  const panel=page.getByTestId('task-advice');
  await panel.locator(':scope > summary').focus();await page.keyboard.press('Enter');
  checked('keyboard opens recommendation '+locale+' '+caseName,await panel.getAttribute('open')!==null);
  return panel;
 }
 async function press(panel:any){
  await panel.locator('button[type=submit]').focus();await page.keyboard.press('Enter');
 }
 async function prepare(panel:any,caseName:string){
  if(caseName==='docs_only')await panel.locator('[name=advice-source]').fill('counter.py');
  else{
   await panel.locator('[name=advice-test]').fill('test_counter.py');
   await panel.locator('[name=advice-command]').fill(fixture.cases.backend_bug.expected.target);
  }
 }
 const endpoint='**/analysis/task-advice';
 let adviceRequests=0;
 page.on('request',(request:any)=>{if(request.url().endsWith('/analysis/task-advice'))adviceRequests++;});
 await page.reload();
 let panel=await openTask('ru','docs_only');
 await prepare(panel,'docs_only');await press(panel);
 await panel.locator('[data-state=unavailable]').waitFor();
 checked('missing analysis is explicit',(await panel.innerText()).includes('Запустите сканирование'));
 const first=await completedScan('/scans');
 await completedScan('/database/scan');await completedScan('/code-database/scan');
 for(const [locale,theme,caseName] of [
  ['ru','light','backend_bug'],['ru','dark','docs_only'],['en','light','backend_bug'],['en','dark','docs_only'],
 ] as const){
  assert.equal((await api('/preferences',{locale,theme},'PUT')).status,200);
  await page.reload();
  await page.waitForFunction((settings:any)=>document.documentElement.lang===settings.locale&&document.documentElement.dataset.theme===settings.theme,{locale,theme});
  panel=await openTask(locale,caseName);
  await prepare(panel,caseName);
  const reply=page.waitForResponse((response:any)=>response.url().endsWith('/analysis/task-advice'));
  await press(panel);
  const advice=await(await reply).json();
  await panel.locator('[data-state=ready]').waitFor();
  report.adapterSourceRevision=advice.adapterSourceRevision;
  checked('real bridge step '+locale,advice.decision.plan.next_step.target===fixture.cases[caseName].expected.target);
  checked('analysis retained through selective scans '+locale,advice.analysisScanId===first.scanId);
  checked('read-only rendering '+locale,(await panel.innerText()).includes(locale==='ru'?'Режим просмотра':'Read-only'));
  checked('no framework overlay '+locale,await page.locator('vite-error-overlay').count()===0);
  checked('isolated layout '+locale,await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1));
  const regions=await panel.evaluate((element:HTMLElement,selectors:Record<string,string>)=>
   Object.entries(selectors).flatMap(([name,selector])=>{
    const region=element.querySelector(selector)?.getBoundingClientRect();
    return region?[{name,top:region.top,bottom:region.bottom,left:region.left,right:region.right}]:[];
   }).sort((a,b)=>a.top-b.top),composition.selectors);
  checked('reviewed region order and geometry '+locale+' '+theme,compositionFindings(composition.expected,regions,1360).length===0);
  checked('wrong order fails despite same dimensions '+locale+' '+theme,
   compositionFindings(composition.intentionalMismatch,regions,1360).includes('REGION_ORDER_MISMATCH'));
  await panel.locator(':scope > summary').scrollIntoViewIfNeeded();
  const screenshot=join(out,locale+'-'+theme+'.png');await page.screenshot({path:screenshot});report.screenshots.push(screenshot);
 }
 await page.setViewportSize({width:400,height:900});
 await panel.getByText('Scope and sources',{exact:true}).click();
 await panel.locator(':scope > summary').scrollIntoViewIfNeeded();
 checked('narrow layout',await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1));
 const narrowBody=await panel.evaluate((el:HTMLElement)=>{
  const advice=el.getBoundingClientRect();
  const sidebar=el.closest('.task-detail-body')!.querySelector('.task-context')!.getBoundingClientRect();
  return {width:advice.width,stacked:advice.bottom<=sidebar.top,leftAligned:sidebar.left<=advice.left};
 });
 checked(`narrow recommendation uses the task body width (${narrowBody.width}px)`,narrowBody.width>=280);
 checked('narrow expanded task stacks its context below the recommendation',narrowBody.stacked&&narrowBody.leftAligned);
 checked('long source revision visible and contained',await panel.locator('details code').first().count()>0
  && await panel.evaluate((el:HTMLElement)=>el.scrollWidth<=el.clientWidth+1));
 const narrow=join(out,'en-dark-narrow.png');await page.screenshot({path:narrow});report.screenshots.push(narrow);
 await page.setViewportSize({width:1360,height:1000});
 checked('wide expanded task keeps its context to the right',await panel.evaluate((el:HTMLElement)=>
  el.getBoundingClientRect().right<=el.closest('.task-detail-body')!.querySelector('.task-context')!.getBoundingClientRect().left));
 const was=adviceRequests;
 await panel.locator('[name=advice-source]').fill('.env');
 checked('unsubmitted inputs clear obsolete advice without sending',adviceRequests===was&&await panel.getByTestId('task-advice-result').count()===0);
 await press(panel);
 await panel.locator('[data-state=partial]').waitFor();
 checked('sensitive source is not projected',!(await page.content()).includes('do_not_project'));
 let release!:()=>void;
 const waiting=new Promise<void>(done=>release=done);
 await context.route(endpoint,async(route:any)=>{await waiting;await route.continue();});
 try{
  await prepare(panel,'docs_only');await press(panel);
  await panel.getByText('Checking task context…',{exact:true}).waitFor();
  checked('loading state announced',true);
 }finally{release();}
 await panel.locator('[data-state=ready]').waitFor();
 await context.unroute(endpoint);
 await context.route(endpoint,async(route:any)=>{
  const response=await route.fetch(),data=await response.json();
  await route.fulfill({response,json:{...data,projectId:'other',taskId:'other'}});
 });
 await prepare(panel,'docs_only');await press(panel);
 await panel.getByTestId('task-advice-error').waitFor();
 checked('wrong project and task payload rejected',(await panel.innerText()).includes('TASK_ADVICE_SCOPE_MISMATCH'));
 await context.unroute(endpoint);
 await context.route(endpoint,(route:any)=>route.fulfill({status:403,json:{error:{code:'CSRF_INVALID'}}}));
 await press(panel);await panel.getByTestId('task-advice-error').waitFor();
 checked('permission state visible',(await panel.innerText()).includes('Access to the current project is required'));
 await context.unroute(endpoint);
 await writeFile(join(workspace,'counter.py'),fixture.files['counter.py']+'# revision drift\n');
 try{await press(panel);await panel.locator('[data-state=stale]').waitFor();checked('source drift invalidates recommendation',true);}
 finally{await writeFile(join(workspace,'counter.py'),fixture.files['counter.py']);}
 checked('no application errors',report.errors.length===0);
 checked('no external requests',report.externalRequests.length===0);
 assert.deepEqual(await hashes(),original);
 report.targetPreserved=true;
 for(const file of await readdir(join(dist,'assets')))report.buildHashes[file]=sha(await readFile(join(dist,'assets',file)));
 for(const file of ['apps/local-service/src/http/application.mts','apps/local-service/src/project-analysis/bridge.py',
  'apps/local-service/src/project-analysis/service.mts','apps/local-service/src/project-analysis/task-advice.mts',
  'apps/local-service/src/project-scans/service.mts','apps/web/src/api/client.ts','apps/web/src/features/tasks/TaskAdvicePanel.tsx',
  'apps/web/src/features/tasks/TaskManager.tsx','apps/web/src/features/tasks/task-detail.css','apps/web/src/design/parity.css','packages/contracts/project-analysis.ts',
  'tests/web/single-window/methodology-advice-browser-acceptance.mts','tools/project-methodology/design.mts',
  'tests/fixtures/product_agent_os/pmeth-b3-composition.json']){
  report.sourceHashes[file]=sha(await readFile(file));
 }
 report.passed=true;
}finally{
 try{
  await context?.close();
  await new Promise<void>(done=>server.close(()=>done()));
  await app?.close();await store?.close();
  const resolved=await realpath(root);
  assert.equal(dirname(resolved),temp);assert.ok(basename(resolved).startsWith('paos-b2-browser-'));
  await rm(resolved,{recursive:true,force:true});report.cleanup=true;
 }finally{
  await writeFile(join(out,'result.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify({evidence:join(out,'result.json'),checks:report.checks.length,passed:report.passed&&report.cleanup}));
 }
}
