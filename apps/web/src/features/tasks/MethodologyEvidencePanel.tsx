import {useEffect,useRef,useState,type FormEvent} from 'react';
import {HttpApiError,type M1Api,type StoredEntity} from '../../api/client.ts';
import {createLatestRequest} from '../../api/latest-request.ts';
import type {MethodologyDecisionCommand,MethodologyDecisionView,MethodologyDisposition,MethodologyEvidenceView} from '../../../../../packages/contracts/methodology-workspace.ts';

const technical={passed:['Пройдена','Passed'],failed:['Ошибка','Failed'],partial:['Ожидает результата','Pending result'],
  missing:['Нет наблюдения','No observation'],stale:['Устарела','Stale']} as const;
const dispositions={use_recommendation:['Следовать рекомендации','Use recommendation'],review_required:['Пересмотреть план','Review the plan'],
  accepted_gap:['Принять пробел по критерию','Accept a criterion gap']} as const;

export function MethodologyEvidencePanel({api,task,locale}:{api:M1Api;task:StoredEntity;locale:'ru'|'en'}){
  const index=locale==='ru'?0:1;
  const w=(ru:string,en:string)=>locale==='ru'?ru:en;
  const [request]=useState(createLatestRequest);
  const [evidence,setEvidence]=useState<MethodologyEvidenceView>();
  const [decision,setDecision]=useState<MethodologyDecisionView>();
  const [busy,setBusy]=useState(false),[error,setError]=useState('');
  const [disposition,setDisposition]=useState<MethodologyDisposition>('review_required');
  const [criterion,setCriterion]=useState(''),[reason,setReason]=useState('');
  const pending=useRef<MethodologyDecisionCommand|null>(null);
  const {projectId,id,revision}=task;
  useEffect(()=>()=>request.dispose(),[request]);

  function load(){
    setBusy(true);setError('');setEvidence(undefined);setDecision(undefined);
    void request.run(signal=>Promise.all([api.methodologyEvidence(projectId,id,revision,signal),api.methodologyDecision(projectId,id,signal)]),
      ([facts,record])=>{
        if(facts?.schemaVersion==='paos_methodology_evidence_v1'&&record?.schemaVersion==='paos_methodology_decision_record_v1'
          &&facts.projectId===projectId&&facts.taskId===id&&record.taskId===id&&facts.taskRevision===revision&&record.taskRevision===revision){
          setEvidence(facts);setDecision(record);
        }else setError('METHODOLOGY_TASK_STALE');
        setBusy(false);
      },cause=>{setError(cause instanceof HttpApiError?cause.code??'METHODOLOGY_UNAVAILABLE':'METHODOLOGY_UNAVAILABLE');setBusy(false);});
  }

  async function save(event:FormEvent){
    event.preventDefault();
    if(!decision||busy)return;
    const input=pending.current??{expectedRevision:decision.revision,taskRevision:revision,scopeDigest:decision.scopeDigest,
      disposition,criterionId:disposition==='accepted_gap'?criterion:null,reason:reason.trim(),idempotencyKey:crypto.randomUUID()};
    pending.current=input;setBusy(true);setError('');
    try{
      const saved=await api.saveMethodologyDecision(projectId,id,input);
      if(saved.taskId!==id||saved.taskRevision!==revision)throw new Error('METHODOLOGY_TASK_STALE');
      pending.current=null;setDecision(saved);setReason('');
    }catch(cause){
      if(cause instanceof HttpApiError&&[400,404,409,422].includes(cause.status))pending.current=null;
      setError(cause instanceof HttpApiError?cause.code??'METHODOLOGY_UNAVAILABLE':'METHODOLOGY_UNAVAILABLE');
    }finally{setBusy(false);}
  }

  const latest=decision?.history.at(-1);
  return <details className="task-advice" data-testid="methodology-evidence-panel">
    <summary>{w('Доказательства и решение','Evidence and decision')}</summary>
    <button type="button" onClick={load} disabled={busy}>{evidence?w('Обновить наблюдения','Refresh observations'):w('Показать наблюдения','Show observations')}</button>
    {busy&&<p role="status">{w('Запрос выполняется…','Request in progress…')}</p>}
    {error&&<p role="alert">{w('Запрос не завершён.','Request could not be completed.')} <code>{error}</code></p>}
    {evidence&&<>
      <ul>{evidence.criteria.map(row=><li key={row.id}>
        <strong>{row.id}</strong> {row.criterion} · {technical[row.technical][index]}
        {row.receipt&&<> · <code>{row.receipt.operationId}</code></>}
        {decision?.status==='current'&&latest?.disposition==='accepted_gap'&&latest.criterionId===row.id&&<> · {w('Пробел принят владельцем','Gap accepted by owner')}</>}
      </li>)}</ul>
      <p>{w('Решение владельца о приёмке','Owner acceptance')} · {evidence.humanAcceptance==='accepted'?w('Принято','Accepted'):
        evidence.humanAcceptance==='declined'?w('Отклонено','Declined'):w('Нет наблюдения','No observation')}</p>
      {evidence.recovery&&<p role="status">{evidence.recovery.state==='reconcile_required'?
        w('Проверьте исход операции в разделе «Сессии» перед повторным запуском.','Reconcile the operation in Sessions before retrying.'):
        w('Дождитесь результата операции в разделе «Сессии».','Wait for the operation result in Sessions.')} <code>{evidence.recovery.operationId}</code></p>}
    </>}
    {decision?.status==='stale'&&<p role="status">{w('Область задачи изменилась. Пересмотрите сохранённое решение.','The task scope changed. Review the saved decision.')}</p>}
    {decision?.status==='unsupported'&&<p role="status">{w('Эта версия приложения не читает сохранённое решение.','This app version cannot read the saved decision.')}</p>}
    {latest&&<details><summary>{w('История решений','Decision history')}</summary><ol>{decision?.history.map((entry,at)=><li key={at}>
      {dispositions[entry.disposition][index]} {entry.criterionId??''} · {entry.reason}
    </li>)}</ol></details>}
    {decision&&decision.status!=='unsupported'&&<form className="task-advice-form" onSubmit={save}>
      <fieldset disabled={busy||pending.current!==null}>
        <label>{w('Решение','Decision')}<select aria-label={w('Решение','Decision')} value={disposition} onChange={event=>setDisposition(event.target.value as MethodologyDisposition)}>
          {Object.entries(dispositions).map(([value,copy])=><option key={value} value={value}>{copy[index]}</option>)}
        </select></label>
        {disposition==='accepted_gap'&&<label>{w('Критерий','Criterion')}<select aria-label={w('Критерий','Criterion')} required value={criterion} onChange={event=>setCriterion(event.target.value)}>
          <option value="">{w('Выберите критерий','Select a criterion')}</option>
          {evidence?.criteria.map(row=><option key={row.id} value={row.id}>{row.id} {row.criterion}</option>)}
        </select></label>}
        <label>{w('Причина','Reason')}<input required maxLength={800} name="methodology-decision-reason" value={reason} onChange={event=>setReason(event.target.value)}/></label>
      </fieldset>
      <button type="submit" disabled={busy}>{pending.current?w('Уточнить результат сохранения','Resolve save result'):w('Сохранить решение','Save decision')}</button>
    </form>}
  </details>;
}
