/** Static source-backed dependencies; no runtime call graph, query execution or row data. */
export type CodeDatabaseOperation='read'|'write'|'schema'|'unknown';
export type CodeDatabaseConfidence='confirmed'|'inferred'|'unresolved';
export type CodeDatabaseLink={id:string;relativePath:string;span:{start:{line:number;column:number};end:{line:number;column:number}};query:string|null;model:string|null;table:string;sourcePath:string|null;operation:CodeDatabaseOperation;method:'literal_sql'|'prisma_static';confidence:CodeDatabaseConfidence;reason:string;codeRevision:string;schemaRevision:string};
export type CodeDatabaseStatus={schemaVersion:'paos_code_database_v1';projectId:string;state:'unavailable'|'fresh'|'stale'|'partial';codeRevision:string|null;schemaRevision:string|null;revision:string|null;sourcePath:string|null;counts:{links:number;confirmed:number;inferred:number;unresolved:number};reasons:string[]};
export type CodeDatabasePage=CodeDatabaseStatus&{links:CodeDatabaseLink[];testCandidates:Array<{relativePath:string;reason:string}>;nextCursor:string|null;total:number;contextBytes:number;truncated:boolean};
