import {posix} from 'node:path';

/** Root-owned JSON metadata only. No package discovery, extends or executable config. */
export type ModuleResolverConfig={baseUrl?:string;paths?:Record<string,string[]>};
export type ModuleResolution={state:'resolved';relativePath:string}|{state:'unresolved';reason:string};
const extensions=['.ts','.tsx','.js','.jsx','.mts','.mjs','.cts','.cjs'];
const folded=(path:string)=>process.platform==='win32'?path.toLowerCase():path;
const plain=(value:unknown):value is Record<string,unknown>=>Boolean(value)&&typeof value==='object'&&!Array.isArray(value)&&[Object.prototype,null].includes(Object.getPrototypeOf(value));
const dataOnly=(value:object)=>Object.values(Object.getOwnPropertyDescriptors(value)).every(d=>'value' in d);
function safePath(value:unknown,wildcard=false):value is string{
 if(typeof value!=='string'||value.length>256||/[\x00-\x1f:\\?#]/.test(value)||value.startsWith('/')||value.split('/').some(p=>p==='..'||p.endsWith(' ')||p!=='.'&&p.endsWith('.')))return false;
 const stars=value.split('*').length-1;return stars<=(wildcard?1:0);
}
const normalize=(value:string)=>posix.normalize(value)==='.'?'':posix.normalize(value).replace(/^\.\//,'');

/** Invalid metadata disables aliases/baseUrl as a whole; relative resolution
 * still works and the caller publishes explicit configReasons. */
export function sanitizeModuleResolverConfig(raw:unknown):{resolverConfig?:ModuleResolverConfig;configReasons:string[]}{
 const invalid=()=>({configReasons:['resolver_config_unsupported']});
 if(raw===undefined)return {configReasons:[]};
 if(!plain(raw)||!dataOnly(raw)||Object.keys(raw).some(k=>!['baseUrl','paths'].includes(k)))return invalid();
 if(raw.baseUrl!==undefined&&!safePath(raw.baseUrl))return invalid();
 let paths:Record<string,string[]>|undefined;
 if(raw.paths!==undefined){
  if(!plain(raw.paths)||!dataOnly(raw.paths)||Object.keys(raw.paths).length>64)return invalid();
  paths={};
  for(const [alias,targets] of Object.entries(raw.paths)){
   if(!alias||!safePath(alias,true)||alias.startsWith('.')||['__proto__','constructor','prototype'].includes(alias)||!Array.isArray(targets)||!dataOnly(targets)||targets.length<1||targets.length>8)return invalid();
   if(Array.from({length:targets.length},(_,i)=>targets[i]).some(t=>!safePath(t,true)||!alias.includes('*')&&t.includes('*')))return invalid();
   paths[alias]=targets.map(t=>normalize(t));
  }
 }
 const resolverConfig:ModuleResolverConfig={...(raw.baseUrl===undefined?{}:{baseUrl:normalize(raw.baseUrl)}),...(paths===undefined?{}:{paths})};
 return {resolverConfig,configReasons:[]};
}

/** A closed allowlist is the entire module universe. The resolver performs no
 * filesystem access, package execution, symlink lookup or ancestor discovery. */
export function createIndexedModuleResolver(indexed:Iterable<string>,config?:ModuleResolverConfig){
 const files=new Map<string,string[]>();
 for(const path of indexed){if(!safePath(path)||normalize(path)!==path||!path)continue;const key=folded(path);files.set(key,[...new Set([...(files.get(key)??[]),path])]);}
 const sanitized=sanitizeModuleResolverConfig(config),allowed=sanitized.resolverConfig;
 const candidates=(base:string)=>[base,...extensions.flatMap(ext=>[base+ext,posix.join(base,'index'+ext)])];
 return (from:string,specifier:string):ModuleResolution=>{
  const unresolved=(reason:string):ModuleResolution=>({state:'unresolved',reason});
  if(typeof specifier!=='string'||!specifier||specifier.length>2048||/[\x00-\x1f:\\?#]/.test(specifier)||specifier.startsWith('/'))return unresolved('module_specifier_unsupported');
  const bases:string[]=[];
  if(specifier.startsWith('./')||specifier.startsWith('../')){
   const base=posix.normalize(posix.join(posix.dirname(from),specifier));
   if(base==='..'||base.startsWith('../')||base.startsWith('/'))return unresolved('module_outside_root');bases.push(base);
  }else{
   if(specifier.split('/').some(p=>p==='.'||p==='..'))return unresolved('module_specifier_unsupported');
   const rules=Object.entries(allowed?.paths??{}),exact=rules.filter(([key])=>key===specifier);
   let matches=exact.map(([key,targets])=>({key,targets,capture:''}));
   if(!matches.length){
    for(const [key,targets] of rules){const star=key.indexOf('*');if(star<0)continue;const prefix=key.slice(0,star),suffix=key.slice(star+1);if(specifier.startsWith(prefix)&&specifier.endsWith(suffix)&&specifier.length>=prefix.length+suffix.length)matches.push({key,targets,capture:specifier.slice(prefix.length,specifier.length-suffix.length)});}
    if(matches.length){const longest=Math.max(...matches.map(m=>m.key.indexOf('*')));matches=matches.filter(m=>m.key.indexOf('*')===longest);}
   }
   if(matches.length)for(const match of matches)for(const target of match.targets)bases.push(posix.join(allowed?.baseUrl??'',target.replace('*',match.capture)));
   else if(allowed?.baseUrl!==undefined)bases.push(posix.join(allowed.baseUrl,specifier));
   else return unresolved(sanitized.configReasons.length?'resolver_config_unsupported':'module_not_resolved');
  }
  const found=new Set<string>();
  for(const base of bases){if(base==='..'||base.startsWith('../')||base.startsWith('/'))continue;for(const candidate of candidates(base))for(const path of files.get(folded(candidate))??[])found.add(path);}
  if(found.size===1)return {state:'resolved',relativePath:[...found][0]};
  return unresolved(found.size?'ambiguous_module':'module_not_resolved');
 };
}
export function resolveIndexedModule(from:string,specifier:string,indexed:Iterable<string>,config?:ModuleResolverConfig):ModuleResolution{return createIndexedModuleResolver(indexed,config)(from,specifier);}
