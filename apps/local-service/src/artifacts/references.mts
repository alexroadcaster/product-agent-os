import {normaliseRelativePath} from '../project-inventory/service.mts';

export type TaskPathReference={relativePath:string;revision:string|null;field:string;availability?:string};
export const sameRelativePath=(a:string,b:string)=>process.platform==='win32'?a.toLowerCase()===b.toLowerCase():a===b;
/** Explicit references only: URL/prose never acquires local filesystem authority. */
export function taskPathReferences(data:Record<string,unknown>):TaskPathReference[]{
 const references:TaskPathReference[]=[];const seen=new Set<string>();
 for(const field of ['files','fileContexts','artifacts','artifactReferences']){
  for(const entry of (Array.isArray(data[field])?data[field]:[]).slice(0,1000) as any[]){
   const paths=typeof entry==='string'?[entry]:[entry?.relativePath??entry?.path??entry?.reference,...(field==='files'&&entry?.previousRelativePath?[entry.previousRelativePath]:[])];
   for(const value of paths){if(typeof value!=='string')continue;let path:string;try{path=normaliseRelativePath(value);}catch{continue;}
    const revision=typeof entry==='object'&&typeof entry.revision==='string'?entry.revision:null;
    const key=JSON.stringify([field,process.platform==='win32'?path.toLowerCase():path,revision]);if(seen.has(key))continue;seen.add(key);
    references.push({relativePath:path,revision,field,...(typeof entry?.availability==='string'?{availability:entry.availability}:{})});
   }
  }
 }
 return references;
}
