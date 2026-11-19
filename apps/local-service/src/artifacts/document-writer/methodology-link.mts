import type {DocumentMethodologyLink} from '../../../../../packages/contracts/artifacts/document-apply.ts';
import type {StoredEntity} from '../../storage/local-store.mts';

function fail(code:string):never { throw Object.assign(new Error(code), {code}); }

export function decodeDocumentMethodologyLink(value:unknown):DocumentMethodologyLink {
  if (!value || typeof value!=='object' || Array.isArray(value)) fail('DOCUMENT_METHODOLOGY_INVALID');
  const raw=value as Record<string,unknown>;
  const {taskId,taskRevision,criterionIds}=raw;
  if (Object.keys(raw).some(key=>!['taskId','taskRevision','criterionIds'].includes(key))
      || typeof taskId!=='string' || !/^[a-z0-9_-]{1,128}$/i.test(taskId)
      || typeof taskRevision!=='number' || !Number.isSafeInteger(taskRevision) || taskRevision<1
      || !Array.isArray(criterionIds) || !criterionIds.length || criterionIds.length>100
      || criterionIds.some(id=>typeof id!=='string'||!/^AC-[1-9][0-9]{0,3}$/.test(id))
      || new Set(criterionIds).size!==criterionIds.length) fail('DOCUMENT_METHODOLOGY_INVALID');
  return {taskId,taskRevision,criterionIds:[...criterionIds]};
}

export function assertDocumentMethodologyTask(link:DocumentMethodologyLink, task:StoredEntity|null):void {
  if (!task || task.kind!=='task' || task.deleted || task.id!==link.taskId || task.revision!==link.taskRevision)
    fail('DOCUMENT_METHODOLOGY_TASK_STALE');
  const criteria=task.data.acceptanceCriteria;
  if (!Array.isArray(criteria) || link.criterionIds.some(id=>typeof criteria[Number(id.slice(3))-1]!=='string'))
    fail('DOCUMENT_METHODOLOGY_INVALID');
}
