"""Task-scoped documentation impact, reviewed section patches and completion.

Facts are explicit review inputs, not inferred semantic truth. This module owns
no status database or writer: changes use the existing CAS/recovery journal.
Recovery bytes are private workspace data and must not be published as logs.
"""
from __future__ import annotations

import difflib
import json
import os
import re
from pathlib import Path
from typing import Any

from product_agent_os import control_plane_compaction as storage
from product_agent_os.control_plane_documents import DOCUMENT_CONTRACTS
from product_agent_os.document_navigation import DOMAINS, DOMAIN_ALIASES, _headings
from product_agent_os.stage_manifest import canonical_json, content_digest

KIND = 'documentation_sync_v1'
# Event classifications are reviewer-supplied; paths alone never establish impact.
_ROOT_EVENTS = {'requirements': 'scope_change', 'sequencing': 'queue_change',
                'verification_command': 'verification_change', 'eval_policy': 'eval_applicable',
                'handoff': 'slice_outcome'}
# Core ownership remains source-owned by the existing document contract; these
# are task-event aliases, not a second registry of canonical filenames.
TRIGGERS = {event: next(name for name, contract in DOCUMENT_CONTRACTS.items() if contract['trigger'] == trigger)
            for event, trigger in _ROOT_EVENTS.items()} | {
    'architecture': 'architecture', 'decision': 'decisions',
    'api': 'api', 'schema': 'data', 'operations': 'operations',
    'evidence': 'verification', 'retained_history': 'history',
    'bugfix_no_contract': None, 'test_rerun': None,
}


def section_range(raw: bytes, anchor: str) -> tuple[int, int]:
    """Select one heading and its children; reject ambiguous/generated duplicate IDs."""
    text = raw.decode('utf-8')
    headings = _headings(text)
    matches = [offset for offset, slug in headings if slug == anchor]
    if len(matches) != 1:
        raise ValueError('section anchor missing or ambiguous')
    start = matches[0]
    line = raw[start:].splitlines()[0]
    match = re.match(rb'^(#{1,6})\s', line)
    if not match:
        raise ValueError('section selector must identify a Markdown heading')
    depth = len(match[1])
    # A repeated source heading is ambiguous even when a renderer assigns -1.
    if sum(raw[offset:].splitlines()[0] == line for offset, _ in headings) != 1:
        raise ValueError('duplicate section heading needs explicit author reconciliation')
    end = len(raw)
    for offset, _ in headings:
        other = re.match(rb'^(#{1,6})\s', raw[offset:])
        if offset > start and other and len(other[1]) <= depth:
            end = offset
            break
    return start, end


def _source(root: Path, record: dict, *, check: bool = True) -> None:
    path = storage._path(root, record['path'])
    if not re.fullmatch(r'sha256:[0-9a-f]{64}', record.get('revision', '')):
        raise ValueError('source revision required')
    if check and (not path.is_file() or content_digest(path.read_bytes()) != record['revision']):
        raise ValueError('stale or missing source')


