import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,readFile,readdir,rm,rename} from 'node:fs/promises';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {inventoryForProject} from '../../apps/local-service/src/code-index/sources.mts';
import {createProjectAnalysis} from '../../apps/local-service/src/project-analysis/service.mts';

async function fixture(t:any){
 const root=await mkdtemp(join(tmpdir(),'paos-analysis-test-')),workspace=join(root,'workspace');await mkdir(workspace);
 const files:Record<string,string>={'package.json':'{"name":"synthetic","scripts":{"prepare":"DO_NOT_EXECUTE"}}','src/main.ts':'export const ordinary=1;','schema/schema.prisma':'model Account { id Int @id }','migrations/001.sql':'CREATE TABLE account (id INTEGER);','AGENTS.md':'Synthetic local instructions.','config.py':'raise RuntimeError("never execute target")','sitecustomize.py':'raise RuntimeError("never import target")','state.sqlite':'not a database','secret.env':'DEMO_SECRET=synthetic-do-not-copy'};
 for(const [path,text] of Object.entries(files)){await mkdir(join(workspace,path,'..'),{recursive:true});await writeFile(join(workspace,path),text);}
 const binding=await bindProject('p',workspace),store=await openLocalStore({databasePath:join(root,'profile.sqlite')});
 await store.registerProject({id:'p',keyPrefix:'PAOS',canonicalRoot:binding.workspaceRoot,rootIdentity:binding.directoryIdentity,authorityMode:'sql'});
 t.after(async()=>{await store.close();await rm(root,{recursive:true,force:true});});
 const controller=new AbortController();let publish=true;
 const project=(await store.project('p'))!,inventory=await inventoryForProject(project).snapshot(project);
 const context={project,inventory,signal:controller.signal,publicationGuard:async()=>{if(!publish)throw Object.assign(Error('ANALYSIS_CANCELLED'),{code:'ANALYSIS_CANCELLED'});},canPublish:()=>publish,onProgress:async(_completed:number,_total:number)=>{}};
 return {root,workspace,store,files,context,controller,revoke:()=>{publish=false;},service:(options:any={})=>createProjectAnalysis({store,...options}),bridge:async(text:string)=>{const path=join(root,'fixture-bridge.py');await writeFile(path,text);return path;}};
}
const analysis=(result:any)=>result.data.analysis;

test('real isolated Python discovery retains source references, schema candidates and target bytes',async t=>{
 const f=await fixture(t),before=await readdir(tmpdir()),service=f.service();const result=await service.analyze(f.context),view=analysis(result);
 assert.equal(result.state,'partial');assert.equal(view.availability,'available');assert.ok(view.stack.some((entry:any)=>entry.name==='node'&&entry.sources[0].path==='package.json'));
 assert.ok(view.languages.some((entry:any)=>entry.name==='TypeScript'));assert.ok(view.schemaCandidates.some((entry:any)=>entry.kind==='orm'));assert.ok(view.schemaCandidates.some((entry:any)=>entry.kind==='database_file'&&entry.opened===false));
 assert.equal(view.controlPlane.find((entry:any)=>entry.path==='AGENTS.md').status,'present_unverified');assert.equal(view.database.available,false);assert.equal(view.inventoryRevision,f.context.inventory.revision);assert.equal(view.stale,false);
 assert.match(view.adapterSourceRevision,/^[a-f0-9]{64}$/);assert.match(view.runtime.pythonVersion,/^3\.\d+\.\d+$/);assert.equal(view.runtime.coreModule,'product_agent_os.discovery.analyze_workspace');assert.equal(view.runtime.deployment,'checkout_projection');
 assert.equal(await service.currentRevision(),view.adapterSourceRevision);
 for(const [path,text] of Object.entries(f.files))assert.equal(await readFile(join(f.workspace,path),'utf8'),text);
 assert.ok(!JSON.stringify(view).includes(f.workspace));assert.ok(!JSON.stringify(view).includes('synthetic-do-not-copy'));assert.deepEqual((await readdir(tmpdir())).filter(name=>name.startsWith('paos-analysis-')&&!before.includes(name)),[]);
});

test('missing core and Python are unavailable without installation or synthetic completion',async t=>{
 const f=await fixture(t);for(const runtime of [{coreScripts:join(f.root,'missing')},{pythonExecutable:join(f.root,'missing-python.exe')}]){const view=analysis(await f.service({runtime}).analyze(f.context));assert.equal(view.availability,'unavailable');assert.ok(view.limitations.some((reason:string)=>/UNAVAILABLE/.test(reason)));}
});

