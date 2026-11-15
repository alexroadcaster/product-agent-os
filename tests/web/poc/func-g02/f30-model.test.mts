import assert from 'node:assert/strict';
import {test} from 'node:test';
import {relativePath,normalizedCruise,edgeAccuracy,queryChangeTask} from './f30-model.mts';
test('engine paths are relative normalized data and never traversal or absolute authority',()=>{
 assert.equal(relativePath('src\\module.ts'),'src/module.ts');
 for(const path of ['../secret','/absolute','C:\\secret','a/../secret','a//b','a\u0000b'])assert.throws(()=>relativePath(path));
});
test('normalization preserves import semantics, type/dynamic evidence and unresolved diagnostics',()=>{
 const files={'src/a.ts':"import type { X } from './b';\nimport('./missing');",'src/b.ts':'export type X=1;'};
 const result=normalizedCruise({modules:[{source:'src/a.ts',dependencies:[{module:'./b',resolved:'src/b.ts',preCompilationOnly:true},{module:'./missing',couldNotResolve:true,dynamic:true}]},{source:'./missing',couldNotResolve:true,dependencies:[]}]},files);
 assert.equal(result.edges[0].type,'import');assert.equal(result.edges[0].line,1);assert.equal(result.edges[0].typeOnly,true);
 assert.equal(result.unresolved[0].line,2);assert.equal(result.unresolved[0].reason,'missing_import');
 assert.deepEqual(edgeAccuracy(result.edges,[['src/a.ts','src/b.ts']]),{truePositive:1,falsePositive:[],falseNegative:[],precision:1,recall:1});
});
test('an omitted type-only classification remains unknown rather than becoming runtime evidence',()=>{
 const graph=normalizedCruise({modules:[{source:'a.ts',dependencies:[{module:'./b',resolved:'b.ts'}]}]},{'a.ts':"import { x } from './b';",'b.ts':'export const x=1;'});
 assert.equal(graph.edges[0].typeOnly,null);
});
test('change tasks use actual incoming edges and cycle reachability without mutating the snapshot',()=>{
 const edges=[{from:'src/main.ts',to:'src/model.ts',type:'import'},{from:'a',to:'b',type:'import'},{from:'b',to:'a',type:'import'}];
 assert.deepEqual(queryChangeTask(edges,'incoming-alias-model'),['src/main.ts']);assert.deepEqual(queryChangeTask(edges,'cycle'),['a','b']);assert.equal(edges.length,3);
});
