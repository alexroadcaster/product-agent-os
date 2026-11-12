import type {Execution} from '../execution-recipes/contract.mts';
import type {StoredEntity} from '../storage/local-store.mts';
import type {RecipeRecoveryView} from '../../../../packages/contracts/execution-recipes/recipe.ts';

/** Only persisted terminal evidence authorizes continuation. Lease expiry and Stop requests are not settlements. */
export function recipeCheckpoint(e:Execution,child:StoredEntity|null):RecipeRecoveryView{
 const last=e.attempts.at(-1),job=child?.data.appAgentRun as any;
 const valid=(!last?.runId||!!child)&&(!child||!!last&&child.id===last.runId&&job?.recipeExecution===e.id&&job.clientMessageId===last.clientMessageId
  &&job.bindingId===e.bindingId&&child.status===job.state);
 const settled=valid&&!!child&&['completed','failed','interrupted'].includes(child.status)
  &&!(job.operations??[]).some((op:any)=>['dispatching','recovery_required','awaiting_approval'].includes(op.state));
 const checkpoint=!valid?'unresolved':!last?'not_dispatched':child&&!settled?'unresolved'
  :['completed','failed'].includes(last.state)?'processed':settled&&['completed','failed'].includes(child!.status)&&!job.autonomyStopReason?'terminal_result'
  :settled?'interrupted':last.admissionRejected&&!last.runId?'rejected_admission':'unresolved';
 return {checkpoint,canResume:['paused','recovery_required'].includes(e.state)&&['not_dispatched','processed','terminal_result'].includes(checkpoint),
  canCancel:checkpoint!=='unresolved',runId:last?.runId??null,childState:child?.status??null};
}
