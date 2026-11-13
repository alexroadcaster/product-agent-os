import {chromium} from 'file:///C:/Users/user/AppData/Local/npm-cache/_npx/eb7983f9b02fb67f/node_modules/playwright-core/index.mjs';
import {dirname,join} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
const root=dirname(fileURLToPath(import.meta.url));
const browser=await chromium.launch({executablePath:'C:/Users/user/AppData/Local/ms-playwright/chromium-1223/chrome-win64/chrome.exe',headless:true});
const ctx=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'no-preference'});
const report={command:'node design/2026-11-13-v3/verify-sidebar.mjs',result:'running',checks:[],errors:[],network:[]};
await ctx.route(/^https?:/,r=>{report.network.push(r.request().url());return r.abort();});
const page=await ctx.newPage();page.setDefaultTimeout(5000);page.on('pageerror',e=>report.errors.push(e.message));
async function settled(){await page.waitForFunction(()=>window.DESIGN_SIDEBAR?.settled);}
try{
 await page.goto(`${pathToFileURL(join(root,'index.html'))}?screen=overview&theme=light`);
 assert.equal(await page.locator('#sidebar-toggle').count(),1,'Sidebar collapse toggle must exist');
 await settled();
 const constants=await page.evaluate(()=>DESIGN_SIDEBAR.springs);
 assert.deepEqual(constants,{width:[260,24],rotation:[300,22],highlight:[380,28],label:[300,26]});
 report.checks.push('Exact source spring stiffness/damping');
 const toggle=page.locator('#sidebar-toggle');
 for(const theme of ['light','dark']){
  await page.evaluate(theme=>{state.theme=theme;render();},theme);await settled();
  await toggle.click();
  await page.waitForFunction(()=>{const w=document.querySelector('.sidebar').getBoundingClientRect().width;return w>65&&w<215;});
  await settled();assert.equal(await toggle.getAttribute('aria-expanded'),'false');
  assert.equal(Math.round((await page.locator('.sidebar').boundingBox()).width),64);
  for(const width of [1280,1440,1920]){
   await page.setViewportSize({width,height:1000});await settled();
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   assert.equal(await page.locator('.nav-link').count(),15);
  }
  await page.setViewportSize({width:1440,height:1000});
  await page.locator('.nav-link[data-section="tasks"]').focus();
  await page.locator('#sidebar-tooltip').waitFor({state:'visible'});
  assert.equal(await page.locator('#sidebar-tooltip').innerText(),'Задачи');
  await page.keyboard.press('Escape');assert.ok(await page.locator('#sidebar-tooltip').isHidden());
  await page.keyboard.press('Enter');await page.waitForFunction(()=>DESIGN_RENDER_READY.id==='tasks-list');await settled();
  assert.equal(await toggle.getAttribute('aria-expanded'),'false');
  assert.equal(await page.locator('.nav-link[aria-current="page"]').getAttribute('data-section'),'tasks');
  await page.waitForFunction(()=>DesignRuntime.gsap.globalTimeline.getChildren().every(t=>!t.isActive()));
  await page.screenshot({path:join(root,'screenshots',`${theme}-sidebar-collapsed.png`)});
  await toggle.focus();await page.keyboard.press('Enter');await settled();
  assert.equal(Math.round((await page.locator('.sidebar').boundingBox()).width),216);
  assert.equal(await toggle.getAttribute('aria-expanded'),'true');
  await page.screenshot({path:join(root,'screenshots',`${theme}-sidebar-expanded.png`)});
 }
 report.checks.push('Both themes: animated 216→64→216, three widths, all 15 routes, tooltip/Escape, Enter, selected item and collapse preserved across navigation');
 for(let i=0;i<5;i++)await toggle.click();await settled();
 assert.equal(await toggle.getAttribute('aria-expanded'),'false');
 await page.waitForTimeout(800);assert.equal(await toggle.getAttribute('aria-expanded'),'false');
 report.checks.push('Rapid reversal settles without delayed reopen');
 await page.setViewportSize({width:1280,height:720});
 await page.locator('.nav-link[data-section="settings"]').focus();
 await page.locator('#sidebar-tooltip').waitFor({state:'visible'});
 assert.equal(await page.locator('#sidebar-tooltip').innerText(),'Настройки');
 const lastItem=await page.locator('.nav-link[data-section="settings"]').boundingBox();assert.ok(lastItem.y>=0&&lastItem.y+lastItem.height<664);
 report.checks.push('Short desktop viewport: final section scrolls into keyboard view');
 await page.emulateMedia({reducedMotion:'reduce'});await toggle.click();await settled();
 assert.equal(Math.round((await page.locator('.sidebar').boundingBox()).width),216);
 assert.equal(await page.evaluate(()=>DESIGN_SIDEBAR.framePending),false);
 await toggle.click();await settled();assert.equal(Math.round((await page.locator('.sidebar').boundingBox()).width),64);
 report.checks.push('Reduced motion snaps directly and leaves no frame loop');
 assert.deepEqual(report.errors,[]);assert.deepEqual(report.network,[]);report.result='passed';report.exitCode=0;
}catch(error){report.result='failed';report.exitCode=1;report.failure=error.message;await page.screenshot({path:join(root,'screenshots','sidebar-check-failure.png')});throw error;}
finally{await writeFile(join(root,'sidebar-check-report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));await browser.close();}
