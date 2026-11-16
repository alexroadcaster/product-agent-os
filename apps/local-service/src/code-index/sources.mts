import {createHash} from 'node:crypto';
import {extname} from 'node:path';
import {createProjectInventory,classifyInventoryPath} from '../project-inventory/service.mts';
import type {InventoryProject,InventoryPolicy} from '../../../../packages/contracts/project-inventory.ts';

export const graphFail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
export const digest=(value:string|Buffer)=>createHash('sha256').update(value).digest('hex');
export type SourceProject=InventoryProject & {inventoryPolicy?:InventoryPolicy};
const inventories=new Map<string,ReturnType<typeof createProjectInventory>>();
/** Consumers share the same policy instance; cursors stay valid until policy/cache changes. */
export function inventoryForProject(project:SourceProject){
 const key=JSON.stringify(project.inventoryPolicy??{});let inventory=inventories.get(key);
 if(!inventory){inventory=createProjectInventory({policy:project.inventoryPolicy});if(inventories.size>=32)inventories.delete(inventories.keys().next().value!);inventories.set(key,inventory);}
 return inventory;
}
export const sensitiveSourcePath=(path:string)=>{try{return !classifyInventoryPath(path).readable;}catch{return true;}};
function compatibleError(error:unknown):never{
 const original=(error as {code?:string}).code;
 const code:Record<string,string>={INVENTORY_PATH_FORBIDDEN:'GRAPH_SOURCE_FORBIDDEN',INVENTORY_SOURCE_FORBIDDEN:'GRAPH_SOURCE_FORBIDDEN',INVENTORY_LINKED_SOURCE:'GRAPH_LINKED_SOURCE',INVENTORY_FILE_TOO_LARGE:'GRAPH_SOURCE_LIMIT',INVENTORY_ENCODING_UNSUPPORTED:'GRAPH_SOURCE_ENCODING',INVENTORY_BINARY_FILE:'GRAPH_SOURCE_ENCODING',INVENTORY_SENSITIVE_CONTENT:'GRAPH_SOURCE_FORBIDDEN',INVENTORY_SOURCE_DRIFT:'GRAPH_SOURCE_DRIFT',INVENTORY_REVISION_STALE:'GRAPH_SOURCE_DRIFT',INVENTORY_CANCELLED:'GRAPH_BUILD_CANCELLED',INVENTORY_TIMEOUT:'GRAPH_INVENTORY_LIMIT'};
 if(original&&code[original])graphFail(code[original]);throw error;
}
export async function assertSourceProject(project:SourceProject){try{await inventoryForProject(project).assertProject(project);}catch(error){compatibleError(error);}}
export async function readCheckedSource(project:SourceProject,path:string,limit=512*1024,options:{redactSensitive?:true}={}){
 try{return await inventoryForProject(project).read(project,{path,maxBytes:limit,...options});}catch(error){compatibleError(error);}
}
/** Metadata policy applies before extension filtering; exclusions and partial scope remain observable. */
export async function scanCheckedSources(project:SourceProject,extensions?:Set<string>,options:{signal?:AbortSignal}={}){
 try{
  const snapshot=await inventoryForProject(project).snapshot(project,options);
  const files=snapshot.entries.filter(entry=>entry.kind==='file'&&entry.access.readable&&(!extensions||extensions.has(extname(entry.relativePath).toLowerCase()))).map(entry=>entry.relativePath);
  const exclusions=snapshot.entries.filter(entry=>entry.kind==='link'||entry.kind==='file'&&!entry.access.readable).map(entry=>({relativePath:entry.relativePath,reason:entry.access.reason??'unreadable'}));
  return {files,excluded:exclusions.map(entry=>entry.relativePath),exclusions,inventoryRevision:snapshot.revision,inventory:snapshot};
 }catch(error){compatibleError(error);}
}
