import assert from 'node:assert/strict';
import test from 'node:test';
import {mkdtemp,writeFile,rm} from 'node:fs/promises';
import {resolve,join} from 'node:path';
import {isolatedEnvironment,classifyAdmission,manifest} from './codebase-memory.mts';

test('native PoC environment excludes ambient credentials and keeps runtime/cache/config under the owned home',()=>{
 const home=resolve('.tmp/func-g02/f31/unit-home'),root=resolve('.tmp/func-g02/f31/unit-project');
 const env=isolatedEnvironment(home,root);
 for(const key of ['OPENAI_API_KEY','ANTHROPIC_API_KEY','GITHUB_TOKEN','CODEX_HOME','CBM_DOWNLOAD_URL'])assert.equal(Object.hasOwn(env,key),false,key);
 for(const key of ['USERPROFILE','HOME','APPDATA','LOCALAPPDATA','XDG_CONFIG_HOME','TEMP','TMP','CBM_CACHE_DIR','CBM_RUNTIME_DIR'])assert.ok(env[key].startsWith(home),key);
 assert.equal(env.CBM_ALLOWED_ROOT,root);assert.equal(env.CBM_DIAGNOSTICS,'false');
});
test('native admission rejection is distinguished from executor setup failures and unrelated tool errors',()=>{
 assert.equal(classifyAdmission({exitCode:1,stderr:'codebase-memory-mcp: could not load saved runtime settings'}),'runtime_settings_admission_rejected');
 assert.equal(classifyAdmission({exitCode:null,error:'spawn EPERM',stderr:''}),'executor_or_spawn_failure');
 assert.equal(classifyAdmission({exitCode:1,stderr:'invalid argument'}),'other_engine_error');
 assert.equal(classifyAdmission({exitCode:0,stderr:''}),'admitted');
});
test('source-preservation observation detects a changed source without persisting source text',async()=>{
 const root=await mkdtemp(resolve('.tmp/func-g02/f31/source-observation-'));
 try{const path=join(root,'fixture.ts');await writeFile(path,'export const x=1;');const before=await manifest(root);await writeFile(path,'export const x=2;');const after=await manifest(root);assert.notEqual(before['fixture.ts'],after['fixture.ts']);assert.match(before['fixture.ts'],/^[a-f0-9]{64}$/);}
 finally{await rm(root,{recursive:true,force:true});}
});
