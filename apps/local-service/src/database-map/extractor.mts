import {DatabaseSync,constants as c} from 'node:sqlite';
import type {Worker} from 'node:worker_threads';
import {startSchemaWatchdog} from './watchdog.mts';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import type {DatabaseTable,DatabaseMapLimits,DatabaseIndex,DatabaseForeignKey} from '../../../../packages/contracts/database-map.ts';
const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
const quote=(name:string)=>'"'+name.replaceAll('"','""')+'"';
/** Fixed authorization policy, also exercised against the installed SQLite engine. */
export function metadataAuthorizer(){
 const pragmas=new Set(['schema_version','table_list','table_xinfo','index_list','index_xinfo','foreign_key_list']);
 return (action:number,a:string|null,b:string|null,database:string|null,view:string|null)=>{
   if(view||database&&database!=='main')return c.SQLITE_DENY;
   if(action===c.SQLITE_SELECT)return c.SQLITE_OK;
   if(action===c.SQLITE_READ&&(a==='sqlite_master'||a==='sqlite_schema')&&['name','type','rootpage',''].includes(b??''))return c.SQLITE_OK;
   if(action===c.SQLITE_PRAGMA&&pragmas.has(a??''))return c.SQLITE_OK;
   if(action===c.SQLITE_TRANSACTION&&a==='COMMIT')return c.SQLITE_OK;
   return c.SQLITE_DENY;
 };
}
/** F32 sqlite_metadata_v2_effective_nullable semantics, implemented over fixed
 * metadata statements only. A child process owns SQLite so cancellation can
 * terminate native work; JS heap bounds are not a native RSS limit. */
