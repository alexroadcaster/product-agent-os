import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {mkdtemp,mkdir,readFile,readdir,realpath,rm,symlink,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {tmpdir} from 'node:os';
import {basename,dirname,join,relative,resolve} from 'node:path';
import test,{type TestContext} from 'node:test';
import {compositionFindings,planJourney} from '../../tools/project-methodology/design.mts';
import {newBoundaryViolations} from '../../tools/project-methodology/architecture.mts';

const cli=resolve('tools/project-methodology.mts');
async function project(t:TestContext,files:Record<string,string>,linked=false){
 const temp=await realpath(tmpdir()),root=await mkdtemp(join(temp,'paos-b3-test-')),workspace=join(root,'workspace');
 t.after(async()=>{const actual=await realpath(root);assert.equal(dirname(actual),temp);assert.ok(basename(actual).startsWith('paos-b3-test-'));await rm(actual,{recursive:true});});
 await mkdir(workspace);
 for(const [name,content] of Object.entries(files)){
  const target=join(workspace,name);await mkdir(dirname(target),{recursive:true});await writeFile(target,content);
 }
 if(linked){
  const external=join(root,'external');await mkdir(external);
  await writeFile(join(external,'private.ts'),'export const secretFixture=1;');
  await symlink(external,join(workspace,'linked'),process.platform==='win32'?'junction':'dir');
 }
 async function snapshot(){
  const entries=await readdir(workspace,{recursive:true,withFileTypes:true});
  return Object.fromEntries(await Promise.all(entries.filter(entry=>entry.isFile()).map(async entry=>{
   const path=join(entry.parentPath,entry.name);
   return [relative(workspace,path),createHash('sha256').update(await readFile(path)).digest('hex')];
  })));
 }
 const before=await snapshot();
 return {async baseline(file:string){
  const old=spawnSync('python',['-B',resolve('plugins/product-agent-os/scripts/run_codex_runtime_runner.py'),
   workspace,'--contract','--task','Review the selected frontend page','--change-mode','configuration',
   '--changed-path',file,'--acceptance','Review the current page boundary','--risk-level','low'],{encoding:'utf8',timeout:20_000});
  assert.ok([0,1].includes(old.status??-1),old.stderr);
  const selection=JSON.parse(old.stdout).route_packet.methodology_decision.decisions.find((item:any)=>item.method==='fsd');
  assert.deepEqual(await snapshot(),before);
  return selection;
 },async run(kind:string,input:unknown,...flags:string[]){
  const file=join(root,'input.json');await writeFile(file,JSON.stringify(input));
  const done=spawnSync(process.execPath,[cli,kind,workspace,file,...flags],{encoding:'utf8',timeout:30_000});
  assert.equal(done.status,0,done.stderr);
  assert.deepEqual(await snapshot(),before);
  return JSON.parse(done.stdout);
 }};
}
const page={path:'src/pages/orders.tsx',owner:'orders'};
const layers=[
 {root:'src/pages',layer:'pages',owner:'orders'},
 {root:'src/features/checkout',layer:'features',owner:'checkout',publicApi:'src/features/checkout/index.ts'},
 {root:'src/entities/order',layer:'entities',owner:'domain',publicApi:'src/entities/order/index.ts'},
 {root:'src/entities/customer',layer:'entities',owner:'customer',publicApi:'src/entities/customer/index.ts'},
];
const scoped={surface:'frontend',pages:[page],boundaries:layers,changeFrequency:'frequent',migrationCost:'medium',exceptions:[]};

test('static, modular and coupled frontend profiles receive different source-bound advice',async t=>{
 const small=await project(t,{'index.html':'<!doctype html><main>Local page</main>','features/unrelated.ts':'export const count=1;'});
 const staticBaseline=await small.baseline('index.html');
 const localized=await small.run('architecture',{...scoped,pages:[{path:'index.html',owner:'site'}],boundaries:[],changeFrequency:'occasional'});
 assert.equal(localized.recommendation,'retain_architecture');
 assert.equal(localized.migration,null);
 const modular=await project(t,{
  [page.path]:"import {show} from '../features/checkout'; export const route=show;",
  'src/features/checkout/index.ts':"export {show} from '../../entities/order';",
  'src/entities/order/index.ts':"export {customer as show} from '../customer/@x/order';",
  'src/entities/customer/index.ts':'export const customer=1;',
  'src/entities/customer/@x/order.ts':"export {customer} from '../index';",
 });
 const modularBaseline=await modular.baseline(page.path);
 const registered=[...layers.slice(0,-1),{...layers.at(-1),crossApi:[{
  consumer:'src/entities/order',entry:'src/entities/customer/@x/order.ts',
 }]}];
 const current=await modular.run('architecture',{...scoped,boundaries:registered});
 assert.equal(current.coverage,'observed');
 assert.equal(current.recommendation,'retain_modular_boundaries');
 assert.deepEqual(current.findings,[]);
 assert.equal(current.migration,null);
 const unregistered=await modular.run('architecture',scoped);
 assert.ok(unregistered.findings.some((item:any)=>item.rule==='cross_slice_import'));

 const coupled=await project(t,{
  [page.path]:"export {show as route} from '../features/checkout/internal';",
  'src/pages/help.ts':'export const help = 1;',
  'src/features/checkout/index.ts':"export {show} from './internal';",
  'src/features/checkout/internal.ts':"import {order} from '../../entities/order'; export const show=order;",
  'src/entities/order/index.ts':"import {show} from '../../features/checkout/internal'; export const order=show;",
  'src/entities/customer/index.ts':'export const customer=1;',
 });
 const coupledBaseline=await coupled.baseline(page.path);
 assert.equal(staticBaseline.applicability,'not_applicable');
 assert.deepEqual(coupledBaseline,modularBaseline);
 const proposed=await coupled.run('architecture',scoped);
 assert.equal(proposed.recommendation,'gradual_fsd');
 assert.equal(proposed.authority,'read_only');
 assert.ok(proposed.findings.some((item:any)=>item.rule==='private_entry'&&item.from===page.path&&item.line===1&&item.owner==='orders'));
 assert.ok(proposed.findings.some((item:any)=>item.rule==='layer_direction'));
 assert.ok(proposed.findings.some((item:any)=>item.rule==='import_cycle'));
 assert.equal(proposed.migration.firstPage,page.path);
 assert.equal(proposed.migration.ownerDecisionRequired,true);
 assert.ok(proposed.migration.baselineImports.length);
 assert.equal(proposed.migration.checkpoints[1].dependsOn,'page_boundary acceptance');
 const unrelated=await coupled.run('architecture',{...scoped,pages:[{path:'src/pages/help.ts',owner:'support'}]});
 assert.equal(unrelated.recommendation,'strengthen_boundaries');
 assert.equal(unrelated.migration,null);
 const {line:_,...exception}=proposed.findings.find((item:any)=>item.rule==='private_entry');
 const retained=await coupled.run('architecture',{...scoped,exceptions:[{...exception,reason:'Compatibility bridge'}],migrationCost:'high'});
 assert.equal(retained.recommendation,'strengthen_boundaries');
 assert.equal(retained.legacyExceptions.length,1);
 assert.equal(retained.migration,null);
 const baseline=proposed.findings[0];
 assert.deepEqual(newBoundaryViolations([baseline],[{...baseline,line:80}]),[]);
 assert.deepEqual(newBoundaryViolations([baseline],[baseline,baseline]),[baseline]);
});

test('partial and non-frontend scopes never yield a migration proposal',async t=>{
 const partial=await project(t,{
  [page.path]:"export const load=()=>import('@unknown/module'); const x=()=>import(name);",
  'src/code.ts':"import legacy = require('./hidden'); import '../../outside'; export const data=legacy;",
  'src/app.vue':'<template><p>Unsupported</p></template>',
  'tsconfig.json':'{"extends":"outside-package"}',
 },true);
 const input={...scoped,boundaries:[layers[0]]};
 const unresolved=await partial.run('architecture',input);
 assert.equal(unresolved.coverage,'partial');
 assert.equal(unresolved.recommendation,'inspect_coverage');
 assert.ok(unresolved.gaps.some((item:any)=>item.reason==='UNSUPPORTED_CONFIG'));
 assert.ok(unresolved.gaps.some((item:any)=>item.reason==='dynamic_import'));
 assert.ok(unresolved.gaps.some((item:any)=>item.reason==='unsupported_import_equals'));
 assert.ok(unresolved.gaps.some((item:any)=>item.reason==='module_outside_root'));
 assert.ok(unresolved.gaps.some((item:any)=>item.reason==='language_not_supported'));
 assert.ok(unresolved.gaps.some((item:any)=>item.reason==='linked_source'));
 assert.equal(unresolved.migration,null);
 const withoutGraph=await partial.run('architecture',input,'--without-f14');
 assert.ok(withoutGraph.gaps.some((item:any)=>item.reason==='F14_ADAPTER_UNAVAILABLE'));
 for(const [surface,file,recommendation] of [['backend','main.py','backend_boundary_policy'],['native','App.swift','native_boundary_policy']]){
  const native=await project(t,{[file]:'// synthetic'});
  const outcome=await native.run('architecture',{...scoped,surface,pages:[],boundaries:[]});
  assert.equal(outcome.coverage,'not_applicable');
  assert.equal(outcome.recommendation,recommendation);
  assert.equal(outcome.observed.surfaceSignals,1);
 }
});

test('design CLI preserves existing references, proposes missing states and exposes unauthorized or stale checks',async t=>{
 const data=JSON.parse(await readFile(new URL('../fixtures/product_agent_os/pmeth-b3-design.json',import.meta.url),'utf8'));
 const target=await project(t,{[data.designRefs[0]]:'.panel { display:block; }'});
 const proposed=await target.run('design',data);
 assert.equal(proposed.status,'proposed');
 assert.ok(proposed.checks.every((item:any)=>item.status==='planned'));
 assert.equal(proposed.humanAcceptance,'not_observed');
 const partial=planJourney({...data,sourceRevision:proposed.sourceRevision,extent:'substantial',apiEvidence:'unavailable',
  stateMatrix:{...data.stateMatrix,dirty:undefined,loading:{expected:'Candidate',source:'current'}},
  available:{...data.available,browserAuthorized:false}},new Set(data.designRefs)) as any;
 assert.ok(partial.gaps.includes('STATE_NOT_SPECIFIED:dirty'));
 assert.ok(partial.gaps.includes('API_EVIDENCE_INSUFFICIENT:loading'));
 assert.ok(partial.gaps.includes('HUMAN_OBSERVATION_REQUIRED'));
 assert.ok(partial.gaps.includes('CHECK_UNAVAILABLE:browser'));
 assert.equal(partial.stateMatrix[0].source,'unavailable');
 const stale=await target.run('design',{...data,sourceRevision:'1'.repeat(64)});
 assert.equal(stale.status,'stale');
 assert.equal((await target.run('design',{surface:'backend',taskId:'backend'})).status,'not_applicable');
});

test('reviewed composition detects a wrong order with unchanged overflow dimensions',()=>{
 const actual=[
  {name:'header',top:0,bottom:25,left:0,right:180},
  {name:'controls',top:30,bottom:80,left:0,right:180},
  {name:'result',top:90,bottom:160,left:0,right:180},
 ];
 assert.deepEqual(compositionFindings(['header','controls','result'],actual,200),[]);
 assert.deepEqual(compositionFindings(['header','result','controls'],actual,200),['REGION_ORDER_MISMATCH']);
});
