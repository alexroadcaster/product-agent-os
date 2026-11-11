import {mkdtemp,mkdir,readFile,writeFile,rm,stat,readdir} from 'node:fs/promises';
import {join,isAbsolute,resolve} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash,randomUUID} from 'node:crypto';
import {runNativeLauncher,readLoopbackHealth} from '../../../apps/launcher/main.mts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';
import {uiLabel} from '../../../apps/web/src/locales/messages.ts';

/** No account mutations, runtime dispatch, imports, external routes, or arbitrary local origins. */
export function allowsSyntheticRequest(origin:string,url:string,method:string):boolean {
 try {
  const target=new URL(url);if(target.origin!==origin||target.username||target.password)return false;
  const path=target.pathname;
  if(method==='GET')return path==='/'||path==='/health'||/^\/assets\/[A-Za-z0-9_.-]+$/.test(path)
   ||/^\/api\/v1\/(?:session|projects|preferences|connection|runtime\/state)$/.test(path)
   ||/^\/api\/v1\/projects\/[^/]+\/(?:entities(?:\/[^/]+)?|search|sources(?:\/[^/]+)?|catalogs|history|imports\/(?:source-status|export))$/.test(path);
  return method==='POST'&&(/^\/api\/v1\/(?:bootstrap\/exchange|projects|quit)$/.test(path)||/^\/api\/v1\/projects\/[^/]+\/commands$/.test(path));
 }catch{return false;}
}
const sleep=(ms:number)=>new Promise<void>(resolve=>setTimeout(resolve,ms));
async function exists(path:string){try{await stat(path);return true;}catch(error){if((error as NodeJS.ErrnoException).code==='ENOENT')return false;throw error;}}

