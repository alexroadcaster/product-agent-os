import {test} from 'node:test';
import assert from 'node:assert/strict';
import {sanitizeModuleResolverConfig,resolveIndexedModule} from '../../apps/local-service/src/code-index/module-resolver.mts';
test('bounded pure resolver maps relative, baseUrl and alias literals only to admitted indexed paths',()=>{
 const sanitized=sanitizeModuleResolverConfig({baseUrl:'.',paths:{'@app/*':['src/*']}});assert.deepEqual(sanitized.configReasons,[]);
 const admitted=['src/main.ts','src/lib.ts','src/model.ts','src/имя с пробелом.ts'];
 assert.deepEqual(resolveIndexedModule('src/main.ts','./lib',admitted,sanitized.resolverConfig),{state:'resolved',relativePath:'src/lib.ts'});
 assert.deepEqual(resolveIndexedModule('src/main.ts','@app/model',admitted,sanitized.resolverConfig),{state:'resolved',relativePath:'src/model.ts'});
 assert.deepEqual(resolveIndexedModule('src/main.ts','src/имя с пробелом',admitted,sanitized.resolverConfig),{state:'resolved',relativePath:'src/имя с пробелом.ts'});
 assert.equal(resolveIndexedModule('src/main.ts','@app/private',admitted,sanitized.resolverConfig).state,'unresolved');
});

import {Worker} from 'node:worker_threads';
import {readFile} from 'node:fs/promises';
const parserWorker=new URL('../../apps/local-service/src/code-index/parser-worker.mts',import.meta.url);
async function parseFiles(files:Array<{relativePath:string;text:string;language:string}>,resolverConfig?:unknown,configReasons:string[]=[]):Promise<any>{
 return new Promise((accept,reject)=>{const worker=new Worker(parserWorker,{workerData:{files,resolverConfig,configReasons},resourceLimits:{maxOldGenerationSizeMb:128}}),timer=setTimeout(()=>{void worker.terminate();reject(Error('test_parser_timeout'));},10000);worker.once('message',result=>{clearTimeout(timer);accept(result);});worker.once('error',error=>{clearTimeout(timer);reject(error);});});
}
test('production parser Worker resolves all ten committed G02 corpus imports without inventing cross-file calls',async()=>{
 const corpus=JSON.parse(await readFile('tests/fixtures/func_g02/corpus.json','utf8')),files=Object.entries(corpus.files).filter(([path])=>/\.(?:[cm]?js|[cm]?ts|tsx|jsx)$/.test(path)).map(([relativePath,text])=>({relativePath,text:text as string,language:relativePath.endsWith('.ts')?'ts':'js'}));
 const config=JSON.parse(corpus.files['tsconfig.json']).compilerOptions,result=await parseFiles(files,config);assert.ok(!result.error);
 const nodes=result.results.flatMap((r:any)=>r.nodes??[]),byId=new Map(nodes.map((n:any)=>[n.id,n])),edges=result.results.flatMap((r:any)=>r.edges??[]);
 const resolved=edges.filter((e:any)=>e.type==='import'&&e.resolution==='lexical').map((e:any)=>[(byId.get(e.from) as any).relativePath,(byId.get(e.to) as any).relativePath]);
 assert.deepEqual(resolved.map((v:any)=>JSON.stringify(v)).sort(),corpus.expectedImports.map((v:any)=>JSON.stringify(v)).sort());
 assert.ok(!edges.some((e:any)=>e.type==='call'&&(byId.get(e.to) as any)?.kind==='file'));
 const missing=edges.filter((e:any)=>e.type==='import'&&e.resolution==='unresolved');assert.equal(missing.length,1);assert.equal((byId.get(missing[0].to) as any).reason,'module_not_resolved');
});

