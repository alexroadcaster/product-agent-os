import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {createLocalApplication} from '../../apps/local-service/src/http/application.mts';
import {createSessionGate} from '../../apps/local-service/src/http/session-gate.mts';
import {createBrowserLaunch} from '../../apps/local-service/src/http/browser-launch.mts';

const origin='http://127.0.0.1:43127';
const navigation={'sec-fetch-site':'none','sec-fetch-mode':'navigate','sec-fetch-dest':'document','sec-fetch-user':'?1'};
async function fixture(t:any){
 const root=await mkdtemp(join(tmpdir(),'paos-launch-'));
 const store=await openLocalStore({databasePath:join(root,'state.sqlite')});
 t.after(async()=>{await store.close();await rm(root,{recursive:true,force:true});});
 return createLocalApplication({store,origin,instanceId:'launch-fixture',profileDirectory:root});
}
function request(path:string,headers:Record<string,string>={},payload?:unknown){return new Request(origin+path,{method:payload===undefined?'GET':'POST',headers:{host:new URL(origin).host,...headers},...(payload===undefined?{}:{body:JSON.stringify(payload)})});}
async function bootstrap(app:Awaited<ReturnType<typeof fixture>>){
 const response=await app.handleRequest(request('/launch',navigation));
 assert.equal(response.status,200,'direct browser navigation must provide automatic bootstrap');
 const html=await response.text();
 const proof=/const proof="([a-f0-9]{64})"/.exec(html)?.[1];
 assert.equal(typeof proof,'string','bootstrap must provide a body-bound proof');
 const cookie=response.headers.get('set-cookie')!.split(';')[0];
 return {proof,cookie,response,html};
}
const exchange=(app:any,b:any)=>app.handleRequest(request('/bootstrap/launch',{origin,cookie:b.cookie,'content-type':'application/json','sec-fetch-site':'same-origin','sec-fetch-mode':'cors','sec-fetch-dest':'empty'},{proof:b.proof}));

test('direct local browser launch exchanges a one-use challenge without a code or URL secret',async t=>{
 const app=await fixture(t),b=await bootstrap(app);
 assert.equal(b.response.headers.get('cache-control'),'no-store');
 assert.match(b.response.headers.get('content-security-policy')!,/frame-ancestors 'none'/);
 assert.match(b.response.headers.get('set-cookie')!,/HttpOnly; SameSite=Strict/);
 assert.equal(b.html.includes('location.replace("/")'),true);
 const result=await exchange(app,b);assert.equal(result.status,200);
 const session=await result.json();assert.equal(typeof session.csrfToken,'string');
 const cookie=result.headers.getSetCookie().find(c=>c.startsWith('paos_session_'))!.split(';')[0];
 assert.equal((await app.handleRequest(request('/api/v1/session',{cookie}))).status,200);
 assert.equal((await exchange(app,b)).status,403,'challenge replay must fail');
 const noCsrf=await app.handleRequest(request('/api/v1/preferences',{origin,cookie,'content-type':'application/json'},{locale:'en',theme:'dark'}));
 assert.equal(noCsrf.status,403,'automatic login must preserve CSRF');
});

test('launch rejects browser-controlled navigations, embeds, fetches, missing metadata and URL data',async t=>{
 const app=await fixture(t);
 const cases=[{}, {...navigation,'sec-fetch-site':'cross-site'}, {...navigation,'sec-fetch-site':'same-site'},
  {...navigation,'sec-fetch-site':'same-origin'}, {...navigation,'sec-fetch-dest':'iframe'},
  {...navigation,'sec-fetch-mode':'cors'}, {...navigation,'sec-fetch-user':'?0'},
  {...navigation,origin:'null'}, {...navigation,referer:origin+'/'}, {...navigation,forwarded:'for=127.0.0.1'},
  {...navigation,'x-forwarded-for':'127.0.0.1'}, {...navigation,host:'foreign.example'}];
 for(const headers of cases)assert.equal((await app.handleRequest(request('/launch',headers))).status,403);
 assert.equal((await app.handleRequest(request('/launch?next=other',navigation))).status,403);
 assert.equal((await app.handleRequest(request('/launch',navigation,{}))).status,403);
 assert.equal((await app.handleRequest(request('/api/v1/projects'))).status,401);
});

test('launch exchange requires both proof and same-origin challenge and preserves other sessions',async t=>{
 const app=await fixture(t),first=await bootstrap(app),second=await bootstrap(app);
 const invalid=await exchange(app,{...first,cookie:second.cookie});assert.equal(invalid.status,403);
 const result=await exchange(app,first);assert.equal(result.status,200);
 const cookie=result.headers.getSetCookie().find(c=>c.startsWith('paos_session_'))!.split(';')[0];
 assert.equal((await exchange(app,second)).status,200);
 assert.equal((await app.handleRequest(request('/api/v1/session',{cookie}))).status,200);
 const reopened=await app.handleRequest(request('/launch',{...navigation,cookie}));
 assert.equal(reopened.status,303);assert.equal(reopened.headers.get('location'),'/');
 app.revokeSessions();
 assert.equal((await app.handleRequest(request('/api/v1/session',{cookie}))).status,401);
});

test('bootstrap challenges expire, revoke and stay bounded; concurrent exchange admits once',async()=>{
 let now=0;const gate=createSessionGate({origin,instanceId:'clock',now:()=>now});
 const launch=createBrowserLaunch({gate,instanceId:'clock',now:()=>now});
 async function challenge(){const response=launch.navigate(request('/launch',navigation));const proof=/const proof="([a-f0-9]{64})"/.exec(await response.text())![1];return {proof,cookie:response.headers.get('set-cookie')!.split(';')[0]};}
 const req=(b:any)=>request('/bootstrap/launch',{origin,cookie:b.cookie,'content-type':'application/json','sec-fetch-site':'same-origin','sec-fetch-mode':'cors','sec-fetch-dest':'empty'},{});
 const old=await challenge();now=30_000;assert.throws(()=>launch.exchange(req(old),old.proof),{code:'LAUNCH_REJECTED'});
 const revoked=await challenge();launch.revoke();assert.throws(()=>launch.exchange(req(revoked),revoked.proof),{code:'LAUNCH_REJECTED'});
 const first=await challenge();for(let i=0;i<16;i++)await challenge();assert.throws(()=>launch.exchange(req(first),first.proof),{code:'LAUNCH_REJECTED'});
 const fresh=await challenge();const results=await Promise.allSettled([Promise.resolve().then(()=>launch.exchange(req(fresh),fresh.proof)),Promise.resolve().then(()=>launch.exchange(req(fresh),fresh.proof))]);
 assert.equal(results.filter(r=>r.status==='fulfilled').length,1);
 for(const patch of [{'sec-fetch-site':'cross-site'},{'sec-fetch-mode':'navigate'},{origin:'null'},{'sec-fetch-dest':'document'},{'content-type':'text/plain'}]){
  const b=await challenge();const invalid=new Request(req(b),{headers:{...Object.fromEntries(req(b).headers),...patch}});
  assert.throws(()=>launch.exchange(invalid,b.proof));
 }
});
