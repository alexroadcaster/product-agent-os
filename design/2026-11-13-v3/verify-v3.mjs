import {chromium} from 'file:///C:/Users/user/AppData/Local/npm-cache/_npx/eb7983f9b02fb67f/node_modules/playwright-core/index.mjs';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {dirname,join} from 'node:path';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
const root=dirname(fileURLToPath(import.meta.url));
await mkdir(join(root,'screenshots'),{recursive:true});
const browser=await chromium.launch({executablePath:'C:/Users/user/AppData/Local/ms-playwright/chromium-1223/chrome-win64/chrome.exe',headless:true});
const ctx=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
const network=[];await ctx.route(/^https?:/,r=>{network.push(r.request().url());return r.abort();});
const page=await ctx.newPage();page.setDefaultTimeout(12000);
const report={command:'node design/2026-11-13-v3/verify-v3.mjs',result:'running',checks:[],errors:[],network};
page.on('pageerror',e=>report.errors.push(e.message));
async function load(screen,theme='light'){
 await page.goto(`${pathToFileURL(join(root,'index.html'))}?screen=${screen}&theme=${theme}`);
 await page.waitForFunction(id=>window.DESIGN_RENDER_READY?.id===id,screen);
 await page.evaluate(async()=>{await (window.DESIGN_V3.readyPromise??window.DESIGN_V3.ready);});
}
async function capture(name){await page.screenshot({path:join(root,'screenshots',name+'.png'),fullPage:await page.locator('[role="dialog"]').count()===0});}
try{
 await load('portfolio-dashboard');
 const versions=await page.evaluate(()=>({versions:DesignRuntime.versions,gsap:DesignRuntime.gsap.version,mermaid:typeof DesignRuntime.mermaid.render,d3:typeof DesignRuntime.d3.forceSimulation,icons:Object.keys(DesignRuntime.icons.icons).length}));
 assert.equal(versions.gsap,'3.15.1');assert.equal(versions.mermaid,'function');assert.equal(versions.d3,'function');assert.equal(versions.icons,91);report.runtime=versions;
 assert.ok(await page.locator('[data-renderer="d3"]').count()>0);
 assert.ok(await page.locator('.duo-icon').count()>15);report.checks.push('Local GSAP/D3/Mermaid/Duoicons loaded; actual D3 chart SVG');
 await page.locator('[data-v3-mode="current"]').click();
 assert.equal(await page.locator('[data-renderer="d3"]').count(),0);
 assert.ok((await page.locator('main').innerText()).includes('Нет подтверждённых'));
 await capture('light-current-availability');report.checks.push('Unknown mode removes numeric charts rather than zeroing');
 await page.locator('[data-v3-mode="demo"]').click();
 for(const id of ['demo-ui','demo-docs','demo-data']){
  await load('portfolio-dashboard');await page.locator(`[data-v3-project="${id}"]`).first().click();
  const name=await page.evaluate(id=>DesignFixtures.projects.find(p=>p.id===id).name,id);
  assert.ok((await page.locator('main h1').innerText()).includes(name));
 }
 report.checks.push('All three project drill-downs change scope');
 for(const id of ['demo-builder','demo-reviewer','demo-docs']){
  await load('agents-dashboard');await page.locator(`[data-v3-agent="${id}"]`).first().click();
  const name=await page.evaluate(id=>DesignFixtures.agents.find(p=>p.id===id).name,id);
  assert.ok((await page.locator('main h1').innerText()).includes(name));
 }
 report.checks.push('All three agent drill-downs change scope');
 await load('tasks-list');
 const selectedRow=page.locator('[data-v3-task-row="DEMO-105"]');await selectedRow.click();
 assert.ok((await page.locator('main .inspector').innerText()).includes('DEMO-105'));
 assert.equal(await page.locator('main .inspector [data-v3-open-task]').first().getAttribute('data-v3-open-task'),'DEMO-105');
 report.checks.push('Single click selects coherent inspector and full-card target');
 const taskTarget=page.locator('[data-v3-task-row]').first();
 await taskTarget.dblclick();
 assert.ok(await page.locator('.v3-task-modal[role="dialog"]').isVisible());
 await capture('light-task-dialog');
 assert.equal(await page.locator('.v3-task-tabs [role="tab"]').count(),9);
 const fields=['title','type','parentId','priority','summary','technicalValue','productValue','acceptanceCriteria','estimateSeconds','rank','startDate','dueDate','timezone','components','affectsVersions','fixVersions','risks','blocker.reason','blocker.owner','reason'];
 const names=await page.locator('.v3-task-modal [name]').evaluateAll(xs=>xs.map(x=>x.name));
 for(const field of fields)assert.ok(names.includes(field),`Task field ${field}`);
 await page.locator('.v3-task-modal [name="components"]').selectOption(['Интерфейс','Качество']);
 await page.locator('#v3-task-tab-files').click();
 const details=await page.locator('.v3-task-modal [name]').evaluateAll(xs=>xs.map(x=>x.name));
 for(const field of ['files[0].relativePath','files[0].plannedOperation','files[0].actualOperation','fileContexts[0].revision','fileContexts[0].context','agentAssignments','assignments[0].profileVersion','assignments[0].runId','assignments[0].sessionId','assignments[0].startedAt','assignments[0].endedAt','artifactReferences','artifacts[0].type','artifacts[0].reference','artifacts[0].revision','artifacts[0].provenance','artifacts[0].availability'])assert.ok(details.includes(field),`Detailed field ${field}`);
 await capture('light-task-dialog-files');
 for(const id of ['acceptance','comments','history','attachments','links','sessions','usage']){
  await page.locator(`#v3-task-tab-${id}`).click();assert.ok((await page.locator('#v3-task-panel').innerText()).trim().length>40);
 }
 await page.locator('#v3-task-tab-summary').click();
 assert.equal(await page.locator('.v3-task-modal [name="components"] option:checked').count(),2);
 report.checks.push('Multiple-selection survives modal tab rerender');
 await page.locator('#v3-task-tab-summary').focus();await page.keyboard.press('ArrowRight');
 assert.equal(await page.evaluate(()=>document.activeElement.id),'v3-task-tab-files');
 await page.locator('.v3-task-modal button').last().focus();await page.keyboard.press('Tab');
 assert.ok(await page.evaluate(()=>!!document.activeElement.closest('.v3-task-modal')));
 await page.keyboard.press('Escape');assert.equal(await page.locator('.v3-task-modal').count(),0);
 assert.ok(await page.evaluate(()=>!!document.activeElement.closest('[data-v3-task-row]')));
 await taskTarget.focus();await page.keyboard.press('Enter');assert.ok(await page.locator('.v3-task-modal').isVisible());await page.keyboard.press('Escape');
 report.checks.push('Task dblclick/Enter, complete fields, 9 tabs, keyboard focus trap/Escape return');
 await load('tasks-list','dark');await page.locator('[data-v3-task-row]').first().dblclick();await capture('dark-task-dialog');await page.keyboard.press('Escape');
 await load('tasks-list');await page.locator('[data-v3-task-row="DEMO-107"]').click();
 await page.evaluate(async()=>{navigate('task-usage');await DESIGN_V3.ready;});
 assert.equal(await page.locator('.v3-chart .bar').count(),0);
 assert.ok((await page.locator('main').innerText()).includes('Неизвестно'));
 report.checks.push('All-unknown task tool breakdown has no fake zero bars');
 await load('session-usage');assert.ok((await page.locator('main').innerText()).includes('23 200')||(await page.locator('main').innerText()).includes('23 200'));
 report.checks.push('Direct session usage resolves the existing synthetic run');
 await load('graph-map');assert.ok(await page.locator('[data-renderer="d3-force"]').count()>0);
 const graphCount=await page.locator('.v3-graph-node').count();
 const transform=await page.locator('.v3-graph-viewport').getAttribute('transform');
 await page.locator('[data-v3-zoom="in"]').click();assert.notEqual(await page.locator('.v3-graph-viewport').getAttribute('transform'),transform);
 await page.locator('#v3-graph-module').selectOption('contracts');
 assert.equal(await page.locator('.v3-graph-node').count(),3);
 await page.locator('.v3-graph-node').first().focus();await page.keyboard.press('Enter');
 assert.equal(await page.locator('.v3-graph-node[aria-pressed="true"]').count(),1);
 await load('graph-mermaid');assert.ok(await page.locator('.v3-mermaid svg').count()>0);await capture('light-mermaid-whole');
 assert.equal(await page.locator('.v3-mermaid g.node').count(),graphCount);
 await page.locator('#v3-mermaid-module').selectOption('contracts');await page.evaluate(async()=>await DESIGN_V3.ready);
 assert.equal(await page.locator('.v3-mermaid g.node').count(),3);
 await capture('light-mermaid-module');
 report.checks.push('D3 graph zoom/filter/keyboard; Mermaid whole/module same node counts');
 await page.emulateMedia({reducedMotion:'no-preference'});
 const liveTweens=await page.evaluate(async()=>{navigate('overview');await DESIGN_V3.ready;await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));return DesignRuntime.gsap.globalTimeline.getChildren().filter(t=>t.isActive()).length;});
 assert.ok(liveTweens>0);report.liveGsapTweens=liveTweens;
 await page.emulateMedia({reducedMotion:'reduce'});await page.evaluate(async()=>{navigate('agents-dashboard');await DESIGN_V3.ready;});
 assert.equal(await page.evaluate(()=>DesignRuntime.gsap.globalTimeline.getChildren().filter(t=>t.isActive()).length),0);
 report.checks.push('GSAP route animation active; reduced-motion has no active tween');
 assert.deepEqual(network,[]);assert.deepEqual(report.errors,[]);report.result='passed';report.exitCode=0;
}catch(error){report.result='failed';report.exitCode=1;report.failure=error.message;await capture('v3-check-failure');throw error;}
finally{await writeFile(join(root,'v3-check-report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));await browser.close();}
