import type { M1TaskProfile } from '../tasks/m1-task-profile.ts';
import type { TaskProfile } from '../issues/task-profile.ts';

export type EntityKind = 'task' | 'session' | 'message' | 'draft' | 'comment' | 'settings' | 'document' | 'run' | 'approval' | 'evidence';
export type Coverage = 'complete' | 'partial' | 'unavailable';
export type Project = Readonly<{
  id: string; keyPrefix: string; canonicalRoot: string; rootIdentity: string; displayName?: string;
  authorityMode: 'legacy_files' | 'sql'; authorityEpoch: number;
}>;
export type EntityInput = Readonly<{
  id: string; kind: EntityKind; parentId?: string | null; title?: string; body?: string;
  status?: string; publicKey?: string | null; coverage?: Coverage; data?: Record<string, unknown> | M1TaskProfile;
  blobIds?: readonly string[];
}>;
export type StoredEntity = Readonly<{
  projectId: string; id: string; kind: EntityKind; parentId: string | null;
  title: string; body: string; status: string; publicKey: string | null; coverage: Coverage;
  data: Record<string, unknown>; revision: number; deleted: boolean; updatedAt: string;
  blobIds: readonly string[];
  /** Local database-generation insertion ordinal for message paging; never an entity ID or replay cursor. */
  journalOrder?: number;
}>;
export type StoreWrite = Readonly<{
  projectId: string; actorId: string; idempotencyKey: string; expectedAuthorityEpoch: number;
  /** Check the project runtime fence in the same transaction as a scope/acceptance mutation. */
  requireIdle?: true;
  /** Trusted Task Manager transition metadata; browser generic commands cannot supply it. */
  taskManagerAction?: 'transition' | 'complete';
  taskManagerReason?: string;
  taskManagerHotfixReason?: string;
  taskManagerReviewReason?: string;
  /** Bound runtime tool context; never accepted from generic browser commands. */
  taskManagerRun?: {id:string;bindingId:string;generation:string;taskId:string};
  changes: readonly { entity: EntityInput; expectedRevision: number; delete?: boolean }[];
  outbox?: readonly { kind: string; payload: Record<string, unknown> }[];
}>;
export type StoreReceipt = Readonly<{
  commandId: string; projectId: string; seq: number; revisions: readonly { id: string; revision: number }[];
  /** Original pre-cutover backup, atomically retained for lost-ACK retries. Legacy receipts may omit it. */
  cutoverBackupId?: string;
}>;
export type StoreEventPage = Readonly<{
  generation: string;
  items: readonly { seq: number; eventId: string; actorId: string; occurredAt: string; payload: unknown }[];
  hasMore: boolean;
}>;
export type ListOptions = Readonly<{ kind?: EntityKind; parentId?: string; limit?: number; offset?: number; order?: 'newest' }>;
export type PromoteLegacy = Readonly<{
  projectId: string; actorId: string; expectedAuthorityEpoch: number; sourceDigest: string;
  verifiedSourceDigest: string; writerInventoryVerified: boolean; restoreRehearsalVerified: boolean;
  items: readonly TaskProfile[]; idempotencyKey: string;
  sourceBindings?: readonly ImportSourceBinding[];
  cutoverBackupId?: string;
}>;
export type ImportSourceBinding = Readonly<{ role: 'records' | 'projection'; sourceName: string; sourceRelativePath: string;
  sourceDigest: string; byteSize: number }>;
export type BlobReceipt = Readonly<{ id: string; projectId: string; sha256: string; byteSize: number }>;
export type BackupManifest = Readonly<{
  schemaVersion: 1|2; migrationChecksum: string; appCompatibility: 'paos-m1-v1'|'paos-m2-v1'; backupId: string;
  createdAt: string; databaseSha256: string; manifestSha256: string;
  blobs: readonly BlobReceipt[];
  exclusions: readonly string[];
}>;
