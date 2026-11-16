import {createHash,randomUUID} from 'node:crypto';
import type {DatabaseSync} from 'node:sqlite';
import type {StoredEntity,EntityKind} from '../../../../packages/contracts/storage/local-store.ts';

export type HistorySnapshotInput={projectId:string;mode:'catalog'|'transcript'|'search';sessionId?:string;query?:string;filters?:{status?:string|null;taskId?:string|null;agentId?:string|null;source?:string|null;archived?:string|null};cursor?:string;limit:number;anchor?:string};
export type HistorySnapshotResult={items:StoredEntity[];nextCursor:string|null;previousCursor:string|null;snapshot:{generation:string;total:number;createdAt:string};anchorFound?:boolean};
type Options={maxSnapshots?:number;maxBytes?:number;now?:()=>number};
type Row=Record<string,any>;
function fail(code:string):never{throw Object.assign(new Error(code),{code});}
const visible=`COALESCE(json_type(data,'$.hidden'),'') != 'true' AND COALESCE(json_extract(data,'$.role'),'') NOT IN ('reasoning','analysis','hidden_reasoning') AND COALESCE(json_extract(data,'$.channel'),json_extract(data,'$.visibility'),json_extract(data,'$.type'),'') NOT IN ('analysis','hidden','reasoning')`;
const columns=['project_id','id','kind','parent_id','title','body','status','public_key','coverage','data','revision','deleted','updated_at','journal_order'];
const payload='json_object('+columns.map(c=>`'${c}',${c}`).join(',')+')';
function initialize(db:DatabaseSync){
 // Connection-private, disk-backed frozen values; no persistent schema or migration is changed.
 db.exec(`PRAGMA temp_store=FILE; CREATE TEMP TABLE IF NOT EXISTS paos_history_snapshots(id TEXT PRIMARY KEY,scope TEXT NOT NULL,total INTEGER NOT NULL,bytes INTEGER NOT NULL,created_at TEXT NOT NULL,expires INTEGER NOT NULL,touched INTEGER NOT NULL);CREATE TEMP TABLE IF NOT EXISTS paos_history_rows(generation TEXT NOT NULL,ordinal INTEGER NOT NULL,entity_id TEXT NOT NULL,payload TEXT NOT NULL,PRIMARY KEY(generation,ordinal));`);
 const pageSize=Number(db.prepare('PRAGMA temp.page_size').get()!.page_size);db.exec('PRAGMA temp.max_page_count='+Math.floor(256*1024*1024/pageSize));
 // SQLite's built-in lower() only folds ASCII. Match the existing JavaScript Unicode search contract.
 db.function('paos_history_lower',{deterministic:true},value=>String(value??'').toLowerCase());
}
function remove(db:DatabaseSync,id:string){db.prepare('DELETE FROM paos_history_rows WHERE generation=?').run(id);db.prepare('DELETE FROM paos_history_snapshots WHERE id=?').run(id);}