test('bounded projection excludes sensitive marker content without asserting absent control plane',async t=>{
 const f=await fixture(t);await writeFile(join(f.workspace,'AGENTS.md'),'api_key = "sk-proj-abcdefghijklmnopqrstuvwxyz0123456789"');f.context.inventory=await inventoryForProject(f.context.project).snapshot(f.context.project);
 const view=analysis(await f.service({limits:{files:2}}).analyze(f.context));assert.equal(view.availability,'available');assert.ok(view.projection.omitted>0);assert.equal(view.controlPlane.find((entry:any)=>entry.path==='AGENTS.md').status,'not_observed');assert.ok(!JSON.stringify(view).includes('sk-proj-'));
});

test('root replacement and source drift reject publication',async t=>{
 const f=await fixture(t);await writeFile(join(f.workspace,'src/main.ts'),'export const changed=2;');await assert.rejects(f.service().analyze(f.context),{code:'ANALYSIS_SOURCE_STALE'});
 await rename(f.workspace,join(f.root,'old'));await mkdir(f.workspace);await assert.rejects(f.service().analyze(f.context));
});

test('policy drift and revoked publication reject results',async t=>{
 const f=await fixture(t),project=f.context.project;
 // Constructor context is an immutable old attempt; registry policy mutation is simulated at its public store boundary.
 const original=f.store.project;f.store.project=async id=>id==='p'?{...project,inventoryPolicy:{exclude:['src/**']}}:original(id);
 await assert.rejects(f.service().analyze(f.context),{code:'ANALYSIS_POLICY_STALE'});f.store.project=original;f.revoke();await assert.rejects(f.service().analyze(f.context),{code:'ANALYSIS_CANCELLED'});
});

test('core plugin component retains its actual relative manifest source',async t=>{
 const f=await fixture(t);await mkdir(join(f.workspace,'packages','sample','.codex-plugin'),{recursive:true});await writeFile(join(f.workspace,'packages','sample','.codex-plugin','plugin.json'),'{"name":"synthetic-plugin","version":"1.0.0"}');f.context.inventory=await inventoryForProject(f.context.project).snapshot(f.context.project);
 const view=analysis(await f.service().analyze(f.context));assert.ok(view.components.some((component:any)=>component.sources.some((source:any)=>source.path==='packages/sample/.codex-plugin/plugin.json')));
});

test('timeout, excessive output and malformed Python output are explicit and cleaned',async t=>{
 const f=await fixture(t);
 for(const [text,limits,reason] of [
  ['import time\ntime.sleep(5)',{milliseconds:200},'ANALYSIS_TIMEOUT'],
  ['print("x" * 10000)',{outputBytes:128},'ANALYSIS_OUTPUT_LIMIT'],
  ['print("not-json")',{},'ANALYSIS_OUTPUT_INVALID'],
  ['raise RuntimeError("private absolute traceback")',{},'ANALYSIS_CORE_FAILED'],
 ] as const){const bridgePath=await f.bridge(text);const view=analysis(await f.service({runtime:{bridgePath},limits}).analyze(f.context));assert.equal(view.availability,'unavailable');assert.ok(view.limitations.includes(reason),JSON.stringify(view.limitations));assert.ok(!JSON.stringify(view).includes('traceback'));}
});

test('abort while Python is running rejects late output and removes its projection',async t=>{
 const f=await fixture(t),bridgePath=await f.bridge('import time\ntime.sleep(5)');f.context.onProgress=async()=>{setTimeout(()=>f.controller.abort(),50);};
 await assert.rejects(f.service({runtime:{bridgePath}}).analyze(f.context),{code:'ANALYSIS_CANCELLED'});
});

test('source changes during Python work cannot publish mixed revisions',async t=>{
 const f=await fixture(t),bridgePath=await f.bridge('import time,json\ntime.sleep(.2)\nprint(json.dumps({"schemaVersion":"paos_analysis_bridge_v1","pythonVersion":"3.13.5","stack":[],"controlPlane":[],"components":[]}))');
 f.context.onProgress=async completed=>{if(!completed)await writeFile(join(f.workspace,'src/main.ts'),'export const changedDuringChild=3;');};
 await assert.rejects(f.service({runtime:{bridgePath}}).analyze(f.context),{code:'ANALYSIS_SOURCE_STALE'});
});
