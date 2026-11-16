import {useEffect,useRef,useState} from 'react';
import {HttpApiError,type M1Api,type ProjectRegistration} from '../../api/client.ts';
import type {AppLabel} from '../../locales/app.ts';

/** User-selected filesystem root stays a draft until Add; retry keeps the exact registration envelope. */
export function ProjectOnboarding({api,t,onProject,locale='ru',onOpenFiles}:{api:M1Api;t:(key:AppLabel)=>string;locale?:'ru'|'en';onOpenFiles?:(id:string)=>void;onProject:(name:string,root:string,requestId:string)=>Promise<ProjectRegistration>}){
 const w=(ru:string,en:string)=>locale==='ru'?ru:en;
 const [name,setName]=useState(''),[root,setRoot]=useState(''),[busy,setBusy]=useState(false),[notice,setNotice]=useState(''),[error,setError]=useState(''),[result,setResult]=useState<ProjectRegistration>();
 const selectButton=useRef<HTMLButtonElement>(null),selection=useRef<string|undefined>(undefined),pending=useRef<{id:string;name:string;root:string}|undefined>(undefined);
 const selectionAbort=useRef<AbortController|undefined>(undefined),mounted=useRef(true);
 useEffect(()=>{mounted.current=true;return()=>{mounted.current=false;selectionAbort.current?.abort();};},[]);
 function describe(cause:unknown){if(cause instanceof HttpApiError){if(cause.code==='ROUTE_NOT_FOUND'||cause.code?.includes('UNAVAILABLE'))return t('desktopUnavailable');if(cause.code==='DESKTOP_BUSY')return t('folderAlreadyOpen');if(cause.code==='PROJECT_IDENTITY_CONFLICT')return t('projectAlreadyAdded');}return String(cause);}
 async function choose(){setBusy(true);setError('');setNotice(t('folderDialogOpen'));selection.current??=crypto.randomUUID();selectionAbort.current=new AbortController();
  try{const selected=await api.selectProjectFolder(selection.current,root||undefined,selectionAbort.current.signal);if(!mounted.current)return;selection.current=undefined;if(selected.cancelled){setNotice(t('folderSelectionCancelled'));return;}
   setRoot(selected.workspaceRoot);setName(current=>current||selected.workspaceRoot.replace(/[\\/]+$/,'').split(/[\\/]/).at(-1)||'Project');setResult(undefined);pending.current=undefined;setNotice(t('folderSelected'));
  }catch(cause){if(!mounted.current)return;if(cause instanceof HttpApiError)selection.current=undefined;setError(describe(cause));setNotice('');}
  finally{if(mounted.current){setBusy(false);selectButton.current?.focus();}}
 }
 async function add(){setBusy(true);setError('');setNotice(t('projectScanning'));
  const envelope=pending.current??{id:crypto.randomUUID(),name:name.trim(),root:root.trim()};pending.current=envelope;
  try{const saved=await onProject(envelope.name,envelope.root,envelope.id);if(!mounted.current)return;setResult(saved);pending.current=undefined;setName('');setRoot('');setNotice(t('projectAdded'));
  }catch(cause){if(!mounted.current)return;if(cause instanceof HttpApiError&&cause.status<500)pending.current=undefined;setError(describe(cause));setNotice('');}
  finally{if(mounted.current)setBusy(false);}
 }
 return <section className="panel" data-testid="project-onboarding"><h2>{t('addProject')}</h2><p>{t('projectFolderHint')}</p>
  <button type="button" ref={selectButton} disabled={busy} onClick={()=>void choose()}>{t('chooseProjectFolder')}</button>
  <form onSubmit={e=>{e.preventDefault();if(name.trim()&&root.trim())void add();}}>
   <label>{t('name')}<input name="name" required disabled={busy||!!pending.current} value={name} onChange={e=>setName(e.target.value)}/></label>
   <label>{t('root')}<input name="root" required autoComplete="off" disabled={busy||!!pending.current} value={root} onChange={e=>{setRoot(e.target.value);setResult(undefined);}} placeholder={t('chooseProjectFolder')}/></label>
   <button disabled={busy||!name.trim()||!root.trim()}>{pending.current&&!busy?t('retryProjectAdd'):t('addProject')}</button>
  </form><p role="status" aria-live="polite">{notice}</p>{error&&<p role="alert">{error}</p>}
  {result&&<section data-testid="project-scan-summary"><h3>{t('projectScanSummary')}</h3><p>{result.name} · {w('Проект зарегистрирован. Сканирование выполняется отдельно.','Project registered. Scanning runs separately.')}</p>
   <p>{result.scan?.latest?.state??(result.scanError?w('Сканирование недоступно','Scan unavailable'):w('Сканирование не запрошено','Scan not requested'))}</p>
   {result.scanError&&<p role="alert">{result.scanError}</p>}
   {onOpenFiles&&<button type="button" data-testid="onboarding-files" onClick={()=>onOpenFiles(result.id)}>{w('Открыть файлы','Open files')}</button>}
   <p className="quiet">{w('Файлы доступны до готовности индекса. Последний сохранённый статус, отмена и повтор показаны ниже.','Files are available before indexing. The persisted status, cancel and retry controls are shown below.')}</p>
  </section>}
 </section>;
}