def assess(root: Path, packet: dict, *, check_sources: bool = True) -> dict:
    """Validate a compact impact packet embedded in an existing task/report.

Each fact names evidence, a classified event, and a reviewed decision. Unknown
owners/events become handoff gaps. There is no assertion that the supplied fact
list exhausts all semantic changes; review remains a separate acceptance gate.
"""
    if type(packet.get('schema_version')) is not int or packet['schema_version'] != 1 or not isinstance(packet.get('task_id'), str) or not packet['task_id'].strip():
        raise ValueError('impact schema/task identity required')
    facts = packet.get('facts')
    if not isinstance(facts, list) or not 1 <= len(facts) <= 64:
        raise ValueError('one to 64 reviewed impact facts required')
    gaps, targets, seen = [], [], set()
    for fact in facts:
        if not isinstance(fact, dict) or any(not isinstance(fact.get(k), str) or not fact[k].strip()
                                              for k in ('id', 'event', 'changed_fact', 'reason', 'decision')):
            raise ValueError('fact identity, change, decision and reason required')
        if fact['id'] in seen:
            raise ValueError('duplicate fact identity')
        seen.add(fact['id'])
        refs = fact.get('sources')
        if not isinstance(refs, list) or not 1 <= len(refs) <= 16:
            raise ValueError('fact requires bounded source/evidence references')
        for ref in refs:
            _source(root, ref, check=check_sources)
        decision, event = fact['decision'], fact['event']
        if decision not in {'updated', 'no_change_needed', 'handoff_required'}:
            raise ValueError('unknown synchronization decision')
        if event not in TRIGGERS or decision == 'handoff_required':
            gaps.append(fact['id'] + ':owner_review_required')
            continue
        role = TRIGGERS[event]
        if role is None:
            if decision != 'no_change_needed':
                raise ValueError('no-contract events cannot authorize document writes')
            continue
        target = fact.get('target', {})
        if not target.get('owner') or not target.get('section') or target.get('role') != role:
            gaps.append(fact['id'] + ':canonical_section_owner_required')
            continue
        name = target.get('path', '')
        storage._path(root, name)
        if not name.endswith('.md') or name.split('/')[0].casefold() in {'.codex', '.git', '.aws', '.ssh'}:
            raise ValueError('impact target must be a project Markdown document')
        if role.endswith('.md') and name != role and not target.get('canonical_alias_reason'):
            raise ValueError('nonstandard canonical path requires an explicit alias reason')
        _source(root, target, check=check_sources)
        if check_sources:
            section_range(storage._path(root, name).read_bytes(), target['section'])
        if decision == 'no_change_needed' and (not isinstance(fact.get('existing_coverage'), str) or not fact['existing_coverage'].strip()):
            raise ValueError('changed contract needs section-specific existing coverage evidence')
        targets.append({'fact_id': fact['id'], 'decision': decision, **target})
    return {'task_id': packet['task_id'], 'targets': targets, 'gaps': gaps,
            'status': 'handoff_required' if gaps else 'reviewed_inputs_valid',
            'claim_ceiling': 'integrity_and_explicit_review_inputs_not_semantic_completeness'}


def owner_candidates(root: Path, event: str) -> dict:
    """Read-only owner hints shared with formation; ambiguous entries stay a gap."""
    role = TRIGGERS.get(event)
    if event not in TRIGGERS:
        return {'status': 'unknown_owner', 'paths': []}
    if role is None:
        return {'status': 'no_change_candidate', 'paths': []}
    if role.endswith('.md'):
        paths = [role] if storage._path(root, role).is_file() else []
    else:
        directories = (DOMAINS[role][0], *DOMAIN_ALIASES.get(role, ()))
        paths = [f'{directory}/{entry}' for directory in directories for entry in ('README.md', 'index.md', 'overview.md')
                 if storage._path(root, f'{directory}/{entry}').is_file()]
    return {'status': 'candidate' if len(paths) == 1 else 'owner_review_required', 'paths': paths}


def _file(name: str, before: bytes, after: bytes) -> dict:
    return {'path': name, 'before': storage._encode(before), 'after': storage._encode(after),
            'before_digest': content_digest(before), 'after_digest': content_digest(after),
            'before_bytes': len(before), 'after_bytes': len(after),
            'diff': ''.join(difflib.unified_diff(before.decode().splitlines(True), after.decode().splitlines(True), name, name))}


def _patches(root: Path, packet: dict, patches: list[dict], originals: dict[str, bytes]) -> dict[str, bytes]:
    """Replay only selected ranges; retained identifiers and links are invariants."""
    assessment = assess(root, packet, check_sources=False)
    required = {item['fact_id']: item for item in assessment['targets'] if item['decision'] == 'updated'}
    if len(patches) != len(required) or {p.get('fact_id') for p in patches} != set(required):
        raise ValueError('each updated fact needs exactly one section patch')
    ranges: dict[str, list] = {}
    for patch in patches:
        target = required[patch['fact_id']]
        name = target['path']
        raw = originals[name]
        if content_digest(raw) != target['revision']:
            raise ValueError('target revision mismatch')
        start, end = section_range(raw, target['section'])
        replacement = patch['replacement'].encode('utf-8')
        if not replacement.endswith(b'\n') or replacement.splitlines()[0] != raw[start:end].splitlines()[0]:
            raise ValueError('replacement must preserve section heading and final newline')
        if re.findall(rb'(?m)^#{1,6}\s.+', replacement)[1:] != re.findall(rb'(?m)^#{1,6}\s.+', raw[start:end])[1:]:
            raise ValueError('nested heading changes require separate reviewed structural migration')
        # Historical identifiers/evidence links cannot disappear during a section update.
        for token in re.findall(rb'\b[A-Z][A-Z0-9]+(?:-[A-Z0-9]+){1,}\b|\]\([^)]+\)', raw[start:end]):
            if token not in replacement:
                raise ValueError('identifier or evidence link removal requires retained-history migration')
        ranges.setdefault(name, []).append((start, end, replacement))
    after = dict(originals)
    for name, parts in ranges.items():
        previous_end = 0
        for start, end, _ in sorted(parts):
            if start < previous_end:
                raise ValueError('overlapping section updates')
            previous_end = end
        for start, end, replacement in sorted(parts, reverse=True):
            after[name] = after[name][:start] + replacement + after[name][end:]
        if storage._exceeds_budget(root, name, after[name], 40000):
            raise ValueError('document exceeds 40000 bytes; reviewed lossless compaction required')
    return after


