import {resolve,sep,join,relative,isAbsolute} from 'node:path';
import {lstat,realpath} from 'node:fs/promises';
import {bindProject} from '../adapters/project-sources.ts';
import {pathKey,recipeFail as fail} from '../execution-recipes/contract.mts';
import type {FrozenRecipePlan} from './contract.mts';
import type {OwnershipClaim} from '../../../../packages/contracts/scheduler/queue.ts';
const key=(path:string)=>process.platform==='win32'?resolve(path).toLowerCase():resolve(path);
/** Whole native workspaces are exclusive, even when logical file claims do not intersect. */
export function workspaceOverlap(a:string,b:string){const left=key(a),right=key(b);const contains=(base:string,child:string)=>{const part=relative(base,child);return !part||part!=='..'&&!part.startsWith('..'+sep)&&!isAbsolute(part);};return contains(left,right)||contains(right,left);}
export function workspaceCount(roots:string[]){const unique:string[]=[];for(const root of roots)if(!unique.some(other=>workspaceOverlap(root,other)))unique.push(root);return unique.length;}
export function recipeClaims(plan:FrozenRecipePlan):OwnershipClaim[]{
 const claims=new Map<string,OwnershipClaim>();
 const add=(path:string,mode:'read'|'write')=>{const canonical=pathKey(path),prior=claims.get(canonical);claims.set(canonical,{path,mode:prior?.mode==='write'?'write':mode});};
 for(const file of plan.taskContext.files??[])add(file.relativePath,file.plannedOperation==='read'?'read':'write');
 for(const step of plan.recipe.steps){for(const path of step.inputArtifacts)add(path,'read');for(const path of [...step.outputArtifacts,...step.ownership])add(path,'write');}
 if(!claims.size)add('.','write');if(claims.size>128)fail('QUEUE_OWNERSHIP_LIMIT');return [...claims.values()];
}
/** Reject existing aliases and multiply linked files. Missing descendants remain bounded by the pinned root. */
export async function verifyQueueOwnership(plan:FrozenRecipePlan,claims:OwnershipClaim[]){
 const binding=await bindProject('queue-ownership',plan.workspaceRoot);if(binding.directoryIdentity!==plan.rootIdentity)fail('QUEUE_ROOT_CHANGED');
 for(const claim of claims){pathKey(claim.path);if(claim.path==='.')continue;const parts=claim.path.split('/');
  for(let i=1;i<=parts.length;i++){const path=join(binding.workspaceRoot,...parts.slice(0,i));try{const info=await lstat(path);if(info.isSymbolicLink()||key(await realpath(path))!==key(path)||info.isFile()&&info.nlink!==1||i<parts.length&&!info.isDirectory())fail('QUEUE_UNSAFE_OWNERSHIP');}
   catch(error){if((error as NodeJS.ErrnoException).code==='ENOENT')break;throw error;}}
 }
}
