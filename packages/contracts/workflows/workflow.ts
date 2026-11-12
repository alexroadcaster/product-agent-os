export const WORKFLOW_CATEGORIES=['backlog','ready','in_progress','review','verification','awaiting_acceptance','done','cancelled'] as const;
export type WorkflowCategory=typeof WORKFLOW_CATEGORIES[number];
export type WorkflowState={id:string;name:string;category:WorkflowCategory;initial?:boolean};
export type WorkflowTransition={id:string;name:string;from:string;to:string;actors:('user'|'agent')[];requiredFields:string[];guards:string[];recipeId?:string;successTarget?:string;failureTarget?:string;requiresDecision?:boolean};
/** Recipes are bounded, non-executable proposals. Host permissions never come from this metadata. */
export type WorkflowRecipe={id:string;name:string;steps:{id:string;role:string;skills:string[];profileVersion:string;skillVersions:Record<string,string>;inputArtifacts:string[];outputArtifacts:string[];checks:string[];ownership:string[];timeoutSeconds:number;retryBudget:number;iterationBudget:number;next?:string[];join?:string[]}[]};
export type WorkflowDefinition={name:string;states:WorkflowState[];transitions:WorkflowTransition[];recipes:WorkflowRecipe[]};
export type WorkflowVersion={version:number;definition:WorkflowDefinition;definitionHash:string;publishedAt:string|null};
export type WorkflowRecord={id:string;archived:boolean;activeVersion:number|null;draft:WorkflowDefinition|null;versions:WorkflowVersion[]};
export type WorkflowRegistry={category:'workflow_registry';defaultWorkflowId:string;typeMapping:Record<string,string>;workflows:WorkflowRecord[]};
export type WorkflowSnapshot={ref:{id:string;version:number};definition:WorkflowDefinition;definitionHash:string};
