import {useId} from 'react';
import {capabilityLabel,type CapabilityState} from './capability.ts';

/** A local explanation, not an approval control. Existing actions retain their authority checks. */
export function CapabilityNotice({state,locale,scope,reason,next,observedAt,testId}:{state:CapabilityState;locale:'ru'|'en';scope:string;reason:string;next:string;observedAt?:string;testId:string}){
 const id=useId(),ru=locale==='ru';
 return <aside className="ui-notice" role="note" aria-labelledby={id} data-testid={testId} data-capability-state={state}>
  <strong id={id}>{capabilityLabel(state,locale)}</strong>
  <p>{ru?'Область: ':'Scope: '}{scope}. {reason}</p>
  {observedAt&&<p>{ru?'Наблюдалось: ':'Observed: '}<time dateTime={observedAt}>{observedAt}</time></p>}
  <p>{ru?'Следующий шаг: ':'Next step: '}{next}</p>
 </aside>;
}
