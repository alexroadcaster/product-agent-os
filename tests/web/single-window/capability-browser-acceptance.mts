import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {mkdtemp,mkdir,writeFile,readFile,readdir,rm,lstat} from 'node:fs/promises';
import {join,resolve,relative,dirname,isAbsolute} from 'node:path';
import {pathToFileURL} from 'node:url';
import {randomUUID,createHash} from 'node:crypto';
import {openLocalStore} from '../../../apps/local-service/src/storage/local-store.mts';
import {createLocalApplication} from '../../../apps/local-service/src/http/application.mts';
import {createAppAgentGateway} from '../../../apps/local-service/src/runtime/app-agent-gateway.mts';
import {createTeamService} from '../../../apps/local-service/src/team/service.mts';
import {taskManagerCommand} from '../../../apps/local-service/src/task-manager/service.mts';
import {newM2Task} from '../../../packages/contracts/issues/task-profile.ts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';
import {uiLabel} from '../../../apps/web/src/locales/messages.ts';
import {fixtureFetch,revision as fixtureRevision} from '../remote-skill-fixture.mts';

const argv=process.argv.slice(2);
if(argv[0]!=='--synthetic-browser'||![5,7].includes(argv.length))throw Error('EXPLICIT_SYNTHETIC_BROWSER_REQUIRED');
const options=Object.fromEntries(Array.from({length:(argv.length-1)/2},(_v,i)=>argv.slice(1+i*2,3+i*2)));
if(Object.keys(options).length!==(argv.length-1)/2||Object.keys(options).some(key=>!['--playwright-core','--chromium','--phase'].includes(key))||['--playwright-core','--chromium'].some(key=>!isAbsolute(options[key]??''))||options['--phase']!==undefined&&!['visual-red','final'].includes(options['--phase']))throw Error('INSTALLED_BROWSER_PATH_REQUIRED');
const scratch=resolve('.tmp/func-g07/browser-acceptance');await mkdir(scratch,{recursive:true});
const fixture=await mkdtemp(join(scratch,'fixture-')),out=await mkdtemp(join(scratch,'evidence-'));
const workspace=join(fixture,'workspace'),other=join(fixture,'other'),profile=join(fixture,'profile'),home=join(fixture,'chromium');
for(const path of [workspace,other,profile,home])await mkdir(path);
const sourceBefore='# Synthetic G07 file guide\n\nOriginal source.\n',sourceAfter=sourceBefore+'Reviewed source change.\n';
await writeFile(join(workspace,'guide.md'),sourceBefore);
await writeFile(join(other,'other.md'),'# Independent project guide\n');
for(const root of [workspace,other])for(const name of ['AGENTS.md','REQUIREMENTS.md','PLAN.md','TEST.md','EVALS.md','RUNLOG.md'])await writeFile(join(root,name),'# Synthetic '+name+'\n\nFixture-only project documentation. Preserve bounded checks and source evidence.\n');
const sqlBefore='# Synthetic G07 SQL guide\n\nOriginal stored document.\n',sqlAfter=sqlBefore+'Reviewed stored change.\n';
const external=fixtureFetch(true),sha=(value:Buffer|string)=>createHash('sha256').update(value).digest('hex');
const report:any={startedAt:new Date().toISOString(),syntheticOnly:true,browserPlugin:'not_available',fallback:'installed Playwright; Browser plugin not available',providerCalls:0,realCredentials:false,humanAcceptance:false,checks:[],screenshots:[],pageErrors:[],consoleErrors:[],externalRequests:[],apiResponses:[],fixtureTransport:{source:'anonymous fixed-source fixture transport, not live GitHub qualification',revision:fixtureRevision},gatewayFixture:{route:'real App-agent gateway lifecycle',executor:'none; connected worker is not execution-qualified',clock:'controlled server clock; independent 4s expected duration'},expectedHttpFailures:[],restartScope:'actual application/gateway/store close and reopen; not OS process or closed Codex App'};
report.phase=options['--phase']==='visual-red'?'visual_red_not_current_build':'final';report.sourceAndDistAlignment=options['--phase']==='visual-red'?'intentionally_previous_build_for_visual_regression':'current_build_claim_requires_root_source_build_evidence';
let app:any,store:any,gateway:any,server:any,context:any,page:any,origin='',csrf='',stage='setup',locale:'ru'|'en'='ru',project:any,second:any,workerAuth:any;
let clock=Date.now()-60000,instance=0,measured:any,agentId='',taskId='',activeHttp=0;
const w=(ru:string,en:string)=>locale==='ru'?ru:en;
async function hashes(root:string,prefix=''):Promise<Record<string,string>>{const result:Record<string,string>={};for(const entry of await readdir(join(root,prefix),{withFileTypes:true})){const path=prefix?prefix+'/'+entry.name:entry.name;if(entry.isDirectory())Object.assign(result,await hashes(root,path));else if(entry.isFile())result[path]=sha(await readFile(join(root,path)));}return result;}
async function bindings(){const result:Record<string,string>={};for(const root of ['apps/web/src','apps/local-service/src','packages/contracts'])for(const [path,hash] of Object.entries(await hashes(resolve(root))))result[root+'/'+path]=hash;for(const path of ['apps/web/package-lock.json','tests/web/remote-skill-fixture.mts','tests/web/single-window/capability-browser-acceptance.mts'])result[path]=sha(await readFile(path));return result;}
async function until(name:string,fn:()=>Promise<boolean>,milliseconds=20000){const deadline=Date.now()+milliseconds;for(;;){if(await fn())return;if(Date.now()>=deadline)throw Error(name);await new Promise(r=>setTimeout(r,30));}}
async function observed<T>(name:string,promise:Promise<T>):Promise<T>{let timer:ReturnType<typeof setTimeout>|undefined;try{return await Promise.race([promise,new Promise<T>((_resolve,reject)=>{timer=setTimeout(()=>reject(Error(name)),20000);})]);}finally{if(timer)clearTimeout(timer);}}
async function check(name:string,fn:()=>Promise<void>){stage=name;await writeFile(resolve('.tmp/func-g07/browser-progress.json'),JSON.stringify({stage,checks:report.checks.length,pid:process.pid}));const began=performance.now();await fn();report.checks.push({name,passed:true,elapsedMs:performance.now()-began});}
async function shot(name:string){const path=join(out,name+'.png');await page.screenshot({path,fullPage:false});report.screenshots.push(relative(resolve('.'),path).replaceAll('\\','/'));}
async function api(path:string,input?:unknown,method?:string){return page.evaluate(async({path,input,csrf,method}:any)=>{const response=await fetch('/api/v1'+path,{method:method??(input===undefined?'GET':'POST'),headers:{'content-type':'application/json','x-paos-csrf':csrf},...(input===undefined?{}:{body:JSON.stringify(input)})});return {status:response.status,body:await response.json()};},{path,input,csrf,method});}
async function nav(section:string){const menu=page.getByRole('button',{name:appLabel(locale,'menu'),exact:true});if(await menu.isVisible()&&await menu.getAttribute('aria-expanded')!=='true')await menu.click();await page.locator('.navigation nav').getByRole('button',{name:uiLabel(locale,('nav.'+section) as any),exact:true}).click();}
async function selectProject(id:string){const menu=page.getByRole('button',{name:appLabel(locale,'menu'),exact:true});if(await menu.isVisible()&&await menu.getAttribute('aria-expanded')!=='true')await menu.click();await page.locator('.navigation select').selectOption(id);if(await menu.isVisible()&&await menu.getAttribute('aria-expanded')==='true')await menu.click();}
async function pair(){await page.getByLabel(/Код сопряжения|Pairing code/).waitFor();const ru=await page.getByLabel(appLabel('ru','code'),{exact:true}).isVisible(),language=ru?'ru':'en';await page.getByLabel(appLabel(language,'code'),{exact:true}).fill(app.issuePairingCode());const response=page.waitForResponse((r:any)=>r.url().endsWith('/bootstrap/exchange')&&r.status()===200);await page.getByRole('button',{name:appLabel(language,'connect'),exact:true}).click();csrf=(await(await response).json()).csrfToken;await page.locator('.navigation select:enabled').waitFor();}
async function boot(){
 gateway=createAppAgentGateway({store,profileId:'g07-browser-profile',actorId:'synthetic-app-consumer',assetRoots:[],now:()=>clock});
 await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'g07-browser-worker',generation:'g07-generation-'+(++instance)});workerAuth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};
 app=await createLocalApplication({store,origin,instanceId:randomUUID(),profileDirectory:profile,staticDirectory:resolve('apps/web/dist'),assetRoots:[],runtime:gateway.runtime,connection:gateway.connection,externalSkillFetch:external.fetcher});
}
let timer:ReturnType<typeof setTimeout>|undefined;
try{
 report.targetInitialHashes=await hashes(workspace);report.otherInitialHashes=await hashes(other);report.sourceHashes=await bindings();report.buildHashes=await hashes(resolve('apps/web/dist'));
 store=await openLocalStore({databasePath:join(profile,'state.sqlite')});
 server=createServer(async(req,res)=>{activeHttp++;try{const chunks:Buffer[]=[];for await(const chunk of req)chunks.push(Buffer.from(chunk));const headers=new Headers();for(const [key,value] of Object.entries(req.headers))if(value!==undefined)headers.set(key,Array.isArray(value)?value.join(','):value);const response=await app.handleRequest(new Request(origin+req.url,{method:req.method,headers,...(!['GET','HEAD'].includes(req.method??'GET')?{body:Buffer.concat(chunks)}:{})})),bytes=Buffer.from(await response.arrayBuffer());if(req.url?.startsWith('/api/v1')){let code:string|undefined;if(response.status>=400)try{code=JSON.parse(bytes.toString()).error?.code;}catch{}report.apiResponses.push({path:req.url.split('?')[0],status:response.status,bytes:bytes.length,...(code?{code}:{})});}res.statusCode=response.status;for(const [key,value] of response.headers)res.setHeader(key,value);res.end(bytes);}catch{res.writeHead(500,{'content-type':'application/json'});res.end('{"error":{"code":"SYNTHETIC_HTTP_FAILURE"}}');}finally{activeHttp--;}});
 await new Promise<void>(r=>server.listen(0,'127.0.0.1',r));origin='http://127.0.0.1:'+server.address().port;await boot();
 const {chromium}=await import(pathToFileURL(join(options['--playwright-core'],'index.mjs')).href);
 context=await chromium.launchPersistentContext(home,{headless:true,chromiumSandbox:true,serviceWorkers:'block',viewport:{width:1440,height:1000},executablePath:options['--chromium'],env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:home,HOME:home,APPDATA:home,LOCALAPPDATA:home,TEMP:home,TMP:home}});
 timer=setTimeout(()=>void context.close(),300000);
 await context.route('**/*',async(route:any)=>{const url=new URL(route.request().url());if(url.origin!==origin){report.externalRequests.push(url.origin);await route.abort();}else await route.continue();});
 page=context.pages()[0];page.setDefaultTimeout(20000);page.on('pageerror',(e:Error)=>report.pageErrors.push(e.message));page.on('console',(m:any)=>{if(m.type()==='error')report.consoleErrors.push(m.text());});await page.goto(origin);await pair();
 project=(await api('/projects',{name:'Synthetic G07 Primary',workspaceRoot:workspace,keyPrefix:'GPRI',requestId:'g07-primary',scan:false})).body;second=(await api('/projects',{name:'Synthetic G07 Other',workspaceRoot:other,keyPrefix:'GOTH',requestId:'g07-other',scan:false})).body;
 await store.write({projectId:project.id,actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'g07-sql-document',changes:[{expectedRevision:0,entity:{id:'g07-sql-guide',kind:'document',title:'Synthetic G07 SQL guide',body:sqlBefore}}]});
 await page.reload();await page.locator('.navigation select:enabled').waitFor();await selectProject(project.id);
 await check('Connected worker displays action-local execution limits before use',async()=>{
  await nav('settings');await page.locator('[data-settings-section=connection]').click();await page.getByRole('heading',{name:appLabel(locale,'connection'),exact:true}).waitFor();
  assert.equal(await page.getByTestId('capability-runtime').count(),1,'attached worker needs an explicit execution capability explanation');
  const note=page.getByTestId('capability-runtime');assert.equal(await note.getAttribute('data-capability-state'),'connected');
  assert.ok((await note.innerText()).includes('PAOS'));assert.ok((await page.locator('.connection-chip').innerText()).includes(appLabel(locale,'appWorkerConnected')),'global connection badge must name attachment scope');assert.equal(await page.locator('.navigation .connection').getAttribute('title'),appLabel(locale,'appWorkerConnected'));await shot('connected-is-not-qualified');
 });
 for(const language of ['ru','en'] as const)for(const theme of ['light','dark'])await check(language+'/'+theme+' action-local scope, reason and next action remain readable and keyboard accessible',async()=>{
  assert.equal((await api('/preferences',{locale:language,theme},'PUT')).status,200);locale=language;
  await page.reload();await selectProject(project.id);
  async function notice(id:string){const note=page.getByTestId('capability-'+id).filter({visible:true});await note.waitFor();assert.ok((await note.innerText()).includes(w('Область:','Scope:')));assert.ok((await note.innerText()).includes(w('Следующий шаг:','Next step:')));const heading=await note.getAttribute('aria-labelledby');assert.ok(heading);assert.ok(await note.locator('[id="'+heading+'"]').innerText());return note;}
  await nav('settings');await page.locator('[data-settings-section=connection]').click();assert.equal(await(await notice('runtime')).getAttribute('data-capability-state'),'connected');
  await nav('projectMap');assert.equal(await(await notice('graph')).getAttribute('data-capability-state'),'unavailable');
  await nav('files');await page.getByTestId('files-list').waitFor();assert.ok(await page.locator('[data-file-path="guide.md"]').isVisible(),'tree stays available without parser/index');
  await nav('database');assert.equal(await(await notice('database')).getAttribute('data-capability-state'),'not_configured');
  await page.getByRole('tab',{name:w('Использование в коде','Code usages'),exact:true}).click();await notice('code-usages');
  await nav('overview');await page.locator('[data-overview-section=usage]').click();await notice('usage');
  await nav('agents');await page.locator('[data-resource-section=generate]').click();await notice('proposals');
  await nav('skills');await page.locator('[data-resource-section=discover]').click();await notice('discovery');
  const search=page.getByTestId('skill-discovery').getByRole('button',{name:w('Найти в доступных источниках','Search available sources'),exact:true});await search.focus();assert.equal(await search.evaluate((el:HTMLElement)=>el===document.activeElement),true);
  await page.locator('[data-resource-section=requirements]').click();await notice('skill-proposal');
  await nav('sessions');await notice('history');
  await nav('autonomy');await notice('autonomy');
  await page.setViewportSize({width:390,height:844});
  const geometry=await page.getByTestId('capability-autonomy').evaluate((el:HTMLElement)=>{const host=el.closest('.autonomy-workspace') as HTMLElement,style=getComputedStyle(host);return {noticeWidth:el.getBoundingClientRect().width,hostInnerWidth:host.clientWidth-parseFloat(style.paddingLeft)-parseFloat(style.paddingRight),tabsDirection:getComputedStyle(host.querySelector('.section-tabs')!).flexDirection};});
  report.mobileGeometry??=[];report.mobileGeometry.push({locale,theme,...geometry});
  assert.ok(geometry.noticeWidth>=280,'mobile capability note needs a readable full-width column');assert.ok(geometry.noticeWidth>=geometry.hostInnerWidth-2,'mobile note must span the workspace width');assert.equal(geometry.tabsDirection,'row');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));await shot(language+'-'+theme+'-capability-mobile');await page.setViewportSize({width:1440,height:1000});
 });
 await check('BYOK controls never inherit an App-channel availability notice',async()=>{
  await nav('settings');await page.locator('[data-settings-section=connection]').click();await page.getByRole('button',{name:appLabel(locale,'appDisconnect'),exact:true}).click();
  await page.getByLabel(appLabel(locale,'connectionRoute'),{exact:true}).selectOption('local_api_byok');
  assert.equal(await page.getByTestId('capability-runtime').count(),0,'App channel note must not describe BYOK availability');
  assert.equal(await page.locator('input[name=apiKey]').inputValue(),'');await shot('byok-keeps-own-scope');
 });
 await check('No external lookup, new authority prompt, source drift, target mutation or browser error',async()=>{
  assert.equal(external.calls.length,0);assert.deepEqual(report.externalRequests,[]);assert.deepEqual(report.pageErrors,[]);assert.deepEqual(report.consoleErrors.filter((v:string)=>!/status of 401/.test(v)),[]);assert.deepEqual(report.apiResponses.filter((r:any)=>r.status>=400&&r.status!==401),[]);
  assert.deepEqual(await hashes(workspace),report.targetInitialHashes);assert.deepEqual(await hashes(other),report.otherInitialHashes);assert.deepEqual(await bindings(),report.sourceHashes);assert.deepEqual(await hashes(resolve('apps/web/dist')),report.buildHashes);
 });
 report.status='passed';report.finishedAt=new Date().toISOString();
}catch(error){report.status='failed';report.stage=stage;report.error=String(error);report.finishedAt=new Date().toISOString();if(page)try{await page.screenshot({path:join(out,'failed.png'),fullPage:false});}catch{}await writeFile(join(out,'failed.json'),JSON.stringify(report,null,2)+'\n');throw error;}
finally{if(timer)clearTimeout(timer);await context?.close().catch(()=>{});await app?.close().catch(()=>{});await gateway?.close().catch(()=>{});if(server)await new Promise<void>(done=>server.close(()=>done()));await store?.close().catch(()=>{});const target=resolve(fixture);assert.equal(dirname(target),scratch);await rm(target,{recursive:true,force:true});if(report.status==='passed'){report.fixtureCleaned=true;report.fixtureRoot=relative(resolve('.'),target).replaceAll('\\','/');report.cleanupFinishedAt=new Date().toISOString();await assert.rejects(lstat(target),{code:'ENOENT'});await writeFile(join(out,'result.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({status:report.status,checks:report.checks.length,report:relative(resolve('.'),join(out,'result.json')).replaceAll('\\','/')}));}}