async function main(argv:string[]) {
 if(argv.length!==5||argv[0]!=='--synthetic-browser')throw new Error('EXPLICIT_LOCAL_BROWSER_PATHS_REQUIRED');
 const args=Object.fromEntries([argv.slice(1,3),argv.slice(3,5)]);
 if(Object.keys(args).length!==2||!args['--playwright-core']||!args['--chromium']||!Object.values(args).every(value=>typeof value==='string'&&isAbsolute(value)))throw new Error('INVALID_BROWSER_PATHS');
 const {chromium}=await import(pathToFileURL(join(args['--playwright-core'],'index.mjs')).href);
 const scratch=fileURLToPath(new URL('../../../.tmp/paos-m1/',import.meta.url));await mkdir(scratch,{recursive:true});
 const output=await mkdtemp(join(scratch,'autonomous-launcher-evidence-'));
 const fixture=await mkdtemp(join(scratch,'autonomous-launcher-fixture-'));
 const profile=join(fixture,'profile'),workspace=join(fixture,'workspace'),browserHome=join(fixture,'browser-home');
 await mkdir(profile);await mkdir(workspace);await mkdir(browserHome);
 const report:any={startedAt:new Date().toISOString(),syntheticOnly:true,providerUsed:false,keysUsed:false,osStoreUsed:false,
  appClosedClaim:false,nativeDialogClaim:false,manualReceiptOverridden:false,checks:[],screenshots:[],httpErrors:[],pageErrorCount:0,blockedRequests:[],sourceHashes:{}};
 const check=(name:string,value:boolean)=>{report.checks.push({name,passed:value});if(!value)throw new Error(name);};
 let context:any,page:any,code='',csrf='',paired=false,sessionRead:Promise<any>|undefined;
 const lock=join(profile,'service-instance');
 let stopped=false;const deadline=Date.now()+180_000;
 try {
  for(const path of ['tests/web/single-window/autonomous-launcher-acceptance.mts','tests/web/single-window/standalone-acceptance.mts','apps/launcher/main.mts','apps/launcher/launcher.ts','apps/launcher/profile-instance.ts','apps/launcher/native-window.ps1','apps/local-service/src/main.mts','apps/web/dist/index.html'])report.sourceHashes[path]=createHash('sha256').update(await readFile(fileURLToPath(new URL('../../../'+path,import.meta.url)))).digest('hex');
  for(const name of await readdir(fileURLToPath(new URL('../../../apps/web/dist/assets/',import.meta.url))))report.sourceHashes['apps/web/dist/assets/'+name]=createHash('sha256').update(await readFile(fileURLToPath(new URL('../../../apps/web/dist/assets/'+name,import.meta.url)))).digest('hex');
  const baselinePath=join(scratch,'standalone-BVldIt-result.json');
  if(await exists(baselinePath)){const baseline=JSON.parse(await readFile(baselinePath,'utf8'));report.priorNativeComponents={receipt:'standalone-BVldIt-result.json',ownerAccepted:baseline.ownerAttestations?.accepted===true,appAbsenceValid:baseline.appAbsence?.valid===true,
   sourceComparison:Object.entries(baseline.sourceHashes??{}).map(([path,hash])=>({path,currentHash:report.sourceHashes[path]??null,priorHash:hash,matching:report.sourceHashes[path]===hash})),acceptanceOverridden:false};}
  const result=await runNativeLauncher({profileDirectory:profile,async showWindow({origin,pairingCode,owner}){
   check('owner_service_started',owner);code=pairingCode??'';check('pairing_code_received_in_memory',code.length>0);
   report.origin=origin;
   async function openBrowser(){
    context=await chromium.launchPersistentContext(browserHome,{headless:true,chromiumSandbox:true,serviceWorkers:'block',viewport:{width:1440,height:1000},locale:'ru-RU',executablePath:args['--chromium'],timeout:20000,
     env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:browserHome,HOME:browserHome,APPDATA:browserHome,LOCALAPPDATA:browserHome,TEMP:browserHome,TMP:browserHome}});
    report.browserVersion=context.browser()?.version()??'persistent-context';
    await context.route('**/*',async(route:any)=>{
     const request=route.request();if(!allowsSyntheticRequest(origin,request.url(),request.method())){report.blockedRequests.push({path:new URL(request.url()).pathname,method:request.method()});await route.abort();}else await route.continue();
    });
    page=context.pages()[0]??await context.newPage();instrumentPage();
    // Close only this disposable browser on deadline. Production launcher catches and gracefully stops its service.
    const timer=setTimeout(()=>void context?.close(),Math.max(1,deadline-Date.now()));
    context.once('close',()=>clearTimeout(timer));await page.goto(origin);
   }
   function instrumentPage(){page.setDefaultTimeout(10000);page.setDefaultNavigationTimeout(15000);
    sessionRead=page.waitForResponse((response:any)=>response.url()===origin+'/api/v1/session');
    page.on('pageerror',()=>{report.pageErrorCount++;});
    page.on('response',(response:any)=>{if(response.status()>=400)report.httpErrors.push({path:new URL(response.url()).pathname,status:response.status(),afterPairing:paired});});
   }
   async function api(path:string,payload?:unknown){
    return page.evaluate(async({path,payload,csrf}:any)=>{const response=await fetch('/api/v1'+path,{method:payload===undefined?'GET':'POST',headers:{'content-type':'application/json','x-paos-csrf':csrf},...(payload===undefined?{}:{body:JSON.stringify(payload)})});return {status:response.status,body:await response.json()};},{path,payload,csrf});
   }
   async function nav(section:string){const label=['search','import','backup'].includes(section)?appLabel('ru',section as any):uiLabel('ru',`nav.${section}` as any);
    await page.locator('nav').getByRole('button',{name:label,exact:true}).click();await page.getByRole('heading',{level:1,name:label,exact:true}).waitFor();
    check('heading_'+section,true);check('no_session_required_'+section,!(await page.locator('body').innerText()).includes('SESSION_REQUIRED'));
   }
   await openBrowser();await page.getByRole('heading',{name:appLabel('ru','connect'),exact:true}).waitFor();
   await sessionRead;
   // Initial /session 401 is expected and must render guidance instead of a failed application state.
   await page.getByLabel(appLabel('ru','code'),{exact:true}).waitFor();
   await page.waitForFunction(()=>[...document.querySelectorAll('nav button')].every(button=>(button as HTMLButtonElement).disabled));
   check('unpaired_navigation_disabled',true);check('unpaired_guidance_has_no_session_error',!(await page.locator('body').innerText()).includes('SESSION_REQUIRED'));
   await page.screenshot({path:join(output,'initial-unpaired-guidance.png'),mask:[page.locator('input')]});report.screenshots.push('initial-unpaired-guidance.png');
   const pairingResponse=page.waitForResponse((response:any)=>response.url()===origin+'/api/v1/bootstrap/exchange'&&response.status()===200);
   await page.getByLabel(appLabel('ru','code'),{exact:true}).fill(code);await page.getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();
   csrf=(await(await pairingResponse).json()).csrfToken;code='';paired=true;
   await page.locator('.navigation select:enabled').waitFor();check('paired_session_available',(await api('/session')).status===200);
   await nav('settings');await page.getByLabel(appLabel('ru','name'),{exact:true}).fill('Autonomous synthetic project');
   await page.getByLabel(appLabel('ru','root'),{exact:true}).fill(workspace);await page.getByRole('button',{name:appLabel('ru','addProject'),exact:true}).click();
   await page.locator('.navigation select option').filter({hasText:'Autonomous synthetic project'}).waitFor({state:'attached'});
   const projects=(await api('/projects')).body;const project=(projects.items??projects)[0];check('synthetic_project_persisted',!!project?.id);
   const sessionId=randomUUID();const seed=await api(`/projects/${project.id}/commands`,{expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:'autonomous-session',changes:[{expectedRevision:0,entity:{id:sessionId,kind:'session',title:'Autonomous synthetic session',status:'idle',data:{mode:'discussion'}}}]});check('synthetic_session_persisted',seed.status===200);
   await nav('tasks');await page.screenshot({path:join(output,'paired-tasks.png'),mask:[page.locator('input[type=password]')]});report.screenshots.push('paired-tasks.png');
   for(const section of ['overview','tasks','sessions','agents','skills','projectMap','documents','checks','search','import','backup','settings'])await nav(section);
   await nav('sessions');await page.locator('.session-list .records button').filter({hasText:'Autonomous synthetic session'}).click();await page.locator('.chat-panel').waitFor();
   await page.locator('.chat-panel textarea').fill('Local draft; never dispatch');check('offline_send_disabled',await page.getByRole('button',{name:uiLabel('ru','action.send'),exact:true}).isDisabled());
   const state=(await api(`/runtime/state?projectId=${project.id}&sessionId=${sessionId}`)).body;check('runtime_gate_has_explicit_reason',state.canSend===false&&typeof state.reason==='string'&&state.reason.length>0);
   report.offlineReason=state.reason;check('no_runtime_selection',!await exists(join(profile,'runtime-selection.json')));
   await page.screenshot({path:join(output,'paired-offline-session.png'),fullPage:false});report.screenshots.push('paired-offline-session.png');
   const reused=await runNativeLauncher({profileDirectory:profile,async showWindow(second){check('second_instance_same_origin',second.owner===false&&second.origin===origin);return 'closed';}});
   check('launcher_reused_instance',reused.status==='opened'&&reused.instance==='existing');
   const endpoint=JSON.parse(await readFile(join(lock,'endpoint.json'),'utf8'));
   // Keep a neutral tab open so this checks tab lifetime, not Chromium's last-window/session shutdown.
   const neutral=await context.newPage();await page.close();
   const health=await readLoopbackHealth(endpoint,AbortSignal.timeout(5000));check('tab_close_retains_service',health.alive&&health.instanceId===endpoint.instanceId);
   page=await context.newPage();instrumentPage();await page.goto(origin);await page.locator('.navigation select:enabled').waitFor();await neutral.close();
   const restored=await api('/session');check('same_browser_session_retains_pairing',restored.status===200&&typeof restored.body.csrfToken==='string');csrf=restored.body.csrfToken;
   const sessions=await api(`/projects/${project.id}/entities?kind=session`);check('reopen_retains_session',sessions.body.items?.some((item:any)=>item.id===sessionId));
   await nav('settings');await page.getByLabel(appLabel('ru','quitConfirm'),{exact:true}).check();
   const quitResponse=page.waitForResponse((response:any)=>response.url()===origin+'/api/v1/quit');
   await page.getByRole('button',{name:appLabel('ru','quit'),exact:true}).click();const quit=await quitResponse;
   check('authenticated_browser_quit',quit.status()===202);
   for(let count=0;count<80&&await exists(lock);count++)await sleep(250);
   check('browser_quit_released_reservation',!await exists(lock));stopped=true;
   await context.close();context=undefined;return 'closed';
  }});
  report.launcherResult=result;check('production_launcher_completed',result.status==='opened'&&stopped);
  // A separate service generation tests closing the entire browser without pretending session cookies are persistent.
  const browserClose=await runNativeLauncher({profileDirectory:profile,async showWindow({origin,owner}){
   check('full_browser_close_owner_started',owner);
   context=await chromium.launchPersistentContext(browserHome,{headless:true,chromiumSandbox:true,serviceWorkers:'block',viewport:{width:1280,height:900},executablePath:args['--chromium'],timeout:20000,
    env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:browserHome,HOME:browserHome,APPDATA:browserHome,LOCALAPPDATA:browserHome,TEMP:browserHome,TMP:browserHome}});
   await context.route('**/*',async(route:any)=>allowsSyntheticRequest(origin,route.request().url(),route.request().method())?route.continue():route.abort());
   page=context.pages()[0]??await context.newPage();await page.goto(origin,{timeout:15000});
   await context.close();context=undefined;
   const endpoint=JSON.parse(await readFile(join(lock,'endpoint.json'),'utf8'));
   const health=await readLoopbackHealth(endpoint,AbortSignal.timeout(5000));check('full_browser_close_retains_service',health.alive&&health.instanceId===endpoint.instanceId);
   report.browserRestartAuthPolicy='not_asserted_session_cookie_no_cookie_injection';return 'quit';
  }});
  check('full_browser_close_owner_quit_ack',browserClose.status==='opened'&&!await exists(lock));
  check('no_post_pairing_http_errors',report.httpErrors.every((entry:any)=>!entry.afterPairing&&entry.path==='/api/v1/session'&&entry.status===401));
  check('no_page_errors',report.pageErrorCount===0);check('route_allowlist_clean',report.blockedRequests.length===0);
  report.status='passed_autonomous_local_launcher_browser';
 }catch(error){report.status='failed';const reason=String((error as {code?:string}).code??(error instanceof Error?error.message:'unknown'));
  report.failedCheck=/^[a-zA-Z0-9_]{1,100}$/.test(reason)?reason:'BROWSER_OR_LAUNCHER_CHECK_FAILED';process.exitCode=1;}
 finally {
  code='';csrf='';if(context)await context.close();const reserved=await exists(lock);report.reservationRemaining=reserved;
  if(!reserved&&resolve(fixture,'..')===resolve(scratch)){await rm(fixture,{recursive:true,force:true});report.fixtureCleaned=true;}else report.fixtureCleaned=false;
  report.finishedAt=new Date().toISOString();await writeFile(join(output,'autonomous-launcher-result.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify({status:report.status,evidence:output,checks:report.checks.length,failedCheck:report.failedCheck,fixtureCleaned:report.fixtureCleaned}));
 }
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))main(process.argv.slice(2)).catch(()=>{console.error('AUTONOMOUS_LAUNCHER_SETUP_FAILED');process.exitCode=1;});
