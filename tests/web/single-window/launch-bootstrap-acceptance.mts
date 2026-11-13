import {mkdtemp,mkdir,rm,writeFile,readFile,stat} from 'node:fs/promises';
import {resolve,join,dirname,isAbsolute} from 'node:path';
import {pathToFileURL} from 'node:url';
import {runNativeLauncher,nativeWindow} from '../../../apps/launcher/main.mts';

// Bounded native ShellExecute + production HTTP/Web verification; browser profile and workspace are synthetic.
const argv=process.argv.slice(2);if(argv[0]!=='--synthetic-browser'||argv.length!==5)throw Error('EXPLICIT_SYNTHETIC_BROWSER_REQUIRED');
const args=Object.fromEntries([[argv[1],argv[2]],[argv[3],argv[4]]]);for(const key of ['--playwright-core','--chromium'])if(!isAbsolute(args[key]??''))throw Error('INSTALLED_PATH_REQUIRED');
const scratch=resolve('.tmp/paos-local-launch');await mkdir(scratch,{recursive:true});
const fixture=await mkdtemp(join(scratch,'browser-fixture-')),profile=join(fixture,'profile'),home=join(fixture,'browser'),workspace=join(fixture,'workspace');
await Promise.all([mkdir(profile),mkdir(home),mkdir(workspace)]);await writeFile(join(workspace,'PLAN.md'),'# Synthetic launch plan\n\nRead only fixture.\n');
const report:any={startedAt:new Date().toISOString(),checks:[],pageErrors:[],consoleErrors:0,consoleEvents:[],unexpectedNetwork:0,metadata:[],browserPlugin:'not_available',nativeShellExecute:true,providerCalls:0};
let context:any,page:any,origin='',timer:any;
let negativeCases=false,shuttingDown=false,loggingOut=false;
const check=(name:string,passed:boolean)=>{report.checks.push({name,passed});if(!passed)throw Error(name);};
async function launch(){
 let opened:any;
 const result=await runNativeLauncher({profileDirectory:profile,showWindow:async input=>{
  origin=input.origin;const next=context.waitForEvent('page',{timeout:20000});
  const outcome=await nativeWindow({...input,browserExecutable:args['--chromium'],browserProfileDirectory:home});
  opened=await next;return outcome;
 }});
 check('native_launcher_opened',result.status==='opened');page=opened;
 page.on('pageerror',(e:any)=>report.pageErrors.push(String(e.message).slice(0,150)));
 await page.waitForURL(origin+'/');await page.locator('nav button:enabled').first().waitFor();
 return result;
}
try{
 const {chromium}=await import(pathToFileURL(join(args['--playwright-core'],'index.mjs')).href);
 context=await chromium.launchPersistentContext(home,{headless:false,chromiumSandbox:true,serviceWorkers:'block',viewport:{width:1440,height:1000},executablePath:args['--chromium'],
  env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:home,HOME:home,APPDATA:home,LOCALAPPDATA:home,TEMP:home,TMP:home}});
 timer=setTimeout(()=>void context?.close(),150000);
 context.on('page',(opened:any)=>opened.on('console',(message:any)=>{
  if(opened.url().startsWith(origin+'/')&&['error','warning'].includes(message.type())){
   const text=message.text(),status=/\b([45]\d\d)\b/.exec(text)?.[1];
   const expected=shuttingDown||negativeCases||/favicon|404/.test(text)||loggingOut&&status==='401';
   report.consoleEvents.push({status:status??'other',phase:shuttingDown?'shutdown':negativeCases?'negative':loggingOut?'logout':'startup',expected});
   if(!expected)report.consoleErrors++;
  }
 }));
 await context.route('**/*',async(route:any)=>{
  const url=new URL(route.request().url());
  if(url.hostname==='attacker.invalid')return route.fulfill({status:url.pathname==='/redirect'?302:200,headers:url.pathname==='/redirect'?{location:origin+'/launch'}:{'content-type':'text/html'},body:'<a id="link" href="'+origin+'/launch">Open</a><a id="nr" rel="noreferrer" target="_blank" href="'+origin+'/launch">New</a><a id="redirect" href="/redirect">Redirect</a><form action="'+origin+'/launch"><button>Submit</button></form>'});
  if(url.origin!==origin){report.unexpectedNetwork++;return route.abort();}
  if(url.pathname==='/launch'){const h=route.request().headers();report.metadata.push({site:h['sec-fetch-site'],mode:h['sec-fetch-mode'],dest:h['sec-fetch-dest'],user:h['sec-fetch-user']});}
  return route.continue();
 });
 const first=await launch();check('new_profile_without_manual_pairing',first.status==='opened'&&first.instance==='started');
 // A native-created app target may finish its first navigation before Playwright attaches.
 // Fresh profile + authenticated UI prove guarded admission; do not invent an observed initial-header capture.
 report.nativeNavigationProof='fresh browser profile, native ShellExecute, guarded route, authenticated UI; earliest headers may precede automation attachment';
 const cookies=await context.cookies(origin);check('automatic_session_is_httponly_strict',cookies.some((c:any)=>c.name.startsWith('paos_session_')&&c.httpOnly&&c.sameSite==='Strict'));
 check('no_pairing_form_on_working_screen',await page.locator('input[autocomplete=off]').count()===0);
 check('page_identity',(await page.title())==='Product-Agent OS');check('not_blank',(await page.locator('body').innerText()).includes('Обзор'));
 check('no_framework_overlay',await page.locator('vite-error-overlay').count()===0);
 check('clean_url',page.url()===origin+'/');
 await page.locator('nav').getByRole('button',{name:'Настройки',exact:true}).click();
 const form=page.locator('form').filter({has:page.locator('input[name=root]')});await form.locator('[name=name]').fill('Launch verification');await form.locator('[name=root]').fill(workspace);await form.getByRole('button').click();
 await page.locator('.navigation select option').filter({hasText:'Launch verification'}).waitFor({state:'attached'});
 check('first_project_created',true);await page.reload();await page.locator('nav button:enabled').first().waitFor();check('session_survives_reload',true);
 const shot=resolve('C:/Users/user/.codex/visualizations/2026/11/11/01a1cb91-c2df-7d13-97fe-64e981d02d42/launch-without-code.png');await page.screenshot({path:shot});report.screenshot=shot;
 await page.setViewportSize({width:390,height:844});check('mobile_working_screen',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 report.mobileScreenshot=shot.replace('.png','-mobile.png');await page.screenshot({path:report.mobileScreenshot});await page.setViewportSize({width:1440,height:1000});
 const second=await launch();check('repeat_launch_reuses_service',second.status==='opened'&&second.instance==='existing');
 negativeCases=true;
 const attack=await context.newPage();
 async function denied(action:()=>Promise<unknown>,target=attack){const response=target.waitForResponse((r:any)=>new URL(r.url()).origin===origin&&new URL(r.url()).pathname==='/launch');await action();check('foreign_navigation_denied',(await response).status()===403);}
 await attack.goto('http://attacker.invalid/');await denied(()=>attack.locator('#link').click());
 await attack.goto('http://attacker.invalid/');const pop=context.waitForEvent('page');await attack.locator('#nr').click();const popup=await pop;await popup.waitForLoadState();check('noreferrer_popup_denied',(await popup.locator('body').innerText()).includes('ORIGIN_REJECTED'));await popup.close();
 await attack.goto('http://attacker.invalid/');await denied(()=>attack.getByRole('button',{name:'Submit'}).click());
 await attack.goto('http://attacker.invalid/');await denied(()=>attack.locator('#redirect').click());
 await attack.goto('http://attacker.invalid/');
 check('foreign_fetch_denied',await attack.evaluate(async url=>{try{await fetch(url);return false;}catch{return true;}},origin+'/launch'));
 const embedded=attack.waitForEvent('framenavigated',{predicate:(f:any)=>f.parentFrame()!==null});
 await attack.evaluate(url=>{const f=document.createElement('iframe');f.src=url;document.body.append(f);},origin+'/launch');
 const blockedFrame=await embedded;await blockedFrame.locator('body').waitFor({state:'attached'});
 const blockedText=blockedFrame.url().startsWith('chrome-error:')?'':await blockedFrame.locator('body').textContent();
 check('foreign_iframe_denied',blockedFrame.url().startsWith('chrome-error:')||blockedText.includes('ORIGIN_REJECTED')||blockedText.includes('LAUNCH_REJECTED'));
 check('same_origin_scripted_launch_denied',await page.evaluate(async()=>{const r=await fetch('/launch');return r.status===403;}));
 negativeCases=false;
 const csrf=await page.evaluate(async()=>{const r=await fetch('/api/v1/session');return (await r.json()).csrfToken;});
 loggingOut=true;const logout=await page.evaluate(async csrf=>(await fetch('/api/v1/logout',{method:'POST',headers:{'x-paos-csrf':csrf}})).status,csrf);check('logout_works',logout===200);
 await launch();check('relaunch_after_logout_without_code',true);
 loggingOut=false;
 check('no_unexpected_console_errors',report.consoleErrors===0);check('no_external_network',report.unexpectedNetwork===0);shuttingDown=true;
 const current=await page.evaluate(async()=>await(await fetch('/api/v1/session')).json());
 const quit=await page.evaluate(async csrf=>(await fetch('/api/v1/quit',{method:'POST',headers:{'x-paos-csrf':csrf}})).status,current.csrfToken);check('quit_acknowledged',quit===202);
 const deadline=Date.now()+15000;let released=false;while(Date.now()<deadline){try{await stat(join(profile,'service-instance'));}catch(e){if((e as any).code==='ENOENT'){released=true;break;}throw e;}await new Promise(r=>setTimeout(r,100));}
 check('owner_ipc_drain_releases_reservation',released);check('no_page_errors',report.pageErrors.length===0);
 report.status='passed';
}catch(error){report.status='failed';report.error=String(error).slice(0,250);process.exitCode=1;}
finally{
 if(timer)clearTimeout(timer);
 if(origin){try{await page?.evaluate(async()=>{const s=await(await fetch('/api/v1/session')).json();await fetch('/api/v1/quit',{method:'POST',headers:{'x-paos-csrf':s.csrfToken}});});}catch{}}
 await context?.close();
 if(dirname(fixture)!==scratch)throw Error('CLEANUP_BOUNDARY');
 // Keep failed fixture if the service still owns it; never force-kill user applications.
 try{await stat(join(profile,'service-instance'));report.fixtureCleaned=false;}catch{await rm(fixture,{recursive:true,force:true});report.fixtureCleaned=true;}
 report.finishedAt=new Date().toISOString();await writeFile(join(scratch,'browser-result.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({status:report.status,checks:report.checks.length,error:report.error,fixtureCleaned:report.fixtureCleaned}));
}
