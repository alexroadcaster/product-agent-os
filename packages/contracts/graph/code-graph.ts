/** Derived lexical graph. Offsets are UTF-16 code units in the hash-pinned UTF-8 source. */
export type GraphAnchor={fileId:string;start:number;end:number;line:number;column:number};
export type GraphEdgeType='import'|'call'|'define'|'read'|'write'|'reference';
export type GraphNode={id:string;kind:'file'|'symbol'|'unresolved';name:string;relativePath:string;fileId:string;language:string;scope:string;namespace:'value'|'module'|'dynamic';anchor?:GraphAnchor;reason?:string};
export type GraphEdge={id:string;type:GraphEdgeType;from:string;to:string;anchor:GraphAnchor;resolution:'lexical'|'unresolved'|'dynamic'};
export type GraphCoverage={relativePath:string;status:'indexed'|'unsupported'|'parse_error'|'excluded';reason?:string};
export type GraphStatus={state:'unavailable'|'fresh'|'stale';revision?:string;coverage?:GraphCoverage[];counts?:{files:number;nodes:number;edges:number};limitations:string[]};
/** Context nodes hydrate off-page endpoints; they never change the primary node cursor. */
export type GraphPage={revision:string;state:'fresh'|'stale';nodes:GraphNode[];contextNodes:GraphNode[];edges:GraphEdge[];nextCursor:string|null;partial:boolean};
export type GraphNodeDetail={revision:string;state:'fresh'|'stale';node:GraphNode};
export type GraphTaskMatch={id:string;title:string;revision:number;matchReason:string;sourceState:'matching'|'stale'|'unknown';expectedSourceRevision:string|null;actualSourceRevision:string;sourceRevision:string;matches:{matchReason:string;sourceState:string;expectedSourceRevision:string|null;actualSourceRevision:string}[]};
export type GraphImpact=GraphNodeDetail&{edges:GraphEdge[];nextCursor:string|null;tasks:GraphTaskMatch[];tasksCoverage:'bounded_first_1000'};
export type GraphSourceExcerpt={revision:string;fileId:string;relativePath:string;start:number;end:number;sha256:string;content:string;redacted:boolean};
