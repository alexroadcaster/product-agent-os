/** Cheap profile observation. Filesystem changes require the explicit bounded refresh route. */
export type ProjectFreshness={schemaVersion:'paos_project_freshness_v1';projectId:string;generation:string;throughSeq:number;scanVersion:number;policyVersion:number;rootIdentity:string};
/** Shared scope for Files, documents, graph/analysis and future schema/code-table consumers. */
export type SourceProvenance={projectId:string;rootIdentity:string;policyVersion:string;inventoryRevision:string};
export function sameSourceRevision(saved:SourceProvenance,current:SourceProvenance):boolean{
 return saved.projectId===current.projectId&&saved.rootIdentity===current.rootIdentity&&saved.policyVersion===current.policyVersion&&saved.inventoryRevision===current.inventoryRevision;
}
export function sameProjectFreshness(saved:ProjectFreshness,current:ProjectFreshness):boolean{
 return saved.schemaVersion===current.schemaVersion&&saved.projectId===current.projectId&&saved.generation===current.generation&&saved.throughSeq===current.throughSeq&&saved.scanVersion===current.scanVersion&&saved.policyVersion===current.policyVersion&&saved.rootIdentity===current.rootIdentity;
}