import {createCodeIndex} from '../../apps/local-service/src/code-index/service.mts';
import {m2Fixture} from './m2-fixture.mts';
import {mkdir,writeFile,lstat} from 'node:fs/promises';
import {join,dirname} from 'node:path';
test('production createCodeIndex wires checked root tsconfig aliases and detects changed/hostile config without execution',async t=>{
 const f=await m2Fixture(t),corpus=JSON.parse(await readFile('tests/fixtures/func_g02/corpus.json','utf8'));
 for(const [path,text] of Object.entries(corpus.files)){await mkdir(dirname(join(f.root,path)),{recursive:true});await writeFile(join(f.root,path),text as string);}
 await writeFile(join(f.root,'.dependency-cruiser.cjs'),"require('node:fs').writeFileSync('CONFIG_EXECUTED','unsafe');module.exports={};");
 const index=createCodeIndex(f.store),built=await index.rebuild('p'),nodes=new Map<string,any>(),edges=new Map<string,any>();let cursor:string|null=null;
 do{const page=await index.graph('p',new URLSearchParams({revision:built.revision!,mode:'dependencies',limit:'100',...(cursor?{cursor}:{})}));for(const node of [...page.nodes,...page.contextNodes])nodes.set(node.id,node);for(const edge of page.edges)edges.set(edge.id,edge);cursor=page.nextCursor;}while(cursor);
 const resolved=[...edges.values()].filter(e=>e.type==='import'&&e.resolution==='lexical').map(e=>JSON.stringify([nodes.get(e.from).relativePath,nodes.get(e.to).relativePath]));assert.deepEqual(resolved.sort(),corpus.expectedImports.map((v:any)=>JSON.stringify(v)).sort());
 await writeFile(join(f.root,'tsconfig.json'),JSON.stringify({extends:'.dependency-cruiser.cjs',compilerOptions:{baseUrl:'..',paths:{'@app/*':['../outside/*']}}}));assert.equal((await index.status('p')).state,'stale');const unsupported=await index.rebuild('p');assert.notEqual(unsupported.revision,built.revision);assert.ok(unsupported.limitations.includes('resolver_config_unavailable_or_unsupported'));await assert.rejects(lstat(join(f.root,'CONFIG_EXECUTED')),{code:'ENOENT'});
});
test('ambient require respects parameter, function, import, catch, block and hoisted var bindings; dynamic inputs stay unresolved',async()=>{
 const files=[
  {relativePath:'dep.ts',language:'ts',text:'export const value=1;'},
  {relativePath:'entry.ts',language:'ts',text:"const a=require('./dep'); function param(require){require('./dep');} function named(){require('./dep'); function require(){}} function hoisted(){require('./dep'); if(false){var require;}} try{}catch(require){require('./dep');} {let require;require('./dep');} require(input); import(input); import(`./dep`); module.require('./dep');"},
  {relativePath:'imported.ts',language:'ts',text:"import require from './dep'; require('./dep');"},
  {relativePath:'module-var.ts',language:'ts',text:"require('./dep'); if(false){var require;}"}
 ];
 const result=await parseFiles(files),all=result.results.flatMap((r:any)=>r.edges??[]),nodes=new Map(result.results.flatMap((r:any)=>r.nodes??[]).map((n:any)=>[n.id,n]));
 const imports=all.filter((e:any)=>e.type==='import'&&e.resolution==='lexical');assert.equal(imports.length,2);assert.deepEqual(imports.map((e:any)=>(nodes.get(e.from) as any).relativePath).sort(),['entry.ts','imported.ts']);
 const reasons=result.results.flatMap((r:any)=>r.nodes??[]).map((n:any)=>n.reason);assert.equal(reasons.filter((r:string)=>r==='dynamic_require').length,1);assert.equal(reasons.filter((r:string)=>r==='dynamic_import').length,2);
 assert.ok(!all.some((e:any)=>e.type==='call'&&(nodes.get(e.to) as any)?.kind==='file'));
});
test('resolver reports ambiguity and invalid/hostile metadata without widening the allowlist or invoking accessors',async()=>{
 const admitted=['src/entry.ts','src/x.ts','src/x.js','fallback/x.ts','src/space name.ts'];assert.deepEqual(resolveIndexedModule('src/entry.ts','./x',admitted),{state:'unresolved',reason:'ambiguous_module'});
 assert.deepEqual(resolveIndexedModule('src/entry.ts','../../outside',admitted),{state:'unresolved',reason:'module_outside_root'});
 assert.equal(resolveIndexedModule('src/entry.ts','@p/x',admitted,{paths:{'@p/*':['src/*','fallback/*']}}).state,'unresolved');
 for(const config of [{baseUrl:'../outside'},{baseUrl:'C:\\outside'},{extends:'../shared.json'},{references:[{path:'../other'}]},{paths:{'@x/*':['../../secret']}},{paths:{'@x/**':['src/*']}},{paths:{'@x':['src/*']}},{paths:{alias:Array(9).fill('src/x')}},{paths:Object.fromEntries(Array.from({length:65},(_,i)=>['@'+i,['src/x']]))}]){const safe=sanitizeModuleResolverConfig(config);assert.equal(safe.resolverConfig,undefined);assert.deepEqual(safe.configReasons,['resolver_config_unsupported']);}
 let executed=false;const accessor=Object.defineProperty({},'baseUrl',{get(){executed=true;return '..';},enumerable:true});assert.equal(sanitizeModuleResolverConfig(accessor).resolverConfig,undefined);assert.equal(executed,false);
 const invalid=await parseFiles([{relativePath:'entry.ts',language:'ts',text:"import './dep';import '@p/dep';"},{relativePath:'dep.ts',language:'ts',text:'export const x=1;'}],{baseUrl:'..'},['root_config_diagnostic']);assert.deepEqual(invalid.configReasons,['root_config_diagnostic','resolver_config_unsupported']);assert.equal(invalid.results.flatMap((r:any)=>r.edges??[]).filter((e:any)=>e.type==='import'&&e.resolution==='lexical').length,1);
});

