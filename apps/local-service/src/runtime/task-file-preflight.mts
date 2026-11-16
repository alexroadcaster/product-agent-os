import type {LocalStore} from '../storage/local-store.mts';
import {decodeTaskProfile} from '../../../../packages/contracts/issues/task-profile.ts';
import {normaliseRelativePath} from '../project-inventory/service.mts';
import {preflightTaskFiles} from './app-agent-files.mts';
import type {FilePreflight} from '../../../../packages/contracts/runtime/file-preflight.ts';
import {inventoryScopeFingerprint} from '../project-inventory/scope.mts';

function fail(code:string):never{throw Object.assign(new Error(code),{code});}
/** Stable semantic scope, including policy, across awaited file/dependency checks. */
export const fileScopeFingerprint=inventoryScopeFingerprint;
/** Registry and saved task own scope; client paths and limits are never accepted here. */
export async function taskFilePreflight(store:LocalStore,projectId:string,taskId:string,expectedRevision?:number){
 const project=await store.project(projectId);if(!project)fail('PROJECT_NOT_FOUND');
 const task=await store.get(projectId,taskId);if(!task||task.kind!=='task'||task.deleted)fail('TASK_NOT_FOUND');
 if(expectedRevision!==undefined&&task.revision!==expectedRevision)fail('FILE_PREFLIGHT_STALE');
 const profile=decodeTaskProfile(task.data),key=(path:string)=>{const normal=normaliseRelativePath(path);return process.platform==='win32'?normal.toLowerCase():normal;};
 const pins=new Map((profile.schemaVersion==='m2_task_profile_v1'?profile.fileContexts:[]).filter(item=>item.revision).map(item=>[key(item.relativePath),item.revision!]));
 const files=profile.files.map(file=>({...file,...(pins.has(key(file.previousRelativePath??file.relativePath))?{revision:pins.get(key(file.previousRelativePath??file.relativePath))}:{})}));
 const report=await preflightTaskFiles(project,files);
 // Registry policy and task revision are observed in one SQLite snapshot after I/O.
 const current=await store.runtimeFileScope(projectId,taskId);
 if(!current.project||!current.task||current.task.revision!==task.revision||fileScopeFingerprint(current.project)!==fileScopeFingerprint(project))fail('FILE_PREFLIGHT_STALE');
 return {...report,taskId,taskRevision:task.revision};
}
/** A pin is evidence of the reviewed snapshot, never execution authority. */
export function assertFilePreflight(report:FilePreflight&{taskRevision:number},pin:unknown){
 if(!report.allowed)fail('FILE_PREFLIGHT_BLOCKED');
 if(pin!==undefined){if(!pin||typeof pin!=='object'||Array.isArray(pin)||Object.keys(pin).some(key=>!['digest','taskRevision'].includes(key))||(pin as any).digest!==report.digest||(pin as any).taskRevision!==report.taskRevision)fail('FILE_PREFLIGHT_STALE');}
}
