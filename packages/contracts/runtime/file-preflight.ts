import type {InventoryPolicy} from '../project-inventory.ts';

export const EXECUTION_FILE_LIMITS=Object.freeze({files:32,fileBytes:65536,totalBytes:524288});
export type ExecutionFileOperation='read'|'create'|'modify'|'delete'|'rename'|'create_or_modify_after_discovery'|'create_or_modify';
export type ExecutionFileRequest={relativePath:string;previousRelativePath?:string;plannedOperation?:ExecutionFileOperation|null;revision?:string|null;fileRevision?:string|null};
export type ExecutionFileProject=({id?:string;canonicalRoot:string;rootIdentity:string}|{projectId?:string;workspaceRoot:string;directoryIdentity:string})&{inventoryPolicy?:InventoryPolicy};
export type FilePreflightItem={path:string;operation:ExecutionFileOperation;role:'target'|'rename_source'|'rename_destination';state:'present'|'missing'|'excluded'|'stale'|'invalid'|'conflict'|'not_checked';allowed:boolean;reason?:string;byteSize?:number;sha256?:string;fileRevision?:string;redacted?:boolean};
/** This public report deliberately contains no file contents or diffs. */
export type FilePreflight={schemaVersion:'paos_file_preflight_v1';allowed:boolean;rootIdentity:string;policyVersion:string;inventoryRevision:string;observedAt:string;limits:typeof EXECUTION_FILE_LIMITS;counts:{requested:number;paths:number;present:number;missing:number;excluded:number;totalBytes:number;bytesComplete:boolean};items:FilePreflightItem[];reasons:string[];digest:string;truncated?:boolean};
