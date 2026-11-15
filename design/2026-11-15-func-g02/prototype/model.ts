export type Node={id:string;kind:string;name:string;relativePath:string;line:number};
export type Edge={id:string;from:string;to:string;type:string;relativePath:string;line:number;resolution:string;dynamic?:boolean|null;typeOnly?:boolean|null;columns?:string[];parentColumns?:string[]};
export type Snapshot={meta:{engine:string;version:string;sourceRevision:string;rootIdentity:string;coverage:{status:string;reasons:string[]};capabilities:Record<string,boolean>;warnings:string[]};nodes:Node[];edges:Edge[];tables?:any[];sourceFiles?:Record<string,string>};
export type State={project:string;route:string;engine:string;view:string;selected:string;query:string;direction:string;type:string;focus:string;target:string;phase:string;locale:'ru'|'en';theme:'light'|'dark'};
export const defaults:State={project:'a',route:'map',engine:'f30',view:'list',selected:'',query:'',direction:'all',type:'all',focus:'none',target:'',phase:'ready',locale:'ru',theme:'light'};
const allowed:Partial<Record<keyof State,string[]>>={project:['a','b'],route:['map','database','files','source'],engine:['f30','f31','f32','contract'],view:['list','graph','mermaid'],direction:['all','incoming','outgoing'],type:['all','static','dynamic','type-only'],focus:['none','cycle','path','impact'],phase:['ready','loading','empty','partial','error','unavailable','stale'],locale:['ru','en'],theme:['light','dark']};
export function decode(search:string):State{const query=new URLSearchParams(search),state={...defaults};for(const key of Object.keys(defaults) as (keyof State)[]){const value=query.get(key);if(value!==null&&value.length<=300&&(!allowed[key]||allowed[key]!.includes(value)))(state as any)[key]=value;}return state;}
export function encode(state:State){return '?'+new URLSearchParams(Object.entries(state).filter(([key,value])=>value!==defaults[key as keyof State])).toString();}
export function switchProject(state:State,project:string):State{return {...state,project,route:'map',engine:'f30',type:'all',selected:'',query:'',target:'',focus:'none',direction:'all',phase:'ready'};}
export function visible(snapshot:Snapshot,state:State){
 const typed=snapshot.edges.filter(e=>state.type==='all'||state.type==='dynamic'&&e.dynamic===true||state.type==='type-only'&&e.typeOnly===true||state.type==='static'&&e.dynamic===false&&e.typeOnly===false);
 const incident=state.direction==='all'||!state.selected?typed:typed.filter(e=>state.direction==='incoming'?e.to===state.selected:e.from===state.selected);
 const matching=new Set(snapshot.nodes.filter(n=>(n.name+' '+n.relativePath).toLowerCase().includes(state.query.toLowerCase())).map(n=>n.id));
 let nodes=snapshot.nodes.filter(n=>matching.has(n.id));
 if(state.direction!=='all'&&state.selected){const ids=new Set(incident.flatMap(e=>[e.from,e.to]));ids.add(state.selected);nodes=nodes.filter(n=>ids.has(n.id));}
 const ids=new Set(nodes.map(n=>n.id));return {nodes,edges:incident.filter(e=>ids.has(e.from)&&ids.has(e.to))};
}
export function pathEdges(edges:Edge[],from:string,to:string){
 if(!from||!to||from===to)return new Set<string>();const queue=[from],previous=new Map<string,Edge>(),seen=new Set([from]);
 for(let i=0;i<queue.length;i++)for(const edge of edges.filter(e=>e.from===queue[i])){if(seen.has(edge.to))continue;seen.add(edge.to);previous.set(edge.to,edge);queue.push(edge.to);}
 if(!seen.has(to))return new Set<string>();const result=new Set<string>();for(let at=to;at!==from;){const edge=previous.get(at)!;result.add(edge.id);at=edge.from;}return result;
}
export function highlight(edges:Edge[],state:State){
 if(state.focus==='path')return pathEdges(edges,state.selected,state.target);
 if(state.focus==='impact'){const seen=new Set([state.selected]),result=new Set<string>();let changed=true;while(changed){changed=false;for(const edge of edges)if(seen.has(edge.to)&&!seen.has(edge.from)){seen.add(edge.from);result.add(edge.id);changed=true;}}return result;}
 if(state.focus==='cycle')return new Set(edges.filter(e=>e.from===e.to||pathEdges(edges,e.to,e.from).size>0).map(e=>e.id));
 return new Set<string>();
}
/** Stable generated Mermaid identifiers separate syntax from source-owned display labels. */
export function flowchart(nodes:Node[],edges:Edge[]){const ids=new Map(nodes.map((n,i)=>[n.id,'n'+i]));const escape=(value:string)=>[...value].map(c=>/[\p{L}\p{N} _./:-]/u.test(c)?c:'#'+c.codePointAt(0)+';').join('');return 'flowchart LR\n'+nodes.map(n=>`${ids.get(n.id)}["${escape(n.name)}"]`).join('\n')+'\n'+edges.filter(e=>ids.has(e.from)&&ids.has(e.to)).map(e=>`${ids.get(e.from)} -->|${e.type}| ${ids.get(e.to)}`).join('\n');}
export function contractFixture():Snapshot{return {meta:{engine:'proposed-contract fixture — NOT CBM output',version:'unmeasured',sourceRevision:'synthetic-interface-v1',rootIdentity:'synthetic-code-project-a',coverage:{status:'contract_fixture',reasons:['Not an engine measurement']},capabilities:{calls:true,definitions:true,references:true,impact:true},warnings:['Reference UI only; no measured CBM graph']},nodes:[{id:'run',kind:'symbol',name:'run',relativePath:'src/lib.ts',line:2},{id:'helper',kind:'symbol',name:'helper',relativePath:'src/lib.ts',line:1}],edges:[{id:'fixture-call',from:'run',to:'helper',type:'call',relativePath:'src/lib.ts',line:2,resolution:'ground_truth_fixture'}]};}

/** Source and schema exports share the selected project's bounded snapshot. */
export function projectSources(project:string,sources:Record<string,string>){return project==='a'?sources:{};}
export function schemaMermaid(snapshot:Snapshot){
 const identifier=(name:string)=>/^[A-Za-z_][A-Za-z_0-9]*$/.test(name)?name:'u_'+[...name].map(c=>c.codePointAt(0)!.toString(16)).join('_');
 const names=new Map(snapshot.nodes.map(n=>[n.id,identifier(n.name)]));
 const tables=(snapshot.tables??[]).filter(t=>snapshot.nodes.some(n=>n.name===t.name));
 const lines=['erDiagram'];
 for(const table of tables){lines.push(identifier(table.name)+' {');for(const column of table.columns)lines.push('  '+identifier(column.type||'UNKNOWN')+' '+identifier(column.name)+(column.primaryKeyPosition?' PK':''));lines.push('}');}
 for(const edge of snapshot.edges)if(names.has(edge.from)&&names.has(edge.to))lines.push(`${names.get(edge.from)} }o--o| ${names.get(edge.to)} : declared_FK`);
 return lines.join('\n')+'\n';
}