def _completion(root: Path, packet: dict, completion: dict, originals: dict, after: dict) -> None:
    """Derive task-card and matching PLAN revision together, preserving other bytes."""
    from product_agent_os.task_plan_lifecycle import TaskCompletion, mark_task_implemented
    from product_agent_os.validators import validate_task_matrix_text
    if assess(root, packet, check_sources=False)['gaps']:
        raise ValueError('unresolved documentation handoff prevents implemented closure')
    name = completion['matrix_path']
    if name == 'PLAN.md' or not name.startswith(('docs/planning/', 'docs/superpowers/', 'research/')) or not name.endswith('.md'):
        raise ValueError('completion requires a source-owned task matrix and separate PLAN pointer')
    if name in after or 'PLAN.md' in after:
        raise ValueError('completion owns matrix and PLAN; conflicting section patches forbidden')
    raw = originals[name]
    start, end = section_range(raw, 'task-' + packet['task_id'].lower())
    block = raw[start:end].decode('utf-8')
    block = re.sub(r'\n<!-- product-agent-os:docs-impact:start -->.*?<!-- product-agent-os:docs-impact:end -->\r?\n?', '', block, flags=re.S)
    updated = mark_task_implemented(block, packet['task_id'], TaskCompletion(**completion['report']))
    # The receipt lives in the existing card, not a parallel status registry.
    receipt = json.loads(canonical_json(packet))
    for fact in receipt['facts']:
        target = fact.get('target')
        if target and target['path'] in after:
            target['revision'] = content_digest(after[target['path']])
    updated += '\n<!-- product-agent-os:docs-impact:start -->\n```json\n' + canonical_json(receipt) + '\n```\n<!-- product-agent-os:docs-impact:end -->\n'
    if b'\r\n' in raw[start:end]:
        updated = updated.replace('\n', '\r\n')
    matrix = raw[:start] + updated.encode() + raw[end:]
    errors = validate_task_matrix_text(matrix.decode())
    if errors:
        raise ValueError('invalid completed task matrix: ' + str(errors))
    if storage._exceeds_budget(root, name, matrix, 40000):
        raise ValueError('matrix exceeds applicable byte budget; no automatic split')
    pointer_raw = originals['PLAN.md']
    pointer = pointer_raw.decode()
    pattern = r'(<!-- product-agent-os:current-state:start -->\s*```json\s*)(.*?)(\s*```\s*<!-- product-agent-os:current-state:end -->)'
    matches = list(re.finditer(pattern, pointer, re.S))
    if len(matches) != 1:
        raise ValueError('one current-state PLAN pointer required')
    match = matches[0]
    data = json.loads(match[2])
    refs = [ref for ref in data['sources'] if ref['path'] == name]
    if data.get('schema_version') != 1 or len(refs) != 1 or refs[0]['revision'] != content_digest(raw):
        raise ValueError('stale or ambiguous matrix revision pin')
    selected = []
    for item in re.finditer(r'\{[^{}]*\}', match[2]):
        if json.loads(item[0]).get('path') == name:
            selected.append(item)
    if len(selected) != 1:
        raise ValueError('unsupported pointer structure')
    item = selected[0]
    revised = item[0].replace(refs[0]['revision'], content_digest(matrix))
    begin = match.start(2) + item.start()
    finish = match.start(2) + item.end()
    after[name] = matrix
    after['PLAN.md'] = (pointer[:begin] + revised + pointer[finish:]).encode()
    if storage._exceeds_budget(root, 'PLAN.md', after['PLAN.md'], 40000):
        raise ValueError('PLAN exceeds byte budget')


