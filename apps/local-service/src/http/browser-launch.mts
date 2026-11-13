import {randomBytes,timingSafeEqual} from 'node:crypto';
import type {createSessionGate} from './session-gate.mts';

type Gate=ReturnType<typeof createSessionGate>;
const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
const secureHeaders={
 'cache-control':'no-store','referrer-policy':'no-referrer','x-content-type-options':'nosniff',
 'x-frame-options':'DENY','cross-origin-opener-policy':'same-origin','cross-origin-resource-policy':'same-origin',
 vary:'Sec-Fetch-Site, Sec-Fetch-Mode, Sec-Fetch-Dest, Sec-Fetch-User',
};

/** Direct desktop navigation is user intent, not launcher identity. Native HTTP clients are outside this boundary.
 * Fail closed for unsupported metadata; keep all bootstrap material in memory/body/HttpOnly cookie, never URLs. */
export function createBrowserLaunch({gate,instanceId,now=Date.now}:{gate:Gate;instanceId:string;now?:()=>number}){
 const cookieName=`paos_launch_${instanceId}`;
 const pending=new Map<string,{proof:string;expiresAt:number}>();
 const cookie=(token:string)=>`${cookieName}=${token}; HttpOnly; SameSite=Strict; Path=/bootstrap/launch; Max-Age=30`;
 function sweep(){for(const [key,value] of pending)if(value.expiresAt<=now())pending.delete(key);}
 function navigate(request:Request){
  gate.validateOrigin(request,false);
  const h=request.headers,url=new URL(request.url);
  if(request.method!=='GET'||url.pathname!=='/launch'||url.search||url.username||url.password
   ||h.get('sec-fetch-site')!=='none'||h.get('sec-fetch-mode')!=='navigate'||h.get('sec-fetch-dest')!=='document'
   ||h.get('sec-fetch-user')!=='?1'||h.has('origin')||h.has('referer')
   ||['x-forwarded-for','x-forwarded-proto','x-forwarded-port'].some(key=>h.has(key)))fail('LAUNCH_REJECTED');
  try{gate.authorize(request);return new Response(null,{status:303,headers:{...secureHeaders,location:'/'}});}
  catch(error){if((error as any)?.code!=='SESSION_REQUIRED')throw error;}
  sweep();if(pending.size>=16)pending.delete(pending.keys().next().value!);
  const token=randomBytes(32).toString('hex'),proof=randomBytes(32).toString('hex'),nonce=randomBytes(18).toString('base64');
  pending.set(token,{proof,expiresAt:now()+30_000});
  const html=`<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Product-Agent OS</title><style nonce="${nonce}">body{font:18px system-ui;margin:15vh auto;padding:24px;max-width:640px;color:#eee;background:#242421}p{line-height:1.6}</style><main><h1>Product-Agent OS</h1><p role="status" id="status">Открываем рабочее пространство…</p></main><script nonce="${nonce}">const proof="${proof}";fetch("/bootstrap/launch",{method:"POST",credentials:"same-origin",headers:{"content-type":"application/json"},body:JSON.stringify({proof})}).then(response=>{if(!response.ok)throw new Error();location.replace("/");}).catch(()=>{document.getElementById("status").textContent="Не удалось открыть приложение. Запустите Product-Agent OS ещё раз. Вводить коды не нужно.";});</script></html>`;
  return new Response(html,{headers:{...secureHeaders,'content-type':'text/html; charset=utf-8','set-cookie':cookie(token),
   'content-security-policy':`default-src 'none'; script-src 'nonce-${nonce}'; style-src 'nonce-${nonce}'; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'`}});
 }
 function exchange(request:Request,proof:unknown){
  gate.validateOrigin(request,true);
  const h=request.headers,url=new URL(request.url);
  if(request.method!=='POST'||url.pathname!=='/bootstrap/launch'||url.search
   ||h.get('content-type')?.split(';')[0].trim()!=='application/json'||h.get('sec-fetch-site')!=='same-origin'
   ||!['cors','same-origin'].includes(h.get('sec-fetch-mode')??'')||h.get('sec-fetch-dest')!=='empty'
   ||['x-forwarded-for','x-forwarded-proto','x-forwarded-port'].some(key=>h.has(key)))fail('LAUNCH_REJECTED');
  sweep();const matches=(h.get('cookie')??'').split(';').map(c=>c.trim()).filter(c=>c.startsWith(cookieName+'='));
  const token=matches.length===1?matches[0].slice(cookieName.length+1):'',value=pending.get(token);
  if(!value||typeof proof!=='string'||!/^[a-f0-9]{64}$/.test(proof)||!timingSafeEqual(Buffer.from(proof),Buffer.from(value.proof)))fail('LAUNCH_REJECTED');
  pending.delete(token); // Consume synchronously before issuing a session: concurrent exchange cannot replay.
  const session=gate.createSession(),headers=new Headers({...secureHeaders,'content-type':'application/json; charset=utf-8'});
  headers.append('set-cookie',session.cookie);headers.append('set-cookie',`${cookieName}=; HttpOnly; SameSite=Strict; Path=/bootstrap/launch; Max-Age=0`);
  return new Response(JSON.stringify({csrfToken:session.csrfToken,instanceId,actorId:'local-user'}),{headers});
 }
 return {navigate,exchange,revoke:()=>pending.clear()};
}
