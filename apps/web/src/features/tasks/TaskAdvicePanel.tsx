import {useEffect,useState,type FormEvent} from 'react';
import {HttpApiError,type M1Api,type StoredEntity} from '../../api/client.ts';
import {createLatestRequest} from '../../api/latest-request.ts';
import type {TaskAdviceRequest,TaskAdviceView} from '../../../../../packages/contracts/project-analysis.ts';

const methods={spec_driven:'Spec-DD',design_driven:'Design-DD',tdd:'TDD',add:'ADD',fsd:'FSD'};
const methodReasonsRu={
 spec_driven:'Цель и критерии задачи требуют проверяемой спецификации.',
 design_driven:'В области задачи нет подтверждённого изменения интерфейса.',
 add:'Область задачи задана. Доступна проверка в режиме чтения.',
 fsd:'Изменение границ между frontend-функциями не обнаружено.',
};
const reasonsRu={
 TASK_ADVICE_SOURCE_NOT_OBSERVED:'Часть выбранных файлов недоступна для чтения.',
 TASK_ADVICE_BOUNDED_COVERAGE:'Часть проекта за пределами проекции.',
 TASK_ADVICE_TEST_NOT_OBSERVED:'Укажите файл теста и команду из TEST.md.',
 TASK_ADVICE_DOC_SOURCE_REQUIRED:'Укажите исходник, подтверждающий критерий документации.',
 ANALYSIS_SCAN_REQUIRED:'Запустите сканирование проекта со стадией анализа.',
 ANALYSIS_SOURCE_STALE:'Повторите сканирование проекта перед запросом совета.',
 TASK_ADVICE_TASK_SCOPE_REQUIRED:'Заполните файлы задачи и критерии приёмки.',
 TASK_ADVICE_MODE_CONFLICT:'Файлы задачи не соответствуют выбранному виду работы.',
 TASK_ADVICE_BUSY:'Анализ занят другим запросом. Повторите попытку.',
};
const reasonsEn={
 TASK_ADVICE_SOURCE_NOT_OBSERVED:'Some selected files could not be read.',
 TASK_ADVICE_BOUNDED_COVERAGE:'Some files fall outside the bounded projection.',
 TASK_ADVICE_TEST_NOT_OBSERVED:'Provide the test file and the command declared in TEST.md.',
 TASK_ADVICE_DOC_SOURCE_REQUIRED:'Provide the source for the documentation criterion.',
 ANALYSIS_SCAN_REQUIRED:'Run a project scan with the Analysis stage.',
 ANALYSIS_SOURCE_STALE:'Run a new project scan before requesting advice.',
 TASK_ADVICE_TASK_SCOPE_REQUIRED:'Provide task files and acceptance criteria.',
 TASK_ADVICE_MODE_CONFLICT:'The task files do not match the selected type of work.',
 TASK_ADVICE_BUSY:'Another advice request is running. Try again.',
};
const statusText={
 ready:['Рекомендация доступна','Advice available'],
 partial:['Частичное покрытие','Partial coverage'],
 stale:['Рекомендация устарела','Advice is stale'],
 unavailable:['Рекомендация недоступна','Advice unavailable'],
} as const;

