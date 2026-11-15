import assert from 'node:assert/strict';
import {test} from 'node:test';
import {readFile,readdir} from 'node:fs/promises';
import {resolve,dirname,relative,join} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
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
function moduleEdges(source:string){
 const parsed=parser.parseSync('source.ts',source,{lang:'ts',astType:'ts'}),edges:string[]=[];
 assert.equal(parsed.errors.length,0,'boundary check must parse every source');
 function visit(node:any){
  if(!node||typeof node!=='object')return;
  if(['ImportDeclaration','ExportNamedDeclaration','ExportAllDeclaration','ImportExpression','TSImportType'].includes(node.type)&&typeof node.source?.value==='string')edges.push(node.source.value);
  if(node.type==='CallExpression'&&node.callee?.type==='Identifier'&&node.callee.name==='require'&&typeof node.arguments[0]?.value==='string')edges.push(node.arguments[0].value);
  for(const child of Object.values(node))if(Array.isArray(child))child.forEach(visit);else if(child&&typeof child==='object')visit(child);
 }
 visit(parsed.program);return edges;
}
async function sources(directory:string):Promise<string[]>{
 const files:string[]=[];
 for(const entry of await readdir(directory,{withFileTypes:true})){
  const path=join(directory,entry.name);
  if(entry.isDirectory())files.push(...await sources(path));
  else if(entry.isFile()&&/\.(?:ts|mts)$/.test(entry.name))files.push(path);
 }
 return files;
}
test('import boundary parser includes type-only edges, re-exports and literal dynamic imports without matching comments',()=>{
 const code=`import type { A } from './a.ts'; export { b } from './b.ts'; const c=import('./c.ts'); type D=import('./d.ts').D; const e=require('./e.ts'); // import './comment.ts'`;
 assert.deepEqual(moduleEdges(code),['./a.ts','./b.ts','./c.ts','./d.ts','./e.ts']);
});
test('shared contracts never import applications, and the local service never imports frontend source',async()=>{
 const violations:string[]=[];
 for(const area of ['packages/contracts','apps/local-service/src'])for(const file of await sources(join(root,area))){
  for(const specifier of moduleEdges(await readFile(file,'utf8'))){
   if(!specifier.startsWith('.'))continue;
   const target=relative(root,resolve(dirname(file),specifier)).replaceAll('\\','/');
   if(area==='packages/contracts'&&target.startsWith('apps/')||area==='apps/local-service/src'&&target.startsWith('apps/web/src/'))violations.push(relative(root,file)+' -> '+specifier);
  }
 }
 assert.deepEqual(violations,[],'application-independent contract ownership');
});
