import {chromium} from 'file:///C:/Users/user/AppData/Local/npm-cache/_npx/eb7983f9b02fb67f/node_modules/playwright-core/index.mjs';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {dirname, join} from 'node:path';
import {access} from 'node:fs/promises';
import assert from 'node:assert/strict';

// Capture only this offline synthetic design artifact using a disposable browser context.
const root=dirname(fileURLToPath(import.meta.url));
const executable='C:/Users/user/AppData/Local/ms-playwright/chromium-1223/chrome-win64/chrome.exe';
await access(executable);
const browser=await chromium.launch({executablePath:executable,headless:true});
const context=await browser.newContext({viewport:{width:1440,height:1000},deviceScaleFactor:1});
const page=await context.newPage();
await page.emulateMedia({reducedMotion:'reduce'});
const errors=[];
page.on('pageerror',error=>errors.push(error.message));
await context.route(/^https?:/,route=>route.abort());
const url=(theme,screen)=>`${pathToFileURL(join(root,'index.html')).href}?theme=${theme}&screen=${screen}`;
const receipts=[];
const contrastReceipts=[];
try{
  for(const theme of ['cobalt','mint','warm']){
    for(const screen of ['tasks','connection','workflows','sessions','components']){
      await page.goto(url(theme,screen));
      await page.locator('main h1').waitFor();
      const contrast=await page.evaluate(()=>{
        const rgb=value=>value.match(/[\d.]+/g).slice(0,3).map(Number);
        const luminance=value=>rgb(value).map(channel=>{const c=channel/255;return c<=.04045?c/12.92:((c+.055)/1.055)**2.4;}).reduce((sum,value,index)=>sum+value*[.2126,.7152,.0722][index],0);
        return ['main h1','.page-heading p'].map(selector=>{
          const el=document.querySelector(selector);let ancestor=el;let background;
          while(ancestor){background=getComputedStyle(ancestor).backgroundColor;if(background!=='rgba(0, 0, 0, 0)')break;ancestor=ancestor.parentElement;}
          const foreground=getComputedStyle(el).color;
          const values=[luminance(foreground),luminance(background)].sort((a,b)=>b-a);
          return {selector,ratio:(values[0]+.05)/(values[1]+.05)};
        });
      });
      for(const sample of contrast)assert.ok(sample.ratio>=4.5,`${theme}/${screen}: text contrast ${sample.selector} ${sample.ratio}`);
      contrastReceipts.push({theme,screen,samples:contrast});
      await page.screenshot({path:join(root,`${theme}-${screen}.png`),fullPage:true});
      for(const width of [1280,1440,1920]){
        await page.setViewportSize({width,height:1000});
        const layout=await page.evaluate(()=>({
          width:innerWidth,scroll:document.documentElement.scrollWidth,
          overflow:[...document.querySelectorAll('main button,main input,main select,main textarea,.sidebar,.app-header')]
            .filter(el=>el.getClientRects().length)
            .filter(el=>{const r=el.getBoundingClientRect();return r.right>innerWidth+1||r.left<0;})
            .map(el=>el.outerHTML.slice(0,100))
        }));
        assert.equal(layout.scroll,layout.width,`${theme}/${screen}/${width}: page overflow`);
        assert.equal(layout.overflow.length,0,`${theme}/${screen}/${width}: clipped controls ${layout.overflow}`);
        receipts.push(`${theme}/${screen}/${width}: fit`);
      }
      await page.setViewportSize({width:1440,height:1000});
    }
  }
  await page.goto(url('cobalt','tasks'));
  await page.keyboard.press('Tab');
  const keyboardFocus=await page.evaluate(()=>({tag:document.activeElement.tagName,style:getComputedStyle(document.activeElement).outlineStyle,width:getComputedStyle(document.activeElement).outlineWidth}));
  assert.equal(keyboardFocus.tag,'A');
  assert.equal(keyboardFocus.style,'solid');
  assert.equal(keyboardFocus.width,'2px');
  assert.equal(await page.locator('.nav-button').count(),14);
  assert.equal(await page.locator('[data-task-tab]').count(),8);
  await page.getByRole('button',{name:'B Graphite Mint',exact:true}).click();
  assert.equal(await page.locator('html').getAttribute('data-theme'),'mint');
  await page.locator('[data-task="UI-103"]').first().click();
  await page.locator('.inspector h2').filter({hasText:'Проверить доступность'}).waitFor();
  await page.locator('[data-task-tab="Комментарии"]').click();
  await page.getByRole('tabpanel').filter({hasText:'Демонстрационный комментарий'}).waitFor();
  await page.locator('.screen-selector [data-screen="workflows"]').click();
  await page.locator('[data-transition="5"]').click();
  assert.equal(await page.locator('#wf-id').inputValue(),'awaiting_acceptance-done');
  assert.equal(await page.locator('#wf-checks').inputValue(),'criteria,dependencies,children,blocker');
  await page.getByRole('button',{name:'Сохранить черновик',exact:true}).click();
  await page.locator('#notice').filter({hasText:'Данные приложения не изменяются'}).waitFor();
  await page.emulateMedia({reducedMotion:'reduce'});
  const animation=await page.locator('.workflow-editor').evaluate(el=>getComputedStyle(el).animationName);
  assert.equal(animation,'none');
  await page.goto(url('cobalt','tasks'));
  await page.locator('#task-search').fill('перенос');
  assert.equal(await page.locator('.task-row:visible').count(),1);
  assert.deepEqual(errors,[]);
  console.log(JSON.stringify({result:'passed',screenshots:15,desktopLayouts:receipts.length,
    interactions:['14 navigation destinations','8 task tabs','theme switch','task selection','task tab',
      'transition selection with preserved fields','demo-only action notice','reduced motion','task filtering','keyboard visible focus'],
    sampledContrastPairs:contrastReceipts.length*2,minimumContrast:Math.min(...contrastReceipts.flatMap(receipt=>receipt.samples.map(sample=>sample.ratio))),
    pageErrors:errors,network:'HTTP(S) aborted; file-only artifact'},null,2));
}finally{await browser.close();}