export function TaskAdvicePanel({api,task,locale}:{api:Pick<M1Api,'taskAdvice'>;task:StoredEntity;locale:'ru'|'en'}){
 const w=(ru:string,en:string)=>locale==='ru'?ru:en;
 const [request]=useState(createLatestRequest);
 const [mode,setMode]=useState<TaskAdviceRequest['mode']>(task.data?.type==='bug'?'defect_fix':'docs_only');
 const [source,setSource]=useState(''),[testPath,setTestPath]=useState(''),[command,setCommand]=useState('');
 const [result,setResult]=useState<TaskAdviceView>(),[busy,setBusy]=useState(false),[error,setError]=useState('');
 useEffect(()=>()=>request.dispose(),[request]);
 function revise(update:()=>void){
  request.dispose();update();setResult(undefined);setError('');setBusy(false);
 }
 function submit(event:FormEvent){
  event.preventDefault();setBusy(true);setError('');setResult(undefined);
  const input:TaskAdviceRequest={taskId:task.id,taskRevision:task.revision,mode};
  if(mode==='docs_only'&&source.trim())input.sourcePath=source.trim();
  if(mode==='defect_fix'){
   if(testPath.trim())input.testPath=testPath.trim();
   if(command.trim())input.testCommand=command.trim();
  }
  void request.run(signal=>api.taskAdvice(task.projectId,input,signal),view=>{
   if(view?.schemaVersion==='paos_project_task_advice_v1'&&view.projectId===task.projectId&&view.taskId===task.id
    &&view.taskRevision===task.revision&&view.selector==='project_analysis_task_bridge'
    &&Object.hasOwn(statusText,view.status)&&Array.isArray(view.warnings)&&view.warnings.every(code=>/^[A-Z_]{1,80}$/.test(code))
    &&(!view.decision||view.decision.scope?.task_id===task.id)){
    setResult(view);
   }else setError('TASK_ADVICE_SCOPE_MISMATCH');
   setBusy(false);
  },cause=>{
   setError(cause instanceof HttpApiError?(cause.code??'TASK_ADVICE_UNAVAILABLE'):'TASK_ADVICE_UNAVAILABLE');
   setBusy(false);
  });
 }
 const advice=result&&(result.status==='ready'||result.status==='partial')?result.decision:null;
 const denied=error==='SESSION_REQUIRED'||error==='ORIGIN_REJECTED'||error==='CSRF_INVALID';
 const copy=locale==='ru'?reasonsRu:reasonsEn;
 const step=advice?.plan.next_step;
 const stepTitle=step?.kind==='run_regression'?w('Воспроизведите поведение указанным тестом','Reproduce the behavior with the named test'):
  step?.kind==='check_source'?w('Сверьте утверждение с исходником','Compare the claim with the source'):
   w('Уточните доступную проверку','Confirm the available check');
 return <details className="task-advice" data-testid="task-advice">
  <summary>{w('Рекомендация по задаче','Task recommendation')}</summary>
  <p className="quiet">{w('Режим просмотра. Команды и изменения требуют отдельного действия.','Read-only. Commands and changes require a separate action.')}</p>
  <form className="task-advice-form" onSubmit={submit}>
   <label>{w('Вид работы','Change type')}<select value={mode} onChange={event=>revise(()=>setMode(event.target.value==='defect_fix'?'defect_fix':'docs_only'))}>
    <option value="docs_only">{w('Правка документации','Documentation edit')}</option>
    <option value="defect_fix">{w('Локальная ошибка логики Python','Scoped Python logic defect')}</option>
   </select></label>
   {mode==='docs_only'?<label>{w('Путь к источнику','Source path')}<input name="advice-source" value={source} maxLength={300} onChange={event=>revise(()=>setSource(event.target.value))}/></label>:<>
    <label>{w('Путь к файлу теста','Test file path')}<input name="advice-test" value={testPath} maxLength={300} onChange={event=>revise(()=>setTestPath(event.target.value))}/></label>
    <label>{w('Команда из TEST.md','Command from TEST.md')}<input name="advice-command" value={command} maxLength={256} onChange={event=>revise(()=>setCommand(event.target.value))}/></label>
   </>}
   <button type="submit" disabled={busy}>{w('Показать рекомендацию','Show recommendation')}</button>
  </form>
  {busy&&<p role="status">{w('Проверяем данные задачи…','Checking task context…')}</p>}
  {error&&<p role="alert" className="ui-notice warning" data-testid="task-advice-error">
   {denied?w('Требуется доступ к текущему проекту.','Access to the current project is required.'):
    error==='TASK_ADVICE_TASK_STALE'?w('Версия задачи устарела. Обновите список задач.','The task revision is stale. Refresh the task list.'):
     w('Получить рекомендацию не удалось.','Advice could not be loaded.')} <code>{error}</code>
  </p>}
  {result&&<section aria-label={w('Результат рекомендации','Recommendation result')} data-testid="task-advice-result" data-state={result.status}>
   <p role="status">{statusText[result.status][locale==='ru'?0:1]}</p>
   {result.warnings.length>0&&<ul>{result.warnings.map(code=><li key={code}>{copy[code as keyof typeof copy]??<code>{code}</code>}</li>)}</ul>}
   {advice&&<><h4>{w('Следующий шаг','Next step')}</h4>
    <p>{stepTitle} {step?.target&&<code>{step.target}</code>}</p>
    {advice.plan.blocking_question&&<p>{advice.plan.blocking_question}</p>}
    <ul>{advice.decisions.map(row=><li key={row.method}><strong>{methods[row.method]}</strong> · {
     row.applicability==='applicable'?w('Применим','Applicable'):row.applicability==='needs_context'?w('Требует уточнения','Needs context'):w('Не применяется','Not applicable')
    }{row.depth!=='none'&&` · ${row.depth==='full'?w('полный','full'):w('краткий','compact')}`}<br/>
    {locale==='en'?row.reason:row.method==='tdd'?(row.applicability==='applicable'?'Найден тест для воспроизведения поведения.':
     row.applicability==='needs_context'?'Требуется подтверждённый тест изменяемого поведения.':'Для правки документации подходит сверка с исходником.'):
     methodReasonsRu[row.method]}</li>)}</ul>
    <details><summary>{w('Область и источники','Scope and sources')}</summary>
     <p>{w('Файлы задачи','Task paths')}: {advice.requirements.changed_paths.map(path=><code key={path}>{path} </code>)}</p>
     {result.sourceRevision&&<p>{w('Версия исходников','Source revision')}: <code>{result.sourceRevision}</code></p>}
     <p>{w('Прочитано файлов','Files read')}: {result.coverage.content.length} · {w('Только метаданные','Metadata only')}: {result.coverage.metadataCount} · {w('Пропущено','Omitted')}: {result.coverage.omittedCount}</p>
     <ul>{advice.evidence.filter(item=>item.kind==='file').map(item=><li key={item.id}><code>{item.path}</code></li>)}</ul>
     {advice.plan.gaps.length>0&&<ul>{advice.plan.gaps.map(gap=><li key={gap}>{gap}</li>)}</ul>}
    </details>
   </>}
  </section>}
 </details>;
}
