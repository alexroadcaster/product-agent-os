import type {InventoryCounts} from './project-inventory.ts';

export type ProjectScanStageKind='inventory'|'documents'|'code'|'analysis'|'schema'|'code_database';
export type ProjectScanState='queued'|'running'|'completed'|'partial'|'cancelled'|'interrupted'|'failed'|'recovery_required';
export type ProjectScanStageState='pending'|'running'|'completed'|'partial'|'unavailable'|'failed'|'cancelled';
export type ProjectScanStage={kind:ProjectScanStageKind;state:ProjectScanStageState;startedAt?:string;updatedAt:string;counts?:Record<string,number|null>;reasons:string[];data?:Record<string,unknown>;progress?:{completed:number;total:number}};
export type ProjectScan={
 schemaVersion:'paos_project_scan_v1';scanId:string;projectId:string;attempt:number;rootIdentity:string;policyVersion:string;
 requestedRevision:string|null;inventoryRevision:string|null;state:ProjectScanState;stage:ProjectScanStageKind|null;
 startedAt:string;updatedAt:string;finishedAt?:string;counts:InventoryCounts|null;reasons:string[];stages:ProjectScanStage[];
};
export type ProjectScanCapabilities=Record<ProjectScanStageKind,boolean>;
export type ProjectScanView={
 schemaVersion:'paos_project_scan_view_v1';projectId:string;version:number;latest:ProjectScan|null;lastSuccessful:ProjectScan|null;
 capabilities:ProjectScanCapabilities;limits:{concurrency:number;milliseconds:number;stageMilliseconds:number;resultBytes:number;queued:number};
 replayedScanId?:string;coalesced?:boolean;
};
