import {createHash} from 'node:crypto';
import type {GraphNode,GraphEdge,GraphAnchor,GraphEdgeType} from '../../../../packages/contracts/graph/code-graph.ts';
type Ast=any;
type Scope={id:string;kind:string;parent?:Scope;bindings:Map<string,GraphNode>};
const hash=(s:string)=>createHash('sha256').update(s).digest('hex');
/** Two passes collect declarations before resolving references, including var hoisting and nearest shadowing.
 * This is lexical source evidence, not type, alias, module-linker or runtime resolution. */
export function buildLexicalGraph(file:{relativePath:string;text:string;language:string},program:Ast){
 const fileId=hash(file.relativePath),nodes:GraphNode[]=[],edges:GraphEdge[]=[],imports:{specifier:string;anchor:GraphAnchor}[]=[],scopeAt=new WeakMap<object,Scope>(),definitions=new WeakSet<object>();
 let visited=0;const root:Scope={id:'module:0',kind:'module',bindings:new Map()};
 const anchor=(n:Ast):GraphAnchor=>{const before=file.text.slice(0,n.start),line=before.split('\n').length;return {fileId,start:n.start,end:n.end,line,column:n.start-(before.lastIndexOf('\n')+1)+1};};
 const base={relativePath:file.relativePath,fileId,language:file.language};
 nodes.push({id:fileId,kind:'file',name:file.relativePath,...base,scope:root.id,namespace:'module'});
 const children=(n:Ast)=>Object.entries(n).filter(([k])=>!['parent','typeAnnotation','returnType','typeParameters','superTypeParameters','implements','decorators'].includes(k)).flatMap(([key,value])=>Array.isArray(value)?value.filter(v=>v&&typeof v.type==='string').map(v=>({key,node:v})):value&&typeof value==='object'&&typeof (value as Ast).type==='string'?[{key,node:value}]:[]);
 const declare=(n:Ast,s:Scope)=>{if(!n)return;if(n.type==='Identifier'){definitions.add(n);let symbol=s.bindings.get(n.name);if(!symbol){symbol={id:hash(`${fileId}|${file.language}|${s.id}|${n.start}|value|${n.name}`),kind:'symbol',name:n.name,...base,scope:s.id,namespace:'value',anchor:anchor(n)};s.bindings.set(n.name,symbol);nodes.push(symbol);}edges.push({id:hash(`define|${symbol.id}|${n.start}`),type:'define',from:fileId,to:symbol.id,anchor:anchor(n),resolution:'lexical'});return;}
  if(n.type==='AssignmentPattern')declare(n.left,s);else if(n.type==='RestElement')declare(n.argument,s);else if(n.type==='ObjectPattern')for(const p of n.properties)declare(p.type==='RestElement'?p.argument:p.value,s);else if(n.type==='ArrayPattern')for(const e of n.elements)declare(e,s);
 };
 function first(n:Ast,s:Scope,depth=0){if(++visited>150000||depth>200)throw Error('limit');if(!n||n.type?.startsWith('TS')&&!['TSAsExpression','TSSatisfiesExpression','TSNonNullExpression'].includes(n.type))return;
  const outer=s;
  if(n.type==='FunctionDeclaration'&&n.id)declare(n.id,s);
  if(/Function|Method/.test(n.type)||['BlockStatement','CatchClause','ForStatement','ForInStatement','ForOfStatement','SwitchStatement','ClassBody'].includes(n.type))s={id:`${n.type}:${n.start}`,kind:/Function|Method/.test(n.type)?'function':'block',parent:s,bindings:new Map()};
  scopeAt.set(n,s);
  if(/Function|Method/.test(n.type)){if(n.type!=='FunctionDeclaration'&&n.id)declare(n.id,s);for(const p of n.params??[])declare(p,s);}
  if(n.type==='CatchClause')declare(n.param,s);
  if(n.type==='VariableDeclaration'){let target=s;if(n.kind==='var')while(target.parent&&target.kind!=='function')target=target.parent;for(const d of n.declarations)declare(d.id,target);}
  if(n.type==='ClassDeclaration'&&n.id)declare(n.id,s);
  if(n.type==='ImportDeclaration')for(const p of n.specifiers){declare(p.local,s);const symbol=s.bindings.get(p.local.name);if(symbol)symbol.reason='module_alias_unresolved';}
  // The switch discriminant is evaluated before the case block lexical environment exists.
  for(const {node,key} of children(n))first(node,n.type==='SwitchStatement'&&key==='discriminant'?outer:s,depth+1);
 }
 first(program,root);
 const resolve=(s:Scope,name:string):GraphNode|undefined=>s.bindings.get(name)??(s.parent?resolve(s.parent,name):undefined);
 const unresolved=(n:Ast,s:Scope,reason:string)=>{const id=hash(`${fileId}|${s.id}|${n.start}|${reason}`),node:GraphNode={id,kind:'unresolved',name:n.type==='Identifier'?n.name:n.type,...base,scope:s.id,namespace:'dynamic',anchor:anchor(n),reason};nodes.push(node);return node;};
 const edge=(n:Ast,s:Scope,type:GraphEdgeType,force?:string)=>{const target=force?unresolved(n,s,force):resolve(s,n.name)??unresolved(n,s,'unresolved_identifier');edges.push({id:hash(`${fileId}|${n.start}|${type}|${target.id}`),type,from:fileId,to:target.id,anchor:anchor(n),resolution:force?'dynamic':target.kind==='unresolved'||target.reason?'unresolved':'lexical'});};
 function second(n:Ast,parent?:Ast,key='',mode:GraphEdgeType='read'){
  const s=scopeAt.get(n);if(!s)return;
  if(n.type==='Identifier'){
   if(definitions.has(n))return;
   if(parent&&((['MemberExpression','OptionalMemberExpression'].includes(parent.type)&&key==='property'&&!parent.computed)||(['Property','MethodDefinition','PropertyDefinition'].includes(parent.type)&&key==='key'&&!parent.computed)||['ImportSpecifier','ImportDefaultSpecifier','ImportNamespaceSpecifier','ExportSpecifier','LabeledStatement','BreakStatement','ContinueStatement','MetaProperty'].includes(parent.type)))return;
   edge(n,s,mode);return;
  }
  if(n.type==='AssignmentExpression'){second(n.left,n,'left','write');if(n.operator!=='=')second(n.left,n,'left','read');second(n.right,n,'right');return;}
  // Destructuring writes targets, but computing a key or a default value only reads its inputs.
  if(n.type==='AssignmentPattern'){second(n.left,n,'left',mode);second(n.right,n,'right','read');return;}
  if(n.type==='Property'){if(n.computed)second(n.key,n,'key','read');second(n.value,n,'value',mode);return;}
  if(n.type==='UpdateExpression'){second(n.argument,n,'argument','read');second(n.argument,n,'argument','write');return;}
  if(n.type==='ForInStatement'||n.type==='ForOfStatement'){second(n.left,n,'left',n.left.type==='VariableDeclaration'?'read':'write');second(n.right,n,'right');second(n.body,n,'body');return;}
  if(['CallExpression','NewExpression'].includes(n.type)){if(n.callee.type==='Identifier')edge(n.callee,s,'call',n.callee.name==='eval'?'eval':undefined);else edge(n.callee,s,'call','member_or_dynamic_call');second(n.callee,n,'callee','reference');for(const a of n.arguments)second(a,n,'arguments');return;}
  if(n.type==='ImportDeclaration'){imports.push({specifier:n.source.value,anchor:anchor(n)});return;}
  if((n.type==='ExportNamedDeclaration'||n.type==='ExportAllDeclaration')&&n.source)imports.push({specifier:n.source.value,anchor:anchor(n)});
  if(n.type==='ImportExpression')edge(n,s,'import','dynamic_import');
  if(n.type==='MemberExpression'||n.type==='OptionalMemberExpression'){second(n.object,n,'object','reference');if(n.computed)second(n.property,n,'property');if(mode==='write')edge(n,s,'write','member_write');return;}
  for(const c of children(n))second(c.node,n,c.key,mode);
 }
 second(program);
 if(nodes.length>25000||edges.length>50000)throw Error('limit');
 return {nodes,edges,imports};
}
