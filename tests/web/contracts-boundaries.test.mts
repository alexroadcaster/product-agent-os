import assert from 'node:assert/strict';
import {test} from 'node:test';
import {readFile,readdir} from 'node:fs/promises';
import {resolve,dirname,relative,join,posix} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire,isBuiltin} from 'node:module';
import {createIndexedModuleResolver,sanitizeModuleResolverConfig,type ModuleResolverConfig} from '../../apps/local-service/src/code-index/module-resolver.mts';
import {decodeM1TaskProfile,encodeM1TaskProfile} from '../../packages/contracts/tasks/decode-task-profile.ts';
import * as legacyDecoder from '../../apps/local-service/src/tasks/task-profile.ts';
import {loadUiPreferences,saveUiPreferences} from '../../packages/contracts/ui/preferences.ts';
import * as frontendPreferences from '../../apps/web/src/design/preferences.ts';

const root=fileURLToPath(new URL('../../',import.meta.url));
const require=createRequire(new URL('../../apps/web/package.json',import.meta.url));
const parser=await import(pathToFileURL(require.resolve('rolldown/utils')).href);

test('legacy decoder and frontend preferences re-export their single shared implementation',()=>{
 assert.equal(legacyDecoder.decodeM1TaskProfile,decodeM1TaskProfile);
 assert.equal(legacyDecoder.encodeM1TaskProfile,encodeM1TaskProfile);
 assert.equal(frontendPreferences.loadUiPreferences,loadUiPreferences);
 assert.equal(frontendPreferences.saveUiPreferences,saveUiPreferences);
});

/** Parse static module edges, including type imports, re-exports and literal dynamic imports. */
function moduleEdges(source:string,file='source.ts'){
 const parsed=parser.parseSync(file,source,{lang:file.endsWith('.tsx')?'tsx':'ts',astType:'ts'});
 const edges:(string|null)[]=[];
 assert.equal(parsed.errors.length,0,'boundary check must parse '+file);
 function visit(node:any){
  if(!node||typeof node!=='object')return;
  if(['ImportDeclaration','ExportNamedDeclaration','ExportAllDeclaration','TSImportType'].includes(node.type)&&typeof node.source?.value==='string')edges.push(node.source.value);
  if(node.type==='ImportExpression'){
   const source=node.source;
   edges.push(typeof source?.value==='string'?source.value:source?.type==='TemplateLiteral'&&!source.expressions.length?source.quasis[0].value.cooked:null);
  }
  if(node.type==='TSExternalModuleReference'&&typeof node.expression?.value==='string')edges.push(node.expression.value);
  if(node.type==='CallExpression'&&node.callee?.type==='Identifier'&&node.callee.name==='require')edges.push(typeof node.arguments[0]?.value==='string'?node.arguments[0].value:null);
  for(const child of Object.values(node))if(Array.isArray(child))child.forEach(visit);else if(child&&typeof child==='object')visit(child);
 }
 visit(parsed.program);return edges;
}
async function sources(directory:string):Promise<string[]>{
 const files:string[]=[];
 for(const entry of await readdir(directory,{withFileTypes:true})){
  const path=join(directory,entry.name);
  if(entry.isDirectory())files.push(...await sources(path));
  else if(entry.isFile()&&/\.(?:ts|tsx|mts)$/.test(entry.name))files.push(path);
 }
 return files;
}
test('import boundary parser includes type-only edges, re-exports and literal dynamic imports without matching comments',()=>{
 const code=`import type { A } from './a.ts'; export { b } from './b.ts'; const c=import('./c.ts'); type D=import('./d.ts').D; const e=require('./e.ts'); // import './comment.ts'`;
 assert.deepEqual(moduleEdges(code),['./a.ts','./b.ts','./c.ts','./d.ts','./e.ts']);
});
test('import boundary parser reads the module edges of a TSX component',()=>{
 const code=`import type { Props } from './types'; export type * from './public';
 const view = <section aria-label="test"/>; const load = () => import('./panel.mts');`;
 assert.deepEqual(moduleEdges(code,'Dashboard.tsx'),['./types','./public','./panel.mts']);
});
test('shared contracts never import applications, and the local service never imports frontend source',async()=>{
 const violations:string[]=[];
 for(const area of ['packages/contracts','apps/local-service/src'])for(const file of await sources(join(root,area))){
  for(const specifier of moduleEdges(await readFile(file,'utf8'),file)){
   if(!specifier?.startsWith('.'))continue;
   const target=relative(root,resolve(dirname(file),specifier)).replaceAll('\\','/');
   if(area==='packages/contracts'&&target.startsWith('apps/')||area==='apps/local-service/src'&&target.startsWith('apps/web/src/'))violations.push(relative(root,file)+' -> '+specifier);
  }
 }
 assert.deepEqual(violations,[],'application-independent contract ownership');
});

