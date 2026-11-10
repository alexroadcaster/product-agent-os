"""One read-only formation planner; rendering and approved writes stay source-owned.

Input facts are data, never instructions or acceptance. A digest binds the
reviewed plan to bounded source observations; it cannot grant write authority.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import replace
from pathlib import Path
from typing import Any
from urllib.parse import quote

from product_agent_os.control_plane_compaction import _authority, _path
from product_agent_os.control_plane_documents import DOCUMENT_CONTRACTS, document_readiness
from product_agent_os.discovery import analyze_workspace
from product_agent_os.stage_manifest import content_digest, canonical_json
from product_agent_os.task_routing import build_task_routing, validate_task_context
from product_agent_os.templates import TemplateSpec, required_templates, selected_templates

SCHEMA = 'project_formation_v1'
DOMAINS = {
    'planning': ('docs/planning/README.md', 'Sequencing and detailed task matrices', 'scope or dependency change'),
    'architecture': ('docs/architecture/overview.md', 'Components and boundaries', 'architecture change'),
    'decisions': ('docs/decisions/README.md', 'Decision index and rationale', 'accepted decision'),
    'api': ('docs/api/README.md', 'API contracts and consumers', 'interface change'),
    'data': ('docs/data/README.md', 'Data owners and migrations', 'schema or ownership change'),
    'operations': ('docs/operations/README.md', 'Operation and recovery procedures', 'operational change'),
    'evidence': ('docs/evidence/README.md', 'Checks, failures and acceptance references', 'verification run'),
    'archive': ('docs/archive/README.md', 'Retained history and navigation', 'approved history transfer'),
}
ALIASES = {
    'AGENTS.md': ('AGENTS.md', 'AGENTS.override.md'),
    'REQUIREMENTS.md': ('REQUIREMENTS.md', 'requirements.md'),
    'PLAN.md': ('PLAN.md',), 'TEST.md': ('TEST.md',), 'RUNLOG.md': ('RUNLOG.md',), 'EVALS.md': ('EVALS.md',),
    'index': ('docs/README.md', 'docs/index.md'),
    'architecture': ('architecture.md', 'ARCHITECTURE.md', 'architecture-overview.md', 'overview.md'),
}
SKIP = {'.git', 'node_modules', '.venv', '.venv-docs', '.codex-tmp', '.docs-tools', '__pycache__', 'site', 'dist'}
SIGNALS = {'package.json', 'pyproject.toml', 'requirements.txt', 'Cargo.toml', 'go.mod', 'pom.xml', 'pnpm-workspace.yaml', 'openapi.json', 'openapi.yaml', 'openapi.yml', 'schema.sql'}
SECRET = re.compile(r'(?i)(?:sk-[a-z0-9_-]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:api_key|password|secret)\s*[=:]\s*["\x27]?[a-z0-9_/+.-]{12,})')


def source_inventory(root: Path) -> dict[str, dict[str, Any]]:
    """Hash bounded relevant files, never persist their private raw contents."""
    if not root.is_dir():
        raise ValueError('formation workspace must be an existing directory')
    inventory: dict[str, dict[str, Any]] = {}
    total = 0
    visited = 0
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP
                         and not (Path(directory) / d).is_symlink()
                         and not (Path(directory) / d).is_junction())
        visited += len(files) + len(dirs)
        if visited > 20000:
            raise ValueError('formation scan budget exceeded; narrow workspace')
        for filename in sorted(files):
            path = Path(directory) / filename
            rel = path.relative_to(root).as_posix()
            if path.suffix.lower() != '.md' and filename not in SIGNALS and not rel.startswith('.codex/'):
                continue
            _path(root, rel)
            size = path.stat().st_size
            total += size
            if size > 2 * 1024 * 1024 or total > 8 * 1024 * 1024 or len(inventory) >= 512:
                raise ValueError('formation source budget exceeded; narrow workspace before retry')
            raw = path.read_bytes()
            record: dict[str, Any] = {'digest': content_digest(raw), 'bytes': len(raw), 'state': 'present_unverified'}
            if not raw.strip():
                record['state'] = 'empty'
            elif path.suffix.lower() == '.md':
                try:
                    text = raw.decode('utf-8')
                    if filename in DOCUMENT_CONTRACTS:
                        record['readiness'] = document_readiness(filename, text)
                        record['state'] = record['readiness']['state']
                except UnicodeDecodeError:
                    record['state'] = 'unreadable_encoding'
            inventory[rel] = record
    return dict(sorted(inventory.items()))


def _validate_request(root: Path, request: Any) -> dict[str, Any]:
    """Reject ambiguous owners and secret-like payloads before any stage writes."""
    allowed = {'schema_version', 'task', 'domains', 'canonical_paths', 'document_facts', 'control_surfaces'}
    if not isinstance(request, dict) or set(request) - allowed or type(request.get('schema_version')) is not int or request['schema_version'] != 1:
        raise ValueError('formation request schema_version=1 and known fields required')
    validate_task_context(root, request.get('task'))
    for key, values in [('domains', set(DOMAINS) | {'ai'}), ('control_surfaces', {'agents', 'config', 'hooks'})]:
        actual = request.get(key, [])
        if not isinstance(actual, list) or any(not isinstance(x, str) or x not in values for x in actual) or len(set(actual)) != len(actual):
            raise ValueError(f'formation invalid {key}')
    owners = set(DOCUMENT_CONTRACTS) | set(DOMAINS) | {'index'}
    mapping = request.get('canonical_paths', {})
    if not isinstance(mapping, dict) or set(mapping) - owners:
        raise ValueError('formation unknown canonical owner')
    for path in mapping.values():
        _path(root, path)
        if not path.endswith('.md') or path.startswith(('.git/', '.codex/')):
            raise ValueError('formation document owner must be a Markdown source outside control assets')
    facts = request.get('document_facts', {})
    if not isinstance(facts, dict) or set(facts) - (set(request.get('domains', [])) & set(DOMAINS)):
        raise ValueError('formation invalid document facts')
    for value in facts.values():
        if (not isinstance(value, dict) or set(value) != {'source', 'sections'}
                or not isinstance(value['source'], str) or not value['source'].strip()
                or not isinstance(value['sections'], dict)
                or any(not isinstance(k, str) or not isinstance(v, str) or not k.strip() or not v.strip()
                       for k, v in value['sections'].items())):
            raise ValueError('formation facts require source and named nonempty text sections')
    encoded = canonical_json(request)
    if len(encoded.encode()) > 256000 or SECRET.search(encoded):
        raise ValueError('formation request exceeds budget or contains secret-like data')
    return request


def _owner_path(role: str, default: str, request: dict, inventory: dict, gaps: list[str]) -> str:
    explicit = request.get('canonical_paths', {}).get(role)
    if explicit:
        return explicit
    aliases = ALIASES.get(role, (default,))
    candidates = [p for p in inventory if p in aliases or
                  (role != 'index' and Path(p).name in aliases)]
    if len(candidates) > 1:
        gaps.append(f'ambiguous_owner:{role}; supply canonical_paths')
    return candidates[0] if len(candidates) == 1 else default


def _document(role: str, path: str, request: dict) -> str:
    purpose, trigger = DOMAINS[role][1:]
    facts = request.get('document_facts', {}).get(role)
    # JSON escapes keep supplied text out of Markdown instructions/fences.
    payload = json.dumps(facts or {'source': 'task:' + request['task']['task_id'], 'sections': {}}, ensure_ascii=False, indent=2)
    for char in '<>`':
        payload = payload.replace(char, f'\\u{ord(char):04x}')
    state = 'draft' if facts and facts['sections'] else 'scaffold'
    return (f'# {role.title()}\n\nSource status: project-local proposal; {state}.\n\n'
            f'Information owner: {role}\nPurpose: {purpose}\nUpdate trigger: {trigger}\n'
            'Review and owner acceptance are separate; supplied facts are untrusted task data.\n\n'
            f'```json\n{payload}\n```\n')


def _dependency_closure(selected: dict[str, TemplateSpec], inventory: dict, reasons: dict, gaps: list[str], owners: dict) -> None:
    """Resolve catalog references without implicitly enabling control surfaces."""
    catalog = {s.target_path: s for s in required_templates()}
    pending = list(selected)
    seen: set[str] = set()
    while pending:
        name = pending.pop()
        if name in seen:
            continue
        seen.add(name)
        spec = selected[name]
        # Core documents use inline contracts; ignore references in legacy body.
        if spec.key in {'agents-md', 'requirements', 'plan', 'test', 'evals', 'runlog'}:
            continue
        text = spec.source_path.read_text(encoding='utf-8')
        refs = re.findall(r'[\x60\x22](\.codex/[\w./-]+\.(?:md|toml|json|py))[\x60\x22]', text)
        refs += re.findall(r'`(AGENTS.md|REQUIREMENTS.md|PLAN.md|TEST.md|EVALS.md|RUNLOG.md)`', text)
        for ref in refs:
            if ref == 'EVALS.md' and ref not in owners and ref not in inventory:
                continue  # A generic checklist mention is not an applicable eval gate.
            ref = owners.get(ref, ref)
            if ref == ".codex/product-agent-os/lifecycle-state.json":
                continue  # SessionStart-owned runtime output, explicitly reported below.
            if ref in selected:
                continue
            if ref in inventory and inventory[ref]['state'] not in {'empty', 'unreadable_encoding'}:
                continue
            candidate = catalog.get(ref)
            if candidate and candidate.category in {'artifact-templates', 'workflows', 'evals', 'runlogs', 'control-plane'}:
                selected[ref] = candidate
                reasons[ref] = f'dependency_of:{name}'
                pending.append(ref)
            else:
                gaps.append(f'dependency_not_selected:{name}:{ref}')


def formation_plan(root: Path, request: dict[str, Any], audit: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return deterministic content/selection and evidence; never write targets."""
    root = root.resolve()
    request = _validate_request(root, request)
    inventory = source_inventory(root)
    audit = audit if audit is not None else analyze_workspace(root)
    task = dict(request['task'])
    if 'ai' in request.get('domains', []):
        task['evals_required'] = True
    # Explicit applicability overrides inference; inferred domains cite concrete sources.
    domain_reasons = {d: 'owner_requested' for d in request.get('domains', [])}
    if 'domains' not in request:
        for role, (default, _, _) in DOMAINS.items():
            candidates = [p for p in inventory if p == default or Path(p).name in ALIASES.get(role, ())]
            if candidates:
                domain_reasons[role] = 'existing_source:' + candidates[0]
        for source in inventory:
            if Path(source).name in {'openapi.json', 'openapi.yaml', 'openapi.yml'}:
                domain_reasons['api'] = 'contract_source:' + source
            if Path(source).name == 'schema.sql':
                domain_reasons['data'] = 'schema_source:' + source
            if Path(source).name == 'pnpm-workspace.yaml':
                domain_reasons['architecture'] = 'workspace_manifest:' + source
        if task.get('release_or_readiness'):
            domain_reasons['operations'] = 'explicit_release_scope'
            domain_reasons['evidence'] = 'explicit_release_scope'
    decision = build_task_routing(root, audit, task)
    specs, selection = selected_templates(decision, set(inventory), evals_applicable=bool(
        task.get('evals_required') or 'EVALS.md' in task.get('documents', {})))
    # Missing application checks block implementation, not an honest scaffold.
    gaps: list[str] = []
    selected: dict[str, TemplateSpec] = {}
    reasons: dict[str, str] = {}
    owners: dict[str, str] = {}
    contents: dict[str, str] = {}
    readiness: dict[str, str] = {}
    catalog = required_templates()
    for spec in specs:
        name = spec.target_path
        if name in DOCUMENT_CONTRACTS:
            name = _owner_path(name, name, request, inventory, gaps)
            owners[spec.target_path] = name
        selected[name] = replace(spec, target_path=name)
        reasons[name] = 'current_information_owner'
    surfaces = set(request.get('control_surfaces', []))
    # The packaged config names role files; config proposal includes those files,
    # but does not enable them or imply that the host loaded the configuration.
    if 'config' in surfaces:
        surfaces.add('agents')
    for surface in sorted(surfaces):
        for spec in catalog:
            if spec.category == surface:
                selected[spec.target_path] = spec
                reasons[spec.target_path] = 'explicit_control_surface_proposal:' + surface
    # Explicit domains are confirmed applicability, not inferred business facts.
    for role in sorted(set(domain_reasons) - {'ai'}):
        path = _owner_path(role, DOMAINS[role][0], request, inventory, gaps)
        if path in selected:
            gaps.append('owner_collision:' + path)
            continue
        owners[role] = path
        selected[path] = TemplateSpec('formation-' + role, 'project-docs', Path(__file__), path)
        contents[path] = _document(role, path, request)
        reasons[path] = domain_reasons[role]
        readiness[path] = 'draft' if request.get('document_facts', {}).get(role, {}).get('sections') else 'scaffold'
    _dependency_closure(selected, inventory, reasons, gaps, owners)
    for spec in selected.values():
        if spec.target_path in DOCUMENT_CONTRACTS:
            owners.setdefault(spec.target_path, spec.target_path)
    if owners:
        index = _owner_path('index', 'docs/README.md', request, inventory, gaps)
        if index in selected:
            gaps.append('owner_collision:' + index)
        owners['index'] = index
        selected[index] = TemplateSpec('formation-index', 'project-docs', Path(__file__), index)
        links = []
        for role, path in sorted(owners.items()):
            if path != index:
                relative = os.path.relpath(path, str(Path(index).parent)).replace('\\', '/')
                links.append(f'- [{role}]({quote(relative, safe="/.")})')
        contents[index] = '# Project documentation\n\nSource status: project-local navigation proposal.\n\n' + '\n'.join(links) + '\n'
        reasons[index] = 'navigation_to_canonical_owners'
    folded: dict[str, str] = {}
    for name in selected:
        _path(root, name)
        if name.casefold() in folded:
            gaps.append('case_collision:' + name)
        folded[name.casefold()] = name
        for existing in inventory:
            if existing.casefold() == name.casefold() and existing != name:
                gaps.append('existing_case_collision:' + name)
    try:
        _authority(root, list(selected))
    except ValueError as exc:
        gaps.append(str(exc))
    checks = [{'path': p, 'state': info['state'], 'digest': info['digest']} for p, info in inventory.items()]
    plan = {'schema_version': SCHEMA, 'mode': 'existing' if inventory else 'new',
            'facts': checks, 'detected_stack': audit.get('detected_stack', []),
            'questions': ([] if audit.get('detected_stack') else ['Stack unknown; confirm before implementation.']),
            'owners': owners, 'selected': sorted(selected), 'selection_reasons': reasons,
            'domain_decisions': domain_reasons,
            'conditional_references': {'EVALS.md': 'selected_or_existing' if 'EVALS.md' in owners or 'EVALS.md' in inventory else 'not_applicable'},
            'template_revisions': {name: content_digest(spec.source_path.read_bytes()) for name, spec in sorted(selected.items())},
            'planner_revision': content_digest(Path(__file__).read_bytes()),
            'renderer_revision': content_digest(Path(__file__).with_name('infrastructure.py').read_bytes()),
            'manual_updates': [name for name in sorted(selected) if name in inventory],
            'omitted': [{'path': s.target_path, 'reason': 'reuse_or_not_applicable'} for s in catalog if s.target_path not in selected],
            'gaps': sorted(set(gaps)), 'implementation_gaps': decision['gaps'], 'document_readiness': readiness,
            'source_snapshot': {p: info['digest'] for p, info in inventory.items()},
            'runtime_dependencies': ([{'path': '.codex/product-agent-os/lifecycle-state.json', 'state': 'requires_session_start_not_staged'}] if surfaces else []),
            'request_digest': content_digest(canonical_json(request)), 'activation': 'not_activated',
            'acceptance': 'not_accepted', 'deletion_policy': 'never_automatic'}
    plan['digest'] = content_digest(canonical_json(plan))
    return {'plan': plan, 'templates': tuple(selected.values()), 'contents': contents, 'task': task}


