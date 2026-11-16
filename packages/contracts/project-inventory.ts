/** Metadata eligibility is not proof of a successful read or a completed analyzer. */
export type InventoryProject = { id: string; canonicalRoot: string; rootIdentity: string };
export type InventoryPolicy = { version?: string; include?: string[]; exclude?: string[]; respectGitignore?: boolean };
export type InventoryLimits = { pageSize: number; directoryEntries: number; entries: number; files: number; depth: number; milliseconds: number; fileBytes: number; responseBytes: number };
export type InventoryAccess = { readable: boolean; indexable: boolean; reason?: string };
export type InventoryEntry = {
  relativePath: string; name: string; kind: 'file' | 'directory' | 'link' | 'other';
  byteSize: number; modifiedAt: string; revision: string; access: InventoryAccess;
};
export type InventoryCounts = { discovered: number; files: number; directories: number; readEligible: number; indexEligible: number; readable: number | null; indexed: number | null; unsupported: number; excluded: number; error: number };
export type InventoryMeta = {
  schemaVersion: 'paos_project_inventory_v1'; projectId: string; rootIdentity: string;
  policyVersion: string; ignoreRevision: string; revision: string; observedAt: string; coverage: 'complete' | 'partial'; reasons: string[];
};
export type InventorySnapshot = InventoryMeta & { entries: InventoryEntry[]; counts: InventoryCounts };
export type InventoryDirectory = InventorySnapshot & { path: string; searchScope: 'directory'; nextCursor: string | null; total: number; limit: number };
export type InventoryRead = InventoryMeta & { relativePath: string; text: string; hash: string; byteSize: number; modifiedAt: string; fileRevision: string; redacted: boolean };
