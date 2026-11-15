import {useEffect,useLayoutEffect,useRef,type ReactNode} from 'react';

function containFocus(event:React.KeyboardEvent<HTMLDialogElement>){
 if(event.key!=='Tab')return;
 const controls=Array.from(event.currentTarget.querySelectorAll<HTMLElement>('button:not(:disabled),input:not(:disabled):not([type=hidden]),select:not(:disabled),textarea:not(:disabled),a[href],[tabindex]:not([tabindex="-1"])')).filter(e=>e.getClientRects().length>0),first=controls[0],last=controls.at(-1);
 if(event.shiftKey&&document.activeElement===first){event.preventDefault();last?.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus();}
}

/** Promote the same detail DOM into the top layer so raw inputs and pending previews survive expansion. */
export function DetailSurface({label,expanded,onCollapse,children}:{label:string;expanded:boolean;onCollapse:()=>void;children:ReactNode}){
 const ref=useRef<HTMLDialogElement>(null),opener=useRef<HTMLElement|null>(null),wasExpanded=useRef(false);
 useLayoutEffect(()=>{
  const dialog=ref.current!;
  if(expanded)opener.current=document.activeElement instanceof HTMLElement?document.activeElement:null;
  if(dialog.open)dialog.close();
  if(expanded){dialog.showModal();dialog.scrollTop=0;dialog.querySelector<HTMLElement>('[data-testid="task-expand"]')?.focus({preventScroll:true});}else dialog.show();
  if(!expanded&&wasExpanded.current&&opener.current?.isConnected)opener.current.focus();
  wasExpanded.current=expanded;
 },[expanded]);
 useEffect(()=>()=>{if(ref.current?.open)ref.current.close();if(wasExpanded.current&&opener.current?.isConnected)opener.current.focus();},[]);
 return <dialog ref={ref} className={`task-detail-surface${expanded?' task-detail-overlay':''}`} data-testid="task-detail-surface" aria-label={label} aria-modal={expanded?'true':undefined} onCancel={event=>{if(expanded){event.preventDefault();onCollapse();}}} onKeyDown={expanded?containFocus:undefined}>{children}</dialog>;
}

/** Native modal focus containment and Escape semantics; restore the opener when React removes the dialog. */
export function Modal({label,onDismiss,children}:{label:string;onDismiss:()=>void;children:ReactNode}){
 const ref=useRef<HTMLDialogElement>(null);
 useEffect(()=>{const dialog=ref.current!,opener=document.activeElement;dialog.showModal();return()=>{if(dialog.open)dialog.close();if(opener instanceof HTMLElement&&opener.isConnected)opener.focus();};},[]);
 return <dialog ref={ref} className="m2-modal" aria-label={label} onCancel={event=>{event.preventDefault();onDismiss();}} onKeyDown={containFocus}>{children}</dialog>;
}
