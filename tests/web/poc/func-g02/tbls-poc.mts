import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,mkdtemp,lstat,realpath,stat,readdir,rm} from 'node:fs/promises';
import {resolve,join,relative,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {DatabaseSync} from 'node:sqlite';
import {spawn} from 'node:child_process';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {platform,arch,release,cpus,totalmem} from 'node:os';

const protocol=JSON.parse(await readFile('tests/fixtures/func_g02/protocol.json','utf8'));
const hash=(value:Uint8Array|string)=>createHash('sha256').update(value).digest('hex');
const quoted=(name:string)=>'"'+name.replaceAll('"','""')+'"';
export type SchemaTable={name:string;kind:string;withoutRowid:boolean;strict:boolean;columns:any[];foreignKeys:any[];indexes:any[]};

/** Existing local metadata only. table_xinfo deliberately includes generated/hidden columns. No rows are read. */
export function inspectSqlite(path:string){
 const db=new DatabaseSync(path,{readOnly:true});
 try{
  db.exec('PRAGMA query_only=ON; BEGIN');
  const schemaVersion=(db.prepare('PRAGMA schema_version').get() as any).schema_version;
  const tableFlags=new Map((db.prepare('PRAGMA table_list').all() as any[]).filter(t=>t.schema==='main').map(t=>[t.name,t]));
  const tables:SchemaTable[]=(db.prepare("SELECT name,type FROM sqlite_schema WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ORDER BY name").all() as any[]).map(row=>{
   const flags=tableFlags.get(row.name),columns=db.prepare('PRAGMA table_xinfo('+quoted(row.name)+')').all() as any[];
   const indexes=(db.prepare('PRAGMA index_list('+quoted(row.name)+')').all() as any[]).map(i=>({name:i.name,unique:i.unique===1,origin:i.origin,partial:i.partial===1,columns:db.prepare('PRAGMA index_info('+quoted(i.name)+')').all()}));
   const primary=columns.filter(c=>c.pk>0);
   // A single exact-INTEGER PK without a PK index is a rowid alias. The PK index preserves the historical inline DESC exception.
   const rowidAlias=row.type==='table'&&flags?.wr===0&&primary.length===1&&primary[0].type.toUpperCase()==='INTEGER'&&!indexes.some(i=>i.origin==='pk')?primary[0].name:null;
   return{name:row.name,kind:row.type,withoutRowid:flags?.wr===1,strict:flags?.strict===1,
    columns:columns.map(c=>({name:c.name,type:c.type,nullable:c.notnull===0&&c.name!==rowidAlias,notNullDeclared:c.notnull===1,rowidAlias:c.name===rowidAlias,primaryKeyPosition:c.pk,generated:c.hidden===2||c.hidden===3,hidden:c.hidden})),
    foreignKeys:db.prepare('PRAGMA foreign_key_list('+quoted(row.name)+')').all(),indexes};
  });
  db.exec('COMMIT');return{schemaVersion,tables,schemaFingerprint:hash(JSON.stringify(tables))};
 }finally{db.close();}
}

// The process handle remains owned until output and peak working set are captured; all child arguments arrive as JSON, never shell text.
const measuredScript=String.raw`
$pathValue=[System.Environment]::GetEnvironmentVariable('Path','Process')
if([string]::IsNullOrEmpty($pathValue)){$pathValue=[System.Environment]::GetEnvironmentVariable('PATH','Process')}
if(-not [string]::IsNullOrEmpty($pathValue)){[System.Environment]::SetEnvironmentVariable('Path',$null,'Process');[System.Environment]::SetEnvironmentVariable('PATH',$null,'Process');[System.Environment]::SetEnvironmentVariable('Path',$pathValue,'Process')}
$job=([Console]::In.ReadToEnd() | ConvertFrom-Json)
$psi=[System.Diagnostics.ProcessStartInfo]::new();$psi.FileName=$job.binary;$psi.WorkingDirectory=$job.cwd;$psi.UseShellExecute=$false;$psi.CreateNoWindow=$true;$psi.RedirectStandardOutput=$true;$psi.RedirectStandardError=$true
$psi.Environment.Clear();foreach($entry in $job.env.PSObject.Properties){$psi.Environment[$entry.Name]=[string]$entry.Value};foreach($arg in $job.args){$psi.ArgumentList.Add([string]$arg)}
$p=[System.Diagnostics.Process]::new();$p.StartInfo=$psi;$watch=[System.Diagnostics.Stopwatch]::StartNew();[void]$p.Start();$handle=$p.Handle;$out=$p.StandardOutput.ReadToEndAsync();$err=$p.StandardError.ReadToEndAsync();$peak=0L;$timedOut=$false
while(-not $p.HasExited){try{$p.Refresh();$peak=[Math]::Max($peak,$p.PeakWorkingSet64)}catch{};if($watch.ElapsedMilliseconds -gt $job.timeoutMs){$p.Kill($true);$timedOut=$true;break};Start-Sleep -Milliseconds 1}
$p.WaitForExit();$watch.Stop();try{$peak=[Math]::Max($peak,$p.PeakWorkingSet64)}catch{}
$result=@{status=$p.ExitCode;elapsedMs=$watch.Elapsed.TotalMilliseconds;peakRssBytes=$peak;timedOut=$timedOut;stdout=$out.Result;stderr=$err.Result};$p.Dispose();$result|ConvertTo-Json -Depth 4 -Compress
`;
export async function measured(binary:string,args:string[],cwd:string,pwsh:string,timeoutMs=protocol.budgets.smallIndexTimeoutMs){
 const home=join(cwd,'home');await mkdir(home,{recursive:true});
 const env={SystemRoot:process.env.SystemRoot!,WINDIR:process.env.WINDIR??process.env.SystemRoot!,TEMP:home,TMP:home,HOME:home,USERPROFILE:home,APPDATA:home,LOCALAPPDATA:home,PATH:dirname(binary)};
 const result=await new Promise<string>((resolveResult,reject)=>{const child=spawn(pwsh,['-NoProfile','-NonInteractive','-Command',measuredScript],{windowsHide:true,stdio:['pipe','pipe','pipe']});let output='',error='';const timer=setTimeout(()=>{child.kill();reject(Error('MEASUREMENT_WRAPPER_TIMEOUT'));},timeoutMs+10000);child.stdout.on('data',chunk=>{output+=chunk;if(output.length>4*protocol.budgets.maxOutputBytes){child.kill();reject(Error('MEASUREMENT_OUTPUT_LIMIT'));}});child.stderr.on('data',chunk=>error+=chunk);child.once('error',reject);child.once('exit',code=>{clearTimeout(timer);code===0?resolveResult(output):reject(Error('MEASUREMENT_WRAPPER_FAILED '+error.slice(0,500)));});child.stdin.end(JSON.stringify({binary,args,cwd,env,timeoutMs}));});
 return JSON.parse(result) as {status:number;elapsedMs:number;peakRssBytes:number;timedOut:boolean;stdout:string;stderr:string};
}
/** No arbitrary DSN/driver/config/template is accepted. The tool only receives an existing regular SQLite fixture and generated config. */
export async function runTbls(binary:string,path:string,cwd:string,pwsh:string,format:'json'|'mermaid'='json',timeoutMs?:number){
 if(!['json','mermaid'].includes(format))throw Error('FORMAT_NOT_ALLOWED');
 const root=resolve('.tmp/func-g02/f32'),target=await realpath(path),rel=relative(root,target);
 if(rel.startsWith('..')||!rel)throw Error('OUTSIDE_POC_ROOT');
 const file=await lstat(path);if(!file.isFile()||file.isSymbolicLink()||file.nlink!==1)throw Error('REGULAR_SINGLE_LINK_FIXTURE_REQUIRED');
 const config=join(cwd,'controlled-config.json');await mkdir(cwd,{recursive:true});
 await writeFile(config,JSON.stringify({name:'Synthetic schema',docPath:join(cwd,'no-schema-cache'),detectVirtualRelations:{enabled:false},er:{format:'mermaid'}}));
 const dsn='sqlite://'+target.replaceAll('\\','/')+'?mode=ro&_query_only=1';
 return measured(binary,['out','--config',config,'--sort','-t',format,dsn],cwd,pwsh,timeoutMs);
}

export function normalizeSchema(schema:ReturnType<typeof inspectSqlite>,sourceSql?:string){
 const sourceLine=(table:SchemaTable)=>{if(!sourceSql)return null;const start=sourceSql.indexOf('CREATE '+table.kind.toUpperCase()+' '+table.name+' ');return start<0?null:sourceSql.slice(0,start).split('\n').length;};
 const nodes=schema.tables.map((t,i)=>({id:'table-'+i,kind:t.kind,name:t.name,relativePath:'synthetic-schema.sql',line:sourceLine(t)}));
 const byName=new Map(nodes.map(n=>[n.name,n.id]));
 const edges=schema.tables.flatMap(table=>{const groups=new Map<number,any[]>();for(const fk of table.foreignKeys){const list=groups.get(fk.id)??[];list.push(fk);groups.set(fk.id,list);}return [...groups].map(([id,rows])=>({id:hash(table.name+':'+id),from:byName.get(table.name),to:byName.get(rows[0].table),type:'foreign_key',relativePath:'synthetic-schema.sql',line:sourceLine(table),resolution:'declared',columns:rows.map(r=>r.from),parentColumns:rows.map(r=>r.to)}));});
 return{schemaVersion:'paos_engine_poc_snapshot_v1',meta:{engine:'node:sqlite',version:process.versions.sqlite,candidate:{engine:'tbls',version:'1.96.1',decision:'reject',reason:'generated-column loss, identifier failure and unqualified read-only DSN'},sourceRevision:schema.schemaFingerprint,rootIdentity:'synthetic-sqlite-schema',policyVersion:'draft-F28-poc-v1',coverage:{status:'complete_for_fixture',reasons:[]},capabilities:{tables:true,columns:true,keys:true,indexes:true,views:true,rows:false},warnings:['SQLite declared metadata only; business constraints and live data usage are outside this snapshot.','Source lines identify the synthetic fixture DDL, not a location inside a database file.']},tables:schema.tables,nodes,edges,sourceFiles:sourceSql?{'synthetic-schema.sql':sourceSql}:{}};
}
/** Detect drift across an external extraction envelope; a changed schema is never returned as current. */
export async function stableSchemaRead<T>(path:string,read:()=>Promise<T>){const before=inspectSqlite(path),value=await read(),after=inspectSqlite(path);return{state:before.schemaFingerprint===after.schemaFingerprint?'current':'stale',value,beforeRevision:before.schemaFingerprint,afterRevision:after.schemaFingerprint};}
export function canonicalMermaid(snapshot:ReturnType<typeof normalizeSchema>){
 // Encoded identifiers are deterministic and cannot become Mermaid markup; visible original names remain in the separate object table.
 const token=(value:string)=>/^[A-Za-z_][A-Za-z0-9_]*$/.test(value)?value:'n_'+[...value].map(c=>c.codePointAt(0)!.toString(16)).join('_');
 return 'erDiagram\n'+snapshot.tables.map(t=>`${token(t.name)} {\n${t.columns.map(c=>'  '+token(c.type||'unknown')+' '+token(c.name)+(c.primaryKeyPosition?' PK':'')).join('\n')}\n}`).join('\n')+'\n'+snapshot.edges.map(e=>`${token(snapshot.nodes.find(n=>n.id===e.from)!.name)} }o--o| ${token(snapshot.nodes.find(n=>n.id===e.to)!.name)} : declared_FK`).join('\n')+'\n';
}

export async function runPoc(pwsh:string){
 const output=resolve('.tmp/func-g02/f32');await mkdir(output,{recursive:true});const fixture=await mkdtemp(join(output,'fixtures-'));
 const binary=resolve('.tmp/func-g02/tools/tbls-tbls.exe'),dbPath=join(fixture,'schema.db');
 const fixtureSql=await readFile(new URL('./tbls-fixture.sql',import.meta.url),'utf8');
 const db=new DatabaseSync(dbPath);db.exec(fixtureSql);db.close();
 const baseline=inspectSqlite(dbPath),snapshot=normalizeSchema(baseline,fixtureSql),sourceDigest=hash(await readFile(dbPath));await writeFile(join(output,'synthetic-schema.sql'),fixtureSql);
 const checks:any[]=[],runs:any[]=[];const check=(name:string,passed:boolean,details?:unknown)=>checks.push({name,passed,...(details===undefined?{}:{details})});
 const expectedNames=['child','composite_parent','orphan','parent','parent_view','self_node'];
 check('baseline_ground_truth_tables',JSON.stringify(baseline.tables.map(t=>t.name))===JSON.stringify(expectedNames));
 check('baseline_generated_column',baseline.tables.find(t=>t.name==='parent')!.columns.some(c=>c.name==='doubled'&&c.generated));
 check('baseline_composite_fk',snapshot.edges.some(e=>e.columns.length===2));check('baseline_no_inferred_fk',!snapshot.edges.some(e=>e.from===snapshot.nodes.find(n=>n.name==='orphan')!.id));
 await writeFile(join(fixture,'.tbls.yml'),'dsn: unknown-driver://DO_NOT_EXECUTE\ntemplates:\n  mermaid:\n    schema: DO_NOT_READ_PROJECT_TEMPLATE\n');
 for(let i=0;i<protocol.budgets.repeatCount;i++){
  const run=await runTbls(binary,dbPath,fixture,pwsh);const parsed=run.status===0?JSON.parse(run.stdout):null;
  runs.push({case:'small_json',iteration:i,...run,stdout:undefined,stderr:run.stderr.slice(0,400),bytes:Buffer.byteLength(run.stdout)});
  if(i===0){await writeFile(join(output,'tbls-raw-schema.json'),run.stdout);check('tbls_basic_success',run.status===0);check('tbls_target_config_ignored',run.status===0);check('tbls_generated_column_complete',Boolean(parsed?.tables.find((t:any)=>t.name==='parent')?.columns.some((c:any)=>c.name==='doubled')));check('tbls_table_set',JSON.stringify(parsed?.tables.map((t:any)=>t.name).sort())===JSON.stringify(expectedNames));check('tbls_composite_fk',Boolean(parsed?.relations?.some((r:any)=>r.columns?.length===2)));check('tbls_no_inferred_fk',!parsed?.relations?.some((r:any)=>r.table==='orphan'));}
 }
 const mm=await runTbls(binary,dbPath,fixture,pwsh,'mermaid');await writeFile(join(output,'tbls-raw-schema.mmd'),mm.stdout);check('tbls_mermaid_basic_success',mm.status===0&&mm.stdout.startsWith('erDiagram'));check('tbls_json_mermaid_generated_omission_agree',!mm.stdout.includes('doubled'));runs.push({case:'small_mermaid',status:mm.status,elapsedMs:mm.elapsedMs,peakRssBytes:mm.peakRssBytes,bytes:Buffer.byteLength(mm.stdout)});
 check('original_database_unchanged',hash(await readFile(dbPath))===sourceDigest);
 // The raw CLI is probed with mode=ro on a missing fixture; the guarded adapter refuses it before launch.
 const missing=join(fixture,'missing.db');const missingRun=await measured(binary,['out','--config',join(fixture,'controlled-config.json'),'-t','json','sqlite://'+missing.replaceAll('\\','/')+'?mode=ro&_query_only=1'],fixture,pwsh);
 check('missing_database_not_created',missingRun.status!==0&&!await stat(missing).then(()=>true,()=>false),{status:missingRun.status,created:await stat(missing).then(s=>({bytes:s.size}),()=>false)});
 const corrupt=join(fixture,'corrupt.db');await writeFile(corrupt,'synthetic-not-a-database');const corruptRun=await runTbls(binary,corrupt,fixture,pwsh);check('corrupt_database_explicit_failure',corruptRun.status!==0&&/database|file/i.test(corruptRun.stderr+corruptRun.stdout));
 const bad=join(fixture,'adversarial.db'),badDb=new DatabaseSync(bad);badDb.exec('CREATE TABLE "odd`table" ("col\"\"name" TEXT, id INTEGER PRIMARY KEY);');badDb.close();const nativeOdd=inspectSqlite(bad);check('baseline_adversarial_name',nativeOdd.tables[0].name==='odd`table');const badRun=await runTbls(binary,bad,fixture,pwsh);check('tbls_adversarial_identifier_supported',badRun.status===0);await writeFile(join(output,'tbls-adversarial-result.json'),JSON.stringify({status:badRun.status,stderr:badRun.stderr.slice(0,800)}));
 const locked=join(fixture,'locked.db'),lockDb=new DatabaseSync(locked);lockDb.exec('CREATE TABLE item(id INTEGER PRIMARY KEY); BEGIN EXCLUSIVE');const lockedRun=await runTbls(binary,locked,fixture,pwsh,'json',1500);lockDb.exec('ROLLBACK');lockDb.close();check('locked_database_bounded_failure',lockedRun.status!==0||lockedRun.timedOut);runs.push({case:'locked',status:lockedRun.status,timedOut:lockedRun.timedOut,elapsedMs:lockedRun.elapsedMs});
 const walPath=join(fixture,'wal.db'),wal=new DatabaseSync(walPath);wal.exec('PRAGMA journal_mode=WAL; CREATE TABLE original(id INTEGER PRIMARY KEY);');const walRun=await runTbls(binary,walPath,fixture,pwsh);check('wal_schema_read',walRun.status===0&&JSON.parse(walRun.stdout).tables.some((t:any)=>t.name==='original'));const envelope=await stableSchemaRead(walPath,async()=>{const pending=runTbls(binary,walPath,fixture,pwsh);await new Promise(r=>setTimeout(r,20));wal.exec('CREATE TABLE changed(id INTEGER PRIMARY KEY)');return pending;});check('change_during_read_marked_stale',envelope.state==='stale');wal.close();
 const bigPath=join(fixture,'large.db'),big=new DatabaseSync(bigPath);big.exec(Array.from({length:200},(_,i)=>`CREATE TABLE t${i}(id INTEGER PRIMARY KEY,parent_id INTEGER${i?' REFERENCES t'+(i-1)+'(id)':''});`).join(''));big.close();
 const baselineRuns=[];for(let i=0;i<3;i++){const start=performance.now();const value=inspectSqlite(bigPath);baselineRuns.push({elapsedMs:performance.now()-start,objects:value.tables.length,bytes:Buffer.byteLength(JSON.stringify(value)),peakRssKiB:process.resourceUsage().maxRSS});const run=await runTbls(binary,bigPath,fixture,pwsh);runs.push({case:'large_200_json',iteration:i,status:run.status,elapsedMs:run.elapsedMs,peakRssBytes:run.peakRssBytes,bytes:Buffer.byteLength(run.stdout)});check('large_tables_'+i,run.status===0&&JSON.parse(run.stdout).tables.length===200);}
 check('latency_budget',runs.filter(r=>r.elapsedMs!==undefined).every(r=>r.elapsedMs<=protocol.budgets.largeIndexTimeoutMs));check('response_budget',runs.filter(r=>r.bytes!==undefined).every(r=>r.bytes<=protocol.budgets.maxOutputBytes));check('rss_budget',runs.filter(r=>r.peakRssBytes!==undefined).every(r=>r.peakRssBytes>0&&r.peakRssBytes<=protocol.budgets.maxPeakRssMiB*1024**2));
 await writeFile(join(output,'snapshot.json'),JSON.stringify(snapshot,null,2)+'\n');await writeFile(join(output,'schema.mmd'),canonicalMermaid(snapshot));
 const result={task:'PAOS-FUNC-32',status:'engine_poc_complete_ui_pending',decision:'reject_as_authoritative_sqlite_metadata',selectedAlternative:'Node26 node:sqlite table_xinfo/foreign_key_list/index_list, explicitly selected rather than silent fallback',version:'1.96.1',commit:'aa7e7326b3555205148c20cd4702ccdacf9af7c4',binarySha256:hash(await readFile(binary)),archiveSha256:'ecd641e0d1ffde95350b1336cb03603c7f7fd8c7fc20a996323ea80d8594a5c6',protocolSha256:hash(await readFile('tests/fixtures/func_g02/protocol.json')),sourceHashes:Object.fromEntries(await Promise.all(['tests/web/poc/func-g02/tbls-poc.mts','tests/web/poc/func-g02/tbls-fixture.sql'].map(async p=>[p,hash(await readFile(p))]))),hardware:{platform:platform(),arch:arch(),release:release(),logicalCpus:cpus().length,cpuModel:cpus()[0]?.model,totalMemoryMiB:Math.round(totalmem()/1024**2)},checks,runs,baselineRuns,coverage:{tables:baseline.tables.length,foreignKeys:snapshot.edges.length,generatedColumns:1},limits:['tbls omits generated columns from JSON and Mermaid','tbls rejects a valid SQLite backtick-containing table identifier','tested Windows DSN mode=ro forms created missing DB; read-only admission is not established','engine metadata was compared to explicit fixture ground truth, not inferred from README','peak RSS for tbls is process PeakWorkingSet64; Node baseline resourceUsage maxRSS includes harness lifetime','SQLite server/provider/real rows not accessed; UI/tiny Mermaid render owned by root'],fixtureRoot:relative(resolve('.'),fixture).replaceAll('\\','/'),fixtureRetained:false,networkDuringMeasurements:false,realCredentials:false,providerCalls:false};
 const actual=await realpath(fixture);assert.equal(dirname(actual),await realpath(output),'CLEANUP_BOUNDARY');await rm(actual,{recursive:true,force:true});
 await writeFile(join(output,'result.json'),JSON.stringify(result,null,2)+'\n');return result;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){const pwsh=process.argv[2];if(!pwsh)throw Error('ABSOLUTE_PWSH_PATH_REQUIRED');const result=await runPoc(pwsh);console.log(JSON.stringify({decision:result.decision,checks:result.checks.length,engineLimitations:result.checks.filter(c=>!c.passed).map(c=>c.name),output:'.tmp/func-g02/f32/result.json'}));}
