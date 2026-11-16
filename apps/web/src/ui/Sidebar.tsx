import {Fragment,useEffect,useRef,useState} from 'react';
import type {Project} from '../api/client.ts';
import {Icon,type IconName} from './Icon.tsx';

// DesignBookmark unit-mass springs: four semi-implicit Euler substeps, dt <= 1/30.
export const SIDEBAR_SPRINGS={width:[260,24],rotation:[300,22],highlight:[380,28],label:[300,26]} as const;
export function Sidebar({items,selected,onSelect,projects,projectId,onProject,ready,locale,mobileNav,onEscape,connection}:{items:{id:IconName;label:string}[];selected:string;onSelect:(id:IconName)=>void;projects:Project[];projectId:string;onProject:(id:string)=>void;ready:boolean;locale:'ru'|'en';mobileNav:boolean;onEscape:()=>void;connection:{verified:boolean;label:string;reason?:string}}){
 const [expanded,setExpanded]=useState(true),[tip,setTip]=useState<{text:string;top:number;left:number}>();
 const side=useRef<HTMLElement>(null),nav=useRef<HTMLElement>(null),toggle=useRef<HTMLButtonElement>(null),pill=useRef<HTMLSpanElement>(null),control=useRef<{expand:(value:boolean)=>void;select:()=>void}|undefined>(undefined);
 const w=(ru:string,en:string)=>locale==='ru'?ru:en;
 useEffect(()=>{
  const element=side.current!,menu=nav.current!,media=matchMedia('(prefers-reduced-motion: reduce)');
  const spring=(x:number,pair:readonly[number,number])=>({x,v:0,t:x,k:pair[0],c:pair[1]});
  const width=spring(216,SIDEBAR_SPRINGS.width),rotation=spring(0,SIDEBAR_SPRINGS.rotation),highlight=spring(0,SIDEBAR_SPRINGS.highlight);
  const labels=Array.from(element.querySelectorAll<HTMLElement>('.sidebar-label')).map(el=>({el,s:spring(1,SIDEBAR_SPRINGS.label),delay:0}));
  let expanded=true,frame=0,last=0;
  const springs=[width,rotation,highlight,...labels.map(l=>l.s)];
  const paint=()=>{element.style.width=width.x+'px';element.closest<HTMLElement>('.app')?.style.setProperty('--sidebar-width',width.x+'px');toggle.current?.firstElementChild?.setAttribute('style',`transform:rotate(${rotation.x*180}deg)`);for(const l of labels){const p=Math.max(0,Math.min(1,l.s.x));l.el.style.opacity=String(p);l.el.style.transform=`translateX(${(1-p)*-10}px)`;}if(pill.current)pill.current.style.transform=`translateY(${highlight.x}px)`;};
  const snap=()=>{cancelAnimationFrame(frame);frame=0;for(const s of springs){s.x=s.t;s.v=0;}for(const l of labels)l.delay=0;paint();};
  function tick(now:number){const dt=Math.min((now-last)/1000,1/30);last=now;for(const l of labels)if(l.delay>0){l.delay-=dt;if(l.delay<=0)l.s.t=expanded?1:0;}for(let i=0;i<4;i++)for(const s of springs){const h=dt/4;s.v+=(-s.k*(s.x-s.t)-s.c*s.v)*h;s.x+=s.v*h;}paint();frame=0;if(springs.some(s=>Math.abs(s.x-s.t)>.005||Math.abs(s.v)>.01)||labels.some(l=>l.delay>0))frame=requestAnimationFrame(tick);else snap();}
  function wake(){if(media.matches){labels.forEach(l=>l.s.t=expanded?1:0);snap();}else if(!frame){last=performance.now();frame=requestAnimationFrame(tick);}}
  function select(){const button=menu.querySelector<HTMLElement>('[aria-current="page"]');if(button&&pill.current){highlight.t=button.getBoundingClientRect().top-menu.getBoundingClientRect().top+menu.scrollTop;pill.current.style.height=button.getBoundingClientRect().height+'px';wake();}}
  control.current={expand(value){expanded=value;width.t=value?216:64;rotation.t=value?0:1;labels.forEach((l,i)=>{l.delay=value?.06+i*.04:0;if(!value)l.s.t=0;});wake();},select};
  const change=()=>{if(media.matches){labels.forEach(l=>l.s.t=expanded?1:0);snap();}};
  const resize=()=>{setTip(undefined);select();};media.addEventListener('change',change);window.addEventListener('resize',resize);select();
  return()=>{cancelAnimationFrame(frame);media.removeEventListener('change',change);window.removeEventListener('resize',resize);control.current=undefined;};
 },[]);
 useEffect(()=>{control.current?.expand(expanded);setTip(undefined);},[expanded]);
 useEffect(()=>{control.current?.select();setTip(undefined);},[selected,locale]);
 function showTip(button:HTMLElement,text:string){if(expanded)return;const rect=button.getBoundingClientRect();setTip({text,top:Math.max(8,Math.min(innerHeight-52,rect.top)),left:side.current!.getBoundingClientRect().right+8});}
 return <><aside ref={side} id="project-navigation" className={'navigation v3-navigation '+(mobileNav?'open':'')} data-collapsed={!expanded} aria-label={w('Навигация','Navigation')} onKeyDown={e=>{if(e.key==='Escape'){setTip(undefined);onEscape();}}}>
  <div className="sidebar-brand"><div className="brand sidebar-label"><span className="brand-mark" aria-hidden="true">P</span>Product-Agent OS<span>{w('Рабочая среда','Workspace')}</span></div><button ref={toggle} className="sidebar-toggle" aria-expanded={expanded} aria-controls="sidebar-links" aria-label={w(expanded?'Свернуть меню':'Развернуть меню',expanded?'Collapse sidebar':'Expand sidebar')} onClick={()=>setExpanded(!expanded)}><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="m14 6-6 6 6 6" fill="none" stroke="currentColor" strokeWidth="1.8"/></svg></button></div>
  <label className="sidebar-project" hidden={!expanded}><span className="project-avatar"><Icon name="portfolio"/></span><span className="project-picker-label">{w('Проект','Project')}</span><select value={projectId} disabled={!ready} onChange={e=>onProject(e.target.value)}><option value="">—</option>{projects.map(p=><option key={p.id} value={p.id}>{p.name}</option>)}</select></label>
  {!expanded&&<button className="collapsed-project" disabled={!ready} aria-label={w('Выбрать проект','Select project')} onClick={()=>setExpanded(true)}><Icon name="portfolio"/></button>}
  <nav ref={nav} id="sidebar-links" onScroll={()=>setTip(undefined)}><span ref={pill} className="sidebar-highlight" aria-hidden="true"/>{items.map((item,i)=><Fragment key={item.id}>{(['portfolio','files','autonomy','search'].includes(item.id))&&<span className="nav-group-label sidebar-label">{item.id==='portfolio'?w('Работа','Work'):item.id==='files'?w('Знания','Knowledge'):item.id==='autonomy'?w('Управление','Management'):w('Среда','Workspace')}</span>}<button className={'nav-link '+(['overview','documents','search'].includes(item.id)?'nav-group-start':'')} disabled={!ready} aria-label={item.label} aria-current={selected===item.id?'page':undefined} title={expanded?undefined:item.label} onPointerEnter={e=>showTip(e.currentTarget,item.label)} onPointerLeave={()=>setTip(undefined)} onFocus={e=>showTip(e.currentTarget,item.label)} onBlur={()=>setTip(undefined)} onClick={()=>onSelect(item.id)}><Icon name={item.id}/><span className="sidebar-label">{item.label}</span></button></Fragment>)}</nav>
  <div className="connection" title={connection.label}><span className={'connection-dot '+(connection.verified?'verified':'')} aria-hidden="true"/><div className="sidebar-label"><strong>{connection.label}</strong><small>{connection.reason}</small></div></div>
 </aside>{tip&&<div role="tooltip" className="sidebar-tooltip" style={{top:tip.top,left:tip.left}}>{tip.text}</div>}</>;
}