const webRoot='apps/web/src/';
const dashboard=webRoot+'features/dashboard/';
const tasks=webRoot+'features/tasks/';
const tasksReadApi=tasks+'read.ts';
const runUsage=webRoot+'features/usage/RunUsage.tsx';
const teamManager=webRoot+'features/team/TeamManager.tsx';
const app=webRoot+'ui/App.tsx';
const sharedPresentation=['MarkdownBody.tsx','markdown.ts','external-url.ts','MermaidView.tsx','NetworkView.tsx'].map(name=>webRoot+'ui/'+name);
const sharedUi=['CapabilityNotice.tsx','Icon.tsx','Modal.tsx','ProjectFreshness.tsx','MarkdownBody.tsx','external-url.ts'].map(name=>webRoot+'ui/'+name);
const inPilot=(file:string)=>file.startsWith(dashboard)||file.startsWith(tasks);
const relativePath=(path:string)=>relative(root,path).replaceAll('\\','/');
type Edge={from:string;to:string};

function boundaryRule({from,to}:Edge){
 if(sharedPresentation.includes(from)&&(to.startsWith(webRoot+'features/')||to===app))return 'shared view depends on feature';
 if(from===runUsage&&(to.startsWith(webRoot+'features/')||to===app))return 'usage depends on screen';
 const fromDashboard=from.startsWith(dashboard),toDashboard=to.startsWith(dashboard);
 const fromTasks=from.startsWith(tasks),toTasks=to.startsWith(tasks);
 if(!inPilot(from)&&!inPilot(to))return;
 if(fromDashboard&&toDashboard||fromTasks&&toTasks)return;
 if(from===app&&(to===dashboard+'Dashboard.tsx'||to===tasks+'TaskManager.tsx'))return;
 if((fromDashboard||from===teamManager)&&to===tasksReadApi)return;
 if((fromDashboard||fromTasks)&&to===runUsage)return;
 if(inPilot(from)&&to.startsWith(webRoot+'ui/')&&!sharedUi.includes(to))return 'upward import';
 if(fromTasks&&toDashboard)return 'upward import';
 if(inPilot(from)&&to.startsWith(webRoot+'features/')&&!toTasks)return 'cross-feature import';
 if((toDashboard||toTasks)&&!inPilot(from))return 'non-public consumer';
 if(fromDashboard&&toTasks)return 'deep Tasks import';
}

function hasPath(from:string,to:string,adjacency:Map<string,Set<string>>){
 const seen=new Set<string>();
 const pending=[from];
 for(const file of pending){
  if(file===to)return true;
  if(seen.has(file))continue;
  seen.add(file);
  pending.push(...adjacency.get(file)??[]);
 }
 return false;
}

function inspectWebImports(files:Map<string,string>,indexed:Iterable<string>,config:ModuleResolverConfig,external:(specifier:string)=>boolean){
 const resolveImport=createIndexedModuleResolver(indexed,config);
 const adjacency=new Map<string,Set<string>>();
 const diagnostics=new Set<string>();
 const rules=new Set<string>();
 for(const [from,source] of files){
  const targets=new Set<string>();
  adjacency.set(from,targets);
  for(const specifier of moduleEdges(source,from)){
   if(specifier===null){diagnostics.add(from+' [dynamic target]');continue;}
   const moduleName=specifier.replace(/\?url$/,'');
   const target=resolveImport(from,moduleName);
   if(target.state==='unresolved'){
    if(target.reason!=='module_not_resolved'||!external(moduleName))diagnostics.add(from+' -> '+specifier+' [resolution: '+target.reason+']');
    continue;
   }
   targets.add(target.relativePath);
   const rule=boundaryRule({from,to:target.relativePath});
   if(rule)rules.add(from+' -> '+target.relativePath+' ['+rule+']');
  }
 }
 for(const [from,targets] of adjacency){
  for(const to of targets){
   if((inPilot(from)||inPilot(to))&&hasPath(to,from,adjacency))rules.add(from+' -> '+to+' [cycle]');
  }
 }
 return {diagnostics:[...diagnostics].sort(),rules:[...rules].sort()};
}

test('frontend boundary distinguishes an alias resolving to a forbidden edge from resolution failure',()=>{
 const view=dashboard+'view.tsx',model=tasks+'model.mts',icon=webRoot+'ui/Icon.tsx';
 const files=new Map([[view,"import type { T } from '@fixture/tasks/model'; export { Icon } from '../../ui/Icon.tsx'; import('@missing/x'); import(target);"]]);
 const actual=inspectWebImports(files,[view,model,icon],{paths:{'@fixture/*':[webRoot+'features/*']}},()=>false);
 assert.deepEqual(actual.rules,[view+' -> '+model+' [deep Tasks import]']);
 assert.deepEqual(actual.diagnostics,[view+' -> @missing/x [resolution: module_not_resolved]',view+' [dynamic target]']);
});

