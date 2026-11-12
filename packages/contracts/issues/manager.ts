import type { IssueLink } from './task-profile.ts';
import type {WorkflowRegistry} from '../workflows/workflow.ts';
export type CatalogItem={id:string;name:string;status:'active'|'archived'};
export type VersionItem={id:string;name:string;description?:string;status:'unreleased'|'released'|'archived';startDate?:string|null;releaseDate?:string|null};
export type Board={columns:{id:string;statuses:string[];wipLimit?:number;wipMode?:'soft'|'hard'}[];outOfBoard:boolean;
  releaseRequiredTypes?:string[];releaseRequiredComponents?:string[];attachmentFileBytes:number;attachmentTaskBytes:number;timezone?:string;view?:Record<string,unknown>};
export type ManagerSnapshot<T>={tasks:T[];components:CatalogItem[];versions:VersionItem[];board:Board;links:IssueLink[];workflows:WorkflowRegistry;
  comments:T[];attachments:T[];settingsRevisions:Record<string,number>;quota:{fileBytes:number;taskBytes:number};coverage:'complete'};
