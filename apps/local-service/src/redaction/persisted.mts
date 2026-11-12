/** Known credential forms only. This is a conservative local filter, not a guarantee of detecting every secret. */
export function safePersistedText(value:string):string {
 return value.replace(/-----BEGIN [^-]*PRIVATE KEY-----[\s\S]*?-----END [^-]*PRIVATE KEY-----/g,'[redacted]')
 .replace(/\bsk-[A-Za-z0-9_-]{12,}/g,'[redacted]').replace(/\bBearer\s+[A-Za-z0-9._~+\/-]{12,}/gi,'Bearer [redacted]')
 .replace(/((?:["']?)(?:password|passwd|api[_-]?key|access[_-]?token|secret|token)(?:["']?)\s*[:=]\s*)(?:"[^"]*"|'[^']*'|[^\s,;]+)/gi,'$1[redacted]');
}
export function safeVisibleValue<T>(value:T):T {
 return JSON.parse(JSON.stringify(value,(key,item)=>{if(isHiddenMessage(item))return {unavailable:'hidden_content_excluded'};if(/^(?:password|passwd|api[_-]?key|access[_-]?token|private[_-]?key|secret)$/i.test(key))return '[redacted]';return typeof item==='string'?safePersistedText(item):item;}));
}
export function isHiddenMessage(value:unknown):boolean{if(!value||typeof value!=='object')return false;const r=value as Record<string,unknown>,d=(r.data&&typeof r.data==='object'?r.data:r) as Record<string,unknown>;return d.hidden===true||['reasoning','analysis','hidden_reasoning'].includes(String(d.role))||['analysis','hidden','reasoning'].includes(String(d.channel??d.visibility??d.type));}
/** Only user-visible runtime fields; private lease/binding authentication remains byte-exact. */
export function safeRuntimeData(data:Record<string,unknown>):Record<string,unknown>{
 const result={...data};for(const key of ['appAgentRun','runtimeRun']){
  const run=result[key];if(!run||typeof run!=='object')continue;
  const row={...run as Record<string,unknown>};for(const field of ['input','progress','lastReport','taskContext','operations','assetPins','proposalContext'])if(row[field]!==undefined)row[field]=safeVisibleValue(row[field]);result[key]=row;
 }return result;
}
