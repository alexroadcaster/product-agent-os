import type {LocalStore} from '../storage/local-store.mts';
/** Explicit task source paths only. Names and prose are never interpreted as semantic code impact. */
export async function relatedGraphTasks(store:LocalStore,projectId:string,path:string,revision:string,sourceHash:string){
 const rows=[];for(let offset=0;offset<1000;offset+=100){const batch=await store.list(projectId,{kind:'task',limit:100,offset});rows.push(...batch);if(batch.length<100)break;}
 const matches=[];for(const task of rows){const d=task.data,refs=[];
  for(const field of ['files','fileContexts','artifacts','artifactReferences'])for(const r of Array.isArray(d[field])?d[field] as any[]:[]){
   const target=typeof r==='string'?r:r?.relativePath??r?.path??r?.reference;if(target!==path)continue;
   const expected=typeof r==='object'&&typeof r.revision==='string'?r.revision:null;
   refs.push({matchReason:`${field}:explicit_path`,sourceState:expected?(expected===sourceHash?'matching':'stale'):'unknown',expectedSourceRevision:expected,actualSourceRevision:sourceHash});
  }
  if(refs.length){const selected=refs.find(r=>r.sourceState==='stale')??refs.find(r=>r.sourceState==='matching')??refs[0];matches.push({id:task.id,title:task.title,revision:task.revision,...selected,sourceRevision:revision,matches:refs});}
 }return matches.slice(0,100);
}
