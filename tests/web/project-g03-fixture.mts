import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,rm} from 'node:fs/promises';
import {join,resolve,dirname,basename} from 'node:path';
import {tmpdir} from 'node:os';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {createLocalApplication,type ApplicationOptions} from '../../apps/local-service/src/http/application.mts';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';

export async function g03Fixture(t:{after(callback:()=>Promise<void>):void},extra:Partial<ApplicationOptions>={}){
 const scratch=resolve(tmpdir()),root=await mkdtemp(join(scratch,'paos-g03-')),workspace=join(root,'workspace'),profile=join(root,'profile');
 await mkdir(workspace);await mkdir(profile);await writeFile(join(workspace,'main.ts'),'export const visible=1;\n');
 const store=await openLocalStore({databasePath:join(profile,'state.sqlite')}),binding=await bindProject('p',workspace);
 await store.registerProject({id:'p',keyPrefix:'TEST',canonicalRoot:binding.workspaceRoot,rootIdentity:binding.directoryIdentity,authorityMode:'sql',displayName:'Synthetic project'});
 const origin='http://127.0.0.1:43210',options={store,origin,instanceId:'func-g03',profileDirectory:profile,...extra};
 let app=await createLocalApplication(options),cookie='',csrf='';
 async function pair(){const result=await app.handleRequest(new Request(origin+'/bootstrap/exchange',{method:'POST',headers:{host:new URL(origin).host,origin,'content-type':'application/json'},body:JSON.stringify({code:app.issuePairingCode()})}));cookie=result.headers.get('set-cookie')!.split(';')[0];csrf=(await result.json()).csrfToken;}
 await pair();
 t.after(async()=>{await (app as any).close?.();await store.close();assert.equal(dirname(resolve(root)),scratch);assert.ok(basename(root).startsWith('paos-g03-'));await rm(root,{recursive:true,force:true});});
 return {root,workspace,profile,store,get app(){return app;},
  async request(path:string,input?:unknown,headers:Record<string,string>={}){return app.handleRequest(new Request(origin+'/api/v1'+path,{method:input===undefined?'GET':'POST',headers:{host:new URL(origin).host,origin,cookie,'x-paos-csrf':csrf,'content-type':'application/json',...headers},...(input===undefined?{}:{body:JSON.stringify(input)})}));},
  async restart(){await (app as any).close?.();app=await createLocalApplication(options);await pair();}
 };
}

export async function until<T>(load:()=>Promise<T>,done:(value:T)=>boolean,milliseconds=10000){const deadline=Date.now()+milliseconds;for(;;){const value=await load();if(done(value))return value;if(Date.now()>deadline)throw Error('OBSERVABLE_CONDITION_TIMEOUT');await new Promise(resolve=>setTimeout(resolve,20));}}