test('frontend boundary detects a cycle through another module and admits an acyclic public entry',()=>{
 const view=dashboard+'Dashboard.tsx',helper=webRoot+'api/helper.ts',model=dashboard+'model.ts';
 const files=new Map([[app,"import '../features/dashboard/Dashboard.tsx';"],[view,"import '../../api/helper.ts';"],[helper,"export * from '../features/dashboard/model.ts';"],[model,"import './Dashboard.tsx';"]]);
 const actual=inspectWebImports(files,files.keys(),{},()=>false);
 assert.deepEqual(actual.diagnostics,[]);
 assert.deepEqual(actual.rules,[
  helper+' -> '+model+' [cycle]',
  helper+' -> '+model+' [non-public consumer]',
  view+' -> '+helper+' [cycle]',
  model+' -> '+view+' [cycle]',
 ]);
});

test('Tasks cannot reach App composition or peer screen internals',()=>{
 const manager=tasks+'TaskManager.tsx',team=webRoot+'features/team/TeamManager.tsx';
 const files=new Map([[manager,"import '../../ui/App.tsx'; import('../team/TeamManager.tsx');"]]);
 const actual=inspectWebImports(files,[manager,app,team],{},()=>false);
 assert.deepEqual(actual.diagnostics,[]);
 assert.deepEqual(actual.rules,[
  manager+' -> '+team+' [cross-feature import]',
  manager+' -> '+app+' [upward import]',
 ]);
});

test('Dashboard and TeamManager use the public Tasks read entry and other consumers stay fenced',()=>{
 const view=dashboard+'Dashboard.tsx',other=webRoot+'features/team/Other.tsx';
 const files=new Map([
  [view,"import '../tasks/read.ts'; import('../tasks/model.ts');"],
  [teamManager,"import '../tasks/read.ts'; export { label } from '../tasks/labels.ts'; import('../tasks/model.ts');"],
  [other,"import '../tasks/read.ts';"],
 ]);
 const actual=inspectWebImports(files,[...files.keys(),tasksReadApi,tasks+'model.ts',tasks+'labels.ts'],{},()=>false);
 assert.deepEqual(actual.diagnostics,[]);
 assert.deepEqual(actual.rules,[
  view+' -> '+tasks+'model.ts [deep Tasks import]',
  other+' -> '+tasksReadApi+' [non-public consumer]',
  teamManager+' -> '+tasks+'labels.ts [non-public consumer]',
  teamManager+' -> '+tasks+'model.ts [non-public consumer]',
 ]);
});

test('shared Markdown is available to all three consumers and does not depend on feature internals',()=>{
 const body=webRoot+'ui/MarkdownBody.tsx',markdown=webRoot+'ui/markdown.ts',url=webRoot+'ui/external-url.ts';
 const files=new Map([
  [tasks+'Panels.tsx',"import '../../ui/MarkdownBody.tsx'; import '../../ui/external-url.ts';"],
  [webRoot+'features/artifacts/ArtifactExplorer.tsx',"import '../../ui/MarkdownBody.tsx';"],
  [webRoot+'features/sessions/SessionsCatalog.tsx',"import '../../ui/MarkdownBody.tsx';"],
  [body,"import './markdown.ts';"],
  [markdown,"import './external-url.ts';"],
  [url,"import '../features/artifacts/reader.ts';"],
 ]);
 const reader=webRoot+'features/artifacts/reader.ts';
 const actual=inspectWebImports(files,[...files.keys(),reader],{},()=>false);
 assert.deepEqual(actual.diagnostics,[]);
 assert.deepEqual(actual.rules,[url+' -> '+reader+' [shared view depends on feature]']);
});

test('shared diagrams take presentation inputs and keep graph mapping in its feature',()=>{
 const mermaid=webRoot+'ui/MermaidView.tsx',network=webRoot+'ui/NetworkView.tsx';
 const graph=webRoot+'features/graph/',mapping=graph+'diagram-source.ts';
 const files=new Map([
  [graph+'GraphExplorer.tsx',"import '../../ui/MermaidView.tsx'; import '../../ui/NetworkView.tsx'; import './diagram-source.ts';"],
  [webRoot+'features/database/DatabaseExplorer.tsx',"import '../../ui/MermaidView.tsx';"],
  [webRoot+'features/database/CodeDatabaseUsages.tsx',"import '../../ui/NetworkView.tsx';"],
  [webRoot+'features/workflows/WorkflowManager.tsx',"import '../../ui/MermaidView.tsx';"],
  [mermaid,"import '../features/graph/diagram-source.ts';"],
  [network,"import './App.tsx';"],
 ]);
 const actual=inspectWebImports(files,[...files.keys(),mapping,app],{},()=>false);
 assert.deepEqual(actual.diagnostics,[]);
 assert.deepEqual(actual.rules,[
  mermaid+' -> '+mapping+' [shared view depends on feature]',
  network+' -> '+app+' [shared view depends on feature]',
 ]);
});

