import {useEffect,useRef,useState} from 'react';
import {CommentMarkdown} from './CommentMarkdown.tsx';
import type {ManagerSnapshot} from '../../../../../packages/contracts/issues/manager.ts';
import type {M1Api,StoredEntity,TaskReference,HistoryEvent} from '../../api/client.ts';
import {profile,targetStatuses,safeExternalUrl,lines,durationText,hierarchyStats,type M2TaskProfile} from './model.ts';
import {label,statusText,typeText,errorText,type Locale,type Word} from './labels.ts';
export type Command=(input:Record<string,unknown>)=>Promise<Record<string,unknown>>;
type PendingUpload={file:File;revision:number;key:string;payload:{filename:string;mediaType:string;base64:string}};
// Unknown upload outcomes retain the original envelope in memory, including CAS revision.
const pendingUploads=new Map<string,PendingUpload>();
function useAction(locale:Locale){const[busy,setBusy]=useState(false),[error,setError]=useState('');return {busy,error,run:async(fn:()=>Promise<unknown>)=>{setBusy(true);setError('');try{await fn();}catch(cause){setError(errorText(locale,cause));}finally{setBusy(false);}}};}

export function LifecyclePanel({entity,snapshot,command,locale,requestedStatus}:{entity:StoredEntity;snapshot:ManagerSnapshot<StoredEntity>;command:Command;locale:Locale;requestedStatus?:string}){
 const t=(key:Word)=>label(locale,key),p=profile(entity),action=useAction(locale);
 const targets=[...targetStatuses(entity.status??''),...(requestedStatus==='done'&&!targetStatuses(entity.status??'').includes('done')?['done']:[])];
 const [reason,setReason]=useState(''),[status,setStatus]=useState(requestedStatus??targetStatuses(entity.status??'')[0]??''),[resolution,setResolution]=useState('cancelled'),[hotfix,setHotfix]=useState(''),[override,setOverride]=useState(false);
 const [evidence,setEvidence]=useState(()=>p.acceptanceCriteria.map(criterion=>p.criteriaEvidence.find(e=>e.criterion===criterion)??{criterion,evidence:'',outcome:'failed' as const}));
 useEffect(()=>{if(requestedStatus)setStatus(requestedStatus);},[requestedStatus]);
 const children=snapshot.tasks.filter(task=>task.data?.parentId===entity.id),exclusions=p.scopeExclusions??[];
 const totals=hierarchyStats(snapshot.tasks,entity.id);
 async function transition(next:string,manual=false){return command({action:'transition',taskId:entity.id,expectedRevision:entity.revision,status:next,manual:manual||next==='done'&&entity.status!=='awaiting_acceptance',reason,resolution,evidence:evidence.filter(item=>item.evidence.trim()),softWipOverride:override,...(hotfix?{hotfixReason:hotfix}:{})});}
 return <section className="m2-panel" data-testid="task-transition"><h3>{t('acceptance')}</h3><p className="quiet">{t('manualHint')}</p>
  <dl className="task-metadata"><dt>{t('actual')}</dt><dd>{p.actual.startedAt===null?t('notStarted'):p.actual.durationSeconds===null?t('unknown'):durationText(p.actual.durationSeconds)} · {p.actual.startedAt??'—'} → {p.actual.endedAt??t('unknown')}</dd><dt>{t('creator')}</dt><dd>{p.creator.displayName??p.creator.actorId??t('unknown')} · {p.creator.kind}</dd><dt>{t('initiator')}</dt><dd>{p.initiatedBy??'—'}</dd><dt>{t('created')}</dt><dd>{p.createdAt??t('unknown')}</dd></dl>
  {p.acceptanceCriteria.map((criterion,index)=><fieldset key={criterion}><legend>{criterion}</legend><label>{t('evidence')}<input name={`criterion-evidence-${index}`} value={evidence[index]?.evidence??''} onChange={e=>setEvidence(evidence.map((v,i)=>i===index?{...v,evidence:e.target.value}:v))}/></label><label className="m2-check"><input name={`criterion-passed-${index}`} type="checkbox" checked={evidence[index]?.outcome==='passed'} onChange={e=>setEvidence(evidence.map((v,i)=>i===index?{...v,outcome:e.target.checked?'passed':'failed'}:v))}/>{t('passed')}</label></fieldset>)}
  <form onSubmit={e=>{e.preventDefault();void action.run(()=>transition(status));}}>
   <label>{t('reason')}<input name="transition-reason" value={reason} required onChange={e=>setReason(e.target.value)}/></label>
   <label>{t('transition')}<select name="transition-status" value={status} onChange={e=>setStatus(e.target.value)}>{targets.map(s=><option key={s} value={s}>{statusText(locale,s)}</option>)}</select></label>
   <label>{t('resolution')}<select value={resolution} onChange={e=>setResolution(e.target.value)}>{['cancelled','duplicate','wont_do'].map(v=><option key={v} value={v}>{v}</option>)}</select></label>
   <label>{t('hotfix')}<input name="hotfix-reason" value={hotfix} onChange={e=>setHotfix(e.target.value)}/></label>
   <label className="m2-check"><input name="soft-wip-override" type="checkbox" checked={override} onChange={e=>setOverride(e.target.checked)}/>{t('softOverride')}</label>
   <button disabled={action.busy||!status}>{['done','cancelled'].includes(entity.status??'')?t('reopen'):t('transition')}</button>
  </form>
  {!['done','cancelled'].includes(entity.status??'')&&<div className="m2-actions"><button disabled={action.busy||!reason.trim()} className="primary" onClick={()=>void action.run(()=>transition('done',true))}>{t('complete')}</button><button disabled={action.busy||!reason.trim()} onClick={()=>void action.run(()=>transition('cancelled'))}>{t('cancelTask')}</button></div>}
  <p>{t('timezone')}: {snapshot.board.timezone??p.timezone}{p.timezone!==snapshot.board.timezone?` · ${p.timezone}`:''}</p><h4>{t('rollup')}</h4><p>{totals.done}/{totals.descendants} · {statusText(locale,'cancelled')}: {totals.cancelled} · {t('estimate')}: {durationText(totals.estimateSeconds)}{totals.unknownEstimates?` + ${totals.unknownEstimates} ${t('unknown')}`:''} · {t('actual')}: {durationText(totals.actualSeconds)}</p><p>{t('ownEstimate')}: {durationText(totals.ownEstimateSeconds)}</p>
  <h4>{t('children')}</h4><ul>{children.map(child=><li key={child.id}><strong>{child.publicKey} · {child.title}</strong> · {statusText(locale,child.status??'')}{exclusions.find(e=>e.taskId===child.id)?<><p>{t('excluded')}: {exclusions.find(e=>e.taskId===child.id)?.reason}</p><button disabled={action.busy} onClick={()=>void action.run(()=>command({action:'save',task:{...p,scopeExclusions:exclusions.filter(e=>e.taskId!==child.id)},expectedRevision:entity.revision,reason}))}>{t('restoreScope')}</button></>:<button disabled={action.busy||!reason.trim()} onClick={()=>void action.run(()=>command({action:'save',task:{...p,scopeExclusions:[...exclusions,{taskId:child.id,reason}]},expectedRevision:entity.revision,reason}))}>{t('exclude')}</button>}</li>)}</ul>
  <p role="alert">{action.error}</p>
 </section>;
}

