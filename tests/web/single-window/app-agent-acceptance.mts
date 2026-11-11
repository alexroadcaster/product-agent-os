import {mkdtemp,mkdir,readFile,writeFile,rm} from 'node:fs/promises';
import {join,resolve,isAbsolute} from 'node:path';
import {pathToFileURL} from 'node:url';
import {randomUUID} from 'node:crypto';
import {startLocalService} from '../../../apps/local-service/src/main.mts';
import {appLabel} from '../../../apps/web/src/locales/app.ts';
import {uiLabel} from '../../../apps/web/src/locales/messages.ts';

/** Explicit real App worker acceptance. The host must attach an actual agent; no fixture RPC or provider SDK. */
async function main(){
 const args=Object.fromEntries(process.argv.slice(2).reduce<string[][]>((rows,item,index,array)=>{if(item.startsWith('--'))rows.push([item,array[index+1]]);return rows;},[]));
 if(!process.argv.includes('--app-agent-browser')||!isAbsolute(args['--playwright-core']??'')||!isAbsolute(args['--chromium']??''))throw new Error('EXPLICIT_APP_AGENT_BROWSER_REQUIRED');
 const work=resolve('.tmp/paos-m1');await mkdir(work,{recursive:true});const root=await mkdtemp(join(work,'app-agent-live-'));
 const output=await mkdtemp(join(work,'app-agent-evidence-'));const coordination=join(work,'app-agent-live-coordination.json');
 const workspace=join(root,'workspace'),profileDirectory=join(root,'profile'),browserHome=join(root,'browser');await mkdir(workspace);await mkdir(browserHome);
 const report:any={schemaVersion:'paos_app_agent_acceptance_v1',actualAppAgent:false,actualAppServer:false,externalProviderClient:false,apiKey:false,nativeSandbox:false,checks:[],screenshots:[],pageErrorCount:0,blockedExternalRequests:0,startedAt:new Date().toISOString()};
 const check=(name:string,passed:boolean)=>{report.checks.push({name,passed});if(!passed)throw new Error(name);};
 let service:Awaited<ReturnType<typeof startLocalService>>|undefined,context:any;
 const note=async(value:unknown)=>writeFile(coordination,JSON.stringify(value,null,2));
 try{
  service=await startLocalService({profileDirectory,instanceId:randomUUID()});const origin=`http://127.0.0.1:${service.port}`;
  const {chromium}=await import(pathToFileURL(join(args['--playwright-core'],'index.mjs')).href);
  context=await chromium.launchPersistentContext(browserHome,{headless:true,chromiumSandbox:true,serviceWorkers:'block',viewport:{width:1440,height:1000},locale:'ru-RU',executablePath:args['--chromium'],timeout:20000,
   env:{SystemRoot:process.env.SystemRoot!,USERPROFILE:browserHome,HOME:browserHome,APPDATA:browserHome,LOCALAPPDATA:browserHome,TEMP:browserHome,TMP:browserHome}});
  await context.route('**/*',async(route:any)=>{if(new URL(route.request().url()).origin===origin)await route.continue();else{report.blockedExternalRequests++;await route.abort();}});
  const page=context.pages()[0]??await context.newPage();page.setDefaultTimeout(15000);page.on('pageerror',()=>report.pageErrorCount++);
  await page.goto(origin);await page.getByLabel(appLabel('ru','code'),{exact:true}).fill(service.pairingCode);
  const exchange=page.waitForResponse((response:any)=>response.url()===origin+'/api/v1/bootstrap/exchange'&&response.status()===200);
  await page.getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();const csrf=(await(await exchange).json()).csrfToken;
  async function api(path:string,input?:unknown){return page.evaluate(async({path,input,csrf}:any)=>{const response=await fetch('/api/v1'+path,{method:input===undefined?'GET':'POST',headers:{'content-type':'application/json','x-paos-csrf':csrf},...(input===undefined?{}:{body:JSON.stringify(input)})});return {status:response.status,body:await response.json()};},{path,input,csrf});}
  async function nav(section:string){await page.locator('nav').getByRole('button',{name:uiLabel('ru',`nav.${section}` as any),exact:true}).click();}
  async function until(name:string,predicate:()=>Promise<boolean>,timeout=15000){const deadline=Date.now()+timeout;while(Date.now()<deadline){if(await predicate()){check(name,true);return;}await new Promise(resolve=>setTimeout(resolve,250));}check(name,false);}
  const created=await api('/projects',{name:'Codex App bridge acceptance',workspaceRoot:workspace,keyPrefix:'APPA'});check('project_registered',created.status===201);const project=created.body,sessionId=randomUUID();
  check('session_saved',(await api(`/projects/${project.id}/commands`,{expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:'app-acceptance-session',changes:[{expectedRevision:0,entity:{id:sessionId,kind:'session',title:'Actual Codex App agent',data:{mode:'discussion'}}}]})).status===200);
  await page.reload();await page.locator('.navigation select:enabled').waitFor();await page.locator('.navigation select').selectOption(project.id);await nav('settings');
  check('app_route_default',await page.getByLabel(appLabel('ru','connectionRoute'),{exact:true}).inputValue()==='codex_app_agent');
  check('no_api_key_input',await page.locator('input[name=apiKey]').count()===0);
  const connectionResponse=page.waitForResponse((response:any)=>response.url()===origin+'/api/v1/connection'&&response.request().method()==='POST');
  await page.locator('.panel').filter({has:page.getByLabel(appLabel('ru','connectionRoute'),{exact:true})}).getByRole('button',{name:appLabel('ru','openAppAgentChannel'),exact:true}).click();
  check('app_route_connected_waiting',(await connectionResponse).status()===200);
  const shared={descriptorPath:service.appAgentDescriptorPath,workerId:'actual-app-worker',output,scope:{projectId:project.id,sessionId},evidence:'actual Codex App host agent required; do not simulate result'};
  await note({...shared,stage:'waiting_for_agent'});console.log(JSON.stringify({stage:'waiting_for_agent',coordination,output}));
  await until('actual_agent_attached',async()=>(await api('/connection')).body.verified===true,240000);
  await nav('sessions');await page.locator('.session-list .records button').filter({hasText:'Actual Codex App agent'}).click();await page.locator('.composer').waitFor();
  await page.locator('.composer select').first().selectOption('discussion');await page.locator('.composer').getByRole('button',{name:appLabel('ru','connect'),exact:true}).click();
  const state=async()=>(await api(`/runtime/state?${new URLSearchParams(shared.scope)}`)).body;
  await until('app_binding_ready',async()=>(await state()).canSend===true);
  const nonce=randomUUID();const prompt=`Synthetic PAOS bridge verification. Do not access files, network, or other tasks. Sort the numbers 17, 4, 9 in ascending order and calculate their sum. Return exactly one final line: TOKEN=${nonce}; ORDER=<comma-separated ascending numbers>; SUM=<sum>. No reasoning or extra text.`;
  await page.locator('.composer textarea').fill(prompt);await until('send_enabled',()=>page.getByRole('button',{name:uiLabel('ru','action.send'),exact:true}).isEnabled());
  await page.getByRole('button',{name:uiLabel('ru','action.send'),exact:true}).click();await until('durable_job_queued',async()=>(await state()).state==='queued');
  await note({...shared,stage:'job_queued',runId:(await state()).runId});console.log(JSON.stringify({stage:'job_queued'}));
  await until('actual_agent_result_persisted',async()=>{const value=await state();if(value.state==='recovery_required')throw new Error('actual_agent_lease_lost');return value.state==='completed';},240000);
  const messages=(await api(`/projects/${project.id}/entities?kind=message&parentId=${sessionId}`)).body.items;
  const answer=messages.find((message:any)=>message.data?.role==='assistant')?.body??'';
  check('actual_agent_answer_correlated',answer===`TOKEN=${nonce}; ORDER=4,9,17; SUM=30`);
  await until('result_visible_in_browser',async()=>(await page.locator('.transcript').innerText()).includes(answer));
  check('execution_explicitly_blocked',(await api('/runtime/bindings',{...shared.scope,mode:'execution'})).status!==200);
  check('native_sandbox_not_claimed',(await state()).capabilities.nativeSandbox===false);
  check('no_browser_errors',report.pageErrorCount===0);check('no_external_browser_requests',report.blockedExternalRequests===0);
  report.actualAppAgent=true;report.actualAgentExecution='host collaboration worker through capability-authenticated pull/claim/report';report.answer=answer;report.hostWorker='actual-app-worker';
  const screenshot=join(output,'actual-app-agent-result.png');await page.screenshot({path:screenshot,fullPage:true});report.screenshots.push(screenshot);
  await note({...shared,stage:'completed'});
 }catch(error){report.error=String((error as Error).message);process.exitCode=1;}
 finally{if(context)await context.close();if(service){await service.quit();report.serviceClosed=true;}
  // This runner owns exactly its mkdtemp root; keep only the redacted receipt and screenshot.
  await rm(root,{recursive:true,force:true});report.fixtureCleaned=true;report.finishedAt=new Date().toISOString();await writeFile(join(output,'app-agent-result.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({output,passed:report.checks.filter((item:any)=>item.passed).length,failed:report.checks.filter((item:any)=>!item.passed).length,error:report.error??null}));}
}
main().catch(()=>{console.error('APP_AGENT_ACCEPTANCE_FAILED');process.exitCode=1;});
