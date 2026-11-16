import {useEffect,useRef,useState} from 'react';
import {createLatestRequest} from '../../api/latest-request.ts';
import type {ProjectAnalysisView,AnalysisEvidence,AnalysisSource} from '../../../../../packages/contracts/project-analysis.ts';
import './project-analysis.css';

type AnalysisApi={projectAnalysis:(projectId:string,signal?:AbortSignal)=>Promise<ProjectAnalysisView>};
/** Saved projection evidence loads only for the mounted selected project. It never starts scans. */
export function ProjectAnalysis({api,projectId,locale,onOpenFiles,onOpenGraph,onOpenDatabase}:{api:AnalysisApi;projectId:string;locale:'ru'|'en';onOpenFiles?:()=>void;onOpenGraph?:()=>void;onOpenDatabase?:()=>void}){
 const [view,setView]=useState<ProjectAnalysisView>(),[error,setError]=useState(''),[loading,setLoading]=useState(false),[refresh,setRefresh]=useState(0);
 const current=useRef<ProjectAnalysisView|undefined>(undefined);
 const w=(ru:string,en:string)=>locale==='ru'?ru:en;
 useEffect(()=>{
  const request=createLatestRequest();setLoading(Boolean(projectId));setError('');
  if(current.current?.projectId!==projectId){current.current=undefined;setView(undefined);}
  if(projectId)void request.run(signal=>api.projectAnalysis(projectId,signal),next=>{
   if(next.schemaVersion!=='paos_project_analysis_v1'||next.projectId!==projectId){setError('ANALYSIS_SCOPE_MISMATCH');setLoading(false);return;}
   // observedAt is evidence time, not a scan generation. Request disposal fences
   // stale responses; a completed stage may predate an unavailable GET fallback.
   current.current=next;setView(next);setLoading(false);
  },()=>{setError('ANALYSIS_UNAVAILABLE');setLoading(false);});
  return()=>request.dispose();
 },[api,projectId,refresh]);
 const visible=view?.projectId===projectId?view:undefined;
 const source=(item:AnalysisSource)=><span className="analysis-source" key={item.path}><code>{item.path}</code> · {item.basis==='content'?w('содержимое','content'):w('метаданные','metadata')} · {w('строка не определена','line unknown')}</span>;
 const evidence=(items:AnalysisEvidence[])=>items.length?<ul>{items.map((item,index)=><li key={item.name+index}><strong>{item.name}</strong> <span className="quiet">{item.confidence==='candidate'?w('Признак, требует проверки','Candidate, requires verification'):w('Обнаружено','Detected')}</span>{item.sources.map(source)}</li>)}</ul>:<p className="quiet">{w('Нет наблюдений в доступной проекции.','No observations in the available projection.')}</p>;
 return <section className="panel project-analysis" data-testid="project-analysis" data-project-id={projectId} data-analysis-revision={visible?.inventoryRevision??''} aria-busy={loading}>
  <header className="analysis-heading"><div><h2>{w('Анализ проекта','Project analysis')}</h2><p className="quiet">{w('Признаки стека, документов и схемы из ограниченной проекции файлов.','Stack, document and schema signals from a bounded file projection.')}</p></div><button type="button" data-testid="analysis-refresh" disabled={loading||!projectId} onClick={()=>setRefresh(value=>value+1)}>{w('Обновить','Refresh')}</button></header>
  {!projectId&&<p>{w('Выберите проект.','Select a project.')}</p>}
  {loading&&<p role="status">{w('Загрузка анализа…','Loading analysis…')}</p>}
  {error&&<p role="alert">{w('Актуальность анализа не подтверждена. Обновите данные или повторите сканирование.','Current analysis could not be confirmed. Refresh or retry scanning.')} <code>{error}</code></p>}
  {visible&&<>
   <p data-testid="analysis-state" data-availability={visible.availability} role="status">{visible.availability==='available'?w('Частичное покрытие','Partial coverage'):w('Анализ недоступен','Analysis unavailable')}</p>
   {visible.stale&&<p role="alert" data-testid="analysis-stale">{w('Снимок устарел. Запустите новое сканирование перед выводами о проекте.','This snapshot is stale. Start a new scan before drawing conclusions about the project.')}</p>}
   <dl className="analysis-meta"><div><dt>{w('Наблюдение','Observed')}</dt><dd><time dateTime={visible.observedAt}>{visible.observedAt}</time></dd></div><div><dt>{w('Версия исходников','Source revision')}</dt><dd><code>{visible.sourceRevision}</code></dd></div><div><dt>{w('Корень','Root identity')}</dt><dd><code>{visible.rootIdentity}</code></dd></div><div><dt>{w('Политика','Policy')}</dt><dd><code>{visible.policyVersion}</code></dd></div><div><dt>{w('Проекция','Projection')}</dt><dd>{visible.projection.files} {w('файлов','files')} · {visible.projection.bytes} {w('байт','bytes')} · {visible.projection.omitted} {w('пропущено при проекции','omitted during projection')}</dd></div><div><dt>{w('Версия адаптера и core','Adapter and core revision')}</dt><dd><code>{visible.adapterSourceRevision??w('Не измерена','Not measured')}</code></dd></div>{visible.runtime&&<div><dt>{w('Исполненный модуль','Executed module')}</dt><dd><code>{visible.runtime.coreModule}</code> · Python {visible.runtime.pythonVersion} · <code>{visible.runtime.deployment}</code></dd></div>}</dl>
   <div className="analysis-sections"><section><h3>{w('Стек','Stack')}</h3>{evidence(visible.stack)}</section><section><h3>{w('Языки','Languages')}</h3>{evidence(visible.languages)}</section><section><h3>{w('Компоненты','Components')}</h3>{evidence(visible.components)}</section><section><h3>{w('Документы управления','Control plane')}</h3><ul>{visible.controlPlane.map(item=><li key={item.path}><code>{item.path}</code> · {item.status==='present_unverified'?w('Есть, не проверен','Present, unverified'):w('Не наблюдался','Not observed')}{item.source&&source(item.source)}</li>)}</ul></section><section><h3>{w('Кандидаты схемы БД','Database schema candidates')}</h3>{evidence(visible.schemaCandidates)}<p className="quiet">{w('Схемы и ORM определены по путям. Файлы БД не открывались; соединение и связи с кодом не проверены.','Schema and ORM signals come from paths. Database files were not opened; connections and code links are unverified.')}</p></section><section><h3>{w('Замечания','Findings')}</h3>{visible.findings.length?<ul>{visible.findings.map(item=><li key={item.code}><code>{item.code}</code></li>)}</ul>:<p className="quiet">{w('Нет наблюдений. Это не подтверждает отсутствие проблем.','No observations. This does not establish the absence of issues.')}</p>}</section></div>
   <details><summary>{w('Ограничения анализа','Analysis limitations')}</summary><ul>{visible.limitations.map(reason=><li key={reason}><code>{reason}</code></li>)}</ul></details>
  </>}
  <nav className="analysis-navigation" aria-label={w('Связанные данные проекта','Related project evidence')}><button type="button" onClick={onOpenFiles} disabled={!onOpenFiles||!projectId}>{w('Открыть файлы','Open Files')}</button><button type="button" onClick={onOpenGraph} disabled={!onOpenGraph||!projectId}>{w('Открыть граф','Open Graph')}</button><button type="button" data-testid="analysis-database" disabled={!onOpenDatabase||!projectId} onClick={onOpenDatabase}>{w('Открыть базу данных','Open Database')}</button></nav>
 </section>;
}