/** Freeze SQL-selected raw values on TEMP disk, then map/redact only the returned page. */
export function historySnapshotPage(db:DatabaseSync,map:(row:Row)=>StoredEntity,input:HistorySnapshotInput,options:Options={}):HistorySnapshotResult{
 if(!Number.isSafeInteger(input.limit)||input.limit<1||input.limit>100)fail('INVALID_PAGINATION');
 if(!['catalog','transcript','search'].includes(input.mode)||typeof input.projectId!=='string'||input.query!==undefined&&(typeof input.query!=='string'||input.query.length>512))fail('INVALID_QUERY');
 // Leave 26 MiB inside the physical TEMP cap for indexes/page metadata; evict before attempting the next freeze.
 const maxBytes=Math.min(options.maxBytes??230*1024*1024,230*1024*1024),maxSnapshots=options.maxSnapshots??100,now=(options.now??Date.now)();initialize(db);
 for(const row of db.prepare('SELECT id FROM paos_history_snapshots WHERE expires<=?').all(now))remove(db,String(row.id));
 const touched=Number(db.prepare('SELECT COALESCE(MAX(touched),0)+1 AS next FROM paos_history_snapshots').get()!.next);
 const project=db.prepare('SELECT root_identity,canonical_root,authority_epoch FROM projects WHERE id=?').get(input.projectId);if(!project)fail('PROJECT_NOT_FOUND');
 const policy=db.prepare('SELECT value FROM store_meta WHERE key=?').get('project_inventory_policy_v1:'+input.projectId)?.value??null;
 const scope=createHash('sha256').update(JSON.stringify([input.projectId,input.mode,input.sessionId??null,input.query??'',input.filters??{},project,policy])).digest('hex');
 let generation='',offset=0,snapshot:Row|undefined,anchorFound:boolean|undefined;
 if(input.cursor){let cursor:any;try{cursor=JSON.parse(Buffer.from(input.cursor,'base64url').toString());}catch{fail('CURSOR_INVALID');}if(typeof cursor.generation!=='string'||!Number.isSafeInteger(cursor.offset)||cursor.offset<0)fail('CURSOR_INVALID');generation=cursor.generation;offset=cursor.offset;snapshot=db.prepare('SELECT * FROM paos_history_snapshots WHERE id=?').get(generation);if(!snapshot||snapshot.scope!==scope)fail('CURSOR_STALE');if(offset>Number(snapshot.total))fail('CURSOR_INVALID');}
 else{
  const values:any[]=[input.projectId];let select:string;
  if(input.mode==='catalog'){
   // Resolve inherited attribution without loading message bodies or joining all task/run values into JS.
   select=`SELECT e.rowid AS journal_order,e.project_id,e.id,e.kind,e.parent_id,e.title,e.body,e.status,e.public_key,e.coverage,json_set(e.data,'$.taskId',COALESCE(json_extract(e.data,'$.taskId'),json_extract(r.data,'$.appAgentRun.taskContext.taskId'),json_extract(r.data,'$.runtimeRun.taskContext.taskId'),json_extract(r.data,'$.appAgentRun.taskId'),json_extract(r.data,'$.runtimeRun.taskId'),(SELECT t.id FROM entities t,json_each(t.data,'$.sessionIds') j WHERE t.project_id=e.project_id AND t.kind='task' AND t.deleted=0 AND j.value=e.id ORDER BY t.rowid LIMIT 1)),'$.agentId',COALESCE(json_extract(e.data,'$.agentId'),(SELECT json_extract(pin.value,'$.assetId') FROM json_each(COALESCE(json_extract(r.data,'$.appAgentRun.assetPins'),json_extract(r.data,'$.runtimeRun.assetPins'),'[]')) pin WHERE json_extract(pin.value,'$.kind')='agent' LIMIT 1)),'$.source',COALESCE(json_extract(e.data,'$.source'),json_extract(r.data,'$.appAgentRun.route'),json_extract(r.data,'$.runtimeRun.route'),CASE WHEN r.id IS NOT NULL THEN 'codex_app_agent' ELSE 'local_store' END)) AS data,e.revision,e.deleted,e.updated_at FROM entities e LEFT JOIN entities r ON r.rowid=(SELECT rowid FROM entities rr WHERE rr.project_id=e.project_id AND rr.kind='run' AND rr.deleted=0 AND COALESCE(json_extract(rr.data,'$.appAgentRun.sessionId'),json_extract(rr.data,'$.runtimeRun.sessionId'))=e.id ORDER BY rr.rowid DESC LIMIT 1) WHERE e.project_id=? AND e.kind='session' AND e.deleted=0`;
   select='SELECT * FROM ('+select+') WHERE 1=1';const filters=input.filters??{};
   for(const name of ['status','taskId','agentId','source'] as const){if(filters[name]){select+=name==='status'?' AND status=?':` AND json_extract(data,'$.${name}')=?`;values.push(filters[name]);}}
   if(filters.archived!==undefined&&filters.archived!==null&&filters.archived!=='all'){select+=` AND (status='archived' OR COALESCE(json_extract(data,'$.archived'),0)=1)=?`;values.push(filters.archived==='true'?1:0);}
   if(input.query){select+=' AND instr(paos_history_lower(title||char(10)||body),paos_history_lower(?))>0';values.push(input.query);}
  }else{
   if(input.mode==='transcript'){const session=db.prepare("SELECT 1 FROM entities WHERE project_id=? AND id=? AND kind='session' AND deleted=0").get(input.projectId,input.sessionId??'');if(!session)fail('SESSION_NOT_FOUND');}
   select=`SELECT rowid AS journal_order,* FROM entities WHERE project_id=? AND kind='message' AND deleted=0 AND ${visible}`;
   if(input.mode==='transcript'){select+=' AND parent_id=?';values.push(input.sessionId);}
   else{if(!input.query?.trim())fail('INVALID_QUERY');select+=' AND instr(paos_history_lower(body),paos_history_lower(?))>0';values.push(input.query);}
  }
  generation=randomUUID();const createdAt=new Date(now).toISOString();db.exec('SAVEPOINT paos_history_freeze');
  try{
   const size=db.prepare(`SELECT count(*) AS total,COALESCE(sum(length(CAST(payload AS BLOB))),0) AS bytes FROM (SELECT ${payload} AS payload FROM (${select}) LIMIT 200001)`).get(...values)!;
   const total=Number(size.total),bytes=Number(size.bytes);if(total>200000||bytes>maxBytes)fail('HISTORY_SNAPSHOT_BUSY');
   for(;;){const used=db.prepare('SELECT count(*) AS count,COALESCE(sum(bytes),0) AS bytes FROM paos_history_snapshots').get()!;if(Number(used.count)<maxSnapshots&&Number(used.bytes)+bytes<=maxBytes)break;const oldest=db.prepare('SELECT id FROM paos_history_snapshots ORDER BY touched,rowid LIMIT 1').get();if(!oldest)fail('HISTORY_SNAPSHOT_BUSY');remove(db,String(oldest.id));}
   db.prepare(`INSERT INTO paos_history_rows SELECT ?,ROW_NUMBER() OVER(ORDER BY journal_order)-1,id,${payload} FROM (${select}) ORDER BY journal_order LIMIT 200001`).run(generation,...values);
   db.prepare('INSERT INTO paos_history_snapshots VALUES(?,?,?,?,?,?,?)').run(generation,scope,total,bytes,createdAt,now+15*60_000,touched);db.exec('RELEASE paos_history_freeze');snapshot={total,created_at:createdAt};
  }catch(error){db.exec('ROLLBACK TO paos_history_freeze;RELEASE paos_history_freeze');if((error as any).errcode===13)fail('HISTORY_SNAPSHOT_BUSY');throw error;}
  if(input.anchor){const anchor=db.prepare('SELECT ordinal FROM paos_history_rows WHERE generation=? AND entity_id=?').get(generation,input.anchor);anchorFound=!!anchor;if(anchor)offset=Math.max(0,Number(anchor.ordinal)-Math.floor(input.limit/2));}
 }
 db.prepare('UPDATE paos_history_snapshots SET touched=? WHERE id=?').run(touched,generation);
 const items:StoredEntity[]=[];let bytes=32768;for(const row of db.prepare('SELECT payload FROM paos_history_rows WHERE generation=? AND ordinal>=? ORDER BY ordinal LIMIT ?').iterate(generation,offset,input.limit)){const raw=JSON.parse(String(row.payload)),entity={...map(raw),journalOrder:Number(raw.journal_order)},encodedBytes=Buffer.byteLength(JSON.stringify(entity));if(encodedBytes>1024*1024-32768)fail('HISTORY_ITEM_TOO_LARGE');if(bytes+encodedBytes>1024*1024)break;items.push(entity);bytes+=encodedBytes;}
 const cursor=(n:number)=>Buffer.from(JSON.stringify({generation,offset:n})).toString('base64url');return {items,nextCursor:offset+items.length<Number(snapshot!.total)?cursor(offset+items.length):null,previousCursor:offset?cursor(Math.max(0,offset-input.limit)):null,snapshot:{generation,total:Number(snapshot!.total),createdAt:String(snapshot!.created_at)},...(anchorFound!==undefined?{anchorFound}:{})};
}

