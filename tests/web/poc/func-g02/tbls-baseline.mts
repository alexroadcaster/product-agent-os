import assert from 'node:assert/strict';
import {readFile,writeFile,mkdtemp,realpath,rm} from 'node:fs/promises';
import {resolve,join,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {DatabaseSync} from 'node:sqlite';
import {inspectSqlite} from './tbls-poc.mts';

// Alternative-only measurement; preserves original native runs and their source provenance.
const root=await realpath(resolve('.tmp/func-g02/f32'));
const temporary=await mkdtemp(join(root,'baseline-'));
try{
 const small=join(temporary,'small.db'),large=join(temporary,'large.db');
 for(const [path,sql] of [[small,await readFile('tests/web/poc/func-g02/tbls-fixture.sql','utf8')],[large,Array.from({length:200},(_,i)=>`CREATE TABLE t${i}(id INTEGER PRIMARY KEY,parent_id INTEGER${i?' REFERENCES t'+(i-1)+'(id)':''});`).join('')]]){
  const db=new DatabaseSync(path);db.exec(sql);db.close();
 }
 const runs=[];
 for(const [name,path] of [['small',small],['large_200',large]])for(let iteration=0;iteration<3;iteration++){
  const start=performance.now(),value=inspectSqlite(path);
  runs.push({case:name,iteration,elapsedMs:performance.now()-start,objects:value.tables.length,bytes:Buffer.byteLength(JSON.stringify(value)),peakRssKiB:process.resourceUsage().maxRSS});
 }
 const sourceSha256=createHash('sha256').update(await readFile('tests/web/poc/func-g02/tbls-poc.mts')).digest('hex');
 const resultPath=join(root,'result.json'),result=JSON.parse(await readFile(resultPath,'utf8'));
 result.baselineAfterNullabilityFix={measuredAt:new Date().toISOString(),command:'node tests/web/poc/func-g02/tbls-baseline.mts',sourceSha256,normalizationVersion:'sqlite_metadata_v2_effective_nullable',scope:'in-process metadata extraction; maxRSS includes harness lifetime',runs,medianMs:Object.fromEntries(['small','large_200'].map(name=>[name,runs.filter(r=>r.case===name).map(r=>r.elapsedMs).sort((a,b)=>a-b)[1]])),nativeToolExecuted:false,originalBaselineRunsPreserved:true};
 await writeFile(resultPath,JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify(result.baselineAfterNullabilityFix,null,2));
}finally{
 const actual=await realpath(temporary);assert.equal(dirname(actual),root,'CLEANUP_BOUNDARY');await rm(actual,{recursive:true,force:true});
}
