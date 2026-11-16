import type {ProjectScanView} from '../../../../../packages/contracts/project-scan.ts';

const terminal=new Set(['completed','partial','cancelled','interrupted','failed','recovery_required']);
/** Record versions order responses; attempt/scope pins prevent a stale job from reopening. */
export function mergeScanView(projectId:string,previous:ProjectScanView|undefined,incoming:ProjectScanView):ProjectScanView|undefined{
 const current=previous?.projectId===projectId?previous:undefined;
 if(!incoming||incoming.schemaVersion!=='paos_project_scan_view_v1'||incoming.projectId!==projectId||!Number.isSafeInteger(incoming.version)||incoming.version<0)return current;
 if(incoming.latest!==null&&(!incoming.latest||incoming.latest.projectId!==projectId||incoming.latest.schemaVersion!=='paos_project_scan_v1'))return current;
 if(incoming.lastSuccessful!==null&&(!incoming.lastSuccessful||incoming.lastSuccessful.projectId!==projectId||incoming.lastSuccessful.schemaVersion!=='paos_project_scan_v1'))return current;
 if(!current)return incoming;
 if(incoming.version<=current.version)return current;
 const before=current.latest,next=incoming.latest;
 if(before&&!next)return current;
 if(before&&next){
  if(next.attempt<before.attempt)return current;
  if(next.attempt===before.attempt){
   if(next.scanId!==before.scanId||next.rootIdentity!==before.rootIdentity||next.policyVersion!==before.policyVersion)return current;
   if(before.inventoryRevision&&next.inventoryRevision!==before.inventoryRevision)return current;
   if(terminal.has(before.state)&&next.state!==before.state)return current;
  }
 }
 return incoming;
}
