import {useEffect,useRef,type ReactNode} from 'react';

/** Native modal focus containment and Escape semantics; restore the opener when React removes the dialog. */
export function Modal({label,onDismiss,children}:{label:string;onDismiss:()=>void;children:ReactNode}){
 const ref=useRef<HTMLDialogElement>(null);
 useEffect(()=>{const dialog=ref.current!,opener=document.activeElement;dialog.showModal();return()=>{if(dialog.open)dialog.close();if(opener instanceof HTMLElement&&opener.isConnected)opener.focus();};},[]);
 return <dialog ref={ref} className="m2-modal" aria-label={label} onCancel={event=>{event.preventDefault();onDismiss();}} onKeyDown={event=>{
  if(event.key!=='Tab')return;
  // Keep the boundary inside the dialog instead of cycling through browser chrome in Chromium.
  const controls=Array.from(event.currentTarget.querySelectorAll<HTMLElement>('button:not(:disabled),input:not(:disabled):not([type=hidden]),select:not(:disabled),textarea:not(:disabled),a[href],[tabindex]:not([tabindex="-1"])')).filter(e=>e.getClientRects().length>0),first=controls[0],last=controls.at(-1);
  if(event.shiftKey&&document.activeElement===first){event.preventDefault();last?.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus();}
 }}>{children}</dialog>;
}