def propose(root: Path, packet: dict, patches: list[dict], *, completion: dict | None = None) -> dict:
    """Prepare exact before/after bytes without writing or claiming owner acceptance."""
    root = root.resolve()
    assessment = assess(root, packet)
    names = {t['path'] for t in assessment['targets'] if t['decision'] == 'updated'}
    originals = {name: storage._path(root, name).read_bytes() for name in names}
    after = _patches(root, packet, patches, originals)
    if completion is not None:
        for name in (completion['matrix_path'], 'PLAN.md'):
            if name in originals:
                raise ValueError('completion/section ownership overlap')
            originals[name] = storage._path(root, name).read_bytes()
        _completion(root, packet, completion, originals, after)
        names = set(originals)
    plan = {'schema_version': 1, 'kind': KIND, 'workspace_digest': content_digest(os.path.normcase(str(root))),
            'impact': packet, 'patches': patches, 'completion': completion,
            'files': [_file(name, originals[name], after[name]) for name in sorted(names) if originals[name] != after[name]],
            'closure': 'handoff_required' if assessment['gaps'] else 'documentation_ready',
            'warnings': [name + ':over_32000_bytes' for name in sorted(names) if len(after[name]) > 32000],
            # Include even no-op target bytes so validation can replay without a new writer.
            'originals': {name: storage._encode(raw) for name, raw in originals.items()}}
    plan['digest'] = storage._digest(plan)
    validate_proposal(root, plan)
    return plan


def validate_proposal(root: Path, plan: dict, *, check_sources: bool = True) -> None:
    """Replay section edits; a recomputed digest alone cannot authorize arbitrary bytes."""
    if plan.get('kind') != KIND or plan.get('schema_version') != 1 or plan.get('digest') != storage._digest(plan):
        raise ValueError('invalid documentation proposal')
    if plan.get('workspace_digest') != content_digest(os.path.normcase(str(root.resolve()))):
        raise ValueError('wrong workspace')
    assessment = assess(root, plan['impact'], check_sources=check_sources)
    originals = {name: storage._decode(raw) for name, raw in plan['originals'].items()}
    expected_names = {t['path'] for t in assessment['targets'] if t['decision'] == 'updated'}
    completion = plan.get('completion')
    patch_names = set(expected_names)
    if completion is not None:
        expected_names.update((completion['matrix_path'], 'PLAN.md'))
    if set(originals) != expected_names:
        raise ValueError('unexpected proposal target')
    if len({name.casefold() for name in originals}) != len(originals):
        raise ValueError('case alias conflict')
    after = _patches(root, plan['impact'], plan['patches'], {name: originals[name] for name in patch_names})
    if completion is not None:
        _completion(root, plan['impact'], completion, originals, after)
    expected = [_file(name, originals[name], after[name]) for name in sorted(originals) if originals[name] != after[name]]
    if plan['files'] != expected:
        raise ValueError('section preservation replay failed')
    if plan['closure'] != ('handoff_required' if assessment['gaps'] else 'documentation_ready'):
        raise ValueError('invalid closure claim')


def apply(root: Path, plan: dict, *, approved_digest: str, after_write=None) -> dict:
    """Apply reviewed local changes; repeated identical requests do not write."""
    root = root.resolve()
    validate_proposal(root, plan, check_sources=False)
    storage._authority(root, [f['path'] for f in plan['files']])
    if approved_digest != plan['digest']:
        raise ValueError('exact proposal approval required')
    if not plan['files']:
        assess(root, plan['impact'])
        if any(storage._raw(storage._path(root, name)) != storage._decode(raw) for name, raw in plan['originals'].items()):
            raise ValueError('stale no-op completion snapshot')
        return {'status': 'no_change_needed', 'writes': 0, 'closure': plan['closure']}
    already = all(storage._raw(storage._path(root, f['path'])) == storage._decode(f['after']) for f in plan['files'])
    changed = {f['path'] for f in plan['files']}
    for fact in plan['impact']['facts']:
        for ref in fact['sources']:
            if ref['path'] not in changed:
                _source(root, ref)
        if fact.get('target') and fact['target']['path'] not in changed:
            _source(root, fact['target'])
    if not already:
        assess(root, plan['impact'])
    def check_after_write(index):
        if after_write:
            after_write(index)
        # An external editor can change evidence as well as a target. Check the
        # unaffected sources again before accepting a multi-file operation.
        changed = {f['path'] for f in plan['files']}
        for fact in plan['impact']['facts']:
            for ref in fact['sources']:
                if ref['path'] not in changed:
                    _source(root, ref)
            if fact.get('target') and fact['target']['path'] not in changed:
                _source(root, fact['target'])
    result = storage._apply_validated(root, plan, approved_digest=approved_digest, after_write=check_after_write)
    return {**result, 'closure': plan['closure']}