export function LinkedIssues({entity,snapshot,command,locale,onOpenSession,api,onRefresh}:{entity:StoredEntity;snapshot:ManagerSnapshot<StoredEntity>;command:Command;locale:Locale;onOpenSession?:(id:string)=>void;api:M1Api;onRefresh:()=>Promise<void>}){
 const t=(key:Word)=>label(locale,key),action=useAction(locale),[query,setQuery]=useState(''),[reason,setReason]=useState(''),[target,setTarget]=useState(''),[relation,setRelation]=useState('relates_to'),[waiver,setWaiver]=useState('');
 const links=snapshot.links.filter(l=>l.sourceId===entity.id||l.targetId===entity.id),find=(id:string)=>snapshot.tasks.find(t=>t.id===id);
 const candidates=snapshot.tasks.filter(t=>t.id!==entity.id&&`${t.publicKey} ${t.title}`.toLowerCase().includes(query.toLowerCase()));
 return <section data-testid="task-links" className="task-relations"><h3>{t('links')}</h3><ul>{links.map(link=>{
  const other=find(link.sourceId===entity.id?link.targetId:link.sourceId),incoming=link.targetId===entity.id;
  return <li key={link.id}><div><strong>{link.relation}{incoming?` · ${t('incoming')}`:''}</strong><p>{other?.publicKey} · {other?.title} · {statusText(locale,other?.status??'')} · {typeText(String(other?.data?.type??''))}</p><p>{link.reason} · {link.actorId} · <time dateTime={link.createdAt??undefined}>{link.createdAt}</time></p>{link.waiver&&<p>{t('waiver')}: {link.waiver}</p>}{link.state==='pending'&&<><p role="status">{t('pendingLink')}</p><button disabled={action.busy} onClick={()=>void action.run(async()=>{await api.stopPendingLink(entity.projectId,link.id);await onRefresh();})}>{t('requestStop')}</button>{onOpenSession&&<button onClick={()=>{const ids=find(link.targetId)?.data?.sessionIds as string[]|undefined;if(ids?.length)onOpenSession(ids.at(-1)!);}}>{t('sessions')}</button>}<button disabled={action.busy} onClick={()=>void action.run(()=>command({action:'activate-link',linkId:link.id,reason,expectedRevision:snapshot.settingsRevisions.links}))}>{t('activateLink')}</button></>}</div><button disabled={action.busy||!reason.trim()} onClick={()=>void action.run(()=>command({action:'unlink',linkId:link.id,reason,expectedRevision:snapshot.settingsRevisions.links}))}>{t('remove')}</button></li>;
 })}</ul>
 <form onSubmit={e=>{e.preventDefault();void action.run(()=>command({action:'link',expectedRevision:snapshot.settingsRevisions.links,link:{sourceId:entity.id,targetId:target,relation,reason,...(waiver?{waiver}:{})}}));}}>
  <label>{t('query')}<input name="linked-search" value={query} onChange={e=>setQuery(e.target.value)}/></label>
  <label>{t('relation')}<select name="link-relation" value={relation} onChange={e=>setRelation(e.target.value)}>{['blocks','relates_to','duplicates','clones'].map(v=><option key={v} value={v}>{v}</option>)}</select></label>
  <label>{t('target')}<select name="link-target" required value={target} onChange={e=>setTarget(e.target.value)}><option value="">{t('none')}</option>{candidates.map(task=><option key={task.id} value={task.id}>{task.publicKey} · {task.title}</option>)}</select></label>
  <label>{t('linkReason')}<input name="link-reason" required value={reason} onChange={e=>setReason(e.target.value)}/></label>
  <label>{t('waiver')}<input name="link-waiver" value={waiver} onChange={e=>setWaiver(e.target.value)}/></label>
  <button disabled={action.busy}>{t('add')} · {t('links')}</button>
 </form><p role="alert">{action.error}</p></section>;
}

