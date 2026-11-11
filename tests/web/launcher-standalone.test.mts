import assert from 'node:assert/strict';
import {test} from 'node:test';
import {assertExternalParent,AbsenceMonitor,desktopExecutableName} from './single-window/standalone-acceptance.mts';
import {allowsSyntheticRequest} from './single-window/autonomous-launcher-acceptance.mts';

const app='C:\\Program Files\\WindowsApps\\OpenAI.Codex\\Codex.exe';
const rows=[{pid:10,parentPid:20,path:'C:\\node.exe'},{pid:20,parentPid:30,path:'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'},{pid:30,parentPid:0,path:'C:\\Windows\\explorer.exe'}];
test('autonomous browser permits only the synthetic local journey, never connection or inference writes',()=>{
 const origin='http://127.0.0.1:41111';
 assert.equal(allowsSyntheticRequest(origin,origin+'/api/v1/bootstrap/exchange','POST'),true);
 assert.equal(allowsSyntheticRequest(origin,origin+'/api/v1/connection','POST'),false);
 assert.equal(allowsSyntheticRequest(origin,origin+'/api/v1/runtime/send','POST'),false);
 assert.equal(allowsSyntheticRequest(origin,'https://example.com/','GET'),false);
 assert.equal(allowsSyntheticRequest(origin,origin+'/api/v1/projects/p/imports/commit','POST'),false);
 assert.equal(allowsSyntheticRequest(origin,origin+'/api/v1/projects/p/entities?kind=task','GET'),true);
});
test('external runner rejects Codex ancestry and incomplete process observations',()=>{
 assert.doesNotThrow(()=>assertExternalParent(rows,10,app,'C:\\Windows'));
 assert.throws(()=>assertExternalParent([...rows.slice(0,2),{pid:30,parentPid:0,path:app}],10,app,'C:\\Windows'),{code:'APP_ANCESTOR'});
 assert.throws(()=>assertExternalParent(rows.slice(0,1),10,app,'C:\\Windows'),{code:'ANCESTRY_UNVERIFIED'});
});
test('absence observations reject blind inventory and permanently invalidate App reappearance or gaps',()=>{
 const blind=new AbsenceMonitor(app);assert.throws(()=>blind.observe([],1000),{code:'INVENTORY_INVALID'});
 const monitor=new AbsenceMonitor(app,2000);monitor.observe(rows,1000);monitor.observe(rows,2000);
 assert.equal(monitor.receipt().valid,true);assert.equal(monitor.receipt().samples,2);
 assert.throws(()=>monitor.observe([...rows,{pid:40,parentPid:30,path:app.toUpperCase()}],3000),{code:'APP_RUNNING'});
 assert.throws(()=>monitor.observe(rows,4000),{code:'ABSENCE_INVALIDATED'});assert.equal(monitor.receipt().valid,false);
 const gap=new AbsenceMonitor(app,2000);gap.observe(rows,1000);
 assert.throws(()=>gap.observe(rows,3001),{code:'OBSERVATION_GAP'});assert.equal(gap.receipt().valid,false);
});
test('desktop selection supports the installed Codex package ChatGPT.exe and rejects its CLI',()=>{
 const installed='C:\\Program Files\\WindowsApps\\OpenAI.Codex_26.1103.7773.0_x64__2p2nqsd0c76g0\\app\\ChatGPT.exe';
 assert.equal(desktopExecutableName(installed),'ChatGPT.exe');
 assert.throws(()=>desktopExecutableName('C:\\Program Files\\WindowsApps\\OpenAI.Codex_26.1103.7773.0_x64__2p2nqsd0c76g0\\app\\resources\\codex.exe'),{code:'DESKTOP_EXECUTABLE_REQUIRED'});
 const monitor=new AbsenceMonitor(installed);monitor.observe(rows,1000);
 assert.throws(()=>monitor.observe([...rows,{pid:40,parentPid:30,path:installed}],2000),{code:'APP_RUNNING'});
});
