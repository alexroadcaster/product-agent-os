import {createRequire} from 'node:module';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {posix} from 'node:path';
import {safePersistedText} from '../redaction/persisted.mts';
import {tokens,sqlReferences} from './sql.mts';
import {parserVersion} from './version.mts';
import type {CodeDatabaseLink,CodeDatabaseConfidence,CodeDatabaseOperation} from '../../../../packages/contracts/code-database.ts';
const require=createRequire(new URL('../../../web/package.json',import.meta.url)),parser=await import(pathToFileURL(require.resolve('rolldown/utils')).href);
export {parserVersion} from './version.mts';
export type StaticFile={relativePath:string;text:string};
type Binding={sourcePath:string|null;confidence:CodeDatabaseConfidence;reason:string};
const hash=(v:unknown)=>createHash('sha256').update(JSON.stringify(v)).digest('hex');
const ascii=(v:string)=>v.replace(/[A-Z]/g,c=>c.toLowerCase());
function relativeSource(file:string,path:string){if(!/^\.\.?\//.test(path)||/[\\:#?\x00]/.test(path))return null;const normalized=posix.normalize(posix.join(posix.dirname(file),path));return normalized.startsWith('../')||normalized==='..'||normalized.startsWith('/')?null:normalized;}
function prismaSchemas(files:StaticFile[]){const schemas=[] as Array<{models:Map<string,{model:string;table:string}>;sourcePath:string|null;reason?:string}>;
 const configured=files.some(f=>/(?:^|\/)prisma\.config\.[cm]?[jt]s$/.test(f.relativePath));
 for(const file of files.filter(f=>f.relativePath.endsWith('.prisma'))){const models=new Map<string,{model:string;table:string}>();let t;try{t=tokens(file.text,true);}catch{schemas.push({models,sourcePath:null,reason:'prisma_schema_parse_unavailable'});continue;}let provider='',url:string|null=null,datasources=0,generators=0,defaultClient=false,customOutput=false,invalid=false;
  for(let i=0;i<t.length;i++){if(!['datasource','model','generator'].includes(t[i].value)||t[i].kind!=='word'||t[i+1]?.kind!=='word'||t[i+2]?.value!=='{')continue;const kind=t[i].value,name=t[i+1].value;let depth=1,end=i+3;for(;end<t.length&&depth;end++){if(t[end].value==='{')depth++;if(t[end].value==='}')depth--;}if(depth)invalid=true;const block=t.slice(i+3,end-1);
   if(kind==='datasource'||kind==='generator'){if(kind==='datasource')datasources++;else generators++;for(let j=0;j<block.length-2;j++){if(block[j+1].value!=='=')continue;const value=block[j+2].kind==='string'?block[j+2].value:null;if(kind==='datasource'){if(block[j].value==='provider')provider=value??'';if(block[j].value==='url')url=value;}else{if(block[j].value==='provider')defaultClient=value==='prisma-client-js';if(block[j].value==='output')customOutput=true;}}}
   else{let table=name;for(let j=0;j<block.length-4;j++)if(block[j].value==='@'&&block[j+1].value==='@'&&block[j+2].value==='map'&&block[j+3].value==='('&&block[j+4].kind==='string')table=block[j+4].value;models.set(name[0].toLowerCase()+name.slice(1),{model:name,table});}i=end-1;
  }const sourcePath=!invalid&&!configured&&datasources===1&&generators===1&&defaultClient&&!customOutput&&provider==='sqlite'&&url?.startsWith('file:')?relativeSource(file.relativePath,url.slice(5)):null;schemas.push({models,sourcePath,...(!sourcePath?{reason:configured?'prisma_config_unresolved':'prisma_datasource_or_client_unresolved'}:{})});
 }return schemas;
}
/** Static syntax only: no compiler Program, module loading, config resolution, generated client, SQL or target execution. */
export function analyzeCodeDatabase(files:StaticFile[],options:{sourcePath:string;tables:string[];codeRevision:string;schemaRevision:string;maxLinks?:number}){
 const links:CodeDatabaseLink[]=[],reasons=new Set<string>(['static_subset_not_runtime_call_graph']),schemas=prismaSchemas(files),schema=schemas.length===1?schemas[0]:undefined,models=new Map<string,{model:string;table:string}>();
 for(const s of schemas){if(s.reason)reasons.add(s.reason);for(const [delegate,model] of s.models){const previous=models.get(delegate);models.set(delegate,previous&&previous.table!==model.table?{...model,table:'?'}:model);}}if(schemas.length>1)reasons.add('prisma_schema_ambiguous');
 const append=(file:StaticFile,span:CodeDatabaseLink['span'],table:string,operation:CodeDatabaseOperation,method:CodeDatabaseLink['method'],binding:Binding,model:string|null=null,extraReason?:string)=>{
  let confidence=binding.confidence,reason=binding.reason;const actual=options.tables.find(t=>ascii(t)===ascii(table));if(!actual){confidence='unresolved';reason=table==='?'?'dynamic_query_unresolved':'table_not_observed_in_selected_schema';}if(extraReason){confidence='unresolved';reason=extraReason;}if(links.length>=(options.maxLinks??1000)){reasons.add('link_limit');return;}
  const normalized=actual??table,value={relativePath:file.relativePath,span,query:method==='literal_sql'?safePersistedText(operation.toUpperCase()+' '+normalized).slice(0,160):null,model,table:normalized,sourcePath:binding.sourcePath,operation,method,confidence,reason,codeRevision:options.codeRevision,schemaRevision:options.schemaRevision};links.push({id:hash(value),...value});
 };
 const bindingFor=(path:string|null,unknownReason='dynamic_database_binding'):Binding=>({sourcePath:path,confidence:path===options.sourcePath?'confirmed':path?'inferred':'unresolved',reason:path===options.sourcePath?'literal_selected_source':path?'different_database_source':unknownReason});
 for(const file of files){
  const line=(offset:number)=>{const before=file.text.slice(0,offset),lines=before.split('\n');return {line:lines.length,column:lines.at(-1)!.length};};
  if(file.relativePath.endsWith('.sql')){try{for(const ref of sqlReferences(file.text))append(file,{start:line(ref.offset),end:line(ref.offset+ref.table.length)},ref.table,ref.operation,'literal_sql',{sourcePath:null,confidence:'inferred',reason:'sql_file_source_unbound'},null,ref.reason);}catch{reasons.add('sql_parse_unavailable:'+file.relativePath);}continue;}
  if(file.relativePath.endsWith('.prisma'))continue;if(!/\.(?:[cm]?[jt]sx?)$/.test(file.relativePath)){reasons.add('unsupported_language:'+file.relativePath);continue;}
  // Conservative admission before native parsing. Delimiters inside literals/comments also count;
  // exceeding the bound means partial coverage, not a claim that the source is invalid.
  let delimiterDepth=0,depthExceeded=false;for(const character of file.text){if('([{'.includes(character)){if(++delimiterDepth>128){depthExceeded=true;break;}}else if(')]}'.includes(character))delimiterDepth=Math.max(0,delimiterDepth-1);}if(depthExceeded){reasons.add('source_depth_limit:'+file.relativePath);continue;}
  let program:any;try{const result=parser.parseSync(file.relativePath,file.text,{lang:file.relativePath.endsWith('x')?'tsx':/\.[cm]?ts$/.test(file.relativePath)?'ts':'js',astType:'ts'});if(result.errors.length)throw Error('PARSE');program=result.program;}catch{reasons.add('code_parse_unavailable:'+file.relativePath);continue;}
  type Scope={parent?:Scope;kind:string;names:Map<string,any>};const root:Scope={kind:'Program',names:new Map()},scopeAt=new WeakMap<object,Scope>();let visited=0;
  const children=(node:any)=>Object.entries(node).filter(([key])=>!['parent','typeAnnotation','returnType','typeParameters','typeArguments','decorators'].includes(key)).flatMap(([,value])=>Array.isArray(value)?value.filter(v=>v&&typeof v.type==='string'):value&&typeof value==='object'&&typeof (value as any).type==='string'?[value]:[]);
  const define=(scope:Scope,name:string,value:any)=>scope.names.set(name,scope.names.has(name)?null:value);
  const names=(node:any):string[]=>!node?[]:node.type==='Identifier'?[node.name]:node.type==='TSParameterProperty'?names(node.parameter):node.type==='RestElement'?names(node.argument):node.type==='AssignmentPattern'?names(node.left):node.type==='ArrayPattern'?node.elements.flatMap(names):node.type==='ObjectPattern'?node.properties.flatMap((p:any)=>names(p.value??p.argument)):[];
  const declarations=(node:any,scope:Scope,parent?:any,depth=0)=>{if(++visited>200000||depth>256)throw Error('AST_LIMIT');if(['FunctionDeclaration','ClassDeclaration'].includes(node.type)&&node.id)define(scope,node.id.name,null);let current=scope;if(['FunctionDeclaration','FunctionExpression','ArrowFunctionExpression','ClassDeclaration','ClassExpression','BlockStatement','CatchClause','ForStatement','ForOfStatement','ForInStatement','SwitchStatement'].includes(node.type)){current={parent:scope,kind:node.type,names:new Map()};if((node.type==='FunctionExpression'||node.type.startsWith('Class'))&&node.id)define(current,node.id.name,null);if(node.type.includes('Function')){for(const param of node.params??[])for(const name of names(param))define(current,name,null);}if(node.type==='CatchClause')for(const name of names(node.param))define(current,name,null);}scopeAt.set(node,current);
   if(node.type==='ImportDeclaration')for(const spec of node.specifiers)define(root,spec.local.name,spec.type==='ImportSpecifier'&&node.importKind!=='type'&&spec.importKind!=='type'?{kind:'import',module:node.source.value,imported:spec.imported.name??spec.imported.value}:null);
   if(node.type==='VariableDeclarator'){let target=current;if(parent?.kind==='var')while(target.parent&&!target.kind.includes('Function')&&target.kind!=='Program')target=target.parent;for(const name of names(node.id))define(target,name,{kind:'variable',node,constant:parent?.kind==='const'});}
   if(node.type==='ClassDeclaration'&&node.id)define(current,node.id.name,null);for(const child of children(node))declarations(child,current,node,depth+1);
  };try{declarations(program,root);}catch{reasons.add('ast_limit:'+file.relativePath);continue;}
  const resolve=(node:any)=>{for(let scope=scopeAt.get(node);scope;scope=scope.parent)if(scope.names.has(node.name))return scope.names.get(node.name);return undefined;};
  const literal=(node:any)=>node?.type==='Literal'&&typeof node.value==='string'?node.value:node?.type==='TemplateLiteral'&&!node.expressions.length?node.quasis[0].value.cooked:null;
  const member=(node:any,name?:string)=>node?.type==='MemberExpression'&&!node.computed&&node.property.type==='Identifier'&&(!name||node.property.name===name);
  const imported=(node:any,module:string,name:string)=>{if(node?.type!=='Identifier')return false;const bound=resolve(node);return bound?.kind==='import'&&bound.module===module&&bound.imported===name;};
  const variable=(node:any,prisma=false):Binding=>{if(node?.type!=='Identifier')return bindingFor(null,'untraced_receiver');const bound=resolve(node),initializer=bound?.node?.init;if(bound?.kind!=='variable'||!bound.constant||initializer?.type!=='NewExpression')return bindingFor(null,'untraced_receiver');
   if(prisma){if(!imported(initializer.callee,'@prisma/client','PrismaClient')||initializer.arguments.length)return bindingFor(null,'untraced_prisma_client');return bindingFor(schema?.sourcePath??null,schemas.length!==1?'prisma_schema_ambiguous':'prisma_datasource_unresolved');}
   if(!imported(initializer.callee,'node:sqlite','DatabaseSync'))return bindingFor(null,'untraced_receiver');const url=initializer.arguments[0];if(url?.type!=='NewExpression'||url.callee.type!=='Identifier'||url.callee.name!=='URL'||resolve(url.callee)!==undefined)return bindingFor(null);const [path,base]=url.arguments;
   const meta=member(base,'url')&&base.object.type==='MetaProperty'&&base.object.meta.name==='import'&&base.object.property.name==='meta';return bindingFor(meta&&literal(path)!==null?relativeSource(file.relativePath,literal(path)):null);
  };
  const visit=(node:any)=>{if(node.type==='CallExpression'&&member(node.callee)){const access=node.callee,method=access.property.name,span={start:line(node.start),end:line(node.end)};
    if(['prepare','exec'].includes(method)){const sql=literal(node.arguments[0]),binding=variable(access.object);if(sql===null)append(file,span,'?','unknown','literal_sql',binding);else try{for(const ref of sqlReferences(sql))append(file,span,ref.table,ref.operation,'literal_sql',binding,null,ref.reason);}catch{reasons.add('sql_parse_unavailable:'+file.relativePath);}}
    else{const operation:CodeDatabaseOperation=['findMany','findFirst','findFirstOrThrow','findUnique','findUniqueOrThrow','count','aggregate','groupBy'].includes(method)?'read':['create','createMany','update','updateMany','upsert','delete','deleteMany'].includes(method)?'write':'unknown';if(member(access.object)){const model=models.get(access.object.property.name);if(model)append(file,span,model.table,operation,'prisma_static',variable(access.object.object,true),model.model,operation==='unknown'?'prisma_method_unsupported':undefined);}
     else if(access.object?.type==='Identifier'){const alias=resolve(access.object)?.node?.init,model=member(alias)?models.get(alias.property.name):undefined;if(model)append(file,span,model.table,operation,'prisma_static',bindingFor(null,'prisma_delegate_alias_untraced'),model.model);}
     else if(access.object?.type==='MemberExpression'&&access.object.computed&&variable(access.object.object,true).confidence==='confirmed')append(file,span,'?',operation,'prisma_static',variable(access.object.object,true),null,'prisma_delegate_dynamic');
    }
   }else if(node.type==='CallExpression'){const sql=literal(node.arguments[0]);if(sql!==null)try{for(const ref of sqlReferences(sql))append(file,{start:line(node.start),end:line(node.end)},ref.table,ref.operation,'literal_sql',bindingFor(null,'untraced_call_target'),null,ref.reason);}catch{reasons.add('sql_parse_unavailable:'+file.relativePath);}}
   for(const child of children(node))visit(child);};visit(program);
 }
 return {links,reasons:[...reasons].sort(),parserVersion};
}
