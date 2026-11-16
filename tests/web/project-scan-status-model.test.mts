import {test} from 'node:test';
import assert from 'node:assert/strict';
import type {ProjectScanView,ProjectScan} from '../../packages/contracts/project-scan.ts';
import {mergeScanView} from '../../apps/web/src/features/projects/ProjectScanStatus.model.ts';

function fixture(projectId='p',version=1,attempt=1,state:ProjectScan['state']='running'):ProjectScanView{
 return {schemaVersion:'paos_project_scan_view_v1',projectId,version,latest:{schemaVersion:'paos_project_scan_v1',projectId,scanId:'scan-'+attempt,attempt,rootIdentity:'root-a',policyVersion:'policy-a',requestedRevision:null,inventoryRevision:'revision-a',state,stage:'code',startedAt:'2026-11-15T00:00:00Z',updatedAt:'2026-11-15T00:00:00Z',counts:null,reasons:[],stages:[]},lastSuccessful:null,capabilities:{inventory:true,documents:true,code:true,analysis:false,schema:false,code_database:false},limits:{concurrency:1,milliseconds:60000,stageMilliseconds:30000,resultBytes:262144,queued:20}};
}
test('a foreign or malformed snapshot never enters the selected project view',()=>{
 const current=fixture();assert.equal(mergeScanView('p',current,fixture('q',9)),current);assert.equal(mergeScanView('q',undefined,current),undefined);
 assert.equal(mergeScanView('p',current,{...fixture(),version:-1}),current);assert.equal(mergeScanView('p',current,{...fixture('p',10),latest:{...fixture().latest!,projectId:'q'}}),current);
});
test('monotonic versions and attempt identities reject late superseded responses',()=>{
 const current=fixture('p',6,2);assert.equal(mergeScanView('p',current,fixture('p',5,3)),current);assert.equal(mergeScanView('p',current,fixture('p',6,2)),current);
 assert.equal(mergeScanView('p',current,fixture('p',7,1)),current);assert.equal(mergeScanView('p',current,{...fixture('p',7,2),latest:{...current.latest!,scanId:'different-id'}}),current);
 const newer=fixture('p',8,3);assert.equal(mergeScanView('p',current,newer),newer);
});
test('a terminal attempt cannot reopen and one attempt cannot change its bound scope or revision',()=>{
 const cancelled=fixture('p',5,1,'cancelled');assert.equal(mergeScanView('p',cancelled,fixture('p',6,1,'running')),cancelled);
 const current=fixture('p',3);for(const field of ['rootIdentity','policyVersion','inventoryRevision'] as const){const incoming=fixture('p',4);incoming.latest![field]='different';assert.equal(mergeScanView('p',current,incoming),current);}
 const initial=fixture('p',1);initial.latest!.inventoryRevision=null;const bound=fixture('p',2);assert.equal(mergeScanView('p',initial,bound),bound);
});
