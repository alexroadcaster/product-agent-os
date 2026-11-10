"""Versioned document content, separate from task state and acceptance receipts.

Existing Markdown remains readable in structural mode. Schema v1 adds an
explicit data block; headings and language never determine acceptance.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import PurePosixPath
from typing import Any

DOCUMENT_CONTRACTS = {
    'AGENTS.md': {'owns': 'durable_rules', 'fields': ('rules', 'boundaries'), 'trigger': 'instruction_change'},
    'REQUIREMENTS.md': {'owns': 'scope_and_acceptance', 'fields': ('goal', 'scope', 'acceptance', 'constraints'), 'trigger': 'scope_change'},
    'PLAN.md': {'owns': 'sequencing', 'fields': ('tasks', 'dependencies', 'next_step'), 'trigger': 'queue_change'},
    'TEST.md': {'owns': 'verification', 'fields': ('checks', 'evidence_limits'), 'trigger': 'verification_change'},
    'EVALS.md': {'owns': 'quality_rubric', 'fields': ('cases', 'thresholds', 'claim_limits'), 'trigger': 'eval_applicable'},
    'RUNLOG.md': {'owns': 'current_handoff', 'fields': ('result', 'evidence', 'risks', 'next_step'), 'trigger': 'slice_outcome'},
}
DATA_START = '<!-- product-agent-os:data:start -->'
DATA_END = '<!-- product-agent-os:data:end -->'


def is_detailed_planning_matrix(relative: str, text: str) -> bool:
    """Recognize detailed planning content, never exempt an entire directory.

    The owner's exception is size-only. Navigation and control-plane filenames
    retain their budgets even if someone embeds task cards in them.
    """
    path = PurePosixPath(relative)
    reserved = {name.casefold() for name in DOCUMENT_CONTRACTS} | {'index.md', 'readme.md'}
    if (path.parts[:2] != ('docs', 'planning') or '..' in path.parts
            or path.suffix.lower() != '.md' or path.name.casefold() in reserved
            or path.name.casefold().startswith(('index.', 'readme.'))):
        return False
    # Ignore examples in fenced blocks: an example card does not change a
    # navigation document's information ownership.
    content = re.sub(r'(?ms)^\s*(`{3,}|~{3,}).*?^\s*\1\s*$', '', text)
    if re.search(r'(?m)^\s*(?:`{3,}|~{3,})', content):
        return False  # An unclosed example is not an authoritative task matrix.
    cards = (re.search(r'(?m)^### Task `[^`]+`', content)
             and re.search(r'(?m)^- ID:\s*\S', content)
             and re.search(r'(?m)^- Status:\s*\S', content)
             and re.search(r'(?m)^- Acceptance criteria:\s*\S', content))
    if cards:
        return True
    for line in content.splitlines():
        if not line.lstrip().startswith('|'):
            continue
        cells = {cell.strip().strip('*').casefold() for cell in line.strip().strip('|').split('|')}
        if (cells & {'id', 'ид'} and cells & {'task', 'задача', 'название задачи'}
                and cells & {'status', 'статус'}
                and cells & {'acceptance criteria', 'критерии приёмки', 'критерии приемки'}):
            return True
    return False


def read_document_data(text: str) -> dict[str, Any]:
    """Read exactly one schema block; ambiguous/malformed content fails closed."""
    # Markdown delimiters accept Windows line endings; the receipt digest still
    # binds the original bytes in document_readiness, not this parser view.
    text = text.replace('\r\n', '\n')
    if DATA_START not in text and DATA_END not in text:
        return {}
    if text.count(DATA_START) != 1 or text.count(DATA_END) != 1:
        raise ValueError('duplicate or unpaired document data markers')
    start, end = text.index(DATA_START), text.index(DATA_END)
    if end < start:
        raise ValueError('reversed document data markers')
    body = text[start + len(DATA_START):end].strip()
    if not body.startswith('```json\n') or not body.endswith('\n```'):
        raise ValueError('invalid document data block')
    data = json.loads(body[8:-4])
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        raise ValueError('unsupported document schema')
    name = data.get('document')
    if not isinstance(name, str) or name not in DOCUMENT_CONTRACTS:
        raise ValueError('unknown document identity')
    populate_document(name, {k: v for k, v in data.items() if k not in {'schema_version', 'document'}})
    return data


def populate_document(name: str, packet: dict[str, Any]) -> str:
    """Render supplied facts without inferring verification or owner decisions.

    JSON escaping keeps source content inside a data block, even when it contains
    Markdown fences, template syntax or HTML markers. Consumers treat it as data.
    """
    contract = DOCUMENT_CONTRACTS[name]
    if set(packet) - {'source', *contract['fields']}:
        raise ValueError('unknown document fields; explicit schema migration required')
    if not isinstance(packet.get('source'), str) or not packet['source'].strip():
        raise ValueError('document packet requires source provenance')
    data = {'schema_version': 1, 'document': name, 'source': packet['source']}
    for field in contract['fields']:
        value = packet.get(field)
        if value is not None and not isinstance(value, (str, list, dict)):
            raise ValueError(f'invalid document field: {field}')
        data[field] = value
    encoded = json.dumps(data, ensure_ascii=False, indent=2)
    for char in '<>`':
        encoded = encoded.replace(char, f'\\u{ord(char):04x}')
    return f'{DATA_START}\n```json\n{encoded}\n```\n{DATA_END}\n'


def scoped_document(name: str, section: str, task: dict[str, Any]) -> str:
    """Compact opt-in scaffold; reuse legacy templates outside scoped routing."""
    packet = dict(task.get('documents', {}).get(name, {}))
    packet.setdefault('source', 'task:' + task['task_id'])
    if name == 'REQUIREMENTS.md':
        packet.setdefault('goal', task['intent'])
        packet.setdefault('scope', task['changed_paths'])
        packet.setdefault('acceptance', task['acceptance'])
    elif name == 'AGENTS.md':
        packet.setdefault('rules', ['Preserve user content; separate instructions from task data.',
                                   'Read applicable project instructions; verify before completion claims.'])
        packet.setdefault('boundaries', ['Staging is not activation or target-write permission.',
                                        'No credentials, raw private logs or customer data in artifacts.'])
    return (f'# {name}\n\n<!-- product-agent-os:start {section} -->\n'
            f'Information owner: {DOCUMENT_CONTRACTS[name]["owns"]}\n'
            'Readiness: scaffold until required facts are supplied; review and acceptance need receipts.\n\n'
            + populate_document(name, packet) + f'<!-- product-agent-os:end {section} -->\n')


def document_readiness(name: str, text: str, receipt: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return content/review/acceptance state independently of file presence."""
    contract = DOCUMENT_CONTRACTS[name]
    digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
    result: dict[str, Any] = {'state': 'scaffold', 'owner': contract['owns'],
                             'source_digest': digest, 'missing_fields': [], 'errors': []}
    try:
        data = read_document_data(text)
    except ValueError as exc:
        result['errors'] = [str(exc)]
        return result
    result['missing_fields'] = [key for key in contract['fields'] if not data.get(key)]
    if not data:
        result['errors'].append('content_schema_missing; use explicit legacy structural mode')
        return result
    if data.get('document') != name or not data.get('source'):
        result['errors'].append('document identity or source missing')
        return result
    if not result['missing_fields']:
        result['state'] = 'draft'
    if receipt:
        if receipt.get('source_digest') != digest:
            result['state'] = 'stale'
        elif result['state'] == 'draft' and receipt.get('reviewer') and receipt.get('evidence'):
            result['state'] = 'reviewed'
            if receipt.get('owner_decision') == 'accepted' and receipt.get('owner'):
                result['state'] = 'accepted'
    return result