export function Attachments({api,entity,snapshot,command,locale,onRefresh}:{api:M1Api;entity:StoredEntity;snapshot:ManagerSnapshot<StoredEntity>;command:Command;locale:Locale;onRefresh:()=>Promise<void>}){
 const t=(key:Word)=>label(locale,key),action=useAction(locale),[reason,setReason]=useState(''),[ack,setAck]=useState(false),[selected,setSelected]=useState<File|null>(null);
 const attachments=snapshot.attachments.filter(a=>a.data?.taskId===entity.id);
 const uploadScope=`${entity.projectId}:${entity.id}`;
 const pendingUpload=useRef<PendingUpload|undefined>(pendingUploads.get(uploadScope));
 const used=attachments.filter(a=>a.data?.status!=='deleted').reduce((sum,a)=>sum+Number(a.data?.byteSize??0),0);
 async function upload(){
  if(!pendingUpload.current){if(!selected)return;if(selected.size>snapshot.quota.fileBytes)throw new Error('FILE_QUOTA_EXCEEDED');if(used+selected.size>snapshot.quota.taskBytes)throw new Error('TASK_QUOTA_EXCEEDED');
   const bytes=new Uint8Array(await selected.arrayBuffer());let binary='';for(let i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode(...bytes.subarray(i,i+8192));
   pendingUpload.current={file:selected,revision:entity.revision,key:crypto.randomUUID(),payload:{filename:selected.name,mediaType:selected.type||'application/octet-stream',base64:btoa(binary)}};pendingUploads.set(uploadScope,pendingUpload.current);
  }
  const pending=pendingUpload.current;
  await api.uploadAttachment(entity.projectId,entity.id,pending.revision,pending.payload,pending.key);
  pendingUploads.delete(uploadScope);pendingUpload.current=undefined;setSelected(null);await onRefresh();
 }
 return <section className="m2-panel" data-testid="task-attachments"><h3>{t('attachments')}</h3><p>{t('attachmentHint')}</p><p>{t('fileLimit')}: {snapshot.quota.fileBytes/1048576} · {t('taskLimit')}: {snapshot.quota.taskBytes/1048576} · {Math.ceil(used/1024)} KiB</p>
  <form onSubmit={e=>{e.preventDefault();void action.run(upload);}}><label>{t('upload')}<input name="attachment-file" type="file" disabled={action.busy} onChange={e=>{setSelected(e.target.files?.[0]??null);pendingUploads.delete(uploadScope);pendingUpload.current=undefined;}}/></label><button disabled={action.busy||!selected&&!pendingUpload.current}>{pendingUpload.current?t('retry'):t('upload')}</button>{pendingUpload.current&&<button type="button" disabled={action.busy} onClick={()=>{pendingUploads.delete(uploadScope);pendingUpload.current=undefined;setSelected(null);}}>{t('cancel')}</button>}</form>
  <label>{t('reason')}<input name="attachment-reason" value={reason} onChange={e=>setReason(e.target.value)}/></label><label className="m2-check"><input name="attachment-ack" type="checkbox" checked={ack} onChange={e=>setAck(e.target.checked)}/>{t('ackRefs')}</label>
  <ul className="records">{attachments.map(a=>{
   const refs=snapshot.comments.filter(c=>(c.data?.attachmentIds as string[]|undefined)?.includes(a.id));return <li key={a.id}><strong>{String(a.data?.filename)}</strong><p>{String(a.data?.mediaType)} · {String(a.data?.byteSize)} bytes · {String(a.data?.actorId)} · {String(a.data?.createdAt)}</p><p className="mono">SHA-256 {String(a.data?.sha256)}</p>{refs.length>0&&<p>{t('references')}: {refs.map(r=>r.id).join(', ')}</p>}{a.data?.status==='deleted'?<p>{t('deleted')}</p>:<div className="m2-actions"><a href={api.attachmentUrl(entity.projectId,entity.id,a.id)} download>{t('download')}</a><button disabled={action.busy||!reason.trim()||refs.length>0&&!ack} onClick={()=>void action.run(()=>command({action:'attachment-delete',taskId:entity.id,attachmentId:a.id,expectedRevision:a.revision,reason,referencesAcknowledged:ack}))}>{t('remove')}</button></div>}</li>;
  })}</ul><p role="alert">{action.error}</p>
 </section>;
}

export function CommentsPanel({entity,snapshot,command,locale}:{entity:StoredEntity;snapshot:ManagerSnapshot<StoredEntity>;command:Command;locale:Locale}){
 const t=(key:Word)=>label(locale,key),action=useAction(locale),[body,setBody]=useState(''),[editId,setEditId]=useState<string>(),[reply,setReply]=useState(''),[attachmentIds,setAttachments]=useState<string[]>([]),[mentions,setMentions]=useState('');
 const comments=snapshot.comments.filter(c=>c.parentId===entity.id),editing=comments.find(c=>c.id===editId),attachments=snapshot.attachments.filter(a=>a.data?.taskId===entity.id&&a.data?.status!=='deleted');
 function clear(){setEditId(undefined);setBody('');setReply('');setAttachments([]);setMentions('');}
 return <section data-testid="task-comments"><h3>{t('comments')}</h3><ul className="comments">{comments.map(c=><li key={c.id}><small>{String(c.data?.actorId??c.data?.category??t('unknown'))} · <time dateTime={String(c.data?.createdAt??'')}>{String(c.data?.createdAt??'')}</time> · r{c.revision}{c.data?.edited?` · ${t('edited')}`:''}</small>{Boolean(c.data?.replyTo)&&<p>{t('replyTo')}: {String(c.data?.replyTo)}</p>}{c.data?.deleted?<p>{t('deleted')}</p>:<><CommentMarkdown body={c.body??''}/>{Array.isArray(c.data?.mentions)&&<p>{c.data.mentions.join(', ')}</p>}<p>{(c.data?.attachmentIds as string[]|undefined)?.map(id=>snapshot.attachments.find(a=>a.id===id)?.title??id).join(', ')}</p><div className="m2-actions"><button disabled={action.busy} onClick={()=>{clear();setReply(c.id);}}>{t('reply')}</button>{c.data?.category==='m2_comment'&&<><button disabled={action.busy} onClick={()=>{setEditId(c.id);setBody(c.body??'');setReply(String(c.data?.replyTo??''));setAttachments((c.data?.attachmentIds as string[])??[]);setMentions(((c.data?.mentions as string[])??[]).join('\n'));}}>{t('edit')}</button><button disabled={action.busy} onClick={()=>void action.run(()=>command({action:'comment',taskId:entity.id,id:c.id,expectedRevision:c.revision,delete:true}))}>{t('remove')}</button></>}</div></>}</li>)}</ul>
  <form onSubmit={e=>{e.preventDefault();void action.run(async()=>{await command({action:'comment',taskId:entity.id,...(editId?{id:editId}:{}),expectedRevision:editing?.revision??0,body,replyTo:reply||null,attachmentIds,mentions:lines(mentions)});clear();});}}>
   <p className="quiet">{t('markdownHint')}</p><label>{t('comment')}<textarea name="comment" value={body} required rows={4} onChange={e=>setBody(e.target.value)}/></label>
   <label>{t('replyTo')}<select name="comment-reply" value={reply} onChange={e=>setReply(e.target.value)}><option value="">{t('none')}</option>{comments.map(c=><option key={c.id} value={c.id}>{c.id} · {(c.body??'').slice(0,60)}</option>)}</select></label>
   <label>{t('commentAttachments')}<select multiple name="comment-attachments" value={attachmentIds} onChange={e=>setAttachments(Array.from(e.target.selectedOptions,o=>o.value))}>{attachments.map(a=><option key={a.id} value={a.id}>{a.title}</option>)}</select></label>
   <label>{t('mentions')}<textarea name="comment-mentions" value={mentions} onChange={e=>setMentions(e.target.value)}/></label>
   <button disabled={action.busy}>{editing?t('save'):t('comment')}</button>{(editId||reply)&&<button type="button" onClick={clear}>{t('cancel')}</button>}
  </form><p role="alert">{action.error}</p>
 </section>;
}

export function ReferencesPanel({api,entity,locale,onOpenSession}:{api:M1Api;entity:StoredEntity;locale:Locale;onOpenSession?:(id:string)=>void}){
 const p=profile(entity),t=(key:Word)=>label(locale,key),action=useAction(locale),[result,setResult]=useState<TaskReference>();
 const fileContexts=p.fileContexts??[];
 const open=(relativePath:string,revision?:string|null)=>action.run(async()=>setResult(await api.taskReference(entity.projectId,{taskId:entity.id,relativePath,revision})));
 return <section data-testid="task-references"><h3>{t('files')}</h3><p>{t('referenceHint')}</p><ul className="records">{p.files.map((file,index)=><li key={index}><strong>{file.relativePath}</strong><p>{t('planned')}: {file.plannedOperation??'—'} · {t('recorded')}: {file.actualOperation??t('unknown')}</p>{file.previousRelativePath&&<p>{file.previousRelativePath} → {file.relativePath}</p>}<p>{fileContexts.find(c=>c.relativePath===file.relativePath)?.context}</p><p className="mono">{fileContexts.find(c=>c.relativePath===file.relativePath)?.revision??t('unknown')}</p><button disabled={action.busy} onClick={()=>void open(file.relativePath,fileContexts.find(c=>c.relativePath===file.relativePath)?.revision)}>{t('readReference')}</button></li>)}</ul>
  <h3>{t('assignments')}</h3><ul>{(p.assignments??[]).map((a,i)=><li key={i}><strong>{a.agentId}</strong> · {t('profileVersion')}: {a.profileVersion??t('unknown')} · {a.runId??'—'} · {a.sessionId??'—'}<p>{a.startedAt??'—'} → {a.endedAt??'—'}</p>{a.sessionId&&onOpenSession&&<button onClick={()=>onOpenSession(a.sessionId!)}>{t('sessions')}</button>}</li>)}{p.agentAssignments.map(a=><li key={a}>{a}</li>)}</ul>
  <h3>{t('artifacts')}</h3><ul>{[...(p.artifacts??[]),...p.artifactReferences.map(reference=>({type:'reference',reference,revision:null,provenance:'legacy',availability:'unverified' as const}))].map((a,i)=>{
   const external=safeExternalUrl(a.reference);return <li key={i}><strong>{a.type}</strong> · {a.reference}<p>{a.provenance} · {t(a.availability)} · {a.revision??t('unknown')}</p>{external?<a href={external} target="_blank" rel="noopener noreferrer">{t('reference')}</a>:<button disabled={action.busy} onClick={()=>void open(a.reference,a.revision)}>{t('readReference')}</button>}</li>;
  })}</ul><p role="alert">{action.error}</p>{result&&<section role="status"><h4>{t(result.availability)} · {result.relativePath}</h4><p>{result.reason??''}</p><p className="mono">{result.revision}</p>{result.content!==undefined&&<pre className="diff">{result.content}</pre>}</section>}
 </section>;
}

/** History renders only safe service metadata; deleted comment bodies never re-enter this view. */
export function ManagerHistory({api,entity,locale}:{api:M1Api;entity:StoredEntity;locale:Locale}){
 const t=(key:Word)=>label(locale,key),[items,setItems]=useState<HistoryEvent[]>([]),[cursor,setCursor]=useState<string>(),[actor,setActor]=useState(''),[field,setField]=useState(''),[after,setAfter]=useState(''),action=useAction(locale);
 const load=(append=false)=>action.run(async()=>{const page=await api.history(entity.projectId,append?cursor:undefined);setItems(old=>append?[...old,...page.items]:page.items);setCursor(page.nextCursor);});
 useEffect(()=>{void load();},[entity.projectId,entity.id]);
 const entries=items.filter(item=>{
  const data=JSON.stringify(item.payload??{});return data.includes(entity.id)&&(!actor||(item.actorId??'').includes(actor))&&(!field||data.includes(field))&&(!after||(item.occurredAt??'')>=after);
 });
 return <section data-testid="task-history"><h3>{t('history')}</h3><div className="m2-fields"><label>{t('creatorFilter')}<input value={actor} onChange={e=>setActor(e.target.value)}/></label><label>{t('query')}<input value={field} onChange={e=>setField(e.target.value)}/></label><label>{t('startAfter')}<input type="date" value={after} onChange={e=>setAfter(e.target.value)}/></label></div>
  <ul className="records">{entries.map((item,index)=>{const payload=item.payload as Record<string,unknown>|undefined;const changes=(payload?.taskChanges??[]) as Record<string,unknown>[];return <li key={`${item.seq}:${index}`}><p>{item.actorId??t('unknown')} · <time dateTime={item.occurredAt}>{item.occurredAt}</time> · #{item.seq}</p>{changes.filter(c=>c.id===entity.id).map((change,i)=><section key={i}><p>r{String(change.previousRevision)} → r{String(change.currentRevision)} · {String(change.source)} · {String(change.reason??'—')} · coverage: {String(change.coverage??'unknown')}{change.omittedFields?` · omitted: ${change.omittedFields}`:''}</p>{((change.fields??[]) as Record<string,unknown>[]).map((f,j)=><dl key={j}><dt>{String(f.field)} · coverage: {String(f.coverage??'unknown')}{f.redacted?' · redacted':''}</dt><dd><pre className="diff">{JSON.stringify(f.previous,null,2)} → {JSON.stringify(f.current,null,2)}</pre></dd></dl>)}</section>)}{Array.isArray(payload?.commentChanges)&&<p>{t('comments')}: {payload.commentChanges.map((c:any)=>`${c.id} r${c.current?.revision??''}${c.current?.deleted?' · deleted':''}`).join(', ')}</p>}{Array.isArray(payload?.managerChanges)&&payload.managerChanges.map((change:any,i:number)=><section key={i}><h4>{String(change.kind)} · {String(change.id)}</h4><pre className="diff">{JSON.stringify({previous:change.previous,current:change.current,redacted:change.redacted},null,2)}</pre></section>)}</li>;})}</ul>
  {!entries.length&&!action.busy&&<p>{t('empty')}</p>}<button disabled={action.busy} onClick={()=>void load(true)}>{action.busy?t('loading'):t('refresh')}</button><p role="alert">{action.error}</p>
 </section>;
}
