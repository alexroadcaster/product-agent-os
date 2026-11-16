import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import type {InventoryProject,InventoryPolicy} from '../../../../packages/contracts/project-inventory.ts';
import type {LocalStore} from '../storage/local-store.mts';
type Scope=InventoryProject&{inventoryPolicy?:InventoryPolicy};
/** Registry policy is authority; a captured filesystem binding alone cannot prove it stayed current. */
export function inventoryScopeFingerprint(project:Scope){const path=resolve(project.canonicalRoot);return createHash('sha256').update(JSON.stringify([project.id,process.platform==='win32'?path.toLowerCase():path,project.rootIdentity,project.inventoryPolicy??{}])).digest('hex');}
export async function assertCurrentSourceProject(store:Pick<LocalStore,'project'|'runtimeFileScope'>,saved:Scope,task?:{id:string;revision:number}){
 const current=task?await store.runtimeFileScope(saved.id,task.id):{project:await store.project(saved.id),task:null};
 if(!current.project||inventoryScopeFingerprint(current.project)!==inventoryScopeFingerprint(saved)||task&&current.task?.revision!==task.revision)throw Object.assign(new Error('Project source authority changed'),{code:'PROJECT_SCOPE_STALE'});
}
