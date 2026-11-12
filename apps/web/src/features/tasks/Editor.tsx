import {useEffect,useState} from 'react';
import type {ManagerSnapshot} from '../../../../../packages/contracts/issues/manager.ts';
import type {StoredEntity} from '../../api/client.ts';
import {draftTask,profile,issueTypes,priorities,fileOperations,durationText,parseDuration,lines,type M2TaskProfile} from './model.ts';
import {label,typeText,priorityText,errorText,type Locale,type Word} from './labels.ts';

type Draft={task:M2TaskProfile;revision:number};
// Memory-only drafts survive navigation; no project text is written into browser persistence.
const drafts=new Map<string,Draft>();
export function TaskEditor({entity,projectId,snapshot,locale,onSave,onPreview}:{entity?:StoredEntity;projectId:string;snapshot:ManagerSnapshot<StoredEntity>;locale:Locale;
 onSave:(task:M2TaskProfile,revision:number,reason:string,digest?:string)=>Promise<void>;
 onPreview:(task:M2TaskProfile,revision:number,reason:string)=>Promise<{previewDigest:string}>}){
 const cacheKey=`${projectId}:${entity?.id??'new'}`;
 const [state,setState]=useState<Draft>(()=>drafts.get(cacheKey)??{task:entity?structuredClone(profile(entity)):draftTask(projectId),revision:entity?.revision??0});
 const [dirty,setDirty]=useState(drafts.has(cacheKey)),[busy,setBusy]=useState(false),[error,setError]=useState(''),[reason,setReason]=useState(''),[preview,setPreview]=useState<string>();
 const [estimate,setEstimate]=useState(()=>state.task.estimateSeconds===null?'':durationText(state.task.estimateSeconds));
 const [rawInputs,setRawInputs]=useState<Record<string,string>>({});
 // A successful save adopts server-bound identity; refresh never overwrites an unsaved draft.
 useEffect(()=>{if(entity&&!dirty){const task=structuredClone(profile(entity));setState({task,revision:entity.revision});setEstimate(task.estimateSeconds===null?'':durationText(task.estimateSeconds));setRawInputs({});}},[entity?.id,entity?.revision,dirty]);
 const t=(key:Word)=>label(locale,key),task=state.task;
 function patch(next:Partial<M2TaskProfile>){const changed={...state,task:{...task,...next}};setState(changed);drafts.set(cacheKey,changed);setDirty(true);setPreview(undefined);}
 function textField(key:'title'|'summary'|'technicalValue'|'productValue',word:Word,name:string=key){return <label>{t(word)}{key==='title'?<input name={name} required value={task[key]} onChange={e=>patch({[key]:e.target.value})}/>:<textarea name={name} rows={3} value={task[key]} onChange={e=>patch({[key]:e.target.value})}/>}</label>;}
 function multi(key:'components'|'affectsVersions'|'fixVersions',word:Word,items:{id:string;name:string;status:string}[]){return <label>{t(word)}<select name={key} multiple value={task[key]} onChange={e=>patch({[key]:Array.from(e.target.selectedOptions,o=>o.value)})}>{items.map(item=><option key={item.id} value={item.id}>{item.name}{item.status==='archived'?` (${t('archived')})`:''}</option>)}</select></label>;}
 async function run(previewOnly=false){setBusy(true);setError('');try{
   const parsed={...task,estimateSeconds:parseDuration(estimate)};
   if(previewOnly){const result=await onPreview(parsed,state.revision,reason);setPreview(result.previewDigest);}
   else{await onSave(parsed,state.revision,reason,preview);drafts.delete(cacheKey);setDirty(false);}
  }catch(cause){setError(errorText(locale,cause));}finally{setBusy(false);}}
 const parentOptions=snapshot.tasks.filter(item=>item.id!==task.id&&(task.type==='sub_task'?['task','bug','user_story','Task'].includes(String(item.data?.type)):item.data?.type==='epic'));
 const parentDue=snapshot.tasks.find(item=>item.id===task.parentId)?.data?.dueDate;
 return <form data-testid="task-editor" className="m2-editor" onSubmit={e=>{e.preventDefault();void run();}}>
  {dirty&&<p role="status">{t('unsaved')}</p>}<p role="alert">{error}</p>
  <div className="m2-fields">{textField('title','title')}
   <label>{t('type')}<select name="type" value={task.type} onChange={e=>patch({type:e.target.value as M2TaskProfile['type'],...(e.target.value==='epic'?{parentId:null}:{})})}>{issueTypes.map(type=><option key={type} value={type}>{typeText(type)}</option>)}</select></label>
   <label>{t('parent')}<select name="parentId" disabled={task.type==='epic'} value={task.parentId??''} onChange={e=>patch({parentId:e.target.value||null})}><option value="">{t('none')}</option>{parentOptions.map(parent=><option key={parent.id} value={parent.id}>{parent.publicKey} · {parent.title}</option>)}</select></label>
   <label>{t('priority')}<select name="priority" value={task.priority??''} onChange={e=>patch({priority:e.target.value as M2TaskProfile['priority']})}>{priorities.map(p=><option key={p} value={p}>{priorityText(locale,p)}</option>)}</select></label>
  </div>
  {textField('summary','description','body')}
  <div className="m2-fields">{textField('technicalValue','technicalValue')}{textField('productValue','productValue')}</div>
  <label>{t('criteria')}<textarea name="criteria" rows={4} value={rawInputs.criteria??task.acceptanceCriteria.join('\n')} onChange={e=>{setRawInputs({...rawInputs,criteria:e.target.value});patch({acceptanceCriteria:lines(e.target.value)});}}/></label>
  <div className="m2-fields">
   <label>{t('estimate')}<input name="estimate" placeholder="00:30:00" value={estimate} onChange={e=>{setEstimate(e.target.value);setDirty(true);try{patch({estimateSeconds:parseDuration(e.target.value)});}catch{}}}/></label>
   <label>{t('rank')}<input name="rank" type="number" min="0" step="1" value={task.rank} onChange={e=>patch({rank:Number(e.target.value)})}/></label>
   <label>{t('startDate')}<input name="startDate" type="date" value={task.startDate??''} onChange={e=>patch({startDate:e.target.value||null})}/></label>
   <label>{t('dueDate')}<input name="dueDate" type="date" value={task.dueDate??''} onChange={e=>patch({dueDate:e.target.value||null})}/></label>
   <label>{t('timezone')}<input name="timezone" value={task.timezone} onChange={e=>patch({timezone:e.target.value})}/></label>
   {multi('components','components',snapshot.components)}{multi('affectsVersions','affects',snapshot.versions)}{multi('fixVersions','fix',snapshot.versions)}
  </div>
  {typeof parentDue==='string'&&task.dueDate&&task.dueDate>parentDue&&<p role="status">{locale==='ru'?'Срок задачи позже срока родителя':'Task due date exceeds parent due date'}: {parentDue}. {locale==='ru'?'Даты не наследуются автоматически.':'Dates are not inherited automatically.'}</p>}
  <label>{t('risks')}<textarea name="risks" rows={3} value={rawInputs.risks??task.risks.join('\n')} onChange={e=>{setRawInputs({...rawInputs,risks:e.target.value});patch({risks:lines(e.target.value)});}}/></label>
  <label className="m2-check"><input name="noRisks" type="checkbox" checked={task.risks.length===1&&task.risks[0]==='none'} onChange={e=>{setRawInputs({...rawInputs,risks:e.target.checked?'none':''});patch({risks:e.target.checked?['none']:[]});}}/>{t('noneRisk')}</label>
  <details open><summary>{t('files')}</summary><p className="quiet">{t('referenceHint')}</p>
   {task.files.map((file,index)=>{
    const context=task.fileContexts.find(c=>c.relativePath===file.relativePath);
    const change=(next:Partial<typeof file>)=>{const files=task.files.map((f,i)=>{if(i!==index)return f;const value={...f,...next};if(value.plannedOperation!=='rename'&&value.actualOperation!=='rename'){const {previousRelativePath:unused,...plain}=value;return plain;}return value;});patch({files,fileContexts:task.fileContexts.map(c=>c.relativePath===file.relativePath?{...c,relativePath:files[index].relativePath}:c)});};
    const contextChange=(next:{revision?:string|null;context?:string})=>patch({fileContexts:[...task.fileContexts.filter(c=>c.relativePath!==file.relativePath),{relativePath:file.relativePath,revision:context?.revision??null,context:context?.context??'source',...next}]});
    return <fieldset key={index}><legend>{t('files')} {index+1}</legend><div className="m2-fields">
     <label>{t('relativePath')}<input name={`file-path-${index}`} value={file.relativePath} onChange={e=>change({relativePath:e.target.value})}/></label>
     <label>{t('planned')}<select name={`file-planned-${index}`} value={file.plannedOperation??''} onChange={e=>change({plannedOperation:e.target.value as typeof file.plannedOperation})}><option value="">—</option>{fileOperations.map(op=><option key={op} value={op}>{op}</option>)}</select></label>
     <label>{t('recorded')}<select name={`file-actual-${index}`} value={file.actualOperation??''} onChange={e=>change({actualOperation:(e.target.value||null) as typeof file.actualOperation})}><option value="">—</option>{fileOperations.filter(op=>op!=='create_or_modify_after_discovery').map(op=><option key={op} value={op}>{op}</option>)}</select></label>
     {(file.plannedOperation==='rename'||file.actualOperation==='rename')&&<label>{t('previousPath')}<input value={file.previousRelativePath??''} onChange={e=>change({previousRelativePath:e.target.value})}/></label>}
     <label>{t('revision')}<input name={`file-revision-${index}`} value={context?.revision??''} onChange={e=>contextChange({revision:e.target.value||null})}/></label>
     <label>{t('context')}<input name={`file-context-${index}`} value={context?.context??''} onChange={e=>contextChange({context:e.target.value})}/></label>
    </div><button type="button" onClick={()=>patch({files:task.files.filter((_,i)=>i!==index),fileContexts:task.fileContexts.filter(c=>c.relativePath!==file.relativePath)})}>{t('remove')}</button></fieldset>;
   })}
   <button type="button" data-testid="add-file" onClick={()=>patch({files:[...task.files,{relativePath:'',plannedOperation:'modify',actualOperation:null}]})}>{t('add')} · {t('files')}</button>
  </details>
  <details><summary>{t('assignments')}</summary>
   <label>{t('agentId')}<textarea name="agents" value={rawInputs.agents??task.agentAssignments.join('\n')} onChange={e=>{setRawInputs({...rawInputs,agents:e.target.value});patch({agentAssignments:lines(e.target.value)});}}/></label>
   {task.assignments.map((assignment,index)=><fieldset key={index}><legend>{t('assignments')} {index+1}</legend><div className="m2-fields">{(['agentId','profileVersion','runId','sessionId','startedAt','endedAt'] as const).map(key=><label key={key}>{t(key==='startedAt'?'started':key==='endedAt'?'ended':key)}<input value={assignment[key]??''} onChange={e=>patch({assignments:task.assignments.map((a,i)=>i===index?{...a,[key]:e.target.value||null}:a)})}/></label>)}</div><button type="button" onClick={()=>patch({assignments:task.assignments.filter((_,i)=>i!==index)})}>{t('remove')}</button></fieldset>)}
   <button type="button" onClick={()=>patch({assignments:[...task.assignments,{agentId:'',profileVersion:null,runId:null,sessionId:null,startedAt:null,endedAt:null}]})}>{t('add')} · {t('assignments')}</button>
  </details>
  <details><summary>{t('artifacts')}</summary>
   <label>{t('reference')}<textarea name="artifacts" value={rawInputs.artifacts??task.artifactReferences.join('\n')} onChange={e=>{setRawInputs({...rawInputs,artifacts:e.target.value});patch({artifactReferences:lines(e.target.value)});}}/></label>
   {task.artifacts.map((artifact,index)=><fieldset key={index}><legend>{t('artifacts')} {index+1}</legend><div className="m2-fields">{(['type','reference','revision','provenance'] as const).map(key=><label key={key}>{t(key==='type'?'artifactType':key)}<input value={artifact[key]??''} onChange={e=>patch({artifacts:task.artifacts.map((a,i)=>i===index?{...a,[key]:key==='revision'?(e.target.value||null):e.target.value}:a)})}/></label>)}<label>{t('availability')}<select value={artifact.availability} onChange={e=>patch({artifacts:task.artifacts.map((a,i)=>i===index?{...a,availability:e.target.value as typeof a.availability}:a)})}>{(['available','unverified','unavailable','stale'] as const).map(v=><option key={v} value={v}>{t(v)}</option>)}</select></label></div><button type="button" onClick={()=>patch({artifacts:task.artifacts.filter((_,i)=>i!==index)})}>{t('remove')}</button></fieldset>)}
   <button type="button" onClick={()=>patch({artifacts:[...task.artifacts,{type:'document',reference:'',revision:null,provenance:'user',availability:'unverified'}]})}>{t('add')} · {t('artifacts')}</button>
  </details>
  <div className="m2-fields"><label>{t('blocker')}<input value={task.blocker?.reason??''} onChange={e=>patch({blocker:e.target.value?{reason:e.target.value,owner:task.blocker?.owner??'',since:task.blocker?.since??new Date().toISOString()}:null})}/></label><label>{t('blockerOwner')}<input value={task.blocker?.owner??''} disabled={!task.blocker} onChange={e=>patch({blocker:task.blocker?{...task.blocker,owner:e.target.value}:null})}/></label></div>
  <label>{t('reason')}<input name="reason" value={reason} onChange={e=>setReason(e.target.value)}/></label>
  {entity&&<button type="button" disabled={busy} onClick={()=>void run(true)}>{t('preview')}</button>}
  {preview&&<p role="status">{t('previewReady')} · {typeText(task.type)} → {parentOptions.find(p=>p.id===task.parentId)?.publicKey??t('none')}</p>}
  <div className="m2-actions"><button disabled={busy} className="primary">{preview?t('applyPreview'):t('save')}</button><button type="button" disabled={busy} onClick={()=>{drafts.delete(cacheKey);const next=entity?structuredClone(profile(entity)):draftTask(projectId);setState({task:next,revision:entity?.revision??0});setEstimate(next.estimateSeconds===null?'':durationText(next.estimateSeconds));setDirty(false);setPreview(undefined);}}>{t('discard')}</button></div>
 </form>;
}
