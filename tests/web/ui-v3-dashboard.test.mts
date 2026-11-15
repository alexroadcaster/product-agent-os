import test from 'node:test';
import assert from 'node:assert/strict';
import {summarizeTasks,aggregateSnapshots,assignedWork,recentTasks} from '../../apps/web/src/features/dashboard/model.ts';
test('dashboard uses complete task snapshots and excludes cancelled from progress denominator',()=>{
 const tasks=['done','backlog','in_progress','cancelled'].map((status,i)=>({id:String(i),status,data:{},revision:1}));
 const result=summarizeTasks({tasks,links:[],workflows:{workflows:[]}} as any);
 assert.equal(result.total,4);assert.equal(result.done,1);assert.equal(result.remaining,2);assert.equal(result.progress,1/3);assert.equal(result.cancelled,1);
 assert.equal(summarizeTasks({tasks:[],links:[],workflows:{workflows:[]}} as any).progress,null);
});
test('portfolio never converts failed or missing snapshots into zero',()=>{
 const summary=aggregateSnapshots([{summary:{total:4,done:1,remaining:2,cancelled:1,progress:1/3,blocked:0,counts:{done:1,backlog:2,cancelled:1}}},{error:'offline'}] as any);
 assert.equal(summary.loaded,1);assert.equal(summary.expected,2);assert.equal(summary.total,4);assert.equal(summary.partial,true);
 assert.equal(aggregateSnapshots([]).progress,null);
});

test('agent workload deduplicates open task assignments and excludes ended assignments and terminal tasks',()=>{
 const snapshot={workflows:{workflows:[]},tasks:[{id:'a',status:'in_progress',data:{agentAssignments:['agent'],assignments:[{agentId:'agent',endedAt:null},{agentId:'former',endedAt:'2026-01-01'}]}},{id:'b',status:'done',data:{agentAssignments:['agent']}},{id:'c',status:'cancelled',data:{agentAssignments:['agent']}}]};
 assert.deepEqual(assignedWork(snapshot as any),{agent:['a']});
});

test('agent IDs that match Object prototype keys remain valid independent assignments',()=>{
 const tasks=[{id:'a',status:'ready',data:{agentAssignments:['constructor','toString','__proto__']}}];
 const result=assignedWork({tasks,workflows:{workflows:[]}} as any);
 for(const id of ['constructor','toString','__proto__'])assert.deepEqual(result[id],['a']);
});

test('portfolio retains the expected project count before any read completes',()=>{
 const result=aggregateSnapshots([],2);
 assert.equal(result.expected,2);assert.equal(result.loaded,0);assert.equal(result.partial,true);assert.equal(result.progress,null);
});

test('recent tasks follow modification time instead of storage ID order without mutating the snapshot',()=>{
 const tasks=[{id:'a',updatedAt:'2026-11-15T12:00:00Z'},{id:'b',updatedAt:'2026-11-14T12:00:00Z'},{id:'c',updatedAt:'2026-11-13T12:00:00Z'},{id:'d',updatedAt:'2026-11-12T12:00:00Z'}];
 assert.deepEqual(recentTasks(tasks as any).map(t=>t.id),['a','b','c']);
 assert.deepEqual(tasks.map(t=>t.id),['a','b','c','d']);
});

test('recent task ties and absent or invalid timestamps have deterministic ID order',()=>{
 const tasks=[{id:'z',updatedAt:'2026-11-15T12:00:00Z'},{id:'b'},{id:'a',updatedAt:'invalid'},{id:'y',updatedAt:'2026-11-15T12:00:00Z'}];
 assert.deepEqual(recentTasks(tasks as any).map(t=>t.id),['y','z','a']);
 assert.deepEqual(recentTasks(tasks.slice(1,3) as any).map(t=>t.id),['a','b']);
 assert.deepEqual(recentTasks([]),[]);
});