test('run usage has its own entry and cannot import screen internals',()=>{
 const dashboardView=dashboard+'Dashboard.tsx',taskManager=tasks+'TaskManager.tsx';
 const usage=webRoot+'features/usage/RunUsage.tsx',session=webRoot+'features/sessions/SessionsCatalog.tsx',team=webRoot+'features/team/model.ts';
 const files=new Map([
  [taskManager,"import '../usage/RunUsage.tsx';"],
  [dashboardView,"import '../usage/RunUsage.tsx';"],
  [session,"import '../usage/RunUsage.tsx';"],
  [app,"import '../features/usage/RunUsage.tsx';"],
  [usage,"import '../team/model.ts';"],
 ]);
 const actual=inspectWebImports(files,[...files.keys(),team],{},()=>false);
 assert.deepEqual(actual.diagnostics,[]);
 assert.deepEqual(actual.rules,[usage+' -> '+team+' [usage depends on screen]']);
});

test('the Tasks read entry exposes the existing selectors and labels through named exports',async()=>{
 const entry=await import(pathToFileURL(join(root,tasksReadApi)).href);
 const model=await import('../../apps/web/src/features/tasks/model.ts');
 const labels=await import('../../apps/web/src/features/tasks/labels.ts');
 assert.deepEqual(Object.keys(entry).sort(),['durationText','errorText','isBlocked','label','semanticStatus','statusText']);
 assert.equal(entry.durationText,model.durationText);
 assert.equal(entry.isBlocked,model.isBlocked);
 assert.equal(entry.semanticStatus,model.semanticStatus);
 assert.equal(entry.label,labels.label);
 assert.equal(entry.statusText,labels.statusText);
 assert.equal(entry.errorText,labels.errorText);
});

test('Dashboard and Tasks boundaries admit only the revision-pinned legacy edges',async()=>{
 const webFiles=await sources(join(root,webRoot));
 const sharedFiles=await sources(join(root,'packages/contracts'));
 const files=new Map(await Promise.all(webFiles.map(async file=>[relativePath(file),await readFile(file,'utf8')] as const)));
 const indexed=[...files.keys(),...sharedFiles.map(relativePath)];
 // Vite's entry imports these local assets. Index them by exact path, never as TypeScript.
 const webAssets=await readdir(join(root,webRoot),{recursive:true,withFileTypes:true});
 indexed.push(...webAssets.filter(entry=>entry.isFile()&&!/\.(?:ts|tsx|mts)$/.test(entry.name)).map(entry=>relativePath(join(entry.parentPath,entry.name))));
 const {compilerOptions,extends:parentConfig}=JSON.parse(await readFile(join(root,'apps/web/tsconfig.json'),'utf8'));
 assert.equal(parentConfig,undefined,'review inherited module resolution before checking boundaries');
 const {baseUrl,paths}=compilerOptions;
 assert.deepEqual(sanitizeModuleResolverConfig({baseUrl,paths}).configReasons,[],'unsupported TypeScript resolution options');
 const config:ModuleResolverConfig={
  ...(baseUrl===undefined&&paths===undefined?{}:{baseUrl:posix.join('apps/web',baseUrl??'.')}),
  ...(paths===undefined?{}:{paths}),
 };
 const actual=inspectWebImports(files,indexed,config,specifier=>{
  if(isBuiltin(specifier))return true;
  if(!/^(?:@[\w.-]+\/)?[\w-][\w.-]*(?:\/[\w.-]+)*$/.test(specifier))return false;
  try{return require.resolve(specifier).includes('node_modules');}catch{return false;}
 });
 assert.deepEqual(actual.diagnostics,[],'every frontend module must resolve or be a known package');
 const baseline=JSON.parse(await readFile(new URL('./fixtures/dashboard-import-baseline.json',import.meta.url),'utf8')) as {
  revision:string;groups:{owner:string;removal_task:string;edges:string[]}[];
 };
 assert.match(baseline.revision,/^[a-f0-9]{40}$/);
 for(const group of baseline.groups){
  assert.ok(group.owner.trim());
  assert.match(group.removal_task,/^PAOS-METH-\d{2}$/);
 }
 assert.deepEqual(actual.rules.map(rule=>rule.replaceAll(webRoot,'')),baseline.groups.flatMap(group=>group.edges).sort(),
  'add no legacy exceptions; remove each exception when its edge is migrated');
});
