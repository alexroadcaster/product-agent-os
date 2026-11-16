import {useEffect,useRef,useState} from 'react';
import {HttpApiError,type M1Api} from '../../api/client.ts';
import {createLatestRequest} from '../../api/latest-request.ts';
import type {ProjectScanView,ProjectScanStageKind,ProjectScanState,ProjectScanStageState} from '../../../../../packages/contracts/project-scan.ts';
import {mergeScanView} from './ProjectScanStatus.model.ts';
import './project-scan-status.css';

type Locale='ru'|'en';
const stageLabels:Record<ProjectScanStageKind,[string,string]>={inventory:['Файлы и исключения','Inventory and exclusions'],documents:['Документы','Documents'],code:['Код','Code'],analysis:['Анализ проекта','Project analysis'],schema:['Схема БД','Database schema'],code_database:['Код и таблицы БД','Code-to-database links']};
const stateLabels:Record<ProjectScanState|ProjectScanStageState,[string,string]>={queued:['В очереди','Queued'],running:['Выполняется','Running'],completed:['Завершено','Completed'],partial:['Частичное покрытие','Partial coverage'],cancelled:['Отменено','Cancelled'],interrupted:['Прервано; требуется повтор','Interrupted; retry required'],failed:['Ошибка','Failed'],recovery_required:['Требуется восстановление','Recovery required'],pending:['Ожидает','Pending'],unavailable:['Недоступно','Unavailable']};
const countLabels:Record<string,[string,string]>={discovered:['Найдено записей','Discovered entries'],files:['Файлы','Files'],directories:['Каталоги','Directories'],readEligible:['Допустимо читать','Read eligible'],indexEligible:['Допустимо индексировать','Index eligible'],readable:['Успешно прочитано','Successfully read'],indexed:['Индексировано','Indexed'],unsupported:['Не поддержано индексатором','Unsupported by indexer'],excluded:['Исключено','Excluded'],error:['Ошибки доступа','Access errors']};
const isActive=(state?:string)=>state==='queued'||state==='running';
const selection=(pair:[string,string],locale:Locale)=>pair[locale==='ru'?0:1];

