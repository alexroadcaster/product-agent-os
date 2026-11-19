import {posix} from 'node:path';
import {digest} from './sources.mts';
import {sanitizeModuleResolverConfig,type ModuleResolverConfig} from './module-resolver.mts';

type Source = {text:string;hash:string};
type Located = {baseUrl?:string;paths?:ModuleResolverConfig['paths'];pathsDirectory?:string};
const object=(value:unknown):value is Record<string,unknown>=>Boolean(value)&&typeof value==='object'&&!Array.isArray(value);
const invalid=():never=>{throw Error('Unsupported module configuration');};

/** Resolve a bounded chain of explicitly relative JSON configs. The reader owns file authority. */
export async function readResolverConfig(read:(path:string)=>Promise<Source>){
 const observed=new Map<string,string>();
 async function visit(path:string):Promise<Located>{
  if(observed.has(path)||observed.size>=5)return invalid();
  const source=await read(path);
  observed.set(path,source.hash);
  const config:unknown=JSON.parse(source.text);
  if(!object(config)||Object.hasOwn(config,'references'))return invalid();
  let inherited:Located={};
  if(Object.hasOwn(config,'extends')){
   const extension=config.extends;
   if(typeof extension!=='string'||!/^\.\.?\//.test(extension)||!extension.endsWith('.json')
    ||/[\\:\x00-\x20?#]/.test(extension))return invalid();
   const relative=posix.normalize(posix.join(posix.dirname(path),extension));
   if(relative.startsWith('../')||relative==='..'||relative.startsWith('/'))return invalid();
   inherited=await visit(relative);
  }
  const options=config.compilerOptions===undefined?{}:config.compilerOptions;
  if(!object(options))return invalid();
  const local=sanitizeModuleResolverConfig({
   ...(options.baseUrl===undefined?{}:{baseUrl:options.baseUrl}),
   ...(options.paths===undefined?{}:{paths:options.paths}),
  });
  if(!local.resolverConfig||local.configReasons.length)return invalid();
  const {baseUrl,paths}=local.resolverConfig,folder=posix.dirname(path);
  if([baseUrl,...Object.values(paths??{}).flat()].some(value=>value?.includes('${')))return invalid();
  return {
   ...inherited,
   ...(baseUrl===undefined?{}:{baseUrl:posix.join(folder,baseUrl)}),
   ...(paths===undefined?{}:{paths,pathsDirectory:folder}),
  };
 }
 let resolverConfig:ModuleResolverConfig|undefined,configReasons:string[]=[];
 try{
  const {baseUrl,paths,pathsDirectory}=await visit('tsconfig.json');
  const selected=sanitizeModuleResolverConfig({
   ...(baseUrl===undefined?{}:{baseUrl}),
   ...(paths===undefined?{}:{paths:baseUrl===undefined
    ?Object.fromEntries(Object.entries(paths).map(([alias,targets])=>[alias,targets.map(target=>posix.join(pathsDirectory!,target))]))
    :paths}),
  });
  if(selected.configReasons.length)return invalid();
  resolverConfig=selected.resolverConfig;
 }catch{configReasons=['resolver_config_unavailable_or_unsupported'];}
 return {resolverConfig,configReasons,moduleConfigHash:digest(JSON.stringify([...observed]))};
}
