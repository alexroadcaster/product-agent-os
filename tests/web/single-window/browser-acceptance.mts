import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,rm,stat} from 'node:fs/promises';
import {join,isAbsolute} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {runNativeLauncher} from '../../../apps/launcher/main.mts';
import {newTask} from '../../../apps/web/src/api/task.ts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';
import {uiLabel} from '../../../apps/web/src/locales/messages.ts';

if(process.argv[2]!=='--synthetic-browser'||process.argv.length!==7)throw new Error('Explicit synthetic browser mode and installed binaries required');
const args=Object.fromEntries([process.argv.slice(3,5),process.argv.slice(5,7)]);
if(!args['--playwright-core']||!args['--chromium']||Object.keys(args).length!==2||!Object.values(args).every(isAbsolute))throw new Error('Invalid local browser paths');
const {chromium}=await import(pathToFileURL(join(args['--playwright-core'],'index.mjs')).href);
const scratch=fileURLToPath(new URL('../../../.tmp/paos-m1/',import.meta.url));
const output=await mkdtemp(join(scratch,'browser-evidence-'));
const root=await mkdtemp(join(scratch,'browser-fixture-'));
const profile=join(root,'profile'),workspace=join(root,'workspace'),browserHome=join(root,'browser-home');
await mkdir(profile);await mkdir(workspace);await mkdir(browserHome);
const report:any={startedAt:new Date().toISOString(),syntheticOnly:true,providerUsed:false,realKeysUsed:false,osStoreUsed:false,
 browserPlugin:'absent',browserDriver:'existing Playwright cache',checks:[],screenshots:[],pageErrors:[],consoleErrors:[],blockedRequests:[]};