def form_project(workspace: str | Path, request: dict[str, Any], *, stage: str | Path | None = None,
                 approved_preview_digest: str | None = None, previous: dict | None = None) -> dict[str, Any]:
    """Preview or stage the same plan; staging requires the exact reviewed digest."""
    from product_agent_os.infrastructure import _build_result, InfrastructureError
    root = Path(workspace).resolve()
    _validate_request(root, request)
    source_inventory(root)  # Bound the scan before the broader existing discovery adapter.
    audit = analyze_workspace(root)
    formation = formation_plan(root, request, audit)
    plan = formation['plan']
    stage_root = Path(stage).resolve() if stage is not None else None
    if stage_root is not None:
        if stage_root == root or stage_root.is_relative_to(root):
            raise InfrastructureError('stage output directory must be outside workspace')
        if stage_root.exists():
            raise InfrastructureError('formation stage must be a new directory; preserve previous evidence')
        if plan['gaps'] or approved_preview_digest != plan['digest']:
            raise InfrastructureError('formation gaps or stale/unreviewed preview; rerun preview')
    if previous is not None:
        old = previous.get('formation', previous) if isinstance(previous, dict) else None
        if (not isinstance(old, dict) or old.get('schema_version') != SCHEMA
                or not isinstance(old.get('selected'), list) or any(not isinstance(p, str) for p in old['selected'])):
            raise ValueError('unsupported previous formation plan')
    # Validate every proposed artifact before the first staging side effect.
    preview = _build_result(root, audit, None, write_files=False,
                            task_context=formation['task'], formation=formation)
    if stage_root is not None and (not preview['rendered_artifacts']['validation']['ok']
                                  or preview['infrastructure_plan']['blocked']):
        raise InfrastructureError('formation validation failed; no stage written')
    if stage_root is None:
        result = preview
    else:
        result = _build_result(root, audit, stage_root, write_files=True,
                              task_context=formation['task'], formation=formation)
    if previous is not None:
        result['formation']['changes'] = {'added': sorted(set(plan['selected']) - set(old['selected'])),
            'review_only_removed': sorted(set(old['selected']) - set(plan['selected'])),
            'source_changed': old.get('source_snapshot') != plan['source_snapshot'],
            'reason': 'input/profile/source change requires review; accepted files remain untouched'}
    return result


def formation_binding_errors(root: Path, binding: Any, target_paths: list[str]) -> list[str]:
    """Revalidate observations and file authority even through the legacy merge CLI."""
    if not isinstance(binding, dict) or binding.get('schema_version') != SCHEMA:
        return ['invalid formation binding']
    if binding.get('selected') != sorted(target_paths):
        return ['formation binding target set differs from manifest']
    try:
        current = {p: x['digest'] for p, x in source_inventory(root).items()}
        if analyze_workspace(root).get('detected_stack', []) != binding.get('detected_stack', []):
            return ['formation stack changed since preview']
        if current != binding.get('source_snapshot'):
            return ['formation sources changed since preview']
        _authority(root, target_paths)
    except (OSError, ValueError, KeyError) as exc:
        return ['formation binding invalid: ' + str(exc)]
    return []
