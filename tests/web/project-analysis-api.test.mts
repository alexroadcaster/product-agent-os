import test from 'node:test';import assert from 'node:assert/strict';
import {writeFile,rename} from 'node:fs/promises';import {join} from 'node:path';
import {g03Fixture,until} from './project-g03-fixture.mts';
test('analysis is explicit before observation and actual core scan result persists with source invalidation',async t=>{
 const f=await g03Fixture(t);await writeFile(join(f.workspace,'pyproject.toml'),'[project]\nname="synthetic"\nversion="0.0.1"\n');
 const missing=await f.request('/projects/p/analysis');assert.equal(missing.status,200);assert.equal((await missing.json()).availability,'unavailable');
 assert.equal((await f.request('/projects/p/scans',{requestId:'analysis-api'})).status,202);
 const scanned=await until(async()=>await(await f.request('/projects/p/scans')).json(),view=>['partial','completed','failed'].includes(view.latest?.state));assert.equal(scanned.latest.stages.find((stage:any)=>stage.kind==='analysis').state,'partial');
 const view=await(await f.request('/projects/p/analysis')).json();assert.equal(view.availability,'available');assert.equal(view.stale,false);assert.equal(view.projection.files,scanned.latest.stages.find((stage:any)=>stage.kind==='analysis').counts.projected);assert.ok(view.projection.files>=2);assert.ok(view.stack.some((row:any)=>row.name==='python'));assert.equal(view.runtime.coreModule,'product_agent_os.discovery.analyze_workspace');assert.match(view.adapterSourceRevision,/^[a-f0-9]{64}$/);
 await f.restart();const restored=await(await f.request('/projects/p/analysis')).json();assert.equal(restored.sourceRevision,view.sourceRevision);assert.equal(restored.stale,false);
 await rename(join(f.workspace,'main.ts'),join(f.workspace,'changed.ts'));const stale=await(await f.request('/projects/p/analysis')).json();assert.equal(stale.stale,true);assert.equal(stale.sourceRevision,view.sourceRevision);
 assert.equal((await f.request('/projects/p/files/policy',{expectedVersion:0,policy:{exclude:['pyproject.toml']}})).status,200);assert.equal((await(await f.request('/projects/p/analysis')).json()).stale,true);
});
