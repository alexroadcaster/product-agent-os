import type {CodeDatabaseOperation} from '../../../../packages/contracts/code-database.ts';
export type Token={kind:'word'|'identifier'|'string'|'punct';value:string;offset:number};
/** Bounded lexical subset: comments/value strings cannot introduce table references. */
export function tokens(source:string,prisma=false):Token[]{
 const result:Token[]=[];let i=0;
 while(i<source.length){const at=i,c=source[i],next=source[i+1];if(/\s/.test(c)){i++;continue;}if(c==='-'&&next==='-'||prisma&&c==='/'&&next==='/'){while(i<source.length&&source[i]!=='\n')i++;continue;}if(c==='/'&&next==='*'){const end=source.indexOf('*/',i+2);if(end<0)throw Error('UNTERMINATED_COMMENT');i=end+2;continue;}
  if(c==="'"||c==='"'||c==='`'||c==='['){const end=c==='['?']':c;let value='';i++;let closed=false;while(i<source.length){if(source[i]===end){if(source[i+1]===end){value+=end;i+=2;continue;}i++;closed=true;break;}if(prisma&&source[i]==='\\'&&i+1<source.length){value+=source[++i];i++;}else value+=source[i++];}if(!closed)throw Error('UNTERMINATED_QUOTE');result.push({kind:c==="'"||prisma?'string':'identifier',value,offset:at});}
  else if(/[\p{L}_$]/u.test(c)){let end=i+1;while(end<source.length&&/[\p{L}\p{N}_$]/u.test(source[end]))end++;result.push({kind:'word',value:source.slice(i,end),offset:at});i=end;}
  else{result.push({kind:'punct',value:c,offset:at});i++;}
  if(result.length>50000)throw Error('TOKEN_LIMIT');
 }return result;
}
export type SqlReference={table:string;operation:CodeDatabaseOperation;offset:number;reason?:string};
export function sqlReferences(source:string):SqlReference[]{
 const all=tokens(source),result:SqlReference[]=[];let start=0;
 for(let end=0;end<=all.length;end++){if(end<all.length&&(all[end].kind!=='punct'||all[end].value!==';'))continue;const t=all.slice(start,end);start=end+1;const word=(i:number,value:string)=>t[i]?.kind==='word'&&t[i].value.toUpperCase()===value;const cte=word(0,'WITH');
  const add=(index:number,operation:CodeDatabaseOperation)=>{while(word(index,'IF')||word(index,'NOT')||word(index,'EXISTS')||word(index,'ONLY'))index++;let token=t[index];if(!token||!['word','identifier'].includes(token.kind))return;let reason=cte?'sql_cte_unresolved':undefined;if(t[index+1]?.value==='.'){if(token.value.toLowerCase()!=='main')reason='attached_schema_unresolved';index+=2;token=t[index];if(!token||!['word','identifier'].includes(token.kind))return;}result.push({table:token.value,operation,offset:token.offset,...(reason?{reason}:{})});};
  let depth=0,deleteTargetSeen=false;
  for(let i=0;i<t.length;i++){
   if(t[i].kind==='punct'&&t[i].value==='(')depth++;else if(t[i].kind==='punct'&&t[i].value===')')depth=Math.max(0,depth-1);
   if(word(i,'FROM')||word(i,'JOIN')){const target=word(i,'FROM')&&word(0,'DELETE')&&depth===0&&!deleteTargetSeen;if(target)deleteTargetSeen=true;add(i+1,target?'write':'read');}
   else if(word(i,'INSERT')){let j=i+1;if(word(j,'OR'))j+=2;if(word(j,'INTO'))add(j+1,'write');}
   else if(word(i,'UPDATE')){let j=i+1;if(word(j,'OR'))j+=2;add(j,'write');}
   else if((word(i,'CREATE')||word(i,'DROP'))&&(word(i+1,'TABLE')||word(i+1,'VIEW')))add(i+2,'schema');
   else if(word(i,'ALTER')&&word(i+1,'TABLE')){add(i+2,'schema');for(let j=i+3;j<t.length-1;j++)if(word(j,'RENAME')&&word(j+1,'TO'))add(j+2,'schema');}
  }
 }return result;
}
