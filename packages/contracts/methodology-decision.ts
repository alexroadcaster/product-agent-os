/** TypeScript reader for Python's paos_methodology_decision_v1 read-only wire contract. */

export type MethodologyScope = {
  project_id: string;
  task_id: string;
  source_revision: string;
  task_revision: string;
};

const methods = ['spec_driven', 'design_driven', 'tdd', 'add', 'fsd'] as const;
const stepKinds = [
  'run_regression', 'check_source', 'run_characterization', 'check_configuration',
  'review_evaluation', 'clarify', 'review_scope',
] as const;
type Depth = 'compact' | 'full';
type Evidence = {id: string; kind: 'file' | 'task' | 'workspace'; path: string | null; revision: string};
type Criterion = {
  id: string; criterion: string; scenario: string; owner: string; trace: 'proposed' | 'gap';
  check: 'plan.next_step' | null; evidence_refs: string[];
};
type MethodologyRow = {
  method: typeof methods[number]; owner: string; applicability: 'applicable' | 'needs_context' | 'not_applicable';
  depth: Depth | 'none'; reason: string; next_action: string; evidence_refs: string[];
};

export type MethodologyDecision = {
  schema_version: 'paos_methodology_decision_v1';
  scope: MethodologyScope;
  facts: {
    lifecycle: 'greenfield_candidate' | 'legacy_candidate' | 'existing_code_observed';
    surface: 'frontend' | 'backend' | 'native' | 'mixed' | 'docs' | 'unknown';
    scale: 'small' | 'medium';
    coupling: 'cross_surface' | 'multiple_frontend_areas' | 'local_scope' | 'unknown';
    risk: 'low' | 'medium' | 'high' | 'unknown';
    change_mode: string; ui_scope: boolean; stack: string[]; check_count: number; test_paths: string[];
    environment: 'not_observed' | 'caller_reported';
    provenance: {lifecycle_scale_stack: string; surface_coupling: string; intent_acceptance_risk: string; checks: string};
  };
  evidence: Evidence[];
  decisions: MethodologyRow[];
  requirements: {owner: 'requirements-author'; depth: Depth; changed_paths: string[]; invariants: string[]; non_goals: string[]; criteria: Criterion[]};
  plan: {
    next_step: {kind: typeof stepKinds[number]; action: string; target: string | null; evidence_refs: string[]};
    assumptions: string[]; gaps: string[]; blocking_question: string | null;
  };
  execution: 'not_started';
  acceptance: 'not_evaluated';
  authority: 'read_only';
};

const scopeKeys = ['project_id', 'task_id', 'source_revision', 'task_revision'] as const;
const digest = (value: unknown): value is string => typeof value === 'string' && value.length === 64 && /^[0-9a-f]{64}$/.test(value);
const text = (value: unknown): value is string => typeof value === 'string' && !!value.trim() && !value.includes('\0');
const strings = (value: unknown): value is string[] => Array.isArray(value) && value.every(text);
const path = (value: unknown): value is string => (
  text(value) && !/[\x00-\x1f:\\]/.test(value) && value.split('/').every(part => part !== '' && part !== '.' && part !== '..')
);
const oneOf = (value: unknown, choices: readonly string[]) => typeof value === 'string' && choices.includes(value);
const depth = ['compact', 'full'] as const;

function exact(value: unknown, fields: readonly string[]): value is Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return false;
  const keys = Object.keys(value);
  return keys.length === fields.length && fields.every(key => Object.hasOwn(value, key));
}

function evidenceIds(value: unknown, scope: MethodologyScope): Set<string> {
  if (!Array.isArray(value)) return new Set();
  const ids = new Set<string>();
  for (const row of value) {
    if (!exact(row, ['id', 'kind', 'path', 'revision']) || !text(row.id) || !digest(row.revision) || ids.has(row.id)) {
      return new Set();
    }
    if (row.kind === 'file') {
      if (!path(row.path) || row.id !== `file:${row.path}`) return new Set();
    } else {
      const revision = row.kind === 'task' ? scope.task_revision : row.kind === 'workspace' ? scope.source_revision : null;
      if (row.id !== row.kind || row.path !== null || row.revision !== revision) return new Set();
    }
    ids.add(row.id);
  }
  return ids;
}

