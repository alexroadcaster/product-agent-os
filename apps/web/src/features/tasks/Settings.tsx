import {useEffect,useState} from 'react';
import type {Board,CatalogItem,VersionItem,ManagerSnapshot} from '../../../../../packages/contracts/issues/manager.ts';
import type {M1Api,StoredEntity} from '../../api/client.ts';
import {requiredBoardStates} from '../../../../../packages/contracts/workflows/helpers.ts';
import {issueTypes,taskStatuses} from './model.ts';
import {label,statusText,typeText,errorText,type Locale,type Word} from './labels.ts';
import type {Command} from './Panels.tsx';

function CatalogRow({value,revision,version,locale,onSave}:{value:CatalogItem|VersionItem;revision:number;version:boolean;locale:Locale;onSave:(item:CatalogItem|VersionItem,revision:number)=>Promise<unknown>}){
 const [draft,setDraft]=useState({item:value,revision,dirty:false}),[busy,setBusy]=useState(false),[error,setError]=useState('');const t=(k:Word)=>label(locale,k);
 const item=draft.item,setItem=(item:typeof value)=>setDraft(old=>({...old,item,dirty:true}));
 // A dirty draft keeps the revision it was edited against, even after a refresh.
 useEffect(()=>{setDraft(old=>old.dirty?old:{item:value,revision,dirty:false});},[value,revision,draft.dirty]);
 return <form className="m2-catalog-row" onSubmit={e=>{e.preventDefault();setBusy(true);setError('');void onSave(item,draft.revision).then(()=>setDraft(old=>({...old,dirty:false}))).catch(e=>setError(errorText(locale,e))).finally(()=>setBusy(false));}}>
  <label>{t('name')}<input name={version?'version-name':'component-name'} required value={item.name} onChange={e=>setItem({...item,name:e.target.value})}/></label>
  <label>{t('availability')}<select name={version?'version-state':'component-state'} value={item.status} onChange={e=>setItem({...item,status:e.target.value} as typeof item)}>{(version?['unreleased','released','archived']:['active','archived']).map(s=><option key={s} value={s}>{t(s as Word)}</option>)}</select></label>
  {version&&<><label>{t('description')}<textarea name="version-description" maxLength={20000} value={(item as VersionItem).description??''} onChange={e=>setItem({...item,description:e.target.value})}/></label><label>{t('startDate')}<input type="date" value={(item as VersionItem).startDate??''} onChange={e=>setItem({...item,startDate:e.target.value||null})}/></label><label>{t('releaseDate')}<input type="date" value={(item as VersionItem).releaseDate??''} onChange={e=>setItem({...item,releaseDate:e.target.value||null})}/></label></>}
  <button disabled={busy}>{t('save')}</button>{draft.dirty&&<button type="button" disabled={busy} onClick={()=>{setDraft({item:value,revision,dirty:false});setError('');}}>{t('discard')}</button>}<span role="alert">{error}</span>
 </form>;
}
export function ManagerSettings({snapshot,command,locale}:{snapshot:ManagerSnapshot<StoredEntity>;command:Command;locale:Locale}){
 const t=(k:Word)=>label(locale,k),[board,setBoard]=useState<Board>(()=>structuredClone(snapshot.board)),[busy,setBusy]=useState(false),[error,setError]=useState('');
 const [boardRevision,setBoardRevision]=useState(snapshot.settingsRevisions.board),[boardDirty,setBoardDirty]=useState(false);
 useEffect(()=>{if(!boardDirty){setBoard(structuredClone(snapshot.board));setBoardRevision(snapshot.settingsRevisions.board);}},[snapshot.board,snapshot.settingsRevisions.board,boardDirty]);
 const [componentName,setComponentName]=useState(''),[versionName,setVersionName]=useState('');
 async function add(version:boolean){setBusy(true);setError('');try{await command({action:version?'version':'component',expectedRevision:snapshot.settingsRevisions[version?'versions':'components'],item:{id:crypto.randomUUID(),name:version?versionName:componentName,status:version?'unreleased':'active'}});if(version)setVersionName('');else setComponentName('');}catch(e){setError(errorText(locale,e));}finally{setBusy(false);}}
 const statusOptions=[...new Set([...taskStatuses,...requiredBoardStates(snapshot.workflows,snapshot.tasks.map(t=>t.data as any)),...snapshot.workflows.workflows.flatMap(w=>w.draft?.states.map(s=>s.id)??[])])];
 const patch=(value:Partial<Board>)=>{setBoard({...board,...value});setBoardDirty(true);};
 return <details data-testid="manager-settings" className="m2-settings"><summary>{t('settings')}</summary>
  <section><h3>{t('components')}</h3>{snapshot.components.map(c=><CatalogRow key={c.id} value={c} revision={snapshot.settingsRevisions.components} version={false} locale={locale} onSave={(item,revision)=>command({action:'component',item,expectedRevision:revision})}/>)}
   <form onSubmit={e=>{e.preventDefault();void add(false);}}><label>{t('name')}<input name="new-component-name" value={componentName} required onChange={e=>setComponentName(e.target.value)}/></label><button disabled={busy}>{t('add')} · {t('components')}</button></form>
  </section>
  <section><h3>{t('versions')}</h3><p>{t('releaseHint')}</p>{snapshot.versions.map(v=><CatalogRow key={v.id} value={v} revision={snapshot.settingsRevisions.versions} version locale={locale} onSave={(item,revision)=>command({action:'version',item,expectedRevision:revision})}/>)}
   <form onSubmit={e=>{e.preventDefault();void add(true);}}><label>{t('name')}<input name="new-version-name" value={versionName} required onChange={e=>setVersionName(e.target.value)}/></label><button disabled={busy}>{t('add')} · {t('versions')}</button></form>
  </section>
  <form data-testid="board-settings" onSubmit={e=>{e.preventDefault();setBusy(true);setError('');void command({action:'board',expectedRevision:boardRevision,board}).then(()=>setBoardDirty(false)).catch(e=>setError(errorText(locale,e))).finally(()=>setBusy(false));}}>
   <h3>{t('releasePolicy')}</h3><label>{t('requireTypes')}<select multiple name="release-required-types" value={board.releaseRequiredTypes??[]} onChange={e=>patch({releaseRequiredTypes:Array.from(e.target.selectedOptions,o=>o.value)})}>{issueTypes.map(type=><option key={type} value={type}>{typeText(type)}</option>)}</select></label>
   <label>{t('requireComponents')}<select multiple name="release-required-components" value={board.releaseRequiredComponents??[]} onChange={e=>patch({releaseRequiredComponents:Array.from(e.target.selectedOptions,o=>o.value)})}>{snapshot.components.map(c=><option key={c.id} value={c.id}>{c.name}</option>)}</select></label>
   <label>{t('timezone')}<input name="project-timezone" value={board.timezone??'Europe/Moscow'} onChange={e=>patch({timezone:e.target.value})}/></label>
   <h3>{t('board')}</h3>{board.columns.map((column,index)=><fieldset key={index}><legend>{t('column')} {index+1}</legend><div className="m2-fields"><label>{t('name')}<input name={`column-name-${index}`} required value={column.id} onChange={e=>patch({columns:board.columns.map((c,i)=>i===index?{...c,id:e.target.value}:c)})}/></label>
    <label>{t('statuses')}<select multiple name={`column-statuses-${index}`} value={column.statuses} onChange={e=>patch({columns:board.columns.map((c,i)=>i===index?{...c,statuses:Array.from(e.target.selectedOptions,o=>o.value)}:c)})}>{statusOptions.map(s=><option key={s} value={s}>{statusText(locale,s)}</option>)}</select></label>
    <label>{t('wip')}<input name={`column-wip-${index}`} type="number" min="0" step="1" value={column.wipLimit??''} onChange={e=>patch({columns:board.columns.map((c,i)=>i===index?{...c,wipLimit:e.target.value===''?undefined:Number(e.target.value),wipMode:c.wipMode??'soft'}:c)})}/></label>
    <label>{t('wipMode')}<select name={`column-mode-${index}`} value={column.wipMode??'soft'} onChange={e=>patch({columns:board.columns.map((c,i)=>i===index?{...c,wipMode:e.target.value as 'soft'|'hard'}:c)})}><option value="soft">soft</option><option value="hard">hard</option></select></label>
   </div><button type="button" onClick={()=>patch({columns:board.columns.filter((_,i)=>i!==index)})}>{t('remove')}</button></fieldset>)}
   <button type="button" onClick={()=>patch({columns:[...board.columns,{id:`column-${board.columns.length+1}`,statuses:[]}]})}>{t('add')} · {t('column')}</button>
   <label className="m2-check"><input name="board-outside" type="checkbox" checked={board.outOfBoard} onChange={e=>patch({outOfBoard:e.target.checked})}/>{t('outOfBoard')}</label>
   <div className="m2-fields"><label>{t('fileLimit')}<input name="attachment-file-limit" type="number" min="1" max="50" value={board.attachmentFileBytes/1048576} onChange={e=>patch({attachmentFileBytes:Number(e.target.value)*1048576})}/></label><label>{t('taskLimit')}<input name="attachment-task-limit" type="number" min="1" value={board.attachmentTaskBytes/1048576} onChange={e=>patch({attachmentTaskBytes:Number(e.target.value)*1048576})}/></label></div>
   <button disabled={busy} className="primary">{t('save')} · {t('settings')}</button>
   {boardDirty&&<button type="button" disabled={busy} onClick={()=>{setBoard(structuredClone(snapshot.board));setBoardRevision(snapshot.settingsRevisions.board);setBoardDirty(false);setError('');}}>{t('discard')}</button>}
  </form><p role="alert">{error}</p>
 </details>;
}
export function FullArchive({api,projectId,locale}:{api:M1Api;projectId:string;locale:Locale}){
 const t=(k:Word)=>label(locale,k),[busy,setBusy]=useState(false),[error,setError]=useState(''),[backupId,setBackupId]=useState(''),[ack,setAck]=useState(false),[result,setResult]=useState('');
 return <details data-testid="manager-archive" className="m2-settings"><summary>{t('archive')}</summary><p>{t('restoreHint')}</p>
  <button disabled={busy} onClick={()=>{setBusy(true);setError('');void api.exportFullProfile(projectId).then(archive=>{setBackupId(archive.backupId);setResult(`${archive.format} · ${archive.backupId}`);}).catch(e=>setError(errorText(locale,e))).finally(()=>setBusy(false));}}>{t('exportArchive')}</button>
  <form onSubmit={e=>{e.preventDefault();setBusy(true);setError('');void api.restoreFullProfile(projectId,backupId).then(result=>setResult(`${result.restoreId} · ${t('restartRequired')}`)).catch(e=>setError(errorText(locale,e))).finally(()=>setBusy(false));}}>
   <label>{t('backupId')}<input name="full-backup-id" value={backupId} required onChange={e=>setBackupId(e.target.value)}/></label>
   <label className="m2-check"><input name="full-restore-confirm" type="checkbox" checked={ack} onChange={e=>setAck(e.target.checked)}/>{t('restoreConfirm')}</label>
   <button disabled={busy||!ack}>{t('restoreArchive')}</button>
  </form><p role="status">{result}</p><p role="alert">{error}</p>
 </details>;
}
