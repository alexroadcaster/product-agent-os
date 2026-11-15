import {createHash} from 'node:crypto';
export const digest=(value:string)=>createHash('sha256').update(value).digest('hex');
/** External output is data, never an authority to read a path or execute an import. */
export function relativePath(value:string){
 const path=value.replaceAll('\\','/');
 if(!path||path.startsWith('/')||path.includes(':')||path.split('/').some(p=>!p||p==='.'||p==='..')||/[\x00-\x1f]/.test(path))throw Error('UNSAFE_ENGINE_PATH');
 return path;
}
export function normalizedCruise(raw:any,files:Record<string,string>){
 const nodes:any[]=[],edges:any[]=[],unresolved:any[]=[];
 for(const module of raw.modules??[]){
  // Unresolved pseudo-modules are represented by their importing dependency diagnostic, never as source files.
  if(module.couldNotResolve)continue;
  const from=relativePath(module.source);if(!Object.hasOwn(files,from))continue;
  nodes.push({id:from,kind:'file',name:from.split('/').at(-1),relativePath:from,line:1});
  for(const dependency of module.dependencies??[]){
   if(dependency.coreModule)continue;
   const target=dependency.couldNotResolve?undefined:relativePath(dependency.resolved);
   const literal=String(dependency.module),lines=files[from].split('\n'),line=lines.findIndex(l=>l.includes("'"+literal+"'")||l.includes('"'+literal+'"'))+1;
   if(!target||!Object.hasOwn(files,target)){unresolved.push({from,specifier:literal,line:line||1,reason:dependency.couldNotResolve?'missing_import':'outside_project'});continue;}
   edges.push({id:digest(from+'|'+target+'|import'),from,to:target,type:'import',relativePath:from,line:line||1,resolution:'resolved',typeOnly:typeof dependency.preCompilationOnly==='boolean'?dependency.preCompilationOnly:null,dynamic:typeof dependency.dynamic==='boolean'?dependency.dynamic:null});
  }
 }
 return {nodes,edges,unresolved};
}
export function edgeAccuracy(edges:any[],expected:string[][]){
 const actual=new Set(edges.filter(e=>e.type==='import'&&e.resolution!=='unresolved').map(e=>e.from+' -> '+e.to));
 const truth=new Set(expected.map(e=>e.join(' -> '))),matched=[...actual].filter(e=>truth.has(e));
 return {truePositive:matched.length,falsePositive:[...actual].filter(e=>!truth.has(e)),falseNegative:[...truth].filter(e=>!actual.has(e)),precision:actual.size?matched.length/actual.size:0,recall:truth.size?matched.length/truth.size:0};
}
export function queryChangeTask(edges:any[],id:string){
 const imports=edges.filter(e=>e.type==='import');
 if(id==='incoming-lib'||id==='incoming-alias-model'){const target=id==='incoming-lib'?'src/lib.ts':'src/model.ts';return [...new Set(imports.filter(e=>e.to===target).map(e=>e.from))].sort();}
 const cycle=new Set<string>();
 for(const start of new Set(imports.map(e=>e.from))){const visit=(current:string,path:string[]):void=>{for(const e of imports.filter(e=>e.from===current)){if(e.to===start){path.forEach(p=>cycle.add(p));cycle.add(current);}else if(!path.includes(e.to))visit(e.to,[...path,e.to]);}};visit(start,[start]);}
 return [...cycle].sort();
}
