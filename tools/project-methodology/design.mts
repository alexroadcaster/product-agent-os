import {normaliseRelativePath} from '../../apps/local-service/src/project-inventory/service.mts';

const states=['loading','empty','error','dirty'] as const;
const modes=['synthetic','current','unavailable'] as const;
type State=typeof states[number];
type Mode=typeof modes[number];
const text=(value:unknown):value is string=>typeof value==='string'&&value.trim().length>0&&value.length<=400&&!/\x00/.test(value);
type Step={action:string;expected:string;role:string;accessibleName:string};
type Journey={
 surface:'frontend'|'backend'|'native',
 taskId:string;goal:string;sourceRevision:string;
 extent:'localized'|'substantial';apiEvidence:Mode;
 designRefs:string[];dataSource:string;steps:Step[];
 stateMatrix:Record<State,{expected:string;source:Mode}>,
 accessibility:{entryFocus:string;exitFocus:string;keyboard:string};
 owners:{design:string;implementation:string;acceptance:string};
 available:{component:boolean;browser:boolean;visual:boolean;keyboard:boolean;browserAuthorized:boolean};
 hypothesis?:string;userObservation?:{kind:'representative_user';reference:string};
};
type CheckStatus='planned'|'gap';
const object=(value:unknown,keys:string[]):value is Record<string,unknown>=>Boolean(value)&&typeof value==='object'&&!Array.isArray(value)&&Object.keys(value!).every(k=>keys.includes(k));
const sha=/^[a-f0-9]{64}$/;
const invalid=():never=>{throw Error('DESIGN_CONTEXT_INVALID');};
const names=['component','browser','visual','keyboard'] as const;

export function planJourney(value:unknown,observedPaths:ReadonlySet<string>){
 if(!object(value,['surface','taskId','goal','sourceRevision','extent','apiEvidence','designRefs','dataSource','steps','stateMatrix','accessibility','owners','available','hypothesis','userObservation']))return invalid();
 if(!text(value.taskId)||!['frontend','backend','native'].includes(String(value.surface)))return invalid();
 if(value.surface!=='frontend')return {schemaVersion:'paos_design_journey_v1',taskId:value.taskId,status:'not_applicable',authority:'read_only'};
 const input=value as unknown as Journey;
 if(!text(input.goal)||typeof input.sourceRevision!=='string'||!sha.test(input.sourceRevision)
  ||!['localized','substantial'].includes(input.extent)||!modes.includes(input.apiEvidence)||!text(input.dataSource)
  ||!Array.isArray(input.designRefs)||input.designRefs.length>20
  ||!input.designRefs.every(ref=>text(ref)&&normaliseRelativePath(ref)===ref)
  ||!Array.isArray(input.steps)||!input.steps.length||input.steps.length>12
  ||!input.steps.every(step=>object(step,['action','expected','role','accessibleName'])&&
   (['action','expected','role','accessibleName'] as const).every(key=>text(step[key])))
  ||!object(input.stateMatrix,[...states])||!object(input.accessibility,['entryFocus','exitFocus','keyboard'])
  ||!['entryFocus','exitFocus','keyboard'].every(key=>text((input.accessibility as Record<string,unknown>)[key]))
  ||!object(input.owners,['design','implementation','acceptance'])||!['design','implementation','acceptance'].every(key=>text((input.owners as Record<string,unknown>)[key]))
  ||!object(input.available,[...names,'browserAuthorized'])||![...names,'browserAuthorized'].every(key=>typeof (input.available as Record<string,unknown>)[key]==='boolean')
  ||input.hypothesis!==undefined&&!text(input.hypothesis)
  ||input.userObservation!==undefined&&(!object(input.userObservation,['kind','reference'])||input.userObservation.kind!=='representative_user'||!text(input.userObservation.reference)))return invalid();
 const gaps:string[]=[];
 const matrix=states.map(state=>{
  const item=input.stateMatrix[state];
  if(item===undefined){gaps.push('STATE_NOT_SPECIFIED:'+state);return {state,status:'proposed',expected:null,source:'unavailable'};}
  if(!object(item,['expected','source'])||!text(item.expected)||!modes.includes(item.source))return invalid();
  if(item.source==='current'&&input.apiEvidence!=='current'){
   gaps.push('API_EVIDENCE_INSUFFICIENT:'+state);
   return {state,status:'proposed',expected:item.expected,source:'unavailable'};
  }
  return {state,status:'specified',...item};
 });
 const reference=(ref:string)=>observedPaths.has(ref);
 const reused=input.designRefs.filter(reference);
 if(!reused.length)gaps.push('DESIGN_SYSTEM_REFERENCE_UNOBSERVED');
 for(const ref of input.designRefs)if(!reference(ref))gaps.push('DESIGN_REFERENCE_UNOBSERVED:'+ref);
 if(input.extent==='substantial'&&!input.hypothesis)gaps.push('PROBLEM_HYPOTHESIS_REQUIRED');
 if(input.extent==='substantial'&&!input.userObservation)gaps.push('HUMAN_OBSERVATION_REQUIRED');
 const checks=names.map(kind=>{
  const unavailable=!input.available[kind]||(kind!=='component'&&(!input.available.browser||!input.available.browserAuthorized));
  if(unavailable)gaps.push('CHECK_UNAVAILABLE:'+kind);
  return {kind,status:(unavailable?'gap':'planned') as CheckStatus,
   next:unavailable?'Record unavailable evidence and use the available component or source checks':'Review the current build against the journey contract'};
 });
 return {
  schemaVersion:'paos_design_journey_v1',authority:'read_only',status:gaps.length?'partial':'proposed',
  taskId:input.taskId,goal:input.goal,sourceRevision:input.sourceRevision,steps:input.steps,
  data:{source:input.dataSource,evidence:input.apiEvidence},stateMatrix:matrix,reusedDesignRefs:reused,
  accessibility:input.accessibility,owners:input.owners,hypothesis:input.hypothesis??null,
  humanAcceptance:'not_observed',userObservation:input.userObservation??null,checks,gaps,
  verification:{viewports:[400,1360],themes:['light','dark'],longContent:true,
   requiredProvenance:['sourceRevision','buildHashes','harnessHash','browserVersion'],
   baselineUpdate:'reviewed diff with design owner before replacing expected composition'},
 };
}

export type CompositionRegion={name:string;top:number;bottom:number;left:number;right:number};
/** Compare visible semantic regions in layout order; overflow alone is insufficient. */
export function compositionFindings(expected:string[],actual:CompositionRegion[],viewportWidth:number):string[]{
 const problems:string[]=[];
 if(expected.join('\0')!==actual.map(region=>region.name).join('\0'))problems.push('REGION_ORDER_MISMATCH');
 for(const [index,region] of actual.entries()){
  if(![region.top,region.bottom,region.left,region.right].every(Number.isFinite)||region.bottom<=region.top||region.right<=region.left)
   problems.push('REGION_NOT_VISIBLE:'+region.name);
  if(region.left < -1||region.right > viewportWidth+1)problems.push('REGION_OUTSIDE_VIEWPORT:'+region.name);
  if(index>0&&region.top<actual[index-1].bottom-1)problems.push('REGION_OVERLAP:'+region.name);
 }
 return problems;
}
