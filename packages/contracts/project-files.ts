import type {InventoryDirectory, InventoryEntry} from './project-inventory.ts';

export type ProjectFilesPage = InventoryDirectory;
/** Legacy task pins are raw SHA256; fileRevision separately pins metadata/policy. */
export type ProjectFileReference = {
  relativePath:string; revision:string; revisionKind:'sha256'; fileRevision:string;
  rootIdentity:string; policyVersion:string; line:number;
};
type ProjectFileBase = {
  schemaVersion:'paos_project_file_v1'; projectId:string; rootIdentity:string;
  policyVersion:string; relativePath:string; observedAt:string; line:number;
  entry?:InventoryEntry; expectedRevision?:string; fileRevision?:string;
};
export type ProjectFileRead = ProjectFileBase & (
  | {state:'available';content:string;hash:string;redacted:boolean;fileRevision:string;reference:ProjectFileReference}
  | {state:'stale'|'unavailable'|'binary'|'too_large'|'unsupported'|'forbidden';content:null;reason:string}
);
