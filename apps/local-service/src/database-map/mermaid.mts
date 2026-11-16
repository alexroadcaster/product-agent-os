import {createHash} from 'node:crypto';
import type {DatabaseTable} from '../../../../packages/contracts/database-map.ts';
export const databaseEntityId=(name:string)=>'T_'+createHash('sha256').update(name).digest('hex').slice(0,16);
const id=databaseEntityId;
const label=(name:string)=>Array.from(name).map(c=>/[A-Za-z0-9 _.-]/.test(c)?c:'#'+c.codePointAt(0)+';').join('');
const field=(name:string)=>'c_'+Buffer.from(name).toString('hex');
/** Export keeps stable encoded identifiers and entity-escaped readable aliases/comments; no source string becomes Mermaid syntax. */
export function databaseMermaid(tables:DatabaseTable[]){
 const lines=['erDiagram'],names=new Map(tables.map(t=>[t.name,t]));
 for(const t of tables){lines.push('  '+id(t.name)+'["'+label(t.name)+'"] {');for(const c of t.columns)lines.push('    '+(/^[A-Za-z][A-Za-z0-9_]*$/.test(c.type)?c.type:'unknown')+' '+field(c.name)+(c.primaryKeyPosition?' PK':'')+' "'+label(c.name)+'"');lines.push('  }');}
 for(const t of tables){const groups=new Map<number,typeof t.foreignKeys>();for(const fk of t.foreignKeys)groups.set(fk.id,[...(groups.get(fk.id)??[]),fk]);for(const [key,fks] of groups){if(!names.has(fks[0].targetTable))continue;const cols=fks.map(f=>f.from).sort(),nullable=cols.some(n=>t.columns.find(c=>c.name===n)?.nullable!==false),primary=t.columns.filter(c=>c.primaryKeyPosition>0).map(c=>c.name).sort(),unique=JSON.stringify(cols)===JSON.stringify(primary)||t.indexes.some(i=>i.unique&&!i.partial&&JSON.stringify(i.columns.filter(c=>c.key&&c.name).map(c=>c.name!).sort())===JSON.stringify(cols));lines.push('  '+id(fks[0].targetTable)+' '+(nullable?'o|':'||')+'--'+(unique?'o|':'o{')+' '+id(t.name)+' : fk_'+key);}}
 return lines.join('\n')+'\n';
}