const check=(name:string,passed:boolean,detail?:unknown)=>{report.checks.push({name,passed,...(detail===undefined?{}:{detail})});if(!passed)throw new Error(name);};
let browser:any;let page:any;let secret='';let currentLocale:'ru'|'en'='ru';
try {
 const result=await runNativeLauncher({profileDirectory:profile,async showWindow({origin,pairingCode}){
  secret=pairingCode??'';
  browser=await chromium.launch({headless:true,chromiumSandbox:true,executablePath:args['--chromium'],
   env:{SystemRoot:process.env.SystemRoot!,TEMP:browserHome,TMP:browserHome,USERPROFILE:browserHome,HOME:browserHome,APPDATA:browserHome,LOCALAPPDATA:browserHome}});
  report.browserVersion=browser.version();report.origin=origin;
  const context=await browser.newContext({viewport:{width:1280,height:900},locale:'en-US',colorScheme:'light'});
  await context.route('**/*',async(route:any)=>{const url=new URL(route.request().url());
   if(url.origin!==origin||(/\/api\/v1\/(connection|runtime)(\/|$)/.test(url.pathname)&&route.request().method()!=='GET')){
    report.blockedRequests.push({origin:url.origin,path:url.pathname,method:route.request().method()});await route.abort();
   }else await route.continue();});
  page=await context.newPage();page.setDefaultTimeout(8000);
  function instrument(target:any){
   target.on('pageerror',(error:Error)=>report.pageErrors.push(error.message));
   target.on('console',(entry:any)=>{if(entry.type()==='error')report.consoleErrors.push(entry.text());});
   target.on('response',(response:any)=>{if(response.status()>=400){report.httpErrors??=[];report.httpErrors.push({path:new URL(response.url()).pathname,status:response.status()});}});
  }
  instrument(page);
  let csrf='';
  page.on('response',async(response:any)=>{if(response.url()===origin+'/api/v1/bootstrap/exchange'&&response.status()===200)csrf=(await response.json()).csrfToken;});
  const initialSession=page.waitForResponse((response:any)=>response.url()===origin+'/api/v1/session'&&response.status()===401);
  await page.goto(origin);await initialSession;check('page_identity',page.url()===origin+'/'&&(await page.title()).includes('Product-Agent OS'));
  await page.getByRole('heading',{name:appLabel('ru','connect'),exact:true}).waitFor();check('meaningful_pairing_ui',true);
  check('unpaired_state_has_no_failure_banner',await page.getByRole('alert').count()===0);
  check('unpaired_navigation_disabled',await page.locator('nav button:enabled').count()===0);
  await page.getByLabel(appLabel('ru','code'),{exact:true}).fill(secret);
  await page.getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();
  await page.getByRole('button',{name:uiLabel('ru','nav.settings'),exact:true}).click();
  const longName='Синтетический проект — Long project name for layout verification';
  await page.getByLabel(appLabel('ru','name'),{exact:true}).fill(longName);
  await page.getByLabel(appLabel('ru','root'),{exact:true}).fill(workspace);
  await page.getByRole('button',{name:appLabel('ru','addProject'),exact:true}).click();
  await page.locator('.navigation select option').filter({hasText:longName}).waitFor({state:'attached'});
  const projects=await (await page.request.get(origin+'/api/v1/projects')).json();const project=projects.items?.[0]??projects[0];
  assert.ok(project?.id,'synthetic project created');
  const longTitle='Длинная задача — Verify long English and Russian text without hiding actions '.repeat(2);
  const task=newTask(project.id,longTitle,'Описание и summary '.repeat(25),['Проверить видимость всех действий и длинного текста']);
  const sessionId=crypto.randomUUID(),longSession='Синтетическая сессия — Long session title for locale layout';
  const seeded=await page.request.post(`${origin}/api/v1/projects/${project.id}/commands`,{headers:{origin,'x-paos-csrf':csrf},data:{expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:'browser-seed',changes:[{expectedRevision:0,entity:task},
   {expectedRevision:0,entity:{id:sessionId,projectId:project.id,kind:'session',title:longSession,status:'idle',data:{mode:'discussion'}}}]}});
  check('synthetic_seed',seeded.ok(),seeded.status());
  const sectionLabel=(section:string)=>['search','import','backup'].includes(section)?appLabel(currentLocale,section as any):uiLabel(currentLocale,`nav.${section}` as any);
  async function nav(section:string){
   const menu=page.getByRole('button',{name:appLabel(currentLocale,'menu'),exact:true});
   if(await menu.isVisible()&&await menu.getAttribute('aria-expanded')!=='true')await menu.click();
   await page.locator('nav').getByRole('button',{name:sectionLabel(section),exact:true}).click();
  }
  async function appearance(locale:'ru'|'en',theme:string,resolved=theme){
   await nav('settings');
   report.preferenceSelectLabels=await page.locator('.settings-grid select').evaluateAll((elements:any[])=>elements.map(element=>({label:element.labels?.[0]?.textContent,ariaLabel:element.getAttribute('aria-label')})));
   await page.getByLabel(uiLabel(currentLocale,'preferences.language'),{exact:true}).selectOption(locale);
   await page.getByLabel(uiLabel(currentLocale,'preferences.theme'),{exact:true}).selectOption(theme);
   await page.getByRole('button',{name:uiLabel(currentLocale,'preferences.save'),exact:true}).click();
   await page.waitForFunction(({locale,theme}:any)=>document.documentElement.lang===locale&&document.documentElement.dataset.theme===theme,{locale,theme:resolved});
   currentLocale=locale;
  }
  async function geometry(label:string){
   const value=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,main:document.querySelector('main')!.getBoundingClientRect().toJSON(),
    overflow:[...document.querySelectorAll('header,main,main button,main input,main select,main textarea')].filter(element=>{const r=element.getBoundingClientRect();return r.width>0&&(r.left< -1||r.right>innerWidth+1);}).slice(0,8).map(element=>({tag:element.tagName,text:element.textContent?.slice(0,80),rect:element.getBoundingClientRect().toJSON()}))}));
   check(label,value.scroll<=value.width+1,value);
  }
  async function screenshot(name:string){await page.screenshot({path:join(output,name),fullPage:false,mask:[page.locator('input[type=password],input[autocomplete=off]')]});report.screenshots.push(name);}
  async function controls(label:string,locator:any){
   let index=0;for(const element of await locator.all()){
    if(!await element.isVisible())continue;await element.scrollIntoViewIfNeeded();
    const visibility=await element.evaluate((node:HTMLElement)=>{const rect=node.getBoundingClientRect();const hit=document.elementFromPoint(rect.left+rect.width/2,rect.top+rect.height/2);return {left:rect.left,right:rect.right,width:innerWidth,hit:!!hit&&(hit===node||node.contains(hit))};});
    check(`${label}_action_${index++}`,visibility.left>=-1&&visibility.right<=visibility.width+1&&visibility.hit,visibility);
   }
   await page.evaluate(()=>scrollTo(0,0));
  }
  function contrast(a:string,b:string){
   const lum=(color:string)=>{const rgb=color.startsWith('#')?[1,3,5].map(offset=>parseInt(color.slice(offset,offset+2),16)):color.match(/[\d.]+/g)!.slice(0,3).map(Number);
    return rgb.map(value=>{const n=value/255;return n<=0.04045?n/12.92:((n+0.055)/1.055)**2.4;}).reduce((sum,n,index)=>sum+n*[0.2126,0.7152,0.0722][index],0);};
   const x=lum(a),y=lum(b);return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05);
  }
  async function colors(label:string){
   const values=await page.evaluate(()=>{const root=getComputedStyle(document.documentElement);const primary=getComputedStyle(document.querySelector('button.primary')!);
    return {ink:root.getPropertyValue('--ink').trim(),muted:root.getPropertyValue('--muted').trim(),paper:root.getPropertyValue('--paper').trim(),panel:root.getPropertyValue('--panel').trim(),focus:root.getPropertyValue('--focus').trim(),primaryInk:primary.color,primaryBackground:primary.backgroundColor};});
   check(label+'_body_contrast',contrast(values.ink,values.paper)>=4.5,values);
   check(label+'_muted_contrast',contrast(values.muted,values.panel)>=4.5);
   check(label+'_primary_contrast',contrast(values.primaryInk,values.primaryBackground)>=4.5);
   check(label+'_focus_contrast',contrast(values.focus,values.panel)>=3);
  }
  for(const locale of ['ru','en'] as const)for(const theme of ['light','dark']){
   await page.setViewportSize({width:1280,height:900});await appearance(locale,theme);
   await page.reload();await page.locator('.navigation select:enabled').waitFor();
   check(`persist_${locale}_${theme}`,await page.locator('html').getAttribute('lang')===locale&&await page.locator('html').getAttribute('data-theme')===theme);
   for(const width of [320,1280,1440,1920]){
    await page.setViewportSize({width,height:900});await nav('tasks');
    if(await page.locator('.task-detail').count())await page.locator('.task-detail').getByRole('button',{name:appLabel(locale,'close'),exact:true}).click();
    await page.getByText(longTitle,{exact:true}).first().waitFor();await geometry(`task_list_${locale}_${theme}_${width}`);
    await controls(`task_list_${locale}_${theme}_${width}`,page.locator('header button,.task-list .section-heading button'));
    if(width===320||width===1440)await screenshot(`${locale}-${theme}-${width}.png`);
    await page.getByText(longTitle,{exact:true}).first().click();await page.locator('.task-detail').waitFor();
    await geometry(`task_detail_${locale}_${theme}_${width}`);
    await controls(`task_detail_${locale}_${theme}_${width}`,page.locator('.task-detail button'));
    await page.locator('.task-detail').getByRole('button',{name:appLabel(locale,'close'),exact:true}).click();
    await page.getByRole('button',{name:appLabel(locale,'board'),exact:true}).click();await page.locator('.kanban').waitFor();
    await geometry(`kanban_${locale}_${theme}_${width}`);
    await controls(`kanban_${locale}_${theme}_${width}`,page.locator('.kanban .records button'));
    await page.getByRole('button',{name:appLabel(locale,'list'),exact:true}).click();
    await nav('sessions');await page.locator('.session-list .records button').filter({hasText:longSession}).click();
    await page.locator('.chat-panel').waitFor();
    await page.locator('.chat-panel .tabs').getByRole('button',{name:appLabel(locale,'chat'),exact:true}).click();
    await page.locator('.chat-panel textarea').fill('Длинный текст сообщения / Long composer text '.repeat(8));
    check(`offline_send_disabled_${locale}_${theme}_${width}`,await page.getByRole('button',{name:uiLabel(locale,'action.send'),exact:true}).isDisabled());
    await geometry(`composer_${locale}_${theme}_${width}`);
    await controls(`composer_${locale}_${theme}_${width}`,page.locator('.chat-panel .actions button'));
    for(const tab of ['context','changes']){
     await page.locator('.chat-panel .tabs').getByRole('button',{name:appLabel(locale,tab as any),exact:true}).click();
     await geometry(`${tab}_${locale}_${theme}_${width}`);
    }
    if(width===320&&locale==='en'&&theme==='dark')await screenshot('en-dark-320-session.png');
   }
   for(const width of [320,1440])for(const section of ['overview','sessions','agents','skills','projectMap','documents','checks','search','import','backup','settings']){
    await page.setViewportSize({width,height:900});await nav(section);
    check(`route_${locale}_${theme}_${width}_${section}`,await page.getByRole('heading',{level:1,name:sectionLabel(section),exact:true}).count()===1);
    await geometry(`route_geometry_${locale}_${theme}_${width}_${section}`);
   }
   await page.setViewportSize({width:1280,height:900});await nav('settings');await colors(`${locale}_${theme}`);
   // Start with a fresh document and use keyboard navigation, rather than programmatically focusing controls.
   await page.reload();await page.locator('.navigation select:enabled').waitFor();await page.keyboard.press('Tab');
   check(`skip_link_${locale}_${theme}`,await page.evaluate(()=>document.activeElement?.getAttribute('href')==='#main'));
   await page.keyboard.press('Enter');check(`skip_focus_${locale}_${theme}`,await page.evaluate(()=>document.activeElement?.id==='main'));
   // The skip target is a noninteractive landmark. Verify visible focus on the adjacent operable control.
   await page.keyboard.press('Shift+Tab');
   const focus=await page.evaluate(()=>{const element=document.activeElement as HTMLElement;return {tag:element.tagName,text:element.textContent,style:getComputedStyle(element).outlineStyle,width:getComputedStyle(element).outlineWidth};});
   check(`visible_focus_${locale}_${theme}`,focus.tag==='BUTTON'&&focus.text===appLabel(locale,'reload')&&focus.style!=='none'&&parseFloat(focus.width)>=2,focus);
  }
  await page.emulateMedia({colorScheme:'dark'});await appearance('en','system','dark');check('system_dark',true);
  await page.emulateMedia({colorScheme:'light'});await page.locator('html[data-theme=light]').waitFor();check('system_live_change',true);
  await page.reload();await page.locator('.navigation select:enabled').waitFor();await page.locator('html[lang=en][data-theme=light]').waitFor();
  const stored=await (await page.request.get(origin+'/api/v1/preferences')).json();check('system_preference_retained',stored.locale==='en'&&stored.theme==='system');
  const cookies=await context.cookies();await browser.close();
  let baseline:{width:number;ratio:number}|undefined;
  // Source-backed Chromium zoom preference, written only before launching a newly created disposable profile.
  // Read back DPR and CSS viewport to prove native page zoom; no injected page CSS or device metrics.
  for(const factor of [1,2]) {
   const nativeHome=join(root,`native-zoom-${factor}`);await mkdir(join(nativeHome,'Default'),{recursive:true});
   await writeFile(join(nativeHome,'Default','Preferences'),JSON.stringify({partition:{default_zoom_level:{x:Math.log(factor)/Math.log(1.2)}}}),{flag:'wx'});
   const nativeContext=await chromium.launchPersistentContext(nativeHome,{headless:false,chromiumSandbox:true,viewport:null,colorScheme:'light',executablePath:args['--chromium'],args:['--window-size=1280,960'],
    env:{SystemRoot:process.env.SystemRoot!,TEMP:browserHome,TMP:browserHome,USERPROFILE:browserHome,HOME:browserHome,APPDATA:browserHome,LOCALAPPDATA:browserHome}});
   browser=nativeContext;await nativeContext.addCookies(cookies);
   await nativeContext.route('**/*',async(route:any)=>{const url=new URL(route.request().url());if(url.origin!==origin||((url.pathname==='/api/v1/connection'||/\/runtime(?:\/|$)/.test(url.pathname))&&route.request().method()!=='GET')){report.blockedRequests.push({origin:url.origin,path:url.pathname,method:route.request().method()});await route.abort();}else await route.continue();});
   page=await nativeContext.newPage();instrument(page);page.setDefaultTimeout(8000);await page.goto(origin);await page.locator('.navigation select:enabled').waitFor({state:'attached'});await nav('tasks');
   await page.getByText(longTitle,{exact:true}).first().waitFor();
   const observed=await page.evaluate(()=>({width:innerWidth,ratio:devicePixelRatio,visualScale:visualViewport?.scale}));
   if(factor===1){baseline=observed;await screenshot('native-zoom-100.png');}
   else {
    report.nativeZoom={mechanism:'fixture-only Chromium partition.default_zoom_level.x',before:baseline,after:observed,percent:100*observed.ratio/baseline!.ratio};
    check('actual_browser_zoom_200',Math.abs(report.nativeZoom.percent-200)<2&&observed.width<baseline!.width&&observed.visualScale===1,report.nativeZoom);
    for(const locale of ['ru','en'] as const)for(const theme of ['light','dark']) {
     await appearance(locale,theme);await nav('tasks');await page.getByText(longTitle,{exact:true}).first().waitFor();
     await geometry(`native_zoom_200_${locale}_${theme}`);await controls(`native_zoom_200_${locale}_${theme}`,page.locator('header button,.task-list .section-heading button'));
     await screenshot(`native-zoom-200-${locale}-${theme}.png`);
     await nav('sessions');await page.locator('.session-list .records button').filter({hasText:longSession}).click();await page.locator('.chat-panel').waitFor();
     await geometry(`native_zoom_200_composer_${locale}_${theme}`);await controls(`native_zoom_200_composer_${locale}_${theme}`,page.locator('.chat-panel .actions button'));
    }
   }
   check(`native_no_framework_overlay_${factor}`,await page.locator('vite-error-overlay').count()===0);
   await nativeContext.close();browser=undefined;
  }
  check('no_page_errors',report.pageErrors.length===0);
  return 'quit';
 }});
 check('launcher_shutdown_ack',result.status==='opened');
 await assert.rejects(stat(join(profile,'service-instance')),{code:'ENOENT'});check('reservation_released',true);
  check('console_health',report.consoleErrors.every((message:string)=>message.includes('401'))&&report.pageErrors.length===0);
  check('no_unexpected_http_errors',(report.httpErrors??[]).every((item:any)=>item.status===401&&item.path==='/api/v1/session'));
  check('no_unexpected_requests',report.blockedRequests.length===0);
  report.status='passed_browser_acceptance';
}catch(error){report.status='failed';report.error=String(error).replaceAll(secret||'__no_secret__','[redacted]');process.exitCode=1;
 if(page&&!page.isClosed())try{await page.screenshot({path:join(output,'failure.png'),mask:[page.locator('input[type=password],input[autocomplete=off]')]});report.screenshots.push('failure.png');}catch{}
}finally{
 if(browser)await browser.close();let reserved=false;try{await stat(join(profile,'service-instance'));reserved=true;}catch{}
 if(!reserved){await rm(root,{recursive:true,force:true});report.fixtureCleaned=true;}else report.fixtureCleaned=false;
 report.finishedAt=new Date().toISOString();await writeFile(join(output,'browser-result.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({status:report.status,evidence:output,checks:report.checks.length,failed:report.checks.filter((item:any)=>!item.passed),error:report.error,fixtureCleaned:report.fixtureCleaned}));
}
