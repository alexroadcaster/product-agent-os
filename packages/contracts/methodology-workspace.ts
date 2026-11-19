export type MethodologyTechnicalState = 'passed'|'failed'|'partial'|'missing'|'stale';
export type MethodologyEvidenceView = {
  schemaVersion:'paos_methodology_evidence_v1';projectId:string;taskId:string;taskRevision:number;
  taskSpecRevision:string;sourceRevision:string|null;
  criteria:{id:string;criterion:string;owner:string;technical:MethodologyTechnicalState;human:'accepted'|'not_observed';
    receipt:{runId:string;operationId:string;route:'native_command_broker';inputDigest:string;environmentRevision:string}|null}[];
  humanAcceptance:'accepted'|'declined'|'not_observed';releaseAcceptance:'not_evaluated';
  coverage:'bounded_history'|'observed_history';
  recovery:{state:'observation_pending'|'reconcile_required';runId:string;operationId:string}|null;
};
export type MethodologyDisposition = 'use_recommendation'|'review_required'|'accepted_gap';
export type MethodologyDecisionCommand = {
  expectedRevision:number;taskRevision:number;scopeDigest:string;idempotencyKey:string;
  disposition:MethodologyDisposition;criterionId:string|null;reason:string;
};
export type MethodologyDecisionEntry = {
  taskRevision:number;scopeDigest:string;disposition:MethodologyDisposition;criterionId:string|null;
  reason:string;actorId:string;observedAt:string;
};
export type MethodologyDecisionView = {
  schemaVersion:'paos_methodology_decision_record_v1';taskId:string;taskRevision:number;scopeDigest:string;
  revision:number;status:'unknown'|'current'|'stale'|'unsupported';history:MethodologyDecisionEntry[];
};
