import type {LocalStore,StoredEntity} from '../storage/local-store.mts';
import {safePersistedText} from '../redaction/persisted.mts';
import type {HistoryPage,SessionSummary,TranscriptMessage} from '../../../../packages/contracts/sessions/history.ts';
import type {HistorySnapshotInput} from '../storage/history-snapshots.mts';
function fail(code:string):never{throw Object.assign(new Error(code),{code});}
const nullable=(value:unknown)=>typeof value==='string'?value:null;
/** Worker-owned TEMP snapshots freeze membership and values; only a bounded page crosses the Worker boundary. */
export function createSessionHistory(store:LocalStore){
 async function page<T>(projectId:string,query:URLSearchParams,input:Omit<HistorySnapshotInput,'projectId'|'limit'|'cursor'|'anchor'>,map:(row:StoredEntity)=>T):Promise<HistoryPage<T>>{
  const limit=Number(query.get('limit')??50);if(!Number.isSafeInteger(limit)||limit<1||limit>100)fail('INVALID_PAGINATION');
  const snapshot=await store.historySnapshotPage(projectId,{...input,limit,...(query.has('cursor')?{cursor:query.get('cursor')!}:{}),...(query.has('anchor')?{anchor:query.get('anchor')!}:{})});
  return {...snapshot,source:{schemaVersion:'paos_history_capability_v1',adapter:'paos_local_store',projectId,generation:snapshot.snapshot.generation,localHistory:'available',hostHistory:'not_connected',loadedProfiles:'unavailable',reason:'selected_route_has_no_host_history_adapter'},items:snapshot.items.map(map),coverage:{status:'partial',reasons:['selected_route_has_no_host_history_adapter','cursor_expires_after_15_minutes','cursor_may_be_evicted_by_storage_budget']},retention:{policy:'retain_available',truncated:false,omittedCount:0},...(query.has('anchor')?{anchorId:query.get('anchor')!,anchorFound:snapshot.anchorFound??false}:{})};
 }
 function message(r:StoredEntity):TranscriptMessage{return {id:r.id,sessionId:r.parentId!,body:safePersistedText(r.body),role:String(r.data.role??'unknown'),authorId:nullable(r.data.authorId),agentId:nullable(r.data.agentId),taskId:nullable(r.data.taskId),runId:nullable(r.data.runId),fileRefs:Array.isArray(r.data.fileRefs)?r.data.fileRefs:[],parentSessionId:nullable(r.data.parentSessionId),journalOrder:r.journalOrder??0,timestamp:nullable(r.data.timestamp??r.data.createdAt),source:String(r.data.source??r.data.route??'local_store'),toolType:nullable(r.data.toolType??r.data.itemType),redacted:r.data.redacted===true||r.body!==safePersistedText(r.body),coverage:r.coverage};}
 return {
  catalog:(projectId:string,query:URLSearchParams)=>page(projectId,query,{mode:'catalog',query:(query.get('q')??'').toLowerCase(),filters:Object.fromEntries(['status','taskId','agentId','source','archived'].map(key=>[key,query.get(key)]))},(r):SessionSummary=>({id:r.id,title:r.title,status:r.status,archived:r.status==='archived'||r.data.archived===true,parentSessionId:nullable(r.data.parentSessionId??r.parentId),forkOf:nullable(r.data.forkOf),agentId:nullable(r.data.agentId),updatedAt:r.updatedAt,taskId:nullable(r.data.taskId),source:String(r.data.source??'local_store'),coverage:r.coverage})),
  transcript:(projectId:string,sessionId:string,query:URLSearchParams)=>page(projectId,query,{mode:'transcript',sessionId},message),
  search:(projectId:string,query:URLSearchParams)=>{const q=safePersistedText(query.get('q')??'').toLowerCase();if(!q.trim())fail('INVALID_QUERY');return page(projectId,query,{mode:'search',query:q},message);}
 };
}
