/** Assigned by the local project registry. The canonical root stays service-side. */
export type ProjectBinding = Readonly<{
  projectId: string;
  workspaceRoot: string;
  directoryIdentity: string;
}>;

export type ProjectSourceId =
  | 'instructions'
  | 'requirements'
  | 'plan'
  | 'test'
  | 'evals'
  | 'runlog'
  | 'runtimeHistory';

export type ProjectSourceCoverage = Readonly<{
  id: ProjectSourceId;
  relativePath?: string;
} & (
  | { status: 'available' }
  | { status: 'unavailable'; reason: 'missing' | 'unreadable' | 'runtime_not_connected' | 'runtime_history_unreadable' }
  | { status: 'excluded'; reason: 'linked_file' | 'unsupported_file' }
  | { status: 'partial'; reason: 'persisted_threads_only' | 'runtime_scope_mismatch'; visibleThreadCount: number; hasMore: boolean }
)>;

/** The local App Server transport implements only the scoped thread/list method at this boundary. */
export type ListRuntimeThreads = (request: Readonly<{
  cwd: string;
  sourceKinds: readonly ('cli' | 'vscode' | 'appServer')[];
  modelProviders: readonly string[];
  limit: number;
}>) => Promise<unknown>;

export type ProjectSources = Readonly<{
  projectId: string;
  sources: readonly ProjectSourceCoverage[];
}>;