export function extractDatabaseMetadata(path:string,limits:DatabaseMapLimits){
 const db=new DatabaseSync(path,{readOnly:true,allowExtension:false,defensive:true,timeout:0,limits:{attach:0,length:1024*1024,sqlLength:1024*1024,exprDepth:100,column:4096}});
 try{
  db.exec('PRAGMA query_only=ON; PRAGMA trusted_schema=OFF; BEGIN');
  db.setAuthorizer(metadataAuthorizer());
  const schemaVersion=Number((db.prepare('PRAGMA schema_version').get() as any).schema_version);
  const objects:any[]=[];
  for(const row of db.prepare("SELECT name,type FROM sqlite_schema WHERE type IN ('table','view') ORDER BY name").iterate())if(!String(row.name).startsWith('sqlite_')){objects.push(row);if(objects.length>limits.tables)fail('DATABASE_SCHEMA_TABLE_LIMIT');}
  const flags=new Map<string,any>();let flagCount=0;
  for(const row of db.prepare('PRAGMA table_list').iterate()){if(++flagCount>limits.tables+16)fail('DATABASE_SCHEMA_TABLE_LIMIT');if(row.schema==='main'&&!String(row.name).startsWith('sqlite_'))flags.set(String(row.name),row);}
  const tables:DatabaseTable[]=[],reasons:string[]=[];let columnCount=0,foreignCount=0,indexPartCount=0;
  for(const object of objects){
   if(object.name.startsWith('sqlite_'))continue;
   const f=flags.get(object.name),kind=f?.type==='virtual'?'virtual':object.type as 'table'|'view';
   if(kind!=='table'){const reason=kind==='virtual'?'VIRTUAL_TABLE_NOT_EXPANDED':'VIEW_NOT_EXPANDED';tables.push({name:object.name,kind,withoutRowid:false,strict:false,columns:[],foreignKeys:[],indexes:[],reasons:[reason]});reasons.push(reason);continue;}
   const raw=db.prepare('PRAGMA table_xinfo('+quote(object.name)+')').all() as any[];columnCount+=raw.length;if(columnCount>limits.columns)fail('DATABASE_SCHEMA_COLUMN_LIMIT');
   const indexes:DatabaseIndex[]=[];
   for(const value of db.prepare('PRAGMA index_list('+quote(object.name)+')').iterate()){
    const i=value as any,columns:DatabaseIndex['columns']=[];
    for(const value of db.prepare('PRAGMA index_xinfo('+quote(i.name)+')').iterate()){if(++indexPartCount>limits.indexParts)fail('DATABASE_SCHEMA_INDEX_LIMIT');const x=value as any;columns.push({position:x.seqno,columnId:x.cid,expression:x.cid===-2,rowid:x.cid===-1,name:x.name,descending:x.desc===1,collation:x.coll,key:x.key===1});}
    indexes.push({name:i.name,unique:i.unique===1,origin:i.origin,partial:i.partial===1,columns});if(indexes.length>limits.indexParts)fail('DATABASE_SCHEMA_INDEX_LIMIT');
   }
   const primary=raw.filter(x=>x.pk>0),rowidAlias=f?.wr===0&&primary.length===1&&primary[0].type.toUpperCase()==='INTEGER'&&!indexes.some(i=>i.origin==='pk')?primary[0].name:null;
   const foreignKeys:DatabaseForeignKey[]=[];
   for(const value of db.prepare('PRAGMA foreign_key_list('+quote(object.name)+')').iterate()){if(++foreignCount>limits.foreignKeys)fail('DATABASE_SCHEMA_FOREIGN_KEY_LIMIT');const x=value as any;foreignKeys.push({id:x.id,sequence:x.seq,from:x.from,to:x.to,targetTable:x.table,declaredTargetColumn:x.to,targetResolution:'unresolved',onUpdate:x.on_update,onDelete:x.on_delete,match:x.match});}
   tables.push({name:object.name,kind,withoutRowid:f?.wr===1,strict:f?.strict===1,columns:raw.map(x=>({name:x.name,type:x.type,nullable:x.notnull===0&&x.name!==rowidAlias,notNullDeclared:x.notnull===1,rowidAlias:x.name===rowidAlias,primaryKeyPosition:x.pk,generated:x.hidden===2||x.hidden===3,hidden:x.hidden})),foreignKeys,indexes,reasons:[]});
  }
  for(const table of tables)for(const fk of table.foreignKeys){const target=tables.find(t=>t.name===fk.targetTable);if(!target){table.reasons.push('FOREIGN_KEY_TARGET_UNRESOLVED');reasons.push('FOREIGN_KEY_TARGET_UNRESOLVED');continue;}if(fk.to!==null&&target.columns.some(c=>c.name===fk.to))fk.targetResolution='column';else if(fk.to===null){const column=target.columns.find(c=>c.primaryKeyPosition===fk.sequence+1);if(column){fk.to=column.name;fk.targetResolution='primary_key';}}if(fk.targetResolution==='unresolved'){table.reasons.push('FOREIGN_KEY_TARGET_UNRESOLVED');reasons.push('FOREIGN_KEY_TARGET_UNRESOLVED');}}
  db.exec('COMMIT');const revision=createHash('sha256').update(JSON.stringify(tables)).digest('hex');return {schemaVersion,tables,revision,reasons:[...new Set(reasons)]};
 }finally{db.close();}
}
// stdin is constructor-owned input, never target SQL. Public output excludes SQLite error messages.
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 let input='';for await(const chunk of process.stdin){input+=chunk;if(input.length>8192)fail('DATABASE_SCHEMA_INPUT_LIMIT');}
 let watchdog:Worker|undefined;
 try{const data=JSON.parse(input);
  // Fixed trusted watchdog runs independently of native SQLite on the main
  // thread. It can kill only this owned process, never a target/provider PID.
  watchdog=await startSchemaWatchdog(data.limits.milliseconds);
  const started=performance.now(),schema=extractDatabaseMetadata(data.path,data.limits),result={...schema,metrics:{elapsedMs:performance.now()-started,maxRssKiB:process.resourceUsage().maxRSS}},text=JSON.stringify({result});if(Buffer.byteLength(text)>data.limits.outputBytes)fail('DATABASE_SCHEMA_OUTPUT_LIMIT');process.stdout.write(text);
 }
 catch(error){process.stdout.write(JSON.stringify({error:/^DATABASE_SCHEMA_/.test((error as any).code??'')?(error as any).code:'DATABASE_SCHEMA_UNAVAILABLE'}));process.exitCode=1;}
 finally{await watchdog?.terminate();}
}