test('TypeScript constructor parameter properties shadow ambient require',async()=>{
 const result=await parseFiles([{relativePath:'entry.ts',language:'ts',text:"class Loader { constructor(public require:(s:string)=>unknown) { require('./dep'); } }"},{relativePath:'dep.ts',language:'ts',text:'export const value=1;'}]);
 assert.equal(result.results.flatMap((r:any)=>r.edges??[]).filter((e:any)=>e.type==='import').length,0);
});

test('F14 observes TypeScript import-type, re-export and literal dynamic edges',async()=>{
 const result=await parseFiles([
  {relativePath:'page.tsx',language:'tsx',text:"export type T=import('./dep').T;\nexport {value} from './dep';\nconst load=()=>import('./dep');"},
  {relativePath:'dep.ts',language:'ts',text:"export type T=string;export const value=1;"},
 ]);
 const edges=result.results.find((row:any)=>row.relativePath==='page.tsx').edges;
 assert.deepEqual(edges.filter((edge:any)=>edge.type==='import'&&edge.resolution==='lexical').map((edge:any)=>edge.anchor.line),[1,2,3]);
});

test('local JSON inheritance resolves aliases relative to their defining config and invalidates on drift',async t=>{
 const f=await m2Fixture(t);
 for(const [file,text] of Object.entries({
  'tsconfig.json':'{"extends":"./config/base.json"}',
  'config/base.json':'{"compilerOptions":{"paths":{"@domain/*":["domain/*"]}}}',
  'config/domain/model.ts':'export type Model=number;',
  'page.tsx':"export type View=import('@domain/model').Model;",
 })){await mkdir(dirname(join(f.root,file)),{recursive:true});await writeFile(join(f.root,file),text);}
 const index=createCodeIndex(f.store);
 const observed=await index.rebuild('p');
 const evidence=await index.architectureEvidence('p',observed.revision!);
 assert.ok(evidence.imports.some(edge=>edge.from==='page.tsx'&&edge.to==='config/domain/model.ts'));
 await writeFile(join(f.root,'config/base.json'),'{"extends":"./base.json"}');
 await assert.rejects(index.architectureEvidence('p',observed.revision!),{code:'GRAPH_SOURCE_STALE'});
 const bad=await index.rebuild('p');
 const partial=await index.architectureEvidence('p',bad.revision!);
 assert.ok(partial.limitations.includes('resolver_config_unavailable_or_unsupported'));
 assert.ok(partial.imports.some(edge=>edge.from==='page.tsx'&&edge.to===null));
});
