import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,rm,writeFile,mkdir,link,symlink,rename,readFile} from 'node:fs/promises';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {createHash} from 'node:crypto';
import {preflightTaskFiles,captureTaskFiles,compareTaskFiles} from '../../apps/local-service/src/runtime/app-agent-files.mts';
async function fixture(t:any){const root=await mkdtemp(join(tmpdir(),'paos-preflight-'));t.after(()=>rm(root,{recursive:true,force:true}));const binding=await bindProject('p',root);return {root,project:{id:'p',canonicalRoot:binding.workspaceRoot,rootIdentity:binding.directoryIdentity}};}

test('33 selected paths are blocked before dispatch rather than reported as a started or allowed run',async t=>{
 const {project}=await fixture(t),files=Array.from({length:33},(_v,i)=>({relativePath:`new-${i}.txt`,plannedOperation:'create' as const}));
 const report=await preflightTaskFiles(project,files);assert.equal(report.allowed,false);assert.equal(report.counts.bytesComplete,false);
 await assert.rejects(captureTaskFiles(project,files),{code:'task_file_budget_exceeded'});
});

test('32 planned creates remain allowed and immutable execution limits are reported as raw-byte budgets',async t=>{
 const {project}=await fixture(t),files=Array.from({length:32},(_v,i)=>({relativePath:`new-${i}.txt`,plannedOperation:'create' as const})),report=await preflightTaskFiles(project,files);
 assert.equal(report.allowed,true);assert.deepEqual(report.limits,{files:32,fileBytes:65536,totalBytes:524288});assert.equal(report.counts.paths,32);assert.equal(report.counts.missing,32);assert.equal(report.items.every(item=>item.state==='missing'&&item.allowed),true);
});

test('65536 raw bytes pass and 65537 fail even when UTF-8 character counts are smaller',async t=>{
 const {root,project}=await fixture(t);await writeFile(join(root,'exact.txt'),'я'.repeat(32768));await writeFile(join(root,'over.txt'),'я'.repeat(32768)+'x');
 const exact=await preflightTaskFiles(project,[{relativePath:'exact.txt',plannedOperation:'read'}]),over=await preflightTaskFiles(project,[{relativePath:'over.txt',plannedOperation:'read'}]);
 assert.equal(exact.allowed,true);assert.equal(exact.items[0].byteSize,65536);assert.equal(exact.counts.bytesComplete,true);assert.equal(over.allowed,false);assert.equal(over.items[0].byteSize,65537);assert.equal(over.items[0].reason,'file_byte_limit');
});

test('524288 combined raw bytes pass and 524289 fail before reading the over-budget file',async t=>{
 const {root,project}=await fixture(t),files=[];
 for(let i=0;i<8;i++){const relativePath=`part-${i}.txt`;await writeFile(join(root,relativePath),'x'.repeat(65536));files.push({relativePath,plannedOperation:'read' as const});}
 const exact=await preflightTaskFiles(project,files);assert.equal(exact.allowed,true);assert.equal(exact.counts.totalBytes,524288);
 await writeFile(join(root,'extra.txt'),'x');const over=await preflightTaskFiles(project,[...files,{relativePath:'extra.txt',plannedOperation:'read'}]);assert.equal(over.allowed,false);assert.equal(over.counts.totalBytes,524289);assert.equal(over.items.at(-1)!.reason,'total_byte_limit');assert.equal(over.items.at(-1)!.sha256,undefined);
});

test('planned operations distinguish missing create/read/modify/delete and existing create conflicts',async t=>{
 const {root,project}=await fixture(t);await writeFile(join(root,'existing.txt'),'ordinary source');
 assert.equal((await preflightTaskFiles(project,[{relativePath:'new/deep/file.ts',plannedOperation:'create'}])).allowed,true);
 for(const plannedOperation of ['read','modify','delete'] as const){const report=await preflightTaskFiles(project,[{relativePath:'missing.txt',plannedOperation}]);assert.equal(report.allowed,false);assert.equal(report.items[0].reason,'source_missing');}
 const conflict=await preflightTaskFiles(project,[{relativePath:'existing.txt',plannedOperation:'create'}]);assert.equal(conflict.allowed,false);assert.equal(conflict.items[0].state,'conflict');assert.equal(conflict.items[0].reason,'destination_exists');
 for(const relativePath of ['existing.txt','missing.txt'])assert.equal((await preflightTaskFiles(project,[{relativePath,plannedOperation:'create_or_modify_after_discovery'}])).allowed,true);
});

test('rename validates both paths, counts two and preserves observed before/after diffs after creation',async t=>{
 const {root,project}=await fixture(t);await writeFile(join(root,'old.txt'),'rename source');const files=[{relativePath:'new.txt',previousRelativePath:'old.txt',plannedOperation:'rename' as const}],report=await preflightTaskFiles(project,files);
 assert.equal(report.allowed,true);assert.equal(report.counts.paths,2);assert.deepEqual(report.items.map(item=>[item.path,item.role]),[['old.txt','rename_source'],['new.txt','rename_destination']]);
 const before=await captureTaskFiles(project,files);await rename(join(root,'old.txt'),join(root,'new.txt'));const after=await captureTaskFiles(project,files);assert.deepEqual(compareTaskFiles(before,after).map(change=>[change.path,change.operation]),[['old.txt','delete'],['new.txt','add']]);
 const conflict=await preflightTaskFiles(project,files);assert.equal(conflict.allowed,false);assert.ok(conflict.reasons.includes('rename_source_missing'));assert.ok(conflict.reasons.includes('destination_exists'));
 const tooMany=Array.from({length:17},(_v,i)=>({relativePath:`new-${i}.txt`,previousRelativePath:`old-${i}.txt`,plannedOperation:'rename' as const}));assert.equal((await preflightTaskFiles(project,tooMany)).counts.paths,34);assert.equal((await preflightTaskFiles(project,tooMany)).allowed,false);
});

