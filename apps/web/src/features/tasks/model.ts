import type {StoredEntity} from '../../api/client.ts';
import type {IssueLink,M2TaskProfile} from '../../../../../packages/contracts/issues/task-profile.ts';
export type {M2TaskProfile,IssueLink};
export const issueTypes=['epic','task','bug','user_story','sub_task'] as const;
export const taskStatuses=['backlog','ready','in_progress','review','verification','awaiting_acceptance','done','cancelled'] as const;
export const priorities=['highest','high','medium','low','lowest'] as const;
export const fileOperations=['create','modify','delete','rename','read','create_or_modify_after_discovery'] as const;
export type View={view:'list'|'board';query:string;type:string;parent:string;epic:string;agent:string;creator:string;priority:string;component:string;cardFields:string[];
  affectsVersion:string;fixVersion:string;startAfter:string;dueBefore:string;blocked:boolean;hideCancelled:boolean;group:'none'|'type'|'parent'|'status'|'priority';sort:'rank'|'title'|'dueDate'|'priority'};
export const defaultView:View={view:'list',query:'',type:'',parent:'',epic:'',agent:'',creator:'',priority:'',component:'',cardFields:['priority','components','dueDate','estimate','children','agents','blocked'],affectsVersion:'',fixVersion:'',startAfter:'',dueBefore:'',blocked:false,hideCancelled:false,group:'none',sort:'rank'};
export function readView(value:unknown):View{
  const raw=value&&typeof value==='object'?value as Record<string,unknown>:{};
  const view={...defaultView};
  for(const key of Object.keys(defaultView) as (keyof View)[]){if(typeof raw[key]===typeof defaultView[key])(view as unknown as Record<string,unknown>)[key]=raw[key];}
  if(!['list','board'].includes(view.view))view.view='list';
  if(!['none','type','parent','status','priority'].includes(view.group))view.group='none';
  if(!['rank','title','dueDate','priority'].includes(view.sort))view.sort='rank';
  if(!Array.isArray(view.cardFields)||view.cardFields.some(v=>typeof v!=='string'))view.cardFields=[...defaultView.cardFields];
  return view;
}
export const profile=(entity:StoredEntity)=>entity.data as unknown as M2TaskProfile;
export const isM2=(entity:StoredEntity)=>entity.data?.schemaVersion==='m2_task_profile_v1';
export function draftTask(projectId:string,id=crypto.randomUUID()):M2TaskProfile{
  return {schemaVersion:'m2_task_profile_v1',type:'task',projectId,id,key:'',legacyAlias:null,title:'',summary:'',technicalValue:'',productValue:'',
    files:[],agentAssignments:[],artifactReferences:[],acceptanceCriteria:[],estimateSeconds:null,actual:{startedAt:null,endedAt:null,durationSeconds:null},risks:[],
    status:'backlog',creator:{kind:'user',actorId:'local-user'},priority:'medium',startDate:null,dueDate:null,links:[],sessionIds:[],provenance:null,
    parentId:null,initiatedBy:null,createdAt:null,timezone:'Europe/Moscow',components:[],affectsVersions:[],fixVersions:[],rank:0,resolution:null,blocker:null,
    criteriaEvidence:[],assignments:[],artifacts:[],fileContexts:[],scopeExclusions:[],workflow:{id:'default',version:1},hotfixReason:null};
}
export function isBlocked(task:StoredEntity,tasks:StoredEntity[],links:IssueLink[]):boolean{
  return Boolean(task.data?.blocker)||links.some(l=>l.relation==='blocks'&&l.targetId===task.id&&l.state!=='pending'&&!l.waiver&&tasks.find(t=>t.id===l.sourceId)?.status!=='done');
}
/** Filters consume one complete service snapshot; no first-page-only hierarchy or count. */
export function selectTasks(tasks:StoredEntity[],view:View,links:IssueLink[]):StoredEntity[]{
  const byId=new Map(tasks.map(t=>[t.id,t]));
  const blockers=new Set(links.filter(l=>l.relation==='blocks'&&l.state!=='pending'&&!l.waiver&&byId.get(l.sourceId)?.status!=='done').map(l=>l.targetId));
  return tasks.filter(t=>{
    const p=t.data??{};
    if(view.query&&!`${t.publicKey??''} ${t.title??''} ${p.summary??''}`.toLocaleLowerCase().includes(view.query.toLocaleLowerCase()))return false;
    if(view.type&&(p.type==='Task'?'task':p.type)!==view.type)return false;
    if(view.parent&&p.parentId!==view.parent)return false;
    if(view.epic){let parent=p.parentId as string|undefined;const visited=new Set<string>();let found=false;while(parent&&!visited.has(parent)){visited.add(parent);if(parent===view.epic){found=true;break;}parent=byId.get(parent)?.data?.parentId as string|undefined;}if(!found&&t.id!==view.epic)return false;}
    if(view.priority&&p.priority!==view.priority)return false;
    if(view.component&&!(p.components as string[]|undefined)?.includes(view.component))return false;
    if(view.affectsVersion&&!(p.affectsVersions as string[]|undefined)?.includes(view.affectsVersion))return false;
    if(view.fixVersion&&!(p.fixVersions as string[]|undefined)?.includes(view.fixVersion))return false;
    if(view.creator&&!(String((p.creator as {actorId?:string}|undefined)?.actorId??'').toLowerCase().includes(view.creator.toLowerCase())))return false;
    if(view.agent&&!JSON.stringify([p.agentAssignments,p.assignments]).toLowerCase().includes(view.agent.toLowerCase()))return false;
    if(view.startAfter&&(!p.startDate||String(p.startDate)<view.startAfter))return false;
    if(view.dueBefore&&(!p.dueDate||String(p.dueDate)>view.dueBefore))return false;
    if(view.blocked&&!p.blocker&&!blockers.has(t.id))return false;
    return !view.hideCancelled||t.status!=='cancelled';
  }).sort((a,b)=>{
    const pa=a.data??{},pb=b.data??{};
    if(view.sort==='title')return String(a.title).localeCompare(String(b.title));
    if(view.sort==='priority')return priorities.indexOf(pa.priority as typeof priorities[number])-priorities.indexOf(pb.priority as typeof priorities[number]);
    if(view.sort==='dueDate')return String(pa.dueDate??'9999').localeCompare(String(pb.dueDate??'9999'));
    return Number(pa.rank??0)-Number(pb.rank??0)||String(a.publicKey??a.id).localeCompare(String(b.publicKey??b.id),undefined,{numeric:true});
  });
}
export function durationText(value:unknown):string{
  if(typeof value!=='number'||!Number.isFinite(value)||value<0)return '—';
  const n=Math.floor(value);return `${String(Math.floor(n/3600)).padStart(2,'0')}:${String(Math.floor(n/60)%60).padStart(2,'0')}:${String(n%60).padStart(2,'0')}`;
}
export function parseDuration(value:string):number|null{
  if(!value.trim())return null;
  if(!/^\d+:\d{2}:\d{2}$/.test(value))throw new Error('ESTIMATE_FORMAT');
  const [h,m,s]=value.split(':').map(Number);if(m>59||s>59||!Number.isSafeInteger(h*3600+m*60+s))throw new Error('ESTIMATE_FORMAT');
  return h*3600+m*60+s;
}
export function safeExternalUrl(value:string):string|null{
  try{const url=new URL(value);return ['http:','https:'].includes(url.protocol)&&!url.username&&!url.password?url.href:null;}catch{return null;}
}
export function targetStatuses(status:string):string[]{return ({backlog:['ready','cancelled'],ready:['backlog','in_progress','cancelled'],in_progress:['review','cancelled'],review:['in_progress','verification','cancelled'],verification:['in_progress','awaiting_acceptance','cancelled'],awaiting_acceptance:['in_progress','done','cancelled'],done:['ready'],cancelled:['backlog']} as Record<string,string[]>)[status]??[];}
export const lines=(value:string)=>value.split('\n').map(s=>s.trim()).filter(Boolean);
export function hierarchyStats(tasks:StoredEntity[],taskId:string){
  const children=new Map<string,StoredEntity[]>();for(const task of tasks){const parent=task.data?.parentId;if(typeof parent==='string')children.set(parent,[...(children.get(parent)??[]),task]);}
  const visited=new Set<string>([taskId]),descendants:StoredEntity[]=[],queue=[...(children.get(taskId)??[])];
  for(let i=0;i<queue.length;i++){const task=queue[i];if(visited.has(task.id))continue;visited.add(task.id);descendants.push(task);queue.push(...(children.get(task.id)??[]));}
  const actual=descendants.map(task=>(task.data?.actual as {durationSeconds?:number|null}|undefined)?.durationSeconds);
  return {descendants:descendants.length,done:descendants.filter(t=>t.status==='done').length,cancelled:descendants.filter(t=>t.status==='cancelled').length,
    estimateSeconds:descendants.reduce((sum,t)=>sum+Number(t.data?.estimateSeconds??0),0),unknownEstimates:descendants.filter(t=>t.data?.estimateSeconds==null).length,
    actualSeconds:actual.length&&actual.every(value=>typeof value==='number')?actual.reduce<number>((sum,value)=>sum+Number(value),0):null,
    ownEstimateSeconds:tasks.find(t=>t.id===taskId)?.data?.estimateSeconds??null};
}
export function dueState(date:string|null,timezone:string):boolean{
  if(!date)return false;try{const parts=new Intl.DateTimeFormat('en-CA',{timeZone:timezone,year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts();const get=(type:string)=>parts.find(p=>p.type===type)?.value??'';return `${get('year')}-${get('month')}-${get('day')}`>date;}catch{return false;}
}
