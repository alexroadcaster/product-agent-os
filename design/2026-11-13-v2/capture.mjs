import {chromium} from 'file:///C:/Users/user/AppData/Local/npm-cache/_npx/eb7983f9b02fb67f/node_modules/playwright-core/index.mjs';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {dirname,join} from 'node:path';
import {mkdir,writeFile,access,rename} from 'node:fs/promises';
import assert from 'node:assert/strict';

// Only this offline synthetic artifact is loaded. No server or application profile is used.
const root=dirname(fileURLToPath(import.meta.url));
const executable='C:/Users/user/AppData/Local/ms-playwright/chromium-1223/chrome-win64/chrome.exe';
await access(executable);
await mkdir(join(root,'screenshots'),{recursive:true});
const browser=await chromium.launch({executablePath:executable,headless:true});
const context=await browser.newContext({viewport:{width:1440,height:1000},deviceScaleFactor:1,reducedMotion:'reduce'});
await context.route(/^https?:/,route=>route.abort());
const page=await context.newPage();
const errors=[];const consoleErrors=[];
page.on('pageerror',error=>errors.push(error.message));
page.on('console',message=>{if(message.type()==='error')consoleErrors.push(message.text());});
const url=(id,theme='light',extra='')=>`${pathToFileURL(join(root,'index.html')).href}?screen=${id}&theme=${theme}${extra}`;
const keys=['tasks-list','sessions-work','workflow-transitions','motion-lab'];
const keyOnly=process.argv.includes('--key');
const interactionsOnly=process.argv.includes('--interactions');
const output={result:'running',command:`node design/2026-11-13-v2/capture.mjs ${process.argv.slice(2).join(' ')}`.trim(),exitCode:null,browser:'installed Chromium / disposable context',browserPlugin:'not available',pageIdentity:true,uniqueRoutes:80,routes:0,screenshots:0,desktopLayouts:0,meaningfulBodies:0,contrastSamples:0,minimumTextContrast:null,minimumControlContrast:null,interactions:[],errors,consoleErrors,
 previousFailedAttempt:{command:'node design/2026-11-13-v2/capture.mjs --interactions',exitCode:1,observed:'AssertionError: tasks-list: meaningful body while checking an alternate empty/loading specimen',cause:'The original harness applied the full-screen 180-character minimum to intentionally short alternate states.',repair:'Alternate states require meaningful text plus semantic empty-region/aria-busy checks; full routes retain the 180-character requirement.',followup:'The corrected interaction-only run passed before full capture.'}};