test('capture is observational after planned creates and does not reuse preflight operation or stale-pin fences',async t=>{
 const {root,project}=await fixture(t),file={relativePath:'created.txt',plannedOperation:'create' as const};const before=await captureTaskFiles(project,[file]);await writeFile(join(root,file.relativePath),'created text');const after=await captureTaskFiles(project,[{...file,revision:'0'.repeat(64)}]);assert.equal(after[0].kind,'present');assert.equal(compareTaskFiles(before,after)[0].operation,'add');
 assert.equal((await preflightTaskFiles(project,[file])).allowed,false);
});

test('raw content and metadata pins are separate; stale pins block admission and public reports contain no text or diffs',async t=>{
 const {root,project}=await fixture(t),content='SENSITIVE_RAW_CANARY ordinary source';await writeFile(join(root,'file.txt'),content);const revision=createHash('sha256').update(content).digest('hex'),fresh=await preflightTaskFiles(project,[{relativePath:'file.txt',plannedOperation:'modify',revision}]);
 assert.equal(fresh.allowed,true);assert.equal(fresh.items[0].sha256,revision);assert.ok(fresh.items[0].fileRevision);assert.notEqual(fresh.items[0].fileRevision,revision);assert.equal(JSON.stringify(fresh).includes(content),false);assert.equal('content' in fresh.items[0],false);assert.equal('diff' in fresh.items[0],false);
 const stale=await preflightTaskFiles(project,[{relativePath:'file.txt',plannedOperation:'modify',revision:'0'.repeat(64)}]);assert.equal(stale.items[0].state,'stale');assert.equal(stale.allowed,false);
 const metadata=await preflightTaskFiles(project,[{relativePath:'file.txt',plannedOperation:'modify',fileRevision:'0'.repeat(64)}]);assert.equal(metadata.allowed,false);assert.equal(metadata.items[0].reason,'source_revision_stale');
 assert.equal((await preflightTaskFiles(project,[{relativePath:'file.txt',plannedOperation:'modify',revision}])).digest,fresh.digest);assert.equal(await readFile(join(root,'file.txt'),'utf8'),content);
});

test('inventory excludes, missing ignored targets and private/binary/encoding sources remain blocked without contents',async t=>{
 const {root,project}=await fixture(t);await writeFile(join(root,'.gitignore'),'*.log\nignored/\n');await writeFile(join(root,'.env'),'SENSITIVE_ENV_CANARY');await writeFile(join(root,'binary.txt'),Buffer.from([1,0,2]));await writeFile(join(root,'encoding.txt'),Buffer.from([255]));await writeFile(join(root,'key.txt'),'-----BEGIN PRIVATE KEY-----\nSYNTHETIC');await writeFile(join(root,'allowed.ts'),'let ordinary=1;');
 for(const relativePath of ['new.log','ignored/new.ts','.env']){const report=await preflightTaskFiles(project,[{relativePath,plannedOperation:'create'}]);assert.equal(report.allowed,false,relativePath);}
 for(const [relativePath,reason] of [['binary.txt','binary_file'],['encoding.txt','encoding_unsupported'],['key.txt','sensitive_content']]){const report=await preflightTaskFiles(project,[{relativePath,plannedOperation:'modify'}]);assert.equal(report.allowed,false);assert.equal(report.items[0].reason,reason);assert.equal(report.items[0].sha256,undefined);}
 const excluded=await preflightTaskFiles({...project,inventoryPolicy:{exclude:['allowed.ts']}},[{relativePath:'allowed.ts',plannedOperation:'modify'}]);assert.equal(excluded.items[0].reason,'project_exclude');assert.equal(excluded.allowed,false);
});

test('path duplicates, traversal, URL, linked ancestors and root replacement cannot widen execution authority',async t=>{
 const {root,project}=await fixture(t);const outside=join(root,'outside'),target=join(root,'target');await mkdir(outside);await mkdir(target);await writeFile(join(outside,'foreign.txt'),'OUTSIDE_FILE_CANARY');const binding=await bindProject('t',target),p={id:'t',canonicalRoot:binding.workspaceRoot,rootIdentity:binding.directoryIdentity};await link(join(outside,'foreign.txt'),join(target,'linked.txt'));await symlink(outside,join(target,'alias'),'junction');
 for(const relativePath of ['../outside/foreign.txt','https://example.invalid/foreign','C:/foreign','alias/foreign.txt','linked.txt']){const report=await preflightTaskFiles(p,[{relativePath,plannedOperation:'modify'}]);assert.equal(report.allowed,false,relativePath);assert.equal(JSON.stringify(report).includes('OUTSIDE_FILE_CANARY'),false);}
 const duplicate=await preflightTaskFiles(project,[{relativePath:'a.txt',plannedOperation:'create'},{relativePath:'a.txt',plannedOperation:'create'}]);assert.equal(duplicate.allowed,false);assert.ok(duplicate.reasons.includes('path_duplicate'));
 await rename(target,join(root,'old-target'));await mkdir(target);const replaced=await preflightTaskFiles(p,[{relativePath:'fresh.txt',plannedOperation:'create'}]);assert.equal(replaced.allowed,false);assert.ok(replaced.reasons.includes('project_root_changed'));
});
