/** The source owner is explicit; applying never mirrors a workspace file into SQL or vice versa. */
export type DocumentTargetSource=
 | {origin:'local_store';entityId:string;entityRevision:number}
 | {origin:'workspace_file';path:string;rootIdentity:string;policyVersion:string;fileRevision:string;rawHash:string};
export type DocumentApplyState='prepared'|'applied'|'not_applied'|'recovery_required'|'rolled_back';
export type DocumentApplyOutcome={operationId:string;proposalId:string;action:'apply'|'rollback';state:DocumentApplyState;beforeHash:string;afterHash:string;accepted:false;origin:DocumentTargetSource['origin'];reason?:string};
export type DocumentApplyPreview={proposalId:string;proposalRevision:number;action:'apply'|'rollback';previewDigest:string;source:DocumentTargetSource;before:string;after:string;beforeHash:string;afterHash:string;executable:true;accepted:false};
export type DocumentApplyInput={proposalId:string;proposalRevision:number;previewDigest:string;epoch:number;idempotencyKey:string};
/** Private recovery bytes are exclusively accessed through LocalStore's service-only journal port.
 * They must never become public entities, events, artifact search rows, or HTTP responses. */
export type DocumentApplyRecord={operationId:string;proposalId:string;proposalRevision:number;action:'apply'|'rollback';idempotencyKey:string;requestDigest:string;state:DocumentApplyState;source:DocumentTargetSource;scopeFingerprint:string;generation:string;authorityEpoch:number;beforeHash:string;afterHash:string;beforeBase64:string;afterBase64:string;createdAt:string;result:DocumentApplyOutcome;nativeOwner?:{processId:number;temporaryDirectory:string;directoryIdentity:string}};
export type DocumentApplyJournal={version:number;records:DocumentApplyRecord[]};
