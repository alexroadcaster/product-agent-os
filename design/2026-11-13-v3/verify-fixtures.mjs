import {readFile,writeFile} from 'node:fs/promises';
import {runInNewContext} from 'node:vm';
import assert from 'node:assert/strict';
const root=new URL('./',import.meta.url), sandbox={window:{}};
runInNewContext(await readFile(new URL('fixtures.js',root),'utf8'),sandbox);
const f=sandbox.window.DesignFixtures;
assert.equal(new Set(f.runs.map(r=>r.id)).size,f.runs.length,'unique receipt IDs');
for(const r of f.runs){
 assert.ok(f.tasks.some(t=>t.id===r.taskId&&t.projectId===r.projectId));
 assert.ok(f.agents.some(a=>a.id===r.agentId));
 if(r.inputTokens!==null){assert.equal(r.totalTokens,r.inputTokens+r.outputTokens);assert.ok(r.cachedInputTokens<=r.inputTokens);}
 else assert.equal(r.totalTokens,null);
 if(r.tools)assert.equal(r.toolUse,Object.values(r.tools).reduce((a,b)=>a+b,0));
}
const total=f.summarize();
for(const field of ['totalTokens','inputTokens','outputTokens','cachedInputTokens','costMicros','toolUse']){
 for(const [key,items] of [['projectId',f.projects],['agentId',f.agents],['taskId',f.tasks]]){
  assert.equal(items.reduce((sum,item)=>sum+f.summarize({[key]:item.id})[field].value,0),total[field].value,`${key}/${field} partitions agree`);
 }
}
assert.equal(total.totalTokens.value,104800);
assert.equal(total.toolUse.value,87);
assert.equal(total.costMicros.value,185500);
assert.equal(total.totalTokens.unknown,1);
assert.equal(f.summarize({taskId:'DEMO-107'}).totalTokens.available,false);
assert.equal(f.summarize({taskId:'DOC-203'}).totalTokens.available,true);
assert.equal(f.summarize({taskId:'DOC-203'}).totalTokens.value,0);
assert.equal(f.progress().total,12);
assert.equal(f.progress().done,3);
const report={command:'node design/2026-11-13-v3/verify-fixtures.mjs',result:'passed',exitCode:0,receipts:f.runs.length,projects:f.projects.length,agents:f.agents.length,tasks:f.tasks.length,knownTotals:{tokens:total.totalTokens.value,toolUse:total.toolUse.value,costMicros:total.costMicros.value},unknownReceipts:total.totalTokens.unknown,checks:['unique IDs','scope foreign keys','input/output/cache composition','tool counts','project/agent/task partitions','zero vs unknown','task progress denominator']};
await writeFile(new URL('fixture-report.json',root),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