/** Preview bodies are cut in SQL; this API deliberately does not claim full-body search coverage. */
export function artifactSummaryRows(db:DatabaseSync,map:(row:Row)=>StoredEntity,projectId:string,options:{kinds?:readonly EntityKind[]}={}):StoredEntity[]{
 const kinds=options.kinds??['document','task','session','message','comment','evidence','run'];if(!Array.isArray(kinds)||!kinds.length||kinds.length>10||kinds.some(kind=>!['document','task','session','message','comment','evidence','run'].includes(kind)))fail('INVALID_QUERY');
 const result:StoredEntity[]=[];let bytes=0;for(const row of db.prepare(`SELECT project_id,id,kind,parent_id,title,substr(body,1,280) AS body,length(body) AS source_body_chars,status,public_key,coverage,data,revision,deleted,updated_at FROM entities WHERE project_id=? AND deleted=0 AND kind IN (${kinds.map(()=>'?').join(',')}) AND (kind!='message' OR (${visible})) ORDER BY rowid LIMIT 150001`).iterate(projectId,...kinds)){bytes+=Buffer.byteLength(String(row.data))+Buffer.byteLength(String(row.body));if(result.length>=150000||bytes>64*1024*1024)fail('ARTIFACT_SUMMARY_TOO_LARGE');result.push({...map(row),...Number(row.source_body_chars)>280?{bodyPreviewTruncated:true}:{}} as StoredEntity);}
 return result;
}

/** Reject oversized persisted content before any full body or metadata crosses into JavaScript. */
export function artifactDocumentRow(db:DatabaseSync,map:(row:Row)=>StoredEntity,projectId:string,id:string):StoredEntity|null{
 const size=db.prepare('SELECT length(CAST(body AS BLOB)) AS bytes,length(CAST(data AS BLOB)) AS metadata FROM entities WHERE project_id=? AND id=? AND deleted=0').get(projectId,id);if(!size)return null;if(Number(size.bytes)>512*1024||Number(size.metadata)>256*1024)fail('DOCUMENT_TOO_LARGE');
 const row=db.prepare('SELECT * FROM entities WHERE project_id=? AND id=? AND deleted=0').get(projectId,id);return row?map(row):null;
}
