/** Discovery evidence describes a bounded projection, never runtime or database validation. */
export type AnalysisSource={path:string;line:null;basis:'content'|'metadata'};
export type AnalysisEvidence={name:string;confidence:'detected'|'candidate';sources:AnalysisSource[]};
export type ProjectAnalysisView={
 schemaVersion:'paos_project_analysis_v1';projectId:string;sourceRevision:string;rootIdentity:string;
 adapterSourceRevision?:string;runtime?:{pythonVersion:string;coreModule:'product_agent_os.discovery.analyze_workspace';deployment:'checkout_projection'};
 policyVersion:string;inventoryRevision:string;observedAt:string;availability:'available'|'unavailable';stale:boolean;
 stack:AnalysisEvidence[];languages:AnalysisEvidence[];components:AnalysisEvidence[];
 controlPlane:{path:string;status:'present_unverified'|'not_observed';source:AnalysisSource|null}[];
 findings:{code:string;confidence:'candidate';sources:AnalysisSource[]}[];
 schemaCandidates:(AnalysisEvidence&{kind:'schema'|'migration'|'orm'|'database_file';opened:false})[];
 limitations:string[];database:{available:false;reason:'DATABASE_CONNECTION_NOT_CONFIGURED'};
 projection:{files:number;bytes:number;omitted:number;coverage:'partial'};
};
