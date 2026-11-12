import {useEffect,useRef,useState} from 'react';
import type {M1Api,StoredEntity} from '../../api/client.ts';
import type {UiLocale} from '../../locales/messages.ts';
import {defaultAutonomyPolicy,type AutonomyPolicy,type AutonomyPreview,type AutonomySnapshot} from '../../../../../packages/contracts/autonomy/policy.ts';

/** Policy proposals never start work. Every mutation uses the last observed revision. */
export function AutonomyManager({api,projectId,locale}:{api:M1Api;projectId:string;locale:UiLocale}) {
 const w=(ru:string,en:string)=>locale==='ru'?ru:en;
 const [snapshot,setSnapshot]=useState<AutonomySnapshot|null>(null),[tasks,setTasks]=useState<StoredEntity[]>([]);
 const [draft,setDraft]=useState<AutonomyPolicy>(defaultAutonomyPolicy),[preview,setPreview]=useState<AutonomyPreview|null>(null);
 const [busy,setBusy]=useState(false),[loading,setLoading]=useState(true),[error,setError]=useState(''),[notice,setNotice]=useState(''),[dirty,setDirty]=useState(false);
 const [interrupts,setInterrupts]=useState<{runId:string;status:string;reason?:string}[]>([]);
 const alive=useRef(true);
 useEffect(()=>{alive.current=true;let ignore=false;void Promise.all([api.autonomy(projectId),api.taskManager(projectId)]).then(([state,manager])=>{
  if(ignore)return;setSnapshot(state);setDraft(state.policy??defaultAutonomyPolicy());setTasks(manager.tasks);
 }).catch(e=>{if(!ignore)setError(String(e));}).finally(()=>{if(!ignore)setLoading(false);});return()=>{ignore=true;alive.current=false;};},[api,projectId]);
 function patch(change:Partial<AutonomyPolicy>){setDraft(current=>({...current,...change}));setDirty(true);setPreview(null);setNotice('');}
 // Refresh and CAS failures preserve the edited policy; only a fresh preview permits saving it.
 async function act(action:'preview'|'save'|'pause'|'resume'|'refresh') {
  if(busy||!snapshot&&action!=='refresh')return;setBusy(true);setError('');setNotice('');
  try {
   if(action==='refresh') {const [state,manager]=await Promise.all([api.autonomy(projectId),api.taskManager(projectId)]);if(alive.current){setSnapshot(state);setTasks(manager.tasks);setPreview(null);}}
   else if(action==='preview'){const value=await api.autonomyPreview(projectId,{policy:draft,expectedRevision:snapshot!.revision});if(alive.current)setPreview(value);}
   else {
    if(action==='save'&&!preview?.executable)return;
    const project=await api.project(projectId);
    const value=await api.autonomyAction(projectId,action,{expectedRevision:snapshot!.revision,expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:crypto.randomUUID(),
     ...(action==='save'?{policy:draft,previewDigest:preview!.previewDigest}:{})});
    if(alive.current)setInterrupts(value.interrupts??[]);
    if(alive.current){setSnapshot(value);setPreview(null);if(action==='save')setDirty(false);setNotice(action==='save'?w('Политика сохранена на паузе. Разрешите новые запуски отдельно.','Policy saved paused. Enable new runs separately.'):action==='pause'?(value.paused?w('Новые запуски заблокированы. Остановка текущих запусков требует подтверждения runtime.','New runs are blocked. Current runs need runtime stop acknowledgement.'):w('Повтор старого запроса не меняет текущий допуск.','Retrying an old request does not change current admission.')):w('Допуск новых запусков включён. Очередь не запускается и работа не повторяется.','New run admission enabled. No queue is started and no work is replayed.'));}
   }
  }catch(e){if(alive.current){setError(String(e));setPreview(null);}}
  finally{if(alive.current)setBusy(false);}
 }
 const commands=draft.allowedActions.includes('command');
 return <section className="panel" data-testid="autonomy-manager"><h2>{w('Автономная работа','Autonomous work')}</h2>
  <p>{w('Задайте границы запусков, затем включите допуск. Каждый запуск выбирается явно в сессии.','Set run boundaries, then enable admission. Each run is explicitly selected in its session.')}</p>
  {loading&&<p role="status">{w('Загрузка…','Loading…')}</p>}
  {error&&<p role="alert">{w('Операция недоступна. Черновик сохранён в форме.','Operation unavailable. Your draft remains in the form.')} {error}</p>}
  {notice&&<p role="status">{notice}</p>}
  {interrupts.length>0&&<ul aria-label={w('Запросы остановки','Stop requests')}>{interrupts.map(item=><li key={item.runId}>{item.runId}: {item.status==='stop_requested'?w('Остановка запрошена','Stop requested'):w('Нужна сверка с runtime','Runtime reconciliation required')}{item.reason?` (${item.reason})`:''}</li>)}</ul>}
  <button disabled={busy||loading} onClick={()=>void act('refresh')}>{w('Обновить состояние, сохранив черновик','Refresh state, keeping draft')}</button>
  {snapshot&&<>
   <p role="status">{!snapshot.policy?w('Политика не настроена','No policy configured'):snapshot.paused?w('На паузе','Paused'):w('Допуск включён','Admission enabled')} · {w('Запусков использовано','Runs used')}: {snapshot.usedRuns}/{snapshot.policy?.maxRuns??0}</p>
   <div className="actions"><button disabled={busy||snapshot.paused} onClick={()=>void act('pause')}>{w('Пауза','Pause')}</button><button disabled={busy||dirty||!snapshot.paused||!snapshot.policy||snapshot.usedRuns>=snapshot.policy.maxRuns} onClick={()=>void act('resume')}>{w('Разрешить новые запуски','Enable new runs')}</button></div>
   <form onSubmit={e=>{e.preventDefault();void act('preview');}}><fieldset disabled={busy||loading}><legend>{w('Предложение политики','Policy proposal')}</legend>
    {dirty&&<p role="status">{w('Есть несохранённые изменения','Unsaved changes')}</p>}
    <label>{w('Разрешённые задачи','Allowed tasks')}<select name="autonomy-tasks" multiple value={[...draft.allowedTaskIds]} onChange={e=>patch({allowedTaskIds:Array.from(e.target.selectedOptions,o=>o.value)})}>
     {tasks.filter(task=>task.data?.type!=='epic').map(task=><option key={task.id} value={task.id}>{task.publicKey??task.id}: {task.title??String(task.data?.title??'')}</option>)}
    </select></label>{!tasks.length&&<p>{w('В проекте нет задач для выбора.','No tasks available in this project.')}</p>}
    <label>{w('Разрешённые пути, по одному на строку; точка — весь workspace','Allowed paths, one per line; dot means the whole workspace')}<textarea name="autonomy-paths" value={draft.allowedPaths.join('\n')} onChange={e=>patch({allowedPaths:e.target.value.split('\n')})}/></label>
    <label className="m2-check"><input name="autonomy-commands" type="checkbox" checked={commands} onChange={e=>patch({allowedActions:e.target.checked?['execution','command']:['execution'],maxCommandsPerRun:e.target.checked?1:0})}/>{w('Разрешить команды с отдельным подтверждением','Allow commands with separate approval')}</label>
    <div className="m2-fields">{(['maxRuns','maxCommandsPerRun','maxRunSeconds'] as const).map(key=><label key={key}>{key==='maxRuns'?w('Максимум запусков','Maximum runs'):key==='maxCommandsPerRun'?w('Команд на запуск','Commands per run'):w('Лимит запуска, секунды','Run limit, seconds')}<input name={'autonomy-'+key} type="number" step="1" min={key==='maxCommandsPerRun'?0:1} max={key==='maxRuns'?1000:key==='maxRunSeconds'?3600:64} disabled={key==='maxCommandsPerRun'&&!commands} value={draft[key]} onChange={e=>patch({[key]:Number(e.target.value)})}/></label>)}</div>
    <p>{w('Одновременно — один запуск.','One run at a time.')}</p>
    <label className="m2-check"><input type="checkbox" name="autonomy-stop-on-failure" checked={draft.stopOnFailedCommand} onChange={e=>patch({stopOnFailedCommand:e.target.checked})}/>{w('Остановить текущий запуск после ошибки команды','Stop the current run after a failed command')}</label>
    <button className="primary" disabled={busy||!draft.allowedTaskIds.length}>{w('Предпросмотр политики','Preview policy')}</button>
   </fieldset></form>
   <aside><h3>{w('Границы выполнения','Execution boundaries')}</h3><ul>
    <li>{w('Выполнение по политике доступно через Codex App. Для другого runtime маршрут недоступен.','Execution under policy is available through Codex App. Other runtime routes are unavailable.')}</li>
    <li>{w('Политика ограничивает только работу через PAOS. Собственные tools Codex App не ограничиваются; host permissions не меняются.','Policy limits PAOS-mediated work only. Codex App host tools are not constrained; host permissions do not change.')}</li>
    <li>{w('Команды по-прежнему требуют отдельного подтверждения.','Commands still require separate approval.')}</li>
    <li>{w('Изоляция отдельных файлов недоступна. Выполнимый scope — весь workspace; узкие пути блокируют включение.','Per-file isolation is unavailable. Executable scope is the entire workspace; narrow paths block enabling.')}</li>
    <li>{w('Расход токенов и стоимость не измеряются. Пауза и истечение времени запрашивают остановку, но не доказывают её завершение.','Token usage and cost are not metered. Pause and timeout request a stop but do not prove it has completed.')}</li>
   </ul></aside>
   {preview&&<section data-testid="autonomy-preview"><h3>{w('Предпросмотр','Preview')}</h3><p>{preview.executable?w('Политика доступна для сохранения на паузе','Policy can be saved paused'):w('Политика не может выполняться','Policy cannot execute')}</p>{preview.reasons.length>0&&<ul>{preview.reasons.map(reason=><li key={reason}>{reason}</li>)}</ul>}<button disabled={busy||!preview.executable} onClick={()=>void act('save')}>{w('Сохранить на паузе','Save paused')}</button></section>}
   <h3>{w('Учтённые запуски','Reserved runs')}</h3>{!snapshot.runs.length?<p>{w('Запусков ещё нет.','No runs yet.')}</p>:<ul>{snapshot.runs.map(run=><li key={run.runId}>{tasks.find(task=>task.id===run.taskId)?.publicKey??run.taskId} · {run.operationIds.length} {w('команд','commands')} · {run.stopReason??w('Причина остановки не зафиксирована','No stop reason recorded')}</li>)}</ul>}
  </>}
 </section>;
}