function facts(value: unknown): boolean {
  return exact(value, ['lifecycle', 'surface', 'scale', 'coupling', 'risk', 'change_mode', 'ui_scope',
    'stack', 'check_count', 'test_paths', 'environment', 'provenance'])
    && oneOf(value.lifecycle, ['greenfield_candidate', 'legacy_candidate', 'existing_code_observed'])
    && oneOf(value.surface, ['frontend', 'backend', 'native', 'mixed', 'docs', 'unknown'])
    && oneOf(value.scale, ['small', 'medium'])
    && oneOf(value.coupling, ['cross_surface', 'multiple_frontend_areas', 'local_scope', 'unknown'])
    && oneOf(value.risk, ['low', 'medium', 'high', 'unknown'])
    && text(value.change_mode) && typeof value.ui_scope === 'boolean' && strings(value.stack)
    && typeof value.check_count === 'number' && Number.isSafeInteger(value.check_count) && value.check_count >= 0
    && Array.isArray(value.test_paths) && value.test_paths.every(path)
    && oneOf(value.environment, ['not_observed', 'caller_reported'])
    && exact(value.provenance, ['lifecycle_scale_stack', 'surface_coupling', 'intent_acceptance_risk', 'checks'])
    && Object.values(value.provenance).every(text);
}

/** Read advice for an independently selected project, task and revision. No fallback for unknown versions. */
export function decodeMethodologyDecision(input: unknown, expected: MethodologyScope): MethodologyDecision {
  if (!exact(input, ['schema_version', 'scope', 'facts', 'evidence', 'decisions', 'requirements', 'plan', 'execution', 'acceptance', 'authority'])
    || input.schema_version !== 'paos_methodology_decision_v1') throw new Error('methodology_decision:unsupported_version_or_shape');
  const scope = input.scope;
  if (!exact(scope, scopeKeys) || !text(scope.task_id) || !digest(scope.project_id) || !digest(scope.source_revision)
    || !digest(scope.task_revision) || scopeKeys.some(key => scope[key] !== expected[key])) {
    throw new Error('methodology_decision:scope_mismatch');
  }
  const ids = evidenceIds(input.evidence, expected);
  if (!ids.has('task') || !ids.has('workspace')) throw new Error('methodology_decision:invalid_evidence');
  const refs = (value: unknown) => strings(value) && value.length > 0
    && new Set(value).size === value.length && value.every(id => ids.has(id));
  const rows = input.decisions;
  const requirements = input.requirements;
  const plan = input.plan;
  if (!facts(input.facts) || !Array.isArray(rows) || rows.length !== methods.length
    || !rows.every((row, index) => exact(row, ['method', 'owner', 'applicability', 'depth', 'reason', 'next_action', 'evidence_refs'])
      && row.method === methods[index] && text(row.owner) && text(row.reason) && text(row.next_action)
      && oneOf(row.applicability, ['applicable', 'needs_context', 'not_applicable'])
      && oneOf(row.depth, [...depth, 'none']) && refs(row.evidence_refs))
    || !exact(requirements, ['owner', 'depth', 'changed_paths', 'invariants', 'non_goals', 'criteria'])
    || requirements.owner !== 'requirements-author' || !oneOf(requirements.depth, depth)
    || !Array.isArray(requirements.changed_paths) || !requirements.changed_paths.every(path)
    || !strings(requirements.invariants) || !strings(requirements.non_goals)
    || !Array.isArray(requirements.criteria) || !requirements.criteria.length
    || !requirements.criteria.every((row, index) => exact(row, ['id', 'criterion', 'scenario', 'owner', 'trace', 'check', 'evidence_refs'])
      && row.id === `AC-${index + 1}` && text(row.criterion) && text(row.scenario) && text(row.owner)
      && oneOf(row.trace, ['proposed', 'gap']) && refs(row.evidence_refs)
      && row.check === (row.trace === 'proposed' ? 'plan.next_step' : null))
    || !exact(plan, ['next_step', 'assumptions', 'gaps', 'blocking_question'])
    || !strings(plan.assumptions) || !strings(plan.gaps) || (plan.gaps.length ? !text(plan.blocking_question) : plan.blocking_question !== null)
    || !exact(plan.next_step, ['kind', 'action', 'target', 'evidence_refs']) || !oneOf(plan.next_step.kind, stepKinds)
    || !text(plan.next_step.action) || !refs(plan.next_step.evidence_refs)
    || (oneOf(plan.next_step.kind, ['clarify', 'review_scope']) ? plan.next_step.target !== null : !text(plan.next_step.target))
    || input.execution !== 'not_started' || input.acceptance !== 'not_evaluated' || input.authority !== 'read_only') {
    throw new Error('methodology_decision:invalid_projection');
  }
  const next = plan.next_step;
  if (oneOf(next.kind, ['check_source', 'check_configuration', 'review_evaluation'])
    && !(next.evidence_refs as string[]).includes(`file:${next.target}`)) throw new Error('methodology_decision:invalid_projection');
  if (oneOf(next.kind, ['run_regression', 'run_characterization'])
    && !(next.evidence_refs as string[]).some(ref => ref.startsWith('file:'))) throw new Error('methodology_decision:invalid_projection');
  return input as unknown as MethodologyDecision;
}