const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
async function load(id,theme='light',extra=''){
 await page.goto(url(id,theme,extra));
 await page.waitForFunction(({id,theme})=>window.DESIGN_RENDER_READY?.id===id&&window.DESIGN_RENDER_READY?.theme===theme,{id,theme});
 await page.evaluate(()=>{document.documentElement.dataset.capture='true';});
 assert.ok((await page.title()).endsWith(': Product-Agent OS'));
 const alternateState=extra.includes('&state=');
 assert.ok((await page.locator('[data-content-route]').innerText()).trim().length>(alternateState?60:180),`${id}: meaningful body`);
 if(extra.includes('state=empty'))assert.equal(await page.locator('.empty-region').count(),1);
 if(extra.includes('state=loading'))assert.equal(await page.locator('[aria-busy="true"]').count(),1);
 assert.equal(await page.locator('main h1').count(),1,`${id}: single heading`);
 assert.equal(await page.locator('.nav-link').count(),14);
}
async function layoutCheck(id,theme,width){
 await page.setViewportSize({width,height:1000});
 const layout=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,
  controls:[...document.querySelectorAll('main button,main input,main select,main textarea,main table,.modal button,.modal input,.modal select,.review-ribbon')]
   .filter(el=>el.getClientRects().length).filter(el=>{const r=el.getBoundingClientRect();return r.right>innerWidth+1||r.left<0;}).map(el=>el.outerHTML.slice(0,120))}));
 assert.equal(layout.scroll,layout.width,`${id}/${theme}/${width}: page overflow`);
 assert.deepEqual(layout.controls,[],`${id}/${theme}/${width}: clipped control`);output.desktopLayouts++;
}
// Composite inherited painted backgrounds and sample real text/control pairs. This is not a full WCAG audit.
async function contrastCheck(id,theme){
 // Sample computed foreground/background pairs, not token intent; disabled controls are excluded.
 const samples=await page.evaluate(()=>{
  const rgb=value=>{const m=value.match(/[\d.]+/g).map(Number);return m.slice(0,3);};
  const lum=value=>rgb(value).map(v=>{const c=v/255;return c<=.04045?c/12.92:((c+.055)/1.055)**2.4;}).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
  const ratio=(a,b)=>{const x=[lum(a),lum(b)].sort((a,b)=>b-a);return(x[0]+.05)/(x[1]+.05);};
  const background=el=>{while(el){const b=getComputedStyle(el).backgroundColor;if(b!=='rgba(0, 0, 0, 0)')return b;el=el.parentElement;}return getComputedStyle(document.body).backgroundColor;};
  const selectors=['main h1','.page-title p','.nav-link.active','.inspector-body p','.lead','.badge.sage','.badge.amber','.badge.coral','.badge.neutral','.primary','.field label','.field small','.field input','.field select','.data-list .row-title','.meta','.section-tabs a.active','.review-ribbon a'];
  const values=[];
  for(const selector of selectors){for(const el of [...document.querySelectorAll(selector)].filter(el=>el.getClientRects().length&&!el.matches(':disabled')).slice(0,3)){const style=getComputedStyle(el);if(style.opacity!=='1')continue;values.push({selector,type:'text',ratio:ratio(style.color,background(el))});}}
  for(const el of [...document.querySelectorAll('.field input:not([type="checkbox"]),.field select,.field textarea,.search-field')].filter(el=>el.getClientRects().length&&!el.matches(':disabled')).slice(0,8)){values.push({selector:el.tagName,type:'control',ratio:ratio(getComputedStyle(el).borderTopColor,background(el))});}
  return values;
 });
 for(const sample of samples){assert.ok(sample.ratio>=(sample.type==='text'?4.5:3),`${id}/${theme} ${sample.type} ${sample.selector}: contrast ${sample.ratio}`);if(sample.type==='text')output.minimumTextContrast=Math.min(output.minimumTextContrast??Infinity,sample.ratio);else output.minimumControlContrast=Math.min(output.minimumControlContrast??Infinity,sample.ratio);output.contrastSamples++;}
}
function gallery(coverage){const cards=coverage.routes.flatMap(r=>coverage.themes.map(theme=>`<article data-group="${r.group}" data-theme="${theme}" data-name="${esc(`${r.title} ${r.id}`.toLowerCase())}"><a href="index.html?screen=${r.id}&amp;theme=${theme}"><img src="${r.screenshots[theme]}" alt="${esc(r.title)} / ${theme}" loading="lazy" width="1440" height="1000"><strong>${esc(r.title)}</strong><small>${theme==='light'?'Porcelain':'Obsidian'} / ${r.id}</small></a></article>`)).join('');return `<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Product-Agent OS: галерея 80 экранов</title><link rel="stylesheet" href="tokens.css"><style>html,body{margin:0;background:var(--canvas);color:var(--ink);font-family:var(--font-body);overflow-x:clip}body{padding:24px}header{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}h1{font-size:24px}p,small{color:var(--muted)}a{color:var(--accent-text);text-decoration:none}input,select{font:inherit;padding:8px;background:var(--surface);color:var(--ink);border:1px solid var(--control-line);border-radius:6px}a:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid var(--focus);outline-offset:3px}.filters{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;max-width:1680px;margin:auto}article{min-width:0}img{display:block;width:100%;height:250px;object-fit:contain;object-position:top;background:var(--recess);border:1px solid var(--line);border-radius:8px}strong{display:block;margin-top:12px;font-size:14px}small{display:block;margin-top:4px;font-size:12px}[hidden]{display:none!important}</style></head><body><header><div><h1>Полный альбом Product-Agent OS</h1><p>80 содержательных экранов в двух темах. Синтетические данные, функции приложения не изменяются.</p></div><a href="index.html">Открыть интерактивный альбом</a></header><div class="filters"><label>Тема <select id="theme"><option value="all">Обе темы</option><option value="light">Porcelain</option><option value="dark">Obsidian</option></select></label><label>Раздел <select id="group"><option value="all">Все разделы</option>${[...new Set(coverage.routes.map(r=>r.group))].map(group=>`<option>${group}</option>`).join('')}</select></label><input id="query" type="search" placeholder="Найти экран" aria-label="Найти экран"><span id="count">160 изображений</span></div><div class="grid">${cards}</div><script>function filter(){const t=document.querySelector('#theme').value,g=document.querySelector('#group').value,q=document.querySelector('#query').value.toLowerCase();let n=0;document.querySelectorAll('article').forEach(el=>{el.hidden=(t!=='all'&&el.dataset.theme!==t)||(g!=='all'&&el.dataset.group!==g)||!el.dataset.name.includes(q);if(!el.hidden)n++;});document.querySelector('#count').textContent=n+' изображений';}document.querySelectorAll('select,input').forEach(el=>el.addEventListener('input',filter));</script></body></html>`;}
try{
 await load('tasks-list');
 const coverage=await page.evaluate(()=>window.DESIGN_COVERAGE);
 assert.equal(coverage.routes.length,80);assert.equal(new Set(coverage.routes.map(r=>r.id)).size,80);
 await writeFile(join(root,'coverage.json'),JSON.stringify(coverage,null,2)+'\n','utf8');
 await writeFile(join(root,'contact-sheet.html'),gallery(coverage),'utf8');
 const ordered=interactionsOnly?[]:keyOnly?keys:coverage.routes.map(r=>r.id);
 for(const theme of ['light','dark'])for(const id of ordered){
  await load(id,theme);await contrastCheck(id,theme);
  for(const width of [1280,1440,1920])await layoutCheck(id,theme,width);
  await page.setViewportSize({width:1440,height:1000});
  await page.screenshot({path:join(root,'screenshots',`${theme}-${id}.png`),fullPage:true});
  output.routes++;output.screenshots++;output.meaningfulBodies++;
 }
 if(!keyOnly){
  for(const theme of ['light','dark'])for(const selected of ['loading','empty','error','stale']){
   await load('tasks-list',theme,`&state=${selected}`);await layoutCheck(`tasks-${selected}`,theme,1280);
   await page.screenshot({path:join(root,'screenshots',`${theme}-state-${selected}.png`),fullPage:true});output.screenshots++;
  }
  await load('tasks-list');await page.keyboard.press('Tab');
  assert.equal(await page.evaluate(()=>getComputedStyle(document.activeElement).outlineWidth),'2px');output.interactions.push('Keyboard focus visible');
  await load('task-summary');await page.locator('#tab-task-summary').focus();await page.keyboard.press('ArrowRight');await page.waitForFunction(()=>window.DESIGN_RENDER_READY.id==='task-files');assert.equal(await page.evaluate(()=>document.activeElement.id),'tab-task-files');await page.keyboard.press('End');assert.equal(await page.evaluate(()=>document.activeElement.id),'tab-task-sessions');await page.keyboard.press('Home');assert.equal(await page.evaluate(()=>document.activeElement.id),'tab-task-summary');assert.equal(await page.locator('#tab-task-summary').getAttribute('aria-selected'),'true');output.interactions.push('APG object tabs Arrow/Home/End preserve focused selected tab');
  await page.locator('[data-action="task-menu"]').click();await page.keyboard.press('Escape');assert.equal(await page.evaluate(()=>document.activeElement.dataset.action),'task-menu');assert.equal(await page.locator('[data-action="task-menu"]').getAttribute('aria-expanded'),'false');output.interactions.push('Context menu Escape focus return');
  await page.locator('#catalog-button').click();await page.locator('#catalog-query').fill('скилл');assert.ok(await page.locator('[data-catalog-item]:visible').count()>4);
  await page.keyboard.press('Escape');assert.equal(await page.locator('[role="dialog"]').count(),0);output.interactions.push('Catalog search and Escape');
  await load('task-delete');assert.ok(await page.locator('[role="dialog"]').isVisible());assert.ok(await page.locator('#task-delete-button').isDisabled());await page.locator('#task-delete-confirm').check();assert.ok(await page.locator('#task-delete-button').isEnabled());
  const dialogFocus=await page.evaluate(()=>document.activeElement.closest('[role="dialog"]')!==null);assert.ok(dialogFocus);await page.keyboard.press('Escape');await page.waitForFunction(()=>window.DESIGN_RENDER_READY.id==='task-summary');output.interactions.push('Modal confirmation and Escape route');
  await load('workflow-transitions');await page.locator('[data-transition="5"]').click();assert.equal(await page.locator('#transition-checks').inputValue(),'criteria,dependencies,children,blocker');output.interactions.push('Transition selected fields');
  await load('document-proposal');assert.ok(await page.locator('#document-save').isDisabled());await page.locator('#document-confirm').check();await page.locator('#document-save').click();await page.locator('#toast').filter({hasText:'Данные приложения не изменяются'}).waitFor();output.interactions.push('Staged proposal demo-only confirmation');
  await load('component-lab');await page.locator('#lab-process-id').fill('неверный id');await page.locator('#lab-process-id').blur();assert.equal(await page.locator('#lab-process-id').getAttribute('aria-invalid'),'true');await page.locator('[data-action="lab-menu"]').click();assert.ok(await page.locator('#lab-menu').isVisible());await page.keyboard.press('Escape');assert.ok(await page.locator('#lab-menu').isHidden());output.interactions.push('Inline validation, popover');
  await load('motion-lab');await page.locator('#lab-copy').click();await page.locator('#copy-feedback').filter({hasText:'Симуляция подтверждения'}).waitFor();await page.locator('[data-lab-select="Доска"]').click();assert.equal(await page.locator('[data-lab-select="Доска"]').getAttribute('aria-pressed'),'true');await page.locator('#inspector-toggle').click();assert.ok(await page.locator('#motion-inspector').isHidden());await page.locator('#inspector-toggle').click();assert.ok(await page.locator('#motion-inspector').isVisible());await page.locator('#lab-progress').focus();await page.keyboard.press('End');assert.equal(await page.locator('#lab-progressbar').getAttribute('aria-valuenow'),'100');await page.locator('#lab-pause').click();assert.ok(await page.locator('#lab-recover').isEnabled());await page.locator('#lab-recover').click();output.interactions.push('Copy, segmented, inspector, progress, pause/recover');
  assert.equal(await page.locator('.spinning').evaluate(el=>getComputedStyle(el).animationName),'none');output.interactions.push('Reduced motion static fallback');
  await page.emulateMedia({reducedMotion:'no-preference'});await page.locator('#inspector-toggle').click();await page.waitForFunction(()=>document.querySelector('#motion-inspector').hidden);await page.locator('#inspector-toggle').click();await page.waitForFunction(()=>!document.querySelector('#motion-inspector').hidden);output.interactions.push('Motion enabled enter/exit');
  try{
   const videoContext=await browser.newContext({viewport:{width:1440,height:1000},recordVideo:{dir:join(root,'screenshots'),size:{width:1440,height:1000}},reducedMotion:'no-preference'});
   await videoContext.route(/^https?:/,route=>route.abort());
   const motionPage=await videoContext.newPage();
   const recording=motionPage.video();
   await motionPage.goto(url('motion-lab','dark'));
   await motionPage.waitForFunction(()=>window.DESIGN_RENDER_READY?.id==='motion-lab');
   for(const selector of ['#lab-copy','[data-lab-select="Доска"]','#inspector-toggle','#inspector-toggle']){await motionPage.locator(selector).click();await motionPage.waitForTimeout(600);}
   await motionPage.locator('#lab-progress').focus();await motionPage.keyboard.press('End');await motionPage.waitForTimeout(600);
   await motionPage.locator('#lab-pause').click();await motionPage.waitForTimeout(600);await motionPage.locator('#lab-recover').click();await motionPage.waitForTimeout(600);
   await videoContext.close();
   await rename(await recording.path(),join(root,'screenshots','motion-demo.webm'));
   output.motionVideo='screenshots/motion-demo.webm';
  }catch(error){output.motionVideoGap=error.message;}
 }
 assert.deepEqual(errors,[]);assert.deepEqual(consoleErrors,[]);
 output.result='passed';output.exitCode=0;await writeFile(join(root,'capture-report.json'),JSON.stringify(output,null,2)+'\n','utf8');console.log(JSON.stringify(output,null,2));
}catch(error){output.result='failed';output.exitCode=1;output.failure=error.message;await writeFile(join(root,'capture-report.json'),JSON.stringify(output,null,2)+'\n','utf8');throw error;
}finally{await browser.close();}