/** Persisted scan evidence is polled only while this selected-project surface is enabled. */
export function ProjectScanStatus({api,projectId,locale,enabled=true}:{api:M1Api;projectId:string;locale:Locale;enabled?:boolean}){
 const [view,setView]=useState<ProjectScanView>(),[loading,setLoading]=useState(true),[busy,setBusy]=useState(false),[error,setError]=useState(''),[checkedAt,setCheckedAt]=useState('');
 const current=useRef<ProjectScanView|undefined>(undefined),epoch=useRef(0),active=useRef(false),actionBusy=useRef(false),refresh=useRef<(()=>void)|undefined>(undefined),pendingStart=useRef<{projectId:string;id:string}|undefined>(undefined);
 const context=useRef({projectId,enabled});context.current={projectId,enabled};
 const w=(ru:string,en:string)=>locale==='ru'?ru:en;
 const visible=view?.projectId===projectId?view:undefined,latest=visible?.latest,last=visible?.lastSuccessful;
 function publish(next:ProjectScanView,selected:string){
  const previous=current.current?.projectId===selected?current.current:undefined,merged=mergeScanView(selected,previous,next);
  if(!merged||next.projectId!==selected||next.schemaVersion!=='paos_project_scan_view_v1'){setError('SCAN_SNAPSHOT_SCOPE_MISMATCH');return;}
  if(merged===previous&&next.version>previous!.version){setError('SCAN_SNAPSHOT_REVISION_REJECTED');return;}
  current.current=merged;setView(merged);setError('');setCheckedAt(new Date().toISOString());
 }
 useEffect(()=>{
  const own=++epoch.current;let disposed=false,inFlight=false,again=false,timer:ReturnType<typeof setTimeout>|undefined;
  const requests=createLatestRequest();active.current=enabled&&Boolean(projectId);actionBusy.current=false;setBusy(false);setLoading(enabled&&Boolean(projectId));setError('');setCheckedAt('');
  if(current.current?.projectId!==projectId){current.current=undefined;setView(undefined);pendingStart.current=undefined;}
  const relevant=()=>!disposed&&epoch.current===own&&context.current.projectId===projectId&&context.current.enabled;
  async function load(){
   clearTimeout(timer);if(!relevant()||!projectId)return;if(inFlight){again=true;return;}inFlight=true;
   await requests.run(signal=>api.projectScans(projectId,signal),next=>{if(relevant())publish(next,projectId);},cause=>{if(relevant())setError(cause instanceof HttpApiError?cause.code??'PROJECT_SCAN_UNAVAILABLE':'PROJECT_SCAN_UNAVAILABLE');});
   inFlight=false;if(!relevant())return;setLoading(false);
   // One flight and one timer; refresh during a slow response is queued once.
   if(again){again=false;void load();}else timer=setTimeout(()=>void load(),2000);
  }
  refresh.current=()=>{if(relevant())void load();};if(active.current)void load();
  return()=>{disposed=true;active.current=false;epoch.current++;clearTimeout(timer);requests.dispose();refresh.current=undefined;};
 },[api,projectId,enabled]);
 async function command(action:'start'|'cancel'|'retry'){
  if(actionBusy.current||!active.current||!projectId||!enabled)return;
  const own=epoch.current,selected=projectId,scan=current.current?.projectId===selected?current.current.latest:undefined;
  if(action!=='start'&&!scan)return;
  actionBusy.current=true;setBusy(true);setError('');
  try{
   if(action==='start'&&pendingStart.current?.projectId!==selected)pendingStart.current={projectId:selected,id:crypto.randomUUID()};
   const next=action==='start'?await api.startProjectScan(selected,{requestId:pendingStart.current!.id}):action==='cancel'?await api.cancelProjectScan(selected,scan!.scanId):await api.retryProjectScan(selected,scan!.scanId);
   if(active.current&&epoch.current===own&&context.current.projectId===selected&&context.current.enabled){publish(next,selected);if(action==='start')pendingStart.current=undefined;refresh.current?.();}
  }catch(cause){if(active.current&&epoch.current===own&&context.current.projectId===selected&&context.current.enabled)setError(cause instanceof HttpApiError?cause.code??'PROJECT_SCAN_UNAVAILABLE':'PROJECT_SCAN_UNAVAILABLE');}
  finally{if(epoch.current===own){actionBusy.current=false;setBusy(false);}}
 }
 const number=(value:number|null|undefined)=>value==null?w('Не измерено','Not measured'):String(value);
 return <section className="panel project-scan-status" data-testid="project-scan-status" data-project-id={projectId} data-scan-version={visible?.version??''} data-scan-id={latest?.scanId??''} data-scan-attempt={latest?.attempt??''} aria-busy={loading||busy}>
  <header className="scan-status-heading"><div><h2>{w('Сканирование проекта','Project scanning')}</h2><p className="quiet">{w('Файлы доступны независимо от завершения анализа.','Files remain available independently of analysis completion.')}</p></div><button type="button" data-testid="scan-refresh" disabled={!enabled||!projectId||busy} onClick={()=>refresh.current?.()}>{w('Обновить статус','Refresh status')}</button></header>
  {!projectId?<p>{w('Выберите проект.','Select a project.')}</p>:<>
   {!enabled&&<p className="quiet">{w('Обновление приостановлено: раздел неактивен.','Updates paused while this surface is inactive.')}</p>}
   {loading&&!visible&&<p role="status">{w('Загрузка сохранённого состояния…','Loading saved state…')}</p>}
   {error&&<p role="alert" className="scan-status-error">{w('Не удалось получить актуальный статус. Показан последний доступный снимок; обновите или повторите действие.','Current status could not be confirmed. The last available snapshot is retained; refresh or retry.')} <code>{error}</code></p>}
   {visible&&!latest&&<p data-testid="scan-empty">{w('Сохранённого сканирования пока нет. Запустите его, когда будете готовы.','No saved scan yet. Start one when ready.')}</p>}
   {latest&&<>
    <div className="scan-status-summary"><strong data-testid="scan-state" data-state={latest.state} role="status" aria-live="polite">{selection(stateLabels[latest.state],locale)}</strong><span>{w('Попытка','Attempt')} {latest.attempt}{latest.stage?' · '+selection(stageLabels[latest.stage],locale):''}</span><time dateTime={latest.updatedAt}>{latest.updatedAt}</time></div>
    {latest.state==='partial'&&<p className="scan-status-note">{w('Часть результатов доступна. Завершённый индекс не означает полный анализ проекта.','Some results are available. A completed index does not mean complete project analysis.')}</p>}
    <div className="scan-status-counts">{Object.entries(countLabels).map(([key,label])=><div key={key}><span>{selection(label,locale)}</span><strong>{number(latest.counts?.[key as keyof NonNullable<typeof latest.counts>])}</strong></div>)}</div>
    <p className="quiet">{w('Счётчики описывают разные стадии и могут пересекаться; их нельзя складывать. Неизвестное значение не равно нулю.','Counters describe different stages and may overlap; do not add them. Unknown is not zero.')}</p>
    <ol className="scan-stage-list">{latest.stages.map(stage=><li key={stage.kind} data-scan-stage={stage.kind} data-stage-state={stage.state}>
     <header><h3>{selection(stageLabels[stage.kind],locale)}</h3><span>{selection(stateLabels[stage.state],locale)}</span></header>
     {stage.progress&&<div className="scan-stage-progress"><progress aria-label={selection(stageLabels[stage.kind],locale)} value={stage.progress.completed} max={Math.max(1,stage.progress.total)}/><span>{stage.progress.completed}/{stage.progress.total}</span></div>}
     {stage.counts&&<dl className="scan-stage-counts">{Object.entries(stage.counts).map(([key,value])=><div key={key}><dt>{countLabels[key]?selection(countLabels[key],locale):key}</dt><dd>{number(value)}</dd></div>)}</dl>}
     {stage.reasons.length>0&&<ul className="scan-status-reasons">{stage.reasons.map(reason=><li key={reason}><code>{reason}</code></li>)}</ul>}
    </li>)}</ol>
    {latest.reasons.length>0&&<details className="scan-status-details"><summary>{w('Причины неполноты или остановки','Coverage or stop reasons')}</summary><ul className="scan-status-reasons">{latest.reasons.map(reason=><li key={reason}><code>{reason}</code></li>)}</ul></details>}
    <details className="scan-status-details"><summary>{w('Источник и версия снимка','Snapshot source and version')}</summary><dl>
     <dt>scanId</dt><dd><code>{latest.scanId}</code></dd><dt>{w('Идентичность корня','Root identity')}</dt><dd><code>{latest.rootIdentity}</code></dd><dt>{w('Политика','Policy')}</dt><dd><code>{latest.policyVersion}</code></dd><dt>{w('Inventory revision','Inventory revision')}</dt><dd><code>{latest.inventoryRevision??w('Ещё не определена','Not bound yet')}</code></dd><dt>{w('Версия записи','Record version')}</dt><dd>{visible!.version}</dd>
    </dl></details>
   </>}
   <div className="scan-status-actions"><button type="button" data-testid="scan-start" disabled={!enabled||busy||loading||isActive(latest?.state)} onClick={()=>void command('start')}>{w('Сканировать проект','Scan project')}</button>{latest&&<><button type="button" data-testid="scan-cancel" disabled={!enabled||busy||!isActive(latest.state)} onClick={()=>void command('cancel')}>{w('Отменить сканирование','Cancel scan')}</button><button type="button" data-testid="scan-retry" disabled={!enabled||busy||isActive(latest.state)} onClick={()=>void command('retry')}>{w('Повторить попытку','Retry scan')}</button></>}</div>
   {last&&<aside className="scan-last-success" data-testid="scan-last-success"><strong>{w('Последнее сохранённое покрытие','Last saved coverage')}</strong><p>{selection(stateLabels[last.state],locale)} · {last.finishedAt??last.updatedAt}</p><p>{w('Файлов','Files')}: {number(last.counts?.files)} · {w('Найдено записей','Discovered entries')}: {number(last.counts?.discovered)}</p><code>{last.inventoryRevision??w('Версия неизвестна','Revision unknown')}</code></aside>}
   {visible&&<details className="scan-status-details"><summary>{w('Доступные анализаторы и ограничения','Analyzer capabilities and limits')}</summary><ul className="scan-capabilities">{Object.entries(visible.capabilities).map(([kind,available])=><li key={kind}>{selection(stageLabels[kind as ProjectScanStageKind],locale)}: {available?w('подключён','connected'):w('недоступен','unavailable')}</li>)}</ul><p>{w('Одновременно','Concurrency')}: {visible.limits.concurrency} · {w('На попытку','Per attempt')}: {visible.limits.milliseconds/1000}s · {w('На этап','Per stage')}: {visible.limits.stageMilliseconds/1000}s</p></details>}
   {checkedAt&&<p className="quiet scan-checked-at">{w('Статус проверен','Status checked')}: <time dateTime={checkedAt}>{checkedAt}</time> · {w('Без фонового выполнения команд проекта.','No background execution of project commands.')}</p>}
  </>}
 </section>;
}
