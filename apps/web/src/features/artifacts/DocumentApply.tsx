import {useEffect,useRef,useState} from 'react';
import {HttpApiError,type M1Api} from '../../api/client.ts';
import type {ArtifactDocument} from '../../../../../packages/contracts/artifacts/catalog.ts';
import type {DocumentApplyPreview,DocumentApplyInput} from '../../../../../packages/contracts/artifacts/document-apply.ts';
import type {UiLocale as Locale} from '../../locales/messages.ts';

/** Explicit exact-document writes. A lost ACK keeps its immutable request; a known rejection requires a fresh preview. */
export function DocumentApply({api,projectId,document,locale,onChanged}:{api:M1Api;projectId:string;document:ArtifactDocument;locale:Locale;onChanged:()=>Promise<void>}){
 const w=(ru:string,en:string)=>locale==='ru'?ru:en,state=document.proposal?.state;
 const [plan,setPlan]=useState<{preview:DocumentApplyPreview;epoch:number}>(),[ack,setAck]=useState(false),[busy,setBusy]=useState(false),[error,setError]=useState(''),[notice,setNotice]=useState('');
 const sequence=useRef(0),pending=useRef<{action:'apply'|'rollback';input:DocumentApplyInput}|undefined>(undefined);
 useEffect(()=>{sequence.current++;setPlan(undefined);setAck(false);setBusy(false);setError('');pending.current=undefined;return()=>{sequence.current++;};},[api,projectId,document.item.id,document.item.source.version]);
 async function perform(fn:(ticket:number)=>Promise<void>){const ticket=++sequence.current;setBusy(true);setError('');setNotice('');try{await fn(ticket);}catch(e){if(ticket===sequence.current)setError(e instanceof HttpApiError?e.code??e.message:String(e));}finally{if(ticket===sequence.current)setBusy(false);}}
 async function preview(action:'apply'|'rollback'){
  const revision=Number(document.item.source.version.replace(/^entity:/,''));if(!Number.isSafeInteger(revision)||revision<1)return;
  await perform(async ticket=>{const [project,value]=await Promise.all([api.project(projectId),api.documentApplyPreview(projectId,{proposalId:document.item.id,proposalRevision:revision},action)]);if(ticket===sequence.current){setPlan({preview:value,epoch:project.authorityEpoch});setAck(false);}});
 }
 async function apply(){await perform(async ticket=>{
  if(!pending.current){if(!plan||!ack)return;pending.current={action:plan.preview.action,input:{proposalId:plan.preview.proposalId,proposalRevision:plan.preview.proposalRevision,previewDigest:plan.preview.previewDigest,epoch:plan.epoch,idempotencyKey:crypto.randomUUID()}};}
  const request=pending.current;let result;
  try{result=await api.documentApply(projectId,request.input,request.action);}catch(e){if(e instanceof HttpApiError&&[400,404,409,422].includes(e.status)){pending.current=undefined;setPlan(undefined);setAck(false);}throw e;}
  if(ticket!==sequence.current)return;pending.current=undefined;setPlan(undefined);setAck(false);setNotice(result.state);await onChanged();
 });}
 async function recover(){await perform(async ticket=>{const operationId=(document.proposal?.operation??document.proposal?.apply)?.operationId;if(!operationId)return;const project=await api.project(projectId),result=await api.documentRecover(projectId,{proposalId:document.item.id,operationId,epoch:project.authorityEpoch});if(ticket===sequence.current){setNotice(result.state);await onChanged();}});}
 return <section className="panel" data-testid="document-apply-controls"><h3>{w('Применение предложения','Apply proposal')}</h3>
  <p>{w('Применение меняет проверенный источник. Приёмка владельцем фиксируется отдельно.','Apply changes the checked source. Owner acceptance is recorded separately.')}</p>
  {error&&<p role="alert">{error}</p>}{notice&&<p role="status">{notice}</p>}
  {['staged','not_applied'].includes(state??'')&&<button disabled={busy||Boolean(pending.current)} onClick={()=>void preview('apply')}>{w('Предпросмотр применения','Preview apply')}</button>}
  {state==='applied'&&<button disabled={busy||Boolean(pending.current)} onClick={()=>void preview('rollback')}>{w('Предпросмотр отката','Preview rollback')}</button>}
  {state==='stale'&&<p>{w('Источник изменился. Обновите исходный документ и создайте новое предложение.','The source changed. Refresh the original document and create a new proposal.')}</p>}
  {['prepared','recovery_required'].includes(state??'')&&<><p>{w('Исход записи требует сверки. Автоматическое повторное применение отключено.','The write outcome needs reconciliation. Automatic replay is disabled.')}</p><button disabled={busy} onClick={()=>void recover()}>{w('Сверить исход записи','Reconcile write outcome')}</button></>}
  {pending.current&&<button disabled={busy} onClick={()=>void apply()}>{w('Повторить запрос с прежним ключом','Retry the same request')}</button>}
  {plan&&<section data-testid="document-write-preview"><p>{w('Будет изменён','Will change')}: {plan.preview.source.origin==='workspace_file'?plan.preview.source.path:w('Документ PAOS','PAOS document')+' · '+plan.preview.source.entityId}</p><div className="m2-fields"><pre className="diff">{plan.preview.before}</pre><pre className="diff">{plan.preview.after}</pre></div><p>{w('Локальный журнал восстановления хранит до четырёх операций. Файловая запись защищена от конкурирующего доступа; при неизвестном исходе потребуется сверка.','The local recovery journal retains up to four operations. File writes exclude concurrent access; an unknown outcome requires reconciliation.')}</p><label><input name="document-write-ack" type="checkbox" checked={ack} onChange={e=>setAck(e.target.checked)}/>{w('Проверил источник и изменения; разрешаю эту запись','I reviewed the source and changes and authorize this write')}</label><button disabled={busy||!ack} onClick={()=>void apply()}>{plan.preview.action==='apply'?w('Применить к источнику','Apply to source'):w('Откатить проверенную версию','Roll back reviewed version')}</button></section>}
 </section>;
}
