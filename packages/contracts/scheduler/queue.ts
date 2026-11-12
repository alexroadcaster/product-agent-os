import type {RecipeStepView} from '../execution-recipes/recipe.ts';
export type QueueState='queued'|'paused'|'running'|'completed'|'failed'|'cancelled'|'recovery_required'|'needs_review';
export type OwnershipClaim={path:string;mode:'read'|'write'};
export type QueueEntryView={id:string;taskId:string;taskKey:string;taskTitle:string;revision:number;state:QueueState;position:number|null;workflow:{id:string;version:number};recipeId:string;sessionId:string;steps:RecipeStepView[];claims:OwnershipClaim[];ownershipScope:'entire_workspace';executionId:string|null;executionState:string|null;waitReasons:string[];createdAt:number;updatedAt:number};
export type QueueSnapshot={revision:number;paused:boolean;order:string[];items:QueueEntryView[];capabilities:{maxWritersPerWorkspace:1;maxConcurrentWorkspaces:4;parallelism:'disjoint_canonical_workspaces';hostToolsConstrained:false}};
export type QueuePreview={mode:'recipe';previewDigest:string;queueRevision:number;target:string;recipeId:string;workflow:{id:string;version:number};steps:RecipeStepView[];claims:OwnershipClaim[];waitReasons:string[];maxAttempts:number;policy:{remainingRuns:number;concurrency:1};ownershipScope:'entire_workspace'};
