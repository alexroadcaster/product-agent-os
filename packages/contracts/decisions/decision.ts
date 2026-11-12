export type DecisionKind='clarification'|'product'|'runtime_permission';
export type DecisionState='pending'|'expired'|'stale'|'resolved'|'outcome_unknown';
export type DecisionView={
 id:string;revision:number;projectId:string;sessionId:string|null;taskId:string|null;kind:DecisionKind;source:string;title:string;body:string;
 state:DecisionState;delivery:'not_sent'|'intent_persisted'|'response_sent'|'acknowledged'|'not_applicable';response:string|null;answer:string|null;
 createdAt:number;updatedAt:number;expiresAt:number|null;actions:string[];reviewable:boolean;
 scope:{taskRevision:number|null;files:{path:string;operation:string|null}[];summary:string;coverage:string};
 diff:{status:'unavailable'|'proposed'|'observed';text:string;reason:string};
 evidence:{coverage:string;items:{id:string;kind:string;status:string;summary:string}[]};
 runtime:{route:string;bindingId:string;runId:string;generation:string;requestId:string|number;operationState:string|null}|null;
 history:{at:number;event:string;actor:string;detail:string}[];
};
export type DecisionsPage={items:DecisionView[];hasMore:boolean;offset:number;total:number;coverage:{runtime:string;legacyNotes:string};
 autonomy:{policyRevision:number;paused:boolean;usedRuns:number;maxRuns:number|null;enforcement:string;hostToolsConstrained:false};
 executions:{id:string;taskId:string;sessionId:string;state:string;reason:string|null;checkpoint:string|null}[];
 runs:{id:string;sessionId:string;taskId:string|null;state:string;reason:string|null}[];
 queue:{paused:boolean;items:{id:string;taskId:string;state:string;waitReasons:string[]}[]}|null};
export type DecisionResponse={decision:DecisionView;runtimeReceipt?:Record<string,unknown>};
