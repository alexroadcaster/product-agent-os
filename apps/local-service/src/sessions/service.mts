import {randomUUID} from 'node:crypto';
import type {LocalStore,StoredEntity} from '../storage/local-store.mts';
import {safePersistedText,isHiddenMessage} from '../redaction/persisted.mts';
import type {HistoryPage,SessionSummary,TranscriptMessage} from '../../../../packages/contracts/sessions/history.ts';
function fail(code:string):never{throw Object.assign(new Error(code),{code});}
const nullable=(value:unknown)=>typeof value==='string'?value:null;
/** Frozen membership and values isolate paging from concurrent inserts, edits and archival. Cursors expire explicitly. */
export function createSessionHistory(store:LocalStore){
 const snapshots=new Map<string,{scope:string;rows:any[];createdAt:string;expires:number;coverage:'complete'|'partial';bytes:number}>();
 function page<T>(scope:string,rows:T[],query:URLSearchParams,coverage:'complete'|'partial'):HistoryPage<T>{
  const limit=Number(query.get('limit')??50);if(!Number.isSafeInteger(limit)||limit<1||limit>100)fail('INVALID_PAGINATION');
  let generation='',offset=0,snapshot:ReturnType<typeof snapshots.get>;
  if(query.has('cursor')){let token:any;try{token=JSON.parse(Buffer.from(query.get('cursor')!,'base64url').toString());}catch{fail('CURSOR_INVALID');}
   generation=token.generation;offset=token.offset;snapshot=snapshots.get(generation);
   if(!snapshot||snapshot.scope!==scope||snapshot.expires<Date.now())fail('CURSOR_STALE');if(!Number.isSafeInteger(offset)||offset<0||offset>snapshot.rows.length)fail('CURSOR_INVALID');
  }else{for(const [id,s]of snapshots)if(s.expires<Date.now())snapshots.delete(id);const bytes=Buffer.byteLength(JSON.stringify(rows));if(bytes>32*1024*1024||snapshots.size>=100||[...snapshots.values()].reduce((n,s)=>n+s.bytes,0)+bytes>64*1024*1024)fail('HISTORY_SNAPSHOT_BUSY');
   generation=randomUUID();snapshot={scope,rows,createdAt:new Date().toISOString(),expires:Date.now()+15*60_000,coverage,bytes};snapshots.set(generation,snapshot);
   if(query.has('anchor')){const index=rows.findIndex((r:any)=>r.id===query.get('anchor'));if(index>=0)offset=Math.max(0,index-Math.floor(limit/2));}
  }
  const cursor=(n:number)=>Buffer.from(JSON.stringify({generation,offset:n})).toString('base64url');
  return {items:snapshot.rows.slice(offset,offset+limit),nextCursor:offset+limit<snapshot.rows.length?cursor(offset+limit):null,previousCursor:offset?cursor(Math.max(0,offset-limit)):null,
   snapshot:{generation,total:snapshot.rows.length,createdAt:snapshot.createdAt},coverage:{status:snapshot.coverage,reasons:['host_history_not_exposed','cursor_expires_after_15_minutes']},retention:{policy:'retain_available',truncated:false,omittedCount:0},
   ...(query.has('anchor')?{anchorId:query.get('anchor')!,anchorFound:snapshot.rows.some(r=>r.id===query.get('anchor'))}:{})};
 }
 const visible=(r:StoredEntity)=>r.kind==='message'&&!isHiddenMessage(r);
 function message(r:StoredEntity):TranscriptMessage{return {id:r.id,sessionId:r.parentId!,body:safePersistedText(r.body),role:String(r.data.role??'unknown'),authorId:nullable(r.data.authorId),agentId:nullable(r.data.agentId),taskId:nullable(r.data.taskId),runId:nullable(r.data.runId),fileRefs:Array.isArray(r.data.fileRefs)?r.data.fileRefs:[],parentSessionId:nullable(r.data.parentSessionId),journalOrder:r.journalOrder??0,timestamp:nullable(r.data.timestamp??r.data.createdAt),source:String(r.data.source??r.data.route??'local_store'),toolType:nullable(r.data.toolType??r.data.itemType),redacted:r.data.redacted===true||r.body!==safePersistedText(r.body),coverage:r.coverage};}
 return {
  async catalog(projectId:string,query:URLSearchParams){const rows=await store.historyRows(projectId);const q=(query.get('q')??'').toLowerCase(),archived=query.get('archived');
   for(const session of rows.filter(r=>r.kind==='session')){const linked=rows.filter(r=>r.kind==='run'&&((r.data.appAgentRun??r.data.runtimeRun) as any)?.sessionId===session.id).at(-1);const run=(linked?.data.appAgentRun??linked?.data.runtimeRun) as any;const task=rows.find(r=>r.kind==='task'&&Array.isArray(r.data.sessionIds)&&r.data.sessionIds.includes(session.id));(session as any).data={...session.data,taskId:session.data.taskId??run?.taskContext?.taskId??run?.taskId??task?.id,agentId:session.data.agentId??run?.assetPins?.find((p:any)=>p.kind==='agent')?.assetId,source:session.data.source??run?.route??(run?'codex_app_agent':'local_store')};}
   const filterNames=['status','taskId','agentId','source'];const filters=Object.fromEntries(filterNames.map(k=>[k,query.get(k)]));
   const sessions=rows.filter(r=>r.kind==='session').filter(r=>filterNames.every(k=>!filters[k]||String(k==='status'?r.status:r.data[k]??(k==='source'?'local_store':''))===filters[k])).filter(r=>!q||`${r.title} ${r.body}`.toLowerCase().includes(q)).filter(r=>archived===null||archived==='all'||(r.status==='archived'||r.data.archived===true)===(archived==='true')).map((r):SessionSummary=>({id:r.id,title:r.title,status:r.status,archived:r.status==='archived'||r.data.archived===true,parentSessionId:nullable(r.data.parentSessionId??r.parentId),forkOf:nullable(r.data.forkOf),agentId:nullable(r.data.agentId),updatedAt:r.updatedAt,taskId:nullable(r.data.taskId),source:String(r.data.source??'local_store'),coverage:r.coverage}));
   return page(`${projectId}:catalog:${q}:${archived}:${JSON.stringify(filters)}`,sessions,query,'partial');},
  async transcript(projectId:string,sessionId:string,query:URLSearchParams){const session=await store.get(projectId,sessionId);if(!session||session.kind!=='session')fail('SESSION_NOT_FOUND');const rows=(await store.historyRows(projectId)).filter(r=>visible(r)&&r.parentId===sessionId).map(message);return page(`${projectId}:transcript:${sessionId}`,rows,query,'partial');},
  async search(projectId:string,query:URLSearchParams){const q=safePersistedText(query.get('q')??'').toLowerCase();if(!q.trim())fail('INVALID_QUERY');const rows=(await store.historyRows(projectId)).filter(r=>visible(r)&&r.body.toLowerCase().includes(q)).map(message);return page(`${projectId}:search:${q}`,rows,query,'partial');}
 };
}
