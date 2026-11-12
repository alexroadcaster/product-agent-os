/** Rendered RGB-only audit. Gradients/native widget paint and assistive technology behavior require separate review. */
export function auditRenderedPage(){
 if(window.scrollX)window.scrollTo(0,window.scrollY);
 const visible=(e:Element)=>{const s=getComputedStyle(e);if(s.display==='none'||s.visibility==='hidden'||!e.getClientRects().length||e.closest('[inert]'))return false;for(let a:Element|null=e.parentElement;a;a=a.parentElement)if(a.tagName==='DETAILS'&&!a.hasAttribute('open')&&!a.querySelector(':scope>summary')?.contains(e))return false;return true;};
 const rgb=(s:string)=>{const a=s.match(/[\d.]+/g)?.map(Number)??[];return [a[0]??0,a[1]??0,a[2]??0,a[3]??1];};
 const blend=(a:number[],b:number[])=>a.slice(0,3).map((v,i)=>v*a[3]+b[i]*(1-a[3]));
 function background(e:Element|null):number[]{if(!e)return [255,255,255];return blend(rgb(getComputedStyle(e).backgroundColor),background(e.parentElement));}
 const luminance=(c:number[])=>c.map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4;}).reduce((v,n,i)=>v+n*[.2126,.7152,.0722][i],0);
 const contrast=(a:number[],b:number[])=>{const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);};
 const key=(e:Element)=>e.tagName.toLowerCase()+(e.getAttribute('name')?'[name='+e.getAttribute('name')+']':'')+(e.id?'#'+e.id:'');
 const findings:any[]=[],seen=new Set<string>();let textSamples=0,controlSamples=0;
 function inspect(e:Element){if(!visible(e)||e.closest('button:disabled,input:disabled,select:disabled,textarea:disabled,fieldset:disabled'))return;const s=getComputedStyle(e);if(s.backgroundImage!=='none')return;
  const bg=background(e),fg=blend(rgb(s.color),bg),ratio=contrast(fg,bg),large=parseFloat(s.fontSize)>=24||parseFloat(s.fontSize)>=18.6666667&&Number(s.fontWeight)>=700,minimum=large?3:4.5;textSamples++;
  if(ratio<minimum){const id='contrast:'+key(e)+':'+s.color+':'+bg.join();if(!seen.has(id)){seen.add(id);findings.push({kind:'text_contrast',element:key(e),ratio,minimum,foreground:s.color,background:bg});}}
 }
 const scope=document.querySelector('dialog:modal')??document.body;
 const walker=document.createTreeWalker(scope,NodeFilter.SHOW_TEXT);for(let n=walker.nextNode();n;n=walker.nextNode())if(n.textContent?.trim()&&n.parentElement)inspect(n.parentElement);
 for(const e of scope.querySelectorAll('input:not([type=checkbox]):not([type=radio]):not([type=hidden]),select,textarea')){if(!visible(e)||e.matches(':disabled'))continue;inspect(e);const s=getComputedStyle(e);controlSamples++;const border=rgb(s.borderTopColor),outside=background(e.parentElement),inside=background(e),ratio=Math.min(contrast(blend(border,outside),outside),contrast(blend(border,inside),inside));if(parseFloat(s.borderTopWidth)>0&&ratio<3)findings.push({kind:'control_boundary',element:key(e),ratio,minimum:3});}
 const ids=new Set<string>();for(const e of document.querySelectorAll('[id]')){if(ids.has(e.id))findings.push({kind:'duplicate_id',id:e.id});ids.add(e.id);}
 const overflow=Array.from(document.querySelectorAll('main *,header *,aside.navigation *')).filter(visible).map(e=>({element:key(e),right:e.getBoundingClientRect().right,width:e.getBoundingClientRect().width})).filter(e=>e.right>innerWidth+1).slice(0,12);
 return {findings,textSamples,controlSamples,geometry:{width:innerWidth,scroll:document.documentElement.scrollWidth},overflow,lang:document.documentElement.lang,theme:document.documentElement.dataset.theme,limitations:['RGB computed styles; gradients and native widget paint excluded','No manual screen-reader certification']};
}

/** Native focus must expose an action even inside nested scroll containers. */
export async function auditFocusedControls(){
 const scope=document.querySelector('dialog:modal')??document.body,original=document.activeElement,scrolls=Array.from(document.querySelectorAll('*')).filter(e=>e.scrollLeft||e.scrollTop).map(e=>[e,e.scrollLeft,e.scrollTop] as const),x=scrollX,y=scrollY;
 const findings:any[]=[];let samples=0;
 for(const e of scope.querySelectorAll<HTMLElement>('button,input:not([type=hidden]),select,textarea,a[href],summary,[tabindex="0"]')){
  if(e.matches(':disabled')||e.closest('[inert]')||!e.getClientRects().length||getComputedStyle(e).visibility==='hidden')continue;
  if(Array.from(e.parentElement?.closest('details:not([open])')?[e.parentElement.closest('details:not([open])')]:[]).some(d=>!d?.querySelector(':scope>summary')?.contains(e)))continue;
  const leavingDisclosure=Boolean(document.querySelector('.navigation.open'))&&!e.closest('.navigation');
  e.focus();if(leavingDisclosure)await new Promise(r=>requestAnimationFrame(r));else await Promise.resolve();if(document.activeElement!==e)continue;samples++;
  const r=e.getBoundingClientRect();let left=Math.max(0,r.left),right=Math.min(innerWidth,r.right),top=Math.max(0,r.top),bottom=Math.min(innerHeight,r.bottom);
  for(let a=e.parentElement;a;a=a.parentElement){const s=getComputedStyle(a),b=a.getBoundingClientRect();if(/auto|scroll|hidden|clip/.test(s.overflowX)){left=Math.max(left,b.left);right=Math.min(right,b.right);}if(/auto|scroll|hidden|clip/.test(s.overflowY)){top=Math.max(top,b.top);bottom=Math.min(bottom,b.bottom);}}
  const shape=e instanceof SVGElement?e.querySelector('circle')?.getBoundingClientRect():null;
  const hit=right>left&&bottom>top?document.elementFromPoint(shape?(shape.left+shape.right)/2:(left+right)/2,shape?(shape.top+shape.bottom)/2:(top+bottom)/2):null;
  if(right-left<Math.min(8,r.width)||bottom-top<Math.min(8,r.height)||!hit||!(e===hit||e.contains(hit)))findings.push({element:e.tagName.toLowerCase(),name:e.getAttribute('name')??e.textContent?.trim().slice(0,65),rect:{left:r.left,right:r.right,top:r.top,bottom:r.bottom},reason:'focused_action_clipped_or_obscured'});
 }
 if(original instanceof HTMLElement&&original.isConnected)original.focus({preventScroll:true});for(const [e,left,top]of scrolls){e.scrollLeft=left;e.scrollTop=top;}window.scrollTo(x,y);
 return {samples,findings};
}
